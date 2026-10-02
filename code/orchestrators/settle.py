#!/usr/bin/env python3
"""Settle dirty work: classify changes, run the tiered battery, land the commits."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
from collections.abc import Iterable
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]
from docxology_tools.change_classifier import Classification, classify_paths  # noqa: E402

from docxology_tools.release_controls import is_control_path  # noqa: E402
# Replaces the manual sequence: payload commit, control-tail commit, then the
# gate cascade by hand (docs/operations/settle.md).  Commits are split per the
# release_controls.is_control_path semantics encoded in
# change_classifier.classify_paths.  The full tier runs the same four checks
# as the validate job of .github/workflows/validate.yml (validate_repo.py,
# pytest, ruff, artifact budget), so a green settle predicts a green CI.
TIER_ORDER: dict[str, int] = {"fast": 0, "routine": 1, "full": 2, "release": 3}
DEFAULT_COMMIT_MESSAGE = "Settle pending payload changes"
CONTROL_TAIL_SUFFIX = " (control tail)"
MAX_BINDER_PASSES = 4
_LOCAL_PYTHON = ("uv", "run", "--no-sync", "python3")
_BINDER_WRITERS = (
    ("Pages manifest", "build_pages_artifact.py", ("--write-manifest", "--check-size-only")),
    ("generated manifest", "build_generated_manifest.py", ()),
    ("agent index", "build_agent_index.py", ()),
    ("release integrity", "build_release_integrity.py", ()),
    ("final generated manifest", "build_generated_manifest.py", ()),
)
_BINDER_CHECKS = (
    ("Pages manifest", "build_pages_artifact.py", ("--check-size-only", "--check-manifest")),
    ("generated manifest", "build_generated_manifest.py", ("--check",)),
    ("agent index", "build_agent_index.py", ("--check",)),
    ("release integrity", "build_release_integrity.py", ("--check",)),
)
_REVIEW_INPUT_FLAGS = {
    "public_source_snapshot": "--snapshot",
    "previous_public_source_snapshot": "--previous-snapshot",
    "public_source_inventory": "--inventory",
    "paired_publications": "--paired-publications",
    "paired_publication_decisions": "--pair-decisions",
    "doi_role_review": "--doi-review",
    "repository_classification": "--repository-classification",
    "claims_ledger": "--claims",
    "public_source_observation_decisions": "--observation-decisions",
    "biographical_claim_decisions": "--biographical-claim-decisions",
    "scholar_snapshot": "--scholar-snapshot",
    "scholar_verification_receipt": "--scholar-verification-receipt",
}

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
# Routine is the lighter contract for control-only landings and clean-tree
# checks: the fast floor plus standard validation — no pytest or release step.
# Binder work belongs to the landing phase, after this battery.
# Any payload-dirty path raises the TIER to full
# (resolve_tier), because every payload commit moves the payload anchor the
# Pages deploy re-validates via the binder manifest.  battery_for_tier
# enforces that precondition fail-closed for direct API callers.
_ROUTINE_STEPS = _FAST_STEPS + (_VALIDATE_STANDARD_STEP,)


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

    ``routine`` is the control-only/clean-tree contract: the fast floor plus
    standard validation, never pytest (a payload-dirty tree never reaches this
    branch — resolve_tier raises it to ``full``, which runs the suite), never
    the release step. Passing ``dirty=None`` for
    routine fails closed rather than guessing the set, and any dirty path that
    is not control-classified (per ``release_controls.is_control_path``) also
    fails closed: the Pages deploy re-checks the binder manifest, which every
    payload commit stales, so a payload change must ride the full tier.
    """
    if tier == "routine":
        if dirty is None:
            raise ValueError("battery_for_tier('routine') requires the dirty-path set")
        if any(not is_control_path(Path(path)) for path in dirty):
            raise ValueError(
                "routine battery requires a payload-clean tree; resolve_tier raises "
                "payload-dirty work to 'full' (the Pages deploy re-checks the binder "
                "manifest, which any payload commit stales)"
            )
        return _ROUTINE_STEPS
    if tier == "release":
        return _FULL_STEPS + (_release_step(),)
    return _FAST_STEPS if tier == "fast" else _FULL_STEPS


