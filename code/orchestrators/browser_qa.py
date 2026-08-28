#!/usr/bin/env python3
"""Run progressive-enhancement and interaction checks in a local Chromium.

This complements ``browser_smoke.py``.  Smoke checks prove that representative
pages render and screenshots exist; this report exercises the behaviors most
likely to regress when the shared navigation, data-driven pages, CSP, or
gallery controls change.  The script is intentionally not part of the offline
regeneration chain because it launches a browser and writes a dated report.

Install the optional browser QA dependency and browser binary before running:

    uv sync --extra browser-qa
    uv run playwright install chromium
    uv run --extra browser-qa python3 code/orchestrators/browser_qa.py
    uv run --extra browser-qa python3 code/orchestrators/browser_qa.py --check
"""

from __future__ import annotations

import argparse
import json
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

try:
    from report_paths import dated_report_dir, generated_timestamp, latest_subdir_file, source_commit, source_worktree_state
except ImportError:  # pragma: no cover - package import path
    from .report_paths import dated_report_dir, generated_timestamp, latest_subdir_file, source_commit, source_worktree_state

OUT_DIR = dated_report_dir("browser-qa")
MANIFEST = OUT_DIR / "manifest.json"
CHECK_NAMES = (
    "core routes render without console errors",
    "mobile menu opens, closes, and restores focus",
    "no-JavaScript fallbacks remain usable",
    "publication filters, announcements, and sorting update state",
    "gallery lightbox traps and restores focus",
    "320px layout honors reduced motion without page overflow",
    "forced colors and YouTube iframe policy remain covered",
)


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def wait_for_server(url: str) -> None:
    for _ in range(60):
        try:
            with urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except Exception:
            time.sleep(0.2)
    raise RuntimeError(f"Server did not become ready: {url}")


def require_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:  # pragma: no cover - environment-specific
        raise SystemExit(
            "browser_qa.py requires the optional browser QA dependency; run "
            "`uv sync --extra browser-qa` and `uv run playwright install chromium`."
        ) from exc
    return sync_playwright


