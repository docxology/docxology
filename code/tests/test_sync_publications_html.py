"""Tests for publications.html sync orchestrator."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from generated_outputs import stale_output_paths, write_output_texts  # noqa: E402
from sync_publications_html import (  # noqa: E402
    PUBLICATIONS_HTML,
    PUBLICATIONS_LD_JSON,
    PUBLICATIONS_TEMPLATE,
    build_collection_page,
    canonical_link_url,
    load_source_template,
    load_rows,
    render_outputs,
    render_outputs_from_template,
    schema_type_for_row,
    validate_rows,
)


def test_dry_run_cli():
    rows = load_rows()
    result = subprocess.run(
        ["python3", "code/orchestrators/sync_publications_html.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert f"OK dry-run: {len(rows)} rows" in result.stdout
    assert f"publications-ld.json would have {len(rows)} mainEntity items" in result.stdout


def test_check_cli_reports_exact_source_rendered_status_without_writing():
    before = {
        PUBLICATIONS_HTML: PUBLICATIONS_HTML.read_bytes(),
        PUBLICATIONS_LD_JSON: PUBLICATIONS_LD_JSON.read_bytes(),
    }
    expected_stale = stale_output_paths(render_outputs(), repo_root=REPO_ROOT)
    result = subprocess.run(
        ["python3", "code/orchestrators/sync_publications_html.py", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert {path: path.read_bytes() for path in before} == before
    if expected_stale:
        assert result.returncode != 0
        assert "Stale source-rendered publication outputs" in result.stderr
        for path in expected_stale:
            assert str(path.relative_to(REPO_ROOT)) in result.stderr
    else:
        assert result.returncode == 0, result.stderr
        assert "Checked 2 publication outputs" in result.stdout


def test_collection_page_entity_count():
    rows = load_rows()
    validate_rows(rows)
    collection = build_collection_page(rows)
    assert collection["@type"] == "CollectionPage"
    assert len(collection["mainEntity"]) == len(rows)
    assert f"{len(rows)} works" in collection["description"]


def test_generated_publications_surfaces():
    rows = load_rows()
    html = PUBLICATIONS_HTML.read_text(encoding="utf-8")
    assert f"{len(rows)} Research Works" in html
    assert '<script type="application/ld+json">' in html
    assert 'src="/data/publications-ld.json"' not in html
    og_match = re.search(r'<meta property="og:title" content="([^"]*)">', html)
    twitter_match = re.search(r'<meta name="twitter:title" content="([^"]*)">', html)
    assert og_match and twitter_match
    assert og_match.group(1) == twitter_match.group(1)

    ld = json.loads(PUBLICATIONS_LD_JSON.read_text(encoding="utf-8"))
    assert ld["@type"] == "CollectionPage"
    assert len(ld["mainEntity"]) == len(rows)
    for entity in ld["mainEntity"]:
        assert entity.get("headline")
        assert entity.get("@type")


def _temporary_publication_outputs(tmp_path: Path, rendered: dict[Path, str]) -> dict[Path, str]:
    """Map canonical source-rendered text to isolated real output files."""
    return {
        tmp_path / "publications.html": rendered[PUBLICATIONS_HTML],
        tmp_path / "data" / "publications-ld.json": rendered[PUBLICATIONS_LD_JSON],
    }


def _replace_in_static_tbody(html_text: str, old: str, new: str) -> str:
    tbody_start = html_text.index('<tbody id="pub-tbody">')
    head, tbody = html_text[:tbody_start], html_text[tbody_start:]
    assert old in tbody
    return head + tbody.replace(old, new, 1)


def test_render_and_check_detect_stale_doi_static_row_and_json_ld(tmp_path: Path):
    """Every generated publication surface must fail an exact no-write check.

    These are the regressions that a count-only dry run misses: a stale DOI
    link, a hand-edited static table row, and a mismatched downloadable JSON-LD
    document.  The HTML cases also prove the renderer replaces the source-owned
    table body instead of preserving its stale contents.
    """
    rendered = render_outputs()
    canonical_html = rendered[PUBLICATIONS_HTML]
    targets = _temporary_publication_outputs(tmp_path, rendered)
    write_output_texts(targets, repo_root=tmp_path)

    tbody = canonical_html[canonical_html.index('<tbody id="pub-tbody">') :]
    doi_match = re.search(r'href="(https://doi\.org/[^"]+)"', tbody)
    assert doi_match
    stale_doi = _replace_in_static_tbody(
        canonical_html,
        doi_match.group(1),
        "https://doi.org/10.0000/stale-static-doi",
    )
    assert render_outputs_from_template(None, stale_doi)[PUBLICATIONS_HTML] == canonical_html

    stale_row = _replace_in_static_tbody(
        canonical_html,
        '<td class="td-num">1</td>',
        '<td class="td-num">999</td>',
    )
    assert render_outputs_from_template(None, stale_row)[PUBLICATIONS_HTML] == canonical_html

    stale_json_ld = rendered[PUBLICATIONS_LD_JSON].replace(
        '"CollectionPage"', '"StaleCollectionPage"', 1
    )

    html_target, json_target = tuple(targets)
    cases = {
        "stale DOI in static tbody": {html_target: stale_doi},
        "stale static tbody row": {html_target: stale_row},
        "stale JSON-LD": {json_target: stale_json_ld},
    }
    for label, changed in cases.items():
        original = {path: path.read_text(encoding="utf-8") for path in changed}
        try:
            for path, stale in changed.items():
                path.write_text(stale, encoding="utf-8")
            assert stale_output_paths(targets, repo_root=tmp_path) == tuple(changed), label
        finally:
            for path, content in original.items():
                path.write_text(content, encoding="utf-8")


def test_source_owned_template_detects_hand_authored_body_framing_drift(tmp_path: Path):
    """A changed body frame cannot become the check-mode render template.

    Before the source-template split, ``render_outputs()`` read
    ``publications.html`` directly, so a changed navigation/header/body frame
    was preserved in its expected output and the no-write check passed.
    """
    template = load_source_template()
    assert PUBLICATIONS_TEMPLATE.is_file()
    assert "{{PUBLICATIONS_INLINE_LD}}" in template
    assert "{{PUBLICATIONS_STATIC_TBODY}}" in template

    rendered = render_outputs()
    canonical_html = rendered[PUBLICATIONS_HTML]
    assert "{{PUBLICATIONS_STATIC_TBODY}}" not in canonical_html
    targets = _temporary_publication_outputs(tmp_path, rendered)
    write_output_texts(targets, repo_root=tmp_path)
    html_target = tmp_path / "publications.html"

    stale_frame = canonical_html.replace(
        '<header class="page-hero">',
        '<header class="page-hero" data-unowned-frame-drift="true">',
        1,
    )
    assert stale_frame != canonical_html
    html_target.write_text(stale_frame, encoding="utf-8")

    assert stale_output_paths(targets, repo_root=tmp_path) == (html_target,)
    assert render_outputs()[PUBLICATIONS_HTML] == canonical_html


def test_apply_mapping_normalizes_publication_targets(tmp_path: Path):
    """The exact mapping used by ``--apply`` restores every checked target."""
    targets = _temporary_publication_outputs(tmp_path, render_outputs())
    write_output_texts(targets, repo_root=tmp_path)
    html_target, json_target = tuple(targets)
    html_target.write_text(targets[html_target] + "\n<!-- stale -->\n", encoding="utf-8")
    json_target.write_text("{}\n", encoding="utf-8")

    assert stale_output_paths(targets, repo_root=tmp_path) == (html_target, json_target)
    write_output_texts(targets, repo_root=tmp_path)
    assert stale_output_paths(targets, repo_root=tmp_path) == ()


def test_render_refuses_a_missing_generated_static_table_body():
    canonical_html = render_outputs()[PUBLICATIONS_HTML]
    missing_tbody = re.sub(
        r'<tbody id="pub-tbody">[\s\S]*?</tbody>',
        "",
        canonical_html,
        count=1,
    )
    with pytest.raises(ValueError, match=r"#pub-tbody"):
        render_outputs_from_template(None, missing_tbody)


def test_canonical_link_url_handles_markdown_doi_and_isbn():
    assert canonical_link_url("[10.5281/zenodo.1](https://doi.org/10.5281/zenodo.1)", "Zenodo") == (
        "https://doi.org/10.5281/zenodo.1"
    )
    assert canonical_link_url("10.5281/zenodo.2", "Zenodo") == "https://doi.org/10.5281/zenodo.2"
    assert canonical_link_url("978-0-12-345678-9", "Publisher") == "https://www.worldcat.org/isbn/978-0-12-345678-9"
    assert canonical_link_url("978-0-12-345678-9", "COGSEC.org") == "https://cogsec.org"
    assert canonical_link_url("—", "Zenodo") == ""


def test_schema_type_for_row_maps_known_types():
    assert schema_type_for_row("Paper") == "ScholarlyArticle"
    assert schema_type_for_row("Book") == "Book"
    assert schema_type_for_row("Presentation") == "PresentationDigitalDocument"
    assert schema_type_for_row("Course") == "Course"
    assert schema_type_for_row("Series") == "CreativeWorkSeries"
    assert schema_type_for_row("Unknown Type") == "ScholarlyArticle"
