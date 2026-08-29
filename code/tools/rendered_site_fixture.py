"""Shared helpers for rendered-site pytest tests.

Serves a COPY of the built site (never the live checkout) over a local
ephemeral port using http.server in a daemon thread. Browser tests pytest.skip
cleanly when playwright or the chromium binary is unavailable locally; CI
installs them (validate.yml browser-tests job).
"""

from __future__ import annotations

import functools
import http.server
import shutil
import threading
import time
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


def skip_without_playwright() -> None:
    """pytest.skip when playwright or the chromium binary is unavailable."""
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except Exception as exc:  # pragma: no cover - local env without playwright
        pytest.skip(f"playwright unavailable: {exc}")
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            if not p.chromium.executable_path:
                raise RuntimeError("chromium executable missing")
    except Exception as exc:  # pragma: no cover - chromium not installed
        pytest.skip(f"chromium unavailable: {exc}")


def copy_site(tmp_path: Path) -> Path:
    """Copy the rendered site (html pages + asset dirs) into tmp_path/site."""
    site = tmp_path / "site"
    site.mkdir(parents=True, exist_ok=True)
    for item in sorted(REPO_ROOT.iterdir()):
        if item.suffix == ".html":
            shutil.copy2(item, site / item.name)
        elif item.is_file() and item.name in {"style.css", "favicon.ico", "robots.txt", "sitemap.xml"}:
            shutil.copy2(item, site / item.name)
        elif item.is_dir() and item.name in {"css", "js", "data", "works", "videos", "assets"}:
            shutil.copytree(item, site / item.name)
    return site


def serve_site(site_dir: Path) -> tuple[str, object]:
    """Serve ``site_dir`` on an ephemeral local port. Returns (base_url, httpd)."""
    import http.server

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

    httpd = _Server(site_dir)
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
    context = browser.new_context(viewport={"width": 1280, "height": 900})
    page = context.new_page()
    try:
        yield page, base_url, httpd
    finally:
        context.close()
        browser.close()
        pw.stop()
        stop_server(httpd)
