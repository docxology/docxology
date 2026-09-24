#!/usr/bin/env python3
"""Build static artwork landing pages from ``data/artworks.json``.

Outputs (all renderer-owned, marked with ``ARTWORK_PAGE_MARKER``):

- ``artworks/<id>-<slug>.html`` — one crawlable VisualArtwork page per record,
  with meta description, canonical + social tags, compact JSON-LD
  ``VisualArtwork`` and ``BreadcrumbList``, visible image/description/tags/
  license, prev/next and tag-overlap related links, and a Flickr backlink.
  Records with no tags and a very short description are still generated but
  marked ``noindex, follow``.
- ``artworks/index.html`` — the no-JS crawlable hub listing every artwork page
  (and the curated collections), so ``art.html``'s JS-rendered grid can defer
  its full link floor to a plain-HTML surface.
- ``art-collections/<slug>.html`` — curated themed hubs parsed from
  ``pages/ART_COLLECTIONS.md`` (CollectionPage + ItemList JSON-LD).
- ``data/artwork-pages-manifest.json`` — stable ownership manifest used for
  orphan detection (pruning stays a manual ``--prune-owned`` action).

This mirrors ``build_video_pages.py``/``build_work_pages.py`` conventions:
shared nav/breadcrumb/social rendering from ``docxology_tools.site_nav``, the
interactive-layer script tags, and a byte-stable ``--check`` mode. Page CSS
lives in ``style.css`` (one shared copy), visible descriptions and tag links
are capped, and JSON-LD is minified — 944 per-artwork pages must stay inside
the Pages artifact budget, which is a release gate.
"""

from __future__ import annotations

import argparse
import json
import sys
from html import escape as _html_escape
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "data" / "artworks.json"
ARTWORKS_DIR = REPO_ROOT / "artworks"
COLLECTIONS_DIR = REPO_ROOT / "art-collections"
MANIFEST_OUT = REPO_ROOT / "data" / "artwork-pages-manifest.json"
STYLE_VERSION = "newspaper-glitch-20260530c"
OG_ART_IMAGE = "https://danielarifriedman.com/og-art.jpg"
PERSON_ID = "https://danielarifriedman.com/#person"
FLICKR_PROFILE_URL = "https://www.flickr.com/photos/43693624@N07/"
TAG_LINK_CAP = 8
RELATED_COUNT = 4
VISIBLE_DESCRIPTION_CHARS = 700

from docxology_tools.art_collections import ArtCollection, load_collections, members_for, record_collections  # noqa: E402
from docxology_tools.artwork_pages import (  # noqa: E402
    ARTWORK_PAGE_MARKER,
    ARTWORK_PAGES_MANIFEST_VERSION,
    ARTWORKS_INDEX_PATH,
    COLLECTIONS_DIR as COLLECTIONS_DIR_NAME,
    SITE_ORIGIN,
    created_date,
    image_alt_text,
    is_thin,
    meta_description,
    og_image_url,
    page_filename,
    page_rel_path,
    page_title,
    page_url,
    plain_text,
)
from docxology_tools.generated_outputs import (  # noqa: E402
    read_generated_output_text,
    safe_generated_output_path,
    write_generated_output_text,
)
from docxology_tools.site_nav import (  # noqa: E402
    HEAD_EXTRAS,
    INTERACTIVE_SCRIPTS,
    MENU_ESC_SCRIPT,
    clip_description,
    render_breadcrumb,
    render_nav,
    social_meta_tags,
)


def h(value: object) -> str:
    return _html_escape(str(value), quote=True)


def compact_json_ld(payload: dict) -> str:
    """Minified JSON-LD: identical data, materially smaller across 949 pages."""
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False)


def load_payload() -> dict:
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def view_text(record: dict) -> str:
    try:
        return f"{int(str(record.get('views', '0'))) :,} views"
    except ValueError:
        return ""


def license_html(record: dict) -> str:
    """License notice from the data: CC licenses link with rel=license; ARR is a plain notice."""
    name = plain_text(record.get("license_name", "")) or ""
    url = str(record.get("license_url", "") or "")
    if url.startswith("https://creativecommons.org/"):
        return f'<a rel="license" href="{h(url)}" target="_blank" rel="noopener">{h(name or "Creative Commons license")}</a>'
    if name:
        return f'<span title="License from the Flickr record">{h(name)}</span>'
    return "<span>© Daniel Ari Friedman — all rights reserved</span>"


