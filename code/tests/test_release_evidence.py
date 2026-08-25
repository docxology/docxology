"""Tests for strict report freshness and post-deploy attestation semantics."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from release_evidence import (  # noqa: E402
    RELEASE_EVIDENCE,
    collect_release_evidence,
    deployment_attestation_path,
    expected_browser_qa_names,
    expected_browser_smoke_names,
    expected_external_urls,
    expected_live_paths,
    expected_public_source_labels,
    expected_visual_targets,
    is_ephemeral_release_evidence_path,
    matches_requirement_path,
    render_attestation,
    validate_attestation,
)


COMMIT = "a" * 40
NOW = datetime(2026, 8, 25, 12, tzinfo=timezone.utc)
GENERATED = "2026-08-25T11:00:00Z"
PROVENANCE = {
    "source_worktree_clean": True,
    "source_worktree_dirty_paths": [],
    # Temporary fixtures are not Git worktrees, so the production tree-hash
    # comparison intentionally has no candidate to compare against here.
    "source_tree_sha": "unknown",
}


def _path_for(root: Path, requirement: object) -> Path:
    pattern = getattr(requirement, "pattern")
    if "browser-smoke" in pattern:
        return root / "reports/browser-smoke/2026-08-25/manifest.json"
    if "browser-qa" in pattern:
        return root / "reports/browser-qa/2026-08-25/manifest.json"
    if "visual-qa" in pattern:
        return root / "reports/visual-qa/2026-08-25/manifest.json"
    if "external_links" in pattern:
        return root / "reports/external_links_2026-08-25.json"
    if "public_source_review" in pattern:
        return root / "reports/public_source_review_2026-08-25.json"
    if "public_source" in pattern:
        return root / "reports/public_source_snapshot_2026-08-25.json"
    return root / "reports/live_site_verification_2026-08-25.json"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write_scholar_source(root: Path, *, include_receipt: bool = True) -> None:
    """Materialize a real source-and-sidecar pair for release fixtures."""
    snapshot = root / "data/scholar-snapshot.json"
    _write_json(
        snapshot,
        {
            "profile_id": "canonical",
            "citations": 10,
            "h_index": 2,
            "i10_index": 3,
            "as_of": "2026-08-25",
        },
    )
    if not include_receipt:
        return
    _write_json(
        root / "data/scholar-verification-receipt.json",
        {
            "schema_version": "1.0",
            "receipt_type": "google_scholar_direct_authenticated",
            "profile_id": "canonical",
            "direct": True,
            "authenticated": True,
            "verified_at": "2026-08-25T10:00:00Z",
            "snapshot_path": "data/scholar-snapshot.json",
            "snapshot_sha256": _sha256(snapshot),
            "snapshot_as_of": "2026-08-25",
            "metrics": {"citations": 10, "h_index": 2, "i10_index": 3},
            "source": "local release-evidence fixture",
            "method": "fixture direct authenticated verification",
        },
    )


def _common(commit: str) -> dict:
    return {"generated_at": GENERATED, "source_commit": commit, **PROVENANCE}


def _review_payload(root: Path, commit: str, snapshot_path: Path) -> dict:
    categories = (
        "zenodo_candidate",
        "ambiguous_doi_change",
        "repository_classification",
        "scholar_metric_change",
        "biographical_claim_change",
    )
    items = [
        {
            "id": f"item:{category}",
            "category": category,
            "status": "deferred" if category == "scholar_metric_change" else "applied",
        }
        for category in categories
    ]
    category_counts = {
        category: {
            "applied": 0 if category == "scholar_metric_change" else 1,
            "deferred": 1 if category == "scholar_metric_change" else 0,
            "rejected": 0,
        }
        for category in categories
    }
    return {
        "schema_version": "1.0",
        "date": "2026-08-25",
        "generated_at": "2026-08-25T00:00:00Z",
        "source_commit": commit,
        **PROVENANCE,
        "refresh_context": {"pairing_refresh_status": "auto", "pairing_refresh_note": ""},
        "inputs": {
            "public_source_snapshot": {
                "path": snapshot_path.relative_to(root).as_posix(),
                "sha256": _sha256(snapshot_path),
                "generated_at": GENERATED,
                "source_commit": commit,
            }
        },
        "items": items,
        "summary": {
            "items": len(items),
            "applied": 4,
            "deferred": 1,
            "rejected": 0,
            "review_required": True,
            "categories": category_counts,
        },
    }


def _screenshot(path: Path, label: str, root: Path) -> tuple[str, str]:
    path.write_bytes(label.encode("utf-8"))
    return path.relative_to(root).as_posix(), _sha256(path)


def _write_complete_evidence(
    root: Path, *, commit: str = COMMIT, include_scholar_receipt: bool = True
) -> None:
    _write_scholar_source(root, include_receipt=include_scholar_receipt)
    snapshot = _path_for(root, next(item for item in RELEASE_EVIDENCE if item.name == "public-source snapshot"))
    _write_json(
        snapshot,
        {
            **_common(commit),
            "checks": [{"label": label, "ok": True} for label in sorted(expected_public_source_labels())],
        },
    )

    for requirement in RELEASE_EVIDENCE:
        path = _path_for(root, requirement)
        if requirement.name == "public-source snapshot":
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        if requirement.name == "public-source review":
            payload = _review_payload(root, commit, snapshot)
        elif requirement.name == "external-link report":
            urls = sorted(expected_external_urls())
            payload = {
                **_common(commit),
                "total_unique_urls": len(urls),
                "checked_urls": len(urls),
                "ok": len(urls),
                "warnings": 0,
                "results": [{"url": url, "ok": True} for url in urls],
            }
        elif requirement.name == "browser smoke":
            checks = []
            for name in sorted(expected_browser_smoke_names()):
                screenshot, digest = _screenshot(path.parent / f"{name}.png", name, root)
                checks.append({"name": name, "ok": True, "screenshot": screenshot, "screenshot_sha256": digest})
            payload = {**_common(commit), "count": len(checks), "passing": len(checks), "checks": checks}
        elif requirement.name == "browser QA":
            checks = [{"name": name, "ok": True} for name in sorted(expected_browser_qa_names())]
            payload = {**_common(commit), "count": len(checks), "passing": len(checks), "checks": checks}
        elif requirement.name == "visual QA":
            screenshots = []
            for index, (page, viewport, size) in enumerate(sorted(expected_visual_targets())):
                screenshot, digest = _screenshot(path.parent / f"shot-{index}.png", f"{page}|{viewport}|{size}", root)
                screenshots.append({"page": page, "viewport": viewport, "size": size, "file": screenshot, "sha256": digest})
            payload = {
                **_common(commit),
                "screenshots": screenshots,
                "review": {"status": "reviewed", "reviewed_by": "Release reviewer", "reviewed_at": "2026-08-25T11:30:00Z"},
            }
        else:
            payload = {
                **_common(commit),
                "overall_ok": True,
                "github_pages": {"status": "built"},
                "deployment": {"head_sha": commit},
                "results": [{"path": route, "ok": True} for route in sorted(expected_live_paths())],
            }
        _write_json(path, payload)


def test_collect_release_evidence_accepts_complete_successful_exact_revision(tmp_path):
    _write_complete_evidence(tmp_path)
    receipts, errors = collect_release_evidence(tmp_path, COMMIT, max_age_days=30, now=NOW)
    assert errors == []
    assert {receipt.name for receipt in receipts} == {requirement.name for requirement in RELEASE_EVIDENCE}
    # A deferred public refresh is not a curated metric change.  The valid
    # source-bound baseline receipt therefore permits release evidence.
    review = _path_for(tmp_path, next(item for item in RELEASE_EVIDENCE if item.name == "public-source review"))
    scholar_item = next(
        item
        for item in json.loads(review.read_text(encoding="utf-8"))["items"]
        if item["category"] == "scholar_metric_change"
    )
    assert scholar_item["status"] == "deferred"


def test_collect_release_evidence_rejects_missing_scholar_source_receipt(tmp_path):
    _write_complete_evidence(tmp_path, include_scholar_receipt=False)

    _receipts, errors = collect_release_evidence(tmp_path, COMMIT, max_age_days=30, now=NOW)

    assert any("missing direct authenticated Scholar verification receipt" in error for error in errors)


def test_collect_release_evidence_rejects_tampered_scholar_snapshot(tmp_path):
    _write_complete_evidence(tmp_path)
    snapshot = tmp_path / "data/scholar-snapshot.json"
    payload = json.loads(snapshot.read_text(encoding="utf-8"))
    payload["citations"] = 11
    _write_json(snapshot, payload)

    _receipts, errors = collect_release_evidence(tmp_path, COMMIT, max_age_days=30, now=NOW)

    assert any("snapshot_sha256 does not match" in error for error in errors)
    assert any("metrics do not match" in error for error in errors)


def test_collect_release_evidence_rejects_tampered_scholar_receipt_binding(tmp_path):
    _write_complete_evidence(tmp_path)
    receipt = tmp_path / "data/scholar-verification-receipt.json"
    payload = json.loads(receipt.read_text(encoding="utf-8"))
    payload["snapshot_sha256"] = "0" * 64
    _write_json(receipt, payload)

    _receipts, errors = collect_release_evidence(tmp_path, COMMIT, max_age_days=30, now=NOW)

    assert any("snapshot_sha256 does not match" in error for error in errors)


def test_collect_release_evidence_rejects_non_direct_scholar_source_receipt(tmp_path):
    _write_complete_evidence(tmp_path)
    receipt = tmp_path / "data/scholar-verification-receipt.json"
    payload = json.loads(receipt.read_text(encoding="utf-8"))
    payload["direct"] = False
    _write_json(receipt, payload)

    _receipts, errors = collect_release_evidence(tmp_path, COMMIT, max_age_days=30, now=NOW)

    assert any("direct=true and authenticated=true" in error for error in errors)


def test_collect_release_evidence_rejects_stale_wrong_revision_and_failed_report(tmp_path):
    _write_complete_evidence(tmp_path, commit="b" * 40)
    stale = _path_for(tmp_path, RELEASE_EVIDENCE[0])
    payload = json.loads(stale.read_text(encoding="utf-8"))
    payload["generated_at"] = "2026-06-01T00:00:00Z"
    _write_json(stale, payload)
    smoke = _path_for(tmp_path, next(item for item in RELEASE_EVIDENCE if item.name == "browser smoke"))
    smoke_payload = json.loads(smoke.read_text(encoding="utf-8"))
    smoke_payload["checks"][0]["ok"] = False
    _write_json(smoke, smoke_payload)

    _receipts, errors = collect_release_evidence(tmp_path, COMMIT, max_age_days=30, now=NOW)
    assert any("stale public-source snapshot" in error for error in errors)
    assert any("source_commit" in error for error in errors)
    assert any("browser smoke failed semantic validation" in error for error in errors)


def test_collect_release_evidence_rejects_a_control_tail_review_for_deployed_sha(tmp_path):
    """The normal review anchor cannot stand in for post-deploy exact evidence."""
    _write_complete_evidence(tmp_path)
    review = _path_for(tmp_path, next(item for item in RELEASE_EVIDENCE if item.name == "public-source review"))
    payload = json.loads(review.read_text(encoding="utf-8"))
    payload["source_commit"] = "b" * 40
    _write_json(review, payload)

    _receipts, errors = collect_release_evidence(tmp_path, COMMIT, max_age_days=30, now=NOW)
    assert any(
        "public-source review source_commit " + "b" * 40 + " != release commit " + COMMIT in error
        for error in errors
    )


def test_collect_release_evidence_rejects_external_screenshot_symlink_and_unreviewed_visuals(tmp_path):
    _write_complete_evidence(tmp_path)
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"not evidence")
    smoke = _path_for(tmp_path, next(item for item in RELEASE_EVIDENCE if item.name == "browser smoke"))
    smoke_payload = json.loads(smoke.read_text(encoding="utf-8"))
    linked = smoke.parent / "linked.png"
    linked.symlink_to(outside)
    smoke_payload["checks"][0]["screenshot"] = linked.relative_to(tmp_path).as_posix()
    smoke_payload["checks"][0]["screenshot_sha256"] = _sha256(outside)
    _write_json(smoke, smoke_payload)
    visual = _path_for(tmp_path, next(item for item in RELEASE_EVIDENCE if item.name == "visual QA"))
    visual_payload = json.loads(visual.read_text(encoding="utf-8"))
    visual_payload["review"]["status"] = "pending"
    _write_json(visual, visual_payload)

    _receipts, errors = collect_release_evidence(tmp_path, COMMIT, max_age_days=30, now=NOW)
    assert any("symlinked release evidence" in error for error in errors)
    assert any("visual QA has not recorded an explicit review" in error for error in errors)


def test_collect_release_evidence_rejects_hard_linked_screenshot(tmp_path):
    _write_complete_evidence(tmp_path)
    outside = tmp_path / "outside.png"
    outside.write_bytes(b"not evidence")
    smoke = _path_for(tmp_path, next(item for item in RELEASE_EVIDENCE if item.name == "browser smoke"))
    smoke_payload = json.loads(smoke.read_text(encoding="utf-8"))
    linked = smoke.parent / "linked.png"
    linked.hardlink_to(outside)
    smoke_payload["checks"][0]["screenshot"] = linked.relative_to(tmp_path).as_posix()
    smoke_payload["checks"][0]["screenshot_sha256"] = _sha256(outside)
    _write_json(smoke, smoke_payload)

    _receipts, errors = collect_release_evidence(tmp_path, COMMIT, max_age_days=30, now=NOW)
    assert any("hard-linked release evidence" in error for error in errors)


def test_collect_release_evidence_rejects_partial_coverage_and_dirty_capture(tmp_path):
    _write_complete_evidence(tmp_path)
    snapshot = _path_for(tmp_path, next(item for item in RELEASE_EVIDENCE if item.name == "public-source snapshot"))
    payload = json.loads(snapshot.read_text(encoding="utf-8"))
    payload["checks"].pop()
    payload["source_worktree_clean"] = False
    _write_json(snapshot, payload)

    _receipts, errors = collect_release_evidence(tmp_path, COMMIT, max_age_days=30, now=NOW)
    assert any("clean source worktree" in error for error in errors)
    assert any("coverage does not match" in error for error in errors)


def test_attestation_requires_canonical_path_and_detects_report_mutation(tmp_path):
    _write_complete_evidence(tmp_path)
    receipts, errors = collect_release_evidence(tmp_path, COMMIT, max_age_days=30, now=NOW)
    assert errors == []
    attestation = deployment_attestation_path(tmp_path, COMMIT)
    _write_json(attestation, render_attestation(COMMIT, receipts, attested_at="2026-08-25T11:30:00Z"))
    assert validate_attestation(tmp_path, attestation, COMMIT, max_age_days=30, now=NOW) == []
    assert validate_attestation(tmp_path, tmp_path / "attestation.json", COMMIT, max_age_days=30, now=NOW) == [
        "deployment attestation must use the canonical path reports/deployment-attestations/" + COMMIT + ".json for its deployment SHA"
    ]

    changed = _path_for(tmp_path, next(item for item in RELEASE_EVIDENCE if item.name == "external-link report"))
    changed.write_text(changed.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    errors = validate_attestation(tmp_path, attestation, COMMIT, max_age_days=30, now=NOW)
    assert any("changed after attestation" in error for error in errors)


def test_only_post_commit_release_receipts_are_worktree_exempt():
    assert is_ephemeral_release_evidence_path("reports/browser-smoke/2026-08-25/home.png")
    assert is_ephemeral_release_evidence_path("reports/public_source_review_2026-08-25.md")
    assert is_ephemeral_release_evidence_path("reports/deployment-attestations/" + "a" * 40 + ".json")
    assert not is_ephemeral_release_evidence_path("reports/browser-smoke/notdate/source.py")
    assert not is_ephemeral_release_evidence_path("reports/browser-qa/evil/source.py")
    assert not is_ephemeral_release_evidence_path("reports\\browser-smoke\\2026-08-25\\home.png")
    assert not is_ephemeral_release_evidence_path("data/claims.json")


def test_attested_requirement_paths_are_root_anchored():
    requirement = next(item for item in RELEASE_EVIDENCE if item.name == "external-link report")
    assert matches_requirement_path("reports/external_links_2026-08-25.json", requirement)
    assert not matches_requirement_path(
        "untrusted/reports/external_links_2026-08-25.json", requirement
    )
