#!/usr/bin/env python3
"""
Migrate inline event handlers (onclick, onchange, onsubmit) to data-*
attributes so interactive.js can wire them via addEventListener.

Transformations:
  - onclick="var o=...toggle('open')..."  → removed (wiring is bound by class
    on `.menu-btn` in js/interactive.js, so no data attribute is needed)
  - onclick="showTab(event,'video')"      → data-tab="video"
  - onclick="setTypeFilter('Paper',this)" → data-type-filter="Paper"
  - onchange="setYearFilter(this.value)"  → data-year-filter
  - onchange="setVenueFilter(this.value)" → data-venue-filter
  - onchange="filterPubs()"               → data-filter-pubs
  - onsubmit="return false"               → data-no-submit
  - onclick="setSize('sm')"               → data-set-size="sm"
  - onclick="closeLightbox()"             → data-lightbox="close"
  - onclick="navLightbox(-1)"             → data-lightbox="prev"
  - onclick="navLightbox(1)"              → data-lightbox="next"
  - onchange="filterGallery()"            → data-filter-gallery

All inline on* attributes are removed after conversion. Handlers that
don't match a known pattern are left in place with a warning.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

SKIP_PAGES = {
    "googlef0f1a1a4a7ba4be8.html",
    "about.html",
    "meditations.html",
    "nft.html",
    "research.html",
}


def is_redirect_stub(html: str) -> bool:
    match = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', html, re.I)
    return bool(match and "noindex" in match.group(1))


def migrate_nav_toggle(html: str) -> str:
    """Replace the nav-toggle inline onclick with data-nav-toggle."""
    pattern = re.compile(
        r'<button([^>]*?)\s*onclick="var o=document\.querySelector\(\'.nav-links\'\)\.classList\.toggle\(\'open\'\);this\.setAttribute\(\'aria-expanded\',o\)"([^>]*?)>',
        re.I,
    )

    def replace(m: re.Match) -> str:
        before = m.group(1)
        after = m.group(2)
        return f"<button{before}{after}>"

    return pattern.sub(replace, html)


def migrate_show_tab(html: str) -> str:
    """Replace onclick="showTab(event,'name')" with data-tab="name"."""
    pattern = re.compile(
        r'onclick="showTab\(event,\'(\w+)\'\)"', re.I
    )

    def replace(m: re.Match) -> str:
        tab_name = m.group(1)
        return f'data-tab="{tab_name}"'

    return pattern.sub(replace, html)


def migrate_set_type_filter(html: str) -> str:
    """Replace onclick="setTypeFilter('X',this)" with data-type-filter="X"."""
    pattern = re.compile(
        r'onclick="setTypeFilter\(\'([^\']*)\',this\)"', re.I
    )

    def replace(m: re.Match) -> str:
        filter_val = m.group(1)
        return f'data-type-filter="{filter_val}"'

    return pattern.sub(replace, html)


def migrate_year_filter(html: str) -> str:
    """Replace onchange="setYearFilter(this.value)" with data-year-filter."""
    return re.sub(
        r'onchange="setYearFilter\(this\.value\)"',
        'data-year-filter',
        html,
        flags=re.I,
    )


def migrate_venue_filter(html: str) -> str:
    """Replace onchange="setVenueFilter(this.value)" with data-venue-filter."""
    return re.sub(
        r'onchange="setVenueFilter\(this\.value\)"',
        'data-venue-filter',
        html,
        flags=re.I,
    )


def migrate_filter_pubs(html: str) -> str:
    """Replace onchange="filterPubs()" with data-filter-pubs."""
    return re.sub(
        r'onchange="filterPubs\(\)"',
        'data-filter-pubs',
        html,
        flags=re.I,
    )


def migrate_onsubmit(html: str) -> str:
    """Replace onsubmit="return false" with data-no-submit."""
    return re.sub(
        r'onsubmit="return false"',
        'data-no-submit',
        html,
        flags=re.I,
    )


def migrate_set_size(html: str) -> str:
    """Replace onclick="setSize('sm')" with data-set-size="sm"."""
    pattern = re.compile(
        r'onclick="setSize\(\'(\w+)\'\)"', re.I
    )

    def replace(m: re.Match) -> str:
        size = m.group(1)
        return f'data-set-size="{size}"'

    return pattern.sub(replace, html)


def migrate_lightbox(html: str) -> str:
    """Replace onclick="closeLightbox()" / "navLightbox(N)" with data-lightbox."""
    html = re.sub(
        r'onclick="closeLightbox\(\)"',
        'data-lightbox="close"',
        html,
        flags=re.I,
    )
    html = re.sub(
        r'onclick="navLightbox\(-1\)"',
        'data-lightbox="prev"',
        html,
        flags=re.I,
    )
    html = re.sub(
        r'onclick="navLightbox\(1\)"',
        'data-lightbox="next"',
        html,
        flags=re.I,
    )
    return html


def migrate_filter_gallery(html: str) -> str:
    """Replace onchange="filterGallery()" with data-filter-gallery."""
    return re.sub(
        r'onchange="filterGallery\(\)"',
        'data-filter-gallery',
        html,
        flags=re.I,
    )


def migrate_set_domain_filter(html: str) -> str:
    """Replace onclick="setDomainFilter('X',this)" with data-domain-filter="X"."""
    pattern = re.compile(
        r'onclick="setDomainFilter\(\'([^\']*)\',this\)"', re.I
    )

    def replace(m: re.Match) -> str:
        filter_val = m.group(1)
        return f'data-domain-filter="{filter_val}"'

    return pattern.sub(replace, html)


def migrate_sort_by(html: str) -> str:
    """Replace onclick="sortBy('X')" with data-sort-by="X"."""
    pattern = re.compile(
        r'onclick="sortBy\(\'([^\']*)\'\)"', re.I
    )

    def replace(m: re.Match) -> str:
        sort_val = m.group(1)
        return f'data-sort-by="{sort_val}"'

    return pattern.sub(replace, html)


def migrate_reset_filters(html: str) -> str:
    """Replace onclick="resetFilters()" with data-reset-filters."""
    return re.sub(
        r'onclick="resetFilters\(\)"',
        'data-reset-filters',
        html,
        flags=re.I,
    )


def migrate_set_channel(html: str) -> str:
    """Replace onclick="setChannel('X',this)" with data-channel="X"."""
    pattern = re.compile(
        r'onclick="setChannel\(\'([^\']*)\',this\)"', re.I
    )

    def replace(m: re.Match) -> str:
        channel = m.group(1)
        return f'data-channel="{channel}"'

    return pattern.sub(replace, html)


def migrate_set_zoom(html: str) -> str:
    """Replace onclick="setZoom(N,this)" with data-zoom="N"."""
    pattern = re.compile(
        r'onclick="setZoom\((\d+),this\)"', re.I
    )

    def replace(m: re.Match) -> str:
        zoom = m.group(1)
        return f'data-zoom="{zoom}"'

    return pattern.sub(replace, html)


def count_remaining_handlers(html: str) -> list[str]:
    """Find any remaining inline on* handlers."""
    pattern = re.compile(r'\son(click|change|submit|load|error|mouseover|mouseout|keyup|keydown)="', re.I)
    return pattern.findall(html)


def process_file(path: Path) -> dict:
    html = path.read_text(encoding="utf-8")

    if is_redirect_stub(html) or path.name in SKIP_PAGES:
        return {"file": path.name, "skipped": True}

    original = html
    html = migrate_nav_toggle(html)
    html = migrate_show_tab(html)
    html = migrate_set_type_filter(html)
    html = migrate_set_domain_filter(html)
    html = migrate_sort_by(html)
    html = migrate_reset_filters(html)
    html = migrate_set_channel(html)
    html = migrate_set_zoom(html)
    html = migrate_year_filter(html)
    html = migrate_venue_filter(html)
    html = migrate_filter_pubs(html)
    html = migrate_onsubmit(html)
    html = migrate_set_size(html)
    html = migrate_lightbox(html)
    html = migrate_filter_gallery(html)

    remaining = count_remaining_handlers(html)

    if html != original:
        path.write_text(html, encoding="utf-8")

    return {
        "file": path.name,
        "changed": html != original,
        "remaining": remaining,
    }


def main() -> None:
    html_files = sorted(REPO_ROOT.glob("*.html"))
    total_changed = 0
    total_remaining = 0

    for f in html_files:
        result = process_file(f)
        if result.get("skipped"):
            print(f"  SKIP  {result['file']}")
            continue

        status = "MIGRATE" if result["changed"] else "OK"
        remaining = result.get("remaining", [])
        if remaining:
            print(f"  {status:7s} {result['file']}: {len(remaining)} remaining handlers: {set(remaining)}")
            total_remaining += len(remaining)
        else:
            print(f"  {status:7s} {result['file']}")
        if result["changed"]:
            total_changed += 1

    print(f"\n{total_changed} file(s) migrated, {total_remaining} remaining handler(s)")


if __name__ == "__main__":
    main()
