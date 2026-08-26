"""Tests for the Zenodo-uncatalogued diff check."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "code" / "src"
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(ORCH_DIR))

from publication_pairing import ZenodoRecord  # noqa: E402
from check_zenodo_uncatalogued import (  # noqa: E402
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


def test_non_canonical_doi_records_omits_distinct_aii_yearly_snapshot():
    records = [_record("17982447", "10.5281/zenodo.14108991", "AII Ecosystem v3")]
    catalogued = {"10.5281/zenodo.17982447"}

    assert non_canonical_doi_records(records, catalogued) == []


def test_non_canonical_doi_records_empty_when_totally_uncatalogued():
    records = [_record("999", "10.5281/zenodo.999", "Brand New Paper")]
    catalogued: set[str] = set()
    assert non_canonical_doi_records(records, catalogued) == []
