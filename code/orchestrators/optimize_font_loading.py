#!/usr/bin/env python3
"""Make Google Fonts non-render-blocking across all HTML pages.

Converts:
  <link href="...fonts.googleapis.com/css2..." rel="stylesheet">
To:
  <link href="...fonts.googleapis.com/css2..." rel="stylesheet" media="print" data-media-swap="all">

The stylesheet loads with media="print" (non-render-blocking) and
js/interactive.js swaps it to media="all" once the DOM is parsed.
The classic web.dev inline onload="this.media='all'" pattern is NOT used
because the site CSP (script-src 'self') blocks inline event handlers —
it shipped once and silently broke font loading on every converted page.
The font-display: swap parameter is already in the URL, so text remains
visible during font load.

Idempotent — only modifies links that don't already have the pattern, and
migrates any legacy onload variant to the CSP-safe attribute form.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

PATTERN = re.compile(
    r'<link\s+href="(https://fonts\.googleapis\.com/css2[^"]*)"\s+rel="stylesheet"\s*>'
)
REPLACEMENT = r'<link href="\1" rel="stylesheet" media="print" data-media-swap="all">'

# Already-converted pattern (skip these)
ALREADY_DONE = re.compile(r'media="print" data-media-swap="all"')

# Legacy CSP-incompatible variants (inline onload, with or without the
# stray backslash-escaping a previous sed pass introduced) → migrate.
LEGACY_ONLOAD = re.compile(
    r'media="print" onload="this\.media=\\?\'all\\?\'"'
)


def fix_file(path: Path) -> bool:
    """Fix one HTML file. Returns True if changed."""
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8")
    new_content = LEGACY_ONLOAD.sub('media="print" data-media-swap="all"', content)
    if not ALREADY_DONE.search(new_content):
        new_content = PATTERN.sub(REPLACEMENT, new_content)
    if new_content != content:
        path.write_text(new_content, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    skipped = 0
    for html in sorted(REPO_ROOT.glob("*.html")):
        if fix_file(html):
            print(f"  FIXED: {html.name}")
            changed += 1
        else:
            skipped += 1
    print("\n=== Summary ===")
    print(f"  Fixed: {changed}")
    print(f"  Skipped (already done or no match): {skipped}")


if __name__ == "__main__":
    main()
