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
import hashlib
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = REPO_ROOT / "_site"
MAX_ARTIFACT_BYTES = 900 * 1024 * 1024  # leave margin below the 1 GiB hard limit
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
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, check=False, capture_output=True, text=True
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def _manifest_payload(existing: dict | None = None) -> dict:
    manifest_rel = ARTIFACT_MANIFEST.relative_to(REPO_ROOT)
    included = [path for path in _relative_paths() if path != manifest_rel and path not in CONTROL_FILES]
    controls = [path for path in _relative_paths() if path in CONTROL_FILES and path != manifest_rel]
    omitted = _omitted_paths()
    source_bytes = sum((REPO_ROOT / path).stat().st_size for path in included if (REPO_ROOT / path).is_file())
    omitted_bytes = sum((REPO_ROOT / path).stat().st_size for path in omitted if (REPO_ROOT / path).is_file())
    files = [
        {"path": path.as_posix(), "bytes": (REPO_ROOT / path).stat().st_size, "sha256": _sha256(REPO_ROOT / path)}
        for path in included
        if (REPO_ROOT / path).is_file() and path != ARTIFACT_MANIFEST.relative_to(REPO_ROOT)
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
        },
        "budget": {
            "hard_limit_bytes": HARD_ARTIFACT_BYTES,
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
            if (REPO_ROOT / path).is_file()
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
    if ARTIFACT_MANIFEST.exists():
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
    existing = json.loads(ARTIFACT_MANIFEST.read_text(encoding="utf-8"))
    expected = _manifest_payload(existing)
    for key in ("schema_version", "canonical_origin", "github_fallback", "policy", "budget", "included_files", "control_files", "omitted_paper_images"):
        if existing.get(key) != expected.get(key):
            raise SystemExit(f"stale Pages artifact manifest: {ARTIFACT_MANIFEST.relative_to(REPO_ROOT)} ({key})")
    print(f"checked {ARTIFACT_MANIFEST.relative_to(REPO_ROOT)}")


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
    paths = _relative_paths()
    return len(paths), sum((REPO_ROOT / path).stat().st_size for path in paths if (REPO_ROOT / path).is_file())


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
        print(f"warning: Pages artifact is {size / 1024 / 1024:.1f} MiB; review growth trend above the {WARNING_ARTIFACT_BYTES / 1024 / 1024:.1f} MiB warning budget")


if __name__ == "__main__":
    main()
