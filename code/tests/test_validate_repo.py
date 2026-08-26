"""Tests for validate_repo report artifact gating."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import validate_repo as vr  # noqa: E402
import generate_citation_cff as cff  # noqa: E402
from report_paths import source_worktree_state  # noqa: E402


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


def _fixture_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "candidate-repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "Release fixture")
    return repo


def test_validation_scope_excludes_dependency_and_cache_trees_but_keeps_docs():
    assert not vr.is_validation_source_path(
        Path(".venv/lib/python3.12/site-packages/package/diagnostic.html")
    )
    assert not vr.is_validation_source_path(Path("node_modules/package/README.md"))
    assert vr.is_validation_source_path(Path("docs/operations/release-integrity.md"))


def test_release_commit_must_match_candidate_head():
    assert vr.release_commit_errors("a" * 40, "a" * 40) == []
    assert vr.release_commit_errors("a" * 40, "b" * 40) == [
        "--release-commit must resolve to the current HEAD; validate another SHA from a checkout at that exact commit"
    ]


def test_public_source_review_provenance_mode_matches_validation_tier():
    assert vr.public_source_review_check_args(release=False) == [
        "python3",
        "code/orchestrators/build_public_source_review.py",
        "--check",
    ]
    assert vr.public_source_review_check_args(release=True) == [
        "python3",
        "code/orchestrators/build_public_source_review.py",
        "--check",
        "--exact-source-revision",
    ]


def test_live_site_check_mode_matches_validation_tier():
    assert vr.live_site_check_args(release=False) == [
        "python3",
        "code/orchestrators/verify_live_site.py",
        "--check",
        "--allow-source-count-drift",
    ]
    assert vr.live_site_check_args(release=True) == [
        "python3",
        "code/orchestrators/verify_live_site.py",
        "--check",
    ]


def test_release_worktree_rejects_unrecognized_changes_but_allows_declared_receipts(tmp_path: Path):
    repo = _fixture_repo(tmp_path)
    (repo / "source.txt").write_text("committed\n", encoding="utf-8")
    _git(repo, "add", "source.txt")
    _git(repo, "commit", "-qm", "fixture")

    reports = repo / "reports"
    reports.mkdir()
    (reports / "external_links_2026-08-25.json").write_text("{}\n", encoding="utf-8")
    assert vr._release_worktree_errors(repo) == []

    (repo / "README.md").write_text("unrecognized source change\n", encoding="utf-8")
    errors = vr._release_worktree_errors(repo)
    assert errors == ["release source worktree is not clean: README.md"]


def test_all_declared_postdeploy_receipts_are_clean_but_unknown_report_is_source_drift(tmp_path: Path):
    repo = _fixture_repo(tmp_path)
    (repo / "source.txt").write_text("committed\n", encoding="utf-8")
    _git(repo, "add", "source.txt")
    _git(repo, "commit", "-qm", "fixture")

    evidence_paths = [
        "reports/public_source_snapshot_2026-08-26.json",
        "reports/public_source_review_2026-08-26.json",
        "reports/public_source_review_2026-08-26.md",
        "reports/external_links_2026-08-26.json",
        "reports/external_links_triage_2026-08-26.json",
        "reports/external_links_triage_2026-08-26.md",
        "reports/browser-smoke/2026-08-26/manifest.json",
        "reports/browser-smoke/2026-08-26/home.png",
        "reports/browser-qa/2026-08-26/manifest.json",
        "reports/visual-qa/2026-08-26/manifest.json",
        "reports/visual-qa/2026-08-26/home.png",
        "reports/live_site_verification_2026-08-26.json",
        "reports/deployment-attestations/" + "a" * 40 + ".json",
    ]
    for relative in evidence_paths:
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("receipt\n", encoding="utf-8")

    assert source_worktree_state(repo)["source_worktree_clean"] is True
    assert vr._release_worktree_errors(repo) == []

    unknown = repo / "reports" / "external_links_triage_2026-08-26.txt"
    unknown.write_text("unrecognized evidence\n", encoding="utf-8")
    state = source_worktree_state(repo)
    assert state["source_worktree_clean"] is False
    assert state["source_worktree_dirty_paths"] == [
        "reports/external_links_triage_2026-08-26.txt"
    ]
    assert vr._release_worktree_errors(repo) == [
        "release source worktree is not clean: reports/external_links_triage_2026-08-26.txt"
    ]


def test_isolated_candidate_validation_reads_committed_source_not_fresh_receipts(tmp_path: Path):
    """A real detached worktree must see HEAD, including same-path report bytes."""
    repo = _fixture_repo(tmp_path)
    report = repo / "reports" / "external_links_2026-08-25.json"
    report.parent.mkdir()
    (repo / "source.txt").write_text("committed source\n", encoding="utf-8")
    report.write_text("committed receipt\n", encoding="utf-8")
    (repo / "verify_candidate.py").write_text(
        "from pathlib import Path\n"
        "import subprocess\n"
        "assert Path('source.txt').read_text(encoding='utf-8') == 'committed source\\n'\n"
        "assert Path('reports/external_links_2026-08-25.json').read_text(encoding='utf-8') == 'committed receipt\\n'\n"
        "assert sorted(Path('reports').glob('external_links_*.json'))[-1].name == 'external_links_2026-08-25.json'\n"
        "assert not Path('reports/browser-smoke/2026-08-26/manifest.json').exists()\n"
        "assert subprocess.run(['git', 'status', '--porcelain'], check=True, capture_output=True, text=True).stdout == ''\n",
        encoding="utf-8",
    )
    _git(repo, "add", "source.txt", "reports", "verify_candidate.py")
    _git(repo, "commit", "-qm", "candidate")
    commit = _git(repo, "rev-parse", "HEAD").strip()

    # The report has the same pathname as its committed baseline, while a
    # newer raw report and browser receipt are fresh untracked post-deploy
    # artifacts. A normal latest-report reader must still see the committed
    # baseline in the detached candidate worktree.
    report.write_text("fresh receipt\n", encoding="utf-8")
    (repo / "reports" / "external_links_2026-08-26.json").write_text(
        "newer fresh receipt\n", encoding="utf-8"
    )
    fresh_browser = repo / "reports" / "browser-smoke" / "2026-08-26" / "manifest.json"
    fresh_browser.parent.mkdir(parents=True)
    fresh_browser.write_text("{}\n", encoding="utf-8")

    vr.run_isolated_candidate_validation(
        commit,
        repo_root=repo,
        validator_command=(sys.executable, "verify_candidate.py"),
    )

    assert report.read_text(encoding="utf-8") == "fresh receipt\n"
    assert fresh_browser.exists()
    assert _git(repo, "worktree", "list", "--porcelain").count("worktree ") == 1


def test_iter_local_links_ignores_fenced_markdown_examples():
    text = """See [real link](pages/README.md).

