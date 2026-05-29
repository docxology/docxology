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


def test_policy_entanglement_page_links_docs_pdf_and_work_page():
    path = REPO_ROOT / "papers" / "2026_PolicyEntanglementActive" / "index.html"
    content = render_outputs()[path]

    assert "Policy Entanglement in Active Inference" in content
    assert "10.5281/zenodo.20419637" in content
    assert 'href="README.md"' in content
    assert 'href="AGENTS.md"' in content
    assert 'href="SKILL.md"' in content
    assert "Friedman_2026_Policy_ae7cdd62.pdf" in content
    assert "../../works/Friedman2026PolicyEntanglementActiveInference119.html" in content
    assert 'rel="canonical" href="https://danielarifriedman.com/works/Friedman2026PolicyEntanglementActiveInference119.html"' in content
    assert 'meta name="robots" content="noindex, follow"' in content
    assert "application/ld+json" not in content
