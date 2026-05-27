#!/usr/bin/env python3
"""Generate sitemap.xml from static pages, generated work pages, and data exports."""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "sitemap.xml"

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


def static_rows() -> list[tuple[str, str, str]]:
    return [
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
    ("repositories.html", "monthly", "0.6"),
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
    ("data/github-repositories.json", "monthly", "0.3"),
    ("data/people.json", "monthly", "0.3"),
    ("data/organizations.json", "monthly", "0.3"),
    ("data/claims.json", "monthly", "0.3"),
    ("data/resume.json", "monthly", "0.3"),
    ("data/catalog.json", "monthly", "0.3"),
    ("data/generated-manifest.json", "monthly", "0.3"),
    ("data/reconciliation.json", "monthly", "0.3"),
    ("GENERATED.md", "monthly", "0.2"),
    ("resume/README.md", "monthly", "0.2"),
    ("resume/full.txt", "monthly", "0.3"),
    ("resume/academic.txt", "monthly", "0.3"),
    ("resume/software-consulting.txt", "monthly", "0.3"),
    ("resume/teaching-service.txt", "monthly", "0.3"),
    ("resume/resume.pdf", "monthly", "0.4"),
    ("resume/verify.html", "monthly", "0.4"),
    ("CHANGELOG.md", "monthly", "0.2"),
    ("docs/REDIRECTS.md", "monthly", "0.2"),
    ("docs/RELEASE_2026-05_DISCOVERY_LAYER.md", "monthly", "0.2"),
    (_latest_rel("asset_size_*.json", "reports/asset_size_2026-05-13.json"), "monthly", "0.2"),
    (_latest_rel("public_source_snapshot_*.json", "reports/public_source_snapshot_2026-05-15.json"), "monthly", "0.2"),
    (_latest_rel("public_source_inventory_*.json", "reports/public_source_inventory_2026-05-15.json"), "monthly", "0.2"),
    (_latest_rel("live_site_verification_*.json", "reports/live_site_verification_2026-05-13.json"), "monthly", "0.2"),
    (_latest_rel("reconciliation_*.md", "reports/reconciliation_2026-05-15.md"), "monthly", "0.2"),
    (_latest_rel("accessibility_static_*.json", "reports/accessibility_static_2026-05-13.json"), "monthly", "0.2"),
    (_latest_rel("external_links_[0-9]*.json", "reports/external_links_2026-05-13.json"), "monthly", "0.2"),
    (_latest_rel("external_links_triage_*.json", "reports/external_links_triage_2026-05-13.json"), "monthly", "0.2"),
    (_latest_rel("external_links_triage_*.md", "reports/external_links_triage_2026-05-13.md"), "monthly", "0.2"),
    (_latest_subdir_rel("browser-smoke", "manifest.json", "reports/browser-smoke/2026-05-13/manifest.json"), "monthly", "0.2"),
    (_latest_subdir_rel("visual-qa", "manifest.json", "reports/visual-qa/2026-05-13/manifest.json"), "monthly", "0.2"),
    ]


def loc(rel: str) -> str:
    return "https://danielarifriedman.com/" + rel


def existing_lastmod() -> str | None:
    if not OUT.exists():
        return None
    match = re.search(r"<lastmod>([^<]+)</lastmod>", OUT.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def url_entry(rel_path: str, changefreq: str, priority: str, lastmod: str) -> str:
    return f"  <url><loc>{html.escape(loc(rel_path))}</loc><lastmod>{lastmod}</lastmod><changefreq>{changefreq}</changefreq><priority>{priority}</priority></url>"


def render(lastmod: str | None = None) -> str:
    date = lastmod or report_date_string()
    entries = [url_entry(*row, date) for row in static_rows()]
    works_dir = REPO_ROOT / "works"
    if works_dir.exists():
        for path in sorted(works_dir.glob("*.html")):
            if path.name == "index.html":
                continue
            entries.append(url_entry(f"works/{path.name}", "yearly", "0.45", date))
    return "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n" + "\n".join(entries) + "\n</urlset>\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if sitemap.xml is stale")
    args = parser.parse_args()
    content = render(existing_lastmod() if args.check else None)
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Stale generated sitemap.xml")
    else:
        OUT.write_text(content, encoding="utf-8")
    print(("checked" if args.check else "wrote") + " sitemap.xml")


if __name__ == "__main__":
    main()
