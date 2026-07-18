#!/usr/bin/env python3
"""Build the source-to-release integrity envelope for the public projection."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "data" / "release-integrity.json"
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from public_integrity import scan_public_files  # noqa: E402

SOURCE_FILES = (
    "pages/BIBLIOGRAPHY.md",
    "pages/SOFTWARE.md",
    "resume/source.json",
    "data/current-counts.json",
    "data/coverage-exceptions.json",
    "data/repository-classification.json",
    "data/agent-index.json",
    "data/generated-manifest.json",
    "data/pages-artifact-manifest.json",
)
GENERATOR_FILES = (
    "code/orchestrators/regenerate_all.py",
    "code/orchestrators/build_pages_artifact.py",
    "code/orchestrators/build_agent_index.py",
    "code/orchestrators/build_coverage_exceptions.py",
    "code/orchestrators/classify_repositories.py",
    "code/orchestrators/verify_live_site.py",
    "code/orchestrators/audit_assets.py",
    "code/src/public_integrity.py",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_value(*args: str) -> str:
    result = subprocess.run(["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=False)
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def latest_report(prefix: str) -> Path | None:
    paths = sorted((REPO_ROOT / "reports").glob(f"{prefix}_*.json"))
    return paths[-1] if paths else None


def build_payload() -> dict:
    current = json.loads((REPO_ROOT / "data/current-counts.json").read_text(encoding="utf-8"))
    pages = json.loads((REPO_ROOT / "data/pages-artifact-manifest.json").read_text(encoding="utf-8"))
    live_path = latest_report("live_site_verification")
    live = json.loads(live_path.read_text(encoding="utf-8")) if live_path else {}
    source_hashes = {path: sha256(REPO_ROOT / path) for path in SOURCE_FILES if (REPO_ROOT / path).is_file()}
    generator_hashes = {path: sha256(REPO_ROOT / path) for path in GENERATOR_FILES if (REPO_ROOT / path).is_file()}
    deployment = live.get("deployment", {})
    return {
        "schema_version": "1.0",
        "generated_at": current.get("generated_at"),
        # The release envelope is itself part of the commit, so recording the
        # current commit SHA here would be self-referential. Anchor it to the
        # source commit measured by the Pages manifest instead; deployment
        # metadata below records the separately verifiable hosted commit.
        "source_commit_at_generation": pages.get("source_commit_at_generation") or git_value("rev-parse", "HEAD"),
        "repository": "docxology/docxology",
        "canonical_origin": "https://danielarifriedman.com/",
        "generator": {
            "pipeline": "code/orchestrators/regenerate_all.py",
            # Record the project contract, not the runner's patch/minor
            # version. CI uses Python 3.12 while the maintainer workstation
            # may use 3.13; the integrity envelope must be cross-runtime
            # reproducible while still documenting the supported floor.
            "python": ">=3.12 (pyproject.toml)",
            "project_version": "0.1.0",
            "orchestrator_sha256": generator_hashes,
        },
        "source_sha256": source_hashes,
        "pages_artifact": {
            "manifest": "data/pages-artifact-manifest.json",
            "source_commit_at_generation": pages.get("source_commit_at_generation"),
            "artifact_file_count": pages.get("budget", {}).get("artifact_file_count"),
            "artifact_bytes": pages.get("budget", {}).get("artifact_bytes"),
            "omitted_paper_image_count": pages.get("omitted_paper_images", {}).get("count"),
        },
        "deployment": {
            "commit": deployment.get("head_sha") or deployment.get("commit") or pages.get("source_commit_at_generation"),
            "workflow_run_id": deployment.get("workflow_run_id"),
            "workflow_url": deployment.get("workflow_url"),
            "pages_status": live.get("github_pages", {}).get("status"),
            "verification_report": str(live_path.relative_to(REPO_ROOT)) if live_path else None,
            "verification_generated_at": live.get("generated_at"),
            "verification_overall_ok": live.get("overall_ok"),
            "verified_routes": f"{live.get('passing', 0)}/{live.get('checked_urls', 0)}",
        },
        "privacy": {
            "cv_public_integrity_errors": scan_public_files(REPO_ROOT),
            "policy": "No local filesystem paths, secret-like tokens, or unsafe URL schemes in public CV/source manifests.",
        },
        "counts": current.get("counts", {}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if release-integrity.json is stale")
    args = parser.parse_args()
    payload = build_payload()
    if OUT.exists():
        try:
            payload["generated_at"] = json.loads(OUT.read_text(encoding="utf-8")).get("generated_at", payload["generated_at"])
        except json.JSONDecodeError:
            pass
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"stale release integrity manifest: {OUT.relative_to(REPO_ROOT)}")
        print(f"checked {OUT.relative_to(REPO_ROOT)}")
        return
    OUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
