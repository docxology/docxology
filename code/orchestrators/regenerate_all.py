#!/usr/bin/env python3
"""Regenerate locally-derived site artifacts with two ordered passes by default.

`validate_repo.py` runs each generator with ``--check`` in its authoritative order and
fails on the first stale output. There was no write-mode equivalent, so after a
publication apply (or any source edit) the regeneration order had to be rediscovered by
hand, re-running generators one at a time until `validate_repo.py` went green.

This script encodes the shared order in *write* mode. Some consumers precede a
producer (counts/software, domain pages/work enrichment, and resume/folder flags),
so the default second pass refreshes those consumers after their producers ran.
Two passes address those known dependencies; ``--validate`` remains the authority
for stale outputs and does not promise arbitrary fixed-point convergence. The integrity
tail is deliberately explicit: Pages budget → generated manifest → agent index → release
integrity → final generated manifest. The first generated-manifest pass must precede the
agent index because the latter records the manifest hash; the final pass confirms the
complete command matrix after release-integrity is written.

Scope: LOCAL artifacts only. This script is deliberately offline; after the
generated layer converges, repeated runs preserve its content. Network
*freshness* operations are intentionally NOT bundled here, because each fetch writes a new
dated report and mutates GitHub/Zenodo-derived data, which would make this command
non-idempotent and inflate `reports/`. Run those deliberately instead (see
docs/operations/publication-sync.md → "Refresh Public Sources"):
    build_github_inventory.py, refresh_public_sources.py,
    refresh_public_source_inventory.py, verify_live_site.py

Usage:
    uv run python3 code/orchestrators/regenerate_all.py            # two local passes
    uv run python3 code/orchestrators/regenerate_all.py --validate # then run validate_repo
    uv run python3 code/orchestrators/regenerate_all.py --force    # run every step, no skipping
    uv run python3 code/orchestrators/regenerate_all.py --passes 1 # diagnostic single pass
    uv run python3 code/orchestrators/regenerate_all.py --list     # print the plan, run nothing

This is the single write-mode entry point for the intake path: one command runs
the full local chain twice by default. Steps that declare ``inputs`` in
``code/src/generation_plan.py`` are skipped when those declared inputs hash to
the same content as the previous successful run. The cache also fingerprints
each writer, the shared ``code/src`` Python libraries, and declared imported
orchestrator helpers (persisted in
``reports/regeneration-state.json``, gitignored); ``--force`` disables
skipping. ``validate_repo.py`` never consults this state — its ``--check``
battery stays the authority, so a write-mode skip can never mask a check
failure.

Caveats:
  * Run from the repo root (enforced via REPO_ROOT).
  * A private POSIX flock rejects overlapping coordinated runs before any writer;
    it covers all passes and optional validation. Never delete its lock file.
  * `sitemap.xml` <lastmod> derives from git commit dates, so for an accurate sitemap
    regenerate it AGAIN after committing (see the runbook's Acceptance Checks).
  * When counts changed (e.g. a new publication), the cached live-site snapshot's
    expected_counts goes stale; run `verify_live_site.py` (needs GITHUB_TOKEN) before
    `validate_repo`, or its verify_live_site --check will report a snapshot mismatch.
"""

from __future__ import annotations

import argparse
import os
import stat
import subprocess
import sys
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from pathlib import Path

try:
    import fcntl
except ImportError:  # POSIX flock is required; never silently run unlocked.
    fcntl = None

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]

from docxology_tools.generation_plan import (  # noqa: E402
    LOCAL_GENERATION_STEPS,
    GenerationStep,
    effective_step_inputs,
    load_regeneration_state,
    record_step_state,
    save_regeneration_state,
    step_input_fingerprint,
    step_skip_reason,
    validate_generation_plan,
)

# Compatibility projection for scripts/tests that consume the historical
# ``(script, args)`` shape. The authoritative write/check pairing is declared
# once in ``code/src/generation_plan.py``.
CHAIN: list[tuple[str, list[str]]] = [
    (step.script, list(step.write_args)) for step in LOCAL_GENERATION_STEPS
]


class RegenerationLockError(RuntimeError):
    """The repository cannot safely acquire its single-writer lock."""


