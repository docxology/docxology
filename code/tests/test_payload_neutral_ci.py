"""CI-configuration commits leave the payload anchor in place.

A Dependabot action bump changes only ``.github/workflows/*.yml``. Those files
never reach the Pages projection, so a commit touching only them must not move
``source_commit_at_generation`` (which would stale every committed control
record and fail the PR's validate job). The guards below pin the premise: no
generator declares or hashes a payload-neutral file, and the report-citation
scan that decides which superseded reports ship never reads ``.github``.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

REPO_ROOT = Path(__file__).resolve().parents[2]

from docxology_tools import release_controls, report_references  # noqa: E402
from docxology_tools.generation_plan import LOCAL_GENERATION_STEPS, effective_step_inputs  # noqa: E402
from docxology_tools.release_controls import (  # noqa: E402
    is_control_path,
    is_payload_neutral_path,
    latest_payload_commit,
    source_payload_commit,
)

import build_pages_artifact as bpa  # noqa: E402


@pytest.mark.parametrize(
    "path",
    [
        ".github/workflows/pages.yml",
        ".github/workflows/browser-qa.yml",
        ".github/workflows/release.yaml",
        ".github/dependabot.yml",
    ],
)
def test_ci_configuration_is_payload_neutral(path: str):
    assert is_payload_neutral_path(Path(path))
    # Neutral is not control: settle still lands these files as payload.
    assert not is_control_path(Path(path))


@pytest.mark.parametrize(
    "path",
    [
        ".github/README.md",  # generated output
        ".github/AGENTS.md",
        ".github/workflows/README.md",
        ".github/workflows/AGENTS.md",
        ".github/workflows/nested/pages.yml",
        ".github/workflows/.hidden.yml",
        ".github/ISSUE_TEMPLATE/config.yml",
        ".github/dependabot.yaml",
        "untrusted/.github/workflows/pages.yml",
        "docs/.github/workflows/pages.yml",
        "pages.yml",
        "data/pages-artifact-manifest.yml",
    ],
)
def test_only_exact_ci_configuration_is_payload_neutral(path: str):
    assert not is_payload_neutral_path(Path(path))


def _walk(head: str, history: dict[str, tuple[str | None, list[str]]]) -> str:
    return latest_payload_commit(
        head,
        lambda c: history[c][0],
        lambda c: [Path(p) for p in history[c][1]],
    )


def test_walk_skips_workflow_only_commits_after_a_control_tail():
    history = {
        "bump2": ("bump1", [".github/workflows/pages.yml"]),
        "bump1": ("tail", [".github/workflows/browser-qa.yml", ".github/dependabot.yml"]),
        "tail": ("payload", ["data/pages-artifact-manifest.json", "reports/asset_size_2026-10-07.json"]),
        "payload": ("root", ["pages/BIBLIOGRAPHY.md"]),
        "root": (None, ["README.md"]),
    }
    assert _walk("bump2", history) == "payload"


def test_mixed_control_and_workflow_commit_is_skipped():
    history = {
        "mixed": ("payload", ["data/pages-artifact-manifest.json", ".github/workflows/pages.yml"]),
        "payload": (None, ["pages/BIBLIOGRAPHY.md"]),
    }
    assert _walk("mixed", history) == "payload"


def test_mixed_workflow_and_payload_commit_is_payload():
    history = {
        "mixed": ("payload", [".github/workflows/pages.yml", "README.md"]),
        "payload": (None, ["pages/BIBLIOGRAPHY.md"]),
    }
    assert _walk("mixed", history) == "mixed"


def test_generated_github_readme_commit_is_payload():
    history = {
        "readme": ("payload", [".github/README.md", ".github/workflows/pages.yml"]),
        "payload": (None, ["pages/BIBLIOGRAPHY.md"]),
    }
    assert _walk("readme", history) == "readme"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def _commit(repo: Path, files: dict[str, str], message: str) -> str:
    for relative, text in files.items():
        target = repo / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        _git(repo, "add", relative)
    _git(repo, "commit", "-qm", message)
    return _git(repo, "rev-parse", "HEAD")


def _init(repo: Path) -> None:
    _git(repo, "init", "-q", "--initial-branch=main")
    _git(repo, "config", "user.email", "test@example.invalid")
    _git(repo, "config", "user.name", "Test")


def test_dependabot_bump_on_main_keeps_payload_anchor(tmp_path: Path):
    """End-to-end: payload, control tail, then a direct workflow bump."""
    _init(tmp_path)
    payload = _commit(tmp_path, {"pages/BIBLIOGRAPHY.md": "payload\n"}, "payload")
    _commit(tmp_path, {"data/pages-artifact-manifest.json": "{}\n"}, "payload (control tail)")
    _commit(tmp_path, {".github/workflows/pages.yml": "uses: actions/upload-artifact@v7\n"}, "bump")
    assert source_payload_commit(tmp_path) == payload


def test_dependabot_pr_merge_ref_keeps_base_payload_anchor(tmp_path: Path):
    """End-to-end: a PR-shaped merge ref of a workflow-only branch."""
    _init(tmp_path)
    payload = _commit(tmp_path, {"pages/BIBLIOGRAPHY.md": "payload\n"}, "payload")
    _commit(tmp_path, {"data/pages-artifact-manifest.json": "{}\n"}, "payload (control tail)")
    _git(tmp_path, "checkout", "-qb", "dependabot/github_actions/bump")
    _commit(tmp_path, {".github/workflows/pages.yml": "uses: actions/upload-artifact@v7\n"}, "bump")
    _git(tmp_path, "checkout", "-q", "main")
    _git(tmp_path, "merge", "--no-ff", "-q", "-m", "merge bump", "dependabot/github_actions/bump")
    assert source_payload_commit(tmp_path) == payload


def test_workflow_branch_merged_onto_an_advanced_base_keeps_main_payload_anchor(tmp_path: Path):
    """A merge commit whose tree matches no parent is judged by its first-parent diff."""
    _init(tmp_path)
    _commit(tmp_path, {"pages/BIBLIOGRAPHY.md": "payload\n"}, "payload")
    _commit(tmp_path, {"data/pages-artifact-manifest.json": "{}\n"}, "payload (control tail)")
    _git(tmp_path, "checkout", "-qb", "dependabot/github_actions/bump")
    _commit(tmp_path, {".github/workflows/pages.yml": "uses: actions/upload-artifact@v7\n"}, "bump")
    _git(tmp_path, "checkout", "-q", "main")
    advanced = _commit(tmp_path, {"pages/SOFTWARE.md": "later payload\n"}, "later payload")
    _commit(tmp_path, {"data/pages-artifact-manifest.json": "{\"v\": 2}\n"}, "later payload (control tail)")
    _git(tmp_path, "merge", "--no-ff", "-q", "-m", "merge bump", "dependabot/github_actions/bump")
    assert source_payload_commit(tmp_path) == advanced


def test_content_branch_merged_onto_an_advanced_base_is_payload(tmp_path: Path):
    _init(tmp_path)
    _commit(tmp_path, {"pages/BIBLIOGRAPHY.md": "payload\n"}, "payload")
    _git(tmp_path, "checkout", "-qb", "feature")
    _commit(tmp_path, {"README.md": "feature\n", ".github/workflows/pages.yml": "x: 1\n"}, "feature")
    _git(tmp_path, "checkout", "-q", "main")
    _commit(tmp_path, {"pages/SOFTWARE.md": "later payload\n"}, "later payload")
    _git(tmp_path, "merge", "--no-ff", "-q", "-m", "merge feature", "feature")
    assert source_payload_commit(tmp_path) == _git(tmp_path, "rev-parse", "HEAD")


def _workflow_pr_behind_an_advanced_main(repo: Path) -> str:
    """A workflow-only PR cut before main gained a payload commit and its tail; returns that payload."""
    _init(repo)
    _commit(repo, {"pages/BIBLIOGRAPHY.md": "payload\n"}, "payload")
    _commit(repo, {"data/pages-artifact-manifest.json": "{}\n"}, "payload (control tail)")
    _git(repo, "checkout", "-qb", "dependabot/github_actions/bump")
    _commit(repo, {".github/workflows/pages.yml": "uses: actions/upload-artifact@v7\n"}, "bump")
    _git(repo, "checkout", "-q", "main")
    advanced = _commit(repo, {"pages/SOFTWARE.md": "later payload\n"}, "later payload")
    _commit(repo, {"data/pages-artifact-manifest.json": "{\"v\": 2}\n"}, "later payload (control tail)")
    return advanced


def test_update_branch_merge_on_a_workflow_pr_keeps_base_payload_anchor(tmp_path: Path):
    """GitHub's "Update branch" merges main into the PR with the PR branch as first parent."""
    advanced = _workflow_pr_behind_an_advanced_main(tmp_path)
    _git(tmp_path, "checkout", "-q", "dependabot/github_actions/bump")
    _git(tmp_path, "merge", "--no-ff", "-q", "-m", "Merge branch 'main' into bump", "main")
    assert source_payload_commit(tmp_path) == advanced


