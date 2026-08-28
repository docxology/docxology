#!/usr/bin/env python3
"""Regenerate every locally-derived site artifact in one dependency-ordered pass.

`validate_repo.py` runs each generator with ``--check`` in its authoritative order and
fails on the first stale output. There was no write-mode equivalent, so after a
publication apply (or any source edit) the regeneration order had to be rediscovered by
hand, re-running generators one at a time until `validate_repo.py` went green.

This script encodes that order once, in *write* mode, so a single command rebuilds the
generated layer deterministically from the current sources. The order below is
dependency-correct (each step's inputs are produced by an earlier step). The integrity
tail is deliberately explicit: Pages budget → generated manifest → agent index → release
integrity → final generated manifest. The first generated-manifest pass must precede the
agent index because the latter records the manifest hash; the final pass confirms the
complete command matrix after release-integrity is written.

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
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from generation_plan import LOCAL_GENERATION_STEPS, validate_generation_plan  # noqa: E402

# Compatibility projection for scripts/tests that consume the historical
# ``(script, args)`` shape. The authoritative write/check pairing is declared
# once in ``code/src/generation_plan.py``.
CHAIN: list[tuple[str, list[str]]] = [
    (step.script, list(step.write_args)) for step in LOCAL_GENERATION_STEPS
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
    validate_generation_plan()

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
