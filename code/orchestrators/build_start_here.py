#!/usr/bin/env python3
"""Validate and enrich start-here.html (Start Here curated reading paths).

start-here.html is hand-authored (not generated), so this orchestrator's job
is validation and targeted enrichment, never wholesale re-rendering:

* ``--check`` (default when no flag is passed): fail non-zero unless the page
  exists, contains all four curated reading paths, every local link resolves
  to a real file in the repository, no visible card title exceeds 65
  characters, and the hand-authored bibliography/paper-folder counts match
  ``data/current-counts.json``.
* ``--enrich``: rewrite the page's shared navigation from the single nav
  manifest in ``code/src/site_nav.py`` (keeping ``aria-current`` on the
  start-here link), stamp the hand-authored counts from
  ``data/current-counts.json`` (the same volatile-fact pattern
  ``sync_site_facts.py`` applies elsewhere), and refresh ``dateModified`` in
  the WebPage JSON-LD to today, so the hand-authored shell cannot drift from
  the manifest or the count report.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)
from docxology_tools import site_nav  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
PAGE = REPO_ROOT / "start-here.html"

PAGE_KEY = "start-here.html"
CURRENT_COUNTS = REPO_ROOT / "data" / "current-counts.json"


# Card section ids that must all be present (acceptance criterion 1).
REQUIRED_PATH_IDS: tuple[str, ...] = (
    "new-to-active-inference",
    "ant-researcher-entomology",
    "cognitive-security",
    "hiring-or-collaborating",
)

MAX_TITLE_CHARS = 65

_LINK_RE = re.compile(r'href="([^"#]+)"')
_H2_RE = re.compile(r"<h2>(.*?)</h2>", re.S)
_TAG_RE = re.compile(r"<[^>]+>")


def _is_local(href: str) -> bool:
    return not (href.startswith(("http://", "https://", "//", "mailto:", "/")))


_ASSET_PREFIXES = ("style.css", "js/", "favicon", "manifest.json", "feed.xml",
                   "opensearch.xml", "search-index.json")


def _link_hrefs(markup: str) -> list[str]:
    return [m for m in _LINK_RE.findall(markup)]


def check_links(markup: str) -> list[str]:
    """Return hrefs (anchors included) that do not resolve to real files."""
    errors: list[str] = []
    for href in _link_hrefs(markup):
        if not _is_local(href):
            continue
        target = href.split("#", 1)[0].split("?", 1)[0]
        if not target:
            continue  # pure in-page anchor
        if target.startswith(_ASSET_PREFIXES) and (REPO_ROOT / target.split("?")[0]).exists():
            continue  # static asset (may carry a cache-busting query string)
        if not (REPO_ROOT / target.split("?")[0]).exists():
            errors.append(f"broken link: {href}")
    return errors


def check_titles(markup: str) -> list[str]:
    """Card h2 titles must stay within MAX_TITLE_CHARS (no wrapping blowouts)."""
    errors: list[str] = []
    for raw in _H2_RE.findall(markup):
        title = _TAG_RE.sub("", raw).strip()
        if len(title) > MAX_TITLE_CHARS:
            errors.append(f"title over {MAX_TITLE_CHARS} chars: {title!r} ({len(title)})")
    return errors


def check_paths(markup: str) -> list[str]:
    missing = [pid for pid in REQUIRED_PATH_IDS if f'id="{pid}"' not in markup]
    return [f"missing reading path: {pid}" for pid in missing]


def load_public_counts() -> dict:
    """Load the generated count report the hand-authored prose must track."""
    with open(CURRENT_COUNTS, encoding="utf-8") as f:
        return json.load(f)["counts"]


def stamp_counts(markup: str) -> str:
    """Stamp the hand-authored bibliography/paper-folder counts (sync_site_facts-style)."""
    counts = load_public_counts()
    markup = re.sub(
        r"a unified bibliography of \d+ works",
        f"a unified bibliography of {counts['bibliography_works']} works",
        markup,
    )
    markup = re.sub(
        r"\b\d+ folders under <code>papers/</code>",
        f"{counts['paper_folder_docs']} folders under <code>papers/</code>",
        markup,
    )
    return markup


def check_counts(markup: str) -> list[str]:
    """The two hand-authored counts must match data/current-counts.json."""
    try:
        counts = load_public_counts()
    except (OSError, KeyError, ValueError) as exc:
        return [f"cannot read {CURRENT_COUNTS.name}: {exc}"]
    works = counts.get("bibliography_works")
    folders = counts.get("paper_folder_docs")
    if not isinstance(works, int) or not isinstance(folders, int):
        return ["current-counts.json missing integer bibliography_works/paper_folder_docs"]
    errors = []
    if not re.search(rf"a unified bibliography of {works} works", markup):
        errors.append(f"stale works count in start-here.html (current-counts says {works})")
    if not re.search(rf"\b{folders} folders under <code>papers/</code>", markup):
        errors.append(f"stale paper-folder count in start-here.html (current-counts says {folders})")
    return errors


def check() -> list[str]:
    if not PAGE.exists():
        return [f"missing page: {PAGE.name}"]
    markup = PAGE.read_text(encoding="utf-8")
    return check_counts(markup) + check_paths(markup) + check_links(markup) + check_titles(markup)


def enrich() -> None:
    """Rewrite the shared nav from the manifest, stamp counts, and stamp dateModified today."""
    markup = PAGE.read_text(encoding="utf-8")

    fresh_nav = site_nav.render_nav(active="start-here", depth=0)
    nav_block = re.compile(r'<nav aria-label="Main navigation".*?</nav>', re.S)
    if not nav_block.search(markup):
        raise SystemExit("start-here.html: main nav block not found")
    markup = nav_block.sub(lambda _: fresh_nav, markup, count=1)
    markup = stamp_counts(markup)

    today = dt.date.today().isoformat()
    markup = re.sub(
        r'("dateModified"\s*:\s*")[0-9-]+(")',
        lambda m: f"{m.group(1)}{today}{m.group(2)}",
        markup,
    )

    PAGE.write_text(markup, encoding="utf-8")
    print(f"enriched {PAGE.name}: nav re-rendered from manifest, dateModified={today}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate the page (default)")
    parser.add_argument("--enrich", action="store_true", help="re-render nav + stamp counts + stamp dateModified")
    args = parser.parse_args()

    if args.enrich:
        enrich()
        errors = check()
        if errors:
            print("\n".join(errors), file=sys.stderr)
            raise SystemExit(1)
        print("post-enrich check: clean")
        return

    errors = check()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"start-here.html: {len(REQUIRED_PATH_IDS)} paths, all links resolve, titles <= {MAX_TITLE_CHARS} chars")


if __name__ == "__main__":
    main()
