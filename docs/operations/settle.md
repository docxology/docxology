# Settle driver

`code/orchestrators/settle.py` is the one-command way to finish a change: it
classifies the dirty paths, runs the tiered check battery (stopping at the
first failure), and only then lands the payload and control-tail commits. It
replaces the manual rhythm of *payload commit, control-tail commit, then the
gate cascade by hand* with a single driver whose exit code answers one
question: is this work safe to push?

```bash
python3 code/orchestrators/settle.py [--tier fast|full|release] [--dry-run] \
  [--commit-message MSG] [--push] [--pr TITLE] [--skip-commit]
```

The driver is standard-library Python; the battery it shells out to runs
through `uv` exactly like CI.

## Tier battery

Each tier extends the one below it. Checks run in the listed order and the
run stops at the first failure.

| Tier | Battery (in order) | Measured cost |
| --- | --- | --- |
| `fast` | `build_sitemap.py --check`; `code/src/artifact_budget.py`; `ruff check code` | sitemap `--check` ~0.8s; budget gate is a single JSON read (near-instant); whole tier a few seconds |
| `full` | fast battery + `pytest code/tests -q` + `validate_repo.py` (standard, no `--release`) | minutes — standard validation runs the full local generation-check battery |
| `release` | full battery + `validate_repo.py --release --strict-reports` | minutes (adds release-evidence checks; see below) |

The full tier is the CI-equivalent one: it runs the same four checks as the
`validate` job of [`.github/workflows/validate.yml`](../../.github/workflows/validate.yml)
— `validate_repo.py`, `pytest code/tests -q`, `ruff check code`, and the
`code/src/artifact_budget.py` budget gate (settle orders the cheap floor
first; CI lists `validate_repo` first, but the set is identical). The validate
job's separate generator-drift review step (`build_video_pages.py --check`,
~5.7s, plus `build_work_pages.py --check`) is belt-and-suspenders:
`validate_repo.py` already runs both checks internally via its generation-plan
no-write battery, so settle's full tier covers them; the rendered-browser
`browser-tests` CI job is a separate job settle does not mirror. A green settle
`full` therefore predicts a green `validate` job up to drift-sensitive changes.

## Effective tier

`--tier` is a floor, not a switch. Every run first classifies the dirty paths
(`git status --porcelain`, then `classify_paths` from
`code/src/change_classifier.py`) and raises the tier when the paths demand it:
`fast < full < release`. Nothing is ever refused — the driver prints a
decision line such as
`tier decision: requested=fast path-derived=full -> effective=full` and runs
the stronger battery.

Which tier to reach for:

1. **Unsure?** Start with `--dry-run`: it prints the classification, the
   effective tier, the exact battery commands, the planned commits, and the
   push/PR plan without executing anything.
2. **Reports/docs-only edits** classify as `fast` — landing them with
   `--tier fast` runs the three cheap gates.
3. **Data intake and generated surfaces** (`data/`, `works/`, `papers/`,
   `pages/`, `feeds/`, sitemap) classify as `full` — any surface beyond
   reports/docs raises the tier, so an intake touching `data/` plus its dated
   reports lands at `full` even if you asked for `fast`.
4. **Code changes under `code/`** classify as `full` — the classifier never
   derives `release` from paths, so `release` is strictly opt-in via
   `--tier release`; treat `full` as the landing tier for ordinary code work.
5. **Release confirmation** uses `--tier release`. The added
   `validate_repo.py --release --strict-reports` refuses a dirty worktree
   (everything except `_site/` and ephemeral release evidence must be
   committed) and demands a deployment attestation for the candidate commit.
   settle binds the conventional
   `reports/deployment-attestations/<HEAD>.json` receipt when it exists and
   otherwise lets the step fail closed with validate_repo's own message, so
   the release tier is a *confirmation* pass for an attested candidate: land
   first with a lower tier, then re-run settled and clean:

   ```bash
   python3 code/orchestrators/settle.py --tier full --commit-message "Land the change"
   python3 code/orchestrators/settle.py --tier release --skip-commit --push --pr "Title"
   ```

## Commit chain

After the battery passes (and unless `--dry-run` or `--skip-commit`), the
driver makes two commits on the current branch:

1. **Payload commit** — `git add` of exactly the classified payload paths,
   using `--commit-message` (default: `Settle pending payload changes`).
2. **Control-tail commit** — the classified control paths, with the same
   message plus the ` (control tail)` suffix, per the CONTROL_FILES
   semantics the classifier encodes.

