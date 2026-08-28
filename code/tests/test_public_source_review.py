"""Tests for the review-only public-source evidence report."""

from __future__ import annotations

import json
import hashlib
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "code" / "src"
ORCH = REPO_ROOT / "code" / "orchestrators" / "build_public_source_review.py"
sys.path.insert(0, str(SRC_DIR))
sys.path.insert(0, str(ORCH.parent))

import build_public_source_review  # noqa: E402
from public_source_review import (  # noqa: E402
    build_review_report,
    render_json,
    render_markdown,
    validate_review_report,
)


def _write_json(path: Path, payload: dict) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def _inputs(root: Path) -> dict[str, Path]:
    reports = root / "reports"
    data = root / "data"
    snapshot = _write_json(
        reports / "public_source_snapshot_2026-08-25.json",
        {
            "generated_at": "2026-08-25T12:00:00Z",
            "source_commit": "a" * 40,
            "facts": {"AII officers": {"value": "fresh"}},
            "checks": [{"url": "https://example.test/officers", "ok": True}],
        },
    )
    previous_snapshot = _write_json(
        reports / "public_source_snapshot_2026-08-24.json",
        {
            "generated_at": "2026-08-24T12:00:00Z",
            "source_commit": "b" * 40,
            "facts": {"AII officers": {"value": "prior"}},
            "checks": [],
        },
    )
    inventory = _write_json(
        reports / "public_source_inventory_2026-08-25.json",
        {
            "generated_at": "2026-08-25T12:00:00Z",
            "source_commit": "a" * 40,
            "sections": [{"url": "https://example.test/profile", "ok": True}],
        },
    )
    paired = _write_json(
        reports / "paired_publications_2026-08-25.json",
        {
            "generated_at": "2026-08-25T12:00:00Z",
            "actions": [
                {
                    "action_type": "update_existing",
                    "doi": "10.1234/zenodo-candidate",
                    "github_release_url": "https://github.example/releases/v1",
                    "zenodo_record_url": "https://zenodo.example/1",
                    "title": "Candidate",
                    "confidence": "strong",
                },
                {
                    "action_type": "needs_review",
                    "doi": "10.1234/ambiguous",
                    "github_release_url": "https://github.example/releases/v2",
                    "title": "Ambiguous",
                    "confidence": "needs_review",
                },
                {
                    "action_type": "already_reviewed",
                    "doi": "10.1234/rejected",
                    "github_repo": "example/rejected",
                    "github_release_url": "https://github.example/releases/v3",
                    "zenodo_record_url": "https://zenodo.example/3",
                    "title": "Rejected pair",
                    "release_tag": "v3",
                },
            ],
        },
    )
    decisions = _write_json(
        data / "paired-publication-decisions.json",
        {
            "decision_summary": {
                "note": "The complete candidate was manually reviewed for this fixture."
            },
            "groups": [
                {
                    "id": "R01",
                    "decision": "rejected",
                    "decided_by": "user",
                    "decided_at": "2026-08-25T12:30:00Z",
                    "doi": "10.1234/rejected",
                    "title": "Rejected pair",
                    "candidate_github_repo": "example/rejected",
                    "raw_candidates": [
                        {
                            "doi": "10.1234/rejected",
                            "github_repo": "example/rejected",
                            "github_release_url": "https://github.example/releases/v3",
                            "zenodo_record_url": "https://zenodo.example/3",
                            "record_title": "Rejected pair",
                            "release_tag": "v3",
                        }
                    ],
                }
            ]
        },
    )
    doi_review = _write_json(
        reports / "doi_role_reconciliation_2026-08-25.proposed.json",
        {
            "status": "proposed",
            "actions": [
                {
                    "folder": "2026_Candidate",
                    "prior_canonical_doi": "10.1234/version",
                    "canonical_doi": "10.1234/citation",
                    "artifact_doi": "10.1234/version",
                    "action": "set_canonical_and_preserve_prior_as_artifact",
                }
            ],
            "conflicts": [
                {"folder": "2026_Conflict", "code": "canonical_doi_mismatch"}
            ],
        },
    )
    classifications = _write_json(
        data / "repository-classification.json",
        {
            "repositories": [
                {
                    "full_name": "example/defer",
                    "review_status": "defer",
                    "catalog_role": "not_curated",
                },
                {
                    "full_name": "example/acknowledged",
                    "review_status": "acknowledged",
                    "catalog_role": "acknowledged_not_curated",
                },
                {
                    "full_name": "example/rejected",
                    "review_status": "rejected",
                    "catalog_role": "not_curated",
                },
            ]
        },
    )
    claims = _write_json(
        data / "claims.json",
        {
            "claims": [
                {
                    "id": "google-scholar-citations",
                    "status": "dated-snapshot",
                    "claim": "Scholar snapshot",
                    "sources": ["data/scholar-snapshot.json"],
                },
                {
                    "id": "aii-officer-roles",
                    "status": "public-profile",
                    "claim": "Officers",
                    "checked_at": "2026-05-16",
                    "sources": ["https://example.test/officers"],
                },
                {
                    "id": "stanford-phd",
                    "status": "public-institutional-record",
                    "claim": "PhD",
                    "sources": ["https://example.test/profile"],
                },
            ]
        },
    )
    scholar = _write_json(
        data / "scholar-snapshot.json",
        {"profile_id": "canonical", "citations": 10, "h_index": 2, "i10_index": 3},
    )
    observation_decisions = _write_json(
        data / "public-source-observation-decisions.json",
        {"schema_version": "1.0", "decisions": []},
    )
    biographical_claim_decisions = _write_json(
        data / "biographical-claim-decisions.json",
        {"schema_version": "1.0", "decisions": []},
    )
    return {
        "snapshot_path": snapshot,
        "previous_snapshot_path": previous_snapshot,
        "inventory_path": inventory,
        "paired_publications_path": paired,
        "pair_decisions_path": decisions,
        "doi_review_path": doi_review,
        "repository_classification_path": classifications,
        "claims_path": claims,
        "scholar_snapshot_path": scholar,
        "observation_decisions_path": observation_decisions,
        "biographical_claim_decisions_path": biographical_claim_decisions,
    }


