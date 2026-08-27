"""Shared site navigation HTML for generated pages."""

from __future__ import annotations

import html
import json
import re

SITE_ORIGIN = "https://danielarifriedman.com/"

# Content-Security-Policy meta tag (deployed on all public pages). GitHub Pages
# does not allow custom response headers, so this meta policy is the strongest
# site-local enforcement layer.
# Single definition of the site CSP; deploy_seo_security.py imports this one.
#
# Header-only directives are deliberately absent. Per the CSP spec a policy
# delivered through <meta> MUST ignore `frame-ancestors`, `report-uri` and
# `sandbox`, and Chromium logs a console error for each page that ships one.
# Carrying `frame-ancestors 'none'` here bought no clickjacking protection
# whatsoever and put an error on every one of ~1540 pages, which is real cost:
# it trained the browser QA gate to filter console errors, and any genuine
# error is easier to miss in noise. Framing protection needs an HTTP response
# header, which GitHub Pages cannot serve — see docs/security/security-posture.md.
CSP_META_TAG = (
    '<meta http-equiv="Content-Security-Policy" content="default-src \'self\'; '
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline'; "
    "font-src 'self'; "
    'img-src \'self\' data: https:; '
    "connect-src 'self'; "
    "frame-src https://www.youtube-nocookie.com; "
    "base-uri 'self'; "
    'form-action \'self\';">'
)

# Directives a <meta>-delivered CSP must never carry, because the spec requires
# user agents to ignore them there. Enforced by code/tests/test_seo_invariants.py.
META_INVALID_CSP_DIRECTIVES = ("frame-ancestors", "report-uri", "sandbox")

REFERRER_POLICY_META = '<meta name="referrer" content="strict-origin-when-cross-origin">'

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

# Combined head extras block — CSP + rel-me + resource hints.
# Inject this before the closing </head> or before the first <meta property="og:">
# in generated HTML templates.
HEAD_EXTRAS = (
    f"    {CSP_META_TAG}\n"
    f"    {REFERRER_POLICY_META}\n"
    f"{REL_ME_LINKS}\n"
    '    <link rel="alternate" type="application/json" href="/data/agent-index.json" title="Agent route manifest">'
)

# Shared mobile-menu Escape-to-close handler — moved to external JS file
# (js/menu-esc.js) so it complies with the CSP (script-src 'self').
# Previously this was an inline <script> block, which CSP blocks.
MENU_ESC_SCRIPT = '<script src="/js/menu-esc.js?v=20260813" defer></script>'

# search-utils.js defines global esc() and must load before interactive.js.
INTERACTIVE_SCRIPTS = (
    '<script src="/js/search-utils.js?v=20260813"></script>\n'
    '<script src="/js/tts-controls.js?v=20260813" defer></script>\n'
    '<script src="/js/interactive.js?v=20260813" defer></script>'
)

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


# Domain emoji -> domain hub page slug. Mirrors DomainConfig.domains/slug in
# build_domain_pages.py; kept here so per-work and per-paper pages can link back
# to their domain hub (bidirectional discovery) without importing the orchestrator.
DOMAIN_EMOJI_TO_SLUG = {
    "🐜": "entomology",
    "🧠": "active-inference",
    "🛡️": "cognitive-security",
    "🛡": "cognitive-security",
    "🎨": "art-synergetics",
    "💻": "computational",
    "🧬": "biomedicine",
    "🌍": "aii-ecosystem",
    "🎥": "presentations-media",
}


def domain_page_href(emoji: str, *, depth: int = 0) -> str:
    """Return the domain hub page href for a work's domain emoji, or '' if unknown.

    depth is the number of directory levels below site root (works/ and papers/*
    pages use depth=1 so the link resolves to ../domain-<slug>.html).
    """
    slug = DOMAIN_EMOJI_TO_SLUG.get((emoji or "").strip())
    if not slug:
        return ""
    return f"{'../' * depth}domain-{slug}.html"


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


