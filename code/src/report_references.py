"""Shared citation scan for ``reports/`` references from projected surfaces.

One deterministic scan answers "which ``reports/`` paths does the published
projection reference?" for both ``build_pages_artifact`` (superseded-report
omission protection) and ``prune_old_reports`` (dated-subdir safety net).

Citing sources are projected surfaces: ``pages/``, ``data/``, ``docs/``, root
HTML/MD/JSON/txt, and ``papers/*/metadata.json``. Excluded sources mirror
``prune_old_reports``: ``reports/`` (a set's own manifest cites its own files),
``code/`` (generators carry stale fallback-default literals), ``_site/`` (a
generated projection, not a consumer), ``.github/`` (CI configuration outside
the projection; ``release_controls.is_payload_neutral_path`` relies on it never
deciding the published file set), and the inventory manifests
(``data/pages-artifact-manifest.json``, ``data/generated-manifest.json``,
``data/report-retention.json``), which enumerate paths without serving them as
live links.
"""

from __future__ import annotations

import re
import stat
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

class ReferenceScanError(RuntimeError):
    """A destructive caller cannot establish complete reference protection."""


REPORT_PATH_PATTERN = re.compile(r"reports/[A-Za-z0-9._/-]+")
# These links explicitly resolve historical evidence in the repository archive,
# rather than requesting an object from the current Pages projection. Keep the
# exception repository- and commit-specific; local/relative, same-origin, and
# unpinned links continue to protect their report bytes.
_URL_TOKEN = re.compile(r"(?<![A-Za-z0-9_=:/?&%.-])(?:https?:)?//[^\s\"'<>()[\]]+")
_PINNED_ARCHIVE_PATH = re.compile(r"/docxology/docxology/(?:blob|tree)/[0-9a-f]{40}/reports/[A-Za-z0-9._/-]+")


def local_report_paths(text: str) -> set[str]:
    """Exclude direct immutable archive URLs, preserving every other token.

    Parse complete URL spans so a nested GitHub URL in another host's query
    cannot disable local citation protection for the retention service.
    """
    def archive_span(match: re.Match[str]) -> str:
        token = match.group(0)
        try:
            parsed = urlsplit(token)
        except ValueError:
            return token
        if (parsed.scheme == "https" and parsed.netloc == "github.com"
                and _PINNED_ARCHIVE_PATH.fullmatch(parsed.path)):
            return " "
        return token
    return {match.group(0) for match in REPORT_PATH_PATTERN.finditer(_URL_TOKEN.sub(archive_span, text))}


_GIT_GREP_EXCLUDES = (
    ":(exclude)reports/*",
    ":(exclude)code/*",
    ":(exclude)_site/*",
    ":(exclude).github/*",
    ":(exclude)data/pages-artifact-manifest.json",
    ":(exclude)data/generated-manifest.json",
    ":(exclude)data/report-retention.json",
)

_WORKING_TREE_SUFFIXES = {".html", ".json", ".md", ".xml", ".txt"}
_WORKING_TREE_SKIP_DIRS = {"reports", "code", ".git", ".github", "__pycache__", "_site"}
_WORKING_TREE_SKIP_FILES = {
    "data/pages-artifact-manifest.json",
    "data/generated-manifest.json",
    "data/report-retention.json",
}


def referenced_report_paths(repo_root: Path, *, strict: bool = False) -> set[str]:
    """Return ``reports/`` path tokens cited from projected surfaces.

    ``git grep`` covers tracked citing files; a working-tree scan catches
    untracked files git grep would miss. ``papers/`` is intentionally in
    scope: paper ``metadata.json`` files are projected provenance surfaces.
    ``strict=True`` refuses incomplete reader observations for destructive callers.
    """
    references = _git_grep_report_references(repo_root, strict=strict)
    references.update(_working_tree_report_references(repo_root, strict=strict))
    return references


def _git_grep_report_references(repo_root: Path, *, strict: bool = False) -> set[str]:
    try:
        result = subprocess.run(
            ["git", "grep", "-hE", REPORT_PATH_PATTERN.pattern, "--", ".", *_GIT_GREP_EXCLUDES],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        if strict:
            raise ReferenceScanError("Git reference scan failed or timed out") from exc
        return set()  # Still honor the independent working-tree reference scan.
    if result.returncode not in (0, 1):
        if strict:
            raise ReferenceScanError("Git reference scan failed")
        return set()
    return local_report_paths(result.stdout)


def _unignored_working_tree_files(root: Path, *, strict: bool = False) -> list[Path] | None:
    """Tracked plus untracked files that git does not ignore, or None without git.

    Ignored files (local tool caches, editor state, anything in ``.gitignore`` or
    ``.git/info/exclude``) never reach a clean checkout, so letting them protect a
    report would make the Pages manifest depend on one machine's local state.
    """
    try:
        result = subprocess.run(
            ["git", "ls-files", "-co", "--exclude-standard", "-z"],
            cwd=root,
            capture_output=True,
            check=False,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        if strict:
            raise ReferenceScanError("Git file inventory failed or timed out") from exc
        return None
    if result.returncode != 0:
        if strict:
            raise ReferenceScanError("Git file inventory failed")
        return None
    return [root / raw for raw in result.stdout.decode("utf-8", "surrogateescape").split("\0") if raw]


def _working_tree_report_references(repo_root: Path, *, strict: bool = False) -> set[str]:
    """Return report tokens found in working-tree text files (tracked or not).

    Skips the same trees and inventory manifests as the tracked scan: those
    enumerate report paths without serving them as live links. Git-ignored files
    are skipped too, so the result matches what a clean checkout would see.
    """
    references: set[str] = set()
    root = repo_root.resolve()
    candidates = _unignored_working_tree_files(root, strict=strict)
    for path in candidates if candidates is not None else root.rglob("*"):
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
        if strict and any(p.is_symlink() for p in (path, *path.parents)):
            raise ReferenceScanError(f"Linked reference source: {relative.as_posix()}")
        if strict:
            try:
                mode = path.lstat().st_mode
            except OSError as exc:
                raise ReferenceScanError(f"Unavailable reference source: {relative.as_posix()}") from exc
            if not stat.S_ISREG(mode):
                raise ReferenceScanError(f"Non-regular reference source: {relative.as_posix()}")
        elif not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            if strict:
                raise ReferenceScanError(f"Unreadable reference source: {relative.as_posix()}") from exc
            continue
        references.update(local_report_paths(text))
    return references