def _item(report: dict, identifier: str) -> dict:
    return next(item for item in report["items"] if item["id"] == identifier)


def _json_sha256(value: object) -> str:
    rendered = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def test_review_input_resolution_defaults_to_direct_scholar_receipt():
    """The dated evidence report must bind Scholar claims to their receipt."""
    args = build_public_source_review.build_parser().parse_args([])
    inputs = build_public_source_review._resolve_inputs(
        args,
        report_path=REPO_ROOT / "reports" / "public_source_review_2026-08-26.json",
    )

    assert inputs["scholar_receipt_path"] == (
        REPO_ROOT / "data" / "scholar-verification-receipt.json"
    )


def test_review_check_selection_ignores_malformed_newer_report_names(tmp_path: Path):
    reports = tmp_path / "reports"
    reports.mkdir()
    valid = reports / "public_source_review_2026-08-25.json"
    malformed = reports / "public_source_review_zzzz.json"
    valid.write_text("{}\n", encoding="utf-8")
    malformed.write_text("{}\n", encoding="utf-8")

    assert build_public_source_review._latest_public_source_review(reports) == valid


def test_review_report_queues_sensitive_changes_without_mutating_curated_inputs(
    tmp_path: Path,
):
    paths = _inputs(tmp_path)
    before = {name: path.read_bytes() for name, path in paths.items()}

    report = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )

    assert (
        _item(
            report,
            "paired-publication:10.1234/zenodo-candidate:https://github.example/releases/v1",
        )["status"]
        == "deferred"
    )
    assert (
        _item(
            report,
            "paired-publication:10.1234/ambiguous:https://github.example/releases/v2",
        )["category"]
        == "ambiguous_doi_change"
    )
    assert (
        _item(
            report,
            "paired-publication:10.1234/rejected:https://github.example/releases/v3",
        )["status"]
        == "rejected"
    )
    assert _item(report, "doi-role:2026_Candidate")["status"] == "deferred"
    assert (
        _item(report, "doi-conflict:2026_Conflict:canonical_doi_mismatch")["status"]
        == "deferred"
    )
    assert _item(report, "repository:example/defer")["status"] == "deferred"
    assert _item(report, "repository:example/acknowledged")["status"] == "applied"
    assert _item(report, "repository:example/rejected")["status"] == "rejected"
    assert _item(report, "scholar-metrics")["status"] == "deferred"
    assert _item(report, "biographical-claim:aii-officer-roles")["status"] == "deferred"
    assert (
        _item(report, "public-source-observation:AII officers")["status"] == "deferred"
    )
    assert report["summary"]["categories"]["zenodo_candidate"]["deferred"] == 1
    assert report["summary"]["categories"]["ambiguous_doi_change"]["deferred"] == 3
    assert validate_review_report(report) == []
    assert render_json(report) == render_json(report)
    assert "## Deferred review" in render_markdown(report)
    assert before == {name: path.read_bytes() for name, path in paths.items()}


