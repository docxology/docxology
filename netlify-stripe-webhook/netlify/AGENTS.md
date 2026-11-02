# AGENTS.md — `netlify-stripe-webhook/netlify/`

The Netlify side of the webhook service: `functions/` holds the deployed handler(s).
Configuration for the site is the service's `../netlify.toml`.

- Deploys happen from Netlify, not from this repository's CI: a merged change here is
  not a deployed change until Netlify builds it.
- Nothing in this folder is exercised by the repository's test gate.

Repository rules: [root guide](../../AGENTS.md).
