#!/usr/bin/env python3
"""
Rewrite publications.html PUBS (inline JS) and JSON-LD mainEntity from pages/BIBLIOGRAPHY.md.

Usage:
    python3 sync_publications_html.py           # dry-run: validate counts only
    python3 sync_publications_html.py --apply   # write publications.html
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from biblio_table import DEFAULT_BIB_PATH, BiblioRow, iter_bibliography_rows

REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLICATIONS_HTML = REPO_ROOT / "publications.html"

PUBS_BEGIN = "/* <PUBS_SYNC_BEGIN> */"
PUBS_END = "/* <PUBS_SYNC_END> */"


def canonical_link_url(link_cell: str, venue: str) -> str:
    """URL string for PUBS.doi / JSON-LD sameAs."""
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
    if t == "Paper":
        return "ScholarlyArticle"
    if t == "Book Chapter":
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
    return [
        {
            "@type": "Person",
            "name": "Daniel Ari Friedman",
        }
    ]


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


def _link(row: BiblioRow) -> str:
    return canonical_link_url(row.link_cell, row.venue)


def pub_js_object(row: BiblioRow, link: str) -> str:
    year = int(row.year) if row.year.isdigit() else row.year
    parts = [
        f"num:{row.num}",
        f"year:{year}",
        f"domain:{json.dumps(row.domain, ensure_ascii=False)}",
        f"type:{json.dumps(row.typ, ensure_ascii=False)}",
        f"title:{json.dumps(row.title, ensure_ascii=False)}",
        f"venue:{json.dumps(row.venue, ensure_ascii=False)}",
        f"doi:{json.dumps(link, ensure_ascii=False)}",
    ]
    return "{" + ",".join(parts) + "}"


def format_pubs_block(rows: list[BiblioRow]) -> str:
    """PUBS array plus sync markers; indentation matches publications.html <script> body."""
    ind = "    "
    lines = [ind + PUBS_BEGIN]
    first = pub_js_object(rows[0], _link(rows[0]))
    if len(rows) == 1:
        lines.append(f"{ind}const PUBS = [ {first}")
    else:
        lines.append(f"{ind}const PUBS = [ {first},")
    for r in rows[1:-1]:
        lines.append(f"{ind}    {pub_js_object(r, _link(r))},")
    if len(rows) > 1:
        lines.append(f"{ind}    {pub_js_object(rows[-1], _link(rows[-1]))}")
    lines.append(f"{ind}];")
    lines.append(ind + PUBS_END)
    return "\n".join(lines)


def splice_pubs_block(html: str, pubs_block: str) -> str:
    if PUBS_BEGIN in html and PUBS_END in html:
        return re.sub(
            re.escape(PUBS_BEGIN) + r"[\s\S]*?" + re.escape(PUBS_END),
            pubs_block,
            html,
            count=1,
        )
    m = re.search(r"(^\s*)const PUBS = \[[\s\S]*?\n\s*\];", html, re.MULTILINE)
    if not m:
        raise ValueError("Could not locate const PUBS = [...]; in publications.html")
    return html[: m.start()] + pubs_block + html[m.end() :]


def first_ld_json_script(html: str) -> tuple[int, int, dict]:
    start_tag = '<script type="application/ld+json">'
    end_tag = "</script>"
    i0 = html.find(start_tag)
    if i0 < 0:
        raise ValueError("No application/ld+json script found")
    j0 = i0 + len(start_tag)
    i1 = html.find(end_tag, j0)
    if i1 < 0:
        raise ValueError("Unclosed ld+json script")
    raw = html[j0:i1].strip()
    data = json.loads(raw)
    return j0, i1, data


def replace_main_entity(html: str, rows: list[BiblioRow]) -> str:
    j0, i1, data = first_ld_json_script(html)
    if data.get("@type") != "CollectionPage":
        raise ValueError("First JSON-LD block is not CollectionPage")
    me = [main_entity_object(r, canonical_link_url(r.link_cell, r.venue)) for r in rows]
    data["mainEntity"] = me
    new_json = json.dumps(data, indent=4, ensure_ascii=False)
    return html[:j0] + "\n" + new_json + "\n    " + html[i1:]


def load_rows() -> list[BiblioRow]:
    return list(iter_bibliography_rows(DEFAULT_BIB_PATH))


def validate_rows(rows: list[BiblioRow]) -> None:
    n = len(rows)
    if n == 0:
        raise SystemExit("No bibliography rows parsed")
    for i, r in enumerate(rows, start=1):
        if r.num != i:
            raise SystemExit(f"Row order/num mismatch at index {i}: expected num {i}, got {r.num}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write publications.html")
    args = parser.parse_args()

    rows = load_rows()
    validate_rows(rows)

    if not PUBLICATIONS_HTML.is_file():
        raise SystemExit(f"Missing {PUBLICATIONS_HTML}")

    html = PUBLICATIONS_HTML.read_text(encoding="utf-8")
    pubs_block = format_pubs_block(rows)
    html_out = replace_main_entity(html, rows)
    html_out = splice_pubs_block(html_out, pubs_block)

    _, _, data_check = first_ld_json_script(html_out)
    if len(data_check["mainEntity"]) != len(rows):
        raise SystemExit("mainEntity length mismatch after splice")

    if not args.apply:
        print(f"OK dry-run: {len(rows)} rows, mainEntity would be {len(data_check['mainEntity'])} items")
        return

    PUBLICATIONS_HTML.write_text(html_out, encoding="utf-8")
    print(f"Wrote {PUBLICATIONS_HTML} ({len(rows)} PUBS + mainEntity)")


if __name__ == "__main__":
    main()
