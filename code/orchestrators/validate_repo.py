#!/usr/bin/env python3
"""Validate generated files, structured data, local links, and metadata."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

try:
    from report_paths import latest_report, latest_subdir_file
except ImportError:  # pragma: no cover - package import path
    from .report_paths import latest_report, latest_subdir_file

from release_evidence import (  # noqa: E402
    is_ephemeral_release_evidence_path,
    scholar_source_receipt_errors,
    validate_attestation,
)
from generation_plan import LOCAL_GENERATION_STEPS, validate_generation_plan  # noqa: E402


REQUIRED_JSON_FILES: list[str] = [
    "bibliography.csl.json",
    "codemeta.json",
    "search-index.json",
    "data/catalog.json",
    "data/current-counts.json",
    "data/generated-manifest.json",
    "data/github-repositories.json",
    "data/artworks.json",
    "data/artworks-index.json",
    "data/videos-index.json",
    "data/works.json",
    "data/video-pages-manifest.json",
    "data/work-enrichment.json",
    "data/software-ld.json",
    "data/software.json",
    "data/people.json",
    "data/organizations.json",
    "data/paired-publication-decisions.json",
    "data/public-source-observation-decisions.json",
    "data/biographical-claim-decisions.json",
    "data/claims.json",
    "data/resume.json",
    "data/reconciliation.json",
    "data/agent-index.json",
    "data/coverage-exceptions.json",
    "data/repository-classification.json",
    "data/pages-artifact-manifest.json",
    "data/release-integrity.json",
]

OPTIONAL_REPORT_PATTERNS: list[tuple[str, str]] = [
    ("accessibility_static_*.json", "accessibility static checks"),
    ("asset_size_*.json", "asset-size audit"),
    ("external_links_[0-9]*.json", "external-links snapshot"),
    ("external_links_triage_*.json", "external-links triage"),
    ("live_site_verification_*.json", "live-site verification"),
    ("paired_publications_*.json", "paired-publication snapshot"),
    ("public_source_inventory_*.json", "public-source inventory"),
    ("public_source_snapshot_*.json", "public-source snapshot"),
    ("source_coverage_*.json", "source coverage"),
    ("pages_artifact_growth_*.json", "Pages artifact growth"),
]

# Repository validation deliberately scans hand-authored docs and code examples,
# but never virtual environments, dependency installations, or local build
# caches.  Those trees can contain third-party HTML/Markdown whose links and
# JSON-LD are not site artifacts; allowing an optional QA extra to alter this
# scope would make the release gate environment-dependent.
IGNORED_VALIDATION_PATH_PARTS = frozenset(
    {".git", "_site", ".venv", ".pytest_cache", "__pycache__", "node_modules"}
)


def is_validation_source_path(path: Path) -> bool:
    """Whether a discovered text file belongs to the checkout's source scope."""
    return not bool(IGNORED_VALIDATION_PATH_PARTS.intersection(path.parts))


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def run_resume_check() -> None:
    """Use the locked ReportLab environment for byte-for-byte PDF checks.

    ReportLab embeds its own version/vendor string in the PDF header and metadata.
    The repository pins that dependency in pyproject.toml; invoking the check via
    uv keeps local and CI validation on the same deterministic runtime instead of
    accidentally using a globally installed ReportLab version.
    """
    subprocess.run(
        ["uv", "run", "python3", "code/orchestrators/build_resume.py", "--check"],
        cwd=REPO_ROOT,
        check=True,
    )


def run_local_generation_checks() -> None:
    """Run the mechanically paired no-write checks for every local writer."""
    validate_generation_plan()
    for step in LOCAL_GENERATION_STEPS:
        if step.script == "build_resume.py":
            run_resume_check()
            continue
        run(["python3", f"code/orchestrators/{step.script}", *step.check_args])


def public_source_review_check_args(*, release: bool) -> list[str]:
    """Render the provenance mode required by the validation tier."""
    command = ["python3", "code/orchestrators/build_public_source_review.py", "--check"]
    if release:
        command.append("--exact-source-revision")
    return command


