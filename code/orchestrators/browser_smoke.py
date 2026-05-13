#!/usr/bin/env python3
"""Run lightweight browser smoke checks with the cached Playwright CLI."""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import time
from pathlib import Path
from urllib.request import urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = REPO_ROOT / "reports" / "browser-smoke" / "2026-05-13"
MANIFEST = OUT_DIR / "manifest.json"

PAGES = [
    ("home", "index.html", "h1"),
    ("publications", "publications.html", "table"),
    ("works", "works/index.html", ".work-row"),
    ("search", "search.html?q=active%20inference", ".result-card"),
    ("catalog", "catalog.html", ".catalog-card"),
    ("updates", "updates.html", ".update-card"),
    ("art", "art.html", ".art-card"),
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


def run_smoke() -> dict:
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
        checks = []
        for name, rel, selector in PAGES:
            out = OUT_DIR / f"{name}.png"
            cmd = [
                "npx",
                "playwright",
                "screenshot",
                "--browser=chromium",
                "--block-service-workers",
                "--viewport-size=1100,850",
                "--wait-for-selector",
                selector,
                "--timeout=15000",
                f"{base}/{rel}",
                str(out),
            ]
            proc = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, check=False)
            checks.append(
                {
                    "name": name,
                    "page": rel,
                    "selector": selector,
                    "ok": proc.returncode == 0 and out.exists(),
                    "screenshot": str(out.relative_to(REPO_ROOT)) if out.exists() else "",
                    "stdout": proc.stdout.strip()[-500:],
                    "stderr": proc.stderr.strip()[-500:],
                }
            )
        manifest = {
            "generated_at": "2026-05-13",
            "tool": "npx playwright screenshot",
            "note": "Selector-based smoke checks for core local site behavior.",
            "passing": sum(1 for item in checks if item["ok"]),
            "count": len(checks),
            "checks": checks,
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
        raise SystemExit("Missing browser smoke manifest")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures = [item["page"] for item in manifest.get("checks", []) if not item.get("ok")]
    missing = [item["screenshot"] for item in manifest.get("checks", []) if item.get("screenshot") and not (REPO_ROOT / item["screenshot"]).exists()]
    if failures:
        raise SystemExit("Browser smoke failures: " + ", ".join(failures))
    if missing:
        raise SystemExit("Missing browser smoke screenshots: " + ", ".join(missing))
    print(f"checked browser smoke report ({manifest['passing']}/{manifest['count']} passing)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify existing smoke report and screenshots")
    args = parser.parse_args()
    if args.check:
        check()
        return
    manifest = run_smoke()
    print(f"wrote browser smoke report ({manifest['passing']}/{manifest['count']} passing)")


if __name__ == "__main__":
    main()
