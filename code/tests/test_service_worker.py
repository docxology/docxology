"""Actual Chromium worker lifecycle, network-error, and bounded-cache acceptance.

The production worker and shell assets run against a mutable loopback server.
These checks use real HTTP 404/500 responses and Chromium's offline transport,
not mocked Cache/Fetch APIs. All fixture changes stay in tmp_path.
"""
from __future__ import annotations

import http.server
import json
import re
import sys
import threading
import time
from pathlib import Path
from urllib.parse import urlsplit

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import REPO_ROOT, skip_without_playwright, stop_server, unavailable_browser_capability  # noqa: E402

WORKER_SOURCE = (REPO_ROOT / "sw.js").read_text(encoding="utf-8")
SHELL_ASSETS = re.findall(r"'([^']+)'", re.search(r"const STATIC_ASSETS = \[(.*?)\];", WORKER_SOURCE, re.S).group(1))
RUNTIME_CACHE = "daf-portfolio-runtime-v1"


def test_service_worker_install_downloads_only_small_shell():
    assert not any(path.startswith("/data/") or "search-index" in path for path in SHELL_ASSETS)
    shell_bytes = sum((REPO_ROOT / (path.lstrip("/") or "index.html")).stat().st_size for path in SHELL_ASSETS)
    assert shell_bytes < 320 * 1024, f"Offline shell grew to {shell_bytes:,} raw bytes"


@pytest.fixture
def worker_server(tmp_path):
    # Each entry is status, bytes, content type, optional response headers.
    routes = {}
    for path in SHELL_ASSETS:
        source = REPO_ROOT / (path.lstrip("/") or "index.html")
        mime = "text/javascript" if source.suffix == ".js" else "text/css" if source.suffix == ".css" else "application/json" if source.suffix == ".json" else "text/html"
        routes[path] = (200, source.read_bytes(), mime, {})
    routes["/"] = routes["/index.html"] = (200, b"<!doctype html><html lang='en'><title>Shell one</title><h1>Shell one</h1></html>", "text/html", {})
    routes["/sw.js"] = (200, WORKER_SOURCE.encode(), "text/javascript", {"Cache-Control": "no-store"})
    requested = []

    class Handler(http.server.BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_GET(self):
            path = urlsplit(self.path).path
            requested.append(path)
            status, body, mime, headers = routes.get(path, (404, b"missing", "text/plain", {}))
            time.sleep(headers.get("_header_delay", 0))
            self.send_response(status)
            self.send_header("Content-Type", mime)
            if not headers.get("_omit_length"):
                self.send_header("Content-Length", str(len(body)))
            for key, value in headers.items():
                if not key.startswith("_"):
                    self.send_header(key, value)
            self.end_headers()
            try:
                chunk_bytes = headers.get("_chunk_bytes", len(body) or 1)
                for offset in range(0, len(body), chunk_bytes):
                    self.wfile.write(body[offset:offset + chunk_bytes])
                    self.wfile.flush()
                    time.sleep(headers.get("_chunk_delay", 0))
            except (BrokenPipeError, ConnectionResetError):
                pass  # The worker's deadline deliberately cancels this transport.

    try:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    except PermissionError as exc:
        unavailable_browser_capability(f"local HTTP server not permitted: {exc}")
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_address[1]}", routes, requested
    stop_server(server)


def install_worker(page, base):
    page.goto(base + "/", wait_until="load")
    page.evaluate("async () => { await navigator.serviceWorker.register('/sw.js'); await navigator.serviceWorker.ready; }")
    page.wait_for_function("navigator.serviceWorker.controller !== null")


def fetch_resource(page, path, headers=None):
    return page.evaluate("""async ({path, headers}) => {
      const response = await fetch(path, {headers, cache: 'no-store'});
      return {status: response.status, type: response.headers.get('content-type'), text: await response.text()};
    }""", {"path": path, "headers": headers or {}})


def wait_cached(page, path, text):
    page.wait_for_function("""async ({cache, path, text}) => {
      const response = await (await caches.open(cache)).match(path);
      return response && (await response.text()) === text;
    }""", arg={"cache": RUNTIME_CACHE, "path": path, "text": text})


def update_worker(page):
    return page.evaluate("""async () => {
      const registration = await navigator.serviceWorker.getRegistration();
      const previous = registration.active;
      const terminalState = new Promise(resolve => registration.addEventListener('updatefound', () => {
        const worker = registration.installing;
        worker.addEventListener('statechange', () => {
          if (['activated', 'redundant'].includes(worker.state)) resolve(worker.state);
        });
      }, {once: true}));
      await registration.update();
      const state = await terminalState;
      return {state, sameActive: registration.active === previous};
    }""")