def test_durable_pair_decision_requires_the_full_candidate_fingerprint(
    tmp_path: Path,
):
    paths = _inputs(tmp_path)
    original = json.loads(paths["paired_publications_path"].read_text(encoding="utf-8"))

    for field, changed_value in (
        ("zenodo_record_url", "https://zenodo.example/changed-record"),
        ("title", "Rejected pair, revised evidence"),
    ):
        mutated = json.loads(json.dumps(original))
        action = mutated["actions"][2]
        action[field] = changed_value
        _write_json(paths["paired_publications_path"], mutated)

        report = build_review_report(
            repo_root=tmp_path,
            report_date="2026-08-25",
            source_commit="a" * 40,
            **paths,
        )

        item = _item(
            report,
            "paired-publication:10.1234/rejected:https://github.example/releases/v3",
        )
        assert item["status"] == "deferred"
        assert "no exact durable decision" in item["reason"]


def test_durable_pair_decision_can_dispose_an_exact_ambiguous_candidate(
    tmp_path: Path,
):
    paths = _inputs(tmp_path)
    paired = json.loads(paths["paired_publications_path"].read_text(encoding="utf-8"))
    action = paired["actions"][1]
    action.update(
        {
            "github_repo": "example/ambiguous",
            "zenodo_record_url": "https://zenodo.example/2",
            "release_tag": "v2",
        }
    )
    _write_json(paths["paired_publications_path"], paired)
    decisions = json.loads(paths["pair_decisions_path"].read_text(encoding="utf-8"))
    decisions["groups"].append(
        {
            "id": "R02",
            "decision": "superseded",
            "decided_by": "user",
            "decided_at": "2026-08-25T12:45:00Z",
            "doi": "10.1234/ambiguous",
            "title": "Ambiguous",
            "candidate_github_repo": "example/ambiguous",
            "representation": "version-history-only",
            "raw_candidates": [
                {
                    "doi": "10.1234/ambiguous",
                    "record_title": "Ambiguous",
                    "zenodo_record_url": "https://zenodo.example/2",
                    "github_repo": "example/ambiguous",
                    "github_release_url": "https://github.example/releases/v2",
                    "release_tag": "v2",
                }
            ],
        }
    )
    _write_json(paths["pair_decisions_path"], decisions)

    report = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )

    item = _item(
        report,
        "paired-publication:10.1234/ambiguous:https://github.example/releases/v2",
    )
    assert item["category"] == "ambiguous_doi_change"
    assert item["status"] == "applied"
    assert "durable manual pairing decision" in item["reason"]


def test_malformed_or_conflicting_pair_decisions_never_clear_public_review(
    tmp_path: Path,
):
    paths = _inputs(tmp_path)
    decisions = json.loads(paths["pair_decisions_path"].read_text(encoding="utf-8"))
    del decisions["groups"][0]["decided_by"]
    _write_json(paths["pair_decisions_path"], decisions)

    malformed = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    item = _item(
        malformed,
        "paired-publication:10.1234/rejected:https://github.example/releases/v3",
    )
    assert item["status"] == "deferred"
    assert "no exact durable decision" in item["reason"]

    # Any duplicate decision for the exact same six-field candidate is a
    # ledger-integrity error, not an invitation for last-row-wins behavior.
    decisions = json.loads(paths["pair_decisions_path"].read_text(encoding="utf-8"))
    first = decisions["groups"][0]
    first["decided_by"] = "user"
    conflicting = json.loads(json.dumps(first))
    conflicting.update(
        {
            "id": "R02",
            "decision": "accepted",
            "decided_by": "second reviewer",
            "decided_at": "2026-08-25T12:45:00Z",
        }
    )
    decisions["groups"].append(conflicting)
    _write_json(paths["pair_decisions_path"], decisions)

    try:
        build_review_report(
            repo_root=tmp_path,
            report_date="2026-08-25",
            source_commit="a" * 40,
            **paths,
        )
    except ValueError as exc:
        assert "duplicate paired-publication decisions" in str(exc)
    else:
        raise AssertionError("duplicate pair decisions were allowed to clear review")


def test_pair_decision_candidate_count_mismatch_never_clears_public_review(
    tmp_path: Path,
):
    paths = _inputs(tmp_path)
    decisions = json.loads(paths["pair_decisions_path"].read_text(encoding="utf-8"))
    decisions["groups"][0]["raw_candidate_count"] = 2
    _write_json(paths["pair_decisions_path"], decisions)

    report = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )

    item = _item(
        report,
        "paired-publication:10.1234/rejected:https://github.example/releases/v3",
    )
    assert item["status"] == "deferred"


