# FractiSkills: One Portable Agent Skill per Page

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22712650.svg)](https://doi.org/10.5281/zenodo.22712650)

---

## Abstract

FractiSkills treats an entire website as a corpus of agent skills: every reachable page is normalized into a SKILL.md-style artifact so that a whole site — not a single document — becomes loadable context for an agent. The work is organized around a four-stage pipeline — discover, render, publish, research — with Skillarum serving as the engine that turns raw crawl output into citable, receipt-bearing skill documents. Discovery unions the declared sitemap with a bounded, robots-respecting breadth-first crawl (reaching a maximum depth of 5), resolves redirect and canonical aliases, and partitions every page into site-derived sections; the render stage emits one receipt-bearing skill per page; publish and research then validate, organize, and measure the corpus. The resulting corpus covers 405 pages from 53 sitemap URLs, organized into 12 sections and 405 skills totaling 497896 words (3887524 characters). Augmentation — a declared, same-origin document retrieval for client-rendered pages — was attempted 173 times and succeeded 169 times (1988848 document characters retrieved), with 4 failures recorded as receipts. The size effect is stark: augmented skills have a median of 1824 words versus 486 for static pages, a ratio of 3.8$\times$. The run issued 417 network requests, all evidence origins marked live, under pipeline version 0.8 and cache version 7. Reproducibility is enforced rather than promised: every statistic in this manuscript is emitted as a token that must resolve against a machine-generated data contract, and every page carries a fetch receipt — URL, timestamp, SHA-256 content hash, and augmentation status — so any number can be traced to a specific observation within the 2026-09-10T23:51:05.959201+00:00 through 2026-09-10T22:19:21.394219+00:00 (UTC) window. Failed augmentations are reported, not silently dropped. Keywords: agent skills, SKILL.md, web scraping, Skillarum, provenance, reproducible research.

## Keywords

agent skills · SKILL.md · web scraping · Skillarum · reproducible research · digital art documentation · provenance

## Artifacts

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.22712650](https://doi.org/10.5281/zenodo.22712650) |
| **Published** | 2026 |
| **Version** | 0.1.0 |
| **Zenodo record** | https://zenodo.org/records/22712650 |
| **GitHub release** | https://github.com/docxology/FractiSkills/releases/tag/v0.1.0 |
| **Source repository** | https://github.com/docxology/FractiSkills |

## Files

- `FractiSkills_combined.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *FractiSkills: One Portable Agent Skill per Page*. Zenodo. DOI: 10.5281/zenodo.22712650. URL: https://doi.org/10.5281/zenodo.22712650.

## Related

- Zenodo record: https://zenodo.org/records/22712650
- GitHub release: https://github.com/docxology/FractiSkills/releases/tag/v0.1.0
- Source repository: https://github.com/docxology/FractiSkills
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
