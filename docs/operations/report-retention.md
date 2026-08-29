# Report retention

Historical reports are evidence, not disposable build by-products. Current
report manifests remain served by Pages; dated visual-QA screenshot binaries
remain committed in GitHub but are intentionally omitted from the bounded Pages
artifact. Older material is retained in Git history or a release archive only
after its provenance is recorded. This policy applies before any historical
report or screenshot directory is removed.

## Retention classes

- **Current:** the latest report required by validation stays in the repository
  and its manifest stays in the Pages projection. Visual-QA screenshot binaries
  remain in the repository with their manifest SHA-256 values and are retrieved
  through the manifest's repository-relative path plus a GitHub raw/tree
  template for the commit that contains the evidence.
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
  "path": "reports/visual-qa/<YYYY-MM-DD>",
  "generated_at": "<ISO-8601 generation time of the set>",
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

## Appendix: 2026-08-29 prune run (Option C)

On 2026-08-29 the first full application of this policy removed 4 superseded,
dated report sets, freeing **111.5 MB**:

| Path | Replacement |
| ---- | ----------- |
| `reports/visual-qa/2026-07-18` | `git:e7b6a45d68d5365d54b8f9d542ec589b1c351c1f` |
| `reports/visual-qa/2026-08-25` | `git:512cf51ba6287d535aab0a70774ea2faad702259` |
| `reports/browser-smoke/2026-07-29` | `git:57b5f35b95389f9db42644fc6cf526f3aa2418dc` |
| `reports/browser-smoke/2026-08-25` | `git:512cf51ba6287d535aab0a70774ea2faad702259` |

Each entry in [`data/report-retention.json`](../../data/report-retention.json)
records the set's generation time, the SHA-256 provenance hash of the
manifest before removal, the durable `git:` replacement commit, and the
reviewer identity, exactly as this document requires. Removal was from the
working checkout only; no history was rewritten and the current
browser/visual-QA manifests remain in the Pages projection.

**Scan-skip fix in `prune_old_reports.py`:** the pruner's reference safety net
(keep a dated subdir if any tracked file outside it references that path)
previously misread two surfaces as live references and blocked legitimate
pruning:

1. `_site/` — the generated local build projection mirrors the whole tree,
   including historical report paths, without being an actual consumer.
2. `data/report-retention.json` — the retention manifest names the very paths
   it authorizes for removal; reading it as a reference made every candidate
   self-blocking.

`code/orchestrators/prune_old_reports.py` now excludes both (`_site` in the
working-tree skip set; `data/report-retention.json` in the
pathspec exclusions of its tracked-reference scan). The pinned behavior is
covered by `code/tests/test_prune_old_reports.py`. Strategic rationale and
revisit triggers for this prune: see
[`asset-strategy-adr.md`](asset-strategy-adr.md).
