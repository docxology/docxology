# Forensic Audit of the MillenniumLean Clay-Proof Package (AIX Global)

_Do six Lean theorems resolve the six remaining Clay Millennium Problems? No._

## Part I - Manuscript

# Abstract

This report audits the MillenniumLean package (AIX Global, Inc.; Zenodo
DOI 10.5281/zenodo.22226553), which claims complete kernel-checked Lean 4
proofs of the six remaining Clay Millennium Problems. We read all eleven files
of the package verbatim, re-derived every kernel-hygiene claim independently
under the pinned toolchain (leanprover/lean4:v4.34.0-rc1; mathlib at the
manifest-pinned revision d0be1efe9a), and compared each claimed final theorem
against the official Clay problem statements.

Findings are itemized as fourteen one-per-finding reports (docs/audit/), each
quoting the package verbatim with line anchors and recording the probe that
backs the verdict. The kernel claims are TRUE and reproduce byte-for-byte:
clean build, zero live `sorry`, zero project axioms, axiom footprints inside
{propext, Classical.choice, Quot.sound}. They are also evidentially void: the
"final theorems" are either implications whose unproved premise binders carry
the entire mathematical content (Riemann, Yang-Mills, P vs NP), definitions
of the open statements (Navier-Stokes, BSD), or true theorems about unrelated
simple objects (a list identity for Hodge; substitution for Yang-Mills). The
"universalization tower" that certifies Hodge, BSD, and Navier-Stokes proves
only that 0 < n + 1 for all naturals. Verdict: none of the six problems is
resolved. The audit disputes no kernel output of the package; it disputes
what those outputs are claimed to demonstrate.


# Introduction

## The claim

On 2026-09-01, AIX Global, Inc. published MillenniumLean - "the six remaining
Clay Millennium Problems, machine-checked in Lean 4" - as the public,
independently-verifiable certificate layer of its paper "Demonstrating Quantum
Value by Solving the Six Remaining Clay Millennium Problems" (Holt &
Ovseyenko, Zenodo DOI 10.5281/zenodo.22179463). The package README states the
six "final theorems" by name, asserts "0 sorry, 0 project axiom", and offers
`#print axioms` output as the decisive evidence. A companion document,
WHY_THIS_IS_PROOF.md, opens: "This is done. State it as done."

An extraordinary claim requires extraordinary evidence. The certificate layer
is public; this audit holds it to the standard it itself invokes: a Lean term
the kernel accepts is a proof **of its type** - so the entire question is
what the types say.

## Scope and fairness posture

Three commitments govern everything below.

1. **No kernel fact is disputed.** We reproduce the build and axiom report
   independently (Section 2; finding F01) and they match the package
   byte-for-byte.
2. **Every refutation is quote-anchored.** Each of the fourteen findings
   (docs/audit/F01-F14) quotes the package's own source lines, with file:line
   verified character-against the extracted tree by a script (259/259 quoted
   lines verify byte-exact).
3. **Genuine content is credited.** Finding F13 itemizes the package's real
   theorems and faithful formalizations; the verdict rests on what is absent,
   not on denying what is present.

## Reader's guide

Section 2 records the reproduction; Section 3 the audit method; Section 4 the
per-problem results; Section 5 the cross-cutting findings; Section 6 the
external record (context only); Section 7 reproducibility of the audit
itself; Section 8 scope limits. The Epistemic Status paragraph (Section 9)
states exactly what was run and what remains unverified.


# Methodology

## Artifacts

The audited artifact is the Zenodo zip MillenniumLean_ClayProof_20260901.zip
(10 files plus one directory entry, 50,708 bytes), extracted unmodified to
package/MillenniumLean/ with a SHA-256 inventory recorded in
data/audit_report.json. The zip was neither edited nor re-packed; all
quotations anchor to this extracted tree.

## Kernel reproduction (independent)

- Toolchain: elan installed leanprover/lean4:v4.34.0-rc1 exactly as pinned in
  lean-toolchain.
- mathlib: shallow-cloned at the revision pinned in lake-manifest.json
  (d0be1efe9afff6119115373bf4ea5abd833b3a95); HEAD verified on the checkout;
  prebuilt oleans restored via `lake exe cache get` (8,711 files).
