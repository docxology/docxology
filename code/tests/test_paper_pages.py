"""Tests for generated paper-folder landing pages."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(ORCH_DIR))

from build_paper_pages import render_outputs, validate_inputs  # noqa: E402


def test_every_docs_path_has_required_folder_docs():
    assert validate_inputs() == []


def test_render_outputs_cover_all_nonempty_docs_paths():
    works = json.loads((REPO_ROOT / "data" / "works.json").read_text(encoding="utf-8"))["works"]
    expected = {str(work["docs_path"]).rstrip("/") for work in works if work.get("docs_path")}
    outputs = render_outputs()
    actual = {str(path.relative_to(REPO_ROOT).parent) for path in outputs}

    assert actual == expected


def test_docs_folder_page_links_local_docs_and_canonical():
    works = json.loads((REPO_ROOT / "data" / "works.json").read_text(encoding="utf-8"))["works"]
    work = next(item for item in works if item.get("docs_path") and item.get("doi"))
    path = REPO_ROOT / work["docs_path"] / "index.html"
    content = render_outputs()[path]

    assert 'href="README.md"' in content
    assert 'href="AGENTS.md"' in content
    assert 'href="SKILL.md"' in content
    assert work["citation_key"] in content
    assert work["doi"] in content or "doi.org" in content
    assert 'name="robots"' not in content
    assert "application/ld+json" not in content
