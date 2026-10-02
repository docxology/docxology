"""Recorded abstracts remain complete source data and render as inert prose."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.abstract_text import abstract_display_text  # noqa: E402
from docxology_tools.generation_plan import LOCAL_GENERATION_STEPS  # noqa: E402
from docxology_tools.paper_artifacts import PaperResources  # noqa: E402
import build_generated_manifest as manifest  # noqa: E402
import build_paper_pages as bpp  # noqa: E402
import build_work_pages as bwp  # noqa: E402
import regenerate_docs as rd  # noqa: E402


@pytest.mark.parametrize("value", [None, False, 0, 2.5, [], {}, "", "  \n "])
def test_missing_or_unsupported_metadata_is_not_invented_into_prose(value):
    assert abstract_display_text(value) == ""


def test_html_keeps_complete_paragraphs_inline_text_entities_breaks_and_urls():
    long_paragraph = "Recorded qualification. " * 60 + "No universal equivalence is claimed."
    raw = (
        '<p><strong>Source release</strong> retains <code>zero_sorry</code> &amp; context.</p>'
        '<p>' + long_paragraph + '</p>'
        '<p>Source: <a href="https://example.test/archive?a=1&amp;b=2">release record</a>.'
        '<br>Final qualification.</p>'
    )
    assert abstract_display_text(raw) == (
        "Source release retains zero_sorry & context.\n\n" + long_paragraph + "\n\n"
        "Source: release record (https://example.test/archive?a=1&b=2).\nFinal qualification."
    )


def test_plain_text_keeps_paragraphs_math_and_literal_encoded_tags():
    raw = "A < B and C > D.\r\n\r\nUse type <T> &amp; keep literal &lt;code&gt; notation."
    assert abstract_display_text(raw) == (
        "A < B and C > D.\n\nUse type <T> & keep literal <code> notation."
    )


def test_urls_are_not_lost_when_labels_only_share_a_prefix_or_an_anchor_is_unclosed():
    assert abstract_display_text(
        '<p><a href="https://example.test/archive">https://example.test/archive2</a></p>'
    ) == "https://example.test/archive2 (https://example.test/archive)"
    assert abstract_display_text(
        '<p><a href="https://example.test/archive">https://example.test/archive</a></p>'
    ) == "https://example.test/archive"
    assert abstract_display_text(
        '<p>Unclosed <a href="https://example.test/archive">source record'
    ) == "Unclosed source record (https://example.test/archive)"


def test_non_prose_html_and_executable_or_credential_urls_are_not_displayed():
    raw = (
        '<p onclick="run()">Recorded prose '
        '<script>alert("not prose")</script><style>.secret{}</style>'
        '<a href="javascript:run()">label</a> '
        '<a href="https://user:password@example.test/">private URL</a>.</p>'
    )
    assert abstract_display_text(raw) == "Recorded prose label private URL."


def _render_fixture(tmp_path, abstract):
    resources = PaperResources.load(tmp_path, "", frozenset())
    work = {
        "citation_key": "Example2026", "num": 1, "year": 2026,
        "title": "Example source record", "type": "Paper", "domain_name": "Mathematics",
        "venue": "Zenodo", "doi": "", "url": "", "_resources": resources,
        "enrichment": {"abstract": abstract, "sources": {}, "keywords": []},
    }
    metadata = {"name": work["title"], "authors": "Recorded Author", "abstract": abstract}
    return work, metadata


def test_work_html_readme_and_structured_abstract_are_safe_without_mutating_source(tmp_path):
    raw = (
        '<p><strong>Recorded release</strong> reports <code>155/155</code>.</p>'
        '<p>A &lt; B. <a href="https://example.test/release?a=1&amp;b=2">Release</a>'
        '<br>No physical-theory proof is claimed.</p>'
        '<p>Literal <img src=x onerror="run()"> notation.</p>'
    )
    work, metadata = _render_fixture(tmp_path, raw)
    original_work, original_metadata = copy.deepcopy(work["enrichment"]), copy.deepcopy(metadata)
    rendered = bwp.render_work_page(work)
    readme = rd.generate_readme("2026_Example", metadata, paths=rd.DocumentPaths(
        tmp_path / "papers", tmp_path / "pages" / "BIBLIOGRAPHY.md",
    ))
    expected = abstract_display_text(raw)
    assert '<p>Recorded release reports 155/155.</p>' in rendered
    assert '<p>A &lt; B. Release (https://example.test/release?a=1&amp;b=2)<br>' in rendered
    assert 'No physical-theory proof is claimed.</p>' in rendered
    assert '<img src=x' not in rendered
    assert '&lt;img src=x onerror=&quot;run()&quot;&gt;' in rendered
    assert json.loads(bwp.json_ld(work))["abstract"] == expected
    assert '&lt;p&gt;' not in rendered
    assert '> Recorded release reports 155/155.\n>\n> A &lt; B.' in readme
    assert '> No physical-theory proof is claimed.' in readme
    assert 'https://example.test/release?a=1&amp;b=2' in readme
    assert '<img src=x' not in readme
    assert '&lt;img src=x onerror="run()"&gt;' in readme
    assert work["enrichment"] == original_work
    assert metadata == original_metadata


def test_plain_work_and_readme_render_every_paragraph_without_changing_metadata(tmp_path):
    raw = "First recorded paragraph.\n\nA < B and type <T>.\nFinal scope qualification."
    work, metadata = _render_fixture(tmp_path, raw)
    rendered = bwp.render_work_page(work)
    readme = rd.generate_readme("2026_Example", metadata)
    assert '<p>First recorded paragraph.</p><p>A &lt; B and type &lt;T&gt;.<br>' in rendered
    assert 'Final scope qualification.</p>' in rendered
    assert '> First recorded paragraph.\n>\n> A &lt; B and type &lt;T&gt;.' in readme
    assert '> Final scope qualification.' in readme
    assert work["enrichment"]["abstract"] == metadata["abstract"] == raw


@pytest.mark.parametrize("raw, expected", [
    (
        '<p><strong>Recorded release</strong> reports <code>155/155</code>.</p>'
        '<p>A &lt; B. <a href="https://example.test/archive">Release</a><br>Final qualification.</p>',
        '<p>Recorded release reports 155/155.</p>'
        '<p>A &lt; B. Release (https://example.test/archive)<br>Final qualification.</p>',
    ),
    (
        'First paragraph.\n\nA < B and literal <img src=x onerror="run()">.\nFinal qualification.',
        '<p>First paragraph.</p><p>A &lt; B and literal &lt;img src=x onerror=&quot;run()&quot;&gt;.'
        '<br>Final qualification.</p>',
    ),
])
def test_paper_page_uses_the_same_inert_display_boundary_and_retains_source(tmp_path, raw, expected):
    folder = tmp_path / "papers" / "2026_Example"
    folder.mkdir(parents=True)
    (folder / "README.md").write_text("# Public example documentation\n", encoding="utf-8")
    resources = PaperResources.load(tmp_path, "papers/2026_Example/",
                                    frozenset({"papers/2026_Example/README.md"}))
    work, _ = _render_fixture(tmp_path, raw)
    work.update({
        "docs_path": "papers/2026_Example/", "_resources": resources,
        "_enrichment": work.pop("enrichment"),
    })
    original = copy.deepcopy(work["_enrichment"])
    rendered = bpp.render_page(work)
    assert '<div class="overview-box">' + expected in rendered
    assert '<img src=x' not in rendered
    assert '&lt;p&gt;' not in rendered
    assert '<meta name="description" content="&lt;p' not in rendered
    assert work["_enrichment"] == original


def test_flat_and_dotted_abstract_helper_imports_share_one_module():
    import abstract_text
    import docxology_tools.abstract_text
    assert abstract_text is docxology_tools.abstract_text


def test_abstract_helper_is_a_declared_input_for_every_connected_renderer():
    for step_id in ("paper-documents", "work-pages", "paper-pages"):
        step = next(step for step in LOCAL_GENERATION_STEPS if step.identifier == step_id)
        assert "code/src/abstract_text.py" in step.inputs
    for name in ("Paper folder doc regeneration", "Work pages", "Paper folder pages"):
        artifact = next(item for item in manifest.ARTIFACTS if item["name"] == name)
        assert "code/src/abstract_text.py" in artifact["sources"]
        assert "code/src/abstract_text.py" not in artifact["outputs"]
