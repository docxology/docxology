"""Regression coverage for metadata and direct command execution."""
import importlib.util
import subprocess
import sys
from pathlib import Path

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
    assert "https://danielarifriedman.com/" in result.stdout.splitlines()


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
