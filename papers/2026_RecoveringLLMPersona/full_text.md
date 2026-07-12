# Full Text: Recovering LLM-Persona Accuracies from Unlabeled Votes

> Extracted from `Friedman_2026_Recovering_e1196698.pdf`

---

## Page 1

Recovering LLM-Persona Accuracies from Unlabeled Votes
An algebraic NTQR evaluation study, and why disagreement is not enough
Daniel Ari Friedman
Active Inference Institute
FractAI
daniel@activeinference.institute
ORCID: 0000-0001-6232-9096
DOI: 10.5281/zenodo.20498699
2026-06-01
2026-06-01

## Page 2

Contents
1
Abstract
2
2
Introduction
3
2.1
Reader map: what is observed, recovered, and checked . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3
2.2
Related evaluation paradigms . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
5
3
Methods
6
3.1
Evaluation object and data flow . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
3.2
The classifiers: three LLM personas . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
3.3
The test: 64 binary scenarios
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
6
3.4
The models . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
3.5
The evaluators
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
3.6
The algebra: from votes to accuracies
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
3.7
Statistics
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
9
3.8
The evaluability diagnostic
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
9
3.9
Reproducibility . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
4
Results
11
4.1
Unsupervised recovery works when the ensemble is well-behaved
. . . . . . . . . . . . . . . . . . . . . . . .
11
4.2
Failure modes: constant classifiers and non-compliance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
13
4.3
Disagreement is not evaluability (the non-obvious result) . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
14
4.4
A label-free diagnostic predicts evaluability
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
15
4.5
Majority voting and error-independent recovery coincided here
. . . . . . . . . . . . . . . . . . . . . . . . .
15
4.6
Reading the figure suite together . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
15
4.7
Synthetic validation: recovery scaling and the alarm’s blind spot
. . . . . . . . . . . . . . . . . . . . . . . .
15
4.8
The two-solution tie-break needs clearly-better-than-random judges . . . . . . . . . . . . . . . . . . . . . . .
22
4.9
Error-independent vs. majority-voting: exactness vs. robustness . . . . . . . . . . . . . . . . . . . . . . . . .
23
4.10 Statistical validation matrix . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
24
5
Discussion
25
6
Figures — formal specification
27
7
Supplemental material
28
7.1
S1 — The two-solution tie-break
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
28
7.2
S1.5 — Worked example: the prevalence algebra on real votes . . . . . . . . . . . . . . . . . . . . . . . . . .
28
7.3
S1.6 — Exactly when the imaginary-root alarm fires (and its blind spot) . . . . . . . . . . . . . . . . . . . .
29
7.4
S2 — Full per-model label vote counts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
29
7.5
S3 — Full per-persona recovery (mistral:latest) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
31
7.6
S4 — Personas, scenarios, and authored truth . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
31
7.6.1
Persona system prompts (verbatim)
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
31
7.6.2
Scenarios and authored truth (Q = 64)
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
32
7.7
S5 — Reproduction
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
35
7.8
S6 — The evaluability diagnostic, defined . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
36
7.9
S7 — Output file inventory
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
36
8
References
38

## Page 3

1
Abstract
Algebraic (NTQR) evaluation infers how accurate a group of noisy classifiers was on a finite test using only their
responses — no answer key.
We test this end to end on real large language models.
Three trader “personas”
(optimistic, neutral, pessimistic), instantiated as system prompts, each make a binary bullish/bearish call on the same
64 market scenarios; we run the identical trio through six locally-hosted models via Ollama. For each model we recover
per-persona, per-label accuracy with ErrorIndependentEvaluation (unsupervised) and score it against the authored
ground truth (supervised), which is used only as a check.
On the five models whose three judges all varied (mistral:latest,
gemma4:latest,
gemma3:4b,
gemma2:2b,
granite4.1:3b), the unsupervised algebra recovered persona accuracies to a mean absolute error of 0.012, within
the 0.102 sampling-noise floor across all six per-label accuracy terms, with no labels – including a persona’s genuinely poor
bullish accuracy of 0.57, recovered as 0.59. The other model collapsed at least one persona into a constant classifier
(a judge that voted one way on all 64 scenarios), which makes the error-independent algebra unsolvable.
The central, non-obvious result: inter-judge disagreement does not imply evaluability. Aggregate disagreement
separated this run only because the unevaluable model(s) collapsed to 0.00; the five evaluable models spanned 0.03–0.23.
What gates evaluation is a per-judge condition — every judge must vary (and answer) — not an ensemble one. We formalize
this as a label-free evaluability diagnostic (a judge whose modal-vote fraction reaches 1.0 is a constant classifier; an
unparseable vote is an abstention) that predicted exactly which models would be evaluable, before any solve and without
ground truth. This is a concrete instance of the safety property the NTQR logic promises: it warns you when an ensemble
is not good enough to be evaluated. A scenario bootstrap puts a 95% CI of [0.000, 0.038] on the recovery MAE (well inside
the 0.102 noise floor), and a deterministic synthetic study generalizes the recovery beyond the finite set of real evaluable
models — error falls like 1/√Q (slope -0.58, stable across ensembles) — while mapping two honest limits: the built-in
failure alarm catches anti-correlated judges with no false positives yet can miss positively-correlated (shared-training)
errors, and the two-solution tie-break inverts once judges are no longer clearly better than random — exactly where simple
majority-voting evaluation, though biased, is the more robust fallback.
2

## Page 4

2
Introduction
Evaluation is the “forgotten twin” of learning: most AI work optimizes training, while the question how good were these
judges, really? is usually answered only when labels exist. The unlabeled version of that question is old: Dawid-Skene-style
observer-error models, annotator-expertise models, truth inference in crowdsourcing, and weak-supervision systems all use
repeated judgments to infer reliability without a conventional answer key [Dawid and Skene, 1979, Yan et al., 2010, Zheng
et al., 2017, Ratner et al., 2017]. Modern LLM-as-judge work makes the same problem newly practical and newly fragile:
LLM judges can scale evaluation, but their errors, biases, and measurement uncertainty have to be modeled rather than
wished away [Zheng et al., 2023, Chen et al., 2026].
That is also why majority vote and self-consistency are not enough as evaluation instrumentation. They can select an
answer, but they do not by themselves tell us whether the voters were reliable, whether one judge was systematically wrong
on one label, or whether the response matrix has enough variation to estimate reliability at all. A high-integrity evaluator
needs to separate three questions that are often collapsed in practice: did the interface return valid measurements, is the
vote matrix algebraically evaluable, and how does the selected estimate compare with external truth when such truth is
available?
Algebraic evaluation (the NTQR logic [Corrada-Emmanuel et al., 2026, Corrada-Emmanuel, 2023a,b]; see the repository
root README) takes a deliberately narrower stance. It constructs postulates — true for any finite test, containing no
probability theory and no model of the task domain — that link the observed agreements and disagreements of an ensemble
to the unknown statistics of their correctness. Agreement-rate estimators showed how much unlabeled signal is present in
classifier agreements [Platanios et al., 2014, 2016]; NTQR uses a complete algebraic postulate system to ask when that
signal is suﬀicient to recover judge accuracies, and when the response matrix itself warns that the evaluation is not justified.
A crucial caveat in that same framing is that the logic “is not magical … GIGO also applies to evaluation on unlabeled data,”
and its distinctive safety value is that it “can warn you if the ensemble is not good enough to perform a reliable evaluation.”
This paper turns that promise into a measured, reproducible demonstration on contemporary LLMs, and sharpens the
warning into a quantitative diagnostic. The claim is not that NTQR solves crowdsourcing or judge aggregation generally.
The narrow claim is that, under its stated algebraic assumptions, NTQR can recover per-judge accuracies from a finite
unlabeled vote matrix — or emit an evaluability warning when the matrix lacks the required structure [Corrada-Emmanuel
et al., 2024, Corrada-Emmanuel, 2025].
We ask three questions:
1. Does unsupervised algebraic recovery actually work on real LLMs? When an LLM ensemble is well-behaved,
how close does the answer-key-free recovery come to the truth?
2. What breaks it? Across a spread of models — strong and deliberately weak — what failure mode dominates, and
what is its mechanism?
3. Can we predict failure without labels? Is there a statistic, computable from the votes alone, that tells us in
advance whether an ensemble is evaluable at all?
Our contributions: (i) an end-to-end, cached, reproducible pipeline that runs the same persona trio across many local
models and scores unsupervised recovery against authored truth; (ii) the empirical finding that disagreement is not
evaluability — the binding constraint is per-judge variation, not ensemble disagreement; and (iii) a label-free evaluability
diagnostic that, in this study, perfectly predicted which models the algebra could solve.
The experiment is therefore not asking an LLM to predict markets better than another LLM. It is asking whether a finite
matrix of binary judgments contains enough internal structure to evaluate the judges themselves. That distinction is what
makes the method useful when a task model is unavailable: the algebra evaluates the response process, while authored
truth is reserved for the controlled validation step.
2.1
Reader map: what is observed, recovered, and checked
Because the idea is unconventional, the central bookkeeping matters. The unsupervised evaluator never sees the authored
truth; it sees only the vote matrix. The truth appears later, as a validation target for this controlled study. The simulations
then ask whether the same algebra behaves the same way when the true data-generating process is known by construction.
3

## Page 5

Table 1: What is observed, recovered, and checked. The answer key is not an input to the unsupervised solve; it is the
controlled-study check.
Object
Observed without labels?
Validation-only?
Meaning in this study
Scenario text
yes
no
A finite authored
question containing
only the market facts
the model may use.
Persona vote
yes
no
One parsed bullish or
bearish response, or an
abstention if parsing
fails.
Bullish / bearish labels
yes
no
Operational response
labels: expected
next-quarter direction
up or down under the
stated facts.
Authored truth
no
yes
The defensible answer
used after the
unsupervised solve to
check recovery accuracy.
Prevalence
recovered
checked
Fraction of scenarios
whose authored truth is
bullish (a).
Persona accuracy
recovered
checked
Per-persona, per-label
correctness rates
inferred from
vote-pattern structure.
Best predictor
recovered convention
checked
The
higher-mean-accuracy
algebraic branch
selected without seeing
truth.
Task/world model
no
no
Not estimated here; the
algebra evaluates judges
on a finite test rather
than learning market
semantics.
The important negative statement is as load-bearing as the positive one: without a task/world model, the algebra does
not learn what financial markets will do. It evaluates a finite response matrix. In this study, bullish and bearish are
operational labels defined by the authored scenario facts: bullish means the defensible next-quarter directional call is
up under the stated facts; bearish means down. The estimator then asks whether the pattern of judge agreements is
suﬀicient to recover each judge’s per-label accuracy on that finite test.
Table 2: Representative operational questions and answers. The full 64-scenario answer key is generated in the supple-
mental; these rows show how bullish and bearish are defined without a learned task model.
ID
Operational truth
Why this is the authored
answer
Scenario
s01
bullish
Growth, estimate beat, and
raised guidance all point to
upside.
Revenue grew 42% YoY,
beat estimates, and
management raised full-year
guidance.
4

## Page 6

