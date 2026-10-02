# AGENTS.md — `docxology/netlify-stripe-webhook`

## What this is

Netlify-hosted Stripe webhook service accompanying the docxology site (membership payments).

## Layout

- netlify/functions/, public/, local .netlify/ build state.

## Invariants & gotchas

- Commit only reviewed public content authorized by the user; preserve concurrent edits.
- Live repo tree: read, don't write (see lane-root AGENTS.md for which trees are dirty).

## Verify

- `ls netlify-stripe-webhook`
