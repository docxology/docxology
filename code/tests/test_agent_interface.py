"""The agent entry point previews real contracts without executing them."""

import json
from pathlib import Path
import subprocess
import sys

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402,F401
import agent  # noqa: E402
from docxology_tools.generation_plan import LOCAL_GENERATION_STEPS, EXCLUDED_OPERATIONS  # noqa: E402


def test_json_plan_is_the_authoritative_order_and_does_not_execute_commands(capsys, monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("plan must not launch a command")

    monkeypatch.setattr(subprocess, "run", forbidden)
    assert agent.main(["plan", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["execution"] == "preview_only"
    assert [row["id"] for row in payload["steps"]] == [step.identifier for step in LOCAL_GENERATION_STEPS]
    for row, step in zip(payload["steps"], LOCAL_GENERATION_STEPS):
        assert row["write_argv"][3:] == [f"code/orchestrators/{step.script}", *step.write_args]
        assert row["check_argv"][3:] == [f"code/orchestrators/{step.script}", *step.check_args]
    assert [row["script"] for row in payload["excluded_operations"]] == [entry.script for entry in EXCLUDED_OPERATIONS]


def test_selected_step_and_invalid_requests_have_json_contract(capsys):
    assert agent.main(["plan", "--step", "catalog", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert [step["id"] for step in payload["steps"]] == ["catalog"]
    assert payload["steps"][0]["git_index_inputs"] == ["reports/**"]
    for argv in (["plan", "--step", "unknown", "--json"], ["push", "--json"],
                 ["plan", "--apply", "--json"]):
        assert agent.main(argv) == 2
        payload = json.loads(capsys.readouterr().out)
        assert payload["ok"] is False and payload["errors"]


def test_status_does_not_certify_clean_checkout_and_observes_detached_dirty_state(tmp_path, capsys, monkeypatch):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.com",
                    "commit", "--allow-empty", "-qm", "fixture"], cwd=tmp_path, check=True)
    subprocess.run(["git", "checkout", "--detach", "-q"], cwd=tmp_path, check=True)
    monkeypatch.setattr(agent, "coverage_errors", lambda **kwargs: [])
    assert agent.main(["status", "--json"], repo_root=tmp_path) == 0
    clean = json.loads(capsys.readouterr().out)
    assert clean["git"]["clean"] is True and clean["git"]["branch"] is None
    assert clean["validation"] == "not_run" and clean["deployment"] == "not_checked"
    assert clean["git"]["remote_verified"] is False
    (tmp_path / "untracked.txt").write_text("work in progress")
    assert agent.main(["status", "--json"], repo_root=tmp_path) == 0
    dirty = json.loads(capsys.readouterr().out)
    assert dirty["git"]["clean"] is False
    assert dirty["human_visual_review"] == "not_attested"


def test_unavailable_git_is_an_error_not_a_clean_state(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(agent, "coverage_errors", lambda **kwargs: [])
    assert agent.main(["status", "--json"], repo_root=tmp_path) == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is False and payload["git"]["available"] is False
    assert "clean" not in payload["git"]


def test_plan_coverage_failure_is_explicit(capsys, monkeypatch):
    monkeypatch.setattr(agent, "coverage_errors", lambda: ["unclassified writer"])
    assert agent.main(["plan", "--json"]) == 1
    assert json.loads(capsys.readouterr().out)["errors"] == ["unclassified writer"]
