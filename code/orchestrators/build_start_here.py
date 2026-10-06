#!/usr/bin/env python3
"""Validate and enrich start-here.html (Start Here curated reading paths).

start-here.html is hand-authored (not generated), so this orchestrator's job
is validation and targeted enrichment, never wholesale re-rendering:

* ``--check`` (default when no flag is passed): fail non-zero unless the page
  exists, contains all four curated reading paths, every local link resolves
  to a real file in the repository, no visible card title exceeds 65
  characters, the hand-authored bibliography/paper-folder counts match
  ``data/current-counts.json``, and the catalogued-drawings count matches
  ``data/artworks.json``.
* ``--enrich``: rewrite the page's shared navigation from the single nav
  manifest in ``code/src/site_nav.py`` (keeping ``aria-current`` on the
  start-here link), stamp the hand-authored counts from
  ``data/current-counts.json`` and ``data/artworks.json`` (the same volatile-fact pattern
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
ARTWORKS = REPO_ROOT / "data" / "artworks.json"


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


# The whole number token is captured (digits with optional ",ddd" thousands
# groups, not preceded by a word character, comma or period) so a stale larger
# number such as "1,943" or "9943" can never satisfy a check for "943".
_ART_COUNT_RE = re.compile(r"(?<![\w,.])(?P<count>\d+(?:,\d{3})*) catalogued pen-and-ink drawings")


# Full-text and extracted-image counts in the paper-folder bullet, anchored like
# _ART_COUNT_RE so a stale number can never satisfy the check by suffix.
_FULL_TEXT_RE = re.compile(r"(?<![\w,.])(?P<count>\d+(?:,\d{3})*) with full-text extraction")
_IMAGES_RE = re.compile(r"(?<![\w,.])(?P<count>\d+(?:,\d{3})*) extracted images")
_EXTRACTION_COUNTS = (
    (_FULL_TEXT_RE, "full_text_papers", "with full-text extraction"),
    (_IMAGES_RE, "extracted_images", "extracted images"),
)


def stamp_extraction_counts(markup: str, counts: dict) -> str:
    """Stamp the full-text and extracted-image counts from data/current-counts.json."""
    for pattern, key, phrase in _EXTRACTION_COUNTS:
        value = counts.get(key)
        if type(value) is int:
            markup = pattern.sub(f"{value:,} {phrase}", markup)
    return markup


def check_extraction_counts(markup: str, counts: dict) -> list[str]:
    """Every full-text/extracted-image count on the page equals data/current-counts.json."""
    errors = []
    for pattern, key, phrase in _EXTRACTION_COUNTS:
        value = counts.get(key)
        if type(value) is not int:
            errors.append(f"current-counts.json missing integer {key}")
            continue
        found = [match.group("count") for match in pattern.finditer(markup)]
        if not found:
            errors.append(f"start-here.html has no '{phrase}' count")
        elif any(number != f"{value:,}" for number in found):
            errors.append(f"stale '{phrase}' count in start-here.html (current-counts says {value:,})")
    return errors


def load_artwork_count(path: Path | None = None) -> int:
    """Number of catalogued artworks in the Flickr gallery export (``data/artworks.json``)."""
    with open(path or ARTWORKS, encoding="utf-8") as f:
        payload = json.load(f)
    count = payload.get("count") if isinstance(payload, dict) else None
    if type(count) is not int or count < 0:
        raise ValueError(f"artworks export has no non-negative integer count: {count!r}")
    return count


def stamp_art_count(markup: str, art_count: int) -> str:
    """Stamp the 'N catalogued pen-and-ink drawings' count (thousands separator from 1,000)."""
    return _ART_COUNT_RE.sub(f"{art_count:,} catalogued pen-and-ink drawings", markup)


def check_art_count(markup: str, art_count: int) -> list[str]:
    """The catalogued-drawings count must be present and every occurrence must equal the export count.

    The phrase is matched with the same anchored regex ``stamp_art_count``
    rewrites and each captured number is compared exactly with the formatted
    count, so a page that lost the phrase, or carries any occurrence with a
    different number (including a longer one that merely ends in the expected
    digits), is an error.
    """
    expected = f"{art_count:,}"
    found = [match.group("count") for match in _ART_COUNT_RE.finditer(markup)]
    if not found:
        return [
            "missing 'N catalogued pen-and-ink drawings' count in start-here.html "
            f"(artworks.json says {art_count})"
        ]
    if any(number != expected for number in found):
        return [f"stale art count in start-here.html (artworks.json says {art_count})"]
    return []


def stamp_counts(markup: str) -> str:
    """Stamp the hand-authored bibliography/paper-folder/art counts (sync_site_facts-style)."""
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
    markup = stamp_extraction_counts(markup, counts)
    return stamp_art_count(markup, load_artwork_count())


def check_counts(markup: str) -> list[str]:
    """The hand-authored counts must match data/current-counts.json and data/artworks.json."""
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
    errors.extend(check_extraction_counts(markup, counts))
    try:
        errors.extend(check_art_count(markup, load_artwork_count()))
    except (OSError, KeyError, ValueError) as exc:
        errors.append(f"cannot read {ARTWORKS.name}: {exc}")
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


def sync_counts() -> bool:
    """Stamp only the generated counts; idempotent and date-free.

    This is the regeneration-chain mode: a bibliography add or retirement
    changes ``data/current-counts.json`` (and an artwork resync changes
    ``data/artworks.json``), and the hand-authored prose must
    follow without the clock-dependent ``dateModified`` stamp that ``--enrich``
    applies (that would break the chain's byte-stable rerun guarantee).
    Returns whether the page changed.
    """
    markup = PAGE.read_text(encoding="utf-8")
    stamped = stamp_counts(markup)
    if stamped == markup:
        return False
    PAGE.write_text(stamped, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate the page (default)")
    parser.add_argument("--enrich", action="store_true", help="re-render nav + stamp counts + stamp dateModified")
    parser.add_argument(
        "--sync-counts",
        action="store_true",
        help="stamp only the generated work/paper-folder/art counts (idempotent; used by regenerate_all.py)",
    )
    args = parser.parse_args()

    if args.sync_counts:
        changed = sync_counts()
        print(f"{PAGE.name}: counts {'stamped from' if changed else 'already match'} {CURRENT_COUNTS.name} and {ARTWORKS.name}")
        errors = check()
        if errors:
            print("\n".join(errors), file=sys.stderr)
            raise SystemExit(1)
        return

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
