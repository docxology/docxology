"""Measured Scholar prerequisites cannot imply inclusion or follow private aliases."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.scholar_readiness import PDF_BYTE_LIMIT, build_report, render_markdown  # noqa: E402


def fixture(root, *, pdf=True, size=20):
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    (root / "data").mkdir()
    (root / "works").mkdir()
    folder = root / "papers/2026_Example"
    folder.mkdir(parents=True)
    work = {"citation_key": "Example", "title": "An example", "type": "Paper", "docs_path": "papers/2026_Example/"}
    (root / "data/works.json").write_text(json.dumps({"works": [work]}))
    tags = '<meta name="citation_title" content="An example"><meta name="citation_author" content="A. Author"><meta name="citation_publication_date" content="2026">'
    if pdf:
        (folder / "paper.pdf").write_bytes(b"x" * size)
        tags += '<meta name="citation_pdf_url" content="https://danielarifriedman.com/papers/2026_Example/paper.pdf">'
    (root / "works/Example.html").write_text("<html><head>" + tags + "</head><body>Summary</body></html>")
    return folder


def test_directory_gap_and_hash_bound_measurements(tmp_path):
    fixture(tmp_path)
    report = build_report(tmp_path)
    row = report["works"][0]
    assert row["blockers"] == ["pdf_directory_differs_from_abstract"]
    assert row["primary_pdf"]["bytes"] == 20
    assert len(row["primary_pdf"]["sha256"]) == 64
    assert "searchable_pdf" in row["unverified_requirements"]
    assert not report["indexing_verified"] and not report["network_checked"]
    assert build_report(tmp_path) == report
    assert "do not establish Scholar inclusion" in render_markdown(report)


@pytest.mark.parametrize("size,oversized", [(PDF_BYTE_LIMIT, False), (PDF_BYTE_LIMIT + 1, True)])
def test_size_boundary(tmp_path, size, oversized):
    fixture(tmp_path, size=size)
    row = build_report(tmp_path)["works"][0]
    assert ("pdf_exceeds_byte_limit" in row["blockers"]) is oversized


def test_missing_pdf_and_body_or_comment_tags(tmp_path):
    fixture(tmp_path, pdf=False)
    (tmp_path / "works/Example.html").write_text('<head><!-- <meta name="citation_author" content="Fake"> --></head><body><meta name="citation_title" content="Fake"></body>')
    blockers = build_report(tmp_path)["works"][0]["blockers"]
    assert "no_selected_local_pdf" in blockers
    assert "missing_citation_author" in blockers and "missing_citation_title" in blockers


def test_ambiguous_pdf_is_never_guessed(tmp_path):
    folder = fixture(tmp_path)
    (folder / "second.pdf").write_bytes(b"other")
    row = build_report(tmp_path)["works"][0]
    assert row["primary_pdf"] is None
    assert "no_selected_local_pdf" in row["blockers"]


def test_whitespace_only_citation_fields_are_missing(tmp_path):
    fixture(tmp_path)
    page = tmp_path / "works/Example.html"
    page.write_text(page.read_text().replace('content="A. Author"', 'content=" &#9; "'))
    assert "missing_citation_author" in build_report(tmp_path)["works"][0]["blockers"]


@pytest.mark.parametrize("field", ["citation_title", "citation_publication_date", "citation_doi", "citation_pdf_url"])
def test_duplicate_singleton_metadata_is_blocked(tmp_path, field):
    fixture(tmp_path)
    page = tmp_path / "works/Example.html"
    extra = f'<meta name="{field}" content="Duplicate">'
    if field == "citation_doi":
        extra *= 2
    page.write_text(page.read_text().replace('</head>', extra + '</head>'))
    assert f"duplicate_{field}" in build_report(tmp_path)["works"][0]["blockers"]


def test_catalogued_doi_requires_nonempty_doi_tag(tmp_path):
    fixture(tmp_path)
    dataset = tmp_path / "data/works.json"
    works = json.loads(dataset.read_text())
    works["works"][0]["doi"] = "10.1234/example"
    dataset.write_text(json.dumps(works))
    assert "missing_citation_doi" in build_report(tmp_path)["works"][0]["blockers"]
    page = tmp_path / "works/Example.html"
    page.write_text(page.read_text().replace('</head>', '<meta name="citation_doi" content="10.1234/example"></head>'))
    assert "missing_citation_doi" not in build_report(tmp_path)["works"][0]["blockers"]


def test_source_change_changes_evidence(tmp_path):
    folder = fixture(tmp_path)
    first = build_report(tmp_path)
    (folder / "paper.pdf").write_bytes(b"different")
    second = build_report(tmp_path)
    assert first["works"][0]["primary_pdf"]["sha256"] != second["works"][0]["primary_pdf"]["sha256"]


def test_private_alias_is_rejected(tmp_path):
    fixture(tmp_path)
    original = tmp_path / "data/works.json"
    hidden = tmp_path / "private.json"
    original.rename(hidden)
    original.symlink_to(hidden)
    with pytest.raises(ValueError, match="Symlinked"):
        build_report(tmp_path)
