# Full text: Mapping William Blake's Works: Evidence ledgers, source provenance, text-image diagnostics, and rights-bounded release controls

> Extracted from `Blake.pdf`
> Source: https://zenodo.org/api/records/23921364/files/Blake.pdf/content
> SHA-256: 812e53237b40f808b4502e3dd358cbee5cda7d587e493ba95e41f02c11ad03eb
> Version: 0.5.0
> Extraction: pypdf 6.16.2; 94 pages.

## Page 1

Mapping William Blake’s Works
Evidence ledgers, source provenance, text-image diagnostics, and rights-bounded release
controls
Daniel Ari Friedman
Active Inference Institute
daniel@activeinference.institute
ORCID: 0000-0001-6232-9096
DOI: 10.5281/zenodo.21047573
2026-11-01


## Page 2

Contents
Abstract 3
1 Introduction: Making Blake Coverage Measurable 4
1.1 Related Work: Blake Editions, Digital Corpus Methods, and Representativeness Risks . . . . . . . . . . 4
2 Methods: T arget Ledger, Source Custody , and Offline Analysis 6
2.1 Units and Target-Ledger Denominator . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
2.2 Acquisition Architecture and Source Authority . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
2.3 Retained Sources and Independent Analysis Epoch . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
2.4 Provenance and Missing-Evidence Queue . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7
3 Methods: Shared Evidence Operations and Saved Corpus Diagnostics 8
3.1 Shared Mechanisms and Application Policy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
3.2 Exact Support and Record Multiplicity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8
3.3 Finite Grouped-Category Composition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
3.4 Retrieval Profiles and Counting Units . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
3.5 Source-Bound Occurrence Search . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
3.6 Analysis Population and Authorship Boundary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
3.7 Text and Model Diagnostics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
3.8 Membership-Bound Text Projection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
3.9 Images, Cross-Modal Joins, and Error Accounting . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
4 Results: T arget Coverage, Provenance, and Evidence Gaps 14
4.1 Target-Ledger Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14
4.2 Local Record and Modality Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
4.3 Retained Evidence Gaps and Search Queue . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 16
5 Results: T ext Scale, Visual Evidence, and Cross-Modal Diagnostics 18
5.1 Lexical Results: Text Scale, Vocabulary, and Phrase Diagnostics . . . . . . . . . . . . . . . . . . . . . . 18
5.2 Embedding Results: Covariance Principal-Component Structure and Entity Extraction . . . . . . . . . . 20
5.3 Theme-Graph Results: A Navigable Index of Blake Motifs . . . . . . . . . . . . . . . . . . . . . . . . . . 22
5.4 Image-Linkage Results: Work-Level Cross-Modal Evidence . . . . . . . . . . . . . . . . . . . . . . . . . . 22
6 Discussion: What the Corpus Can and Cannot Claim 28
7 Rights and Distribution Controls 29
7.1 Duration and Reproduction Layers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
7.2 Provider Policies and Release Decisions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
7.3 Use-Specific Review . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 30
8 Limitations: T arget Scope, Source Drift, and Missing Evidence 31
9 Reproducibility: Source Snapshot, Analysis Epoch, and Publication 32
9.1 Verify Retained Inputs Before Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32
9.2 Create and Analyze a New Local Epoch . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 32
9.3 Generate Figures and Hydrate the Manuscript . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
9.3.1 Authoring, Evidence and Output Roots . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
9.3.2 Mathematical Interval Diagnostic . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
9.4 Render and Validate . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 34
10 Conclusion: Evidence-Bounded Blake Corpus Mapping 35
11 Supplement: T arget-Ledger Evidence Gap T able 36

## Page 3

12 Supplement: Bounded Missing-Evidence Search Queue 41
13 Supplement: Aggregate Image and Evidence Profiles 81
14 Supplement: Rights Matrix for Distribution and Reuse Decisions 85
15 Supplement: Local Recovery and Integrity Evidence 87
2

## Page 4

Abstract
William Blake’s works survive across editions, copy records, image archives, museum catalogues, transcriptions, and
finding aids. Computational coverage is diﬀicult to assess without explicit units, source authority, and evidence bound-
aries. We present blake, a 7-phase pipeline that connects a 104-entry work-level target ledger with retained source
records, local analysis, provenance, recoverability checks, and generated publication artifacts.
The saved offline run analyzes 727 local source/copy records. Its 6109 image associations reference 5975 distinct files.
It represents 69 ledger targets (66.3%) and fully satisfies the declared evidence profile for 45 targets (43.3%). The
text-bearing subset has 540 records and 682407 tokenizer-defined words. These exploratory text results include retained
transcriptions with unverified authorship; they are not a Blake-authored language census. The top-level analysis ledger
records 727/727 records analyzed and 0 top-level errors. Nested sub-analysis limitations are counted separately.
Local recovery preserves 8481 inventoried files and 5975/6003 discovered image identifiers, leaving 28 unresolved.
Checksums and a corruption-detection restore drill establish recoverability of the captured inventory, not complete-
ness of Blake’s oeuvre. Quantitative prose, tables, and figures derive from saved artifacts. Public releases contain
project-authored software, manuscript sources, aggregate evidence, and checksums; provider texts, XML, images, pri-
vate indexes, backups, and source-image mosaics remain local. The contribution is an auditable corpus-governance and
preservation method with explicit scholarly and distribution limits.
The implementation separates corpus custody from application policy. Portable source snapshots and explicit schema
conversion preserve source identities and roles, while distinct retrieval profiles expose normalized-token, literal-casefold
and regex contracts. Shared counting, hierarchy and evidence-admission methods support application papers with-
out embedding their vocabularies or interpretations. Exact half-open interval methods distinguish occupied support,
multiplicity and overlapping record pairs while keeping source frames and application judgments explicit. Current
source-derived diagrams identify those interfaces separately from the historical analytical producer.
3

## Page 5

1 Introduction: Making Blake Coverage Measurable
Computational work on William Blake faces a bibliographic problem before any interpretation begins. The William
Blake Archive is treated here as the principal public scholarly digital base for editorial metadata, Text Encoding Initiative
(TEI) transcriptions, facsimile-oriented identifiers, copy structures, and object references [ Eaves et al., 1996, Eaves, 1997,
Eaves et al. , 1999, 2002, Viscomi, 2002, Jones, 2006, Crawford and Levy , 2017, Fox and Fletcher , 2018, Whitson and
Whittaker, 2013]. That literature matters because the Archive is not merely a file host: it is a long-running scholarly
edition and relational environment for works, copies, objects, texts, images, and editorial decisions [ Reed, 2014, Fox
and Fletcher , 2018]. Printed catalogues, editions, and visual scholarship supply broader authority for title histories,
copy relations, textual canon boundaries, and image/object classes [ Bentley, 1977, 1995, 2004, Butlin, 1981, Bindman,
1978, Essick, 1980, Erdman, 1988, Viscomi, 1993, Phillips, 2000]. Project Gutenberg, Wikisource, the Internet Archive,
museum catalogues, HathiTrust, and finding lists add useful corroboration, but their holdings and identifiers do not
align cleanly with Blake bibliography, copy history, or the Archive’s object model. A corpus that simply reports what
it downloaded can therefore look more complete than it is.
The central design choice in blake is to make completeness a measured object rather than a mood of confidence. The
system declares a pipeline-canonical target ledger, profile canonical, version 2026-06-22, with 104 work-level entries.
Every acquired record is matched back to that ledger, and every ledger target is classified as present, partial, missing,
duplicate, or unverified. The reported run holds 727 local source/copy records, represents 69 ledger targets (66.3%),
and reaches full required evidence for 45 targets (43.3%). That difference matters: representation means that a target
has local work evidence, while full presence requires the expected text and image evidence declared by the ledger. The
same distinction applies within source evidence: Archive-primary records, validated fallback text, and corroborating or
unclassified records remain visibly tiered rather than flattened into a single undifferentiated “source” field.
This paper therefore reports a target-aware offline analysis epoch over retained evidence, not a complete Blake corpus.
The remaining 2 partial targets and 35 missing targets are part of the result. They are not treated as incidental
defects outside the narrative; they are surfaced in the manifest, tables, figures, and a missing-evidence search report.
The manuscript also distinguishes generated visual design from evidentiary images: the cover is a generated Blakean
interpretation with recorded provenance, while corpus images are tied to acquisition metadata. When the opt-in Archive
image mirror is used, image coverage is reported as object-depth evidence rather than as a vague claim to “all images. ”
This stance follows the reproducibility norms of computational research [ Peng, 2011, Sandve et al. , 2013, Wilson et al. ,
2014] and the Findable, Accessible, Interoperable and Reusable (F AIR) emphasis on explicit, reusable provenance
[Wilkinson et al. , 2016].
1.1 Related Work: Blake Editions, Digital Corpus Methods, and Representativeness
Risks
This project sits at the intersection of Blake bibliography, digital scholarly editing, and corpus design. Blake’s work-
level and object-level boundaries are mediated by catalogues, editions, visual records, and illuminated-book scholarship
rather than by file availability alone [ Bentley, 1977, Butlin, 1981, Bindman, 1978, Viscomi, 1993]. The William Blake
Archive gives the corpus a stable public digital environment, but the project is not itself a replacement for an archive,
scholarly edition, database, catalogue raisonne, or thematic research collection; those terms name different scholarly
objects and responsibilities [ Price, 2009, Sahle, 2016, McGann, 1991, McKenzie, 1999]. The same distinction matters for
source leads. The Morgan Library’s Pickering Manuscript pages are source-owned and page-level, whereas the Blake/An
Illustrated Quarterly Four Zoas bibliography and article index are scholarship controls rather than corpus evidence [ The
Morgan Library & Museum , 2021, 2026, Blake/An Illustrated Quarterly , 2026b,a]. At the same time, the target-ledger
method follows corpus-linguistic work on design criteria and representativeness, where the evidentiary value of a corpus
depends on declared inclusion rules, sampling assumptions, and a visible denominator rather than raw size [ Atkins et al.,
1992, Biber, 1993, McEnery and Hardie , 2012]. Digital-literary-history and data-modeling scholarship further motivate
the distinction between represented, partial, missing, and fully evidenced targets: data are constructed by modeling
choices, and digitized availability is not the same thing as literary representativeness [ McCarty, 2005, Flanders and
Jannidis, 2019, Pechenick et al. , 2015, Bode, 2018, Piper, 2018, Underwood, 2019].
Collections-as-data scholarship makes the same point at the institutional scale. A reusable cultural-heritage dataset is
not a neutral dump of whatever files happen to be available; it is an accountable transformation of collections, metadata,
4

## Page 6

rights constraints, and documentation into a publishable data object [ Padilla et al. , 2019a,b, Candela et al. , 2023]. blake
applies that lesson locally. It does not redistribute provider files in this manuscript build, and it does not use source
leads as automatic evidence. Instead, it exposes the target ledger, audit rows, acquisition review, analysis diagnostics,
figure registry, and rights gate as linked surfaces that let a reader test how each claim was made.
Recent cultural-heritage artificial intelligence (AI) work points to adjacent, but different, design spaces: multimodal
metadata assignment for cultural-heritage artifacts, museum knowledge graphs, and multimodal heritage knowledge-
graph extension [ Rei et al. , 2023, Li et al. , 2025, Zhang et al. , 2026]. Those papers are relevant because Blake evidence
is both textual and visual, but this manuscript does not use them as evidence that blake performs knowledge-graph
completion or open-world metadata inference. Here, graph-like structures and multimodal tables are run-bounded
diagnostics over acquired local evidence.
The paper contributes a provenance-aware corpus scaffold for Blake studies. It combines a researched work-level
ledger, source-audit capabilities, local acquisition, metadata normalization, text and visual analysis, cross-modal linkage,
manuscript generation, and a reproducible visual identity for the report. It also demonstrates how a digital-humanities
pipeline can scale toward macroanalytic questions [ Jockers, 2013, Wilkens, 2015, Underwood, 2019] while refusing to
let partial evidence masquerade as complete coverage. The methods sections describe the target ledger, source audit,
acquisition path, and analysis modules; the results sections report coverage, provenance, evidence gaps, missing-evidence
candidates, text scale, visual linkage, object-image depth, authority tiers, and theme structure. The paper’s central
interpretive discipline is therefore double: it reports what the saved corpus can support and specifies what the model
must not yet be asked to prove.
5

## Page 7

2 Methods: Target Ledger, Source Custody, and Offline Analysis
The blake pipeline is organized as a 7-phase directed acyclic graph (DAG): discovery, acquisition, metadata, analysis,
visualizations, export, and reports. The saved publication run completed 5 phases with status completed. Discovery and
acquisition reused the retained local evidence; this run did not make new source-availability measurements. Analysis
and downstream reporting generated fresh artifacts. fig. 1 distinguishes those actions. Automated derivation connects
the saved inputs, analysis, figures, and quantitative prose [ Sandve et al. , 2013, Wilson et al. , 2014].
Figure 1: Saved corpus workflow as a 7-phase directed acyclic graph. Discovery and acquisition reused retained local
evidence without a live refresh; analysis and downstream reporting generated new artifacts. Counts describe this saved
run and do not establish that every external Blake source has been mirrored.
2.1 Units and Target-Ledger Denominator
The target ledger, profile canonical, version 2026-06-22, declares 104 work-level targets. It is canonical for this pipeline,
rather than a complete canon for Blake studies. Bibliographies, editions, Archive identifiers, and visual catalogues
inform its titles, aliases, categories, expected modalities, and source hints [ Bentley, 1977, 1995, 2004, Butlin, 1981,
Erdman, 1988, Viscomi, 1993].
A local record has a different unit: it is a retained source document or copy-level record. The 727 local records must
not be read as that many distinct Blake works. Multiple copies and source documents can map to the same ledger
target. Image counts likewise have two units: 6109 work-image associations reference 5975 distinct existing local image
files, with 134 associations beyond the unique-file count. Analyses can revisit the same physical image through different
records; these associations are not independent image observations. Neither the work-level ledger nor the retained
inventory establishes a complete copy-, plate-, impression-, or museum-object census [ Viscomi, 1993, Essick, 1980, Fox
and Fletcher , 2018].
2.2 Acquisition Architecture and Source Authority
The source registry contains 3 providers: the William Blake Archive, Project Gutenberg, and the Internet Archive.
The William Blake Archive supplies editorial and identifier authority [ Eaves et al. , 1996, 1999, Jones, 2006]. Project
Gutenberg, Wikisource, Internet Archive, the Erdman edition, museum catalogues, HathiTrust, and scholarly finding
lists provide fallback or corroborating leads. They are not interchangeable authorities [ Project Gutenberg , 2026, Wik-
isource contributors , 2026, Internet Archive, 2026, Erdman, 1988, Tate, 2026, The British Museum , 2026, HathiTrust
Digital Library , 2026, Essick, 1969, McGann, 1991, McKenzie, 1999].
The acquisition implementation can combine a declared ledger with pinned GitHub TEI inventories and bounded,
opportunistic Archive API enrichment. TEI filenames are resolved from the actual inventory before inferred copy-name
candidates are tried. Image acquisition normalizes object identifiers and records attempted source URLs. Fallback
6

## Page 8

transcriptions require explicit source, title, attribution, rights, and checksum review. Structured encoding is a model of
evidence rather than an assurance that extracted text is Blake-authored reading text [ TEI Consortium , 2026, Burnard,
2014, DeRose et al. , 1990].
These are acquisition capabilities, not activities newly measured by this offline run. Its live Archive metadata status is
unrecorded; the saved discovery and source-audit artifacts record reuse or not-rerun states. Previously captured URLs
and source commits remain provenance, not fresh endpoint-health evidence. Interface drift and reference rot make this
temporal distinction necessary [ Reed, 2014, Klein et al. , 2014, Van de Sompel et al. , 2013].
2.3 Retained Sources and Independent Analysis Epoch
The retained-source workflow captures source commits, byte sizes, SHA-256 digests, extraction outcomes, and unresolved
image references. Publication analysis starts from a new metadata database and copied decoded transcriptions under b
lake_data/publication/v0.2.0-01, while referencing the original image files. The original corpus database, recovery
manifest, passage file, and recovery search database are hash-checked before and after analysis. The prior analysis
output is preserved separately. This avoids modifying the captured evidence or silently combining new results with stale
per-record processing flags.
The saved run identifier is d1f5af70e02a45868db1c372ee28814a. Its analysis producer version is 0.2.0rc1; its input
receipt has SHA-256 a9d601d33222906bc06e3d69e00b7d67ff1a0fda4e07c7fb206fb0d30a817798 . The publication
software version and the version that actually produced the analysis are separate provenance fields. A package version
change does not retrospectively rerun an analysis. Recovery coverage, backup verification, and the corruption-detection
restore drill are reported separately in sec. 15.
2.4 Provenance and Missing-Evidence Queue
Source identifiers, URLs, authority tiers, rights notes, and image links accompany the local records. Coverage joins
them to the target ledger and emits missing-evidence candidates for targets that remain partial, missing, or unverified.
A candidate guides review; it does not establish that a remote source contains the required evidence. The queue in
tbl. 8 is derived from retained coverage and source hints. Endpoint states marked unchecked were not tested during
this analysis epoch. Provenance therefore records relationships among source material, acquisition, derived artifacts,
and claims without substituting availability for identity or permission [ Moreau and Groth , 2013, Soiland-Reyes et al. ,
2022].
7

