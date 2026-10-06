"""The rendered-site fixture serves text gzip-compressed, like GitHub Pages.

Lighthouse and the rendered browser suite measure the fixture, so a copy served
without compression scores far below the production site (art 84 vs 99-100,
publications 76-85 vs 100). These tests drive the real request handler through
a fake connection: no socket, browser or Playwright is needed, so they run in
every environment. The loopback tests go through ``serve_site`` and skip
through the shared capability helper when binding is not permitted.
"""
from __future__ import annotations

import gzip
import functools
import http.client
import http.server
import io
import sys
import urllib.request
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import rendered_site_fixture as fixture  # noqa: E402
import test_lighthouse_budgets as gate  # noqa: E402 - the Lighthouse gzip-parity helper under test

REPEATED = "<p>Active Inference rendered fixture text, repeated so gzip shrinks it.</p>\n" * 200

TEXT_FILES = {
    "page.html": REPEATED,
    "style.css": "body { margin: 0; padding: 0; color: #111; }\n" * 200,
    "app.js": "const value = 1; console.log(value);\n" * 200,
    "data.json": '{"works": [' + ",".join(['{"title": "A work"}'] * 300) + "]}\n",
    "robots.txt": "User-agent: *\nAllow: /\n" * 100,
    "feed.xml": "<?xml version='1.0'?><feed>" + "<entry>one</entry>" * 300 + "</feed>\n",
    "icon.svg": "<svg xmlns='http://www.w3.org/2000/svg'>" + "<path d='M0 0h10v10z'/>" * 300 + "</svg>\n",
    "app.webmanifest": '{"name": "Site", "icons": [' + ",".join(['{"src": "/i.png"}'] * 300) + "]}\n",
}
# GitHub Pages serves favicon.ico with Content-Encoding: gzip (verified live).
ICON_FILES = {
    "favicon.ico": b"\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x20\x00" + b"\x00" * 4096,
}
# One asset of each type the pages load, at the paths the Lighthouse gate requests.
PARITY_FILES = {
    "index.html": REPEATED,
    "style.css": TEXT_FILES["style.css"],
    "js/interactive.js": TEXT_FILES["app.js"],
    "data/works.json": TEXT_FILES["data.json"],
}
BINARY_FILES = {
    "photo.png": b"\x89PNG\r\n\x1a\n" + b"\x00" * 4096,
    "document.pdf": b"%PDF-1.7\n" + b"0" * 4096,
    "photo.jpg": b"\xff\xd8\xff" + b"\x00" * 4096,
    "photo.webp": b"RIFF\x00\x00\x00\x00WEBP" + b"\x00" * 4096,
}


class _Connection:
    """Just enough of a socket for ``StreamRequestHandler`` to serve one request."""

    def __init__(self, request: bytes) -> None:
        self._request = request
        self.sent = bytearray()

    def makefile(self, mode: str, bufsize: int = -1):
        if "r" in mode:
            return io.BytesIO(self._request)
        return io.BytesIO()

    def sendall(self, data) -> None:
        self.sent += bytes(data)

    def settimeout(self, timeout) -> None:
        return None

    def close(self) -> None:
        return None


class _ResponseSocket:
    def __init__(self, payload: bytes) -> None:
        self._payload = payload

    def makefile(self, mode: str, bufsize: int = -1):
        return io.BytesIO(self._payload)


def served_type(name: str) -> str:
    """The Content-Type the handler would send for ``name``, without parameters."""
    handler = object.__new__(fixture.FixtureHandler)
    return handler.guess_type(name).partition(";")[0].strip().lower()


class _StockHandler(http.server.SimpleHTTPRequestHandler):
    """The unmodified standard-library handler, the reference for bypassed requests."""

    def log_message(self, format, *args):  # noqa: A002 - signature of the base class
        return None


def _drive(factory, path: str, headers: dict[str, str] | None, method: str) -> tuple[http.client.HTTPResponse, bytes]:
    """Run one request through a handler factory and parse the wire bytes."""
    lines = [f"{method} {path} HTTP/1.1", "Host: fixture.test"]
    lines += [f"{name}: {value}" for name, value in (headers or {}).items()]
    connection = _Connection(("\r\n".join(lines) + "\r\n\r\n").encode("ascii"))
    factory(connection, ("127.0.0.1", 0), None)
    response = http.client.HTTPResponse(_ResponseSocket(bytes(connection.sent)), method=method)
    response.begin()
    return response, response.read()


