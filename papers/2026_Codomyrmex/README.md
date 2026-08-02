# Codomyrmex: An Artificial Ecology for Agentic Software Development

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21750800.svg)](https://doi.org/10.5281/zenodo.21750800)

---

## Abstract

Agentic software can preserve task state while still forgetting the consequences of prior actions. Codomyrmex studies a narrow control-plane question: after a caller reports a failed action at one software location, can the system deterministically increase friction for a materially similar proposal at that location without changing an unrelated target? Its Colony Control Plane records consequence reports and couples them to target-indexed signal pressure, agent trust, role labels, resource accounting, adversarial checks, and an explicit EXECUTE/HOLD/REFUSE gate. The implementation comprises 8 cooperating subsystems. The ordinary Model Context Protocol path remains caller-reported and unattested. Optional and required `ColonyKernel` attestation modes instead bind proposal, verdict, authorization, execution receipt, and outcome in a signed, hash-linked local ledger. That ledger protects lifecycle linkage but does not independently observe external actuation or establish deployment safety. Consequence records can use file-backed SQLite; the default MCP kernel and signal field remain process-local. Evaluation is limited to implementation properties and controlled fixtures. At composition time, the scoped Colony Kernel surface contains 819 passing tests with 76.6% branch coverage, 0 Ruff errors, and 0 ty diagnostics. A paired deterministic replay moves the same-target proposal from 0.875/EXECUTE to 0.725/HOLD after a reported failure while leaving an unrelated target unchanged. Separate fixtures exercise trust promotion, bounded arithmetic, linear signal decay, local attestation integrity, and interface behavior. These results support reproducible software contracts, not ecological optimality, calibrated risk, production harm reduction, or generalization to external workloads. The report contributes the typed control plane, transparent gate, coupled local feedback, authenticated local lifecycle option, and source-bound publication workflow. Generated variables, figures, citations, claim boundaries, and release receipts tie the rendered report to the evaluated checkout. End-to-end external-actuation attestation, restart-persistent field storage, representative benchmarks, and independent deployment validation remain open.

## Keywords

ai-agents · model-context-protocol · mcp · multi-agent · orchestration · colony-control-plane · stigmergy · artificial-ecology · agentic-software-engineering · falsification-worker · actuation-gate · trust-scoring

## Artifacts

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.21750800](https://doi.org/10.5281/zenodo.21750800) |
| **Published** | 2026-08-01 |
| **Version** | 1.3.0 |
| **Zenodo record** | https://zenodo.org/records/21750800 |

## Files

- `codomyrmex-1.3.0.pdf` - Zenodo PDF
- `codomyrmex-1.3.0-content.pdf` - Zenodo PDF

## Citation

> Daniel Ari Friedman (2026). *Codomyrmex: An Artificial Ecology for Agentic Software Development*. Zenodo. DOI: 10.5281/zenodo.21750800. URL: https://doi.org/10.5281/zenodo.21750800.

## Related

- Zenodo record: https://zenodo.org/records/21750800
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