## Page 9

3 Methods: Shared Evidence Operations and Saved Corpus Diagnostics
3.1 Shared Mechanisms and Application Policy
The public core separates reusable evidence mechanisms from caller-owned research decisions. Projection and portable-
bundle adapters retain source/copy identity, edition, locator, rights, role and plane under caller-held pins. Explicit
schema conversion validates those fields without supplying missing provenance or promoting unverified text. Shared
methods perform retrieval, counted aggregation, artifact admission and review-queue membership checks. Applications
supply query forms, scope, review labels and interpretation. This division permits selected corpus evidence to be reused
without treating the applications’ questions or conclusions as properties of the corpus itself.
Recovery executes through blake.recovery_commands and the registered corpus commands. Explicit schema conver-
sion belongs to blake.methods.schema_conversion; workspace serialization calls its public implementations directly.
Source-authority classification is shared by manifests, provenance exports and analytical displays. These interfaces
retain the distinct matching profiles and existing evidence boundaries.
The current source declares 3 retrieval profiles. The profile and responsibility diagnostic binds 25 source files under SHA-
256 ff1be696fd7fab1ab9a17151988bba9e38bb51bbf4d1af9f74193e752d388d98. fig. 2 is generated from those profile
declarations and explicit public API responsibility references. It measures the current implementation, independently
of the saved analytical producer 0.2.0rc1; it does not represent another NLP run.
The generic evidence-tree API validates a connected rooted hierarchy and computes a deterministic layout without
recursion. Sibling traversal follows declared order; placements return in declared node order. Leaves receive consecutive
rows and an internal row is the arithmetic mean of all descendant leaf rows. A veraging only immediate child rows would
over-weight small subtrees. Depth counts parent edges. Neither depth nor row represents elapsed time, evolutionary
distance or confidence, and the API supplies no domain taxonomy or identity judgment.
3.2 Exact Support and Record Multiplicity
An interval record is a half-open integer range 𝐼𝑖 = [𝑎 𝑖, 𝑏𝑖) in one caller-declared coordinate frame, with 0 ≤ 𝑎 𝑖 ≤ 𝑏 𝑖.
Equal endpoints represent empty support. The application establishes the frame, units, eligible records, source grouping
and any activation conditions before invoking geometry. Operations assume compatible coordinates supplied by the
caller; they do not authenticate a frame or source identity, establish a source-length bound or decide inclusion. A
source-indexed application must check its ranges against the exact original expression before computing geometry.
For a finite indexed collection 𝑅 = (𝐼 𝑖), define its union 𝑈 (𝑅) and its multiplicity-threshold support 𝐷𝑘(𝑅), for a
positive integer 𝑘:
𝑈 (𝑅) = ⋃
𝑖
𝐼𝑖, 𝐷 𝑘(𝑅) = {𝑥 ∶ ∑
𝑖
1𝐼𝑖
(𝑥) ≥ 𝑘} . (1)
Union, intersection and difference concern sets of coordinates. Their outputs are sorted maximal positive components;
adjacent components coalesce. The measure 𝜇(𝑆) denotes the total length of a coordinate support 𝑆; the API computes
𝜇(𝑈 (𝑅)), not the sum of record lengths. By contrast, the positive-intersection pair count preserves the separate record
indices:
𝜇(𝑈 (𝑅)) = ∑
[𝑎,𝑏)∈components(𝑈(𝑅))
(𝑏 − 𝑎), 𝑃 (𝑅) = ∑
𝑖<𝑗
1{max(𝑎𝑖, 𝑎𝑗) < min(𝑏𝑖, 𝑏𝑗)} . (2)
Duplicating a positive record leaves the union unchanged but can increase threshold support and the pair count.
Touching endpoints can join the union without producing a positive intersection. Empty records contribute neither
support nor pairs. The lengths 𝜇(𝑈 (𝑅)) and 𝜇(𝐷𝑘(𝑅)) concern different coordinate supports, while 𝑃 (𝑅) counts record
pairs; these quantities cannot substitute for one another. Subtraction retains every connected fragment of 𝑈 (𝑅) ∖ 𝑈 (𝑀 )
for a supplied mask collection 𝑀 ; it does not summarize a fragmented remainder by its total length alone.
fig. 3 is a mathematical illustration, not a corpus observation. Its 5 indexed records are [1, 5), [3, 7), [3, 7), [7, 9), [4, 4).
The union is [1, 9), with length 8, while the summed record lengths are 14. Against mask [4, 8), the intersection is [4, 8)
8

## Page 10

Figure 2: Source-derived retrieval contracts and declared responsibility boundaries. Profile normalization and boundary
descriptions come from the executable registry; the companion artifact binds the referenced public source files. Appli-
cation policy names required caller inputs, without measuring private application outcomes. This code diagnostic does
not update the saved corpus analysis.
9

## Page 11

and the remainder is [1, 4) ∪ [8, 9). Support covered by at least two indices is [3, 7), of length 4; support covered by at
least three is [3, 5). The positive-intersection pair count is 3. Geometric outputs and pair counts come from the actual
public API; summed record lengths are calculated directly from the validated input endpoints. Values are generated by
the tooling, rather than transcribed into the diagram or treated as findings about Blake.
The implementation sorts integer endpoints rather than enumerating coordinates. Union and pair counting use
𝑂(𝑛 log 𝑛) time; threshold support combines endpoint events before advancing to the next segment. Binary set opera-
tions canonicalize their operands and scan the resulting components. Arbitrary-size integer arithmetic avoids conversion
to floating coordinates. The figure’s displayed pair list is constructed only for this finite illustration through individual
API calls; the pair-counting API itself does not materialize that list.
Admission rejects invalid scalar types, undeclared fields, negative endpoints, reversed ranges and invalid thresholds.
Public operations revalidate existing models, including instances made through construction or copying that bypassed
normal admission. The illustration records 3 actual refusing controls: a boolean endpoint, a constructed reversed interval
and a boolean threshold. Accepting any of these aborts illustration production. Its 17 producer-source bindings have
digest 944a05aaaacae6f216bbf59668510f0c242d4b439bdef308109353a3e5a9c391 . These controls qualify named
implementation boundaries; they do not validate an application’s eligibility, grouping or interpretive choices. The
complete API and its separate software qualification are documented in docs/methods/intervals.md . Retrieval
windows retain their own matching and feasible-origin contract; they are not silently converted to this nonnegative
half-open geometry.
3.3 Finite Grouped-Category Composition
A separate composition API accepts explicit category identities and complete, disjoint group strata from the counted
inventory. It checks category counts, matched-unit denominators and token totals before comparing the pooled category
profile with the mean of within-group profiles. A group with no category mass has undefined composition and is omitted
from this particular mean; it remains a zero in coverage and can retain a defined zero token rate. Composition and
token frequency therefore answer different questions.
Total variation is half the sum of absolute differences between corresponding category shares. Leave-one-group-out
profiles expose dependence on supplied group identities. Rational mass thresholds and inverse concentration describe
how category counts are distributed across those groups. Zero mass remains undefined, ties follow declared category
order, and no procedure interprets overlapping categories as distinct organisms or groups as independent samples. These
descriptive measures supply neither significance tests nor confidence intervals for a larger population.
Applications select the categories and supply their literary or institutional meaning. The public implementation contains
no animal vocabulary, taxonomic allocation or political scoring rule. Its contract is documented in docs/methods/c
omposition.md . This source-method addition does not replace the retained exploratory NLP producer or reclassify
historical source text.
3.4 Retrieval Profiles and Counting Units
The regex profile uses Python IGNORECASE with explicit escaped alternatives and source word boundaries. Lit-
eral search uses Unicode casefold while retaining original-source spans and exact punctuation and whitespace. The
normalized-token profile applies NFKC and casefold before contiguous-token matching; punctuation and line breaks
separate tokens. These contracts can disagree, so a new profile is never substituted for an old query epoch. Runtime
Python and Unicode versions are recorded separately from stable semantic identity.
Counts name their units: occurrences, eligible stored source units, copy-retaining documents, exact-text groups or
distinct work identifiers. Eligible zero-hit groups and token denominators precede display caps. A source unit without
word tokens has an unavailable normalized rate. Exact-text grouping tests sensitivity to repetition while preserving the
original source/copy identities. Proximity restricts retrieval within a declared source unit or complete word window; it
does not establish semantic or historical relatedness.
10

## Page 12

Figure 3: Mathematical illustration in arbitrary integer coordinate units. The indexed records include a duplicate, an
adjacent positive record and an empty record. The canonical union has length 8, compared with summed record lengths
of 14; 3 unordered record pairs intersect positively. The mask, intersection, remainder and multiplicity-threshold rows
answer separate questions. Open endpoint markers and direct labels supplement color. The companion JSON binds
the exact illustrated inputs, API outputs, source bytes and generated image digests.
11

## Page 13

3.5 Source-Bound Occurrence Search
The private search profile keeps reading passages, Erdman editorial pages, and raw XML in separate source planes.
Primary scope requires identified authorship and primary reading text. Exploratory scope retains unverified and editorial
labels. Normalized token and phrase matches preserve offsets into the original expression; exact matching is case-
sensitive. Curated variants and concept vocabularies aid navigation without establishing semantic equivalence or whole-
oeuvre occurrence claims. Source and index integrity failures refuse a query. Search counts name the selected indexed
scope before display limits; the versioned contract is documented in docs/methods.md.
3.6 Analysis Population and Authorship Boundary
The saved analysis population is 727 local source/copy records, including 540 with text, 720 with images, and 537
with both. The recovered reading layer separates 199 primary-reading transcriptions from 341 transcriptions with
unverified authorship. The exploratory natural language processing (NLP) described below includes the saved text-
bearing subset without promoting every transcription to Blake-authored primary text. Archive-primary metadata
authority and reading-text authorship are different classifications.
Counts are descriptive for this retained population. Copy repetition, editorial material, shared image files, transcription
variants, and missing sources preclude treating records as independent samples of Blake’s oeuvre. Corpus construction
therefore bounds every downstream result [ Atkins et al. , 1992, Biber, 1993, Bode, 2018].
3.7 Text and Model Diagnostics
The text module writes basic token counts, per-record vocabulary size, type-token ratio, lexical sentiment, named
entities, sentence-level topic descriptors, style metrics, readability estimates, and theme matches. The lexical-signature
artifact applies its own documented deterministic tokenizer, stopword and editorial-apparatus filters, adjacent-term
phrase counts, and distinctive-term scores. Tokenizers and filters define different quantities; their totals are not assumed
interchangeable. Type-token ratios remain length-sensitive [ DeRose et al. , 1990, TEI Consortium , 2026, Tweedie and
Baayen, 1998, McCarthy and Jarvis , 2010].
Sentiment uses the Natural Language Toolkit (NLTK) Valence Aware Dictionary and sEntiment Reasoner (V ADER)
lexicon [ Hutto and Gilbert , 2014]. Readability uses the implementation’s sentence, word, and syllable heuristics to
compute Flesch-style estimates. Neither is validated here against Blake scholarship or annotated historical-language
judgments [Flesch, 1948, Pang and Lee , 2008, Kim and Klinger , 2019]. Topic extraction fits latent Dirichlet allocation to
sentence-level TF-IDF weights. That is an exploratory weighted-input heuristic rather than a validated generative model
of word counts. Short texts and vocabularies emptied by document-frequency pruning produce explicit unavailable/error
results; they do not contribute fabricated topic components [ Blei et al. , 2003, Blei, 2012].
Entity extraction combines the pretrained spaCy en_core_web_sm statistical model with bounded rule-based Blake
vocabularies. The ontology layer caps entities and relationships and serializes its outputs. It is not a Blake-specific
trained or validated entity recognizer. Named-entity strings, heuristic labels, co-occurrence relationships, and metadata-
derived themes are navigation aids requiring editorial review; a graph edge does not establish a historically correct
relation [ Weingart, 2011, Moretti, 2011, Ramsay, 2011].
3.8 Membership-Bound Text Projection
The manuscript diagnostic producer is version 0.7.0, with source SHA-256 7f818548bad51df1f8f3f2b69d1d4b8447f
060715cee4a7c7c494ff272d21e76. It is recorded separately from the producer of the saved per-record analyses.
The manuscript diagnostic selects text-bearing IDs from the saved text_metrics.json and resolves transcriptions
through that run’s manifest data directory. It rejects external or symlinked data-directory substitutions, excludes
unmatched cached IDs, and partitions saved members into embedded, missing-file, and token-empty groups. Content
and membership digests bind those selections. This fixes the source-selection boundary; it does not retrospectively
explain numerical discrepancies in earlier published epochs.
The projection uses 120 selected terms across 530 transcriptions. Term-frequency/inverse-document-frequency (TF-
IDF) vectors are normalized to unit length and centered. A symmetric covariance eigendecomposition computes the
12

## Page 14

leading principal components, with a fixed sign convention. Explained-variance fractions are nonnegative eigenvalues
divided by covariance trace. Rank-deficient and constant text spaces are checked against an independent singular-value
oracle. The display is a principal-component projection, not an uncentered latent semantic analysis, a learned semantic
encoder, or a stable map of Blake’s oeuvre. A direct numerical comparison with an independent eigendecomposition
checks the saved matrix and variance calculations. Missing, unverified, repetitive, and editorial transcriptions remain
interpretive constraints [ Biber, 1993, Bode, 2018, Rockwell and Sinclair , 2016].
3.9 Images, Cross-Modal Joins, and Error Accounting
Visual analysis computes image-level color and composition descriptors on local files. Repeated file associations can
be processed under several source records. Cross-modal analysis joins available text and image evidence; it does not
validate iconography, copy state, or a theory of Blake’s composite art [ Arnold and Tilton , 2019, Wevers and Smits, 2020,
Mitchell, 1994, Viscomi, 1993]. The work-theme visualization is a separate descriptive index, with 10576 nodes and 40828
edges including 10 theme nodes. The graph uses available metadata themes, scored text-analyzer themes, and entity
surface strings from the text module’s categories, including its other-entity category. It preserves case after whitespace
normalization and does not resolve spelling variants or authenticate historical identities. Its entity population differs
from the selected labels and rules used by the ontology census. Each record/theme or record/entity pair contributes
one edge; edge source labels distinguish metadata from model output. It is an exploratory index, with no validated
knowledge-graph or entity-authentication claim.
Top-level completion and nested component availability are separate ledgers. A completed record can contain a topic
or sentiment error. The publication census recursively counts explicit error fields and separately reports insuﬀicient-
text topic results, vocabulary-pruning failures, and any other nested errors. JSON artifacts, figure inputs, manuscript
variables, and publication checks preserve those distinctions [ Sandve et al. , 2013, Owens, 2018, Moreau and Groth ,
2013].
13

## Page 15

4 Results: Target Coverage, Provenance, and Evidence Gaps
The saved corpus represents 69 of 104 ledger targets (66.3%), while 45 satisfy the declared local evidence profile (43.3%).
The manifest classifies overall coverage as partial. Representation includes accepted or duplicate local matches; it
excludes missing and unverified ledger states. It is not a claim that every matched source/copy record is a distinct work
or a validated primary transcription.
4.1 Target-Ledger Results
The ledger classifies 45 targets as present, 2 as partial, and 35 as missing. Duplicate and unverified states remain explicit
in tbl. 1. These classifications express the pipeline’s modeling and evidence rules, rather than independent facts about
the limits of Blake’s oeuvre [ McCarty, 2005, Atkins et al. , 1992, Bowker and Star , 1999].
Figure 4: Coverage states for the 104-entry canonical ledger. Present, partial, missing, duplicate, and unverified states
remain distinct. Counts use the declared work-level target denominator rather than downloaded files or local source
records.
Table 1: Coverage states against the pipeline-canonical target ledger.
Status Targets % of ledger
present 45 43.3
partial 2 1.9
missing 35 33.7
duplicate 22 21.2
unverified 0 0.0
14

