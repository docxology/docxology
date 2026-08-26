"""Tests for the scoped external-link checker."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from check_external_links import (  # noqa: E402
    build_report,
    cached_report_errors,
    clean_url,
    collect_urls_from_text,
    scan_files,
)


def test_clean_url_strips_trailing_tab():
    assert clean_url("https://example.com/path\t") == "https://example.com/path"
    assert clean_url("https://example.com/path.\t\n\r") == "https://example.com/path"


def test_collect_urls_ignores_csp_source_expression_but_keeps_links():
    text = (
        '<meta http-equiv="Content-Security-Policy" '
        'content="frame-src https://www.youtube-nocookie.com;">'
        '<iframe src="https://www.youtube-nocookie.com/embed/demo"></iframe>'
        '<a href="https://example.org/working">working</a>'
    )

    assert collect_urls_from_text(text) == [
        "https://www.youtube-nocookie.com/embed/demo",
        "https://example.org/working",
    ]


def test_scan_files_includes_root_html_but_not_nested_html(tmp_path: Path):
    (tmp_path / "redirect.html").write_text("<!doctype html>", encoding="utf-8")
    nested = tmp_path / "works"
    nested.mkdir()
    (nested / "index.html").write_text("<!doctype html>", encoding="utf-8")

    scope = scan_files(tmp_path)

    assert "redirect.html" in scope
    assert "works/index.html" not in scope


def test_build_report_accounting_when_limited():
    sources = {
        "https://a.example/1": ["index.html"],
        "https://a.example/2": ["index.html"],
        "https://a.example/3": ["README.md"],
    }
    def local_request(url: str, timeout: int) -> dict:
        assert timeout == 1
        ok = url.endswith("1")
        return {
            "url": url,
            "ok": ok,
            "status": 200 if ok else 404,
            "method": "HEAD",
            "final_url": url,
            "error": "",
        }

    report = build_report(
        timeout=1,
        workers=2,
        limit=2,
        url_sources=sources,
        request=local_request,
    )
    assert report["total_unique_urls"] == 3
    assert report["checked_urls"] == 2
    assert report["unchecked_urls"] == 1
    assert report["ok"] + report["warnings"] == report["checked_urls"]
    assert report["checked_urls"] + report["unchecked_urls"] == report["total_unique_urls"]
    assert report["ok"] + report["warnings"] == 2


def test_cached_report_check_rejects_stale_redirect_scope_and_url_coverage():
    stale_sources = {"https://example.org/old": ["index.html"]}

    def local_request(url: str, timeout: int) -> dict:
        return {
            "url": url,
            "ok": True,
            "status": 200,
            "method": "HEAD",
            "final_url": url,
            "error": "",
        }

    report = build_report(
        timeout=1,
        workers=1,
        limit=None,
        url_sources=stale_sources,
        request=local_request,
    )
    report["scope"] = ["index.html"]

    errors = cached_report_errors(
        report,
        url_sources={"https://example.org/new": ["redirect.html"]},
        scope=["index.html", "redirect.html"],
    )

    assert any("scope does not match" in error for error in errors)
    assert any("URL coverage does not match" in error for error in errors)
