"""Real-string contracts for shared CollectionPage JSON-LD rendering."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from collection_jsonld import display_paths, replace_inline_collection_ld  # noqa: E402


BEGIN = "<!-- <CATALOG_LD_BEGIN> -->"
END = "<!-- <CATALOG_LD_END> -->"
COLLECTION = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "Catalog"}


def _frame() -> str:
    return (
        "<head>\n"
        f"    {BEGIN}\n"
        "    {{CATALOG_INLINE_LD}}\n"
        f"    {END}\n"
        '    <link rel="stylesheet" href="style.css">\n'
        '<script type="application/ld+json">{"@type":"BreadcrumbList"}</script>\n'
        "</head>\n"
    )


def test_marked_collection_jsonld_is_idempotent_and_preserves_other_schema():
    rendered = replace_inline_collection_ld(
        _frame(),
        COLLECTION,
        begin_marker=BEGIN,
        end_marker=END,
        page_label="catalog",
        compact=False,
    )

    assert rendered.count(BEGIN) == rendered.count(END) == 1
    assert rendered.count('"@type": "CollectionPage"') == 1
    assert '"@type":"BreadcrumbList"' in rendered
    assert (
        replace_inline_collection_ld(
            rendered,
            COLLECTION,
            begin_marker=BEGIN,
            end_marker=END,
            page_label="catalog",
            compact=False,
        )
        == rendered
    )


def test_legacy_collection_after_breadcrumb_is_replaced_without_duplication():
    frame = (
        '<head><script type="application/ld+json">{"@type":"BreadcrumbList"}</script>'
        '<script type="application/ld+json">{"@type":"CollectionPage","name":"Legacy"}</script>'
        '<link rel="stylesheet" href="style.css"></head>'
    )

    rendered = replace_inline_collection_ld(
        frame,
        COLLECTION,
        begin_marker=BEGIN,
        end_marker=END,
        page_label="catalog",
        compact=True,
    )

    assert rendered.count('"@type":"CollectionPage"') == 1
    assert '"@type":"BreadcrumbList"' in rendered


def test_compact_collection_jsonld_and_relative_stale_paths(tmp_path: Path):
    root = tmp_path / "repo"
    output = root / "data" / "catalog.json"
    output.parent.mkdir(parents=True)

    rendered = replace_inline_collection_ld(
        _frame(),
        COLLECTION,
        begin_marker=BEGIN,
        end_marker=END,
        page_label="catalog",
        compact=True,
    )

    assert '<script type="application/ld+json">{"@context":"https://schema.org","@type":"CollectionPage"' in rendered
    assert display_paths((output,), root) == "data/catalog.json"


def test_duplicate_collection_jsonld_markers_fail_closed():
    with pytest.raises(ValueError, match="zero or one complete catalog JSON-LD marker pair"):
        replace_inline_collection_ld(
            _frame() + f"{BEGIN}{END}",
            COLLECTION,
            begin_marker=BEGIN,
            end_marker=END,
            page_label="catalog",
            compact=True,
        )
