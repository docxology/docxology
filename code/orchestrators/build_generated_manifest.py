#!/usr/bin/env python3
"""Generate a manifest documenting generated artifacts and rebuild commands."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from report_paths import generated_timestamp, latest_report, latest_subdir_file, rel
except ImportError:  # pragma: no cover - package import path
    from .report_paths import generated_timestamp, latest_report, latest_subdir_file, rel

REPO_ROOT = Path(__file__).resolve().parents[2]
JSON_OUT = REPO_ROOT / "data" / "generated-manifest.json"
MD_OUT = REPO_ROOT / "GENERATED.md"


def _latest_report(pattern: str, fallback: str) -> str:
    try:
        return rel(latest_report(pattern))
    except FileNotFoundError:
        return fallback


def _latest_subdir_manifest(prefix: str, fallback: str) -> str:
    try:
        latest = latest_subdir_file(prefix, "manifest.json")
    except FileNotFoundError:
        return fallback
    return rel(latest)


def _latest_subdir_pngs(prefix: str, fallback: str) -> str:
    try:
        latest = latest_subdir_file(prefix, "manifest.json")
    except FileNotFoundError:
        return fallback
    return rel(latest.parent / "*.png")


def _existing_generated_at() -> str | None:
    if not JSON_OUT.exists():
        return None
    try:
        return json.loads(JSON_OUT.read_text(encoding="utf-8")).get("generated_at")
    except json.JSONDecodeError:
        return None


LATEST_EXTERNAL_LINK_REPORT = _latest_report("external_links_[0-9]*.json", "reports/external_links_2026-05-13.json")

ARTIFACTS = [
    {
        "name": "Bibliography exports",
        "outputs": ["bibliography.bib", "bibliography.csl.json", "bibliography.ris", "data/works.json"],
        "sources": ["pages/BIBLIOGRAPHY.md", "code/src/biblio_table.py"],
        "command": "python3 code/orchestrators/export_bibliography.py",
    },
    {
        "name": "Scholar metrics sync",
        "outputs": [
            "pages/BIBLIOGRAPHY.md (badge)",
            "index.html (meta/og/stat/li)",
            "pages/PROFILE.md (prose + metrics table)",
            "pages/LINKS.md",
            "publications.html (header metrics pill)",
        ],
        "sources": ["data/scholar-snapshot.json", "code/orchestrators/sync_scholar_metrics.py"],
        "command": "python3 code/orchestrators/sync_scholar_metrics.py",
    },
    {
        "name": "Current count report",
        "outputs": ["reports/current_counts.md", "data/current-counts.json"],
        "sources": [
            "pages/BIBLIOGRAPHY.md",
            "papers/README.md",
            "pages/SOFTWARE.md",
            "data/works.json",
            "data/software.json",
            "data/github-repositories.json",
            "reports/public_source_snapshot_*.json",
            "reports/paired_publications_*.json",
        ],
        "command": "uv run python3 code/orchestrators/build_current_counts.py",
    },
    {
        "name": "Agent data exports",
        "outputs": ["data/software.json", "data/people.json", "data/organizations.json", "data/claims.json"],
        "sources": ["pages/SOFTWARE.md", "code/src/software_table.py", "data/scholar-snapshot.json", "code/orchestrators/export_agent_data.py"],
        "command": "python3 code/orchestrators/export_agent_data.py",
    },
    {
        "name": "Resume and CV exports",
        "outputs": [
            "data/resume.json",
            "resume/full.txt",
            "resume/academic.txt",
            "resume/software-consulting.txt",
            "resume/teaching-service.txt",
            "resume/resume.pdf",
            "resume/verify.html",
        ],
        "sources": [
            "resume/source.json",
            "data/works.json",
            "data/software.json",
            "data/scholar-snapshot.json",
            "data/claims.json",
            "code/src/resume_data.py",
            "code/orchestrators/build_resume.py",
        ],
        "command": "uv run python3 code/orchestrators/build_resume.py --all",
    },
    {
        "name": "Software catalog HTML sync",
        "outputs": ["software.html", "data/software-ld.json"],
        "sources": ["pages/SOFTWARE.md", "code/src/software_table.py", "code/orchestrators/sync_software_html.py"],
        "command": "python3 code/orchestrators/sync_software_html.py --apply",
    },
    {
        "name": "Full GitHub repository inventory",
        "outputs": ["data/github-repositories.json", "repositories.html"],
        "sources": ["GitHub REST API", "data/software.json", "code/orchestrators/build_github_inventory.py"],
        "command": "python3 code/orchestrators/build_github_inventory.py",
    },
    {
        "name": "Paired publication sync report",
        "outputs": [_latest_report("paired_publications_*.json", "reports/paired_publications_2026-05-27.json")],
        "sources": [
            "GitHub Releases API",
            "Zenodo Records API",
            "docs/operations/publication-sync.md",
            "code/src/publication_pairing.py",
            "code/orchestrators/sync_paired_publications.py",
        ],
        "command": "python3 code/orchestrators/sync_paired_publications.py",
    },
    {
        "name": "Paired publication review decisions",
        "outputs": ["data/paired-publication-decisions.json", _latest_report("paired_publications_review_queue_*.md", "reports/paired_publications_review_queue_2026-06-04.md")],
        "sources": [
            _latest_report("paired_publications_*.json", "reports/paired_publications_2026-06-04.json"),
            "manual review decision",
        ],
        "command": "manual review; update data/paired-publication-decisions.json",
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
        "name": "Video pages",
        "outputs": ["videos/*.html", "data/videos.json"],
        "sources": [
            "code/data/youtube_personal.json",
            "code/data/youtube_institute.json",
            "data/video-transcripts/*.txt",
            "data/works.json",
            "data/work-enrichment.json",
        ],
        "command": "python3 code/orchestrators/build_video_pages.py",
    },
    {
        "name": "Video transcript cache",
        "outputs": ["data/video-transcripts/*.txt"],
        "sources": ["YouTube captions", "code/orchestrators/fetch_video_transcripts.py"],
        "command": "python3 code/orchestrators/fetch_video_transcripts.py --channel all",
    },
    {
        "name": "Paper folder pages",
        "outputs": ["papers/*/index.html"],
        "sources": ["data/works.json", "papers/*/README.md", "papers/*/AGENTS.md", "papers/*/*.pdf"],
        "command": "python3 code/orchestrators/build_paper_pages.py",
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
        "name": "Exports hub",
        "outputs": ["exports.html"],
        "sources": ["code/orchestrators/build_exports_page.py", "data/catalog.json"],
        "command": "python3 code/orchestrators/build_exports_page.py",
    },
    {
        "name": "Updates page",
        "outputs": ["updates.html"],
        "sources": ["CHANGELOG.md", "code/orchestrators/build_updates_page.py"],
        "command": "python3 code/orchestrators/build_updates_page.py",
    },
    {
        "name": "External link report",
        "outputs": [_latest_report("external_links_[0-9]*.json", "reports/external_links_2026-05-13.json")],
        "sources": ["site-critical HTML, Markdown, and JSON-LD files"],
        "command": "python3 code/orchestrators/check_external_links.py",
    },
    {
        "name": "Public source snapshot",
        "outputs": [_latest_report("public_source_snapshot_*.json", "reports/public_source_snapshot_2026-05-15.json")],
        "sources": ["GitHub, ORCID, PubMed, Europe PMC, Crossref, Zenodo public APIs"],
        "command": "python3 code/orchestrators/refresh_public_sources.py",
    },
    {
        "name": "Public source inventory",
        "outputs": [_latest_report("public_source_inventory_*.json", "reports/public_source_inventory_2026-05-15.json")],
        "sources": ["ORCID, Crossref, PubMed, Europe PMC, Zenodo, Wikidata, Semantic Scholar, GitHub, AII pages"],
        "command": "python3 code/orchestrators/refresh_public_source_inventory.py",
    },
    {
        "name": "External link triage",
        "outputs": [
            _latest_report("external_links_triage_*.json", "reports/external_links_triage_2026-05-13.json"),
            _latest_report("external_links_triage_*.md", "reports/external_links_triage_2026-05-13.md"),
        ],
        "sources": [LATEST_EXTERNAL_LINK_REPORT],
        "command": "python3 code/orchestrators/build_external_link_triage.py",
    },
    {
        "name": "Asset size audit",
        "outputs": [_latest_report("asset_size_*.json", "reports/asset_size_2026-05-13.json")],
        "sources": ["root HTML pages", "og-*.jpg", "data/*.json", "style.css", "sw.js"],
        "command": "python3 code/orchestrators/audit_assets.py",
    },
    {
        "name": "Static accessibility report",
        "outputs": [_latest_report("accessibility_static_*.json", "reports/accessibility_static_2026-05-13.json")],
        "sources": ["root HTML pages", "style.css", "code/orchestrators/accessibility_audit.py"],
        "command": "python3 code/orchestrators/accessibility_audit.py",
    },
    {
        "name": "Browser smoke checks",
        "outputs": [
            _latest_subdir_pngs("browser-smoke", "reports/browser-smoke/2026-05-13/*.png"),
            _latest_subdir_manifest("browser-smoke", "reports/browser-smoke/2026-05-13/manifest.json"),
        ],
        "sources": ["root HTML pages", "works/index.html", "search-index.json"],
        "command": "python3 code/orchestrators/browser_smoke.py",
    },
    {
        "name": "Live site verification",
        "outputs": [_latest_report("live_site_verification_*.json", "reports/live_site_verification_2026-05-13.json")],
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
        "sources": ["works/*.html", "code/src/sitemap_policy.py", "code/orchestrators/build_sitemap.py"],
        "command": "python3 code/orchestrators/build_sitemap.py",
    },
    {
        "name": "Visual QA",
        "outputs": [
            _latest_subdir_pngs("visual-qa", "reports/visual-qa/2026-05-13/*.png"),
            _latest_subdir_manifest("visual-qa", "reports/visual-qa/2026-05-13/manifest.json"),
        ],
        "sources": ["root HTML pages", "style.css"],
        "command": "python3 code/orchestrators/visual_qa.py",
    },
]


def render_json(generated_at: str | None = None) -> str:
    generated_at = generated_at or generated_timestamp()
    return json.dumps({"generated_at": generated_at, "artifacts": ARTIFACTS}, indent=2, ensure_ascii=False) + "\n"


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


def outputs(generated_at: str | None = None) -> dict[Path, str]:
    return {JSON_OUT: render_json(generated_at), MD_OUT: render_md()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated manifest files are stale")
    args = parser.parse_args()
    stale = []
    generated_at = _existing_generated_at() if args.check else None
    for path, content in outputs(generated_at).items():
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
