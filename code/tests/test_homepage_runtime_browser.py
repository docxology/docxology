"""Homepage script execution and service worker registration."""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import REPO_ROOT, serve_site, stop_server  # noqa: E402

pytestmark = pytest.mark.browser

def test_homepage_registers_service_worker_without_runtime_errors(browser_runtime):
    from playwright.sync_api import sync_playwright

    base, server = serve_site(REPO_ROOT)
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("console", lambda message: errors.append(message.text) if message.type == "error" and "frame-ancestors" not in message.text else None)
            page.goto(base + "/index.html", wait_until="networkidle")
            page.wait_for_function("async () => (await navigator.serviceWorker.getRegistration('/'))?.active?.scriptURL.endsWith('/sw.js')")
            assert not errors, errors
            browser.close()
    finally:
        stop_server(server)
