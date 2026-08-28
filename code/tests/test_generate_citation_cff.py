"""Regression tests for canonical versus artifact DOI roles in paper CFFs."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import generate_citation_cff as cff  # noqa: E402
from generated_outputs import stale_output_paths, write_output_texts  # noqa: E402


def _metadata() -> dict[str, object]:
    return {
        "title": "Example work",
        "publication_date": "2026-08-26",
        "doi": "10.5281/zenodo.100",
        "artifact_doi": "10.5281/zenodo.101",
        "creators": [{"name": "Friedman, Daniel Ari"}],
    }


def test_reconcile_cff_promotes_canonical_doi_and_keeps_artifact_secondary(tmp_path: Path):
    paper = tmp_path / "papers" / "2026_Example"
    paper.mkdir(parents=True)
    stale = """cff-version: 1.2.0
message: "If you use this work, please cite it as below."
type: article
title: "Example work"
date-released: 2026-08-26
doi: 10.5281/zenodo.101
url: "https://doi.org/10.5281/zenodo.101"
authors:
  - family-names: "Friedman"
    given-names: "Daniel Ari"
identifiers:
  - type: doi
    value: 10.5281/zenodo.101
    description: "Zenodo DOI"
  - type: url
    value: "https://github.com/example/example/releases/tag/v1.0.0"
    description: "GitHub release"
"""

    reconciled = cff.reconcile_cff_doi_roles(stale, _metadata(), paper)

    assert "doi: 10.5281/zenodo.100\n" in reconciled
    assert 'url: "https://doi.org/10.5281/zenodo.100"\n' in reconciled
    assert 'value: "10.5281/zenodo.101"' in reconciled
    assert 'description: "Version/download DOI (Zenodo artifact)"' in reconciled
    assert "https://github.com/example/example/releases/tag/v1.0.0" in reconciled
    assert cff.cff_doi_role_errors(reconciled, _metadata(), paper) == []


def test_render_outputs_check_mapping_detects_and_repairs_a_stale_cff_without_writing(tmp_path: Path):
    paper = tmp_path / "papers" / "2026_Example"
    paper.mkdir(parents=True)
    metadata_path = paper / "metadata.json"
    metadata_path.write_text(json.dumps(_metadata()) + "\n", encoding="utf-8")
    cff_path = paper / "CITATION.cff"
    cff_path.write_text(
        "cff-version: 1.2.0\n"
        "title: \"Example work\"\n"
        "date-released: 2026-08-26\n"
        "doi: 10.5281/zenodo.101\n"
        "url: \"https://doi.org/10.5281/zenodo.101\"\n"
        "authors:\n"
        "  - family-names: \"Friedman\"\n"
        "    given-names: \"Daniel Ari\"\n",
        encoding="utf-8",
    )
    before = cff_path.read_bytes()

    outputs = cff.render_outputs(tmp_path / "papers")
    assert stale_output_paths(outputs, repo_root=tmp_path) == (cff_path,)
    assert cff_path.read_bytes() == before

    write_output_texts(outputs, repo_root=tmp_path)
    assert stale_output_paths(cff.render_outputs(tmp_path / "papers"), repo_root=tmp_path) == ()


def test_legacy_version_doi_metadata_field_fails_closed(tmp_path: Path):
    metadata = {**_metadata(), "version_doi": "10.5281/zenodo.101"}
    try:
        cff.doi_role_values(metadata, tmp_path / "2026_Example")
    except ValueError as exc:
        assert "version_doi is unsupported" in str(exc)
    else:  # pragma: no cover - assertion branch
        raise AssertionError("legacy version_doi must not silently bypass artifact DOI handling")


def test_artifact_doi_without_canonical_doi_fails_closed(tmp_path: Path):
    metadata = {"artifact_doi": "10.5281/zenodo.101"}

    try:
        cff.doi_role_values(metadata, tmp_path / "2026_Example")
    except ValueError as exc:
        assert "requires a canonical doi citation identity" in str(exc)
    else:  # pragma: no cover - assertion branch
        raise AssertionError("an artifact DOI must not become the only CFF identity")
