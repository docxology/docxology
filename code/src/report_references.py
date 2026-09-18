"""Shared citation scan for ``reports/`` references from projected surfaces.

One deterministic scan answers "which ``reports/`` paths does the published
projection reference?" for both ``build_pages_artifact`` (superseded-report
omission protection) and ``prune_old_reports`` (dated-subdir safety net).

Citing sources are projected surfaces: ``pages/``, ``data/``, ``docs/``, root
HTML/MD/JSON/txt, and ``papers/*/metadata.json``. Excluded sources mirror
``prune_old_reports``: ``reports/`` (a set's own manifest cites its own files),
``code/`` (generators carry stale fallback-default literals), ``_site/`` (a
generated projection, not a consumer), and the inventory manifests
(``data/pages-artifact-manifest.json``, ``data/generated-manifest.json``,
``data/report-retention.json``), which enumerate paths without serving them as
live links.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPORT_PATH_PATTERN = re.compile(r"reports/[A-Za-z0-9._/-]+")

_GIT_GREP_EXCLUDES = (
    ":(exclude)reports/*",
    ":(exclude)code/*",
    ":(exclude)_site/*",
    ":(exclude)data/pages-artifact-manifest.json",
    ":(exclude)data/generated-manifest.json",
    ":(exclude)data/report-retention.json",
)

_WORKING_TREE_SUFFIXES = {".html", ".json", ".md", ".xml"}
_WORKING_TREE_SKIP_DIRS = {"reports", "code", ".git", "__pycache__", "_site"}
_WORKING_TREE_SKIP_FILES = {
    "data/pages-artifact-manifest.json",
    "data/generated-manifest.json",
    "data/report-retention.json",
}


def referenced_report_paths(repo_root: Path) -> set[str]:
    """Return ``reports/`` path tokens cited from projected surfaces.

    ``git grep`` covers tracked citing files; a working-tree scan catches
    untracked files git grep would miss. ``papers/`` is intentionally in
    scope: paper ``metadata.json`` files are projected provenance surfaces.
    """
    references = _git_grep_report_references(repo_root)
    references.update(_working_tree_report_references(repo_root))
    return references


def prefix_is_referenced(repo_root: Path, rel_prefix: str) -> bool:
    """Return whether any referenced token equals or extends ``rel_prefix``.

    A token extends the prefix when the citation names the prefix itself or a
    path beneath it, matching the prefix-containment semantics the dated-subdir
    pruner has always used.
    """
    return any(
        reference == rel_prefix or reference.startswith(rel_prefix)
        for reference in referenced_report_paths(repo_root)
    )


def _git_grep_report_references(repo_root: Path) -> set[str]:
    try:
        result = subprocess.run(
            ["git", "grep", "-ohE", REPORT_PATH_PATTERN.pattern, "--", ".", *_GIT_GREP_EXCLUDES],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return set()  # git unavailable: still honor working-tree references
    if result.returncode not in (0, 1):
        return set()
    return {token for token in result.stdout.splitlines() if token}


def _working_tree_report_references(repo_root: Path) -> set[str]:
    """Return report tokens found in working-tree text files (tracked or not).

    Skips the same trees and inventory manifests as the tracked scan: those
    enumerate report paths without serving them as live links.
    """
    references: set[str] = set()
    root = repo_root.resolve()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if any(part in _WORKING_TREE_SKIP_DIRS for part in relative.parts):
            continue
        if relative.as_posix() in _WORKING_TREE_SKIP_FILES:
            continue
        if path.suffix.lower() not in _WORKING_TREE_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        references.update(match.group(0) for match in REPORT_PATH_PATTERN.finditer(text))
    return references
