"""Tests for client-side HTML escape helper."""

from __future__ import annotations

from pathlib import Path


def test_search_utils_escapes_html():
    js = (Path(__file__).resolve().parents[2] / "js" / "search-utils.js").read_text(encoding="utf-8")
    assert "function esc(" in js
    assert "&amp;" in js
    assert "&#39;" in js
    assert "export " not in js
