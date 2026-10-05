"""Publication browsing stays light; abstract search remains complete and honest."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import REPO_ROOT, serve_site, skip_without_playwright, stop_server  # noqa: E402


@pytest.fixture
def publication_site(tmp_path):
    skip_without_playwright()
    site = tmp_path / "site"
    site.mkdir()
    shutil.copytree(REPO_ROOT / "js", site / "js")
    shutil.copy2(REPO_ROOT / "style.css", site / "style.css")
    shutil.copy2(REPO_ROOT / "publications.html", site / "publications.html")
    data_dir = site / "data"
    data_dir.mkdir()
    works = [
        {"num": number, "year": 2027 - number, "citation_key": name + "2026", "title": "Catalog " + name,
         "authors": ["Public Author"], "domain": domain, "domain_name": label, "type": "Paper", "venue": "Public Fixture", "url": "https://doi.org/10.example/" + name}
        for number, name, domain, label in [(1, "alpha", "🧠", "Active Inference"), (2, "beta", "🐜", "Entomology"), (3, "gamma", "💻", "Computational")]
    ]
    (data_dir / "works.json").write_text(json.dumps({"works": works}), encoding="utf-8")
    enrichment = {"works": {
        "alpha2026": {"abstract": "Alpha sourceonlyabstract", "keywords": ["firstkeyword"]},
        "beta2026": {"abstract": "Beta finding", "keywords": ["latestkeyword"]},
        "gamma2026": {"abstract": "Gamma finding", "keywords": []},
    }}
    (data_dir / "work-enrichment.json").write_text(json.dumps(enrichment), encoding="utf-8")
    base, server = serve_site(site)
    try:
        yield base
    finally:
        stop_server(server)


def _wait_catalog(page):
    page.wait_for_function("() => document.getElementById('result-count').textContent === '3 of 3 shown'")


def _record_requests(page):
    requests = []
    page.on("request", lambda request: requests.append(request.url.split("/")[-1].split("?")[0]))
    return requests


def _observe_enrichment_consumption(page):
    # Observe actual response parsing so post-response assertions cannot run
    # before the deferred fetch has completed its application callbacks.
    page.add_init_script("""const originalJSON = Response.prototype.json;
