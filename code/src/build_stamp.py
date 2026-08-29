"""Build stamp for generated page footers: "build <short-sha> <YYYY-MM-DD>".

The short SHA comes from git at generation time (``git rev-parse --short HEAD``)
and the date is that commit's committer date, so regeneration is deterministic
per commit. ``BUILD_SHA``/``BUILD_DATE`` environment variables override both for
release/integration runs that must pin a stamp explicitly.

Every generator that emits the site footer appends :func:`footer_build_stamp_html`
inside its ``<footer>`` block, so all generated pages share one stamp format and
one commit URL base.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

COMMIT_URL_BASE = "https://github.com/docxology/docxology/commit"

_SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class BuildStampError(RuntimeError):
    """Raised when the build stamp cannot be derived from git or the environment."""


def _git(repo_root: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_root), *args],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise BuildStampError(f"git {' '.join(args)} failed: {exc}") from exc
    return result.stdout.strip()


def build_stamp_info(repo_root: Path | str | None = None) -> tuple[str, str]:
    """Return ``(short_sha, YYYY-MM-DD)`` for the current build.

    ``BUILD_SHA`` / ``BUILD_DATE`` environment variables take precedence so a
    release or integration run can pin the stamp; otherwise both come from the
    repository's HEAD commit.
    """
    root = Path(repo_root) if repo_root else Path(__file__).resolve().parents[2]
    sha = os.environ.get("BUILD_SHA", "").strip()
    stamp_date = os.environ.get("BUILD_DATE", "").strip()
    if sha and _SHA_RE.match(sha) and stamp_date and _DATE_RE.match(stamp_date):
        return sha, stamp_date
    git_sha = _git(root, "rev-parse", "--short", "HEAD")
    git_date = _git(root, "show", "-s", "--format=%cs", "HEAD")
    if not _SHA_RE.match(git_sha):
        raise BuildStampError(f"unexpected git short SHA {git_sha!r}")
    if not _DATE_RE.match(git_date):
        raise BuildStampError(f"unexpected git commit date {git_date!r}")
    return git_sha, git_date


def build_stamp_text(repo_root: Path | str | None = None) -> str:
    """The stamp label: ``build <short-sha> <YYYY-MM-DD>``."""
    sha, stamp_date = build_stamp_info(repo_root)
    return f"build {sha} {stamp_date}"


def build_stamp_url(repo_root: Path | str | None = None) -> str:
    """The commit URL the stamp links to on github.com/docxology/docxology."""
    sha, _ = build_stamp_info(repo_root)
    return f"{COMMIT_URL_BASE}/{sha}"


def footer_build_stamp_html(repo_root: Path | str | None = None) -> str:
    """One-line footer paragraph linking the stamp to its commit URL."""
    return (
        f'<p class="build-stamp"><a href="{build_stamp_url(repo_root)}">'
        f"{build_stamp_text(repo_root)}</a></p>"
    )
