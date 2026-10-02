# Homepage, Curio Cards, and connected reliability — 2026-10-02

The homepage now leads with a concise research introduction and clear routes to
publications, software, art, and teaching. Responsive typography, a native
profile disclosure, and media content available without JavaScript preserve
access across narrow layouts and keyboard use.

The three Curio tiles show the complete official numbered images for
[24 — Complexity](https://curio.cards/card/24/),
[25 — Passion](https://curio.cards/card/25/), and
[26 — Education](https://curio.cards/card/26/). They retain their original 900 ×
1200 dimensions and 3:4 framing, load lazily, and link to their primary records.
Exact bytes, source URLs, and artwork rights are recorded in
[`assets/curio-cards/`](../assets/curio-cards/README.md). Unsupported edition,
rarity, undated price, and individual May mint claims were removed. The gallery
context distinguishes CurioDAO (2021) from Distributed Development (2017), and
its meaningful `#curio-cards` target repairs an existing domain-page link.

Search reserves a bounded horizontal filter row before its core index loads.
Real delayed-core checks at 320px and 412px verified unchanged filter height and
result position, keyboard visibility of later options, sparse and long-query
results, and no-JavaScript links. The generated manifest records all four search
exports and their actual paper-text and report sources. The worker's small
shell includes the homepage stylesheet; live verification requires exact hashes
for that stylesheet and all three card images.

Branch review also identified a historical migration edit inside paper text.
The separate [source-custody receipt](paper_text_custody_2026-10-02.md) records
43 exact text restorations, one repaired quotation, unchanged archived PDFs,
and the retained newer Pitch Deck extraction. Historical unique branch work
requires recoverable archival evidence before pruning; ordinary merged tips
remain reachable through main.

Independent evidence review caught absolute workspace paths in the smoke
generator's diagnostic output. The writer now normalizes its known checkout
prefix before truncation; a regression checks partial-path exposure, while
fresh real smoke captures retain selector results and screenshot hashes.
The older affected receipt marks diagnostic-only redaction explicitly and
preserves its original capture date, source revision, results, and image hashes.

Local acceptance:

| Check | Observed result |
| --- | --- |
| Actual homepage browser tests | 10 passed; zero failures, errors, or skips |
| Final homepage Lighthouse 13.4.1 | Performance 75, accessibility 100, SEO 100; CLS 0; no runtime error |
| Visual/axe observations | Desktop and mobile, explicit dark and light themes; no overflow, JavaScript errors, or serious/critical violations |
| Independent search geometry | Two actual Chromium cases passed at 320px and 412px |
| Independent deployed-byte/manifest unit checks | 36 passed |
| Independent offline-shell size | 12 requests; 236,276 raw bytes, below 320 KiB |
| Source-custody focused suites | 53 passed; all 1,723 grounded quotations matched their own texts |
| Full integration before the diagnostic privacy follow-up, with browser QA required | 1,214 passed; zero failures, errors, or skips; 349.759 seconds |
| Integration Lighthouse 13.4.1 | Eight real routes passed the declared floors; homepage and search CLS 0, accessibility 100, SEO 100 |
| Source stability during integration | All 2,847 checked runtime/code files retained identical bytes |
| Progressive browser QA and smoke | 8/8 and 10/10 scenarios passed |
| External-link refresh | 856 URLs checked; 706 successful; no 404/410; 150 explicitly classified access or transient warnings |

The [machine-readable local observation](homepage_curio_2026-10-02.json)
binds the integration and Lighthouse diagnostics to source hashes and records
their limits, including the later independently reviewed privacy regression.
Final clean-candidate integration is a separate publication gate. The old search
CLS follow-up is resolved by these real measurements
and the delayed-core mobile checks. Remaining performance targets stay in the
active backlog. The external-link report was refreshed after standard validation
identified missing coverage for the three new primary card URLs; its
[review queue](external_links_triage_2026-10-02.md) preserves access warnings.

The existing shared reading-progress region retains a moderate axe landmark
warning. Homepage performance remains below the aspirational 85 target.
Hosted checks and live acceptance remain separate publication gates with their
own candidate-bound evidence. These local checks do not attest deployment or a
complete human-reviewed release. The new standard visual capture remains pending
human review; independent agent observations of the affected homepage are
additional local evidence and do not substitute for that requirement.
