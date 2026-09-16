"""Scope tests for the static public-HTML accessibility audit."""

from __future__ import annotations

import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)


from accessibility_audit import audited_html_paths  # noqa: E402


def test_audited_html_paths_excludes_local_dependency_html(tmp_path):
    public = tmp_path / "index.html"
    public.write_text("<html></html>", encoding="utf-8")
    dependency = tmp_path / ".venv" / "lib" / "dashboard.html"
    dependency.parent.mkdir(parents=True)
    dependency.write_text("<html></html>", encoding="utf-8")

    assert audited_html_paths(tmp_path) == [public]
