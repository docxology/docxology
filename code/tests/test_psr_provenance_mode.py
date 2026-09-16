"""Public-source-review provenance-mode tests.

The routine default payload-anchored mode binds the review to the last payload
revision (``release_controls.latest_payload_commit`` via
``source_payload_commit``); ``--exact-source-revision`` is the release-gate-only
mode that binds the exact current ``HEAD``.
"""

from __future__ import annotations

import contextlib
import os
import subprocess
import sys
from pathlib import Path

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
_ORCH_DIR = _DOCXOLOGY_SRC.parent / "orchestrators"
for _dir in (_DOCXOLOGY_SRC, _ORCH_DIR):
    if str(_dir) not in sys.path:
        sys.path.append(str(_dir))

import build_public_source_review as psr  # noqa: E402


def _git(
    repo: Path, *args: str, extra_env: dict[str, str] | None = None
) -> str:
    env = os.environ.copy()
    env.update(
        {
            "GIT_AUTHOR_NAME": "Fixture",
            "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
            "GIT_COMMITTER_NAME": "Fixture",
            "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
        }
    )
    if extra_env:
        env.update(extra_env)
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    return result.stdout.strip()


def _payload_repo_with_control_tail(tmp_path: Path) -> tuple[Path, str, str]:
    """A repo whose HEAD is a control-tail commit on top of a payload commit.

    The tail only touches ``reports/public_source_review_*.json``, a path the
    control-tail policy classifies as control metadata, so the payload-anchored
    binding must resolve past it.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "README.md").write_text("payload\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(repo, "commit", "-q", "-m", "payload")
    payload_commit = _git(repo, "rev-parse", "HEAD")
    reports = repo / "reports"
    reports.mkdir()
    (reports / "public_source_review_2026-01-02.json").write_text(
        "{}\n", encoding="utf-8"
    )
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "review control tail")
    head_commit = _git(repo, "rev-parse", "HEAD")
    assert payload_commit != head_commit
    return repo, payload_commit, head_commit


def test_default_mode_binds_the_latest_payload_commit(tmp_path):
    repo, payload_commit, head_commit = _payload_repo_with_control_tail(tmp_path)
    bound = psr._review_source_commit(False, repo)
    assert bound == payload_commit
    assert bound != head_commit


def test_exact_source_revision_binds_head(tmp_path):
    repo, _payload_commit, head_commit = _payload_repo_with_control_tail(tmp_path)
    assert psr._review_source_commit(True, repo) == head_commit


def test_exact_source_revision_is_opt_in_and_default_is_payload_anchored():
    args = psr.build_parser().parse_args([])
    assert args.exact_source_revision is False
    args = psr.build_parser().parse_args(["--exact-source-revision"])
    assert args.exact_source_revision is True


def test_flag_help_states_the_release_gate_only_contract(capsys):
    with contextlib.suppress(SystemExit):
        psr.build_parser().parse_args(["--help"])
    help_text = capsys.readouterr().out
    assert "RELEASE-GATE MODE ONLY" in help_text
    assert "release-integrity.md" in help_text
