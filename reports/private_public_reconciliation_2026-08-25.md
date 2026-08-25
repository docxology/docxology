# Private-versus-Public Release Reconciliation

Report date: 2026-08-25

Public baseline: `b08dc428` → `b08dc428aa578572feb0977c2c28e1f597b29378`
Private reference: `a73d89b` → `a73d89bc5c759458a5672380d10a2cc2e0c8dadf`

This is a read-only comparison. It neither merges nor cherry-picks private history.

## Disposition Summary

| Classification | Changed paths | Release disposition |
| --- | ---: | --- |
| source metadata | 55 | defer |
| derived output | 245 | regenerate |
| binary intake | 156 | defer |
| other source | 11 | defer |

## Required Release Treatment

- Treat private metadata/bibliography agreement as a review candidate, not independent corroboration or an automatic source port.
- Regenerate every derived output from reconciled public sources; do not copy private rendered files or reports.
- Defer all PDFs, extracted text, and paper-image binaries pending separately verified intake provenance.
- Defer all private-only source changes until a public canonical source or external primary authority is recorded.

## Private Identity Candidates (Deferred)

| Folder | Field | Baseline | Canonical/private | Decision | Local release status |
| --- | --- | --- | --- | --- | --- |
| 2021_NarrativeEcosystems | title | NarrativeEcosystems | Narrative Information Ecosystems: Conflict and Trust on the Endless Frontier | defer | deferred pending independent public authority |
| 2025_OnTime | doi | 10.5281/zenodo.15168381 | 10.5281/zenodo.15168382 | defer | deferred pending independent public authority |

## Deferred Source Metadata

106 metadata fields across 50 paper metadata files remain deferred pending independent public-source verification.

## Evidence Boundary

The report records an internal source comparison only. It does not verify private Zenodo, PDF, image, Scholar, biographical, repository-classification, or generated-claim changes against their external authorities.
