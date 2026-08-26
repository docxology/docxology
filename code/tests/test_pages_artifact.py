"""Tests for the bounded GitHub Pages publication projection."""

from __future__ import annotations

import sys
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import build_pages_artifact as bpa  # noqa: E402


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


def test_paper_extracted_binary_images_are_omitted_from_pages():
    assert not bpa.is_published_path(Path("papers/2026_Example/images/page1_img1.png"))
    assert not bpa.is_published_path(Path("papers/2026_Example/images/page1_img1.jpeg"))


def test_dated_visual_qa_screenshot_binaries_are_omitted_but_manifests_remain_public():
    assert bpa.is_published_path(Path("reports/browser-smoke/2026-08-25/home.png"))
    assert not bpa.is_published_path(Path("reports/visual-qa/2026-08-25/home-desktop.webp"))
    assert bpa.is_published_path(Path("reports/browser-smoke/2026-08-25/manifest.json"))
    assert bpa.is_published_path(Path("reports/visual-qa/2026-08-25/manifest.json"))


def test_visual_qa_screenshot_exclusion_cannot_match_a_nested_untrusted_path():
    nested = Path("untrusted/reports/visual-qa/2026-08-25/home-desktop.png")
    assert not bpa.is_visual_qa_screenshot(nested)
    assert bpa.is_published_path(nested)


def test_artwork_and_public_site_images_are_retained():
    assert bpa.is_published_path(Path("art/42_drawing.jpg"))
    assert bpa.is_published_path(Path("og-image.jpg"))
    assert bpa.is_published_path(Path("papers/2026_Example/figure.jpg"))


def test_source_and_local_only_tooling_are_separated():
    assert bpa.is_published_path(Path("code/orchestrators/build_pages_artifact.py"))
    assert not bpa.is_published_path(Path(".github/workflows/pages.yml"))
    assert bpa.is_published_path(Path("data/agent-index.json"))
    assert bpa.is_published_path(Path("resume/resume.pdf"))


def test_control_manifests_have_public_fallback_policy():
    assert Path("GENERATED.md") in bpa.CONTROL_FILES
    assert Path("data/pages-artifact-manifest.json") in bpa.CONTROL_FILES
    assert Path("data/release-integrity.json") in bpa.CONTROL_FILES


def test_all_dated_artifact_control_reports_are_control_metadata():
    assert bpa.is_control_path(Path("reports/asset_size_2026-07-22.json"))
    assert bpa.is_control_path(Path("reports/pages_artifact_growth_2026-07-22.json"))
    assert bpa.is_control_path(Path("reports/pages_artifact_growth_2026-07-24.json"))
    assert bpa.is_control_path(Path("reports/public_source_review_2026-08-25.json"))
    assert bpa.is_control_path(Path("reports/public_source_review_2026-08-25.md"))


def test_only_top_level_growth_reports_are_control_metadata():
    """A payload cannot hide behind Path.match's suffix matching behavior."""
    assert not bpa.is_control_path(Path("untrusted/reports/asset_size_2026-08-25.json"))
    assert not bpa.is_control_path(
        Path("untrusted/reports/pages_artifact_growth_2026-08-25.json")
    )
    assert not bpa.is_control_path(
        Path("untrusted/reports/public_source_review_2026-08-25.json")
    )
    assert not bpa.is_control_path(Path("reports/public_source_review_evil.json"))
    assert not bpa.is_control_path(Path("reports/public_source_review_2026-99-99.json"))
    assert not bpa.is_control_path(Path("reports/public_source_review_2026-08-25.proposed.json"))
    assert not bpa.is_control_path(Path(r"reports\\public_source_review_2026-08-25.json"))


def test_pages_input_symlinks_fail_closed(tmp_path):
    outside = tmp_path.parent / "outside-pages-input.txt"
    outside.write_text("private", encoding="utf-8")
    link = tmp_path / "published.txt"
    link.symlink_to(outside)

    with pytest.raises(SystemExit, match="symlinked Pages input"):
        bpa.source_path(Path("published.txt"), repo_root=tmp_path)


def test_pages_input_hard_links_fail_closed(tmp_path):
    source = tmp_path / "source.txt"
    source.write_text("shared", encoding="utf-8")
    linked = tmp_path / "published.txt"
    linked.hardlink_to(source)

    with pytest.raises(SystemExit, match="hard-linked Pages input"):
        bpa.source_path(Path("published.txt"), repo_root=tmp_path)


