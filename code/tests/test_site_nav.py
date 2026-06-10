"""Tests for shared site navigation HTML."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from site_nav import clip_description, render_nav, render_nav_domain, social_meta_tags


def test_clip_description_short_text_unchanged():
    text = "A concise abstract that fits well within the limit."
    assert clip_description(text) == text


def test_clip_description_truncates_on_word_boundary():
    text = (
        "This commentary critiques the analysis by Nogueiro et al. regarding the genetic "
        "heritage of Portuguese crypto-Jews, highlighting methodological weaknesses and "
        "the ambiguity of the genetic markers used to infer ancestry across populations."
    )
    assert len(text) > 155
    out = clip_description(text, limit=155)
    assert len(out) <= 155
    assert out.endswith("…")
    # No partial word: the prefix before the ellipsis ends exactly at a word boundary.
    stem = out[:-1]
    assert text.startswith(stem)
    assert text[len(stem)] == " "


def test_clip_description_collapses_whitespace():
    assert clip_description("a   b\n c") == "a b c"


def test_social_meta_tags_emits_card_and_alt():
    block = social_meta_tags(
        "Title — Daniel Ari Friedman",
        "A description.",
        "https://danielarifriedman.com/og-image.jpg",
        image_alt="Title — Daniel Ari Friedman",
    )
    assert 'name="twitter:card" content="summary_large_image"' in block
    assert 'property="og:image:alt"' in block
    assert 'name="twitter:image" content="https://danielarifriedman.com/og-image.jpg"' in block


def test_render_nav_marks_active_and_depth():
    html = render_nav(active="works", depth=1)
    assert 'href="../publications.html"' in html
    assert 'class="active"' in html
    assert "Works" in html


def test_render_nav_supports_deeper_pages():
    html = render_nav(active="works", depth=2)
    assert 'href="../../publications.html"' in html
    assert 'href="../../works/" class="active"' in html


def test_render_nav_includes_catalog_and_cite():
    html = render_nav(active="catalog", depth=0)
    assert 'href="catalog.html" class="active"' in html
    assert 'href="cite-verify.html"' in html


def test_render_nav_domain_marks_domains_active():
    html = render_nav_domain(active="domains")
    assert 'href="domains.html" class="active"' in html
    assert "Software" in html
    assert 'href="catalog.html"' in html