ID
Operational truth
Why this is the authored
answer
Scenario
s02
bearish
Repeated misses plus a
dividend cut indicate
deteriorating fundamentals.
The company missed
earnings for the third
straight quarter and cut its
dividend.
s19
bullish
Mixed but positive: the
earnings beat is the
operational tie-break
despite full valuation.
Earnings beat but guidance
was merely in line; shares
are near all-time highs.
s20
bearish
Mixed but negative: margin
compression and weak
macro outweigh sales
growth.
Sales grew but margins
thinned and the macro
outlook for the sector is
murky.
s23
bullish
Mixed but positive: cost
cuts plus reinvestment
create a turnaround path.
New management is cutting
costs aggressively and
reinvesting in a growing
niche.
s24
bearish
Mixed but negative: low
valuation is outweighed by
structural decline.
The stock is cheap on paper
but sits in a structurally
declining industry.
2.2
Related evaluation paradigms
The experiment is easiest to read if NTQR is placed beside the neighboring evaluation paradigms it resembles but does
not replace. The table below keeps the comparison concrete: what is observed, what assumption does the work, what the
method returns, and what kind of warning it can or cannot provide.
Table 3: Neighboring evaluation paradigms. Citations in the surrounding text identify the canonical references for each
row; the key distinction is that NTQR returns either a label-free algebraic recovery or a label-free warning that recovery
is not justified.
Paradigm
Observed input
Main assumption
Output
Failure warning
Supervised evaluation
Votes plus labels
Trusted labels
Empirical accuracies
None about unlabeled
evaluability
Dawid-Skene /
expertise
Repeated labels
Latent truth model
Worker error
estimates
Model-fit warning
Agreement-rate
estimation
Classifier agreements
Independence / priors
Accuracy estimates
Assumption
sensitivity
Weak supervision
Labeling functions
Generative
dependency model
Probabilistic labels
Dependency
diagnostics
LLM-as-judge
Model judgments
Judge reliability
model
Scalable evaluation
Bias /
measurement-error
correction
Majority vote /
self-consistency
Multiple votes
Better-than-random
voters
Aggregate answer
No per-judge recovery
guarantee
NTQR in this paper
Unlabeled vote sketch
Algebraic postulates
Accuracies or alarm
Constant-classifier /
imaginary-root failure
5

## Page 7

3
Methods
3.1
Evaluation object and data flow
The unit of analysis is a model-specific vote matrix: three personas by 64 scenarios, with each cell containing exactly
one parsed bullish or bearish call. The unsupervised NTQR solve never consumes scenario text, market semantics,
model logits, chain-of-thought, or the authored answer key. It receives only unlabeled vote-pattern counts derived from
that matrix.
The controlled experiment adds two layers around that solve.
First, a schema-constrained collection interface makes
parsing a measured engineering boundary rather than a hidden source of invented labels. Ollama’s structured output
interface accepts a JSON Schema in the format field and its public guidance recommends lower-temperature decoding for
more reliable schema adherence [Ollama, 2026b, 2024]. Structured-output reliability is itself an active evaluation problem
[Wang et al., 2025]; here we make it a measured interface check and then move the scientific question to the completed
binary vote matrix. Second, the authored scenario truth is kept out of the solve and used only afterward to score recovery
error. fig. 1 shows this separation explicitly.
Figure 1: Pipeline boundary for the experiment. Scenario facts and system prompts create parsed persona votes; the
unsupervised NTQR solve sees only the resulting unlabeled agreement sketch.
Authored truth is held out until the
validation step, where recovered accuracies are compared with supervised truth.
3.2
The classifiers: three LLM personas
We use three system-prompted “trader” personas as noisy binary judges, chosen so their mistakes are not identical —
exactly the error structure error-independent evaluation needs:
• Optimist — leans bullish on ambiguous setups.
• Neutral — weighs the stated facts with no directional bias.
• Pessimist — leans bearish on ambiguous setups.
Three personas form a trio, matching the three-classifier R=2 evaluators in the public NTQR package documentation
[Corrada-Emmanuel et al., 2026]. Each persona reads the same scenario and returns a single JSON call. The prompt
contract is versioned as v3_binary_schema (4d157f84885a) and appears verbatim in sec. 7.6. We treat the personas as
instruction-following interfaces, not as human trader models; instruction-following behavior itself is a product of modern
LLM alignment and fine-tuning practice [Ouyang et al., 2022].
3.3
The test: 64 binary scenarios
The test is T = 1 test of Q = 64 one-line market scenarios with R = 2 possible responses (bullish→label a,
bearish→label b). Each scenario carries an authored truth — the defensible call given only the stated facts. Most
scenarios are clear-cut; six are deliberately ambiguous (mixed signals) so the personas’ dispositions pull their calls apart.
6

## Page 8

The deck is deliberately not balanced. The authored prevalence is 40 bullish, 24 bearish — true prevalence of
label a = 0.625. This is a methodological requirement, not an accident. The error-independent evaluator has a removable
singularity at prevalence exactly 1/2: there its accuracy equations degenerate (the two algebraic solutions coalesce and
the per-label accuracies resolve to 0/0, returned as NaN). An exactly 50/50 answer key places the true prevalence on that
singularity, so any competent ensemble — whose recovered prevalence sits near the truth — lands on it and cannot be
solved, even when every judge varies. Tilting the deck to 0.625 moves the whole problem off the singularity while leaving
24 clear bearish scenarios, so even the bullish-leaning personas keep casting both calls and never collapse into a constant
classifier (sec. 4.2). The full scenario list and truths are in sec. 7.6.
The authored truth is never an input to the unsupervised evaluator. It is used only to build a SupervisedEvaluation
as a check against which recovery is scored.
This distinction also defines the meaning of “best predictor” in the paper. The best model is not the model with the
most plausible financial prose.
It is the evaluable vote matrix whose selected unsupervised solution has the smallest
validation-only recovery MAE against the authored labels.
3.4
The models
We run the identical trio through six locally-hosted chat models via Ollama at temperature 0.1 (stochastic decoding):
mistral:latest, gemma4:latest, gemma3:4b, gemma2:2b, granite4.1:3b, smollm2:135m-instruct-q4_K_S. The mod-
els span a range of sizes and capabilities, from small sub-instruction-following models to multi-billion-parameter chat mod-
els. Votes are cached per (backend, model, temperature, prompt version, prompt hash, persona, scenario), so
the sweep is reproducible and resumable without mixing prompt designs.
The local Ollama tags are the experimental identifiers. Public model-family references provide provenance only: Mistral
for mistral:latest [Jiang et al., 2023], the Gemma-family reports for the local Gemma tags [Gemma Team, 2024b,a,
2025], IBM Granite 4.1 for granite4.1:3b [IBM, 2026], and SmolLM2 as family context for the quantized local smollm
2:135m-instruct-q4_K_S tag [Ben Allal et al., 2025]. None of those citations enters the solve; the solve uses only the
cached votes and the model names recorded in summary.json.
Table 4: Local model lineup, public family provenance, and data-driven run status. The citations identify model families,
while the solve uses only cached votes and the recorded local tags.
Local Ollama tag
Public family citation
Run status
What the status means here
granite4.1:3b
IBM Granite 4.1 [IBM,
2026]
evaluable; recovery MAE
0.054
All three personas varied,
every cell parsed, and the
error-independent solve
returned a selected branch.
mistral:latest
Mistral family [Jiang et al.,
2023]
best recovered model;
recovery MAE 0.012
All three personas varied,
every cell parsed, and the
error-independent solve
returned a selected branch.
gemma2:2b
Gemma and Gemma 2
family [Gemma Team,
2024b,a]
evaluable; recovery MAE
0.026
All three personas varied,
every cell parsed, and the
error-independent solve
returned a selected branch.
gemma3:4b
Gemma family reports
[Gemma Team, 2024b, 2025]
evaluable; recovery MAE
0.024
All three personas varied,
every cell parsed, and the
error-independent solve
returned a selected branch.
gemma4:latest
Gemma family reports
[Gemma Team, 2024b, 2025]
evaluable; recovery MAE
0.024
All three personas varied,
every cell parsed, and the
error-independent solve
returned a selected branch.
smollm2:135m-instruct-q
4_K_S
SmolLM2 family [Ben Allal
et al., 2025]
not solved; constant
persona(s): Optimist,
Neutral, Pessimist
At least one judge never
varied, so the trio carries no
recoverable error signal for
that judge.
Each requested model is asked the same binary task under the same schema. If a primary response violates the schema,
7

## Page 9

the collector allows one model-driven repair attempt using the same scenario facts and the same binary contract. A cell
is accepted only if the model returns one of the two allowed labels; the collector never maps neutral, mixed, malformed
JSON, or an unavailable model into a vote.
3.5
The evaluators
For each model we encode the trio’s votes as TrioLabelVoteCounts and run three ntqr.r2 evaluators [Corrada-Emmanuel
et al., 2026, Corrada-Emmanuel, 2023b]:
• ErrorIndependentEvaluation (unsupervised) — recovers prevalence and each persona’s per-label accuracy from
agreement structure alone, with no answer key. It returns two algebraically consistent solutions (the labelling we
want and its near-zero-accuracy mirror image).
• MajorityVotingEvaluation (unsupervised) — a simpler unsupervised baseline, also returning two solutions.
• SupervisedEvaluation (the check) — the answer-key truth.
Two-solution tie-break.
From the two unsupervised solutions we keep the one with higher mean accuracy — the
standard, answer-key-free “experts are better than random” assumption. We deliberately do not break the tie by closeness
to the true prevalence: that would peek at the ground truth and would fail whenever the two prevalences are symmetric
about 0.5. The derivation is in sec. 7.1.
3.6
The algebra: from votes to accuracies
This section makes the “exact algebra” concrete, because the whole study turns on its structure — including why it
fails. The derivation follows the NTQR complete-postulate and streaming-algorithm line of work [Corrada-Emmanuel,
2023a,b], with the agreement-rate literature as its nearest statistical antecedent [Platanios et al., 2014, 2016]. We follow
the construction in SimplestExampleOfEvaluationWithAlgebraicGeometry.md and the public NTQR implementation
documented for ntqr.r2.evaluators.ErrorIndependentEvaluation [Corrada-Emmanuel et al., 2026].
The universal evaluation polynomial. Write the two labels as 𝛼(bullish, a) and 𝛽(bearish, b), the unknown
test prevalence of 𝛼as 𝑃𝛼(with 𝑃𝛽= 1 −𝑃𝛼), and a single judge’s per-label accuracies as 𝑃𝑖,𝛼and 𝑃𝑖,𝛽. The observed
frequency with which that judge votes 𝛼decomposes — by definition, with no probability model — into “correct on 𝛼
items” plus “wrong on 𝛽items”:
𝑓𝛼= 𝑃𝛼𝑃𝑖,𝛼+ 𝑃𝛽(1 −𝑃𝑖,𝛽).
(1)
This polynomial is exact and universal: any noisy judge on any finite test satisfies it identically. It contains no domain
knowledge — that emptiness is precisely what makes it immune to the out-of-distribution failures of trained estimators.
It is an evaluation thermometer, not a model.
The trio raises the rank. One judge gives two such equations in three unknowns — underdetermined. Three error-
independent judges sharing one test supply enough agreement structure to close the system. The ntqr data sketch is the
eight trio vote-pattern frequencies 𝑓𝑣0𝑣1𝑣2 (each 𝑣𝑖∈{𝛼, 𝛽}, ∑𝑓= 1). From them the evaluator forms three orders of
statistic (shown here for label 𝛽; datasketches.py):
𝑓𝛽𝑖=∑
𝑣𝑗,𝑣𝑘
𝑓…𝑣𝑖=𝛽…,
𝛿(𝑖,𝑗) = 𝑓𝛽𝑖𝛽𝑗−𝑓𝛽𝑖𝑓𝛽𝑗,
𝑚012 =∏
𝑖
𝑓𝛽𝑖+ ∑
(𝑖,𝑗,𝑘)
𝑓𝛽𝑖𝛿(𝑗,𝑘).
(2)
Here 𝑓𝛽𝑖is judge 𝑖’s marginal 𝛽-vote frequency, the pair moment 𝛿(𝑖,𝑗) is the (sample) covariance of judges 𝑖, 𝑗voting 𝛽
— a measured agreement, not a modelled one — and 𝑚012 is the trio frequency moment. The prevalence of 𝛼is then the
root of a quadratic
𝑎𝑃2
𝛼+ 𝑏𝑃𝛼+ 𝑐= 0,
𝑎= Δ2 + 4∏
(𝑖,𝑗)
𝛿(𝑖,𝑗),
𝑏= −𝑎,
𝑐= ∏
(𝑖,𝑗)
𝛿(𝑖,𝑗).
(3)
where Δ = 𝑓𝛽𝛽𝛽−𝑚012 is the gap between the all-𝛽vote frequency and the trio frequency moment 𝑚012 (see alpha_pre
valence_quadratic_terms). Because 𝑏= −𝑎, the closed form collapses to a single ± pair:
𝑃𝛼=
1
2 ∓
1
2√1 −4𝑐/𝑎.
(4)
8

