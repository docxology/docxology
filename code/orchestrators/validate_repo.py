#!/usr/bin/env python3
"""Validate generated files, structured data, local links, and metadata."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

try:
    from report_paths import latest_report, latest_subdir_file, rel
except ImportError:  # pragma: no cover - package import path
    from .report_paths import latest_report, latest_subdir_file, rel


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, cwd=REPO_ROOT, check=True)


def validate_json_files() -> None:
    paths = [
        "bibliography.csl.json",
        "codemeta.json",
        "search-index.json",
        "data/catalog.json",
        "data/generated-manifest.json",
        "data/github-repositories.json",
        "data/artworks.json",
        "data/works.json",
        "data/work-enrichment.json",
        "data/software-ld.json",
        "data/software.json",
        "data/people.json",
        "data/organizations.json",
        "data/claims.json",
        "data/reconciliation.json",
    ]
    paths.extend(
        [
            rel(latest_report("accessibility_static_*.json")),
            rel(latest_report("asset_size_*.json")),
            rel(latest_subdir_file("browser-smoke", "manifest.json")),
            rel(latest_report("external_links_[0-9]*.json")),
            rel(latest_report("external_links_triage_*.json")),
            rel(latest_report("live_site_verification_*.json")),
            rel(latest_report("public_source_inventory_*.json")),
            rel(latest_report("public_source_snapshot_*.json")),
        ]
    )
    for path_rel in paths:
        with open(REPO_ROOT / path_rel, encoding="utf-8") as f:
            json.load(f)


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


def iter_local_links(text: str) -> list[str]:
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
        if not (REPO_ROOT / rel).exists():
            missing.append(rel)
    if missing:
        raise SystemExit("Sitemap targets missing locally: " + ", ".join(missing))


def main() -> None:
    run(["python3", "papers/sync_publications_html.py"])
    run(["python3", "papers/sync_software_html.py"])
    run(["python3", "code/orchestrators/export_bibliography.py", "--check"])
    run(["python3", "code/orchestrators/export_agent_data.py", "--check"])
    run(["python3", "code/orchestrators/build_domain_pages.py", "--check"])
    run(["python3", "code/orchestrators/build_work_pages.py", "--check"])
    run(["python3", "code/orchestrators/build_catalog.py", "--check"])
    run(["python3", "code/orchestrators/build_updates_page.py", "--check"])
    run(["python3", "code/orchestrators/build_evidence_page.py", "--check"])
    run(["python3", "code/orchestrators/build_reconciliation_report.py", "--check"])
    run(["python3", "code/orchestrators/build_generated_manifest.py", "--check"])
    run(["python3", "code/orchestrators/build_github_inventory.py", "--check"])
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
    validate_json_files()
    validate_citation_cff()
    validate_xml_files()
    validate_json_ld()
    validate_count_consistency()
    validate_local_links()
    validate_sitemap_targets()
    print("repo validation ok")


if __name__ == "__main__":
    main()