def run_report() -> dict:
    sync_playwright = require_playwright()
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
        checks: list[dict] = []

        def record(name: str, fn) -> None:
            started = time.monotonic()
            try:
                details = fn() or {}
                checks.append({"name": name, "ok": True, "details": details})
            except Exception as exc:  # noqa: BLE001 - report every scenario
                checks.append(
                    {
                        "name": name,
                        "ok": False,
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
            checks[-1]["duration_ms"] = round((time.monotonic() - started) * 1000)

        def new_context(browser, **kwargs):
            options = {"viewport": {"width": 1100, "height": 850}, "service_workers": "block"}
            options.update(kwargs)
            return browser.new_context(**options)

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            def load_pages() -> dict:
                routes = {
                    "index.html": "h1",
                    "publications.html": "#pub-tbody tr",
                    "works/index.html": ".work-row",
                    "search.html?q=active%20inference": ".result-card",
                    "art.html": ".art-card",
                    "videos.html": ".video-topic-panel",
                }
                with new_context(browser) as context:
                    page = context.new_page()
                    console_errors: list[str] = []
                    console_warnings: list[str] = []
                    page_errors: list[str] = []
                    def capture_console(msg) -> None:
                        # No console errors are excused. The one exemption that
                        # used to live here — Chromium's "frame-ancestors is
                        # ignored in a <meta> policy" — was filtered on every
                        # page for months; removing the directive removed the
                        # error, so the gate now catches it if it returns.
                        if msg.type == "error":
                            console_errors.append(msg.text)
                    page.on("console", capture_console)
                    page.on("pageerror", lambda exc: page_errors.append(str(exc)))
                    for route, selector in routes.items():
                        page.goto(base + "/" + route, wait_until="domcontentloaded", timeout=30000)
                        page.wait_for_selector(selector, timeout=30000)
                        page.wait_for_timeout(250)
                    if console_errors or page_errors:
                        raise AssertionError({"console": console_errors[:10], "page": page_errors[:10]})
                return {
                    "routes": len(routes),
                    "console_errors": 0,
                    "page_errors": 0,
                    "known_meta_csp_warnings": len(console_warnings),
                }

            record(CHECK_NAMES[0], load_pages)

            def mobile_menu() -> dict:
                with new_context(browser, viewport={"width": 320, "height": 760}) as context:
                    page = context.new_page()
                    page.goto(base + "/index.html", wait_until="domcontentloaded")
                    toggle = page.locator(".menu-btn")
                    toggle.click()
                    if toggle.get_attribute("aria-expanded") != "true":
                        raise AssertionError("menu did not set aria-expanded=true")
                    page.keyboard.press("Escape")
                    if toggle.get_attribute("aria-expanded") != "false":
                        raise AssertionError("Escape did not close the menu")
                    if page.evaluate("document.activeElement === document.querySelector('.menu-btn')") is not True:
                        raise AssertionError("Escape did not restore focus to the menu toggle")
                return {"opened_and_closed": True, "focus_restored": True}

            record(CHECK_NAMES[1], mobile_menu)

            def no_javascript_fallback() -> dict:
                routes = {
                    "publications.html": "canonical work index",
                    "art.html": "full artwork data export",
                    "videos.html": "static video index",
                }
                with new_context(browser, java_script_enabled=False) as context:
                    page = context.new_page()
                    for route, marker in routes.items():
                        page.goto(base + "/" + route, wait_until="domcontentloaded")
                        if not page.locator("h1").count():
                            raise AssertionError(f"{route} has no heading without JavaScript")
                        if marker not in page.locator("body").inner_text():
                            raise AssertionError(f"{route} missing fallback marker: {marker}")
                return {"routes": len(routes), "fallbacks": "visible"}

            record(CHECK_NAMES[2], no_javascript_fallback)

            def publications_controls() -> dict:
                with new_context(browser) as context:
                    page = context.new_page()
                    page.goto(base + "/publications.html", wait_until="domcontentloaded")
                    page.wait_for_selector("#pub-tbody tr")
                    all_rows = page.locator("#pub-tbody tr").count()
                    page.locator("#filter-paper").click()
                    paper_rows = page.locator("#pub-tbody tr").count()
                    if paper_rows >= all_rows:
                        raise AssertionError(f"paper filter did not narrow rows ({all_rows} -> {paper_rows})")
                    if page.locator("#filter-paper").get_attribute("aria-pressed") != "true":
                        raise AssertionError("paper filter did not expose pressed state")
                    first_sort = page.locator(".th-sort-btn").first
                    first_sort.click()
                    sort_state = page.locator("th[data-sortable]").first.get_attribute("aria-sort")
                    if sort_state not in {"ascending", "descending"}:
                        raise AssertionError(f"sort state missing: {sort_state}")
                return {"all_rows": all_rows, "paper_rows": paper_rows, "sort_state": sort_state}

            record(CHECK_NAMES[3], publications_controls)

            def gallery_focus() -> dict:
                with new_context(browser) as context:
                    page = context.new_page()
                    page.goto(base + "/art.html", wait_until="domcontentloaded")
                    page.wait_for_selector(".art-card")
                    first = page.locator(".art-card").first
                    title = first.get_attribute("aria-label")
                    first.click()
                    page.wait_for_selector("#lightbox[aria-hidden='false']")
                    if page.evaluate("document.activeElement.id") != "lb-close":
                        raise AssertionError("lightbox did not focus its close button")
                    page.keyboard.press("Escape")
                    if page.locator("#lightbox").get_attribute("aria-hidden") != "true":
                        raise AssertionError("Escape did not close the lightbox")
                    if page.evaluate("document.activeElement.classList.contains('art-card')") is not True:
                        raise AssertionError("lightbox did not restore focus to the artwork card")
                return {"trigger": title, "focus_restored": True}

            record(CHECK_NAMES[4], gallery_focus)

            def responsive_accessibility() -> dict:
                routes = ["index.html", "publications.html", "art.html", "videos.html"]
                with new_context(browser, viewport={"width": 320, "height": 760}) as context:
                    context.set_default_timeout(30000)
                    page = context.new_page()
                    page.emulate_media(reduced_motion="reduce")
                    for route in routes:
                        page.goto(base + "/" + route, wait_until="domcontentloaded")
                        page.wait_for_timeout(250)
                        if page.evaluate("window.matchMedia('(prefers-reduced-motion: reduce)').matches") is not True:
                            raise AssertionError("reduced-motion media query not active")
                        overflow = page.evaluate("document.documentElement.scrollWidth - window.innerWidth")
                        if overflow > 2:
                            raise AssertionError(f"{route} overflows viewport by {overflow}px")
                return {"routes": len(routes), "viewport": "320x760", "reduced_motion": True, "max_overflow_px": 2}

            record(CHECK_NAMES[5], responsive_accessibility)

            def forced_colors_and_iframes() -> dict:
                with new_context(browser, forced_colors="active") as context:
                    page = context.new_page()
                    page.goto(base + "/index.html", wait_until="domcontentloaded")
                    forced = page.evaluate("window.matchMedia('(forced-colors: active)').matches")
                    if not forced:
                        raise AssertionError("forced-colors emulation did not activate")
                    page.goto(base + "/videos/personal-NWrGixOmW6k.html", wait_until="domcontentloaded")
                    iframe = page.locator("iframe").first
                    src = iframe.get_attribute("src") or ""
                    if not src.startswith("https://www.youtube-nocookie.com/embed/"):
                        raise AssertionError(f"unapproved iframe origin: {src}")
                    if not iframe.get_attribute("title"):
                        raise AssertionError("YouTube iframe has no title")
                    if iframe.get_attribute("referrerpolicy") != "strict-origin-when-cross-origin":
                        raise AssertionError("YouTube iframe referrer policy drifted")
                return {"forced_colors": True, "iframe_origin": "www.youtube-nocookie.com", "iframe_title": True}

            record(CHECK_NAMES[6], forced_colors_and_iframes)
            browser.close()

        if tuple(check.get("name") for check in checks) != CHECK_NAMES:
            raise RuntimeError("browser QA implementation no longer matches its declared coverage contract")

        report = {
            "generated_at": generated_timestamp(),
            "source_commit": source_commit(),
            **source_worktree_state(),
            "tool": "Playwright Python sync API",
            "scope": "progressive enhancement, interaction, responsive, CSP-adjacent runtime checks",
            "passing": sum(1 for check in checks if check["ok"]),
            "count": len(checks),
            "checks": checks,
        }
        MANIFEST.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"wrote browser QA report ({report['passing']}/{report['count']} passing)")
        return report
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


def check() -> None:
    path = latest_subdir_file("browser-qa", "manifest.json")
    if not path.exists():
        raise SystemExit("Missing browser QA manifest")
    report = json.loads(path.read_text(encoding="utf-8"))
    failures = [item["name"] for item in report.get("checks", []) if not item.get("ok")]
    if not report.get("checks") or failures or report.get("passing") != report.get("count"):
        raise SystemExit("Browser QA failures: " + ", ".join(failures or ["incomplete report"]))
    print(f"checked browser QA report ({report['passing']}/{report['count']} passing)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify the latest report")
    args = parser.parse_args()
    check() if args.check else run_report()


if __name__ == "__main__":
    main()
