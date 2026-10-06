"""Shared helpers for rendered-site pytest tests.

Serves a COPY of the built site (never the live checkout) over a local
ephemeral port using http.server in a daemon thread. Browser tests pytest.skip
cleanly when playwright, the chromium binary, or permission to bind a loopback
socket is unavailable locally; CI has all three (validate.yml browser-tests job).

The copy is served gzip-compressed, like GitHub Pages: text types are
compressed at level 5 (the zlib level whose output matches the Pages sizes for
the published files) whenever the client sends ``Accept-Encoding: gzip``, and
every response carries ``Vary: Accept-Encoding``. Measuring an uncompressed copy scores the
site far below its production Lighthouse results. ``compress=False`` restores
the identity transport.
"""

from __future__ import annotations

import functools
import gzip
import http.server
import io
import os
import re
import shutil
import threading
import urllib.parse
from http import HTTPStatus
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

# GitHub Pages compresses text responses of any size, plus SVG and ICO
# (verified: ``favicon.ico`` is served ``Content-Encoding: gzip``); raster images
# other than icons are never compressed. Python maps ``.js`` to text/javascript
# (3.12+) or application/javascript (older mimetypes tables) and ``.ico`` to
# image/x-icon or image/vnd.microsoft.icon (platform mime tables differ), so
# both spellings of each are listed.
GZIP_CONTENT_TYPES = frozenset({
    "text/html",
    "text/css",
    "text/plain",
    "text/xml",
    "text/javascript",
    "application/javascript",
    "application/json",
    "application/manifest+json",
    "application/xml",
    "image/svg+xml",
    "image/x-icon",
    "image/vnd.microsoft.icon",
})
# zlib level 5 matches the GitHub Pages gzip sizes for the published files
# (identical for most, within 1% for the rest).
GZIP_LEVEL = 5
_QVALUE = re.compile(r"(?:0(?:\.\d{0,3})?|1(?:\.0{0,3})?)")


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
        elif item.is_dir() and item.name in {"css", "js", "data", "works", "videos", "artworks", "assets"}:
            shutil.copytree(item, site / item.name)
    for relative in PWA_ICON_FILES:
        target = site / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / relative, target)
    return site


def accepts_gzip(header: str | None) -> bool:
    """True when an ``Accept-Encoding`` value permits a gzip response (RFC 9110).

    ``gzip``/``x-gzip`` need a positive q-value; an explicit coding overrides
    ``*``; a malformed q-value rejects the coding.
    """
    if not header:
        return False
    explicit: float | None = None
    wildcard: float | None = None
    for item in header.split(","):
        coding, _, parameters = item.partition(";")
        coding = coding.strip().lower()
        if coding not in {"gzip", "x-gzip", "*"}:
            continue
        quality = 1.0
        for parameter in parameters.split(";"):
            name, _, value = parameter.partition("=")
            if name.strip().lower() == "q":
                value = value.strip()
                quality = float(value) if _QVALUE.fullmatch(value) else 0.0
        if coding == "*":
            wildcard = quality if wildcard is None else max(wildcard, quality)
        else:
            explicit = quality if explicit is None else max(explicit, quality)
    chosen = explicit if explicit is not None else wildcard
    return chosen is not None and chosen > 0


class FixtureHandler(http.server.SimpleHTTPRequestHandler):
    """Quiet static handler that gzips text responses like GitHub Pages.

    Only plain 200 file responses are compressed: redirects, 404s and directory
    listings fall through to the stock handler untouched.

    Requests carrying ``If-Modified-Since``, ``If-None-Match`` or ``Range`` are
    also served by the stock handler, uncompressed: ``SimpleHTTPRequestHandler``
    answers them from the raw file (a 304 when the file is unchanged, otherwise
    the full identity body, since it ignores ``Range``), and re-deriving those
    semantics for a gzipped representation is not worth the code. This does not
    distort measurements. A fresh browser context, which is what Lighthouse and
    the Playwright suite use, never sends these headers on its first request for
    a URL, so every measured load is compressed; a real revalidation of an
    unchanged file still yields ``304 Not Modified``, which has no body to
    compress. ``Vary: Accept-Encoding`` is sent on every response regardless.
    """

    compress = True

    def log_message(self, format, *args):  # noqa: A002 - signature of the base class
        return None

    def end_headers(self) -> None:
        if self.compress:
            self.send_header("Vary", "Accept-Encoding")
        super().end_headers()

    def _gzip_target(self) -> tuple[str, str] | None:
        """Return (file path, Content-Type) when this request is served gzipped."""
        if not self.compress or not accepts_gzip(self.headers.get("Accept-Encoding")):
            return None
        if any(name in self.headers for name in ("If-Modified-Since", "If-None-Match", "Range")):
            return None
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            # Redirects (no trailing slash) and listings stay with the parent.
            if not urllib.parse.urlsplit(self.path).path.endswith("/"):
                return None
            for index in getattr(self, "index_pages", ("index.html", "index.htm")):
                candidate = os.path.join(path, index)
                if os.path.isfile(candidate):
                    path = candidate
                    break
            else:
                return None
        if path.endswith("/") or not os.path.isfile(path):
            return None
        content_type = self.guess_type(path)
        if content_type.partition(";")[0].strip().lower() not in GZIP_CONTENT_TYPES:
            return None
        return path, content_type

    def send_head(self):
        target = self._gzip_target()
        if target is None:
            return super().send_head()
        path, content_type = target
        try:
            with open(path, "rb") as source:
                modified = os.fstat(source.fileno()).st_mtime
                raw = source.read()
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None
        body = gzip.compress(raw, compresslevel=GZIP_LEVEL, mtime=0)
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", content_type)
        self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Last-Modified", self.date_time_string(modified))
        self.end_headers()
        # do_GET copies this stream to the client; do_HEAD closes it unread,
        # so HEAD reports the compressed length and sends no body.
        return io.BytesIO(body)


class PlainFixtureHandler(FixtureHandler):
    """The identity transport: no compression, no ``Vary`` header."""

    compress = False


def make_handler(site_dir: Path, *, compress: bool = True) -> functools.partial:
    """Request-handler factory serving ``site_dir`` (gzip unless ``compress=False``)."""
    handler = FixtureHandler if compress else PlainFixtureHandler
    return functools.partial(handler, directory=str(site_dir))


def serve_site(site_dir: Path, *, compress: bool = True) -> tuple[str, object]:
    """Serve ``site_dir`` on an ephemeral local port. Returns (base_url, httpd)."""
    handler = make_handler(site_dir, compress=compress)

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


def serve_copy(tmp_path: Path, *, compress: bool = True) -> tuple[str, object]:
    """Copy the built site into tmp_path and serve it. Caller must stop server."""
    return serve_site(copy_site(tmp_path), compress=compress)


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