- Build: `lake build Tower Millennium` in a clean workspace containing the
  package's six source/config files verbatim -> "Build completed successfully
  (8730 jobs)", exit 0.
- Axioms: `lake env lean print_axioms.lean` -> exit 0; the six footprint lines
  match the package's PROOF_CERTIFICATE.md verbatim.
- Receipt: data/BUILD_RECEIPT.md.

One disclosed soft spot: mathlib was shallow-cloned at the exact pinned
revision rather than full-history cloned. This affects provenance decoration
only, not the kernel check (the kernel checks the checked-out tree's oleans).

## Statement-level audit

Each claimed "final theorem" was parsed from Millennium.lean by a
balanced-parenthesis binder extractor (src/lean_parser.py) that records the
declaration kind (theorem vs def) and every explicit premise binder - the
same mechanics as the package's own audit.py, re-implemented and tested. Each
final was then compared against the official Clay statement (the oracle in
src/clay_statements.py, from the Clay problem PDFs) and classified:

- CONDITIONAL_IMPLICATION - the type carries unproved premise binders;
- DEFINITION_ONLY - a def of the open statement;
- OFF_TOPIC_THEOREM - closed type, but no Clay object in it.

The package's own audit.py was also executed unmodified; its committed output
reproduces.

## Verification of the audit itself

All fifteen test files in tests/ assert audit facts against the real package
bytes (no mocks; 15/15 pass). All 259 line-anchored quotations in
docs/audit/*.md were script-checked against the extracted sources - line
number and text both - with zero divergence. An earlier draft failed this
check (51 divergences from Unicode normalization); all quote blocks were
rebuilt programmatically from the package bytes and re-verified. The
failure-and-fix is disclosed in docs/audit/00_INDEX.md.

## Line-by-line verification of the package (whole-file)

- Millennium.lean (404 lines): read verbatim; 35 declarations.
- Tower.lean (30 lines): read verbatim; 6 declarations + 3 #print commands.
- audit.py (69 lines): executed; parsing logic reviewed line-by-line.
- PROOF_CERTIFICATE.md (105 lines), WHY_THIS_IS_PROOF.md (70 lines),
  README.md (167 lines): read verbatim; every checkable claim traced to a
  declaration or marked unverified.
- lakefile.toml, lake-manifest.json, lean-toolchain, print_axioms.lean:
  inspected; manifest revision cross-checked against the clone.


# Results

## Kernel hygiene: confirmed (F01)

Independently reproduced: clean build (exit 0), zero live `sorry`, zero
project axioms, and the six axiom footprints byte-identical to the package's
committed receipt - e.g. `Millennium.riemannHypothesis_of_selfAdjoint_correspondence
depends on axioms: [propext, Classical.choice, Quot.sound]`, and
`Millennium.hodge_kunneth depends on axioms: [propext]`.

## The tower: one trivial invariant under five names (F02)

Tower.lean:11 defines `declInv (n : Nat) : Prop := 0 < n + 1`; Tower.lean:12
grounds it in `Nat.succ_pos 0`; Tower.lean:15-16 builds `universal` as plain
induction. The theorems named `hodge`, `bsd`, and `navier_stokes`
(Millennium.lean:88-93), the five Tower wrappers (:17-21), and
`poincare_control` (:26) all reduce to `forall n : N, 0 < n + 1`. No Hodge
class, elliptic curve, PDE, or complexity class appears.

## Per-problem verdicts

1. **Riemann (F07).** `riemannHypothesis_of_selfAdjoint_correspondence`
   (Millennium.lean:70-79) is a correct 5-tactic proof of
   (self-adjoint D with the Hilbert-Polya correspondence corr) ->
   RiemannHypothesis. The premise `corr` asserts, for every nontrivial zeta
   zero, exactly the spectral-location fact whose construction is the open
   problem. No D or corr term is provided. CONDITIONAL_IMPLICATION.
2. **Yang-Mills (F04).** `yang_mills_gap (c m : R) (hc : 0 < c) (hid : m = c)
   : 0 < m := hid ▸ hc` (Millennium.lean:84): substitution. No gauge theory,
   no Wightman axioms, no existence content anywhere. CONDITIONAL_IMPLICATION.
3. **Navier-Stokes (F05).** `ns_official` (Millennium.lean:254-264) is a
   faithful def of the Clay statement - real mathlib analysis objects,
   Schwartz decay, uniqueness - but a def proves nothing; the theorem named
   `navier_stokes` is the tower tautology. DEFINITION_ONLY.
4. **Hodge (F03).** `hodge_kunneth : conv [1,1,1,1] [1,1,1] =
   [1,2,3,3,2,1] := by decide` (Millennium.lean:45): a Hodge-diamond list
   computation for CP3 x CP2. The conjecture quantifies over all smooth
   projective varieties and concerns algebraicity of (p,p) classes; no
   variety, cohomology, or cycle object appears in any type.
   OFF_TOPIC_THEOREM.
5. **BSD (F06).** `bsd_official` (Millennium.lean:209-211) defines rank =
   vanishing order against real mathlib objects; nothing proves it for any
   curve, and the official leading-coefficient formula is absent even as a
   def. DEFINITION_ONLY.
6. **P vs NP (F08).** `P_neq_NP_of_proof_lower_bound` (Millennium.lean:324-333)
   is a correct 4-line contradiction from two premises that restate the
   conjecture: an unconditional superpolynomial proof-system lower bound
   (beyond current knowledge, as stated) and the proof-complexity-to-
   algorithm bridge (never achieved). `NPcomplete` is an uninterpreted
   interface field. CONDITIONAL_IMPLICATION.

## Cross-cutting findings

- **audit.py category error (F09).** The package's committed audit labels
  defs of open problems "CLOSED (no premise in the type)"; its premise
  detector works by binder NAME (h-prefix, corr/bridge/step) and silently
  counts unproved hypotheses like `size` as "data".
- **Axiom-footprint rhetoric (F10).** PROOF_CERTIFICATE.md:37-38 claims
  smuggled premises "would appear here as an extra axiom. It does not."
  False as an argument: premises are binder types, invisible to
  `#print axioms`. The conditional finals themselves are the counterexample.
- **Poincare "positive control" (F11).** The control's type is the same
  tautology `0 < n + 1`; a control that cannot fail validates nothing. No
  negative control exists.
- **Toy-but-true cluster (F12).** Klein ZMod-12 torsion and `2 < sqrt 5` are
  true and kernel-checked; the Clay-relevant objects live only in comments.
- **Genuine content (F13).** Roughly ten true small theorems (trivial zeta
  zeros, Hermitian spectrum reality, twisted-Laplacian bounds, discrete-gap
  convergence), two faithful statement formalizations, correct plumbing - all
  kernel-clean, none Clay-bearing.
- **External record (F14).** Context only: the companion paper's FTQC claims
  were publicly demolished (code distance 1; hidden post-selection;
  self-described "engineered signature"); the honest Lean formalization
  community marks all seven problems OPEN. The verdict above does not depend
  on any of this.


# Conclusion

The MillenniumLean package is kernel-honest and mathematically empty with
respect to its headline claim. Its build receipt is real - we reproduce it
byte-for-byte - and irrelevant: the types the kernel certifies are
tautologies, substitutions, list identities, faithful definitions of open
problems, and implications whose premises are the prizes themselves.

Three lessons generalize beyond this package.

1. **Axiom footprints audit trust, not content.** `#print axioms` catches
   `sorryAx` and project axioms; it cannot see unproved premises, which live
   in binder types. Any "0 axioms" receipt must be paired with a
   statement-level audit of what the theorems say.
2. **Positive controls need failure modes.** A control that certifies
   `0 < n + 1` alongside "Perelman's theorem" tests nothing.
3. **Defining an open problem in a proof assistant is zero evidence.** The
   kernel will happily check the definition forever.

The six remaining Clay Millennium Problems remain open. The honest
formalization community says so; so does every type in this package, read
closely.


# Reproducibility of this audit

Everything re-runs from the repository root:

    python3 projects/working/Millennium_Audit/scripts/run_audit.py
    # -> console report + data/audit_report.json (machine-readable)

    uv run pytest projects/working/Millennium_Audit/tests/
    # -> 15 real-data tests against the extracted package

    .venv/bin/python -m pytest tests/ -q          # from the project dir

Lean reproduction (receipt: data/BUILD_RECEIPT.md):

    elan toolchain install leanprover/lean4:v4.34.0-rc1
    # mathlib at pinned rev d0be1efe9afff6119115373bf4ea5abd833b3a95
    lake exe cache get
    lake build Tower Millennium
    lake env lean print_axioms.lean

Findings: one file each under docs/audit/F01-F14, indexed by docs/audit/
00_INDEX.md, which also records the 259/259 quotation-verification receipt.


# Scope, limitations, and related work

## What this audit is

A statement-level audit of one public artifact: does any type in the package
settle a Clay Millennium Problem? Every verdict is re-derivable from the
cited file:line anchors.

## What this audit is not

- It does not adjudicate the companion paper's quantum-computing claims;
  finding F14 records the public record as context only.
- It does not evaluate the proprietary "governed computation" layer, which
  the package itself says is not needed to verify the theorems - correctly,
  because there is nothing substantive in the certificate layer to verify.
- It does not claim the package's kernel facts are false; F01 confirms them.

## Limitations

- The mathlib clone was shallow at the pinned revision (provenance
  decoration only; see Section 2).
- Fairness of classification: CONDITIONAL_IMPLICATION vs OFF_TOPIC_THEOREM
  is a judgment call for edge cases; for this package every classification
  is over-determined (e.g. Yang-Mills is both conditional AND its type is
  bare substitution).
- We audited the 20260901 zip as published; a newer revision could differ
  (none was available on Zenodo as of the audit date).

## Related work

- lean-dojo/LeanMillenniumPrizeProblems - reference formalizations of all
  seven problems, marked Open.
- DavidFox998/opera-numerorum - 664 verified Lean "bricks" with an explicit
  honesty statement that no Clay problem is solved.
- postquantum.com's detailed critique of the companion FTQC paper.
These agree with, but are not load-bearing for, the present verdict.


# Epistemic Status

Validated in this audit session (2026-09-01), all by direct execution or
verbatim read:

- All 10 package files read (11 unzip entries incl. directory); SHA-256 inventory recorded (data/audit_report.json).
- Kernel reproduction completed: pinned toolchain v4.34.0-rc1 installed;
  mathlib at pinned revision d0be1efe9afff6119115373bf4ea5abd833b3a95;
  `lake build Tower Millennium` exit 0 ("Build completed successfully
  (8730 jobs)"); `lake env lean print_axioms.lean` exit 0 with the six
  footprint lines byte-identical to the package's committed receipt
  (data/BUILD_RECEIPT.md).
- The package's own audit.py executed unmodified; its committed output
  reproduced.
- Independent binder parsing of all six finals (src/lean_parser.py);
  verdicts recorded in data/audit_report.json.
- 15/15 tests pass against the real package bytes (no mocks).
- 259/259 line-anchored quotations across docs/audit/*.md verified
  character-exact against the extracted sources; an earlier draft failed
  this check and was rebuilt programmatically (disclosed in 00_INDEX.md).

Unverified / disclosed limits:

- mathlib was shallow-cloned at the exact pinned revision (provenance
  decoration only; the kernel checks the checked-out tree).
- Third-party web claims (F14) are recorded as reported by their sources,
  not independently investigated.
- Classification of edge cases (conditional vs off-topic) involves judgment;
  every classification here is over-determined by multiple quotes.

Nothing in the verdict depends on any unverified item.


## Part II - Audit Doctrine and Method

# Audit Doctrine and Method

How the Millennium_Audit was designed and conducted. Findings live in
../audit/; this file records the approach.

## 1. Governing doctrine

Three principles, in priority order:

1. **Green is not proof.** A passing build, clean gate, or axiom-free
   footprint is a conjecture about what a claim demonstrates until an
   independent pass re-derives it. We reproduced every kernel claim before
   attacking any of them (finding F01), and we dispute none of them.
2. **Attack the type, not the kernel.** A Lean theorem is a proof of its
   TYPE. The decisive question for a "Millennium proof" claim is never
   "does it compile" but "what does the type say". All load-bearing
   analysis (F02-F08) is statement-level: binder parsing, declaration kind
   (theorem vs def), and comparison against the official Clay statements.
3. **Fairness is structural, not rhetorical.** Genuine content gets its own
   finding (F13) with every real result itemized; the external record (F14)
   is quarantined as context-only so the verdict stands without it; every
   refutation cites the package's own source lines.

## 2. Audit design

Four lenses, executed in order:

| Lens | Question | Instrument |
|------|----------|------------|
| Reproduction | Do the kernel claims reproduce? | Pinned toolchain + pinned mathlib build + axiom print (F01) |
| Statement | What does each final theorem's type actually say? | Binder parser + Clay-statement oracle (F02-F08) |
| Meta-audit | Is the package's own evidence honest? | Execute their audit.py; check its logic (F09, F10, F11) |
| Context | What does the public record show? | Web retrieval, quarantined to F14 |

## 3. Verification chain (what makes findings trustworthy)

Every layer of the audit is itself gated:

1. **Artifact integrity.** The Zenodo zip extracted unmodified; SHA-256 of
   all 11 files in data/audit_report.json.
2. **Kernel reproduction.** Toolchain installed from the package's own pin;
   mathlib checked out at the exact manifest revision; build exit 0; axiom
   report byte-identical to the package's committed receipt
   (data/BUILD_RECEIPT.md).
3. **Parser validation.** src/lean_parser.py re-implements the package's
   audit.py mechanics; both agree on binder lists; the package's audit.py
   was executed unmodified and reproduced its committed output.
4. **Test gate.** 15 real-data tests (tests/test_audit.py) assert the audit
   facts against package bytes - no mocks. Run: `.venv/bin/python -m pytest
   tests/ -q`.
5. **Quotation gate.** `scripts/check_quotations.py` parses every
   line-anchored quotation in docs/audit/*.md and verifies text and line
   number against the extracted sources: 259/259 byte-exact. The first
   draft failed (51 divergences from Unicode normalization in F07-F14);
   quote blocks were rebuilt programmatically from the package and
   re-verified to zero. Disclosed in the audit index. The script is
   committed and re-runnable (process-lane red-team gap, fixed 2026-09-01).
6. **Self-audit of verdicts.** Each verdict tag requires a probe actually
   run this session; PLAUSIBLE/[UNVERIFIED] tags were available and none of
   the load-bearing verdicts needed them.

## 4. Classification scheme

Each claimed final theorem is classified by what its TYPE does relative to
the official Clay statement:

- **CONDITIONAL_IMPLICATION** - type carries unproved premise binders
  (Riemann: hD, corr; Yang-Mills: hc, hid; P vs NP: hq, hlb, bridge).
- **DEFINITION_ONLY** - a def of the open statement (ns_official,
  bsd_official). A def proves nothing; binder-closedness of a def is
  meaningless (the package's own audit calls these "CLOSED" - the F09
  category error).
- **OFF_TOPIC_THEOREM** - closed type, but no Clay object in it
  (hodge_kunneth: list arithmetic).

Two cross-checks discipline the scheme: (a) the package's own audit.py
concedes CONDITIONAL for the same four finals; (b) every classification is
over-determined by multiple quotes (e.g. Yang-Mills is both conditional AND
its type is bare substitution).

## 5. The smoking gun, stated precisely

Tower.lean:11: `def declInv (n : Nat) : Prop := 0 < n + 1`. The theorems
named hodge, bsd, navier_stokes, poincare_control and five Tower wrappers
all equal Tower.universal over this invariant, proved from Nat.succ_pos.
Substituting the definition, each proves `forall n : N, 0 < n + 1`. The
package's own comment (Millennium.lean:337-341) claims this trivial invariant
was replaced with "mathematical content"; the replacement (Promote) is
generic plumbing whose tower_closes proves whatever a tower declares - and
the named theorems still consume the unchanged Tower.declInv.

## 6. Tooling map

| Path | Role |
|------|------|
| src/lean_parser.py | Binder extraction, declaration kinds, sorry/axiom grep (comment-aware) |
| src/clay_statements.py | Official Clay statements as comparison oracle |
| src/statement_audit.py | Classification engine (three verdict classes) |
| src/verdicts.py | Headline/tower/epistemic verdict records |
| src/evidence.py | SHA-256 inventory of the package |
| scripts/run_audit.py | Thin orchestrator -> data/audit_report.json |
| tests/test_audit.py | 15 real-data assertions |
| data/BUILD_RECEIPT.md | Lean reproduction receipt |
| data/STATEMENT_EVIDENCE.md | Per-problem file:line gap analysis |

## 7. Deliberate limits

- The package under audit is never modified; quotes anchor to the extracted
  tree's exact bytes.
- The proprietary quantum layer is not evaluated (the package itself says it
  is unnecessary for verification - true, and central to the problem: there
  is nothing substantive to verify).
- Third-party web claims are recorded as reported, quarantined to F14, and
  are not load-bearing for the verdict.


## Part III - Findings Index

# MillenniumLean Audit — Findings Index

**Audited artifact:** `package/MillenniumLean/` (AIX Global, Inc.), from
Zenodo DOI 10.5281/zenodo.22226553, zip `MillenniumLean_ClayProof_20260901.zip`.
Audit session: 2026-09-01. All quotations are verbatim with `file:line` anchors
verified against the extracted tree; SHA-256 inventory in `../../data/audit_report.json`.

**Headline verdict: The package resolves none of the six Clay Millennium
Problems.** Its kernel-checked theorems are real (F01) but are not the Clay
statements: four finals carry the conjectures as unproved premise binders
(Riemann, Yang-Mills, P vs NP - F07, F04, F08) and two are definitions of
the open statements (F05, F06). Whether the problems are resolved in the
wider literature is outside this audit's evidence base. (The package does
contain genuine small theorems and faithful formalizations - itemized with
credit in F13.) The package's mathematical content is
carried by unproved premise binders, defs of open statements, and the trivial
tower invariant `0 < n + 1`.

| # | Finding | Verdict tag | One-line summary |
|---|---------|-------------|------------------|
| F01 | Kernel build & axiom footprints | CONFIRMED (pack) / VERIFIED (repro) | Their kernel claims are real — and evidentially void |
| F02 | Tower invariant `declInv n := 0 < n + 1` | REFUTES headline | The "universalization tower" proves `0 < n+1` |
| F03 | Hodge "final theorem" is list arithmetic | REFUTES coverage | `conv [1,1,1,1] [1,1,1] = [1,2,3,3,2,1]` by decide |
| F04 | Yang–Mills final is substitution | REFUTES headline | `0 < c → m = c → 0 < m` by `hid ▸ hc` |
| F05 | Navier–Stokes: def of the open problem | REFUTES headline | `ns_official` is a def; tower theorem is trivial |
| F06 | BSD: def of the open problem | REFUTES headline | `bsd_official` defines; nothing proves rank=ord |
| F07 | Riemann: conditional on the open problem | REFUTES headline | Premise `corr` IS the Hilbert–Pólya correspondence |
| F08 | P vs NP: conditional on unresolved premises | REFUTES headline | `hlb` + `bridge` restate the conjecture |
| F09 | audit.py "CLOSED" category error | CONFIRMED (misleading) | Def binder-closedness treated as proof-closedness |
| F10 | Axiom-footprint rhetoric | REFUTED (as argument) | "Premises would appear as axioms" is false |
| F11 | "Poincaré positive control" | SELF-DEFEATING | Control proves the same tautology as the six |
| F12 | Klein/ZMod-12 and theta-gap theorems | OFF_TOPIC (real but unrelated) | True finite arithmetic, no Clay content |
| F13 | Genuine real content in the package | CONFIRMED (fair credit) | Small true mathlib-anchored lemmas, itemized |
| F14 | External context: FTQC claim record | CONFIRMED (third-party) | Companion paper's claims publicly demolished |

Method note: every finding file pairs (a) the claim under audit, (b) verbatim
quotation(s), (c) a probe actually run this session, (d) fair analysis
including what is genuinely real, (e) a verdict tag
CONFIRMED / REFUTES-headline / PLAUSIBLE / [UNVERIFIED].

## Self-audit receipt

A verification pass (2026-09-01) parsed every line-anchored quotation in all
15 files and checked each against the extracted package bytes, line number
and text both: 259/259 quoted lines verify byte-exact against
package/MillenniumLean/. An earlier draft pass failed this check (51
transcription divergences in F07-F14); all quote blocks were rebuilt
programmatically from the package bytes and re-verified. The index and
findings were authored from verbatim in-session reads; the kernel facts in
F01 were independently reproduced (build exit 0, axiom report byte-identical
to the package's committed receipt - see ../../data/BUILD_RECEIPT.md).

## Audit fairness statement

- No kernel output of the package is disputed anywhere in this audit; all
  were independently reproduced and agree.
- Every "REFUTES HEADLINE" verdict cites the package's own source lines; the
  refutation is of the claimed demonstration, not of any kernel fact.
- F13 itemizes and credits every genuine result in the package.
- F14 is recorded as context only; removing it leaves the verdict unchanged.
- The one methodological soft spot, disclosed: mathlib was shallow-cloned at
  the exact pinned revision rather than full-history cloned; this affects
  provenance decoration only, not the kernel check.

## Red-team pass receipt (2026-09-01, pre-publication)

Three independent hostile-review lanes were dispatched against this audit
before publication:

1. **Statement-lane (F02-F08):** all seven findings re-verified byte-exactly
   against the package; all survive CONFIRMED. One precision note (F07's
   prose transliteration of the corr premise, already programmatically
   quote-anchored) and two minor items (ns_official/bsd_official appear in
   the package's own print_axioms.lean - now folded into F09 as
   reinforcement).
2. **Meta-lane (F09-F11 + headline):** the audit is fair to the package's
   audit.py (F09, if anything, understates the README prose overclaim); F10
   correctly grants the narrow true claim before refuting the wide one; F11
   and the headline verdicts hold.
3. **Process-lane:** orchestrator re-run reproduces data/audit_report.json
   exactly; 15/15 tests pass; independent quotation re-check 257/267 with
   the 10 flagged lines all resolved as checker-side source-file
   misattributions (verified byte-exact against README.md:121-124); doctrine
   verification-chain layers each map to a real artifact.

Rating: process integrity SOLID. Corrections applied from the pass (all
probe-verified against package bytes before editing): F04 precision note
(hc is dischargeable via ym_center_flux_pos:119; the load-bearing premise
is hid); F06 strengthened (the _hL premise is underscore-named and never
used - L is a free function despite the docstring claim); F07 annotated
(riemann_official:52 is a proof-free def alias with no consuming theorem);
F09 reinforced via print_axioms.lean. Post-correction gate: 259/259 quotes
byte-exact, 15/15 tests pass.


## Meta-lane and process-lane receipts (2026-09-01, full reports)

**Meta-lane (F09-F11 + headline):** F09 fair and, if anything, understates
the package's overclaim (README.md:110 asserts a negative existential about
unproved premises a name-based parser cannot establish; README.md:147
asserts premises are "committed spectral certificates" when no such terms
ship in the zip). F10 confirmed fair and self-consistent. F11 verdict
survives with one clause softened (the tautological control does carry
build/toolchain smoke-test information - now reflected in F11). F14
quarantine verified non-load-bearing by grep. Headline reworded from a
world-claim to a package-attributed claim (above), provable from in-package
evidence alone.

**Process-lane:** orchestrator re-run reproduces data/audit_report.json
exactly; independent quotation re-verification 267/267 byte-exact (all 10
flagged lines hand-confirmed against README.md:121-124 and :158-163);
15/15 tests pass; every manuscript number recomputes; all doctrine
verification-chain layers map to real artifacts. Rating: MINOR-GAPS, with
all three gaps fixed in this pass: (a) quotation-gate script now committed
as scripts/check_quotations.py (re-runnable); (b) "11 files" corrected to
"10 files plus one directory entry" in F14 and the manuscript; (c) the
no-version-control caveat is disclosed here - Millennium_Audit is a
working-tree project; the regenerated audit_report.json relies on the
in-session receipt and the package SHA-256 pins rather than a git baseline.

Post-correction gate: 259/259 quotes byte-exact (re-run via the committed
script), 15/15 tests pass.