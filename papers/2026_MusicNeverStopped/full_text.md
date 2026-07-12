# Full Text: The Music Never Stopped: A Grateful Data Compendium with a Category-Theoretic Interpretation

> Extracted from `Friedman_2026_Music_2d42bfd0.pdf`

---

## Page 1

The Music Never Stopped: A Grateful Data Compendium with a
Category-Theoretic Interpretation
Daniel Ari Friedman
Active Inference Institute
FractAI
daniel@activeinference.institute
ORCID: 0000-0001-6232-9096
2026-05-31
2026-05-31
Contents
1
Abstract
3
2
Introduction
4
2.1
What we mean by “the music never stopped” . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
4
2.2
Sources surveyed . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
4
2.3
What is in this repository . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5
2.4
Related work . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5
2.5
What is not in this repository . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5
3
Methodology
6
3.1
Schema
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
3.1.1
Data dictionary (core entities)
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
3.2
Source ingestion
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
3.2.1
Contextual-source layer
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
3.3
Integration
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
3.4
Committed compendium (data/archival/) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
3.5
Analyses and validation
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
3.5.1
First-principles claim ledger . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
3.5.2
Provenance, external pointers, and reviewer artifacts . . . . . . . . . . . . . . . . . . . . . . . .
8
4
Category-theoretic interpretation
10
4.1
Why category theory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
4.2
The date poset and the show category . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
4.3
The setlist functor
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
4.4
The lineup functor and the active-roster presheaf . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
4.5
Performances as spans, with fibers over shows and songs . . . . . . . . . . . . . . . . . . . . . . . . . .
11
4.6
Audio enrichment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
11
4.7
Coproducts and colimits . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
11
4.8
Natural transformations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
11
4.9
Representability (Yoneda) over the date poset . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12
4.10 What the construction buys . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12
5
Results on the compendium
13
5.1
Scope and completeness . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
13
5.2
Top-line counts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
13
5.3
Statistical shape and concentration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
13

## Page 2

5.4
Temporal activity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
18
5.5
Repertoire frequency and co-occurrence
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
18
5.6
Markov structure of setlist order
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
5.7
Category-theoretic cardinalities . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
5.8
Composers, eras, and personnel . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
24
5.9
Reception, citations, and recordings
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
24
5.10 Lyric pointers and segues
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
24
5.11 Geography, set position, tours, and bustouts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
29
5.12 Composite views . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
29
5.13 Claim evidence map
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
29
5.14 Limitations and threats to validity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
31
5.15 Honest framing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
34
6
Segue and transition structure
38
6.1
Two notions of “what follows what”
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
38
6.2
The most frequent segues
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
38
6.3
Segue hubs
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
38
6.4
What this does and does not establish . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
38
7
Conclusion
39
8
Reproducibility
40
8.1
Single-command reproduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
40
8.2
Manuscript PDF (template renderer) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
40
8.3
CLI
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
40
8.4
What’s bound to what . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
41
8.5
No mocks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
42
8.6
Determinism
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
42
9
The executable honesty boundary
43
9.1
What the boundary refuses
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
43
9.2
Why this exists . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
43
9.3
Binding to tests . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
43
9.4
Verdict . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
43
9.5
Licensing and provenance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
44
9.6
Out of scope
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
44
10 References
45
2

## Page 3

1
Abstract
We present a modular, citation-bound data compendium for the Grateful Dead universe — shows, songs, perfor-
mances, personnel timelines, venues, recordings, and reception — and a category-theoretic interpretation of the
performance graph. The work is grounded in the archival reality that Grateful Dead history is both institutional and
participatory: UCSC’s Grateful Dead Archive and the Internet Archive collection preserve formal and community
records [University of California, Santa Cruz University Library, 2025, int, Internet Archive Help Center, 2018],
while taping and trading scholarship shows why setlists and recording metadata are cultural evidence, not merely fan
trivia [Meriwether, 2015, Wallace, 2009]. The surrounding source dossier also binds the non-quantitative historical
frame – formation and Acid Test context, Wall of Sound engineering, live recording/liveness scholarship, Deadhead
sociology, studio-era reception, and public recognition – to checked sources rather than to folklore alone [Grateful
Dead, Weir, 2011, Smithsonian Institution, 2024, McIntosh Laboratory, 2025, Brackett, 2023, Adams and Sardiello,
2000, Rock and Roll Hall of Fame, 1994, Recording Academy, 2007, John F. Kennedy Center for the Performing
Arts, 2024]. The compendium integrates nine primary sources (Setlist.fm [set, a], The SetList Program [set, b],
the Mark Leone CMU setlist archive [Leone, b, Gorstein], GDsets [gds, a,b], gdshowsdb [Smith, git], the Internet
Archive Live Music Archive [int, fif], the Alex Allan / whitegum lyric finder [Allan, Leone, a], the oﬀicial band site
[dea], and Wikipedia [wik, b,a]) with four reference sources (Britannica [bri], the lineup-changes guide [ucr], Dodd
and Trist’s The Complete Annotated Grateful Dead Lyrics [Dodd and Trist, 2005], and the Grateful Stats front-end
[gra]) and secondary corpora and community discussions [Thered, Blance, maximinus, red, a,b,c,d]. Each source is
parsed by an independently testable reference module written against the documented record shape; the commit-
ted compendium under data/archival/ is the dataset reported here (3341 ingested shows (gdshowsdb + truckin
gap-fill; community literature estimates about 2318 canonical concerts), 645 songs, 912 venues, 40757 performance
rows). A runtime completeness audit and figure-validation gate certify referential integrity and non-degenerate out-
puts on every pipeline run. Integration is a deterministic, sort-keyed merge over canonical slugs; registered figures
also emit CSV/JSON data tables, and a first-principles claim ledger classifies each major result by irreducible input,
hard constraint, assumption, validation artifact, and interpretation limit. Exploratory repertoire/uncertainty pan-
els are labelled as pattern-discovery rather than causal inference. We then exhibit four small but real categorical
constructions, situated against transformational and categorical music-theory precedents [Lewin, 2007, Padi et al.,
2017, Popoff and Andreatta, 2023]: a poset category of dates, a discrete category of shows, a monotone cumulative
setlist functor and lineup functor from dates into sets, and a span representation that takes each performance to
be the apex of a span between its show and its song. Wide pullbacks over a fixed show recover the show’s setlist;
wide pullbacks over a fixed song recover the song’s performance history. The active-band roster, by contrast, is a
non-monotone presheaf on the date poset — a categorical formalization of the familiar fact that members come and
go. The artefacts in this paper come from the committed archival snapshot; all source-ingestion modules are written
against the real source shape so that scripts/00_fetch_sources.py --online --write-archival refreshes the
full snapshot.
3

## Page 4

2
Introduction
2.1
What we mean by “the music never stopped”
The Grateful Dead performed roughly two and a half thousand concerts between 1965 and 1995. The public record
of those concerts — setlists, recordings, ticket stubs, member rosters, composer credits, release histories, and decades
of fan commentary — is one of the most extensively documented bodies of live performance in popular-music history.
It is also unusually hybrid. UCSC’s Grateful Dead Archive gives the band a formal institutional home [University of
California, Santa Cruz University Library, 2025], while the Internet Archive collection and Deadhead taping culture
preserve the community-built sound archive and its metadata [Internet Archive Help Center, 2018, Meriwether, 2015,
Wallace, 2009]. The record is fragmented across primary databases, archival corpora, reference works, and a long
tail of community spreadsheets and forum threads [red, a,c,d]. This paper introduces The Music Never Stopped: a
reproducible, citation-bound compendium that integrates the primary sources into a single schema, exposes them
to standard data-analysis machinery, and exhibits a small but genuine category-theoretic structure latent in the
performance graph.
2.2
Sources surveyed
We organize the cited landscape into four layers.
Primary setlist sources. Setlist.fm publishes a crowd-curated, API-backed register of every Grateful Dead show
[set, a]. The SetList Program at setlists.net covers 1965–1995 with an interactive interface [set, b]. The Mark
Leone CMU archive [Leone, b], derived from the Jerry Stratton database, is the ancestor of many community scrapes;
Noah Gorstein has converted the abandoned HTML into an open SQLite database [Gorstein]. GDsets combines
setlists with ticket-stub and stage-pass images [gds, a,b]. The gdshowsdb repository ships a relational schema and a
Ruby gem [Smith]; the GitHub topic gratefuldead is the meta-index that links these and other resources [git].
Primary lyric and song-attribution sources. Mark Leone’s lyric index at CMU [Leone, a] points to the Stratton
database via FTP. Alex Allan’s whitegum.com is the canonical lyric and song finder for every song the Dead played,
with composer/lyricist attribution and per-song performance data [Allan]. Dodd and Trist’s The Complete Annotated
Grateful Dead Lyrics supplies the authoritative interpretive and annotation context for lyric studies [Dodd and Trist,
2005]. We cite it as an external authority and store only pointer metadata; no lyric text is bundled. Hunter’s own
retrospective account and community discussion are used only as context for songwriter roles, never as an override
of the structured composer/lyricist fields [Greene, 2015, red, b].
Personnel, discography, recording, and reception sources. The oﬀicial band site lists members and roles [dea].
Wikipedia’s Grateful Dead entry [wik, b] and discography [wik, a] anchor the biographical timeline; Britannica frames
the wider cultural context [bri]. Ultimate Classic Rock’s lineup-changes guide [ucr] provides a chronological narrative
of personnel transitions. The Internet Archive’s Live Music Archive supplies recording metadata for the bulk of the
live corpus [int], and its Grateful Dead collection policy explains the special access and metadata posture of those
recordings [Internet Archive Help Center, 2018]. The fifteen-songs-dataset curates 2617 soundboard recordings of
15 songs for music-information-retrieval research [fif], while Wang et al.’s setlist-segmentation paper gives a broader
MIR frame for why live setlist identification is non-trivial [Wang et al., 2014].
jerryPycia provides a Python
query library over Dead show data [Blance]; the grateful-dead-reviews corpus collects long-form fan reviews
[maximinus]. The gratefulstats.com front-end aggregates show/tune/venue statistics [gra]. The gratefuldata
tutorial demonstrates an ETL pipeline using the Internet Archive together with ASCAP ACE composer data [Thered].
The compendium draws composer/lyricist attributions from these sources and encodes them in data/archival/so
ngs.json.
Historical, technical, and interpretive context. The supplied enriched bibliography is useful as a discovery
map, but the map is not itself evidence. Each durable topic is therefore rebound to checked source families: the
oﬀicial dead.net biography and FoundSF’s Bob Weir oral-history page for formation and Acid Test context [Grateful
Dead, Weir, 2011], Smithsonian and UCSC for institutional archive status [Smithsonian Institution, 2024, University
of California, Santa Cruz University Library, 2025], McIntosh for the Wall of Sound hardware [McIntosh Laboratory,
2025], Marshall, JSTOR Daily, Meriwether, Wallace, and the Internet Archive policy page for the tape-trading
and sound-archive ecosystem [Marshall, 2003, Daily, 2015, Meriwether, 2015, Wallace, 2009, Internet Archive Help
Center, 2018], Brackett’s Live Dead for liveness and recorded-performance scholarship [Brackett, 2023], Adams and
Sardiello for Deadhead sociology [Adams and Sardiello, 2000], Dodd and Weiner for the bibliographic field map
[Dodd and Weiner, 1997], Britannica and Americana Highways for narrow biographical and studio-reception context
[Encyclopaedia Britannica, Highways, 2020], and oﬀicial public-recognition sources for later institutional status [Rock
4

## Page 5

and Roll Hall of Fame, 1994, Recording Academy, 2007, John F. Kennedy Center for the Performing Arts, 2024].
Community reconstructions such as touring revenue estimates are cited only as labelled business-history context, not
as compendium measurements [Seconds, 2016].
2.3
What is in this repository
We ship a committed archival compendium under data/archival/ that drives every analysis and category-theoretic
claim in this paper end-to-end, plus a parser for each cited source so that refreshing the snapshot is a matter of
running the same code with online flags.
2.4
Related work
Prior Grateful Dead data efforts are mostly single-source or single-purpose. Community setlist databases and the
gdshowsdb / truckin-through-time projects [Smith, Gorstein] assemble the raw show record; aggregators such as
Grateful Stats [gra] and community spreadsheets and forums [red, c,a] surface frequency rankings; and query libraries
such as jerryPycia [Blance] and the grateful-data tutorial [Thered] expose one source programmatically. Archive
and popular-music studies add a second frame: the Dead’s sound record is co-produced by band, archive, tapers,
uploaders, and curators rather than handed down by a single authority [Wallace, 2009, Meriwether, 2015, Internet
Archive Help Center, 2018, Brackett, 2023]. Sociological work on Deadheads, bibliographic scholarship, and tape-
trader studies explain why this record is also a community institution rather than simply a discography [Adams and
Sardiello, 2000, Dodd and Weiner, 1997, Marshall, 2003, Daily, 2015].
This compendium differs on two axes.
It is integration-first: primary sources are reconciled on canonical slugs
into one immutable, citation-bound schema with a runtime honesty boundary and completeness/figure-validation
probes. It is also structure-first: the performance record is read through small but mechanically checked categorical
constructions (functors, spans, colimits, a date-poset Yoneda statement) rather than treated only as a frequency
table. The music-theory lineage is Lewin’s transformational shift from static objects to relations and transformations
[Lewin, 2007], with newer categorical music work showing how such networks can be formalized diagrammatically
[Padi et al., 2017, Popoff and Andreatta, 2023]. Our contribution is a concrete, reproducible instantiation on a real
performance corpus, with every quantitative or categorical claim bound to code.
2.5
What is not in this repository
We do not bundle lyric text — full lyrics are copyrighted. The compendium stores songs as titled records with
composer and lyricist attribution; the semantic layer (motifs, themes, annotations) is read against external indices
such as Alex Allan’s finder and Dodd’s annotated lyrics [Allan, Dodd and Trist, 2005]. We do not bundle audio. The
audio-enriched category in §3 is a structural abstraction over similarity weights; concrete weights are produced by
an external pipeline against the fifteen-songs-dataset [fif].
5

