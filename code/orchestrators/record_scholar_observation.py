#!/usr/bin/env python3
"""Record an operator-attested direct authenticated Google Scholar observation.

Sources: the operator-supplied observation (``--as-of`` plus the six metrics
Scholar shows: all-time and since-2021 citations, h-index, i10-index) and the
current ``data/scholar-snapshot.json``.  Nothing is fetched; the tool cannot
see whether a profile was viewed while signed in, so a recording run requires
``--attest-direct-authenticated`` and the receipt's ``direct`` and
``authenticated`` assertions are never inferred.  The read-only modes
(``--check`` and ``--dry-run``) assert nothing and need no attestation.  The six
numbers are cross-checked before anything is touched: each since-2021 value must
be at most its all-time counterpart, and each h-index and i10-index at most the
citations in its own column.

Outputs, written together: ``data/scholar-snapshot.json`` (new values, method,
the previous history entry marked superseded, one appended history entry) and
``data/scholar-verification-receipt.json`` (bound to the SHA-256 of the exact
snapshot bytes written).  Both are validated from disk with
``validate_scholar_snapshot_receipt`` before the command succeeds; on any
failure the original bytes are restored.

Usage:
  python code/orchestrators/record_scholar_observation.py \\
      --as-of YYYY-MM-DD --citations N --h-index N --i10-index N \\
      --since-2021-citations N --since-2021-h-index N --since-2021-i10-index N \\
      --attest-direct-authenticated            # record the observation (the only mode that writes)
  ... --dry-run                                # print old -> new and the predicted SHA-256, write nothing
  ... --check                                  # exit 0 only if the pair already records exactly this

Optional text: ``--verified-at`` (timezone-qualified; default now, UTC),
``--method`` and ``--source`` (default to neutral wording that asserts nothing
the operator did not attest: no browser, no app), ``--history-note`` (descriptor
for the new history entry, which always ends with an em dash and "current source
of truth.").  Put interface details such as which browser in ``--source`` or
``--method`` only when you attest them.

``verified_at`` is bounded by ``as_of``: when it is not stated with
``--verified-at`` it is taken from the clock, and a clock more than one day after
``as_of`` is refused (a receipt must not vouch for a verification nobody stated);
stating ``--verified-at`` explicitly lifts that bound.

Re-running the same observation is a no-op ("already recorded").  If only the
receipt is missing or invalid (including undecodable bytes), the same command
regenerates just the receipt, reusing the existing receipt's ``verified_at`` when
it still vouches for this observation and otherwise applying the rule above.
An observation must be strictly newer than the recorded ``as_of``.
If a write fails the original bytes are restored; if that restoration itself
fails the command says so, names the files, and the same command repairs the pair.

Afterwards run ``sync_scholar_metrics.py`` to propagate the snapshot, then the
regenerate/settle flow printed at the end of a successful run.  This command
is deliberately outside ``regenerate_all.py``: an attested observation cannot
be derived from repository files.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]

from docxology_tools.scholar_verification import (  # noqa: E402
    SCHOLAR_METRIC_FIELDS,
    SCHOLAR_RECEIPT_RELATIVE_PATH,
    SCHOLAR_SINCE_2021_KEY,
    SCHOLAR_SNAPSHOT_RELATIVE_PATH,
    build_observation_artifacts,
    build_receipt_bytes,
    format_verified_at,
    observation_matches_snapshot,
    observation_timing_errors,
    parse_observation_date,
    parse_verified_at,
    reusable_receipt_verified_at,
    sha256_bytes,
    validate_observation,
    validate_scholar_snapshot_receipt,
)

SNAPSHOT = REPO_ROOT / SCHOLAR_SNAPSHOT_RELATIVE_PATH
RECEIPT = REPO_ROOT / SCHOLAR_RECEIPT_RELATIVE_PATH

NEXT_STEPS = (
    "uv run python3 code/orchestrators/sync_scholar_metrics.py",
    "uv run python3 code/orchestrators/regenerate_all.py --validate",
    "uv run python3 code/orchestrators/settle.py --tier full --dry-run   # inspect, then re-run without --dry-run",
)


class Refusal(Exception):
    """A recording the tool will not make; the message says why."""


def _non_negative_int(text: str) -> int:
    """argparse type: ASCII digits only, so booleans, signs and floats are refused."""
    if not re.fullmatch(r"[0-9]+", text):
        raise argparse.ArgumentTypeError(f"expected a non-negative integer, got {text!r}")
    return int(text)


def _calendar_date(text: str) -> str:
    """argparse type: a strict YYYY-MM-DD calendar date, returned unchanged."""
    try:
        parse_observation_date(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc
    return text.strip()


def _timestamp(text: str) -> datetime:
    """argparse type: a timezone-qualified ISO timestamp (trailing Z accepted)."""
    try:
        return parse_verified_at(text)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc)) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Record a direct authenticated Google Scholar observation: update the snapshot and write its SHA-256-bound receipt."
    )
    parser.add_argument("--as-of", required=True, type=_calendar_date, metavar="YYYY-MM-DD", help="calendar date of the observation")
    parser.add_argument("--citations", required=True, type=_non_negative_int, help="all-time citations")
    parser.add_argument("--h-index", required=True, type=_non_negative_int, help="all-time h-index")
    parser.add_argument("--i10-index", required=True, type=_non_negative_int, help="all-time i10-index")
    parser.add_argument("--since-2021-citations", required=True, type=_non_negative_int, help="since-2021 citations")
    parser.add_argument("--since-2021-h-index", required=True, type=_non_negative_int, help="since-2021 h-index")
    parser.add_argument("--since-2021-i10-index", required=True, type=_non_negative_int, help="since-2021 i10-index")
    parser.add_argument(
        "--attest-direct-authenticated",
        action="store_true",
        help=(
            "required to write (not for --dry-run or --check): you viewed the canonical profile "
            "directly while signed in (not a cached or anonymous view)"
        ),
    )
    parser.add_argument(
        "--verified-at",
        type=_timestamp,
        metavar="TIMESTAMP",
        help=(
            "timezone-qualified ISO timestamp (default: now, UTC, refused when more than one day "
            "after --as-of; receipt-only recovery reuses the existing receipt's value when it still fits)"
        ),
    )
    parser.add_argument(
        "--method",
        help=(
            "method text for the snapshot and receipt (default: neutral template that names no browser or app; "
            "add interface details such as which browser only if you attest them)"
        ),
    )
    parser.add_argument(
        "--source",
        help=(
            "receipt source text (default: 'Direct authenticated observation of <profile URL>'; "
            "add interface details such as which browser only if you attest them)"
        ),
    )
    parser.add_argument("--history-note", help="descriptor for the new history entry (the 'current source of truth' suffix is added)")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="print old -> new values and the predicted snapshot SHA-256; write nothing")
    mode.add_argument("--check", action="store_true", help="read-only: exit 0 only if the on-disk pair already records exactly this observation")
    return parser


def observation_from_args(args: argparse.Namespace) -> dict[str, Any]:
    return {
        "as_of": args.as_of,
        "citations": args.citations,
        "h_index": args.h_index,
        "i10_index": args.i10_index,
        SCHOLAR_SINCE_2021_KEY: {
            "citations": args.since_2021_citations,
            "h_index": args.since_2021_h_index,
            "i10_index": args.since_2021_i10_index,
        },
    }


def _read_bytes(path: Path, label: str, *, required: bool) -> bytes | None:
    """Read an on-disk source, refusing symlinks; a missing optional file is None."""
    rel = _display(path)
    if path.is_symlink():
        raise Refusal(f"{label} must not be a symlink: {rel}")
    try:
        return path.read_bytes()
    except FileNotFoundError:
        if required:
            raise Refusal(f"missing {label}: {rel}") from None
        return None
    except OSError as exc:
        raise Refusal(f"unable to read {label} {rel}: {exc}") from exc


def _load_snapshot(raw: bytes) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Refusal(f"data/scholar-snapshot.json is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise Refusal("data/scholar-snapshot.json must be a JSON object")
    return value


def _atomic_write(path: Path, data: bytes) -> None:
    """Replace ``path`` with ``data`` via a same-directory temp file (bytes, no newline translation)."""
    if path.is_symlink():
        raise OSError(f"refusing to write through a symlink: {path.as_posix()}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        if path.exists():
            shutil.copymode(path, temporary)
        else:
            os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _display(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _restore(originals: dict[Path, bytes | None]) -> list[str]:
    """Put the original bytes back (or remove a file that did not exist); return any failures."""
    failures: list[str] = []
    for path, original in originals.items():
        try:
            if original is None:
                path.unlink(missing_ok=True)
            else:
                _atomic_write(path, original)
        except OSError as exc:
            failures.append(f"{_display(path)}: {exc}")
    return failures


def _prevalidate(snapshot_bytes: bytes, receipt_bytes: bytes) -> list[str]:
    """Run the on-disk validator over the candidate pair in a scratch tree first."""
    with tempfile.TemporaryDirectory(prefix="scholar-observation-") as scratch:
        root = Path(scratch)
        (root / SCHOLAR_SNAPSHOT_RELATIVE_PATH).parent.mkdir(parents=True)
        (root / SCHOLAR_SNAPSHOT_RELATIVE_PATH).write_bytes(snapshot_bytes)
        (root / SCHOLAR_RECEIPT_RELATIVE_PATH).write_bytes(receipt_bytes)
        return validate_scholar_snapshot_receipt(root)


def _validate_pair(root: Path) -> list[str]:
    """Validate the on-disk pair; undecodable bytes are reported as errors by the shared loader."""
    return validate_scholar_snapshot_receipt(root)


def _delta(old: object, new: object) -> str:
    if type(old) is int and type(new) is int:
        return f"{old} -> {new} ({new - old:+d})"
    return f"{old!r} -> {new!r}"


def _describe_changes(old: dict[str, Any], new: dict[str, Any]) -> list[str]:
    lines = [f"  as_of       {old.get('as_of')!r} -> {new.get('as_of')!r}"]
    for field in SCHOLAR_METRIC_FIELDS:
        lines.append(f"  {field:<11} {_delta(old.get(field), new.get(field))}")
    old_since = old.get(SCHOLAR_SINCE_2021_KEY) if isinstance(old.get(SCHOLAR_SINCE_2021_KEY), dict) else {}
    new_since = new.get(SCHOLAR_SINCE_2021_KEY) if isinstance(new.get(SCHOLAR_SINCE_2021_KEY), dict) else {}
    for field in SCHOLAR_METRIC_FIELDS:
        lines.append(f"  since_2021.{field:<9} {_delta(old_since.get(field), new_since.get(field))}")
    old_history = old.get("history") or []
    new_history = new.get("history") or []
    if len(new_history) >= 2 and old_history:
        lines.append(f"  history[{len(old_history) - 1}].note  {old_history[-1].get('note')!r}")
        lines.append(f"      -> {new_history[-2].get('note')!r}")
        lines.append(f"  history[+1]  {json.dumps(new_history[-1], ensure_ascii=False)}")
    return lines


def _warnings(old: dict[str, Any], new: dict[str, Any]) -> list[str]:
    """A decrease is legitimate (the history records corrections) but worth a look."""
    return [
        f"warning: {field} decreased ({old[field]} -> {new[field]}); recording anyway"
        for field in SCHOLAR_METRIC_FIELDS
        if type(old.get(field)) is int and type(new.get(field)) is int and new[field] < old[field]
    ]


def _check(snapshot: dict[str, Any], observation: dict[str, Any], pair_errors: list[str]) -> int:
    recorded = observation_matches_snapshot(snapshot, observation)
    if recorded and not pair_errors:
        print(f"ok: snapshot and receipt already record the observation as of {observation['as_of']}")
        return 0
    if not recorded:
        print(
            f"not recorded: data/scholar-snapshot.json is as of {snapshot.get('as_of')!r} "
            f"and does not match the observation as of {observation['as_of']}"
        )
    for error in pair_errors:
        print(f"  - {error}")
    return 1


def run(args: argparse.Namespace, now: datetime) -> int:
    snapshot_raw = _read_bytes(SNAPSHOT, "Scholar snapshot", required=True)
    receipt_raw = _read_bytes(RECEIPT, "Scholar verification receipt", required=False)
    assert snapshot_raw is not None
    snapshot = _load_snapshot(snapshot_raw)
    observation = observation_from_args(args)
    problems = validate_observation(observation)
    if problems:
        raise Refusal("; ".join(problems))

    pair_errors = _validate_pair(REPO_ROOT)
    recorded = observation_matches_snapshot(snapshot, observation)
    if args.check:
        return _check(snapshot, observation, pair_errors)
    if recorded and not pair_errors:
        print(f"already recorded: snapshot and receipt hold the observation as of {observation['as_of']}; nothing written")
        return 0

    as_of = parse_observation_date(observation["as_of"])
    verified_at = args.verified_at
    verified_reused = False
    if verified_at is None and recorded:
        # Receipt-only recovery: keep the instant the lost receipt stated, when it still fits.
        verified_at = reusable_receipt_verified_at(receipt_raw, as_of, now)
        verified_reused = verified_at is not None
    if verified_at is None:
        verified_at = now.astimezone(timezone.utc).replace(microsecond=0)
    verified_text = format_verified_at(verified_at)
    current_as_of = None
    if not recorded:
        try:
            current_as_of = parse_observation_date(snapshot.get("as_of"))
        except ValueError as exc:
            raise Refusal(f"recorded snapshot as_of is unusable ({exc})") from exc
    timing = observation_timing_errors(
        as_of,
        verified_at,
        now,
        current_as_of=current_as_of,
        verified_at_defaulted=args.verified_at is None,
    )
    if timing:
        raise Refusal("; ".join(timing))

    try:
        if recorded:
            # Crash recovery: the snapshot already holds this observation, so only the
            # receipt is regenerated, bound to the snapshot bytes exactly as they sit on disk.
            if args.method is not None and args.method != snapshot.get("method"):
                raise Refusal("--method differs from the recorded snapshot method; receipt-only recovery cannot change it")
            snapshot_bytes = snapshot_raw
            receipt_bytes = build_receipt_bytes(snapshot_bytes, verified_at=verified_text, source=args.source)
        else:
            snapshot_bytes, receipt_bytes = build_observation_artifacts(
                snapshot,
                observation,
                verified_at=verified_text,
                method=args.method,
                source=args.source,
                history_note=args.history_note,
            )
    except ValueError as exc:
        raise Refusal(str(exc)) from exc
    candidate_errors = _prevalidate(snapshot_bytes, receipt_bytes)
    if candidate_errors:
        raise Refusal("candidate pair failed validation: " + "; ".join(candidate_errors))

    new_snapshot = json.loads(snapshot_bytes.decode("utf-8"))
    digest = sha256_bytes(snapshot_bytes)
    heading = "receipt-only recovery" if recorded else "observation"
    print(f"Scholar {heading} as of {observation['as_of']} (verified_at {verified_text})")
    if recorded:
        print("  snapshot already holds this observation; only the receipt is regenerated")
        if verified_reused:
            print("  verified_at reused from the existing receipt")
        if args.history_note is not None:
            print("  ignoring --history-note: receipt-only recovery changes no history")
    else:
        for line in _describe_changes(snapshot, new_snapshot):
            print(line)
    print(f"  snapshot_sha256 {digest}")
    for warning in _warnings(snapshot, new_snapshot):
        print(warning, file=sys.stderr)
    if args.dry_run:
        print("dry run: nothing written")
        print(
            "a real run requires --attest-direct-authenticated: your statement that you viewed the "
            "canonical profile directly while signed in"
        )
        return 0

    # Snapshot first, then receipt: a crash between the two leaves a SHA mismatch, which
    # fails closed and is repaired by re-running the same command (receipt-only recovery).
    originals: dict[Path, bytes | None] = {SNAPSHOT: snapshot_raw, RECEIPT: receipt_raw}
    replaced: dict[Path, bytes | None] = {}
    failures: list[str] = []
    restore_failures: list[str] = []
    committed = False
    try:
        for path, content in ((SNAPSHOT, snapshot_bytes), (RECEIPT, receipt_bytes)):
            if content == originals[path]:
                continue
            _atomic_write(path, content)
            replaced[path] = originals[path]
        failures = _validate_pair(REPO_ROOT)
        if SNAPSHOT.read_bytes() != snapshot_bytes or RECEIPT.read_bytes() != receipt_bytes:
            failures.append("on-disk bytes differ from the bytes written")
        committed = not failures
    except OSError as exc:
        failures = [f"write failed: {exc}"]
    finally:
        if not committed:
            restore_failures = _restore(replaced)
            for failure in restore_failures:
                print(f"CRITICAL: could not restore {failure}", file=sys.stderr)
    if not committed:
        reason = "; ".join(failures)
        if restore_failures:
            raise Refusal(
                f"recording failed AND restoration FAILED, so the data pair may be inconsistent: {reason}. "
                f"Not restored: {'; '.join(restore_failures)}. The SHA-256 binding fails closed until the pair "
                "is repaired. Fix the cause (permissions, disk space), then re-run this exact command: it "
                "regenerates just the receipt when the snapshot already holds the observation, and records "
                "the full observation when the snapshot was rolled back. Alternatively restore both files from "
                f"version control (git restore {SCHOLAR_SNAPSHOT_RELATIVE_PATH.as_posix()} "
                f"{SCHOLAR_RECEIPT_RELATIVE_PATH.as_posix()}). Confirm with --check."
            )
        if not replaced:
            raise Refusal(f"recording failed before any file was replaced; both files are unchanged: {reason}")
        raise Refusal(f"recording failed and every replaced file was restored: {reason}")

    print(f"wrote {SCHOLAR_SNAPSHOT_RELATIVE_PATH.as_posix()} and {SCHOLAR_RECEIPT_RELATIVE_PATH.as_posix()}")
    print("next steps:")
    for command in NEXT_STEPS:
        print(f"  {command}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not (args.attest_direct_authenticated or args.dry_run or args.check):
        parser.error(
            "--attest-direct-authenticated is required to write: the receipt asserts a direct, authenticated "
            "observation, and that is never inferred (--dry-run and --check do not need it)"
        )
    try:
        return run(args, datetime.now(timezone.utc))
    except Refusal as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