def description_paragraphs(record: dict) -> str:
    """Flickr description HTML -> visible paragraphs (tags stripped, CSP-safe).

    Capped at the same 700 chars as the JSON-LD description: the full text
    lives on the Flickr photo page, and 944 pages must stay inside the
    Pages artifact budget.
    """
    raw = str(record.get("desc", "") or "")
    if not raw.strip():
        return '<p class="artwork-desc muted">No description recorded on Flickr yet — see the Flickr page for context.</p>'
    paragraphs = []
    used = 0
    for chunk in raw.split("\n\n"):
        text = plain_text(chunk)
        if not text:
            continue
        if used + len(text) > VISIBLE_DESCRIPTION_CHARS:
            remaining = VISIBLE_DESCRIPTION_CHARS - used
            if remaining > 40:
                clipped = text[:remaining].rsplit(" ", 1)[0].rstrip(" ,;:.–—-")
                paragraphs.append(f"<p>{h(clipped)}…</p>")
            paragraphs.append('<p class="muted">Full description on the Flickr photo page.</p>')
            break
        paragraphs.append(f"<p>{h(text)}</p>")
        used += len(text)
    return "\n".join(paragraphs) or '<p class="artwork-desc muted">No description recorded on Flickr yet.</p>'


def related_artworks(index: int, records: list[dict], *, max_related: int = RELATED_COUNT) -> list[int]:
    """Tag-overlap related indices, padded with nearest neighbors for layout stability."""
    self_tags = {tag.lower() for tag in records[index].get("tags", [])}
    scored: list[tuple[int, int, int]] = []
    for other_index, record in enumerate(records):
        if other_index == index:
            continue
        shared = len(self_tags & {tag.lower() for tag in record.get("tags", [])})
        if shared:
            scored.append((-shared, abs(other_index - index), other_index))
    scored.sort()
    picked = [entry[2] for entry in scored[:max_related]]
    if len(picked) < max_related:
        step = 1
        while len(picked) < max_related and step < len(records):
            for neighbor in (index - step, index + step):
                if 0 <= neighbor < len(records) and neighbor != index and neighbor not in picked:
                    picked.append(neighbor)
                    if len(picked) == max_related:
                        break
            step += 1
    return picked[:max_related]


def breadcrumb_trail(record: dict) -> list[tuple[str, str]]:
    return [
        ("Home", ""),
        ("Art", "art.html"),
        (plain_text(record.get("title", "")) or "Untitled artwork", page_rel_path(record)),
    ]


def artwork_json_ld(record: dict) -> str:
    payload = {
        "@context": "https://schema.org",
        "@type": "VisualArtwork",
        "@id": page_url(record) + "#artwork",
        "name": plain_text(record.get("title", "")) or "Untitled artwork",
        "url": page_url(record),
        "image": og_image_url(record),
        "dateCreated": created_date(record),
        "artform": "Drawing",
        "artMedium": "Ink on paper",
        "creator": {"@id": PERSON_ID},
        "isPartOf": {"@id": f"{SITE_ORIGIN}art.html#collection"},
        "sameAs": [str(record.get("flickr_url", ""))],
        "inLanguage": "en",
    }
    description = plain_text(record.get("desc", ""))
    if description:
        payload["description"] = description[:700]
    tags = [plain_text(tag) for tag in record.get("tags", [])][:TAG_LINK_CAP]
    if tags:
        payload["keywords"] = ", ".join(tags)
    license_url = str(record.get("license_url", "") or "")
    if license_url.startswith("https://creativecommons.org/"):
        payload["license"] = license_url
    else:
        payload["copyrightNotice"] = "© Daniel Ari Friedman. All rights reserved."
    return compact_json_ld(payload)


def compact_breadcrumb_script(trail: list[tuple[str, str]]) -> str:
    from docxology_tools.site_nav import breadcrumb_list_jsonld

    payload = compact_json_ld(breadcrumb_list_jsonld(trail))
    return f'    <script type="application/ld+json">\n{payload}\n    </script>'


