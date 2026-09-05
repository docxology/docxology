"""`.github/README.md` is what GitHub renders — its links must resolve.

GitHub picks `.github/README.md` over the root `README.md` for the repository
page and resolves that file's relative links against `.github/`. The mirror
committed on 2026-09-02 was a byte-identical copy, so all 120 of its
repo-relative links pointed at `.github/publications.html`,
`.github/papers/...`, and friends — broken on the rendered page and red in
`validate_repo.py`'s local-link gate.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))

import build_github_readme as mirror  # noqa: E402

MIRROR = REPO_ROOT / ".github" / "README.md"
_TARGET = re.compile(r"\]\(([^)\s]+)")


def test_mirror_is_current():
    assert MIRROR.is_file()
    assert MIRROR.read_text(encoding="utf-8") == mirror.render()


def test_every_relative_target_resolves_from_the_github_directory():
    unresolved = []
    for target in _TARGET.findall(MIRROR.read_text(encoding="utf-8")):
        if target.startswith(("#", "http://", "https://", "mailto:", "tel:", "data:")):
            continue
        path = target.split("#", 1)[0].split("?", 1)[0]
        if not path:
            continue
        candidate = (MIRROR.parent / path) if not path.startswith("/") else (REPO_ROOT / path.lstrip("/"))
        if not candidate.exists():
            unresolved.append(target)
    assert unresolved == [], f"unresolvable targets in the rendered README: {unresolved[:8]}"


def test_absolute_and_anchor_targets_are_left_alone():
    for target in (
        "https://example.org/x",
        "mailto:someone@example.org",
        "#section",
        "/root-absolute.html",
        "../already-relocated.md",
    ):
        assert mirror.relocate_target(target) == target


def test_repo_relative_targets_are_relocated_to_the_repository_root():
    assert mirror.relocate_target("publications.html") == "../publications.html"
    assert mirror.relocate_target("papers/") == "../papers/"
    assert mirror.relocate_target(".well-known/security.txt") == "../.well-known/security.txt"


def test_render_carries_a_do_not_edit_marker():
    """A generated file that reads as hand-written invites a divergent edit."""
    assert mirror.render("# Title\n").startswith(mirror.GENERATED_MARKER)
    assert "build_github_readme.py" in mirror.GENERATED_MARKER
