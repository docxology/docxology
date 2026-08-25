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
                    "github_release_url": "https://github.example/releases/v3",
                    "title": "Rejected pair",
                },
            ]
        },
    )
    decisions = _write_json(
        data / "paired-publication-decisions.json",
        {
            "groups": [
                {
                    "decision": "rejected",
                    "doi": "10.1234/rejected",
                    "raw_candidates": ["https://github.example/releases/v3"],
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
            "conflicts": [{"folder": "2026_Conflict", "code": "canonical_doi_mismatch"}],
        },
    )
    classifications = _write_json(
        data / "repository-classification.json",
        {
            "repositories": [
                {"full_name": "example/defer", "review_status": "defer", "catalog_role": "not_curated"},
                {
                    "full_name": "example/acknowledged",
                    "review_status": "acknowledged",
                    "catalog_role": "acknowledged_not_curated",
                },
                {"full_name": "example/rejected", "review_status": "rejected", "catalog_role": "not_curated"},
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
    }


def _item(report: dict, identifier: str) -> dict:
    return next(item for item in report["items"] if item["id"] == identifier)


def test_review_report_queues_sensitive_changes_without_mutating_curated_inputs(tmp_path: Path):
    paths = _inputs(tmp_path)
    before = {name: path.read_bytes() for name, path in paths.items()}

    report = build_review_report(
        repo_root=tmp_path,
        report_date="2026-08-25",
        source_commit="a" * 40,
        **paths,
    )

    assert _item(report, "paired-publication:10.1234/zenodo-candidate:https://github.example/releases/v1")["status"] == "deferred"
    assert _item(report, "paired-publication:10.1234/ambiguous:https://github.example/releases/v2")["category"] == "ambiguous_doi_change"
    assert _item(report, "paired-publication:10.1234/rejected:https://github.example/releases/v3")["status"] == "rejected"
    assert _item(report, "doi-role:2026_Candidate")["status"] == "deferred"
    assert _item(report, "doi-conflict:2026_Conflict:canonical_doi_mismatch")["status"] == "deferred"
    assert _item(report, "repository:example/defer")["status"] == "deferred"
    assert _item(report, "repository:example/acknowledged")["status"] == "applied"
    assert _item(report, "repository:example/rejected")["status"] == "rejected"
    assert _item(report, "scholar-metrics")["status"] == "deferred"
    assert _item(report, "biographical-claim:aii-officer-roles")["status"] == "deferred"
    assert _item(report, "public-source-observation:AII officers")["status"] == "deferred"
    assert report["summary"]["categories"]["zenodo_candidate"]["deferred"] == 1
    assert report["summary"]["categories"]["ambiguous_doi_change"]["deferred"] == 3
    assert validate_review_report(report) == []
    assert render_json(report) == render_json(report)
    assert "## Deferred review" in render_markdown(report)
    assert before == {name: path.read_bytes() for name, path in paths.items()}


def test_scholar_receipt_must_be_direct_authenticated_and_still_does_not_auto_apply_difference(tmp_path: Path):
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


def test_stale_or_failed_pairing_report_is_never_treated_as_current_candidate_set(tmp_path: Path):
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
    assert not any(item["id"].startswith("paired-publication:") for item in stale["items"])

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
    assert _item(warning_bearing, "zenodo-refresh-incomplete")["candidate"]["refresh_state"] == "failed"

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
    assert _item(same_day_stale, "zenodo-refresh-incomplete")["candidate"]["refresh_state"] == "stale"


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
    proposal_path = tmp_path / "reports" / "doi_role_reconciliation_2026-08-25.proposed.json"
    _write_json(proposal_path, proposal)
    proposal_sha = hashlib.sha256(proposal_path.read_bytes()).hexdigest()
    actions_sha = hashlib.sha256(
        json.dumps(actions, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
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

    applied = build_review_report(repo_root=tmp_path, report_date="2026-08-25", source_commit="a" * 40, **paths)
    assert _item(applied, "doi-role:2026_Candidate")["status"] == "applied"

    receipt["approval"]["actions_sha256"] = "0" * 64
    _write_json(receipt_path, receipt)
    false_green = build_review_report(repo_root=tmp_path, report_date="2026-08-25", source_commit="a" * 40, **paths)
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
        "--scholar-snapshot",
        str(paths["scholar_snapshot_path"]),
    ]
    written = subprocess.run(args, cwd=REPO_ROOT, text=True, capture_output=True)
    assert written.returncode == 0, written.stderr
    before = report.read_bytes()
    checked = subprocess.run([*args, "--check"], cwd=REPO_ROOT, text=True, capture_output=True)
    assert checked.returncode == 0, checked.stderr
    assert report.read_bytes() == before

    # Re-run without a --previous-snapshot argument. The report's recorded
    # baseline is authoritative, so a no-write check cannot silently replace
    # an issue-specific baseline with a newer daily snapshot.
    previous_index = args.index("--previous-snapshot")
    preserved_args = [*args[:previous_index], *args[previous_index + 2 :]]
    preserved = subprocess.run([*preserved_args, "--check"], cwd=REPO_ROOT, text=True, capture_output=True)
    assert preserved.returncode == 0, preserved.stderr

    markdown = report.with_suffix(".md")
    markdown.write_text(markdown.read_text(encoding="utf-8") + "stale\n", encoding="utf-8")
    stale = subprocess.run([*preserved_args, "--check"], cwd=REPO_ROOT, text=True, capture_output=True)
    assert stale.returncode != 0
    assert "stale public-source review artifacts" in stale.stderr
