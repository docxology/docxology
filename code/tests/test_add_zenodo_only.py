"""Tests for Zenodo-only citation rendering."""

from __future__ import annotations

import re
import json
import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)


from add_zenodo_only import render_citation  # noqa: E402
import add_zenodo_only  # noqa: E402


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


def test_zenodo_intake_rejects_unsafe_key_before_bibliography_write(tmp_path, monkeypatch):
    import pytest
    from docxology_tools.work_identifiers import WorkIdentifierError
    bibliography = tmp_path / "BIBLIOGRAPHY.md"
    bibliography.write_text("| # | Year | Domain | Type | Title | Venue | DOI/Link | Docs |\n", encoding="utf-8")
    registry = tmp_path / "data/work-identifiers.json"
    registry.parent.mkdir()
    registry.write_text(json.dumps({"schema_version": "WorkIdentifierRegistry.v1", "identifiers": {}}) + "\n", encoding="utf-8")
    monkeypatch.setattr(add_zenodo_only, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(add_zenodo_only, "BIB", bibliography)
    before = (bibliography.read_bytes(), registry.read_bytes())
    with pytest.raises(WorkIdentifierError, match="unsafe citation key"):
        add_zenodo_only.add_bib_row(1, "2026", "🧠", "Paper", "A" * 220, "10.5281/zenodo.1", "2026_Example")
    assert (bibliography.read_bytes(), registry.read_bytes()) == before
