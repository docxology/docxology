"""Explicit selection, real prerequisites, and isolated disposable checkouts."""
from __future__ import annotations

import os

import pytest


class SelectedTestsMustRun:
    """A selected skip is incomplete evidence, including reports from workers."""

    def __init__(self) -> None:
        self.incomplete: set[str] = set()

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        if report.skipped:
            self.incomplete.add(report.nodeid)

    def pytest_collectreport(self, report: pytest.CollectReport) -> None:
        if report.skipped:
            self.incomplete.add(report.nodeid)

    def pytest_sessionfinish(self, session: pytest.Session, exitstatus: int) -> None:
        # Workers must finish their protocol normally; the controller owns
        # acceptance after it receives every selected test's report.
        if self.incomplete and not hasattr(session.config, "workerinput"):
            if exitstatus in {pytest.ExitCode.OK, pytest.ExitCode.TESTS_FAILED, pytest.ExitCode.NO_TESTS_COLLECTED}:
                session.exitstatus = pytest.ExitCode.TESTS_FAILED

    def pytest_terminal_summary(self, terminalreporter) -> None:
        if self.incomplete:
            terminalreporter.write_sep("=", "Selected tests did not execute", red=True)
            for nodeid in sorted(self.incomplete):
                terminalreporter.write_line(nodeid, red=True)
            terminalreporter.write_line("Install the declared prerequisites or explicitly select a smaller suite with -m.")


def pytest_configure(config: pytest.Config) -> None:
    config.pluginmanager.register(SelectedTestsMustRun(), "selected-tests-must-run")


@pytest.fixture(scope="session", autouse=True)
def isolated_git_discovery(tmp_path_factory: pytest.TempPathFactory):
    """A non-Git fixture cannot discover the SSD's enclosing manager repo."""
    boundary = str(tmp_path_factory.getbasetemp())
    existing = os.environ.get("GIT_CEILING_DIRECTORIES", "")
    with pytest.MonkeyPatch.context() as environment:
        environment.setenv("GIT_CEILING_DIRECTORIES", boundary + (os.pathsep + existing if existing else ""))
        yield


@pytest.fixture(scope="session")
def browser_runtime() -> None:
    """Prove Chromium can launch once per worker; tests keep fresh contexts."""
    from rendered_site_fixture import require_playwright

    require_playwright()


@pytest.fixture(autouse=True)
def selected_browser_runtime(request: pytest.FixtureRequest) -> None:
    if request.node.get_closest_marker("browser"):
        request.getfixturevalue("browser_runtime")