## Page 10

Two solutions, by construction. The ∓is not numerical noise: absent labels, the votes alone admit exactly two logically
consistent evaluation points — the labelling we want and its near-mirror image with the labels swapped. Each judge’s
per-label accuracy is then recovered as an exact linear function of 𝑃𝛼(classifier_a_label_accuracy / classifier_b
_label_accuracy), so fixing the prevalence root fixes all six accuracy terms. The tie-break (sec. 3.5) selects between the
two points without peeking at the truth.
The singularity at 𝑃𝛼= 1
2. The two roots coalesce exactly when 1 −4𝑐/𝑎= 0, i.e. when prevalence sits at 1
2. There the
radical vanishes, both solutions equal 1
2, and the downstream accuracy ratios resolve to 0/0 (NaN). This is the removable
singularity that motivates the deliberately unbalanced deck in sec. 3.3: an exactly 50/50 answer key puts the true prevalence
on the singularity, so any competent ensemble lands on it and cannot be solved. Tilting prevalence to 0.625 moves the
whole problem off the singular point.
The built-in alarm. When the judges are in fact error-correlated on the test, the discriminant 1 −4𝑐/𝑎goes negative
and the prevalence root becomes imaginary — ntqr surfaces this as a PrevalenceImaginaryException. An imaginary
prevalence is an iron-clad, label-free detection that the error-independence assumption is violated: the algebra refuses
to return a number it cannot justify. This is the “warning light” property at the center of the safety framing and the
later no-knowledge alarm formulation [Corrada-Emmanuel et al., 2024, Corrada-Emmanuel, 2025] — and the per-judge
constant-classifier failure of sec. 4.2 is its discrete cousin, which the following makes precise.
Proposition (per-judge evaluability). If any judge 𝑖is a constant classifier — it casts one label on all 𝑄
items — then the error-independent trio has no interior prevalence solution, regardless of the other two judges.
Proof. A constant judge has marginal 𝑓𝛽𝑖∈{0, 1}, so its sample variance is zero and every pair moment
touching 𝑖vanishes, 𝛿(𝑖,𝑗) = 𝑓𝛽𝑖𝛽𝑗−𝑓𝛽𝑖𝑓𝛽𝑗= 0. Hence the product ∏(𝑖,𝑗) 𝛿(𝑖,𝑗) = 0, giving 𝑐= 0 and 𝑎= Δ2.
The quadratic degenerates to Δ2𝑃𝛼(𝑃𝛼−1) = 0, whose only roots are the boundary points 𝑃𝛼∈{0, 1}; the
per-label accuracies then resolve to 0/0 and ntqr returns NaN. ■
This is why disagreement is the wrong axis. The degeneracy is triggered by a per-judge quantity (𝛿(𝑖,⋅) = 0 for a single
𝑖) and is blind to the ensemble quantity of how much the judges collectively disagree. Two judges can disagree violently
while the third sits constant: the product still vanishes and the system is still unsolvable. Conversely the worked example
in sec. 7.2 shows all three pair moments strictly positive on real votes, a positive discriminant, and the two mirror-image
roots resolving to the truth. sec. 4.3 is the empirical face of this proposition; sec. 4.4 turns it into a label-free screen.
3.7
Statistics
• Recovery MAE (headline): mean absolute error between recovered and true per-persona, per-label accuracies. We
also report it split by label.
• Prevalence absolute error: | recovered −true| prevalence of label a.
• Sampling-noise floor: a reference scale for the recovery MAE. A per-label accuracy is estimated from only the
questions carrying that label; the worst-case binomial standard error of such a proportion is sqrt(0.25 / k), where
k is the minority label’s question count (here k = 24, giving a floor of 0.102). A recovery MAE at or below this
floor is smaller than the worst-case uncertainty of the supervised estimate it is compared against. We use it as a
scale reference, not as a formal hypothesis test.
• Degeneracy guard: a constant classifier makes the algebra unsolvable and yields a SymPy nan; because float(nan)
succeeds, we reject non-finite values explicitly (math.isfinite) and report the model as a named failure rather than
averaging NaN into a meaningless statistic.
• Scenario bootstrap: uncertainty for the finite scenario deck is estimated by nonparametric resampling of scenarios
with replacement, following the bootstrap logic of Efron and Tibshirani [Efron and Tibshirani, 1993].
• Evaluability diagnostic (label-free; see sec. 3.8).
3.8
The evaluability diagnostic
Computed from the votes alone — no answer key, no solve:
• Vote variation — for each judge, the fraction of scenarios on its single most common call (modal_fraction). A
value of 1.0 means the judge never varied: a constant classifier, which carries no error signal.
• Pairwise disagreement — for each pair of judges, the fraction of scenarios on which they differ; and its mean over
pairs.
• Verdict — predicted_evaluable = (no judge is constant).
9

## Page 11

3.9
Reproducibility
Everything is exact and offline-reproducible from the cached votes. The numeric core (scripts/llm/_analysis.py) is
pure — no I/O, no plotting — and covered by 99 unit tests that run with no network and no Ollama. The manuscript
itself is generated: every number below is injected from summary.json by scripts/manuscript/render.py, so the prose
cannot drift from the data. Exact commands are in sec. 7.7.
10

## Page 12

4
Results
4.1
Unsupervised recovery works when the ensemble is well-behaved
Among five evaluable models, mistral:latest recovered the authored truth most closely. Its unsupervised recovery tracked
the authored truth to a mean absolute error of 0.012, within the 0.102 sampling-noise floor:
Table 5: Recovered vs. authored-truth per-persona, per-label accuracies for mistral:latest. The recovered columns use
only votes; the truth columns are validation-only.
Persona
Label
True
Recovered
Abs. error
Optimist
a
1.0000
1.0000
0.0000
Optimist
b
0.7917
0.7600
0.0317
Neutral
a
0.9750
1.0000
0.0250
Neutral
b
1.0000
1.0000
0.0000
Pessimist
a
0.5750
0.5897
0.0147
Pessimist
b
1.0000
1.0000
0.0000
• Recovery MAE = 0.012 (by label: a = 0.013, b = 0.011) across six accuracy terms.
• Prevalence: true 0.625, recovered 0.609; absolute error 0.016.
The most striking row is the Pessimist on label a: the pessimist was genuinely bad at the bullish calls (true accuracy 0.57
— it called bearish even when the facts were clearly bullish), and the unsupervised algebra recovered that poor accuracy
as 0.59 (against a true 0.57) — with no answer key. Unsupervised evaluation is not merely detecting who is good; it
is quantifying who is bad. At temperature 0.1 the recovery is close but not exact (recovery MAE 0.012, within the 0.102
sampling-noise floor); §3.5 and the limitations frame this as one stochastic draw, not a general guarantee.
Figure 2: Recovered vs. authored-truth per-persona, per-label accuracy for mistral:latest. Bars track the truth term
for term; the answer-key-free algebra recovers even the Pessimist’s poor bullish accuracy (0.57). Recovery MAE = 0.012.
Across the five evaluable matrices, recovery MAE spans 0.012-0.054 with median 0.024 (tbl. 6). This range is useful
context: NTQR is not merely ranking model quality, and a low recovery error does not mean every judge is good. It means
the algebra recovered the judges’ strengths and weaknesses faithfully. fig. 4 makes that distinction visible: the left panel
shows validation-only true accuracies, while the right panel shows how much the unsupervised recovery missed each term
by.
11

## Page 13

Figure 3: The same recovery as a scatter of recovered vs. true accuracy: points on the diagonal have zero error. For the
evaluable model the terms sit near the line (recovery MAE 0.012).
12

## Page 14

Table 6: Recovery ranking across evaluable model matrices. The MAE columns are computed after the unsupervised
branch is selected; the authored truth is used only to score validation error.
Rank
Model
Recovery MAE
Max term error
Prevalence error
MV MAE
Validation
role
1
mistral:latest
0.012
0.032
0.016
0.012
best
recovered
matrix
2
gemma4:latest
0.024
0.050
0.016
0.024
evaluable
comparison
3
gemma3:4b
0.024
0.050
0.031
0.024
evaluable
comparison
4
gemma2:2b
0.026
0.050
0.031
0.026
evaluable
comparison
5
granite4.1:3b
0.054
0.107
0.062
0.054
evaluable
comparison
Figure 4: Validation-only accuracy landscape across evaluable models. The left panel shows supervised true accuracy by
model/persona/label; the right panel shows absolute error of the unsupervised recovery for the same terms.
How stable is that number? The recovery MAE is one figure from one finite test, so we bootstrap it: resample the 64
scenarios with replacement and re-run the same unsupervised solve on each resample (2000 resamples, no new model calls).
The point estimate is 0.012, with a 95% bootstrap CI of [0.000, 0.038] for the recovery MAE and [0.000, 0.047] for the
prevalence error — the entire interval sits well below the 0.102 sampling-noise floor (fig. 5). In 2% of resamples a persona
happened to collapse to a constant classifier and the solve was unavailable, a concrete measure of how the evaluability
condition (not the recovery accuracy) is the fragile part.
4.2
Failure modes: constant classifiers and non-compliance
The other model collapsed at least one persona into a constant classifier:
Table 7: Per-model constant-classifier diagnostics. A model is evaluable only when every persona varies and every cell is
parseable.
Model
Constant classifier(s)
Evaluable?
granite4.1:3b
—
yes
mistral:latest
—
yes
13

## Page 15

Model
Constant classifier(s)
Evaluable?
gemma2:2b
—
yes
gemma3:4b
—
yes
gemma4:latest
—
yes
smollm2:135m-instruct-q4_K_S
Optimist, Neutral, Pessimist
no
A capable model that follows a strongly-dispositioned persona prompt too rigidly turns that persona into a judge who
answers the same way every time. A constant classifier carries no error signal, so the error-independent system becomes
unsolvable (it returns a degenerate / NaN solution). We report these under failed_models with the offending persona
named, rather than crashing the sweep or emitting a NaN statistic. fig. 6 shows each judge’s modal-vote fraction per model;
bars at 1.0 (red) are the constant classifiers — you can read the failures straight off the votes.
Non-compliance (no fabricated votes). At temperature 0.1, every model returned a parseable vote on all 192 persona
calls – no responses were unparseable, so no model was dropped for non-compliance.
Table 8: Prompt-health diagnostics by model and persona under prompt version v3_binary_schema. Model labels are
compacted for PDF fit; the full model names appear in tbl. 4 and in summary.json. Parse methods and entropy are
derived from cached raw-response records.
Model
Persona
Primary
Repaired
Parsed
Invalid
Modal
Entropy
Parser
mistral
Optimist
1.000
0
64
0
0.703
0.877
schema:64
mistral
Neutral
1.000
0
64
0
0.609
0.965
schema:64
mistral
Pessimist
1.000
0
64
0
0.641
0.942
schema:64
gemma4
Optimist
1.000
0
64
0
0.625
0.954
schema:64
gemma4
Neutral
1.000
0
64
0
0.609
0.965
schema:64
gemma4
Pessimist
1.000
0
64
0
0.578
0.982
schema:64
gemma3
Optimist
1.000
0
64
0
0.688
0.896
schema:64
gemma3
Neutral
1.000
0
64
0
0.594
0.974
schema:64
gemma3
Pessimist
1.000
0
64
0
0.531
0.997
schema:64
gemma2
Optimist
1.000
0
64
0
0.609
0.965
schema:64
gemma2
Neutral
1.000
0
64
0
0.594
0.974
schema:64
gemma2
Pessimist
1.000
0
64
0
0.516
0.999
schema:64
granite
Optimist
1.000
0
64
0
0.609
0.965
schema:64
granite
Neutral
1.000
0
64
0
0.562
0.989
schema:64
granite
Pessimist
1.000
0
64
0
0.516
0.999
schema:64
smollm2
Optimist
1.000
0
64
0
1.000
-0.000
schema:64
smollm2
Neutral
1.000
0
64
0
1.000
-0.000
schema:64
smollm2
Pessimist
1.000
0
64
0
1.000
-0.000
schema:64
The previous temperature 0.7 prompt contract is retained as a stress-test baseline: it parsed 947/1152 cells, whereas the
current temperature 0.1 schema-constrained headline parsed 1152/1152. The comparison isolates interface compliance from
the algebraic evaluability question. fig. 8 shows why the low-temperature schema-constrained run replaces the temperature-
0.7 prompt as the headline experiment: parseability is now an interface check, while evaluable vote matrices remain the
scientific object.
4.3
Disagreement is not evaluability (the non-obvious result)
The intuitive story – “you need the judges to disagree” – is incomplete. In this low-temperature schema run, aggregate
disagreement happens to separate the groups: the one unevaluable model sat at 0.00, while the five evaluable models
spanned 0.03–0.23. That separation is a symptom of the failed model’s constant-classifier collapse, not the algebraic gate.
Table 9: Mean pairwise disagreement by model. Disagreement is not the evaluability gate; per-judge variation is.
Model
Mean pairwise disagreement
Evaluable?
smollm2:135m-instruct-q4_K_S
0.00
no
gemma4:latest
0.03
yes
14

