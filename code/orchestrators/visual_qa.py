#!/usr/bin/env python3
"""Capture Playwright screenshots for key site pages.

Requires `npx playwright` to be available. The script starts a local static
server, captures desktop and mobile screenshots, and writes a manifest under
reports/visual-qa/.
"""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import time
from pathlib import Path
from urllib.request import urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "reports" / "visual-qa" / "2026-05-13"
MANIFEST = OUT_DIR / "manifest.json"

PAGES = [
    ("home", "index.html"),
    ("publications", "publications.html"),
    ("works", "works/index.html"),
    ("domains", "domains.html"),
    ("search", "search.html?q=active%20inference"),
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


def capture() -> dict:
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
                        "npx",
                        "--yes",
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
                shots.append({"page": rel, "viewport": viewport_name, "size": size, "file": str(out.relative_to(REPO_ROOT))})
        manifest = {
            "generated_at": "2026-05-13",
            "tool": "npx playwright screenshot",
            "note": "Human review still required; these snapshots guard against obvious layout regressions.",
            "screenshots": shots,
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
    if not MANIFEST.exists():
        raise SystemExit("Missing visual QA manifest")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    missing = [shot["file"] for shot in manifest.get("screenshots", []) if not (REPO_ROOT / shot["file"]).exists()]
    if missing:
        raise SystemExit("Missing visual QA screenshots: " + ", ".join(missing[:10]))
    print(f"checked {len(manifest.get('screenshots', []))} visual QA screenshots")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify the existing manifest and screenshot files")
    args = parser.parse_args()
    if args.check:
        check()
        return
    manifest = capture()
    print(f"wrote {len(manifest['screenshots'])} visual QA screenshots")


if __name__ == "__main__":
    main()