def test_merge_commit_landing_of_an_updated_workflow_pr_keeps_payload_anchor(tmp_path: Path):
    advanced = _workflow_pr_behind_an_advanced_main(tmp_path)
    _git(tmp_path, "checkout", "-q", "dependabot/github_actions/bump")
    _git(tmp_path, "merge", "--no-ff", "-q", "-m", "Merge branch 'main' into bump", "main")
    _git(tmp_path, "checkout", "-q", "main")
    _git(tmp_path, "merge", "--no-ff", "-q", "-m", "Merge pull request", "dependabot/github_actions/bump")
    assert source_payload_commit(tmp_path) == advanced


def test_merge_ref_of_a_branch_with_payload_resolves_the_branch_payload(tmp_path: Path):
    """The merge's first-parent diff carries the branch payload, so only merge awareness resolves it."""
    _init(tmp_path)
    _commit(tmp_path, {"pages/BIBLIOGRAPHY.md": "payload\n"}, "payload")
    _commit(tmp_path, {"data/pages-artifact-manifest.json": "{}\n"}, "payload (control tail)")
    _git(tmp_path, "checkout", "-qb", "feature")
    branch_payload = _commit(tmp_path, {"pages/SOFTWARE.md": "branch payload\n"}, "branch payload")
    _commit(tmp_path, {".github/workflows/pages.yml": "uses: actions/upload-artifact@v7\n"}, "bump")
    _git(tmp_path, "checkout", "-q", "main")
    _git(tmp_path, "merge", "--no-ff", "-q", "-m", "merge feature", "feature")
    assert source_payload_commit(tmp_path) == branch_payload


