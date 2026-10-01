---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "The Line Set: Holding Instruments Apart"
description: "A thin reader that declares what a set of small evaluative instruments is, reads whichever sibling packages are installed, and checks one narrow property: that no two of them have given the same spelling to different things. It adds no instrument of ..."
tags: ["modularity", "information-hiding", "separation-of-concerns", "boundary-objects", "namespace-collision", "declarative-registry", "reproducible-review", "open-science"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *The Line Set: Holding Instruments Apart*. Zenodo."
doi: "10.5281/zenodo.21754243"
---

# The Line Set: Holding Instruments Apart

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: modularity, information hiding, separation of concerns, boundary objects.

## Methods

Primary methods and techniques applied in this work:

- **Declarative set registry: four LineEntry records plus one shared token** — Declares the set (Red, Black, Golden, White Line) as data, each entry naming its question, job, and what it must not become.
- **Five-stage reader with fixed-precedence set statuses** — Reads installed sibling packages through resolve, bind, collide, declare and status stages, returning one of four SET_-prefixed readings.
- **Enum-member name collision check across sibling package roots** — Collects enum member names each line publishes at its package root and flags any name carried by more than one line, unless declared and disambiguated.
- **Seven offline structural checks plus a self-application check** — Runs seven declaration-only checks and an eighth that applies the package's own collision check to a declaration including itself.
- **Executed extensibility example appending a fifth colour at runtime** — Appends a hypothetical green_line entry without editing the package and runs the battery and reader on the extended declaration.

## Key Findings

Core contributions and results:

- On the review date the four packages yielded 81 line-and-name pairs spanning 80 distinct names, and the only shared name was the already-declared, disambiguated one.
- The single shared name was OUTSIDE_SCOPE, carried by red_line and black_line.
- Appending a fifth line whose package is not installed yielded SET_PARTIAL, which the author argues is the correct answer rather than a shortfall.
- The author stresses that disjoint vocabularies are a necessary, not sufficient, condition: the check cannot detect conceptual overlap between instruments.
- The paper states the set digest is a comparison handle only, not tamper evidence or a record of who changed what.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21754243
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-08-02T15:11:27Z

## Prerequisites

- Familiarity with modularity, information hiding, separation of concerns
- Background in Computational fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21754243`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
