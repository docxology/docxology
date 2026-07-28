#!/usr/bin/env python3
"""Ensure hand-maintained pages carry Twitter Card + og:image:alt tags.

The generator-built pages (work, domain, catalog, exports, evidence, updates,
repository inventory) emit Twitter Card and og:image:alt tags from their own
templates. The pages in PAGES below are authored by hand and have no generator,
so this idempotent pass injects the same social tags, derived from each page's
existing Open Graph values, immediately after the og:image:height line.

Usage:
    python3 code/orchestrators/ensure_social_meta.py          # apply in place
    python3 code/orchestrators/ensure_social_meta.py --check   # exit 1 if stale
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Hand-maintained, indexable pages (no dedicated generator).
PAGES: tuple[str, ...] = (
    "index.html",
    "publications.html",
    "art.html",
    "videos.html",
    "collaborators.html",
    "search.html",
    "discovery.html",
    "cite-verify.html",
    "media.html",
    "software.html",
)

_OG = lambda prop: re.compile(  # noqa: E731
    rf'<meta\s+property="og:{prop}"\s+content="([^"]*)"', re.I
)
_OG_TITLE = _OG("title")
_OG_DESC = _OG("description")
_OG_IMAGE = _OG("image")
_OG_HEIGHT = re.compile(r'([ \t]*)<meta\s+property="og:image:height"[^>]*>', re.I)
_OG_ALT_LINE = re.compile(r'[ \t]*<meta\s+property="og:image:alt"[^>]*>', re.I)
_TW_IMAGE_LINE = re.compile(r'[ \t]*<meta\s+name="twitter:image"\s+content="[^"]*"[^>]*>', re.I)
_HAS_TWITTER = re.compile(r'<meta\s+name="twitter:card"', re.I)
_HAS_ALT = re.compile(r'<meta\s+property="og:image:alt"', re.I)
_HAS_TW_IMG_ALT = re.compile(r'<meta\s+name="twitter:image:alt"', re.I)


def _insert_after(html: str, anchor: re.Pattern[str], line: str) -> str:
    """Insert ``line`` on its own line immediately after the anchor match."""
    match = anchor.search(html)
    if not match:
        return html
    return html[: match.end()] + "\n" + line + html[match.end() :]


def transform(html: str) -> str:
    """Idempotently ensure og:image:alt, the Twitter summary card, and
    twitter:image:alt are present, all derived from the page's existing Open
    Graph values. Safe to run repeatedly; only inserts what is missing."""
    if _HAS_TWITTER.search(html) and _HAS_ALT.search(html) and _HAS_TW_IMG_ALT.search(html):
        return html
    title_m, desc_m, image_m = _OG_TITLE.search(html), _OG_DESC.search(html), _OG_IMAGE.search(html)
    height_m = _OG_HEIGHT.search(html)
    if not (title_m and desc_m and image_m and height_m):
        return html  # leave pages we cannot safely derive from untouched
    indent = height_m.group(1)
    title, desc, image = title_m.group(1), desc_m.group(1), image_m.group(1)

    # og:image:alt — directly after og:image:height.
    if not _HAS_ALT.search(html):
        html = _insert_after(html, _OG_HEIGHT, f'{indent}<meta property="og:image:alt" content="{title}">')

    if not _HAS_TWITTER.search(html):
        # No Twitter card at all — inject the full card after og:image:alt.
        card = "\n".join([
            f'{indent}<meta name="twitter:card" content="summary_large_image">',
            f'{indent}<meta name="twitter:title" content="{title}">',
            f'{indent}<meta name="twitter:description" content="{desc}">',
            f'{indent}<meta name="twitter:image" content="{image}">',
            f'{indent}<meta name="twitter:image:alt" content="{title}">',
        ])
        html = _insert_after(html, _OG_ALT_LINE, card)
    elif not _HAS_TW_IMG_ALT.search(html):
        # Card predates twitter:image:alt — add just that line after twitter:image.
        html = _insert_after(html, _TW_IMAGE_LINE, f'{indent}<meta name="twitter:image:alt" content="{title}">')

    return html


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if any page is stale")
    args = parser.parse_args()
    stale: list[str] = []
    changed = 0
    for rel in PAGES:
        path = REPO_ROOT / rel
        if not path.is_file():
            stale.append(f"missing: {rel}")
            continue
        original = path.read_text(encoding="utf-8")
        updated = transform(original)
        if updated == original:
            continue
        if args.check:
            stale.append(rel)
        else:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    if stale:
        raise SystemExit("Pages missing social meta: " + ", ".join(stale))
    print(f"{'checked' if args.check else 'updated'} social meta on {len(PAGES)} pages"
          + ("" if args.check else f" ({changed} changed)"))


if __name__ == "__main__":
    main()
