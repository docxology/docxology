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

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = REPO_ROOT / "papers"

sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from generated_outputs import (  # noqa: E402
    generated_output_files,
    stale_output_paths,
    write_output_texts,
)
from site_nav import HEAD_EXTRAS, INTERACTIVE_SCRIPTS, MENU_ESC_SCRIPT, clip_description, domain_page_href, render_nav  # noqa: E402


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


def pdf_rows(folder: Path) -> str:
    pdfs = sorted(folder.glob("*.pdf"))
    if not pdfs:
        return '<li class="muted">No PDF file is tracked in this folder.</li>'
    return "\n".join(
        f'<li><a href="{h(path.name)}">{h(path.name)}</a> <span class="muted">{path.stat().st_size:,} bytes</span></li>'
        for path in pdfs
    )


def image_gallery_link(folder: Path) -> str:
    """Return GitHub-backed image previews for the repository-only binaries."""
    images_dir = folder / "images"
    if not images_dir.is_dir():
        return ""
    img_files = sorted(
        [f for f in images_dir.iterdir() if f.is_file() and f.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif")],
        key=lambda f: f.name,
    )
    if not img_files:
        return ""
    count = len(img_files)
    # Show up to 6 thumbnail previews
    thumbs = img_files[:6]
    # Build descriptive alt text from folder name + image filename
    folder_title = folder.name
    thumb_html = '<div class="image-thumbs">'
    for img in thumbs:
        # Extract page number from filename like "page10_img1.png" or "slide1_img1.png"
        page_match = __import__('re').search(r'(?:page|slide)(\d+)', img.name)
        page_num = page_match.group(1) if page_match else img.stem
        alt_text = f"Figure from {folder_title}, page {page_num}"
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


def required_links(folder: Path) -> str:
    labels = [
        ("README.md", "README"),
        ("AGENTS.md", "AGENTS"),
        ("SKILL.md", "SKILL"),
        ("metadata.json", "Metadata"),
        ("full_text.md", "Full Text"),
    ]
    return "\n".join(
        f'<a class="btn btn-outline" href="{h(filename)}">{h(label)}</a>'
        for filename, label in labels
        if (folder / filename).is_file()
    )


def works_canonical(work: dict) -> str:
    return f"https://danielarifriedman.com/works/{work['citation_key']}.html"


def render_page(work: dict) -> str:
    docs_path = str(work["docs_path"]).rstrip("/")
    folder = REPO_ROOT / docs_path
    summary = overview(folder) or "Local documentation and source artifacts for this bibliography entry."
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
    <link rel="stylesheet" href="../../style.css?v=newspaper-glitch-20260530c">
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
        .paper-hero{{max-width:980px;margin:0 auto;text-align:center;padding:7rem 2rem 2.5rem}}
        .paper-hero h1{{font-family:Georgia,'Times New Roman',serif;font-size:clamp(2rem,4vw,3.35rem);line-height:1.12;margin-bottom:1rem}}
        .artifact-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem}}
        .artifact-card{{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1rem;line-height:1.7}}
        .artifact-card strong{{display:block;color:var(--gold);margin-bottom:.25rem}}
        .artifact-card ul{{margin-left:1.1rem}}
        .muted{{color:var(--text-muted);font-size:.86rem}}
        .overview-box{{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1.15rem;line-height:1.75;color:var(--text-secondary)}}
    </style>
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
{render_nav(active="works", depth=2)}
    <header class="paper-hero">
        <p class="eyebrow">{domain_label} · {h(work['type'])} · {h(work['year'])}</p>
        <h1>{h(work['title'])}</h1>
        <p class="sub">Documentation folder for catalog row {h(work['num'])} · <a href="../../works/{h(work['citation_key'])}.html">Canonical work page</a></p>
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
            <div class="section-header"><h2>Overview</h2><p>Extracted from the local README when available.</p><div class="section-divider"></div></div>
            <div class="overview-box"><p>{h(summary)}</p></div>
        </section>
        <section class="section">
            <div class="section-header"><h2>Artifacts</h2><p>Tracked documentation and PDFs served directly from this folder.</p><div class="section-divider"></div></div>
            <div class="artifact-grid">
                <div class="artifact-card"><strong>Documentation</strong><p>{required_links(folder)}</p></div>
                <div class="artifact-card"><strong>PDF Files</strong><ul>{pdf_rows(folder)}</ul></div>
                <div class="artifact-card"><strong>Extracted Content</strong><p>{image_gallery_link(folder) or '<span class="muted">Full text extraction pending.</span>'}</p></div>
            </div>
        </section>
    </main>
    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="../../publications.html">Unified bibliography</a> · <a href="../../works/">Works index</a></p>
    </footer>
""" + INTERACTIVE_SCRIPTS + "\n" + MENU_ESC_SCRIPT + """</body>
</html>
"""


def render_outputs() -> dict[Path, str]:
    outputs: dict[Path, str] = {}
    failures: list[str] = []
    for work in unique_doc_works(load_works()):
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
