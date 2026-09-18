"""The generation plan's order is a tested dependency invariant.

``regenerate_all.py``'s module docstring asserts the chain is
dependency-correct ("each step's inputs are produced by an earlier step").
This module pins that claim to the declared ``inputs``: every declared input
glob must resolve at plan-build time — to files that exist in the checkout,
or to an earlier step's declared output — and no step may consume a file
whose only producer sits later in the chain.

Co-produced families (the first/final audit, manifest, fact, bibliography,
and publication passes that rewrite the same dated or rendered artifact) are
attributed to their EARLIEST producer in ``OUTPUTS``: the earliest pass is
what makes the file available to mid-chain consumers, and the later pass
refreshes it in place — exactly the "deliberately explicit second pass"
design documented in the plan header.

The grandfathered audit/accessibility scan scopes (``ASSET_AUDIT_INPUTS`` and
``**/*.html``) are exempt from the producer rule: they mirror the audit
generators' own broad scan scope (see the plan's comment block), where
re-running on any audited-surface change is the point, not a dependency
claim on one file.
"""

from __future__ import annotations

import fnmatch
import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

import docxology_tools  # noqa: F401,E402  (canonical bootstrap: code/src + code/orchestrators onto sys.path)
from docxology_tools.generation_plan import (  # noqa: E402
    ASSET_AUDIT_INPUTS,
    LOCAL_GENERATION_STEPS,
    GenerationStep,
)
from docxology_tools.release_controls import is_control_path  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]

POSITIONS: dict[str, int] = {step.identifier: i for i, step in enumerate(LOCAL_GENERATION_STEPS)}

# Declared output patterns per producing step, attributed to the earliest
# producer of each path (see module docstring).
OUTPUTS: dict[str, tuple[str, ...]] = {
    "export-bibliography": ("bibliography.bib", "bibliography.ris", "bibliography.csl.json", "data/works.json"),
    "sync-publications": ("publications.html", "data/publications-ld.json"),
    "sync-software": ("software.html", "data/software-ld.json"),
    "github-inventory-pages": ("repositories.html", "repositories-forks.html"),
    "current-counts": ("data/current-counts.json", "reports/current_counts.md"),
    "coverage-exceptions": ("data/coverage-exceptions.json", "reports/source_coverage_*.json", "reports/source_coverage_*.md"),
    "repository-classification": ("data/repository-classification.json",),
    "og-images": ("og-*.jpg", "data/og-image-counts.json"),
    "agent-data": ("data/software.json", "data/people.json", "data/organizations.json", "data/claims.json"),
    "resume": ("data/resume.json", "resume/full.txt", "resume/academic.txt", "resume/software-consulting.txt", "resume/teaching-service.txt", "resume/resume.pdf", "resume/resume.html", "resume/verify.html"),
    "domain-pages": ("domains.html", "domain-*.html", "pages/DOMAINS.md"),
    "pillar-pages": ("cognitive-security.html", "computational-entomology.html", "insect-cognition.html", "active-inference.html", "neurosymbolic-ai.html"),
    "paper-documents": ("papers/*/README.md", "papers/*/AGENTS.md", "papers/*/SKILL.md", "papers/generated-documents.json"),
    "citation-cff": ("papers/*/CITATION.cff",),
    "work-pages": ("works/*.html", "data/work-enrichment.json"),
    "video-pages": ("videos/*.html", "data/videos.json", "data/videos-index.json", "data/video-pages-manifest.json"),
    "site-facts-first": ("index.html", "discovery.html", "pages/DISCOVERY.md", "llms.txt", "art.html", "videos.html"),
    "paper-pages": ("papers/*/index.html",),
    "redirect-stubs": ("about.html", "agent-verify.html", "blog/index.html", "blog/winged-snowflake-2021/index.html", "meditations.html", "nft.html", "reports.html", "research.html"),
    "exports-page": ("exports.html",),
    "updates-page": ("updates.html",),
    "evidence-page": ("evidence.html", "pages/EVIDENCE.md"),
    "reproducibility": ("data/reproducibility.json", "reproducibility.html", "pages/REPRODUCIBILITY.md"),
    "reconciliation": ("data/reconciliation.json", "reports/reconciliation_*.md"),
    "asset-audit-first": ("reports/asset_size_*.json",),
    "accessibility-first": ("reports/accessibility_static_*.json",),
    "catalog": ("catalog.html", "data/catalog.json"),
    "github-readme": (".github/README.md",),
    "search-index": ("search-index.json", "search-index-core.json", "search-index-content-*.json"),
    "feed": ("feed.xml",),
    "domain-feeds": ("feeds/domain-*.xml",),
    "sitemap": ("sitemap.xml",),
    "404-page": ("404.html",),
    "artwork-index": ("data/artworks-index.json",),
    "pages-artifact": ("data/pages-artifact-manifest.json", "reports/pages_artifact_growth_*.json"),
    "generated-manifest-first": ("GENERATED.md", "data/generated-manifest.json"),
    "agent-index": ("data/agent-index.json",),
}


