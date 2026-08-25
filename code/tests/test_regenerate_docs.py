from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import regenerate_docs as rd  # noqa: E402


CANONICAL_DOI = "10.5281/zenodo.10000001"
ARTIFACT_DOI = "10.5281/zenodo.10000002"


def _write_paper_fixture(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    metadata_doi: str = CANONICAL_DOI,
    artifact_doi: str | None = None,
) -> tuple[Path, Path, Path]:
    """Create a real minimal paper tree and point the generator at it."""
    papers = tmp_path / "papers"
    folder = papers / "2026_Example"
    pages = tmp_path / "pages"
    folder.mkdir(parents=True)
    pages.mkdir()
    metadata = {
        "2026_Example": {
            "name": "Example Paper",
            "authors": "Daniel Ari Friedman",
            "abstract": "A deterministic test paper.",
            "keywords": ["example"],
            "doi": metadata_doi,
        }
    }
    if artifact_doi is not None:
        metadata["2026_Example"]["artifact_doi"] = artifact_doi
    (papers / "paper_metadata.json").write_text(json.dumps(metadata), encoding="utf-8")
    bibliography = "\n".join(
        [
            "| # | Year | Domain | Type | Title | Venue | DOI/Link | Docs |",
            "|--:|:----:|:------:|:----:|-------|-------|----------|:----:|",
            (
                "| 1 | 2026 | 💻 | Paper | Example Paper | *Zenodo* | "
                f"[{CANONICAL_DOI}](https://doi.org/{CANONICAL_DOI}) | "
                "[📁](../papers/2026_Example/) |"
            ),
            "",
        ]
    )
    bibliography_path = pages / "BIBLIOGRAPHY.md"
    bibliography_path.write_text(bibliography, encoding="utf-8")
    monkeypatch.setattr(rd, "PAPERS_DIR", papers)
    monkeypatch.setattr(rd, "BIBLIOGRAPHY_PATH", bibliography_path)
    return papers, folder, bibliography_path


def test_truncate_display_text_avoids_mid_token_urls():
    text = "Intro " + ("word " * 30) + "https://www.youtube.com/watch?v=abcdef"

    shortened = rd.truncate_display_text(text, limit=150)

    assert "https://www.youtube.co..." not in shortened
    assert shortened.endswith("...")


def test_generate_readme_normalizes_markdown_doi_link():
    meta = {
        "name": "Example Paper",
        "authors": "Daniel Ari Friedman",
        "abstract": (
            "<p>Example &mdash; abstract.</p>\n\n"
            "---\nAssociated artifacts\n"
            "DOI: https://doi.org/10.5281/zenodo.20396328"
        ),
        "doi": "10.5281/zenodo.20396328",
        "doi_url": "https://doi.org/10.5281/zenodo.20396328",
        "artifact_doi": "10.5281/zenodo.20396329",
        "artifact_doi_url": "https://doi.org/10.5281/zenodo.20396329",
        "github_repo": "docxology/entofile",
        "github_release_url": "https://github.com/docxology/entofile/releases/tag/v0.4",
        "release_tag": "v0.4",
        "zenodo_record": "https://zenodo.org/records/20396328",
        "files": [
            {
                "name": "Enhanced NSF Postdoctoral Reporting via Synthetic Intelligence Language Processing (1).pdf",
                "download_url": "https://zenodo.org/api/records/10160657/files/Enhanced%20NSF%20Postdoctoral%20Reporting%20via%20Synthetic%20Intelligence%20Language%20Processing%20(1).pdf/content",
            }
        ],
        "keywords": ["example"],
    }
    bib_entry = {
        "venue": "Zenodo",
        "link": "[10.5281/zenodo.20396328](https://doi.org/10.5281/zenodo.20396328)",
        "domain": "💻",
    }

    readme = rd.generate_readme("2026_Example", meta, bib_entry)

    assert "> Example \u2014 abstract." in readme
    assert "Associated artifacts" not in readme
    assert "<p>" not in readme
    assert "[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20396328-blue)](https://doi.org/10.5281/zenodo.20396328)" in readme
    assert "- DOI: [10.5281/zenodo.20396328](https://doi.org/10.5281/zenodo.20396328)" in readme
    assert "- Artifact DOI: [10.5281/zenodo.20396329](https://doi.org/10.5281/zenodo.20396329)" in readme
    assert "- GitHub repository: [docxology/entofile](https://github.com/docxology/entofile)" in readme
    assert "- GitHub release: [v0.4](https://github.com/docxology/entofile/releases/tag/v0.4)" in readme
    assert "- Zenodo record: [https://zenodo.org/records/20396328](https://zenodo.org/records/20396328)" in readme
    assert (
        "[Enhanced NSF Postdoctoral Reporting via Synthetic Intelligence Language Processing (1).pdf]"
        "(https://zenodo.org/api/records/10160657/files/"
        "Enhanced%20NSF%20Postdoctoral%20Reporting%20via%20Synthetic%20Intelligence%20Language%20Processing%20%281%29.pdf/content)"
    ) in readme
    assert "https:%2F%2F" not in readme
    assert "]([" not in readme
    assert (
        "> Daniel Ari Friedman (2026). *Example Paper*. Zenodo. "
        "DOI: 10.5281/zenodo.20396328. URL: https://doi.org/10.5281/zenodo.20396328."
    ) in readme


