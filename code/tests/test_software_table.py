"""Tests for SOFTWARE.md table parsing."""

from __future__ import annotations

import sys
from pathlib import Path

PAPERS_DIR = Path(__file__).resolve().parents[2] / "papers"
sys.path.insert(0, str(PAPERS_DIR))

from software_table import (  # noqa: E402
    description_html,
    iter_software_rows,
    paper_path,
    software_rows_to_dict,
    zenodo_url,
)


def test_software_row_counts():
    rows = list(iter_software_rows())
    docx = [r for r in rows if r.catalog_section == "docxology"]
    aii = [r for r in rows if r.catalog_section == "active-inference-institute"]
    assert len(docx) == 57
    assert len(aii) == 32
    assert len(rows) == 89


def test_biology_textbook_row_fields():
    row = next(r for r in iter_software_rows() if r.name == "biology_textbook")
    assert row.url == "https://github.com/docxology/biology_textbook"
    assert row.language == "Python"
    assert row.stars == 0
    exported = software_rows_to_dict(row)
    assert exported["paper_path"] == "papers/2026_BiologyTextbook/"
    assert exported["zenodo_url"] == "https://doi.org/10.5281/zenodo.20286478"


def test_itrace_row_fields():
    row = next(r for r in iter_software_rows() if r.name == "itrace")
    assert row.url == "https://github.com/docxology/itrace"
    assert row.language == "Python"
    assert row.stars == 0
    exported = software_rows_to_dict(row)
    assert exported["paper_path"] == "papers/2026_ITrace/"
    assert exported["zenodo_url"] == "https://doi.org/10.5281/zenodo.20614909"


def test_description_html_paper_and_zenodo_links():
    raw = (
        "Open generative biology textbook — archived at "
        "[Zenodo](https://doi.org/10.5281/zenodo.20286478) · "
        "[📄](../papers/2026_BiologyTextbook/)"
    )
    html = description_html(raw)
    assert 'href="papers/2026_BiologyTextbook/"' in html
    assert "paper</a>" in html
    assert "https://doi.org/10.5281/zenodo.20286478" in html
    assert paper_path(raw) == "papers/2026_BiologyTextbook/"
    assert zenodo_url(raw) == "https://doi.org/10.5281/zenodo.20286478"
