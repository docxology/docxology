# Live verification

Run the verifier after the bounded Pages deployment has completed. It compares
cache-busted public routes and JSON payloads against the local canonical graph,
then records the Pages API deployment status and selected deployment run.
Use an authenticated `gh` session and a clean checkout of the candidate:

```bash
candidate_sha="$(git rev-parse HEAD)"
uv run python3 code/orchestrators/verify_live_site.py \
  --expected-commit "$candidate_sha" \
  --output /tmp/live-site-verification.json
```

For a specific Pages run, also pass its numeric ID with `--deployment-run-id`.
This requires `--expected-commit` and looks up that exact run rather than
selecting a later successful deployment. The binding requires the checkout and
deployment to match the candidate, a clean source tree, a completed successful
main-branch run, and the declared Pages workflow name and path. Wrong or stale
run identities fail even if every route marker passes.

The `workflow_run` follow-up checks out the triggering `head_sha` and supplies
the triggering run ID. A queued job therefore cannot float to a newer main
commit. Manual follow-ups are restricted to main. IndexNow likewise reads the
deployed candidate's sitemap rather than whichever commit is newest when its
job starts.

Require `overall_ok: true`, every configured route passing, current JSON-level
counts, a `built` Pages status, and successful candidate/run binding for a
release. A clean, matching candidate with a completed built deployment cannot
classify a missing route as propagation merely because that file exists locally.
For that clean, matching candidate, a 404 after Pages reports `built` is a hard
failure. Explicit source/deployment lag or a Pages `building`/`queued` status
may defer a mismatched 200 response or a locally
present 404; transport status 0, server errors, and locally absent routes remain
hard failures. A deferred report retains `overall_ok: false` and does not
establish release acceptance.

Recorded success, propagation, Pages, and binding flags must be JSON booleans;
marker, JSON-contract, and structured-data checks must contain booleans as well.
Strings such as `"false"` and integers such as `1` cannot stand in for success.
Legacy successful rows may omit their explicit `ok` field, but their status and
recorded contracts must still pass. A required binding cannot claim success with
missing or failed checks.

A completed probe writes the dedicated JSON receipt before failing on route or
binding errors. The workflow attempts the summary and artifact upload even
after freshness or verification failure, retains receipts for 90 days, and fails
the upload if no fresh receipt exists. Argument or checkout preflight failures
may produce no receipt; inspect their failed step instead of substituting an
older checked-in report. Default unbound capture still writes a dated report
under `reports/` for maintenance, and must not be mistaken for candidate-bound
acceptance.

`--check` validates an existing report offline against the current count
fingerprint and hard-failure rules. `--allow-source-count-drift` is only for
explicit offline candidate validation; it does not refresh observations or
turn a cached receipt into live acceptance. Candidate/run binding requires a
fresh probe and cannot be combined with `--check`.

This verifier establishes route markers, public JSON contracts, and deployment
identity. The Pages deployment's separate
[`verify_deployed_artifact.py`](../../code/orchestrators/verify_deployed_artifact.py)
receipt checks manifest, work-page, and critical-asset byte hashes, archived-PDF
response contracts, and sample PDF byte hashes against the candidate. Those
targeted technical checks remain distinct from
whole-artifact coverage and human-reviewed release attestation. Preserve older
dated receipts, and add the current receipt to the release envelope only after
its actual deployment commit and workflow run are confirmed.

The 2026-10-02 verifier/workflow refinement received an independent local review
and 89 passing focused regression tests with no skips. That evidence covers
the implemented binding and failure rules; hosted follow-up execution and live
acceptance require their own candidate-bound receipts.
