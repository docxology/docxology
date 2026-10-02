"""Copy-BibTeX acceptance tests: embedded entries, button wiring, CSP compliance."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

import docxology_tools  # noqa: E402, F401
import build_work_pages  # noqa: E402
from docxology_tools.generated_outputs import UnsafeGeneratedOutputPathError  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKS_DIR = REPO_ROOT / "works"

BTN_RE = re.compile(r'<button[^>]*id="cite-bibtex-btn"[^>]*>')
BIB_RE = re.compile(
    r'<script type="application/json" id="work-bibtex">(.*?)</script>', re.S
)


def _entry(payload: str) -> str:
    entry = json.loads(payload)
    assert isinstance(entry, str), "embedded BibTeX must be a JSON string"
    return entry


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
        entry_key = re.match(r"@(\w+)\{([^,]+),", _entry(bib.group(1)))
        assert entry_key, f"unparseable BibTeX on {page.name}"
        # The file stem IS the citation key (works/{key}.html).
        if entry_key.group(2) != page.stem:
            mismatched.append((page.name, entry_key.group(2)))
    assert not mismatched, f"embedded BibTeX keyed to the wrong work: {mismatched[:5]}"


def test_embedded_bibtex_entries_are_brace_balanced():
    for page in _generated_work_pages():
        bib = BIB_RE.search(page.read_text(encoding="utf-8"))
        assert bib is not None
        body = _entry(bib.group(1))
        assert body.count("{") == body.count("}"), f"unbalanced BibTeX on {page.name}"


def test_embedded_entries_match_the_canonical_bibliography_exactly():
    for page in _generated_work_pages():
        bib = BIB_RE.search(page.read_text(encoding="utf-8"))
        assert bib is not None
        assert _entry(bib.group(1)) == build_work_pages.work_bibtex(page.stem)


@pytest.fixture
def citation_fragment(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[str, str]:
    entry = (
        '@article{Example001,\n'
        '  title = {Art & "Science": β < λ </script><img src=x onerror=alert(1)>},\n'
        '  note = {Literal &amp; entity and \\LaTeX notation}\n'
        '}'
    )
    (tmp_path / "bibliography.bib").write_text(entry + "\n", encoding="utf-8")
    monkeypatch.setattr(build_work_pages, "REPO_ROOT", tmp_path)
    fragment = build_work_pages.bibtex_button_html({"citation_key": "Example001"})
    return entry, fragment


def test_citation_payload_round_trip_preserves_text_and_cannot_close_its_script(citation_fragment):
    entry, fragment = citation_fragment
    match = BIB_RE.search(fragment)
    assert match is not None
    assert _entry(match.group(1)) == entry
    assert "<" not in match.group(1)
    assert fragment.count("</script>") == 1
    assert "<img" not in fragment


def test_citation_read_rejects_a_symlinked_bibliography(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    private = tmp_path / "unrelated.bib"
    private.write_text("sentinel unrelated source", encoding="utf-8")
    (repo / "bibliography.bib").symlink_to(private)
    monkeypatch.setattr(build_work_pages, "REPO_ROOT", repo)

    with pytest.raises(UnsafeGeneratedOutputPathError):
        build_work_pages.work_bibtex("Example001")
    assert private.read_text(encoding="utf-8") == "sentinel unrelated source"


def test_citation_batch_load_reads_once_and_does_not_cache_between_batches(tmp_path, monkeypatch):
    first = "@article{First001,\n  title = {First}\n}"
    second = "@article{Second002,\n  title = {Second}\n}"
    source = tmp_path / "bibliography.bib"
    source.write_text(first + "\n\n" + second + "\n", encoding="utf-8")
    monkeypatch.setattr(build_work_pages, "REPO_ROOT", tmp_path)
    read = build_work_pages.read_generated_output_text
    calls = []

    def counted_read(*args, **kwargs):
        calls.append(args)
        return read(*args, **kwargs)

    monkeypatch.setattr(build_work_pages, "read_generated_output_text", counted_read)
    assert build_work_pages.load_bibtex_entries() == {"First001": first, "Second002": second}
    assert len(calls) == 1
    source.write_text(second + "\n", encoding="utf-8")
    assert build_work_pages.load_bibtex_entries() == {"Second002": second}


def test_citation_batch_rejects_duplicate_keys(tmp_path, monkeypatch):
    (tmp_path / "bibliography.bib").write_text(
        "@article{Example001,\n  title = {First}\n}\n\n@article{Example001,\n  title = {Second}\n}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(build_work_pages, "REPO_ROOT", tmp_path)
    with pytest.raises(ValueError, match="Duplicate BibTeX citation key: Example001"):
        build_work_pages.load_bibtex_entries()


@pytest.mark.parametrize("entry", ["", "@article{Example001,\n  title = {Given entry}\n}"])
def test_citation_button_uses_the_batch_entry_without_another_read(monkeypatch, entry):
    def unexpected_read(key):
        pytest.fail("the batch entry must avoid an individual bibliography read")

    monkeypatch.setattr(build_work_pages, "work_bibtex", unexpected_read)
    fragment = build_work_pages.bibtex_button_html({"citation_key": "Example001", "_bibtex": entry})
    if not entry:
        assert fragment == ""
    else:
        match = BIB_RE.search(fragment)
        assert match is not None
        assert _entry(match.group(1)) == entry


def _copy_with_javascript(payload: str, *, secure_clipboard: bool) -> dict:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node interpreter not available")
    # Execute the shipped click handler. The raw textContent below models the
    # inert script element; neither the DOM nor this harness decodes entities.
    program = r"""
const fs = require('fs');
const vm = require('vm');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
const copied = [];
let click;
let scratch;
const button = {
    textContent: 'Copy BibTeX', dataset: {}, disabled: false,
    addEventListener: (event, callback) => { if (event === 'click') click = callback; },
};
const document = {
    readyState: 'complete',
    getElementById: (id) => id === 'cite-bibtex-btn' ? button : {textContent: input.payload},
    createElement: () => scratch = {setAttribute() {}, style: {}, select() {}},
    body: {appendChild() {}, removeChild() {}},
    execCommand: () => { copied.push(scratch.value); return true; },
};
const navigator = input.secure_clipboard ? {
    clipboard: {writeText: (text) => { copied.push(text); return Promise.resolve(); }},
} : {};
vm.runInNewContext(input.source, {
    document, navigator, window: {isSecureContext: input.secure_clipboard}, setTimeout() {},
});
click();
setImmediate(() => process.stdout.write(JSON.stringify({copied, label: button.textContent})));
"""
    result = subprocess.run(
        [node, "-e", program],
        input=json.dumps({
            "payload": payload,
            "source": (REPO_ROOT / "js" / "cite-export.js").read_text(encoding="utf-8"),
            "secure_clipboard": secure_clipboard,
        }),
        text=True, capture_output=True, check=True, timeout=10,
    )
    return json.loads(result.stdout)


@pytest.mark.parametrize("secure_clipboard", [True, False])
def test_citation_click_copies_decoded_entry_exactly(citation_fragment, secure_clipboard):
    entry, fragment = citation_fragment
    match = BIB_RE.search(fragment)
    assert match is not None
    result = _copy_with_javascript(match.group(1), secure_clipboard=secure_clipboard)
    assert result == {"copied": [entry], "label": "Copied"}


@pytest.mark.parametrize("payload", ["", "not JSON", '{"title": "wrong shape"}'])
def test_malformed_citation_payload_is_not_copied(payload):
    assert _copy_with_javascript(payload, secure_clipboard=True) == {
        "copied": [], "label": "Copy BibTeX",
    }


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