## Page 16

Figure 5: Coverage states by ledger category. Segments count modeled target states within each category. Category
labels do not independently validate source metadata, genre, dating, or historical representativeness.
15

## Page 17

Table 2: Target coverage by declared ledger category. Duplicate and unverified targets contribute to category totals;
the present percentage measures only fully satisfied targets.
Category Present Partial Missing Total Present %
color prints 0 0 1 1 0.0
commercial illustrations 8 0 9 18 44.4
drawings 2 0 3 5 40.0
engravings 0 0 2 2 0.0
illuminated books 3 0 2 20 15.0
letters 0 0 2 2 0.0
manuscripts 9 2 0 11 81.8
paintings 2 0 1 3 66.7
poems 1 0 1 2 50.0
separate prints 13 0 0 19 68.4
typographic works 2 0 1 3 66.7
watercolors drawings 5 0 13 18 27.8
4.2 Local Record and Modality Results
This offline epoch reconstructs target states from retained local records and does not import discovery-only candidates
as verified holdings. A target can therefore be missing locally even when a prior discovery ledger retained an unverified
lead. That ledger state is separate from the primary/unverified authorship labels on reading transcriptions.
The 727 local records include 10 metadata work-type labels. Those labels describe the retained metadata and can
include defaults or unresolved classification; they are not a newly validated genre census. Text availability is 74.3%,
image availability is 99.0%, and processing coverage is 100.0% of local records.
Table 3: Work-type labels recorded in local metadata, separate from the target-ledger categories.
Metadata work type Local records % of local records
manuscript 466 64.1
illuminated book 96 13.2
prophecy 51 7.0
letter 39 5.4
engraving 30 4.1
illustration 22 3.0
drawing 17 2.3
painting 3 0.4
prose 2 0.3
essay 1 0.1
The text-bearing subset contains 540 records, the image-bearing subset 720, and the joint subset 537. Repeated
source/copy records and reused image files can contribute to several record-level counts.
4.3 Retained Evidence Gaps and Search Queue
The unresolved targets remain part of the result. fig. 7 summarizes missing expected evidence; tbl. 7 gives the target-level
rows. Missingness shapes the scope of subsequent computational claims [ Klein, 2013, Borgman, 2015, Bode, 2018].
The retained audit generates 243 candidates across 59 targets: 54 text checks, 128 image checks, and 61 source-match
checks. tbl. 8 preserves their source hints, confidence scores, and actions. This offline run did not refresh provider
discovery or endpoint health. An unchecked status remains unchecked; source leads do not become corpus evidence
without identity, attribution, rights, and content validation.
16

## Page 18

Figure 6: A vailable modalities across local records. Bars distinguish text-plus-image, text-only, image-only, and
metadata-only records. These are evidence-presence counts, not a population sample or a census of independent Blake
works.
Figure 7: Evidence gaps derived from non-present target states. Counts group missing expected text, image, source, or
local-record evidence. A gap is an acquisition or review task, not evidence that a named remote provider contains the
missing item.
17

## Page 19

5 Results: Text Scale, Visual Evidence, and Cross-Modal Diagnostics
This section reports exploratory analysis over retained source/copy records. The text population includes primary and
unverified transcriptions; its aggregates are not restricted to verified Blake-authored reading text. Because only 540 of
727 local source/copy records contain text, textual metrics describe a substantial but incomplete subset. Likewise, image
and cross-modal metrics describe the 720 image-bearing records and the 537 records with both modalities. The results
function as a materials meta-analysis: they show which local evidence can support text diagnostics, image diagnostics,
and joint inspection before any reader treats those diagnostics as literary interpretation. The figures should therefore
be read as interpretive displays of the saved evidence state, not as stylistic periodization, iconographic classification, or
a model of Blake as a whole [ Drucker, 2011, 2020].
5.1 Lexical Results: Text Scale, Vocabulary, and Phrase Diagnostics
The text-bearing subset contains 682407 total words. When per-record unique counts are summed, the subset contains
186289 unique-word observations; this is a per-record vocabulary diagnostic rather than a deduplicated corpus lexicon.
Per-record word counts range from 1 to 45281 words. fig. 8 plots the largest text-bearing records, and tbl. 4 records the
same top rows with unique-word and image-link counts.
Figure 8: Largest local text-bearing corpus records by word count. Bars measure acquired transcription length, showing
which source-backed text files dominate aggregate vocabulary and theme diagnostics; works without local text are
excluded.
18

## Page 20

Table 4: Largest text-bearing local source/copy records. The image column indicates whether a text-heavy work also
participates in cross-modal analysis.
Source/copy
record Words Unique words Vocab richness Image associations
Jerusalem The
Emanation of
The Giant
Albion
45281 5537 0.122 100
Jerusalem The
Emanation of
The Giant
Albion
45280 5537 0.122 100
Jerusalem The
Emanation of
The Giant
Albion
45279 5534 0.122 100
Jerusalem The
Emanation of
The Giant
Albion
45274 5540 0.122 100
Milton a Poem 19341 3557 0.184 50
Milton a Poem 18905 3492 0.185 49
Milton a Poem 17389 3368 0.194 45
Milton a Poem 17381 3369 0.194 45
Poetical
Sketches
12690 2995 0.236 72
A Descriptive
Catalogue
9980 2548 0.255 72
Jerusalem The
Emanation of
The Giant
Albion
8927 2038 0.228 31
illum 7806 1815 0.233 0
Vocabulary richness averages 0.680 across text-bearing records and ranges from 0.083 to 1.000. fig. 9 plots type-token
ratio against text length. The downward shape is expected for length-sensitive type-token ratios and should be treated
as a diagnostic of metric behavior over the acquired text set, not as a global claim about Blake’s vocabulary [ Tweedie
and Baayen, 1998, McCarthy and Jarvis , 2010, Jockers, 2013].
The lexical-signature artifact uses regex_token_frequency_stopword_filtered over 539 text-bearing records. It
records 392560 stopword-filtered lexical tokens and 15426 distinct terms, with mean lexical density 0.598. The highest-
count terms include thy, thou, albion, thee, night, man, love, and little, and frequent adjacent-term phrases include
thou art, daughters albion, eternal death, wilt thou, day night, and lamb god. fig. 10 visualizes the leading terms and
phrases, while tbl. 5 preserves their document-frequency context.
Table 5: Leading stopword-filtered corpus terms. Document counts show whether a term is corpus-wide or concentrated
in a small number of transcriptions.
Term Count Documents
thy 2773 142
thou 2497 145
albion 1991 67
19

## Page 21

Term Count Documents
thee 1811 127
night 1792 140
man 1631 175
love 1578 166
little 1465 140
los 1419 41
god 1317 164
down 1233 142
earth 1233 167
5.2 Embedding Results: Covariance Principal-Component Structure and Entity Extrac-
tion
The saved-run denominator contains 540 eligible text work IDs. Of these, 530 enter the embedding, 0 lack a local
transcription, and 10 yield no retained tokens. Those disjoint groups reconcile exactly. A further 0 cached IDs are
outside the saved text membership and cannot enlarge its denominator. The membership file is bound by SHA-256 a1
5fd169524308526a6cc3f3af604bb573d5b402e9602f6faaee6bb9573eddb1 . Coverage and embedding counts therefore
name their own selection rules; a difference is not silently treated as an acquisition or historical counting correction.
The text layer supports a more explicitly natural-language analysis than word counts alone. The manuscript pipeline
builds a row-normalized, centered TF-IDF covariance principal-component projection from 530 local transcriptions and
a 120-term vocabulary. fig. 11 projects that space onto the leading axes: PC1 accounts for 23.2% of the TF-IDF
variance, PC2 accounts for 9.6%, and the plotted plane accounts for 32.8%. This is a bounded corpus diagnostic, not a
semantic map of every Blake work, because texts absent from local storage cannot enter the vector space [ Biber, 1993,
Bode, 2018]. Its value is procedural: it makes the acquired text set explorable and contestable, the way algorithmic
criticism and computer-assisted interpretation treat computation as a partner in reading rather than an oracle [ Ramsay,
2011, Rockwell and Sinclair , 2016].
The leading vocabulary terms also make the projection auditable. PC1 is driven by terms such as blake, thee, night,
like, little, upon, joy, and love, while PC2 is driven by terms such as blake, thee, night, like, joy, little, sweet, and love.
These terms should be read as feature loadings over local transcriptions: they help locate clusters, outliers, transcription
effects, and acquisition artifacts, but they do not by themselves establish interpretive periodization.
Entity extraction adds a second kind of linguistic evidence. Across 540 ontological-analysis artifacts, 498 records
currently contribute named-entity evidence. The extraction layer records 37777 entity mentions across 5942 distinct
display-normalized strings and 8 entity labels, including person, org, gpe, loc, myth, symbol, place, and concept.
The most frequent display-normalized strings are Jerusalem, Albion, Earth, Sweet, Enitharmon, London, Urizen, and
Spectre. This is an index into person, place, mythic, and textual reference patterns, but it still requires human review
because Blakean names, plate captions, and editorial metadata can blur the boundary between character, place, title,
and bibliographic entity.
The per-record text-analysis artifacts broaden the picture further: 540 artifacts carry sentiment and readability diag-
nostics, with 226 positive, 202 neutral, and 112 negative sentiment classifications in the reported run. The mean Flesch
reading-ease score is 72.4, and topic extraction emitted 1251 topic components across local text-analysis artifacts. These
values help locate works for close reading and QA, but the manuscript treats them as computational descriptors rather
than as stand-alone literary judgments [ Flesch, 1948, Pang and Lee , 2008, Kim and Klinger , 2019, Blei, 2012, Ramsay,
2011].
The nested-component census records 277 explicit error fields. Topic extraction is unavailable for 268 records because
of insuﬀicient text and for 9 because pruning leaves no vocabulary; 0 other nested errors remain. These counts are
separate from 0 top-level analysis errors and do not imply that every requested component succeeded.
20

## Page 22

Figure 9: Vocabulary richness versus text length for local text-bearing records. Each point is one acquired transcription;
the log-scaled x-axis supports comparison across text sizes, while the metric remains bounded to local text evidence
and is not a Blake-wide stylistic claim.
21

## Page 23

Figure 10: Stopword-filtered lexical signature for local transcriptions. Term and phrase counts are generated from the
acquired text files used elsewhere in the manuscript, so the denominator is the local text subset rather than unsourced
Blake-wide vocabulary.
5.3 Theme-Graph Results: A Navigable Index of Blake Motifs
The record/theme/entity graph contains 10576 nodes and 40828 edges, including 10 theme nodes and 9839 case-sensitive
entity surface strings from the text module. These strings include categories outside the ontology census above; the two
totals are not interchangeable. fig. 12 summarizes the most frequent themes by record-theme links. The graph indexes
how the acquired corpus is currently organized, but it inherits the corpus evidence boundary: manuscript targets with
missing text cannot contribute textual entities until their transcriptions are acquired [ Newman, 2010, Weingart, 2011,
Moretti, 2011].
5.4 Image-Linkage Results: Work-Level Cross-Modal Evidence
The visual subset contains 6109 image associations linked across 720 source/copy records. They reference 5975 distinct
physical files, with 134 reused associations. fig. 13 shows the works with the most local image evidence, while tbl. 6
records whether those image-rich works also carry text. Image-bearing means that at least one local image record is
linked to a work; object-depth mirroring is measured separately in the supplement. In this run the image-depth dataset
records 722 works, 6137 resolved Archive object candidates, and 6109 locally available object-image associations. These
counts support distant-viewing style inventory and QA, but they still do not imply full copy-, plate-, object-, or manifest-
level completeness outside the discoverable Archive API paths used by the command [ Butlin, 1981, Bindman, 1978,
Viscomi, 1993, Arnold and Tilton , 2019, Wevers and Smits , 2020].
fig. 14 adds the complementary view: text length is plotted against linked local image count, with color encoding lexical
density. This makes the joint analytical surface visible instead of implying that every text-bearing work is equally visual
or that every image-bearing work has enough transcription evidence for language analysis.
22

## Page 24

Figure 11: Latent text embedding from local transcriptions. The map projects 530 text-bearing corpus records from
a 120-term TF-IDF matrix onto deterministic covariance principal-component axes; missing and image-only works do
not enter this textual geometry.
23

## Page 25

Figure 12: Theme frequencies in the generated record-theme graph. Bars count current local record-theme links from
serialized analysis artifacts; the graph is an index over acquired evidence, not a settled thematic hierarchy for Blake’s
complete oeuvre.
24

## Page 26

Figure 13: Local works with the most linked image evidence. Bars count locally stored image records by work. Green
means local text is present and gold means it is absent; the adjacent table also states text availability explicitly. These
colors describe the text-image comparison subset, not source authority.
25

## Page 27

Figure 14: Text-image density across local text-bearing records. Each point is a work with local text; x encodes
transcription length, y encodes linked local image files, and color encodes lexical density, so image-only works and
remote-only objects remain outside this plot.
26

## Page 28

Table 6: Local works with the most image evidence. Rows with text available are candidates for joint text-image
reading; rows without text remain visual-evidence records only.
Source/copy record Image associations Has text
Illustrations to Young’s Night
Thoughts
537 yes
V ALA, or The Four Zoas 145 no
Blake’s Notebook 122 no
Illustrations to Gray’s Poems 116 yes
Illustrations to Dante’s Divine
Comedy
102 yes
Jerusalem The Emanation of The
Giant Albion
100 yes
Jerusalem The Emanation of The
Giant Albion
100 yes
Jerusalem The Emanation of The
Giant Albion
100 yes
Jerusalem The Emanation of The
Giant Albion
100 yes
Blake’s Annotations to Bacon’s
Essays Moral, Economical, and
Political.
91 yes
A Descriptive Catalogue 72 yes
Poetical Sketches 72 yes
The corpus supports cross-modal inspection for 537 works. It also supports an opt-in Archive object-image mirror whose
depth is reported in fig. 16 and fig. 17. The result remains a descriptive materials corpus: text, image, and joint analyses
are tied to recorded local evidence, while object-depth counts are bounded by discoverable Archive work/copy metadata
and local download success [ Mitchell, 1994, Drucker, 2011, 2020, Arnold and Tilton , 2019]. This is the appropriate
level of claim for a corpus-governance paper: the pipeline identifies where cross-modal reading is possible and where the
evidence surface is still too thin.
27

## Page 29

6 Discussion: What the Corpus Can and Cannot Claim
The shared-core/application-policy boundary makes reuse reviewable. Different applications can consume the same
pinned source evidence while declaring different query vocabularies, retrieval profiles and review policies. Agreement
in byte custody does not imply agreement in interpretation. Likewise, a reusable hierarchy layout is a mechanism for
displaying declared relationships; the application must justify those relationships independently. The profile diagnostic
therefore documents computational choices rather than presenting shared software as a validation of any literary or
disciplinary conclusion.
The main result is a connected account of corpus construction, local custody, and bounded analysis. The 727 source/copy
records map to 69 represented ledger targets; 45 meet the full declared evidence profile. Those are different quantities.
Copy repetition, source authority, authorship, missing modalities, and rights decisions remain visible instead of being
collapsed into a download count [ Atkins et al. , 1992, Biber, 1993, McEnery and Hardie , 2012, Price, 2009, Sahle, 2016].
The exploratory language results describe 682407 tokenizer-defined words across 540 text-bearing records. They include
transcriptions with unverified authorship and must not be interpreted as Blake-wide vocabulary, sentiment, or entity
estimates. A separate primary-scope search requires verified reading-text roles. This separation lets uncertain material
remain recoverable and inspectable without silently promoting it into primary evidence [ Pechenick et al. , 2015, Bode,
2018, Piper, 2018, Underwood, 2019].
Preservation adds a complementary denominator. A source inventory can be fully recoverable relative to its declared
captured files while image acquisition remains incomplete and whole-oeuvre coverage remains unknown. The backup
checksum and the failed-before-repaired corruption control test byte custody. They do not test scholarly completeness
or transcription accuracy. Reusing original images while analyzing an independent metadata store preserves that
distinction across analysis epochs [ Owens, 2018, Kirschenbaum, 2008, Moreau and Groth , 2013].
The computational figures are instruments for review and close reading. Vocabulary projections expose transcription and
selection effects; theme links and entity strings suggest places to inspect. They do not establish literary periodization,
iconographic truth, or a settled semantic graph. In particular, spaCy performs pretrained statistical named-entity
recognition. Its outputs are not model-free, and this project supplies no Blake-specific accuracy validation. Future
multimodal, optical-character-recognition, and knowledge-graph experiments require their own evidence and evaluation
[Ramsay, 2011, Rockwell and Sinclair , 2016, Drucker, 2011, 2020, Greif et al. , 2025, Rei et al. , 2023, Li et al. , 2025,
Zhang et al. , 2026].
Publication custody is part of the method. The generated cover is a labeled design asset; aggregate figures are project-
authored analytical displays. Provider-image mosaics remain private. The public release distributes software, manuscript
sources, aggregate evidence, and checksums, while preserving the distinction between the project license and source-
provider rights [ Candela et al. , 2023, Padilla et al. , 2019b]. Publication identifies a reproducible artifact set; it is not
peer review or a declaration of completed Blake scholarship.
The remaining work follows the evidence ledger: resolve partial and unverified targets, improve source/copy classification
and dating, review reading-text authorship, investigate unresolved image references, and evaluate model outputs against
editorial judgments. New acquisition must record current source identity and availability rather than inherit the
endpoint-health claims of an older epoch [ Reed, 2014, Klein et al. , 2014, Van de Sompel et al. , 2013].
28

