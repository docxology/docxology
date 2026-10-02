<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20417016-blue)](https://doi.org/10.5281/zenodo.20417016)

---

## Abstract

> This paper presents Deterministic bounded AutoResearch for a small MNIST neural-network task, a public template exemplar that turns an AutoResearch loop into ordinary reproducible research infrastructure. The case study is intentionally small but concrete: 2000 training and 500 test images from MNIST handwritten digit database are evaluated by the bounded small MNIST neural-network classification loop. The run evaluates 4 of 5 proposed candidates, including Tiny patch-attention classifier, selects exp-mlp-tanh-64 (MLP, 50890 parameters), and improves test_accuracy from 82.6% to 89.4% (6.8% absolute change). The validated diagnostic layer reports macro F1 89.4%, bootstrap accuracy interval 86.4% to 92.0%, Brier score 0.161, negative log likelihood 0.361, top-2 accuracy 95.6%, and exact McNemar p-value 0.000. The same pipeline writes proposal, candidate, run, review, benchmark, evidence, figure, confusion-matrix, statistical-summary, probability-quality, and security-integrity artifacts from declared output contracts; uses 0 LLM calls at USD 0.00 cost; and records 7 configured stages, 6 supported local-artifact claims, and 78 required artifacts. The local security attestation status is passed, with 0 checksum mismatch(es). The final readiness status is passed, with review gates deferred to a human rather than self-approved by the generated run.

## Keywords

`autoresearch` · `reproducible research` · `machine learning benchmark` · `artifact readiness` · `human review` · `local artifact integrity`

## Methods

- **Offline MNIST subset: 2000 train / 500 test images, seed 20260525** — Uses a committed, class-balanced local MNIST subset with recorded provenance hashes; no data are downloaded at runtime.
- **Bounded candidate search over MLP, softmax, nearest-centroid, patch-attention** — Evaluates at most 4 configured candidates against a nearest-centroid baseline, choosing by test accuracy with deterministic tie-breaks.
- **Seven-stage AutoResearch pipeline with file-backed ledgers** — Runs 7 configured stages, writing proposal, candidate, run, phase and review ledgers that hydrate manuscript variables.
- **Safety controls: proposal-only autonomy, no LLM calls, deferred review** — Defaults to proposal_only autonomy, records 0 LLM calls and no cost, never executes generated code, and leaves publication approval to a human.
- **Statistical diagnostics: Wilson intervals, bootstrap, McNemar, calibration** — Reports Wilson score intervals, deterministic bootstrap intervals, paired discordance tests, Brier score and negative log likelihood.

## Key Findings

- The loop selected exp-mlp-tanh-64 after evaluating 4 of 5 proposed candidates, raising test accuracy from the 82.6% baseline to 89.4%.
- Diagnostics report macro F1 of 89.4%, a bootstrap accuracy interval of 86.4% to 92.0%, and top-2 accuracy of 95.6%.
- The selected candidate was top-ranked in 72.5% of deterministic bootstrap resamples, with exp-mlp-relu-32 as runner-up.
- The local security attestation passed with 0 checksum mismatches, and readiness passed with review gates deferred to a human.
- The paper states its contribution is not a new MNIST classifier but a template showing bounded AutoResearch run through a reproducible-paper lifecycle.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_autoresearch_project](https://github.com/docxology/template_autoresearch_project)
- GitHub release: [v0.3.2](https://github.com/docxology/template_autoresearch_project/releases/tag/v0.3.2)
- DOI: [10.5281/zenodo.20417016](https://doi.org/10.5281/zenodo.20417016)
- Zenodo record: [https://zenodo.org/records/20417016](https://zenodo.org/records/20417016)
- PDF: [Friedman_2026_Bounded_537dd8a6.pdf](Friedman_2026_Bounded_537dd8a6.pdf)
- PDF: [Friedman_2026_Bounded_e07b6285.pdf](Friedman_2026_Bounded_e07b6285.pdf)
- PDF: [Friedman_2026_Bounded_f02abeea.pdf](Friedman_2026_Bounded_f02abeea.pdf)
- PDF SHA-256: e07b62850a1995935283d37a45c21d71fa7c4e69cdcc451c5a1ea8aee6d0c94a

## Citation

> Daniel Ari Friedman (2026). *Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task*. Zenodo. DOI: 10.5281/zenodo.20417016. URL: https://doi.org/10.5281/zenodo.20417016.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
