"""Real-browser mobile fallback and shortcut-dialog keyboard acceptance."""
from __future__ import annotations

import sys
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import REPO_ROOT, ROOT_RUNTIME_FILES, serve_copy, skip_without_playwright, stop_server  # noqa: E402


def test_mobile_routes_remain_reachable_without_javascript_and_shortcuts_restore_focus(tmp_path):
    skip_without_playwright()
    from playwright.sync_api import sync_playwright

    base, server = serve_copy(tmp_path)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(java_script_enabled=False, viewport={"width": 320, "height": 760}, service_workers="block")
            page = context.new_page()
            for route in ("index.html", "publications.html", "art.html", "videos.html", "search.html", "works/Friedman2026FourfoldVisionWilliamBlake196.html"):
                page.goto(base + "/" + route, wait_until="domcontentloaded")
                links = page.locator(".nav-links > li > a")
                assert links.count() >= 4, route
                assert all(link.is_visible() for link in links.all()), route
                more = page.locator(".nav-more summary").first
                more.click()
                assert page.locator(".nav-more-panel a").first.is_visible(), route
                assert not page.locator(".menu-btn").is_visible(), route
            context.close()
            context = browser.new_context(viewport={"width": 1100, "height": 850}, service_workers="block")
            page = context.new_page()
            page.goto(base + "/index.html", wait_until="domcontentloaded")
            page.wait_for_selector("#shortcuts-overlay", state="attached")
            opener = page.locator(".nav-logo").first
            opener.focus()
            page.keyboard.press("?")
            page.wait_for_selector("#shortcuts-overlay[aria-hidden='false']")
            for key in ("Tab", "Shift+Tab", "Tab"):
                page.keyboard.press(key)
                assert page.evaluate("document.querySelector('#shortcuts-overlay').contains(document.activeElement)"), key
            page.keyboard.press("Escape")
            assert page.locator("#shortcuts-overlay").get_attribute("aria-hidden") == "true"
            assert opener.evaluate("node => node === document.activeElement")
            assert page.locator("#shortcuts-overlay").evaluate("node => node.inert")
            context.close()
            browser.close()
    finally:
        stop_server(server)


def test_actual_generated_search_exports_render_a_deferred_text_match(tmp_path):
    """Exercise the real search page/exports, beyond small synthetic fixtures."""
    skip_without_playwright()
    from playwright.sync_api import sync_playwright

    core = json.loads((REPO_ROOT / "search-index-core.json").read_text(encoding="utf-8"))
    works = json.loads((REPO_ROOT / "search-index-content-work.json").read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in core["items"]}
    target = None
    # Find a real, uncommon body term absent from that work's initial metadata.
    # This forces deferred full text to supply the match, without freezing a
    # source-dependent phrase or relying on initial title/summary matches.
    for item in works["items"]:
        metadata = " ".join(str(value) for value in by_id[item["id"]].values()).lower()
        for term in re.findall(r"\b[A-Za-z]{10,30}\b", item["content"].lower()):
            if term in metadata:
                continue
            pattern = re.compile(r"\b" + re.escape(term) + r"\b", re.I)
            if sum(bool(pattern.search(other["content"])) for other in works["items"]) <= 4:
                target = (term, by_id[item["id"]]["url"])
                break
        if target:
            break
    assert target, "Generated work text has no deep-search acceptance candidate"
    term, expected_url = target
    base, server = serve_copy(tmp_path)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(service_workers="block")
            page = context.new_page()
            requests = []
            page.on("request", lambda request: requests.append(urlsplit(request.url).path))
            page.goto(base + "/search.html", wait_until="load")
            page.wait_for_selector(".result-card")
            assert requests.count("/search-index-core.json") == 1
            assert "/search-index-content-work.json" not in requests
            assert "/search-index-content-video.json" not in requests
            work_count = sum(item["type"] == "work" for item in core["items"])
            page.get_by_role("button", name=f"work ({work_count})", exact=True).click()
            page.locator("#q").fill(term)
            page.wait_for_function("""({ term, url }) => new URLSearchParams(location.search).get('q') === term &&
              document.getElementById('results').getAttribute('aria-busy') === 'false' &&
              Array.from(document.querySelectorAll('.result-card h2 a')).some(link => link.getAttribute('href') === url)
            """, arg={"term": term, "url": expected_url})
            assert requests.count("/search-index-core.json") == 1
            assert requests.count("/search-index-content-work.json") == 1
            assert "/search-index-content-video.json" not in requests
            assert "/search-index.json" not in requests
            assert not page.get_by_role("button", name="Retry full-text search").count()
            # The served core and both detail segments must be exact siblings
            # of the checked-in generation, never fixture-invented substitutes.
            for name in sorted(ROOT_RUNTIME_FILES | {path.name for path in REPO_ROOT.glob("search-index*.json")}):
                response = context.request.get(base + "/" + name)
                assert response.status == 200, name
                assert response.body() == (REPO_ROOT / name).read_bytes(), name
            # Homepage startup also must not eagerly transfer the agent-facing
            # full export through an obsolete browser prefetch hint.
            requests.clear()
            page.goto(base + "/index.html", wait_until="networkidle")
            assert "/search-index.json" not in requests
            context.close()
            browser.close()
    finally:
        stop_server(server)