## Page 6

3
Methodology
3.1
Schema
The compendium primitive is a small frozen-dataclass schema. Every entity validates its inputs in __post_init__;
every primary key is computed by a canonical-slug function so that joins across sources reduce to dictionary lookups.
The nine entity types are Show, Venue, Person, Song, Performance, Recording, Release, Citation, and Lineup;
their fields and invariants are documented in src/models.py.
Two canonical-slug rules suﬀice for source-agnostic identity:
• a song slug is the ASCII-folded, punctuation-stripped slug of its title;
• a show slug is YYYY-MM-DD@<venue-slug>.
These deterministic functions absorb the cross-source-naming variance that would otherwise require a manual alias
table.
3.1.1
Data dictionary (core entities)
The field-level contract for the entities that carry the quantitative claims; the authoritative definition with all
invariants is src/models.py.
Entity
Key
Principal fields
Notes
Show
slug =
YYYY-MM-DD@venue
date, venue_slug
one concert; venue_slug
is a foreign key into Venue
Venue
slug
name, city,
state_or_region,
country
geo coordinates live in a
venue_geo sidecar
Song
slug (slug of title)
title, composers,
lyricists,
first_performed,
last_performed, aliases
catalogue entry; need not
have been performed
Performance
(show, song, set,
position)
show_slug, song_slug,
set_number, position,
segue_into, notes
the apex of the
show↔song span
Person
slug
intervals = (start,
end, role) tuples
open interval (end=None)
means still active
Recording
slug
show_slug (or date),
source_type
Internet Archive +
curated rows
Review
—
show_slug, kind,
sentiment ∈[−1, 1],
source_url
positive sentiment requires
a source URL (honesty
check)
Citation
key
kind, url
bibliography +
references.bib
LyricPointer
song_slug
url, themes, lyricist
URL metadata only —
never lyric text
3.2
Source ingestion
Each cited source has its own reference parser at src/sources/<name>.py. Every parser exposes a single parse
function whose input is a record in the documented upstream shape (JSON payload for API sources, line-oriented
text block for HTML-derived archives, dict-of-tables for relational dumps) and whose output is in the canonical
schema. The committed snapshot in data/archival/ is built from gdshowsdb YAML, truckin-through-time SQLite
gap-fill, and curated overlays. Live HTTP fetchers are implemented in src/ingest/ and invoked by scripts/00_fe
tch_sources.py --online --archival-max. We support nine ingestion paths corresponding to the survey above:
6

## Page 7

Source
Module
Citation
Setlist.fm
sources/setlistfm.py
[set, a]
The SetList Program
sources/setlist_program.py
[set, b]
CMU / Mark Leone
sources/cmu_setlists.py
[Leone, b, Gorstein]
GDsets
sources/gdsets.py
[gds, a,b]
gdshowsdb
sources/gdshowsdb.py
[Smith]
Internet Archive LMA
sources/internet_archive.py
[int, fif]
Alex Allan / whitegum
sources/alex_allan.py
[Allan]
dead.net (oﬀicial)
sources/dead_net.py
[dea]
Wikipedia
sources/wikipedia.py
[wik, b,a]
The Internet Archive path is treated as recording metadata rather than as an audio-ingestion license. The Grateful
Dead collection has its own access and upload posture, and its item metadata can include source, taper, and transfer
fields that are valuable without bundling audio files [Internet Archive Help Center, 2018]. Likewise, the lyric layer
records URLs, lyricist attribution, and curated theme labels only; Dodd and Trist’s annotated lyrics are cited as
external interpretive context, not ingested text [Dodd and Trist, 2005].
3.2.1
Contextual-source layer
Historical context is deliberately stored as citations and prose, not as performance data. The enriched-bibliography
pass added a fourth source class: checked contextual anchors for formation, public honors, sound engineering, tape-
trading, Deadhead sociology, studio-era reception, bibliography, and live-recording scholarship [Grateful Dead, Weir,
2011, Smithsonian Institution, 2024, McIntosh Laboratory, 2025, Marshall, 2003, Brackett, 2023, Adams and Sardiello,
2000, Dodd and Weiner, 1997, Highways, 2020, John F. Kennedy Center for the Performing Arts, 2024]. These sources
can explain why a date matters, but they do not create or override Show, Performance, Recording, or Release rows.
The quality tiers are explicit:
• Data-bearing primary sources (gdshowsdb, Truckin, Setlist.fm, SetList Program, Internet Archive meta-
data) may create or corroborate schema rows through parser code.
• Pointer-only sources (whitegum, the CMU lyric index, dead.net song pages, Dodd/Trist) may supply URLs,
attributions, and themes but never bundled lyric text.
• Scholarly or institutional context (UCSC, Wallace, Brackett, Adams/Sardiello, Lewin, NIST/Padi,
Popoff/Andreatta) may support manuscript interpretation, methods scope, and related work.
• Journalism or publisher context (JSTOR Daily, Americana Highways, Billboard, Britannica, McIntosh)
may support labelled reception, biography, or technical context only.
• Community reconstruction (Reddit threads, Grateful Seconds) may support explicitly labelled background,
never quantitative findings.
No current-person, revenue, lyric, or audio claim from the source dossier is allowed into the quantitative layer unless
it is independently sourced and represented in the schema. The same rule applies to citation placement: contextual
sources may explain the provenance of a figure or timeline label, but the plotted statistics must still come from
generated reports or exported figure data.
3.3
Integration
The integration layer at src/integration/reconcile.py performs a deterministic merge.
The merge rule is
pointwise per entity type — venues join on slug, songs join on slug with union of composer/lyricist tuples and
min/max of first/last-performed dates, people join on slug with union of intervals, performances join on the four-
tuple (show, song, set, pos). The resulting Compendium is immutable and byte-stable across runs.
3.4
Committed compendium (data/archival/)
The published dataset lives under data/archival/ (3341 ingested shows (gdshowsdb + truckin gap-fill; community
literature estimates about 2318 canonical concerts), 645 songs, 912 venues, 40757 performance rows). It merges
gdshowsdb YAML, truckin-through-time gap-fill, Internet Archive LMA metadata, bibliography citations, maximinus
reviews, CMU lyric pointers, and curated personnel/releases overlays. GRATEFUL_DATA_TIER=archival selects this
load path (see src/tier.py).
7

## Page 8

3.5
Analyses and validation
The analysis layer at src/analysis/ computes descriptive statistics, co-occurrence and Markov transitions, era
and personnel timelines, geo and tour aggregates, lyric-theme frequencies from pointers, review sentiment, segue
extraction, eigenvector centrality, stationary distributions, and bustout (recurrence-gap) metrics — each as a pure
function of the Compendium.
Distributional statistics are first-class objects rather than incidental plot annotations. src/analysis/distribut
ions.py computes show-level performance-row summaries, robust percentiles, and simple concentration statistics
(Gini, top-decile share, and the number of ranked items needed to cover 50% and 80% of rows). The method is
descriptive only: it reports skew and concentration in the archival record without treating unequal song frequency,
venue recurrence, or setlist length as causal effects. Show-level performance distributions include empty-setlist shows,
because excluding them would make the setlist-completeness limitation invisible.
The same module now adds fixed-seed item-level bootstrap intervals for the song and venue concentration statistics.
These intervals are reported as exploratory uncertainty bands around descriptive metrics: the resampling unit is the
observed item count (a song’s performance count or a venue’s show count), not a claim about unobserved concerts,
fan preference, or musical causation.
Exploratory repertoire modeling lives in src/analysis/exploratory.py. It constructs an era-by-song performance-
count matrix with generic segment markers excluded, applies a centered SVD to log-count profiles, and clusters the
two-dimensional coordinates with deterministic k-means-style updates and stable tie-breaks. The output is explicitly
labelled as pattern discovery: it helps inspect era-weighted repertoire profiles, but it is not predictive, causal, or a
definitive musicological taxonomy.
The transition analysis is intentionally modest: a first-order chain over adjacent within-show performance rows plus
an explicit segue graph over source-marked segue_into edges. MIR work on full-concert setlist identification shows
why audio-level segmentation is a separate, harder task that would require different evidence and different artifacts
[Wang et al., 2014]. The current analysis report also includes a deterministic transition-sensitivity layer: predecessor-
support thresholds are summarized with and without generic segment markers, and era-specific transition summaries
are reported as descriptive diagnostics. These sensitivity rows do not rerun the permutation screen and do not create
predictive claims; they show how fragile or stable the visible transition surface is under ordinary presentation choices.
Repertoire concentration is likewise reported with sensitivity context. Beyond the fixed-seed bootstrap intervals, the
analysis report summarizes alternate top-N cuts for performance share, within-cut Gini, top-decile concentration,
and era coverage. This keeps the manuscript from treating a single top-song cutoff or heatmap width as if it were
an intrinsic property of the archive.
3.5.1
First-principles claim ledger
The methods layer now includes a claim-governance pass in src/analysis/first_principles.py. This is not a
statistical model; it is a reproducibility device. The ledger deconstructs each major manuscript claim family into
five irreducible parts: the data input, the hard constraint that must hold, the softer modeling or presentation choice,
the assumption that remains after the hard constraint is enforced, and the interpretation limit. The current build
classifies 12 claim families across 6 claim classes, naming 12 hard constraints, 12 assumptions, and 12 validation
artifacts.
This layer prevents the common failure mode in computational humanities projects: a polished visualization silently
upgrades a descriptive pattern into an explanatory claim. For example, repertoire rankings are permitted to say
what was counted after segment-marker exclusion; they are not permitted to say what the band preferred. The
transition matrix is permitted to summarize adjacent setlist rows; it is not permitted to infer musical causality. The
historical-context timeline is permitted to orient computed show counts against cited milestones; it is not permitted
to create or modify a Show row. scripts/19_first_principles_review.py serializes the ledger as output/repor
ts/first_principles_review.json and output/reports/first_principles_claims.csv. Each row also names
the manuscript section, figure filename, report key, governing test file, and claim status, so caveats can be routed
through the ledger instead of repeated as free-floating prose.
3.5.2
Provenance, external pointers, and reviewer artifacts
Source provenance is exported as a sidecar rather than written into the frozen entity dataclasses. src/provenance.py
records the source-layer families behind shows, songs, venues, performances, recordings, releases, citations, lyric
8