Response.prototype.json = function () {
    return originalJSON.call(this).then(data => {
        if (this.url.includes('work-enrichment.json')) window.enrichmentResponseParsed = true;
        return data;
    });
};""")


def test_catalog_startup_and_filters_do_not_download_enrichment(publication_site):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(service_workers="block")
        requests = _record_requests(page)
        page.goto(publication_site + "/publications.html", wait_until="load")
        _wait_catalog(page)
        assert page.locator("#pub-tbody tr").count() == 3
        assert requests.count("works.json") == 1
        assert "work-enrichment.json" not in requests
        page.get_by_role("button", name="Entomology", exact=True).click()
        assert page.locator("#pub-tbody .td-title").inner_text() == "Catalog beta"
        page.locator("#year-filter").select_option("2025")
        assert page.locator("#pub-tbody tr").count() == 1
        assert "work-enrichment.json" not in requests
        assert page.locator("#pub-table").get_attribute("aria-busy") == "false"
        browser.close()


def test_delayed_abstract_search_keeps_latest_query_and_scope(publication_site):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(service_workers="block")
        held = []
        page.route("**/data/work-enrichment.json*", lambda route: held.append(route))
        requests = _record_requests(page)
        page.goto(publication_site + "/publications.html", wait_until="load")
        _wait_catalog(page)
        with page.expect_request("**/data/work-enrichment.json*"):
            page.locator("#pub-search").fill("sourceonlyabstract")
        assert page.locator("#pub-table").get_attribute("aria-busy") == "true"
        assert page.locator("#no-results").is_hidden()
        assert "Searching publication abstracts" in page.locator("#pub-search-status").inner_text()
        page.locator("#pub-search").fill("latestkeyword")
        page.get_by_role("button", name="Entomology", exact=True).click()
        assert len(held) == 1
        held[0].fulfill(response=held[0].fetch())
        page.wait_for_function("() => document.querySelector('#pub-tbody .td-title')?.textContent === 'Catalog beta' && document.getElementById('pub-table').getAttribute('aria-busy') === 'false'")
        assert page.locator("#pub-search").input_value() == "latestkeyword"
        assert page.get_by_role("button", name="Entomology", exact=True).get_attribute("aria-pressed") == "true"
        assert requests.count("work-enrichment.json") == 1
        assert "search-index-core.json" not in requests
        assert page.locator(".search-suggestions").count() == 0
        page.get_by_role("button", name="Reset", exact=True).click()
        page.locator("#pub-search").fill("sourceonlyabstract")
        assert page.locator("#pub-tbody .td-title").inner_text() == "Catalog alpha"
        assert requests.count("work-enrichment.json") == 1
        browser.close()


def test_cleared_query_is_not_reinstated_after_enrichment_finishes(publication_site):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(service_workers="block")
        _observe_enrichment_consumption(page)
        held = []
        page.route("**/data/work-enrichment.json*", lambda route: held.append(route))
        page.goto(publication_site + "/publications.html", wait_until="load")
        _wait_catalog(page)
        with page.expect_request("**/data/work-enrichment.json*"):
            page.locator("#pub-search").fill("sourceonlyabstract")
        page.locator("#pub-search").fill("")
        _wait_catalog(page)
        assert page.locator("#pub-table").get_attribute("aria-busy") == "false"
        held[0].fulfill(response=held[0].fetch())
        page.wait_for_function("() => window.enrichmentResponseParsed === true")
        assert page.locator("#pub-search").input_value() == ""
        assert page.locator("#pub-tbody tr").count() == 3
        assert page.locator("#pub-search-status").is_hidden()
        browser.close()


@pytest.mark.parametrize("failure", ["http", "schema", "missing"])
def test_enrichment_failure_is_explicit_and_retryable(publication_site, failure):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(service_workers="block")
        requests = _record_requests(page)
        page.route("**/data/work-enrichment.json*", lambda route: route.fulfill(status=503, body="unavailable") if failure == "http" else route.fulfill(json={"works": [] if failure == "schema" else {}}))
        page.goto(publication_site + "/publications.html", wait_until="load")
        _wait_catalog(page)
        page.locator("#pub-search").fill("sourceonlyabstract")
        page.get_by_role("button", name="Retry abstract search", exact=True).wait_for()
        assert "temporarily unavailable" in page.locator("#pub-search-status").inner_text()
        assert page.locator("#no-results").is_hidden()
        assert page.locator("#pub-table").get_attribute("aria-busy") == "false"
        page.unroute("**/data/work-enrichment.json*")
        page.get_by_role("button", name="Retry abstract search", exact=True).click()
        page.wait_for_function("() => document.querySelector('#pub-tbody .td-title')?.textContent === 'Catalog alpha' && document.getElementById('pub-table').getAttribute('aria-busy') === 'false'")
        assert page.locator("#pub-search-status").is_hidden()
        assert requests.count("work-enrichment.json") == 2
        browser.close()


@pytest.mark.parametrize("javascript", [True, False])
def test_unavailable_catalog_preserves_server_rendered_native_links(publication_site, javascript):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(service_workers="block", java_script_enabled=javascript)
        page.route("**/data/works.json*", lambda route: route.fulfill(status=503, body="unavailable"))
        page.goto(publication_site + "/publications.html", wait_until="load")
        if javascript:
            page.wait_for_function("() => document.getElementById('result-count').textContent === 'Interactive catalog unavailable'")
            page.locator("#pub-search").fill("anything")
        assert page.locator("#pub-tbody tr").count() == 50
        assert page.locator("#pub-tbody .td-title a").first.get_attribute("href").startswith("works/")
        assert page.locator("#pub-tbody .td-title a").first.is_visible()
        browser.close()


def test_sorting_keeps_catalog_bounded_and_load_more_moves_keyboard_focus(publication_site):
    from playwright.sync_api import sync_playwright

    works = [{'num': number, 'year': 2026, 'citation_key': f'PublicFixture{number}',
              'title': f'Fixture work {number:03d}', 'authors': ['Public Author'],
              'domain': '🧠', 'type': 'Paper', 'venue': 'Public Fixture'}
             for number in range(1, 124)]
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(service_workers='block')
        page.route('**/data/works.json*', lambda route: route.fulfill(json={'works': works}))
        requests = _record_requests(page)
        page.goto(publication_site + '/publications.html')
        page.wait_for_function('() => document.getElementById("result-count").textContent === "50 of 123 shown"')
        page.get_by_role('button', name='Sort by Title', exact=True).click()
        assert page.locator('#pub-tbody tr').count() == 50
        page.locator('#pub-load-more').click()
        assert page.locator('#pub-tbody tr').count() == 100
        assert page.evaluate('() => document.activeElement.textContent') == 'Fixture work 051'
        page.get_by_role('button', name='Sorted by Title ascending', exact=True).click()
        assert page.locator('#pub-tbody tr').count() == 50
        page.locator('#pub-load-more').click()
        page.locator('#pub-load-more').click()
        assert page.locator('#pub-tbody tr').count() == len(works)
        assert page.locator('#pub-load-more').is_hidden()
        assert page.locator('#pub-tbody .td-title').all_text_contents() == [work['title'] for work in reversed(works)]
        assert 'work-enrichment.json' not in requests
        browser.close()
