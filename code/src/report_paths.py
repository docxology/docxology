#!/usr/bin/env python3
"""Small shared helpers for date-stamped report artifacts."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Optional

from release_evidence import is_ephemeral_release_evidence_path

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = REPO_ROOT / "reports"


def _sorted_path_list(paths: list[Path]) -> list[Path]:
    return sorted(paths, key=lambda p: p.name, reverse=True)


def report_date_string() -> str:
    """Return today's UTC YYYY-MM-DD date string."""
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).date().isoformat()


def generated_timestamp() -> str:
    """Return an ISO-8601 UTC timestamp for generated JSON payloads."""
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def source_commit(repo_root: Path = REPO_ROOT) -> str:
    """Return the exact revision exercised by a dated report.

    Release validation intentionally rejects ``unknown`` values.  Keeping the
    fallback makes normal local diagnostics usable outside a Git checkout while
    preserving a truthful provenance boundary for release claims.
    """
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def _porcelain_paths(repo_root: Path) -> list[str] | None:
    """Return every changed path from NUL-delimited porcelain output.

    Human-readable porcelain output quotes unusual filenames and changes the
    shape of rename records.  Release evidence must not turn either behaviour
    into an accidental allow-list bypass, so use the documented NUL form and
    retain both sides of a rename/copy.
    """
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    records = result.stdout.split(b"\0")
    paths: list[str] = []
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        if len(record) < 4 or record[2:3] != b" ":
            return None
        status = record[:2].decode("ascii", errors="strict")
        paths.append(os.fsdecode(record[3:]))
        if "R" in status or "C" in status:
            if index >= len(records) or not records[index]:
                return None
            paths.append(os.fsdecode(records[index]))
            index += 1
    return paths


def source_worktree_state(repo_root: Path = REPO_ROOT) -> dict[str, object]:
    """Describe whether release *source* was clean when a report was made.

    Only narrowly declared post-commit evidence and the transient local Pages
    projection do not alter release source. Every other tracked or untracked
    path, including hand-authored or unrecognized report files, does. A source
    tree hash accompanies the assertion so a release validator can bind a
    clean capture to the candidate commit's exact Git tree.
    """
    paths = _porcelain_paths(repo_root)
    if paths is None:
        return {
            "source_worktree_clean": False,
            "source_worktree_dirty_paths": ["<git-status-unavailable>"],
            "source_tree_sha": "unknown",
        }
    source_paths: list[str] = []
    for path in paths:
        # Backslashes are valid POSIX filename bytes but never valid release
        # paths.  Do not silently normalize them into an evidence exemption.
        if "\\" in path:
            source_paths.append(path)
            continue
        if path == "_site" or path.startswith("_site/"):
            continue
        if is_ephemeral_release_evidence_path(path):
            continue
        source_paths.append(path)
    tree = subprocess.run(
        ["git", "rev-parse", "HEAD^{tree}"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    return {
        "source_worktree_clean": not source_paths,
        "source_worktree_dirty_paths": source_paths,
        "source_tree_sha": tree.stdout.strip() if tree.returncode == 0 else "unknown",
    }


def stable_generated_at(path: Path, payload: dict) -> str | None:
    """Reuse a timestamp when a generated JSON payload body is unchanged."""
    if not path.exists():
        return None
    try:
        existing = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(existing, dict) or not isinstance(payload, dict):
        return None
    current_body = {key: value for key, value in payload.items() if key != "generated_at"}
    existing_body = {key: value for key, value in existing.items() if key != "generated_at"}
    timestamp = existing.get("generated_at")
    return str(timestamp) if current_body == existing_body and timestamp else None


def latest_report(pattern: str, *, required: bool = True) -> Path | None:
    """Resolve latest matching report file by glob pattern.

    Args:
        pattern: A glob pattern rooted in reports/, for example
            ``"public_source_snapshot_*.json"``.
        required: If True, raise ``FileNotFoundError`` when no match exists.
    """
    matches = _sorted_path_list(list(REPORT_DIR.glob(pattern)))
    if matches:
        return matches[0]
    if not required:
        return None
    raise FileNotFoundError(f"No reports match: {REPORT_DIR / pattern}")


def dated_report_path(prefix: str, suffix: str) -> Path:
    """Build a report output path for today's date."""
    if not suffix.startswith("."):
        suffix = f".{suffix}"
    return REPORT_DIR / f"{prefix}_{report_date_string()}{suffix}"


def dated_report_dir(prefix: str) -> Path:
    """Build a date-stamped report directory path under reports/."""
    return REPORT_DIR / prefix / report_date_string()


def latest_subdir_file(prefix: str, filename: str, *, required: bool = True) -> Path | None:
    """Resolve the newest date-stamped report directory and return a child file.

    Args:
        prefix: Directory prefix under reports (for example, ``browser-smoke``).
        filename: Child file name, such as ``manifest.json``.
    """
    nested_root = REPORT_DIR / prefix
    if nested_root.is_dir():
        candidates = sorted([p for p in nested_root.iterdir() if p.is_dir()], key=lambda p: p.name, reverse=True)
    else:
        candidates = sorted(
            [p for p in REPORT_DIR.glob(f"{prefix}_*/") if p.is_dir() and p.name.startswith(prefix)],
            key=lambda p: p.name,
            reverse=True,
        )
    candidates = [p for p in candidates if (p / filename).exists()]
    if not candidates:
        if not required:
            return None
        raise FileNotFoundError(f"No report directories match: {REPORT_DIR / (prefix + '_*')}")
    return candidates[0] / filename


def repo_path(path_like: str | Path) -> Path:
    """Return an absolute repository path for a relative path-like value."""
    path = Path(path_like)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def rel(path: Path) -> str:
    """Return a POSIX repository-relative path."""
    return path.relative_to(REPO_ROOT).as_posix()


def default_latest_file(*paths: Path) -> Optional[Path]:
    """Return the first existing path from the given list.

    Useful for backward-compatible checks against multiple legacy report names.
    """
    for path in paths:
        if path.exists():
            return path
    return None
