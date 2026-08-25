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
import fnmatch
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = REPO_ROOT / "_site"
# 900 MiB is the repository's release hard ceiling; GitHub Pages itself has a
# 1 GiB platform maximum.  Keep both values explicit so a warning is not
# mistaken for permission to cross the release ceiling.
MAX_ARTIFACT_BYTES = 900 * 1024 * 1024
WARNING_ARTIFACT_BYTES = 850 * 1024 * 1024
HARD_ARTIFACT_BYTES = 1024 * 1024 * 1024
ARTIFACT_MANIFEST = REPO_ROOT / "data" / "pages-artifact-manifest.json"
GROWTH_REPORT = REPO_ROOT / "reports" / f"pages_artifact_growth_{datetime.now(timezone.utc).date().isoformat()}.json"
CONTROL_FILES = {
    Path("GENERATED.md"),
    Path("data/agent-index.json"),
    Path("data/generated-manifest.json"),
    Path("data/pages-artifact-manifest.json"),
    Path("data/release-integrity.json"),
    GROWTH_REPORT.relative_to(REPO_ROOT),
}

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
    paths = [Path(raw) for raw in result.stdout.decode().split("\0") if raw]
    if ARTIFACT_MANIFEST.exists() and ARTIFACT_MANIFEST.relative_to(REPO_ROOT) not in paths:
        paths.append(ARTIFACT_MANIFEST.relative_to(REPO_ROOT))
    # The current growth report is created during this pipeline before it is
    # necessarily staged. Include it in local projections so the manifest and
    # assembled artifact describe the same file set in the write/check cycle.
    growth_report = GROWTH_REPORT.relative_to(REPO_ROOT)
    if GROWTH_REPORT.exists() and growth_report not in paths:
        paths.append(growth_report)
    return paths


def is_published_path(path: Path) -> bool:
    """Return whether a tracked path belongs in the public web projection."""
    if path.parts and path.parts[0] in EXCLUDED_ROOTS:
        return False
    if len(path.parts) >= 3 and path.parts[0] == "papers" and "images" in path.parts:
        if path.suffix.lower() in PAPER_IMAGE_SUFFIXES:
            return False
    return True


def _relative_paths() -> list[Path]:
    return sorted((path for path in tracked_paths() if is_published_path(path)), key=lambda path: path.as_posix())


def source_path(relative: Path, *, repo_root: Path = REPO_ROOT) -> Path:
    """Return a safe regular Pages input or fail closed.

    A committed symlink can resolve outside the checkout and cause ``copy2``
    (or manifest hashing) to publish a maintainer/CI-local file. Git does not
    need symlinks for this static site, so reject final and ancestor links
    instead of trying to preserve or dereference them.
    """
    if relative.is_absolute() or ".." in relative.parts:
        raise SystemExit(f"unsafe Pages input path: {relative}")
    source = repo_root / relative
    try:
        metadata = source.lstat()
    except FileNotFoundError as exc:
        raise SystemExit(f"missing tracked Pages input: {relative}") from exc
    cursor = repo_root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise SystemExit(f"symlinked Pages input is not allowed: {relative}")
    try:
        source.resolve(strict=True).relative_to(repo_root.resolve(strict=True))
    except (FileNotFoundError, ValueError) as exc:
        raise SystemExit(f"Pages input escapes repository: {relative}") from exc
    if not source.is_file():
        raise SystemExit(f"non-file Pages input is not allowed: {relative}")
    if metadata.st_nlink != 1:
        raise SystemExit(f"hard-linked Pages input is not allowed: {relative}")
    return source


def is_control_path(path: Path) -> bool:
    """Return whether a published path is control metadata, not payload data."""
    # ``Path.match`` treats a pattern containing a directory as a suffix match,
    # so ``untrusted/reports/pages_artifact_growth_*.json`` would otherwise
    # evade the payload manifest and budget. Control reports live exactly at
    # the repository's top-level reports/ path.
    is_growth_report = (
        path.parent == Path("reports")
        and fnmatch.fnmatchcase(path.name, "pages_artifact_growth_*.json")
    )
    return path in CONTROL_FILES or is_growth_report


