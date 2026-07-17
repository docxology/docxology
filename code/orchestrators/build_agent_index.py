#!/usr/bin/env python3
"""Build the stable machine-readable route manifest for public agents."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "data" / "agent-index.json"
COUNTS = REPO_ROOT / "data" / "current-counts.json"
DATASET_PATHS = {
    "works": "data/works.json",
    "software": "data/software.json",
    "repositories": "data/github-repositories.json",
    "artworks": "data/artworks.json",
    "videos": "data/videos.json",
    "search": "search-index.json",
    "claims": "data/claims.json",
    "coverage_exceptions": "data/coverage-exceptions.json",
    "repository_classification": "data/repository-classification.json",
}


def sha256(path: Path) -> str | None:
    if not path.is_file():
        return None
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(relative: str, default: dict | list | None = None):
    path = REPO_ROOT / relative
    if not path.is_file():
        return {} if default is None else default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {} if default is None else default


def latest_report(pattern: str, fallback: str) -> str:
    matches = sorted((REPO_ROOT / "reports").glob(pattern))
    return "/" + str((matches[-1] if matches else REPO_ROOT / fallback).relative_to(REPO_ROOT))


SCHEMAS = {
    "Work": {
        "type": "object",
        "description": "One curated bibliography row; citation_key is the permanent public URL identifier.",
        "required": ["num", "citation_key", "year", "domain", "domain_name", "type", "title", "url", "doi", "docs_path"],
        "fields": {
            "num": "integer; immutable catalog identity, with retired gaps preserved",
            "citation_key": "string; stable URL and BibTeX key",
            "year": "integer",
            "domain": "string; domain emoji code",
            "domain_name": "string; human-readable domain",
            "type": "string; Paper, Book, Course, Presentation, Playbook, or Series",
            "title": "string",
            "venue": "string",
            "url": "string; canonical external identifier or landing page",
            "doi": "string or empty",
            "docs_path": "string or empty; paper-folder path",
            "has_paper_folder": "boolean",
            "has_full_text": "boolean",
            "has_images": "boolean",
        },
    },
    "SoftwareRepository": {
        "type": "object",
        "description": "One curated software catalog row from pages/SOFTWARE.md.",
        "required": ["name", "url", "owner", "catalog_section", "description", "language", "paper_path", "zenodo_url"],
        "fields": {
            "name": "string",
            "url": "string; GitHub repository URL",
            "owner": "docxology or ActiveInferenceInstitute",
            "catalog_section": "curated source-table section",
            "description": "string",
            "language": "string or empty",
            "stars": "integer or null; API snapshot value",
            "updated_or_year": "string; API snapshot month/year or source year",
            "paper_path": "string or empty",
            "zenodo_url": "string or empty",
        },
    },
    "Repository": {
        "type": "object",
        "description": "One public repository in the complete GitHub inventory, including forks.",
        "required": ["name", "full_name", "owner", "html_url", "fork", "archived", "private", "curated", "recently_updated"],
        "fields": {
            "full_name": "string; owner/name",
            "html_url": "string",
            "owner": "docxology or ActiveInferenceInstitute",
            "fork": "boolean",
            "archived": "boolean",
            "private": "boolean",
            "curated": "boolean; present in the curated software catalog",
            "recently_updated": "boolean; current inventory freshness flag",
            "created_at": "ISO-8601 timestamp",
            "updated_at": "ISO-8601 timestamp",
            "pushed_at": "ISO-8601 timestamp or null",
        },
    },
    "ClaimWithEvidence": {
        "type": "object",
        "description": "One claim ledger entry with dated verification and explicit caveat handling.",
        "required": ["id", "claim", "status", "sources", "checked_at", "confidence", "verification_method", "caveat"],
        "fields": {
            "id": "stable claim identifier",
            "claim": "string",
            "status": "curated-local, public-api, dated-snapshot, public-profile, or related evidence status",
            "sources": "array of URLs or repository-relative paths",
            "checked_at": "ISO date or timestamp",
            "confidence": "high, medium, or low",
            "verification_method": "string",
            "maintenance_owner": "role responsible for refresh",
            "caveat": "string; do not silently omit uncertainty",
        },
    },
    "SearchResult": {
        "type": "object",
        "description": "One lexical search-index item spanning pages, works, software, repositories, people, organizations, and claims.",
        "required": ["id", "type", "title", "url", "summary", "tags", "content"],
        "fields": {
            "id": "stable type-prefixed identifier",
            "type": "page, work, software, repository, person, organization, claim, or report",
            "title": "string",
            "url": "root-relative public URL",
            "summary": "short human-readable description",
            "tags": "array of strings",
            "content": "normalized search text",
        },
    },
    "GeneratedReport": {
        "type": "object",
        "description": "A dated generated QA, freshness, reconciliation, or deployment report.",
        "required": ["generated_at"],
        "fields": {
            "generated_at": "ISO-8601 generation timestamp",
            "checked_at": "ISO date or timestamp when an external source was checked, when applicable",
            "overall_ok": "boolean for reports that aggregate checks",
            "results": "array of check-specific objects for QA/deployment reports",
            "facts": "object of normalized source facts for public-source snapshots",
        },
    },
    "CoverageException": {
        "type": "object",
        "description": "One explicit bibliography coverage gap with a legitimacy/review status.",
        "required": ["citation_key", "title", "type", "reasons", "review_status"],
        "fields": {
            "citation_key": "string; permanent work identifier",
            "title": "string",
            "type": "string",
            "reasons": "array; no_paper_folder, no_full_text, no_doi, no_canonical_url, or non_paper_record",
            "review_status": "legitimate_gap or needs_review",
        },
    },
    "RepositoryClassification": {
        "type": "object",
        "description": "Review queue row for a public repository outside the curated software catalog.",
        "required": ["full_name", "owner", "html_url", "fork", "archived", "catalog_role", "exclusion_reason", "review_status"],
        "fields": {
            "full_name": "string; owner/name",
            "owner": "string",
            "html_url": "https URL",
            "fork": "boolean",
            "archived": "boolean",
            "catalog_role": "not_curated until manually reviewed",
            "exclusion_reason": "fork_not_curated or primary_repo_requires_manual_review",
            "review_status": "defer, accept, reject, or supersede",
        },
    },
    "PagesArtifactManifest": {
        "type": "object",
        "description": "Bounded GitHub Pages projection file list, byte budget, omitted-image policy, and GitHub fallback templates.",
        "required": ["schema_version", "source_commit_at_generation", "github_fallback", "budget", "included_files", "omitted_paper_images"],
        "fields": {
            "source_commit_at_generation": "Git commit used when the artifact was measured",
            "github_fallback": "tree/raw URL templates",
            "budget": "hard limit, safety ceiling, warning, file count, and byte totals",
            "included_files": "array of included path/size/hash records",
            "omitted_paper_images": "count and fallback-preserving policy summary",
        },
    },
    "ReleaseIntegrity": {
        "type": "object",
        "description": "Source-to-release integrity envelope connecting hashes, generators, Pages, deployment, and live verification.",
        "required": ["schema_version", "source_sha256", "generator", "pages_artifact", "deployment", "privacy"],
        "fields": {
            "source_sha256": "map of source/generated input paths to SHA-256",
            "generator": "ordered pipeline and generator hashes",
            "pages_artifact": "bounded artifact manifest summary",
            "deployment": "workflow/deployment and live verification metadata",
            "privacy": "CV public-integrity result and policy",
        },
    },
}


def payload() -> dict:
    current = json.loads(COUNTS.read_text(encoding="utf-8"))
    counts = current.get("counts", {})
    artworks = load_json("data/artworks.json")
    videos = load_json("data/videos.json")
    works = load_json("data/works.json")
    software = load_json("data/software.json")
    repositories = load_json("data/github-repositories.json")
    claims = load_json("data/claims.json")
    search = load_json("search-index.json")
    coverage = load_json("data/coverage-exceptions.json")
    classification = load_json("data/repository-classification.json")
    pages_artifact = load_json("data/pages-artifact-manifest.json")
    live_report_path = latest_report("live_site_verification_*.json", "reports/live_site_verification_2026-05-15.json")
    live_report = load_json(live_report_path.lstrip("/"))
    dataset_hashes = {key: sha256(REPO_ROOT / path) for key, path in DATASET_PATHS.items() if (REPO_ROOT / path).is_file()}
    dataset_hashes["current_counts"] = sha256(COUNTS)
    return {
        "schema_version": "1.2",
        "generated_at": current.get("generated_at"),
        "canonical_origin": "https://danielarifriedman.com/",
        "canonical_sources": {
            "bibliography": "/pages/BIBLIOGRAPHY.md",
            "software": "/pages/SOFTWARE.md",
            "claims": "/data/claims.json",
            "counts": "/data/current-counts.json",
            "verification": "/pages/VERIFICATION_LOG.md",
            "backlog": "/TODO.md",
            "coverage_exceptions": "/data/coverage-exceptions.json",
            "repository_classification": "/data/repository-classification.json",
            "release_integrity": "/data/release-integrity.json",
        },
        "routes": [
            {"id": "home", "path": "/", "format": "text/html", "kind": "profile"},
            {"id": "publications", "path": "/publications.html", "format": "text/html", "kind": "collection"},
            {"id": "works", "path": "/works/", "format": "text/html", "kind": "collection"},
            {"id": "domains", "path": "/domains.html", "format": "text/html", "kind": "taxonomy"},
            {"id": "software", "path": "/software.html", "format": "text/html", "kind": "collection"},
            {"id": "repositories", "path": "/repositories.html", "format": "text/html", "kind": "collection"},
            {"id": "art", "path": "/art.html", "format": "text/html", "kind": "collection"},
            {"id": "videos", "path": "/videos.html", "format": "text/html", "kind": "collection"},
            {"id": "search", "path": "/search.html", "format": "text/html", "kind": "query", "query": "?q={terms}"},
            {"id": "discovery", "path": "/discovery.html", "format": "text/html", "kind": "source-map"},
            {"id": "catalog", "path": "/catalog.html", "format": "text/html", "kind": "data-catalog"},
            {"id": "exports", "path": "/exports.html", "format": "text/html", "kind": "export-hub"},
            {"id": "evidence", "path": "/evidence.html", "format": "text/html", "kind": "evidence-ledger"},
            {"id": "updates", "path": "/updates.html", "format": "text/html", "kind": "changelog"},
            {"id": "cv", "path": "/resume/resume.html", "format": "text/html", "kind": "accessible-cv"},
            {"id": "agent-index", "path": "/data/agent-index.json", "format": "application/json", "kind": "route-manifest"},
        ],
        "datasets": {
            "works": {"path": "/data/works.json", "count": counts.get("bibliography_works"), "schema": "Work"},
            "software": {"path": "/data/software.json", "count": counts.get("software", {}).get("curated_total"), "schema": "SoftwareRepository"},
            "repositories": {"path": "/data/github-repositories.json", "count": counts.get("github_inventory", {}).get("total"), "schema": "Repository"},
            "artworks": {"path": "/data/artworks.json", "count": artworks.get("count", len(artworks.get("artworks", []))), "schema": "VisualArtwork"},
            "videos": {"path": "/data/videos.json", "count": videos.get("count", len(videos.get("videos", []))), "schema": "VideoObject"},
            "search": {"path": "/search-index.json", "count": None, "schema": "SearchResult"},
            "claims": {"path": "/data/claims.json", "count": None, "schema": "ClaimWithEvidence"},
            "coverage_exceptions": {"path": "/data/coverage-exceptions.json", "count": len(coverage.get("exceptions", [])), "schema": "CoverageException"},
            "repository_classification": {"path": "/data/repository-classification.json", "count": len(classification.get("repositories", [])), "schema": "RepositoryClassification"},
            "pages_artifact": {"path": "/data/pages-artifact-manifest.json", "count": None, "schema": "PagesArtifactManifest"},
            "release_integrity": {"path": "/data/release-integrity.json", "count": None, "schema": "ReleaseIntegrity"},
        },
        "reports": [
            {"id": "current-counts", "path": "/data/current-counts.json", "format": "application/json", "schema": "GeneratedReport", "freshness_field": "generated_at"},
            {"id": "public-source-snapshot", "path": latest_report("public_source_snapshot_*.json", "reports/public_source_snapshot_2026-05-15.json"), "format": "application/json", "schema": "GeneratedReport", "freshness_field": "generated_at"},
            {"id": "public-source-inventory", "path": latest_report("public_source_inventory_*.json", "reports/public_source_inventory_2026-05-15.json"), "format": "application/json", "schema": "GeneratedReport", "freshness_field": "generated_at"},
            {"id": "paired-publications", "path": latest_report("paired_publications_*.json", "reports/paired_publications_2026-05-15.json"), "format": "application/json", "schema": "GeneratedReport", "freshness_field": "generated_at"},
            {"id": "accessibility", "path": latest_report("accessibility_static_*.json", "reports/accessibility_static_2026-05-15.json"), "format": "application/json", "schema": "GeneratedReport", "freshness_field": "generated_at"},
            {"id": "asset-size", "path": latest_report("asset_size_*.json", "reports/asset_size_2026-05-15.json"), "format": "application/json", "schema": "GeneratedReport", "freshness_field": "generated_at"},
            {"id": "live-site", "path": latest_report("live_site_verification_*.json", "reports/live_site_verification_2026-05-15.json"), "format": "application/json", "schema": "GeneratedReport", "freshness_field": "generated_at"},
        ],
        "schemas": SCHEMAS,
        "schema_registry_version": "1.0",
        "schema_examples": {
            "Work": works.get("works", [])[:1],
            "SoftwareRepository": software.get("repositories", [])[:1],
            "Repository": repositories.get("repositories", [])[:1],
            "ClaimWithEvidence": claims.get("claims", [])[:1],
            "SearchResult": search.get("items", [])[:1],
            "CoverageException": coverage.get("exceptions", [])[:1],
            "RepositoryClassification": classification.get("repositories", [])[:1],
            "GeneratedReport": current,
            "PagesArtifactManifest": {"schema_version": pages_artifact.get("schema_version"), "budget": pages_artifact.get("budget"), "github_fallback": pages_artifact.get("github_fallback")},
            "ReleaseIntegrity": {"schema_version": "1.0", "note": "See /data/release-integrity.json for the current envelope."},
        },
        "dataset_hashes": dataset_hashes,
        "source_provenance": {
            "generated_by": "code/orchestrators/build_agent_index.py",
            "source_of_truth": ["pages/BIBLIOGRAPHY.md", "pages/SOFTWARE.md", "data/current-counts.json"],
            "hash_policy": "SHA-256 values cover hosted JSON datasets and integrity manifests at generation time.",
        },
        "hosted_availability": {
            "pages_origin": "https://danielarifriedman.com/",
            "github_repository": "https://github.com/docxology/docxology",
            "artifact_manifest": "/data/pages-artifact-manifest.json",
            "paper_image_fallback": "Use the Pages artifact manifest GitHub tree/raw templates for omitted extracted paper images.",
        },
        "verification_status": {
            "live_report": live_report_path,
            "generated_at": live_report.get("generated_at"),
            "overall_ok": live_report.get("overall_ok"),
            "passing": live_report.get("passing"),
            "checked_urls": live_report.get("checked_urls"),
            "pages_status": live_report.get("github_pages", {}).get("status"),
        },
        "counts": counts,
        "freshness": {
            "policy": "Use generated_at and checked_at fields; do not infer freshness from page copy.",
            "volatile_sources": ["data/current-counts.json", "data/scholar-snapshot.json", "data/verification-log.json"],
            "verification": "/cite-verify.html",
        },
        "query_recipes": {
            "site_search": "/search.html?q={urlencoded_terms}",
            "publication_filter": "/publications.html?domain={emoji}&type={type}&year={year}",
            "work_by_key": "/works/{citation_key}.html",
            "raw_bibliography": "/pages/BIBLIOGRAPHY.md",
            "repository_by_full_name": "/repositories.html?repo={owner}/{name}",
            "claim_by_id": "/data/claims.json#id={claim_id}",
            "reports": "/data/agent-index.json#reports",
            "coverage_exceptions": "/data/coverage-exceptions.json",
            "repository_classification": "/data/repository-classification.json",
            "release_integrity": "/data/release-integrity.json",
        },
        "notes": [
            "Canonical work URLs use citation_key values and preserve retired numeric gaps.",
            "Paper-folder pages are documentation mirrors; canonical indexable work pages live under /works/.",
            "External facts and metrics are evidence-dated; retain caveats when primary verification is incomplete.",
            "Pages omits duplicated paper-extracted image binaries only; use the manifest fallback templates for GitHub retrieval.",
            "Coverage exceptions and repository classifications are review queues, not automatic certification or rejection.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the manifest is stale")
    args = parser.parse_args()
    rendered = json.dumps(payload(), indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"stale agent manifest: {OUT.relative_to(REPO_ROOT)}")
        print(f"checked {OUT.relative_to(REPO_ROOT)}")
        return
    OUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
