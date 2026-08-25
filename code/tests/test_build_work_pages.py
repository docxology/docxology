from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import build_work_pages as bwp  # noqa: E402
from generated_outputs import UnsafeGeneratedOutputPathError  # noqa: E402
from site_nav import BREADCRUMB_CSS, breadcrumb_jsonld_script, render_breadcrumb  # noqa: E402


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
