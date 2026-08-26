from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import build_github_inventory as bgi  # noqa: E402


def _repo(name: str, *, fork: bool, owner: str = "docxology") -> dict:
    return {
        "github_id": 1000 + len(owner) + len(name),
        "github_node_id": f"R_kgDO_{owner}_{name}",
        "name": name,
        "full_name": f"{owner}/{name}",
        "owner": owner,
        "html_url": f"https://github.com/{owner}/{name}",
        "description": f"{name} description",
        "homepage": "",
        "language": "Python",
        "stars": 1,
        "forks": 0,
        "watchers": 1,
        "open_issues": 0,
        "visibility": "public",
        "private": False,
        "fork": fork,
        "archived": False,
        "disabled": False,
        "is_template": False,
        "topics": [],
        "license": "",
        "default_branch": "main",
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-02T00:00:00Z",
        "pushed_at": "2026-01-02T00:00:00Z",
        "curated": not fork,
        "recently_updated": True,
    }


def test_repository_pages_split_primary_and_forks():
    repos = [
        _repo("primary", fork=False),
        _repo("aii-primary", fork=False, owner="ActiveInferenceInstitute"),
        _repo("upstream-copy", fork=True),
    ]
    counts = bgi.count_repositories(repos)
    counts["primary_total"] = 2
    counts["primary_docxology"] = 1
    counts["primary_ActiveInferenceInstitute"] = 1
    counts["fork_docxology"] = 1
    counts["fork_ActiveInferenceInstitute"] = 0
    payload = {
        "generated_at": "2026-01-03T00:00:00Z",
        "warnings": [],
        "counts": counts,
        "repositories": repos,
    }

    primary = bgi.render_html(payload)
    forks = bgi.render_html(payload, forks=True)

    assert "Primary GitHub Repository Inventory" in primary
    assert "docxology/primary" in primary
    assert "docxology/upstream-copy" not in primary
    assert 'data-fork="true"' not in primary
    assert "Forked GitHub Repository Archive" in forks
    assert "docxology/upstream-copy" in forks
    assert "docxology/primary" not in forks
    assert 'data-fork="true"' in forks
    assert "/js/repo-inventory.js" in primary
    assert "/js/repo-inventory.js" in forks
    assert 'http-equiv="Content-Security-Policy"' in primary
    assert 'name="referrer" content="strict-origin-when-cross-origin"' in primary
    assert '<a href="data/agent-index.json">Agent Map</a>' in primary
    assert 'http-equiv="Content-Security-Policy"' in forks
    assert '<a href="data/agent-index.json">Agent Map</a>' in forks
    assert "const rows = Array.from(document.querySelectorAll('#inventoryRows tr'))" not in primary
    assert "const rows = Array.from(document.querySelectorAll('#inventoryRows tr'))" not in forks


def test_cached_inventory_render_is_idempotent_and_check_fails_on_drift(tmp_path: Path):
    """The no-network derivative must detect every byte of page drift."""
    repos = [
        _repo("primary", fork=False),
        _repo("aii-primary", fork=False, owner="ActiveInferenceInstitute"),
        _repo("upstream-copy", fork=True),
    ]
    counts = bgi.count_repositories(repos)
    counts.update(
        {
            "primary_total": 2,
            "primary_docxology": 1,
            "primary_ActiveInferenceInstitute": 1,
            "fork_docxology": 1,
            "fork_ActiveInferenceInstitute": 0,
        }
    )
    payload = {
        "generated_at": "2026-01-03T00:00:00Z",
        "warnings": [],
        "counts": counts,
        "repositories": repos,
    }
    cache = tmp_path / "data" / "github-repositories.json"
    cache.parent.mkdir()
    cache.write_text(json.dumps(payload), encoding="utf-8")
    primary = tmp_path / "repositories.html"
    forks = tmp_path / "repositories-forks.html"
    baseline = tmp_path / "missing-baseline.json"

    bgi.render_cached_inventory_outputs(
        json_out=cache, primary_html_out=primary, forks_html_out=forks
    )
    first = (primary.read_bytes(), forks.read_bytes())
    bgi.check_outputs(
        json_out=cache,
        primary_html_out=primary,
        forks_html_out=forks,
        baseline_path=baseline,
    )
    primary.write_text(primary.read_text(encoding="utf-8").replace("Agent Map", "Missing"), encoding="utf-8")
    with pytest.raises(SystemExit, match="repositories.html is stale"):
        bgi.check_outputs(
            json_out=cache,
            primary_html_out=primary,
            forks_html_out=forks,
            baseline_path=baseline,
        )

    bgi.render_cached_inventory_outputs(
        json_out=cache, primary_html_out=primary, forks_html_out=forks
    )
    assert (primary.read_bytes(), forks.read_bytes()) == first

    broken = json.loads(cache.read_text(encoding="utf-8"))
    broken["repositories"][0]["github_node_id"] = ""
    cache.write_text(json.dumps(broken), encoding="utf-8")
    with pytest.raises(SystemExit, match="missing immutable github_id/github_node_id"):
        bgi.check_outputs(
            json_out=cache,
            primary_html_out=primary,
            forks_html_out=forks,
            baseline_path=baseline,
        )


def test_normalize_repo_retains_immutable_github_identity():
    raw = {
        "id": 12345,
        "node_id": "R_kgDOExample",
        "owner": {"login": "docxology"},
        "name": "example",
        "full_name": "docxology/example",
        "html_url": "https://github.com/docxology/example",
        "updated_at": "2026-08-25T00:00:00Z",
    }

    normalized = bgi.normalize_repo(
        raw, set(), "2026-08-26T00:00:00Z"
    )

    assert normalized["github_id"] == 12345
    assert normalized["github_node_id"] == "R_kgDOExample"
