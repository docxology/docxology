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
DEPLOYMENT_COMPARE_EXCLUDES = (
    ":(exclude)GENERATED.md",
    ":(exclude)data/agent-index.json",
    ":(exclude)data/generated-manifest.json",
    ":(exclude)data/pages-artifact-manifest.json",
    ":(exclude)data/release-integrity.json",
    ":(exclude)reports/**",
)
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from public_integrity import scan_public_files  # noqa: E402

# Keep the release envelope coupled to the same source-revision policy as the
# Pages manifest.  A stale manifest must not be able to mint a fresh-looking
# release-integrity envelope merely because its stored SHA is reused below.
import build_pages_artifact  # noqa: E402

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
    "code/orchestrators/audit_assets.py",
    "code/src/public_integrity.py",
    "code/src/release_controls.py",
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


def has_release_changes(status_output: str) -> bool:
    """Return whether status contains changes beyond the preserved local `_site/`."""
    for line in status_output.splitlines():
        if len(line) < 4:
            continue
        path = line[3:].split(" -> ")[-1].strip('"')
        if path != "_site" and not path.startswith("_site/"):
            return True
    return False


def current_worktree_has_release_changes() -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return has_release_changes(result.stdout) if result.returncode == 0 else True


def latest_report(prefix: str) -> Path | None:
    paths = sorted((REPO_ROOT / "reports").glob(f"{prefix}_*.json"))
    return paths[-1] if paths else None


def deployed_content_differs(deployed_commit: str) -> bool | None:
    """Compare release content with a known deployed commit.

    Control manifests and dated evidence are deliberately excluded: they are
    refreshed after deployment and must not make an otherwise identical site
    look stale. ``None`` means Git could not resolve or compare the commit.
    """
    if not deployed_commit or deployed_commit == "unknown":
        return None
    result = subprocess.run(
        ["git", "diff", "--quiet", deployed_commit, "--", ".", *DEPLOYMENT_COMPARE_EXCLUDES],
        cwd=REPO_ROOT,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return False
    if result.returncode == 1:
        return True
    return None


def deployment_pending_reasons(
    source_commit: str,
    deployment: dict,
    *,
    deployed_content_differs: bool | None = None,
) -> list[str]:
    """Explain why the recorded deployment is not the current release."""
    reasons: list[str] = []
    deployed_commit = deployment.get("commit")
    if not deployed_commit or deployed_commit == "unknown":
        reasons.append("no verified deployment commit")
    elif deployed_content_differs is True:
        reasons.append("tracked release content differs from the deployed commit")
    elif deployed_content_differs is None:
        reasons.append("unable to compare tracked release content with the deployed commit")
    if deployment.get("pages_status") != "built":
        reasons.append(f"Pages status is {deployment.get('pages_status') or 'unknown'}")
    if deployment.get("verification_overall_ok") is not True:
        reasons.append("live verification is not passing")
    return reasons


def validated_pages_source_commit(pages: dict) -> str:
    """Return the Pages source revision only after the manifest policy accepts it."""
    return build_pages_artifact.validate_source_commit_at_generation(
        pages.get("source_commit_at_generation")
    )


def build_payload() -> dict:
    current = json.loads((REPO_ROOT / "data/current-counts.json").read_text(encoding="utf-8"))
    pages = json.loads((REPO_ROOT / "data/pages-artifact-manifest.json").read_text(encoding="utf-8"))
    source_hashes = {path: sha256(REPO_ROOT / path) for path in SOURCE_FILES if (REPO_ROOT / path).is_file()}
    generator_hashes = {path: sha256(REPO_ROOT / path) for path in GENERATOR_FILES if (REPO_ROOT / path).is_file()}
    source_commit = validated_pages_source_commit(pages)
    deployment_payload = {
        "status": "pending_post_deploy_attestation",
        "candidate_source_commit": source_commit,
        "attestation_path_template": "reports/deployment-attestations/{deployment_sha}.json",
        "policy": "This pre-deploy envelope deliberately excludes mutable live-site evidence. A release-ready claim requires attest_release.py to bind fresh post-deploy reports to the deployed SHA.",
    }
    return {
        "schema_version": "1.0",
        "generated_at": current.get("generated_at"),
        # The release envelope is itself part of the commit, so recording the
        # current commit SHA here would be self-referential. Anchor it to the
        # source commit measured by the Pages manifest instead; deployment
        # metadata below records the separately verifiable hosted commit.
        "source_commit_at_generation": source_commit,
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
        "deployment": deployment_payload,
        "privacy": {
            "cv_public_integrity_errors": scan_public_files(REPO_ROOT),
            "policy": "No local filesystem paths, secret-like tokens, or unsafe URL schemes in public CV/source manifests.",
        },
        "counts": current.get("counts", {}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if release-integrity.json is stale")
    parser.add_argument(
        "--require-deployed",
        action="store_true",
        help="Fail with the post-deploy attestation command; this pre-deploy envelope never asserts deployment success",
    )
    args = parser.parse_args()
    payload = build_payload()
    if OUT.exists():
        try:
            payload["generated_at"] = json.loads(OUT.read_text(encoding="utf-8")).get("generated_at", payload["generated_at"])
        except json.JSONDecodeError:
            pass
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
    if args.require_deployed:
        raise SystemExit(
            "release deployment is verified only by a post-deploy attestation; run "
            "code/orchestrators/attest_release.py --apply --commit <deployment-sha>"
        )
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"stale release integrity manifest: {OUT.relative_to(REPO_ROOT)}")
        print(f"checked {OUT.relative_to(REPO_ROOT)}")
        return
    OUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
