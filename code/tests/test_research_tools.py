"""Source identities, exact citation subsets and numerical model oracles."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.research_connections import graph_catalog, related_catalog  # noqa: E402
from docxology_tools.generated_outputs import (  # noqa: E402
    stale_output_paths,
    write_output_texts,
    UnsafeGeneratedOutputPathError,
)
import build_research_tools as builder  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    "route", ["collections", "trails", "research-map", "lab", "publications"]
)
def test_exploration_pages_follow_the_site_static_accessibility_contract(route):
    from accessibility_audit import audit_page

    result = audit_page(ROOT / (route + ".html"))
    assert result["ok"], {
        name: passed for name, passed in result["checks"].items() if not passed
    }


def work(key, domain="A", **extras):
    return {
        "citation_key": key,
        "title": key,
        "year": 2026,
        "domain": domain,
        "domain_name": domain,
        "authors": [],
        **extras,
    }


def test_specific_cross_domain_evidence_outranks_recent_domain_only_match():
    works = [
        work("Target"),
        work("Newest", year=2030),
        work("Specific", "B", year=2020),
        work("Unrelated", "C"),
    ]
    enrichment = {
        key: {"keywords": ["Bayesian modeling"]} for key in ("Target", "Specific")
    }
    ranked = related_catalog(works, enrichment, {})["Target"]
    assert [w["citation_key"] for w in ranked] == ["Specific", "Newest"]
    assert ranked[0]["reasons"] == ["Recorded topic: Bayesian modeling"]
    assert "domain" in ranked[1]["reasons"][0]
    assert not related_catalog([work("Lone")], {}, {})["Lone"]


@pytest.mark.parametrize(
    "left,right,label,reverse",
    [
        ("author", "author", "Coauthor: Shared Person", "Coauthor: Shared Person"),
        (
            "editor",
            "editor",
            "Shared editor: Shared Person",
            "Shared editor: Shared Person",
        ),
        (
            "editor",
            "author",
            "Shared contributor: Shared Person (editor of this work; author of related work)",
            "Shared contributor: Shared Person (author of this work; editor of related work)",
        ),
        (
            "author",
            "editor",
            "Shared contributor: Shared Person (author of this work; editor of related work)",
            "Shared contributor: Shared Person (editor of this work; author of related work)",
        ),
    ],
)
def test_related_contributor_explanations_preserve_roles_in_both_directions(
    left, right, label, reverse
):
    works = [
        work("A", "X", authors=["Shared Person"], contributor_role=left),
        work("B", "Y", authors=["Shared Person"], contributor_role=right),
    ]
    result = related_catalog(works, {}, {})
    assert result["A"][0]["reasons"] == [label]
    assert result["B"][0]["reasons"] == [reverse]
    if left == "editor" or right == "editor":
        assert not any(
            reason.startswith("Coauthor:")
            for rows in result.values()
            for item in rows
            for reason in item["reasons"]
        )


def test_substrings_and_generic_site_author_do_not_create_relationships():
    works = [work(str(i), str(i), authors=["Shared Profile Author"]) for i in range(6)]
    assert (
        related_catalog(
            works, {"0": {"keywords": ["ant"]}, "1": {"keywords": ["anticipation"]}}, {}
        )["0"]
        == []
    )


def test_recommendations_exclude_duplicate_dois_and_canonical_aliases():
    works = [
        work("A", doi="10.1/exact"),
        work("B", doi="10.1/exact"),
        work("Friedman2024CommentsSubmittedByBlockScience162"),
        work("Friedman2024CommentsNationalDigitalTwins033"),
    ]
    ranked = related_catalog(works, {}, {})
    assert "B" not in [w["citation_key"] for w in ranked["A"]]
    assert "Friedman2024CommentsNationalDigitalTwins033" not in [
        w["citation_key"]
        for w in ranked["Friedman2024CommentsSubmittedByBlockScience162"]
    ]


def test_graph_records_roles_exact_names_and_only_explicit_repository_edges():
    works = [
        work("A", authors=["One, Author"], docs_path="papers/2026_A/"),
        work("B", authors=["One, Author"], contributor_role="editor"),
        work("C", authors=["Author One"]),
    ]
    graph = graph_catalog(works, {"A": "https://github.com/example/repo"})
    nodes = {node["id"] for node in graph["nodes"]}
    assert all(
        edge["source"] in nodes and edge["target"] in nodes for edge in graph["edges"]
    )
    assert len([n for n in graph["nodes"] if n["kind"] == "person"]) == 2
    assert (
        len([e for e in graph["edges"] if e["relation"] == "Associated software"]) == 1
    )
    assert (
        next(e for e in graph["edges"] if e["relation"] == "Recorded editor")["source"]
        == "work:B"
    )
    assert not any("citation" in e["relation"].lower() for e in graph["edges"])


@pytest.mark.parametrize(
    "bad_step",
    [
        {"kind": "work", "ref": "Missing", "minutes": 20, "goal": "Read"},
        {"kind": "demo", "ref": "bayes", "minutes": True, "goal": "Read"},
        {
            "kind": "software",
            "ref": "javascript:alert(1)",
            "minutes": 20,
            "goal": "Read",
        },
        {"kind": "demo", "ref": "bayes", "minutes": 0, "goal": "Read"},
    ],
)
def test_trail_rejects_unknown_resources_and_invalid_estimates(bad_step):
    source = {
        "schema_version": 1,
        "trails": [
            {
                "id": "valid",
                "title": "Trail",
                "summary": "Summary",
                "prerequisites": "None",
                "steps": [bad_step],
            }
        ],
    }
    with pytest.raises(ValueError):
        builder.resolve_trails(source, [], [], [])


def test_generated_catalog_preserves_citation_identity_roles_and_order():
    catalog = json.loads((ROOT / "data/collection-catalog.json").read_text())["works"]
    works = json.loads((ROOT / "data/works.json").read_text())["works"]
    csl = json.loads((ROOT / "bibliography.csl.json").read_text())
    assert [w["key"] for w in catalog] == [w["citation_key"] for w in works]
    assert [w["csl"] for w in catalog] == csl
    assert (
        "\n\n".join(w["ris"] for w in catalog) + "\n"
        == (ROOT / "bibliography.ris").read_text()
    )
    original = builder.load_bibtex_entries()
    assert all(w["bib"] == original[w["key"]] for w in catalog)


def node(script: str) -> str:
    result = subprocess.run(
        ["node", "-e", script], cwd=ROOT, text=True, capture_output=True, check=False
    )
    assert result.returncode == 0, result.stdout + result.stderr
    return result.stdout


def test_collection_models_fail_closed_and_exports_are_ordered_exact_subsets():
    node(r"""