def dirty_paths() -> list[str]:
    """Return every dirty path (staged, unstaged, untracked), repo-relative.

    ``-z`` keeps literal paths with NUL separators; rename/copy entries carry
    the original path as a second NUL-separated field. A rename includes
    both paths so its source deletion cannot escape the scoped commit.
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
        if "R" in entry[:2] or "C" in entry[:2]:
            if index >= len(fields) or not fields[index]:
                raise SystemExit("git status returned an incomplete rename/copy entry")
            if "R" in entry[:2]:
                paths.append(fields[index])
            index += 1  # a copied source remains unchanged
    return sorted(set(paths))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tier",
        choices=sorted(TIER_ORDER),
        default="fast",
        help="Minimum battery tier; dirty paths may raise it, never lower it"
        " (routine rises to full for payload changes; default: fast).",
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


def resolve_tier(
    requested: str, derived: Iterable[str], payload_dirty: bool = False
) -> str:
    """Return the effective tier for the requested floor.

    ``routine`` stays routine only for control-only landings and clean-tree
    checks.  Any payload-dirty path raises it to ``full`` — a correctness
    raise, not a convenience one: every payload commit moves the payload
    anchor the Pages deploy re-validates (``build_pages_artifact.py
    --check-manifest`` in the pages.yml deploy job), so a stale binder
    manifest would turn the deploy red.  The path-derived *convenience*
    raises in ``derived`` stay ignored for routine.
    """
    if requested == "routine":
        return "full" if payload_dirty else "routine"
    known = [requested, *(tier for tier in derived if tier in TIER_ORDER)]
    return max(known, key=TIER_ORDER.__getitem__)


def _tail(text: str, limit: int = 20) -> str:
    kept = [line for line in text.splitlines() if line.strip()]
    return "\n".join(kept[-limit:]) or "(no output)"


def run_steps(steps: Iterable[tuple[str, tuple[str, ...]]]) -> bool:
    """Run local commands in order, retaining diagnostics on failure."""
    steps = tuple(steps)
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
    return True


def run_battery(tier: str, dirty: Iterable[str]) -> bool:
    """Run the tier battery in order; stop at the first failure."""
    if not run_steps(battery_for_tier(tier, dirty)):
        return False
    higher = sorted(
        (name for name in TIER_ORDER if TIER_ORDER[name] > TIER_ORDER[tier]),
        key=TIER_ORDER.__getitem__,
    )
    if higher:
        print(f"skipped higher-tier checks ({', '.join(higher)}): effective tier is {tier}")
    return True


def _git_paths(*args: str) -> set[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", *args], cwd=REPO_ROOT,
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise SystemExit(f"git ls-files failed: {result.stderr.strip()}")
    return set(filter(None, result.stdout.split("\0")))


def _head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "HEAD"], cwd=REPO_ROOT,
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise SystemExit(f"git HEAD lookup failed: {result.stderr.strip()}")
    return result.stdout.strip()


def _same_head(expected: str) -> bool:
    if _head() != expected:
        print("settle refused: HEAD changed concurrently; review the new commit before continuing")
        return False
    return True


def stage_paths(paths: Iterable[str]) -> bool:
    """Stage selected paths without dropping staged deletions or renames.

    A rename source already removed from the index is still a commit path,
    but ``git add`` rejects it. Leave that staged deletion alone. Literal
    pathspecs also protect filenames containing Git wildcard syntax.
    """
    indexed = _git_paths("--cached")
    stageable = sorted(
        path for path in set(paths)
        if path in indexed or os.path.lexists(REPO_ROOT / path)
    )
    if not stageable:
        return True
    try:
        for name in stageable:
            _safe_local_file(REPO_ROOT / name, required=False)
    except (OSError, ValueError) as exc:
        print(f"staging refused: {exc}")
        return False
    staged = subprocess.run(
        ["git", "--literal-pathspecs", "add", "--all", "--", *stageable],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    )
    if staged.returncode:
        print("staging selected paths ... FAIL")
        print(_tail(staged.stderr or staged.stdout))
        return False
    return True


def commit_paths(paths: list[str], message: str, label: str) -> bool:
    """Commit only selected worktree paths, preserving other staged changes."""
    print(f"commit {label}: staging {len(paths)} path(s) for {message!r}")
    if not stage_paths(paths):
        return False
    committed = subprocess.run(
        ["git", "--literal-pathspecs", "commit", "--only", "-m", message, "--", *paths],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    )
    if committed.returncode != 0:
        print(f"commit {label} ... FAIL (git commit)")
        print(_tail((committed.stdout or "") + (committed.stderr or "")))
        return False
    summary = committed.stdout.strip().splitlines() or committed.stderr.strip().splitlines()
    print(f"commit {label} ... OK" + (f": {summary[0]}" if summary else ""))
    return True


def _path_state(paths: Iterable[str]) -> dict[str, str]:
    """Bind convergence and concurrent-edit guards to bytes and file kind."""
    state = {}
    for name in sorted(set(paths)):
        path = REPO_ROOT / name
        try:
            _safe_local_file(path, required=False)
        except (OSError, ValueError) as exc:
            raise SystemExit(f"settle custody refused: {exc}") from None
        if path.is_file():
            content = str(path.stat().st_mode).encode() + b"\0" + path.read_bytes()
        elif not path.exists():
            content = b"deleted"
        else:
            raise SystemExit(f"cannot settle a directory/submodule path automatically: {name}")
        state[name] = hashlib.sha256(content).hexdigest()
    return state


def _control_state() -> dict[str, str]:
    paths = _git_paths("--cached", "--others", "--exclude-standard") | set(dirty_paths())
    return _path_state(path for path in paths if is_control_path(Path(path)))


def _payload_clean() -> bool:
    payload = [path for path in dirty_paths() if not is_control_path(Path(path))]
    if payload:
        print("binder landing refused: payload paths changed; preserve and review them:")
        print("\n".join(f"  - {path}" for path in payload))
        return False
    return True


def _safe_local_file(path: Path, *, required: bool) -> Path:
    """Check lexical custody before reading or preparing an atomic output.

    Resolving beneath the checkout is insufficient: an internal link can
    target an ignored private file. Existing leaf files must be regular and
    single-link; ancestors must be real directories. A missing output/deletion path
    is permitted, but linked output/temp siblings are never followed.
    """
    relative = path.relative_to(REPO_ROOT)
    if not relative.parts or ".." in relative.parts:
        raise ValueError("unsafe settle source/control path")
    cursor = REPO_ROOT
    for index, part in enumerate(relative.parts):
        cursor = cursor / part
        leaf = index == len(relative.parts) - 1
        try:
            metadata = cursor.lstat()
        except FileNotFoundError:
            if not required:
                return path
            raise ValueError(f"missing settle source/control path: {relative}") from None
        if stat.S_ISLNK(metadata.st_mode):
            raise ValueError(f"symlinked settle source/control path: {relative}")
        if leaf:
            if not stat.S_ISREG(metadata.st_mode):
                raise ValueError(f"non-file settle source/control path: {relative}")
            if metadata.st_nlink != 1:
                raise ValueError(f"hard-linked settle source/control path: {relative}")
        elif not stat.S_ISDIR(metadata.st_mode):
            raise ValueError(f"non-directory settle source/control ancestor: {relative}")
    return path


def _review_writer() -> tuple[str, str, tuple[str, ...]]:
    """Rebind the existing review without choosing new dates or input paths.

    CLI defaults can change comparison baselines or refresh-failure context.
    Only complete recorded local inputs are safe for this automatic replay;
    unusual/custom reports remain a deliberate manual review operation.
    """
    reports = sorted(
        path for path in (REPO_ROOT / "reports").glob("public_source_review_*.json")
        if is_control_path(path.relative_to(REPO_ROOT))
    )
    if not reports:
        raise ValueError("missing dated public-source review; render it explicitly before settling")
    report = reports[-1]
    _safe_local_file(report, required=True)
    markdown = report.with_suffix(".md")
    # The renderer writes predictable sibling .tmp files before os.replace.
    # Validate both output pairs and their temp names before even reading the
    # existing report, not after a linked private file has entered memory.
    for output in (report, markdown):
        _safe_local_file(output, required=output == report)
        _safe_local_file(output.with_name(output.name + ".tmp"), required=False)
    payload = json.loads(report.read_text(encoding="utf-8"))
    date = report.name.removeprefix("public_source_review_").removesuffix(".json")
    if not isinstance(payload, dict) or payload.get("date") != date:
        raise ValueError("public-source review date does not match its dated filename")
    inputs = payload.get("inputs")
    context = payload.get("refresh_context")
    if not isinstance(inputs, dict) or not isinstance(context, dict):
        raise ValueError("public-source review lacks recorded inputs/refresh context")
    if set(inputs) != set(_REVIEW_INPUT_FLAGS):
        raise ValueError("public-source review input schema changed; review its replay explicitly")
    indexed = _git_paths("--cached")
    args = ["--report", report.relative_to(REPO_ROOT).as_posix(), "--date", date]
    for name, flag in _REVIEW_INPUT_FLAGS.items():
        provenance = inputs[name]
        raw = provenance.get("path") if isinstance(provenance, dict) else None
        if not isinstance(raw, str) or not raw or "\\" in raw:
            raise ValueError(f"cannot replay absent/invalid review input {name}; render it explicitly")
        path = Path(raw)
        if (not path.parts or path.is_absolute() or raw != path.as_posix() or ".." in path.parts
                or path.parts[0] not in {"data", "reports"} or path.suffix != ".json"
                or raw not in indexed):
            raise ValueError(f"review input {name} is not a tracked local JSON path")
        _safe_local_file(REPO_ROOT / path, required=True)
        args.extend((flag, raw))
    status = context.get("pairing_refresh_status")
    note = context.get("pairing_refresh_note")
    if not isinstance(status, str) or status not in {"auto", "failed"} or not isinstance(note, str):
        raise ValueError("invalid recorded pairing refresh context")
    args.extend(("--pairing-refresh-status", status, f"--pairing-refresh-note={note}"))
    return "public-source review (recorded inputs)", "build_public_source_review.py", tuple(args)


def refresh_review() -> bool:
    """Prepare the recorded review for the pre-landing dirty-tree check."""
    try:
        name, script, args = _review_writer()
    except (OSError, ValueError) as exc:
        print(f"review replay refused: {exc}")
        return False
    return run_steps(((name, (*_LOCAL_PYTHON, f"code/orchestrators/{script}", *args)),))


def rebind_controls(*, max_passes: int = MAX_BINDER_PASSES) -> bool:
    """Refresh control writers to a bounded byte fixed point after landing.

    Each writer's recognized controls are staged before its consumers run:
    latest_source_report deliberately discovers only index-tracked receipts.
    Consumer pointer changes can alter report retention on the next pass.
    Payload writes abort rather than entering another automatic commit.
    """
    if not _payload_clean():
        return False
    head = _head()
    try:
        review_writer = _review_writer()
    except (OSError, ValueError) as exc:
        print(f"binder landing refused: {exc}")
        return False
    if not stage_paths(path for path in dirty_paths() if is_control_path(Path(path))):
        return False
    previous = _control_state()
    changed = []
    for iteration in range(1, max_passes + 1):
        print(f"binder pass {iteration}/{max_passes}")
        for name, script, args in (review_writer, *_BINDER_WRITERS):
            if not _same_head(head) or not _payload_clean():
                return False
            if script == "build_public_source_review.py":
                try:
                    if _review_writer() != review_writer:
                        raise ValueError("recorded public-source review inputs changed during landing")
                except (OSError, ValueError) as exc:
                    print(f"binder landing refused: {exc}")
                    return False
            if not run_steps(((name, (*_LOCAL_PYTHON, f"code/orchestrators/{script}", *args)),)):
                return False
            if not _same_head(head) or not _payload_clean():
                return False
            if not stage_paths(path for path in dirty_paths() if is_control_path(Path(path))):
                return False
        current = _control_state()
        changed = sorted(path for path in current.keys() | previous.keys()
                         if current.get(path) != previous.get(path))
        if not changed:
            print(f"binder controls converged after {iteration} pass(es)")
            try:
                if _review_writer() != review_writer:
                    raise ValueError("recorded public-source review inputs changed before checks")
            except (OSError, ValueError) as exc:
                print(f"binder landing refused: {exc}")
                return False
            name, script, args = review_writer
            checks = ((name + " --check", (*_LOCAL_PYTHON, f"code/orchestrators/{script}", *args, "--check")),)
            checked = run_steps((*checks, *(
                (name + " --check", (*_LOCAL_PYTHON, f"code/orchestrators/{script}", *args))
                for name, script, args in _BINDER_CHECKS
            )))
            return checked and _same_head(head) and _payload_clean()
        print("binder controls changed: " + ", ".join(changed))
        previous = current
    print(f"binder controls did not converge within {max_passes} passes; no control commit or push")
    print("remaining changes: " + ", ".join(changed))
    return False


def validate_landing() -> bool:
    """Check the landed tree against its new commit before publication."""
    if dirty_paths():
        print("post-landing validation refused: worktree still has pending changes")
        return False
    head = _head()
    name, script, args = _BINDER_CHECKS[0]
    checked = run_steps((
        (name + " (landed)", (*_LOCAL_PYTHON, f"code/orchestrators/{script}", *args)),
        _VALIDATE_STANDARD_STEP,
    ))
    if not checked or not _same_head(head):
        return False
    pending = dirty_paths()
    if pending:
        print("settle refused: paths changed during post-landing validation: " + ", ".join(pending))
        return False
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
    if not args.skip_commit and (classification.payload_paths or classification.control_paths):
        print("preflight: replay existing public-source review with its recorded inputs")
    print(f"battery ({tier}, {len(steps)} checks, stop on first failure):")
    for index, (name, cmd) in enumerate(steps, start=1):
        print(f"  [{index}/{len(steps)}] {name}: {' '.join(cmd)}")
    message = args.commit_message or DEFAULT_COMMIT_MESSAGE
    print("commits:")
    if args.skip_commit:
        print("  skipped (--skip-commit)")
    else:
        if classification.payload_paths:
            print(f"  payload commit: git commit --only -m {message!r} -- <payload paths>")
            for path in classification.payload_paths:
                print(f"    - {path}")
        else:
            print("  payload commit: skipped (no payload paths)")
        if classification.payload_paths or classification.control_paths:
            print(f"  binder writers: converge controls in at most {MAX_BINDER_PASSES} passes")
            print("  stage recognized controls after each writer; refuse payload drift")
            print(f"  control-tail commit: git commit --only -m {(message + CONTROL_TAIL_SUFFIX)!r} -- <fresh control paths>")
            for path in classification.control_paths:
                print(f"    - {path}")
        else:
            print("  control-tail commit: skipped (no control paths)")
        print("  confirm landed Pages manifest and standard validation before push")
    if args.skip_commit and args.push:
        print("  push requires a clean tree and fresh post-landing validation")
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
    payload_dirty = any(not is_control_path(Path(path)) for path in paths)
    tier = resolve_tier(args.tier, classification.tiers, payload_dirty)
    derived = sorted(t for t in classification.tiers if t in TIER_ORDER)
    decision = (
        f"tier decision: requested={args.tier} path-derived={'+'.join(derived) or 'none'}"
        f" -> effective={tier}"
    )
    if args.tier == "routine":
        decision += (
            " (payload paths dirty: raised to full — the Pages deploy re-checks"
            " the binder manifest, which any payload commit stales)"
            if tier == "full"
            else " (routine: control-only or clean tree)"
        )
    print(decision)
    if args.dry_run:
        print_plan(args, classification, tier, paths)
        return
    payload_before = _path_state(payload)
    head_before = _head()
    if not args.skip_commit and (payload or control):
        if not refresh_review():
            raise SystemExit(1)
        current_payload = [path for path in dirty_paths() if not is_control_path(Path(path))]
        if not _same_head(head_before) or _path_state(current_payload) != payload_before:
            print("settle refused: payload changed during review preflight; review it and run again")
            raise SystemExit(1)
    if not run_battery(tier, paths):
        raise SystemExit(1)
    payload_after = [path for path in dirty_paths() if not is_control_path(Path(path))]
    if not _same_head(head_before) or _path_state(payload_after) != payload_before:
        print("settle refused: payload changed during the battery; review it and run again")
        raise SystemExit(1)
    if args.skip_commit:
        print("commit chain skipped (--skip-commit)")
        if args.push and not validate_landing():
            raise SystemExit(1)
    else:
        if payload:
            if not commit_paths(payload, args.commit_message or DEFAULT_COMMIT_MESSAGE, "payload"):
                raise SystemExit(1)
        else:
            print("payload commit skipped (no payload paths)")
        # Do not reuse the pre-battery list: binders can create a new dated
        # growth receipt, and index-tracked discovery needs it in this tail.
        if payload or any(is_control_path(Path(path)) for path in dirty_paths()):
            if not rebind_controls():
                raise SystemExit(1)
        control = [path for path in dirty_paths() if is_control_path(Path(path))]
        if control:
            tail_message = (args.commit_message or DEFAULT_COMMIT_MESSAGE) + CONTROL_TAIL_SUFFIX
            if not commit_paths(control, tail_message, "control tail"):
                raise SystemExit(1)
        else:
            print("control-tail commit skipped (no control paths)")
        if not validate_landing():
            raise SystemExit(1)
    if args.push and not push_head():
        raise SystemExit(1)
    if args.pr and not create_pr(args.pr, tier, len(battery_for_tier(tier, paths))):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