def test_worker_offline_fallback_error_poisoning_and_bounded_cache(worker_server):
    skip_without_playwright()
    from playwright.sync_api import sync_playwright

    base, routes, requested = worker_server
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(service_workers="allow")
        page = context.new_page()
        try:
            install_worker(page, base)
            assert not any(path.startswith("/data/") or "search-index" in path for path in requested)
            routes["/visited.html"] = (200, b"<h1>Saved paper</h1>", "text/html", {})
            page.goto(base + "/visited.html")
            wait_cached(page, "/visited.html", "<h1>Saved paper</h1>")
            routes["/data/sample.json"] = (200, b'{"value":"saved"}', "application/json", {})
            assert fetch_resource(page, "/data/sample.json")["status"] == 200
            wait_cached(page, "/data/sample.json", '{"value":"saved"}')
            for status in (404, 500):
                routes["/visited.html"] = (status, b"server error", "text/html", {})
                assert page.goto(base + "/visited.html").status == 200
                assert page.locator("h1").inner_text() == "Saved paper"
                routes["/data/sample.json"] = (status, b'{"error":"server"}', "application/json", {})
                assert fetch_resource(page, "/data/sample.json")["text"] == '{"value":"saved"}'
            routes["/data/uncached-error.json"] = (500, b'{"error":"server"}', "application/json", {})
            assert fetch_resource(page, "/data/uncached-error.json")["status"] == 500

            context.set_offline(True)
            assert page.goto(base + "/visited.html").status == 200
            assert page.locator("h1").inner_text() == "Saved paper"
            assert fetch_resource(page, "/data/sample.json")["text"] == '{"value":"saved"}'
            missing = fetch_resource(page, "/data/uncached-error.json")
            assert missing["status"] == 503 and missing["type"].startswith("application/json")
            assert json.loads(missing["text"])["error"] == "offline"
            assert page.goto(base + "/never-visited.html").status == 503
            assert page.locator("h1").inner_text() == "This page is unavailable offline"

            context.set_offline(False)
            # Leave the intentionally restrictive offline fallback document.
            page.goto(base + "/visited.html")
            routes["/data/large.json"] = (200, b"x" * (2 * 1024 * 1024 + 1), "application/json", {})
            routes["/data/private.json"] = (200, b"not retained", "application/json", {"Cache-Control": "no-store"})
            routes["/source.pdf"] = (200, b"source document", "application/pdf", {})
            routes["/data/range.json"] = (200, b"partial request", "application/json", {})
            for path in ("/data/large.json", "/data/private.json", "/source.pdf"):
                assert fetch_resource(page, path)["status"] == 200
            routes["/data/oversized-stream.json"] = (200, b"x" * (16 * 1024 * 1024 + 1), "application/json", {"_omit_length": True})
            assert fetch_resource(page, "/data/oversized-stream.json")["status"] == 503
            assert fetch_resource(page, "/data/range.json", {"Range": "bytes=0-7"})["status"] == 200
            # A sentinel successful write orders the worker's serialized cache queue.
            for index in range(52):
                path, body = f"/data/item-{index}.json", str(index)
                routes[path] = (200, body.encode(), "application/json", {})
                fetch_resource(page, path)
                wait_cached(page, path, body)
            paths = page.evaluate("async cache => (await (await caches.open(cache)).keys()).map(r => new URL(r.url).pathname)", RUNTIME_CACHE)
            assert len(paths) <= 48
            assert "/data/item-0.json" not in paths and "/data/item-51.json" in paths
            assert not set(paths) & {"/data/large.json", "/data/private.json", "/source.pdf", "/data/range.json", "/data/uncached-error.json", "/data/oversized-stream.json"}
        finally:
            context.close()
            browser.close()


