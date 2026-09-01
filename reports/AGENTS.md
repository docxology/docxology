# AGENTS.md — `docxology/reports/`

Added by the 2026-08-29 ongoing-docs fleet pass.

## What this is

Timestamped QA and attestation artifacts for the docxology site: static
accessibility audits, dated browser-QA / browser-smoke / visual-QA run folders,
and deployment attestations. Generated output, not source.

## Layout

- `accessibility_static_YYYY-MM-DD.json` — dated static accessibility audits (2026-05→06 series).
- `browser-qa/YYYY-MM-DD/` — per-run browser QA (`manifest.json` per run: 2026-07-18, 2026-07-29, 2026-08-25, 2026-08-26).
- `browser-smoke/2026-08-26/` — smoke run artifacts.
- `visual-qa/2026-08-26/` — visual QA run artifacts.
- `deployment-attestations/` — per-commit attestation JSON (hash-named).

## Invariants

- Local-only; never commit. Generated artifacts — regenerate, don't hand-edit.
- Live work tree (docxology, 3 remotes) — read, don't write.

## Verify

- `ls docxology/reports | head` — dated JSON series present.
