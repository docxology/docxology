#!/usr/bin/env python3
"""Generate updates.html from CHANGELOG.md."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "CHANGELOG.md"
OUT = REPO_ROOT / "updates.html"


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def inline_md(value: str) -> str:
    escaped = h(value)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)


def parse_changelog() -> list[dict]:
    text = SOURCE.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.M))
    sections = []
    for i, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        bullets = []
        for line in text[start:end].splitlines():
            stripped = line.strip()
            if stripped.startswith("- "):
                bullets.append(stripped[2:])
        if bullets:
            sections.append({"date": title, "items": bullets})
    return sections


def json_ld(sections: list[dict]) -> str:
    data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": "https://danielarifriedman.com/updates.html#webpage",
        "url": "https://danielarifriedman.com/updates.html",
        "name": "Updates — Daniel Ari Friedman",
        "description": "Human-readable changelog for the docxology public research and software index.",
        "dateModified": "2026-05-13",
        "isPartOf": {"@id": "https://danielarifriedman.com/#website"},
        "about": {"@id": "https://danielarifriedman.com/#person"},
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": idx + 1,
                    "name": section["date"],
                    "description": " ".join(section["items"])[:500],
                }
                for idx, section in enumerate(sections)
            ],
        },
    }
    return json.dumps(data, indent=4, ensure_ascii=False)


def render() -> str:
    sections = parse_changelog()
    body = "\n".join(
        f"""            <article class="update-card">
                <h2>{h(section['date'])}</h2>
                <ul>{''.join(f'<li>{inline_md(item)}</li>' for item in section['items'])}</ul>
            </article>"""
        for section in sections
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Updates — Daniel Ari Friedman</title>
    <meta name="description" content="Human-readable updates for the docxology public research, software, citation, evidence, and discovery index.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://danielarifriedman.com/updates.html">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Daniel Ari Friedman updates">
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Daniel Ari Friedman">
    <link rel="alternate" type="text/markdown" href="/CHANGELOG.md" title="Changelog source">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Updates — Daniel Ari Friedman">
    <meta property="og:description" content="Recent changes to the public research and software index.">
    <meta property="og:url" content="https://danielarifriedman.com/updates.html">
    <meta property="og:image" content="https://danielarifriedman.com/og-discovery.jpg">
    <link rel="stylesheet" href="style.css">
    <style>.updates-list{{display:grid;gap:1rem;max-width:920px;margin:0 auto}}.update-card{{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1.15rem}}.update-card h2{{font-size:1.1rem;color:var(--gold);margin-bottom:.7rem}}.update-card li{{margin:.45rem 0;color:var(--text-secondary);line-height:1.65}}.update-card code{{font-size:.86em;color:var(--silver-bright);background:rgba(255,255,255,.05);border:1px solid var(--border);border-radius:4px;padding:.05rem .24rem;overflow-wrap:anywhere}}</style>
    <script type="application/ld+json">
{json_ld(sections)}
    </script>
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
    <nav role="navigation" aria-label="Main navigation">
        <a href="index.html" class="nav-logo">Daniel Ari Friedman</a>
        <button class="menu-btn" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Toggle menu">☰</button>
        <div class="nav-links"><a href="publications.html">Publications</a><a href="works/">Works</a><a href="search.html">Search</a><a href="discovery.html">Discovery</a><a href="updates.html" class="active">Updates</a></div>
    </nav>
    <header class="page-hero"><h1>Updates</h1><p class="sub">Recent changes to the public research, software, citation, evidence, and discovery index.</p></header>
    <main id="main" class="main"><section class="section"><div class="updates-list">
{body}
    </div></section></main>
    <footer role="contentinfo"><div class="footer-rule" aria-hidden="true"></div><p>Daniel Ari Friedman, PhD · <a href="CHANGELOG.md">CHANGELOG.md</a> · <a href="feed.xml">RSS feed</a></p></footer>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if updates.html is stale")
    args = parser.parse_args()
    content = render()
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Stale updates.html")
    else:
        OUT.write_text(content, encoding="utf-8")
    print(("checked" if args.check else "wrote") + " updates.html")


if __name__ == "__main__":
    main()