def render_pillar_head(
    *,
    title: str,
    description: str,
    canonical_path: str,
    og_image: str,
    style: str,
    jsonld: dict,
) -> str:
    """Render the shared security/SEO head for a root-level pillar page.

    Pillar pages are long-form, server-rendered sources and cannot delegate
    their essential metadata to client JavaScript.  This renderer keeps their
    CSP, referrer policy, rel=me links, canonical, social metadata, and JSON-LD
    in the same shared layer as other generated public pages.
    """
    canonical = f"{SITE_ORIGIN}{canonical_path.lstrip('/')}"
    escaped_title = html.escape(title, quote=True)
    escaped_description = html.escape(description, quote=True)
    image_url = f"{SITE_ORIGIN}{og_image.lstrip('/')}"
    jsonld_text = json.dumps(jsonld, indent=4, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escaped_title}</title>
    <meta name="description" content="{escaped_description}">
    <meta name="author" content="Daniel Ari Friedman">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{canonical}">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="text/plain" href="/llms.txt" title="LLMs.txt">
    <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Daniel Ari Friedman updates">
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Daniel Ari Friedman">
{HEAD_EXTRAS}
    <meta property="og:type" content="article">
    <meta property="og:title" content="{escaped_title}">
    <meta property="og:description" content="{escaped_description}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:image" content="{image_url}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
{social_meta_tags(title, description, image_url, image_alt=title)}
    <link rel="stylesheet" href="style.css?v=newspaper-glitch-20260530c">
    <meta name="theme-color" content="#0c0c0e">
    <style>
{BREADCRUMB_CSS}
{style.rstrip()}
    </style>
    <script type="application/ld+json">
{jsonld_text}
    </script>
