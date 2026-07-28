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
  this rule; every other row here is a real drift worth correcting.

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
        if record.doi not in catalogued_dois and version_doi(record) not in catalogued_dois
    ]


def non_canonical_doi_records(records: list[ZenodoRecord], catalogued_dois: set[str]) -> list[ZenodoRecord]:
    """Records cited only by their version DOI, not the documented-canonical concept DOI."""
    return [
        record
        for record in records
        if record.doi
        and version_doi(record)
        and record.doi != version_doi(record)
        and record.doi not in catalogued_dois
        and version_doi(record) in catalogued_dois
    ]


def build_report(repo_root: Path = REPO_ROOT) -> dict[str, object]:
    records, warnings = fetch_zenodo_records()
    catalogued = bibliography_doi_set(repo_root)
    missing = uncatalogued_records(records, catalogued)
    non_canonical = non_canonical_doi_records(records, catalogued)
    return {
        "generated_at": generated_timestamp(),
        "zenodo_records_fetched": len(records),
        "bibliography_dois": len(catalogued),
        "uncatalogued_count": len(missing),
        "non_canonical_doi_count": len(non_canonical),
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
    }


def write_report(repo_root: Path = REPO_ROOT) -> Path:
    report = build_report(repo_root)
    out = repo_root / "reports" / OUT.name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return out


def check_report(repo_root: Path = REPO_ROOT) -> list[str]:
    """Return a list of human-readable problems for the latest report, empty if clean."""
    path = latest_report("zenodo_uncatalogued_*.json", required=False)
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
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diff live Zenodo records for this profile against the curated bibliography."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate the latest report only (no network call); exit 1 if uncatalogued records or API warnings exist",
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
