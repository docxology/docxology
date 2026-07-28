#!/usr/bin/env python3
"""Build the compact artwork index used by the public gallery.

The complete ``data/artworks.json`` export remains the source of truth and is
available for agents, downloads, and the lightbox detail view.  The gallery's
initial grid only needs searchable identity, thumbnail, and display metadata;
resolution maps and media URLs are fetched lazily when a visitor opens a work
or searches descriptions.  Keeping this projection generated prevents the
interactive page from paying the cost of every original-size URL up front.

Outputs: data/artworks-index.json
Sources: data/artworks.json, this orchestrator
Rebuild: python3 code/orchestrators/build_artwork_index.py (--check)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "data" / "artworks.json"
OUTPUT = REPO_ROOT / "data" / "artworks-index.json"
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

try:
    from report_paths import generated_timestamp, stable_generated_at
except ImportError:  # pragma: no cover - package import path
    from .report_paths import generated_timestamp, stable_generated_at


# Descriptions are intentionally omitted: the first keystroke in the search
# field loads the full export, while the initial grid stays small and fast.
INDEX_FIELDS = ("id", "title", "tags", "date", "views", "thumb")


def load_source() -> dict:
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("artworks"), list):
        raise ValueError(f"Invalid artwork source: {SOURCE}")
    return payload


def build_payload(source: dict) -> dict:
    artworks = [
        {field: artwork.get(field) for field in INDEX_FIELDS}
        for artwork in source["artworks"]
    ]
    return {
        "generated_at": generated_timestamp(),
        "source": "data/artworks.json",
        "count": len(artworks),
        "schema": "ArtworkIndex.v1",
        "detail_source": "data/artworks.json",
        "fields": list(INDEX_FIELDS),
        "artworks": artworks,
    }


def render(payload: dict) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


def write() -> None:
    candidate = build_payload(load_source())
    if OUTPUT.exists():
        try:
            existing = json.loads(OUTPUT.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = None
        if isinstance(existing, dict):
            previous_timestamp = stable_generated_at(OUTPUT, candidate)
            if previous_timestamp:
                candidate["generated_at"] = previous_timestamp
    OUTPUT.write_text(render(candidate), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(REPO_ROOT)} ({candidate['count']} artworks)")


def check() -> None:
    expected = build_payload(load_source())
    if not OUTPUT.exists():
        raise SystemExit(f"Missing generated artwork index: {OUTPUT}")
    try:
        actual = json.loads(OUTPUT.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid generated artwork index: {exc}") from exc
    if actual.get("generated_at"):
        expected["generated_at"] = actual["generated_at"]
    if actual != expected:
        raise SystemExit("Artwork index is stale; run build_artwork_index.py")
    print(f"checked artwork index ({actual['count']} artworks)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify the generated projection")
    args = parser.parse_args()
    check() if args.check else write()


if __name__ == "__main__":
    main()
