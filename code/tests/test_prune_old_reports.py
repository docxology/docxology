"""Tests for dated-report prune helpers."""

from __future__ import annotations

import sys
import argparse
import hashlib
import json
import os
import subprocess

import pytest
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)


import prune_old_reports as pruner  # noqa: E402
from prune_old_reports import _retention_errors, _archive_errors, _retention_entries, _legacy_root_set  # noqa: E402
from docxology_tools.report_references import referenced_report_paths  # noqa: E402


PREFIX = "reports/visual-qa/2026-01-01"


def test_working_tree_references_untracked_html(tmp_path: Path):
    (tmp_path / "index.html").write_text(f'<img src="{PREFIX}/shot.png">', encoding="utf-8")
    assert PREFIX + "/shot.png" in referenced_report_paths(tmp_path)


def test_working_tree_references_ignores_excluded_trees(tmp_path: Path):
    (tmp_path / "reports" / "visual-qa" / "2026-01-01").mkdir(parents=True)
    (tmp_path / "reports" / "visual-qa" / "2026-01-01" / "manifest.json").write_text(
        PREFIX, encoding="utf-8"
    )
    (tmp_path / "code").mkdir()
    (tmp_path / "code" / "note.md").write_text(PREFIX, encoding="utf-8")
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "pages-artifact-manifest.json").write_text(PREFIX, encoding="utf-8")
    (tmp_path / "data" / "generated-manifest.json").write_text(PREFIX, encoding="utf-8")
    assert not referenced_report_paths(tmp_path)

    (tmp_path / "llms.md").write_text(f"see {PREFIX}/shot.png", encoding="utf-8")
    assert PREFIX + "/shot.png" in referenced_report_paths(tmp_path)


def test_retention_errors_require_durable_review_fields():
    candidate = "reports/visual-qa/2026-07-18"
    assert _retention_errors([candidate], {}) == [f"no retention record for {candidate}"]
    errors = _retention_errors(
        [candidate],
        {
            candidate: {
                "generated_at": "2026-07-18T01:55:49Z",
                "provenance_sha256": "abc",
                "replacement_location": "git:deadbeef",
                "decision": "remove-from-checkout",
                "reviewed_by": "MAINTAINER",
            }
        },
    )
    assert errors == []


@pytest.fixture
def archive(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    rel = "reports/visual-qa/2026-01-01"
    folder = tmp_path / rel
    folder.mkdir(parents=True)
    manifest = folder / "manifest.json"
    manifest.write_text('{"generated_at":"2026-01-01T00:00:00Z"}')
    (folder / "shot.png").write_bytes(b"capture")
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=tmp_path, text=True).strip()
    git("add", ".")
    git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.org",
        "-c", "commit.gpgsign=false", "commit", "-qm", "archive")
    sha = git("rev-parse", "HEAD")
    entry = {"generated_at": "2026-01-01T00:00:00Z",
             "provenance_sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
             "replacement_location": "git:" + sha}
    return tmp_path, rel, folder, entry, sha


def test_archive_proves_exact_committed_bytes(archive):
    root, rel, folder, entry, sha = archive
    assert _archive_errors(root, rel, entry) == []
    entry["replacement_location"] = f"https://github.com/docxology/docxology/tree/{sha}/{rel}"
    assert _archive_errors(root, rel, entry) == []
    (folder / "shot.png").write_bytes(b"edited capture")
    assert "bytes differ" in _archive_errors(root, rel, entry)[0]


@pytest.mark.parametrize("change", ["addition", "deletion", "symlink", "manifest"])
def test_archive_preserves_unarchived_work(archive, change):
    root, rel, folder, entry, _sha = archive
    if change == "addition":
        (folder / "local.txt").write_text("do not discard")
    elif change == "deletion":
        (folder / "shot.png").unlink()
    elif change == "symlink":
        (folder / "shot.png").unlink()
        (folder / "shot.png").symlink_to(folder / "manifest.json")
    else:
        (folder / "manifest.json").write_text('{}')
    assert _archive_errors(root, rel, entry)


@pytest.mark.parametrize("location", ["git:deadbeef", "git:" + "0" * 40,
    "https://example.org/archive", "https://github.com/other/repo/tree/" + "a" * 40])