def test_generated_documents_are_deterministic_and_check_detects_real_drift(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    papers, folder, _ = _write_paper_fixture(tmp_path, monkeypatch)
    legacy_log = papers / "regenerate_docs.log"

    assert rd.main(["--apply"]) == 0
    generated = {name: (folder / name).read_text(encoding="utf-8") for name in rd.DOCUMENT_FILENAMES}
    manifest_path = papers / rd.MANIFEST_FILENAME
    manifest_before = manifest_path.read_text(encoding="utf-8")
    assert not legacy_log.exists()
    assert all(rd.is_generated_document(name, content) for name, content in generated.items())

    assert rd.main(["--check"]) == 0
    assert {name: (folder / name).read_text(encoding="utf-8") for name in rd.DOCUMENT_FILENAMES} == generated
    assert manifest_path.read_text(encoding="utf-8") == manifest_before
    assert not legacy_log.exists()

    managed_path = folder / "AGENTS.md"
    managed_path.write_text(generated["AGENTS.md"] + "\n<!-- manual drift -->\n", encoding="utf-8")
    assert rd.main(["--check"]) == 1
    assert managed_path.read_text(encoding="utf-8").endswith("<!-- manual drift -->\n")
    assert manifest_path.read_text(encoding="utf-8") == manifest_before
    assert not legacy_log.exists()


def test_check_rejects_semantically_valid_but_noncanonical_manifest_bytes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    papers, _folder, _ = _write_paper_fixture(tmp_path, monkeypatch)

    assert rd.main(["--apply"]) == 0
    manifest_path = papers / rd.MANIFEST_FILENAME
    expected = manifest_path.read_text(encoding="utf-8")
    payload = json.loads(expected)
    # This keeps every ownership record intact while changing only formatting
    # and ordering—the precise false-green case a parsed-object comparison
    # would miss.
    payload["documents"] = list(reversed(payload["documents"]))
    manifest_path.write_text(json.dumps(payload, indent=4) + "\n", encoding="utf-8")

    assert rd.main(["--check"]) == 1
    assert manifest_path.read_text(encoding="utf-8") != expected

    assert rd.main(["--apply"]) == 0
    assert manifest_path.read_text(encoding="utf-8") == expected
    assert rd.main(["--check"]) == 0


def test_symlinked_manifest_is_rejected_before_any_read_or_write(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """The ownership manifest must never redirect the renderer outside papers/."""
    papers, _folder, _ = _write_paper_fixture(tmp_path, monkeypatch)
    manifest_path = papers / rd.MANIFEST_FILENAME
    external_manifest = tmp_path / "external-manifest.json"
    external_content = '{"version": 1, "documents": []}\n'
    external_manifest.write_text(external_content, encoding="utf-8")
    manifest_path.symlink_to(external_manifest)

    with pytest.raises(ValueError, match="symlinked generated-document manifest"):
        rd.load_generated_documents_manifest(manifest_path)
    assert rd.main(["--check"]) == 2
    assert rd.main(["--apply"]) == 2
    assert external_manifest.read_text(encoding="utf-8") == external_content


def test_manifest_path_outside_papers_is_rejected_before_reading(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """The optional manifest argument cannot widen the renderer's ownership root."""
    _write_paper_fixture(tmp_path, monkeypatch)
    external_manifest = tmp_path / "external-manifest.json"
    external_manifest.write_text('{"version": 1, "documents": []}\n', encoding="utf-8")

    with pytest.raises(ValueError, match="must be contained"):
        rd.load_generated_documents_manifest(external_manifest)
    assert rd.main(["--check", "--manifest", str(external_manifest)]) == 2


def test_symlinked_paper_folder_is_rejected_before_rendering(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """A folder link cannot make rendering create documents outside papers/."""
    _papers, folder, _ = _write_paper_fixture(tmp_path, monkeypatch)
    external_folder = tmp_path / "external-paper-folder"
    folder.rename(external_folder)
    folder.symlink_to(external_folder, target_is_directory=True)

    with pytest.raises(ValueError, match="symlinked paper folder"):
        rd.paper_folders()
    assert rd.main(["--check"]) == 2
    assert rd.main(["--apply"]) == 2
    assert not any((external_folder / filename).exists() for filename in rd.DOCUMENT_FILENAMES)


def test_symlinked_papers_root_is_rejected_before_metadata_loading(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """The consolidated metadata loader cannot follow a redirected papers root."""
    papers, _folder, _ = _write_paper_fixture(tmp_path, monkeypatch)
    external_papers = tmp_path / "external-papers"
    papers.rename(external_papers)
    papers.symlink_to(external_papers, target_is_directory=True)

    with pytest.raises(ValueError, match="symlinked papers root"):
        rd.load_metadata()
    assert rd.main(["--check"]) == 2
    assert rd.main(["--apply"]) == 2


def test_symlinked_folder_metadata_is_rejected_before_reading(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """Folder metadata must remain a real file within its real paper folder."""
    _papers, folder, _ = _write_paper_fixture(tmp_path, monkeypatch)
    external_metadata = tmp_path / "external-metadata.json"
    external_metadata.write_text('{"name": "External metadata"}\n', encoding="utf-8")
    (folder / "metadata.json").symlink_to(external_metadata)

    with pytest.raises(ValueError, match="symlinked folder metadata"):
        rd.resolved_metadata("2026_Example", rd.load_metadata())
    assert rd.main(["--check"]) == 2
    assert rd.main(["--apply"]) == 2


def test_symlinked_manifest_owned_target_fails_plan_check_and_apply(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """A managed target link is rejected and cannot overwrite its external referent."""
    papers, folder, _ = _write_paper_fixture(tmp_path, monkeypatch)
    assert rd.main(["--apply"]) == 0

    target = folder / "README.md"
    external_target = tmp_path / "external-readme.md"
    external_content = "outside the paper-document ownership boundary\n"
    external_target.write_text(external_content, encoding="utf-8")
    target.unlink()
    target.symlink_to(external_target)

    metadata = rd.load_metadata()
    bibliography = rd.parse_bibliography()
    folders = rd.paper_folders()
    manifest_entries = rd.load_generated_documents_manifest()
    metadata_by_folder = {name: rd.resolved_metadata(name, metadata) for name in folders}
    with pytest.raises(ValueError, match="symlinked managed document"):
        rd.plan_document_changes(
            folders,
            metadata_by_folder,
            bibliography,
            manifest_entries,
            adopt_existing=False,
        )

    assert rd.main(["--check"]) == 2
    assert rd.main(["--apply"]) == 2
    assert external_target.read_text(encoding="utf-8") == external_content


def test_hard_linked_manifest_owned_target_cannot_overwrite_external_alias(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """Link-count validation runs before an apply-mode target is truncated."""
    _papers, folder, _ = _write_paper_fixture(tmp_path, monkeypatch)
    assert rd.main(["--apply"]) == 0

    target = folder / "README.md"
    external_target = tmp_path / "external-readme.md"
    target.rename(external_target)
    os.link(external_target, target)
    external_content = "outside the paper-document ownership boundary via hard link\n"
    external_target.write_text(external_content, encoding="utf-8")

    with pytest.raises(ValueError, match="hard-linked managed document"):
        rd.plan_document_changes(
            ["2026_Example"],
            {"2026_Example": rd.resolved_metadata("2026_Example", rd.load_metadata())},
            rd.parse_bibliography(),
            rd.load_generated_documents_manifest(),
            adopt_existing=False,
        )
    assert rd.main(["--check"]) == 2
    assert rd.main(["--apply"]) == 2
    assert external_target.read_text(encoding="utf-8") == external_content


def test_hard_linked_manifest_cannot_overwrite_external_alias(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    """The manifest gets the same pre-truncation link-count defense as documents."""
    papers, _folder, _ = _write_paper_fixture(tmp_path, monkeypatch)
    assert rd.main(["--apply"]) == 0

    manifest_path = papers / rd.MANIFEST_FILENAME
    external_manifest = tmp_path / "external-manifest.json"
    manifest_path.rename(external_manifest)
    os.link(external_manifest, manifest_path)
    external_content = external_manifest.read_text(encoding="utf-8")

    with pytest.raises(ValueError, match="hard-linked generated-document manifest"):
        rd.load_generated_documents_manifest()
    assert rd.main(["--check"]) == 2
    assert rd.main(["--apply"]) == 2
    assert external_manifest.read_text(encoding="utf-8") == external_content


def test_unlisted_hand_authored_document_is_never_overwritten(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    papers, folder, _ = _write_paper_fixture(tmp_path, monkeypatch)
    hand_authored = "# Curated README\n\nThis document is intentionally hand-authored.\n"
    readme_path = folder / "README.md"
    readme_path.write_text(hand_authored, encoding="utf-8")

    assert rd.main(["--apply", "--force"]) == 0
    assert readme_path.read_text(encoding="utf-8") == hand_authored
    manifest = json.loads((papers / rd.MANIFEST_FILENAME).read_text(encoding="utf-8"))
    managed_paths = {entry["path"] for entry in manifest["documents"]}
    assert "2026_Example/README.md" not in managed_paths
    assert managed_paths == {"2026_Example/AGENTS.md", "2026_Example/SKILL.md"}
    assert rd.main(["--check"]) == 0

    # A marker is not sufficient ownership by itself: a marker without the
    # explicit manifest record is a configuration error, not permission to
    # overwrite a previously hand-authored file.
    readme_path.write_text(rd.wrap_generated_document("README.md", "# Orphaned marker"), encoding="utf-8")
    assert rd.main(["--check"]) == 1


def test_explicit_adoption_requires_manifest_opt_in(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    papers, folder, _ = _write_paper_fixture(tmp_path, monkeypatch)
    readme_path = folder / "README.md"
    original = "# Previously reviewed content\n"
    readme_path.write_text(original, encoding="utf-8")
    (papers / rd.MANIFEST_FILENAME).write_text(
        json.dumps(
            {
                "version": rd.MANIFEST_VERSION,
                "documents": [{"path": "2026_Example/README.md", "adopt": True}],
            }
        ),
        encoding="utf-8",
    )

    assert rd.main(["--apply"]) == 1
    assert readme_path.read_text(encoding="utf-8") == original
    assert rd.main(["--adopt-existing", "--apply"]) == 0
    assert readme_path.read_text(encoding="utf-8").startswith(rd.generated_document_marker("README.md"))
    manifest = json.loads((papers / rd.MANIFEST_FILENAME).read_text(encoding="utf-8"))
    adopted = next(item for item in manifest["documents"] if item["path"] == "2026_Example/README.md")
    assert adopted == {"path": "2026_Example/README.md"}


def test_doi_audit_treats_artifact_doi_as_informational_only(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    _, _, _ = _write_paper_fixture(
        tmp_path,
        monkeypatch,
        metadata_doi=ARTIFACT_DOI,
        artifact_doi=CANONICAL_DOI,
    )

    assert rd.main(["--doi-audit"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["canonical_source"] == "pages/BIBLIOGRAPHY.md"
    assert report["canonical_field"] == "doi"
    assert report["artifact_field"] == "artifact_doi"
    assert report["summary"]["conflicts"] == 1
    assert report["conflicts"] == [
        {
            "artifact_doi": CANONICAL_DOI,
            "bibliography_doi": CANONICAL_DOI,
            "code": "canonical_doi_mismatch",
            "folder": "2026_Example",
            "metadata_doi": ARTIFACT_DOI,
        }
    ]


def test_bibliography_doi_is_rendered_as_canonical_while_artifact_is_labeled(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
):
    _, _, _ = _write_paper_fixture(
        tmp_path,
        monkeypatch,
        metadata_doi=CANONICAL_DOI,
        artifact_doi=ARTIFACT_DOI,
    )
    bibliography = rd.parse_bibliography()
    meta = rd.resolved_metadata("2026_Example", rd.load_metadata())

    readme = rd.generate_readme("2026_Example", meta, bibliography["2026_Example"])
    skill = rd.generate_skill("2026_Example", meta, ["2026_Example"], bibliography["2026_Example"])

    assert f"DOI: {CANONICAL_DOI}." in readme
    assert f"DOI: {ARTIFACT_DOI}." not in readme
    assert f"- Artifact DOI: [{ARTIFACT_DOI}]" in readme
    assert f'doi: "{CANONICAL_DOI}"' in skill
    assert f'artifact_doi: "{ARTIFACT_DOI}"' in skill
    assert f"- Canonical DOI: {CANONICAL_DOI}" in skill
    assert f"- Artifact DOI: {ARTIFACT_DOI}" in skill
