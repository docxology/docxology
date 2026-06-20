#!/usr/bin/env python3
"""Render evidence.html and pages/EVIDENCE.md from data/claims.json."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HTML_OUT = REPO_ROOT / "evidence.html"
MD_OUT = REPO_ROOT / "pages" / "EVIDENCE.md"

sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from site_nav import BREADCRUMB_CSS, breadcrumb_jsonld_script, render_breadcrumb  # noqa: E402

_BREADCRUMB = [("Home", ""), ("Evidence", "evidence.html")]
_WEBPAGE_LD = {
    "@context": "https://schema.org",
    "@type": "WebPage",
    "@id": "https://danielarifriedman.com/evidence.html#page",
    "name": "Evidence Ledger — Daniel Ari Friedman",
    "description": "Claim-level evidence ledger for Daniel Ari Friedman: source links, confidence levels, caveats, and latest public-source snapshot.",
    "url": "https://danielarifriedman.com/evidence.html",
    "isPartOf": {"@id": "https://danielarifriedman.com/#website"},
}


def _head_extra() -> str:
    return (
        f"    <style>{BREADCRUMB_CSS}</style>\n"
        f'    <script type="application/ld+json">\n{json.dumps(_WEBPAGE_LD, indent=4, ensure_ascii=False)}\n    </script>\n'
        f"{breadcrumb_jsonld_script(_BREADCRUMB)}\n"
    )

try:
    from report_paths import latest_report, rel
except ImportError:  # pragma: no cover - package import path
    from .report_paths import latest_report, rel


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_claims() -> list[dict]:
    with open(REPO_ROOT / "data" / "claims.json", encoding="utf-8") as f:
        return json.load(f)["claims"]


def source_link(source: str, prefix: str = "") -> str:
    if source.startswith("http"):
        return source
    return prefix + source


def latest_report_link(pattern: str, fallback: str, prefix: str = "") -> str:
    try:
        path = rel(latest_report(pattern))
    except FileNotFoundError:
        path = fallback
    return prefix + path


def render_html(claims: list[dict]) -> str:
    snapshot = latest_report_link("public_source_snapshot_*.json", "reports/public_source_snapshot_2026-05-15.json")
    inventory = latest_report_link("public_source_inventory_*.json", "reports/public_source_inventory_2026-05-15.json")
    cards = []
    for claim in claims:
        first_source = claim["sources"][0]
        cards.append(
            f"""                <article class="claim-card">
                    <h3>{h(claim['claim'])}</h3>
                    <p>{h(claim['caveat'])}</p>
                    <dl>
                        <div><dt>Status</dt><dd>{h(claim['status'])}</dd></div>
                        <div><dt>Confidence</dt><dd>{h(claim['confidence'].title())}</dd></div>
                        <div><dt>Checked</dt><dd>{h(claim['checked_at'])}</dd></div>
                        <div><dt>Owner</dt><dd>{h(claim['maintenance_owner'])}</dd></div>
                    </dl>
                    <p class="claim-source"><a href="{h(source_link(first_source))}">{h(first_source)}</a></p>
                </article>"""
        )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Evidence Ledger — Daniel Ari Friedman</title>
    <meta name="description" content="Claim-level evidence ledger for Daniel Ari Friedman: source links, confidence levels, caveats, and latest public-source snapshot.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://danielarifriedman.com/evidence.html">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Daniel Ari Friedman updates">
    <link rel="alternate" type="text/plain" href="/llms.txt" title="LLMs.txt">
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Daniel Ari Friedman">
    <link rel="alternate" type="application/json" href="/search-index.json" title="Site search index">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Evidence Ledger — Daniel Ari Friedman">
    <meta property="og:description" content="Claim-level evidence ledger with source links, confidence levels, and caveats.">
    <meta property="og:url" content="https://danielarifriedman.com/evidence.html">
    <meta property="og:image" content="https://danielarifriedman.com/og-cite-verify.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="Evidence Ledger — Daniel Ari Friedman">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="Evidence Ledger — Daniel Ari Friedman">
    <meta name="twitter:description" content="Claim-level evidence ledger with source links, confidence levels, and caveats.">
    <meta name="twitter:image" content="https://danielarifriedman.com/og-cite-verify.jpg">
    <meta name="twitter:image:alt" content="Evidence Ledger — Daniel Ari Friedman">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css?v=newspaper-glitch-20260530c">
    <meta name="theme-color" content="#0c0c0e">
    <style>
        .claim-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1rem}}
        .claim-card{{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1rem;display:flex;flex-direction:column;gap:.75rem}}
        .claim-card h3{{font-size:1rem;line-height:1.45;color:#fff}}
        .claim-card p{{font-size:.84rem;color:var(--text-secondary);line-height:1.6}}
        .claim-card dl{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:.55rem}}
        .claim-card dt{{font-size:.66rem;text-transform:uppercase;letter-spacing:.08em;color:var(--text-muted)}}
        .claim-card dd{{font-size:.82rem;color:var(--silver-bright);margin:0}}
        .claim-source{{margin-top:auto;overflow-wrap:anywhere}}
    </style>
{_head_extra()}</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
    <nav role="navigation" aria-label="Main navigation">
        <a href="index.html" class="nav-logo">Daniel Ari Friedman</a>
        <button class="menu-btn" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Toggle menu">☰</button>
        <div class="nav-links">
            <a href="index.html#about">About</a>
            <a href="publications.html">Publications</a>
            <a href="domains.html">Domains</a>
            <a href="software.html">Software</a>
            <a href="discovery.html">Discovery</a>
            <a href="cite-verify.html">Cite</a>
        </div>
    </nav>
{render_breadcrumb(_BREADCRUMB)}
    <header class="page-hero">
        <h1>Evidence Ledger</h1>
        <p class="sub">Source links, confidence levels, caveats, maintenance owners, and public-source freshness reports for key site claims.</p>
    </header>
    <main id="main" class="main">
        <section class="section">
            <div class="section-header"><h2>Claim Register</h2><p>Use this table as an audit trail, not a substitute for primary sources.</p><div class="section-divider"></div></div>
            <div class="claim-grid">
{chr(10).join(cards)}
            </div>
            <p class="text-center mt-2"><a class="btn btn-outline" href="data/claims.json">Claims JSON</a> <a class="btn btn-outline" href="data/reconciliation.json">Reconciliation JSON</a> <a class="btn btn-outline" href="{h(snapshot)}">Latest snapshot</a> <a class="btn btn-outline" href="{h(inventory)}">Source inventory</a></p>
        </section>
    </main>
    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="https://danielarifriedman.com/">danielarifriedman.com</a></p>
        <div class="footer-links"><a href="cite-verify.html">Cite & Verify</a><a href="discovery.html">Discovery</a><a href="pages/EVIDENCE.md">Markdown</a><a href="https://github.com/docxology/docxology">Source Repo</a></div>
    </footer>
</body>
</html>
"""


