#!/usr/bin/env python3
"""Settle dirty work: classify changes, run the tiered battery, land the commits."""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

REPO_ROOT = Path(__file__).resolve().parents[2]
from docxology_tools.change_classifier import Classification, classify_paths  # noqa: E402

# Replaces the manual sequence: payload commit, control-tail commit, then the
# gate cascade by hand (docs/operations/settle.md).  Commits are split per the
# release_controls.is_control_path semantics encoded in
# change_classifier.classify_paths.  The full tier runs the same four checks
# as the validate job of .github/workflows/validate.yml (validate_repo.py,
# pytest, ruff, artifact budget), so a green settle predicts a green CI.
TIER_ORDER: dict[str, int] = {"fast": 0, "routine": 1, "full": 2, "release": 3}
DEFAULT_COMMIT_MESSAGE = "Settle pending payload changes"
CONTROL_TAIL_SUFFIX = " (control tail)"

# Contract note: the settle contract named "code/orchestrators/artifact_budget.py
# --check", but the gate lives in code/src/ and takes no flags (see
# docs/operations/asset-strategy-adr.md); running the nonexistent literal would
# fail the fast tier unconditionally.
_FAST_STEPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (
        "sitemap --check",
        ("uv", "run", "--no-sync", "python3", "code/orchestrators/build_sitemap.py", "--check"),
    ),
    (
        "artifact budget",
        ("uv", "run", "--no-sync", "python3", "code/src/artifact_budget.py"),
    ),
    (
        "ruff lint",
        ("uv", "run", "--group", "lint", "ruff", "check", "code"),
    ),
)
_PYTEST_STEP = (
    "pytest (code/tests)",
    ("uv", "run", "--no-sync", "python3", "-m", "pytest", "code/tests", "-q"),
)
_VALIDATE_STANDARD_STEP = (
    "validate_repo (standard)",
    ("uv", "run", "--no-sync", "python3", "code/orchestrators/validate_repo.py"),
)
_FULL_STEPS = _FAST_STEPS + (_PYTEST_STEP, _VALIDATE_STANDARD_STEP)
# Routine is the lighter contract: the fast floor plus standard validation —
# no pytest (unless code/test paths are dirty vs HEAD, in which case the
# battery is exactly full's), no binder-chain work, no release step.  data/
# and other site changes never raise routine to full (see battery_for_tier).
_ROUTINE_STEPS = _FAST_STEPS + (_VALIDATE_STANDARD_STEP,)
_CODE_DIRTY_PREFIXES = ("code/src/", "code/orchestrators/", "code/tests/")


def _release_step() -> tuple[str, tuple[str, ...]]:
    """Build the release confirmation step, binding an attestation when one exists.

    ``validate_repo.py --release`` refuses a dirty worktree and demands
    ``--deployment-attestation`` (validate_release_evidence), so the release
    tier is a post-landing confirmation pass.  The conventional receipt path is
    ``reports/deployment-attestations/<HEAD>.json`` (release-integrity.md);
    without one the step fails closed with validate_repo's own message.
    Built lazily so ``--help`` stays subprocess-free.
    """
    command = [
        "uv",
        "run",
        "--no-sync",
        "python3",
        "code/orchestrators/validate_repo.py",
        "--release",
        "--strict-reports",
    ]
    head = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if head.returncode == 0:
        attestation = Path("reports/deployment-attestations") / f"{head.stdout.strip()}.json"
        if attestation.is_file():
            command += ["--deployment-attestation", attestation.as_posix()]
    return ("validate_repo --release --strict-reports", tuple(command))