## Page 30

7 Rights and Distribution Controls
This section records the release’s operational distribution policy, not legal advice or item-level clearance. Underlying
authorship, publication history, editorial contributions, digital files, provider terms, database rights, and a particular
proposed use are separate questions. The release publishes project code, manuscript prose, aggregate figures, and
reproducibility metadata while withholding the expressive provider corpus.
7.1 Duration and Reproduction Layers
William Blake died in 1827. His death date supports a public-domain baseline for ordinary life-plus-70 author-term
works, but it is insuﬀicient to decide every source file’s status. U.S. pre-1978 publication rules differ from modern
author-term rules. The Copyright Oﬀice’s circular states that works published in the United States before 1931 are in
the public domain as of 2026; that statement must not be generalized without regard to publication history or other
legal categories [ U.S. Copyright Oﬀice , 2026b,c].
Special unpublished-work rules also matter. U.S. section 303 can preserve a floor through 2047 for qualifying older works
first published by the end of 2002. U.K. guidance describes protection through 2039 for specified older unpublished
works and engravings. The E.U. term directive provides a 25-year economic-rights term for qualifying first lawful
publication or communication of a previously unpublished work after copyright expiry [ U.S. Copyright Oﬀice , 2026b,
UK Intellectual Property Oﬀice , 2021, European Parliament and Council of the European Union , 2006]. These are
reasons to retain item-level publication-history questions, especially for manuscripts and later editions.
Underlying public-domain art and a supplied digital file must likewise be distinguished. Feist separates unprotectable
facts from original selection or arrangement. Bridgeman addresses originality in exact photographic copies of public-
domain two-dimensional art, without supplying a worldwide license for every image file. E.U. DSM Article 14 excludes
copyright or related-rights protection for reproductions of expired visual-art works unless the reproduction itself meets
the originality criterion [ Supreme Court of the United States , 1991, United States District Court for the Southern
District of New York , 1999, European Parliament and Council of the European Union , 2019, Petri, 2014]. Modern
editorial apparatus may contain original expression even where Blake’s own text is public domain. Whether a particular
file or contribution qualifies requires source-specific assessment.
7.2 Provider Policies and Release Decisions
Provider terms are not automatically copyright, nor does every online term necessarily bind every user. Ordinary notice
and assent remain relevant to contract analysis [ United States Court of Appeals for the Second Circuit , 2002, United
States Court of Appeals for the Ninth Circuit , 2014]. This release nevertheless follows a conservative publication policy:
potential provider, edition, database, contract, and access restrictions are reviewed independently from underlying
public-domain status [ Mazzone, 2006, Wallace, 2022].
The historical static Blake Archive conditions page describes restrictions on Archive texts and images. It is historical
evidence of a policy, not a verified current permission grant; the current permissions route could not be refreshed during
the publication check. Keep raw Archive files and full image mirrors out of the public deposit unless an applicable item-
level permission or reuse basis has been documented [ The William Blake Archive , n.d.a,n]. This withholding policy
does not assert that every faithful reproduction necessarily has a new copyright.
The default release rules are:
• Code, tests, scripts, and project-authored prose: include under the repository license to the extent the
authors hold the relevant rights.
• Aggregate counts, checksums, source URLs, authority labels, and charts without source images:
include with provenance and citations. The release does not relicense the underlying provider material [ Supreme
Court of the United States , 1991].
• Blake-authored underlying material: assess separately from its supplied edition, transcription, apparatus, or
image file. Public-domain authorship is not an automatic license for every surrounding contribution.
• Project Gutenberg material: distinguish underlying text from Project Gutenberg branding and license wrap-
pers; any proposed distribution must follow the applicable source and trademark conditions [ Project Gutenberg
29

## Page 31

Literary Archive Foundation , 2026]. This release includes no fallback source texts.
• Wikisource material: inspect the specific revision, footer, history, and attribution requirements. Current
Wikimedia terms use CC BY-SA 4.0 for contributed text, with provisions and exceptions for imported material
and public-domain content. Do not assume a universal license from a page’s presence on Wikisource or fold
contributor text into MIT [ Wikimedia Foundation, 2026].
• Archive TEI/XML, transcriptions, images, private indexes, backups, and restore copies: retain
locally; omit from the public repository and deposit.
• Museum and catalogue leads: cite as corroborating metadata or future review leads unless a compatible reuse
basis is established for a proposed file.
• Generated cover and project-authored diagrams: include with provenance and a non-evidence label. The
release license conveys only rights the authors can license; inclusion does not assert exclusive copyright in generated
output.
• Mosaics containing acquired source images: retain as private inspection artifacts. They are omitted from
the public PDF, HTML, and reproduction archive.
The code can be open source; the entire local evidence cache is not thereby open source. The Archive-all acquisition
option describes evidence depth, not a permission grant. Public assets exclude blake_data/ and other provider-payload
territories. sec. 14 records the corresponding artifact-level checklist [ Candela et al. , 2023].
7.3 Use-Specific Review
U.S. section 107 weighs purpose, nature, amount, and market effect for the particular use. Research or indexing is not an
automatic blanket exemption. HathiTrust and Google Books concern specific transformative uses; they do not authorize
this project to publish a bulk mirror of provider files [ U.S. Copyright Oﬀice , 2026a, United States Court of Appeals for
the Second Circuit , 2014, 2015]. A proposal to distribute excerpts, thumbnails, images, or expressive derived material
requires its own source, attribution, amount, venue, and permission or exception review.
The deposited set therefore makes the workflow inspectable through software, source identities, aggregate evidence, and
commands while keeping the provider corpus local. Byte integrity, access, authorship, and distribution authority remain
separate properties [ Owens, 2018].
30

## Page 32

8 Limitations: Target Scope, Source Drift, and Missing Evidence
The ledger is a declared 104-target model, not a complete bibliography or a worldwide census of Blake holdings. It
represents 69 targets and fully satisfies evidence for 45. Partial, missing, duplicate, and unverified states remain explicit.
No result establishes a completed Blake corpus [ Biber, 1993, Pechenick et al. , 2015, Bode, 2018].
Local records have source/copy granularity. They are not independent works; image associations are not independent
physical files. The 540 text-bearing records include primary and unverified reading roles. Repeated copies, edition
apparatus, captions, transcription errors, and unknown authorship can affect aggregate words, vocabulary, entities,
themes, sentiment, and projections. Private primary-scope occurrence search has stricter authorship rules than the
exploratory NLP population.
The image inventory is bounded by discovered identifiers and successful local capture. Recovery leaves 28 discovered
image identifiers unresolved. Copy, plate, impression, coloring, unpublished-source, and museum-object coverage require
item-level scholarship beyond this inventory [ Viscomi, 1993, Essick, 1980, Butlin, 1981, Phillips, 2000]. Nominal source
resolution codes do not independently establish scan resolution or image quality.
This analysis reused local material without refreshing discovery, acquisition, or endpoint health. Retained URLs, source
commits, and historical checks do not establish present remote availability. The search queue is a review aid, not a
guarantee that a candidate contains the required text or image. Morgan manuscript pages and scholarly bibliographies
can guide review without satisfying whole-work evidence [ The Morgan Library & Museum , 2021, Blake/An Illustrated
Quarterly, 2026b, Yale Library, 2026, Reed, 2014, Klein et al. , 2014].
The models have no task-specific accuracy validation here. V ADER sentiment, heuristic readability, weighted-input topic
extraction, spaCy entities, rule-based themes, and image descriptors are computational diagnostics rather than literary
judgments. Short-text and pruned-vocabulary failures remain unavailable components. The principal-component display
is vocabulary- and membership-dependent and is evaluated in floating-point arithmetic. A numerical oracle checks
computation, not literary validity [ Flesch, 1948, Kim and Klinger , 2019, Blei, 2012, Ramsay, 2011].
The Python dependency lock does not pin separately downloaded language-resource bytes or guarantee bitwise equality
of a new model run. Saved result ledgers and their identities define the numerical evidence used by this publication.
Preservation evidence is also bounded. Checksums and the restore drill test captured bytes; they do not prove transcrip-
tion correctness, complete source acquisition, scholarly acceptance, or redistribution rights. The backup and restore
copies reside locally, and a copied-byte drill alone does not establish resilience to loss of the entire physical storage
device. The public release omits expressive provider files and image mosaics. Its code license does not relicense the
private evidence cache.
The generated cover is a labeled design asset with recorded provenance, outside the corpus ledger. Generative images
supply no evidence about Blake’s objects or historical technique [ Klein et al. , 2025].
31

## Page 33

9 Reproducibility: Source Snapshot, Analysis Epoch, and Publication
The publishing information gives the concept DOI for this versioned working paper. The release manifest identifies the
particular deposited edition and its exact PDF and source bytes. Earlier deposited versions remain separate archival
records.
Reproduction requires the captured source inventory, its private local files, the recorded analysis producer, and a
compatible environment. The public release supplies project-owned source, the manuscript, aggregate evidence, producer
identities, and checksums; it does not supply the provider corpus. The preservation chain connects inputs, commands,
derived results, figures, and rendered bytes [ Peng, 2011, Sandve et al. , 2013, Wilson et al. , 2014, Moreau and Groth ,
2013, Owens, 2018].
9.1 Verify Retained Inputs Before Analysis
Use a fresh reproduction checkout with the recorded dependency lock and the documented Python environment. Restore
or acquire the local evidence under applicable provider terms, then run the integrity verifier:
uv run python -m blake.recovery_commands verify
The saved recovery-manifest digest is 7b98377fe3e3f61cf8dd8781d47e5854876c490472419df61b1a7d6689186e96. A
different capture defines a different input epoch. Source inventory recovery, unresolved images, and the historical restore
drill are reported in sec. 15. Fresh remote acquisition can produce a different inventory and must not be substituted
for the recorded capture without updating the evidence identities.
9.2 Create and Analyze a New Local Epoch
Preserve previous outputs before using a fresh checkout or an unused output directory. The preparation command
refuses an occupied destination and writes a new metadata database and copied transcriptions; it references original
local image files without copying or altering them.
uv run python scripts/prepare_manuscript_epoch.py \
--destination blake_data/publication/reproduction
uv run python scripts/reproduce_manuscript_analysis.py \
--data-dir blake_data/publication/reproduction \
--seed 20261023
The driver uses the corpus API with offline reuse, no synthetic fixtures, the core visualization profile, Archive-inventory
scope, and Archive-all image metadata. It seeds Python and NumPy and limits numerical-library and OpenCV threads.
The analyzed publication epoch used software 0.2.0rc1, seed 20261023, and run ID d1f5af70e02a45868db1c372ee288
14a. The reproduction bundle records its exact producer-file digests separately from the final publication software. The
original run saved its model payloads in JSON but omitted the SQLite handoff consumed by reports and the dashboard.
A separately receipted derived refresh restored those exact payloads to the independent publication database and
regenerated reports without repeating inference. The repair command, when needed for an already sealed previously
saved epoch, is:
uv run python scripts/refresh_manuscript_epoch.py
Reseal after that command. New analyses persist each component directly. The original model receipt remains un-
changed; derived-artifact provenance names its own producer. Subsequent manuscript diagnostics select the saved run’s
actual data directory and identified result ledger.
The saved pipeline status is completed, with 727/727 records analyzed and current-results status yes. Its top-level
ledger reports 0 errors; the recursive component census reports 277 nested errors, including 268 insuﬀicient-text and 9
pruned-vocabulary topic results. Successful pipeline completion does not erase component unavailability.
32

## Page 34

9.3 Generate Figures and Hydrate the Manuscript
9.3.1 Authoring, Evidence and Output Roots
Preparation normally reads evidence and writes derived outputs in the authoring project. A staged authoring candidate
may instead name an explicit evidence read root with --evidence-root or BLAKE_MANUSCRIPT_EVIDENCE_ROOT. This
changes the saved analysis and custody inputs while keeping manuscript prose, legal-claim ledger and executing producer
code in the authoring tree. Generated figures and hydrated sources remain under its output/ directory. No other
checkout is searched and an invalid explicit read root fails even if authoring caches exist.
uv run python scripts/generate_manuscript_figures.py --public-only \
--evidence-root "$BLAKE_EVIDENCE_ROOT"
TEMPLATE_REPO_ROOT=../template \
uv run python scripts/z_generate_manuscript_variables.py \
--evidence-root "$BLAKE_EVIDENCE_ROOT"
Figure preparation reads diagnostic inputs without rewriting their saved files. A bounded aggregate/text stage cannot
satisfy full recovery verification merely by being selected as a read root. Strict publication-token admission retains its
saved-epoch and input-binding checks; full recovery and backup verification still require their original complete local
sources. Preserve existing output artifacts before producing a new display epoch. A source-code profile diagram has its
own source digest and never changes the analytical producer identity.
With the retained backup and historical restore-control files available locally, the publication seal freshly verifies the
captured inventory, existing backup, private search projection, and the retained repaired/corrupted control copies:
uv run python scripts/seal_manuscript_evidence.py \
--analysis-receipt analysis_output/data/analysis_epoch_receipt.json
This verifies the existing restore evidence; it does not run another restore drill. The commands require the private
corpus for analytical regeneration. The public reproduction archive separately includes hydrated manuscript sources
and aggregate figures for rendering the deposited paper without redistributing those source files.
The figure producer reads the saved analysis artifacts:
uv run python scripts/generate_manuscript_figures.py --public-only
TEMPLATE_REPO_ROOT=../template \
uv run python scripts/z_generate_manuscript_variables.py
The cover is a labeled project-authored generated asset with provenance, outside the corpus evidence ledger. Local
source-image mosaics can be generated for private inspection but are excluded from the public manuscript and repro-
duction archive. Publication hydration requires every used quantitative token to resolve from the saved artifacts and
verified publication evidence. The input membership and content digests remain inspectable.
9.3.2 Mathematical Interval Diagnostic
The registered core_interval_support figure is a mathematical illustration produced by manuscript_tools.inte
rval_illustration and manuscript_tools.interval_figure through the actual public interval API. It reads no
retained corpus or model output. Its JSON sidecar records the illustrated interval records, mask, canonical supports,
threshold supports, indexed pair count, actual refusal controls and source bindings, followed by digests of its PNG, SVG
and PDF assets. The figure source digest 944a05aaaacae6f216bbf59668510f0c242d4b439bdef308109353a3e5a9c391
is separate from the saved analytical producer and the deposited-paper identities.
The normal figure dispatcher includes this diagnostic in both local and public profiles. A code-only check can call the
dedicated builder with a new destination:
33

## Page 35

from pathlib import Path
from manuscript_tools.interval_figure import fig_interval_support
fig_interval_support(
Path("unused-analysis-input"),
Path("output/interval-illustration-new"),
)
Use the declared external Python environment and external temporary/cache bindings. The first argument retains the
common figure-builder interface and is deliberately not read. The dedicated builder refuses occupied artifact names and
symlinked output roots; its completion sidecar follows the real image files. It does not infer permission to regenerate a
corpus, recover missing provider files or invoke the native template. A passing code-only figure check is distinct from
complete figure/hydration preparation and final rendered-page acceptance.
9.4 Render and Validate
The shared template renderer uses a separate compatible environment. The release records its exact source commit.
Bind its local ignored projects/active/blake lifecycle leaf link to this checkout without changing other project
bindings. After strict hydration succeeds, run from that template checkout:
uv run python scripts/pipeline/stage_03_render.py \
--project active/blake --skip-manuscript-hydration
uv run python scripts/pipeline/stage_04_validate.py --project active/blake
The explicit hydration step preserves Blake’s analysis environment while using the template’s native rendering infras-
tructure. The skip flag reuses already validated hydrated sources; it does not authorize unresolved tokens or stale
results. Rendered-page inspection, citation and cross-reference checks, privacy checks, source tests, installed-package
checks, and release-asset checksums qualify the final artifact set. The deposited PDF and software assets must match the
independently verified download bytes. Publication and an identifier do not themselves establish peer review, scientific
validation, or whole-oeuvre completeness [ Smith et al. , 2016, Soiland-Reyes et al. , 2022].
34

