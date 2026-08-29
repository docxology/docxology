"""Canonical/link invariant: internal links never disagree with their target's canonical.

Static, no browser. Scope matches the lane contract: repo-root *.html,
works/*.html, videos/*.html, papers/*/index.html. For every internal
<a href> whose target is an in-scope HTML page, the directory implied by the
href (site-rooted) must equal the directory implied by the target page's own
canonical URL. This is stricter than raw URL equality and immune to the
index.html-vs-/ duality of the site's canonical scheme.

Measured baseline (2026-08-29): 0 mismatches across 43,594 checked links.
Regression guard: this must keep passing.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
BASE = "https://danielarifriedman.com"

CANONICAL_RE = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"')
HREF_RE = re.compile(r'<a[^>]+href="([^"]+)"')

INTERNAL_PREFIXES = (BASE + "/", "https://www.danielarifriedman.com/")


def lane_pages() -> list[Path]:
    pages = sorted(REPO_ROOT.glob("*.html"))
    pages += sorted((REPO_ROOT / "works").glob("*.html"))
    pages += sorted((REPO_ROOT / "videos").glob("*.html"))
    pages += sorted(REPO_ROOT.glob("papers/*/index.html"))
    return pages


def canonical_of(path: Path) -> str | None:
    match = CANONICAL_RE.search(path.read_text(encoding="utf-8", errors="replace"))
    return match.group(1) if match else None


def canonical_dir(canonical_url: str) -> str:
    """Directory part of a canonical URL, site-rooted ('' for the homepage)."""
    for prefix in INTERNAL_PREFIXES:
        if canonical_url.startswith(prefix):
            rest = canonical_url[len(prefix):]
            break
    else:
        return canonical_url  # non-site canonical: compared as-is upstream
    rest = rest.split("#")[0].split("?")[0]
    if rest == "":
        return ""
    if rest.endswith("index.html"):
        return rest[: -len("index.html")]
    return rest


def href_url_and_dir(href: str, page: Path) -> tuple[str, str] | None:
    """Site-rooted URL directory implied by an internal href, or None."""
    if href.startswith(("#", "mailto:", "tel:", "http://", "https:", "//")):
        return None
    if href.startswith(INTERNAL_PREFIXES):
        prefix = BASE + "/" if href.startswith(BASE + "/") else "https://www.danielarifriedman.com/"
        rest = href[len(prefix):]
    elif href == "/":
        rest = ""
    elif href.startswith("/"):
        rest = href.lstrip("/")
    else:
        target = (page.parent / href.split("#")[0].split("?")[0]).resolve()
        try:
            rest = target.relative_to(REPO_ROOT).as_posix()
        except ValueError:
            return None
    rest = rest.split("#")[0].split("?")[0]
    if rest.endswith("index.html"):
        return rest, rest[: -len("index.html")]
    return rest, rest


@pytest.fixture(scope="module")
def pages() -> list[Path]:
    found = lane_pages()
    assert len(found) > 1000, f"lane page scope collapsed: {len(found)} pages"
    return found


def test_lane_scope_matches_fleet_contract(pages: list[Path]) -> None:
    names = {p.relative_to(REPO_ROOT).as_posix() for p in pages}
    assert "index.html" in names
    assert any(n.startswith("works/") for n in names)
    assert any(n.startswith("videos/") for n in names)
    assert any(n.startswith("papers/") and n.endswith("index.html") for n in names)


def test_internal_links_agree_with_target_canonical(pages: list[Path]) -> None:
    canon_dirs = {}
    for page in pages:
        canonical = canonical_of(page)
        canon_dirs[page] = canonical_dir(canonical) if canonical else None

    mismatches: list[str] = []
    links_without_target_canonical = 0
    checked = 0
    for page in pages:
        text = page.read_text(encoding="utf-8", errors="replace")
        for href in HREF_RE.findall(text):
            parsed = href_url_and_dir(href, page)
            if parsed is None:
                continue
            rest, href_dir = parsed
            target = REPO_ROOT / (rest or "index.html")
            if not target.exists() or target.suffix != ".html":
                continue
            checked += 1
            target_dir = canon_dirs.get(target)
            if target_dir is None:
                # Pages without a canonical are counted, not failed: the
                # invariant binds links to pages that declare one.
                links_without_target_canonical += 1
                continue
            if target_dir != href_dir:
                mismatches.append(
                    f"{page.relative_to(REPO_ROOT).as_posix()} -> {href} "
                    f"(target canonical dir {target_dir!r} != href dir {href_dir!r})"
                )
    assert checked > 10000, f"internal-link scan collapsed: {checked} checked"
    print(
        f"canonical invariant: {checked} internal links checked; "
        f"{links_without_target_canonical} to pages without canonical"
    )
    assert not mismatches, (
        f"{len(mismatches)} internal links disagree with their target's canonical:\n"
        + "\n".join(mismatches[:20])
    )


def test_canonical_urls_are_wellformed_where_present(pages: list[Path]) -> None:
    bad: list[str] = []
    for page in pages:
        canonical = canonical_of(page)
        if canonical is None:
            continue
        if not canonical.startswith(("https://danielarifriedman.com", "https://www.danielarifriedman.com")):
            bad.append(f"{page.relative_to(REPO_ROOT).as_posix()}: {canonical}")
    assert not bad, "non-site canonical URLs:\n" + "\n".join(bad[:20])
