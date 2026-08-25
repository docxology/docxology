#!/usr/bin/env python3
"""
Rewrite software.html repo grids and data/software-ld.json from pages/SOFTWARE.md.

Usage:
    python3 sync_software_html.py           # dry-run: validate counts only
    python3 sync_software_html.py --check   # fail if source-rendered targets drift
    python3 sync_software_html.py --apply   # write software.html + software-ld.json
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from software_table import (  # noqa: E402
    SoftwareRow,
    DEFAULT_SOFTWARE_PATH,
    description_html,
    description_plain,
    iter_software_rows,
    lang_css_class,
    zenodo_url,
)
from count_consistency import parse_software_catalog_counts  # noqa: E402
from generated_outputs import stale_output_paths, write_output_texts  # noqa: E402

SOFTWARE_HTML = REPO_ROOT / "software.html"
SOFTWARE_LD_JSON = REPO_ROOT / "data" / "software-ld.json"
GITHUB_REPOSITORIES_JSON = REPO_ROOT / "data" / "github-repositories.json"
SOFTWARE_TEMPLATE = REPO_ROOT / "code" / "templates" / "software.html.tmpl"

LD_SYNC_BEGIN = "<!-- <SOFTWARE_LD_SYNC_BEGIN> -->"
LD_SYNC_END = "<!-- <SOFTWARE_LD_SYNC_END> -->"
DOCX_GRID_BEGIN = "<!-- <SOFTWARE_DOCX_GRID_BEGIN> -->"
DOCX_GRID_END = "<!-- <SOFTWARE_DOCX_GRID_END> -->"
AII_GRID_BEGIN = "<!-- <SOFTWARE_AII_GRID_BEGIN> -->"
AII_GRID_END = "<!-- <SOFTWARE_AII_GRID_END> -->"
DOCX_FOOTER_BEGIN = "<!-- <SOFTWARE_DOCX_FOOTER_BEGIN> -->"
DOCX_FOOTER_END = "<!-- <SOFTWARE_DOCX_FOOTER_END> -->"
SOFTWARE_TEMPLATE_TOKENS = (
    "{{SOFTWARE_INLINE_LD}}",
    "{{SOFTWARE_DOCX_GRID}}",
    "{{SOFTWARE_AII_GRID}}",
    "{{SOFTWARE_DOCX_FOOTER}}",
)


def load_rows() -> list[SoftwareRow]:
    return list(iter_software_rows(DEFAULT_SOFTWARE_PATH))


def load_source_template() -> str:
    """Load the versioned full page frame for the generated catalog output.

    The deployed HTML is an output rather than a template input.  Keeping the
    non-generated frame here makes a manual body edit observable to both
    ``--check`` and ``--apply`` instead of silently preserving it.
    """
    if not SOFTWARE_TEMPLATE.is_file():
        raise SystemExit(f"Missing source template {SOFTWARE_TEMPLATE}")
    template = SOFTWARE_TEMPLATE.read_text(encoding="utf-8")
    invalid = [token for token in SOFTWARE_TEMPLATE_TOKENS if template.count(token) != 1]
    if invalid:
        raise ValueError(
            "Software template must contain exactly one of each placeholder: "
            + ", ".join(invalid)
        )
    return template


def load_github_counts() -> dict[str, int]:
    if not GITHUB_REPOSITORIES_JSON.is_file():
        return {}
    data = json.loads(GITHUB_REPOSITORIES_JSON.read_text(encoding="utf-8"))
    counts = data.get("counts", {})
    return {k: v for k, v in counts.items() if isinstance(v, int)}


def load_github_repos_by_url() -> dict[str, dict]:
    """Map each repository html_url to its full inventory record (license, dates, topics)."""
    if not GITHUB_REPOSITORIES_JSON.is_file():
        return {}
    data = json.loads(GITHUB_REPOSITORIES_JSON.read_text(encoding="utf-8"))
    repos = data.get("repositories", data if isinstance(data, list) else [])
    return {(r.get("html_url") or "").rstrip("/"): r for r in repos if r.get("html_url")}


def split_rows(rows: list[SoftwareRow]) -> tuple[list[SoftwareRow], list[SoftwareRow]]:
    docx = [r for r in rows if r.is_docxology]
    aii = [r for r in rows if not r.is_docxology]
    return docx, aii


def validate_rows(rows: list[SoftwareRow]) -> tuple[list[SoftwareRow], list[SoftwareRow]]:
    if not rows:
        raise SystemExit("No software rows parsed")
    expected_docx, expected_aii = parse_software_catalog_counts()
    docx, aii = split_rows(rows)
    if len(docx) != expected_docx:
        raise SystemExit(f"Expected {expected_docx} docxology rows from SOFTWARE.md, got {len(docx)}")
    if len(aii) != expected_aii:
        raise SystemExit(f"Expected {expected_aii} AII rows from SOFTWARE.md, got {len(aii)}")
    return docx, aii


def main_entity_object(row: SoftwareRow, repos_by_url: dict[str, dict] | None = None) -> dict:
    obj: dict = {
        "@type": "SoftwareSourceCode",
        "@id": f"{(row.url or '').rstrip('/')}#software",
        "name": row.name,
        "description": description_plain(row.description_raw),
        "codeRepository": row.url,
        "author": {"@type": "Person", "name": "Daniel Ari Friedman"},
    }
    if row.language:
        obj["programmingLanguage"] = row.language
    repo = (repos_by_url or {}).get((row.url or "").rstrip("/"))
    if repo:
        spdx = repo.get("license")
        if spdx and spdx not in {"NOASSERTION", "NONE"}:
            obj["license"] = f"https://spdx.org/licenses/{spdx}.html"
        if repo.get("created_at"):
            obj["dateCreated"] = repo["created_at"]
        modified = repo.get("pushed_at") or repo.get("updated_at")
        if modified:
            obj["dateModified"] = modified
        topics = repo.get("topics")
        if isinstance(topics, list) and topics:
            obj["keywords"] = ", ".join(topics)
    zenodo = zenodo_url(row.description_raw)
    if zenodo:
        obj["sameAs"] = zenodo
    return obj


def collection_page_description(docx_count: int, aii_count: int) -> str:
    return (
        f"{docx_count} original repositories and {aii_count} catalogued Active Inference Institute "
        "contributions spanning Active Inference, cognitive security, computational biology, and research tools."
    )


def build_collection_page(rows: list[SoftwareRow]) -> dict:
    docx, aii = split_rows(rows)
    repos_by_url = load_github_repos_by_url()
    me = [main_entity_object(r, repos_by_url) for r in rows]
    return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Daniel Ari Friedman Software",
        "description": collection_page_description(len(docx), len(aii)),
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
    return f"""            <div class=\"repo-card\">\n                <div class=\"repo-header\">\n                    <a href=\"{html.escape(row.url, quote=True)}\" class=\"repo-title\">{html.escape(row.name)}</a>\n                    <span class=\"repo-stars\">⭐ {row.stars}</span>\n                </div>\n                <p class=\"repo-desc\">{description_html(row.description_raw)}</p>\n                <div class=\"repo-meta\"><span class=\"repo-lang\"><span class=\"lang-dot lang-{lang_class}\"></span>{html.escape(lang)}</span>{updated}</div>\n            </div>"""


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
    if text.count(begin) != 1 or text.count(end) != 1:
        raise ValueError(f"Expected exactly one marker pair {begin} / {end} in software.html")
    replaced, replacement_count = re.subn(
        pattern,
        f"{begin}\n{replacement}\n        {end}",
        text,
        count=1,
    )
    if replacement_count != 1:  # Defensive: marker-count checks above should guarantee this.
        raise ValueError(f"Could not replace markers {begin} / {end} in software.html")
    return replaced