def live_site_check_args(*, release: bool) -> list[str]:
    """Render the cached-live-site check appropriate to the validation tier.

    A candidate can legitimately change source-derived counts before Pages has
    deployed it. Normal offline validation still checks the last known live
    route health, but must not require the old deployment to impersonate the
    candidate. Release validation invokes the strict form only after fresh
    deployed evidence is present.
    """
    command = ["python3", "code/orchestrators/verify_live_site.py", "--check"]
    if not release:
        command.append("--allow-source-count-drift")
    return command


def _load_json_payload(
    path: Path,
    errors: list[str],
    warnings: list[str],
    *,
    optional: bool = False,
) -> None:
    try:
        with path.open(encoding="utf-8") as f:
            json.load(f)
    except FileNotFoundError:
        message = f"Missing JSON artifact: {path}"
        if optional:
            warnings.append(message)
        else:
            errors.append(message)
    except json.JSONDecodeError as exc:
        if optional:
            warnings.append(f"Invalid JSON artifact {path}: {exc}")
        else:
            errors.append(f"Invalid JSON artifact {path}: {exc}")


def validate_json_files(
    strict_reports: bool,
    *,
    repo_root: Path | None = None,
    required_json_files: list[str] | None = None,
    optional_report_patterns: list[tuple[str, str]] | None = None,
) -> None:
    """Validate required JSON artifacts and report artifacts.

    Required artifacts are always strict. Optional report artifacts are warnings by
    default, but strict when --strict-reports is enabled.  ``repo_root`` and the
    two artifact collections make this check reusable against a concrete
    temporary checkout without mutating module-level production configuration.
    """
    root = repo_root or REPO_ROOT
    report_dir = root / "reports"
    required_paths = REQUIRED_JSON_FILES if required_json_files is None else required_json_files
    report_patterns = OPTIONAL_REPORT_PATTERNS if optional_report_patterns is None else optional_report_patterns
    errors: list[str] = []
    warnings: list[str] = []

    for rel_path in required_paths:
        _load_json_payload(root / rel_path, errors, warnings, optional=False)

    for pattern, label in report_patterns:
        report = latest_report(pattern, required=False, report_dir=report_dir)
        if not report:
            message = f"Optional {label} report missing: {pattern}"
            if strict_reports:
                errors.append(message)
            else:
                warnings.append(message)
            continue
        _load_json_payload(report, errors, warnings, optional=not strict_reports)

    browser_smoke = latest_subdir_file(
        "browser-smoke", "manifest.json", required=False, report_dir=report_dir
    )
    if not browser_smoke:
        message = "Optional browser-smoke manifest missing: browser-smoke/manifest.json"
        if strict_reports:
            errors.append(message)
        else:
            warnings.append(message)
    else:
        _load_json_payload(browser_smoke, errors, warnings, optional=not strict_reports)

    browser_qa = latest_subdir_file(
        "browser-qa", "manifest.json", required=False, report_dir=report_dir
    )
    if not browser_qa:
        message = "Optional progressive browser QA manifest missing: browser-qa/manifest.json"
        if strict_reports:
            errors.append(message)
        else:
            warnings.append(message)
    else:
        _load_json_payload(browser_qa, errors, warnings, optional=not strict_reports)

    if warnings:
        print("optional artifact warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        raise SystemExit("JSON artifact validation failed:\n" + "\n".join(f"  - {e}" for e in errors))


def validate_citation_cff() -> None:
    text = (REPO_ROOT / "CITATION.cff").read_text(encoding="utf-8")
    required = ["cff-version:", "message:", "title:", "authors:", "repository-code:", "url:", "date-released:"]
    missing = [key for key in required if key not in text]
    if missing:
        raise SystemExit("CITATION.cff missing keys: " + ", ".join(missing))


def validate_paper_citation_cff(repo_root: Path = REPO_ROOT) -> None:
    """Reject paper CFF files whose DOI roles drift from reviewed metadata.

    This repeats the exact no-write rendering used by the generation plan so a
    direct repository-validation call remains a precise, independently
    testable release invariant.  The renderer owns only DOI-role fields and
    preserves other hand-curated CFF identifiers.
    """
    from generate_citation_cff import render_outputs
    from generated_outputs import stale_output_paths

    papers_dir = repo_root / "papers"
    if not papers_dir.is_dir():
        raise SystemExit(f"Paper CFF DOI-role validation requires {papers_dir}")
    stale = stale_output_paths(render_outputs(papers_dir), repo_root=repo_root)
    if stale:
        shown = "\n".join(f"  - {path.relative_to(repo_root)}" for path in stale)
        raise SystemExit(f"Paper CITATION.cff DOI-role drift:\n{shown}")


def validate_xml_files() -> None:
    for rel in ["feed.xml", "opensearch.xml", "sitemap.xml"]:
        ET.parse(REPO_ROOT / rel)


def validate_json_ld() -> None:
    pattern = re.compile(r"<script\s+type=[\"']application/ld\+json[\"']>(.*?)</script>", re.S | re.I)
    count = 0
    for path in sorted(REPO_ROOT.rglob("*.html")):
        if not is_validation_source_path(path):
            continue
        text = path.read_text(encoding="utf-8")
        for block in pattern.findall(text):
            json.loads(block)
            count += 1
    if count == 0:
        raise SystemExit("No JSON-LD blocks found")


def strip_fenced_code_blocks(text: str) -> str:
    return re.sub(r"(?ms)^(```|~~~)[^\n]*\n.*?^\1[ \t]*$", "", text)


def iter_local_links(text: str) -> list[str]:
    text = strip_fenced_code_blocks(text)
    md_link = re.compile(r"\[[^\]]+\]\((<[^>]+>|[^)]+)\)")
    html_link = re.compile(r"\b(?:href|src)=['\"]([^'\"]+)['\"]")
    return md_link.findall(text) + html_link.findall(text)


def validate_local_links() -> None:
    files = list(REPO_ROOT.rglob("*.md")) + list(REPO_ROOT.rglob("*.html")) + [REPO_ROOT / "llms.txt"]
    missing: list[str] = []
    for path in files:
        if not is_validation_source_path(path):
            continue
        # full_text.md files are extracted paper texts with internal academic references
        # (to figures, source code, manuscript sections) that don't exist as local files.
        if path.name == "full_text.md":
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for raw in iter_local_links(text):
            link = raw.strip()
            if link.startswith("<") and link.endswith(">"):
                link = link[1:-1]
            if not link or link.startswith(("#", "http://", "https://", "mailto:", "tel:", "javascript:", "data:")):
                continue
            if "${" in link or "{" in link:
                continue
            link = urllib.parse.unquote(link.split("#", 1)[0].split("?", 1)[0])
            if not link:
                continue
            target = (REPO_ROOT / link.lstrip("/")) if link.startswith("/") else (path.parent / link).resolve()
            if not target.exists():
                try:
                    target_display = target.relative_to(REPO_ROOT)
                except ValueError:
                    target_display = target
                missing.append(f"{path.relative_to(REPO_ROOT)}: {raw} -> {target_display}")
    if missing:
        raise SystemExit("Missing local links:\n" + "\n".join(missing[:120]))


def validate_count_consistency() -> None:
    sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
    from count_consistency import collect_count_drift

    errors = collect_count_drift()
    if errors:
        raise SystemExit("Volatile count drift:\n" + "\n".join(f"  - {e}" for e in errors))


def validate_sitemap_targets() -> None:
    text = (REPO_ROOT / "sitemap.xml").read_text(encoding="utf-8")
    locs = re.findall(r"<loc>https://danielarifriedman\.com/([^<]*)</loc>", text)
    missing = []
    for loc in locs:
        rel = "index.html" if loc == "" else urllib.parse.unquote(loc)
        if rel.endswith("/"):
            rel += "index.html"
        if not (REPO_ROOT / rel).exists():
            missing.append(rel)
    if missing:
        raise SystemExit("Sitemap targets missing locally: " + ", ".join(missing))


def validate_seo_invariants() -> None:
    sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
    from seo_invariants import collect_seo_errors

    errors = collect_seo_errors(REPO_ROOT)
    if errors:
        raise SystemExit("SEO invariant violations:\n" + "\n".join(f"  - {e}" for e in errors[:40]))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict-reports",
        action="store_true",
        help="Fail when optional report artifacts are missing or invalid.",
    )
    parser.add_argument(
        "--release",
        action="store_true",
        help="Require fresh, revision-bound evidence and a post-deploy attestation for a clean release commit.",
    )
    parser.add_argument(
        "--release-commit",
        help="Commit SHA to validate for --release (default: HEAD).",
    )
    parser.add_argument(
        "--deployment-attestation",
        type=Path,
        help="Post-deploy receipt created by attest_release.py; required with --release.",
    )
    parser.add_argument(
        "--max-report-age-days",
        type=int,
        default=30,
        help="Maximum evidence/attestation age for --release (default: 30).",
    )
    return parser.parse_args()