def head_block(
    *,
    title: str,
    description: str,
    canonical: str,
    og_image: str,
    image_alt: str,
    robots: str = "index, follow",
    jsonld: str = "",
    breadcrumb_trail: list[tuple[str, str]] | None = None,
) -> str:
    social = social_meta_tags(title, description, og_image, image_alt=image_alt)
    breadcrumb_script = compact_breadcrumb_script(breadcrumb_trail) if breadcrumb_trail else ""
    return f"""<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{h(title)}</title>
    <meta name="description" content="{h(description)}">
    <meta name="robots" content="{robots}">
    <link rel="canonical" href="{h(canonical)}">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="application/json" href="/data/artworks.json" title="Artwork metadata JSON">
{HEAD_EXTRAS}
    <meta property="og:type" content="website">
    <meta property="og:title" content="{h(title)}">
    <meta property="og:description" content="{h(description)}">
    <meta property="og:url" content="{h(canonical)}">
    <meta property="og:image" content="{h(og_image)}">
{social}
    <link rel="stylesheet" href="../style.css?v={STYLE_VERSION}">
    <script type="application/ld+json">
{jsonld}
    </script>
{breadcrumb_script}
</head>"""


def render_artwork_page(record: dict, records: list[dict], index: int, collections: list[ArtCollection]) -> str:
    title = page_title(record)
    description = meta_description(record)
    canonical = page_url(record)
    image = og_image_url(record) or OG_ART_IMAGE
    alt = image_alt_text(record)
    thin = is_thin(record)
    robots = "noindex, follow" if thin else "index, follow"
    date = created_date(record)
    trail = breadcrumb_trail(record)

    prev_record = records[index - 1] if index > 0 else None
    next_record = records[index + 1] if index + 1 < len(records) else None
    related = [records[i] for i in related_artworks(index, records)]
    chips = record_collections(record, collections)

    tag_links = "\n".join(
        f'<a href="../art.html?q={quote(tag)}">{h(tag)}</a>' for tag in record.get("tags", [])[:TAG_LINK_CAP]
    )
    chip_links = "\n".join(
        f'<a href="../{COLLECTIONS_DIR_NAME}/{h(collection.slug)}.html">{h(collection.title)}</a>'
        for collection in chips
    )
    related_links = "\n".join(
        f'<li><a href="{h(page_filename(art))}">{h(plain_text(art.get("title", "")) or "Untitled artwork")}</a></li>'
        for art in related
    )
    prev_link = (
        f'<a href="{h(page_filename(prev_record))}" rel="prev">← {h(plain_text(prev_record.get("title", "")) or "Untitled artwork")}</a>'
        if prev_record
        else "<span></span>"
    )
    next_link = (
        f'<a href="{h(page_filename(next_record))}" rel="next">{h(plain_text(next_record.get("title", "")) or "Untitled artwork")} →</a>'
        if next_record
        else "<span></span>"
    )
    views = view_text(record)
    sizes = record.get("sizes", {})
    display_src = sizes.get("Medium 800") or sizes.get("Large") or image
    artwork_title = h(plain_text(record.get("title", "")) or "Untitled artwork")

    body = f"""    <header class="page-hero">
        <p class="eyebrow">Art</p>
        <h1>{artwork_title}</h1>
        <p class="sub">{date}{" · " + views if views else ""} · license: {license_html(record)}</p>
    </header>
    <main id="main" class="main">
        <section class="section artwork-layout">
            <div>
                <figure class="artwork-figure">
                    <img src="{h(display_src)}" alt="{h(alt)}" loading="eager" decoding="async">
                    <figcaption>{artwork_title} — pen and ink drawing</figcaption>
                </figure>
                <div class="tag-row">{tag_links}</div>
                <div class="collection-chips">{chip_links}</div>
            </div>
            <aside class="card">
                <h2>Details</h2>
                <ul class="meta-list">
                    <li><strong>Created:</strong> {date or "—"}</li>
                    <li><strong>License:</strong> {license_html(record)}</li>
                    <li><strong>Flickr ID:</strong> {h(record.get("id", ""))}</li>
                </ul>
                <p><a class="btn btn-outline" href="{h(record.get("flickr_url", ""))}" target="_blank" rel="noopener">View on Flickr ↗</a></p>
            </aside>
        </section>
        <section class="section">
            <div class="section-header"><h2>Description</h2><div class="section-divider"></div></div>
            <div class="artwork-desc">{description_paragraphs(record)}</div>
        </section>
        <section class="section">
            <div class="section-header"><h2>Related Works</h2><div class="section-divider"></div></div>
            <ul class="meta-list">{related_links}</ul>
            <div class="pager">{prev_link}{next_link}</div>
        </section>
    </main>
    <footer role="contentinfo"><div class="footer-rule" aria-hidden="true"></div><p>Daniel Ari Friedman - <a href="../artworks/">Artwork index</a> - <a href="../data/artworks.json">artwork JSON</a> - <a href="{FLICKR_PROFILE_URL}" target="_blank" rel="noopener">Flickr archive</a></p></footer>"""
    return _page_shell(
        head=head_block(
            title=title,
            description=description,
            canonical=canonical,
            og_image=image,
            image_alt=alt,
            robots=robots,
            jsonld=artwork_json_ld(record),
            breadcrumb_trail=trail,
        ),
        body=body,
        breadcrumb_html=render_breadcrumb(trail, depth=1),
    )