def test_worker_updates_returning_visitors_and_preserves_prior_install_on_failure(worker_server):
    skip_without_playwright()
    from playwright.sync_api import sync_playwright

    base, routes, _ = worker_server
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(service_workers="allow")
        page = context.new_page()
        try:
            install_worker(page, base)
            routes["/visited.html"] = (200, b"<h1>Saved before update</h1>", "text/html", {})
            page.goto(base + "/visited.html")
            wait_cached(page, "/visited.html", "<h1>Saved before update</h1>")
            routes["/probe.css"] = (200, b"body{color:blue}", "text/css", {})
            fetch_resource(page, "/probe.css")
            wait_cached(page, "/probe.css", "body{color:blue}")
            routes["/probe.css"] = (200, b"body{color:black}", "text/css", {})
            assert fetch_resource(page, "/probe.css")["text"] == "body{color:blue}"
            wait_cached(page, "/probe.css", "body{color:black}")
            page.close()
            page = context.new_page()
            page.goto(base + "/visited.html")
            assert fetch_resource(page, "/probe.css")["text"] == "body{color:black}"
            page.evaluate("caches.open('unrelated-app-cache')")

            updated = re.sub(r"const CACHE_NAME = '[^']+';", "const CACHE_NAME = 'daf-portfolio-test-update';", WORKER_SOURCE)
            routes["/sw.js"] = (200, updated.encode(), "text/javascript", {"Cache-Control": "no-store"})
            assert update_worker(page) == {"state": "activated", "sameActive": False}
            names = page.evaluate("caches.keys()")
            assert "daf-portfolio-test-update-shell" in names
            assert "unrelated-app-cache" in names
            assert not any(name.endswith("-shell") and name != "daf-portfolio-test-update-shell" for name in names)
            context.set_offline(True)
            assert page.goto(base + "/visited.html").status == 200
            assert page.locator("h1").inner_text() == "Saved before update"
            context.set_offline(False)
            routes["/visited.html"] = (200, b"<h1>Fresh after update</h1>", "text/html", {})
            page.goto(base + "/visited.html")
            wait_cached(page, "/visited.html", "<h1>Fresh after update</h1>")
            assert page.locator("h1").inner_text() == "Fresh after update"

            broken = updated.replace("daf-portfolio-test-update'", "daf-portfolio-test-broken'")
            routes["/sw.js"] = (200, broken.encode(), "text/javascript", {"Cache-Control": "no-store"})
            routes["/js/menu-esc.js"] = (500, b"unavailable shell file", "text/javascript", {})
            assert update_worker(page) == {"state": "redundant", "sameActive": True}
            context.set_offline(True)
            assert page.goto(base + "/visited.html").status == 200
            assert page.locator("h1").inner_text() == "Fresh after update"
            context.set_offline(False)
            stalled = updated.replace("daf-portfolio-test-update'", "daf-portfolio-test-stalled'")
            stalled = stalled.replace("const NETWORK_HEADER_TIMEOUT_MS = 5000;", "const NETWORK_HEADER_TIMEOUT_MS = 500;")
            stalled = stalled.replace("const NETWORK_BODY_TIMEOUT_MS = 25000;", "const NETWORK_BODY_TIMEOUT_MS = 500;")
            routes["/sw.js"] = (200, stalled.encode(), "text/javascript", {"Cache-Control": "no-store"})
            routes["/js/menu-esc.js"] = (200, b"/* incomplete slow shell script */", "text/javascript", {"_chunk_bytes": 1, "_chunk_delay": 0.1})
            started = time.monotonic()
            assert update_worker(page) == {"state": "redundant", "sameActive": True}
            assert time.monotonic() - started < 2.0
            names = page.evaluate("caches.keys()")
            assert "daf-portfolio-test-stalled-shell" not in names
            assert "daf-portfolio-test-update-shell" in names
            context.set_offline(True)
            assert page.goto(base + "/visited.html").status == 200
            assert page.locator("h1").inner_text() == "Fresh after update"
        finally:
            context.close()
            browser.close()


def test_worker_deadline_covers_delayed_headers_and_slow_body(worker_server):
    skip_without_playwright()
    from playwright.sync_api import sync_playwright

    base, routes, _ = worker_server
    # Shorten only the declared duration in this served copy; production logic
    # and real browser/HTTP streams remain unchanged.
    worker = WORKER_SOURCE.replace("const NETWORK_HEADER_TIMEOUT_MS = 5000;", "const NETWORK_HEADER_TIMEOUT_MS = 500;")
    worker = worker.replace("const NETWORK_BODY_TIMEOUT_MS = 25000;", "const NETWORK_BODY_TIMEOUT_MS = 1000;")
    assert worker != WORKER_SOURCE
    routes["/sw.js"] = (200, worker.encode(), "text/javascript", {"Cache-Control": "no-store"})
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(service_workers="allow")
        page = context.new_page()
        try:
            install_worker(page, base)
            routes["/data/saved.json"] = (200, b'{"value":"complete"}', "application/json", {})
            fetch_resource(page, "/data/saved.json")
            wait_cached(page, "/data/saved.json", '{"value":"complete"}')
            # A legitimate body may take longer than the header window while
            # completing within the separate body window.
            routes["/data/mobile-complete.json"] = (200, b'{"ok":true}', "application/json", {"_chunk_bytes": 1, "_chunk_delay": 0.065})
            assert fetch_resource(page, "/data/mobile-complete.json")["status"] == 200
            wait_cached(page, "/data/mobile-complete.json", '{"ok":true}')
            for path, headers in (
                ("/data/delayed-headers.json", {"_header_delay": 1.5}),
                ("/data/slow-body.json", {"_chunk_bytes": 1, "_chunk_delay": 0.1}),
                ("/data/saved.json", {"_chunk_bytes": 1, "_chunk_delay": 0.1}),
            ):
                routes[path] = (200, b'{"value":"incomplete network response"}', "application/json", headers)
                started = time.monotonic()
                response = fetch_resource(page, path)
                elapsed = time.monotonic() - started
                assert 0.3 <= elapsed < 2.0, (path, elapsed)
                if path == "/data/saved.json":
                    assert response["status"] == 200 and response["text"] == '{"value":"complete"}'
                else:
                    assert response["status"] == 503 and json.loads(response["text"])["error"] == "offline"
            # Successful writes prove the expired streams no longer block the
            # worker's event/cache queue, and incomplete bodies never entered it.
            routes["/data/sentinel.json"] = (200, b"complete", "application/json", {})
            fetch_resource(page, "/data/sentinel.json")
            wait_cached(page, "/data/sentinel.json", "complete")
            paths = page.evaluate("async cache => (await (await caches.open(cache)).keys()).map(r => new URL(r.url).pathname)", RUNTIME_CACHE)
            assert "/data/slow-body.json" not in paths and "/data/delayed-headers.json" not in paths
            wait_cached(page, "/data/saved.json", '{"value":"complete"}')
        finally:
            context.close()
            browser.close()
