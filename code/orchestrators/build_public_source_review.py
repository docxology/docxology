#!/usr/bin/env python3
"""Build a dated, review-only public-source evidence report.

The report is intentionally a boundary, not an updater: it reads refreshed
public-source evidence and curated ledgers, then writes JSON and Markdown under
``reports/``.  It never edits claims, Scholar metrics, bibliography rows,
paper metadata, or repository classifications.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from typing import Iterable

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from public_source_review import (  # noqa: E402
    build_review_report,
    render_json,
    render_markdown,
    validate_review_report,
)
from release_controls import source_payload_commit, source_tree_sha  # noqa: E402
from report_paths import control_tail_worktree_state, source_commit, source_worktree_state  # noqa: E402


def _utc_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _parse_date(value: str) -> str:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError("date must use YYYY-MM-DD") from exc


def _repo_path(value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def _latest(pattern: str, *, exclude: Iterable[Path] = ()) -> Path | None:
    excluded = {path.resolve() for path in exclude}
    paths = sorted((REPO_ROOT / "reports").glob(pattern), key=lambda path: path.name, reverse=True)
    return next((path for path in paths if path.resolve() not in excluded), None)


def _latest_doi_review() -> Path | None:
    candidates = sorted((REPO_ROOT / "reports").glob("doi_role_reconciliation_*.json"), key=lambda path: path.name, reverse=True)
    if not candidates:
        return None
    # A dated apply receipt is more authoritative than a sidecar proposal from
    # the same day.  Fall back to the newest proposal only when no receipt exists.
    for path in candidates:
        try:
            if '"status": "applied"' in path.read_text(encoding="utf-8"):
                return path
        except OSError:
            continue
    return candidates[0]


def _default_markdown_path(report: Path) -> Path:
    return report.with_suffix(".md")


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


def _atomic_write(path: Path, content: str) -> None:
    """Write an explicitly requested review artifact through a sibling file.

    Review reports support an isolated external report directory for tests and
    manual review. Repository-local generated writers use the stricter shared
    output mapping; this intentionally scoped helper preserves that external
    review workflow while avoiding a partially written final file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def _prior_snapshot_from_existing_report(report_path: Path | None) -> Path | None:
    """Preserve an explicitly chosen comparison baseline during ``--check``.

    The review may be opened to resolve a particular issue whose baseline is
    older than the immediately prior daily snapshot.  Replacing it with the
    newest file during a no-write check would silently erase observations.
    """
    if report_path is None or not report_path.is_file():
        return None
    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    inputs = payload.get("inputs") if isinstance(payload, dict) else None
    provenance = inputs.get("previous_public_source_snapshot") if isinstance(inputs, dict) else None
    raw = provenance.get("path") if isinstance(provenance, dict) else None
    if not isinstance(raw, str) or not raw or "\\" in raw:
        return None
    candidate = _repo_path(raw)
    try:
        resolved = candidate.resolve()
        if candidate.is_absolute():
            # Explicit custom reports may be rendered in an isolated review
            # directory. Preserve only a sibling snapshot, never an arbitrary
            # external path named inside an untrusted report.
            if resolved.parent != report_path.parent.resolve():
                return None
        else:
            resolved.relative_to(REPO_ROOT.resolve())
    except (OSError, ValueError):
        return None
    return candidate if candidate.is_file() else None


