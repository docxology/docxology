"""Tests for the scoped external-link checker."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import check_external_links as cel  # noqa: E402
from check_external_links import build_report, clean_url  # noqa: E402


def test_clean_url_strips_trailing_tab():
    assert clean_url("https://example.com/path\t") == "https://example.com/path"
    assert clean_url("https://example.com/path.\t\n\r") == "https://example.com/path"


def test_build_report_accounting_when_limited(monkeypatch):
    sources = {
        "https://a.example/1": ["index.html"],
        "https://a.example/2": ["index.html"],
        "https://a.example/3": ["README.md"],
    }
    monkeypatch.setattr(cel, "collect_urls", lambda: sources)

    def fake_request(url: str, timeout: int) -> dict:
        ok = url.endswith("1")
        return {
            "url": url,
            "ok": ok,
            "status": 200 if ok else 404,
            "method": "HEAD",
            "final_url": url,
            "error": "",
        }

    monkeypatch.setattr(cel, "request_url", fake_request)

    report = build_report(timeout=1, workers=2, limit=2)
    assert report["total_unique_urls"] == 3
    assert report["checked_urls"] == 2
    assert report["unchecked_urls"] == 1
    assert report["ok"] + report["warnings"] == report["checked_urls"]
    assert report["checked_urls"] + report["unchecked_urls"] == report["total_unique_urls"]
    assert report["ok"] + report["warnings"] == 2
