"""Regression tests for the public agent route manifest."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_agent_index_is_current_and_has_stable_routes():
    path = REPO_ROOT / "data" / "agent-index.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1.0"
    routes = {route["id"]: route for route in payload["routes"]}
    assert routes["publications"]["path"] == "/publications.html"
    assert routes["agent-index"]["format"] == "application/json"
    assert payload["datasets"]["works"]["count"] == json.loads((REPO_ROOT / "data/works.json").read_text())["count"]
    assert payload["freshness"]["verification"] == "/cite-verify.html"


def test_agent_index_check_command_passes():
    result = subprocess.run(
        ["python3", "code/orchestrators/build_agent_index.py", "--check"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
