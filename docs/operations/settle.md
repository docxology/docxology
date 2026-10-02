# Settle driver

`code/orchestrators/settle.py` is the one-command way to finish a change: it
classifies the dirty paths, replays the existing public-source review when
landing changes, runs the tiered check battery (stopping at the
first failure), lands scoped payload and control-tail commits, and validates
the landed tree before an optional push. It
replaces the manual rhythm of *payload commit, control-tail commit, then the
gate cascade by hand* with a single driver whose exit code answers one
question: is this work safe to push?

```bash
python3 code/orchestrators/settle.py [--tier fast|routine|full|release] [--dry-run] \
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
| `routine` | fast battery + `validate_repo.py` (standard) — control-only landings and clean-tree checks only; any payload-dirty path auto-raises the tier to `full` | seconds for control-only/clean trees — no pytest ever; payload work never reaches this battery (fail-closed) |
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

`routine` is the deliberate lighter contract for **control-only landings and
clean-tree checks** ("is everything consistent right now?"): the fast floor
plus standard validation and no pytest. Binder refreshes belong to the
landing phase and also run for pending control changes. The raise rule is a
correctness rule, not a convenience rule: **any payload-dirty path — `data/`,
`code/`, `docs/`, `papers/`, `pages/`, dated receipts — raises the tier to
`full` before the battery runs**, because every payload commit moves the
payload anchor that the Pages deploy re-validates (`build_pages_artifact.py
--check-manifest` in the pages.yml deploy job): a payload commit without a
fresh binder manifest turns the deploy red. Leftover/unclassified paths count
as payload for this rule (fail-closed). What routine gives up vs `full`:

1. **No pytest.** routine's battery is exactly the fast floor plus standard
   validation — reachable only when the tree is payload-clean or
   control-only-dirty, where the test suite cannot be affected by the
   landing's own content. A payload change rides `full` and pays for the
   suite there.
2. **No release step.** `--tier release` still extends the *full* battery,
   never routine's; the release gate is unaffected.

## Effective tier

`--tier` is a floor, not a switch. Every run first classifies the dirty paths
(`git status --porcelain`, then `classify_paths` from
`code/src/change_classifier.py`) and raises the tier when the paths demand it:
`fast < routine < full < release`. The driver
prints a decision line such as
`tier decision: requested=fast path-derived=full -> effective=full` and runs
the stronger battery.

Two raise classes exist. The **convenience raises** (path-derived tiers for
reports/docs edits) stay ignored for routine. The **payload raise** is
honored and printed with its reason:
`tier decision: requested=routine path-derived=none -> effective=full (payload paths dirty: raised to full — the Pages deploy re-checks the binder manifest, which any payload commit stales)`.
A control-only tree prints
`tier decision: requested=routine path-derived=full -> effective=routine (routine: control-only or clean tree)`.

Which tier to reach for:

1. **Unsure?** Start with `--dry-run`: it prints the classification, the
   effective tier, the exact battery commands, the planned commits, and the
   push/PR plan without executing anything.
2. **Reports/docs-only edits** validate as `fast`, but they are still
   payload commits: every payload commit moves the payload anchor the
   Pages deploy re-validates, so the landing needs the binder rebind. Land
   them with `--tier full` (or ride routine, which raises automatically).
3. **Routine ops that change payload** (paper updates, catalog fixes,
   release-pair intake) raise to `full` automatically — do not fight the
   raise; it is the deploy contract. Use `--tier routine` for control-only
   receipts (binder tails, PSR re-renders) and for the clean-tree
   consistency check. `--dry-run` shows the raise reason before anything
   executes.
4. **Data intake and generated surfaces** (`data/`, `works/`, `papers/`,
   `pages/`, `feeds/`, sitemap) classify as `full` — any surface beyond
   reports/docs raises the tier, so an intake touching `data/` plus its dated
   reports lands at `full` even if you asked for `fast`.
5. **Code changes under `code/`** classify as `full` — the classifier never
   derives `release` from paths, so `release` is strictly opt-in via
   `--tier release`; treat `full` as the landing tier for ordinary code work.
6. **Release confirmation** uses `--tier release`. The added
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
driver uses this sequence on the current branch:

1. **Payload commit** — stage the classified payload paths, then use
   `git commit --only -- <paths>` with `--commit-message` (default:
   `Settle pending payload changes`). Other previously staged paths stay
   staged. Rename sources and destinations are included; staged and
   unstaged deletions and literal wildcard filenames are supported.
2. **Binder convergence** — for a payload landing or pending control paths,
   run public-source review → Pages manifest → generated manifest → agent index → release integrity
   → final generated manifest. Stage recognized control outputs after every
   writer so index-tracked receipt discovery sees new reports. Repeat until
   the controls are byte-stable, with a four-pass bound, then run binder
   checks. Payload drift aborts instead of entering an extra automatic commit.
3. **Control-tail commit** — discover the current control paths, including
   new growth receipts, and commit only those paths, with the same
   message plus the ` (control tail)` suffix, per the CONTROL_FILES
   semantics the classifier encodes.
4. **Post-landing validation** — require a clean worktree, check the Pages
   manifest against the landed payload commit, and run standard validation.
   These checks must pass before push or PR creation. They use local sources
   and existing evidence receipts; they do not refresh remote evidence.

A phase with an empty path set is skipped with a signpost line. Paths the
classifier assigns to neither group are left uncommitted and reported, so a
stray file cannot vanish into a commit silently. Work on a branch: settle
commits wherever you are, and committing on local `main` is a known failure
mode (see the Source-Of-Truth rules in `AGENT_START.md`).

If the battery observes concurrent payload changes, settle preserves them
and aborts before committing. Binder failure, non-convergence, unexpected
payload changes, and post-landing validation failure leave reviewable local
changes/commits and prevent push. No reset or automatic rollback occurs.

The preflight review replay is required because standard validation checks
the report's dirty-worktree provenance as well as its payload anchor. Both
preflight and post-payload replay preserve the existing report's date, all
recorded input paths, comparison baseline, and pairing-refresh context. A
missing report, absent optional input, changed input schema, or input outside
tracked local `data/`/`reports/` JSON stops settle before replay. Resolve those
cases through the explicit public-source review workflow.
Inputs, output JSON/Markdown, and their temporary siblings must be regular
files with one hard link and no symlink ancestors; missing output files are
allowed. These custody checks run before reads/replay, including aliases to
ignored private files inside the checkout. Staging and convergence snapshots
use the same custody boundary.

`--push` runs `git push -u origin HEAD` after post-landing validation.
`--skip-commit --push` also requires a clean tree and post-landing validation;
`--skip-commit` alone executes only the battery and writes no binders.
`--pr TITLE` then creates a pull request with `gh pr create` (it therefore
requires `--push`) and never merges — merging stays a human/CI decision.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Every executed check passed; the commit chain, push, and PR ran or were intentionally skipped (`--dry-run` always exits 0) |
| 1 | A failing check, commit, binder convergence, concurrent-edit guard, or push/PR — the run stops there with diagnostics |
| 2 | Usage error (argparse), e.g. `--pr` without `--push` |

## Worked examples

Reports-only payload edit (payload, binder refresh, control tail):

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
- `--commit-message` sets the payload message; the control tail appends
  ` (control tail)`.
- Battery commands run with `uv run --no-sync` (the lint step uses
  `uv run --group lint` instead) so settling rarely mutates the lockfile
  environment mid-run.
- **Binder ordering (land-then-confirm cycle):** settle implements the
  bounded control chain described above after the payload commit. A
  pre-commit manifest becomes stale as soon as payload lands. New receipts
  must be index-tracked before dependent renderers run. The agent index can
  retire an old report pointer, which changes Pages report retention on the
  next pass; convergence therefore includes the Pages manifest, generated
  manifest, agent index, release envelope, and dated control receipts.
  Four passes are a bound, not permission to publish non-convergent output.
  Settle prints the changing control paths and aborts if they remain unstable.
  Source consumers such as `sync_site_facts.py`, `build_catalog.py`,
  `build_search_index.py`, and git-date-dependent `build_sitemap.py` remain
  deliberate payload renders. If post-landing validation reports those stale,
  regenerate the named consumers, review and land their payload changes,
  then rerun settle; it will not automatically commit unrelated payload
  churn. Staging dated receipts before their initial consumer render can fold
  those pointer changes into the original payload commit (see
  [`publication-sync.md`](publication-sync.md)).
  Initial source-review creation and changes to its baseline/input set remain
  manual. Settle calls `build_public_source_review.py` only to replay the
  existing report with every recorded input supplied explicitly, preserving
  its date, previous snapshot, decision-ledger paths, refresh status, and note.
  Post-deploy: commit the live-site receipt *together with* its binder
  rebind — a receipt-only push re-stales the binders and turns main CI red
  until the rebind lands.
- **Routine tier and the binder chain:** a control-only landing preserves
  the payload anchor but can still alter receipt discovery and report
  retention, so settle runs the bounded binder cycle for pending controls.
  A clean-tree routine check runs no binder writers. Payload changes raise
  routine to `full`, including the pytest gate.
- **Local regeneration:** `regenerate_all.py` runs two ordered passes by
  default to refresh consumers of late-produced counts/software, work
  enrichment, and paper-folder flags. Use `--validate` to check the result;
  `--passes 1` is a diagnostic override, not a convergence guarantee. Binder
  convergence after landing is separate from those pre-commit local passes.
