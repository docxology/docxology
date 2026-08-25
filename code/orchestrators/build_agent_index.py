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
    "artworks_index": "data/artworks-index.json",
    "artworks": "data/artworks.json",
    "videos": "data/videos.json",
    "videos_index": "data/videos-index.json",
    "search": "search-index.json",
    "claims": "data/claims.json",
    "scholar_verification_receipt": "data/scholar-verification-receipt.json",
    "coverage_exceptions": "data/coverage-exceptions.json",
    "repository_classification": "data/repository-classification.json",
    "people": "data/people.json",
    "organizations": "data/organizations.json",
    "resume": "data/resume.json",
    "work_enrichment": "data/work-enrichment.json",
    "catalog": "data/catalog.json",
    "reconciliation": "data/reconciliation.json",
    "generated_manifest": "data/generated-manifest.json",
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


def latest_report(pattern: str, _fallback: str) -> str:
    matches = sorted((REPO_ROOT / "reports").glob(pattern))
    if not matches:
        raise FileNotFoundError(
            f"build_agent_index: no report matches {pattern!r}; refusing a stale fallback link"
        )
    return "/" + str(matches[-1].relative_to(REPO_ROOT))


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
            "has_skill_md": "boolean; a per-paper agent SKILL.md exists in the folder",
            "has_agents_md": "boolean; a per-paper AGENTS.md exists in the folder",
            "has_readme": "boolean; a per-paper README.md exists in the folder",
            "full_text_url": "string or empty; site-relative URL of the paper's full_text.md",
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
    "ArtworkIndex": {
        "type": "object",
        "description": "Compact artwork grid/search projection; full resolution and media details live in VisualArtwork.",
        "required": ["id", "title", "tags", "date", "views", "thumb"],
        "fields": {
            "id": "string; stable Flickr artwork identifier",
            "title": "string",
            "tags": "array of strings",
            "date": "string or empty",
            "views": "string or numeric display count",
            "thumb": "HTTPS thumbnail URL",
        },
    },
    "VideoIndex": {
        "type": "object",
        "description": "Compact video timeline projection; complete topic, relationship, and transcript metadata lives in VideoObject.",
        "required": ["schema_version", "generated_at", "source", "count", "counts", "channels", "fields", "detail_source", "videos"],
        "fields": {
            "schema_version": "VideoIndex.v1",
            "generated_at": "ISO-8601 generation timestamp",
            "source": "data/videos.json",
            "count": "integer",
            "counts": "channel totals and transcript count",
            "channels": "channel freshness metadata",
            "fields": "ordered compact video fields",
            "detail_source": "complete VideoObject export",
            "videos": "array of compact timeline records",
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
    "ScholarVerificationReceipt": {
        "type": "object",
        "description": "A direct-authenticated verification assertion bound by SHA-256 to the canonical dated Scholar snapshot.",
        "required": ["schema_version", "receipt_type", "profile_id", "direct", "authenticated", "verified_at", "snapshot_path", "snapshot_sha256", "snapshot_as_of", "metrics", "source", "method"],
        "fields": {
            "receipt_type": "google_scholar_direct_authenticated",
            "profile_id": "string; canonical Google Scholar profile identifier",
            "direct": "boolean; must be true",
            "authenticated": "boolean; must be true",
            "verified_at": "timezone-qualified ISO-8601 timestamp of the recorded direct observation",
            "snapshot_path": "data/scholar-snapshot.json",
            "snapshot_sha256": "SHA-256 of the exact canonical snapshot bytes",
            "snapshot_as_of": "dated snapshot value",
            "metrics": "object with non-negative citations, h_index, and i10_index",
            "source": "provenance note for the recorded observation",
            "method": "direct-authenticated verification method; not an implied new fetch",
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
        "description": "Review queue row for a public repository outside the curated software catalog, including description-quality triage.",
        "required": ["full_name", "name", "owner", "html_url", "fork", "archived", "private", "description", "description_quality", "catalog_role", "exclusion_reason", "review_status"],
        "fields": {
            "full_name": "string; owner/name",
            "name": "string; repository name",
            "owner": "string",
            "html_url": "https URL",
            "fork": "boolean",
            "archived": "boolean",
            "private": "boolean; inventory privacy state",
            "description": "string; current GitHub description or empty",
            "description_quality": "missing, short, or substantive; triage signal only",
            "language": "string or empty",
            "topics": "array of GitHub topics",
            "recently_updated": "boolean; current inventory freshness flag",
            "relevance": "unknown until manual review",
            "catalog_role": "not_curated, or acknowledged_not_curated for deliberate exclusions",
            "exclusion_reason": "fork_not_curated, primary_repo_requires_manual_review, or acknowledged_not_catalogued",
            "review_status": "defer, acknowledged, accept, reject, or supersede",
            "acknowledged_reason": "present when review_status is acknowledged; one of profile_repo, profile_infrastructure, test_repo, website, rename_duplicate, private_mirror (see data/repository-exclusions.json)",
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
            "deployment": "workflow/deployment and live verification metadata, including current source commit and explicit deployment_pending reasons",
            "privacy": "CV public-integrity result and policy",
        },
    },
    "VisualArtwork": {
        "type": "object",
        "description": "One complete gallery artwork record (pen-and-ink or blockchain art); the full counterpart to the compact ArtworkIndex projection. Aligns with schema.org VisualArtwork.",
        "schema_org": "https://schema.org/VisualArtwork",
        "required": ["id", "title", "tags", "date", "views", "media", "thumb", "flickr_url", "sizes"],
        "fields": {
            "id": "string; stable Flickr artwork identifier",
            "title": "string",
            "desc": "string; artwork description or empty",
            "tags": "array of strings",
            "date": "string or empty",
            "views": "string or numeric display count",
            "media": "string; medium/format label",
            "thumb": "HTTPS thumbnail URL",
            "flickr_url": "HTTPS canonical Flickr page URL",
            "sizes": "object; resolution label to HTTPS image URL map",
        },
    },
    "VideoObject": {
        "type": "object",
        "description": "One complete video record; the full counterpart to the compact VideoIndex projection. Aligns with schema.org VideoObject.",
        "schema_org": "https://schema.org/VideoObject",
        "required": ["id", "title", "channel", "upload_date", "youtube_url", "embed_url", "page_url"],
        "fields": {
            "id": "string; YouTube video identifier",
            "title": "string",
            "channel": "string; channel slug",
            "channel_name": "string",
            "channel_url": "HTTPS channel URL",
            "upload_date": "ISO-8601 date",
            "year": "integer",
            "duration": "duration in seconds or ISO-8601",
            "duration_text": "human-readable duration",
            "view_count": "integer or display string",
            "youtube_url": "HTTPS watch URL",
            "embed_url": "HTTPS embeddable player URL",
            "thumbnail_url": "HTTPS thumbnail URL",
            "page_url": "HTTPS canonical on-site video page",
            "transcript_available": "boolean",
            "transcript_path": "string or empty; repository-relative transcript",
            "topics": "array of strings",
            "related_pages": "array; on-site related page URLs",
            "related_works": "array; related work citation_keys",
        },
    },
    "Person": {
        "type": "object",
        "description": "One collaborator or identity record. Aligns with schema.org Person.",
        "schema_org": "https://schema.org/Person",
        "required": ["name", "role"],
        "fields": {
            "name": "string",
            "role": "string; relationship or contribution role",
            "orcid": "string or empty; ORCID URL",
            "wikidata": "string or empty; Wikidata QID URL",
            "homepage": "string or empty",
            "github": "string or empty; GitHub profile URL",
        },
    },
    "Organization": {
        "type": "object",
        "description": "One institutional affiliation record. Aligns with schema.org Organization.",
        "schema_org": "https://schema.org/Organization",
        "required": ["name", "role"],
        "fields": {
            "name": "string",
            "alternate_names": "array of strings",
            "url": "string; canonical URL",
            "public_landing_page": "string or empty",
            "wikidata": "string or empty; Wikidata QID URL",
            "github": "string or empty; GitHub account URL",
            "github_account_type": "User or Organization",
            "ein": "string or empty; US tax identifier",
            "irs_status": "string or empty",
            "role": "string; affiliation role",
        },
    },
    "ResumeData": {
        "type": "object",
        "description": "Structured CV: profile, contact, metrics, and dated education/experience/awards/service sections with per-variant selection.",
        "required": ["profile", "education", "experience"],
        "fields": {
            "profile": "object; name, title, and summary",
            "contact": "object; email and public links",
            "metrics": "object; citation and output counts",
            "education": "array of degree records",
            "experience": "array of role records",
            "awards": "array",
            "service": "array",
            "works": "array; selected work references",
            "software": "array; selected software references",
            "variants": "object; named CV variant section selections",
        },
    },
    "WorkEnrichment": {
        "type": "object",
        "description": "Abstracts and keywords extracted from paper folders, keyed to Work citation identifiers.",
        "required": ["generated_at", "source", "count", "works"],
        "fields": {
            "generated_at": "ISO-8601 timestamp",
            "source": "string; extraction source",
            "count": "integer",
            "works": "array or object; per-work abstract and keyword enrichment",
        },
    },
    "DataCatalog": {
        "type": "object",
        "description": "Schema.org DataCatalog describing every public JSON export as a Dataset with a DataDownload distribution.",
        "schema_org": "https://schema.org/DataCatalog",
        "required": ["@context", "@type", "name", "dataset"],
        "fields": {
            "@type": "DataCatalog",
            "name": "string",
            "url": "string",
            "dataset": "array of schema.org Dataset nodes, each with url, encodingFormat, license, and distribution",
        },
    },
    "ReconciliationReport": {
        "type": "object",
        "description": "Curated local counts compared against public-source indexes (ORCID, PubMed, Crossref, Zenodo, GitHub), with an explicit relationship interpretation per comparison.",
        "required": ["generated_at", "comparisons"],
        "fields": {
            "generated_at": "ISO-8601 timestamp",
            "snapshot": "string; public-source snapshot report path",
            "claims_count": "integer",
            "comparisons": "array; each has name, local_value, public_value, relationship, and interpretation",
        },
    },
    "GeneratedManifest": {
        "type": "object",
        "description": "Source-to-output rebuild map: every generated artifact with the sources it derives from and the command that produces it.",
        "required": ["generated_at", "artifacts"],
        "fields": {
            "generated_at": "ISO-8601 timestamp",
            "artifacts": "array; each has name, outputs, sources, and command",
        },
    },
}


def payload() -> dict:
    current = json.loads(COUNTS.read_text(encoding="utf-8"))
    counts = current.get("counts", {})
    artworks = load_json("data/artworks.json")
    artworks_index = load_json("data/artworks-index.json")
    videos = load_json("data/videos.json")
    videos_index = load_json("data/videos-index.json")
    works = load_json("data/works.json")
    software = load_json("data/software.json")
    repositories = load_json("data/github-repositories.json")
    claims = load_json("data/claims.json")
    scholar_receipt = load_json("data/scholar-verification-receipt.json")
    search = load_json("search-index.json")
    coverage = load_json("data/coverage-exceptions.json")
    classification = load_json("data/repository-classification.json")
    people = load_json("data/people.json")
    organizations = load_json("data/organizations.json")
    work_enrichment = load_json("data/work-enrichment.json")
    catalog = load_json("data/catalog.json")
    reconciliation = load_json("data/reconciliation.json")
    generated_manifest = load_json("data/generated-manifest.json")
    pages_artifact = load_json("data/pages-artifact-manifest.json")
    live_report_path = latest_report("live_site_verification_*.json", "reports/live_site_verification_2026-05-15.json")
    live_report = load_json(live_report_path.lstrip("/"))
    dataset_hashes = {key: sha256(REPO_ROOT / path) for key, path in DATASET_PATHS.items() if (REPO_ROOT / path).is_file()}
    dataset_hashes["current_counts"] = sha256(COUNTS)
    return {
        "schema_version": "1.5",
        "generated_at": current.get("generated_at"),
        "canonical_origin": "https://danielarifriedman.com/",
        "canonical_sources": {
            "bibliography": "/pages/BIBLIOGRAPHY.md",
            "software": "/pages/SOFTWARE.md",
            "claims": "/data/claims.json",
            "scholar_verification_receipt": "/data/scholar-verification-receipt.json",
            "counts": "/data/current-counts.json",
            "verification": "/pages/VERIFICATION_LOG.md",
            "backlog": "/TODO.md",
            "coverage_exceptions": "/data/coverage-exceptions.json",
            "repository_classification": "/data/repository-classification.json",
            "repository_exclusions": "/data/repository-exclusions.json",
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
            "artworks_index": {"path": "/data/artworks-index.json", "count": artworks_index.get("count", len(artworks_index.get("artworks", []))), "schema": "ArtworkIndex"},
            "videos": {"path": "/data/videos.json", "count": videos.get("count", len(videos.get("videos", []))), "schema": "VideoObject"},
            "videos_index": {"path": "/data/videos-index.json", "count": videos_index.get("count", len(videos_index.get("videos", []))), "schema": "VideoIndex"},
            "search": {"path": "/search-index.json", "count": None, "schema": "SearchResult"},
            "claims": {"path": "/data/claims.json", "count": None, "schema": "ClaimWithEvidence"},
            "scholar_verification_receipt": {"path": "/data/scholar-verification-receipt.json", "count": None, "schema": "ScholarVerificationReceipt"},
            "coverage_exceptions": {"path": "/data/coverage-exceptions.json", "count": len(coverage.get("exceptions", [])), "schema": "CoverageException"},
            "repository_classification": {"path": "/data/repository-classification.json", "count": len(classification.get("repositories", [])), "schema": "RepositoryClassification"},
            "pages_artifact": {"path": "/data/pages-artifact-manifest.json", "count": None, "schema": "PagesArtifactManifest"},
            "release_integrity": {"path": "/data/release-integrity.json", "count": None, "schema": "ReleaseIntegrity"},
            "people": {"path": "/data/people.json", "count": len(people.get("people", [])), "schema": "Person"},
            "organizations": {"path": "/data/organizations.json", "count": len(organizations.get("organizations", [])), "schema": "Organization"},
            "resume": {"path": "/data/resume.json", "count": None, "schema": "ResumeData"},
            "work_enrichment": {"path": "/data/work-enrichment.json", "count": work_enrichment.get("count"), "schema": "WorkEnrichment"},
            "catalog": {"path": "/data/catalog.json", "count": len(catalog.get("dataset", [])), "schema": "DataCatalog"},
            "reconciliation": {"path": "/data/reconciliation.json", "count": len(reconciliation.get("comparisons", [])), "schema": "ReconciliationReport"},
            "generated_manifest": {"path": "/data/generated-manifest.json", "count": len(generated_manifest.get("artifacts", [])), "schema": "GeneratedManifest"},
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
        "schema_registry_version": "1.3",
        "schema_examples": {
            "Work": works.get("works", [])[:1],
            "SoftwareRepository": software.get("repositories", [])[:1],
            "ArtworkIndex": artworks_index.get("artworks", [])[:1],
            "VideoIndex": {
                **{key: videos_index.get(key) for key in ("schema_version", "generated_at", "source", "count", "counts", "channels", "fields", "detail_source")},
                "videos": videos_index.get("videos", [])[:1],
            },
            "Repository": repositories.get("repositories", [])[:1],
            "ClaimWithEvidence": claims.get("claims", [])[:1],
            "ScholarVerificationReceipt": scholar_receipt,
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
            "source_of_truth": ["pages/BIBLIOGRAPHY.md", "pages/SOFTWARE.md", "data/current-counts.json", "data/scholar-snapshot.json", "data/scholar-verification-receipt.json"],
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
            "volatile_sources": ["data/current-counts.json", "data/scholar-snapshot.json", "data/scholar-verification-receipt.json", "data/verification-log.json"],
            "verification": "/cite-verify.html",
        },
        "query_recipes": {
            "site_search": "/search.html?q={urlencoded_terms}",
            "publication_filter": "/publications.html?domain={emoji}&type={type}&year={year}",
            "work_by_key": "/works/{citation_key}.html",
            "raw_bibliography": "/pages/BIBLIOGRAPHY.md",
            "repository_by_full_name": "/repositories.html?repo={owner}/{name}",
            "claim_by_id": "/data/claims.json#id={claim_id}",
            "scholar_verification_receipt": "/data/scholar-verification-receipt.json",
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
