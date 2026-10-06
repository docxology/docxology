"""Tests for GSC follow-up preflight orchestrator."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]

import gsc_followup_preflight  # noqa: E402
from build_sitemap import sitemap_locs  # noqa: E402
from gsc_followup_preflight import (  # noqa: E402
    MANUAL_STEPS,
    build_report,
    has_noindex_robots_meta,
    local_checks,
    priority_local_path,
    priority_url_problems,
    retired_sitemap_row,
    sitemap_file_problems,
)
from docxology_tools.seo_invariants import REDIRECT_STUBS  # noqa: E402
from docxology_tools.sitemap_policy import (  # noqa: E402
    RETIRED_SITEMAP_PATHS,
    SITE_ORIGIN,
    gsc_priority_urls,
)

CANONICAL_ROBOTS = (
    "User-agent: *\n"
    "Allow: /\n"
    "\n"
    "# Public site — full crawl permitted.\n"
    "# Index priorities: sitemap.xml\n"
    "\n"
    f"Sitemap: {SITE_ORIGIN}sitemap.xml\n"
)
SITEMAP_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    f"  <url><loc>{SITE_ORIGIN}</loc></url>\n"
    "</urlset>\n"
)


def _page(robots: str) -> str:
    return f'<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="{robots}"></head><body></body></html>\n'


def _sitemap_fixture(root: Path, robots: str = CANONICAL_ROBOTS) -> Path:
    (root / "sitemap.xml").write_text(SITEMAP_XML, encoding="utf-8")
    (root / "robots.txt").write_text(robots, encoding="utf-8")
    return root


def test_manual_steps_cover_plan_todos():
    ids = {step["id"] for step in MANUAL_STEPS}
    assert ids == {
        "gsc-sitemap",
        "gsc-remove-retired-sitemap",
        "gsc-index-hubs",
        "gsc-review-exclusions",
        "gsc-monitor",
    }


def test_manual_steps_have_no_blanket_validate_fix():
    assert not [step["id"] for step in MANUAL_STEPS if step["id"].startswith("gsc-validate")]
    review = next(step for step in MANUAL_STEPS if step["id"] == "gsc-review-exclusions")
    assert "all affected URLs" in review["action"]
    retired = next(step for step in MANUAL_STEPS if step["id"] == "gsc-remove-retired-sitemap")
    assert all(path in retired["action"] for path in RETIRED_SITEMAP_PATHS)


def test_local_checks_pass_on_repo():
    rows = local_checks(REPO_ROOT)
    assert rows
    assert all(row["ok"] for row in rows), rows
    names = {row["check"] for row in rows}
    assert {"sitemap_files_canonical_only", "priority_urls_indexable"} <= names


def test_build_report_skip_live_preflight_ok():
    report = build_report(REPO_ROOT, skip_live=True)
    assert report["preflight_ok"] is True
    assert report["priority_urls"] == gsc_priority_urls()
    assert "https://danielarifriedman.com/repositories.html" in report["priority_urls"]
    assert "https://danielarifriedman.com/videos.html" in report["priority_urls"]


def test_build_report_checklist_matches_manual_steps():
    report = build_report(REPO_ROOT, skip_live=True)
    checklist = "\n".join(report["checklist"])
    assert "Validate fix:" not in checklist
    assert "Reviewed exclusions" in checklist
    assert all(path in checklist for path in RETIRED_SITEMAP_PATHS)


def test_priority_urls_exclude_noindex_videos_index():
    urls = gsc_priority_urls()
    assert SITE_ORIGIN + "videos/" not in urls
    assert SITE_ORIGIN + "videos.html" in urls
    assert len(urls) == len(set(urls)) == 10


def test_priority_urls_in_sitemap_and_indexable_on_repo():
    assert priority_url_problems(REPO_ROOT, gsc_priority_urls(), set(sitemap_locs())) == []


def test_priority_local_path_maps_hubs_to_files():
    assert priority_local_path(SITE_ORIGIN) == "index.html"
    assert priority_local_path(SITE_ORIGIN + "works/") == "works/index.html"
    assert priority_local_path(SITE_ORIGIN + "software.html") == "software.html"
    assert priority_local_path("https://www.example.org/x.html") is None


def test_priority_url_problems_flags_noindex_unsitemapped_and_missing(tmp_path):
    (tmp_path / "index.html").write_text(_page("index, follow"), encoding="utf-8")
    (tmp_path / "videos").mkdir()
    (tmp_path / "videos" / "index.html").write_text(_page("noindex, follow"), encoding="utf-8")
    home = SITE_ORIGIN
    videos_index = SITE_ORIGIN + "videos/"
    missing = SITE_ORIGIN + "missing.html"

    assert priority_url_problems(tmp_path, [home], {home}) == []

    problems = priority_url_problems(tmp_path, [home, videos_index, missing], {home})
    assert any(videos_index in p and "not in the sitemap" in p for p in problems)
    assert any(videos_index in p and "noindex" in p for p in problems)
    assert any(missing in p and "not found" in p for p in problems)
    assert not any(p.startswith(f"{home}: ") for p in problems)


@pytest.mark.parametrize(
    "html, expected",
    [
        ('<meta name="robots" content="noindex, follow">', True),
        ('<meta content="NOINDEX,nofollow" name="robots">', True),
        ("<meta name='robots' content='index, nofollow, noindex'>", True),
        ('<meta name="robots" content="index, follow">', False),
        ('<meta name="description" content="why noindex pages exist">', False),
        ("<html><head><title>no robots meta</title></head></html>", False),
    ],
)
def test_has_noindex_robots_meta_handles_attribute_order_and_quotes(html, expected):
    assert has_noindex_robots_meta(html) is expected


@pytest.mark.parametrize(
    "html, expected",
    [
        ('<meta name="robots" content="none">', True),
        ('<meta content="NONE" name="robots">', True),
        ('<meta name="robots" content="none, follow">', True),
        ('<meta name="robots" content="index, nofollow">', False),
        ('<meta name="robots" content="noarchive; noindex">', True),
        ('<meta name="robots" content="index" content="noindex">', False),
        ('<meta name="description" name="robots" content="noindex">', False),
        ('<head></head><body><meta name="robots" content="noindex"></body>', False),
        ('<meta name="robots" content="nonexistent">', False),
        ('<meta name="robots">', False),
    ],
)
def test_has_noindex_robots_meta_treats_none_as_noindex(html, expected):
    assert has_noindex_robots_meta(html) is expected


@pytest.mark.parametrize(
    "html, expected",
    [
        ('<meta name="googlebot" content="noindex">', True),
        ('<meta content="none" name="googlebot">', True),
        ("<meta name='GoogleBot' content='noindex, nofollow'>", True),
        ('<meta name="googlebot" content="index, follow">', False),
        # Both meta tags are inspected: noindex on either one blocks indexing.
        ('<meta name="robots" content="index"><meta name="googlebot" content="noindex">', True),
        ('<meta name="robots" content="noindex"><meta name="googlebot" content="index">', True),
        ('<meta name="robots" content="index"><meta name="googlebot" content="index">', False),
        # Not a name attribute, so not a robots directive.
        ('<meta data-name="robots" content="noindex">', False),
        ('<meta property="robots" content="noindex">', False),
    ],
)
def test_has_noindex_robots_meta_inspects_googlebot_as_well_as_robots(html, expected):
    assert has_noindex_robots_meta(html) is expected


@pytest.mark.parametrize(
    "html, expected",
    [
        ("<meta name=robots content=noindex>", True),
        ("<meta name=robots content=noindex,nofollow>", True),
        ("<meta content=none name=googlebot>", True),
        ("<meta name=robots content=noindex/>", True),
        ("<meta name=robots content=index>", False),
        ("<meta name=robots content=index,follow>", False),
        ("<meta name=robots content=nofollow>", False),
        # A ">" inside a quoted attribute value does not end the tag early.
        ('<meta name="robots" data-note="a > b" content="noindex">', True),
    ],
)
def test_has_noindex_robots_meta_accepts_unquoted_content_values(html, expected):
    assert has_noindex_robots_meta(html) is expected


@pytest.mark.parametrize(
    "html, expected",
    [
        ('<!-- <meta name="robots" content="noindex"> -->', False),
        ('<!--<meta name="googlebot" content="none">-->', False),
        ('<!--\n<meta name="robots" content="noindex">\n-->', False),
        ('<!--[if IE]><meta name="robots" content="noindex"><![endif]-->', False),
        # An unterminated comment swallows the rest of the document.
        ('<!-- <meta name="robots" content="noindex">', False),
        # A live tag outside the comment still counts.
        ('<!-- retired --><meta name="robots" content="noindex">', True),
        ('<!-- <meta name="robots" content="index"> --><meta name="robots" content="noindex">', True),
        ('<meta name="robots" content="noindex"><!-- trailing -->', True),
        ('<!-- <meta name="robots" content="noindex"> --><meta name="robots" content="index">', False),
    ],
)
def test_has_noindex_robots_meta_ignores_html_comments(html, expected):
    assert has_noindex_robots_meta(html) is expected


def test_sitemap_file_guard_passes_on_repo():
    assert sitemap_file_problems(REPO_ROOT) == []


def test_sitemap_file_guard_passes_on_canonical_fixture(tmp_path):
    _sitemap_fixture(tmp_path)
    assert sitemap_file_problems(tmp_path) == []


@pytest.mark.parametrize("extra", ["sitemap-video.xml", "sitemap_index.xml", "news-sitemap.xml"])
def test_sitemap_file_guard_rejects_any_extra_root_sitemap_file(tmp_path, extra):
    _sitemap_fixture(tmp_path)
    (tmp_path / extra).write_text(SITEMAP_XML, encoding="utf-8")
    problems = sitemap_file_problems(tmp_path)
    assert any("extra root sitemap file" in p and extra in p for p in problems), problems


def test_sitemap_file_guard_ignores_non_sitemap_xml_and_nested_files(tmp_path):
    _sitemap_fixture(tmp_path)
    (tmp_path / "feed.xml").write_text("<rss/>\n", encoding="utf-8")
    (tmp_path / "feeds").mkdir()
    (tmp_path / "feeds" / "domain-x.xml").write_text("<rss/>\n", encoding="utf-8")
    assert sitemap_file_problems(tmp_path) == []


def test_sitemap_file_guard_rejects_extra_robots_sitemap_line(tmp_path):
    _sitemap_fixture(tmp_path, CANONICAL_ROBOTS + f"Sitemap: {SITE_ORIGIN}sitemap-video.xml\n")
    problems = sitemap_file_problems(tmp_path)
    assert any("2 Sitemap: lines" in p for p in problems), problems
    assert any("sitemap-video.xml" in p for p in problems), problems


def test_sitemap_file_guard_rejects_duplicate_canonical_robots_line(tmp_path):
    _sitemap_fixture(tmp_path, CANONICAL_ROBOTS + f"sitemap: {SITE_ORIGIN}sitemap.xml\n")
    problems = sitemap_file_problems(tmp_path)
    assert any("2 Sitemap: lines" in p for p in problems), problems


def test_sitemap_file_guard_rejects_non_canonical_or_missing_robots_sitemap(tmp_path):
    _sitemap_fixture(tmp_path, CANONICAL_ROBOTS.replace("https://danielarifriedman.com", "https://www.danielarifriedman.com"))
    assert any("not canonical" in p for p in sitemap_file_problems(tmp_path))

    _sitemap_fixture(tmp_path, "User-agent: *\nAllow: /\n# Index priorities: sitemap.xml\n")
    assert any("0 Sitemap: lines" in p for p in sitemap_file_problems(tmp_path))

    (tmp_path / "robots.txt").unlink()
    assert sitemap_file_problems(tmp_path) == ["robots.txt is missing"]


def test_retired_sitemap_paths_are_absent_from_repo_root():
    assert RETIRED_SITEMAP_PATHS
    for path in RETIRED_SITEMAP_PATHS:
        assert not (REPO_ROOT / path).exists(), path
        assert SITE_ORIGIN + path not in (REPO_ROOT / "robots.txt").read_text(encoding="utf-8")


@pytest.mark.parametrize("status", [404, 410])
def test_retired_sitemap_row_ok_when_gone(status):
    url = SITE_ORIGIN + "sitemap-video.xml"
    row = retired_sitemap_row("sitemap-video.xml", {"url": url, "status": status, "ok": False, "elapsed_ms": 12})
    assert row["check"] == "retired_sitemap_sitemap-video.xml"
    assert row["ok"] is True
    assert row["url"] == url
    assert str(status) in row["detail"]


@pytest.mark.parametrize("status", [200, 301, 403, 500])
def test_retired_sitemap_row_fails_when_still_served_or_erroring(status):
    row = retired_sitemap_row("sitemap-video.xml", {"url": SITE_ORIGIN + "sitemap-video.xml", "status": status, "ok": 200 <= status < 400})
    assert row["ok"] is False
    assert str(status) in row["detail"]


def test_retired_sitemap_row_fails_on_network_error_or_no_response():
    error_hit = {"url": SITE_ORIGIN + "sitemap-video.xml", "status": None, "ok": False, "error": "timed out"}
    row = retired_sitemap_row("sitemap-video.xml", error_hit)
    assert row["ok"] is False
    assert "timed out" in row["detail"]

    row = retired_sitemap_row("sitemap-video.xml", None)
    assert row["ok"] is False
    assert row["url"] == SITE_ORIGIN + "sitemap-video.xml"


def _retired_urls() -> dict[str, str]:
    return {SITE_ORIGIN + path: path for path in RETIRED_SITEMAP_PATHS}


def _fake_fetch_status(retired_status, calls):
    """Stand-in for ``fetch_status``: every live URL is 200 except the retired sitemaps."""
    retired = _retired_urls()

    def fake(url, timeout=30):
        calls.append(url)
        status = retired_status if url in retired else 200
        hit = {
            "url": url,
            "status": status,
            "ok": status is not None and 200 <= status < 400,
            "elapsed_ms": 1,
        }
        if status is None:
            hit["error"] = "timed out"
        return hit

    return fake


@pytest.mark.parametrize("status", [404, 410])
def test_live_checks_retired_sitemap_probe_passes_when_gone(monkeypatch, status):
    calls: list[str] = []
    monkeypatch.setattr(gsc_followup_preflight, "fetch_status", _fake_fetch_status(status, calls))
    rows = {row["check"]: row for row in gsc_followup_preflight.live_checks()}
    for url, path in _retired_urls().items():
        row = rows[f"retired_sitemap_{path}"]
        assert row["ok"] is True, row
        assert row["url"] == url
        assert str(status) in row["detail"]
        assert url in calls
    assert all(row["ok"] for row in rows.values()), [r for r in rows.values() if not r["ok"]]


@pytest.mark.parametrize("status", [200, 301, 500, None])
def test_live_checks_retired_sitemap_probe_fails_when_served_or_unconfirmed(monkeypatch, status):
    calls: list[str] = []
    monkeypatch.setattr(gsc_followup_preflight, "fetch_status", _fake_fetch_status(status, calls))
    rows = gsc_followup_preflight.live_checks()
    failing = [row["check"] for row in rows if not row["ok"]]
    # Only the retired-sitemap rows fail: the other live URLs all return 200.
    assert failing == [f"retired_sitemap_{path}" for path in RETIRED_SITEMAP_PATHS]
    assert all(url in calls for url in _retired_urls())


@pytest.mark.parametrize(
    "status, expected_ok",
    [(404, True), (410, True), (200, False), (500, False), (None, False)],
)
def test_build_report_preflight_ok_gates_on_retired_sitemap_probe(monkeypatch, status, expected_ok):
    # Isolate the live wiring: the local checks are covered by test_local_checks_pass_on_repo.
    monkeypatch.setattr(gsc_followup_preflight, "local_checks", lambda root: [{"check": "stub", "ok": True, "detail": "ok"}])
    monkeypatch.setattr(gsc_followup_preflight, "fetch_status", _fake_fetch_status(status, []))
    report = gsc_followup_preflight.build_report(REPO_ROOT, skip_live=False)
    retired_rows = [row for row in report["live_checks"] if row["check"].startswith("retired_sitemap_")]
    assert [row["check"] for row in retired_rows] == [f"retired_sitemap_{path}" for path in RETIRED_SITEMAP_PATHS]
    assert all(row["ok"] is expected_ok for row in retired_rows)
    assert report["preflight_ok"] is expected_ok


def test_committed_checklist_json_matches_code():
    """``data/gsc-followup-checklist.json`` is published; it must be regenerated with the code.

    Regenerate with ``gsc_followup_preflight.py --json`` (it also rewrites the dated
    preflight receipt, so run it on the day the receipt should carry).
    """
    checklist = json.loads((REPO_ROOT / "data" / "gsc-followup-checklist.json").read_text(encoding="utf-8"))
    report = build_report(REPO_ROOT, skip_live=True)
    for key in ("property", "priority_urls", "gsc_links", "manual_steps", "checklist"):
        assert checklist[key] == report[key], key


def test_runbook_stub_canonicals_match_redirect_stubs():
    """The runbook says the four section stubs canonicalize to the homepage and refresh to a section."""
    section_stubs = {
        stub.path: stub for stub in REDIRECT_STUBS if stub.target_url.startswith(SITE_ORIGIN + "#")
    }
    assert set(section_stubs) == {"about.html", "blog/index.html", "meditations.html", "research.html"}
    assert all(stub.canonical_url == SITE_ORIGIN for stub in section_stubs.values())
    fragments = [stub.target_url.removeprefix(SITE_ORIGIN) for stub in section_stubs.values()]
    assert sorted(fragments) == ["#about", "#media", "#media", "#research"]

    runbook = (REPO_ROOT / "docs" / "seo" / "gsc-followup.md").read_text(encoding="utf-8")
    assert f"canonicalize to the homepage (`{SITE_ORIGIN}`)" in runbook
    assert "meta-refresh targets are the `#about`, `#media`, `#media` and `#research` sections" in runbook
