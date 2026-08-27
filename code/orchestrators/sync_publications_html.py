#!/usr/bin/env python3
"""
Rewrite publications.html head meta and data/publications-ld.json from pages/BIBLIOGRAPHY.md.

Catalog table data loads at runtime from data/works.json (see js/publications.js).
CollectionPage JSON-LD is emitted inline in publications.html and mirrored in
data/publications-ld.json for agents and downloads.

Usage:
    python3 sync_publications_html.py           # dry-run: validate counts only
    python3 sync_publications_html.py --check   # fail if source-rendered targets drift
    python3 sync_publications_html.py --apply   # write publications.html + publications-ld.json
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
import html
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from biblio_table import DEFAULT_BIB_PATH, BiblioRow, iter_bibliography_rows  # noqa: E402
from bibliography_links import canonical_link_url  # noqa: E402
from collection_jsonld import display_paths, replace_inline_collection_ld  # noqa: E402
from export_bibliography import row_to_work, source_paths  # noqa: E402
from generated_outputs import stale_output_paths, write_output_texts  # noqa: E402
from site_facts import generated_date, generated_month_year  # noqa: E402

PUBLICATIONS_HTML = REPO_ROOT / "publications.html"
PUBLICATIONS_LD_JSON = REPO_ROOT / "data" / "publications-ld.json"
PUBLICATIONS_TEMPLATE = REPO_ROOT / "code" / "templates" / "publications.html.tmpl"

# Crawler-visible static floor: only the first N bibliography rows are
# server-rendered into <tbody id="pub-tbody">.  Non-rendering AI crawlers see
# the complete work set through the inline CollectionPage JSON-LD (one mainEntity
# per row, emitted below) and data/publications-ld.json; browsers get the full
# table from data/works.json via js/publications.js, which paginates client-side
# starting from these SSR rows.  The floor keeps raw-HTML weight bounded as the
# bibliography grows without ever replacing server rendering.
SSR_FLOOR_ROWS = 50

LD_SYNC_BEGIN = "<!-- <PUBLICATIONS_LD_SYNC_BEGIN> -->"
LD_SYNC_END = "<!-- <PUBLICATIONS_LD_SYNC_END> -->"
PUBLICATIONS_TEMPLATE_TOKENS = (
    "{{PUBLICATIONS_INLINE_LD}}",
    "{{PUBLICATIONS_STATIC_TBODY}}",
)


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


PRINCIPAL = {
    "@type": "Person",
    "@id": "https://danielarifriedman.com/#person",
    "name": "Daniel Ari Friedman",
    "sameAs": [
        "https://orcid.org/0000-0001-6232-9096",
        "https://www.wikidata.org/wiki/Q138781444",
    ],
}


def is_principal(display_name: str) -> bool:
    family, _, given = display_name.partition(",")
    return family.strip() == "Friedman" and given.strip().startswith("Daniel")


def author_entity(display_name: str) -> dict:
    """One schema.org author from a "Family, Given" (or literal) display name."""
    if is_principal(display_name):
        return PRINCIPAL
    if "," not in display_name:
        return {"@type": "Organization", "name": display_name}
    family, _, given = display_name.partition(",")
    return {"@type": "Person", "name": f"{given.strip()} {family.strip()}".strip()}


def _author_block(authors: list[str] | None = None) -> list[dict]:
    # Co-authors come from the bibliography's Authors column; where none were
    # confirmed, the principal alone is asserted, as before.
    if not authors:
        return [PRINCIPAL]
    return [author_entity(name) for name in authors]


def source_works_by_num(rows: list[BiblioRow]) -> dict[int, dict]:
    """Project each static table row directly from bibliography source and papers.

    ``data/works.json`` is itself a generated derivative.  Rendering this page
    through that derivative made a stale image/full-text flag invisible to the
    synchronizer's own ``--check``.  Reusing the exporter projection directly
    keeps the crawler-visible static table anchored to the bibliography and the
    paper directories, while ``export_bibliography.py --check`` independently
    verifies the JSON export.
    """
    visible_source_paths = source_paths()
    works = [asdict(row_to_work(row, visible_source_paths=visible_source_paths)) for row in rows]
    by_num = {work["num"]: work for work in works}
    if len(by_num) != len(rows):  # validate_rows prevents this; retain a hard guard for callers.
        raise ValueError("Duplicate bibliography row number in static table projection")
    return by_num


def main_entity_object(row: BiblioRow, same_as: str, work: dict | None = None) -> dict:
    pub_name = row.venue if row.venue else "Unknown"
    obj: dict = {
        "@type": schema_type_for_row(row.typ),
        "name": row.title,
        "headline": row.title,
        "datePublished": row.year,
        "author": _author_block(row.authors),
        "publisher": {"@type": "Organization", "name": pub_name},
        "keywords": row.domain,
    }
    if work and work.get("citation_key"):
        canonical = f"https://danielarifriedman.com/works/{work['citation_key']}.html"
        obj["@id"] = f"{canonical}#work"
        obj["url"] = canonical
        obj["mainEntityOfPage"] = canonical
        if work.get("doi"):
            obj["identifier"] = {
                "@type": "PropertyValue",
                "propertyID": "DOI",
                "value": work["doi"],
                "url": f"https://doi.org/{work['doi']}",
            }
    if same_as:
        obj["sameAs"] = same_as
    if work:
        from build_work_pages import citation_text
        cite = citation_text(work)
        if cite:
            obj["citation"] = cite
        if work.get("license"):
            obj["license"] = work["license"]
    return obj


def collection_page_description(count: int) -> str:
    return (
        f"Complete bibliography of {count} works by Daniel Ari Friedman across Active Inference, "
        "entomology, cognitive security, art, computational biology, and genetics."
    )


def load_source_template() -> str:
    """Load the versioned page frame that defines the complete HTML output.

    ``publications.html`` is a generated artifact, never an input.  The
    template contains only hand-authored framing plus explicit placeholders for
    the JSON-LD and static table regions rendered below.  This prevents a
    mutated output body from becoming the next check-mode template.
    """
    if not PUBLICATIONS_TEMPLATE.is_file():
        raise SystemExit(f"Missing source template {PUBLICATIONS_TEMPLATE}")
    template = PUBLICATIONS_TEMPLATE.read_text(encoding="utf-8")
    missing = [token for token in PUBLICATIONS_TEMPLATE_TOKENS if template.count(token) != 1]
    if missing:
        raise ValueError(
            "Publication template must contain exactly one of each placeholder: "
            + ", ".join(missing)
        )
    return template


def build_collection_page(rows: list[BiblioRow], works_by_num: dict[int, dict] | None = None) -> dict:
    count = len(rows)
    works_by_num = works_by_num if works_by_num is not None else source_works_by_num(rows)
    me = [main_entity_object(r, canonical_link_url(r.link_cell, r.venue), works_by_num.get(r.num)) for r in rows]
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
        f"Browse {count} research works by Daniel Ari Friedman spanning Active Inference, "
        "computational biology, cognitive security, art, and open science."
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
    month_year = generated_month_year()
    hero = (
        f'<p class="sub">{count} works spanning Active Inference, computational entomology, '
        f'cognitive security, art &amp; synergetics, genetics, and open science — as of {month_year}</p>'
    )
    html, hero_count = re.subn(r'<p class="sub">[^<]*</p>', hero, html, count=1)
    if hero_count != 1:
        raise ValueError("Publication source template is missing the hero subtitle")
    html, revised_count = re.subn(
        r'<meta name="revised" content="[^"]*">',
        f'<meta name="revised" content="{generated_date()}">',
        html,
        count=1,
    )
    if revised_count != 1:
        raise ValueError("Publication source template is missing meta[name=revised]")
    html, footer_count = re.subn(
        r'(Data refreshed )[A-Z][a-z]+ \d{4}',
        rf"\g<1>{month_year}",
        html,
        count=1,
    )
    if footer_count != 1:
        raise ValueError("Publication source template is missing its refresh footer")
    return html


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



DOMAIN_LABELS = {
    "🐜": "Entomology",
    "🧠": "Active Inference",
    "🛡": "Cognitive Security",
    "🛡️": "Cognitive Security",
    "🎨": "Art & Synergetics",
    "💻": "Computational",
    "🧬": "Genetics",
    "🌍": "AII Ecosystem",
    "🎥": "Media",
}


def type_badge_class(t: str) -> str:
    t_clean = re.sub(r"[^a-zA-Z0-9]+", "-", (t or "").strip().lower()).strip("-")
    return f"type-{t_clean}" if t_clean else "type-other"


def render_static_tbody(works: list[dict]) -> str:
    rows_html = []
    for p in works:
        title = html.escape(p.get("title", ""))
        citation_key = p.get("citation_key", "")
        work_page = f"works/{citation_key}.html" if citation_key else ""
        url = p.get("url", "")
        doi_url = f"https://doi.org/{p['doi']}" if p.get("doi") else url

        if work_page:
            title_cell = f'<a href="{html.escape(work_page)}">{title}</a>'
        elif doi_url:
            title_cell = f'<a href="{html.escape(doi_url)}" target="_blank" rel="noopener">{title}</a>'
        else:
            title_cell = title

        if p.get("doi") or (url and url.startswith("https://doi.org/")):
            primary = f'<a href="{html.escape(doi_url)}" target="_blank" rel="noopener">→ Link</a>'
        else:
            primary = '<span aria-label="No primary link">—</span>'

        docs_path = p.get("docs_path", "")
        if docs_path and p.get("has_paper_folder"):
            docs = f' <a href="https://github.com/docxology/docxology/tree/main/{html.escape(docs_path.rstrip("/" ))}" target="_blank" rel="noopener">Docs</a>'
        else:
            docs = ""

        if docs_path and p.get("has_full_text"):
            ft = f' <a href="{html.escape(docs_path.rstrip("/" ))}/full_text.md" title="Full text extraction">FT</a>'
        else:
            ft = ""

        if p.get("has_images"):
            img = ' <span class="badge-img" title="Has extracted images">🖼</span>'
        else:
            img = ""

        domain = p.get("domain", "")
        domain_label = DOMAIN_LABELS.get(domain, domain)

        row_str = (
            "<tr>"
            f'<td class="td-num">{p.get("num", "")}</td>'
            f'<td class="td-year">{p.get("year", "")}</td>'
            f'<td class="td-domain">{html.escape(domain_label)}</td>'
            f'<td class="td-type"><span class="type-badge {type_badge_class(p.get("type", ""))}">{html.escape(p.get("type", ""))}</span></td>'
            f'<td class="td-title">{title_cell}</td>'
            f'<td class="td-venue">{html.escape(p.get("venue", ""))}</td>'
            f'<td class="td-doi">{primary}{docs}{ft}{img}</td>'
            "</tr>"
        )
        rows_html.append(row_str)
    return chr(10).join(rows_html)


def replace_tbody(html_content: str, works: list[dict]) -> str:
    tbody_inner = chr(10) + render_static_tbody(works) + chr(10) + "                "
    replaced, replacement_count = re.subn(
        r'<tbody id="pub-tbody">[\s\S]*?</tbody>',
        f'<tbody id="pub-tbody">{tbody_inner}</tbody>',
        html_content,
        count=1,
    )
    if replacement_count != 1:
        raise ValueError("Missing generated publication table body #pub-tbody")
    return replaced

def render_outputs_from_template(
    rows: list[BiblioRow] | None,
    html_template: str,
) -> dict[Path, str]:
    """Render publication outputs from an explicit template (test seam).

    Production callers use :func:`render_outputs`, which loads only the
    versioned source template.  Keeping this lower-level helper separate makes
    it impossible for the CLI check to accidentally accept the generated
    output as its template again.
    """
    rows = rows if rows is not None else load_rows()
    validate_rows(rows)

    works_by_num = source_works_by_num(rows)
    collection = build_collection_page(rows, works_by_num)
    html_out = replace_inline_collection_ld(
        html_template,
        collection,
        begin_marker=LD_SYNC_BEGIN,
        end_marker=LD_SYNC_END,
        page_label="publications",
        # Compact one-line JSON-LD: identical graph (all rows as mainEntity),
        # roughly a third of the raw-HTML bytes of the indented form.
        compact=True,
    )
    html_out = replace_head_meta(html_out, len(rows))
    html_out = replace_tbody(html_out, [works_by_num[row.num] for row in rows[:SSR_FLOOR_ROWS]])

    if len(collection["mainEntity"]) != len(rows):
        raise SystemExit("mainEntity length mismatch after build")

    return {
        PUBLICATIONS_HTML: html_out,
        PUBLICATIONS_LD_JSON: json.dumps(collection, indent=4, ensure_ascii=False) + "\n",
    }


def render_outputs(rows: list[BiblioRow] | None = None) -> dict[Path, str]:
    """Render every source-owned publication target without writing it.

    The output is assembled from a versioned source template, bibliography
    rows, paper metadata, and the current-count snapshot.  It never reads
    ``publications.html`` as an input, so check mode detects drift anywhere in
    the rendered page, including hand-authored body framing.
    """
    return render_outputs_from_template(rows, load_source_template())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Write publications.html and publications-ld.json")
    mode.add_argument("--check", action="store_true", help="Fail if source-rendered publication outputs are stale")
    args = parser.parse_args()

    rows = load_rows()
    validate_rows(rows)
    outputs = render_outputs(rows)

    if not args.apply and not args.check:
        print(
            f"OK dry-run: {len(rows)} rows, "
            f"publications-ld.json would have {len(rows)} mainEntity items"
        )
        return

    if args.check:
        stale = stale_output_paths(outputs, repo_root=REPO_ROOT)
        if stale:
            raise SystemExit(
                "Stale source-rendered publication outputs: "
                f"{display_paths(stale, REPO_ROOT)} (run sync_publications_html.py --apply)"
            )
        print(f"Checked {len(outputs)} publication outputs from {len(rows)} bibliography rows")
        return

    write_output_texts(outputs, repo_root=REPO_ROOT)
    print(
        f"Wrote {PUBLICATIONS_LD_JSON} and {PUBLICATIONS_HTML} "
        f"({len(rows)} mainEntity + head meta)"
    )


if __name__ == "__main__":
    main()
