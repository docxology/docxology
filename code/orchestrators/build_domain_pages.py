#!/usr/bin/env python3
"""Build domain landing pages from generated works and software indexes."""

from __future__ import annotations

import argparse
import html
import json
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class DomainConfig:
    slug: str
    emoji: str
    title: str
    short_title: str
    description: str
    domains: tuple[str, ...]
    repo_names: tuple[str, ...]
    learning_path: tuple[str, ...]
    collaborators: tuple[str, ...]


DOMAINS = [
    DomainConfig(
        slug="entomology",
        emoji="🐜",
        title="Entomology & Collective Behavior",
        short_title="Entomology",
        description="Ant colony behavior, physiology, transcriptomics, and computational models of collective cognition.",
        domains=("🐜",),
        repo_names=("MetaInformAnt", "ActiveInferAnts", "ant_stack", "ant-pheromone", "ento_linguistics", "FORMINDEX"),
        learning_path=(
            "Start with the Stanford dissertation for biological context.",
            "Read Active Inferants for the Active Inference bridge.",
            "Use Ant Stack and Ento-Linguistics for recent computational extensions.",
        ),
        collaborators=("Deborah Gordon", "Karl Friston", "Chris Fields"),
    ),
    DomainConfig(
        slug="active-inference",
        emoji="🧠",
        title="Active Inference & Free Energy Principle",
        short_title="Active Inference",
        description="Free Energy Principle, generative models, belief sharing, formalization, and educational infrastructure.",
        domains=("🧠", "🌍"),
        repo_names=(
            "active_inference",
            "active_torchference",
            "goference",
            "AgenticMesh",
            "ActiveInferAnts",
            "GeneralizedNotationNotation",
            "FEP_Lean",
            "CEREBRUM",
            "cognitive",
        ),
        learning_path=(
            "Start with the literature review and ontology papers.",
            "Move to GNN, CEREBRUM, and Cognitive Case Diagrams for notation and modeling.",
            "Use FEP_Lean for formalization-oriented work.",
        ),
        collaborators=("Karl Friston", "Thomas Parr", "Maxwell J. D. Ramstead", "Conor Heins", "Tim Verbelen"),
    ),
    DomainConfig(
        slug="cognitive-security",
        emoji="🛡️",
        title="Cognitive Security",
        short_title="Cognitive Security",
        description="Narrative ecosystems, information commons, digital rhetoric, and multiagent security.",
        domains=("🛡️", "🛡"),
        repo_names=("p3if", "opentir", "cognitive-engine", "ATLAS"),
        learning_path=(
            "Start with the three COGSEC books for the program arc.",
            "Read P3IF, Narrative Information Management, and Cognitive Integrity for the formal thread.",
            "Use opentir and p3if as software companions.",
        ),
        collaborators=("RJ Cordes", "Carlos Gershenson", "Micah Musser"),
    ),
    DomainConfig(
        slug="art-synergetics",
        emoji="🎨",
        title="Art & Synergetics",
        short_title="Art & Synergetics",
        description="William Blake, Buckminster Fuller, visual art, Curio Cards, quadray coordinates, and synergetics.",
        domains=("🎨",),
        repo_names=("QuadCraft", "QuadMath", "ivm-xyz", "godel_ivm", "symergetics", "fuller-obsidian"),
        learning_path=(
            "Start with Blake & Fuller for the historical bridge.",
            "Read QuadMath and Symergetics for the formal geometry thread.",
            "Use the art gallery and Curio Cards materials for visual context.",
        ),
        collaborators=("Buckminster Fuller source tradition", "William Blake source tradition", "Curio Cards artists"),
    ),
    DomainConfig(
        slug="computational",
        emoji="💻",
        title="Computational Methods & Open Science",
        short_title="Computational",
        description="Research templates, markdown containers, discovery engines, reproducible workflows, and software infrastructure.",
        domains=("💻",),
        repo_names=("template", "mdkv", "markdown_decision_process", "steganographer", "timeline_generator", "codomyrmex"),
        learning_path=(
            "Start with the reproducible generative research template.",
            "Use MDKV and Markdown Decision Process for structured document work.",
            "Use the Discovery Engine and software catalog for agentic research navigation.",
        ),
        collaborators=("Active Inference Institute contributors", "Open-source repository contributors"),
    ),
]


