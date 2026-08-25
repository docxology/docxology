"""Shared control-tail policy for deterministic release metadata.

Some generated records necessarily describe the commit immediately before the
record itself is committed.  The Pages manifest, release-integrity envelope,
and dated public-source review are examples: treating their own control-only
commit as a new content revision would make every no-write check permanently
stale.  This module owns the deliberately narrow definition of those control
paths and the first-parent history walk used to find the last payload commit.

It is not a release-attestation shortcut.  Post-deploy evidence must continue
to bind to the exact deployed ``HEAD`` through its explicit exact-revision
mode.
"""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from datetime import date
from pathlib import Path
import re


CONTROL_FILES = frozenset(
    {
        Path("GENERATED.md"),
        Path("data/agent-index.json"),
        Path("data/generated-manifest.json"),
        Path("data/pages-artifact-manifest.json"),
        Path("data/release-integrity.json"),
    }
)

# These reports are derived control receipts, not curated content.  Keep the
# patterns rooted at ``reports/`` in ``is_control_path``; a nested path must
# never be able to impersonate a control record.
CONTROL_REPORT_PATTERNS = (
    "asset_size_*.json",
    "pages_artifact_growth_*.json",
    "public_source_review_*.json",
    "public_source_review_*.md",
)
_CONTROL_REPORT_NAME = re.compile(
    r"^(asset_size|pages_artifact_growth|public_source_review)_(\d{4}-\d{2}-\d{2})(\.json|\.md)$"
)
_CONTROL_REPORT_SUFFIXES = {
    "asset_size": {".json"},
    "pages_artifact_growth": {".json"},
    "public_source_review": {".json", ".md"},
}


def _is_control_report_name(name: str) -> bool:
    """Accept only recognized, date-stamped control receipts."""
    match = _CONTROL_REPORT_NAME.fullmatch(name)
    if match is None:
        return False
    kind, raw_date, suffix = match.groups()
    if suffix not in _CONTROL_REPORT_SUFFIXES[kind]:
        return False
    try:
        date.fromisoformat(raw_date)
    except ValueError:
        return False
    return True


def is_control_path(path: Path) -> bool:
    """Return whether a repository-relative path is control metadata.

    ``Path.match`` suffix-matches directory-containing patterns, which would
    let ``untrusted/reports/...`` evade payload provenance.  Require the exact
    top-level ``reports/`` parent before matching a control report name.
    """
    if path in CONTROL_FILES:
        return True
    return path.parent == Path("reports") and _is_control_report_name(path.name)


def latest_payload_commit(
    head: str,
    parent_for: Callable[[str], str | None],
    changed_paths_for: Callable[[str], list[Path]],
) -> str:
    """Return the latest non-control commit in a first-parent history.

    Explicit collaborators keep the decision testable with a small local
    fixture rather than coupling it to the caller's checkout.
    """
    candidate = head
    while True:
        parent = parent_for(candidate)
        if not parent:
            return candidate
        changed = changed_paths_for(candidate)
        if not all(is_control_path(path) for path in changed):
            return candidate
        candidate = parent


def _first_parent(repo_root: Path, commit: str) -> str | None:
    result = subprocess.run(
        ["git", "show", "-s", "--format=%P", commit],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    parents = result.stdout.split()
    return parents[0] if parents else None


def _changed_paths(repo_root: Path, commit: str) -> list[Path]:
    """Return first-parent diff paths, failing closed for unresolved history."""
    parent = _first_parent(repo_root, commit)
    if not parent:
        return []
    result = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", parent, commit],
        cwd=repo_root,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        return [Path(".unresolved-source-revision")]
    return [
        Path(raw)
        for raw in result.stdout.decode("utf-8", errors="surrogateescape").split("\0")
        if raw
    ]


def source_payload_commit(repo_root: Path) -> str:
    """Return the revision that last changed release payload content.

    A missing or unresolved Git checkout is represented as ``"unknown"`` so
    a normal local diagnostic can report its limitation while strict release
    validation still rejects it.
    """
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    head = result.stdout.strip() if result.returncode == 0 else "unknown"
    if head == "unknown":
        return head
    return latest_payload_commit(
        head,
        lambda commit: _first_parent(repo_root, commit),
        lambda commit: _changed_paths(repo_root, commit),
    )


def source_tree_sha(repo_root: Path, commit: str) -> str:
    """Return the exact tree for a declared source revision or ``unknown``."""
    if not commit or commit == "unknown":
        return "unknown"
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"{commit}^{{tree}}"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"