def test_archive_rejects_unverifiable_location(archive, location):
    root, rel, _folder, entry, _sha = archive
    entry["replacement_location"] = location
    assert _archive_errors(root, rel, entry)


def test_archive_generation_time_and_exact_path(archive):
    root, rel, _folder, entry, sha = archive
    entry["generated_at"] = "2025-01-01T00:00:00Z"
    assert "generation time" in _archive_errors(root, rel, entry)[0]
    entry["generated_at"] = "2026-01-01T00:00:00Z"
    entry["replacement_location"] = f"https://github.com/docxology/docxology/tree/{sha}/reports/other"
    assert _archive_errors(root, rel, entry)


def test_duplicate_retention_records_fail(tmp_path):
    path = tmp_path / "retention.json"
    path.write_text(json.dumps({"schema_version": "1.0", "entries": [{"path": PREFIX}] * 2}))
    with pytest.raises(SystemExit, match="Duplicate"):
        _retention_entries(path)


def test_root_copies_require_older_date_and_capture_only_content(tmp_path, monkeypatch):
    monkeypatch.setattr(pruner, "REPORTS_DIR", tmp_path)
    (tmp_path / "visual-qa/2026-01-02").mkdir(parents=True)
    copy = tmp_path / "2026-01-01"
    copy.mkdir()
    (copy / "manifest.json").write_text('{}')
    (copy / "shot.png").write_bytes(b"capture")
    assert _legacy_root_set("2026-01-01") == copy
    for value in ["../papers", "2026-01-02", "2026-02-30", "20260101"]:
        with pytest.raises(argparse.ArgumentTypeError):
            _legacy_root_set(value)
    (copy / "paper.pdf").write_bytes(b"source")
    with pytest.raises(argparse.ArgumentTypeError, match="only"):
        _legacy_root_set("2026-01-01")


