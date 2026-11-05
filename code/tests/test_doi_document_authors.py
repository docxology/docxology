"""A reviewed PDF byline can differ from its frozen DOI creator order."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import sys

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401
import fetch_work_authors as authors  # noqa: E402

KEY = "Friedman2026ExampleWork999"
DOI = "10.5281/zenodo.1000"


@pytest.fixture
def doi_document(tmp_path, monkeypatch):
    folder = tmp_path / "papers/2026_Example"
    folder.mkdir(parents=True)
    source = folder / "full_text.md"
    source.write_text("Example work\nWritten by Ada Example and Zoe Other\n", encoding="utf-8")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    registry = {"record_id": "1001", "doi": "10.5281/zenodo.1001", "conceptdoi": DOI,
                "title": "Example work", "publication_date": "2026-01-01", "version": "1.0",
                "creators": [{"name": "Other, Zoe"}, {"name": "Example, Ada"}],
                "record_json_sha256": "c" * 64}
    document = {"release": "1.0", "date": "2026-01-01",
                "byline": ["Example, Ada", "Other, Zoe"], "note": "PDF and deposit author order differ."}
    evidence = {"schema_version": "1.0",
                "source_pdf": {"record_id": "1001", "concept_doi": DOI, "name": "paper.pdf", "sha256": "b" * 64},
                "extraction": {"file": "full_text.md", "sha256": digest, "source_pdf_sha256": "b" * 64},
                "registry_observation": registry, "document_observation": document}
    sidecar = folder / "source_evidence.json"
    sidecar.write_text(json.dumps(evidence), encoding="utf-8")
    bibliography = tmp_path / "pages/BIBLIOGRAPHY.md"
    bibliography.parent.mkdir()
    bibliography.write_text(
        "| # | Year | Domain | Type | Title | Venue | Link | Docs | Authors |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        f"| 999 | 2026 | 💻 | Paper | Example work | Zenodo | https://doi.org/{DOI} | "
        "[docs](../papers/2026_Example/) | — |\n", encoding="utf-8"
    )
    output = tmp_path / "data/work-authors.json"
    output.parent.mkdir()
    (output.parent / "work-identifiers.json").write_text(json.dumps({
        "schema_version": "WorkIdentifierRegistry.v1",
        "identifiers": {"999": {"citation_key": KEY, "status": "active"}},
    }), encoding="utf-8")
    entry = {
        "num": 999, "doi": DOI, "title": "Example work", "status": "doi_document_verified",
        "authors": [{"family": "Example", "given": "Ada"}, {"family": "Other", "given": "Zoe"}],
        "source": "papers/2026_Example/full_text.md", "source_sha256": digest,
        "source_pdf_sha256": "b" * 64, "evidence": "Written by Ada Example and Zoe Other",
        "source_evidence": "papers/2026_Example/source_evidence.json",
        "source_evidence_sha256": hashlib.sha256(sidecar.read_bytes()).hexdigest(),
        "source_record_id": "1001", "registry_baseline": copy.deepcopy(registry),
        "document_baseline": copy.deepcopy(document), "source_authority": "deposited_pdf_title_page",
        "review": {"reviewed_at": "2026-01-02T00:00:00Z", "reviewed_by": "Named byline reviewer",
                   "reason": "Use deposited title-page order; retain different raw registry order."},
    }
    payload = {"works": {KEY: entry}}
    output.write_text(json.dumps(payload), encoding="utf-8")
    monkeypatch.setattr(authors, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(authors, "BIBLIOGRAPHY", bibliography)
    monkeypatch.setattr(authors, "OUTPUT", output)
    return tmp_path, source, sidecar, bibliography, output, payload


def test_doi_document_byline_is_valid_and_applies_pdf_order(doi_document):
    _, _, _, bibliography, _, payload = doi_document
    assert authors.document_evidence_errors(payload) == []
    assert authors.apply_to_bibliography() == 0
    assert "| Example, Ada; Other, Zoe |" in bibliography.read_text()


@pytest.mark.parametrize("failure", (
    "text-sha", "sidecar-sha", "pdf-sha", "doi", "num", "title", "folder", "quote", "record-id",
    "registry-creators", "document-order", "missing-review", "future-review", "source-symlink",
))
def test_doi_document_authority_rejects_unbound_evidence(doi_document, failure, tmp_path):
    _, source, sidecar, _, output, payload = doi_document
    entry = payload["works"][KEY]
    if failure == "text-sha":
        entry["source_sha256"] = "d" * 64
    elif failure == "sidecar-sha":
        entry["source_evidence_sha256"] = "d" * 64
    elif failure == "pdf-sha":
        entry["source_pdf_sha256"] = "d" * 64
    elif failure == "doi":
        entry["doi"] = "10.5281/zenodo.2000"
    elif failure == "num":
        entry["num"] = 998
    elif failure == "title":
        entry["title"] = "Another work"
    elif failure == "folder":
        other = tmp_path / "papers/2026_Other"
        other.mkdir()
        (other / "full_text.md").write_bytes(source.read_bytes())
        entry["source"] = "papers/2026_Other/full_text.md"
    elif failure == "quote":
        entry["evidence"] = "Written by someone unlisted"
    elif failure == "record-id":
        entry["source_record_id"] = "1002"
    elif failure == "registry-creators":
        entry["registry_baseline"]["creators"].reverse()
    elif failure == "document-order":
        entry["authors"].reverse()
    elif failure == "missing-review":
        entry.pop("review")
    elif failure == "future-review":
        entry["review"]["reviewed_at"] = "2099-01-01T00:00:00Z"
    else:
        external = tmp_path / "external.md"
        external.write_bytes(source.read_bytes())
        source.unlink()
        source.symlink_to(external)
    assert authors.document_evidence_errors(payload)
    output.write_text(json.dumps(payload), encoding="utf-8")
    before = doi_document[3].read_bytes()
    assert authors.apply_to_bibliography() == 1
    assert doi_document[3].read_bytes() == before


def _refresh(doi_document, monkeypatch, result):
    _, _, _, _, output, _ = doi_document
    monkeypatch.setattr(authors, "load_works", lambda: [{"num": 999, "doi": DOI, "title": "Example work", "citation_key": KEY}])
    monkeypatch.setattr(authors, "resolve", lambda doi, title: copy.deepcopy(result))
    monkeypatch.setattr(authors.time, "sleep", lambda _: None)
    monkeypatch.setattr(sys, "argv", ["fetch_work_authors"])
    code = authors.main()
    return code, json.loads(output.read_text())["works"][KEY]


def test_registry_refresh_preserves_valid_reviewed_document_order_and_frozen_baselines(doi_document, monkeypatch):
    original = copy.deepcopy(doi_document[-1]["works"][KEY])
    result = {"status": "verified", "resolved_title": "Example work", "registration_agency": "DataCite",
              "authors": [{"family": "Other", "given": "Zoe"}, {"family": "Example", "given": "Ada"}]}
    code, kept = _refresh(doi_document, monkeypatch, result)
    assert code == 0
    assert kept["status"] == "doi_document_verified"
    for field in ("authors", "review", "source_sha256", "source_evidence_sha256", "registry_baseline", "document_baseline"):
        assert kept[field] == original[field]
    assert kept["registry_refresh"]["status"] == "matches_frozen_byline"


@pytest.mark.parametrize("result", [
    {"status": "verified", "resolved_title": "Example work", "authors": [{"family": "Unreviewed", "given": "Author"}]},
    {"status": "doi_unresolved"},
])
def test_changed_or_unavailable_registry_is_reported_without_overwriting_pdf_byline(doi_document, monkeypatch, result):
    original = copy.deepcopy(doi_document[-1]["works"][KEY])
    code, kept = _refresh(doi_document, monkeypatch, result)
    assert code == 1
    assert kept["authors"] == original["authors"]
    assert kept["registry_baseline"] == original["registry_baseline"]
    assert kept["registry_refresh"]["status"] in {"registry_drift", "registry_unavailable"}


def test_invalid_document_binding_aborts_refresh_before_saved_authors_are_overwritten(doi_document, monkeypatch):
    _, source, _, _, output, _ = doi_document
    source.write_text("Changed extraction", encoding="utf-8")
    before = output.read_bytes()
    result = {"status": "verified", "resolved_title": "Example work", "authors": [{"family": "Registry", "given": "Order"}]}
    code, _ = _refresh(doi_document, monkeypatch, result)
    assert code == 1
    assert output.read_bytes() == before


@pytest.mark.parametrize("field,value", (("doi", "10.5281/zenodo.2000"), ("num", 998)))
def test_saved_registry_comparison_requires_the_same_doi_and_work_number(doi_document, monkeypatch, field, value):
    result = {"status": "verified", "resolved_title": "Example work",
              "authors": [{"family": "Other", "given": "Zoe"}, {"family": "Example", "given": "Ada"}]}
    code, kept = _refresh(doi_document, monkeypatch, result)
    assert code == 0
    kept["registry_refresh"]["observation"][field] = value
    assert authors.document_evidence_errors({"works": {KEY: kept}})


@pytest.mark.parametrize("invalid_num", (True, 1.0, "1"))
def test_registry_comparison_requires_integer_work_identity_not_equal_coercions(doi_document, invalid_num):
    entry = copy.deepcopy(doi_document[-1]["works"][KEY])
    entry["num"] = 1
    observation = {"num": 1, "doi": DOI.upper(), "status": "verified", "resolved_title": "Example work",
                   "authors": [{"family": "Other", "given": "Zoe"}, {"family": "Example", "given": "Ada"}]}
    assert authors._registry_refresh_state(entry, observation) == "matches_frozen_byline"
    observation["num"] = invalid_num
    assert authors._registry_refresh_state(entry, observation) == "registry_drift"
