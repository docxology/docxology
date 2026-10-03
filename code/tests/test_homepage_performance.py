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
