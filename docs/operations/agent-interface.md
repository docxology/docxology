# Agent maintenance inspection

Run from the repository root with the pinned Python environment:

```bash
uv run python3 code/orchestrators/agent.py status --json
uv run python3 code/orchestrators/agent.py plan --json
uv run python3 code/orchestrators/agent.py plan --step catalog --json
```

The interface is offline and previews commands without executing them. `plan`
derives stable step IDs, ordered write/check argument arrays, effective cache
inputs, Git index dependencies, and excluded network/manual operations from
[`generation_plan.py`](../../code/src/generation_plan.py). Existing scripts and
their flags remain the execution interface; this adds no second command list.
Argument arrays are data: do not interpolate them into a shell string.

`status` reports the observed local HEAD, branch, checkout cleanliness, runtime
pin, installed package versions, and plan-coverage errors. It uses Git without
optional index-refresh locks. It does not fetch refs, compare a remote HEAD, run
validation, find a browser executable, inspect account access, deploy, or record
human approval. A clean tree is an observation, never a passing release gate.
A missing or timed-out Git reader is explicitly unavailable, never clean.

JSON responses use `schema_version: "1.0"` and `ok`; failures include `errors`.
`plan.steps` is an ordered array with `id`, `description`, `write_argv`,
`check_argv`, `cache_inputs`, `cache_exclusions`, `git_index_inputs`, and
`always_run`. `status` keeps `validation: "not_run"`,
`network_freshness: "not_checked"`, `deployment: "not_checked"`, and
`human_visual_review: "not_attested"` explicit. Dirty work in progress does not
make inspection fail. Unknown step IDs, writer flags, and unknown operations
are rejected; there is no arbitrary command-execution endpoint.

| Exit | Meaning |
| --- | --- |
| 0 | Requested inspection completed; no execution or release approval implied |
| 1 | Observation or generation-plan coverage failed |
| 2 | Invalid command, step ID, or arguments |

Use [`AGENT_START.md`](../../AGENT_START.md) for task routing,
[`GENERATED.md`](../../GENERATED.md) for output ownership, and
[`regeneration.md`](regeneration.md) for rebuild semantics. Edit sources on a
work branch, rebuild their projections, and follow [`settle.md`](settle.md).
Within a managed GitVault, repository edits, staging, generation, commits, and
pushes also require its enclosing operation lock and migration guard. Hold that
guard for finite commands and yield between independently reviewable batches.
Never stop another transfer or delete a lock to obtain admission.

Post-deploy technical acceptance and human release review remain separate. Keep
candidate-SHA diagnostics outside source artifacts when they are not being
adopted as reviewed evidence; a receipt-only push still needs its binder rebind.
