#!/usr/bin/env python3
"""Diff every live Zenodo record under the profile's ORCID against the curated bibliography.

sync_paired_publications.py only emits a report row for a Zenodo record that has
some GitHub-release evidence -- a record with no matching release is silently
absent from its pairs/actions/needs_review output, not flagged. This script
closes that blind spot: it fetches the same live Zenodo query the pairing tool
uses and diffs every record against pages/BIBLIOGRAPHY.md directly.

Two independent findings, not one:

- ``uncatalogued``: neither the record's concept DOI nor its version-specific
  DOI (``10.5281/zenodo.<record_id>``) appears anywhere in the bibliography --
  a genuine gap. Belongs in the bibliography via
  ``add_zenodo_only.py <record_id>`` (see docs/operations/publication-sync.md).
- ``non_canonical_doi``: the record IS represented, but only under its
  version-specific DOI, not the documented canonical concept DOI
  ("Canonical DOI = Zenodo concept DOI", docs/operations/publication-sync.md).
  The yearly AII-Ecosystem snapshots are a documented, deliberate exception to
  this rule. Approved exceptions remain visible in the report and are checked
  against their exact record identity; every other row is actionable drift.

Matching uses every bibliography row with a DOI, not just rows with a local
``papers/`` folder (existing_doi_map() in sync_paired_publications.py requires
a folder, which produces false positives for cited-but-folderless rows such as
playbooks/video transcripts that were never given a paper folder).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

try:
    from report_paths import dated_report_path, generated_timestamp, latest_report
except ImportError:  # pragma: no cover - package import path
    from .report_paths import dated_report_path, generated_timestamp, latest_report  # type: ignore[import]

from publication_pairing import ZenodoRecord
from sync_paired_publications import fetch_zenodo_records, parse_bibliography_rows

OUT = dated_report_path("zenodo_uncatalogued", "json")

# Superseded Zenodo versions retained by the source registry but deliberately
# not catalogued as new works. The current bibliography cites the replacement
# concept/version for each. Keep this explicit so the freshness gate measures
# actionable drift rather than known release-history records.
KNOWN_STALE_RECORD_IDS = {
    "21418901",  # SynthOBS v1.618.0; current row cites concept 21418782
    "20804586",  # CogSecSkills v1; current row cites concept 21513316
    "19139090",  # Template/Reproducible duplicate of kept row #1
}

# These records are intentionally cited by their version DOI because each is
# a separately curated bibliographic snapshot, not merely a software release
# superseded by its Zenodo concept record. Keep the exact identity here rather
# than a bare record-ID allowlist: a changed title, concept DOI, bibliography
# DOI role, or missing record must become a visible, failing review item.
VERSION_SPECIFIC_CITATION_EXCEPTIONS = {
    "17982447": {
        "title": "The Active Inference Institute & Active Inference Ecosystem",
        "concept_doi": "10.5281/zenodo.14108991",
        "version_doi": "10.5281/zenodo.17982447",
        "reason": (
            "AII Ecosystem v3 is a separately curated 2025 bibliographic "
            "snapshot, distinct from the earlier v2 concept record."
        ),
    }
}


def version_doi(record: ZenodoRecord) -> str:
    """The record's own per-version DOI, independent of ZenodoRecord.doi's concept-DOI preference."""
    return f"10.5281/zenodo.{record.record_id}" if record.record_id else ""


def bibliography_doi_set(repo_root: Path = REPO_ROOT) -> set[str]:
    """Every DOI cited in the bibliography, regardless of whether the row has a papers/ folder."""
    return {row["doi"] for row in parse_bibliography_rows(repo_root) if row["doi"]}


def uncatalogued_records(records: list[ZenodoRecord], catalogued_dois: set[str]) -> list[ZenodoRecord]:
    """Records where neither the concept DOI nor the version DOI is cited anywhere."""
    return [
        record
        for record in records
        if record.record_id not in KNOWN_STALE_RECORD_IDS
        and record.doi not in catalogued_dois
        and version_doi(record) not in catalogued_dois
    ]


def non_canonical_doi_records(
    records: list[ZenodoRecord], catalogued_dois: set[str]
) -> list[ZenodoRecord]:
    """All records cited only by their version DOI, not their concept DOI.

    This deliberately includes approved exceptions. ``build_report`` divides
    the result into reviewed exceptions and unresolved drift so that a broad
    record-ID allowlist can never make a future DOI-role change invisible.
    """
    return [
        record
        for record in records
        if record.doi
        and version_doi(record)
        and record.doi != version_doi(record)
        and record.doi not in catalogued_dois
        and version_doi(record) in catalogued_dois
    ]


def approved_version_specific_doi_exceptions(
    records: list[ZenodoRecord], catalogued_dois: set[str]
) -> tuple[list[dict[str, str]], list[dict[str, object]]]:
    """Return explicitly approved exception rows and any identity drift.

    The exception registry is intentionally a complete assertion, not a
    suppression rule. A configured record must be returned by Zenodo and must
    still have the expected title, concept DOI, version DOI, and version-only
    bibliography role. Anything else is a review failure.
    """
    records_by_id = {record.record_id: record for record in records}
    approved: list[dict[str, str]] = []
    drift: list[dict[str, object]] = []

    for record_id, expected in VERSION_SPECIFIC_CITATION_EXCEPTIONS.items():
        record = records_by_id.get(record_id)
        if record is None:
            drift.append(
                {
                    "record_id": record_id,
                    "expected": {"record_id": record_id, **expected},
                    "observed": None,
                    "mismatches": ["record_not_returned_by_zenodo"],
                }
            )
            continue

        observed_version_doi = version_doi(record)
        version_only = record in non_canonical_doi_records([record], catalogued_dois)
        observed = {
            "record_id": record.record_id,
            "title": record.title,
            "concept_doi": record.doi,
            "version_doi": observed_version_doi,
            "version_only_bibliography_citation": version_only,
        }
        mismatches = [
            field
            for field in ("title", "concept_doi", "version_doi")
            if observed[field] != expected[field]
        ]
        if not version_only:
            mismatches.append("version_only_bibliography_citation")
        if mismatches:
            drift.append(
                {
                    "record_id": record_id,
                    "expected": {"record_id": record_id, **expected},
                    "observed": observed,
                    "mismatches": mismatches,
                }
            )
            continue

        approved.append(
            {
                "record_id": record_id,
                "title": record.title,
                "concept_doi": record.doi,
                "version_doi_in_bibliography": observed_version_doi,
                "reason": expected["reason"],
            }
        )

    return approved, drift


def build_report(repo_root: Path = REPO_ROOT) -> dict[str, object]:
    records, warnings = fetch_zenodo_records()
    catalogued = bibliography_doi_set(repo_root)
    missing = uncatalogued_records(records, catalogued)
    version_only = non_canonical_doi_records(records, catalogued)
    approved_exceptions, exception_drift = approved_version_specific_doi_exceptions(
        records, catalogued
    )
    approved_record_ids = {item["record_id"] for item in approved_exceptions}
    non_canonical = [
        record for record in version_only if record.record_id not in approved_record_ids
    ]
    return {
        "generated_at": generated_timestamp(),
        "zenodo_records_fetched": len(records),
        "bibliography_dois": len(catalogued),
        "uncatalogued_count": len(missing),
        "non_canonical_doi_count": len(non_canonical),
        "approved_version_specific_doi_exception_count": len(approved_exceptions),
        "version_specific_doi_exception_drift_count": len(exception_drift),
        "warnings": warnings,
        "uncatalogued": [
            {
                "record_id": record.record_id,
                "doi": record.doi,
                "title": record.title,
                "publication_date": record.publication_date,
                "html_url": record.html_url,
            }
            for record in missing
        ],
        "non_canonical_doi": [
            {
                "record_id": record.record_id,
                "concept_doi": record.doi,
                "version_doi_in_bibliography": version_doi(record),
                "title": record.title,
            }
            for record in non_canonical
        ],
        "approved_version_specific_doi_exceptions": approved_exceptions,
        "version_specific_doi_exception_drift": exception_drift,
    }


def write_report(repo_root: Path = REPO_ROOT) -> Path:
    report = build_report(repo_root)
    out = repo_root / "reports" / OUT.name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return out


def check_report(report_path: Path | None = None) -> list[str]:
    """Return a list of human-readable problems for the latest report, empty if clean."""
    path = report_path or latest_report("zenodo_uncatalogued_*.json", required=False)
    if path is None:
        return ["no zenodo_uncatalogued report found -- run this script without --check first"]
    payload = json.loads(path.read_text(encoding="utf-8"))
    problems = []
    if payload.get("warnings"):
        problems.append(f"API warnings present: {payload['warnings']}")
    count = payload.get("uncatalogued_count", 0)
    if count:
        titles = ", ".join(item["title"] for item in payload.get("uncatalogued", [])[:5])
        problems.append(f"{count} Zenodo record(s) not in the bibliography: {titles}")
    non_canonical_count = payload.get("non_canonical_doi_count", 0)
    if non_canonical_count:
        titles = ", ".join(
            item["title"] for item in payload.get("non_canonical_doi", [])[:5]
        )
        problems.append(
            f"{non_canonical_count} Zenodo record(s) use a version DOI without an approved exception: {titles}"
        )
    exception_drift_count = payload.get(
        "version_specific_doi_exception_drift_count", 0
    )
    if exception_drift_count:
        record_ids = ", ".join(
            item["record_id"]
            for item in payload.get("version_specific_doi_exception_drift", [])[:5]
        )
        problems.append(
            f"{exception_drift_count} approved version-DOI exception(s) drifted: {record_ids}"
        )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diff live Zenodo records for this profile against the curated bibliography."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Validate the latest report only (no network call); exit 1 for API warnings, "
            "uncatalogued records, unresolved DOI-role drift, or changed approved exceptions"
        ),
    )
    args = parser.parse_args()

    if args.check:
        problems = check_report()
        if problems:
            for problem in problems:
                print(problem)
            return 1
        print("checked zenodo_uncatalogued report: 0 uncatalogued records")
        return 0

    out = write_report()
    report = json.loads(out.read_text(encoding="utf-8"))
    count = report["uncatalogued_count"]
    non_canonical_count = report["non_canonical_doi_count"]
    approved_exception_count = report["approved_version_specific_doi_exception_count"]
    exception_drift_count = report["version_specific_doi_exception_drift_count"]
    if count:
        print(f"wrote {out.relative_to(REPO_ROOT)}: {count} record(s) not yet in the bibliography")
        for item in report["uncatalogued"]:
            print(f"  {item['record_id']}  {item['doi']}  {item['title']}")
        print("Add real publications with: uv run python3 code/orchestrators/add_zenodo_only.py <record_id>")
    else:
        print(f"wrote {out.relative_to(REPO_ROOT)}: 0 uncatalogued records (bibliography is caught up)")
    if non_canonical_count:
        print(f"{non_canonical_count} record(s) cited only by version DOI, not the canonical concept DOI:")
        for item in report["non_canonical_doi"]:
            print(f"  {item['record_id']}  bibliography has {item['version_doi_in_bibliography']}, concept is {item['concept_doi']}  {item['title']}")
    if approved_exception_count:
        print(f"{approved_exception_count} approved version-specific DOI exception(s):")
        for item in report["approved_version_specific_doi_exceptions"]:
            print(
                f"  {item['record_id']}  bibliography has {item['version_doi_in_bibliography']}, "
                f"concept is {item['concept_doi']}  {item['title']}"
            )
    if exception_drift_count:
        print(f"{exception_drift_count} approved version-specific DOI exception(s) drifted:")
        for item in report["version_specific_doi_exception_drift"]:
            print(f"  {item['record_id']}  {', '.join(item['mismatches'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