def list_item_html(record: dict) -> str:
    title = plain_text(record.get("title", "")) or "Untitled artwork"
    date = created_date(record)
    views = view_text(record)
    meta = " · ".join(part for part in (date, views) if part)
    suffix = f' <span class="muted">{h(meta)}</span>' if meta else ""
    return f'      <li><a href="../{h(page_rel_path(record))}">{h(title)}</a>{suffix}</li>'


def clip_title(title: str, max_len: int = 65) -> str:
    """Clip a hub page title to the SERP budget on word boundaries."""
    if len(title) <= max_len:
        return title
    cut = title[: max_len - 1].rsplit(" ", 1)[0].rstrip(" ,;:.–—-")
    return (cut or title[: max_len - 1].rstrip()) + "…"


def render_artworks_index(payload: dict, collections: list[ArtCollection]) -> str:
    records = payload.get("artworks", [])
    count = len(records)
    title = "Artwork Index — Daniel Ari Friedman"
    description = clip_description(
        f"Complete crawlable index of Daniel Ari Friedman's {count} pen-and-ink drawings, "
        "each with its own page, description, tags, license, and Flickr backlink."
    )
    rel_path = ARTWORKS_INDEX_PATH
    canonical = SITE_ORIGIN + "artworks/"
    trail = [("Home", ""), ("Art", "art.html"), ("Artwork Index", rel_path)]
    collection_links = "\n".join(
        f'      <li><a href="../{COLLECTIONS_DIR_NAME}/{h(collection.slug)}.html">{h(collection.title)}</a></li>'
        for collection in collections
    )
    items = "\n".join(list_item_html(record) for record in records)
    jsonld = compact_json_ld(
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "@id": canonical + "#collection",
            "name": title,
            "url": canonical,
            "description": description,
            "creator": {"@id": PERSON_ID},
            "isPartOf": {"@id": SITE_ORIGIN + "#website"},
            "numberOfItems": count,
        }
    )
    body = f"""    <header class="page-hero">
        <p class="eyebrow">Art</p>
        <h1>Artwork Index</h1>
        <p class="sub">Every drawing has its own static page — {count} total. The interactive, filterable gallery lives at <a href="../art.html">art.html</a>; the structured export is <a href="../data/artworks.json">data/artworks.json</a>.</p>
    </header>
    <main id="main" class="main">
        <section class="section">
            <div class="section-header"><h2>Curated Collections</h2><div class="section-divider"></div></div>
            <ul class="artwork-list">
{collection_links}
            </ul>
        </section>
        <section class="section">
            <div class="section-header"><h2>All Works</h2><p>One plain-HTML page per drawing, newest upload first. This list needs no JavaScript.</p><div class="section-divider"></div></div>
            <ul class="artwork-list">
{items}
            </ul>
        </section>
    </main>
    <footer role="contentinfo"><div class="footer-rule" aria-hidden="true"></div><p>Daniel Ari Friedman - <a href="../art.html">Art gallery</a> - <a href="../data/artworks.json">artwork JSON</a> - <a href="{FLICKR_PROFILE_URL}" target="_blank" rel="noopener">Flickr archive</a></p></footer>"""
    return _page_shell(
        head=head_block(
            title=title,
            description=description,
            canonical=canonical,
            og_image=OG_ART_IMAGE,
            image_alt=title,
            jsonld=jsonld,
            breadcrumb_trail=trail,
        ),
        body=body,
        breadcrumb_html=render_breadcrumb(trail, depth=1),
    )


