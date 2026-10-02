"""Real-browser acceptance for paper access, mobile layout and citation copying."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from rendered_site_fixture import AXE_JS, REPO_ROOT, serve_site, skip_without_playwright, stop_server  # noqa: E402

WORK_PAGE = "works/Friedman2026FourfoldVisionWilliamBlake196.html"
PAPER_PAGE = "papers/2026_FourfoldVision/index.html"
PDF = "papers/2026_FourfoldVision/blake_fourfold_synergetics_combined.pdf"


def test_rendered_work_download_copy_and_accessible_mobile_layout(tmp_path):
    skip_without_playwright()
    from playwright.sync_api import sync_playwright

    site = tmp_path / "site"
    site.mkdir()
    for name in ("style.css", "favicon.ico", WORK_PAGE, PAPER_PAGE, PDF):
        target = site / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / name, target)
    shutil.copytree(REPO_ROOT / "js", site / "js")
    shutil.copy2(AXE_JS, site / "js" / "axe.min.js")
    base_url, server = serve_site(site)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(permissions=["clipboard-read", "clipboard-write"], viewport={"width": 1280, "height": 900})
            # Keep browser acceptance independent of CDN fonts and GitHub images.
            context.route("**/*", lambda route: route.continue_() if route.request.url.startswith(base_url) else route.abort())
            page = context.new_page()
            page.goto(base_url + "/" + WORK_PAGE, wait_until="load")
            assert "an atlas can preserve all 4" in page.locator("main").inner_text()
            assert page.get_by_role("link", name="Paper folder on GitHub", exact=True).get_attribute("href") == "https://github.com/docxology/docxology/tree/main/papers/2026_FourfoldVision"
            with page.expect_download() as download_info:
                page.get_by_role("link", name="Download PDF", exact=True).click()
            download = download_info.value
            assert download.suggested_filename == Path(PDF).name
            assert Path(download.path()).read_bytes() == (REPO_ROOT / PDF).read_bytes()
            expected_bibtex = page.locator("#work-bibtex").evaluate("node => JSON.parse(node.textContent)")
            page.get_by_role("button", name="Copy BibTeX entry to clipboard").click()
            page.wait_for_function("navigator.clipboard.readText().then(text => text.startsWith('@article{'))")
            assert page.evaluate("navigator.clipboard.readText()") == expected_bibtex
            for path in (WORK_PAGE, PAPER_PAGE):
                for width, font_size in ((320, "100%"), (768, "100%"), (1280, "200%")):
                    page.set_viewport_size({"width": width, "height": 900})
                    page.goto(base_url + "/" + path, wait_until="load")
                    page.evaluate("size => document.documentElement.style.fontSize = size", font_size)
                    overflow = page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth")
                    assert overflow <= 1, (path, width, font_size, overflow)
                page.add_script_tag(url=base_url + "/js/axe.min.js")
                violations = page.evaluate("async () => (await axe.run()).violations.filter(v => ['serious','critical'].includes(v.impact))")
                assert not violations, [(v["id"], v["description"]) for v in violations]
            context.close()
            browser.close()
    finally:
        stop_server(server)
