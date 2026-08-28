#!/usr/bin/env python3
"""Assemble the bounded static artifact deployed to GitHub Pages.

The repository is the canonical archive, while Pages is the navigable web
projection. Paper-extracted image binaries and visual-QA screenshot binaries
remain in GitHub for provenance but are not duplicated into the Pages artifact;
generated paper pages point to their GitHub source image URLs and visual-QA
manifests retain repository-relative paths plus SHA-256 digests. This keeps the
published site below GitHub's 1 GiB Pages limit without removing source data
from the repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
import release_controls  # noqa: E402
from release_evidence import is_ephemeral_release_evidence_path  # noqa: E402

# Re-export the shared policy for existing callers and focused contract tests.
CONTROL_FILES = release_controls.CONTROL_FILES
CONTROL_REPORT_PATTERNS = release_controls.CONTROL_REPORT_PATTERNS
is_control_path = release_controls.is_control_path
_latest_payload_commit = release_controls.latest_payload_commit

DEFAULT_OUTPUT = REPO_ROOT / "_site"
# 900 MiB is the repository's release hard ceiling; GitHub Pages itself has a
# 1 GiB platform maximum.  Keep both values explicit so a warning is not
# mistaken for permission to cross the release ceiling.
MAX_ARTIFACT_BYTES = 900 * 1024 * 1024
WARNING_ARTIFACT_BYTES = 850 * 1024 * 1024
HARD_ARTIFACT_BYTES = 1024 * 1024 * 1024
ARTIFACT_MANIFEST = REPO_ROOT / "data" / "pages-artifact-manifest.json"
GROWTH_REPORT = REPO_ROOT / "reports" / f"pages_artifact_growth_{datetime.now(timezone.utc).date().isoformat()}.json"
_GROWTH_REPORT_NAME = re.compile(r"^pages_artifact_growth_(\d{4}-\d{2}-\d{2})\.json$")
_PREPAYLOAD_SOURCE_SNAPSHOT_NAME = re.compile(r"^public_source_snapshot_(\d{4}-\d{2}-\d{2})\.json$")

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
VISUAL_QA_SCREENSHOT_SUFFIXES = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tiff", ".webp"}


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


def _head_commit(repo_root: Path) -> str | None:
    """Return the current commit without treating an unresolved checkout as safe."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    value = result.stdout.strip()
    return value if result.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}", value) else None


def is_current_dirty_prepayload_source_snapshot(path: Path, repo_root: Path) -> bool:
    """Recognize the one reviewed source receipt allowed during payload assembly.

    ``refresh_public_sources.py`` runs before the source payload is committed,
    so its truthful snapshot records ``source_worktree_clean: false``.  It is
    source evidence to be committed with that payload, not post-deployment
    evidence.  Keep this exception deliberately narrower than the release
    evidence allowlist: only a validly dated top-level source snapshot, bound
    to the current ``HEAD``, can use it.  A clean deployed-SHA snapshot (or an
    unparseable/misbound file) remains a blocked post-deploy receipt.
    """
    if path.parent != Path("reports"):
        return False
    match = _PREPAYLOAD_SOURCE_SNAPSHOT_NAME.fullmatch(path.name)
    if match is None:
        return False
    try:
        date.fromisoformat(match.group(1))
        payload = json.loads((repo_root / path).read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError):
        return False
    return (
        isinstance(payload, dict)
        and payload.get("source_worktree_clean") is False
        and payload.get("source_commit") == _head_commit(repo_root)
    )