## Page 36

10 Conclusion: Evidence-Bounded Blake Corpus Mapping
blake connects a declared work-level ledger, retained source custody, descriptive local analysis, private search, and
generated publication artifacts. The saved epoch analyzes 727 source/copy records and fully satisfies evidence for 45 of
104 ledger targets. Its 6109 image associations reference 5975 distinct files. Its 540 text-bearing records contain 682407
tokenizer-defined words, with primary and unverified transcription roles explicitly distinguished.
Recoverability is a separate measured result. The captured inventory contains 8481 files; image recovery retains 28
unresolved identifiers. Byte verification and the corruption-detection restore drill support custody of that inventory.
They do not establish a completed Blake corpus, definitive textual accuracy, validated interpretive models, or permission
to redistribute provider materials.
The remaining obligations are concrete: resolve partial and unverified target evidence, review reading-text authorship
and edition boundaries, test unresolved image leads, improve record classification, and validate model outputs against
scholarly judgments. Versioned software, saved producer identities, aggregate evidence, and separately checked publi-
cation bytes make those obligations reviewable. The public deposit preserves the method and its measured limits while
the expressive corpus remains local.
35

## Page 37

11 Supplement: Target-Ledger Evidence Gap Table
This table is the negative side of the coverage model. It records target-ledger rows that do not yet satisfy the current
evidence profile, so absence remains tied to a named target, category, status, and generated evidence note rather than
disappearing into an aggregate percentage [ McCarty, 2005, Klein, 2013].
Table 7: Targets not yet satisfying complete target evidence. Each row names the ledger target and the evidence note
generated by the coverage builder.
Target ID Title Category Status Evidence note
nnr There is No Natural
Religion
illuminated books duplicate Multiple local works
match this target
entry.
s-inn Songs of Innocence illuminated books duplicate Multiple local works
match this target
entry.
songs-experience Songs of Experience illuminated books missing No matching local
work or source record
in the current
discovery set.
songsie Songs of Innocence
and of Experience
illuminated books duplicate Multiple local works
match this target
entry.
thel The Book of Thel illuminated books duplicate Multiple local works
match this target
entry.
mhh The Marriage of
Heaven and Hell
illuminated books duplicate Multiple local works
match this target
entry.
vda Visions of the
Daughters of Albion
illuminated books duplicate Multiple local works
match this target
entry.
america America a Prophecy illuminated books duplicate Multiple local works
match this target
entry.
europe Europe a Prophecy illuminated books duplicate Multiple local works
match this target
entry.
urizen The First Book of
Urizen
illuminated books duplicate Multiple local works
match this target
entry.
s-los The Song of Los illuminated books duplicate Multiple local works
match this target
entry.
gates-child For Children: The
Gates of Paradise
illuminated books duplicate Multiple local works
match this target
entry.
gates-sexes For the Sexes: The
Gates of Paradise
illuminated books duplicate Multiple local works
match this target
entry.
milton Milton a Poem illuminated books duplicate Multiple local works
match this target
entry.
36

## Page 38

Target ID Title Category Status Evidence note
jerusalem Jerusalem The
Emanation of The
Giant Albion
illuminated books duplicate Multiple local works
match this target
entry.
abel The Ghost of Abel illuminated books duplicate Multiple local works
match this target
entry.
laocoon Laocoon engravings missing No matching local
work or source record
in the current
discovery set.
homer On Homer’s Poetry
[and] On Virgil
illuminated books missing No matching local
work or source record
in the current
discovery set.
bb206 To the Public:
Prospectus
typographic works missing No matching local
work or source record
in the current
discovery set.
everlasting-gospel The Everlasting
Gospel
poems missing No matching local
work or source record
in the current
discovery set.
bb209 V ALA, or The Four
Zoas
manuscripts partial Expected text is not
available locally.
bb122 Blake’s Notebook manuscripts partial Expected text is not
available locally.
letters Letters letters missing No matching local
work or source record
in the current
discovery set.
bb134 Receipts letters missing No matching local
work or source record
in the current
discovery set.
bb504 The Pastorals of
Virgil
commercial
illustrations
missing No matching local
work or source record
in the current
discovery set.
but536 Illustrations to
Milton’s Paradise
Lost, The Butts Set
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
but537 Illustrations to
Milton’s Paradise
Lost, The Linnell Set
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
but529 Illustrations to
Milton’s Paradise
Lost, The Thomas
Set
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
37

## Page 39

Target ID Title Category Status Evidence note
cpd The Large Color
Printed Drawings
color prints missing No matching local
work or source record
in the current
discovery set.
esi Joseph of Arimathea
Among the Rocks of
Albion
separate prints duplicate Multiple local works
match this target
entry.
esv Job separate prints duplicate Multiple local works
match this target
entry.
esvii Albion rose separate prints duplicate Multiple local works
match this target
entry.
esviii The Accusers of
Theft Adultery
Murder
separate prints duplicate Multiple local works
match this target
entry.
esx Lucifer and the Pope
in Hell
separate prints duplicate Multiple local works
match this target
entry.
esxiv Experimental Relief
Plate
separate prints duplicate Multiple local works
match this target
entry.
bbwba14 Portrait of George
Romney
engravings missing No matching local
work or source record
in the current
discovery set.
bb442 The Poetical Works
of Geoffrey Chaucer
commercial
illustrations
missing No matching local
work or source record
in the current
discovery set.
bb456 John Flaxman,
Compositions From
the Works Days and
Theogony of Hesiod
commercial
illustrations
missing No matching local
work or source record
in the current
discovery set.
bb466 William Hayley,
Designs to a Series of
Ballads
commercial
illustrations
missing No matching local
work or source record
in the current
discovery set.
bb467 William Hayley, An
Essay on Sculpture
commercial
illustrations
missing No matching local
work or source record
in the current
discovery set.
bb468 William Hayley, The
Life, and Posthumous
Writings, of William
Cowper
commercial
illustrations
missing No matching local
work or source record
in the current
discovery set.
bb469 William Hayley, The
Life of George
Romney
commercial
illustrations
missing No matching local
work or source record
in the current
discovery set.
38

## Page 40

Target ID Title Category Status Evidence note
bb470 William Hayley,
Little Tom the Sailor
commercial
illustrations
duplicate Multiple local works
match this target
entry.
bb499 John Gabriel
Stedman, Narrative,
of a Five Years’
Expedition, against
the Revolted Negroes
of Surinam
commercial
illustrations
missing No matching local
work or source record
in the current
discovery set.
bb512 John Whitaker, The
Seraph
commercial
illustrations
missing No matching local
work or source record
in the current
discovery set.
gravewd Drawings for Robert
Blair’s The Grave
drawings missing No matching local
work or source record
in the current
discovery set.
gravepd Sketches for Robert
Blair’s The Grave
drawings missing No matching local
work or source record
in the current
discovery set.
gravewc Preliminary
Illustrations to
Robert Blair’s The
Grave
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
pencil1 Pencil Sketches drawings missing No matching local
work or source record
in the current
discovery set.
but330 Illustrations to
Edward Young’s
Night Thoughts
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
but527 Illustrations to
Milton’s Comus, The
Thomas Set
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
but528 Illustrations to
Milton’s Comus, The
Butts Set
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
but538 Illustrations to
Milton’s On the
Morning of Christ’s
Nativity, The
Thomas Set
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
but542 Illustrations to
Milton’s On the
Morning of Christ’s
Nativity, The Butts
Set
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
39

## Page 41

Target ID Title Category Status Evidence note
but550 Illustrations to the
Book of Job, The
Butts Set
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
but551 Illustrations to the
Book of Job, The
Linnell Set
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
1780swc Water Color
Drawings
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
biblicalwc Water Color
Drawings Illustrating
the Bible
watercolors drawings missing No matching local
work or source record
in the current
discovery set.
biblicaltemperas Paintings Illustrating
the Bible
paintings missing No matching local
work or source record
in the current
discovery set.
40

## Page 42

12 Supplement: Bounded Missing-Evidence Search Queue
The search queue translates missing or partial target evidence into reviewable candidate actions. It is intentionally
conservative: a row can guide review without changing corpus status, because source ownership, title matching, attri-
bution, checksum, and rights metadata must be verified before a candidate becomes corpus evidence. Display labels
replace field-name underscores with spaces. Long prose words use discretionary hyphens, while identifiers may wrap
without a printed hyphen; authoritative identifiers remain unchanged in the accompanying aggregate JSON.
Table 8: Bounded missing-evidence search candidates. The table records where the next pass should look and whether
the relevant endpoint was checked during this run; it does not treat fallback sources as replacements for William Blake
Archive authority.
Target ID Title Evidence
Candidate
source Status Confidence Action
1780swc Water Color
Drawings
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
1780swc Water Color
Drawings
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
1780swc Water Color
Drawings
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
1780swc Water Color
Drawings
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
1780swc Water Color
Drawings
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
41

## Page 43

Target ID Title Evidence
Candidate
source Status Confidence Action
abel The Ghost of
Abel
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
america America a
Prophecy
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
bb122 Blake’s
Notebook
text William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
bb122 Blake’s
Notebook
text Blake
Archive
GitHub TEI
inventory
not checked 0.90 Search exact
Archive id in
the live TEI
filename
inventory.
bb122 Blake’s
Notebook
text Project
Gutenberg
author page
not checked 0.72 Record as
corrobor-
ating text
evidence
only; do not
override
Archive
authority.
bb122 Blake’s
Notebook
text Wikisource
author page
not checked 0.68 Record as
corrobor-
ating
transcription
evidence
when
title/alias
matches.
42

## Page 44

Target ID Title Evidence
Candidate
source Status Confidence Action
bb122 Blake’s
Notebook
text Internet
Archive
advanced
search
not checked 0.62 Record
facsimile or
derivative-
edition
evidence as
fallback
provenance.
bb122 Blake’s
Notebook
text HathiTrust
Blake record
not checked 0.56 Use catalog
records as
bibliographic
corrobor-
ation, not
primary text
authority.
bb134 Receipts source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
bb134 Receipts source match Yale
University
Library
not checked 0.67 manual
review:
source-owned
lead only;
exact-title
validation,
attribution,
checksum,
rights
metadata,
and
regenerated
coverage are
required
before any
target status
changes.
bb134 Receipts text William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
43

## Page 45

Target ID Title Evidence
Candidate
source Status Confidence Action
bb134 Receipts text Blake
Archive
GitHub TEI
inventory
not checked 0.90 Search exact
Archive id in
the live TEI
filename
inventory.
bb134 Receipts text Project
Gutenberg
author page
not checked 0.72 Record as
corrobor-
ating text
evidence
only; do not
override
Archive
authority.
bb134 Receipts text Wikisource
author page
not checked 0.68 Record as
corrobor-
ating
transcription
evidence
when
title/alias
matches.
bb134 Receipts text Internet
Archive
advanced
search
not checked 0.62 Record
facsimile or
derivative-
edition
evidence as
fallback
provenance.
bb134 Receipts text HathiTrust
Blake record
not checked 0.56 Use catalog
records as
bibliographic
corrobor-
ation, not
primary text
authority.
bb206 To the
Public:
Prospectus
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
bb206 To the
Public:
Prospectus
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
44

## Page 46

Target ID Title Evidence
Candidate
source Status Confidence Action
bb206 To the
Public:
Prospectus
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
bb206 To the
Public:
Prospectus
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
bb206 To the
Public:
Prospectus
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
bb206 To the
Public:
Prospectus
source match William
Blake
Archive
not checked 0.67 manual
review:
source-owned
lead only;
exact-title
validation,
attribution,
checksum,
rights
metadata,
and
regenerated
coverage are
required
before any
target status
changes.
bb206 To the
Public:
Prospectus
text William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
45

## Page 47

Target ID Title Evidence
Candidate
source Status Confidence Action
bb206 To the
Public:
Prospectus
text Blake
Archive
GitHub TEI
inventory
not checked 0.90 Search exact
Archive id in
the live TEI
filename
inventory.
bb206 To the
Public:
Prospectus
text Project
Gutenberg
author page
not checked 0.72 Record as
corrobor-
ating text
evidence
only; do not
override
Archive
authority.
bb206 To the
Public:
Prospectus
text Wikisource
author page
not checked 0.68 Record as
corrobor-
ating
transcription
evidence
when
title/alias
matches.
bb206 To the
Public:
Prospectus
text Internet
Archive
advanced
search
not checked 0.62 Record
facsimile or
derivative-
edition
evidence as
fallback
provenance.
bb206 To the
Public:
Prospectus
text HathiTrust
Blake record
not checked 0.56 Use catalog
records as
bibliographic
corrobor-
ation, not
primary text
authority.
bb209 V ALA, or
The Four
Zoas
text William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
bb209 V ALA, or
The Four
Zoas
text Blake
Archive
GitHub TEI
inventory
not checked 0.90 Search exact
Archive id in
the live TEI
filename
inventory.
46

## Page 48

Target ID Title Evidence
Candidate
source Status Confidence Action
bb209 V ALA, or
The Four
Zoas
text Project
Gutenberg
author page
not checked 0.72 Record as
corrobor-
ating text
evidence
only; do not
override
Archive
authority.
bb209 V ALA, or
The Four
Zoas
text Wikisource
author page
not checked 0.68 Record as
corrobor-
ating
transcription
evidence
when
title/alias
matches.
bb209 V ALA, or
The Four
Zoas
text Wikisource not checked 0.67 manual
review:
source-owned
lead only;
exact-title
validation,
attribution,
checksum,
rights
metadata,
and
regenerated
coverage are
required
before any
target status
changes.
bb209 V ALA, or
The Four
Zoas
text Internet
Archive
advanced
search
not checked 0.62 Record
facsimile or
derivative-
edition
evidence as
fallback
provenance.
bb209 V ALA, or
The Four
Zoas
text HathiTrust
Blake record
not checked 0.56 Use catalog
records as
bibliographic
corrobor-
ation, not
primary text
authority.
47

## Page 49

Target ID Title Evidence
Candidate
source Status Confidence Action
bb442 The Poetical
Works of
Geoffrey
Chaucer
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
bb442 The Poetical
Works of
Geoffrey
Chaucer
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
bb442 The Poetical
Works of
Geoffrey
Chaucer
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
bb442 The Poetical
Works of
Geoffrey
Chaucer
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
bb442 The Poetical
Works of
Geoffrey
Chaucer
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
bb456 John
Flaxman,
Composit-
ions From
the Works
Days and
Theogony of
Hesiod
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
48

## Page 50

Target ID Title Evidence
Candidate
source Status Confidence Action
bb456 John
Flaxman,
Composit-
ions From
the Works
Days and
Theogony of
Hesiod
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
bb456 John
Flaxman,
Composit-
ions From
the Works
Days and
Theogony of
Hesiod
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
bb456 John
Flaxman,
Composit-
ions From
the Works
Days and
Theogony of
Hesiod
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
bb456 John
Flaxman,
Composit-
ions From
the Works
Days and
Theogony of
Hesiod
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
bb466 William
Hayley,
Designs to a
Series of
Ballads
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
bb466 William
Hayley,
Designs to a
Series of
Ballads
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
49

## Page 51

Target ID Title Evidence
Candidate
source Status Confidence Action
bb466 William
Hayley,
Designs to a
Series of
Ballads
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
bb466 William
Hayley,
Designs to a
Series of
Ballads
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
bb466 William
Hayley,
Designs to a
Series of
Ballads
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
bb467 William
Hayley, An
Essay on
Sculpture
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
bb467 William
Hayley, An
Essay on
Sculpture
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
bb467 William
Hayley, An
Essay on
Sculpture
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
bb467 William
Hayley, An
Essay on
Sculpture
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
50

## Page 52

Target ID Title Evidence
Candidate
source Status Confidence Action
bb467 William
Hayley, An
Essay on
Sculpture
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
bb468 William
Hayley, The
Life, and
Posthumous
Writings, of
William
Cowper
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
bb468 William
Hayley, The
Life, and
Posthumous
Writings, of
William
Cowper
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
bb468 William
Hayley, The
Life, and
Posthumous
Writings, of
William
Cowper
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
bb468 William
Hayley, The
Life, and
Posthumous
Writings, of
William
Cowper
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
bb468 William
Hayley, The
Life, and
Posthumous
Writings, of
William
Cowper
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
51

