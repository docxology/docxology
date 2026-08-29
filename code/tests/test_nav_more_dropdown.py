"""Dropdown behavior: details.nav-more closes on outside click and Escape."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from rendered_site_fixture import serve_copy, stop_server  # noqa: E402


def test_nav_more_closes_on_outside_click_and_escape(tmp_path: Path) -> None:
    from playwright.sync_api import sync_playwright

    from rendered_site_fixture import skip_without_playwright

    skip_without_playwright()
    base_url, httpd = serve_copy(tmp_path)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_context(viewport={"width": 1280, "height": 900}).new_page()
            for path in ("index.html", "publications.html"):
                page.goto(f"{base_url}/{path}", wait_until="load")
                page.wait_for_timeout(200)
                more = page.locator("details.nav-more")
                if more.count() == 0:
                    continue
                more.first.click()
                assert more.first.get_attribute("open") is not None, f"{path}: dropdown did not open"
                page.mouse.click(10, 500)
                page.wait_for_timeout(200)
                assert more.first.get_attribute("open") is None, f"{path}: outside click did not close dropdown"
                more.first.click()
                page.keyboard.press("Escape")
                page.wait_for_timeout(200)
                assert more.first.get_attribute("open") is None, f"{path}: Escape did not close dropdown"
            browser.close()
    finally:
        stop_server(httpd)