def _omitted_paths() -> list[Path]:
    return sorted(
        (
            path
            for path in tracked_paths()
            if not is_published_path(path)
            and len(path.parts) >= 3
            and path.parts[0] == "papers"
            and "images" in path.parts
            and path.suffix.lower() in PAPER_IMAGE_SUFFIXES
        ),
        key=lambda path: path.as_posix(),
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _source_commit() -> str:
    """Return the commit that last changed Pages payload content.

    A Pages manifest is necessarily committed *after* it is rendered, so a
    clean release can end with one control-only commit containing the manifest,
    agent index, release envelope, and growth receipt.  In that case ``HEAD``
    is not the payload revision that the manifest describes.  Walk past that
    narrow trailing control-only suffix, but stop immediately at any content
    change.  This makes a later README/source commit visible to ``--check``
    without creating a self-referential manifest requirement.
    """
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, check=False, capture_output=True, text=True
    )
    head = result.stdout.strip() if result.returncode == 0 else "unknown"
    if head == "unknown":
        return head
    return _latest_payload_commit(head, _first_parent, _changed_paths)


def _first_parent(commit: str) -> str | None:
    """Return ``commit``'s first parent, or ``None`` for a root/unresolved commit."""
    result = subprocess.run(
        ["git", "show", "-s", "--format=%P", commit],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    parents = result.stdout.split()
    return parents[0] if parents else None


def _changed_paths(commit: str) -> list[Path]:
    """Return paths changed from the first parent to ``commit``.

    Using the first parent gives merges the same source-revision meaning as a
    normal release branch: a merge is substantive whenever it introduces a
    non-control path relative to the branch it extends.
    """
    parent = _first_parent(commit)
    if not parent:
        return []
    result = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "-z", parent, commit],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
    )
    if result.returncode != 0:
        # An unresolved history must never be silently classified as a
        # control-only suffix.  The commit itself remains the source anchor.
        return [Path(".unresolved-source-revision")]
    return [Path(raw) for raw in result.stdout.decode("utf-8", errors="surrogateescape").split("\0") if raw]


