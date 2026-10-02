"""Real first-paint geometry with delayed or unavailable navigation scripts."""
from __future__ import annotations

import shutil
import sys
import time
from pathlib import Path
from urllib.parse import urlsplit

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import REPO_ROOT, serve_site, skip_without_playwright, stop_server  # noqa: E402


@pytest.fixture
def navigation_site(tmp_path):
    """Serve real generated lane bytes with their actual local dependencies."""
    skip_without_playwright()
    site = tmp_path / "site"
    site.mkdir()
    for name in ("index.html", "publications.html", "style.css", "favicon.ico", "manifest.json"):
        shutil.copy2(REPO_ROOT / name, site / name)
    for name in ("js", "data"):
        shutil.copytree(REPO_ROOT / name, site / name)
    for name in ("index.html", "publications.html"):
        source = (site / name).read_text(encoding="utf-8")
        head = source.split("</head>", 1)[0]
        assert 'src="/js/nav-toggle.js?' in head, "Regenerate the real head initializer first"
        assert source.count("/js/nav-toggle.js") == 1
    base, server = serve_site(site)
    try:
        yield base
    finally:
        stop_server(server)


FRAME_PROBE = """(() => {
  window.__navFrames = [];
  window.__navCLS = 0;
  new PerformanceObserver(list => {
    for (const entry of list.getEntries()) {
      if (!entry.hadRecentInput) window.__navCLS += entry.value;
    }
  }).observe({type: 'layout-shift', buffered: true});
  function sample() {
    const nav = document.querySelector('nav');
    const main = document.querySelector('main, .hero, .page-hero');
    if (nav && main) window.__navFrames.push({
      y: main.getBoundingClientRect().top + window.scrollY,
      enhanced: nav.classList.contains('nav-enhanced'),
      wired: nav.querySelector('.menu-btn')?.dataset.navToggleWired === 'true'
    });
    requestAnimationFrame(sample);
  }
  requestAnimationFrame(sample);
})();"""


@pytest.mark.parametrize("head_mode, interactive_mode", [
    ("normal", "delayed"),
    ("delayed", "blocked"),
    ("blocked", "delayed"),
])
@pytest.mark.parametrize("route", ["index.html", "publications.html"])
def test_mobile_first_paint_never_waits_for_a_later_navigation_owner(
    navigation_site, head_mode, interactive_mode, route,
):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 320, "height": 760}, service_workers="block")
        page = context.new_page()
        page.add_init_script(FRAME_PROBE)

        def route_script(route):
            path = urlsplit(route.request.url).path
            mode = head_mode if path == "/js/nav-toggle.js" else interactive_mode
            if mode == "blocked":
                route.abort()
            else:
                if mode == "delayed":
                    time.sleep(0.7)
                route.continue_()

        page.route("**/js/nav-toggle.js*", route_script)
        page.route("**/js/interactive.js*", route_script)
        response = page.goto(navigation_site + "/" + route, wait_until="load")
        assert response.status == 200
        assert response.body() == (REPO_ROOT / route).read_bytes()
        page.wait_for_timeout(150)
        frames = page.evaluate("window.__navFrames")
        assert len(frames) >= 2, frames
        assert max(frame["y"] for frame in frames) - min(frame["y"] for frame in frames) <= 1, {
            "frames": frames, "observed_CLS": page.evaluate("window.__navCLS"),
        }
        if head_mode == "blocked":
            assert all(not frame["enhanced"] and not frame["wired"] for frame in frames), frames
            links = page.locator(".nav-links > li > a")
            assert links.count() >= 6
            assert all(link.is_visible() for link in links.all())
            assert not page.locator(".menu-btn").is_visible()
        else:
            assert all(frame["enhanced"] and frame["wired"] for frame in frames), frames
            button = page.locator(".menu-btn")
            links = page.locator(".nav-links")
            assert button.get_attribute("aria-expanded") == "false"
            assert not links.is_visible()
            button.click()
            assert links.is_visible() and button.get_attribute("aria-expanded") == "true"
            # A loaded index-page.js must not flip aria-expanded independently.
            button.click()
            assert not links.is_visible() and button.get_attribute("aria-expanded") == "false"
            button.click()
            page.keyboard.press("Escape")
            assert not links.is_visible() and button.get_attribute("aria-expanded") == "false"
            assert button.evaluate("node => node === document.activeElement")
        context.close()
        browser.close()
