#!/usr/bin/env python3
"""Prune superseded dated QA screenshot sets under reports/ to bound the working tree.

`visual_qa.py` and `browser_smoke.py` each write a fresh dated subdirectory of full-page
screenshots every run (`reports/visual-qa/YYYY-MM-DD/`, `reports/browser-smoke/YYYY-MM-DD/`),
and `validate_repo.py` only ever reads the LATEST set via `latest_subdir_file(...)`. The
older sets are pure history — at ~29 MB per visual-qa set they dominate the repo's tracked
size (88 MB of 100 MB at last count). Git history still retains anything pruned here, so
this only trims the checked-out tree and bounds future growth. Before an apply run, every
removal must also carry a reviewed provenance record in `data/report-retention.json`.

Scope is deliberately narrow:
  * Only the dated SCREENSHOT subdirectories are pruned. Each old `manifest.json` only
    references its own PNGs, so removing a whole dated subdir leaves no dangling link.
  * Dated JSON reports (paired_publications_*, public_source_*, asset_size_*, ...) are NOT
    pruned: they are cited as provenance from paper `metadata.json`, GENERATED.md, and the
    claims/evidence ledger, so deleting them would orphan those references.

As a safety net, a dated subdir is skipped (kept) if any tracked file OUTSIDE that subdir
still references it.

Usage:
    uv run python3 code/orchestrators/prune_old_reports.py            # dry-run (default)
    uv run python3 code/orchestrators/prune_old_reports.py --apply --retention-manifest data/report-retention.json
    uv run python3 code/orchestrators/prune_old_reports.py --apply --keep 2  # retain 2 latest
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = REPO_ROOT / "reports"
DEFAULT_RETENTION_MANIFEST = REPO_ROOT / "data" / "report-retention.json"

# Dated-screenshot parents whose subdirs are superseded snapshots (validation reads latest).
SCREENSHOT_PARENTS = ["visual-qa", "browser-smoke"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _dir_size_bytes(path: Path) -> int:
    return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())


def _dated_subdirs(parent: Path) -> list[Path]:
    if not parent.is_dir():
        return []
    return sorted((p for p in parent.iterdir() if p.is_dir() and DATE_RE.match(p.name)),
                  key=lambda p: p.name)


_WORKING_TREE_SUFFIXES = {".html", ".json", ".md", ".xml"}
_WORKING_TREE_SKIP_DIRS = {"reports", "code", ".git", "__pycache__", "_site"}
_WORKING_TREE_SKIP_FILES = {
    "data/pages-artifact-manifest.json",
    "data/generated-manifest.json",
    # The retention manifest cites removed paths to document the decision; it is
    # provenance, not a live link. Same reasoning as the inventory manifests.
    "data/report-retention.json",
}


def _working_tree_references(repo_root: Path, rel_prefix: str) -> bool:
    """True if a working-tree content file mentions ``rel_prefix``.

    Catches untracked files that ``git grep`` would miss. Skips reports/, code/,
    and the generated inventory manifests — those enumerate paths without
    serving them as live links.
    """
    root = repo_root.resolve()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        if any(part in _WORKING_TREE_SKIP_DIRS for part in rel.parts):
            continue
        if rel.as_posix() in _WORKING_TREE_SKIP_FILES:
            continue
        if path.suffix.lower() not in _WORKING_TREE_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        if rel_prefix in text:
            return True
    return False


def _referenced_externally(rel_prefix: str) -> bool:
    """True if a published content/data file references this dated subdir.

    Excludes reports/ (a set's own manifest cites its own PNGs) and code/ (generators
    carry stale fallback-default literals like ``"/reports/visual-qa/2026-05-13/..."``
    that are only used when no dated subdir exists — they are not live links in any
    served artifact). Also excludes the build INVENTORY manifests
    (data/pages-artifact-manifest.json, data/generated-manifest.json), which enumerate
    every tracked file by path but do not *link* to them — treating that inventory as a
    reference would pin every dated set forever and neuter this tool. We only care about
    orphaning genuine links in served content (HTML pages, llms.txt, feeds, sitemaps).

    After git grep, also scan the working tree so untracked files that mention the
    dated subdir still block prune.
    """
    try:
        out = subprocess.run(
            ["git", "grep", "-l", rel_prefix, "--", ".",
             ":(exclude)reports/*", ":(exclude)code/*",
             ":(exclude)data/pages-artifact-manifest.json",
             ":(exclude)data/generated-manifest.json",
             ":(exclude)data/report-retention.json"],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
        if out.stdout.strip():
            return True
    except FileNotFoundError:
        pass  # git unavailable: still honor working-tree references
    return _working_tree_references(REPO_ROOT, rel_prefix)


def _retention_entries(path: Path) -> dict[str, dict]:
    """Load reviewed removal records keyed by their exact report path."""
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Missing report-retention manifest: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid report-retention manifest {path}: {exc}") from exc
    if not isinstance(payload, dict) or payload.get("schema_version") != "1.0":
        raise SystemExit(f"Unsupported report-retention manifest: {path}")
    entries = payload.get("entries")
    if not isinstance(entries, list):
        raise SystemExit(f"Report-retention manifest has no entries list: {path}")
    result: dict[str, dict] = {}
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            raise SystemExit(f"Report-retention manifest has an invalid entry: {path}")
        result[entry["path"]] = entry
    return result


def _retention_errors(candidates: list[str], entries: dict[str, dict]) -> list[str]:
    """Return missing provenance fields before a destructive apply run."""
    required = ("generated_at", "provenance_sha256", "replacement_location", "decision", "reviewed_by")
    errors: list[str] = []
    for candidate in candidates:
        entry = entries.get(candidate)
        if not entry:
            errors.append(f"no retention record for {candidate}")
            continue
        missing = [field for field in required if not isinstance(entry.get(field), str) or not entry[field].strip()]
        if missing:
            errors.append(f"incomplete retention record for {candidate}: missing {', '.join(missing)}")
        elif entry.get("decision") != "remove-from-checkout":
            errors.append(f"retention decision for {candidate} is not remove-from-checkout")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="actually delete (default is dry-run)")
    parser.add_argument("--keep", type=int, default=1, help="number of most-recent sets to retain per parent (default 1)")
    parser.add_argument(
        "--retention-manifest",
        type=Path,
        default=DEFAULT_RETENTION_MANIFEST,
        help="Reviewed provenance records required for --apply.",
    )
    args = parser.parse_args()

    if args.keep < 1:
        parser.error("--keep must be >= 1")

    candidates: list[tuple[Path, str, int]] = []
    for name in SCREENSHOT_PARENTS:
        parent = REPORTS_DIR / name
        subdirs = _dated_subdirs(parent)
        superseded = subdirs[:-args.keep] if len(subdirs) > args.keep else []
        for sub in superseded:
            rel = f"reports/{name}/{sub.name}"
            if _referenced_externally(rel):
                print(f"keep (still referenced): {rel}")
                continue
            size = _dir_size_bytes(sub)
            candidates.append((sub, rel, size))
        kept = subdirs[-args.keep:] if subdirs else []
        if kept:
            print(f"{name}: keeping {', '.join(p.name for p in kept)}")

    if args.apply:
        retention_path = args.retention_manifest
        if not retention_path.is_absolute():
            retention_path = REPO_ROOT / retention_path
        errors = _retention_errors([rel for _sub, rel, _size in candidates], _retention_entries(retention_path))
        if errors:
            raise SystemExit(
                "Refusing to prune reports without durable provenance:\n"
                + "\n".join(f"  - {error}" for error in errors)
            )

    freed = sum(size for _sub, _rel, size in candidates)
    removed = len(candidates)
    for sub, rel, size in candidates:
        if args.apply:
            shutil.rmtree(sub)
            print(f"removed {rel} ({size / 1_000_000:.1f} MB)")
        else:
            print(f"would remove {rel} ({size / 1_000_000:.1f} MB)")

    verb = "freed" if args.apply else "would free"
    print(f"\n{verb} {freed / 1_000_000:.1f} MB across {removed} superseded screenshot set(s).")
    if not args.apply and removed:
        print("Re-run with --apply to delete, then `git add -A reports/` and commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
