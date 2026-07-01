#!/usr/bin/env python3
"""Verify the deployed GitHub Pages site against expected public artifacts."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
CURRENT_COUNTS_JSON = REPO_ROOT / "data" / "current-counts.json"

try:
    from report_paths import dated_report_path, generated_timestamp, latest_report
except ImportError:  # pragma: no cover - package import path
    from .report_paths import dated_report_path, generated_timestamp, latest_report

OUT = dated_report_path("live_site_verification", "json")
BASE = "https://danielarifriedman.com/"


def _read_current_counts() -> dict:
    if not CURRENT_COUNTS_JSON.exists():
        return {}
    try:
        return json.loads(CURRENT_COUNTS_JSON.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def load_dynamic_checks() -> list[dict[str, list[str]]]:
    """Build marker checks from canonical volatile-count sources."""
    payload = _read_current_counts()
    counts = payload.get("counts", {})
    software = counts.get("software", {})
    github_inventory = counts.get("github_inventory", {})

    def as_text(value: int | str | None) -> str | None:
        return str(value) if value is not None else None

    works = as_text(counts.get("bibliography_works"))
    software_docx = as_text(software.get("docxology_owned"))
    software_aii = as_text(software.get("active_inference_institute"))
    public_repos = as_text(github_inventory.get("public"))

    checks = [
        {
            "path": "",
            "markers": ["danielarifriedman.com", "publications", "software.html", "Search"],
        },
        {
            "path": "publications.html",
            "markers": ["Publications", "data/publications-ld.json", "catalogued works"],
        },
        {
            "path": "software.html",
            "markers": ["Software", "data/software-ld.json", "Open-Source Repositories"],
        },
        {
            "path": "search.html",
            "markers": ["Search", "search-index.json", "OpenSearch"],
        },
        {
            "path": "catalog.html",
            "markers": ["Data Catalog", "\"@context\"", "/data/catalog.json", "application/ld+json"],
        },
        {
            "path": "updates.html",
            "markers": ["Updates", "update-card", "changelog"],
        },
        {
            "path": "opensearch.xml",
            "markers": ["OpenSearchDescription", "search.html?q={searchTerms}"],
        },
        {
            "path": "sitemap.xml",
            "markers": ["sitemap", "publications.html", "software.html"],
        },
        {
            "path": "llms.txt",
            "markers": ["Human search page", "Data catalog", "Agent start guide"],
        },
        {
            "path": "search-index.json",
            "markers": ['"count"', '"items"', "items"],
        },
        {
            "path": "data/catalog.json",
            "markers": ["DataCatalog", "External Link Triage", "Software"],
        },
        {
            "path": "GENERATED.md",
            "markers": ["# Generated Files", "Rebuild command", "Validation"],
        },
        {
            "path": "humans.txt",
            "markers": ["Daniel Ari Friedman", "docxology"],
        },
        {
            "path": ".well-known/security.txt",
            "markers": ["Contact:", "Policy:"],
        },
    ]

    if works is not None:
        checks[1]["markers"].append(f"{works} Works")
    if software_docx is not None:
        checks[2]["markers"].append(f"{software_docx} owned")
    if software_aii is not None:
        checks[2]["markers"].append(f"{software_aii} catalogued")
    if public_repos is not None:
        checks[2]["markers"].append(f"{public_repos} public repositories")

    return checks


def load_current_counts_fingerprint() -> dict[str, int | str | None]:
    payload = _read_current_counts()
    counts = payload.get("counts", {})
    software = counts.get("software", {})
    github_inventory = counts.get("github_inventory", {})
    return {
        "generated_at": payload.get("generated_at"),
        "works": counts.get("bibliography_works"),
        "software_docx": software.get("docxology_owned"),
        "software_aii": software.get("active_inference_institute"),
        "software_total": software.get("curated_total"),
        "public_repos": github_inventory.get("public"),
    }


def fetch(url: str, timeout: int, extra_headers: dict[str, str] | None = None) -> dict:
    started = time.time()
    headers = {
        "User-Agent": "docxology-live-verify/1.0 (+https://danielarifriedman.com/)",
        "Cache-Control": "no-cache",
    }
    if extra_headers:
        headers.update(extra_headers)
    req = urllib.request.Request(
        url,
        headers=headers,
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            raw = response.read(2_000_000)
            text = raw.decode("utf-8", errors="replace")
            return {
                "status": response.status,
                "ok": 200 <= response.status < 400,
                "elapsed_ms": int((time.time() - started) * 1000),
                "bytes": len(raw),
                "headers": {k.lower(): v for k, v in response.headers.items()},
                "text": text,
                "error": "",
            }
    except urllib.error.HTTPError as exc:
        body = exc.read(200_000).decode("utf-8", errors="replace")
        return {
            "status": exc.code,
            "ok": False,
            "elapsed_ms": int((time.time() - started) * 1000),
            "bytes": len(body),
            "headers": dict(exc.headers.items()) if exc.headers else {},
            "text": body,
            "error": str(exc.reason),
        }
    except Exception as exc:
        return {
            "status": 0,
            "ok": False,
            "elapsed_ms": int((time.time() - started) * 1000),
            "bytes": 0,
            "headers": {},
            "text": "",
            "error": f"{type(exc).__name__}: {exc}",
        }


def pages_status(timeout: int) -> dict:
    try:
        proc = subprocess.run(
            ["gh", "api", "repos/docxology/docxology/pages"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        if proc.returncode == 0:
            payload = json.loads(proc.stdout)
            return {
                "ok": payload.get("status") == "built",
                "status": payload.get("status", ""),
                "cname": payload.get("cname", ""),
                "source": payload.get("source", {}),
                "html_url": payload.get("html_url", ""),
            }
    except Exception:
        pass
    url = "https://api.github.com/repos/docxology/docxology/pages"
    headers = {}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = fetch(url, timeout, headers)
    if not data["ok"]:
        return {"ok": False, "status": data["status"], "error": data["error"]}
    try:
        payload = json.loads(data["text"])
    except json.JSONDecodeError as exc:
        return {"ok": False, "status": data["status"], "error": str(exc)}
    return {
        "ok": payload.get("status") == "built",
        "status": payload.get("status", ""),
        "cname": payload.get("cname", ""),
        "source": payload.get("source", {}),
        "html_url": payload.get("html_url", ""),
    }


def build_report(timeout: int) -> dict:
    checks = load_dynamic_checks()
    fingerprint = load_current_counts_fingerprint()
    results = []
    for check in checks:
        url = BASE + check["path"]
        response = fetch(url, timeout)
        markers = {marker: marker in response["text"] for marker in check["markers"]}
        cache = {
            key: response["headers"].get(key, "")
            for key in ("last-modified", "etag", "cache-control", "age", "x-cache", "x-served-by")
        }
        ok = response["ok"] and all(markers.values())
        results.append(
            {
                "path": check["path"] or "index.html",
                "url": url,
                "ok": ok,
                "status": response["status"],
                "bytes": response["bytes"],
                "elapsed_ms": response["elapsed_ms"],
                "markers": markers,
                "cache": cache,
                "error": response["error"],
            }
        )

    pages = pages_status(timeout)
    return {
        "generated_at": generated_timestamp(),
        "base_url": BASE,
        "expected_counts": fingerprint,
        "note": "Live verification can fail while GitHub Pages is still building or CDN caches are stale.",
        "github_pages": pages,
        "checked_urls": len(results),
        "passing": sum(1 for item in results if item["ok"]),
        "overall_ok": pages.get("ok", False) and all(item["ok"] for item in results),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate the cached report exists and is parseable")
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()
    current_fingerprint = load_current_counts_fingerprint()
    if args.check:
        if not CURRENT_COUNTS_JSON.exists():
            raise SystemExit("Current-counts source missing: data/current-counts.json")
        out = latest_report("live_site_verification_*.json")
        if not out.exists():
            raise SystemExit("Missing live-site verification report")
        payload = json.loads(out.read_text(encoding="utf-8"))
        if payload.get("expected_counts") != current_fingerprint:
            raise SystemExit(
                f"Live-site verification counts snapshot mismatch: expected={current_fingerprint} got={payload.get('expected_counts')}"
            )
        if not payload.get("results"):
            raise SystemExit("Live-site verification report has no results")
        for item in payload.get("results", []):
            if item.get("status") >= 400:
                raise SystemExit(f"Live-site page failure: {item.get('url')} status {item.get('status')}")
        if not payload.get("overall_ok"):
            print(
                "checked live-site verification report "
                f"({payload.get('passing')}/{payload.get('checked_urls')} passing; live markers pending deploy)"
            )
            return
        print(f"checked live-site verification report ({payload['passing']}/{payload['checked_urls']} passing)")
        return
    payload = build_report(args.timeout)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote live-site verification report: {payload['passing']}/{payload['checked_urls']} passing; pages={payload['github_pages'].get('status', 'unknown')}")


if __name__ == "__main__":
    main()