</head>
"""


_VISIBLE_AGENT_LINK = re.compile(
    r'<a\b[^>]*href=["\'][^"\']*data/agent-index\.json[^"\']*["\'][^>]*>',
    re.I,
)


def ensure_agent_map_link(markup: str, *, href: str = "data/agent-index.json") -> str:
    """Ensure a public page's visible navigation links to the agent manifest.

    Generated work/domain pages already use :func:`render_nav`; this helper covers
    hand-authored collection pages whose bespoke navigation otherwise made the
    manifest discoverable only through a head ``alternate`` link. It is deliberately
    idempotent and only touches the first ``nav-links`` or ``nav-right`` container.
    """
    anchor = f'<a href="{html.escape(href, quote=True)}">Agent Map</a>'
    if 'role="menubar"' in markup or "role='menubar'" in markup:
        anchor = f'<a href="{html.escape(href, quote=True)}" role="menuitem">Agent Map</a>'

    container = re.compile(
        r'(?P<open><div\b[^>]*class=["\'][^"\']*\b(?:nav-links|nav-right)\b[^"\']*["\'][^>]*>)'
        r'(?P<body>.*?)'
        r'(?P<close></div>)',
        re.I | re.S,
    )
    match = container.search(markup)
    if not match:
        return markup

    body = match.group("body")
    open_line_indent = markup[: match.start("open")].rsplit("\n", 1)[-1]
    if _VISIBLE_AGENT_LINK.search(body):
        # A compact bespoke nav may already be canonical.  Returning it as-is
        # avoids introducing a newline on the second application, preserving
        # the helper's idempotence for both compact and multiline markup.
        if "\n" not in body:
            return markup
        # Normalize links that were inserted by an older version of this helper
        # so generated navigation remains readable and diff-stable.
        normalized = re.sub(
            r"\n[ \t]*\n([ \t]*<a\b[^>]*data/agent-index\.json[^>]*>Agent Map</a>)",
            r"\n\1",
            body,
            flags=re.I,
        ).rstrip()
        first_link = re.search(r"(?m)^([ \t]+)<a\b", normalized)
        if first_link:
            link_indent = first_link.group(1)
            normalized = re.sub(
                r"(?m)^[ \t]*(<a\b[^>]*data/agent-index\.json[^>]*>Agent Map</a>)",
                link_indent + r"\1",
                normalized,
                flags=re.I,
            )
        return markup[: match.start("body")] + normalized + "\n" + open_line_indent + markup[match.end("body") :]

    trimmed = body.rstrip()
    trailing = body[len(trimmed) :]
    trimmed = re.sub(r"\n[ \t]*\n[ \t]*$", "\n", trimmed)
    if trailing:
        indent = trailing.split("\n")[-1]
        updated_body = trimmed + "\n" + indent + anchor + "\n" + open_line_indent
    else:
        updated_body = trimmed + " " + anchor
    return markup[: match.start("body")] + updated_body + markup[match.end("body") :]


# Inline CSS for the breadcrumb component. Kept inline (rather than in style.css)
# so pages render correctly without depending on a bumped style.css cache version.
BREADCRUMB_CSS = (
    # This element is a <nav>, so it inherits the global "nav{position:fixed;
    # top:0;z-index:200;...}" toolbar rule in style.css. That previously made the
    # breadcrumb a second full-width fixed bar that PAINTED OVER the primary nav
    # (logo + links + mobile hamburger), leaving the site header unusable on every
    # page. Fix: pin it as a slim bar directly BELOW the fixed nav, with a z-index
    # below the nav (200) so the nav always stays on top and clickable.
    ".breadcrumb{position:fixed;top:74px;left:0;right:0;z-index:150;background:var(--bg-primary);border-bottom:1px solid var(--paper-line);box-shadow:none;height:auto;min-height:0;padding:0 2rem;display:block;align-items:flex-start;justify-content:flex-start;max-width:1180px;margin:0 auto}"
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


# ── Single navigation manifest ──────────────────────────────────────────────
# One source of truth for EVERY page shell (root pages, works/papers/videos/
# domains/pillars, publications template). Six primary links render directly in
# the header so it never overflows at intermediate viewport widths; all other
# destinations stay reachable through the visible "More" disclosure. Replaces
# the divergent per-page navs that preceded this manifest.

def nav_manifest(depth: int = 0) -> tuple[list[tuple[str, str, str, str]], list[tuple[str, str, str, str]]]:
    """Return (primary, secondary) nav link tuples (key, href, label, extra_class)."""
    prefix = "../" * depth
    home = f"{prefix}index.html"
    primary = [
        ("publications", f"{prefix}publications.html", "Publications", ""),
        ("works", f"{prefix}works/", "Works", ""),
        ("domains", f"{prefix}domains.html", "Domains", ""),
        ("software", f"{prefix}software.html", "Software", ""),
        ("videos", f"{prefix}videos.html", "Videos", ""),
        ("art", f"{prefix}art.html", "Art", "nav-art-link"),
    ]
    secondary = [
        ("about", f"{home}#about", "About", ""),
        ("research", f"{home}#research", "Research", ""),
        ("media", f"{prefix}media.html", "Media", ""),
        ("collaborators", f"{prefix}collaborators.html", "Collaborators", ""),
        ("resume", f"{prefix}resume/resume.html", "CV", ""),
        ("search", f"{prefix}search.html", "Search", ""),
        ("catalog", f"{prefix}catalog.html", "Data Catalog", ""),
        ("evidence", f"{prefix}evidence.html", "Evidence", ""),
        ("reproducibility", f"{prefix}reproducibility.html", "Reproducibility", ""),
        ("cite", f"{prefix}cite-verify.html", "Cite", ""),
        ("discovery", f"{prefix}discovery.html", "Discovery", ""),
        ("agent-map", f"{prefix}data/agent-index.json", "Agent Map", ""),
    ]
    return primary, secondary


def _nav_anchor(key: str, href: str, label: str, extra: str, *, active: str = "") -> str:
    classes = [c for c in (extra, "active" if key == active else "") if c]
    attrs = f' class="{" ".join(classes)}"' if classes else ""
    current = ' aria-current="page"' if key == active else ""
    return f'<a href="{html.escape(href, quote=True)}"{attrs}{current}>{html.escape(label)}</a>'


def _render_nav_shell(*, active: str = "", depth: int = 0) -> str:
    """Render the shared header nav: plain <nav><ul><li><a> (no menubar roles)."""
    prefix = "../" * depth
    home = f"{prefix}index.html"
    primary, secondary = nav_manifest(depth)
    items = "\n".join(f"            <li>{_nav_anchor(*l, active=active)}</li>" for l in primary)
    more_items = "\n".join(f"                    <li>{_nav_anchor(*l, active=active)}</li>" for l in secondary)
    return (
        f'    <nav aria-label="Main navigation">\n'
        f'        <a href="{home}" class="nav-logo">Daniel Ari Friedman</a>\n'
        f'        <button class="menu-btn" aria-label="Toggle menu" aria-expanded="false" aria-controls="nav-menu">\u2630</button>\n'
        f'        <ul class="nav-links" id="nav-menu">\n'
        f"{items}\n"
        f'            <li>\n'
        f'                <details class="nav-more">\n'
        f'                    <summary>More</summary>\n'
        f'                    <ul class="nav-more-panel">\n'
        f"{more_items}\n"
        f"                    </ul>\n"
        f"                </details>\n"
        f"            </li>\n"
        f"        </ul>\n"
        f"    </nav>"
    )


def render_nav(*, active: str = "", depth: int = 0) -> str:
    """Shared header nav from the single manifest. depth=0 root, 1+ nested."""
    return _render_nav_shell(active=active, depth=depth)


def render_nav_domain(*, active: str = "domains", depth: int = 0) -> str:
    """Nav for domain pages — same shell, domains highlighted by default."""
    return _render_nav_shell(active=active, depth=depth)


def render_nav_compact(*, depth: int = 1) -> str:
    """Compact nav for work detail pages — same manifest shell, no default active."""
    return _render_nav_shell(active="", depth=depth)
