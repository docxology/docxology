#!/usr/bin/env python3
"""Generate sitemap.xml from index-priority static pages and work landing pages."""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "sitemap.xml"

sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from sitemap_policy import INDEX_PRIORITY_STATIC, SITE_ORIGIN  # noqa: E402

try:
    from report_paths import report_date_string
except ImportError:  # pragma: no cover - package import path
    from .report_paths import report_date_string


def loc(rel: str) -> str:
    return SITE_ORIGIN + rel


def existing_lastmod() -> str | None:
    if not OUT.exists():
        return None
    match = re.search(r"<lastmod>([^<]+)</lastmod>", OUT.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def url_entry(rel_path: str, changefreq: str, priority: str, lastmod: str) -> str:
    return f"  <url><loc>{html.escape(loc(rel_path))}</loc><lastmod>{lastmod}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>"


def sitemap_locs(lastmod: str | None = None) -> list[str]:
    """Absolute URLs included in sitemap.xml (for IndexNow and tests)."""
    date = lastmod or report_date_string()
    _ = date
    locs = [loc(rel_path) for rel_path, _, _ in INDEX_PRIORITY_STATIC]
    works_dir = REPO_ROOT / "works"
    if works_dir.exists():
        for path in sorted(works_dir.glob("*.html")):
            if path.name == "index.html":
                continue
            locs.append(loc(f"works/{path.name}"))
    return locs


def render(lastmod: str | None = None) -> str:
    date = lastmod or report_date_string()
    entries = [url_entry(*row, date) for row in INDEX_PRIORITY_STATIC]
    works_dir = REPO_ROOT / "works"
    if works_dir.exists():
        for path in sorted(works_dir.glob("*.html")):
            if path.name == "index.html":
                continue
            entries.append(url_entry(f"works/{path.name}", "yearly", "0.45", date))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(entries)
        + "\n</urlset>\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if sitemap.xml is stale")
    args = parser.parse_args()
    content = render(existing_lastmod() if args.check else None)
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Stale generated sitemap.xml")
    else:
        OUT.write_text(content, encoding="utf-8")
    print(("checked" if args.check else "wrote") + " sitemap.xml")


if __name__ == "__main__":
    main()
