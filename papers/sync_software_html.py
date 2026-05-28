#!/usr/bin/env python3
"""
Rewrite software.html repo grids and data/software-ld.json from pages/SOFTWARE.md.

Usage:
    python3 sync_software_html.py           # dry-run: validate counts only
    python3 sync_software_html.py --apply   # write software.html + software-ld.json
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

from software_table import (
    SoftwareRow,
    DEFAULT_SOFTWARE_PATH,
    description_html,
    description_plain,
    iter_software_rows,
    lang_css_class,
    zenodo_url,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
SOFTWARE_HTML = REPO_ROOT / "software.html"
SOFTWARE_LD_JSON = REPO_ROOT / "data" / "software-ld.json"

LD_SYNC_BEGIN = "<!-- <SOFTWARE_LD_SYNC_BEGIN> -->"
LD_SYNC_END = "<!-- <SOFTWARE_LD_SYNC_END> -->"
LD_EXTERNAL_SCRIPT = '<script type="application/ld+json" src="/data/software-ld.json"></script>'
DOCX_GRID_BEGIN = "<!-- <SOFTWARE_DOCX_GRID_BEGIN> -->"
DOCX_GRID_END = "<!-- <SOFTWARE_DOCX_GRID_END> -->"
AII_GRID_BEGIN = "<!-- <SOFTWARE_AII_GRID_BEGIN> -->"
AII_GRID_END = "<!-- <SOFTWARE_AII_GRID_END> -->"
DOCX_FOOTER_BEGIN = "<!-- <SOFTWARE_DOCX_FOOTER_BEGIN> -->"
DOCX_FOOTER_END = "<!-- <SOFTWARE_DOCX_FOOTER_END> -->"

AII_COUNT = 32
PUBLIC_GITHUB_REPOS = 286


def load_rows() -> list[SoftwareRow]:
    return list(iter_software_rows(DEFAULT_SOFTWARE_PATH))


def split_rows(rows: list[SoftwareRow]) -> tuple[list[SoftwareRow], list[SoftwareRow]]:
    docx = [r for r in rows if r.is_docxology]
    aii = [r for r in rows if not r.is_docxology]
    return docx, aii


def validate_rows(rows: list[SoftwareRow]) -> tuple[list[SoftwareRow], list[SoftwareRow]]:
    if not rows:
        raise SystemExit("No software rows parsed")
    docx, aii = split_rows(rows)
    if len(docx) != 50:
        raise SystemExit(f"Expected 50 docxology rows, got {len(docx)}")
    if len(aii) != AII_COUNT:
        raise SystemExit(f"Expected {AII_COUNT} AII rows, got {len(aii)}")
    return docx, aii


def main_entity_object(row: SoftwareRow) -> dict:
    obj: dict = {
        "@type": "SoftwareSourceCode",
        "name": row.name,
        "description": description_plain(row.description_raw),
        "codeRepository": row.url,
        "author": {"@type": "Person", "name": "Daniel Ari Friedman"},
    }
    if row.language:
        obj["programmingLanguage"] = row.language
    zenodo = zenodo_url(row.description_raw)
    if zenodo:
        obj["sameAs"] = zenodo
    return obj


def collection_page_description(docx_count: int) -> str:
    return (
        f"{docx_count} original repositories and {AII_COUNT} catalogued "
        "Active Inference Institute contributions spanning Active Inference, "
        "entomology, and synergetics."
    )


def build_collection_page(rows: list[SoftwareRow]) -> dict:
    docx, aii = split_rows(rows)
    me = [main_entity_object(r) for r in rows]
    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Software — Daniel Ari Friedman, PhD",
        "description": collection_page_description(len(docx)),
        "author": {
            "@type": "Person",
            "name": "Daniel Ari Friedman",
            "url": "https://danielarifriedman.com/",
        },
        "mainEntity": me,
    }


def render_repo_card(row: SoftwareRow, *, show_updated: bool) -> str:
    lang = row.language or "—"
    lang_class = lang_css_class(row.language)
    updated = (
        f"<span>Updated: {html.escape(row.updated_or_year)}</span>"
        if show_updated
        else ""
    )
    return f"""            <div class="repo-card">
                <div class="repo-header">
                    <a href="{html.escape(row.url, quote=True)}" class="repo-title">{html.escape(row.name)}</a>
                    <span class="repo-stars">⭐ {row.stars}</span>
                </div>
                <p class="repo-desc">{description_html(row.description_raw)}</p>
                <div class="repo-meta"><span class="repo-lang"><span class="lang-dot lang-{lang_class}"></span>{html.escape(lang)}</span>{updated}</div>
            </div>"""


def render_docx_grid(rows: list[SoftwareRow]) -> str:
    return "\n".join(render_repo_card(r, show_updated=True) for r in rows)


def render_aii_grid(rows: list[SoftwareRow]) -> str:
    return "\n".join(render_repo_card(r, show_updated=False) for r in rows)


def render_docx_footer(docx_count: int) -> str:
    return (
        f'        <p class="text-center mt-2">'
        f'<a href="https://github.com/docxology" class="filter-btn">'
        f"View all {docx_count} original repositories on GitHub</a> "
        f'<a href="repositories.html" class="filter-btn">Search full generated inventory</a></p>'
    )


def replace_between_markers(text: str, begin: str, end: str, replacement: str) -> str:
    pattern = re.escape(begin) + r"[\s\S]*?" + re.escape(end)
    if begin not in text or end not in text:
        raise ValueError(f"Missing markers {begin} / {end} in software.html")
    return re.sub(pattern, f"{begin}\n{replacement}\n        {end}", text, count=1)


def external_ld_marker_block() -> str:
    return f"    {LD_SYNC_BEGIN}\n    {LD_EXTERNAL_SCRIPT}\n    {LD_SYNC_END}"


def remove_inline_collection_ld(html_text: str) -> str:
    start_tag = '<script type="application/ld+json">'
    end_tag = "</script>"
    while True:
        i0 = html_text.find(start_tag)
        if i0 < 0:
            break
        j0 = i0 + len(start_tag)
        i1 = html_text.find(end_tag, j0)
        if i1 < 0:
            break
        raw = html_text[j0:i1].strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            break
        if data.get("@type") != "CollectionPage":
            break
        html_text = html_text[:i0] + html_text[i1 + len(end_tag) :]
    return html_text


def replace_inline_collection_ld(html_text: str) -> str:
    html_text = remove_inline_collection_ld(html_text)
    marker = external_ld_marker_block()
    if LD_SYNC_BEGIN in html_text and LD_SYNC_END in html_text:
        return re.sub(
            re.escape(LD_SYNC_BEGIN) + r"[\s\S]*?" + re.escape(LD_SYNC_END),
            marker.strip(),
            html_text,
            count=1,
        )
    if LD_EXTERNAL_SCRIPT in html_text:
        return html_text
    stylesheet_match = re.search(r'<link rel="stylesheet" href="style\.css(?:\?[^"]*)?">', html_text)
    insert_at = stylesheet_match.start() if stylesheet_match else -1
    if insert_at < 0:
        insert_at = html_text.find("</head>")
    if insert_at < 0:
        raise ValueError("Could not locate insertion point for external JSON-LD in software.html")
    return html_text[:insert_at] + marker + "\n    " + html_text[insert_at:]


def replace_head_meta(html_text: str, docx_count: int) -> str:
    desc = (
        "Open-source frameworks by Daniel Ari Friedman: CEREBRUM, GNN, Thoughtseeds, P3IF. "
        f"{PUBLIC_GITHUB_REPOS} public repositories, {docx_count} owned repos, "
        f"and {AII_COUNT} catalogued AII contributions."
    )
    html_text = re.sub(
        r'(<meta name="description" content=")[^"]*(")',
        rf"\g<1>{desc}\2",
        html_text,
        count=1,
    )
    html_text = re.sub(
        r'(<meta property="og:description" content=")[^"]*(")',
        rf"\g<1>{desc}\2",
        html_text,
        count=1,
    )
    hero = (
        f"Open-Source Repositories • Python, Rust, Go, TypeScript, Julia<br>"
        f"{docx_count} owned repositories, {AII_COUNT} catalogued AII contributions, "
        f"and {PUBLIC_GITHUB_REPOS} public GitHub repositories overall."
    )
    html_text = re.sub(
        r'(<p class="sub">)[^<]*(?:<br>[^<]*)?(</p>)',
        rf"\g<1>{hero}\2",
        html_text,
        count=1,
    )
    return html_text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Write software.html and software-ld.json")
    args = parser.parse_args()

    rows = load_rows()
    docx, aii = validate_rows(rows)

    if not SOFTWARE_HTML.is_file():
        raise SystemExit(f"Missing {SOFTWARE_HTML}")

    collection = build_collection_page(rows)
    html_out = SOFTWARE_HTML.read_text(encoding="utf-8")
    html_out = replace_inline_collection_ld(html_out)
    html_out = replace_head_meta(html_out, len(docx))
    html_out = replace_between_markers(html_out, DOCX_GRID_BEGIN, DOCX_GRID_END, render_docx_grid(docx))
    html_out = replace_between_markers(html_out, AII_GRID_BEGIN, AII_GRID_END, render_aii_grid(aii))
    html_out = replace_between_markers(
        html_out, DOCX_FOOTER_BEGIN, DOCX_FOOTER_END, render_docx_footer(len(docx)).strip()
    )

    if len(collection["mainEntity"]) != len(rows):
        raise SystemExit("mainEntity length mismatch after build")

    if "49 original" in html_out.lower():
        raise SystemExit("software.html still contains stale '49 original' copy")

    if not args.apply:
        print(
            f"OK dry-run: {len(docx)} docxology + {len(aii)} AII rows, "
            f"software-ld.json would have {len(collection['mainEntity'])} mainEntity items"
        )
        return

    SOFTWARE_LD_JSON.parent.mkdir(parents=True, exist_ok=True)
    SOFTWARE_LD_JSON.write_text(
        json.dumps(collection, indent=4, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    SOFTWARE_HTML.write_text(html_out, encoding="utf-8")
    print(
        f"Wrote {SOFTWARE_LD_JSON} and {SOFTWARE_HTML} "
        f"({len(rows)} mainEntity + {len(docx)} docx cards + {len(aii)} AII cards)"
    )


if __name__ == "__main__":
    main()
