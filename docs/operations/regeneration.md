# Local regeneration

[`regenerate_all.py`](../../code/orchestrators/regenerate_all.py) is the single
write-mode coordinator for locally derived artifacts.
[`generation_plan.py`](../../code/src/generation_plan.py) declares each writer,
its inputs, its exact no-write check, and the deliberate network or manual
exclusions. The driver executes this shared plan in order; it does not perform
source intake, fetch new evidence, or publish a release.

```bash
# Inspect the ordered plan without running writers or updating cache state.
uv run python3 code/orchestrators/regenerate_all.py --list

# Run two local passes, then the authoritative repository validation battery.
uv run python3 code/orchestrators/regenerate_all.py --validate

# Ignore cached input fingerprints and run every step in both passes.
uv run python3 code/orchestrators/regenerate_all.py --force

# A single pass is useful for diagnosis, but does not establish convergence.
uv run python3 code/orchestrators/regenerate_all.py --passes 1
```

Two ordered passes refresh consumers of late-produced counts, enrichment, and
folder metadata. `--passes` accepts one through four. A failed writer stops the
chain immediately, so later passes and optional validation cannot present a
partial render as successful. Two passes address the known dependencies;
`validate_repo.py` remains the authority for stale outputs.

## Single-writer contract

Before reading cache state or launching a writer, the driver acquires a
nonblocking POSIX `flock` on `.docxology/regeneration.lock`. A second coordinated
run against the same repository fails immediately with `another regeneration
is active`, before it can change outputs or cache state. The lock covers all
ordered passes and the CLI's optional validation. The one-pass and multi-pass
Python APIs enforce the same guard without acquiring it recursively.

The private directory is ignored by Git and excluded from public artifacts.
The lock file has mode `0600`; directory and file symlinks and shared hardlinks
are rejected. The file stays in place after a run. Its existence does not mean
a run is active: the kernel releases the lock when its last descriptor closes,
including after exceptions or process termination. Never delete a lock file to
clear a suspected stale run; that can let processes lock different inodes and
write concurrently. Wait for the active process to finish instead.

Default writer children inherit the lock descriptor, keeping the guard active
if the driver is terminated while a launched writer still runs. The driver
fails closed on platforms without POSIX `flock` and safe file-open support;
macOS and Linux are supported. This is an advisory guard for coordinated runs,
not a lock against independent writer commands, source editing, or processes
that deliberately remove private bookkeeping. Custom Python runners must keep
their work synchronous or manage their own child-process lifetime.

## Cache contract

Steps with declared inputs may skip when their input bytes, writer, and shared
Python implementation match the previous successful run. Declared imported
orchestrator helpers also participate. Steps without inputs always run.
Modification times alone do not invalidate the cache.

The private bookkeeping file is `reports/regeneration-state.json`, which is
ignored by Git and excluded from the public artifact. Unsupported schema
versions, malformed fingerprints, missing files, and unreadable inputs cause a
cold run. Writes use an ignored temporary sibling and an atomic rename, so a
failed replacement preserves the prior file. A run that skips every step leaves
the file untouched. Before a writer runs, any old entry for it is removed from
the persisted cache. A failed or interrupted forced rebuild therefore cannot
leave a partial output eligible to skip. Successful entries are persisted only
after the whole pass finishes; a failed pass persists invalidations, not its
successful partial state.

The driver compares source fingerprints before and after each successful
writer. If a source changes, disappears, or first becomes available during the
write, it clears that step's cache entry so a later pass renders again. A changed
readable fingerprint emits `cache invalidated`. This detects observed changes;
it is not a filesystem snapshot or a lock against concurrent source edits.
Review source diffs and run the independent checks before landing.

The Python APIs `run_regeneration` and `run_regeneration_passes` accept a
`repo_root`, optional test runner, and message emitter. The default child process
and cache both use that repository root, so disposable fixtures cannot route
writers into the caller's checkout. The resume writer still uses the repository's
locked `uv` environment for reproducible PDF output. Other writers inherit the
driver's Python interpreter.

## Release boundary

Local rendering and cache freshness do not establish network freshness,
deployment, human visual review, or full release attestation. Follow
[publication-sync.md](publication-sync.md) for deliberate public-source refreshes
and [settle.md](settle.md) for publication. Land the reviewed payload before
converging its control binders from a clean tree; local pass counts do not replace
that separate release process. Regenerate the git-date-dependent sitemap after
committing when its `<lastmod>` needs to reflect the landed change.

Focused contract tests:

```bash
uv run python3 -m pytest code/tests/test_regenerate_all.py \
  code/tests/test_regeneration_contracts.py code/tests/test_regeneration_skips.py \
  code/tests/test_generation_cache_sources.py code/tests/test_generation_plan.py \
  code/tests/test_generation_plan_order.py code/tests/test_generation_plan_gating.py -q
```
