"""Source custody and edition selection for public paper downloads."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from docxology_tools.paper_artifacts import PaperResources, source_file  # noqa: E402
import build_work_pages as bwp  # noqa: E402


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    folder = tmp_path / "papers" / "2026_Example"
    folder.mkdir(parents=True)
    (folder / "README.md").write_text("# A work\n", encoding="utf-8")
    return tmp_path, folder


def resolve(repo):
    root, folder = repo
    return PaperResources.load(root, folder.relative_to(root).as_posix())


def test_lone_pdf_and_encoded_url(repo):
    _, folder = repo
    pdf = folder / 'A paper #1 & β.PDF'
    pdf.write_bytes(b"%PDF-1.7\n")
    resources = resolve(repo)
    assert resources.primary_pdf == pdf
    assert resources.primary_basis == "only archived PDF"
    assert resources.url(pdf).endswith("A%20paper%20%231%20%26%20%CE%B2.PDF")
    assert resources.absolute_url(pdf).startswith("https://danielarifriedman.com/papers/")


def test_primary_wins_over_larger_supplement_and_extraction(repo):
    _, folder = repo
    paper = folder / "paper.pdf"
    paper.write_bytes(b"paper")
    (folder / "supplement.pdf").write_bytes(b"supplement" * 500)
    (folder / "full_text.md").write_text('> Extracted from `supplement.pdf`\n', encoding="utf-8")
    (folder / "metadata.json").write_text(json.dumps({"primary_pdf": "paper.pdf"}), encoding="utf-8")
    resources = resolve(repo)
    assert resources.primary_pdf == paper
    assert resources.primary_basis == "declared primary"
    assert resources.extraction_source == "supplement.pdf"
    assert "extracted text comes from supplement.pdf" in resources.selection_issue
    graph = json.loads(bwp.json_ld(dict(citation_key="Example001", title="Example", year=2026, type="Paper", domain_name="Art", _resources=resources)))
    assert [item["encodingFormat"] for item in graph["encoding"]] == ["application/pdf"]
    assert any(item["name"] == "Extracted text from supplement.pdf" for item in graph["associatedMedia"])


def test_extraction_source_is_identified_without_claiming_latest(repo):
    _, folder = repo
    old = folder / "old.pdf"
    old.write_bytes(b"old")
    (folder / "new.pdf").write_bytes(b"new")
    (folder / "full_text.md").write_text('# Full Text\n\n> Extracted from `old.pdf`\n', encoding="utf-8")
    resources = resolve(repo)
    assert resources.primary_pdf == old
    assert resources.primary_basis == "extracted-text source"


def test_ambiguous_pdfs_are_not_selected_by_size_or_name(repo):
    _, folder = repo
    (folder / "a.pdf").write_bytes(b"a")
    (folder / "z.pdf").write_bytes(b"z" * 1000)
    assert len(resolve(repo).pdfs) == 2
    assert resolve(repo).primary_pdf is None


def test_missing_extraction_source_does_not_promote_another_document(repo):
    _, folder = repo
    (folder / "supplement.pdf").write_bytes(b"supplement")
    (folder / "full_text.md").write_text('> Extracted from `missing.pdf`\n', encoding="utf-8")
    resources = resolve(repo)
    assert resources.primary_pdf is None
    assert resources.selection_issue


@pytest.mark.parametrize("primary", ["missing.pdf", "../outside.pdf", "https://example.org/paper.pdf"])
def test_invalid_declared_primary_fails_closed(repo, primary):
    _, folder = repo
    (folder / "metadata.json").write_text(json.dumps({"primary_pdf": primary}), encoding="utf-8")
    with pytest.raises(ValueError, match="Unavailable primary_pdf"):
        resolve(repo)


def test_ignored_and_symlinked_files_are_not_published(repo, tmp_path):
    root, folder = repo
    (root / ".gitignore").write_text("ignored.pdf\nfull_text.md\nimages/\n", encoding="utf-8")
    (folder / "ignored.pdf").write_bytes(b"ignored")
    (folder / "full_text.md").write_text("private extraction", encoding="utf-8")
    (folder / "images").mkdir()
    (folder / "images" / "private.png").write_bytes(b"private")
    secret = tmp_path / "secret.pdf"
    secret.write_bytes(b"private")
    (folder / "linked.pdf").symlink_to(secret)
    resources = resolve(repo)
    assert not resources.pdfs
    assert resources.full_text is None
    assert not resources.images
    with pytest.raises(ValueError):
        resources.url(secret)


@pytest.mark.parametrize("path", ["../private", "/papers/2026_Example", "papers/2026_Example/../Other", "papers/2026_Example\\private"])
def test_escaped_folder_path_is_rejected(repo, path):
    with pytest.raises(ValueError, match="Invalid paper-folder"):
        PaperResources.load(repo[0], path)


def test_symlinked_folder_and_authoritative_source_are_rejected(repo, tmp_path):
    root, _ = repo
    outside = tmp_path / "outside"
    outside.mkdir()
    (root / "papers" / "2026_Linked").symlink_to(outside)
    with pytest.raises(ValueError, match="Symlinked paper-folder"):
        PaperResources.load(root, "papers/2026_Linked/")
    (root / "papers" / "paper_metadata.json").symlink_to(outside / "private.json")
    with pytest.raises(ValueError, match="Symlinked public source"):
        source_file(root, "papers/paper_metadata.json")


def test_missing_folder_has_no_synthetic_access_links(repo):
    resources = PaperResources.load(repo[0], "papers/2026_Missing/")
    assert not resources.github_url
    assert not resources.docs_url


def test_hardlinked_source_is_rejected_before_public_render(repo, tmp_path):
    root, folder = repo
    private = tmp_path / "private-source"
    private.write_bytes(b"private sentinel")
    os.link(private, folder / "metadata.json")
    with pytest.raises(ValueError, match="Hardlinked paper source"):
        resolve(repo)
    os.link(private, root / "papers" / "paper_metadata.json")
    with pytest.raises(ValueError, match="Hardlinked public source"):
        source_file(root, "papers/paper_metadata.json")
    assert private.read_bytes() == b"private sentinel"


def test_work_page_exposes_pdf_and_folder_and_preserves_text_encoding(repo, monkeypatch):
    root, folder = repo
    (folder / "paper.pdf").write_bytes(b"%PDF-1.7\n")
    (folder / "full_text.md").write_text('> Extracted from `paper.pdf`\n', encoding="utf-8")
    resources = resolve(repo)
    monkeypatch.setattr(bwp, "REPO_ROOT", root)
    (root / "bibliography.bib").write_text("", encoding="utf-8")
    work = dict(citation_key="Example001", num=1, title="Example", year=2026, type="Paper", domain_name="Art", domain="🎨", doi="", url="", authors=[], _resources=resources)
    page = bwp.render_work_page(work)
    assert 'download="paper.pdf"' in page
    assert 'Paper folder on GitHub' in page
    assert 'citation_pdf_url' in page
    graph = json.loads(bwp.json_ld(work))
    assert "author" not in graph
    assert {encoding["encodingFormat"] for encoding in graph["encoding"]} == {"application/pdf", "text/markdown"}
    assert "by Daniel Ari Friedman" not in page


def test_companion_pdfs_do_not_claim_to_encode_the_primary_work(repo):
    _, folder = repo
    (folder / "paper.pdf").write_bytes(b"paper")
    (folder / "example.pdf").write_bytes(b"example")
    (folder / "metadata.json").write_text(json.dumps({"primary_pdf": "paper.pdf", "github_repo": "docxology/example"}), encoding="utf-8")
    resources = resolve(repo)
    work = dict(citation_key="Example001", title="Example", year=2026, type="Paper", domain_name="Art", doi="", url="", _resources=resources)
    graph = json.loads(bwp.json_ld(work))
    assert [item["name"] for item in graph["encoding"]] == ["paper.pdf"]
    assert [item["name"] for item in graph["associatedMedia"]] == ["example.pdf"]
    assert bwp.source_repository_url(resources.docs_path, resources) == "https://github.com/docxology/example"


def test_work_jsonld_normalizes_inert_abstract_without_mutating_source(repo):
    title = 'A </script><img src=x onerror=alert(1)> & "B"'
    abstract = "An abstract </script> with < and >"
    work = dict(citation_key="Example001", title=title, year=2026, type="Paper", domain_name="Art", doi="", url="", _resources=resolve(repo), enrichment={"abstract": abstract})
    payload = bwp.json_ld(work)
    assert "<" not in payload
    graph = json.loads(payload)
    assert graph["name"] == title
    assert graph["abstract"] == "An abstract with < and >"
    assert work["enrichment"]["abstract"] == abstract
