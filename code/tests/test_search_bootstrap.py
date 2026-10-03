"""The initial browsing preview defers full search without narrowing queries."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import REPO_ROOT, serve_site, skip_without_playwright, stop_server  # noqa: E402


@pytest.fixture
def bootstrap_site(tmp_path):
    skip_without_playwright()
    site = tmp_path / "site"
    site.mkdir()
    shutil.copytree(REPO_ROOT / "js", site / "js")
    shutil.copy2(REPO_ROOT / "style.css", site / "style.css")
    shutil.copy2(REPO_ROOT / "search.html", site / "search.html")
    stamp = "2026-10-03T00:00:00Z"
    pages = [
        {"id": f"page:{i}", "type": "page", "title": f"Public page {i}", "url": f"/pages/{i}.html", "summary": "Browse preview", "content": "page-only detail"}
        for i in range(40)
    ]
    work = {"id": "work:1", "type": "work", "title": "Research outside preview", "url": "/works/paper.html", "summary": "Publication overview"}
    video = {"id": "video:1", "type": "video", "title": "Talk outside preview", "url": "/videos/talk.html", "summary": "Video overview"}
    for name, data in {
        "search-index-bootstrap.json": {"generated_at": stamp, "count": 42, "type_counts": {"page": 40, "work": 1, "video": 1}, "items": pages},
        "search-index-core.json": {"generated_at": stamp, "content_segments": ["work", "video"], "items": [*pages, work, video]},
        "search-index-content-work.json": {"generated_at": stamp, "type": "work", "items": [dict(work, content="sourceonlyneedle ant-colony c++")]},
        "search-index-content-video.json": {"generated_at": stamp, "type": "video", "items": [dict(video, content="transcriptonlyneedle important inference")]},
    }.items():
        (site / name).write_text(json.dumps(data), encoding="utf-8")
    base, server = serve_site(site)
    try:
        yield base
    finally:
        stop_server(server)


def test_empty_browse_only_fetches_preview_with_complete_counts_and_filters(bootstrap_site):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(service_workers="block")
        requests = []
        page.on("request", lambda request: requests.append(request.url.split("/")[-1]))
        page.goto(bootstrap_site + "/search.html", wait_until="load")
        page.wait_for_function("() => document.querySelector('#results h2') && document.getElementById('results').getAttribute('aria-busy') === 'false'")
        assert page.locator(".result-card").count() == 40
        assert page.get_by_role("button", name="all (42)", exact=True).count() == 1
        assert requests.count("search-index-bootstrap.json") == 1
        assert "search-index-core.json" not in requests
        assert not any("content-" in name for name in requests)

        page.get_by_role("button", name="work (1)", exact=True).click()
        page.wait_for_function("() => document.querySelector('#results h2')?.textContent === 'Research outside preview' && document.getElementById('results').getAttribute('aria-busy') === 'false'")
        assert requests.count("search-index-core.json") == 1
        assert not any("content-" in name for name in requests)
        page.locator("#q").fill("sourceonlyneedle")
        page.wait_for_function("() => new URL(location.href).searchParams.get('q') === 'sourceonlyneedle' && document.getElementById('results').getAttribute('aria-busy') === 'false'")
        assert page.get_by_role("link", name="Research outside preview", exact=True).count() == 1
        assert requests.count("search-index-content-work.json") == 1
        assert "search-index-content-video.json" not in requests
        browser.close()


def test_url_query_skips_preview_and_preserves_full_text_matches(bootstrap_site):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(service_workers="block")
        requests = []
        page.on("request", lambda request: requests.append(request.url.split("/")[-1]))
        page.goto(bootstrap_site + "/search.html?q=transcriptonlyneedle", wait_until="load")
        page.wait_for_function("() => document.querySelector('#results h2')?.textContent === 'Talk outside preview' && document.getElementById('results').getAttribute('aria-busy') === 'false'")
        assert "search-index-bootstrap.json" not in requests
        assert requests.count("search-index-core.json") == 1
        assert requests.count("search-index-content-work.json") == 1
        assert requests.count("search-index-content-video.json") == 1
        browser.close()


def test_unavailable_core_can_retry_without_losing_the_query(bootstrap_site):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(service_workers="block")
        page.route("**/search-index-core.json", lambda route: route.fulfill(status=503, body="unavailable"))
        page.goto(bootstrap_site + "/search.html?q=sourceonlyneedle", wait_until="load")
        page.get_by_role("button", name="retry search", exact=True).wait_for()
        assert page.locator("#results").get_attribute("role") == "alert"
        assert page.locator("#results").get_attribute("aria-busy") == "false"
        assert page.locator("#result-status").is_hidden()
        page.unroute("**/search-index-core.json")
        page.get_by_role("button", name="retry search", exact=True).click()
        page.wait_for_function("() => document.querySelector('#results h2')?.textContent === 'Research outside preview' && document.getElementById('results').getAttribute('aria-busy') === 'false'")
        assert page.locator("#q").input_value() == "sourceonlyneedle"
        assert page.locator("#results").get_attribute("role") is None
        browser.close()


def test_late_preview_does_not_replace_an_active_query_or_scope(bootstrap_site):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(service_workers="block")
        held = []
        page.route("**/search-index-bootstrap.json", lambda route: held.append(route))
        page.goto(bootstrap_site + "/search.html", wait_until="load")
        page.wait_for_function("() => document.getElementById('q').hasAttribute('data-local-search')")
        page.locator("#q").fill("sourceonlyneedle")
        page.wait_for_function("() => document.querySelector('#results h2')?.textContent === 'Research outside preview' && document.getElementById('results').getAttribute('aria-busy') === 'false'")
        page.get_by_role("button", name="work (1)", exact=True).click()
        assert len(held) == 1
        with page.expect_response("**/search-index-bootstrap.json"):
            held[0].fulfill(response=held[0].fetch())
        # A subsequent task observes all promise reactions from the response.
        page.evaluate("() => new Promise(resolve => setTimeout(resolve, 0))")
        assert page.locator("#q").input_value() == "sourceonlyneedle"
        assert page.get_by_role("button", name="work (1)", exact=True).get_attribute("aria-pressed") == "true"
        assert page.locator("#results h2").inner_text() == "Research outside preview"
        browser.close()


@pytest.mark.parametrize("failure", ["unavailable", "bad-counts", "duplicate"])
def test_preview_failure_falls_back_to_existing_complete_core(bootstrap_site, failure):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(service_workers="block")

        def broken_preview(route):
            if failure == "unavailable":
                route.fulfill(status=503, body="temporarily unavailable")
                return
            response = route.fetch()
            data = response.json()
            if failure == "bad-counts":
                data["type_counts"]["work"] = 4
            else:
                data["items"][1] = data["items"][0]
            route.fulfill(response=response, json=data)

        page.route("**/search-index-bootstrap.json", broken_preview)
        requests = []
        page.on("request", lambda request: requests.append(request.url.split("/")[-1]))
        page.goto(bootstrap_site + "/search.html", wait_until="load")
        page.get_by_role("button", name="all (42)", exact=True).wait_for()
        page.wait_for_function("() => document.getElementById('results').getAttribute('aria-busy') === 'false'")
        assert page.locator(".result-card").count() == 40
        assert requests.count("search-index-core.json") == 1
        browser.close()
