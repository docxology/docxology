"""Validate the durable provenance receipt for the curated Scholar snapshot.

``data/scholar-snapshot.json`` is a deliberately curated source, not a live
API cache.  A release therefore needs a small, reviewable receipt that binds a
direct authenticated observation to the *exact bytes* of that source.  The
receipt remains valid across unrelated releases; changing the snapshot makes
its SHA-256 binding fail until a new direct observation is recorded.

This module does not fetch Scholar and does not infer authentication from a
public page.  It validates only the explicit, source-controlled assertion.
"""

from __future__ import annotations

from datetime import date, datetime
import hashlib
import json
from pathlib import Path
from typing import Any


SCHOLAR_METRIC_FIELDS = ("citations", "h_index", "i10_index")
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
