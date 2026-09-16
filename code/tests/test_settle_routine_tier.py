"""Tests for the settle driver's ``routine`` tier (code/orchestrators/settle.py).

Pure logic tests: tier resolution, battery composition, and the
code-changed-triggers-pytest rule.  No battery step is ever executed and no
git/network call is made — the routines under test only assemble command
tuples from the requested tier and the dirty-path set.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import mock

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

import settle  # noqa: E402

_STEP_NAMES = {step[0] for step in settle._FAST_STEPS}
_PYTEST_NAME = "pytest (code/tests)"
_VALIDATE_NAME = "validate_repo (standard)"


def _names(tier: str, dirty: tuple[str, ...] | None = None) -> list[str]:
    return [name for name, _ in settle.battery_for_tier(tier, dirty)]


def _commands(tier: str, dirty: tuple[str, ...] | None = None) -> dict[str, tuple[str, ...]]:
    return dict(settle.battery_for_tier(tier, dirty))


# --- tier resolution -------------------------------------------------------


def test_tier_order_places_routine_between_fast_and_full() -> None:
    order = settle.TIER_ORDER
    assert order["fast"] < order["routine"] < order["full"] < order["release"]


@pytest.mark.parametrize(
    ("derived", "label"),
    [
        (frozenset({"fast", "full"}), "data intake derives full"),
        (frozenset({"fast"}), "docs-only derives fast"),
        (frozenset(), "clean tree derives nothing"),
    ],
    ids=["data-intake", "docs-only", "clean-tree"],
)
def test_resolve_tier_routine_is_sticky(derived: frozenset[str], label: str) -> None:
    """--tier routine is never raised by path-derived tiers, not even full."""
    assert settle.resolve_tier("routine", derived) == "routine", label


def test_resolve_tier_non_routine_tiers_still_auto_raise() -> None:
    assert settle.resolve_tier("fast", frozenset({"fast", "full"})) == "full"
    assert settle.resolve_tier("full", frozenset({"fast"})) == "full"
    assert settle.resolve_tier("fast", frozenset()) == "fast"


# --- battery composition ---------------------------------------------------


def test_routine_battery_is_fast_floor_plus_standard_validation() -> None:
    names = _names("routine", ("docs/settle-notes.md",))
    assert names == [
        "sitemap --check",
        "artifact budget",
        "ruff lint",
        _VALIDATE_NAME,
    ]
    validate_cmd = _commands("routine", ("docs/settle-notes.md",))[_VALIDATE_NAME]
    assert "code/orchestrators/validate_repo.py" in validate_cmd
    assert "--release" not in validate_cmd


def test_routine_battery_never_includes_the_release_step() -> None:
    for dirty in (("docs/a.md",), ("data/artworks.json",), ("code/src/x.py",)):
        assert not any(
            name.startswith("validate_repo --release")
            for name in _names("routine", dirty)
        )


def test_routine_battery_requires_the_dirty_path_set() -> None:
    """dirty=None must fail closed, never silently guess a composition."""
    with pytest.raises(ValueError):
        settle.battery_for_tier("routine")


def test_full_battery_includes_pytest_and_validation_unconditionally() -> None:
    names = _names("full")
    assert _PYTEST_NAME in names
    assert _VALIDATE_NAME in names
    assert _PYTEST_NAME not in _names("fast")


def test_routine_battery_extends_the_full_battery_below_it() -> None:
    """full = routine (no code dirty) plus the pytest step; same set, richer."""
    routine_names = _names("routine", ("reports/growth.json",))
    full_names = _names("full")
    assert set(routine_names) < set(full_names)
    assert set(full_names) - set(routine_names) == {_PYTEST_NAME}
    # with code dirty, routine composes to exactly full's battery
    assert settle.battery_for_tier("routine", ("code/tests/test_x.py",)) == settle.battery_for_tier("full")


# --- the code-changed-triggers-pytest rule ---------------------------------


@pytest.mark.parametrize(
    "dirty_path",
    ["code/src/new_module.py", "code/orchestrators/settle.py", "code/tests/test_new.py"],
    ids=["src", "orchestrator", "test"],
)
def test_routine_battery_runs_pytest_when_code_paths_are_dirty(
    dirty_path: str,
) -> None:
    assert _PYTEST_NAME in _names("routine", (dirty_path,))


def test_routine_battery_runs_pytest_once_for_mixed_code_and_site_changes() -> None:
    names = _names("routine", ("data/artworks.json", "code/tests/test_x.py"))
    assert names.count(_PYTEST_NAME) == 1
    assert names[-1] == _VALIDATE_NAME


@pytest.mark.parametrize(
    "dirty",
    [
        ("data/artworks.json",),
        ("papers/2026/example.md",),
        ("reports/pages_artifact_growth_2026-09-16.json",),
        ("docs/operations/settle.md",),
    ],
    ids=["data", "papers", "reports", "docs"],
)
def test_routine_battery_skips_pytest_without_code_changes(dirty: tuple[str, ...]) -> None:
    """data/ and other site changes never raise routine to full (nor add pytest)."""
    assert _PYTEST_NAME not in _names("routine", dirty)


# --- CLI surface -----------------------------------------------------------


def test_parse_args_accepts_routine_tier() -> None:
    with mock.patch.object(sys, "argv", ["settle.py", "--tier", "routine"]):
        args = settle.parse_args()
    assert args.tier == "routine"


def test_help_lists_routine_tier(capsys: pytest.CaptureFixture[str]) -> None:
    argv = ["settle.py", "--help"]
    with mock.patch.object(sys, "argv", argv), pytest.raises(SystemExit) as excinfo:
        settle.parse_args()
    assert excinfo.value.code == 0
    assert "routine" in capsys.readouterr().out


def test_fast_step_names_are_the_routine_floor() -> None:
    """The routine battery starts from exactly the fast tier's steps."""
    assert set(_names("routine", ())[:3]) == _STEP_NAMES


