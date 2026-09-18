"""docxology_tools — canonical import surface for the legacy flat modules.

``code/src/*.py`` (report_paths, site_nav, publication_pairing, ...) are plain
top-level modules. Historically every orchestrator and test inserted
``code/src`` (and sometimes ``code/orchestrators``) onto ``sys.path`` by hand
and imported them flat. This package is the single canonical bootstrap for
that layout:

1. It owns the one canonical ``sys.path`` bootstrap (``code/src`` and
   ``code/orchestrators``). The only other ``sys.path`` writers are the
   orchestrator wrappers themselves, each starting with the uniform
   two-line locate (``sys.path.insert`` of ``code/src`` + the
   ``import docxology_tools`` bootstrap call, DOC-014) so a wrapper run as
   a script — or copied into a minimal fixture checkout next to a bare
   ``__init__.py`` — bootstraps itself. The flat
   modules still import each other by flat names internally, so both
   directories must stay importable.
2. It is a namespace window over ``code/src``: ``__path__`` points there, so
   ``docxology_tools.<flat_module>`` resolves as an ordinary submodule of the
   real file — ``from docxology_tools.report_paths import latest_report``,
   ``import docxology_tools.report_paths as rp``, and the attribute form
   ``from docxology_tools import report_paths`` all work with no eager
   imports. Importing the package itself imports nothing else, so minimal
   checkouts carrying only this ``__init__.py`` plus the modules they use
   (test fixtures, bundled scripts) keep working.

Name-level re-exports are deliberately NOT provided: the flat modules define
colliding public names (``load_json`` exists in both youtube_fetcher and
resume_data; ``REPO_ROOT`` in six modules), so
``from docxology_tools import load_json`` would be ambiguous. Import a
module, then take names from it. Star imports are likewise unsupported.

One import-system affordance beyond the plain window remains: the flat
modules import each other by flat names while callers use the dotted form,
and one file must yield one module object — exception classes raised through
``redirect_stubs`` must stay identical to the ``docxology_tools``
``generated_outputs`` class tests import, monkeypatches must hit the copy the
code under test uses, and ``docxology_tools.report_paths is report_paths``.
``_CrossFormAliasFinder`` wraps the *first* load of any ``MODULES`` member,
whichever form comes first, and mirrors the loaded module under its sibling
name afterwards; when the sibling name is already loaded, the existing object
is reused. Convergence is lazy per module — nothing is registered or aliased
at package import time.
"""

from __future__ import annotations

import importlib.abc
import importlib.machinery
import importlib.util
import sys
from pathlib import Path

_SRC_DIR = Path(__file__).resolve().parents[1]
_ORCH_DIR = _SRC_DIR.parent / "orchestrators"

# The one canonical bootstrap: code/src so the legacy flat modules resolve,
# code/orchestrators so the src->orchestrator cross-imports (seo_invariants)
# and the flat orchestrator imports used by tests keep working wherever the
# package is imported from.
for _dir in (_SRC_DIR, _ORCH_DIR):
    _location = str(_dir)
    if _location not in sys.path:
        sys.path.insert(0, _location)

# Namespace window: docxology_tools.<flat_module> resolves against code/src.
__path__ = [str(_SRC_DIR)]

#: Legacy flat modules (``code/src/*.py``) reachable through this package.
MODULES: tuple[str, ...] = (
    "artifact_budget",
    "biblio_table",
    "bibliography_links",
    "build_stamp",
    "change_classifier",
    "collection_jsonld",
    "count_consistency",
    "deploy_freshness",
    "domain_inference",
    "generated_outputs",
    "generation_plan",
    "paper_metadata_schema",
    "private_reconciliation",
    "public_integrity",
    "public_source_review",
    "publication_pairing",
    "redirect_stubs",
    "release_controls",
    "release_evidence",
    "report_paths",
    "report_references",
    "resume_data",
    "scholar_verification",
    "seo_invariants",
    "site_facts",
    "site_nav",
    "sitemap_policy",
    "software_table",
    "title_policy",
    "youtube_fetcher",
)

_PACKAGE_PREFIX = __name__ + "."


class _CrossFormAliasLoader(importlib.abc.Loader):
    """First-load wrapper: execute the file once, then mirror the module
    object under its sibling import name (flat <-> dotted)."""

    def __init__(self, inner, partner: str) -> None:
        self._inner = inner
        self._partner = partner

    def create_module(self, spec):
        return self._inner.create_module(spec)

    def exec_module(self, module) -> None:
        self._inner.exec_module(module)
        sys.modules.setdefault(self._partner, module)


class _ReuseModuleLoader(importlib.abc.Loader):
    """Hands back an already-initialized sibling module object."""

    def __init__(self, module) -> None:
        self._module = module

    def create_module(self, spec):
        return self._module

    def exec_module(self, module) -> None:
        """The module already ran under its first name; nothing left to do."""


class _CrossFormAliasFinder:
    """meta_path hook: flat and dotted imports of a legacy module share one
    module object (see the module docstring for why).

    Submodule imports outside ``MODULES`` are untouched and keep flowing
    through the plain ``__path__`` window.
    """

    def find_spec(self, fullname, path=None, target=None):
        if fullname in MODULES:
            partner = _PACKAGE_PREFIX + fullname
        elif fullname.startswith(_PACKAGE_PREFIX):
            flat = fullname[len(_PACKAGE_PREFIX):]
            if "." in flat or flat not in MODULES:
                return None
            partner = flat
        else:
            return None
        sibling = sys.modules.get(partner)
        if sibling is not None:
            # The sibling form loaded first (e.g. a flat import before this
            # package was ever imported): alias it, never re-execute.
            return importlib.util.spec_from_loader(
                fullname, _ReuseModuleLoader(sibling)
            )
        spec = importlib.machinery.PathFinder.find_spec(fullname, __path__)
        if spec is None or spec.loader is None:
            return None
        spec.loader = _CrossFormAliasLoader(spec.loader, partner)
        return spec


if not any(
    isinstance(_finder, _CrossFormAliasFinder) for _finder in sys.meta_path
):
    sys.meta_path.insert(0, _CrossFormAliasFinder())


def __getattr__(name: str):
    """Fallback for attribute-form access (normal attribute hits skip this):
    import the flat module — the finder keeps it identical to the dotted
    form — and cache it as a package attribute."""
    if name not in MODULES:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = importlib.import_module(name)
    globals()[name] = module
    return module


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(MODULES))
