#!/usr/bin/env python3
"""Build domain landing pages from generated works and software indexes."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from generated_outputs import stale_output_paths, write_output_texts  # noqa: E402
from site_nav import (  # noqa: E402
    BREADCRUMB_CSS,
    HEAD_EXTRAS,
    INTERACTIVE_SCRIPTS,
    MENU_ESC_SCRIPT,
    breadcrumb_list_jsonld,
    clip_description,
    render_breadcrumb,
    render_nav_domain,
    social_meta_tags,
)
from site_facts import generated_date, generated_month_year  # noqa: E402


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
            "Read the foundational pillar guide on <a href='computational-entomology.html'>Computational Entomology</a> for simulation models and neurogenomic algorithms.",
            "Explore <a href='insect-cognition.html'>Insect Cognition &amp; Collective Intelligence</a> for distributed cognition and stigmergic coordination.",
            "Investigate behavioral neurochemistry in <a href='works/Friedman2020MeasurementNaturalVariationNeurotransmitter088.html'>Measurement of Natural Variation in Neurotransmitter Content</a>.",
            "Study molecular and transcriptomic foundations in <a href='works/Friedman2020GeneExpressionVariationBrains086.html'>Gene Expression Variation in Harvester Ant Foragers</a>.",
            "Examine distributed active inference modeling in <a href='works/Friedman2021ActiveInferantsActiveInference075.html'>Active Inferants: An Active Inference Framework for Ant Colony Behavior</a>.",
            "Explore modern software implementations via <a href='https://github.com/docxology/MetaInformAnt'>MetaInformAnt</a> and <a href='https://github.com/ActiveInferenceInstitute/ActiveInferAnts'>ActiveInferAnts</a>.",
            "Inspect global bibliometric archives via the <a href='https://github.com/docxology/FORMINDEX'>FORMINDEX</a> interface to FORMIS.",
        ),
        collaborators=("Deborah Gordon", "Karl Friston", "Chris Fields"),
    ),
    DomainConfig(
        slug="active-inference",
        emoji="🧠",
        title="Active Inference & Free Energy Principle",
        short_title="Active Inference",
        description="Free Energy Principle, generative models, belief sharing, formalization, and educational infrastructure.",
        domains=("🧠",),
        repo_names=(
            "active_inference",
            "active_torchference",
            "goference",
            "AgenticMesh",
            "ActiveInferAnts",
            "GeneralizedNotationNotation",
            "fep_lean",
            "CEREBRUM",
            "cognitive",
        ),
        learning_path=(
            "Read the comprehensive <a href='active-inference.html'>Active Inference &amp; Free Energy Principle Tutorial</a>.",
            "Explore neurosymbolic integrations in <a href='neurosymbolic-ai.html'>Neurosymbolic AI &amp; Active Inference</a>.",
            "Trace multi-agent coordination theory in <a href='works/Friedman2024SharedProtentionsMultiAgent040.html'>Shared Protentions in Multi-Agent Active Inference</a>.",
            "Examine distributed belief updates in <a href='works/Friedman2024FederatedInferenceBeliefSharing036.html'>Federated Inference and Belief Sharing</a>.",
            "Study formal mathematical notation systems in <a href='works/Friedman2023GeneralizedNotationNotationActive056.html'>Generalized Notation Notation (GNN)</a>.",
            "Explore theorem proving in Lean 4 via <a href='works/Friedman2026TowardsLean4Formalization113.html'>Towards Lean 4 Formalization of Active Inference</a> and the <a href='https://github.com/ActiveInferenceInstitute/fep_lean'>fep_lean</a> repository.",
            "Engage with multi-agent orchestration and case-based reasoning in <a href='https://github.com/ActiveInferenceInstitute/CEREBRUM'>CEREBRUM</a> and <a href='https://github.com/docxology/active_torchference'>active_torchference</a>.",
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
            "Read the comprehensive explainer guide <a href='cognitive-security.html'>What Is Cognitive Security? Theory, Threat Models, and Defense</a>.",
            "Survey the foundational COGSEC publications: Information Resonance &amp; Narrative Information Ecosystems, Narrative Information Management (NIM-21), and Emergent Teams for Complex Threats.",
            "Examine multiagent epistemic defense in <a href='works/Friedman2026CognitiveIntegrityFrameworkFormal005.html'>Cognitive Integrity Framework: Formal Foundations (Part 1: Theory)</a>.",
            "Analyze information commons and open standards in <a href='works/Friedman2022StructuringInformationCommonsOpen071.html'>Structuring the Information Commons: Open Standards and Cognitive Security</a>.",
            "Study multi-perspective property framing in <a href='works/Friedman2023P3IFPropertiesProcessesPerspectives062.html'>The P3IF: Properties, Processes, and Perspectives Inter-Framework</a>.",
            "Implement multi-agent cognitive security tools using <a href='https://github.com/docxology/p3if'>p3if</a> and the <a href='https://github.com/docxology/ATLAS'>ATLAS</a> framework.",
            "Examine ecosystem dependency profiles and intelligence mapping via <a href='https://github.com/docxology/opentir'>opentir</a>.",
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
            "Browse the curated visual archive on the <a href='art.html'>Visual Art Gallery</a> (940+ catalogued pen-and-ink drawings).",
            "Explore early blockchain history with <a href='art.html#curio-cards'>Curio Cards (Cards 24, 25, 26 — Complexity, Passion, Education; 2017)</a>.",
            "Study prophetic economics and metaphysics in <a href='works/Friedman2026GoldenCompassLunarFlux004.html'>The Golden Compass and the Lunar Flux: William Blake and the Architecture of Value</a>.",
            "Examine anticipatory epistemology in <a href='works/Friedman2026BeforePragmatismHadName003.html'>Before Pragmatism Had a Name: Blake's America A Prophecy</a>.",
            "Investigate tetrahedral geometry and coordinate systems in <a href='works/Friedman2025QuadMathAnalyticalReview4D018.html'>QuadMath: An Analytical Review of 4D and Quadray Coordinates</a>.",
            "Interact with 3D synergetics environments through <a href='https://github.com/docxology/QuadCraft'>QuadCraft</a> and <a href='https://github.com/docxology/ivm-xyz'>ivm-xyz</a>.",
            "Explore digital knowledge graphs of synergetics with <a href='https://github.com/docxology/fuller-obsidian'>fuller-obsidian</a>.",
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
        repo_names=(
            "template",
            "mdkv",
            "markdown_decision_process",
            "steganographer",
            "timeline_generator",
            "codomyrmex",
            "biology_textbook",
            "biol-1",
            "biol-8",
        ),
        learning_path=(
            "Explore the principles of verifiable open research in <a href='cite-verify.html'>AI Provenance &amp; Verification Architecture</a>.",
            "Review the infrastructure-as-code research methodology in <a href='works/Friedman2026TemplateApproachReproducibleGenerative001.html'>A template/ approach to Reproducible Generative Research</a>.",
            "Study structured document semantics in <a href='works/Friedman2025MarkdownDecisionProcessFramework015.html'>Markdown Decision Process Framework</a>.",
            "Inspect verified software execution records in the <a href='reproducibility.html'>Reproducibility Ledger</a>.",
            "Explore modular AI-agent development environments with <a href='https://github.com/docxology/codomyrmex'>codomyrmex</a> and <a href='https://github.com/docxology/template'>template</a>.",
            "Query canonical knowledge graph endpoints via the <a href='discovery.html'>Discovery Map</a> and <a href='catalog.html'>Data Catalog</a>.",
        ),
        collaborators=("Active Inference Institute contributors", "Open-source repository contributors"),
    ),
    DomainConfig(
        slug="biomedicine",
        emoji="🧬",
        title="Genetics & Biomedicine",
        short_title="Genetics & Biomedicine",
        description="Honey bee evolution, gene expression variation, nuclear structure, population genetics, and biomedical mechanisms.",
        domains=("🧬",),
        repo_names=("MetaInformAnt", "EvoJump", "biology_textbook", "biol-8", "biol-1"),
        learning_path=(
            "Explore empirical behavioral genomics in <a href='works/Friedman2020GeneExpressionVariationBrains086.html'>Gene Expression Variation in Harvester Ant Forager Brains</a>.",
            "Study tissue-specific transcriptomic pipelines in <a href='works/Friedman2023SnapshotPipelineTissueSpecific047.html'>Pipeline for Tissue-Specific Gene Expression Meta-Analysis in Honey Bees</a>.",
            "Read evolutionary and developmental synthesis in <a href='works/Friedman2023VariationalSynthesisEvolutionaryDevelopmental048.html'>A Variational Synthesis of Evolutionary and Developmental Dynamics</a>.",
            "Investigate cellular biophysics and mechanobiology in <a href='works/Friedman2016CellsMechanobiologyOsteopathy164.html'>Cells, Mechanobiology, and Osteopathy</a>.",
            "Review undergraduate open curriculum materials in <a href='https://github.com/docxology/biology_textbook'>biology_textbook</a>, <a href='https://github.com/docxology/biol-1'>biol-1</a>, and <a href='https://github.com/docxology/biol-8'>biol-8</a>.",
            "Query public biomedical indexing records directly via the <a href='https://pubmed.ncbi.nlm.nih.gov/?term=Daniel+Ari+Friedman%5BAuthor%5D'>PubMed Author Query</a> and <a href='https://europepmc.org/search?query=AUTH:%22Daniel%20Ari%20Friedman%22'>Europe PMC</a>.",
        ),
        collaborators=("Deborah Gordon", "UC Davis Genetics", "Stanford Biology"),
    ),
    DomainConfig(
        slug="aii-ecosystem",
        emoji="🌍",
        title="AII Ecosystem",
        short_title="AII Ecosystem",
        description="Active Inference Institute programs, infrastructure, textbook cohorts, and organizational ecosystem work.",
        domains=("🌍",),
        repo_names=("active_inference", "fep_lean", "cognitive", "AgenticMesh"),
        learning_path=(
            "Discover the organizational mission, governance, and programs on the <a href='https://activeinference.institute/'>Active Inference Institute Official Portal</a>.",
            "Survey ecosystem development and open research milestones in <a href='works/Friedman2025ActiveInferenceInstituteActive024.html'>The Active Inference Institute &amp; Active Inference Ecosystem (v3, 2025 snapshot)</a>.",
            "Explore ontology standardization efforts in <a href='works/Friedman2024AligningActiveInferenceOntology029.html'>Aligning Active Inference Ontology to SUMO</a>.",
            "Participate in community education through the <a href='https://activeinference.institute/projects/textbook-group/'>Textbook Group Cohorts</a> and <a href='videos.html'>Institute Video Archives</a>.",
            "Engage with formal mathematical specifications on the <a href='https://github.com/ActiveInferenceInstitute/fep_lean'>fep_lean repository</a>.",
            "Review verified non-profit records via the <a href='https://projects.propublica.org/nonprofits/organizations/882985125'>ProPublica Nonprofit Explorer (EIN 88-2985125)</a>.",
        ),
        collaborators=("Active Inference Institute educators and contributors", "Institute program participants"),
    ),
    DomainConfig(
        slug="presentations-media",
        emoji="🎥",
        title="Presentations & Media",
        short_title="Presentations & Media",
        description="Talks, courses, presentations, and media artifacts connected to the research and teaching program.",
        domains=("🎥",),
        repo_names=("biology_textbook", "biol-1", "biol-8"),
        learning_path=(
            "Browse 500+ indexed lectures, symposia, and live streams on the <a href='videos.html'>Video Index &amp; Interactive Timeline</a>.",
            "Explore media appearances, podcasts, and interview features on the <a href='media.html'>Media Appearances Hub</a>.",
            "Study active-inference live streams in <a href='works/Friedman2026ActiveInferenceJournal500002.html'>Active Inference Journal — 500+ Videos with Transcripts</a>.",
            "Access generative biology curriculum and lecture materials in <a href='works/Friedman2026IntroductionBiologyGenerativeApproach117.html'>Introduction to Biology: A Generative Approach</a>.",
            "Review transcript processing software pipelines in the <a href='https://doi.org/10.5281/zenodo.18686966'>Journal-Utilities Software Release (Zenodo 18686966)</a>.",
            "Explore public video channels on <a href='https://youtube.com/@activeinference'>Active Inference YouTube</a> and <a href='https://youtube.com/@danielarifriedman'>Personal YouTube Channel</a>.",
        ),
        collaborators=("Active Inference Institute educators", "Course and media collaborators"),
    ),
]


def load_json(path: str) -> dict:
    with open(REPO_ROOT / path, encoding="utf-8") as f:
        return json.load(f)


def h(value: object) -> str:
    return html.escape(str(value), quote=True)


def clean_markdown_for_html(text: str) -> str:
    """Strip markdown links/formatting and escape for HTML attribute/text context."""
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", str(text or ""))
    cleaned = re.sub(r"[*_`#]", "", cleaned)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def strip_html_tags(text: str) -> str:
    """Strip HTML tags for pure-text outputs such as Markdown or plain titles."""
    return re.sub(r"<[^>]+>", "", str(text or "")).strip()


def page_head(
    title: str,
    description: str,
    canonical: str,
    og_image: str = "og-image.jpg",
    *,
    nav_active: str = "domains",
    breadcrumb: list[tuple[str, str]] | None = None,
    extra_jsonld: list[dict] | None = None,
) -> str:
    nav = render_nav_domain(active=nav_active)
    blocks = list(extra_jsonld or [])
    crumb_css = ""
    crumb_html = ""
    if breadcrumb:
        crumb_css = BREADCRUMB_CSS
        crumb_html = "\n" + render_breadcrumb(breadcrumb)
        blocks.append(breadcrumb_list_jsonld(breadcrumb))
    jsonld_html = "".join(
        f'    <script type="application/ld+json">\n{json.dumps(b, indent=4, ensure_ascii=False)}\n    </script>\n'
        for b in blocks
    )
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
{HEAD_EXTRAS}
    <meta property="og:type" content="website">
    <meta property="og:title" content="{h(title)} — Daniel Ari Friedman">
    <meta property="og:description" content="{h(description)}">
    <meta property="og:url" content="https://danielarifriedman.com/{canonical}">
    <meta property="og:image" content="https://danielarifriedman.com/{og_image}">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
{social_meta_tags(f"{title} — Daniel Ari Friedman", description, f"https://danielarifriedman.com/{og_image}", image_alt=f"{title} — Daniel Ari Friedman")}
    <link rel="stylesheet" href="style.css?v=newspaper-glitch-20260530c">
    <meta name="theme-color" content="#0c0c0e">
    <style>
        .domain-hero{{max-width:980px;margin:0 auto;text-align:center;padding:7rem 2rem 3rem}}
        .domain-hero h1{{font-family:Georgia,'Times New Roman',serif;font-size:clamp(2.2rem,5vw,4rem);line-height:1.1;margin-bottom:1rem}}
        .domain-hero p{{color:var(--text-secondary);max-width:760px;margin:0 auto;line-height:1.7}}
        .mini-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:1rem}}
        .mini-card{{background:var(--bg-card);border:1px solid var(--border);border-radius:var(--radius);padding:1.1rem}}
        .mini-card h2,.mini-card h3{{font-size:1rem;margin-bottom:.35rem;font-weight:700}}
        .mini-card p,.mini-card li{{font-size:.86rem;color:var(--text-secondary);line-height:1.6}}
        .work-list{{display:grid;gap:.75rem}}
        .work-row{{display:grid;grid-template-columns:4.5rem 1fr auto;gap:1rem;align-items:start;padding:.9rem 1rem;background:var(--bg-card);border:1px solid var(--border);border-radius:8px}}
        .work-row .year{{color:var(--gold);font-weight:700}}
        .work-row .venue{{color:var(--text-muted);font-size:.8rem}}
        .work-desc{{font-size:.84rem;color:var(--text-secondary);margin-top:.35rem;line-height:1.5}}
        .work-meta-links{{margin-top:.4rem;display:flex;gap:.75rem;font-size:.78rem;flex-wrap:wrap}}
        .work-meta-links a{{color:var(--silver-bright);text-decoration:none}}
        .work-meta-links a:hover{{text-decoration:underline;color:var(--gold)}}
        .repo-meta-links{{margin-top:.5rem;display:flex;gap:.75rem;font-size:.8rem;flex-wrap:wrap}}
        .repo-meta-links a{{color:var(--silver-bright);text-decoration:none}}
        .repo-meta-links a:hover{{text-decoration:underline;color:var(--gold)}}
        .api-card{{display:flex;flex-direction:column;justify-content:space-between}}
        @media(max-width:760px){{.work-row{{grid-template-columns:1fr}}}}
        {crumb_css}
    </style>
{jsonld_html}</head>
<body>
    <a href="#main" class="skip-link">Skip to main content</a>
{nav}{crumb_html}
"""


