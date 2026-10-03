#!/usr/bin/env python3
"""Retain bounded, SHA-bound technical acceptance after a Pages deployment.

This is technical deployment evidence, not the human-reviewed release
attestation. It checks the exact hosted manifest, every work page, critical
shared assets, every archived paper PDF's HEAD contract, and three PDF hashes.
The receipt is intended for an Actions artifact, never a source-tree rewrite.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
import time
from urllib.parse import quote, urlsplit

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401
from docxology_tools.release_controls import source_payload_commit  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
ORIGIN = "https://danielarifriedman.com/"
MANIFEST_PATH = "data/pages-artifact-manifest.json"
CRITICAL_PATHS = {
    "index.html", "search.html", "publications.html", "software.html", "art.html", "videos.html",
    "style.css", "css/home.css", "sw.js", "js/search-utils.js", "js/search-page.js",
    "js/interactive.js", "js/index-page.js", "js/nav-toggle.js", "js/cite-export.js", "search-index-core.json",
    "search-index-content-work.json", "search-index-content-video.json", "search-index-bootstrap.json",
    "data/work-identifiers.json",
    "js/publications.js", "js/art-gallery.js", "js/videos-page.js",
    "data/artworks-index.json", "data/videos-index.json",
    "assets/curio-cards/24-complexity.jpg",
    "assets/curio-cards/25-passion.jpg",
    "assets/curio-cards/26-education.jpg",
}
MAX_BODY_BYTES = 64 * 1024 * 1024


def safe_path(value: str) -> str:
    """Require an ordinary repository-relative URL path."""
    path = PurePosixPath(value)
    if (not value or path.is_absolute() or "\\" in value
            or any(part in {"", ".", ".."} for part in value.split("/"))
            or urlsplit(value).scheme or "?" in value or "#" in value):
        raise ValueError(f"unsafe artifact path: {value}")
    return path.as_posix()


def public_url(path: str, *, origin: str = ORIGIN) -> str:
    return origin + quote(safe_path(path), safe="/")


def fetch(path: str, *, method: str = "GET", timeout: float = 20,
          origin: str = ORIGIN, limit: int = MAX_BODY_BYTES) -> dict:
    """Fetch with a process wall deadline and byte ceiling; never follow redirects.

    curl is part of the hosted runner and macOS runtime. Its total deadline
    includes a slow-drip response; a socket inactivity timeout alone does not.
    """
    result = {"path": path, "method": method, "ok": False, "attempted": True}
    try:
        url = public_url(path, origin=origin)
        # A fresh key prevents a prior deployment's CDN cache entry from
        # repeatedly defeating propagation retries. No account data is sent.
        url += "?__acceptance=" + str(time.monotonic_ns())
        with tempfile.TemporaryDirectory(prefix="docxology-acceptance-") as directory:
            body_path, header_path = Path(directory) / "body", Path(directory) / "headers"
            command = ["curl", "--silent", "--show-error", "--proto", "=http,https",
                       "--max-time", str(timeout), "--connect-timeout", str(timeout),
                       "--max-filesize", str(limit), "--user-agent", "docxology-deployment-acceptance/1.0",
                       "--header", "Cache-Control: no-cache", "--dump-header", str(header_path),
                       "--output", str(body_path), "--write-out", "%{http_code}", url]
            if method == "HEAD":
                command.insert(1, "--head")
            process = subprocess.run(command, capture_output=True, text=True, timeout=timeout + 2, check=False)
            status = int(process.stdout) if process.stdout.strip().isdigit() else None
            result["status"] = status
            if process.returncode:
                raise OSError(process.stderr.strip() or f"curl exited {process.returncode}")
            # Ignore interim headers (e.g. HTTP proxy connection responses).
            headers = {}
            for line in header_path.read_text(encoding="utf-8").splitlines():
                if line.startswith("HTTP/"):
                    headers = {}
                elif ":" in line:
                    name, value = line.split(":", 1)
                    headers[name.lower()] = value.strip()
            with body_path.open("rb") as handle:
                body = handle.read(limit + 1) if method == "GET" else b""
            if len(body) > limit:
                raise ValueError("response exceeded body ceiling")
            result.update(content_type=headers.get("content-type", "").split(";", 1)[0].lower(),
                          content_length=headers.get("content-length"),
                          sha256=hashlib.sha256(body).hexdigest() if method == "GET" else None,
                          bytes=len(body) if method == "GET" else None,
                          ok=status == 200)
    except (subprocess.TimeoutExpired, TimeoutError, OSError, ValueError) as exc:
        result["error"] = str(exc)
    return result


def verify_file(item: dict, *, head: bool = False, origin: str = ORIGIN,
                timeout: float = 20) -> dict:
    result = fetch(item["path"], method="HEAD" if head else "GET", origin=origin, timeout=timeout)
    if head:
        result["length_matches"] = result.get("content_length") == str(item["bytes"])
        result["type_matches"] = result.get("content_type") == "application/pdf"
        result["ok"] = result["ok"] and result["length_matches"] and result["type_matches"]
    else:
        result["expected_sha256"] = item["sha256"]
        result["hash_matches"] = result.get("sha256") == item["sha256"]
        result["ok"] = result["ok"] and result["hash_matches"]
    return result


def acceptance_plan(manifest: dict) -> tuple[list[dict], list[dict], list[dict]]:
    """Build explicit scopes and fail if a required family disappears."""
    files = manifest["included_files"]
    paths = [safe_path(item["path"]) for item in files]
    if len(paths) != len(set(paths)):
        raise ValueError("duplicate artifact paths")
    by_path = {item["path"]: item for item in files}
    missing = CRITICAL_PATHS - by_path.keys()
    if missing:
        raise ValueError("missing critical assets: " + ", ".join(sorted(missing)))
    works = [item for item in files if item["path"].startswith("works/")
             and item["path"].endswith(".html") and item["path"] != "works/index.html"]
    pdfs = [item for item in files if item["path"].startswith("papers/")
            and item["path"].lower().endswith(".pdf")]
    if not works or not pdfs:
        raise ValueError("empty work-page or paper-PDF acceptance scope")
    html = sorted(works + [by_path[path] for path in sorted(CRITICAL_PATHS)], key=lambda item: item["path"])
    # Deterministic samples spread across the archive, independent of filenames.
    ordered_pdfs = sorted(pdfs, key=lambda item: item["path"])
    samples = [ordered_pdfs[index] for index in sorted({0, len(pdfs) // 2, len(pdfs) - 1})]
    return html, ordered_pdfs, samples


def require_committed_manifest(repo_root: Path, commit: str) -> None:
    """Reject working-tree substitutions before binding live hashes to a SHA."""
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("expected commit must be a full lowercase Git SHA")
    committed = subprocess.check_output(["git", "show", f"{commit}:{MANIFEST_PATH}"], cwd=repo_root)
    if (repo_root / MANIFEST_PATH).read_bytes() != committed:
        raise ValueError("Pages manifest bytes differ from the expected committed candidate")


def check_deployment(manifest_path: Path, *, commit: str, attempts: int = 6,
                     interval: float = 15, timeout: float = 20,
                     origin: str = ORIGIN, workers: int = 6,
                     max_duration: float = 720) -> dict:
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("expected commit must be a full lowercase Git SHA")
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw)
    expected_manifest = {"path": MANIFEST_PATH, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    html, pdfs, samples = acceptance_plan(manifest)
    if max_duration <= 0:
        raise ValueError("total deployment deadline must be positive")
    started = time.monotonic()
    deadline = started + max_duration

    def bounded_check(item: dict, *, head: bool = False) -> dict:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return {"path": item["path"], "method": "HEAD" if head else "GET",
                    "ok": False, "attempted": False,
                    "error": "Total deployment acceptance deadline exhausted"}
        return verify_file(item, head=head, origin=origin, timeout=min(timeout, remaining))

    results = []
    requests_attempted = 0
    for attempt in range(1, attempts + 1):
        hosted = bounded_check(expected_manifest)
        if hosted["ok"]:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                html_results = list(pool.map(bounded_check, html))
                pdf_results = list(pool.map(lambda item: bounded_check(item, head=True), pdfs))
                sample_results = list(pool.map(bounded_check, samples))
            results = [hosted, *html_results, *pdf_results, *sample_results]
        else:
            results = [hosted]
        requests_attempted += sum(result.get("attempted", False) for result in results)
        if all(result["ok"] for result in results):
            break
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        if attempt < attempts:
            time.sleep(min(interval, remaining))
            if time.monotonic() >= deadline:
                break
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "evidence_kind": "technical post-deployment artifact acceptance",
        "source_commit": commit,
        "source_payload_commit": manifest["source_commit_at_generation"],
        "base_url": origin,
        "manifest_sha256": expected_manifest["sha256"],
        "scope": {"work_and_critical_asset_hashes": len(html), "paper_pdf_heads": len(pdfs),
                  "sample_pdf_hashes": len(samples), "all_artifact_files": False,
                  "human_visual_review": False, "full_release_attestation": False},
        "attempts": attempt,
        "total_deadline_seconds": max_duration,
        "duration_ms": round((time.monotonic() - started) * 1000),
        "deadline_exhausted": time.monotonic() >= deadline,
        "requests_attempted": requests_attempted,
        "overall_ok": all(result["ok"] for result in results),
        "passing": sum(result["ok"] for result in results),
        "checked": len(results),
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--attempts", type=int, default=6)
    parser.add_argument("--interval", type=float, default=15)
    parser.add_argument("--timeout", type=float, default=20)
    parser.add_argument("--max-duration", type=float, default=720,
                        help="Total acceptance deadline in seconds (default 12 minutes)")
    args = parser.parse_args()
    if not 1 <= args.attempts <= 10 or not 0 <= args.interval <= 60 or not 1 <= args.timeout <= 30:
        parser.error("attempts 1..10, interval 0..60s, timeout 1..30s required")
    if not 1 <= args.max_duration <= 780:
        parser.error("total duration must be 1..780s, below the 15-minute hosted step limit")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()
    if args.expected_commit != head:
        parser.error("expected deployment commit must equal checkout HEAD")
    try:
        require_committed_manifest(REPO_ROOT, head)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.error(str(exc))
    manifest = json.loads((REPO_ROOT / MANIFEST_PATH).read_text(encoding="utf-8"))
    if manifest.get("source_commit_at_generation") != source_payload_commit(REPO_ROOT):
        parser.error("Pages manifest must bind the candidate checkout's current payload commit")
    receipt = check_deployment(REPO_ROOT / MANIFEST_PATH, commit=head,
                               attempts=args.attempts, interval=args.interval, timeout=args.timeout,
                               max_duration=args.max_duration)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(f"Technical deployment acceptance: {receipt['passing']}/{receipt['checked']} passed; commit {head}")
    if not receipt["overall_ok"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
