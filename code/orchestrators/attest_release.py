#!/usr/bin/env python3
"""Create or verify a content-addressed post-deploy release attestation.

This tool never deploys.  Run it only after Pages and the live-site verifier
have observed the candidate commit.  ``validate_repo.py --release`` consumes
the receipt before any release-ready claim is made.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from release_evidence import (  # noqa: E402
    collect_release_evidence,
    deployment_attestation_path,
    live_deployment_errors,
    render_attestation,
    validate_attestation,
)


def resolve_commit(value: str | None) -> str:
    requested = value or "HEAD"
    result = subprocess.run(
        ["git", "rev-parse", "--verify", f"{requested}^{{commit}}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(f"Unable to resolve release commit: {requested}")
    return result.stdout.strip()


def default_output(commit: str) -> Path:
    return deployment_attestation_path(REPO_ROOT, commit)


def head_commit() -> str:
    return resolve_commit("HEAD")


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--apply", action="store_true", help="Write a fresh attestation after validating deployed evidence")
    mode.add_argument("--check", action="store_true", help="Verify an existing deployment attestation")
    parser.add_argument("--commit", help="Deployment SHA to attest (default: HEAD)")
    parser.add_argument("--output", type=Path, help="Attestation path (default: reports/deployment-attestations/SHA.json)")
    parser.add_argument("--max-report-age-days", type=int, default=30)
    args = parser.parse_args()

    commit = resolve_commit(args.commit)
    if commit != head_commit():
        raise SystemExit("A deployment attestation must bind the current HEAD checkout; create a detached/clean candidate checkout for another SHA.")
    canonical_output = default_output(commit)
    if args.output:
        output = args.output if args.output.is_absolute() else REPO_ROOT / args.output
        if output.resolve(strict=False) != canonical_output.resolve(strict=False):
            raise SystemExit(
                "--output is not permitted for deployment attestations; use "
                f"{canonical_output.relative_to(REPO_ROOT)}"
            )
    output = canonical_output
    if args.check:
        errors = validate_attestation(
            REPO_ROOT, output, commit, max_age_days=args.max_report_age_days
        )
        if errors:
            raise SystemExit("Release attestation validation failed:\n" + "\n".join(f"  - {error}" for error in errors))
        print(f"checked deployment attestation {output.relative_to(REPO_ROOT)} for {commit}")
        return

    receipts, errors = collect_release_evidence(
        REPO_ROOT, commit, max_age_days=args.max_report_age_days
    )
    errors.extend(live_deployment_errors(REPO_ROOT, commit))
    if errors:
        raise SystemExit("Cannot attest release:\n" + "\n".join(f"  - {error}" for error in errors))
    payload = render_attestation(commit, receipts, attested_at=timestamp())
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote deployment attestation {output.relative_to(REPO_ROOT)} for {commit}")


if __name__ == "__main__":
    main()
