"""Tests for dated-report prune helpers."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from prune_old_reports import _retention_errors, _working_tree_references  # noqa: E402


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
