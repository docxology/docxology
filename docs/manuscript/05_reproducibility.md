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

For interactive changes, install the `browser-qa` extra and Chromium, then set `DOCXOLOGY_REQUIRE_BROWSER_QA=1` for required acceptance as documented in [site-runtime.md](../operations/site-runtime.md). Missing optional tooling in an ordinary local test run can produce skips; those skips do not establish browser behavior.

## Candidate and evidence recording

Record the tested commit, exact command, runtime, exit status, and receipt scope. Preserve earlier failed observations when a focused correction or recheck is needed. Keep local tests, hosted CI, deployed byte/route checks, and human review distinguishable. Publication verification must compare the final local commit with the remote and bind deployed checks to that candidate.

## Manuscript reproducibility

`validate_manuscript.py` is read-only and can inspect a disposable fixture with `--root PATH`. Its JSON states that rendering and publication-readiness assessment were not performed. The current draft has no token producer or figure-rendering pipeline. A future renderer must have a declared reproducible command and inspected outputs before the draft can claim successful rendering.
