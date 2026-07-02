# Stripe webhook handler for danielarifriedman.com

## Why this exists (and why it's a separate deployment)

`danielarifriedman.com` is GitHub Pages by design — static files only, no
server-side code execution — and stays that way. Stripe's registered
endpoint (`fascinating-voyage`, `checkout.session.completed`) needs a
real HTTP handler somewhere, so this is deployed standalone on Netlify
(its own `*.netlify.app` domain), with **Stripe's webhook endpoint URL
pointed at this deployment**, not at the GitHub Pages domain. No DNS
change to danielarifriedman.com is required — this is a fully separate
site under the same Netlify account.

(An earlier version of this scaffold targeted Cloudflare Workers, which
would have required moving the domain's DNS to Cloudflare. Replaced with
this Netlify version per direction to keep danielarifriedman.com on
GitHub Pages untouched.)

## What it does

`netlify/functions/stripe-webhook.js` verifies the `Stripe-Signature`
header per Stripe's documented HMAC scheme using Node's built-in
`crypto` module (no Stripe SDK dependency). On a verified
`checkout.session.completed` event, it logs the event id and object id.
Fulfillment (download links, email, etc.) is deliberately **not**
implemented yet — this only proves the signature and records that the
sale happened.

Handles the base64-encoded-body case Netlify Functions can hit
(`event.isBase64Encoded`) — Stripe's signature is computed over the
exact raw body, so this must be decoded correctly before verification,
not just read from `event.body` directly.

## Deploy

Netlify CLI is already authenticated on this machine as
`danielarifriedman@gmail.com`.

```bash
cd projects/ongoing/docxology/netlify-stripe-webhook
netlify init   # first time only — creates/links the site
netlify env:set STRIPE_WEBHOOK_SECRET "whsec_..."   # paste the real value — never commit it
netlify deploy --prod
```

Note the deployed URL from the output (`https://<site-name>.netlify.app`).

## Point Stripe at it

In the Stripe dashboard (Developers → Webhooks → the `fascinating-voyage`
endpoint), update the endpoint URL to
`https://<site-name>.netlify.app/.netlify/functions/stripe-webhook`.

## Verifying it's live

```bash
curl -i -X POST https://<site-name>.netlify.app/.netlify/functions/stripe-webhook \
  -H "Content-Type: application/json" -d '{}'
# Expect 400 "Missing Stripe-Signature header" — that's the signal the
# function is actually receiving the request, not a platform-level 404/405.
```

Then trigger a real test event from the Stripe dashboard
(Developers → Webhooks → fascinating-voyage → "Send test webhook") and
confirm a 200 with `{"received": true}`.
