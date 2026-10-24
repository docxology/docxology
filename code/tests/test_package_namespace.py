"""One shared source file must have one module and class identity."""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.append(str(SRC))
import docxology_tools  # noqa: E402

NEW_MODULES = (
    "art_collections", "artwork_pages", "content_audit", "content_citations",
    "pillar_content", "research_connections",
)


def test_registry_covers_each_shared_source_once():
    sources = {path.stem for path in SRC.glob("*.py")}
    assert set(docxology_tools.MODULES) == sources
    assert len(docxology_tools.MODULES) == len(sources)


@pytest.mark.parametrize("module_name", NEW_MODULES)
@pytest.mark.parametrize("first", ["flat", "dotted"])
def test_real_modules_converge_in_both_import_orders(module_name, first):
    script = """
import importlib, sys
name, first = sys.argv[1:]
first_name = name if first == 'flat' else 'docxology_tools.' + name
importlib.import_module(first_name)
package = importlib.import_module('docxology_tools')
flat = importlib.import_module(name)
dotted = importlib.import_module('docxology_tools.' + name)
assert flat is dotted
assert getattr(package, name) is flat
if name == 'content_audit':
    assert isinstance(flat.ContentPage('<main></main>'), dotted.ContentPage)
"""
    subprocess.run([sys.executable, "-c", script, module_name, first], check=True,
                   env={**os.environ, "PYTHONPATH": str(SRC)})


def test_package_import_remains_lazy_and_needs_no_optional_library():
    script = """
import sys, docxology_tools
assert not (set(docxology_tools.MODULES) & sys.modules.keys())
assert not ({'PIL', 'reportlab', 'playwright'} & sys.modules.keys())
"""
    subprocess.run([sys.executable, "-c", script], check=True,
                   env={**os.environ, "PYTHONPATH": str(SRC)})


@pytest.mark.parametrize("first", ["flat", "dotted"])
def test_minimal_checkout_preserves_exception_catching(tmp_path, first):
    package = tmp_path / "docxology_tools"
    package.mkdir()
    shutil.copy2(SRC / "docxology_tools/__init__.py", package / "__init__.py")
    (tmp_path / "content_citations.py").write_text(
        "class BoundaryFailure(ValueError):\n    pass\n"
        "def reject():\n    raise BoundaryFailure('invalid boundary')\n"
    )
    script = """
import importlib, sys
first = sys.argv[1]
importlib.import_module('content_citations' if first == 'flat' else 'docxology_tools.content_citations')
flat = importlib.import_module('content_citations')
dotted = importlib.import_module('docxology_tools.content_citations')
try:
    flat.reject()
except dotted.BoundaryFailure:
    pass
else:
    raise AssertionError('cross-form exception was not caught')
assert flat is dotted
"""
    subprocess.run([sys.executable, "-c", script, first], cwd=tmp_path, check=True,
                   env={**os.environ, "PYTHONPATH": str(tmp_path)})
