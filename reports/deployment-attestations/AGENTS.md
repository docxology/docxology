# AGENTS.md — `reports/deployment-attestations/`

Post-deploy attestations, one hash-named JSON per deployed SHA: each records
`attested_at`, `deployment_sha`, and a `result` (all three committed receipts read
`passed` as of 2026-11-02). They are written by
`code/orchestrators/attest_release.py` and consumed by the release-integrity checks.

- An attestation binds evidence to a deployed commit: a release-ready claim needs this
  receipt to connect every required report to that exact SHA. Read the JSON for which
  SHA it covers rather than assuming it describes the current deployment.
- Do not hand-write or edit one; produce a new attestation through the orchestrator
  after a real deployment.
- `build_release_integrity.py` and the release-evidence tests are the checks that read
  these files.

Report policy: [`../AGENTS.md`](../AGENTS.md).
