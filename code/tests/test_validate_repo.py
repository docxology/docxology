"""Tests for validate_repo report artifact gating."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import validate_repo as vr  # noqa: E402


def test_validation_scope_excludes_dependency_and_cache_trees_but_keeps_docs():
    assert not vr.is_validation_source_path(
        Path(".venv/lib/python3.12/site-packages/package/diagnostic.html")
    )
    assert not vr.is_validation_source_path(Path("node_modules/package/README.md"))
    assert vr.is_validation_source_path(Path("docs/operations/release-integrity.md"))


def test_release_commit_must_match_candidate_head():
    assert vr.release_commit_errors("a" * 40, "a" * 40) == []
    assert vr.release_commit_errors("a" * 40, "b" * 40) == [
        "--release-commit must resolve to the current HEAD; validate another SHA from a checkout at that exact commit"
    ]


def test_public_source_review_provenance_mode_matches_validation_tier():
    assert vr.public_source_review_check_args(release=False) == [
        "python3",
        "code/orchestrators/build_public_source_review.py",
        "--check",
    ]
    assert vr.public_source_review_check_args(release=True) == [
        "python3",
        "code/orchestrators/build_public_source_review.py",
        "--check",
        "--exact-source-revision",
    ]


def test_iter_local_links_ignores_fenced_markdown_examples():
    text = """See [real link](pages/README.md).

```markdown
![Example figure](../output/figures/example.png){#fig:example}
<a href="missing-example.html">example</a>
```
"""

    links = vr.iter_local_links(text)

    assert links == ["pages/README.md"]


def test_validate_json_files_default_warns_on_missing_optional_artifacts(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr(vr, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(vr, "REQUIRED_JSON_FILES", [])
    monkeypatch.setattr(vr, "OPTIONAL_REPORT_PATTERNS", [("accessibility_static_*.json", "accessibility static checks")])
    monkeypatch.setattr(vr, "latest_report", lambda pattern, required=False: None)
    monkeypatch.setattr(vr, "latest_subdir_file", lambda *args, **kwargs: None)

    vr.validate_json_files(False)
    output = capsys.readouterr().out

    assert "optional artifact warnings:" in output
    assert "Optional accessibility static checks report missing: accessibility_static_*.json" in output


def test_validate_json_files_strict_enforces_optional_artifacts(monkeypatch, tmp_path):
    monkeypatch.setattr(vr, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(vr, "REQUIRED_JSON_FILES", [])
    monkeypatch.setattr(vr, "OPTIONAL_REPORT_PATTERNS", [("accessibility_static_*.json", "accessibility static checks")])
    monkeypatch.setattr(vr, "latest_report", lambda pattern, required=False: None)
    monkeypatch.setattr(vr, "latest_subdir_file", lambda *args, **kwargs: None)

    with pytest.raises(SystemExit):
        vr.validate_json_files(True)


def test_validate_json_files_warns_on_optional_invalid_json(monkeypatch, tmp_path):
    (tmp_path / "reports").mkdir()
    invalid = tmp_path / "reports" / "accessibility_static_2026-06-16.json"
    invalid.write_text("{not valid json", encoding="utf-8")

    monkeypatch.setattr(vr, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(vr, "REQUIRED_JSON_FILES", [])
    monkeypatch.setattr(vr, "OPTIONAL_REPORT_PATTERNS", [("accessibility_static_*.json", "accessibility static checks")])
    monkeypatch.setattr(vr, "latest_report", lambda pattern, required=False: invalid)
    monkeypatch.setattr(vr, "latest_subdir_file", lambda *args, **kwargs: None)

    with pytest.raises(SystemExit):
        vr.validate_json_files(True)

    vr.validate_json_files(False)
