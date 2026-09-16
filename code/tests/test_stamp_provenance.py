"""Stamp provenance tests: the default stamp binds the payload commit, not HEAD.

A control-only tail commit (for example a committed public-source review
receipt under ``reports/``) moves ``HEAD`` without chasing the footer stamp,
so re-rendering an unchanged payload tree is byte-stable. ``BUILD_SHA``/
``BUILD_DATE`` environment overrides still win for release runs.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools import build_stamp  # noqa: E402

FOOTER_STAMP_RE = re.compile(
    r'<p class="build-stamp"><a href="https://github\.com/docxology/docxology/commit/'
    r"([0-9a-f]{7,40})\">(build [0-9a-f]{7,40} \d{4}-\d{2}-\d{2})</a></p>"
)


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
    control-tail policy classifies as control metadata.
    """
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    (repo / "README.md").write_text("payload\n", encoding="utf-8")
    _git(repo, "add", "README.md")
    _git(
        repo,
        "commit",
        "-q",
        "-m",
        "payload",
        extra_env={
            "GIT_AUTHOR_DATE": "2026-01-02T12:00:00+00:00",
            "GIT_COMMITTER_DATE": "2026-01-02T12:00:00+00:00",
        },
    )
    payload_commit = _git(repo, "rev-parse", "HEAD")
    reports = repo / "reports"
    reports.mkdir()
    (reports / "public_source_review_2026-01-02.json").write_text(
        "{}\n", encoding="utf-8"
    )
    _git(repo, "add", ".")
    _git(
        repo,
        "commit",
        "-q",
        "-m",
        "review control tail",
        extra_env={
            "GIT_AUTHOR_DATE": "2026-01-03T12:00:00+00:00",
            "GIT_COMMITTER_DATE": "2026-01-03T12:00:00+00:00",
        },
    )
    head_commit = _git(repo, "rev-parse", "HEAD")
    assert payload_commit != head_commit
    return repo, payload_commit, head_commit


def _commit_date(repo: Path, commit: str) -> str:
    return _git(repo, "show", "-s", "--format=%cs", commit)


def test_default_stamp_binds_payload_commit_not_head(tmp_path):
    repo, payload_commit, head_commit = _payload_repo_with_control_tail(tmp_path)
    sha, stamp_date = build_stamp.build_stamp_info(repo)
    assert payload_commit.startswith(sha)
    assert not head_commit.startswith(sha)
    assert stamp_date == _commit_date(repo, payload_commit)


def test_stamp_is_byte_stable_across_head_moves_on_the_same_payload_tree(tmp_path):
    repo, payload_commit, _head_commit = _payload_repo_with_control_tail(tmp_path)
    # The stamp the payload commit itself would have produced (HEAD at the
    # payload commit) must equal the stamp rendered after the control tail
    # moved HEAD.
    payload_stamp = (
        f"build {_git(repo, 'rev-parse', '--short', payload_commit)} "
        f"{_commit_date(repo, payload_commit)}"
    )
    assert build_stamp.build_stamp_text(repo) == payload_stamp


def test_footer_stamp_url_points_at_the_payload_commit(tmp_path):
    repo, payload_commit, _head_commit = _payload_repo_with_control_tail(tmp_path)
    html = build_stamp.footer_build_stamp_html(repo)
    match = FOOTER_STAMP_RE.search(html)
    assert match, f"bad footer stamp html: {html!r}"
    sha = match.group(1)
    assert payload_commit.startswith(sha)
    assert not _git(repo, "rev-parse", "HEAD").startswith(sha)


def test_build_sha_and_date_overrides_still_win(tmp_path, monkeypatch):
    repo, _payload_commit, _head_commit = _payload_repo_with_control_tail(tmp_path)
    monkeypatch.setenv("BUILD_SHA", "deadbee1234")
    monkeypatch.setenv("BUILD_DATE", "2026-01-02")
    sha, stamp_date = build_stamp.build_stamp_info(repo)
    assert sha == "deadbee1234"
    assert stamp_date == "2026-01-02"


def test_stamp_raises_outside_a_git_checkout(tmp_path):
    empty = tmp_path / "not-a-repo"
    empty.mkdir()
    with pytest.raises(build_stamp.BuildStampError):
        build_stamp.build_stamp_info(empty)
