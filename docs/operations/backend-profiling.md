# Backend performance diagnostics

Use Python 3.15 through the locked uv environment. The command measures two
fixed, read-only workloads: the complete local SEO invariant audit (`seo`) and
all declared cached-step source fingerprints (`fingerprints`). Workload choices
come from one registry in `code/src/backend_profiling.py`; fingerprint steps come
from the existing generation plan. No source intake, writer, network call,
commit, deployment, or release attestation runs.

```bash
uv sync --locked --all-extras --group lint
uv run python3 code/orchestrators/profile_backend.py seo --repeats 3 \
  --output /tmp/docxology-seo-timing.json
uv run python3 code/orchestrators/profile_backend.py seo --mode tracing --repeats 1 \
  --output /tmp/docxology-seo-trace.json
uv run python3 code/orchestrators/profile_backend.py fingerprints --repeats 3
```

Choose a new external output filename for each capture. Existing files are never
replaced, and paths resolving into the checkout are rejected. Stdout always
contains versioned JSON; exit 0 means a stable diagnostic completed, 1 means a
failed/unavailable observation, and argparse usage errors exit 2. A timeout
invalidates the run instead of emitting a partial success.

Each sample runs in a fresh process using the current interpreter, with closed
stdin, bytecode writes disabled, and optional Git locks disabled. Repeats are
bounded to 1–10; `--timeout` is 1–600 seconds per sample (default 180), including
source capture. The fixed worker never accepts arbitrary commands, modules or
input paths. Run it while repository sources are quiescent, under the normal
repository coordination guard if another operation could edit the checkout.

Before and after each workload, context capture hashes Git-visible names and
file bytes, HEAD, and cached-index path membership. It rejects unavailable,
linked or changing source files. Runtime, installed workload package versions,
platform, machine and CPU count accompany the sample. Context capture is outside
the measured interval. Differing source/runtime/result bindings across samples
fail the capture; identical bindings are necessary, but do not eliminate OS
cache, background-load or thermal effects. Run paired comparisons serially on
the same machine, preserve individual unprofiled samples, and describe their
scope. Across revisions, inspect the intentional source changes and unchanged
input workload rather than treating different source hashes as equivalent.

Timing mode reports elapsed workload seconds. Tracing mode uses Python 3.15's
[`profiling.tracing.Profile`](https://docs.python.org/3.15/library/profiling.tracing.html)
and exports the 30 largest cumulative-time entries as plain JSON with call
counts, self time and cumulative time. Tracing adds overhead; compare unprofiled
timings separately. The command never loads pickle or external profiler binaries.
Runtime and source binding do not certify semantic correctness: run the focused
regressions, full suite, generated-data checks and required browser gates.

[`profiling.sampling`](https://docs.python.org/3.15/library/profiling.sampling.html)
can require process-memory access. The bounded local sampling attempt on macOS
was unavailable because permission was denied. This command reports sampling as
`not_run`; it does not elevate privileges, change OS protections, or silently
substitute a sampling claim. Tracing remains available without that access.

## Measured optimization scope

The initial paired prototype comparison used Python 3.15.0 and the same locked
dependencies and unchanged input tree at commit
`b5e42ebe7cfe8ed637db723003e32f51daa00cfc`. Baseline and candidate implementations
were loaded against that same tree, with three serial samples per workload.
The Ruff/runtime configuration migration and the profiling CLI were validated
separately from these timing samples.

| Workload | Baseline seconds | Optimized seconds | Median change |
| --- | --- | --- | --- |
| SEO audit | 24.7183, 22.3492, 21.5869 | 8.5364, 5.5865, 5.5718 | 22.3492 → 5.5865 (75.0% lower) |
| Declared-step fingerprints | 19.9431, 17.4849, 15.7696 | 14.0601, 13.5482, 16.8191 | 17.4849 → 14.0601 (19.6% lower) |

All six SEO results hashed to
`4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`
(the empty error list); all six fingerprint mappings hashed to
`d5e259609b0867c4a724c91d9ee03639f2491066ca717b9e6828d0a6fe18869f`.
These measurements describe this tree and machine, not universal speedups or
hosted page performance. Initial overlapping discovery captures and a failed
source-overlay attempt were excluded from the comparison.

The optimizations avoid parsing long HTML bodies after the real head boundary,
retain a bounded cache large enough for the current page sweep, screen obvious
non-redirect documents before parsing, and index Git-visible paper names once
per snapshot. Cached HTML versions include device, inode, size, mtime and ctime;
fresh reads recheck the version. Paper contents and link safety are checked
again on every load. Fingerprinting keeps its byte format while calculating
relative names once. Regeneration shares its pre-writer fingerprint with the
skip decision and still hashes independently after a successful writer; cache
misses therefore avoid a redundant full pre-writer hash. No per-file digest
memoization or release validation shortcut was added.
