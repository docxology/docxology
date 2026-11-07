"""Exercise reviewed credit units in research data and graph construction."""

from dataclasses import asdict
import json
from pathlib import Path
import sys

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from test_literal_credit_authority import KEY, LABELS, credited as _credited  # noqa: E402
from docxology_tools.research_connections import graph_catalog  # noqa: E402
import build_research_tools as builder  # noqa: E402
import export_bibliography as export  # noqa: E402

credited = _credited


@pytest.fixture
def desk(credited, monkeypatch):
    root, work, registry = credited
    values = {
        "works.json": {"works": [asdict(work)]},
        "videos.json": {"videos": []},
        "software.json": {"repositories": []},
        "research-trails-source.json": {"schema_version": 1, "trails": []},
    }
    for name, payload in values.items():
        (root / "data" / name).write_text(json.dumps(payload) + "\n")
    original_bib = (
        "@book{" + KEY + ",\n"
        "  author = {{Active Inference Institute} and "
        "{Friedman, Daniel and Other} and {Dan Corva, Kevin Backhouse}}\n}\n"
    )
    monkeypatch.setattr(builder, "REPO_ROOT", root)
    monkeypatch.setattr(builder, "load_bibtex_entries", lambda: {KEY: original_bib})
    monkeypatch.setattr(builder, "source_paths", lambda root: {})
    monkeypatch.setattr(
        builder.PaperResources, "load", classmethod(lambda cls, *args: None)
    )
    monkeypatch.setattr(builder, "source_repository_url", lambda *args: "")
    # Isolate unrelated page-shell stamps; exercise real catalog/map rendering.
    monkeypatch.setattr(builder, "page", lambda slug, title, description, content, script: content)
    return root, work, registry, original_bib


def test_selected_csl_preserves_reviewed_literal_units_and_other_export_bytes(desk):
    root, work, _registry, original_bib = desk
    outputs = builder.render_outputs()
    row = json.loads(outputs[root / "data/collection-catalog.json"])["works"][0]
    assert row["csl"]["author"] == [{"literal": name} for name in LABELS]
    assert row["authors"] == LABELS
    assert row["bib"] == original_bib
    assert row["ris"] == export.ris_record(work)


def test_research_consumers_refuse_invalid_literal_authority_without_writes(
    desk, monkeypatch
):
    root, _work, registry, _original_bib = desk
    registry["works"][KEY]["literal_credit_review"]["source_sha256"] = "0" * 64
    (root / "data/work-authors.json").write_text(json.dumps(registry) + "\n")
    before = {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in root.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(root).parts
    }
    monkeypatch.setattr(sys, "argv", ["build_research_tools.py"])
    with pytest.raises(ValueError):
        builder.main()
    after = {
        p.relative_to(root).as_posix(): p.read_bytes()
        for p in root.rglob("*")
        if p.is_file() and ".git" not in p.relative_to(root).parts
    }
    assert after == before


def test_research_builder_passes_exact_per_work_credit_types_to_graph(desk):
    root, _work, _registry, _original_bib = desk
    graph = json.loads(builder.render_outputs()[root / "data/research-map.json"])
    by_id = {node["id"]: node for node in graph["nodes"]}
    assert by_id["organization:active inference institute"]["kind"] == "organization"
    assert by_id["contributor:friedman, daniel and other"]["label"] == LABELS[1]
    assert by_id["contributor:dan corva, kevin backhouse"]["label"] == LABELS[2]
    assert not any(node["kind"] == "person" for node in graph["nodes"])
    assert {
        edge["target"] for edge in graph["edges"]
        if edge["relation"] == "Recorded author"
    } == {
        "organization:active inference institute",
        "contributor:friedman, daniel and other",
        "contributor:dan corva, kevin backhouse",
    }


def graph_work(key, *, role="author"):
    return {
        "citation_key": key, "title": key, "year": 2026,
        "domain": "A", "domain_name": "A", "authors": ["Shared Exact Label"],
        "contributor_role": role,
    }


@pytest.mark.parametrize("reverse", [False, True])
def test_graph_separates_same_label_types_independent_of_work_order(reverse):
    works = [graph_work("P"), graph_work("O"), graph_work("C", role="editor")]
    types = {
        "P": {"Shared Exact Label": "Person"},
        "O": {"Shared Exact Label": "Organization"},
        "C": {"Shared Exact Label": "Unspecified"},
    }
    if reverse:
        works.reverse()
    graph = graph_catalog(works, {}, author_types=types)
    by_id = {node["id"]: node for node in graph["nodes"]}
    for prefix in ("person", "organization", "contributor"):
        node = by_id[prefix + ":shared exact label"]
        assert node == {
            "id": prefix + ":shared exact label", "kind": prefix,
            "label": "Shared Exact Label", "url": "",
        }
    targets = {
        edge["source"]: (edge["target"], edge["relation"])
        for edge in graph["edges"] if edge["relation"].startswith("Recorded ")
    }
    assert targets == {
        "work:P": ("person:shared exact label", "Recorded author"),
        "work:O": ("organization:shared exact label", "Recorded author"),
        "work:C": ("contributor:shared exact label", "Recorded editor"),
    }


def test_graph_default_api_preserves_existing_person_ids():
    works = [graph_work("Legacy")]
    default = graph_catalog(works, {})
    assert default["description"] == (
        "Catalog relationships, not a citation network or identity registry. "
        "Author nodes group exact normalized recorded names; homonyms may be "
        "grouped and name variants remain separate."
    )
    assert default == graph_catalog(works, {}, author_types={})
    assert default == graph_catalog(
        works, {}, author_types={"Legacy": {"Shared Exact Label": "Person"}}
    )
    assert any(
        node["id"] == "person:shared exact label" and node["kind"] == "person"
        for node in default["nodes"]
    )


def test_graph_rejects_an_unknown_explicit_type():
    with pytest.raises(ValueError):
        graph_catalog(
            [graph_work("W")], {},
            author_types={"W": {"Shared Exact Label": "InventedType"}},
        )
