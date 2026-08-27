"""Tests for shared site navigation HTML."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from site_nav import (
    CSP_META_TAG,
    nav_manifest,
    HEAD_EXTRAS,
    clip_description,
    ensure_agent_map_link,
    render_nav,
    render_nav_compact,
    render_nav_domain,
    social_meta_tags,
)


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
    assert 'name="twitter:image:alt" content="Title — Daniel Ari Friedman"' in block


def test_render_nav_marks_active_and_depth():
    html = render_nav(active="works", depth=1)
    assert 'href="../publications.html"' in html
    assert 'href="../works/" class="active" aria-current="page"' in html


def test_render_nav_supports_deeper_pages():
    html = render_nav(active="works", depth=2)
    assert 'href="../../publications.html"' in html
    assert 'href="../../works/" class="active" aria-current="page"' in html


def test_render_nav_includes_catalog_and_cite():
    html = render_nav(active="catalog", depth=0)
    assert 'href="catalog.html" class="active" aria-current="page"' in html
    assert 'href="cite-verify.html"' in html


def test_render_nav_domain_marks_domains_active():
    html = render_nav_domain(active="domains")
    assert 'href="domains.html" class="active" aria-current="page"' in html
    assert "Software" in html
    assert 'href="catalog.html"' in html


def test_render_nav_single_manifest_shape():
    """One shared shell: plain nav>ul>li>a, no menubar/menuitem roles, ~6 primary + More."""
    for active in ("", "works", "domains"):
        html = render_nav(active=active, depth=0)
        assert 'role="menubar"' not in html
        assert 'role="menuitem"' not in html
        assert '<ul class="nav-links" id="nav-menu">' in html
        assert '<details class="nav-more">' in html
        assert "<summary>More</summary>" in html
        assert html.count('aria-current="page"') == (1 if active else 0)


def test_nav_manifest_primary_set_is_stable():
    primary, secondary = nav_manifest()
    assert len(primary) == 6
    keys = [k for k, _, _, _ in primary]
    assert keys == ["publications", "works", "domains", "software", "videos", "art"]
    secondary_keys = {k for k, _, _, _ in secondary}
    assert "search" in secondary_keys and "agent-map" in secondary_keys
    assert not (set(keys) & secondary_keys)


def test_render_nav_compact_uses_same_manifest():
    html = render_nav_compact(depth=1)
    assert 'href="../works/"' in html
    assert '<details class="nav-more">' in html
    assert 'role="menubar"' not in html


def test_shared_security_policy_allows_only_required_frame_origin():
    assert "frame-src https://www.youtube-nocookie.com" in CSP_META_TAG
    assert "fonts.googleapis.com" not in CSP_META_TAG
    assert 'name="referrer"' in HEAD_EXTRAS
    assert "data/agent-index.json" in HEAD_EXTRAS


def test_ensure_agent_map_link_is_idempotent_for_bespoke_navigation():
    source = '<nav><div class="nav-links"><a href="publications.html">Publications</a></div></nav>'
    updated = ensure_agent_map_link(source)
    assert 'href="data/agent-index.json">Agent Map</a>' in updated
    assert ensure_agent_map_link(updated) == updated


def test_ensure_agent_map_link_supports_art_navigation():
    source = '<nav><div class="nav-right"><a href="index.html">Home</a></div></nav>'
    assert 'href="data/agent-index.json">Agent Map</a>' in ensure_agent_map_link(source)
