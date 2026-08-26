"""Single source of truth for local generation and exact-check coverage.

The release pipeline used to have a write list in ``regenerate_all.py`` and a
separate, hand-maintained check list in ``validate_repo.py``.  They inevitably
drifted.  This module declares every local deterministic step once; both
drivers consume it, and the coverage check rejects a writer without a matching
no-write verification command.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class GenerationStep:
    """A deterministic local writer and the exact check for its outputs."""

    identifier: str
    script: str
    write_args: tuple[str, ...]
    check_args: tuple[str, ...]
    description: str


@dataclass(frozen=True)
class ExcludedOperation:
    """An intentionally non-automatic operation and its release boundary."""

    script: str
    category: str
    reason: str


# Ordered writer chain. Repeated audit/fact steps are deliberately explicit:
# later generators consume their dated reports, so the second pass verifies the
# final dependency state rather than a one-step-behind report pointer.
LOCAL_GENERATION_STEPS: tuple[GenerationStep, ...] = (
    GenerationStep("export-bibliography", "export_bibliography.py", (), ("--check",), "Bibliography exports and works projection"),
    GenerationStep("sync-publications", "sync_publications_html.py", ("--apply",), ("--check",), "Publication HTML and JSON-LD"),
    GenerationStep("sync-software", "sync_software_html.py", ("--apply",), ("--check",), "Software HTML and JSON-LD"),
    GenerationStep("github-inventory-pages", "render_github_inventory.py", (), ("--check",), "Cached GitHub inventory HTML pages"),
    GenerationStep("current-counts", "build_current_counts.py", (), ("--check",), "Volatile count report"),
    GenerationStep("coverage-exceptions", "build_coverage_exceptions.py", (), ("--check",), "Source coverage queue"),
    GenerationStep("repository-classification", "classify_repositories.py", (), ("--check",), "Repository review queue"),
    GenerationStep("scholar-metrics", "sync_scholar_metrics.py", (), ("--check",), "Snapshot-backed Scholar surfaces"),
    GenerationStep("og-images", "generate_og_images.py", (), ("--check",), "Open Graph images"),
    GenerationStep("agent-data", "export_agent_data.py", (), ("--check",), "Agent data exports"),
    GenerationStep("resume", "build_resume.py", ("--all",), ("--check",), "Resume/CV exports"),
    GenerationStep("domain-pages", "build_domain_pages.py", (), ("--check",), "Domain landing pages"),
    GenerationStep("pillar-pages", "generate_pillar_pages.py", (), ("--check",), "Shared-rendered pillar pages"),
    GenerationStep("paper-documents", "regenerate_docs.py", ("--apply",), ("--check",), "Manifest-owned paper documentation"),
    GenerationStep("citation-cff", "generate_citation_cff.py", ("--apply",), ("--check",), "Canonical/artifact DOI roles in paper CFF files"),
    # Paper-document rendering can create the README/AGENTS/SKILL files that
    # bibliography exports classify. Re-export before public work pages so a
    # first clean run reaches a fixed point instead of requiring a second pass.
    GenerationStep("export-bibliography-final", "export_bibliography.py", (), ("--check",), "Bibliography exports after paper documents"),
    GenerationStep("sync-publications-final", "sync_publications_html.py", ("--apply",), ("--check",), "Publication HTML and JSON-LD after paper documents"),
    GenerationStep("work-pages", "build_work_pages.py", (), ("--check",), "Per-work landing pages"),
    GenerationStep("video-pages", "build_video_pages.py", (), ("--check",), "Video landing pages and exports"),
    GenerationStep("site-facts-first", "sync_site_facts.py", (), ("--check",), "Volatile public facts after content projections"),
    GenerationStep("paper-pages", "build_paper_pages.py", (), ("--check",), "Paper folder HTML pages"),
    GenerationStep("redirect-stubs", "generate_redirect_stubs.py", ("--apply",), ("--check",), "Centrally rendered legacy redirects"),
    GenerationStep("seo-security", "deploy_seo_security.py", (), ("--check",), "Shared public head/security normalization"),
    GenerationStep("exports-page", "build_exports_page.py", (), ("--check",), "Exports hub"),
    GenerationStep("updates-page", "build_updates_page.py", (), ("--check",), "Updates page"),
    GenerationStep("evidence-page", "build_evidence_page.py", (), ("--check",), "Evidence page"),
    GenerationStep("reproducibility", "build_reproducibility_ledger.py", (), ("--check",), "Reproducibility ledger"),
    GenerationStep("agent-navigation", "ensure_agent_navigation.py", (), ("--check",), "Visible Agent Map navigation"),
    GenerationStep("reconciliation", "build_reconciliation_report.py", (), ("--check",), "Reconciliation report"),
    GenerationStep("asset-audit-first", "audit_assets.py", (), ("--check",), "Asset-size report"),
    GenerationStep("accessibility-first", "accessibility_audit.py", (), ("--check",), "Static accessibility report"),
    GenerationStep("catalog", "build_catalog.py", (), ("--check",), "Public data catalog"),
    GenerationStep("asset-audit-final", "audit_assets.py", (), ("--check",), "Final asset-size report after catalog"),
    GenerationStep("accessibility-final", "accessibility_audit.py", (), ("--check",), "Final accessibility report after catalog"),
    GenerationStep("site-facts-final", "sync_site_facts.py", (), ("--check",), "Final fact links to latest reports"),
    GenerationStep("search-index", "build_search_index.py", (), ("--check",), "Site search index"),
    GenerationStep("feed", "generate_feed.py", (), ("--check",), "RSS feed"),
    GenerationStep("sitemap", "build_sitemap.py", (), ("--check",), "Sitemap"),
    GenerationStep("artwork-index", "build_artwork_index.py", (), ("--check",), "Compact artwork index"),
    GenerationStep("image-sitemap", "build_image_sitemap.py", (), ("--check",), "Image sitemap"),
    GenerationStep("pages-artifact", "build_pages_artifact.py", ("--write-manifest", "--allow-dirty-prepayload-evidence", "--check-size-only"), ("--check-size-only", "--check-manifest"), "Pages artifact manifest and budget"),
    GenerationStep("generated-manifest-first", "build_generated_manifest.py", (), ("--check",), "Generated artifact matrix before agent index"),
    GenerationStep("agent-index", "build_agent_index.py", (), ("--check",), "Agent route manifest"),
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
