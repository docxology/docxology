"""All search-index surfaces must agree on one `generated_at`.

`search-index.json`, its three split companions, and bounded preview are written together, but
`--check` re-renders all surfaces pinned to the timestamp it reads out of
`search-index.json`. So if a write ever stamps the companions with a different
clock reading, the companions are stale from that moment on and no amount of
regeneration fixes them — the writer keeps reproducing the split.

That is exactly what happened: `stable_generated_at` returns None when the body
actually changed, and the None reached `render()` and `render_split()`
separately, each of which then read the clock for itself. On slow storage the
readings landed seconds apart. The repository validation gate had been red on
main since at least 2026-09-01 for this reason.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "orchestrators"))
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

import build_search_index as bsi  # noqa: E402

SURFACES = (
    REPO_ROOT / "search-index.json",
    REPO_ROOT / "search-index-core.json",
    REPO_ROOT / "search-index-content-work.json",
    REPO_ROOT / "search-index-content-video.json",
    REPO_ROOT / "search-index-bootstrap.json",
)


def test_checked_in_surfaces_share_one_generated_at():
    stamps = {
        path.name: json.loads(path.read_text(encoding="utf-8"))["generated_at"]
        for path in SURFACES
    }
    assert len(set(stamps.values())) == 1, stamps


def test_a_changed_body_still_stamps_every_surface_identically(monkeypatch):
    """The regression itself: a body change makes the reuse path return None."""
    clock = iter(["2026-01-01T00:00:00Z", "2026-01-01T00:00:03Z", "2026-01-01T00:00:06Z"])
    monkeypatch.setattr(bsi, "generated_timestamp", lambda: next(clock))
    # Force the "body changed" branch, which is the one that used to leak a None.
    monkeypatch.setattr(bsi, "stable_generated_at", lambda path, payload: None)

    candidate = json.loads(bsi.render())
    generated_at = bsi.stable_generated_at(bsi.OUT, candidate) or candidate["generated_at"]
    outputs = {bsi.OUT: bsi.render(generated_at)}
    outputs.update(bsi.render_split(generated_at))

    stamps = {json.loads(text)["generated_at"] for text in outputs.values()}
    assert stamps == {"2026-01-01T00:00:00Z"}, stamps


def test_check_mode_pins_every_surface_to_the_main_index_timestamp():
    """Why the invariant matters: check mode has one source of truth for it."""
    main_stamp = json.loads(SURFACES[0].read_text(encoding="utf-8"))["generated_at"]
    assert bsi.existing_generated_at() == main_stamp
