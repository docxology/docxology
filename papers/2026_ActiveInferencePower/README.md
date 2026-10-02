<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 Active Inference Power Suite: Conditional Statistical Power under Controlled Generative Settings

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21695160-blue)](https://doi.org/10.5281/zenodo.21695160)

---

## Abstract

> Statistical power is an investigator-facing operating characteristic of an adaptive-study design. Before simulation, the investigator fixes an agent-side model, evaluator-side process, testing setting, policy, and replication plan. Each embedded agent acts only on visible history; simulated hidden truth is retained for scoring. active_inference_power makes that conditional estimand inspectable. The suite combines fixed-horizon procedures, analytic references, dependence/calibration experiments, and a discrete-state active-inference agent checked against a binary oracle. It extends this to action loops with sensing reliability, latent context, target choice, cost, and stopping. The study distinguishes model-relative posterior belief from calibrated p-value and likelihood-ratio e-process evidence. It compares Benjamini–Hochberg (BH) false discovery rate (FDR) procedures with family-wise error rate (FWER) alternatives, and separates either evidence object from online FDR procedure-specific accounting. Results are scenario-indexed finite-simulation estimates with Monte Carlo standard error (MCSE) and declared error, dependence, filtration, and optional-stopping boundaries; they do not assign a universal power value to an agent, task environment, or active inference. Instead, they support auditable comparisons among explicitly declared adaptive-study designs. Contracts, seed schedules, certificates, figures, claim ledger, and rendered manuscript form a linked evidence chain, allowing readers to trace each claim to its design and artifact. Source and release materials are available at the verified GitHub repository ActiveInferenceInstitute/active_inference_power.
>
> Active Inference Power Suite v1.0.0 is a source-bound release of an adaptive-study design suite. It reports scenario- and policy-indexed finite-simulation operating characteristics; it does not claim a universal "power of active inference."
>
> Source repository and exact release: https://github.com/ActiveInferenceInstitute/active_inference_power/releases/tag/v1.0.0
>
> Concept DOI (release family): 10.5281/zenodo.21695160 (https://doi.org/10.5281/zenodo.21695160)
>
> Version DOI (this immutable archive): 10.5281/zenodo.21695161 (https://doi.org/10.5281/zenodo.21695161)
>
> Zenodo record: https://zenodo.org/records/21695161
>
> PDF SHA-256: 24fa25a4f29affcfd92c8c001ff6487a0c36960c6b4f38ed4419984fc8743cbf
>
> The uploaded PDF, exact tag-derived source archive, release manifest, renderer provenance, and final review receipt make the release auditable. The evidence boundary remains finite, scenario-specific simulation rather than a universal theorem or deployment claim.

## Keywords

`multiple testing` · `false discovery rate` · `Benjamini-Hochberg` · `statistical power` · `active inference` · `pymdp` · `sequential hypothesis testing` · `reproducible research`

## Methods

- **Power estimated as an operating characteristic of an investigator-declared design** — Defines power over replications of a declared model/process/setting/policy design, scoring traces against evaluator-only hidden truth.
- **Seeded Monte Carlo comparison of 9 FWER/FDR correction procedures** — Compares Bonferroni, Šidák, Holm, Hochberg, BH, BY, Storey, adaptive BH and weighted BH on a seeded two-groups design with MC SE bands.
- **Dependence-regime stress grid for BH and BY** — Evaluates BH and BY FDR and power under negative equicorrelation, independence, positive-factor and block covariance regimes.
- **Discrete-state active-inference agent: posterior threshold vs BH on calibrated p-values** — Runs identical streams through a posterior-threshold decision and a BH-calibrated evidence rule under strong and weak evidence regimes.
- **Action-in-the-loop policies with sensing reliability, cost and stopping** — Compares fixed-horizon, posterior-cutoff, information-gain, cost-aware, posterior-sampling and e-process stopping policies in a synthetic action loop.

## Key Findings

- In the configured design, FWER-oriented procedures reached power 0.315–0.321 while FDR-oriented procedures reached 0.430–0.749, framed as the expected trade-off, not dominance.
- Storey's paired power gain over BH was about 0.073, which the paper stresses is an operating-characteristic comparison, not a validity certificate.
- Under weak evidence the posterior-threshold policy had FDR 0.153 and FWER 0.366, while the calibrated BH policy made no rejections, illustrating a calibration gap.
- Across the dependence grid, BH estimates stayed within the finite-simulation band and BY stayed more conservative; the paper states this is not a new PRDS proof.
- The paper concludes power numbers should not be carried into a new design; adaptive actions change data path, cost and evidence contract together.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [ActiveInferenceInstitute/active_inference_power](https://github.com/ActiveInferenceInstitute/active_inference_power)
- GitHub release: [v1.0.0](https://github.com/ActiveInferenceInstitute/active_inference_power/releases/tag/v1.0.0)
- DOI: [10.5281/zenodo.21695160](https://doi.org/10.5281/zenodo.21695160)
- Zenodo record: [https://zenodo.org/records/21695160](https://zenodo.org/records/21695160)
- PDF: [active_inference_power_v1.0.0.pdf](active_inference_power_v1.0.0.pdf)
- PDF SHA-256: 24fa25a4f29affcfd92c8c001ff6487a0c36960c6b4f38ed4419984fc8743cbf

## Citation

> Daniel Ari Friedman (2026). *Active Inference Power Suite: Conditional Statistical Power under Controlled Generative Settings*. Zenodo. DOI: 10.5281/zenodo.21695160. URL: https://doi.org/10.5281/zenodo.21695160.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
