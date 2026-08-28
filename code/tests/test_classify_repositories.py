from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
import classify_repositories  # noqa: E402


def test_repository_classification_exposes_description_quality_and_review_contract():
    payload = classify_repositories.build_payload()
    rows = payload["repositories"]
    assert rows
    required = {
        "full_name", "github_id", "github_node_id", "name", "owner", "html_url", "fork", "archived", "private",
        "description", "description_quality", "catalog_role", "exclusion_reason", "review_status",
    }
    assert required <= set(rows[0])
    assert {row["review_status"] for row in rows} <= {"defer", "acknowledged", "accept", "reject", "supersede"}
    # Deliberate human-reviewed exclusions carry an acknowledged status + reason
    # and drop out of the primary review queue (see data/repository-exclusions.json).
    for row in rows:
        if row["review_status"] == "acknowledged":
            assert row.get("acknowledged_reason")
            assert row.get("reviewed_by") == "principal"
            assert row.get("reviewed_at") == "2026-08-26"
            assert isinstance(row["github_id"], int) and row["github_id"] > 0
            assert isinstance(row["github_node_id"], str) and row["github_node_id"]
            if row["fork"]:
                assert row["catalog_role"] == "acknowledged_not_curated"
                assert row["exclusion_reason"] == "fork_not_curated"
                assert row["acknowledged_reason"] == "fork_not_curated"
            else:
                assert row["exclusion_reason"] == "acknowledged_not_catalogued"
    approved_forks = [row for row in rows if row["fork"] and row["review_status"] == "acknowledged"]
    assert len(approved_forks) == payload["summary"]["forks"]
    assert payload["summary"]["acknowledged_forks"] == len(approved_forks)
    assert payload["summary"]["primary_requires_review"] + payload["summary"]["acknowledged_excluded"] + payload["summary"]["forks"] == len(rows)
    assert payload["summary"]["uncatalogued"] == len(rows)
    assert payload["summary"]["missing_description"] + payload["summary"]["short_description"] + payload["summary"]["substantive_description"] == len(rows)


def test_repository_classification_projection_is_current():
    actual = json.loads((REPO_ROOT / "data" / "repository-classification.json").read_text(encoding="utf-8"))
    expected = classify_repositories.build_payload()
    expected["generated_at"] = actual["generated_at"]
    assert actual == expected


def test_malformed_fork_exclusion_cannot_clear_the_review_queue():
    payload = {
        "schema_version": "1.3",
        "reasons": {
            "fork_not_curated": "A reviewed public fork remains out of catalog."
        },
        "exclusions": [
            {
                "full_name": "example/fork",
                "reason": "fork_not_curated",
                "reviewed_by": "principal",
                "note": "This fork was reviewed.",
            }
        ],
    }

    try:
        classify_repositories.validate_acknowledged_exclusions(payload)
    except ValueError as exc:
        assert "reviewed_at" in str(exc)
    else:
        raise AssertionError("a fork exclusion without reviewed_at was accepted")

    primary_reason = {
        "full_name": "example/fork",
        "reason": "profile_repo",
        "note": "Wrong kind of exclusion for a fork.",
        "github_id": 1,
        "github_node_id": "R_kgDOexample",
    }
    assert (
        classify_repositories.acknowledged_exclusion(
            primary_reason,
            fork=True,
            github_id=1,
            github_node_id="R_kgDOexample",
        )
        is None
    )


def test_malformed_primary_exclusion_cannot_clear_the_review_queue():
    payload = {
        "schema_version": "1.3",
        "reasons": {
            "profile_repo": "The profile repository is deliberately not catalogued."
        },
        "exclusions": [
            {
                "full_name": "example/profile",
                "reason": "profile_repo",
                "note": "The primary exclusion was reviewed, but its receipt is incomplete.",
            }
        ],
    }

    try:
        classify_repositories.validate_acknowledged_exclusions(payload)
    except ValueError as exc:
        assert "reviewed_by" in str(exc)
    else:
        raise AssertionError("a primary exclusion without reviewed_by was accepted")


def test_recreated_repository_cannot_inherit_a_path_only_exclusion(
    tmp_path: Path, monkeypatch
):
    """A transferred/recreated repo has a new immutable identity despite its name."""
    inventory = tmp_path / "github-repositories.json"
    exclusions = tmp_path / "repository-exclusions.json"
    inventory.write_text(
        json.dumps(
            {
                "repositories": [
                    {
                        "full_name": "example/recreated",
                        "github_id": 202,
                        "github_node_id": "R_kgDOCurrent",
                        "name": "recreated",
                        "owner": "example",
                        "html_url": "https://github.com/example/recreated",
                        "fork": False,
                        "archived": False,
                        "private": False,
                        "description": "A replacement repository with the same path.",
                        "language": "Python",
                        "topics": [],
                        "recently_updated": True,
                        "curated": False,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    exclusions.write_text(
        json.dumps(
            {
                "schema_version": "1.3",
                "reasons": {"profile_repo": "Reviewed profile infrastructure."},
                "exclusions": [
                    {
                        "full_name": "example/recreated",
                        "github_id": 101,
                        "github_node_id": "R_kgDOFormer",
                        "reason": "profile_repo",
                        "reviewed_by": "principal",
                        "reviewed_at": "2026-08-26",
                        "note": "This applies only to the prior immutable repository.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(classify_repositories, "IN", inventory)
    monkeypatch.setattr(classify_repositories, "EXCLUSIONS", exclusions)

    row = classify_repositories.build_payload()["repositories"][0]
    assert row["full_name"] == "example/recreated"
    assert row["review_status"] == "defer"
    assert row["exclusion_reason"] == "primary_repo_requires_manual_review"
