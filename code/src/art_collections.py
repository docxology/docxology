"""Curated art-collection (themed hub) definitions and matching.

Source of truth: [`pages/ART_COLLECTIONS.md`](../../pages/ART_COLLECTIONS.md) —
one row per generated collection page under ``art-collections/<slug>.html``.
A work joins a collection when any of its Flickr tags (normalized: lowercased,
spaces removed) appears in the row's Tags column, or when any Title keyword
phrase occurs in the work title. Matching is pure text, so the generator stays
deterministic and the curated file stays reviewable.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "pages" / "ART_COLLECTIONS.md"


@dataclass(frozen=True)
class ArtCollection:
    slug: str
    title: str
    intro: str
    tags: frozenset[str]
    keywords: tuple[str, ...]


def normalize_tag(tag: str) -> str:
    """Flickr tag as stored in artworks.json -> matching key (lowercase, no spaces)."""
    return re.sub(r"\s+", "", str(tag or "").lower())


def parse_row_cells(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [cell.strip() for cell in cells]


def _split_list(cell: str) -> list[str]:
    return [part.strip() for part in cell.split(",") if part.strip()]


def load_collections(source: Path = SOURCE) -> list[ArtCollection]:
    """Parse the pipe table; raise on structural drift so curation stays loud."""
    lines = [line for line in source.read_text(encoding="utf-8").splitlines()]
    header_idx = next(i for i, line in enumerate(lines) if line.strip().startswith("| Slug |"))
    separator_idx = header_idx + 1
    if not re.match(r"^\s*\|[\s\-|]+\|\s*$", lines[separator_idx]):
        raise ValueError(f"{source}: malformed table separator after the Slug header row")
    collections: list[ArtCollection] = []
    slugs: set[str] = set()
    for line in lines[separator_idx + 1 :]:
        if not line.strip().startswith("|"):
            break
        cells = parse_row_cells(line)
        if len(cells) != 5:
            raise ValueError(f"{source}: expected 5 columns (Slug, Title, Intro, Tags, Title keywords), got {len(cells)}: {line[:80]}")
        slug, title, intro, tags_cell, keywords_cell = cells
        if not slug or not title or not intro:
            raise ValueError(f"{source}: slug, title, and intro are required: {line[:80]}")
        if slug in slugs:
            raise ValueError(f"{source}: duplicate collection slug {slug!r}")
        slugs.add(slug)
        collections.append(
            ArtCollection(
                slug=slug,
                title=title,
                intro=intro,
                tags=frozenset(normalize_tag(tag) for tag in _split_list(tags_cell)),
                keywords=tuple(keyword.lower() for keyword in _split_list(keywords_cell)),
            )
        )
    if not collections:
        raise ValueError(f"{source}: no collection rows parsed")
    return collections


def members_for(collection: ArtCollection, records: list[dict]) -> list[dict]:
    """Deterministic member list (payload order = upload-desc) for one collection."""
    return [record for record in records if _matches(record, collection)]


def _matches(record: dict, collection: ArtCollection) -> bool:
    tags = {normalize_tag(tag) for tag in record.get("tags", [])}
    return bool(tags & collection.tags) or _title_matches(record, collection)


def record_collections(record: dict, collections: list[ArtCollection]) -> list[ArtCollection]:
    """Collections whose tag set or title keywords match the record."""
    return [collection for collection in collections if _matches(record, collection)]


def _matches(record: dict, collection: ArtCollection) -> bool:
    tags = {normalize_tag(tag) for tag in record.get("tags", [])}
    return bool(tags & collection.tags) or _title_matches(record, collection)


def _title_matches(record: dict, collection: ArtCollection) -> bool:
    title = re.sub(r"\s+", " ", str(record.get("title", "")).lower())
    return any(keyword in title for keyword in collection.keywords)