def inline_ld_marker_block(collection: dict) -> str:
    payload = json.dumps(collection, ensure_ascii=False, separators=(",", ":"))
    return f"    {LD_SYNC_BEGIN}\n    <script type=\"application/ld+json\">{payload}</script>\n    {LD_SYNC_END}"


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


def replace_inline_collection_ld(html_text: str, collection: dict) -> str:
    html_text = remove_inline_collection_ld(html_text)
    marker = inline_ld_marker_block(collection)
    begin_count = html_text.count(LD_SYNC_BEGIN)
    end_count = html_text.count(LD_SYNC_END)
    if begin_count != end_count or begin_count > 1:
        raise ValueError("Expected zero or one complete software JSON-LD marker pair")
    if begin_count == 1:
        replaced, replacement_count = re.subn(
            re.escape(LD_SYNC_BEGIN) + r"[\s\S]*?" + re.escape(LD_SYNC_END),
            marker.strip(),
            html_text,
            count=1,
        )
        if replacement_count != 1:  # Defensive: marker-count checks above should guarantee this.
            raise ValueError("Could not replace software JSON-LD marker block")
        return replaced
    stylesheet_match = re.search(r'<link rel="stylesheet" href="style\.css(?:\?[^\"]*)?">', html_text)
    insert_at = stylesheet_match.start() if stylesheet_match else -1
    if insert_at < 0:
        insert_at = html_text.find("</head>")
    if insert_at < 0:
        raise ValueError("Could not locate insertion point for inline JSON-LD in software.html")
    return html_text[:insert_at] + marker + "\n    " + html_text[insert_at:]


