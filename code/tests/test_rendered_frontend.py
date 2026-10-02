"""Browser acceptance for progressive search and truthful section-link copying."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import REPO_ROOT, serve_site, skip_without_playwright, stop_server  # noqa: E402


@pytest.fixture
def frontend_site(tmp_path):
    """Serve a small public fixture with the actual shared scripts and stylesheet."""
    skip_without_playwright()
    site = tmp_path / "site"
    site.mkdir()
    shutil.copytree(REPO_ROOT / "js", site / "js")
    shutil.copy2(REPO_ROOT / "style.css", site / "style.css")
    (site / "index.html").write_text("""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Frontend acceptance</title><link rel="stylesheet" href="/style.css"><script src="/js/nav-toggle.js"></script></head><body>
<nav aria-label="Main"><a class="nav-logo" href="#topic">Profile</a><button class="menu-btn" aria-controls="nav-menu" aria-expanded="false">Menu</button><ul class="nav-links" id="nav-menu"><li><a href="#topic" id="opener">Works</a></li></ul></nav>
<main class="page-hero"><section id="topic"><h2>Research section</h2></section>
<input class="search-input" id="q" aria-label="Search"><div id="filters"></div><section id="result-status"></section><section id="results"></section></main>
<script src="/js/search-utils.js"></script><script src="/js/search-page.js" defer></script><script src="/js/interactive.js" defer></script>
</body></html>""", encoding="utf-8")
    stamp = "2026-10-02T00:00:00Z"
    work = {"id": "work:1", "type": "work", "title": "Test paper", "url": "/works/paper.html", "summary": "Paper overview"}
    video = {"id": "video:1", "type": "video", "title": "Test talk", "url": "/videos/talk.html", "summary": "Talk overview"}
    page = {"id": "page:1", "type": "page", "title": "Profile", "url": "/about.html", "content": "crypticpagephrase"}
    for name, data in {
        "search-index-core.json": {"generated_at": stamp, "content_segments": ["work", "video"], "items": [work, video, page]},
        "search-index-content-work.json": {"generated_at": stamp, "type": "work", "items": [dict(work, content="crypticworkphrase ant-colony active c++")]},
        "search-index-content-video.json": {"generated_at": stamp, "type": "video", "items": [dict(video, content="crypticvideophrase important inference")]},
    }.items():
        (site / name).write_text(json.dumps(data), encoding="utf-8")
    base, server = serve_site(site)
    try:
        yield base
    finally:
        stop_server(server)


def test_progressive_search_fetches_core_once_and_retains_all_text_matches(frontend_site):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(service_workers="block")
        page = context.new_page()
        requests = []
        page.on("request", lambda request: requests.append(request.url.split("/")[-1]))
        page.goto(frontend_site + "/index.html", wait_until="load")
        page.wait_for_selector(".result-card")
        assert requests.count("search-index-core.json") == 1
        assert not any("content-work" in url or "content-video" in url for url in requests)
        for phrase, title in (("crypticworkphrase", "Test paper"), ("crypticvideophrase", "Test talk"), ("crypticpagephrase", "Profile")):
            page.locator("#q").fill(phrase)
            page.wait_for_function("expected => new URL(location.href).searchParams.get('q') === expected.q && document.getElementById('results').getAttribute('aria-busy') === 'false' && document.querySelector('#results h2')?.textContent === expected.title", arg={"q": phrase, "title": title})
        assert requests.count("search-index-core.json") == 1
        assert page.locator(".search-suggestions").count() == 0
        assert requests.count("search-index-content-work.json") == 1
        assert requests.count("search-index-content-video.json") == 1
        assert "search-index.json" not in requests
        context.close()
        browser.close()


def test_selected_search_type_loads_only_its_text_and_keeps_term_semantics(frontend_site):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(service_workers="block")
        page = context.new_page()
        requests = []
        page.on("request", lambda request: requests.append(request.url.split("/")[-1]))
        page.goto(frontend_site + "/index.html", wait_until="load")
        page.get_by_role("button", name="work (1)", exact=True).click()
        page.locator("#q").fill("crypticworkphrase")
        page.wait_for_function("new URL(location.href).searchParams.get('q') === 'crypticworkphrase' && document.getElementById('results').getAttribute('aria-busy') === 'false' && document.querySelector('#results h2')?.textContent === 'Test paper'")
        assert "search-index-content-work.json" in requests
        assert "search-index-content-video.json" not in requests
        page.get_by_role("button", name="all (3)", exact=True).click()
        for phrase in ("ant", "c++"):
            page.locator("#q").fill(phrase)
            page.wait_for_function("q => new URL(location.href).searchParams.get('q') === q && document.getElementById('results').getAttribute('aria-busy') === 'false' && document.querySelector('#results h2')?.textContent === 'Test paper'", arg=phrase)
            assert page.locator(".result-card").count() == 1
        page.locator("#q").fill("active inference")
        page.wait_for_function("document.getElementById('result-status').textContent.includes('No results for')")
        assert not page.locator(".result-card").count()
        context.close()
        browser.close()


def test_partial_search_failure_is_explicit_and_retry_recovers(frontend_site):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(service_workers="block")
        page = context.new_page()
        page.route("**/search-index-content-work.json", lambda route: route.fulfill(status=503, body="unavailable"))
        page.goto(frontend_site + "/index.html?q=crypticworkphrase", wait_until="load")
        page.get_by_role("button", name="Retry full-text search").wait_for()
        assert "temporarily unavailable" in page.locator("#result-status").inner_text()
        assert "No results" not in page.locator("#result-status").inner_text()
        page.unroute("**/search-index-content-work.json")
        page.get_by_role("button", name="Retry full-text search").click()
        page.get_by_role("link", name="Test paper", exact=True).wait_for()
        assert "temporarily unavailable" not in page.locator("#result-status").inner_text()
        context.close()
        browser.close()


def test_deploy_transition_retry_updates_core_and_filter_counts(frontend_site):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(service_workers="block")
        page = context.new_page()
        core_requests = []

        def deployed_core(route):
            response = route.fetch()
            data = response.json()
            core_requests.append(route.request.url)
            if len(core_requests) == 1:
                data["generated_at"] = "2026-10-01T00:00:00Z"
            else:
                data["items"].append({"id": "page:2", "type": "page", "title": "New page", "url": "/new.html", "content": "new deployment"})
            route.fulfill(response=response, json=data)

        page.route("**/search-index-core.json", deployed_core)
        page.goto(frontend_site + "/index.html?q=crypticworkphrase", wait_until="load")
        page.get_by_role("button", name="Retry full-text search").wait_for()
        assert len(core_requests) == 1
        assert page.get_by_role("button", name="all (3)", exact=True).count() == 1
        page.get_by_role("button", name="Retry full-text search").click()
        page.get_by_role("link", name="Test paper", exact=True).wait_for()
        page.get_by_role("button", name="all (4)", exact=True).wait_for()
        assert len(core_requests) == 2
        assert "temporarily unavailable" not in page.locator("#result-status").inner_text()
        context.close()
        browser.close()


def test_section_copy_reports_success_after_resolution_and_preserves_query(frontend_site):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(service_workers="block")
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'clipboard', {configurable:true, value:{writeText:url=>{window.copiedURL=url; return new Promise(resolve=>window.finishCopy=resolve);}}});")
        page.goto(frontend_site + "/index.html?q=paper", wait_until="load")
        link = page.locator(".anchor-link")
        link.click()
        page.wait_for_function("typeof window.finishCopy === 'function'")
        assert link.inner_text() == "#"
        assert page.evaluate("window.copiedURL") == frontend_site + "/index.html?q=paper#topic"
        page.evaluate("window.finishCopy()")
        page.wait_for_function("document.querySelector('.anchor-link').textContent === '✓'")
        context.close()
        browser.close()


@pytest.mark.parametrize("clipboard", ["undefined", "{writeText:()=>Promise.reject(new Error('denied'))}", "{writeText:()=>{throw new Error('unavailable')}}"])
def test_section_copy_unavailable_or_denied_uses_real_anchor(frontend_site, clipboard):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(service_workers="block")
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.add_init_script("Object.defineProperty(navigator, 'clipboard', {configurable:true, value:" + clipboard + "});")
        page.goto(frontend_site + "/index.html", wait_until="load")
        page.locator(".anchor-link").click()
        page.wait_for_function("location.hash === '#topic'")
        assert page.locator(".anchor-link").inner_text() == "#"
        assert not errors
        context.close()
        browser.close()