def render_collection_page(collection: ArtCollection, records: list[dict], collections: list[ArtCollection]) -> str:
    members = members_for(collection, records)
    count = len(members)
    title = clip_title(f"{collection.title} — Art by Daniel Ari Friedman")
    description = clip_description(f"{collection.title} — {collection.intro}")
    rel_path = f"{COLLECTIONS_DIR_NAME}/{collection.slug}.html"
    canonical = SITE_ORIGIN + rel_path
    trail = [("Home", ""), ("Art", "art.html"), (collection.title, rel_path)]

    item_list = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": collection.title,
        "numberOfItems": count,
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": position,
                "name": plain_text(record.get("title", "")) or "Untitled artwork",
                "url": page_url(record),
            }
            for position, record in enumerate(members, start=1)
        ],
    }
    jsonld = compact_json_ld(
        {
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "@id": canonical + "#collection",
            "name": collection.title,
            "url": canonical,
            "description": description,
            "creator": {"@id": PERSON_ID},
            "isPartOf": {"@id": SITE_ORIGIN + "#website"},
            "mainEntity": item_list,
        }
    )
    sibling_links = "\n".join(
        f'      <li><a href="{h(other.slug)}.html">{h(other.title)}</a></li>'
        for other in collections
        if other.slug != collection.slug
    )
    items = "\n".join(list_item_html(record) for record in members) or '      <li class="muted">No works match this collection yet.</li>'
    body = f"""    <header class="page-hero">
        <p class="eyebrow">Art collection · {count} works</p>
        <h1>{h(collection.title)}</h1>
        <p class="sub">{h(collection.intro)}</p>
    </header>
    <main id="main" class="main">
        <section class="section">
            <div class="section-header"><h2>Works in this collection</h2><div class="section-divider"></div></div>
            <ul class="artwork-list">
{items}
            </ul>
        </section>
        <section class="section">
            <div class="section-header"><h2>Other collections</h2><div class="section-divider"></div></div>
            <ul class="artwork-list">
{sibling_links}
            </ul>
        </section>
    </main>
    <footer role="contentinfo"><div class="footer-rule" aria-hidden="true"></div><p>Daniel Ari Friedman - <a href="../art.html">Art gallery</a> - <a href="../artworks/">Artwork index</a> - <a href="{FLICKR_PROFILE_URL}" target="_blank" rel="noopener">Flickr archive</a></p></footer>"""
    return _page_shell(
        head=head_block(
            title=title,
            description=description,
            canonical=canonical,
            og_image=OG_ART_IMAGE,
            image_alt=title,
            jsonld=jsonld,
            breadcrumb_trail=trail,
        ),
        body=body,
        breadcrumb_html=render_breadcrumb(trail, depth=1),
    )


def _page_shell(*, head: str, body: str, breadcrumb_html: str = "") -> str:
    """Shared DOCTYPE/nav/footer wrapper. Page CSS lives in style.css once —
    944 per-artwork pages must not duplicate it inline (artifact budget)."""
    return f"""<!DOCTYPE html>
{ARTWORK_PAGE_MARKER}
<html lang="en">
{head}
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
{render_nav(active="art", depth=1)}
{breadcrumb_html}
{body}
{INTERACTIVE_SCRIPTS}
{MENU_ESC_SCRIPT}
</body>
</html>
"""