def page_footer() -> str:
    return f"""    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="https://activeinference.institute/">Active Inference Institute</a> · <a href="https://danielarifriedman.com/">danielarifriedman.com</a></p>
        <div class="footer-links">
            <a href="publications.html">Publications</a>
            <a href="software.html">Software</a>
            <a href="search.html">Search</a>
            <a href="discovery.html">Discovery</a>
            <a href="cite-verify.html">Cite &amp; Verify</a>
            <a href="https://github.com/docxology/docxology">Source Repo</a>
        </div>
        <p class="text-center text-sm text-muted mt-1">© 2026 Daniel Ari Friedman. All rights reserved. · Data refreshed {generated_month_year()}</p>
    </footer>
""" + INTERACTIVE_SCRIPTS + "\n" + MENU_ESC_SCRIPT + """</body>
</html>
"""


def work_link(work: dict) -> str:
    """Link to the local work page, falling back to the paper folder or primary URL."""
    citation_key = work.get("citation_key")
    if citation_key:
        return f"works/{citation_key}.html"
    if work.get("docs_path"):
        return f"{work['docs_path'].rstrip('/')}/"
    return work.get("url") or "publications.html"


def select_repositories(repos: list[dict], names: tuple[str, ...]) -> list[dict]:
    order = {name.lower(): idx for idx, name in enumerate(names)}
    wanted = set(order)
    selected = [repo for repo in repos if repo["name"].lower() in wanted]
    return sorted(selected, key=lambda repo: (order.get(repo["name"].lower(), 999), repo["owner"]))


