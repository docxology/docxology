#!/usr/bin/env python3
"""Regenerate every locally-derived site artifact in one dependency-ordered pass.

`validate_repo.py` runs each generator with ``--check`` in its authoritative order and
fails on the first stale output. There was no write-mode equivalent, so after a
publication apply (or any source edit) the regeneration order had to be rediscovered by
hand, re-running generators one at a time until `validate_repo.py` went green.

This script encodes that order once, in *write* mode, so a single command rebuilds the
generated layer deterministically from the current sources. The order below is
dependency-correct (each step's inputs are produced by an earlier step). The integrity
tail is deliberately explicit: Pages budget → agent index → generated manifest → release
integrity → final generated manifest. The agent index is built only after all dated
reports and the Pages projection exist because it links to their latest paths and
records the Pages manifest's dataset hashes.

Scope: LOCAL artifacts only. This script is deliberately offline and idempotent — run it
as many times as you like and (absent a source edit) it changes nothing. Network
*freshness* operations are intentionally NOT bundled here, because each fetch writes a new
dated report and mutates GitHub/Zenodo-derived data, which would make this command
non-idempotent and inflate `reports/`. Run those deliberately instead (see
docs/operations/publication-sync.md → "Refresh Public Sources"):
    build_github_inventory.py, refresh_public_sources.py,
    refresh_public_source_inventory.py, verify_live_site.py

Usage:
    uv run python3 code/orchestrators/regenerate_all.py            # rebuild local layer
    uv run python3 code/orchestrators/regenerate_all.py --validate # then run validate_repo
    uv run python3 code/orchestrators/regenerate_all.py --list     # print the plan, run nothing

Caveats:
  * Run from the repo root (enforced via REPO_ROOT).
  * `sitemap.xml` <lastmod> derives from git commit dates, so for an accurate sitemap
    regenerate it AGAIN after committing (see the runbook's Acceptance Checks).
  * When counts changed (e.g. a new publication), the cached live-site snapshot's
    expected_counts goes stale; run `verify_live_site.py` (needs GITHUB_TOKEN) before
    `validate_repo`, or its verify_live_site --check will report a snapshot mismatch.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Local, dependency-ordered write chain. Each tuple is (script, args).
# The final build_generated_manifest is intentionally last (it hashes every other output).
CHAIN: list[tuple[str, list[str]]] = [
    ("export_bibliography.py", []),              # works.json + bib/csl/ris  <- pages/BIBLIOGRAPHY.md
    ("sync_publications_html.py", ["--apply"]),  # publications.html + -ld   <- works.json
    ("sync_software_html.py", ["--apply"]),      # software.html + -ld       <- pages/SOFTWARE.md
    ("build_current_counts.py", []),             # current-counts.{json,md}  <- works + software
    ("build_coverage_exceptions.py", []),        # explicit source coverage queue <- works.json
    ("classify_repositories.py", []),            # repository review queue <- GitHub inventory
    ("sync_scholar_metrics.py", []),             # dated Scholar snapshot -> hand-authored surfaces
    ("generate_og_images.py", []),               # og-*.jpg + counts sidecar <- current-counts.json
    ("export_agent_data.py", []),                # claims/people/orgs        <- counts
    ("build_resume.py", ["--all"]),              # resume.{json,txt,pdf}     <- claims + counts
    ("build_domain_pages.py", []),
    ("build_work_pages.py", []),
    ("build_video_pages.py", []),
    ("sync_site_facts.py", []),                  # finalize volatile facts after video/art data generation
    ("prune_old_reports.py", ["--apply"]),       # drop superseded QA screenshot sets — MUST follow sync_site_facts
                                                 # (which repoints discovery/llms refs to the latest set, so older
                                                 # sets are now unreferenced) and precede build_pages_artifact so the
                                                 # manifest reflects the trimmed tree
    ("build_paper_pages.py", []),
    ("deploy_seo_security.py", []),         # CSP/referrer/agent metadata on public HTML
    ("build_exports_page.py", []),
    ("build_updates_page.py", []),
    ("build_evidence_page.py", []),              # evidence.html + EVIDENCE.md <- claims.json
    ("ensure_agent_navigation.py", []),    # visible manifest link on bespoke entry pages
    ("build_reconciliation_report.py", []),      # writes reports/reconciliation_*.md
    ("audit_assets.py", []),                     # writes reports/asset_size_*.json
    ("accessibility_audit.py", []),              # writes reports/accessibility_static_*.json
    # Indexes below link the *latest* dated reports, so they must run AFTER the report
    # producers above. (validate_repo's --check order differs because --check never
    # writes a new dated report; in write mode the order matters.)
    ("build_catalog.py", []),                    # links latest asset_size/a11y/reconciliation reports
    # The catalog is itself in the public HTML asset budget. Re-run the two
    # report producers after it is rendered so adding a dataset cannot leave
    # the checked-in reports one dependency step behind.
    ("audit_assets.py", []),
    ("accessibility_audit.py", []),
    ("build_search_index.py", []),               # links latest reports + indexes pages
    ("generate_feed.py", []),
    ("build_sitemap.py", []),                    # see caveat: regenerate again post-commit
    ("build_artwork_index.py", []),              # compact gallery grid index <- data/artworks.json
    ("build_image_sitemap.py", []),               # sitemap-images.xml       <- data/artworks.json
    ("build_pages_artifact.py", ["--write-manifest", "--check-size-only"]),
    ("build_agent_index.py", []),                # stable agent route/schema map <- final reports + Pages manifest
    ("build_generated_manifest.py", []),         # include the integrity outputs in the command matrix
    ("build_release_integrity.py", []),
    ("build_generated_manifest.py", []),         # LAST — stable source/output command matrix
]


def _run(script: str, args: list[str]) -> None:
    # ReportLab is pinned in pyproject.toml for byte-identical PDFs. Use the
    # locked uv environment for the CV generator even when this driver is
    # launched with a different system Python.
    interpreter = ["uv", "run", "python3"] if script == "build_resume.py" else [sys.executable]
    cmd = [*interpreter, f"code/orchestrators/{script}", *args]
    print(f"\n=== {script} {' '.join(args)} ".rstrip().ljust(72, "="))
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--validate", action="store_true",
                        help="run validate_repo.py after regeneration")
    parser.add_argument("--list", action="store_true", dest="list_only",
                        help="print the ordered plan and exit without running anything")
    args = parser.parse_args()

    if args.list_only:
        for i, (script, extra) in enumerate(CHAIN, 1):
            print(f"{i:2}. {script} {' '.join(extra)}".rstrip())
        return 0

    for script, extra in CHAIN:
        _run(script, extra)

    print(f"\nRegenerated {len(CHAIN)} local surfaces.")
    print("Note: network freshness (GitHub inventory, live-site snapshot, public sources) "
          "was NOT run — do that deliberately per docs/operations/publication-sync.md.")

    if args.validate:
        print("\n=== validate_repo.py ".ljust(72, "="))
        subprocess.run(["python3", "code/orchestrators/validate_repo.py"], cwd=REPO_ROOT, check=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
