#!/usr/bin/env python3
"""Capture Playwright screenshots for key site pages.

Requires the optional ``browser-qa`` dependency plus its Chromium binary
(``uv sync --extra browser-qa && uv run playwright install chromium``). The
script starts a local static server, captures desktop and mobile screenshots,
and writes a manifest under reports/visual-qa/.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import socket
import subprocess
import time
import sys
from pathlib import Path
from urllib.request import urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

try:
    from report_paths import dated_report_dir, generated_timestamp, latest_subdir_file, source_commit, source_worktree_state
except ImportError:  # pragma: no cover - package import path
    from .report_paths import dated_report_dir, generated_timestamp, latest_subdir_file, source_commit, source_worktree_state

OUT_DIR = dated_report_dir("visual-qa")
MANIFEST = OUT_DIR / "manifest.json"

PAGES = [
    ("home", "index.html"),
    ("publications", "publications.html"),
    ("works", "works/index.html"),
    ("domains", "domains.html"),
    ("search", "search.html?q=active%20inference"),
    ("repositories", "repositories.html"),
    ("repository-forks", "repositories-forks.html"),
    ("catalog", "catalog.html"),
    ("updates", "updates.html"),
    ("art", "art.html"),
    ("discovery", "discovery.html"),
    ("cite-verify", "cite-verify.html"),
    ("evidence", "evidence.html"),
]

VIEWPORTS = [
    ("desktop", "1440,1100"),
    ("mobile", "390,900"),
]


def sha256_file(path: Path) -> str:
    """Return the digest of a visual-review screenshot."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_server(url: str) -> None:
    for _ in range(60):
        try:
            with urlopen(url, timeout=1) as res:
                if res.status == 200:
                    return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError(f"Server did not become ready: {url}")


def capture(*, reviewed_by: str | None = None) -> dict:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    port = free_port()
    server = subprocess.Popen(
        ["python3", "-m", "http.server", str(port), "--bind", "127.0.0.1"],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        base = f"http://127.0.0.1:{port}"
        wait_for_server(base + "/index.html")
        shots = []
        for page_name, rel in PAGES:
            for viewport_name, size in VIEWPORTS:
                out = OUT_DIR / f"{page_name}-{viewport_name}.png"
                subprocess.run(
                    [
                        "playwright",
                        "screenshot",
                        "--browser=chromium",
                        f"--viewport-size={size}",
                        "--full-page",
                        f"{base}/{rel}",
                        str(out),
                    ],
                    cwd=REPO_ROOT,
                    check=True,
                )
                shots.append(
                    {
                        "page": rel,
                        "viewport": viewport_name,
                        "size": size,
                        "file": str(out.relative_to(REPO_ROOT)),
                        "sha256": sha256_file(out),
                    }
                )
        reviewer = (reviewed_by or "").strip()
        manifest = {
            "generated_at": generated_timestamp(),
            "source_commit": source_commit(),
            **source_worktree_state(),
            "tool": "playwright screenshot",
            "note": "Human review still required; these snapshots guard against obvious layout regressions.",
            "screenshots": shots,
            "review": {
                "status": "reviewed" if reviewer else "pending",
                "reviewed_by": reviewer or None,
                "reviewed_at": generated_timestamp() if reviewer else None,
            },
        }
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return manifest
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


def check() -> None:
    manifest_path = latest_subdir_file("visual-qa", "manifest.json")
    if not manifest_path.exists():
        raise SystemExit("Missing visual QA manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    missing = [shot["file"] for shot in manifest.get("screenshots", []) if not (REPO_ROOT / shot["file"]).exists()]
    if missing:
        raise SystemExit("Missing visual QA screenshots: " + ", ".join(missing[:10]))
    print(f"checked {len(manifest.get('screenshots', []))} visual QA screenshots")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify the existing manifest and screenshot files")
    parser.add_argument(
        "--reviewed-by",
        help="Record the person who visually reviewed this fresh capture; required by the post-deploy release gate.",
    )
    args = parser.parse_args()
    if args.check and args.reviewed_by:
        parser.error("--reviewed-by applies only when capturing a new visual QA report")
    if args.check:
        check()
        return
    manifest = capture(reviewed_by=args.reviewed_by)
    print(f"wrote {len(manifest['screenshots'])} visual QA screenshots")


if __name__ == "__main__":
    main()
