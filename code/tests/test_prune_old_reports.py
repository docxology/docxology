"""Tests for dated-report prune helpers."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from prune_old_reports import _working_tree_references  # noqa: E402


PREFIX = "reports/visual-qa/2026-01-01"


def test_working_tree_references_untracked_html(tmp_path: Path):
    (tmp_path / "index.html").write_text(f'<img src="{PREFIX}/shot.png">', encoding="utf-8")
    assert _working_tree_references(tmp_path, PREFIX) is True


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
    assert _working_tree_references(tmp_path, PREFIX) is False

    (tmp_path / "llms.md").write_text(f"see {PREFIX}/shot.png", encoding="utf-8")
    assert _working_tree_references(tmp_path, PREFIX) is True