def _resolve_inputs(args: argparse.Namespace, *, report_path: Path | None = None) -> dict[str, Path | None]:
    snapshot = _repo_path(args.snapshot) if args.snapshot else _latest("public_source_snapshot_*.json")
    if snapshot is None:
        raise ValueError("missing public-source snapshot; run refresh_public_sources.py first")
    previous = _repo_path(args.previous_snapshot) if args.previous_snapshot else _prior_snapshot_from_existing_report(report_path)
    if previous is None:
        previous = _latest("public_source_snapshot_*.json", exclude=[snapshot])
    return {
        "snapshot_path": snapshot,
        "inventory_path": _repo_path(args.inventory) if args.inventory else _latest("public_source_inventory_*.json"),
        "paired_publications_path": _repo_path(args.paired_publications) if args.paired_publications else _latest("paired_publications_*.json"),
        "pair_decisions_path": _repo_path(args.pair_decisions) if args.pair_decisions else REPO_ROOT / "data/paired-publication-decisions.json",
        "doi_review_path": _repo_path(args.doi_review) if args.doi_review else _latest_doi_review(),
        "repository_classification_path": _repo_path(args.repository_classification)
        if args.repository_classification
        else REPO_ROOT / "data/repository-classification.json",
        "claims_path": _repo_path(args.claims) if args.claims else REPO_ROOT / "data/claims.json",
        "scholar_snapshot_path": _repo_path(args.scholar_snapshot)
        if args.scholar_snapshot
        else REPO_ROOT / "data/scholar-snapshot.json",
        "scholar_receipt_path": _repo_path(args.scholar_verification_receipt)
        if args.scholar_verification_receipt
        else None,
        "previous_snapshot_path": previous,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", help="JSON output path (default: reports/public_source_review_DATE.json)")
    parser.add_argument("--markdown-report", help="Markdown output path (default: JSON path with .md suffix)")
    parser.add_argument("--date", type=_parse_date, help="Report date in YYYY-MM-DD (default: UTC today)")
    parser.add_argument("--check", action="store_true", help="Re-render existing report inputs and fail on any JSON or Markdown difference")
    parser.add_argument("--snapshot", help="Public-source snapshot JSON; default is newest dated snapshot")
    parser.add_argument("--previous-snapshot", help="Optional prior snapshot for observation diffing")
    parser.add_argument("--inventory", help="Public-source inventory JSON; default is newest dated inventory")
    parser.add_argument("--paired-publications", help="GitHub–Zenodo pairing report; default is newest dated report")
    parser.add_argument(
        "--pairing-refresh-status",
        choices=("auto", "failed"),
        default=None,
        help="Record a failed current pairing refresh rather than treating an older successful report as current",
    )
    parser.add_argument(
        "--pairing-refresh-note",
        default="",
        help="Verbatim bounded note for a failed pairing refresh (for example, API rate-limit evidence)",
    )
    parser.add_argument("--pair-decisions", help="Durable pairing decisions JSON")
    parser.add_argument("--doi-review", help="DOI-role reconciliation/audit JSON")
    parser.add_argument("--repository-classification", help="Repository classification queue JSON")
    parser.add_argument("--claims", help="Claims ledger JSON")
    parser.add_argument("--scholar-snapshot", help="Canonical Scholar snapshot JSON")
    parser.add_argument("--scholar-verification-receipt", help="Direct authenticated Scholar verification receipt JSON")
    parser.add_argument(
        "--exact-source-revision",
        action="store_true",
        help=(
            "Bind this report to the exact current HEAD for post-deploy attestation. "
            "The default uses the last payload revision so a committed review control tail remains checkable."
        ),
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.check and args.report:
        report_path = _repo_path(args.report)
    elif args.check:
        report_path = _latest("public_source_review_*.json")
        if report_path is None:
            raise SystemExit("missing public-source review report")
    else:
        report_date = args.date or _utc_date()
        report_path = _repo_path(args.report) if args.report else REPO_ROOT / "reports" / f"public_source_review_{report_date}.json"
    markdown_path = _repo_path(args.markdown_report) if args.markdown_report else _default_markdown_path(report_path)

    report_date = args.date
    if args.check and report_date is None:
        try:
            import json

            report_date = json.loads(report_path.read_text(encoding="utf-8")).get("date")
        except (OSError, ValueError):
            report_date = None
    report_date = report_date or _utc_date()
    pairing_refresh_status = args.pairing_refresh_status
    pairing_refresh_note = args.pairing_refresh_note
    if args.check and pairing_refresh_status is None:
        try:
            import json

            existing = json.loads(report_path.read_text(encoding="utf-8"))
            context = existing.get("refresh_context", {}) if isinstance(existing, dict) else {}
            if isinstance(context, dict):
                pairing_refresh_status = context.get("pairing_refresh_status")
                pairing_refresh_note = str(context.get("pairing_refresh_note") or "")
        except (OSError, ValueError, json.JSONDecodeError):
            pass
    pairing_refresh_status = pairing_refresh_status or "auto"
    review_source_commit = source_commit(REPO_ROOT) if args.exact_source_revision else source_payload_commit(REPO_ROOT)
    source_provenance = (
        source_worktree_state(REPO_ROOT)
        if args.exact_source_revision
        else control_tail_worktree_state(REPO_ROOT, review_source_commit)
    )
    # The default review record deliberately describes the last payload tree,
    # not the later control-only commit that contains the record itself.  The
    # explicit post-deploy mode remains exact-HEAD so release attestation can
    # require the deployed SHA and its exact tree.
    source_provenance["source_tree_sha"] = source_tree_sha(REPO_ROOT, review_source_commit)
    try:
        inputs = _resolve_inputs(args, report_path=report_path)
        report = build_review_report(
            repo_root=REPO_ROOT,
            report_date=report_date,
            source_commit=review_source_commit,
            source_provenance=source_provenance,
            pairing_refresh_status=pairing_refresh_status,
            pairing_refresh_note=pairing_refresh_note,
            **inputs,
        )
    except (OSError, ValueError) as exc:
        raise SystemExit(f"public-source review failed: {exc}") from exc
    errors = validate_review_report(report)
    if errors:
        raise SystemExit("public-source review failed validation: " + "; ".join(errors))
    rendered_json = render_json(report)
    rendered_markdown = render_markdown(report)
    if args.check:
        stale: list[str] = []
        if not report_path.exists() or report_path.read_text(encoding="utf-8") != rendered_json:
            stale.append(str(report_path))
        if not markdown_path.exists() or markdown_path.read_text(encoding="utf-8") != rendered_markdown:
            stale.append(str(markdown_path))
        if stale:
            raise SystemExit("stale public-source review artifacts: " + ", ".join(stale))
        print(f"checked {_display_path(report_path)} and {_display_path(markdown_path)}")
        return 0
    _atomic_write(report_path, rendered_json)
    _atomic_write(markdown_path, rendered_markdown)
    print(
        f"wrote {_display_path(report_path)} and {_display_path(markdown_path)}: "
        f"{report['summary']['applied']} applied, {report['summary']['deferred']} deferred, {report['summary']['rejected']} rejected"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
