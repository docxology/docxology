"""Click-to-load YouTube facade on generated video pages.

The player iframe must not exist until the reader clicks the poster: the eager
third-party player bundle gates first paint.  Measured live 2026-11-03, the
same page with identical bytes showed observed LCP 2.4 s with the eager iframe
against 0.26 s behind the facade, and the Lighthouse performance score swung
between 59 and 100 with it.

These tests drive the real generated page in Chromium.  The click contract is a
degradation ladder, not a single happy path:

* with the shared module loaded, the click prevents the default navigation and
  injects the youtube-nocookie player in place of the poster;
* without JavaScript, the poster link still opens the watch page;
* with the shared module missing (an older cached copy is exactly this), the
  same link still opens the watch page instead of a dead poster.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import REPO_ROOT, serve_site, stop_server  # noqa: E402

pytestmark = pytest.mark.browser

VIDEO_PAGE = "videos/personal-NWrGixOmW6k.html"
WATCH_URL_PREFIX = "https://www.youtube.com/watch?"
WATCH_STUB = "<html><body><h1 id=watch-stub>watch page</h1></body></html>"


@pytest.fixture(scope="module")
def video_site(tmp_path_factory):
    site = tmp_path_factory.mktemp("video-facade") / "site"
    site.mkdir()
    for name in ("style.css", "favicon.ico", "manifest.json"):
        source = REPO_ROOT / name
        if source.exists():
            shutil.copy2(source, site / name)
    for name in ("js", "data"):
        shutil.copytree(REPO_ROOT / name, site / name)
    (site / "videos").mkdir()
    shutil.copy2(REPO_ROOT / VIDEO_PAGE, site / VIDEO_PAGE)
    page_text = (site / VIDEO_PAGE).read_text(encoding="utf-8")
    assert "data-youtube-src=" in page_text, (
        "Regenerate the video pages first: the facade contract belongs to the generator"
    )
    base, server = serve_site(site)
    try:
        yield base
    finally:
        stop_server(server)


@pytest.fixture(scope="module")
def browser(browser_runtime):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        instance = p.chromium.launch(headless=True)
        yield instance
        instance.close()


def stub_watch_page(context) -> None:
    """Serve a local marker for the watch URL so navigation is observable."""
    context.route(
        WATCH_URL_PREFIX + "**",
        lambda route: route.fulfill(
            status=200, content_type="text/html", body=WATCH_STUB
        ),
    )


def assert_opens_watch_page(context, facade) -> None:
    with context.expect_page() as opened:
        facade.click()
    watch_page = opened.value
    watch_page.wait_for_selector("#watch-stub")
    assert watch_page.url.startswith(WATCH_URL_PREFIX.rstrip("?"))


def test_click_injects_the_player_and_the_page_still_renders(video_site, browser):
    base = video_site
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    # Third-party requests are refused, so the assertions are about the markup
    # the click creates rather than about YouTube's response.
    context.route(
        "**/*",
        lambda route: (
            route.continue_() if route.request.url.startswith(base) else route.abort()
        ),
    )
    page = context.new_page()
    page.goto(base + "/" + VIDEO_PAGE, wait_until="domcontentloaded")

    # Render without the player: heading, transcript, facade, and no iframe.
    assert page.locator("h1").count() == 1
    assert page.locator(".transcript").count() == 1
    assert page.locator("iframe").count() == 0
    facade = page.locator("[data-youtube-src]").first
    assert facade.count() == 1
    embed_src = facade.get_attribute("data-youtube-src") or ""
    assert embed_src.startswith("https://www.youtube-nocookie.com/embed/")
    label = facade.get_attribute("aria-label") or ""
    assert label.startswith("Play video:"), f"facade label drifted: {label!r}"
    assert facade.get_attribute("data-youtube-title")
    assert (facade.get_attribute("href") or "").startswith(WATCH_URL_PREFIX)

    facade.click()
    page.wait_for_selector("iframe")
    iframe = page.locator("iframe").first
    assert iframe.get_attribute("src") == embed_src
    assert iframe.get_attribute("referrerpolicy") == "strict-origin-when-cross-origin"
    assert iframe.get_attribute("title")
    assert "picture-in-picture" in (iframe.get_attribute("allow") or "")
    # The default navigation was prevented: the reader stays on the video page.
    assert page.url == base + "/" + VIDEO_PAGE

    # The rest of the page is still the page after the click.
    assert page.locator("h1").count() == 1
    assert page.locator(".transcript").count() == 1
    assert page.locator("[data-youtube-src]").count() == 0
    context.close()


def test_poster_link_opens_the_watch_page_without_javascript(video_site, browser):
    base = video_site
    context = browser.new_context(java_script_enabled=False)
    stub_watch_page(context)
    page = context.new_page()
    page.goto(base + "/" + VIDEO_PAGE, wait_until="domcontentloaded")
    assert page.locator("iframe").count() == 0
    facade = page.locator("[data-youtube-src]").first
    assert facade.count() == 1
    assert_opens_watch_page(context, facade)
    context.close()


def test_poster_link_opens_the_watch_page_when_the_module_is_missing(
    video_site, browser
):
    """An older cached module behaves exactly like a blocked one: no listener."""
    base = video_site
    context = browser.new_context()
    stub_watch_page(context)
    context.route("**/js/interactive.js*", lambda route: route.abort())
    page = context.new_page()
    page.goto(base + "/" + VIDEO_PAGE, wait_until="domcontentloaded")
    assert page.locator("iframe").count() == 0
    facade = page.locator("[data-youtube-src]").first
    assert facade.count() == 1
    assert_opens_watch_page(context, facade)
    context.close()