## Page 16

Model
Mean pairwise disagreement
Evaluable?
granite4.1:3b
0.06
yes
gemma2:2b
0.06
yes
gemma3:4b
0.10
yes
mistral:latest
0.23
yes
smollm2:135m-instruct-q4_K_S is unevaluable because one or more personas never varied, not because its ensemble-
disagreement statistic fell below a universal threshold. The reason is structural: evaluability is gated by a per-judge
necessary condition (every judge must vary), not by an ensemble quantity (how much the judges collectively disagree).
A single judge who never varies breaks the algebra no matter how loudly the rest of the ensemble argues. Aggregate
disagreement and per-judge variation are different axes, and only the latter is necessary for a solution to exist. fig. 9 plots
the two axes against each other and shows the evaluable region is gated horizontally (by per-judge variation), not vertically
(by disagreement).
4.4
A label-free diagnostic predicts evaluability
Because the binding condition is per-judge variation, it is detectable from the votes alone. Our evaluability diagnostic —
flagging any judge whose modal-vote fraction is 1.0 — predicted predicted_evaluable = True for exactly gemma2:2b,
gemma3:4b, gemma4:latest, granite4.1:3b, mistral:latest and False for the other one. The ntqr solve then evaluated
exactly mistral:latest, gemma4:latest, gemma3:4b, gemma2:2b, granite4.1:3b.
The prediction and the outcome
agreed on all six models (diagnostic_matched_outcome = true). The diagnostic needs no answer key and no solve: it
is computed directly from the response matrix, making it a usable pre-flight “evaluation thermometer.”
4.5
Majority voting and error-independent recovery coincided here
For mistral:latest, MajorityVotingEvaluation and ErrorIndependentEvaluation returned the same selected solution,
so their recovery MAE was identical (0.012). This is a property of this particular, near-error-independent vote pattern
rather than a general theorem; we report both so the comparison is visible per run.
Majority voting is included because it is the classical aggregation baseline: Condorcet-style jury arguments justify it only
when voters are independent and better than random [Dietrich and Spiekermann, 2021], and LLM self-consistency applies
the same intuition by sampling multiple reasoning paths and taking the modal answer [Wang et al., 2022]. NTQR asks a
different question: not which label wins, but whether the votes contain enough structure to estimate each judge’s accuracy.
4.6
Reading the figure suite together
The 16 embedded figures tell the paper’s arc in one pass. fig. 1 fixes the data boundary: votes enter the unsupervised
solve, and authored truth enters only for validation. fig. 9 is the thesis: evaluability separates along the per-judge-variation
axis, not the disagreement axis. fig. 2 and fig. 3 are the recovery result: for the best evaluable model, recovered and true
accuracies track each other term for term (recovery MAE 0.012), while fig. 11 shows where every evaluable model sits.
fig. 6 is the mechanism: the red 1.0 bars are exactly the judges that broke the algebra. The scorecard headline is: the five
evaluable models sit at recovery MAE 0.012, within the 0.102 sampling-noise floor. Each figure ships a <stem>.data.json
sidecar carrying its exact series and thresholds where applicable, so every plotted value is backed by a machine-readable
number. fig. 4 separates two questions that should not be conflated: how accurate each judge actually was after validation,
and how accurately the unlabeled solve recovered that fact. fig. 7, fig. 8, and fig. 10 expose the prompt interface and
scenario diﬀiculty that determine whether the algebra gets a usable response matrix; the remaining simulation figures
extend the same logic through deterministic simulation, bootstrap uncertainty, the tie-break boundary, and the EI-vs-MV
trade-off.
4.7
Synthetic validation: recovery scaling and the alarm’s blind spot
The five evaluable real models give a finite empirical ranking, not a population estimate.
To test the algebra across
many ensembles — and to probe the failure detector directly — we ran a deterministic companion study on synthetic
judges whose ground truth is set by construction (scripts/sim/synthetic_recovery_study.py; no network, fully
seeded, reproducible). A trio with prevalence 0.55 and per-judge (a, b) accuracies (0.90, 0.80), (0.85, 0.75), (0.70, 0.95)
is sampled under error-independence, its votes are fed through the identical ErrorIndependentEvaluation used on the
LLM votes, and the unsupervised recovery is scored against the sample truth. We average 200 independent draws at each
test size.
15

## Page 17

Figure 5: Bootstrap distribution of the unsupervised recovery MAE over 2000 scenario resamples of mistral:latest. The
point estimate (0.012) and the 95% CI [0.000, 0.038] both sit far below the 0.102 sampling-noise floor; 2% of resamples
were degenerate.
Figure 6: Per-judge modal-vote fraction for every model. A bar at 1.0 marks a constant classifier — a persona whose
parseable calls never varied — which carries no error signal and makes the error-independent solve degenerate. The label-
free read-out of which ensembles are unevaluable.
16

## Page 18

Figure 7: Prompt compliance for the persona-scenario grid. Dark green cells were valid on the first schema-constrained
attempt; light green cells were accepted only after the one allowed model-driven repair retry; red/grey cells remain missing
votes rather than fabricated labels.
Figure 8:
Temperature/schema comparison between the previous temperature-0.7 prompt contract and the current
temperature-0.1 binary-schema run.
Bar height is final parse rate; E marks a model whose final vote matrix was al-
gebraically evaluable.
17

## Page 19

Figure 9: Per-judge modal-vote concentration (x, low = every judge varies) against ensemble mean pairwise disagreement
(y). Evaluable models avoid the constant-classifier boundary; unevaluable models hit it. The y-axis is descriptive, while
the x-axis contains the solvability condition.
Figure 10: Scenario-level vote split and authored direction. Each point is one authored market scenario. The y-value is
the fraction of parsed persona/model calls that were bullish; marker color is the authored operational truth. Points near
0.5 are the hard or intentionally mixed cases that create useful variation.
18

## Page 20

Figure 11: Scorecard: unsupervised recovery MAE for each evaluable model (lower is better), drawn against the “excellent”
(0.05) and sampling-noise-floor (0.102) reference lines. the five evaluable models sit at recovery MAE 0.012, within the
0.102 sampling-noise floor.
19

## Page 21

Recovery error falls like sampling noise. As the test grows from Q = 32 to Q = 4096, the mean recovery MAE drops
from 0.123 to 0.007 (tbl. 10). A log–log fit of error against Q has slope -0.58 (R2 = 0.989; the prevalence error scales
the same way, slope -0.55) — close to the −0.5 of an unbiased, sampling-noise-limited estimator. So the algebra carries
no persistent bias: the only thing between the unsupervised recovery and the truth is finite-sample noise, and the real
mistral:latest result (recovery MAE 0.012 at Q = 64) sits squarely on this curve rather than being a fortunate one-off.
Table 10: Synthetic recovery error vs. test size, averaged over 200 error-independent ensembles per row. Every draw solved
cleanly — no spurious alarms.
Q
Accuracy MAE
Prevalence error
Trials solved
32
0.123
0.117
200/200
64
0.073
0.074
200/200
128
0.040
0.048
200/200
256
0.029
0.036
200/200
512
0.019
0.023
200/200
1024
0.013
0.016
200/200
2048
0.009
0.011
200/200
4096
0.007
0.008
200/200
Figure 12: Unsupervised recovery error vs. test size Q on log–log axes, over 200 synthetic error-independent ensembles per
point (accuracy MAE with ±1 sd error bars; prevalence error overlaid). The dotted line is a 1/√Q reference; the fitted
slope -0.58 (R2 = 0.989) matches the −0.5 of a sampling-noise-limited estimator.
The scaling is not an artifact of one ensemble. Repeating the convergence fit across 4 deliberately different ensembles
— varied prevalence (0.50–0.70) and accuracy spread — keeps every fitted slope in a tight band [-0.60, -0.50] around the
ideal −0.5 (tbl. 11), so the sampling-noise-limited behaviour is a property of the algebra, not of the particular judges we
chose.
20

## Page 22

Table 11: The 1/√Q convergence slope is stable across diverse ensembles, each fitted over the same Q grid. All slopes
cluster near the ideal −0.5.
Ensemble
Prevalence
Fitted slope
𝑅2
balanced p=0.50
0.50
-0.55
0.999
tilted p=0.70
0.70
-0.51
0.995
strong p=0.55
0.55
-0.50
0.997
modest p=0.65
0.65
-0.60
0.986
The alarm is sound but has a blind spot. The error-independent solve carries a built-in failure detector: when the
prevalence quadratic’s discriminant D = 1 −4c/a goes negative the prevalence root is imaginary — an answer-key-free
signal that error-independence is violated. We characterised it by injecting two kinds of dependence at Q = 1024 (tbl. 12,
fig. 13). On genuinely error-independent draws the alarm fired in 0% of trials — no false positives. An anti-correlated
judge pair (which drives a pairwise vote-moment negative) tripped it in up to 94% of trials. But positive common-mode
correlation — all judges sharing a forced error, the natural analogue of shared training data — never tripped it (0%),
even as it silently worsened the recovery it failed to warn about (prevalence error rising from 0.016 under independence to
0.042 at the strongest common-mode setting).
Table 12: Alarm-firing rate by error structure at Q = 1024 (200 trials each). D is the mean prevalence discriminant; the
last column is the recovery error on the trials where the alarm stayed silent.
Error structure
Alarm fires
Mean 𝐷
Recovery error (alarm
silent)
independent
0%
0.0115
0.016
common-mode 0.1
0%
0.0080
0.014
common-mode 0.2
0%
0.0041
0.024
common-mode 0.3
0%
0.0021
0.034
common-mode 0.4
0%
0.0013
0.042
anti-pair 0.2
0%
0.0126
0.043
anti-pair 0.3
40%
0.0962
0.204
anti-pair 0.4
94%
-0.0726
0.407
Figure 13: Left: the imaginary-prevalence alarm fires only under anti-correlation, never on independent or common-mode
data. Right: the mechanism — as common-mode correlation strengthens, the discriminant D falls toward the D = 0 alarm
threshold but never crosses it, while the un-warned recovery error climbs.
This sharpens the safety claim honestly: the imaginary-prevalence alarm is a suﬀicient, never-false-positive detector of
violated error-independence, but it is not necessary — the most realistic LLM failure, positively-correlated errors from
21

## Page 23

