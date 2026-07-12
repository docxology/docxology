"""Shared site navigation HTML for generated pages."""

from __future__ import annotations

import html
import json

SITE_ORIGIN = "https://danielarifriedman.com/"

# Content-Security-Policy meta tag (deployed on all indexable pages).
# script-src 'self' blocks inline event handlers and inline <script> blocks.
CSP_META_TAG = (
    '<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; '
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    'img-src \'self\' data: https:; '
    "connect-src 'self'; "
    "frame-ancestors 'none'; "
    "base-uri 'self'; "
    'form-action \'self\';">'
)

# rel="me" social verification links (same set as index.html head).
REL_ME_LINKS = (
    '    <link rel="me" href="https://scholar.google.com/citations?user=DXjPFtYAAAAJ&hl=en">\n'
    '    <link rel="me" href="https://orcid.org/0000-0001-6232-9096">\n'
    '    <link rel="me" href="https://github.com/docxology">\n'
    '    <link rel="me" href="https://linkedin.com/in/danielarifriedman">\n'
    '    <link rel="me" href="https://youtube.com/@danielarifriedman">\n'
    '    <link rel="me" href="https://www.wikidata.org/wiki/Q138781444">\n'
    '    <link rel="me" href="https://bsky.app/profile/danielarifriedman.com" title="Bluesky">'
)

# hreflang alternate links.
HREFLANG_LINKS = (
    '    <link rel="alternate" href="https://danielarifriedman.com/" hreflang="en" />\n'
    '    <link rel="alternate" href="https://danielarifriedman.com/" hreflang="x-default" />'
)

# Combined head extras block — CSP + rel-me + hreflang + resource hints.
# Inject this before the closing </head> or before the first <meta property="og:">
# in generated HTML templates.
HEAD_EXTRAS = (
    f"    {CSP_META_TAG}\n"
    f"{REL_ME_LINKS}\n"
    f"{HREFLANG_LINKS}\n"
    '    <link rel="dns-prefetch" href="https://fonts.googleapis.com">\n'
    '    <link rel="dns-prefetch" href="https://fonts.gstatic.com">'
)

# Shared mobile-menu Escape-to-close handler — moved to external JS file
# (js/menu-esc.js) so it complies with the CSP (script-src 'self').
# Previously this was an inline <script> block, which CSP blocks.
MENU_ESC_SCRIPT = '<script src="/js/menu-esc.js?v=20260712" defer></script>'

# Interactive layer script tags (TTS + interactive features) — appended before MENU_ESC_SCRIPT on generated pages.
INTERACTIVE_SCRIPTS = '<script src="/js/tts-controls.js?v=20260712" defer></script>\n<script src="/js/interactive.js?v=20260712" defer></script>'

# Work pages that are duplicates of another catalogued work (same paper, different
# Zenodo deposit/version) point their rel=canonical at the primary entry so search
# engines consolidate ranking signals instead of splitting them across duplicates.
#   key (duplicate citation_key) -> value (canonical/primary citation_key)
#   Currently empty — the CEREBRUM "v1.4" duplicate this once consolidated was
#   removed outright. Add entries here if a future deposit duplicates a work.
WORK_CANONICAL_OVERRIDES: dict[str, str] = {}


def canonical_work_key(citation_key: str) -> str:
    """Return the canonical citation_key for a work (itself unless it is a known duplicate)."""
    return WORK_CANONICAL_OVERRIDES.get(citation_key, citation_key)


def clip_description(text: str, limit: int = 155) -> str:
    """Clip a meta description to <= limit chars on a word boundary.

    Avoids cutting mid-word; appends an ellipsis when truncation occurs.
    Used for SERP snippets, og:description, and twitter:description.
    """
    text = " ".join(str(text or "").split()).strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0].rstrip(" ,;:.–—-")
    if not cut:  # single very long token; hard cut as last resort
        cut = text[: limit - 1].rstrip()
    return cut + "…"


def social_meta_tags(
    og_title: str,
    description: str,
    og_image_url: str,
    *,
    image_alt: str,
    indent: str = "    ",
) -> str:
    """og:image:alt + Twitter summary_large_image card tags.

    Returns a newline-joined block (no trailing newline) mirroring the page's
    Open Graph values so X/Slack/Discord render large-image previews. og_title
    should match the page's og:title; description should already be clipped.
    """
    esc = lambda v: html.escape(str(v), quote=True)  # noqa: E731
    lines = [
        f'{indent}<meta property="og:image:alt" content="{esc(image_alt)}">',
        f'{indent}<meta name="twitter:card" content="summary_large_image">',
        f'{indent}<meta name="twitter:title" content="{esc(og_title)}">',
        f'{indent}<meta name="twitter:description" content="{esc(description)}">',
        f'{indent}<meta name="twitter:image" content="{esc(og_image_url)}">',
        f'{indent}<meta name="twitter:image:alt" content="{esc(image_alt)}">',
    ]
    return "\n".join(lines)


# Inline CSS for the breadcrumb component. Kept inline (rather than in style.css)
# so pages render correctly without depending on a bumped style.css cache version.
BREADCRUMB_CSS = (
    ".breadcrumb{max-width:1100px;margin:1.4rem auto 0;padding:0 2rem}"
    ".breadcrumb ol{list-style:none;display:flex;flex-wrap:wrap;gap:.4rem;padding:0;margin:0;font-size:.8rem;color:var(--text-muted)}"
    ".breadcrumb li+li::before{content:'\\203A';margin-right:.4rem;color:var(--text-muted)}"
    ".breadcrumb a{color:var(--silver-bright);text-decoration:none}"
    ".breadcrumb a:hover{text-decoration:underline}"
    ".breadcrumb [aria-current=page]{color:var(--text-secondary)}"
)


