#!/usr/bin/env python3
"""Build sitemap-images.xml: a Google image sitemap for the art gallery.

The gallery (art.html) presents 900+ pen-and-ink drawings. The page is rendered
client-side from data/artworks.json, so the images are not visible to crawlers in
the static HTML. This sitemap declares each artwork image explicitly so Google
Images can discover them, preferring the same-domain copies served from /art/
(stronger ownership signal) and falling back to the source Flickr URL when no
local file is present.

Outputs: sitemap-images.xml
Sources: data/artworks.json, local files under art/
Rebuild: python3 code/orchestrators/build_image_sitemap.py   (--check to verify)
"""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from urllib.parse import quote

REPO_ROOT = Path(__file__).resolve().parents[2]
ART_DIR = REPO_ROOT / "art"
ARTWORKS_JSON = REPO_ROOT / "data" / "artworks.json"
OUT = REPO_ROOT / "sitemap-images.xml"
SITE = "https://danielarifriedman.com/"
GALLERY_URL = SITE + "art.html"
# Google allows up to 1000 images per <url> entry.
MAX_IMAGES_PER_URL = 1000


def load_artworks() -> list[dict]:
    data = json.loads(ARTWORKS_JSON.read_text(encoding="utf-8"))
    return data["artworks"] if isinstance(data, dict) else data


def local_files_by_id() -> dict[str, str]:
    """Map artwork id (numeric filename prefix) -> local art/ filename."""
    out: dict[str, str] = {}
    if not ART_DIR.is_dir():
        return out
    for p in ART_DIR.glob("*.jpg"):
        prefix = p.name.split("_", 1)[0]
        if prefix.isdigit():
            out.setdefault(prefix, p.name)
    return out


def best_flickr_url(art: dict) -> str | None:
    sizes = art.get("sizes") or {}
    for key in ("Original", "X-Large 3K", "Large 2048", "Large 1600", "Large", "Medium 800", "Medium"):
        if sizes.get(key):
            return sizes[key]
    return art.get("thumb")


def _absolutize(loc: str | None) -> str | None:
    """Sitemap image locs must be absolute URLs."""
    if not loc:
        return None
    if loc.startswith(("http://", "https://")):
        return loc
    return SITE + quote(loc.lstrip("/"))


def image_loc(art: dict, local: dict[str, str]) -> str | None:
    fname = local.get(str(art.get("id")))
    if fname:
        return SITE + "art/" + quote(fname)
    return _absolutize(best_flickr_url(art))


def render(artworks: list[dict], local: dict[str, str]) -> str:
    seen: set[str] = set()
    blocks: list[str] = []
    for art in artworks:
        loc = image_loc(art, local)
        if not loc or loc in seen:
            continue
        seen.add(loc)
        title = html.escape(str(art.get("title") or "Untitled artwork"), quote=True)
        blocks.append(
            "    <image:image>\n"
            f"      <image:loc>{html.escape(loc, quote=True)}</image:loc>\n"
            f"      <image:title>{title}</image:title>\n"
            "    </image:image>"
        )
        if len(blocks) >= MAX_IMAGES_PER_URL:
            break
    images = "\n".join(blocks)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
        "  <url>\n"
        f"    <loc>{GALLERY_URL}</loc>\n"
        f"{images}\n"
        "  </url>\n"
        "</urlset>\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if sitemap-images.xml is stale")
    args = parser.parse_args()
    artworks = load_artworks()
    content = render(artworks, local_files_by_id())
    count = content.count("<image:image>")
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Stale sitemap-images.xml")
        print(f"checked sitemap-images.xml ({count} images)")
        return
    OUT.write_text(content, encoding="utf-8")
    print(f"wrote sitemap-images.xml ({count} images)")


if __name__ == "__main__":
    main()