def battery_for_tier(
    tier: str, dirty: Iterable[str] | None = None
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Return the ordered battery for *tier*; release extends full.

    ``routine`` composes from the dirty-path set: the pytest step joins only
    when a path under ``code/src``, ``code/orchestrators``, or ``code/tests``
    is dirty vs HEAD (untracked files included), so a pure data/docs/report
    settle skips the suite; data/ changes never raise routine to full.  The
    code-dirty composition is full's battery (same ordering); passing
    ``dirty=None`` for routine fails closed rather than guessing the set.
    """
    if tier == "routine":
        if dirty is None:
            raise ValueError("battery_for_tier('routine') requires the dirty-path set")
        if any(path.startswith(_CODE_DIRTY_PREFIXES) for path in dirty):
            return _FULL_STEPS
        return _ROUTINE_STEPS
    if tier == "release":
        return _FULL_STEPS + (_release_step(),)
    return _FAST_STEPS if tier == "fast" else _FULL_STEPS


def dirty_paths() -> list[str]:
    """Return every dirty path (staged, unstaged, untracked), repo-relative.

    ``-z`` keeps literal paths with NUL separators; rename/copy entries carry
    the original path as a second NUL-separated field, which is skipped.
    """
    result = subprocess.run(
        ["git", "status", "--porcelain", "-z"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"git status failed: {result.stderr.strip()}")
    paths: list[str] = []
    fields = result.stdout.split("\0")
    index = 0
    while index < len(fields):
        entry = fields[index]
        index += 1
        if len(entry) < 4:
            continue  # trailing NUL or malformed entry
        paths.append(entry[3:])
        if entry[0] in "RC":
            index += 1  # rename/copy: next field is the original path
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tier",
        choices=sorted(TIER_ORDER),
        default="fast",
        help="Minimum battery tier; dirty paths may raise it, never lower it"
        " (routine is sticky: never raised by dirty paths; default: fast).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the plan only: no checks, commits, push, or pull request.",
    )
    parser.add_argument(
        "--commit-message",
        help="Payload commit message; the control tail appends ' (control tail)'.",
    )
    parser.add_argument(
        "--push",
        action="store_true",
        help="Push HEAD to origin after the commit chain.",
    )
    parser.add_argument(
        "--pr",
        metavar="TITLE",
        help="Create (never merge) a pull request with this title; requires --push.",
    )
    parser.add_argument(
        "--skip-commit",
        action="store_true",
        help="Run the battery but land no commits.",
    )
    args = parser.parse_args()
    if args.pr and not args.push:
        parser.error("--pr requires --push: a pull request needs a pushed branch")
    return args


def resolve_tier(requested: str, derived: frozenset[str]) -> str:
    """Return the stronger of the requested tier and the path-derived tiers.

    ``routine`` is sticky: it is an explicitly requested lighter contract, so
    path-derived raises (``data/`` and other site surfaces normally adding
    ``full``) are ignored — the routine battery never becomes the full one.
    """
    if requested == "routine":
        return "routine"
    known = [requested, *(tier for tier in derived if tier in TIER_ORDER)]
    return max(known, key=TIER_ORDER.__getitem__)


def _tail(text: str, limit: int = 20) -> str:
    kept = [line for line in text.splitlines() if line.strip()]
    return "\n".join(kept[-limit:]) or "(no output)"


def run_battery(tier: str, dirty: Iterable[str]) -> bool:
    """Run the tier battery in order; stop at the first failure."""
    steps = battery_for_tier(tier, dirty)
    for index, (name, cmd) in enumerate(steps, start=1):
        print(f"[{index}/{len(steps)}] {name} ... ", end="", flush=True)
        result = subprocess.run(
            list(cmd), cwd=REPO_ROOT, capture_output=True, text=True, check=False
        )
        if result.returncode == 0:
            print("OK")
            continue
        print("FAIL")
        if result.stdout.strip():
            print("--- stdout (tail) ---\n" + _tail(result.stdout))
        if result.stderr.strip():
            print("--- stderr (tail) ---\n" + _tail(result.stderr))
        return False
    higher = sorted(
        (name for name in TIER_ORDER if TIER_ORDER[name] > TIER_ORDER[tier]),
        key=TIER_ORDER.__getitem__,
    )
    if higher:
        print(f"skipped higher-tier checks ({', '.join(higher)}): effective tier is {tier}")
    return True


def commit_paths(paths: list[str], message: str, label: str) -> bool:
    """Stage exactly *paths* and commit with *message*; signpost progress."""
    print(f"commit {label}: staging {len(paths)} path(s) for {message!r}")
    staged = subprocess.run(
        ["git", "add", "--", *paths], cwd=REPO_ROOT, capture_output=True, text=True, check=False
    )
    if staged.returncode != 0:
        print(f"commit {label} ... FAIL (git add)")
        print(_tail(staged.stderr or staged.stdout))
        return False
    committed = subprocess.run(
        ["git", "commit", "-m", message], cwd=REPO_ROOT, capture_output=True, text=True, check=False
    )
    if committed.returncode != 0:
        print(f"commit {label} ... FAIL (git commit)")
        print(_tail((committed.stdout or "") + (committed.stderr or "")))
        return False
    summary = committed.stdout.strip().splitlines() or committed.stderr.strip().splitlines()
    print(f"commit {label} ... OK" + (f": {summary[0]}" if summary else ""))
    return True


def push_head() -> bool:
    print("push: git push -u origin HEAD ... ", end="", flush=True)
    result = subprocess.run(
        ["git", "push", "-u", "origin", "HEAD"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("FAIL")
        print(_tail(result.stderr or result.stdout))
        return False
    print("OK")
    return True


def create_pr(title: str, tier: str, checks: int) -> bool:
    body = (
        f"Settle run via code/orchestrators/settle.py: effective tier `{tier}`, "
        f"battery passed ({checks} checks). Payload and control-tail commits are "
        "split per CONTROL_FILES semantics. Merging is a human/CI decision."
    )
    print(f"pull request: gh pr create --title {title!r} ... ", end="", flush=True)
    result = subprocess.run(
        ["gh", "pr", "create", "--title", title, "--body", body],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("FAIL")
        print(_tail(result.stderr or result.stdout))
        return False
    print("OK")
    if result.stdout.strip():
        print(result.stdout.strip())
    return True


def print_plan(
    args: argparse.Namespace, classification: Classification, tier: str, dirty: Iterable[str]
) -> None:
    """Print the settle plan without executing anything."""
    steps = battery_for_tier(tier, dirty)
    print(f"battery ({tier}, {len(steps)} checks, stop on first failure):")
    for index, (name, cmd) in enumerate(steps, start=1):
        print(f"  [{index}/{len(steps)}] {name}: {' '.join(cmd)}")
    message = args.commit_message or DEFAULT_COMMIT_MESSAGE
    print("commits:")
    if args.skip_commit:
        print("  skipped (--skip-commit)")
    else:
        if classification.payload_paths:
            print(f"  payload commit: git commit -m {message!r}")
            for path in classification.payload_paths:
                print(f"    - {path}")
        else:
            print("  payload commit: skipped (no payload paths)")
        if classification.control_paths:
            print(f"  control-tail commit: git commit -m {(message + CONTROL_TAIL_SUFFIX)!r}")
            for path in classification.control_paths:
                print(f"    - {path}")
        else:
            print("  control-tail commit: skipped (no control paths)")
    print("push: " + ("git push -u origin HEAD" if args.push else "skipped (--push not given)"))
    print(
        "pull request: "
        + (f"gh pr create --title {args.pr!r}" if args.pr else "skipped (--pr not given)")
    )
    print("dry-run: nothing was executed")


def main() -> None:
    args = parse_args()
    paths = dirty_paths()
    classification = classify_paths(paths)
    payload = list(classification.payload_paths)
    control = list(classification.control_paths)
    print(f"dirty paths: {len(paths)} ({len(payload)} payload, {len(control)} control)")
    leftovers = sorted(set(paths) - set(payload) - set(control))
    if leftovers:
        print("left uncommitted (classified into neither commit phase): " + ", ".join(leftovers))
    tier = resolve_tier(args.tier, classification.tiers)
    derived = sorted(t for t in classification.tiers if t in TIER_ORDER)
    decision = (
        f"tier decision: requested={args.tier} path-derived={'+'.join(derived) or 'none'}"
        f" -> effective={tier}"
    )
    if args.tier == "routine" and derived:
        decision += " (routine is sticky: path-derived raises are ignored)"
    print(decision)
    if args.dry_run:
        print_plan(args, classification, tier, paths)
        return
    if not run_battery(tier, paths):
        raise SystemExit(1)
    if args.skip_commit:
        print("commit chain skipped (--skip-commit)")
    else:
        if payload:
            if not commit_paths(payload, args.commit_message or DEFAULT_COMMIT_MESSAGE, "payload"):
                raise SystemExit(1)
        else:
            print("payload commit skipped (no payload paths)")
        if control:
            tail_message = (args.commit_message or DEFAULT_COMMIT_MESSAGE) + CONTROL_TAIL_SUFFIX
            if not commit_paths(control, tail_message, "control tail"):
                raise SystemExit(1)
        else:
            print("control-tail commit skipped (no control paths)")
    if args.push and not push_head():
        raise SystemExit(1)
    if args.pr and not create_pr(args.pr, tier, len(battery_for_tier(tier, paths))):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