def _strict_reports_enabled(cli_value: bool) -> bool:
    return cli_value or os.environ.get("DOCXOLOGY_STRICT_REPORTS", "").lower() in {"1", "true", "yes", "on"}


def _resolve_release_commit(value: str | None) -> str:
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


def _head_commit() -> str:
    return _resolve_release_commit("HEAD")


def release_commit_errors(release_commit: str, head_commit: str) -> list[str]:
    """Return the candidate-checkout invariant without querying Git twice."""
    if release_commit == head_commit:
        return []
    return [
        "--release-commit must resolve to the current HEAD; validate another SHA from a checkout at that exact commit"
    ]


def _release_worktree_errors(repo_root: Path = REPO_ROOT) -> list[str]:
    """Require clean release source while allowing local output and fresh receipts."""
    result = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=repo_root,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return ["unable to inspect release worktree"]
    changed: list[str] = []
    records = result.stdout.split(b"\0")
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        if len(record) < 4 or record[2:3] != b" ":
            return ["unable to parse NUL-delimited release worktree status"]
        status = record[:2].decode("ascii", errors="replace")
        raw_paths = [os.fsdecode(record[3:])]
        if "R" in status or "C" in status:
            if index >= len(records) or not records[index]:
                return ["unable to parse renamed release worktree status"]
            raw_paths.append(os.fsdecode(records[index]))
            index += 1
        for path in raw_paths:
            if "\\" in path:
                changed.append(path)
                continue
            # Do not whitelist an ambiguous current-directory spelling.
            if path.startswith("./"):
                changed.append(path)
                continue
            if path == "_site" or path.startswith("_site/"):
                continue
            if is_ephemeral_release_evidence_path(path):
                continue
            changed.append(path)
    if not changed:
        return []
    shown = ", ".join(changed[:10])
    suffix = " …" if len(changed) > 10 else ""
    return [f"release source worktree is not clean: {shown}{suffix}"]


