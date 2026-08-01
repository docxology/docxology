"""Tests for the client-side HTML escape helper (js/search-utils.js).

These execute the real ``esc()`` function through Node on concrete inputs, so
the test fails if the escape logic is broken — the old version only grepped the
source for substrings and would pass even if ``esc`` returned input unchanged.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

JS = Path(__file__).resolve().parents[2] / "js" / "search-utils.js"


def _node_path() -> str:
    node = shutil.which("node")
    if node is None:
        pytest.skip("node interpreter not available")
    return node


def _esc(value: str) -> str:
    node = _node_path()
    source = JS.read_text(encoding="utf-8")
    program = (
        source
        + "\nprocess.stdout.write(JSON.stringify(esc("
        + json.dumps(value)
        + ")));"
    )
    out = subprocess.run([node, "-e", program], capture_output=True, text=True, check=True)
    return json.loads(out.stdout)


def test_source_is_a_plain_global_script():
    js = JS.read_text(encoding="utf-8")
    assert "function esc(" in js
    assert "export " not in js


def test_esc_escapes_html_meta_characters():
    assert _esc("<a href='x'>&") == "&lt;a href=&#39;x&#39;&gt;&amp;"


def test_esc_escapes_double_quotes():
    assert _esc('Tom & "Jerry"') == "Tom &amp; &quot;Jerry&quot;"


def test_esc_leaves_plain_text_unchanged():
    assert _esc("plain text 123") == "plain text 123"
