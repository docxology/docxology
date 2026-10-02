"""Shared helpers for rendered-site pytest tests.

Serves a COPY of the built site (never the live checkout) over a local
ephemeral port using http.server in a daemon thread. Browser tests pytest.skip
cleanly when playwright, the chromium binary, or permission to bind a loopback
socket is unavailable locally; CI has all three (validate.yml browser-tests job).
"""

from __future__ import annotations

import functools
import http.server
import os
import shutil
import threading
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
AXE_JS = REPO_ROOT / "code" / "tools" / "vendor" / "axe.min.js"

# The 8 lane pages exercised by the rendered browser suite.
LANE_PAGES = (
    "index.html",
    "publications.html",
    "art.html",
    "videos.html",
    "search.html",
    "404.html",
    "works/Friedman2015CommentaryPortugueseCryptoJews106.html",
    "videos/institute--39CESDAfLM.html",
)

NAV_VIEWPORTS = (900, 1024, 1152, 1280, 1440, 1920)
ROOT_RUNTIME_FILES = frozenset({
    "style.css", "favicon.ico", "robots.txt", "sitemap.xml",
    "manifest.json", "sw.js", "opensearch.xml", "feed.xml",
})
PWA_ICON_FILES = ("art/favicon-192.png", "art/favicon-512.png")


def browser_qa_required() -> bool:
    return os.environ.get("DOCXOLOGY_REQUIRE_BROWSER_QA", "").lower() in {"1", "true"} or os.environ.get("GITHUB_JOB") == "browser-tests"


def unavailable_browser_capability(reason: str) -> None:
    """Missing local optional capabilities skip; mandatory hosted gates fail."""
    if browser_qa_required():
        pytest.fail(f"Required browser QA capability unavailable: {reason}")
    pytest.skip(reason)


def skip_without_playwright() -> None:
    """Require an installed executable, failing closed in the hosted browser job."""
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except Exception as exc:  # pragma: no cover - local env without playwright
        unavailable_browser_capability(f"playwright unavailable: {exc}")
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            if not p.chromium.executable_path or not Path(p.chromium.executable_path).is_file():
                raise RuntimeError("chromium executable missing")
            # Complete an actual API round trip before shutting down Playwright;
            # path access alone does not prove the browser can launch.
            browser = p.chromium.launch(headless=True)
            browser.close()
    except Exception as exc:  # pragma: no cover - chromium not installed
        unavailable_browser_capability(f"chromium unavailable: {exc}")


def copy_site(tmp_path: Path) -> Path:
    """Copy rendered pages and their actual runtime exports into tmp_path/site.

    Keep root selection bounded; a page without its search/worker/PWA exports
    is an incomplete application and cannot supply representative browser QA.
    """
    site = tmp_path / "site"
    site.mkdir(parents=True, exist_ok=True)
    for item in sorted(REPO_ROOT.iterdir()):
        if item.suffix == ".html":
            shutil.copy2(item, site / item.name)
        elif item.is_file() and (item.name in ROOT_RUNTIME_FILES or item.match("search-index*.json")):
            shutil.copy2(item, site / item.name)
        elif item.is_dir() and item.name in {"css", "js", "data", "works", "videos", "assets"}:
            shutil.copytree(item, site / item.name)
    for relative in PWA_ICON_FILES:
        target = site / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / relative, target)
    return site


def serve_site(site_dir: Path) -> tuple[str, object]:
    """Serve ``site_dir`` on an ephemeral local port. Returns (base_url, httpd)."""
    handler = type(
        "QuietHandler",
        (http.server.SimpleHTTPRequestHandler,),
        {"log_message": lambda self, *args: None},
    )
    handler = functools.partial(handler, directory=str(site_dir))

    class _Server(http.server.ThreadingHTTPServer):
        def __init__(self, directory: Path) -> None:
            super().__init__(("127.0.0.1", 0), handler)
            self._directory = directory

    try:
        httpd = _Server(site_dir)
    except PermissionError as exc:
        # A sandbox that forbids binding a loopback socket is a missing local
        # capability, exactly like a missing chromium binary — not a site
        # defect. Only EACCES/EPERM is treated this way: an address already in
        # use, a missing directory, or any other OSError still fails the test.
        unavailable_browser_capability(f"local HTTP server not permitted in this environment: {exc}")
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    return f"http://127.0.0.1:{httpd.server_address[1]}", httpd


def serve_copy(tmp_path: Path) -> tuple[str, object]:
    """Copy the built site into tmp_path and serve it. Caller must stop server."""
    return serve_site(copy_site(tmp_path))


def stop_server(httpd: object) -> None:
    httpd.shutdown()  # type: ignore[attr-defined]
    httpd.server_close()  # type: ignore[attr-defined]


def page_and_server(tmp_path: Path):
    """Yield (page, base_url, httpd) for one playwright chromium page."""
    skip_without_playwright()
    from playwright.sync_api import sync_playwright

    base_url, httpd = serve_copy(tmp_path)
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    # Ordinary interaction QA inspects direct responses; worker lifecycle is
    # explicitly enabled only in its dedicated real-browser acceptance tests.
    context = browser.new_context(viewport={"width": 1280, "height": 900}, service_workers="block")
    page = context.new_page()
    try:
        yield page, base_url, httpd
    finally:
        context.close()
        browser.close()
        pw.stop()
        stop_server(httpd)
