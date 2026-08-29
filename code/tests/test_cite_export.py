"""Copy-BibTeX acceptance tests: embedded entries, button wiring, CSP compliance."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKS_DIR = REPO_ROOT / "works"

BTN_RE = re.compile(r'<button[^>]*id="cite-bibtex-btn"[^>]*>')
BIB_RE = re.compile(
    r'<script type="application/x-bibtex" id="work-bibtex">(.*?)</script>', re.S
)


def _generated_work_pages() -> list[Path]:
    return sorted(
        p for p in WORKS_DIR.glob("*.html")
        if p.name != "index.html"
        and "<!-- docxology:generated-work-page" in p.read_text(encoding="utf-8")[:400]
    )


def test_every_generated_work_page_has_button_and_bibtex_block():
    pages = _generated_work_pages()
    assert pages, "no generated work pages found"
    missing = []
    for page in pages:
        html = page.read_text(encoding="utf-8")
        if not BTN_RE.search(html) or not BIB_RE.search(html):
            missing.append(page.name)
    assert not missing, f"pages missing Copy-BibTeX affordance: {missing[:5]}"


def test_embedded_bibtex_matches_the_work_citation_key():
    mismatched = []
    for page in _generated_work_pages():
        html = page.read_text(encoding="utf-8")
        bib = BIB_RE.search(html)
        if not bib:
            continue
        entry_key = re.match(r"@(\w+)\{([^,]+),", bib.group(1).strip())
        assert entry_key, f"unparseable BibTeX on {page.name}"
        # The file stem IS the citation key (works/{key}.html).
        if entry_key.group(2) != page.stem:
            mismatched.append((page.name, entry_key.group(2)))
    assert not mismatched, f"embedded BibTeX keyed to the wrong work: {mismatched[:5]}"


def test_embedded_bibtex_entries_are_brace_balanced():
    for page in _generated_work_pages():
        bib = BIB_RE.search(page.read_text(encoding="utf-8"))
        assert bib is not None
        body = bib.group(1)
        assert body.count("{") == body.count("}"), f"unbalanced BibTeX on {page.name}"


def test_cite_export_js_uses_clipboard_with_fallback_and_no_inline_handlers():
    js = (REPO_ROOT / "js" / "cite-export.js").read_text(encoding="utf-8")
    assert "navigator.clipboard" in js
    assert "execCommand" in js
    assert "cite-bibtex-btn" in js
    assert "work-bibtex" in js
    # CSP compliance: no eval / inline-script generation.
    assert "eval(" not in js and "innerHTML" not in js


def test_work_pages_load_cite_export_externally_and_stay_csp_clean():
    inline_handler_re = re.compile(r"\son(click|change|load|submit|mouse\w+)=", re.I)
    violating = []
    for page in _generated_work_pages()[:25]:
        html = page.read_text(encoding="utf-8")
        if "js/cite-export.js" not in html:
            violating.append((page.name, "missing cite-export.js script tag"))
        if inline_handler_re.search(html):
            violating.append((page.name, "inline event handler"))
    assert not violating, f"CSP violations on work pages: {violating[:5]}"