def render_manifest(paths: set[str]) -> str:
    payload = {
        "schema_version": ARTWORK_PAGES_MANIFEST_VERSION,
        "pages": sorted(paths),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def expected_page_paths(rendered_outputs: dict[Path, str]) -> set[str]:
    return {path.relative_to(REPO_ROOT).as_posix() for path in rendered_outputs if path.suffix == ".html"}


def outputs() -> dict[Path, str]:
    payload = load_payload()
    records = payload.get("artworks", [])
    collections = load_collections()
    out: dict[Path, str] = {}
    for index, record in enumerate(records):
        out[REPO_ROOT / page_rel_path(record)] = render_artwork_page(record, records, index, collections)
    out[REPO_ROOT / ARTWORKS_INDEX_PATH] = render_artworks_index(payload, collections)
    for collection in collections:
        out[REPO_ROOT / COLLECTIONS_DIR_NAME / f"{collection.slug}.html"] = render_collection_page(
            collection, records, collections
        )
    out[MANIFEST_OUT] = render_manifest(expected_page_paths(out))
    return out


def check_interactive_page_integrity(rendered_outputs: dict[Path, str]) -> tuple[str, ...]:
    """Every emitted page that loads interactive/tts scripts must link style.css."""
    errors: list[str] = []
    for path, content in rendered_outputs.items():
        if "/js/tts-controls.js" in content and "style.css" not in content:
            errors.append(f"{path.relative_to(REPO_ROOT).as_posix()}: loads interactive scripts but does not link style.css")
    return tuple(errors)


def owned_generated_pages(directory: Path) -> list[Path]:
    """Existing renderer-owned pages (marker present) in one output directory."""
    if not directory.is_dir():
        return []
    owned: list[Path] = []
    for path in sorted(directory.glob("*.html")):
        text = read_generated_output_text(REPO_ROOT, path)
        if text is not None and ARTWORK_PAGE_MARKER in text:
            owned.append(path)
    return owned


def generated_artwork_page_orphans(rendered_outputs: dict[Path, str]) -> tuple[tuple[Path, ...], tuple[str, ...]]:
    """Return managed artwork/collection pages no longer produced, never deleting files."""
    current = expected_page_paths(rendered_outputs)
    orphans: list[Path] = []
    for directory in (ARTWORKS_DIR, COLLECTIONS_DIR):
        for path in owned_generated_pages(directory):
            if path.relative_to(REPO_ROOT).as_posix() not in current:
                orphans.append(path)
    return tuple(orphans), ()


def stale_outputs(rendered_outputs: dict[Path, str]) -> tuple[str, ...]:
    stale: list[str] = []
    for path, content in sorted(rendered_outputs.items()):
        existing = read_generated_output_text(REPO_ROOT, path)
        if existing != content:
            stale.append(path.relative_to(REPO_ROOT).as_posix())
    for orphan in generated_artwork_page_orphans(rendered_outputs)[0]:
        stale.append(orphan.relative_to(REPO_ROOT).as_posix() + " (orphan)")
    stale.extend(check_interactive_page_integrity(rendered_outputs))
    return tuple(stale)


def prune_owned(rendered_outputs: dict[Path, str]) -> int:
    """Delete renderer-owned orphan pages (manual, explicit — like work pages)."""
    orphans, _errors = generated_artwork_page_orphans(rendered_outputs)
    for path in orphans:
        path.unlink()
        print(f"pruned {path.relative_to(REPO_ROOT).as_posix()}")
    return len(orphans)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if any rendered output differs from disk")
    parser.add_argument(
        "--prune-owned",
        action="store_true",
        help="Delete renderer-owned artwork/collection pages the current data no longer produces",
    )
    args = parser.parse_args()

    rendered = outputs()
    if args.prune_owned:
        raise SystemExit(prune_owned(rendered))
    if args.check:
        stale = stale_outputs(rendered)
        if stale:
            raise SystemExit(f"stale artwork outputs ({len(stale)}): " + ", ".join(stale[:8]))
        print("checked artwork pages")
        return
    for path, content in sorted(rendered.items()):
        target = safe_generated_output_path(REPO_ROOT, path)
        write_generated_output_text(REPO_ROOT, target, content)
    pages = sum(1 for path in rendered if path.suffix == ".html")
    print(f"wrote {pages} artwork/collection pages + manifest")


if __name__ == "__main__":
    main()
