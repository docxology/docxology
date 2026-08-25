"""Deterministic source and validation helpers for legacy redirect documents.

Redirects are still served as static HTML on GitHub Pages.  Their source lives
here rather than in individually hand-maintained files, so crawler directives,
canonical URLs, refresh targets, and accessible fallback links cannot drift
apart.  A redirect stub deliberately uses a meta refresh only: its CSP permits
no inline JavaScript and the visible link remains usable when refresh is
disabled.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from html.parser import HTMLParser
import os
from pathlib import Path
import re

from generated_outputs import (
    UnsafeGeneratedOutputPathError,
    generated_output_directory_exists,
    read_generated_output_text,
)


SITE_ORIGIN = "https://danielarifriedman.com/"
EXCLUDED_PARTS = frozenset(
    {
        ".git",
        ".pytest_cache",
        ".venv",
        "__pycache__",
        "_site",
        "code",
        "docs",
        "node_modules",
        "reports",
    }
)


@dataclass(frozen=True)
class RedirectStub:
    """One legacy HTML address and its canonical destination."""

    path: str
    title: str
    target_url: str
    canonical_url: str
    link_label: str


REDIRECT_STUBS: tuple[RedirectStub, ...] = (
    RedirectStub("about.html", "About Daniel Ari Friedman", f"{SITE_ORIGIN}#about", SITE_ORIGIN, "About — Daniel Ari Friedman"),
    RedirectStub("agent-verify.html", "Agent Verify — Daniel Ari Friedman", f"{SITE_ORIGIN}cite-verify.html", f"{SITE_ORIGIN}cite-verify.html", "Cite & Verify — Daniel Ari Friedman"),
    RedirectStub("blog/index.html", "Writing — Daniel Ari Friedman", f"{SITE_ORIGIN}#media", SITE_ORIGIN, "Media & Writing — Daniel Ari Friedman"),
    RedirectStub("blog/winged-snowflake-2021/index.html", "Winged Snowflake — Daniel Ari Friedman", f"{SITE_ORIGIN}art.html", f"{SITE_ORIGIN}art.html", "Art — Daniel Ari Friedman"),
    RedirectStub("meditations.html", "Meditations — Daniel Ari Friedman", f"{SITE_ORIGIN}#media", SITE_ORIGIN, "Media — Daniel Ari Friedman"),
    RedirectStub("nft.html", "NFT Art — Daniel Ari Friedman", f"{SITE_ORIGIN}art.html", f"{SITE_ORIGIN}art.html", "Art — Daniel Ari Friedman"),
    RedirectStub("reports.html", "Reports — Daniel Ari Friedman", f"{SITE_ORIGIN}evidence.html", f"{SITE_ORIGIN}evidence.html", "Evidence Ledger — Daniel Ari Friedman"),
    RedirectStub("research.html", "Research — Daniel Ari Friedman", f"{SITE_ORIGIN}#research", SITE_ORIGIN, "Research — Daniel Ari Friedman"),
)


_INLINE_REDIRECT_RE = re.compile(
    r"\b(?:window\.)?location\.(?:replace|assign)\s*\(|\b(?:window\.)?location(?:\.href)?\s*=",
    re.I,
)


class _RedirectProbe(HTMLParser):
    """Recognize a semantic meta refresh without assuming attribute spelling/order.

    The previous regular expression only recognized one serialization:
    ``http-equiv`` before ``content`` with double-quoted attributes.  HTML
    permits single quotes, unquoted values, and arbitrary attribute order, so
    use the standard parser to inspect the actual element instead.  A stub is
    treated as a redirect whenever it declares a non-empty refresh content
    value; target validation is then handled by the exact central renderer.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.has_meta_refresh = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "meta":
            return
        attributes = {
            name.lower(): value
            for name, value in attrs
            if name and value is not None
        }
        if (
            attributes.get("http-equiv", "").strip().lower() == "refresh"
            and attributes.get("content", "").strip()
        ):
            self.has_meta_refresh = True


