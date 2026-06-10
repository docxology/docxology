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
_HAS_TWITTER = re.compile(r'<meta\s+name="twitter:card"', re.I)
_HAS_ALT = re.compile(r'<meta\s+property="og:image:alt"', re.I)


def _social_block(indent: str, title: str, desc: str, image: str, *, need_alt: bool) -> str:
    lines = []
    if need_alt:
        lines.append(f'{indent}<meta property="og:image:alt" content="{title}">')
    lines += [
        f'{indent}<meta name="twitter:card" content="summary_large_image">',
        f'{indent}<meta name="twitter:title" content="{title}">',
        f'{indent}<meta name="twitter:description" content="{desc}">',
        f'{indent}<meta name="twitter:image" content="{image}">',
    ]
    return "\n".join(lines)


def transform(html: str) -> str:
    """Insert social tags after og:image:height if not already present."""
    if _HAS_TWITTER.search(html) and _HAS_ALT.search(html):
        return html
    title_m, desc_m, image_m = _OG_TITLE.search(html), _OG_DESC.search(html), _OG_IMAGE.search(html)
    height_m = _OG_HEIGHT.search(html)
    if not (title_m and desc_m and image_m and height_m):
        return html  # leave pages we cannot safely derive from untouched
    indent = height_m.group(1)
    block = _social_block(
        indent,
        title_m.group(1),
        desc_m.group(1),
        image_m.group(1),
        need_alt=not _HAS_ALT.search(html),
    )
    if _HAS_TWITTER.search(html):  # only og:image:alt missing
        block = "\n".join(
            line for line in block.splitlines() if "og:image:alt" in line
        )
    insert_at = height_m.end()
    return html[:insert_at] + "\n" + block + html[insert_at:]


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
