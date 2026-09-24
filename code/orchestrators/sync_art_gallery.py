#!/usr/bin/env python3
"""Sync the SSR crawler floor in hand-authored ``art.html`` with the artwork export.

``art.html`` is hand-authored; its interactive grid is client-rendered by
``js/art-gallery.js`` from the compact index. The only generated region is the
marker-delimited SSR block (``<!-- docxology:ssr-gallery-cards ... -->``):
the newest tiles server-rendered so crawlers and no-JS visitors reach real
artwork pages without JavaScript. This in-place patcher is the single writer of
that block — the one-time source of those tiles (a manual paste) went stale the
moment the Flickr sync refreshed the export (newest artwork first, and every
tile now links its ``artworks/<id>-<slug>.html`` page).

- Tiles render as ``<a class="art-card" href="artworks/...">`` so every grid
  entry is a real link; the lightbox stays progressive enhancement
  (``js/art-gallery.js`` preventDefaults the click).
- Thumbnails keep the ``_z`` size and the ``art-thumb ssr`` classes the
  hydration tests pin; no width/height attributes (NEW-1 contract).
- ``--check`` verifies the rendered block matches disk without writing.

The count heading, JSON-LD ``numberOfItems``, and og:description counts in
``art.html`` remain ``sync_site_facts.py``'s responsibility.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]
TARGET = REPO_ROOT / "art.html"
SOURCE = REPO_ROOT / "data" / "artworks.json"

SSR_FLOOR_ROWS = 30
BLOCK_START = re.compile(r"<!-- docxology:ssr-gallery-cards[^>]*-->")
# The SSR block ends at the gallery grid's own closing tag (4-space indent on
# its own line). Tile markup contains inline </div>s, so a bare "</div>" find
# would splice mid-tile — the exact bug that duplicated the block once.
GRID_CLOSE = re.compile(r"\n    </div>")

from docxology_tools.artwork_pages import image_alt_text, page_rel_path, plain_text  # noqa: E402


def h(value: object) -> str:
    return escape(str(value), quote=True)


def load_records() -> list[dict]:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    return payload.get("artworks", [])


def tile_html(record: dict) -> str:
    """One SSR tile exactly as the hydration layer expects to reuse it."""
    title = plain_text(record.get("title", "")) or "Untitled artwork"
    date = str(record.get("date", ""))[:10]
    thumb = record.get("sizes", {}).get("Medium 640") or str(record.get("thumb", "")).replace("_m.jpg", "_z.jpg")
    try:
        views = f"{int(str(record.get('views', '0'))) :,} views"
    except ValueError:
        views = ""
    return (
        f'      <a class="art-card" href="{h(page_rel_path(record))}" '
        f'aria-label="Open artwork: {h(title)}">'
        f'<img src="{h(thumb)}" alt="{h(image_alt_text(record))}" class="art-thumb ssr" '
        f'loading="lazy" decoding="async">'
        f'<div class="art-info">'
        f'<div class="art-title">{h(title)}</div>'
        f'<div class="art-meta">{h(date)}</div>'
        + (f'<div class="art-views">{h(views)}</div>' if views else "")
        + "</div></a>"
    )


def render_block(records: list[dict]) -> str:
    tiles = "\n".join(tile_html(record) for record in records[:SSR_FLOOR_ROWS])
    return (
        f"<!-- docxology:ssr-gallery-cards (first {SSR_FLOOR_ROWS}; no-JS/crawler content; "
        f"hydrated by js/art-gallery.js; maintained by code/orchestrators/sync_art_gallery.py) -->\n"
        f"{tiles}"
    )


def patched_html(html: str, records: list[dict]) -> tuple[str, bool]:
    """Replace the marker-delimited block; return (html, changed)."""
    start = BLOCK_START.search(html)
    if not start:
        raise SystemExit("art.html: SSR gallery marker not found — block ownership is unclear, refusing to patch")
    close = GRID_CLOSE.search(html, start.end())
    if not close:
        raise SystemExit("art.html: grid closing </div> not found after the SSR marker")
    updated = html[: start.start()] + render_block(records) + html[close.start() :]
    return updated, updated != html


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the SSR gallery block is stale")
    args = parser.parse_args()
    original = TARGET.read_text(encoding="utf-8")
    updated, changed = patched_html(original, load_records())
    if args.check:
        if changed:
            raise SystemExit("art.html SSR gallery block is stale (run sync_art_gallery.py)")
        print("checked art.html SSR gallery block")
        return
    if changed:
        TARGET.write_text(updated, encoding="utf-8")
        print("updated art.html SSR gallery block")
    else:
        print("art.html SSR gallery block already current")


if __name__ == "__main__":
    main()
