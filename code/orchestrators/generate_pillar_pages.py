#!/usr/bin/env python3
"""Generate or verify the five high-authority pillar content explainers."""

import argparse
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "code" / "src"
sys.path.insert(0, str(SRC_DIR))

from generated_outputs import stale_output_paths, write_output_texts  # noqa: E402
from site_nav import (  # noqa: E402
    INTERACTIVE_SCRIPTS,
    MENU_ESC_SCRIPT,
    render_breadcrumb,
    render_nav_domain,
    render_pillar_head,
)

STYLE_BLOCK = """
        .pillar-content{max-width:880px;margin:0 auto;padding:7.5rem 1.5rem 4rem;line-height:1.8;color:var(--text-primary)}
        .pillar-header{margin-bottom:2.5rem;text-align:left;border-bottom:1px solid var(--border);padding-bottom:1.5rem}
        .pillar-header h1{font-family:Georgia,'Times New Roman',serif;font-size:clamp(2.2rem,4.5vw,3.4rem);line-height:1.15;margin-bottom:1rem;color:#fff}
        .pillar-meta{font-size:.9rem;color:var(--text-secondary);display:flex;flex-wrap:wrap;gap:1.5rem;margin-top:1rem}
        .pillar-meta span strong{color:var(--silver-bright)}
        .pillar-content h2{font-family:Georgia,'Times New Roman',serif;font-size:1.75rem;margin:2.5rem 0 1rem;color:#fff;border-bottom:1px solid var(--border);padding-bottom:.5rem}
        .pillar-content h3{font-size:1.25rem;margin:1.8rem 0 .75rem;color:var(--gold)}
        .pillar-content p{margin-bottom:1.4rem;font-size:1.02rem;color:var(--text-secondary)}
        .pillar-content ul,.pillar-content ol{margin:1rem 0 1.5rem 1.5rem;color:var(--text-secondary)}
        .pillar-content li{margin-bottom:.5rem;font-size:1rem}
        .answer-box{background:var(--bg-card);border-left:4px solid var(--gold);padding:1.4rem;margin-bottom:2rem;border-radius:0 8px 8px 0}
        .answer-box p{margin-bottom:0;font-size:1.1rem;color:var(--text-primary);font-weight:500;line-height:1.7}
        .callout-card{background:var(--bg-card);border:1px solid var(--border);border-radius:8px;padding:1.4rem;margin:1.5rem 0}
        .callout-card h4{color:var(--gold);margin-bottom:.5rem;font-size:1rem;text-transform:uppercase;letter-spacing:.05em}
        .faq-block{margin-top:3rem;background:var(--bg-card);border:1px solid var(--border);border-radius:12px;padding:2rem}
        .faq-item{margin-bottom:1.75rem;border-bottom:1px solid var(--border);padding-bottom:1.25rem}
        .faq-item:last-child{margin-bottom:0;border-bottom:none;padding-bottom:0}
        .faq-item h3{font-size:1.15rem;color:#fff;margin-bottom:.5rem}
"""


def render_page(
    filename: str,
    title: str,
    description: str,
    og_image: str,
    eyebrow: str,
    h1_text: str,
    answer_lead: str,
    sections: list[tuple[str, str]],
    faqs: list[tuple[str, str]],
    domain_url: str,
    domain_name: str,
    terms: list[str],
) -> str:
    canonical_url = f"https://danielarifriedman.com/{filename}"
    faq_items = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in faqs
    ]
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": f"{canonical_url}#article",
                "isPartOf": {"@id": "https://danielarifriedman.com/#website"},
                "headline": title,
                "description": description,
                "url": canonical_url,
                "author": {"@id": "https://danielarifriedman.com/#person"},
                "publisher": {"@id": "https://danielarifriedman.com/#person"},
                "datePublished": "2026-08-14",
                "dateModified": "2026-08-14",
                "inLanguage": "en-US",
                "mainEntityOfPage": canonical_url,
                "about": [{"@type": "DefinedTerm", "name": t} for t in terms],
            },
            {
                "@type": "FAQPage",
                "@id": f"{canonical_url}#faq",
                "mainEntity": faq_items,
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://danielarifriedman.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Domains", "item": "https://danielarifriedman.com/domains.html"},
                    {"@type": "ListItem", "position": 3, "name": domain_name, "item": canonical_url},
                ],
            },
        ],
    }

    sec_html = []
    for h2, body in sections:
        sec_html.append(f"        <h2>{h2}</h2>\n        {body}")
    sec_str = "\n\n".join(sec_html)

    faq_html = []
    for q, a in faqs:
        faq_html.append(f'            <div class="faq-item"><h3>{q}</h3><p>{a}</p></div>')
    faq_str = "\n".join(faq_html)

    return render_pillar_head(
        title=title,
        description=description,
        canonical_path=filename,
        og_image=og_image,
        style=STYLE_BLOCK,
        jsonld=jsonld,
    ) + f"""<body>
    <a href="#main" class="skip-link">Skip to main content</a>
{render_nav_domain(active="domains")}
{render_breadcrumb([("Home", ""), ("Domains", "domains.html"), (domain_name, filename)])}
    <main id="main" class="pillar-content">
        <header class="pillar-header">
            <p class="eyebrow" style="color:var(--gold);font-weight:600;text-transform:uppercase;letter-spacing:0.08em;font-size:0.85rem;margin-bottom:0.5rem;">{eyebrow}</p>
            <h1>{h1_text}</h1>
            <div class="pillar-meta">
                <span>Author: <strong>Daniel Ari Friedman, PhD</strong></span>
                <span>Affiliation: <strong>Active Inference Institute</strong></span>
                <span>Last updated: <strong>2026-08-14</strong></span>
                <span>Domain: <a href="{domain_url}" style="color:var(--gold);">{domain_name}</a></span>
            </div>
        </header>

        <div class="answer-box">
            <p>{answer_lead}</p>
        </div>

{sec_str}

        <section class="faq-block">
            <h2 style="font-size:1.6rem;margin-top:0;border-bottom:none;">Frequently Asked Questions</h2>
{faq_str}
        </section>
    </main>

    <footer role="contentinfo">
        <div class="footer-rule" aria-hidden="true"></div>
        <p>Daniel Ari Friedman, PhD · <a href="https://activeinference.institute/">Active Inference Institute</a> · <a href="index.html">danielarifriedman.com</a></p>
        <div class="footer-links">
            <a href="index.html">Home</a>
            <a href="publications.html">Publications</a>
            <a href="domains.html">Domains</a>
            <a href="software.html">Software</a>
            <a href="discovery.html">Discovery</a>
            <a href="cite-verify.html">Cite &amp; Verify</a>
        </div>
    </footer>
{INTERACTIVE_SCRIPTS}
    {MENU_ESC_SCRIPT}
</body>
</html>
"""


