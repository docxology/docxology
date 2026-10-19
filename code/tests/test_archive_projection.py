"""Projection omissions require exact archived bytes and no local consumers."""

import hashlib
import json
import subprocess
from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401
from docxology_tools.archive_projection import declared_archives, verified_archives  # noqa: E402


@pytest.fixture
def archive(tmp_path):
    def git(*args):
        return subprocess.check_output(["git", *args], cwd=tmp_path, text=True).strip()

    git("init", "-q")
    name = "papers/2022_Transcript/source.docx"
    file = tmp_path / name
    file.parent.mkdir(parents=True)
    file.write_bytes(b"archived-office-source")
    git("add", ".")
    git(
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.org",
        "-c",
        "commit.gpgsign=false",
        "commit",
        "-qm",
        "archive",
    )
    entry = {
        "path": name,
        "commit": git("rev-parse", "HEAD"),
        "bytes": file.stat().st_size,
        "sha256": hashlib.sha256(file.read_bytes()).hexdigest(),
        "reason": "Fixture",
        "reviewed_by": "Fixture",
    }
    registry = tmp_path / "data/pages-archive-documents.json"
    registry.parent.mkdir()
    registry.write_text(json.dumps({"schema_version": "1.0", "entries": [entry]}))
    return tmp_path, name, file, entry, registry


def test_original_bytes_remain_and_pinned_downloads_are_allowed(archive):
    root, name, file, entry, _registry = archive
    declaration = declared_archives(root)[name]
    (root / "index.html").write_text(
        f'<a href="{declaration["url"]}">Original source</a>'
    )
    assert verified_archives(root)[name]["commit"] == entry["commit"]
    assert file.read_bytes() == b"archived-office-source"


@pytest.mark.parametrize(
    "reference",
    [
        '<a href="papers/2022_Transcript/source.docx">Source</a>',
        "[Source](source.docx)",
        "https://example.org/?next=https://github.com/docxology/docxology/blob/REV/papers/2022_Transcript/source.docx",
    ],
)
def test_current_local_or_nested_archive_references_protect_asset(archive, reference):
    root, _name, _file, entry, _registry = archive
    (root / "index.html").write_text(reference.replace("REV", entry["commit"]))
    with pytest.raises(ValueError, match="reference"):
        verified_archives(root)


def test_modified_source_is_not_silently_omitted(archive):
    root, _name, file, _entry, _registry = archive
    file.write_bytes(b"unreviewed source edit")
    with pytest.raises(ValueError, match="source bytes changed"):
        verified_archives(root)


def test_review_hash_cannot_substitute_different_committed_bytes(archive):
    root, _name, file, entry, registry = archive
    file.write_bytes(b"different-office-data!")
    entry.update(
        bytes=file.stat().st_size, sha256=hashlib.sha256(file.read_bytes()).hexdigest()
    )
    registry.write_text(json.dumps({"schema_version": "1.0", "entries": [entry]}))
    with pytest.raises(ValueError, match="object"):
        verified_archives(root)


@pytest.mark.parametrize(
    "path",
    [
        "papers/2022_Transcript/source.pdf",
        "papers/2022_Transcript/../source.docx",
        "resume/source.docx",
    ],
)
def test_policy_cannot_remove_pdfs_or_escape_supporting_document_scope(archive, path):
    root, _name, _file, entry, registry = archive
    entry["path"] = path
    registry.write_text(json.dumps({"schema_version": "1.0", "entries": [entry]}))
    with pytest.raises(ValueError, match="invalid"):
        declared_archives(root)


def test_unreadable_public_reference_source_stops_omission(archive, monkeypatch):
    from docxology_tools import generated_outputs

    root, _name, _file, _entry, _registry = archive
    page = root / "index.html"
    page.write_text("page")
    original = generated_outputs.read_generated_output_text

    def read(base, path, *args, **kwargs):
        if path == page:
            raise PermissionError("unavailable")
        return original(base, path, *args, **kwargs)

    monkeypatch.setattr(generated_outputs, "read_generated_output_text", read)
    with pytest.raises(PermissionError):
        verified_archives(root)


@pytest.mark.parametrize(
    "surface", ["reports/current.html", "code/current.js", "assets/current.svg"]
)
@pytest.mark.parametrize(
    "reference",
    ["source%2Edocx", "source&#46;docx", "source%252Edocx", r"source\u002edocx"],
)
def test_encoded_references_on_public_surfaces_protect_source(
    archive, surface, reference
):
    root, _name, _file, _entry, _registry = archive
    page = root / surface
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text(f'<a href="../papers/2022_Transcript/{reference}">Source</a>')
    with pytest.raises(ValueError, match="reference"):
        verified_archives(root)


