#!/usr/bin/env python3
"""Generate exports.html — HTML index of public machine-readable artifacts."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "exports.html"

EXPORT_ROW_SPECS: list[tuple[str, str, str, str]] = [
    ("CITATION.cff", "CITATION.cff", "Repository citation metadata for GitHub and Zenodo harvesters.", "text/x-yaml"),
    ("bibliography.bib", "BibTeX", "Full bibliography export for LaTeX, Pandoc, and citation managers.", "application/x-bibtex"),
    ("bibliography.csl.json", "CSL JSON", "citeproc- and Pandoc-compatible structured citations.", "application/json"),
    ("bibliography.ris", "RIS", "Import format for Zotero, EndNote, and Mendeley.", "application/x-research-info-systems"),
    ("codemeta.json", "CodeMeta", "Software and source metadata for research software indexers.", "application/json"),
    ("data/works.json", "Works JSON", "{works_count}-row structured bibliography with DOIs, domains, and doc paths.", "application/json"),
    ("data/software.json", "Software JSON", "Owned and AII software catalog rows.", "application/json"),
    ("data/catalog.json", "Catalog JSON", "Schema.org DataCatalog mirror of catalog.html.", "application/json"),
    ("data/claims.json", "Claims JSON", "Evidence ledger with confidence and source links.", "application/json"),
    ("data/people.json", "People JSON", "Collaborator and identity index.", "application/json"),
    ("data/organizations.json", "Organizations JSON", "Institutional affiliation index.", "application/json"),
    ("data/resume.json", "Resume JSON", "Structured CV data merged from resume/source.json.", "application/json"),
    ("data/artworks.json", "Artworks JSON", "Gallery metadata for pen-and-ink and blockchain art.", "application/json"),
    ("data/github-repositories.json", "GitHub inventory JSON", "Full public repository inventory.", "application/json"),
    ("data/work-enrichment.json", "Work enrichment JSON", "Abstracts and keywords extracted from paper folders.", "application/json"),
    ("data/generated-manifest.json", "Generated manifest JSON", "Source-to-output rebuild map.", "application/json"),
    ("data/reconciliation.json", "Reconciliation JSON", "Curated counts vs public-source indexes.", "application/json"),
    ("search-index.json", "Search index JSON", "Site-wide lexical index for search.html.", "application/json"),
    ("feed.xml", "RSS feed", "Recent works and site updates.", "application/rss+xml"),
    ("llms.txt", "LLMs.txt", "Agent-facing source map and crawl inventory.", "text/plain"),
]


def works_count() -> int:
    data = json.loads((REPO_ROOT / "data" / "works.json").read_text(encoding="utf-8"))
    return len(data["works"])


def export_rows() -> list[tuple[str, str, str, str]]:
    count = works_count()
    return [
        (rel, title, desc.format(works_count=count), mime)
        for rel, title, desc, mime in EXPORT_ROW_SPECS
    ]


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def render() -> str:
    cards = "\n".join(
        f"""                <article class="export-card">
                    <h2><a href="{h(rel)}">{h(title)}</a></h2>
                    <p>{h(desc)}</p>
                    <span class="mime">{h(mime)} · {h(rel)}</span>
                </article>"""
        for rel, title, desc, mime in export_rows()
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Public Exports — Daniel Ari Friedman</title>
    <meta name="description" content="Machine-readable citation exports, JSON datasets, and syndication files for Daniel Ari Friedman's public research index.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://danielarifriedman.com/exports.html">
    <link rel="alternate" type="application/x-bibtex" href="/bibliography.bib" title="BibTeX bibliography">
    <link rel="alternate" type="application/json" href="/bibliography.csl.json" title="CSL JSON bibliography">
    <link rel="alternate" href="/CITATION.cff" title="CITATION.cff">
    <link rel="alternate" type="application/json" href="/codemeta.json" title="CodeMeta">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Public Exports — Daniel Ari Friedman">
    <meta property="og:description" content="Citation exports and JSON datasets for the public research index.">
    <meta property="og:url" content="https://danielarifriedman.com/exports.html">
    <meta property="og:image" content="https://danielarifriedman.com/og-cite-verify.jpg">
    <link rel="stylesheet" href="style.css?v=newspaper-glitch-20260530c">
    <style>
        .export-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem}}
        .export-card{{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1rem}}
        .export-card h2{{font-size:1rem;margin-bottom:.4rem}}
        .export-card p{{color:var(--text-secondary);font-size:.86rem;line-height:1.6}}
        .export-card .mime{{display:block;margin-top:.75rem;color:var(--text-muted);font-size:.75rem;overflow-wrap:anywhere}}
    </style>
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
    <nav role="navigation" aria-label="Main navigation">
        <a href="index.html" class="nav-logo">Daniel Ari Friedman</a>
        <button class="menu-btn" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Toggle menu">☰</button>
        <div class="nav-links">
            <a href="publications.html">Publications</a>
            <a href="catalog.html">Data Catalog</a>
            <a href="cite-verify.html">Cite &amp; Verify</a>
            <a href="discovery.html">Discovery</a>
        </div>
    </nav>
    <header class="page-hero">
        <h1>Public Exports</h1>
        <p class="sub">Citation-manager formats and JSON datasets. All paths are public and crawlable; this page is the HTML index face for export discovery.</p>
    </header>
    <main id="main" class="main">
        <section class="section">
            <div class="export-grid">
{cards}
            </div>
            <p class="text-center mt-2"><a class="btn btn-outline" href="catalog.html">Full data catalog</a> <a class="btn btn-outline" href="cite-verify.html">Cite &amp; verify</a> <a class="btn btn-outline" href="llms.txt">LLMs.txt</a></p>
        </section>
    </main>
    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="https://danielarifriedman.com/">danielarifriedman.com</a></p>
    </footer>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if exports.html is stale")
    args = parser.parse_args()
    content = render()
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Stale generated exports.html")
    else:
        OUT.write_text(content, encoding="utf-8")
    print(("checked" if args.check else "wrote") + " exports.html")


if __name__ == "__main__":
    main()
