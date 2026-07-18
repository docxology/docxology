"""Regression tests for the public agent route manifest."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_agent_index_is_current_and_has_stable_routes():
    path = REPO_ROOT / "data" / "agent-index.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == "1.2"
    routes = {route["id"]: route for route in payload["routes"]}
    assert routes["publications"]["path"] == "/publications.html"
    assert routes["repositories"]["path"] == "/repositories.html"
    assert routes["agent-index"]["format"] == "application/json"
    assert payload["datasets"]["works"]["count"] == json.loads((REPO_ROOT / "data/works.json").read_text())["count"]
    assert payload["datasets"]["repositories"]["count"] == json.loads(
        (REPO_ROOT / "data/github-repositories.json").read_text()
    )["counts"]["total"]
    assert set(("Work", "SoftwareRepository", "Repository", "ClaimWithEvidence", "SearchResult", "GeneratedReport")) <= set(
        payload["schemas"]
    )
    assert payload["datasets"]["artworks_index"]["schema"] == "ArtworkIndex"
    assert payload["schema_examples"]["ArtworkIndex"]
    assert payload["schemas"]["Work"]["fields"]["citation_key"]
    assert payload["schema_examples"]["Work"]
    assert payload["dataset_hashes"]["works"]
    assert payload["hosted_availability"]["artifact_manifest"] == "/data/pages-artifact-manifest.json"
    assert payload["source_provenance"]["generated_by"].endswith("build_agent_index.py")
    assert payload["reports"]
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
