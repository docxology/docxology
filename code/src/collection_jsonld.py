"""Shared rendering helpers for crawler-visible CollectionPage JSON-LD.

Publication and software catalogs have different data models but the same
HTML contract: a source-owned marker pair contains exactly one synchronized
``CollectionPage`` script, while BreadcrumbList and other JSON-LD remain
untouched.  Keeping this machinery in one module prevents their check-mode
semantics from drifting apart.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
from typing import Any


def inline_collection_ld_marker_block(
    collection: dict[str, Any],
    *,
    begin_marker: str,
    end_marker: str,
    compact: bool,
) -> str:
    """Return one marked JSON-LD block, retaining each page's established layout."""
    if compact:
        payload = json.dumps(collection, ensure_ascii=False, separators=(",", ":"))
    else:
        payload = json.dumps(collection, indent=4, ensure_ascii=False)
    return (
        f"    {begin_marker}\n"
        f'    <script type="application/ld+json">{payload if compact else chr(10) + payload + chr(10) + "    "}</script>\n'
        f"    {end_marker}"
    )


def remove_inline_collection_ld(html_text: str) -> str:
    """Drop legacy inline CollectionPage JSON-LD without touching other scripts."""
    script_pattern = re.compile(
        r'<script type="application/ld\+json">(?P<payload>[\s\S]*?)</script>'
    )

    def remove_collection(match: re.Match[str]) -> str:
        raw = match.group("payload").strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)
        if isinstance(data, dict) and data.get("@type") == "CollectionPage":
            return ""
        return match.group(0)

    return script_pattern.sub(remove_collection, html_text)


def replace_inline_collection_ld(
    html_text: str,
    collection: dict[str, Any],
    *,
    begin_marker: str,
    end_marker: str,
    page_label: str,
    compact: bool,
) -> str:
    """Synchronize one marked CollectionPage block into a source-owned HTML frame."""
    html_text = remove_inline_collection_ld(html_text)
    marker = inline_collection_ld_marker_block(
        collection,
        begin_marker=begin_marker,
        end_marker=end_marker,
        compact=compact,
    )
    begin_count = html_text.count(begin_marker)
    end_count = html_text.count(end_marker)
    if begin_count != end_count or begin_count > 1:
        raise ValueError(f"Expected zero or one complete {page_label} JSON-LD marker pair")
    if begin_count == 1:
        replaced, replacement_count = re.subn(
            re.escape(begin_marker) + r"[\s\S]*?" + re.escape(end_marker),
            marker.strip(),
            html_text,
            count=1,
        )
        if replacement_count != 1:  # Defensive: marker-count checks above should guarantee this.
            raise ValueError(f"Could not replace {page_label} JSON-LD marker block")
        return replaced
    stylesheet_match = re.search(r'<link rel="stylesheet" href="style\.css(?:\?[^"]*)?">', html_text)
    insert_at = stylesheet_match.start() if stylesheet_match else -1
    if insert_at < 0:
        insert_at = html_text.find("</head>")
    if insert_at < 0:
        raise ValueError(f"Could not locate insertion point for inline JSON-LD in {page_label}.html")
    return html_text[:insert_at] + marker + "\n    " + html_text[insert_at:]


def display_paths(paths: tuple[Path, ...], repo_root: Path) -> str:
    """Render a stable, repository-relative stale-output list."""
    return ", ".join(str(path.relative_to(repo_root)) for path in paths)