def fetch(site: Path, path: str, headers: dict[str, str] | None = None, *, method: str = "GET",
          compress: bool = True) -> tuple[http.client.HTTPResponse, bytes]:
    """Drive the real fixture handler for one request and parse the wire bytes."""
    return _drive(fixture.make_handler(site, compress=compress), path, headers, method)


def fetch_stock(site: Path, path: str, headers: dict[str, str] | None = None) -> tuple[http.client.HTTPResponse, bytes]:
    """The same request through the stock ``SimpleHTTPRequestHandler``."""
    return _drive(functools.partial(_StockHandler, directory=str(site)), path, headers, "GET")


@pytest.fixture
def site(tmp_path: Path) -> Path:
    root = tmp_path / "site"
    (root / "sub").mkdir(parents=True)
    (root / "empty").mkdir()
    for name, text in TEXT_FILES.items():
        (root / name).write_text(text, encoding="utf-8")
    for name, data in {**ICON_FILES, **BINARY_FILES}.items():
        (root / name).write_bytes(data)
    for name, text in PARITY_FILES.items():
        (root / name).parent.mkdir(exist_ok=True)
        (root / name).write_text(text, encoding="utf-8")
    (root / "sub" / "index.html").write_text(REPEATED + "sub", encoding="utf-8")
    return root


GZIP = {"Accept-Encoding": "gzip"}


@pytest.mark.parametrize(("header", "expected"), [
    (None, False),
    ("", False),
    ("identity", False),
    ("br", False),
    ("gzip", True),
    ("GZIP", True),
    ("x-gzip", True),
    ("gzip, deflate, br", True),
    ("deflate, gzip;q=0.5", True),
    ("gzip;q=1.0", True),
    ("gzip;q=0.001", True),
    ("gzip;q=0", False),
    ("gzip;q=0.000", False),
    ("gzip; q=0", False),
    ("gzip;q=banana", False),
    ("gzip;q=2", False),
    ("gzip;q=-1", False),
    ("*", True),
    ("*;q=0", False),
    ("gzip;q=0, *", False),
    ("gzip, *;q=0", True),
    ("br, *;q=0.1", True),
])
def test_accepts_gzip_follows_rfc_9110_codings(header, expected):
    assert fixture.accepts_gzip(header) is expected


def test_allow_list_covers_both_javascript_and_icon_types_but_no_raster_images():
    assert {"text/javascript", "application/javascript"} <= fixture.GZIP_CONTENT_TYPES
    assert {"text/html", "text/css", "text/plain", "text/xml", "application/xml", "application/json",
            "application/manifest+json", "image/svg+xml"} <= fixture.GZIP_CONTENT_TYPES
    # GitHub Pages gzips favicon.ico; platform mime tables name it either way.
    assert {"image/x-icon", "image/vnd.microsoft.icon"} <= fixture.GZIP_CONTENT_TYPES
    assert served_type("favicon.ico") in fixture.GZIP_CONTENT_TYPES
    images = {kind for kind in fixture.GZIP_CONTENT_TYPES if kind.startswith("image/")}
    assert images == {"image/svg+xml", "image/x-icon", "image/vnd.microsoft.icon"}
    assert fixture.GZIP_LEVEL == 5


@pytest.mark.parametrize("name", sorted(TEXT_FILES))
def test_text_types_are_gzipped_with_correct_headers(site, name):
    raw = (site / name).read_bytes()
    plain, plain_body = fetch(site, f"/{name}", compress=False)
    assert plain.getheader("Content-Encoding") is None and plain_body == raw
    response, body = fetch(site, f"/{name}", GZIP)
    assert response.status == 200
    assert response.getheader("Content-Encoding") == "gzip"
    assert response.getheader("Content-Type") == plain.getheader("Content-Type")
    assert response.getheader("Vary") == "Accept-Encoding"
    assert response.getheader("Content-Length") == str(len(body))
    assert len(body) < len(raw)
    assert gzip.decompress(body) == raw
    assert response.getheader("Last-Modified") == plain.getheader("Last-Modified")


@pytest.mark.parametrize("name", sorted(ICON_FILES))
def test_icons_are_gzipped_like_github_pages(site, name):
    raw = ICON_FILES[name]
    plain, plain_body = fetch(site, f"/{name}", compress=False)
    assert plain.getheader("Content-Encoding") is None and plain_body == raw
    response, body = fetch(site, f"/{name}", GZIP)
    assert response.status == 200
    assert response.getheader("Content-Encoding") == "gzip"
    assert response.getheader("Content-Type") == plain.getheader("Content-Type")
    assert response.getheader("Vary") == "Accept-Encoding"
    assert response.getheader("Content-Length") == str(len(body))
    assert gzip.decompress(body) == raw


