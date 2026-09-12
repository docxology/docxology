"""Classify changed repository paths into surfaces and settle-driver tiers.

The settle driver decides how much work an update/push cycle needs from the
set of changed paths.  This module owns that decision: every changed path
maps to exactly one surface, the paths split into payload and control
groups, and the tiers to run derive from the surfaces.

Surface mapping (first match wins, repository-relative POSIX paths):

    reports/*                                                    -> reports
    data/*, works/*, papers/*, pages/*, feeds/*                  -> site
    publications.html, publications.html.js, search-index.json,
    sitemap.xml, llms.txt, agent-index.json (exact root names)   -> site
    code/src/*, code/orchestrators/*                             -> code
    code/tests/*                                                 -> tests
    .github/*                                                    -> ci
    docs/*, *.md at the repository root                          -> docs
    everything else                                              -> other

Control paths: a changed path is a control path iff
``release_controls.is_control_path`` accepts it: an exact ``CONTROL_FILES``
entry, or a dated control receipt directly under ``reports/``
(``asset_size_*``, ``pages_artifact_growth_*``, ``public_source_review_*``
with a ``.json``/``.md`` suffix and a valid calendar date).  Dated receipts
ride the control tail deliberately, so they never count as payload
commits; a nested path that merely contains ``reports/`` cannot impersonate
a receipt (the receipt name is only honored for the exact top-level
``reports/`` parent).

Policy:

* ``surfaces`` covers every changed path, control files included.
* Tier policy: surfaces limited to ``reports``/``docs`` run ``fast``; any
  other surface present adds ``full``.  ``release`` is never emitted; it is
  opt-in via a CLI flag in the settle driver, not path-derived.
* Paths keep input order and duplicates; empty input yields empty payload
  and control tuples, no surfaces, and the ``fast`` floor.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from release_controls import is_control_path

_SITE_PREFIXES = ("data/", "works/", "papers/", "pages/", "feeds/")
_SITE_ROOT_FILES = frozenset(
    {
        "publications.html",
        "publications.html.js",
        "search-index.json",
        "sitemap.xml",
        "llms.txt",
        "agent-index.json",
    }
)
_CODE_PREFIXES = ("code/src/", "code/orchestrators/")
_FAST_ONLY_SURFACES = frozenset({"reports", "docs"})
_FAST_TIERS = frozenset({"fast"})
_FAST_AND_FULL_TIERS = frozenset({"fast", "full"})


@dataclass(frozen=True)
class Classification:
    """Settle decision for one batch of changed paths."""

    payload_paths: tuple[str, ...]
    control_paths: tuple[str, ...]
    tiers: frozenset[str]
    surfaces: frozenset[str]


def _surface(path: str) -> str:
    """Return the surface a repository-relative POSIX path belongs to."""
    if path.startswith("reports/"):
        return "reports"
    if path in _SITE_ROOT_FILES or path.startswith(_SITE_PREFIXES):
        return "site"
    if path.startswith(_CODE_PREFIXES):
        return "code"
    if path.startswith("code/tests/"):
        return "tests"
    if path.startswith(".github/"):
        return "ci"
    if path.startswith("docs/") or ("/" not in path and path.endswith(".md")):
        return "docs"
    return "other"


def _tiers(surfaces: frozenset[str]) -> frozenset[str]:
    """Apply the tier policy to a set of surfaces."""
    if surfaces - _FAST_ONLY_SURFACES:
        return _FAST_AND_FULL_TIERS
    return _FAST_TIERS


def classify_paths(paths: Iterable[str]) -> Classification:
    """Split changed paths into payload/control groups and derive tiers.

    See the module docstring for the surface mapping, the control-path rule,
    and the tier policy.
    """
    payload: list[str] = []
    control: list[str] = []
    surfaces: set[str] = set()
    for path in paths:
        surfaces.add(_surface(path))
        if is_control_path(Path(path)):
            control.append(path)
        else:
            payload.append(path)
    surface_set = frozenset(surfaces)
    return Classification(
        payload_paths=tuple(payload),
        control_paths=tuple(control),
        tiers=_tiers(surface_set),
        surfaces=surface_set,
    )
