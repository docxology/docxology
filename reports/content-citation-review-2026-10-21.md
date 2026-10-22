# Content citation and link review — 2026-10-21

The clean checkout, local main, origin/main, and live GitHub main matched `34273cf538796804f8c04c0af6f29b122e004a3e` before corrections. Corrections were developed on `codex/content-citation-audit-20261021`; this review does not assert deployment.

The audit covers public content guides, collaborator HTML/Markdown, catalog citations, generated work and paper pages, and link targets across the tracked Pages HTML projection. Local structure checks and source interpretation are separate evidence.

## Source review

All 208 DOI-bearing catalog entries were checked against first-party Crossref or DataCite metadata. Contributor order and identity were reviewed using established name conventions rather than inferring authors from permanent citation keys. One containing Science feature publishes no contributor list in its DOI metadata. The 15 DOI-free records received explicit source dispositions below.

The retained registry observation files preserve source URLs, timestamps, response SHA-256 values, source titles, contributor arrays, and years. Raw registry response bytes are retained under GitVault Local task storage, outside the public repository. An initial capture found a missing author-registry entry for work 227; a separate direct DataCite retrieval confirmed its existing author and supplied that missing registry entry. Initial observations and the subsequent correction are kept distinct.

### Content corrections

- **Woodlice interview:** the publisher identifies Friston, Fortier, and Friedman (2018), with Fortier and Friedman interviewing Friston. Removed the incorrect Friedman–Ramstead attribution and unsupported anatomical claims. [Publisher PDF](https://aliusresearch.org/library/pdfs/alius-bulletin/issue-02/alius-bulletin-issue-02-friston-of-woodlice-and-men-a-bayesian-account-of-cognition-life-and.pdf), page 17.
- **Foraging gene:** Ingram and colleagues (2016), *Proceedings of the Royal Society B*, not *Communications Biology*. [Publisher record](https://doi.org/10.1098/rspb.2016.0841).
- **Pheromone model:** Saund and Friedman (2023), with the complete title and bounded model-comparison interpretation. [Publisher record](https://doi.org/10.1016/j.cogsys.2023.02.005).
- **Distributed physiology:** Friedman, Johnson, and Linksvayer (2020); described as a review of distributed physiological regulation. [Publisher record](https://doi.org/10.1016/j.yhbeh.2020.104757).
- **Bayesian mechanics:** distinguished the four-contributor [discussion transcript](https://doi.org/10.5281/zenodo.7400785) from [Sakthivadivel's original article](https://arxiv.org/abs/2206.12996).
- **Edited volumes:** rows 71, 79, and 89 identify editors explicitly in bylines, references, domain RSS descriptions, paper README/AGENTS/SKILL citations, structured metadata, BibTeX, CSL, and RIS. Archived primary documents contain the edited-by evidence. The three legacy book CFF files were retired: [CFF 1.2's schema](https://github.com/citation-file-format/citation-file-format/blob/396f738fb025b1d8acdb02a56ffc923f95dc8999/schema.json) cannot represent a standalone editor-only book without inventing authors. Their role-aware BibTeX, CSL, and RIS records remain available. This is a contributor-role correction, not a certification of schema conformance for all other legacy CFF files.
- **Framework scope:** replaced claims of immunity to prompt injection, elimination of hallucinations/reward hacking, autonomous proof repair, universal efficiency superiority, and biological polynomial-time proofs with descriptions bounded to the cited models and experiments.
- **Teaching references:** linked the 2022 Parr–Pezzulo–Friston textbook and [Namjoshi's 2026 textbook](https://mitpress.mit.edu/9780262050951/fundamentals-of-active-inference/); aligned cohort wording with the maintained teaching source.
- **Collaborators:** corrected Mridula Mascarenhas's first name; removed false joint authorship linking Johnson to the forager-expression/neurotransmitter papers, Linksvayer to the Blattodea paper, Pitliya to *Thoughtseeds*, and Cordes to the sole-authored CIF paper. Distinguished Gordon's adviser role on the dissertation and clarified interview credits.
- **Publisher/venue:** represented Cognitive Diagrams, FEP Lean, and A Living Meta-Analysis Architecture as Zenodo deposits. Publisher fields, author affiliation, or repository deposition alone do not establish journal publication or peer review. Corrected the Springer series abbreviation to Communications in Computer and Information Science (CCIS); omitted the volume number because the retained Crossref record does not establish it. [Springer chapter](https://doi.org/10.1007/978-3-032-16955-6_11).
- **Edition identities:** the Digital Twins concept/version rows 33 and 162 represent the same submission; retained both stable URLs and consolidated the canonical destination. Totals describe catalog records, including editions, rather than distinct publications. Updated row 219 to the current concept record's daf-jev title, consistent with its current metadata; its old title belongs to version DOI 22816188.

### Catalog title reconciliation

The retained responses also received a venue review: after corrections, 157 Zenodo labels, three arXiv labels, 35 Crossref records, and 13 other labels. The Crossref records comprise 31 journal articles, two posted-content records, and two proceedings chapters. Nontrivial conference, agency, and ALIUS labels were checked against source descriptions, relations, or primary-document citation lines. This review distinguishes repository labels from evidence of journal publication.

42 catalog titles were completed or reconciled with their primary records, including three presentation-only punctuation/notation differences. Stable citation keys and URLs were preserved.

| Row | Corrected title | Primary source |
| --- | --- | --- |
| 8 | Abstract book for: 5th Applied Active Inference Symposium | [Source](https://doi.org/10.5281/zenodo.17555266) |
| 9 | Adaptive Basic Income (AuBI): Integrating AI, Decentralized Infrastructure, and Active Inference for Next-Generation Economic Systems | [Source](https://doi.org/10.5281/zenodo.17228945) |
| 13 | Increasing the Accessibility and Applicability of Active Inference: Generative Playbooks and Open-Source Summer School Curriculum Development | [Source](https://doi.org/10.5281/zenodo.15061666) |
| 15 | Markdown Decision Process: A Framework for Probabilistic Document Analysis and Optimization | [Source](https://doi.org/10.5281/zenodo.17244386) |
| 20 | Symergetics: Symbolic Synergetics for Rational Arithmetic, Geometric Pattern Discovery, and All-Integer Accounting | [Source](https://doi.org/10.5281/zenodo.17114389) |
| 23 | Temporal depth in a coherent self and in depersonalization: theoretical model | [Source](https://doi.org/10.3389/fpsyg.2025.1585315) |
| 24 | The Active Inference Institute & Active Inference Ecosystem | [Source](https://doi.org/10.5281/zenodo.17982447) |
| 31 | Bridging gaps in image meme research: A multidisciplinary paradigm for scaling up qualitative analyses | [Source](https://doi.org/10.1002/asi.24900) |
| 33 | Comments Submitted by BlockScience, University of Washington APL Information Risk and Synthetic Intelligence Research Initiative (IRSIRI), Cognitive Security and Education Forum (COGSEC), and the Active Inference Institute (AII) to the Networking and Information Technology Research and Development National Coordination Office's Request for Comment on The Creation of a National Digital Twins R&D Strategic Plan NITRD-2024-13379 | [Source](https://doi.org/10.5281/zenodo.13273681) |
| 38 | MathArt Stream #8 ~ William Blake and Active Inference | [Source](https://doi.org/10.5281/zenodo.13711301) |
| 39 | Transcript of: "Sensemaking Federation: Exploring the Frontiers of Digital Innovation" | [Source](https://doi.org/10.5281/zenodo.14574046) |
| 41 | The Active Inference Institute & Active Inference Ecosystem | [Source](https://doi.org/10.5281/zenodo.14108992) |
| 42 | Way Finding in the Infinite Imaginarium: Juxtaposing Epistemic Tempos and Modes | [Source](https://doi.org/10.5281/zenodo.10601081) |
| 43 | Why Paleolithic Rockstars were both enigmatic and sporadic: A comment on: ‘Snakes and Ladders’ in paleoanthropology: From cognitive surprise to skillfulness a million years ago | [Source](https://doi.org/10.1016/j.plrev.2024.04.010) |
| 45 | A guided tour through the spaces of particular “minds”: A Comment on “Path integrals, particular kinds, and strange things” | [Source](https://doi.org/10.1016/j.plrev.2023.11.001) |
| 46 | A single-pheromone model accounts for empirical patterns of ant colony foraging previously modeled using two pheromones | [Source](https://doi.org/10.1016/j.cogsys.2023.02.005) |
| 47 | A snapshot and pipeline for tissue-specific gene expression meta-analysis in honey bees (Apis mellifera) | [Source](https://doi.org/10.5281/zenodo.10400744) |
| 52 | Comments on AI Accountability Policy Submitted to NTIA Docket 2023-0005-0001 by IRSIRI, AII, PFH, and COGSEC | [Source](https://doi.org/10.5281/zenodo.8025956) |
| 53 | Distributed Science - The Scientific Process as Multi-Scale Active Inference | [Source](https://doi.org/10.31219/osf.io/dnw5k) |
| 59 | Open Access science needs Open Science Sensemaking (OSSm): open infrastructure for sharing scientific sensemaking data | [Source](https://doi.org/10.31222/osf.io/9nb3u) |
| 60 | Postdoc review (2020-2023) ~ September 25, 2023 | [Source](https://doi.org/10.5281/zenodo.8377987) |
| 61 | The Active Inference Institute and Active Inference Ecosystem | [Source](https://doi.org/10.5281/zenodo.8266280) |
| 62 | The Properties, Processes, and Perspectives Inter-Framework (P3IF): Multiplexing interdisciplinary requirements frameworks to manage information risk and foster cognitive security | [Source](https://doi.org/10.5281/zenodo.10034511) |
| 64 | Transcript of Chris Fields, "Physics as Information Processing" course in 2023 | [Source](https://doi.org/10.5281/zenodo.10447642) |
| 65 | William Blake & Buckminster Fuller: Lives in Juxtaposition (A study in Comprehensivity) | [Source](https://doi.org/10.5281/zenodo.7514367) |
| 66 | An Active Inference Ontology for Decentralized Science: from Situated Sensemaking to the Epistemic Commons | [Source](https://doi.org/10.5281/zenodo.6320574) |
| 67 | Catechism for: "Towards Active Diffusion: A Tale of Multiple (den)Cities" | [Source](https://doi.org/10.5281/zenodo.7443847) |
| 69 | On free will or the lack thereof | [Source](https://doi.org/10.5281/zenodo.7394900) |
| 70 | Predictive Processing Interpretation of the Mirror Test and Implications of a Reflection Prediction for Human Cognition | [Source](https://doi.org/10.5281/zenodo.7377255) |
| 88 | Measurement of natural variation of neurotransmitter tissue content in red harvester ant brains among different colonies | [Source](https://doi.org/10.1007/s00216-019-02355-3) |
| 91 | The Neuroscience of Decision Making. An interview of Timothy Hanks by Alexandra Mikhailova and Daniel A. Friedman. | [Source](https://doi.org/10.34700/8pg4-0h12) |
| 92 | Dennett Explained. An interview with Daniel Dennett. | [Source](https://doi.org/10.34700/7gkw-zh08) |
| 93 | Behavioral, physiological, and transcriptomic variation among colonies of the red harvester ant (Pogonomyrmex barbatus) | [Source](https://purl.stanford.edu/pb813wm1484) |
| 98 | Of woodlice and men: A Bayesian account of cognition, life and consciousness. An interview with Karl Friston. | [Source](https://doi.org/10.34700/h460-nz89) |
| 99 | Partner Pen Play in Parallel (PPPiP): A New PPPiParadigm for Relationship Improvement | [Source](https://doi.org/10.3390/arts7030039) |
| 104 | Context-dependent expression of the foraging gene in field colonies of ants: the interacting roles of age, environment and task | [Source](https://doi.org/10.1098/rspb.2016.0841) |
| 119 | Policy Entanglement in Active Inference: A Coupling-Parameter Deformation Framework for Multi-Stream Policy Posterior Distributions, Machine-Checked and Simulated with a Typed Float Boundary | [Source](https://doi.org/10.5281/zenodo.20418904) |
| 162 | Comments Submitted by BlockScience, University of Washington APL Information Risk and Synthetic Intelligence Research Initiative (IRSIRI), Cognitive Security and Education Forum (COGSEC), and the Active Inference Institute (AII) to the Networking and Information Technology Research and Development National Coordination Office's Request for Comment on The Creation of a National Digital Twins R&D Strategic Plan NITRD-2024-13379 | [Source](https://doi.org/10.5281/zenodo.13273682) |
| 165 | iTrace: verification-first webcam eye-movement analysis (corrected manuscript) | [Source](https://doi.org/10.5281/zenodo.20614908) |
| 168 | Generalized_Notation_Notation (GNN) | [Source](https://doi.org/10.5281/zenodo.7803313) |
| 180 | Sortition Upstream of NTQR: How Panel Formation and Size Shape Ground-Truth-Free Evaluation | [Source](https://doi.org/10.5281/zenodo.21083779) |
| 219 | daf-jev: Modular Decision Models, Orchestration, and Reproducible Evaluation | [Source](https://doi.org/10.5281/zenodo.22816187) |

## DOI-free source dispositions

| Rows | Disposition |
| --- | --- |
| 2, 6 | Series/channel identities resolve; no individual author list is asserted. Embedded historical counts are not newly attested by this review. |
| 28 | Chapter attribution follows its archived primary title/byline; book-level contributors are not substituted for chapter authors. |
| 44 | Friedman and Ripley's Curio Cards contribution is documented in the archived source; its current external book-link availability remains unconfirmed. |
| 71, 79, 89 | Edited-by lines in the archived source establish editor roles. |
| 78 | Kang, Cordes, Friedman verified from the [official playbook](https://www.innovatorsdigitalplaybook.com/), with HTTP response hash and captured author evidence. |
| 93 | Friedman, sole author, Stanford PhD dissertation (2019). [Stanford record](https://purl.stanford.edu/pb813wm1484). |
| 155 | Friedman byline and contribution title verified in the [publisher digital issue](https://www.sciencemagazinedigital.org/sciencemagazine/20_may_2016?pg=24); replaced the nonresolving DOI-shaped link. The containing feature has a separate identity. |
| 83, 87 | Course-specific instructor metadata remains unverified: anonymous Udemy responses expose a generic shell. |
| 157 | The linked containing Science feature is identified, but its full contributor list cannot establish the subsection-specific byline for *Disinforge*. Attribution remains unverified. |
| 163, 164 | Exact-title primary records, bylines, and scans are unavailable. Entries are retained with explicit incomplete-record notices. |

## Link observations and corrections

The initial local scan checked 2,621 HTML pages, 102,723 local links, 7,813 fragments, and 6,890 work links. Three links targeted `papers/`, which lacks an index document. Their authoritative sources now point to `papers/README.md`.

A separate live scan checked 3,022 distinct external main-content links. It recorded 2,847 successful responses and 175 warnings: 165 blocked/rate-limited, four timeouts, three connection failures, and three HTTP 404 responses. This is a dated network observation with its original source hashes, not a claim that all external content is available or that a successful response proves a citation's meaning.

Verified same-entity/event replacements were applied for the Johnson Lab, Los Tuxtlas station, and the Stanford 2016 Art of Neuroscience event. The GSA recipient list supports the Victoria Finnerty Undergraduate Travel Award in **2014**, correcting the former title/year. [GSA recipient list](https://genetics-gsa.org/awards/victoria-finnerty-undergraduate-travel-awards/).

No exact successor was found for the Stanford Systems Biology seed-grant source, the UC Davis Genetics Department Citation source, or the Probe article. Their unresolved availability is recorded; unrelated homepages were not substituted. Christie’s and Me Judice returned the matching content through web retrieval despite command-line probe failures. Canonical DOI links were retained when publisher access was blocked; DOI identity was checked through registration APIs.

## Repeatable checks and limits

`uv run python3 code/orchestrators/audit_content_citations.py` checks local targets against the Pages publication projection, HTML fragments, work identities, catalog-derived inline citations and full references, and explicit collaborator joint-publication claims. It is also called by `validate_repo.py`. `--report PATH` saves the source-bound inventory; `--network-report PATH` deliberately performs live probes.

Negative controls cover invented authors, altered years/titles/targets, single-quoted annotation markup, missing fragments, existing files omitted from Pages, unsupported editor evidence, false joint authorship, and author receipts with changed identity/source fields. These controls exercise the properties the local gate claims to check. They do not automate semantic proof of every prose assertion.

The five topic guides now derive citation labels and full references from the reviewed catalog, fail when contributors are missing, include primary-source links, and expose citation URLs in Article structured data. Regeneration owns all downstream projections.

Local tests, repository validation, rendered browser observations, and independent code review are reported separately in the task's final disposition. This report records source review, not deployment attestation or external-service correction.