@pytest.mark.parametrize("name", sorted(BINARY_FILES))
def test_raster_images_and_pdfs_are_never_compressed(site, name):
    response, body = fetch(site, f"/{name}", GZIP)
    assert response.status == 200
    assert response.getheader("Content-Encoding") is None
    assert response.getheader("Vary") == "Accept-Encoding"
    assert body == BINARY_FILES[name]
    assert response.getheader("Content-Length") == str(len(body))


def test_gzip_bytes_are_deterministic_level_five_with_no_timestamp(site):
    raw = (site / "style.css").read_bytes()
    first = fetch(site, "/style.css", GZIP)[1]
    assert first == fetch(site, "/style.css", GZIP)[1]
    assert first == gzip.compress(raw, compresslevel=5, mtime=0)


@pytest.mark.parametrize("header", [{}, {"Accept-Encoding": "identity"}, {"Accept-Encoding": "gzip;q=0"},
                                    {"Accept-Encoding": "br"}])
def test_clients_that_do_not_accept_gzip_get_identity_with_vary(site, header):
    response, body = fetch(site, "/style.css", header)
    assert response.getheader("Content-Encoding") is None
    assert response.getheader("Vary") == "Accept-Encoding"
    assert body == (site / "style.css").read_bytes()


def test_head_reports_the_compressed_length_without_a_body(site):
    got, body = fetch(site, "/style.css", GZIP)
    head, head_body = fetch(site, "/style.css", GZIP, method="HEAD")
    assert head.status == 200 and head_body == b""
    assert head.getheader("Content-Encoding") == "gzip"
    assert head.getheader("Content-Length") == got.getheader("Content-Length") == str(len(body))
    assert head.getheader("Content-Type") == got.getheader("Content-Type")
    assert head.getheader("Vary") == "Accept-Encoding"
    missing_head, _ = fetch(site, "/missing.html", GZIP, method="HEAD")
    assert missing_head.status == 404
    assert missing_head.getheader("Content-Encoding") is None


def test_cache_busting_queries_and_directory_indexes_are_compressed(site):
    for path, expected in (
        ("/app.js?v=art-20261006", TEXT_FILES["app.js"]),
        ("/style.css#fragment", TEXT_FILES["style.css"]),
        ("/", REPEATED),
        ("/index.html", REPEATED),
        ("/sub/", REPEATED + "sub"),
    ):
        response, body = fetch(site, path, GZIP)
        assert response.status == 200, path
        assert response.getheader("Content-Encoding") == "gzip", path
        assert gzip.decompress(body).decode("utf-8") == expected, path
        assert response.getheader("Content-Type") == fetch(site, path, compress=False)[0].getheader("Content-Type"), path


def test_redirects_missing_files_and_listings_are_untouched(site):
    redirect, _ = fetch(site, "/sub", GZIP)
    assert redirect.status == 301
    assert redirect.getheader("Location") == "/sub/"
    assert redirect.getheader("Content-Encoding") is None
    assert redirect.getheader("Vary") == "Accept-Encoding"

    missing, body = fetch(site, "/nope.html", GZIP)
    assert missing.status == 404
    assert missing.getheader("Content-Encoding") is None
    assert missing.getheader("Vary") == "Accept-Encoding"
    assert b"File not found" in body

    trailing, _ = fetch(site, "/style.css/", GZIP)
    assert trailing.status == 404 and trailing.getheader("Content-Encoding") is None

    listing, listing_body = fetch(site, "/empty/", GZIP)
    assert listing.status == 200
    assert listing.getheader("Content-Encoding") is None
    assert listing.getheader("Content-Length") == str(len(listing_body))


