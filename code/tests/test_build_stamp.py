"""Build stamp tests: format, commit URL, helpers, footer presence, CSP cleanliness."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import build_stamp  # noqa: E402

STAMP_TEXT_RE = re.compile(r"^build [0-9a-f]{7,40} \d{4}-\d{2}-\d{2}$")
FOOTER_STAMP_RE = re.compile(
    r'<p class="build-stamp"><a href="https://github\.com/docxology/docxology/commit/'
    r"([0-9a-f]{7,40})\">(build [^<]+)</a></p>"
)


def test_build_stamp_text_format_matches_spec():
    text = build_stamp.build_stamp_text(REPO_ROOT)
    assert STAMP_TEXT_RE.match(text), f"bad stamp format: {text!r}"


def test_build_stamp_url_points_at_the_embedded_sha():
    sha, _ = build_stamp.build_stamp_info(REPO_ROOT)
    url = build_stamp.build_stamp_url(REPO_ROOT)
    assert url == f"https://github.com/docxology/docxology/commit/{sha}"


def test_footer_build_stamp_html_shape():
    html = build_stamp.footer_build_stamp_html(REPO_ROOT)
    match = FOOTER_STAMP_RE.search(html)
    assert match, f"bad footer stamp html: {html!r}"
    sha, label = match.groups()
    assert label == f"build {sha} {label.split()[-1]}"  # label embeds its own sha


def test_env_overrides_pin_the_stamp(monkeypatch):
    monkeypatch.setenv("BUILD_SHA", "deadbee1234")
    monkeypatch.setenv("BUILD_DATE", "2026-01-02")
    sha, date = build_stamp.build_stamp_info(REPO_ROOT)
    assert sha == "deadbee1234"
    assert date == "2026-01-02"


def test_env_overrides_reject_malformed_values(monkeypatch):
    monkeypatch.setenv("BUILD_SHA", "NOT A SHA; rm -rf /")
    monkeypatch.setenv("BUILD_DATE", "2026-01-02")
    sha, _ = build_stamp.build_stamp_info(REPO_ROOT)
    assert sha != "NOT A SHA; rm -rf /"  # falls back to git HEAD


def test_generated_pages_carry_the_footer_stamp():
    sampled = 0
    for rel in ("404.html", "catalog.html", "evidence.html", "exports.html", "updates.html"):
        html = (REPO_ROOT / rel).read_text(encoding="utf-8")
        match = FOOTER_STAMP_RE.search(html)
        assert match, f"{rel} missing footer build stamp"
        sampled += 1
    assert sampled == 5


def test_work_pages_carry_the_footer_stamp():
    works = REPO_ROOT / "works"
    pages = sorted(p for p in works.glob("*.html") if p.name != "index.html")
    assert pages
    without = [p.name for p in pages[:40] if not FOOTER_STAMP_RE.search(p.read_text(encoding="utf-8"))]
    assert not without, f"work pages missing stamp: {without[:5]}"


def test_stamp_markup_is_csp_clean_and_link_only():
    # The stamp must be a plain link (no inline handlers, no scripts).
    sample = build_stamp.footer_build_stamp_html(REPO_ROOT)
    assert "onclick" not in sample.lower()
    assert "<script" not in sample.lower()
