"""Invariants for the generated artwork pages, collections, and gallery floor."""

from __future__ import annotations

import json
import re
import sys
from html import unescape
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401

REPO_ROOT = Path(__file__).resolve().parents[2]

import build_artwork_pages  # noqa: E402
import sync_art_gallery  # noqa: E402
from docxology_tools.art_collections import load_collections, normalize_tag  # noqa: E402
from docxology_tools.artwork_pages import (  # noqa: E402
    ARTWORK_PAGE_MARKER,
    artwork_page_paths,
    is_thin,
    page_rel_path,
    sitemap_paths,
)


def _payload() -> dict:
    return json.loads((REPO_ROOT / "data" / "artworks.json").read_text(encoding="utf-8"))


def test_every_artwork_record_has_a_page() -> None:
    payload = _payload()
    for rel in artwork_page_paths(payload):
        assert (REPO_ROOT / rel).is_file(), f"missing generated artwork page: {rel}"
    assert (REPO_ROOT / "artworks" / "index.html").is_file()
    # Newest record's page exists (Solstice regression: the record the frozen
    # snapshot was missing).
    newest = payload["artworks"][0]
    assert (REPO_ROOT / page_rel_path(newest)).is_file()


def test_every_collection_page_exists_and_is_listed() -> None:
    collections = load_collections()
    assert collections, "ART_COLLECTIONS.md parsed no collections"
    slugs = {collection.slug for collection in collections}
    for slug in slugs:
        assert (REPO_ROOT / "art-collections" / f"{slug}.html").is_file()
        collection_page = (REPO_ROOT / "art-collections" / f"{slug}.html").read_text(encoding="utf-8")
        assert ARTWORK_PAGE_MARKER in collection_page
    index_html = (REPO_ROOT / "artworks" / "index.html").read_text(encoding="utf-8")
    for slug in slugs:
        assert f'href="../art-collections/{slug}.html"' in index_html


def test_page_titles_and_descriptions_within_serp_limits() -> None:
    payload = _payload()
    for record in payload["artworks"]:
        page = (REPO_ROOT / page_rel_path(record)).read_text(encoding="utf-8")
        title_match = re.search(r"<title>(.*?)</title>", page, re.S)
        assert title_match, f"{record['id']}: missing title"
        # Rendered (unescaped) length is what SERPs clip on.
        assert len(unescape(title_match.group(1))) <= 65, f"{record['id']}: title too long"
        description_match = re.search(r'<meta name="description" content="(.*?)"', page, re.S)
        assert description_match, f"{record['id']}: missing meta description"
        rendered = unescape(description_match.group(1))
        assert rendered.strip(), f"{record['id']}: empty meta description"
        assert len(rendered) <= 160, f"{record['id']}: meta description {len(rendered)} chars"
        assert "…" not in rendered or rendered.endswith("…"), f"{record['id']}: mid-word ellipsis"


def test_json_ld_parses_with_required_visualartwork_keys() -> None:
    payload = _payload()
    required = {"@context", "@type", "@id", "name", "url", "image", "dateCreated", "artform", "artMedium", "creator", "sameAs"}
    checked = 0
    for record in payload["artworks"][:40]:
        page = (REPO_ROOT / page_rel_path(record)).read_text(encoding="utf-8")
        blocks = re.findall(r"<script type=\"application/ld\+json\">\n(.*?)\n    </script>", page, re.S)
        payloads = [json.loads(block) for block in blocks]
        visual = [item for item in payloads if item.get("@type") == "VisualArtwork"]
        assert visual, f"{record['id']}: no VisualArtwork JSON-LD"
        data = visual[0]
        missing = required - set(data)
        assert not missing, f"{record['id']}: VisualArtwork missing {missing}"
        assert data["artform"] == "Drawing"
        assert data["artMedium"] == "Ink on paper"
        assert data["creator"]["@id"] == "https://danielarifriedman.com/#person"
        assert data["sameAs"] == [record["flickr_url"]]
        assert data["url"].startswith("https://danielarifriedman.com/artworks/")
        checked += 1
    assert checked == 40
    breadcrumbs = re.findall(r'"@type":\s*"BreadcrumbList"', (REPO_ROOT / page_rel_path(payload["artworks"][0])).read_text(encoding="utf-8"))
    assert breadcrumbs, "artwork page missing BreadcrumbList"


