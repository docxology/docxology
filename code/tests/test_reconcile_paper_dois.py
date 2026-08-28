"""Tests for review-gated canonical/artifact DOI reconciliation."""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import reconcile_paper_dois as reconcile  # noqa: E402


def test_proposed_actions_preserve_prior_version_as_artifact(tmp_path):
    metadata = tmp_path / "papers/2026_Example/metadata.json"
    metadata.parent.mkdir(parents=True)
    metadata.write_text(json.dumps({"doi": "10.1234/example-v2", "doi_url": "https://doi.org/10.1234/example-v2"}), encoding="utf-8")
    actions = reconcile.proposed_actions(
        {"2026_Example": "10.1234/example-v1"}, {"2026_Example": metadata}, repo_root=tmp_path
    )
    assert actions == [
        {
            "folder": "2026_Example",
            "metadata_path": "papers/2026_Example/metadata.json",
            "prior_canonical_doi": "10.1234/example-v2",
            "canonical_doi": "10.1234/example-v1",
            "artifact_doi": "10.1234/example-v2",
            "action": "set_canonical_and_preserve_prior_as_artifact",
        }
    ]


def test_proposal_rejects_ambiguous_existing_artifact(tmp_path):
    metadata = tmp_path / "papers/2026_Example/metadata.json"
    metadata.parent.mkdir(parents=True)
    metadata.write_text(json.dumps({"doi": "10.1234/example-v2", "artifact_doi": "10.1234/other"}), encoding="utf-8")
    try:
        reconcile.proposed_actions(
            {"2026_Example": "10.1234/example-v1"}, {"2026_Example": metadata}, repo_root=tmp_path
        )
    except ValueError as exc:
        assert "requires manual DOI-role review" in str(exc)
    else:  # pragma: no cover - assertion branch
        raise AssertionError("ambiguous artifact DOI must block automatic reconciliation")


def test_proposal_rejects_nonempty_malformed_doi_roles(tmp_path):
    metadata = tmp_path / "papers/2026_Example/metadata.json"
    metadata.parent.mkdir(parents=True)
    for field in ("doi", "artifact_doi"):
        metadata.write_text(json.dumps({field: "not a DOI"}), encoding="utf-8")
        try:
            reconcile.proposed_actions(
                {"2026_Example": "10.1234/example-v1"}, {"2026_Example": metadata}, repo_root=tmp_path
            )
        except ValueError as exc:
            assert f"{field} is nonempty but malformed" in str(exc)
        else:  # pragma: no cover - assertion branch
            raise AssertionError(f"malformed {field} must block automatic reconciliation")


def test_apply_requires_a_separate_attributed_approval_record(tmp_path):
    actions = [
        {
            "folder": "2026_Example",
            "metadata_path": "papers/2026_Example/metadata.json",
            "prior_canonical_doi": "",
            "canonical_doi": "10.1234/example-v1",
            "artifact_doi": "",
            "action": "set_canonical_doi",
        }
    ]
    proposal = reconcile.render_report(actions, "a" * 64, status="proposed")
    proposal_path = tmp_path / "proposal.json"
    proposal_path.write_text(json.dumps(proposal), encoding="utf-8")
    approved = reconcile.validate_approval(proposal_path, proposal)

    try:
        reconcile.validate_review_approval(proposal_path, proposal_path, approved)
    except ValueError as exc:
        assert "separate record" in str(exc)
    else:  # pragma: no cover - assertion branch
        raise AssertionError("a generated proposal must not approve itself")

    approval_path = tmp_path / "approval.json"
    approval = {
        "schema_version": "1.0",
        "decision": "approved",
        "proposal_sha256": reconcile.file_sha256(proposal_path),
        "source_sha256": proposal["source_sha256"],
        "actions_sha256": reconcile.actions_sha256(actions),
        "reviewed_by": "Release reviewer",
        "reviewed_at": "2026-08-25T12:00:00Z",
    }
    approval_path.write_text(json.dumps(approval), encoding="utf-8")

    assert reconcile.validate_review_approval(approval_path, proposal_path, approved) == approval
