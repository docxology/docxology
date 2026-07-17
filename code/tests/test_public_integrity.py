"""Regression tests for public CV/source privacy and URL safety."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from public_integrity import LOCAL_PATH_RE, scan_public_files  # noqa: E402


def test_current_public_cv_surfaces_have_no_privacy_violations():
    assert scan_public_files(REPO_ROOT) == []


def test_local_path_detector_catches_user_home_paths():
    assert LOCAL_PATH_RE.search("source: /Users/example/Downloads/CV.pdf")
    assert LOCAL_PATH_RE.search("source: /home/example/private.json")


def test_public_integrity_checks_can_scan_a_narrow_fixture(tmp_path):
    fixture = tmp_path / "fixture.json"
    fixture.write_text('{"url":"javascript:alert(1)"}', encoding="utf-8")
    errors = scan_public_files(tmp_path, ("fixture.json",))
    assert "unsafe URL scheme" in errors[0]


def test_csp_data_source_is_not_treated_as_an_unsafe_link_scheme(tmp_path):
    fixture = tmp_path / "fixture.html"
    fixture.write_text('<meta content="img-src self data: https:">', encoding="utf-8")
    assert scan_public_files(tmp_path, ("fixture.html",)) == []
