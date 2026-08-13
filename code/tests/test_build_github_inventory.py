from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import build_github_inventory as bgi  # noqa: E402


def _repo(name: str, *, fork: bool, owner: str = "docxology") -> dict:
    return {
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
    repos = [_repo("primary", fork=False), _repo("upstream-copy", fork=True)]
    counts = bgi.count_repositories(repos)
    counts["primary_total"] = 1
    counts["primary_docxology"] = 1
    counts["primary_ActiveInferenceInstitute"] = 0
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
    assert "const rows = Array.from(document.querySelectorAll('#inventoryRows tr'))" not in primary
    assert "const rows = Array.from(document.querySelectorAll('#inventoryRows tr'))" not in forks