shared pre-training, is exactly the regime it can miss. The per-judge evaluability diagnostic (sec. 3.8) and this alarm are
complementary screens, and neither is a substitute for a held-out check when correlated errors are plausible.
4.8
The two-solution tie-break needs clearly-better-than-random judges
Error-independent evaluation returns two mirror-image solutions; we pick the one with higher mean accuracy (sec. 7.1),
the standard better-than-random assumption. That assumption has teeth, and a synthetic sweep shows exactly where it
loses them. We hold the trio symmetric (so mean per-label accuracy is the only varying factor), fix prevalence 0.60 and Q
= 256, and slide the accuracy from strong toward random (tbl. 13, fig. 14). For strong judges the tie-break is essentially
flawless — 0% catastrophic mirror-selection down to accuracy 0.82 — but as the judges approach random the mirror
starts winning by chance and recovery inverts, reaching 85% catastrophic selections near accuracy 0.5. The practical rule:
algebraic recovery is trustworthy only for an ensemble that is clearly better than random; a barely-better-than-chance jury
can be confidently and silently inverted.
Table 13: Catastrophic mirror-selection (prevalence error > 0.25) vs. mean judge accuracy at prevalence 0.60, Q = 256,
200 trials each.
Judge accuracy
Catastrophic mirror-selection
Mean prevalence error
0.90
0%
0.014
0.82
0%
0.039
0.76
4%
0.093
0.70
26%
0.185
0.62
71%
0.421
0.56
85%
0.485
0.52
82%
0.487
Figure 14: The better-than-random tie-break is flawless for strong judges and inverts as the ensemble approaches random:
catastrophic mirror-selection climbs from 0% to 85% and the mean prevalence error rises with it.
22

## Page 24

4.9
Error-independent vs. majority-voting: exactness vs. robustness
sec. 4.5 reported that on mistral:latest the error-independent (EI) and majority-voting (MV) evaluators returned the
same recovery — explicitly “a property of this particular vote pattern, not a general theorem.” The synthetic harness
settles the general question by running both evaluators on the same draws across a prevalence × accuracy grid (Q = 512;
tbl. 14, fig. 15). The answer is a clean trade-off, not a winner:
• EI is more accurate where its assumption holds. For clearly-better-than- random judges the exact algebra
beats majority voting — e.g. at prevalence 0.55, accuracy 0.74, EI’s recovery MAE is 0.047 vs MV’s 0.068 (1.43×
lower), and EI wins on 79% of draws. MV is biased — it assumes the majority vote is the truth — so it cannot reach
the exact answer.
• MV is more robust where EI’s assumption fails. In the tie-break danger zone of sec. 4.8 (weak judges, here
accuracy 0.58 at prevalence 0.70), EI’s mirror inverts and its MAE explodes to 1.098 while MV — which has no
imaginary roots and no mirror — stays at 0.176; EI wins only 18% of draws.
The practical guidance mirrors the diagnostics of sec. 3.8 and sec. 4.8: prefer the exact algebra for an ensemble that
clears the evaluability bar and is clearly better than random, but keep majority voting as the robust fallback when those
conditions are in doubt — and report both, as we do per run.
Table 14: Error-independent vs. majority-voting recovery MAE across a prevalence × accuracy grid (Q = 512, 200 trials
per cell). “EI wins” is the fraction of draws where the exact algebra’s MAE was lower.
Prevalence
Judge accuracy
EI MAE
MV MAE
EI wins
0.55
0.90
0.011
0.011
60%
0.55
0.82
0.023
0.032
83%
0.55
0.74
0.047
0.068
79%
0.55
0.66
0.841
0.116
61%
0.55
0.58
1.235
0.176
25%
0.70
0.90
0.012
0.013
65%
0.70
0.82
0.027
0.031
66%
0.70
0.74
0.059
0.065
64%
0.70
0.66
0.357
0.113
47%
0.70
0.58
1.098
0.176
18%
0.85
0.90
0.018
0.019
61%
0.85
0.82
0.041
0.037
50%
0.85
0.74
0.096
0.063
45%
0.85
0.66
1.589
0.109
25%
0.85
0.58
1.432
0.173
20%
Figure 15: Recovery MAE of the error-independent algebra vs. majority-voting as judge accuracy falls from strong to
near-random, one panel per prevalence. EI is lower while judges are strong, then crosses above and diverges as its tie-break
inverts; MV stays bounded throughout.
23

## Page 25

4.10
Statistical validation matrix
The manuscript’s main claims are checked by a generated validation report rather than by prose alone. scripts/valid
ation/statistical_validation_report.py reads the LLM summary, simulation summaries, bootstrap summary, and
figure sidecars; it does not call models or rerun experiments. The report currently passes 9/9 checks, covering the real
recovery scale, label-free diagnostic, bootstrap uncertainty, synthetic convergence, alarm behavior, tie-break boundary,
EI-vs-MV trade-off, and figure sidecar completeness.
Table 15: Offline validation checks for the manuscript’s load-bearing claims. Each row is computed from generated JSON
artifacts, not hand-audited numbers in prose.
Check
Result
Evidence
Label-free diagnostic matches solver
outcome
PASS
predicted 5; evaluated 5
Real recovery is below sampling-noise
floor
PASS
MAE 0.028 <= floor 0.102
Bootstrap CI remains below
sampling-noise floor
PASS
CI_hi 0.038 <= floor 0.102
Synthetic recovery follows 1/sqrt(Q)
PASS
slope -0.585; R2 0.989
Imaginary-root alarm has zero
independent false alarms
PASS
false alarm 0%
Common-mode dependence is
reported as a blind spot
PASS
alarm 0%; silent error 0.042
Better-than-random tie-break
boundary is quantified
PASS
safe to 0.82; max inversion 85%
EI-vs-MV trade-off has both regimes
PASS
EI win 79%; danger-zone EI win 18%
Every source data figure has a
parseable sidecar
PASS
16/16 sidecars parse
Figure 16: Validation matrix for the statistical claims. Green rows are checks that passed against the generated artifacts;
the evidence labels show the actual thresholds or counts used by each check.
24

## Page 26

5
Discussion
What this shows. On real, contemporary LLM-persona ensembles that satisfy the evaluability condition, purely algebraic,
answer-key-free evaluation recovered per-judge accuracies closely (recovery MAE 0.012, within the 0.102 sampling-noise
floor) – including correctly identifying and quantifying a bad judge. That is the positive existence result: the NTQR logic
is not only theoretically universal but operationally effective on real model vote matrices, while still refusing to solve a
matrix whose judges carry no variation signal.
How it fits the literature.
The result is complementary to crowdsourcing, weak-supervision, and LLM-as-judge
measurement-error methods rather than a replacement for them [Zheng et al., 2017, Ratner et al., 2017, Zheng et al.,
2023, Chen et al., 2026]. Those approaches ask how to infer or aggregate task truth under a model of workers, labeling
functions, or judges; majority-vote and self-consistency baselines ask which answer should win under better-than-random
aggregation assumptions [Dietrich and Spiekermann, 2021, Wang et al., 2022]. This experiment asks a prior algebraic ques-
tion: before using a judge ensemble as an evaluator, does the unlabeled response matrix contain the variation and agreement
structure required for evaluation at all? That is the practical role of the NTQR alarm lineage [Corrada-Emmanuel et al.,
2024, Corrada-Emmanuel, 2025].
The sharper lesson is the warning. The repository frames the safety value of algebraic evaluation as its ability to
“warn you if the ensemble is not good enough.” We make that warning concrete and show it fires correctly: one of six models
was not evaluable, and a label-free diagnostic predicted it in advance. Crucially, the warning is not “did the ensemble
disagree enough?”; the failing model sits at low disagreement because its personas collapsed into constant classifiers. The
correct warning is per-judge: at least one of your judges is a constant classifier. For practitioners assembling LLM juries,
this reframes ensemble design: maximizing diversity/disagreement is neither suﬀicient nor the right target; ensuring every
judge actually exercises both responses across the test is the necessary condition.
Implications for evaluation engineering. The operational lesson is to treat LLM evaluation as measurement engi-
neering, not just answer aggregation. First, make the interface boring: schema-constrained, low-temperature collection
and explicit repair diagnostics should make parseability a controlled boundary, not the headline result. Second, check the
unlabeled matrix before trusting any recovered score: a constant judge is not a weak signal, it is no signal for the trio
algebra. Third, distinguish good judges from recoverable judges: fig. 4 shows that the scientific value is not only finding
high accuracies, but recovering poor or label-specific accuracies without looking at the answer key. That is what makes
the method relevant to LLM-as-judge systems where the evaluator itself is part of the risk surface.
Why strong models fail this way. A strongly dispositioned persona prompt is a recipe for a constant classifier: a
model follows its instruction (“lean bullish”) so rigidly that it casts the same call on every scenario. The very capability
that makes a model a good instruction-follower can make it a useless evaluable judge — in this sweep a capable mid-sized
model collapsed personas into constant classifiers (sec. 4.2). Crucially this is not cured by sampling: it appears here even
at temperature 0.1 (stochastic decoding), so the failure is prompt-induced degeneracy, not a decoding artifact. This is a
caution about over-prompting LLM-as-judge ensembles.
Limitations (and what would falsify the claims).
• Single run, single test. T = 1, Q = 64 — a single stochastic draw at temperature 0.1. The recovery result is one
sample, not a population estimate; because decoding is stochastic, repeating the sweep would now yield a distribution
of recovery MAE (a fixed temperature-0 run could not). A stronger design would repeat the draw many times and
report that distribution, and also vary the scenario set. Decoding is fixed, but the scenario set is itself a finite
sample, so sec. 4.1 bootstraps over it: the recovery MAE carries a 95% CI of [0.000, 0.038] and 2% of resamples are
degenerate — the test-draw uncertainty this limitation flags, now quantified.
• Recovery needs clearly-better-than-random judges. The two-solution tie-break (sec. 7.1) assumes the ensem-
ble beats random; sec. 4.8 shows it stays exact down to accuracy 0.82 but inverts (up to 85% catastrophic) as judges
approach chance. The evaluated mistral:latest judges are well clear of that boundary, but a borderline jury is
not safe.
• Five evaluable models. mistral:latest, gemma4:latest, gemma3:4b, gemma2:2b, granite4.1:3b cleared the
evaluability bar, so the head-to-head recovery ranking compares five real models. The recovery-quality claim rests
on those finite real vote matrices; the failure-mode and diagnostic claims rest on all six. The deterministic synthetic
study (sec. 4.7) extends the recovery-quality claim across 200 ensembles per test size where the ground truth is
known by construction, showing the real result is on-curve, not a fluke.
• Diagnostic is necessary, not proven suﬀicient. “No constant classifier” is a necessary condition for the error-
independent solve; this study shows it was also suﬀicient on these six models, but six models is not a powered test
of suﬀiciency. A model could in principle vary on every judge yet still violate error-independence and recover poorly.
The honest claim is: the diagnostic is a cheap, label-free necessary-condition screen that caught every failure here.
25

## Page 27

• Authored truth. “Truth” is the authors’ defensible call, not a market outcome; it calibrates the check, not the
unsupervised recovery.
Future work. Repeat across temperatures and scenario draws to get a recovery distribution; extend beyond the trio
(larger N, R>2); test whether a softened persona prompt (or light temperature) restores variation in the collapsed judges
and thereby restores evaluability. The synthetic study (sec. 4.7) begins the last of these — it shows positive common-mode
correlation silently degrades recovery without tripping the alarm — and a natural next step is to measure the realized
error-correlation of real LLM juries (e.g. from shared base models) and predict the resulting recovery bias.
26

## Page 28

