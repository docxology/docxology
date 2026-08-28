#!/usr/bin/env python3
"""
Deploy SEO + security improvements across all indexable HTML pages:

1. Content-Security-Policy meta tag (if missing)
2. rel="me" social verification links (if missing)

Skips redirect stubs (centrally rendered by generate_redirect_stubs.py) and the
Google verification page.
Idempotent — only adds tags that are missing.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from site_nav import CSP_META_TAG  # noqa: E402
from redirect_stubs import discover_redirect_stubs  # noqa: E402
from generated_outputs import (  # noqa: E402
    UnsafeGeneratedOutputPathError,
    read_generated_output_text,
    safe_generated_output_path,
    write_generated_output_text,
)

# Pages to skip (non-HTML verification surfaces). Redirect stubs are discovered
# from their actual markup rather than maintained as another fixed allowlist.
SKIP_PAGES = {"googlef0f1a1a4a7ba4be8.html"}
EXCLUDED_HTML_PATH_PARTS = frozenset(
    {
        ".git",
        ".venv",
        ".pytest_cache",
        "__pycache__",
        "node_modules",
        "docs",
        "code",
        "reports",
        "netlify-stripe-webhook",
        "_site",
    }
)

# The CSP policy from docs/security/security-posture.md. Imported rather than
# duplicated: the two copies previously carried a "keep this in sync" comment,
# which is a standing invitation for the generated pages and the generator to
# disagree.
CSP_META = CSP_META_TAG
REFERRER_META = '<meta name="referrer" content="strict-origin-when-cross-origin">'

# rel="me" social verification links (same set as index.html head)
REL_ME_LINKS = """    <link rel="me" href="https://scholar.google.com/citations?user=DXjPFtYAAAAJ&hl=en">
    <link rel="me" href="https://orcid.org/0000-0001-6232-9096">
    <link rel="me" href="https://github.com/docxology">
    <link rel="me" href="https://linkedin.com/in/danielarifriedman">
    <link rel="me" href="https://youtube.com/@danielarifriedman">
    <link rel="me" href="https://www.wikidata.org/wiki/Q138781444">
    <link rel="me" href="https://bsky.app/profile/danielarifriedman.com" title="Bluesky">"""


EXTERNAL_FONT_LINK = re.compile(
    r"\s*<link\b[^>]*(?:fonts\.googleapis\.com|fonts\.gstatic\.com)[^>]*>\s*",
    re.I,
)


def is_redirect_stub(html: str) -> bool:
    """Check if the page is a noindex redirect stub."""
    match = re.search(r'<meta\s+name="robots"\s+content="([^"]+)"', html, re.I)
    return bool(match and "noindex" in match.group(1))


def find_insertion_point(html: str) -> int | None:
    """
    Find the insertion point for new <head> tags.
    We insert before the <meta name="revised"> tag if it exists,
    otherwise before the first <meta property="og: tag,
    otherwise before </head>.
    """
    # Try to find the revised meta tag
    match = re.search(r'\s*<meta\s+name="revised"', html)
    if match:
        return match.start()

    # Try to find the first OG meta tag
    match = re.search(r'\s*<meta\s+property="og:', html)
    if match:
        return match.start()

    # Fallback: before </head>
    match = re.search(r'\s*</head>', html)
    if match:
        return match.start()

    return None


def add_csp_if_missing(html: str) -> str:
    """Add or normalize the CSP meta tag."""
    existing = re.compile(r'<meta\s+http-equiv="Content-Security-Policy"\s+content="[^"]*">', re.I)
    if existing.search(html):
        return existing.sub(CSP_META, html, count=1)
    insert_pos = find_insertion_point(html)
    if insert_pos is None:
        return html
    return html[:insert_pos] + "    " + CSP_META + "\n" + html[insert_pos:]


def remove_external_font_links(html: str) -> str:
    """Remove runtime Google Fonts dependencies from public HTML.

    The site intentionally uses the local/system stack now. Removing the
    preconnect, dns-prefetch, and stylesheet tags also prevents a delayed
    media-swap script from attempting a blocked third-party font request.
    """
    return EXTERNAL_FONT_LINK.sub("\n", html)


def add_referrer_policy_if_missing(html: str) -> str:
    """Add the site-wide cross-origin referrer policy when absent."""
    if 'name="referrer"' in html.lower():
        return html
    insert_pos = find_insertion_point(html)
    if insert_pos is None:
        return html
    return html[:insert_pos] + "    " + REFERRER_META + "\n" + html[insert_pos:]


def add_rel_me_if_missing(html: str) -> str:
    """Add rel=me social verification links if not present."""
    if 'rel="me"' in html:
        return html
    insert_pos = find_insertion_point(html)
    if insert_pos is None:
        return html
    return html[:insert_pos] + REL_ME_LINKS + "\n" + html[insert_pos:]


HREFLANG_TAG_RE = re.compile(r"\s*<link\b[^>]*\bhreflang=[^>]*>\s*", re.I)


def strip_hreflang_tags(html: str) -> str:
    """Remove hreflang alternate links from public HTML."""
    return HREFLANG_TAG_RE.sub("\n", html)


def transform_html(html: str, *, is_redirect: bool = False, is_skipped: bool = False) -> tuple[str, list[str], bool]:
    """Return normalized HTML, changes, and whether the page is intentionally skipped.

    Keeping this pure lets ``--check`` prove the same transformation would be
    applied without writing an on-disk byte.
    """
    changes = []

    if is_redirect or is_skipped:
        return html, changes, True

    original = html
    html = remove_external_font_links(html)
    if html != original:
        changes.append("external-fonts-removed")
        original = html

    html = add_csp_if_missing(html)
    if html != original:
        changes.append("csp")
        original = html

    html = add_referrer_policy_if_missing(html)
    if html != original:
        changes.append("referrer-policy")
        original = html

    html = add_rel_me_if_missing(html)
    if html != original:
        changes.append("rel-me")
        original = html

    html = strip_hreflang_tags(html)
    if html != original:
        changes.append("hreflang-stripped")
        original = html

    return html, changes, False


def process_file(
    path: Path,
    *,
    redirect_paths: set[str],
    write: bool = True,
    repo_root: Path = REPO_ROOT,
) -> dict:
    """Process or check one repository-local public HTML file safely.

    This generator updates hand-authored pillar pages as well as generated
    pages, so it deliberately does not assert an ownership marker.  It does
    enforce the same filesystem boundary as generated outputs: an HTML path
    cannot escape the checked-out repository through a symlink, hard link, or
    swapped ancestor while ``--check`` reads it or write mode refreshes it.
    """
    target = safe_generated_output_path(repo_root, path)
    original = read_generated_output_text(repo_root, target)
    if original is None:
        raise UnsafeGeneratedOutputPathError(
            f"SEO/security normalization input is missing: {target}"
        )
    relative = target.relative_to(repo_root.absolute()).as_posix()
    updated, changes, skipped = transform_html(
        original,
        is_redirect=relative in redirect_paths,
        is_skipped=path.name in SKIP_PAGES,
    )
    if changes and write:
        write_generated_output_text(repo_root, target, updated)
    return {"file": relative, "changes": changes, "skipped": skipped}


def is_indexable_html_path(path: Path) -> bool:
    """Exclude tooling/dependency trees from site-wide source normalization."""
    return not bool(EXCLUDED_HTML_PATH_PARTS.intersection(path.parts))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if an indexable page needs a SEO/security normalization")
    args = parser.parse_args()
    html_files = sorted(
        path
        for path in REPO_ROOT.rglob("*.html")
        if is_indexable_html_path(path)
    )
    redirect_paths = discover_redirect_stubs(REPO_ROOT)
    total_changes = 0
    stale: list[str] = []

    for f in html_files:
        result = process_file(f, redirect_paths=redirect_paths, write=not args.check)
        if result.get("skipped"):
            print(f"  SKIP  {result['file']}")
        elif result.get("changes"):
            verb = "STALE" if args.check else "ADD"
            print(f"  {verb}  {result['file']}: {', '.join(result['changes'])}")
            total_changes += len(result["changes"])
            stale.append(result["file"])
        else:
            print(f"  OK    {result['file']}")

    if args.check and stale:
        raise SystemExit("SEO/security normalization is stale: " + ", ".join(stale))
    print(f"\n{total_changes} tag(s) added across {len(html_files)} files")


if __name__ == "__main__":
    main()
