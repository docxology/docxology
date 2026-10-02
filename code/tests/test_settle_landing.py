"""Landing regressions use disposable Git repos; no network or real commits."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401
import settle  # noqa: E402
from docxology_tools.release_controls import source_payload_commit  # noqa: E402


def git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True, text=True,
    ).stdout


def write(root: Path, name: str, content: str = "baseline\n") -> None:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def initialize_repo(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-b", "codex/fixture")
    git(root, "config", "user.name", "Public fixture")
    git(root, "config", "user.email", "fixture@example.invalid")
    git(root, "config", "commit.gpgsign", "false")
    git(root, "config", "core.hooksPath", "/dev/null")
    # Disposable repos must not inherit an ambient filesystem daemon/cache.
    # A globally enabled macOS fsmonitor creates detached daemons per fixture
    # and couples parallel status/ls-files checks to external IPC lifetime.
    # These settings affect only this temporary repo, before its first add.
    git(root, "config", "core.fsmonitor", "false")
    git(root, "config", "core.untrackedCache", "false")
    for name in ("README.md", "unrelated.md", "data/agent-index.json"):
        write(root, name)
    git(root, "add", "--all")
    git(root, "commit", "-m", "baseline")
    return root


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    initialize_repo(tmp_path)
    monkeypatch.setattr(settle, "REPO_ROOT", tmp_path)
    return tmp_path


def test_disposable_repo_overrides_enabled_ambient_monitor_without_mutating_global_config(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    global_config = tmp_path / "ambient.gitconfig"
    original = "[core]\nfsmonitor = true\nuntrackedCache = true\n"
    global_config.write_text(original)
    trace_path = tmp_path / "git-trace.jsonl"
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(global_config))
    monkeypatch.setenv("GIT_TRACE2_EVENT", str(trace_path))
    root = initialize_repo(tmp_path / "repo")
    monkeypatch.setattr(settle, "REPO_ROOT", root)

    assert git(root, "config", "--global", "--get", "core.fsmonitor").strip() == "true"
    assert git(root, "config", "--global", "--get", "core.untrackedCache").strip() == "true"
    assert git(root, "config", "--local", "--get", "core.fsmonitor").strip() == "false"
    assert git(root, "config", "--local", "--get", "core.untrackedCache").strip() == "false"
    write(root, "README.md", "real payload\n")
    assert settle.dirty_paths() == ["README.md"]
    assert "README.md" in settle._git_paths("--cached")
    assert settle.commit_paths(["README.md"], "isolated real commit", "fixture")
    assert settle.dirty_paths() == []

    events = [json.loads(line) for line in trace_path.read_text().splitlines()]
    assert not any(
        event.get("event") == "child_start"
        and any("fsmonitor" in argument for argument in event.get("argv", []))
        for event in events
    )
    assert global_config.read_text() == original


def test_scoped_commit_preserves_previously_staged_controls_and_other_paths(repo: Path) -> None:
    write(repo, "README.md", "payload\n")
    write(repo, "unrelated.md", "staged unrelated\n")
    write(repo, "data/agent-index.json", "staged control\n")
    git(repo, "add", "unrelated.md", "data/agent-index.json")
    staged_before = git(repo, "diff", "--cached", "--binary")

    assert settle.commit_paths(["README.md"], "payload", "fixture")

    assert git(repo, "show", "--format=", "--name-only", "HEAD").splitlines() == ["README.md"]
    assert git(repo, "diff", "--cached", "--binary") == staged_before


def test_scoped_commit_treats_wildcards_and_spaces_as_literal_paths(repo: Path) -> None:
    write(repo, "docs/[ab] file.md", "selected\n")
    write(repo, "docs/a file.md", "other\n")
    git(repo, "add", "--all")

    assert settle.commit_paths(["docs/[ab] file.md"], "literal path", "fixture")

    assert git(repo, "show", "--format=", "--name-only", "HEAD").splitlines() == ["docs/[ab] file.md"]
    assert git(repo, "diff", "--cached", "--name-only").splitlines() == ["docs/a file.md"]


def test_rename_source_and_destination_land_together(repo: Path) -> None:
    git(repo, "mv", "README.md", "renamed README.md")
    write(repo, "data/agent-index.json", "staged control\n")
    git(repo, "add", "data/agent-index.json")
    paths = [path for path in settle.dirty_paths() if not settle.is_control_path(Path(path))]
    assert paths == ["README.md", "renamed README.md"]

    assert settle.commit_paths(paths, "rename", "fixture")

    assert "R100\tREADME.md\trenamed README.md" in git(repo, "show", "--format=", "--name-status", "HEAD")
    assert git(repo, "diff", "--cached", "--name-only").splitlines() == ["data/agent-index.json"]


def test_rename_source_from_removed_directory_is_still_a_commit_path(repo: Path) -> None:
    write(repo, "old folder/source.md", "move me\n")
    git(repo, "add", "--all")
    git(repo, "commit", "-m", "nested source")
    (repo / "new folder").mkdir()
    git(repo, "mv", "old folder/source.md", "new folder/source.md")
    (repo / "old folder").rmdir()
    paths = settle.dirty_paths()

    assert set(settle._path_state(paths)) == {"old folder/source.md", "new folder/source.md"}
    assert settle.commit_paths(paths, "nested move", "fixture")
    assert settle.dirty_paths() == []


@pytest.mark.parametrize("staged", [False, True])
def test_scoped_deletion_handles_staged_and_unstaged_sources(repo: Path, staged: bool) -> None:
    (repo / "README.md").unlink()
    if staged:
        git(repo, "add", "README.md")
    write(repo, "data/agent-index.json", "retained control\n")
    git(repo, "add", "data/agent-index.json")

    assert settle.commit_paths(["README.md"], "delete", "fixture")

    assert git(repo, "show", "--format=", "--name-status", "HEAD").strip() == "D\tREADME.md"
    assert git(repo, "diff", "--cached", "--name-only").splitlines() == ["data/agent-index.json"]


def binder_fixture(repo: Path, monkeypatch: pytest.MonkeyPatch, *, oscillate: bool = False,
                   payload_drift: bool = False) -> list[str]:
    """Model the real retention/discovery cycle with Git's actual index.

    The first Pages pass sees an old agent pointer and keeps an old receipt.
    Its newly written growth receipt must be tracked before discovery can
    update the pointer. The next Pages pass can then retire the old receipt.
    """
    old = "reports/pages_artifact_growth_2026-09-30.json"
    new = "reports/pages_artifact_growth_2026-10-01.json"
    write(repo, old, "old\n")
    write(repo, "data/agent-index.json", json.dumps({"receipt": old}))
    write(repo, "data/review-input.json", "{}\n")
    review = "reports/public_source_review_2026-09-30.json"
    write(repo, review, json.dumps({
        "date": "2026-09-30",
        "inputs": {name: {"path": "data/review-input.json"} for name in settle._REVIEW_INPUT_FLAGS},
        "refresh_context": {"pairing_refresh_status": "failed", "pairing_refresh_note": "--preserved failure note"},
    }))
    git(repo, "add", "--all")
    git(repo, "commit", "-m", "fixture old receipt")
    calls: list[str] = []

    def run_steps(steps):
        for _name, command in steps:
            script = Path(command[4]).name
            calls.append(script + (" --check" if "--check" in command or "--check-manifest" in command else ""))
            if "--check" in command or "--check-manifest" in command:
                continue
            if script == "build_public_source_review.py":
                assert command[command.index("--date") + 1] == "2026-09-30"
                assert command[command.index("--previous-snapshot") + 1] == "data/review-input.json"
                assert command[command.index("--pairing-refresh-status") + 1] == "failed"
                assert "--pairing-refresh-note=--preserved failure note" in command
                report = json.loads((repo / review).read_text())
                report["source_commit"] = source_payload_commit(repo)
                write(repo, review, json.dumps(report))
            elif script == "build_pages_artifact.py":
                pointer = json.loads((repo / "data/agent-index.json").read_text())["receipt"]
                write(repo, new, "new\n")
                write(repo, "data/pages-artifact-manifest.json", json.dumps({
                    "source": source_payload_commit(repo), "retained": [old] if pointer == old else [],
                }))
                if payload_drift:
                    write(repo, "unrelated.md", "concurrent edit\n")
            elif script == "build_generated_manifest.py":
                assert new in git(repo, "ls-files").splitlines(), "receipt was not staged before discovery"
                manifest = json.loads((repo / "data/pages-artifact-manifest.json").read_text())
                write(repo, "data/generated-manifest.json", json.dumps(manifest))
            elif script == "build_agent_index.py":
                assert new in git(repo, "ls-files").splitlines()
                write(repo, "data/agent-index.json", json.dumps({"receipt": new}))
            elif script == "build_release_integrity.py":
                prior = (repo / "data/release-integrity.json")
                value = not json.loads(prior.read_text())["toggle"] if oscillate and prior.exists() else oscillate
                write(repo, "data/release-integrity.json", json.dumps({"toggle": value}))
        return True

    monkeypatch.setattr(settle, "run_steps", run_steps)
    return calls


def test_binders_reach_retention_fixed_point_and_bind_scoped_payload(repo: Path, monkeypatch) -> None:
    calls = binder_fixture(repo, monkeypatch)
    write(repo, "README.md", "landed payload\n")
    assert settle.commit_paths(["README.md"], "payload", "fixture")
    payload_head = git(repo, "rev-parse", "HEAD").strip()

    assert settle.rebind_controls()

    assert calls.count("build_pages_artifact.py") == 3
    manifest = json.loads((repo / "data/pages-artifact-manifest.json").read_text())
    assert manifest == {"source": payload_head, "retained": []}
    review = json.loads((repo / "reports/public_source_review_2026-09-30.json").read_text())
    assert review["source_commit"] == payload_head
    assert review["date"] == "2026-09-30"
    assert review["refresh_context"]["pairing_refresh_note"] == "--preserved failure note"
    controls = [path for path in settle.dirty_paths() if settle.is_control_path(Path(path))]
    assert "reports/pages_artifact_growth_2026-10-01.json" in controls
    assert settle.commit_paths(controls, "binders", "fixture")
    assert source_payload_commit(repo) == payload_head
    assert settle.dirty_paths() == []


def test_nonconvergent_controls_fail_at_bound_without_commit(repo: Path, monkeypatch, capsys) -> None:
    calls = binder_fixture(repo, monkeypatch, oscillate=True)
    head = git(repo, "rev-parse", "HEAD")

    assert not settle.rebind_controls(max_passes=4)

    assert calls.count("build_pages_artifact.py") == 4
    assert "did not converge within 4 passes" in capsys.readouterr().out
    assert git(repo, "rev-parse", "HEAD") == head


def test_payload_drift_during_rebind_is_preserved_and_fails_before_commit(repo: Path, monkeypatch) -> None:
    binder_fixture(repo, monkeypatch, payload_drift=True)
    head = git(repo, "rev-parse", "HEAD")

    assert not settle.rebind_controls()

    assert (repo / "unrelated.md").read_text() == "concurrent edit\n"
    assert "unrelated.md" not in git(repo, "diff", "--cached", "--name-only").splitlines()
    assert git(repo, "rev-parse", "HEAD") == head


@pytest.mark.parametrize("unsafe", ["../private.json", "/tmp/private.json", "data/missing.json", ".", None])
def test_review_replay_refuses_untracked_external_or_absent_inputs_before_writing(repo: Path, monkeypatch, unsafe) -> None:
    calls = binder_fixture(repo, monkeypatch)
    path = repo / "reports/public_source_review_2026-09-30.json"
    report = json.loads(path.read_text())
    report["inputs"]["previous_public_source_snapshot"] = {"path": unsafe}
    path.write_text(json.dumps(report))
    before = path.read_bytes()
    head = git(repo, "rev-parse", "HEAD")

    assert not settle.rebind_controls()

    assert calls == []
    assert path.read_bytes() == before
    assert git(repo, "diff", "--cached", "--name-only") == ""
    assert git(repo, "rev-parse", "HEAD") == head


def test_recorded_review_command_parses_without_defaulting_baseline_or_failure_note(repo: Path, monkeypatch) -> None:
    import build_public_source_review

    binder_fixture(repo, monkeypatch)
    _name, _script, args = settle._review_writer()
    parsed = build_public_source_review.build_parser().parse_args(list(args))

    assert parsed.date == "2026-09-30"
    assert parsed.report == "reports/public_source_review_2026-09-30.json"
    assert parsed.previous_snapshot == "data/review-input.json"
    assert parsed.pairing_refresh_status == "failed"
    assert parsed.pairing_refresh_note == "--preserved failure note"
    assert not parsed.exact_source_revision


@pytest.mark.parametrize("target", [
    "data/review-input.json",
    "reports/public_source_review_2026-09-30.json",
    "reports/public_source_review_2026-09-30.md",
    "reports/public_source_review_2026-09-30.json.tmp",
    "reports/public_source_review_2026-09-30.md.tmp",
])
@pytest.mark.parametrize("link_kind", ["symlink", "hardlink"])
def test_review_replay_rejects_links_to_ignored_private_sentinels_before_read_or_write(
    repo: Path, monkeypatch, target: str, link_kind: str,
) -> None:
    calls = binder_fixture(repo, monkeypatch)
    (repo / ".git" / "info" / "exclude").write_text("private/\n")
    sentinel = repo / "private" / "sentinel.json"
    write(repo, "private/sentinel.json", '{"synthetic_private_sentinel": "unchanged"}\n')
    before = sentinel.read_bytes()
    alias = repo / target
    alias.unlink(missing_ok=True)
    if link_kind == "symlink":
        alias.symlink_to(os.path.relpath(sentinel, alias.parent))
    else:
        os.link(sentinel, alias)
    assert git(repo, "check-ignore", "private/sentinel.json").strip() == "private/sentinel.json"
    read_paths = []
    original_read = Path.read_text

    def observe_read(path, *args, **kwargs):
        read_paths.append(path)
        return original_read(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", observe_read)

    with pytest.raises(ValueError, match="symlinked|hard-linked"):
        settle._review_writer()

    assert alias not in read_paths
    assert sentinel not in read_paths
    assert calls == []
    assert sentinel.read_bytes() == before


@pytest.mark.parametrize("ancestor", ["data", "reports"])
def test_review_replay_rejects_linked_ancestors_before_reading_private_files(repo: Path, monkeypatch, ancestor: str) -> None:
    calls = binder_fixture(repo, monkeypatch)
    (repo / ".git" / "info" / "exclude").write_text("private/\n")
    private = repo / "private"
    private.mkdir()
    original = repo / ancestor
    moved = private / ancestor
    original.rename(moved)
    original.symlink_to(moved.relative_to(repo))
    before = {path.name: path.read_bytes() for path in moved.iterdir() if path.is_file()}
    read_paths = []
    original_read = Path.read_text

    def observe_read(path, *args, **kwargs):
        read_paths.append(path)
        return original_read(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", observe_read)

    with pytest.raises(ValueError, match="symlinked"):
        settle._review_writer()

    assert not any(path.is_relative_to(original) for path in read_paths)
    assert calls == []
    assert {path.name: path.read_bytes() for path in moved.iterdir() if path.is_file()} == before


def test_commit_refuses_hardlinked_source_before_staging_private_sentinel(repo: Path) -> None:
    (repo / ".git" / "info" / "exclude").write_text("private/\n")
    write(repo, "private/sentinel.txt", "synthetic private sentinel\n")
    sentinel = repo / "private/sentinel.txt"
    before = sentinel.read_bytes()
    (repo / "README.md").unlink()
    os.link(sentinel, repo / "README.md")
    head = git(repo, "rev-parse", "HEAD")

    assert not settle.commit_paths(["README.md"], "must refuse", "fixture")

    assert git(repo, "rev-parse", "HEAD") == head
    assert git(repo, "diff", "--cached", "--name-only") == ""
    assert sentinel.read_bytes() == before


def test_missing_review_fails_preflight_before_any_commit(repo: Path, monkeypatch) -> None:
    write(repo, "README.md", "payload\n")
    head = git(repo, "rev-parse", "HEAD")
    args = argparse.Namespace(tier="full", dry_run=False, commit_message=None,
                              skip_commit=False, push=True, pr=None)
    monkeypatch.setattr(settle, "parse_args", lambda: args)
    monkeypatch.setattr(settle, "run_battery", lambda *_: pytest.fail("review must precede battery"))
    monkeypatch.setattr(settle, "push_head", lambda: pytest.fail("must not push"))

    with pytest.raises(SystemExit):
        settle.main()

    assert git(repo, "rev-parse", "HEAD") == head
    assert git(repo, "diff", "--cached", "--name-only") == ""


def test_main_discovers_new_controls_and_validates_landed_tree_before_push(repo: Path, monkeypatch) -> None:
    calls = binder_fixture(repo, monkeypatch)
    write(repo, "README.md", "payload\n")
    # This existing staged control must stay outside the payload commit.
    write(repo, "data/agent-index.json", json.dumps({
        "receipt": "reports/pages_artifact_growth_2026-09-30.json", "pending": True,
    }))
    git(repo, "add", "data/agent-index.json")
    args = argparse.Namespace(tier="full", dry_run=False, commit_message="land fixture",
                              skip_commit=False, push=True, pr=None)
    monkeypatch.setattr(settle, "parse_args", lambda: args)
    monkeypatch.setattr(settle, "run_battery", lambda *_: True)
    pushed = []

    def push():
        assert calls[-1] == "validate_repo.py"
        assert settle.dirty_paths() == []
        pushed.append(git(repo, "rev-parse", "HEAD").strip())
        return True

    monkeypatch.setattr(settle, "push_head", push)
    settle.main()

    assert len(pushed) == 1
    assert git(repo, "show", "--format=", "--name-only", "HEAD~1").splitlines() == ["README.md"]
    tail_paths = git(repo, "show", "--format=", "--name-only", "HEAD").splitlines()
    assert "reports/pages_artifact_growth_2026-10-01.json" in tail_paths
    assert all(settle.is_control_path(Path(path)) for path in tail_paths)
    assert source_payload_commit(repo) == git(repo, "rev-parse", "HEAD~1").strip()


def test_skip_commit_push_requires_a_clean_validated_tree(repo: Path, monkeypatch) -> None:
    write(repo, "README.md", "unlanded payload\n")
    head = git(repo, "rev-parse", "HEAD")
    args = argparse.Namespace(tier="full", dry_run=False, commit_message=None,
                              skip_commit=True, push=True, pr=None)
    monkeypatch.setattr(settle, "parse_args", lambda: args)
    monkeypatch.setattr(settle, "run_battery", lambda *_: True)
    monkeypatch.setattr(settle, "push_head", lambda: pytest.fail("must not push dirty tree"))

    with pytest.raises(SystemExit):
        settle.main()

    assert git(repo, "rev-parse", "HEAD") == head
    assert git(repo, "diff", "--cached", "--name-only") == ""


@pytest.mark.parametrize("failure", ["rebind", "validation"])
def test_landing_failure_never_pushes(repo: Path, monkeypatch, failure: str) -> None:
    write(repo, "README.md", "payload\n")
    args = argparse.Namespace(tier="full", dry_run=False, commit_message=None,
                              skip_commit=False, push=True, pr=None)
    monkeypatch.setattr(settle, "parse_args", lambda: args)
    monkeypatch.setattr(settle, "run_battery", lambda *_: True)
    monkeypatch.setattr(settle, "refresh_review", lambda: True)
    monkeypatch.setattr(settle, "rebind_controls", lambda: failure != "rebind")
    monkeypatch.setattr(settle, "validate_landing", lambda: False)
    pushed = []
    monkeypatch.setattr(settle, "push_head", lambda: pushed.append(True))

    with pytest.raises(SystemExit):
        settle.main()

    assert pushed == []


def test_payload_change_during_battery_never_lands_or_pushes(repo: Path, monkeypatch) -> None:
    write(repo, "README.md", "original request\n")
    before = git(repo, "rev-parse", "HEAD")
    args = argparse.Namespace(tier="full", dry_run=False, commit_message=None,
                              skip_commit=False, push=True, pr=None)
    monkeypatch.setattr(settle, "parse_args", lambda: args)
    monkeypatch.setattr(settle, "refresh_review", lambda: True)

    def battery(*_args):
        write(repo, "README.md", "concurrent change\n")
        return True

    monkeypatch.setattr(settle, "run_battery", battery)
    monkeypatch.setattr(settle, "push_head", lambda: pytest.fail("must not push"))
    with pytest.raises(SystemExit):
        settle.main()
    assert git(repo, "rev-parse", "HEAD") == before
    assert (repo / "README.md").read_text() == "concurrent change\n"