6
Figures — formal specification
Every figure is regenerated by the pipeline — the real-sweep figures into outputs/llm/multi_llm_personas_evaluatio
n/, the simulation figures into outputs/sim/synthetic_recovery_study/, the bootstrap figure into outputs/sim/boo
tstrap_recovery_ci/, and the validation figure into outputs/validation/statistical_validation/ — and ships a
machine-readable <stem>.data.json sidecar holding its exact series, threshold values, and a provenance block (backend,
model set, temperature 0.1, Q=64, render date). A figure is therefore not an illustration but a typeset view of a data
file: the claim, the encoding, and the numbers are all pinned. Each figure below is specified as claim -> encoding ->
reference lines -> data source.
• fig:disagreement-vs-evaluability (disagreement_vs_evaluability.png; disagreement_vs_evaluability
.data.json) supports sec. 4.3 and sec. 3.6. It plots per-judge modal-vote concentration against mean pairwise
disagreement, with a vertical evaluability band.
• fig:evaluation-pipeline (evaluation_pipeline.png; evaluation_pipeline.data.json) supports sec. 3.1. It
shows which objects are observed, which are inferred by NTQR, and where authored truth enters only as a validation
target.
• fig:best-model-recovery (best_model_recovery.png; best_model_recovery.data.json) supports sec. 4.1. It
uses grouped bars for recovered vs. true per-(persona, label) accuracy, with the sampling-noise floor.
• fig:recovered-vs-true (recovered_vs_true_scatter.png; recovered_vs_true_scatter.data.json) supports
sec. 4.1. It plots true accuracy against recovered accuracy with the 𝑦= 𝑥identity line.
• fig:validation-accuracy-heatmap (validation_accuracy_heatmap.png; validation_accuracy_heatmap.dat
a.json) supports sec. 4.1. It shows validation-only true accuracy and absolute recovery error for every evaluable
model/persona/label term.
• fig:evaluability-diagnostic (evaluability_diagnostic.png; evaluability_diagnostic.data.json) sup-
ports sec. 4.2. It shows per-judge modal-vote fraction by model, with the 1.0 constant-classifier boundary.
• fig:prompt-compliance (prompt_compliance.png; prompt_compliance.data.json) supports sec. 4.2. It sepa-
rates primary-valid cells, repaired-valid cells, final-invalid cells, and unavailable cells under the binary schema.
• fig:temperature-schema-comparison (temperature_schema_comparison.png; temperature_schema_compar
ison.data.json) supports sec. 4.2.
It compares the old temperature-0.7 prompt baseline against the headline
temperature-0.1 schema run on parseability and evaluability.
• fig:scenario-hardness (scenario_hardness.png; scenario_hardness.data.json) supports sec. 2.1. It plots
the fraction of parsed calls that were bullish for each authored scenario, colored by the authored operational truth,
with a 0.5 split line.
• fig:recovery-mae-scorecard (recovery_mae_by_model.png; recovery_mae_by_model.data.json) supports
sec. 4.6. It shows recovery MAE per evaluable model against the 0.05 “excellent” and 0.102 sampling-noise ref-
erence lines.
• fig:synthetic-convergence (synthetic_convergence.png; synthetic_convergence.data.json) supports
sec. 4.7. It plots recovery error against test size on log-log axes, with the 1/sqrt(Q) reference and fitted slope -0.58.
• fig:synthetic-alarm (synthetic_alarm.png; synthetic_alarm.data.json) supports sec. 4.7. It shows alarm
rate, discriminant behavior, and silent recovery error by error structure, with the D = 0 alarm threshold.
• fig:bootstrap-recovery (bootstrap_recovery_mae.png; bootstrap_recovery_mae.data.json) supports
sec. 4.1.
It shows 2000 scenario-resampled recovery-MAE draws, with the point estimate, 95% CI, and 0.102
sampling-noise floor.
• fig:synthetic-tiebreak (synthetic_tiebreak.png; synthetic_tiebreak.data.json) supports sec. 4.8.
It
shows catastrophic mirror-selection and prevalence error as judge accuracy approaches random.
• fig:synthetic-mv-vs-ei (synthetic_mv_vs_ei.png; synthetic_mv_vs_ei.data.json) supports sec. 4.9.
It
compares EI and MV recovery MAE as judge accuracy falls.
• fig:validation-matrix (validation_matrix.png; validation_matrix.data.json) supports sec. 4.10. It reports
generated checks for the manuscript’s load-bearing statistical claims.
The figures are mutually reinforcing: fig. 1 defines the experimental boundary, fig. 9 states the thesis on the right axes,
fig. 6 shows the per-judge mechanism that gates it, fig. 2 and fig. 3 show the positive recovery when the gate is cleared, fig. 4
explains what was actually recovered across models, and fig. 11 scores how close that recovery is to the 0.102 sampling-noise
floor.
27

## Page 29

7
Supplemental material
Companion to the main manuscript. All numbers here are reproduced from generated artifacts: the cached LLM sweep
in outputs/llm/multi_llm_personas_evaluation/ (Ollama backend, temperature 0.1, N=3 personas, T=1 test, Q=64
scenarios, R=2 responses), the deterministic simulation/bootstrap outputs, and the offline validation matrix.
• S1 — The two-solution tie-break
• S1.5 — Worked example: the prevalence algebra on real votes
• S1.6 — Exactly when the imaginary-root alarm fires (and its blind spot)
• S2 — Full per-model label vote counts
• S3 — Full per-persona recovery (mistral:latest)
• S4 — Personas, scenarios, and authored truth
• S5 — Reproduction
• S6 — The evaluability diagnostic, defined
• S7 — Output file inventory
7.1
S1 — The two-solution tie-break
ErrorIndependentEvaluation (and MajorityVotingEvaluation) each return two algebraically consistent solutions for
the trio’s prevalence and per-persona accuracies. The two are a symmetry pair: the labelling we intend, and its mirror
image in which every judge is treated as near-random/anti-correct and the prevalence is reflected about 0.5. Both satisfy
the postulates exactly — the algebra alone cannot distinguish them.
We select with the standard answer-key-free assumption that the judges are better than random: keep the solution
with the higher mean per-judge, per-label accuracy (scripts/llm/_analysis.py::select_best).
Two tempting alternatives are rejected on principle:
1. Pick the solution closest to the true prevalence. This peeks at the ground truth, so it is not unsupervised. It
also fails outright when the two candidate prevalences are symmetric about 0.5 (e.g. 0.46 vs 0.54), where “closest to
0.5” is a coin flip.
2. Pick by internal consistency. Both solutions are exactly consistent — that is the whole point — so consistency
cannot break the tie.
For mistral:latest, the selected solution had mean accuracy ≈0.89 against its mirror’s ≈0.11; the tie-break is unambiguous.
See the two solutions verbatim in outputs/llm/multi_llm_personas_evaluation/models/mistral_latest/evaluati
on_error_independent.json.
7.2
S1.5 — Worked example: the prevalence algebra on real votes
This section runs the sec. 3.6 formalism on mistral:latest’s actual votes — no toy numbers. Every value below is
recomputed by _values.py from the on-disk label_vote_counts.json through ntqr.r2, so it cannot drift from the data.
Step 1 — the data sketch. From the trio’s votes we read the all-bearish vote-pattern frequency and the frequency
moments (label b):
Table 16: Real-vote frequency moments for mistral:latest, recomputed from label_vote_counts.json.
Quantity
Symbol
Value
All-b vote frequency
𝑓𝛽𝛽𝛽
n/a
Trio frequency moment
𝑚012
n/a
Gap
Δ = 𝑓𝛽𝛽𝛽−𝑚012
n/a
Pair moment (Opt,Neu)
𝛿(0,1)
n/a
Pair moment (Opt,Pes)
𝛿(0,2)
n/a
Pair moment (Neu,Pes)
𝛿(1,2)
n/a
Product of pair moments
∏(𝑖,𝑗) 𝛿(𝑖,𝑗)
n/a
All three pair moments are strictly positive — every judge varies and the pairs co-vary — so the product does not vanish
and the system is non-degenerate (contrast sec. 4.2, where a constant classifier drives a pair moment to zero).
Step 2 — the prevalence quadratic. With 𝑎= Δ2 + 4 ∏𝛿and 𝑐= ∏𝛿, the discriminant of 𝑃𝛼= 1
2 ∓1
2√1 −4𝑐/𝑎
evaluates to
28

## Page 30

1 −4𝑐/𝑎= 𝑛/𝑎> 0
⟹
1
2√1 −4𝑐/𝑎= 𝑛/𝑎.
(5)
The discriminant is positive, so the prevalence is real — the algebra finds no error-correlation violation (had it been
negative, ntqr would raise PrevalenceImaginaryException; see sec. 3.6).
Step 3 — the two solutions. The ∓yields the symmetry pair
𝑃𝛼∈{ 𝑛/𝑎, 𝑛/𝑎}.
(6)
mirror images about 1
2. The tie-break (sec. 7.1) selects n/a (higher mean accuracy), against the authored true prevalence
of n/a — an absolute error of n/a, recovered with no answer key. Fixing this root then fixes all six per-persona, per-label
accuracies via the linear maps of sec. 3.6 (tabulated in sec. 7.5).
7.3
S1.6 — Exactly when the imaginary-root alarm fires (and its blind spot)
The sec. 4.7 simulation finds, empirically, that the imaginary-prevalence alarm trips on an anti-correlated judge pair but
never on positive common-mode correlation. That asymmetry is not a quirk of the draws — it falls straight out of the
quadratic. Substituting 𝑎= Δ2 + 4 ∏𝛿and 𝑐= ∏𝛿into the discriminant and simplifying,
𝐷= 1 −4𝑐
𝑎
= Δ2 + 4 ∏𝛿−4 ∏𝛿
Δ2 + 4 ∏𝛿
=
Δ2
Δ2 + 4 ∏𝛿,
(7)
where Δ = 𝑓𝛽𝛽𝛽−𝑚012 and ∏𝛿= 𝛿(0,1) 𝛿(0,2) 𝛿(1,2) is the product of the three pairwise vote-moments. The numerator
Δ2 ≥0 is a square, so (for Δ ≠0) the alarm condition 𝐷< 0 is exactly
Δ2 + 4 ∏𝛿< 0
⟺
∏𝛿< −1
4 Δ2 ≤0.
(8)
Two consequences, both visible in sec. 4.7:
1. The alarm is suﬀicient, never a false positive. 𝐷< 0 forces ∏𝛿< 0 — an odd number of the three pairs are
anti-correlated in their votes. No genuinely error-independent test produces that in expectation, which is why the
independent control fired in 0% of trials.
2. It is blind to positive common-mode correlation. If every pair co-varies positively (∏𝛿> 0), then 𝐷∈(0, 1]
for any strength of that correlation: the root stays real and the alarm is structurally silent. Shared errors only push
every 𝛿(𝑖,𝑗) more positive, enlarging the denominator and driving 𝐷→0+ without ever crossing it — precisely the
sec. 4.7 curve where recovery degraded from 0.016 to 0.042 while the alarm never sounded. The real worked example
above sits in this safe regime: all three 𝛿(𝑖,𝑗) are positive, so 𝐷= 𝑛/𝑎> 0.
The practical reading: the imaginary-root alarm is a genuine, answer-key-free suﬀicient check, but a silent 𝐷is not a
certificate of error-independence — only an absence of the specific anti-correlated signature it can see.
7.4
S2 — Full per-model label vote counts
Vote patterns are ordered (Optimist, Neutral, Pessimist); a = bullish, b = bearish. The outer key is the authored
truth of the scenario. Counts sum to 64 (40 bullish a, 24 bearish b).
granite4.1:3b — evaluable (every judge varies):
Truth
Vote pattern
Count
a (bullish)
a,a,a
33
a
a,b,b
3
a
a,a,b
3
a
b,b,b
1
b (bearish)
b,b,b
24
Per-judge: Optimist a×39/b×25, Neutral a×36/b×28, Pessimist a×33/b×31 →no constant classifier.
mistral:latest — evaluable (every judge varies):
29

## Page 31

