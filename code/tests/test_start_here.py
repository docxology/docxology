"""Tests for start-here.html and its validator (starthere lane, 2026-08-29)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

REPO_ROOT = Path(__file__).resolve().parents[2]

import build_start_here  # noqa: E402
from docxology_tools.site_nav import nav_manifest  # noqa: E402

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


def test_art_count_is_derived_from_the_artworks_export():
    # The Art line must follow data/artworks.json, not a hand-typed number.
    export_count = json.loads((REPO_ROOT / "data" / "artworks.json").read_text(encoding="utf-8"))["count"]
    assert build_start_here.load_artwork_count() == export_count
    markup = PAGE_PATH.read_text(encoding="utf-8")
    assert f"{export_count:,} catalogued pen-and-ink drawings" in markup
    assert build_start_here.check_art_count(markup, export_count) == []


def test_load_artwork_count_reads_the_given_export(tmp_path):
    export = tmp_path / "artworks.json"
    export.write_text(json.dumps({"count": 1234, "artworks": []}), encoding="utf-8")
    assert build_start_here.load_artwork_count(export) == 1234


def test_stamp_art_count_rewrites_only_the_art_number():
    markup = (
        "<li><strong>Art</strong> — 942 catalogued pen-and-ink drawings at <a>art</a>, "
        "a unified bibliography of 7 works</li>"
    )
    stamped = build_start_here.stamp_art_count(markup, 943)
    assert "943 catalogued pen-and-ink drawings" in stamped
    assert "942" not in stamped
    assert "a unified bibliography of 7 works" in stamped
    # Idempotent, and thousands separators are accepted on input and written from 1,000.
    assert build_start_here.stamp_art_count(stamped, 943) == stamped
    assert "1,043 catalogued pen-and-ink drawings" in build_start_here.stamp_art_count(stamped, 1043)
    assert build_start_here.stamp_art_count("1,043 catalogued pen-and-ink drawings", 943).startswith("943 catalogued")


def test_check_counts_flags_a_stale_art_count():
    export_count = build_start_here.load_artwork_count()
    markup = PAGE_PATH.read_text(encoding="utf-8")
    stale = markup.replace(f"{export_count:,} catalogued pen-and-ink drawings", "7 catalogued pen-and-ink drawings")
    assert stale != markup
    assert build_start_here.check_counts(markup) == []
    errors = build_start_here.check_counts(stale)
    assert errors == [f"stale art count in start-here.html (artworks.json says {export_count})"]
    # A page that lost the phrase entirely is flagged too, not silently accepted.
    assert build_start_here.check_art_count("<p>no drawings line</p>", export_count)


def test_check_art_count_requires_an_exact_number_not_a_suffix():
    phrase = "catalogued pen-and-ink drawings"
    # Exact formatted count passes, with and without a thousands separator.
    assert build_start_here.check_art_count(f"<li>943 {phrase}</li>", 943) == []
    assert build_start_here.check_art_count(f"<li>1,943 {phrase}</li>", 1943) == []
    stale = "stale art count in start-here.html (artworks.json says 943)"
    # A larger stale number that merely ends in the expected digits must NOT pass
    # (the old substring test accepted both of these).
    assert f"943 {phrase}" in f"1,943 {phrase}"
    assert build_start_here.check_art_count(f"<li>1,943 {phrase}</li>", 943) == [stale]
    assert build_start_here.check_art_count(f"<li>9943 {phrase}</li>", 943) == [stale]
    assert build_start_here.check_art_count(f"<li>x943 {phrase}</li>", 943) == [
        "missing 'N catalogued pen-and-ink drawings' count in start-here.html (artworks.json says 943)"
    ]
    # Every occurrence is compared, not just the first.
    assert build_start_here.check_art_count(f"<p>943 {phrase}</p><p>942 {phrase}</p>", 943) == [stale]
    assert build_start_here.check_art_count(f"<p>942 {phrase}</p><p>943 {phrase}</p>", 943) == [stale]
    assert build_start_here.check_art_count(f"<p>943 {phrase}</p><p>943 {phrase}</p>", 943) == []


def test_check_art_count_errors_when_the_phrase_is_missing():
    errors = build_start_here.check_art_count("<p>no drawings line, 943 drawings</p>", 943)
    assert errors == [
        "missing 'N catalogued pen-and-ink drawings' count in start-here.html (artworks.json says 943)"
    ]


def test_check_counts_rejects_a_larger_stale_art_count_on_the_real_page():
    export_count = build_start_here.load_artwork_count()
    markup = PAGE_PATH.read_text(encoding="utf-8")
    phrase = "catalogued pen-and-ink drawings"
    larger = markup.replace(f"{export_count:,} {phrase}", f"{export_count + 1000:,} {phrase}")
    assert larger != markup
    assert build_start_here.check_counts(larger) == [
        f"stale art count in start-here.html (artworks.json says {export_count})"
    ]
    # --sync-counts' stamp repairs exactly that page and nothing else.
    assert build_start_here.stamp_counts(larger) == markup


def test_stamp_counts_is_a_no_op_on_the_checked_in_page():
    markup = PAGE_PATH.read_text(encoding="utf-8")
    assert build_start_here.stamp_counts(markup) == markup


@pytest.mark.parametrize("payload", ["[]", '{"count": null}', '{"count": "943"}', '{"count": -1}', "{}"])
def test_load_artwork_count_refuses_malformed_exports_with_a_value_error(tmp_path, payload):
    export = tmp_path / "artworks.json"
    export.write_text(payload, encoding="utf-8")
    with pytest.raises(ValueError):
        build_start_here.load_artwork_count(export)


def test_extraction_counts_are_stamped_and_checked_exactly():
    counts = {"full_text_papers": 199, "extracted_images": 8959}
    stale = "203 folders, 190 with full-text extraction and 8,944 extracted images"
    assert len(build_start_here.check_extraction_counts(stale, counts)) == 2
    stamped = build_start_here.stamp_extraction_counts(stale, counts)
    assert stamped == "203 folders, 199 with full-text extraction and 8,959 extracted images"
    assert build_start_here.check_extraction_counts(stamped, counts) == []
    # A stale larger number ending in the right digits never passes.
    assert build_start_here.check_extraction_counts("1,199 with full-text extraction and 8,959 extracted images", counts)
    assert build_start_here.check_extraction_counts("no counts here", counts)
