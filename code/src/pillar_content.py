from __future__ import annotations

from docxology_tools.content_citations import ContentCitations


def guides(works: list[dict]) -> list[dict]:
    pages = []

    def page(filename, title, description, image, eyebrow, domain, domain_name, terms, lead, sections, faqs, citations, external_references=()):
        external_html = "".join(f'<li>{text} <a href="{url}">Publication source</a>.</li>' for text, url in external_references)
        pages.append(dict(
            filename=filename, title=title, description=description, og_image=image,
            eyebrow=eyebrow, h1_text=title, answer_lead=lead,
            sections=sections + [("References", citations.references() + (f"<ul>{external_html}</ul>" if external_html else ""))], faqs=faqs,
            domain_url=domain, domain_name=domain_name, terms=terms,
            citation_urls=citations.source_urls() + [url for _, url in external_references],
        ))

    refs = ContentCitations(works)
    c = refs.cite
    page(
        "cognitive-security.html", "What Is Cognitive Security? Theory, Threat Models, and Multi-Agent Defense",
        "A source-linked introduction to cognitive security, narrative analysis, information commons, and bounded agent verification.",
        "og-cognitive-security-pillar.jpg", "Research Synthesis & Foundational Guide",
        "domain-cognitive-security.html", "Cognitive Security",
        ["Cognitive Security", "Active Inference", "Epistemic Security", "Narrative Topography"],
        "<strong>Cognitive security</strong> concerns the integrity of sensemaking and decision-making by people, organizations, and artificial agents. This guide connects research on information environments with proposals for documenting and checking claims. A conceptual framework, a computational demonstration, and a deployed defense provide different kinds of evidence.",
        [
            ("What Is Cognitive Security?",
             f"<p>{c('Friedman2022StructuringInformationCommonsOpen071')} examines open standards and cognitive security in information commons. {c('Friedman2024BridgingGapsImageMeme031')} proposes a multidisciplinary research approach to image memes. These works offer ways to study information environments; they do not establish that every meme is malicious or that a single intervention secures public discourse.</p>"),
            ("How Does Cognitive Security Relate to Information Security?",
             "<p>Information security addresses properties such as confidentiality, integrity, and availability of data and systems. Cognitive security also asks how information is interpreted and used. Accurate transmission alone does not establish that a claim is true, that its context is complete, or that a decision is well supported.</p>"),
            ("Which Publications Address Narratives and Collaborative Analysis?",
             f"<p>{c('Friedman2020ReimaginingMaps148')} considers mapping practices. {c('Friedman2021NarrativeInformationManagement080')} addresses narrative information management. {c('Friedman2020EmergentTeamsComplexThreats085')} and {c('Friedman2021FacilitatorSCatechismPlaybook081')} discuss collaborative work and facilitation. Together these publications address mapping, information management, teamwork, and facilitation.</p>"),
            ("How Can Active Inference Inform Cognitive Security?",
             f"<p>{c('Friedman2021ActiveInferantsActiveInference075')} applies Active Inference to ant colony behavior. It illustrates how generative models can be used to describe adaptive behavior; its ant models do not validate a human influence-defense system. Applying related concepts to cognitive security requires explicit models, threat assumptions, and evaluation in the intended setting.</p>"),
            ("What Do Formal and Computational Frameworks Establish?",
             f"<p>{c('Friedman2026CognitiveIntegrityFrameworkFormal005')} develops a formal framework. {c('Friedman2026WhiteLineTypedLedger202')} and {c('Friedman2026PersonalRedLinesDevelopment203')} address claim boundaries and development constraints. {c('Friedman2026CognitiveDiagramsReviewingCategorical112')} reviews categorical accounts of linguistic case with bounded synthetic illustrations. These sources do not demonstrate immunity to prompt injection or guarantee the correctness of deployed agents.</p>"),
            ("How Can Claims Be Made Easier to Check?",
             f"<p>{c('Friedman2023ATLASQuestionOrientedApproach136')} addresses question-oriented pattern languages in knowledge management. On this site, the <a href='cite-verify.html'>citation guide</a> and <a href='evidence.html'>evidence ledger</a> expose sources and verification boundaries. A source link enables inspection; it does not by itself prove that the adjacent claim follows from the source.</p>"),
        ],
        [
            ("What is cognitive security?", "Cognitive security concerns the integrity of sensemaking and decision-making, including how people and agents assess information and respond to manipulation."),
            ("Does a formal framework guarantee secure agents?", "A formal result applies to its stated model and assumptions. Deployment security requires separate evaluation against concrete threats."),
            ("Where can I find the source publications?", "Use the References section and the <a href='domain-cognitive-security.html'>Cognitive Security domain index</a>. The catalog includes books, reports, preprints, and research papers; inclusion does not imply peer review."),
        ], refs,
    )

    refs = ContentCitations(works)
    c = refs.cite
    page(
        "computational-entomology.html", "Computational Entomology: Algorithms, Models, and Digital Insect Colonies",
        "Research and software connecting insect behavior, physiology, gene expression, and computational models, with publication sources.",
        "og-computational-entomology.jpg", "Domain Deep-Dive & Computational Foundations",
        "domain-entomology.html", "Entomology",
        ["Computational Entomology", "Collective Behavior", "Stigmergy", "Bio-Inspired Computing"],
        "<strong>Computational entomology</strong> uses quantitative analysis, simulation, and bioinformatics to study insects. Models can connect individual behavior with colony dynamics, but their biological interpretation depends on the observations, assumptions, and validation available for each study.",
        [
            ("What Evidence Connects Physiology With Collective Foraging?",
             f"<p>{c('Friedman2019PhysiologyForagerHydrationVariation095')} reports that hydrated harvester ant foragers made more trips than unhydrated nestmates, with hydration and desiccation responses varying among colonies. {c('Friedman2020GeneExpressionVariationBrains086')} reports associations between brain gene expression and collective behavior. An association between expression and colony behavior does not alone establish a causal molecular mechanism.</p>"),
            ("How Can Models Explain Colony Behavior?",
             f"<p>{c('Friedman2023SinglePheromoneModelAccounts046')} shows that a single-pheromone model can account for empirical patterns previously addressed with more complex pheromone models. {c('Friedman2025ComputationalComplexityEnergeticsAnt011')} studies a particular Ant Stack framework. Its computational and energy analysis concerns that biomimetic architecture and its assumptions.</p>"),
            ("Which Software Projects Are Relevant?",
             f"<p>{c('Friedman2026BeeStackEvidenceTypedScaffold125')} presents a scaffold for honeybee simulation with explicit evidence distinctions. {c('Friedman2026EntoLinguisticsLanguageAmbiguity109')} concerns language and scientific communication in entomology. {c('Friedman2026COGANTDeterministicCodebaseGNN169')} describes codebase-to-GNN translation; it is a computational tool rather than an empirical insect model.</p>"
             "<p>Project repositories include <a href='https://github.com/docxology/BeeStack'>BeeStack</a>, <a href='https://github.com/docxology/ento_linguistics'>Ento-Linguistics</a>, <a href='https://github.com/docxology/MetaInformAnt'>MetaInformAnt</a>, and <a href='https://github.com/ActiveInferenceInstitute/Active_InferAnts'>Active_InferAnts</a>. Their implementation and validation scopes differ; consult the project documentation before choosing one.</p>"),
            ("What Does Neurogenomics Add?",
             f"<p>{c('Friedman2018RoleDopamineCollectiveRegulation100')} reports experiments on dopamine and foraging in harvester ants. {c('Friedman2019PhDBehavioralPhysiologicalTranscriptomic093')} brings together behavioral, physiological, and transcriptomic variation among colonies. Combining these measurements can motivate models, but a calibrated prediction from molecular measurements to whole-colony behavior requires its own validation.</p>"),
            ("How Should Biological and Engineering Claims Be Compared?",
             "<p>A simulation that reproduces a behavioral pattern is evidence about that model under its tested conditions. It does not establish that insects implement the same algorithm or that a related robotic system will behave reliably. Compare the model assumptions, measured outputs, negative controls, and available code before transferring a result to another setting.</p>"),
        ],
        [
            ("What is computational entomology?", "Computational entomology applies quantitative analysis, computational models, and bioinformatics to insect biology and behavior."),
            ("Are the listed projects complete biological simulations?", "They have different purposes and evidence boundaries. A software scaffold or synthetic model should not be treated as a validated whole-organism or whole-colony simulation."),
            ("Where can I find publications?", "The <a href='domain-entomology.html'>Entomology domain index</a> includes journal articles and other research outputs. Zenodo is a repository; deposition there does not establish peer review."),
        ], refs,
    )

    refs = ContentCitations(works)
    c = refs.cite
    page(
        "insect-cognition.html", "Insect Cognition & Collective Intelligence: How Ant Colonies Think Without a Brain",
        "A source-linked guide to insect cognition, distributed physiology, and Active Inference models of ant colony behavior.",
        "og-insect-cognition.jpg", "Cognitive Biology & Distributed Intelligence",
        "domain-entomology.html", "Entomology",
        ["Insect Cognition", "Collective Intelligence", "Active Inferants", "Superorganism", "Stigmergy"],
        "<strong>Insect cognition and collective intelligence</strong> concern how individual insects and colonies respond to information and coordinate behavior. Individual ants have brains; the colony has no single central brain. Describing colony behavior as cognition is a modeling perspective whose predictions must be compared with biological evidence.",
        [
            ("How Does Bayesian Modeling Relate to Insect Cognition?",
             f"<p>{c('Friedman2018WoodliceMenBayesianAccount098')} is a published interview in <em>ALIUS Bulletin</em>: Martin Fortier and Daniel Friedman interview Karl Friston about the Free Energy Principle, cognition, life, and consciousness. It provides a conceptual discussion, rather than an experimental comparison of insect and vertebrate brain structures.</p>"),
            ("Can a Colony Be Studied as an Integrated Biological System?",
             f"<p>{c('Friedman2020DistributedPhysiologyMolecularBasis084')} develops the idea of distributed physiology in eusocial insects, connecting molecular processes with social organization. This perspective motivates studying regulation across individuals; it does not formalize colony attention as precision weighting or establish that workers are equivalent to neurons.</p>"),
            ("What Is the Active Inferants Framework?",
             f"<p>{c('Friedman2021ActiveInferantsActiveInference075')} presents an Active Inference framework for ant colony behavior in <em>Frontiers in Behavioral Neuroscience</em>, including a Markov decision process simulation of ant foraging in an alternating T-maze. It considers how generative models and action-perception cycles can be used to model behavior across individual and colony scales. The framework is a theoretical and computational approach, rather than proof that ants literally represent the model variables.</p>"
             f"<p>{c('Friedman2024SharedProtentionsMultiAgent040')} studies shared anticipatory structure in multi-agent Active Inference. It is relevant to coordination theory, but it is not an empirical demonstration that ants exchange posterior beliefs through pheromones.</p>"),
            ("What Do Gene Expression Studies Show?",
             f"<p>{c('Friedman2016ContextDependentExpressionForaging104')} was published in <em>Proceedings of the Royal Society B</em>. {c('Friedman2020GeneExpressionVariationBrains086')} appeared in <em>Communications Biology</em>. The 2016 study examines the interacting roles of age, environment, task, and light exposure in foraging-gene expression. The 2020 RNA-seq study associates among-colony expression differences with humidity response and dopamine-to-serotonin ratios. These associations do not establish that gene expression alone causes colony behavior.</p>"),
            ("What Can Pheromone Models Establish?",
             f"<p>Stigmergy describes indirect coordination through changes to the environment. {c('Friedman2023SinglePheromoneModelAccounts046')} provides a specific model of ant foraging patterns. Reproducing those patterns should not be generalized into a claim that natural pheromone networks solve arbitrary routing or optimization problems exactly.</p>"),
        ],
        [
            ("Do ants have individual brains?", "Yes. Individual ants have nervous systems and brains. Neuron counts differ among species, castes, and measurement methods, so a single count should not be applied to all ants."),
            ("How can colonies coordinate without a central brain?", "Local interactions, environmental conditions, and individual response differences can produce colony-level patterns. The relevant mechanisms depend on the species and behavior studied."),
            ("What is Active Inferants?", "Active Inferants is the 2021 framework by Friedman and colleagues for modeling ant colony behavior using Active Inference. See its full citation and publication source in the References section."),
            ("Where can I learn more?", "Explore the <a href='domain-entomology.html'>Entomology</a> and <a href='domain-active-inference.html'>Active Inference</a> indexes and the primary sources in the references."),
        ], refs,
    )

    refs = ContentCitations(works)
    c = refs.cite
    page(
        "active-inference.html", "Active Inference & The Free Energy Principle: A Practical Tutorial",
        "An introduction to generative models, variational and expected free energy, and Active Inference research tools with primary sources.",
        "og-active-inference-tutorial.jpg", "Foundational Tutorial & Technical Guide",
        "domain-active-inference.html", "Active Inference",
        ["Active Inference", "Free Energy Principle", "Expected Free Energy", "Markov Blanket", "Bayesian Mechanics"],
        "<strong>Active Inference</strong> is a framework for modeling perception, learning, and action with probabilistic generative models. Its applications depend on specific assumptions and implementations. The Free Energy Principle motivates the framework; a model's mathematical consistency does not itself establish its empirical adequacy.",
        [
            ("What Is a Generative Model?",
             "<p>A generative model specifies how hidden states give rise to observations and how states change. In discrete-state formulations, an A matrix commonly encodes observation likelihoods, B matrices encode transitions, C encodes preferences over outcomes, and D encodes initial-state beliefs. These conventions are described in <a href='https://mitpress.mit.edu/9780262045353/active-inference/'>Parr, Pezzulo and Friston's <em>Active Inference</em> (2022, MIT Press)</a>.</p>"),
            ("How Do Variational and Expected Free Energy Differ?",
             "<p>Variational free energy is evaluated for observed data and an approximate posterior. Its complexity-minus-accuracy form provides a bound on negative log model evidence. Minimization finds the best approximation within the chosen family; it need not recover the exact posterior. Expected free energy evaluates possible future outcomes under policies and can include preference satisfaction and information-seeking terms. See the textbook above for definitions and assumptions.</p>"),
            ("How Does Active Inference Compare With Reinforcement Learning?",
             "<p>Both frameworks study action under uncertainty. Reinforcement learning includes model-based and information-seeking methods as well as model-free methods. Active Inference commonly expresses goals as prior preferences and evaluates policies using expected free energy. Neither formulation guarantees sample efficiency, prevents reward hacking, or ensures safe behavior outside its tested setting.</p>"),
            ("What Is a Markov Blanket?",
             "<p>A Markov blanket expresses a conditional independence: internal and external states are conditionally independent given blanket states. A sensory/active partition adds modeling assumptions. This structure alone is not proof of consciousness or agency. For the original research article, see <a href='https://arxiv.org/abs/2206.12996'>Sakthivadivel, <em>A worked example of the Bayesian mechanics of classical objects</em> (2022)</a>.</p>"
             f"<p>{c('Friedman2022WorkedExampleBayesianMechanics143')} catalogs associated discussion transcripts, rather than the original research article. The transcript contributors and the original article's sole author have distinct citation roles.</p>"),
            ("Which Tools and Research Projects Are Available?",
             f"<p>{c('Friedman2026TowardsLean4Formalization113')} describes formalization work whose proofs apply to stated definitions and assumptions. Compilation does not establish the Free Energy Principle as a physical theory. {c('Friedman2023GeneralizedNotationNotationActive056')} concerns model notation; {c('Friedman2025CEREBRUMCaseEnabledReasoning010')} explores case-based representations for modeling.</p>"
             "<p>Repositories include <a href='https://github.com/ActiveInferenceInstitute/fep_formal'>fep_formal</a>, <a href='https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation'>Generalized Notation Notation</a>, <a href='https://github.com/ReactiveBayes/RxInfer.jl'>RxInfer.jl</a>, and <a href='https://github.com/infer-actively/pymdp'>pymdp</a>. RxInfer is a probabilistic programming engine; using it in an Active Inference model requires specifying that model.</p>"),
            ("Where Can I Study Active Inference?",
             "<p>The <a href='https://activeinference.institute/'>Active Inference Institute</a> provides study groups, recordings, and research resources. The textbook line comprises nine completed cohorts for the 2022 Parr, Pezzulo and Friston monograph and a live first cohort for Namjoshi's <a href='https://mitpress.mit.edu/9780262050951/fundamentals-of-active-inference/'>Fundamentals of Active Inference</a> (2026). See the <a href='videos.html'>video archive</a> and <a href='domain-active-inference.html'>domain index</a> for materials and publication types.</p>"),
        ],
        [
            ("What is Active Inference in simple terms?", "It models agents as updating beliefs about their surroundings and selecting actions using a generative model and preferences over outcomes."),
            ("Does minimizing variational free energy recover the true posterior?", "Only if the model, approximation family, and optimization permit it. In general, inference is approximate."),
            ("Does Active Inference guarantee safe AI?", "No. Safety and performance claims require evaluation of the particular model, implementation, environment, and threat assumptions."),
            ("Where are the sources?", "The textbooks, original Bayesian mechanics article, related publications, and discussion materials are listed in the References section."),
        ], refs, external_references=[
            ("Parr, Thomas; Pezzulo, Giovanni; Friston, Karl J. 2022. <em>Active Inference: The Free Energy Principle in Mind, Brain, and Behavior</em>. MIT Press.", "https://mitpress.mit.edu/9780262045353/active-inference/"),
            ("Namjoshi, Sanjeev V. 2026. <em>Fundamentals of Active Inference: Principles, Algorithms, and Applications of the Free Energy Principle for Engineers</em>. MIT Press.", "https://mitpress.mit.edu/9780262050951/fundamentals-of-active-inference/"),
            ("Sakthivadivel, Dalton A. R. 2022. <em>A Worked Example of the Bayesian Mechanics of Classical Objects</em>. arXiv:2206.12996.", "https://arxiv.org/abs/2206.12996"),
        ],
    )

    refs = ContentCitations(works)
    c = refs.cite
    page(
        "neurosymbolic-ai.html", "Neurosymbolic AI & Active Inference: Bridging Symbolic Reasoning and Generative Agents",
        "A guide to neural and symbolic representations, Active Inference projects, and the limits of formal and computational evidence.",
        "og-neurosymbolic-ai.jpg", "Advanced AI Architectures & Epistemic Synthesis",
        "domain-computational.html", "Computational",
        ["Neurosymbolic AI", "Active Inference", "Knowledge Graphs", "Symbolic Reasoning", "AGEINT"],
        "<strong>Neurosymbolic AI</strong> combines learned statistical representations with explicit symbolic structures or reasoning. Such combinations can make some constraints inspectable, but do not automatically eliminate hallucinations, produce correct causal models, or establish secure behavior.",
        [
            ("How Can Neural and Symbolic Representations Be Combined?",
             "<p>Neural components can propose classifications or candidate statements; symbolic components can check specified relations, types, or rules. A check establishes only the property it actually tests. Incorrect source data, incomplete rules, and invalid mappings between natural language and formal representations can still produce false conclusions.</p>"),
            ("How Does Active Inference Relate to These Approaches?",
             f"<p>{c('Friedman2026CognitiveDiagramsReviewingCategorical112')} reviews categorical treatments of linguistic case and presents bounded synthetic examples. {c('Friedman2026TowardsLean4Formalization113')} concerns formalization under explicit assumptions. Neither work establishes that attaching diagrams or Lean proofs to a language model constrains all of its behavior. A discrete probabilistic state space is not automatically a symbolic logic or a causal model.</p>"),
            ("What Is AGEINT?",
             f"<p>{c('Friedman2026AGEINTAgenticIntelligence170')} is a curriculum and reference work on agentic intelligence. It organizes guidance and assurance practices for bounded AI assistance, with synthetic fixtures and explicit review boundaries. {c('Friedman2026WhiteLineTypedLedger202')} addresses typed claim boundaries; a ledger records evidence distinctions rather than guaranteeing that its contents are true.</p>"),
            ("Which Projects Illustrate Related Research Directions?",
             f"<p>{c('Friedman2025DiscoveryEngineAIDriven026')} proposes a framework for scientific knowledge discovery and synthesis. {c('Friedman2025CEREBRUMCaseEnabledReasoning010')} develops case-enabled modeling. {c('Friedman2026COGANTDeterministicCodebaseGNN169')} describes deterministic codebase-to-GNN translation. These are distinct projects with their own evaluation scopes, rather than interchangeable demonstrations of hallucination-free AI.</p>"
             f"<p>{c('Friedman2026BoundedAutoResearchTinyReproducible120')} studies a bounded machine-learning research task. Its reported deterministic MNIST experiment uses zero LLM calls and retains human review gates.</p>"),
            ("How Should Future Capabilities Be Evaluated?",
             "<p>Claims about proof-carrying agent communication, causal discovery, or autonomous research need explicit task definitions, failure cases, and measurements in the relevant environment. They are research directions, not capabilities established merely by combining a language model, a knowledge graph, and an Active Inference model.</p>"),
        ],
        [
            ("What is neurosymbolic AI?", "It combines learned statistical representations with explicit symbolic representations or reasoning methods."),
            ("Does symbolic verification eliminate hallucinations?", "No. It can reject outputs that violate checked constraints, but its scope depends on the rules, source evidence, and translation into the formal representation."),
            ("Are all Active Inference systems neurosymbolic?", "No. The relationship depends on the implementation; probabilistic inference alone does not establish a neural-symbolic architecture."),
            ("Where can I read the research?", "See the references and the <a href='domain-computational.html'>Computational</a> and <a href='domain-active-inference.html'>Active Inference</a> indexes. Publication and validation types differ across projects."),
        ], refs,
    )
    return pages