def test_manifest_reuses_one_complete_proof_but_rechecks_each_operation(archive, monkeypatch):
    import build_pages_artifact as bpa
    root, name, _file, _entry, _registry = archive
    monkeypatch.setattr(bpa, "REPO_ROOT", root)
    monkeypatch.setattr(bpa, "ARTIFACT_MANIFEST", root / "data/pages-artifact-manifest.json")
    monkeypatch.setattr(bpa, "GROWTH_REPORT", root / "reports/pages_artifact_growth_2026-10-19.json")
    safe_source = bpa.source_path
    monkeypatch.setattr(bpa, "source_path", lambda relative: safe_source(relative, repo_root=root))
    calls = []
    original = bpa.verified_archives
    def verify(base):
        calls.append(base)
        return original(base)
    monkeypatch.setattr(bpa, "verified_archives", verify)
    first = bpa._manifest_payload()
    assert calls == [root]
    assert first["omitted_source_documents"]["archives"][0]["path"] == name
    assert first["omitted_source_documents"]["count"] == 1
    (root / "index.html").write_text(f'<a href="{name}">Source</a>')
    with pytest.raises(ValueError, match="reference"):
        bpa._manifest_payload()
    assert calls == [root, root]


@pytest.fixture
def assembly_archive(archive, monkeypatch):
    import build_pages_artifact as bpa

    root, name, _file, _entry, _registry = archive
    monkeypatch.setattr(bpa, "REPO_ROOT", root)
    monkeypatch.setattr(bpa, "ARTIFACT_MANIFEST", root / "data/pages-artifact-manifest.json")
    monkeypatch.setattr(bpa, "GROWTH_REPORT", root / "reports/pages_artifact_growth_2026-10-19.json")
    safe_source = bpa.source_path
    monkeypatch.setattr(bpa, "source_path", lambda relative: safe_source(relative, repo_root=root))
    bpa._referenced_report_paths.cache_clear()
    (root / "index.html").write_text(f'<a href="{declared_archives(root)[name]["url"]}">Archive</a>')
    (root / "papers/2022_Transcript/source.pdf").write_bytes(b"%PDF-retained-fixture")
    (root / "papers/2022_Transcript/unreviewed.docx").write_bytes(b"unreviewed-kept")
    subprocess.run(["git", "add", "."], cwd=root, check=True)
    subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.org",
                    "-c", "commit.gpgsign=false", "commit", "-qm", "projection inputs"], cwd=root, check=True)
    yield bpa, root, name
    bpa._referenced_report_paths.cache_clear()


def test_assembled_files_and_bytes_match_projection_with_reviewed_office_source(assembly_archive, tmp_path):
    bpa, root, name = assembly_archive
    output = tmp_path / "assembled"
    expected_paths = {path.as_posix() for path in bpa._relative_paths()}
    expected_size = bpa.projected_size()
    manifest = bpa._manifest_payload(include_pending_growth=False)
    expected_manifest_paths = {item["path"] for item in manifest["included_files"] + manifest["control_files"]}
    copied, size, omitted = bpa.assemble(output)
    actual = {path.relative_to(output).as_posix() for path in output.rglob("*") if path.is_file()}
    assert actual == expected_paths == expected_manifest_paths
    assert (copied, size) == expected_size
    assert size == sum(path.stat().st_size for path in output.rglob("*") if path.is_file())
    assert name in omitted and not (output / name).exists()
    assert (root / name).read_bytes() == b"archived-office-source"
    assert (output / "papers/2022_Transcript/source.pdf").read_bytes() == b"%PDF-retained-fixture"
    assert (output / "papers/2022_Transcript/unreviewed.docx").read_bytes() == b"unreviewed-kept"


def test_assembly_rechecks_archive_proof_before_replacing_existing_output(assembly_archive, tmp_path):
    bpa, root, name = assembly_archive
    output = tmp_path / "assembled"
    output.mkdir()
    sentinel = output / "prior-build.txt"
    sentinel.write_text("preserve previous build")
    (root / "index.html").write_text(f'<a href="{name}">Local source</a>')
    with pytest.raises(ValueError, match="reference"):
        bpa.assemble(output)
    assert sentinel.read_text() == "preserve previous build"
