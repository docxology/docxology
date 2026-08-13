"""Tests for Zenodo-only citation rendering."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ORCH = REPO_ROOT / "code" / "orchestrators"
SRC = REPO_ROOT / "code" / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ORCH))

from add_zenodo_only import render_citation  # noqa: E402


def _version_scalar_and_rest(cff: str) -> tuple[str, str]:
    marker = 'version: "'
    start = cff.index(marker) + len(marker)
    i = start
    while i < len(cff):
        if cff[i] == "\\":
            i += 2
            continue
        if cff[i] == '"':
            return cff[start:i], cff[i + 1 :]
        i += 1
    raise AssertionError("unterminated version scalar")


def test_render_citation_version_quote_newline_cannot_inject_yaml_key():
    rec = {"conceptdoi": "10.5281/zenodo.1", "id": 1}
    meta = {
        "title": "Safe Title",
        "publication_date": "2026-01-01",
        "version": '0.1.0"\ninjected: pwned',
        "creators": [{"name": "Friedman, Daniel Ari"}],
    }
    rendered = render_citation(rec, meta)
    inner, rest = _version_scalar_and_rest(rendered)
    assert "injected: pwned" in inner.replace("\\n", "\n")
    assert not re.search(r"^injected:", rest, re.M)
