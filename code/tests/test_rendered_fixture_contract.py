"""Mandatory browser gates cannot turn missing capabilities into green skips."""
from __future__ import annotations

from contextlib import contextmanager
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import rendered_site_fixture as fixture  # noqa: E402


@pytest.mark.parametrize("required", [False, True])
def test_missing_actual_chromium_executable_is_not_available(monkeypatch, tmp_path, required):
    @contextmanager
    def fake_playwright():
        yield SimpleNamespace(chromium=SimpleNamespace(executable_path=str(tmp_path / "missing-chromium")))
    monkeypatch.setitem(sys.modules, "playwright.sync_api", SimpleNamespace(sync_playwright=fake_playwright))
    monkeypatch.delenv("GITHUB_JOB", raising=False)
    monkeypatch.setenv("DOCXOLOGY_REQUIRE_BROWSER_QA", "1" if required else "0")
    expected = pytest.fail.Exception if required else pytest.skip.Exception
    with pytest.raises(expected, match="chromium.*missing"):
        fixture.skip_without_playwright()


@pytest.mark.parametrize("required", [False, True])
def test_missing_playwright_is_explicit_skip_or_required_failure(monkeypatch, required):
    monkeypatch.setitem(sys.modules, "playwright.sync_api", None)
    monkeypatch.delenv("GITHUB_JOB", raising=False)
    monkeypatch.setenv("DOCXOLOGY_REQUIRE_BROWSER_QA", "1" if required else "0")
    expected = pytest.fail.Exception if required else pytest.skip.Exception
    with pytest.raises(expected, match="playwright unavailable"):
        fixture.skip_without_playwright()


def test_hosted_browser_job_is_mandatory_without_extra_flag(monkeypatch):
    monkeypatch.delenv("DOCXOLOGY_REQUIRE_BROWSER_QA", raising=False)
    monkeypatch.setenv("GITHUB_JOB", "browser-tests")
    with pytest.raises(pytest.fail.Exception, match="Required browser QA"):
        fixture.unavailable_browser_capability("loopback socket unavailable")


def test_copied_site_contains_actual_root_runtime_exports_and_pwa_icons(tmp_path):
    site = fixture.copy_site(tmp_path)
    names = sorted(fixture.ROOT_RUNTIME_FILES | {path.name for path in fixture.REPO_ROOT.glob("search-index*.json")})
    assert {"search-index.json", "search-index-core.json", "search-index-bootstrap.json", "search-index-content-work.json", "search-index-content-video.json"}.issubset(names)
    for relative in [*names, *fixture.PWA_ICON_FILES]:
        assert (site / relative).read_bytes() == (fixture.REPO_ROOT / relative).read_bytes(), relative
