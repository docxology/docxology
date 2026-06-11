#!/usr/bin/env python3
"""Generate browsable paper-folder landing pages from data/works.json."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = REPO_ROOT / "papers"

sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from site_nav import clip_description, render_nav  # noqa: E402


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


def required_links(folder: Path) -> str:
    labels = [
        ("README.md", "README"),
        ("AGENTS.md", "AGENTS"),
        ("SKILL.md", "SKILL"),
        ("metadata.json", "Metadata"),
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
    <meta property="og:type" content="article">
    <meta property="og:title" content="{h(work['title'])} Documentation">
    <meta property="og:description" content="{h(clip_description(summary))}">
    <meta property="og:url" content="{h(canonical)}">
    <meta property="og:image" content="https://danielarifriedman.com/og-publications.jpg">
    <style>
        .paper-hero{{max-width:980px;margin:0 auto;text-align:center;padding:7rem 2rem 2.5rem}}
        .paper-hero h1{{font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3.35rem);line-height:1.12;margin-bottom:1rem}}
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
        <p class="eyebrow">{h(work['domain_name'])} · {h(work['type'])} · {h(work['year'])}</p>
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
            </div>
        </section>
    </main>
    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="../../publications.html">Unified bibliography</a> · <a href="../../works/">Works index</a></p>
    </footer>
</body>
</html>
"""


def render_outputs() -> dict[Path, str]:
    return {REPO_ROOT / work["docs_path"] / "index.html": render_page(work) for work in unique_doc_works(load_works())}


def validate_inputs() -> list[str]:
    errors: list[str] = []
    for work in unique_doc_works(load_works()):
        folder = REPO_ROOT / work["docs_path"]
        for filename in ["README.md", "AGENTS.md", "SKILL.md"]:
            if not (folder / filename).is_file():
                errors.append(f"{work['docs_path']}{filename} missing")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated paper-folder pages are stale")
    args = parser.parse_args()
    errors = validate_inputs()
    if errors:
        raise SystemExit("Invalid paper folders:\n" + "\n".join(errors[:120]))
    outputs = render_outputs()
    stale: list[str] = []
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if args.check:
        expected = {path.resolve() for path in outputs}
        extra = {
            path.resolve()
            for path in PAPERS_DIR.glob("*/index.html")
            if re.match(r"\d{4}_", path.parent.name)
        } - expected
        stale.extend(str(path.relative_to(REPO_ROOT)) for path in sorted(extra))
    if stale:
        raise SystemExit("Stale generated paper pages: " + ", ".join(stale[:20]))
    action = "checked" if args.check else "wrote"
    print(f"{action} {len(outputs)} paper folder pages")


if __name__ == "__main__":
    main()
