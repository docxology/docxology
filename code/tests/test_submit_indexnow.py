"""Tests for IndexNow submission orchestrator (no mocks; injected opener)."""

from __future__ import annotations

import json
import sys
import urllib.error
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(ORCH_DIR))

from submit_indexnow import indexnow_urls, key_location, submit_bulk  # noqa: E402
from sitemap_policy import SITE_ORIGIN, gsc_priority_urls  # noqa: E402


class _Resp:
    """Real minimal context-managed response, not a mock."""

    def __init__(self, status: int):
        self.status = status

    def __enter__(self) -> "_Resp":
        return self

    def __exit__(self, *args) -> bool:
        return False


def _ok_opener(request, timeout=None) -> _Resp:
    return _Resp(200)


def _url_error_opener(request, timeout=None) -> _Resp:
    raise urllib.error.URLError("connection refused")


def test_gsc_priority_urls_include_hubs():
    urls = gsc_priority_urls()
    assert SITE_ORIGIN in urls
    assert f"{SITE_ORIGIN}exports.html" in urls
    assert f"{SITE_ORIGIN}publications.html" in urls


def test_indexnow_urls_include_homepage_and_works():
    urls = indexnow_urls()
    assert SITE_ORIGIN in urls
    assert any("/works/" in url and url.endswith(".html") for url in urls)


def test_key_location_uses_txt_suffix_for_32_char_key():
    key = "a" * 32
    assert key_location(key) == f"{SITE_ORIGIN}{key}.txt"


def test_submit_bulk_dry_run_no_network():
    assert submit_bulk(gsc_priority_urls(), "test-key", dry_run=True) == 0


def test_submit_bulk_success():
    assert submit_bulk([SITE_ORIGIN], "test-key", dry_run=False, opener=_ok_opener) == 0


def test_submit_bulk_returns_one_on_url_error():
    # A URLError (timeout/DNS/connection-refused) must be caught and returned
    # as a clean exit code 1, not surfaced as an uncaught traceback.
    assert submit_bulk([SITE_ORIGIN], "test-key", dry_run=False, opener=_url_error_opener) == 1


def test_submit_bulk_constructs_single_post_with_key_and_urls():
    captured: dict = {}

    def capture(request, timeout=None) -> _Resp:
        captured["request"] = request
        return _Resp(200)

    urls = [SITE_ORIGIN, f"{SITE_ORIGIN}works/"]
    submit_bulk(urls, "a" * 32, dry_run=False, opener=capture)
    body = json.loads(captured["request"].data.decode("utf-8"))
    assert body["host"] == "danielarifriedman.com"
    assert body["key"] == "a" * 32
    assert body["urlList"] == urls
    assert body["keyLocation"] == f"{SITE_ORIGIN}{'a' * 32}.txt"
