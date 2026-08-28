"""Tests for the shared report_paths helpers (code/src/report_paths.py)."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import report_paths  # noqa: E402
from release_controls import source_payload_commit, source_tree_sha  # noqa: E402
from report_paths import (  # noqa: E402
    dated_report_dir,
    dated_report_path,
    default_latest_file,
    generated_timestamp,
    latest_source_report,
    latest_source_subdir_file,
    latest_report,
    latest_subdir_file,
    rel,
    report_date_string,
    repo_path,
    stable_generated_at,
    control_tail_worktree_state,
    source_worktree_state,
)


@pytest.fixture
def fake_reports(tmp_path: Path) -> Path:
    report_dir = tmp_path / "reports"
    report_dir.mkdir()
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

    latest = latest_report("snapshot_*.json", report_dir=fake_reports)

    assert latest.name == "snapshot_2026-06-18.json"


def test_latest_report_raises_when_required_and_missing(fake_reports: Path):
    with pytest.raises(FileNotFoundError):
        latest_report("nothing_*.json", report_dir=fake_reports)


def test_latest_report_returns_none_when_not_required(fake_reports: Path):
    assert latest_report("nothing_*.json", required=False, report_dir=fake_reports) is None


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


def _init_repo(repo: Path) -> None:
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "Report fixture")


def test_latest_source_report_ignores_untracked_postdeploy_receipt(tmp_path: Path):
    _init_repo(tmp_path)
    reports = tmp_path / "reports"
    reports.mkdir()
    committed = reports / "snapshot_2026-08-25.json"
    committed.write_text("{}", encoding="utf-8")
    _git(tmp_path, "add", "reports")
    _git(tmp_path, "commit", "-qm", "source receipt")
    (reports / "snapshot_2026-08-26.json").write_text("{}", encoding="utf-8")

    assert latest_source_report(
        "snapshot_*.json", report_dir=reports, repo_root=tmp_path
    ) == committed


def test_latest_source_subdir_file_ignores_untracked_postdeploy_receipt(tmp_path: Path):
    _init_repo(tmp_path)
    reports = tmp_path / "reports"
    committed = reports / "browser" / "2026-08-25" / "manifest.json"
    committed.parent.mkdir(parents=True)
    committed.write_text("{}", encoding="utf-8")
    _git(tmp_path, "add", "reports")
    _git(tmp_path, "commit", "-qm", "source receipt")
    fresh = reports / "browser" / "2026-08-26" / "manifest.json"
    fresh.parent.mkdir(parents=True)
    fresh.write_text("{}", encoding="utf-8")

    assert latest_source_subdir_file(
        "browser", "manifest.json", report_dir=reports, repo_root=tmp_path
    ) == committed


def test_dated_report_path_normalizes_suffix(fake_reports: Path):
    path = dated_report_path("asset_size", "json", report_dir=fake_reports)
    assert path.parent == fake_reports
    assert path.name == f"asset_size_{report_date_string()}.json"

    path_with_dot = dated_report_path("asset_size", ".json", report_dir=fake_reports)
    assert path_with_dot == path


def test_dated_report_dir_nests_under_prefix(fake_reports: Path):
    d = dated_report_dir("visual-qa", report_dir=fake_reports)
    assert d == fake_reports / "visual-qa" / report_date_string()


def test_latest_subdir_file_picks_newest_dated_directory(fake_reports: Path):
    older = fake_reports / "visual-qa" / "2026-05-13"
    newer = fake_reports / "visual-qa" / "2026-05-28"
    older.mkdir(parents=True)
    newer.mkdir(parents=True)
    (older / "manifest.json").write_text("{}", encoding="utf-8")
    (newer / "manifest.json").write_text("{}", encoding="utf-8")

    found = latest_subdir_file("visual-qa", "manifest.json", report_dir=fake_reports)

    assert found == newer / "manifest.json"


def test_latest_subdir_file_skips_directories_missing_the_file(fake_reports: Path):
    newer_without_file = fake_reports / "visual-qa" / "2026-06-30"
    older_with_file = fake_reports / "visual-qa" / "2026-05-28"
    newer_without_file.mkdir(parents=True)
    older_with_file.mkdir(parents=True)
    (older_with_file / "manifest.json").write_text("{}", encoding="utf-8")

    found = latest_subdir_file("visual-qa", "manifest.json", report_dir=fake_reports)

    assert found == older_with_file / "manifest.json"


def test_latest_subdir_file_raises_when_required_and_missing(fake_reports: Path):
    with pytest.raises(FileNotFoundError):
        latest_subdir_file("nonexistent-prefix", "manifest.json", report_dir=fake_reports)


def test_repo_path_resolves_relative_against_repo_root():
    assert repo_path("data/works.json") == report_paths.REPO_ROOT / "data" / "works.json"


def test_repo_path_passes_through_absolute_paths(tmp_path: Path):
    absolute = tmp_path / "x.json"
    assert repo_path(absolute) == absolute


def test_rel_returns_posix_repo_relative_path():
    target = report_paths.REPO_ROOT / "data" / "works.json"
    assert rel(target) == "data/works.json"


def test_stable_generated_at_reuses_timestamp_only_for_equal_json_body(tmp_path: Path):
    path = tmp_path / "snapshot.json"
    path.write_text('{"generated_at":"2026-07-17T00:00:00Z","count":3}\n', encoding="utf-8")

    assert stable_generated_at(path, {"generated_at": "2026-07-18T00:00:00Z", "count": 3}) == "2026-07-17T00:00:00Z"
    assert stable_generated_at(path, {"generated_at": "2026-07-18T00:00:00Z", "count": 4}) is None


def test_default_latest_file_returns_first_existing(tmp_path: Path):
    missing = tmp_path / "missing.json"
    present = tmp_path / "present.json"
    present.write_text("{}", encoding="utf-8")

    assert default_latest_file(missing, present) == present
    assert default_latest_file(missing) is None


def test_source_worktree_state_only_exempts_declared_release_evidence(tmp_path: Path):
    """An arbitrary report cannot make an evidence capture claim a clean source tree."""
    for args in (
        ["git", "init", "-q"],
        ["git", "config", "user.email", "test@example.invalid"],
        ["git", "config", "user.name", "Test"],
    ):
        subprocess.run(args, cwd=tmp_path, check=True)
    (tmp_path / "source.txt").write_text("tracked\n", encoding="utf-8")
    subprocess.run(["git", "add", "source.txt"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=tmp_path, check=True)
    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "public_source_snapshot_2026-08-25.json").write_text("{}", encoding="utf-8")

    assert source_worktree_state(tmp_path)["source_worktree_clean"] is True

    (reports / "hand-authored-note.md").write_text("source change\n", encoding="utf-8")
    state = source_worktree_state(tmp_path)
    assert state["source_worktree_clean"] is False
    assert state["source_worktree_dirty_paths"] == ["reports/hand-authored-note.md"]


def test_payload_commit_and_tree_skip_only_a_committed_control_tail(tmp_path: Path):
    """A dated review may be committed without becoming its own source revision."""
    for args in (
        ["git", "init", "-q"],
        ["git", "config", "user.email", "test@example.invalid"],
        ["git", "config", "user.name", "Test"],
    ):
        subprocess.run(args, cwd=tmp_path, check=True)
    (tmp_path / "source.txt").write_text("payload\n", encoding="utf-8")
    subprocess.run(["git", "add", "source.txt"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "payload"], cwd=tmp_path, check=True)
    payload = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, check=True, capture_output=True, text=True
    ).stdout.strip()
    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "public_source_review_2026-08-25.json").write_text("{}\n", encoding="utf-8")
    (reports / "public_source_review_2026-08-25.md").write_text("# review\n", encoding="utf-8")
    subprocess.run(["git", "add", "reports"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "review controls"], cwd=tmp_path, check=True)

    expected_tree = subprocess.run(
        ["git", "rev-parse", f"{payload}^{{tree}}"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert source_payload_commit(tmp_path) == payload
    assert source_tree_sha(tmp_path, payload) == expected_tree

    (reports / "hand-authored-note.md").write_text("payload\n", encoding="utf-8")
    subprocess.run(["git", "add", "reports/hand-authored-note.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "content report"], cwd=tmp_path, check=True)
    assert source_payload_commit(tmp_path) != payload


def test_control_tail_provenance_ignores_only_declared_generated_controls(tmp_path: Path):
    for args in (
        ["git", "init", "-q"],
        ["git", "config", "user.email", "test@example.invalid"],
        ["git", "config", "user.name", "Test"],
    ):
        subprocess.run(args, cwd=tmp_path, check=True)
    (tmp_path / "source.txt").write_text("payload\n", encoding="utf-8")
    subprocess.run(["git", "add", "source.txt"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "payload"], cwd=tmp_path, check=True)
    payload = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, check=True, capture_output=True, text=True
    ).stdout.strip()
    expected_tree = source_tree_sha(tmp_path, payload)

    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "pages-artifact-manifest.json").write_text("{}\n", encoding="utf-8")
    reports = tmp_path / "reports"
    reports.mkdir()
    (reports / "asset_size_2026-08-25.json").write_text("{}\n", encoding="utf-8")
    state = control_tail_worktree_state(tmp_path, payload)
    assert state == {
        "source_worktree_clean": True,
        "source_worktree_dirty_paths": [],
        "source_tree_sha": expected_tree,
    }

    (tmp_path / "README.md").write_text("source change\n", encoding="utf-8")
    state = control_tail_worktree_state(tmp_path, payload)
    assert state["source_worktree_clean"] is False
    assert state["source_worktree_dirty_paths"] == ["README.md"]