def load_json(path: str) -> dict:
    with open(REPO_ROOT / path, encoding="utf-8") as f:
        return json.load(f)


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def page_head(title: str, description: str, canonical: str, og_image: str = "og-image.jpg") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{h(title)} — Daniel Ari Friedman</title>
    <meta name="description" content="{h(description)}">
    <meta name="author" content="Daniel Ari Friedman">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://danielarifriedman.com/{canonical}">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="manifest" href="/manifest.json">
    <link rel="alternate" type="text/plain" href="/llms.txt" title="LLMs.txt">
    <link rel="alternate" type="application/rss+xml" href="/feed.xml" title="Daniel Ari Friedman updates">
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="Daniel Ari Friedman">
    <link rel="alternate" type="application/json" href="/search-index.json" title="Site search index">
    <meta property="og:type" content="website">
    <meta property="og:title" content="{h(title)} — Daniel Ari Friedman">
    <meta property="og:description" content="{h(description)}">
    <meta property="og:url" content="https://danielarifriedman.com/{canonical}">
    <meta property="og:image" content="https://danielarifriedman.com/{og_image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css">
    <meta name="theme-color" content="#0c0c0e">
    <style>
        .domain-hero{{max-width:980px;margin:0 auto;text-align:center;padding:7rem 2rem 3rem}}
        .domain-hero h1{{font-family:'Playfair Display',serif;font-size:clamp(2.2rem,5vw,4rem);line-height:1.1;margin-bottom:1rem}}
        .domain-hero p{{color:var(--text-secondary);max-width:760px;margin:0 auto;line-height:1.7}}
        .mini-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem}}
        .mini-card{{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:1.1rem}}
        .mini-card h3{{font-size:1rem;margin-bottom:.35rem}}
        .mini-card p,.mini-card li{{font-size:.86rem;color:var(--text-secondary);line-height:1.6}}
        .work-list{{display:grid;gap:.75rem}}
        .work-row{{display:grid;grid-template-columns:4.5rem 1fr auto;gap:1rem;align-items:start;padding:.9rem 1rem;background:var(--bg-card);border:1px solid var(--border);border-radius:8px}}
        .work-row .year{{color:var(--gold);font-weight:700}}
        .work-row .venue{{color:var(--text-muted);font-size:.8rem}}
        @media(max-width:760px){{.work-row{{grid-template-columns:1fr}}}}
    </style>
</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
    <nav role="navigation" aria-label="Main navigation">
        <a href="index.html" class="nav-logo">Daniel Ari Friedman</a>
        <button class="menu-btn" onclick="document.querySelector('.nav-links').classList.toggle('open')" aria-label="Toggle menu">☰</button>
        <div class="nav-links">
            <a href="index.html#about">About</a>
            <a href="index.html#research">Research</a>
            <a href="publications.html">Publications</a>
            <a href="domains.html" class="active">Domains</a>
            <a href="software.html">Software</a>
            <a href="search.html">Search</a>
            <a href="discovery.html">Discovery</a>
            <a href="media.html">Media</a>
        </div>
    </nav>
"""


def page_footer() -> str:
    return """    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="https://activeinference.institute/">Active Inference Institute</a> · <a href="https://danielarifriedman.com/">danielarifriedman.com</a></p>
        <div class="footer-links">
            <a href="publications.html">Publications</a>
            <a href="software.html">Software</a>
            <a href="search.html">Search</a>
            <a href="discovery.html">Discovery</a>
            <a href="cite-verify.html">Cite & Verify</a>
            <a href="https://github.com/docxology/docxology">Source Repo</a>
        </div>
        <p class="text-center text-sm text-muted mt-1">© 2026 Daniel Ari Friedman. All rights reserved. · Last updated: May 2026</p>
    </footer>
