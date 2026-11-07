"""Exercise the complete generated Updates list at narrow widths."""

from pathlib import Path
import shutil
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import REPO_ROOT, serve_site, stop_server  # noqa: E402

pytestmark = pytest.mark.browser

PAGE_INPUTS = (
    "updates.html",
    "style.css",
    "js/nav-toggle.js",
    "js/search-utils.js",
    "js/tts-controls.js",
    "js/interactive.js",
    "js/menu-esc.js",
)


@pytest.fixture(scope="module")
def updates_site(tmp_path_factory):
    directory = tmp_path_factory.mktemp("updates-layout")
    for name in PAGE_INPUTS:
        target = directory / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / name, target)
    base, server = serve_site(directory)
    try:
        yield base
    finally:
        stop_server(server)


@pytest.fixture(scope="module")
def updates_browser(browser_runtime):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            yield browser
        finally:
            browser.close()


@pytest.mark.parametrize(
    "width,enhanced",
    [(320, True), (390, True), (390, False), (1440, True)],
)
def test_updates_cards_and_long_links_fit_the_viewport(updates_site, updates_browser, width, enhanced):
    context = updates_browser.new_context(
        viewport={"width": width, "height": 900},
        java_script_enabled=enhanced,
        service_workers="block",
    )
    try:
        context.route(
            "**/*",
            lambda route: route.continue_()
            if route.request.url.startswith(updates_site + "/")
            else route.abort(),
        )
        page = context.new_page()
        with page.expect_response("**/style.css*") as css:
            response = page.goto(updates_site + "/updates.html", wait_until="load")
        assert response is not None and response.ok and css.value.ok
        assert page.get_by_role("heading", name="Updates", exact=True).is_visible()
        assert page.locator(".updates-list .update-card").count() > 10
        assert page.locator(".updates-list .update-card a").count() > 10

        layout = page.evaluate(
            """() => {
                const viewport = document.documentElement.clientWidth;
                const width = document.documentElement.scrollWidth;
                const offenders = [];
                const measured = document.querySelectorAll(
                    '.updates-list, .update-card, .update-card a, .update-card code'
                );
                for (const element of measured) {
                    for (const rect of element.getClientRects()) {
                        if (rect.left < -1 || rect.right > viewport + 1) {
                            offenders.push({
                                tag: element.tagName,
                                className: element.className,
                                text: element.textContent.trim().slice(0, 120),
                                left: Math.round(rect.left),
                                right: Math.round(rect.right)
                            });
                            break;
                        }
                    }
                }
                return {viewport, width, count: offenders.length, sample: offenders.slice(0, 8)};
            }"""
        )
        assert layout["width"] <= layout["viewport"] + 1 and not layout["count"], (
            f"Updates content overflows viewport: {layout}"
        )
    finally:
        context.close()
