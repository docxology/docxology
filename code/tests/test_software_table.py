"""Tests for SOFTWARE.md table parsing."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from count_consistency import parse_software_catalog_counts  # noqa: E402
from software_table import (  # noqa: E402
    SoftwareRow,
    description_html,
    doi_role_label_errors,
    iter_software_rows,
    paper_path,
    software_rows_to_dict,
    zenodo_url,
)


def test_software_row_counts():
    rows = list(iter_software_rows())
    docx = [r for r in rows if r.catalog_section == "docxology"]
    aii = [r for r in rows if r.catalog_section == "active-inference-institute"]
    expected_docx, expected_aii = parse_software_catalog_counts()
    assert len(docx) == expected_docx
    assert len(aii) == expected_aii
    assert len(rows) == expected_docx + expected_aii


def test_every_software_row_has_name_github_and_optional_paths():
    repo_root = Path(__file__).resolve().parents[2]
    rows = list(iter_software_rows())
    assert rows
    for row in rows:
        exported = software_rows_to_dict(row)
        assert exported["name"]
        assert exported["url"].startswith("https://github.com/")
        paper = exported["paper_path"]
        if paper:
            assert (repo_root / paper).exists(), paper
        zenodo = exported["zenodo_url"]
        if zenodo:
            assert "zenodo" in zenodo.lower()


def test_description_html_paper_and_zenodo_links():
    raw = (
        "Open generative biology textbook — archived at "
        "[Zenodo](https://doi.org/10.5281/zenodo.20286478) · "
        "[📄](../papers/2026_BiologyTextbook/)"
    )
    html = description_html(raw)
    assert 'href="papers/2026_BiologyTextbook/"' in html
    assert "paper</a>" in html
    assert "https://doi.org/10.5281/zenodo.20286478" in html
    assert paper_path(raw) == "papers/2026_BiologyTextbook/"
    assert zenodo_url(raw) == "https://doi.org/10.5281/zenodo.20286478"


def test_zenodo_url_prefers_explicit_citation_doi_over_preceding_artifact_link():
    raw = (
        "[Zenodo artifact v1.1.0](https://doi.org/10.5281/zenodo.101) · "
        "[Citation DOI](https://doi.org/10.5281/zenodo.100)"
    )

    assert zenodo_url(raw) == "https://doi.org/10.5281/zenodo.100"


def test_description_html_escapes_future_catalog_markup():
    rendered = description_html('Safe <script>alert(1)</script> [Docs](javascript:alert(2))')
    assert "<script>" not in rendered
    assert "&lt;script&gt;" in rendered
    assert "javascript:" not in rendered


def test_doi_role_labels_require_explicit_citation_and_artifact_terms(tmp_path: Path):
    paper_dir = tmp_path / "papers" / "2026_Example"
    paper_dir.mkdir(parents=True)
    (paper_dir / "metadata.json").write_text(
        '{"doi": "10.5281/zenodo.100", "artifact_doi": "10.5281/zenodo.101"}\n',
        encoding="utf-8",
    )
    row = SoftwareRow(
        name="example",
        url="https://github.com/example/example",
        owner="docxology",
        catalog_section="docxology",
        description_raw=(
            "[📄](papers/2026_Example/) · "
            "[Citation DOI](https://doi.org/10.5281/zenodo.100) · "
            "[Zenodo artifact](https://doi.org/10.5281/zenodo.101)"
        ),
        language="Python",
        stars=0,
        updated_or_year="2026",
    )
    assert doi_role_label_errors([row], tmp_path) == []

    artifact_only = row._replace(
        description_raw=(
            "[📄](papers/2026_Example/) · "
            "[Zenodo artifact](https://doi.org/10.5281/zenodo.101)"
        )
    )
    assert doi_role_label_errors([artifact_only], tmp_path) == [
        "example: dual-role linked paper has Zenodo link(s) but omits canonical citation DOI 10.5281/zenodo.100"
    ]

    ambiguous = row._replace(
        description_raw=(
            "[📄](papers/2026_Example/) · "
            "[Zenodo](https://doi.org/10.5281/zenodo.100) · "
            "[Zenodo](https://doi.org/10.5281/zenodo.101)"
        )
    )
    errors = doi_role_label_errors([ambiguous], tmp_path)
    assert errors == [
        "example: canonical DOI link 10.5281/zenodo.100 must be labelled citation or canonical",
        "example: artifact DOI link 10.5281/zenodo.101 must be labelled artifact, version, or download",
    ]
