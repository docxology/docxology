"""Source custody and conservative name correction in the author intake tool."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

import docxology_tools  # noqa: E402,F401
import fetch_work_authors as authors  # noqa: E402
import pytest  # noqa: E402


@pytest.fixture
def document_case(tmp_path, monkeypatch):
    source = tmp_path / "papers" / "2026_Example" / "full_text.md"
    source.parent.mkdir(parents=True)
    source.write_text("Written by Ada Example", encoding="utf-8")
    bibliography = tmp_path / "pages" / "BIBLIOGRAPHY.md"
    bibliography.parent.mkdir()
    bibliography.write_text(
        "| # | Year | Domain | Type | Title | Venue | Link | Docs | Authors |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        "| 999 | 2026 | 💻 | Paper | Example work | Archive | — | "
        "[docs](../papers/2026_Example/) | — |\n",
        encoding="utf-8",
    )
    output = tmp_path / "data" / "work-authors.json"
    output.parent.mkdir()
    monkeypatch.setattr(authors, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(authors, "BIBLIOGRAPHY", bibliography)
    monkeypatch.setattr(authors, "OUTPUT", output)
    payload = {"works": {"Friedman2026ExampleWork999": {
        "num": 999,
        "doi": None,
        "title": "Example work",
        "status": "document_verified",
        "authors": [{"family": "Example", "given": "Ada"}],
        "source": "papers/2026_Example/full_text.md",
        "evidence": "Written by Ada Example",
    }}}
    return source, bibliography, output, payload


def _entry(payload):
    return payload["works"]["Friedman2026ExampleWork999"]


def test_document_evidence_accepts_the_matching_work(document_case):
    _, _, _, payload = document_case
    assert authors.document_evidence_errors(payload) == []


@pytest.mark.parametrize("source_path", [
    "papers/2026_Other/full_text.md",
    "papers/2026_Example/../2026_Other/full_text.md",
])
def test_document_evidence_rejects_another_work_with_the_same_quote(document_case, source_path):
    source, _, _, payload = document_case
    other = source.parent.parent / "2026_Other" / "full_text.md"
    other.parent.mkdir()
    other.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    _entry(payload)["source"] = source_path
    assert authors.document_evidence_errors(payload) == [
        "Friedman2026ExampleWork999: source must remain inside papers/2026_Example/"
    ]


def test_document_evidence_rejects_a_source_symlink_escaping_its_folder(document_case, tmp_path):
    source, _, _, payload = document_case
    other = tmp_path / "external.md"
    other.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    source.unlink()
    source.symlink_to(other)
    assert authors.document_evidence_errors(payload) == [
        "Friedman2026ExampleWork999: source must remain inside papers/2026_Example/"
    ]


def test_document_evidence_rejects_a_paper_folder_symlink(document_case, tmp_path):
    source, _, _, payload = document_case
    other = tmp_path / "external-folder"
    other.mkdir()
    (other / source.name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    source.unlink()
    source.parent.rmdir()
    source.parent.symlink_to(other, target_is_directory=True)
    assert authors.document_evidence_errors(payload) == [
        "Friedman2026ExampleWork999: source must remain inside papers/2026_Example/"
    ]


def test_document_evidence_rejects_an_absolute_source_path(document_case):
    source, _, _, payload = document_case
    _entry(payload)["source"] = str(source)
    assert authors.document_evidence_errors(payload) == [
        "Friedman2026ExampleWork999: source must remain inside papers/2026_Example/"
    ]


@pytest.mark.parametrize("doi_location", ["entry", "bibliography"])
def test_document_evidence_requires_both_current_work_and_record_to_be_doi_free(document_case, doi_location):
    _, bibliography, _, payload = document_case
    if doi_location == "entry":
        _entry(payload)["doi"] = "10.5281/zenodo.999"
    else:
        bibliography.write_text(
            bibliography.read_text(encoding="utf-8").replace("| — | [docs]", "| https://doi.org/10.5281/zenodo.999 | [docs]"),
            encoding="utf-8",
        )
    assert authors.document_evidence_errors(payload) == [
        "Friedman2026ExampleWork999: document_verified is only for works without a DOI"
    ]


def test_document_evidence_cannot_redirect_authors_to_another_row_number(document_case):
    _, _, _, payload = document_case
    _entry(payload)["num"] = 998
    assert authors.document_evidence_errors(payload) == [
        "Friedman2026ExampleWork999: must match a bibliography work with a paper folder and the same num"
    ]


def test_document_evidence_rejects_an_unknown_work_key(document_case):
    _, _, _, payload = document_case
    payload["works"]["unknown-work"] = payload["works"].pop("Friedman2026ExampleWork999")
    assert authors.document_evidence_errors(payload) == [
        "unknown-work: must match a bibliography work with a paper folder and the same num"
    ]


def test_document_apply_refuses_invalid_evidence_before_any_bibliography_write(document_case, capsys):
    _, bibliography, output, payload = document_case
    _entry(payload)["evidence"] = "Written by Somebody Else"
    output.write_text(json.dumps(payload), encoding="utf-8")
    before = bibliography.read_bytes()
    assert authors.apply_to_bibliography() == 1
    assert bibliography.read_bytes() == before
    assert "evidence quote not found" in capsys.readouterr().err


def test_document_apply_accepts_bound_valid_evidence(document_case):
    _, bibliography, output, payload = document_case
    output.write_text(json.dumps(payload), encoding="utf-8")
    assert authors.apply_to_bibliography() == 0
    assert "| Example, Ada |" in bibliography.read_text(encoding="utf-8")


def test_document_evidence_fails_closed_without_its_bibliography(document_case):
    _, bibliography, _, payload = document_case
    bibliography.unlink()
    errors = authors.document_evidence_errors(payload)
    assert len(errors) == 1
    assert errors[0].startswith("document_verified validation needs a readable bibliography:")


@pytest.mark.parametrize(("family", "orcid", "expected"), [
    ("Andrew Pashea", "0009-0004-4061-6296", "Pashea, Andrew"),
    ("Daniel A. Friedman", "0000-0001-6232-9096", "Friedman, Daniel A."),
    ("Daniel Ari Friedman", "0000-0001-6232-9096", "Friedman, Daniel Ari"),
    ("Evelyn C. Goh", "0000-0001-7182-3950", "Goh, Evelyn C."),
    ("Siddhant Shrivastava", "0000-0002-9688-4730", "Shrivastava, Siddhant"),
    ("Tucker Chambers", "0009-0008-3793-7872", "Chambers, Tucker"),
])
def test_audited_name_aliases_are_bound_to_their_orcid(family, orcid, expected):
    author = {"family": family, "given": "", "orcid": f"https://orcid.org/{orcid}"}
    before = copy.deepcopy(author)
    assert authors.format_author(author) == expected
    assert author == before
    author["orcid"] = "0000-0000-0000-0000"
    assert authors.format_author(author) == family


@pytest.mark.parametrize("family", ["de la Cruz", "Juan de la Cruz"])
def test_unknown_orcid_names_keep_compound_surnames_and_ambiguous_order(family):
    author = {"family": family, "given": "", "orcid": "0000-0000-0000-0000"}
    assert authors.format_author(author) == family