const assert = require('node:assert/strict');
const c = require('./js/collections.js');
for (const bad of [null, [], {version:2,lists:[]}, {version:1,active:'x',lists:[{id:'x',title:'X',keys:['A','A']}]}]) assert.throws(()=>c.validateStore(bad));
for (const bad of ['#v=2&title=X&works=A','#v=1&title=X&works=../secret','#v=1&title=X&works=A&works=B','#v=1&title=X&works=A,A']) assert.throws(()=>c.parseShare(bad));
const list={id:'one',title:'A <literal> title',keys:['B','A']};
assert.deepEqual(c.parseShare(new URL(c.shareURL(list,'https://example.com')).hash).keys,['B','A']);
const catalog=new Map([['A',{title:'A',year:2026,url:'/works/A.html',bib:'@article{A,\n}',ris:'TY  - JOUR\nTI  - A\nER  -',csl:{id:'A'}}],['B',{title:'B',year:2025,url:'/works/B.html',bib:'@book{B,\n}',ris:'TY  - BOOK\nTI  - B\nER  -',csl:{id:'B'}}]]);
assert.equal(c.exportList(list,catalog,'bib'),'@book{B,\n}\n\n@article{A,\n}\n');
assert.deepEqual(JSON.parse(c.exportList(list,catalog,'csl')),[{id:'B'},{id:'A'}]);
assert.match(c.exportList(list,catalog,'md'),/1\. \[B\]/);
assert.throws(()=>c.exportList({...list,keys:['Missing']},catalog,'bib'));
assert.throws(()=>c.exportList(list,catalog,'invented'));
""")


def test_binary_update_against_closed_form_and_impossible_evidence():
    node(r"""
const assert=require('node:assert/strict');
const {binaryHistory:b}=require('./js/probability-lab.js');
assert.ok(Math.abs(b(.2,.8,.2,[true]).at(-1).posterior-.5)<1e-14);
assert.ok(Math.abs(b(.2,.8,.2,[true,false]).at(-1).posterior-.2)<1e-14);
assert.ok(Math.abs(b(.2,.8,.2,Array(5).fill(true)).at(-1).posterior-256/257)<1e-14);
assert.equal(b(0,.8,.2,[true]).at(-1).posterior,0);
assert.equal(b(1,.8,.2,[true]).at(-1).posterior,1);
assert.equal(b(.7,.5,.5,Array(100).fill(true)).at(-1).posterior.toFixed(12),'0.700000000000');
for(const args of [[NaN,.8,.2,[]],[.5,2,.2,[]],[.5,0,0,[true]],[0,.8,0,[true]],[.5,.8,.2,Array(101).fill(true)]]) assert.throws(()=>b(...args));
""")


def test_seeded_urn_fixed_sequence_and_conservation_oracles():
    node(r"""
const assert=require('node:assert/strict');
const {urnHistory:u}=require('./js/probability-lab.js');
const fixed=u(2,3,0,10,42);
assert.deepEqual(fixed.slice(1).map(r=>r.color),['blue','blue','blue','blue','amber','blue','amber','blue','blue','blue']);
assert.ok(fixed.every(r=>r.amber===2&&r.blue===3&&r.fraction===.4));
for(const seed of [0,1,42,4294967295]) {
 const rows=u(2,3,4,200,seed); assert.deepEqual(rows,u(2,3,4,200,seed));
 assert.ok(rows.every((r,i)=>r.amber+r.blue===5+4*i&&r.fraction===r.amber/(r.amber+r.blue)));
}
assert.notDeepEqual(u(1,1,1,100,1),u(1,1,1,100,2));
for(const args of [[0,1,1,10,42],[1,1,-1,10,42],[1,1,1,201,42],[1,1,1,10,1.5],[1,1,1,10,4294967296]]) assert.throws(()=>u(...args));
""")


def test_generator_drift_and_symlink_negative_control(tmp_path):
    outputs = {
        tmp_path / "data/map.json": '{"nodes": []}\n',
        tmp_path / "map.html": "<!DOCTYPE html>expected\n",
    }
    write_output_texts(outputs, repo_root=tmp_path)
    assert not stale_output_paths(outputs, repo_root=tmp_path)
    (tmp_path / "data/map.json").write_text('{"nodes": ["tampered"]}\n')
    before = (tmp_path / "data/map.json").read_bytes()
    assert stale_output_paths(outputs, repo_root=tmp_path) == (
        tmp_path / "data/map.json",
    )
    assert (tmp_path / "data/map.json").read_bytes() == before
    (tmp_path / "map.html").unlink()
    (tmp_path / "map.html").symlink_to(tmp_path / "data/map.json")
    with pytest.raises(UnsafeGeneratedOutputPathError):
        write_output_texts(outputs, repo_root=tmp_path)
    assert (tmp_path / "data/map.json").read_bytes() == before
