"""Real-browser acceptance of the complete research exploration workflows."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
import sys
from urllib.parse import urlencode, urlparse, parse_qs

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import AXE_JS, REPO_ROOT, copy_site, serve_site, stop_server  # noqa: E402

pytestmark = pytest.mark.browser
CATALOG = json.loads((REPO_ROOT / "data/collection-catalog.json").read_text())["works"]
FIRST, SECOND = CATALOG[:2]


@pytest.fixture(scope="module")
def site(tmp_path_factory):
    directory = copy_site(tmp_path_factory.mktemp("research-tools"))
    shutil.copy2(AXE_JS, directory / "js/axe.min.js")
    base, server = serve_site(directory)
    yield base, directory
    stop_server(server)


@pytest.fixture(scope="module")
def browser(browser_runtime):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        instance = p.chromium.launch(headless=True)
        yield instance
        instance.close()


@pytest.fixture
def page(site, browser):
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    context.route(
        "**/*",
        lambda route: (
            route.continue_()
            if route.request.url.startswith(site[0])
            else route.abort()
        ),
    )
    page = context.new_page()
    yield page
    context.close()


def ready_collection(page, base, suffix=""):
    page.goto(base + "/collections.html" + suffix)
    page.locator("#collection-app:not([disabled])").wait_for(state="visible")


@pytest.mark.parametrize(
    ("path", "asset", "app", "control"),
    [
        ("collections.html", "collection-catalog.json", "collection-app", "collection-title"),
        ("research-map.html", "research-map.json", "map-app", "map-search"),
    ],
)
def test_catalog_loading_reserves_editor_layout(page, site, path, asset, app, control):
    from playwright.sync_api import expect

    pending = []
    page.route("**/data/" + asset + "*", lambda route: pending.append(route))
    page.goto(site[0] + "/" + path, wait_until="domcontentloaded")
    editor = page.locator("#" + app)
    expect(editor).to_be_visible()
    expect(editor).to_have_attribute("aria-busy", "true")
    expect(page.locator("#" + control)).to_be_disabled()
    before = page.locator("#" + control).bounding_box()
    assert pending, "The real catalog request must remain pending for this check"
    pending.pop().continue_()
    expect(editor).to_have_attribute("aria-busy", "false")
    expect(page.locator("#" + control)).to_be_enabled()
    after = page.locator("#" + control).bounding_box()
    assert before is not None and after is not None
    assert abs(before["y"] - after["y"]) < 1


def test_publication_filters_roundtrip_and_browser_history(page, site):
    base = site[0]
    query = urlencode(
        {
            "q": "pheromone",
            "domain": "🐜",
            "year": "2023",
            "type": "Paper",
            "sort": "title",
            "dir": "desc",
            "docs": "1",
        }
    )
    page.goto(base + "/publications.html?" + query)
    page.wait_for_function(
        "() => document.querySelector('#result-count').textContent.includes('shown')"
    )
    page.wait_for_function(
        "() => document.querySelector('#pub-search-status')?.hidden === true"
    )
    titles = page.locator("#pub-tbody .td-title").all_text_contents()
    assert len(titles) == 1 and "pheromone" in titles[0].lower()
    assert page.locator("#year-filter").input_value() == "2023"
    assert page.locator("#docs-filter").is_checked()
    assert (
        page.locator('[data-domain-filter="🐜"]').get_attribute("aria-pressed")
        == "true"
    )
    page.reload()
    page.wait_for_function(
        "() => document.querySelector('#result-count').textContent.includes('shown')"
    )
    assert page.locator("#pub-tbody .td-title").all_text_contents() == titles
    previous = page.url
    page.locator('[data-type-filter="Book"]').click()
    assert parse_qs(urlparse(page.url).query)["type"] == ["Book"]
    page.go_back()
    assert page.url == previous
    assert (
        page.locator('[data-type-filter="Paper"]').get_attribute("aria-pressed")
        == "true"
    )
    assert page.locator("#pub-tbody .td-title").all_text_contents() == titles
    page.locator("#pub-share").click()
    assert page.locator("#pub-share-url").input_value() == page.url


def test_collect_filtered_set_includes_the_entire_catalog_not_only_first_page(
    page, site
):
    page.goto(site[0] + "/publications.html")
    page.wait_for_function(
        "() => document.querySelector('#result-count').textContent.includes('shown')"
    )
    assert page.locator("#pub-tbody tr").count() == 50
    href = page.locator("#collect-results").get_attribute("href")
    shared = parse_qs(urlparse(href).fragment)
    assert len(shared["works"][0].split(",")) == len(CATALOG)
    page.goto(site[0] + href)
    page.locator("#collection-app:not([disabled])").wait_for(state="visible")
    assert page.locator("#collection-items > li").count() == len(CATALOG)
    assert page.locator("#collection-save-shared").is_visible()
    assert page.evaluate("localStorage.getItem('docxology.reading-lists.v1')") is None


def test_list_save_reorder_remove_and_exact_citation_downloads(page, site):
    ready_collection(page, site[0], "?add=" + FIRST["key"])
    page.locator("#collection-candidate").select_option(SECOND["key"])
    page.locator("#collection-add").click()
    page.locator("#collection-items li").nth(1).get_by_role(
        "button", name="Move up:", exact=False
    ).click()
    assert page.locator("#collection-items li > a").all_text_contents() == [
        SECOND["title"],
        FIRST["title"],
    ]
    page.reload()
    page.locator("#collection-app:not([disabled])").wait_for(state="visible")
    assert page.locator("#collection-items li > a").all_text_contents() == [
        SECOND["title"],
        FIRST["title"],
    ]
    for format in ("bib", "ris", "csl", "md"):
        with page.expect_download() as info:
            page.locator(f'[data-collection-export="{format}"]').click()
        text = Path(info.value.path()).read_text()
        if format in {"bib", "ris"}:
            assert (
                text == SECOND[format].strip() + "\n\n" + FIRST[format].strip() + "\n"
            )
        elif format == "csl":
            assert json.loads(text) == [SECOND["csl"], FIRST["csl"]]
        else:
            assert text.index(SECOND["url"]) < text.index(FIRST["url"])
    page.locator("#collection-share").click()
    shared = page.locator("#collection-share-url").input_value()
    before = page.evaluate("localStorage.getItem('docxology.reading-lists.v1')")
    page.goto(shared)
    page.locator("#collection-save-shared").wait_for(state="visible")
    assert page.evaluate("localStorage.getItem('docxology.reading-lists.v1')") == before
    page.locator("#collection-save-shared").click()
    assert (
        len(
            json.loads(
                page.evaluate("localStorage.getItem('docxology.reading-lists.v1')")
            )["lists"]
        )
        == 2
    )
    page.locator("#collection-items li").first.get_by_role(
        "button", name="Remove:", exact=False
    ).click()
    assert page.locator("#collection-items li > a").all_text_contents() == [
        FIRST["title"]
    ]


def test_corrupt_storage_is_preserved_and_shared_title_cannot_inject_markup(page, site):
    ready_collection(page, site[0])
    page.evaluate("localStorage.setItem('docxology.reading-lists.v1','{broken')")
    suffix = "#" + urlencode(
        {"v": "1", "title": '<img src=x onerror="alert(1)">', "works": FIRST["key"]}
    )
    ready_collection(page, site[0], suffix)
    page.reload()
    page.locator("#collection-app:not([disabled])").wait_for(state="visible")
    assert "unreadable" in page.locator("#collection-status").inner_text()
    assert page.locator("#collection-title").input_value().startswith("<img")
    assert page.locator("#collection-app img").count() == 0
    assert (
        page.evaluate("localStorage.getItem('docxology.reading-lists.v1')") == "{broken"
    )
    page.get_by_text("Import or back up lists", exact=True).click()
    with page.expect_download() as info:
        page.locator("#collection-original").click()
    assert Path(info.value.path()).read_text() == "{broken"


def test_storage_denied_still_allows_preview_and_citation_export(page, site):
    page.add_init_script(
        "Object.defineProperty(window,'localStorage',{get(){throw new DOMException('blocked','SecurityError')}})"
    )
    ready_collection(page, site[0], "?add=" + FIRST["key"])
    assert "unavailable" in page.locator("#collection-status").inner_text()
    with page.expect_download() as info:
        page.locator('[data-collection-export="bib"]').click()
    assert Path(info.value.path()).read_text() == FIRST["bib"].strip() + "\n"


def test_valid_import_is_a_preview_and_list_deletion_can_be_undone(
    page, site, tmp_path
):
    ready_collection(page, site[0], "?add=" + FIRST["key"])
    backup = {
        "version": 1,
        "active": "imported",
        "lists": [
            {
                "id": "imported",
                "title": "Imported selection",
                "keys": [SECOND["key"], FIRST["key"]],
            }
        ],
    }
    source = tmp_path / "backup.json"
    source.write_text(json.dumps(backup))
    before = page.evaluate("localStorage.getItem('docxology.reading-lists.v1')")
    page.get_by_text("Import or back up lists", exact=True).click()
    page.locator("#collection-import").set_input_files(source)
    page.locator("#collection-import-choice option").wait_for(state="attached")
    page.locator("#collection-preview-import").click()
    assert page.locator("#collection-items li > a").all_text_contents() == [
        SECOND["title"],
        FIRST["title"],
    ]
    assert page.evaluate("localStorage.getItem('docxology.reading-lists.v1')") == before
    with page.expect_download() as info:
        page.locator("#collection-backup").click()
    exported = json.loads(Path(info.value.path()).read_text())
    assert exported["lists"][0]["keys"] == [SECOND["key"], FIRST["key"]]
    page.locator("#collection-save-shared").click()
    page.locator("#collection-delete").click()
    assert (
        len(
            json.loads(
                page.evaluate("localStorage.getItem('docxology.reading-lists.v1')")
            )["lists"]
        )
        == 1
    )
    page.locator("#collection-undo").click()
    assert page.locator("#collection-title").input_value() == "Imported selection"
    assert page.locator("#collection-items li > a").all_text_contents() == [
        SECOND["title"],
        FIRST["title"],
    ]


def test_cross_tab_change_does_not_overwrite_a_saved_library(page, site):
    ready_collection(page, site[0], "?add=" + FIRST["key"])
    other = page.context.new_page()
    ready_collection(other, site[0])
    page.locator("#collection-title").fill("Updated in first tab")
    page.locator("#collection-title").press("Tab")
    other.wait_for_function(
        "() => document.querySelector('#collection-status').textContent.includes('another tab')"
    )
    saved = page.evaluate("localStorage.getItem('docxology.reading-lists.v1')")
    other.locator("#collection-candidate").select_option(SECOND["key"])
    other.locator("#collection-add").click()
    assert other.locator("#collection-items li > a").count() == 2
    assert page.evaluate("localStorage.getItem('docxology.reading-lists.v1')") == saved
    other.close()


def test_unknown_shared_key_is_retained_and_blocks_lossy_citation_export(page, site):
    ready_collection(
        page,
        site[0],
        "#"
        + urlencode(
            {"v": "1", "title": "Missing work", "works": FIRST["key"] + ",UnknownWork"}
        ),
    )
    assert "UnknownWork" in page.locator("#collection-items").inner_text()
    downloads = []
    page.on("download", lambda item: downloads.append(item))
    page.locator('[data-collection-export="bib"]').click()
    assert (
        "Resolve unavailable work UnknownWork"
        in page.locator("#collection-status").inner_text()
    )
    assert downloads == []


def test_invalid_publication_url_is_normalized_and_checkbox_history_restores(
    page, site
):
    page.goto(
        site[0]
        + "/publications.html?type=Unknown&year=9999&domain=unsafe&sort=__proto__&dir=sideways"
    )
    page.wait_for_function(
        "() => document.querySelector('#result-count').textContent.includes('shown')"
    )
    assert "URL filter" in page.locator("#pub-url-status").inner_text()
    assert page.locator("#year-filter").input_value() == "all"
    assert page.locator("#filter-all").get_attribute("aria-pressed") == "true"
    previous = page.url
    page.locator("#doi-filter").check()
    assert parse_qs(urlparse(page.url).query)["doi"] == ["1"]
    page.go_back()
    page.wait_for_function("() => !document.querySelector('#doi-filter').checked")
    assert page.url == previous


def test_missing_catalog_and_invalid_import_are_explicit_recoverable_failures(
    page, site, tmp_path
):
    page.route("**/data/collection-catalog.json*", lambda route: route.abort())
    page.goto(site[0] + "/collections.html")
    page.locator("#collection-retry").wait_for(state="visible")
    assert "unavailable" in page.locator("#collection-status").inner_text()
    page.unroute("**/data/collection-catalog.json*")
    page.locator("#collection-retry").click()
    page.locator("#collection-app:not([disabled])").wait_for(state="visible")
    invalid = tmp_path / "invalid.json"
    invalid.write_text('{"version":2,"lists":[]}')
    page.get_by_text("Import or back up lists", exact=True).click()
    page.locator("#collection-import").set_input_files(invalid)
    page.wait_for_function(
        "() => document.querySelector('#collection-status').textContent.includes('Import refused')"
    )
    assert page.evaluate("localStorage.getItem('docxology.reading-lists.v1')") is None


def test_map_neighborhood_and_complete_list_match_graph_and_survive_history(page, site):
    graph = json.loads((REPO_ROOT / "data/research-map.json").read_text())
    node_id = "work:" + FIRST["key"]
    expected = [e for e in graph["edges"] if node_id in {e["source"], e["target"]}]
    page.goto(site[0] + "/research-map.html?" + urlencode({"node": node_id}))
    page.locator("#map-app:not([disabled])").wait_for(state="visible")
    assert page.locator("#map-title").inner_text() == FIRST["title"]
    assert page.locator("#map-connections li").count() == len(expected)
    page.locator("#map-connections button").first.click()
    assert page.locator("#map-title").inner_text() != FIRST["title"]
    page.go_back()
    assert page.locator("#map-title").inner_text() == FIRST["title"]
    person = max(
        (n for n in graph["nodes"] if n["kind"] == "person"),
        key=lambda n: sum(
            n["id"] in (e["source"], e["target"]) for e in graph["edges"]
        ),
    )
    page.goto(site[0] + "/research-map.html?" + urlencode({"node": person["id"]}))
    page.locator("#map-app:not([disabled])").wait_for(state="visible")
    total = sum(person["id"] in (e["source"], e["target"]) for e in graph["edges"])
    while page.locator("#map-more").is_visible():
        page.locator("#map-more").click()
    assert page.locator("#map-connections li").count() == total
    assert page.locator("#research-map-svg circle").count() == 13


def test_lab_worked_example_impossible_evidence_and_reproducible_csv(page, site):
    page.goto(site[0] + "/lab.html")
    page.locator("#bayes-positive").click()
    assert "0.50000000" in page.locator("#bayes-result").inner_text()
    page.locator("#bayes-negative").click()
    assert "0.20000000" in page.locator("#bayes-result").inner_text()
    page.locator("#bayes-prior").fill("0")
    page.locator("#bayes-no").fill("0")
    page.locator("#bayes-positive").click()
    assert "impossible" in page.locator("#bayes-result").inner_text()
    assert page.locator("#bayes-history tr").count() == 1
    page.locator("#urn-amber").fill("2")
    page.locator("#urn-blue").fill("3")
    page.locator("#urn-reinforcement").fill("0")
    page.locator("#urn-draws").fill("50")
    page.locator("#urn-run").click()
    assert "0.40000000" in page.locator("#urn-result").inner_text()
    exports = []
    for _ in range(2):
        page.locator("#urn-run").click()
        with page.expect_download() as info:
            page.locator("#urn-export").click()
        exports.append(Path(info.value.path()).read_bytes())
    assert exports[0] == exports[1]
    assert len(exports[0].decode().splitlines()) == 52
    with page.expect_download() as info:
        page.get_by_role(
            "link", name="Download the model implementations (JavaScript)"
        ).click()
    assert (
        Path(info.value.path()).read_bytes()
        == (REPO_ROOT / "js/probability-lab.js").read_bytes()
    )
    page.locator("#urn-draws").fill("201")
    page.locator("#urn-run").click()
    assert "integer" in page.locator("#urn-result").inner_text()
    assert page.locator("#urn-export").is_disabled()


@pytest.mark.parametrize("route", ["collections", "trails", "research-map", "lab"])
def test_tool_layout_keyboard_and_accessibility(page, site, route):
    page.goto(site[0] + "/" + route + ".html")
    if route == "collections":
        page.locator("#collection-app:not([disabled])").wait_for(state="visible")
    if route == "research-map":
        page.locator("#map-app:not([disabled])").wait_for(state="visible")
    for width, font in [(320, "100%"), (768, "100%"), (1280, "200%")]:
        page.set_viewport_size({"width": width, "height": 900})
        page.evaluate("size=>document.documentElement.style.fontSize=size", font)
        assert (
            page.evaluate(
                "document.documentElement.scrollWidth-document.documentElement.clientWidth"
            )
            <= 1
        ), route
    page.evaluate("document.documentElement.style.fontSize='100%'")
    page.emulate_media(reduced_motion="reduce", forced_colors="active")
    page.keyboard.press("Tab")
    assert page.evaluate("document.activeElement.tagName") in {
        "A",
        "BUTTON",
        "INPUT",
        "SELECT",
        "SUMMARY",
    }
    page.emulate_media(forced_colors="none")
    page.add_script_tag(url=site[0] + "/js/axe.min.js")
    violations = page.evaluate(
        "async()=>(await axe.run()).violations.filter(v=>['serious','critical'].includes(v.impact))"
    )
    assert not violations, [(v["id"], v["description"]) for v in violations]


def test_no_javascript_trails_and_model_definitions_remain_readable(site, browser):
    context = browser.new_context(java_script_enabled=False)
    page = context.new_page()
    page.goto(site[0] + "/trails.html")
    assert page.locator(".trail-steps").count() == 4
    assert page.get_by_text("Prerequisites:", exact=False).count() == 4
    assert page.locator('.trail-steps a[href^="/works/"]').count() >= 8
    page.goto(site[0] + "/lab.html")
    assert "posterior of 0.50" in page.locator("#bayes").inner_text()
    assert "not an ant-colony model" in page.locator("#urn").inner_text()
    page.goto(site[0] + "/research-map.html")
    page.get_by_text("Browse domains without", exact=False).click()
    domain_count = len(
        {
            w["domain_name"]
            for w in json.loads((REPO_ROOT / "data/works.json").read_text())["works"]
        }
    )
    assert (
        page.locator('main details a[href^="/publications.html"]').count()
        == domain_count
    )
    context.close()
