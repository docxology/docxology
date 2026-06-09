#!/usr/bin/env python3
"""Generate per-work HTML landing pages from data/works.json."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKS_DIR = REPO_ROOT / "works"
ENRICHMENT_OUT = REPO_ROOT / "data" / "work-enrichment.json"

sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from site_nav import render_nav  # noqa: E402

try:
    from report_paths import generated_timestamp
except ImportError:  # pragma: no cover - package import path
    from .report_paths import generated_timestamp


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
    text = re.sub(r"[<>]", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def section(markdown: str, heading: str) -> str:
    pattern = re.compile(rf"^##+\s+.*{re.escape(heading)}.*?$", re.I | re.M)
    match = pattern.search(markdown)
    if not match:
        return ""
    start = match.end()
    next_heading = re.search(r"^##+\s+", markdown[start:], re.M)
    end = start + next_heading.start() if next_heading else len(markdown)
    return markdown[start:end].strip()


def section_paragraph(markdown: str, heading: str, max_chars: int = 900) -> str:
    raw = section(markdown, heading)
    if not raw:
        return ""
    lines = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("|") or line.startswith("- ") or line.startswith("* "):
            continue
        lines.append(line)
    text = strip_md(" ".join(lines))
    return text[:max_chars].rstrip()


def bullet_section(markdown: str, heading: str, limit: int = 5) -> list[str]:
    raw = section(markdown, heading)
    items = []
    for line in raw.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            item = strip_md(stripped[2:])
            if item:
                items.append(item)
        if len(items) >= limit:
            break
    return items


def keyword_list(markdown: str, limit: int = 12) -> list[str]:
    raw = section(markdown, "Keywords")
    if not raw:
        return []
    text = strip_md(raw.replace("·", ",").replace(";", ","))
    words = [w.strip(" ,.") for w in re.split(r",|\n", text) if w.strip(" ,.")]
    seen: set[str] = set()
    out: list[str] = []
    for word in words:
        key = word.lower()
        if key not in seen:
            seen.add(key)
            out.append(word)
        if len(out) >= limit:
            break
    return out


def enrichment_for(work: dict) -> dict:
    path = work.get("docs_path")
    readme = REPO_ROOT / path / "README.md" if path else None
    skill = REPO_ROOT / path / "SKILL.md" if path else None
    source = ""
    if readme and readme.exists():
        source = readme.read_text(encoding="utf-8", errors="ignore")
    skill_text = skill.read_text(encoding="utf-8", errors="ignore") if skill and skill.exists() else ""
    abstract = section_paragraph(source, "Abstract")
    keywords = keyword_list(source) or keyword_list(skill_text)
    findings = (
        bullet_section(source, "Key Findings")
        or bullet_section(source, "Key Contributions")
        or bullet_section(skill_text, "Key Findings")
        or bullet_section(skill_text, "Key Concepts")
    )
    methods = bullet_section(source, "Methods") or bullet_section(skill_text, "Methods")
    return {
        "citation_key": work["citation_key"],
        "abstract": abstract,
        "keywords": keywords,
        "findings": findings,
        "methods": methods,
        "source": f"{path}README.md" if abstract or keywords or findings or methods else "",
    }


def enrichment_map(works: list[dict]) -> dict[str, dict]:
    return {work["citation_key"]: enrichment_for(work) for work in works}


def local_docs_link(path: str) -> str:
    return f"../{path.rstrip('/')}/" if path else "../publications.html"


def source_repository_url(docs_path: str) -> str:
    if not docs_path:
        return ""
    meta_path = REPO_ROOT / docs_path / "metadata.json"
    if not meta_path.is_file():
        return ""
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ""
    for item in meta.get("related_resources", []):
        url = item.get("url", "")
        if item.get("type") == "repository" and url.startswith("https://github.com/"):
            return url
    return ""


def citation_text(work: dict) -> str:
    venue = f" {work['venue']}." if work.get("venue") else ""
    return f"Friedman, Daniel Ari. {work['year']}. {work['title']}.{venue}"


def breadcrumb_trail(work: dict) -> list[tuple[str, str]]:
    """(label, absolute URL) pairs from site root to the current work."""
    return [
        ("Home", "https://danielarifriedman.com/"),
        ("Works", "https://danielarifriedman.com/works/"),
        (work["title"], f"https://danielarifriedman.com/works/{work['citation_key']}.html"),
    ]


def breadcrumb_json_ld(work: dict) -> str:
    items = [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
        for i, (name, url) in enumerate(breadcrumb_trail(work))
    ]
    return json.dumps(
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items},
        indent=4,
        ensure_ascii=False,
    )


def breadcrumb_html(work: dict) -> str:
    trail = breadcrumb_trail(work)
    crumbs = []
    for idx, (name, _url) in enumerate(trail):
        if idx == len(trail) - 1:
            crumbs.append(f'<li aria-current="page">{h(name)}</li>')
        else:
            href = "../index.html" if name == "Home" else "../works/"
            crumbs.append(f'<li><a href="{href}">{h(name)}</a></li>')
    return (
        '    <nav class="breadcrumb" aria-label="Breadcrumb">\n'
        f'        <ol>{"".join(crumbs)}</ol>\n'
        '    </nav>'
    )


def related_works_html(work: dict) -> str:
    related = work.get("related", [])
    if not related:
        return ""
    items = "".join(
        f'<li><a href="{h(r["citation_key"])}.html">{h(r["title"])}</a>'
        f'<span class="muted"> · {h(r["year"])}</span></li>'
        for r in related
    )
    return f"""
        <section class="section">
            <div class="section-header"><h2>Related in {h(work['domain_name'])}</h2><p>Other catalogued works in the same domain.</p><div class="section-divider"></div></div>
            <ul class="related-list">{items}</ul>
        </section>"""


def json_ld(work: dict) -> str:
    typ = "ScholarlyArticle" if work["type"] in {"Paper", "Book Chapter"} else "CreativeWork"
    enrich = work.get("enrichment", {})
    same_as = [work["url"]] if work.get("url") else []
    if work.get("doi"):
        same_as.append(f"https://doi.org/{work['doi']}")
    data = {
        "@context": "https://schema.org",
        "@type": typ,
        "@id": f"https://danielarifriedman.com/works/{work['citation_key']}.html#work",
        "name": work["title"],
        "headline": work["title"],
        "author": {"@id": "https://danielarifriedman.com/#person"},
        "datePublished": str(work["year"]),
        "url": f"https://danielarifriedman.com/works/{work['citation_key']}.html",
        "mainEntityOfPage": f"https://danielarifriedman.com/works/{work['citation_key']}.html",
        "isPartOf": {"@id": "https://danielarifriedman.com/#website"},
        "about": [
            {"@type": "DefinedTerm", "name": work["domain_name"]},
            {"@type": "DefinedTerm", "name": work["type"]},
        ],
        "genre": work["type"],
        "inLanguage": "en",
        "citation": citation_text(work),
        "sameAs": same_as,
        "image": "https://danielarifriedman.com/og-publications.jpg",
    }
    if work.get("doi"):
        data["identifier"] = [
            {"@type": "PropertyValue", "propertyID": "DOI", "value": work["doi"], "url": f"https://doi.org/{work['doi']}"},
            {"@type": "PropertyValue", "propertyID": "Citation key", "value": work["citation_key"]},
        ]
    else:
        data["identifier"] = {"@type": "PropertyValue", "propertyID": "Citation key", "value": work["citation_key"]}
    if work.get("venue"):
        data["publisher"] = {"@type": "Organization", "name": work["venue"]}
    if enrich.get("abstract"):
        data["abstract"] = enrich["abstract"]
    if enrich.get("keywords"):
        data["keywords"] = enrich["keywords"]
        data["about"].extend({"@type": "DefinedTerm", "name": keyword} for keyword in enrich["keywords"][:8])
    if enrich.get("findings") or enrich.get("methods"):
        data["description"] = " ".join([*(enrich.get("findings") or []), *(enrich.get("methods") or [])])[:700]
    if work.get("docs_path"):
        data["hasPart"] = {
            "@type": "CreativeWork",
            "name": "Local paper documentation",
            "url": f"https://github.com/docxology/docxology/tree/main/{work['docs_path'].rstrip('/')}",
        }
    return json.dumps(data, indent=4, ensure_ascii=False)


def page_head(work: dict) -> str:
    description = work.get("enrichment", {}).get("abstract") or f"{work['type']} in {work['domain_name']} by Daniel Ari Friedman, catalogued in the unified bibliography."
    description = description[:155].rstrip()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{h(work['title'])} — Daniel Ari Friedman</title>
    <meta name="description" content="{h(description)}">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://danielarifriedman.com/works/{h(work['citation_key'])}.html">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Daniel Ari Friedman updates">
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Daniel Ari Friedman">
    <link rel="alternate" type="application/json" href="/search-index.json" title="Site search index">
    <link rel="alternate" type="text/x-bibtex" href="/bibliography.bib" title="BibTeX bibliography">
    <link rel="alternate" type="application/vnd.citationstyles.csl+json" href="/bibliography.csl.json" title="CSL JSON bibliography">
    <meta property="og:type" content="article">
    <meta property="og:title" content="{h(work['title'])}">
    <meta property="og:description" content="{h(description)}">
    <meta property="og:url" content="https://danielarifriedman.com/works/{h(work['citation_key'])}.html">
    <meta property="og:image" content="https://danielarifriedman.com/og-publications.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{h(work['title'])}">
    <meta name="twitter:description" content="{h(description)}">
    <meta name="twitter:image" content="https://danielarifriedman.com/og-publications.jpg">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../style.css?v=newspaper-glitch-20260530c">
    <meta name="theme-color" content="#0c0c0e">
    <style>
        .work-hero{{max-width:960px;margin:0 auto;text-align:center;padding:7rem 2rem 2.5rem}}
        .work-hero h1{{font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3.4rem);line-height:1.12;margin-bottom:1rem}}
        .meta-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:1rem}}
        .meta-card{{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1rem}}
        .meta-card strong{{display:block;color:var(--gold);margin-bottom:.25rem}}
        .cite-box{{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1rem;line-height:1.7;color:var(--text-secondary)}}
        .work-detail{{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1.15rem;line-height:1.75;color:var(--text-secondary)}}
        .work-detail ul{{margin-left:1.2rem}}
        .keyword-row{{display:flex;flex-wrap:wrap;gap:.4rem;margin-top:.75rem}}
        .keyword-row span{{border:1px solid var(--border);border-radius:999px;padding:.2rem .55rem;color:var(--silver-bright);font-size:.76rem;background:rgba(255,255,255,.03)}}
        .breadcrumb{{max-width:960px;margin:1.4rem auto 0;padding:0 2rem}}
        .breadcrumb ol{{list-style:none;display:flex;flex-wrap:wrap;gap:.4rem;padding:0;margin:0;font-size:.8rem;color:var(--text-muted)}}
        .breadcrumb li+li::before{{content:'\\203A';margin-right:.4rem;color:var(--text-muted)}}
        .breadcrumb a{{color:var(--silver-bright);text-decoration:none}}
        .breadcrumb a:hover{{text-decoration:underline}}
        .breadcrumb [aria-current=page]{{color:var(--text-secondary)}}
        .related-list{{list-style:none;padding:0;margin:0;display:grid;gap:.5rem}}
        .related-list li{{padding:.6rem .9rem;background:var(--bg-card);border:1px solid var(--border);border-radius:8px}}
        .related-list a{{color:var(--silver-bright);text-decoration:none}}
        .related-list a:hover{{text-decoration:underline}}
    </style>
    <script type="application/ld+json">
{json_ld(work)}
    </script>
    <script type="application/ld+json">
{breadcrumb_json_ld(work)}
    </script>
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
{render_nav(active="works", depth=1)}
"""


