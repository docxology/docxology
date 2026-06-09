"""Tests for volatile count consistency helpers."""

from __future__ import annotations

from collections import Counter
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from count_consistency import (
    collect_count_drift,
    parse_bibliography_rows,
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
    rows = parse_bibliography_rows()
    assert len(rows) == 164
    assert sum(1 for row in rows if "../papers/" in row["docs"]) == 147
    assert Counter(row["type"] for row in rows) == {
        "Paper": 143,
        "Presentation": 9,
        "Book": 5,
        "Course": 3,
        "Playbook": 2,
        "Series": 2,
    }
    assert Counter(row["domain"] for row in rows) == {
        "\U0001f41c": 22,
        "\U0001f9e0": 37,
        "\U0001f6e1\ufe0f": 30,
        "\U0001f3a8": 15,
        "\U0001f4bb": 24,
        "\U0001f30d": 6,
        "\U0001f3a5": 15,
        "\U0001f9ec": 15,
    }
    assert parse_software_catalog_counts() == (56, 32)