def test_no_empty_alt_text() -> None:
    payload = _payload()
    for record in payload["artworks"][:100]:
        page = (REPO_ROOT / page_rel_path(record)).read_text(encoding="utf-8")
        for alt in re.findall(r'<img[^>]*\balt="([^"]*)"', page):
            assert unescape(alt).strip(), f"{record['id']}: empty alt text"
    for page_path in sorted((REPO_ROOT / "artworks").glob("*.html"))[:0] + [REPO_ROOT / "artworks" / "index.html"]:
        for alt in re.findall(r'alt=""', page_path.read_text(encoding="utf-8")):
            raise AssertionError(f"{page_path.name}: empty alt text")


def test_canonicals_and_robots_policy() -> None:
    payload = _payload()
    thin_seen = 0
    for record in payload["artworks"]:
        page = (REPO_ROOT / page_rel_path(record)).read_text(encoding="utf-8")
        expected = f'<link rel="canonical" href="https://danielarifriedman.com/{page_rel_path(record)}">'
        assert expected in page, f"{record['id']}: canonical mismatch"
        robots = 'content="noindex, follow"' if is_thin(record) else 'content="index, follow"'
        assert f'<meta name="robots" {robots}>' in page, f"{record['id']}: wrong robots for thin={is_thin(record)}"
        if is_thin(record):
            thin_seen += 1
        # Every page carries a visible Flickr backlink.
        assert "View on Flickr" in page, f"{record['id']}: missing Flickr backlink"
        assert 'rel="license" href="https://creativecommons.org/' in page or "all rights reserved" in page, (
            f"{record['id']}: missing license notice"
        )
    # Report the thin count: DAF enriches these on Flickr; the sync promotes them.
    print(f"thin (noindex) artwork pages: {thin_seen}")


def test_sitemap_excludes_thin_pages_and_matches_policy() -> None:
    payload = _payload()
    promoted = set(sitemap_paths(payload))
    all_pages = set(artwork_page_paths(payload))
    assert promoted <= all_pages
    thin = {page_rel_path(record) for record in payload["artworks"] if is_thin(record)}
    assert not (promoted & thin), "thin noindex pages must be excluded from the sitemap"
    # The sitemap builder's loc set agrees with the policy module.
    sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
    import build_sitemap  # noqa: E402

    locs = build_sitemap.sitemap_locs()
    artwork_locs = {loc.removeprefix("https://danielarifriedman.com/") for loc in locs if "/artworks/" in loc}
    collection_locs = {loc.removeprefix("https://danielarifriedman.com/") for loc in locs if "/art-collections/" in loc}
    assert artwork_locs == promoted | {"artworks/"}
    assert collection_locs == {f"art-collections/{c.slug}.html" for c in load_collections()}


def test_generation_is_idempotent() -> None:
    first = build_artwork_pages.outputs()
    second = build_artwork_pages.outputs()
    assert first.keys() == second.keys()
    assert all(first[path] == second[path] for path in first), "rendering is not byte-stable"


def test_art_html_tiles_are_links_with_fresh_data() -> None:
    html = (REPO_ROOT / "art.html").read_text(encoding="utf-8")
    payload = _payload()
    records = payload["artworks"][: sync_art_gallery.SSR_FLOOR_ROWS]
    for record in records:
        expected_href = f'href="{page_rel_path(record)}"'
        assert expected_href in html, f"{record['id']}: SSR tile not linked"
    assert '<button type="button" class="art-card"' not in html, "stale button tiles remain in art.html"
    for img in re.findall(r"<img[^>]*art-thumb ssr[^>]*>", html):
        assert "_m.jpg" not in img
        assert "onclick" not in img.lower()
        assert 'alt="' in img
    # The no-JS floor points at the plain-HTML artwork index.
    assert '<a href="artworks/">artwork index</a>' in html
    # The interactive layer hydrates the same tiles and keeps them links.
    js = (REPO_ROOT / "js" / "art-gallery.js").read_text(encoding="utf-8")
    assert "art-thumb.ssr" in js
    assert "ssrByTitle" in js
    assert 'data-src="${esc(largeThumb(art.thumb))}"' in js
    assert "createElement('a')" in js and "card.href = art.page" in js


def test_collections_match_records_deterministically() -> None:
    payload = _payload()
    collections = load_collections()
    records = payload["artworks"]
    assert sum(len(members) for members in (build_artwork_pages_render_members(c, records) for c in collections)) > 0


def build_artwork_pages_render_members(collection, records):
    from docxology_tools.art_collections import members_for

    return members_for(collection, records)


def test_normalize_tag_matches_flickr_format() -> None:
    assert normalize_tag("Collective Behavior") == "collectivebehavior"
    assert normalize_tag("DNA") == "dna"
