<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🛡️ CogSecSkills: Multiharness Agentic Skills for Cognitive Security

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21513316-blue)](https://doi.org/10.5281/zenodo.21513316)

---

## Abstract

> CogSecSkills is a defensive, harness-neutral agent-interface library that turns the human doctrine of cognitive security and analytic tradecraft into dependable, inspectable, agent-usable skills, distributed as an open repository from github.com/docxology/CogSecSkills; the motivation is an information environment in which mis-, dis-, and malinformation are analytically distinct but operationally entangled, false content can diffuse rapidly at platform scale, and credible source evaluation increasingly demands explicit expert practice rather than page-bound reading alone, so that agents asked to weigh competing hypotheses, trace provenance, or critically review a claim need a repeatable procedure and a stable tool-use contract rather than improvisation. The live generated catalogue reports one hundred implemented skills across seven taxonomy groups — Structured Analytic Techniques, Cognitive Security, Critical Review and Assurance, OSINT and Source Integrity, Counterintelligence and Deception Detection, Information Environment and Influence Analysis, and Research and Synthesis Methods — and the library is organized as a Plan, Build, and Teach system in which a registry declares the catalogue, a definitions layer owns the substance and quality controls of each skill, a skills tree exposes the harness-facing build, and a vendored educational upstream named AGEINT explains why each technique exists and how to use it responsibly. The central design choice is to make the reusable skill contract smaller than any one agent interface yet stricter than a prompt collection: each skill is owned by a single canonical definition that declares triggers, inputs, outputs, per-skill reference metadata, group-aware quality controls, and a closed vocabulary of neutral tool verbs before any harness-specific adapter is considered, and that definition is rendered deterministically into a harness-neutral specification, a human-readable skill description, an executable workflow, and one adapter per configured harness whose default members are Claude, Codex, and Hermes, so that portability becomes a property the test suite proves rather than a hope, and installation is concrete rather than interpretive — clone the public repository, install or run the Python package, run validation, point the agent harness at a chosen skill, execute its workflow, and bind runtime tools through the named harness adapter, regenerating adapters from a configuration file for any non-default harness. The quality discipline is the core of the contribution: an automated audit checks that every skill's defensive boundaries, misuse redirects, evidence requirements, confidence rubrics, privacy and legal constraints, uncertainty handling, failure modes, and negative controls are not merely present but specific to that skill and not reused across the corpus, while an evidence ladder adds curated safe-use and unsafe-redirect scenarios with expected defensive response-shape contracts, reviewed expected answers, and one source-owned worked example per skill, and a generated quality dashboard, supplemental catalogue, metadata matrix, data exports, and a family of deterministic figures — taxonomy counts, the hundred-skill atlas, tool-verb coverage, AGEINT topic crosswalks, the Plan-Build-Teach flow, reference density, harness coverage, and a cover-page installation route — are all produced directly from the live registry and skill specifications so that every visual stays synchronized with the source tree. The evidence boundary is deliberately and explicitly repository-local and reproducible within the checked-out project state, following reproducible-computing, open-data stewardship, and software-citation norms for explicit workflows, version specificity, and citable artifacts; every claim is backed by source files, canonical definitions, generated supplements and figures, the generated dashboard, and project-local verification commands together with a focused test suite and a manuscript renderer, and the work positions CogSecSkills as a validated interface between reasoning, tool use, and defensive output discipline rather than as a claim that any particular model runtime behaves correctly in the field, so its figures, supplements, scenarios, worked examples, and dashboard should be read as synchronized views of the current library state and never as independent measurements of operational performance.

## Keywords

`cognitive security` · `agent skills` · `analytic tradecraft` · `structured analytic techniques` · `multiharness`

## Methods

- **Plan/Build/Teach architecture: registry, definitions, skills tree, AGEINT** — Separates a catalogue registry, canonical per-skill definitions, a harness-facing skills tree, and the AGEINT educational upstream.
- **Harness-neutral skill contract over a closed set of eight tool verbs** — Each skill may use only neutral verbs (read, search, write, exec, reason, web, delegate, ask), bound per harness through adapters.
- **Deterministic rendering into Claude, Codex, and Hermes adapters** — Renders each canonical definition into a spec, skill description, workflow, and one adapter per configured harness.
- **Automated anti-boilerplate per-skill quality audit** — Requires a skill-specific quality bundle and rejects generic or reused negative controls, rubrics, evidence and privacy entries.
- **Evidence ladder: 28 scenario fixtures and per-skill worked examples** — Checks curated safe and unsafe scenarios against the local router and verifies one reviewed worked example per skill.

## Key Findings

- The generated catalogue reports one hundred implemented skills across seven taxonomy groups, from Structured Analytic Techniques to Research and Synthesis Methods.
- The author describes a local quality gate, explicitly 'not a safety proof', that can show all 100 skills include group-aware defensive boundaries and skill-specific governance entries in the current repository state.
- The worked-example gate verifies exact 100-skill coverage; the examples are expected-answer shapes, not live model transcripts.
- The author states the evidence is local conformance only and does not establish operational effectiveness, adversary coverage, user outcomes, or superiority over other libraries.
- The deterministic gates do not show that a live runtime will select the same skill, use tools correctly, or answer well in the field.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/CogSecSkills](https://github.com/docxology/CogSecSkills)
- GitHub release: [v1.0.0](https://github.com/docxology/CogSecSkills/releases/tag/v1.0.0)
- DOI: [10.5281/zenodo.21513316](https://doi.org/10.5281/zenodo.21513316)
- Zenodo record: [https://zenodo.org/records/21513316](https://zenodo.org/records/21513316)
- PDF: [Friedman_2026_Cogsecskills_1a99a2e4.pdf](Friedman_2026_Cogsecskills_1a99a2e4.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21513316)

## Citation

> Daniel Ari Friedman (2026). *CogSecSkills: Multiharness Agentic Skills for Cognitive Security*. Zenodo. DOI: 10.5281/zenodo.21513316. URL: https://doi.org/10.5281/zenodo.21513316.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
