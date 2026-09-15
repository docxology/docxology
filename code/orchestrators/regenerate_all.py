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
    uv run python3 code/orchestrators/regenerate_all.py --force    # run every step, no skipping
    uv run python3 code/orchestrators/regenerate_all.py --list     # print the plan, run nothing

This is the single write-mode entry point for the intake path: one command runs
the full local chain once. Steps that declare ``inputs`` in
``code/src/generation_plan.py`` are skipped when those declared inputs hash to
the same content as the previous successful run (persisted in
``reports/regeneration-state.json``, gitignored); ``--force`` disables
skipping. ``validate_repo.py`` never consults this state — its ``--check``
battery stays the authority, so a write-mode skip can never mask a check
failure.

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
from collections.abc import Callable
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from generation_plan import (  # noqa: E402
    LOCAL_GENERATION_STEPS,
    GenerationStep,
    load_regeneration_state,
    record_step_state,
    save_regeneration_state,
    step_skip_reason,
    validate_generation_plan,
)

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


def run_regeneration(
    *,
    force: bool = False,
    runner: Callable[[str, list[str]], None] = _run,
    repo_root: Path = REPO_ROOT,
    emit: Callable[[str], None] = print,
    steps: tuple[GenerationStep, ...] = LOCAL_GENERATION_STEPS,
) -> tuple[int, int]:
    """Run the write chain, skipping input-gated steps whose inputs are fresh.

    Steps without declared inputs always run. Fingerprint state is persisted
    only after a step ran successfully, and only when something actually ran,
    so a crash or a pure-skip run can never record a state the tree does not
    reflect. Returns ``(ran, skipped)``.
    """
    state = load_regeneration_state(repo_root)
    ran = skipped = 0
    for step in steps:
        reason = None if force else step_skip_reason(step, state, repo_root)
        if reason is not None:
            emit(f"skip {step.identifier}: {reason}")
            skipped += 1
            continue
        runner(step.script, list(step.write_args))
        record_step_state(step, state, repo_root)
        ran += 1
    if ran:
        save_regeneration_state(state, repo_root)
    return ran, skipped


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--validate", action="store_true",
                        help="run validate_repo.py after regeneration")
    parser.add_argument("--force", action="store_true",
                        help="run every step even when its declared inputs are unchanged")
    parser.add_argument("--list", action="store_true", dest="list_only",
                        help="print the ordered plan and exit without running anything")
    args = parser.parse_args()
    validate_generation_plan()

    if args.list_only:
        for i, step in enumerate(LOCAL_GENERATION_STEPS, 1):
            line = f"{i:2}. {step.script} {' '.join(step.write_args)}".rstrip()
            if step.inputs:
                line += f"  # inputs: {', '.join(step.inputs)}"
            print(line)
        return 0

    ran, skipped = run_regeneration(force=args.force)

    print(f"\nRan {ran} local surfaces (skipped {skipped} with unchanged declared inputs).")
    print("Note: network freshness (GitHub inventory, live-site snapshot, public sources) "
          "was NOT run — do that deliberately per docs/operations/publication-sync.md. "
          "Use --force to ignore skip-on-unchanged state and rebuild every surface.")

    if args.validate:
        print("\n=== validate_repo.py ".ljust(72, "="))
        subprocess.run([sys.executable, "code/orchestrators/validate_repo.py"], cwd=REPO_ROOT, check=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
