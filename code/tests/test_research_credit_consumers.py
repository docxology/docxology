"""Tests-only proposal: reviewed credit units at research-desk consumers.

Requires the separately reviewed F5 source and test_literal_credit_authority.py.
No implementation, execution or RED/GREEN claim accompanies this file.
"""

from dataclasses import asdict
import json
from pathlib import Path
import sys
from urllib.parse import parse_qs, urlencode, urlsplit

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from test_literal_credit_authority import KEY, LABELS, credited as _credited  # noqa: E402
from docxology_tools.research_connections import graph_catalog  # noqa: E402
import build_research_tools as builder  # noqa: E402
import export_bibliography as export  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import copy_site, serve_site, stop_server  # noqa: E402


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


@pytest.fixture(scope="module")
def credit_site(tmp_path_factory):
    directory = copy_site(tmp_path_factory.mktemp("typed-credit-map"))
    html = builder.page(
        "research-map", "Research map", "Recorded metadata relationships",
        builder.map_content([]), "research-map.js",
    )
    base, server = serve_site(directory)
    try:
        yield base, html
    finally:
        stop_server(server)


@pytest.fixture(scope="module")
def credit_browser(browser_runtime):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            yield browser
        finally:
            browser.close()


@pytest.fixture
def credit_page(credit_site, credit_browser):
    base, html = credit_site
    context = credit_browser.new_context(
        viewport={"width": 1280, "height": 900}, service_workers="block"
    )
    context.route(
        "**/*",
        lambda route: route.continue_()
        if route.request.url.startswith(base + "/") else route.abort(),
    )
    page = context.new_page()
    page.route(
        "**/research-map.html*",
        lambda route: route.fulfill(status=200, content_type="text/html", body=html),
    )
    try:
        yield page, base
    finally:
        context.close()


def graph_payload(kinds, *, reverse=False):
    label = "Shared Exact Label"
    nodes = [
        {
            "id": kind + ":shared exact label", "kind": kind,
            "label": label, "url": "",
        }
        for kind in kinds
    ]
    if reverse:
        nodes.reverse()
    return {"schema_version": 1, "nodes": nodes, "edges": []}


def supply_graph(page, payload):
    page.route(
        "**/data/research-map.json*",
        lambda route: route.fulfill(
            status=200, content_type="application/json", body=json.dumps(payload)
        ),
    )


@pytest.mark.browser
@pytest.mark.parametrize(
    "kind,display", [("organization", "organization"), ("contributor", "contributor label")]
)
def test_map_typed_filter_summary_aria_and_saved_url_agree(credit_page, kind, display):
    page, base = credit_page
    supply_graph(page, graph_payload(["person", "organization", "contributor"]))
    wanted = kind + ":shared exact label"
    page.goto(base + "/research-map.html?" + urlencode({"node": wanted, "kind": kind}))
    page.locator("#map-app:not([disabled])").wait_for(state="visible")
    assert page.locator("#map-kind").input_value() == kind
    assert page.locator("#map-node").input_value() == wanted
    assert page.locator("#map-node option").all_text_contents() == [
        display + " — Shared Exact Label"
    ]
    assert page.locator("#map-summary").inner_text().startswith(display + " ·")
    assert page.locator("#research-map-svg a").get_attribute("aria-label") == (
        "Explore " + display + ": Shared Exact Label"
    )
    page.reload()
    page.locator("#map-app:not([disabled])").wait_for(state="visible")
    assert page.locator("#map-node").input_value() == wanted


@pytest.mark.browser
def test_exact_legacy_person_id_wins_over_other_typed_candidates(credit_page):
    page, base = credit_page
    supply_graph(page, graph_payload(["organization", "person", "contributor"]))
    wanted = "person:shared exact label"
    page.goto(base + "/research-map.html?" + urlencode({"node": wanted, "kind": "person"}))
    page.locator("#map-app:not([disabled])").wait_for(state="visible")
    assert page.locator("#map-node").input_value() == wanted
    assert page.locator("#map-summary").inner_text().startswith("person ·")


