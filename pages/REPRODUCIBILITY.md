---
title: "REPRODUCIBILITY - Daniel Ari Friedman"
description: "Per-work reproducibility ledger scoring artifact availability across the curated bibliography."
keywords: "Daniel Ari Friedman, reproducibility, open science, verification, research artifacts"
---
<div align="center">

# Reproducibility Ledger

> **Navigation**: [🏠 Home](../README.md) | [🧾 Evidence](EVIDENCE.md) | [🧭 Discovery](DISCOVERY.md) | [📚 Bibliography](BIBLIOGRAPHY.md)

[Website version](../reproducibility.html) · [Ledger JSON](../data/reproducibility.json)

</div>

---

What a third party can check about each of 206 catalogued works without asking the author for anything.

This ledger scores **artifact availability, not correctness**. A work can hold a perfect
score and still be wrong; an important result published before persistent identifiers
existed can score low through no fault of its own. Values are computed from
`data/works.json` and `data/software.json` by
`code/orchestrators/build_reproducibility_ledger.py`; the build fails if this file drifts
from that computation.

## Signal coverage

| Signal | Works | Share | What it lets a reader do |
| --- | --- | --- | --- |
| Persistent identifier | 191 / 206 | 93% | Resolve a DOI instead of trusting a live URL. |
| Public archive | 149 / 206 | 72% | Fetch a deposited copy from a third-party archive. |
| Open full text | 171 / 206 | 83% | Read the full text without a paywall or request. |
| Source documents | 189 / 206 | 92% | Inspect the working folder behind the entry. |
| Executable code | 37 / 206 | 18% | Run the software that produced or accompanies it. |
| Agent-readable guidance | 189 / 206 | 92% | Parse structured guidance without scraping prose. |

Mean score 4.495 of 6.

## Bands

| Band | Works | Share | Meaning |
| --- | --- | --- | --- |
| independently reproducible | 140 | 68% | Code, archive, and text are all reachable without contacting the author. |
| independently checkable | 49 | 24% | Enough is public to confirm the record and read the argument. |
| citable only | 8 | 4% | The record resolves, but little beyond it is machine-checkable. |
| unverified | 9 | 4% | Nothing here is independently checkable from this site alone. |

## Weakest entries

Published deliberately. A ledger that only showed its strongest records would not be
evidence of anything.

| Work | Year | Score | Missing |
| --- | --- | --- | --- |
| [Active Inference Journal — 500+ videos on Active Inference with transcripts](../works/Friedman2026ActiveInferenceJournal500002.html) | 2026 | 0 / 6 | Persistent identifier, Public archive, Open full text, Source documents, Executable code, Agent-readable guidance |
| [Personal YouTube — 200+ livestreams: drawings, Synergetics, paper discussions](../works/Friedman2026PersonalYouTube200Livestreams006.html) | 2026 | 0 / 6 | Persistent identifier, Public archive, Open full text, Source documents, Executable code, Agent-readable guidance |
| [Innovator's Digital Playbook](../works/Friedman2021InnovatorSDigitalPlaybook078.html) | 2021 | 0 / 6 | Persistent identifier, Public archive, Open full text, Source documents, Executable code, Agent-readable guidance |
| [Communication for Remote Teams](../works/Friedman2020CommunicationRemoteTeams083.html) | 2020 | 0 / 6 | Persistent identifier, Public archive, Open full text, Source documents, Executable code, Agent-readable guidance |
| [How to use Keybase for remote teams](../works/Friedman2020HowUseKeybaseRemote087.html) | 2020 | 0 / 6 | Persistent identifier, Public archive, Open full text, Source documents, Executable code, Agent-readable guidance |
| [Lessons from the colony](../works/Friedman2016LessonsFromColony155.html) | 2016 | 0 / 6 | Persistent identifier, Public archive, Open full text, Source documents, Executable code, Agent-readable guidance |
| [Disinforge](../works/Friedman2021Disinforge157.html) | 2021 | 0 / 6 | Persistent identifier, Public archive, Open full text, Source documents, Executable code, Agent-readable guidance |
| [Osteopathy and the Variable Variability of Health](../works/Friedman2017OsteopathyVariableVariabilityHealth163.html) | 2017 | 0 / 6 | Persistent identifier, Public archive, Open full text, Source documents, Executable code, Agent-readable guidance |
| [Cells, Mechanobiology, and Osteopathy](../works/Friedman2016CellsMechanobiologyOsteopathy164.html) | 2016 | 0 / 6 | Persistent identifier, Public archive, Open full text, Source documents, Executable code, Agent-readable guidance |
| [Full speed ahead to the City on the Hill](../works/Friedman2016FullSpeedAheadCity156.html) | 2016 | 1 / 6 | Public archive, Open full text, Source documents, Executable code, Agent-readable guidance |
| [Defining events: 2020 in hindsight](../works/Friedman2021DefiningEvents2020Hindsight158.html) | 2021 | 1 / 6 | Public archive, Open full text, Source documents, Executable code, Agent-readable guidance |
| [Active Blockference: cadCAD with Active Inference for Cognitive Systems Modeling](../works/Friedman2022ActiveBlockferenceCadCADActive159.html) | 2022 | 1 / 6 | Public archive, Open full text, Source documents, Executable code, Agent-readable guidance |

## Maintenance

- Regenerate with `uv run python3 code/orchestrators/build_reproducibility_ledger.py`.
- Verify without writing using `--check`; `validate_repo.py` runs that check.
- Raising a score means shipping the missing artifact, never editing this file.
