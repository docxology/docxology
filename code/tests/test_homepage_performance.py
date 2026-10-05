"""Decorative CSS images must not compete with the homepage's content."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import serve_copy, skip_without_playwright, stop_server  # noqa: E402


@pytest.mark.parametrize("path", ["index.html", "publications.html"])
def test_content_pages_avoid_eager_decorative_image_requests(tmp_path, path):
    skip_without_playwright()
    from playwright.sync_api import sync_playwright

    base, server = serve_copy(tmp_path)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 412, "height": 900}, service_workers="block")
            requests = []
            page.on("request", lambda request: requests.append(request.url))
            page.goto(base + "/" + path, wait_until="load")
            assert not any("/hero-art/" in url for url in requests)
            if path == "index.html":
                assert page.locator(".hero h1").is_visible()
                assert page.locator(".card").count() > 15
                assert page.locator(".curio-card img").count() == 3
                assert page.locator(".curio-card").evaluate_all("cards => cards.every(card => !getComputedStyle(card, '::before').backgroundImage.includes('url('))")
            else:
                page.wait_for_function("() => document.getElementById('pub-load-more') && document.getElementById('pub-table').getAttribute('aria-busy') === 'false'")
                assert page.locator(".page-hero h1").is_visible()
                assert page.locator("#pub-tbody tr").count() == 50
                assert page.locator("#pub-tbody .td-title a").first.is_visible()
                assert page.locator(".page-hero").evaluate("hero => !getComputedStyle(hero, '::after').backgroundImage.includes('url(')")
            browser.close()
    finally:
        stop_server(server)


def test_optional_hero_canvas_is_static_under_reduced_motion_and_reacts_to_preference_changes(tmp_path):
    skip_without_playwright()
    from playwright.sync_api import sync_playwright

    # The current homepage does not mount this optional effect. Exercise its
    # reusable module on an explicit, disposable fixture with native assets.
    base, server = serve_copy(tmp_path)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 412, 'height': 900}, reduced_motion='reduce', service_workers='block')
            page.add_init_script('''window.heroDraws = 0;
const originalDrawImage = CanvasRenderingContext2D.prototype.drawImage;
CanvasRenderingContext2D.prototype.drawImage = function (...args) {
    if (this.canvas.matches('.hero-glitch-canvas')) window.heroDraws++;
    return originalDrawImage.apply(this, args);
};''')
            page.route('**/hero-motion-fixture.html', lambda route: route.fulfill(content_type='text/html', body='''<!doctype html>
<html lang="en"><head><title>Public hero motion fixture</title></head><body>
<header class="hero" style="height:240px;width:100%"><canvas class="hero-glitch-canvas" aria-hidden="true"></canvas><a href="index.html">Home</a></header>
<script type="module" src="js/hero-glitch.js"></script></body></html>'''))
            requests = []
            page.on('request', lambda request: requests.append(request.url))
            page.goto(base + '/hero-motion-fixture.html')
            page.wait_for_function('() => window.heroDraws > 0')
            before = page.evaluate('() => ({draws:window.heroDraws,image:document.querySelector("canvas").toDataURL()})')
            page.mouse.move(200, 120)
            page.wait_for_timeout(900)  # Covers the former reduced-motion 700ms loop.
            after = page.evaluate('() => ({draws:window.heroDraws,image:document.querySelector("canvas").toDataURL()})')
            assert after == before
            assert [url for url in requests if '/hero-art/' in url] == [base + '/assets/hero-art/ant-head.webp']
            page.emulate_media(reduced_motion='no-preference')
            page.wait_for_function('(count) => window.heroDraws > count + 5', arg=before['draws'])
            page.wait_for_function('() => performance.getEntriesByType("resource").filter(entry => entry.name.includes("/hero-art/")).length === 5')
            page.emulate_media(reduced_motion='reduce')
            page.wait_for_timeout(100)
            paused = page.evaluate('() => ({draws:window.heroDraws,image:document.querySelector("canvas").toDataURL()})')
            page.mouse.move(20, 30)
            page.wait_for_timeout(900)
            assert page.evaluate('() => ({draws:window.heroDraws,image:document.querySelector("canvas").toDataURL()})') == paused
            page.set_viewport_size({'width': 430, 'height': 900})
            page.wait_for_function('(count) => window.heroDraws > count', arg=paused['draws'])
            resized = page.evaluate('() => window.heroDraws')
            page.wait_for_timeout(900)
            assert page.evaluate('() => window.heroDraws') == resized
            assert len([url for url in requests if '/hero-art/' in url]) == 5
            browser.close()
    finally:
        stop_server(server)
