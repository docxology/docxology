# Evidence and coverage refresh

Public APIs and profile pages are freshness evidence, not automatic replacements
for curated rows. Refresh before a claim-sensitive release, then review every
change before regeneration.

```bash
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/refresh_public_sources.py
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/refresh_public_source_inventory.py
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/build_github_inventory.py
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/sync_paired_publications.py --include-aii
uv run python3 code/orchestrators/build_public_source_review.py
```

`build_public_source_review.py` writes a dated JSON and Markdown review record
under `reports/`. It is deliberately read-only with respect to curated source:
it never edits bibliography rows, paper metadata, claims, Scholar metrics,
repository classifications, or generated site data. Its `--check` mode
re-renders both artifacts without writing and fails on any difference.

For a pre-deploy committed review, the renderer records the latest non-control
payload revision. This permits the dated review itself to be committed in the
same narrow control tail as the Pages manifest without making its no-write
check self-referential. It is not a deployment receipt. After Pages has
deployed a clean candidate checkout, regenerate the review with
`--exact-source-revision` before creating the deployment attestation; that
mode binds its `source_commit` and `source_tree_sha` to the exact current
candidate `HEAD` required by `validate_repo.py --release`.

If the GitHub–Zenodo scan is rate-limited or otherwise refuses to write a
fresh pairing report, do not let the prior dated report stand in for the failed
refresh. Record the bounded failure in the review artifact instead:

```bash
uv run python3 code/orchestrators/build_public_source_review.py \
  --pairing-refresh-status failed \
  --pairing-refresh-note "GitHub release API rate-limited; sync_paired_publications.py refused 403/429 warnings"
```

Without that flag, the builder still marks a pairing report older than the
selected public-source snapshot as deferred and stale.

The review record assigns each candidate one of `applied`, `deferred`, or
`rejected`, and explicitly includes:

- GitHub–Zenodo candidates and ambiguous DOI/release relations;
- DOI-role reconciliation proposals or conflicts;
- repository-classification queue rows;
- Scholar metrics; and
- every time-sensitive biographical claim in the claims ledger.

Treat a public endpoint response as evidence for review, not evidence that a
claim should be rewritten. In particular, Scholar metrics remain **deferred**
unless a direct authenticated verification receipt is supplied. A valid receipt
must name the canonical `profile_id`, state `direct: true` and
`authenticated: true`, include `verified_at`, and provide non-negative integer
`citations`, `h_index`, and `i10_index` fields under `metrics`. Even then, a
difference is only a reviewed candidate: update
`data/scholar-snapshot.json` deliberately, run
`sync_scholar_metrics.py`, and regenerate dependent outputs afterward.

The release source contract is stricter than the review queue: every curated
snapshot is bound to
[`data/scholar-verification-receipt.json`](../../data/scholar-verification-receipt.json).
That sidecar records the direct/authenticated assertion, the canonical metrics
and as-of date, a source/method note, and the SHA-256 of the exact snapshot
bytes. Update the receipt in the same review as any snapshot edit, then run
`uv run python3 code/orchestrators/sync_scholar_metrics.py --check`; a stale,
missing, anonymous, or mismatched receipt fails before derived surfaces can be
accepted. The sidecar can preserve an already-verified baseline across later
releases; it is not evidence that a new external refresh found a change.

Use an explicit review record before applying any queue item. For example, a
DOI-role proposal must be reviewed and supplied back to
`reconcile_paper_dois.py --apply`; a pairing decision belongs in
`data/paired-publication-decisions.json`; and catalog decisions belong in the
human-reviewed software/source records. Regenerate only deterministic
derivatives after those source decisions are made, then rebuild this report for
the candidate release revision.

Public-source observations and time-sensitive biographical claims use separate
durable review inputs: `data/public-source-observation-decisions.json` and
`data/biographical-claim-decisions.json`. Each decision names the exact queue
item, a timezone-qualified reviewer decision, rationale, and SHA-256 digests
of the observed evidence. The review renderer accepts an acknowledgement or
rejection only when those hashes still match; changed evidence returns the item
to `deferred`. An acknowledgement may explicitly record that no curated claim
change was required. Do not advance a snapshot baseline merely to make an
unreviewed observation disappear.

Apply only strong, reviewed GitHub–Zenodo pairs. Record ambiguous outcomes in
`data/paired-publication-decisions.json`; do not auto-create bibliography rows
from a plausible title match. Rebuild `data/coverage-exceptions.json` to keep
legitimate missing-folder, missing-full-text, no-DOI, no-URL, and non-paper
records explicit.

Google Scholar counts and current organizational roles require direct primary
verification. If a signed-in or otherwise authoritative view is unavailable,
keep the dated snapshot and caveat rather than guessing. Finish with
`regenerate_all.py --validate`, then inspect the newest source, reconciliation,
and pairing reports.