def render_work_page(work: dict) -> str:
    doi_link = f"https://doi.org/{work['doi']}" if work.get("doi") else ""
    docs = local_docs_link(work.get("docs_path", ""))
    primary = work.get("url") or "../publications.html"
    source_repo = source_repository_url(work.get("docs_path", ""))
    source_repo_btn = (
        f'<a class="btn btn-outline" href="{h(source_repo)}">Source repository</a>'
        if source_repo
        else ""
    )
    enrich = work.get("enrichment", {})
    abstract = enrich.get("abstract", "")
    keywords = enrich.get("keywords", [])
    findings = enrich.get("findings", [])
    methods = enrich.get("methods", [])
    detail_sections = ""
    if abstract or keywords:
        detail_sections += f"""
        <section class="section">
            <div class="section-header"><h2>Overview</h2><p>Extracted from the local paper documentation when available.</p><div class="section-divider"></div></div>
            <div class="work-detail">
                {f'<p>{h(abstract)}</p>' if abstract else '<p>Detailed local abstract is not available for this work yet.</p>'}
                {f'<div class="keyword-row">{''.join(f'<span>{h(k)}</span>' for k in keywords)}</div>' if keywords else ''}
            </div>
        </section>"""
    if findings or methods:
        findings_html = "".join(f"<li>{h(item)}</li>" for item in findings)
        methods_html = "".join(f"<li>{h(item)}</li>" for item in methods)
        detail_sections += f"""
        <section class="section section-alt">
            <div class="section-header"><h2>Use Notes</h2><p>Concise findings and methods pulled from README/SKILL documentation.</p><div class="section-divider"></div></div>
            <div class="meta-grid">
                <div class="work-detail"><strong>Findings / Concepts</strong><ul>{findings_html or '<li>Not yet summarized.</li>'}</ul></div>
                <div class="work-detail"><strong>Methods / Techniques</strong><ul>{methods_html or '<li>Not yet summarized.</li>'}</ul></div>
            </div>
        </section>"""
    return (
        page_head(work)
        + f"""
{breadcrumb_html(work)}
    <header class="work-hero">
        <p class="eyebrow">{h(work['domain_name'])} · {h(work['type'])} · {h(work['year'])}</p>
        <h1>{h(work['title'])}</h1>
        <p class="sub">{h(work.get('venue') or 'Curated bibliography entry')}</p>
    </header>
    <main id="main" class="main">
        <section class="section">
            <div class="meta-grid">
                <div class="meta-card"><strong>Catalog Row</strong>{h(work['num'])}</div>
                <div class="meta-card"><strong>Citation Key</strong>{h(work['citation_key'])}</div>
                <div class="meta-card"><strong>Paper Folder</strong>{'Available' if work.get('has_paper_folder') else 'Not available'}</div>
                <div class="meta-card"><strong>DOI</strong>{f'<a href="{h(doi_link)}">{h(work["doi"])}</a>' if doi_link else 'Not listed'}</div>
            </div>
        </section>
{detail_sections}
        <section class="section section-alt">
            <div class="section-header"><h2>Citation</h2><p>Plain-text citation for quick reuse.</p><div class="section-divider"></div></div>
            <div class="cite-box">{h(citation_text(work))}</div>
            <p class="text-center mt-2">
                <a class="btn btn-gold" href="{h(primary)}">Primary source</a>
                <a class="btn btn-outline" href="{h(docs)}">Documentation</a>
                {source_repo_btn}
                <a class="btn btn-outline" href="../bibliography.bib">BibTeX</a>
            </p>
        </section>
{related_works_html(work)}
    </main>
    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="../publications.html">Unified bibliography</a> · <a href="../cite-verify.html">Cite & Verify</a></p>
    </footer>
</body>
</html>
"""
    )


