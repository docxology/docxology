"""Check the work and paper breadcrumb against the real page layout."""

from pathlib import Path
import shutil
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import REPO_ROOT, serve_site, stop_server  # noqa: E402

pytestmark = pytest.mark.browser

ROUTES = (
    "works/Friedman2026RikishiReproducibleOperationAnalysis236.html",
    "works/Friedman20262026ActiveInferenceSymposium237.html",
    "papers/2026_Rikishi/index.html",
    "papers/2026_SymposiumPresenterProgram/index.html",
)
RUNTIME_FILES = (
    "style.css",
    "js/nav-toggle.js",
    "js/search-utils.js",
    "js/tts-controls.js",
    "js/interactive.js",
    "js/cite-export.js",
    "js/menu-esc.js",
)


@pytest.fixture(scope="module")
def breadcrumb_site(tmp_path_factory):
    directory = tmp_path_factory.mktemp("work-breadcrumb-site")
    for name in (*ROUTES, *RUNTIME_FILES):
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / name, target)
    base, server = serve_site(directory)
    try:
        yield base
    finally:
        stop_server(server)


@pytest.fixture(scope="module")
def breadcrumb_browser(browser_runtime):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            yield browser
        finally:
            browser.close()


@pytest.mark.parametrize("route", ROUTES)
@pytest.mark.parametrize(
    "width,enhanced",
    [(320, True), (412, True), (320, False), (412, False), (1440, True)],
)
def test_work_and_paper_breadcrumb_leaves_title_uncovered(
    breadcrumb_site, breadcrumb_browser, route, width, enhanced
):
    from playwright.sync_api import expect

    height = 900
    context = breadcrumb_browser.new_context(
        viewport={"width": width, "height": height},
        java_script_enabled=enhanced,
        service_workers="block",
    )
    try:
        context.route(
            "**/*",
            lambda request: request.continue_()
            if request.request.url.startswith(breadcrumb_site + "/")
            else request.abort(),
        )
        page = context.new_page()
        with page.expect_response("**/style.css*") as css:
            response = page.goto(f"{breadcrumb_site}/{route}", wait_until="load")
        assert response is not None and response.ok
        assert css.value.ok

        masthead = page.get_by_role("navigation", name="Main navigation")
        breadcrumb = page.get_by_role("navigation", name="Breadcrumb")
        heading = page.get_by_role("heading", level=1)
        expect(masthead.locator(".nav-logo")).to_be_visible()
        expect(breadcrumb.get_by_role("link", name="Works", exact=True)).to_be_visible()
        expect(heading).to_be_visible()

        masthead_box = masthead.bounding_box()
        breadcrumb_box = breadcrumb.bounding_box()
        heading_box = heading.bounding_box()
        assert masthead_box is not None and breadcrumb_box is not None and heading_box is not None
        assert masthead_box["y"] + masthead_box["height"] <= breadcrumb_box["y"] + 1
        gap = heading_box["y"] - (breadcrumb_box["y"] + breadcrumb_box["height"])
        assert 0 <= gap <= 100, f"breadcrumb-to-title gap {gap}px on {route}"
        assert heading_box["y"] < height
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1")
        expect(breadcrumb).to_have_css("position", "static")
        expect(masthead).to_have_css("position", "fixed" if enhanced else "relative")
        if not enhanced:
            expect(masthead.locator(".nav-links")).to_be_visible()
            expect(masthead.locator(".menu-btn")).to_be_hidden()

        # Exercise the actual link hit target without leaving this route.
        breadcrumb.get_by_role("link", name="Works", exact=True).click(trial=True, timeout=3000)
    finally:
        context.close()
