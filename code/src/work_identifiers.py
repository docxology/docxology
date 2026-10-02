"""Permanent public work identifiers, independent of editable citation metadata.

``data/work-identifiers.json`` is a reviewed source, not a generated export.
Numeric IDs and citation keys remain reserved when a catalog row is retired.
Ordinary renderers never invent or rewrite identifiers; authorized intake or
``export_bibliography.py --register-new-identifiers`` allocates new rows once.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from pathlib import Path

from docxology_tools.biblio_table import BiblioRow, bibliography_rows_from_lines
from docxology_tools.generated_outputs import read_generated_output_text, write_generated_output_text

REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "data/work-identifiers.json"
SCHEMA_VERSION = "WorkIdentifierRegistry.v1"
_KEY_RE = re.compile(r"[A-Za-z][A-Za-z0-9]{0,199}\Z")
_NUM_RE = re.compile(r"[1-9][0-9]*\Z")


class WorkIdentifierError(ValueError):
    """The permanent identity source or its catalog binding is invalid."""


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise WorkIdentifierError(f"duplicate identity registry property: {key!r}")
        result[key] = value
    return result


def load_registry(path: Path = REGISTRY_PATH, *, repo_root: Path = REPO_ROOT) -> dict:
    """Read and validate active and retired reservations without writing."""
    try:
        content = read_generated_output_text(repo_root, path)
        if content is None:
            raise FileNotFoundError("missing identity registry")
        payload = json.loads(content, object_pairs_hook=_unique_object)
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkIdentifierError(f"cannot read work identity registry {path}: {exc}") from exc
    validate_registry(payload)
    return payload


def validate_registry(payload: dict) -> None:
    """Validate every reservation, including retired keys and case collisions."""
    if not isinstance(payload, dict) or payload.get("schema_version") != SCHEMA_VERSION:
        raise WorkIdentifierError(f"work identity registry must use {SCHEMA_VERSION}")
    identifiers = payload.get("identifiers")
    if not isinstance(identifiers, dict):
        raise WorkIdentifierError("work identity registry must contain identifier reservations")
    keys: dict[str, str] = {}
    for num, record in identifiers.items():
        if not isinstance(num, str) or not _NUM_RE.fullmatch(num) or not isinstance(record, dict):
            raise WorkIdentifierError(f"invalid numeric work reservation: {num!r}")
        key = record.get("citation_key")
        if not isinstance(key, str) or not _KEY_RE.fullmatch(key):
            raise WorkIdentifierError(f"unsafe citation key for work #{num}: {key!r}")
        if key.casefold() in keys:
            raise WorkIdentifierError(f"citation key collision between #{keys[key.casefold()]} and #{num}: {key}")
        keys[key.casefold()] = num
        status = record.get("status")
        if not isinstance(status, str) or status not in {"active", "retired"}:
            raise WorkIdentifierError(f"work #{num} must be active or retired")
        if status == "retired":
            reason = record.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                raise WorkIdentifierError(f"retired work #{num} requires a reason")


def validate_catalog(rows: Iterable[BiblioRow], registry: dict) -> None:
    """Require exactly one active reservation for every current catalog row."""
    nums = [str(row.num) for row in rows]
    if len(nums) != len(set(nums)):
        raise WorkIdentifierError("duplicate numeric ID in bibliography")
    identifiers = registry["identifiers"]
    for num in nums:
        if num not in identifiers:
            raise WorkIdentifierError(
                f"work #{num} has no permanent identifier; run "
                "export_bibliography.py --register-new-identifiers after reviewing the new row"
            )
        if identifiers[num]["status"] != "active":
            raise WorkIdentifierError(f"retired work #{num} cannot be reused")
    orphans = sorted(
        (num for num, record in identifiers.items() if record["status"] == "active" and num not in nums),
        key=int,
    )
    if orphans:
        raise WorkIdentifierError(
            "active work reservations have no bibliography row: " + ", ".join(orphans)
            + "; mark removed works retired with a reason, preserving their keys"
        )


def key_for_num(num: int, registry: dict) -> str:
    record = registry["identifiers"].get(str(num))
    if record is None or record["status"] != "active":
        raise WorkIdentifierError(f"work #{num} has no active permanent identifier")
    return record["citation_key"]


def initial_key(row: BiblioRow) -> str:
    """Propose the historical readable format only at first allocation."""
    words = re.findall(r"[A-Za-z0-9]+", row.title)
    stop = {"a", "an", "and", "for", "in", "of", "on", "the", "to", "with"}
    words = [word for word in words if word.lower() not in stop][:4]
    suffix = "".join(word[:1].upper() + word[1:] for word in words) or "Work"
    # A nonnumeric date is metadata, not safe filename syntax.
    year = row.year if row.year.isdigit() else "Undated"
    return f"Friedman{year}{suffix}{row.num:03d}"


def prepare_new_rows(
    rows: Iterable[BiblioRow], path: Path = REGISTRY_PATH, *, repo_root: Path = REPO_ROOT
) -> tuple[dict, list[int]]:
    """Allocate reviewed additions above every reserved ID; never rewrite keys.

    The complete candidate catalog is validated before the one source write.
    Existing rows may change title/year freely, but retirement is an explicit
    source edit and cannot be inferred from a temporarily incomplete catalog.
    """
    rows = list(rows)
    registry = load_registry(path, repo_root=repo_root)
    reservations = registry["identifiers"]
    high_water = max(map(int, reservations), default=0)
    added = []
    for row in rows:
        if str(row.num) in reservations:
            continue
        if row.num <= high_water:
            raise WorkIdentifierError(f"new work #{row.num} cannot reuse an earlier catalog ID")
        reservations[str(row.num)] = {"citation_key": initial_key(row), "status": "active"}
        added.append(row.num)
    validate_catalog(rows, registry)
    # Reuse the structural validator to catch unsafe proposed keys/collisions
    # before writing, without reading another source or temporary public file.
    validate_registry(registry)
    if added:
        registry["identifiers"] = dict(sorted(reservations.items(), key=lambda item: int(item[0])))
    return registry, added


def register_new_rows(
    rows: Iterable[BiblioRow], path: Path = REGISTRY_PATH, *, repo_root: Path = REPO_ROOT
) -> list[int]:
    """Validate the full candidate before atomically adding new reservations."""
    registry, added = prepare_new_rows(rows, path, repo_root=repo_root)
    if added:
        write_generated_output_text(repo_root, path, json.dumps(registry, indent=2, ensure_ascii=False) + "\n")
    return added


def write_catalog_with_identifiers(
    bibliography: Path, candidate: str, *, repo_root: Path = REPO_ROOT,
    expected_previous: str | None = None,
) -> list[int]:
    """Prevalidate intake and roll back its source pair on a write failure.

    Both files use contained descriptor reads and atomic inode replacement.
    No filesystem primitive commits two files atomically: a caught second
    write failure restores the first. An interrupted process may require
    source repair, which ordinary catalog/identity validation fails closed.
    """
    registry_path = repo_root / "data/work-identifiers.json"
    previous_bibliography = read_generated_output_text(repo_root, bibliography)
    previous_registry = read_generated_output_text(repo_root, registry_path)
    if previous_bibliography is None or previous_registry is None:
        raise WorkIdentifierError("intake requires existing bibliography and identity sources")
    if expected_previous is not None and previous_bibliography != expected_previous:
        raise WorkIdentifierError("bibliography changed concurrently; retry intake from fresh source")
    registry, added = prepare_new_rows(
        bibliography_rows_from_lines(candidate.splitlines()), registry_path, repo_root=repo_root
    )
    candidate_registry = json.dumps(registry, indent=2, ensure_ascii=False) + "\n"
    if read_generated_output_text(repo_root, registry_path) != previous_registry:
        raise WorkIdentifierError("identity registry changed concurrently; retry intake")
    if read_generated_output_text(repo_root, bibliography) != previous_bibliography:
        raise WorkIdentifierError("bibliography changed concurrently; retry intake from fresh source")
    if candidate == previous_bibliography:
        if added:
            write_generated_output_text(repo_root, registry_path, candidate_registry)
        return added
    write_generated_output_text(repo_root, bibliography, candidate)
    if added:
        try:
            write_generated_output_text(repo_root, registry_path, candidate_registry)
        except BaseException:
            # Never overwrite another writer's source while repairing ours.
            if read_generated_output_text(repo_root, bibliography) != candidate:
                raise WorkIdentifierError("intake failed and bibliography changed concurrently; manual source repair required") from None
            write_generated_output_text(repo_root, bibliography, previous_bibliography)
            raise
    return added


def next_catalog_num(
    rows: Iterable[BiblioRow], path: Path = REGISTRY_PATH, *, repo_root: Path = REPO_ROOT
) -> int:
    """Allocate after retired reservations too, including a retired final row."""
    registry = load_registry(path, repo_root=repo_root)
    rows = list(rows)
    validate_catalog(rows, registry)
    return max([*(int(num) for num in registry["identifiers"]), *(row.num for row in rows)], default=0) + 1
