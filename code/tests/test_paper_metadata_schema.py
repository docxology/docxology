"""Regression coverage for canonical and artifact DOI metadata roles."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from paper_metadata_schema import PaperMetadata  # noqa: E402


def test_schema_preserves_distinct_canonical_and_artifact_doi_fields():
    metadata = PaperMetadata.from_dict(
        {
            "title": "Example",
            "doi": "10.5281/zenodo.100",
            "doi_url": "https://doi.org/10.5281/zenodo.100",
            "artifact_doi": "10.5281/zenodo.101",
            "artifact_doi_url": "https://doi.org/10.5281/zenodo.101",
        }
    )

    assert metadata.artifact_doi == "10.5281/zenodo.101"
    assert metadata.to_dict()["artifact_doi_url"] == "https://doi.org/10.5281/zenodo.101"
    assert metadata.validate() == []


def test_schema_rejects_an_artifact_doi_without_a_canonical_identity():
    metadata = PaperMetadata.from_dict(
        {"title": "Example", "artifact_doi": "10.5281/zenodo.101"}
    )

    assert metadata.validate() == [
        "Missing both DOI and venue",
        "Artifact DOI requires a canonical DOI",
    ]
