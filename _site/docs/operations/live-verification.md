# Live verification

Run the verifier after the bounded Pages deployment has completed. It compares
cache-busted public routes and JSON payloads against the local canonical graph,
then records the Pages API deployment status.

```bash
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/verify_live_site.py
```

Require 17/17 route checks, current JSON-level counts, a `built` Pages status,
and a successful deployment for a release. During propagation, a 404 for a
route that exists locally may be classified as `deployment_pending`; a route
missing locally is always a hard failure. Check the resulting
`reports/live_site_verification_*.json` into the release envelope only after the
deployment commit and workflow run are confirmed.