```markdown
![Example figure](../output/figures/example.png){#fig:example}
<a href="missing-example.html">example</a>
```
"""

    links = vr.iter_local_links(text)

    assert links == ["pages/README.md"]


def _validate_json_files_in_empty_repo(tmp_path: Path, *, strict_reports: bool) -> None:
    vr.validate_json_files(
        strict_reports,
        repo_root=tmp_path,
        required_json_files=[],
        optional_report_patterns=[("accessibility_static_*.json", "accessibility static checks")],
    )


def test_validate_json_files_default_warns_on_missing_optional_artifacts(tmp_path: Path, capsys):
    _validate_json_files_in_empty_repo(tmp_path, strict_reports=False)
    output = capsys.readouterr().out

    assert "optional artifact warnings:" in output
    assert "Optional accessibility static checks report missing: accessibility_static_*.json" in output


def test_validate_json_files_strict_enforces_optional_artifacts(tmp_path: Path):
    with pytest.raises(SystemExit):
        _validate_json_files_in_empty_repo(tmp_path, strict_reports=True)


def test_validate_json_files_warns_on_optional_invalid_json(tmp_path: Path):
    (tmp_path / "reports").mkdir()
    invalid = tmp_path / "reports" / "accessibility_static_2026-06-16.json"
    invalid.write_text("{not valid json", encoding="utf-8")

    with pytest.raises(SystemExit):
        _validate_json_files_in_empty_repo(tmp_path, strict_reports=True)

    _validate_json_files_in_empty_repo(tmp_path, strict_reports=False)


def test_paper_cff_validation_rejects_stale_doi_roles_and_accepts_rendered_output(
    tmp_path: Path,
):
    paper = tmp_path / "papers" / "2026_Example"
    paper.mkdir(parents=True)
    metadata = {
        "title": "Example work",
        "publication_date": "2026-08-26",
        "doi": "10.5281/zenodo.100",
        "artifact_doi": "10.5281/zenodo.101",
        "creators": [{"name": "Friedman, Daniel Ari"}],
    }
    (paper / "metadata.json").write_text(json.dumps(metadata) + "\n", encoding="utf-8")
    cff_path = paper / "CITATION.cff"
    cff_path.write_text(
        "cff-version: 1.2.0\n"
        "title: \"Example work\"\n"
        "date-released: 2026-08-26\n"
        "doi: 10.5281/zenodo.101\n"
        "url: \"https://doi.org/10.5281/zenodo.101\"\n",
        encoding="utf-8",
    )

    with pytest.raises(SystemExit, match="Paper CITATION.cff DOI-role drift"):
        vr.validate_paper_citation_cff(tmp_path)

    cff_path.write_text(
        cff.render_outputs(tmp_path / "papers")[cff_path], encoding="utf-8"
    )
    vr.validate_paper_citation_cff(tmp_path)
