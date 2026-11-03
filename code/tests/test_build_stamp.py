"""Build stamp tests: format, commit URL, helpers, footer presence, CSP cleanliness."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

REPO_ROOT = Path(__file__).resolve().parents[2]

from docxology_tools import build_stamp  # noqa: E402

# The label carries two labelled facts: the payload-anchored build (short SHA
# plus that commit's committer date) and the UTC instant this run generated the
# page. The build prefix stays contiguous and first because
# code/src/deploy_freshness.py:STAMP_RE parses the payload SHA from it.
STAMP_TEXT_RE = re.compile(
    r"^build [0-9a-f]{7,40} \d{4}-\d{2}-\d{2} · generated "
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)
FOOTER_STAMP_RE = re.compile(
    r'<p class="build-stamp"><a href="https://github\.com/docxology/docxology/commit/'
    r"([0-9a-f]{7,40})\">(build [^<]+)</a></p>"
)
LABEL_SPLIT = " · generated "


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
    build_part, separator, generated = label.partition(LABEL_SPLIT)
    assert separator, f"label missing the labelled second fact: {label!r}"
    # The binding is unchanged: the label embeds its own sha and committer date.
    _sha, stamp_date = build_stamp.build_stamp_info(REPO_ROOT)
    assert build_part == f"build {sha} {stamp_date}", label
    assert STAMP_TEXT_RE.match(label), f"bad stamp label: {label!r}"
    assert generated == build_stamp.build_generated_at(), label


def test_stamp_label_names_both_facts():
    label = build_stamp.build_stamp_text(REPO_ROOT)
    build_part, separator, generated = label.partition(LABEL_SPLIT)
    # Which payload the page describes, and when it was generated, are separate
    # labelled values rather than one value standing in for the other.
    assert separator, f"label missing the labelled second fact: {label!r}"
    assert re.fullmatch(r"build [0-9a-f]{7,40} \d{4}-\d{2}-\d{2}", build_part), label
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", generated), label
    # The generated instant is a rendering fact, not the payload commit's date.
    assert generated != build_stamp.build_stamp_info(REPO_ROOT)[1], label


def test_generated_at_override_pins_the_rendering_instant(monkeypatch):
    monkeypatch.setenv("BUILD_GENERATED_AT", "2026-03-04T05:06:07Z")
    label = build_stamp.build_stamp_text(REPO_ROOT)
    assert label.endswith(f"{LABEL_SPLIT}2026-03-04T05:06:07Z"), label


def test_generated_at_override_rejects_a_malformed_instant(monkeypatch):
    monkeypatch.setenv("BUILD_GENERATED_AT", "yesterday")
    generated = build_stamp.build_generated_at()
    assert generated != "yesterday"
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", generated), generated


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
    assert sha != "NOT A SHA; rm -rf /"  # falls back to the payload commit


def test_generated_pages_carry_the_footer_stamp():
    sampled = 0
    for rel in (
        "404.html",
        "catalog.html",
        "evidence.html",
        "exports.html",
        "updates.html",
    ):
        html = (REPO_ROOT / rel).read_text(encoding="utf-8")
        match = FOOTER_STAMP_RE.search(html)
        assert match, f"{rel} missing footer build stamp"
        sampled += 1
    assert sampled == 5


def test_work_pages_carry_the_footer_stamp():
    works = REPO_ROOT / "works"
    pages = sorted(p for p in works.glob("*.html") if p.name != "index.html")
    assert pages
    without = [
        p.name
        for p in pages[:40]
        if not FOOTER_STAMP_RE.search(p.read_text(encoding="utf-8"))
    ]
    assert not without, f"work pages missing stamp: {without[:5]}"


def test_stamp_markup_is_csp_clean_and_link_only():
    # The stamp must be a plain link (no inline handlers, no scripts).
    sample = build_stamp.footer_build_stamp_html(REPO_ROOT)
    assert "onclick" not in sample.lower()
    assert "<script" not in sample.lower()


def _stamped_page(body: str, sha: str, generated: str = "2026-01-02T03:04:05Z") -> str:
    label = f"build {sha} 2026-01-02 · generated {generated}"
    return f'<html><main>{body}</main><footer><p class="build-stamp"><a href="https://github.com/docxology/docxology/commit/{sha}">{label}</a></p></footer></html>'


def _legacy_stamped_page(body: str, sha: str) -> str:
    """A page stamped before the label carried its second, labelled fact."""
    return f'<html><main>{body}</main><footer><p class="build-stamp"><a href="https://github.com/docxology/docxology/commit/{sha}">build {sha} 2026-01-02</a></p></footer></html>'


def test_stamp_reuse_requires_complete_equal_content_and_preserves_href():
    old = _stamped_page("same body", "aaaaaaa")
    new = _stamped_page("same body", "bbbbbbb")
    assert build_stamp.reuse_on_disk_stamp(new, old) == old


def test_old_format_on_disk_stamp_is_not_reused():
    """A label without the labelled second fact is upgraded, not preserved.

    Reuse forgives a differing stamp *value*; it must not forgive a differing
    stamp *format*. Otherwise the new footer would converge only as pages
    happened to be edited and ``--check`` would never report the mixed state.
    """
    old = _legacy_stamped_page("same body", "aaaaaaa")
    new = _stamped_page("same body", "bbbbbbb")
    assert build_stamp.reuse_on_disk_stamp(new, old) == new


def test_changed_content_gets_current_stamp_instead_of_old_provenance():
    old = _stamped_page("old body", "aaaaaaa")
    new = _stamped_page("corrected body", "bbbbbbb")
    assert build_stamp.reuse_on_disk_stamp(new, old) == new


def test_stamp_fragment_cannot_claim_equality_of_a_whole_page():
    old = _stamped_page("old body", "aaaaaaa")
    new = '<p class="build-stamp"><a href="new">build bbbbbbb 2026-01-02</a></p>'
    assert build_stamp.reuse_on_disk_stamp(new, old) == new


def test_multiple_stamps_are_not_normalized_away():
    old = _stamped_page("same body", "aaaaaaa")
    new = _stamped_page("same body", "bbbbbbb")
    assert build_stamp.reuse_on_disk_stamp(new + new, old + old) == new + new


def _load_validate_repo():
    """Import validate_repo.py without running its CLI."""
    spec = importlib.util.spec_from_file_location(
        "validate_repo_for_stamp_test",
        REPO_ROOT / "code" / "orchestrators" / "validate_repo.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_validate_build_stamp_labels_rejects_a_legacy_page(tmp_path, monkeypatch):
    """Negative control: the repo validator fails on an old-format stamp.

    This is the assertion that makes the adoption complete. Without it, a
    format change would be forgiven on every unchanged page and mixed formats
    could ship while ``--check`` stayed green.
    """
    validator = _load_validate_repo()
    page = tmp_path / "legacy.html"
    page.write_text(_legacy_stamped_page("same body", "aaaaaaa"), encoding="utf-8")
    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)

    with pytest.raises(SystemExit) as excinfo:
        validator.validate_build_stamp_labels()

    assert "legacy.html" in str(excinfo.value)


def test_validate_build_stamp_labels_accepts_current_and_unstamped_pages(
    tmp_path, monkeypatch
):
    """Positive control: a current label passes, and a page without one is exempt."""
    validator = _load_validate_repo()
    (tmp_path / "current.html").write_text(
        _stamped_page("current body", "aaaaaaa"), encoding="utf-8"
    )
    (tmp_path / "plain.html").write_text(
        "<html><body>hand-authored, no stamp</body></html>", encoding="utf-8"
    )
    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)

    validator.validate_build_stamp_labels()


def _prefixless_stamped_page(body: str, sha: str) -> str:
    """A stamped page whose label lost the fixed ``build `` prefix.

    The anchor is structurally intact, so the page is not unstamped: it is
    stamped with a label no consumer can parse.
    """
    return f'<html><main>{body}</main><footer><p class="build-stamp"><a href="https://github.com/docxology/docxology/commit/{sha}">generated 2026-01-02T03:04:05Z</a></p></footer></html>'


def test_validate_build_stamp_labels_rejects_a_prefixless_label(tmp_path, monkeypatch):
    """An anchor whose label does not parse is a problem, not an absence.

    ``STAMP_HTML_RE`` requires the fixed ``build `` prefix, so a prefixless
    anchor is invisible to it and would otherwise read as an unstamped page.
    The gate counts the raw marker against the anchors that parse, so the label
    is reported instead of exempted.
    """
    validator = _load_validate_repo()
    (tmp_path / "prefixless.html").write_text(
        _prefixless_stamped_page("same body", "aaaaaaa"), encoding="utf-8"
    )
    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)

    with pytest.raises(SystemExit) as excinfo:
        validator.validate_build_stamp_labels()

    assert "prefixless.html" in str(excinfo.value)


def test_validate_build_stamp_labels_rejects_unparseable_anchor_markup(
    tmp_path, monkeypatch
):
    """A marker that is not a parseable anchor is reported, not skipped."""
    validator = _load_validate_repo()
    (tmp_path / "broken.html").write_text(
        '<html><footer><p class="build-stamp">build aaaaaaa 2026-01-02'
        " · generated 2026-01-02T03:04:05Z</p></footer></html>",
        encoding="utf-8",
    )
    monkeypatch.setattr(validator, "REPO_ROOT", tmp_path)

    with pytest.raises(SystemExit) as excinfo:
        validator.validate_build_stamp_labels()

    assert "broken.html" in str(excinfo.value)


def test_find_stamp_label_problems_ignores_pages_without_a_marker(tmp_path):
    """A page with no stamp marker at all stays exempt."""
    page = tmp_path / "plain.html"
    page.write_text("<html><body>hand-authored</body></html>", encoding="utf-8")
    assert build_stamp.find_stamp_label_problems([page]) == []