def replace_head_meta(html_text: str, docx_count: int, aii_count: int, github_counts: dict[str, int]) -> str:
    public_total = github_counts.get("total")
    title = "Daniel Ari Friedman Software | Active Inference Tools"
    public_phrase = (
        f"{public_total} public repositories across docxology and AII"
        if public_total is not None
        else "generated public GitHub repository totals"
    )
    # Keep the meta/og description under ~160 chars for clean SERP snippets;
    # fuller phrasing with "across docxology and AII" remains in the hero below.
    if public_total is not None:
        desc = (
            f"Explore CEREBRUM, GNN, P3IF, MDKV, and {public_total} public repositories by "
            "Daniel Ari Friedman and AII across Active Inference and research software."
        )
    else:
        desc = (
            "Explore CEREBRUM, GNN, P3IF, MDKV, and open-source research software by "
            "Daniel Ari Friedman across Active Inference, biology, and security."
        )
    html_text = re.sub(r"<title>[^<]*</title>", f"<title>{title}</title>", html_text, count=1)
    html_text = re.sub(
        r'(<meta name="description" content=")[^"]*(")',
        rf"\g<1>{desc}\2",
        html_text,
        count=1,
    )
    html_text = re.sub(
        r'(<meta property="og:title" content=")[^"]*(")',
        rf"\g<1>{title}\2",
        html_text,
        count=1,
    )
    html_text = re.sub(
        r'(<meta property="og:image:alt" content=")[^"]*(")',
        rf"\g<1>{title}\2",
        html_text,
        count=1,
    )
    html_text = re.sub(
        r'(<meta property="og:description" content=")[^"]*(")',
        rf"\g<1>{desc}\2",
        html_text,
        count=1,
    )
    html_text = re.sub(
        r'(<meta name="twitter:title" content=")[^"]*(")',
        rf"\g<1>{title}\2",
        html_text,
        count=1,
    )
    html_text = re.sub(
        r'(<meta name="twitter:description" content=")[^"]*(")',
        rf"\g<1>{desc}\2",
        html_text,
        count=1,
    )
    hero = (
        f"Open-Source Repositories • Python, Rust, Go, TypeScript, Julia<br>"
        f"{docx_count} owned repositories, {aii_count} catalogued AII contributions, "
        f"and {public_phrase}."
    )
    html_text = re.sub(
        r'(<p class="sub">)[^<]*(?:<br>[^<]*)?(</p>)',
        rf"\g<1>{hero}\2",
        html_text,
        count=1,
    )
    return html_text


