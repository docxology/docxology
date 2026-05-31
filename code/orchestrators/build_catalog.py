#!/usr/bin/env python3
"""Generate DataCatalog JSON and HTML for structured scholarly exports."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
JSON_OUT = REPO_ROOT / "data" / "catalog.json"
HTML_OUT = REPO_ROOT / "catalog.html"

# Self-contained creator node so Google can resolve the Dataset/DataCatalog
# `creator` field on this page without dereferencing the index-page #person node.
CREATOR = {
    "@type": "Person",
    "@id": "https://danielarifriedman.com/#person",
    "name": "Daniel Ari Friedman",
    "url": "https://danielarifriedman.com/",
}
LICENSE = "https://creativecommons.org/licenses/by/4.0/"

try:
    from report_paths import latest_report, latest_subdir_file, rel, report_date_string
except ImportError:  # pragma: no cover - package import path
    from .report_paths import latest_report, latest_subdir_file, rel, report_date_string


def _latest_rel(pattern: str, fallback: str) -> str:
    try:
        return rel(latest_report(pattern))
    except FileNotFoundError:
        return fallback


def _latest_subdir_rel(prefix: str, filename: str, fallback: str) -> str:
    try:
        latest = latest_subdir_file(prefix, filename)
    except FileNotFoundError:
        return fallback
    return rel(latest)


def datasets() -> list[tuple[str, str, str, str]]:
    return [
    ("works", "Curated Works Bibliography", "data/works.json", "149 bibliography rows with citation keys, DOI links, domains, and documentation paths."),
    ("artworks", "Artwork Gallery Data", "data/artworks.json", "Structured metadata for 942 artworks used by the gallery without embedding the full payload in art.html."),
    ("software", "Software Catalog", "data/software.json", "82 catalogued software repositories across docxology and AII contributions."),
    ("github-repositories", "Full GitHub Repository Inventory", "data/github-repositories.json", "Generated full inventory of public docxology and Active Inference Institute repositories with curated catalog flags."),
    ("people", "People Index", "data/people.json", "Compact collaborator and identity context for agentic discovery."),
    ("organizations", "Organizations Index", "data/organizations.json", "Organization context for AII, COGSEC, Stanford, and teaching affiliations."),
    ("claims", "Evidence Claims", "data/claims.json", "Claim-level evidence ledger with confidence, source links, and caveats."),
    ("resume", "Structured Resume and CV", "data/resume.json", "Merged resume/CV data with contact, education, experience, works, software, service, media, and art-use records."),
    ("resume-verify", "Resume Verification Page", "resume/verify.html", "HTML verification surface with source manifest, generated JSON hash, final PDF hash, file sizes, counts, and artifact links."),
    ("reconciliation", "Public-Source Reconciliation", "data/reconciliation.json", "Curated local counts compared with public-source indexes."),
    ("work-enrichment", "Work Enrichment", "data/work-enrichment.json", "Extracted abstracts, keywords, methods, and findings from per-paper README and SKILL files."),
    ("generated-manifest", "Generated Artifact Manifest", "data/generated-manifest.json", "Source-to-output map and rebuild commands for generated files."),
    ("search", "Search Index", "search-index.json", "Site-wide index covering pages, works, software, people, organizations, and claims."),
    ("public-source-inventory", "Public Source Inventory", _latest_rel("public_source_inventory_*.json", "reports/public_source_inventory_2026-05-15.json"), "Paginated public-source inventory for ORCID, Crossref, PubMed, Europe PMC, Zenodo, Wikidata, Semantic Scholar, GitHub, and AII pages."),
    ("public-source-snapshot", "Public Source Snapshot", _latest_rel("public_source_snapshot_*.json", "reports/public_source_snapshot_2026-05-15.json"), "Current public API freshness snapshot with normalized drift-comparison facts."),
    ("external-links", "External Link Report", _latest_rel("external_links_[0-9]*.json", "reports/external_links_2026-05-13.json"), "Scoped network freshness report for site-critical outbound links."),
    ("external-link-triage", "External Link Triage", _latest_rel("external_links_triage_*.json", "reports/external_links_triage_2026-05-13.json"), "Categorized link warnings: bot-protected, transient, timeout, stale, and review."),
    ("asset-size", "Asset Size Audit", _latest_rel("asset_size_*.json", "reports/asset_size_2026-05-13.json"), "Size report for public HTML, OG images, data exports, and runtime assets."),
    ("browser-smoke", "Browser Smoke Manifest", _latest_subdir_rel("browser-smoke", "manifest.json", "reports/browser-smoke/2026-05-13/manifest.json"), "Selector-based Playwright smoke checks for core local pages."),
    ("live-site", "Live Site Verification", _latest_rel("live_site_verification_*.json", "reports/live_site_verification_2026-05-13.json"), "Deployed-site status, CDN headers, expected markers, and GitHub Pages build status."),
    ]


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def absolute(rel: str) -> str:
    return f"https://danielarifriedman.com/{rel}"


def encoding_format(rel: str) -> str:
    if rel.endswith(".html"):
        return "text/html"
    if rel.endswith(".md"):
        return "text/markdown"
    if rel.endswith(".xml"):
        return "application/xml"
    return "application/json"


def existing_date_modified() -> str | None:
    if not JSON_OUT.exists():
        return None
    try:
        return json.loads(JSON_OUT.read_text(encoding="utf-8")).get("dateModified")
    except json.JSONDecodeError:
        return None


def catalog_payload(date_modified: str | None = None) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "DataCatalog",
        "@id": "https://danielarifriedman.com/catalog.html#catalog",
        "name": "Daniel Ari Friedman Public Research Data Catalog",
        "description": "Machine-readable datasets for Daniel Ari Friedman's public research, software, citation, and evidence index.",
        "url": "https://danielarifriedman.com/catalog.html",
        "creator": CREATOR,
        "dateModified": date_modified or report_date_string(),
        "license": LICENSE,
        "dataset": [
            {
                "@type": "Dataset",
                "@id": f"https://danielarifriedman.com/catalog.html#{slug}",
                "name": name,
                "description": desc,
                "url": absolute(rel),
                "encodingFormat": encoding_format(rel),
                "creator": CREATOR,
                "license": LICENSE,
                "includedInDataCatalog": {"@id": "https://danielarifriedman.com/catalog.html#catalog"},
                "distribution": {
                    "@type": "DataDownload",
                    "contentUrl": absolute(rel),
                    "encodingFormat": encoding_format(rel),
                },
            }
            for slug, name, rel, desc in datasets()
        ],
    }


def render_json(date_modified: str | None = None) -> str:
    return json.dumps(catalog_payload(date_modified), indent=2, ensure_ascii=False) + "\n"


def render_html(date_modified: str | None = None) -> str:
    rows = "\n".join(
        f"""                <article class="catalog-card" id="{h(slug)}">
                    <h2><a href="{h(rel)}">{h(name)}</a></h2>
                    <p>{h(desc)}</p>
                    <span>{h(rel)}</span>
                </article>"""
        for slug, name, rel, desc in datasets()
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Catalog — Daniel Ari Friedman</title>
    <meta name="description" content="Structured data catalog for Daniel Ari Friedman's public research, software, bibliography, evidence, and search exports.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://danielarifriedman.com/catalog.html">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Daniel Ari Friedman updates">
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Daniel Ari Friedman">
    <link rel="alternate" type="application/json" href="/data/catalog.json" title="Data catalog JSON">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Data Catalog — Daniel Ari Friedman">
    <meta property="og:description" content="Structured JSON datasets for the public research and software index.">
    <meta property="og:url" content="https://danielarifriedman.com/catalog.html">
    <meta property="og:image" content="https://danielarifriedman.com/og-discovery.jpg">
    <link rel="stylesheet" href="style.css?v=newspaper-glitch-20260530c">
    <style>.catalog-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:1rem}}.catalog-card{{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1rem}}.catalog-card h2{{font-size:1rem;margin-bottom:.4rem}}.catalog-card p{{color:var(--text-secondary);font-size:.86rem;line-height:1.6}}.catalog-card span{{display:block;margin-top:.75rem;color:var(--text-muted);font-size:.75rem;overflow-wrap:anywhere}}</style>
    <script type="application/ld+json">
{render_json(date_modified)}
    </script>
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
    <nav role="navigation" aria-label="Main navigation">
        <a href="index.html" class="nav-logo">Daniel Ari Friedman</a>
        <button class="menu-btn" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Toggle menu">☰</button>
        <div class="nav-links"><a href="publications.html">Publications</a><a href="works/">Works</a><a href="catalog.html">Data Catalog</a><a href="exports.html">Exports</a><a href="cite-verify.html">Cite</a><a href="discovery.html">Discovery</a></div>
    </nav>
    <header class="page-hero"><h1>Data Catalog</h1><p class="sub">Structured exports for the bibliography, software catalog, evidence layer, and agentic discovery surfaces.</p></header>
    <main id="main" class="main"><section class="section"><div class="catalog-grid">
{rows}
    </div></section></main>
    <footer role="contentinfo"><div class="footer-rule" aria-hidden="true"></div><p>Daniel Ari Friedman, PhD · <a href="data/catalog.json">catalog.json</a></p></footer>
</body>
</html>
"""


def outputs(date_modified: str | None = None) -> dict[Path, str]:
    return {JSON_OUT: render_json(date_modified), HTML_OUT: render_html(date_modified)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated catalog files are stale")
    args = parser.parse_args()
    stale = []
    date_modified = existing_date_modified() if args.check else None
    for path, content in outputs(date_modified).items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale generated catalog files: " + ", ".join(stale))
    print(("checked" if args.check else "wrote") + " catalog files")


if __name__ == "__main__":
    main()
