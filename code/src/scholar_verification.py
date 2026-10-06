"""Validate the durable provenance receipt for the curated Scholar snapshot.

``data/scholar-snapshot.json`` is a deliberately curated source, not a live
API cache.  A release therefore needs a small, reviewable receipt that binds a
direct authenticated observation to the *exact bytes* of that source.  The
receipt remains valid across unrelated releases; changing the snapshot makes
its SHA-256 binding fail until a new direct observation is recorded.

This module does not fetch Scholar and does not infer authentication from a
public page.  It validates only the explicit, source-controlled assertion.

The I/O-free helpers at the end of the module build the snapshot and receipt
byte strings for a newly attested observation, so the writer
(``code/orchestrators/record_scholar_observation.py``) and the validator share
one definition of the canonical bytes and cannot drift apart.
"""

from __future__ import annotations

import copy
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import re
from typing import Any


SCHOLAR_METRIC_FIELDS = ("citations", "h_index", "i10_index")
SCHOLAR_SINCE_2021_KEY = "since_2021"
SCHOLAR_SNAPSHOT_RELATIVE_PATH = Path("data/scholar-snapshot.json")
SCHOLAR_RECEIPT_RELATIVE_PATH = Path("data/scholar-verification-receipt.json")
RECEIPT_SCHEMA_VERSION = "1.0"


def sha256_bytes(content: bytes) -> str:
    """Return the stable SHA-256 value used to bind a source receipt."""
    return hashlib.sha256(content).hexdigest()


def _load_object(path: Path, *, label: str) -> tuple[dict[str, Any] | None, str | None]:
    if path.is_symlink():
        return None, f"{label} must not be a symlink: {path.as_posix()}"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, f"missing {label}: {path.as_posix()}"
    except UnicodeDecodeError as exc:
        return None, f"invalid {label} {path.as_posix()}: not valid UTF-8 ({exc})"
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"invalid {label} {path.as_posix()}: {exc}"
    if not isinstance(value, dict):
        return None, f"{label} must be a JSON object: {path.as_posix()}"
    return value, None


def _metrics(payload: dict[str, Any], *, label: str) -> tuple[dict[str, int] | None, list[str]]:
    values: dict[str, int] = {}
    errors: list[str] = []
    for field in SCHOLAR_METRIC_FIELDS:
        value = payload.get(field)
        if type(value) is not int or value < 0:
            errors.append(f"{label} field {field!r} must be a non-negative integer")
        else:
            values[field] = value
    return (values if not errors else None), errors


def _receipt_metrics(payload: dict[str, Any]) -> tuple[dict[str, int] | None, list[str]]:
    metrics = payload.get("metrics")
    if not isinstance(metrics, dict):
        return None, ["Scholar verification receipt is missing a metrics object"]
    return _metrics(metrics, label="Scholar verification receipt metrics")


def _optional_since_2021_metrics(
    payload: dict[str, Any], *, label: str
) -> tuple[dict[str, int] | None, list[str]]:
    """Validate the optional authenticated since-2021 metric column.

    Scholar presents all-time and since-2021 columns together.  The latter is
    optional for historical receipts, but once curated it must be bound exactly
    to the direct-authenticated receipt just like the all-time metrics.
    """
    value = payload.get(SCHOLAR_SINCE_2021_KEY)
    if value is None:
        return None, []
    if not isinstance(value, dict):
        return None, [f"{label} field {SCHOLAR_SINCE_2021_KEY!r} must be an object"]
    return _metrics(value, label=f"{label} {SCHOLAR_SINCE_2021_KEY}")


