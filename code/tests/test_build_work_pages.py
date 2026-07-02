from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

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
