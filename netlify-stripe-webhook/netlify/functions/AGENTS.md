# AGENTS.md — `netlify-stripe-webhook/netlify/functions/`

The webhook handler (`stripe-webhook.js`): the code that receives Stripe events for the
service.

- Treat it as production code for a service outside the repository's CI: verify signing
  behaviour and error handling locally before deploying, and never log or commit
  secrets — the signing material belongs in Netlify's environment configuration.
- No test in this repository executes this function.

Repository rules: [root guide](../../../AGENTS.md).
