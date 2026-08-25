# Report retention

Historical reports are evidence, not disposable build by-products. The current
report set remains served by Pages; older material is retained in Git history or
a release archive only after its provenance is recorded. This policy applies
before any historical report or screenshot directory is removed.

## Retention classes

- **Current:** the latest report required by validation stays in the repository
  and the Pages projection.
- **Archive:** superseded evidence may move out of the Pages projection only
  when a durable Git commit, GitHub release asset, or externally stable archive
  location is recorded.
- **Remove from checkout:** only an archived item with a reviewed entry in
  [`data/report-retention.json`](../../data/report-retention.json) may be
  pruned. This does not authorize rewriting Git history.

## Required provenance record

Before running `prune_old_reports.py --apply`, add one entry per candidate to
`data/report-retention.json` with all of these fields:

```json
{
  "path": "reports/visual-qa/2026-07-18",
  "generated_at": "2026-07-18T01:55:49Z",
  "provenance_sha256": "sha256 of the manifest or archive index before removal",
  "replacement_location": "git:<commit> or a durable release/archive URL",
  "decision": "remove-from-checkout",
  "reviewed_by": "name or accountable role"
}
```

The pruning tool rejects an incomplete record before deleting anything. Keep
the retention manifest itself in the release commit so later reviewers can
reconstruct why an artifact left the working tree.

## Operating sequence

1. Run the pruner without `--apply` and inspect its candidates.
2. Capture the source manifest/hash and create reviewed entries.
3. Confirm every `replacement_location` is durable and accessible to the
   intended audience.
4. Run the pruner with `--apply --retention-manifest data/report-retention.json`.
5. Regenerate manifests, validate links, and record the removal in the release
   change log.

No network snapshot, evidence ledger, publication-pairing report, or source
material is eligible for automatic pruning.