def _assert_html_summary(html_text: str, docx_count: int, aii_count: int, total_count: int) -> None:
    if f"{docx_count} owned repositories" not in html_text:
        raise SystemExit(f"software.html missing owned repository summary for {docx_count}")
    if f"{aii_count} catalogued" not in html_text:
        raise SystemExit(f"software.html missing AII catalog summary for {aii_count}")
    if f"{docx_count + aii_count} repos" in html_text:
        raise SystemExit("software.html contains unexpected hardcoded summary format")


def _assert_collection_consistency(collection: dict, rows: list[SoftwareRow]) -> None:
    main_entities = collection.get("mainEntity", [])
    if len(main_entities) != len(rows):
        raise SystemExit("mainEntity length mismatch after build")


def render_outputs_from_template(
    rows: list[SoftwareRow] | None,
    html_template: str,
) -> dict[Path, str]:
    """Render software outputs from an explicit template (test seam).

    The production renderer below always supplies the versioned source frame.
    This separation prevents check mode from reusing a generated output as a
    template simply because a caller has an HTML string available.
    """
    rows = rows if rows is not None else load_rows()
    docx, aii = validate_rows(rows)
    github_counts = load_github_counts()

    collection = build_collection_page(rows)
    html_out = replace_inline_collection_ld(html_template, collection)
    html_out = replace_head_meta(html_out, len(docx), len(aii), github_counts)
    html_out = replace_between_markers(html_out, DOCX_GRID_BEGIN, DOCX_GRID_END, render_docx_grid(docx))
    html_out = replace_between_markers(html_out, AII_GRID_BEGIN, AII_GRID_END, render_aii_grid(aii))
    html_out = replace_between_markers(
        html_out, DOCX_FOOTER_BEGIN, DOCX_FOOTER_END, render_docx_footer(len(docx)).strip()
    )

    _assert_collection_consistency(collection, rows)
    _assert_html_summary(html_out, len(docx), len(aii), len(rows))

    return {
        SOFTWARE_HTML: html_out,
        SOFTWARE_LD_JSON: json.dumps(collection, indent=4, ensure_ascii=False) + "\n",
    }


def render_outputs(rows: list[SoftwareRow] | None = None) -> dict[Path, str]:
    """Render every source-owned software target without writing it.

    The output is assembled from the versioned full-page template, the source
    catalog, and the repository inventory.  It never reads ``software.html``
    as a template, so ``--check`` catches drift in the hand-authored body frame
    as well as generated cards and JSON-LD.
    """
    return render_outputs_from_template(rows, load_source_template())


def _display_paths(paths: tuple[Path, ...]) -> str:
    return ", ".join(str(path.relative_to(REPO_ROOT)) for path in paths)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true", help="Write software.html and software-ld.json")
    mode.add_argument("--check", action="store_true", help="Fail if source-rendered software outputs are stale")
    args = parser.parse_args()

    rows = load_rows()
    docx, aii = validate_rows(rows)
    outputs = render_outputs(rows)

    if not args.apply and not args.check:
        print(
            f"OK dry-run: {len(docx)} docxology + {len(aii)} AII rows, "
            f"software-ld.json would have {len(rows)} mainEntity items"
        )
        return

    if args.check:
        stale = stale_output_paths(outputs, repo_root=REPO_ROOT)
        if stale:
            raise SystemExit(
                "Stale source-rendered software outputs: "
                f"{_display_paths(stale)} (run sync_software_html.py --apply)"
            )
        print(f"Checked {len(outputs)} software outputs from {len(rows)} catalog rows")
        return

    write_output_texts(outputs, repo_root=REPO_ROOT)
    print(
        f"Wrote {SOFTWARE_LD_JSON} and {SOFTWARE_HTML} "
        f"({len(rows)} mainEntity + {len(docx)} docx cards + {len(aii)} AII cards)"
    )


if __name__ == "__main__":
    main()
