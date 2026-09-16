"""Content-lineage receipt bindings for the post-deploy attestation layer.

DOC-002: every evidence receipt records its own capture-time HEAD, so it can
never strictly bind the later commit that lands it.  The attestation layer
therefore accepts ancestor-bound receipts for ephemeral tool evidence when
they are byte-identical, same-day, and lineally related, while strict
repository validation keeps demanding the exact release commit.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools.release_evidence import (  # noqa: E402
    BINDING_MODE_CONTENT_LINEAGE,
    BINDING_MODE_STRICT,
    EvidenceReceipt,
    _review_snapshot_binding_errors,
    collect_release_evidence,
    deployment_attestation_path,
    expected_external_urls,
    receipt_binds_expected_commit,
    validate_attestation,
)

GENERATED = "2026-08-25T11:00:00Z"
SAME_DAY = datetime(2026, 8, 25, 18, tzinfo=timezone.utc)
NEXT_DAY = datetime(2026, 8, 26, 9, tzinfo=timezone.utc)
REPORT_PATH = "reports/external_links_2026-08-25.json"
SNAPSHOT_PATH = "reports/public_source_snapshot_2026-08-25.json"
REVIEW_PATH = "reports/public_source_review_2026-08-25.json"
HAND_AUTHORED_PATH = "reports/manual_review_2026-08-25.json"


def _git(repo: Path, *args: str) -> str:
    """Run one real Git fixture command and return its stdout."""
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def _fixture_repo(tmp_path: Path) -> tuple[Path, str, str]:
    """Create a repo with a capture commit and the later commit landing it.

    Returns ``(repo, capture_commit, landing_commit)``: the capture commit is
    the parent of the landing commit, mirroring the DOC-002 mechanics where a
    receipt records its own capture-time HEAD and lands in a descendant.
    """
    repo = tmp_path / "binding-repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "Binding fixture")
    (repo / "source.txt").write_text("payload\n", encoding="utf-8")
    _git(repo, "add", "source.txt")
    _git(repo, "commit", "-qm", "capture")
    capture = _git(repo, "rev-parse", "HEAD").strip()
    reports = repo / "reports"
    reports.mkdir()
    (reports / "receipts.txt").write_text("landed receipts\n", encoding="utf-8")
    _git(repo, "add", "reports")
    _git(repo, "commit", "-qm", "land receipts")
    landing = _git(repo, "rev-parse", "HEAD").strip()
    return repo, capture, landing


def _bind(
    repo: Path,
    path: str,
    *,
    expected: str,
    source: str,
    context: datetime,
    mode: str,
    recorded: str,
    current: str,
) -> bool:
    return receipt_binds_expected_commit(
        repo,
        path,
        expected_commit=expected,
        source_commit=source,
        generated_at=GENERATED,
        context=context,
        binding_mode=mode,
        recorded_sha256=recorded,
        current_sha256=current,
    )


def test_content_lineage_accepts_ancestor_same_day_byte_identical_receipt(tmp_path):
    repo, capture, landing = _fixture_repo(tmp_path)
    digest = hashlib.sha256(b"receipt bytes\n").hexdigest()
    assert _bind(
        repo,
        REPORT_PATH,
        expected=landing,
        source=capture,
        context=SAME_DAY,
        mode=BINDING_MODE_CONTENT_LINEAGE,
        recorded=digest,
        current=digest,
    )


def test_content_lineage_rejects_receipt_captured_on_a_different_calendar_day(tmp_path):
    repo, capture, landing = _fixture_repo(tmp_path)
    digest = hashlib.sha256(b"receipt bytes\n").hexdigest()
    assert not _bind(
        repo,
        REPORT_PATH,
        expected=landing,
        source=capture,
        context=NEXT_DAY,
        mode=BINDING_MODE_CONTENT_LINEAGE,
        recorded=digest,
        current=digest,
    )


def test_content_lineage_rejects_a_capture_commit_that_is_not_an_ancestor(tmp_path):
    repo, capture, landing = _fixture_repo(tmp_path)
    digest = hashlib.sha256(b"receipt bytes\n").hexdigest()
    lineage_kwargs = {
        "context": SAME_DAY,
        "mode": BINDING_MODE_CONTENT_LINEAGE,
        "recorded": digest,
        "current": digest,
    }
    # The landing commit is a descendant of the capture commit, so a receipt
    # recorded at the landing commit claiming the capture commit is forgery.
    assert not _bind(repo, REPORT_PATH, expected=capture, source=landing, **lineage_kwargs)
    # An unverifiable commit provides no lineage proof either.
    assert not _bind(repo, REPORT_PATH, expected=landing, source="f" * 40, **lineage_kwargs)


def test_content_lineage_rejects_drifted_receipt_bytes(tmp_path):
    repo, capture, landing = _fixture_repo(tmp_path)
    recorded = hashlib.sha256(b"receipt bytes\n").hexdigest()
    current = hashlib.sha256(b"edited receipt bytes\n").hexdigest()
    assert not _bind(
        repo,
        REPORT_PATH,
        expected=landing,
        source=capture,
        context=SAME_DAY,
        mode=BINDING_MODE_CONTENT_LINEAGE,
        recorded=recorded,
        current=current,
    )


def test_content_lineage_keeps_hand_authored_receipts_strict(tmp_path):
    repo, capture, landing = _fixture_repo(tmp_path)
    digest = hashlib.sha256(b"hand authored\n").hexdigest()
    assert not _bind(
        repo,
        HAND_AUTHORED_PATH,
        expected=landing,
        source=capture,
        context=SAME_DAY,
        mode=BINDING_MODE_CONTENT_LINEAGE,
        recorded=digest,
        current=digest,
    )


def test_strict_binding_mode_ignores_content_lineage_entirely(tmp_path):
    repo, capture, landing = _fixture_repo(tmp_path)
    digest = hashlib.sha256(b"receipt bytes\n").hexdigest()
    assert not _bind(
        repo,
        REPORT_PATH,
        expected=landing,
        source=capture,
        context=SAME_DAY,
        mode=BINDING_MODE_STRICT,
        recorded=digest,
        current=digest,
    )
    assert _bind(
        repo,
        REPORT_PATH,
        expected=landing,
        source=landing,
        context=SAME_DAY,
        mode=BINDING_MODE_STRICT,
        recorded=digest,
        current=digest,
    )


def _write_external_links_report(repo: Path, *, source_commit: str, source_tree_sha: str) -> Path:
    urls = sorted(expected_external_urls())
    path = repo / REPORT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "generated_at": GENERATED,
                "source_commit": source_commit,
                "source_worktree_clean": True,
                "source_worktree_dirty_paths": [],
                "source_tree_sha": source_tree_sha,
                "total_unique_urls": len(urls),
                "checked_urls": len(urls),
                "ok": len(urls),
                "warnings": 0,
                "results": [{"url": url, "ok": True} for url in urls],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_collect_release_evidence_default_is_strict_and_lineage_mode_clears_it(tmp_path):
    repo, capture, landing = _fixture_repo(tmp_path)
    capture_tree = _git(repo, "rev-parse", f"{capture}^{{tree}}").strip()
    _write_external_links_report(repo, source_commit=capture, source_tree_sha=capture_tree)

    default_errors = collect_release_evidence(repo, landing, max_age_days=30, now=SAME_DAY)[1]
    assert any(
        f"external-link report source_commit {capture} != release commit {landing}" in error
        for error in default_errors
    )
    assert any(
        "external-link report source_tree_sha does not match the release commit" in error
        for error in default_errors
    )

    lineage_errors = collect_release_evidence(
        repo,
        landing,
        max_age_days=30,
        now=SAME_DAY,
        binding_mode=BINDING_MODE_CONTENT_LINEAGE,
    )[1]
    assert not any("external-link report source_commit" in error for error in lineage_errors)
    assert not any("external-link report source_tree_sha" in error for error in lineage_errors)
    # Other required families are still missing in this single-report fixture.
    assert any("missing browser smoke" in error for error in lineage_errors)


def test_attestation_layer_accepts_lineage_binding_and_fails_closed_on_drift(tmp_path):
    repo, capture, landing = _fixture_repo(tmp_path)
    capture_tree = _git(repo, "rev-parse", f"{capture}^{{tree}}").strip()
    report = _write_external_links_report(repo, source_commit=capture, source_tree_sha=capture_tree)
    attestation = deployment_attestation_path(repo, landing)
    attestation.parent.mkdir(parents=True, exist_ok=True)
    attestation.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "attested_at": "2026-08-25T12:00:00Z",
                "deployment_sha": landing,
                "evidence": [
                    {
                        "name": "external-link report",
                        "path": REPORT_PATH,
                        "generated_at": GENERATED,
                        "source_commit": capture,
                        "sha256": hashlib.sha256(report.read_bytes()).hexdigest(),
                    }
                ],
                "result": "passed",
                "note": "fixture attestation",
            }
        ),
        encoding="utf-8",
    )
    lineage_kwargs = {
        "max_age_days": 30,
        "now": SAME_DAY,
        "binding_mode": BINDING_MODE_CONTENT_LINEAGE,
    }

    # The strict default (the validate_repo --release signature) still rejects
    # the intact ancestor-bound attestation.
    strict_errors = validate_attestation(repo, attestation, landing, max_age_days=30, now=SAME_DAY)
    assert any("not bound to release commit" in error for error in strict_errors)

    # Content-lineage accepts the same intact attestation; other families are
    # still missing from this single-entry fixture.
    lineage_errors = validate_attestation(repo, attestation, landing, **lineage_kwargs)
    assert not any("not bound to release commit" in error for error in lineage_errors)
    assert any("deployment attestation lacks browser smoke" in error for error in lineage_errors)

    # Byte drift after attestation voids the content-identity condition.
    original = report.read_bytes()
    report.write_bytes(original + b"\n")
    drift_errors = validate_attestation(repo, attestation, landing, **lineage_kwargs)
    assert any("changed after attestation" in error for error in drift_errors)
    assert any("not bound to release commit" in error for error in drift_errors)
    report.write_bytes(original)

    # A capture on a different calendar day than the attestation is stale lineage.
    payload = json.loads(attestation.read_text(encoding="utf-8"))
    payload["attested_at"] = "2026-08-26T09:00:00Z"
    attestation.write_text(json.dumps(payload), encoding="utf-8")
    late_errors = validate_attestation(
        repo,
        attestation,
        landing,
        max_age_days=30,
        now=NEXT_DAY,
        binding_mode=BINDING_MODE_CONTENT_LINEAGE,
    )
    assert any("not bound to release commit" in error for error in late_errors)


def test_review_provenance_may_name_only_the_content_bound_snapshot(tmp_path):
    repo, capture, landing = _fixture_repo(tmp_path)
    snapshot_digest = "b" * 64
    review = repo / REVIEW_PATH
    review.parent.mkdir(parents=True, exist_ok=True)
    review.write_text(
        json.dumps(
            {
                "inputs": {
                    "public_source_snapshot": {
                        "path": SNAPSHOT_PATH,
                        "sha256": snapshot_digest,
                        "generated_at": GENERATED,
                        "source_commit": capture,
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    receipts = [
        EvidenceReceipt(
            "public-source snapshot", SNAPSHOT_PATH, GENERATED, capture, snapshot_digest
        ),
        EvidenceReceipt(
            "public-source review", REVIEW_PATH, GENERATED, capture, "d" * 64
        ),
    ]
    assert (
        _review_snapshot_binding_errors(
            repo, receipts, landing, binding_mode=BINDING_MODE_CONTENT_LINEAGE
        )
        == []
    )
    # The strict default still rejects the ancestor-bound provenance.
    assert (
        "public-source review public-source snapshot provenance is not bound to the release commit"
        in _review_snapshot_binding_errors(repo, receipts, landing)
    )
    # The provenance may not name a commit the accepted snapshot does not carry.
    forged = [
        EvidenceReceipt(
            "public-source snapshot", SNAPSHOT_PATH, GENERATED, "9" * 40, snapshot_digest
        ),
        receipts[1],
    ]
    errors = _review_snapshot_binding_errors(
        repo, forged, landing, binding_mode=BINDING_MODE_CONTENT_LINEAGE
    )
    assert (
        "public-source review public-source snapshot provenance is not bound to the release commit"
        in errors
    )
