"""Tests for the Zenodo-uncatalogued diff check."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "code" / "src"
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(ORCH_DIR))

from publication_pairing import ZenodoRecord  # noqa: E402
from report_paths import generated_timestamp  # noqa: E402
from sync_paired_publications import zenodo_record_from_payload  # noqa: E402
from check_zenodo_uncatalogued import (  # noqa: E402
    approved_version_specific_doi_exceptions,
    build_report,
    check_report,
    load_cached_records,
    non_canonical_doi_records,
    uncatalogued_records,
    version_doi,
)


def _record(record_id: str, concept_doi: str, title: str) -> ZenodoRecord:
    return ZenodoRecord(
        record_id=record_id,
        doi=concept_doi,
        title=title,
        publication_date="2026-07-01",
        version="1.0.0",
        resource_type={"type": "publication", "title": "Publication"},
        creators=[{"name": "Friedman, Daniel Ari", "orcid": "0000-0001-6232-9096"}],
        description="A test record.",
        keywords=[],
        related_identifiers=[],
        files=[],
        html_url=f"https://zenodo.org/records/{record_id}",
    )


def test_version_doi_derives_from_record_id():
    record = _record("21298895", "10.5281/zenodo.21298894", "Some Title")
    assert version_doi(record) == "10.5281/zenodo.21298895"


def test_uncatalogued_records_returns_empty_when_concept_doi_present():
    records = [_record("111", "10.5281/zenodo.111", "Catalogued Paper")]
    catalogued = {"10.5281/zenodo.111"}
    assert uncatalogued_records(records, catalogued) == []


def test_uncatalogued_records_returns_empty_when_only_version_doi_present():
    # add_zenodo_only.py's known drift: bibliography stores the version DOI
    # (record_id-derived), not the concept DOI -- still catalogued, just non-canonical.
    records = [_record("21298895", "10.5281/zenodo.21298894", "Reproducible Literature Synthesis")]
    catalogued = {"10.5281/zenodo.21298895"}
    assert uncatalogued_records(records, catalogued) == []


def test_uncatalogued_records_surfaces_record_with_neither_doi_cited():
    records = [
        _record("111", "10.5281/zenodo.111", "Catalogued Paper"),
        _record("999", "10.5281/zenodo.999", "Brand New Uncatalogued Paper"),
    ]
    catalogued = {"10.5281/zenodo.111"}
    missing = uncatalogued_records(records, catalogued)
    assert len(missing) == 1
    assert missing[0].record_id == "999"


def test_non_canonical_doi_records_flags_version_only_citation():
    records = [_record("21298895", "10.5281/zenodo.21298894", "Reproducible Literature Synthesis")]
    catalogued = {"10.5281/zenodo.21298895"}
    flagged = non_canonical_doi_records(records, catalogued)
    assert len(flagged) == 1
    assert flagged[0].record_id == "21298895"


def test_non_canonical_doi_records_empty_when_concept_doi_is_canonical():
    records = [_record("111", "10.5281/zenodo.111", "Catalogued Paper")]
    catalogued = {"10.5281/zenodo.111"}
    assert non_canonical_doi_records(records, catalogued) == []


def test_non_canonical_doi_records_surfaces_distinct_aii_yearly_snapshot_for_review():
    records = [_record("17982447", "10.5281/zenodo.14108991", "AII Ecosystem v3")]
    catalogued = {"10.5281/zenodo.17982447"}

    flagged = non_canonical_doi_records(records, catalogued)
    assert [record.record_id for record in flagged] == ["17982447"]


def test_approved_version_specific_doi_exception_is_emitted_with_asserted_identity():
    records = [
        _record(
            "17982447",
            "10.5281/zenodo.14108991",
            "The Active Inference Institute & Active Inference Ecosystem",
        ),
        _record(
            "15168382",
            "10.5281/zenodo.15168381",
            "On Time",
        ),
    ]
    catalogued = {"10.5281/zenodo.17982447", "10.5281/zenodo.15168382"}

    approved, drift = approved_version_specific_doi_exceptions(records, catalogued)

    assert drift == []
    assert approved == [
        {
            "record_id": "17982447",
            "title": "The Active Inference Institute & Active Inference Ecosystem",
            "concept_doi": "10.5281/zenodo.14108991",
            "version_doi_in_bibliography": "10.5281/zenodo.17982447",
            "reason": (
                "AII Ecosystem v3 is a separately curated 2025 bibliographic "
                "snapshot, distinct from the earlier v2 concept record."
            ),
        },
        {
            "record_id": "15168382",
            "title": "On Time",
            "concept_doi": "10.5281/zenodo.15168381",
            "version_doi_in_bibliography": "10.5281/zenodo.15168382",
            "reason": (
                "On Time is a separately curated 2025 paper snapshot; all "
                "references were deliberately pointed at version record "
                "15168382 in commit d086e7a3 (2026-08-22)."
            ),
        },
    ]



def test_approved_version_specific_doi_exception_fails_closed_on_identity_drift():
    records = [
        _record(
            "17982447",
            "10.5281/zenodo.changed",
            "The Active Inference Institute & Active Inference Ecosystem",
        )
    ]
    catalogued = {"10.5281/zenodo.17982447"}

    approved, drift = approved_version_specific_doi_exceptions(records, catalogued)

    assert approved == []
    assert drift[0]["record_id"] == "17982447"
    assert drift[0]["mismatches"] == ["concept_doi"]


def test_check_report_fails_closed_for_unreviewed_version_doi_and_exception_drift(
    tmp_path: Path,
):
    report = tmp_path / "zenodo_uncatalogued_2026-08-26.json"
    report.write_text(
        json.dumps(
            {
                "warnings": [],
                "uncatalogued_count": 0,
                "uncatalogued": [],
                "non_canonical_doi_count": 1,
                "non_canonical_doi": [{"title": "Unexpected version DOI"}],
                "version_specific_doi_exception_drift_count": 1,
                "version_specific_doi_exception_drift": [{"record_id": "17982447"}],
            }
        ),
        encoding="utf-8",
    )

    problems = check_report(report)

    assert problems == [
        "1 Zenodo record(s) use a version DOI without an approved exception: Unexpected version DOI",
        "1 approved version-DOI exception(s) drifted: 17982447",
    ]


def test_non_canonical_doi_records_empty_when_totally_uncatalogued():
    records = [_record("999", "10.5281/zenodo.999", "Brand New Paper")]
    catalogued: set[str] = set()
    assert non_canonical_doi_records(records, catalogued) == []


def _pairing_report_payload(records: list[ZenodoRecord], *, generated_at: str | None = None, warnings: list[str] | None = None) -> dict:
    return {
        "source": "GitHub Releases API + Zenodo Records API",
        "generated_at": generated_at or generated_timestamp(),
        "warnings": warnings or [],
        "zenodo_records": [record.to_dict() for record in records],
    }


def test_zenodo_record_payload_roundtrip_is_exact():
    record = _record("21298895", "10.5281/zenodo.21298894", "Reproducible Literature Synthesis")
    assert zenodo_record_from_payload(record.to_dict()) == record


def test_load_cached_records_reuses_same_day_pairing_report(tmp_path: Path):
    record = _record("999", "10.5281/zenodo.999", "Brand New Paper")
    path = tmp_path / "paired_publications_2026-09-14.json"
    path.write_text(json.dumps(_pairing_report_payload([record])), encoding="utf-8")
    assert load_cached_records(path) == [record]


def test_load_cached_records_refuses_non_same_day_report_unless_forced(tmp_path: Path):
    record = _record("999", "10.5281/zenodo.999", "Brand New Paper")
    path = tmp_path / "paired_publications_old.json"
    payload = _pairing_report_payload([record], generated_at="2020-01-01T00:00:00Z")
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(SystemExit, match="not same-day"):
        load_cached_records(path)
    assert load_cached_records(path, force=True) == [record]


def test_load_cached_records_refuses_warned_scan_even_when_forced(tmp_path: Path):
    record = _record("999", "10.5281/zenodo.999", "Brand New Paper")
    path = tmp_path / "paired_publications_warned.json"
    payload = _pairing_report_payload([record], warnings=["zenodo: query rate limited"])
    path.write_text(json.dumps(payload), encoding="utf-8")
    with pytest.raises(SystemExit, match="API warning"):
        load_cached_records(path, force=True)


def test_load_cached_records_refuses_non_pairing_report(tmp_path: Path):
    path = tmp_path / "not_a_pairing_report.json"
    path.write_text(json.dumps({"source": "something else"}), encoding="utf-8")
    with pytest.raises(SystemExit, match="unexpected report source"):
        load_cached_records(path)


def test_build_report_uses_injected_records_without_network(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    def _explode():
        raise AssertionError("live fetch must not run when records are injected")

    monkeypatch.setattr("check_zenodo_uncatalogued.fetch_zenodo_records", _explode)
    record = _record("999", "10.5281/zenodo.999", "Brand New Paper")
    report = build_report(tmp_path, records=[record], records_source="cached")
    assert report["uncatalogued_count"] == 1
    assert report["zenodo_records_fetched"] == 1
    assert report["warnings"] == []
    assert report["zenodo_records_source"] == {"mode": "cached", "source_report": None}
