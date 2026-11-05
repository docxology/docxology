"""Explicit remote editions preserve local archives without selecting old bytes."""

from __future__ import annotations

import json
from pathlib import Path
import sys

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401
from docxology_tools.paper_artifacts import PaperResources  # noqa: E402
from docxology_tools import paper_artifacts  # noqa: E402
from docxology_tools.paper_metadata_schema import PaperMetadata  # noqa: E402
from docxology_tools.seo_invariants import check_work_citations  # noqa: E402
from docxology_tools.publication_revisions import revision_notice_html, revision_notice_markdown  # noqa: E402
import build_paper_pages as paper_pages  # noqa: E402
import build_work_pages as work_pages  # noqa: E402
import regenerate_docs as docs  # noqa: E402

REMOTE = {
    "name": "paper.pdf",
    "url": "https://zenodo.org/api/records/123456/files/paper.pdf/content",
    "version": "0.5.0",
    "record_id": "123456",
    "bytes": 1234567,
    "sha256": "a" * 64,
}


def _fixture(tmp_path, *, local=False, remote=None, extracted=False):
    folder = tmp_path / "papers" / "2026_Example"
    folder.mkdir(parents=True)
    (folder / "README.md").write_text("# Example\n", encoding="utf-8")
    meta = {"title": "Example", "doi": "10.5281/zenodo.123455"}
    if remote is not None:
        meta["remote_primary_pdf"] = remote
    (folder / "metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    if local:
        (folder / "paper.pdf").write_bytes(b"preserved historical PDF bytes")
    if extracted:
        (folder / "full_text.md").write_text(
            "# Full text\n\n> Extracted from `paper.pdf`\n\nHistorical text.\n",
            encoding="utf-8",
        )
    visible = frozenset(
        path.relative_to(tmp_path).as_posix()
        for path in folder.iterdir()
        if path.is_file()
    )
    resources = PaperResources.load(tmp_path, "papers/2026_Example/", visible)
    return folder, resources


def _work(resources):
    return {
        "citation_key": "Example001",
        "num": 1,
        "title": "Example",
        "year": 2026,
        "type": "Paper",
        "domain_name": "Art",
        "domain": "🎨",
        "doi": "10.5281/zenodo.123455",
        "url": "https://doi.org/10.5281/zenodo.123455",
        "authors": [],
        "docs_path": "papers/2026_Example/",
        "_resources": resources,
    }


def test_remote_only_work_exposes_direct_current_pdf_on_both_pages(tmp_path, monkeypatch):
    folder, resources = _fixture(tmp_path, remote=REMOTE)
    monkeypatch.setattr(work_pages, "REPO_ROOT", tmp_path)
    (tmp_path / "bibliography.bib").write_text("", encoding="utf-8")
    page = work_pages.render_work_page(_work(resources))
    assert f'<meta name="citation_pdf_url" content="{REMOTE["url"]}">' in page
    assert page.count(REMOTE["url"]) >= 2
    assert "0.5.0" in page
    assert "Zenodo" in page
    rows = paper_pages.pdf_rows(folder, resources)
    assert REMOTE["url"] in rows
    assert "No PDF file" not in rows
    graph = json.loads(work_pages.json_ld(_work(resources)))
    assert graph["encoding"][0]["contentUrl"] == REMOTE["url"]
    assert graph["encoding"][0]["contentSize"] == f'{REMOTE["bytes"]} bytes'


def test_remote_edition_keeps_same_named_local_pdf_and_text_historical(tmp_path, monkeypatch):
    folder, resources = _fixture(tmp_path, remote=REMOTE, local=True, extracted=True)
    original = (folder / "paper.pdf").read_bytes()
    monkeypatch.setattr(work_pages, "REPO_ROOT", tmp_path)
    (tmp_path / "bibliography.bib").write_text("", encoding="utf-8")
    assert resources.primary_pdf is None
    assert resources.primary_pdf_url == REMOTE["url"]
    assert resources.remote_primary_pdf.name == "paper.pdf"
    assert resources.extraction_source == "paper.pdf"
    assert "historical" in resources.selection_issue.lower()
    assert "0.5.0" in resources.selection_issue
    page = work_pages.render_work_page(_work(resources))
    assert "historical" in page.lower()
    assert "paper.pdf" in page
    rows = paper_pages.pdf_rows(folder, resources)
    assert REMOTE["url"] in rows
    assert "../../papers/2026_Example/paper.pdf" in rows
    assert "historical" in rows.lower()
    graph = json.loads(work_pages.json_ld(_work(resources)))
    assert [row["contentUrl"] for row in graph["encoding"]] == [REMOTE["url"]]
    historical = graph["associatedMedia"]
    assert any(row["contentUrl"].endswith("/papers/2026_Example/paper.pdf") for row in historical)
    assert any(row.get("contentUrl", "").endswith("/full_text.md") for row in historical)
    assert (folder / "paper.pdf").read_bytes() == original


def test_local_default_selection_and_urls_are_preserved(tmp_path):
    folder, resources = _fixture(tmp_path, local=True)
    assert resources.primary_pdf == folder / "paper.pdf"
    assert resources.remote_primary_pdf is None
    assert resources.primary_pdf_url.endswith("/papers/2026_Example/paper.pdf")
    assert resources.primary_basis == "only archived PDF"


def test_remote_only_extracted_text_is_not_assumed_to_be_historical(tmp_path):
    _, resources = _fixture(tmp_path, remote=REMOTE, extracted=True)
    assert "historical" not in resources.selection_issue.lower()
    assert "provenance" in resources.selection_issue.lower()
    graph = json.loads(work_pages.json_ld(_work(resources)))
    extracted = [row for row in graph["associatedMedia"] if row.get("encodingFormat") == "text/markdown"]
    assert len(extracted) == 1
    assert "historical" not in extracted[0]["name"].lower()


@pytest.mark.parametrize(
    "change",
    [
        {"url": "http://zenodo.org/api/records/123456/files/paper.pdf/content"},
        {"url": "javascript:alert(1)"},
        {"url": "https://zenodo.org.evil.example/api/records/123456/files/paper.pdf/content"},
        {"url": "https://user@zenodo.org/api/records/123456/files/paper.pdf/content"},
        {"url": REMOTE["url"] + "?download=1"},
        {"url": REMOTE["url"] + "#fragment"},
        {"url": "https://zenodo.org/api/records/999999/files/paper.pdf/content"},
        {"url": "https://zenodo.org/api/records/123456/files/other.pdf/content"},
        {"url": "https://zenodo.org/api/records/123456/files/paper.pdf"},
        {"name": "../paper.pdf"},
        {"name": "notes.txt"},
        {"record_id": "not-a-record"},
        {"version": ""},
        {"bytes": 0},
        {"bytes": -1},
        {"bytes": True},
        {"bytes": "1234567"},
        {"sha256": "not-a-digest"},
    ],
)
def test_unsafe_or_unbound_remote_declarations_fail_closed(tmp_path, change):
    with pytest.raises(ValueError, match="remote|Remote|PDF|Zenodo"):
        _fixture(tmp_path, remote={**REMOTE, **change})


def test_record_download_url_form_is_supported(tmp_path):
    declaration = {**REMOTE, "url": "https://zenodo.org/records/123456/files/paper.pdf"}
    _, resources = _fixture(tmp_path, remote=declaration)
    assert resources.primary_pdf_url == declaration["url"]


def test_regenerated_readme_keeps_current_remote_link_even_when_name_matches_local(tmp_path):
    folder, _ = _fixture(tmp_path, remote=REMOTE, local=True, extracted=True)
    metadata = json.loads((folder / "metadata.json").read_text(encoding="utf-8"))
    metadata["files"] = [{"name": "paper.pdf", "download_url": REMOTE["url"]}]
    paths = docs.DocumentPaths(tmp_path / "papers", tmp_path / "BIBLIOGRAPHY.md")
    readme = docs.generate_readme("2026_Example", metadata, paths=paths)
    assert REMOTE["url"] in readme
    assert "[paper.pdf](paper.pdf)" in readme
    assert "historical" in readme.lower()
    assert "0.5.0" in readme


def test_metadata_schema_roundtrips_explicit_remote_declaration():
    metadata = PaperMetadata.from_dict({"title": "Example", "remote_primary_pdf": REMOTE})
    assert metadata.to_dict()["remote_primary_pdf"] == REMOTE


def test_remote_citation_integrity_gate_rejects_a_different_pdf(tmp_path, monkeypatch):
    folder, resources = _fixture(tmp_path, remote=REMOTE)
    monkeypatch.setattr(work_pages, "REPO_ROOT", tmp_path)
    (tmp_path / "bibliography.bib").write_text("", encoding="utf-8")
    visible = frozenset(path.relative_to(tmp_path).as_posix() for path in folder.iterdir())
    monkeypatch.setattr(paper_artifacts, "source_paths", lambda root: visible)
    work = _work(resources)
    page = work_pages.render_work_page(work)
    work.pop("_resources")
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "works.json").write_text(json.dumps({"works": [work]}), encoding="utf-8")
    (tmp_path / "works").mkdir()
    output = tmp_path / "works" / "Example001.html"
    output.write_text(page, encoding="utf-8")
    assert check_work_citations(tmp_path) == []
    output.write_text(page.replace(REMOTE["url"], "https://zenodo.org/records/999/files/old.pdf", 1), encoding="utf-8")
    assert any("citation_pdf_url" in error for error in check_work_citations(tmp_path))


@pytest.mark.parametrize("render", (revision_notice_html, revision_notice_markdown))
def test_earlier_source_review_does_not_classify_or_certify_a_newer_edition(render):
    summary = "An earlier edition used an inconsistent count; the pinned correction records the source boundary."
    metadata = {
        "publication_date": "2026-11-04",
        "remote_primary_pdf": REMOTE,
        "source_revision_review": {
            "reviewed_at": "2026-10-19",
            "repository": "docxology/example",
            "commit": "1" * 40,
            "document": "docs/review.md",
            "summary": summary,
        },
    }
    notice = render(metadata)
    assert summary in notice
    assert "2026-10-19" in notice
    assert "https://github.com/docxology/example/blob/" + "1" * 40 + "/docs/review.md" in notice
    assert "earlier source edition" in notice
    assert "retain their own source provenance" in notice
    assert "does not certify a newer edition" in notice
    assert "describe the historical archive" not in notice