@contextmanager
def _regeneration_lock(repo_root: Path) -> Iterator[int]:
    """Acquire one private, nonblocking POSIX lock without replacing its inode."""
    if fcntl is None or not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise RegenerationLockError("regeneration requires POSIX flock and safe file opens")
    directory = repo_root.resolve() / ".docxology"
    descriptor = directory_descriptor = None
    try:
        try:
            directory.mkdir(mode=0o700, exist_ok=True)
            directory_descriptor = os.open(
                directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
            )
            descriptor = os.open(
                "regeneration.lock", os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK,
                0o600, dir_fd=directory_descriptor,
            )
            metadata = os.fstat(descriptor)
            if not stat.S_ISREG(metadata.st_mode) or metadata.st_nlink != 1:
                raise RegenerationLockError("regeneration lock must be a regular, unshared file")
            os.fchmod(descriptor, 0o600)
            try:
                fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise RegenerationLockError(
                    f"another regeneration is active for {repo_root.resolve()}; "
                    "wait for it to finish and retry (do not delete the lock file)"
                ) from exc
        except OSError as exc:
            raise RegenerationLockError(f"cannot acquire regeneration lock: {exc}") from exc
        yield descriptor
    finally:
        # Closing releases flock on success or failure. Do not explicitly unlock:
        # a launched writer may still hold this descriptor if the driver exits.
        if descriptor is not None:
            os.close(descriptor)
        if directory_descriptor is not None:
            os.close(directory_descriptor)


def _run(
    script: str, args: list[str], *, repo_root: Path = REPO_ROOT,
    lock_descriptor: int | None = None,
) -> None:
    # ReportLab is pinned in pyproject.toml for byte-identical PDFs. Use the
    # locked uv environment for the CV generator even when this driver is
    # launched with a different system Python.
    interpreter = ["uv", "run", "python3"] if script == "build_resume.py" else [sys.executable]
    cmd = [*interpreter, f"code/orchestrators/{script}", *args]
    print(f"\n=== {script} {' '.join(args)} ".rstrip().ljust(72, "="))
    subprocess.run(
        cmd, cwd=repo_root, check=True,
        pass_fds=() if lock_descriptor is None else (lock_descriptor,),
    )


def run_regeneration(
    *,
    force: bool = False,
    runner: Callable[[str, list[str]], None] | None = None,
    repo_root: Path = REPO_ROOT,
    emit: Callable[[str], None] = print,
    steps: tuple[GenerationStep, ...] = LOCAL_GENERATION_STEPS,
) -> tuple[int, int]:
    """Acquire the repository lock and run one input-gated write pass.

    Steps without declared inputs always run. Fingerprint state is persisted
    only after a step ran successfully, and only when something actually ran,
    so a crash or a pure-skip run can never record a state the tree does not
    reflect. Inputs must have the same fingerprint before and after the writer;
    a concurrent change invalidates that cache entry. The default child process
    runs in ``repo_root`` just like the cache. Returns ``(ran, skipped)``.
    """
    with _regeneration_lock(repo_root) as lock_descriptor:
        return _run_regeneration_locked(
            force=force, runner=runner, repo_root=repo_root, emit=emit, steps=steps,
            lock_descriptor=lock_descriptor,
        )


def _run_regeneration_locked(
    *, force: bool, runner: Callable[[str, list[str]], None] | None,
    repo_root: Path, emit: Callable[[str], None], steps: tuple[GenerationStep, ...],
    lock_descriptor: int,
) -> tuple[int, int]:
    """Run a pass under its caller's lock; never acquire recursively."""
    state = load_regeneration_state(repo_root)
    persisted_state = state.copy()
    ran = skipped = 0
    for step in steps:
        reason = None if force else step_skip_reason(step, state, repo_root)
        if reason is not None:
            emit(f"skip {step.identifier}: {reason}")
            skipped += 1
            continue
        before = step_input_fingerprint(step, repo_root)
        # Invalidate an older successful entry before touching outputs. A
        # forced writer can fail or be interrupted with unchanged inputs;
        # leaving that old entry would let the next run skip partial output.
        # Persist only invalidations here, never successful partial-pass work.
        if step.identifier in persisted_state:
            persisted_state.pop(step.identifier)
            save_regeneration_state(persisted_state, repo_root)
        if runner is None:
            _run(
                step.script, list(step.write_args), repo_root=repo_root,
                lock_descriptor=lock_descriptor,
            )
        else:
            runner(step.script, list(step.write_args))
        if step.inputs:
            if before is None:
                state.pop(step.identifier, None)
            elif not record_step_state(step, state, repo_root, expected_fingerprint=before):
                emit(f"cache invalidated {step.identifier}: declared inputs changed during writer")
        ran += 1
    if ran:
        save_regeneration_state(state, repo_root)
    return ran, skipped