</body>
</html>
"""


def work_link(work: dict) -> str:
    if work.get("docs_path"):
        return f"https://github.com/docxology/docxology/tree/main/{work['docs_path'].rstrip('/')}"
    return work.get("url") or "publications.html"


def select_repositories(repos: list[dict], names: tuple[str, ...]) -> list[dict]:
    order = {name.lower(): idx for idx, name in enumerate(names)}
    wanted = set(order)
    selected = [repo for repo in repos if repo["name"].lower() in wanted]
    return sorted(selected, key=lambda repo: (order.get(repo["name"].lower(), 999), repo["owner"]))


def render_domain_page(config: DomainConfig, works: list[dict], repos: list[dict]) -> str:
    domain_works = [w for w in works if w["domain"] in config.domains]
    selected = sorted(domain_works, key=lambda w: (int(w["year"]), -int(w["num"])), reverse=True)[:12]
    domain_repos = select_repositories(repos, config.repo_names)

    works_html = "\n".join(
        f"""                <article class="work-row">
                    <div class="year">{h(w['year'])}</div>
                    <div><a href="{h(work_link(w))}">{h(w['title'])}</a><div class="venue">{h(w['venue'])} · {h(w['type'])}</div></div>
                    <a href="{h(w['url'])}" aria-label="Primary link for {h(w['title'])}">Link</a>
                </article>"""
        for w in selected
    )
    repos_html = "\n".join(
        f"""                <article class="mini-card">
                    <h3><a href="{h(r['url'])}">{h(r['name'])}</a></h3>
                    <p>{h(r['description'])}</p>
                    <p class="text-muted">{h(r['language'] or 'Unspecified')} · ⭐ {h(r['stars'])}</p>
                </article>"""
        for r in domain_repos
    )
    learning_html = "\n".join(f"<li>{h(item)}</li>" for item in config.learning_path)
    collaborators_html = ", ".join(h(c) for c in config.collaborators)
    title = config.title
    canonical = f"domain-{config.slug}.html"
    return (
        page_head(title, config.description, canonical, f"og-{config.slug}.jpg")
        + f"""
    <header class="domain-hero">
        <h1>{config.emoji} {h(config.title)}</h1>
        <p>{h(config.description)}</p>
    </header>
    <main id="main" class="main">
        <section class="section">
            <div class="mini-grid">
                <div class="mini-card"><h3>{len(domain_works)} Works</h3><p>Curated works in this domain from the unified bibliography.</p></div>
                <div class="mini-card"><h3>{len(domain_repos)} Related Repositories</h3><p>Selected software entries connected to this domain.</p></div>
                <div class="mini-card"><h3>Collaborator Context</h3><p>{collaborators_html}</p></div>
            </div>
        </section>
        <section class="section section-alt">
            <div class="section-header">
                <h2>Selected Works</h2>
                <p>Newest and most relevant entries for this domain.</p>
                <div class="section-divider"></div>
            </div>
            <div class="work-list">
{works_html}
            </div>
            <p class="text-center mt-2"><a href="publications.html" class="btn btn-gold">Open full bibliography</a></p>
        </section>
        <section class="section">
            <div class="section-header">
                <h2>Related Software</h2>
                <p>Repository entry points for implementation, data, and teaching work.</p>
                <div class="section-divider"></div>
            </div>
            <div class="mini-grid">
{repos_html}
            </div>
        </section>
        <section class="section section-alt">
            <div class="section-header">
                <h2>Learning Path</h2>
                <p>A compact route through the material.</p>
                <div class="section-divider"></div>
            </div>
            <div class="mini-card"><ul>{learning_html}</ul></div>
            <p class="text-center mt-2"><a href="pages/DOMAINS.md" class="btn btn-outline">Markdown domain map</a></p>
        </section>
    </main>
