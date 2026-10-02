<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🐜 Illegal States, Mostly Unrepresentable

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21298885-blue)](https://doi.org/10.5281/zenodo.21298885)

---

## Abstract

> This paper presents a strongly-typed, decentralized multiagent simulation — an ant-robot colony — as the computational exemplar of the Research Project Template (https://github.com/docxology/template). Each colony member is an Agent that owns exactly one real, on-disk SQLite database and one in-process, fault-injectable protocol endpoint; no agent ever touches another agent's storage or network state. The implementation lives under projects/templates/template_formal/src/template_formal/; the demo pipeline is orchestrated by scripts/02_run_analysis.py. The paper's central claim is methodological, not a typing-features showcase: static typing's honest value in Python is edit-time/CI-time error prevention on structurally representable invariants, and nothing more. Nominal identifiers (AgentId, MessageId, TxnId as distinct NewType wrappers), a tagged-union Result[T, E] ADT with match-exhaustiveness, and a session-typed protocol state machine (IdleSession → HandshakingSession → EstablishedSession → ClosedSession) each make an illegal program a type error, verified by a real mypy --strict subprocess run against six known-bad negative-control fixtures plus three known-good positive-control fixtures (tests/mypy_fixtures/). Where the type system cannot help — reusing a consumed transaction handle, reusing a consumed protocol-phase instance, or receiving malformed bytes off an untyped network boundary — the implementation runtime-guards instead, and the manuscript says so explicitly rather than eliding the distinction. We also frame, without over-claiming, two additional lenses: the per-agent storage schema as a functor $\mathrm{Schema} \to \mathbf{Set}$ in the sense of @fong2018seven, and each agent's per-tick decision as an approximate minimizer of a closed-form expected-free-energy quantity in the spirit of @friston2005theory, bridged to collective organization via the Memory Evolutive Systems framework of . Both framings are declared as design lenses, not machine-checked mathematical results — the paper is explicit about which of its claims are proofs and which are analogies. Contributions are architectural, epistemic, and empirical. Architecturally: a zero-mock test suite (tests/) covering ADT exhaustiveness, affine-handle reuse, session-type phase transitions, seeded fault injection over a real in-process bus, and a three-agent colony integration test exhibiting a real stigmergic positive-feedback mechanism (deliberately not overclaimed as "emergence" — see @sec:results-discussion). Epistemically: an explicit "What mypy --strict proves vs. what is a runtime discipline" section (@sec:honesty-line) that pins every strong claim to the ISC (Ideal-State Criterion) number of its paired negative-control test, so the claim-to-evidence mapping is auditable rather than asserted. Empirically: eight pre-registered analyses grouped across three experiment families, falsifiable experiments (@sec:results-discussion) — a decay-rate sweep revealing a real, non-monotonic threshold effect (near-zero convergence below decay $\approx 0.35$, a $100\%$ plateau at moderate decay, and a measurable decline at total evaporation); a random-choice null-model comparison showing the real mechanism's Wilson-bounded convergence rate ($93.3\%$) does not overlap a chance baseline's ($0.67\%$); and a heterogeneity-magnitude sweep showing convergence rate decreases strictly monotonically as agent preferences spread wider — each stated with its falsification criterion before its real, seeded result, using genuinely new stdlib-only infrastructure (colony/nullmodel.py, colony/sweep.py) rather than one-off scripts. Keywords: strongly typed programming, session types, algebraic data types, category theory, Active Inference, multiagent systems, affine types, illegal state unrepresentable.

## Keywords

`strongly typed programming` · `session types` · `algebraic data types` · `category theory` · `active inference` · `multiagent systems` · `affine types` · `illegal state unrepresentable`

## Methods

- **Simulated ant-robot colony: agents with own SQLite DB and protocol endpoint** — Each simulated colony member owns one on-disk SQLite database and one fault-injectable protocol endpoint, with no shared storage or network state.
- **mypy --strict as oracle on six known-bad and three known-good fixtures** — Runs mypy --strict as a subprocess on negative-control fixtures (expect errors), positive-control fixtures, and the src tree (expect zero exit).
- **Seeded fault injection (drop/reorder/duplicate/corrupt) over an in-process bus** — Drives real handshakes through an in-process bus with each fault mode enabled, checking typed error results and seed determinism.
- **Pre-registered seeded experiments with Wilson CIs, Fisher and Cochran–Armitage tests** — Tests colony convergence over independently seeded trials at a calibrated baseline (8 agents, 2 locations, 30 ticks) using Wilson intervals, Fisher and trend tests.
- **Design lenses: schema as functor; decision as expected-free-energy minimizer** — Frames per-agent storage as a functor Schema→Set and decisions via expected free energy, explicitly as design lenses rather than proofs.

## Key Findings

- In the tested calibrated configuration, the stigmergic mechanism beat a random-choice null model: its Wilson lower bound (0.8816) clears the null model's upper bound (0.0368).
- Disabling only pheromone deposit collapsed convergence to chance level, attributing the mechanism's advantage to the stigmergic channel in this configuration.
- Convergence versus decay showed a threshold rather than a monotonic slope, with 0/60 trials converging at decay 0.10 and 0.30.
- Convergence decreased strictly as preference heterogeneity widened (1.0000 > 0.9333 > 0.2500 > 0.0333).
- An audit found a defect the src-only mypy gate missed (a Protocol a frozen dataclass could not satisfy), fixed with read-only properties and a good-fixture regression guard.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21298885](https://doi.org/10.5281/zenodo.21298885)
- Zenodo record: [https://zenodo.org/records/21298885](https://zenodo.org/records/21298885)
- PDF: [Friedman_2026_Illegal_5bda439c.pdf](Friedman_2026_Illegal_5bda439c.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21298885)

## Citation

> Daniel Ari Friedman (2026). *Illegal States, Mostly Unrepresentable*. Zenodo. DOI: 10.5281/zenodo.21298885. URL: https://doi.org/10.5281/zenodo.21298885.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
