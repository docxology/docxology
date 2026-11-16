"""Regression coverage for metadata and direct command execution."""
import importlib.util
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlsplit

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
from docxology_tools.bibliography_links import canonical_link_url  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]

@pytest.mark.parametrize("suffix", ["", ".", ",", ";", ":", "!", "?"])
def test_doi_prose_punctuation(suffix):
    doi = "10.5281/zenodo.24069474"
    assert canonical_link_url(doi + suffix, "Zenodo") == "https://doi.org/" + doi
    assert canonical_link_url("https://doi.org/" + doi + suffix, "Zenodo") == "https://doi.org/" + doi

def test_internal_doi_punctuation():
    doi = "10.1000/a;b:c"
    assert canonical_link_url(doi, "") == "https://doi.org/" + doi

def test_cjk_is_not_emoji():
    spec = importlib.util.spec_from_file_location("audit_metadata", ROOT / "code/audit_metadata.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert not module.has_emoji("中文 日本語 한국어")
    assert module.has_emoji("Research 🔬")

def test_indexnow_direct_execution_from_other_cwd(tmp_path):
    result = subprocess.run([sys.executable, str(ROOT / "code/orchestrators/indexnow_urls.py")], cwd=tmp_path, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    parsed = [urlsplit(line.strip()) for line in result.stdout.splitlines() if line.strip()]
    assert any((url.scheme, url.netloc, url.path) == ("https", "danielarifriedman.com", "/") for url in parsed)


def test_prior_deposit_is_catalogued_without_adopting_related_citations(tmp_path):
    from check_zenodo_uncatalogued import bibliography_doi_set

    pages = tmp_path / "pages"
    pages.mkdir()
    (pages / "BIBLIOGRAPHY.md").write_text(
        "| 1 | 2026 | 💻 | Paper | Sample | Zenodo | "
        "[Citation DOI](https://doi.org/10.5281/zenodo.2) · "
        "[Prior deposit](https://doi.org/10.5281/zenodo.1) · "
        "[Related publication](https://doi.org/10.5281/zenodo.3) | — | A |\n"
    )
    assert bibliography_doi_set(tmp_path) == {"10.5281/zenodo.1", "10.5281/zenodo.2"}


def test_release_backed_date_requires_the_exact_release_identity():
    from docxology_tools.citation_metadata import publication_date

    url = "https://github.com/example/project/releases/tag/v1.0.0"
    work = {"year": 2026, "doi": "", "url": url}
    metadata = {"doi": "", "publication_date": "2026-11-15", "github_release_url": url}
    assert publication_date(work, metadata) == "2026-11-15"
    metadata["github_release_url"] = url + "-other"
    assert publication_date(work, metadata) == "2026"


@pytest.mark.parametrize("following", ["; second citation", ": explanatory note", "."])
def test_doi_prose_delimiters(following):
    doi = "10.5281/zenodo.24069474"
    assert canonical_link_url(doi + following, "Zenodo") == "https://doi.org/" + doi


@pytest.mark.parametrize("repository", ["example/project", "https://github.com/example/project", "https://github.com/example/project/"])
def test_citation_repository_normalization(repository):
    from generate_citation_cff import _repository_code
    assert _repository_code({"github_repo": repository}) == "https://github.com/example/project"


def test_no_nested_github_scheme_in_citations():
    import re
    for path in (ROOT / "papers").glob("*/CITATION.cff"):
        assert re.search(r"github[.]com/https?://", path.read_text()) is None, path


def test_private_related_links_are_removed_without_mutating_observation():
    from docxology_tools.public_repository_links import project_pairing_report
    public = "docxology/public-research"
    private = "https://github.com/docxology/unlisted-research"
    raw = {"related_identifiers": [{"identifier": private}, {"identifier": "https://github.com/" + public}], "description": "Source " + private, "source_observations": {"captured_at": "2026-11-16"}}
    projected = project_pairing_report(raw, frozenset({public}))
    assert raw["related_identifiers"][0]["identifier"] == private
    assert projected["related_identifiers"] == [{"identifier": "https://github.com/" + public}]
    assert projected["description"] == "Source [non-public repository]"
    assert "source_observations" not in projected
    assert projected["public_link_projection"]["upstream_source_observations"] == raw["source_observations"]


def test_shipped_sources_introduce_no_nonpublic_owned_repository_urls():
    from docxology_tools.public_repository_links import URL_RX, owned_repository, public_repositories
    # Historical public references stay only in their original published paths.
    # This is not a public-visibility declaration or permission for new intake.
    baseline = subprocess.run(["git", "grep", "-I", "-o", "-E", r"https?://(www\.)?github\.com/docxology/[A-Za-z0-9_.-]+", "c2523b1c51f6e506031ceb5b90a890956337ec7c", "--", "papers", "data", "pages", "reports", "*.html"], cwd=ROOT, stdin=subprocess.DEVNULL, capture_output=True, text=True, check=True)
    historical = set()
    for line in baseline.stdout.splitlines():
        _, path, url = line.split(":", 2)
        historical.add((path, owned_repository(url)))
    names = subprocess.check_output(["git", "ls-files", "-z", "--", "papers", "data", "pages", "reports", "*.html"], cwd=ROOT, stdin=subprocess.DEVNULL).decode().split("\0")
    allowed = public_repositories(ROOT)
    failures = set()
    for name in names:
        path = ROOT / name
        if not name or path.suffix.casefold() not in {".md", ".json", ".html", ".cff", ".txt", ".xml", ".bib", ".ris"} or not path.is_file():
            continue
        for match in URL_RX.finditer(path.read_text(errors="replace")):
            repository = owned_repository(match.group())
            if repository and repository not in allowed and (name, repository) not in historical:
                failures.add(name)
    assert not failures, sorted(failures)



def test_source_sidecar_projection_is_idempotent_and_preserves_frozen_source(tmp_path):
    import json
    from docxology_tools.public_repository_links import source_link_outputs
    (tmp_path / "data").mkdir()
    (tmp_path / "data/github-repositories.json").write_text(json.dumps({"repositories": [{"full_name": "docxology/public-research", "private": False}]}))
    paper = tmp_path / "papers/sample"
    paper.mkdir(parents=True)
    source = {"source_pdf": {"sha256": "a" * 64}, "registry_observation": {"creators": ["Observed byline"]}, "registry_refresh_test": {"related_identifiers": [{"identifier": "https://github.com/docxology/unlisted-research"}, {"identifier": "https://github.com/docxology/public-research"}]}}
    path = paper / "source_evidence.json"
    path.write_text(json.dumps(source))
    outputs = source_link_outputs(tmp_path)
    projected = json.loads(outputs[path])
    assert projected["source_pdf"] == source["source_pdf"]
    assert projected["registry_observation"] == source["registry_observation"]
    assert len(projected["registry_refresh_test"]["related_identifiers"]) == 1
    path.write_text(outputs[path])
    assert source_link_outputs(tmp_path) == {}


def test_pairing_report_writer_enforces_the_public_inventory(tmp_path, monkeypatch):
    import json
    import sync_paired_publications as pairing
    from docxology_tools.publication_pairing import ZenodoRecord
    (tmp_path / "data").mkdir()
    (tmp_path / "data/github-repositories.json").write_text(json.dumps({"repositories": [{"full_name": "docxology/public-research", "private": False}]}))
    monkeypatch.setattr(pairing, "REPO_ROOT", tmp_path)
    record = ZenodoRecord.from_api({"id": 12345, "doi": "10.5281/zenodo.12345", "metadata": {"title": "Test work", "related_identifiers": [{"identifier": "https://github.com/docxology/unlisted-research"}, {"identifier": "https://github.com/docxology/public-research"}]}})
    report = tmp_path / "report.json"
    pairing.write_report(report, owners=["docxology"], releases=[], records=[record], pairs=[], actions=[], warnings=[])
    saved = json.loads(report.read_text())
    assert saved["zenodo_records"][0]["related_identifiers"] == [{"identifier": "https://github.com/docxology/public-research"}]
    assert saved["public_link_projection"]["policy"] == "public-owned-repositories-v1"