def _valid_timestamp(value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def validate_bound_scholar_receipt(
    snapshot: dict[str, Any],
    receipt: dict[str, Any] | None,
    *,
    snapshot_sha256: str,
) -> list[str]:
    """Return errors for a receipt that is not bound to this Scholar snapshot.

    The raw snapshot hash intentionally covers its values, as-of date, method,
    and history.  Thus any edit to the metric source, not merely an increase in
    a count, requires an explicitly renewed direct-authenticated receipt.
    """
    errors: list[str] = []
    profile_id = snapshot.get("profile_id")
    if not isinstance(profile_id, str) or not profile_id.strip():
        errors.append("Scholar snapshot is missing canonical profile_id")
    as_of = snapshot.get("as_of")
    if not isinstance(as_of, str) or not as_of.strip():
        errors.append("Scholar snapshot is missing as_of")
    else:
        try:
            date.fromisoformat(as_of)
        except ValueError:
            errors.append("Scholar snapshot as_of must be an ISO-8601 calendar date")
    snapshot_metrics, snapshot_errors = _metrics(snapshot, label="Scholar snapshot")
    errors.extend(snapshot_errors)
    snapshot_since_2021, snapshot_since_2021_errors = _optional_since_2021_metrics(
        snapshot, label="Scholar snapshot"
    )
    errors.extend(snapshot_since_2021_errors)
    if receipt is None:
        return [*errors, "missing direct authenticated Scholar verification receipt"]

    if receipt.get("schema_version") != RECEIPT_SCHEMA_VERSION:
        errors.append("Scholar verification receipt has unsupported schema_version")
    if receipt.get("receipt_type") != "google_scholar_direct_authenticated":
        errors.append("Scholar verification receipt has invalid receipt_type")
    if receipt.get("profile_id") != profile_id:
        errors.append("Scholar verification receipt profile_id does not match the canonical snapshot")
    if receipt.get("direct") is not True or receipt.get("authenticated") is not True:
        errors.append("Scholar verification receipt must explicitly state direct=true and authenticated=true")
    if not _valid_timestamp(receipt.get("verified_at")):
        errors.append("Scholar verification receipt must include a timezone-qualified verified_at")
    if receipt.get("snapshot_path") != SCHOLAR_SNAPSHOT_RELATIVE_PATH.as_posix():
        errors.append("Scholar verification receipt snapshot_path does not name the canonical snapshot")
    if receipt.get("snapshot_sha256") != snapshot_sha256:
        errors.append("Scholar verification receipt snapshot_sha256 does not match data/scholar-snapshot.json")
    if receipt.get("snapshot_as_of") != as_of:
        errors.append("Scholar verification receipt snapshot_as_of does not match the canonical snapshot")
    for field in ("source", "method"):
        if not isinstance(receipt.get(field), str) or not receipt[field].strip():
            errors.append(f"Scholar verification receipt is missing {field}")
    receipt_metrics, receipt_errors = _receipt_metrics(receipt)
    errors.extend(receipt_errors)
    if snapshot_metrics is not None and receipt_metrics is not None and receipt_metrics != snapshot_metrics:
        errors.append("Scholar verification receipt metrics do not match the canonical snapshot")
    receipt_metrics_payload = receipt.get("metrics")
    receipt_since_2021, receipt_since_2021_errors = _optional_since_2021_metrics(
        receipt_metrics_payload if isinstance(receipt_metrics_payload, dict) else {},
        label="Scholar verification receipt metrics",
    )
    errors.extend(receipt_since_2021_errors)
    if (snapshot_since_2021 is None) != (receipt_since_2021 is None):
        errors.append(
            "Scholar verification receipt since_2021 metrics do not match the canonical snapshot"
        )
    elif (
        snapshot_since_2021 is not None
        and receipt_since_2021 is not None
        and snapshot_since_2021 != receipt_since_2021
    ):
        errors.append(
            "Scholar verification receipt since_2021 metrics do not match the canonical snapshot"
        )
    return errors


def validate_scholar_snapshot_receipt(repo_root: Path) -> list[str]:
    """Validate the canonical source receipt without making a network request."""
    snapshot_path = repo_root / SCHOLAR_SNAPSHOT_RELATIVE_PATH
    receipt_path = repo_root / SCHOLAR_RECEIPT_RELATIVE_PATH
    snapshot, snapshot_error = _load_object(snapshot_path, label="Scholar snapshot")
    if snapshot_error:
        return [snapshot_error]
    assert snapshot is not None
    try:
        snapshot_sha256 = sha256_bytes(snapshot_path.read_bytes())
    except OSError as exc:
        return [f"unable to hash Scholar snapshot {snapshot_path.as_posix()}: {exc}"]
    receipt, receipt_error = _load_object(receipt_path, label="Scholar verification receipt")
    if receipt_error:
        return validate_bound_scholar_receipt(snapshot, None, snapshot_sha256=snapshot_sha256) + [receipt_error]
    return validate_bound_scholar_receipt(snapshot, receipt, snapshot_sha256=snapshot_sha256)


# ---------------------------------------------------------------------------
# Observation recording helpers (pure: no filesystem, network, or clock access)
# ---------------------------------------------------------------------------

_ISO_CALENDAR_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
# The suffix the recorder writes on the live history entry, and the form the
# curated history already uses for it (matched case-insensitively because an
# earlier revision wrote ``CURRENT``).
_CURRENT_NOTE_SUFFIX = re.compile(
    r"\s*[\u2014\u2013-]+\s*current source of truth\.?\s*$", re.IGNORECASE
)
DEFAULT_HISTORY_NOTE = "Direct authenticated observation"
VERIFIED_AT_FUTURE_SKEW = timedelta(minutes=5)


def canonical_json_bytes(payload: Any) -> bytes:
    """Return the exact UTF-8 bytes the Scholar snapshot and receipt use on disk.

    Key insertion order is preserved (no ``sort_keys``), non-ASCII text such as
    the em dash in history notes stays literal, and the file ends in a newline.
    Because the receipt binds the SHA-256 of these bytes, writer and validator
    must agree on this one serialization.
    """
    return (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def parse_observation_date(value: object) -> date:
    """Parse a strict ``YYYY-MM-DD`` calendar date (no week or compact forms)."""
    text = value.strip() if isinstance(value, str) else ""
    if not _ISO_CALENDAR_DATE.fullmatch(text):
        raise ValueError(f"as_of must be a YYYY-MM-DD calendar date, got {value!r}")
    try:
        return date.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"as_of is not a real calendar date: {value!r}") from exc


def parse_verified_at(value: str) -> datetime:
    """Parse a timezone-qualified ISO timestamp into whole-second UTC.

    A trailing ``Z`` is accepted.  Naive timestamps (including bare dates) are
    refused: a receipt must say which instant it vouches for.
    """
    text = value.strip() if isinstance(value, str) else ""
    if text[-1:] in ("Z", "z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise ValueError(f"verified_at is not an ISO-8601 timestamp: {value!r}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(
            f"verified_at must be timezone-qualified (for example 2026-01-02T03:04:05Z), got {value!r}"
        )
    try:
        return parsed.astimezone(timezone.utc).replace(microsecond=0)
    except OverflowError as exc:
        raise ValueError(f"verified_at is outside the representable range: {value!r}") from exc


def format_verified_at(moment: datetime) -> str:
    """Render a timezone-aware instant in the receipt's ``YYYY-MM-DDTHH:MM:SSZ`` form."""
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def observation_timing_errors(
    as_of: date,
    verified_at: datetime,
    now: datetime,
    *,
    current_as_of: date | None = None,
    verified_at_defaulted: bool = False,
) -> list[str]:
    """Return refusals for the dates of a new observation; ``now`` is supplied.

    ``as_of`` may be at most one UTC day ahead of ``now`` (an evening Pacific
    observation is already tomorrow in UTC).  ``verified_at`` may not be in the
    future beyond a small clock skew, and its UTC date may not precede ``as_of``
    by more than one day.  When ``current_as_of`` is given the new observation
    must also be strictly newer than the recorded one.

    ``verified_at_defaulted`` is True when the operator did not state the
    verification instant (it was taken from the clock or from an earlier
    receipt).  A receipt must not vouch for a verification the operator never
    attested, so a defaulted instant whose UTC date is later than ``as_of`` plus
    one day is refused; stating ``--verified-at`` explicitly lifts that bound.
    """
    errors: list[str] = []
    moment = now.astimezone(timezone.utc)
    if current_as_of is not None and as_of <= current_as_of:
        errors.append(
            f"as_of {as_of.isoformat()} must be strictly later than the recorded as_of {current_as_of.isoformat()}"
        )
    if as_of > moment.date() + timedelta(days=1):
        errors.append(f"as_of {as_of.isoformat()} is in the future (today is {moment.date().isoformat()} UTC)")
    if verified_at > moment + VERIFIED_AT_FUTURE_SKEW:
        errors.append(f"verified_at {format_verified_at(verified_at)} is in the future")
    verified_date = verified_at.astimezone(timezone.utc).date()
    if verified_date < as_of - timedelta(days=1):
        errors.append(
            f"verified_at {format_verified_at(verified_at)} precedes as_of {as_of.isoformat()} by more than one day"
        )
    if verified_at_defaulted and verified_date > as_of + timedelta(days=1):
        errors.append(
            f"verified_at would default to {format_verified_at(verified_at)}, more than one day after "
            f"as_of {as_of.isoformat()}; a receipt cannot vouch for a verification you did not state, "
            "so pass --verified-at with the instant you actually verified the profile"
        )
    return errors


def reusable_receipt_verified_at(
    receipt_bytes: bytes | None, as_of: date, now: datetime
) -> datetime | None:
    """Return an existing receipt's ``verified_at`` when it can vouch for ``as_of`` again.

    Used by receipt-only recovery so a regenerated receipt keeps the instant
    that was originally stated instead of silently re-stamping recovery time.
    The receipt must be a decodable JSON object whose ``snapshot_as_of`` is
    this observation's date and whose ``verified_at`` is timezone-qualified and
    passes the same bounds a defaulted instant must pass.  Anything else
    (missing, binary, naive, out of bounds, a different observation) returns
    ``None`` and the caller falls back to the clock under the defaulted rule.
    """
    if receipt_bytes is None:
        return None
    try:
        receipt = json.loads(receipt_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(receipt, dict) or receipt.get("snapshot_as_of") != as_of.isoformat():
        return None
    stamp = receipt.get("verified_at")
    if not isinstance(stamp, str):
        return None
    try:
        verified_at = parse_verified_at(stamp)
    except ValueError:
        return None
    if observation_timing_errors(as_of, verified_at, now, verified_at_defaulted=True):
        return None
    return verified_at


def validate_observation(observation: dict[str, Any]) -> list[str]:
    """Return errors for an operator-supplied observation (as_of plus six metrics)."""
    errors: list[str] = []
    try:
        parse_observation_date(observation.get("as_of"))
    except ValueError as exc:
        errors.append(str(exc))
    _, metric_errors = _metrics(observation, label="Scholar observation")
    errors.extend(metric_errors)
    since_2021 = observation.get(SCHOLAR_SINCE_2021_KEY)
    if not isinstance(since_2021, dict):
        errors.append(f"Scholar observation field {SCHOLAR_SINCE_2021_KEY!r} must be an object")
    else:
        _, since_errors = _metrics(since_2021, label=f"Scholar observation {SCHOLAR_SINCE_2021_KEY}")
        errors.extend(since_errors)
    errors.extend(_observation_consistency_errors(observation))
    return errors


def _observation_consistency_errors(observation: dict[str, Any]) -> list[str]:
    """Return errors for six individually valid numbers that cannot all be true.

    The operator types these numbers and nothing downstream can check them
    against Scholar, so the arithmetic that must hold is enforced here: the
    since-2021 window is a subset of all time, so each of its three values is at
    most the all-time value; and an h-index or i10-index is bounded by the
    citations in the same column.  Only integer fields are compared (type
    errors are reported by the field checks).
    """
    columns: list[tuple[str, dict[str, Any]]] = [("all-time", observation)]
    since_2021 = observation.get(SCHOLAR_SINCE_2021_KEY)
    if isinstance(since_2021, dict):
        columns.append((SCHOLAR_SINCE_2021_KEY, since_2021))

    def number(source: dict[str, Any], field: str) -> int | None:
        value = source.get(field)
        return value if type(value) is int else None

    errors: list[str] = []
    for name, column in columns:
        citations = number(column, "citations")
        for field in ("h_index", "i10_index"):
            value = number(column, field)
            if citations is not None and value is not None and value > citations:
                errors.append(
                    f"{name} {field} ({value}) exceeds {name} citations ({citations}), which is impossible"
                )
    if isinstance(since_2021, dict):
        for field in SCHOLAR_METRIC_FIELDS:
            recent, total = number(since_2021, field), number(observation, field)
            if recent is not None and total is not None and recent > total:
                errors.append(
                    f"{SCHOLAR_SINCE_2021_KEY} {field} ({recent}) exceeds the all-time {field} ({total}); "
                    "the since-2021 window is a subset of all time, so check the columns are not transposed"
                )
    return errors


def observation_matches_snapshot(snapshot: dict[str, Any], observation: dict[str, Any]) -> bool:
    """Return True when the snapshot already records exactly this observation."""
    if snapshot.get("as_of") != observation.get("as_of"):
        return False
    if any(snapshot.get(field) != observation.get(field) for field in SCHOLAR_METRIC_FIELDS):
        return False
    return snapshot.get(SCHOLAR_SINCE_2021_KEY) == observation.get(SCHOLAR_SINCE_2021_KEY)


def default_observation_method(observation: dict[str, Any]) -> str:
    """Return the neutral method text used for the snapshot and the receipt.

    Deliberately says nothing about the browser or interface the operator used:
    a SHA-bound provenance record must not assert details nobody attested.
    """
    since_2021 = observation[SCHOLAR_SINCE_2021_KEY]
    return (
        f"Direct authenticated observation of the canonical profile on {observation['as_of']}. "
        f"All-time: {observation['citations']} citations, h-index {observation['h_index']}, "
        f"i10-index {observation['i10_index']}; "
        f"Since-2021: {since_2021['citations']} / {since_2021['h_index']} / {since_2021['i10_index']}. "
        "No anonymous or search-engine cached result was used."
    )


def default_observation_source(snapshot: dict[str, Any]) -> str:
    """Return the receipt ``source`` text naming the canonical profile URL.

    Like the default method, this says nothing about the interface used (which
    browser, an app): the operator attests a direct, authenticated view of the
    profile, and any finer detail belongs in an explicit ``--source`` only when
    the operator can attest it.
    """
    profile_url = snapshot.get("profile_url")
    if not isinstance(profile_url, str) or not profile_url.strip():
        raise ValueError("Scholar snapshot is missing profile_url; supply an explicit source")
    return f"Direct authenticated observation of {profile_url.strip()}"


def current_history_note(history_note: str | None = None) -> str:
    """Return the note for the newly current history entry.

    The note always ends with an em dash and ``current source of truth.``;
    ``history_note`` replaces the default descriptor (any trailing period or
    pre-existing suffix is dropped so the suffix is never doubled).
    """
    base = _CURRENT_NOTE_SUFFIX.sub("", history_note or "").strip().rstrip(".").strip()
    return f"{base or DEFAULT_HISTORY_NOTE} \u2014 current source of truth."


def superseded_note(note: str, new_as_of: str) -> str:
    """Rewrite a history note so it reads as superseded on ``new_as_of``.

    A trailing em dash plus ``current source of truth.`` is replaced by
    `` (superseded <date>)``, the form the curated history already uses.  A
    note without that suffix gets the marker appended after any trailing period
    is dropped; a note already marked superseded is returned unchanged.
    """
    if "(superseded" in note:
        return note
    marker = f" (superseded {new_as_of})"
    if _CURRENT_NOTE_SUFFIX.search(note):
        return _CURRENT_NOTE_SUFFIX.sub(marker, note).strip()
    return f"{note.rstrip().rstrip('.').rstrip()}{marker}"


def supersede_history(history: Any, snapshot: dict[str, Any], new_as_of: str) -> list[dict[str, Any]]:
    """Return a copy of ``history`` whose last entry is marked superseded.

    The last entry must mirror the live snapshot (as_of and the three
    all-time metrics); otherwise the curated pair has drifted and recording a
    new observation on top of it would bury that drift, so this raises
    ``ValueError`` instead.
    """
    if not isinstance(history, list) or not history or not isinstance(history[-1], dict):
        raise ValueError("Scholar snapshot history is missing or empty; cannot supersede the current entry")
    last = history[-1]
    for field in ("as_of", *SCHOLAR_METRIC_FIELDS):
        if last.get(field) != snapshot.get(field):
            raise ValueError(
                f"last history entry disagrees with the snapshot on {field!r} "
                f"({last.get(field)!r} vs {snapshot.get(field)!r}); reconcile the history before recording"
            )
    note = last.get("note")
    if not isinstance(note, str) or not note.strip():
        raise ValueError("last Scholar history entry has no note to supersede")
    updated = copy.deepcopy(history)
    updated[-1]["note"] = superseded_note(note, new_as_of)
    return updated


def _with_value_after(
    payload: dict[str, Any], after_key: str, key: str, value: Any
) -> dict[str, Any]:
    """Set ``key`` in place, or insert it right after ``after_key`` when absent."""
    if key in payload or after_key not in payload:
        payload[key] = value
        return payload
    items = list(payload.items())
    payload.clear()
    for existing_key, existing_value in items:
        payload[existing_key] = existing_value
        if existing_key == after_key:
            payload[key] = value
    return payload


def build_observation_snapshot(
    snapshot: dict[str, Any],
    observation: dict[str, Any],
    *,
    method: str,
    history_note: str | None = None,
) -> dict[str, Any]:
    """Return the snapshot object recording ``observation``; ``snapshot`` is untouched.

    Values are updated in place on a copy so the key order, ``policy``,
    ``profile_*`` and ``secondary_*`` fields stay exactly as curated.  History
    entries keep their five-key shape (no ``since_2021``).
    """
    problems = validate_observation(observation)
    if problems:
        raise ValueError("; ".join(problems))
    new_as_of = observation["as_of"]
    history = supersede_history(snapshot.get("history"), snapshot, new_as_of)
    history.append(
        {
            "as_of": new_as_of,
            "citations": observation["citations"],
            "h_index": observation["h_index"],
            "i10_index": observation["i10_index"],
            "note": current_history_note(history_note),
        }
    )
    updated = copy.deepcopy(snapshot)
    for field in SCHOLAR_METRIC_FIELDS:
        updated[field] = observation[field]
    _with_value_after(
        updated,
        "i10_index",
        SCHOLAR_SINCE_2021_KEY,
        {field: observation[SCHOLAR_SINCE_2021_KEY][field] for field in SCHOLAR_METRIC_FIELDS},
    )
    updated["as_of"] = new_as_of
    updated["method"] = method
    updated["history"] = history
    return updated


def build_observation_receipt(
    snapshot: dict[str, Any],
    *,
    snapshot_sha256: str,
    verified_at: str,
    source: str,
) -> dict[str, Any]:
    """Return the receipt object that binds a direct authenticated observation.

    Metrics, ``snapshot_as_of`` and ``method`` are copied from ``snapshot`` so
    they match it by construction.  The two ``True`` assertions are written
    here deliberately: callers must have obtained an explicit operator
    attestation, because nothing in this module can observe authentication.
    """
    metrics: dict[str, Any] = {field: snapshot[field] for field in SCHOLAR_METRIC_FIELDS}
    since_2021 = snapshot.get(SCHOLAR_SINCE_2021_KEY)
    if isinstance(since_2021, dict):
        metrics[SCHOLAR_SINCE_2021_KEY] = {field: since_2021[field] for field in SCHOLAR_METRIC_FIELDS}
    return {
        "schema_version": RECEIPT_SCHEMA_VERSION,
        "receipt_type": "google_scholar_direct_authenticated",
        "profile_id": snapshot["profile_id"],
        "direct": True,
        "authenticated": True,
        "verified_at": verified_at,
        "snapshot_path": SCHOLAR_SNAPSHOT_RELATIVE_PATH.as_posix(),
        "snapshot_sha256": snapshot_sha256,
        "snapshot_as_of": snapshot["as_of"],
        "metrics": metrics,
        "source": source,
        "method": snapshot["method"],
    }


def build_receipt_bytes(
    snapshot_bytes: bytes, *, verified_at: str, source: str | None = None
) -> bytes:
    """Return validated receipt bytes bound to the exact ``snapshot_bytes``.

    Raises ``ValueError`` when the bytes are not a snapshot object or when the
    resulting receipt would not satisfy :func:`validate_bound_scholar_receipt`.
    """
    try:
        snapshot = json.loads(snapshot_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"snapshot bytes are not valid JSON: {exc}") from exc
    if not isinstance(snapshot, dict):
        raise ValueError("snapshot bytes must hold a JSON object")
    digest = sha256_bytes(snapshot_bytes)
    receipt = build_observation_receipt(
        snapshot,
        snapshot_sha256=digest,
        verified_at=verified_at,
        source=source if source is not None else default_observation_source(snapshot),
    )
    errors = validate_bound_scholar_receipt(snapshot, receipt, snapshot_sha256=digest)
    if errors:
        raise ValueError("; ".join(errors))
    return canonical_json_bytes(receipt)


def build_observation_artifacts(
    snapshot: dict[str, Any],
    observation: dict[str, Any],
    *,
    verified_at: str,
    method: str | None = None,
    source: str | None = None,
    history_note: str | None = None,
) -> tuple[bytes, bytes]:
    """Return ``(snapshot_bytes, receipt_bytes)`` recording ``observation``.

    The receipt is built from the final snapshot bytes, so its SHA-256 binding
    holds by construction; both objects are validated before anything is
    returned.  ``ValueError`` signals a refusal (drifted history, malformed
    observation, or a pair the validator would reject).
    """
    new_snapshot = build_observation_snapshot(
        snapshot,
        observation,
        method=method if method is not None else default_observation_method(observation),
        history_note=history_note,
    )
    snapshot_bytes = canonical_json_bytes(new_snapshot)
    receipt_bytes = build_receipt_bytes(snapshot_bytes, verified_at=verified_at, source=source)
    return snapshot_bytes, receipt_bytes
