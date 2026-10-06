#!/usr/bin/env python3
"""Preflight checks before manual Google Search Console follow-up.

Local checks: sitemap URL count and no ``/papers/`` entries, SEO invariants, open
crawl in ``robots.txt``, a sitemap-file guard (``sitemap.xml`` is the only root
sitemap file and ``robots.txt`` names exactly that one ``Sitemap:``), and a
priority-URL guard (every priority URL is in the sitemap and not ``noindex``).
Live checks: HTTP readiness of the priority hubs, redirect stubs and
``sitemap.xml``, plus a 404/410 probe for each retired sitemap path. Prints GSC
deep links and a copy-paste checklist.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]

from docxology_tools.sitemap_policy import RETIRED_SITEMAP_PATHS, SITE_ORIGIN, gsc_priority_urls  # noqa: E402
from build_sitemap import sitemap_locs  # noqa: E402

from docxology_tools.report_paths import dated_report_path, generated_timestamp  # noqa: E402

from docxology_tools.seo_invariants import REDIRECT_STUBS, collect_seo_errors  # noqa: E402

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
        "id": "gsc-remove-retired-sitemap",
        "title": "Remove the retired sitemap entry",
        "gsc_url": GSC_LINKS["sitemaps"],
        "action": (
            f"Sitemaps → open the row for {', '.join(RETIRED_SITEMAP_PATHS)} → remove it; "
            "it returns 404 by design, so never recreate or resubmit it"
        ),
    },
    {
        "id": "gsc-index-hubs",
        "title": "Request indexing for priority URLs",
        "gsc_url": GSC_LINKS["url_inspection"],
        "action": "URL Inspection → Request indexing for each priority URL",
    },
    {
        "id": "gsc-review-exclusions",
        "title": "Review exclusions; Validate fix only after a real fix",
        "gsc_url": GSC_LINKS["page_indexing"],
        "action": (
            "Page indexing → Why pages aren’t indexed → compare each bucket with the "
            "legitimate-exclusion list in docs/seo/gsc-followup.md; use Validate fix only "
            "for a site change that is live across all affected URLs"
        ),
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


# An unterminated comment swallows the rest of the document, as it does in a browser.
_HTML_COMMENT = re.compile(r"<!--.*?(?:-->|\Z)", re.S)
# A <meta> start tag whose quoted attribute values may themselves contain ">".
_META_TAG = re.compile(r"""<meta\b(?:[^>"']|"[^"]*"|'[^']*')*>""", re.I)
# One attribute: name, then a double-quoted, single-quoted, or unquoted value.
_META_ATTR = re.compile(r"""([^\s"'<>/=]+)\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'<>=`]+))""")
# Meta names whose directives reach Google web search.
_ROBOTS_META_NAMES = frozenset({"robots", "googlebot"})
# "none" is shorthand for "noindex, nofollow".
_NOINDEX_DIRECTIVES = frozenset({"noindex", "none"})
_ROBOTS_SITEMAP_LINE = re.compile(r"^\s*sitemap\s*:\s*(\S*)", re.I | re.M)


def sitemap_file_problems(root: Path) -> list[str]:
    """Problems with the sitemap files a crawler can discover under ``root``.

    The only root-level file matching ``*sitemap*.xml`` is ``sitemap.xml``, and
    ``robots.txt`` carries exactly one ``Sitemap:`` line, equal to the canonical
    sitemap URL. The guard is class-based: it rejects any extra sitemap file or
    robots reference rather than naming one retired file.
    """
    problems: list[str] = []
    extras = sorted(
        entry.name
        for entry in root.iterdir()
        if entry.is_file() and fnmatch.fnmatch(entry.name.lower(), "*sitemap*.xml") and entry.name != "sitemap.xml"
    )
    if extras:
        problems.append("extra root sitemap file(s): " + ", ".join(extras))
    robots_path = root / "robots.txt"
    if not robots_path.is_file():
        problems.append("robots.txt is missing")
        return problems
    declared = _ROBOTS_SITEMAP_LINE.findall(robots_path.read_text(encoding="utf-8"))
    canonical = SITE_ORIGIN + "sitemap.xml"
    if len(declared) != 1:
        problems.append(f"robots.txt has {len(declared)} Sitemap: lines (expected exactly 1)")
    stray = [url for url in declared if url != canonical]
    if stray:
        problems.append("robots.txt Sitemap: not canonical: " + ", ".join(stray))
    return problems


def priority_local_path(url: str) -> str | None:
    """Repo-relative file that serves ``url`` (``''`` -> ``index.html``, ``x/`` -> ``x/index.html``)."""
    if not url.startswith(SITE_ORIGIN):
        return None
    rel = url.removeprefix(SITE_ORIGIN)
    if rel == "" or rel.endswith("/"):
        rel += "index.html"
    return rel


def has_noindex_robots_meta(html: str) -> bool:
    """True when a ``<meta name="robots">`` or ``<meta name="googlebot">`` tag blocks indexing.

    A tag blocks indexing when its ``content`` lists the ``noindex`` or ``none``
    directive. Attribute order and quoting (double, single, or none) do not
    matter, and HTML comments are ignored because a browser or crawler never
    sees a tag inside one.
    """
    # Robots meta tags belong in <head>; scanning only the head also bounds the
    # tag regex, which backtracks on malformed quoting in very long documents.
    head = re.split(r"</head\s*>", html, maxsplit=1, flags=re.I)[0]
    for tag in _META_TAG.findall(_HTML_COMMENT.sub("", head)):
        attrs: dict[str, str] = {}
        for name, double, single, bare in _META_ATTR.findall(tag):
            value = double or single or bare.rstrip("/")
            attrs.setdefault(name.lower(), value)  # the first duplicate attribute wins
        if attrs.get("name", "").strip().lower() not in _ROBOTS_META_NAMES:
            continue
        directives = {token for token in re.split(r"[\s,;]+", attrs.get("content", "").lower()) if token}
        if directives & _NOINDEX_DIRECTIVES:
            return True
    return False


def priority_url_problems(root: Path, urls: list[str], sitemap_urls: set[str]) -> list[str]:
    """Priority URLs that are not sitemap members, have no local file, or are ``noindex``."""
    problems: list[str] = []
    for url in urls:
        if url not in sitemap_urls:
            problems.append(f"{url}: not in the sitemap")
        rel = priority_local_path(url)
        if rel is None:
            problems.append(f"{url}: outside {SITE_ORIGIN}")
            continue
        page = root / rel
        if not page.is_file():
            problems.append(f"{url}: {rel} not found")
        elif has_noindex_robots_meta(page.read_text(encoding="utf-8", errors="replace")):
            problems.append(f"{url}: {rel} is noindex")
    return problems


def retired_sitemap_row(path: str, hit: dict | None) -> dict:
    """Live-check row for a retired sitemap: healthy means HTTP 404 or 410.

    ``fetch_status`` reports ``ok`` False for 404, the opposite of what a retired
    sitemap needs, so the verdict is computed here from the status code. A network
    error (no status) is never healthy: the sitemap's absence was not confirmed.
    """
    hit = hit or {}
    status = hit.get("status")
    detail = f"HTTP {status} (expected 404 or 410)" if status is not None else f"no HTTP status ({hit.get('error', 'no response')})"
    return {
        "check": f"retired_sitemap_{path}",
        "ok": status in (404, 410),
        "detail": detail,
        "url": hit.get("url", SITE_ORIGIN + path),
    }


def local_checks(repo_root: Path) -> list[dict]:
    results: list[dict] = []
    sitemap = repo_root / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    locs = re.findall(r"<loc>([^<]+)</loc>", text)
    policy_locs = sitemap_locs()
    expected_url_count = len(policy_locs)
    results.append(
        {
            "check": "sitemap_url_count",
            "ok": len(locs) == expected_url_count,
            "detail": f"{len(locs)} URLs (expected {expected_url_count})",
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
    sitemap_problems = sitemap_file_problems(repo_root)
    results.append(
        {
            "check": "sitemap_files_canonical_only",
            "ok": not sitemap_problems,
            "detail": (
                "sitemap.xml is the only root sitemap file; robots.txt names only it"
                if not sitemap_problems
                else "; ".join(sitemap_problems)
            ),
        }
    )
    priority_problems = priority_url_problems(repo_root, gsc_priority_urls(), set(policy_locs))
    results.append(
        {
            "check": "priority_urls_indexable",
            "ok": not priority_problems,
            "detail": (
                f"{len(gsc_priority_urls())} priority URLs in the sitemap and indexable"
                if not priority_problems
                else "; ".join(priority_problems[:3])
            ),
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
    for stub in REDIRECT_STUBS:
        rel = stub.path
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
    for retired in RETIRED_SITEMAP_PATHS:
        results.append(retired_sitemap_row(retired, fetch_status(SITE_ORIGIN + retired)))
    return results


def build_report(repo_root: Path, skip_live: bool) -> dict:
    local = local_checks(repo_root)
    live = [] if skip_live else live_checks()
    preflight_ok = all(row["ok"] for row in local + live)
    priority_paths = ", ".join(
        "/" if url == SITE_ORIGIN else "/" + url.removeprefix(SITE_ORIGIN)
        for url in gsc_priority_urls()
    )
    retired_paths = ", ".join(RETIRED_SITEMAP_PATHS)
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
            f"[ ] Removed the retired sitemap from GSC Sitemaps: {retired_paths}",
            f"[ ] Requested indexing: {priority_paths}",
            "[ ] Reviewed exclusions against the legitimate-exclusion list (Validate fix only after a real, live, site-wide fix)",
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
    print("Full runbook: docs/seo/gsc-followup.md")


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