def test_missing_or_invalid_observation_baseline_is_deferred(tmp_path: Path):
    paths = _inputs(tmp_path)
    without_previous = {
        name: path for name, path in paths.items() if name != "previous_snapshot_path"
    }

    missing = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        previous_snapshot_path=None,
        **without_previous,
    )
    item = _item(missing, "public-source-observation:baseline-unavailable")
    assert item["status"] == "deferred"
    assert item["candidate"]["current_snapshot"]["facts_valid"] is True
    assert item["candidate"]["previous_snapshot"]["available"] is False
    assert missing["summary"]["review_required"] is True

    previous = json.loads(paths["previous_snapshot_path"].read_text(encoding="utf-8"))
    previous["facts"] = []
    _write_json(paths["previous_snapshot_path"], previous)
    invalid = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    item = _item(invalid, "public-source-observation:baseline-unavailable")
    assert item["status"] == "deferred"
    assert item["candidate"]["previous_snapshot"]["available"] is True
    assert item["candidate"]["previous_snapshot"]["facts_valid"] is False


def test_sha_bound_observation_and_biographical_decisions_fail_closed_on_changed_evidence(
    tmp_path: Path,
):
    paths = _inputs(tmp_path)
    snapshot = json.loads(paths["snapshot_path"].read_text(encoding="utf-8"))
    previous = json.loads(paths["previous_snapshot_path"].read_text(encoding="utf-8"))
    claims_payload = json.loads(paths["claims_path"].read_text(encoding="utf-8"))
    officer_claim = next(
        claim
        for claim in claims_payload["claims"]
        if claim["id"] == "aii-officer-roles"
    )
    officer_evidence = {
        "claim_sources": ["https://example.test/officers"],
        "snapshot_checks": [{"url": "https://example.test/officers", "ok": True}],
        "inventory_sections": [],
    }
    observation = {
        "id": "public-source-observation:AII officers",
        "label": "AII officers",
        "previous_sha256": _json_sha256(previous["facts"]["AII officers"]),
        "current_sha256": _json_sha256(snapshot["facts"]["AII officers"]),
        "decision": "acknowledged",
        "decided_by": "user",
        "decided_at": "2026-08-25T12:30:00Z",
        "rationale": "The exact source observation was reviewed.",
        "curated_targets": [],
    }
    biographical = {
        "id": "biographical-claim:aii-officer-roles",
        "claim_id": "aii-officer-roles",
        "claim_sha256": _json_sha256(officer_claim),
        "evidence_sha256": _json_sha256(officer_evidence),
        "decision": "acknowledged",
        "decided_by": "user",
        "decided_at": "2026-08-25T12:30:00Z",
        "rationale": "The exact claim and cited evidence were reviewed.",
        "curated_targets": [],
    }
    _write_json(
        paths["observation_decisions_path"],
        {"schema_version": "1.0", "decisions": [observation]},
    )
    _write_json(
        paths["biographical_claim_decisions_path"],
        {"schema_version": "1.0", "decisions": [biographical]},
    )

    applied = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    assert (
        _item(applied, "public-source-observation:AII officers")["status"] == "applied"
    )
    assert _item(applied, "biographical-claim:aii-officer-roles")["status"] == "applied"

    snapshot["facts"]["AII officers"] = {"value": "new evidence"}
    _write_json(paths["snapshot_path"], snapshot)
    stale_observation = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    assert (
        _item(stale_observation, "public-source-observation:AII officers")["status"]
        == "deferred"
    )
    assert (
        "SHA-bound"
        in _item(stale_observation, "public-source-observation:AII officers")["reason"]
    )

    claims_payload["claims"] = [
        {**claim, "claim": "Changed officer claim"}
        if claim["id"] == "aii-officer-roles"
        else claim
        for claim in claims_payload["claims"]
    ]
    _write_json(paths["claims_path"], claims_payload)
    stale_claim = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    assert (
        _item(stale_claim, "biographical-claim:aii-officer-roles")["status"]
        == "deferred"
    )
    assert (
        "SHA-bound"
        in _item(stale_claim, "biographical-claim:aii-officer-roles")["reason"]
    )


