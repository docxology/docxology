"""Tests for volatile count consistency helpers."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))


from docxology_tools.count_consistency import (  # noqa: E402
    _require_software_hero,
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


@pytest.mark.parametrize("label", (
    "Open-Source Repositories", "Owned Repositories", "Public Software and Research Repositories",
))
def test_software_hero_accepts_current_owned_and_legacy_labels(label):
    errors = []
    _require_software_hero(errors, f"**{label} by Example Author**\n")
    assert errors == []


def test_repository_count_prose_does_not_stand_in_for_the_software_hero():
    errors = []
    _require_software_hero(errors, "*167 owned repositories · current totals*\n")
    assert errors == ["pages/SOFTWARE.md software hero: missing repository heading"]


def test_current_canonical_source_counts():
    biblio = canonical_bibliography_snapshot()
    software = canonical_software_snapshot()

    assert biblio["header_works"] == biblio["works"]
    assert biblio["docs_links"] == biblio["paper_folders"]
    assert software["total"] == software["docxology"] + software["aii"]

    docx, aii = parse_software_catalog_counts()
    assert (docx, aii) == (software["docxology"], software["aii"])
