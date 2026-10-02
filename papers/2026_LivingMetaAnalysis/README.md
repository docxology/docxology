<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 A Living Meta-Analysis of the Modafinil Literature

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20931964-blue)](https://doi.org/10.5281/zenodo.20931964)

---

## Abstract

> Manual synthesis cannot keep pace with a fast-growing research literature, and ad-hoc reviews bind no evidence to a reproducible pipeline. We present a configurable, reproducible meta-analysis framework that takes a single search term and produces a complete quantitative portrait of its literature. For this instance the term is Modafinil. The pipeline dispatches across 7 literature engines (arXiv, OpenAlex, Semantic Scholar, Crossref, PubMed, SovietRxiv, and ChinaRxiv), each degrading gracefully to a skipped source when an API key or the network is unavailable, then merges and de-duplicates records by a canonical identifier hierarchy (DOI $>$ arXiv ID $>$ Semantic Scholar ID $>$ OpenAlex ID $>$ title digest) into a corpus of $N = 2302$ records spanning 2000--2026 (26 years). Records are classified into a configurable 6-bucket subfield taxonomy (Clinical Sleep, Cognition, Pharmacology, Psychiatry, Safety, and Neuroscience); the largest subfield is Clinical Sleep (64.3\% of the classified corpus). The corpus grows at a compound annual rate of 3.45\% (mean year-over-year growth 6.3\%, doubling time 11.3 years), peaking in 2025 with 112 records. Non-negative matrix factorization extracts 5 latent topics over a 500-feature vocabulary, offline deterministic embeddings place every title, abstract, and (when available) full text in a shared vector space, and citation-network analysis exposes the corpus's internal structure (8,772 intra-corpus edges across 2204 nodes, 1377 communities, graph density 0.18\%). Of 38,802 total outgoing references, 22.6\% resolve to another record inside the corpus. Abstract coverage stands at 55.5\%, open-access status is known for 14.4\% of records, and 40.9\% have a direct PDF link. An optional, LLM-gated knowledge-graph stage scores the 6 hypotheses explored against the evidence. This run produced 18 publication-quality figures. Every domain-specific value in this manuscript — the search term, keyword set, engine roster, subfield taxonomy, and hypotheses — is injected from a single configuration file and the pipeline's own outputs; re-targeting the configuration re-targets the entire paper. The result is a reusable architecture for living literature reviews: continuously re-runnable, evidence-bound syntheses for any topic. Keywords: modafinil, meta-analysis, literature retrieval, bibliometrics, record de-duplication, full-text mining, document embeddings, citation network, topic modeling, entity extraction, wakefulness, cognitive enhancement, reproducible research

## Keywords

`modafinil` · `meta-analysis` · `literature retrieval` · `bibliometrics` · `record de-duplication` · `full-text mining` · `document embeddings` · `citation network` · `topic modeling` · `entity extraction` · `wakefulness` · `cognitive enhancement`

## Methods

- **Multi-engine literature retrieval across 7 engines with graceful degradation** — Dispatches the 'modafinil' query to arXiv, OpenAlex, Semantic Scholar, Crossref, PubMed, SovietRxiv and ChinaRxiv; unavailable engines report skipped without aborting.
- **Canonical-identifier de-duplication and keyword relevance filtering** — Merges records by DOI > arXiv ID > Semantic Scholar ID > OpenAlex ID > title digest, keeping the most complete version, then filters by relevance keywords and start year 2000.
- **Keyword-based 6-bucket subfield classification and growth metrics** — Classifies records into Clinical Sleep, Cognition, Pharmacology, Psychiatry, Safety and Neuroscience and computes year counts, CAGR and doubling time.
- **TF-IDF (500 features) + NMF topic model and TF-IDF/SVD embeddings** — Builds a 500-feature TF-IDF representation of titles/abstracts, extracts 5 NMF topics, and embeds texts with offline deterministic TF-IDF/SVD.
- **Intra-corpus citation network and config-driven token-injected manuscript** — Builds a citation graph with community detection; all manuscript numbers are injected from a single config file and pipeline outputs with fixed seeds.

## Key Findings

- The live run retrieved and de-duplicated a corpus of 2302 modafinil records spanning 2000-2026.
- In the retrieved corpus (2000–2026), modafinil publications grow at a CAGR of 3.45%, doubling every 11.3 years, with a peak of 112 publications in 2025.
- Clinical Sleep is the largest subfield, at 64.3% of the classified corpus.
- The citation network has 2204 nodes, 8,772 edges and 1377 communities, with 22.6% of outgoing references resolving inside the retrieved corpus.
- The author notes the corpus is a bounded sample: a 1,000-per-engine cap applied and Semantic Scholar was rate-limited, returning zero records.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_literature_meta_analysis](https://github.com/docxology/template_literature_meta_analysis)
- GitHub release: [v0.1.0](https://github.com/docxology/template_literature_meta_analysis/releases/tag/v0.1.0)
- DOI: [10.5281/zenodo.20931964](https://doi.org/10.5281/zenodo.20931964)
- Zenodo record: [https://zenodo.org/records/20931964](https://zenodo.org/records/20931964)
- PDF: [Friedman_2026_Living_412d4fcf.pdf](Friedman_2026_Living_412d4fcf.pdf)
- PDF SHA-256: 412d4fcf4b0c2e14fb950f9080f107d81fd9a90dfdf216b9161a13833eff62ff

## Citation

> Daniel Ari Friedman (2026). *A Living Meta-Analysis of the Modafinil Literature*. Zenodo. DOI: 10.5281/zenodo.20931964. URL: https://doi.org/10.5281/zenodo.20931964.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
