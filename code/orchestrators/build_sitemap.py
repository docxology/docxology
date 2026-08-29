#!/usr/bin/env python3
"""Generate sitemap.xml from index-priority static pages and work landing pages."""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from functools import lru_cache
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


def existing_lastmod(output: Path = OUT) -> str | None:
    if not output.exists():
        return None
    matches = re.findall(r"<lastmod>([^<]+)</lastmod>", output.read_text(encoding="utf-8"))
    return max(matches) if matches else None


def _fs_path(rel: str) -> str:
    """Map a sitemap rel path to the file whose git history dates it."""
    if rel == "" or rel.endswith("/"):
        return rel + "index.html"
    return rel


@lru_cache(maxsize=None)
def git_lastmod(rel: str, repo_root: Path = REPO_ROOT) -> str | None:
    """Last commit date (YYYY-MM-DD) for a path, or None if git is unavailable.

    Gives each URL an accurate per-page <lastmod> instead of one shared date.
    Falls back to None on shallow checkouts / exported trees so the caller can
    use the global build date — preserving prior behaviour in those cases.
    """
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", _fs_path(rel)],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    date = result.stdout.strip()
    return date or None


def url_entry(
    rel_path: str,
    changefreq: str,
    priority: str,
    lastmod: str,
    *,
    repo_root: Path = REPO_ROOT,
) -> str:
    entry_lastmod = git_lastmod(rel_path, repo_root) or lastmod
    return f"  <url><loc>{html.escape(loc(rel_path))}</loc><lastmod>{entry_lastmod}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>"


def generated_url_entry(rel_path: str, changefreq: str, priority: str, lastmod: str) -> str:
    return f"  <url><loc>{html.escape(loc(rel_path))}</loc><lastmod>{lastmod}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>"


def sitemap_locs(lastmod: str | None = None, *, repo_root: Path = REPO_ROOT) -> list[str]:
    """Absolute URLs included in sitemap.xml (for IndexNow and tests)."""
    date = lastmod or report_date_string()
    _ = date
    locs = [loc(rel_path) for rel_path, _, _ in INDEX_PRIORITY_STATIC]
    works_dir = repo_root / "works"
    if works_dir.exists():
        for path in sorted(works_dir.glob("*.html")):
            if path.name == "index.html":
                continue
            locs.append(loc(f"works/{path.name}"))
    videos_dir = repo_root / "videos"
    if videos_dir.exists():
        for path in sorted(videos_dir.glob("*.html")):
            if path.name == "index.html":
                continue
            locs.append(loc(f"videos/{path.name}"))
    return locs


def render(lastmod: str | None = None, *, repo_root: Path = REPO_ROOT) -> str:
    date = lastmod or report_date_string()
    entries = [url_entry(*row, date, repo_root=repo_root) for row in INDEX_PRIORITY_STATIC]
    works_dir = repo_root / "works"
    if works_dir.exists():
        for path in sorted(works_dir.glob("*.html")):
            if path.name == "index.html":
                continue
            entries.append(
                url_entry(
                    f"works/{path.name}",
                    "yearly",
                    "0.45",
                    date,
                    repo_root=repo_root,
                )
            )
    # Paper folder index.html pages are already covered by paper_pages builder;
    # full_text.md is NOT sitemapped (SEO invariant forbids /papers/ URLs in sitemap).
    videos_dir = repo_root / "videos"
    if videos_dir.exists():
        for path in sorted(videos_dir.glob("*.html")):
            if path.name == "index.html":
                continue
            entries.append(url_entry(f"videos/{path.name}", "yearly", "0.35", date, repo_root=repo_root))
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
        if not OUT.exists():
            raise SystemExit("Stale generated sitemap.xml: missing")

        import re as _re

        def _norm(s: str) -> str:
            """Blank out <lastmod> values: they are anchored to HEAD at
            generation time, so a lastmod-only difference is not staleness
            (mirrors build-stamp reuse semantics)."""
            return _re.sub(r"<lastmod>[^<]+</lastmod>", "<lastmod/>", s)

        on_disk = OUT.read_text(encoding="utf-8")
        if _norm(on_disk) == _norm(content):
            print("checked sitemap.xml (lastmod-only drift tolerated)")
            return
        if on_disk != content:
            # One bounded retry: under heavy machine load an individual
            # git_lastmod probe can hit its timeout and fall back to the build
            # date, making a single render non-deterministic. Re-render once
            # before declaring staleness so load-induced flakes don't fail the
            # gate (a genuinely stale sitemap still fails both renders).
            content = render(existing_lastmod())
            if _norm(OUT.read_text(encoding="utf-8")) != _norm(content):
                raise SystemExit("Stale generated sitemap.xml")
    else:
        OUT.write_text(content, encoding="utf-8")
    print(("checked" if args.check else "wrote") + " sitemap.xml")


if __name__ == "__main__":
    main()
