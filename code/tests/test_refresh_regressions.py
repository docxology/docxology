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
