"""Tests for paper full text extraction utilities."""

from __future__ import annotations

import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)


import extract_paper_texts  # noqa: E402


def test_is_scanned_pdf_handles_synthetic_pdf(tmp_path):
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    pdf_path = tmp_path / "blank.pdf"
    with open(pdf_path, "wb") as f:
        writer.write(f)
    assert extract_paper_texts.is_scanned_pdf(pdf_path) is True


def test_extract_text_pypdf_handles_empty(tmp_path):
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    pdf_path = tmp_path / "blank.pdf"
    with open(pdf_path, "wb") as f:
        writer.write(f)
    pages = extract_paper_texts.extract_text_pypdf(pdf_path)
    assert len(pages) == 1
    assert pages[0][0] == 1
    assert pages[0][1] == ""
