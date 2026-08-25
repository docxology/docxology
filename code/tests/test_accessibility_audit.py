"""Scope tests for the static public-HTML accessibility audit."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

from accessibility_audit import audited_html_paths  # noqa: E402


def test_audited_html_paths_excludes_local_dependency_html(tmp_path):
    public = tmp_path / "index.html"
    public.write_text("<html></html>", encoding="utf-8")
    dependency = tmp_path / ".venv" / "lib" / "dashboard.html"
    dependency.parent.mkdir(parents=True)
    dependency.write_text("<html></html>", encoding="utf-8")

    assert audited_html_paths(tmp_path) == [public]
