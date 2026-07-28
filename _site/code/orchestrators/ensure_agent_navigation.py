#!/usr/bin/env python3
"""Add and validate visible Agent Map links on public entry-page navigation."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from site_nav import ensure_agent_map_link  # noqa: E402


def is_non_indexable(markup: str) -> bool:
    match = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']+)', markup, re.I)
    return bool(match and "noindex" in match.group(1).lower())


def public_root_pages() -> list[Path]:
    pages = []
    for path in sorted(REPO_ROOT.glob("*.html")):
        if path.name == "googlef0f1a1a4a7ba4be8.html":
            continue
        markup = path.read_text(encoding="utf-8", errors="replace")
        if is_non_indexable(markup) or "<nav" not in markup.lower():
            continue
        pages.append(path)
    return pages


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if a public entry page lacks the link")
    args = parser.parse_args()

    stale: list[str] = []
    for path in public_root_pages():
        original = path.read_text(encoding="utf-8")
        updated = ensure_agent_map_link(original)
        if original != updated:
            stale.append(str(path.relative_to(REPO_ROOT)))
            if not args.check:
                path.write_text(updated, encoding="utf-8")
    if stale and args.check:
        raise SystemExit("public navigation is missing Agent Map links: " + ", ".join(stale))
    print(("checked" if args.check else "updated") + " Agent Map navigation for " + ", ".join(stale or ["all public entry pages"]))


if __name__ == "__main__":
    main()