## Page 53

Target ID Title Evidence
Candidate
source Status Confidence Action
bb469 William
Hayley, The
Life of
George
Romney
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
bb469 William
Hayley, The
Life of
George
Romney
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
bb469 William
Hayley, The
Life of
George
Romney
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
bb469 William
Hayley, The
Life of
George
Romney
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
bb469 William
Hayley, The
Life of
George
Romney
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
bb470 William
Hayley,
Little Tom
the Sailor
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
52

## Page 54

Target ID Title Evidence
Candidate
source Status Confidence Action
bb499 John Gabriel
Stedman,
Narrative, of
a Five Years’
Expedition,
against the
Revolted
Negroes of
Surinam
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
bb499 John Gabriel
Stedman,
Narrative, of
a Five Years’
Expedition,
against the
Revolted
Negroes of
Surinam
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
bb499 John Gabriel
Stedman,
Narrative, of
a Five Years’
Expedition,
against the
Revolted
Negroes of
Surinam
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
bb499 John Gabriel
Stedman,
Narrative, of
a Five Years’
Expedition,
against the
Revolted
Negroes of
Surinam
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
bb499 John Gabriel
Stedman,
Narrative, of
a Five Years’
Expedition,
against the
Revolted
Negroes of
Surinam
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
53

## Page 55

Target ID Title Evidence
Candidate
source Status Confidence Action
bb504 The
Pastorals of
Virgil
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
bb504 The
Pastorals of
Virgil
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
bb504 The
Pastorals of
Virgil
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
bb504 The
Pastorals of
Virgil
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
bb504 The
Pastorals of
Virgil
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
bb512 John
Whitaker,
The Seraph
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
bb512 John
Whitaker,
The Seraph
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
54

## Page 56

Target ID Title Evidence
Candidate
source Status Confidence Action
bb512 John
Whitaker,
The Seraph
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
bb512 John
Whitaker,
The Seraph
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
bb512 John
Whitaker,
The Seraph
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
bbwba14 Portrait of
George
Romney
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
bbwba14 Portrait of
George
Romney
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
bbwba14 Portrait of
George
Romney
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
bbwba14 Portrait of
George
Romney
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
55

## Page 57

Target ID Title Evidence
Candidate
source Status Confidence Action
bbwba14 Portrait of
George
Romney
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
biblical
temperas
Paintings
Illustrating
the Bible
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
biblical
temperas
Paintings
Illustrating
the Bible
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
biblical
temperas
Paintings
Illustrating
the Bible
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
biblical
temperas
Paintings
Illustrating
the Bible
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
biblical
temperas
Paintings
Illustrating
the Bible
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
56

## Page 58

Target ID Title Evidence
Candidate
source Status Confidence Action
biblicalwc Water Color
Drawings
Illustrating
the Bible
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
biblicalwc Water Color
Drawings
Illustrating
the Bible
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
biblicalwc Water Color
Drawings
Illustrating
the Bible
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
biblicalwc Water Color
Drawings
Illustrating
the Bible
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
biblicalwc Water Color
Drawings
Illustrating
the Bible
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
but330 Illustrations
to Edward
Young’s
Night
Thoughts
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
but330 Illustrations
to Edward
Young’s
Night
Thoughts
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
57

## Page 59

Target ID Title Evidence
Candidate
source Status Confidence Action
but330 Illustrations
to Edward
Young’s
Night
Thoughts
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
but330 Illustrations
to Edward
Young’s
Night
Thoughts
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
but330 Illustrations
to Edward
Young’s
Night
Thoughts
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
but527 Illustrations
to Milton’s
Comus, The
Thomas Set
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
but527 Illustrations
to Milton’s
Comus, The
Thomas Set
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
but527 Illustrations
to Milton’s
Comus, The
Thomas Set
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
but527 Illustrations
to Milton’s
Comus, The
Thomas Set
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
58

## Page 60

Target ID Title Evidence
Candidate
source Status Confidence Action
but527 Illustrations
to Milton’s
Comus, The
Thomas Set
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
but528 Illustrations
to Milton’s
Comus, The
Butts Set
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
but528 Illustrations
to Milton’s
Comus, The
Butts Set
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
but528 Illustrations
to Milton’s
Comus, The
Butts Set
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
but528 Illustrations
to Milton’s
Comus, The
Butts Set
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
but528 Illustrations
to Milton’s
Comus, The
Butts Set
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
59

## Page 61

Target ID Title Evidence
Candidate
source Status Confidence Action
but529 Illustrations
to Milton’s
Paradise
Lost, The
Thomas Set
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
but529 Illustrations
to Milton’s
Paradise
Lost, The
Thomas Set
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
but529 Illustrations
to Milton’s
Paradise
Lost, The
Thomas Set
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
but529 Illustrations
to Milton’s
Paradise
Lost, The
Thomas Set
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
but529 Illustrations
to Milton’s
Paradise
Lost, The
Thomas Set
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
but536 Illustrations
to Milton’s
Paradise
Lost, The
Butts Set
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
but536 Illustrations
to Milton’s
Paradise
Lost, The
Butts Set
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
60

## Page 62

Target ID Title Evidence
Candidate
source Status Confidence Action
but536 Illustrations
to Milton’s
Paradise
Lost, The
Butts Set
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
but536 Illustrations
to Milton’s
Paradise
Lost, The
Butts Set
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
but536 Illustrations
to Milton’s
Paradise
Lost, The
Butts Set
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
but537 Illustrations
to Milton’s
Paradise
Lost, The
Linnell Set
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
but537 Illustrations
to Milton’s
Paradise
Lost, The
Linnell Set
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
but537 Illustrations
to Milton’s
Paradise
Lost, The
Linnell Set
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
but537 Illustrations
to Milton’s
Paradise
Lost, The
Linnell Set
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
61

## Page 63

Target ID Title Evidence
Candidate
source Status Confidence Action
but537 Illustrations
to Milton’s
Paradise
Lost, The
Linnell Set
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
but538 Illustrations
to Milton’s
On the
Morning of
Christ’s
Nativity, The
Thomas Set
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
but538 Illustrations
to Milton’s
On the
Morning of
Christ’s
Nativity, The
Thomas Set
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
but538 Illustrations
to Milton’s
On the
Morning of
Christ’s
Nativity, The
Thomas Set
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
but538 Illustrations
to Milton’s
On the
Morning of
Christ’s
Nativity, The
Thomas Set
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
but538 Illustrations
to Milton’s
On the
Morning of
Christ’s
Nativity, The
Thomas Set
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
62

## Page 64

Target ID Title Evidence
Candidate
source Status Confidence Action
but542 Illustrations
to Milton’s
On the
Morning of
Christ’s
Nativity, The
Butts Set
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
but542 Illustrations
to Milton’s
On the
Morning of
Christ’s
Nativity, The
Butts Set
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
but542 Illustrations
to Milton’s
On the
Morning of
Christ’s
Nativity, The
Butts Set
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
but542 Illustrations
to Milton’s
On the
Morning of
Christ’s
Nativity, The
Butts Set
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
but542 Illustrations
to Milton’s
On the
Morning of
Christ’s
Nativity, The
Butts Set
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
but550 Illustrations
to the Book
of Job, The
Butts Set
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
63

## Page 65

Target ID Title Evidence
Candidate
source Status Confidence Action
but550 Illustrations
to the Book
of Job, The
Butts Set
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
but550 Illustrations
to the Book
of Job, The
Butts Set
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
but550 Illustrations
to the Book
of Job, The
Butts Set
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
but550 Illustrations
to the Book
of Job, The
Butts Set
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
but551 Illustrations
to the Book
of Job, The
Linnell Set
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
but551 Illustrations
to the Book
of Job, The
Linnell Set
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
but551 Illustrations
to the Book
of Job, The
Linnell Set
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
64

## Page 66

Target ID Title Evidence
Candidate
source Status Confidence Action
but551 Illustrations
to the Book
of Job, The
Linnell Set
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
but551 Illustrations
to the Book
of Job, The
Linnell Set
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
cpd The Large
Color
Printed
Drawings
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
cpd The Large
Color
Printed
Drawings
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
cpd The Large
Color
Printed
Drawings
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
cpd The Large
Color
Printed
Drawings
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
cpd The Large
Color
Printed
Drawings
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
65

## Page 67

Target ID Title Evidence
Candidate
source Status Confidence Action
esi Joseph of
Arimathea
Among the
Rocks of
Albion
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
esv Job source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
esvii Albion rose source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
esviii The Accusers
of Theft
Adultery
Murder
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
esx Lucifer and
the Pope in
Hell
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
66

## Page 68

Target ID Title Evidence
Candidate
source Status Confidence Action
esxiv Experime-
ntal Relief
Plate
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
europe Europe a
Prophecy
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
everlast
ing-gospel
The
Everlasting
Gospel
source match Project
Gutenberg
author page
not checked 0.64 Search
text-canon
fallback
holdings for
a title or
alias match.
everlast
ing-gospel
The
Everlasting
Gospel
source match Wikisource
author page
not checked 0.62 Search public
transcription
holdings for
a title or
alias match.
everlast
ing-gospel
The
Everlasting
Gospel
source match Internet
Archive
advanced
search
not checked 0.56 Search
facsimile and
edition
metadata for
title
corrobor-
ation.
everlast
ing-gospel
The
Everlasting
Gospel
text Project
Gutenberg
author page
not checked 0.72 Record as
corrobor-
ating text
evidence
only; do not
override
Archive
authority.
67

## Page 69

Target ID Title Evidence
Candidate
source Status Confidence Action
everlast
ing-gospel
The
Everlasting
Gospel
text Wikisource
author page
not checked 0.68 Record as
corrobor-
ating
transcription
evidence
when
title/alias
matches.
everlast
ing-gospel
The
Everlasting
Gospel
text Wikisource not checked 0.67 manual
review:
source-owned
lead only;
exact-title
validation,
attribution,
checksum,
rights
metadata,
and
regenerated
coverage are
required
before any
target status
changes.
everlast
ing-gospel
The
Everlasting
Gospel
text Internet
Archive
advanced
search
not checked 0.62 Record
facsimile or
derivative-
edition
evidence as
fallback
provenance.
everlast
ing-gospel
The
Everlasting
Gospel
text HathiTrust
Blake record
not checked 0.56 Use catalog
records as
bibliographic
corrobor-
ation, not
primary text
authority.
gates-child For Children:
The Gates of
Paradise
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
68

## Page 70

Target ID Title Evidence
Candidate
source Status Confidence Action
gates-sexes For the
Sexes: The
Gates of
Paradise
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
gravepd Sketches for
Robert
Blair’s The
Grave
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
gravepd Sketches for
Robert
Blair’s The
Grave
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
gravepd Sketches for
Robert
Blair’s The
Grave
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
gravepd Sketches for
Robert
Blair’s The
Grave
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
gravepd Sketches for
Robert
Blair’s The
Grave
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
69

## Page 71

Target ID Title Evidence
Candidate
source Status Confidence Action
gravewc Preliminary
Illustrations
to Robert
Blair’s The
Grave
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
gravewc Preliminary
Illustrations
to Robert
Blair’s The
Grave
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
gravewc Preliminary
Illustrations
to Robert
Blair’s The
Grave
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
gravewc Preliminary
Illustrations
to Robert
Blair’s The
Grave
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
gravewc Preliminary
Illustrations
to Robert
Blair’s The
Grave
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
gravewd Drawings for
Robert
Blair’s The
Grave
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
gravewd Drawings for
Robert
Blair’s The
Grave
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
70

## Page 72

Target ID Title Evidence
Candidate
source Status Confidence Action
gravewd Drawings for
Robert
Blair’s The
Grave
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
gravewd Drawings for
Robert
Blair’s The
Grave
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
gravewd Drawings for
Robert
Blair’s The
Grave
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
homer On Homer’s
Poetry [and]
On Virgil
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
homer On Homer’s
Poetry [and]
On Virgil
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
homer On Homer’s
Poetry [and]
On Virgil
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
homer On Homer’s
Poetry [and]
On Virgil
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
71

## Page 73

Target ID Title Evidence
Candidate
source Status Confidence Action
homer On Homer’s
Poetry [and]
On Virgil
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
homer On Homer’s
Poetry [and]
On Virgil
text William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
homer On Homer’s
Poetry [and]
On Virgil
text Blake
Archive
GitHub TEI
inventory
not checked 0.90 Search exact
Archive id in
the live TEI
filename
inventory.
homer On Homer’s
Poetry [and]
On Virgil
text Project
Gutenberg
author page
not checked 0.72 Record as
corrobor-
ating text
evidence
only; do not
override
Archive
authority.
homer On Homer’s
Poetry [and]
On Virgil
text Wikisource
author page
not checked 0.68 Record as
corrobor-
ating
transcription
evidence
when
title/alias
matches.
homer On Homer’s
Poetry [and]
On Virgil
text Internet
Archive
advanced
search
not checked 0.62 Record
facsimile or
derivative-
edition
evidence as
fallback
provenance.
72

## Page 74

Target ID Title Evidence
Candidate
source Status Confidence Action
homer On Homer’s
Poetry [and]
On Virgil
text HathiTrust
Blake record
not checked 0.56 Use catalog
records as
bibliographic
corrobor-
ation, not
primary text
authority.
jerusalem Jerusalem
The
Emanation
of The Giant
Albion
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
laocoon Laocoon image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
laocoon Laocoon image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
laocoon Laocoon image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
laocoon Laocoon image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
73

## Page 75

Target ID Title Evidence
Candidate
source Status Confidence Action
laocoon Laocoon source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
laocoon Laocoon text William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
laocoon Laocoon text Blake
Archive
GitHub TEI
inventory
not checked 0.90 Search exact
Archive id in
the live TEI
filename
inventory.
laocoon Laocoon text Project
Gutenberg
author page
not checked 0.72 Record as
corrobor-
ating text
evidence
only; do not
override
Archive
authority.
laocoon Laocoon text Wikisource
author page
not checked 0.68 Record as
corrobor-
ating
transcription
evidence
when
title/alias
matches.
laocoon Laocoon text Internet
Archive
advanced
search
not checked 0.62 Record
facsimile or
derivative-
edition
evidence as
fallback
provenance.
74

## Page 76

Target ID Title Evidence
Candidate
source Status Confidence Action
laocoon Laocoon text HathiTrust
Blake record
not checked 0.56 Use catalog
records as
bibliographic
corrobor-
ation, not
primary text
authority.
letters Letters source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
letters Letters text William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
letters Letters text Blake
Archive
GitHub TEI
inventory
not checked 0.90 Search exact
Archive id in
the live TEI
filename
inventory.
letters Letters text Project
Gutenberg
author page
not checked 0.72 Record as
corrobor-
ating text
evidence
only; do not
override
Archive
authority.
letters Letters text Wikisource
author page
not checked 0.68 Record as
corrobor-
ating
transcription
evidence
when
title/alias
matches.
75

## Page 77

Target ID Title Evidence
Candidate
source Status Confidence Action
letters Letters text Internet
Archive
advanced
search
not checked 0.62 Record
facsimile or
derivative-
edition
evidence as
fallback
provenance.
letters Letters text HathiTrust
Blake record
not checked 0.56 Use catalog
records as
bibliographic
corrobor-
ation, not
primary text
authority.
mhh The
Marriage of
Heaven and
Hell
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
milton Milton a
Poem
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
nnr There is No
Natural
Religion
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
pencil1 Pencil
Sketches
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
76

## Page 78

Target ID Title Evidence
Candidate
source Status Confidence Action
pencil1 Pencil
Sketches
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
pencil1 Pencil
Sketches
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
pencil1 Pencil
Sketches
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
pencil1 Pencil
Sketches
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
s-inn Songs of
Innocence
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
s-los The Song of
Los
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
77

## Page 79

Target ID Title Evidence
Candidate
source Status Confidence Action
songs-
experience
Songs of
Experience
image William
Blake
Archive
image/API
metadata
not checked 0.88 Use Archive
object/image
metadata
before
museum-
catalog
corrobor-
ation.
songs-
experience
Songs of
Experience
image British
Museum
collection
search
not checked 0.58 Use as vi-
sual/catalog
corrobor-
ation for
image
provenance.
songs-
experience
Songs of
Experience
image Tate artist
page
not checked 0.52 Use as vi-
sual/catalog
corrobor-
ation when
the work is
in Tate
holdings.
songs-
experience
Songs of
Experience
image Blake
Quarterly
Essick
finding list
not checked 0.48 Use as a
reproduction
finding aid,
not as local
image
evidence.
songs-
experience
Songs of
Experience
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
songs-
experience
Songs of
Experience
text William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
songs-
experience
Songs of
Experience
text Blake
Archive
GitHub TEI
inventory
not checked 0.90 Search exact
Archive id in
the live TEI
filename
inventory.
78