def test_pages_manifest_rejects_dirty_postdeploy_receipts(tmp_path):
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "test@example.invalid")
    _git(tmp_path, "config", "user.name", "Pages fixture")
    report = tmp_path / "reports" / "external_links_2026-08-25.json"
    control = tmp_path / "reports" / "public_source_review_2026-08-25.json"
    report.parent.mkdir()
    report.write_text("committed\n", encoding="utf-8")
    control.write_text("committed\n", encoding="utf-8")
    _git(tmp_path, "add", "reports")
    _git(tmp_path, "commit", "-qm", "receipt baseline")
    report.write_text("fresh evidence\n", encoding="utf-8")
    control.write_text("control tail\n", encoding="utf-8")

    assert bpa.dirty_postdeploy_payload_paths(tmp_path) == [
        Path("reports/external_links_2026-08-25.json")
    ]
    with pytest.raises(SystemExit, match="regenerate the Pages control tail in a clean worktree"):
        bpa.require_clean_postdeploy_payload_inputs(tmp_path)


def test_growth_report_contract_is_compared_by_manifest_validation():
    expected = {field: {} for field in bpa.MANIFEST_COMPARISON_FIELDS}
    expected["growth_report"] = "reports/pages_artifact_growth_2026-08-25.json"
    stale = {**expected, "growth_report": "reports/pages_artifact_growth_2026-08-24.json"}

    assert bpa.manifest_drift_fields(stale, expected) == ["growth_report"]


def test_manifest_check_preserves_recorded_growth_receipt_after_utc_rollover():
    """A day change alone must not make unchanged Pages source look stale."""
    current_growth_report = bpa.REPO_ROOT / "reports" / "pages_artifact_growth_2026-08-26.json"
    existing = {"growth_report": "reports/pages_artifact_growth_2026-08-25.json"}

    assert bpa._growth_report_for_manifest(
        existing,
        include_pending_growth=False,
        current_growth_report=current_growth_report,
    ) == Path("reports/pages_artifact_growth_2026-08-25.json")


def test_manifest_check_requires_current_receipt_when_one_exists():
    """A same-day write remains detectable instead of being silently ignored."""
    current_growth_report = bpa.REPO_ROOT / "reports" / "pages_artifact_growth_2026-08-26.json"
    existing = {"growth_report": "reports/pages_artifact_growth_2026-08-25.json"}

    assert bpa._growth_report_for_manifest(
        existing,
        include_pending_growth=True,
        current_growth_report=current_growth_report,
    ) == Path("reports/pages_artifact_growth_2026-08-26.json")


def test_manifest_check_rejects_malformed_recorded_growth_receipt():
    current_growth_report = bpa.REPO_ROOT / "reports" / "pages_artifact_growth_2026-08-26.json"

    assert bpa._growth_report_for_manifest(
        {"growth_report": "reports/../../outside.json"},
        include_pending_growth=False,
        current_growth_report=current_growth_report,
    ) == Path("reports/pages_artifact_growth_2026-08-26.json")


def test_source_revision_allows_a_trailing_control_only_commit() -> None:
    """The final manifest commit is intentionally not a self-referential source SHA."""
    parents = {"controls": "payload", "payload": "base"}
    changes = {
        "controls": [
            Path("data/pages-artifact-manifest.json"),
            Path("data/release-integrity.json"),
            Path("reports/asset_size_2026-08-25.json"),
            Path("reports/pages_artifact_growth_2026-08-25.json"),
            Path("reports/public_source_review_2026-08-25.json"),
            Path("reports/public_source_review_2026-08-25.md"),
        ],
        "payload": [Path("pages/BIBLIOGRAPHY.md")],
    }

    assert bpa._latest_payload_commit(
        "controls", parents.get, changes.__getitem__
    ) == "payload"


def test_manifest_drift_includes_stale_source_commit() -> None:
    """A hand-edited/old source SHA must no longer produce a false-green check."""
    expected = {
        "schema_version": "1.0",
        "source_commit_at_generation": "current-source-commit",
        "canonical_origin": "https://danielarifriedman.com/",
        "github_fallback": {},
        "policy": {},
        "budget": {},
        "included_files": [],
        "control_files": [],
        "omitted_paper_images": {},
        "omitted_visual_qa_screenshots": {},
    }
    stale = {**expected, "source_commit_at_generation": "stale-source-commit"}
    assert bpa.manifest_drift_fields(stale, expected) == ["source_commit_at_generation"]