def test_content_pr_merged_onto_a_main_advanced_only_by_ci_resolves_the_pr_payload(tmp_path: Path):
    """The merge differs from the PR tip only by main's workflow bump, so the PR's records still bind."""
    _init(tmp_path)
    _commit(tmp_path, {"pages/BIBLIOGRAPHY.md": "payload\n"}, "payload")
    _commit(tmp_path, {"data/pages-artifact-manifest.json": "{}\n"}, "payload (control tail)")
    _git(tmp_path, "checkout", "-qb", "feature")
    feature = _commit(tmp_path, {"pages/SOFTWARE.md": "feature payload\n"}, "feature payload")
    _commit(tmp_path, {"data/pages-artifact-manifest.json": "{\"f\": 1}\n"}, "feature payload (control tail)")
    _git(tmp_path, "checkout", "-q", "main")
    _commit(tmp_path, {".github/workflows/pages.yml": "uses: actions/upload-artifact@v7\n"}, "bump")
    _git(tmp_path, "merge", "--no-ff", "-q", "-m", "merge feature", "feature")
    assert source_payload_commit(tmp_path) == feature


def test_merge_with_payload_on_both_sides_is_the_payload_commit(tmp_path: Path):
    """A later parent's own last commit being a control tail is not enough to step to it.

    The merge differs from each parent by the other side's payload, so it is the
    anchor; judging the parent by its own changes would silently drop main's payload.
    """
    _init(tmp_path)
    _commit(tmp_path, {"pages/BIBLIOGRAPHY.md": "payload\n"}, "payload")
    _commit(tmp_path, {"data/pages-artifact-manifest.json": "{}\n"}, "payload (control tail)")
    _git(tmp_path, "checkout", "-qb", "feature")
    _commit(tmp_path, {"pages/SOFTWARE.md": "feature payload\n"}, "feature payload")
    _commit(tmp_path, {"data/pages-artifact-manifest.json": "{\"f\": 1}\n"}, "feature payload (control tail)")
    _git(tmp_path, "checkout", "-q", "main")
    _commit(tmp_path, {"README.md": "main payload\n"}, "main payload")
    _commit(tmp_path, {"data/pages-artifact-manifest.json": "{\"g\": 1}\n"}, "main payload (control tail)")
    _git(tmp_path, "merge", "--no-ff", "-q", "-X", "ours", "-m", "merge feature", "feature")
    assert source_payload_commit(tmp_path) == _git(tmp_path, "rev-parse", "HEAD")