def _latest_payload_commit(
    head: str,
    parent_for: Callable[[str], str | None],
    changed_paths_for: Callable[[str], list[Path]],
) -> str:
    """Find the latest non-control commit in a first-parent history.

    ``parent_for`` and ``changed_paths_for`` are explicit collaborators so the
    release boundary can be tested with a small deterministic history rather
    than by mutating the real Git repository.
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


def validate_source_commit_at_generation(
    value: object,
    *,
    expected_source_commit: str | None = None,
    manifest_path: Path | None = None,
) -> str:
    """Fail closed when a manifest's source revision no longer matches HEAD.

    The expected revision deliberately permits a trailing control-only commit
    (see :func:`_source_commit`), but not a later commit that changes published
    payload content.  Returning the validated value keeps consumers from
    accidentally reusing an unchecked manifest field.
    """
    actual = str(value or "").strip()
    expected = expected_source_commit or _source_commit()
    path = manifest_path or ARTIFACT_MANIFEST
    if not actual or actual != expected:
        raise SystemExit(
            "stale Pages artifact manifest: "
            f"{path} "
            "(source_commit_at_generation; "
            f"expected {expected or 'unknown'}, found {actual or 'missing'})"
        )
    return actual


MANIFEST_COMPARISON_FIELDS = (
    "schema_version",
    "source_commit_at_generation",
    "canonical_origin",
    "github_fallback",
    "policy",
    "budget",
    "included_files",
    "control_files",
    "omitted_paper_images",
    "growth_report",
)


def manifest_drift_fields(existing: dict, expected: dict) -> list[str]:
    """Return every semantic manifest field that differs from its renderer."""
    return [field for field in MANIFEST_COMPARISON_FIELDS if existing.get(field) != expected.get(field)]


def _manifest_payload(existing: dict | None = None, *, include_pending_growth: bool = True) -> dict:
    manifest_rel = ARTIFACT_MANIFEST.relative_to(REPO_ROOT)
    relative_paths = _relative_paths()
    sources = {path: source_path(path) for path in relative_paths}
    included = [path for path in relative_paths if path != manifest_rel and not is_control_path(path)]
    # Write path: include today's growth report even before it exists so the
    # first UTC-day run cannot make the manifest stale of itself.
    # Check path: only require that path when the file is actually on disk,
    # otherwise later-day CI `--check-manifest` would fail against a committed
    # manifest that still lists the previous day's report.
    growth_rel = GROWTH_REPORT.relative_to(REPO_ROOT)
    expected_control_paths = set(relative_paths)
    if include_pending_growth:
        expected_control_paths.add(growth_rel)
    controls = sorted(
        (path for path in expected_control_paths if path != manifest_rel and is_control_path(path)),
        key=lambda path: path.as_posix(),
    )
    omitted = _omitted_paths()
    source_bytes = sum(sources[path].stat().st_size for path in included)
    omitted_sources = {path: source_path(path) for path in omitted}
    omitted_bytes = sum(source.stat().st_size for source in omitted_sources.values())
    files = [
        {"path": path.as_posix(), "bytes": sources[path].stat().st_size, "sha256": _sha256(sources[path])}
        for path in included
        if path != ARTIFACT_MANIFEST.relative_to(REPO_ROOT)
    ]
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    payload = {
        "schema_version": "1.0",
        "generated_at": generated_at,
        "source_commit_at_generation": _source_commit(),
        "canonical_origin": "https://danielarifriedman.com/",
        "github_fallback": {
            "tree_template": "https://github.com/docxology/docxology/tree/{commit}/{path}",
            "raw_template": "https://raw.githubusercontent.com/docxology/docxology/{commit}/{path}",
        },
        "policy": {
            "repository_role": "complete archival source",
            "pages_role": "bounded navigable web projection",
            "omitted_assets": "duplicated extracted paper-image binaries only",
            "omitted_assets_fallback": "Use the GitHub tree/raw templates with the source commit and repository-relative path.",
            "warning_policy": "At 850 MiB, review growth and report retention before deployment; 900 MiB is a release hard ceiling below the GitHub Pages 1 GiB platform limit.",
        },
        "budget": {
            "hard_limit_bytes": HARD_ARTIFACT_BYTES,
            "release_hard_ceiling_bytes": MAX_ARTIFACT_BYTES,
            "safety_ceiling_bytes": MAX_ARTIFACT_BYTES,
            "warning_bytes": WARNING_ARTIFACT_BYTES,
            "source_bytes": source_bytes,
            "budget_scope": "published content files plus this manifest; control metadata files are listed but excluded to avoid self-referential hashes",
            "manifest_bytes_excluded_from_source_bytes": True,
            "artifact_file_count": len(files) + len(controls) + 1,
            "artifact_bytes": 0,
        },
        "included_files": files,
        "control_files": [
            {"path": path.as_posix(), "role": "public control metadata"}
            for path in controls
            # growth_rel is exempt from the existence check: write_manifest()
            # creates it *after* this payload is built, so requiring it on disk
            # cancelled the pre-inclusion above and left the freshly written
            # manifest one control entry short of its own recomputation —
            # permanently stale until a second pass.
            if (REPO_ROOT / path).is_file() or path == growth_rel
        ],
        "omitted_paper_images": {
            "count": len(omitted),
            "bytes": omitted_bytes,
            "examples": [path.as_posix() for path in omitted[:20]],
        },
        "growth_report": str(GROWTH_REPORT.relative_to(REPO_ROOT)),
    }
    # The manifest is part of the artifact. Iterate to account for its own
    # serialized byte size without introducing a self-referential hash.
    for _ in range(5):
        rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        artifact_bytes = source_bytes + len(rendered.encode("utf-8"))
        if payload["budget"]["artifact_bytes"] == artifact_bytes:
            break
        payload["budget"]["artifact_bytes"] = artifact_bytes
    if existing:
        current_body = {key: value for key, value in payload.items() if key != "generated_at"}
        existing_body = {key: value for key, value in existing.items() if key != "generated_at"}
        if current_body == existing_body and existing.get("generated_at"):
            payload["generated_at"] = existing["generated_at"]
    return payload


def write_manifest() -> dict:
    existing = None
    manifest_rel = ARTIFACT_MANIFEST.relative_to(REPO_ROOT)
    if ARTIFACT_MANIFEST.exists():
        # Validate before reading: an existing symlink must not supply either
        # manifest state or a write destination outside this checkout.
        source_path(manifest_rel)
        try:
            existing = json.loads(ARTIFACT_MANIFEST.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = None
    payload = _manifest_payload(existing)
    ARTIFACT_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT_MANIFEST.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    growth = {
        "schema_version": "1.0",
        "generated_at": payload["generated_at"],
        "source_commit_at_generation": payload["source_commit_at_generation"],
        "artifact_file_count": payload["budget"]["artifact_file_count"],
        "artifact_bytes": payload["budget"]["artifact_bytes"],
        "artifact_mib": round(payload["budget"]["artifact_bytes"] / 1024 / 1024, 2),
        "warning_bytes": WARNING_ARTIFACT_BYTES,
        "safety_ceiling_bytes": MAX_ARTIFACT_BYTES,
        "hard_limit_bytes": HARD_ARTIFACT_BYTES,
        "omitted_paper_image_count": payload["omitted_paper_images"]["count"],
    }
    previous = sorted((REPO_ROOT / "reports").glob("pages_artifact_growth_*.json"))
    if previous and previous[-1] != GROWTH_REPORT:
        try:
            prior = json.loads(previous[-1].read_text(encoding="utf-8"))
            growth["delta_bytes"] = growth["artifact_bytes"] - int(prior.get("artifact_bytes", growth["artifact_bytes"]))
            growth["previous_report"] = str(previous[-1].relative_to(REPO_ROOT))
        except (OSError, ValueError, json.JSONDecodeError):
            pass
    GROWTH_REPORT.parent.mkdir(parents=True, exist_ok=True)
    GROWTH_REPORT.write_text(json.dumps(growth, indent=2) + "\n", encoding="utf-8")
    return payload


def check_manifest() -> None:
    if not ARTIFACT_MANIFEST.exists():
        raise SystemExit(f"Missing Pages artifact manifest: {ARTIFACT_MANIFEST.relative_to(REPO_ROOT)}")
    manifest_path = source_path(ARTIFACT_MANIFEST.relative_to(REPO_ROOT))
    existing = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = _manifest_payload(existing, include_pending_growth=GROWTH_REPORT.exists())
    stale_fields = manifest_drift_fields(existing, expected)
    if stale_fields:
        raise SystemExit(
            f"stale Pages artifact manifest: {ARTIFACT_MANIFEST.relative_to(REPO_ROOT)} ({', '.join(stale_fields)})"
        )
    validate_source_commit_at_generation(existing.get("source_commit_at_generation"))
    print(f"checked {ARTIFACT_MANIFEST.relative_to(REPO_ROOT)}")


def assemble(output: Path) -> tuple[int, int, list[str]]:
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    copied = 0
    bytes_copied = 0
    omitted: list[str] = []
    for relative in tracked_paths():
        if not is_published_path(relative):
            if len(relative.parts) >= 3 and relative.parts[0] == "papers" and "images" in relative.parts:
                omitted.append(str(relative))
            continue
        source = source_path(relative)
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied += 1
        bytes_copied += source.stat().st_size
    return copied, bytes_copied, omitted


def projected_size() -> tuple[int, int]:
    """Return (included file count, included bytes) without copying files."""
    paths = _relative_paths()
    return len(paths), sum(source_path(path).stat().st_size for path in paths)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-size", action="store_true", help="Fail if the assembled artifact exceeds the safety ceiling")
    parser.add_argument("--check-size-only", action="store_true", help="Check the projected size without copying an artifact")
    parser.add_argument("--write-manifest", action="store_true", help="Write the checked-in Pages artifact and growth manifests")
    parser.add_argument("--check-manifest", action="store_true", help="Fail if the checked-in Pages artifact manifest is stale")
    args = parser.parse_args()
    if args.write_manifest:
        write_manifest()
    if args.check_manifest:
        check_manifest()
    if args.check_size_only:
        copied, size = projected_size()
        print(f"projected Pages artifact: {copied} tracked files ({size / 1024 / 1024:.1f} MiB)")
        if size > MAX_ARTIFACT_BYTES:
            raise SystemExit(
                f"Pages artifact is {size / 1024 / 1024:.1f} MiB; safety ceiling is "
                f"{MAX_ARTIFACT_BYTES / 1024 / 1024:.1f} MiB"
            )
        if size > WARNING_ARTIFACT_BYTES:
            print(
                "warning: Pages artifact is "
                f"{size / 1024 / 1024:.1f} MiB; it exceeds the 850 MiB review threshold "
                f"and remains below the {MAX_ARTIFACT_BYTES / 1024 / 1024:.1f} MiB release hard ceiling. "
                "Review growth and report retention before deployment."
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
    if args.check_size and size > WARNING_ARTIFACT_BYTES:
        print(
            f"warning: Pages artifact is {size / 1024 / 1024:.1f} MiB; it exceeds the "
            f"{WARNING_ARTIFACT_BYTES / 1024 / 1024:.1f} MiB review threshold and remains below the "
            f"{MAX_ARTIFACT_BYTES / 1024 / 1024:.1f} MiB release hard ceiling. Review growth and report retention before deployment."
        )


if __name__ == "__main__":
    main()