def test_historical_observation_decision_is_ignored_until_the_label_changes_again(
    tmp_path: Path,
):
    paths = _inputs(tmp_path)
    snapshot = json.loads(paths["snapshot_path"].read_text(encoding="utf-8"))
    previous = json.loads(paths["previous_snapshot_path"].read_text(encoding="utf-8"))
    decision = {
        "id": "public-source-observation:AII officers",
        "label": "AII officers",
        "previous_sha256": _json_sha256(previous["facts"]["AII officers"]),
        "current_sha256": _json_sha256(snapshot["facts"]["AII officers"]),
        "decision": "acknowledged",
        "decided_by": "user",
        "decided_at": "2026-08-25T12:30:00Z",
        "rationale": "The initial before/after observation was reviewed.",
        "curated_targets": [],
    }
    _write_json(
        paths["observation_decisions_path"],
        {"schema_version": "1.0", "decisions": [decision]},
    )

    first = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    assert _item(first, "public-source-observation:AII officers")["status"] == "applied"

    # The next refresh uses the already-reviewed value as its baseline.  The
    # decision is historical, rather than malformed or unresolved, so this
    # later unchanged refresh must remain renderable.
    previous["facts"]["AII officers"] = snapshot["facts"]["AII officers"]
    _write_json(paths["previous_snapshot_path"], previous)
    unchanged = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    assert not any(
        item["id"] == "public-source-observation:AII officers"
        for item in unchanged["items"]
    )

    # If the label becomes active again, the old hash binding cannot clear the
    # new evidence.  It must re-enter the queue as deferred.
    snapshot["facts"]["AII officers"] = {"value": "later evidence"}
    _write_json(paths["snapshot_path"], snapshot)
    changed_again = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    item = _item(changed_again, "public-source-observation:AII officers")
    assert item["status"] == "deferred"
    assert "SHA-bound" in item["reason"]


def test_retired_observation_decision_is_preserved_as_non_actionable_history(
    tmp_path: Path,
):
    """A retired provider label must not turn a valid historic decision into an error."""
    paths = _inputs(tmp_path)
    retired_prior = {"value": "historical prior"}
    retired_current = {"value": "historical current"}
    decision = {
        "id": "public-source-observation:Retired provider endpoint",
        "label": "Retired provider endpoint",
        "previous_sha256": _json_sha256(retired_prior),
        "current_sha256": _json_sha256(retired_current),
        "decision": "acknowledged",
        "decided_by": "user",
        "decided_at": "2026-08-25T12:30:00Z",
        "rationale": "The retired endpoint was reviewed before its removal.",
        "curated_targets": [],
    }
    _write_json(
        paths["observation_decisions_path"],
        {"schema_version": "1.0", "decisions": [decision]},
    )

    report = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    item = _item(report, decision["id"])
    assert item["status"] == "applied"
    assert item["candidate"]["state"] == "historical-retired"
    assert item["candidate"]["previous_sha256"] == decision["previous_sha256"]
    assert item["candidate"]["current_sha256"] == decision["current_sha256"]
    assert "deprecated" in item["reason"]


def test_applied_strong_update_requires_exact_provenance_and_approval(
    tmp_path: Path,
):
    paths = _inputs(tmp_path)
    paired = json.loads(paths["paired_publications_path"].read_text(encoding="utf-8"))
    action = paired["actions"][0]
    action["folder"] = "2026_Candidate"
    metadata_path = tmp_path / "papers" / "2026_Candidate" / "metadata.json"
    _write_json(metadata_path, {"doi": action["doi"], "title": action["title"]})

    unapplied = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    item = _item(
        unapplied,
        "paired-publication:10.1234/zenodo-candidate:https://github.example/releases/v1",
    )
    assert item["status"] == "deferred"
    assert item["candidate"]["applied_receipt_valid"] is False

    action_sha256 = _json_sha256(action)
    paired["applied"] = [
        {
            "doi": action["doi"],
            "folder": action["folder"],
            "created": False,
            "updated_files": ["papers/2026_Candidate/metadata.json"],
            "action": action,
            "provenance": {
                "action_sha256": action_sha256,
                "metadata_path": "papers/2026_Candidate/metadata.json",
                "metadata_sha256": hashlib.sha256(metadata_path.read_bytes()).hexdigest(),
                "applied_at": "2026-08-25T12:15:00Z",
                "approval": {
                    "decision": "approved",
                    "approved_by": "sync_paired_publications --apply",
                    "approved_at": "2026-08-25T12:15:00Z",
                    "action_sha256": action_sha256,
                },
            },
        }
    ]
    _write_json(paths["paired_publications_path"], paired)

    applied = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    item = _item(
        applied,
        "paired-publication:10.1234/zenodo-candidate:https://github.example/releases/v1",
    )
    assert item["status"] == "applied"
    assert item["candidate"]["applied_receipt_valid"] is True

    paired["applied"][0]["provenance"]["approval"]["action_sha256"] = "0" * 64
    _write_json(paths["paired_publications_path"], paired)
    tampered = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    item = _item(
        tampered,
        "paired-publication:10.1234/zenodo-candidate:https://github.example/releases/v1",
    )
    assert item["status"] == "deferred"
    assert item["candidate"]["applied_receipt_valid"] is False
    assert "approval" in item["reason"]


