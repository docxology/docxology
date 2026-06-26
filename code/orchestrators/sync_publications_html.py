#!/usr/bin/env python3
"""
Rewrite publications.html head meta and data/publications-ld.json from pages/BIBLIOGRAPHY.md.

Catalog table data loads at runtime from data/works.json (see js/publications.js).
CollectionPage JSON-LD lives in data/publications-ld.json (referenced from publications.html).

Usage:
    python3 sync_publications_html.py           # dry-run: validate counts only
    python3 sync_publications_html.py --apply   # write publications.html + publications-ld.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from biblio_table import DEFAULT_BIB_PATH, BiblioRow, iter_bibliography_rows  # noqa: E402

PUBLICATIONS_HTML = REPO_ROOT / "publications.html"
PUBLICATIONS_LD_JSON = REPO_ROOT / "data" / "publications-ld.json"

LD_SYNC_BEGIN = "<!-- <PUBLICATIONS_LD_SYNC_BEGIN> -->"
LD_SYNC_END = "<!-- <PUBLICATIONS_LD_SYNC_END> -->"
LD_EXTERNAL_SCRIPT = '<script type="application/ld+json" src="/data/publications-ld.json"></script>'


def canonical_link_url(link_cell: str, venue: str) -> str:
    """URL string for JSON-LD sameAs."""
    cell = (link_cell or "").strip()
    venue_u = venue.upper()

    m = re.search(r"\[([^\]]*)\]\((https?://[^)\s]+)\)", cell)
    if m:
        return m.group(2).rstrip(").,")

    m = re.search(r"(https?://[^\s\])>]+)", cell)
    if m:
        return m.group(1).rstrip(").,")

    doi_m = re.search(r"(10\.\d{4,}[^\s\])]*)", cell)
    if doi_m:
        slug = doi_m.group(1).rstrip(").,")
        return f"https://doi.org/{slug}"

    if re.search(r"^978[-\dXx]+$", cell) or cell.startswith("978-"):
        isbn = cell.split()[0]
        if "COGSEC" in venue_u or "COGSEC.ORG" in venue_u:
            return "https://cogsec.org"
        return f"https://www.worldcat.org/isbn/{isbn}"

    if cell in ("—", "-", ""):
        return ""

    if "UDEMY" in cell.upper() or "udemy.com" in cell.lower():
        um = re.search(r"(https?://www\.udemy\.com/[^\s)]+)", cell)
        if um:
            return um.group(1).rstrip(").,")

    return cell


def schema_type_for_row(typ: str) -> str:
    t = typ.strip()
    if t in ("Paper", "Book Chapter"):
        return "ScholarlyArticle"
    if t == "Book":
        return "Book"
    if t == "Presentation":
        return "PresentationDigitalDocument"
    if t == "Course":
        return "Course"
    if t == "Series":
        return "CreativeWorkSeries"
    if t == "Playbook":
        return "CreativeWork"
    return "ScholarlyArticle"


def _author_block() -> list[dict]:
    return [{"@type": "Person", "name": "Daniel Ari Friedman"}]


def main_entity_object(row: BiblioRow, same_as: str) -> dict:
    pub_name = row.venue if row.venue else "Unknown"
    obj: dict = {
        "@type": schema_type_for_row(row.typ),
        "headline": row.title,
        "datePublished": row.year,
        "author": _author_block(),
        "publisher": {"@type": "Organization", "name": pub_name},
        "keywords": row.domain,
    }
    if same_as:
        obj["sameAs"] = same_as
    return obj


def collection_page_description(count: int) -> str:
    return (
        f"Complete bibliography of {count} works by Daniel Ari Friedman across Active Inference, "
        "entomology, cognitive security, art, computational biology, and genetics."
    )


def build_collection_page(rows: list[BiblioRow]) -> dict:
    count = len(rows)
    me = [main_entity_object(r, canonical_link_url(r.link_cell, r.venue)) for r in rows]
    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Daniel Ari Friedman Publications",
        "description": collection_page_description(count),
        "author": {
            "@type": "Person",
            "name": "Daniel Ari Friedman",
            "url": "https://danielarifriedman.com/",
        },
        "mainEntity": me,
    }


def replace_head_meta(html: str, count: int) -> str:
    """Patch title, meta description, and og:* counts from bibliography row count."""
    title = f"Daniel Ari Friedman Publications | {count} Research Works"
    desc = (
        f"Search {count} Works across {count} catalogued works by Daniel Ari Friedman on Active Inference, "
        "computational biology, cognitive security, art, and research software."
    )
    html = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", html, count=1)
    html = re.sub(
        r'(<meta name="description" content=")[^"]*(")',
        rf"\g<1>{desc}\2",
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta property="og:title" content=")[^"]*(")',
        rf"\g<1>{title}\2",
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta property="og:image:alt" content=")[^"]*(")',
        rf"\g<1>{title}\2",
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta name="twitter:image:alt" content=")[^"]*(")',
        rf"\g<1>{title}\2",
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta property="og:description" content=")[^"]*(")',
        rf"\g<1>{desc}\2",
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta name="twitter:title" content=")[^"]*(")',
        rf"\g<1>{title}\2",
        html,
        count=1,
    )
    html = re.sub(
        r'(<meta name="twitter:description" content=")[^"]*(")',
        rf"\g<1>{desc}\2",
        html,
        count=1,
    )
    hero_sub = re.search(
        r'(<p class="sub">)\d+ works spanning',
        html,
    )
    if hero_sub:
        html = re.sub(
            r'(<p class="sub">)\d+ works spanning',
            rf"\g<1>{count} works spanning",
            html,
            count=1,
        )
    return html


def external_ld_marker_block() -> str:
    return f"    {LD_SYNC_BEGIN}\n    {LD_EXTERNAL_SCRIPT}\n    {LD_SYNC_END}"


def remove_inline_collection_ld(html: str) -> str:
    """Drop any inline CollectionPage JSON-LD block (keep BreadcrumbList and other scripts)."""
    start_tag = '<script type="application/ld+json">'
    end_tag = "</script>"
    while True:
        i0 = html.find(start_tag)
        if i0 < 0:
            break
        j0 = i0 + len(start_tag)
        i1 = html.find(end_tag, j0)
        if i1 < 0:
            break
        raw = html[j0:i1].strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            break
        if data.get("@type") != "CollectionPage":
            break
        html = html[:i0] + html[i1 + len(end_tag) :]
    return html


def replace_inline_collection_ld(html: str) -> str:
    """Ensure publications.html references external JSON-LD instead of inline mainEntity."""
    html = remove_inline_collection_ld(html)
    marker = external_ld_marker_block()
    if LD_SYNC_BEGIN in html and LD_SYNC_END in html:
        return re.sub(
            re.escape(LD_SYNC_BEGIN) + r"[\s\S]*?" + re.escape(LD_SYNC_END),
            marker.strip(),
            html,
            count=1,
        )
    if LD_EXTERNAL_SCRIPT in html:
        return html
    stylesheet_match = re.search(r'<link rel="stylesheet" href="style\.css(?:\?[^"]*)?">', html)
    insert_at = stylesheet_match.start() if stylesheet_match else -1
    if insert_at < 0:
        insert_at = html.find("</head>")
    if insert_at < 0:
        raise ValueError("Could not locate insertion point for external JSON-LD in publications.html")
    return html[:insert_at] + marker + "\n    " + html[insert_at:]


def load_rows() -> list[BiblioRow]:
    return list(iter_bibliography_rows(DEFAULT_BIB_PATH))


def validate_rows(rows: list[BiblioRow]) -> None:
    # `num` is a STABLE id embedded in each work's citation key / page URL
    # (Friedman{year}{suffix}{num:03d}), assigned append-only as max+1. Numbers must
    # be strictly increasing and unique, but gaps are allowed: removing a work leaves
    # its number retired rather than renumbering (and breaking) every later URL.
    n = len(rows)
    if n == 0:
        raise SystemExit("No bibliography rows parsed")
    prev = 0
    for i, r in enumerate(rows, start=1):
        if r.num <= prev:
            raise SystemExit(f"Row order/num mismatch at index {i}: num {r.num} not greater than previous {prev}")
        prev = r.num


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write publications.html and publications-ld.json")
    args = parser.parse_args()

    rows = load_rows()
    validate_rows(rows)

    if not PUBLICATIONS_HTML.is_file():
        raise SystemExit(f"Missing {PUBLICATIONS_HTML}")

    collection = build_collection_page(rows)
    html = PUBLICATIONS_HTML.read_text(encoding="utf-8")
    html_out = replace_inline_collection_ld(html)
    html_out = replace_head_meta(html_out, len(rows))

    if len(collection["mainEntity"]) != len(rows):
        raise SystemExit("mainEntity length mismatch after build")

    if not args.apply:
        print(
            f"OK dry-run: {len(rows)} rows, "
            f"publications-ld.json would have {len(collection['mainEntity'])} mainEntity items"
        )
        return

    PUBLICATIONS_LD_JSON.parent.mkdir(parents=True, exist_ok=True)
    PUBLICATIONS_LD_JSON.write_text(
        json.dumps(collection, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    PUBLICATIONS_HTML.write_text(html_out, encoding="utf-8")
    print(
        f"Wrote {PUBLICATIONS_LD_JSON} and {PUBLICATIONS_HTML} "
        f"({len(rows)} mainEntity + head meta)"
    )


if __name__ == "__main__":
    main()
