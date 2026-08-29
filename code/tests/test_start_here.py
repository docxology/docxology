"""Tests for start-here.html and its validator (starthere lane, 2026-08-29)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import build_start_here  # noqa: E402
from site_nav import nav_manifest  # noqa: E402

PAGE_PATH = REPO_ROOT / "start-here.html"


def test_page_exists_with_four_paths():
    assert PAGE_PATH.exists(), "start-here.html must exist at repo root"
    markup = PAGE_PATH.read_text(encoding="utf-8")
    assert build_start_here.check_paths(markup) == []


def test_all_local_links_resolve():
    markup = PAGE_PATH.read_text(encoding="utf-8")
    assert build_start_here.check_links(markup) == []


def test_titles_within_limit():
    markup = PAGE_PATH.read_text(encoding="utf-8")
    assert build_start_here.check_titles(markup) == []


def test_full_check_passes():
    assert build_start_here.check() == []


def test_each_path_has_5_to_8_links():
    markup = PAGE_PATH.read_text(encoding="utf-8")
    import re

    for pid in build_start_here.REQUIRED_PATH_IDS:
        card = re.search(
            rf'<article class="start-card" id="{pid}">.*?</article>', markup, re.S
        )
        assert card, f"card {pid} missing"
        links = [h for h in build_start_here._link_hrefs(card.group(0)) if h.startswith(("works/", ".html", "index", "resume", "domain")) or h.endswith(".html")]
        assert 5 <= len(links) <= 8, f"{pid}: {len(links)} links"


def test_page_has_standard_shell():
    markup = PAGE_PATH.read_text(encoding="utf-8")
    for needle in (
        'rel="canonical" href="https://danielarifriedman.com/start-here.html"',
        'property="og:title"',
        'property="og:image"',
        'application/ld+json',
        '"@type": "WebPage"',
        'class="skip-link"',
        'aria-current="page">Start Here</a>',
        'rel="stylesheet" href="style.css',
    ):
        assert needle in markup, f"shell element missing: {needle}"


def test_nav_manifest_contains_start_here():
    primary, secondary = nav_manifest()
    keys = [k for k, *_ in primary + secondary]
    assert "start-here" in keys
    entry = next(e for e in secondary if e[0] == "start-here")
    assert entry[1].endswith("start-here.html")
    assert entry[2] == "Start Here"


def test_check_rejects_broken_link(tmp_path, monkeypatch):
    # Negative control: a fabricated page with a dead link must fail the check.
    markup = '<a href="no-such-page.html">ghost</a>'
    errors = build_start_here.check_links(markup)
    assert errors and "broken link" in errors[0]


def test_check_rejects_overlong_title():
    markup = "<h2>" + "x" * 66 + "</h2>"
    errors = build_start_here.check_titles(markup)
    assert errors and "title over" in errors[0]
