"""Tests for volatile count consistency helpers."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from count_consistency import collect_count_drift, parse_bibliography_work_count, parse_paper_folder_count


def test_parse_bibliography_work_count():
    count = parse_bibliography_work_count()
    assert count >= 116


def test_parse_paper_folder_count():
    count = parse_paper_folder_count()
    assert count >= 109


def test_collect_count_drift_clean_after_sync():
    errors = collect_count_drift()
    assert errors == [], "count drift: " + "; ".join(errors)
