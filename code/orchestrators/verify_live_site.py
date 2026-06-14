#!/usr/bin/env python3
"""Verify the deployed GitHub Pages site against expected public artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

try:
    from report_paths import dated_report_path, generated_timestamp, latest_report
except ImportError:  # pragma: no cover - package import path
    from .report_paths import dated_report_path, generated_timestamp, latest_report

OUT = dated_report_path("live_site_verification", "json")
BASE = "https://danielarifriedman.com/"

CHECKS = [
    {"path": "", "markers": ["167 Works", "299", "search.html", "Last updated: May 2026"]},
    {"path": "search.html", "markers": ["Search", "search-index.json", "OpenSearch"]},
    {"path": "catalog.html", "markers": ["Data Catalog", "data/catalog.json", "Search Index"]},
    {"path": "updates.html", "markers": ["Updates", "update-card"]},
    {"path": "opensearch.xml", "markers": ["OpenSearchDescription", "search.html?q={searchTerms}"]},
    {"path": "sitemap.xml", "markers": ["search.html", "catalog.html", "updates.html"]},
    {"path": "llms.txt", "markers": ["Human search page", "Data catalog", "Agent start guide"]},
    {"path": "search-index.json", "markers": ['"count"', '"items"', "Active Inference"]},
    {"path": "data/catalog.json", "markers": ["DataCatalog", "External Link Triage", "Asset Size Audit"]},
    {"path": "GENERATED.md", "markers": ["Generated Files", "Live site verification"]},
    {"path": "humans.txt", "markers": ["Daniel Ari Friedman", "docxology"]},
    {"path": ".well-known/security.txt", "markers": ["Contact:", "Policy:"]},
]


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
    results = []
    for check in CHECKS:
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
    if args.check:
        out = latest_report("live_site_verification_*.json")
        if not out.exists():
            raise SystemExit("Missing live-site verification report")
        payload = json.loads(out.read_text(encoding="utf-8"))
        if not payload.get("results"):
            raise SystemExit("Live-site verification report has no results")
        if not payload.get("overall_ok"):
            raise SystemExit(
                f"Live-site verification report is not passing: {payload.get('passing')}/{payload.get('checked_urls')}"
            )
        print(f"checked live-site verification report ({payload['passing']}/{payload['checked_urls']} passing)")
        return
    payload = build_report(args.timeout)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote live-site verification report: {payload['passing']}/{payload['checked_urls']} passing; pages={payload['github_pages'].get('status', 'unknown')}")


if __name__ == "__main__":
    main()
