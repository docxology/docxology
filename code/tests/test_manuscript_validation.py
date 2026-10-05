"""Failure-boundary checks for read-only repository manuscript validation."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.manuscript_validation import validate_manuscript  # noqa: E402


@pytest.fixture
def manuscript(tmp_path):
    folder = tmp_path / "docs/manuscript"
    folder.mkdir(parents=True)
    config = {
        "paper": {"title": "An evidence map"},
        "authors": [{"name": "Public Example"}],
        "publication": {"github_repository": "docxology/docxology"},
        "metadata": {"license": "TBD", "language": "en"},
        "manuscript_dir": "docs/manuscript",
        "render": {"formats": {"html": True, "pdf": False}},
        "bibliography": {"references_path": "docs/manuscript/references.bib", "fail_on_missing": True, "fail_on_unused": False},
    }
    (folder / "config.yaml").write_text(yaml.safe_dump(config), encoding="utf-8")
    (folder / "00_abstract.md").write_text("# Abstract {#sec:abstract}\n\nA structural draft.\n", encoding="utf-8")
    (folder / "99_references.md").write_text("# References {#sec:references}\n\n[Source](references.bib).\n", encoding="utf-8")
    (folder / "references.bib").write_text("@comment{No literature claims.}\n", encoding="utf-8")
    return tmp_path


def test_valid_draft_does_not_imply_rendering_or_publication(manuscript):
    result = validate_manuscript(manuscript)
    assert result["source_valid"] is True
    assert result["configured_render_formats"] == ["html"]
    assert result["render_performed"] is False
    assert result["publication_readiness_assessed"] is False
    assert str(manuscript) not in json.dumps(result)


@pytest.mark.parametrize("replacement,expected", [
    ("# Abstract\n", "H1"),
    ("Preface\n# Abstract {#sec:abstract}\n", "H1"),
    ("# Abstract {#sec:abstract}\n# Extra {#sec:extra}\n", "H1"),
    ("# Abstract {#sec:abstract}\n{{WORK_COUNT}}\n", "generated-value token"),
    ("# Abstract {#sec:abstract}\n[@missing]\n", "unresolved citation"),
    ("# Abstract {#sec:references}\n", "duplicate label"),
    ("# Abstract {#sec:abstract}\nSee @fig:missing.\n", "unresolved cross-reference"),
    ("# Abstract {#sec:abstract}\n![A figure](../output/missing.svg){#fig:missing}\n", "missing local figure"),
    ("# Abstract {#sec:abstract}\n[Missing](missing.md)\n", "missing local link"),
    ("# Abstract {#sec:abstract}\n[Unsafe](javascript:alert)\n", "unsupported link scheme"),
    ("# Abstract {#sec:abstract}\n[Outside](../../../../private.md)\n", "escapes repository"),
    ("# Abstract {#sec:abstract}\n```text\n[@missing]\n", "unterminated"),
    ("# Abstract {#sec:abstract}\n[Bad](http://[invalid)\n", "malformed link URL"),
    ("# Abstract {#sec:abstract}\n[Bad](bad%00path)\n", "invalid local reference"),
    ("# Abstract {#sec:abstract}\n![Directory](.)\n", "regular file"),
    ("# Abstract {#sec:abstract}\n[Bad](https:///broken)\n", "external URL"),
    ("# Abstract {#sec:abstract}\n[Bad](https://example.com:not-a-port/)\n", "external URL"),
    ("# Abstract {#sec:abstract}\n[Bad](https://user:password@example.com/)\n", "external URL"),
    ("# Abstract {#sec:abstract}\n![Figure][missing]\n", "reference-style figure"),
    ("# Abstract {#sec:abstract}\n![Figure][missing]\n\n[missing]: missing.svg\n", "missing local figure"),
    ("# Abstract {#sec:abstract}\n![Figure]\n", "shortcut figure"),
])
def test_prose_failure_boundaries(manuscript, replacement, expected):
    (manuscript / "docs/manuscript/00_abstract.md").write_text(replacement, encoding="utf-8")
    result = validate_manuscript(manuscript)
    assert result["source_valid"] is False
    assert any(expected in error for error in result["errors"])


def test_code_examples_and_guides_are_not_manuscript_claims(manuscript):
    folder = manuscript / "docs/manuscript"
    (folder / "README.md").write_text("# Guide\n{{TOKEN}}\n[@missing]\n", encoding="utf-8")
    (folder / "preamble.md").write_text("# Preamble\n```latex\n\\usepackage{geometry}\n```\n", encoding="utf-8")
    with (folder / "00_abstract.md").open("a", encoding="utf-8") as handle:
        handle.write("\n```markdown\n# Example {#sec:references}\n[@missing] {{TOKEN}}\n```\n\n```mermaid\nflowchart LR\n A --> B\n```\n")
    assert validate_manuscript(manuscript)["source_valid"] is True


def test_real_citations_labels_and_figure_references(manuscript):
    folder = manuscript / "docs/manuscript"
    (folder / "references.bib").write_text("@article{evidence,\n title={An actual fixture entry}\n}\n", encoding="utf-8")
    (manuscript / "docs/output").mkdir()
    (manuscript / "docs/output/diagram.svg").write_text("<svg/>\n", encoding="utf-8")
    (folder / "00_abstract.md").write_text("# Abstract {#sec:abstract}\n\n[@evidence] See @sec:references and @fig:flow.\n![Flow](../output/diagram.svg){#fig:flow}\n", encoding="utf-8")
    result = validate_manuscript(manuscript)
    assert result["source_valid"] is True
    assert result["citation_count"] == 1


@pytest.mark.parametrize("key,value,expected", [
    ("manuscript_dir", "manuscript", "manuscript_dir"),
    ("manuscript_dir", "../private", "manuscript_dir"),
    ("manuscript_dir", "bad\0path", "manuscript_dir"),
    ("render", {"formats": {"html": "true"}}, "YAML boolean"),
    ("render", {"formats": {"invented": True}}, "unsupported render formats"),
    ("authors", [{"name": ""}], "named author"),
    ("paper", {"title": ""}, "non-empty string"),
    ("bibliography", {"references_path": "outside.bib", "fail_on_missing": False, "fail_on_unused": 0}, "references_path"),
    ("publication", {"github_repository": "private/example"}, "github_repository"),
])
def test_configuration_contracts(manuscript, key, value, expected):
    path = manuscript / "docs/manuscript/config.yaml"
    config = yaml.safe_load(path.read_text())
    config[key] = value
    path.write_text(yaml.safe_dump(config), encoding="utf-8")
    result = validate_manuscript(manuscript)
    assert result["source_valid"] is False
    assert any(expected in error for error in result["errors"])


@pytest.mark.parametrize("text", ["paper: one\npaper: two\n", "!!python/object/apply:os.system ['exit 0']", "- not\n- a mapping\n"])
def test_unsafe_duplicate_or_nonmapping_yaml_fails(manuscript, text):
    (manuscript / "docs/manuscript/config.yaml").write_text(text, encoding="utf-8")
    assert validate_manuscript(manuscript)["source_valid"] is False


def test_missing_required_sections_and_duplicate_bib_keys(manuscript):
    folder = manuscript / "docs/manuscript"
    (folder / "00_abstract.md").unlink()
    (folder / "references.bib").write_text("@article{same, title={One}}\n@book{same, title={Two}}\n", encoding="utf-8")
    errors = validate_manuscript(manuscript)["errors"]
    assert any("required section is missing" in error for error in errors)
    assert any("duplicate citation keys" in error for error in errors)


@pytest.mark.parametrize("text", [
    "@article{fixture,\n title={Never closed}\n",
    "@article{fixture, title={Closed}}\n}\n",
    "this is not BibTeX",
    "@article{missing-key}\n",
])
def test_bibliography_entry_delimiters_fail_closed(manuscript, text):
    (manuscript / "docs/manuscript/references.bib").write_text(text, encoding="utf-8")
    result = validate_manuscript(manuscript)
    assert result["source_valid"] is False
    assert any("references.bib" in error for error in result["errors"])
    assert result["bibliography_syntax_validated"] is False


def test_reference_and_shortcut_figures_resolve_without_rendering(manuscript):
    folder = manuscript / "docs/manuscript"
    (folder / "figure.svg").write_text("<svg/>\n", encoding="utf-8")
    (folder / "00_abstract.md").write_text(
        "# Abstract {#sec:abstract}\n\n![Flow][diagram]\n![diagram]\n\n[diagram]: figure.svg\n", encoding="utf-8",
    )
    assert validate_manuscript(manuscript)["source_valid"] is True


def test_main_supplement_and_back_matter_have_stable_order(manuscript):
    folder = manuscript / "docs/manuscript"
    (folder / "01_methods.md").write_text("# Methods {#sec:methods}\n", encoding="utf-8")
    (folder / "S01_evidence.md").write_text("# Evidence {#sec:evidence}\n", encoding="utf-8")
    result = validate_manuscript(manuscript)
    assert result["source_valid"] is True
    assert result["sections"] == ["00_abstract.md", "01_methods.md", "S01_evidence.md", "99_references.md"]
    (folder / "01_other.md").write_text("# Other {#sec:other}\n", encoding="utf-8")
    assert any("section-number" in error for error in validate_manuscript(manuscript)["errors"])


def test_symlink_source_is_rejected_without_reading_private_bytes(manuscript, tmp_path):
    source = manuscript / "docs/manuscript/00_abstract.md"
    source.unlink()
    private = tmp_path / "private.txt"
    private.write_text("DO NOT EXPOSE THIS CONTENT", encoding="utf-8")
    source.symlink_to(private)
    result = validate_manuscript(manuscript)
    assert result["source_valid"] is False
    assert "DO NOT EXPOSE" not in json.dumps(result)


def test_cli_is_read_only_and_json_exit_status_reflects_errors(manuscript):
    script = Path(__file__).resolve().parents[1] / "orchestrators/validate_manuscript.py"
    before = {p.relative_to(manuscript): p.read_bytes() for p in manuscript.rglob("*") if p.is_file()}
    result = subprocess.run([sys.executable, str(script), "--root", str(manuscript), "--json"], text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["source_valid"] is True
    after = {p.relative_to(manuscript): p.read_bytes() for p in manuscript.rglob("*") if p.is_file()}
    assert after == before
    (manuscript / "docs/manuscript/00_abstract.md").unlink()
    result = subprocess.run([sys.executable, str(script), "--root", str(manuscript), "--json"], text=True, capture_output=True, check=False)
    assert result.returncode == 1
    assert json.loads(result.stdout)["source_valid"] is False
