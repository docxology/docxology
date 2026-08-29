"""Deterministic freshness alarm comparing the live build stamp to main's HEAD.

The live-verify workflow imports :func:`run_freshness_check` so a stale
production deploy fails the job with a clear message. Kept dependency-free
(standard library only) so the workflow can call it from a plain python3
step without uv extras.
"""

from __future__ import annotations

import os
import re
import subprocess
import time
import urllib.request
from pathlib import Path

DEFAULT_URL = "https://danielarifriedman.com/"
DEFAULT_GRACE_ATTEMPTS = 3
DEFAULT_GRACE_SLEEP_SECONDS = 150
GITHUB_REPO = "docxology/docxology"

# Matches "build <short-sha> <YYYY-MM-DD>" as emitted by code/src/build_stamp.py,
# inside either the plain or anchor-wrapped <p class="build-stamp"> markup.
STAMP_RE = re.compile(r"build ([0-9a-f]{7,40}) \d{4}-\d{2}-\d{2}")


class DeployFreshnessError(RuntimeError):
    """Raised when production is stale (or unverifiable) relative to main."""


def extract_live_stamp(html: str) -> str | None:
    """Return the short SHA in a live build-stamp footer, or None."""
    match = STAMP_RE.search(html)
    return match.group(1) if match else None


def fetch_live_stamp(url: str = DEFAULT_URL) -> str | None:
    """Fetch the live homepage and extract its build stamp (None if absent)."""
    request = urllib.request.Request(  # noqa: S310 - fixed https URL
        url, headers={"User-Agent": "deploy-freshness-check"}
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return extract_live_stamp(response.read().decode("utf-8", errors="replace"))


def main_head_sha_from_checkout(repo_root: Path | None = None) -> str | None:
    """Short SHA of the checked-out commit (the action checks out main)."""
    root = Path(repo_root) if repo_root else Path(__file__).resolve().parents[2]
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
    except (OSError, subprocess.CalledProcessError):
        return None
    return result.stdout.strip() or None


def normalize_sha(sha: str) -> str:
    """Truncate a full SHA to the 7-char short form used in build stamps."""
    return sha[:7]


def run_freshness_check(
    *,
    url: str = DEFAULT_URL,
    expected_sha: str | None = None,
    repo_root: Path | None = None,
    grace_attempts: int = DEFAULT_GRACE_ATTEMPTS,
    grace_sleep_seconds: int = DEFAULT_GRACE_SLEEP_SECONDS,
) -> str:
    """Verify production's build stamp matches main's HEAD short SHA.

    Retries up to ``grace_attempts`` times with ``grace_sleep_seconds`` sleeps
    between attempts, so a normal in-progress deploy does not false-alarm.
    Raises :class:`DeployFreshnessError` with a clear message when the stamp is
    missing or mismatched after the grace window. Returns the live stamp.
    """
    if not expected_sha:
        raise DeployFreshnessError(
            "deploy freshness check requires an expected SHA (workflow must "
            "pass the ref that production was built from)"
        )
    expected = normalize_sha(expected_sha)
    last_error: DeployFreshnessError | None = None
    for attempt in range(1, grace_attempts + 1):
        stamp = None
        try:
            stamp = fetch_live_stamp(url)
        except OSError as exc:
            last_error = DeployFreshnessError(
                f"attempt {attempt}/{grace_attempts}: could not fetch {url}: {exc}"
            )
        if stamp is not None:
            if stamp == expected:
                return stamp
            last_error = DeployFreshnessError(
                f"PRODUCTION STALE: live build stamp is {stamp!r} but main HEAD "
                f"is {expected!r} (attempt {attempt}/{grace_attempts})."
            )
        else:
            last_error = last_error or DeployFreshnessError(
                f"attempt {attempt}/{grace_attempts}: no build-stamp footer "
                f"found on {url} (expected 'build <short-sha> <date>')"
            )
        if attempt < grace_attempts:
            time.sleep(grace_sleep_seconds)
    raise last_error if last_error else DeployFreshnessError("freshness check failed")
