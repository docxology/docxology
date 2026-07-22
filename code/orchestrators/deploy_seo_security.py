#!/usr/bin/env python3
"""
Deploy SEO + security improvements across all indexable HTML pages:

1. Content-Security-Policy meta tag (if missing)
2. rel="me" social verification links (if missing)
3. hreflang alternate links (if missing)

Skips redirect stubs (noindex pages) and the Google verification page.
Idempotent — only adds tags that are missing.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Pages to skip (redirect stubs or non-HTML)
SKIP_PAGES = {
    "googlef0f1a1a4a7ba4be8.html",
    "about.html",
    "meditations.html",
    "nft.html",
    "research.html",
}

# The CSP policy from docs/security/security-posture.md. Keep this in sync
# with code/src/site_nav.py; GitHub Pages provides no custom response headers.
CSP_META = (
    '<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; '
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "font-src 'self'; "
    'img-src \'self\' data: https:; '
    "connect-src 'self'; "
    "frame-src https://www.youtube-nocookie.com; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    'form-action \'self\';">'
)
REFERRER_META = '<meta name="referrer" content="strict-origin-when-cross-origin">'

# rel="me" social verification links (same set as index.html head)
REL_ME_LINKS = """    <link rel="me" href="https://scholar.google.com/citations?user=DXjPFtYAAAAJ&hl=en">
    <link rel="me" href="https://orcid.org/0000-0001-6232-9096">
    <link rel="me" href="https://github.com/docxology">
    <link rel="me" href="https://linkedin.com/in/danielarifriedman">
    <link rel="me" href="https://youtube.com/@danielarifriedman">
    <link rel="me" href="https://www.wikidata.org/wiki/Q138781444">
    <link rel="me" href="https://bsky.app/profile/danielarifriedman.com" title="Bluesky">"""

# hreflang alternate links
HREFLANG_LINKS = """    <link rel="alternate" href="https://danielarifriedman.com/" hreflang="en" />
    <link rel="alternate" href="https://danielarifriedman.com/" hreflang="x-default" />"""
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


def add_hreflang_if_missing(html: str) -> str:
    """Add hreflang alternate links if not present."""
    if "hreflang" in html:
        return html
    insert_pos = find_insertion_point(html)
    if insert_pos is None:
        return html
    return html[:insert_pos] + HREFLANG_LINKS + "\n" + html[insert_pos:]


def process_file(path: Path) -> dict:
    """Process a single HTML file. Returns a dict with what was changed."""
    html = path.read_text(encoding="utf-8")
    changes = []

    if is_redirect_stub(html) or path.name in SKIP_PAGES:
        return {"file": path.name, "skipped": True}

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

    html = add_hreflang_if_missing(html)
    if html != original:
        changes.append("hreflang")
        original = html

    if changes:
        path.write_text(html, encoding="utf-8")

    return {"file": path.name, "changes": changes}


def main() -> None:
    html_files = sorted(
        path
        for path in REPO_ROOT.rglob("*.html")
        if not ({".git", "node_modules", "docs", "code", "reports", "netlify-stripe-webhook", "_site"} & set(path.parts))
    )
    total_changes = 0

    for f in html_files:
        result = process_file(f)
        if result.get("skipped"):
            print(f"  SKIP  {result['file']}")
        elif result.get("changes"):
            print(f"  ADD   {result['file']}: {', '.join(result['changes'])}")
            total_changes += len(result["changes"])
        else:
            print(f"  OK    {result['file']}")

    print(f"\n{total_changes} tag(s) added across {len(html_files)} files")


if __name__ == "__main__":
    main()