def breadcrumb_list_jsonld(trail: list[tuple[str, str]]) -> dict:
    """Schema.org BreadcrumbList from (label, root-relative path) pairs ('' = home)."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": label, "item": SITE_ORIGIN + rel}
            for i, (label, rel) in enumerate(trail)
        ],
    }


def breadcrumb_jsonld_script(trail: list[tuple[str, str]]) -> str:
    payload = json.dumps(breadcrumb_list_jsonld(trail), indent=4, ensure_ascii=False)
    return f'    <script type="application/ld+json">\n{payload}\n    </script>'


def render_breadcrumb(trail: list[tuple[str, str]], *, depth: int = 0) -> str:
    """Accessible visible breadcrumb nav. Last item is the current page (no link)."""
    prefix = "../" * depth
    out = []
    for i, (label, rel) in enumerate(trail):
        if i == len(trail) - 1:
            out.append(f'<li aria-current="page">{html.escape(label)}</li>')
        else:
            href = f"{prefix}{rel}" if rel else f"{prefix}index.html"
            out.append(f'<li><a href="{html.escape(href, quote=True)}">{html.escape(label)}</a></li>')
    return (
        '    <nav class="breadcrumb" aria-label="Breadcrumb">\n'
        f'        <ol>{"".join(out)}</ol>\n'
        '    </nav>'
    )


def render_nav(*, active: str = "", depth: int = 0) -> str:
    """Return nav block. depth=0 for root pages, depth=1+ for nested pages."""
    prefix = "../" * depth
    home = f"{prefix}index.html"
    links = [
        ("about", f"{prefix}index.html#about", "About"),
        ("publications", f"{prefix}publications.html", "Publications"),
        ("works", f"{prefix}works/", "Works"),
        ("domains", f"{prefix}domains.html", "Domains"),
        ("software", f"{prefix}software.html", "Software"),
        ("videos", f"{prefix}videos.html", "Videos"),
        ("search", f"{prefix}search.html", "Search"),
        ("catalog", f"{prefix}catalog.html", "Data Catalog"),
        ("cite", f"{prefix}cite-verify.html", "Cite"),
        ("discovery", f"{prefix}discovery.html", "Discovery"),
    ]
    parts = [
        f'    <nav role="navigation" aria-label="Main navigation">',
        f'        <a href="{home}" class="nav-logo">Daniel Ari Friedman</a>',
        '        <button class="menu-btn" aria-label="Toggle menu" aria-expanded="false">☰</button>',
        '        <div class="nav-links">',
    ]
    for key, href, label in links:
        cls = ' class="active"' if key == active else ""
        parts.append(f'            <a href="{html.escape(href, quote=True)}"{cls}>{html.escape(label)}</a>')
    parts.extend(["        </div>", "    </nav>"])
    return "\n".join(parts)


def render_nav_domain(*, active: str = "domains", depth: int = 0) -> str:
    """Nav for domain-*.html and domains.html (matches software/search/discovery cluster)."""
    prefix = "../" * depth
    home = f"{prefix}index.html"
    links = [
        ("about", f"{home}#about", "About"),
        ("research", f"{home}#research", "Research"),
        ("publications", f"{prefix}publications.html", "Publications"),
        ("domains", f"{prefix}domains.html", "Domains"),
        ("software", f"{prefix}software.html", "Software"),
        ("search", f"{prefix}search.html", "Search"),
        ("catalog", f"{prefix}catalog.html", "Data Catalog"),
        ("cite", f"{prefix}cite-verify.html", "Cite"),
        ("discovery", f"{prefix}discovery.html", "Discovery"),
        ("media", f"{prefix}media.html", "Media"),
    ]
    parts = [
        '    <nav role="navigation" aria-label="Main navigation">',
        f'        <a href="{home}" class="nav-logo">Daniel Ari Friedman</a>',
        '        <button class="menu-btn" aria-label="Toggle menu" aria-expanded="false">☰</button>',
        '        <div class="nav-links">',
    ]
    for key, href, label in links:
        cls = ' class="active"' if key == active else ""
        parts.append(f'            <a href="{html.escape(href, quote=True)}"{cls}>{html.escape(label)}</a>')
    parts.extend(["        </div>", "    </nav>"])
    return "\n".join(parts)


def render_nav_compact(*, depth: int = 1) -> str:
    """Compact nav for work detail pages (legacy subset + discovery)."""
    prefix = "../" * depth
    return (
        f'<nav role="navigation" aria-label="Main navigation">'
        f'<a href="{prefix}index.html" class="nav-logo">Daniel Ari Friedman</a>'
        f'<div class="nav-links">'
        f'<a href="{prefix}publications.html">Publications</a>'
        f'<a href="{prefix}domains.html">Domains</a>'
        f'<a href="{prefix}search.html">Search</a>'
        f'<a href="{prefix}catalog.html">Data Catalog</a>'
        f'<a href="{prefix}cite-verify.html">Cite</a>'
        f'<a href="{prefix}discovery.html">Discovery</a>'
        f"</div></nav>"
    )
