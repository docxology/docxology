"""Tests for live-site verification payload checks."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import verify_live_site as vl  # noqa: E402


def _write_current_counts(path: Path) -> dict:
    payload = {
        "generated_at": "2026-06-16T03:36:11+00:00",
        "counts": {
            "bibliography_works": 168,
            "software": {
                "docxology_owned": 58,
                "active_inference_institute": 33,
            },
            "github_inventory": {
                "public": 360,
            },
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def _write_report(path: Path, payload: dict, *, overall_ok: bool = True, expected_counts: dict | None = None) -> None:
    report_payload = {
        "generated_at": "2026-06-16T03:36:11Z",
        "expected_counts": expected_counts if expected_counts is not None else vl.load_current_counts_fingerprint(),
        "results": [
            {"status": 200},
            {"status": 200},
            {"status": 200},
        ],
        "overall_ok": overall_ok,
        "passing": 3,
        "checked_urls": 3,
    }
    report_payload.update(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report_payload, indent=2), encoding="utf-8")


def test_load_dynamic_checks_uses_current_counts(monkeypatch, tmp_path):
    counts_path = tmp_path / "data" / "current-counts.json"
    payload = _write_current_counts(counts_path)
    monkeypatch.setattr(vl, "CURRENT_COUNTS_JSON", counts_path)

    checks = vl.load_dynamic_checks()

    pubs = next(check for check in checks if check["path"] == "publications.html")
    software = next(check for check in checks if check["path"] == "software.html")

    assert any("168 Works" in marker for marker in pubs["markers"])
    assert any("58 owned" in marker for marker in software["markers"])
    assert any("33 catalogued" in marker for marker in software["markers"])
    assert any(f"{payload['counts']['github_inventory']['public']} public repositories" in marker for marker in software["markers"])


def test_verify_live_site_check_command_validates_fingerprint(monkeypatch, tmp_path, capsys):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    monkeypatch.setattr(vl, "CURRENT_COUNTS_JSON", counts_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    _write_report(report_path, {}, expected_counts=vl.load_current_counts_fingerprint())

    monkeypatch.setattr(vl, "latest_report", lambda pattern, required=False: report_path)
    monkeypatch.setattr(sys, "argv", ["verify_live_site.py", "--check"])

    vl.main()
    output = capsys.readouterr().out
    assert "checked live-site verification report" in output


def test_verify_live_site_check_fails_when_fingerprint_drifted(monkeypatch, tmp_path):
    counts_path = tmp_path / "data" / "current-counts.json"
    _write_current_counts(counts_path)
    monkeypatch.setattr(vl, "CURRENT_COUNTS_JSON", counts_path)
    report_path = tmp_path / "reports" / "live_site_verification_2026-06-16.json"
    drifted = vl.load_current_counts_fingerprint().copy()
    drifted["works"] = 999
    _write_report(report_path, {"expected_counts": drifted}, expected_counts=drifted)

    monkeypatch.setattr(vl, "latest_report", lambda pattern, required=False: report_path)
    monkeypatch.setattr(sys, "argv", ["verify_live_site.py", "--check"])

    with pytest.raises(SystemExit):
        vl.main()