def test_conditional_and_range_requests_fall_through_to_the_stock_handler(site):
    """The documented bypass: these requests are served by the stock handler, uncompressed."""
    doc = " ".join((fixture.FixtureHandler.__doc__ or "").split())
    assert all(name in doc for name in ("If-Modified-Since", "If-None-Match", "Range"))
    assert "uncompressed" in doc and "304" in doc

    body_bytes = (site / "style.css").read_bytes()
    modified = fetch(site, "/style.css", GZIP)[0].getheader("Last-Modified")
    assert modified
    stale = "Mon, 01 Jan 2001 00:00:00 GMT"
    cases = {
        "If-Modified-Since (current)": {"If-Modified-Since": modified},
        "If-Modified-Since (stale)": {"If-Modified-Since": stale},
        "If-None-Match": {"If-None-Match": '"etag"'},
        "Range": {"Range": "bytes=0-9"},
        "If-Modified-Since + If-None-Match": {"If-Modified-Since": modified, "If-None-Match": '"etag"'},
    }
    for label, extra in cases.items():
        response, body = fetch(site, "/style.css", {**GZIP, **extra})
        stock, stock_body = fetch_stock(site, "/style.css", {**GZIP, **extra})
        assert response.status == stock.status, label
        assert body == stock_body, label
        assert response.getheader("Content-Encoding") is None, label
        assert response.getheader("Content-Length") == stock.getheader("Content-Length"), label
        assert response.getheader("Content-Type") == stock.getheader("Content-Type"), label
        assert response.getheader("Vary") == "Accept-Encoding", label
        if response.status == 200:
            assert body == body_bytes, label

    # A real revalidation of an unchanged file still yields 304 with no body.
    revalidated, revalidated_body = fetch(site, "/style.css", {**GZIP, "If-Modified-Since": modified})
    assert revalidated.status == 304 and revalidated_body == b""
    # A file changed since the validator is answered in full from the raw bytes.
    changed, changed_body = fetch(site, "/style.css", {**GZIP, "If-Modified-Since": stale})
    assert changed.status == 200 and changed_body == body_bytes
    # Without those headers the same URL is gzipped, so a fresh client always is.
    fresh, fresh_body = fetch(site, "/style.css", GZIP)
    assert fresh.getheader("Content-Encoding") == "gzip" and gzip.decompress(fresh_body) == body_bytes


def test_compress_false_is_the_identity_transport(site):
    for name in TEXT_FILES:
        response, body = fetch(site, f"/{name}", GZIP, compress=False)
        assert response.getheader("Content-Encoding") is None, name
        assert response.getheader("Vary") is None, name
        assert body == (site / name).read_bytes(), name
        assert response.getheader("Content-Length") == str(len(body)), name


def test_every_text_type_in_the_copied_site_is_gzipped(tmp_path):
    """No site file served as text may silently escape compression."""
    copy = fixture.copy_site(tmp_path)
    seen: dict[str, str] = {}
    for path in copy.rglob("*"):
        if path.is_file():
            seen.setdefault(served_type(path.name), path.relative_to(copy).as_posix())
    uncompressed = {kind: example for kind, example in seen.items() if kind not in fixture.GZIP_CONTENT_TYPES}
    # Anything left over must be raster media, a PDF or markdown source, not text
    # (or an icon) the production server compresses.
    unexpected = {kind: example for kind, example in uncompressed.items()
                  if not kind.startswith("image/") and kind not in {"text/markdown", "application/pdf"}}
    assert unexpected == {}, f"site files with a type that would be served uncompressed: {unexpected}"

    for relative in ("style.css", "sw.js", "manifest.json", "index.html", "search-index-core.json", "robots.txt",
                     "favicon.ico", "js/interactive.js", "data/works.json"):
        raw = (copy / relative).read_bytes()
        response, body = fetch(copy, f"/{relative}", GZIP)
        assert response.getheader("Content-Encoding") == "gzip", relative
        assert gzip.decompress(body) == raw, relative
    response, body = fetch(copy, "/art/favicon-192.png", GZIP)
    assert response.getheader("Content-Encoding") is None
    assert body == (copy / "art" / "favicon-192.png").read_bytes()


def _socketless(site: Path, *, compress: bool = True, edit=None):
    """A parity-helper transport that drives the real handler without a socket.

    ``edit(path, headers)`` may rewrite the parsed response headers in place.
    """

    def transport(path: str, headers: dict[str, str]):
        response, _ = fetch(site, f"/{path}", headers, compress=compress)
        if edit is not None:
            edit(path, response.headers)
        return response.status, response.headers

    return transport


