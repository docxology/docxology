"""Real-file regression coverage for the Scholar source-receipt boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
SYNC_SOURCE = REPO_ROOT / "code" / "orchestrators" / "sync_scholar_metrics.py"
VALIDATOR_SOURCE = REPO_ROOT / "code" / "src" / "scholar_verification.py"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sync_fixture(root: Path) -> tuple[Path, Path]:
    """Create a minimal runnable checkout without patching imported modules."""
    script = root / "code" / "orchestrators" / "sync_scholar_metrics.py"
    validator = root / "code" / "src" / "scholar_verification.py"
    script.parent.mkdir(parents=True, exist_ok=True)
    validator.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SYNC_SOURCE, script)
    shutil.copy2(VALIDATOR_SOURCE, validator)

    snapshot = root / "data" / "scholar-snapshot.json"
    _write_json(
        snapshot,
        {
            "profile_id": "canonical",
            "citations": 10,
            "h_index": 2,
            "i10_index": 3,
            "as_of": "2026-08-25",
        },
    )
    receipt = root / "data" / "scholar-verification-receipt.json"
    _write_json(
        receipt,
        {
            "schema_version": "1.0",
            "receipt_type": "google_scholar_direct_authenticated",
            "profile_id": "canonical",
            "direct": True,
            "authenticated": True,
            "verified_at": "2026-08-25T10:00:00Z",
            "snapshot_path": "data/scholar-snapshot.json",
            "snapshot_sha256": _sha256(snapshot),
            "snapshot_as_of": "2026-08-25",
            "metrics": {"citations": 10, "h_index": 2, "i10_index": 3},
            "source": "local CLI fixture",
            "method": "fixture direct authenticated verification",
        },
    )
    return script, snapshot


def test_sync_scholar_metrics_check_requires_a_current_bound_receipt(tmp_path: Path):
    script, snapshot = _sync_fixture(tmp_path)
    receipt = tmp_path / "data" / "scholar-verification-receipt.json"
    before = {path: path.read_bytes() for path in (snapshot, receipt)}

    valid = subprocess.run(
        [sys.executable, str(script), "--check"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
    )

    assert valid.returncode == 0, valid.stderr
    assert before == {path: path.read_bytes() for path in (snapshot, receipt)}

    changed = json.loads(snapshot.read_text(encoding="utf-8"))
    changed["citations"] = 11
    _write_json(snapshot, changed)
    tampered_before = snapshot.read_bytes()
    invalid = subprocess.run(
        [sys.executable, str(script), "--check"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
    )

    assert invalid.returncode == 1
    assert "snapshot_sha256 does not match" in invalid.stdout
    assert snapshot.read_bytes() == tampered_before


def test_sync_scholar_metrics_check_rejects_a_malformed_snapshot_date(tmp_path: Path):
    script, snapshot = _sync_fixture(tmp_path)
    receipt = tmp_path / "data" / "scholar-verification-receipt.json"
    changed = json.loads(snapshot.read_text(encoding="utf-8"))
    changed["as_of"] = "not-a-date"
    _write_json(snapshot, changed)
    receipt_payload = json.loads(receipt.read_text(encoding="utf-8"))
    receipt_payload["snapshot_as_of"] = "not-a-date"
    receipt_payload["snapshot_sha256"] = _sha256(snapshot)
    _write_json(receipt, receipt_payload)

    result = subprocess.run(
        [sys.executable, str(script), "--check"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "as_of must be an ISO-8601 calendar date" in result.stdout