Truth
Vote pattern
Count
a (bullish)
a,a,a
23
a
a,a,b
16
a
a,b,b
1
b (bearish)
b,b,b
19
b
a,b,b
5
Per-judge: Optimist a×45/b×19, Neutral a×39/b×25, Pessimist b×41/a×23 →no constant classifier.
gemma2:2b — evaluable (every judge varies):
Truth
Vote pattern
Count
a (bullish)
a,a,a
33
a
a,a,b
5
a
a,b,b
1
a
b,b,b
1
b (bearish)
b,b,b
24
Per-judge: Optimist a×39/b×25, Neutral a×38/b×26, Pessimist a×33/b×31 →no constant classifier.
gemma3:4b — evaluable (every judge varies):
Truth
Vote pattern
Count
a (bullish)
a,a,a
34
a
a,a,b
4
a
a,b,b
1
a
b,b,b
1
b (bearish)
b,b,b
19
b
a,b,b
5
Per-judge: Optimist a×44/b×20, Neutral a×38/b×26, Pessimist a×34/b×30 →no constant classifier.
gemma4:latest — evaluable (every judge varies):
Truth
Vote pattern
Count
a (bullish)
a,a,a
37
a
b,b,b
1
a
a,a,b
1
a
a,b,b
1
b (bearish)
b,b,b
23
b
a,a,b
1
Per-judge: Optimist a×40/b×24, Neutral a×39/b×25, Pessimist a×37/b×27 →no constant classifier.
smollm2:135m-instruct-q4_K_S — Optimist and Neutral and Pessimist constant:
Truth
Vote pattern
Count
a (bullish)
a,a,a
40
b (bearish)
a,a,a
24
Optimist, Neutral, Pessimist never varied →two constant classifiers (Optimist, Neutral, Pessimist).
30

## Page 32

7.5
S3 — Full per-persona recovery (mistral:latest)
Unsupervised recovery (ErrorIndependentEvaluation, better-than-random branch) vs. supervised truth. Source: model
s/mistral_latest/comparison.json and recovery_stats.json.
Table 17: Full per-persona recovery table for mistral:latest, with the selected unsupervised branch compared to the
supervised check.
Persona
Label
True
Recovered
Abs. error
Optimist
a
1.0000
1.0000
0.0000
Optimist
b
0.7917
0.7600
0.0317
Neutral
a
0.9750
1.0000
0.0250
Neutral
b
1.0000
1.0000
0.0000
Pessimist
a
0.5750
0.5897
0.0147
Pessimist
b
1.0000
1.0000
0.0000
• Recovery MAE = 0.0119 over six accuracy terms (close recovery, within the 0.102 sampling-noise floor).
• Recovery MAE by label: a = 0.0132, b = 0.0106.
• Prevalence (label a): true 0.6250, recovered 0.6094, abs. error 0.0156.
• Majority-voting recovery MAE = 0.0119 (identical to error-independent here).
Exact fractions (from evaluation_*.json): recovered prevalence = 39/64; Optimist(b) = 19/25; Neutral = 1; Pessimist(a)
= 23/39. The recovered values are close to the supervised truth, not exact; the residual error is the finite-test recovery
error reported above and remains within the 0.102 sampling-noise floor.
7.6
S4 — Personas, scenarios, and authored truth
7.6.1
Persona system prompts (verbatim)
Prompt contract: v3_binary_schema (4d157f84885a).
Table 18: Versioned persona system prompts. The optimist and pessimist policies bias only genuinely mixed cases and
explicitly allow evidence to override the persona.
Persona
System prompt
Optimist
You classify next-quarter equity direction from the stated
facts only. Use the Optimist decision policy: in genuinely
mixed cases, give slightly more weight to upside catalysts
and recovery paths. If the evidence is exactly balanced,
choose bullish. Do not force optimism when explicit
negative evidence dominates; such cases should be bearish.
Return valid JSON only.
Neutral
You classify next-quarter equity direction from the stated
facts only. Use the Neutral decision policy: weigh positive
and negative evidence symmetrically, with no directional
prior. Make the call the evidence best supports; if it is
close, still choose the stronger stated side. Return valid
JSON only.
Pessimist
You classify next-quarter equity direction from the stated
facts only. Use the Pessimist decision policy: in genuinely
mixed cases, give slightly more weight to downside risks
and execution failure. If the evidence is exactly balanced,
choose bearish. Do not force pessimism when explicit
positive evidence dominates; such cases should be bullish.
Return valid JSON only.
Each persona receives the scenario and this user prompt:
31

## Page 33

Market scenario:[scenario text]Task: classify the asset’s expected direction over the next quarter.Use only the
facts stated above; do not assume outside market data.Choose exactly one allowed value for call: bullish or
bearish.No neutral, no mixed, no abstention, and no explanation are allowed. If evidence is mixed, choose the
allowed side implied by your persona policy.Return exactly one JSON object and no other text, for example
{“call”:“bullish”} or {“call”:“bearish”}.
7.6.2
Scenarios and authored truth (Q = 64)
Table 19: Full generated scenario list and authored operational truth. These truths are validation-only and are not visible
to the unsupervised evaluator.
ID
Truth
Scenario
s01
bullish
Revenue grew 42% YoY, beat
estimates, and management raised
full-year guidance.
s02
bearish
The company missed earnings for the
third straight quarter and cut its
dividend.
s03
bullish
A blockbuster drug just received FDA
approval ahead of schedule with a
broad label.
s04
bearish
Regulators opened a fraud probe and
the CFO abruptly resigned this
morning.
s05
bullish
Free cash flow doubled, the firm
initiated a large buyback, and debt
fell sharply.
s06
bearish
A key patent was invalidated and two
generic competitors announced
launches.
s07
bullish
The company signed a multi-year
supply contract with the largest buyer
in its sector.
s08
bearish
Inventory is piling up, margins
compressed 600bps, and demand
guidance was withdrawn.
s09
bullish
Same-store sales accelerated, traﬀic is
up, and the loyalty program is
growing fast.
s10
bearish
A major data breach exposed millions
of customers and class-action suits are
filed.
s11
bullish
The central bank signaled rate cuts
and the company is highly
rate-sensitive on the upside.
s12
bearish
The main product was recalled for a
safety defect and shipments are
halted.
s13
bullish
Order backlog hit a record and lead
times extended, signaling robust
demand.
s14
bearish
A larger rival slashed prices 30% to
take share in the company’s core
market.
s15
bullish
Gross margins expanded for the fifth
straight quarter as input costs fell.
32

## Page 34

ID
Truth
Scenario
s16
bearish
The firm issued a going-concern
warning and is in breach of its loan
covenants.
s17
bullish
A respected activist investor took a
9% stake and won three board seats.
s18
bearish
Key engineering talent is leaving and
the flagship project slipped a full year.
s19
bullish
Earnings beat but guidance was
merely in line; shares are near all-time
highs. (mixed)
s20
bearish
Sales grew but margins thinned and
the macro outlook for the sector is
murky. (mixed)
s21
bullish
A turnaround plan is showing early
traction though leverage remains
elevated. (mixed)
s22
bearish
A one-time gain flattered profit while
underlying organic growth stalled.
(mixed)
s23
bullish
New management is cutting costs
aggressively and reinvesting in a
growing niche. (mixed)
s24
bearish
The stock is cheap on paper but sits
in a structurally declining industry.
(mixed)
s25
bullish
A new product line sold out within
hours and the company doubled its
production targets.
s26
bullish
The company won a multi-year
government contract that triples its
addressable market.
s27
bullish
Subscriber growth reaccelerated and
monthly churn fell to a multi-year low.
s28
bullish
A long-running patent suit was settled
in the company’s favor with a large
damages award.
s29
bullish
Operating leverage kicked in: revenue
rose 20% while operating expenses
stayed flat.
s30
bullish
The firm raised full-year guidance
twice this quarter as bookings
outpaced every forecast.
s31
bullish
A strategic partner took a minority
stake at a premium and committed to
joint development.
s32
bullish
Margins hit a record after the firm
exited its lowest-margin segment and
raised prices.
s33
bullish
Posted record annual revenue and free
cash flow and initiated its first-ever
dividend.
s34
bullish
A flagship product launch drew record
preorders and sold out within a day.
s35
bullish
Regulators granted a breakthrough
designation that fast-tracks the lead
program.
33

## Page 35

ID
Truth
Scenario
s36
bullish
Closed an all-cash, immediately
accretive acquisition that added no
new debt.
s37
bullish
Its credit rating was upgraded to
investment grade and borrowing costs
fell sharply.
s38
bullish
Signed its largest-ever enterprise
contract, a multi-year committed deal.
s39
bullish
Margins expanded as a new
automated plant came online ahead of
schedule.
s40
bullish
A major competitor exited the
segment, leaving the firm the
dominant supplier.
s41
bullish
Recurring revenue crossed 80% of sales
as customer churn hit a record low.
s42
bullish
Won a landmark licensing deal that
monetizes its previously idle patent
portfolio.
s43
bullish
Order backlog doubled year over year
on accelerating enterprise demand.
s44
bullish
Raised full-year guidance after a
blowout quarter across every segment.
s45
bullish
A cornerstone investor took a large
stake at a premium to the market
price.
s46
bullish
Grew its net cash position while
retiring high-coupon debt early.
s47
bullish
International expansion beat plan and
the new region turned profitable
quickly.
s48
bullish
A long-delayed product cleared its
final certification with no conditions
attached.
s49
bearish
Slashed full-year guidance twice
within a single month as demand
evaporated.
s50
bearish
A surprise goodwill writedown wiped
out the entire quarter’s profit.
s51
bearish
Its largest customer terminated a
contract and switched to a direct rival.
s52
bearish
An accounting restatement triggered a
delayed filing and an SEC inquiry.
s53
bearish
A safety recall halted production of its
top-selling product line.
s54
bearish
Debt covenants were breached and
lenders demanded immediate
renegotiation.
s55
bearish
The CEO and CFO resigned in the
same week amid a board dispute.
s56
bearish
A core patent expired and generic
rivals immediately flooded the market.
s57
bullish
Revenue beat expectations but the
firm guided conservatively citing
macro caution.
34

## Page 36

ID
Truth
Scenario
s58
bearish
Margins held up but unit volumes
quietly declined for a third straight
quarter.
s59
bullish
A costly restructuring is underway but
early customer cohorts show real
traction.
s60
bearish
A buyback was announced even as
several insiders sold into the news.
s61
bullish
Cash burn continues but a recent raise
extends the runway by two years.
s62
bearish
Headline growth impressed but was
driven entirely by one large one-off
deal.
s63
bullish
The dividend was trimmed to fund a
high-return capacity expansion.
s64
bearish
The stock screens cheap but sits in a
slowly shrinking end market.
Authored prevalence: 40 bullish (a) / 24 bearish (b) →true prevalence of a = 0.625. The deck is intentionally
tilted off an even 50/50: an exactly balanced answer key would put the true prevalence at 1/2, a removable singularity
of the error-independent evaluator where its accuracy equations degenerate to NaN (see sec. 3.3). The 24 clear bearish
scenarios keep even the bullish-leaning personas casting both calls, so no judge collapses to a constant classifier.
7.7
S5 — Reproduction
All commands run from the repository root. The sweep is reproducible offline from the cached votes (outputs/llm/.../
cache.json); only a fresh --set refresh=true run needs a live Ollama.
# 1. Project test suite (no network, no Ollama, no TeX):
.venv/bin/python -m pytest tests/ -q
# 99 tests
#
or: cd python && ../.venv/bin/python -m pytest -q
# 22 library tests
# 2. Regenerate the multi-LLM sweep from the cache (JSON + figures):
.venv/bin/python scripts/llm/multi_llm_personas_evaluation.py
# 2b. Regenerate the deterministic synthetic-validation study (no network):
.venv/bin/python scripts/sim/synthetic_recovery_study.py
# 2c. Bootstrap a CI on the real recovery MAE (deterministic, offline):
.venv/bin/python scripts/sim/bootstrap_recovery_ci.py
# 2d. Regenerate the offline statistical validation matrix:
.venv/bin/python scripts/validation/statistical_validation_report.py
# 3. Re-inject the numbers into the manuscript (generated from templates):
.venv/bin/python scripts/manuscript/render.py
.venv/bin/python scripts/manuscript/render.py --check
# verify no drift
.venv/bin/python scripts/z_generate_manuscript_variables.py
# 4. Run the whole orchestrator harness including the LLM category:
.venv/bin/python scripts/run_all.py --include llm
# 5. Re-query live models (requires `ollama serve` and the pulled models):
.venv/bin/python scripts/llm/multi_llm_personas_evaluation.py \
--set refresh=true --set timeout=45
# 6. Run a custom model list:
35

