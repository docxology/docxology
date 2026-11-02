# AGENTS.md — `netlify-stripe-webhook/`

The repository's only server-side component: a small Netlify service that receives
Stripe webhook events. The public site stays static GitHub Pages by design — no
server-side execution there — so this service exists separately, with its own
`netlify.toml`, function, and public page.

- Its secrets (the Stripe signing material) live in Netlify's configuration, never in
  the repository; nothing here should need a credential to be read.
- Its tests and runbook live with the service or in `docs/operations/`, not here; this
  guide cannot tell you what is currently deployed.

Repository rules: [root guide](../AGENTS.md).
