from __future__ import annotations

import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))


from docxology_tools.generated_outputs import UnsafeGeneratedOutputPathError  # noqa: E402
from docxology_tools.site_nav import BREADCRUMB_CSS, breadcrumb_jsonld_script, render_breadcrumb  # noqa: E402
import build_work_pages as bwp  # noqa: E402


def _work(**overrides: object) -> dict:
    work = {
        "citation_key": "Friedman2026Example001",
        "year": 2026,
        "title": "Example Work",
        "venue": "Zenodo",
        "url": "https://doi.org/10.5281/zenodo.123456",
        "doi": "10.5281/zenodo.123456",
    }
    work.update(overrides)
    return work


def test_citation_text_includes_doi_and_full_url():
    citation = bwp.citation_text(_work())

    assert "DOI: 10.5281/zenodo.123456." in citation
    assert "URL: https://doi.org/10.5281/zenodo.123456." in citation


def test_citation_text_falls_back_to_work_page_url():
    citation = bwp.citation_text(_work(url="", doi=""))

    assert "DOI:" not in citation
    assert "URL: https://danielarifriedman.com/works/Friedman2026Example001.html." in citation


def test_citation_preserves_verified_author_order_and_collectives():
    names = ["Tickles, Dean", "Friedman, Daniel", "Research Collective"]
    work = _work(authors=names, type="Paper", domain_name="Entomology")
    citation = bwp.citation_text(work)
    assert citation.startswith("Tickles, Dean; Friedman, Daniel; Research Collective. 2026.")
    assert citation in bwp.json_ld(work)


def test_citation_does_not_invent_an_author_when_none_are_recorded():
    assert bwp.citation_text(_work()).startswith("2026. Example Work.")


def test_work_page_ownership_requires_an_explicit_renderer_marker(tmp_path: Path):
    manual = tmp_path / "curated.html"
    manual.write_text("<!DOCTYPE html>\n<html><body>Curated by hand</body></html>\n", encoding="utf-8")
    owned = tmp_path / "generated.html"
    owned.write_text(bwp.mark_generated_page("<!DOCTYPE html>\n<html></html>\n"), encoding="utf-8")

    assert not bwp.is_owned_generated_page(manual, repo_root=tmp_path)
    assert bwp.is_owned_generated_page(owned, repo_root=tmp_path)


def test_work_page_ownership_read_rejects_a_symlinked_page(tmp_path: Path):
    outside = tmp_path / "outside.html"
    outside.write_text("manual outside content\n", encoding="utf-8")
    target = tmp_path / "works" / "generated.html"
    target.parent.mkdir()
    target.symlink_to(outside)

    with pytest.raises(UnsafeGeneratedOutputPathError):
        bwp.is_owned_generated_page(target, repo_root=tmp_path)


def test_work_page_uses_shared_breadcrumb_css_markup_and_jsonld():
    work = bwp.load_works()[0]
    trail = bwp.breadcrumb_trail(work)
    rendered = bwp.render_work_page(work)

    assert trail == [
        ("Home", ""),
        ("Works", "works/"),
        (work["title"], f"works/{work['citation_key']}.html"),
    ]
    assert BREADCRUMB_CSS in rendered
    assert breadcrumb_jsonld_script(trail) in rendered
    assert render_breadcrumb(trail, depth=1) in rendered


def test_citation_dates_and_journal_fields_are_source_backed():
    from docxology_tools.citation_metadata import journal_fields, publication_date

    work = _work()
    meta = {
        'doi': work['doi'],
        'publication_date': '2026-10-12',
        'citation_metadata': {
            'doi': work['doi'], 'resource_type': 'journal-article',
            'publication_date': '2026-09-01', 'journal_title': 'Methods & Evidence',
            'volume': '12', 'issue': '3', 'pages': '45–52', 'issn': '1234-5678',
        },
    }
    assert publication_date(work, meta) == '2026-09-01'
    assert journal_fields(work, meta) == {
        'journal_title': 'Methods & Evidence', 'volume': '12', 'issue': '3',
        'issn': '1234-5678', 'firstpage': '45', 'lastpage': '52',
    }
    meta['citation_metadata']['publication_date'] = '2025-09-01'
    assert publication_date(work, meta) == '2026'  # Keep the selected citation year.
    meta['citation_metadata']['doi'] = '10.5281/zenodo.999999'
    assert journal_fields(work, meta) == {}
    assert publication_date(work, meta) == '2026-10-12'
    meta['doi'] = '10.5281/zenodo.999999'
    assert publication_date(work, meta) == '2026'


@pytest.mark.parametrize('value', ['2026-02-30', '2026-13-01', '2026-10', '', None])
def test_citation_date_does_not_invent_precision(value):
    from docxology_tools.citation_metadata import publication_date

    work = _work()
    assert publication_date(work, {'doi': work['doi'], 'publication_date': value}) == '2026'


def test_deposit_is_not_invented_as_journal():
    from docxology_tools.citation_metadata import journal_fields

    work = _work()
    assert journal_fields(work, {'citation_metadata': {
        'doi': work['doi'], 'resource_type': 'posted-content', 'journal_title': 'Zenodo',
    }}) == {}


@pytest.mark.parametrize('metadata', [
    {'citation_metadata': 'invalid'}, {'citation_metadata': None},
    {'citation_metadata': {'doi': 1}}, {'doi': 1},
])
def test_invalid_citation_source_types_fail_explicitly(metadata):
    from docxology_tools.citation_metadata import publication_date

    with pytest.raises(ValueError, match='citation_metadata|citation DOI'):
        publication_date(_work(), metadata)


def test_journal_metadata_block_and_doi_types_fail_explicitly():
    from docxology_tools.citation_metadata import journal_fields

    for metadata in ({'citation_metadata': 'invalid'}, {'citation_metadata': {'doi': 1}}):
        with pytest.raises(ValueError, match='citation_metadata|citation DOI'):
            journal_fields(_work(), metadata)
