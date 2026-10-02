#!/usr/bin/env python3
"""Generate browsable paper-folder landing pages from data/works.json."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = REPO_ROOT / "papers"

from docxology_tools.generated_outputs import (  # noqa: E402
    generated_output_files,
    stale_output_paths,
    write_output_texts,
)
from docxology_tools.build_stamp import footer_build_stamp_html  # noqa: E402
from docxology_tools.site_nav import (  # noqa: E402
    BREADCRUMB_CSS,
    HEAD_EXTRAS,
    INTERACTIVE_SCRIPTS,
    MENU_ESC_SCRIPT,
    clip_description,
    domain_page_href,
    render_breadcrumb,
    render_nav,
)

from docxology_tools.paper_artifacts import PaperResources, source_paths  # noqa: E402
from build_work_pages import abstract_source_html, enrichment_map  # noqa: E402


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_works() -> list[dict]:
    with open(REPO_ROOT / "data" / "works.json", encoding="utf-8") as f:
        return json.load(f)["works"]


def strip_md(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[*_>#|]+", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def section(markdown: str, heading: str) -> str:
    match = re.search(rf"^##+\s+.*{re.escape(heading)}.*?$", markdown, re.I | re.M)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##+\s+", markdown[start:], re.M)
    end = start + next_heading.start() if next_heading else len(markdown)
    return markdown[start:end].strip()


def overview(folder: Path) -> str:
    readme = folder / "README.md"
    if not readme.is_file():
        return ""
    text = readme.read_text(encoding="utf-8", errors="ignore")
    raw = section(text, "Abstract") or section(text, "Overview")
    if not raw:
        lines = [line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")]
        raw = " ".join(lines[:4])
    cleaned = strip_md(raw)
    return cleaned[:900].rstrip()


def unique_doc_works(works: list[dict]) -> list[dict]:
    by_path: dict[str, dict] = {}
    for work in works:
        path = str(work.get("docs_path") or "").strip()
        if path:
            by_path.setdefault(path.rstrip("/") + "/", work)
    return [by_path[path] for path in sorted(by_path)]


def pdf_rows(folder: Path, resources: PaperResources | None = None) -> str:
    resources = resources or PaperResources.load(REPO_ROOT, folder.relative_to(REPO_ROOT).as_posix())
    if not resources.pdfs:
        return '<li class="muted">No PDF file is archived in this folder.</li>'
    rows = []
    for path in resources.pdfs:
        label = f" · {resources.primary_basis}" if path == resources.primary_pdf else ""
        rows.append(
            f'<li><a href="{h(resources.url(path, prefix="../../"))}" download="{h(path.name)}" type="application/pdf">'
            f'{h(path.name)}</a> <span class="muted">{path.stat().st_size:,} bytes{h(label)}</span></li>'
        )
    return "\n".join(rows)


def image_gallery_link(folder: Path, work_title: str = "", resources: PaperResources | None = None) -> str:
    """Return GitHub-backed image previews for the repository-only binaries."""
    resources = resources or PaperResources.load(REPO_ROOT, folder.relative_to(REPO_ROOT).as_posix())
    img_files = resources.images
    if not img_files:
        return ""
    count = len(img_files)
    # Show up to 6 thumbnail previews
    thumbs = img_files[:6]
    # Alt text names the work itself (not the folder id) so screen-reader
    # users hear what the figure belongs to.
    folder_title = work_title.strip() or folder.name
    thumb_html = '<div class="image-thumbs">'
    for img in thumbs:
        # Extract page number from filename like "page10_img1.png" or "slide1_img1.png"
        page_match = __import__('re').search(r'(page|slide)(\d+)', img.name)
        if page_match:
            alt_text = f"Figure from {folder_title}, {page_match.group(1)} {page_match.group(2)}"
        else:
            alt_text = f"Figure from {folder_title} ({img.stem})"
        raw_url = "https://raw.githubusercontent.com/docxology/docxology/main/" + \
            "/".join(quote(part) for part in (*folder.relative_to(REPO_ROOT).parts, "images", img.name))
        tree_url = "https://github.com/docxology/docxology/tree/main/" + \
            "/".join(quote(part) for part in (*folder.relative_to(REPO_ROOT).parts, "images"))
        thumb_html += f'<a href="{h(tree_url)}" class="thumb-link"><img src="{h(raw_url)}" alt="{h(alt_text)}" loading="lazy"></a>'
    thumb_html += "</div>"
    more = f' <span class="muted">+{count - 6} more</span>' if count > 6 else ""
    tree_url = "https://github.com/docxology/docxology/tree/main/" + \
        "/".join(quote(part) for part in (*folder.relative_to(REPO_ROOT).parts, "images"))
    return f'<a class="btn btn-outline" href="{h(tree_url)}">Extracted Images ({count}) — GitHub</a>{more}{thumb_html}'


def required_links(folder: Path, resources: PaperResources | None = None) -> str:
    resources = resources or PaperResources.load(REPO_ROOT, folder.relative_to(REPO_ROOT).as_posix())
    labels = [
        ("README.md", "README"),
        ("AGENTS.md", "AGENTS"),
        ("SKILL.md", "SKILL"),
        ("metadata.json", "Metadata"),
        ("full_text.md", "Extracted text"),
        ("CITATION.cff", "Citation metadata"),
    ]
    return "\n".join(
        f'<a class="btn btn-outline" href="{h(filename)}">{h(label)}</a>'
        for filename, label in labels
        if resources.file(filename)
    )


def works_canonical(work: dict) -> str:
    return f"https://danielarifriedman.com/works/{work['citation_key']}.html"


def breadcrumb_trail(work: dict) -> list[tuple[str, str]]:
    """Root-relative (label, path) breadcrumb for one paper-folder landing page."""
    return [
        ("Home", ""),
        ("Works", "works/"),
        (work["title"], f"works/{work['citation_key']}.html"),
    ]


def render_page(work: dict) -> str:
    footer_stamp = footer_build_stamp_html()
    docs_path = str(work["docs_path"]).rstrip("/")
    resources = work.get("_resources") or PaperResources.load(REPO_ROOT, docs_path)
    folder = resources.folder
    if folder is None:
        raise ValueError(f"No public source folder: {docs_path}")
    summary = work.get("_enrichment", {}).get("abstract") or "An abstract is not available in this archive."
    doi_url = f"https://doi.org/{work['doi']}" if work.get("doi") else ""
    canonical = works_canonical(work)
    domain_href = domain_page_href(work.get("domain", ""), depth=2)
    domain_label = (
        f'<a href="{domain_href}">{h(work["domain_name"])}</a>' if domain_href else h(work["domain_name"])
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{h(work['title'])} Documentation — Daniel Ari Friedman</title>
    <meta name="description" content="{h(clip_description(summary))}">
    <meta name="robots" content="noindex, follow">
    <link rel="canonical" href="{h(canonical)}">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Daniel Ari Friedman updates">
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Daniel Ari Friedman">
    <link rel="stylesheet" href="../../style.css?v=work-access-20261001">
{HEAD_EXTRAS}
    <meta property="og:type" content="article">
    <meta property="og:title" content="{h(work['title'])} Documentation">
    <meta property="og:description" content="{h(clip_description(summary))}">
    <meta property="og:url" content="{h(canonical)}">
    <meta property="og:image" content="https://danielarifriedman.com/og-publications.jpg">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{h(work['title'])} Documentation">
    <meta name="twitter:description" content="{h(clip_description(summary))}">
    <meta name="twitter:image" content="https://danielarifriedman.com/og-publications.jpg">
    <meta name="twitter:image:alt" content="{h(work['title'])}">
    <style>
        {BREADCRUMB_CSS}
    </style>
</head>
<body class="paper-page">
    <a href="#main" class="skip-link">Skip to main content</a>
{render_nav(active="works", depth=2)}
{render_breadcrumb(breadcrumb_trail(work), depth=2)}
    <header class="paper-hero">
        <p class="eyebrow">{domain_label} · {h(work['type'])} · {h(work['year'])}</p>
        <h1>{h(work['title'])}</h1>
        <p class="sub">Documentation folder for catalog row {h(work['num'])} · <a href="../../works/{h(work['citation_key'])}.html">Canonical work page</a></p>
        <div class="work-actions" role="group" aria-label="Paper source files"><a class="btn btn-outline" href="{h(resources.github_url)}">Paper folder on GitHub</a></div>
    </header>
    <main id="main" class="main">
        <section class="section">
            <div class="artifact-grid">
                <div class="artifact-card"><strong>Primary Work Page</strong><a href="../../works/{h(work['citation_key'])}.html">{h(work['citation_key'])}</a></div>
                <div class="artifact-card"><strong>DOI / Source</strong>{f'<a href="{h(doi_url)}">{h(work["doi"])}</a>' if doi_url else f'<a href="{h(work.get("url") or "../../publications.html")}">Primary source</a>'}</div>
                <div class="artifact-card"><strong>Folder</strong><span>{h(docs_path)}/</span></div>
            </div>
        </section>
        <section class="section section-alt">
            <div class="section-header"><h2>Overview</h2><p>Curated abstract when available.</p><div class="section-divider"></div></div>
            <div class="overview-box"><p>{h(summary)}</p>{abstract_source_html(work.get("_enrichment", {}), prefix="../../")}</div>
        </section>
        <section class="section">
            <div class="section-header"><h2>Artifacts</h2><p>Tracked documentation and PDFs served directly from this folder.</p><div class="section-divider"></div></div>
            <div class="artifact-grid">
                <div class="artifact-card"><strong>Documentation</strong><p>{required_links(folder, resources)}</p></div>
                <div class="artifact-card"><strong>PDF Files</strong><ul>{pdf_rows(folder, resources)}</ul></div>
                <div class="artifact-card"><strong>Extracted Content</strong><p>{image_gallery_link(folder, work['title'], resources) or '<span class="muted">No extracted figures are archived.</span>'}</p></div>
            </div>
        </section>
    </main>
    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="../../publications.html">Unified bibliography</a> · <a href="../../works/">Works index</a></p>
        {footer_stamp}
    </footer>
""" + INTERACTIVE_SCRIPTS + "\n" + MENU_ESC_SCRIPT + """</body>
</html>
"""