def test_parity_assets_are_one_gzippable_file_per_page_asset_type_in_the_copied_site(tmp_path):
    copy = fixture.copy_site(tmp_path)
    assert all((copy / asset).is_file() for asset in gate.PARITY_ASSETS), gate.PARITY_ASSETS
    kinds = {Path(asset).suffix: served_type(asset) for asset in gate.PARITY_ASSETS}
    assert set(kinds) == {".html", ".css", ".js", ".json"}
    assert all(kind in fixture.GZIP_CONTENT_TYPES for kind in kinds.values()), kinds
    assert set(gate.PARITY_ASSETS) == set(PARITY_FILES), "the synthetic site must mirror the gate's asset paths"
    gate.assert_gzip_parity("http://fixture.test", transport=_socketless(copy))
    with pytest.raises(AssertionError, match="compression parity"):
        gate.assert_gzip_parity("http://fixture.test", transport=_socketless(copy, compress=False))


def test_gzip_parity_passes_against_the_compressing_handler(site):
    gate.assert_gzip_parity("http://fixture.test", transport=_socketless(site))


def test_gzip_parity_fails_with_a_parity_message_against_the_identity_handler(site):
    with pytest.raises(AssertionError, match="compression parity") as raised:
        gate.assert_gzip_parity("http://fixture.test", transport=_socketless(site, compress=False))
    message = str(raised.value)
    for asset in gate.PARITY_ASSETS:
        assert f"{asset}: Content-Encoding=None, expected 'gzip'" in message
        assert f"{asset}: Vary=None, expected it to include 'Accept-Encoding'" in message


def test_gzip_parity_names_only_the_asset_types_that_are_not_compressed(site):
    def strip_script_encoding(path, headers):
        if path == "js/interactive.js":
            del headers["Content-Encoding"]

    with pytest.raises(AssertionError) as raised:
        gate.assert_gzip_parity("http://fixture.test", transport=_socketless(site, edit=strip_script_encoding))
    message = str(raised.value)
    assert "js/interactive.js: Content-Encoding=None" in message
    assert all(asset not in message for asset in ("index.html", "style.css", "data/works.json"))


def test_gzip_parity_requires_vary_accept_encoding_among_the_tokens(site):
    def set_vary(value):
        def edit(path, headers):
            del headers["Vary"]
            if value is not None:
                headers["Vary"] = value
        return edit

    for accepted in ("Accept-Encoding", "accept-encoding", "Origin, Accept-Encoding", "Accept-Language,accept-encoding"):
        gate.assert_gzip_parity("http://fixture.test", transport=_socketless(site, edit=set_vary(accepted)))
    for rejected in (None, "Origin", "Accept-Language", "Accept-Encodings"):
        with pytest.raises(AssertionError, match="Vary="):
            gate.assert_gzip_parity("http://fixture.test", transport=_socketless(site, edit=set_vary(rejected)))


def test_gzip_parity_reports_a_missing_asset_instead_of_raising_http_error(site):
    (site / "data" / "works.json").unlink()
    with pytest.raises(AssertionError, match=r"data/works\.json: HTTP 404, expected 200"):
        gate.assert_gzip_parity("http://fixture.test", transport=_socketless(site))


def test_gzip_parity_over_a_real_socket_passes_and_fails_with_messages(site):
    base_url, httpd = fixture.serve_site(site)  # skips when loopback bind is denied
    try:
        gate.assert_gzip_parity(base_url)
        (site / "js" / "interactive.js").unlink()
        with pytest.raises(AssertionError, match=r"js/interactive\.js: HTTP 404, expected 200"):
            gate.assert_gzip_parity(base_url)
    finally:
        fixture.stop_server(httpd)
    plain_url, plain_httpd = fixture.serve_site(site, compress=False)
    try:
        with pytest.raises(AssertionError, match="Content-Encoding=None, expected 'gzip'"):
            gate.assert_gzip_parity(plain_url, assets=("style.css",))
    finally:
        fixture.stop_server(plain_httpd)


def test_serve_site_negotiates_gzip_over_a_real_socket(site):
    base_url, httpd = fixture.serve_site(site)  # skips when loopback bind is denied
    try:
        raw = (site / "style.css").read_bytes()
        request = urllib.request.Request(f"{base_url}/style.css", headers=GZIP)
        with urllib.request.urlopen(request, timeout=10) as response:
            assert response.headers["Content-Encoding"] == "gzip"
            assert response.headers["Vary"] == "Accept-Encoding"
            assert gzip.decompress(response.read()) == raw
        with urllib.request.urlopen(f"{base_url}/style.css", timeout=10) as response:
            assert response.headers["Content-Encoding"] is None
            assert response.read() == raw
    finally:
        fixture.stop_server(httpd)
