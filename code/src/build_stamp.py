"""Build stamp for generated page footers.

The label carries two distinct facts, each named:

    build <short-sha> <YYYY-MM-DD> · generated <YYYY-MM-DDTHH:MM:SSZ>

* **Which payload the page describes.** The short SHA is bound to the
  payload-anchored commit (``release_controls.source_payload_commit``) rather
  than ``HEAD``, and the date is that commit's committer date. Control-only
  tail commits therefore move ``HEAD`` without chasing the stamp, so routine
  re-renders of an unchanged payload tree stay byte-stable.
* **When the page was generated.** The UTC wall-clock instant of the rendering
  run, memoized per process so every page stamped in one run agrees. It is not
  derived from the payload commit, which is why the two are labelled separately:
  a page can describe an old payload and still have been rendered much later.

The ``build <short-sha> <YYYY-MM-DD>`` prefix is a fixed contract and must stay
first and unchanged: ``code/src/deploy_freshness.py:STAMP_RE`` parses the payload
SHA out of exactly that text, so relabelling it disarms the deploy freshness
alarm. The ``generated`` suffix is additive.

``BUILD_SHA``/``BUILD_DATE``/``BUILD_GENERATED_AT`` environment variables
override all three values for release/integration runs that must pin a stamp
explicitly.

Every generator that emits the site footer appends :func:`footer_build_stamp_html`
inside its ``<footer>`` block, so all generated pages share one stamp format and
one commit URL base.
"""

from __future__ import annotations

import os
import re
from collections.abc import Iterable
from datetime import datetime, timezone
from docxology_tools.release_controls import source_payload_commit
import subprocess
from pathlib import Path

COMMIT_URL_BASE = "https://github.com/docxology/docxology/commit"

_SHA_RE = re.compile(r"^[0-9a-f]{7,40}$")
# Matches the full footer stamp anchor so generators can swap the stamp
# text without touching surrounding markup (drift forgiveness).
STAMP_HTML_RE = re.compile(
    r'(<p class="build-stamp"><a href="[^"]*">)(build [^<]+)(</a></p>)'
)
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
GENERATED_AT_FMT = "%Y-%m-%dT%H:%M:%SZ"
_GENERATED_AT_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

# The current label shape, in full. The leading ``build <short-sha> <date>``
# prefix is fixed by code/src/deploy_freshness.py:STAMP_RE; the labelled
# ``generated`` suffix is the additive second fact. ``reuse_on_disk_stamp``
# refuses to reuse a label that does not match this, so a format change forces
# re-rendering instead of being silently forgiven as a stamp-only difference.
STAMP_LABEL_RE = re.compile(
    r"^build [0-9a-f]{7,40} \d{4}-\d{2}-\d{2} · generated "
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)


def label_has_current_shape(label: str) -> bool:
    """Whether a stamp label carries the current, fully labelled shape."""
    return bool(STAMP_LABEL_RE.match(label))


class BuildStampError(RuntimeError):
    """Raised when the build stamp cannot be derived from git or the environment."""


_STAMP_CACHE: tuple[str, str] | None = None
# (pinned override, rendered value) — keyed by the override so a run that pins
# the stamp is never served a timestamp memoized without one.
_GENERATED_AT_CACHE: tuple[str, str] | None = None


def build_stamp_info(repo_root: Path | str | None = None) -> tuple[str, str]:
    """Return ``(short_sha, YYYY-MM-DD)`` for the current build.

    ``BUILD_SHA`` / ``BUILD_DATE`` environment variables take precedence so a
    release or integration run can pin the stamp; otherwise both come from the
    payload-anchored commit (``release_controls.source_payload_commit``), not
    ``HEAD``: control-only tail commits move ``HEAD`` without chasing the
    stamp, so re-rendering an unchanged payload tree is byte-stable. The git
    probes run once per process and are memoized: generators that stamp
    thousands of pages otherwise spawn git subprocesses per page.
    """
    global _STAMP_CACHE
    if repo_root is None and _STAMP_CACHE is not None:
        return _STAMP_CACHE
    root = Path(repo_root) if repo_root else Path(__file__).resolve().parents[2]
    sha = os.environ.get("BUILD_SHA", "").strip()
    stamp_date = os.environ.get("BUILD_DATE", "").strip()
    if sha and _SHA_RE.match(sha) and stamp_date and _DATE_RE.match(stamp_date):
        return sha, stamp_date
    payload_commit = source_payload_commit(root)
    if not _SHA_RE.match(payload_commit):
        raise BuildStampError(
            f"cannot derive payload-anchored source revision: {payload_commit!r}"
        )
    git_sha = _git(root, "rev-parse", "--short", payload_commit)
    git_date = _git(root, "show", "-s", "--format=%cs", payload_commit)
    if not _SHA_RE.match(git_sha):
        raise BuildStampError(f"unexpected git short SHA {git_sha!r}")
    if not _DATE_RE.match(git_date):
        raise BuildStampError(f"unexpected git commit date {git_date!r}")
    if repo_root is None:
        _STAMP_CACHE = (git_sha, git_date)
    return git_sha, git_date


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


