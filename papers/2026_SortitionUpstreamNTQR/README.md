# Sortition Upstream of NTQR

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21083779.svg)](https://doi.org/10.5281/zenodo.21083779)

---

## Abstract

How should you choose the judges, jurors, or reviewers who form a panel — and does
that upstream choice change how well you can evaluate them without an answer key?
A panel can be selected many ways — by competence, by a representative lottery
(sortition), by ideological bloc, or at random — and, separately, its noisy
judgments can be evaluated blind: given the agreement/disagreement pattern among
three binary judges, the ntqr package's error-independent (EIE) evaluator returns
logically consistent estimates of item prevalence and per-judge accuracy with no
labels at all. But that evaluator takes the panel as given. We join the two
questions and ask whether the rule that forms the panel changes the
oracle-referenced error of the no-answer-key evaluation — how far the blind estimate
lands from the answer-key result, lower being better.

On a fully deterministic instrument (96 seeds, 96 experts,
300 items), the dominant lever is which rule forms the panel, not its size:
competence-first selection recovers best (0.037), while
representative, single-bloc, and random selection collapse together — by
construction, because with independent judge errors composition cannot move an
estimator that only sees agreement. Supplying the missing channel — same-group judges
sharing a latent, marginal-accuracy-preserving error confound — makes the strategies
fan out monotonically as within-bloc coupling rises: representative sortition stays
flat while single-bloc selection degrades, the gap widening from 0.000 to
0.112. Within this instrument the relationship is closed-form: recovery
error tracks the panel's Herfindahl concentration index over the axis a shared
error rides on — minimized exactly by a balanced (representative) draw, maximized by a
single bloc — and a continuous representativeness dial confirms error rises
monotonically with it.

The protection is conditional: re-keying the confound to an axis the lottery does
not balance erases the protection (0.147→0.229). The
lesson for selecting and evaluating panels is thus a falsifiable, simulation-bounded
prediction, not a preference for any one rule — representativeness protects blind
recovery precisely when the panel balances the attribute a shared error rides on.
Evidence is synthetic and oracle-scored; in a single small live model
(gemma3:4b) the synthetically-best competence-first rule was the worst,
illustrating that a selection rule validated on parameterized judges need not carry
over to prompted ones — a hypothesis to test, not an established caution. All methods
and documentation are openly available at the public repository
docxology/ntqr_allotment.

---
Associated artifacts
GitHub release: v0.1.0 (https://github.com/docxology/ntqr_allotment/releases/tag/v0.1.0)
DOI: https://doi.org/10.5281/zenodo.21083779
Zenodo: https://zenodo.org/records/21083779
PDF SHA-256: 73289489d2d123f198ccee83adac10e61a752805d908970030c2d5ac009061e4

## Keywords

sortition · NTQR · unlabeled evaluation · expert panels · peer review · error independence · statistical power · panel formation · synthetic evaluation · LLM reviewers

## Publication Details

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.21083779](https://doi.org/10.5281/zenodo.21083779) |
| **Published** | 2026-06-25 |
| **Version** | 0.1.0 |
| **Zenodo record** | https://zenodo.org/records/21083779 |
| **GitHub release** | https://github.com/docxology/ntqr_allotment/releases/tag/v0.1.0 |
| **Source repository** | https://github.com/docxology/ntqr_allotment |

## Files

- `Friedman_2026_Sortition_73289489.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *Sortition Upstream of NTQR*. Zenodo. https://doi.org/10.5281/zenodo.21083779

## Related

- Zenodo record: https://zenodo.org/records/21083779
- GitHub release: https://github.com/docxology/ntqr_allotment/releases/tag/v0.1.0
- Source repository: https://github.com/docxology/ntqr_allotment
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