def run_regeneration_passes(
    *,
    passes: int = 2,
    force: bool = False,
    runner: Callable[[str, list[str]], None] | None = None,
    repo_root: Path = REPO_ROOT,
    emit: Callable[[str], None] = print,
    steps: tuple[GenerationStep, ...] = LOCAL_GENERATION_STEPS,
) -> tuple[int, int]:
    """Run bounded ordered passes; validate only after the final one.

    Keep ``run_regeneration`` as the single-pass API used by scoped callers.
    A failed pass propagates immediately, preventing later passes or checks
    from presenting a partial render as successful.
    """
    if not 1 <= passes <= 4:
        raise ValueError("regeneration passes must be between 1 and 4")
    with _regeneration_lock(repo_root) as lock_descriptor:
        return _run_regeneration_passes_locked(
            passes=passes, force=force, runner=runner, repo_root=repo_root,
            emit=emit, steps=steps, lock_descriptor=lock_descriptor,
        )


def _run_regeneration_passes_locked(
    *, passes: int, force: bool, runner: Callable[[str, list[str]], None] | None,
    repo_root: Path, emit: Callable[[str], None], steps: tuple[GenerationStep, ...],
    lock_descriptor: int,
) -> tuple[int, int]:
    ran = skipped = 0
    for number in range(1, passes + 1):
        emit(f"Local regeneration pass {number}/{passes}")
        pass_ran, pass_skipped = _run_regeneration_locked(
            force=force, runner=runner, repo_root=repo_root, emit=emit, steps=steps,
            lock_descriptor=lock_descriptor,
        )
        ran += pass_ran
        skipped += pass_skipped
    return ran, skipped


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--validate", action="store_true",
                        help="run validate_repo.py after regeneration")
    parser.add_argument("--force", action="store_true",
                        help="run every step even when its declared inputs are unchanged")
    parser.add_argument("--passes", type=int, choices=range(1, 5), default=2,
                        help="ordered local passes (default: 2; 1 is diagnostic)")
    parser.add_argument("--list", action="store_true", dest="list_only",
                        help="print the ordered plan and exit without running anything")
    args = parser.parse_args()
    validate_generation_plan()

    if args.list_only:
        for i, step in enumerate(LOCAL_GENERATION_STEPS, 1):
            line = f"{i:2}. {step.script} {' '.join(step.write_args)}".rstrip()
            if step.inputs:
                line += f"  # inputs: {', '.join(effective_step_inputs(step))}"
            print(line)
        return 0

    try:
        with _regeneration_lock(REPO_ROOT) as lock_descriptor:
            ran, skipped = _run_regeneration_passes_locked(
                force=args.force, passes=args.passes, repo_root=REPO_ROOT,
                runner=None, emit=print, steps=LOCAL_GENERATION_STEPS,
                lock_descriptor=lock_descriptor,
            )
            if args.validate:
                print("\n=== validate_repo.py ".ljust(72, "="))
                subprocess.run(
                    [sys.executable, "code/orchestrators/validate_repo.py"],
                    cwd=REPO_ROOT, check=True, pass_fds=(lock_descriptor,),
                )
    except RegenerationLockError as exc:
        print(f"regeneration refused: {exc}", file=sys.stderr)
        return 1

    print(f"\nRan {ran} local surfaces (skipped {skipped} with unchanged declared inputs).")
    print("Note: network freshness (GitHub inventory, live-site snapshot, public sources) "
          "was NOT run — do that deliberately per docs/operations/publication-sync.md. "
          "Use --force to ignore skip-on-unchanged state and rebuild every surface.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
