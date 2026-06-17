"""Tests for SOFTWARE.md table parsing."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from count_consistency import parse_software_catalog_counts  # noqa: E402
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
    expected_docx, expected_aii = parse_software_catalog_counts()
    assert len(docx) == expected_docx
    assert len(aii) == expected_aii
    assert len(rows) == expected_docx + expected_aii


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
