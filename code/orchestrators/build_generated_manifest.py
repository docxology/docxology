#!/usr/bin/env python3
"""Generate a manifest documenting generated artifacts and rebuild commands."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

try:
    from report_paths import generated_timestamp, latest_source_report, latest_source_subdir_file, rel
except ImportError:  # pragma: no cover - package import path
    from .report_paths import generated_timestamp, latest_source_report, latest_source_subdir_file, rel

JSON_OUT = REPO_ROOT / "data" / "generated-manifest.json"
MD_OUT = REPO_ROOT / "GENERATED.md"


def _latest_report(pattern: str, _fallback: str) -> str:
    try:
        return rel(latest_source_report(pattern))
    except FileNotFoundError:
        raise FileNotFoundError(
            f"build_generated_manifest: no report matches {pattern!r}; refusing a stale fallback link"
        ) from None


def _latest_subdir_manifest(prefix: str, fallback: str) -> str:
    try:
        latest = latest_source_subdir_file(prefix, "manifest.json")
    except FileNotFoundError:
        return fallback
    return rel(latest)


def _latest_subdir_pngs(prefix: str, fallback: str) -> str:
    try:
        latest = latest_source_subdir_file(prefix, "manifest.json")
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
        "name": "Paper folder doc regeneration",
        "outputs": [
            "papers/generated-documents.json",
            "papers/*/README.md",
            "papers/*/AGENTS.md",
            "papers/*/SKILL.md",
        ],
        "sources": [
            "papers/paper_metadata.json",
            "pages/BIBLIOGRAPHY.md",
            "papers/*/metadata.json",
            "papers/generated-documents.json",
        ],
        "command": "uv run python3 code/orchestrators/regenerate_docs.py --apply",
    },
    {
        "name": "Paper CFF DOI-role synchronization",
        "outputs": [
            "papers/*/CITATION.cff (canonical top-level DOI/URL and explicit artifact identifiers)",
        ],
        "sources": [
            "papers/*/metadata.json (doi and optional artifact_doi)",
            "papers/*/CITATION.cff (non-DOI fields and identifiers)",
            "code/orchestrators/generate_citation_cff.py",
        ],
        "command": "uv run python3 code/orchestrators/generate_citation_cff.py --apply",
    },
    {
        "name": "Publications HTML sync",
        "outputs": ["publications.html", "data/publications-ld.json"],
        "sources": [
            "pages/BIBLIOGRAPHY.md",
            "data/current-counts.json",
            "papers/*/README.md",
            "papers/*/AGENTS.md",
            "papers/*/SKILL.md",
            "papers/*/full_text.md",
            "papers/*/images/",
            "code/src/biblio_table.py",
            "code/templates/publications.html.tmpl",
            "code/orchestrators/sync_publications_html.py",
        ],
        "command": "python3 code/orchestrators/sync_publications_html.py --apply",
    },
    {
        "name": "Metadata enrichment",
        "outputs": ["papers/*/metadata.json"],
        "sources": ["papers/paper_metadata.json", "pages/BIBLIOGRAPHY.md"],
        "command": "uv run python3 code/orchestrators/batch_enrich_metadata.py --apply",
    },
    {
        "name": "Metadata quality improvement",
        "outputs": ["papers/*/metadata.json"],
        "sources": ["papers/*/metadata.json"],
        "command": "uv run python3 code/orchestrators/improve_metadata_quality.py --apply",
    },
    {
        "name": "Bibliography exports",
        "outputs": ["bibliography.bib", "bibliography.csl.json", "bibliography.ris", "data/works.json"],
        "sources": [
            "pages/BIBLIOGRAPHY.md",
            "papers/*/README.md",
            "papers/*/AGENTS.md",
            "papers/*/SKILL.md",
            "papers/*/full_text.md",
            "papers/*/images/",
            "code/src/biblio_table.py",
        ],
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
        "sources": [
            "data/scholar-snapshot.json",
            "data/scholar-verification-receipt.json",
            "code/src/scholar_verification.py",
            "code/orchestrators/sync_scholar_metrics.py",
        ],
        "command": "python3 code/orchestrators/sync_scholar_metrics.py",
    },
    {
        "name": "Current count report",
        "outputs": ["reports/current_counts.md", "data/current-counts.json"],
        "sources": [
            "pages/BIBLIOGRAPHY.md",
            "papers/README.md",
            "papers/*/full_text.md",
            "papers/*/images/*",
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
        "name": "Source coverage exceptions",
        "outputs": ["data/coverage-exceptions.json", _latest_report("source_coverage_*.json", "reports/source_coverage_2026-07-17.json"), _latest_report("source_coverage_*.md", "reports/source_coverage_2026-07-17.md")],
        "sources": ["data/works.json", "code/orchestrators/build_coverage_exceptions.py"],
        "command": "python3 code/orchestrators/build_coverage_exceptions.py",
    },
    {
        "name": "Repository classification queue",
        "outputs": ["data/repository-classification.json"],
        "sources": ["data/github-repositories.json", "data/software.json", "data/repository-exclusions.json", "code/orchestrators/classify_repositories.py"],
        "command": "python3 code/orchestrators/classify_repositories.py",
    },
    {
        "name": "Volatile site facts",
        "outputs": ["index.html", "publications.html", "discovery.html", "pages/DISCOVERY.md"],
        "sources": ["data/current-counts.json", "reports/public_source_snapshot_*.json", "code/orchestrators/sync_site_facts.py"],
        "command": "python3 code/orchestrators/sync_site_facts.py",
    },
    {
        "name": "Open Graph preview images",
        "outputs": ["og-*.jpg", "data/og-image-counts.json"],
        "sources": ["data/current-counts.json", "code/orchestrators/generate_og_images.py"],
        "command": "python3 code/orchestrators/generate_og_images.py",
    },
    {
        "name": "Pillar research explainers",
        "outputs": [
            "cognitive-security.html",
            "computational-entomology.html",
            "insect-cognition.html",
            "active-inference.html",
            "neurosymbolic-ai.html",
        ],
        "sources": ["data/works.json", "code/orchestrators/generate_pillar_pages.py"],
        "command": "python3 code/orchestrators/generate_pillar_pages.py",
    },
    {
        "name": "Redirect stubs",
        "outputs": [
            "about.html",
            "agent-verify.html",
            "blog/index.html",
            "blog/winged-snowflake-2021/index.html",
            "meditations.html",
            "nft.html",
            "reports.html",
            "research.html",
        ],
        "sources": ["code/src/redirect_stubs.py", "code/orchestrators/generate_redirect_stubs.py"],
        "command": "python3 code/orchestrators/generate_redirect_stubs.py --apply",
    },
    {
        "name": "Agent data exports",
        "outputs": ["data/software.json", "data/people.json", "data/organizations.json", "data/claims.json"],
        "sources": [
            "pages/SOFTWARE.md",
            "code/src/software_table.py",
            "data/scholar-snapshot.json",
            "data/works.json",
            "data/current-counts.json",
            "papers/",
            "code/orchestrators/export_agent_data.py",
        ],
        "command": "python3 code/orchestrators/export_agent_data.py",
    },
    {
        "name": "Agent route manifest",
        "outputs": ["data/agent-index.json"],
        "sources": [
            "data/current-counts.json",
            "data/pages-artifact-manifest.json",
            "data/github-repositories.json",
            "data/works.json",
            "data/software.json",
            "data/claims.json",
            "data/scholar-verification-receipt.json",
            "reports/*latest dated reports",
            "code/orchestrators/build_agent_index.py",
        ],
        "command": "python3 code/orchestrators/build_agent_index.py",
    },
    {
        "name": "Visible agent navigation",
        "outputs": ["root public HTML navigation"],
        "sources": ["code/src/site_nav.py", "code/orchestrators/ensure_agent_navigation.py"],
        "command": "python3 code/orchestrators/ensure_agent_navigation.py",
    },
    {
        "name": "GitHub Pages artifact",
        "outputs": ["bounded _site/ deployment projection", "data/pages-artifact-manifest.json", _latest_report("pages_artifact_growth_*.json", "reports/pages_artifact_growth_2026-07-17.json")],
        "sources": ["tracked repository files", "code/src/release_controls.py", "code/orchestrators/build_pages_artifact.py", "docs/operations/github-pages-artifact.md"],
        "command": "python3 code/orchestrators/build_pages_artifact.py --write-manifest --output /tmp/docxology-pages --check-size --check-manifest",
    },
    {
        "name": "Release integrity envelope",
        "outputs": ["data/release-integrity.json"],
        "sources": ["data/current-counts.json", "data/agent-index.json", "data/pages-artifact-manifest.json", "code/orchestrators/build_release_integrity.py"],
        "command": "python3 code/orchestrators/build_release_integrity.py",
    },
    {
        "name": "Post-deploy release attestation",
        "outputs": ["reports/deployment-attestations/<deployment-sha>.json"],
        "sources": [
            "reports/public_source_snapshot_*.json",
            "reports/external_links_[0-9]*.json",
            "reports/browser-smoke/*/manifest.json",
            "reports/browser-qa/*/manifest.json",
            "reports/visual-qa/*/manifest.json",
            "reports/live_site_verification_*.json",
            "code/orchestrators/attest_release.py",
        ],
        "command": "python3 code/orchestrators/attest_release.py --apply --commit <deployment-sha>",
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
            "resume/resume.html",
            "resume/verify.html",
        ],
        "sources": [
            "resume/source.json",
            "data/works.json",
            "data/software.json",
            "data/scholar-snapshot.json",
            "data/claims.json",
            "data/github-repositories.json",
            "code/src/resume_data.py",
            "code/orchestrators/build_resume.py",
        ],
        "command": "uv run python3 code/orchestrators/build_resume.py --all",
    },
    {
        "name": "Software catalog HTML sync",
        "outputs": ["software.html", "data/software-ld.json"],
        "sources": [
            "pages/SOFTWARE.md",
            "data/github-repositories.json",
            "code/src/software_table.py",
            "code/templates/software.html.tmpl",
            "code/orchestrators/sync_software_html.py",
        ],
        "command": "python3 code/orchestrators/sync_software_html.py --apply",
    },
    {
        "name": "Full GitHub repository inventory",
        "outputs": ["data/github-repositories.json"],
        "sources": ["GitHub REST API", "data/software.json", "code/orchestrators/build_github_inventory.py"],
        "command": "python3 code/orchestrators/build_github_inventory.py",
    },
    {
        "name": "Cached GitHub repository inventory pages",
        "outputs": ["repositories.html", "repositories-forks.html"],
        "sources": [
            "data/github-repositories.json",
            "code/orchestrators/build_github_inventory.py",
            "code/orchestrators/render_github_inventory.py",
        ],
        "command": "python3 code/orchestrators/render_github_inventory.py",
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
        "name": "Zenodo-only publication backfill",
        "outputs": [
            "pages/BIBLIOGRAPHY.md",
            "papers/<YEAR>_<Slug>/",
            "papers/paper_metadata.json",
            "papers/README.md",
        ],
        "sources": [
            "Zenodo Records API",
            "docs/operations/publication-sync.md",
            "code/orchestrators/add_zenodo_only.py",
        ],
        "command": "python3 code/orchestrators/add_zenodo_only.py <record_id>",
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
        "sources": [
            "data/works.json",
            "data/work-enrichment.json",
            "papers/*/README.md",
            "papers/*/SKILL.md",
        ],
        "command": "python3 code/orchestrators/build_work_pages.py",
    },
    {
        "name": "Work authors",
        "outputs": ["data/work-authors.json"],
        "sources": ["pages/BIBLIOGRAPHY.md", "DOI registration agencies (Crossref/DataCite)", "code/orchestrators/fetch_work_authors.py"],
        "command": "python3 code/orchestrators/fetch_work_authors.py --apply",
    },
    {
        "name": "Video pages",
        "outputs": [
            "videos/*.html",
            "data/videos.json",
            "data/videos-index.json",
            "data/video-pages-manifest.json",
        ],
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
        "name": "Reproducibility ledger",
        "outputs": ["reproducibility.html", "pages/REPRODUCIBILITY.md", "data/reproducibility.json"],
        "sources": ["data/works.json", "papers/paper_metadata.json", "code/orchestrators/build_reproducibility_ledger.py"],
        "command": "python3 code/orchestrators/build_reproducibility_ledger.py",
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
        "sources": ["all root-level public HTML plus site-critical Markdown and JSON-LD surfaces"],
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
        "name": "Public-source review record",
        "outputs": [
            _latest_report("public_source_review_*.json", "reports/public_source_review_2026-05-15.json"),
            _latest_report("public_source_review_*.md", "reports/public_source_review_2026-05-15.md"),
        ],
        "sources": [
            "reports/public_source_snapshot_*.json",
            "reports/public_source_inventory_*.json",
            "reports/paired_publications_*.json",
            "data/paired-publication-decisions.json",
            "data/public-source-observation-decisions.json",
            "data/biographical-claim-decisions.json",
            "data/claims.json",
            "data/scholar-snapshot.json",
            "data/scholar-verification-receipt.json",
            "code/orchestrators/build_public_source_review.py",
        ],
        "command": "python3 code/orchestrators/build_public_source_review.py",
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
        "name": "Progressive browser QA",
        "outputs": [_latest_subdir_manifest("browser-qa", "reports/browser-qa/2026-07-18/manifest.json")],
        "sources": ["root HTML pages", "js/*.js", "style.css", "code/orchestrators/browser_qa.py"],
        "command": "uv run --extra browser-qa python3 code/orchestrators/browser_qa.py",
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
        "name": "Compact artwork gallery index",
        "outputs": ["data/artworks-index.json"],
        "sources": ["data/artworks.json", "code/orchestrators/build_artwork_index.py"],
        "command": "python3 code/orchestrators/build_artwork_index.py",
    },
    {
        "name": "Image sitemap",
        "outputs": ["sitemap-images.xml"],
        "sources": ["data/artworks.json", "art/*", "code/orchestrators/build_image_sitemap.py"],
        "command": "python3 code/orchestrators/build_image_sitemap.py",
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

# Orchestrators that do not produce a matrix artifact row: drivers, auditors,
# network submitters, maintenance tools, and completed one-shot migrations.
# Documented in GENERATED.md so every code/orchestrators/*.py script is
# discoverable from the authoritative matrix. MD-only: data/generated-manifest.json
# keeps its frozen {generated_at, artifacts} schema for downstream consumers.
UTILITIES = [
    ("regenerate_all.py", "Dependency-ordered write-mode rebuild of every locally-derived artifact; `--validate` chains validate_repo.py", "driver"),
    ("validate_repo.py", "Authoritative generated-layer gate: runs every generator in `--check` mode plus repo invariants", "gate"),
    ("build_generated_manifest.py", "Writes GENERATED.md + data/generated-manifest.json from the ARTIFACTS/UTILITIES lists in this file", "meta"),
    ("audit_publication_skills.py", "Validates papers/*/SKILL.md against data/works.json docs_path references; runs in validate_repo.py", "audit"),
    ("build_reconciliation_report.py", "Builds the public-source reconciliation report from local indexes and the freshness snapshot", "audit"),
    ("build_public_source_review.py", "Builds dated applied/deferred/rejected review evidence from refresh snapshots without changing curated claims, metrics, classifications, or bibliography data", "review"),
    ("audit_private_reconciliation.py", "Classifies public-main versus private-only changes without merging history and records source ports, derived regeneration, and binary deferrals", "audit"),
    ("check_zenodo_uncatalogued.py", "Diffs live Zenodo records under the profile ORCID against the curated bibliography", "audit"),
    ("gsc_followup_preflight.py", "Prints the pre-GSC-followup checklist (sitemap, priority URLs, validation rows); see docs/seo/gsc-followup.md", "audit"),
    ("indexnow_urls.py", "Emits the IndexNow URL list from the sitemap index-priority policy", "seo"),
    ("submit_indexnow.py", "Submits index-priority URLs to IndexNow endpoints (Bing, Yandex, Naver)", "seo"),
    ("ensure_social_meta.py", "Idempotently adds Twitter Card + og:image:alt tags to the hand-maintained pages", "maintenance"),
    ("prune_old_reports.py", "Prunes superseded dated QA screenshot sets only with a reviewed provenance-preserving retention manifest", "maintenance"),
    ("reconcile_paper_dois.py", "Builds an approval-bound canonical DOI versus artifact DOI reconciliation receipt; bibliography DOI is canonical", "maintenance"),
    ("attest_release.py", "Creates or checks a content-addressed post-deploy deployment-SHA attestation; never deploys", "release"),
    ("generate_redirect_stubs.py", "Renders or checks all centrally declared redirect stubs without inline JavaScript", "maintenance"),
    ("extract_paper_texts.py", "Extracts full text and images from paper PDFs into the papers/ tree", "maintenance"),
    ("fetch_youtube_data.py", "Fetches YouTube channel metadata for both channels into code/data/youtube_*.json (network)", "fetch"),
    ("generate_citation_cff.py", "Synchronizes canonical citation DOI and labelled artifact DOI roles in per-paper CFF files while preserving non-DOI identifiers", "maintenance"),
    ("render_github_inventory.py", "Renders the primary and fork GitHub inventory pages deterministically from the reviewed cached JSON inventory", "generation"),
    ("deploy_seo_security.py", "Deploys/refreshes the CSP and rel=\"me\" head tags across indexable pages; idempotent and re-run on every rebuild (not a one-shot)", "maintenance"),
    ("migrate_inline_handlers.py", "One-shot migration: inline event handlers to data-* + addEventListener for CSP (completed; kept for provenance)", "one-shot"),
    ("optimize_font_loading.py", "One-shot migration: legacy Google Fonts links to self-hosted loading (completed; kept for provenance)", "one-shot"),
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
            "## Maintenance & Utility Orchestrators",
            "",
            "Scripts under `code/orchestrators/` that do not produce a matrix artifact row:"
            " rebuild drivers, gates, audits, network submitters, and completed one-shot"
            " migrations. Full source-layer map: `code/README.md`.",
            "",
            "| Script | Role | Purpose |",
            "| --- | --- | --- |",
        ]
    )
    for script, purpose, role in UTILITIES:
        lines.append(f"| `code/orchestrators/{script}` | {role} | {purpose} |")
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
    generated_at = _existing_generated_at() or generated_timestamp()
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
