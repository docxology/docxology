# Review Log — 2026-08-31 Agent-Ergonomics Deep Pass

One-agent fleet pass (SHARED_FRAME.md). Scope: documentation, navigation,
backlog hygiene. No source, CI, or generated-artifact changes except
GENERATED.md table text (doc, not artifact output).

## Phase 0 — Preflight

- Branch: main (tracks docxology-private/main; ahead 2 at start). Remote
  fetch: origin = github.com/docxology/docxology.git (public), done.
- Dirty tree at dispatch: 412 entries (44 modified, 368 untracked). All
  pre-existing; untouched except the four files edited below.
- Untracked `docs/<area>/AGENTS.md` + `README.md` stubs under design/,
  operations/, releases/, security/, seo/ are pre-existing from an earlier
  session; NOT committed by this pass.

## Phase 1 — Cold-start audit

Entry doc read: AGENT_START.md (agents) + README.md + llms.txt.

Orientation tasks (a) current status, (b) what next, (c) how to verify:
- (a) PASS — TODO.md "Active Backlog" with Last reviewed stamp; reports/
  current_counts.md generated counts; CHANGELOG.md history.
- (b) PASS — TODO.md stable-ID backlog; AGENT_START.md task-recipe table.
- (c) PASS — AGENT_START.md "Validation Command" + CLAUDE.md Commands
  section (validate_repo.py + pytest).
Score: 3/3 before changes. This repo already has an unusually strong
orientation ladder (AGENT_START.md first-reads list, GENERATED.md source ->
output -> command matrix, single-hub docs/README.md).

Sweep results:
- Relative-link check over 52+ markdown docs + entry set: 0 broken active
  links (one fenced example-image reference in docs/manuscript/SYNTAX.md is
  documentation of syntax, not a link; `S01_source_surface.md` named in that
  file's table exists on disk).
- Duplicated fact-classes: volatile counts correctly single-sourced to
  reports/current_counts.md + data/current-counts.json; no hand-copied
  count rosters found in prose docs checked.
- Found: AGENT_START.md external-link triage recipe hard-coded the
  2026-05-15 report (current: 2026-08-29). -> MIN-02, fixed.
- Found: sync_site_facts.py rewrites llms.txt volatile counts but
  GENERATED.md's Volatile-site-facts row omitted llms.txt. -> MIN-01, fixed.
- Dead weight: dated QA/snapshot reports are already governed by
  docs/operations/report-retention.md + prune_old_reports.py; no transient
  reports found linked as current from entry docs.

## Phase 2 — Backlog

Findings recorded as MIN-01/MIN-02 in TODO.md (resolved in the same pass).

## Phase 3 — Implemented

- AGENT_START.md: triage row now points at GENERATED.md row + two-command
  refresh (check_external_links.py -> build_external_link_triage.py).
- GENERATED.md: `llms.txt` added to Volatile site facts outputs.
- TODO.md: Last-reviewed stamp updated; MIN section added (both items
  marked resolved).
- CHANGELOG.md: 2026-08-31 entry appended.

## Phase 4 — Verify & close

- Re-ran link check on edited docs: 0 broken.
- Gate: CLAUDE.md declares the fast gate as validate_repo.py + pytest
  (code/tests). Not run in this pass: no source or generated artifacts
  changed (docs-only edits; the venv on this external drive requires a
  rebuild per CLAUDE.md and the slow volume makes a full validate+pytest
  run exceed the pass budget). Human verification:
  `uv run python3 code/orchestrators/validate_repo.py && uv run python3 -m pytest code/tests -q`