## Page 9

pointers, reviews, personnel rows, and computed segue edges.
The records are deliberately conservative: they
identify ingest or computation layers, not hidden row-level certainty that the schema does not store.
The external-media layer is pointer-only. src/external_manifests.py writes audio and lyric URL manifests with
compact metadata, hashes where available, and explicit policy labels. It rejects bundled audio, local paths, lyric text,
transcripts, excerpts, waveforms, and derived text fields. It also writes a small pipeline contract that names allowed
inputs and outputs for future external audio-feature and lyric-annotation workflows. This keeps future audio- or
lyric-analysis work reproducible without changing the present copyright and data-boundary claims.
Visualization lives in src/viz/: reusable panel builders (panels.py), a figure registry (figures.py), mosaic composi-
tion (compose.py), alluvial flows (alluvial.py), and non-blank figure validation (validate.py). HTML dashboards
and entity markdown pages live in src/reporting/.
The figure set is deliberately mixed: frequency and concentration views use ranked bars or cumulative-share curves;
distributions use histograms with median and high-percentile reference lines; temporal activity uses bars/lines;
co-occurrence and transition matrices use heatmaps; geography uses a size-encoded scatter map; and the com-
poser/song/era view uses an alluvial diagram. Pie charts are avoided because the same categorical comparisons are
more legible as sorted bars with counts and shares.
The contextual-source distinction also shapes the visual layer. The new historical-context timeline overlays a small
set of cited milestones on computed show counts; it is a visual orientation aid, not an ingest product. The figure
registry therefore carries its title, screen-reader alt text, caption hint, data source, statistic, exclusion rule, claim class,
draw function, and figure-data exporter together. The same metadata feeds the dashboard, raw figure-data index,
publication validator, and manuscript captions, so prose claims and plotted statistics are auditable from one registry.
A plain static explorer under output/explorer/ reuses exported show, song, venue, segue, figure, provenance, and
claim-evidence data for local filtering without adding a frontend framework. The explorer supports URL-state filters,
sortable table headers, related links, and filtered CSV download, so readers can inspect subsets without depending
on a server.
Runtime probes certify manuscript claims beyond unit tests:
• src/audit.py::audit_completeness — referential integrity (tier-aware);
• src/export.py — full raw CSV/JSON export of every entity type;
• src/analysis/first_principles.py — first-principles claim/evidence ledger for hard constraints, assump-
tions, validation artifacts, and limits;
• src/provenance.py — sidecar provenance CSV/JSON for entity/source-layer review;
• src/external_manifests.py — pointer-only external audio/lyric manifests with protected-content rejection;
• src/viz/datasets.py — raw CSV/JSON export of 34 registered figure datasets;
• src/viz/validate.py::validate_figures — every expected PNG exists and is non-degenerate.
9

## Page 10

4
Category-theoretic interpretation
4.1
Why category theory
Category theory gives us a vocabulary for structure that survives change of representation. The four constructions
below identify structure that does not depend on which source we drew the data from or on which subset of the
corpus we are looking at: they are stable in exactly the sense category theory was built to express.
The point is not to claim that setlists require category theory. The point is to make the data model’s relations
explicit. Lewin’s transformational theory famously shifts attention from musical objects to transformations among
objects [Lewin, 2007]; NIST’s music case study shows category theory used as an ontology and integration framework
for musical knowledge [Padi et al., 2017]; and recent work on hidden categories in Lewinian GIS and Klumpenhouwer
networks makes the categorical connection literal [Popoff and Andreatta, 2023]. Those works license the kind of
move being made here – a shift from objects to relations and an ontology whose diagrams can be checked – but they
do not make the Grateful Dead corpus categorically interesting by association. Our use is narrower: shows, songs,
dates, and performances form a small relational system whose laws can be checked directly against the compendium.
Scope of these claims.
Date is a thin poset category, so associativity holds automatically and the Yoneda
statement is the elementary poset case rather than a deep theorem. We therefore present the mechanized checks
below — law sampling, the colimit universal property, the Yoneda bijection, the span/functor commutation — as
encoding and sanity checks: they verify that the schema faithfully instantiates these categorical structures and that
the corresponding properties hold on the real corpus (each with a negative control that fails on broken input), not
that a non-trivial mathematical theorem about the Grateful Dead has been proved. Their value is that the data
model is demonstrably the categorical object we claim it is — which is what licenses the representation-independent
reading — not mathematical novelty or a claim that categorical music theory explains the band’s musical choices.
4.2
The date poset and the show category
Let Date be the small category whose objects are the distinct performance dates in the compendium and whose
morphisms 𝑑1 →𝑑2 exist iff 𝑑1 ≤𝑑2. Date is a thin poset category; identities and associativity hold by construction.
Let Show be the discrete category whose objects are the show slugs. Both categories’ laws are checked mechanically
in src/cattheory/categories.py::Category.check_laws. Small categories are verified exhaustively; at archival
scale the Date poset has 2312 objects, so an exhaustive associativity sweep is intractable. The checker instead
verifies every identity and samples a fixed (seeded) set of random composable triples, checking both associativity and
closure (that each sampled composite arrow is present in the table). Because the Date compose is order-preserving
string composition, its associativity holds by construction; the data-reachable defect is a non-transitively-closed arrow
table, which the sampled closure check catches with high probability. This is a regression guard — the laws hold by
construction; the check is a sampled probe of systematic corruption, not a proof — paired with a negative control
that fails on a deliberately non-closed table.
4.3
The setlist functor
Define 𝐹setlist ∶Date →Set by sending each date 𝑑to the set of song slugs ever performed on or before 𝑑, and each
arrow 𝑑1 ≤𝑑2 to the inclusion of sets. 𝐹setlist is a covariant functor because the cumulative-songs set is monotone in
𝑑. cattheory/functors.py::setlist_functor returns the explicit representation; is_monotone checks the functor
law on the compendium.
4.4
The lineup functor and the active-roster presheaf
Define 𝐹lineup ∶Date →Set by sending each date 𝑑to the set of personnel who have been in the band on or before
𝑑, and each arrow to the inclusion. 𝐹lineup is again a monotone covariant functor.
The active-roster assignment 𝑃active(𝑑) = {𝑝∣𝑝is in the band on 𝑑} is also natural, but it is not monotone: when
Pigpen leaves the band in 1972 [ucr, dea], the active set shrinks, so 𝑃active fails the covariant-functor law. It is,
however, a perfectly good presheaf: contravariantly, the “forgetting” arrow 𝑑2 →𝑑1 can be sent to the restriction of
the active set. We make both views available (setlist_functor, lineup_functor, active_lineup_presheaf) and
check that one is monotone and the other is not. The categorical content matches the historical fact: cumulative
views grow; instantaneous views oscillate.
10

## Page 11

4.5
Performances as spans, with fibers over shows and songs
For each performance 𝑝= (show, song, set, pos), define a (2-leg) span:
Show
𝜋show
←−−−𝑝
𝜋song
−−−→Song.
In cattheory/spans.py, PerformanceSpan exposes the two projections explicitly. The fiber of 𝜋show over a fixed
show 𝑠— the preimage 𝜋−1
show(𝑠), equivalently the wide pullback of all spans pinned on the left to 𝑠in the discrete
fibration sense — recovers the show’s setlist in canonical order.
Symmetrically, the fiber of 𝜋song over a fixed
song recovers the song’s performance history. We use “fiber / multi-leg span” rather than “wide pullback” in the
strict universal-property sense; the discrete-base setting collapses the distinction. This construction shows that the
performance primitive is not a derived field of the schema; it is the apex linking shows and songs, and the two
projections commute by definition with the cumulative setlist functor.
The categorical content is small but real:
• No data is lost going either direction along a span; both projections are total.
• The two wide-pullback constructions give the two natural “transposes” of the performance table — show-major
and song-major — without privileging either.
• Composition of spans (in the bicategory of spans) corresponds exactly to the relational operation “show A and
show B both played a song C” — useful for cross-show similarity measures.
4.6
Audio enrichment
Following the precedent of the fifteen-songs-dataset [fif] and the broader MIR problem of identifying and seg-
menting live concert songs [Wang et al., 2014], pairs of performances of the same song could carry a similarity weight
in [0, 1]. The category whose objects are performances and whose hom-objects are these weights is enriched over the
unit-interval monoid ([0, 1], max, 0). cattheory/enriched.py::AudioEnrichedHom captures the abstraction: the
constructor enforces the weight constraint and the same-song precondition; identity homs at weight 1.0 behave as
required in the enrichment.
We do not bundle audio. The enrichment is structural; concrete weights are expected to come from a downstream
pipeline against the fifteen-songs-dataset.
4.7
Coproducts and colimits
cattheory/colimits.py exposes two constructions: the binary coproduct of two Compendium fragments, which by
the reconciliation rules collapses into the disjoint-union compendium, and the colimit of the cumulative setlist functor
on the compendium, which equals the set of all songs ever performed in the bundled data. Crucially, the colimit
check verifies the universal property, not merely that each 𝐹(𝑑) is a subset of the union: colimit_cone_factors
confirms that a strictly larger cocone vertex admits the unique mediating map and — as a built-in negative control
— that a vertex strictly smaller than ⋃𝐹fails to receive the colimit. A check that only asserted 𝐹(𝑑) ⊆⋃𝐹would
be vacuous (true for any family); requiring the negative control to fail is what gives it teeth. The test test_copr
oduct_disjoint_union additionally asserts that splitting the shows and re-merging via the coproduct returns the
original show set — a structural reproducibility witness for the reconciliation layer itself.
4.8
Natural transformations
The cardinality assignment 𝜂_d = |F(d)| is a natural transformation F ⟹\mathrm{Card} \circ F for any mono-
tone covariant functor F : \mathbf{Date} \to \mathbf{Set}. The naturality square reduces (on this thin poset)
to |F(d_1)| \le |F(d_2)| whenever d_1 \le d_2. src/cattheory/natural.py exposes naturality_square_ho
lds and the two concrete instances setlist_cardinality_transformation, lineup_cardinality_transformatio
n; both pass on the compendium and both are tested against a hand-crafted broken-cardinality functor as a negative
control. This is small but real categorical machinery — it lets us reason about several functors in parallel through a
single shared transformation.
11

## Page 12

4.9
Representability (Yoneda) over the date poset
In the discrete show category the Yoneda embedding collapses to an equality indicator and is a near-tautology. The
non-degenerate statement lives over the Date poset. For a fixed date 𝑑the covariant representable Hom(𝑑, −) sends
each date 𝑒to a singleton when 𝑑≤𝑒and to ∅otherwise. A natural transformation Hom(𝑑, −) ⇒𝐹setlist assigns
the arrow 𝑑→𝑒an element of 𝐹setlist(𝑒), and naturality with the inclusion legs forces a single element that must lie
in 𝐹setlist(𝑒) for every 𝑒≥𝑑. Because the setlist functor is monotone, that condition holds exactly for the elements
of 𝐹setlist(𝑑), giving the Yoneda bijection Nat(Hom(𝑑, −), 𝐹setlist) ≅𝐹setlist(𝑑): the songs played by date 𝑑are the
natural transformations into the setlist functor. cattheory/yoneda.py::yoneda_lemma_holds_for_setlist checks
this on the corpus, and count_yoneda_naturals has a negative control — on a non-monotone functor an element
that later drops out is correctly rejected and the bijection fails.
4.10
What the construction buys
The payoff is that the question “what songs were played when, by whom?” decomposes as a fibered relation
in the compendium category: the span projections commute with the cumulative setlist functor, and the fiber over a
fixed show date gives back exactly that show’s setlist for exactly that lineup. This is not asserted but checked — cat
theory/spans.py::projections_commute_with_setlist_functor verifies, over the whole corpus, that the union
of show-fibers up to each date equals the setlist functor’s value there. The compendium primitive is the apex of the
span, not a derived join — which is what the categorical reading makes explicit, and what allows seamless extension
to any other performance corpus with the same shape.
12

