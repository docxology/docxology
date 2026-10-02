<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Sortition Upstream of NTQR

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21083779-blue)](https://doi.org/10.5281/zenodo.21083779)

---

## Abstract

> How should you choose the judges, jurors, or reviewers who form a panel — and does that upstream choice change how well you can evaluate them without an answer key? A panel can be selected many ways — by competence, by a representative lottery (sortition), by ideological bloc, or at random — and, separately, its noisy judgments can be evaluated blind: given the agreement/disagreement pattern among three binary judges, the ntqr package's error-independent (EIE) evaluator returns logically consistent estimates of item prevalence and per-judge accuracy with no labels at all. But that evaluator takes the panel as given. We join the two questions and ask whether the rule that forms the panel changes the oracle-referenced error of the no-answer-key evaluation — how far the blind estimate lands from the answer-key result, lower being better. On a fully deterministic instrument (96 seeds, 96 experts, 300 items), the dominant lever is which rule forms the panel, not its size: competence-first selection recovers best (0.037), while representative, single-bloc, and random selection collapse together — by construction, because with independent judge errors composition cannot move an estimator that only sees agreement. Supplying the missing channel — same-group judges sharing a latent, marginal-accuracy-preserving error confound — makes the strategies fan out monotonically as within-bloc coupling rises: representative sortition stays flat while single-bloc selection degrades, the gap widening from 0.000 to 0.112. Within this instrument the relationship is closed-form: recovery error tracks the panel's Herfindahl concentration index over the axis a shared error rides on — minimized exactly by a balanced (representative) draw, maximized by a single bloc — and a continuous representativeness dial confirms error rises monotonically with it. The protection is conditional: re-keying the confound to an axis the lottery does not balance erases the protection (0.147→0.229). The lesson for selecting and evaluating panels is thus a falsifiable, simulation-bounded prediction, not a preference for any one rule — representativeness protects blind recovery precisely when the panel balances the attribute a shared error rides on. Evidence is synthetic and oracle-scored; in a single small live model (gemma3:4b) the synthetically-best competence-first rule was the worst, illustrating that a selection rule validated on parameterized judges need not carry over to prompted ones — a hypothesis to test, not an established caution. All methods and documentation are openly available at the public repository docxology/ntqr_allotment.

## Keywords

`sortition` · `NTQR` · `unlabeled evaluation` · `expert panels` · `peer review` · `error independence` · `statistical power` · `panel formation` · `synthetic evaluation` · `LLM reviewers`

## Methods

- **Seeded synthetic panel instrument scored against a known oracle** — Generates synthetic expert populations and corpora, forms panels, runs the ntqr evaluator without labels, and scores its estimate against the supervised oracle.
- **Four panel-formation strategies compared** — Compares representative sortition, uniform random selection, single-bloc ideological selection, and competence-first expertise thresholding.
- **ntqr error-independent (EIE) evaluator over judge trios** — Uses the ntqr package's exact three-judge EIE solver for no-answer-key evaluation, treating larger panels as ensembles of trios; recovery error is an L1-style distance to the oracle.
- **Gaussian-copula composition-coupled error confound** — Injects shared latent shocks among same-group judges via a Gaussian copula on probit-thresholded competence, preserving marginal accuracy while tuning cross-judge error correlation.
- **Live gemma3:4b reviewer-panel companion and five pre-stated hypotheses** — Tests transfer (H5) with one local Ollama gemma3:4b model prompted as postdoctoral reviewers on fictitious applications; H1-H4 tested on the synthetic track.

## Key Findings

- Formation rule, not panel size, was the dominant lever: competence-first selection had the lowest recovery error (0.037), while the other three strategies clustered around 0.147-0.148.
- With a composition-coupled error confound, single-bloc error exceeded representative error in 180/205 matched regimes, the gap widening from 0.000 to 0.112 as coupling rose.
- Recovery error tracks the panel's Herfindahl concentration over the axis the shared error rides on; re-keying the confound to an unbalanced axis erased the protection (0.147 to 0.229).
- Increasing panel size from three to six seats produced at most tiny increases in error (largest +0.015), so size was essentially neutral.
- H5 was rejected: with the live gemma3:4b panel, the synthetically best expertise-threshold rule was the worst (0.347), which the author frames as a hypothesis to test beyond one model.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/ntqr_allotment](https://github.com/docxology/ntqr_allotment)
- GitHub release: [v0.1.0](https://github.com/docxology/ntqr_allotment/releases/tag/v0.1.0)
- DOI: [10.5281/zenodo.21083779](https://doi.org/10.5281/zenodo.21083779)
- Zenodo record: [https://zenodo.org/records/21083779](https://zenodo.org/records/21083779)
- PDF: [Friedman_2026_Sortition_73289489.pdf](Friedman_2026_Sortition_73289489.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21083779)

## Citation

> Daniel Ari Friedman (2026). *Sortition Upstream of NTQR*. Zenodo. DOI: 10.5281/zenodo.21083779. URL: https://doi.org/10.5281/zenodo.21083779.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
