#!/usr/bin/env python3
"""Generate sitemap.xml from static pages, generated work pages, and data exports."""

from __future__ import annotations

import argparse
import html
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "sitemap.xml"
DATE = "2026-05-13"

STATIC = [
    ("", "weekly", "1.0"),
    ("publications.html", "monthly", "0.9"),
    ("works/", "monthly", "0.8"),
    ("domains.html", "monthly", "0.8"),
    ("domain-entomology.html", "monthly", "0.7"),
    ("domain-active-inference.html", "monthly", "0.7"),
    ("domain-cognitive-security.html", "monthly", "0.7"),
    ("domain-art-synergetics.html", "monthly", "0.7"),
    ("domain-computational.html", "monthly", "0.7"),
    ("art.html", "weekly", "0.9"),
    ("videos.html", "weekly", "0.8"),
    ("collaborators.html", "monthly", "0.7"),
    ("media.html", "monthly", "0.7"),
    ("software.html", "monthly", "0.7"),
    ("search.html", "monthly", "0.7"),
    ("catalog.html", "monthly", "0.6"),
    ("updates.html", "monthly", "0.6"),
    ("discovery.html", "monthly", "0.7"),
    ("cite-verify.html", "monthly", "0.6"),
    ("evidence.html", "monthly", "0.6"),
    ("feed.xml", "weekly", "0.5"),
    ("opensearch.xml", "monthly", "0.4"),
    ("llms.txt", "monthly", "0.5"),
    ("humans.txt", "monthly", "0.3"),
    ("AGENT_START.md", "monthly", "0.3"),
    ("search-index.json", "monthly", "0.4"),
    ("codemeta.json", "monthly", "0.4"),
    ("CITATION.cff", "monthly", "0.4"),
    ("bibliography.bib", "monthly", "0.4"),
    ("bibliography.csl.json", "monthly", "0.4"),
    ("bibliography.ris", "monthly", "0.4"),
    ("data/works.json", "monthly", "0.3"),
    ("data/artworks.json", "monthly", "0.3"),
    ("data/work-enrichment.json", "monthly", "0.3"),
    ("data/software.json", "monthly", "0.3"),
    ("data/people.json", "monthly", "0.3"),
    ("data/organizations.json", "monthly", "0.3"),
    ("data/claims.json", "monthly", "0.3"),
    ("data/catalog.json", "monthly", "0.3"),
    ("data/generated-manifest.json", "monthly", "0.3"),
    ("data/reconciliation.json", "monthly", "0.3"),
    ("GENERATED.md", "monthly", "0.2"),
    ("CHANGELOG.md", "monthly", "0.2"),
    ("docs/REDIRECTS.md", "monthly", "0.2"),
    ("docs/RELEASE_2026-05_DISCOVERY_LAYER.md", "monthly", "0.2"),
    ("reports/asset_size_2026-05-13.json", "monthly", "0.2"),
    ("reports/public_source_snapshot_2026-05-13.json", "monthly", "0.2"),
    ("reports/live_site_verification_2026-05-13.json", "monthly", "0.2"),
    ("reports/reconciliation_2026-05-13.md", "monthly", "0.2"),
    ("reports/accessibility_static_2026-05-13.json", "monthly", "0.2"),
    ("reports/external_links_2026-05-13.json", "monthly", "0.2"),
    ("reports/external_links_triage_2026-05-13.json", "monthly", "0.2"),
    ("reports/external_links_triage_2026-05-13.md", "monthly", "0.2"),
    ("reports/browser-smoke/2026-05-13/manifest.json", "monthly", "0.2"),
    ("reports/visual-qa/2026-05-13/manifest.json", "monthly", "0.2"),
]


def loc(rel: str) -> str:
    return "https://danielarifriedman.com/" + rel


def url_entry(rel: str, changefreq: str, priority: str) -> str:
    return f"  <url><loc>{html.escape(loc(rel))}</loc><lastmod>{DATE}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>"


def render() -> str:
    entries = [url_entry(*row) for row in STATIC]
    works_dir = REPO_ROOT / "works"
    if works_dir.exists():
        for path in sorted(works_dir.glob("*.html")):
            if path.name == "index.html":
                continue
            entries.append(url_entry(f"works/{path.name}", "yearly", "0.45"))
    return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "\n".join(entries) + "\n</urlset>\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if sitemap.xml is stale")
    args = parser.parse_args()
    content = render()
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Stale generated sitemap.xml")
    else:
        OUT.write_text(content, encoding="utf-8")
    print(("checked" if args.check else "wrote") + " sitemap.xml")


if __name__ == "__main__":
    main()
