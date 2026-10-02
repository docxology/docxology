"""Resource changes must invalidate cached work and paper-page generation."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.generation_plan import (  # noqa: E402
    LOCAL_GENERATION_STEPS,
    step_input_fingerprint,
    step_skip_reason,
)


COMMON_INPUTS = (
    ".gitignore", "data/works.json", "papers/paper_metadata.json",
    "papers/Example/metadata.json", "papers/Example/README.md",
    "papers/Example/AGENTS.md", "papers/Example/SKILL.md",
    "papers/Example/CITATION.cff", "papers/Example/full_text.md",
    "papers/Example/manuscript.PDF", "papers/Example/images/page1.png",
    "code/src/paper_artifacts.py", "code/src/site_nav.py",
    "code/orchestrators/build_work_pages.py", "code/src/metadata_templates.py",
    "code/src/abstract_text.py",
)


def _seed_page_inputs(tmp_path, step):
    for relative in (
        *COMMON_INPUTS, "data/publishing-status.json", "bibliography.bib",
        "code/src/metadata_templates.py", f"code/orchestrators/{step.script}",
    ):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("original\n", encoding="utf-8")
    before = step_input_fingerprint(step, tmp_path)
    assert before is not None, "the fixture must exercise cached generation"
    state = {step.identifier: before}
    assert step_skip_reason(step, state, tmp_path) is not None
    return state


@pytest.mark.parametrize("identifier", ["work-pages", "paper-pages"])
@pytest.mark.parametrize("changed_path", COMMON_INPUTS)
def test_paper_resource_changes_invalidate_page_generation(tmp_path, identifier, changed_path):
    step = next(item for item in LOCAL_GENERATION_STEPS if item.identifier == identifier)
    state = _seed_page_inputs(tmp_path, step)

    (tmp_path / changed_path).write_text("changed\n", encoding="utf-8")

    assert step_skip_reason(step, state, tmp_path) is None


@pytest.mark.parametrize("identifier", ["work-pages", "paper-pages"])
def test_abstract_display_boundary_is_an_explicit_page_generation_input(identifier):
    step = next(item for item in LOCAL_GENERATION_STEPS if item.identifier == identifier)
    assert "code/src/abstract_text.py" in step.inputs


@pytest.mark.parametrize("changed_path", ["data/publishing-status.json", "bibliography.bib"])
def test_work_platform_and_citation_changes_invalidate_page_generation(tmp_path, changed_path):
    test_paper_resource_changes_invalidate_page_generation(tmp_path, "work-pages", changed_path)


@pytest.mark.parametrize("identifier", ["work-pages", "paper-pages"])
def test_adding_another_pdf_invalidates_the_cached_selection(tmp_path, identifier):
    step = next(item for item in LOCAL_GENERATION_STEPS if item.identifier == identifier)
    state = _seed_page_inputs(tmp_path, step)
    (tmp_path / "papers/Example/supplement.pdf").write_bytes(b"new PDF")

    assert step_skip_reason(step, state, tmp_path) is None