def test_superseded_strong_receipt_is_historical_only_with_a_later_current_receipt(
    tmp_path: Path,
):
    """Older exact receipts are non-actionable only after an exact successor wins."""
    paths = _inputs(tmp_path)
    metadata_path = tmp_path / "papers" / "2026_Candidate" / "metadata.json"
    old_action = {
        "action_type": "update_existing",
        "doi": "10.1234/zenodo-candidate",
        "folder": "2026_Candidate",
        "github_repo": "example/candidate",
        "github_release_url": "https://github.example/releases/v1",
        "zenodo_record_url": "https://zenodo.example/1",
        "title": "Candidate",
        "release_tag": "v1",
        "confidence": "strong",
        "reason": "exact old pair",
    }
    current_action = {
        **old_action,
        "github_release_url": "https://github.example/releases/v2",
        "zenodo_record_url": "https://zenodo.example/2",
        "release_tag": "v2",
        "reason": "exact current pair",
    }
    _write_json(metadata_path, {"doi": old_action["doi"], "release": "v1"})
    old_metadata_sha256 = hashlib.sha256(metadata_path.read_bytes()).hexdigest()
    _write_json(metadata_path, {"doi": old_action["doi"], "release": "v2"})
    current_metadata_sha256 = hashlib.sha256(metadata_path.read_bytes()).hexdigest()

    def receipt(action: dict, metadata_sha256: str) -> dict:
        action_sha256 = _json_sha256(action)
        return {
            "doi": action["doi"],
            "folder": action["folder"],
            "created": False,
            "updated_files": ["papers/2026_Candidate/metadata.json"],
            "action": action,
            "provenance": {
                "action_sha256": action_sha256,
                "metadata_path": "papers/2026_Candidate/metadata.json",
                "metadata_sha256": metadata_sha256,
                "applied_at": "2026-08-25T12:15:00Z",
                "approval": {
                    "decision": "approved",
                    "approved_by": "sync_paired_publications --apply",
                    "approved_at": "2026-08-25T12:15:00Z",
                    "action_sha256": action_sha256,
                },
            },
        }

    _write_json(
        paths["paired_publications_path"],
        {
            "generated_at": "2026-08-25T12:00:00Z",
            "actions": [old_action, current_action],
            "applied": [
                receipt(old_action, old_metadata_sha256),
                receipt(current_action, current_metadata_sha256),
            ],
        },
    )
    report = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    old = _item(
        report,
        "paired-publication:10.1234/zenodo-candidate:https://github.example/releases/v1",
    )
    assert old["status"] == "applied"
    assert old["candidate"]["applied_receipt_valid"] is False
    assert old["candidate"]["historical_supersession_valid"] is True
    assert old["candidate"]["historical_supersession"]["state"] == "historical-superseded"
    assert (
        old["candidate"]["historical_supersession"]["superseded_by"][
            "github_release_url"
        ]
        == current_action["github_release_url"]
    )

    current = _item(
        report,
        "paired-publication:10.1234/zenodo-candidate:https://github.example/releases/v2",
    )
    assert current["status"] == "applied"
    assert current["candidate"]["applied_receipt_valid"] is True

    # A stale receipt cannot self-supersede or gain the status without the
    # later exact current action and receipt.
    paired = json.loads(paths["paired_publications_path"].read_text(encoding="utf-8"))
    paired["actions"] = [old_action]
    paired["applied"] = [receipt(old_action, old_metadata_sha256)]
    _write_json(paths["paired_publications_path"], paired)
    unresolved = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    assert (
        _item(
            unresolved,
            "paired-publication:10.1234/zenodo-candidate:https://github.example/releases/v1",
        )["status"]
        == "deferred"
    )


