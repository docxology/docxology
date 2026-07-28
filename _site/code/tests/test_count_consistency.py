"""Tests for volatile count consistency helpers."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from count_consistency import (
    canonical_bibliography_snapshot,
    canonical_software_snapshot,
    collect_count_drift,
    parse_bibliography_work_count,
    parse_paper_folder_count,
    parse_software_catalog_counts,
)


def test_parse_bibliography_work_count():
    count = parse_bibliography_work_count()
    assert count >= 117


def test_parse_paper_folder_count():
    count = parse_paper_folder_count()
    assert count >= 110


def test_collect_count_drift_clean_after_sync():
    errors = collect_count_drift()
    assert errors == [], "count drift: " + "; ".join(errors)


def test_current_canonical_source_counts():
    biblio = canonical_bibliography_snapshot()
    software = canonical_software_snapshot()

    assert biblio["header_works"] == biblio["works"]
    assert biblio["docs_links"] == biblio["paper_folders"]
    assert software["total"] == software["docxology"] + software["aii"]

    docx, aii = parse_software_catalog_counts()
    assert (docx, aii) == (software["docxology"], software["aii"])
