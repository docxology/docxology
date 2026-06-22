#!/usr/bin/env python3
"""Validate generated files, structured data, local links, and metadata."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

try:
    from report_paths import latest_report, latest_subdir_file
except ImportError:  # pragma: no cover - package import path
    from .report_paths import latest_report, latest_subdir_file


REQUIRED_JSON_FILES: list[str] = [
    "bibliography.csl.json",
    "codemeta.json",
    "search-index.json",
    "data/catalog.json",
    "data/current-counts.json",
    "data/generated-manifest.json",
    "data/github-repositories.json",
    "data/artworks.json",
    "data/works.json",
    "data/work-enrichment.json",
    "data/software-ld.json",
    "data/software.json",
    "data/people.json",
    "data/organizations.json",
    "data/paired-publication-decisions.json",
    "data/claims.json",
    "data/resume.json",
    "data/reconciliation.json",
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
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


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


def validate_json_files(strict_reports: bool) -> None:
    """Validate required JSON artifacts and report artifacts.

    Required artifacts are always strict. Optional report artifacts are warnings by
    default, but strict when --strict-reports is enabled.
    """
    errors: list[str] = []
    warnings: list[str] = []

    for rel_path in REQUIRED_JSON_FILES:
        _load_json_payload(REPO_ROOT / rel_path, errors, warnings, optional=False)

    for pattern, label in OPTIONAL_REPORT_PATTERNS:
        report = latest_report(pattern, required=False)
        if not report:
            message = f"Optional {label} report missing: {pattern}"
            if strict_reports:
                errors.append(message)
            else:
                warnings.append(message)
            continue
        _load_json_payload(report, errors, warnings, optional=not strict_reports)

    browser_smoke = latest_subdir_file("browser-smoke", "manifest.json", required=False)
    if not browser_smoke:
        message = "Optional browser-smoke manifest missing: browser-smoke/manifest.json"
        if strict_reports:
            errors.append(message)
        else:
            warnings.append(message)
    else:
        _load_json_payload(browser_smoke, errors, warnings, optional=not strict_reports)

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


def validate_xml_files() -> None:
    for rel in ["feed.xml", "opensearch.xml", "sitemap.xml"]:
        ET.parse(REPO_ROOT / rel)


def validate_json_ld() -> None:
    pattern = re.compile(r"<script\s+type=[\"']application/ld\+json[\"']>(.*?)</script>", re.S | re.I)
    count = 0
    for path in sorted(REPO_ROOT.rglob("*.html")):
        if ".git" in path.parts:
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
        if ".git" in path.parts:
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
    return parser.parse_args()


def _strict_reports_enabled(cli_value: bool) -> bool:
    return cli_value or os.environ.get("DOCXOLOGY_STRICT_REPORTS", "").lower() in {"1", "true", "yes", "on"}


def main() -> None:
    args = parse_args()
    strict_reports = _strict_reports_enabled(args.strict_reports)

    run(["python3", "code/orchestrators/sync_publications_html.py"])
    run(["python3", "code/orchestrators/sync_software_html.py"])
    run(["python3", "code/orchestrators/export_bibliography.py", "--check"])
    run(["python3", "code/orchestrators/export_agent_data.py", "--check"])
    run(["python3", "code/orchestrators/build_resume.py", "--check"])
    run(["python3", "code/orchestrators/build_domain_pages.py", "--check"])
    run(["python3", "code/orchestrators/build_work_pages.py", "--check"])
    run(["python3", "code/orchestrators/build_paper_pages.py", "--check"])
    run(["python3", "code/orchestrators/build_catalog.py", "--check"])
    run(["python3", "code/orchestrators/build_exports_page.py", "--check"])
    run(["python3", "code/orchestrators/build_updates_page.py", "--check"])
    run(["python3", "code/orchestrators/build_evidence_page.py", "--check"])
    run(["python3", "code/orchestrators/build_current_counts.py", "--check"])
    run(["python3", "code/orchestrators/build_reconciliation_report.py", "--check"])
    run(["python3", "code/orchestrators/build_generated_manifest.py", "--check"])
    run(["python3", "code/orchestrators/build_github_inventory.py", "--check"])
    run(["python3", "code/orchestrators/sync_paired_publications.py", "--check"])
    run(["python3", "code/orchestrators/audit_publication_skills.py", "--check"])
    run(["python3", "code/orchestrators/build_search_index.py", "--check"])
    run(["python3", "code/orchestrators/generate_feed.py", "--check"])
    run(["python3", "code/orchestrators/audit_assets.py", "--check"])
    run(["python3", "code/orchestrators/accessibility_audit.py", "--check"])
    run(["python3", "code/orchestrators/build_sitemap.py", "--check"])
    run(["python3", "code/orchestrators/check_external_links.py", "--check"])
    run(["python3", "code/orchestrators/build_external_link_triage.py", "--check"])
    run(["python3", "code/orchestrators/browser_smoke.py", "--check"])
    run(["python3", "code/orchestrators/verify_live_site.py", "--check"])
    run(["python3", "code/orchestrators/refresh_public_source_inventory.py", "--check"])
    run(["python3", "code/orchestrators/visual_qa.py", "--check"])
    validate_json_files(strict_reports)
    validate_citation_cff()
    validate_xml_files()
    validate_json_ld()
    validate_local_links()
    validate_count_consistency()
    validate_sitemap_targets()
    validate_seo_invariants()
    print("Repository validation completed")


if __name__ == "__main__":
    main()
