"""Tests for the shared report_paths helpers (code/src/report_paths.py)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import report_paths  # noqa: E402
from report_paths import (  # noqa: E402
    dated_report_dir,
    dated_report_path,
    default_latest_file,
    generated_timestamp,
    latest_report,
    latest_subdir_file,
    rel,
    report_date_string,
    repo_path,
)


@pytest.fixture
def fake_reports(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
    monkeypatch.setattr(report_paths, "REPORT_DIR", report_dir)
    return report_dir


def test_report_date_string_is_iso_format():
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", report_date_string())


def test_generated_timestamp_is_zulu_iso8601():
    ts = generated_timestamp()
    assert ts.endswith("Z")
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", ts)


def test_latest_report_picks_newest_by_name(fake_reports: Path):
    (fake_reports / "snapshot_2026-05-01.json").write_text("{}", encoding="utf-8")
    (fake_reports / "snapshot_2026-06-18.json").write_text("{}", encoding="utf-8")
    (fake_reports / "snapshot_2026-05-27.json").write_text("{}", encoding="utf-8")

    latest = latest_report("snapshot_*.json")

    assert latest.name == "snapshot_2026-06-18.json"


def test_latest_report_raises_when_required_and_missing(fake_reports: Path):
    with pytest.raises(FileNotFoundError):
        latest_report("nothing_*.json")


def test_latest_report_returns_none_when_not_required(fake_reports: Path):
    assert latest_report("nothing_*.json", required=False) is None


def test_dated_report_path_normalizes_suffix(fake_reports: Path):
    path = dated_report_path("asset_size", "json")
    assert path.parent == fake_reports
    assert path.name == f"asset_size_{report_date_string()}.json"

    path_with_dot = dated_report_path("asset_size", ".json")
    assert path_with_dot == path


def test_dated_report_dir_nests_under_prefix(fake_reports: Path):
    d = dated_report_dir("visual-qa")
    assert d == fake_reports / "visual-qa" / report_date_string()


def test_latest_subdir_file_picks_newest_dated_directory(fake_reports: Path):
    older = fake_reports / "visual-qa" / "2026-05-13"
    newer = fake_reports / "visual-qa" / "2026-05-28"
    older.mkdir(parents=True)
    newer.mkdir(parents=True)
    (older / "manifest.json").write_text("{}", encoding="utf-8")
    (newer / "manifest.json").write_text("{}", encoding="utf-8")

    found = latest_subdir_file("visual-qa", "manifest.json")

    assert found == newer / "manifest.json"


def test_latest_subdir_file_skips_directories_missing_the_file(fake_reports: Path):
    newer_without_file = fake_reports / "visual-qa" / "2026-06-30"
    older_with_file = fake_reports / "visual-qa" / "2026-05-28"
    newer_without_file.mkdir(parents=True)
    older_with_file.mkdir(parents=True)
    (older_with_file / "manifest.json").write_text("{}", encoding="utf-8")

    found = latest_subdir_file("visual-qa", "manifest.json")

    assert found == older_with_file / "manifest.json"


def test_latest_subdir_file_raises_when_required_and_missing(fake_reports: Path):
    with pytest.raises(FileNotFoundError):
        latest_subdir_file("nonexistent-prefix", "manifest.json")


def test_repo_path_resolves_relative_against_repo_root():
    assert repo_path("data/works.json") == report_paths.REPO_ROOT / "data" / "works.json"


def test_repo_path_passes_through_absolute_paths(tmp_path: Path):
    absolute = tmp_path / "x.json"
    assert repo_path(absolute) == absolute


def test_rel_returns_posix_repo_relative_path():
    target = report_paths.REPO_ROOT / "data" / "works.json"
    assert rel(target) == "data/works.json"


def test_default_latest_file_returns_first_existing(tmp_path: Path):
    missing = tmp_path / "missing.json"
    present = tmp_path / "present.json"
    present.write_text("{}", encoding="utf-8")

    assert default_latest_file(missing, present) == present
    assert default_latest_file(missing) is None
