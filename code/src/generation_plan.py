"""Single source of truth for local generation and exact-check coverage.

The release pipeline used to have a write list in ``regenerate_all.py`` and a
separate, hand-maintained check list in ``validate_repo.py``.  They inevitably
drifted.  This module declares every local deterministic step once; both
drivers consume it, and the coverage check rejects a writer without a matching
no-write verification command.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GenerationStep:
    """A deterministic local writer and the exact check for its outputs.

    ``inputs`` optionally declares the step's source-of-truth glob patterns
    (relative to the repository root).  Only curated/upstream files the step
    *reads* may be declared — never the step's own outputs — so a write-mode
    driver can safely skip the step when no declared input changed.  Steps
    without ``inputs`` always run.
    """

    identifier: str
    script: str
    write_args: tuple[str, ...]
    check_args: tuple[str, ...]
    description: str
    inputs: tuple[str, ...] = ()
    inputs_exclude: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExcludedOperation:
    """An intentionally non-automatic operation and its release boundary."""

    script: str
    category: str
    reason: str


# Ordered writer chain. Repeated audit/fact steps are deliberately explicit:
# later generators consume their dated reports, so the second pass verifies the
# final dependency state rather than a one-step-behind report pointer.
# Input globs for the audited public surfaces. These mirror the audit
# generators' own scan scope (audit_assets.PATTERNS / accessibility_audit's
# public-HTML sweep), so a write-mode driver may skip an audit when none of the
# surfaces it audits changed. They are upstream chain outputs, not the audits'
# own reports — declaring them is what keeps the audit pair skippable while the
# dependency-ordered chain keeps the inputs fresh.
ASSET_AUDIT_INPUTS: tuple[str, ...] = (
    "*.html",
    "og-*.jpg",
    "data/*.json",
    "resume/*.txt",
    "resume/*.pdf",
    "bibliography.*",
    "sw.js",
    "manifest.json",
    "style.css",
    "assets/hero-art/*.webp",
)

# The audit generator itself excludes these post-audit control files from its
# budget (audit_assets.EXCLUDED_ASSETS) because the chain's integrity tail
# writes them *after* the audits record their fingerprints — counting them as
# inputs would make the audit steps never converge to a skip.
ASSET_AUDIT_INPUTS_EXCLUDE: tuple[str, ...] = (
    "data/agent-index.json",
    "data/generated-manifest.json",
    "data/pages-artifact-manifest.json",
    "data/release-integrity.json",
)

LOCAL_GENERATION_STEPS: tuple[GenerationStep, ...] = (
    # Bibliography table -> citation exports + works.json (pure renderer).
    GenerationStep("export-bibliography", "export_bibliography.py", (), ("--check",), "Bibliography exports and works projection", ("pages/BIBLIOGRAPHY.md",)),
    # Full re-render of publications.html + publications-ld.json from the
    # curated table and template. This first pass may legally read
    # one-step-behind state (current-counts, paper-folder flags); the final
    # instance below declares those inputs so one pass reaches the fixed point.
    GenerationStep("sync-publications", "sync_publications_html.py", ("--apply",), ("--check",), "Publication HTML and JSON-LD", ("pages/BIBLIOGRAPHY.md", "code/templates/publications.html.tmpl")),
    GenerationStep("sync-software", "sync_software_html.py", ("--apply",), ("--check",), "Software HTML and JSON-LD", ("pages/SOFTWARE.md", "code/templates/software.html.tmpl", "data/github-repositories.json")),
    GenerationStep("github-inventory-pages", "render_github_inventory.py", (), ("--check",), "Cached GitHub inventory HTML pages", ("data/github-repositories.json",)),
    # DERIVED (always-run): reads data/software.json — a projection agent-data
    # rewrites later in the same pass — while agent-data itself reads this
    # step's current-counts.json. That cross-pass cycle cannot be ordered
    # away, so gating here would mask the software.json refresh behind an
    # unchanged-inputs skip.
    GenerationStep("current-counts", "build_current_counts.py", (), ("--check",), "Volatile count report"),
    GenerationStep("coverage-exceptions", "build_coverage_exceptions.py", (), ("--check",), "Source coverage queue", ("data/works.json",)),
    # DERIVED (always-run): classifies from data/software.json, which
    # agent-data rewrites later in the same pass (same cross-pass cycle as
    # current-counts above).
    GenerationStep("repository-classification", "classify_repositories.py", (), ("--check",), "Repository review queue"),
    # DERIVED (always-run): in-place patcher — README.md, pages/*.md,
    # index.html, publications.html, and llms.txt are simultaneously the
    # surfaces it reads and the ones it rewrites, several hand-authored.
    GenerationStep("scholar-metrics", "sync_scholar_metrics.py", (), ("--check",), "Snapshot-backed Scholar surfaces"),
    GenerationStep("og-images", "generate_og_images.py", (), ("--check",), "Open Graph images", ("data/current-counts.json",)),
    # Paper-folder presence (iterdir over papers/) is intentionally undeclared:
    # a new folder always arrives with bibliography/metadata edits, which this
    # input set already covers.
    GenerationStep("agent-data", "export_agent_data.py", (), ("--check",), "Agent data exports", ("pages/SOFTWARE.md", "pages/BIBLIOGRAPHY.md", "data/works.json", "data/scholar-snapshot.json", "data/current-counts.json", "reports/public_source_snapshot_*.json")),
    GenerationStep("resume", "build_resume.py", ("--all",), ("--check",), "Resume/CV exports", ("resume/source.json", "data/works.json", "data/software.json", "data/scholar-snapshot.json", "data/claims.json", "data/github-repositories.json")),
    # DERIVED (always-run): reads data/work-enrichment.json, which work-pages
    # rewrites later in the same pass (documented fixed-point two-pass
    # design); gating on the other inputs would mask enrichment refreshes
    # behind a skip.
    GenerationStep("domain-pages", "build_domain_pages.py", (), ("--check",), "Domain landing pages"),
    # DERIVED (always-run): renders entirely from in-script curated templates;
    # consumes no repository files.
    GenerationStep("pillar-pages", "generate_pillar_pages.py", (), ("--check",), "Shared-rendered pillar pages"),
    GenerationStep("paper-documents", "regenerate_docs.py", ("--apply",), ("--check",), "Manifest-owned paper documentation", ("pages/BIBLIOGRAPHY.md", "papers/paper_metadata.json", "papers/*/metadata.json", "papers/generated-documents.json")),
    # DERIVED (always-run): in-place patcher — rewrites each CITATION.cff's
    # DOI roles while preserving hand-maintained non-DOI fields read from the
    # same file it writes.
    GenerationStep("citation-cff", "generate_citation_cff.py", ("--apply",), ("--check",), "Canonical/artifact DOI roles in paper CFF files"),
    # Paper-document rendering can create the README/AGENTS/SKILL files that
    # bibliography exports classify. Re-export before public work pages so a
    # first clean run reaches a fixed point instead of requiring a second pass.
    GenerationStep("export-bibliography-final", "export_bibliography.py", (), ("--check",), "Bibliography exports after paper documents", ("pages/BIBLIOGRAPHY.md", "papers/*/README.md", "papers/*/AGENTS.md", "papers/*/SKILL.md", "papers/*/full_text.md", "papers/*/images/*")),
    # Final pass adds the paper-documents outputs and current-counts so the
    # fixed point (folder flags + "as of" month) is reached in one pass.
    GenerationStep("sync-publications-final", "sync_publications_html.py", ("--apply",), ("--check",), "Publication HTML and JSON-LD after paper documents", ("pages/BIBLIOGRAPHY.md", "code/templates/publications.html.tmpl", "data/current-counts.json", "papers/*/README.md", "papers/*/AGENTS.md", "papers/*/SKILL.md", "papers/*/full_text.md", "papers/*/images/*")),
    GenerationStep("work-pages", "build_work_pages.py", (), ("--check",), "Per-work landing pages", ("data/works.json", "data/work-enrichment.json", "papers/*/README.md", "papers/*/SKILL.md")),
    GenerationStep("video-pages", "build_video_pages.py", (), ("--check",), "Video landing pages and exports", ("data/works.json", "data/work-enrichment.json", "data/video-transcripts/*.txt", "code/data/youtube_*.json")),
    # DERIVED (always-run): in-place patcher — rewrites volatile counts,
    # dates, and latest-report pointers inside its own seven target surfaces
    # (index/publications/discovery/art/videos pages, DISCOVERY.md, llms.txt),
    # several of which are hand-authored shells.
    GenerationStep("site-facts-first", "sync_site_facts.py", (), ("--check",), "Volatile public facts after content projections"),
    # start-here.html is hand-authored and the step is check-only in the
    # chain, so the page is a genuine upstream input, not an output.
    GenerationStep("start-here", "build_start_here.py", (), ("--check",), "Start Here curated reading paths page", ("start-here.html",)),
    GenerationStep("paper-pages", "build_paper_pages.py", (), ("--check",), "Paper folder HTML pages", ("data/works.json", "papers/*/README.md", "papers/*/*.pdf", "papers/*/images/*")),
    # DERIVED (always-run): renders from the centrally declared stub table in
    # code/src/redirect_stubs.py; consumes no repository files.
    GenerationStep("redirect-stubs", "generate_redirect_stubs.py", ("--apply",), ("--check",), "Centrally rendered legacy redirects"),
    # DERIVED (always-run): idempotent in-place CSP/referrer/rel="me"
    # normalization whose scan scope equals its write scope (every public
    # HTML file).
    GenerationStep("seo-security", "deploy_seo_security.py", (), ("--check",), "Shared public head/security normalization"),
    GenerationStep("exports-page", "build_exports_page.py", (), ("--check",), "Exports hub", ("data/works.json", "data/current-counts.json")),
    GenerationStep("updates-page", "build_updates_page.py", (), ("--check",), "Updates page", ("CHANGELOG.md",)),
    GenerationStep("evidence-page", "build_evidence_page.py", (), ("--check",), "Evidence page", ("data/claims.json", "data/current-counts.json", "reports/public_source_snapshot_*.json", "reports/public_source_inventory_*.json")),
    GenerationStep("reproducibility", "build_reproducibility_ledger.py", (), ("--check",), "Reproducibility ledger", ("data/works.json", "data/software.json")),
    # DERIVED (always-run): idempotent in-place Agent Map nav patch whose
    # scan scope equals its write scope (every public root HTML page).
    GenerationStep("agent-navigation", "ensure_agent_navigation.py", (), ("--check",), "Visible Agent Map navigation"),
    GenerationStep("reconciliation", "build_reconciliation_report.py", (), ("--check",), "Reconciliation report", ("data/works.json", "data/software.json", "data/claims.json", "reports/public_source_snapshot_*.json")),
    GenerationStep("asset-audit-first", "audit_assets.py", (), ("--check",), "Asset-size report", ASSET_AUDIT_INPUTS, ASSET_AUDIT_INPUTS_EXCLUDE),
    GenerationStep("accessibility-first", "accessibility_audit.py", (), ("--check",), "Static accessibility report", ("**/*.html",)),
    # Renders the DataCatalog payload from dataset counts, the per-paper
    # extraction footprint, and latest-report path resolution. Outputs
    # data/catalog.json + catalog.html are release PAYLOAD:
    # release_controls.is_control_path is False for both (control paths are
    # GENERATED.md, the four tail manifests, and the dated asset_size /
    # pages_artifact_growth / public_source_review receipts). The report
    # families are declared for path resolution; because pointer resolution
    # is git-tracked-filtered while fingerprints are content-only, a receipt
    # committed after the last catalog run needs the post-commit pointer
    # re-render or --force (publication-sync.md, discovery-pointer bullet).
    GenerationStep("catalog", "build_catalog.py", (), ("--check",), "Public data catalog", ("data/works.json", "data/software.json", "data/videos.json", "papers/*/full_text.md", "papers/*/images/*", "reports/public_source_inventory_*.json", "reports/public_source_snapshot_*.json", "reports/external_links_[0-9]*.json", "reports/external_links_triage_*.json", "reports/asset_size_*.json", "reports/live_site_verification_*.json", "reports/browser-smoke/*/manifest.json", "reports/browser-qa/*/manifest.json")),
    GenerationStep("asset-audit-final", "audit_assets.py", (), ("--check",), "Final asset-size report after catalog", ASSET_AUDIT_INPUTS, ASSET_AUDIT_INPUTS_EXCLUDE),
    GenerationStep("accessibility-final", "accessibility_audit.py", (), ("--check",), "Final accessibility report after catalog", ("**/*.html",)),
    # DERIVED (always-run): in-place patcher (same class as
    # site-facts-first); this second pass re-binds pointers to the reports
    # written since the first pass (reconciliation, asset/accessibility finals).
    GenerationStep("site-facts-final", "sync_site_facts.py", (), ("--check",), "Final fact links to latest reports"),
    # After the last README rewrite, so the mirror GitHub renders on the repo
    # page carries the final counts and links that resolve from .github/.
    GenerationStep("github-readme", "build_github_readme.py", (), ("--check",), "GitHub-rendered README mirror", ("README.md",)),
    # Renders the site index from the dataset exports, per-paper extraction
    # presence/counts, and latest-report URL resolution. Outputs
    # search-index.json plus the core/content split companions are release
    # PAYLOAD: release_controls.is_control_path is False for all of them.
    # Pointer families carry the same git-trackedness boundary noted on the
    # catalog step.
    GenerationStep("search-index", "build_search_index.py", (), ("--check",), "Site search index", ("data/works.json", "data/work-enrichment.json", "data/software.json", "data/github-repositories.json", "data/videos.json", "data/people.json", "data/organizations.json", "data/claims.json", "data/resume.json", "papers/*/full_text.md", "papers/*/images/*", "reports/reconciliation_*.md", "reports/public_source_inventory_*.json", "reports/accessibility_static_*.json", "reports/external_links_[0-9]*.json", "reports/external_links_triage_*.md", "reports/asset_size_*.json", "reports/live_site_verification_*.json", "reports/visual-qa/*/manifest.json", "reports/browser-smoke/*/manifest.json")),
    GenerationStep("feed", "generate_feed.py", (), ("--check",), "RSS feed", ("data/works.json", "data/site-updates.json")),
    GenerationStep("domain-feeds", "build_domain_feeds.py", (), ("--check",), "Per-domain RSS feeds", ("data/works.json", "data/videos.json")),
    # DERIVED (always-run): <lastmod> derives from git commit dates, which no
    # content fingerprint captures — and --check tolerates lastmod-only
    # drift, so a skip would silently strand the runbook's post-commit
    # sitemap re-render.
    GenerationStep("sitemap", "build_sitemap.py", (), ("--check",), "Sitemap"),
    # DERIVED (always-run): renders from the shared nav manifest in
    # code/src/site_nav.py; consumes no repository data files.
    GenerationStep("404-page", "build_404_page.py", (), ("--check",), "GitHub Pages 404 page"),
    GenerationStep("artwork-index", "build_artwork_index.py", (), ("--check",), "Compact artwork index", ("data/artworks.json",)),
    # DERIVED (always-run): projects the whole tracked tree into the Pages
    # artifact — no bounded input glob exists for its source set.
    GenerationStep("pages-artifact", "build_pages_artifact.py", ("--write-manifest", "--allow-dirty-prepayload-evidence", "--check-size-only"), ("--check-size-only", "--check-manifest"), "Pages artifact manifest and budget"),
    # DERIVED (always-run): renders GENERATED.md + data/generated-manifest.json
    # from the in-script ARTIFACTS/UTILITIES tables; consumes no repo files.
    GenerationStep("generated-manifest-first", "build_generated_manifest.py", (), ("--check",), "Generated artifact matrix before agent index"),
    GenerationStep("agent-index", "build_agent_index.py", (), ("--check",), "Agent route manifest", ("data/current-counts.json", "data/artworks.json", "data/artworks-index.json", "data/videos.json", "data/videos-index.json", "data/works.json", "data/software.json", "data/github-repositories.json", "data/claims.json", "data/scholar-verification-receipt.json", "search-index.json", "data/coverage-exceptions.json", "data/repository-classification.json", "data/people.json", "data/organizations.json", "data/work-enrichment.json", "data/catalog.json", "data/reconciliation.json", "data/reproducibility.json", "data/generated-manifest.json", "data/pages-artifact-manifest.json", "reports/live_site_verification_*.json")),
    # DERIVED (always-run): the envelope binds git deployment state (source
    # commit, worktree-vs-deployed diff) and generator-script hashes that no
    # content fingerprint captures; skipping could mint a stale-looking
    # integrity envelope.
    GenerationStep("release-integrity", "build_release_integrity.py", (), ("--check",), "Pre-deploy integrity envelope"),
    GenerationStep("generated-manifest-final", "build_generated_manifest.py", (), ("--check",), "Final generated artifact matrix"),
)


EXCLUDED_OPERATIONS: tuple[ExcludedOperation, ...] = (
    ExcludedOperation("add_zenodo_only.py", "network/source-authoring/binary-intake/manual-review", "Zenodo intake can create bibliography rows, paper folders, and downloaded binaries."),
    ExcludedOperation("audit_private_reconciliation.py", "manual-review", "Private/public comparison writes a dated decision receipt and must remain an explicit reconciliation action."),
    ExcludedOperation("batch_enrich_metadata.py", "source-authoring/manual-review", "Bulk metadata enrichment can introduce inferred methods/findings and clock-derived fields; it requires per-paper review rather than local regeneration."),
    ExcludedOperation("build_external_link_triage.py", "network-derived/review", "Triage derives a review queue from an explicitly refreshed external-link report."),
    ExcludedOperation("build_public_source_review.py", "network-derived/manual-review", "Review records applied, deferred, and rejected findings without automatically changing curated source."),
    ExcludedOperation("check_zenodo_uncatalogued.py", "network/manual-review", "Live Zenodo discovery produces curation candidates requiring review."),
    ExcludedOperation("ensure_social_meta.py", "source-migration/manual-review", "Legacy hand-authored social-meta normalizer remains an explicit migration until its canonical renderer supersedes it."),
    ExcludedOperation("extract_paper_texts.py", "binary-intake/manual-review", "PDF extraction and image intake are explicitly deferred binary operations."),
    ExcludedOperation("fetch_video_transcripts.py", "network/cache-refresh", "Caption intake is a deliberate network cache refresh."),
    ExcludedOperation("fetch_work_authors.py", "network/manual-review", "DOI-agency author enrichment can alter curated bibliography source after review."),
    ExcludedOperation("fetch_youtube_data.py", "network/cache-refresh/manual-review", "YouTube cache refresh is intentionally outside local regeneration and fails closed on incomplete tabs."),
    ExcludedOperation("gsc_followup_preflight.py", "network/manual-review", "Search Console follow-up requires a signed-in human action."),
    ExcludedOperation("improve_metadata_quality.py", "source-authoring/manual-review", "Targeted metadata quality edits can introduce paper-specific research claims and require explicit review."),
    ExcludedOperation("migrate_inline_handlers.py", "source-migration/manual-review", "This migration edits hand-authored HTML and lacks an exact no-write renderer."),
    ExcludedOperation("optimize_font_loading.py", "source-migration/manual-review", "This migration edits hand-authored HTML and lacks an exact no-write renderer."),
    ExcludedOperation("reconcile_paper_dois.py", "manual-review/source-reconciliation", "DOI role changes require an approval-bound source reconciliation receipt."),
    ExcludedOperation("refresh_public_sources.py", "network", "Public API evidence requires explicit review before curated claims change."),
    ExcludedOperation("refresh_public_source_inventory.py", "network", "Public inventory fetch writes dated evidence and may expose review candidates."),
    ExcludedOperation("build_github_inventory.py", "network", "GitHub inventory refresh is an explicit freshness operation."),
    ExcludedOperation("sync_paired_publications.py", "network/manual-review", "Ambiguous DOI/release pairings must not be auto-promoted."),
    ExcludedOperation("check_external_links.py", "network", "External link probing is a deliberate cached-evidence refresh."),
    ExcludedOperation("browser_smoke.py", "browser", "Browser evidence is refreshed deliberately against the candidate revision."),
    ExcludedOperation("browser_qa.py", "browser", "Interaction and accessibility evidence requires the browser runtime."),
    ExcludedOperation("visual_qa.py", "browser/manual-review", "Screenshots require human visual review."),
    ExcludedOperation("verify_live_site.py", "network/post-deploy", "Live-site verification must observe the deployed SHA."),
    ExcludedOperation("attest_release.py", "post-deploy", "Release attestation is only valid after deployment and live verification."),
    ExcludedOperation("build_work_pages.py --prune-owned", "destructive/manual-review", "Only an explicit manual invocation may remove renderer-owned orphan work pages; hand-authored pages are preserved."),
    ExcludedOperation("prune_old_reports.py", "destructive/manual-review", "Deletion requires reviewed provenance records in data/report-retention.json."),
)


ORCHESTRATORS_DIR = Path(__file__).resolve().parents[1] / "orchestrators"
# This intentionally favors false positives: a new ordinary Python write form
# must be classified as a deterministic generation step or an explicit manual/
# network/destructive operation before the release plan can pass.  Supporting
# ``open(..., "w")`` closes the common bypass where a writer did not use a
# pathlib convenience method.
_WRITE_CALL = re.compile(
    r"(?:"
    r"(?:write_text|write_bytes|\.unlink|rmtree|os\.(?:remove|unlink|replace|rename))\s*\(|"
    r"(?:^|[^.\w])open\([^\n]*?,\s*['\"](?:w|a|x)[^'\"]*['\"]|"
    r"\.open\(\s*['\"](?:w|a|x)[^'\"]*['\"]|"
    r"\.open\([^\n]*?,\s*['\"](?:w|a|x)[^'\"]*['\"]|"
    r"os\.fdopen\([^\n]*?,\s*['\"](?:w|a|x)[^'\"]*['\"]"
    r")"
)


def discovered_writer_scripts(orchestrators_dir: Path = ORCHESTRATORS_DIR) -> set[str]:
    """Conservatively discover direct filesystem-mutating orchestrators.

    The declared inventory is the release boundary. This lightweight source
    scan makes a newly introduced common writer form fail planning until it is
    paired with a no-write check or explicitly classified as excluded.
    """
    return {
        path.name
        for path in orchestrators_dir.glob("*.py")
        if _WRITE_CALL.search(path.read_text(encoding="utf-8", errors="ignore"))
    }


def coverage_errors(
    steps: tuple[GenerationStep, ...] = LOCAL_GENERATION_STEPS,
    exclusions: tuple[ExcludedOperation, ...] = EXCLUDED_OPERATIONS,
    orchestrators_dir: Path = ORCHESTRATORS_DIR,
) -> list[str]:
    """Return structural gaps that could create a false-green generation gate."""
    errors: list[str] = []
    identifiers = [step.identifier for step in steps]
    if len(identifiers) != len(set(identifiers)):
        errors.append("duplicate generation-step identifiers")
    for step in steps:
        if not step.script.endswith(".py"):
            errors.append(f"{step.identifier}: script must be a Python orchestrator")
        if not step.check_args:
            errors.append(f"{step.identifier}: missing no-write check arguments")
        if "--apply" in step.check_args or "--write-manifest" in step.check_args:
            errors.append(f"{step.identifier}: check command contains a write flag")
        if not (orchestrators_dir / step.script).is_file():
            errors.append(f"{step.identifier}: missing orchestrator {step.script}")
    step_scripts = {step.script for step in steps}
    excluded_scripts = {entry.script.split(maxsplit=1)[0] for entry in exclusions}
    # An excluded *sub-operation* such as ``build_work_pages.py --prune-owned``
    # may coexist with the safe normal writer. Only an exact script-level
    # exclusion conflicts with a generation step.
    exact_excluded_scripts = {entry.script for entry in exclusions if " " not in entry.script}
    overlap = sorted(step_scripts & exact_excluded_scripts)
    if overlap:
        errors.append("writer both generated and excluded: " + ", ".join(overlap))
    for script in sorted(excluded_scripts):
        if not (orchestrators_dir / script).is_file():
            errors.append(f"excluded operation references missing orchestrator {script}")
    unclassified = sorted(discovered_writer_scripts(orchestrators_dir) - step_scripts - excluded_scripts)
    if unclassified:
        errors.append("unclassified write-capable orchestrators: " + ", ".join(unclassified))
    return errors


def validate_generation_plan() -> None:
    """Fail fast before either driver runs an incomplete metadata plan."""
    errors = coverage_errors()
    if errors:
        raise RuntimeError("Invalid generation plan: " + "; ".join(errors))


REPO_ROOT = Path(__file__).resolve().parents[2]
# Persisted skip-on-unchanged state for write-mode regeneration. This is local
# build bookkeeping, not a site artifact: it lives outside the public data
# layer and is gitignored, so it never enters the generated manifest, the Pages
# artifact, or a release-source cleanliness gate.
REGENERATION_STATE_RELATIVE_PATH = Path("reports") / "regeneration-state.json"
REGENERATION_STATE_SCHEMA_VERSION = 1
# Directory parts that are local build/dependency noise, never generation
# inputs. Mirrors validate_repo.IGNORED_VALIDATION_PATH_PARTS; kept independent
# so the plan module does not import an orchestrator.
_FINGERPRINT_EXCLUDED_PARTS = frozenset(
    {".git", "_site", ".venv", ".pytest_cache", "__pycache__", "node_modules"}
)


def regeneration_state_path(repo_root: Path = REPO_ROOT) -> Path:
    """Location of the persisted input fingerprints for skipped steps."""
    return repo_root / REGENERATION_STATE_RELATIVE_PATH


def load_regeneration_state(repo_root: Path = REPO_ROOT) -> dict[str, str]:
    """Load persisted ``identifier -> input fingerprint`` entries.

    Any unreadable or unexpected payload yields an empty state, which makes the
    next write-mode run execute every step (the conservative direction).
    """
    path = regeneration_state_path(repo_root)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    if not isinstance(payload, dict) or not isinstance(payload.get("steps"), dict):
        return {}
    return {str(key): str(value) for key, value in payload["steps"].items()}


def save_regeneration_state(state: dict[str, str], repo_root: Path = REPO_ROOT) -> None:
    """Persist fingerprints deterministically (no timestamps, sorted keys)."""
    payload = {
        "schema_version": REGENERATION_STATE_SCHEMA_VERSION,
        "steps": dict(sorted(state.items())),
    }
    path = regeneration_state_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def input_fingerprint(
    repo_root: Path,
    patterns: tuple[str, ...],
    exclude: tuple[str, ...] = (),
) -> str | None:
    """Content hash over every file matched by ``patterns`` minus ``exclude``.

    Returns ``None`` — the caller must then run the step — when any pattern
    matches no file, an input cannot be read, or ``patterns`` is empty, so a
    typo or an empty tree can never produce a false skip. The digest covers
    path, size, and bytes, so it ignores mtime-only touches and reacts to any
    content change.
    """
    if not patterns:
        return None
    excluded = {
        path.relative_to(repo_root).as_posix()
        for pattern in exclude
        for path in repo_root.glob(pattern)
    }
    digest = hashlib.sha256()
    for pattern in patterns:
        matches = [
            path
            for path in sorted(repo_root.glob(pattern))
            if path.is_file()
            and path.relative_to(repo_root).as_posix() not in excluded
            and not _FINGERPRINT_EXCLUDED_PARTS.intersection(path.parts)
        ]
        if not matches:
            return None
        for path in matches:
            rel = path.relative_to(repo_root).as_posix()
            digest.update(f"{rel}\0{path.stat().st_size}\0".encode())
            try:
                with path.open("rb") as handle:
                    for chunk in iter(lambda: handle.read(1 << 20), b""):
                        digest.update(chunk)
            except OSError:
                return None
            digest.update(b"\0")
    return digest.hexdigest()


def step_skip_reason(
    step: GenerationStep,
    state: dict[str, str],
    repo_root: Path = REPO_ROOT,
) -> str | None:
    """Return a skip reason when the step's declared inputs are unchanged.

    Steps without declared inputs never skip; a fingerprint of ``None`` always
    runs the step.
    """
    if not step.inputs:
        return None
    fingerprint = input_fingerprint(repo_root, step.inputs, step.inputs_exclude)
    if fingerprint is None or state.get(step.identifier) != fingerprint:
        return None
    return f"declared inputs unchanged since {REGENERATION_STATE_RELATIVE_PATH}"


def record_step_state(
    step: GenerationStep,
    state: dict[str, str],
    repo_root: Path = REPO_ROOT,
) -> None:
    """Store the current input fingerprint after a step ran successfully."""
    if not step.inputs:
        return
    fingerprint = input_fingerprint(repo_root, step.inputs, step.inputs_exclude)
    if fingerprint is not None:
        state[step.identifier] = fingerprint
