"""Gallery edition labels require an explicit, source-bound historical claim."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401
from docxology_tools.paper_artifacts import PaperResources  # noqa: E402
import build_paper_pages as paper_pages  # noqa: E402
import build_work_pages as work_pages  # noqa: E402


@pytest.fixture
def gallery(tmp_path):
    folder = tmp_path / "papers/2026_Example"
    images = folder / "images"
    images.mkdir(parents=True)
    (images / "page10_img1.png").write_bytes(b"preserved historical image")
    (images / "page11_img1.png").write_bytes(b"another preserved image")
    (folder / "README.md").write_text("# Example\n", encoding="utf-8")
    (folder / "old.pdf").write_bytes(b"preserved old PDF")
    historical = folder / "full_text_v0.1.md"
    historical.write_text(
        "# Earlier extraction\n\n> Extracted from `old.pdf`\n\n"
        "> 2 figures extracted to `images/`\n", encoding="utf-8"
    )
    (folder / "full_text.md").write_text("# Current edition text\n", encoding="utf-8")
    metadata = {
        "title": "Example", "doi": "10.5281/zenodo.500",
        "remote_primary_pdf": {
            "name": "current.pdf", "url": "https://zenodo.org/records/501/files/current.pdf",
            "version": "0.5.0", "record_id": "501", "bytes": 1234, "sha256": "a" * 64,
        },
    }
    (folder / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
    evidence = {"schema_version": "1.0", "historical_sources": [{
        "file": historical.name, "sha256": hashlib.sha256(historical.read_bytes()).hexdigest(),
        "source_pdf": "old.pdf", "edition": "0.1.0", "images": "images/",
    }]}
    (folder / "source_evidence.json").write_text(json.dumps(evidence), encoding="utf-8")
    return tmp_path, folder, evidence


def _resources(gallery):
    root, folder, _ = gallery
    visible = frozenset(path.relative_to(root).as_posix() for path in folder.rglob("*") if path.is_file())
    return PaperResources.load(root, "papers/2026_Example/", visible)


def _work_page(gallery, monkeypatch):
    root, _, _ = gallery
    monkeypatch.setattr(work_pages, "REPO_ROOT", root)
    (root / "bibliography.bib").write_text("", encoding="utf-8")
    return work_pages.render_work_page({
        "citation_key": "Example001", "num": 1, "title": "Example", "year": 2026,
        "type": "Paper", "domain": "🎨", "domain_name": "Art", "authors": [],
        "doi": "10.5281/zenodo.500", "url": "https://doi.org/10.5281/zenodo.500",
        "docs_path": "papers/2026_Example/", "_resources": _resources(gallery),
    })


def test_explicit_historical_gallery_labels_both_consumers_and_thumbnail_alts(gallery, monkeypatch):
    root, folder, _ = gallery
    monkeypatch.setattr(paper_pages, "REPO_ROOT", root)
    before = {path.name: path.read_bytes() for path in (folder / "images").iterdir()}
    preview = paper_pages.image_gallery_link(folder, "Example", _resources(gallery))
    assert "Historical" in preview
    assert "edition 0.1.0" in preview
    assert "old.pdf" in preview
    assert "full_text_v0.1.md" in preview
    assert 'alt="Historical figure from Example, edition 0.1.0' in preview
    assert "https://raw.githubusercontent.com/docxology/docxology/main/papers/2026_Example/images/page10_img1.png" in preview
    page = _work_page(gallery, monkeypatch)
    assert "Historical figures (edition 0.1.0) on GitHub" in page
    assert "old.pdf" in page
    assert "full_text_v0.1.md" in page
    assert {path.name: path.read_bytes() for path in (folder / "images").iterdir()} == before


def test_remote_primary_alone_does_not_assign_an_edition_to_images(gallery, monkeypatch):
    root, folder, evidence = gallery
    evidence["historical_sources"][0].pop("images")
    (folder / "source_evidence.json").write_text(json.dumps(evidence), encoding="utf-8")
    monkeypatch.setattr(paper_pages, "REPO_ROOT", root)
    preview = paper_pages.image_gallery_link(folder, "Example", _resources(gallery))
    assert "Extracted Images (2)" in preview
    assert 'alt="Figure from Example, page 10"' in preview
    assert "Historical" not in preview
    assert "0.1.0" not in preview
    page = _work_page(gallery, monkeypatch)
    assert ">Figures on GitHub</a>" in page
    assert "Historical figures" not in page


@pytest.mark.parametrize("failure", ("changed-text", "missing-text", "unsafe-path", "ambiguous-source", "unsafe-pdf"))
def test_historical_gallery_provenance_must_remain_exact(gallery, monkeypatch, failure):
    root, folder, evidence = gallery
    entry = evidence["historical_sources"][0]
    if failure == "changed-text":
        (folder / entry["file"]).write_text("Changed historical extraction", encoding="utf-8")
    elif failure == "missing-text":
        (folder / entry["file"]).unlink()
    elif failure == "unsafe-path":
        entry["images"] = "../images/"
    elif failure == "unsafe-pdf":
        entry["source_pdf"] = "../private.pdf"
    else:
        evidence["historical_sources"].append(dict(entry))
    (folder / "source_evidence.json").write_text(json.dumps(evidence), encoding="utf-8")
    monkeypatch.setattr(paper_pages, "REPO_ROOT", root)
    with pytest.raises(ValueError, match="image|Image|historical|Historical"):
        paper_pages.image_gallery_link(folder, "Example", _resources(gallery))