def render_md(claims: list[dict]) -> str:
    snapshot = latest_report_link("public_source_snapshot_*.json", "reports/public_source_snapshot_2026-05-15.json", "../")
    inventory = latest_report_link("public_source_inventory_*.json", "reports/public_source_inventory_2026-05-15.json", "../")
    lines = [
        "---",
        'title: "EVIDENCE - Daniel Ari Friedman"',
        'description: "Claim-level evidence ledger with source links, confidence, caveats, and maintenance ownership."',
        'keywords: "Daniel Ari Friedman, evidence ledger, claims, verification, source freshness"',
        "---",
        "<div align=\"center\">",
        "",
        "# Evidence Ledger",
        "",
        "> **Navigation**: [🏠 Home](../README.md) | [🧭 Discovery](DISCOVERY.md) | [🧾 Cite & Verify](CITE_VERIFY.md) | [📚 Bibliography](BIBLIOGRAPHY.md)",
        "",
        f"[Website version](../evidence.html) · [Source claims JSON](../data/claims.json) · [Reconciliation JSON](../data/reconciliation.json) · [Latest public-source snapshot]({snapshot}) · [Public-source inventory]({inventory})",
        "",
        "</div>",
        "",
        "---",
        "",
        "This ledger records selected public claims, the type of source backing each claim, the confidence level, and the caveat that should travel with the claim.",
        "",
        "| Claim | Status | Confidence | Checked | Owner | Sources | Caveat |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for claim in claims:
        sources = "<br>".join(f"[{src}]({source_link(src, '../')})" for src in claim["sources"])
        lines.append(
            f"| {claim['claim']} | {claim['status']} | {claim['confidence']} | {claim['checked_at']} | {claim['maintenance_owner']} | {sources} | {claim['caveat']} |"
        )
    lines.extend(
        [
            "",
            "## Maintenance Notes",
            "",
            "- Prefer public APIs as freshness checks, not as automatic overrides of curated local metadata.",
            "- If a claim changes, update `code/orchestrators/export_agent_data.py`, regenerate `data/claims.json`, and then regenerate this page.",
            "- Use conservative language when an external source depends on definitions that vary across communities.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def outputs() -> dict[Path, str]:
    claims = load_claims()
    return {HTML_OUT: render_html(claims), MD_OUT: render_md(claims)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if evidence pages are stale")
    args = parser.parse_args()
    stale = []
    for path, content in outputs().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale generated evidence pages: " + ", ".join(stale))
    print(("checked" if args.check else "wrote") + " evidence pages")


if __name__ == "__main__":
    main()