def test_prune_scans_references_once_and_matches_directory_boundaries(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(pruner, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(pruner, "REPORTS_DIR", tmp_path / "reports")
    for family in pruner.SCREENSHOT_PARENTS:
        for date in ["2026-01-01", "2026-01-02", "2026-01-03"]:
            (tmp_path / "reports" / family / date).mkdir(parents=True)
    calls = []
    def references(root, **_kwargs):
        calls.append(root)
        return {"reports/visual-qa/2026-01-01-extra/shot.png",
                "reports/browser-smoke/2026-01-01/shot.png"}
    monkeypatch.setattr(pruner.report_references, "referenced_report_paths", references)
    monkeypatch.setattr(sys, "argv", ["prune_old_reports.py"])
    assert pruner.main() == 0
    assert calls == [tmp_path]
    output = capsys.readouterr().out
    assert "would remove reports/visual-qa/2026-01-01" in output
    assert "keep (still referenced): reports/browser-smoke/2026-01-01" in output
    assert "across 3 superseded" in output


def test_apply_checks_all_archives_before_deleting_any(tmp_path, monkeypatch):
    monkeypatch.setattr(pruner, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(pruner, "REPORTS_DIR", tmp_path / "reports")
    for date in ["2026-01-01", "2026-01-02", "2026-01-03"]:
        (tmp_path / "reports/visual-qa" / date).mkdir(parents=True)
    candidates = ["reports/visual-qa/2026-01-01", "reports/visual-qa/2026-01-02"]
    monkeypatch.setattr(pruner.report_references, "referenced_report_paths", lambda _, **_kwargs: set())
    monkeypatch.setattr(pruner, "_retention_entries", lambda _: {p: {} for p in candidates})
    monkeypatch.setattr(pruner, "_retention_errors", lambda *_: [])
    monkeypatch.setattr(pruner, "_archive_errors", lambda _r, rel, _e: ["unarchived work"] if rel.endswith("02") else [])
    monkeypatch.setattr(sys, "argv", ["prune_old_reports.py", "--apply"])
    with pytest.raises(SystemExit, match="unarchived work"):
        pruner.main()
    assert all((tmp_path / p).is_dir() for p in candidates)


def test_archive_preserves_staged_edit_even_when_worktree_matches_archive(archive):
    root, rel, folder, entry, _sha = archive
    shot = folder / "shot.png"
    shot.write_bytes(b"staged work")
    subprocess.run(["git", "add", rel], cwd=root, check=True)
    shot.write_bytes(b"capture")
    assert "Git index differs" in _archive_errors(root, rel, entry)[0]


def test_archive_preserves_fifo_without_reading_it(archive):
    root, rel, folder, entry, _sha = archive
    os.mkfifo(folder / "local.pipe")
    assert "non-regular filesystem" in _archive_errors(root, rel, entry)[0]


def test_archive_preserves_changed_executable_mode(archive):
    root, rel, folder, entry, _sha = archive
    (folder / "shot.png").chmod(0o755)
    assert "file modes differ" in _archive_errors(root, rel, entry)[0]


def test_prune_stops_before_deletion_on_incomplete_reference_scan(tmp_path, monkeypatch):
    monkeypatch.setattr(pruner, "REPO_ROOT", tmp_path)
    def unavailable(_root, *, strict=False):
        assert strict
        raise pruner.report_references.ReferenceScanError("unreadable public source")
    monkeypatch.setattr(pruner.report_references, "referenced_report_paths", unavailable)
    monkeypatch.setattr(sys, "argv", ["prune_old_reports.py", "--apply"])
    with pytest.raises(SystemExit, match="incomplete reference scan"):
        pruner.main()


@pytest.mark.parametrize("reader", ["grep", "ls-files"])
def test_strict_reference_scan_refuses_git_reader_failure(tmp_path, monkeypatch, reader):
    module = pruner.report_references
    real = subprocess.run
    def run(argv, **kwargs):
        if reader in argv:
            return subprocess.CompletedProcess(argv, 2, stdout=b"" if reader == "ls-files" else "")
        return real(argv, **kwargs)
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    monkeypatch.setattr(module.subprocess, "run", run)
    with pytest.raises(module.ReferenceScanError):
        module.referenced_report_paths(tmp_path, strict=True)
    assert module.referenced_report_paths(tmp_path) == set()


def test_strict_reference_scan_refuses_unreadable_source(tmp_path, monkeypatch):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    source = tmp_path / "index.html"
    source.write_text("public page")
    real = Path.read_text
    def read(path, **kwargs):
        if path == source:
            raise PermissionError("unavailable")
        return real(path, **kwargs)
    monkeypatch.setattr(Path, "read_text", read)
    module = pruner.report_references
    with pytest.raises(module.ReferenceScanError, match="Unreadable"):
        module.referenced_report_paths(tmp_path, strict=True)
    assert module.referenced_report_paths(tmp_path) == set()


def test_strict_reference_scan_covers_untracked_plaintext(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    target = PREFIX + "/shot.png"
    (tmp_path / "llms.txt").write_text(target)
    assert target in pruner.report_references.referenced_report_paths(tmp_path, strict=True)


def test_root_capture_selection_rejects_special_entries(tmp_path, monkeypatch):
    monkeypatch.setattr(pruner, "REPORTS_DIR", tmp_path)
    (tmp_path / "visual-qa/2026-01-02").mkdir(parents=True)
    copy = tmp_path / "2026-01-01"
    copy.mkdir()
    (copy / "manifest.json").write_text('{}')
    os.mkfifo(copy / "local.pipe")
    with pytest.raises(argparse.ArgumentTypeError, match="only"):
        _legacy_root_set("2026-01-01")


@pytest.mark.parametrize("failure", ["missing", "stat-error"])
def test_strict_reference_scan_refuses_unavailable_inventoried_source(tmp_path, monkeypatch, failure):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    source = tmp_path / "index.html"
    source.write_text("public page")
    subprocess.run(["git", "add", "index.html"], cwd=tmp_path, check=True)
    if failure == "missing":
        source.unlink()
    else:
        real = Path.lstat
        def unavailable(path, **kwargs):
            if path == source:
                raise PermissionError("unavailable")
            return real(path, **kwargs)
        monkeypatch.setattr(Path, "lstat", unavailable)
    with pytest.raises(pruner.report_references.ReferenceScanError, match="Unavailable"):
        pruner.report_references.referenced_report_paths(tmp_path, strict=True)
