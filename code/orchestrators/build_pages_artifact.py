#!/usr/bin/env python3
"""Assemble the bounded static artifact deployed to GitHub Pages.

The repository is the canonical archive, while Pages is the navigable web
projection. Paper-extracted image binaries remain in GitHub for provenance but
are not duplicated into the Pages artifact; generated paper pages point to
their GitHub source image URLs. This keeps the published site below GitHub's
1 GiB Pages limit without removing source data from the repository.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = REPO_ROOT / "_site"
MAX_ARTIFACT_BYTES = 900 * 1024 * 1024  # leave margin below the 1 GiB hard limit

EXCLUDED_ROOTS = {
    ".benchmarks",
    ".claude",
    ".cursor",
    ".github",
    ".pytest_cache",
    ".venv",
    "manuscript",
    "netlify-stripe-webhook",
    "output",
    "Plans",
}
PAPER_IMAGE_SUFFIXES = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tiff", ".webp"}


def tracked_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    return [Path(raw) for raw in result.stdout.decode().split("\0") if raw]


def is_published_path(path: Path) -> bool:
    """Return whether a tracked path belongs in the public web projection."""
    if path.parts and path.parts[0] in EXCLUDED_ROOTS:
        return False
    if len(path.parts) >= 3 and path.parts[0] == "papers" and "images" in path.parts:
        if path.suffix.lower() in PAPER_IMAGE_SUFFIXES:
            return False
    return True


def assemble(output: Path) -> tuple[int, int, list[str]]:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    copied = 0
    bytes_copied = 0
    omitted: list[str] = []
    for relative in tracked_paths():
        source = REPO_ROOT / relative
        if not is_published_path(relative):
            if len(relative.parts) >= 3 and relative.parts[0] == "papers" and "images" in relative.parts:
                omitted.append(str(relative))
            continue
        if not source.is_file():
            continue
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied += 1
        bytes_copied += source.stat().st_size
    return copied, bytes_copied, omitted


def projected_size() -> tuple[int, int]:
    """Return (included file count, included bytes) without copying files."""
    paths = [path for path in tracked_paths() if is_published_path(path)]
    return len(paths), sum((REPO_ROOT / path).stat().st_size for path in paths if (REPO_ROOT / path).is_file())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-size", action="store_true", help="Fail if the assembled artifact exceeds the safety ceiling")
    parser.add_argument("--check-size-only", action="store_true", help="Check the projected size without copying an artifact")
    args = parser.parse_args()
    if args.check_size_only:
        copied, size = projected_size()
        print(f"projected Pages artifact: {copied} tracked files ({size / 1024 / 1024:.1f} MiB)")
        if size > MAX_ARTIFACT_BYTES:
            raise SystemExit(
                f"Pages artifact is {size / 1024 / 1024:.1f} MiB; safety ceiling is "
                f"{MAX_ARTIFACT_BYTES / 1024 / 1024:.1f} MiB"
            )
        return
    output = args.output if args.output.is_absolute() else REPO_ROOT / args.output
    copied, size, omitted = assemble(output)
    print(f"assembled {copied} tracked files ({size / 1024 / 1024:.1f} MiB) at {output}")
    print(f"omitted {len(omitted)} paper-extracted image binaries; source copies remain in GitHub")
    if args.check_size and size > MAX_ARTIFACT_BYTES:
        raise SystemExit(
            f"Pages artifact is {size / 1024 / 1024:.1f} MiB; safety ceiling is "
            f"{MAX_ARTIFACT_BYTES / 1024 / 1024:.1f} MiB"
        )


if __name__ == "__main__":
    main()
