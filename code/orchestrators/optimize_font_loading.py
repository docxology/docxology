#!/usr/bin/env python3
"""Make Google Fonts non-render-blocking across all HTML pages.

Converts:
  <link href="...fonts.googleapis.com/css2..." rel="stylesheet">
To:
  <link href="...fonts.googleapis.com/css2..." rel="stylesheet" media="print" onload="this.media='all'">

This uses the media="print" onload pattern recommended by web.dev for
non-blocking CSS loading. The font-display: swap parameter is already
in the URL, so text remains visible during font load.

Idempotent — only modifies links that don't already have the pattern.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

PATTERN = re.compile(
    r'<link\s+href="(https://fonts\.googleapis\.com/css2[^"]*)"\s+rel="stylesheet"\s*>'
)
REPLACEMENT = r'<link href="\1" rel="stylesheet" media="print" onload="this.media=\'all\'">'

# Already-converted pattern (skip these)
ALREADY_DONE = re.compile(r"media=\"print\" onload=\"this\.media='all'\"")


def fix_file(path: Path) -> bool:
    """Fix one HTML file. Returns True if changed."""
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8")
    if ALREADY_DONE.search(content):
        return False  # Already fixed
    new_content = PATTERN.sub(REPLACEMENT, content)
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
    print(f"\n=== Summary ===")
    print(f"  Fixed: {changed}")
    print(f"  Skipped (already done or no match): {skipped}")


if __name__ == "__main__":
    main()
