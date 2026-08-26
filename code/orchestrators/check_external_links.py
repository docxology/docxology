#!/usr/bin/env python3
"""Check a scoped set of external links and write a cached report.

The default scope is every root-level public HTML page plus site-critical hubs,
not every paper folder or art metadata file. That keeps the report useful
without hammering external services with thousands of archive links.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
import sys
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

try:
    from report_paths import dated_report_path, generated_timestamp, latest_report, source_commit, source_worktree_state
except ImportError:  # pragma: no cover - package import path
    from .report_paths import dated_report_path, generated_timestamp, latest_report, source_commit, source_worktree_state

OUT = dated_report_path("external_links", "json")

EXTRA_SCAN_FILES = [
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
    return url.rstrip(".,;`\\\t\n\r")


def scan_files(repo_root: Path = REPO_ROOT) -> list[str]:
    """Return the bounded scan contract, including every root HTML route."""
    root_html = [path.name for path in repo_root.glob("*.html") if path.is_file()]
    return sorted(set(EXTRA_SCAN_FILES) | set(root_html))


def is_csp_source_expression(text: str, position: int) -> bool:
    """Return whether a URL token belongs to a CSP meta-policy expression.

    CSP source expressions are not navigable links. In particular,
    ``https://www.youtube-nocookie.com`` is a valid ``frame-src`` origin while
    the host root intentionally returns 404; actual video embeds retain their
    explicit ``/embed/<id>`` paths and are covered by browser QA.
    """
    tag_start = text.rfind("<meta", 0, position)
    if tag_start < 0:
        return False
    tag_end = text.find(">", tag_start)
    if tag_end < position:
        return False
    return "content-security-policy" in text[tag_start : tag_end + 1].lower()


def collect_urls_from_text(text: str) -> list[str]:
    """Collect scoped, navigable external URLs from one source document."""
    urls: list[str] = []
    for match in URL_RE.finditer(text):
        if is_csp_source_expression(text, match.start()):
            continue
        url = clean_url(match.group(0))
        if any(url.startswith(prefix) for prefix in IGNORE_PREFIXES):
            continue
        host = urlparse(url).netloc.lower()
        if host in IGNORE_HOSTS:
            continue
        urls.append(url)
    return urls


def collect_urls() -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for rel in scan_files():
        path = REPO_ROOT / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for url in collect_urls_from_text(text):
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


def build_report(
    timeout: int,
    workers: int,
    limit: int | None,
    *,
    url_sources: dict[str, list[str]] | None = None,
    request: Callable[[str, int], dict] | None = None,
) -> dict:
    """Build a link report from the normal scan or explicit dependencies.

    ``url_sources`` and ``request`` preserve the CLI defaults while allowing
    isolated callers to use local fixture inputs without replacing globals.
    """
    sources = collect_urls() if url_sources is None else url_sources
    request_url_fn = request_url if request is None else request
    urls = sorted(sources)
    if limit:
        urls = urls[:limit]
    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(request_url_fn, url, timeout): url for url in urls}
        for future in as_completed(futures):
            result = future.result()
            result["sources"] = sources[result["url"]]
            result["category"] = category(result)
            results.append(result)
    results.sort(key=lambda row: row["url"])
    return {
        "generated_at": generated_timestamp(),
        "source_commit": source_commit(),
        **source_worktree_state(),
        "scope": scan_files(),
        "note": "Network freshness report. HTTP 403/429 may indicate bot protection or rate limiting, not necessarily broken content.",
        "total_unique_urls": len(sources),
        "checked_urls": len(results),
        "unchecked_urls": len(sources) - len(results),
        "ok": sum(1 for row in results if row["ok"]),
        "warnings": sum(1 for row in results if not row["ok"]),
        "results": results,
    }


def cached_report_errors(
    payload: dict,
    *,
    url_sources: dict[str, list[str]] | None = None,
    scope: list[str] | None = None,
) -> list[str]:
    """Return deterministic drift errors for an existing full link report.

    A cached report is useful only when it covers the current bounded source
    contract. Checking merely for a nonempty result set can leave a newly added
    redirect, root page, or changed source link outside the release gate.
    """
    expected_sources = collect_urls() if url_sources is None else url_sources
    expected_scope = scan_files() if scope is None else scope
    errors: list[str] = []
    if payload.get("scope") != expected_scope:
        errors.append("scope does not match the current external-link contract")

    results = payload.get("results")
    if not isinstance(results, list) or not results:
        return errors + ["has no results"]
    by_url: dict[str, dict] = {}
    duplicate_urls: list[str] = []
    malformed_rows = 0
    for row in results:
        if not isinstance(row, dict) or not isinstance(row.get("url"), str):
            malformed_rows += 1
            continue
        url = row["url"]
        if url in by_url:
            duplicate_urls.append(url)
            continue
        by_url[url] = row
    if malformed_rows:
        errors.append("has malformed result rows")
    if duplicate_urls:
        errors.append("has duplicate URL results: " + ", ".join(sorted(duplicate_urls)[:5]))

    expected_urls = set(expected_sources)
    observed_urls = set(by_url)
    missing = sorted(expected_urls - observed_urls)
    unexpected = sorted(observed_urls - expected_urls)
    if missing or unexpected:
        details: list[str] = []
        if missing:
            details.append("missing " + ", ".join(missing[:3]))
        if unexpected:
            details.append("unexpected " + ", ".join(unexpected[:3]))
        errors.append("URL coverage does not match the current contract (" + "; ".join(details) + ")")

    for url in sorted(expected_urls & observed_urls):
        if by_url[url].get("sources") != expected_sources[url]:
            errors.append(f"source mapping does not match the current contract for {url}")
            break

    expected_count = len(expected_sources)
    if payload.get("total_unique_urls") != expected_count:
        errors.append("total_unique_urls does not match current URL coverage")
    if payload.get("checked_urls") != len(results):
        errors.append("checked_urls does not match result rows")
    if payload.get("unchecked_urls") != 0:
        errors.append("report has unchecked URLs")
    if len(results) != expected_count:
        errors.append("result row count does not match current URL coverage")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate the cached report exists and is parseable")
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--limit", type=int, default=0, help="Optional maximum URLs to check")
    args = parser.parse_args()
    if args.check:
        out = latest_report("external_links_[0-9]*.json")
        if not out.exists():
            raise SystemExit("Missing external link report")
        payload = json.loads(out.read_text(encoding="utf-8"))
        errors = cached_report_errors(payload)
        if errors:
            raise SystemExit("External link report drift:\n" + "\n".join(f"  - {error}" for error in errors))
        print(f"checked external link report ({payload['checked_urls']} URLs)")
        return
    payload = build_report(args.timeout, args.workers, args.limit or None)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote external link report: {payload['ok']}/{payload['checked_urls']} ok")


if __name__ == "__main__":
    main()
