#!/usr/bin/env python3
"""Small shared helpers for date-stamped report artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

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
