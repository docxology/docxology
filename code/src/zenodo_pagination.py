"""Bounded Zenodo search reads with explicit, exact completion checks.

Transport, credentials, timeouts and report ownership stay with each caller.
Only a stable exact total and that many distinct record identities establish
a complete search; partial pages and unavailable metadata raise ``ValueError``.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

MAX_ZENODO_SEARCH_PAGES = 20


@dataclass(frozen=True)
class ZenodoSearchResult:
    records: tuple[dict[str, Any], ...]
    total: int


def exact_zenodo_total(value: Any) -> int:
    """Accept legacy integer and modern exact-value totals, never estimates."""
    if isinstance(value, dict):
        if value.get("relation", "eq") != "eq":
            raise ValueError("Zenodo search total is not exact")
        value = value.get("value")
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("Zenodo search requires a nonnegative integer total")
    return value


def _record_identity(record: dict[str, Any]) -> str:
    value = record.get("id") or record.get("record_id")
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError("Zenodo search record has no valid numeric identity")
    identity = str(value)
    if not identity.isascii() or not identity.isdecimal() or int(identity) <= 0:
        raise ValueError("Zenodo search record has no valid numeric identity")
    return str(int(identity))


def fetch_zenodo_search(
    query: str,
    fetch_json: Callable[[str], Any],
    *,
    size: int = 25,
    max_pages: int = MAX_ZENODO_SEARCH_PAGES,
) -> ZenodoSearchResult:
    """Read one complete search or raise without returning partial records.

    Each request carries ``sort=mostrecent``. Totals must agree on every page;
    a concurrent collection change therefore requires a fresh observation.
    A total above the request budget fails after the first response. A full
    final page needs no speculative extra request because its total is exact.
    """
    for name, value in (("size", size), ("max_pages", max_pages)):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ValueError(f"Zenodo search {name} must be a positive integer")
    records: list[dict[str, Any]] = []
    identities: set[str] = set()
    total: int | None = None
    for page in range(1, max_pages + 1):
        params = {"q": query, "size": size, "page": page, "sort": "mostrecent"}
        payload = fetch_json("https://zenodo.org/api/records?" + urlencode(params))
        if not isinstance(payload, dict) or not isinstance(payload.get("hits"), dict):
            raise ValueError("Zenodo search response has no hits object")
        hits = payload["hits"]
        page_total = exact_zenodo_total(hits.get("total"))
        if total is None:
            total = page_total
        elif page_total != total:
            raise ValueError("Zenodo search total changed during pagination")
        if total > size * max_pages:
            raise ValueError(
                f"Zenodo search total {total} exceeds the {max_pages}-page bound"
            )
        batch = hits.get("hits")
        if not isinstance(batch, list) or len(batch) > size:
            raise ValueError("Zenodo search page must contain a bounded records list")
        for record in batch:
            if not isinstance(record, dict):
                raise ValueError("Zenodo search record is not an object")
            identity = _record_identity(record)
            if identity in identities:
                raise ValueError("Zenodo search repeated a record identity")
            identities.add(identity)
            records.append(record)
        if len(records) > total:
            raise ValueError("Zenodo search returned more records than its total")
        if len(records) == total:
            return ZenodoSearchResult(tuple(records), total)
        if len(batch) < size:
            raise ValueError(
                f"Zenodo search ended early: received {len(records)} of {total} records"
            )
    raise ValueError(f"Zenodo search reached its {max_pages}-page bound incomplete")
