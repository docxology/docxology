#!/usr/bin/env python3
"""Prune superseded dated QA screenshot sets under reports/ to bound the working tree.

`visual_qa.py` and `browser_smoke.py` each write a fresh dated subdirectory of full-page
screenshots every run (`reports/visual-qa/YYYY-MM-DD/`, `reports/browser-smoke/YYYY-MM-DD/`),
and `validate_repo.py` only ever reads the LATEST set via `latest_subdir_file(...)`. The
older sets are pure history — at ~29 MB per visual-qa set they dominate the repo's tracked
size (88 MB of 100 MB at last count). Git history still retains anything pruned here, so
this only trims the checked-out tree and bounds future growth.

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
    uv run python3 code/orchestrators/prune_old_reports.py --apply    # delete superseded sets
    uv run python3 code/orchestrators/prune_old_reports.py --apply --keep 2  # retain 2 latest
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = REPO_ROOT / "reports"

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


def _referenced_externally(rel_prefix: str) -> bool:
    """True if a published content/data file references this dated subdir.

    Excludes reports/ (a set's own manifest cites its own PNGs) and code/ (generators
    carry stale fallback-default literals like ``"/reports/visual-qa/2026-05-13/..."``
    that are only used when no dated subdir exists — they are not live links in any
    served artifact). We only care about orphaning references in the published site/data.
    """
    try:
        out = subprocess.run(
            ["git", "grep", "-l", rel_prefix, "--", ".",
             ":(exclude)reports/*", ":(exclude)code/*"],
            cwd=REPO_ROOT, capture_output=True, text=True,
        )
    except FileNotFoundError:
        return False  # git unavailable: fall back to the self-contained guarantee
    return bool(out.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="actually delete (default is dry-run)")
    parser.add_argument("--keep", type=int, default=1, help="number of most-recent sets to retain per parent (default 1)")
    args = parser.parse_args()

    if args.keep < 1:
        parser.error("--keep must be >= 1")

    freed = 0
    removed = 0
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
            freed += size
            removed += 1
            if args.apply:
                shutil.rmtree(sub)
                print(f"removed {rel} ({size / 1_000_000:.1f} MB)")
            else:
                print(f"would remove {rel} ({size / 1_000_000:.1f} MB)")
        kept = subdirs[-args.keep:] if subdirs else []
        if kept:
            print(f"{name}: keeping {', '.join(p.name for p in kept)}")

    verb = "freed" if args.apply else "would free"
    print(f"\n{verb} {freed / 1_000_000:.1f} MB across {removed} superseded screenshot set(s).")
    if not args.apply and removed:
        print("Re-run with --apply to delete, then `git add -A reports/` and commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