A phase with an empty path set is skipped with a signpost line. Paths the
classifier assigns to neither group are left uncommitted and reported, so a
stray file cannot vanish into a commit silently. Work on a branch: settle
commits wherever you are, and committing on local `main` is a known failure
mode (see the Source-Of-Truth rules in `AGENT_START.md`).

`--push` runs `git push -u origin HEAD` after the commit chain.
`--pr TITLE` then creates a pull request with `gh pr create` (it therefore
requires `--push`) and never merges — merging stays a human/CI decision.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Every executed check passed; the commit chain, push, and PR ran or were intentionally skipped (`--dry-run` always exits 0) |
| 1 | The first failing battery check, a failed commit, or a failed push/PR — the run stops there and prints the failing output tail |
| 2 | Usage error (argparse), e.g. `--pr` without `--push` |

## Worked examples

Reports-only edit (one commit, no control tail):

```bash
python3 code/orchestrators/settle.py --tier fast \
  --commit-message "Refresh reconciliation notes for September"
```

Data intake that touched `data/` and dated reports (tier auto-raises to
`full`, two commits, pushed):

```bash
# after docs/operations/publication-sync.md intake + regeneration
python3 code/orchestrators/settle.py \
  --commit-message "September publication intake" --push
```

Code change landed, then release-confirmed:

```bash
python3 code/orchestrators/settle.py --tier full --commit-message "Harden sitemap renderer"
python3 code/orchestrators/settle.py --tier release --skip-commit --push
```

## How this replaces the manual sequence

The old rhythm was hand-run and drift-prone: payload commit, control-tail
commit, then the three validation commands from
[`AGENT_START.md`](../../AGENT_START.md) run one at a time, and a push that
skipped a gate was indistinguishable from one that passed them. Settle makes
the order mechanical and the failure point explicit. It is still bounded: the
full release ceremony — regeneration double-run, artifact size and manifest
checks, browser evidence, live verification, and the deployment attestation —
remains governed by the ordered release gate in
[`docs/operations/release-integrity.md`](release-integrity.md), and upstream
publication intake stays a deliberate manual step per
[`docs/operations/publication-sync.md`](publication-sync.md). Settle covers
the *landing* half: verify the tree, split the commits, hand the branch to
push/PR.

## Notes

- The budget gate lives at `code/src/artifact_budget.py` and takes no flags
  (`main()` enforces the 880 MiB budget from the newest
  `reports/pages_artifact_growth_*.json`); settle runs it without `--check`.
- The release step binds `--deployment-attestation
  reports/deployment-attestations/<HEAD>.json` when that conventional receipt
  exists; `validate_repo.py --release` cannot pass without an attestation,
  which settle's CLI has no flag to supply.
- `--commit-message` sets the payload message only; the control-tail commit is
- Battery commands run with `uv run --no-sync` (the lint step uses
  `uv run --group lint` instead) so settling rarely mutates the lockfile
  environment mid-run.
- **Binder ordering (land-then-confirm cycle):** regenerate the binder chain
  only *after* the payload commit — the Pages manifest binds
  `source_commit_at_generation` to the commit that last changed Pages payload
  content, so a pre-commit render goes stale the moment the payload lands.
  Render binders only after dated receipts are *tracked*:
  `build_agent_index.py` resolves receipt paths among tracked files, so a
  receipt that exists only untracked is invisible to the render. Chain order
  is dependency order: `build_pages_artifact.py --write-manifest` first (it
  binds the payload commit and produces the growth receipt; on a dirty tree
  it fails closed with "dirty post-deploy Pages inputs" unless the only dirty
  input is a current pre-payload public-source snapshot receipt recording
  `source_worktree_clean: false`, permitted via
  `--allow-dirty-prepayload-evidence` — see `build_pages_artifact.py`
  :105-114 and :172-186) → `build_generated_manifest.py` →
  `build_agent_index.py` → `build_release_integrity.py` → a final
  `build_generated_manifest.py` pass (the canonical chain in
  `code/src/generation_plan.py` ends on it) — re-run `sync_site_facts.py`/
  `build_catalog.py` first if the new receipts change their rendered links.
  `build_public_source_review.py` stays a deliberate manual render (excluded
  from the local chain) and embeds digests of the dated evidence receipts,
  not the binder outputs. Commit any payload churn from the consumer renders, then
  re-render the manifest once against that final payload commit — after the
  receipt *paths* are stable only the manifest and growth receipt churn, and
  the downstream binders are byte-stable. Then confirm with
  `settle.py --tier full --skip-commit` on the clean tree before pushing.
  Post-deploy: commit the live-site receipt *together with* its binder
  rebind — a receipt-only push re-stales the binders and turns main CI red
  until the rebind lands.