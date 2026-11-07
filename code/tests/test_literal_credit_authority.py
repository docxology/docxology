"""Preserve reviewed published credit labels at citation interfaces."""

from copy import deepcopy
from dataclasses import replace
import hashlib
import json
import subprocess

import pytest

from docxology_tools import author_entities
import export_bibliography as export
import generate_citation_cff as cff
import fetch_work_authors as fetch

KEY = "CreditedFixture001"
TITLE = "Synthetic credited program book"
DOI = "10.5281/zenodo.101"
LABELS = [
    "Active Inference Institute",
    "Friedman, Daniel and Other",
    "Dan Corva, Kevin Backhouse",
]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


@pytest.fixture
def credited(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    folder = root / "papers/2026_CreditedFixture"
    folder.mkdir(parents=True)
    (root / "data").mkdir()
    (root / "pages").mkdir()
    creators = [{"name": name, "affiliation": None} for name in LABELS]
    sidecar = {
        "registry_observation": {
            "record_id": "102",
            "doi": "10.5281/zenodo.102",
            "conceptdoi": DOI,
            "title": TITLE,
            "version": "3.2.0",
            "creators": creators,
        },
        "document_observation": {"credit_labels": list(LABELS)},
    }
    source = folder / "source_evidence.json"
    source.write_text(json.dumps(sidecar, indent=2) + "\n")
    review = {
        "schema_version": 1,
        "source": "papers/2026_CreditedFixture/source_evidence.json",
        "source_sha256": sha(source.read_bytes()),
        "record_id": "102",
        "version": "3.2.0",
        "creators_sha256": sha(
            json.dumps(
                creators, sort_keys=True, separators=(",", ":"), ensure_ascii=False
            ).encode()
        ),
        "reviewed_by": "Synthetic source curator",
        "reviewed_at": "2026-01-01T12:00:00+00:00",
        "reason": "Retain published composite credits without inferred people.",
    }
    authors = [
        {"literal": LABELS[0], "entity_type": "Organization"},
        {"literal": LABELS[1], "entity_type": "Unspecified"},
        {"literal": LABELS[2], "entity_type": "Unspecified"},
    ]
    record = {
        "num": 1,
        "title": TITLE,
        "doi": DOI,
        "status": "verified",
        "resolved_title": TITLE,
        "registration_agency": "DataCite",
        "authors": authors,
        "literal_credit_review": review,
        "registry_baseline": {"creators": creators, "title": TITLE},
    }
    registry = {"schema_version": "1.0", "works": {KEY: record}}
    (root / "data/work-authors.json").write_text(json.dumps(registry, indent=2) + "\n")
    (root / "data/work-identifiers.json").write_text(
        json.dumps(
            {
                "schema_version": "WorkIdentifierRegistry.v1",
                "identifiers": {"1": {"citation_key": KEY, "status": "active"}},
            }
        )
    )
    (root / "pages/BIBLIOGRAPHY.md").write_text(
        "| # | Year | Domain | Type | Title | Venue | Link | Docs | Authors |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
        f"| 1 | 2026 | 🎥 | Book | {TITLE} | Zenodo | [{DOI}](https://doi.org/{DOI}) | "
        "[📁](../papers/2026_CreditedFixture/) | " + "; ".join(LABELS) + " |\n"
    )
    for args in (
        ("init", "-q"),
        ("add", "."),
        (
            "-c",
            "user.name=Synthetic Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "core.hooksPath=/dev/null",
            "commit",
            "-qm",
            "Synthetic citation fixture",
        ),
    ):
        subprocess.run(
            ["git", *args],
            cwd=root,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            check=True,
            timeout=15,
        )
    monkeypatch.setattr(export, "REPO_ROOT", root)
    work = export.Work(
        num=1,
        citation_key=KEY,
        year=2026,
        domain="🎥",
        domain_name="Media",
        type="Book",
        title=TITLE,
        venue="Zenodo",
        url="https://doi.org/" + DOI,
        doi=DOI,
        docs_path="papers/2026_CreditedFixture",
        has_paper_folder=True,
        authors=list(LABELS),
    )
    return root, work, registry


def test_reviewed_credit_exports_remain_complete_literal_units(credited):
    root, work, registry = credited
    outputs = export.render_outputs([work], generated_at="2026-01-01T00:00:00Z")
    citation = json.loads(outputs[root / "bibliography.csl.json"])[0]
    assert citation["author"] == [
        {"literal": "Active Inference Institute"},
        {"literal": "Friedman, Daniel and Other"},
        {"literal": "Dan Corva, Kevin Backhouse"},
    ]
    assert (
        "author = {{Active Inference Institute} and {Friedman, Daniel and Other} "
        "and {Dan Corva, Kevin Backhouse}}"
    ) in outputs[root / "bibliography.bib"]
    assert (
        json.loads(outputs[root / "data/works.json"])["works"][0]["authors"] == LABELS
    )


def test_ordinary_person_name_export_keeps_existing_api(credited):
    _, work, _ = credited
    ordinary = replace(work, authors=["Lovelace, Ada"])
    assert export.csl_item(ordinary)["author"] == [
        {"family": "Lovelace", "given": "Ada"}
    ]


def test_unspecified_credit_precedes_principal_and_comma_heuristics():
    principal = {"@id": "https://example.invalid/person", "@type": "Person"}
    for label in LABELS[1:]:
        assert author_entities.author_entity(label, principal, "Unspecified") == {
            "name": label
        }
    assert author_entities.author_entity(
        "Example Collective", principal, "Organization"
    ) == {"@type": "Organization", "name": "Example Collective"}


def test_source_bound_types_include_unspecified(credited):
    root, work, _ = credited
    records = author_entities.load_author_records(root)
    assert author_entities.verified_author_types(work.__dict__, records) == {
        LABELS[0]: "Organization",
        LABELS[1]: "Unspecified",
        LABELS[2]: "Unspecified",
    }


@pytest.mark.parametrize(
    "mutation",
    [
        "source_hash",
        "record",
        "version",
        "creators_hash",
        "reviewer",
        "review_time",
        "document_credits",
        "unknown_entity",
    ],
)
def test_invalid_declared_literal_authority_refuses(credited, mutation):
    root, _, registry = credited
    entry = registry["works"][KEY]
    review = entry["literal_credit_review"]
    if mutation == "source_hash":
        review["source_sha256"] = "0" * 64
    elif mutation == "record":
        review["record_id"] = "999"
    elif mutation == "version":
        review["version"] = "other"
    elif mutation == "creators_hash":
        review["creators_sha256"] = "0" * 64
    elif mutation == "reviewer":
        review["reviewed_by"] = ""
    elif mutation == "review_time":
        review["reviewed_at"] = "2026-01-01"
    elif mutation == "unknown_entity":
        entry["authors"][1]["entity_type"] = "Person"
    else:
        p = root / review["source"]
        doc = json.loads(p.read_text())
        doc["document_observation"]["credit_labels"] = list(reversed(LABELS))
        p.write_text(json.dumps(doc))
        review["source_sha256"] = sha(p.read_bytes())
    (root / "data/work-authors.json").write_text(json.dumps(registry))
    with pytest.raises(ValueError):
        author_entities.load_author_records(root)


@pytest.mark.parametrize(
    "changes",
    [
        {"doi": "10.5281/zenodo.999"},
        {"num": 2},
        {"num": True},
        {"title": "Different title"},
        {"authors": list(reversed(LABELS))},
    ],
)
def test_literal_authority_requires_current_work_identity_and_order(credited, changes):
    _, work, _ = credited
    with pytest.raises(ValueError):
        export.render_outputs([replace(work, **changes)])


def test_cff_public_reconciliation_preserves_reviewed_literal_units(credited):
    root, _, _ = credited
    citation = cff.bibliography_citations(root / "pages/BIBLIOGRAPHY.md")[
        "2026_CreditedFixture"
    ]
    old = 'cff-version: 1.2.0\ntitle: "Old"\nauthors:\n  - name: "Old"\n'
    text = cff.reconcile_cff_bibliography(old, citation)
    assert all('  - name: "' + label + '"' in text for label in LABELS)
    assert "family-names:" not in text
    assert "orcid:" not in text
    assert cff.reconcile_cff_bibliography(text, citation) == text


def run_refresh(root, work, monkeypatch, observation):
    monkeypatch.setattr(fetch, "REPO_ROOT", root)
    monkeypatch.setattr(fetch, "OUTPUT", root / "data/work-authors.json")
    monkeypatch.setattr(fetch, "BIBLIOGRAPHY", root / "pages/BIBLIOGRAPHY.md")
    monkeypatch.setattr(fetch, "REQUEST_PAUSE_SECONDS", 0)
    monkeypatch.setattr(fetch, "load_works", lambda: [work.__dict__])
    monkeypatch.setattr(
        fetch, "resolve", lambda doi, title, **kwargs: deepcopy(observation)
    )
    monkeypatch.setattr("sys.argv", ["fetch_work_authors.py"])
    return fetch.main()


@pytest.mark.parametrize("changed", [False, True])
def test_refresh_preserves_literal_review_without_new_attestation(
    credited, monkeypatch, changed
):
    root, work, registry = credited
    old = deepcopy(registry["works"][KEY])
    observation = {
        "status": "verified",
        "resolved_title": TITLE,
        "authors": [{"literal": label} for label in LABELS],
        "source_creator_names": list(LABELS),
    }
    if changed:
        observation["authors"][-1] = {"literal": "Changed credit"}
        observation["source_creator_names"][-1] = "Changed credit"
    result = run_refresh(root, work, monkeypatch, observation)
    selected = json.loads((root / "data/work-authors.json").read_text())["works"][KEY]
    assert selected["authors"] == old["authors"]
    assert selected["literal_credit_review"] == old["literal_credit_review"]
    assert selected["registry_baseline"] == old["registry_baseline"]
    assert selected["registry_refresh"]["status"] == (
        "registry_drift" if changed else "matches_frozen_byline"
    )
    assert result == (1 if changed else 0)


def test_invalid_source_refresh_refuses_before_overwriting_saved_registry(
    credited, monkeypatch
):
    root, work, registry = credited
    registry["works"][KEY]["literal_credit_review"]["source_sha256"] = "0" * 64
    path = root / "data/work-authors.json"
    path.write_text(json.dumps(registry))
    before = path.read_bytes()
    result = run_refresh(
        root,
        work,
        monkeypatch,
        {
            "status": "verified",
            "resolved_title": TITLE,
            "authors": [{"literal": label} for label in LABELS],
        },
    )
    assert result == 1
    assert path.read_bytes() == before


def test_reviewed_datacite_refresh_observes_raw_labels_without_person_inference(
    monkeypatch,
):
    raw = {
        "data": {
            "attributes": {
                "titles": [{"title": TITLE}],
                "creators": [{"name": label} for label in LABELS],
            }
        }
    }
    monkeypatch.setattr(fetch, "_get", lambda url: (200, json.dumps(raw)))
    observation = fetch.fetch_datacite(DOI, preserve_creator_labels=True)
    assert observation["source_creator_names"] == LABELS
    assert "source_creator_names" not in fetch.fetch_datacite(DOI)


def test_entity_projection_refuses_mismatched_current_doi(credited):
    root, work, _ = credited
    records = author_entities.load_author_records(root)
    with pytest.raises(ValueError):
        author_entities.verified_author_types(
            replace(work, doi="10.5281/zenodo.999").__dict__, records
        )


def test_generated_paper_documents_preserve_reviewed_credit_labels(credited):
    import regenerate_docs as docs

    root, _, _ = credited
    paths = docs.DocumentPaths(
        papers_dir=root / "papers", bibliography_path=root / "pages/BIBLIOGRAPHY.md"
    )
    citation = docs.parse_bibliography(paths=paths)["2026_CreditedFixture"]
    rendered = docs.generate_readme(
        "2026_CreditedFixture",
        {"abstract": "A synthetic program."},
        citation,
        paths=paths,
    )
    assert "; ".join(LABELS) in rendered
    assert "Kevin Backhouse Dan Corva" not in rendered
    assert docs.work_authors({}, {"authors": ["Lovelace, Ada"]}) == "Ada Lovelace"


def test_work_page_byline_and_citation_metadata_preserve_literal_credits(
    credited, monkeypatch
):
    import build_work_pages as pages

    root, work, _ = credited
    monkeypatch.setattr(pages, "REPO_ROOT", root)
    value = dict(work.__dict__)
    value["_author_types"] = author_entities.verified_author_types(
        value, author_entities.load_author_records(root)
    )
    byline = pages.byline_html(value)
    assert all(label in byline for label in LABELS)
    head = pages.page_head(value)
    assert all(
        'name="citation_author" content="' + label + '"' in head for label in LABELS
    )
    assert "Kevin Backhouse Dan Corva" not in byline + head


@pytest.mark.parametrize(
    "tamper",
    [
        "doi",
        "num",
        "labels",
        "missing_labels",
        "null",
        "list",
        "missing_time",
        "naive_time",
        "false_status",
    ],
)
def test_saved_literal_registry_refresh_is_rederived_not_trusted(
    credited, monkeypatch, tamper
):
    root, work, _ = credited
    observation = {
        "status": "verified",
        "resolved_title": TITLE,
        "authors": [{"literal": label} for label in LABELS],
        "source_creator_names": list(LABELS),
    }
    assert run_refresh(root, work, monkeypatch, observation) == 0
    payload = json.loads((root / "data/work-authors.json").read_text())
    refresh = payload["works"][KEY]["registry_refresh"]
    if tamper == "doi":
        refresh["observation"]["doi"] = "10.5281/zenodo.999"
    elif tamper == "num":
        refresh["observation"]["num"] = 999
    elif tamper == "labels":
        refresh["observation"]["source_creator_names"] = list(reversed(LABELS))
    elif tamper == "missing_labels":
        refresh["observation"].pop("source_creator_names")
    elif tamper == "null":
        payload["works"][KEY]["registry_refresh"] = None
    elif tamper == "list":
        payload["works"][KEY]["registry_refresh"] = []
    elif tamper == "missing_time":
        refresh.pop("checked_at")
    elif tamper == "naive_time":
        refresh["checked_at"] = "2026-01-01"
    else:
        refresh["status"] = "registry_drift"
    assert fetch.document_evidence_errors(payload)
