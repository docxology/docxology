"""Software identity selects an explicit software archive without changing citation roles."""

import json
import pytest
from docxology_tools.software_table import (
    SoftwareRow,
    doi_role_label_errors,
    zenodo_url,
    software_archive_url,
)
import sync_software_html as software


@pytest.mark.parametrize(
    "paper,archive", [("20614908", "23404028"), ("23987670", "23987622")]
)
def test_software_jsonld_uses_explicit_software_archive_and_retains_paper_citation(
    tmp_path, paper, archive
):
    description = (
        "[📄](../papers/2026_Example/) · "
        f"[Citation DOI](https://doi.org/10.5281/zenodo.{paper}) · "
        f"[Software archive](https://doi.org/10.5281/zenodo.{archive})"
    )
    row = SoftwareRow(
        "example",
        "https://github.com/example/example",
        "docxology",
        "docxology",
        description,
        "Python",
        0,
        "2026",
    )
    folder = tmp_path / "papers/2026_Example"
    folder.mkdir(parents=True)
    (folder / "metadata.json").write_text(
        json.dumps(
            {"doi": "10.5281/zenodo." + paper, "artifact_doi": "10.5281/zenodo.999"}
        )
    )
    assert zenodo_url(description) == "https://doi.org/10.5281/zenodo." + paper
    assert doi_role_label_errors([row], tmp_path) == []
    entity = software.main_entity_object(row)
    assert entity["@type"] == "SoftwareSourceCode"
    assert entity["sameAs"] == "https://doi.org/10.5281/zenodo." + archive


@pytest.mark.parametrize(
    "description,expected",
    [
        (
            "[Zenodo](https://doi.org/10.5281/zenodo.100)",
            "https://doi.org/10.5281/zenodo.100",
        ),
        (
            "[Artifact](https://doi.org/10.5281/zenodo.101) · [Citation DOI](https://doi.org/10.5281/zenodo.100)",
            "https://doi.org/10.5281/zenodo.100",
        ),
        ("Repository without a DOI", None),
    ],
)
def test_legacy_software_identity_fallback_is_unchanged(description, expected):
    row = SoftwareRow(
        "example",
        "https://github.com/example/example",
        "docxology",
        "docxology",
        description,
        "Python",
        0,
        "2026",
    )
    assert software.main_entity_object(row).get("sameAs") == expected


@pytest.mark.parametrize(
    "folder,paper,artifact",
    [
        ("2026_CognitiveCaseDiagrams", "19695259", "22774403"),
        ("2026_BlackLine", "21754235", "22833503"),
        ("2026_GoldenLine", "21754237", "22833506"),
        ("2026_WitnessRegister", "21754245", "22833511"),
    ],
)
def test_linked_paper_citation_is_not_software_identity(
    tmp_path, folder, paper, artifact
):
    description = (
        f"[📄](../papers/{folder}/) · "
        f"[Citation DOI](https://doi.org/10.5281/zenodo.{paper})"
    )
    row = SoftwareRow(
        "example", "https://github.com/example/example", "docxology", "docxology",
        description, "Python", 0, "2026",
    )
    destination = tmp_path / "papers" / folder
    destination.mkdir(parents=True)
    (destination / "metadata.json").write_text(
        json.dumps({"doi": "10.5281/zenodo." + paper,
                    "artifact_doi": "10.5281/zenodo." + artifact})
    )
    assert zenodo_url(description) == "https://doi.org/10.5281/zenodo." + paper
    assert doi_role_label_errors([row], tmp_path) == []
    assert "sameAs" not in software.main_entity_object(row)
    assert software_archive_url(description) == ""


def test_linked_paper_artifact_does_not_make_its_citation_a_software_identity():
    description = (
        "[📄](../papers/2026_Example/) · "
        "[Artifact](https://doi.org/10.5281/zenodo.101) · "
        "[Citation DOI](https://doi.org/10.5281/zenodo.100)"
    )
    row = SoftwareRow(
        "example", "https://github.com/example/example", "docxology", "docxology",
        description, "Python", 0, "2026",
    )
    assert zenodo_url(description) == "https://doi.org/10.5281/zenodo.100"
    assert "sameAs" not in software.main_entity_object(row)
    assert software_archive_url(description) == ""


def test_unlabelled_linked_paper_keeps_legacy_software_identity_fallback():
    description = (
        "[📄](../papers/2026_Example/) · "
        "[Zenodo](https://doi.org/10.5281/zenodo.100)"
    )
    row = SoftwareRow(
        "example", "https://github.com/example/example", "docxology", "docxology",
        description, "Python", 0, "2026",
    )
    assert software_archive_url(description) == zenodo_url(description)
    assert software.main_entity_object(row)["sameAs"] == zenodo_url(description)