## Page 80

Target ID Title Evidence
Candidate
source Status Confidence Action
songs-
experience
Songs of
Experience
text Project
Gutenberg
author page
not checked 0.72 Record as
corrobor-
ating text
evidence
only; do not
override
Archive
authority.
songs-
experience
Songs of
Experience
text Wikisource
author page
not checked 0.68 Record as
corrobor-
ating
transcription
evidence
when
title/alias
matches.
songs-
experience
Songs of
Experience
text Internet
Archive
advanced
search
not checked 0.62 Record
facsimile or
derivative-
edition
evidence as
fallback
provenance.
songs-
experience
Songs of
Experience
text HathiTrust
Blake record
not checked 0.56 Use catalog
records as
bibliographic
corrobor-
ation, not
primary text
authority.
songsie Songs of
Innocence
and of
Experience
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
thel The Book of
Thel
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
79

## Page 81

Target ID Title Evidence
Candidate
source Status Confidence Action
urizen The First
Book of
Urizen
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
vda Visions of
the
Daughters of
Albion
source match William
Blake
Archive work
API
not checked 0.96 Checked
Archive API
metadata
and GitHub
TEI
inventory
before
external
fallbacks.
The manual-review rows include source-owned leads and scholarship controls. For example, Morgan Library page-level
records for The Pickering Manuscript show that exact page transcriptions can be reviewed, while a single page remains
insuﬀicient for whole-work evidence. Conversely, the Blake/An Illustrated Quarterly Four Zoas bibliography is review
context: it helps explain why V ALA, or The Four Zoas requires manuscript-aware editorial handling, but it cannot itself
satisfy text or image evidence [ The Morgan Library & Museum , 2021, 2026, Blake/An Illustrated Quarterly , 2026b].
The table therefore preserves uncertainty as actionable metadata rather than forcing uncertain leads into a binary
acquired/missing label.
80

## Page 82

13 Supplement: Aggregate Image and Evidence Profiles
This public supplement reports aggregate inventory and provenance graphics. The local generator also produces all_ac
quired_images_mosaic.png and work_area_image_mosaics.png for private cache inspection. Those mosaics contain
provider-supplied images and are excluded from the public manuscript, HTML, and release archives. Their generation
does not grant redistribution rights. The public figures below contain project-authored aggregate marks rather than
acquired source images [ Drucker, 2020, Kirschenbaum, 2008].
Figure 15: Compact target-ledger overview, intended for enlargement in the accompanying PNG. Each tile records
the target’s ledger status. Text availability (T) and image associations (I) describe only its first matched source/copy
record; they do not aggregate all matching copies. Targets without a match show no text and zero image associations.
The ledger unit differs from a source/copy record and from a physical image file.
81

## Page 83

Figure 16: Archive image depth by local source record for the largest image carriers. Bars report resolved object
candidates and locally available image associations in retained metadata. Reused physical files can contribute to
multiple record-level bars; this is not an independent-image census.
82

## Page 84

Figure 17: Archive image depth aggregated by target-ledger work area. Counts describe object candidates and local
image associations attached to retained records. They do not measure completeness across museum collections or Blake’s
entire visual oeuvre.
83

## Page 85

Figure 18: Source-authority tiers attached to local metadata records. Archive-primary identifies a source relationship,
not independent verification that every extracted transcription is Blake-authored primary reading text. Reading-text
authorship remains a separate classification.
84

## Page 86

14 Supplement: Rights Matrix for Distribution and Reuse Decisions
The matrix below converts the legal distribution analysis in sec. 7 into a release checklist. It is not a permission grant.
It records the default publication posture for each artifact class and the evidence needed to change that posture.
Artifact class Rights layer
Default public-release
rule Required metadata Escalation path
Project code, tests,
scripts, and
project-authored
documentation
Project-authored
software and prose
Include under the
repository license to
the extent the
authors hold relevant
rights
Repository license,
authorship, version
Standard software
release review
Aggregate counts,
coverage tables,
checksums, source
URLs, authority
tiers, and non-image
charts
Facts, provenance,
and project-authored
arrangement
Include with citations
and provenance
Source URL,
checksum where
applicable, authority
tier, generation
command
Confirm no
embedded source
expression beyond
factual data
[Supreme Court of
the United States ,
1991]
Published
Blake-authored
underlying works
Underlying
public-domain work,
separate from edition
or file
Treat as low-risk
underlying content
only
Work title, source
edition/provider,
publication-history
note where known
Recheck item-level
publication history
for manuscripts or
uncertain editions
Project Gutenberg
fallback text
Underlying
U.S.-unrestricted
text plus Project
Gutenberg
trademark/license
wrapper
Include only
validated text with
Project Gutenberg
references handled
under the license
policy
Source URL,
checksum, validation
note,
branding/license
handling
Strip Project
Gutenberg references
when relying on the
underlying text layer,
or comply with
Project Gutenberg
conditions [ Project
Gutenberg Literary
Archive Foundation,
2026]
Wikisource fallback
text
Public-domain source
text plus
contributor/editorial
licensing
Include only with
attribution and
license continuity; do
not relicense into
MIT
Page URL, revision
or retrieval note,
attribution,
Applicable
revision-specific
license and
attribution
metadata, checksum
Use a clean
public-domain source
or preserve
Wikimedia reuse
obligations
[Wikimedia
Foundation, 2026]
William Blake
Archive TEI,
transcriptions, object
images, and bulk
mirrors
Provider text/image
terms, possible
copyright, contract,
and fair-use layers
Exclude raw files and
mirrors from the
public repository
Source URL,
object/work id,
checksum, local-cache
path excluded from
release
Seek permission,
document
venue-specific fair
use, or publish
acquisition
instructions only
[The William Blake
Archive, n.d.a]
85

## Page 87

Artifact class Rights layer
Default public-release
rule Required metadata Escalation path
Museum, HathiTrust,
Internet Archive,
Tate, British
Museum, and
catalogue leads
Provider-specific
access and catalogue
terms
Use as corroborating
metadata unless
license-compatible
files are identified
Provider URL,
checked status,
license or terms note
Verify item-level
terms before
bundling content
Generated cover and
project-authored
diagrams
Generated design
and project-authored
marks
Include with
provenance and
non-evidence label;
do not assert
exclusive copyright in
generated output
Prompt/provenance
record, generation
command,
manuscript role
Keep separate from
acquired corpus
evidence
Image mosaics and
visual supplements
made from local
source files
New layout
containing
provider-supplied
images
Exclude from general
public source release
unless cleared for the
exact venue
Input file list, source
URLs, resolution,
caption caveat,
permission or fair-use
memo
Replace with
source-compatible
thumbnails, seek
permission, or keep
as local review
artifact
The practical release rule is conservative: publish code, commands, metadata, manifests, and aggregate diagnostics;
keep expressive provider files local unless their source-specific rights layer has been resolved. This supports collections-
as-data reproducibility without treating the local evidence cache as part of the open-source license [ Candela et al. , 2023,
Wallace, 2022].
86

## Page 88

15 Supplement: Local Recovery and Integrity Evidence
The captured inventory contains 8481 files totaling 8838179463 bytes and is bound by manifest SHA-256 7b98377fe3e
3f61cf8dd8781d47e5854876c490472419df61b1a7d6689186e96. Its source scope is the pinned Archive repository and
retained Erdman API response, rather than every Blake holding. Source-inventory recovery is complete; whole-oeuvre
coverage is not_established.
The extraction ledger contains 727 source/copy documents and 540 nonempty reading transcriptions. Of those, 199
carry primary-reading labels and 341 retain unverified authorship. The retained Erdman response has 799 page records,
of which 796 are nonempty. The private projection contains 2067 records across reading, editorial-page, and XML source
planes. These planes have different meanings and are not pooled into a Blake-authored occurrence denominator.
Image recovery obtained 5975 of 6003 discovered image identifiers (99.53%). It leaves 28 unresolved identifiers. The
nominal source resolution codes are 5971 files at 300 and 4 at 100; these codes describe requested variants, not inde-
pendently measured scan resolution. The image-recovery status remains incomplete.
The retained portable backup contains 8847564800 bytes, with SHA-256 9b5004bbbab7cd6c9b68724ded9817d53c9d9a
028d018cb97a5d2e61db97235f. The prior offline restore drill verified 8481 restored files, then deliberately corrupted a
copied transcription. Verification rejected that copy before repair restored the inventoried bytes. The drill receipt has
SHA-256 fb74b73e1bfd109eb8fbdbe33018073773005fa30345acaacab2d22f143cec42 . Current integrity verification
rechecks the captured files and existing backup; it does not repeat or overwrite the historical restore experiment. This
demonstrates recoverability of the captured inventory, not recovery of unknown or unavailable source material.
Raw transcriptions, TEI/XML, images, private indexes, backup archives, and restore copies remain ignored local mate-
rials. Public deposits contain project-authored code, manuscript sources, derived aggregate evidence, and checksums.
Exact byte identity does not establish transcription accuracy, Blake authorship, scholarly completeness, or redistribution
permission [ Owens, 2018, Candela et al. , 2023].
87

## Page 89

References
Taylor Arnold and Lauren Tilton. Distant viewing: Analyzing large visual corpora. Digital Scholarship in the Human-
ities, 34(Supplement 1):i3–i16, 2019. doi: 10.1093/llc/fqz013. URL https://academic.oup.com/dsh/article/34/Supp
lement_1/i3/5694340.
B. T. Sue Atkins, Jeremy Clear, and Nicholas Ostler. Corpus design criteria. Literary and Linguistic Computing , 7(1):
1–16, 1992.
G. E. Bentley. Blake Books: Annotated Catalogues of William Blake’s Writings in Illuminated Printing, in Conventional
Typography and in Manuscript and Reprints thereof, Reproductions of His Designs, Books with His Engravings,
Catalogues, Books He Owned, and Scholarly and Critical Works about Him . Clarendon Press, Oxford, 1977.
G. E. Bentley. Blake Books Supplement . Clarendon Press, Oxford, 1995.
G. E. Bentley. Blake Records. Yale University Press, New Haven, CT, 2 edition, 2004.
Douglas Biber. Representativeness in corpus design. Literary and Linguistic Computing , 8(4):243–257, 1993.
David Bindman. The Complete Graphic Works of William Blake . Thames and Hudson, London, 1978.
Blake/An Illustrated Quarterly. Index of articles and reviews. https://bq.blakearchive.org/articles , 2026a. Journal
index consulted for Blake scholarship and article-review discovery.
Blake/An Illustrated Quarterly. A bibliography for the study of V ALA/The Four Zoas. https://blakequarterly.org
/public/journals/2/BonusFeatures/FourZoasbibliography.htm , 2026b. Work-specific bibliography consulted as
scholarship context, not corpus evidence.
David M. Blei. Probabilistic topic models. Communications of the ACM , 55(4):77–84, 2012.
David M. Blei, Andrew Y. Ng, and Michael I. Jordan. Latent dirichlet allocation. Journal of Machine Learning Research,
3:993–1022, 2003.
Katherine Bode. A World of Fiction: Digital Collections and the Future of Literary History . University of Michigan
Press, Ann Arbor, MI, 2018. doi: 10.3998/mpub.8784777.
Christine L. Borgman. Big Data, Little Data, No Data: Scholarship in the Networked World . MIT Press, Cambridge,
MA, 2015. doi: 10.7551/mitpress/9963.001.0001.
Geoffrey C. Bowker and Susan Leigh Star. Sorting Things Out: Classification and Its Consequences . MIT Press,
Cambridge, MA, 1999.
Lou Burnard. What Is the Text Encoding Initiative? How to Add Intelligent Markup to Digital Resources . OpenEdition
Press, Marseille, 2014. doi: 10.4000/books.oep.426.
Martin Butlin. The Paintings and Drawings of William Blake . Yale University Press, New Haven, CT, 1981.
Gustavo Candela, Nele Gabriëls, Sally Chambers, Thuy-An Pham, Sarah Ames, Neil Fitzgerald, Katrine Hofmann,
Victor Harbo, Abigail Potter, Meghan Ferriter, Eileen Manchester, Alba Irollo, Ellen Van Keer, Mahendra Mahey,
Olga Holownia, and Milena Dobreva. A checklist to publish collections as data in glam institutions, 2023. URL
https://arxiv.org/abs/2304.02603. Collections-as-data checklist consulted for rights-aware release architecture.
Kendal Crawford and Michelle Levy. The william blake archive. RIDE: A Review Journal for Digital Editions and
Resources, 6, 2017. doi: 10.18716/ride.a.5.5. URL https://ride.i-d-e.de/issues/issue-5/the-william-blake-archive/ .
Steven J. DeRose, David G. Durand, Elli Mylonas, and Allen H. Renear. What is text, really? Journal of Computing
in Higher Education , 1(2):3–26, 1990.
Johanna Drucker. Humanities approaches to graphical display. Digital Humanities Quarterly , 5(1), 2011. doi: 10.637
44/r4ysrh7ae534.
Johanna Drucker. Visualization and Interpretation: Humanistic Approaches to Display . MIT Press, Cambridge, MA,
2020. ISBN 978-0-262-04473-8. doi: 10.7551/mitpress/12523.001.0001. URL https://mitpress.mit.edu/97802620447
38/visualization-and-interpretation/.
88

## Page 90

Morris Eaves. Behind the scenes at the william blake archive: Collaboration takes more than e-mail. Journal of
Electronic Publishing, 3(2), 1997. doi: 10.3998/3336451.0003.202.
Morris Eaves, Robert N. Essick, and Joseph Viscomi. The william blake archive. https://www.blakearchive.org/, 1996.
Editors. Online digital edition of Blake’s illuminated books and works.
Morris Eaves, Robert N. Essick, Joseph Viscomi, and Matthew G. Kirschenbaum. Standards, methods, and objectives
in the william blake archive: A response. The Wordsworth Circle , 30(3):135–144, 1999. doi: 10.1086/TWC24044108.
Morris Eaves, Robert N. Essick, and Joseph Viscomi. The william blake archive: The medium when the millennium
is the message. In Tim Fulford, editor, Romanticism and Millenarianism , pages 219–233. Palgrave Macmillan, New
York, 2002. doi: 10.1057/9780230107205_14.
David V. Erdman. The Complete Poetry and Prose of William Blake . Anchor Books, New York, NY, newly revised
edition, 1988. Commentary by Harold Bloom.
Robert N. Essick. A finding list of reproductions of blake’s art. Blake: An Illustrated Quarterly , 3(2), 1969. URL
https://bq.blakearchive.org/3.2.essick.
Robert N. Essick. William Blake, Printmaker . Princeton University Press, Princeton, NJ, 1980.
European Parliament and Council of the European Union. Directive 2006/116/ec on the term of protection of copyright
and certain related rights. https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32006L0116 , 2006.
European Union copyright-term directive consulted for life-plus-70 and related-rights analysis.
European Parliament and Council of the European Union. Directive (eu) 2019/790 on copyright and related rights in
the digital single market. https://eur-lex.europa.eu/eli/dir/2019/790/oj/eng , 2019. Article 14 consulted for faithful
reproductions of public-domain visual art.
Julia Flanders and Fotis Jannidis. Data modeling in a digital humanities context: An introduction. In Julia Flanders
and Fotis Jannidis, editors, The Shape of Data in Digital Humanities: Modeling Texts and Text-based Resources ,
pages 3–25. Routledge, London, 2019. doi: 10.4324/9781315552941-1. URL https://www.taylorfrancis.com/chapte
rs/edit/10.4324/9781315552941-1/data-modeling-digital-humanities-context-julia-flanders-fotis-jannidis . Copyright
year 2019; publisher-deposited online publication date 2018.
Rudolf Flesch. A new readability yardstick. Journal of Applied Psychology , 32(3):221–233, 1948. doi: 10.1037/h0057532.
Ashley Reed Fox and Rachel Lee Fletcher. All Relate to Art: The william blake archive and its web of relations. Digital
Humanities Quarterly , 12(1), 2018. doi: 10.63744/2vvrwm5cmc2g. URL https://www.digitalhumanities.org/dhq/vo
l/12/1/000372/000372.html.
Gavin Greif, Niclas Griesshaber, and Robin Greif. Multimodal LLMs for OCR, OCR post-correction, and named entity
recognition in historical documents, 2025. URL https://arxiv.org/abs/2504.00414. Preprint.
HathiTrust Digital Library. Hathitrust catalog record: William blake. https://catalog.hathitrust.org/Record/102153
075, 2026. Bibliographic source used for corpus-source checks.
C. J. Hutto and Eric Gilbert. V ADER: A parsimonious rule-based model for sentiment analysis of social media text.
Proceedings of the International AAAI Conference on Web and Social Media , 8(1):216–225, 2014. doi: 10.1609/icws
m.v8i1.14550.
Internet Archive. Internet archive advanced search. https://archive.org/advancedsearch.php , 2026. Search endpoint
used for Blake source discovery checks.
Matthew L. Jockers. Macroanalysis: Digital Methods and Literary History . University of Illinois Press, Urbana, IL,
2013. ISBN 978-0-252-07907-8.
Steven E. Jones. The william blake archive: An overview. Literature Compass, 3(3):409–416, 2006. doi: 10.1111/j.1741-
4113.2006.00331.x.
Evgeny Kim and Roman Klinger. A survey on sentiment and emotion analysis for computational literary studies.
Zeitschrift für digitale Geisteswissenschaften , 2019.
89