def render_outputs() -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    failures: list[str] = []
    visible = source_paths(REPO_ROOT)
    works = [{**work, "_resources": PaperResources.load(REPO_ROOT, work["docs_path"], visible)} for work in unique_doc_works(load_works())]
    enrichments = enrichment_map(works, visible_paths=visible)
    for work in works:
        work["_enrichment"] = enrichments[work["citation_key"]]
        try:
            path = REPO_ROOT / work["docs_path"] / "index.html"
            outputs[path] = render_page(work)
        except Exception as exc:  # noqa: BLE001 - surface every render failure
            failures.append(f"{work.get('docs_path', '?')}: {exc}")
    if failures:
        # Fail loudly instead of silently dropping a paper page: a skipped
        # render would otherwise produce a partial site and sail past --check.
        raise SystemExit("Failed to render paper pages:\n" + "\n".join(failures[:40]))
    return outputs


def validate_inputs() -> list[str]:
    errors: list[str] = []
    for work in unique_doc_works(load_works()):
        folder = REPO_ROOT / work["docs_path"]
        for filename in ["README.md", "AGENTS.md", "SKILL.md"]:
            if not (folder / filename).is_file():
                errors.append(f"{work['docs_path']}{filename} missing")
    return errors


def reconcile_outputs(
    outputs: dict[Path, str], *, repo_root: Path = REPO_ROOT, check: bool
) -> tuple[Path, ...]:
    """Check or write the complete paper-page output set safely.

    Paper-folder pages are generated release artifacts even though they share
    directories with hand-authored paper material.  The shared writer rejects
    symlinks and hard links before either an exact ``--check`` read or a write,
    so a malformed folder cannot redirect the renderer outside the checkout.
    """
    stale = stale_output_paths(outputs, repo_root=repo_root)
    if check:
        return stale
    if stale:
        write_output_texts(outputs, repo_root=repo_root)
    # Write mode has reconciled the exact managed set.  Returning the pre-write
    # drift here would make a successful write look like a failed --check and
    # breaks generator ordering whenever an upstream source update changes a
    # paper page.
    return ()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated paper-folder pages are stale")
    args = parser.parse_args()
    errors = validate_inputs()
    if errors:
        raise SystemExit("Invalid paper folders:\n" + "\n".join(errors[:120]))
    outputs = render_outputs()
    stale = [str(path.relative_to(REPO_ROOT)) for path in reconcile_outputs(outputs, check=args.check)]
    if args.check:
        expected = set(outputs)
        extra = {
            path
            for path in generated_output_files(REPO_ROOT, PAPERS_DIR, "index.html")
            if path.parent.parent == PAPERS_DIR and re.match(r"\d{4}_", path.parent.name)
        } - expected
        stale.extend(str(path.relative_to(REPO_ROOT)) for path in sorted(extra))
    if stale:
        raise SystemExit("Stale generated paper pages: " + ", ".join(stale[:20]))
    action = "checked" if args.check else "wrote"
    print(f"{action} {len(outputs)} paper folder pages")


if __name__ == "__main__":
    main()
