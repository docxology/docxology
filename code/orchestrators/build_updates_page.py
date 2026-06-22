#!/usr/bin/env python3
"""Generate updates.html from CHANGELOG.md."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "CHANGELOG.md"
OUT = REPO_ROOT / "updates.html"

sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from site_nav import BREADCRUMB_CSS, breadcrumb_jsonld_script, render_breadcrumb  # noqa: E402

_BREADCRUMB = [("Home", ""), ("Updates", "updates.html")]


def _head_extra() -> str:
    return f"    <style>{BREADCRUMB_CSS}</style>\n{breadcrumb_jsonld_script(_BREADCRUMB)}\n"


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


VISUAL_EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\ufe0f]")


def strip_visual_emoji(value: str) -> str:
    return re.sub(r"\s{2,}", " ", VISUAL_EMOJI_RE.sub("", value)).strip()


def inline_md(value: str) -> str:
    escaped = h(strip_visual_emoji(value))
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
    date_modified = sections[0]["date"] if sections else ""
    data = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": "https://danielarifriedman.com/updates.html#webpage",
        "url": "https://danielarifriedman.com/updates.html",
        "name": "Updates — Daniel Ari Friedman",
        "description": "Human-readable changelog for the docxology public research and software index.",
        "dateModified": date_modified,
        "isPartOf": {"@id": "https://danielarifriedman.com/#website"},
        "about": {"@id": "https://danielarifriedman.com/#person"},
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": idx + 1,
                    "name": section["date"],
                    "description": strip_visual_emoji(" ".join(section["items"]))[:500],
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
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="Updates — Daniel Ari Friedman">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Updates — Daniel Ari Friedman">
    <meta name="twitter:description" content="Recent changes to the public research and software index.">
    <meta name="twitter:image" content="https://danielarifriedman.com/og-discovery.jpg">
    <meta name="twitter:image:alt" content="Updates — Daniel Ari Friedman">
    <link rel="stylesheet" href="style.css?v=newspaper-glitch-20260530c">
    <style>.updates-list{{display:grid;gap:1rem;max-width:920px;margin:0 auto}}.update-card{{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1.15rem}}.update-card h2{{font-size:1.1rem;color:var(--gold);margin-bottom:.7rem}}.update-card li{{margin:.45rem 0;color:var(--text-secondary);line-height:1.65}}.update-card code{{font-size:.86em;color:var(--silver-bright);background:rgba(255,255,255,.05);border:1px solid var(--border);border-radius:4px;padding:.05rem .24rem;overflow-wrap:anywhere}}</style>
    <script type="application/ld+json">
{json_ld(sections)}
    </script>
{_head_extra()}</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
    <nav role="navigation" aria-label="Main navigation">
        <a href="index.html" class="nav-logo">Daniel Ari Friedman</a>
        <button class="menu-btn" onclick="var o=document.querySelector('.nav-links').classList.toggle('open');this.setAttribute('aria-expanded',o)" aria-label="Toggle menu" aria-expanded="false">☰</button>
        <div class="nav-links"><a href="publications.html">Publications</a><a href="works/">Works</a><a href="search.html">Search</a><a href="discovery.html">Discovery</a><a href="updates.html" class="active">Updates</a></div>
    </nav>
{render_breadcrumb(_BREADCRUMB)}
    <header class="page-hero"><h1>Updates</h1><p class="sub">Recent changes to the public research, software, citation, evidence, and discovery index.</p></header>
    <main id="main" class="main"><section class="section"><div class="updates-list">
{body}
    </div></section></main>
    <footer role="contentinfo"><div class="footer-rule" aria-hidden="true"></div><p>Daniel Ari Friedman, PhD · <a href="CHANGELOG.md">CHANGELOG.md</a> · <a href="feed.xml">RSS feed</a></p></footer>
<script>/*menu-esc*/(function(){{if(window.__navEsc)return;window.__navEsc=1;document.addEventListener("keydown",function(e){{if(e.key==="Escape"){{var m=document.querySelector(".nav-links.open");if(m){{m.classList.remove("open");var b=document.querySelector(".menu-btn");if(b){{b.setAttribute("aria-expanded","false");b.focus();}}}}}}}});}})();</script></body>
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