## Page 91

Matthew G. Kirschenbaum. Mechanisms: New Media and the Forensic Imagination . MIT Press, Cambridge, MA, 2008.
ISBN 978-0-262-11311-3. doi: 10.7551/mitpress/7393.001.0001. URL https://mitpress.mit.edu/9780262113113/mec
hanisms/.
Lauren Klein, Meredith Martin, André Brock, Maria Antoniak, Melanie Walsh, Jessica Marie Johnson, Lauren Tilton,
and David Mimno. Provocations from the humanities for generative AI research, 2025. URL https://arxiv.org/abs/
2502.19190. arXiv preprint, originally submitted 2025; revised version 2026. Not a final peer-reviewed publication.
Lauren F. Klein. The image of absence: Archival silence, data visualization, and james hemings. American Literature,
85(4):661–688, 2013. doi: 10.1215/00029831-2367310.
Martin Klein, Herbert Van de Sompel, Robert Sanderson, Harihar Shankar, Lyudmila Balakireva, Ke Zhou, and Richard
Tobin. Scholarly context not found: One in five articles suffers from reference rot. PLOS ONE , 9(12):e115253, 2014.
doi: 10.1371/journal.pone.0115253.
Jinhao Li, Jianzhong Qi, Soyeon Caren Han, and Eun-Jung Holden. MUSEKG: A knowledge graph over museum
collections, 2025. URL https://arxiv.org/abs/2511.16014. Preprint.
Jason Mazzone. Copyfraud. New York University Law Review , 81:1026–1100, 2006. URL https://www.nyulawreview
.org/wp-content/uploads/2018/08/NYULawReview-81-3-Mazzone.pdf .
Philip M. McCarthy and Scott Jarvis. MTLD, vocd-d, and HD-D: A validation study of sophisticated approaches to
lexical diversity assessment. Behavior Research Methods , 42:381–392, 2010. doi: 10.3758/brm.42.2.381.
Willard McCarty. Humanities Computing . Palgrave Macmillan, Basingstoke, 2005. ISBN 978-1-4039-3504-5. doi:
10.1057/9780230504219.
Tony McEnery and Andrew Hardie. Corpus Linguistics: Method, Theory and Practice . Cambridge University Press,
Cambridge, 2012.
Jerome J. McGann. The Textual Condition . Princeton University Press, Princeton, NJ, 1991.
D. F. McKenzie. Bibliography and the Sociology of Texts . Cambridge University Press, Cambridge, 1999. doi: 10.101
7/cbo9780511483226.
W. J. T. Mitchell. Picture Theory: Essays on Verbal and Visual Representation . University of Chicago Press, Chicago,
IL, 1994.
Luc Moreau and Paul Groth. PROV-Overview: An overview of the PROV family of documents. https://www.w3.org
/TR/prov-overview/, 2013. W3C Working Group Note.
Franco Moretti. Network theory, plot analysis. New Left Review , 68:80–102, 2011.
Mark E. J. Newman. Networks: An Introduction . Oxford University Press, Oxford, 2010.
Trevor Owens. The Theory and Craft of Digital Preservation . Johns Hopkins University Press, Baltimore, MD, 2018.
ISBN 978-1-4214-2697-6. doi: 10.1353/book.62324.
Thomas Padilla, Laurie Allen, Hannah Frost, Sarah Potvin, Elizabeth Russey Roke, and Stewart Varner. Always already
computational: Collections as data: Final report. Technical report, University of Nebraska–Lincoln Digital Commons,
2019a. URL https://digitalcommons.unl.edu/scholcom/181/ . Final report of the Always Already Computational:
Collections as Data project.
Thomas Padilla, Laurie Allen, Hannah Frost, Sarah Potvin, Elizabeth Russey Roke, and Stewart Varner. Santa barbara
statement on collections as data. https://zenodo.org/records/3066209 , 2019b. Version 2 of the Always Already
Computational collections-as-data statement.
Bo Pang and Lillian Lee. Opinion mining and sentiment analysis. Foundations and Trends in Information Retrieval , 2
(1–2):1–135, 2008. doi: 10.1561/1500000011.
Eitan Adam Pechenick, Christopher M. Danforth, and Peter Sheridan Dodds. Characterizing the google books corpus:
Strong limits to inferences of socio-cultural and linguistic evolution. PLOS ONE , 10(10):e0137041, 2015. doi: 10.137
1/journal.pone.0137041.
90

## Page 92

Roger D. Peng. Reproducible research in computational science. Science, 334(6060):1226–1227, 2011. doi: 10.1126/sc
ience.1213847.
Grischka Petri. The public domain vs. the museum: The limits of copyright and reproductions of two-dimensional
works of art. Journal of Conservation and Museum Studies , 12(1):8, 2014. doi: 10.5334/jcms.1021217. URL
https://jcms-journal.com/articles/10.5334/jcms.1021217.
Michael Phillips. William Blake: The Creation of the Songs . British Library, London, 2000.
Andrew Piper. Enumerations: Data and Literary Study . University of Chicago Press, Chicago, IL, 2018. ISBN
978-0-226-56889-8. doi: 10.7208/chicago/9780226568898.001.0001.
Kenneth M. Price. Edition, project, database, archive, thematic research collection: What’s in a name? Digital
Humanities Quarterly , 3(3), 2009. doi: 10.63744/jjfxfkv55guw.
Project Gutenberg. Project gutenberg: William blake. https://www.gutenberg.org/ebooks/author/295 , 2026. Author
page used for text-source corroboration.
Project Gutenberg Literary Archive Foundation. The project gutenberg license. https://www.gutenberg.org/policy/lic
ense.html, 2026. License and trademark terms consulted for fallback text distribution.
Stephen Ramsay. Reading Machines: Toward an Algorithmic Criticism . University of Illinois Press, Urbana, IL, 2011.
ISBN 978-0-252-03641-5. URL https://www.press.uillinois.edu/books/?id=p079511.
Ashley Reed. Managing an established digital humanities project: Principles and practices from the twentieth year
of the william blake archive. Digital Humanities Quarterly , 8(1), 2014. doi: 10.63744/w45pfs4bazky. URL https:
//www.digitalhumanities.org/dhq/vol/8/1/000174/000174.html.
Luis Rei, Dunja Mladenić, Mareike Dorozynski, Franz Rottensteiner, Thomas Schleider, Raphaël Troncy, Jorge Sebastián
Lozano, and Mar Gaitán Salvatella. Multimodal metadata assignment for cultural heritage artifacts. Multimedia
Systems, 29:847–869, 2023. doi: 10.1007/s00530-022-01025-2. URL https://arxiv.org/abs/2406.00423 . Published
article; later author preprint is arXiv:2406.00423.
Geoffrey Rockwell and Stéfan Sinclair. Hermeneutica: Computer-Assisted Interpretation in the Humanities . MIT Press,
Cambridge, MA, 2016. ISBN 978-0-262-03435-9. URL https://mitpress.mit.edu/9780262034359/hermeneutica/.
Patrick Sahle. What is a scholarly digital edition? In Matthew James Driscoll and Elena Pierazzo, editors, Digital
Scholarly Editing: Theories and Practices , pages 19–40. Open Book Publishers, Cambridge, 2016. doi: 10.11647/O
BP.0095.02. URL https://www.openbookpublishers.com/books/10.11647/obp.0095/chapters/10.11647/obp.0095.02.
Geir Kjetil Sandve, Anton Nekrutenko, James Taylor, and Eivind Hovig. Ten simple rules for reproducible computational
research. PLOS Computational Biology , 9(10):e1003285, 2013. doi: 10.1371/journal.pcbi.1003285.
Arfon M. Smith, Daniel S. Katz, and Kyle E. Niemeyer. Software citation principles. PeerJ Computer Science , 2:e86,
2016. doi: 10.7717/peerj-cs.86.
Stian Soiland-Reyes, Peter Sefton, Mercè Crosas, Leyla Jael Castro, Frederik Coppens, José M. Fernández, Daniel
Garijo, et al. Packaging research artefacts with RO-Crate. Data Science, 5(2):97–138, 2022. doi: 10.3233/DS-210053.
Supreme Court of the United States. Feist publications, inc. v. rural telephone service co., 499 u.s. 340. https:
//tile.loc.gov/storage-services/service/ll/usrep/usrep499/usrep499340/usrep499340.pdf , 1991. Case consulted for
originality, facts, and compilation-protection limits.
Tate. William blake. https://www.tate.org.uk/art/artists/william-blake-39 , 2026. Artist catalogue page used for
visual-source corroboration.
TEI Consortium. TEI P5: Guidelines for electronic text encoding and interchange. https://tei-c.org/guidelines/p5/ ,
2026. Versioned guidelines for electronic text encoding.
The British Museum. British museum collection search: William blake. https://www.britishmuseum.org/collection/s
earch?agent=William+Blake, 2026. Visual and catalogue corroboration source.
91

## Page 93

The Morgan Library & Museum. William blake’s pickering manuscript. https://www.themorgan.org/collection/william-
blake/pickering-manuscript , 2021. Source-owned digital facsimile and context page consulted as a manual-review
lead for the Pickering Manuscript.
The Morgan Library & Museum. MA 2879, pp. 16–17, auguries of innocence. https://www.themorgan.org/collection
/william-blake/pickering-manuscript/13, 2026. Page-level Pickering Manuscript record consulted as a manual-review
negative-control lead.
The William Blake Archive. William blake archive: Conditions of use. https://terpconnect.umd.edu/~mgk/blake/c
onditions.html, n.d.a. Historical static conditions page; publication date not established. Consulted 2026-10-23; not
treated as a verified current permission grant.
The William Blake Archive. Copyright and permissions. https://blakearchive.org/staticpage/permissionsNEW, n.d.b.
Current permissions route; unavailable during the 2026-10-23 publication check. No permission grant inferred.
Fiona J. Tweedie and R. Harald Baayen. How variable may a constant be? measures of lexical richness in perspective.
Computers and the Humanities , 32:323–352, 1998.
UK Intellectual Property Oﬀice. Copyright notice: Duration of copyright (term). https://www.gov.uk/governmen
t/publications/copyright-notice-duration-of-copyright-term/copyright-notice-duration-of-copyright-term , 2021.
Guidance consulted for UK duration and pre-1989 unpublished-work rules.
Ted Underwood. Distant Horizons: Digital Evidence and Literary Change . University of Chicago Press, Chicago, IL,
2019. ISBN 978-0-226-61297-3. doi: 10.7208/chicago/9780226612973.001.0001.
United States Court of Appeals for the Ninth Circuit. Nguyen v. barnes & noble inc., 763 f.3d 1171. https://cdn.ca9.
uscourts.gov/datastore/opinions/2014/08/18/12-56628.pdf, 2014. Browsewrap case consulted for online terms notice
and assent.
United States Court of Appeals for the Second Circuit. Specht v. netscape communications corp., 306 f.3d 17. https:
//law.justia.com/cases/federal/appellate-courts/F3/306/17/642323/ , 2002. Online-assent case consulted for notice
and assent limits.
United States Court of Appeals for the Second Circuit. Authors guild, inc. v. hathitrust, 755 f.3d 87. https://law.ju
stia.com/cases/federal/appellate-courts/ca2/12-4547/12-4547-2014-06-10.html , 2014. Fair-use case consulted for
search and accessibility analogies.
United States Court of Appeals for the Second Circuit. Authors guild v. google, inc., 804 f.3d 202. https://law.justia.c
om/cases/federal/appellate-courts/ca2/13-4829/13-4829-2015-10-16.html , 2015. Fair-use case consulted for search,
indexing, and snippet-display analogies.
United States District Court for the Southern District of New York. Bridgeman art library, ltd. v. corel corp., 36 f.
supp. 2d 191. https://law.justia.com/cases/federal/district-courts/FSupp2/36/191/2413183/ , 1999. Case consulted
for U.S. originality treatment of exact photographic copies of public-domain two-dimensional art.
U.S. Copyright Oﬀice. Chapter 1: Subject matter and scope of copyright. https://www.copyright.gov/title17/92chap
1.html, 2026a. Section 107 consulted for the use-specific fair-use factors; accessed 2026-10-23.
U.S. Copyright Oﬀice. Chapter 3: Duration of copyright. https://www.copyright.gov/title17/92chap3.html , 2026b.
Title 17 duration provisions consulted for publication legal-risk analysis.
U.S. Copyright Oﬀice. Circular 15a: Duration of copyright. https://www.copyright.gov/circs/circ15a.pdf , 2026c.
Revised April 2026; consulted for public-domain and pre-1978 duration rules.
Herbert Van de Sompel, Michael L. Nelson, and Robert Sanderson. HTTP framework for time-based access to resource
states–memento. Technical Report RFC 7089, RFC Editor, 2013.
Joseph Viscomi. Blake and the Idea of the Book . Princeton University Press, Princeton, NJ, 1993. ISBN 978-0-691-
06962-4.
Joseph Viscomi. Digital facsimiles: Reading the william blake archive. Computers and the Humanities , 36(1):27–48,
2002.
92

## Page 94

Andrea Wallace. A culture of copyright: A scoping study on open access to digital cultural heritage collections in the
uk. Technical report, Towards a National Collection, 2022. URL https://zenodo.org/records/6242611.
Scott B. Weingart. Demystifying networks. Journal of Digital Humanities , 1(1), 2011.
Melvin Wevers and Thomas Smits. The visual digital turn: Using neural networks to study historical images. Digital
Scholarship in the Humanities , 35(1):194–207, 2020. doi: 10.1093/llc/fqy085. URL https://academic.oup.com/dsh/a
rticle/35/1/194/5296356.
Roger Whitson and Jason Whittaker. William Blake and the Digital Humanities: Collaboration, Participation, and
Social Media. Routledge, New York, NY, 2013. doi: 10.4324/9780203078068.
Wikimedia Foundation. Wikimedia foundation terms of use. https://foundation.wikimedia.org/wiki/Policy:Terms_of
_Use, 2026. Terms consulted for Wikisource contribution and reuse licensing.
Wikisource contributors. Author: William blake. https://en.wikisource.org/wiki/Author:William_Blake, 2026. Public
text index used for source corroboration.
Matthew Wilkens. Digital humanities and its application in the study of literature and culture. Comparative Literature,
67(1):11–20, 2015. doi: 10.1215/00104124-2861911.
Mark D. Wilkinson, Michel Dumontier, IJsbrand Jan Aalbersberg, et al. The F AIR guiding principles for scientific data
management and stewardship. Scientific Data , 3:160018, 2016. doi: 10.1038/sdata.2016.18.
Greg Wilson, D. A. Aruliah, C. Titus Brown, Neil P. Chue Hong, Matt Davis, Richard T. Guy, Steven H. D. Haddock,
et al. Best practices for scientific computing. PLOS Biology, 12(1):e1001745, 2014. doi: 10.1371/journal.pbio.1001745.
Yale Library. William blake: Collection lists. https://guides.library.yale.edu/blake/blakeatyale , 2026. Institutional
collection guide consulted as corroborating source-discovery context.
Yang Zhang, Nada Mimouni, Jean-Claude Moissinac, and Fayçal Hamdi. Multimodal cultural heritage knowledge graph
extension with language and vision models, 2026. URL https://arxiv.org/abs/2605.17669. Preprint.
93