@pytest.mark.browser
@pytest.mark.parametrize("kind", ["organization", "contributor"])
@pytest.mark.parametrize("old_filter", [None, "person"])
def test_missing_legacy_person_link_resolves_only_a_single_typed_label(
    credit_page, kind, old_filter
):
    page, base = credit_page
    supply_graph(page, graph_payload([kind]))
    params = {"node": "person:shared exact label"}
    if old_filter:
        params["kind"] = old_filter
    page.goto(base + "/research-map.html?" + urlencode(params))
    page.locator("#map-app:not([disabled])").wait_for(state="visible")
    assert page.locator("#map-node").input_value() == kind + ":shared exact label"
    assert page.locator("#map-kind").input_value() == (kind if old_filter else "all")
    assert "Unknown" not in page.locator("#map-status").inner_text()
    assert "Ambiguous" not in page.locator("#map-status").inner_text()


@pytest.mark.browser
@pytest.mark.parametrize("reverse", [False, True])
def test_missing_legacy_person_link_refuses_ambiguous_typed_labels(credit_page, reverse):
    page, base = credit_page
    supply_graph(page, graph_payload(["organization", "contributor"], reverse=reverse))
    page.goto(
        base + "/research-map.html?"
        + urlencode({"node": "person:shared exact label", "kind": "person"})
    )
    page.locator("#map-app:not([disabled])").wait_for(state="visible")
    assert page.locator("#map-node").input_value() == ""
    assert "Ambiguous" in page.locator("#map-status").inner_text()
    assert page.locator("#research-map-svg circle").count() == 0
    assert set(page.locator("#map-node option").evaluate_all(
        "(nodes) => nodes.map(node => node.value)"
    )) == {
        "organization:shared exact label",
        "contributor:shared exact label",
    }
    selected = "organization:shared exact label"
    page.locator("#map-node").select_option(selected)
    assert page.locator("#map-node").input_value() == selected
    assert page.locator("#map-summary").inner_text().startswith("organization ·")
    assert "Ambiguous" not in page.locator("#map-status").inner_text()
    assert parse_qs(urlsplit(page.url).query)["node"] == [selected]
    page.go_back()
    page.wait_for_function(
        "() => document.querySelector('#map-status').textContent.includes('Ambiguous')"
    )
    assert page.locator("#map-node").input_value() == ""
    page.go_forward()
    page.wait_for_function(
        "id => document.querySelector('#map-node').value === id", arg=selected
    )
    assert page.locator("#map-summary").inner_text().startswith("organization ·")
    assert "Ambiguous" not in page.locator("#map-status").inner_text()


@pytest.mark.browser
def test_map_unknown_node_kind_still_fails_closed(credit_page):
    page, base = credit_page
    supply_graph(page, graph_payload(["invented"]))
    page.goto(base + "/research-map.html")
    page.wait_for_function(
        "() => document.querySelector('#map-status').textContent.includes('unavailable')"
    )
    assert page.locator("#map-app").get_attribute("disabled") is not None
    assert page.locator("#map-search").is_disabled()
    assert page.locator("#map-node").is_disabled()


@pytest.mark.browser
def test_map_script_and_graph_request_share_a_new_cache_token(credit_page):
    page, base = credit_page
    supply_graph(page, graph_payload(["person"]))
    requests = []
    page.on("request", lambda request: requests.append(request.url))
    page.goto(base + "/research-map.html")
    page.locator("#map-app:not([disabled])").wait_for(state="visible")
    script_url = page.locator('script[src*="/js/research-map.js"]').get_attribute("src")
    script_version = parse_qs(urlsplit(script_url).query)["v"]
    graph_urls = [url for url in requests if urlsplit(url).path == "/data/research-map.json"]
    assert len(graph_urls) == 1
    assert script_version != ["1"]
    assert parse_qs(urlsplit(graph_urls[0]).query)["v"] == script_version