## Page 37

.venv/bin/python scripts/llm/multi_llm_personas_evaluation.py \
--set models='["granite4.1:3b","mistral:latest"]'
Lint/format used in this study: .venv/bin/ruff check scripts tests and .venv/bin/black --check -l 79 script
s tests.
7.8
S6 — The evaluability diagnostic, defined
Computed from the vote matrix alone — no answer key, no solve (scripts/llm/_analysis.py):
• vote_variation(votes) →per judge: distinct_calls, call_counts, modal_fraction = (count of the most
common call) / Q, and is_constant = (only one distinct call seen). modal_fraction == 1.0 ⇔is_constant.
• pairwise_disagreement(votes) →for each judge pair, the fraction of the Q scenarios on which they differ; plus
the mean over the three pairs.
• evaluability_diagnostic(votes) →predicted_evaluable = (no judge is_constant), plus the named consta
nt_classifiers and the mean pairwise disagreement.
Predictive check (this study). The orchestrator records, in summary.json →evaluability_diagnostic, whether
the label-free predicted_evaluable set equals the set of models the ntqr solve actually evaluated.
Result: diagn
ostic_matched_outcome = true — predicted evaluable = gemma2:2b, gemma3:4b, gemma4:latest, granite4.1:3b,
mistral:latest = actually evaluated.
Disagreement vs. evaluability (the key contrast).
Model
Mean pairwise disagreement
Constant classifier?
Evaluable
smollm2:135m-instruct-
q4_K_S
0.000
yes (Optimist, Neutral,
Pessimist)
no
gemma4:latest
0.031
no
yes
granite4.1:3b
0.062
no
yes
gemma2:2b
0.062
no
yes
gemma3:4b
0.104
no
yes
mistral:latest
0.229
no
yes
In this low-temperature schema run, disagreement happens to sort the models because the only unevaluable model is
a zero-disagreement constant-classifier collapse. That is not the NTQR solvability rule; it is a visible symptom of the
per-judge rule. The diagnostic therefore keys on per-judge variation, not on ensemble disagreement.
7.9
S7 — Output file inventory
Per sweep, under outputs/llm/multi_llm_personas_evaluation/:
• summary.json — cross-model ranking, evaluability-diagnostic block, the requested/evaluated/failed model sets.
• cache.json — shared response cache, keyed by backend / model / temperature / prompt-version / prompt
-hash / persona / scenario. New records include every raw attempt, parse method, schema-valid flag, invalid
reason, parsed call, repair status, and prompt version/hash.
• disagreement_vs_evaluability.png, recovery_mae_by_model.png, recovered_vs_true_scatter.png, evalua
bility_diagnostic.png, prompt_compliance.png, temperature_schema_comparison.png, scenario_hardness
.png, best_model_recovery.png — the figures, each with a <stem>.data.json sidecar.
• models/<sanitized-model>/ — per model: votes.json, label_vote_counts.json, evaluability_diagnostic.
json, evaluation_error_independent.json, evaluation_majority_voting.json, evaluation_supervised.js
on, comparison.json, recovery_stats.json, comparison_majority_voting.json, recovery_stats_majority_
voting.json.
Degenerate models still emit votes.json, label_vote_counts.json, and evaluability_diagnostic.json (the inputs
that explain the failure); they do not emit the recovery files, because there is no finite solution to record.
Additional generated artifacts:
• outputs/sim/synthetic_recovery_study/ — deterministic convergence, dependence/alarm, tie-break, robustness,
and EI-vs-MV sweeps; each embedded figure has a parseable .data.json sidecar.
• outputs/sim/bootstrap_recovery_ci/ — scenario-bootstrap summary, bootstrap_recovery_mae.png, and boo
tstrap_recovery_mae.data.json.
36

## Page 38

• outputs/validation/statistical_validation/ — offline validation report (summary.json), validation-matrix
figure, and validation_matrix.data.json.
37

## Page 39

8
References
The bibliography is generated from manuscript/references.bib. The central package citation is the public NTQR 0.8
documentation [Corrada-Emmanuel et al., 2026], which documents the ntqr.r2 evaluators and trio data sketches used
here. This repository is cited as the reproducible experiment artifact [Friedman, 2026], and Ollama is cited for the local
model runtime [Ollama, 2026a].
Supplemental material (tie-break derivation, full vote tables, per-persona recovery, scenario list, reproduction commands,
diagnostic definition): supplemental.md.
38

## Page 40

References
Loubna Ben Allal, Anton Lozhkov, Elie Bakouch, Gabriel Martín Blázquez, Guilherme Penedo, et al. SmolLM2: When
smol goes big – data-centric training of a small language model. arXiv preprint arXiv:2502.02737, 2025. doi: 10.48550
/arXiv.2502.02737. URL https://arxiv.org/abs/2502.02737.
Yiqun T. Chen, Sizhu Lu, Sijia Li, Moran Guo, and Shengyi Li. Eﬀicient inference for noisy LLM-as-a-judge evaluation.
arXiv preprint arXiv:2601.05420, 2026. doi: 10.48550/arXiv.2601.05420. URL https://arxiv.org/abs/2601.05420.
Andrés Corrada-Emmanuel.
The logic of NTQR evaluations of noisy AI agents: Complete postulates and logically
consistent error correlations.
arXiv preprint arXiv:2312.05392, 2023a.
doi:
10.48550/arXiv.2312.05392.
URL
https://arxiv.org/abs/2312.05392.
Andrés Corrada-Emmanuel. Streaming algorithms for evaluating noisy judges on unlabeled data – binary classification.
arXiv preprint arXiv:2306.01726, 2023b. doi: 10.48550/arXiv.2306.01726. URL https://arxiv.org/abs/2306.01726.
Andrés Corrada-Emmanuel. No-knowledge alarms for misaligned LLMs-as-judges. arXiv preprint arXiv:2509.08593, 2025.
doi: 10.48550/arXiv.2509.08593. URL https://arxiv.org/abs/2509.08593.
Andrés Corrada-Emmanuel, Ilya Parker, and Ramesh Bharadwaj. A logical alarm for misaligned binary classifiers. arXiv
preprint arXiv:2409.11052, 2024. doi: 10.48550/arXiv.2409.11052. URL https://arxiv.org/abs/2409.11052.
Andrés Corrada-Emmanuel, Walker Lee, and Adam Sloat. NTQR 0.8 Documentation, 2026. URL https://ntqr.readthe
docs.io/en/latest/. Public documentation for the NTQR Python package; copyright 2026, Andrés Corrada-Emmanuel,
Walker Lee, Adam Sloat.
A. P. Dawid and A. M. Skene. Maximum likelihood estimation of observer error-rates using the EM algorithm. Journal
of the Royal Statistical Society: Series C (Applied Statistics), 28(1):20–28, 1979. doi: 10.2307/2346806.
Franz Dietrich and Kai Spiekermann.
Jury theorems.
The Stanford Encyclopedia of Philosophy, 2021.
URL https:
//plato.stanford.edu/entries/jury-theorems/.
Bradley Efron and Robert J. Tibshirani.
An Introduction to the Bootstrap.
Chapman & Hall/CRC, 1993.
ISBN
9780412042317.
Daniel Ari Friedman.
Ntqr llm personas: Algebraic evaluation of unlabeled persona votes, 2026.
Local reproducible
research project.
Gemma Team. Gemma 2: Improving open language models at a practical size. arxiv preprint arxiv:2408.00118, Google
DeepMind, 2024a. URL https://arxiv.org/abs/2408.00118.
Gemma Team. Gemma: Open models based on gemini research and technology. arxiv preprint arxiv:2403.08295, Google
DeepMind, 2024b. URL https://arxiv.org/abs/2403.08295.
Gemma Team. Gemma 3 technical report. arxiv preprint arxiv:2503.19786, Google DeepMind, 2025. URL https://arxiv.
org/abs/2503.19786.
IBM. Granite 4.1: IBM foundation models, 2026. URL https://www.ibm.com/granite/docs/models/granite4-1.
Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas,
Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux,
Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed. Mistral 7B.
arXiv preprint arXiv:2310.06825, 2023. doi: 10.48550/arXiv.2310.06825. URL https://arxiv.org/abs/2310.06825.
Ollama. Structured outputs, December 2024. URL https://ollama.com/blog/structured-outputs.
Ollama. Ollama local model runtime, 2026a. URL https://ollama.com/.
Ollama. Structured outputs, 2026b. URL https://docs.ollama.com/capabilities/structured-outputs. Oﬀicial Ollama
documentation.
Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal,
Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda Askell,
Peter Welinder, Paul Christiano, Jan Leike, and Ryan Lowe. Training language models to follow instructions with
human feedback. In Advances in Neural Information Processing Systems, volume 35, pages 27730–27744, 2022. doi:
10.48550/arXiv.2203.02155. URL https://arxiv.org/abs/2203.02155.
39

## Page 41

Emmanouil Antonios Platanios, Avrim Blum, and Tom M. Mitchell.
Estimating accuracy from unlabeled data.
In
Proceedings of the 30th Conference on Uncertainty in Artificial Intelligence, pages 643–652. AUAI Press, 2014. URL
https://www.auai.org/uai2014/acceptedPapers.shtml.
Emmanouil Antonios Platanios, Avinava Dubey, and Tom Mitchell. Estimating accuracy from unlabeled data: A Bayesian
approach.
In Proceedings of the 33rd International Conference on Machine Learning, volume 48 of Proceedings of
Machine Learning Research, pages 1416–1425. PMLR, 2016. URL https://proceedings.mlr.press/v48/platanios16.html.
Alexander Ratner, Stephen H. Bach, Henry Ehrenberg, Jason Fries, Sen Wu, and Christopher Ré. Snorkel: Rapid training
data creation with weak supervision. Proceedings of the VLDB Endowment, 11(3):269–282, 2017. doi: 10.14778/31577
94.3157797. URL https://www.vldb.org/pvldb/vol11/p269-ratner.pdf.
Guanghui Wang, Jinze Yu, Xing Zhang, Dayuan Jiang, Yin Song, Tomal Deb, Xuefeng Liu, and Peiyang He. STED and
consistency scoring: A framework for evaluating LLM structured output reliability. arXiv preprint arXiv:2512.23712,
2025. doi: 10.48550/arXiv.2512.23712. URL https://arxiv.org/abs/2512.23712.
Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou.
Self-consistency improves chain of thought reasoning in language models. arXiv preprint arXiv:2203.11171, 2022. doi:
10.48550/arXiv.2203.11171. URL https://arxiv.org/abs/2203.11171.
Yan Yan, Romer Rosales, Glenn Fung, Mark Schmidt, Gerardo Hermosillo, Luca Bogoni, Linda Moy, and Jennifer Dy.
Modeling annotator expertise: Learning when everybody knows a bit of something. In Proceedings of the 13th Interna-
tional Conference on Artificial Intelligence and Statistics, volume 9 of Proceedings of Machine Learning Research, pages
932–939. PMLR, 2010. URL https://proceedings.mlr.press/v9/yan10a.html.
Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li,
Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica. Judging LLM-as-a-judge with MT-bench
and Chatbot Arena. arXiv preprint arXiv:2306.05685, 2023. doi: 10.48550/arXiv.2306.05685. URL https://arxiv.org/
abs/2306.05685.
Yudian Zheng, Guoliang Li, Yuanbing Li, Caihua Shan, and Reynold Cheng. Truth inference in crowdsourcing: Is the
problem solved?
Proceedings of the VLDB Endowment, 10(5):541–552, 2017. doi: 10.14778/3055540.3055547. URL
https://www.vldb.org/pvldb/vol10/p541-zheng.pdf.
40


---
*Extraction method: pymupdf*