def test_scholar_receipt_must_be_direct_authenticated_and_still_does_not_auto_apply_difference(
    tmp_path: Path,
):
    paths = _inputs(tmp_path)
    receipt = _write_json(
        tmp_path / "reports" / "scholar-receipt.json",
        {
            "profile_id": "canonical",
            "direct": True,
            "authenticated": True,
            "verified_at": "2026-08-25T12:00:00Z",
            "metrics": {"citations": 11, "h_index": 2, "i10_index": 3},
        },
    )
    report = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        scholar_receipt_path=receipt,
        **paths,
    )
    scholar = _item(report, "scholar-metrics")
    assert scholar["candidate"]["receipt_valid"] is True
    assert scholar["status"] == "deferred"
    assert "explicit review" in scholar["reason"]

    receipt.write_text(
        json.dumps(
            {
                "profile_id": "canonical",
                "direct": True,
                "authenticated": True,
                "verified_at": "2026-08-25T12:00:00Z",
                "metrics": {"citations": 10, "h_index": 2, "i10_index": 3},
            }
        ),
        encoding="utf-8",
    )
    matching = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        scholar_receipt_path=receipt,
        **paths,
    )
    assert _item(matching, "scholar-metrics")["status"] == "applied"


def test_stale_or_failed_pairing_report_is_never_treated_as_current_candidate_set(
    tmp_path: Path,
):
    paths = _inputs(tmp_path)
    paired = json.loads(paths["paired_publications_path"].read_text(encoding="utf-8"))
    paired["generated_at"] = "2026-08-19T12:00:00Z"
    paths["paired_publications_path"].write_text(json.dumps(paired), encoding="utf-8")

    stale = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    item = _item(stale, "zenodo-refresh-incomplete")
    assert item["status"] == "deferred"
    assert item["candidate"]["refresh_state"] == "stale"
    assert not any(
        item["id"].startswith("paired-publication:") for item in stale["items"]
    )

    failed = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        pairing_refresh_status="failed",
        pairing_refresh_note="GitHub API 403/429 rate limit",
        **paths,
    )
    failed_item = _item(failed, "zenodo-refresh-incomplete")
    assert failed_item["candidate"]["refresh_state"] == "failed"
    assert failed_item["candidate"]["refresh_note"] == "GitHub API 403/429 rate limit"

    paired["generated_at"] = "2026-08-25T12:00:00Z"
    paired["warnings"] = ["HTTP 429"]
    paths["paired_publications_path"].write_text(json.dumps(paired), encoding="utf-8")
    warning_bearing = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    assert (
        _item(warning_bearing, "zenodo-refresh-incomplete")["candidate"][
            "refresh_state"
        ]
        == "failed"
    )

    # A same-day report captured before the selected source snapshot is also
    # stale. Date-only comparison would have accepted this false-green input.
    paired.pop("warnings")
    paired["generated_at"] = "2026-08-25T11:59:59Z"
    paths["paired_publications_path"].write_text(json.dumps(paired), encoding="utf-8")
    same_day_stale = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )
    assert (
        _item(same_day_stale, "zenodo-refresh-incomplete")["candidate"]["refresh_state"]
        == "stale"
    )


