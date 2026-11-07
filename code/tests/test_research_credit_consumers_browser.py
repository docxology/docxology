"""Exercise reviewed credit types through the research map in Chromium."""

import json
from pathlib import Path
import sys
from urllib.parse import parse_qs, urlencode, urlsplit

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

import docxology_tools  # noqa: E402, F401  (canonical import bootstrap)
import build_research_tools as builder  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import copy_site, serve_site, stop_server  # noqa: E402

pytestmark = pytest.mark.browser


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


def test_exact_legacy_person_id_wins_over_other_typed_candidates(credit_page):
    page, base = credit_page
    supply_graph(page, graph_payload(["organization", "person", "contributor"]))
    wanted = "person:shared exact label"
    page.goto(base + "/research-map.html?" + urlencode({"node": wanted, "kind": "person"}))
    page.locator("#map-app:not([disabled])").wait_for(state="visible")
    assert page.locator("#map-node").input_value() == wanted
    assert page.locator("#map-summary").inner_text().startswith("person ·")


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