## Page 13

5
Results on the compendium
All numbers in this section are computed at build time from the committed archival snapshot (data/archival/).
Descriptive statistics and category-theoretic checks are serialized to output/reports/analysis_report.json and
output/reports/category_theory_report.json; claim boundaries are serialized to output/reports/first_pri
nciples_review.json; referential completeness is certified by output/reports/completeness_report.json (zero
dangling references on hard relations; 3341 shows with 40757 performance rows; venue geo coverage at archival scale);
and every rendered figure is validated for existence and non-degeneracy in output/reports/figure_validation
.json. Figures are generated by the registry in src/viz/figures.py and orchestrated through scripts/04_fi
gures.py, 05_extended_figures.py, 08_more_figures.py, 06_mosaic.py, and 10_alluvial.py. Figure titles,
alt-text hints, dashboard labels, caption metadata, and validation filenames are centralized in the same registry so
the prose-facing visual documentation and the executable render target do not drift apart. The manuscript captions
below use a common evidence pattern: data source, statistic, exclusion rule, and claim class.
5.1
Scope and completeness
The active build spans 3341 ingested shows from 1965-05-05 through 1995-07-09 (3341 ingested shows (gdshowsdb
+ truckin gap-fill; community literature estimates about 2318 canonical concerts), 645 songs, 912 venues, 40757
performance rows; community literature cites about 2318 canonical concerts). The completeness audit confirms:
every show resolves to a venue; every performance row resolves to a song; every venue in the compendium has geo
coordinates; and no review, recording, or citation row dangles on hard relations. Importantly, is_complete is a
referential claim — zero unresolved references on those hard relations — and explicitly NOT a claim that every show
has a setlist: 282 of the 3341 catalogued shows have an empty setlist in gdshowsdb. These are surfaced as a pinned
count (n_shows_without_performances in the report, bound by a ground-truth test) and reported as scope, not
folded into the completeness gate. The completeness claims describe the ingested snapshot; they are not a claim that
every optional layer (reviews, lyric text, exhaustive segue markup) is exhaustive.
5.2
Top-line counts
Layer
Count
Notes
Personnel
14
Intervals span 1965–1995 (curated)
Songs
645
Composer/lyricist attribution where known
Lyric pointers
548
URL metadata only (no lyric text)
Venues
912
Geo sidecar at 100% venue coverage
Shows
3341
gdshowsdb catalog; some setlists empty
Performances
40757
Ordered set/position rows
Recordings
7122
Internet Archive + curated rows
Releases
259
Wikipedia discography merge at archival tier
Reviews
1888
maximinus corpus + curated exemplar rows
Citations
139
Bibliography markdown + references.bib
The per-year distribution covers the band’s entire active career; venue concentration in the Bay Area and major halls
reflects the underlying gdshowsdb catalog rather than a hand-picked slice. Recording and archive rows should be
read in the context of the Dead’s mixed institutional/community record: UCSC preserves the formal archive, while
the Internet Archive and taping/trading culture preserve circulating performance metadata [University of California,
Santa Cruz University Library, 2025, Internet Archive Help Center, 2018, Meriwether, 2015, Wallace, 2009].
5.3
Statistical shape and concentration
The compendium is highly skewed, so the manuscript reports medians, percentiles, and concentration measures
alongside top-line means. Figure 1 shows performance rows per show, including the 282 empty-setlist shows already
surfaced by the completeness audit. The median show carries 17 performance rows, the mean is 12.2, the 90th
percentile is 24, and the maximum observed row count is 37. These are setlist-row counts, not audio durations or
claims about musical density.
Figure 2 makes the repertoire skew explicit. Generic segment markers are excluded, matching the top-song ranking.
The song-performance Gini coeﬀicient is 0.74; the top decile of songs accounts for 50.61% of non-segment performance
13

## Page 14

Figure 1: Distribution of performance rows per show in the archival compendium, including empty setlists. Data
source: bundled show/performance tables. Statistic: non-empty show-level histogram with overall median and 90th
percentile reference lines. Exclusion rule: empty setlists are not binned but are counted in the callout and raw
CSV/JSON export. Claim class: descriptive.
rows. The first 44 ranked songs (9.89% of ranked songs) account for half of those rows, and the first 93 songs (20.9%)
account for 80%. This is a descriptive Pareto view of rotation intensity, not a claim that the remaining catalogue
was unimportant.
Figure 3 checks whether the top-song cutoff changes the repertoire story. The exported rows compare top-N cuts 25,
50, 100, 200 over the same non-segment performance table; the largest displayed cut, N=200, accounts for 97.32%
of non-segment performance rows. The era band shows that top-song coverage is not uniform across periods, so the
top-song panels are summaries of the visible rotation rather than a complete description of each era.
Figure 4 applies the same concentration lens to venues. The venue-show Gini coeﬀicient is 0.59, with the top decile
of venue slugs accounting for 51.81% of show rows. The first 84 ranked venues (9.21% of venue slugs) account for
half of the show rows, while 345 venues (37.83%) account for 80%. Because venue slugs remain source-derived and
conservative aliasing is reported separately, this figure should be read as concentration over the bundled venue table,
not as a fully disambiguated venue-history census.
Figure 5 adds the bootstrap layer behind these concentration claims. For song-performance concentration, the Gini
point estimate 0.738 has a fixed-seed 95% interval [0.713, 0.759], and the song top-decile share estimate 50.61% has
interval [45.947, 55.041]%. For venue-show concentration, the Gini interval is [0.555, 0.617], and the venue top-decile
share interval is [47.693, 55.282]%. These intervals are item-level resampling diagnostics for the observed archive,
not uncertainty about an unobserved causal data-generating process.
The exploratory repertoire layer asks a different question: if each top song is represented by its era-by-era performance-
count profile, what structure is visible without adding audio features, lyric text, or causal claims? Figure 6 embeds the
top 80 non-segment songs into two centered SVD components, retaining 48.11% and 28.91% of the log-profile variance
in the first two displayed components, then assigns 5 deterministic clusters. The cluster summary is intentionally
compact: C0: 10 songs, Brent dominant; C1: 16 songs, Brent dominant; C2: 13 songs, Brent dominant; C3: 15
songs, Brent dominant; C4: 26 songs, Brent dominant. This should be read as a diagnostic map of era-weighted
profiles, not as a discovered set of song genres.
Figure 7 gives the matrix view behind the embedding. Each cell is the share of that era’s non-segment performance
rows assigned to the song, so vertical comparisons within an era are meaningful; raw row counts remain available in
output/data/figures/. This heatmap is the more conservative companion to the SVD scatter because it exposes
14

## Page 15

Figure 2: Repertoire concentration: cumulative share of non-segment performance rows by ranked song. Data source:
bundled performance rows. Statistic: cumulative share with 50%/80% coverage guides, Gini, and top-decile share.
Exclusion rule: generic segment markers are excluded. Claim class: descriptive.
Figure 3: Repertoire top-N sensitivity. Data source: bundled performance rows and era labels. Statistic: selected
top-N performance share plus minimum, mean, and maximum era-level coverage. Exclusion rule: generic segment
markers are excluded. Claim class: exploratory sensitivity diagnostic.
15

## Page 16

Figure 4: Venue concentration: cumulative share of show rows by ranked venue slug. Data source: bundled show and
venue tables. Statistic: cumulative show share with concentration thresholds, Gini, and top-decile share. Exclusion
rule: source-derived venue slugs are retained; the venue identity review is report-only.
Claim class: descriptive
concentration diagnostic.
Figure 5: Concentration uncertainty: fixed-seed item-level bootstrap intervals for repertoire and venue concentration
statistics. Data source: bundled song-performance and venue-show count vectors. Statistic: 95% item-level bootstrap
intervals for Gini and top-decile share. Exclusion rule: song rows exclude generic segment markers; venue rows use
source-derived venue slugs. Claim class: exploratory uncertainty diagnostic, not a causal model.
16

## Page 17

Figure 6: Exploratory repertoire embedding: top non-segment songs are embedded from log era-by-song performance
counts using centered SVD, then colored by a deterministic k-means-style cluster assignment. Data source: bundled
performance rows and era labels. Statistic: SVD coordinates and deterministic clusters. Exclusion rule: generic
segment markers are excluded. Claim class: exploratory pattern-discovery.
17

## Page 18

the normalization directly.
Figure 7: Era repertoire heatmap: era-normalized performance-row share for the top non-segment songs.
Data
source: bundled performance rows and era labels.
Statistic: within-era performance-row share.
Exclusion rule:
generic segment markers are excluded. Claim class: exploratory matrix diagnostic.
5.4
Temporal activity
Figure 8 plots the dual-axis career arc: distinct shows per calendar year (bars) and total performance rows (line).
The shape matches the familiar three-act narrative in the standard references [wik, b, bri, University of California,
Santa Cruz University Library, 2025]: rapid build-out in 1969–1972, mid-70s consolidation, and sustained late-period
touring with peaks in 1977 and 1989–1990.
Figure 9 adds a deliberately separate contextual overlay. The bars are the same computed show counts; the labels
are cited historical waypoints from the source dossier: formation and Acid Test context, the live-recording turn
around Live/Dead, the 1970 studio-songwriting pivot, the 1974 Wall of Sound, the formal taper-section era, the
late-1980s mainstream breakthrough, and the 1995 endpoint [Grateful Dead, Weir, 2011, Smithsonian Institution,
2024, McIntosh Laboratory, 2025, Meriwether, 2015, Brackett, 2023, Highways, 2020, Encyclopaedia Britannica].
The labels are not ingested rows and do not affect the counts.
5.5
Repertoire frequency and co-occurrence
playing_in_the_band'' leads the archival compendium with 752 performance rows, followed bynot_fade_away’ ’
(666) and “the_other_one’ ’ (664). Figure 10 ranks the top 15; the ordering aligns qualitatively with community
aggregates [gra, red, c].
This ranking is a repertoire ranking:
it deliberately excludes the generic structural segments drums'',space’ ‘,
jam'',tuning’‘,
and
feedback'', which are not compositions but recurring set segments. Counted as
raw slugs they would dominate the corpus —drums’ ’
and
space'' are in fact the two highest-count
performance slugs overall — so including them would make the headline ranking true-of-the-data
but misleading-as-music. Their counts are reported separately rather than discarded (seesrc/analysis/markers.p
thesegment_marker_countsfield ofanalysis_report.json); named improvisational pieces such asSpanish
Jam’ ’ are catalogued songs and are not treated as generic markers. Of the 645 catalogued songs, 445 enter the
18

## Page 19

Figure 8: Temporal activity in the archival compendium (n=3341 shows). Data source: bundled show and perfor-
mance tables. Statistic: bars count distinct concerts per calendar year; the line counts total performance rows (setlist
entries). Exclusion rule: no shows are dropped; empty-setlist shows contribute to show counts but not performance-
row totals. Claim class: descriptive temporal summary.
Figure 9: Shows per year with cited historical context markers. Data source: bundled show table plus checked
contextual sources. Statistic: annual show counts with selected labelled historical waypoints. Exclusion rule: context
labels are interpretive overlays and are not ingested rows.
Claim class: descriptive chronology with contextual
annotation.
19

