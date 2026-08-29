"""Tests for the live deploy freshness alarm (code/src/deploy_freshness.py)."""

from __future__ import annotations

import sys
import urllib.error
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from deploy_freshness import (  # noqa: E402
    DeployFreshnessError,
    extract_live_stamp,
    normalize_sha,
    run_freshness_check,
)


def test_extract_live_stamp_plain_markup() -> None:
    html = '<p class="build-stamp">build 94bd369 2026-08-28</p>'
    assert extract_live_stamp(html) == "94bd369"


def test_extract_live_stamp_anchor_markup() -> None:
    html = '<p class="build-stamp"><a href="https://github.com/docxology/docxology/commit/94bd369">build 94bd369 2026-08-28</a></p>'
    assert extract_live_stamp(html) == "94bd369"


def test_extract_live_stamp_missing() -> None:
    assert extract_live_stamp("<html><body>no footer</body></html>") is None


def test_normalize_sha_truncates_full_sha() -> None:
    assert normalize_sha("94bd36990a36ae0d5788f66328ee8e73bcd7a1ee") == "94bd369"


def test_run_freshness_check_requires_expected_sha() -> None:
    with pytest.raises(DeployFreshnessError, match="requires an expected SHA"):
        run_freshness_check()


def test_run_freshness_check_immediate_match(monkeypatch: pytest.MonkeyPatch) -> None:
    import deploy_freshness as module

    monkeypatch.setattr(module, "fetch_live_stamp", lambda url: "94bd369")
    assert run_freshness_check(expected_sha="94bd36990a36") == "94bd369"


def test_run_freshness_check_fails_on_mismatch_without_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    import deploy_freshness as module

    monkeypatch.setattr(module, "fetch_live_stamp", lambda url: "94bd369")
    with pytest.raises(DeployFreshnessError, match="PRODUCTION STALE"):
        run_freshness_check(expected_sha="abc1234", grace_attempts=1)


def test_run_freshness_check_missing_stamp_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    import deploy_freshness as module

    monkeypatch.setattr(module, "fetch_live_stamp", lambda url: None)
    with pytest.raises(DeployFreshnessError, match="no build-stamp footer"):
        run_freshness_check(expected_sha="abc1234", grace_attempts=1)


def test_run_freshness_check_grace_window_then_success(monkeypatch: pytest.MonkeyPatch) -> None:
    import deploy_freshness as module

    attempts = {"n": 0}

    def fake_fetch(url: str) -> str | None:
        attempts["n"] += 1
        return "94bd369" if attempts["n"] >= 2 else None

    monkeypatch.setattr(module, "fetch_live_stamp", fake_fetch)
    monkeypatch.setattr(module.time, "sleep", lambda seconds: None)
    assert run_freshness_check(expected_sha="94bd369", grace_attempts=3) == "94bd369"
    assert attempts["n"] == 2


def test_fetch_live_stamp_handles_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    import deploy_freshness as module

    def raise_http_error(url: str) -> str:
        raise OSError("network down")

    monkeypatch.setattr(module, "fetch_live_stamp", raise_http_error)
    with pytest.raises(DeployFreshnessError, match="could not fetch"):
        run_freshness_check(expected_sha="abc1234", grace_attempts=1)
