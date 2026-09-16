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
        (frozenset({"full"}), "data-derived full"),
        (frozenset({"fast", "full"}), "mixed derived"),
    ],
)
def test_resolve_tier_routine_is_sticky(derived: frozenset[str], label: str) -> None:
    """--tier routine ignores path-derived CONVENIENCE raises when payload-clean."""
    assert settle.resolve_tier("routine", derived, payload_dirty=False) == "routine", label


@pytest.mark.parametrize(
    ("dirty", "label"),
    [
        (("data/artworks.json",), "data/"),
        (("code/src/x.py",), "code/"),
        (("docs/operations/settle.md",), "docs/"),
        (("reports/live_site_verification_2026-09-16.json",), "receipt"),
        (("data/agent-index.json", "docs/operations/settle.md"), "control+payload mix"),
        (("some/unclassified/path.txt",), "leftover counts as payload"),
    ],
)
def test_resolve_tier_routine_raises_to_full_on_payload_dirty(
    dirty: tuple[str, ...], label: str
) -> None:
    """Every payload commit moves the anchor the Pages deploy re-validates."""
    from pathlib import Path as _Path

    payload_dirty = any(
        not settle.is_control_path(_Path(path)) for path in dirty
    )
    assert payload_dirty, label
    assert settle.resolve_tier("routine", frozenset(), payload_dirty) == "full", label


def test_resolve_tier_routine_stays_routine_for_control_only_dirty() -> None:
    from pathlib import Path as _Path

    dirty = ("data/agent-index.json", "data/generated-manifest.json")
    payload_dirty = any(not settle.is_control_path(_Path(path)) for path in dirty)
    assert not payload_dirty
    assert settle.resolve_tier("routine", frozenset({"full"}), payload_dirty) == "routine"


def test_resolve_tier_non_routine_tiers_still_auto_raise() -> None:
    assert settle.resolve_tier("fast", frozenset({"fast", "full"})) == "full"
    assert settle.resolve_tier("full", frozenset({"fast"})) == "full"
    assert settle.resolve_tier("fast", frozenset()) == "fast"


# --- battery composition ---------------------------------------------------


def test_routine_battery_is_fast_floor_plus_standard_validation() -> None:
    names = _names("routine", ())
    assert names[:3] == [name for name in sorted(_STEP_NAMES, key=names.index)]
    assert _VALIDATE_NAME in names
    validate_cmd = _commands("routine", ())[_VALIDATE_NAME]
    assert "--release" not in validate_cmd


def test_routine_battery_never_includes_the_release_step() -> None:
    for dirty in ((), ("data/agent-index.json",)):
        assert "validate_repo --release --strict-reports" not in _names("routine", dirty)


def test_routine_battery_requires_the_dirty_path_set() -> None:
    """dirty=None must fail closed, never silently guess a composition."""
    with pytest.raises(ValueError):
        settle.battery_for_tier("routine")


def test_full_battery_includes_pytest_and_validation_unconditionally() -> None:
    names = _names("full")
    assert _PYTEST_NAME in names
    assert _VALIDATE_NAME in names
    assert _PYTEST_NAME not in _names("fast")


def test_full_battery_extends_the_routine_battery_with_pytest() -> None:
    """full interleaves pytest before validation; routine drops exactly that step."""
    routine = settle.battery_for_tier("routine", ())
    full = settle.battery_for_tier("full")
    assert settle._FULL_STEPS == settle._FAST_STEPS + (
        settle._PYTEST_STEP,
        settle._VALIDATE_STANDARD_STEP,
    )
    assert routine == settle._FAST_STEPS + (settle._VALIDATE_STANDARD_STEP,)
    assert [name for name, _ in full] == [
        name for name, _ in settle._FAST_STEPS
    ] + [_PYTEST_NAME, _VALIDATE_NAME]
    assert _PYTEST_NAME not in _names("routine", ())


# --- the payload-dirty fail-closed rule ------------------------------------


@pytest.mark.parametrize(
    ("dirty", "label"),
    [
        (("data/artworks.json",), "data/"),
        (("code/src/x.py",), "code/"),
        (("code/tests/test_x.py",), "code/tests/"),
        (("docs/operations/settle.md",), "docs/"),
        (("reports/live_site_verification_2026-09-16.json",), "receipt"),
        (("data/agent-index.json", "some/unclassified/path.txt"), "control+leftover mix"),
    ],
)
def test_routine_battery_fails_closed_on_payload_dirty(
    dirty: tuple[str, ...], label: str
) -> None:
    """Payload changes must ride full tier; the routine battery refuses them."""
    with pytest.raises(ValueError):
        _names("routine", dirty)


@pytest.mark.parametrize(
    ("dirty", "label"),
    [
        ((), "clean tree"),
        (("data/agent-index.json",), "control-only"),
        (("data/generated-manifest.json", "data/release-integrity.json"), "control set"),
    ],
)
def test_routine_battery_accepts_control_only_and_clean_trees(
    dirty: tuple[str, ...], label: str
) -> None:
    assert _PYTEST_NAME not in _names("routine", dirty), label
    assert _names("routine", dirty)[-1] == _VALIDATE_NAME, label


@pytest.mark.parametrize(
    "dirty",
    [
        ("data/agent-index.json",),
        ("data/pages-artifact-manifest.json",),
        ("reports/pages_artifact_growth_2026-09-16.json",),
        ("reports/public_source_review_2026-09-16.json",),
    ],
    ids=["agent-index", "artifact-manifest", "growth-receipt", "psr"],
)
def test_routine_battery_skips_pytest_for_control_only_changes(
    dirty: tuple[str, ...],
) -> None:
    """Control-only landings stay light: no pytest, no raise."""
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


