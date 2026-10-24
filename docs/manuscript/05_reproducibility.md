# Reproducibility {#sec:reproducibility}

## Local runtime and commands

Run from the repository root using the declared [Python project](../../pyproject.toml) and [dependency lock](../../uv.lock). Read [AGENT_START.md](../../AGENT_START.md) and nearer instructions before mutating sources. These inspection commands do not regenerate public artifacts:

```bash
uv run python3 code/orchestrators/regenerate_all.py --list
uv run python3 code/orchestrators/validate_manuscript.py --json
uv run --group lint ruff check code
```

After an authorized source edit, rebuild the declared projections and check the repository:

```bash
uv run python3 code/orchestrators/regenerate_all.py --validate
uv run python3 -m pytest code/tests -q
```

Regeneration writes checked-in outputs. Standard validation includes cached evidence and freshness gates, so a failing gate must be diagnosed rather than treated as permission to rewrite its evidence. Source refreshes and clean payload/control-binder landing are documented in [evidence-refresh.md](../operations/evidence-refresh.md) and [settle.md](../operations/settle.md).

For interactive changes, install the `browser-qa` extra and Chromium and select the browser marker as documented in [site-runtime.md](../operations/site-runtime.md). Selected tests require their declared tooling locally and in CI; a skipped selected test fails the run. Explicitly deselected tests remain outside that run's evidence. The complete collection also requires the pinned native rendering inputs in the [rendering guide](README.md).

## Package and browser isolation

The [checkout-local package guide](../../code/src/README.md) defines the canonical import surface and compatibility boundary. Real subprocess tests cover both import orders and cross-form exception catching, including a minimal checkout. Registry coverage checks prevent a new shared module from silently escaping that contract.

The [accessibility fixture](../../code/tests/test_accessibility_refinements.py) reuses a browser process within its module while creating a fresh context for every test. Storage, cookies, pages and service-worker state remain isolated. The runtime capability probe completes before the persistent synchronous browser driver starts. Performance measurements remain a separate serial test selection.

A surrounding admission wrapper can select its own Python environment. Bind the child command to this checkout's environment and verify both interpreter prefixes before source work, as described in the [development guide](../operations/development.md). Installed tools, a successful import and a qualified runtime remain different observations.

## Replay inputs

Record the citation-catalog version and source bytes alongside an exported reading selection when exact later replay matters. Shared keys can become unavailable after a catalog change, and browser storage can be cleared. Mathematical replay records assumptions, initial conditions, seed, implementation bytes and the exported trace. Reproducing a trace does not independently validate the model's scientific interpretation.

## Candidate and evidence recording

Record the tested commit, exact command, runtime, exit status, and receipt scope. Preserve earlier failed observations when a focused correction or recheck is needed. Keep local tests, hosted CI, deployed byte/route checks, and human review distinguishable. Publication verification must compare the final local commit with the remote and bind deployed checks to that candidate.

![The release path binds a reviewed payload, converged control metadata, automated acceptance, and separate human review to a candidate revision.](../output/figures/release-path.png){#fig:release_path}

## Manuscript reproducibility

`validate_manuscript.py` is read-only and can inspect a disposable fixture with `--root PATH`. Its JSON states that rendering and publication-readiness assessment were not performed. The pinned manual renderer and its command are documented in [the manuscript guide](README.md). Its receipt binds source, tool, and output hashes; it does not grant human or editorial approval. No generated-value token producer is declared. The cover and body diagrams have explicit offline producers whose source, runtime, and generated assets are bound in the render receipt.

## Manuscript rendering inputs

The [rendering guide](README.md) declares the native template revision and tools,
an explicit external dependency interpreter, staged transformations, and a
deterministic vector cover and registered body diagrams. The receipt binds these inputs and output hashes.
The template checkout may contain unrelated work: only the pinned committed
export is executed. Native PDF rendering is an explicit review operation and
does not run as part of site regeneration.