def render_outputs(*, output_root: Path = REPO_ROOT) -> dict[Path, str]:
    """Render every source-owned pillar page without writing it."""
    outputs: dict[Path, str] = {}
    # 1. Cognitive Security
    cogsec_html = render_page(
        filename="cognitive-security.html",
        title="What Is Cognitive Security? Theory, Threat Models, and Multi-Agent Defense",
        description="Cognitive security protects human and artificial sensemaking against adversarial narrative manipulation, epistemic corruption, and coordination degradation.",
        og_image="og-cognitive-security-pillar.jpg",
        eyebrow="Research Synthesis & Foundational Guide",
        h1_text="What Is Cognitive Security? Theory, Threat Models, and Multi-Agent Defense",
        answer_lead="<strong>Cognitive security (CogSec)</strong> is the systematic engineering, behavioral, and formal discipline dedicated to defending human and artificial agents from the adversarial manipulation of belief formation, narrative ecosystems, and collective sensemaking. While classical cybersecurity protects data in transit and silicon at rest, cognitive security safeguards the integrity of inference and decision-making across distributed socio-technical networks.",
        sections=[
            ("What Is Cognitive Security and Why Is It Necessary?",
             "<p>In modern networked environments, information abundance has created a severe scarcity of attentional and epistemic capacity. Cognitive security emerged as an explicit discipline to address vulnerabilities that operate not at the software layer, but at the psychological, perceptual, and semantic layers of communicative interaction. As explored in foundational work across the <a href='works/Friedman2022StructuringInformationCommonsOpen071.html'>Information Commons framework</a> (David, Cordes & Friedman, 2022) and empirical studies on <a href='works/Friedman2024BridgingGapsImageMeme031.html'>image meme ecosystems</a>, malicious actors routinely exploit biological heuristics, affective biases, and automated feedback loops to destabilize institutional trust and democratic coordination.</p>\n"
             "<p>The imperative for cognitive security stems from three fundamental shifts in the global communication architecture:</p>\n"
             "<ul><li><strong>Algorithmic Amplification of Affect:</strong> Platform recommendation algorithms optimize for engagement rather than epistemic fidelity, structurally favoring high-arousal, divisive, and sensational claims.</li>\n"
             "<li><strong>Generative Epistemic Pollution:</strong> Large language models (LLMs) and synthetic media enable cheap, infinite generation of plausible falsehoods, undermining consensus reality and elevating verification costs exponentially.</li>\n"
             "<li><strong>Multi-Agent Coordination Vulnerabilities:</strong> Autonomous AI agents deployed in business, governance, and research workflows are vulnerable to semantic poisoning, context hijacking, and indirect prompt injection that compromise their objective execution.</li></ul>"),
            ("How Does Cognitive Security Differ From Information Security?",
             "<p>A persistent point of confusion in organizational policy is conflating <em>Information Security (InfoSec)</em> with <em>Cognitive Security (CogSec)</em>. While complementary, their security boundaries, threat models, and validation criteria are fundamentally distinct:</p>\n"
             "<div class='callout-card'><h3>InfoSec vs. CogSec: Core Comparison</h3><ul>\n"
             "<li><strong>Target Layer:</strong> InfoSec defends digital assets, cryptographic keys, servers, and communication protocols (OSI Layers 1–7). CogSec defends internal beliefs, generative world models, narrative coherence, and decision policies (the cognitive and socio-institutional layer).</li>\n"
             "<li><strong>Integrity Metric:</strong> InfoSec evaluates byte-level checksums, cryptographic signatures, and unauthorized system access. CogSec evaluates semantic validity, epistemic grounding, evidentiary provenance, and cognitive agency.</li>\n"
             "<li><strong>Threat Modality:</strong> InfoSec prevents malware execution, distributed denial of service (DDoS), and memory corruption. CogSec mitigates narrative laundering, precision-weighting manipulation, context distortion, and coordinated inauthentic behavior.</li>\n"
             "</ul></div>\n"
             "<p>An attacker executing a cognitive campaign does not need to compromise server firewalls or crack encryption algorithms. If the attacker can induce an adversary or the public to interpret valid, uncorrupted facts through a distorted causal frame, the strategic outcome is achieved with zero InfoSec alarms raised.</p>"),
            ("What Is the Foundational COGSEC Trilogy: IRT-20, NIM-21, and CAT-22?",
             "<p>A comprehensive understanding of cognitive security requires formal models of communicative landscapes and threat propagation. Between 2020 and 2022, Daniel Ari Friedman, R.J. Cordes, and collaborators authored the foundational three-volume architectural curriculum on cognitive infrastructure:</p>\n"
             "<ol>\n"
             "<li><strong>IRT-20 — Information and Rhetorical Topography (2020):</strong> Published as <a href='works/Friedman2020ReimaginingMaps148.html'>Reimagining Maps</a> and associated monographs, IRT-20 establishes mathematical and topological frameworks for mapping narrative spaces. By treating rhetoric and argumentation as geometric fields with coordinate distances, resistance metrics, and flow gradients, researchers can quantitatively measure how ideas propagate across socio-cultural topologies.</li>\n"
             "<li><strong>NIM-21 — Narrative Information Management (2021):</strong> Documented in <a href='works/Friedman2021NarrativeInformationManagement080.html'>Narrative Information Management: A Primer</a>, NIM-21 establishes operational protocols for cataloging, categorizing, and tracking narrative vectors over time. It introduces ledger-based provenance tools that allow organizations to map competing narratives, trace semantic drift, and maintain institutional memory under crisis conditions.</li>\n"
             "<li><strong>CAT-22 — Collaborative Adversarial Threat Modeling (2022):</strong> Expanding on <a href='works/Friedman2020EmergentTeamsComplexThreats085.html'>Emergent Teams for Complex Threats</a> and the <a href='works/Friedman2021FacilitatorSCatechismPlaybook081.html'>Facilitator's Catechism</a>, CAT-22 presents structured team protocols for red-teaming cognitive operations. It integrates decentralized facilitation tools with intelligence analysis techniques to assess institutional vulnerability before hostile narrative campaigns take root.</li>\n"
             "</ol>"),
            ("How Does Active Inference Provide a Mathematical Foundation for Cognitive Security?",
             "<p>At its core, cognition is an ongoing process of inference. Under the <strong>Free Energy Principle (FEP)</strong> and <strong>Active Inference</strong> framework pioneered by Karl Friston and formalized computationally in research such as <a href='works/Friedman2021ActiveInferantsActiveInference075.html'>Active Inferants</a> (Friedman et al., 2021) and <a href='works/Friedman2026TowardsLean4Formalization113.html'>FEP Lean 4 Formalization</a> (2026), an organism or cognitive agent survives by minimizing variational free energy—a mathematical bound on Bayesian surprise.</p>\n"
             "<p>An Active Inference model of cognitive security reveals that cognitive threats operate by attacking the agent's <em>precision optimization</em>:</p>\n"
             "<ul>\n"
             "<li><strong>Precision Hijacking:</strong> Agents assign precision (inverse variance / confidence) to sensory inputs versus prior expectations. Cognitive attacks artificially inflate precision on sensational signals (creating fixation) or degrade precision on authoritative evidence (creating generalized nihilism).</li>\n"
             "<li><strong>Markov Blanket Exploitation:</strong> The statistical boundary separating an agent's internal states from the external environment (the Markov blanket) relies on reciprocal action-perception cycles. Adversarial actors flood sensory channels with coordinated contradictory evidence, driving up free energy until the agent's generative model collapses into hyper-reactive or fragmented states.</li>\n"
             "<li><strong>Generative Model Drift:</strong> When deceptive signals are systematically repeated, the agent's long-term prior beliefs (the transition matrices and prior preference distributions in discrete-state space models) update to internalize the malicious priors, locking the agent into self-reinforcing delusion.</li>\n"
             "</ul>"),
            ("What Is the Cognitive Integrity Framework for Autonomous AI Agents?",
             "<p>As autonomous AI agents and multi-agent swarms take on mission-critical responsibilities in scientific discovery, data analysis, and software orchestration, cognitive security extends beyond human psychology to machine cognition. The <a href='works/Friedman2026CognitiveIntegrityFrameworkFormal005.html'>Cognitive Integrity Framework (CIF-26)</a> provides formal guarantees for multi-agent systems:</p>\n"
             "<ol>\n"
             "<li><strong>Provenance-Bound Claims:</strong> Every generative assertion must carry cryptographic or traceable pointers to source data, preventing hallucination cascading across collaborative agent chains.</li>\n"
             "<li><strong>Non-Monotonic Epistemic Auditing:</strong> Systems must maintain verifiable absence ledgers (such as the <a href='works/Friedman2026WhiteLineTypedLedger202.html'>White Line Ledger</a>) and explicit red lines (<a href='works/Friedman2026PersonalRedLinesDevelopment203.html'>Personal Red Lines</a>) to ensure agent self-improvement remains within bounded, verified parameter regimes.</li>\n"
             "<li><strong>Typological and Categorical Invariants:</strong> Employing formal commutative diagrams as specified in <a href='works/Friedman2026CompositionalApproachesLinguisticCase112.html'>Cognitive Case Diagrams</a>, multi-agent messages must preserve algebraic consistency across relational transformations, immunizing agent swarms against prompt injection and semantic drift.</li>\n"
             "</ol>"),
            ("How Does the AMITT Framework and Epistemic Architecture Function in Practice?",
             "<p>The <strong>Adversarial Misinformation and Influence Tactics and Techniques (AMITT)</strong> framework—modeled on the MITRE ATT&CK framework in classical InfoSec—provides an operational taxonomy for cognitive defenders. By mapping the full incident lifecycle from initial reconnaissance (target audience analysis, sentiment mapping) through weaponization (narrative drafting, meme synthesis), delivery (bot amplification, sockpuppet networks), to exploitation (polarization, institutional paralysis), AMITT enables structured response playbooks.</p>\n"
             "<p>Practical cognitive defense combines three structural pillars:</p>\n"
             "<ul>\n"
             "<li><strong>Defensive Information Architecture:</strong> Developing open, decentralized standards for knowledge commons, as articulated in the <a href='works/Friedman2022StructuringInformationCommonsOpen071.html'>Structuring Information Commons</a> series and <a href='works/Friedman2023ATLASQuestionOrientedApproach136.html'>ATLAS pattern language</a>.</li>\n"
             "<li><strong>Verifiable Citation Infrastructure:</strong> Embedding machine-readable metadata, cryptographic proofs, and reproducible artifacts (exemplified by the <a href='cite-verify.html'>Cite & Verify infrastructure</a>) into public communications to make claims independently auditable.</li>\n"
             "<li><strong>Civic and Institutional Cognitive Ergonomics:</strong> Designing digital interfaces that reduce cognitive friction for deep comprehension while increasing friction on reflexive, unverified dissemination.</li>\n"
             "</ul>"),
        ],
        faqs=[
            ("What is cognitive security?", "Cognitive security is the interdisciplinary field dedicated to protecting the cognitive processes of individuals, organizations, and AI systems from adversarial manipulation, epistemic corruption, and narrative warfare."),
            ("How does cognitive security relate to cybersecurity?", "Cybersecurity protects digital devices, servers, and data transmissions. Cognitive security protects the human and algorithmic understanding derived from that data. An attacker can achieve complete cognitive compromise through perfectly secure communication channels."),
            ("What are the primary tools used in cognitive security?", "Cognitive security employs narrative tracking ledgers (such as NIM), Active Inference generative modeling, AMITT threat taxonomy mapping, formal case-theoretic verification diagrams, and cryptographically verifiable citation systems."),
            ("Where can I study peer-reviewed literature on cognitive security?", "Explore the unified Cognitive Security Domain Index at <a href='domain-cognitive-security.html'>domain-cognitive-security.html</a>, open-source repositories like <a href='https://github.com/docxology/p3if'>P3IF</a> and <a href='https://github.com/docxology/opentir'>OpenTIR</a>, and foundational texts published via COGSEC.org and the Active Inference Institute."),
        ],
        domain_url="domain-cognitive-security.html",
        domain_name="Cognitive Security",
        terms=["Cognitive Security", "Active Inference", "Epistemic Security", "Narrative Topography"],
    )
    outputs[output_root / "cognitive-security.html"] = cogsec_html

    # 2. Computational Entomology
    comp_ento_html = render_page(
        filename="computational-entomology.html",
        title="Computational Entomology: Algorithms, Models, and Digital Insect Colonies",
        description="Computational entomology applies algorithmic modeling, Active Inference, and genomic analysis to decipher social insect behavior and bio-inspired computing.",
        og_image="og-computational-entomology.jpg",
        eyebrow="Domain Deep-Dive & Computational Foundations",
        h1_text="Computational Entomology: Algorithms, Models, and Digital Insect Colonies",
        answer_lead="<strong>Computational entomology</strong> is the intersection of entomological biology, computational modeling, and information theory dedicated to simulating, analyzing, and formalizing insect behavior from molecular neurogenomics to whole-colony collective intelligence. By translating biological observations into algorithmic systems, it uncovers principles of decentralized control, self-organization, and adaptive resilience.",
        sections=[
            ("What Is Computational Entomology and How Did It Develop?",
             "<p>Entomology has historically relied on field ethology and anatomical taxonomy. However, understanding how thousands of sterile social insect workers cooperate without centralized orchestration requires quantitative, mathematical, and algorithmic tools. <strong>Computational entomology</strong> bridges biological experimentation and computational science by treating individual insects as embodied computational agents and the colony as a distributed computing network.</p>\n"
             "<p>Pioneering work in harvester ant (<em>Pogonomyrmex barbatus</em>) foraging ecology—including field-tested genomic analysis in <a href='works/Friedman2020GeneExpressionVariationBrains086.html'>Gene Expression Variation in Brains of Harvester Ant Foragers</a> (Friedman et al., <em>Communications Biology</em> 2020) and physiological measurements in <a href='works/Friedman2019PhysiologyForagerHydrationVariation095.html'>Physiology of Forager Hydration Variation</a> (Friedman et al., 2019)—demonstrated that colony-level decision-making emerges from local interaction rates and neuromodulatory dynamics (such as octopamine and dopamine regulation) rather than centralized commands.</p>"),
            ("How Are Insect Colonies Modeled as Distributed Computational Systems?",
             "<p>Social insect colonies solve complex optimization problems that parallel fundamental challenges in distributed computing, including packet routing, load balancing, consensus protocols, and task allocation under environmental uncertainty:</p>\n"
             "<ul>\n"
             "<li><strong>Interaction-Rate Task Allocation:</strong> Harvester ant colonies regulate foraging activity using antenna-to-antenna contact rates. When returning foragers carrying seeds enter the nest at high frequency, outgoing foragers infer high food availability and low desiccation risk, initiating foraging trips without any individual knowing the global reserve status.</li>\n"
             "<li><strong>Pheromone Trail Optimization and Stigmergy:</strong> Foraging trails represent living spatial computing networks. As formalized in <a href='works/Friedman2023SinglePheromoneModelAccounts046.html'>A Single Pheromone Model of Foraging Trails</a> (Friedman, 2023), volatile chemical gradients enact positive feedback (trail reinforcement) and negative feedback (evaporation), dynamically computing shortest paths in fluctuating terrains.</li>\n"
             "<li><strong>Decentralized Colony Energetics:</strong> In <a href='works/Friedman2025ComputationalComplexityEnergeticsAnt011.html'>Computational Complexity and Energetics in Ant Colonies</a> (Friedman, 2025), ant colony task allocation is proven to operate within polynomial-time complexity bounds, optimizing caloric expenditure against metabolic search costs.</li>\n"
             "</ul>"),
            ("What Computational Frameworks and Software Scaffold Modern Entomology?",
             "<p>Modern computational entomology relies on rigorous, open-source software scaffolds that unify behavioral simulations, computer vision tracking, and linguistic term standardization:</p>\n"
             "<div class='callout-card'><h3>Key Software Platforms in Computational Entomology</h3><ul>\n"
             "<li><strong><a href='https://github.com/docxology/BeeStack'>BeeStack</a>:</strong> An evidence-typed computational scaffold for whole-colony honeybee (<em>Apis mellifera</em>) simulation, integrating thermal regulation, comb construction algorithms, and foraging energetics (<a href='works/Friedman2026BeeStackEvidenceTypedScaffold125.html'>Friedman & Chambers, 2026</a>).</li>\n"
             "<li><strong><a href='https://github.com/ActiveInferenceInstitute/COGANT'>COGANT</a>:</strong> Deterministic Codebase-to-GNN translation engine that compiles codebase architectures and agent interaction rules into formal Generalized Notation Notation Active Inference graphs (<a href='works/Friedman2026COGANTDeterministicCodebaseGNN169.html'>Friedman, 2026</a>).</li>\n"
             "<li><strong><a href='https://github.com/docxology/ento_linguistics'>Ento-Linguistics</a>:</strong> Natural language processing and corpus pipeline that extracts terminology networks and semantic entropy scores from entomological literature (<a href='works/Friedman2026EntoLinguisticsLanguageAmbiguity109.html'>Friedman & Chambers, 2026</a>).</li>\n"
             "<li><strong><a href='https://github.com/docxology/MetaInformAnt'>MetaInformAnt</a> &amp; <a href='https://github.com/docxology/ActiveInferAnts'>ActiveInferAnts</a>:</strong> Python simulations implementing discrete Markov Decision Processes to model ant behavioral transitions as active Bayesian inference.</li>\n"
             "</ul></div>"),
            ("How Does Neurogenomics Integrate With Behavioral Simulation?",
             "<p>A distinctive contribution of computational entomology is linking transcriptomic gene expression directly to behavioral phenotypes. In <a href='works/Friedman2018RoleDopamineCollectiveRegulation100.html'>The Role of Dopamine in Collective Regulation of Foraging</a> (Friedman et al., 2018), neuropharmacological experiments demonstrated that dopamine increases harvester ant foraging propensity. Computational analysis of RNA sequencing data (<a href='works/Friedman2019PhDBehavioralPhysiologicalTranscriptomic093.html'>Friedman, Stanford PhD Dissertation 2019</a>) revealed differential expression of biogenic amine receptor genes and circadian clock components between patrollers, foragers, and nest-maintenance workers.</p>\n"
             "<p>By mapping differential gene expression networks into agent-based parameters, computational entomology creates multi-scale models where molecular-level changes quantitatively predict colony-level collective shifts under climatic and ecological stress.</p>"),
            ("What Are the Applications of Computational Entomology in AI and Robotics?",
             "<p>Bio-inspired algorithms derived from computational entomology have widespread engineering and robotic applications:</p>\n"
             "<ul>\n"
             "<li><strong>Swarm Robotics:</strong> Designing autonomous robotic swarms that coordinate without GPS or central communications, utilizing local sensor contact rates and digital stigmergy for search-and-rescue and planetary exploration.</li>\n"
             "<li><strong>Robust Communication Routing:</strong> Network protocols modeled on ant foraging algorithms that dynamically reroute data packets around damaged infrastructure in mobile ad-hoc networks (MANETs).</li>\n"
             "<li><strong>Multi-Agent Resource Allocation:</strong> Cloud computing resource schedulers that allocate compute tasks across distributed server clusters using threshold-based response models derived from social insect caste polyethism.</li>\n"
             "</ul>"),
        ],
        faqs=[
            ("What is computational entomology?", "Computational entomology is the application of computational models, agent-based simulations, information theory, and bioinformatics to study insect physiology, neurogenomics, and collective social behavior."),
            ("How do ant colonies compute without a leader?", "Ant colonies achieve collective computation through stigmergy (modifying the local environment via pheromones), antenna contact interaction rates, and threshold-based response curves embedded in each individual worker's sensory-behavioral loops."),
            ("What software is available for computational entomology research?", "Open-source tools include BeeStack (honeybee simulation), COGANT (codebase-to-graph compiler), Ento-Linguistics (NLP corpus extraction), and MetaInformAnt / ActiveInferAnts (Active Inference simulations), accessible via docxology on GitHub."),
            ("Where can I find peer-reviewed papers on computational entomology?", "Explore the <a href='domain-entomology.html'>Entomology Domain Hub</a> on this site, which indexes 23+ peer-reviewed papers published in Communications Biology, Cell, iScience, Frontiers, and Zenodo."),
        ],
        domain_url="domain-entomology.html",
        domain_name="Entomology",
        terms=["Computational Entomology", "Ant Colony Optimization", "Collective Behavior", "Stigmergy", "Bio-Inspired Computing"],
    )
    outputs[output_root / "computational-entomology.html"] = comp_ento_html

    # 3. Insect Cognition
    insect_cog_html = render_page(
        filename="insect-cognition.html",
        title="Insect Cognition & Collective Intelligence: How Ant Colonies Think Without a Brain",
        description="How social insects achieve complex cognition, navigate using Bayesian principles, and solve distributed computational tasks without central neural control.",
        og_image="og-insect-cognition.jpg",
        eyebrow="Cognitive Biology & Distributed Intelligence",
        h1_text="Insect Cognition & Collective Intelligence: How Ant Colonies Think Without a Brain",
        answer_lead="<strong>Insect cognition and collective intelligence</strong> is the study of how individual social insects—and the superorganism colonies they form—process sensory information, update internal beliefs, solve multi-criteria optimization problems, and adapt to environmental uncertainty. While an individual ant possesses roughly 250,000 neurons, the collective colony functions as an integrated cognitive system capable of sophisticated learning, memory, and distributed decision-making.",
        sections=[
            ("How Do Insect Brains Compare to Vertebrate Cognitive Systems?",
             "<p>For decades, comparative psychology assumed that complex cognitive capabilities required large vertebrate brains with cerebral cortices. Research across hymenopteran species (ants, bees, and wasps) has overturned this dogma. Despite possessing central nervous systems measured in cubic millimeters, individual insects exhibit numerical cognition, rule abstraction, non-associative learning, metacognitive uncertainty monitoring, and complex multisensory integration.</p>\n"
             "<p>As detailed in <a href='works/Friedman2018WoodliceMenBayesianAccount098.html'>Of Woodlice and Men: A Bayesian Account of Cognition, Life and Consciousness</a> (Friedman & Ramstead, 2018), cognition is fundamentally an embodied process of Bayesian inferential regulation. The insect mushroom bodies—dense neuropils containing hundreds of thousands of Kenyon cells—function analogously to mammalian associative cortices and hippocampal networks, supporting spatial mapping, olfactory memory consolidation, and context-dependent action selection.</p>"),
            ("Can an Ant Colony Be Understood as a Cognitive Superorganism?",
             "<p>The concept of the <strong>superorganism</strong>—popularized by William Morton Wheeler and refined by E.O. Wilson and Bert Hölldobler—posits that a social insect colony is an integrated biological entity where individual workers are functionally analogous to cells or tissues in a metazoan body. In computational cognitive biology, this analogy is extended to neural computation:</p>\n"
             "<ul>\n"
             "<li><strong>Workers as Neurons:</strong> Individual workers act as excitable units that integrate sensory inputs (antennal touch, pheromone plumes, temperature, optical flow) and transmit state changes to neighbors through localized chemical and mechanical contact.</li>\n"
             "<li><strong>Colony Memory:</strong> Information is stored not solely within worker brains, but in the structural topology of the nest, spatial distribution of castes, and dynamic gradients of trail pheromones. A colony can maintain spatial memories of profitable food sites across weeks even as individual foraging cohorts turn over completely.</li>\n"
             "<li><strong>Collective Attention:</strong> In <a href='works/Friedman2020DistributedPhysiologyMolecularBasis084.html'>Distributed Physiology and the Molecular Basis of Social Insect Behavior</a> (Friedman, 2020), attention is formalized as dynamic precision-weighting across sensory modalities, where the colony shifts resources toward hydration defense, brood care, or territorial warfare based on integrated cue thresholds.</li>\n"
             "</ul>"),
            ("What Is Active Inference for Ant Colonies (Active Inferants)?",
             "<p>In 2021, Daniel Ari Friedman, Alec Tschantz, Maxwell J. D. Ramstead, Karl Friston, and Axel Constant published <a href='works/Friedman2021ActiveInferantsActiveInference075.html'>Active Inferants: An Active Inference Framework for Ant Colony Behavior</a> in <em>Frontiers in Behavioral Neuroscience</em>. The paper established the first formal mathematical framework applying the Free Energy Principle to social insect collective behavior.</p>\n"
             "<p>Under the Active Inferants framework:</p>\n"
             "<ol>\n"
             "<li><strong>Generative Model of the Colony:</strong> Individual ants are modeled as discrete-state Bayesian agents possessing generative models of external hidden states (environmental food abundance, climatic desiccation risk, competitor presence).</li>\n"
             "<li><strong>Variational Free Energy Minimization:</strong> Worker task switching emerges naturally as agents select actions that minimize variational free energy (resolving ambiguity and fulfilling homeostatic prior preferences for seed reserves).</li>\n"
             "<li><strong>Stigmergic Belief Sharing:</strong> Pheromone deposition acts as an epistemic action that modifies the sensory niche, allowing ants to share posterior beliefs about food locations without direct symbolic communication (<a href='works/Friedman2024SharedProtentionsMultiAgent040.html'>Shared Protentions in Multi-Agent Active Inference</a>, 2024).</li>\n"
             "</ol>"),
            ("Do Individual Ants Possess Personalities and Behavioral Variation?",
             "<p>Far from being identical automata, individual ants display consistent inter-individual behavioral variation (animal personality). Empirical investigations into harvester ant foragers (<a href='works/Friedman2016ContextDependentExpressionForaging104.html'>Context-Dependent Gene Expression</a>, <em>Communications Biology</em>; <a href='works/Friedman2020GeneExpressionVariationBrains086.html'>Friedman et al., 2020</a>) demonstrated that individual workers differ consistently in exploration propensity, risk tolerance, and response thresholds to dehydration.</p>\n"
             "<p>This individual-level behavioral heterogeneity is functionally crucial for the colony: it prevents catastrophic synchronized over-reactions to transient environmental noise, providing an optimal blend of exploitative stability and exploratory flexibility across the colony swarm.</p>"),
            ("How Does Stigmergy Drive Problem Solving Without Centralized Coordination?",
             "<p><strong>Stigmergy</strong>—a term introduced by French biologist Pierre-Paul Grassé in 1959—describes a mechanism of indirect coordination where the trace left in the environment by an action stimulates the next action by the same or different agents. In social insects, stigmergy enables:</p>\n"
             "<div class='callout-card'><h3>Stigmergic Coordination Modalities</h3><ul>\n"
             "<li><strong>Architectural Stigmergy:</strong> Termite and ant mound construction operates through local pheromone-cement accumulation. Workers deposit soil pellets impregnated with pheromone; subsequent workers are attracted to regions of highest concentration, naturally producing arches, pillars, and ventilation shafts without architectural blueprints.</li>\n"
             "<li><strong>Sematectonic Communication:</strong> Modification of physical nest structures (corridor width, grain piles) alters the physical constraints of worker movement, passively guiding colony traffic flows.</li>\n"
             "<li><strong>Quantitative Stigmergic Optimization:</strong> Pheromone networks self-organize to solve traveling salesperson problems, Steiner minimal tree problems, and dynamic bottleneck bypasses in real time.</li>\n"
             "</ul></div>"),
        ],
        faqs=[
            ("Do ants have individual brains?", "Yes, an individual ant possesses a brain containing roughly 250,000 neurons, equipped with complex sensory lobes and mushroom bodies that support learning, visual navigation, and olfactory recognition."),
            ("How does an ant colony make decisions without a leader?", "The queen reproduces and does not command. Decisions emerge through decentralized feedback loops: worker interaction rates, threshold-based task switching, and stigmergic environmental cues (such as trail pheromones) that aggregate collective information."),
            ("What is the Active Inferants framework?", "Active Inferants (Friedman et al., 2021, Frontiers in Behavioral Neuroscience) is a mathematical framework that models ant colonies as hierarchical Bayesian systems minimizing prediction error (free energy) across individual workers and the superorganism niche."),
            ("Where can I learn more about insect cognition research?", "Review the cataloged publications in the <a href='domain-entomology.html'>Entomology Domain Hub</a>, the <a href='domain-active-inference.html'>Active Inference Domain Hub</a>, and the foundational papers on harvester ant behavior indexed across this site."),
        ],
        domain_url="domain-entomology.html",
        domain_name="Entomology",
        terms=["Insect Cognition", "Collective Intelligence", "Active Inferants", "Superorganism", "Stigmergy"],
    )
    outputs[output_root / "insect-cognition.html"] = insect_cog_html

    # 4. Active Inference Tutorial
    actinf_html = render_page(
        filename="active-inference.html",
        title="Active Inference & The Free Energy Principle: A Practical Tutorial",
        description="Comprehensive explanatory tutorial on Active Inference and the Free Energy Principle, covering generative models, Bayesian mechanics, and AI agent implementation.",
        og_image="og-active-inference-tutorial.jpg",
        eyebrow="Foundational Tutorial & Technical Guide",
        h1_text="Active Inference & The Free Energy Principle: A Practical Tutorial",
        answer_lead="<strong>Active Inference</strong> is a unified mathematical framework developed in theoretical neuroscience, cognitive science, and machine learning that describes how sentient agents survive and adapt by minimizing variational and expected free energy. Rather than treating perception, learning, and action selection as separate modules, Active Inference unifies them as Bayesian inference over a single objective function: minimizing surprise relative to a generative model of the world.",
        sections=[
            ("What Is the Free Energy Principle and How Does Active Inference Work?",
             "<p>Originating in the physics of self-organizing non-equilibrium systems and pioneered by neuroscientist Karl Friston, the <strong>Free Energy Principle (FEP)</strong> states that any self-organizing system that resists dissipation and maintains its structural integrity over time must minimize an upper bound on sensory surprise (negative log evidence). <strong>Active Inference</strong> is the process theory that implements this principle for embodied, cognitive agents.</p>\n"
             "<p>Under Active Inference, an agent maintains a <em>generative model</em> of its environment consisting of:</p>\n"
             "<ul>\n"
             r"<li><strong>Hidden States ($s$):</strong> Unobserved latent causes in the world (e.g., whether a predator is present, or the underlying state of a financial market).</li>" + "\n"
             r"<li><strong>Observations ($o$):</strong> Sensory inputs received by the agent (e.g., visual photons, auditory frequencies, telemetry readings).</li>" + "\n"
             r"<li><strong>Actions / Policies ($\pi$):</strong> Sequences of control states that alter the transition probabilities of future hidden states.</li>" + "\n"
             r"<li><strong>Generative Likelihood ($A$-matrix):</strong> The mapping from hidden states to sensory observations, $P(o | s)$.</li>" + "\n"
             r"<li><strong>State Transition Dynamics ($B$-matrix):</strong> How hidden states evolve conditioned on selected actions, $P(s_{t+1} | s_t, a_t)$.</li>" + "\n"
             r"<li><strong>Prior Preferences ($C$-vector):</strong> The agent's internal homeostatic baseline—the sensory states it expects to inhabit to remain viable.</li>" + "\n"
             r"<li><strong>Initial State Priors ($D$-vector):</strong> Baseline prior beliefs over hidden states at initialization, $P(s_0)$.</li>" + "\n"
             "</ul>"),
            ("What Is the Difference Between Variational Free Energy and Expected Free Energy?",
             "<p>A crucial mathematical distinction in Active Inference is the difference between <strong>Variational Free Energy ($F$)</strong> and <strong>Expected Free Energy ($G$)</strong>:</p>\n"
             "<div class='callout-card'><h3>Variational vs. Expected Free Energy</h3><ul>\n"
             r"<li><strong>Variational Free Energy ($F$) [The Present & Past]:</strong> Evaluated on <em>realized observations</em>. Minimizing $F$ optimizes the agent's current internal beliefs ($q(s)$) to match the true posterior distribution over hidden causes, balancing accuracy against complexity (KL divergence between beliefs and priors).</li>" + "\n"
             r"<li><strong>Expected Free Energy ($G$) [The Future & Action Selection]:</strong> Evaluated over <em>counterfactual future observations</em> that have not yet occurred. An agent evaluates candidate policies $\pi$ by computing the expected free energy $G(\pi)$ for future time steps.</li>" + "\n"
             "</ul></div>\n"
             r"<p>Mathematically, minimizing Expected Free Energy $G(\pi)$ naturally decomposes into two complementary imperatives:</p>" + "\n"
             "<ol>\n"
             "<li><strong>Pragmatic Value (Goal Seeking):</strong> Maximizing the expected utility or log likelihood of future observations under prior preferences.</li>\n"
             "<li><strong>Epistemic Value (Information Seeking / Curiosity):</strong> Maximizing information gain or mutual information between future observations and hidden states, actively resolving ambiguity in unobserved domains.</li>\n"
             "</ol>"),
            ("How Does Active Inference Compare to Reinforcement Learning (RL)?",
             "<p>While both Active Inference and Reinforcement Learning model decision-making under uncertainty, their fundamental axioms differ substantially:</p>\n"
             "<ul>\n"
             "<li><strong>Exploration vs. Exploitation:</strong> In standard RL (Q-learning, policy gradients), exploration is an ad-hoc heuristic bolted onto reward maximization. In Active Inference, epistemic exploration (uncertainty reduction) and pragmatic exploitation (preference satisfaction) arise organically from the exact same mathematical objective ($G$).</li>\n"
             "<li><strong>Sample Efficiency:</strong> Active Inference agents maintain explicit probabilistic generative models, allowing them to perform counterfactual rollouts and plan effectively with vastly fewer environment interactions than model-free RL algorithms.</li>\n"
             "<li><strong>Reward Definition:</strong> RL maximizes an arbitrary external scalar reward. Active Inference satisfies self-consistent prior expectations (homeostasis), preventing reward hacking and out-of-distribution value drift.</li>\n"
             "</ul>"),
            ("What Is the Markov Blanket and Bayesian Mechanics?",
             "<p>In the formal physics of Active Inference—known as <strong>Bayesian Mechanics</strong> (<a href='works/Friedman2022WorkedExampleBayesianMechanics143.html'>Worked Example of Bayesian Mechanics</a>, 2022)—the concept of a <strong>Markov Blanket</strong> formalizes the boundary of any cognitive agent. The states of the universe partition into four sets:</p>\n"
             "<ul>\n"
             r"<li><strong>Internal States ($\mu$):</strong> The agent's internal cognitive and computational states.</li>" + "\n"
             r"<li><strong>External States ($\eta$):</strong> The unobserved physical environment outside the agent.</li>" + "\n"
             "<li><strong>Sensory States ($s$):</strong> States that mediate how external states affect internal states.</li>\n"
             "<li><strong>Active States ($a$):</strong> States that mediate how internal states affect external states.</li>\n"
             "</ul>\n"
             "<p>Sensory and active states together constitute the Markov Blanket. Internal and external states are conditionally independent given the blanket, providing a rigorous mathematical definition of agency, individuality, and selfhood across biological and computational scales.</p>"),
            ("What Tools and Frameworks Exist for Implementing Active Inference?",
             "<p>Researchers and software engineers can implement discrete and continuous Active Inference using standard open-source toolkits:</p>\n"
             "<div class='callout-card'><h3>Active Inference Software Ecosystem</h3><ul>\n"
             "<li><strong><a href='https://github.com/ActiveInferenceInstitute/fep_lean'>fep_lean</a>:</strong> Formalization of Free Energy Principle theorems, discrete-state space models, and Bayesian mechanics in the Lean 4 interactive theorem prover (<a href='works/Friedman2026TowardsLean4Formalization113.html'>Friedman, 2026</a>).</li>\n"
             "<li><strong><a href='https://github.com/ActiveInferenceInstitute/COGANT'>COGANT</a> &amp; GNN:</strong> Generalized Notation Notation and automated compiler tools for declarative Active Inference system specification (<a href='works/Friedman2023GeneralizedNotationNotationActive056.html'>GNN Paper, 2023</a>).</li>\n"
             "<li><strong><a href='https://github.com/infer-stat/RxInfer.jl'>RxInfer.jl</a>:</strong> Reactive message-passing probabilistic programming engine in Julia for real-time variational inference.</li>\n"
             "<li><strong>PyMDP:</strong> Python library for discrete-state Markov Decision Process Active Inference models.</li>\n"
             "<li><strong><a href='https://github.com/docxology/CEREBRUM'>CEREBRUM</a>:</strong> Case-Enabled Reasoning Engine with Bayesian Representations for structured multi-agent inference (<a href='works/Friedman2025CEREBRUMCaseEnabledReasoning010.html'>Friedman, 2025</a>).</li>\n"
             "</ul></div>"),
            ("How Can Beginners and Advanced Researchers Learn Active Inference?",
             "<p>The <a href='https://activeinference.institute'>Active Inference Institute (AII)</a>—founded in 2021—provides open scientific education, livestreams, study cohorts, and public research infrastructure:</p>\n"
             "<ol>\n"
             "<li><strong>Textbook Cohorts:</strong> Join structured cohort discussions studying foundational texts (Thomas Parr, Giovanni Pezzulo, & Karl Friston, <em>Active Inference: The Free Energy Principle in Mind, Brain, and Behavior</em>, MIT Press; and Noor Sajid et al.). Over 10 cohorts have completed through 2026.</li>\n"
             "<li><strong>Active Inference Video Archive:</strong> Watch over 1,100 curated livestreams, guest lectures, and model demonstrations indexed in the <a href='videos.html'>Interactive Video Archive</a> and <a href='videos/'>Video Index</a>.</li>\n"
             "<li><strong>Curated Research Index:</strong> Browse the unified <a href='domain-active-inference.html'>Active Inference Domain Hub</a> on this site, indexing over 45 peer-reviewed publications and formal preprints.</li>\n"
             "</ol>"),
        ],
        faqs=[
            ("What is Active Inference in simple terms?", "Active Inference is a theory of mind and intelligent action stating that brains and adaptive agents maintain internal models of their environment and continuously take actions to minimize surprise, confirm predictions, and resolve uncertainty."),
            ("What is the mathematical equation for Variational Free Energy?", "Variational Free Energy represents Complexity minus Accuracy. Minimizing it makes internal beliefs match the true Bayesian posterior given incoming sensory observations."),
            ("How does Active Inference relate to AI agents?", "Active Inference provides AI agents with intrinsic motivation for exploration, robust decision-making under uncertainty, sample-efficient planning via generative models, and transparent belief-updating dynamics without massive trial-and-error reward hacking."),
            ("Where can I find open-source software for Active Inference?", "Check out fep_lean on GitHub for formal mathematical proofs, RxInfer.jl for reactive probabilistic programming, PyMDP for discrete agents, and COGANT for graph-based inference compilation."),
        ],
        domain_url="domain-active-inference.html",
        domain_name="Active Inference",
        terms=["Active Inference", "Free Energy Principle", "Expected Free Energy", "Markov Blanket", "Bayesian Mechanics"],
    )
    outputs[output_root / "active-inference.html"] = actinf_html

    # 5. Neurosymbolic AI
    neuro_html = render_page(
        filename="neurosymbolic-ai.html",
        title="Neurosymbolic AI & Active Inference: Bridging Symbolic Reasoning and Generative Agents",
        description="How Neurosymbolic AI integrates statistical deep learning and generative models with formal logic, knowledge graphs, and Active Inference architectures.",
        og_image="og-neurosymbolic-ai.jpg",
        eyebrow="Advanced AI Architectures & Epistemic Synthesis",
        h1_text="Neurosymbolic AI & Active Inference: Bridging Symbolic Reasoning and Generative Agents",
        answer_lead="<strong>Neurosymbolic artificial intelligence (Neurosymbolic AI)</strong> is the synthesis of statistical, sub-symbolic machine learning (such as deep neural networks and LLMs) with formal, symbolic reasoning (such as logic, knowledge graphs, category theory, and generative Active Inference models). By combining pattern recognition with verifiable symbolic structures, it overcomes the hallucinations, uninterpretability, and brittle reasoning of purely statistical AI.",
        sections=[
            ("What Is Neurosymbolic AI and Why Is Deep Learning Alone Insufficient?",
             "<p>Modern deep learning and generative large language models (LLMs) excel at perceptual pattern recognition, fluent linguistic generation, and statistical interpolation across vast training distributions. However, purely statistical architectures suffer from severe systemic limitations when deployed in high-stakes domains:</p>\n"
             "<ul>\n"
             "<li><strong>Hallucinations and Epistemic Drift:</strong> LLMs generate probabilistically plausible tokens without guaranteed grounding in truth, formal constraints, or physical reality.</li>\n"
             "<li><strong>Brittle Out-of-Distribution Reasoning:</strong> Deep neural networks struggle with compositional generalization, algebraic manipulation, and strict deductive proofs that fall outside their training manifold.</li>\n"
             "<li><strong>Uninterpretable Black Boxes:</strong> Deep representations lack transparent causal structures, making regulatory compliance, auditability, and safety guarantees virtually impossible.</li>\n"
             "</ul>\n"
             "<p><strong>Neurosymbolic AI</strong> addresses these deficiencies by coupling statistical neural perception with explicit, interpretable symbolic knowledge representations, enabling agents that are both perception-rich and logic-governed.</p>"),
            ("How Does Active Inference Bridge the Neural and Symbolic Paradigms?",
             "<p>Active Inference provides a natural mathematical bridge between statistical learning and symbolic reasoning. Rather than maintaining an arbitrary hybrid pipeline, Active Inference formulates inference across discrete, structured categorical spaces:</p>\n"
             "<div class='callout-card'><h3>Active Inference as a Neurosymbolic Architecture</h3><ul>\n"
             "<li><strong>Statistical Likelihoods with Discrete State Spaces:</strong> The generative model uses continuous probability distributions ($A$-matrix likelihood mappings) to ground noisy neural perception while operating over discrete, structured state spaces ($B$-matrix transitions) that represent formal symbolic relations.</li>\n"
             "<li><strong>Categorical and Case-Theoretic Diagrams:</strong> In <a href='works/Friedman2026CompositionalApproachesLinguisticCase112.html'>Cognitive Case Diagrams</a> (Friedman, 2026), commutative category-theoretic diagrams encode the relational invariants of linguistic cases and causal processes, ensuring that inference preserves algebraic consistency across state transformations.</li>\n"
             "<li><strong>Formal Theorem Verification:</strong> The <a href='works/Friedman2026TowardsLean4Formalization113.html'>fep_lean project</a> (2026) verifies Free Energy Principle mathematics in Lean 4, providing formal symbolic proofs that constrain neurosymbolic agent behavior.</li>\n"
             "</ul></div>"),
            ("What Is the AGEINT Framework for Agentic Intelligence?",
             "<p>In 2026, Daniel Ari Friedman published the comprehensive architectural curriculum <a href='works/Friedman2026AGEINTAgenticIntelligence170.html'>AGEINT: Agentic Intelligence</a>. Comprising over 800,000 words of formal specifications, tradecraft scaffolds, and pedagogical pathways, AGEINT defines the operating discipline for neurosymbolic AI agents.</p>\n"
             "<p>The AGEINT architecture establishes three core tiers for hybrid intelligent agents:</p>\n"
             "<ol>\n"
             "<li><strong>Perceptual and Generative Engine:</strong> Foundation models process multimodal inputs, extract candidate entities, and generate initial natural language outputs.</li>\n"
             "<li><strong>Symbolic Provenance and Verification Ledger:</strong> All generated assertions are parsed into typed knowledge graphs, evaluated against strict schema oracles, and verified against evidentiary absence ledgers (<a href='works/Friedman2026WhiteLineTypedLedger202.html'>White Line Ledger</a>).</li>\n"
             "<li><strong>Active Inference Planning Core:</strong> Policy selection is driven by Expected Free Energy minimization, ensuring that agents balance goal achievement with active information gathering and epistemic verification.</li>\n"
             "</ol>"),
            ("What Are Real-World Examples and Implementations of Neurosymbolic AI?",
             "<p>Neurosymbolic architectures are driving transformative breakthroughs across scientific discovery, automated research, and software engineering:</p>\n"
             "<ul>\n"
             "<li><strong><a href='works/Friedman2025DiscoveryEngineAIDriven026.html'>Discovery Engine</a>:</strong> AI-driven literature discovery systems that combine LLM semantic extraction with formal citation graphs and metadata schemas to eliminate citation hallucination.</li>\n"
             "<li><strong><a href='works/Friedman2025CEREBRUMCaseEnabledReasoning010.html'>CEREBRUM</a>:</strong> Case-Enabled Reasoning Engine with Bayesian Representations, using relational frame semantics to model multi-agent negotiations and legal contract analysis.</li>\n"
             "<li><strong><a href='works/Friedman2026COGANTDeterministicCodebaseGNN169.html'>COGANT</a>:</strong> Deterministic compiler that translates raw source code repositories into Generalized Notation Notation (GNN) graph models for formal verification and multi-agent simulation.</li>\n"
             "<li><strong><a href='works/Friedman2026BoundedAutoResearchTinyReproducible120.html'>Bounded Auto-Research (BART)</a>:</strong> Autonomous computational research harnesses that generate hypotheses, write Python simulation scripts, execute unit tests, and iteratively repair proofs without human intervention.</li>\n"
             "</ul>"),
            ("What Is the Future Roadmap for Neurosymbolic Agent Systems?",
             "<p>The convergence of neurosymbolic AI, Active Inference, and formal interactive theorem proving points toward self-verifying, epistemically secure cognitive infrastructure. Future milestones include:</p>\n"
             "<ul>\n"
             "<li><strong>Certified Multi-Agent Protocols:</strong> Communication protocols for agent swarms where every inter-agent message carries machine-checkable proofs of provenance and correctness.</li>\n"
             "<li><strong>Continuous Causal Discovery:</strong> Generative models that continuously induce and update symbolic causal graphs directly from sensory streams using free energy gradients.</li>\n"
             "<li><strong>Decentralized Knowledge Commons:</strong> Open public research repositories where human researchers and neurosymbolic agents collaboratively curate, verify, and cite immutable scholarly ledgers.</li>\n"
             "</ul>"),
        ],
        faqs=[
            ("What is Neurosymbolic AI?", "Neurosymbolic AI is an artificial intelligence paradigm that combines neural network statistical learning (pattern recognition) with symbolic logic (rules, graphs, and deduction) to create transparent, robust, and verifiable intelligent systems."),
            ("Why is Neurosymbolic AI important for eliminating hallucinations?", "Neural LLMs predict statistical word associations without factual constraints. Symbolic verification layers validate model outputs against deterministic knowledge graphs, mathematical rules, and evidentiary ledgers, preventing false claims from propagating."),
            ("How does Active Inference enhance Neurosymbolic AI?", "Active Inference provides a principled Bayesian mechanics framework for updating discrete symbolic states from continuous neural sensory observations while driving curious, information-seeking action selection via Expected Free Energy."),
            ("Where can I read research on Neurosymbolic Active Inference?", "Explore the cataloged works in the <a href='domain-computational.html'>Computational Methods Hub</a> and <a href='domain-active-inference.html'>Active Inference Hub</a>, including AGEINT, CEREBRUM, and COGANT."),
        ],
        domain_url="domain-computational.html",
        domain_name="Computational",
        terms=["Neurosymbolic AI", "Active Inference", "Knowledge Graphs", "Symbolic Reasoning", "AGEINT"],
    )
    outputs[output_root / "neurosymbolic-ai.html"] = neuro_html

    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if any shared-rendered pillar page is stale")
    args = parser.parse_args()
    outputs = render_outputs()
    stale = stale_output_paths(outputs, repo_root=REPO_ROOT)
    if args.check:
        if stale:
            paths = ", ".join(path.relative_to(REPO_ROOT).as_posix() for path in stale)
            raise SystemExit(f"Stale generated pillar pages: {paths}")
        print(f"checked {len(outputs)} shared-rendered pillar pages")
        return
    write_output_texts(outputs, repo_root=REPO_ROOT)
    for path in outputs:
        print(f"Wrote {path.relative_to(REPO_ROOT)}")

    print("All 5 pillar pages authored and generated successfully!")


if __name__ == "__main__":
    main()
