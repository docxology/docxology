"""Shared site navigation HTML for generated pages."""

from __future__ import annotations

import html


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
        ("search", f"{prefix}search.html", "Search"),
        ("catalog", f"{prefix}catalog.html", "Data Catalog"),
        ("cite", f"{prefix}cite-verify.html", "Cite"),
        ("discovery", f"{prefix}discovery.html", "Discovery"),
    ]
    parts = [
        f'    <nav role="navigation" aria-label="Main navigation">',
        f'        <a href="{home}" class="nav-logo">Daniel Ari Friedman</a>',
        '        <button class="menu-btn" onclick="document.querySelector(\'.nav-links\').classList.toggle(\'open\')" aria-label="Toggle menu">☰</button>',
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
        '        <button class="menu-btn" onclick="document.querySelector(\'.nav-links\').classList.toggle(\'open\')" aria-label="Toggle menu">☰</button>',
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