"""
        + page_footer()
    )


def render_domains_index(works: list[dict], repos: list[dict]) -> str:
    cards = []
    for config in DOMAINS:
        count = sum(1 for w in works if w["domain"] in config.domains)
        repo_count = len(select_repositories(repos, config.repo_names))
        cards.append(
            f"""                <article class="mini-card">
                    <h3><a href="domain-{config.slug}.html">{config.emoji} {h(config.short_title)}</a></h3>
                    <p>{h(config.description)}</p>
                    <p class="text-muted">{count} works · {repo_count} selected repos</p>
                </article>"""
        )
    return (
        page_head(
            "Research Domains",
            "Domain landing pages for Daniel Ari Friedman's research, software, collaborators, and learning pathways.",
            "domains.html",
            "og-domains.jpg",
        )
        + f"""
    <header class="domain-hero">
        <h1>Research Domains</h1>
        <p>Five entry points through the bibliography, software catalog, collaborator network, and learning pathways.</p>
    </header>
    <main id="main" class="main">
        <section class="section">
            <div class="mini-grid">
{chr(10).join(cards)}
            </div>
        </section>
        <p class="text-center mt-2">
            <a href="publications.html" class="btn btn-gold">Bibliography</a>
            <a href="software.html" class="btn btn-outline">Software</a>
            <a href="pages/DOMAINS.md" class="btn btn-outline">Markdown map</a>
        </p>
    </main>
"""
        + page_footer()
    )


def render_domains_md(works: list[dict], repos: list[dict]) -> str:
    lines = [
        "---",
        'title: "DOMAINS - Daniel Ari Friedman"',
        'description: "Research domain map linking works, software, collaborators, and learning paths."',
        'keywords: "Daniel Ari Friedman, research domains, Active Inference, entomology, cognitive security"',
        "---",
        "<div align=\"center\">",
        "",
        "# Research Domains",
        "",
        "> **Navigation**: [🏠 Home](../README.md) | [📚 Bibliography](BIBLIOGRAPHY.md) | [💻 Software](SOFTWARE.md) | [🧭 Discovery](DISCOVERY.md) | [🧾 Evidence](EVIDENCE.md)",
        "",
        "[Website domain index](../domains.html)",
        "",
        "</div>",
        "",
        "---",
        "",
    ]
    for config in DOMAINS:
        domain_works = [w for w in works if w["domain"] in config.domains]
        domain_repos = select_repositories(repos, config.repo_names)
        lines.extend(
            [
                f"## {config.emoji} [{config.title}](../domain-{config.slug}.html)",
                "",
                config.description,
                "",
                f"- Works: {len(domain_works)}",
                f"- Selected repositories: {len(domain_repos)}",
                f"- Collaborator context: {', '.join(config.collaborators)}",
                "",
                "**Learning path**",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in config.learning_path)
        lines.extend(["", "**Selected works**", ""])
        for w in sorted(domain_works, key=lambda x: (int(x["year"]), -int(x["num"])), reverse=True)[:6]:
            lines.append(f"- {w['year']} — [{w['title']}]({w['url']})")
        lines.extend(["", "**Selected repositories**", ""])
        for r in domain_repos[:8]:
            lines.append(f"- [{r['name']}]({r['url']}) — {r['description']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_outputs() -> dict[Path, str]:
    works = load_json("data/works.json")["works"]
    repos = load_json("data/software.json")["repositories"]
    outputs = {REPO_ROOT / "domains.html": render_domains_index(works, repos)}
    for config in DOMAINS:
        outputs[REPO_ROOT / f"domain-{config.slug}.html"] = render_domain_page(config, works, repos)
    outputs[REPO_ROOT / "pages" / "DOMAINS.md"] = render_domains_md(works, repos)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated pages are stale")
    args = parser.parse_args()
    outputs = render_outputs()
    stale: list[str] = []
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.write_text(content, encoding="utf-8")
    if stale:
        raise SystemExit("Stale generated domain pages: " + ", ".join(stale))
    action = "checked" if args.check else "wrote"
    print(f"{action} {len(outputs)} domain pages")


if __name__ == "__main__":
    main()
