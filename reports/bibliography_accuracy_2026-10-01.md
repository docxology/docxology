# Bibliography accuracy review — 2026-10-01

This follow-up independently reviewed the bibliography accuracy payload,
sampled source-grounded summaries, checked every explicitly adjudicated
abstract against the public metadata, and reviewed the changed generation
contracts. It supplements the earlier full summary review; it does not claim
a new contextual review of every summary or execution of software described
by the archived papers. The bibliography remains the citation source of truth,
and existing citation keys remain permanent public URLs.

## Source recovery and identity

| Work | Evidence and decision |
| --- | --- |
| #100 DopamineForaging | Archived the correct published article from [NLM's open dataset](https://pmc-oa-opendata.s3.amazonaws.com/PMC6205345.1/PMC6205345.1.json). Exact DOI, title, seven authors, published-version status and CC BY license match. PDF SHA-256: `7325c9a11c8cd665622ec8143afb64b606cd967607e7a7cc8359411fd2e773f8`. Its final eight pages include the methods supplement. The summaries preserve the inhibitor-measurement limitation and nonsignificant results. |
| #168 GNN | Archived the manuscript from [Zenodo v3.6.0, record 22985529](https://zenodo.org/records/22985529). The complete archive MD5 matches its registered checksum; the extracted manuscript SHA-256 is `acb7749c561b26562064421ca2f7fbca68c8b0e8a955082e5d5a3e28b50bd784`. License: CC BY-NC-SA 4.0. The canonical concept DOI remains unchanged; the version DOI is labeled as the artifact. A direct [DataCite concept-record resolution](https://api.datacite.org/dois/10.5281/zenodo.7803313), latest version and manuscript name Friedman alone. Current citations follow that evidence; historical community-contributor credit is preserved in metadata. The cover date and its internal 3.5.0 reference are distinguished from the enclosing 3.6.0 release. Described software checks were not independently run in this bibliography pass. |
| #63 ToComment | [Crossref](https://api.crossref.org/works/10.1016/j.plrev.2023.06.002) and [PubMed](https://pubmed.ncbi.nlm.nih.gov/37331216/) bind the full registered title to Tickles and Friedman in 2023. Removed the unrelated DRE3 artifact DOI, version and 2022 release date. The full title preserves the existing citation key. PubMed has no abstract; no licensed full text was identified. |
| PaleolithicRockstars | The [registered commentary](https://api.crossref.org/works/10.1016/j.plrev.2024.04.010) and [PubMed record](https://pubmed.ncbi.nlm.nih.gov/38735269/) do not support the old cave-painting/genomics seed synopsis. Removed that synopsis, keywords and template methods/findings. Licensed full text remains unavailable. |
| FocusedAttentionMeditation | The [publisher chapter](https://link.springer.com/chapter/10.1007/978-3-032-16955-6_11) provides a public abstract and identifies subscription full text. Retained a labeled abridged publisher synopsis and cleared ungrounded template methods/findings. Simulation results and proposed future work remain distinct from empirical evidence. |

The recovered PDFs, extraction choices, licenses, archive custody and summary
quotes are recorded in each work's `metadata.json`. Quote occurrence proves
that the excerpt belongs to the archived text; contextual review supports
the paraphrase. These checks do not independently establish the truth of a
paper's results or the behavior of its software.

## Resolved catalog and generation decisions

- Corrected ConCatEnate (#129), Beacons (#132), and DataDescriptorTemplate
  (#192) to Computational: their source texts concern computational agent
  designs and FAIR data/template infrastructure.
- Kept #108's 2015 print/issue year; the 2014 advance-access date is a
  separate publication event.
- Kept registered titles for iTrace (#165), DemoCreate (#166), and THALIA
  (#207); source title variants do not silently replace canonical identities.
- Retained LineSet's five-work collected PDF: it contains the named chapter
  and is an intentional collection, rather than a misfiled unrelated source.
- Verified Skillarum, SilverLine and LineSet's printed version DOIs against
  official Zenodo concept/version relations. Every local PDF matches its
  registered version-file MD5 and size. Kept the concept citation DOI and
  recorded the verified version as `artifact_doi`; the exact API evidence and
  local SHA-256 bindings are in [the DOI-role receipt](bibliography_doi_roles_2026-10-01.json).
- Aligned all 86 explicitly reviewed abstract-decision/recovery folders with
  their displayed source; corrected four false descriptions, seven false
  keyword sets, and the unsupported Woodlice thermodynamic wording.
- Corrected work citations to include the ordered recorded authors, aligned
  SKILL descriptions with curated abstracts, rejected stale CFF artifact
  identifiers, and bound document-verified author intake to its current
  DOI-free bibliography work and archived evidence before writing.
- Limited packed-name inversion to audited name/ORCID aliases; an unfamiliar
  compound surname or ambiguous name order is preserved for review.
- Preserved complete URLs in clipped excerpts and updated the generated
  manifest's bibliography dependency for per-paper CFF identities.

## Deferred decisions and concrete follow-up

| Item | Current decision and follow-up |
| --- | --- |
| #159 Active Blockference | Retain the existing 2022 event-year entry. Establish an event-year versus publication-year policy before adopting Crossref's 2023 year; first preserve and test the existing work URL independently of the changed year. |
| #12 EvoJump, #26 Discovery Engine, #74 TrustFinder | Retain the existing short catalog titles. Full registry/document titles require an explicit stable-key mechanism before replacement. TrustFinder's consultant is not automatically added to the registered creators. |
| #29 SUMO | Retain registered creators pending depositor reconciliation: the title-page list omits a registered creator. A quote alone does not authorize removing a concept-record contributor. |
| #33 Digital Twins | Retain the registered author pending reconciliation. The document's five-person list labels contributing organizations and representatives, which does not by itself establish a five-author byline. |
| Unavailable sources | Acquire legitimate, licensed full text for ToComment, PaleolithicRockstars and FocusedAttentionMeditation, extract it, and replace the explicit gaps with reviewed source-grounded summaries. |
| Internal manuscript inconsistencies | Resolve the conflicting corpus/group/model/test/work counts in the originating publications, then archive the corrected versions. The bibliography summaries retain limitations and avoid disputed assignments. See DOC-016. |
| Scholar metrics | Retain the existing authenticated snapshot. A refresh requires a new direct authenticated observation and matching SHA-bound receipt. |

Verification uses the repository's full test suite, Ruff, generated-layer
validation, external-link triage and artifact-budget gate. Published commit
parity, hosted checks, Pages deployment and live-site acceptance are separate
evidence steps; this source-review report alone does not assert them.

The subsequent [live acceptance receipt](bibliography_live_acceptance_2026-10-01.json)
records the successful Pages deployment, its exact commit, the previous main
commit, and seven matching server/local SHA-256 comparisons. The paired
[site verification receipt](live_site_verification_2026-10-01.json) records
all 17 live contract checks passing at that deployed revision.
