#!/usr/bin/env python3
"""Generate a source-bound Blake pathway without creating a second bibliography."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORD = re.compile(r"\bBlake\b", re.IGNORECASE)
EXCLUDED = {"other_person", "no_match"}

sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

from docxology_tools.build_stamp import footer_build_stamp_html, reuse_on_disk_stamp  # noqa: E402
from docxology_tools.generated_outputs import write_output_texts  # noqa: E402
from docxology_tools.site_nav import (  # noqa: E402
    BREADCRUMB_CSS,
    HEAD_EXTRAS,
    INTERACTIVE_SCRIPTS,
    MENU_ESC_SCRIPT,
    breadcrumb_jsonld_script,
    render_breadcrumb,
)

_PAGE_TITLE = "William Blake Publication Pathway — Daniel Ari Friedman"
_DESCRIPTION = (
    "Source-bound reading pathway through William Blake treatments, quotations, and citations "
    "across the public bibliography, with DOI roles, edition caveats, and extraction coverage limits."
)
_BREADCRUMB = [("Home", ""), ("Blake pathway", "blake-pathway.html")]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_payload(root: Path = REPO_ROOT) -> dict:
    works = json.loads((root / "data/works.json").read_text())["works"]
    review = json.loads((root / "data/blake-review.json").read_text())
    discovery_path = root / review["metadata_source"]
    discovery = json.loads(discovery_path.read_text())
    if discovery.get("warnings"):
        raise ValueError("Blake metadata source has unresolved API warnings")
    records = {str(x["record_id"]): x for x in discovery["zenodo_records"]}
    by_folder = {
        x["docs_path"].strip("/").split("/")[-1]: x for x in works if x["docs_path"]
    }
    decisions = review["reviews"]
    scanned = sorted((root / "papers").glob("*/full_text.md"))
    entries, exclusions, pending = [], [], []
    for path in scanned:
        folder = path.parent.name
        lines = path.read_text().splitlines()
        hits = [i + 1 for i, text in enumerate(lines) if WORD.search(text)]
        decision = decisions.get(folder)
        if not hits and decision is None:
            continue
        work = by_folder.get(folder)
        if work is None:
            raise ValueError(f"Uncatalogued full-text match: {folder}")
        if decision is None:
            pending.append(work["citation_key"])
            decision = {"relation": "needs_review", "note": "Unclassified text match"}
        else:
            if decision["full_text_sha256"] != digest(path):
                raise ValueError(f"Stale passage review: {folder}")
            if bool(hits) == (decision["relation"] == "no_match"):
                raise ValueError(
                    f"Passage classification disagrees with search: {folder}"
                )
            for anchor in decision.get("anchors", []):
                if anchor not in "\n".join(lines):
                    raise ValueError(
                        f"Missing reviewed passage anchor: {folder}: {anchor}"
                    )
        metadata_path = path.parent / "metadata.json"
        metadata = (
            json.loads(metadata_path.read_text()) if metadata_path.is_file() else {}
        )
        record_id = str(metadata.get("record_id") or "")
        record = records.get(record_id)
        metadata_verified = bool(
            record
            and work["doi"].casefold()
            in {record["doi"].casefold(), f"10.5281/zenodo.{record_id}"}
        )
        if (
            record
            and re.sub(r"\s+", " ", record["title"]).strip()
            != re.sub(r"\s+", " ", work["title"]).strip()
        ):
            raise ValueError(f"Primary title mismatch: {folder}")
        row = {
            "citation_key": work["citation_key"],
            "title": work["title"],
            "year": work["year"],
            "work_url": f"/works/{work['citation_key']}.html",
            "citation_doi": work["doi"],
            "citation_url": work["url"],
            "record_id": record_id or None,
            "version_doi": f"10.5281/zenodo.{record_id}" if record_id else None,
            "record_url": f"https://zenodo.org/records/{record_id}"
            if record_id
            else None,
            "version": record.get("version") if record else metadata.get("version"),
            "primary_metadata_matched": metadata_verified,
            "relation": decision["relation"],
            "note": decision["note"],
            "edition_note": decision.get("edition_note"),
            "full_text_path": str(path.relative_to(root)),
            "full_text_sha256": digest(path),
            "matching_lines": hits,
            "evidence_lines": decision.get("evidence_lines", hits[:1]),
            "citation_sources_independently_checked": False,
        }
        if any(line not in hits for line in row["evidence_lines"]):
            raise ValueError(f"Reviewed evidence line lacks Blake match: {folder}")
        (exclusions if row["relation"] in EXCLUDED else entries).append(row)
    missing_reviews = sorted(set(decisions) - {p.parent.name for p in scanned})
    if missing_reviews:
        raise ValueError(f"Reviewed text missing: {missing_reviews}")
    title_keys = {x["citation_key"] for x in works if WORD.search(x["title"])}
    if not title_keys.issubset({x["citation_key"] for x in entries}):
        raise ValueError("A Blake-titled work lacks indexed text and a passage review")
    for row in entries:
        row["title_match"] = row["citation_key"] in title_keys
        row["core_subject"] = row["title_match"] or row["relation"] == "core_subject"
    return {
        "schema_version": "BlakeIndex.v1",
        "schema_ref": "/data/agent-index.json#schemas/BlakeIndex",
        "sources": {
            "bibliography": "pages/BIBLIOGRAPHY.md",
            "works": "data/works.json",
            "reviews": "data/blake-review.json",
            "primary_metadata": review["metadata_source"],
        },
        "primary_metadata_sha256": digest(discovery_path),
        "metadata_observed_at": discovery["generated_at"],
        "method": "Case-insensitive whole-word Blake search of every local papers/*/full_text.md; hash-bound passage classifications. Title matching is a separate subset.",
        "limits": "Available text and classified passages do not establish full-paper reading or independent verification of cited editions, quotations, historical claims, or scientific findings. Missing or imperfect extractions may hide further references.",
        "count": len(entries),
        "counts": {
            "catalog_works": len(works),
            "scanned_full_texts": len(scanned),
            "title_matches": len(title_keys),
            "core_subjects": sum(x["core_subject"] for x in entries),
            "additional_text_matches": sum(not x["title_match"] for x in entries),
            "excluded_or_no_match": len(exclusions),
            "needs_review": len(pending),
        },
        "needs_review": pending,
        "works": sorted(
            entries, key=lambda x: (not x["title_match"], str(x["year"]), x["title"])
        ),
        "exclusions": exclusions,
    }


def render_markdown(payload: dict) -> str:
    counts = payload["counts"]
    text = [
        "# William Blake publication pathway",
        "",
        "<!-- Generated by code/orchestrators/build_blake_index.py; edit bibliography, paper metadata, or data/blake-review.json. -->",
        "",
        "[Complete bibliography](BIBLIOGRAPHY.md) · [Styled pathway page](../blake-pathway.html) · [Current catalog totals](../reports/current_counts.md) · [Machine-readable pathway](../data/blake-index.json) · [Blake corpus and search repository](https://github.com/docxology/blake)",
        "",
        "This pathway references the existing bibliography identities. Citation DOIs identify the curated work; version DOIs and Zenodo record links identify a particular deposited artifact. A concept DOI may resolve to a newer version. An absent version label means the API did not supply one; consult the record page.",
        "",
        f"The current scan covers **{counts['catalog_works']} catalog works** and **{counts['scanned_full_texts']} local full texts**: **{counts['title_matches']} Blake-titled works**, **{counts['additional_text_matches']} additional William Blake text matches**, and **{counts['needs_review']} unclassified matches**. These are indexing counts, not counts of papers read.",
        "",
        "## Core treatments",
        "",
        "| Work | Curated citation DOI | Version DOI / primary source | API version |",
        "| --- | --- | --- | --- |",
    ]
    for row in payload["works"]:
        if row["core_subject"]:
            title = row["title"].replace("|", "\\|")
            text.append(
                f"| [{title}](..{row['work_url']}) | [{row['citation_doi']}]({row['citation_url']}) | [{row['version_doi']}]({row['record_url']}) | {row['version'] or 'unspecified'} |"
            )
    text += [
        "",
        "Core-subject classification also covers works whose subtitle or content explicitly develops Blake, even when the short catalog title omits his name.",
        "",
        "## Related and peripheral passages",
        "",
        "The relation describes the located passage, including short quotations, references to another work, and program or catalog mentions. It does not classify the whole paper as Blake scholarship.",
        "",
        "| Work | Passage relation | Text evidence |",
        "| --- | --- | --- |",
    ]
    for row in payload["works"]:
        if not row["core_subject"]:
            line = row["evidence_lines"][0]
            url = f"https://github.com/docxology/docxology/blob/main/{row['full_text_path']}?plain=1#L{line}"
            text.append(
                f"| [{row['title']}](..{row['work_url']}) | {row['note']} | [text, line {line}]({url}) |"
            )
    text += [
        "",
        f"The pathway classifies **{counts['core_subjects']} core treatments** and **{payload['count'] - counts['core_subjects']} related or peripheral works**. Core classification and title matching are separate fields in the JSON.",
        "",
        "## Deposited versions and printed DOI discrepancies",
        "",
        "Printed cover or slide identifiers are preserved in the extraction. They can differ from registry version metadata and must not silently replace it.",
        "",
    ]
    for row in payload["works"]:
        if row["edition_note"]:
            text.append(f"- **{row['title']}**: {row['edition_note']}")
    text += ["", "## Exclusions and search gaps", ""]
    for row in payload["exclusions"]:
        text.append(f"- [{row['title']}](..{row['work_url']}): {row['note']}")
    text += [
        "",
        "## Evidence and verification boundaries",
        "",
        "- Every included work has metadata and a local extracted full text; matching line numbers and text SHA-256 values are retained in the JSON pathway.",
        "- Passage classifications are bound to the reviewed text hash. Changed text requires renewed classification; new unclassified matches fail the check.",
        f"- Primary publication metadata was compared with [the public discovery snapshot](../{payload['sources']['primary_metadata']}) observed {payload['metadata_observed_at']}; the JSON records metadata-match status per work.",
        "- Located passages are distinct from sections read, complete texts read, and independently checked citation sources. This index makes no full-reading or independent citation-validation claim.",
        "- The search is limited to available local extractions. The [source coverage queue](../data/coverage-exceptions.json) identifies missing full text; image-only, OCR, spelling and edition differences can conceal further references.",
        "- Rebuild with `uv run python code/orchestrators/build_blake_index.py`; verify with the same command plus `--check`. The ordinary regeneration and validation plan includes this check.",
        "",
    ]
    return "\n".join(text)


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _webpage_ld(payload: dict) -> dict:
    """WebPage JSON-LD with a data-derived (not hardcoded) dateModified."""
    modified = str(payload.get("metadata_observed_at", ""))[:10]
    return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "@id": "https://danielarifriedman.com/blake-pathway.html#page",
        "name": _PAGE_TITLE,
        "description": _DESCRIPTION,
        "url": "https://danielarifriedman.com/blake-pathway.html",
        "dateModified": modified,
        "isPartOf": {"@id": "https://danielarifriedman.com/#website"},
    }


def _head_extra(payload: dict) -> str:
    return (
        f"    <style>{BREADCRUMB_CSS}</style>\n"
        f'    <script type="application/ld+json">\n{json.dumps(_webpage_ld(payload), indent=4, ensure_ascii=False)}\n    </script>\n'
        f"{breadcrumb_jsonld_script(_BREADCRUMB)}\n"
    )


def render_html(payload: dict) -> str:
    counts = payload["counts"]
    footer_stamp = footer_build_stamp_html()
    core_rows = []
    for row in payload["works"]:
        if not row["core_subject"]:
            continue
        core_rows.append(
            "<tr>"
            f'<td><a href="{_esc(row["work_url"])}">{_esc(row["title"])}</a></td>'
            f'<td><a href="{_esc(row["citation_url"])}">{_esc(row["citation_doi"])}</a></td>'
            f'<td><a href="{_esc(row["record_url"])}">{_esc(row["version_doi"])}</a></td>'
            f"<td>{_esc(row['version'] or 'unspecified')}</td>"
            "</tr>"
        )
    related_rows = []
    for row in payload["works"]:
        if row["core_subject"]:
            continue
        line = row["evidence_lines"][0]
        url = f"https://github.com/docxology/docxology/blob/main/{row['full_text_path']}?plain=1#L{line}"
        related_rows.append(
            "<tr>"
            f'<td><a href="{_esc(row["work_url"])}">{_esc(row["title"])}</a></td>'
            f"<td>{_esc(row['note'])}</td>"
            f'<td><a href="{_esc(url)}">text, line {line}</a></td>'
            "</tr>"
        )
    edition_items = [
        f"<li><strong>{_esc(row['title'])}</strong>: {_esc(row['edition_note'])}</li>"
        for row in payload["works"]
        if row["edition_note"]
    ]
    exclusion_items = [
        f'<li><a href="{_esc(row["work_url"])}">{_esc(row["title"])}</a>: {_esc(row["note"])}</li>'
        for row in payload["exclusions"]
    ]
    boundaries = [
        "Every included work has metadata and a local extracted full text; matching line numbers and text SHA-256 values are retained in the JSON pathway.",
        "Passage classifications are bound to the reviewed text hash. Changed text requires renewed classification; new unclassified matches fail the check.",
        f'Primary publication metadata was compared with <a href="/{payload["sources"]["primary_metadata"]}">the public discovery snapshot</a> observed {_esc(payload["metadata_observed_at"])}; the JSON records metadata-match status per work.',
        "Located passages are distinct from sections read, complete texts read, and independently checked citation sources. This index makes no full-reading or independent citation-validation claim.",
        'The search is limited to available local extractions. The <a href="/data/coverage-exceptions.json">source coverage queue</a> identifies missing full text; image-only, OCR, spelling and edition differences can conceal further references.',
        "Rebuild with <code>uv run python code/orchestrators/build_blake_index.py</code>; verify with the same command plus <code>--check</code>. The ordinary regeneration and validation plan includes this check.",
    ]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_PAGE_TITLE}</title>
    <meta name="description" content="{_DESCRIPTION}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://danielarifriedman.com/blake-pathway.html">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    {HEAD_EXTRAS}
    <meta property="og:type" content="website">
    <meta property="og:title" content="{_PAGE_TITLE}">
    <meta property="og:description" content="Source-bound William Blake reading pathway across the public bibliography.">
    <meta property="og:url" content="https://danielarifriedman.com/blake-pathway.html">
    <meta property="og:image" content="https://danielarifriedman.com/og-cite-verify.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:image:alt" content="William Blake Publication Pathway — Daniel Ari Friedman">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{_PAGE_TITLE}">
    <meta name="twitter:description" content="Source-bound William Blake reading pathway across the public bibliography.">
    <meta name="twitter:image" content="https://danielarifriedman.com/og-cite-verify.jpg">
    <meta name="twitter:image:alt" content="William Blake Publication Pathway — Daniel Ari Friedman">
    <link rel="stylesheet" href="style.css?v=site-20261002b">
    <style>
        .pathway-table{{width:100%;border-collapse:collapse;font-size:.86rem}}
        .pathway-table caption{{caption-side:top;text-align:left;font-weight:600;padding:.4rem 0}}
        .pathway-table th,.pathway-table td{{border:1px solid var(--border);padding:.5rem;text-align:left;vertical-align:top}}
        .pathway-table th{{background:var(--bg-card)}}
        .pathway-table td{{overflow-wrap:anywhere}}
    </style>
{_head_extra(payload)}</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
    <nav role="navigation" aria-label="Main navigation">
        <a href="index.html" class="nav-logo">Daniel Ari Friedman</a>
        <button class="menu-btn" aria-label="Toggle menu" aria-expanded="false">☰</button>
        <div class="nav-links">
            <a href="publications.html">Publications</a>
            <a href="catalog.html">Data Catalog</a>
            <a href="cite-verify.html">Cite &amp; Verify</a>
            <a href="discovery.html">Discovery</a>
            <a href="data/agent-index.json">Agent Map</a>
        </div>
    </nav>
{render_breadcrumb(_BREADCRUMB)}
    <header class="page-hero">
        <h1>William Blake publication pathway</h1>
        <p class="sub">Core treatments, related passages, DOI roles, edition caveats, and extraction coverage limits — bound to the reviewed full-text hashes in <a href="/data/blake-index.json">data/blake-index.json</a>.</p>
    </header>
    <main id="main" class="main">
        <section class="section">
            <p>This pathway references the existing bibliography identities. Citation DOIs identify the curated work; version DOIs and Zenodo record links identify a particular deposited artifact. A concept DOI may resolve to a newer version. An absent version label means the API did not supply one; consult the record page.</p>
            <p>The current scan covers <strong>{counts["catalog_works"]} catalog works</strong> and <strong>{counts["scanned_full_texts"]} local full texts</strong>: <strong>{counts["title_matches"]} Blake-titled works</strong>, <strong>{counts["additional_text_matches"]} additional William Blake text matches</strong>, and <strong>{counts["needs_review"]} unclassified matches</strong>. These are indexing counts, not counts of papers read.</p>
            <h2>Core treatments</h2>
            <table class="pathway-table">
                <thead><tr><th>Work</th><th>Curated citation DOI</th><th>Version DOI / primary source</th><th>API version</th></tr></thead>
                <tbody>
{chr(10).join(core_rows)}
                </tbody>
            </table>
            <p>Core-subject classification also covers works whose subtitle or content explicitly develops Blake, even when the short catalog title omits his name.</p>
            <h2>Related and peripheral passages</h2>
            <p>The relation describes the located passage, including short quotations, references to another work, and program or catalog mentions. It does not classify the whole paper as Blake scholarship.</p>
            <table class="pathway-table">
                <thead><tr><th>Work</th><th>Passage relation</th><th>Text evidence</th></tr></thead>
                <tbody>
{chr(10).join(related_rows)}
                </tbody>
            </table>
            <p>The pathway classifies <strong>{counts["core_subjects"]} core treatments</strong> and <strong>{payload["count"] - counts["core_subjects"]} related or peripheral works</strong>. Core classification and title matching are separate fields in the JSON.</p>
            <h2>Deposited versions and printed DOI discrepancies</h2>
            <p>Printed cover or slide identifiers are preserved in the extraction. They can differ from registry version metadata and must not silently replace it.</p>
            <ul>
{chr(10).join(edition_items)}
            </ul>
            <h2>Exclusions and search gaps</h2>
            <ul>
{chr(10).join(exclusion_items)}
            </ul>
            <h2>Evidence and verification boundaries</h2>
            <ul>
{chr(10).join(f"                <li>{item}</li>" for item in boundaries)}
            </ul>
            <p><a class="btn btn-outline" href="/publications.html">Complete bibliography</a> <a class="btn btn-outline" href="/reports/current_counts.md">Current catalog totals</a> <a class="btn btn-outline" href="/data/blake-index.json">Machine-readable pathway</a> <a class="btn btn-outline" href="https://github.com/docxology/blake">Blake corpus and search repository</a> <a class="btn btn-outline" href="https://github.com/docxology/docxology/blob/main/pages/BLAKE.md">Markdown source</a></p>
        </section>
    </main>
    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="https://danielarifriedman.com/">danielarifriedman.com</a></p>
        {footer_stamp}
    </footer>
{INTERACTIVE_SCRIPTS}
{MENU_ESC_SCRIPT}</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = build_payload()
    html_out = REPO_ROOT / "blake-pathway.html"
    existing_html = html_out.read_text(encoding="utf-8") if html_out.exists() else None
    html_body = reuse_on_disk_stamp(render_html(payload), existing_html)
    outputs = {
        REPO_ROOT / "data/blake-index.json": json.dumps(
            payload, indent=2, ensure_ascii=False
        )
        + "\n",
        REPO_ROOT / "pages/BLAKE.md": render_markdown(payload),
        html_out: html_body,
    }
    if args.check:
        stale = [
            p.relative_to(REPO_ROOT).as_posix()
            for p, body in outputs.items()
            if not p.is_file() or p.read_text() != body
        ]
        if stale or payload["needs_review"]:
            print(
                f"Blake index needs review or regeneration: {stale}; unclassified: {payload['needs_review']}"
            )
            return 1
    else:
        write_output_texts(outputs, repo_root=REPO_ROOT)
    print(f"Blake index: {payload['counts']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
