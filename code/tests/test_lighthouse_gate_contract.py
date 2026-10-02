"""Quality-gate failures must not become empty score sets or green skips."""
from __future__ import annotations

import subprocess
from types import SimpleNamespace

import pytest

import test_lighthouse_budgets as gate


@pytest.fixture(autouse=True)
def isolated_contract_reports(tmp_path, monkeypatch):
    """Keep mocked tool output out of retained browser measurements."""
    monkeypatch.setenv("DOCXOLOGY_LIGHTHOUSE_REPORT_DIR", str(tmp_path / "contract-reports"))


@pytest.mark.parametrize("score", [None, "0.9", True, -0.1, 1.1, float("nan"), float("inf")])
def test_invalid_required_category_fails(score):
    payload = {"categories": {name: {"score": 0.9} for name in gate.BUDGETS}}
    payload["categories"]["seo"]["score"] = score
    with pytest.raises(AssertionError, match="seo.*valid score"):
        gate.category_scores(payload)


@pytest.mark.parametrize("payload", [{}, {"categories": {}}, {"categories": {"performance": {"score": 1}}}])
def test_partial_lighthouse_report_cannot_pass(payload):
    with pytest.raises(AssertionError):
        gate.category_scores(payload)


def test_complete_report_preserves_zero_scores():
    assert gate.category_scores({"categories": {name: {"score": 0} for name in gate.BUDGETS}}) == {name: 0 for name in gate.BUDGETS}


@pytest.mark.parametrize("result", [
    SimpleNamespace(returncode=1, stdout="", stderr="Chrome crashed"),
    SimpleNamespace(returncode=0, stdout="not json", stderr=""),
    SimpleNamespace(returncode=0, stdout='{"runtimeError":{"code":"NO_FCP"}}', stderr=""),
])
def test_lighthouse_runtime_and_report_failures_fail(tmp_path, monkeypatch, result):
    monkeypatch.setattr(gate.subprocess, "run", lambda *args, **kwargs: result)
    with pytest.raises(AssertionError):
        gate.run_lighthouse("http://127.0.0.1", "index.html", tmp_path)


def test_lighthouse_deadline_failure_fails(tmp_path, monkeypatch):
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired("lighthouse", 180)
    monkeypatch.setattr(gate.subprocess, "run", timeout)
    with pytest.raises(AssertionError, match="could not complete"):
        gate.run_lighthouse("http://127.0.0.1", "index.html", tmp_path)


def test_mandatory_browser_job_requires_lighthouse(tmp_path, monkeypatch):
    monkeypatch.setenv("DOCXOLOGY_REQUIRE_BROWSER_QA", "1")
    monkeypatch.setattr(gate, "lighthouse_available", lambda: False)
    with pytest.raises(pytest.fail.Exception, match="required.*unavailable"):
        gate.test_lighthouse_budgets(tmp_path, lambda *args: None)


def test_npx_probe_and_run_use_the_hosted_pinned_version(tmp_path, monkeypatch):
    commands = []
    monkeypatch.setattr(gate.shutil, "which", lambda name: "/fake/npx" if name == "npx" else None)
    def run(command, **kwargs):
        commands.append(command)
        stdout = gate.LIGHTHOUSE_VERSION if "--version" in command else '{"categories":{}}'
        return SimpleNamespace(returncode=0, stdout=stdout, stderr="")
    monkeypatch.setattr(gate.subprocess, "run", run)
    assert gate.lighthouse_available()
    gate.run_lighthouse("http://127.0.0.1", "index.html", tmp_path)
    assert all(command[:3] == ["npx", "--yes", "lighthouse@13.4.1"] for command in commands)