def render_index(works: list[dict]) -> str:
    rows = "\n".join(
        f"""                <article class="work-row">
                    <div class="year">{h(w['year'])}</div>
                    <div><a href="{h(w['citation_key'])}.html">{h(w['title'])}</a><div class="venue">{h(w['domain_name'])} · {h(w['venue'])}</div></div>
                    <a href="{h(w.get('url') or '../publications.html')}">Source</a>
                </article>"""
        for w in sorted(works, key=lambda x: (int(x["year"]), -int(x["num"])), reverse=True)
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Works Index — Daniel Ari Friedman</title>
    <meta name="description" content="Per-work landing pages for Daniel Ari Friedman's curated bibliography.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://danielarifriedman.com/works/">
    <link rel="stylesheet" href="../style.css?v=newspaper-glitch-20260530c">
    <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Daniel Ari Friedman updates">
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Daniel Ari Friedman">
    <link rel="alternate" type="application/json" href="/search-index.json" title="Site search index">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Works Index — Daniel Ari Friedman">
    <meta property="og:description" content="Per-work landing pages for Daniel Ari Friedman's curated bibliography.">
    <meta property="og:url" content="https://danielarifriedman.com/works/">
    <meta property="og:site_name" content="Daniel Ari Friedman">
    <meta property="og:image" content="https://danielarifriedman.com/og-publications.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <style>.work-list{{display:grid;gap:.75rem}}.work-row{{display:grid;grid-template-columns:4.5rem 1fr auto;gap:1rem;align-items:start;padding:.9rem 1rem;background:var(--bg-card);border:1px solid var(--border);border-radius:8px}}.work-row .year{{color:var(--gold);font-weight:700}}.work-row .venue{{color:var(--text-muted);font-size:.8rem}}@media(max-width:760px){{.work-row{{grid-template-columns:1fr}}}}</style>
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
{render_nav(active="works", depth=1)}
    <header class="page-hero"><h1>Works Index</h1><p class="sub">{len(works)} generated landing pages for the unified bibliography.</p></header>
    <main id="main" class="main"><section class="section"><div class="work-list">
{rows}
    </div></section></main>
</body>
</html>
"""


def existing_generated_at(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("generated_at")
    except json.JSONDecodeError:
        return None


def render_outputs(generated_at: str | None = None) -> dict[Path, str]:
    works = load_works()
    enrichments = enrichment_map(works)
    works = [{**work, "enrichment": enrichments.get(work["citation_key"], {})} for work in works]
    by_domain: dict[str, list[dict]] = {}
    for w in works:
        by_domain.setdefault(w["domain"], []).append(w)
    for w in works:
        siblings = [s for s in by_domain.get(w["domain"], []) if s["citation_key"] != w["citation_key"]]
        siblings.sort(key=lambda x: (int(x["year"]), int(x["num"])), reverse=True)
        w["related"] = siblings[:6]
    outputs = {WORKS_DIR / "index.html": render_index(works)}
    for work in works:
        outputs[WORKS_DIR / f"{work['citation_key']}.html"] = render_work_page(work)
    outputs[ENRICHMENT_OUT] = json.dumps(
        {
            "generated_at": generated_at or generated_timestamp(),
            "source": "papers/*/README.md and papers/*/SKILL.md",
            "count": len(enrichments),
            "works": enrichments,
        },
        indent=2,
        ensure_ascii=False,
    ) + "\n"
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale")
    args = parser.parse_args()
    generated_at = existing_generated_at(ENRICHMENT_OUT) if args.check else None
    outputs = render_outputs(generated_at)
    stale: list[str] = []
    if not args.check:
        if WORKS_DIR.exists():
            for path in WORKS_DIR.glob("*.html"):
                path.unlink()
        else:
            WORKS_DIR.mkdir(parents=True)
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    if args.check:
        expected = {p.resolve() for p in outputs if p.parent == WORKS_DIR}
        extra = {p.resolve() for p in WORKS_DIR.glob("*.html")} - expected if WORKS_DIR.exists() else set()
        stale.extend(str(p.relative_to(REPO_ROOT)) for p in sorted(extra))
    if stale:
        raise SystemExit("Stale generated work pages: " + ", ".join(stale[:20]))
    action = "checked" if args.check else "wrote"
    print(f"{action} {len(outputs)} work pages")


if __name__ == "__main__":
    main()