def render_domain_page(
    config: DomainConfig,
    works: list[dict],
    repos: list[dict],
    enrichments: dict[str, dict] | None = None,
) -> str:
    if enrichments is None:
        enrichments = {}

    domain_works = [w for w in works if w["domain"] in config.domains]

    def _year_key(w: dict) -> int:
        try:
            return int(w["year"]) if str(w["year"]).isdigit() else 9999
        except (TypeError, ValueError, KeyError):
            return 9999

    selected = sorted(domain_works, key=lambda w: (_year_key(w), -int(w.get("num", 0) or 0)), reverse=True)[:12]
    domain_repos = select_repositories(repos, config.repo_names)

    # Count extraction stats for this domain
    domain_ft_count = sum(1 for w in domain_works if w.get("has_full_text"))
    domain_img_count = sum(1 for w in domain_works if w.get("has_images"))

    works_rows = []
    for w in selected:
        ckey = w.get("citation_key", "")
        enrich = enrichments.get(ckey, {})
        abstract = enrich.get("abstract", "")
        findings = enrich.get("findings", [])
        desc_text = ""
        if abstract:
            desc_text = clip_description(clean_markdown_for_html(abstract), 180)
        elif findings:
            desc_text = clip_description(clean_markdown_for_html(findings[0]), 180)

        desc_html = f'<div class="work-desc">{h(desc_text)}</div>' if desc_text else ""

        meta_links = []
        if w.get("doi"):
            meta_links.append(f'<a href="https://doi.org/{h(w["doi"])}">DOI: {h(w["doi"])}</a>')
        if w.get("has_paper_folder") and w.get("docs_path"):
            meta_links.append(f'<a href="{h(w["docs_path"].rstrip("/"))}/">Paper Folder</a>')
        if w.get("citation_key"):
            meta_links.append(f'<a href="works/{h(w["citation_key"])}.html">Full Work Page &amp; Citation</a>')

        meta_links_html = f'<div class="work-meta-links">{" · ".join(meta_links)}</div>' if meta_links else ""

        works_rows.append(
            f"""                <article class="work-row">
                    <div class="year">{h(w['year'])}</div>
                    <div>
                        <a href="{h(work_link(w))}"><strong>{h(w['title'])}</strong></a>
                        <div class="venue">{h(w['venue'])} · {h(w['type'])}</div>
                        {desc_html}
                        {meta_links_html}
                    </div>
                    <a href="{h(w['url'])}" aria-label="Primary link for {h(w['title'])}" class="btn btn-sm btn-outline">Primary Link</a>
                </article>"""
        )

    works_html = "\n".join(works_rows)

    repos_rows = []
    for r in domain_repos:
        repo_links = [f'<a href="{h(r["url"])}">GitHub Repo</a>']
        if r.get("paper_path"):
            repo_links.append(f'<a href="{h(r["paper_path"].rstrip("/"))}/">Companion Paper</a>')
        if r.get("zenodo_url"):
            repo_links.append(f'<a href="{h(r["zenodo_url"])}">Zenodo Release</a>')
        repo_links_html = f'<div class="repo-meta-links">{" · ".join(repo_links)}</div>'

        repos_rows.append(
            f"""                <article class="mini-card">
                    <h3><a href="{h(r['url'])}">{h(r['name'])}</a></h3>
                    <p>{h(r['description'])}</p>
                    <p class="text-muted">{h(r['language'] or 'Unspecified')} · ⭐ {h(r['stars'])} · Updated {h(r.get('updated_or_year', ''))}</p>
                    {repo_links_html}
                </article>"""
        )

    repos_html = "\n".join(repos_rows)

    # Note: learning_path entries already contain valid HTML tags (like <a href="...">)
    learning_html = "\n".join(f"<li>{item}</li>" for item in config.learning_path)
    collaborators_html = ", ".join(h(c) for c in config.collaborators)
    title = config.title
    canonical = f"domain-{config.slug}.html"
    breadcrumb = [("Home", ""), ("Domains", "domains.html"), (config.short_title, canonical)]
    collection_ld = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "@id": f"https://danielarifriedman.com/{canonical}#page",
        "name": f"{config.title} — Daniel Ari Friedman",
        "description": config.description,
        "url": f"https://danielarifriedman.com/{canonical}",
        "isPartOf": {"@id": "https://danielarifriedman.com/#website"},
        "dateModified": generated_date(),
        "about": {"@type": "DefinedTerm", "name": config.short_title},
    }
    return (
        page_head(
            title,
            config.description,
            canonical,
            f"og-{config.slug}.jpg",
            breadcrumb=breadcrumb,
            extra_jsonld=[collection_ld],
        )
        + f"""
    <header class="domain-hero">
        <h1>{h(config.title)}</h1>
        <p>{h(config.description)}</p>
    </header>
    <main id="main" class="main">
        <section class="section">
            <div class="mini-grid">
                <div class="mini-card"><h2>{len(domain_works)} Works</h2><p>Curated works in this domain from the unified bibliography.</p></div>
                <div class="mini-card"><h2>{len(domain_repos)} Related Repositories</h2><p>Selected software entries connected to this domain.</p></div>
                <div class="mini-card"><h2>Full Text &amp; Images</h2><p>{domain_ft_count} of {len(domain_works)} works have extracted full text, {domain_img_count} have image galleries.</p></div>
                <div class="mini-card"><h2>Collaborator Context</h2><p>{collaborators_html}</p></div>
            </div>
        </section>
        <section class="section section-alt">
            <div class="section-header">
                <h2>Selected Works</h2>
                <p>Newest and most relevant entries for this domain with abstracts and full-text links.</p>
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
                <p>Repository entry points for implementation, companion papers, data, and teaching work.</p>
                <div class="section-divider"></div>
            </div>
            <div class="mini-grid">
{repos_html}
            </div>
        </section>
        <section class="section section-alt">
            <div class="section-header">
                <h2>Learning Path</h2>
                <p>A structured, cross-linked route through tutorials, pillar guides, foundational papers, and software repositories.</p>
                <div class="section-divider"></div>
            </div>
            <div class="mini-card"><ul>{learning_html}</ul></div>
        </section>
        <section class="section">
            <div class="section-header">
                <h2>Public APIs &amp; Discovery Endpoints</h2>
                <p>Machine-readable endpoints for querying research metadata and persistent identifiers.</p>
                <div class="section-divider"></div>
            </div>
            <div class="mini-grid">
                <article class="mini-card api-card">
                    <h3><a href="https://orcid.org/0000-0001-6232-9096">ORCID API</a></h3>
                    <p>Persistent researcher identity record (0000-0001-6232-9096) linking published works and verified peer reviews.</p>
                    <p class="text-muted"><a href="https://pub.orcid.org/v3.0/0000-0001-6232-9096">pub.orcid.org/v3.0/0000-0001-6232-9096</a></p>
                </article>
                <article class="mini-card api-card">
                    <h3><a href="https://zenodo.org/api/records?q=metadata.creators.person_or_org.identifiers.identifier%3A%220000-0001-6232-9096%22">Zenodo REST API</a></h3>
                    <p>Open-access deposits, software releases, preprints, and dataset versions indexed by ORCID.</p>
                    <p class="text-muted"><a href="https://zenodo.org/api/records?q=metadata.creators.person_or_org.name%3A%22Friedman%2C%20Daniel%20Ari%22">Zenodo Creator Query</a></p>
                </article>
                <article class="mini-card api-card">
                    <h3><a href="https://api.crossref.org/works?filter=orcid:0000-0001-6232-9096">Crossref Works API</a></h3>
                    <p>Publisher DOI metadata records, license information, and formal citation relations.</p>
                    <p class="text-muted"><a href="https://api.crossref.org/works?filter=orcid:0000-0001-6232-9096">api.crossref.org/works</a></p>
                </article>
                <article class="mini-card api-card">
                    <h3><a href="https://api.github.com/users/docxology">GitHub REST API</a></h3>
                    <p>Repository metadata, release artifacts, and open-source software inventory.</p>
                    <p class="text-muted"><a href="https://api.github.com/users/docxology/repos">api.github.com/users/docxology/repos</a></p>
                </article>
            </div>
            <p class="text-center mt-2">
                <a href="discovery.html" class="btn btn-outline">Full Discovery Map</a>
                <a href="pages/DOMAINS.md" class="btn btn-outline">Markdown Domain Map</a>
            </p>
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
                    <h2><a href="domain-{config.slug}.html">{h(config.short_title)}</a></h2>
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
            breadcrumb=[("Home", ""), ("Domains", "domains.html")],
            extra_jsonld=[{
                "@context": "https://schema.org",
                "@type": "CollectionPage",
                "@id": "https://danielarifriedman.com/domains.html#page",
                "name": "Research Domains — Daniel Ari Friedman",
                "description": "Domain landing pages for Daniel Ari Friedman's research, software, collaborators, and learning pathways.",
                "url": "https://danielarifriedman.com/domains.html",
                "isPartOf": {"@id": "https://danielarifriedman.com/#website"},
                "dateModified": generated_date(),
            }],
        )
        + f"""
    <header class="domain-hero">
        <h1>Research Domains</h1>
        <p>Entry points through the bibliography, software catalog, collaborator network, and learning pathways.</p>
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
            <a href="discovery.html" class="btn btn-outline">Discovery</a>
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
        for item in config.learning_path:
            # Clean HTML tags and fix relative links for pages/ subdirectory context
            md_item = strip_html_tags(item)
            lines.append(f"- {md_item}")
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
    enrichments = load_json("data/work-enrichment.json").get("works", {})
    outputs = {REPO_ROOT / "domains.html": render_domains_index(works, repos)}
    for config in DOMAINS:
        outputs[REPO_ROOT / f"domain-{config.slug}.html"] = render_domain_page(config, works, repos, enrichments)
    outputs[REPO_ROOT / "pages" / "DOMAINS.md"] = render_domains_md(works, repos)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated pages are stale")
    args = parser.parse_args()
    outputs = render_outputs()
    stale = (
        [str(path.relative_to(REPO_ROOT)) for path in stale_output_paths(outputs, repo_root=REPO_ROOT)]
        if args.check
        else []
    )
    if not args.check:
        write_output_texts(outputs, repo_root=REPO_ROOT)
    if stale:
        raise SystemExit("Stale generated domain pages: " + ", ".join(stale))
    action = "checked" if args.check else "wrote"
    print(f"{action} {len(outputs)} domain pages")


if __name__ == "__main__":
    main()
