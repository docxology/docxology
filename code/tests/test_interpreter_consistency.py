"""Child Python processes must inherit the running interpreter.

Every orchestrator that shells out to another repository script used to spawn a
bare ``"python3"``, which resolves through ``PATH`` rather than through the
environment the parent is running in.  Under ``uv run`` the two happen to agree;
run the very same command with ``.venv/bin/python`` (or any other project
interpreter) and the child silently becomes a *different* Python that may not
have the pinned dependencies installed — ``validate_repo.py`` failed exactly
that way with ``ModuleNotFoundError: No module named 'PIL'`` while Pillow was
installed in the environment that launched it.

``sys.executable`` is the fix: the child is always the parent's interpreter.
The one deliberate exception is the CV generator, which must run inside the
locked uv environment for byte-identical ReportLab PDFs and is therefore
invoked as ``uv run python3`` (see ``run_resume_check``).
"""

from __future__ import annotations

import ast
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCANNED_DIRS = ("code/orchestrators", "code/src", "code/tests", "code/tools")
SUBPROCESS_CALLS = {"run", "Popen", "call", "check_call", "check_output"}


def _python_sources() -> list[Path]:
    """Every scanned repository module except this guard's own source.

    The guard quotes both the forbidden and the permitted invocation as literal
    lists, so scanning itself would report its own documentation as a finding.
    """
    this_file = Path(__file__).resolve()
    files: list[Path] = []
    for rel in SCANNED_DIRS:
        files.extend(
            path for path in sorted((REPO_ROOT / rel).glob("*.py"))
            if path.resolve() != this_file
        )
    return files


def _is_subprocess_call(node: ast.Call) -> bool:
    func = node.func
    if isinstance(func, ast.Attribute) and func.attr in SUBPROCESS_CALLS:
        value = func.value
        return isinstance(value, ast.Name) and value.id == "subprocess"
    return False


def _string_elements(node: ast.expr) -> list[str]:
    if not isinstance(node, (ast.List, ast.Tuple)):
        return []
    return [
        element.value
        for element in node.elts
        if isinstance(element, ast.Constant) and isinstance(element.value, str)
    ]


def _bare_interpreter_offenders() -> list[str]:
    offenders: list[str] = []
    for path in _python_sources():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not _is_subprocess_call(node):
                continue
            if not node.args:
                continue
            elements = _string_elements(node.args[0])
            if not elements or elements[0] != "python3":
                continue
            # ``uv run python3 ...`` deliberately re-enters the locked
            # environment instead of the current interpreter.
            offenders.append(f"{path.relative_to(REPO_ROOT)}:{node.lineno}")
    return offenders


def test_no_orchestrator_spawns_a_path_resolved_python3():
    offenders = _bare_interpreter_offenders()
    assert offenders == [], (
        "use sys.executable so the child inherits the running interpreter: "
        + ", ".join(offenders)
    )


def test_the_locked_uv_environment_stays_the_only_documented_exception():
    """The CV generator must keep running under ``uv run`` for pinned ReportLab."""
    uv_invocations: list[str] = []
    for path in _python_sources():
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, (ast.List, ast.Tuple)):
                continue
            elements = _string_elements(node)
            if elements[:3] == ["uv", "run", "python3"]:
                uv_invocations.append(str(path.relative_to(REPO_ROOT)))
    assert sorted(set(uv_invocations)) == [
        "code/orchestrators/regenerate_all.py",
        "code/orchestrators/validate_repo.py",
    ]


def test_the_scan_detects_a_reintroduced_bare_interpreter(tmp_path: Path):
    """The guard fails on a constructed violation, not only on a clean tree."""
    source = "import subprocess\nsubprocess.run(['python3', 'x.py'])\n"
    tree = ast.parse(source)
    calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and _is_subprocess_call(n)]
    assert calls
    assert _string_elements(calls[0].args[0])[0] == "python3"
