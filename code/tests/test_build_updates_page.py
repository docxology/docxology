"""Changelog parsing and inline rendering for the generated updates page."""

from __future__ import annotations

import sys
from pathlib import Path

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

from build_updates_page import inline_md, parse_changelog, plain_md  # noqa: E402

WRAPPED = """# Changelog

## 2026-10-05

- **Wrapped item:** the first physical line
  continues here and
  ends here.
- Single-line item.
  - **Nested item:** starts
    and continues.

## 2026-10-02

Intro paragraph that is not a bullet.

- Older item.
"""


def test_wrapped_bullets_keep_their_continuation_lines() -> None:
    sections = parse_changelog(WRAPPED)
    assert [section["date"] for section in sections] == ["2026-10-05", "2026-10-02"]
    assert sections[0]["items"] == [
        "**Wrapped item:** the first physical line continues here and ends here.",
        "Single-line item.",
        "**Nested item:** starts and continues.",
    ]
    assert sections[1]["items"] == ["Older item."]


def test_inline_markdown_renders_bold_without_stray_asterisks() -> None:
    rendered = inline_md("**Bold title:** see `code` and *emphasis* in [docs](docs/README.md)")
    assert rendered == (
        '<strong>Bold title:</strong> see <code>code</code> and <em>emphasis</em> '
        'in <a href="docs/README.md">docs</a>'
    )
    assert "*" not in rendered


def test_asterisks_inside_code_spans_do_not_open_emphasis() -> None:
    rendered = inline_md("**no `papers/*/metadata.json` or `pages/X.md` rewrites were accepted**")
    assert rendered == (
        "<strong>no <code>papers/*/metadata.json</code> or <code>pages/X.md</code> "
        "rewrites were accepted</strong>"
    )


def test_plain_markdown_for_structured_data() -> None:
    assert plain_md("**Bold:** `x` and *y* [z](a.md)") == "Bold: x and y z"
    assert plain_md("**no `papers/*/metadata.json` rewrites**") == "no papers/*/metadata.json rewrites"


def test_every_real_changelog_bullet_is_complete() -> None:
    root = Path(__file__).resolve().parents[2]
    text = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    items = [item for section in parse_changelog(text) for item in section["items"]]
    continuation_lines = [
        line.strip()
        for line in text.splitlines()
        if line[:1].isspace() and line.strip() and not line.strip().startswith("- ")
    ]
    joined = "\n".join(items)
    assert all(line in joined for line in continuation_lines)
