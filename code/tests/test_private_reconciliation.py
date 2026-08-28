"""Focused tests for private/public reconciliation classification and rendering."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from private_reconciliation import (  # noqa: E402
    bibliography_rows,
    classify_path,
    default_decision,
    parse_name_status_z,
    render_markdown,
    source_backed_metadata_fields,
)


def test_classifier_keeps_paper_metadata_distinct_from_generated_and_binary_content():
    patterns = ("works/*.html", "og-*.jpg")

    assert classify_path("papers/2025_OnTime/metadata.json", patterns) == "source_metadata"
    assert classify_path("papers/2025_OnTime/full_text.md", patterns) == "derived_output"
    assert classify_path("papers/2025_OnTime/images/page1.png", patterns) == "binary_intake"
    assert classify_path("works/Friedman2025Time017.html", patterns) == "derived_output"
    assert classify_path("og-active-inference.jpg", patterns) == "derived_output"
    assert classify_path("README.md", patterns) == "other_source"


def test_classifier_decisions_are_conservative():
    assert default_decision("derived_output")[0] == "regenerate"
    assert default_decision("binary_intake")[0] == "defer"
    assert default_decision("source_metadata")[0] == "defer"


def test_name_status_parser_preserves_rename_source_and_destination():
    changes = parse_name_status_z(b"M\0pages/BIBLIOGRAPHY.md\0R095\0old.png\0new.png\0")

    assert changes[0].status == "M"
    assert changes[0].path == "pages/BIBLIOGRAPHY.md"
    assert changes[1].status == "R095"
    assert changes[1].previous_path == "old.png"
    assert changes[1].path == "new.png"


def test_private_bibliography_agreement_is_a_deferred_doi_candidate():
    bibliography = bibliography_rows(
        "| 17 | 2025 | Art | Paper | On Time | Zenodo | [10.5281/zenodo.15168382](https://doi.org/10.5281/zenodo.15168382) | [folder](../papers/2025_OnTime/) | Friedman |\n"
    )
    public = {"doi": "10.5281/zenodo.15168381", "zenodo_record": "https://zenodo.org/records/15168381"}
    private = {"doi": "10.5281/zenodo.15168382", "zenodo_record": "https://zenodo.org/records/15168382"}

    findings = source_backed_metadata_fields("2025_OnTime", public, private, bibliography)

    assert [item["field"] for item in findings] == ["doi"]
    assert findings[0]["decision"] == "defer"
    assert "candidate-only" in findings[0]["implementation"]


def test_markdown_report_clearly_marks_deferred_and_ported_items():
    payload = {
        "report_date": "2026-08-25",
        "baseline": {"requested": "public", "resolved": "abc"},
        "private_ref": {"requested": "private", "resolved": "def"},
        "summary": {
            "classifications": {
                "source_metadata": {"count": 2, "decision": "defer"},
                "derived_output": {"count": 3, "decision": "regenerate"},
                "binary_intake": {"count": 1, "decision": "defer"},
                "other_source": {"count": 4, "decision": "defer"},
            },
            "deferred_metadata_fields": 5,
            "metadata_files_reviewed": 2,
        },
        "private_identity_candidates": [
            {
                "folder": "2025_OnTime",
                "field": "doi",
                "baseline_value": "old",
                "private_value": "new",
                "decision": "defer",
                "release_status": "deferred pending independent public authority",
            }
        ],
    }

    report = render_markdown(payload)

    assert "read-only comparison" in report
    assert "2025_OnTime" in report
    assert "Treat private metadata/bibliography agreement" in report
    assert "Defer all PDFs" in report