def has_meta_refresh(text: str) -> bool:
    """Return whether *text* contains a valid semantic meta-refresh element.

    ``HTMLParser`` is deliberately tolerant of normal HTML authoring forms.
    A parser error must never turn a malformed redirect into an invisible
    exception, so the caller gets ``False`` and exact-output validation will
    still flag a declared stub as stale.
    """
    probe = _RedirectProbe()
    try:
        probe.feed(text)
        probe.close()
    except (ValueError, AssertionError):
        return False
    return probe.has_meta_refresh


def render_stub(stub: RedirectStub) -> str:
    """Render a complete deterministic legacy redirect document."""
    title = escape(stub.title, quote=True)
    target = escape(stub.target_url, quote=True)
    canonical = escape(stub.canonical_url, quote=True)
    label = escape(stub.link_label, quote=False)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="Legacy address for {title}; redirects to the canonical page.">
  <meta name="robots" content="noindex, follow">
  <meta http-equiv="refresh" content="0; url={target}">
  <link rel="canonical" href="{canonical}">
</head>
<body>
  <main>
    <p>This address has moved to <a href="{target}">{label}</a>.</p>
  </main>
</body>
</html>
"""


def declared_stubs() -> dict[str, RedirectStub]:
    """Return declarations keyed by their repository-relative output paths."""
    return {stub.path: stub for stub in REDIRECT_STUBS}


def discover_redirect_stubs(repo_root: Path) -> set[str]:
    """Find every tracked-style HTML document that behaves as a redirect.

    Discovery intentionally does not rely on the declaration list.  This lets
    validation catch a newly introduced hand-written redirect before it becomes
    an untested exception to the central source of truth.
    """
    # Validate the trusted repository root before walking.  Individual files
    # are checked again by ``read_generated_output_text`` before parsing, so a
    # symlink cannot turn redirect discovery into an outside-root read.
    generated_output_directory_exists(repo_root, repo_root)
    discovered: set[str] = set()
    for directory, child_dirs, filenames in os.walk(repo_root, followlinks=False):
        current = Path(directory)
        # Mutate ``child_dirs`` in place so vendor/cache trees are never
        # traversed or inspected.  For non-excluded paths, reject a directory
        # link before it can hide a redirect outside the repository boundary.
        for name in list(child_dirs):
            child = current / name
            if name in EXCLUDED_PARTS:
                child_dirs.remove(name)
            elif child.is_symlink():
                raise UnsafeGeneratedOutputPathError(
                    f"symlinked redirect-discovery directory is not permitted: {child}"
                )
        for name in filenames:
            if not name.endswith(".html"):
                continue
            path = current / name
            text = read_generated_output_text(repo_root, path, errors="replace")
            if text is None:
                continue
            if has_meta_refresh(text) or _INLINE_REDIRECT_RE.search(text):
                discovered.add(path.relative_to(repo_root).as_posix())
    return discovered


def collect_redirect_errors(repo_root: Path) -> list[str]:
    """Return exact-output and discovery errors for every redirect stub."""
    errors: list[str] = []
    declared = declared_stubs()
    discovered = discover_redirect_stubs(repo_root)
    undeclared = sorted(discovered - set(declared))
    missing = sorted(set(declared) - discovered)
    for rel in undeclared:
        errors.append(f"undeclared redirect stub: {rel}")
    for rel in missing:
        errors.append(f"declared redirect stub is missing a redirect: {rel}")
    for rel, stub in declared.items():
        path = repo_root / rel
        actual = read_generated_output_text(repo_root, path, errors="replace")
        if actual is None:
            errors.append(f"missing redirect stub: {rel}")
            continue
        rendered = render_stub(stub)
        if actual != rendered:
            errors.append(f"stale redirect stub: {rel}")
    return errors