def _files_matching(repo_root: Path, pattern: str) -> list[Path]:
    return [path for path in sorted(repo_root.glob(pattern)) if path.is_file()]


def _is_scan_scope(step: GenerationStep, pattern: str) -> bool:
    if step.identifier in ("asset-audit-first", "asset-audit-final"):
        return pattern in ASSET_AUDIT_INPUTS
    if step.identifier in ("accessibility-first", "accessibility-final"):
        return pattern == "**/*.html"
    return False


def _earliest_producers(repo_root: Path) -> dict[str, int]:
    """Map each existing output file to its earliest producing step position."""
    producers: dict[str, int] = {}
    for identifier, patterns in OUTPUTS.items():
        position = POSITIONS[identifier]
        for pattern in patterns:
            for path in _files_matching(repo_root, pattern):
                rel = path.relative_to(repo_root).as_posix()
                current = producers.get(rel)
                if current is None or position < current:
                    producers[rel] = position
    return producers


def test_every_declared_input_resolves_at_plan_build_time() -> None:
    """Each input glob matches files on disk, or an earlier step's outputs."""
    failures: list[str] = []
    for step in LOCAL_GENERATION_STEPS:
        for pattern in step.inputs:
            if _files_matching(REPO_ROOT, pattern):
                continue
            covered = any(
                fnmatch.fnmatch(rel, pattern)
                for earlier_identifier, patterns in OUTPUTS.items()
                if POSITIONS[earlier_identifier] < POSITIONS[step.identifier]
                for output_pattern in patterns
                for path in _files_matching(REPO_ROOT, output_pattern)
                for rel in [path.relative_to(REPO_ROOT).as_posix()]
            )
            if not covered:
                failures.append(f"{step.identifier}: input {pattern!r} matches nothing")
    assert failures == []


def test_no_step_consumes_a_later_steps_output() -> None:
    """Each consumed file is available by the consuming step's position."""
    producers = _earliest_producers(REPO_ROOT)
    violations: list[str] = []
    for position, step in enumerate(LOCAL_GENERATION_STEPS):
        for pattern in step.inputs:
            if _is_scan_scope(step, pattern):
                continue
            for path in _files_matching(REPO_ROOT, pattern):
                rel = path.relative_to(REPO_ROOT).as_posix()
                produced_at = producers.get(rel)
                if produced_at is not None and produced_at > position:
                    violations.append(
                        f"{step.identifier} (#{position}) consumes {rel} "
                        f"first produced by #{produced_at}"
                    )
    assert violations == []


def test_folded_in_steps_sit_in_dependency_order() -> None:
    """Catalog feeds the final audits; the search index binds final facts."""
    assert POSITIONS["catalog"] < POSITIONS["asset-audit-final"]
    assert POSITIONS["catalog"] < POSITIONS["accessibility-final"]
    assert POSITIONS["site-facts-final"] < POSITIONS["search-index"]
    assert POSITIONS["current-counts"] < POSITIONS["search-index"]
    # The re-export/re-render pairs trail the steps whose outputs they consume.
    assert POSITIONS["paper-documents"] < POSITIONS["export-bibliography-final"]
    assert POSITIONS["paper-documents"] < POSITIONS["sync-publications-final"]
    assert POSITIONS["current-counts"] < POSITIONS["sync-publications-final"]


def test_integrity_tail_matches_the_documented_order() -> None:
    """Pages budget -> generated manifest -> agent index -> release envelope
    -> final generated manifest (regenerate_all.py docstring)."""
    assert (
        POSITIONS["pages-artifact"]
        < POSITIONS["generated-manifest-first"]
        < POSITIONS["agent-index"]
        < POSITIONS["release-integrity"]
        < POSITIONS["generated-manifest-final"]
    )


def test_catalog_and_search_index_outputs_are_payload_not_control() -> None:
    """Grounds the is_control_path note recorded on the two plan steps."""
    payload_paths = (
        "data/catalog.json",
        "catalog.html",
        "search-index.json",
        "search-index-core.json",
        "search-index-content-work.json",
        "search-index-content-video.json",
    )
    assert not any(is_control_path(Path(relative)) for relative in payload_paths)
    assert is_control_path(Path("data/agent-index.json"))
    assert is_control_path(Path("reports/asset_size_2026-01-01.json"))