def test_applied_doi_receipt_requires_the_exact_approved_proposal(tmp_path: Path):
    paths = _inputs(tmp_path)
    actions = [
        {
            "folder": "2026_Candidate",
            "prior_canonical_doi": "10.1234/version",
            "canonical_doi": "10.1234/citation",
            "artifact_doi": "10.1234/version",
            "action": "set_canonical_and_preserve_prior_as_artifact",
        }
    ]
    source_sha = "1" * 64
    proposal = {
        "status": "proposed",
        "source_sha256": source_sha,
        "actions": actions,
    }
    proposal_path = (
        tmp_path / "reports" / "doi_role_reconciliation_2026-08-25.proposed.json"
    )
    _write_json(proposal_path, proposal)
    proposal_sha = hashlib.sha256(proposal_path.read_bytes()).hexdigest()
    actions_sha = hashlib.sha256(
        json.dumps(
            actions, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()
    receipt = {
        "status": "applied",
        "source_sha256": source_sha,
        "actions": actions,
        "approval": {
            "decision": "approved",
            "proposal_sha256": proposal_sha,
            "source_sha256": source_sha,
            "actions_sha256": actions_sha,
            "reviewed_by": "Review person",
            "reviewed_at": "2026-08-25T12:30:00Z",
        },
    }
    receipt_path = tmp_path / "reports" / "doi_role_reconciliation_2026-08-25.json"
    _write_json(receipt_path, receipt)
    paths["doi_review_path"] = receipt_path

    applied = build_review_report(
        repo_root=tmp_path, report_date="2026-08-25", source_commit="a" * 40, **paths
    )
    assert _item(applied, "doi-role:2026_Candidate")["status"] == "applied"

    receipt["approval"]["actions_sha256"] = "0" * 64
    _write_json(receipt_path, receipt)
    false_green = build_review_report(
        repo_root=tmp_path, report_date="2026-08-25", source_commit="a" * 40, **paths
    )
    assert _item(false_green, "doi-role:2026_Candidate")["status"] == "deferred"


def test_cli_check_is_no_write_and_detects_stale_markdown(tmp_path: Path):
    paths = _inputs(tmp_path)
    report = tmp_path / "reports" / "public_source_review_2026-08-25.json"
    args = [
        sys.executable,
        str(ORCH),
        "--date",
        "2026-08-25",
        "--report",
        str(report),
        "--snapshot",
        str(paths["snapshot_path"]),
        "--previous-snapshot",
        str(paths["previous_snapshot_path"]),
        "--inventory",
        str(paths["inventory_path"]),
        "--paired-publications",
        str(paths["paired_publications_path"]),
        "--pair-decisions",
        str(paths["pair_decisions_path"]),
        "--doi-review",
        str(paths["doi_review_path"]),
        "--repository-classification",
        str(paths["repository_classification_path"]),
        "--claims",
        str(paths["claims_path"]),
        "--observation-decisions",
        str(paths["observation_decisions_path"]),
        "--biographical-claim-decisions",
        str(paths["biographical_claim_decisions_path"]),
        "--scholar-snapshot",
        str(paths["scholar_snapshot_path"]),
    ]
    written = subprocess.run(args, cwd=REPO_ROOT, text=True, capture_output=True)
    assert written.returncode == 0, written.stderr
    before = report.read_bytes()
    checked = subprocess.run(
        [*args, "--check"], cwd=REPO_ROOT, text=True, capture_output=True
    )
    assert checked.returncode == 0, checked.stderr
    assert report.read_bytes() == before

    # Re-run without a --previous-snapshot argument. The report's recorded
    # baseline is authoritative, so a no-write check cannot silently replace
    # an issue-specific baseline with a newer daily snapshot.
    previous_index = args.index("--previous-snapshot")
    preserved_args = [*args[:previous_index], *args[previous_index + 2 :]]
    preserved = subprocess.run(
        [*preserved_args, "--check"], cwd=REPO_ROOT, text=True, capture_output=True
    )
    assert preserved.returncode == 0, preserved.stderr

    markdown = report.with_suffix(".md")
    markdown.write_text(
        markdown.read_text(encoding="utf-8") + "stale\n", encoding="utf-8"
    )
    stale = subprocess.run(
        [*preserved_args, "--check"], cwd=REPO_ROOT, text=True, capture_output=True
    )
    assert stale.returncode != 0
    assert "stale public-source review artifacts" in stale.stderr


def test_cli_exact_source_revision_mode_is_separately_checkable(tmp_path: Path):
    paths = _inputs(tmp_path)
    report = tmp_path / "reports" / "public_source_review_2026-08-25.json"
    args = [
        sys.executable,
        str(ORCH),
        "--date",
        "2026-08-25",
        "--report",
        str(report),
        "--snapshot",
        str(paths["snapshot_path"]),
        "--previous-snapshot",
        str(paths["previous_snapshot_path"]),
        "--inventory",
        str(paths["inventory_path"]),
        "--paired-publications",
        str(paths["paired_publications_path"]),
        "--pair-decisions",
        str(paths["pair_decisions_path"]),
        "--doi-review",
        str(paths["doi_review_path"]),
        "--repository-classification",
        str(paths["repository_classification_path"]),
        "--claims",
        str(paths["claims_path"]),
        "--observation-decisions",
        str(paths["observation_decisions_path"]),
        "--biographical-claim-decisions",
        str(paths["biographical_claim_decisions_path"]),
        "--scholar-snapshot",
        str(paths["scholar_snapshot_path"]),
        "--exact-source-revision",
    ]
    written = subprocess.run(args, cwd=REPO_ROOT, text=True, capture_output=True)
    assert written.returncode == 0, written.stderr
    payload = json.loads(report.read_text(encoding="utf-8"))
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert payload["source_commit"] == head
    checked = subprocess.run(
        [*args, "--check"], cwd=REPO_ROOT, text=True, capture_output=True
    )
    assert checked.returncode == 0, checked.stderr
