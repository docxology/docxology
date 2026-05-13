#!/usr/bin/env python3
"""Generate a manifest documenting generated artifacts and rebuild commands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
JSON_OUT = REPO_ROOT / "data" / "generated-manifest.json"
MD_OUT = REPO_ROOT / "GENERATED.md"

ARTIFACTS = [
    {
        "name": "Bibliography exports",
        "outputs": ["bibliography.bib", "bibliography.csl.json", "bibliography.ris", "data/works.json"],
        "sources": ["pages/BIBLIOGRAPHY.md", "papers/biblio_table.py"],
        "command": "python3 code/orchestrators/export_bibliography.py",
    },
    {
        "name": "Agent data exports",
        "outputs": ["data/software.json", "data/people.json", "data/organizations.json", "data/claims.json"],
        "sources": ["pages/SOFTWARE.md", "code/orchestrators/export_agent_data.py"],
        "command": "python3 code/orchestrators/export_agent_data.py",
    },
    {
        "name": "Domain pages",
        "outputs": ["domains.html", "domain-*.html", "pages/DOMAINS.md"],
        "sources": ["data/works.json", "data/software.json", "code/orchestrators/build_domain_pages.py"],
        "command": "python3 code/orchestrators/build_domain_pages.py",
    },
    {
        "name": "Work pages",
        "outputs": ["works/*.html", "data/work-enrichment.json"],
        "sources": ["data/works.json", "papers/*/README.md", "papers/*/SKILL.md"],
        "command": "python3 code/orchestrators/build_work_pages.py",
    },
    {
        "name": "Evidence pages",
        "outputs": ["evidence.html", "pages/EVIDENCE.md"],
        "sources": ["data/claims.json", "code/orchestrators/build_evidence_page.py"],
        "command": "python3 code/orchestrators/build_evidence_page.py",
    },
    {
        "name": "Search index",
        "outputs": ["search-index.json"],
        "sources": ["data/*.json", "data/work-enrichment.json"],
        "command": "python3 code/orchestrators/build_search_index.py",
    },
    {
        "name": "Data catalog",
        "outputs": ["catalog.html", "data/catalog.json"],
        "sources": ["code/orchestrators/build_catalog.py", "data/*.json"],
        "command": "python3 code/orchestrators/build_catalog.py",
    },
    {
        "name": "Updates page",
        "outputs": ["updates.html"],
        "sources": ["CHANGELOG.md", "code/orchestrators/build_updates_page.py"],
        "command": "python3 code/orchestrators/build_updates_page.py",
    },
    {
        "name": "External link report",
        "outputs": ["reports/external_links_2026-05-13.json"],
        "sources": ["site-critical HTML, Markdown, and JSON-LD files"],
        "command": "python3 code/orchestrators/check_external_links.py",
    },
    {
        "name": "External link triage",
        "outputs": ["reports/external_links_triage_2026-05-13.json", "reports/external_links_triage_2026-05-13.md"],
        "sources": ["reports/external_links_2026-05-13.json"],
        "command": "python3 code/orchestrators/build_external_link_triage.py",
    },
    {
        "name": "Asset size audit",
        "outputs": ["reports/asset_size_2026-05-13.json"],
        "sources": ["root HTML pages", "og-*.jpg", "data/*.json", "style.css", "sw.js"],
        "command": "python3 code/orchestrators/audit_assets.py",
    },
    {
        "name": "Browser smoke checks",
        "outputs": ["reports/browser-smoke/2026-05-13/*.png", "reports/browser-smoke/2026-05-13/manifest.json"],
        "sources": ["root HTML pages", "works/index.html", "search-index.json"],
        "command": "python3 code/orchestrators/browser_smoke.py",
    },
    {
        "name": "Live site verification",
        "outputs": ["reports/live_site_verification_2026-05-13.json"],
        "sources": ["https://danielarifriedman.com/", "GitHub Pages API"],
        "command": "python3 code/orchestrators/verify_live_site.py",
    },
    {
        "name": "Feed",
        "outputs": ["feed.xml"],
        "sources": ["data/works.json", "code/orchestrators/generate_feed.py"],
        "command": "python3 code/orchestrators/generate_feed.py",
    },
    {
        "name": "Sitemap",
        "outputs": ["sitemap.xml"],
        "sources": ["works/*.html", "code/orchestrators/build_sitemap.py"],
        "command": "python3 code/orchestrators/build_sitemap.py",
    },
    {
        "name": "Visual QA",
        "outputs": ["reports/visual-qa/2026-05-13/*.png", "reports/visual-qa/2026-05-13/manifest.json"],
        "sources": ["root HTML pages", "style.css"],
        "command": "python3 code/orchestrators/visual_qa.py",
    },
]


def render_json() -> str:
    return json.dumps({"generated_at": "2026-05-13", "artifacts": ARTIFACTS}, indent=2, ensure_ascii=False) + "\n"


def render_md() -> str:
    lines = [
        "# Generated Files",
        "",
        "This repository keeps public site pages, citation exports, data indexes, and QA reports as checked-in generated artifacts so GitHub Pages can serve them statically.",
        "",
        "| Artifact | Outputs | Sources | Rebuild command |",
        "| --- | --- | --- | --- |",
    ]
    for item in ARTIFACTS:
        outputs = "<br>".join(f"`{value}`" for value in item["outputs"])
        sources = "<br>".join(f"`{value}`" for value in item["sources"])
        lines.append(f"| {item['name']} | {outputs} | {sources} | `{item['command']}` |")
    lines.extend(
        [
            "",
            "## Validation",
            "",
            "Run `python3 code/orchestrators/validate_repo.py` before declaring the generated layer current.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def outputs() -> dict[Path, str]:
    return {JSON_OUT: render_json(), MD_OUT: render_md()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated manifest files are stale")
    args = parser.parse_args()
    stale = []
    for path, content in outputs().items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale generated manifest files: " + ", ".join(stale))
    print(("checked" if args.check else "wrote") + " generated manifest")


if __name__ == "__main__":
    main()
