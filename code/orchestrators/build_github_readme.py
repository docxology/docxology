#!/usr/bin/env python3
"""Render the profile README with absolute links usable on GitHub profile and repository pages."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "README.md"
OUT = REPO_ROOT / ".github" / "README.md"

# Published site that serves the generated `.html` pages at their repo paths.
SITE_ORIGIN = "https://danielarifriedman.com/"

GENERATED_MARKER = (
    "<!-- Generated from ../README.md by code/orchestrators/build_github_readme.py."
    " Do not edit: edit README.md and regenerate (GENERATED.md). -->"
)

# Inline links and images: the target between "](" and the closing ")".
_INLINE_TARGET = re.compile(r"(?<=\]\()([^)\s]+)(?=[)\s])")
# Schemes and forms whose resolution does not depend on the file's directory.
_ABSOLUTE_PREFIXES = (
    "#",
    "/",
    "http://",
    "https://",
    "mailto:",
    "tel:",
    "data:",
)


def relocate_target(target: str) -> str:
    """Resolve a repository path independently of GitHub rendering context.

    Repo-relative `.html` pages resolve to the published site instead.
    """
    if target.startswith("/") and not target.startswith("//"):
        return SITE_ORIGIN + target.lstrip("/")
    if target.startswith("../"):
        target = target.removeprefix("../")
    if not target or target.startswith(_ABSOLUTE_PREFIXES):
        return target
    if ":" in target.split("/", 1)[0]:
        # Any other scheme (ftp:, irc:, ...) is absolute for our purposes.
        return target
    path = target.split("#", 1)[0].split("?", 1)[0]
    if path.endswith(".html"):
        # github.com shows an .html blob as source; send readers to the rendered page.
        return SITE_ORIGIN + target
    if path.endswith(".md") or path.startswith("code/"):
        return "https://github.com/docxology/docxology/blob/main/" + target
    if path.endswith("/"):
        return "https://github.com/docxology/docxology/tree/main/" + target
    return SITE_ORIGIN + target


def render(source_text: str | None = None) -> str:
    text = (
        source_text if source_text is not None else SOURCE.read_text(encoding="utf-8")
    )
    body = _INLINE_TARGET.sub(lambda m: relocate_target(m.group(1)), text)
    return f"{GENERATED_MARKER}\n\n{body}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Fail if .github/README.md is stale"
    )
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
