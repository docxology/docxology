#!/usr/bin/env python3
"""Check a scoped set of external links and write a cached report.

The default scope is site-critical public pages and hubs, not every paper
folder or art metadata file. That keeps the report useful without hammering
external services with thousands of archive links.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT = REPO_ROOT / "reports" / "external_links_2026-05-13.json"

SCAN_FILES = [
    "index.html",
    "publications.html",
    "software.html",
    "domains.html",
    "discovery.html",
    "cite-verify.html",
    "evidence.html",
    "search.html",
    "catalog.html",
    "updates.html",
    "README.md",
    "AGENT_START.md",
    "llms.txt",
    "humans.txt",
    "CITATION.cff",
    "codemeta.json",
    "pages/README.md",
    "pages/LINKS.md",
    "pages/DISCOVERY.md",
    "pages/CITE_VERIFY.md",
    "pages/EVIDENCE.md",
    "pages/DOMAINS.md",
    "pages/PROFILE.md",
    "pages/SOFTWARE.md",
    "pages/BIBLIOGRAPHY.md",
]

URL_RE = re.compile(r"https?://[^\s\]\"'<>)]+")
IGNORE_HOSTS = {
    "danielarifriedman.com",
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "github-contributor-stats.vercel.app",
    "github-readme-stats.vercel.app",
    "img.shields.io",
    "localhost",
    "nirzak-streak-stats.vercel.app",
    "127.0.0.1",
    "visitcount.itsvg.in",
}
IGNORE_PREFIXES = (
    "https://github.com/docxology/docxology/blob/main/",
)


def clean_url(url: str) -> str:
    return url.rstrip(".,;`\\")


def collect_urls() -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for rel in SCAN_FILES:
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for raw in URL_RE.findall(text):
            url = clean_url(raw)
            if any(url.startswith(prefix) for prefix in IGNORE_PREFIXES):
                continue
            host = urlparse(url).netloc.lower()
            if host in IGNORE_HOSTS:
                continue
            found.setdefault(url, []).append(rel)
    return found


def curl_probe(url: str, method: str, timeout: int) -> dict:
    args = [
        "curl",
        "--location",
        "--silent",
        "--show-error",
        "--output",
        "/dev/null",
        "--max-time",
        str(timeout),
        "--user-agent",
        "docxology-link-check/1.0 (+https://danielarifriedman.com/)",
        "--write-out",
        "%{http_code}\t%{url_effective}",
    ]
    if method == "HEAD":
        args.append("--head")
    args.append(url)
    proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout + 3, check=False)
    status_text, _, final_url = proc.stdout.partition("\t")
    status = int(status_text) if status_text.isdigit() else 0
    return {
        "url": url,
        "ok": 200 <= status < 400,
        "status": status,
        "method": method,
        "final_url": final_url.strip() or url,
        "error": proc.stderr.strip() if proc.returncode else "",
    }


def request_url(url: str, timeout: int) -> dict:
    started = time.time()
    last: dict | None = None
    for method in ("HEAD", "GET"):
        try:
            result = curl_probe(url, method, timeout)
        except Exception as exc:
            result = {
                "url": url,
                "ok": False,
                "status": 0,
                "method": method,
                "final_url": url,
                "error": f"{type(exc).__name__}: {exc}",
            }
        result["elapsed_ms"] = int((time.time() - started) * 1000)
        last = result
        if result["ok"]:
            return result
        if method == "HEAD" and (result["status"] == 0 or result["status"] >= 400):
            continue
        return result
    if last is None:
        raise AssertionError("unreachable")
    return last


def category(row: dict) -> str:
    host = urlparse(row["url"]).netloc.lower()
    status = int(row.get("status") or 0)
    if row.get("ok"):
        return "ok"
    if status == 404:
        return "needs-replacement"
    if status in {401, 402, 403, 429, 999} or host in {"linkedin.com", "www.linkedin.com", "www.researchgate.net"}:
        return "bot-protected-or-rate-limited"
    if status in {500, 502, 503, 504}:
        return "upstream-transient"
    if status == 0 and "timed out" in row.get("error", "").lower():
        return "timeout"
    if status == 0:
        return "connection-failure"
    return "review"


def build_report(timeout: int, workers: int, limit: int | None) -> dict:
    sources = collect_urls()
    urls = sorted(sources)
    if limit:
        urls = urls[:limit]
    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(request_url, url, timeout): url for url in urls}
        for future in as_completed(futures):
            result = future.result()
            result["sources"] = sources[result["url"]]
            result["category"] = category(result)
            results.append(result)
    results.sort(key=lambda row: row["url"])
    return {
        "generated_at": "2026-05-13",
        "scope": SCAN_FILES,
        "note": "Network freshness report. HTTP 403/429 may indicate bot protection or rate limiting, not necessarily broken content.",
        "total_unique_urls": len(sources),
        "checked_urls": len(results),
        "ok": sum(1 for row in results if row["ok"]),
        "warnings": sum(1 for row in results if not row["ok"]),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate the cached report exists and is parseable")
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--limit", type=int, default=0, help="Optional maximum URLs to check")
    args = parser.parse_args()
    if args.check:
        if not OUT.exists():
            raise SystemExit("Missing external link report")
        payload = json.loads(OUT.read_text(encoding="utf-8"))
        if not payload.get("results"):
            raise SystemExit("External link report has no results")
        print(f"checked external link report ({payload['checked_urls']} URLs)")
        return
    payload = build_report(args.timeout, args.workers, args.limit or None)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote external link report: {payload['ok']}/{payload['checked_urls']} ok")


if __name__ == "__main__":
    main()
