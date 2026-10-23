"""Exercise test-runner failure and selection policy through real pytest runs."""
from __future__ import annotations

import ast
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]


def run_suite(root: Path, source: str, *, parallel: bool = False) -> subprocess.CompletedProcess[str]:
    """Run a disposable suite with the repository's actual runner hooks."""
    policy = ROOT / "code/tests/conftest.py"
    if policy.exists():
        shutil.copy2(policy, root / "conftest.py")
    (root / "test_example.py").write_text(source, encoding="utf-8")
    environment = dict(os.environ, PYTEST_DISABLE_PLUGIN_AUTOLOAD="1")
    environment.pop("PYTEST_ADDOPTS", None)
    environment.pop("PYTEST_PLUGINS", None)
    command = [sys.executable, "-m", "pytest", "-q", "-rs", "--basetemp", str(root / "isolated-tests")]
    if parallel:
        command += ["-p", "xdist.plugin", "-n", "2"]
    return subprocess.run(command, cwd=root, env=environment, capture_output=True, text=True, timeout=45)


@pytest.mark.parametrize("source", [
    "import pytest\npytest.skip('collection prerequisite absent', allow_module_level=True)\n",
    "import pytest\n@pytest.fixture\ndef capability():\n    pytest.skip('fixture prerequisite absent')\ndef test_example(capability):\n    pass\n",
    "import pytest\ndef test_example():\n    pytest.skip('body prerequisite absent')\n",
])
@pytest.mark.parametrize("parallel", [False, True], ids=["serial", "workers"])
def test_selected_skips_fail_the_run(tmp_path, source, parallel):
    result = run_suite(tmp_path, source, parallel=parallel)
    assert result.returncode == 1, result.stdout + result.stderr
    assert "Selected tests did not execute" in result.stdout
    assert "prerequisite absent" in result.stdout


def test_disposable_non_repository_does_not_discover_enclosing_git(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    result = run_suite(tmp_path, '''import subprocess
def test_example(tmp_path):
    probe = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=tmp_path, capture_output=True)
    assert probe.returncode != 0, probe.stdout
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    probe = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=tmp_path, capture_output=True, text=True)
    assert probe.returncode == 0
    assert probe.stdout.strip() == str(tmp_path)
''')
    assert result.returncode == 0, result.stdout + result.stderr


def test_passing_run_remains_successful(tmp_path):
    result = run_suite(tmp_path, "def test_example():\n    assert 2 + 2 == 4\n")
    assert result.returncode == 0, result.stdout + result.stderr


def test_browser_modules_and_native_render_are_explicitly_selected():
    """New browser modules must join marker-based CI without a filename list."""
    for path in (ROOT / "code/tests").glob("test_*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        if any((isinstance(node, ast.ImportFrom) and node.module and node.module.startswith("playwright."))
               or (isinstance(node, ast.Import) and any(name.name == "playwright" or name.name.startswith("playwright.") for name in node.names))
               for node in ast.walk(tree)):
            assert any(isinstance(node, ast.Assign) and ast.unparse(node.value) == "pytest.mark.browser"
                       and any(isinstance(target, ast.Name) and target.id == "pytestmark" for target in node.targets)
                       for node in tree.body), f"Unselected browser module: {path.name}"
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == "test_real_four_format_render_and_receipt":
                assert "pytest.mark.manuscript_render" in [ast.unparse(mark) for mark in node.decorator_list]