@pytest.mark.parametrize("width", [320, 412])
def test_search_reserves_loading_space_and_keeps_sparse_results_usable(tmp_path, width):
    """The real core may arrive late without moving a visible mobile footer."""
    skip_without_playwright()
    from playwright.sync_api import sync_playwright

    core = json.loads((REPO_ROOT / "search-index-core.json").read_text(encoding="utf-8"))
    detail = json.loads((REPO_ROOT / "search-index-content-work.json").read_text(encoding="utf-8"))
    bodies = {item["id"]: item["content"] for item in detail["items"]}
    works = [item for item in core["items"] if item["type"] == "work"]
    searchable = {
        item["id"]: " ".join((item["title"], item.get("summary", ""), " ".join(item.get("tags", [])), bodies.get(item["id"], "")))
        for item in works
    }
    target = None
    for item in works:
        terms = re.findall(r"\b[A-Za-z]+\b", item["title"])
        expressions = [re.compile(r"\b" + re.escape(term), re.I) for term in terms]
        matches = [key for key, text in searchable.items() if all(expression.search(text) for expression in expressions)]
        if matches == [item["id"]]:
            target = (" ".join(terms), item["url"])
            break
    assert target, "Generated catalog has no work-specific single-result query"
    query, expected_url = target
    viewport = {"width": width, "height": 823}
    base, server = serve_copy(tmp_path)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport=viewport, service_workers="block")
            page = context.new_page()
            held_core = []
            page.route("**/search-index-core.json", lambda route: held_core.append(route))
            with page.expect_request("**/search-index-core.json"):
                page.goto(base + "/search.html", wait_until="domcontentloaded")
            page.wait_for_function("() => document.getElementById('results').getAttribute('aria-busy') === 'true'")
            # Let the browser complete layout while the actual export remains
            # pending; no invented core or injected page styles are involved.
            page.evaluate("() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))")
            assert page.locator(".result-card").count() == 0
            assert page.locator("footer").bounding_box()["y"] >= viewport["height"]
            pending_filter_box = page.locator("#filters").bounding_box()
            pending_results_y = page.locator("#results").bounding_box()["y"]
            assert len(held_core) == 1
            held_core[0].continue_()
            page.wait_for_function("() => document.querySelectorAll('.result-card').length === 40 && document.getElementById('results').getAttribute('aria-busy') === 'false'")
            loaded_filter_box = page.locator("#filters").bounding_box()
            assert abs(loaded_filter_box["height"] - pending_filter_box["height"]) <= 1
            assert abs(page.locator("#results").bounding_box()["y"] - pending_results_y) <= 1
            # Every type remains available in the bounded horizontal strip;
            # keyboard focus must bring a later option into its visible area.
            last_filter = page.locator("#filters button").last
            last_filter.focus()
            assert last_filter.evaluate("node => node === document.activeElement")
            page.wait_for_function("() => document.getElementById('filters').scrollLeft > 0")
            page.wait_for_function("() => { const group = document.getElementById('filters').getBoundingClientRect(); const last = document.querySelector('#filters button:last-child').getBoundingClientRect(); return last.right <= group.right + 1; }")
            assert last_filter.bounding_box()["x"] + last_filter.bounding_box()["width"] <= loaded_filter_box["x"] + loaded_filter_box["width"] + 1
            page.get_by_role("button", name=f"work ({len(works)})", exact=True).click()
            absent = "docxology_no_matching_results_" + "x" * 120
            page.locator("#q").fill(absent)
            page.wait_for_function("query => new URLSearchParams(location.search).get('q') === query && document.getElementById('results').getAttribute('aria-busy') === 'false' && document.querySelectorAll('.result-card').length === 0", arg=absent)
            status = page.locator("#result-status")
            assert status.is_visible()
            assert status.get_attribute("aria-live") == "polite"
            assert "No results for" in status.inner_text()
            assert status.get_by_role("link", name="works index").is_visible()
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            page.locator("#q").fill(query)
            page.wait_for_function("({query, url}) => new URLSearchParams(location.search).get('q') === query && document.getElementById('results').getAttribute('aria-busy') === 'false' && document.querySelectorAll('.result-card').length === 1 && document.querySelector('.result-card h2 a').getAttribute('href') === url", arg={"query": query, "url": expected_url})
            assert "1 result for" in status.inner_text()
            card = page.locator(".result-card")
            area = page.locator("#results").bounding_box()
            assert card.bounding_box()["height"] < area["height"], "One result should not stretch to fill reserved loading space"
            result_link = card.get_by_role("link")
            result_link.scroll_into_view_if_needed()
            result_link.focus()
            assert result_link.evaluate("node => node === document.activeElement")
            assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
            context.close()

            context = browser.new_context(viewport=viewport, java_script_enabled=False, service_workers="block")
            page = context.new_page()
            page.goto(base + "/search.html", wait_until="domcontentloaded")
            fallback = page.locator("noscript")
            links = fallback.get_by_role("link")
            assert links.count() == 3
            assert all(link.is_visible() for link in links.all())
            last_link = links.last.bounding_box()
            assert last_link["y"] + last_link["height"] <= page.locator("#results").bounding_box()["y"]
            context.close()
            browser.close()
    finally:
        stop_server(server)
