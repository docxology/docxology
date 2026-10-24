# Research exploration tools

The site provides [reading lists](../../collections.html),
[research trails](../../trails.html), a [research map](../../research-map.html),
and a [probability laboratory](../../lab.html). These static features require
no account, third-party script or remote computation.

## Sources and generation

`build_research_tools.py` owns the four pages and
`data/collection-catalog.json`, `data/research-map.json`, and
`data/research-trails.json`. Its write/check commands are registered in
`code/src/generation_plan.py`, after works/video exports and before security
normalization and discovery. Follow [development.md](development.md) and
[settle.md](settle.md) for regeneration and landing.

The collection catalog reuses exact BibTeX entries and the bibliography's RIS
and CSL renderers, including reviewed editor roles. Selected exports preserve
reading order. The browser does not infer missing citation metadata.

Curate trails in `data/research-trails-source.json`. Work keys, video routes and
software URLs must resolve in their authoritative catalogs; unknown resources
fail generation. Learning goals and first-pass time estimates are editorial
navigation aids, not research findings or measured completion times.

`research_connections.py` ranks exact recorded method/keyword phrases,
distinguishing contributors with their recorded roles and explicit software associations. Contributors appearing
on more than half of the catalog do not distinguish recommendations. Domain-only
fallbacks are labelled; known canonical aliases and equal DOIs cannot recommend
one another. Metadata overlap is not a citation or scientific equivalence.

The map records work/domain, byline and explicit associated-software edges with
provenance. Exact normalized author names group nodes; homonyms may be grouped
and variants remain separate. The diagram displays at most twelve neighbors,
while the paginated list and JSON preserve the complete graph.

## Visitor state

Publication URL parameters are `q`, `type`, `domain`, `year`, `venue`, `doi=1`,
`docs=1`, `sort` and `dir=desc`. Typing replaces the current history entry;
discrete changes add entries. Back/Forward restore the controls. Invalid values
are reported and normalized. Collecting includes the complete matching set,
including works beyond the visible fifty-row batch.

Reading lists use `localStorage` key `docxology.reading-lists.v1`: version 1,
an active list ID, and ordered named lists. Limits are twenty lists, five hundred
unique keys per list, and 1 MB per backup. Storage failures preserve a session
draft with a visible warning. Unreadable original bytes have a separate recovery
download; ordinary backups still export the usable draft. Cross-tab changes stop
writes instead of overwriting another tab. List deletion provides undo.

Shared fragments contain `v=1`, `title` and comma-separated `works` keys. They
open previews and never write saved lists until **Save shared list** is selected.
Imports also preview a new list. Unavailable keys remain visible and block
citation export instead of silently disappearing. Shared links expose their
public keys and title to recipients; edits do not synchronize. Browser storage
can be cleared or evicted, so backups remain useful.

## Teaching models

The binary model implements Bayes' rule for two exhaustive hypotheses with
fixed likelihoods and conditionally independent observations. Log weights avoid
underflow. Impossible evidence fails without changing the accepted history;
one hundred observations bound a run. Prior 0.20 and likelihoods 0.80/0.20 give
posterior 0.50 after E and 0.20 after a subsequent not-E.

The urn draws proportional to current counts, replaces the token and adds the
chosen nonnegative reinforcement. Mulberry32 fixes the seeded 32-bit sequence,
including seed zero. CSV exports include initial conditions, seed and every
step. This is a teaching process, not a calibrated account of cognition, ant
colonies, physiology or pheromone dynamics. The page links model definitions
separately from related research and its evidence boundaries.

## Verification

`test_research_tools.py` checks closed-form numerical oracles, impossible inputs,
seed vectors, count conservation, citation identity/roles, relationship negative
controls, trail identities and generated-output safety.
`test_research_tools_browser.py` checks URLs/history, saved order and downloads,
preview/import boundaries, storage/network failures, graph completeness, CSV,
no-JavaScript content, narrow/enlarged-text layouts, keyboard access and axe.

```bash
uv run python3 -m pytest code/tests/test_research_tools.py code/tests/test_research_tools_browser.py -q
uv run python3 code/orchestrators/build_research_tools.py --check
```

Use the complete-suite prerequisites in [development.md](development.md).
Automated browser checks and screenshots are separate from human visual review.
The four exploration pages also run in the Lighthouse suite at performance 85,
accessibility 95 and SEO 95 floors. Established lane floors remain unchanged.
The asset audit bounds each exploration script and its stylesheet at 50 KB.