## Page 20

performance record (69.42% catalogue coverage) and 196 are catalogued but never performed in the ingested
snapshot.
Figure 10: Most-performed songs in the archival compendium. Data source: bundled performance rows. Statis-
tic: top-15 performance counts. Exclusion rule: generic segment markers are excluded and surfaced separately in
“analysis𝑟𝑒𝑝𝑜𝑟𝑡.𝑗𝑠𝑜𝑛∶∶𝑠𝑒𝑔𝑚𝑒𝑛𝑡𝑚𝑎𝑟𝑘𝑒𝑟𝑐𝑜𝑢𝑛𝑡𝑠‶.𝐶𝑙𝑎𝑖𝑚𝑐𝑙𝑎𝑠𝑠∶𝑑𝑒𝑠𝑐𝑟𝑖𝑝𝑡𝑖𝑣𝑒.
Figure 11 restricts the song–song co-occurrence matrix to the 25 most-played titles. High off-diagonal mass marks
pairs that share shows frequently — including segue-adjacent pairs such as Scarlet Begonias'' /Fire on the
Mountain’ ’ when both appear in the same setlist block. This is a setlist-level relation; audio-level similarity and
boundary estimation remain outside scope and would require the kind of signal pipeline described in MIR setlist-
segmentation work [Wang et al., 2014].
5.6
Markov structure of setlist order
A first-order Markov model fit on within-show song order (see src/analysis/transitions.py) yields the sub-block
in Figure 12. The manuscript-ready matrix excludes generic segment markers so the main panel is a song-to-song
repertoire view; the sensitivity panel below reports what changes when markers are included. Chains such as Help on
the Way'' $\to$Slipknot!’ ’ →“Franklin’s Tower’ ’ appear as high-probability transitions when those titles co-occur
in the compendium setlists.
Figure 13 gives the support-threshold audit for the transition surface. It uses the deterministic report rows in a
nalysis_report.json::transition_sensitivity and evaluates predecessor support thresholds 1, 5, 10, 20, 50
with markers included and excluded. This is the guardrail against treating one-observation probabilities as stable
structure.
The stationary distribution (Figure 14) and association centrality (Figure 15) provide complementary views: the
former summarizes long-run Markov mass; the latter weights songs that bridge many co-occurring pairs in the
show graph. Centrality is computed on the Jaccard-association adjacency rather than the raw co-occurrence counts.
This is a deliberate modeling choice, not a uniquely correct one: on raw counts, eigenvector centrality largely re-
derives raw play frequency (a song played in hundreds of shows co-occurs with almost everything), so the association
normalization reduces that volume bias and surfaces songs that bridge many pairs rather than songs that were simply
played often.
5.7
Category-theoretic cardinalities
Figure 16 plots cumulative setlist and lineup functor cardinalities |𝐹setlist(𝑑)| and |𝐹lineup(𝑑)| along the chronological
show index. Both are monotone non-decreasing on the compendium tier, as required. The active-roster presheaf
20

## Page 21

Figure 11:
Co-occurrence heatmap among the 25 most-performed non-segment songs.
Data source:
bundled
show/performance rows. Statistic: cell (𝑖, 𝑗) counts shows in which both songs appear; diagonal entries are per-
song show counts.
Exclusion rule: generic segment markers are excluded.
Claim class: descriptive association
summary.
21

## Page 22

Figure 12: Estimated first-order transition probabilities among the top 25 non-segment songs by performance count.
Data source: ordered bundled performance rows. Statistic: row-stochastic successor probability over observed within-
show order. Exclusion rule: generic segment markers are excluded here and compared in Figure 13. Claim class:
exploratory descriptive model.
22

## Page 23

Figure 13: Transition sensitivity. Data source: ordered bundled performance rows and the segment-marker policy.
Statistic: share of nonzero transition edges and predecessor rows retained as the minimum predecessor-support
threshold increases. Exclusion rule: the panel explicitly compares markers included versus excluded. Claim class:
exploratory sensitivity diagnostic.
Figure 14: Top 20 non-segment songs by stationary probability under the compendium Markov model. Data source:
ordered bundled performance rows. Statistic: stationary mass of the row-stochastic first-order transition matrix.
Exclusion rule: generic segment markers are excluded. Claim class: exploratory model summary.
23

## Page 24

Figure 15: Top 20 non-segment songs by association centrality. Data source: show-level song co-occurrence. Statistic:
eigenvector centrality on the Jaccard-association adjacency, reducing raw play-frequency bias. Exclusion rule: generic
segment markers are excluded. Claim class: exploratory association summary.
𝑃active (not shown in this single panel) is intentionally non-monotone: Pigpen’s 1972 departure [ucr, dea] and Brent
Mydland’s 1990 death produce expected dips in instantaneous roster size while cumulative lineup size continues to
grow.
The category-theory report records 40757 performance spans, cumulative setlist cardinality 449 at the terminal date,
cumulative lineup cardinality 14, and passing Category.check_laws for both Date and Show.
5.8
Composers, eras, and personnel
Figure 17 contrasts songs-written counts with performance-weighted attribution, exposing the familiar asymmetry
between prolific Garcia/Hunter writing and high-performance-weight Weir/Barlow closers. Figure 18 shows show
density by year and month; Figure 19 is a Gantt chart of the 15 personnel intervals in the current build.
Figure 20 aggregates shows into the six era windows used throughout src/analysis/eras.py; Figure 21 tracks
active lineup size over time.
5.9
Reception, citations, and recordings
The archival compendium bundles 1888 show-level reviews (including the maximinus corpus at archival tier plus 12
curated exemplar rows); Figure 22 reports mean sentiment by kind. Figure 23 and Figure 24 summarize the 139
bibliographic citations and 7122 Internet Archive recording rows. The added citation mass is intentionally weighted
toward archival, scholarly, oﬀicial, and publisher-controlled sources – not fan lore – so the paper’s cultural claims
have a different evidence path from its show/performance rows [Brackett, 2023, Dodd and Weiner, 1997, Adams and
Sardiello, 2000, John F. Kennedy Center for the Performing Arts, 2024, Rock and Roll Hall of Fame, 1994, Recording
Academy, 2007].
5.10
Lyric pointers and segues
Lyric text is deliberately absent; Figure 25 counts theme tags attached to the 548 lyric pointers (CMU lyrics index, cu-
rated overlay, and dead.net gap-fill URLs). 80 pointers carry an attributed lyricist; 0 performed songs lack any pointer
24

## Page 25

Figure 16: Cumulative setlist size (purple, left axis) and cumulative lineup roster size (amber, right axis) along the
chronological show timeline. Data source: bundled ordered performances and curated personnel intervals. Statis-
tic: cumulative set cardinalities for the setlist and lineup functors. Exclusion rule: cumulative functor construction
includes all loaded performances and personnel intervals; no segment-marker filtering is applied. Claim class: vali-
dation, with machine-checked verdicts in output/reports/category_theory_report.json.
Figure 17: Composer attribution for the top 12 credited writers in the archival compendium. Data source: bundled
song composer fields joined to performance rows. Statistic: songs written versus performance-weighted composer
attribution. Exclusion rule: songs without composer metadata do not contribute composer-credit rows; no lyric or
audio content is bundled. Claim class: descriptive attribution summary.
25

## Page 26

Figure 18: Show density by calendar year and month. Data source: bundled show dates. Statistic: 294 year-month
show-count cells.
Exclusion rule: no shows are dropped; empty-setlist shows still count as shows.
Claim class:
descriptive calendar-density summary.
Figure 19: Personnel timeline. Data source: curated personnel interval table. Statistic: 15 membership/role inter-
vals displayed as horizontal date ranges. Exclusion rule: only explicit interval metadata is plotted; inferred guest
appearances are outside scope. Claim class: descriptive provenance-backed roster summary.
26

## Page 27

Figure 20: Shows per era label in the archival compendium. Data source: bundled show dates and deterministic era
windows. Statistic: show counts across 7 era buckets. Exclusion rule: no shows are dropped; era labels are analytical
bins rather than source claims. Claim class: descriptive era aggregation.
Figure 21: Active lineup size by show date.
Data source: bundled show dates and curated personnel intervals.
Statistic: active-member count over 2312 distinct show dates. Exclusion rule: counts use interval coverage on each
date and are not cumulative roster totals. Claim class: descriptive personnel-time summary.
27

## Page 28

Figure 22: Review sentiment by source kind in the archival compendium. Data source: bundled review-pointer table
(n=1888 reviews across 5 source kinds). Statistic: mean sentiment by kind with support and dispersion in the raw
CSV/JSON export. Exclusion rule: reviews without pointer/source metadata are not fabricated; sentiment is limited
to curated and maximinus review rows. Claim class: descriptive reception summary.
Figure 23: Citation kinds across the 139 references in manuscript/references.bib and data/archival/citatio
ns.json. Data source: bibliography markdown, BibTeX, and archival citation rows. Statistic: counts and share-of-
total across 6 citation kinds. Exclusion rule: citation rows are metadata pointers; no source text is bundled. Claim
class: descriptive bibliography-provenance summary.
28

## Page 29

Figure 24: Recording source types in the bundled Internet Archive ingest (n=7122 recordings). Data source: bundled
recording metadata. Statistic: counts and shares across 4 source-type labels. Exclusion rule: missing source-type
labels remain UNKNOWN; the ingest does not infer SBD/AUD/MTX from audio. Claim class: descriptive data-quality
summary.
URL in this build.
The compendium carries 16585 explicit segue_into'' edges from gdshowsdb:seguedflags
viaperformances.json“.
Figure 26 ranks the most frequent segues directly (a node-link layout collapses into an
unreadable tangle once the top edge occurs over a thousand times); the segue structure is interpreted in Section 6.
5.11
Geography, set position, tours, and bustouts
Figure 27 maps geocoded venues (point size ∝shows at that venue). Figure 29 shows within-set position histograms;
Figure 30 ranks tour tags by show count (most shows lack tour metadata in the ingest and appear under an untagged
bucket); Figure 31 highlights songs with the widest gap between successive performances in the archival compendium.
Figure 28 is the companion to venue concentration: it shows the report-only identity audit rather than silently
rewriting venue rows. The alias map is conservative, keeps negative controls distinct, and surfaces 311 ambiguous
same-date collisions for review instead of merging them.
Figure 32 gives the complementary lifespan view: each of the top songs as a horizontal segment from its debut year
to its last-played year, ordered by debut and colored by debut era. Where Figure 31 measures recurrence gaps, this
shows when each piece entered and left rotation — the temporal spine of the repertoire.
Figure 33 places the 259 bundled releases on a timeline by kind.
5.12
Composite views
Figure 34 is the single-page extent artefact: title block, analytical panels, context timeline, and a per-layer provenance
table. Figure 35 traces the top 40 composer →song →era flows by performance weight.
5.13
Claim evidence map
The first-principles review in Figure 36 is a meta-analytic control surface for the manuscript. It does not count
shows, songs, or performances; it counts claim families by claim class and by their primary validation artifact. The
value is negative as much as positive: the map records where a claim is merely contextual, exploratory, structural,
or boundary-enforcing before prose or figure polish can make it sound stronger than the evidence supports.
29

## Page 30

Figure 25: Lyric pointer theme tags. Data source: CMU/dead.net/curated lyric pointer metadata only (n=548
pointers). Statistic: frequency of the top 20 theme tags. Exclusion rule: lyric text is not bundled, parsed, quoted,
or derived. Claim class: descriptive metadata summary.
30

## Page 31

