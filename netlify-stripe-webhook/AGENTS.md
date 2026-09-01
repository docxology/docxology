# AGENTS.md — `docxology/netlify-stripe-webhook`

Added by the 2026-08-29 ongoing-docs fleet pass.

## What this is

Netlify-hosted Stripe webhook service accompanying the docxology site (membership payments).

## Layout

- netlify/functions/, public/, local .netlify/ build state.

## Invariants & gotchas

- Local-only under `projects/ongoing/` — never commit.
- Live repo tree: read, don't write (see lane-root AGENTS.md for which trees are dirty).

## Verify

- `ls docxology/netlify-stripe-webhook`