def test_octopus_merge_steps_to_any_later_payload_equal_parent(tmp_path: Path):
    """Parents [workflow PR, workflow PR, main]: only the third parent matches the merge's payload."""
    advanced = _workflow_pr_behind_an_advanced_main(tmp_path)
    _git(tmp_path, "checkout", "-q", "-b", "other-bump", "main~2")
    _commit(tmp_path, {".github/workflows/browser-qa.yml": "uses: actions/upload-artifact@v7\n"}, "other bump")
    _git(tmp_path, "checkout", "-q", "dependabot/github_actions/bump")
    _git(tmp_path, "merge", "--no-ff", "-q", "-m", "octopus", "other-bump", "main")
    assert len(_git(tmp_path, "show", "-s", "--format=%P", "HEAD").split()) == 3
    assert source_payload_commit(tmp_path) == advanced


def test_an_unreadable_parent_diff_fails_closed(tmp_path: Path):
    _init(tmp_path)
    head = _commit(tmp_path, {"pages/BIBLIOGRAPHY.md": "payload\n"}, "payload")
    paths = release_controls._diff_paths(tmp_path, "0" * 40, head)
    assert paths and not release_controls._carries_no_payload(paths)
    # A merge whose later parent cannot be diffed stays the anchor.
    walked = latest_payload_commit(
        "merge",
        lambda c: {"merge": "base", "base": None}[c],
        lambda c: [Path("pages/BIBLIOGRAPHY.md")],
        parents_for=lambda c: {"merge": ["base", "branch"], "base": []}[c],
        tree_for=lambda c: {"merge": "t-merge", "base": "t-base", "branch": "t-branch"}[c],
        diff_paths_for=lambda parent, commit: paths,
    )
    assert walked == "merge"


def test_ci_configuration_is_outside_the_pages_projection():
    assert ".github" in bpa.EXCLUDED_ROOTS


def test_ci_configuration_never_protects_a_report(tmp_path: Path):
    """The report-citation scan decides which reports ship; CI files must not feed it."""
    _init(tmp_path)
    cited = "reports/external_links_2026-01-01.json"
    _commit(
        tmp_path,
        {
            ".github/workflows/x.yml": f"run: cat {cited}\n",
            ".github/dependabot.yml": f"# {cited}\n",
            ".github/README.md": f"[old]({cited})\n",
            ".github/workflows/untracked-note.md": f"{cited}\n",
        },
        "ci",
    )
    assert cited not in report_references.referenced_report_paths(tmp_path)
    _commit(tmp_path, {"docs/note.md": f"[report]({cited})\n"}, "doc cites")
    assert cited in report_references.referenced_report_paths(tmp_path)  # not vacuous


def _tracked_payload_neutral_paths() -> set[str]:
    listed = _git(REPO_ROOT, "ls-files", "-z", "--", ".github").split("\0")
    neutral = {path for path in listed if path and is_payload_neutral_path(Path(path))}
    assert ".github/workflows/pages.yml" in neutral  # the guard below must not be vacuous
    return neutral


def _expand(patterns: list[str] | tuple[str, ...]) -> set[str]:
    matched: set[str] = set()
    for pattern in patterns:
        matched.update(
            path.relative_to(REPO_ROOT).as_posix() for path in REPO_ROOT.glob(pattern)
        )
    return matched


def test_no_generation_step_reads_payload_neutral_files():
    """A generator input would make a workflow-only commit change payload."""
    neutral = _tracked_payload_neutral_paths()
    offenders = {
        step.identifier: sorted(_expand(effective_step_inputs(step)) & neutral)
        for step in LOCAL_GENERATION_STEPS
    }
    assert {name: paths for name, paths in offenders.items() if paths} == {}


def test_no_generated_artifact_hashes_payload_neutral_files():
    neutral = _tracked_payload_neutral_paths()
    manifest = json.loads((REPO_ROOT / "data" / "generated-manifest.json").read_text(encoding="utf-8"))
    offenders = {
        artifact["name"]: sorted(
            _expand(artifact.get("sources", ())) & neutral
            | _expand(artifact.get("outputs", ())) & neutral
        )
        for artifact in manifest["artifacts"]
    }
    assert {name: paths for name, paths in offenders.items() if paths} == {}