def validate_release_evidence(args: argparse.Namespace) -> None:
    """Fail closed unless a deployed SHA has a current content-addressed receipt."""
    if args.max_report_age_days < 0:
        raise SystemExit("--max-report-age-days must be non-negative")
    errors = _release_worktree_errors()
    if not args.deployment_attestation:
        errors.append("--release requires --deployment-attestation from attest_release.py")
    else:
        attestation = args.deployment_attestation
        if not attestation.is_absolute():
            attestation = REPO_ROOT / attestation
        commit = _resolve_release_commit(args.release_commit)
        errors.extend(release_commit_errors(commit, _head_commit()))
        errors.extend(
            validate_attestation(
                REPO_ROOT,
                attestation,
                commit,
                max_age_days=args.max_report_age_days,
            )
        )
    if errors:
        raise SystemExit("Release evidence validation failed:\n" + "\n".join(f"  - {error}" for error in errors))
    print("Release evidence validation completed (fresh reports and deployed-SHA attestation verified)")


def run_standard_validation(*, strict_reports: bool) -> None:
    """Validate the committed source layer and its deterministic cache inputs."""
    run_local_generation_checks()
    run(["python3", "code/orchestrators/build_github_inventory.py", "--check"])
    run(["python3", "code/orchestrators/sync_paired_publications.py", "--check"])
    run(["python3", "code/orchestrators/audit_publication_skills.py", "--check"])
    run(["python3", "code/orchestrators/check_external_links.py", "--check"])
    run(["python3", "code/orchestrators/build_external_link_triage.py", "--check"])
    run(["python3", "code/orchestrators/browser_smoke.py", "--check"])
    run(live_site_check_args(release=False))
    run(["python3", "code/orchestrators/refresh_public_source_inventory.py", "--check"])
    # The committed source layer uses the control-tail payload anchor.  Exact
    # candidate-HEAD review provenance is checked separately after deployment.
    run(public_source_review_check_args(release=False))
    if strict_reports:
        scholar_errors = scholar_source_receipt_errors(REPO_ROOT)
        if scholar_errors:
            raise SystemExit(
                "Scholar receipt validation failed:\n"
                + "\n".join(f"  - {error}" for error in scholar_errors)
            )
    run(["python3", "code/orchestrators/visual_qa.py", "--check"])
    validate_json_files(strict_reports)
    validate_citation_cff()
    validate_paper_citation_cff()
    validate_xml_files()
    validate_json_ld()
    validate_local_links()
    validate_count_consistency()
    validate_sitemap_targets()
    validate_seo_invariants()
    sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
    from public_integrity import validate_public_files

    validate_public_files(REPO_ROOT)


