#!/usr/bin/env python3
"""Preflight checks before manual Google Search Console follow-up.

Verifies local SEO invariants and live HTTP readiness for sitemap, priority hubs,
and redirect stubs. Prints GSC deep links and a copy-paste checklist.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from sitemap_policy import SITE_ORIGIN, gsc_priority_urls  # noqa: E402

try:
    from report_paths import dated_report_path, generated_timestamp
except ImportError:  # pragma: no cover
    from .report_paths import dated_report_path, generated_timestamp

from seo_invariants import REDIRECT_STUBS, collect_seo_errors  # noqa: E402

GSC_BASE = "https://search.google.com/search-console"
PROPERTY = "https://danielarifriedman.com/"

GSC_LINKS = {
    "sitemaps": f"{GSC_BASE}/sitemaps?resource_id={PROPERTY}",
    "url_inspection": f"{GSC_BASE}/inspect?resource_id={PROPERTY}",
    "page_indexing": f"{GSC_BASE}/index?resource_id={PROPERTY}",
    "performance": f"{GSC_BASE}/performance/search-analytics?resource_id={PROPERTY}",
}

MANUAL_STEPS = [
    {
        "id": "gsc-sitemap",
        "title": "Submit or refresh sitemap.xml",
        "gsc_url": GSC_LINKS["sitemaps"],
        "action": "Add sitemap: sitemap.xml → Submit",
    },
    {
        "id": "gsc-index-hubs",
        "title": "Request indexing for 6 priority hubs",
        "gsc_url": GSC_LINKS["url_inspection"],
        "action": "URL Inspection → Request indexing for each priority URL",
    },
    {
        "id": "gsc-validate-redirect",
        "title": "Validate fix: Page with redirect",
        "gsc_url": GSC_LINKS["page_indexing"],
        "action": "Page indexing → Page with redirect → Validate fix",
    },
    {
        "id": "gsc-validate-canonical",
        "title": "Validate fix: Alternate page with proper canonical",
        "gsc_url": GSC_LINKS["page_indexing"],
        "action": "Page indexing → Alternate canonical → Validate fix",
    },
    {
        "id": "gsc-validate-404",
        "title": "Validate fix: Not found (404)",
        "gsc_url": GSC_LINKS["page_indexing"],
        "action": "Page indexing → Not found (404) → Validate fix",
    },
    {
        "id": "gsc-monitor",
        "title": "Weekly Page indexing check (weeks 1–4)",
        "gsc_url": GSC_LINKS["page_indexing"],
        "action": "Review Page indexing + Performance weekly for 2–4 weeks",
    },
]


def fetch_status(url: str, timeout: int = 30) -> dict:
    started = time.time()
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "docxology-gsc-preflight/1.0 (+https://danielarifriedman.com/)",
            "Cache-Control": "no-cache",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return {
                "url": url,
                "status": response.status,
                "ok": 200 <= response.status < 400,
                "elapsed_ms": int((time.time() - started) * 1000),
            }
    except urllib.error.HTTPError as exc:
        return {
            "url": url,
            "status": exc.code,
            "ok": False,
            "elapsed_ms": int((time.time() - started) * 1000),
            "error": str(exc.reason),
        }
    except urllib.error.URLError as exc:
        return {
            "url": url,
            "status": None,
            "ok": False,
            "elapsed_ms": int((time.time() - started) * 1000),
            "error": str(exc.reason),
        }


def local_checks(repo_root: Path) -> list[dict]:
    results: list[dict] = []
    sitemap = repo_root / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", text)
    results.append(
        {
            "check": "sitemap_url_count",
            "ok": 174 <= len(locs) <= 190,
            "detail": f"{len(locs)} URLs (expected ~181)",
        }
    )
    papers_in_sitemap = [loc for loc in locs if "/papers/" in loc]
    results.append(
        {
            "check": "sitemap_excludes_papers",
            "ok": not papers_in_sitemap,
            "detail": "no /papers/ in sitemap" if not papers_in_sitemap else f"found {len(papers_in_sitemap)}",
        }
    )
    seo_errors = collect_seo_errors(repo_root)
    results.append(
        {
            "check": "seo_invariants",
            "ok": not seo_errors,
            "detail": "ok" if not seo_errors else "; ".join(seo_errors[:3]),
        }
    )
    robots = (repo_root / "robots.txt").read_text(encoding="utf-8")
    results.append(
        {
            "check": "robots_open_crawl",
            "ok": "Allow: /" in robots and "Disallow:" not in robots,
            "detail": "Allow: / without Disallow",
        }
    )
    return results


def live_checks() -> list[dict]:
    results: list[dict] = []
    for url in gsc_priority_urls():
        hit = fetch_status(url)
        results.append(
            {
                "check": f"priority_hub_{url.removeprefix(SITE_ORIGIN) or 'home'}",
                "ok": hit["ok"],
                "detail": f"HTTP {hit.get('status')} ({hit['elapsed_ms']}ms)",
                "url": url,
            }
        )
    for rel, _canonical in REDIRECT_STUBS:
        url = SITE_ORIGIN + rel
        hit = fetch_status(url)
        results.append(
            {
                "check": f"redirect_stub_{rel}",
                "ok": hit["ok"],
                "detail": f"HTTP {hit.get('status')}",
                "url": url,
            }
        )
    sitemap_hit = fetch_status(SITE_ORIGIN + "sitemap.xml")
    results.append(
        {
            "check": "live_sitemap",
            "ok": sitemap_hit["ok"],
            "detail": f"HTTP {sitemap_hit.get('status')}",
            "url": SITE_ORIGIN + "sitemap.xml",
        }
    )
    return results


def build_report(repo_root: Path, skip_live: bool) -> dict:
    local = local_checks(repo_root)
    live = [] if skip_live else live_checks()
    preflight_ok = all(row["ok"] for row in local + live)
    return {
        "generated_at": generated_timestamp(),
        "property": PROPERTY,
        "preflight_ok": preflight_ok,
        "local_checks": local,
        "live_checks": live,
        "priority_urls": gsc_priority_urls(),
        "gsc_links": GSC_LINKS,
        "manual_steps": MANUAL_STEPS,
        "checklist": [
            f"[ ] Signed into GSC for {PROPERTY}",
            "[ ] Preflight passed (this script)",
            "[ ] Submitted sitemap.xml",
            "[ ] Requested indexing: /, exports.html, catalog.html, cite-verify.html, discovery.html, publications.html",
            "[ ] Validate fix: Page with redirect",
            "[ ] Validate fix: Alternate page with proper canonical",
            "[ ] Validate fix: Not found (404)",
            "[ ] Calendar reminder: recheck Page indexing in 7 days",
        ],
    }


def print_summary(report: dict) -> None:
    print(f"GSC preflight — property {report['property']}")
    print(f"Overall: {'PASS' if report['preflight_ok'] else 'FAIL'}")
    print()
    print("Local checks:")
    for row in report["local_checks"]:
        mark = "ok" if row["ok"] else "FAIL"
        print(f"  [{mark}] {row['check']}: {row['detail']}")
    if report["live_checks"]:
        print()
        print("Live checks:")
        for row in report["live_checks"]:
            mark = "ok" if row["ok"] else "FAIL"
            print(f"  [{mark}] {row['check']}: {row['detail']}")
    print()
    print("Manual GSC steps (signed-in browser required):")
    for step in report["manual_steps"]:
        print(f"  • {step['title']}")
        print(f"    {step['gsc_url']}")
        print(f"    {step['action']}")
    print()
    print("Checklist:")
    for line in report["checklist"]:
        print(f"  {line}")
    print()
    print("Full runbook: docs/GSC_FOLLOWUP.md")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-live", action="store_true", help="Local SEO checks only (no HTTP)")
    parser.add_argument("--json", action="store_true", help="Write JSON report to reports/")
    parser.add_argument("--check", action="store_true", help="Exit 1 if preflight fails")
    args = parser.parse_args()

    report = build_report(REPO_ROOT, skip_live=args.skip_live)
    print_summary(report)

    if args.json or args.check:
        out = dated_report_path("gsc_preflight", "json")
        out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        checklist_out = REPO_ROOT / "data" / "gsc-followup-checklist.json"
        checklist_out.write_text(
            json.dumps(
                {
                    "generated_at": report["generated_at"],
                    "property": report["property"],
                    "preflight_ok": report["preflight_ok"],
                    "priority_urls": report["priority_urls"],
                    "gsc_links": report["gsc_links"],
                    "manual_steps": report["manual_steps"],
                    "checklist": report["checklist"],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        if args.json:
            print(f"wrote {out.relative_to(REPO_ROOT)}")
            print(f"wrote {checklist_out.relative_to(REPO_ROOT)}")

    if args.check and not report["preflight_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
