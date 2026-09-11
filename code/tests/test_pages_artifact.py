"""Tests for the bounded GitHub Pages publication projection."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import build_pages_artifact as bpa  # noqa: E402

sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import report_references  # noqa: E402


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


def test_pages_manifest_allows_only_the_current_dirty_prepayload_source_snapshot(tmp_path):
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "test@example.invalid")
    _git(tmp_path, "config", "user.name", "Pages fixture")
    report = tmp_path / "reports" / "public_source_snapshot_2026-08-25.json"
    report.parent.mkdir()
    report.write_text("{}\n", encoding="utf-8")
    _git(tmp_path, "add", "reports")
    _git(tmp_path, "commit", "-qm", "receipt baseline")
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=tmp_path, check=True, capture_output=True, text=True
    ).stdout.strip()
    report.write_text(
        json.dumps({"source_commit": head, "source_worktree_clean": False}) + "\n",
        encoding="utf-8",
    )

    assert bpa.dirty_postdeploy_payload_paths(tmp_path) == [report.relative_to(tmp_path)]
    assert bpa.dirty_postdeploy_payload_paths(
        tmp_path, allow_dirty_prepayload_source_snapshot=True
    ) == []
    bpa.require_clean_postdeploy_payload_inputs(
        tmp_path, allow_dirty_prepayload_source_snapshot=True
    )

    report.write_text(
        json.dumps({"source_commit": head, "source_worktree_clean": True}) + "\n",
        encoding="utf-8",
    )
    assert bpa.dirty_postdeploy_payload_paths(
        tmp_path, allow_dirty_prepayload_source_snapshot=True
    ) == [report.relative_to(tmp_path)]


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


def _init_pages_fixture(repo: Path) -> None:
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "Pages fixture")


def test_dated_report_family_extraction_takes_the_first_date():
    """The FIRST _YYYY-MM-DD occurrence delimits the family and its date."""
    assert bpa._dated_report_family_date("paired_publications_2026-06-09-itrace.json") == (
        "paired_publications",
        date(2026, 6, 9),
    )
    assert bpa._dated_report_family_date("public_source_review_2026-08-25.proposed.json") == (
        "public_source_review",
        date(2026, 8, 25),
    )
    assert bpa._dated_report_family_date("asset_size_2026-07-22.json") == (
        "asset_size",
        date(2026, 7, 22),
    )


def test_dated_report_family_extraction_rejects_non_family_shapes():
    assert bpa._dated_report_family_date("current_counts.md") is None
    assert bpa._dated_report_family_date("_2026-08-25.json") is None
    assert bpa._dated_report_family_date("asset_size_2026-99-99.json") is None
    assert bpa._dated_report_family_date("seo-discoverability-audit-2026-06-10.md") is None
    assert bpa._dated_report_family_date("paired_publications_review_queue") is None


def test_superseded_rule_keeps_only_strictly_older_family_dates():
    paths = [
        Path("reports/asset_size_2026-09-10.json"),
        Path("reports/asset_size_2026-09-11.json"),
        Path("reports/private_public_reconciliation_2026-08-25.md"),
        Path("reports/doi_role_reconciliation_2026-08-25.json"),
        Path("reports/doi_role_reconciliation_2026-08-25.proposed.json"),
        Path("reports/paired_publications_2026-06-09-itrace.json"),
        Path("reports/paired_publications_2026-06-09.json"),
        Path("reports/paired_publications_2026-09-10.json"),
        Path("reports/README.md"),
        Path("pages/index.html"),
    ]
    superseded = bpa.superseded_dated_report_paths(paths)
    assert Path("reports/asset_size_2026-09-10.json") in superseded
    assert Path("reports/asset_size_2026-09-11.json") not in superseded
    # Same-date multi-file sets stay together.
    assert Path("reports/doi_role_reconciliation_2026-08-25.proposed.json") not in superseded
    assert Path("reports/doi_role_reconciliation_2026-08-25.json") not in superseded
    assert Path("reports/private_public_reconciliation_2026-08-25.md") not in superseded
    # The itrace qualifier shares the plain file's family date; both drop together.
    assert Path("reports/paired_publications_2026-06-09.json") in superseded
    assert Path("reports/paired_publications_2026-06-09-itrace.json") in superseded
    # Undated reports and non-reports paths are never members of a family.
    assert Path("reports/README.md") not in superseded
    assert Path("pages/index.html") not in superseded


def test_superseded_rule_omits_whole_older_dated_screenshot_dirs():
    paths = [
        Path("reports/browser-qa/2026-09-07/manifest.json"),
        Path("reports/browser-qa/2026-09-11/manifest.json"),
        Path("reports/browser-qa/2026-09-07/AGENTS.md"),
        Path("reports/visual-qa/2026-08-26/home.png"),
        Path("reports/visual-qa/2026-09-11/home.png"),
        Path("reports/other/2026-09-07/manifest.json"),
        Path("untrusted/reports/browser-qa/2026-09-07/manifest.json"),
    ]
    superseded = bpa.superseded_dated_report_paths(paths)
    assert Path("reports/browser-qa/2026-09-07/manifest.json") in superseded
    assert Path("reports/browser-qa/2026-09-07/AGENTS.md") in superseded
    assert Path("reports/visual-qa/2026-08-26/home.png") in superseded
    assert Path("reports/browser-qa/2026-09-11/manifest.json") not in superseded
    assert Path("reports/visual-qa/2026-09-11/home.png") not in superseded
    # Non-SCREENSHOT_PARENTS dated dirs and nested untrusted paths are untouched.
    assert Path("reports/other/2026-09-07/manifest.json") not in superseded
    assert Path("untrusted/reports/browser-qa/2026-09-07/manifest.json") not in superseded


def test_cited_by_protection_uses_dated_set_granularity():
    paths = [
        Path("reports/asset_size_2026-09-10.json"),
        Path("reports/asset_size_2026-09-11.json"),
        Path("reports/browser-qa/2026-09-07/manifest.json"),
        Path("reports/browser-qa/2026-09-07/AGENTS.md"),
        Path("reports/browser-qa/2026-09-11/manifest.json"),
    ]
    assert bpa.superseded_dated_report_paths(paths) == {
        Path("reports/asset_size_2026-09-10.json"),
        Path("reports/browser-qa/2026-09-07/manifest.json"),
        Path("reports/browser-qa/2026-09-07/AGENTS.md"),
    }
    # A citation naming the older receipt itself protects exactly that file.
    cited = bpa.superseded_dated_report_paths(
        paths, referenced_paths={"reports/asset_size_2026-09-10.json"}
    )
    assert Path("reports/asset_size_2026-09-10.json") not in cited
    # Citing any member file or the bare dated dir protects the whole set.
    cited_set = bpa.superseded_dated_report_paths(
        paths, referenced_paths={"reports/browser-qa/2026-09-07/manifest.json"}
    )
    assert Path("reports/browser-qa/2026-09-07/AGENTS.md") not in cited_set
    cited_bare_dir = bpa.superseded_dated_report_paths(
        paths, referenced_paths={"reports/browser-qa/2026-09-07"}
    )
    assert Path("reports/browser-qa/2026-09-07/AGENTS.md") not in cited_bare_dir
    # A family-level token names no dated set and protects nothing.
    family_token = bpa.superseded_dated_report_paths(
        paths, referenced_paths={"reports/browser-qa", "reports/asset_size"}
    )
    assert family_token == {
        Path("reports/asset_size_2026-09-10.json"),
        Path("reports/browser-qa/2026-09-07/manifest.json"),
        Path("reports/browser-qa/2026-09-07/AGENTS.md"),
    }


def test_control_receipts_follow_the_same_superseded_rule():
    paths = [
        Path("reports/asset_size_2026-09-10.json"),
        Path("reports/asset_size_2026-09-11.json"),
        Path("reports/pages_artifact_growth_2026-09-10.json"),
        Path("reports/pages_artifact_growth_2026-09-11.json"),
        Path("reports/public_source_review_2026-09-10.json"),
        Path("reports/public_source_review_2026-09-11.md"),
    ]
    superseded = bpa.superseded_dated_report_paths(paths)
    assert Path("reports/asset_size_2026-09-10.json") in superseded
    assert Path("reports/pages_artifact_growth_2026-09-10.json") in superseded
    assert Path("reports/public_source_review_2026-09-10.json") in superseded
    assert Path("reports/public_source_review_2026-09-11.md") not in superseded


def test_referenced_report_scan_covers_projected_surfaces_only(tmp_path: Path):
    _init_pages_fixture(tmp_path)
    (tmp_path / "reports").mkdir()
    (tmp_path / "code").mkdir()
    (tmp_path / "data").mkdir()
    (tmp_path / "pages").mkdir()
    (tmp_path / "papers" / "2026_Example").mkdir(parents=True)
    (tmp_path / "_site").mkdir()
    target = "reports/asset_size_2026-09-10.json"
    citing_reports = tmp_path / "reports" / "self.json"
    citing_inventory = tmp_path / "data" / "pages-artifact-manifest.json"
    citing_retention = tmp_path / "data" / "report-retention.json"
    for source in (citing_reports, citing_inventory, citing_retention):
        source.write_text(json.dumps({"cites": target}), encoding="utf-8")
    (tmp_path / "_site" / "echo.html").write_text(f"<a>{target}</a>", encoding="utf-8")
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "fixture")

    assert target not in report_references.referenced_report_paths(tmp_path)

    (tmp_path / "pages" / "index.md").write_text(f"[a]({target})", encoding="utf-8")
    assert target in report_references.referenced_report_paths(tmp_path)

    (tmp_path / "pages" / "index.md").unlink()
    (tmp_path / "data" / "agent-index.json").write_text(
        json.dumps({"cites": target}), encoding="utf-8"
    )
    assert target in report_references.referenced_report_paths(tmp_path)

    (tmp_path / "data" / "agent-index.json").unlink()
    (tmp_path / "papers" / "2026_Example" / "metadata.json").write_text(
        json.dumps({"evidence": target}), encoding="utf-8"
    )
    assert target in report_references.referenced_report_paths(tmp_path)

    (tmp_path / "papers" / "2026_Example" / "metadata.json").unlink()
    (tmp_path / "notes.md").write_text(f"see {target} for provenance", encoding="utf-8")
    # Untracked working-tree files are caught by the fallback scan.
    assert target in report_references.referenced_report_paths(tmp_path)

    # Code fallback literals never protect (untracked on purpose here).
    (tmp_path / "code" / "fallback.py").write_text(f'"{target}"', encoding="utf-8")
    (tmp_path / "notes.md").unlink()
    assert target not in report_references.referenced_report_paths(tmp_path)


def test_superseded_rule_with_the_shared_citation_scan(tmp_path: Path):
    _init_pages_fixture(tmp_path)
    (tmp_path / "reports").mkdir()
    (tmp_path / "pages").mkdir()
    (tmp_path / "reports" / "asset_size_2026-09-10.json").write_text("{}", encoding="utf-8")
    (tmp_path / "reports" / "asset_size_2026-09-11.json").write_text("{}", encoding="utf-8")
    (tmp_path / "pages" / "index.md").write_text(
        "[evidence](reports/asset_size_2026-09-10.json)", encoding="utf-8"
    )
    _git(tmp_path, "add", "-A")
    _git(tmp_path, "commit", "-qm", "fixture")
    tracked = [
        Path(raw)
        for raw in subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=tmp_path,
            check=True,
            capture_output=True,
        )
        .stdout.decode()
        .split("\0")
        if raw
    ]
    assert bpa.superseded_dated_report_paths(tracked) == {
        Path("reports/asset_size_2026-09-10.json")
    }
    protected = bpa.superseded_dated_report_paths(
        tracked, referenced_paths=report_references.referenced_report_paths(tmp_path)
    )
    assert protected == set()


def test_manifest_comparison_fields_cover_the_superseded_class():
    assert "omitted_superseded_reports" in bpa.MANIFEST_COMPARISON_FIELDS
    expected = {field: {} for field in bpa.MANIFEST_COMPARISON_FIELDS}
    stale = {**expected, "omitted_superseded_reports": {"count": 0}}
    assert bpa.manifest_drift_fields(stale, expected) == ["omitted_superseded_reports"]


def test_growth_receipt_counts_the_superseded_class():
    payload = {
        "generated_at": "2026-09-11T00:00:00Z",
        "source_commit_at_generation": "source-commit",
        "budget": {"artifact_file_count": 10, "artifact_bytes": 2048},
        "omitted_paper_images": {"count": 2},
        "omitted_visual_qa_screenshots": {"count": 3, "bytes": 30},
        "omitted_superseded_reports": {"count": 7, "bytes": 70},
    }
    growth = bpa._growth_report_payload(payload)
    assert growth["omitted_superseded_report_count"] == 7
    assert growth["omitted_superseded_report_bytes"] == 70


def test_dangling_report_reference_guard(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    output = tmp_path / "_site"
    (output / "pages").mkdir(parents=True)
    (output / "reports" / "visual-qa" / "2026-09-11").mkdir(parents=True)
    # A referenced receipt that was copied resolves.
    (output / "reports" / "asset_size_2026-09-11.json").write_text("{}", encoding="utf-8")
    (output / "pages" / "index.html").write_text(
        '<a href="reports/asset_size_2026-09-11.json">latest</a>', encoding="utf-8"
    )
    # GitHub raw/tree fallback URLs are not local references.
    (output / "pages" / "fallback.html").write_text(
        '<img src="https://raw.githubusercontent.com/docxology/docxology/abc/reports/asset_size_2026-09-10.json">'
        ' and <a href="//raw.githubusercontent.com/docxology/docxology/abc/reports/x_2026-01-01.json">',
        encoding="utf-8",
    )
    # A visual-QA screenshot binary is intentionally served from the Git commit.
    (output / "pages" / "manifest.html").write_text(
        '<img src="reports/visual-qa/2026-08-26/home.png">', encoding="utf-8"
    )
    # References from the scan's excluded source scopes are ignored.
    (output / "reports" / "README.md").write_text("see reports/asset_size_2026-09-10.json", encoding="utf-8")
    (output / "data").mkdir()
    (output / "data" / "pages-artifact-manifest.json").write_text(
        json.dumps({"path": "reports/asset_size_2026-09-10.json"}), encoding="utf-8"
    )
    # A reference to a path that no longer exists in the repository is
    # pre-existing provenance drift, not an omission this policy created.
    (output / "pages" / "history.html").write_text(
        '<a href="reports/visual-qa/2026-07-18/manifest.json">pruned</a>', encoding="utf-8"
    )
    monkeypatch.setattr(bpa, "REPO_ROOT", tmp_path / "repo")
    assert bpa.dangling_report_references(output) == []

    # A repository path that exists but was not copied into the projection is a
    # shipped 404 and must fail the build.
    repo = tmp_path / "repo"
    (repo / "reports").mkdir(parents=True)
    (repo / "reports" / "asset_size_2026-09-10.json").write_text("{}", encoding="utf-8")
    (output / "pages" / "dangling.html").write_text(
        '<a href="reports/asset_size_2026-09-10.json">superseded</a>', encoding="utf-8"
    )
    assert bpa.dangling_report_references(output) == ["reports/asset_size_2026-09-10.json"]

    # A bare dated-directory reference resolves when the kept dir was copied.
    (output / "pages" / "dangling.html").unlink()
    (output / "reports" / "browser-qa" / "2026-09-11").mkdir(parents=True)
    (output / "pages" / "dir.html").write_text(
        '<a href="reports/browser-qa/2026-09-11/">set</a>'
        '<a href="reports/browser-qa">family</a>',
        encoding="utf-8",
    )
    assert bpa.dangling_report_references(output) == []
