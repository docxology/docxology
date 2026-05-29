"""Tests for IndexNow submission orchestrator."""

from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCH_DIR = REPO_ROOT / "code" / "orchestrators"
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
sys.path.insert(0, str(ORCH_DIR))

from submit_indexnow import indexnow_urls, key_location, submit_bulk  # noqa: E402
from sitemap_policy import SITE_ORIGIN, gsc_priority_urls  # noqa: E402


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
    response = MagicMock()
    response.status = 200
    response.__enter__ = MagicMock(return_value=response)
    response.__exit__ = MagicMock(return_value=False)
    with patch("submit_indexnow.urllib.request.urlopen", return_value=response):
        assert submit_bulk([SITE_ORIGIN], "test-key", dry_run=False) == 0