def current_on_disk_stamp(html_text: str) -> str | None:
    """The stamp label already embedded in a rendered page, if any."""
    match = STAMP_HTML_RE.search(html_text)
    return match.group(2) if match else None


def reuse_on_disk_stamp(candidate: str, on_disk: str | None) -> str:
    """Keep the on-disk stamp (label AND commit href) when that is the only difference.

    Mirrors ``stable_generated_output_timestamp``: a page whose content is
    byte-identical apart from the build stamp is not stale, so the stamp
    recorded at the last content-touching regeneration is preserved (and
    ``--check`` stays green across non-rendering commits).

    Reuse is refused unless the on-disk label already carries the current,
    fully labelled shape. Drift forgiveness is for a differing stamp *value*,
    never for a differing stamp *format*: without this check a format change
    would be silently forgiven on every page whose content did not otherwise
    change, so the site would converge on the new footer only as pages happened
    to be edited and ``--check`` would never report the mixed state.
    """
    if not on_disk:
        return candidate
    disk_match = STAMP_HTML_RE.search(on_disk)
    if not disk_match:
        return candidate
    if not label_has_current_shape(disk_match.group(2)):
        return candidate
    candidate_matches = list(STAMP_HTML_RE.finditer(candidate))
    disk_matches = list(STAMP_HTML_RE.finditer(on_disk))
    if len(candidate_matches) != 1 or len(disk_matches) != 1:
        return candidate
    # Normalize the complete anchor (including href), and nothing else. A
    # stamp-only candidate cannot establish equality of the rendered page.
    if STAMP_HTML_RE.sub("<build-stamp>", candidate) != STAMP_HTML_RE.sub(
        "<build-stamp>", on_disk
    ):
        return candidate
    disk_anchor = disk_match.group(0)
    return STAMP_HTML_RE.sub(lambda _match: disk_anchor, candidate, count=1)


def find_stamp_label_problems(paths: Iterable[Path]) -> list[tuple[Path, str]]:
    """Return pages whose footer stamp label lacks the current labelled shape.

    A page that carries no stamp is not a problem: most hand-authored pages
    never get a footer stamp. A hand-authored page that does carry one
    (``index.html``, so deploy freshness has a stamp to verify on the home page)
    must carry the same labelled shape as a generated page. A page that carries
    a stamp in the pre-suffix format is a problem, because that format does not
    say which of its two values is the payload commit's committer date and which
    is the rendering instant. The format change is therefore detectable rather
    than something the site can drift into a mixture of without any check
    noticing.
    """
    problems: list[tuple[Path, str]] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for match in STAMP_HTML_RE.finditer(text):
            label = match.group(2)
            if not label_has_current_shape(label):
                problems.append((path, label))
                break
    return problems


def build_generated_at() -> str:
    """The UTC instant this process rendered the stamp.

    The second, independent fact in the label: which payload the page describes
    is a committed property, while when it was generated is a rendering
    property, so the two are labelled separately rather than one standing in
    for the other. Memoized per process so every page stamped in one run agrees,
    and overridable with ``BUILD_GENERATED_AT`` for a release run that must pin
    it.
    """
    global _GENERATED_AT_CACHE
    override = os.environ.get("BUILD_GENERATED_AT", "").strip()
    pinned = override if override and _GENERATED_AT_RE.match(override) else ""
    if _GENERATED_AT_CACHE is not None and _GENERATED_AT_CACHE[0] == pinned:
        return _GENERATED_AT_CACHE[1]
    moment = pinned or datetime.now(timezone.utc).strftime(GENERATED_AT_FMT)
    _GENERATED_AT_CACHE = (pinned, moment)
    return moment


def build_stamp_text(repo_root: Path | str | None = None) -> str:
    """The stamp label, both facts named.

    ``build <short-sha> <YYYY-MM-DD> · generated <UTC>`` — the payload-anchored
    revision the page describes, then when the page was generated. The prefix
    stays first and unchanged because ``deploy_freshness.STAMP_RE`` parses the
    payload SHA from it.
    """
    sha, stamp_date = build_stamp_info(repo_root)
    return f"build {sha} {stamp_date} · generated {build_generated_at()}"


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
