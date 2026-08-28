"""Regression tests for deterministic bibliography source visibility."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from biblio_table import BiblioRow  # noqa: E402
from export_bibliography import row_to_work, source_paths  # noqa: E402


def _init_git_fixture(root: Path) -> None:
    for args in (
        ["git", "init", "-q"],
        ["git", "config", "user.email", "test@example.invalid"],
        ["git", "config", "user.name", "Test"],
    ):
        subprocess.run(args, cwd=root, check=True)


def test_ignored_paper_images_cannot_change_the_work_projection(tmp_path: Path):
    _init_git_fixture(tmp_path)
    paper = tmp_path / "papers" / "2026_Example"
    paper.mkdir(parents=True)
    (tmp_path / ".gitignore").write_text("papers/*/images/\n", encoding="utf-8")
    (paper / "README.md").write_text("# Example\n", encoding="utf-8")
    subprocess.run(["git", "add", ".gitignore", "papers/2026_Example/README.md"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-qm", "fixture"], cwd=tmp_path, check=True)
    images = paper / "images"
    images.mkdir()
    (images / "page1.png").write_bytes(b"ignored derivative")

    row = BiblioRow(
        1,
        "2026",
        "🧠",
        "Paper",
        "Example",
        "Venue",
        "https://example.test",
        "[docs](../papers/2026_Example/)",
    )
    visible = source_paths(tmp_path)
    assert "papers/2026_Example/images/page1.png" not in visible
    work = row_to_work(row, visible_source_paths=visible)
    assert work.has_readme is True
    assert work.has_images is False

    # A new non-ignored source file remains visible before staging so intake
    # previews remain useful without reintroducing ignored local artifacts.
    (paper / "full_text.md").write_text("source text\n", encoding="utf-8")
    refreshed = row_to_work(row, visible_source_paths=source_paths(tmp_path))
    assert refreshed.has_full_text is True
    assert refreshed.full_text_url == "/papers/2026_Example/full_text.md"
