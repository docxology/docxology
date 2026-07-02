/**
 * Stripe webhook receiver — deployed standalone on Netlify (its own
 * *.netlify.app domain), separate from danielarifriedman.com's GitHub
 * Pages hosting. GitHub Pages can't run server-side code, so this
 * function is the actual handler; Stripe's registered endpoint URL
 * points at this deployment's URL, not at the GitHub Pages domain.
 *
 * Verifies the Stripe-Signature header per Stripe's documented scheme
 * (https://stripe.com/docs/webhooks/signatures) using Node's built-in
 * `crypto` module — no Stripe SDK dependency needed for this.
 *
 * Required environment variable (set via `netlify env:set` or the
 * Netlify dashboard, never committed):
 *   STRIPE_WEBHOOK_SECRET — the whsec_... signing secret for this endpoint.
 */

const crypto = require("crypto");

const SIGNATURE_TOLERANCE_SECONDS = 300;

exports.handler = async (event) => {
  if (event.httpMethod !== "POST") {
    return { statusCode: 405, body: "Method Not Allowed" };
  }

  const signatureHeader = event.headers["stripe-signature"];
  if (!signatureHeader) {
    return { statusCode: 400, body: "Missing Stripe-Signature header" };
  }

  // Stripe signs the exact raw body — Netlify base64-encodes it in some
  // content-type/size cases, so decode conditionally rather than assuming.
  const payload = event.isBase64Encoded
    ? Buffer.from(event.body, "base64").toString("utf8")
    : event.body;

  const verified = verifyStripeSignature(
    payload,
    signatureHeader,
    process.env.STRIPE_WEBHOOK_SECRET
  );
  if (!verified) {
    return { statusCode: 400, body: "Signature verification failed" };
  }

  let stripeEvent;
  try {
    stripeEvent = JSON.parse(payload);
  } catch {
    return { statusCode: 400, body: "Invalid JSON payload" };
  }

  if (stripeEvent.type === "checkout.session.completed") {
    recordSale(stripeEvent);
  }

  return {
    statusCode: 200,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ received: true }),
  };
};

/**
 * Verify payload against Stripe's `t=...,v1=...` signature header.
 * Returns false on any malformed header, missing secret, expired
 * timestamp, or signature mismatch — never throws.
 */
function verifyStripeSignature(payload, signatureHeader, secret) {
  if (!secret) return false;

  const parts = Object.fromEntries(
    signatureHeader.split(",").map((kv) => {
      const [k, v] = kv.split("=");
      return [k, v];
    })
  );
  const timestamp = parts.t;
  const expectedSig = parts.v1;
  if (!timestamp || !expectedSig) return false;

  const nowSeconds = Math.floor(Date.now() / 1000);
  if (Math.abs(nowSeconds - Number(timestamp)) > SIGNATURE_TOLERANCE_SECONDS) {
    return false;
  }

  const signedPayload = `${timestamp}.${payload}`;
  const computedSig = crypto
    .createHmac("sha256", secret)
    .update(signedPayload)
    .digest("hex");

  return timingSafeEqualHex(computedSig, expectedSig);
}

function timingSafeEqualHex(a, b) {
  if (a.length !== b.length) return false;
  try {
    return crypto.timingSafeEqual(Buffer.from(a, "hex"), Buffer.from(b, "hex"));
  } catch {
    return false;
  }
}

/** Log-only for now — no persistence layer wired up yet. */
function recordSale(stripeEvent) {
  console.log(
    "checkout.session.completed",
    stripeEvent.id,
    stripeEvent.data && stripeEvent.data.object && stripeEvent.data.object.id
  );
}
