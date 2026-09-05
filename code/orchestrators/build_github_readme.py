#!/usr/bin/env python3
"""Render `.github/README.md` from the root README with relocated link targets.

GitHub resolves a README's relative links against the directory the file lives
in, and `.github/README.md` takes precedence over the root `README.md` when
rendering the repository page. A byte-identical mirror therefore replaces the
real README with one whose every repo-relative link resolves under `.github/`
— `publications.html` becomes `.github/publications.html`, `papers/` becomes
`.github/papers`, and so on. The 2026-09-02 mirror did exactly that: 120 links
broken on the rendered page, and `validate_repo.py`'s local-link gate red.

The mirror stays (it is what GitHub shows), but it is generated rather than
copied: every repo-relative target is rewritten with a `../` prefix so it
resolves back to the repository root, and the file carries a do-not-edit
marker. Generating it also removes the duplicate-maintenance hazard — the two
files can no longer drift, because one is derived from the other.

Absolute URLs, `mailto:`, `tel:`, bare fragments, and root-absolute paths are
left untouched.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "README.md"
OUT = REPO_ROOT / ".github" / "README.md"

GENERATED_MARKER = (
    "<!-- Generated from ../README.md by code/orchestrators/build_github_readme.py."
    " Do not edit: edit README.md and regenerate (GENERATED.md). -->"
)

# Inline links and images: the target between "](" and the closing ")".
_INLINE_TARGET = re.compile(r"(?<=\]\()([^)\s]+)(?=[)\s])")
# Schemes and forms whose resolution does not depend on the file's directory.
_ABSOLUTE_PREFIXES = ("#", "/", "../", "http://", "https://", "mailto:", "tel:", "data:")


def relocate_target(target: str) -> str:
    """Prefix a repo-relative target so it resolves from `.github/`."""
    if not target or target.startswith(_ABSOLUTE_PREFIXES):
        return target
    if ":" in target.split("/", 1)[0]:
        # Any other scheme (ftp:, irc:, ...) is absolute for our purposes.
        return target
    return "../" + target


def render(source_text: str | None = None) -> str:
    text = source_text if source_text is not None else SOURCE.read_text(encoding="utf-8")
    body = _INLINE_TARGET.sub(lambda m: relocate_target(m.group(1)), text)
    return f"{GENERATED_MARKER}\n\n{body}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if .github/README.md is stale")
    args = parser.parse_args()
    content = render()
    existing = OUT.read_text(encoding="utf-8") if OUT.is_file() else None
    if args.check:
        if existing != content:
            raise SystemExit("Stale generated .github/README.md")
        print("checked .github/README.md")
        return
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(content, encoding="utf-8")
    print("wrote .github/README.md")


if __name__ == "__main__":
    main()