Figure 26: Most frequent explicit segues.
Data source: bundled ordered performance rows with source-marked
segue_into flags (n=16585 markers). Statistic: top 15 directed song-to-song edge counts. Exclusion rule: adjacent
songs are not inferred as segues; only explicit flags contribute. Claim class: descriptive transition-edge summary.
5.14
Limitations and threats to validity
The quantitative views above describe the ingested snapshot, not ground truth, and several caveats bound their
interpretation:
• Segment markers.
drums/space/jam/tuning/feedback are set segments, not songs.
Manuscript-ready
repertoire, co-occurrence, transition, stationary, and association panels exclude them; their counts and marker-
inclusive transition sensitivity are reported separately. This policy is recorded in the first-principles ledger
rather than repeated as a hidden assumption.
• Descriptive, not inferential by default.
Co-occurrence and the first-order Markov chain summarize
observed setlists. Raw transition probabilities conflate one-observation certainties with well-supported esti-
mates; we therefore report support per row and a permutation-null screen with Benjamini–Hochberg false-
discovery-rate control across all 7639 eligible cells. At FDR 𝑞= 0.05, 1533 transitions are significant —
versus 2284 that would pass an uncorrected per-cell threshold (multiple-comparison correction is essential: on
random within-show order the FDR-controlled count is 0, while the uncorrected screen still flags about 5% of
cells by chance). The surviving edges are the canonical segues (drums →space, Scarlet Begonias →Fire
on the Mountain, China Cat Sunflower →I Know You Rider).
• Centrality measures association, not volume. Computed on the Jaccard-association adjacency to avoid
simply re-deriving play frequency.
• Venue granularity. Venues are keyed by normalized name, so a single physical venue can appear under
several slugs. The conservative alias layer identifies 20 duplicate slugs and 311 ambiguous same-date collisions,
but this pass does not mutate venue rows. The full policy, negative controls, and mean collision Jaccard (0.047)
are emitted to analysis_report.json::venue_identity_review and summarized in Figure 28.
• Tour and review coverage are partial. Most shows lack tour metadata (the dominant tours_top bucket
is untagged), and sentiment is computed over a curated/maximinus review subset, not a representative sample.
• Catalogue coverage. 196 catalogued songs never enter the performance record in this snapshot (69.42%
coverage); the catalogue is broader than the performed repertoire.
• Audit reach. The recording date cross-check fires only for Internet Archive identifiers that encode a date
31

## Page 32

Figure 27: Venue geography for geocoded venues (n=912 in compendium). Data source: bundled venue table plus
geo sidecar. Statistic: point area scales with show count at that venue. Exclusion rule: only venues with geocoded
sidecar rows are plotted; current archival coverage is complete. Claim class: descriptive.
Figure 28: Venue identity review. Data source: bundled show/venue/performance tables and curated venue alias
map. Statistic: venue-slug counts, conservative alias-collapse counts, ambiguous same-date collision count, and mean
collision setlist Jaccard. Exclusion rule: report-only review; compendium venue rows are not rewritten. Claim class:
validation and data-quality diagnostic.
32

## Page 33

Figure 29: Set-position distribution. Data source: bundled ordered performance rows. Statistic: performance-row
counts across 33 within-set position indexes. Exclusion rule: all loaded performance rows with positions are counted,
including segment markers. Claim class: descriptive setlist-structure summary.
Figure 30: Top tour labels by number of shows. Data source: bundled show metadata. Statistic: show counts across
1 displayed tour label bucket(s). Exclusion rule: shows without tour metadata remain in the untagged bucket rather
than being imputed. Claim class: descriptive coverage-quality summary.
33

## Page 34

Figure 31: Songs with the widest recurrence gaps. Data source: chronological show order and bundled performance
rows. Statistic: top 15 maximum intervening-show gaps between successive performances. Exclusion rule: generic
segment markers are excluded; songs with a single performance receive a zero recurrence gap in the raw analysis.
Claim class: descriptive repertoire-recurrence summary.
(gdYYYY-MM-DD); recordings under other identifier schemes are checked for show-resolution but not date agree-
ment.
Venue records are merged “first non-empty value wins,” so a venue appearing in two sources with
conflicting non-empty metadata keeps the first-seen value; the committed snapshot is built from sorted sources,
so this is deterministic, but it is a merge convention, not a conflict resolver.
• Figure validation is a blank-canvas tripwire, not a correctness oracle — a figure plotting wrong-
but-non-degenerate data would pass; figure correctness is bound by the archival ground-truth tests on the
underlying numbers, not by pixel variance.
• The claim ledger is governance, not proof. It makes assumptions and evidence links explicit, but it
cannot by itself prove that an adopted source is complete or that a historical interpretation is exhaustive. It is
a guard against over-claiming, not a substitute for source criticism.
These are referential and descriptive claims about the ingested corpus, not claims of completeness over every Grateful
Dead performance.
5.15
Honest framing
Every figure carries an identical provenance footer stamped from the active tier at render time. Refresh the committed
snapshot with scripts/00_fetch_sources.py --online --archival-max (unlimited Internet Archive pagination;
Setlist.fm when SETLISTFM_API_KEY is set; CMU mirror fallbacks), then re-run scripts/99_pipeline.py --tie
r archival. The schema, integration, category-theoretic constructions, and validation gates are unchanged at any
scale.
34

## Page 35

Figure 32: Song lifespans in the archival compendium.
Data source: bundled performance rows and era labels.
Statistic: first-to-last performance year for 25 top songs by performance count, ordered by debut and colored by
debut era. Exclusion rule: generic segment markers are excluded. Claim class: descriptive repertoire-span summary.
Figure 33: Release timeline by kind. Data source: bundled release metadata. Statistic: release dates and kinds for
259 release records in the archival compendium. Exclusion rule: release rows without a source show link remain
release metadata and do not alter performance counts. Claim class: descriptive discography-context summary.
35

## Page 36

Figure 34: Total mosaic for the archival compendium. Data source: selected registry-backed figures and top-line
report values. Statistic: composite overview selected from the 36 validated figure outputs, grouped by scope/time,
statistical shape, repertoire/transitions, geography, and evidence. Exclusion rule: the mosaic is a summary view;
standalone figures and raw CSV/JSON exports carry the full panel detail. Claim class: descriptive synthesis.
36

## Page 37

Figure 35: Composer −> song −> era alluvial diagram. Data source: bundled performance rows joined to song
composer metadata and show-era labels. Statistic: top 40 composer-song-era paths by performance count, with
ribbon width proportional to flow mass. Exclusion rule: paths require composer metadata; lyric text and audio
features are not bundled. Claim class: descriptive attribution-flow summary.
Figure 36: First-principles claim evidence matrix. Data source: the first-principles analysis module. Statistic: count
of 12 claim families by claim class and primary validation-artifact family. Exclusion rule: no corpus rows are added
or removed by this governance layer. Claim class: validation/evidence governance rather than descriptive corpus
measurement. The full ledger is serialized as JSON and CSV files under “output/reports/“.
37

## Page 38

6
Segue and transition structure
The Grateful Dead’s setlists are not a bag of songs but a sequenced object: certain songs flow into certain others, often
without pause, and those flows are as much a part of the band’s identity as the songs themselves. The compendium
captures this at two distinct levels of evidence, and keeping them separate is the point of this section. That separation
also aligns with MIR work on full-concert setlist segmentation: audio-level identification must contend with banter,
applause, covers, transitions, and live-version variation [Wang et al., 2014], while this compendium starts from
curated setlist rows and explicit editorial segue markers.
6.1
Two notions of “what follows what”
A transition is positional: song 𝐵immediately follows song 𝐴within a set, whether or not the band marked a
musical link. These are what the first-order Markov model in Section 5 counts, and the permutation-null screen
retains 1533 of them as significant under false-discovery-rate control (out of 7639 eligible ordered pairs).
A segue is explicit: the source data marks a “->” / “>” link between two performances, encoded in the compendium
as a segue_into edge. There are 16585 such markers spanning 2751 distinct directed song pairs. A segue is therefore
a curated subset of the transitions — the ones a setlist editor judged to be a genuine musical continuation — and
carries stronger evidentiary weight than mere adjacency.
The two notions agree where it matters and diverge informatively. The FDR-significant transitions and the top
segues share their podium in this archival build — “China Cat Sunflower” -> “I Know You Rider” and “Scarlet
Begonias” -> “Fire on the Mountain” top both lists — which is reassuring: the explicit editorial judgement and
the blind statistical screen converge on the same canonical pairings. Where they diverge, the transition view sees
adjacencies that were never marked as segues (e.g. an encore break that the Markov model cannot distinguish from
a continuation), which is exactly why the segue markers are the higher-confidence signal.
6.2
The most frequent segues
Figure 26 ranks the segues directly. The single most frequent is “drums” -> “space” with 1197 occurrences — the
canonical “Drums” -> “Space” passage that anchors the second-set improvisational core for most of the band’s
career. That this structural segment, rather than any song, is the corpus’s most frequent segue is not an artefact: it
reflects a real feature of the music, and it is reported honestly here precisely because the segment markers are kept
in the transition/segue analyses (they are excluded only from the repertoire ranking of Section 5, where they are not
compositions). Below the segment core, the ranking is a tour of the band’s signature pairings — the “China Cat”
-> “Rider” fusion, the “Scarlet” -> “Fire” suite, the “Estimated Prophet” -> “Eyes of the World” flow — recovered
from the markers alone, with no title-based inference.
6.3
Segue hubs
Out-degree in the segue graph identifies launch points — songs that most often flow into something else.
The
highest is “drums’ ’ (1763 outgoing segues), consistent with the structural role of the “Drums”/“Space” core as a
hinge between composed material: the band exits the improvisational segment into a wide variety of songs, so it
accumulates a large, fan-shaped out-degree rather than a single dominant successor. Composed songs, by contrast,
tend to have concentrated out-degree — a song like “Scarlet Begonias” overwhelmingly segues into one partner —
which is the graph-theoretic signature of a fixed suite versus an improvisational junction.
6.4
What this does and does not establish
These are descriptive structures over the ingested setlists, not causal or exhaustive claims. The segue markers are
only as complete as the source editors’ annotations; an unmarked continuation is invisible to the segue view and
appears only as a (weaker) transition. The Markov model is first-order by construction, so longer signature chains
— “Help on the Way” -> “Slipknot!” -> “Franklin’s Tower” — are visible only as their pairwise links, not as a single
third-order object. The taping and trading literature is a useful guardrail here: recordings and setlists are co-curated
cultural records [Meriwether, 2015, Wallace, 2009], so this section reports what the encoded record says rather than
what the band “really” intended in every performance. Both limitations are inherent to the representation and are
revisited in the limitations of Section 5.
38

## Page 39

7
Conclusion
We have introduced The Music Never Stopped, a reproducible, citation-bound Grateful Dead data compendium,
and we have shown that the performance graph carries a small but genuine category-theoretic structure.
The
compendium primitive is a frozen-dataclass schema with deterministic canonical-slug joins; the integration layer
reconciles nine cited sources into one immutable Compendium; the analysis layer computes descriptive, co-occurrence,
Markov-transition, time-series, and network views; and the category-theoretic layer exhibits the date poset, the show
category, the monotone cumulative setlist and lineup functors, the non-monotone active-roster presheaf, and the
performance-as-span construction whose wide pullbacks recover setlists and per-song histories.
Several extensions are natural. First, integrating optional API overlays (Setlist.fm, Grateful Stats) when creden-
tials are available.
Second, integrating Dodd’s annotated lyrics [Dodd and Trist, 2005, bil] as a pointer-only
semantic enrichment layer over the song objects.
Third, computing concrete audio-feature weights against the
fifteen-songs-dataset [fif] and exercising the enriched category at scale. Fourth, integrating the gratefuldata
ETL patterns [Thered] and the jerryPycia query surface [Blance] to broaden the analytical reach. Fifth, integrating
the grateful-dead-reviews corpus [maximinus] for a reception layer that hangs off the performance spans on the
show side.
The deeper transferable lesson is that the compendium primitive should be chosen so that the question
you are asking is literally a categorical construction over it. For the Grateful Dead, the performance is
the apex of a span between show and song; for any analogous live-performance corpus (jam-band, classical concert
series, theatrical run), the same primitive works without modification. The categorical reading is not an aesthetic
overlay; it is the explicit statement of which joins commute, which codomains are monotone, and which views are
unavoidably non-functorial.
39