def dirty_postdeploy_payload_paths(
    repo_root: Path = REPO_ROOT,
    *,
    allow_dirty_prepayload_source_snapshot: bool = False,
) -> list[Path]:
    """Return dirty tracked evidence that would corrupt a source manifest.

    A Pages manifest hashes source files from the working tree.  Fresh
    post-deploy evidence can intentionally modify a tracked dated receipt in
    place, but that byte content is not present in the candidate commit.  Do
    not let a source-manifest write record those temporary bytes; generate the
    control tail from a clean worktree instead.
    """
    result = subprocess.run(
        ["git", "diff", "--name-only", "-z", "HEAD", "--"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit("unable to inspect dirty Pages inputs")
    return sorted(
        (
            path
            for path in (Path(raw) for raw in result.stdout.decode().split("\0") if raw)
            if is_published_path(path)
            and is_ephemeral_release_evidence_path(path.as_posix())
            and not is_control_path(path)
            and not (
                allow_dirty_prepayload_source_snapshot
                and is_current_dirty_prepayload_source_snapshot(path, repo_root)
            )
        ),
        key=lambda path: path.as_posix(),
    )


def require_clean_postdeploy_payload_inputs(
    repo_root: Path = REPO_ROOT,
    *,
    allow_dirty_prepayload_source_snapshot: bool = False,
) -> None:
    """Fail before source-manifest work can consume mutable evidence bytes."""
    dirty = dirty_postdeploy_payload_paths(
        repo_root,
        allow_dirty_prepayload_source_snapshot=allow_dirty_prepayload_source_snapshot,
    )
    if dirty:
        joined = ", ".join(path.as_posix() for path in dirty)
        raise SystemExit(
            "dirty post-deploy Pages inputs: "
            + joined
            + "; regenerate the Pages control tail in a clean worktree"
        )


def is_paper_extracted_image(path: Path) -> bool:
    """Return whether *path* is an extracted paper-image binary."""
    return (
        len(path.parts) >= 3
        and path.parts[0] == "papers"
        and "images" in path.parts
        and path.suffix.lower() in PAPER_IMAGE_SUFFIXES
    )


def is_visual_qa_screenshot(path: Path) -> bool:
    """Return whether *path* is a dated visual-QA screenshot binary.

    Only the exact top-level QA report layout is excluded. A similarly named
    nested path remains visible to the artifact policy rather than using a
    suffix match to evade it.
    """
    return (
        len(path.parts) >= 4
        and path.parts[0] == "reports"
        and path.parts[1] == "visual-qa"
        and path.suffix.lower() in VISUAL_QA_SCREENSHOT_SUFFIXES
    )


def is_published_path(path: Path) -> bool:
    """Return whether a tracked path belongs in the public web projection."""
    if path.parts and path.parts[0] in EXCLUDED_ROOTS:
        return False
    return not is_paper_extracted_image(path) and not is_visual_qa_screenshot(path)


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


def _omitted_paths() -> list[Path]:
    return sorted(
        (
            path
            for path in tracked_paths()
            if not is_published_path(path)
            and (is_paper_extracted_image(path) or is_visual_qa_screenshot(path))
        ),
        key=lambda path: path.as_posix(),
    )


def _omitted_summary(paths: list[Path], sources: dict[Path, Path]) -> dict[str, object]:
    """Return a provenance-friendly summary for one omitted binary class."""
    return {
        "count": len(paths),
        "bytes": sum(sources[path].stat().st_size for path in paths),
        "examples": [path.as_posix() for path in paths[:20]],
    }


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
    return release_controls.source_payload_commit(REPO_ROOT)


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
    "omitted_visual_qa_screenshots",
    "growth_report",
)


def manifest_drift_fields(existing: dict, expected: dict) -> list[str]:
    """Return every semantic manifest field that differs from its renderer."""
    return [field for field in MANIFEST_COMPARISON_FIELDS if existing.get(field) != expected.get(field)]


def _recorded_growth_report(existing: dict | None) -> Path | None:
    """Return a valid prior growth receipt path from an existing manifest.

    A no-write check can run after UTC midnight without a newly generated
    growth receipt.  In that case the manifest must continue to describe its
    committed, date-stamped receipt instead of becoming stale solely because
    the wall clock advanced.  Keep the accepted form narrow so a malformed
    manifest value remains a detectable drift error rather than an arbitrary
    artifact path.
    """
    raw = existing.get("growth_report") if isinstance(existing, dict) else None
    if not isinstance(raw, str) or "\\" in raw:
        return None
    candidate = Path(raw)
    if candidate.is_absolute() or ".." in candidate.parts or candidate.parent != Path("reports"):
        return None
    match = _GROWTH_REPORT_NAME.fullmatch(candidate.name)
    if match is None:
        return None
    try:
        date.fromisoformat(match.group(1))
    except ValueError:
        return None
    return candidate


def _growth_report_for_manifest(
    existing: dict | None,
    *,
    include_pending_growth: bool,
    current_growth_report: Path | None = None,
) -> Path:
    """Select the receipt that a write or no-write manifest pass must describe."""
    if not include_pending_growth:
        recorded = _recorded_growth_report(existing)
        if recorded is not None:
            return recorded
    growth_report = current_growth_report or GROWTH_REPORT
    return growth_report.relative_to(REPO_ROOT)


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
    growth_rel = _growth_report_for_manifest(
        existing, include_pending_growth=include_pending_growth
    )
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
    paper_images = [path for path in omitted if is_paper_extracted_image(path)]
    visual_qa_screenshots = [path for path in omitted if is_visual_qa_screenshot(path)]
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
            "omitted_assets": "duplicated extracted paper-image binaries and dated visual-QA screenshot binaries",
            "omitted_assets_fallback": "Use the GitHub tree/raw templates with the source commit and repository-relative path.",
            "visual_qa_screenshot_policy": "Visual-QA manifests remain in Pages with repository-relative paths and SHA-256 digests; screenshot binaries remain in the committed repository rather than the deploy artifact.",
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
        "omitted_paper_images": _omitted_summary(paper_images, omitted_sources),
        "omitted_visual_qa_screenshots": _omitted_summary(visual_qa_screenshots, omitted_sources),
        "growth_report": str(growth_rel),
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


def write_manifest(*, allow_dirty_prepayload_source_snapshot: bool = False) -> dict:
    require_clean_postdeploy_payload_inputs(
        allow_dirty_prepayload_source_snapshot=allow_dirty_prepayload_source_snapshot
    )
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
        "omitted_visual_qa_screenshot_count": payload["omitted_visual_qa_screenshots"]["count"],
        "omitted_visual_qa_screenshot_bytes": payload["omitted_visual_qa_screenshots"]["bytes"],
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
    require_clean_postdeploy_payload_inputs()
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
    require_clean_postdeploy_payload_inputs()
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


def projected_size(*, allow_dirty_prepayload_source_snapshot: bool = False) -> tuple[int, int]:
    """Return (included file count, included bytes) without copying files."""
    require_clean_postdeploy_payload_inputs(
        allow_dirty_prepayload_source_snapshot=allow_dirty_prepayload_source_snapshot
    )
    paths = _relative_paths()
    return len(paths), sum(source_path(path).stat().st_size for path in paths)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check-size", action="store_true", help="Fail if the assembled artifact exceeds the safety ceiling")
    parser.add_argument("--check-size-only", action="store_true", help="Check the projected size without copying an artifact")
    parser.add_argument("--write-manifest", action="store_true", help="Write the checked-in Pages artifact and growth manifests")
    parser.add_argument(
        "--allow-dirty-prepayload-evidence",
        action="store_true",
        help=(
            "Allow only a current, dirty public-source snapshot whose own receipt records "
            "source_worktree_clean=false; reserved for pre-commit payload regeneration"
        ),
    )
    parser.add_argument("--check-manifest", action="store_true", help="Fail if the checked-in Pages artifact manifest is stale")
    args = parser.parse_args()
    if args.allow_dirty_prepayload_evidence and not args.write_manifest:
        raise SystemExit("--allow-dirty-prepayload-evidence requires --write-manifest")
    if args.write_manifest:
        write_manifest(
            allow_dirty_prepayload_source_snapshot=args.allow_dirty_prepayload_evidence
        )
    if args.check_manifest:
        check_manifest()
    if args.check_size_only:
        copied, size = projected_size(
            allow_dirty_prepayload_source_snapshot=args.allow_dirty_prepayload_evidence
        )
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
    paper_images = sum(1 for path in omitted if is_paper_extracted_image(Path(path)))
    visual_qa_screenshots = sum(1 for path in omitted if is_visual_qa_screenshot(Path(path)))
    print(
        f"omitted {len(omitted)} source-only binary assets "
        f"({paper_images} paper images, {visual_qa_screenshots} visual-QA screenshots); "
        "source copies remain in GitHub"
    )
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