def run_isolated_candidate_validation(
    candidate_commit: str,
    *,
    repo_root: Path = REPO_ROOT,
    validator_command: tuple[str, ...] | None = None,
) -> None:
    """Run normal strict validation in a temporary clean worktree at ``HEAD``.

    Post-deploy reports are intentionally created in the real checkout after a
    candidate is committed.  Several normal generators correctly consume the
    latest checked-in report cache, so re-running them beside fresh receipts
    would falsely report source drift.  A detached worktree gives ordinary
    validation the exact committed source view without weakening either the
    normal validators or the outer release-evidence checks.

    ``validator_command`` is an internal real-subprocess seam for local Git
    fixture tests.  Production always invokes this validator without
    ``--release`` to avoid recursion.
    """
    command = validator_command or (
        sys.executable,
        "code/orchestrators/validate_repo.py",
        "--strict-reports",
    )
    with tempfile.TemporaryDirectory(prefix="docxology-release-") as temporary_root:
        candidate_root = Path(temporary_root) / "candidate"
        subprocess.run(
            ["git", "worktree", "add", "--detach", str(candidate_root), candidate_commit],
            cwd=repo_root,
            check=True,
        )
        try:
            print("Validating committed release source in an isolated worktree")
            subprocess.run(list(command), cwd=candidate_root, check=True)
        finally:
            # This directory was created solely under TemporaryDirectory above;
            # remove only that exact disposable detached worktree.
            subprocess.run(
                ["git", "worktree", "remove", "--force", str(candidate_root)],
                cwd=repo_root,
                check=True,
            )


def main() -> None:
    args = parse_args()
    strict_reports = _strict_reports_enabled(args.strict_reports)
    if args.release:
        if args.max_report_age_days < 0:
            raise SystemExit("--max-report-age-days must be non-negative")
        release_commit = _resolve_release_commit(args.release_commit)
        commit_errors = release_commit_errors(release_commit, _head_commit())
        if commit_errors:
            raise SystemExit("Release evidence validation failed:\n" + "\n".join(f"  - {error}" for error in commit_errors))
        worktree_errors = _release_worktree_errors()
        if worktree_errors:
            raise SystemExit("Release evidence validation failed:\n" + "\n".join(f"  - {error}" for error in worktree_errors))
        # This is the one post-deploy renderer whose exact candidate revision
        # is itself attested.  Keep it in the real checkout so it verifies the
        # fresh JSON *and* Markdown review pair; all normal source generators
        # run below in the isolated committed worktree.
        run(public_source_review_check_args(release=True))
        run_isolated_candidate_validation(release_commit)
        # The isolated source check intentionally permits a cached report to
        # describe the prior deployment. The real checkout now has the
        # post-deploy receipt, so require its count inputs to match exactly.
        run(live_site_check_args(release=True))
        validate_release_evidence(args)
    else:
        run_standard_validation(strict_reports=strict_reports)
    print("Repository validation completed")


if __name__ == "__main__":
    main()