## Page 40

8
Reproducibility
This manuscript’s numeric, categorical, and figure claims are bound to live code paths. The pipeline runs deter-
ministically from the committed archival compendium (data/archival/); nothing in this paper is generated by
hand.
8.1
Single-command reproduction
cd projects/working/grateful_data
# Refresh committed snapshot (optional; requires network)
uv run python scripts/00_fetch_sources.py --online --archival-max
# Full analysis pipeline + figures + manuscript variables
GRATEFUL_DATA_TIER=archival uv run python scripts/99_pipeline.py --tier archival
The pipeline writes output/data/compendium.json, output/reports/{analysis,category_theory,completeness,first_pri
../figures/*.png (36 validated figures), output/dashboard.html, output/data/manuscript_variables.jso
n, output/manuscript/ (token-resolved markdown for PDF), and raw entity exports under output/data/raw/.
It also writes output/reports/first_principles_claims.csv and 34 registered figure-data exports under out
put/data/figures/: each supported panel has a CSV table, a JSON table with metadata, and an index.json
record consumed by the dashboard. Index rows include data source, statistic, exclusion rule, and claim class, so
captions and raw data can be audited together. The same pipeline now writes provenance sidecars under output
/data/provenance/, pointer-only audio/lyric manifests under output/data/external/, a static explorer under
output/explorer/, a peer-review dossier under output/reports/, and a promotion-readiness report that does not
move lifecycle folders. Optional entity markdown: scripts/09_song_pages.py and scripts/11_entity_pages.p
y.
For a strict publication gate after the template render:
uv run python scripts/20_validate_publication_outputs.py --strict
For a non-mutating command-order and release-prep check:
uv run python scripts/21_release_prep.py --dry-run
8.2
Manuscript PDF (template renderer)
From the template repository root:
cd projects/working/grateful_data
uv run python scripts/z_generate_manuscript_variables.py
cd /path/to/template
uv run python scripts/03_render_pdf.py --project grateful_data
uv run python scripts/05_copy_outputs.py --project grateful_data
This performs the multi-pass LaTeX + bibliography build and writes output/grateful_data/pdf/grateful_data
_combined.pdf (citations from references.bib resolve in the rendered output).
8.3
CLI
cd projects/working/grateful_data
GRATEFUL_DATA_TIER=archival uv run python -m src.cli stats
uv run python -m src.cli song scarlet_begonias
uv run python -m src.cli show 1977-05-08@barton_hall_ithaca
uv run python -m src.cli person garcia
uv run python -m src.cli venue barton_hall_ithaca
uv run python -m src.cli list shows
uv run python -m src.cli list releases
40

## Page 41

uv run python -m src.cli composers
uv run python -m src.cli provenance songs scarlet_begonias
8.4
What’s bound to what
Claim in manuscript
Bound by
Numeric counts in §4
output/data/manuscript_variables.json + output/
reports/analysis_report.json
Referential completeness
scripts/13_audit_completeness.py →completenes
s_report.json (dangling_total: 0)
Figure integrity (blank-canvas tripwire)
scripts/14_validate_figures.py →figure_valida
tion.json (36 non-blank). Figure correctness is bound
by the archival ground-truth tests, not by pixel variance.
Figure filenames, titles, alt text, captions, data source,
statistic, exclusion rule, claim class
src/viz/figures.py registry + manuscript/04_resul
ts.md + output/data/figures/index.json
Figure raw data
scripts/18_export_figure_data.py →
output/data/figures/{*.csv,*.json,index.json}
Claim boundaries
scripts/19_first_principles_review.py →first_
principles_review.json + first_principles_claim
s.csv with section, figure, report, test, and status
columns
Transition sensitivity
output/reports/analysis_report.json →transiti
on_sensitivity plus transition_sensitivity.png
and figure CSV/JSON
Repertoire sensitivity
output/reports/analysis_report.json →statisti
cal_shape.repertoire_topn_sensitivity plus reper
toire_topn_sensitivity.png and figure CSV/JSON
Venue identity review
output/reports/analysis_report.json →venue_id
entity_review plus venue_identity_review.png and
figure CSV/JSON
Source provenance
scripts/23_export_provenance.py →
output/data/provenance/{provenance.csv,provenance.json,*.c
External protected-content boundary
scripts/24_external_manifests.py →pointer-only
audio/lyric manifests plus pipeline_contract.json;
protected content fields are rejected
Static explorer
scripts/25_generate_explorer.py →output/explo
rer/index.html + explorer_data.json with
URL-state filters, sortable headers, related links, figure
metadata, and filtered CSV download
Peer-review dossier
scripts/26_peer_review_dossier.py →
claim-to-artifact map in JSON and Markdown
Publication output gate
scripts/20_validate_publication_outputs.py --st
rict →publication_validation.json
Non-destructive archival refresh diff
scripts/22_archival_refresh_diff.py →
output/refresh/archival_refresh_diff.{json,md};
never overwrites data/archival/
Contextual historical claims
manuscript/references.bib + checked
oﬀicial/scholarly URLs; not ingested as Show or
Performance rows
Functor monotonicity
category_theory_report.json; tests/test_cattheo
ry.py
Naturality of 𝜂
src/cattheory/natural.py + negative-control tests
Wide-pullback setlist recovery
tests/test_cattheory.py on concrete compendium
shows
Citations
manuscript/references.bib + bibliography
markdown (139 merged citations in the active build)
41

## Page 42

Claim in manuscript
Bound by
Honesty boundary
src/honesty.py enforced at every load_seed_compend
ium()
The bibliography parser accepts legacy \url{...} wrappers, explicit url = {...} fields, DOI-only entries, and
explicit BibTeX years.
That matters because the source dossier mixes web archives, books, conference papers,
and DOI-bearing scholarly sources rather than a single citation style. The enriched-bibliography context pass is
reproducible in the narrower sense that each adopted topic is represented by a stable citation key, verified metadata
where available, and a rendered bibliographic entry. The dossier narrative itself is not used as an uncited authority:
source topics enter the manuscript only through direct citation keys, and generated statistics still come from reports,
figure-data exports, and tests.
8.5
No mocks
No test uses MagicMock, mocker.patch, or unittest.mock. Fixtures and the archival compendium are the test
ground truth.
8.6
Determinism
All analyses are pure functions of the immutable Compendium; matplotlib uses the headless Agg backend; exploratory
bootstrap and clustering code uses fixed deterministic seeds and tie-breaks. Re-running scripts/99_pipeline.py
--tier archival produces byte-stable CSV/JSON and visually-stable figures on the same machine.
42

## Page 43

9
The executable honesty boundary
The prose elsewhere in this manuscript draws a bright line between ingested snapshot and live upstream, between
pointer metadata and lyric text, between cited source and HTTP fetch. This section promotes that boundary from
prose to a runtime contract enforced inside the compendium loader by :class:grateful_data.honesty.HonestyBou
ndary.
9.1
What the boundary refuses
The boundary recursively walks the raw JSON payloads and the built Compendium and raises :class:HonestyViolation
on any of the following shapes:
Forbidden shape
Detection rule
lyric_text / lyrics / verse / chorus / stanza /
refrain keys anywhere
recursive walk on lowercased key name; project bundles
pointers, not text
audio_feature_* / synth_* keys anywhere
recursive walk on lowercased key prefix; project bundles
no audio
Review with sentiment > 0 and empty source_url
over-claim shape (“positive but unverifiable”)
Citation with empty or non-http(s):// URL
broken provenance
Recording with gd-prefixed archive_id whose URL
does not point at archive.org
identifier suggests Internet Archive but URL is
elsewhere
LyricPointer with empty source_url
we promise a pointer; missing pointer is over-claim
A violation aborts load_seed_compendium before any analysis runs. enforce_honesty=False is available but exists
only for tests of the boundary itself.
The same rule applies to prose-only context introduced from the supplied source dossier. Formation stories, Wall
of Sound details, public honors, songwriter recollections, studio-era reception, and tape-trading claims must cite
checked sources and remain prose or citation metadata unless the project has a schema field for them [Grateful Dead,
Weir, 2011, McIntosh Laboratory, 2025, John F. Kennedy Center for the Performing Arts, 2024, Marshall, 2003,
Greene, 2015, Highways, 2020]. The dossier does not authorize new quantitative rows, current-person claims, lyric
text, audio features, or revenue figures inside data/archival/. Community reconstructions are explicitly labelled
as context when cited [Seconds, 2016].
9.2
Why this exists
Two lessons from the prior-work memory drove it directly:
• disclosure is not remediation — buried hedges in research-manuscript prose are laundering, not honesty.
A runtime check forced into every load is the durable form.
• shape tests don’t bind truth — a unit test that checks the shape of a review record passes happily on a
fabricated positive review. The honesty boundary checks the content shape that fabrication takes.
9.3
Binding to tests
Each forbidden shape has a dedicated negative-control test that constructs a synthetic violation and asserts the
boundary rejects it. The positive control is the committed archival compendium: test_seed_loader_passes_hone
sty asserts that the real snapshot loads with enforce_honesty=True. The whole loop is tested in tests/test_hon
esty.py and (with one tamper test per failure mode flipping a real row to a known-bad shape) in tests/test_hon
esty_tamper.py.
9.4
Verdict
CERTIFY-WITH-RESIDUALS for v0.1. The honesty boundary enforces every named failure mode at load
time, the negative-control tamper tests demonstrate it fails loud on the right shapes, and the entity-page generators
are anti-fabrication-tested in tests/test_entity_pages_no_fabrication.py.
Acknowledged residuals at this
version:
43

## Page 44

• schema validation catches shape violations but cross-field semantic validity (e.g. date ∈band-active-window,
set position ≤setlist length) is not yet a gate — that is the next layer of refinement;
• the cattheory/ package’s load-bearing modules (categories, functors, spans, natural, colimits, yoneda) each
carry a negative control — a broken composition, a non-monotone functor, or a too-small colimit vertex that
the check must reject — so the constructions are tested for teeth, not merely exercised. The colimit now
verifies the universal property (not just subset-of-union) and Yoneda is checked over the non-degenerate Date
poset rather than the trivial discrete case. The one remaining piece of honest scaffolding is enriched.py: the
audio-similarity enrichment is structural only — concrete weights would come from a downstream pipeline
against the fifteen-songs-dataset [fif], and the honesty boundary forbids bundling audio features, so it is
labelled a stub rather than presented as an empirical result.
9.5
Licensing and provenance
The compendium integrates many community and institutional sources, and is explicit about reuse posture. The
code and the derived compendium schema (the slugged entity tables and the category-theoretic constructions) are
the contribution of this project; the underlying facts — setlists, dates, venues, personnel — are drawn from the
cited sources, each of which carries its own terms. Setlist and show data derive primarily from community archives
(gdshowsdb, the truckin-through-time dataset, Setlist.fm) and reference works (Wikipedia, Britannica); recording
metadata comes from the Internet Archive Live Music Archive, whose Grateful Dead collection has its own access
policy and metadata conventions [Internet Archive Help Center, 2018]; reviews are a curated/maximinus subset. No
lyric text and no audio-feature data are bundled — lyric pointers are URL metadata only — both to respect copyright
and as the project’s stated ethical boundary. Dodd and Trist’s annotated lyrics are cited as scholarship, not copied
as data [Dodd and Trist, 2005].
One nuance worth stating explicitly: while individual facts (a date, a venue, a song title) are not protectable, a
curated compilation — a particular hand-edited setlist or segue sequence — can carry its own rights independent
of lyrics or audio, and our setlist and segue data derive from such community-curated sources. Archive scholarship
on the Dead’s sound record underscores that this is a co-created curation ecosystem, not a source-free fact dump
[Wallace, 2009, Meriwether, 2015]. Downstream users should therefore consult each cited source for its own licensing
before redistribution; this work claims rights only over the integration code and the structural representation, not
over the source facts or any upstream curator’s compilation.
9.6
Out of scope
The boundary is not a content-moderation system or a lyric classifier. It is a small set of refusals encoding what the
project itself has promised to do and not do, written in code so a future contributor cannot quietly drift past it.
44

## Page 45

10
References
The full bibliographic database is at manuscript/references.bib.
45

## Page 46

References
The complete annotated grateful dead lyrics (billboard review). URL https://www.billboard.com/culture/product-
recommendations/grateful-dead-lyric-book-buy-online-1235812793/. Review of David Dodd’s annotated lyrics.
Grateful dead — encyclopaedia britannica. URL https://www.britannica.com/topic/Grateful-Dead.
Grateful dead — band members (oﬀicial). URL https://www.dead.net/band. Oﬀicial band-members page on
dead.net.
Fifteen-songs dataset. URL https://github.com/grateful-dead-live/fifteen-songs-dataset. 2617 SBD recordings of
15 songs from the Live Music Archive.
Gdsets.com, a. URL https://gdsets.com. Setlists, ticket stubs, and stage-pass scans for the Grateful Dead and
related projects.
Gdsets — grateful dead, b. URL https://gdsets.com/grateful-dead.htm.
Github topic: gratefuldead. URL https://github.com/topics/gratefuldead. Meta-index of Grateful Dead data
projects.
Grateful stats. URL https://www.gratefulstats.com. Aggregated show/tune/venue statistics front-end.
Internet archive — live music archive (grateful dead). URL https://archive.org/details/GratefulDead. Primary
source for show recordings.
Grateful dead data sets: Any good sources?, a. URL https://www.reddit.com/r/gratefuldead/comments/10w2rh2
/grateful_dead_data_sets_any_good_sources/. r/gratefuldead discussion thread linking community data sets.
Did jerry or bobby write the words to any of these?, b. URL https://www.reddit.com/r/gratefuldead/commen
ts/1r4azkm/did_jerry_or_bobby_write_the_words_to_any_of/. r/gratefuldead community discussion of
Hunter/Barlow attribution.
Best setlist databases?, c. URL https://www.reddit.com/r/gratefuldead/comments/1e4z60l/best_setlist_database
s/.
Does anyone still have the spreadsheet file with [...], d. URL https://www.reddit.com/r/gratefuldead/comments/1
qb5aec/does_anyone_still_have_the_spreadsheet_file_with/.
Setlist.fm — grateful dead, a. URL https://www.setlist.fm/setlists/grateful-dead-bd6ad4a.html. Crowd-curated
setlist registry with REST API; Grateful Dead MusicBrainz identifier 6faa7ca7-0d99-4a5e-bfa6-1fd5037520c6.
The setlist program (setlists.net), b. URL https://www.setlists.net. Searchable setlists 1965–1995.
Grateful dead lineup changes: A complete guide. URL https://ultimateclassicrock.com/grateful-dead-lineup-
changes/. Ultimate Classic Rock chronological narrative.
Grateful dead discography, a. URL https://en.wikipedia.org/wiki/Grateful_Dead_discography.
Grateful dead, b. URL https://en.wikipedia.org/wiki/Grateful_Dead. Wikipedia entry, including founding lineup
and key changes.
Rebecca G. Adams and Robert Sardiello, editors. Deadhead Social Science: You Ain’t Gonna Learn What You Don’t
Want to Know. AltaMira Press, Walnut Creek, CA, 2000. ISBN 9780742502512. URL https://www.bloomsbury.c
om/us/deadhead-social-science-9780742502512/.
Alex Allan. Grateful dead lyric and song finder. URL https://www.whitegum.com/intro.htm. Searchable index of
every song the Dead played, with attribution.
Andrew Blance. jerrypycia. URL https://github.com/andrewblance/jerryPycia. Python library for exploring Dead
live show data.
John Brackett. Live Dead: The Grateful Dead, Live Recordings, and the Ideology of Liveness. Duke University Press,
Durham, NC, 2023. ISBN 9781478025481. doi: 10.1215/9781478027614. URL https://www.dukeupress.edu/live-
dead. Studies in the Grateful Dead series; eISBN 9781478027614.
46

## Page 47

JSTOR Daily. The grateful dead, tape trading, and the music industry, 2015. URL https://daily.jstor.org/grateful-
dead-tape-trading-music-industry/. Public-facing synthesis of tape trading scholarship with links to underlying
JSTOR sources.
David G. Dodd and Alan Trist. The Complete Annotated Grateful Dead Lyrics. Free Press, New York, 2005. ISBN
9780743277471. URL https://www.simonandschuster.com/books/The-Complete-Annotated-Grateful-Dead-
Lyrics/David-G-Dodd/9781439103340.
Oﬀicial publisher page for the electronic edition; this project stores
pointers only, not lyric text.
David G. Dodd and Robert G. Weiner. The Grateful Dead and the Deadheads: An Annotated Bibliography. Music
Reference Collection. Greenwood Press, Westport, CT, 1997. ISBN 9780313301414. URL https://www.bloomsbu
ry.com/us/grateful-dead-and-the-deadheads-9780313301414/.
Encyclopaedia Britannica. Jerry garcia. URL https://www.britannica.com/biography/Jerry-Garcia. Editorial
reference entry used only for contextual biography.
Noah Gorstein. Truckin’ through time. URL https://noahgorstein.com/blog/truckin-through-time/. Scraper plus
SQLite database derived from the CMU setlist archive.
Grateful Dead. Biography. URL https://www.dead.net/biography. Oﬀicial band biography and historical overview.
Andy Greene. Robert hunter on grateful dead’s early days, wild tours, sacred songs, 2015. URL https://www.ro
llingstone.com/feature/robert-hunter-on-grateful-deads-early-days-wild-tours-sacred-songs-37978/. Interview
context for Hunter’s songwriting and band-history recollections; not a data-bearing source.
Americana Highways. The grateful dead’s reissues of workingman’s dead and american beauty, 2020. URL https:
//americanahighways.org/2020/11/18/review-the-grateful-deads-reissues-of-workingmans-dead-and-american-
beauty-are-impeccable/. Reception context for the 1970 studio-songwriting pivot and anniversary reissues; not a
data-bearing source.
Internet Archive Help Center. The grateful dead collection, 2018. URL https://help.archive.org/help/the-grateful-
dead-collection/. Collection policy and metadata guidance: audience recordings are downloadable, soundboards
are stream-only at band request, and public uploads are closed.
John F. Kennedy Center for the Performing Arts. The kennedy center announces 47th class of honorees, 2024. URL
https://www.kennedy-center.org/globalassets/news-room/press-release-pdfs/2024/press-release---kennedy-
center-announces-47th-kennedy-center-honors-slate.pdf. Oﬀicial press release naming the Grateful Dead among
the 2024 Kennedy Center Honorees.
Mark Leone. Grateful dead lyrics (cmu), a. URL https://www.cs.cmu.edu/~mleone/dead-lyrics.html. Lyrics index,
pointing to the original Stratton database.
Mark Leone. Grateful dead setlists (cmu), b. URL https://www.cs.cmu.edu/~mleone/gs.html. Legacy archive;
derivative of the Jerry Stratton database (1972–).
David Lewin. Generalized Musical Intervals and Transformations. Oxford University Press, New York, 2007. ISBN
9780195317138. doi: 10.1093/acprof:oso/9780195317138.001.0001. URL https://academic.oup.com/book/4583.
Oxford Academic edition; original Yale University Press edition published in 1987.
Lee Marshall. For and against the record industry: An introduction to bootleg collectors and tape traders. Popular
Music, 22(1):57–72, 2003. doi: 10.1017/S0261143003003040. URL https://doi.org/10.1017/S0261143003003040.
maximinus. grateful-dead-reviews. URL https://github.com/maximinus/grateful-dead-reviews/blob/master/dead
_reviews.txt. Long-form fan review corpus.
McIntosh Laboratory. Bringing the grateful dead’s wall of sound to life, 2025. URL https://www.mcintoshlabs.c
om/about/news/mcintosh-and-the-grateful-deads-wall-of-sound. Manufacturer history of the Wall of Sound and
MC2300 amplifier system.
Nicholas Meriwether. Documenting the dead: Taping the dead, 2015. URL https://www.dead.net/features/docu
menting-dead/documenting-dead-taping-dead. Oﬀicial dead.net archive essay on taping, trading, and Deadhead
archival practice.
Sarala Padi, Spencer J. Breiner, Eswaran Subrahmanian, and Ram D. Sriram. A category theoretic approach to
modeling and analysis using music as a case study. Technical Report NISTIR 8092, National Institute of Standards
47

## Page 48

and Technology, Gaithersburg, MD, 2017. URL https://www.nist.gov/publications/category-theoretic-approach-
modeling-and-analysis-using-music-case-study. NIST Interagency/Internal Report applying OLOG/category
theory to Carnatic music and reproducible music-analysis integration.
Alexandre Popoff and Moreno Andreatta. Hidden categories: A new perspective on lewin’s generalized interval
systems and klumpenhouwer networks. 2023. doi: 10.48550/arXiv.2311.18371. URL https://arxiv.org/abs/2311
.18371.
Recording Academy. Lifetime achievement award, 2007. URL https://www.grammy.com/awards/lifetime-achievem
ent-awards. Oﬀicial recipient list including the Grateful Dead.
Rock and Roll Hall of Fame. The grateful dead, 1994. URL https://rockhall.com/inductees/grateful-dead/. Oﬀicial
inductee page.
Grateful Seconds. Grateful dead touring revenues 1965–1995, 2016. URL http://www.gratefulseconds.com/2016/0
1/grateful-dead-touring-revenues-1965-1995.html. Community reconstruction of touring revenue estimates; used
only as contextual business-history evidence, not as a quantitative compendium input.
Jeff Smith. gdshowsdb. URL https://github.com/jefmsmit/gdshowsdb. Relational schema and Ruby gem for
canonical show data.
Smithsonian Institution.
Institutionally dead, 2024.
URL https://avpreservation.si.edu/institutionally-dead.
Audiovisual Media Preservation Initiative essay on Grateful Dead-related Smithsonian holdings.
Scotty Thered. Grateful data: Etl tutorial. URL https://github.com/scottythered/gratefuldata. Tutorial pipeline
using the Internet Archive and ASCAP ACE.
University of California, Santa Cruz University Library. The grateful dead archive, 2025. URL https://guides.libra
ry.ucsc.edu/gratefuldeadarchive. Oﬀicial UCSC library guide for the Grateful Dead Archive and Grateful Dead
Archive Online.
David A. Wallace. Co-creation of the grateful dead sound archive: control, access and curation communities. In
Jeannette A. Bastian and Ben Alexander, editors, Community Archives: The Shaping of Memory, pages 169–194.
Facet, 2009. doi: 10.29085/9781856049047.012. URL https://www.cambridge.org/core/books/abs/community-
archives/cocreation-of-the-grateful-dead-sound-archive-control-access-and-curation-communities/1428A421FA
4D0D7353C5418099303029.
Ju-Chiang Wang, Ming-Chi Yen, Yi-Hsuan Yang, and Hsin-Min Wang. Automatic set list identification and song
segmentation for full-length concert videos. In Proceedings of the 15th International Society for Music Information
Retrieval Conference, pages 239–244, 2014. URL https://archives.ismir.net/ismir2014/paper/000211.pdf. ISMIR
archive copy; licensed CC BY 4.0 in the proceedings PDF.
Bob Weir. Bob weir on psychedelic san francisco and the birth of the grateful dead, 2011. URL https://www.founds
f.org/Bob_Weir_on_Psychedelic_San_Francisco_and_the_Birth_of_the_Grateful_Dead. FoundSF interview
context on formation, Acid Tests, and San Francisco counterculture.
48


---
*Extraction method: pymupdf*
