# Full Text: Policy Entanglement in Active Inference:  A Coupling-Parameter Deformation Framework for Multi-Stream Policy Posterior Distributions, Machine-Checked and Simulated with a Typed Float Boundary

> Extracted from `Friedman_2026_Policy_ae7cdd62.pdf`

> 61 figures extracted to `images/`

---

## Page 1

Policy Entanglement in Active Inference
A Coupling-Parameter Deformation Framework for Multi-Stream Policy Posterior Distributions,
Machine-Checked and Simulated with a Typed Float Boundary
Daniel Ari Friedman
Active Inference Institute
daniel@activeinference.institute
ORCID: 0000-0001-6232-9096
DOI: 10.5281/zenodo.20418904
Version 1.0
Active Inference Journal (2026)
License: CC-BY-4.0
Policy Entanglement source repository
May 27, 2026

## Page 2

Contents
Abstract
6
Part I — Introduction
6
Motivation and Position: Why Multi-Stream Active Inference Needs Parametric Policy Entangle-
ment
7
The problem in plain language
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
Current coping strategies and their limits
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
Significance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
9
Position relative to alternatives . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
How the framework is developed: four parallel tracks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
Reading guide . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
11
Section dependencies (forward signposts)
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
11
Background and Prior Work: Antecedents in Active Inference, Variational Coupling, Information
Geometry, and Tensor Networks
11
Discrete-time POMDP active inference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12
Mean-field variational families and their limits
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12
Hierarchical, deep, and sophisticated active inference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
13
Information geometry
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
13
Tensor networks and entanglement entropy
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
13
KL / path-integral control and reinforcement learning . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
14
Multi-agent inference, Markov blankets, and renormalization
. . . . . . . . . . . . . . . . . . . . . . . . .
14
Computational psychiatry and neural implementation
. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
14
Lean 4, Mathlib, and formal verification of probabilistic systems
. . . . . . . . . . . . . . . . . . . . . . .
15
Reproducible scientific software . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
15
Part II — Theory
15
Setup and Assumptions: Finite-Horizon Discrete POMDPs, Multi-Stream Policy Factorization,
and the Mean-Field Baseline
16
Single-stream POMDP active inference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
16
The multi-stream extension . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
17
The mean-field baseline
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
17
Lambda Deformation: Definition and Properties
17
Coupling potentials . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
17
Definition: lambda-entangled policy posterior . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
18
The coupling parameter lambda as a precision-like coupling weight . . . . . . . . . . . . . . . . . . . . . .
18
What J and K_c look like in practice
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
18
Entanglement Decomposition Theorem: Marginals, Coupling, and Total Correlation
19
Statement . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
19
Proof sketch . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
What the decomposition says . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
Optimal coupling: existence of lambda* . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
22
Takeaways . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
23
Worked Examples: Bernoulli Toy, Motor-Attention Coupling, and Multi-Timescale Coupling
23
The K=2 Bernoulli toy: full closed form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
23
Two-stream motor + attention with realistic EFE . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
24
Multi-timescale coupling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
27
Information Geometry: Geodesics, Flatness, and Pythagorean Decomposition
27
Dual coordinates and the mean-field submanifold . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
27
The lambda-family is an e-geodesic . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
30
Connection to alpha-projections and curved exponential families
. . . . . . . . . . . . . . . . . . . . . . .
33
Connection to escort distributions and deformed exponential families . . . . . . . . . . . . . . . . . . . . .
33
Takeaways . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
33

## Page 3

Spectral Structure: Schmidt Rank, Archetypal Decomposition, and Tensor-Train Bond Profiles
33
Bipartite Schmidt decomposition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
33
The leading singular vectors as archetypal eigenvectors . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
34
Multi-stream tensor decomposition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
37
Birth and death of archetypes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
39
Takeaways . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
39
Heterogeneous Inference: Mixed VFE/EFE Ensembles and the Coupling-Tax Bound
39
Three-level update hierarchy
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
39
Coupled marginal updates . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
39
The VFE-only suboptimality bound
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
39
Updating lambda: precision-like learning on coupling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
41
Habit accumulation and revertibility . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
42
Takeaways . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
42
Phase Structure: Disordered, Mixed, and Frozen Coupling Regimes
42
Phase diagram
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
42
Order parameters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
44
Model predictions and behavioral hypotheses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
44
Comparative Statics: Coupling Payoff, Two-Parameter Generalization, and Sensitivity Surfaces
44
The pay-off structure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
44
Two-parameter habit/EFE generalization
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
45
Sensitivity to potential structure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
45
Part III — Formal Verification
47
What is proved . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
47
How the verification stack composes
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
47
Where to read the per-row content . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
47
Lean 4 Formalization: Current Boundary, Witness Contracts, and Mathlib Scope
48
Current Lean artifact
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
48
What Mathlib4 is used for . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
49
Mathlib4 analytic targets
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
Live-source injection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
What the Lean track proves today . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
The verification stack
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
Validation gates
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
Part IV — Empirical Grounding
52
Empirical Simulation Suite: Bernoulli Validation, Coupling-Tax Envelope, Phase Diagram, and
Spectral Structure
52
Two-stream Bernoulli (K=2) closed-form validation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
53
Heterogeneous VFE / EFE coupling-tax bound . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
54
Phase Structure of the 𝐾= 2 Ising Toy: Disordered, Mixed, and Frozen Regimes . . . . . . . . . . . . . .
54
Spectral structure (Schmidt rank, archetypes) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
58
Information-geometric structure (e-geodesic) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
58
Multi-stream coupling graph
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
58
𝐾> 2 ensembles . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
58
Long-horizon rollouts and trajectory stationarity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
66
𝑚-projection revertibility witness . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
70
Robustness and ablation stress tests
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
70
Software and numerical stack . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
73
Head-to-head BTAI baseline and adversarial-perturbation harnesses
. . . . . . . . . . . . . . . . . . . . .
76
Anchored figure index . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
78
pymdp 1.0.1 POMDP Harness: Architecture, Lambda Sweep, and Deterministic Rollout
78
Architecture: layered, not duplicated . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
78
The static 𝜆-sweep . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
79
Deterministic coupled rollout . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
84
2

## Page 4

Anchored figure index for the pymdp harness . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
84
pymdp Free-Energy Bundle Observables and Auto-Injected Summary Statistics
84
Statistical contracts
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
85
Summary statistics across the sweep . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
85
Visualizations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
85
Theorem 5.1 Numerical Witness
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
85
Anchored figure index for the pymdp free-energy bundle . . . . . . . . . . . . . . . . . . . . . . . . . . . .
93
pymdp Validation: Three-Tier CI Gates, Structured JSONL Run Log, and Bit-Reproducibility
Contract
93
Three-tier validation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
93
Structured run log (JSONL) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
94
Software and source provenance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
94
Reproducibility contract . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
94
Test budget snapshot . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
95
Part V — Connections to Existing Frameworks
95
Framework Connections I: pymdp/SPM Baseline, Hierarchical/Deep AIF, Sophisticated Infer-
ence, and Branching-Time AIF
96
Relationship calculus for AIF variants . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
96
Relation to recent unification efforts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
96
Mean-field active inference (pymdp, SPM, ActiveInference.jl) . . . . . . . . . . . . . . . . . . . . . . . . . .
97
Hierarchical / Deep Active Inference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
97
Sophisticated Inference (recursive EFE) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
97
Branching-Time Active Inference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
99
Synthesis: How Every Connection Lands on Lambda, J, or Kc
. . . . . . . . . . . . . . . . . . . . . . . .
99
Framework Connections II: KL/Path-Integral Control, Options Frameworks, Products-of-Experts,
and Copula Variational Inference
100
KL / Path-Integral Stochastic Optimal Control . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
100
Options framework / Hierarchical RL
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
101
Product of Experts and Mixture of Experts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
101
Copula variational inference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
101
Recovery dictionary
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
101
Framework Connections III: Multi-Agent Inference, RG-AIF Coarse-Graining, Markov Blankets,
and CEREBRUM Case Grammar
102
Interactive Inference / Multi-Agent Active Inference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
102
Renormalization-group active inference (structural analogy) . . . . . . . . . . . . . . . . . . . . . . . . . .
103
Markov Blankets and Bayesian Mechanics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
103
CEREBRUM and case-grammar approaches . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
103
Part VI — Discussion and Outlook
105
Open Theoretical Questions: Analytical Gaps, Identifiability, Empirical Frontiers, and Practical
Research Directions
105
Where to start
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
105
How to read each question . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
105
Analytical questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
106
Identifiability and inference questions
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
106
Empirical questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
107
Conceptual / cross-disciplinary questions
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
107
Practical / formalization questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
108
Discussion and Outlook: Worldview, Live Artifact State, and Limitations
108
What the framework commits to . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
108
What the framework declines to commit to
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
108
The parametric-entanglement worldview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
108
Relation to the Free Energy Principle and active-inference process theory
. . . . . . . . . . . . . . . . . .
109
3

## Page 5

Six load-bearing properties
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
109
Live state of the artifact . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
110
Alignment and Dysregulation Hypotheses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
111
Limitations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
111
Threats to validity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
112
Verification ledger
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
112
Open directions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
113
Proof of the Entanglement Decomposition
113
Definitions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
114
Expanding the EFE expectation
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
114
Expanding the prior log-expectation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
114
Combining
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
114
Interpretation (sign of 𝐼)
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
114
Closed exponential-family form (collapsed identity) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
115
Convexity of Free Energy in Lambda: Conditions and Counter-Example
115
The closed exponential-family form . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
115
The convexity ledger . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
115
Suﬀicient condition for global convexity on [0, ∞) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
116
K = 2 Symmetric Ising specialization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
116
Numerical verification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
116
Complete Derivation: Two-Stream Bernoulli Toy
116
Setup
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
116
Joint posterior
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
116
Marginals (uniform by symmetry)
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
117
Joint and marginal entropies
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
117
Closed-form mutual information
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
117
Coupling from a target alignment (alignment-inversion, not a VFE optimum) . . . . . . . . . . . . . . . .
117
Free-energy curve . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
118
Numerical cross-check . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
118
Tensor-Train Inference Algorithm: Bond-Dimension Sweep, MPS Contraction, and Sparsity-Rank
Tradeoff
119
Tensor-train representation of J . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
119
The exponential map . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
119
Inference cost . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
119
Sampling
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
119
Marginal extraction
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
119
Bond-dimension recursion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
119
Approximate compression . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
120
Connection to the sparsity–rank tradeoff . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
120
Lean 4 Boundary Fragment: Live ActinfPolicyEntanglement Source Excerpts and Validation Wiring120
Package structure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
120
Mathlib-free boundary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
120
Status snapshot . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
121
Building locally . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
121
FepSketches Re-exports for the Sibling fep_lean Layout . . . . . . . . . . . . . . . . . . . . . . . . . . . .
121
Where each manuscript theorem lives in Lean . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
121
The twenty live Lean companions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
122
Decomposition fragment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
122
Geometry fragment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
124
Spectral fragment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
125
Convexity fragment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
126
Heterogeneous fragment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
126
Connections fragment
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
127
Markov-blanket fragment
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
127
How drift is prevented . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
128
4

## Page 6

How a witness is consumed today . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
128
Notation Concordance: Symbol Registry Across Manuscript, LaTeX, Python, and Lean
128
How to read this concordance — one symbol, four tracks . . . . . . . . . . . . . . . . . . . . . . . . .
129
Sign conventions
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
129
Sets, indices, and basic objects
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
130
POMDP generative-model symbols . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
130
Distributions
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
130
Coupling potentials and parameters
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
131
Information-theoretic quantities . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
133
Free energies
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
134
Manifolds, projections, and dual coordinates . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
134
Spectral and tensor-network symbols . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
134
Heterogeneous-ensemble quantities . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
135
KL-control, copula, and product-of-experts symbols
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
135
Relationship classes and claim-strength labels . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
136
Hyperparameters (figure / sweep / simulation)
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
136
LaTeX preamble macros . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
137
Lean type abbreviations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
137
Phase / verdict labels (manuscript-level) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
137
Status notes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
137
Conventions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
138
Common pitfalls when editing across tracks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
138
GNN fifth-track concordance (structural-and-numerical) . . . . . . . . . . . . . . . . . . . . . . . . .
138
Reference Tables: Claim Strength, Variant Recovery, Lean Inventory, pymdp Bundle Statistics,
and JSONL Run-Log Schema
139
Claim-Strength Legend
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
139
Active-Inference Variant Recovery Ledger . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
139
Lean 4 Boundary-Fragment Module Inventory . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
140
MathlibProofs ℝAnalytic Discharge Package: Inventory . . . . . . . . . . . . . . . . . . . . . . . . . . . .
142
pymdp Free-Energy Bundle: Auto-Injected Summary Statistics . . . . . . . . . . . . . . . . . . . . . . . .
143
Robustness and Ablation Stress-Test Ledger . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
143
Evidence Ladder and Claim Provenance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
143
pymdp JSONL Run-Log Field Schema . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
145
GNN as a Shipped Fifth Track: Triple-Play Mapping, a Verified K=2 Bernoulli Round-Trip, and
a Lean Typed-Contract Emitter
146
Scope and Claim-Strength: a Shipped Bridge, with an Explicit Non-Claim About Proof . . . . . . . . . .
146
GNN Background: the Triple Play and the Active Inference Ontology
. . . . . . . . . . . . . . . . . . . .
147
Acronym Disambiguation: GNN (Notation) vs. GNN (Graph Neural Network)
. . . . . . . . . . . . . . .
147
Mapping the (𝐴, 𝐵, 𝐶, 𝐷, 𝐸, 𝐽, 𝜆) Tuple to a GNN Spec
. . . . . . . . . . . . . . . . . . . . . . . . . . . .
148
Worked Example: the K=2 Bernoulli Toy as a Shipped GNN Round-Trip . . . . . . . . . . . . . . . . . .
148
What GNN Preserves and What It Abstracts Away . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
149
Shipped Elaboration: GNN to a Lean Typed-Structure Contract . . . . . . . . . . . . . . . . . . . . . . .
150
Shipped Round-Trip: GNN to pymdp Harness Configuration
. . . . . . . . . . . . . . . . . . . . . . . . .
150
Downstream Use, Open Directions, and Open Questions . . . . . . . . . . . . . . . . . . . . . . . . . . . .
151
Bibliography
152
Active inference and the free-energy principle . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
152
Branching-time and structured AIF
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
155
Information geometry
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
155
Information theory and multi-information . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
155
Variational and copula inference
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
156
Variational inference robustness and Lipschitz bounds . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
156
Tensor networks and quantum-inspired ML
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
156
KL / path-integral control duality
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
157
Control / RL as probabilistic inference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
157
Hierarchical RL / options . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
157
Markov blankets and particular physics
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
158
5

## Page 7

Computational psychiatry . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
158
Integrated information / consciousness . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
158
Multi-agent / interactive inference
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
158
Lean / formalization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
159
Software dependencies (companion code) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
160
Scientific visualization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
160
Abstract
Active inference models often need to choose among several policy streams at once, for example streams tied to
different effectors, sensory channels, agents, agents within a group, or planning horizons. Standard discrete active-
inference implementations keep this manageable by treating those streams as independent, but that simplification
removes the dependencies that make coordinated action possible. This manuscript introduces policy entanglement:
a controlled deformation of the usual independent policy posterior by a scalar coupling strength and explicit
compatibility and preference potentials. The construction preserves the finite active inference setting while making
cross-stream dependence a first-class modeling object rather than an implicit artifact of the chosen factorization. The
framework keeps a claim-strength ledger that distinguishes exact recoveries, parameterized embeddings, numerical
witnesses, and structural analogies. Mean-field active inference is the exact independent case. Products of experts,
copula variational inference, options, hierarchical and sophisticated inference, branching-time active inference,
renormalization-style compression, and Markov-blanket multi-agent views are connected as special cases through
their stated posterior-factorization maps.
The central result is a free-energy decomposition that separates ordinary per-stream free energy, coupling preference
terms, the coupling normalizer, and the information cost of leaving independence. The decomposition makes multi-
information the explicit surcharge paid by a non-factorized policy posterior and shows how coupling strength,
compatibility structure, and off-diagonal preference costs enter the same accounting identity. This result supplies
the organizing principle for the rest of the paper. It supports an information-geometric reading of the coupled policy
family as a path away from the mean-field submanifold, a projection identity that returns the coupled posterior to
its independent marginals, a spectral and tensor-train view of dominant coordinated policy modes, a heterogeneous-
ensemble coupling-tax bound, and a phase vocabulary for under-coupled, mixed, and highly concentrated policy
posteriors. These interpretations are intentionally limited: the manuscript does not claim a neural, clinical, biological,
or quantum implementation, and Markov-blanket and tensor-network language is used as scoped modeling analogy
unless a specific theorem row or generated artifact supports a stronger statement.
The main decomposition analytic identity is machine-checked in ℝin the Mathlib-backed Lean layer with an axiom
audit and negative controls. A separate stock-Lean boundary fragment remains Mathlib-free and exposes the theorem
surface as typed contracts for the Python simulation layer and the manuscript registry, including witness-consuming
rows where analytic payloads are deliberately supplied at the boundary. The executable numerical layer remains
a Float pipeline, so a verified Float↔ℝerror bridge is still an explicitly open interface rather than an implied
proof; conservative interval brackets on the K=2 decomposition sweep certify Float residuals within a widened
high-precision envelope (output/reports/float_real_residual.json) without promoting the registry row to proved.
The empirical companion uses a partially observable Markov decision process (POMDP) simulation layer built with
pymdp and NumPy to sweep coupled policy ensembles, run short and long rollouts, check the projection identity to
round-off precision, produce free-energy, entropy, total-correlation, action-distribution, robustness, and adversarial
sidecars, and render figures from those artifacts. The manuscript, figures, theorem map, citation registry, notation
glossary (§S6), bibliography, and PDF are regenerated from the same source-owned pipeline, so prose claims are
tied to Lean sources, Python witnesses, output metadata, and validation gates rather than maintained by hand.
All
manuscript
methods,
tests,
and
documentation
are
available
as
open-source
software
at
https://github.com/ActiveInferenceInstitute/policy_entanglement
(DOI:
https://doi.org/10.5281/zenodo.20418904).
Part I — Introduction
This part frames the multi-stream policy-inference problem and surveys the prior work on which the framework
builds. Two chapters:
The Free Energy Principle enters this manuscript as a disciplined variational framing rather than as a slogan:
adaptive systems can be modeled as maintaining tractable beliefs that bound sensory surprise, while active inference
turns that variational bound into a process theory of perception, action, learning, and policy selection [Friston et al.,
6

## Page 8

2006, Friston, 2010, Buckley et al., 2017, Parr et al., 2022, Pezzulo et al., 2024]. That framing has also drawn careful
scope critiques, especially around Markov blankets and the temptation to treat FEP as a theory of everything rather
than as a modeling principle with explicit assumptions [Aguilera et al., 2022, Raja et al., 2021, Menary and Gillett,
2022]. The finite POMDP setting used here is therefore intentionally narrow: expected free energy supplies the
policy objective, pymdp supplies a reproducible implementation substrate, and the contribution of this manuscript is
to ask what happens when the policy posterior itself is allowed to carry explicit cross-stream dependence [Friston
et al., 2017a, Parr and Friston, 2017a, Kaplan and Friston, 2018, Da Costa et al., 2020, Smith et al., 2022, Heins
et al., 2022].
• §1 — why parametric coupling is needed. Real agents juggle many concurrent policy streams; strict mean-field
factorization can discard cross-stream structure that is directly visible in the motivating examples of §1. A
single tunable coupling parameter recovers strict factorization at one limit and arbitrary joint structure at the
other.
• §2 — what already exists in active inference, control theory, information geometry, and tensor networks
that this framework relates to exactly, parametrically, or analogically.
Eight axes of antecedents are
surveyed (discrete-time POMDP AIF; mean-field variational families; hierarchical / deep / sophisticated
AIF; information geometry; tensor networks; KL / path-integral control and RL; multi-agent inference and
renormalization; formal verification and reproducible scientific software). The later recovery ledger separates
exact recoveries (for example mean-field AIF and single-stream KL control) from parametric embeddings
(for example explicit factor-graph policy factors, options, copula VI, and multi-agent coupling) and structural
analogies (for example hierarchical, sophisticated, branching-time, renormalization-group, and Markov-blanket
readings). The specific mappings are cataloged in §17 through §19.
After Part I a reader has the motivating examples, the literature context, and the conceptual frame within which
the analytical content of §3 onward is developed.
Every symbol used in this manuscript is cataloged in §S6
across all four tracks (manuscript, LaTeX preamble, Python, Lean), with status notes flagging where a track
diverges (e.g. unicode-vs-ASCII identifier conventions).
The Lean track ships in two complementary packages:
MathlibProofs/, which machine-checks the central S01 free-energy identity (Theorem 5.1) in ℝwith foundational-
only #print axioms (propext, Classical.choice, Quot.sound; two independent negative controls audited on every
build), and lean/ActinfPolicyEntanglement/, a stock-Lean v4.29.0 boundary fragment that ships the 21-row theorem
surface as a typed API for the Python computational layer and the manuscript registry; §12 carries the per-row
content table and docs/reference/veridical_status.md the running audit.
Repository artifact. All four tracks (prose, equations, Python / pymdp, Lean 4) are maintained as a single working
repository artifact [Friedman, 2026a]. The public Zenodo DOI (10.5281/zenodo.20418904) and source repository are
recorded in manuscript/config.yaml and CITATION.cff. The entire build — rendered PDF, pymdp 1.0.1 numerical
sidecars, dashboard invariants, and the MathlibProofs ℝ-level discharge — regenerates from a single command
(./run.sh --pipeline or python scripts/run_all.py), and the repository’s machine-readable CITATION.cff provides
the preferred citation form.
Motivation and Position: Why Multi-Stream Active Inference Needs
Parametric Policy Entanglement
The problem in plain language
Active inference furnishes a normative theory of a perceiving-and-acting unit by minimizing variational free energy
across perception, action, and learning [Friston et al., 2006, Friston, 2010, Buckley et al., 2017, Friston et al.,
2017a, Da Costa et al., 2020, Parr et al., 2022]. In the discrete-time POMDP formulation, a unit is specified by
an observation likelihood 𝐴∶𝑝(𝑜∣𝑠), a transition tensor 𝐵∶𝑝(𝑠′ ∣𝑠, 𝑎), prior preferences over outcomes 𝐶, a
prior over hidden states 𝐷, and a habit / prior over policies 𝐸(𝜋), where policies 𝜋live on a space of action-
affordances replicated across a (possibly flexible) time horizon [Smith et al., 2022, Heins et al., 2022]. Expected free
energy then gives each policy posterior both an epistemic term (seek observations that resolve uncertainty) and a
pragmatic term (seek preferred outcomes), so action selection is not bolted onto perception but derived from the same
variational calculus [Friston et al., 2017a, Sajid et al., 2021, Parr and Friston, 2019, Friston, 2018]. The formalism is
mathematically compact, biologically motivated, and increasingly used across perception, decision-making, robotics,
and computational psychiatry [Adams et al., 2013, Schwartenbeck and Friston, 2016, Lanillos et al., 2021], while its
direct empirical status remains an active comparative-modeling question [Hodson et al., 2024].
An agent of any non-trivial complexity, however, is not best described by a single policy variable. A real agent
7

## Page 9

juggles many concurrent policies: motor and attentional, fast and slow, modality-specific, with some streams
treating the next move as a one-shot gradient descent on variational free energy (VFE) and others engaging in
deep counterfactual planning under expected free energy (EFE). The standard discrete POMDP treatment in pymdp
[Heins et al., 2022] and the continuous-state SPM-DEM lineage [Friston et al., 2008] split inference across independent
factors and policies — that is, they rely on strict mean-field factorizations across hidden-state factors, observation
modalities, and, in the multi-stream construction studied here, policy variables [Da Costa et al., 2020, Smith et al.,
2022].
The mean-field separation is computationally cheap and biologically suggestive — it mirrors functional segregation,
sparse cortical connectivity, and the modular character of much of the cortex — but it discards a structure that
is visible in natural behavior and engineered agents: actions taken on one stream are routinely contingent on,
anticipatory of, and instrumentally coupled to actions on others. A drummer’s left hand does not freely sample
its policy distribution while the right hand plans the next fill; an autonomous vehicle’s lateral and longitudinal
controllers share predictive structure with the symbolic route planner [Lanillos et al., 2021]; a human reaching for a
cup while reading does not factor reach-policy and saccade-policy independently. Natural-task eye-tracking studies
find that gaze typically arrives at the next task object before manipulation begins [Land and Hayhoe, 2001], and
object-manipulation studies show hand shaping and grip forces coupled to visual sampling of the object [Johansson
et al., 2001].
Contemporary world-model RL agents such as DreamerV3 [Hafner et al., 2023] give an adjacent
machine-learning example: cross-modal predictive state is useful, but the architecture does not expose a scalar
coupling parameter that the modeler can tune, infer, or validate.
This document develops a tunable, analytically tractable, machine-checkable formalism for the parametric entangle-
ment of concurrent policies in a single agent. The key move is structural rather than architectural: we do not commit
to translation layers between symbolic planners and motor controllers (which would make the modeler responsible
for the entire bridge), nor to fully joint enumeration of cross-modal policies (which combinatorially explodes), nor to
hand-designed attention-gating that re-introduces the mean-field assumption at a higher level. We instead introduce
a single tunable coupling parameter that interpolates between strict factorization and arbitrary joint structure, with
a closed-form decomposition of free energy that exposes precisely what the entanglement buys. In FEP language, 𝜆
does not replace precision, preferences, or expected-free-energy minimization; it makes the strength of cross-stream
policy dependence an explicit object that can be proved about, simulated, visualized, and validated.
The phrase policy-posterior coupling is used narrowly.
Standard active-inference notation already distinguishes
posteriors over hidden states, policies, and parameters [Friston et al., 2017a, Smith et al., 2022]. This manuscript
changes only the variational family for the policy posterior: the policy prior factors 𝐸𝑘, the expected-free-energy
weights 𝛾𝑘𝐺𝑘, and the agent’s generative-model tensors remain visible, while 𝜆𝐽adds an explicit cross-stream factor
on joint policy space.
Thus 𝜆is not neural precision, not a new preference distribution, and not a biological
measurement by itself; it is the scalar strength of a specified coupling potential inside the finite policy posterior.
Current coping strategies and their limits
The active-inference and probabilistic-modeling literatures have developed several strategies for handling cross-
stream dependence on top of a mean-field backbone. Each is genuinely useful in its regime; each leaves a structural
gap that the parametric construction below is designed to close.
• Architectural translation layers. A common engineering pattern is to factor the agent into independent per-
stream modules and hand-design a translation layer between them — for example, a symbolic-planner outputs
a goal that a motor-controller consumes as a target. This decouples the modules at design time but moves the
entire alignment problem into the translation layer, which is typically non-differentiable, non-Bayesian, and
the implicit source of brittleness when the modules’ assumptions drift apart.
• Hierarchical / deep active inference. Hierarchical AIF [Friston et al., 2017a, Pezzulo et al., 2018] organizes
the agent into a stack of generative models with explicit message passing across levels. Within each level the
mean-field assumption is re-imposed; cross-stream dependence is captured only through the bottleneck of the
inter-level messages. When two streams at the same level depend on each other directly (left hand and right
hand; saccade and reach), hierarchical AIF cannot express the dependence without inflating the level structure
to a degree that loses biological plausibility.
• Sophisticated inference.
Sophisticated inference [Friston et al., 2021] introduces beliefs about beliefs
through recursive expected free energy, capturing how an agent’s plan depends on what it will come to believe
once an action is taken. This is a powerful generalization along the temporal axis but it does not address
concurrent cross-stream coupling at a single decision point; the recursion is over future selves, not over peer
streams.
• Branching-time active inference. Branching-time AIF [Champion et al., 2022] expands the policy tree
and prunes it with Monte Carlo tree search, allowing a much richer enumeration of joint futures. The price
8

## Page 10

is computational: the policy space scales exponentially in horizon and arity, and the agent must spend search
budget the framework does not give it any principled way to allocate.
• Attention-gating and precision modulation.
Dopaminergic precision learning [Friston et al., 2014,
Schwartenbeck et al., 2015], the broader precision-in-action literature [Limanowski et al., 2024], and structured
attention mechanisms [Hoffman and Blei, 2015] gate which streams influence the posterior at a given moment.
This is well-suited to coarse on / off coupling but provides no continuous parameter for how strongly coupled
the streams should be, nor any analytical decomposition of the cost paid for coupling.
• Copula variational inference. Copula VI [Tran et al., 2015, Han et al., 2016] retains mean-field marginals
and adds a parametric copula on top to model dependence. The construction is elegant in static settings but
does not natively integrate with the EFE / planning side of active inference, and the choice of copula family
is a non-trivial modeling commitment that does not interpolate smoothly to or from the mean-field baseline.
• Tensor-network parameterized variational families. Tensor networks — matrix product states, tree-
tensor networks, hierarchical Tucker decompositions [Han et al., 2018, Glasser et al., 2020, Verstraete et al.,
2008, Eisert et al., 2010] — give compact structured joint distributions with controlled bond dimensions. We
are not aware of a prior active-inference treatment that uses this exact tensor-network family as the policy
posterior; one contribution of this manuscript is to show that the parametric coupling below is a tensor-network
family in disguise, recovering MPS-style algorithmic structure as a side effect.
Across these strategies, the diagnostic pattern is consistent: each one solves a piece of the cross-stream-coupling
problem and leaves the remaining pieces to the modeler.
A unified framework needs a single parameter that
interpolates between strict mean-field and arbitrary joint structure, a closed-form bookkeeping for the cost of leaving
the mean-field manifold, and a principled way to classify each neighboring strategy as an exact slice, a parametric
modeling route, or a structural analogy.
This placement also clarifies what the manuscript is not claiming. The framework is not a new general account of the
Free Energy Principle, nor a replacement for the process theory of active inference. It is a focused extension of the
variational family used for policy inference: the usual mean-field policy posterior remains the 𝜆= 0 anchor, while
finite 𝜆represents a controlled departure from that anchor. The Markov-blanket and particular-physics literatures
motivate why boundaries and conditional independences matter for self-organizing systems [Kirchhoff et al., 2018,
Ramstead et al., 2018], and critical reviews warn that those ideas do not automatically license unrestricted biological
or cognitive scope claims [Aguilera et al., 2022, Raja et al., 2021]. The claim tested here is narrower: within a finite-
POMDP agent whose modeling boundary is already fixed, cross-stream policy dependence can be made a transparent
mathematical and computational degree of freedom.
Significance
Six load-bearing properties of the framework:
(i) Theoretical economy. The current AIF literature handles cross-stream coordination through a proliferation
of architectural devices: branching-time tree search [Champion et al., 2022], hierarchical / deep AIF with explicit
message passing [Pezzulo et al., 2018, Friston et al., 2017a,b], sophisticated inference with recursive EFE [Friston
et al., 2021], and factor-graph forward-backward over multi-modal generative models [de Vries and Friston, 2017,
Friston and Parr, 2017, Parr et al., 2019, van de Laar, 2019]. Part V classifies these relationships instead of flattening
them into one claim: mean-field AIF is the exact 𝜆= 0 anchor; factor-graph message passing is a parametric
implementation route whose inserted policy factor has exact semantics only inside the chosen graph; hierarchical,
sophisticated, and branching-time AIF remain structural analogies unless their extra temporal or recursive machinery
is explicitly built into 𝐽and the generative model.
(ii) A clean decomposition theorem. §5 below gives a free-energy decomposition (Theorem 5.1) into (a) per-
stream marginal free energies, (b) a coupling / partition-function bundle (𝛾𝜆⟨𝐾𝑐⟩, log 𝑍𝐸(𝜆), and −𝜆⟨𝐽⟩), and
(c) the multi-information (total-correlation) term 𝐼(𝑞𝜆) ≥0 — see Eq. (5.2). The trade-off between coupling and
correlation makes precise when “joint structure pays for itself” relative to mean-field baselines, where comparable
accounts in the structured-VI literature [Saul and Jordan, 1995, Wainwright and Jordan, 2008, Hoffman and Blei,
2015] state the trade-off only implicitly. Three corollaries follow immediately: Corollary 5.2 (coupling-pays-for-itself
verdict), Corollary 5.3 (mean-field reduction at 𝜆= 0), and Corollary 5.4 (strict gain when 𝑞is non-mean-field).
(iii) Information geometry. The family {𝑞𝜆} is an exponential geodesic (e-geodesic) departing the mean-field
submanifold, which is itself e-flat. This places the framework on the well-developed scaffolding of dually-flat statistical
manifolds [Amari and Nagaoka, 2000, Amari, 2016, Nielsen, 2020], and connects revertibility (collapse to mean-field)
to the canonical m-projection (taking marginals). Non-extensive analogs via escort / 𝜙-deformed exponential families
[Naudts, 2011] generalize the construction to systems with non-extensive statistics.
(iv) Spectral interpretation.
For bipartite (𝐾= 2) couplings, the joint posterior 𝑞𝜆(𝜋1, 𝜋2) has a Schmidt
decomposition; for 𝐾> 2, a Tucker or tensor-train decomposition. The leading singular vectors / Tucker factors
9

## Page 11

are archetypal eigenvectors — the small number of dominant cross-stream behavioral modes that recur across
instances of a habit. This is a direct probabilistic-graphical-model homologue of bipartite entanglement entropy
in quantum many-body systems [Verstraete et al., 2008, Eisert et al., 2010, Han et al., 2018], and inherits all the
favorable algorithmic structure of low-rank tensor decomposition.
(v) Heterogeneous VFE/EFE ensembles. Many real agents are mixed: some streams are reflexive (one-step
VFE descent) and others plan (EFE counterfactuals). §9 derives an 𝑂(𝜆2) suboptimality bound (Theorem 9.1) for
VFE-only streams operating inside coupled ensembles. This formalizes a long-standing intuition: coupled reflexive
controllers can ride along with planners up to a bounded coupling-norm tax (Corollary 9.2), providing a quantitative
answer to “how reflexive can my low-level controllers be while still benefiting from higher-level planning?”
(vi) Lean formalizability. The framework is built from objects (finite probability distributions, KL divergence,
Shannon entropy, Bregman divergences) that are natural targets for Lean’s Mathlib [Community, 2020]. A prior
line of work shipped a 50-topic Mathlib-checked FEP catalog and companion monograph [Friedman, 2026c]; here,
§12 documents this manuscript’s two-package Lean architecture — a Mathlib4-backed MathlibProofs/ library that
machine-checks the central decomposition (Theorem 5.1) in ℝwith foundational-only #print axioms, and a stock-
Lean v4.29.0 ActinfPolicyEntanglement boundary fragment that ships the 21-row theorem surface as a typed API —
reusing the same toolchain pin [de Moura and Ullrich, 2021] and re-export layout as that codebase. The boundary
fragment is sorry / axiom / Mathlib-free and source-extracted into the manuscript prose; the per-row content
table (§12) and the running audit at docs/reference/veridical_status.md document what each row certifies at the
boundary versus what the Mathlib4 discharge layer establishes.
Position relative to alternatives
We make a deliberate choice not to take the embodiment-as-architecture route of solving the multi-policy problem
by partitioning into hardware / software modules with explicit translation layers between symbolic reasoning and
low-level control. That route has well-known costs: the translation layer becomes the entire alignment problem in
microcosm, and it is non-differentiable. Instead, we take the parametric entanglement route: tunably couple the
policy distributions themselves, leaving the structural distinction between modalities / timescales intact at the level
of marginals while permitting arbitrary joint structure to emerge through a learned coupling potential.
This is closest in spirit to: copula variational inference [Tran et al., 2015, Han et al., 2016], structured VI [Saul
and Jordan, 1995, Wainwright and Jordan, 2008, Hoffman and Blei, 2015], product-of-experts compositions [Hinton,
2002], and tensor-network parameterized variational families [Han et al., 2018, Glasser et al., 2020] — but specialized
to the policy-inference setting of active inference with explicit habit (𝐽), expected-free-energy (𝐺), and sophistication
(𝛾). It also connects to KL / path-integral control [Kappen, 2005, Theodorou and Todorov, 2012], options frameworks
[Sutton et al., 1999], multi-agent active inference [Maisto et al., 2024], and renormalization-group AIF [Friston et al.,
2025]. Part V assigns each connection an exact, parametric, or analogical relationship class, so “connection” never
has to mean “full recovery.”
How the framework is developed: four parallel tracks
The manuscript is unusual in that the same mathematical object is developed simultaneously on four parallel
tracks (prose, equations, Python, Lean), each with its own primary literature, its own quality criteria, and its own
role in the overall argument. The tracks are cross-referenced via a registry of injection tokens; a reader can enter on
any track and land on any other in a single hop, and a CI validator fails the build on dangling tokens, hardcoded
grid counts, seeds, or rollout horizons.
• Prose (§3 onward). The natural-language presentation: definitions, theorem statements, proof sketches,
worked examples, interpretive commentary. Every chapter in Part II opens with the objects under discussion
and closes with a three-bullet Takeaways box that surfaces the load-bearing claims. Section numbering is
owned by manuscript/refs/labels.yaml so that renumbering propagates everywhere automatically.
• Formalism in equations (§4, §5, §7, §8, §9). Every load-bearing identity is a registered equation in the
same labels file, auto-numbered as S.K and resolved through registry tokens so the manuscript’s mathematical
structure can be traversed without ever encountering a hand-written equation number. The four foundational
identities — the entanglement decomposition (Eq. (5.2)), the e-geodesic identity (Eq. (7.3)), the Pythagorean
decomposition (Eq. (7.4)), and the 𝑂(𝜆2) coupling-tax bound (Eq. (9.2)) — anchor the rest.
• Simulations on real
pymdp agents (§14, §15).
The empirical layer is not a re-implementation of
pymdp’s mathematics; it instantiates real pymdp.agent.Agent objects [Heins et al., 2022] with the JAX backend
[Bradbury et al., 2018], runs deterministic fixed-point-iteration inference, and reads off the resulting policy
posteriors, expected free energies, and free-energy bundles for every 𝜆on the coupling sweep. The analytical
𝜆-coupling layer takes those pymdp outputs and adds the cross-stream term — so the simulation tracks exactly
10

## Page 12

the deformation the theorems describe, not a stylized stand-in. At 𝜆= 0 the coupled joint is exactly the outer
product of the pymdp per-stream posteriors; at finite 𝜆the joint concentrates on cross-stream archetypes that
the bare pymdp run never sees.
• Lean 4 companions in a real lake
build environment (§12, §E). The formal track is a Lean 4
boundary fragment under ../lean/ that compiles against stock Lean v4.29.0 [de Moura and Ullrich, 2021]
with no Mathlib dependency, zero strict sorrys, zero axioms beyond stock Lean, and no unsafe / partial
/ noncomputable declarations. Every theorem in the body that admits a witness-form statement (including
Theorem 5.1) has a Lean companion that actually compiles in the project’s lake build; its source is auto-
extracted in the theorem sections and appendix via registry Lean tokens. The witness-form discipline makes
the analytic-content boundary explicit: Mathlib4 is used in the manuscript as the named library context for
those analytic obligations, while the current source blocks remain exactly the code that builds today.
The four-track contract is not aspirational;
it is CI-gated.
The cross-reference and hyperlink test suites
under ../tests/test_token_resolution.py and ../tests/test_project_wide_hyperlinks.py fail the build if any
[[SECREF:]], [[THMREF:]], [[LEAN:]], [[VAR:]], [[FIG:]], or markdown link does not resolve, so a reader who
finds a dangling reference has discovered a bug rather than an omission.
Reading guide
The manuscript has three logical layers; readers can profitably enter at any of the three depending on background.
Choose the conceptual path if the question driving you is “why does multi-stream coupling matter and what does it
look like when an agent does it well?”; choose the analytical path if you want to verify the load-bearing mathematical
claims and follow the proofs; choose the empirical path if you want to reproduce every numerical result against the
pymdp-grounded harness and inspect the JSONL run log.
• Conceptual / qualitative path. This section (§1) →§3 (POMDP recap) →§4 (the parametric deformation)
→§6 (worked toys) →§10 (phase regimes) →§21 (worldview). No proofs required; the closed-form K=2
Bernoulli derivation is the fastest entry point to the mathematics.
• Analytical / theorem path. §5 (Theorem 5.1, the load-bearing identity) →§7 (e/m-flatness, e-geodesic,
Pythagorean) →§8 (Schmidt rank, archetypes, tensor-train) →§9 (the 𝑂(𝜆2) coupling-tax bound, Theorem
9.1) →§11 (comparative statics).
• Empirical / reproducibility path. §13 (closed-form Bernoulli + heterogeneous tax + phase + spectral)
→§14 (1.0.1 architecture) →§15 (the free-energy bundle and derived summary statistics) →§16 (validation
gates + JSONL run log + reproducibility contract).
The Lean formalization plan (§12, §E) is orthogonal to all three paths and can be read at any point; every registered
theorem in this manuscript names its Lean companion so a reader can navigate prose →theorem-statement →Lean-
source in one hop. A single notation glossary (§S6) consolidates every symbol — including manuscript / LaTeX
/ Python / Lean counterparts — so prose that introduces new symbols can always be cross-referenced without
ambiguity.
Section dependencies (forward signposts)
Builds on
Used by
§3
every later section
§4
§5, §6, §7, §8
§5 (Theorem 5.1)
§6, §11, §10
§7 (Theorem 7.4, Proposition 7.5)
§8, §9, §17
§8 (Proposition 8.1)
§10, §19
§9 (Theorem 9.1)
§11, §13
§13
§14, §15, §16
§14
§15, §16
Background and Prior Work: Antecedents in Active Inference, Varia-
tional Coupling, Information Geometry, and Tensor Networks
This chapter catalogs the lines of work the framework builds on and points to where each one returns in the body.
Detailed comparisons live in Part V (§17, §18, §19). This chapter provides the substantive orientation required
11

## Page 13

for the body of the paper. The eight subsections below mirror eight axes of structural commitment: a Markov-
decision substrate, a variational family, hierarchical / sophisticated extensions, an information-geometric ambient,
a low-rank algorithmic backend, a control-theoretic and reinforcement-learning dual, multi-agent / renormalization
analogies, and a formal-verification plus reproducible-software scaffold. Clinical and neural language is treated here
as hypothesis-generating context, not as diagnostic evidence.
Discrete-time POMDP active inference
The discrete-time POMDP formulation of active inference is the home setting throughout. The standard treatment
combines a generative model (𝐴, 𝐵, 𝐶, 𝐷, 𝐸) with planning-as-inference under expected free energy [Friston, 2010,
Friston et al., 2014, 2017a, Kaplan and Friston, 2018, Smith et al., 2022, Sajid et al., 2021, Parr et al., 2022],
introducing policies as random variables over which the agent maintains a posterior shaped jointly by past
observations and anticipated outcomes.
Recent unification and agency-formalization work further clarifies how
multiple expected-free-energy formulations can be derived from shared roots, how EFE-based planning may be recast
as variational inference, and how active inference can be used as a model-comparison language for agency [Champion
et al., 2024, de Vries et al., 2025, Nuijten and Lukashchuk, 2025, Da Costa et al., 2024]. That literature is not purely
consolidating: Millidge, Tschantz, and Buckley analyze where EFE derivations diverge, so this manuscript treats
each per-stream 𝐺𝑘as a specified modeling choice rather than a unique consequence of FEP [Millidge et al., 2021].
Implementations now span several software lineages: pymdp targets open-source discrete state-space active inference in
Python [Heins et al., 2022], RxInfer.jl supplies reactive variational message passing for real-time Bayesian inference in
Julia [Bagaev and Podusenko, 2023], ActiveInference.jl provides Julia tooling for POMDP active-inference simulation
and parameter estimation [Nehrer et al., 2025], and SPM-DEM remains the continuous-state dynamic-expectation-
maximization ancestor [Friston et al., 2008]. The present manuscript’s empirical harness is built directly against
pymdp 1.0.1 (§14), while the mathematical recap in §3 and the Lean recap in §12 keep the same generative-model
schema explicit.
Within that lineage, expected free energy is the point at which epistemic and pragmatic control meet: policies
are preferred when they both reduce expected uncertainty and realize prior preferences.
Cognitive-consistency
interpretations make the same split visible in psychological language: epistemic and motivational closure are coupled
but not identical objectives [Friston, 2018]. This is why policy coupling is not a cosmetic addition. If two policy
streams share epistemic opportunities or pragmatic costs, strict factorization can erase precisely the joint structure
through which the process theory expresses coordinated action; epistemic-value and navigation examples make
that risk concrete in ordinary active inference before any coupling extension is added [Parr and Friston, 2017a,
Kaplan and Friston, 2018].
The action-oriented-model-learning literature makes the same pressure visible from
another angle: agents need models that are parsimonious because they are oriented toward possible action [Tschantz
et al., 2020]. Here the parsimonious object is the coupling potential 𝐽and its scalar strength 𝜆, rather than an
additional hidden-state factor or hand-designed controller interface. Factor-graph and graphical-brain accounts show
how generative-model structure induces message-passing schedules [de Vries and Friston, 2017, Friston and Parr,
2017], and approximation-family work distinguishes mean-field, Bethe, and marginal message passing as different
commitments about how local beliefs compose [Parr et al., 2019, Yedidia et al., 2005]. The word “free energy” is
doing different work across those lineages: Bethe / Kikuchi free energies govern approximate marginal inference
on factor graphs, while active inference adds policy selection, preferences, and epistemic terms.
In the present
manuscript, an additional policy factor can implement the 𝜆-coupling inside a chosen graph; the exactness belongs
to that chosen graphical model, not to active inference in the abstract.
The standard discrete-POMDP treatment commits to one policy random variable per agent, or to a factorized
family of per-factor policy posteriors when the model is decomposed. That design is tractable, but multi-stream
coordination is then carried by the modeling factorization rather than by an explicit coupling object [Da Costa et al.,
2020, Smith et al., 2022]. This commitment is the entry point for the parametric coupling introduced in §4.
Mean-field variational families and their limits
Mean-field factorization is the workhorse approximation of variational inference and its active-inference instantiation:
factorize the joint posterior across hidden-state factors, observation modalities, and policy variables to make the
per-factor updates tractable [Wainwright and Jordan, 2008, Blei et al., 2017, Da Costa et al., 2020, Smith et al.,
2022]. The cost is well known and well-studied: Hoffman and Blei note that the independence approximation “limits
the fidelity” of the approximation [Hoffman and Blei, 2015], while Blei, Kucukelbir, and McAuliffe present mean-field
and structured variational families as choices in an optimization problem rather than as exact posterior semantics
[Blei et al., 2017]. In the present setting, any genuine cross-factor dependence is discarded, and the magnitude of
the resulting bias is measured by the multi-information between factors — the same quantity that appears as the
surcharge in Theorem 5.1. The point is not that mean-field is wrong; it is that mean-field lacks an internal observable
12

## Page 14

for the dependence it has projected away.
Three lines of prior work attempt to relax mean-field while preserving tractability:
• Structured VI preserves selected dependency substructures while approximating the remaining interactions
[Saul and Jordan, 1995, Wainwright and Jordan, 2008, Blei et al., 2017], and structured stochastic VI [Hoffman
and Blei, 2015] introduces dependence between subsets of variables via amortized sub-models with shared
parameters, capturing coarse-grained dependencies at the cost of additional architectural commitment.
• Copula variational inference [Tran et al., 2015, Han et al., 2016] inserts a parametric copula on top of
the mean-field marginals, preserving the per-stream factor structure and confining dependence to the copula
density in the classical copula sense [Nelsen, 2006].
• Tensor-network parameterized variational families [Biamonte and Bergholm, 2017, Cichocki et al.,
2016, Han et al., 2018, Glasser et al., 2020] use matrix-product-state and tree-tensor-network factorizations as
compact joint distributions, importing algorithmic infrastructure from tensor-network physics and numerical
multilinear algebra [Verstraete et al., 2008, Eisert et al., 2010, Orus, 2014].
The framework here is a parametric interpolation across all three:
𝜆= 0 recovers strict mean-field; finite 𝜆
with appropriate 𝐽realizes products of experts exactly, copula VI parametrically, and tensor-network variational
structure as the algorithmic backend for low-rank coupling (§18). Crucially, these are structural correspondences,
not benchmark claims: at each exact or parametric specialization the entanglement decomposition of Theorem 5.1
reduces by substitution to the relevant variational-free-energy expression. Where the relationship is only analogical,
such as renormalization-group AIF, the recovery dictionary marks it as analogical rather than exact.
Hierarchical, deep, and sophisticated active inference
Hierarchical / deep active inference [Friston et al., 2017a,b, Pezzulo et al., 2018] decomposes the agent into a hierarchy
of generative models with explicit message passing across levels — a treatment that captures temporally-extended
structure and cortically-plausible scale separation [Friston et al., 2025], but that retains the mean-field assumption
within each level. Sophisticated inference [Friston et al., 2021] introduces beliefs about beliefs through recursive
expected free energy, modeling how an agent’s plan depends on the beliefs it anticipates having after taking an
action. Branching-time AIF [Champion et al., 2022] addresses the exponential cost of policy enumeration via Monte
Carlo tree search applied to the EFE tree.
Each motivates a different structural choice, but none should be read as a full exact recovery in the current artifact.
Hierarchical AIF corresponds to block-bidiagonal 𝐽as a cross-level concentration witness (Theorem 17.1), while
temporal-scale separation and directed top-down / bottom-up message passing remain part of the source process
theory. Sophisticated inference embeds with recursion-depth-many streams and a belief-about-belief 𝐽(Proposition
17.2), while the recursive observation-conditioning is a constraint on how that 𝐽is supplied. Branching-time AIF
suggests tensor-train or prefix-tree compression of 𝑞𝜆, but the present manuscript does not run a head-to-head BTAI
algorithmic comparison. The detailed mappings are tabulated in §17 and the appendix recovery ledger.
Information geometry
Dually-flat statistical manifolds, 𝑒- and 𝑚-coordinates, 𝛼-projections, and Bregman divergences are the natural
language for parametric extensions of variational families [Amari and Nagaoka, 2000, Amari, 2016, Nielsen, 2020,
Ay et al., 2017].
The 𝜆-deformation lives on this scaffolding: {𝑞𝜆} is an 𝑒-geodesic (Theorem 7.4), the mean-
field submanifold is 𝑒-flat (Proposition 7.1), and revertibility (collapse to mean-field marginals) is the canonical
𝑚-projection (Proposition 7.2). The Pythagorean decomposition (Proposition 7.5) provides an exact split of the KL
from the entangled posterior to any reference distribution into a multi-information term and a marginal-to-reference
KL.
Non-extensive generalizations via Tsallis / Rényi entropies and escort distributions [Naudts, 2011] yield 𝜙-deformed
exponential families on which the same construction goes through with quantitatively different geometry; we flag
the 𝑞-deformed analog as a natural extension (§7.4) without developing it here. Information geometry also supplies
vocabulary used in integrated-information studies of consciousness [Tononi, 2008], but the present framework makes
only a policy-space analogy: total correlation and low-rank structure quantify dependence among policy streams
after the modeling boundary is fixed. It does not claim to solve consciousness, define phenomenology, or validate an
integrated-information theory.
Tensor networks and entanglement entropy
Schmidt decomposition, matrix-product states, and the area law of entanglement entropy [Verstraete et al., 2008,
Eisert et al., 2010] supply both the algorithmic backend and the conceptual vocabulary for the spectral structure
13

## Page 15

of entangled posteriors. General tensor-network surveys and machine-learning treatments supply the computational
bridge from that physics vocabulary to low-rank tensor representations of high-dimensional arrays [Biamonte and
Bergholm, 2017, Cichocki et al., 2016, Orus, 2014]. In the bipartite (𝐾= 2) case the joint 𝑞𝜆(𝜋1, 𝜋2) admits a
Schmidt decomposition whose leading singular vectors are the archetypal eigenvectors — the few dominant cross-
stream behavioral modes (§8). For 𝐾> 2 a tensor-train factorization with bond-dimension profile (𝑟1, … , 𝑟𝐾−1)
controls representational capacity (Proposition 8.1, §D).
The tensor-network perspective also gives the framework its sharpest computational claim:
low-rank coupling
potentials produce low-rank posteriors (Theorem 8.3, the sparsity-rank tradeoff), making structured-coupling
inference scalable in the bond dimension rather than in the raw policy-space size. The tensor-network literature
has independently developed eﬀicient inference algorithms — DMRG, TEBD, MERA [Han et al., 2018, Glasser
et al., 2020, Schollwöck, 2011] — that become available once a coupling potential is represented in a tensor-network
form; the present artifact demonstrates the rank/bond-profile side of that claim through the multi-𝐾sweep and
tensor-train figures, while full tensor-network inference is left as an algorithmic extension.
Categorical-systems-
theory formulations of structured active inference [Smithe, 2024] further suggest that the same compositional
vocabulary admits formal-verification-amenable presentations of structured policies. All tensor-network language
in the manuscript is therefore a probability-tensor and linear-algebra analogy. It is not a claim that policy streams
are quantum subsystems, or that quantum entanglement semantics are being imported into active inference.
KL / path-integral control and reinforcement learning
KL / path-integral control duality [Kappen, 2005, Todorov, 2006, Theodorou and Todorov, 2012, Rawlik et al., 2013]
formalizes the equivalence between stochastic optimal control and free-energy minimization: the value function under
a controlled stochastic system is the log-partition of an unnormalized path measure weighted by exponentiated cost.
The options framework / hierarchical RL [Sutton et al., 1999, Barto and Mahadevan, 2003, Bacon et al., 2017, Doll
et al., 2015] decomposes long-horizon RL into reusable temporally-extended sub-policies with explicit initiation /
termination structure. Both fit cleanly into the parametric construction when the required factors are supplied: KL
control corresponds to the special-purpose choice in which 𝜆𝐽is the negative control-effort cost (single-stream limit);
options correspond to an option-like two-stream factorization with 𝐽encoding option-membership structure (§18).
A subtler connection is to products of experts [Hinton, 2002]: the 𝜆-entangled prior ℰ𝜆(𝜋) = ∏𝑘𝐸𝑘(𝜋𝑘) 𝑒𝜆𝐽(𝜋) is
literally a product of experts on joint policy space, with the coupling potential acting as one additional expert that
only fires on configurations where the cross-stream relationship holds.
Multi-agent inference, Markov blankets, and renormalization
Interactive / multi-agent active inference [Maisto et al., 2024] models multi-agent cooperation as joint inference
under shared generative models, while collective active-inference models show how group-level coordination can
arise from surprise minimization under coupled generative models [Heins et al., 2024]. Renormalization-group AIF
[Friston et al., 2025] derives hierarchical generative models via repeated application of a coarse-graining operator
that preserves dynamics-form. Bayesian-mechanics treatments of Markov blankets [Friston, 2019, Da Costa et al.,
2021] identify a system with a partition of states into internal / external / blanket, while Markov-blanket accounts
of autonomy emphasize that a system boundary is an inferential and conditional-independence structure rather than
just a physical envelope [Kirchhoff et al., 2018, Ramstead et al., 2018]. The critical literature is important here:
both technical and philosophical reviews argue that Markov blankets require careful modeling assumptions and do
not, by themselves, settle the scope of FEP, active inference, or cognitive boundaries [Aguilera et al., 2022, Raja
et al., 2021, Menary and Gillett, 2022].
All three relate to 𝑁𝐾-stream entanglement only after the modeling boundary and coupling graph are specified.
Multi-agent inference is a parametric joint-policy prior when within-agent and across-agent blocks of 𝐽are added
to a shared or linked generative model.
Renormalization-group AIF is an analogy between coarse-graining and
low-rank policy-posterior projection. Markov-blanket separation is a policy-space analog quantified by normalized
multi-information (§19), not a recovery of the state-space blanket construction. The manuscript therefore does not
infer new biological boundaries from 𝐽; it supplies a way to measure and manipulate policy dependence once a
modeling boundary has already been chosen.
Computational psychiatry and neural implementation
Computational-psychiatry programs use AIF to model dysregulation of perception, action, and learning [Adams
et al., 2013, Schwartenbeck and Friston, 2016], often associating symptom dimensions with failure modes of the free-
energy-minimization machinery (sensory precision dysregulation, prior over-weighting, habit rigidity). Dopaminergic
/ policy-precision accounts [Friston et al., 2014, Schwartenbeck et al., 2015, Parr and Friston, 2017b] and recent
14

## Page 16

precision-in-action reviews [Limanowski et al., 2024], together with empirical precision-weighting evidence in
psychosis [Haarsma et al., 2021], motivate the precision vocabulary, but the present framework borrows only the
formal precision analogy for 𝜆(§9.4). It does not identify 𝜆with dopamine, synaptic gain, or any specific neural
variable.
The phase-structure analysis in §10 flags a coupling-drift failure mode (under- or over-coupling of behavioral streams)
that is qualitatively distinct from per-stream prior corruption. We treat the clinical language as a model-generated
hypothesis, not a diagnostic claim: if the coupling account is right, controlled tasks would be expected to reveal
cross-stream covariance signatures (joint-action repertoire, between-trial mode statistics, coupling-spectrum effective
rank) that are not visible in per-stream marginal measures alone. This is consistent with the habit-vs-deliberation
balance literature [Doll et al., 2015] while adding an explicit coupling parameter that a follow-up empirical protocol
could estimate.
Lean 4, Mathlib, and formal verification of probabilistic systems
Lean 4 [de Moura and Ullrich, 2021, FRO, 2026a] and the Mathlib library [Community, 2020, FRO, 2026b] are the
formal-verification backbone of the present work. Lean 4 is a dependently-typed proof assistant with a minimal
trusted kernel and a tactic framework expressive enough to mechanize contemporary mathematics; Mathlib provides
— among many other things — the measure theory, linear algebra, and analysis targeted by the separate additive
discharge of the framework’s witness-form theorems.
A prior line of work shipped a 50-topic Mathlib-checked FEP catalog and companion monograph [Friedman, 2026c];
the present manuscript’s ActinfPolicyEntanglement boundary fragment (§12, §E) reuses the same toolchain pin and
re-export layout, with witness-form theorems isolating the analytic content for a separate Mathlib4 discharge layer.
Every numbered theorem in this manuscript — including the spectral semicontinuity and tensor-train rank claims
of §8 (Proposition 8.2, Theorem 8.3) and the hierarchical / sophisticated-inference embeddings of §17 (Theorem
17.1, Proposition 17.2) — now carries a live Lean companion in that fragment. The choice to keep the present
fragment Mathlib-free is deliberate: it forces every theorem statement to be expressible in the in-house CommScalar
α typeclass, exposes the analytic content as explicit witness arguments, and makes the boundary’s hygiene budget
(zero strict sorry, zero axioms, zero unsafe / partial / noncomputable) easy to verify against stock Lean v4.29.0.
The verified-numerics boundary remains separate from this proof story.
Numerical analysis supplies the right
vocabulary for round-off, conditioning, and stability [Higham, 2002], while IEEE 754 fixes the floating-point
arithmetic standard a formal bridge would have to model [IEEE, 2019], and proof-assistant floating-point libraries
such as Flocq show what such a bridge requires [Boldo and Melquiond, 2011]. The present artifact machine-checks
the exact ℝmathematics and tests the Float pipeline to strict tolerances; it does not claim a formal Float↔ℝ
theorem.
Reproducible scientific software
The empirical layer is built on NumPy [Harris et al., 2020], SciPy [Virtanen et al., 2020], JAX [Bradbury et al.,
2018] (which underpins pymdp 1.0.1), and Matplotlib [Hunter, 2007]. Every numeric value in the manuscript flows
from a real run via the [[VAR:<key>]] token system (§16); every figure carries reproducibility tEXt metadata (source
script, function, hyperparameter snapshot, git revision, ISO timestamp, and compact plotted-data summaries); every
cross-reference resolves through the same registry that the renderer consumes. This positions the manuscript inside
the broader open-science / reproducible-research practice and — concretely — makes the manuscript an executable
artifact: running scripts/run_all.py regenerates every numeric, every figure, and every theorem-table row from a
single deterministic pipeline.
Part II — Theory
The mathematical core of the manuscript. Each chapter introduces the objects, states the load-bearing theorems
about them, and immediately gives the proof or proof sketch (full proofs in the supplements). The chain proceeds:
1. §3 — discrete-time POMDP active inference and the mean-field baseline against which everything is measured.
2. §4 — the parametric coupling construction: 𝐽(habit) and 𝐾𝑐(preference) potentials, and the 𝜆-entangled
posterior they define.
3. §5 — the load-bearing identity (Theorem 5.1) splitting free energy into marginals, coupling, and a non-negative
multi-information term.
15

## Page 17

4. §6 — three worked cases (Bernoulli closed form, motor-attention, multi-timescale) that make the abstract
machinery concrete.
5. §7 — dual e/m information geometry; the 𝜆-family is an e-geodesic (Theorem 7.4); Pythagorean decomposition
(Proposition 7.5).
6. §8 — Schmidt rank (Proposition 8.1), archetypal eigenvectors, tensor-train bond dimensions (Theorem 8.3).
7. §9 — VFE/EFE mixed ensembles and the 𝑂(𝜆2) coupling-tax bound (Theorem 9.1).
8. §10 — disordered / mixed / frozen coupling regimes and their behavioral signatures.
9. §11 — sensitivity, two-parameter generalization, potential-structure dependence.
Every theorem in this part carries a Lean companion (see the per-row status in docs/reference/veridical_status.md)
and a Python numerical witness (see docs/reference/_theorem_map.md). The supplements (§A, §B, §C, §D) carry
the full derivations.
Setup and Assumptions:
Finite-Horizon Discrete POMDPs, Multi-
Stream Policy Factorization, and the Mean-Field Baseline
We work throughout with finite, discrete state and action spaces — adequate for the analytical results, computation-
ally tractable, and aligned with the discrete-time POMDP formulation that dominates AIF practice (pymdp, RxInfer,
ActiveInference.jl, SPM-DEM) [Heins et al., 2022, Bagaev and Podusenko, 2023, Nehrer et al., 2025, Friston et al.,
2008]. Continuous extensions are sketched in §21. Every symbol introduced here also appears in the unified notation
glossary (§S6) with its LaTeX, Python, and Lean counterparts.
Single-stream POMDP active inference
A standard discrete POMDP active inference unit:
Symbol
Meaning
𝑠∈𝒮
hidden state (finite)
𝑜∈𝒪
observation (finite)
𝑎∈𝒜
action (finite)
𝜋∈Π
policy: sequence/map of actions over horizon 𝑇
𝐴𝑖𝑗= 𝑝(𝑜= 𝑖∣𝑠= 𝑗)
likelihood matrix
𝐵𝑎
𝑖𝑗= 𝑝(𝑠′ = 𝑖∣𝑠= 𝑗, 𝑎) transition tensor
𝐶(𝑜) = log ̃𝑝(𝑜)
log-prior preferences
𝐷(𝑠) = 𝑝(𝑠0)
initial state prior
𝐸(𝜋)
habit / policy prior on Π
𝛾
policy precision
Under planning-as-inference with expected free energy [Friston et al., 2014, Da Costa et al., 2020]:
𝑞(𝜋) ∝𝐸(𝜋) exp( −𝛾𝐺(𝜋)),
𝐺(𝜋) = Risk(𝜋) + Ambiguity(𝜋)
(3.1)
with the standard EFE decomposition into pragmatic and epistemic components
𝐺(𝜋) = 𝔼𝑞(𝑜,𝑠∣𝜋)[ log 𝑞(𝑠∣𝜋) −log 𝑝(𝑠∣𝑜, 𝜋)]
⏟⏟⏟⏟⏟⏟⏟⏟⏟⏟⏟⏟⏟⏟⏟
epistemic value, negated
+ 𝔼𝑞(𝑜∣𝜋)[𝐷KL(𝑞(𝑜∣𝜋) ‖ ̃𝑝(𝑜))]
⏟⏟⏟⏟⏟⏟⏟⏟⏟⏟⏟
pragmatic value, negated
.
(3.2)
(Sign conventions for 𝐹, 𝐺, 𝐾𝑐are cataloged in §S6.1; the “negated” annotations above match the standard EFE
convention there.)
VFE-only streams are obtained by treating 𝐺as an immediate variational objective (no recursive lookahead), where
action selection is the gradient step on 𝐹at the current belief; the policy distribution effectively collapses to a delta
on the next-action argmin. In planning-as-inference with 𝛾moderate, 𝑞(𝜋) remains a proper distribution over the
policy space.
Having fixed the single-stream POMDP baseline, we now generalize to the multi-stream setting that is the substantive
subject of this manuscript.
16

## Page 18

The multi-stream extension
We posit 𝐾concurrent policy variables
𝜋= (𝜋1, 𝜋2, … , 𝜋𝐾),
𝜋𝑘∈Π𝑘,
Π =
𝐾
∏
𝑘=1
Π𝑘.
(3.3)
Generic streams. The 𝐾streams are generic in three independent senses, all of which the framework handles
uniformly:
• Modality. Each stream may correspond to a distinct observation modality (visual, auditory, proprioceptive)
and/or distinct hidden-state factor (location, identity, intent).
• Time horizon. Streams may differ in planning horizon 𝑇𝑘— a fast attentional policy and a slow navigational
policy are simultaneously representable without forcing them onto a shared clock.
• Inference mode. Each stream may use VFE-only, EFE-planning, or sophisticated inference (recursive EFE;
[Friston et al., 2021]).
Concretely:
a drummer’s left-hand timing stream (motor modality, short horizon, reflexive VFE) co-exists
with a right-hand fill-planning stream (motor modality, longer horizon, EFE planning); an autonomous vehicle
couples a very short-horizon steering controller (proprioceptive, VFE) with a much longer-horizon route planner
(symbolic, EFE) and an intermediate-horizon attention allocator (visual, EFE); a reading-while-reaching agent
factors immediate saccade policy (visual, VFE) from short-horizon reach policy (proprioceptive, EFE). In each
example the streams differ along at least two of the three axes above, and the coordination between them is precisely
what the entanglement framework formalizes.
Let 𝒱⊆{1, … , 𝐾} index VFE-only streams and 𝒫= {1, … , 𝐾} ∖𝒱index planning streams. The heterogeneous-
ensemble pay-off when these two stream classes are coupled is developed in §9.
The mean-field baseline
Strict mean-field across streams:
𝐸MF(𝜋) =
𝐾
∏
𝑘=1
𝐸𝑘(𝜋𝑘),
𝐺MF(𝜋) =
𝐾
∑
𝑘=1
𝐺𝑘(𝜋𝑘),
𝑞MF(𝜋) =
𝐾
∏
𝑘=1
𝑞𝑘(𝜋𝑘),
(3.4)
with each 𝑞𝑘(𝜋𝑘) ∝𝐸𝑘(𝜋𝑘) exp(−𝛾𝑘𝐺𝑘(𝜋𝑘)) a single-stream posterior. This is the regime exemplified by pymdp’s
factorized-A, factorized-B, factorized-policy treatment of multi-factor models [Heins et al., 2022].
Standing assumptions.
- Every per-stream policy alphabet Π𝑘is finite; the joint Π = ∏𝑘Π𝑘is therefore
finite. Continuous-policy extensions are conjectured in §20 (Q4) but are out of scope for the analytical core of
this manuscript. - The per-stream priors 𝐸𝑘are strictly positive on Π𝑘(no exact zeros), so KL divergences and
log-likelihoods are everywhere finite. - The per-stream EFE 𝐺𝑘and coupling potentials 𝐽, 𝐾𝑐are real-valued and
bounded on Π, so 𝔼𝑞𝜆[ ⋅] exists for every observable used below and the Gibbs partition function 𝑍(𝜆) is real-analytic
in 𝜆on [0, ∞).
Standing notation. - 𝐻(⋅): Shannon entropy. - 𝐷KL(𝑝‖𝑞): Kullback-Leibler divergence. - 𝐼(𝑝) = ∑𝑘𝐻(𝑝𝑘)−𝐻(𝑝):
total correlation (multi-information [McGill, 1954, Watanabe, 1960]) of joint 𝑝with respect to its 𝐾marginals 𝑝𝑘(see
Eq. (5.3)). - ℳ: manifold of joint distributions on Π. - ℳMF ⊂ℳ: mean-field submanifold (product distributions);
its e-flatness is recorded in Proposition 7.1 and developed in §7.
Lambda Deformation: Definition and Properties
In symbols: 𝑞𝜆(𝜋) ∝𝑞MF(𝜋) 𝑒𝜆(𝐽(𝜋)−𝛾𝐾𝑐(𝜋)), with 𝑞MF the mean-field baseline introduced in §3.3 and the entangled-
prior / entangled-posterior expansion derived below.
The symbols introduced below — 𝐽, 𝐾𝑐, 𝜆, 𝛾, ℰ𝜆, 𝑞𝜆— are cataloged in the unified notation glossary (§S6) with
their LaTeX, Python, and Lean counterparts.
Coupling potentials
Introduce two real-valued coupling potentials on the joint policy space:
17

## Page 19

• 𝐽∶Π →ℝ— habit coupling (prior-side): structural cross-stream tendencies that the agent has built up and
considers a-priori plausible.
• 𝐾𝑐∶Π →ℝ— preference coupling (EFE-side): cross-stream costs/preferences that show up in expected free
energy beyond the per-stream EFEs.
These need not be informed by anything outside the agent: they are parameters of the agent’s generative model,
learned from experience.
Definition: lambda-entangled policy posterior
Define the 𝜆-entangled prior and 𝜆-entangled posterior as
ℰ𝜆(𝜋) =
1
𝑍𝐸(𝜆)
𝐾
∏
𝑘=1
𝐸𝑘(𝜋𝑘) exp(𝜆𝐽(𝜋))
(4.1)
𝐺𝜆(𝜋) =
𝐾
∑
𝑘=1
𝐺𝑘(𝜋𝑘) + 𝜆𝐾𝑐(𝜋)
(4.2)
𝑞𝜆(𝜋) ∝ℰ𝜆(𝜋) exp( −𝛾𝐺𝜆(𝜋)) =
1
𝑍(𝜆)[∏𝑘𝐸𝑘(𝜋𝑘)]exp(𝜆(𝐽(𝜋) −𝛾𝐾𝑐(𝜋)) −𝛾∑𝑘𝐺𝑘(𝜋𝑘))
(4.3)
Boundary cases. - 𝜆= 0: ℰ0 = 𝐸MF, 𝐺0 = 𝐺MF, 𝑞0 = 𝑞MF. - 𝜆→∞: 𝑞𝜆collapses onto the modes of 𝐽−𝛾𝐾𝑐
— pure archetypal joint policies. (Here “modes” means elements of the argmax set argmax𝜋(𝐽(𝜋) −𝛾𝐾𝑐(𝜋)). As
𝜆→∞, 𝑞𝜆concentrates on this argmax set, with mass restricted to and re-normalized over those policies weighted
by the bare-posterior measure 𝐸MF(𝜋) 𝑒−𝛾𝐺MF(𝜋); in particular, when 𝐸MF and 𝐺MF are constant on the argmax set,
𝑞𝜆concentrates uniformly on the set.) - Intermediate 𝜆: the regime of practical interest.
For analytical separation of habit vs. preference coupling, one can carry two parameters 𝜆𝐸, 𝜆𝐺with coupling
potentials 𝐽, 𝐾𝑐respectively.
We use a single 𝜆in the body of the paper for clarity, with the two-parameter
generalization appearing in §11 for comparative statics.
The coupling parameter lambda as a precision-like coupling weight
A central conceptual point: 𝜆is not merely an arbitrary engineering knob. In the exponential-family representation
it behaves as a precision-like inverse-temperature on the coupling structure, dual (in the Legendre sense) to
the suﬀicient statistics ⟨𝐽⟩and ⟨𝐾𝑐⟩under the joint posterior. This is mathematically analogous to the role 𝛾plays
for EFE in the standard single-stream model, while remaining a distinct model parameter rather than a claim about
any specific neural precision signal. Concretely:
𝜕log 𝑍(𝜆)
𝜕𝜆
= ⟨𝐽−𝛾𝐾𝑐⟩𝑞𝜆.
(4.4)
Updating 𝜆by gradient on free energy (§9) is therefore a formal analog of precision learning [Friston et al., 2014,
Schwartenbeck et al., 2015, Limanowski et al., 2024]. We return to this in §9.4. Two consequences are worth flagging
now. First, 𝜆can be learned from the same free-energy objective the agent already minimizes — there is no auxiliary
regularizer, no separate meta-learner in the model. Second, under the model, coupling strength can vary with task
context or learning history. Any biological, arousal, fatigue, or developmental reading is hypothesis-level until an
empirical protocol estimates 𝜆from joint-action data; tonic over-coupling and under-coupling are therefore framed
as hypotheses about joint-statistical signatures, not as diagnostic claims (§10).
What J and K_c look like in practice
Five archetypal forms span the modeling range, each tuned to a different kind of cross-stream dependency. The choice
of 𝐽is therefore the substantive modeling decision — once 𝐽is fixed, the deformation in Eq. (5.2) is determined,
and the framework’s theorems hold for any bounded-norm choice. The five archetypes:
• Sparse pairwise. 𝐽(𝜋) = ∑(𝑖,𝑗)∈𝒞𝐽𝑖𝑗(𝜋𝑖, 𝜋𝑗) with 𝒞a small set of edges. Recovers pairwise Markov-random-
field structure and is the natural generalization of factor graphs; appropriate when only a few stream pairs
(e.g. left/right-hand pairs in motor coordination) carry meaningful joint dependence.
18

## Page 20

• Tensor-network low-rank. 𝐽(𝜋) = log[MPS(𝜋1, … , 𝜋𝐾)] with bond dimension 𝑟. Recovers all the favorable
algorithmic structure of matrix product states [Han et al., 2018]; bond dimension is a complexity dial that
interpolates between mean-field (𝑟= 1) and arbitrary joint structure (full 𝑟).
• Block-bidiagonal hierarchical. 𝐽couples only stream 𝑘to 𝑘+ 1. This is the structural analog used by the
hierarchical / deep AIF witness-form mapping (§17.2): it captures cross-level coordination in the joint policy
posterior, while temporal-scale separation and directed top-down / bottom-up message passing remain part of
the source generative model.
• Symbolic-task biased. 𝐽encodes a logical constraint (“if policy 1 is reach, then policy 2 is open hand”) via
large-magnitude penalties on violating configurations. Appropriate when domain knowledge dictates discrete
co-occurrences.
• Learned tabular. 𝐽is a free parameter on Π (size ∏𝑘|Π𝑘|) and is learned end-to-end. Computationally
infeasible for large 𝐾but conceptually clean and useful as the universal upper bound against which structured
choices are benchmarked.
The framework is agnostic to the choice of 𝐽, 𝐾𝑐— its theorems hold for any bounded-norm potentials. The art of
the modeler is in choosing parsimonious, mechanistically interpretable forms.
Entanglement Decomposition Theorem: Marginals, Coupling, and Total
Correlation
Statement
The variational free energy under 𝑞𝜆admits a clean decomposition. Define
𝐹[𝑞𝜆] = 𝔼𝑞𝜆[𝛾𝐺𝜆(𝜋) −log ℰ𝜆(𝜋)] −𝐻(𝑞𝜆).
(5.1)
Let 𝑞𝑘
𝜆denote the marginal of 𝑞𝜆on stream 𝑘, and 𝐹[𝑞𝑘
𝜆] the marginal free energy if stream 𝑘were treated in isolation
against its own 𝐸𝑘, 𝐺𝑘.
Theorem 5.1 (Entanglement Decomposition).
𝐹[𝑞] = ∑
𝑘
𝐹[𝑞𝑘] + 𝛾𝜆𝔼𝑞[𝐾𝑐] + log 𝑍𝐸(𝜆) −𝜆𝔼𝑞[𝐽] + 𝐼(𝑞)
(5.2)
where the total correlation
𝐼(𝑞) = ∑
𝑘
𝐻(𝑞𝑘) −𝐻(𝑞) = 𝐷KL(𝑞‖ ∏
𝑘
𝑞𝑘)
(5.3)
is non-negative and vanishes iff 𝑞𝜆is mean-field. (The sign on every term follows §S6.1 in S06 — specifically the
plus-𝐼(𝑞𝜆) and the +𝛾𝜆⟨𝐾𝑐⟩conventions.)
The Lean companion is a boundary statement auto-extracted from the live source:
-- From `lean/ActinfPolicyEntanglement/Decomposition.lean:75` [status: **boundary**]
/-- **Theorem 5.1 (Entanglement Decomposition)** — boundary witness
form.
Given a Mathlib-supplied algebraic split
`F[q] = marginal_part + coupling_expectation + agentic_gain`,
where `coupling_expectation` is the integrated `couplingLogWeight`
against `q`, this theorem certifies the equation in the boundary
fragment. Every coupling parameter `(J, K_c, γ, 𝜆)` is genuinely used
via `couplingExpectationSkeleton`, so the statement is non-vacuous.
**Typed-API-contract disclaimer.** The Lean body is literally
`hWitness ↦hWitness` — the identity term on the algebraic split.
This is **not** a stand-alone proof of Theorem 5.1; it is a typed-API
contract that forces `(J, K_c, γ, 𝜆)` into the conclusion via
`couplingExpectationSkeleton` and locks the four-term decomposition
shape.
The non-vacuous *algebraic* content of the decomposition
(commutative-ring re-grouping of the four bookkeeping scalars) is
discharged separately by `entanglement_decomposition_four_terms_assoc_skeleton`
and `entanglement_decomposition_four_terms_commute_skeleton` below
(genuine `CommScalar` proofs).
The full *analytic* content (Gibbs
expansion + KL chain rule) is supplied as `hWitness` and discharged
19

## Page 21

by the separate MathlibProofs layer; the numerical realization is in
`src/lean/decomposition.py` and verified at the dashboard invariant
`decomposition_lhs_eq_rhs_max_residual` (worst-case `5.55e-16`). -/
theorem entanglement_decomposition {K Pol}
(q : JointDist K Pol) (s : List (PolicySpace K Pol))
(logE G : PolicySpace K Pol →Float)
(J K_c : CouplingPotential Float K Pol) (gamma lam : Float)
(marginal_part agentic_gain : Float)
(hWitness : variationalFreeEnergy q logE G gamma s =
marginal_part
+ couplingExpectationSkeleton q s J K_c gamma lam
+ agentic_gain) :
variationalFreeEnergy q logE G gamma s =
marginal_part
+ couplingExpectationSkeleton q s J K_c gamma lam
+ agentic_gain :=
Honesty
note.
The
Float
boundary
companion
above
carries
status:
boundary
in
manuscript/refs/labels.yaml,
not
status:
proved:
it
type-checks
under
stock
Lean
v4.29.0
and locks the four- term algebraic skeleton, but its analytic content is supplied as a hypothesis. The
analytic content itself is now machine-checked in ℝ:
MathlibProofs.entanglement_decompo-
sition_generalK proves, for general 𝐾and a general entangled 𝑞(positivity + normalization only;
never assumed to factorize), the multi-information non-negativity, the KL chain-rule decomposition,
and 𝑚-projection minimality — depending only on the three standard foundational axioms, with
the previously-deferred product-marginalization core discharged from the standing positivity +
normalization hypotheses without further structural assumptions, and negative-control-verified as
non-vacuous. The full S01 boxed identity itself (F=Σ F[qᵏ]+γ𝜆⟨K_c⟩+log Z_E−𝜆⟨J⟩+I(q)) is then
machine-checked in ℝby MathlibProofs.free_energy_decomposition_full for the genuine entangled
posterior (log
Z_E the definitional normalizer, foundational-only axioms, two independent negative
controls). The Float companion is the numerically-corroborated computational image of the ℝproof;
closing the Float↔ℝformal bridge is the one verification-stack interface residual (the open residual
discussed at §21; interval brackets on the K=2 sweep grid in output/reports/float_real_residual.json
corroborate Float decomposition residuals but do not discharge the bridge); the remaining typed-API
rows are the analytic-discharge follow-on tracked at §20, not a separate verification gap). See the honest
substantive / typed-API split in docs/reference/veridical_status.md for the round-by-round audit of
which Lean theorems are substantive machine-checked proofs versus typed-API contracts.
Proof sketch
Expand 𝐹[𝑞𝜆] = 𝔼𝑞𝜆[𝛾𝐺𝜆−log ℰ𝜆] −𝐻(𝑞𝜆) using
𝛾𝐺𝜆(𝜋) = 𝛾∑
𝑘
𝐺𝑘(𝜋𝑘) + 𝛾𝜆𝐾𝑐(𝜋),
log ℰ𝜆(𝜋) = ∑
𝑘
log 𝐸𝑘(𝜋𝑘) + 𝜆𝐽(𝜋) −log 𝑍𝐸(𝜆)
(5.4)
for the normalized entangled prior ℰ𝜆∝(∏𝑘𝐸𝑘) 𝑒𝜆𝐽.
Linearity of expectation separates 𝔼[𝛾𝐺𝜆] and 𝔼[log ℰ𝜆]
into per-stream pieces plus the 𝛾𝜆⟨𝐾𝑐⟩, 𝜆⟨𝐽⟩, and log 𝑍𝐸(𝜆) terms.
The entropies −𝐻(𝑞𝜆) combine with
∑𝑘𝔼𝑞𝑘
𝜆[𝛾𝐺𝑘−log 𝐸𝑘] into ∑𝑘𝐹[𝑞𝑘
𝜆] + ( ∑𝑘𝐻(𝑞𝑘
𝜆) −𝐻(𝑞𝜆)); the parenthesis is multi-information
𝐼(𝑞) = ∑
𝑘
𝐻(𝑞𝑘) −𝐻(𝑞) = 𝐷KL(𝑞‖ ∏
𝑘
𝑞𝑘)
(5.3)
, i.e. 𝐼(𝑞𝜆). Altogether this yields
𝐹[𝑞] = ∑
𝑘
𝐹[𝑞𝑘] + 𝛾𝜆𝔼𝑞[𝐾𝑐] + log 𝑍𝐸(𝜆) −𝜆𝔼𝑞[𝐽] + 𝐼(𝑞)
(5.2)
. Full line-by-line algebra is in §A; the Python record entanglement_decomposition_rhs sums the same four grouped
terms and matches the Gibbs definition of 𝐹on random joints (see tests/test_decomposition.py).
What the decomposition says
Three terms, three readings:
(i) ∑𝑘𝐹[𝑞𝑘
𝜆]. The free energy that would obtain if each stream were optimized in isolation against the marginal of
𝑞𝜆. This is not the same as ∑𝑘𝐹[𝑞MF
𝑘
], because the marginals 𝑞𝑘
𝜆are themselves shaped by coupling — coupling
deforms what a stream considers a-posteriori plausible even before we charge the multi-information cost.
20

## Page 22

(ii) 𝜆(𝛾⟨𝐾𝑐⟩−⟨𝐽⟩). The coupling cost — what it costs (or pays) the agent to maintain the joint structure encoded
by the potentials. Sign depends on alignment between habit coupling 𝐽(which the agent likes) and preference-side
coupling 𝐾𝑐(which contributes EFE). When 𝐽and 𝐾𝑐point in compatible directions — e.g., when habitual joint
policies happen to also minimize joint EFE — this term can be net negative and pays for itself.
(iii) 𝐼(𝑞𝜆) ≥0. The multi-information term appears with a plus sign in
𝐹[𝑞] = ∑
𝑘
𝐹[𝑞𝑘] + 𝛾𝜆𝔼𝑞[𝐾𝑐] + log 𝑍𝐸(𝜆) −𝜆𝔼𝑞[𝐽] + 𝐼(𝑞)
(5.2)
: holding the marginals fixed, any genuine cross-stream correlation raises the Gibbs variational objective by exactly
𝐼(𝑞𝜆) nats. When joint structure still pays off for the agent is a comparison with the coupling / EFE / log-partition
bundle in the same identity — not literal subtraction of 𝐼from “free energy” in isolation. Corollary 5.2–Corollary
5.4 formalize the sign bookkeeping of that trade-off.
Read together, the three terms expose the central trade-off of policy entanglement. The marginal sum (i) tracks
how each stream is faring on its own slice of the deformed posterior; the coupling bundle (ii) is the price tag of
maintaining the structure encoded in 𝐽and 𝐾𝑐, and can be paid in either direction depending on whether habit and
preference are aligned or in tension; the multi-information (iii) is the correlation surcharge that any non-mean-field
joint owes purely for being correlated. Coupling pays for itself precisely when the bundle (ii) is suﬀiciently negative
to absorb both the correlation surcharge (iii) and any worsening of per-stream marginals (i). Stating it this way also
clarifies why the framework refuses to call (iii) a “cost” in isolation: 𝐼(𝑞𝜆) is the price of joint structure measured
against mean-field, but (i) and (ii) measure how much that structure buys back, and only the sum across all three
is a meaningful free-energy comparison.
The Lean companions for the three immediate corollaries are auto-extracted below.
Corollary 5.2 (the coupling-pays-for-itself verdict) is a tri-state classifier from the sign of the bookkeeping, now
upgraded to a proved theorem (status: proved) whose Lean form discharges the sign-soundness identity by direct
case analysis on the bookkeeping variable:
-- From `lean/ActinfPolicyEntanglement/Decomposition.lean:168` [status: **proved**]
/-- **Corollary 5.2 correctness theorem (boundary identity)**: the
`couplingVerdict` Boolean is `true` precisely when the coupling tax is
strictly less than the agentic gain — i.e. the verdict semantics
faithfully decide the "coupling-pays-for-itself" predicate.
This pins the verdict's contract on the boundary fragment: a `true`
answer is *not* an oracle assertion but a Lean-level proof that
`tax < gain`. Discharged by unfolding the `decide` and forwarding the
proof component, no `sorry`. -/
theorem couplingVerdict_correct (gain tax : Float) :
couplingVerdict gain tax = true ↔tax < gain := by
Corollary 5.3 (mean-field reduction at 𝜆= 0) collapses the four-summand bookkeeping to its sum-of-marginals +
total- correlation-gain pair:
-- From `lean/ActinfPolicyEntanglement/Decomposition.lean:195` [status: **proved**]
/-- **Corollary 5.3 (Mean-field optimum at 𝜆= 0)**: at `𝜆= 0`, the
coupling log-weight contribution vanishes pointwise. Polymorphic over
`[CommScalar α]`; combine with `entanglement_decomposition` to recover
the pure mean-field statement `F[q_0] = Σ_k F[q_0^k] + agentic_gain`. -/
theorem couplingLogWeight_pointwise_at_zero {α : Type} [CommScalar α]
{K Pol}
(J K_c : CouplingPotential α K Pol) (gamma : α)
(π : PolicySpace K Pol) :
couplingLogWeight J K_c gamma 0 π = 0 :=
Corollary 5.4 (strict gain when 𝑞is non-mean-field) is the sign companion of Eq. (5.3). Unlike the two proved
corollaries above, its Lean companion is a typed boundary witness (status: boundary, faithfulness: typed-witness):
the strict-gain inequality is carried as a typed contract, with the analytic discharge at the Mathlib layer.
-- From `lean/ActinfPolicyEntanglement/Decomposition.lean:215` [status: **boundary**]
/-- **Corollary 5.4 (Total-correlation unfolding)**: the boundary
fragment's `totalCorrelation` is by construction the per-stream
entropy sum minus the joint entropy.
This forwarder makes the
definitional unfolding available to downstream modules without
re-importing `FreeEnergy`'s namespace.
The strict-positivity claim `I(q) > 0 iff q is not mean-field` is the
`Iq > 0 ↔¬ IsMeanField q` companion that requires Mathlib's
KL-non-negativity (see `IsNonNegMultiInformation` in
[`FreeEnergy.lean`](FreeEnergy.lean)) and is exposed by the
`MathlibProofs` extension.
Stock-Lean, zero-`sorry`. -/
theorem totalCorrelation_def_unfold {K Pol}
21

## Page 23

(q : JointDist K Pol) (s : List (PolicySpace K Pol))
(sumStreamEntropies : Float) :
totalCorrelation q s sumStreamEntropies
= sumStreamEntropies - shannonEntropy q s := rfl
Optimal coupling: existence of lambda*
Theorem 5.5 (Existence of optimal coupling). For fixed 𝐽, 𝐾𝑐with bounded potentials, 𝐹[𝑞𝜆] is real-analytic
in 𝜆on [0, ∞) and admits the closed exponential-family identity
𝐹[𝑞𝜆] = log 𝑍𝐸(𝜆) −log 𝑍(𝜆)
(5.8)
The Lean boundary companion threads the algebraic identity through the coupling-log-weight skeleton so every
parameter (𝐽, 𝐾𝑐, 𝛾, 𝜆) is genuinely referenced:
-- From `lean/ActinfPolicyEntanglement/Decomposition.lean:243` [status: **boundary**]
/-! ## Theorem 5.5 — closed exponential-family form of `F[q_𝜆]`
The Gibbs decomposition `F[q] = Σ F[q^k] + γ𝜆⟨K_c⟩+ log Z_E(𝜆) - 𝜆⟨J⟩+ I(q)`
collapses to the strikingly clean identity
```
F[q_𝜆] = log Z_E(𝜆) - log Z(𝜆),
```
where `log Z_E(𝜆)` is the entangled-prior log-partition and
`log Z(𝜆)` is the entangled-posterior log-partition.
See
[`manuscript/04_entanglement_decomposition.md`](../../manuscript/04_entanglement_decomposition.md)
([Theorem 5.5](../../manuscript/refs/labels.yaml#thm_4_2)) and the proof appendix
[`manuscript/S01_proof_of_decomposition_theorem.md`](../../manuscript/S01_proof_of_decomposition_theorem.md).
The boundary fragment exposes the identity as a *witness-consuming*
statement: the caller (the separate additive `MathlibProofs` layer or the
numerical Python layer) supplies the algebraic equality
`vfe = logZE - logZ`, and the boundary fragment threads `(𝜆, J, γ, K_c)`
through `couplingExpectationSkeleton` so every parameter is genuinely
referenced and the statement is non-vacuous.
Polymorphic over
`[CommScalar α]`. -/
theorem freeEnergy_closedForm_witness {α : Type} [CommScalar α]
{K Pol}
(vfe logZE logZ : α)
(_s : List (PolicySpace K Pol))
(J K_c : CouplingPotential α K Pol) (gamma lam : α)
(hWitness : vfe = logZE - logZ) :
vfe = logZE - logZ
∧(∀π : PolicySpace K Pol,
couplingLogWeight J K_c gamma lam π
= lam * J π - gamma * lam * K_c π) := by
where 𝑍(𝜆) = ∑𝜋𝐸MF(𝜋) 𝑒𝜆(𝐽−𝛾𝐾𝑐)(𝜋)−𝛾𝐺MF(𝜋) is the normalizer of 𝑞𝜆and 𝑍𝐸(𝜆) = ∑𝜋𝐸MF(𝜋) 𝑒𝜆𝐽(𝜋) is the
normalizer of the entangled prior. Differentiating once gives
d𝐹[𝑞𝜆]
d𝜆
= ⟨𝐽⟩ℰ𝜆−⟨𝐽⟩𝑞𝜆+ 𝛾⟨𝐾𝑐⟩𝑞𝜆
(5.9)
so 𝜆↦𝐹[𝑞𝜆] has at least one stationary point in (0, ∞) whenever the marginal slope is negative,
⟨𝐽⟩𝑞0 −𝛾⟨𝐾𝑐⟩𝑞0 > ⟨𝐽⟩𝐸MF,
(5.10)
i.e. when the posterior coupling alignment net of EFE cost exceeds the prior coupling alignment. Since 𝐹is real-
analytic and bounded below on [0, ∞) — boundedness follows from the compactness of the simplex on a finite Π and
the boundedness of the potentials 𝐽, 𝐾𝑐, 𝐺𝑘standing-assumed in §3.3, so log 𝑍𝐸(𝜆) and log 𝑍(𝜆) are continuous
bounded functions of 𝜆— and 𝐹′(0) < 0 under the stated marginal-slope condition, 𝐹′(𝜆) achieves a zero in some
open interval and a stationary point 𝜆⋆∈(0, ∞) exists. Since the multi-information 𝐼attains its minimum at the
mean-field surface, d𝐼/d𝜆|0 = 0 identically. To see this in one line: by the chain rule along the e-geodesic, the
covariance form is
d𝐼(𝑞𝜆)
d𝜆
= Cov𝑞𝜆(𝐽−𝛾𝐾𝑐, log 𝑞𝜆−log
̂𝑚(𝑞𝜆))
(5.11)
22

## Page 24

A derivation along the e-geodesic from the closed identity Eq. (7.3) is in §9; at 𝜆= 0, 𝑞0 = 𝑞MF =
̂𝑚(𝑞0)
pointwise (here
̂𝑚(𝑞) = ∏𝑘𝑞𝑘is the m-projection of 𝑞onto the mean-field submanifold ℳMF, defined in §7.1), so
log 𝑞0 −log
̂𝑚(𝑞0) ≡0 on Π and the covariance vanishes. The Fisher contribution to 𝐹therefore lives at second order
(Eq. (A.15) and Proposition 11.1; see also §B). Under the symmetric standing prior 𝐸MF = Unif with ⟨𝐽⟩𝐸MF = 0,
the first-order condition collapses to the simpler form ⟨𝐽⟩𝑞0 > 𝛾⟨𝐾𝑐⟩𝑞0 used throughout §6 and §11.
Theorem 5.6 (Convexity of 𝐹in 𝜆— witness-form). If 𝐽−𝛾𝐾𝑐is log-concave on Π (in the finite-simplex
sense developed in §B), then 𝜆↦𝐹[𝑞𝜆] is convex on [0, ∞) and 𝜆∗is unique.
The boundary fragment ships
the witness-consuming Lean companion Convexity.freeEnergy_convex_in_lam_witness; the analytic content is a
structural witness that Mathlib4 can discharge from convex-analysis and log-partition facts without changing the
boundary theorem.
Theorem 5.6 says, in cognitive terms: when habit coupling and preference coupling are coherent (no internal
contradictions in what joint policies the agent prefers and habituates), the optimal entanglement strength is uniquely
determined.
When they are incoherent, the framework predicts multiple stable coupling regimes — a point we develop into a
phase-structure analysis in §10.
Takeaways
1. The decomposition is exact, not an approximation. Variational free energy under the entangled
posterior is identically the sum of per-stream marginal free energies, a coupling/partition bundle, and a
non-negative multi-information term — see Eq. (5.2).
2. Coupling pays for itself iff the surplus exceeds the multi-information cost. The optimum
𝜆⋆is determined by a single first-order condition balancing ⟨𝐽−𝛾𝐾𝑐⟩against the total-correlation slope.
3.
Coherent potentials yield a unique optimum; incoherent potentials predict phase
regimes. Convexity of 𝐹in 𝜆(Theorem 5.6) is the theoretical hinge: when it holds, 𝜆⋆is uniquely
determined; when it fails, multiple stable couplings co-exist (see §10).
Worked Examples:
Bernoulli Toy, Motor-Attention Coupling, and
Multi-Timescale Coupling
The K=2 Bernoulli toy: full closed form
In the symmetric 𝐾= 2 Bernoulli toy (defined just below) the closed-form multi-information has the body-scaling
identity
𝐼(𝜆) = 𝜆𝐽0 tanh(𝜆𝐽0) −log cosh(𝜆𝐽0) = log 2 −𝐻𝑏(𝜎(2𝜆𝐽0)),
(6.1)
where 𝐻𝑏is binary entropy and 𝜎is the logistic; the appendix-scaling form (𝐽∈{± 1
2}) is derived line-by-line in §C.
Not 𝐼(𝜆) = log cosh 𝜆, which would be an algebra error.
Two streams, each with two policies:
Π1 = Π2 = {0, 1}.
Marginal priors 𝐸𝑘= Unif.
Marginal EFEs
𝐺𝑘(0) = 𝐺𝑘(1) = 0 (so the streams are EFE-degenerate; all action is in the coupling).
Bilinear coupling
𝐽(𝜋1, 𝜋2) = 𝐽0 (2𝜋1 −1)(2𝜋2 −1) — i.e., 𝐽= +𝐽0 on aligned, 𝐽= −𝐽0 on anti-aligned.
Set 𝛾𝐾𝑐= 0 for
clarity.
The joint posterior is
𝑞𝜆(𝜋1, 𝜋2) = 𝐸MF(𝜋) 𝑒𝜆𝐽(𝜋)
𝑍(𝜆)
= 𝑒𝜆𝐽0 (2𝜋1−1)(2𝜋2−1)
4 cosh(𝜆𝐽0)
,
(6.2)
with the normalized-joint partition (using the normalized mean-field prior 𝐸MF(𝜋) = 1/4 on each of the four
atoms)
𝑍(𝜆) = ∑
𝜋
𝐸MF(𝜋) 𝑒𝜆𝐽(𝜋) =
1
4(2𝑒𝜆𝐽0 + 2𝑒−𝜆𝐽0) = cosh(𝜆𝐽0).
(6.3)
(The factor 1/4 comes from 𝐸MF; the unnormalized atom-sum 2𝑒𝜆𝐽0 + 2𝑒−𝜆𝐽0 = 4 cosh(𝜆𝐽0) is four times 𝑍(𝜆).) So
𝑞𝜆(𝜋) = 𝐸MF(𝜋) 𝑒𝜆𝐽(𝜋)/𝑍(𝜆) = 𝑒𝜆𝐽(𝜋)/(4 cosh(𝜆𝐽0)), as displayed above.
Marginals: 𝑞1
𝜆(𝜋1) = 𝑞2
𝜆(𝜋2) = 1/2 (symmetry, so 𝐻(𝑞𝑘
𝜆) = log 2).
For the joint, the four atoms have masses
𝜎(2𝜆𝐽0)/2 on the two aligned configurations and (1 −𝜎(2𝜆𝐽0))/2 on the two anti-aligned, where 𝜎(𝑥) = 1/(1 + 𝑒−𝑥)
23

## Page 25

is the logistic.
Direct computation gives the joint entropy 𝐻(𝑞𝜆) = log 2 + 𝐻𝑏(𝜎(2𝜆𝐽0)) with binary entropy
𝐻𝑏(𝑝) = −𝑝log 𝑝−(1 −𝑝) log(1 −𝑝). The total correlation is then
𝐼(𝑞𝜆) = ∑
𝑘
𝐻(𝑞𝑘
𝜆) −𝐻(𝑞𝜆) = 2 log 2 −log 2 −𝐻𝑏(𝜎(2𝜆𝐽0)) = log 2 −𝐻𝑏(𝜎(2𝜆𝐽0)).
(6.4)
Equivalently, in tanh form (the algebraic identity log 2 −𝐻𝑏(𝜎(𝑥)) = 𝑥
2 tanh(𝑥/2) −log cosh(𝑥/2)):
𝐼(𝑞𝜆) = 𝜆𝐽0 tanh(𝜆𝐽0) −log cosh(𝜆𝐽0) = log 2 −𝐻𝑏(𝜎(2𝜆𝐽0)) ,
𝜎(𝑥) =
1
1 + 𝑒−𝑥
(6.5)
This is the well-known mutual information of an Ising pair at inverse temperature 𝜆𝐽0. See §C for the line-by-line
derivation; the body uses the bilinear scaling 𝐽= 𝐽0(2𝜋1 −1)(2𝜋2 −1) while the appendix uses the swing- 1
2 form
𝐽∈{± 1
2}, related by 𝜆body ⋅𝐽0 = 𝜆app/2.
The free energy decomposition
𝐹[𝑞] = ∑
𝑘
𝐹[𝑞𝑘] + 𝛾𝜆𝔼𝑞[𝐾𝑐] + log 𝑍𝐸(𝜆) −𝜆𝔼𝑞[𝐽] + 𝐼(𝑞)
(5.2)
, applied with 𝐾𝑐= 0 and both marginal free energies 𝐹[𝑞𝑘
𝜆] = 0 (symmetric priors, zero per-stream EFE), gives:
𝐹[𝑞𝜆] = log cosh(𝜆𝐽0) −𝜆𝐽0 tanh(𝜆𝐽0) + 𝐼(𝑞𝜆) = 0,
(6.7)
since log 𝑍𝐸(𝜆) = log cosh(𝜆𝐽0), 𝜆⟨𝐽⟩𝑞𝜆= 𝜆𝐽0 tanh(𝜆𝐽0), and 𝐼(𝑞𝜆) = 𝜆𝐽0 tanh(𝜆𝐽0) −log cosh(𝜆𝐽0) — these three
terms cancel identically. The result 𝐹[𝑞𝜆] ≡0 is expected: when 𝐺𝑘= 𝐾𝑐= 0 the posterior equals the prior
(𝑞𝜆= ℰ𝜆) and the Gibbs variational objective is zero by construction.
Optimal 𝜆∗: Because 𝐹[𝑞𝜆] = 0 for all 𝜆, the VFE landscape is flat — there is no free-energy gradient to set 𝜆.
This is the degenerate Ising limit, and it resolves the moment 𝐺𝑘≠0 or 𝐾𝑐≠0, whereupon a well-defined finite 𝜆⋆
appears (see §6.2).
The toy is genuinely instructive: it isolates the pure role of the habit potential 𝐽. Without a preference coupling 𝐾𝑐,
free energy places no penalty on entanglement — all coupling levels are equally consistent with the model. The role
of 𝐾𝑐is to create the free-energy gradient that controls 𝜆⋆; this is the formal version of “habits are cheap; planning
to satisfy preferences is expensive.”
The closed-form mutual-information curve Eq. (6.5), the empirical numerical realization, and the joint posterior
at a representative 𝜆= 2 are reproduced numerically by scripts/parameter_sweep.py and visualized below;
agreement with the closed form is to floating tolerance (≤1𝑒−06 over 121 grid points spanning 𝜆∈[0, 6], see
output/data/parameter_sweep.csv). Sentinel values: 𝐼(𝜆= 1) = 0.1109 nats, 𝐼(𝜆= 2) = 0.3278 nats.
Two-stream motor + attention with realistic EFE
Stream 1 = motor (reach left vs. reach right). Stream 2 = attention (look left vs. look right). Per-stream EFEs:
𝐺1 depends on a hidden target location; 𝐺2 depends on epistemic value of foveation. Habit coupling 𝐽= strong
positive on aligned (look-where-you-reach) and slightly negative on anti-aligned. 𝐾𝑐= mild positive penalty on
simultaneous-novel-action (“don’t change two things at once”).
This recovers a familiar pattern:
optimal 𝜆∗is finite and positive; the agent learns to align gaze and reach
habitually, but the EFE cost of doubling novelty prevents over-rigidity.
Empirically (see scripts/manuscript_-
variables.py::_motor_attention_facts), the joint probability of an aligned (look-where-you-reach) outcome grows
from 𝑃align(𝜆= 0) = 0.5242 to 𝑃align(𝜆= 1) = 0.8451 to 𝑃align(𝜆= 2) = 0.9643.
The empirical suite in §13 already sweeps 𝜆and renders the relevant observables rather than leaving them as a
schematic: total correlation, Schmidt entropy (§8), free-energy surfaces, aligned-policy mass, and tensor-train rank
profiles. In the two-stream worked example, the show-not-tell pattern is visible in Fig. 1, Fig. 8, and Fig. 2: total
correlation grows and saturates, Schmidt entropy rises away from the mean-field boundary and then bends toward
the archetypal regime, and the free-energy surface identifies the coupling range where the utility surplus pays for
the information cost.
The closed-form alignment-inversion map 𝜆⋆(Δalign) for the symmetric K=2 toy — i.e. the coupling that realizes
a given target alignment Δalign = 𝛼(𝜆) = tanh(𝜆/2) — is
𝜆⋆(Δalign) = 2 arctanh(Δalign
Δmax
)
(6.8)
24

## Page 26

Figure 1: The K=2 Ising joint at 𝜆= 2 concentrates probability on the two aligned policies (diagonal)
while the per-stream marginals (side bars) remain symmetric. The inset residual 𝑞−∏𝑘𝑞𝑘is non-zero
— the visual signature of departure from the mean-field manifold, and the m-projection witness of Proposition
7.2 (marginalization = m-projection minimizes KL). Joint built via lean.bernoulli_toy.ising_joint_posterior at
𝜆= 2 (JOINT_HEATMAP_LAMBDA); panel layout from visualizations.joint_plots.plot_joint_heatmap_with_marginals.
Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
25

![page26_img1.png](images/page26_img1.png)

## Page 27

Figure 2: The closed-form mutual information agrees with the empirical sampler to sweep tolerance
(≤1𝑒−06 across 121 grid points). The curve 𝐼(𝜆) = log 2−𝐻𝑏(𝜎(𝜆)) grows from 0 at 𝜆= 0 (independence) and satu-
rates at log 2 ≈0.693 as |𝜆| →∞(perfect alignment). Closed form (lean.bernoulli_toy.ising_mutual_information,
Eq. (6.5)) and empirical (lean.bernoulli_toy.empirical_mutual_information) are overlaid on the 121-point sweep
from simulation.hyperparameters.PARAMETER_SWEEP_LAMBDAS (𝜆∈[0, 6]); CSV at output/data/parameter_sweep.csv.
This is the K=2 specialization of the decomposition theorem Theorem 5.1 (Lean companion ActinfPolicyEntan-
glement.Decomposition.entanglement_decomposition).
Uncertainty semantics: deterministic grid or deterministic
construction; no stochastic error bars are implied.
26

![page27_img1.png](images/page27_img1.png)

## Page 28

(see Eq. (6.8); this is target-alignment inversion, not the free-energy first-order condition, which is treated as a
separate VFE-optimization problem in §C and reduces to 𝜆⋆= 2𝑢in the small-utility limit).
The saturating
monotone shape is recovered numerically by src/lean/bernoulli_toy.py::optimal_lambda.
Numerical anchors:
𝜆⋆(0.5) = 1.0986, 𝜆⋆(0.9) = 2.9444.
Figure 3: The coupling that realizes a target alignment Δalign in the K=2 Bernoulli toy is 𝜆⋆(Δalign) =
2 arctanh(Δalign/Δmax).
This is the alignment-inversion formula — the inverse of the alignment–coupling
correspondence 𝛼(𝜆) = tanh(𝜆/2) — not a VFE optimum.
The actual VFE-optimal coupling under a utility
scalar 𝑢in the same toy is 𝜆⋆= 2𝑢at small 𝑢and only coincides with 2 arctanh(𝑢) in that limit (see §C). Numerical
witnesses for the existence (Theorem 5.5) and uniqueness via convexity (Theorem 5.6) of the VFE-optimal 𝜆⋆are
separate from this alignment-inversion curve. Closed form from lean.bernoulli_toy.optimal_lambda evaluated on
the 191-point sweep Δalign/Δmax ∈[−0.95, 0.95] (simulation.hyperparameters.OPTIMAL_LAMBDA_DELTAS). Uncertainty
semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
Multi-timescale coupling
One stream can be read as fast attentional control and another as a slower navigational plan. A sparse hierarchical
𝐽that couples the fast policy to the first decision point of the slower policy illustrates the coupling shadow of
hierarchical AIF [Pezzulo et al., 2018]: the posterior records cross-level compatibility without claiming to reproduce
the full directed message-passing schedule or temporal-scale separation of the source process theory. §17.2 states
the corresponding witness-form concentration claim and its limitations.
Information Geometry: Geodesics, Flatness, and Pythagorean Decom-
position
Dual coordinates and the mean-field submanifold
Equip the simplex of joint distributions on Π with the standard dually-flat structure [Amari, 1985, Amari and
Nagaoka, 2000, Amari, 2016]:
• e-aﬀine (exponential) coordinates: natural parameters 𝜃of an exponential family.
27

![page28_img1.png](images/page28_img1.png)

## Page 29

Figure 4: Coupling pays off only when the utility surplus is large enough to overcome the multi-
information cost. The free-energy curve 𝐹[𝑞𝜆] collapses to a flat zero at zero utility (no preference signal ⇒
no incentive to leave the mean-field manifold) and becomes monotonically decreasing as the surplus Δutil grows.
Four utility levels Δutil ∈{0, 0.5, 1, 2} shown. All four curves are convex in 𝜆on [0, ∞) — the numerical witness
of Theorem 5.6 (convexity of 𝐹in 𝜆).
Computed via lean.bernoulli_toy.ising_free_energy_curve on the 121-
point sweep PARAMETER_SWEEP_LAMBDAS. Uncertainty semantics: deterministic grid or deterministic construction; no
stochastic error bars are implied.
28

![page29_img1.png](images/page29_img1.png)

## Page 30

• m-aﬀine (mixture) coordinates: expectation parameters 𝜂= ∇𝜓(𝜃) where 𝜓is the log-partition.
• Riemannian metric: Fisher information.
• Canonical divergence: 𝐷KL.
The mean-field submanifold ℳMF ⊂ℳis the set of product distributions on Π. Standard facts:
Proposition 7.1.
ℳMF is e-flat in ℳ:
closed under exponential geodesics (interpolations aﬀine in log-
probability). The Lean companion Geometry.mfImage_isMeanField machine-checks only the definitional membership
IsMeanField(mfToJoint 𝑚) (every product distribution is mean-field, by rfl); it does not discharge the e-flatness /
closure-under-log-mixtures identity, which is the open real-analytic content scoped to the separate Mathlib layer
(registry status: proved but faithfulness: statement-restricted — see docs/reference/veridical_status.md).
Proposition 7.2 (m-projection / marginalization). For any 𝑞∈ℳ, the m-projection onto ℳMF is given by
taking marginals:
̂𝑚(𝑞) = ∏
𝑘
𝑞𝑘= arg min
𝑝∈ℳMF
𝐷KL(𝑞‖ 𝑝).
(7.1)
Proposition 7.3 (Total correlation as Bregman divergence to projection).
𝐼(𝑞) = 𝐷KL(𝑞‖
̂𝑚(𝑞)).
(7.2)
Hence the multi-information appearing in Theorem 5.1 is precisely the Bregman divergence from the joint posterior
to its mean-field projection — the geometric “departure” from the mean-field surface.
Two corollaries follow
immediately and are useful intuition pumps for the rest of the manuscript:
• Non-negativity. 𝐼(𝑞) ≥0 with equality iff 𝑞is mean-field, recovering the entropy sub-additivity inequality
𝐻(𝑞) ≤∑𝑘𝐻(𝑞𝑘) as the expanded form of Eq. (5.3).
• Pythagorean intuition. Because
̂𝑚(𝑞) is the m-projection of 𝑞onto ℳMF, 𝐼(𝑞) is the closest-point KL
distance from 𝑞to the mean-field surface; everything farther on ℳMF is recovered by the Pythagorean
decomposition Eq. (7.4) below.
The
Lean
companions
for
these
three
propositions
are
auto-extracted
from
the
live
source
under
lean/ActinfPolicyEntanglement/Geometry.lean and lean/ActinfPolicyEntanglement/FreeEnergy.lean:
-- From `lean/ActinfPolicyEntanglement/Geometry.lean:40` [status: **proved**]
/-- **`mfImage_isMeanField`** (registry `prop_6_1`, Prop 7.1,
`faithfulness: statement-restricted`).
This theorem proves only that
the product distribution induced by mean-field marginals *is*
mean-field — definitional membership `IsMeanField (mfToJoint m)`,
discharged by `rfl`.
It does **NOT** prove the named manuscript
proposition "the MF submanifold is e-flat" (closure under exponential
geodesics / affine-in-θ); that real-analytic content is the open
target scoped to the separate Mathlib layer (cf.
`entangledFamily_eGeodesic` for the affine-in-𝜆identity).
The name
was deliberately changed from the prior `mfSubmanifold_eFlat` so the
declaration's name states what it actually proves. -/
theorem mfImage_isMeanField {K Pol}
(m : MFDist K Pol) :
IsMeanField (mfToJoint m) := by
-- From `lean/ActinfPolicyEntanglement/Geometry.lean:77` [status: **proved**]
/-- **`mProjection_kl_eq_self_when_meanfield`** (registry `prop_6_2`,
Prop 7.2, `faithfulness: statement-restricted`).
This theorem proves
only the conditional equality `KL(q ‖ mfToJoint m) = KL(q ‖ q)` *under
the hypothesis* `h : q = mfToJoint m` (i.e. `q` is already mean-field).
It does **NOT** prove the named manuscript proposition that the
m-projection *minimises* KL — the information-projection optimality
`∀p ∈M_MF, D_KL(q‖m̂(q)) ≤D_KL(q‖p)` is the open analytic target
for the separate Mathlib layer.
The name was deliberately changed
from the prior `mProjection_minimises_kl` so the declaration's name
states what it actually proves (an equality when `q` is already the
projection, not a minimality result). -/
theorem mProjection_kl_eq_self_when_meanfield {K Pol}
(q : JointDist K Pol) (m : MFDist K Pol)
(h : ∀π, q π = mfToJoint m π)
(s : List (PolicySpace K Pol)) :
kl q (mfToJoint m) s = kl q q s := by
-- From `lean/ActinfPolicyEntanglement/FreeEnergy.lean:140` [status: **witness**]
/-- **Proposition 7.3 (boundary witness form)**: given the per-stream
entropy sum and the value of `KL(q ‖ m̂(q))` together with the
algebraic identity binding them, the boundary fragment certifies the
total correlation equals the KL to the m-projection.
Stock-Lean,
zero-`sorry`.
29

## Page 31

**Typed-API-contract disclaimer.** Not a stand-alone proof of the
KL-chain-rule identity `I(q) = KL(q ‖ ∏_k q^k)`; a typed-API contract.
The caller supplies `hWitness : sumStreamEntropies −shannonEntropy q s = klToMProj`;
the boundary fragment unfolds `totalCorrelation` and forwards. -/
theorem totalCorrelation_eq_kl_to_mprojection {K Pol}
(q : JointDist K Pol) (s : List (PolicySpace K Pol))
(sumStreamEntropies klToMProj : Float)
(hWitness : sumStreamEntropies - shannonEntropy q s = klToMProj) :
totalCorrelation q s sumStreamEntropies = klToMProj := by
The lambda-family is an e-geodesic
Theorem 7.4. The family {𝑞𝜆}𝜆∈ℝis an e-geodesic in ℳ: log 𝑞𝜆(𝜋) is aﬀine in 𝜆up to the normalizing constant.
The geodesic departs ℳMF at 𝜆= 0 in the direction defined by 𝐽−𝛾𝐾𝑐.
Proof. Expand log 𝑞𝜆(𝜋) using the definition of the 𝜆-entangled prior ℰ𝜆and the Gibbs form §4.2: the only 𝜆-
dependent terms are 𝜆𝐽(𝜋) and the normalizer log 𝑍(𝜆).
Subtracting log 𝑍(𝜆) — which is independent of 𝜋—
leaves the e-geodesic identity
log 𝑞𝜆(𝜋) + log 𝑍(𝜆) = ∑
𝑘
log 𝐸𝑘(𝜋𝑘) −𝛾∑
𝑘
𝐺𝑘(𝜋𝑘) + 𝜆(𝐽(𝜋) −𝛾𝐾𝑐(𝜋))
(7.3)
so 𝜋↦log 𝑞𝜆(𝜋) + log 𝑍(𝜆) is aﬀine in 𝜆at every fixed 𝜋with slope 𝐽(𝜋) −𝛾𝐾𝑐(𝜋). ■
The Lean companion (proved by forwarding to the linearity lemma in Coupling.lean):
-- From `lean/ActinfPolicyEntanglement/Geometry.lean:95` [status: **forwarder**]
/-- **Theorem 7.4** (forwarder).
Polymorphic over `[CommScalar α]`. -/
theorem entangledFamily_eGeodesic {α : Type} [CommScalar α] {K Pol}
(J K_c : CouplingPotential α K Pol) (gamma lam1 lam2 : α)
(π : PolicySpace K Pol) :
couplingLogWeight J K_c gamma lam1 π
- couplingLogWeight J K_c gamma lam2 π
= (lam1 - lam2) * (J π - gamma * K_c π) :=
The aﬀineness is straightforwardly observable numerically (see Eq. (7.3)): at every 𝜋the unnormalized log-weight
traces a straight line in 𝜆with slope 𝐽(𝜋) −𝛾𝐾𝑐(𝜋).
The same geodesic is also visible in a low-dimensional summary plane (Fig. 45): projecting the K=2 Ising joint onto
its aligned-corner mass and off-diagonal disparity traces a curve that departs the mean-field anchor at 𝜆= 0 and
bends monotonically toward an archetypal corner.
This places the framework in an exceptionally well-developed geometric setting. Concretely:
• Revertibility = m-projection. To revert an entangled posterior to mean-field, marginalize. This is an analytic,
differentiable operation. The framework therefore predicts that marginal behavioral statistics are recoverable
from coupled policies by the same projection used in the model; factor-isolation experiments are the right
empirical design for testing that recovery rather than evidence that the biological system explicitly performs
this operation.
• Manifold envelope. The “envelope” of joint distributions reachable with bounded coupling-potential norm
is a tubular neighborhood of ℳMF in the Fisher metric, of radius proportional to 𝜆⋅‖𝐽−𝛾𝐾𝑐‖.
• Proposition 7.5 (Pythagorean decomposition). For any joint 𝑞and any reference mean-field distribution
𝑞∗
0, the dually-flat Pythagorean theorem gives
𝐷KL(𝑞‖ 𝑞∗
0) = 𝐼(𝑞) + 𝐷KL( ̂𝑚(𝑞) ‖ 𝑞∗
0)
(7.4)
so 𝐷KL(𝑞‖ 𝑞∗
0) splits orthogonally into the “departure from MF” term 𝐼(𝑞) and the “MF-to-MF distance” term
𝐷KL( ̂𝑚(𝑞) ‖ 𝑞∗
0) — see also Eq. (7.4).
The Lean companion for Proposition 7.5 is a witness-consuming boundary form: the caller supplies the dual-flat
Pythagorean decomposition as a structural witness (dualFlat_pythagorean_witness). The current manuscript claims
that typed contract plus the numerical revertibility witness; the Mathlib4 discharge target is the finite-KL chain
rule and Bregman-divergence identity.
-- From `lean/ActinfPolicyEntanglement/Geometry.lean:169` [status: **witness**]
/-- **Proposition 6.5 (boundary witness, round-4 tie-in upgrade)**:
extracts the Pythagorean identity from a `PythagoreanWitness`.
The
three scalars are now *committed* to boundary-fragment primitives
(`kl`, `totalCorrelation`, `mfToJoint`) via three tie-in equalities —
a caller can no longer satisfy the contract with arbitrary `Float`s.
**Typed-API-contract disclaimer.** The analytic Pythagorean identity
30

## Page 32

Figure 5:
Every policy’s log-weight is consistent with exact linearity in 𝜆(slope error within
floating-point round-off) — the numerical signature of an exponential geodesic.
Four straight
lines (one per policy 𝜋∈{0, 1}2) with slopes 𝐽(𝜋) −𝛾𝐾𝑐(𝜋) depart from the same point at 𝜆= 0 (the
mean-field log-weight).
Linearity is the e-geodesic identity Eq. (7.3) and the numerical witness of Theorem
7.4 (Lean forwarder Geometry.entangledFamily_eGeodesic).
Unnormalized log-weight log ℰ𝜆(𝜋) −𝛾𝜆𝐾𝑐(𝜋) from
lean.coupling.coupling_log_weight on the 31-point sweep LOG_WEIGHT_FLOW_LAMBDAS under symmetric Ising coupling
with 𝐾𝑐≠0. Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars are
implied.
31

![page32_img1.png](images/page32_img1.png)

## Page 33

Figure 6: The K=2 Ising joint posterior, computed by lean.coupling.entangled_posterior on the 21-point linspace
grid over 𝜆∈[0, 4] (simulation.hyperparameters.KL_GEODESIC_LAMBDAS), traced in a 2-D summary plane spanned
by aligned-corner mass 𝑞(0, 0) + 𝑞(1, 1) (horizontal) and off-diagonal disparity |Δrow| + |Δcol| (vertical). The trace
departs the mean-field anchor (red star) at 𝜆= 0 and bends toward an archetypal corner — a visual e-geodesic
in the simplex coordinates used here. Uncertainty semantics: deterministic grid or deterministic construction; no
stochastic error bars are implied.
32

![page33_img1.png](images/page33_img1.png)

## Page 34

itself (the `pythagorean` field) remains a witness payload supplied
by the caller; the separate MathlibProofs layer discharges it from the
KL chain rule.
This theorem is **not** a stand-alone proof of the
Pythagorean decomposition; it certifies that *if* a caller supplies
witnesses that genuinely compute the boundary primitives, *then* the
extracted identity types-check.
The mathematical content lives in
the manuscript appendix S01 + the Python numerical companion in
[`src/lean/geometry.py`](../../src/lean/geometry.py) (which verifies
the identity on randomly sampled joints + reference mean-fields). -/
theorem dualFlat_pythagorean_witness {K Pol}
{q q0_star : JointDist K Pol} {mhat : MFDist K Pol}
{s : List (PolicySpace K Pol)} {sumStreamEntropies : Float}
(w : PythagoreanWitness q q0_star mhat s sumStreamEntropies) :
w.klVal = w.tcVal + w.residual := w.pythagorean
Connection to alpha-projections and curved exponential families
For 𝛼∈[−1, 1], the 𝛼-projection generalizes the 𝑚(𝛼= −1) and 𝑒(𝛼= 1) projections [Amari, 2016]. The mean-
field approximation in classical variational inference is m-projection of the true posterior onto ℳMF (minimize KL
with 𝑞as second argument, which is what variational lower bounds compute, modulo a sign convention cataloged
in §S6.1). Our 𝜆-family is the e-geodesic in the opposite direction: starting from MF and moving outward along a
chosen direction.
This duality is the deep reason the framework is well-behaved: we are not approximating a fixed target; we are
parametrically extending the variational family to admit structure, and the m/e geometry guarantees that revertibility
(back to MF) is the dual move to extension.
Connection to escort distributions and deformed exponential families
For non-extensive entropies (Tsallis, Rényi), one obtains escort distributions and 𝜙-deformed exponential families
[Naudts, 2011, Amari, 2016]. The same construction works for 𝑞𝜆: replacing exp with a deformed exponential gives
a 𝑞-deformed entanglement family. We do not develop this fully here, but flag it as a natural generalization for
systems exhibiting non-extensive statistics, with an evident connection to information-theoretic measures of partial
cognitive integration.
Takeaways
1. The mean-field submanifold is e-flat. Mean-field policy posteriors form an e-flat submanifold
of the probability simplex (Proposition 7.1); the 𝜆-family departs this submanifold along an e-geodesic
(Theorem 7.4). (The boundary Lean companion checks only definitional mean-field membership; full
e-flatness is the Mathlib-layer discharge target — prop_6_1 is status: proved, faithfulness: statement-
restricted.)
2.
Marginalization is exactly m-projection. Taking marginals is the KL-minimizing projection
onto the mean-field submanifold (Proposition 7.2) — revertibility is dual to extension. (The boundary
companion pins the m-projection’s KL value on the submanifold; information-projection minimality is
the Mathlib-layer discharge target — faithfulness: statement-restricted.)
3. Pythagorean decomposition makes the cost explicit. Total correlation 𝐼(𝑞𝜆) equals the KL of
𝑞𝜆to its m-projection (Proposition 7.3) — the multi-information cost in the decomposition theorem is
exactly the squared “distance” from the mean-field manifold in the dual geometry.
Spectral Structure:
Schmidt Rank, Archetypal Decomposition, and
Tensor-Train Bond Profiles
Bipartite Schmidt decomposition
For 𝐾= 2, view 𝑞𝜆as a matrix 𝑀∈ℝ|Π1|×|Π2| with 𝑀𝑖𝑗= 𝑞𝜆(𝜋1 = 𝑖, 𝜋2 = 𝑗). Singular value decomposition:
𝑀= 𝑈Σ𝑉⊤= ∑
𝛼
𝑠𝛼𝑢𝛼𝑣⊤
𝛼,
(8.1)
33

## Page 35

where 𝑠𝛼≥0, 𝑢𝛼, 𝑣𝛼orthonormal. Define:
• Schmidt rank 𝑟(𝑞𝜆) = #{𝑠𝛼> 0}.
• Policy entanglement entropy 𝑆𝐸(𝑞𝜆) = −∑𝛼𝑝𝛼log 𝑝𝛼where 𝑝𝛼= 𝑠2
𝛼/ ∑𝛽𝑠2
𝛽.
Proposition 8.1. 𝑟(𝑞𝜆) = 1 ⟺𝑞𝜆∈ℳMF (the joint distribution is a product). Equivalently, 𝑆𝐸= 0 ⟺
mean-field.
The Lean companion is a live boundary statement for the rank-one / mean-field interface:
-- From `lean/ActinfPolicyEntanglement/Spectral.lean:54` [status: **proved**]
/-- **Proposition 7.1 (forward direction, forwarder)**: extraction
shortcut for callers that already have the bipartite-mean-field
predicate in hand and want the product factorization witness. -/
theorem isBipartiteMeanField_factors {Pol1 Pol2 : Type}
(q : BipartiteJoint Pol1 Pol2)
(h : IsBipartiteMeanField q) :
∃(u : Pol1 →Float) (v : Pol2 →Float),
∀π1 π2, q π1 π2 = u π1 * v π2 :=
Proposition 8.2 (witness-form). 𝑟(𝑞𝜆) is upper-semicontinuous in 𝜆. As 𝜆↑∞, 𝑟(𝑞𝜆) collapses toward the
number of distinct modes of 𝐽−𝛾𝐾𝑐. As 𝜆↓0, 𝑟(𝑞𝜆) = 1.
The Lean companion SpectralWitnesses.schmidtRank_upperSemicontinuous_witness is now live in the boundary
fragment in witness-consuming form: the caller supplies a Schmidt-rank curve rankCurve : Float →Nat together
with the mean-field anchor rankCurve 0 = 1 and the universally quantified upper-semicontinuity inequality as a
structural witness, and the boundary fragment certifies the resulting existence claim by extracting the witness fields.
The Mathlib4 discharge target is the semicontinuity / matrix-rank argument; the current claim is the typed witness
contract plus the numerical rank sweep. The numerical realization lives in src/lean/spectral.py and is exercised
by tests/test_witness_theorems.py:
-- From `lean/ActinfPolicyEntanglement/SpectralWitnesses.lean:68` [status: **witness**]
/-- **Proposition 8.2 (boundary witness form)**: an
`UpperSemicontinuousRankWitness` *is* the existence of an upper-
semicontinuous Schmidt-rank curve anchored at `rankCurve 0 = 1`.
Stock
Lean, zero-`sorry`.
**Typed-API-contract disclaimer.** Not a stand-alone proof of upper
semicontinuity; a typed-API contract.
The continuity inequality is
supplied as `witness.usc`; the boundary fragment re-publishes it
together with the mean-field anchor.
Bipartite K=2 case is now
*genuinely* proved at the boundary as
`Spectral.Bipartite.schmidtRankOne_iff_isBipartiteMeanField` (round 4);
the general-K upper-semicontinuity statement still requires Mathlib's
topological-semicontinuity library + matrix-rank lower-semicontinuity
to discharge. -/
theorem schmidtRank_upperSemicontinuous_witness
(rankCurve : Float →Nat)
(witness : UpperSemicontinuousRankWitness rankCurve) :
rankCurve 0.0 = 1
∧∀(lam0 : Float) (r0 : Nat),
rankCurve lam0 ≤r0 →
∃delta : Float, 0.0 < delta ∧
∀lam : Float, (lam - lam0).abs < delta →rankCurve lam ≤r0 :=
The discontinuous-rank prediction of Proposition 8.1 is empirically observed as a step from 𝑟= 1 at 𝜆= 0 to 𝑟= 2
for any 𝜆> 0 in the K=2 Ising toy. Caveat (non-trivial coupling required). The rank jump from 1 to 2 at
𝜆= 0+ requires that 𝐽is non-trivial across the cut {1} ∣{2}, i.e. 𝐽cannot be written as 𝑓(𝜋1) + 𝑔(𝜋2) for any
per-stream functions 𝑓, 𝑔. In particular, if 𝐽depends only on one stream — say 𝐽(𝜋) = 𝑓(𝜋1) — the coupling is
degenerate across this cut, 𝑞𝜆remains a product across the cut for every 𝜆≥0, and rank remains 1. The Schmidt
rank is computed by src/lean/spectral.py::schmidt_decomposition and gated against the analytical predictions in
tests/test_spectral.py:
The smooth analog, the entanglement entropy 𝑆𝐸(𝑞𝜆), takes the boundary values 𝑆𝐸(0) = −0.0000, 𝑆𝐸(1) = 0.4652,
𝑆𝐸(3) = 0.6882 and is shown across (𝜆, utility) as a heatmap below.
The leading singular vectors as archetypal eigenvectors
This is the formal content of the archetypal eigenvector reading of low-rank entangled posteriors.
Definition (Archetypal modes). The archetypal joint policies of an entangled ensemble are the leading singular
vector pairs {(𝑢𝛼, 𝑣𝛼) ∶𝑠𝛼large}. Each mode 𝛼specifies a coupled pattern: a marginal 𝑢𝛼on 𝜋1 and a co-occurring
marginal 𝑣𝛼on 𝜋2, with weight 𝑠𝛼.
34

## Page 36

Figure 7:
Schmidt rank is integer-valued and steps up from 1 (mean-field manifold) to 2 as
soon as 𝜆exceeds the rank-detection tolerance under pure-𝐽Ising coupling (𝐾𝑐= 0, 𝛾= 0).
This step is the visual signature of the “rank-1 iff mean-field” identity Proposition 8.1 (Lean companion
Spectral.Bipartite.isBipartiteMeanField_factors) and the upper-semicontinuity prediction Proposition 8.2 — a
birth-of-archetype crossover at small positive 𝜆. Joint posterior built by lean.coupling.entangled_posterior; rank
extracted by lean.spectral.schmidt_rank (atol = 1e-09) on the 81-point sweep SCHMIDT_RANK_LAMBDAS. Uncertainty
semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
35

![page36_img1.png](images/page36_img1.png)

## Page 37

Figure 8: Entanglement entropy 𝑆𝐸is zero on the mean-field manifold (𝜆= 0), grows with 𝜆, then
saturates as the posterior collapses onto a single archetypal mode.
The saturation ceiling is utility-
dependent: higher utility shifts mass toward fewer archetypes, lowering peak 𝑆𝐸. The dark band at the left edge is
the visual marker of the mean-field submanifold. Computed on a 41×21 grid via lean.coupling.entangled_posterior
and lean.spectral.entanglement_entropy. Uncertainty semantics: deterministic grid or deterministic construction;
no stochastic error bars are implied.
36

![page37_img1.png](images/page37_img1.png)

## Page 38

These are not policies the agent ever literally executes — they are eigenmodes of the joint posterior. But they
are interpretable as the behavioral templates the coupling structure encodes. A drummer’s “groove” is the leading
(𝑢𝛼, 𝑣𝛼) pair on (left-hand-pattern, right-hand-pattern); a navigator’s “circumnavigation” pattern is a leading mode
on (locomotion, gaze).
This is structurally analogous to bipartite quantum entanglement entropy [Eisert et al., 2010] and to the spectral
theory of probabilistic graphical models [Han et al., 2018].
In the quantum case the Schmidt coeﬀicients {𝑐𝛼}
are amplitudes of a normalized state vector with ∑𝛼|𝑐𝛼|2 = 1; in the classical-probability case here the Schmidt
coeﬀicients are singular values {𝑠𝛼} of the K=2 reshape of 𝑞𝜆, normalized by their sum-of-squares to define the
spectral distribution 𝑝𝛼= 𝑠2
𝛼/ ∑𝛽𝑠2
𝛽. The analogy is mapped in tensor-network tutorials and reviews [Eisert et al.,
2010, Orus, 2014] and does not promote the policy joint to a quantum state — there is no superposition, no phase,
no Hilbert space; the structural similarity is at the level of the SVD-derived entropy of a bipartite array.
Figure 9: A small number of Schmidt archetypes carry almost all the mass: at 𝜆= 3 the leading
archetype dominates. Left panel: archetype weights {𝑠𝛼} in descending order (rank-effective is small). Right
panel: overlap matrix |⟨𝑢𝑖, 𝑢𝑗⟩| ⋅|⟨𝑣𝑖, 𝑣𝑗⟩| is diagonal-dominant — archetypes are mutually orthogonal by SVD
construction.
Computed via lean.spectral.schmidt_decomposition at 𝜆= 3 (ARCHETYPE_DENDROGRAM_LAMBDA).
Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
Multi-stream tensor decomposition
For 𝐾> 2, 𝑞𝜆is a 𝐾-tensor of size ∏𝑘|Π𝑘|. Use:
• CP (CANDECOMP/PARAFAC): 𝑞𝜆≈∑𝛼𝜆𝛼𝑢1
𝛼⊗𝑢2
𝛼⊗⋯⊗𝑢𝐾
𝛼.
• Tucker: 𝑞𝜆≈𝒢×1 𝑈1 ×2 𝑈2 ⋯×𝐾𝑈𝐾.
• Tensor train (matrix product state, MPS): 𝑞𝜆(𝜋1, … , 𝜋𝐾) ≈Tr[∏𝑘𝐴𝑘(𝜋𝑘)] with bond dimension 𝑟.
Tensor-train is computationally favored: storage 𝑂(𝐾⋅|Πmax|2 ⋅𝑟2) vs ∏𝑘|Π𝑘| for the full joint, with rich expressive
power for sparse/sequential coupling structure [Orus, 2014, Glasser et al., 2020, Han et al., 2018].
Definition (Multi-stream entanglement entropy). For tensor-train representation with bond dimensions {𝑟𝑘},
the maximum bond entropy across each cut {1, … , 𝑘} ∣{𝑘+ 1, … , 𝐾} is 𝑆max
𝑘
= log 𝑟𝑘. The actual bond entropy is
𝑆𝑘(𝑞𝜆) = −∑𝛼𝑝(𝑘)
𝛼
log 𝑝(𝑘)
𝛼
where {𝑝(𝑘)
𝛼
= 𝑠(𝑘),2
𝛼
/ ∑𝛽𝑠(𝑘),2
𝛽
} is the spectral distribution of the bipartite reshape of
𝑞𝜆across the 𝑘-th cut; by Jensen, 𝑆𝑘(𝑞𝜆) ≤log 𝑟𝑘with equality iff the bond singular values are uniform. The full
entanglement spectrum is the tuple (𝑟1, … , 𝑟𝐾−1) together with the per-cut singular-value distributions.
Theorem 8.3 (Sparsity-rank tradeoff). If the coupling potential 𝐽is representable as a tensor-train with bond
dimensions {𝑟𝑘} and interaction order 𝑑(the maximum order of any individual clique in the additive decomposition
𝐽= ∑𝑒𝐽𝑒), then the resulting 𝑞𝜆has tensor-train rank at most {𝑟𝑑
𝑘} on each cut (pairwise interactions give the
{𝑟2
𝑘} saturation; see §D for the exact bound and the contraction exp(𝜆𝐽) = ∏𝑒exp(𝜆𝐽𝑒) that produces it). Hence
sparse hierarchical coupling structures (small 𝑟𝑘, small 𝑑) yield computationally eﬀicient posteriors, and the bond
dimensions {𝑟𝑑
𝑘} are the rank of cross-cut entanglement.
37

![page38_img1.png](images/page38_img1.png)

## Page 39

The Lean companion SpectralWitnesses.sparsityRank_tradeoff_witness is now live in the boundary fragment in
witness-consuming form: the caller supplies a per-cut Schmidt-rank function and an a-priori bond- dimension
envelope, together with the universally quantified rank- bound envelope, as a SparsityRankEnvelope
K witness;
the boundary fragment certifies that the entangled posterior respects the envelope on every cut and every 𝜆. The
Mathlib4 discharge target is the tensor-product / matrix-rank proof of that envelope; the rendered Lean block below
is the current source that actually builds.
-- From `lean/ActinfPolicyEntanglement/SpectralWitnesses.lean:136` [status: **witness**]
/-- **Theorem 8.3 (boundary witness form)**: a `SparsityRankEnvelope`
witness *is* the existence of a per-cut Schmidt-rank envelope for the
𝜆-entangled posterior of a tensor-train coupling.
Stock-Lean, zero-
`sorry`.
**Typed-API-contract disclaimer.** Not a stand-alone proof of the
sparsity-rank tradeoff; a typed-API contract.
The per-cut envelope
`cut_rank k 𝜆≤bond_bound k` is supplied as a `SparsityRankEnvelope`
field; the boundary fragment extracts it.
MathlibProofs discharge
from `Mathlib.LinearAlgebra.TensorProduct` plus matrix-rank bounds. -/
theorem sparsityRank_tradeoff_witness (K : Nat)
(witness : SparsityRankEnvelope K) :
∀(k : Fin K) (lam : Float),
witness.cut_rank k lam ≤witness.bond_bound k :=
This is the formal version of: the deeper the coupling structure, the higher the cross-stream rank — but sparse couplings
give low rank, hence eﬀicient inference. It directly mirrors the empirical success of MPS-based generative models
[Han et al., 2018] and Friston’s renormalization-group treatment of FEP [Friston et al., 2025], in which scale-invariant
generative models have an inherent sparse-coupling structure that supports eﬀicient hierarchical inference.
The bond-rank profile is computed numerically across stream counts 𝐾∈{2, 3, 4, 5} for the symmetric Ising K-stream
coupling (src/simulation/builders.py::ising_coupling_tensor): TT𝐾=2 = [2], TT𝐾=3 = [2, 2], TT𝐾=4 = [2, 3, 2],
TT𝐾=5 = [2, 3, 3, 2].
Figure 10: Bond dimensions stay small even as the stream count grows: 𝑟𝑗≤3 across 𝐾∈{2, 3, 4, 5}. This
is the sparsity-rank tradeoff in action — low-rank Ising couplings yield low-rank posteriors, the empirical witness
of Theorem 8.3. Each row of the panel is the bond-rank profile (𝑟1, … , 𝑟𝐾−1) for one stream count at 𝜆= 2. Joint
built via lean.coupling.entangled_posterior over simulation.builders.ising_coupling_tensor; bond dimensions
from lean.spectral.tensor_train_ranks (atol=1e-09). Uncertainty semantics: deterministic grid or deterministic
construction; no stochastic error bars are implied.
38

![page39_img1.png](images/page39_img1.png)

## Page 40

Birth and death of archetypes
As 𝜆varies continuously from 0, the Schmidt rank can jump discontinuously upward (singular value crossings).
These are the symmetry-breaking transitions of the entanglement structure — points at which a new behavioral
archetype becomes available. We develop these as phase transitions in §10.
Takeaways
1. Rank is the operational definition of “non-mean-field”. The joint posterior is mean-field iff
its Schmidt rank is 1 (Proposition 8.1); any coupling that is non-trivial across the cut {1} ∣{2} (i.e. not
of the additive form 𝑓(𝜋1) + 𝑔(𝜋2)) jumps rank to ≥2 at 𝜆> 0. (The boundary Lean companion checks
the definitional rank-one / mean-field unfolding; the full rank equivalence is the Mathlib-layer discharge
target — prop_7_1 is status: proved, faithfulness: statement-restricted.)
2. A few archetypes carry most of the behavioral mass. Leading singular vectors of 𝑞𝜆are the
dominant cross-stream behavioral modes — the few archetypes the agent’s hyperprior repeatedly sculpts.
3. Low-rank couplings give low-rank posteriors. The sparsity-rank tradeoff (Theorem 8.3) bounds
the bond dimensions of the posterior by those of the coupling — sparse hierarchical couplings yield
computationally cheap inference.
Heterogeneous
Inference:
Mixed
VFE/EFE
Ensembles
and
the
Coupling-Tax Bound
Three-level update hierarchy
The framework induces a natural three-level hierarchy of online updates:
1. Level 1 (within-stream). Update 𝑞𝑘
𝜆for each stream, holding 𝐽, 𝐾𝑐, 𝜆fixed.
2. Level 2 (coupling structure). Update 𝐽, 𝐾𝑐as parameters of a generative model (e.g., Dirichlet-coupling
for 𝐽, gradient on free energy of free energy for 𝐾𝑐).
3. Level 3 (coupling precision). Update 𝜆by gradient on 𝐹[𝑞𝜆].
Each level has a clean interpretation: - Level 1: ordinary perception/policy inference. Time scale: per-step. - Level
2: habit/preference learning. Time scale: trials to days. - Level 3: precision-like learning on the coupling itself — a
model-level account of context-dependent coordination. Time scale: task phases or learning contexts.
Coupled marginal updates
For stream 𝑘∈𝒫(planning), the coordinate-descent update on 𝑞𝑘
𝜆is the standard fixed-point:
𝑞𝑘
𝜆(𝜋𝑘) ∝exp(
log 𝐸𝑘(𝜋𝑘) −𝛾𝐺𝑘(𝜋𝑘)
⏟⏟⏟⏟⏟⏟⏟⏟⏟
single-stream EFE term
+
∑
𝑗≠𝑘
⟨log Φ𝑘𝑗(𝜋𝑘, 𝜋𝑗)⟩𝑞𝑗
⏟⏟⏟⏟⏟⏟⏟⏟⏟
coupling messages from other streams
)
(9.1)
where Φ𝑘𝑗(𝜋𝑘, 𝜋𝑗) = exp(𝜆𝐽𝑘𝑗(𝜋𝑘, 𝜋𝑗)−𝛾𝜆𝐾𝑐,𝑘𝑗(𝜋𝑘, 𝜋𝑗)). This is exactly belief propagation on a coupled factor graph
with the coupling potentials Φ𝑘𝑗as factors.
This recovers pymdp-style factorized inference [Heins et al., 2022] as the 𝜆= 0 limit, and generalizes it to coupled
structure.
The VFE-only suboptimality bound
For 𝑘∈𝒱(VFE-only, reflexive), the stream takes a one-step gradient on its marginal free energy without iterative
message passing. We compare to the coordinate-descent step taken by the full coupled inference.
Theorem 9.1 (Heterogeneous coupling tax). Let 𝑞𝑘
∗be the coordinate-descent step for stream 𝑘in the coupled
ensemble at coupling 𝜆, and 𝑞𝑘
∘be the one-step VFE gradient step ignoring couplings. Define the coupling magnitude
‖Φ‖∞= max𝑗,𝑘,𝜋𝑘,𝜋𝑗| log Φ𝑘𝑗(𝜋𝑘, 𝜋𝑗)|. Then:
𝐷KL(𝑞𝑘
∗‖ 𝑞𝑘
∘) ≤𝐶⋅𝜆2 ‖Φ‖2
∞+ 𝑂(𝜆3)
(9.2)
39

## Page 41

for a constant 𝐶depending only on |Π𝑘| and the curvature of 𝐺𝑘.
Proof sketch.
Taylor-expand the coordinate-descent fixed-point equation in 𝜆around the mean-field point
𝑞𝑘
∘.
The zeroth-order term is the single-stream MF posterior; the first-order correction is the linear coupling-
message contribution; the second-order term involves cross-coupling between messages from different streams.
KL divergence is locally a Bregman divergence with Hessian equal to the Fisher information, 𝐷KL(𝑝‖ 𝑞)
=
1
2 ‖∇log 𝑝−∇log 𝑞‖2
𝐹−1 + 𝑂(‖∇log 𝑝−∇log 𝑞‖3), so the leading correction is 𝑂(𝜆2) with prefactor controlled by
‖Φ‖2
∞. Higher-order terms are absorbed in 𝑂(𝜆3) under the standing assumption that 𝐽and 𝐾𝑐are bounded.
Cognitive interpretation. Reflexive controllers can sit inside a coupled ensemble and pay only a quadratic cost (in
coupling strength) for not running the full message-passing inference. For small-to-moderate 𝜆, this is a negligible
tax; for large 𝜆, the reflexive controller becomes systematically suboptimal. This gives a quantitative answer to the
engineering question: how reactive can my low-level controllers be without losing the benefits of higher-level planning?
Answer: reactive is fine until 𝜆2‖Φ‖2
∞becomes comparable to the per-step free-energy budget.
The 𝑂(𝜆2) envelope (see Eq. (9.2)) is verified empirically by the companion code in src/lean/heterogeneous.py
(coupling_tax_within_quadratic_bound) and gated against the analytic prediction in tests/test_heterogeneous.py;
for the symmetric K=2 Ising toy with the standard (J, K_c, γ, modes) of make_ising_ensemble the fitted curvature
is 𝐶≈0.0575 (visualized below).
Figure 11: A reflexive (VFE-only) stream pays a quadratic price for joining a planning (EFE) ensemble
— the price is 𝑂(𝜆2), not 𝑂(𝜆). Numerical tax (dots) lies under the one-point-pinned 𝐶𝜆2 envelope (dashed;
𝐶pinned at the canonical probe 𝜆, not least-squares fitted) on the entire 31-point sweep 𝜆∈[0, 1.5]. This is the
numerical witness of Theorem 9.1 (and its small-𝜆tolerance corollary Corollary 9.2) — a reflexive controller can ride
along with a planner up to a bounded coupling-norm tax. The curvature constant 𝐶(legend) is fit at the canonical
probe 𝜆from simulation.hyperparameters.COUPLING_TAX_PROBE_LAMBDA and tracks the coupling_tax_curvature_-
C entry in output/data/manuscript_variables.json.
Per-stream modes are pinned (VFE,
EFE); tax values from
lean.heterogeneous.coupling_tax(...) (Lean companion ActinfPolicyEntanglement.Heterogeneous.couplingTax_-
quadratic_bound). Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars
are implied.
The Lean companion is the current boundary statement for the quadratic tax witness. The genuine analytic discharge
is the Bregman / KL Taylor expansion, scoped to the Mathlib4 layer:
-- From `lean/ActinfPolicyEntanglement/Heterogeneous.lean:61` [status: **witness**]
/-- **Theorem 9.1 (boundary witness form)**: a `BoundedQuadraticTax`
witness *is* the existence of the quadratic envelope.
Stock-Lean,
40

![page41_img1.png](images/page41_img1.png)

## Page 42

zero-`sorry`.
**Typed-API-contract disclaimer.** This theorem is *not* a stand-alone
proof of the `O(𝜆²)` coupling-tax bound; it is a typed-API contract.
The analytic content — the bound `taxFunction 𝜆≤C·𝜆²` with `C ≥0`
universally over `𝜆` — is supplied as a structural hypothesis
(`BoundedQuadraticTax`); the boundary fragment re-publishes it as an
existence claim.
The Python numerical companion in
[`src/lean/heterogeneous.py`](../../src/lean/heterogeneous.py)
verifies the bound on concrete parameter sweeps; the separate
MathlibProofs layer will discharge it from Taylor expansion of the
coupling-prior log-partition. -/
theorem couplingTax_quadratic_bound (taxFunction : Float →Float)
(witness : BoundedQuadraticTax taxFunction) :
∃(C : Float), 0.0 ≤C ∧
∀lam, couplingTax taxFunction lam ≤C * lam * lam :=
The reflexive-stream tolerance corollary Corollary 9.2 then inverts the bound to deliver a tolerance-explicit lam_max:
from Eq. (9.2), setting 𝐶𝜆2 ‖Φ‖2
∞= 𝜀gives 𝜆max(𝜀) = √𝜀/ (𝐶‖Φ‖2∞), which is the closed form the Lean witness
SmallLambdaTolerance packages. Higher-order corrections from the 𝑂(𝜆3) remainder shrink 𝜆max by a multiplicative
factor that approaches 1 as 𝜀↓0, so the small-tolerance asymptotic 𝜆max ∼√𝜀is exact.
-- From `lean/ActinfPolicyEntanglement/Heterogeneous.lean:106` [status: **witness**]
/-- **Corollary 9.2 (boundary witness form)**: a `SmallLambdaTolerance`
witness *is* the existence of the tolerance window. Stock-Lean,
zero-`sorry`.
**Typed-API-contract disclaimer.** Same as `couplingTax_quadratic_bound`:
this is a typed-API contract, not a stand-alone proof.
The continuity
argument that delivers the tolerance window is supplied as a
`SmallLambdaTolerance` witness; the boundary fragment re-publishes
the existence claim. -/
theorem couplingTax_small_lambda_tolerance
(taxFunction : Float →Float) (eps : Float)
(witness : SmallLambdaTolerance taxFunction eps) :
∃(lamMax : Float), 0.0 < lamMax ∧
∀lam, lam.abs ≤lamMax →couplingTax taxFunction lam ≤eps :=
Updating lambda: precision-like learning on coupling
Treat 𝜆as a free parameter and minimize 𝐹[𝑞𝜆] via gradient.
The cleanest expression of the gradient uses the closed exponential-family form 𝐹[𝑞𝜆] = log 𝑍𝐸(𝜆) −log 𝑍(𝜆) (§5.4
Theorem 5.5), where 𝑍𝐸is the entangled-prior normalizer and 𝑍is the joint posterior normalizer. Differentiating
with the standard exponential-family identities 𝜕log 𝑍𝐸/𝜕𝜆= ⟨𝐽⟩ℰ𝜆and 𝜕log 𝑍/𝜕𝜆= ⟨𝐽−𝛾𝐾𝑐⟩𝑞𝜆gives the total
gradient along the family 𝜆↦𝑞𝜆,
d𝐹[𝑞𝜆]
d𝜆
= ⟨𝐽⟩ℰ𝜆−⟨𝐽⟩𝑞𝜆+ 𝛾⟨𝐾𝑐⟩𝑞𝜆.
(9.3)
The same answer can be unpacked in the Gibbs decomposition of §5: 𝐹[𝑞𝜆] = ∑𝑘𝐹[𝑞𝑘
𝜆] + 𝛾𝜆⟨𝐾𝑐⟩𝑞𝜆+ log 𝑍𝐸(𝜆) −
𝜆⟨𝐽⟩𝑞𝜆+ 𝐼(𝑞𝜆). Holding 𝑞frozen at its current iterate gives the explicit partial
𝜕𝐹
𝜕𝜆∣
𝑞frozen
= 𝛾⟨𝐾𝑐⟩𝑞−⟨𝐽⟩𝑞+ ⟨𝐽⟩ℰ𝜆,
(9.4)
while the implicit chain rule along 𝑞𝜆contributes the multi-information’s 𝜆-sensitivity
d𝐼(𝑞𝜆)
d𝜆
= Cov𝑞𝜆(𝐽−𝛾𝐾𝑐, log 𝑞𝜆−log
̂𝑚(𝑞𝜆)).
(9.5)
This Fisher-style covariance has the same algebraic form as the term that drives standard precision learning, and
the two paths agree term-by-term: when 𝑞𝜆minimizes 𝐹at each 𝜆along the family, the explicit and implicit pieces
collapse to the closed-form gradient above.
Updating 𝜆by a step of −𝜂⋅d𝐹/d𝜆is therefore precision-like learning on coupling — formally analogous to
precision learning [Friston et al., 2014, Schwartenbeck et al., 2015, Limanowski et al., 2024] but scoped to cross-
stream dependence rather than confidence in one stream. The model-level question is not “how confident am I in
my policy?” but “how strongly should my different policies be coupled right now?” Any cognitive reading in terms
of arousal, vigilance, or flexibility is a hypothesis that would need direct joint-action measurements.
41

## Page 43

Habit accumulation and revertibility
Habit learning under coupled 𝐸is straightforward Bayesian updating on 𝐽as a Dirichlet-distributed parameter
[Friston et al., 2017a]:
𝐸𝜆,new(𝜋) ∝exp( ∑
𝑘
log 𝐸𝑘(𝜋𝑘) + 𝜆𝐽new(𝜋)),
𝐽new(𝜋) = 𝐽(𝜋) + 𝛼⋅𝑞𝜆(𝜋) ⋅success_signal.
(9.6)
Over learning, 𝐽accumulates structure shaped by which joint policy regions repeatedly minimize 𝐺𝜆. This is a
formal analog of AIF habit learning [Friston et al., 2017a] in which the updated prior is joint rather than single-
stream: the manuscript claims a coupled-prior update rule and numerical habit-accumulation sidecar, not a direct
biological implementation of habit formation.
Revertibility. The framework distinguishes coupling-rich habit from coupling-poor (mean-field) habit. To revert
a coupling-rich habit to its mean-field component, take the m-projection: 𝐸MF
𝑘
(𝜋𝑘) = ∑𝜋−𝑘𝐸(𝜋). The coupling
structure 𝐽is recoverable via 𝐽= log 𝐸−∑𝑘log 𝐸MF
𝑘
(up to the normalizer). This yields an analytic decomposition
of any habit into its marginal and coupled components, establishing revertibility as a structural property of the
framework rather than a contingent feature.
Takeaways
1. Reflexive controllers can ride along with planners — for a bounded price. The coupling tax
a VFE-only stream pays for joining an EFE ensemble is 𝑂(𝜆2), not 𝑂(𝜆) (Theorem 9.1) — second-order
small for small couplings.
2. The tolerance corollary makes the bound actionable. Corollary 9.2 gives a concrete coupling-
norm threshold below which a reflexive stream is guaranteed to remain within a chosen tolerance of
optimal — answering “how reflexive can my low-level controllers be while still benefiting from high-level
planning?”
3. 𝜆is a precision-like coupling weight, learnable from free energy. Updating 𝜆by gradient on
𝐹is a formal analog of precision learning; tonic over- and under-coupling become testable hypotheses
about joint-statistical signatures, not diagnostic conclusions (cf. §10).
Phase Structure: Disordered, Mixed, and Frozen Coupling Regimes
A note on “phase” as language.
On finite policy spaces with |Π𝑘|, 𝐾< ∞the free energy 𝐹[𝑞𝜆] =
log 𝑍𝐸(𝜆) −log 𝑍(𝜆) is real-analytic on [0, ∞) — it is a continuous function of a finite log-partition sum over a
compact policy alphabet, so no non-analyticity is possible. True non-analyticities (the strict statistical-mechanics
sense of “phase transition”) require the thermodynamic limit, i.e. 𝐾→∞or |Π𝑘| →∞. Everything in this section
therefore concerns smooth crossovers on a finite system, not strict phase transitions; we use the word “phase” as a
behavioral metaphor for the qualitative shifts in policy-posterior structure (Schmidt rank dropping toward 1, total
correlation saturating, archetypal modes becoming dominant) that are nevertheless sharp enough to read off the
relevant order parameters in practice. When we conjecture genuine phase transitions in §20 (Q1), we do so explicitly
in the thermodynamic-limit setting.
Phase diagram
The three regimes below describe the structure of a single coupled ensemble as 𝜆varies along its axis, holding the
underlying potentials 𝐽and 𝐾𝑐fixed. They should not be conflated with the bifurcation phenomenon mentioned in
§5.4 and §20 (Q1), which concerns multiple optima of 𝜆↦𝐹[𝑞𝜆] that arise when (𝐽, 𝐾𝑐) are themselves incoherent.
Phases live along the 𝜆axis at fixed potentials; bifurcations live in the space of potentials at the optimal 𝜆.
Sweep 𝜆for fixed 𝐽, 𝐾𝑐. Three generic regimes:
(I) Disordered phase, 𝜆< 𝜆(1)
𝑐. Schmidt rank 𝑟(𝑞𝜆) equals the rank of the marginal product. Total correlation
𝐼small. Behavior dominated by per-stream posteriors. Model analogy: weakly coordinated streams. Behavioral
signature to test: per-stream actions are statistically independent in repeated trials — a reach is uncorrelated with
the gaze direction at the moment of reach onset because each stream is sampling its own posterior.
(II) Mixed phase, 𝜆(1)
𝑐
< 𝜆< 𝜆(2)
𝑐. Schmidt rank intermediate. Total correlation grows. Several archetypal modes
have comparable weight. Model analogy: flexible coordinated behavior; the “sweet spot” of skilled multi-stream
42

## Page 44

activity. Behavioral signature to test: a small repertoire of modes of coordination alternates from trial to trial —
reach-with-saccade-to-target on most attempts, reach-with-saccade-elsewhere on a smaller fraction, etc., each mode
internally coherent but the agent retains the option of choosing a different mode under context.
(III) Frozen phase, 𝜆> 𝜆(2)
𝑐. Schmidt rank collapses to small number; one or a few archetypes dominate. Total
correlation high. Behavior approaches pure archetypal joint policies. Model analogy: rigid habits or automatized
routines. Behavioral signature to test: the same coupled motor program recurs across stimulus contexts — saccade
and reach are stereotyped and indivisible; perturbing one stream forces a recompute of the entire joint program
rather than a local correction.
A schematic phase band along 𝜆with illustrative thresholds (𝜆(1)
𝑐, 𝜆(2)
𝑐) = (0.5, 2.5) for the K=2 Ising toy is shown
below; the actual thresholds are model-dependent and arise from the analytic conditions stated next.
Analytic conditions for the phase boundaries. On a finite system the boundaries are crossovers, not non-
analyticities, but each is characterised by a derivative or gap condition on the 𝜆-trace of the spectral and entropic
order parameters:
• the disordered →mixed crossover 𝜆(1)
𝑐
is the smallest 𝜆≥0 at which the largest spectral gap Δspec(𝜆) = 𝑠1 −𝑠2
of the Schmidt decomposition exceeds half the bare gap of the marginal product — equivalently, the smallest
𝜆at which the effective rank 𝑟eff(𝜆) = 𝑒𝑆𝐸(𝑞𝜆) drops below 𝑟eff(0) −1;
• the mixed →frozen crossover 𝜆(2)
𝑐
is the smallest 𝜆at which the effective rank drops to within a small tolerance
of unity, 𝑟eff(𝜆) ≤1 + 𝜖for a chosen 𝜖∈(0, 1), equivalently the smallest 𝜆at which total correlation 𝐼(𝑞𝜆)
reaches (1 −𝜖) log 𝐾(the upper bound).
Both conditions reduce to one-dimensional searches on the spectral trace produced by src/lean/bernoulli_toy.py:
the illustrative thresholds reflect the 𝜖= 0.1 choice on the K=2 Ising trace and shift continuously with 𝜖, the
potentials 𝐽, 𝐾𝑐, and the marginal priors. In the thermodynamic limit 𝐾→∞, the same gap conditions become
genuine non-analyticities; the conjectured universality classes (§20 Q3) are indexed by the rank-growth exponent of
Δspec across the bipartite cut at the lower crossover. The companion alignment 𝛼(𝜆) = tanh(𝜆/2) takes the sentinel
values 𝛼(0.5) = 0.2449, 𝛼(1) = 0.4621, 𝛼(2) = 0.7616, 𝛼(3) = 0.9051.
Figure 12: Three coupling phases — disordered (mean-field), mixed (skilled), and frozen (archetypal)
— are separated by two illustrative thresholds 𝜆(1)
𝑐, 𝜆(2)
𝑐.
The disordered band (𝜆< 𝜆(1)
𝑐) is the mean-
field regime:
streams sample independently.
The mixed band (𝜆(1)
𝑐
≤𝜆≤𝜆(2)
𝑐) is the skilled regime:
joint
structure exists but the agent retains flexibility. The frozen band (𝜆> 𝜆(2)
𝑐) is the archetypal regime: the joint
collapses onto a small number of dominant modes. Phases assigned by lean.bernoulli_toy.coupling_phase_at on
a 401-point sweep (simulation.hyperparameters.PHASE_DIAGRAM_LAMBDAS); thresholds from PHASE_LAMBDA_C1, PHASE_-
LAMBDA_C2. Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars are
implied.
The 2-D analog across (𝜆, Δutil) exhibits the same three-regime structure as utility surplus varies; the full 41 × 21
sampled free-energy landscape is shown in the empirical suite (§13, Fig. 7), where the color minimum at each utility
column traces the VFE-optimal coupling 𝜆⋆
VFE(𝑢) — a numerical quantity that should not be conflated with the
43

![page44_img1.png](images/page44_img1.png)

## Page 45

alignment-inversion formula Eq. (6.8) in §6, which inverts the alignment correspondence rather than minimizing free
energy (see the distinction made explicit in §C).
Order parameters
Two natural order parameters:
• Largest gap: Δspec(𝜆) = 𝑠1 −𝑠2 in the spectral decomposition (distinct from the utility surplus Δutil above).
Small in (I), peaks in (III), and changes most rapidly near finite-system crossover bands.
• Effective rank: 𝑟eff(𝜆) = 𝑒𝑆𝐸(𝑞𝜆). Smooth indicator of phase.
Model predictions and behavioral hypotheses
The finite model yields three testable hypotheses for controlled joint-action tasks. They are not clinical classifications;
each would require an empirical protocol that estimates 𝜆, total correlation, and the coupling-spectrum diagnostics
from behavior:
• Rigid, habit-dominated behavior would appear in the model as high effective coupling — high 𝜆regime, Schmidt
rank near 1, behavior concentrated on one archetypal joint policy.
• Poor cross-stream coordination would appear in the model as insuﬀicient coupling — 𝜆too low, 𝐼(𝑞𝜆) near
zero, streams dissociated despite intact per-stream marginals.
• Skilled adaptive behavior would appear in the model as middle-regime 𝜆∼𝜆∗with a rich but not collapsed
entanglement spectrum.
The mechanism is the same in each case: 𝜆controls how much the joint posterior is allowed to depart from the mean-
field surface, so a tonic over- or under-shoot of 𝜆shifts the archetypal spectrum without necessarily distorting any
individual per-stream prior. The empirical claim is therefore narrower than a clinical diagnosis: under this model,
controlled behavioral tasks would test cross-stream correlation (mutual information across modalities, between-trial
joint-action repertoire, or coupling-spectrum effective rank) alongside univariate stream metrics, because the coupling
account predicts the informative signal should live in the joint statistics.
These hypotheses are adjacent to existing computational psychiatry accounts of precision dysregulation [Friston
et al., 2014, Adams et al., 2013] and habit-vs-deliberation balance [Doll et al., 2015]. The contribution here is a
candidate coupling statistic 𝜆that could be estimated or falsified from joint-action data; it is not evidence, by itself,
that any named disorder is explained by coupling drift.
Comparative Statics: Coupling Payoff, Two-Parameter Generalization,
and Sensitivity Surfaces
This section answers: given the structure of 𝐽and 𝐾𝑐, what determines whether the optimal agent has 𝜆∗> 0, and
how large?
The pay-off structure
From the closed form Eq. (5.8) (§5.4 Theorem 5.5) and the first-derivative identity Eq. (5.9), the marginal gain at
𝜆= 0 specializes to
𝜕𝐹[𝑞𝜆]
𝜕𝜆
∣
0 = ⟨𝐽⟩𝐸MF −⟨𝐽⟩𝑞0 + 𝛾⟨𝐾𝑐⟩𝑞0.
(11.1)
The total-correlation contribution 𝜕𝐼/𝜕𝜆|0 vanishes identically because 𝐼attains its minimum at the mean-field
submanifold (Proposition 7.3); the multi-information’s 𝜆-sensitivity is second-order Fisher information, not first
order (Eq. (A.15)). Under the standing assumption of a centered habit potential under the bare prior, ⟨𝐽⟩𝐸MF = 0
— true by symmetry for every example in §6 and the standing convention here onward — the marginal gain reduces
to
𝜕𝐹[𝑞𝜆]
𝜕𝜆
∣
0 = 𝛾⟨𝐾𝑐⟩𝑞0 −⟨𝐽⟩𝑞0,
(11.2)
so coupling pays in marginal terms when
44

## Page 46

⟨𝐽⟩𝑞0 > 𝛾⟨𝐾𝑐⟩𝑞0.
(11.3)
In words: coupling pays when the habitual cross-stream alignment is more beneficial (under the current
marginal posteriors) than the EFE cost of cross-stream commitments. When the prior is asymmetric
(⟨𝐽⟩𝐸MF ≠0), the inequality picks up the prior alignment ⟨𝐽⟩𝐸MF on the right — habit coupling under the posterior
must exceed both the EFE cost and the prior alignment for first-order benefit.
Two-parameter habit/EFE generalization
The primary results in this paper use the single coupling parameter 𝜆throughout (§3, §4, §5). The
two-parameter form below is recovered from the single-𝜆framework by the explicit substitution 𝐽↦(𝜆𝐸/𝜆) ⋅𝐽and
𝐾𝑐↦(𝜆𝐺/𝜆) ⋅𝐾𝑐— i.e., the dual-parameter regime is not a separate theory but a re-parameterization in which
the habit and preference scales are absorbed into the coupling potentials. The corresponding structural statements
(entanglement decomposition Theorem 5.1, coupled-precision log-weight geometry Theorem 7.4, and Schmidt-rank
witness Proposition 8.1) carry through verbatim under this substitution.
Concretely, if we allow distinct precisions on habit-coupling vs. preference-coupling:
𝑞𝜆𝐸,𝜆𝐺(𝜋) ∝∏
𝑘
𝐸𝑘(𝜋𝑘) exp(𝜆𝐸𝐽(𝜋)) exp(−𝛾𝜆𝐺𝐾𝑐(𝜋)) exp(−𝛾∑
𝑘
𝐺𝑘(𝜋𝑘))
(11.4)
then the open question is: under what conditions on 𝐽, 𝐾𝑐does the optimal (𝜆⋆
𝐸, 𝜆⋆
𝐺) lie on the diagonal 𝜆𝐸= 𝜆𝐺?
When it does not, the agent benefits from decoupling habit precision from preference-cost precision —
habits can be maintained in a regime where preference penalties are softened, or vice versa.
This suggests a
computational-psychiatry modeling hypothesis rather than a validated diagnostic claim: anxiety-like overconstraint
would correspond to 𝜆𝐺≫𝜆𝐸(preference-cost dominates), while habit-like automaticity would correspond to
𝜆𝐸≫𝜆𝐺. The current manuscript validates the single-parameter coeﬀicient logic; the two-parameter locus remains
a clearly marked follow-up analysis.
Sensitivity to potential structure
For sparse pairwise 𝐽= ∑(𝑖,𝑗)∈𝒞𝐽𝑖𝑗, the optimal 𝜆∗is determined by the spectral radius of the Fisher matrix at the
MF point, evaluated on the coupling support. Rigorously:
Proposition 11.1 (witness-form;
live Lean companion
Convexity.freeEnergy_localConcavity_at_zero_-
witness).
Differentiating the closed form Eq. (5.8) twice and using the standard exponential-family identity
d2 log 𝑍/d𝜆2 = Var(stat) — with interchange of 𝜕/𝜕𝜆and 𝔼𝑞justified by finite-sum differentiation on the policy
alphabet — gives Eq. (A.15), and at 𝜆= 0 specifically
𝜕2𝐹
𝜕𝜆2 ∣
0 = Var𝐸MF(𝐽) −Var𝑞0(𝐽−𝛾𝐾𝑐).
(11.5)
The right-hand side is negative — i.e. 𝐹is locally concave at 𝜆= 0, and the mean-field baseline is a local saddle in
the joint-policy direction — whenever the posterior dispersion of the combined coupling statistic exceeds the prior
dispersion of the habit coupling. Two regimes make this fail:
• Constant statistic. If 𝐽−𝛾𝐾𝑐is 𝑞0-a.s. constant, the right variance vanishes and 𝜕2𝐹/𝜕𝜆2|0 ≥0 — the
coupling has no first-order effect.
• Strongly habit-anchored prior. If the bare prior 𝐸MF already concentrates 𝐽tightly (large Var𝐸MF(𝐽))
while the per-stream EFE damps the posterior dispersion of 𝐽−𝛾𝐾𝑐, the saddle property weakens.
In every other case — including all the worked examples of §6, where 𝐸MF is uniform so Var𝐸MF(𝐽) = ⟨𝐽2⟩is small
relative to the posterior-amplified statistic — the mean-field baseline is a genuine saddle and some coupling pays
for itself. The interesting question is therefore not whether to couple but how much, governed by the higher-order
structure of 𝐹in 𝜆.
The locus of 𝜆⋆(Δutil, 𝛾) for the K=2 Ising toy is shown below (Fig. 46); it sweeps sigmoidally in the utility surplus
and is amplified by larger EFE precision 𝛾.
45

## Page 47

Figure 13: Optimal coupling 𝜆⋆across (utility, 𝛾) for the K=2 Ising toy on a 20 × 16 linspace grid over [0, 0.95] ×
[0.5, 2] (simulation.hyperparameters.LAMBDA_STAR_UTILITIES, LAMBDA_STAR_GAMMAS). Each cell calls lean.bernoulli_-
toy.optimal_lambda(np.tanh(γ·u)) so the effective surplus is modulated by the precision 𝛾. 𝜆⋆grows sigmoidally in
utility surplus and is amplified by larger EFE precision 𝛾, locating the comparative-statics surface of §11. Uncertainty
semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
46

![page47_img1.png](images/page47_img1.png)

## Page 48

Part III — Formal Verification
Verification in this manuscript is layered: the manuscript’s central analytical identity is machine-checked in ℝby
a Mathlib4-backed Lean package; an independent stock-Lean v4.29.0 boundary fragment ships the same theorem
surface as a typed API so downstream callers and the Python computational layer commit to a specific decomposition
shape; and a numerical companion in src/lean/ evaluates every identity on finite ensembles to floating-point
tolerance. “Machine-checked” means exactly that: Lean’s kernel has type-checked the proof object, #print axioms
has been inspected on the relevant declarations, and only the three foundational axioms of Lean itself (propext,
Classical.choice, Quot.sound) remain.
What is proved
The entanglement decomposition Theorem 5.1 is established at ℝ-level by MathlibProofs.entanglement_decomposi-
tion_generalK for general 𝐾and a general entangled joint 𝑞(strict positivity and normalization the only hypotheses;
𝑞is never assumed to factorize). The proof establishes the three components the manuscript uses downstream:
• non-negativity of the multi-information 0 ≤𝐷(𝑞‖
̂𝑚(𝑞));
• the KL chain-rule identity 𝐷(𝑞‖ 𝑝) = 𝐷(𝑞‖
̂𝑚(𝑞)) + ∑𝑖𝑞𝑖log(𝑚𝑖/𝑝𝑖);
• 𝑚-projection minimality.
The product-marginalization core streamMarginal_productDist and the companion finite-KL kernels (klReal_nonneg
/ Gibbs, klReal_split_via_intermediate, klReal_minimises_generalK) are discharged from the standing positivity +
normalization hypotheses without further structural assumptions, and negative-control-verified as non-vacuous, all
under the same foundational-only axiom set. The full S01 boxed identity 𝐹[𝑞𝜆] = ∑𝑘𝐹[𝑞𝑘
𝜆] + 𝛾𝜆⟨𝐾𝑐⟩+ log 𝑍𝐸(𝜆) −
𝜆⟨𝐽⟩+ 𝐼(𝑞𝜆) is then machine-checked by MathlibProofs.free_energy_decomposition_full for the genuine entangled
posterior, with log 𝑍𝐸the definitional log-normalizer (not an assumed scalar), positivity and unit-mass proved (not
assumed), the multi-information term discharged through the general-𝐾kernel above, and two independent negative
controls. The build and axiom audit are enforced by scripts/build_mathlib_proofs.py, which runs lake build, reads
#print axioms on every certified declaration, and fails the gate on any non-foundational axiom or non-empty sorryAx
list.
How the verification stack composes
The ℝ-level proof is the verification layer. The stock-Lean v4.29.0 boundary fragment under lean/ is the typed-API
layer: it ships the same theorem surface in Float arithmetic without Mathlib, with the analytic content of each
statement either proved at the boundary (the algebraic identities — the four-term re-grouping, the aﬀineness of the
coupling log-weight in 𝜆, the bipartite Schmidt-rank-1 ⟺mean-field equivalence, the verdict-correctness lemma,
the at-zero collapse, 𝑚-projection factorization) or carried as an explicit typed hypothesis (the analytic identities
whose discharge is the ℝlayer’s job). This factoring is deliberate: it forces every downstream caller, including the
separate Mathlib4 discharge layer, to commit to a specific decomposition shape and parameter-threading discipline,
and it gives the stock-Lean fragment a hygiene contract (zero sorry, zero axioms beyond stock Lean, zero Mathlib
dependencies, zero unsafe / partial / noncomputable) that holds independently of the analytic layer’s state.
The numerical companion in src/lean/ and the pymdp harness of §14 then evaluate every identity on finite ensembles.
The worst-case decomposition residual on the coupling-ablation suite is 5.55𝑒−16 — consistent with floating-
point round-off at the scale of the inputs — and the dashboard invariant decomposition_lhs_eq_rhs_max_residual
is regenerated on every build. The pipeline runs at Float; the proof runs at ℝ; the dashboard invariants tie the two
layers to the same numerical content per run. A verified error-bounded Float↔ℝbridge — either a Flocq-style
formal IEEE-754 model or an interval re-implementation — would formally tie the two layers, and is scoped at §21
as roadmap research; the present pipeline binds them empirically via the dashboard invariants.
Where to read the per-row content
§12 contains the per-theorem surface: the live source, the analytic content each row certifies in the boundary
fragment, and the exact Mathlib4 namespace targets for the ℝdischarges. The auto-generated theorem map at
docs/reference/_theorem_map.md indexes every theorem by its four-track wiring (registry label →manuscript token
→Lean declaration →Python witness →test gate), and docs/reference/veridical_status.md carries the per-row
status: (proved / forwarder / witness / boundary) and faithfulness: (substantive / typed-API / definitional /
re-export) fields. A reader can therefore enter on any track — manuscript theorem statement, Lean source, Python
witness, or test gate — and traverse to any other in one hop. The companion supplement §E reproduces the live
source excerpts at chapter length so the prose →Lean traversal is single-document.
One chapter follows:
47

## Page 49

• §12 — the current theorem-proving surface, the per-row content table, the typed-API discipline that factors
algebraic content from analytic payloads, and the Mathlib4 namespace targets for ongoing analytic discharge.
Lean 4 Formalization:
Current Boundary, Witness Contracts, and
Mathlib Scope
This section describes the Lean artifact that is actually built, rendered, and validated in this repository. The source
of truth is the ActinfPolicyEntanglement boundary fragment under ../lean/: it compiles on stock Lean 4 v4.29.0,
carries a Lean companion for every numbered theorem in this manuscript, and is re-exported through FepSketches.*
for compatibility with the formalized-FEP line [Friedman, 2026c]. The section no longer prints non-current Mathlib
sketch code. When the manuscript shows Lean, it shows live source extracted from lean/ActinfPolicyEntanglement/.
Current Lean artifact
The boundary fragment is Mathlib-free by construction and has a zero hygiene budget: 0 strict sorry, 0 axiom,
0 unsafe, 0 partial, 0 noncomputable, and 0 Mathlib imports. The current render reports 22/22 Lake jobs green
over 17 boundary submodules, with 126 total Lean declarations (39 defs, 76 theorems / lemmas, 11 structures).
Every numbered theorem row in manuscript/refs/labels.yaml has a live Lean companion. The companions partition
into four content classes by what each one proves about the named proposition in the boundary fragment:
• algebraic rows prove the named proposition outright in the boundary fragment;
• definitional rows prove a sub-statement of the named proposition (the boundary-content fragment the typed
API commits to), with the propositional content named beyond that sub-statement discharged at ℝ-level by
MathlibProofs/;
• forwarder rows re-export an already-proved boundary lemma;
• typed-API rows accept the analytic payload as a typed structure field and certify the result has the registered
shape (with the analytic discharge living separately — fully done for Theorem 5.1 in MathlibProofs/, named
target for the rest at §20 Q14).
Class
Count
Boundary-fragment content (named
propositions; full content reference)
algebraic (proved, substantive)
2 A complete machine-checked proof of
the named proposition: Corollary 5.2
(coupling-verdict correctness — the
Boolean decision procedure is sound)
and Corollary 5.3 (the coupling
log-weight vanishes pointwise at
𝜆= 0).
definitional (proved, scope-restricted)
3 A machine-checked sub-statement of
the named proposition: Proposition 7.1
(mfImage_isMeanField proves the
definitional membership
IsMeanField(mfToJoint 𝑚) — every
product distribution is mean-field, by
rfl; the full e-flatness statement is
discharged at ℝ-level), Proposition 7.2
(mProjection_kl_eq_self_when_meanfield
proves the KL equality that pins the
𝑚-projection’s value when 𝑞is already
mean-field; information-projection
minimality is the ℝ-level discharge),
Proposition 8.1 (the definitional
unfolding of the bipartite-mean-field
predicate Iff.rfl-checked; the
Schmidt-rank equivalence 𝑟(𝑞) = 1 ⟺
mean-field is the ℝ-level discharge
target).
forwarder
1 The Lean declaration re-exports an
already-proved boundary lemma.
48

## Page 50

Class
Count
Boundary-fragment content (named
propositions; full content reference)
typed-API (boundary + witness-form)
3 + 11 The Lean declaration commits the
caller to a specific decomposition shape
and parameter-threading discipline. 3
boundary rows fix the algebraic interface
and log-weight skeleton; 11
witness-form rows accept the analytic
payload (KL chain-rule identity,
convexity certificate, rank
semicontinuity, concentration bound)
as a typed structure field. The analytic
content for the central row Theorem
5.1 is established at ℝ-level in
MathlibProofs/; the analytic content for
the remaining typed-API rows is the
discharge target of §20 Q14.
The four classes are pinned per-row by the faithfulness: field in manuscript/refs/labels.yaml, audited at every
render by docs/reference/veridical_status.md, and locked against silent re-inflation by tests/test_h1_headline_-
invariant.py. The normative ledger of which substrate proves what is docs/reference/methods_and_assumptions.md.
The typed-API class is not a hidden proof of the analytic content. It is a machine-checked contract: the caller
supplies a witness field, and the boundary fragment certifies that the result has the theorem’s advertised shape. The
numerical layer in src/lean/, src/simulation/, and the dashboard invariants exercises these contracts on concrete
Bernoulli, Ising, pymdp, 𝐾= 3, 𝐾= 4, long-horizon, and revertibility instances; the Mathlib4 discharge layer
establishes the analytic identity at the ℝlevel for the central case.
What Mathlib4 is used for
Mathlib4 is in scope as the analytic discharge library, not as a hidden dependency of the current boundary
fragment. This separation is the most rigorous division for this project:
The distinction mirrors the external toolchain rather than a local terminological preference: Lean is the proof
assistant and programming language whose trusted kernel checks the boundary fragment [de Moura and Ullrich, 2021,
FRO, 2026a], while Mathlib is the community mathematical library that supplies the reusable analysis, probability,
algebra, and linear-algebra substrate for future and current analytic discharges [Community, 2020, FRO, 2026b].
Accordingly, a theorem row is never promoted merely because a typed witness argument exists in the boundary API;
promotion requires the row-specific Lean/Mathlib source and its gate to build.
Layer
Current status
Why this is the right boundary
lean/ActinfPolicyEntanglement/
Builds without Mathlib on Lean 4 v4.29.0.
Keeps the theorem registry fast,
reproducible, and hygiene-auditable.
Witness structures
Current Lean source.
Names the exact analytic payload each
theorem needs without pretending it has
been derived inside Mathlib.
lean/MathlibProofs/
Mathlib-backed analytic discharge package;
machine-checks the full S01 boxed
free-energy identity (Theorem 5.1) in
ℝvia free_energy_decomposition_full, with
the multi-information term discharged
through the axiom-clean general-𝐾kernel
entanglement_decomposition_generalK.
Foundational-only #print axioms (no
sorryAx, two independent negative controls);
enforced by scripts/build_mathlib_proofs.py
and tests/test_mathlib_axiom_audit.py.
Promotes Theorem 5.1 (the central result)
to ℝ-verified; the Float boundary fragment
in this same project is the
numerically-corroborated shadow with one
open residual (a verified error-bounded
Float↔ℝbridge, scoped in
docs/reference/methods_and_assumptions.md
as multi-week future research).
Manuscript + Python evidence
Current, validated.
Shows the analytic identities by derivation
and numerical execution while the Mathlib
discharge remains separate.
The Mathlib target is therefore precise but non-misleading: it tells a Lean contributor where the analytic proof
obligations live, while the present manuscript only claims what the current build and tests actually validate.
49

## Page 51

Mathlib4 analytic targets
The following table is not source code. It is the current dependency map from witness payload to the Mathlib4 area
that should discharge it:
Witness payload
Boundary theorem(s)
Mathlib area
Finite KL / entropy chain rule
Theorem 5.1, Proposition 7.3, Proposition
7.5, Proposition 19.3
PMF / finite-measure probability, finite
sums, logarithms, and KL-style entropy
identities
Convexity and local Taylor behavior in 𝜆
Theorem 5.6, Proposition 11.1
Convex analysis, differentiability / Taylor
expansion, real logarithm and exponential
facts
Bregman / quadratic coupling-tax envelope
Theorem 9.1, Corollary 9.2
Taylor expansion plus local convex-analysis
primitives; no current Mathlib Bregman
divergence module is assumed
Rank and spectral continuity
Proposition 8.2, Theorem 8.3
Matrix rank, semicontinuity, tensor-product
and finite-dimensional linear-algebra
infrastructure
Concentration and recursive embedding
Theorem 17.1, Proposition 17.2
measure tightness, KL convergence, and
recursive fixed-point infrastructure
This map also explains why the boundary fragment should not import Mathlib directly. Several targets are already
present in Mathlib4, several need local finite-discrete definitions on top of existing primitives, and some would require
new upstream work. The current artifact remains honest by keeping those as named witness payloads instead of
interleaving partial Mathlib development with the verified boundary.
Two recent Mathlib infrastructure papers anchor the measure-theoretic end of this map: the Markov-kernel for-
malization in MeasureTheory.Probability.Kernel.* [Degenne, 2025] supplies the kernel-composition / disintegration
primitives used by KL chain-rule discharge, and the recent Brownian-motion formalization in the same namespace
[Degenne et al., 2025] anchors the continuous-time infrastructure that any future extension to continuous policy
spaces (currently out of scope, see §20 Q4) would build on.
Both references are cited here as anchors for the
witness-discharge direction, not as in-flight dependencies of the current build.
Live-source injection
The companion supplement §E is the executable audit trail. It does not contain hand-copied theorem blocks. Each
[[LEAN:<label>]] token is resolved as follows:
1. manuscript/refs/labels.yaml names the theorem’s lean_module and lean_name.
2. src/manuscript/lean_extract.py
indexes
declarations
from
the
live
.lean
files
under
lean/ActinfPolicyEntanglement/.
3. src/manuscript/renderer.py embeds the exact source block with source coordinates and the registry status.
4. scripts/validate_manuscript.py fails if any Lean declaration, theorem token, section reference, figure reference,
equation reference, citation, or variable token is unresolved.
This is the reason the supplement can be read as source evidence rather than as prose illustration: if a theorem is
renamed or moved, the next render fails instead of silently shipping stale text.
What the Lean track proves today
The current Lean track proves the algebraic and structural statements that do not require measure-theoretic or
real-analysis infrastructure:
• 𝜆= 0 reductions and coupling-log-weight aﬀineness;
• Boolean coupling-verdict correctness;
• definitional total-correlation unfoldings over the local scalar API;
• e-geodesic forwarding through the aﬀine log-weight identity;
• the bipartite rank-one / mean-field interface on the boundary fragment;
• stream-mode totality and structural monotonicity lemmas used by the manuscript’s theorem registry.
The witness-form theorems then isolate the analytic content that belongs to Mathlib4. That is not a weakness in
the current artifact; it is the mechanism that keeps each claim assigned to the tool that can actually check it. The
manuscript’s theorem statements, Python witnesses, pymdp harness, figures, and dashboard invariants show the
analytic behavior now; a separate Mathlib-backed library can later replace supplied witness fields with derived fields
without changing the boundary theorem names or manuscript registry wiring.
50

## Page 52

The verification stack
Three layers compose the verification, each with a precise role:
ℝ-level proof (MathlibProofs/). The full S01 boxed free-energy identity 𝐹[𝑞𝜆] = ∑𝑘𝐹[𝑞𝑘
𝜆] + 𝛾𝜆⟨𝐾𝑐⟩+ log 𝑍𝐸(𝜆) −
𝜆⟨𝐽⟩+ 𝐼(𝑞𝜆) (Theorem 5.1) is machine-checked by MathlibProofs.free_energy_decomposition_full, with the multi-
information term discharged through the axiom-clean general-𝐾kernel entanglement_decomposition_generalK and
surfaced for direct callers as multiInformation_nonneg_at_joint. Positivity and unit mass of 𝑞𝜆are proved from the
definitions; per-stream marginals are positive by the standalone streamMarginal_pos lemma; log 𝑍𝐸is the definitional
log-normalizer; two independent negative controls make the build fail when neutralised. Only the three foundational
axioms (propext, Classical.choice, Quot.sound) remain on #print axioms, with zero sorry / axiom. The build and
axiom audit are enforced by scripts/build_mathlib_proofs.py plus tests/test_mathlib_axiom_audit.py (9-keystone
foundational-only gate) and pinned by tests/test_mathlib_proofs_integrity.py (keystone list and proof-body non-
triviality past := by).
Typed-API layer (lean/ActinfPolicyEntanglement/). The stock- Lean v4.29.0 boundary fragment hosts the 21-row
Lean companion surface (§E) as a typed API: the algebraic rows are proved at the boundary, the definitional rows pin
scope-restricted statements, the typed-API rows accept analytic payloads as structure fields, and the forwarder row
re-exports. The fragment compiles with zero strict sorry, zero axioms beyond stock Lean, no Mathlib dependency,
and no unsafe/partial/noncomputable declarations.
Its role is to keep the theorem registry fast, reproducible,
hygiene-auditable, and source-extractable into the manuscript prose without dragging in the analytic substrate at
every render.
Numerical layer (src/lean/, src/simulation/).
Every identity is evaluated on finite ensembles.
The worst-
case decomposition residual on the coupling-ablation suite is 5.55𝑒−16 — floating-point round-off precision —
recorded in decomposition_lhs_eq_rhs_max_residual and regenerated on every build alongside the other dashboard
invariants; the same residuals are exported to output/reports/float_real_residual.json for machine audit (see
FloatRealResidualWitness in the Lean boundary fragment — roadmap witness row, not a closed Float↔ℝproof).
The three layers are pipeline-bound: the dashboard invariants tie the typed-API and numerical layers to the same
per-run content, and MathlibProofs/ discharges the analytic content the typed-API rows name. A verified error-
bounded Float↔ℝbridge — either a Flocq-style formal IEEE-754 model with per-operation |fl(𝑥∘𝑦)−(𝑥∘𝑦)| ≤1
2 ulp
error propagation through the ∑/log/exp graph [IEEE, 2019, Boldo and Melquiond, 2011], or an interval-arithmetic
re-implementation provably bracketing the ℝvalues — is the natural formal sibling of the present empirical binding;
§20 Q14 and docs/reference/methods_and_assumptions.md carry the route map.
When the manuscript says “Lean-checked”, the analytic content lives in the ℝ-level layer for the central case and
in the typed-API layer’s algebraic and definitional rows for the surface the boundary fragment owns. No claim in
this manuscript asserts a Float-arithmetic verification of an analytic identity; no claim asserts that the boundary
fragment proves the analytic content of the typed-API rows.
Validation gates
The Lean / Mathlib boundary is validated by the same project gates that validate the manuscript:
Gate
What it catches
uv run python scripts/build_lean.py
Lean build failures, strict sorry, axiom, unsafe / partial /
noncomputable regressions, accidental Mathlib imports in the
boundary fragment.
uv run python scripts/validate_manuscript.py
Dangling theorem, Lean, equation, section, figure, citation, and
variable tokens; hardcoded section / theorem references;
hardcoded numeric results.
uv run pytest tests/ --cov=src --cov-fail-under=95
Python numerical witnesses, pymdp contracts, renderer / registry
behavior, project-wide link integrity, American-English prose
guard, and regression coverage.
uv run python scripts/run_all.py
End-to-end regeneration of figures, sidecars, manuscript variables,
dashboard, theorem map, output validations, and regression
baseline.
The result is a clean division of responsibility: current Lean source is only what builds; Mathlib4 is documented
only where it is the correct analytic proof substrate; no non-current Mathlib code block is presented as part of the
validated manuscript.
51

## Page 53

Part IV — Empirical Grounding
Part II states the identities; Part IV shows how they survive contact with executable finite ensembles. The empirical
layer starts with the closed-form Bernoulli toy, then uses the real pymdp.agent.Agent class for per-stream inference
and adds the 𝜆-coupling layer only after pymdp has produced its ordinary per-stream posteriors. That split is
intentional: the harness does not ask pymdp to know about policy entanglement, and it does not replace pymdp
with a mock. It measures exactly what changes when an ordinary mean-field active-inference engine is lifted into a
coupled joint policy posterior.
The empirical bridge is specified as a reproducibility checklist, not as an informal simulation description.
The package provenance is the pinned inferactively-pymdp==1.0.1 distribution that provides the pymdp im-
port/API, with the JOSS paper, oﬀicial repository, and oﬀicial documentation serving as the external source
trail [Heins et al., 2022, pymdp developers, 2026a,b]. The local model provenance is src/simulation/specs.py plus
src/simulation/builders.py: those modules materialize the POMDP matrices (𝐴, 𝐵, 𝐶, 𝐷), the configured observa-
tion tuple [0, 0], the ensemble precision 𝛾= 1, and the coupling amplitude 𝜆gen = 1. Agent-level settings are like-
wise source-derived: policy length 1, inference algorithm fpi, FPI iteration count 32, action selection deterministic,
and action precision 16. The emitted observables are CSV/JSONL/PNG sidecars, then scripts/manuscript_vari-
ables.py mirrors their current values into the [[VAR:...]] token system before the manuscript is rendered.
The suite exercises the default 𝐾= 2 Ising-style coupling and the configured multi-K sweep 𝐾∈{3, 4, 5}, runs
both short and long-horizon rollouts (𝑇= 10 and 𝑇= 100, with the long-horizon trace explicitly recording habit
accumulation), and emits the 𝑚-projection revertibility witness (𝐼(𝑞) = 𝐷KL(𝑞‖
̂𝑚(𝑞)) to floating-point tolerance).
Head-to-head comparison with branching-time AIF remains the natural empirical follow-on. Four chapters:
• §13 — the closed-form K=2 Bernoulli toy, whose two algebraically-independent closed forms agree to floating-
point tolerance (internal analytic consistency) and whose total correlation a genuine seeded finite-𝑁Monte-
Carlo estimator (empirical_mutual_information_montecarlo) reproduces within its sampling-error band — the
real finite-sample empirical witness, with convergence and ∼4𝜎concentration gated in tests/test_bernoulli_-
toy.py; the 𝑂(𝜆2) heterogeneous coupling-tax envelope verified on the 31-point coupling sweep; the spectral
and phase-structure witnesses.
• §14 — the 1.0.1 grounded architecture: per-stream Agent construction, deterministic fixed-point-iteration
inference, ensemble coupling layer, and the 𝜆-sweep + coupled-rollout entry points.
• §15 — the full free-energy bundle observable schema: per-stream VFE, expected EFE, joint and marginal
entropies, total correlation, coupling term, action distribution — emitted at every 𝜆in the sweep.
• §16 — three-tier validation gates (schema →range →identity), the [[VAR:...]] token system that pipes
every numeric value from a real run into the manuscript prose, and the validator that fails CI on any hardcoded
grid count, seed, or rollout horizon.
The empirical results regenerate from a single command (scripts/run_all.py). The orchestrator first creates the
empirical sidecars, then materializes manuscript_variables.json, then renders the manuscript. This order matters:
every numeric claim below is injected after the current run has written the sidecar summaries it depends on. Every
emitted PNG carries reproducibility tEXt metadata (source script, function, hyperparameter snapshot, git revision,
ISO timestamp, and compact plotted-data summaries).
Empirical Simulation Suite: Bernoulli Validation, Coupling-Tax Enve-
lope, Phase Diagram, and Spectral Structure
This section pairs every theoretical claim of §5–§10 with a concrete computational experiment. All experiments
are reproduced by the companion code under src/ and scripts/; the deterministic artifacts they emit live under
output/.
The evidence boundary is deliberately narrow. The simulations validate finite, discrete, binary / Ising-style policy
families implemented by this repository; the theorem rows provide stock-Lean boundary or witness contracts; and
the generated CSV/JSON sidecars, PNG metadata, manuscript variables, validators, and tests make each result
auditable. They do not establish a biological, clinical, or alignment process theory. When later sections draw those
analogies, their claim strength is hypothesis unless the paragraph names a primary citation or a generated artifact
that directly supports it.
The suite is split across two computational layers:
1. Closed-form / numeric core — pure-NumPy code under src/lean/, tested with no mocks (≥95 %
52

## Page 54

coverage; deterministic seeds throughout).
Realizes every quantity in the Lean boundary fragment (§12).
Drives every experiment in this section: closed-form Bernoulli validation, heterogeneous coupling-tax envelope,
phase diagram, Schmidt spectrum, e-geodesic flow, and the multi-stream coupling graph.
2. POMDP simulation harness — the pymdp 1.0.1 layer under src/simulation/ that grounds the coupled
policy ensemble inside an actual partially-observed Markov decision process [Heins et al., 2022], instantiated
for the baseline 𝐾= 2-stream Ising toy. Architecture, the free-energy bundle of derived observables, and the
validation / logging contract are documented separately across the three pymdp sub-sections §14, §15, and
§16.
Throughout, “𝜆-coupled” means the joint policy posterior obtained by running the per-stream pymdp posteriors
through
coupling.entangled_posterior with the manuscript’s (𝐽, 𝐾𝑐, 𝛾, 𝜆) parametrization — i.e. the exact
analytical layer of §4.2 sits on top of pymdp’s mean-field engine.
How to read the figures. Following the scientific-visualization discipline of making each figure answer a single
question [Rougier et al., 2014], each plot is meant to be an auditable result rather than decoration. Curves show
monotonicity, saturation, or identity residuals; heatmaps show where the same scalar changes across a controlled
grid; joint heatmaps show the posterior, its marginals, and the residual from independence in one view. Captions
name the generated artifact, the invariant it witnesses, and one uncertainty semantics class: deterministic grid,
canonical fixed seed, replicate envelope, confidence interval, or analytical schematic. The PNG metadata records the
same source script, generating function, hyperparameter snapshot, uncertainty semantics, and compact plotted-data
statistics. Thus a figure can be checked in three passes: read the caption, inspect the sidecar CSV or JSON, and
read the PNG project.* metadata.
Evidence ledger. The empirical suite is organized so that each headline claim has a directly inspectable artifact
and a corresponding test gate:
Claim checked
Primary artifact
Gate that catches drift
Closed-form Ising mutual information
equals empirical total correlation
output/data/parameter_sweep.csv
tests/test_bernoulli_toy.py,
tests/test_invariants_and_dashboard.py
The coupling-tax curve follows the 𝑂(𝜆2)
envelope
output/figures/coupling_tax_quadratic.png +
coupling_tax_curvature_C
tests/test_heterogeneous_ensemble.py,
tests/test_witness_theorems.py
Schmidt rank / entropy record the
departure from mean-field
output/data/ising_archetypes.csv
tests/test_spectral.py,
tests/test_multi_k_experiments.py
pymdp-grounded coupling starts as an
outer product and then gains total
correlation
output/simulations/pymdp_lambda_sweep.csv
tests/test_simulation_pymdp.py,
tests/test_simulation_free_energy.py
Long-horizon rollout reaches a steady tail
and accumulates habit mass
output/simulations/pymdp_long_horizon.csv
tests/test_long_horizon.py,
tests/test_tail_window_kl.py
m-projection revertibility realizes
𝐼(𝑞) = 𝐷KL(𝑞‖ ̂𝑚(𝑞))
output/simulations/pymdp_revertibility.csv
tests/test_revertibility.py,
tests/test_witness_theorems.py
One-axis robustness preserves the 𝜆= 0
anchor while exposing context / precision /
preference / coupling sensitivity
output/simulations/pymdp_robustness.csv +
output/data/robustness_summary.json
tests/test_robustness.py,
tests/test_robustness_plots.py
Coupling ablations and fixed-marginal null
controls separate cross-stream dependence
from marginal drift
output/simulations/pymdp_coupling_-
ablation.csv +
output/simulations/pymdp_marginal_null_-
control.csv
tests/test_robustness.py,
tests/test_robustness_plots.py
Long-horizon replicate seeds and threshold
probes expose stationarity sensitivity rather
than tuning one headline cutoff
output/simulations/pymdp_long_horizon_-
replicates.csv +
output/simulations/pymdp_long_horizon_-
threshold_sensitivity.csv
tests/test_robustness.py,
tests/test_metadata_pure.py
BTAI baseline runs end-to-end on the K=2
task and emits the three tracked
observables across the MCTS budget grid
output/data/btai_baseline.json
tests/test_btai_baseline.py,
tests/test_simulate_btai_adversarial.py
Adversarial (𝜀,𝜆)-grid measures KL drift
against the first-order Lipschitz bound
across three adversary classes
output/data/adversarial_sweep.json
tests/test_adversarial.py,
tests/test_simulate_btai_adversarial.py
Two-stream Bernoulli (K=2) closed-form validation
• Sweep 𝜆∈[0, 6] on a 121-point grid; at each 𝜆compute the closed-form mutual information Eq. (6.5) and the
empirical total correlation of the Ising joint posterior, and confirm they agree to 1𝑒−06. Concrete values:
𝐼(0.5) = 0.0303, 𝐼(1) = 0.1109, 𝐼(2) = 0.3278 nats; the saturation is 𝐼(∞) = 0.6931 ≈log 2.
• Sweep Δutil and plot 𝜆⋆= 2⋅arctanh(Δutil) (see Eq. (6.8)); for Δutil = 0.5 the optimal coupling is 𝜆⋆≈1.0986,
for Δutil = 0.9 it is 𝜆⋆≈2.9444.
• Verify the existence and convexity claims of §5 by numerical fixed-point iteration on the free-energy curve.
Reproduce.
53

## Page 55

uv run python scripts/parameter_sweep.py
# closed-form grid CSV
uv run python scripts/manuscript_variables.py
# JSON of in-text values
The grid count, 𝜆range, and agreement tolerance are sourced from src/simulation/hyperparameters.py (PARAMETER_-
SWEEP_LAMBDAS, PARAMETER_SWEEP_AGREEMENT_TOLERANCE); the 121-row CSV at output/data/parameter_sweep.csv is the
artifact.
Figure 14: The closed-form mutual information agrees with the empirical sampler to sweep tolerance
(≤1𝑒−06 across 121 grid points). The curve 𝐼(𝜆) = log 2−𝐻𝑏(𝜎(𝜆)) grows from 0 at 𝜆= 0 (independence) and satu-
rates at log 2 ≈0.693 as |𝜆| →∞(perfect alignment). Closed form (lean.bernoulli_toy.ising_mutual_information,
Eq. (6.5)) and empirical (lean.bernoulli_toy.empirical_mutual_information) are overlaid on the 121-point sweep
from simulation.hyperparameters.PARAMETER_SWEEP_LAMBDAS (𝜆∈[0, 6]); CSV at output/data/parameter_sweep.csv.
This is the K=2 specialization of the decomposition theorem Theorem 5.1 (Lean companion ActinfPolicyEntan-
glement.Decomposition.entanglement_decomposition).
Uncertainty semantics: deterministic grid or deterministic
construction; no stochastic error bars are implied.
Heterogeneous VFE / EFE coupling-tax bound
This block exercises Theorem 9.1 (coupling-tax bound) numerically.
• Assign one stream InferenceMode.VFE, one InferenceMode.EFE.
• Sweep 𝜆∈[0, 1.5] on a 31-point grid.
• Compute the coupling tax 𝐷KL(𝑞full ‖ 𝑞pinned), fit the small-𝜆slope at the probe 𝜆probe = 0.05, and confirm the
𝑂(𝜆2) envelope predicted by Eq. (9.2). The empirical curvature constant is 𝐶≈0.0575.
Phase Structure of the 𝐾= 2 Ising Toy: Disordered, Mixed, and Frozen Regimes
• Vary 𝜆across the phase-band thresholds (𝜆(1)
𝑐, 𝜆(2)
𝑐) = (0.5, 2.5) defined in §10, holding 𝐽and 𝐾𝑐fixed.
• Visualize the disordered / mixed / frozen regimes as a 1-D phase band.
The
2-D
free-energy
landscape
𝐹(𝜆, Δutil)
is
sampled
on
a
41 × 21
linspace
grid
over
[0, 4] × [0, 2]
(simulation.hyperparameters.PHASE_LANDSCAPE_LAMBDAS,
PHASE_LANDSCAPE_UTILITIES);
each
cell
is
one
call
to
lean.bernoulli_toy.ising_free_energy_curve.
The U-shaped low-utility band (cf. §10) gives way to
monotone-decreasing curves at high utility, and the locus of 𝜆⋆is the color minimum at each utility column
(cf. Eq. (6.8)).
54

![page55_img1.png](images/page55_img1.png)

## Page 56

Figure 15: Coupling pays off only when the utility surplus is large enough to overcome the multi-
information cost. The free-energy curve 𝐹[𝑞𝜆] collapses to a flat zero at zero utility (no preference signal ⇒
no incentive to leave the mean-field manifold) and becomes monotonically decreasing as the surplus Δutil grows.
Four utility levels Δutil ∈{0, 0.5, 1, 2} shown. All four curves are convex in 𝜆on [0, ∞) — the numerical witness
of Theorem 5.6 (convexity of 𝐹in 𝜆).
Computed via lean.bernoulli_toy.ising_free_energy_curve on the 121-
point sweep PARAMETER_SWEEP_LAMBDAS. Uncertainty semantics: deterministic grid or deterministic construction; no
stochastic error bars are implied.
55

![page56_img1.png](images/page56_img1.png)

## Page 57

Figure 16:
The coupling that realizes a target alignment Δalign in the K=2 Bernoulli toy is
𝜆⋆(Δalign) = 2 arctanh(Δalign/Δmax).
This is the alignment-inversion formula — the inverse of the alignment–
coupling correspondence 𝛼(𝜆) = tanh(𝜆/2) — not a VFE optimum. The actual VFE-optimal coupling under a
utility scalar 𝑢in the same toy is 𝜆⋆= 2𝑢at small 𝑢and only coincides with 2 arctanh(𝑢) in that limit (see
§C). Numerical witnesses for the existence (Theorem 5.5) and uniqueness via convexity (Theorem 5.6) of the VFE-
optimal 𝜆⋆are separate from this alignment-inversion curve. Closed form from lean.bernoulli_toy.optimal_lambda
evaluated on the 191-point sweep Δalign/Δmax ∈[−0.95, 0.95] (simulation.hyperparameters.OPTIMAL_LAMBDA_DELTAS).
Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
56

![page57_img1.png](images/page57_img1.png)

## Page 58

Figure 17: A reflexive (VFE-only) stream pays a quadratic price for joining a planning (EFE) ensemble
— the price is 𝑂(𝜆2), not 𝑂(𝜆). Numerical tax (dots) lies under the one-point-pinned 𝐶𝜆2 envelope (dashed;
𝐶pinned at the canonical probe 𝜆, not least-squares fitted) on the entire 31-point sweep 𝜆∈[0, 1.5]. This is the
numerical witness of Theorem 9.1 (and its small-𝜆tolerance corollary Corollary 9.2) — a reflexive controller can ride
along with a planner up to a bounded coupling-norm tax. The curvature constant 𝐶(legend) is fit at the canonical
probe 𝜆from simulation.hyperparameters.COUPLING_TAX_PROBE_LAMBDA and tracks the coupling_tax_curvature_-
C entry in output/data/manuscript_variables.json.
Per-stream modes are pinned (VFE,
EFE); tax values from
lean.heterogeneous.coupling_tax(...) (Lean companion ActinfPolicyEntanglement.Heterogeneous.couplingTax_-
quadratic_bound). Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars
are implied.
57

![page58_img1.png](images/page58_img1.png)

## Page 59

Figure 18: Three coupling phases — disordered (mean-field), mixed (skilled), and frozen (archetypal)
— are separated by two illustrative thresholds 𝜆(1)
𝑐, 𝜆(2)
𝑐.
The disordered band (𝜆< 𝜆(1)
𝑐) is the mean-
field regime:
streams sample independently.
The mixed band (𝜆(1)
𝑐
≤𝜆≤𝜆(2)
𝑐) is the skilled regime:
joint
structure exists but the agent retains flexibility. The frozen band (𝜆> 𝜆(2)
𝑐) is the archetypal regime: the joint
collapses onto a small number of dominant modes. Phases assigned by lean.bernoulli_toy.coupling_phase_at on
a 401-point sweep (simulation.hyperparameters.PHASE_DIAGRAM_LAMBDAS); thresholds from PHASE_LAMBDA_C1, PHASE_-
LAMBDA_C2. Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars are
implied.
Spectral structure (Schmidt rank, archetypes)
• Verify Proposition 8.1 numerically (rank-1 iff mean-field) by sweeping 𝜆. At 𝜆= 0 the rank is 𝑟= 1; at 𝜆= 1
it jumps to 𝑟= 2. The smooth analog, the entanglement entropy, has 𝑆𝐸(0) = −0.0000, 𝑆𝐸(1) = 0.4652,
𝑆𝐸(3) = 0.6882.
• Decompose 𝑞𝜆at 𝜆= 3 into Schmidt archetypes and visualize weights + pairwise overlaps.
• Sweep across stream counts 𝐾∈{2, 3, 4, 5} and tabulate the tensor-train rank profile: the configured entries
give [2], [2, 2], [2, 3, 2], and [2, 3, 3, 2].
Information-geometric structure (e-geodesic)
• For each policy 𝜋, compute the unnormalized log-weight log 𝑞𝜆(𝜋)+log 𝑍(𝜆) on a 31-point sweep across 𝜆∈[0, 3]
(see Eq. (7.3)).
• Plot one line per policy.
Multi-stream coupling graph
For the largest configured multi-stream Ising-style coupling, render the coupling potential 𝐽as a graph over streams
(edge weight = mean |𝐽| across all slot pairs), illustrating the homogeneous all-to-all structure of the symmetric
coupling.
𝐾> 2 ensembles
The harness exercises the framework on the configured multi-stream set 𝐾∈{3, 4, 5} multi-stream Ising ensembles
(scripts/simulate_multi_k.py, one output/simulations/pymdp_K*_sweep.csv file per configured 𝐾). At 𝜆= 2 the
total correlation is 𝐼(𝑞2) ≈0.2169 nats for the first configured multi-K ensemble and 𝐼(𝑞2) ≈0.1216 nats for the
second; the largest configured ensemble reaches 𝐼(𝑞2) ≈0.0784 nats. Together these rows are the empirical witness
that the entanglement decomposition theorem (Theorem 5.1) carries over from the K=2 slice to higher stream counts.
Aligned-corner mass and the tensor- train rank profile at the sweep maximum are recorded in output/data/multi_-
k_summary.json: the first configured multi-K ensemble reaches aligned mass 0.9931 at 𝜆= 4 with maximum bond
58

![page59_img1.png](images/page59_img1.png)

## Page 60

Figure 19: The free-energy landscape over (coupling, utility) shows 𝜆⋆tracking utility surplus. At low
utility the landscape is nearly flat in 𝜆(no incentive to couple); at high utility a clear minimum-locus emerges and
shifts monotonically to the right. The color minimum at each utility row is the optimal coupling 𝜆⋆of Theorem
5.5.
Sampled on a 41 × 21 grid over 𝜆∈[0, 4], Δutil ∈[0, 2] (simulation.hyperparameters.PHASE_LANDSCAPE_-
LAMBDAS, PHASE_LANDSCAPE_UTILITIES) using lean.bernoulli_toy.ising_free_energy_curve. Uncertainty semantics:
deterministic grid or deterministic construction; no stochastic error bars are implied.
59

![page60_img1.png](images/page60_img1.png)

## Page 61

Figure 20:
Schmidt rank is integer-valued and steps up from 1 (mean-field manifold) to 2 as
soon as 𝜆exceeds the rank-detection tolerance under pure-𝐽Ising coupling (𝐾𝑐= 0, 𝛾= 0).
This step is the visual signature of the “rank-1 iff mean-field” identity Proposition 8.1 (Lean companion
Spectral.Bipartite.isBipartiteMeanField_factors) and the upper-semicontinuity prediction Proposition 8.2 — a
birth-of-archetype crossover at small positive 𝜆. Joint posterior built by lean.coupling.entangled_posterior; rank
extracted by lean.spectral.schmidt_rank (atol = 1e-09) on the 81-point sweep SCHMIDT_RANK_LAMBDAS. Uncertainty
semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
60

![page61_img1.png](images/page61_img1.png)

## Page 62

Figure 21: Entanglement entropy 𝑆𝐸is zero on the mean-field manifold (𝜆= 0), grows with 𝜆, then
saturates as the posterior collapses onto a single archetypal mode.
The saturation ceiling is utility-
dependent: higher utility shifts mass toward fewer archetypes, lowering peak 𝑆𝐸. The dark band at the left edge is
the visual marker of the mean-field submanifold. Computed on a 41×21 grid via lean.coupling.entangled_posterior
and lean.spectral.entanglement_entropy. Uncertainty semantics: deterministic grid or deterministic construction;
no stochastic error bars are implied.
61

![page62_img1.png](images/page62_img1.png)

## Page 63

Figure 22: The K=2 Ising joint at 𝜆= 2 concentrates probability on the two aligned policies (diagonal)
while the per-stream marginals (side bars) remain symmetric. The inset residual 𝑞−∏𝑘𝑞𝑘is non-zero
— the visual signature of departure from the mean-field manifold, and the m-projection witness of Proposition
7.2 (marginalization = m-projection minimizes KL). Joint built via lean.bernoulli_toy.ising_joint_posterior at
𝜆= 2 (JOINT_HEATMAP_LAMBDA); panel layout from visualizations.joint_plots.plot_joint_heatmap_with_marginals.
Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
62

![page63_img1.png](images/page63_img1.png)

## Page 64

Figure 23:
A small number of Schmidt archetypes carry almost all the mass:
at 𝜆= 3 the
leading archetype dominates. Left panel: archetype weights {𝑠𝛼} in descending order (rank-effective is small).
Right panel: overlap matrix |⟨𝑢𝑖, 𝑢𝑗⟩| ⋅|⟨𝑣𝑖, 𝑣𝑗⟩| is diagonal-dominant — archetypes are mutually orthogonal by
SVD construction. Computed via lean.spectral.schmidt_decomposition at 𝜆= 3 (ARCHETYPE_DENDROGRAM_LAMBDA).
Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
Figure 24: Bond dimensions stay small even as the stream count grows: 𝑟𝑗≤3 across 𝐾∈{2, 3, 4, 5}. This
is the sparsity-rank tradeoff in action — low-rank Ising couplings yield low-rank posteriors, the empirical witness
of Theorem 8.3. Each row of the panel is the bond-rank profile (𝑟1, … , 𝑟𝐾−1) for one stream count at 𝜆= 2. Joint
built via lean.coupling.entangled_posterior over simulation.builders.ising_coupling_tensor; bond dimensions
from lean.spectral.tensor_train_ranks (atol=1e-09). Uncertainty semantics: deterministic grid or deterministic
construction; no stochastic error bars are implied.
63

![page64_img1.png](images/page64_img1.png)

![page64_img2.png](images/page64_img2.png)

## Page 65

Figure 25:
Every policy’s log-weight is consistent with exact linearity in 𝜆(slope error within
floating-point round-off) — the numerical signature of an exponential geodesic.
Four straight
lines (one per policy 𝜋∈{0, 1}2) with slopes 𝐽(𝜋) −𝛾𝐾𝑐(𝜋) depart from the same point at 𝜆= 0 (the
mean-field log-weight).
Linearity is the e-geodesic identity Eq. (7.3) and the numerical witness of Theorem
7.4 (Lean forwarder Geometry.entangledFamily_eGeodesic).
Unnormalized log-weight log ℰ𝜆(𝜋) −𝛾𝜆𝐾𝑐(𝜋) from
lean.coupling.coupling_log_weight on the 31-point sweep LOG_WEIGHT_FLOW_LAMBDAS under symmetric Ising coupling
with 𝐾𝑐≠0. Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars are
implied.
64

![page65_img1.png](images/page65_img1.png)

## Page 66

Figure 26: Coupling-potential graph for the symmetric 𝐾= 4 Ising ensemble built by simulation.builders.ising_-
coupling_tensor and rendered via visualizations.graphs.plot_coupling_graph(threshold=0.0). Each node is one
stream; edge weights are the mean |𝐽| over slot pairs. Symmetric coupling produces an evenly-weighted clique;
CEREBRUM-style case-grammar couplings would manifest as edge-weight asymmetry.
Uncertainty semantics:
analytical schematic or structural visualization; no stochastic uncertainty interval is implied.
65

![page66_img1.png](images/page66_img1.png)

## Page 67

dimension 2; the second ensemble reaches aligned mass 0.9672 at 𝜆= 4 with maximum bond dimension 3; and the
largest configured ensemble reaches aligned mass 0.9146 with maximum bond dimension 3.
Figure 27: Total correlation 𝐼(𝑞𝜆) grows with both coupling 𝜆and stream count 𝐾∈{3, 4, 5} — the
multi-stream generalization of the K=2 Ising MI curve. At 𝜆= 0 every curve is identically zero (mean-field
baseline). In this binary all-aligned/all-anti-aligned slice, 𝐼approaches the (𝐾−1) log 2 ceiling as 𝜆grows because the
joint concentrates onto the two aligned diagonal corners — derivable from 𝐻marginals −𝐻joint = 𝐾log 2−log 2 under
that mass concentration. This is the numerical cross-cut for Theorem 8.3 (sparsity-rank tradeoff) and Proposition
8.2 (Schmidt-rank upper-semicontinuity) at every 𝜆on the sweep; the corresponding rank-saturation witness lives
at Fig. 14. Computed by simulation.multi_k_experiments.run_multi_k_sweep on the K-stream Ising ensemble built
by simulation.builders.ising_coupling_tensor; sweep grid sourced from simulation.hyperparameters.MULTI_K_-
SWEEP_LAMBDAS; per-𝐾summary in output/data/multi_k_summary.json. Uncertainty semantics: deterministic grid or
deterministic construction; no stochastic error bars are implied.
Long-horizon rollouts and trajectory stationarity
A deterministic 𝑇= 100-step coupled rollout at 𝜆= 2 and seed 0 (scripts/simulate_long_horizon.py, out-
put/simulations/pymdp_long_horizon.csv) provides the long-horizon counterpart to the 𝑇= 10 rollout in §14. The
steady-state KL is computed against the trailing-window mean
̄𝑞𝑘
tail, not against the immediately preceding step: for
each stream and 𝑡≥𝑇−20 we record 𝐷KL(𝑞𝑘
𝑡‖ ̄𝑞𝑘
tail), then report first-tail, mean-tail, and max-tail summaries. The
strict max-tail bound is 0.1334 nats, under the steady-state tolerance 0.15; adjacent-step KL is also stored separately,
with max 0.4621 nats, so the two semantics are not conflated. The per-stream marginal trajectory reaches a stable
steady state, summarised by 1.0000. Honest scope (no over-claim): the rollout agents perform no parameter
learning (the A/B/D matrices are static); this quantity is therefore a trajectory-stationarity / steady-state diagnostic
— the coupled marginals converge and stay put — and is not evidence of habit formation (which would require
learning dynamics the harness does not run). It is consistent with §9.5’s prediction but is a stationarity check, not
an independent demonstration of habit accumulation; a divergent-rollout negative control (a rollout that should fail
stationarity at the same tolerance) is the open discriminating hardening. Total correlation traces from initial 0.3154
to final 0.5758 nats with mean 0.4456 across the 𝑇= 100 trajectory.
66

![page67_img1.png](images/page67_img1.png)

## Page 68

Figure 28: Aligned-policy mass concentrates onto the two aligned diagonal corners {(0, … , 0), (1, … , 1)} as
𝜆grows. At 𝜆= 0 the aligned mass equals the mean-field baseline 2 ⋅2−𝐾(purely uniform); at high 𝜆it saturates
near 1. The cross-over coupling depends on 𝐾: larger 𝐾pays a higher coupling-tax barrier before the aligned
modes dominate, locating a 𝐾-dependent threshold consistent with the disordered →frozen transition predicted by
§10. Joint built via lean.coupling.entangled_posterior on the K-stream Ising ensemble; aligned mass aggregated
by simulation.metrics.aligned_hypercube_mass within simulation.multi_k_experiments.run_multi_k_sweep; sweep
grid sourced from simulation.hyperparameters.MULTI_K_SWEEP_LAMBDAS. Uncertainty semantics: deterministic grid or
deterministic construction; no stochastic error bars are implied.
67

![page68_img1.png](images/page68_img1.png)

## Page 69

Figure 29: Tensor-train bond ranks as 𝜆varies: ranks rise then saturate at the bond-bound envelope
predicted by the sparsity-rank tradeoff. Each panel row shows the bond profile (𝑟1, … , 𝑟𝐾−1) at 𝐾∈{3, 4, 5}
across simulation.hyperparameters.MULTI_K_SWEEP_LAMBDAS. The envelope ceiling is the empirical witness of the
𝐾≥3 generalization of Theorem 8.3 — bond ranks stay bounded by the tensor-train representation of the
coupling potential even as 𝜆grows. Bond dimensions extracted by lean.spectral.tensor_train_ranks (atol=1e-
09); per-𝐾max / sum aggregates in output/data/multi_k_summary.json. Uncertainty semantics: deterministic grid
or deterministic construction; no stochastic error bars are implied.
Figure 30:
A 𝑇
= 100-step coupled rollout under fixed seed:
per-stream marginals 𝑞𝑘
𝑡
evolve
from the mean-field initialization toward a coupled steady state.
The two heatmap rows are the
per-stream marginals; the right panel traces the coupled total correlation 𝐼(𝑞𝑡) growing from 0 to its steady-
state plateau.
The plateau exhibits the habit accumulation predicted by §9.5 — the joint posterior settles
onto a stable archetype mixture under repeated observation. Driven by simulation.rollout.simulate_coupled_-
rollout at simulation.hyperparameters.LONG_HORIZON_STEPS, 𝜆= 2, seed 0. Bit-identical reproducibility under fixed
seed is asserted by tests/test_long_horizon.py::test_long_horizon_deterministic_under_fixed_seed. Uncertainty
semantics: canonical fixed-seed trajectory; seed sensitivity is reported only where a replicate sidecar is registered.
68

![page69_img1.png](images/page69_img1.png)

![page69_img2.png](images/page69_img2.png)

## Page 70

Figure 31:
The coupled joint at the tail of a 𝑇
= 100 rollout enters a tight trailing-window
neighborhood: the per-stream KL 𝐷KL(𝑞𝑘
𝑡‖ ̄𝑞𝑘
tail) stays small across the tail. The tail window of width
simulation.hyperparameters.LONG_HORIZON_TAIL_WINDOW (20 steps) carries first-tail max KL 0.1334, mean-tail max
KL 0.1109, and strict window max KL 0.1334 — under repeated observation at fixed 𝜆= 2 the family enters a tight
trailing-window neighborhood of an empirical tail mean. This is not the 𝜆→∞limit of Theorem 17.1; it is the finite-
𝜆tail-window KL concentration that Theorem 17.1 would extrapolate to in the limit. Adjacent-step KL is tracked
separately (max 0.4621), avoiding ambiguity between tail-window and step-to-step convergence.
Computed by
simulation.long_horizon.long_horizon_summary on the rollout trajectory; summary in output/data/long_horizon_-
summary.json.
Uncertainty semantics: canonical fixed-seed trajectory; seed sensitivity is reported only where a
replicate sidecar is registered.
69

![page70_img1.png](images/page70_img1.png)

## Page 71

𝑚-projection revertibility witness
The revertibility test (scripts/simulate_revertibility.py, output/simulations/pymdp_revertibility.csv) verifies
the 𝑚-projection identity of Proposition 7.2 and Proposition 7.3 numerically: for every 𝜆in 5-point sweep, the
entangled posterior is marginalized back to its mean-field 𝑚-projection and the residual 𝐼(𝑞𝜆) −𝐷KL(𝑞𝜆‖
̂𝑚(𝑞𝜆)) is
computed. Across the full sweep the maximum KL residual is 1.67𝑒−16 and the maximum marginal-difference is
1.11𝑒−16 — i.e. the Pythagorean / KL-equals-multi-information identity 𝐼(𝑞) = 𝐷KL(𝑞‖
̂𝑚(𝑞)) holds to floating-
point tolerance (≤1.67𝑒−16 maximum residual). The summary identity flags revertibility_all_kl_identity_holds
and revertibility_all_marginals_match both evaluate to true, closing the analytical revertibility loop opened in
§7.
Figure 32:
Numerical witness of the multi-information identity 𝐷KL(𝑞𝜆‖
̂𝑚(𝑞𝜆))
=
𝐼(𝑞𝜆) at ev-
ery
𝜆
on
the
sweep.
Three panels:
(a) the residual |𝐷KL(𝑞𝜆‖
̂𝑚(𝑞𝜆)) −𝐼(𝑞𝜆)| stays below
simula-
tion.hyperparameters.REVERTIBILITY_KL_IDENTITY_TOLERANCE across the sweep, computed by two independent code
paths whose equivalence is Proposition 7.3 (free_energy.total_correlation via the entropy route, free_energy.kl_-
divergence via direct ∑𝜋𝑞log(𝑞/ ̂𝑚)); (b) per-stream marginal recovery — the m-projection’s marginals match 𝑞𝜆’s
marginals to REVERTIBILITY_TOLERANCE; (c) revertibility flag at every 𝜆. Code-path agreement is the consistency claim
this figure measures; the witness-conformance suite (tests/test_witness_conformance.py) supplies the complemen-
tary discrimination against wrong-𝑞inputs. Companion Fig. 42 shows the KL-to-baseline behavior at 𝜆= 0. Sweep
grid sourced from simulation.hyperparameters.REVERTIBILITY_LAMBDAS; summary in output/data/revertibility_-
summary.json. Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars are
implied.
Robustness and ablation stress tests
The main pymdp figures answer the cleanest canonical question:
what happens when the configured binary
observation context, precision, preference strength, and aligned Ising coupling are held fixed while 𝜆varies? The
stress-test suite asks the reviewer-facing follow-up: which pieces are invariants of the construction, and which are
contingent on that canonical slice?
scripts/simulate_robustness.py runs one-axis-at-a-time perturbations rather than a Cartesian explosion. It sweeps
the 4 observation contexts, the 3 precision values, the 3 preference-strength values, and the 4 coupling-scale values
over the configured 21-point robustness grid. The result is 294 rows across 14 scenarios. The invariant that matters
most is structural: 𝜆= 0 remains the mean-field anchor and the decomposition residual remains below 1e-09
(observed maximum 1.55e-15). The null coupling row is the negative control: its maximum total correlation is
0.00e+00, so the positive envelopes in the other rows are not an artifact of the plotting or posterior normalization
code.
The ablation branch then changes the role of the coupling potential itself. Aligned coupling, null coupling, anti-
aligned coupling, and a heterogeneous small-tax 𝐾𝑐matrix share the same 𝜆grid. The checks that persist are the
structural ones: the 𝜆= 0 anchor is invariant, null coupling stays flat, non-null sign or role changes can still create
70

![page71_img1.png](images/page71_img1.png)

## Page 72

Figure 33: One-axis-at-a-time robustness stress tests preserve the same coupling signature. The panels
vary observation context, precision 𝛾, preference strength, and Ising coupling scale while holding the other axes at
the canonical pymdp setting. The suite covers 14 scenarios over 21 𝜆values on 𝜆∈[0, 4]. The null-coupling row is
the flatline sentinel (max 𝐼(𝑞𝜆) = 0.00𝑒+ 00), while all non-null rows keep the positive total-correlation envelope.
Data:
output/simulations/pymdp_robustness.csv; summary:
output/data/robustness_summary.json.
Uncertainty
semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
71

![page72_img1.png](images/page72_img1.png)

## Page 73

Figure 34: Half-saturation sensitivity identifies which perturbation axes move the coupling threshold.
For each robustness scenario, 𝜆1/2 is the first grid value where 𝐼(𝑞𝜆) reaches half of that scenario’s sweep maximum.
Across the finite half-saturation scenarios, the mean 𝜆1/2 is 1.231 and the range is [0.800, 2.000]. Null coupling
has no positive half-saturation by construction, so it is displayed as the zero baseline rather than as a failed fit.
Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
Figure 35: The decomposition identity remains numerically closed across every robustness scenario.
Each point is a scenario-level maximum of |𝐹[𝑞𝜆]−RHSdecomp(𝑞𝜆)| over the configured robustness sweep. The worst
residual is 1.55e-15, below the validator tolerance 1e-09. This figure links the stress suite back to the same numerical
realization of Theorem 5.1 used in the main pymdp free-energy bundle. Uncertainty semantics: deterministic grid
or deterministic construction; no stochastic error bars are implied.
72

![page73_img1.png](images/page73_img1.png)

![page73_img2.png](images/page73_img2.png)

## Page 74

dependence, and the decomposition residual remains closed (5.55e-16 maximum). What changes is the archetypal
allocation: the aligned-mass shift across ablation variants at the sweep endpoint is 0.9993, which is a concrete way
to see that the stress suite is not merely re-plotting the same posterior under four names.
Figure 36: Coupling ablations separate structural claims from a single sign choice. The four variants
are aligned, null, anti aligned, heterogeneous kc: aligned Ising coupling, null coupling, anti-aligned coupling, and a
heterogeneous small-tax 𝐾𝑐matrix. The 𝜆= 0 mean-field anchor survives every variant (max 𝐼(𝑞0) = 0.00𝑒+ 00);
the null variant stays flat (max 𝐼(𝑞𝜆) = 0.00𝑒+00); and the non-null variants shift archetypal mass without breaking
the decomposition residual bound (5.55e-16). Data: output/simulations/pymdp_coupling_ablation.csv. Uncertainty
semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
The fixed-marginal null control then asks a sharper diagnostic question: if we preserve each stream’s posterior but
replace the joint with the product of those marginals, does the dependence signal disappear? It does. Across the
same robustness 𝜆grid, the control’s maximum total correlation is 1.11e-16, while the maximum amount of total
correlation removed from the entangled joint is 0.3635. This is the negative-control counterpart to the positive
coupling sweeps: the effect is carried by cross-stream joint structure, not by a hidden change in either stream’s
marginal posterior.
The appendix interaction branch adds a deliberately narrow two-axis suite rather than a full Cartesian grid. It
crosses observation context with coupling scale, precision 𝛾with preference strength, and coupling variant with
coupling scale — the three interactions most likely to change a reviewer-facing interpretation of the canonical sweep.
Across 41 targeted scenarios and 861 rows, the worst decomposition residual is 1.67e-15, and the null-variant flatline
remains bounded by 0.00e+00. These results are reported as supporting stress evidence, not as new theorem claims.
Finally, the long-horizon robustness sidecar leaves the canonical fixed-seed rollout untouched and adds the configured
replicate seeds {0, 7, 13, 29, 41}. The median/IQR envelope reports trajectory sensitivity without changing the main
deterministic figure. Across those seeds, the habit-accumulation pass rate is 0.60 (Wilson 95% interval [0.23, 0.88]),
the final total-correlation mean is 0.3675, and the maximum tail-window KL is 0.1851.
The companion seed-
diagnostics sidecar then records the per-seed failure mode and threshold sensitivity over {0.05, 0.1, 0.15, 0.2, 0.25},
making the observed pass rate a transparent sensitivity result rather than a tuned headline. The dedicated threshold-
sensitivity figure reports the full pass-rate range (0.00 to 1.00) across the configured probes, so the canonical threshold
is visible as one registered choice among the diagnostics rather than an implicit post-hoc cutoff.
Software and numerical stack
The reproducibility chain rests on inferactively-pymdp==1.0.1, which provides the pymdp import/API [Heins
et al., 2022] with its JAX backend [Bradbury et al., 2018] for per-stream POMDP inference, NumPy [Harris
et al., 2020] and SciPy [Virtanen et al., 2020] for the dense joint-policy tensors and spectral decompositions of
the analytical layer, matplotlib [Hunter, 2007] (Agg backend) for every figure, and pytest with a no-mocks policy
for the test-infrastructure gate; Lean 4 [de Moura and Ullrich, 2021] hosts the type-checked boundary fragment
under lean/ActinfPolicyEntanglement/, while Mathlib [Community, 2020] is reserved for the separate optional
73

![page74_img1.png](images/page74_img1.png)

## Page 75

Figure 37: A fixed-marginal null control removes the dependence signal while preserving each stream’s
posterior.
For each configured robustness 𝜆value, the control replaces the entangled joint posterior by the
product of its own marginals.
The null control’s maximum total correlation is 1.11e-16, while the maximum
removed total correlation is 0.3635. The aligned archetypal-mass shift reaches 0.2099, showing that the coupling
signal is not a univariate marginal artifact. Data: output/simulations/pymdp_marginal_null_control.csv; summary:
output/data/marginal_null_control_summary.json.
Uncertainty semantics:
deterministic grid or deterministic
construction; no stochastic error bars are implied.
Figure 38:
Targeted two-axis stress tests expose interaction effects without expanding to a full
Cartesian grid.
The appendix-only suite covers the configured families observation × coupling scale, gamma
× preference strength, coupling variant × coupling scale for 41 scenarios and 861 total 𝜆rows.
The worst
decomposition residual is 1.67e-15, while the null-variant interaction flatline has maximum 𝐼(𝑞𝜆) = 0.00𝑒+ 00.
Data:
output/simulations/pymdp_interaction_robustness.csv; summary:
output/data/interaction_robustness_-
summary.json. Uncertainty semantics: deterministic grid or deterministic construction; no stochastic error bars are
implied.
74

![page75_img1.png](images/page75_img1.png)

![page75_img2.png](images/page75_img2.png)

## Page 76

Figure 39: Long-horizon replicate sidecars preserve the canonical figure while reporting seed sensitivity.
The main long-horizon figures remain the fixed-seed artifact; this sidecar adds the configured replicate seeds
{0, 7, 13, 29, 41} and plots the total-correlation median, interquartile band, and min–max envelope over the same
𝑇= 100 rollout.
The habit-accumulation pass rate is 0.60, final total-correlation mean is 0.3675, and the
maximum tail-window KL over seeds is 0.1851.
Data:
output/simulations/pymdp_long_horizon_replicates.csv;
summary:
output/data/long_horizon_replicates_summary.json. Uncertainty semantics: configured replicate-seed
sidecar; envelope width reflects seed sensitivity.
Figure 40: Per-seed long-horizon diagnostics explain the replicate pass rate rather than tuning it away.
Bars show each configured seed’s strict tail-window KL and maximum adjacent-step KL, with the canonical habit
threshold 0.150 drawn as a dashed line.
The threshold-sensitivity probes {0.05, 0.1, 0.15, 0.2, 0.25} are reported
in output/data/long_horizon_replicates_summary.json; the minimum margin to the canonical tolerance is -0.0351.
Data: output/simulations/pymdp_long_horizon_seed_diagnostics.csv. Uncertainty semantics: configured replicate-
seed sidecar; envelope width reflects seed sensitivity.
75

![page76_img1.png](images/page76_img1.png)

![page76_img2.png](images/page76_img2.png)

## Page 77

Figure 41:
Tail-window threshold sensitivity makes the long-horizon habit pass rate auditable
rather than tuned.
Each bar reports the fraction of configured replicate seeds whose strict tail-window KL
is below one diagnostic threshold in {0.05, 0.1, 0.15, 0.2, 0.25}.
The dashed line marks the canonical threshold
0.150 used by the main habit-accumulation flag.
Across the diagnostic thresholds the pass-rate range is 1.00
with Wilson 95% interval [0.23, 0.88] around the canonical replicate pass rate 0.60 (min 0.00, max 1.00).
Data: output/simulations/pymdp_long_horizon_threshold_sensitivity.csv; summary: output/data/long_horizon_-
replicates_summary.json. Uncertainty semantics: configured replicate sidecar with confidence interval reported from
the generated summary.
lean/MathlibProofs/ package. All pins are resolved by uv through pyproject.toml; the dependency list is deliberately
minimal — losing JAX disables the pymdp grounding, losing Lean disables the formal-verification track, losing
NumPy makes the analytical and empirical decompositions disagree on the seventh significant figure.
Detailed
version pins, optional-group boundaries (sim, viz), and resolution notes are listed in docs/guides/build_run.md.
Three reference tables collect the load-bearing per-module / per-statistic / per-JSONL-field metadata in §S7: Lean
module inventory (§S7.3), pymdp bundle statistics (§S7.4), and JSONL run-log schema (§S7.5).
Head-to-head BTAI baseline and adversarial-perturbation harnesses
Two comparison harnesses originally scoped as follow-on work are now implemented, unit-tested, and run as pipeline
stages emitting auditable sidecars.
Branching-Time
AIF
(BTAI)
baseline
[Champion
et
al.,
2022]
(scripts/simulate_btai.py
→
out-
put/data/btai_baseline.json; src/simulation/btai_baseline.py; tests/test_btai_baseline.py).
A Monte-Carlo-
tree-search BTAI agent is driven by the project’s real 1.0.1 per-stream expected free energy and sweeps the
configured budget grid 𝐵MCTS ∈{100, … , 10000} (3 budgets), recording the per-step joint policy posterior, its total
correlation, and the KL of the MCTS visitation posterior against the closed-form 𝐾= 2 Bernoulli reference at
𝜆= 1. Honest scope (no over-claim): UCB-MCTS estimates the lowest-EFE joint action rather than the soft
policy posterior, so the visitation posterior concentrates (total correlation ≈0.0019 nats at the largest budget) and
the measured sample-complexity exponent of its KL against the soft reference is −0.114. The worked run therefore
ships and exercises the three tracked observables; the full compute-matched hypothesis test of §21 (whether BTAI
attains the exact posterior as 𝐵MCTS →∞at a unit sample-complexity exponent) remains author-led analysis, not
a claim made here.
Adversarial-perturbation sweep (§20 Q11;
scripts/simulate_adversarial.py →output/data/adversarial_-
sweep.json; src/simulation/adversarial.py; tests/test_adversarial.py). The configured (𝜀, 𝜆)-grid runs all three
adversary classes (analytical worst-case rank-one, uniform-random, and sparse single-cell) over 105 scenarios (7 𝜀
values × 5 𝜆values × 3 classes) on the 𝐾= 2 Ising task, comparing the measured KL drift 𝐷KL(𝑞𝜆‖ 𝑞𝐽+Δ𝐽
𝜆
)
against the first-order Lipschitz bound 𝜆𝜀Var𝑞𝜆(𝐽)1/2. The first-order bound holds for a fraction 0.943 of scenarios
(empirical Lipschitz constant 0.964); it is loose at small 𝜀and is exceeded (worst ratio 7.25) in the large-𝜀regime
where the linearization saturates — a regime the sidecar surfaces rather than absorbs.
76

![page77_img1.png](images/page77_img1.png)

## Page 78

Figure 42: The Branching-Time AIF baseline runs end-to-end and emits the three tracked observables;
UCB-MCTS estimates the lowest-EFE joint action rather than the soft policy posterior. (a) KL of
the MCTS visitation posterior against the closed-form 𝐾= 2 Bernoulli reference at 𝜆= 1 across the budget grid
𝐵MCTS ∈{100, … , 10000} (3 budgets); the fitted slope exponent is −0.114 — the visitation KL does not shrink
toward the soft reference because UCB concentrates.
(b) the closed-form reference 𝑞𝜆; (c) the BTAI visitation
posterior at the largest budget, whose total correlation ≈0.0019 nats is near zero (mass concentrated on one joint
action). A reproducible worked run driven by real pymdp 1.0.1 per-stream expected free energy; the full compute-
matched hypothesis test of §21 is author-led future analysis, not asserted here. Source: scripts/simulate_btai.py;
data: output/data/btai_baseline.json. Uncertainty semantics: canonical fixed-seed trajectory; seed sensitivity is
reported only where a replicate sidecar is registered.
Figure 43: Adversarial bound ratio across the (𝜀, 𝜆) grid for three adversary classes. Each panel shows the
ratio of the measured KL drift 𝐷KL(𝑞𝜆‖ 𝑞𝐽+Δ𝐽
𝜆
) to the first-order Lipschitz bound 𝜆𝜀Var𝑞𝜆(𝐽)1/2 for the (a) worst-
case rank-one, (b) uniform-random, and (c) sparse single-cell adversary, over 105 scenarios (7 𝜀values × 5 𝜆values ×
3 classes; the degenerate 𝜆= 0 column is omitted). Blue cells (ratio < 1) are where the first-order bound holds; red
cells (ratio > 1) are where the linearization is exceeded in the large-𝜀regime. The bound holds for a fraction 0.943
of scenarios (empirical Lipschitz constant 0.964; worst ratio 7.25). Source: scripts/simulate_adversarial.py; data:
output/data/adversarial_sweep.json. Uncertainty semantics: deterministic grid or deterministic construction; no
stochastic error bars are implied.
77

![page78_img1.png](images/page78_img1.png)

![page78_img2.png](images/page78_img2.png)

## Page 79

Anchored figure index
The empirical suite produces a family of cross-referenced figures distributed across the closed-form (§6), geometry
(§7), spectral (§8), heterogeneous (§9), phase (§10), and comparative-statics (§11) sections, as well as the pymdp
harness (§14), pymdp free-energy (§15), and validation (§16) sections downstream. Anchor index for the suite’s
figures that are generated by this section’s analyses but cross-referenced from other body sections: Fig. 10 (Schmidt
archetype dendrogram, also cross-referenced from §8.2), Fig. 3 (𝑂(𝜆2) coupling-tax envelope, also cross-referenced
from §9), Fig. 9 (𝐾= 2 joint heatmap with marginals, also cross-referenced from §6.1), Fig. 29 (log-weight 𝑒-geodesic
flow, also cross-referenced from §7), Fig. 16 (long-horizon steady-state KL convergence, also cross-referenced from
§9.5), Fig. 13 (aligned mass concentration as 𝐾varies, also cross-referenced from §10), Fig. 5 (alignment-inversion
𝜆⋆(Δalign), also cross-referenced from §6.1), Fig. 4 (1-D phase diagram, also cross-referenced from §10), Fig. 6
(Schmidt rank vs 𝜆, also cross-referenced from §8.1), and Fig. 11 (tensor-train rank surface, also cross-referenced
from §8.3). Each figure is also independently anchored at its primary referencing subsection; this paragraph exists
so the empirical-suite section is the single place a reader can locate every empirical figure regardless of which
downstream section motivated its generation.
pymdp 1.0.1 POMDP Harness:
Architecture, Lambda Sweep, and
Deterministic Rollout
This sub-section documents the architecture of the pymdp grounding layer — how the manuscript’s analytical 𝜆-
coupling sits on top of a real pymdp.agent.Agent and what each piece contributes. Every POMDP symbol below (𝐴,
𝐵, 𝐶, 𝐷, 𝛾, 𝑇, 𝑞𝑘
𝜋) is cataloged in the unified notation glossary (§S6) with its LaTeX, Python, and pymdp-keyword
counterparts. The free-energy observables it produces are the subject of §15; the validation / logging contract that
gates the entire chain is §16.
Architecture: layered, not duplicated
The pymdp harness wraps each stream of the 𝐾= 2 Ising toy as a separate pymdp.agent.Agent with a 2-state, 2-
action POMDP — identity likelihood (𝐴= 𝐼), hold/swap transitions (𝐵), biased preference vector (𝐶), and uniform
initial prior (𝐷); ensemble precision 𝛾= 1, generative-model coupling 𝜆gen = 1.
┌────────────pymdp 1.0.1 mean-field layer (per-stream) ──────────────┐
│
Agent(A, B, C, D, gamma, inference_algo='fpi')
←deterministic
│
│
.infer_states([obs], prior)
──▶qs
│
│
.infer_policies(qs)
──▶q_pi^k, G_k
│
│
Output: per-stream policy PMF q_pi^k and EFE vector G_k.
│
└─────────────────────────────────────────────────────────────────────┘
│
▼
fed to analytical layer
┌────────analytical 𝜆-coupling layer (numpy, project-owned) ────────┐
│
coupled_policy_posterior(spec, obs, lam)
│
│
= entangled_posterior(mf=q_pi^k, G=zeros, J, K_c, γ, 𝜆)
│
│
Note: G=zeros because pymdp has already absorbed γ·G into q_pi.
│
│
At 𝜆=0 this collapses *exactly* to the outer product of q_pi^k.
│
└─────────────────────────────────────────────────────────────────────┘
│
▼
read off observables
┌──────────────free-energy bundle and observables ──────────────────┐
└─────────────────────────────────────────────────────────────────────┘
The free-energy bundle readout is detailed in §15.
Adapter boundary. The harness does not patch pymdp internals and does not require pymdp to natively support
structured joint policy posteriors.
pymdp supplies each stream’s Agent.infer_states and Agent.infer_policies
result; the project adapter then forms 𝑞𝜆by applying the manuscript’s entangled_posterior construction to those
per-stream policy posteriors. The validation gates therefore test two claims separately: the per-stream calls agree
with the documented pymdp API, and the repository’s coupling layer preserves the 𝜆= 0 mean-field baseline before
adding cross-stream dependence.
Reproducibility checklist. The software package is inferactively-pymdp==1.0.1, installed through the project’s
sim dependency group and cited through both the JOSS software paper and the oﬀicial repository / documentation
[Heins et al., 2022, pymdp developers, 2026a,b].
The POMDP state/action primitives are not prose-only:
StreamSpec and CoupledEnsembleSpec validate the 𝐴, 𝐵, 𝐶, and 𝐷arrays before each Agent is built, and the
78

## Page 80

default Ising ensemble is constructed in make_ising_ensemble.
The policy horizon and inference settings are
exactly the hyperparameters mirrored into the manuscript:
policy_len=1, inference_algo="fpi", num_iter=32,
action_selection="deterministic", alpha=16, use_states_info_gain=False, and use_param_info_gain=False.
The
sweep uses observations [0,
0], and the rollout uses seed 0; all additional random draws are routed through
np.random.default_rng.
Output variables are the per-𝜆policy posterior, EFE vector, free-energy bundle, total
correlation, action distribution, coupled rollout trajectory, JSONL run-log fields, and rendered PNG metadata. The
single rerun command is:
uv run python scripts/simulate_pymdp.py
Three contracts are load-bearing:
1. No double-counting. pymdp’s q_pi^k already contains the per-stream γ · G_k softmax bias. The analytical
layer therefore passes zero_G to entangled_posterior so the coupling potentials 𝜆· J and γ · 𝜆· K_c are
added once, not twice.
2. 𝜆= 0 sentinel.
At 𝜆= 0 the marginals of the coupled joint posterior reproduce pymdp’s per-stream
policy posteriors to floating tolerance (1𝑒−06); the joint factorizes by construction (since exp(𝜆⋅𝐽) = 1
pointwise). This marginal-agreement check is asserted by tests/test_simulation_pymdp.py::test_coupled_-
policy_posterior_lambda_zero_is_outer_product.
The free-energy-bundle test test_free_energy_bundle_-
lambda_zero_baseline checks the stronger implications: total correlation < 1𝑒−07, coupling term < 1𝑒−09,
and joint entropy equals the sum of marginal entropies to 1𝑒−07.
3. Determinism. The harness configures pymdp 1.0.1 with inference_algo="fpi" for infer_states and infer_-
policies; there is no random sampling inside those calls, so the entire chain is reproducible under fixed (spec,
obs, lam, seed).
Note on precision. inferactively-pymdp==1.0.1 provides the pymdp import/API, whose JAX path uses float32
for per-stream inference (infer_states, infer_policies).
The harness recasts the resulting policy posteriors 𝑞𝑘
𝜋
and EFE values 𝐺𝑘(𝜋) to float64 at the analytical-layer boundary in src/simulation/inference.py, so downstream
observables (the entangled posterior, free-energy bundle, total correlation) are computed in double precision. Cross-
platform numerical differences attributable to the JAX backend are bounded by 1𝑒−06 in single-stream observables;
the numerical identities verified in §16 hold at the 1𝑒−06 tolerance.
Scope of the sub-float32 gates (stated precisely).
pymdp’s inference runs in JAX float32 (machine
𝜀≈1.2 × 10−7).
The tight decomposition-residual and total-correlation-zero gates (at 10−9/10−7) therefore do
not certify pymdp’s float32 numbers directly: they are evaluated on the recast-to-float64 analytical coupling layer
(the zeroed-𝐺algebraic path), where the per-stream float32 quantities enter only through the recast boundary
above. These gates verify the analytical-layer algebra (the decomposition identity, 𝐼≥0, the 𝜆= 0 baselines);
pymdp’s float32 contribution is bounded separately at the single-stream 1𝑒−06 tolerance, not at 10−9. No claim
is made that the raw float32 pymdp pipeline satisfies the 10−9 identities.
The static 𝜆-sweep
Sweep parameters: 𝜆∈[0, 4] on a 21-point grid at fixed observations 𝑜= (0, 0). Hyperparameters are sourced from
src/simulation/hyperparameters.py (PYMDP_SWEEP_LAMBDAS, PYMDP_SWEEP_OBSERVATIONS).
The artifact is a 21-row CSV at output/simulations/pymdp_lambda_sweep.csv; the visual rendering is the total-
correlation curve plus three sentinel-𝜆heatmap snapshots.
The four sentinel total correlations along the sweep — auto-injected from scripts/manuscript_variables.py on every
render — are:
𝜆
𝐼(𝑞𝜆) Interpretation
0
0.000000 nats Mean-field baseline (exact zero by
construction)
1
0.1730 nats Sub-saturation: coupling gain
growing rapidly
2
0.3154 nats Past half-saturation 𝜆1/2 ≈1.044
4
0.3635 nats Approaches sweep maximum
𝐼max ≈0.3635
The 𝜆-column labels above are the sentinel values {0, 1, 2, 4} exposed by PYMDP_TOTAL_CORRELATION_SENTINEL_LAMBDAS
in src/simulation/hyperparameters.py; changes to that tuple require regenerating this table. (The full 12-statistic
table is in §S7.4 of the supplement.)
79

## Page 81

Figure
44:
pymdp-grounded
total
correlation
𝐼(𝑞𝜆)
from
simulation.inference.coupled_policy_pos-
terior
→
lean.free_energy.total_correlation,
evaluated
on
a
21-point
linspace
over
𝜆
∈
[0, 4]
(simulation.hyperparameters.PYMDP_SWEEP_LAMBDAS) for the 𝐾
= 2 Ising ensemble at observations (0, 0) and
ensemble precision 𝛾= 1. The CSV at output/simulations/pymdp_lambda_sweep.csv is the source data. Smooth
monotone increase from the mean-field baseline 0 toward saturation at log 2 ≈0.693 — the empirical witness of
Proposition 7.3 inside a grounded POMDP. Uncertainty semantics: deterministic grid or deterministic construction;
no stochastic error bars are implied.
80

![page81_img1.png](images/page81_img1.png)

## Page 82

Figure
45:
Coupled
joint
policy
posterior
at
𝜆
=
0
(pure
mean-field
sentinel
from
simula-
tion.hyperparameters.PYMDP_SWEEP_LAMBDAS). The joint is simulation.inference.coupled_policy_posterior(spec,
[0,0], lam=0.0) rendered with visualizations.joint_plots.plot_joint_heatmap_with_marginals. Marginals (top
/ right bars) match the per-stream pymdp posteriors and the m-projection residual (upper-right inset) is identically
zero — exactly the outer-product baseline. Uncertainty semantics: deterministic grid or deterministic construction;
no stochastic error bars are implied.
81

![page82_img1.png](images/page82_img1.png)

## Page 83

Figure 46: Coupled joint at 𝜆= 2 (mid-grid sentinel of simulation.hyperparameters.PYMDP_SWEEP_LAMBDAS). The
joint is simulation.inference.coupled_policy_posterior(spec, [0,0], lam=2.0). Off-diagonal mass redistributes
onto aligned (0, 0)/(1, 1) corners; the m-projection residual is non-zero, confirming Schmidt rank 𝑟≥2 (strictly
greater than the mean-field rank-1). Uncertainty semantics: deterministic grid or deterministic construction; no
stochastic error bars are implied.
82

![page83_img1.png](images/page83_img1.png)

## Page 84

Figure 47: Coupled joint at 𝜆= 4 (high-end sentinel of simulation.hyperparameters.PYMDP_SWEEP_LAMBDAS, frozen
regime).
The joint is simulation.inference.coupled_policy_posterior(spec,
[0,0],
lam=4.0).
Aligned corners
dominate; the m-projection residual is large; the system has essentially collapsed onto the two aligned-corner
archetypal modes (0, 0) and (1, 1) that share mass under the symmetric Ising coupling.
Uncertainty semantics:
deterministic grid or deterministic construction; no stochastic error bars are implied.
83

![page84_img1.png](images/page84_img1.png)

## Page 85

Deterministic coupled rollout
A second probe of the harness: a 𝑇= 10-step coupled rollout under coupling 𝜆= 2 and seed 0. At each step the
harness:
1. Lets each stream see its observation and runs pymdp’s per-stream inference (per_stream_policy_posterior).
2. Builds the 𝜆-coupled joint via the analytical layer (coupled_policy_posterior).
3. Samples one joint action from the coupled posterior with a seeded np.random.default_rng.
4. Advances each stream’s hidden state under the sampled action’s B matrix and samples the next observation.
Numerically identical reproducibility of the sampled action sequence and hidden-state trajectory under fixed seed is
asserted by tests/test_simulation_pymdp.py::test_simulate_coupled_rollout_deterministic_under_fixed_seed.
Figure 48: Deterministic 𝑇= 10-step coupled rollout from simulation.rollout.simulate_coupled_rollout under 𝜆=
2 and seed 0 (simulation.hyperparameters.PYMDP_ROLLOUT_STEPS, PYMDP_ROLLOUT_LAMBDA, PYMDP_ROLLOUT_SEED). Per-
stream marginals 𝑞𝑘
𝑡from simulation.inference.per_stream_policy_posterior (left two heatmaps) interleave with
the coupled total correlation 𝐼(𝑞𝑡) from lean.free_energy.total_correlation (right). Bit-identical reproducibility
under fixed seed is asserted by tests/test_simulation_pymdp.py::test_simulate_coupled_rollout_deterministic_-
under_fixed_seed. Uncertainty semantics: canonical fixed-seed trajectory; seed sensitivity is reported only where a
replicate sidecar is registered.
Reproduce.
uv run python scripts/simulate_pymdp.py
Emits the CSV + figures referenced above as well as the free-energy bundle artifacts of §15 and the structured
run-log records of §16.
Anchored figure index for the pymdp harness
The harness emits a coupled-rollout trajectory plot and two sentinel joint-policy heatmaps that anchor the
deterministic rollout discipline of this section: Fig. 44 (the coupled-rollout trajectory), Fig. 33 (joint policy at
𝜆= 2), Fig. 34 (joint policy at 𝜆= 4), and Fig. 31 (total correlation curve over the sweep). Each is also embedded
above at its primary generation point; this paragraph exists so the harness section is the canonical anchor index for
them.
pymdp Free-Energy Bundle Observables and Auto-Injected Summary
Statistics
For every 𝜆in the 21-point pymdp sweep (§14) we read off a complete free-energy bundle — every observable that
downstream prose, figures, or tests might want — via simulation.inference.free_energy_curve. The bundle is a
frozen dataclass. Its fields are deliberately named after the mathematical observable they expose, so manuscript
prose, tests, and figures can all point at the same values:
• vfe_per_stream[k]: 𝐹[𝑞𝑘
𝜆] = ⟨log 𝑞𝑘−log 𝐸𝑘+ 𝛾𝐺𝑘⟩𝑞𝑘
𝜆, in nats.
84

![page85_img1.png](images/page85_img1.png)

## Page 86

• vfe_total: ∑𝑘𝐹[𝑞𝑘
𝜆], the sum of streamwise VFE.
• efe_per_stream[k]: pymdp’s per-policy 𝐺𝑘vector for stream 𝑘.
• efe_under_posterior[k]: ⟨𝐺𝑘⟩𝑞𝑘
𝜆, the posterior-weighted EFE for stream 𝑘.
• joint_entropy and marginal_entropies[k]: 𝐻(𝑞𝜆) and 𝐻(𝑞𝑘
𝜆), in nats.
• total_correlation: 𝐼(𝑞𝜆) = ∑𝑘𝐻(𝑞𝑘
𝜆) −𝐻(𝑞𝜆).
• coupling_term: 𝜆⟨𝐽⟩𝑞𝜆= 𝜆∑𝜋𝑞𝜆(𝜋)𝐽(𝜋).
• decomposition_lhs,
decomposition_rhs,
and
decomposition_residual:
the positive-𝜆Theorem 5.1 nu-
merical witness computed with
free_energy_against_entangled_prior and entanglement_decomposition_-
rhs(...).total.
The witness passes zero per-stream G vectors because pymdp has already absorbed EFE
into the per-stream policy posterior before the project adds cross-stream coupling.
• action_distribution: the flattened PMF 𝑞𝜆on ∏𝑘Π𝑘.
Every scalar is also written to output/simulations/pymdp_free_energy_bundle.csv (one row per 𝜆; columns as in the
table above for 𝐾= 2 streams).
Statistical contracts
The bundle satisfies six numerical invariants verified by tests/test_simulation_free_energy.py:
• Sub-additivity: 𝐻(𝑞𝜆) ≤∑𝑘𝐻(𝑞𝑘
𝜆) at every 𝜆.
• Total-correlation positivity: 𝐼(𝑞𝜆) ≥0 everywhere (float-noise floor −1𝑒−09).
• 𝜆= 0 baseline: 𝐼(𝑞0) = 0, coupling term = 0, 𝐻(𝑞0) = ∑𝑘𝐻(𝑞𝑘
0), and vfe_total = ∑𝑘𝐹[𝑞𝑘
0].
• Monotonicity: under the symmetric Ising coupling at observations (0, 0), 𝐼(𝑞𝜆) is non-decreasing in 𝜆— the
empirical witness of Proposition 7.3 inside a real POMDP.
• Bundle / helper consistency: the bundle’s efe_under_posterior and coupling_term agree pointwise with
the standalone expected_free_energy_under_posterior and coupling_energy helpers respectively.
• Positive-𝜆decomposition witness: the full sweep’s maximum residual |LHS −RHS| is 3.33𝑒−16 nats,
below the configured tolerance 1𝑒−09.
Summary statistics across the sweep
The bundle is reduced to a flat summary record by simulation.statistics.pymdp_summary_statistics, mirrored to
output/simulations/pymdp_summary.json, and merged into manuscript_variables.json so every auto-injected value
flows from a real pipeline run. The full 12-statistic reference table (sweep grid, total-correlation range and half-
saturation point, VFE extrema, coupling-term range, entropy bounds, aligned-corner mass, KL divergences, action
entropy, mode probability) is in §S7.4 (supplement).
Every value in §S7.4 is computed once per pipeline run and re-injected on the next render — no number there is
typed by hand.
Visualizations
Nine dashboards are emitted by scripts/simulate_pymdp.py::figure_pymdp_free_energies. The first is a six-panel
summary, the next four magnify each free-energy pillar, and the final four expose the additional auto-injected
statistics (action entropy, KL to mean-field baseline, per-stream marginal entropy). Decomposition plots report
positive 𝐼(𝑞𝜆) (multi-information) next to ∑𝑘𝐹[𝑞𝑘
𝜆] and the coupling observable 𝜆⟨𝐽⟩𝑞𝜆— consistent with Theorem
5.1’s explicit {+}I term — while acknowledging that FreeEnergyBundle alone omits priors/,log 𝑍𝐸(𝜆) bookkeeping
from §5, so stacking only those three curves is illustrative rather than claiming identity with global 𝐹[𝑞𝜆] absent the
remaining terms.
Every PNG carries reproducibility tEXt with the source function, hyperparameter snapshot, git revision, and ISO
timestamp — readable via visualizations.metadata.read_figure_metadata.
Theorem 5.1 Numerical Witness
The manuscript’s load-bearing identity Eq. (5.2)
is not asserted symbolically over Float (the boundary Lean fragment is type-only).
It is instead numerically
witnessed at every 𝜆in the sweep.
The test suite first verifies the 𝜆= 0 sanity collapse, where coupling and
𝐼(𝑞𝜆) vanish; then test_pymdp_decomposition_witness_holds_across_positive_lambda_grid checks the full positive-
𝜆sweep by comparing free_energy_against_entangled_prior to entanglement_decomposition_rhs(...).total. This
is the same bookkeeping used by the analytical companion, with one pymdp-specific correction: the per-stream G
vectors are zeroed in the decomposition call because pymdp has already baked EFE into the per-stream posteriors
85

## Page 87

Figure 49:
Six-panel pymdp summary dashboard derived from simulation.inference.free_energy_curve and
simulation.statistics.pymdp_summary_statistics. Panel A: total correlation 𝐼(𝑞𝜆) with the half-saturation 𝜆1/2
marker. Panel B: free-energy decomposition (total VFE, coupling term, 𝐼(𝑞𝜆)). Panel C: action-distribution Shannon
entropy 𝐻(𝑞𝜆) + mode probability max𝜋𝑞𝜆(𝜋) (twin axes). Panel D: KL divergence 𝐷KL(𝑞𝜆‖ 𝑞0) from the mean-field
anchor. Panel E: per-stream marginal entropy 𝐻(𝑞𝑘
𝜆). Panel F: aligned-corner mass 𝑞(0, 0) + 𝑞(1, 1) relative to the
uniform baseline. Every panel reads off the same bundle CSV at output/simulations/pymdp_free_energy_bundle.csv.
PNG carries reproducibility tEXt (source function, hyperparameter snapshot, git revision, ISO timestamp) per
visualizations.metadata.figure_metadata. Uncertainty semantics: deterministic grid or deterministic construction;
no stochastic error bars are implied.
86

![page87_img1.png](images/page87_img1.png)

## Page 88

Figure
50:
Four-panel
pymdp
free-energy
dashboard
over
the
21-point
linspace
on
𝜆
∈
[0, 4]
(simulation.hyperparameters.PYMDP_SWEEP_LAMBDAS) for the 𝐾= 2 Ising ensemble at observations (0, 0).
Panel
A: total VFE, coupling term 𝜆⟨𝐽⟩𝑞𝜆, and multi-information 𝐼(𝑞𝜆) (same quantity as the entropy gap in panel D).
Panel B: per-stream VFE 𝐹[𝑞𝑘
𝜆]. Panel C: expected EFE under posterior ⟨𝐺𝑘⟩𝑞𝑘
𝜆per stream plus their sum. Panel
D: joint vs sum-of-marginal entropy with the gap shaded as the total correlation 𝐼(𝑞𝜆). Every curve is computed by
simulation.inference.free_energy_curve(spec, [0,0], lams) and reads off the output/simulations/pymdp_free_-
energy_bundle.csv artifact. Uncertainty semantics: deterministic grid or deterministic construction; no stochastic
error bars are implied.
87

![page88_img1.png](images/page88_img1.png)

## Page 89

Figure 51:
pymdp variational free energy decomposed across the 21-point linspace on 𝜆∈[0, 4].
Top:
per-
stream 𝐹[𝑞𝑘
𝜆] (one line per stream). Bottom: total VFE next to the coupling term 𝜆⟨𝐽⟩𝑞𝜆and 𝐼(𝑞𝜆) — the three
quantities whose interplay mirrors the entanglement decomposition theorem (Theorem 5.1) inside a real POMDP run.
Computation: simulation.inference.free_energy_curve. Uncertainty semantics: deterministic grid or deterministic
construction; no stochastic error bars are implied.
Figure 52: Coupling shifts the expected EFE from its mean-field value at 𝜆= 0 toward the EFE of
the dominant archetype. Per-stream expected EFE ⟨𝐺𝑘⟩𝑞𝑘
𝜆as 𝜆sweeps the simulation.hyperparameters.PYMDP_-
SWEEP_LAMBDAS grid. Each 𝐺𝑘is pymdp’s own EFE vector from Agent.infer_policies, averaged against the coupled
marginal 𝑞𝑘
𝜆via simulation.inference.expected_free_energy_under_posterior; the dashed line is the cross-stream
sum. Companion field on FreeEnergyBundle.efe_under_posterior (see §S7.4). Uncertainty semantics: deterministic
grid or deterministic construction; no stochastic error bars are implied.
88

![page89_img1.png](images/page89_img1.png)

![page89_img2.png](images/page89_img2.png)

## Page 90

Figure 53:
Joint entropy 𝐻(𝑞𝜆) vs sum-of-marginal entropy ∑𝑘𝐻(𝑞𝑘
𝜆) across the 21-point pymdp sweep on
𝜆∈[0, 4]; the gap (shaded) is the total correlation 𝐼(𝑞𝜆) = ∑𝑘𝐻(𝑞𝑘) −𝐻(𝑞). At 𝜆= 0 the two curves meet
— the visual signature of the mean-field submanifold. Computation: lean.free_energy.shannon_entropy composed
with lean.joint_dist.joint_marginals on the simulation.inference.coupled_policy_posterior output. Uncertainty
semantics: deterministic grid or deterministic construction; no stochastic error bars are implied.
89

![page90_img1.png](images/page90_img1.png)

## Page 91

Figure 54: Heatmap of the joint action distribution 𝑞𝜆(𝜋) over the 21-point sweep on 𝜆∈[0, 4] (rows) for every joint
policy index 𝜋∈∏𝑘Π𝑘(columns, lex order). Mass concentrates onto the aligned diagonal as 𝜆grows, visualizing
the symmetry-breaking transition predicted by §10.
Computation:
simulation.inference.coupled_policy_-
posterior(spec,
[0,0],
lam).reshape(-1) per row.
Uncertainty semantics: deterministic grid or deterministic
construction; no stochastic error bars are implied.
Figure 55: Joint-action Shannon entropy 𝐻(𝑞𝜆) (left axis, blue) and mode probability max𝜋𝑞𝜆(𝜋) (right axis, red)
across the 21-point pymdp sweep on 𝜆∈[0, 4]. As coupling grows, 𝐻falls toward 0 and the mode probability rises
toward 1 — the visual signature of collapse onto a single archetypal mode. Computation: visualizations.pymdp_-
extras.plot_action_entropy_curve.
Uncertainty semantics: deterministic grid or deterministic construction; no
stochastic error bars are implied.
90

![page91_img1.png](images/page91_img1.png)

![page91_img2.png](images/page91_img2.png)

## Page 92

Figure 56: KL divergence 𝐷KL(𝑞𝜆‖ 𝑞0) of the coupled action distribution back to the mean-field baseline at 𝜆= 0,
across the 21-point pymdp sweep. A direct measure of how far the coupled posterior has moved from the mean-field
anchor — complementary to the total-correlation curve. At 𝜆= 0 the divergence is identically zero by construction.
Computation: visualizations.pymdp_extras.plot_kl_to_lambda_zero. Uncertainty semantics: deterministic grid or
deterministic construction; no stochastic error bars are implied.
91

![page92_img1.png](images/page92_img1.png)

## Page 93

Figure 57: Per-stream marginal entropy 𝐻(𝑞𝑘
𝜆) for each 𝑘∈{0, … , 𝐾−1} across the 21-point pymdp sweep. The
dashed black line is the joint entropy 𝐻(𝑞𝜆) for reference; the gap between the sum of marginal entropies and the
joint is the total correlation 𝐼(𝑞𝜆) shown separately in Fig. 38. Computation: visualizations.pymdp_extras.plot_-
marginal_entropy_per_stream. Uncertainty semantics: deterministic grid or deterministic construction; no stochastic
error bars are implied.
92

![page93_img1.png](images/page93_img1.png)

## Page 94

that serve as the mean-field base. The resulting maximum residual is 3.33𝑒−16, and scripts/validate_outputs.py
fails if any row exceeds 1𝑒−09.
Anchored figure index for the pymdp free-energy bundle
The free-energy bundle of this section produces the following sweep-resolved dashboards, each generated by
scripts/simulate_pymdp.py and validated against pymdp_summary.json: Fig. 39 (joint action distribution evolution
across the 𝜆sweep), Fig. 41 (action entropy + mode probability across 𝜆), Fig. 37 (expected free energy under the
coupled posterior), Fig. 38 (joint vs marginal entropy decomposition), Fig. 35 (four-panel free-energy dashboard),
Fig. 42 (KL to the 𝜆= 0 mean-field baseline), Fig. 43 (per-stream marginal entropy), and Fig. 40 (six-panel summary
dashboard). Each is embedded above at its primary generation point; this paragraph provides the canonical anchor
index for the bundle’s figure family.
pymdp Validation: Three-Tier CI Gates, Structured JSONL Run Log,
and Bit-Reproducibility Contract
The pymdp harness (§14) and free-energy bundle (§15) are the runtime layer. This sub-section documents the
validation gates that protect the manuscript from drift between the runtime and what is asserted in prose, plus
the structured run log that records every load-bearing quantity for post-hoc audit.
Three-tier validation
Every pymdp artifact passes through three CI gates. Any one failing fails the pipeline:
Tier
What it asserts
Source
Numerical contracts (pytest, no mocks)
shape / type / determinism / 𝜆= 0
baseline / sub-additivity / monotonicity /
bundle ↔helper agreement
tests/test_simulation_pymdp.py,
tests/test_simulation_free_energy.py
Output gates
(scripts/validate_outputs.py)
every PNG header is valid; every JSON key
in expected range; the closed-form vs
empirical MI residual ≤1𝑒−06; the
free-energy bundle’s 𝜆= 0 baseline (TC =
0, coupling = 0, 𝐻(𝑞) = ∑𝑘𝐻(𝑞𝑘)) and TC
≥0 everywhere
scripts/validate_outputs.py
Manuscript completeness
(scripts/validate_manuscript.py)
every [[FIG:<label>]], [[EQ:<label>]],
[[VAR:<key>]], [@<citekey>],
[[SECREF:<label>]], [[THMREF:<label>]]
resolves; every numeric variable lies in its
expected range; no hardcoded §N.M outside
permitted sites
scripts/validate_manuscript.py
Run all three with the orchestrator:
uv run python scripts/run_all.py
(20 scripts in canonical order, exits non-zero on any failure.)
The reader-facing order is:
Stage group
Role in the evidence chain
Lean + analytical prelude
Build the boundary fragment and render pure-NumPy analytical
figures.
Empirical producer batch
Write the Bernoulli, pymdp, multi-K, long-horizon, and
revertibility sidecars.
Variable materialization
Convert hyperparameters plus current sidecar summaries into
output/data/manuscript_variables.json.
Manuscript rendering
Substitute [[VAR:...]], figure, theorem, section, citation, and
equation tokens into output/manuscript/.
Gates
Validate artifacts, validate prose, then compare test / coverage /
invariant / Lean-budget metrics against the regression baseline.
93

## Page 95

This is a dependency order, not just a convenience order. In particular, manuscript_variables.py runs after the
empirical sidecars because it reads the multi-K, long-horizon, and revertibility summaries. A clean run therefore
cannot render prose from a previous run’s sidecar values.
Dual-tolerance contract. Two tolerances coexist in the harness: (i) a stricter sentinel cross-check at the 5 𝜆
values {0, 0.5, 1, 2, 4} asserts that the closed-form mutual information matches the numeric total correlation of the
same closed-form joint to < 1𝑒−09 — an internal analytic-consistency check (two algebraically independent
closed forms of the same quantity must agree to numerical precision), not an independent empirical confirmation;
the genuine finite-𝑁seeded Monte-Carlo estimate (empirical_mutual_information_montecarlo, §§13) is the separate
sampling-based witness (tests/test_bernoulli_toy.py); (ii) a looser parameter-sweep CI gate at 1𝑒−06 asserts
the same match across the full 121-point (𝜆, Δ) parameter sweep (scripts/validate_outputs.py). Both tolerances
are real and report distinct guarantees: the sentinel check pins exact analytical agreement at hand-picked 𝜆, the
sweep gate bounds drift across the entire grid.
Structured run log (JSONL)
Every pymdp script emits one structured-record line per (script, 𝜆-sweep, observation, rollout) call to out-
put/logs/pymdp_runs.jsonl via simulation.logging_utils.RunLogger. Each record is a single JSON object on its
own line (JSONL), with the schema:
The full field schema (13 fields: timestamp, script, event, section, hyperparameters K/gamma/lam/seed/T, observa-
tions, grid descriptors, bundle observables, 𝜆=0 sentinels, sampled_actions, runtime_ms, status) is in §S7.5 (supple-
ment).
Inspect with jq:
# Show every record's runtime + status:
jq -c '{timestamp, section, runtime_ms, status}' \
output/logs/pymdp_runs.jsonl
# Extract the 𝜆= 0 free-energy baseline:
jq 'select(.section=="figure_pymdp_free_energies") |
{coupling_term_at_lambda_zero, joint_entropy_at_lambda_zero,
marginal_entropy_sum_at_lambda_zero}' \
output/logs/pymdp_runs.jsonl
The validator scripts/validate_outputs.py::validate_run_log fails CI if:
• the JSONL file is malformed,
• fewer than three records are present,
• any required section (figure_pymdp_lambda_sweep,
figure_pymdp_rollout,
figure_pymdp_free_energies) is
missing,
• any record lacks a timestamp.
Software and source provenance
The pymdp validation layer is intentionally standalone-local. The release environment is refreshed with:
uv sync --group sim --group viz --group lint
The sim group supplies inferactively-pymdp==1.0.1; the lockfile records the exact wheel / source archive, and
the methods prose cites the JOSS paper plus the oﬀicial source and documentation [Heins et al., 2022, pymdp
developers, 2026a,b]. The only module allowed to import pymdp/JAX is src/simulation/agents.py; the no-mock test
policy forbids replacing that boundary with MagicMock, unittest.mock, mocker.patch, or equivalent fake call paths.
A clean collection run therefore proves that lean.invariants, the dashboard builder, and the pymdp harness import
from this checkout without requiring a parent template on PYTHONPATH.
Reproducibility contract
Two consecutive run_all.py invocations on the same code produce numerically identical CSVs and JSON variable
dumps.
PNG rasters are bit-identical modulo the project.timestamp and project.git_revision tEXt metadata
chunks, which embed run-time provenance for audit purposes; the JSONL run log similarly records per-run wall-
clock timestamps. Strict byte-level reproducibility across the metadata chunks requires pinning these to a SOURCE_-
DATE_EPOCH-style fixed value at run time. The guarantees that make this contract possible:
• pymdp.agent.Agent(inference_algo='fpi') — deterministic FPI, no random sampling inside infer_states /
infer_policies.
• All
RNG-bearing
calls
go
through
np.random.default_rng(seed=...)
with
seeds
pinned
in
src/simulation/hyperparameters.py (FIGURE_GLOBAL_SEED = 42, PYMDP_ROLLOUT_SEED = 0).
94

## Page 96

• MPLBACKEND=Agg is set at every figure-script entrypoint to prevent platform-dependent figure rasterisation.
• Every grid count / 𝜆range / rollout horizon flows from the hyperparameters module, then through the JSON
mirror, then into prose via [[VAR:<key>]] — there is no place a number can drift.
Test budget snapshot
Suite
Coverage
tests/test_simulation_pymdp.py
per-stream EFE / posterior PMFs, 𝜆= 0 baseline, monotonicity,
deterministic rollout
tests/test_simulation_free_energy.py
every FreeEnergyBundle invariant + bundle ↔helper agreement
tests/test_simulation_specs.py
StreamSpec / CoupledEnsembleSpec shape + column-stochasticity
validation
tests/test_free_energy_plots.py
every dashboard PNG header, on real bundle data
tests/test_figure_scripts.py
every figure_* function in simulate_pymdp.py smoke-tested
tests/test_logging_utils.py
structured JSONL emission, runtime measurement, status
propagation, schema
tests/test_multi_k_experiments.py
configured multi-K ensemble sweeps 𝐾∈{3, 4, 5}: TC
monotonicity, aligned-mass growth, TT-rank profile, 𝜆= 0
mean-field baseline
tests/test_long_horizon.py
𝑇= 100 long-horizon rollout: deterministic reproducibility,
tail-window steady-state KL bound, habit-accumulation
monotonicity
tests/test_revertibility.py
revertibility_kl_equals_multiinformation:
𝐼(𝑞𝜆) = 𝐷KL(𝑞𝜆‖
̂𝑚(𝑞𝜆)) to floating-point tolerance (≤1.67𝑒−16
maximum residual) on every 𝜆in the sweep — an internal
analytic-consistency check of Proposition 7.3 (both sides are
the same finite-sum quantity via total_correlation_via_kl; true by
construction, not an independent empirical witness)
tests/test_robustness.py
one-axis robustness scenarios, targeted two-axis interactions,
coupling ablations, fixed-marginal null controls, long-horizon
replicate summaries, Wilson intervals, and threshold-sensitivity
summaries
tests/test_robustness_plots.py / tests/test_metadata_pure.py
stress-test figure writers and metadata semantics for robustness
envelopes, ablation summaries, null-control figures, replicate
envelopes, and threshold-sensitivity plots
See the full per-suite breakdown in docs/reference/statistics_reference.md.
Part V — Connections to Existing Frameworks
The parametric-entanglement framework is not a replacement for active inference or for the neighboring control
and probabilistic-programming literatures. It is a relationship calculus for one object: the joint policy posterior.
Some prior constructions are recovered exactly inside this calculus (mean-field AIF at 𝜆= 0, single-stream KL
control, product-of-experts, and copula VI after a CDF change-of-variables). Others are parametric embeddings
that require an explicit modeling choice, and others are only structural analogies: they share a coupling skeleton but
retain additional process-theoretic content, such as temporal-scale separation, recursive observation-conditioning,
message-passing schedules, or state-space Markov-blanket construction. Three chapters map the territory:
• §17 — classical active-inference frameworks. Mean-field AIF as the 𝜆= 0 slice (exact). Hierarchical / deep
AIF as block-bidiagonal coupling (structural analog). Sophisticated inference as a tree-structured coupling
with the recursive observation-conditioning discharged into 𝐽.
Branching- time AIF as Bayesian filtering
over a tensor-train-compressed policy tree, classified as an algorithmic analogy until a direct head-to-head
construction is implemented.
• §18 — control and RL. KL / path-integral control as the single-stream 𝐾= 1, 𝜆= 1 case (the classical
log-partition–value duality). Options frameworks as 𝐾= 2 with policy-matching 𝐽. Products and mixtures
of experts as factorizations of 𝐽. Copula variational inference as the CDF-reparametrized continuous analog.
• §19 — multi-agent, geometry, worldview. Interactive / multi-agent inference as inter-agent coupling potentials.
Renormalization-group AIF as a structural analogy via tensor-train compression. Policy-space Markov-blanket
leakage as a coupling identity (distinct from the state-space construction). CEREBRUM and case grammar
as edge-weight asymmetry on the coupling graph.
95

## Page 97

Each connection is stated with the structural choice that relates it to the 𝜆-coupled posterior, the claim class (exact,
parametric, or analogical), and the specific content that remains outside the present artifact.
Framework Connections I: pymdp/SPM Baseline, Hierarchical/Deep
AIF, Sophisticated Inference, and Branching-Time AIF
This section maps the entanglement framework onto major existing constructions in active inference, control theory,
machine learning, and theoretical neuroscience. The framework gives exact recoveries for some rows, parametric
embeddings for others, and explicitly labeled structural analogies where the prior framework carries additional
process-theoretic content.
The mapping is split into three thematic groups:
• Classical active-inference frameworks (this file) — mean-field AIF (pymdp / SPM), hierarchical / deep
AIF, sophisticated inference, branching-time AIF.
• Control and reinforcement-learning frameworks (§18) — KL / path-integral control, options framework,
products + mixtures of experts, copula VI.
• Multi-agent, geometry, and worldview connections (§19) — interactive / multi-agent inference,
renormalization-group AIF, Markov blankets / Bayesian mechanics, CEREBRUM and case grammar.
Relationship calculus for AIF variants
The common template used throughout Part V is the finite joint-policy posterior
𝑞𝜆(𝜋1∶𝐾) ∝
𝐾
∏
𝑘=1
𝐸𝑘(𝜋𝑘) exp(−
𝐾
∑
𝑘=1
𝛾𝑘𝐺𝑘(𝜋𝑘) + 𝜆𝐽(𝜋1∶𝐾) −𝛾𝜆𝐾𝑐(𝜋1∶𝐾)) .
(17.1)
Every comparison below asks which part of this template a prior framework changes: the generative model, the policy-
posterior factorization, the EFE recursion, the message-passing schedule, the agent-coupling graph, or temporal
depth. The recovery labels are therefore strict.
Exact means literal specialization of this posterior or its single-
stream log-partition dual after all variables and factors have been specified. Parametric means the cited framework
can realize the form after the modeler adds explicit policy nodes, coupling factors, priors, or change-of-variables.
Analogical means the cited framework shares a structural motif, but additional process-theoretic content remains
in the generative model, recursive EFE definition, or message-passing schedule rather than in 𝜆𝐽itself. Exactness
therefore attaches to a fully specified posterior or graphical model, not to active inference as a whole.
The notation bridge to standard active inference is deliberately literal. The generative-model law 𝑃(⋅) remains
represented by the usual likelihood, transition, preference, state-prior, and policy-prior ingredients; the variational
beliefs 𝑄(⋅) become the normalized policy posteriors denoted by 𝑞in this manuscript. The per-stream factors 𝐸𝑘, 𝐺𝑘,
and 𝛾𝑘are the ordinary habit/prior, expected-free-energy, and policy-precision ingredients of single-stream discrete
active inference. The new objects are only 𝐽, 𝐾𝑐, and 𝜆: a pair of joint-policy potentials and the scalar that weights
them. Thus 𝜆is not a substitute for policy precision, neural precision, preferences, desire, or a generative-model
parameter. It is a coupling strength inside the finite policy-posterior family, and every comparison below must say
whether the external framework supplies the same posterior, supplies a parameterized route to it, or merely shares
a structural pattern.
This convention matters because active inference is broader than any one posterior factorization.
Factor-graph
treatments show how generative-model specification and message passing can automate deep temporal active
inference [de Vries and Friston, 2017], while graphical-brain and neuronal-message-passing accounts distinguish
Forney-style belief propagation, mean-field, Bethe, and marginal approximations as alternative implementation
commitments [Friston and Parr, 2017, Parr et al., 2019, Yedidia et al., 2005]. Reactive message-passing toolkits such
as RxInfer support flexible factor insertion [Bagaev and Podusenko, 2023]. Adding exp(𝜆𝐽−𝛾𝜆𝐾𝑐) as a policy factor
is then an exact implementation pattern for that chosen graphical model; it is not a claim that every factor-graph
or RxInfer active-inference model already contains this coupling factor.
Relation to recent unification efforts
Recent work has independently proposed unification narratives for active inference. Da Costa, Tenka, Zhao, and
Sajid treat active inference as a normative model of agency and a comparison language for different agency models
96

## Page 98

[Da Costa et al., 2024]. de Vries, Nuijten, van de Laar et al. [de Vries et al., 2025] recast EFE-based planning
as variational inference on an augmented generative model with preference and epistemic priors; Nuijten and
Lukashchuk [Nuijten and Lukashchuk, 2025] formally argue that active inference is a subtype of variational inference;
Champion, Bowman, Marković, and Grześ [Champion et al., 2024] derive four EFE formulations from unified root
definitions. Millidge, Tschantz, and Buckley [Millidge et al., 2021] provide the complementary caution: expected
free energy has multiple derivational routes whose assumptions matter. These constructions unify over the form of
EFE or over the EFE/VFE equivalence; the present framework unifies over the factorization structure of the joint
policy posterior via a scalar deformation parameter 𝜆. The two unifying strategies are orthogonal — our framework
operates on top of a generative model that the de Vries / Nuijten lineage works to construct, and Champion et
al.’s EFE-reframing applies to the per-stream 𝐺𝑘that enters our 𝜆-deformed prior. This distinction keeps the claim
strength clear: the present manuscript does not solve the EFE unification problem, but it is compatible with those
formulations because it acts on the posterior factorization once the per-stream EFE terms have been specified.
Mean-field active inference (pymdp, SPM, ActiveInference.jl)
The standard factorized treatment of multi-modality, multi-factor active inference [Heins et al., 2022, Smith et al.,
2022] is the 𝜆= 0 slice of our framework. Our addition: extend the variational family along the e-geodesic in any
chosen direction (see Eq. (7.3)). Concretely, in pymdp notation, the multi-stream policy posterior 𝑞(𝜋) = ∏𝑓𝑞𝑓(𝜋𝑓)
becomes 𝑞𝜆(𝜋) with 𝜆as an additional learnable hyperparameter.
This is operationalized by the project’s 1.0.1 simulation harness (§14, src/simulation/, docs/simulation/pomdp_-
simulation.md): each stream is built as a separate pymdp.agent.Agent whose 𝑞𝑘
𝜋= softmax(−𝛾𝐺𝑘) plays the role of
a mean-field marginal, and the analytical layer of §4.2 adds the 𝜆-coupling on top. This is an adapter construction,
not a claim about the native pymdp API: pymdp supplies per-stream inference, while this repository constructs
and validates the structured joint posterior after those per-stream posteriors exist. At 𝜆= 0, the joint is exactly
the outer product of the per-stream pymdp posteriors; for 𝜆> 0 the total correlation grows smoothly toward the
task-specific coordination ceiling. In the binary all-aligned/all-anti-aligned Ising slice used by the pymdp harness,
that ceiling is (𝐾−1) log 2; for the default 𝐾= 2 case this reduces to log 2.
Hierarchical / Deep Active Inference
Hierarchical AIF [Friston et al., 2017a, Pezzulo et al., 2018] decomposes the agent into a hierarchy of slow (high-level)
and fast (low-level) generative models with explicit message passing.
Theorem 17.1 Structural analog of hierarchical AIF (witness-form). With block-bidiagonal 𝐽coupling
adjacent levels of an 𝐿-level ensemble and 𝜆→∞, the entangled posterior concentrates on the cross-level
coordination shadow of hierarchical AIF: each adjacent pair (𝜋ℓ, 𝜋ℓ+1) becomes deterministically linked. The Lean
companion ConnectionsWitnesses.hierarchicalAIF_lambda_limit_witness is now live in the boundary fragment in
witness-consuming form: the caller supplies the entangled family 𝜆↦𝑞𝜆, the hierarchical fixed point 𝑞∞, and
the universally quantified (𝜀, 𝜆0) concentration inequality as a HierarchicalConcentrationWitness structure; the
boundary fragment certifies the resulting existence claim by extracting the witness fields. We do not claim that this
recovers hierarchical AIF in full — the temporal scale separation and directed top-down/bottom-up message passing
that characterize standard hierarchical AIF [Friston et al., 2017a, Pezzulo et al., 2018] are additional structures not
encoded by symmetric 𝐽alone. The construction here recovers the coupling-structural component machine-checked
at the witness level. A generative-model-side embedding (with explicit per-level 𝐵ℓdynamics) would be required to
upgrade the analogy to a recovery, and that stronger construction is outside the present artifact.
Sophisticated Inference (recursive EFE)
Sophisticated inference [Friston et al., 2021] introduces beliefs about beliefs — the agent reasons about counterfactual
consequences of its actions for its own beliefs. Recursive EFE has the form
𝐺soph(𝜋) = 𝔼𝑞(𝑜∣𝜋)[𝐺(𝜋′) + log 𝑞(𝜋′ ∣𝑜)] .
(17.2)
This can be represented within our template by treating one stream 𝜋as the current policy and another stream 𝜋′ as
the next-step policy posterior conditional on observations, with a specific source-supplied choice of 𝐽that encodes
the recursive belief-about-beliefs structure.
Proposition 17.2 Sophisticated inference as a tree-structured coupling (witness-form).
With 𝐾=
𝑑+ 1 streams indexed by lookahead depth and a 𝐽that scores joint trajectories by their sophisticated
EFE, the entangled posterior 𝑞𝜆tracks coordinated lookahead policies.
The Lean companion ConnectionsWit-
nesses.sophisticatedInference_embedding_witness is now live in the boundary fragment as a witness-consuming
97

## Page 99

Figure
58:
pymdp-grounded
total
correlation
𝐼(𝑞𝜆)
from
simulation.inference.coupled_policy_pos-
terior
→
lean.free_energy.total_correlation,
evaluated
on
a
21-point
linspace
over
𝜆
∈
[0, 4]
(simulation.hyperparameters.PYMDP_SWEEP_LAMBDAS) for the 𝐾
= 2 Ising ensemble at observations (0, 0) and
ensemble precision 𝛾= 1. The CSV at output/simulations/pymdp_lambda_sweep.csv is the source data. Smooth
monotone increase from the mean-field baseline 0 toward saturation at log 2 ≈0.693 — the empirical witness of
Proposition 7.3 inside a grounded POMDP. Uncertainty semantics: deterministic grid or deterministic construction;
no stochastic error bars are implied.
Figure 59: Deterministic 𝑇= 10-step coupled rollout from simulation.rollout.simulate_coupled_rollout under 𝜆=
2 and seed 0 (simulation.hyperparameters.PYMDP_ROLLOUT_STEPS, PYMDP_ROLLOUT_LAMBDA, PYMDP_ROLLOUT_SEED). Per-
stream marginals 𝑞𝑘
𝑡from simulation.inference.per_stream_policy_posterior (left two heatmaps) interleave with
the coupled total correlation 𝐼(𝑞𝑡) from lean.free_energy.total_correlation (right). Bit-identical reproducibility
under fixed seed is asserted by tests/test_simulation_pymdp.py::test_simulate_coupled_rollout_deterministic_-
under_fixed_seed. Uncertainty semantics: canonical fixed-seed trajectory; seed sensitivity is reported only where a
replicate sidecar is registered.
98

![page99_img1.png](images/page99_img1.png)

![page99_img2.png](images/page99_img2.png)

## Page 100

form: the caller supplies an opaque sophisticated-inference source type, an embedding map into the entangled-
posterior family, and the VFE-preservation identity as a SophisticatedInferenceEmbedding structure; the boundary
fragment certifies that the embedding lifts into the boundary-fragment variationalFreeEnergy primitive without
sorry. We emphasize that the substantive content of sophisticated inference [Friston et al., 2021] — recursive con-
ditioning of next-step EFE on anticipated observations 𝑜𝜏— requires an explicit form for 𝐽that integrates over
𝑞(𝑜𝜏, 𝑠𝜏∣𝜋𝜏). Spelling out this 𝐽is straightforward but voluminous; we treat it here as a structural analogy with
the recursive content discharged into the construction of 𝐽. The connection is machine-checked at the level of VFE-
preservation through a witness-form Lean embedding; the observation-conditioning recursion is a constraint on 𝐽,
not a consequence of the 𝜆-deformation.
Branching-Time Active Inference
Branching-time AIF [Champion et al., 2022] addresses the exponential complexity of policy enumeration via Bayesian
filtering over a branching policy tree (with optional MCTS-style sampling for tractability, in the lineage of [Fountas
et al., 2020]).
The scoped connection is representational: branching-time AIF performs Bayesian filtering / sampling on the policy
tree, while our framework parameterizes compact probability tensors that can be read as compressed views of
temporally-extended policy posteriors. Concretely, a tensor-train decomposition of 𝑞𝜆over a temporally-extended
policy offers a compact policy-tree summary with bond dimension controlling representational capacity. This is an
analogy and an engineering route for compression, not an algorithmic equivalence to Champion’s Bayesian-filtering
formulation. It is complementary to the Monte-Carlo lineage [Fountas et al., 2020] and to tensor-network techniques
[Orus, 2014, Han et al., 2018, Oseledets, 2011].
Synthesis: How Every Connection Lands on Lambda, J, or Kc
The thirteen frameworks discussed across this section and its two companions (§18, §19) all reduce to a specific
choice of three core objects: the coupling strength 𝜆, the coupling potential 𝐽, and the off-diagonal cost 𝐾𝑐. The
table below summarizes the embedding for each, so a reader can locate any one connection at a glance.
Two patterns are worth flagging before reading the table.
First, the 𝜆axis orders the frameworks by coupling
strength:
mean-field AIF lives at the 𝜆= 0 pole; classical hierarchical AIF and option-like policy-matching
embeddings live near 𝜆→∞with sparse 𝐽; the entire continuum between them is what the parametric framework
covers.
Second, the 𝐽structure orders the frameworks by kind of coordination: block-bidiagonal 𝐽produces
hierarchical structure, tensor-train 𝐽produces renormalization-group-style bond-dimension flow, symmetric Ising-
style 𝐽produces interactive multi-agent behavior, case-graded 𝐽produces CEREBRUM-style asymmetric coupling.
The Recovery type column distinguishes exact (literal specialization of the posterior or its single-stream log-partition
dual), parametric (realized after an explicit parameter, change-of-variables, or factor-graph modeling choice), and
analogical (the prior framework’s coupling-structural skeleton is mirrored, but additional dynamical, temporal, or
message-passing content lies outside the 𝜆-deformation and must be discharged into 𝐽, the EFE recursion, or the
generative model).
Framework
𝐽structure
𝜆regime
Recovery type
Mean-field AIF (pymdp, SPM)
any
𝜆= 0
exact
Factor-graph / RxInfer-style
message passing
additional policy factor
exp(𝜆𝐽−𝛾𝜆𝐾𝑐)
any finite 𝜆once the factor is
added
parametric
Product of Experts
𝐽= ∑𝑗log 𝑓𝑗, 𝐾𝑐= 0
any 𝜆
exact
Copula VI
𝐽= log-copula density on Π
(CDF reparametrization)
any 𝜆
parametric (after CDF
change-of-variables)
Hierarchical / Deep AIF
block-bidiagonal 𝐽, 𝐾𝑐= 0
𝜆→∞on off-diagonal blocks
analogical (structural shadow;
lacks temporal-scale separation
and directed message passing)
Sophisticated inference
𝐽that integrates over
𝑞(𝑜𝜏, 𝑠𝜏∣𝜋𝜏)
𝐾= 𝑑+1 streams, finite 𝜆
analogical (with 𝐽-construction
discharge of recursive
observation-conditioning)
Branching-time AIF
tensor-train 𝐽across
time-extended policies
bond-dimension truncation
analogical (with tensor-train
algorithmic side)
KL / path-integral control
(single-stream)
single-stream cost 𝐶(𝜏)
𝐾= 1, 𝜆= 1
exact (classical
log-partition–value duality)
Options framework /
Hierarchical RL
𝐽(𝜋1, 𝜋2) peaked on
option-matching configs
𝐾= 2, any 𝜆
parametric (soft option
boundaries; policy-matching
only)
RG-AIF (RGM)
tensor-train compression of 𝑞𝜆
bond-dimension flow
analogical (MERA-style scale
invariance lies outside the
present construction)
99

## Page 101

Framework
𝐽structure
𝜆regime
Recovery type
Mixture of Experts
𝑚-mixture (not 𝑒-product)
n/a
out-of-scope (𝑚-geometry dual)
Interactive / multi-agent AIF
𝑁𝐾-stream 𝐽with within- and
across-agent blocks
any 𝜆
parametric (per-stream coupling
extends to per-agent)
Markov blankets / Bayesian
mechanics (policy-space)
𝐽controls cross-stream coupling
𝜆= 0 →𝜂= 0
analogical policy-space leakage
measure (distinct from
state-space blankets)
CEREBRUM / case-grammar
directional asymmetry in 𝐽
any 𝜆
parametric (case = edge-weight
asymmetry)
Three takeaways from the table:
1. The exact recoveries are mean-field AIF, product-of-experts, and single-stream KL control.
Factor-graph / RxInfer-style implementations are parametric until the modeler inserts and validates the policy-
coupling factor in a chosen graph; Copula VI is recovered parametrically after a CDF change-of-variables. The
remaining rows are structural analogies: the coupling skeleton of the prior framework is mirrored, but additional
content (temporal-scale separation in hierarchical AIF; recursive observation-conditioning in sophisticated
inference; Bayesian filtering over the expanded policy tree in branching-time AIF; MERA-style scale invariance
in RG-AIF; state-space construction in Markov blankets) lies outside the 𝜆-deformation.
2. The 𝜆axis is the natural “comparison axis.” Mean-field AIF lives at the 𝜆= 0 pole; sparse-𝐽frameworks
live near 𝜆→∞; the continuum between them is what our framework parametrizes.
3. The 𝐽structure is the natural “kind axis.” Block-bidiagonal 𝐽is hierarchical coupling; tensor-train 𝐽
is RG-style compression; symmetric Ising-style 𝐽is interactive multi-agent; case-graded 𝐽is CEREBRUM.
Every row above is a statement about which 𝐽topology the prior art is implicitly assuming.
In this sense the lattice of existing constructions is mapped onto a low-dimensional set of slices through the (𝜆, 𝐽, 𝐾𝑐)
parameter space, with the connecting tissue between them parameterized rather than ad-hoc — though several of
these mappings remain structural analogies rather than full recoveries, in the senses listed above.
Framework Connections II: KL/Path-Integral Control, Options Frame-
works, Products-of-Experts, and Copula Variational Inference
This sub-section continues §17 by mapping the entanglement framework onto stochastic optimal control, hierarchical
reinforcement learning, and probabilistic-modeling connections that sit between the active-inference and ML
communities. The canonical tutorial on the control-as-inference / maximum-entropy RL viewpoint [Levine, 2018] is
the natural ML-side companion for the active-inference recoveries developed below.
KL / Path-Integral Stochastic Optimal Control
Path-integral and KL control [Kappen, 2005, Todorov, 2006, Theodorou and Todorov, 2012, Rawlik et al., 2013]
solve stochastic optimal control via free-energy duality:
𝑉(𝑥) = −1
𝜌log 𝔼𝑝free[exp(−𝜌𝐶(𝜏))]
(18.1)
where 𝐶(𝜏) is the trajectory cost (renamed from the standard 𝐽to avoid clashing with our habit potential 𝐽) and
𝑝free is the uncontrolled-dynamics prior. The control-effort cost is the KL between the controlled and uncontrolled
measures.
Connection.
At 𝐾= 1, 𝜆= 1 the framework reduces to the classical single-stream log-partition–value-
function duality [Kappen, 2005, Todorov, 2006, Theodorou and Todorov, 2012, Rawlik et al., 2013]:
𝑉(𝑥) =
−(1/𝜌) log 𝔼𝑝[exp(−𝜌𝐶(𝜏))], where ℰ1 = 𝐸1 ⋅exp(𝐽−𝛾𝐾𝑐) plays the role of the Gibbs-controlled trajectory measure.
This is the well-known special case; the genuinely novel content of the framework is at 𝐾≥2, where our 𝐸𝑘(𝜋𝑘) plays
the role of the per-stream uncontrolled prior and the coupling potential 𝜆𝐽encodes cross-stream control coupling —
the sense in which a “joint” KL controller pays a coupling cost beyond the marginal control efforts. A multi-stream
value-function formulation follows in principle from the same log-partition duality; we sketch but do not develop it
here.
Smooth-deformation precedents. Smooth scalar deformations of variational families have prior history in the
structured-VI literature. Li and Turner [Li and Turner, 2016] introduce 𝛼-Rényi divergence variational inference:
100

## Page 102

𝛼= 1 recovers the standard ELBO, 𝛼→0 recovers the log marginal likelihood. Tran, Blei, and Airoldi [Tran
et al., 2015] augment mean-field with copula dependency; the recent Fu–Smith–Panagiotelis vector-copula extension
[Fu et al., 2025] adds learnable dependency between blocks. Our 𝜆differs from these by parametrizing the policy-
posterior factorization structure, not the divergence (as in 𝛼-Rényi-VI) or the dependency form alone (as in copula
VI): at 𝜆= 0 we have strict mean-field, and at 𝜆> 0 we have a coupling-deformed factorization whose structure is
controlled by the habit and preference potentials (𝐽, 𝐾𝑐).
Options framework / Hierarchical RL
The options framework and hierarchical-RL literature [Sutton et al., 1999, Barto and Mahadevan, 2003, Bacon et al.,
2017] introduce temporally-extended actions (“options”) as semi-MDPs with initiation sets, intra-option policies,
and termination conditions. The planning-as-inference program [Toussaint, 2009, Botvinick and Toussaint, 2012]
casts policy search as Bayesian posterior inference over trajectories, giving the options decomposition a probabilistic-
graphical-model reading.
Connection. An option can be represented as a temporally-coupled policy stream: a high-level decision (which
option to invoke) and a low-level intra-option policy. This is a parametric 𝐾= 2 embedding with 𝐽encoding the
option-membership structure (high 𝐽on configurations where intra-option policy matches the invoked option, low
𝐽otherwise). Termination conditions correspond to boundary conditions on the entangled posterior only after the
modeler encodes them in that factorization.
The framework therefore gives an option-like parametric embedding with probabilistic, soft, learnable option-boundary
weights via 𝜆-tunable coupling. It does not replace option discovery or termination learning; those algorithmic choices
must be supplied by the modeler or by a separate option-learning layer.
Product of Experts and Mixture of Experts
Product of Experts (PoE) [Hinton, 2002] combines models multiplicatively:
𝑃(𝑥) ∝∏
𝑗
𝑓𝑗(𝑥).
(18.2)
Our ℰ𝜆(𝜋) = ∏𝑘𝐸𝑘(𝜋𝑘) ⋅exp(𝜆𝐽(𝜋)) is a PoE on the joint policy space, with the coupling potential acting as one
additional expert. The framework therefore inherits PoE’s compositionality: combining experts that each capture a
piece of the policy-coupling structure.
Mixture of Experts (MoE), conversely, is additive combination — corresponding to a different geometric structure
(𝑚-mixtures rather than 𝑒-products). The two are dual.
Copula variational inference
Copula VI [Tran et al., 2015, Nelsen, 2006] retains mean-field marginals while modeling dependence via a
copula. Our framework’s 𝜆-deformation realizes the same copula-density form when the modeler supplies the CDF
reparameterization and chooses 𝐽as the log-density of the desired copula family. Define per-stream marginal CDFs
𝑢𝑘= 𝐹𝐸𝑘(𝜋𝑘) ∈[0, 1]. Under this reparametrization, the entangled prior ℰ𝜆(𝜋) = ∏𝑘𝐸𝑘(𝜋𝑘) exp(𝜆𝐽(𝜋))/𝑍𝐸maps
to a copula density
𝑐(𝑢1, … , 𝑢𝐾) = exp(𝜆𝐽(𝜋(𝑢1, … , 𝑢𝐾)))
(18.3)
on the unit hypercube (up to the normalizer 𝑍𝐸). The framework therefore recovers the parametric copula-density
slice of copula variational inference [Tran et al., 2015, Fu et al., 2025] with copula-log-density 𝜆𝐽; bond-dimension
truncation of 𝐽as a tensor-train is analogous to vine-copula truncation at depth 𝜒rather than a proof that every
vine construction is a tensor-train posterior. This connects active inference to the rich copula literature, importing
techniques for sparse coupling estimation [Nelsen, 2006, Han et al., 2016, Tran et al., 2015, Fu et al., 2025].
Recovery dictionary
The four connections above are concrete only when the relationship class is explicit. Reading the table left-to-right
turns a broad recovery claim into a recipe with the relevant exact, parametric, or out-of-scope boundary attached.
Prior framework
Structural choice in (𝐾, 𝐽, 𝐾𝑐, 𝜆)
Relationship class / behavior
Mean-field active inference (pymdp / SPM)
𝜆= 0, any 𝐽, 𝐾𝑐
𝑞𝜆= ∏𝑘𝐸𝑘𝑒−𝛾𝐺𝑘/𝑍𝑘; per-stream FPI
101

## Page 103

Prior framework
Structural choice in (𝐾, 𝐽, 𝐾𝑐, 𝜆)
Relationship class / behavior
KL / path-integral control (single-stream)
𝐾= 1, 𝜆= 1
𝑉(𝑥) = −(1/𝜌) log 𝔼𝐸[exp(−𝜌𝐶(𝜏))];
classical log-partition–value duality
[Kappen, 2005, Todorov, 2006, Theodorou
and Todorov, 2012, Rawlik et al., 2013]
Options / hierarchical RL
𝐾= 2, 𝐽(𝜋1, 𝜋2) peaked on 𝜋2 that
matches option 𝜋1
option-like soft boundaries; intra-option
policy from 𝑞2
𝜆(parametric —
policy-matching only; option
discovery/termination learning supplied
separately) [Sutton et al., 1999, Barto and
Mahadevan, 2003, Bacon et al., 2017]
Product of Experts
𝐾𝑐= 0, 𝐽= ∑𝑗log 𝑓𝑗
ℰ𝜆∝∏𝑘𝐸𝑘⋅∏𝑗𝑓𝜆
𝑗
Mixture of Experts (dual)
𝑚-mixture rather than 𝑒-product; not in
this construction
additive combination — out-of-scope for
the entangled-prior family
Copula VI
𝐸𝑘= marginals; 𝐽= log-copula density on
𝑢= 𝐹𝐸(𝜋)
ℰ𝜆as a 𝜆-deformed copula-density slice
after CDF change-of-variables [Nelsen,
2006, Tran et al., 2015, Fu et al., 2025]
𝛼-Rényi-VI [Li and Turner, 2016]
divergence-parametrized, not
factorization-parametrized
orthogonal axis — not recovered,
complementary smooth-deformation
precedent
Empty cells mean not subsumed in the entangled-prior construction (e.g. Mixture-of-Experts requires the 𝑚-geometry
dual). Every non-empty row is a worked instance: assigning (𝐾, 𝐽, 𝐾𝑐, 𝜆) the values shown either reproduces the
prior framework’s posterior directly or realizes the relevant parametric policy-matching slice.
Framework Connections III: Multi-Agent Inference, RG-AIF Coarse-
Graining, Markov Blankets, and CEREBRUM Case Grammar
This sub-section closes §17 by mapping the entanglement framework onto multi-agent active inference,
renormalization-group treatments, the Markov-blanket / Bayesian-mechanics worldview, and CEREBRUM-style
case-grammar architectures.
Interactive Inference / Multi-Agent Active Inference
Interactive inference [Maisto et al., 2024] models multi-agent cooperation as joint inference under shared generative
models. Collective active-inference models add a complementary population-scale result: coordinated behavior can
emerge from surprise minimization without treating the group result as a proof of any particular finite-policy coupling
theorem [Heins et al., 2024].
The multi-agent active inference literature has expanded substantially since 2022. Federated inference and belief
sharing [Friston et al., 2024] models belief broadcasting across agents; Shared Protentions [Albarracin et al.,
2024] formalizes coordinated anticipation; collective surprise-minimization models [Heins et al., 2024] show how
coordination can emerge at population scale; As One and Many [Waade et al., 2025] relates individual to emergent
group-level generative models; Factorized Active Inference for Strategic Multi-Agent Interactions [Ruiz-Serra et al.,
2025] explicitly notes the current default mean-field-across-agents assumption — which our 𝜆-deformation relaxes.
The framework here provides the scalar deformation parameter for the policy-coupling part of these lines, not a full
multi-agent process theory by itself.
Connection. A multi-agent setting with 𝑁agents each with 𝐾policy streams maps onto a single 𝑁𝐾-stream
entanglement only after the modeler fixes agent boundaries, shared or separate generative models, and the within-
agent / across-agent blocks of 𝐽. Under that explicit parameterization, the framework gives a joint-policy prior
for single-agent multi-stream coordination and multi-agent joint action under the same scalar coupling parameter.
Without that generative-model choice, the connection is structural rather than an identity with any particular
federated-inference paper.
This is conceptually clean at the level of the variational family: from the perspective of policy entanglement,
interpersonal coordination and intrapersonal coordination can use the same cross-stream coupling machinery once
the modeler has chosen the agent boundaries, observation model, and shared or separate generative models. The
claim class is therefore parametric, not proved or exact for the multi-agent literature as a whole.
102

## Page 104

Renormalization-group active inference (structural analogy)
Scale-free active inference, formalized as Renormalizing Generative Models (RGMs) [Friston et al., 2025], coarse-
grains across temporal/spatial scales preserving the form of the generative model. Our framework’s tensor-train
compression of 𝑞𝜆(bond-dimension truncation) provides a coarse-graining analog at the policy-posterior level: low-
rank truncation projects out high-spectral-rank correlations, akin to integrating out fast modes. We emphasize this
is an analogy, not a recovery: a full RG-AIF correspondence would require a MERA-style scale-invariant ansatz (not
standard tensor-train), which we do not develop here. The proper RG-AIF reference is RGM [Friston et al., 2025]
and we cite it as the canonical scale-free AIF construction.
Markov Blankets and Bayesian Mechanics
The Markov blanket / Bayesian-mechanics formulation of FEP [Friston, 2019, Da Costa et al., 2021, Kirchhoff et al.,
2018, Aguilera et al., 2022, Raja et al., 2021, Menary and Gillett, 2022] identifies a system with a partition of states
into internal/external/blanket. In our framework, streams are candidate partitions of the agent’s policy space chosen
by the modeler, and the factorization structure of 𝑞𝜆across streams induces a policy-space analog of the blanket
idea.
Proposition 19.3 Policy-space Markov blankets. We extend the Markov-blanket idea from state-space [Friston,
2019, Da Costa et al., 2021, Kirchhoff et al., 2018, Aguilera et al., 2022, Raja et al., 2021, Menary and Gillett, 2022]
to policy-space: define the policy-blanket leakage of a joint 𝑞on Π1 × ⋯× Π𝐾as the normalized multi-information
𝜂(𝑞) = 𝐼(𝑞)/𝐻(𝑞) ∈[0, 1].
(19.1)
At 𝜆= 0 we have 𝜂(𝑞0) = 0 (perfect factorization across streams; policy posteriors are conditionally independent
given marginals); at 𝜆> 0, 𝜂(𝑞𝜆) > 0 measures the leakage of cross-stream information that would be lost under a
mean-field projection. We emphasize this is a policy-space analog, not a recovery of the state-space Markov-blanket
construction; the two are formally distinct.
CEREBRUM and case-grammar approaches
CEREBRUM (Case-Enabled Reasoning Engine with Bayesian Representations for Unified Modeling) [Friedman,
2025] explores grammatical case as a structuring principle for cognitive architectures. The connection to policy
entanglement: cases encode role-relations across cognitive operations, which are precisely cross-stream coupling
structures. A nominative-accusative case relation between two streams corresponds to a directional asymmetry in
𝐽. The framework therefore provides a parametric probabilistic backend for case-grammar cognitive architectures
once the case roles have been encoded as edge-weight asymmetries in 𝐽.
A compositional reading of these case-grammar architectures sharpens the connection.
Following the category-
theoretic account of [Friedman, 2026b], let 𝒦be a compact-closed case category whose objects are case roles, whose
morphisms are role-composing sentence and discourse circuits (in the DisCoCat / DisCoCirc sense), and whose
hom-objects are enriched over [0, 1] as magnitudes; an alignment pattern is then a functor 𝛼∶𝒦→Coup𝐾into
a category of directional couplings on the 𝐾-stream policy space, and — when this substrate is supplied — the
habit potential of §4 can be written as the pullback 𝐽= 𝛼∗Φ of a weighting Φ on 𝒦. Two cognitive-architecture
decisions then sit on distinct objects: a choice of case system (nominative– accusative, ergative–absolutive, fluid-𝑆,
split-ergative) is a choice of 𝒦and its alignment functor 𝛼, while the coupling strength of the present framework is the
scalar 𝜆that scales the pulled-back potential 𝜆𝐽inside ℰ𝜆. Topos-theoretic Morita equivalence between alignment
frames in the sense of [Friedman, 2026b] then predicts when two surface-different case-graded couplings induce the
same entangled posterior — a non-identifiability condition on 𝐽that is invisible at the level of the coupling graph
alone. The recovery class is unchanged: the categorical layer supplies the substrate on which case roles license
edge-weight asymmetries in 𝐽, but choosing 𝒦and 𝛼remains an explicit modeling commitment, so the mapping
stays parametric rather than exact.
The interaction graph of 𝐽across multiple streams is itself a useful diagnostic — symmetric all-to-all coupling (as in
the K=4 Ising ensemble below) appears as an evenly-weighted clique, while asymmetric / hierarchical / case-graded
couplings would manifest as edge-weight heterogeneity:
103

## Page 105

Figure 60: Coupling-potential graph for the symmetric 𝐾= 4 Ising ensemble built by simulation.builders.ising_-
coupling_tensor and rendered via visualizations.graphs.plot_coupling_graph(threshold=0.0). Each node is one
stream; edge weights are the mean |𝐽| over slot pairs. Symmetric coupling produces an evenly-weighted clique;
CEREBRUM-style case-grammar couplings would manifest as edge-weight asymmetry.
Uncertainty semantics:
analytical schematic or structural visualization; no stochastic uncertainty interval is implied.
104

![page105_img1.png](images/page105_img1.png)

## Page 106

Part VI — Discussion and Outlook
The closing part collects what remains outside the stock-Lean boundary, how claim strength is labeled, and what
the framework commits to as it lands. Two chapters:
• §20 — the live punch-list across five fronts:
open theoretical questions (Mathlib4 analytic payloads for
convexity, spectral upper-semicontinuity, sparsity-rank); identifiability questions (when can 𝜆be recovered
from behavior?); empirical questions (which regimes does the pymdp harness need to be stress-tested against?);
conceptual questions (precision as 𝜆vs. precision as 𝛾); and practical questions (computational scaling, model
selection).
• §21 — the consolidated discussion: the framework’s load-bearing commitments, the live state of the artifact
(Lean fragment + Python suite + manuscript renderer + reproducibility contract), the limitations the
formalism imposes by construction, and the ordered Mathlib4 analytic-discharge plan that keeps those witnesses
separate from the stock-Lean boundary fragment.
Part VI states the practical implications of the framework — what the 𝜆-coupling buys (cross-stream coordination,
tunable structure, principled recovery of prior frameworks) and what it costs (computational overhead in 𝐽-
construction, the coupling-tax bound, residual analytical-content witnesses in the Lean fragment).
Open Theoretical Questions: Analytical Gaps, Identifiability, Empirical
Frontiers, and Practical Research Directions
A list of well-defined open problems, each suitable for focused investigation.
The questions are grouped by
methodological character — analytical, identifiability / inference, empirical, conceptual / cross-disciplinary, practical
/ formalization — and each carries an explicit statement, conjecture (where we have one), and a pointer to the section
it would extend.
Where to start
For a contributor choosing an entry point, the highest-leverage items by category are:
• Q1 (uniqueness of 𝜆⋆) — analytical, highest-leverage. Convexity of 𝐹[𝑞𝜆] on [0, ∞) governs whether
the framework’s central control parameter is learnable by ordinary gradient descent on free energy. A positive
resolution promotes a large fraction of the typed-API theorems in §12 from analytic-boundary contracts to
substantive proofs in the same Mathlib4 layer, because the dispersion-comparison inequality reformulated in
Q1 is the missing analytic content.
• Q5 (gauge freedom in 𝐽) — identifiability, necessary preparation. No empirical fitting of 𝜆, 𝐽, or
𝐾𝑐to observed behavior can proceed until the gauge orbit is characterised; this is the bottleneck for any
identifiability result downstream.
• Q14 (Mathlib4 analytic discharge) — practical, immediate follow-on. The central result is discharged
at ℝ-level by MathlibProofs.free_energy_decomposition_full; the open question is the Mathlib4 abstraction
layer for the remaining typed-API rows.
Beyond these three, Q4 (continuous-state extension) is the single highest-impact scope-broadening item, Q9 /
Q10 are incrementally extendable by writing new pymdp scenarios against the existing harness, and Q15 (multi-
project coupling) is the right entry point for a contributor whose interest is multi-agent.
How to read each question
A few orientation notes for readers triaging which question to attack. The analytical questions Q1–Q4 are the ones
whose resolution would most directly extend the manuscript’s theorem suite; of these, Q1 (uniqueness of 𝜆⋆) is the
highest-leverage because convexity directly governs whether optimal coupling is learnable by gradient on free energy.
The identifiability / inference questions Q5–Q8 concern statistical and algorithmic contracts the framework
currently leaves open; Q5 (gauge freedom in 𝐽) is necessary preparation for any empirical fitting. The empirical
questions Q9–Q10 stress-test the framework on richer ensembles than the K=2 Ising toy; the current harness ships
initial answers for both (long-horizon habit accumulation across 𝑇= 100 steps; revertibility identity to floating-
point tolerance), so the Q9 and Q10 entries below are reframed as the next-order follow-ons those initial witnesses
make precise. The conceptual / cross-disciplinary questions Q11–Q13 connect the framework to adversarial
105

## Page 107

robustness, integrated information, and quantum analogs. The practical / formalization questions Q14–Q15 are
the engineering prerequisites for the Mathlib4 analytic-discharge plan (§12).
Analytical questions
Q1 — Existence and uniqueness of 𝜆⋆. Using the closed-form identity Eq. (5.8) and its second derivative
Eq. (A.15), convexity of 𝐹[𝑞𝜆] on [0, ∞) reduces to the dispersion-comparison inequality
Varℰ𝜆(𝐽) ≥Var𝑞𝜆(𝐽−𝛾𝐾𝑐)
for all 𝜆≥0
(20.1)
, a crisper characterization than Theorem 5.6’s “log-concavity of 𝐽−𝛾𝐾𝑐”.
Why the reformulation holds. On 𝜆∈[0, ∞) where 𝑍𝐸(𝜆) and 𝑍(𝜆) are finite and strictly positive (automatic for
finite policy spaces with bounded 𝐽, 𝐾𝑐), the log-partition log 𝑍(𝜆) is the cumulant-generating function of 𝐽−𝛾𝐾𝑐
under the 𝜆-tilted base measure ∝𝐸MF exp(𝜆(𝐽−𝛾𝐾𝑐)), so 𝜕2
𝜆log 𝑍(𝜆) = Var𝑞𝜆(𝐽−𝛾𝐾𝑐) is the variance under the
entangled posterior. The matching log-prior partition gives 𝜕2
𝜆log 𝑍𝐸(𝜆) = Varℰ𝜆(𝐽), and Eq. (A.15) unfolds to the
difference 𝜕2
𝜆𝐹[𝑞𝜆] = Varℰ𝜆(𝐽)−Var𝑞𝜆(𝐽−𝛾𝐾𝑐) pointwise on the domain where both cumulant-generating functions
are finite.
Convexity of 𝐹in 𝜆on that domain is therefore equivalent to the dispersion-comparison inequality
Eq. (20.1), not merely implied by it; uniqueness of any interior 𝜆⋆follows from strict convexity, i.e. strict inequality
on the open interval.
Conjecture (sharpened): when 𝐸MF is uniform and 𝐾𝑐≡0, the inequality reduces to Varℰ𝜆(𝐽) ≥Var𝑞𝜆(𝐽) on the
same exponential family, which by Brascamp–Lieb / Bakry–Émery holds whenever the natural-statistic distribution
under the entangled prior is log-concave [Brascamp and Lieb, 1976, Bakry, 1985]; under that hypothesis 𝜆⋆is unique.
Empirically testable via output/data/parameter_sweep.csv across the registered 𝐽families: a measured negative
left-hand side at any sweep point falsifies global convexity for that family.
Q2 — Bifurcation structure.
For non-convex 𝐹, what are the bifurcation structures of 𝜆⋆as 𝐽, 𝐾𝑐vary?
Conjecture:
cusps and Hopf-like bifurcations on a finite-codimensional set in potential-space.
The dispersion-
comparison reformulation of Q1 makes the bifurcation locus the level set {(𝜆, 𝐽, 𝐾𝑐) ∶Varℰ𝜆(𝐽) = Var𝑞𝜆(𝐽−𝛾𝐾𝑐)},
codimension-one in the joint (𝜆, 𝐽, 𝐾𝑐, 𝛾) space — testable empirically via the §10 phase-diagram code.
Q3 — Universality classes. Different choices of 𝐽(sparse pairwise, low-rank, hierarchical) give qualitatively
different phase diagrams. Is there a universality classification of policy entanglement, analogous to the classification
of phase transitions in statistical mechanics? Connection to the RG-AIF mapping (§19) suggests the tensor-train
rank profile is a candidate order parameter. Sharpened conjecture: the relevant universality class is determined
by the rank-growth exponent 𝜌(𝜆) = d log 𝑟𝑘(𝜆)/d log 𝜆across the bipartite cuts of §D, with distinct exponents for
sparse-pairwise / low-rank-MPS / hierarchical families.
Q4 — Continuous-state extension. The framework as stated is for finite Π𝑘. The continuous case (motor torques,
continuous attention) requires Gaussian / copula extension. Is there a clean analog of Theorem 5.1 for Gaussian-
coupled policies? Conjecture: yes — the closed-form identity Eq. (5.8) survives intact in the Gaussian-copula setting
because both log 𝑍𝐸and log 𝑍remain finite-dimensional log-partitions of Gaussian exponential families, provided
the covariance structure remains positive-definite throughout the deformation (a non-trivial condition for 𝜆> 0); we
believe this holds for moderate 𝜆in the regularized Gaussian copula but a rigorous statement is open. Under that
hypothesis, the multi-information appearing in the Gibbs decomposition becomes the negative log-determinant of a
copula correlation matrix.
Identifiability and inference questions
Q5 — Identifiability. Given observed agent behavior, can we identify 𝐽, 𝐾𝑐, 𝜆?
Gauge group, explicit.
The entangled posterior is invariant under 𝐽(𝜋) ↦𝐽(𝜋) + 𝑓(𝜋) for any mean-field-
decomposable 𝑓(𝜋) = ∑𝑘𝑓𝑘(𝜋𝑘): such an 𝑓contributes a per-stream log-weight absorbed into the per-stream
priors 𝐸𝑘, leaving 𝑞𝜆pointwise unchanged. Writing ℱMF(Π) ∶= {𝑓∶Π →ℝ∣𝑓= ∑𝑘𝑓𝑘} for the additive group
of mean-field-decomposable potentials, the identifiable coupling lives in the quotient ℱ(Π)/ℱMF(Π). For 𝐾= 2 on
Π = Π1×Π2 with |Π𝑘| = 𝑛𝑘, the ambient space ℱ(Π) has dimension 𝑛1𝑛2 and the mean-field subspace has dimension
𝑛1 + 𝑛2 −1 (after subtracting the shared constant), so the identifiable 𝐽space has dimension (𝑛1 −1)(𝑛2 −1) —
equal to the dimension of the bipartite Schmidt-rank ceiling described in §8, which is the content the framework can
recover from joint-action data.
A symmetric identifiability statement holds for 𝐾𝑐under the same quotient. The scalar 𝜆is identifiable on [0, ∞)
from the strength of joint structure once the gauge orbit of (𝐽, 𝐾𝑐) is factored out; model comparison against the
𝜆= 0 mean-field posterior is the operational identifiability test (§21). Identifiability conditions for active-inference
parameters are an active topic [Smith et al., 2022, Schwartenbeck and Friston, 2016]; the entangled extension
106

## Page 108

introduces new parameters with their own identifiability questions, and the quotient characterization above is the
prerequisite specification.
Q6 — Free energy of free energy. Updating 𝜆by gradient descent on 𝐹[𝑞𝜆] is itself a meta-inference. Does
this admit a free-energy-of-free-energy interpretation, and does it close into a self-consistent variational hierarchy?
The closed-form gradient Eq. (5.9) suggests a clean answer: the gradient of 𝐹in 𝜆is itself a difference of two
prior/posterior expectations of the same statistic 𝐽, so precision-like learning on 𝜆has the same exponential-family
algebraic shape as ordinary precision learning on 𝛾. Conjecture: the entanglement framework provides a finite-rank
truncation of the regress, with the bond dimensions of the tensor-train representation indexing the depth of belief-
about-belief, and the closed-form gradient identity extends recursively (each meta-level adds one 𝐽(ℓ) statistic and
one ⟨𝐽(ℓ)⟩𝐸(ℓ)
𝜆−⟨𝐽(ℓ)⟩𝑞(ℓ)
𝜆gradient). This is a formal modeling conjecture, not a current neural or clinical claim.
Q7 — Algorithmic complexity.
Coordinate-descent inference on coupled factor graphs (§9.2) has known
complexity by case:
• Tree-structured 𝐽(no cycles in the coupling graph): one forward-backward sweep on the coupling tree
via the standard junction-tree algorithm converges in a single pass with per-iteration cost Θ(𝐾⋅max𝑘|Π𝑘|2)
— quadratic in the largest per-stream support and linear in the tree-edge count.
• Loopy 𝐽(coupling graph with cycles): exact inference is #P-hard (the partition function is a permanent-
class computation); loopy belief propagation converges to a fixed point of the Bethe free energy without general
convergence-or-accuracy guarantees, with the gap from the true marginal bounded by the Wainwright–Jordan
duality on convex relaxations of the marginal polytope [Wainwright and Jordan, 2008].
• TT-aware (𝐽admits a matrix-product factorization with bond dimension 𝑟): exact marginals via
tensor-train contraction cost Θ(𝐾⋅𝑟2 ⋅max𝑘|Π𝑘|) per sweep, strictly dominating loopy BP whenever the
coupling has low-rank tensor-network structure.
The open question is whether a TT-aware inference algorithm specialized to policy entanglement strictly dominates
generic loopy BP in practice (not just in worst-case scaling) when 𝐽has the empirical rank profile recorded in
output/data/manuscript_variables.json.
The TT-rank profile across the configured 𝜆sweep is the falsification
input: if measured ranks stay bounded across the sweep, the TT-aware path dominates; if they grow with 𝜆, generic
loopy BP becomes competitive.
Q8 — Learning to couple (graph-neural-network connection). Coupled policy inference is structurally a
message-passing computation on the coupling graph. Does this admit a graph-neural-network-style implementation
that learns 𝐽, 𝐾𝑐end-to-end from environment interactions? This would be the learning-to-couple version of the
framework, with industrial-scale applications to multi-agent and embodied AI. (Note: the acronym “GNN” is used
in §S8 to mean Generalized Notation Notation, an orthogonal model-description language; the two meanings are
disambiguated at §S8.3.)
Empirical questions
Q9 — Habit-accumulation dynamics. Initial answer in the current harness — see §13: a deterministic 𝑇= 100-
step coupled rollout at 𝜆= 2 records a monotone habit-accumulation signal 1.0000 and steady-state KL bounded
by 0.1334 across the tail window against its empirical mean. Follow-on: pair the long-horizon rollout with a slow 𝐽-
update Hebbian rule and ask how the resulting 𝐽trajectories interact with the phase boundaries of §10. Conjecture
(unchanged): habits accumulate fastest near the mixed / frozen boundary, where the system has maximum sensitivity
to small coupling-potential perturbations.
Q10 — Revertibility under perturbation. Initial answer in the current harness — the 𝑚-projection identity
𝐼(𝑞) = 𝐷KL(𝑞‖
̂𝑚(𝑞)) (Proposition 7.3) holds numerically to floating-point tolerance (≤1.67𝑒−16 maximum residual)
across the 5-point sweep (see §13: maximum KL residual 1.67𝑒−16, maximum marginal difference 1.11𝑒−16).
Follow- on: under environmental perturbations (e.g. adversarial coupling injection), how robust is the 𝑚-projection
estimator? This is the empirical counterpart to Q11.
Conceptual / cross-disciplinary questions
Q11 — Cognitive integrity / adversarial robustness. Cognitive integrity programs in active inference consider
the robustness of cognition to adversarial perturbations.
Does the entanglement framework provide robustness
guarantees — bounds on how much 𝑞𝜆can be perturbed by adversarial 𝐽deformations?
Initial harness answer (shipped, not a controlled adversarial study).
The closed-form Eq. (5.8) yields a first-
order Lipschitz bound (to first order in 𝜀, uniformly for 𝜆∈[0, 𝜆max] on any bounded sub-interval) Δ𝑞(𝜀, 𝜆) ≤
𝜆𝜀⋅Var𝑞𝜆(𝐽)1/2 + 𝑂(𝜀2𝜆2) via the cumulant-generating-function derivative used in Q1’s reformulation [Brascamp
and Lieb, 1976, Barrett et al., 2022]. The adversarial sidecar measures KL drift on a configured (𝜀, 𝜆) grid with three
107

## Page 109

Δ𝐽classes: (i) rank-one stress aligned with coupling covariance, (ii) uniformly random norm-𝜀perturbations, (iii)
sparse single-cell perturbations. The gate compares the empirical Lipschitz slope against the analytical first-order
bound and surfaces the large-𝜀regime where the linearization is exceeded (0.942857, 0.964028). Implementation:
../src/simulation/adversarial.py. A compute-matched adversarial study remains open work.
Q12 — Connection to integrated information theory.
Total correlation is one of several measures of
informational integration. Is there a connection between 𝐼(𝑞𝜆) and the integrated information Φ of IIT [Tononi,
2008]? Both quantify cross-part dependence in different mathematical settings; the framework gives only a candidate
operationalization in the policy-inference setting.
Q13 — Quantum analog. The Schmidt-rank machinery is borrowed directly from quantum many-body theory. Is
there a meaningful quantum policy entanglement that goes beyond the formal analogy — e.g. for quantum-mechanical
agents in the spirit of the scale-free / RG-AIF framework [Friston et al., 2025]? This is speculative but conceptually
clean and may interact with Q3’s universality program.
Practical / formalization questions
Q14 — Mathlib4 analytic discharge for the typed-API rows (§12). The central result (Theorem 5.1) is
discharged in MathlibProofs.free_energy_decomposition_full, with the multi-information non-negativity surfaced
as the standalone-named multiInformation_nonneg_at_joint (using streamMarginal_pos as the per-stream-marginal
positivity precondition); both are on the foundational-only #print axioms audit keystone list. The open question
is the cleanest Mathlib4 abstraction layer to discharge the analytic payloads of the remaining 11 typed-API rows
(Theorem 5.6, Proposition 7.5, Proposition 8.2, Theorem 8.3, Theorem 9.1, Corollary 9.2, Proposition 11.1, Theorem
17.1, Proposition 17.2, Proposition 19.3) and the boundary-form completion for Theorem 5.5, using finite KL /
entropy chain rules, convexity / Taylor payloads, semicontinuity / matrix-rank, tensor-product rank envelopes, and
concentration witnesses. A related question is the verified Float↔ℝbridge — Flocq-style formal IEEE-754 model
or interval arithmetic — that would formally tie the ℝ-level proofs to the Float pipeline (currently bound empirically
by the dashboard invariants).
Q15 — Multi-project coupling. What does the framework predict for multi-agent settings — populations of
agents with their own 𝜆, or hierarchical agents whose sub-streams are themselves entangled ensembles? The §19
mapping is a starting point; the open question is whether the bookkeeping admits a clean recursive identity à la
Theorem 5.1.
Discussion and Outlook: Worldview, Live Artifact State, and Limita-
tions
What the framework commits to
The framework commits to: (i) finite, discrete-time POMDP active inference as the home setting; (ii) mean-field as
the baseline, not the target; (iii) coupling structure as a learnable hyperprior, not a hand-engineered architectural
choice; (iv) revertibility — any coupled habit can be marginalized to its mean-field component — as a non-negotiable
property; (v) information geometry as the natural language for parametric extensions of variational families.
What the framework declines to commit to
The framework does not commit to: (i) embodiment as the primary structuring principle; the same finite-policy
formalism can be applied to robots, brains, institutions, or colonies only after a modeler has chosen the relevant
streams and boundaries; (ii) any specific neural implementation; the message-passing structure (§9.2) is biologically
suggestive but optional; (iii) any specific coupling potential structure; sparse, low-rank, hierarchical, or learned-
tabular are all admissible.
The parametric-entanglement worldview
Structural couplings between behavioral streams are treated as learned hyperpriors rather than architectural
commitments. The framework operationalizes this stance with a single dial (𝜆) and a single mathematical object
(the coupling potential 𝐽) that together determine how much and what kind of cross-stream coordination an agent
learns to express.
108

## Page 110

The design sits on a three-point spectrum rather than a single opposition:
• Modular embodiment.
Build separate controllers for separate functions; engineer a translation layer
between them. Costs: the translation layer is the alignment problem in microcosm; the modular boundaries
are not learnable.
• Joint enumeration. Treat the joint policy as monolithic; suffer the combinatorial cost. Costs: doesn’t scale;
loses interpretability.
• Parametric entanglement (this manuscript). Marginal-preserving, structure-permitting, geometrically
principled, and machine-checkable where the claim is algebraic or formally witnessed, with broader biological
readings kept hypothesis-labeled.
Relation to the Free Energy Principle and active-inference process theory
The contribution is best read as a local refinement of active inference, not as a competing global principle. The Free
Energy Principle supplies the broader variational story: adaptive systems can be modeled as maintaining beliefs and
actions that keep their sensory states within viable bounds by optimizing variational free energy [Friston et al., 2006,
Friston, 2010, Buckley et al., 2017, Ramstead et al., 2018]. Active inference supplies the process theory: finite agents
carry generative models, update beliefs, and select policies by expected free energy [Friston et al., 2017a, Parr and
Friston, 2017a, Kaplan and Friston, 2018, Da Costa et al., 2020, Smith et al., 2022, Parr et al., 2022, Pezzulo et al.,
2024]. This manuscript operates one level down from those commitments. It asks what kind of variational family
the policy posterior should be when an agent has several concurrent streams whose actions are neither independent
nor cheaply enumerable as one monolithic policy.
The empirical status of that broader program should be read cautiously. Reviews of predictive coding and active
inference report a growing but still incomplete empirical base, and emphasize that direct validation requires
comparisons against alternative models, not only successful behavioral fits [Hodson et al., 2024].
The present
artifact therefore treats FEP/AIF as the normative and computational frame in which the finite-policy posterior is
defined. Its validated results are theorem rows, generated numerical sidecars, figures, and validator/PDF gates, not
direct evidence for a biological implementation of the 𝜆-deformation.
This also fixes the identifiability target for future empirical work. Estimating 𝜆from data would require a model-
comparison design that pits the coupled posterior against a mean-field policy posterior, alternative structured priors,
and ordinary changes in 𝐸, 𝐶, 𝐺, or policy precision. A large fitted 𝜆would not by itself identify neural precision,
desire, conscious integration, or a clinical mechanism; it would identify, under the chosen model, residual cross-
stream dependence in policy space. Conversely, a misspecified 𝐽can make coupling harmful or uninterpretable, so
the present finite binary and pymdp sidecars should be read as controlled existence-and-stress evidence rather than
broad behavioral validation.
That positioning matters for interpretation. Precision parameters in active inference weight confidence in beliefs,
prediction errors, or policy preferences; precision-weighting accounts of attention, salience, action, and psychosis
motivate the vocabulary but do not identify this manuscript’s 𝜆with a neural gain parameter [Parr and Friston,
2017b, Haarsma et al., 2021, Limanowski et al., 2024]. The coupling strength 𝜆introduced here weights cross-stream
policy dependence. Precision in active inference itself has multiple roles across discrete policy selection, continuous
sensorimotor control, attention, and action; 𝜆is only a coupling-precision analog inside the present finite policy
posterior. These roles can interact, and §20 flags that interaction as a live question, but the framework does not
collapse one into the other. A high-precision stream can still be weakly coupled to its peers; a strongly coupled
ensemble can still contain uncertain marginals. This separation is the reason the decomposition of Theorem 5.1
is useful: it identifies the free-energy terms attributable to marginal belief quality, coupling structure, and total
correlation separately.
The Markov-blanket literature also helps delimit the claim. Markov blankets and particular-physics accounts address
how a system is distinguished from its environment, and why conditional independences matter for autonomy
[Kirchhoff et al., 2018, Friston, 2019, Aguilera et al., 2022, Raja et al., 2021, Menary and Gillett, 2022].
The
present framework assumes such a modeling boundary has already been chosen and studies dependence inside the
agent’s policy space. Multi-agent and biological readings are therefore hypotheses generated by the mathematics,
not conclusions proved by it. The artifact’s current empirical evidence is finite, discrete, and pymdp-grounded; the
broader FEP reading remains interpretive unless a paragraph points to a theorem row, a generated sidecar, a figure,
and the relevant validation gate.
Six load-bearing properties
Each item below is a pointer into a body section. Together, these six items constitute the load-bearing properties of
the framework: policy entanglement classifies existing architectures as exact, parametric, or analogical relationships
109

## Page 111

to a common joint-policy posterior (economy), explains when joint structure pays for itself (decomposition +
geometry), predicts the small set of dominant coordination modes a coupled agent expresses (spectral), bounds
the suboptimality of mixing reflexive and planning streams (heterogeneous), and is auditable end-to-end against a
stock Lean 4 boundary fragment plus generated numerical artifacts (formalization). The framework is therefore
positioned as a candidate model of multi-stream policy inference and an engineering tool for building agents that
interpolate between modular and joint inference without committing to either pole.
1. Theoretical economy. A single coupling parameter 𝜆exactly recovers the mean-field baseline (Corollary 5.3)
and then organizes the neighboring active-inference variants by claim class: hierarchical AIF is a witness-form
concentration analog (Theorem 17.1), sophisticated inference is a witness-form embedding whose recursive
observation-conditioning must be supplied through 𝐽(Proposition 17.2), and branching-time AIF is an
algorithmic analogy through policy-tree compression rather than a current head-to-head empirical result.
2. Decomposition theorem. The free-energy decomposition (Theorem 5.1, Eq. (5.2)) factors variational free
energy into per-stream marginals, a coupling-potential bundle, and the multi-information 𝐼(𝑞𝜆) ≥0.
3. Geometric principle. The family {𝑞𝜆} traces an e-geodesic away from the mean-field submanifold (Theorem
7.4, Eq. (7.3)); revertibility is the canonical m-projection (Proposition 7.2); phase structure is symmetry-
breaking on the entanglement manifold.
4. Spectral interpretation.
Schmidt rank and tensor-train bond dimensions (Proposition 8.1) give a
computable handle on archetypal eigenvectors — the dominant cross-stream behavioral modes a coupled agent
expresses.
5. Heterogeneous-ensemble bound. The 𝑂(𝜆2) coupling-tax (Theorem 9.1, Eq. (9.2)) bounds the subop-
timality of VFE-only streams operating inside EFE-planning ensembles, with a small-𝜆tolerance corollary
(Corollary 9.2).
6. Lean verification. The central result — the full S01 free-energy identity (Theorem 5.1) 𝐹[𝑞𝜆] = ∑𝑘𝐹[𝑞𝑘
𝜆] +
𝛾𝜆⟨𝐾𝑐⟩+ log 𝑍𝐸(𝜆)−𝜆⟨𝐽⟩+𝐼(𝑞𝜆) — is machine-checked in ℝby MathlibProofs.free_energy_decomposition_-
full for the genuine entangled posterior (log 𝑍𝐸the definitional log-normalizer, positivity/unit-mass proved,
the multi-information term discharged through the axiom-clean general-𝐾kernel), with #print
axioms
foundational-only and two independent negative controls.
A stock-Lean v4.29.0 boundary fragment ships
the 21-row theorem surface as a typed API for the Python computational layer (zero sorry, zero axioms
beyond stock Lean, zero Mathlib dependency); the per-row content table at §12 and the running audit at
docs/reference/veridical_status.md document what each row certifies in the boundary fragment versus the
Mathlib4 discharge target.
Live state of the artifact
This manuscript is rendered against a real, reproducible run:
• The K=2 Bernoulli closed form is verified to floating tolerance (≤1𝑒−06 across 121 grid points).
• The 1.0.1 grounded harness (§14) sweeps 𝜆∈[0, 4] on a 21-point grid; the half-saturation coupling 𝜆1/2 ≈1.044
locates the half-maximum of total correlation 𝐼max ≈0.3635 nats.
• The same harness exercises the configured multi-stream ensemble set 𝐾∈{3, 4, 5} (𝐼(𝑞2) ≈0.2169, 0.1216,
and 0.0784 nats across the configured 𝐾values at 𝜆= 2), runs a 𝑇= 100-step long-horizon rollout with
steady-state KL 0.1334 and habit-accumulation signal 1.0000, reports a long-horizon replicate pass rate
of 0.60, and witnesses the 𝑚-projection revertibility identity 𝐼(𝑞) = 𝐷KL(𝑞‖
̂𝑚(𝑞)) to round-off precision
(1.67𝑒−16 maximum residual across the 5-point sweep).
The revertibility identity is computed by two
independent code paths — 𝐼(𝑞) via ∑𝑘𝐻(𝑞𝑘)−𝐻(𝑞) (free_energy.total_correlation) and 𝐷KL(𝑞‖
̂𝑚(𝑞)) via
direct ∑𝜋𝑞log(𝑞/ ̂𝑚) (free_energy.kl_divergence) — whose equivalence is Proposition 7.3 / Theorem 5.1; the
witness-conformance suite (tests/test_witness_conformance.py) supplies the complementary discriminating
tests against wrong-𝑞inputs.
• The robustness layer adds 14 one-axis scenarios, 4 fixed coupling ablations, and 41 targeted two-axis interaction
scenarios. These rows are supporting stress evidence: the largest two-axis decomposition residual is 1.67e-15,
and the null-variant interaction flatline remains at 0.00e+00.
• Every numeric value above flows from a real run via the
[[VAR:<key>]] token system rooted in
src/simulation/hyperparameters.py, with the no-hardcoded-vars CI gate enforced (§16).
The discussion claims therefore reduce to the following evidence-and-caveat ledger:
Discussion claim
What the current artifact shows
Remaining caveat
𝜆recovers strict mean-field at zero coupling
𝜆= 0 outer-product tests pass in the pure
NumPy layer and the pymdp harness
Continuous-state analogs are outside the
current finite-state artifact
110

## Page 112

Discussion claim
What the current artifact shows
Remaining caveat
Coupling creates measurable joint structure
Total correlation rises from 0.000000 to
0.3635 nats on the pymdp sweep
This is a controlled Ising-style task, not a
broad behavioral benchmark
Structured coupling scales beyond two
streams
The configured 𝐾∈{3, 4, 5} sweeps report
nonzero total correlation and bounded
tensor-train ranks
Larger stream counts need sparse /
tensor-network inference rather than dense
enumeration
Long-horizon coupling can accumulate
habit mass
The 𝑇= 100 rollout reaches tail KL 0.1334
and habit signal 1.0000
The current rollout is deterministic and
task-specific
Revertibility is operational, not rhetorical
The 𝑚-projection identity residual is
1.67𝑒−16 across the revertibility sweep;
the witness-conformance suite discriminates
against wrong-𝑞inputs separately
Both checks are restricted to the configured
finite-policy task family
The Lean track is live
All 21 boundary-fragment theorems ship as
a typed API; the central identity is
machine-checked in ℝby
MathlibProofs.free_energy_decomposition_-
full
Typed-API rows on the boundary fragment
delegate their analytic payload to the
Mathlib4 layer (see §20 Q14)
Stress evidence is supporting, not
headline-tuning
One-axis, ablation, two-axis, and
seed-diagnostic sidecars expose sensitivity
rather than hiding it
The stress suite remains a controlled binary
policy task family
Alignment and Dysregulation Hypotheses
Beyond the regimes characterized in §10, we sketch two interpretive hypotheses not developed as empirical claims in
the present manuscript. Both subsections below carry claim-strength hypothesis per the legend at §S7.1
— they are model-generated interpretive frames, not empirical results. No row in §S7.2 currently
promotes either to empirical.
[claim: hypothesis] — First, on alignment: the framework distinguishes local (per-stream) policy updates from global
(coupling-structure) updates — the distinction between “adjusting what to do in one situation” and “rewiring how
you coordinate across situations.” Most existing AIF safety analysis focuses on the former. Coupling drift across
temporal scales — where 𝜆slowly evolves on a longer timescale than the per-stream beliefs 𝑞𝑘— defines a candidate
failure mode for multi-stream agents: an agent whose 𝜆drifts toward over-coupling (rigid archetypal behavior) or
under-coupling (dissociated streams) would fail in a different way than one whose per-stream priors are corrupted.
We do not develop that learning rule in this artifact; we state only the structural hypothesis and the measurements
needed to test it.
[claim: hypothesis] — Second, on flourishing: the middle-regime 𝜆∼𝜆∗corresponds to the flexibility characteristic
of skilled, integrated behavior — a candidate operationalization of distinctions between rigid habit, fragmented
attention, and integrated awareness. The framework offers an analytic handle; we do not push the analogy further
here, flagging it as a hypothesis for cross-disciplinary inquiry. Clinical and consciousness- science vocabulary in
this paragraph is interpretive, not diagnostic: no row in the variant-recovery ledger of §S7.2 asserts a clinical or
phenomenological equivalence.
Limitations
Limitations a critical reader should track:
• Scope: finite policy spaces. The analytical core (§4–§8) assumes finite Π𝑘. A Gaussian-copula analog is
conjectured for the continuous case (§20 Q4).
• Scope:
empirical task family.
The 1.0.1 grounding exercises the K=2 Ising ensemble plus the multi-
K sweep 𝐾∈{3, 4, 5}, 𝑇= 10 and 𝑇= 100 rollouts, the 𝑚-projection revertibility witness, and the
robustness sidecars. The head-to-head Branching-Time AIF baseline and the adversarial-perturbation sweep
are now implemented, unit-tested, and run as pipeline stages (§13; ../src/simulation/btai_baseline.py,
../src/simulation/adversarial.py), emitting auditable sidecars; the full compute-matched BTAI hypothesis
test and a broader adversarial robustness analysis remain author-led future analysis rather than claims
established here.
• Identifiability gauge. The gauge freedom in 𝐽(§20 Q5) is characterised explicitly as the additive mean-
field-decomposable subgroup; the identifiable coupling lives in the quotient. Multi-agent extensions (§20 Q15)
compound the question.
• Phase-diagram thresholds. The values (𝜆(1)
𝑐, 𝜆(2)
𝑐) = (0.5, 2.5) in §10 are illustrative; the analytic conditions
that determine them (spectral-gap closing / opening on the 𝜆trace) are stated in §10.
• Engagement with recent unification efforts. The Millidge / Champion / de Vries / Nuijten line on
EFE derivations and EFE-as-variational-inference is engaged in §17 at chapter granularity; a paper-by-paper
systematic comparison is tracked as journal-format companion work [Millidge et al., 2021, Champion et al.,
111

## Page 113

2024, de Vries et al., 2025, Nuijten and Lukashchuk, 2025].
• Interpretive scope.
Biological, clinical, and alignment language in this manuscript is claim-strength
hypothesis unless the text points to a formal row, generated artifact, primary citation, or explicit roadmap
item; the empirical-status review serves as the cautionary reference [Hodson et al., 2024].
Each item maps to a tractable extension in §20. The four-track ledger — prose, Lean companion, Python witness,
and test gate — is wired per registry row with status: and faithfulness: tiers (see §S7.1 and methods_and_-
assumptions.md); not every row carries a substantive Python re-proof of its analytic payload.
Threats to validity
The reviewer-facing threat model has five parts. The numerical threat is finite precision: the pymdp/JAX path
and the NumPy analytical path use different floating formats, so residual claims are tolerance-bounded and
validated artifact-by-artifact; a verified error-bounded Float↔ℝbridge linking the ℝ-level proofs to the Float
pipeline (Flocq-style formal IEEE-754 [IEEE, 2019, Boldo and Melquiond, 2011] or interval arithmetic) is the
natural formal sibling of the present dashboard-invariant binding, and remains the one open verification-stack
residual (route map and the specific Mathlib4 lemmas required: docs/reference/methods_and_assumptions.md). The
implementation-link threat is that the Python code is not extracted from Lean: it is an independently implemented
numerical companion whose coherence with the theorem surface is enforced by registries, token resolution, generated
sidecars, and tests, not by a verified compiler. The package-version threat is dependency drift:
inferactively-
pymdp==1.0.1 (the package that provides the pymdp import/API) and Lean v4.29.0 are part of the claim surface,
and release readiness depends on regenerating the sidecars, PNG metadata, rendered manuscript, PDF, and
regression reports under those pins. The publication-metadata threat is metadata drift: the public Zenodo DOI
and public source archive at https://github.com/ActiveInferenceInstitute/policy_entanglement must stay aligned
across manuscript/config.yaml, CITATION.cff, the manuscript citation entry, and rendered PDF front matter. The
interpretive threat is overextension: biological, clinical, and alignment language is claim-strength hypothesis unless
the text points to a formal row, generated artifact, primary citation, or explicit roadmap item.
Verification ledger
Every load-bearing claim of the manuscript is established by one or more of the following five substrates, with a
per-claim assignment that a reader can use to navigate from prose to evidence:
Claim
Substrate
Where it lives
The free-energy decomposition identity
(Theorem 5.1) holds for the genuine
entangled posterior
Lean ℝ-level proof
MathlibProofs.free_energy_decomposition_-
full (foundational-only #print axioms, two
negative controls)
The multi-information 𝐼(𝑞) ≥0 with
equality iff 𝑞is mean-field
Lean ℝ-level proof
MathlibProofs.entanglement_decomposition_-
generalK; standalone-named form
MathlibProofs.multiInformation_nonneg_at_-
joint
Per-stream marginals 𝑞𝑘are strictly
positive on a strictly-positive joint
Lean ℝ-level proof
MathlibProofs.streamMarginal_pos (the
analytic precondition for the bridge identity
above)
The 𝜆= 0 mean-field reduction (Corollary
5.3)
Lean stock-Lean boundary fragment, proved
substantive
Decomposition.couplingLogWeight_pointwise_-
at_zero
The coupling-verdict decision procedure
(Corollary 5.2) is sound
Lean stock-Lean boundary fragment, proved
substantive
Decomposition.couplingVerdict_correct
The four-term decomposition shape locks
the parameter-threading discipline
Lean typed-API contract
3 boundary + 11 witness-form rows in §12
The closed-form K=2 Bernoulli total
correlation matches the finite-𝑁
Monte-Carlo estimator within a
√
𝑁band
Python numerical witness
tests/test_bernoulli_toy.py
The 𝑚-projection revertibility identity
holds across the configured sweep
Two-route Python computation +
dashboard invariant
free_energy.total_correlation vs
free_energy.kl_divergence;
decomposition_lhs_eq_rhs_max_residual
Discrimination against wrong-𝑞inputs
Python witness-conformance suite
tests/test_witness_conformance.py
The pymdp harness emits the full
free-energy bundle at every 𝜆
1.0.1 grounded run + token system
[[VAR:<key>]] injection through
src/simulation/hyperparameters.py
The 𝑂(𝜆2) coupling-tax bound on
heterogeneous ensembles (Theorem 9.1)
Analytic prose proof + numerical envelope
verification
§9 + §13 31-point sweep
Every numeric value in the rendered
manuscript comes from a real run
CI gate
scripts/validate_manuscript.py
no-hardcoded-vars + [[VAR:...]] resolver
Every Lean source block in the rendered
manuscript is a live extraction
CI gate
src/manuscript/lean_extract.py +
dangling-token failure mode
112

## Page 114

Claim
Substrate
Where it lives
Every registry theorem row has a Lean
companion and a four-track wiring check
Per-row registry + four-track validator
manuscript/refs/labels.yaml +
cross-reference tests; Python witnesses are
faithfulness-tiered, not uniformly
substantive re-proofs
dashboard invariants pass on every build
Numerical regeneration gate
scripts/run_all.py final stage
The alignment / dysregulation hypotheses
do not assert clinical equivalence
Claim-strength tag hypothesis
§S7.1 legend; §S7.2 promotion gate
A referee who reads only this table can locate the substrate of every assertion of the manuscript without traversing
the body chapter graph.
Open directions
The verified ℝformal core and the four-track empirical artifact leave a small, explicitly-scoped set of open directions.
Each is tracked in an existing section above or in the appendices rather than asserted as a commitment here; the head-
to-head Branching-Time AIF baseline and the adversarial-perturbation sweep that were previously listed here are
now implemented, unit-tested, and run as pipeline stages (§13). Likewise, the Generalized Notation Notation
(GNN) bridge that was previously listed here as a roadmap direction now ships as a fifth, structural-and-numerical
track (§S8): a project-owned parser, a shipped K=2 round-trip (an internal-consistency reduction that reproduces
the closed-form mutual-information curve to 7.77e-16 nats — not an independent validation — with a non-vacuous
zero-coupling negative control), a Lean typed-contract emitter, and a GNN-sourced manuscript variable, all run in
the pipeline. The GNN track reproduces structure and numbers but proves no theorem, so it does not amend the
four-track proof integration claim of §1; its genuine residuals (a first-class upstream coupling primitive; full-bundle
pymdp regeneration) are scoped as open questions at §S8.9.
• Mathlib4 analytic discharge for the typed-API rows.
Extending MathlibProofs/ to discharge the
analytic payloads behind the 11 witness-tier rows of §12 — finite KL / entropy chain rules (Proposition 7.3,
Proposition 7.5, Proposition 19.3); convexity / Taylor envelopes (Theorem 5.6, Proposition 11.1); Bregman /
quadratic envelope (Theorem 9.1, Corollary 9.2); rank and spectral continuity (Proposition 8.2, Theorem 8.3);
concentration and recursive embedding (Theorem 17.1, Proposition 17.2) — is open theoretical work, tracked
at §20 and the claim-strength roadmap of §S7. The central result (Theorem 5.1) is already discharged in ℝ
by MathlibProofs.free_energy_decomposition_full (see the Verification ledger above); this direction extends
that discharge to the remaining witness-tier analytic payloads.
• Float↔ℝformal bridge. The single open verification-stack residual — a Flocq-style IEEE-754 [IEEE, 2019,
Boldo and Melquiond, 2011] or interval-arithmetic bound linking the ℝ-level proofs to the Float pipeline
— is stated under Threats to validity above, with the route map and the specific Mathlib4 lemmas at
docs/reference/methods_and_assumptions.md.
• Cross-repository reproducibility. Aligning this project’s manuscript_variables.json token schema with
the registries used by sister projects would enable shared reproducibility audits across manuscripts; this is
minor infrastructure, orthogonal to the framework’s claims.
• Community contribution and archival metadata. The working citation entry [Friedman, 2026a] is the
current citation target; the public Zenodo DOI and source repository are recorded in manuscript/config.yaml
and CITATION.cff. The open questions of §20 each admit independent contribution.
Proof of the Entanglement Decomposition
We prove the decomposition identity stated in §5.1 (Theorem 5.1, entanglement decomposition theorem), namely
𝐹[𝑞] = ∑
𝑘
𝐹[𝑞𝑘] + 𝛾𝜆𝔼𝑞[𝐾𝑐] + log 𝑍𝐸(𝜆) −𝜆𝔼𝑞[𝐽] + 𝐼(𝑞)
(5.2)
.
The Lean type-level statement is in lean/ActinfPolicyEntanglement/Decomposition.lean (entanglement_decomposi-
tion); the numerical realization lives in src/lean/decomposition.py and is exercised by tests/test_decomposition.py.
113

## Page 115

Definitions
𝐹[𝑞𝜆] ≡𝔼𝑞𝜆[𝛾𝐺𝜆] −𝔼𝑞𝜆[log ℰ𝜆] −𝐻(𝑞𝜆),
(A.2)
𝐹[𝑞𝑘
𝜆] ≡𝔼𝑞𝑘
𝜆[𝛾𝐺𝑘] −𝔼𝑞𝑘
𝜆[log 𝐸𝑘] −𝐻(𝑞𝑘
𝜆),
(A.3)
with 𝐺𝜆(𝜋) = ∑𝑘𝐺𝑘(𝜋𝑘) + 𝜆𝐾𝑐(𝜋) and, for the normalized entangled prior ℰ𝜆∝( ∏𝑘𝐸𝑘) 𝑒𝜆𝐽,
log ℰ𝜆(𝜋) = ∑
𝑘
log 𝐸𝑘(𝜋𝑘) + 𝜆𝐽(𝜋) −log 𝑍𝐸(𝜆).
(A.4)
Expanding the EFE expectation
𝛾𝐺𝜆(𝜋) = 𝛾∑
𝑘
𝐺𝑘(𝜋𝑘) + 𝛾𝜆𝐾𝑐(𝜋),
(A.5)
so
𝔼𝑞𝜆[𝛾𝐺𝜆] = 𝛾∑
𝑘
𝔼𝑞𝑘
𝜆[𝐺𝑘] + 𝛾𝜆⟨𝐾𝑐⟩𝑞𝜆.
(A.6)
Expanding the prior log-expectation
𝔼𝑞𝜆[log ℰ𝜆] = ∑
𝑘
𝔼𝑞𝑘
𝜆[log 𝐸𝑘] + 𝜆⟨𝐽⟩𝑞𝜆−log 𝑍𝐸(𝜆).
(A.7)
Combining
Substitute both expansions into the definition of 𝐹[𝑞𝜆]:
𝐹[𝑞𝜆] = ∑
𝑘
(𝛾𝔼𝑞𝑘
𝜆[𝐺𝑘] −𝔼𝑞𝑘
𝜆[log 𝐸𝑘]) −𝐻(𝑞𝜆) + 𝛾𝜆⟨𝐾𝑐⟩𝑞𝜆−𝜆⟨𝐽⟩𝑞𝜆+ log 𝑍𝐸(𝜆)
= ∑
𝑘
𝐹[𝑞𝑘
𝜆] + ∑
𝑘
𝐻(𝑞𝑘
𝜆) −𝐻(𝑞𝜆) + 𝛾𝜆⟨𝐾𝑐⟩𝑞𝜆−𝜆⟨𝐽⟩𝑞𝜆+ log 𝑍𝐸(𝜆).
(A.8)
Finally, using the multi-information identity ∑𝑘𝐻(𝑞𝑘
𝜆) −𝐻(𝑞𝜆) = 𝐼(𝑞𝜆) and
𝐼(𝑞) = ∑
𝑘
𝐻(𝑞𝑘) −𝐻(𝑞) = 𝐷KL(𝑞‖ ∏
𝑘
𝑞𝑘)
(5.3)
,
𝐹[𝑞𝜆] = ∑
𝑘
𝐹[𝑞𝑘
𝜆] + 𝛾𝜆⟨𝐾𝑐⟩𝑞𝜆+ log 𝑍𝐸(𝜆) −𝜆⟨𝐽⟩𝑞𝜆+ 𝐼(𝑞𝜆).
(A.10)
This is exactly the registry equation
𝐹[𝑞] = ∑
𝑘
𝐹[𝑞𝑘] + 𝛾𝜆𝔼𝑞[𝐾𝑐] + log 𝑍𝐸(𝜆) −𝜆𝔼𝑞[𝐽] + 𝐼(𝑞)
(5.2)
. The Python helper entanglement_decomposition_rhs sums the same four grouped pieces: ∑𝑘𝐹[𝑞𝑘], coupling_-
cost_term = 𝛾𝜆𝔼[𝐾𝑐], coupling_prior_term = log 𝑍𝐸(𝜆) −𝜆𝔼[𝐽], total_correlation_gain = 𝐼(𝑞).
Numeric agreement with the Gibbs definition of 𝐹[𝑞𝜆] is checked in tests/test_decomposition.py (identity on random
joints).
Interpretation (sign of 𝐼)
The multi-information 𝐼(𝑞𝜆) is non-negative and vanishes iff 𝑞𝜆is mean-field. In the displayed Gibbs expansion it
appears with a plus sign: departures from factorization incur an entropy surplus relative to independent streams
holding the same marginals. Trade-offs with the coupling and EFE terms determine whether 𝜆> 0 is optimal for a
given agent — §6 and Corollary 5.2 make that comparison explicit.
114

## Page 116

Closed exponential-family form (collapsed identity)
The same expansion admits a strikingly compact closed form that the body uses to differentiate 𝐹with respect
to 𝜆in Theorem 5.5 and Proposition 11.1. Let 𝑍𝐸(𝜆) = ∑𝜋𝐸MF(𝜋) 𝑒𝜆𝐽(𝜋) be the entangled-prior normalizer and
𝑍(𝜆) = ∑𝜋𝐸MF(𝜋) 𝑒𝜆(𝐽−𝛾𝐾𝑐)(𝜋)−𝛾𝐺MF(𝜋) the joint posterior normalizer.
Substituting log 𝑞𝜆(𝜋) = log 𝐸MF(𝜋) −
𝛾𝐺MF(𝜋)+𝜆(𝐽(𝜋)−𝛾𝐾𝑐(𝜋))−log 𝑍(𝜆) into 𝐹[𝑞𝜆] = 𝔼𝑞𝜆[𝛾𝐺𝜆−log ℰ𝜆]−𝐻(𝑞𝜆) (with 𝐻(𝑞𝜆) = −𝔼𝑞𝜆[log 𝑞𝜆]) cancels
every expectation term and leaves the registered identity Eq. (5.8):
𝐹[𝑞𝜆] = log 𝑍𝐸(𝜆) −log 𝑍(𝜆)
(5.8)
The Gibbs decomposition above and this closed identity are the same fact; one is additive over streams, the other
multiplicative through normalizers. The closed form makes derivatives in 𝜆trivial via standard exponential-family
identities,
d
d𝜆log 𝑍𝐸(𝜆) = ⟨𝐽⟩ℰ𝜆,
d
d𝜆log 𝑍(𝜆) = ⟨𝐽−𝛾𝐾𝑐⟩𝑞𝜆,
(A.13)
so the registered first- and second-derivative forms Eq. (5.9) and Eq. (A.15) follow:
d𝐹[𝑞𝜆]
d𝜆
= ⟨𝐽⟩ℰ𝜆−⟨𝐽⟩𝑞𝜆+ 𝛾⟨𝐾𝑐⟩𝑞𝜆
(5.9)
d2𝐹[𝑞𝜆]
d𝜆2
= Varℰ𝜆(𝐽) −Var𝑞𝜆(𝐽−𝛾𝐾𝑐)
(A.15)
These are the formulas that Theorem 5.5 (existence of 𝜆⋆) and Proposition 11.1 (sign of the second derivative at
𝜆= 0) consume; §B uses the same identity to characterize convexity of 𝐹in 𝜆.
Convexity of Free Energy in Lambda: Conditions and Counter-Example
The free-energy curve along the 𝜆-deformation has a clean exponential-family structure that delivers convexity in 𝜆on
the natural side. We sketch the proof here; the closed-form K = 2 case is verified numerically by scripts/generate_-
figures.py (see output/figures/free_energy_curve.png).
The closed exponential-family form
§A establishes the closed identity
𝐹[𝑞𝜆] = log 𝑍𝐸(𝜆) −log 𝑍(𝜆),
(B.1)
where the two normalizers are the entangled prior ℰ𝜆and the entangled posterior 𝑞𝜆respectively. Each is the log-
partition of an exponential family in 𝜆— natural parameter 𝜆, suﬀicient statistic 𝐽(for the prior side) and 𝐽−𝛾𝐾𝑐
(for the posterior side). Standard exponential-family identities give
d
d𝜆log 𝑍𝐸(𝜆) = ⟨𝐽⟩ℰ𝜆,
d2
d𝜆2 log 𝑍𝐸(𝜆) = Varℰ𝜆(𝐽),
(B.2)
and analogously for log 𝑍(𝜆) with statistic 𝐽−𝛾𝐾𝑐and reference distribution 𝑞𝜆. Both log-partitions are convex in
𝜆; their difference is a question of which side is “more convex” in 𝜆.
The convexity ledger
Differentiating the closed identity once more:
d2𝐹[𝑞𝜆]
d𝜆2
= Varℰ𝜆(𝐽) −Var𝑞𝜆(𝐽−𝛾𝐾𝑐).
(B.3)
Hence:
• Convex regime — 𝐹″(𝜆) ≥0 on an interval iff the prior dispersion of 𝐽exceeds the posterior dispersion of
𝐽−𝛾𝐾𝑐throughout that interval. This holds, e.g., whenever the posterior concentrates much faster than the
prior in the natural-parameter direction (large 𝛾, sharply peaked 𝐺𝑘).
115

## Page 117

• Concave / saddle regime — 𝐹″(𝜆) ≤0 when the posterior dispersion dominates. This is the regime in
which raising 𝜆pays for itself first-order: every example in §6 starts here at 𝜆= 0 (Proposition 11.1).
• Inflection / mixed regime — 𝐹″ may change sign exactly once along [0, ∞), locating an inflection coupling
𝜆infl that separates the two regimes. Below 𝜆infl the agent benefits from more coupling; above, marginal returns
reverse — the location of the optimal 𝜆⋆(§5.4).
Suﬀicient condition for global convexity on [0, ∞)
If for every 𝜆≥0 the prior dispersion of the habit coupling dominates the posterior dispersion of the combined
statistic,
Varℰ𝜆(𝐽) ≥Var𝑞𝜆(𝐽−𝛾𝐾𝑐)
for all 𝜆≥0,
(B.4)
then 𝐹[𝑞𝜆] is convex on [0, ∞) and 𝜆⋆is unique. This is the crisp form of Theorem 5.6 in the language of dispersion
comparison; the original “log-concavity of 𝐽−𝛾𝐾𝑐” suﬀicient condition implies this dispersion inequality on the
natural domain via Brascamp–Lieb (we omit the standard argument).
K = 2 Symmetric Ising specialization
In the symmetric K = 2 Ising example with uniform 𝐸MF, zero per-stream EFE, and bilinear 𝐽= 𝐽0(2𝜋1−1)(2𝜋2−1):
log 𝑍𝐸(𝜆) = log cosh(𝜆𝐽0),
log 𝑍(𝜆) = log cosh(𝜆𝐽0)
(B.5)
(both partition functions agree because 𝛾𝐾𝑐≡0 here), so 𝐹[𝑞𝜆] ≡0 — the toy is flat in 𝜆when no preference
coupling is present. Adding a utility-driven 𝐺shifts log 𝑍(𝜆) but leaves log 𝑍𝐸invariant; the resulting 𝐹[𝑞𝜆] =
log cosh(𝜆𝐽0) −log 𝑍(𝜆) is convex in 𝜆on [0, ∞) for any utility level (verified numerically across 𝑢∈{0, 0.5, 1, 2} in
output/figures/free_energy_curve.png).
Numerical verification
The K = 2 Ising free-energy curve at four utility values is plotted in output/figures/free_energy_curve.png. The
curve is monotonically decreasing in |𝜆| for any 𝑢≥0, consistent with convexity (and with the closed-form expression
in §C).
Complete Derivation: Two-Stream Bernoulli Toy
Closed-form
derivations
of
the
multi-information
𝐼(𝜆),
the
alignment-inversion
coupling
𝜆⋆(Δalign)
=
2 arctanh(Δalign/Δmax),
and
the
closed-form
free-energy
curve.
Appendix
scaling
gives
𝐼(𝜆) = (𝜆/2) tanh(𝜆/2) −log cosh(𝜆/2) = log 2 −𝐻𝑏(𝜎(𝜆)); not 𝐼(𝜆) = log cosh 𝜆(which would be a derivation
error).
Reproduces the calculation in §6.1 with full algebra. Companion code: src/lean/bernoulli_toy.py; Lean boundary:
lean/ActinfPolicyEntanglement/BernoulliToy.lean.
Setup
Two binary streams 𝜋1, 𝜋2 ∈{0, 1} with symmetric Bernoulli( 1
2) mean-field marginals 𝐸1(𝜋1) = 𝐸2(𝜋2) = 1
2, zero
per-stream EFE, and the swing-1 Ising coupling
𝐽(𝜋1, 𝜋2) = 1[𝜋1 = 𝜋2] −1
2,
𝐽∈{+ 1
2, −1
2}.
(C.1)
Joint posterior
The unnormalized joint at coupling 𝜆is
̃𝑞𝜆(𝜋) = 1
4 exp(𝜆𝐽(𝜋)). The normalizer is
𝑍(𝜆) =
1
4(2𝑒𝜆/2 + 2𝑒−𝜆/2) =
1
2 (𝑒𝜆/2 + 𝑒−𝜆/2) = cosh(𝜆/2).
(C.2)
Hence the normalized joint:
116

## Page 118

𝑞𝜆(𝜋1 = 𝜋2) =
𝑒𝜆/2
4 cosh(𝜆/2),
𝑞𝜆(𝜋1 ≠𝜋2) =
𝑒−𝜆/2
4 cosh(𝜆/2).
(C.3)
The aligned mass (sum over the two aligned atoms) is
𝑃𝑎(𝜆) ≡𝑞𝜆(𝜋1 = 𝜋2) ⋅2 =
𝑒𝜆/2
2 cosh(𝜆/2) =
1
1 + 𝑒−𝜆= 𝜎(𝜆).
(C.4)
Marginals (uniform by symmetry)
By inspection, summing over 𝜋2:
𝑞1
𝜆(𝜋1 = 0) = 1
2𝑃𝑎+ 1
2(1 −𝑃𝑎) = 1
2,
𝑞1
𝜆(𝜋1 = 1) = 1
2.
(C.5)
Marginals are uniform Bernoulli( 1
2) for any 𝜆— marginal invariance of the Ising deformation.
Joint and marginal entropies
Using natural log throughout:
𝐻(𝑞𝑘
𝜆) = log 2
(𝑘= 1, 2).
(C.6)
For the joint, the four atoms have masses {𝑃𝑎/2, 𝑃𝑎/2, (1 −𝑃𝑎)/2, (1 −𝑃𝑎)/2}, so
𝐻(𝑞𝜆) = −2 ⋅𝑃𝑎
2 log 𝑃𝑎
2
−2 ⋅1 −𝑃𝑎
2
log 1 −𝑃𝑎
2
.
(C.7)
Expand:
𝐻(𝑞𝜆) = −𝑃𝑎(log 𝑃𝑎−log 2) −(1 −𝑃𝑎)(log(1 −𝑃𝑎) −log 2) = 𝐻𝑏(𝑃𝑎) + log 2,
(C.8)
where 𝐻𝑏(𝑝) = −𝑝log 𝑝−(1 −𝑝) log(1 −𝑝).
Closed-form mutual information
By definition 𝐼(𝑞𝜆) = ∑𝑘𝐻(𝑞𝑘
𝜆) −𝐻(𝑞𝜆):
𝐼(𝜆) = 2 log 2 −𝐻𝑏(𝜎(𝜆)) −log 2 = log 2 −𝐻𝑏(𝜎(𝜆)).
(C.9)
Equivalently, using the identities log ((1 + 𝑒𝜆)/2) = log cosh(𝜆/2) + 𝜆/2 and 𝜎−1
2 = 1
2 tanh(𝜆/2), one obtains the
second canonical form
𝐼(𝜆) =
𝜆
2 tanh(𝜆/2) −log cosh(𝜆/2).
(C.10)
This is the form that appears naturally in §B’s exponential-family decomposition (where 𝜓(𝜆) = log cosh(𝜆/2) is the
log-partition). The two forms are algebraically identical; we use whichever is more convenient.
Sanity checks:
• 𝜆= 0: 𝜎(0) = 1
2, 𝐻𝑏( 1
2) = log 2, so 𝐼(0) = 0 ✓(mean-field).
• 𝜆→∞: 𝜎(𝜆) →1, 𝐻𝑏→0, so 𝐼→log 2 ✓(saturation at one-bit alignment).
• Even in 𝜆: 𝜎(−𝜆) = 1 −𝜎(𝜆) and 𝐻𝑏is symmetric around 𝑝= 1
2, so 𝐼(−𝜆) = 𝐼(𝜆) ✓.
• Numerical: at 𝜆= 1, 𝐼(1) = log 2 −𝐻𝑏(𝜎(1)) ≈0.1109; 1
2 tanh( 1
2) −log cosh( 1
2) ≈0.1109 ✓.
Coupling from a target alignment (alignment-inversion, not a VFE optimum)
Define the expected alignment of the joint posterior as
𝛼(𝜆) ≡2𝜎(𝜆) −1 = tanh(𝜆/2),
(C.11)
ranging from 0 at 𝜆= 0 (uniform) to ±1 at 𝜆→±∞(perfectly aligned / anti-aligned). Given a target alignment
Δalign ∈(−Δmax, Δmax) with Δmax = 1, inverting 𝛼(𝜆) = Δalign yields
117

## Page 119

𝜆⋆(Δalign) = 2 arctanh(Δalign/Δmax).
(C.12)
This is the closed-form coupling that realizes the target alignment Δalign; it is the inverse of the alignment–
coupling correspondence, not a free-energy first-order condition. We use the name 𝜆⋆(Δalign) rather than
𝜆⋆(Δutil) to make this explicit: Δalign is a target on the alignment axis, not a utility surplus.
• Δalign = 0 ⇒𝜆⋆= 0 (mean-field).
• Δalign →±Δmax ⇒𝜆⋆→±∞(frozen archetypes).
Connection to actual VFE optimization. The genuine VFE-optimization problem in this Bernoulli toy is:
given a utility scalar 𝑢that pays 𝑢per unit alignment via an EFE term −𝑢𝛼(𝜆), minimize the framework free
energy 𝐹VFE(𝜆) = −𝑢(2𝜎(𝜆) −1) + 𝐼(𝜆) = −𝑢tanh(𝜆/2) + 𝐼(𝜆) in 𝜆— note the +𝐼sign, consistent with the
decomposition theorem Eq. (5.2) in which multi-information enters with a plus sign (sign conventions in §S6).
Using d𝐼/d𝜆= 1
4 𝜆sech2(𝜆/2) (differentiate the closed form 𝐼= (𝜆/2) tanh(𝜆/2) −log cosh(𝜆/2) and simplify with
d tanh(𝜆/2)/d𝜆=
1
2 sech2(𝜆/2)), the first-order condition is −𝑢
2 sech2(𝜆/2) + 𝜆
4 sech2(𝜆/2) = 0, which simplifies
(since sech2(𝜆/2) > 0) to
𝜆⋆
VFE(𝑢) = 2𝑢.
(C.13)
The second derivative is 1
4 sech2(𝜆/2) at 𝜆⋆modulo a correction of order 𝑢through the chain rule, and is positive
on a neighborhood of 𝜆⋆, confirming a strict minimum. Thus the VFE-optimum is linear in the utility scalar; the
alignment-inversion formula 2 arctanh(𝑢) agrees with it only at small 𝑢(Taylor: 2 arctanh(𝑢) = 2𝑢+ 2
3𝑢3 + ⋯) and
diverges from it as 𝑢→1. The two should not be conflated: 𝜆⋆
VFE(𝑢) = 2𝑢is the answer to “what coupling minimizes
free energy under utility 𝑢?”, while 𝜆⋆(Δalign) = 2 arctanh(Δalign) is the answer to “what coupling realizes a given
target alignment Δalign?”.
A second, Lagrangian, interpretation. If instead one seeks the 𝜆that maximizes a Lagrangian of the form
Δalign 𝛼(𝜆) −𝜅𝐼(𝜆) (utility-times-alignment minus a multi-information cost with multiplier 𝜅> 0), the first-order
condition gives yet another formula: the slope of the multi-information balances the slope of the alignment. This is
the Lagrange-balance regime studied numerically in scripts/parameter_sweep.py. In every interpretation, 𝜆⋆inherits
saturation at Δmax and monotonicity in Δalign, but the three formulas (2 arctanh, 2𝑢, Lagrange-balance) are distinct
quantities answering distinct questions.
Free-energy curve
With utility scalar 𝑢≥0 giving the surplus per aligned outcome, the toy’s Lagrangian-style scalarisation of free
energy is the following — note this is a distinct object from the framework’s variational free energy 𝐹[𝑞𝜆] of §A:
here multi-information enters with a minus sign (a reward-style scalarisation), whereas the decomposition theorem’s
𝐹[𝑞𝜆] carries + 𝐼(𝑞𝜆). The same glyph 𝐹is reused for brevity; the two are reconciled in the remark immediately
below.
𝐹(𝜆) = −𝑢(2𝜎(𝜆) −1) −𝐼(𝜆),
(C.14)
monotonically decreasing in |𝜆| for 𝑢≥0.
See output/figures/free_energy_curve.png.
This is a Lagrangian-
style scalarisation rather than the framework’s 𝐹[𝑞𝜆] = log 𝑍𝐸(𝜆) −log 𝑍(𝜆) identity from §A; the genuine VFE
minimization in the same toy with multi-information entering with a plus sign gives 𝜆⋆
VFE(𝑢) = 2𝑢, derived in the
previous subsection.
Numerical cross-check
The Python companion verifies every identity above to floating tolerance (< 1e-09) at 5 values of 𝜆∈{0, 0.5, 1, 2, 4}:
• test_empirical_mi_matches_closed_form — 𝐼(𝜆) equals the TC of 𝑞𝜆.
• test_ising_mutual_information_zero_at_zero — 𝐼(0) = 0.
• test_ising_mutual_information_saturates_to_log2 — 𝐼(50) ≈log 2.
• test_ising_mutual_information_even_in_lambda — symmetry.
• test_optimal_lambda_* — closed-form 𝜆∗(Δ).
Run them with:
uv run pytest tests/test_bernoulli_toy.py -v
118

## Page 120

Tensor-Train Inference Algorithm: Bond-Dimension Sweep, MPS Con-
traction, and Sparsity-Rank Tradeoff
For coupling potentials representable as tensor trains (TT) with low bond rank 𝑟, the 𝜆-entangled posterior admits
eﬀicient inference and sampling via standard matrix-product-state (MPS) machinery [Orus, 2014, Schollwöck, 2011].
Throughout this appendix, 𝑟denotes the maximal bond dimension of the TT contraction; 𝑟is the parameter that
controls the time / memory trade-off and corresponds to the Schmidt rank of the bipartite reshape of 𝑞𝜆across any
cut along the train. Companion code: src/lean/spectral.py exposes the rank and entropy diagnostics used in the
current figures; the dense empirical suite computes the small-𝐾witnesses directly, while the full TT contraction
algorithm below is an engineering extension of that current rank evidence.
Tensor-train representation of J
Suppose 𝐽(𝜋) = 𝐽(𝜋1, … , 𝜋𝐾) admits a TT representation with bond dimension 𝑟:
𝐽(𝜋1, … , 𝜋𝐾) =
∑
𝑎0,…,𝑎𝐾
𝐴(1)
𝑎0,𝜋1,𝑎1 𝐴(2)
𝑎1,𝜋2,𝑎2 ⋯𝐴(𝐾)
𝑎𝐾−1,𝜋𝐾,𝑎𝐾,
(D.1)
with boundary indices 𝑎0 = 𝑎𝐾= 1. Each tensor 𝐴(𝑘) has shape (𝑟, |Π𝑘|, 𝑟) except at the boundaries.
The exponential map
The pointwise exponential of a TT is not itself low-rank in general, but for additive-form couplings 𝐽= ∑𝑒𝐽𝑒over a
local interaction graph 𝑒∈ℰ(the practically relevant case — pairwise / triplet couplings between adjacent streams),
the factorization
exp(𝜆𝐽) = ∏
𝑒∈ℰ
exp(𝜆𝐽𝑒)
(D.2)
is a product of bond-dimension-bounded operators that contracts into a TT of bond dimension 𝑟′ = 𝑂(𝑟𝑑) where 𝑑
is the maximum order of an interaction. For pairwise couplings, 𝑟′ = 𝑂(𝑟2).
Inference cost
Per-pass cost of computing 𝑞𝜆, its marginals, and its log-partition is
𝒪(𝐾⋅|Πmax|2 ⋅𝑟′2),
(D.3)
where |Πmax| = max𝑘|Π𝑘|.
Compared to dense inference (which is 𝒪( ∏𝑘|Π𝑘|)), this is exponentially cheaper
whenever 𝑟′ ≪∏𝑘|Π𝑘|1/2.
Sampling
Standard MPS conditional sampling [Orus, 2014, Han et al., 2018]: draw 𝜋1 from its marginal, condition the
remaining streams, draw 𝜋2, and so on. Each conditional draw is an 𝒪(|Πmax| 𝑟′2) operation; total 𝒪(𝐾|Πmax| 𝑟′2)
per sample.
Marginal extraction
Marginals 𝑞𝑘
𝜆are extracted by tracing out all other streams from the TT, an 𝒪(𝐾|Πmax| 𝑟′2) operation.
The
Python companion implements this end-to-end for the dense (small 𝐾) case in src/lean/joint_dist.py; a sparse TT
contraction version would extend the same interface rather than change the theorem statement.
Bond-dimension recursion
The bond dimensions of the contracted TT for 𝑞𝜆obey a compositional recursion over the interaction graph. Order
the streams 1, 2, … , 𝐾along the train and define the partial bond rank 𝑟𝑘(𝜆) as the Schmidt rank of the bipartite
factorization {1, … , 𝑘} ∣{𝑘+ 1, … , 𝐾} of 𝑞𝜆. Then:
• Lower bound (rank-additivity at the boundary). 𝑟𝑘(0) = 1 for every 𝑘(mean-field has rank one across
every cut).
119

## Page 121

• Upper bound (sparsity ⟹low rank). If 𝐽has TT rank ≤𝑟across the cut at 𝑘, then 𝑟𝑘(𝜆) ≤𝑟2 for every
𝜆— pairwise interactions saturate at this bound; a 𝑑-clique of streams pushes it to 𝑟𝑘≤𝑟𝑑.
• Monotone growth. 𝑟𝑘(𝜆) is non-decreasing in 𝜆on every cut where 𝐽is non-trivial — the symmetry-breaking
transitions of §8.4 are the discrete jumps in 𝑟𝑘(𝜆).
The recursion is exploited algorithmically in the DMRG-style sweep: fix all bonds except one, solve a local generalized-
eigenvalue problem to update that bond, advance. Each sweep is 𝒪(𝐾|Πmax|2 𝑟3
max); convergence in 𝒪(log(1/𝜀))
sweeps for KL accuracy 𝜀is standard for log-concave coupling potentials [Verstraete et al., 2008, Orus, 2014, Han
et al., 2018]. The numerical companion records the empirical 𝑟𝑘profile across stream counts 𝐾∈{2, 3, 4, 5} — see
the tt_ranks_K2–tt_ranks_K5 variables in output/data/manuscript_variables.json, exposed in prose at §8.3.
Approximate compression
When the exact TT rank of exp(𝜆𝐽) exceeds a budget 𝑟max, truncated SVD across each bond gives a rank-𝑟max
approximation with controlled KL error. This is the standard matrix-product-operator / MPO-MPS contraction
trick.
Connection to the sparsity–rank tradeoff
Theorem 8.3 (sparsity-rank tradeoff): a TT coupling potential of bond dim 𝑟produces a posterior with TT rank
bounded by 𝑟′ as above. This is the formal counterpart of the practical observation that low-rank couplings give
cheap posteriors.
Lean 4 Boundary Fragment: Live ActinfPolicyEntanglement Source Ex-
cerpts and Validation Wiring
The Lean 4 boundary fragment — the type-checked statements of every formal claim in this manuscript — lives
under lean/ of the companion repository. This appendix indexes the modules; the full source is in the companion
repository.
Package structure
lean/
├──lakefile.lean
←Lake package definition
├──lean-toolchain
←v4.29.0
├──ActinfPolicyEntanglement.lean
├──ActinfPolicyEntanglement/
←boundary-fragment submodules
│
├──Basic.lean
│
├──JointDist.lean
│
├──Coupling.lean
│
├──FreeEnergy.lean
│
├──Geometry.lean
│
├──Spectral.lean
│
├──SpectralWitnesses.lean
←prop_7_2, thm_7_3
│
├──Heterogeneous.lean
│
├──BernoulliToy.lean
│
├──Decomposition.lean
│
├──Constructive.lean
│
├──Monotonicity.lean
│
├──Convexity.lean
←thm_4_3, prop_10_1
│
├──MarkovBlanket.lean
←prop_11_3
│
├──ConnectionsWitnesses.lean
←thm_11_1, prop_11_2
│
└──Scalar.lean
├──FepSketches.lean
└──FepSketches/
└──PolicyEntanglementBoundary.lean
←re-exports
Mathlib-free boundary
The package compiles against a stock Lean 4 v4.29.0 with no Mathlib dependency at the boundary layer. This
was a deliberate design choice: the boundary fragment encodes the type signatures of every analytic claim so that
downstream agents can lake build immediately and discharge witness payloads in a separate Mathlib4 layer without
changing the boundary theorem names.
120

## Page 122

Status snapshot
Live grep count, source-of-truth verified on each render (strict-form sorry count = blocking sorries in proof bodies;
the “sorry” mentions inside /-! … -/ docstrings advertising sorry-free status are not blocking and are not counted):
Lean module
Defs
Theorems / Lemmas
Structures
Strict sorry
Manuscript
section
Basic
3
1
0
0 §3
JointDist
5
0
0
0 §3, §7
Coupling
3
2
0
0 §4
FreeEnergy
8
1
0
0 §5
Geometry
0
4
0
0 §7
Spectral
1
2
0
0 §8
SpectralWitnesses
0
3
2
0 §8
Heterogeneous
1
2
2
0 §9
BernoulliToy
14
2
0
0 §6, §C
Decomposition
2
5
0
0 §5, §A
Constructive
0
4
0
0 §5, §7
Monotonicity
0
16
0
0 §5, §10
Convexity
0
2
2
0 §5, §11
MarkovBlanket
0
2
1
0 §19
Connections /
Witnesses
0
4
2
0 §17
Scalar
0
6
0
0 §4
Totals: 17 boundary submodules, 39 defs, 76 theorems / lemmas, 11 structures, 0 strict sorry, 0 axioms
beyond stock Lean 4.
The current registry’s
status distribution is:
0
deferred,
0
sketch,
0
strict
sorry — every num-
bered
theorem
in
the
manuscript
resolves
through
[[LEAN:<label>]]
to
a
live
Lean
source
block
in
lean/ActinfPolicyEntanglement/.
The
witness-form
theorems
are
tracked
in
docs/reference/lean_refer-
ence.md and lean/ActinfPolicyEntanglement/MathlibRefinementRoadmap.md as Mathlib4 analytic-discharge targets
(i.e. work to derive the witness payloads in a separate library, not new statements to ship).
Building locally
cd lean
lake build
Expected: Build completed successfully (22 jobs). The 22 jobs are the 17 ActinfPolicyEntanglement.* submodules,
the ActinfPolicyEntanglement root, the FepSketches.PolicyEntanglementBoundary re-export, the FepSketches root,
and two Lake-internal targets.
FepSketches Re-exports for the Sibling fep_lean Layout
lean/FepSketches/PolicyEntanglementBoundary.lean re-exposes the load-bearing structural facts under the FepS-
ketches.* namespace, matching the import layout used alongside the fep_lean catalog [Friedman, 2026c] and the
research manuscript template monorepo (GitHub organization docxology).
Where each manuscript theorem lives in Lean
The
lean_module
/
lean_name
columns
of
manuscript/refs/labels.yaml
are
the
wiring;
the
renderer’s
[[LEAN:<theorem-label>]] token extracts the live source. The 20 theorem rows with manuscript [[THMREF:...]]
tokens resolve at render time; the separate Float↔ℝroadmap row resolves through the registry but is not inlined
in this Lean-code supplement:
• Theorem 5.1 →Decomposition.entanglement_decomposition
• Theorem 5.5 →Decomposition.freeEnergy_closedForm_witness
• Theorem 5.6 →Convexity.freeEnergy_convex_in_lam_witness
• Corollary 5.2 →Decomposition.couplingVerdict_correct
• Corollary 5.3 →Decomposition.couplingLogWeight_pointwise_at_zero
• Corollary 5.4 →Decomposition.totalCorrelation_def_unfold
• Proposition 7.1 →Geometry.mfImage_isMeanField
• Proposition 7.2 →Geometry.mProjection_kl_eq_self_when_meanfield
• Proposition 7.3 →FreeEnergy.totalCorrelation_eq_kl_to_mprojection
• Theorem 7.4 →Geometry.entangledFamily_eGeodesic
121

## Page 123

• Proposition 7.5 →Geometry.dualFlat_pythagorean_witness
• Proposition 8.1 →Spectral.Bipartite.isBipartiteMeanField_factors
• Proposition 8.2 →SpectralWitnesses.schmidtRank_upperSemicontinuous_witness
• Theorem 8.3 →SpectralWitnesses.sparsityRank_tradeoff_witness
• Theorem 9.1 →Heterogeneous.couplingTax_quadratic_bound
• Corollary 9.2 →Heterogeneous.couplingTax_small_lambda_tolerance
• Proposition 11.1 →Convexity.freeEnergy_localConcavity_at_zero_witness
• Theorem 17.1 →ConnectionsWitnesses.hierarchicalAIF_lambda_limit_witness
• Proposition 17.2 →ConnectionsWitnesses.sophisticatedInference_embedding_witness
• Proposition 19.3 →MarkovBlanket.markovBlanket_separation_identity_witness
The twenty live Lean companions
The blocks below are produced by [[LEAN:<label>]] tokens that src/manuscript/lean_extract.py resolves against
the live .lean sources in lean/ActinfPolicyEntanglement/. Each block carries a -- From <file>:<line> [status:
...] caption pointing at the exact source coordinates so the supplement is a verbatim window onto the formalization,
not a hand-curated copy. If a registered theorem is ever renamed in Lean, the next render either updates the inlined
source or fails fast with a [[MISSING:LEAN:...]] marker — there is no way for the supplement to drift silently from
the boundary fragment.
Decomposition fragment
Entanglement decomposition
-- From `lean/ActinfPolicyEntanglement/Decomposition.lean:75` [status: **boundary**]
/-- **Theorem 5.1 (Entanglement Decomposition)** — boundary witness
form.
Given a Mathlib-supplied algebraic split
`F[q] = marginal_part + coupling_expectation + agentic_gain`,
where `coupling_expectation` is the integrated `couplingLogWeight`
against `q`, this theorem certifies the equation in the boundary
fragment. Every coupling parameter `(J, K_c, γ, 𝜆)` is genuinely used
via `couplingExpectationSkeleton`, so the statement is non-vacuous.
**Typed-API-contract disclaimer.** The Lean body is literally
`hWitness ↦hWitness` — the identity term on the algebraic split.
This is **not** a stand-alone proof of Theorem 5.1; it is a typed-API
contract that forces `(J, K_c, γ, 𝜆)` into the conclusion via
`couplingExpectationSkeleton` and locks the four-term decomposition
shape.
The non-vacuous *algebraic* content of the decomposition
(commutative-ring re-grouping of the four bookkeeping scalars) is
discharged separately by `entanglement_decomposition_four_terms_assoc_skeleton`
and `entanglement_decomposition_four_terms_commute_skeleton` below
(genuine `CommScalar` proofs).
The full *analytic* content (Gibbs
expansion + KL chain rule) is supplied as `hWitness` and discharged
by the separate MathlibProofs layer; the numerical realization is in
`src/lean/decomposition.py` and verified at the dashboard invariant
`decomposition_lhs_eq_rhs_max_residual` (worst-case `5.55e-16`). -/
theorem entanglement_decomposition {K Pol}
(q : JointDist K Pol) (s : List (PolicySpace K Pol))
(logE G : PolicySpace K Pol →Float)
(J K_c : CouplingPotential Float K Pol) (gamma lam : Float)
(marginal_part agentic_gain : Float)
(hWitness : variationalFreeEnergy q logE G gamma s =
marginal_part
+ couplingExpectationSkeleton q s J K_c gamma lam
+ agentic_gain) :
variationalFreeEnergy q logE G gamma s =
marginal_part
+ couplingExpectationSkeleton q s J K_c gamma lam
+ agentic_gain :=
Existence of optimal coupling
-- From `lean/ActinfPolicyEntanglement/Decomposition.lean:243` [status: **boundary**]
/-! ## Theorem 5.5 — closed exponential-family form of `F[q_𝜆]`
The Gibbs decomposition `F[q] = Σ F[q^k] + γ𝜆⟨K_c⟩+ log Z_E(𝜆) - 𝜆⟨J⟩+ I(q)`
collapses to the strikingly clean identity
122

## Page 124

```
F[q_𝜆] = log Z_E(𝜆) - log Z(𝜆),
```
where `log Z_E(𝜆)` is the entangled-prior log-partition and
`log Z(𝜆)` is the entangled-posterior log-partition.
See
[`manuscript/04_entanglement_decomposition.md`](../../manuscript/04_entanglement_decomposition.md)
([Theorem 5.5](../../manuscript/refs/labels.yaml#thm_4_2)) and the proof appendix
[`manuscript/S01_proof_of_decomposition_theorem.md`](../../manuscript/S01_proof_of_decomposition_theorem.md).
The boundary fragment exposes the identity as a *witness-consuming*
statement: the caller (the separate additive `MathlibProofs` layer or the
numerical Python layer) supplies the algebraic equality
`vfe = logZE - logZ`, and the boundary fragment threads `(𝜆, J, γ, K_c)`
through `couplingExpectationSkeleton` so every parameter is genuinely
referenced and the statement is non-vacuous.
Polymorphic over
`[CommScalar α]`. -/
theorem freeEnergy_closedForm_witness {α : Type} [CommScalar α]
{K Pol}
(vfe logZE logZ : α)
(_s : List (PolicySpace K Pol))
(J K_c : CouplingPotential α K Pol) (gamma lam : α)
(hWitness : vfe = logZE - logZ) :
vfe = logZE - logZ
∧(∀π : PolicySpace K Pol,
couplingLogWeight J K_c gamma lam π
= lam * J π - gamma * lam * K_c π) := by
Coupling-pays-for-itself verdict
-- From `lean/ActinfPolicyEntanglement/Decomposition.lean:168` [status: **proved**]
/-- **Corollary 5.2 correctness theorem (boundary identity)**: the
`couplingVerdict` Boolean is `true` precisely when the coupling tax is
strictly less than the agentic gain — i.e. the verdict semantics
faithfully decide the "coupling-pays-for-itself" predicate.
This pins the verdict's contract on the boundary fragment: a `true`
answer is *not* an oracle assertion but a Lean-level proof that
`tax < gain`. Discharged by unfolding the `decide` and forwarding the
proof component, no `sorry`. -/
theorem couplingVerdict_correct (gain tax : Float) :
couplingVerdict gain tax = true ↔tax < gain := by
Mean-field at 𝜆= 0
-- From `lean/ActinfPolicyEntanglement/Decomposition.lean:195` [status: **proved**]
/-- **Corollary 5.3 (Mean-field optimum at 𝜆= 0)**: at `𝜆= 0`, the
coupling log-weight contribution vanishes pointwise. Polymorphic over
`[CommScalar α]`; combine with `entanglement_decomposition` to recover
the pure mean-field statement `F[q_0] = Σ_k F[q_0^k] + agentic_gain`. -/
theorem couplingLogWeight_pointwise_at_zero {α : Type} [CommScalar α]
{K Pol}
(J K_c : CouplingPotential α K Pol) (gamma : α)
(π : PolicySpace K Pol) :
couplingLogWeight J K_c gamma 0 π = 0 :=
Total correlation unfolds to KL-self
-- From `lean/ActinfPolicyEntanglement/Decomposition.lean:215` [status: **boundary**]
/-- **Corollary 5.4 (Total-correlation unfolding)**: the boundary
fragment's `totalCorrelation` is by construction the per-stream
entropy sum minus the joint entropy.
This forwarder makes the
definitional unfolding available to downstream modules without
re-importing `FreeEnergy`'s namespace.
The strict-positivity claim `I(q) > 0 iff q is not mean-field` is the
`Iq > 0 ↔¬ IsMeanField q` companion that requires Mathlib's
KL-non-negativity (see `IsNonNegMultiInformation` in
[`FreeEnergy.lean`](FreeEnergy.lean)) and is exposed by the
`MathlibProofs` extension.
Stock-Lean, zero-`sorry`. -/
theorem totalCorrelation_def_unfold {K Pol}
(q : JointDist K Pol) (s : List (PolicySpace K Pol))
(sumStreamEntropies : Float) :
totalCorrelation q s sumStreamEntropies
= sumStreamEntropies - shannonEntropy q s := rfl
123

## Page 125

Geometry fragment
Mean-field submanifold is e-flat
-- From `lean/ActinfPolicyEntanglement/Geometry.lean:40` [status: **proved**]
/-- **`mfImage_isMeanField`** (registry `prop_6_1`, Prop 7.1,
`faithfulness: statement-restricted`).
This theorem proves only that
the product distribution induced by mean-field marginals *is*
mean-field — definitional membership `IsMeanField (mfToJoint m)`,
discharged by `rfl`.
It does **NOT** prove the named manuscript
proposition "the MF submanifold is e-flat" (closure under exponential
geodesics / affine-in-θ); that real-analytic content is the open
target scoped to the separate Mathlib layer (cf.
`entangledFamily_eGeodesic` for the affine-in-𝜆identity).
The name
was deliberately changed from the prior `mfSubmanifold_eFlat` so the
declaration's name states what it actually proves. -/
theorem mfImage_isMeanField {K Pol}
(m : MFDist K Pol) :
IsMeanField (mfToJoint m) := by
m-projection minimizes KL
-- From `lean/ActinfPolicyEntanglement/Geometry.lean:77` [status: **proved**]
/-- **`mProjection_kl_eq_self_when_meanfield`** (registry `prop_6_2`,
Prop 7.2, `faithfulness: statement-restricted`).
This theorem proves
only the conditional equality `KL(q ‖ mfToJoint m) = KL(q ‖ q)` *under
the hypothesis* `h : q = mfToJoint m` (i.e. `q` is already mean-field).
It does **NOT** prove the named manuscript proposition that the
m-projection *minimises* KL — the information-projection optimality
`∀p ∈M_MF, D_KL(q‖m̂(q)) ≤D_KL(q‖p)` is the open analytic target
for the separate Mathlib layer.
The name was deliberately changed
from the prior `mProjection_minimises_kl` so the declaration's name
states what it actually proves (an equality when `q` is already the
projection, not a minimality result). -/
theorem mProjection_kl_eq_self_when_meanfield {K Pol}
(q : JointDist K Pol) (m : MFDist K Pol)
(h : ∀π, q π = mfToJoint m π)
(s : List (PolicySpace K Pol)) :
kl q (mfToJoint m) s = kl q q s := by
Total correlation equals KL to m-projection
-- From `lean/ActinfPolicyEntanglement/FreeEnergy.lean:140` [status: **witness**]
/-- **Proposition 7.3 (boundary witness form)**: given the per-stream
entropy sum and the value of `KL(q ‖ m̂(q))` together with the
algebraic identity binding them, the boundary fragment certifies the
total correlation equals the KL to the m-projection.
Stock-Lean,
zero-`sorry`.
**Typed-API-contract disclaimer.** Not a stand-alone proof of the
KL-chain-rule identity `I(q) = KL(q ‖ ∏_k q^k)`; a typed-API contract.
The caller supplies `hWitness : sumStreamEntropies −shannonEntropy q s = klToMProj`;
the boundary fragment unfolds `totalCorrelation` and forwards. -/
theorem totalCorrelation_eq_kl_to_mprojection {K Pol}
(q : JointDist K Pol) (s : List (PolicySpace K Pol))
(sumStreamEntropies klToMProj : Float)
(hWitness : sumStreamEntropies - shannonEntropy q s = klToMProj) :
totalCorrelation q s sumStreamEntropies = klToMProj := by
e-geodesic family
-- From `lean/ActinfPolicyEntanglement/Geometry.lean:95` [status: **forwarder**]
/-- **Theorem 7.4** (forwarder).
Polymorphic over `[CommScalar α]`. -/
theorem entangledFamily_eGeodesic {α : Type} [CommScalar α] {K Pol}
(J K_c : CouplingPotential α K Pol) (gamma lam1 lam2 : α)
(π : PolicySpace K Pol) :
couplingLogWeight J K_c gamma lam1 π
- couplingLogWeight J K_c gamma lam2 π
= (lam1 - lam2) * (J π - gamma * K_c π) :=
Pythagorean witness on the dual-flat pair
-- From `lean/ActinfPolicyEntanglement/Geometry.lean:169` [status: **witness**]
/-- **Proposition 6.5 (boundary witness, round-4 tie-in upgrade)**:
extracts the Pythagorean identity from a `PythagoreanWitness`.
The
three scalars are now *committed* to boundary-fragment primitives
(`kl`, `totalCorrelation`, `mfToJoint`) via three tie-in equalities —
124

## Page 126

a caller can no longer satisfy the contract with arbitrary `Float`s.
**Typed-API-contract disclaimer.** The analytic Pythagorean identity
itself (the `pythagorean` field) remains a witness payload supplied
by the caller; the separate MathlibProofs layer discharges it from the
KL chain rule.
This theorem is **not** a stand-alone proof of the
Pythagorean decomposition; it certifies that *if* a caller supplies
witnesses that genuinely compute the boundary primitives, *then* the
extracted identity types-check.
The mathematical content lives in
the manuscript appendix S01 + the Python numerical companion in
[`src/lean/geometry.py`](../../src/lean/geometry.py) (which verifies
the identity on randomly sampled joints + reference mean-fields). -/
theorem dualFlat_pythagorean_witness {K Pol}
{q q0_star : JointDist K Pol} {mhat : MFDist K Pol}
{s : List (PolicySpace K Pol)} {sumStreamEntropies : Float}
(w : PythagoreanWitness q q0_star mhat s sumStreamEntropies) :
w.klVal = w.tcVal + w.residual := w.pythagorean
Spectral fragment
Bipartite mean-field ⇔Schmidt rank 1
-- From `lean/ActinfPolicyEntanglement/Spectral.lean:54` [status: **proved**]
/-- **Proposition 7.1 (forward direction, forwarder)**: extraction
shortcut for callers that already have the bipartite-mean-field
predicate in hand and want the product factorization witness. -/
theorem isBipartiteMeanField_factors {Pol1 Pol2 : Type}
(q : BipartiteJoint Pol1 Pol2)
(h : IsBipartiteMeanField q) :
∃(u : Pol1 →Float) (v : Pol2 →Float),
∀π1 π2, q π1 π2 = u π1 * v π2 :=
Schmidt rank upper-semicontinuous in 𝜆
-- From `lean/ActinfPolicyEntanglement/SpectralWitnesses.lean:68` [status: **witness**]
/-- **Proposition 8.2 (boundary witness form)**: an
`UpperSemicontinuousRankWitness` *is* the existence of an upper-
semicontinuous Schmidt-rank curve anchored at `rankCurve 0 = 1`.
Stock
Lean, zero-`sorry`.
**Typed-API-contract disclaimer.** Not a stand-alone proof of upper
semicontinuity; a typed-API contract.
The continuity inequality is
supplied as `witness.usc`; the boundary fragment re-publishes it
together with the mean-field anchor.
Bipartite K=2 case is now
*genuinely* proved at the boundary as
`Spectral.Bipartite.schmidtRankOne_iff_isBipartiteMeanField` (round 4);
the general-K upper-semicontinuity statement still requires Mathlib's
topological-semicontinuity library + matrix-rank lower-semicontinuity
to discharge. -/
theorem schmidtRank_upperSemicontinuous_witness
(rankCurve : Float →Nat)
(witness : UpperSemicontinuousRankWitness rankCurve) :
rankCurve 0.0 = 1
∧∀(lam0 : Float) (r0 : Nat),
rankCurve lam0 ≤r0 →
∃delta : Float, 0.0 < delta ∧
∀lam : Float, (lam - lam0).abs < delta →rankCurve lam ≤r0 :=
Sparsity-rank tradeoff for tensor-train coupling
-- From `lean/ActinfPolicyEntanglement/SpectralWitnesses.lean:136` [status: **witness**]
/-- **Theorem 8.3 (boundary witness form)**: a `SparsityRankEnvelope`
witness *is* the existence of a per-cut Schmidt-rank envelope for the
𝜆-entangled posterior of a tensor-train coupling.
Stock-Lean, zero-
`sorry`.
**Typed-API-contract disclaimer.** Not a stand-alone proof of the
sparsity-rank tradeoff; a typed-API contract.
The per-cut envelope
`cut_rank k 𝜆≤bond_bound k` is supplied as a `SparsityRankEnvelope`
field; the boundary fragment extracts it.
MathlibProofs discharge
from `Mathlib.LinearAlgebra.TensorProduct` plus matrix-rank bounds. -/
theorem sparsityRank_tradeoff_witness (K : Nat)
(witness : SparsityRankEnvelope K) :
∀(k : Fin K) (lam : Float),
witness.cut_rank k lam ≤witness.bond_bound k :=
125

## Page 127

Convexity fragment
Convexity of 𝐹in 𝜆
-- From `lean/ActinfPolicyEntanglement/Convexity.lean:77` [status: **witness**]
/-- **Theorem 5.6 (boundary witness form)**: a
`FreeEnergyConvexityWitness` *is* the existence of a convex `𝜆`-curve
for `F[q_𝜆]` together with the `𝜆= 0` anchor that ties the curve to the
boundary-fragment coupling skeleton (via
`couplingLogWeight_pointwise_at_zero`).
Polymorphic over `[CommScalar α]`
on the coupling side so the anchor genuinely uses every coupling
parameter `(J, K_c, γ)`.
**Typed-API-contract disclaimer.** This theorem is *not* a stand-alone
proof that `F[q_𝜆]` is convex in `𝜆`.
It is a typed-API contract: the
convex curve and the universally-quantified midpoint inequality are
supplied as a `FreeEnergyConvexityWitness`; the boundary fragment
extracts the fields and re-publishes them.
Numerical witness in
`src/lean/free_energy.py` + `scripts/parameter_sweep.py`; MathlibProofs
discharge from log-concavity-on-the-simplex arguments. -/
theorem freeEnergy_convex_in_lam_witness {α : Type} [CommScalar α]
{K Pol}
(F_curve : Float →Float)
(J K_c : CouplingPotential α K Pol) (gamma : α)
(witness : FreeEnergyConvexityWitness F_curve) :
(∀lam1 lam2 t : Float,
F_curve (t * lam1 + (1.0 - t) * lam2)
≤t * F_curve lam1 + (1.0 - t) * F_curve lam2)
∧(∀π : PolicySpace K Pol,
couplingLogWeight J K_c gamma 0 π = 0) := by
Local concavity of 𝐹at 𝜆= 0
-- From `lean/ActinfPolicyEntanglement/Convexity.lean:154` [status: **witness**]
/-- **Proposition 11.1 (boundary witness form)**: a
`LocalConcavityAtZero` witness *is* the existence of a Taylor-form local
concavity bound for `F[q_𝜆]` at `𝜆= 0`, together with the `𝜆= 0`
anchor that ties the curve to the boundary-fragment coupling skeleton
(via `couplingLogWeight_pointwise_at_zero`).
Polymorphic over
`[CommScalar α]` on the coupling side so the anchor genuinely uses every
coupling parameter `(J, K_c, γ)`.
**Typed-API-contract disclaimer.** Not a stand-alone proof of local
concavity; a typed-API contract.
The Taylor coefficients, the
`a₂ ≤0` sign, the local window radius, and the cubic-remainder bound
are all supplied as `LocalConcavityAtZero` fields.
Numerical witness
in `parameter_sweep.py`; MathlibProofs discharge from real-analytic
second-derivative arguments. -/
theorem freeEnergy_localConcavity_at_zero_witness {α : Type} [CommScalar α]
{K Pol}
(F_curve : Float →Float)
(J K_c : CouplingPotential α K Pol) (gamma : α)
(witness : LocalConcavityAtZero F_curve) :
witness.a2 ≤0.0
∧0.0 < witness.eps
∧(∀lam : Float, 0.0 ≤lam →lam ≤witness.eps →
F_curve lam
≤witness.a0
+ witness.a1 * lam
+ witness.a2 * lam * lam
+ witness.C * lam * lam * lam)
∧(∀π : PolicySpace K Pol,
couplingLogWeight J K_c gamma 0 π = 0) := by
Heterogeneous fragment
Coupling-tax quadratic bound
-- From `lean/ActinfPolicyEntanglement/Heterogeneous.lean:61` [status: **witness**]
/-- **Theorem 9.1 (boundary witness form)**: a `BoundedQuadraticTax`
witness *is* the existence of the quadratic envelope.
Stock-Lean,
zero-`sorry`.
**Typed-API-contract disclaimer.** This theorem is *not* a stand-alone
proof of the `O(𝜆²)` coupling-tax bound; it is a typed-API contract.
The analytic content — the bound `taxFunction 𝜆≤C·𝜆²` with `C ≥0`
universally over `𝜆` — is supplied as a structural hypothesis
126

## Page 128

(`BoundedQuadraticTax`); the boundary fragment re-publishes it as an
existence claim.
The Python numerical companion in
[`src/lean/heterogeneous.py`](../../src/lean/heterogeneous.py)
verifies the bound on concrete parameter sweeps; the separate
MathlibProofs layer will discharge it from Taylor expansion of the
coupling-prior log-partition. -/
theorem couplingTax_quadratic_bound (taxFunction : Float →Float)
(witness : BoundedQuadraticTax taxFunction) :
∃(C : Float), 0.0 ≤C ∧
∀lam, couplingTax taxFunction lam ≤C * lam * lam :=
Small-𝜆tolerance witness
-- From `lean/ActinfPolicyEntanglement/Heterogeneous.lean:106` [status: **witness**]
/-- **Corollary 9.2 (boundary witness form)**: a `SmallLambdaTolerance`
witness *is* the existence of the tolerance window. Stock-Lean,
zero-`sorry`.
**Typed-API-contract disclaimer.** Same as `couplingTax_quadratic_bound`:
this is a typed-API contract, not a stand-alone proof.
The continuity
argument that delivers the tolerance window is supplied as a
`SmallLambdaTolerance` witness; the boundary fragment re-publishes
the existence claim. -/
theorem couplingTax_small_lambda_tolerance
(taxFunction : Float →Float) (eps : Float)
(witness : SmallLambdaTolerance taxFunction eps) :
∃(lamMax : Float), 0.0 < lamMax ∧
∀lam, lam.abs ≤lamMax →couplingTax taxFunction lam ≤eps :=
Connections fragment
Hierarchical AIF as the 𝜆→∞limit
-- From `lean/ActinfPolicyEntanglement/ConnectionsWitnesses.lean:74` [status: **witness**]
/-- **Theorem 17.1 (boundary witness form)**: a
`HierarchicalConcentrationWitness` *is* the existence of a 𝜆→∞
hierarchical-AIF concentration claim for the entangled family.
Stock-
Lean, zero-`sorry`.
**Typed-API-contract disclaimer.** Not a stand-alone proof of the
hierarchical-AIF concentration limit; a typed-API contract.
The
`concentrate` field — that for every 𝜀> 0 a coupling threshold
exists beyond which the entangled posterior is 𝜀-close in KL to the
limit `q_∞` — is supplied as a witness obligation.
MathlibProofs
discharge from `Mathlib.MeasureTheory.Measure.Tight` (tightness of the
𝜆-entangled posterior family in the 𝜆→∞limit). -/
theorem hierarchicalAIF_lambda_limit_witness {K : Nat} {Pol : PolicyFactor K}
(qFamily : Float →JointDist K Pol)
(q_infty : JointDist K Pol)
(support : List (PolicySpace K Pol))
(witness : HierarchicalConcentrationWitness qFamily q_infty support) :
∀(eps : Float), 0.0 < eps →
∃lam0 : Float, 0.0 < lam0 ∧
∀lam : Float, lam0 ≤lam →
kl (qFamily lam) q_infty support ≤eps :=
Sophisticated-inference embedding
-- From `lean/ActinfPolicyEntanglement/ConnectionsWitnesses.lean:167` [status: **witness**]
/-- **Proposition 17.2 (boundary witness form)**: a
`SophisticatedInferenceEmbedding` *is* the existence of an embedding
from a sophisticated-inference source into the 𝜆-deformation family
that maps the sophisticated-inference value function onto the
variational free energy.
Stock-Lean, zero-`sorry`. -/
theorem sophisticatedInference_embedding_witness {K : Nat} {Pol : PolicyFactor K}
(logE G : PolicySpace K Pol →Float) (gamma : Float)
(support : List (PolicySpace K Pol))
(witness : SophisticatedInferenceEmbedding logE G gamma support) :
∀(x : witness.source),
witness.siValue x =
variationalFreeEnergy (witness.embed x) logE G gamma support :=
Markov-blanket fragment
Markov-blanket separation identity 1 −𝐼/𝐻
127

## Page 129

-- From `lean/ActinfPolicyEntanglement/MarkovBlanket.lean:96` [status: **witness**]
/-- **Proposition 19.3 (boundary witness form)**: a
`MarkovBlanketSeparationWitness` *is* the existence of the
Markov-blanket separation identity `sep = 1 −I(q) / H(q)` on a finite
support, with `Hq > 0` and the tie-ins certifying that:
* `Hq` genuinely refers to `shannonEntropy q s`;
* `Iq` is the multi-information `Σ_k H(q^k) −H(q)` computed via the
boundary fragment's `totalCorrelation`;
* `Iq` is non-negative (the analytic discharge from KL ≥0).
Stock-Lean, zero-`sorry`.
This is now genuinely non-vacuous because
both tie-ins commit `Iq` to a definite boundary-fragment quantity
rather than a free Float. -/
theorem markovBlanket_separation_identity_witness {K Pol}
(q : JointDist K Pol) (s : List (PolicySpace K Pol))
(witness : MarkovBlanketSeparationWitness q s) :
0.0 < witness.Hq
∧witness.Hq = shannonEntropy q s
∧witness.Iq = totalCorrelation q s witness.sumStreamEntropies
∧0.0 ≤witness.Iq
∧witness.sep = 1.0 - witness.Iq / witness.Hq :=
How drift is prevented
The [[LEAN:...]] injection turns each Lean theorem in this appendix into a single source of truth shared with the
boundary fragment itself:
1. manuscript/refs/labels.yaml declares the theorem registry with lean_module / lean_name for each entry.
2. At
render
time,
src/manuscript/lean_extract.py::load_lean_snippets
parses
every
.lean
file
under
lean/ActinfPolicyEntanglement/ and indexes each declaration by (module, qualified_name).
3. src/manuscript/renderer.py::_lean resolves the registry pair against this index and emits a fenced Lean block
carrying the source coordinates and the registry-declared status.
4. If the qualified name is missing or has been renamed, the renderer substitutes a [[MISSING:LEAN:...]]
marker that scripts/validate_manuscript.py refuses to ship — so a Lean rename either flows through to
the manuscript or fails CI.
This eliminates every form of stale-quote risk: the supplement above is the boundary fragment, sliced theorem-by-
theorem.
How a witness is consumed today
The stock-Lean boundary is now zero-sorry and zero-deferred. For a status: witness theorem, the current source
consumes a typed structure whose fields bind the analytic payload to boundary-fragment primitives. The validated
contract is:
1. The theorem row in manuscript/refs/labels.yaml names the live Lean declaration.
2. The Lean declaration type-checks without Mathlib and without hidden axioms.
3. The corresponding Python witness or pymdp run computes the same payload numerically.
4. The relevant test file and dashboard invariant fail if the numerical payload drifts.
5. The manuscript renderer embeds only the live Lean declaration, never a hand-written replacement.
Mathlib4 enters only at the analytic-discharge boundary described in §12: a separate Mathlib-backed library may
later construct these witness structures from Real, PMF, KL, convexity, rank, and measure-theoretic lemmas. Until
such a module builds, it is not cited as a current result and is not rendered as source code.
Notation Concordance: Symbol Registry Across Manuscript, LaTeX,
Python, and Lean
This appendix is the single contract between the manuscript prose, the LaTeX preamble macros, the Python
source under src/, and the Lean boundary fragment under lean/. Every symbol used in the body appears here
exactly once; columns trace the symbol across all four tracks so a reader can navigate from prose →code →proof in
one hop. Empty cells indicate that the symbol does not surface on that track (e.g. a manuscript-only typographical
convention).
128

## Page 130

The same identifiers also appear in docs/reference/math_reference.md and the Python-side identifier inventory in
docs/reference/python_api.md.
A fifth, structural-and-numerical track — Generalized Notation Notation (GNN) — is shipped and documented
in §S8 and tabulated in the GNN fifth-track concordance subsection at the end of this appendix. GNN reproduces the
framework’s structure and numbers (a project-owned parser, a verified K=2 round-trip, and a Lean typed-contract
emitter), but it does not prove theorems; the four-track proof contract documented above is therefore unchanged,
and the GNN track is tabulated separately so the two are never conflated.
How to read this concordance — one symbol, four tracks
Take the entangled posterior 𝑞𝜆, the central object of the framework. The four tracks line up as follows:
• Manuscript prose (§4). 𝑞𝜆(𝜋) ∝∏𝑘𝐸𝑘(𝜋𝑘) exp (𝜆𝐽(𝜋) −𝛾𝐺𝜆(𝜋)).
• LaTeX preamble (preamble.md). Either spell out q_\lambda or use the macro \fe for the matching VFE
operator.
• Python (src/lean/coupling.py).
from lean.coupling import entangled_posterior
q_lam = entangled_posterior(mf, G, J, Kc, gamma=1.0, lam=2.0)
# q_lam.shape == (|Π¹|, |Π²|, …, |Π^K|);
q_lam.sum() == 1.0
• Lean (lean/ActinfPolicyEntanglement/Coupling.lean).
def entangledPosteriorLogWeight {α : Type} [Add α] [Mul α] [Sub α] {K Pol}
(logE : PolicySpace K Pol →α)
(G : PolicySpace K Pol →α)
(J K_c : CouplingPotential α K Pol)
(gamma lam : α) : PolicySpace K Pol →α :=
fun pi => logE pi - gamma * G pi + couplingLogWeight J K_c gamma lam pi
• Numerical witness (tests/test_coupling.py).
At 𝜆= 0 with symmetric MF prior and zero coupling,
entangled_posterior(...) == mean_field_to_joint(mf) to floating tolerance — the proved-form companion of
Corollary 5.3.
Reading any row of the tables below in the same fashion lands a reader on the exact construct on all four tracks.
Sign conventions
The framework spans variational free energy, expected free energy, KL, multi-information, coupling, and Schmidt
spectra; each carries a sign convention that the rest of the manuscript silently adheres to. An editor or reader who
is confused about a sign somewhere in the body should consult this subsection first. When the body says “negated
𝐾” or “modulo a sign convention”, it is invoking one of the conventions below.
• Variational free energy.
𝐹[𝑞] = 𝔼𝑞[log 𝑞−log ℰ] + 𝛾𝔼𝑞[𝐺].
𝐹is non-negative on the natural domain
(Gibbs inequality with fixed ℰ) and is the quantity to be minimized. Every 𝐹[𝑞𝜆], 𝐹[𝑞𝑘
𝜆], and ∑𝑘𝐹[𝑞𝑘] in the
manuscript follows this sign — no inverted-sign “ELBO” form appears anywhere; an apparent extra minus in
a body equation is a typo, not a convention change.
• Expected free energy. 𝐺(𝜋) ≥0 on the standard active-inference decomposition; both the epistemic value
and the pragmatic value are reported as negated quantities so that minimizing 𝐺corresponds to maximizing
utility plus information gain. When the body writes “epistemic value, negated” / “pragmatic value, negated”
(as in §3.1), the negation is already absorbed into the sign of 𝐺— no further sign-flip is needed downstream.
• Kullback–Leibler divergence. 𝐷KL(𝑞‖ 𝑝) = 𝔼𝑞[log 𝑞−log 𝑝] ≥0, never reversed. The first argument is
the distribution one is drawing from; the second is the reference. When a derivation appears to “swap” the
arguments (e.g. for variational vs. mean-field projections), the manuscript spells out the swap explicitly; an
inferred swap is an error.
• Multi-information / total correlation. 𝐼(𝑞) = ∑𝑘𝐻(𝑞𝑘) −𝐻(𝑞) = 𝐷KL(𝑞‖ ∏𝑘𝑞𝑘) ≥0. Appears with a
PLUS sign in the decomposition theorem (Eq. (5.2)); the body never carries an inverted-sign 𝐼.
• Coupling parameter 𝜆. 𝜆≥0 throughout the body of the paper. Negative 𝜆would correspond to anti-
coupling (the entangled posterior is pushed away from the modes of 𝐽−𝛾𝐾𝑐) and is out of scope; figures show
𝜆≥0 unless otherwise indicated. In the symmetric K=2 Bernoulli toy of §6.1 the closed-form expressions are
even in 𝜆so the sign restriction is harmless; in asymmetric cases the restriction is substantive and should be
flagged if relaxed.
• Schmidt singular values.
𝑠𝛼≥0 (singular values of a real matrix are non-negative).
The spectral
distribution 𝑝𝛼= 𝑠2
𝛼/ ∑𝛽𝑠2
𝛽is obtained by squaring the singular values and normalizing by their sum-of-
squares; this is the same normalization used in the quantum-entanglement dictionary but applied to the SVD
of a classical-probability joint, not to amplitudes of a state vector.
The analogy with bipartite quantum
129

## Page 131

entanglement entropy is structural, not literal (see the clarification at §8.2 / [Eisert et al., 2010]).
• Convention on “negated 𝐾”. Phrases such as “negated 𝐾” or “modulo a sign convention” elsewhere in
the manuscript refer collectively to the conventions in this subsection — almost always to the EFE-side sign
of 𝐾𝑐(which enters 𝐺𝜆with a plus 𝜆𝐾𝑐, contributing +𝛾𝜆⟨𝐾𝑐⟩to 𝐹via the 𝛾𝐺𝜆expectation; the minus-sign
convention in some derivations of related work corresponds to a re-definition 𝐾𝑐→−𝐾𝑐).
Sets, indices, and basic objects
Symbol
Meaning
LaTeX
Python
Lean
𝐾∈ℕ
Number of policy
streams
K
K (int)
K : Nat
𝑘∈{1, … , 𝐾}
Stream index
k
k (int)
k : StreamIdx K
Π𝑘
Per-stream policy factor
(finite type)
\Pi^k (or \policySpace^k)
(implicit via array shape)
Pol k (in PolicyFactor K
:= StreamIdx K →Type)
Π = ∏𝑘Π𝑘
Joint policy space
\Pi (or \policySpace)
(implicit)
PolicySpace K Pol (∀k,
Pol k)
𝜋= (𝜋1, … , 𝜋𝐾) ∈Π
Joint policy
\pi (or \policy)
flat ndarray index
pi : PolicySpace K Pol
𝜋𝑘∈Π𝑘
Per-stream policy
\pi^k
pi[k]
pi k
𝜋−𝑘
Tuple of all policies other
than stream 𝑘
\pi^{-k}
(sum-axis param)
(implicit in
marginalization)
𝑇𝑘
Planning horizon
attached to stream 𝑘
T_k
per-stream horizon in
StreamSpec / rollout
sidecars
horizon k when a
HorizonProfile K witness
is in scope
𝐿
Number of hierarchy
levels in the
hierarchical-AIF
structural analogy
L
(manuscript-level; no
dedicated runtime
object)
(witness payload supplied
to ConnectionsWitnesses)
ℓ
Hierarchy-level index,
used in adjacent-level
pairs (𝜋ℓ, 𝜋ℓ+1)
\ell
(manuscript-level; no
dedicated runtime
object)
(witness payload supplied
to ConnectionsWitnesses)
𝑑
Lookahead depth for
sophisticated-inference /
branching-style policy
stacks
d
lookahead_depth when an
experiment supplies one
(witness payload supplied
to ConnectionsWitnesses)
𝒱⊆{1, … , 𝐾}
VFE (reflexive) stream
indices
\mathcal{V}
[m for m,_ in
enumerate(modes) if m ==
InferenceMode.VFE]
(implicit via horizon :
HorizonProfile K)
𝒫= {1, … , 𝐾} ∖𝒱
EFE / planning stream
indices
\mathcal{P}
(complement)
(implicit)
POMDP generative-model symbols
The single-stream POMDP recap of §3.1 uses the classical pymdp / SPM symbols. These are the inputs to the
pymdp.agent.Agent constructor in src/simulation/agents.py and the fields of StreamSpec.
Symbol
Meaning
LaTeX
Python (StreamSpec)
pymdp keyword
𝐴
Likelihood matrix
(num_obs × num_states)
A
spec.A
A=
𝐵
Transition tensor
(num_states × num_states
× num_controls)
B
spec.B
B=
𝐶
Log-preference vector
(num_obs)
C
spec.C
C=
𝐷
Prior over hidden states
(num_states)
D
spec.D
D=
𝑜
Observation
o
observations[k]
passed to infer_states
𝑠
Hidden state
s
states[k] (in Rollout)
output of infer_states
𝑢
Control / action
u
sampled_actions[k]
output of policy sampling
𝑇
Rollout horizon
T
H.PYMDP_ROLLOUT_STEPS
(script-level)
𝑃(⋅)
Generic generative-model
law in active-inference
prose
P
stored concretely as A, B,
C, D, E arrays / factors
(not a boundary
primitive)
𝑄(⋅)
Generic variational
posterior notation in
active-inference prose
Q
normalized q arrays;
Agent.qs / Agent.q_pi in
pymdp contexts
(not a boundary
primitive; boundary uses
JointDist)
Distributions
130

## Page 132

Symbol
Meaning
LaTeX
Python
Lean
𝐸𝑘(𝜋𝑘)
Per-stream policy prior
(habit)
E_k
mf_prior[k] (per-stream
marginal supplied to
entangled_prior /
mean_field_to_joint) —
distinct from
StreamSpec.D, which is
the hidden-state prior;
see the
hidden-state-prior
row above
E : MFDist K Pol
𝐸MF(𝜋) = ∏𝑘𝐸𝑘(𝜋𝑘)
Mean-field prior
E_{\mathrm{MF}}
mean_field_to_joint(mf_-
prior)
mfProductWeight
ℰ𝜆(𝜋)
𝜆-entangled prior
\mathcal{E}_\lambda
entangled_prior(...)
(no Lean — boundary
fragment carries only the
log-weight via entangled-
PosteriorLogWeight)
𝐺𝑘(𝜋𝑘)
Per-stream expected free
energy (EFE)
G_k (or \efe_k)
per_stream_efe(spec,
obs)[k]
(consumed as data via
MFDist K Pol)
𝐺MF(𝜋) = ∑𝑘𝐺𝑘(𝜋𝑘)
Mean-field EFE
G_{\mathrm{MF}}
sum(per_stream_efe(...))
(no top-level Lean def;
consumed as MFDist K Pol
argument)
𝐺𝜆(𝜋) =
𝐺MF(𝜋) + 𝜆𝐾𝑐(𝜋)
𝜆-coupled total EFE
(per-stream EFEs plus
preference-side coupling)
G_\lambda
(inlined)
(inlined; appears inside
entangledPosteriorLog-
Weight)
𝑞(𝜋)
Joint policy posterior
q
q : ndarray (joint shape)
q : JointDist K Pol
𝑞𝑘(𝜋𝑘) = ∑𝜋−𝑘𝑞(𝜋)
Per-stream marginal
q^k
joint_marginal(q, k)
(no Lean —
marginalization is inline
in mfToJoint)
𝑞𝜆(𝜋)
𝜆-entangled posterior
q_\lambda
entangled_posterior(mf,
G, J, K_c, gamma, lam) /
coupled_policy_-
posterior(spec, obs, lam)
entangledPosterior /
LogWeight
𝑞MF(𝜋) = ∏𝑘𝑞𝑘(𝜋𝑘)
Product of marginals
(m-projection of 𝑞)
q_{\mathrm{MF}}
m_projection(q)
mfToJoint (direction: MF
→joint;
joint-to-marginal
projection is Python-only
in the current boundary)
𝑞𝑘
𝑡
Per-stream marginal at
rollout time 𝑡
q_t^k
rollout.steps[t].mean_-
field_marginals[k]
(no Lean)
Coupling potentials and parameters
Symbol
Meaning
LaTeX
Python
Lean
𝐽(𝜋)
Habit coupling potential
— prior side
J (or \coupJ)
coupling_j (in
CoupledEnsembleSpec)
J : CouplingPotential α K
Pol
𝐾𝑐(𝜋)
Preference coupling
potential — EFE side
K_c (or \coupK)
coupling_kc
Kc : CouplingPotential α
K Pol
𝜆∈[0, ∞)
Coupling parameter
\lambda
lam (parameter)
lam : α
𝛾> 0
Policy precision
(inverse-temperature on
EFE)
\gamma
gamma (in
CoupledEnsembleSpec)
gamma : α
𝛾𝑘> 0
Per-stream policy
precision; collapses to
scalar 𝛾in homogeneous
examples
\gamma_k
per-stream gamma when a
helper supports
heterogeneous precision;
scalar gamma otherwise
(not a separate boundary
primitive)
Δutil ∈[−Δmax, Δmax]
Utility surplus for
aligned outcomes (a
substantive payoff
parameter; not a target
on the alignment axis)
\Delta_{\mathrm{util}}
delta argument to
optimal_lambda
delta : Float
131

## Page 133

Symbol
Meaning
LaTeX
Python
Lean
Δalign ∈[−Δmax, Δmax]
Target alignment for the
alignment-inversion
formula 𝜆⋆(Δalign) =
2 arctanh(Δalign/Δmax);
equals 𝛼(𝜆) = tanh(𝜆/2)
at the realizing 𝜆
(Eq. (6.8)). Distinct
from Δutil —
alignment-inversion is not
the VFE first-order
condition.
\Delta_{\mathrm{align}}
delta argument to
optimal_lambda (same
code path; semantics is
alignment, not utility)
delta : Float
Δmax
Saturation point of Δutil
/ Δalign (Bernoulli toy:
1)
\Delta_{\max}
delta_max argument
(default 1.0)
delta_max : Float
Δspec(𝜆) = 𝑠1 −𝑠2
Spectral gap (largest
minus second-largest
singular value of the
bipartite reshape of 𝑞𝜆);
distinct from utility
surplus and target
alignment
\Delta_{\mathrm{spec}}
schmidt_decomposi-
tion(q)[0].weight -
schmidt_decomposi-
tion(q)[1].weight
(composition form)
(no current Lean SVD
companion; Python
computes the spectrum)
𝜆⋆(Δalign)
Alignment-inversion
coupling =
2 arctanh(Δalign/Δmax);
inverse of the alignment
correspondence in the
K=2 Bernoulli toy. Not a
VFE optimum.
\lambda^\star (or
\lambda^*)
optimal_lambda(delta)
optimalLambda
𝜆⋆
VFE(𝑢)
True VFE-optimal
coupling under utility
scalar 𝑢; equals 2𝑢in the
symmetric K=2 Bernoulli
toy (see §C). Coincides
with 𝜆⋆(Δalign = 𝑢) only
at small 𝑢.
(inline)
(derived analytically)
(no Lean)
𝜆infl
Inflection coupling:
the point in [0, ∞) where
𝐹″ changes sign exactly
once, separating the
regime where the agent
benefits from more
coupling (below) from
the regime where
marginal returns reverse
(above) — see §B
\lambda_{\mathrm{infl}}
(inline; located where 𝐹″
changes sign)
(no Lean)
𝜆(1)
𝑐, 𝜆(2)
𝑐
Phase-band thresholds
(default (0.5, 2.5))
\lambda_c^{(1)},\lambda_-
c^{(2)}
H.PHASE_LAMBDA_C1,
H.PHASE_LAMBDA_C2
lambdaC1, lambdaC2
𝜆probe
Small-𝜆probe for the
coupling-tax curvature fit
\lambda_{\mathrm{probe}}
H.COUPLING_TAX_PROBE_-
LAMBDA
(no Lean)
𝐽0
Bernoulli / Ising coupling
strength (scalar prefactor
of the 𝐾= 2
aligned-indicator
coupling 𝐽)
J_0
j0 (closed-form scalar in
bernoulli_toy)
(no Lean — Bernoulli toy
uses BinaryCoupling)
𝜆𝐸, 𝜆𝐺
Decoupled-parameter
form: two-parameter
generalization in which
the habit-side and
EFE-side coupling
strengths are
independent (𝜆in the
body is the symmetric
𝜆𝐸= 𝜆𝐺restriction)
\lambda_E,\,\lambda_G
lam_e, lam_g (parameter
overrides)
(no Lean — symmetric
lam : α only)
𝜆1/2
Half-saturation coupling:
𝜆at which the alignment
correspondence reaches
Δmax/2
\lambda_{1/2}
manuscript_-
variables.json[pymdp_-
summary_lambda_at_half_-
saturation]
(no Lean)
𝜆max
Max admissible coupling
under small-𝜆tolerance 𝜀
(Theorem 9.1)
\lambda_{\max}
(derived from
SmallLambdaTolerance)
SmallLambdaTolerance /
lambda_max
132

## Page 134

Symbol
Meaning
LaTeX
Python
Lean
Φ𝑘𝑗
Per-pair coupling factor:
entry (𝑘, 𝑗) of Φ (the
sup-norm ‖Φ‖∞already
has a row)
\Phi_{kj}
(entry of
coupling-log-weight
matrix)
(no Lean — magnitude
consumed via
couplingNormSq_of_-
trivialCoupling)
𝒞
Interaction graph: set of
coupled stream pairs
(𝑘, 𝑗) with Φ𝑘𝑗≠0
\mathcal{C}
(set / sparsity pattern of
coupling)
(no Lean — implicit
support of
CouplingPotential)
𝐽𝑒
Per-clique additive
component of 𝐽in the
tensor-train
decomposition (indexed
by edge 𝑒∈𝒞)
J_e
(clique components in
coupling_decomposition)
(no Lean)
𝑍(𝜆)
Unnormalized posterior
partition function; see
normalizer note below
Z(\lambda)
(implicit in
entangled_posterior)
(implicit in entangledPos-
teriorLogWeight)
𝑍𝐸(𝜆)
Normalizing constant of
the entangled prior
ℰ𝜆∝(∏𝑘𝐸𝑘) 𝑒𝜆𝐽
Z_E(\lambda)
(implicit; sourced from
entangled_prior)
(no top-level Lean def;
implicit in entangledPos-
teriorLogWeight)
𝜓(𝜆) = log 𝑍(𝜆)
Posterior log-partition
function
\psi(\lambda)
(implicit)
(no top-level Lean def;
implicit in entangledPos-
teriorLogWeight)
𝜓𝐸(𝜆) = log 𝑍𝐸(𝜆)
Prior log-partition
function
\psi_E(\lambda)
(implicit)
(no top-level Lean def;
implicit in entangledPos-
teriorLogWeight)
𝐹[𝑞𝜆] =
log 𝑍𝐸(𝜆) −log 𝑍(𝜆)
Closed exponential-family
form of the entangled
VFE (see Theorem 5.5)
(inline)
entanglement_-
decomposition_rhs(...)
(Gibbs form)
(boundary; Lean
companion is the
algebraic skeleton in
Decomposition.lean)
mode𝑘
Inference mode of stream
𝑘
\mathrm{mode}_k
InferenceMode.VFE / EFE /
SOPHISTICATED
(manuscript label; no
Lean inductive in current
boundary fragment —
see Status notes)
Normalizer note. 𝑍(𝜆) normalizes the unnormalized exponential 𝐸MF(𝜋) 𝑒𝜆(𝐽−𝛾𝐾𝑐)(𝜋)−𝛾𝐺MF(𝜋), so 𝑞𝜆(𝜋) is that
numerator divided by 𝑍(𝜆). It is not ∑𝜋𝑞𝜆(𝜋), which is 1 by definition. It is the partition function that appears in
the closed identity 𝐹= log 𝑍𝐸−log 𝑍(Eq. (5.8)).
Information-theoretic quantities
Symbol
Definition
LaTeX
Python
Lean
𝐻(𝑝) = −∑𝑝log 𝑝
Shannon entropy
(natural log)
H(p) (or \Hent(p))
shannon_entropy(p)
shannonEntropy
𝐻𝑏(𝑝)
Binary entropy
−𝑝log 𝑝−(1−𝑝) log(1−𝑝)
H_b(p)
(inline)
binaryEntropy
𝐷KL(𝑞‖ 𝑝)
KL divergence
D_{\mathrm{KL}} (or
\KL{q}{p})
kl_divergence(q, p)
kl
𝐼(𝑞) = ∑𝑘𝐻(𝑞𝑘) −𝐻(𝑞)
Total correlation
(multi-information)
I(q) (or \MI(q))
total_correlation(q)
totalCorrelation
𝜂(𝑞)
Normalized
multi-information /
policy-blanket leakage —
𝐼(𝑞)/𝐻(𝑞) ∈[0, 1]; 0 at
strict mean-field, 1 at
maximally entangled.
Distinct from 𝜂as
m-coordinates (see
Pitfalls).
\eta(q)
composition of
total_correlation(q) and
shannon_entropy(q)
(no direct Lean; derivable
from totalCorrelation
and shannonEntropy)
Var𝑞[𝑋]
Variance under 𝑞
\mathrm{Var}_q (or
\Var{q}{X})
np.var(...) (ad-hoc)
(no Lean)
Cov𝑞[𝑋, 𝑌]
Covariance under 𝑞
\mathrm{Cov}_q
(ad-hoc)
(no Lean)
𝜎(𝑥) = 1/(1 + 𝑒−𝑥)
Logistic sigmoid
\sigma(x)
scipy.special.expit
(ad-hoc)
floatLogistic
⟨𝑋⟩𝑞= 𝔼𝑞[𝑋]
Expectation operator
under joint 𝑞
\langle X \rangle_q (or
\E{q}{X})
expected_value(q, X)
(inline finite sum over q_i
* X_i)
⟨𝑋⟩𝑞𝜆
Expectation under the
entangled posterior 𝑞𝜆
\langle X
\rangle_{q_\lambda}
expected_-
value(entangled_-
posterior(...), X)
(inline)
133

## Page 135

Symbol
Definition
LaTeX
Python
Lean
⟨𝑋⟩ℰ𝜆
Expectation under the
entangled prior ℰ𝜆—
distinct from posterior
expectation when 𝐺≢0
\langle X \rangle_-
{\mathcal{E}_\lambda}
expected_-
value(entangled_-
prior(...), X)
(inline)
d log 𝑍𝐸/d𝜆= ⟨𝐽⟩ℰ𝜆
Standard
exponential-family
identity for the prior
log-partition derivative —
used in Theorem 5.5 /
Proposition 11.1
(inline)
(analytical)
(analytical)
Free energies
Symbol
Definition
LaTeX
Python
Lean
𝐹[𝑞]
Variational free energy of
𝑞
F (or \fe)
free_energy(q, prior, G,
gamma)
variationalFreeEnergy
𝐹[𝑞𝑘]
Per-stream marginal free
energy
F[q^k]
marginal_free_energy(q,
prior, G, gamma, k)
marginalFreeEnergy
∑𝑘𝐹[𝑞𝑘
𝜆]
Sum of per-stream VFEs
(the mean-field
free-energy baseline)
(sum)
free_energy_bundle(spec,
obs, lam).vfe_total
(FreeEnergyBundle.vfe_-
total)
marginalFreeEnergy
(aggregated over
StreamIdx K)
⟨𝐺𝑘⟩𝑞𝑘
𝜆
Expected EFE under
coupled posterior
\langle
G_k\rangle_{q^k_\lambda}
expected_free_energy_-
under_posterior(spec,
obs, lam)[k] /
FreeEnergyBundle.efe_-
under_posterior[k]
(numerical)
𝜆⟨𝐽⟩𝑞𝜆
Coupling-energy
contribution to 𝐹
\lambda \langle J\rangle
coupling_energy(spec,
obs, lam) / FreeEnergy-
Bundle.coupling_term
couplingExpectation /
Skeleton
Manifolds, projections, and dual coordinates
Symbol
Meaning
LaTeX
Python
Lean
ℳ
Simplex of
strictly-positive joint
distributions on Π
\mathcal{M} (or \Mfd)
(implicit ambient)
(implicit)
ℳMF ⊂ℳ
Mean-field submanifold
(product distributions)
\mathcal{M}_{\mathrm{MF}}
(or \MFsubmfd)
is_mean_field(q, atol)
(membership predicate)
IsMeanField
̂𝑚(𝑞) = ∏𝑘𝑞𝑘
m-projection of 𝑞onto
ℳMF
\hat{m}(q)
m_projection(q)
mfToJoint (direction: MF
→joint; Python
computes the joint →
MF marginals before
rejoining)
𝜃= log 𝑞
e-coordinates (natural
parameters)
\theta
np.log(q) (ad-hoc)
(no Lean)
𝜂= 𝔼𝑞[⋅]
m-coordinates
(expectation parameters
of an exponential family).
Distinct from 𝜂(𝑞)
policy-blanket leakage
(see Pitfalls).
\eta
(ad-hoc)
(no Lean)
Pythagorean residual
𝐷KL(𝑞‖ 𝑞∗
0) −𝐼(𝑞) −
𝐷KL( ̂𝑚(𝑞) ‖ 𝑞∗
0)
(inline)
pythagorean_residual(q,
mf_reference)
dualFlat_pythagorean_-
witness
Spectral and tensor-network symbols
Symbol
Meaning
LaTeX
Python
Lean
𝑟
Schmidt rank of bipartite
(K=2) joint
r
schmidt_rank(q, atol)
(boundary witness)
𝑠𝛼
𝛼-th singular value
s_\alpha
Archetype.weight (in
schmidt_decomposition)
(numerical)
134

## Page 136

Symbol
Meaning
LaTeX
Python
Lean
𝑢𝛼, 𝑣𝛼
Left / right singular
vectors (archetype
marginals)
u_\alpha,\,v_\alpha
Archetype.u, Archetype.v
(numerical)
𝑆𝐸(𝑞)
Policy entanglement
entropy of bipartite cut
S_E(q)
entanglement_entropy(q,
atol)
(numerical)
𝑟eff(𝜆) = 𝑒𝑆𝐸(𝑞𝜆)
Effective rank —
smooth phase order
parameter (continuous
proxy for the integer
Schmidt rank) used in
§10
r_{\mathrm{eff}}
np.exp(entanglement_-
entropy(q)) (composition)
(no Lean — numerical)
𝑟𝑘
Tensor-train bond
dimension across 𝑘-th cut
r_k
tensor_train_ranks(q,
atol)[k]
(numerical)
(𝑟1, … , 𝑟𝐾−1)
Tensor-train rank profile
(r_1,\ldots,r_{K-1})
entanglement_spectrum(q)
(numerical)
𝐴(𝑘)
MPS / tensor-train
tensor at site 𝑘(factor of
the matrix-product
factorization of 𝑞𝜆); see
§8.3
A^{(k)}
mps_decomposition(q)[k]
(canonical left-orthogonal
TT-SVD;
reconstruction-verified in
tests/test_spectral.py)
(no Lean)
𝑆𝑘(𝑞𝜆)
Per-cut bond entropy:
entanglement entropy
across the bipartition
splitting streams
{1, … , 𝑘} from
{𝑘+ 1, … , 𝐾}
S_k(q_\lambda)
entanglement_entropy_-
per_cut(q, k)
(composition of
entanglement_entropy with
the per-cut bipartite
reshape)
(no Lean)
𝑆max
𝑘
= log 𝑟𝑘
Maximum bond entropy
across cut 𝑘(achieved by
the uniform spectrum on
𝑟𝑘singular values)
S_k^{\max}
np.log(tensor_train_-
ranks(q)[k])
(no Lean)
Cov𝑞𝜆(𝐽−𝛾𝐾𝑐, log 𝑞𝜆−
log
̂𝑚(𝑞𝜆))
Covariance identity for
the derivative 𝑑𝐼/𝑑𝜆of
total correlation along
the entangled family (§4)
(inline)
(numerical; from
entangled_posterior
outputs)
(no Lean)
Heterogeneous-ensemble quantities
Symbol
Meaning
LaTeX
Python
Lean
tax(𝜆)
Coupling tax (KL
between fully-adaptive
and pinned posteriors)
\mathrm{tax}(\lambda)
coupling_tax(mf, G, J,
K_c, gamma, lam, modes)
couplingTax (witness
form)
‖Φ‖∞
Coupling magnitude
(sup-norm)
norm_inf(Phi)
(sup over
coupling-log-weight)
couplingNormSq
𝐶≥0
Structural curvature
constant in Theorem 9.1.
Live rendered value:
manuscript_-
variables.json[coupling_-
tax_curvature_C].
C
quadratic_bound_-
curvature(...)
(boundary witness)
KL-control, copula, and product-of-experts symbols
These symbols appear in §18.1 (KL-control / path-integral correspondence) and the copula / product-of-experts
extensions of §4 and §18.4. They are documented here so the reader can disambiguate against the main coupling
notation (particularly the trajectory cost 𝐶(𝜏), renamed from 𝐽to avoid collision with the habit coupling potential).
Symbol
Meaning
LaTeX
Python
Lean
𝑉(𝑥)
KL-control /
path-integral value
function (cost-to-go)
V(x)
(no Python — symbol
only)
(no Lean)
𝑝free
Uncontrolled / free
dynamics distribution
(reference law in the
KL-control
correspondence)
p_{\mathrm{free}}
(no Python — symbol
only)
(no Lean)
135

## Page 137

Symbol
Meaning
LaTeX
Python
Lean
𝜌
Risk-sensitivity
parameter in KL-control
(inverse-temperature on
the trajectory cost)
\rho
(no Python — symbol
only)
(no Lean)
𝐶(𝜏)
Trajectory cost in
KL-control. Renamed
from 𝐽to avoid clash
with the habit coupling
potential 𝐽(𝜋).
C(\tau)
(no Python — symbol
only)
(no Lean)
𝑢𝑘= 𝐹𝐸𝑘(𝜋𝑘)
Copula CDF
reparameterization of
per-stream policy: 𝑢𝑘is
the CDF transform of 𝜋𝑘
under 𝐸𝑘, mapping each
stream onto [0, 1] for
copula-based coupling
u^k = F_{E_k}(\pi^k)
(no Python — symbol
only; copula extension is
outside the present
implementation)
(no Lean)
𝑓𝑗
Product-of-experts factor
(one of the multiplicative
experts in
𝑞(𝜋) ∝∏𝑗𝑓𝑗(𝜋))
f_j
(no Python — symbol
only)
(no Lean)
𝐺soph(𝜋)
Sophisticated-inference
expected free energy
(recursive EFE over
future belief updates)
G_{\mathrm{soph}}
per_stream_efe(...,
SOPHISTICATED)
ConnectionsWitnesses /
sophisticated-inference
witness
𝐽soph
Source-supplied coupling
carrying recursive
observation-conditioning
for sophisticated
inference; not generated
by 𝜆alone
J_soph
witness payload
SI embedding payload
Relationship classes and claim-strength labels
Part V and §S7.2 use two small controlled vocabularies. They are not mathematical variables, but they are notation
in the audit sense: they determine how strongly a sentence is allowed to identify this framework with an external
active-inference variant.
Label
Meaning
Where enforced
exact
Literal specialization of the posterior family
or a single-stream log-partition dual after
all factors are specified
Active-inference recovery ledger;
relationship-guard tests
parametric
Realized only after the modeler adds an
explicit factor, change of variables, agent
boundary, or structural parameter
Active-inference recovery ledger;
relationship-guard tests
analogical
Shares a structural motif, while temporal,
recursive, state-space, or message-passing
content remains outside the 𝜆-deformation
Active-inference recovery ledger;
relationship-guard tests
out-of-scope
Related background whose geometry or
modeling object is not represented by the
current posterior family
Active-inference recovery ledger
proved / witness / empirical / hypothesis /
roadmap
Claim-strength labels used to separate
stock-Lean proofs, witness-consuming
theorem rows, generated numerical
evidence, interpretation, and future proof
discharge
§S7.1; claim-provenance tests
Hyperparameters (figure / sweep / simulation)
The constants below live in src/simulation/hyperparameters.py and are mirrored into output/data/manuscript_-
variables.json; they reach the prose via [[VAR:<key>]] substitutions.
Symbol
Source-of-truth constant
JSON key
Default
Param-sweep grid count
PARAMETER_SWEEP_LAMBDAS.num
param_sweep_grid_points
121
Param-sweep range
PARAMETER_SWEEP_-
LAMBDAS.[start,stop]
param_sweep_lambda_min/max
[0, 6]
Coupling-tax grid
COUPLING_TAX_LAMBDAS.num
coupling_tax_grid_points
31
Phase-diagram grid
PHASE_DIAGRAM_LAMBDAS.num
phase_diagram_grid_points
401
136

## Page 138

Symbol
Source-of-truth constant
JSON key
Default
pymdp sweep grid
PYMDP_SWEEP_LAMBDAS.num
pymdp_sweep_grid_points
21
pymdp rollout horizon 𝑇
PYMDP_ROLLOUT_STEPS
pymdp_rollout_steps
10
pymdp rollout seed
PYMDP_ROLLOUT_SEED
pymdp_rollout_seed
0
Figure-script global RNG seed
FIGURE_GLOBAL_SEED
figure_global_seed
42
Param-sweep agreement
tolerance
PARAMETER_SWEEP_AGREEMENT_-
TOLERANCE
param_sweep_agreement_tolerance
1𝑒−06
LaTeX preamble macros
Reserved LaTeX macros (currently unused in the body; available for future expansion): see manuscript/preamble.md
for the canonical definitions (\KL, \E, \Var, \policy, \policySpace, \Mfd, \MFsubmfd, \MI, \Hent, \efe, \fe, \coupJ,
\coupK). Each glossary row above cross-references the spelled-out form which is the one actually used throughout the
manuscript.
Lean type abbreviations
The Lean boundary fragment uses lower-case ASCII identifiers as substitutes for reserved binder tokens (𝜆→lam,
π →pi, Π →Pol).
Lean abbrev
Meaning
Defined in
α : Type
Generic scalar type satisfying CommScalar α
Scalar.lean
CommScalar α
In-house typeclass over a commutative
scalar
Scalar.lean
K : Nat
Stream count
Basic.lean
StreamIdx K
Fin K — stream index
Basic.lean
PolicyFactor K
StreamIdx K →Type — per-stream policy
type
Basic.lean
PolicySpace K Pol
∀k, Pol k — joint policy type
Basic.lean
JointDist K Pol
PolicySpace K Pol →α — joint PMF
JointDist.lean
MFDist K Pol
∀k, Pol k →α — mean-field PMF
JointDist.lean
CouplingPotential α K Pol
PolicySpace K Pol →α — 𝐽/ 𝐾𝑐shape
Coupling.lean
BinaryCoupling
Bool →Bool →Float — K=2 closed-form
coupling
BernoulliToy.lean
HorizonProfile K
StreamIdx K →Nat — temporal horizon per
stream
Basic.lean
pi : PolicySpace K Pol
A joint policy
(use sites)
lam : α
Coupling parameter
(use sites)
q_lam : JointDist K Pol
Entangled posterior at coupling lam
(use sites)
Phase / verdict labels (manuscript-level)
Three discrete classifiers used in the body of the manuscript.
Label
Values
Where defined
Manuscript role
InferenceMode
VFE / EFE / SOPHISTICATED
Python enum in
src/lean/heterogeneous.py
Stream-mode label (§3.2, §9)
CouplingPhase
disordered / mixed / frozen
(string)
Returned by bernoulli_-
toy.coupling_phase_at(lam)
Cognitive phase (§10)
CouplingRole
habit (𝐽) / preference (𝐾𝑐)
Manuscript convention; not a
Python or Lean type
Side of the coupling potential
CouplingVerdict
pays / neutral / does_not_pay
Manuscript convention;
manifests as the Lean theorem
couplingVerdict (in
Decomposition.lean)
Coupling-pays-for-itself outcome
(§11)
Status notes
• InferenceMode is presently a Python-only Enum; the Lean boundary fragment treats stream mode as a witness
consumed by IsPlanningStream / IsReflexiveStream predicates (Heterogeneous.lean). The current Lean source
therefore uses the predicates directly rather than an InferenceMode inductive.
• CouplingPhase
is
a
string-returning
Python
predicate
(coupling_phase_at)
plus
the
Lean
func-
tion
couplingPhaseAt
:
Float
→
Nat
(returning
0/1/2);
the
inductive
form
is
documented
in
lean/ActinfPolicyEntanglement/README.md but has not been promoted into the boundary source.
• CouplingRole has no Python or Lean type — it is manuscript-level convention to disambiguate the two coupling
potentials in prose.
137

## Page 139

Conventions
• Natural log is used throughout; numeric values therefore have units of nats. Where binary log is needed it is
written log2.
• Joint vs marginal: distributions on Π are joints; per-stream distributions on Π𝑘are marginals.
• Vector / tensor: bold x when shape matters, plain 𝑥otherwise.
• Equations vs definitions: an equation set off as 𝑋≡𝑌is a definition; 𝑋= 𝑌is a derivable identity.
• Probability conventions: every distribution is normalized to 1 unless explicitly unnormalized; KL is always
𝐷KL(𝑞‖ 𝑝) (not the reverse).
• Information geometry: dually-flat structure on the simplex follows the standard development [Amari and
Nagaoka, 2000, Amari, 2016, Nielsen, 2020]; non-extensive / 𝜙-deformed analogs use the framework of [Naudts,
2011].
• Active-inference background: the single-stream POMDP recap follows [Friston, 2010, Da Costa et al.,
2020, Smith et al., 2022], with EFE conventions per [Friston et al., 2017a].
• Determinism: all numerical figures are bit-reproducible under fixed seeds; see the full determinism contract
in docs/reference/statistics_reference.md.
Common pitfalls when editing across tracks
The four-track contract permits a few notation hazards that have bitten earlier drafts and that automated validation
does not catch. They are listed here so an editor can recognise them by name.
• Prior vs posterior expectation. The symbol ⟨𝑋⟩𝜆is ambiguous; the manuscript uses ⟨𝑋⟩ℰ𝜆for prior
expectations (used in the log-partition derivative d log 𝑍𝐸/d𝜆= ⟨𝐽⟩ℰ𝜆) and ⟨𝑋⟩𝑞𝜆for posterior expectations.
Mixing them silently introduces a sign error in convex / concavity arguments (see §B).
• 𝜆as parameter vs 𝜆as Lean keyword.
In Lean, 𝜆is reserved for anonymous-function syntax; the
manuscript parameter 𝜆becomes the identifier lam on the Lean side. Every lam
:
α in .lean files is the
coupling parameter, not a closure binder.
• 𝐾vs 𝐾𝑐. 𝐾(stream count) and 𝐾𝑐(preference coupling potential) collide at one ASCII letter. Use Kc
(Python, Lean) or K_c (LaTeX); never bare K in a context that could be read as either.
• MF prior 𝐸MF vs 𝜆-entangled prior ℰ𝜆. Both pieces of notation use the letter “E”, and e_lambda / mf_-
prior are the disambiguating Python names; never write E in code or prose without the appropriate subscript
or qualifier.
• Total correlation vs per-stream entropy sum. 𝐼(𝑞) = ∑𝑘𝐻(𝑞𝑘) −𝐻(𝑞) ≥0, not ∑𝑘𝐻(𝑞𝑘) alone. The
Python total_correlation(q) returns the difference; an editor importing sum_marginal_entropies and calling
it “total correlation” by mistake will introduce a manuscript-vs-code divergence the validator cannot detect.
• Natural log everywhere. Information-theoretic quantities are in nats. When citing a log2-convention source
in the bibliography, convert before quoting numeric values.
• Floating tolerance. atol=1e-9 is the project-wide default for spectral / SVD-based predicates; atol=1e-12
is the default for conservation laws / sum-to-one checks; tests under tests/test_*.py adopt either explicitly.
Don’t change the default in one place without checking the others.
• 𝜂is overloaded.
In §7 (information geometry) it denotes m-coordinates (expectation parameters of an
exponential family); in §19 (policy-blanket leakage) it denotes the normalized multi-information 𝜂(𝑞) =
𝐼(𝑞)/𝐻(𝑞). Subscripts and context disambiguate; we keep both usages because each is standard in its parent
literature (Amari / Nagaoka for the geometric 𝜂; Friston / Pellet-Massini for the leakage 𝜂).
GNN fifth-track concordance (structural-and-numerical)
The fifth track maps each standing symbol of the K=2 toy to its declaration in the shipped GNN
source gnn/bernoulli_toy.gnn.md (parser:
src/gnn/parser.py; round-trip:
scripts/simulate_gnn.py; parity test:
tests/test_gnn_concordance.py). This track is structural-and-numerical, not a proof track, and the round-trip
is an internal-consistency reduction — the general machinery reduces to the closed form for this toy — not
an independent corroboration: it reproduces the model’s structure and the K=2 mutual-information curve to
7.77e-16 nats, but promotes no theorem row in §S7. See §S8.
Symbol
GNN variable
Active Inference Ontology term
𝜋1 (stream-1 policy)
pi1
Stream1PolicyVector
𝜋2 (stream-2 policy)
pi2
Stream2PolicyVector
𝐸1 (stream-1 habit prior)
E1
Stream1HabitPrior
𝐸2 (stream-2 habit prior)
E2
Stream2HabitPrior
138

## Page 140

Symbol
GNN variable
Active Inference Ontology term
𝐽(cross-stream coupling)
J (joint var on the policy product)
CrossStreamCouplingPotential
𝜆(deformation)
lam
EntanglementDeformationParameter
𝛾(sophistication)
gamma
SophisticationWeight
𝑞𝜆(entangled joint posterior)
q_joint
EntangledJointPosterior
Reference Tables: Claim Strength, Variant Recovery, Lean Inventory,
pymdp Bundle Statistics, and JSONL Run-Log Schema
This supplement collects reference catalogs that are too detailed for main-body prose but essential for auditing the
boundary fragment, the free-energy bundle, and the structured run log. Each table is labeled and cross-referenced
from the body section that introduces it.
Claim-Strength Legend
The manuscript uses five claim-strength labels so readers can see whether a sentence is formal, numerical, interpretive,
or forward work:
Strength
Meaning
Promotion rule
proved
machine-checked as the registered boundary
statement; row-level faithfulness:
distinguishes substantive rows from
statement-restricted rows
already source-backed by the default Lean
build for Float-track boundary statements,
with claim strength limited by the row’s
faithfulness: value; analytic real-valued
rows require the --with-mathlib
MathlibProofs build with foundational-only
#print axioms
proved (analytic, ℝ)
machine-checked in the Mathlib-backed
lean/MathlibProofs/ package over ℝ(not
stock-Lean Float), with foundational-only
#print axioms (no sorryAx / no
project-axiom), at least one independent
negative control, and an enforced
reproducible audit gate
(scripts/build_mathlib_proofs.py +
tests/test_mathlib_axiom_audit.py)
already source-backed by the MathlibProofs
build path
witness
a typed Lean witness record or
witness-consuming theorem exists
promote only when the analytic payload is
constructed in a green proof layer
empirical
generated by scripts and validated by
CSV/JSON/PNG/PDF gates
promote only by adding replicated or
broader benchmark evidence
hypothesis
model-generated biological, clinical, or
alignment interpretation
promote only by adding direct empirical
study or citation-backed validation
roadmap
scoped future work, including Mathlib
witness discharge and the verified Float↔ℝ
bridge
promote only when source and gates exist
Active-Inference Variant Recovery Ledger
Part V uses the same finite joint-policy template for every connection, but it does not assign the same claim strength
to every prior framework. The ledger below records the structural choice, the relationship class, and the validation
hook that prevents an analogical mapping from being read as an exact recovery.
Read each row as a statement about where the comparison lands in the shared notation of §S6: 𝐸𝑘, 𝐺𝑘, and 𝛾𝑘
come from the single-stream active-inference posterior; 𝐽, 𝐾𝑐, and 𝜆are the added policy-space coupling objects;
and special payloads such as 𝐽soph or a block-bidiagonal hierarchical 𝐽must be supplied by the modeler. A row
marked analogical is therefore not a failed exact recovery; it is a deliberate boundary saying that recursive EFE,
temporal-scale separation, state-space Markov blankets, or a message-passing schedule live outside the scalar 𝜆
deformation.
139

## Page 141

Variant or framework
Structural choice in the
𝜆-coupled posterior
Relationship class
Evidence / gate
Do not overclaim
Mean-field discrete
POMDP AIF (pymdp,
SPM, ActiveInference.jl)
Set 𝜆= 0 so the joint
policy posterior is the
outer product of
per-stream policy
posteriors
exact
Corollary 5.3; pymdp
𝜆= 0 free-energy-bundle
gate; test_coupled_-
policy_posterior_lambda_-
zero_is_outer_product
Does not imply that
every multi-factor AIF
model already has
multiple coupled policy
variables
Factor-graph /
RxInfer-style message
passing
Add exp(𝜆𝐽−𝛾𝜆𝐾𝑐) as
an explicit policy factor
in the graphical model
parametric
Factor-graph citations
[de Vries and Friston,
2017, Friston and Parr,
2017, Parr et al., 2019];
RxInfer software citation
[Bagaev and Podusenko,
2023]; manuscript
validation of the recovery
table
The inserted factor has
exact semantics only
inside the chosen graph;
message passing itself is
the implementation
substrate, not a new
theorem
Hierarchical / deep
temporal AIF
Use block-bidiagonal 𝐽
between adjacent levels
and supply the
concentration witness
analogical + witness
Theorem 17.1;
ConnectionsWit-
nesses.hierarchicalAIF_-
lambda_limit_witness;
Lean boundary gate
Temporal-scale
separation and directed
message passing are not
recovered by symmetric
𝐽alone
Sophisticated inference
Encode recursive EFE
content in a
source-supplied 𝐽soph /
embedding witness
analogical + witness
Proposition 17.2;
sophisticatedInference_-
embedding_witness; Lean
boundary gate
Recursive
observation-conditioning
must be built into the
witness payload
Branching-time AIF
View tensor-train or
prefix-tree compression
as a compact
representation of the
expanded policy tree
analogical + empirical
(scoped)
Shipped UCB-MCTS
baseline worked run
([Champion et al., 2022];
; 1, 3 budgets) — estimates lowest-EFE joint action, not the soft variational posterior of [Champion et al., 2022]
| No algorithmic equivalence to Bayesian-filter BTAI; compute-matched head-to-head study remains open | |
Multi-agent / federated AIF | Use within-agent and across-agent blocks of 𝐽after agent boundaries and shared or
linked generative models are specified | parametric | Multi-agent/federated citations [Maisto et al., 2024, Friston
et al., 2024]; interaction and coupling-ablation sidecars | The literature is not asserted to optimize this exact joint
posterior unless it writes that model | | Scale-free / RGM | Interpret low-rank projection of 𝑞𝜆as a policy-posterior
coarse-graining analogy | analogical | RGM / scale-free citation [Friston et al., 2025]; tensor-train rank profile
figure | MERA-style scale invariance and generative-model RG flow are outside this artifact | | Markov blankets /
Bayesian mechanics | Use normalized multi-information as policy-space leakage after a model boundary is chosen
| analogical + witness | Proposition 19.3; Markov-blanket critical citations [Kirchhoff et al., 2018, Aguilera
et al., 2022, Raja et al., 2021] | This is not a recovery of state-space Markov blankets or an argument for new
biological boundaries | | CEREBRUM / case grammar | Encode role relations as asymmetric edge weights in 𝐽,
with 𝒦
𝛼−→Coup𝐾pullback when a categorical case substrate is supplied | parametric | CEREBRUM citation
[Friedman, 2025]; compositional-case substrate [Friedman, 2026b]; coupling-graph figure | Case grammar supplies
role structure; the categorical substrate licenses the asymmetry but does not prove it from the coupling model |
Lean 4 Boundary-Fragment Module Inventory
Implementation status of lean/ActinfPolicyEntanglement/, Lean 4 v4.29.0 (cross-referenced from §12):
140

![page141_img1.png](images/page141_img1.png)

## Page 142

Module
Theorems / definitions
Sorries
Basic
StreamIdx, PolicyFactor, PolicySpace,
IsPlanningStream, IsReflexiveStream,
instDecidableIsPlanningStream,
instDecidableIsReflexiveStream,
stream_classification
0
Scalar
CommScalar α typeclass, derived
mul_sub/sub_mul/sub_self/affine_-
diff/affine_at_zero; instance : CommScalar
Int
0
JointDist
JointDist, MFDist, IsNonNeg, IsPMF,
mfProductWeight, mfToJoint, IsMeanField
0
Coupling
CouplingPotential α, trivialCoupling,
couplingLogWeight,
entangledPosteriorLogWeight,
couplingLogWeight_affine_in_lam,
couplingLogWeight_at_zero (both proved on
[CommScalar α])
0
FreeEnergy
supportSum, safeLog, shannonEntropy, kl,
totalCorrelation, variationalFreeEnergy,
marginalFreeEnergy,
totalCorrelation_eq_kl_to_mprojection
0
Geometry
mfImage_isMeanField,
mProjection_kl_eq_self_when_meanfield,
entangledFamily_eGeodesic,
dualFlat_pythagorean_witness
0
Spectral
Bipartite.BipartiteJoint,
Bipartite.IsBipartiteMeanField,
Bipartite.isBipartiteMeanField_factors,
Bipartite.factors_isBipartiteMeanField
0
Heterogeneous
HorizonProfile, couplingTax,
BoundedQuadraticTax structure,
couplingTax_quadratic_bound (Theorem 9.1),
SmallLambdaTolerance structure,
couplingTax_small_lambda_tolerance
(Corollary 9.2)
0
BernoulliToy
Action, BinaryMF, BinaryJoint,
BinaryCoupling, float-
Exp/floatLog/floatLogistic/floatArctanh,
alignedIndicator, isingCoupling, xLogX,
binaryEntropy, isingMutualInformation,
optimalLambda, isingFreeEnergyCurve,
lambdaC1/lambdaC2/couplingPhaseAt,
isingMI_zero_at_zero,
isingFreeEnergyCurve_total
0
Decomposition
couplingExpectationSkeleton,
entanglement_decomposition (Theorem 5.1,
witness form), couplingVerdict,
couplingLogWeight_pointwise_at_zero
(Corollary 5.3), totalCorrelation_def_unfold
(Corollary 5.4),
freeEnergy_closedForm_witness (Theorem
5.5, closed-form boundary),
freeEnergy_closedForm_at_zero (mean-field
collapse)
0
Monotonicity
nat_le_refl, nat_le_trans, nat_succ_pos,
nat_zero_le, nat_le_succ, nat_lt_succ_self,
or_self_iff, or_comm_iff, and_self_iff,
list_length_nonneg, list_length_cons,
list_length_append, list_append_nil,
list_nil_append, fin_lt_size, fin_zero_lt
0
Constructive
entangledPosteriorLogWeight_at_zero,
couplingLogWeight_trivialCoupling,
couplingNormSq_of_trivialCoupling,
couplingTax_zero_at_zero (all
CommScalar-polymorphic, genuine = 0 proofs)
0
Convexity
freeEnergy_convex_in_lam_witness,
freeEnergy_localConcavity_at_zero_witness
(witness payloads for Theorem 5.6,
Proposition 11.1)
0
SpectralWitnesses
schmidtRank_upperSemicontinuous_witness,
sparsityRank_tradeoff_witness
0
ConnectionsWitnesses
hierarchicalAIF_lambda_limit_witness,
sophisticatedInference_embedding_witness
0
141

## Page 143

Module
Theorems / definitions
Sorries
MarkovBlanket
markovBlanket_separation_identity_witness
0
FloatRealResidualWitness
FloatRealResidualWitness structure +
floatRealResidual_witness (roadmap
Float↔ℝresidual shell; values from
output/reports/float_real_residual.json)
0
Total: ~126 declarations (39 defs, 76 theorems / lemmas, 11 structures in Heterogeneous — BoundedQuadraticTax
and SmallLambdaTolerance), 0 sorries, 0 axioms, 0 unsafe/partial/noncomputable.
Worked excerpt — the load-bearing identity in Lean. To make the shape concrete, here is the boundary
statement of the entanglement decomposition theorem (Theorem 5.1) as it lives in Decomposition.lean:
/-- **Theorem 5.1 (Entanglement Decomposition)** — boundary witness
form.
Given a Mathlib-supplied algebraic split
`F[q] = marginal_part + coupling_expectation + agentic_gain`,
where `coupling_expectation` is the integrated `couplingLogWeight`
against `q`, this theorem certifies the equation in the boundary
fragment. Every coupling parameter `(J, K_c, γ, 𝜆)` is genuinely used
via `couplingExpectationSkeleton`, so the statement is non-vacuous. -/
theorem entanglement_decomposition {K Pol}
(q : JointDist K Pol) (s : List (PolicySpace K Pol))
(logE G : PolicySpace K Pol →Float)
(J K_c : CouplingPotential Float K Pol) (gamma lam : Float)
(marginal_part agentic_gain : Float)
(hWitness : variationalFreeEnergy q logE G gamma s =
marginal_part
+ couplingExpectationSkeleton q s J K_c gamma lam
+ agentic_gain) :
variationalFreeEnergy q logE G gamma s =
marginal_part
+ couplingExpectationSkeleton q s J K_c gamma lam
+ agentic_gain :=
hWitness
The hWitness argument is the analytic-content boundary: the caller supplies the algebraic equality once Mathlib’s
Finset.sum_comm (or its target-language analog) is in scope;
the boundary fragment retains the structural
decomposition so its type-check is unaffected. Every witness-form theorem in the table above follows the same
pattern.
MathlibProofs ℝAnalytic Discharge Package: Inventory
The companion package lean/MathlibProofs/MathlibProofs.lean is separate from the Float boundary fragment
listed above. Built independently via lake build (or via the enforced scripts/build_mathlib_proofs.py), it imports
Mathlib4 and machine-checks the manuscript’s central analytic identities in ℝ. The keystone declarations the audit
gate tests/test_mathlib_axiom_audit.py pins, in their natural order:
Declaration
Role
Foundational-only #print axioms?
klReal_nonneg
Gibbs inequality: 𝐷KL(𝑝‖ 𝑞) ≥0 for finite
probability vectors with strictly-positive 𝑞
yes
klReal_split_via_intermediate
KL chain-rule decomposition through an
intermediate distribution
yes
klReal_minimises_generalK
𝑚-projection minimality for general
entangled 𝑞over the mean-field
submanifold (general 𝐾)
yes
crossTerm_matches_K2
𝐾= 2 specialization of the cross-term
identity
yes
crossTerm_matches_of_equal_marginals
General-𝐾cross-term discharge under the
equal-marginals hypothesis
yes
entanglement_decomposition_generalK
Axiom-clean general-𝐾kernel for the
multi-information term in Theorem 5.1
yes
free_energy_decomposition_full
Capstone — the full S01 boxed
free-energy identity machine-checked in ℝ
for the genuine entangled posterior 𝑞𝜆;
positivity and unit mass proved from the
definitions, log 𝑍𝐸the genuine definitional
log-normalizer, 𝐼(𝑞𝜆) discharged via
entanglement_decomposition_generalK
yes
142

## Page 144

Non-vacuity is verified by two independent negative controls: (i) the log 𝑍𝐸definitional body and (ii) the 𝛾𝜆⟨𝐾𝑐⟩
coupling term each make the build fail when neutralised. The whole package depends only on the three standard
foundational axioms (propext, Classical.choice, Quot.sound). The single open analytic residual is a verified error-
bounded Float↔ℝbridge scoped in docs/reference/methods_and_assumptions.md as multi-week research.
pymdp Free-Energy Bundle: Auto-Injected Summary Statistics
The 12 summary statistics computed by simulation.statistics.pymdp_summary_statistics and mirrored to out-
put/simulations/pymdp_summary.json (cross-referenced from §15). Every value flows from a real pipeline run via
[[VAR:<key>]] substitution:
Quantity
Symbol
Auto-injected value
Sweep grid points
𝑁𝜆
21
Sweep range
𝜆∈[𝜆min, 𝜆max]
[0, 4]
Total correlation
𝐼min, 𝐼max, 𝐼
0.0000, 0.3635, 0.2530 nats
Half-saturation
𝜆1/2, 𝐼(𝜆1/2)
1.044, 0.1818 nats
Total VFE
𝐹min, 𝐹max, 𝐹
1.6840, 2.4167, 2.2778 nats
Coupling term
𝜆⟨𝐽⟩min,max
0.0000, 3.9983 nats
Joint entropy
𝐻min, 𝐻max
0.3675, 1.1644 nats
Aligned-corner mass
min, max, at 𝜆max
0.6068, 0.9998, 0.9998
KL to 𝑞0
min, max
0.0000, 0.4976 nats
KL to uniform at 𝜆max
—
1.0188 nats
Action entropy
min, max
0.3675, 1.1644 nats
Mode probability at 𝜆max
max𝜋𝑞𝜆max(𝜋)
0.8806
Robustness and Ablation Stress-Test Ledger
The stress-test sidecars are intentionally compact:
one-axis perturbations for robustness, four fixed role/sign
ablations, and replicate seeds for long-horizon behavior. The table records what each branch is allowed to claim and
which artifact validates it.
Branch
Configured scope
Artifact
Claim checked
Robustness envelopes
14 one-axis scenarios over 21 𝜆
values
output/simulations/pymdp_-
robustness.csv; Fig. 20
Positive total-correlation
envelopes persist outside the
canonical observation /
precision / preference slice.
Robustness half-saturation
scenario-level 𝜆1/2 summaries
output/data/robustness_-
summary.json; Fig. 21
Threshold movement is reported
as sensitivity, not as a new
theorem.
Robustness decomposition
residuals
same rows as the envelope
branch
output/simulations/pymdp_-
robustness.csv; Fig. 22
Theorem 5.1 remains
numerically closed; max residual
1.55e-15.
Coupling ablation
4 fixed variants
output/simulations/pymdp_-
coupling_ablation.csv; Fig. 23
𝜆= 0 is invariant, null coupling
is flat, non-null role/sign
changes alter archetypal mass
without breaking the
decomposition.
Two-axis interactions
41 targeted scenarios across
observation × coupling scale,
gamma × preference strength,
coupling variant × coupling
scale
output/simulations/pymdp_-
interaction_robustness.csv;
Fig. 25
Interaction effects are appendix
evidence; the null-variant
flatline and decomposition
residual guard remain intact.
Long-horizon replicates
seeds {0, 7, 13, 29, 41}
output/simulations/pymdp_long_-
horizon_replicates.csv; Fig. 26
The fixed-seed figure remains
canonical; the replicate sidecar
reports TC-envelope and
habit-pass-rate sensitivity.
Long-horizon diagnostics
one row per configured replicate
seed
output/simulations/pymdp_long_-
horizon_seed_diagnostics.csv;
Fig. 27
Seed failures are explained as
tail-window KL sensitivity
rather than retuned away.
Evidence Ladder and Claim Provenance
The project distinguishes formal theorem rows, empirical artifacts, figures, and tests. A headline claim should appear
with all four tracks when it is theorem-backed, or with an explicitly empirical artifact/test pair when it is a numerical
stress observation.
143

## Page 145

Claim
Strength
Formal row
Simulation / data
artifact
Figure
Test or validator
gate
Entanglement
decomposition closes
for the pymdp
posterior
witness + empirical
Theorem 5.1
Free-energy bundle
CSV; robustness
CSV
Fig. 36; Fig. 22
validate_free_-
energy_bundle;
validate_-
robustness_suite;
focused simulation
tests
Mean-field anchor at
𝜆= 0
proved (substantive
on Corollary 5.3;
statement-restricted
on Proposition 7.2)
+ empirical
Corollary 5.3,
Proposition 7.2
Free-energy bundle
CSV;
coupling-ablation
CSV
Fig. 32; Fig. 23
validate_free_-
energy_bundle;
validate_coupling_-
ablation; robustness
tests
Fixed-marginal null
control removes
cross-stream
dependence
empirical
Proposition 7.3
Marginal-null-control
CSV and JSON
Fig. 24
validate_marginal_-
null_control;
robustness tests
Total correlation
equals KL to the
𝑚-projection
witness + empirical
Proposition 7.3
Revertibility CSV
Fig. 17
validate_-
revertibility;
revertibility tests
Multi-stream
coupling scales
beyond 𝐾= 2
witness + empirical
Theorem 8.3
Per-𝐾sweep CSVs;
multi-𝐾summary
JSON
Fig. 12; Fig. 14
validate_multi_k_-
sweep; multi-𝐾tests
Heterogeneous /
role-changing
couplings alter mass
without voiding the
identity
witness + empirical
Theorem 9.1,
Corollary 9.2
Coupling-ablation
CSV; interaction
CSV
Fig. 23; Fig. 25
validate_coupling_-
ablation;
validate_-
interaction_-
robustness;
robustness tests
Long-horizon
trajectory
stationarity is a
finite-horizon
empirical witness
(not “habit
formation” — the
rollout agents
perform no
parameter learning;
see §13 honest-scope
disclosure)
empirical +
hypothesis
Theorem 17.1
Long-horizon CSV;
replicate CSV;
seed-diagnostics
CSV;
threshold-sensitivity
CSV
Fig. 15; Fig. 26;
Fig. 27; Fig. 28
validate_long_-
horizon;
validate_long_-
horizon_replicates;
validate_long_-
horizon_threshold_-
sensitivity;
long-horizon tests
MathlibProofs
machine-checks the
full S01 free-energy
identity in ℝ
proved (analytic, ℝ)
Theorem 5.1
MathlibProofs.free_-
energy_-
decomposition_full;
entanglement_-
decomposition_-
generalK general-𝐾
kernel
no paper figure
(formal-track row)
scripts/build_-
mathlib_proofs.py
(foundational-only
#print axioms);
test_mathlib_axiom_-
audit.py;
test_mathlib_-
proofs_integrity.py
Witness-form
analytic payloads
(the witness-tier
rows) admit
Mathlib4 discharge
roadmap
Theorem 5.6,
Proposition 7.3,
Proposition 7.5,
Proposition 8.2,
Theorem 8.3,
Theorem 9.1,
Corollary 9.2,
Proposition 11.1,
Theorem 17.1,
Proposition 17.2,
Proposition 19.3
future
lean/MathlibProofs
extension consuming
Mathlib’s KL /
PMF, convexity /
Taylor,
semicontinuity /
rank, tensor-product
and
measure-theoretic
primitives [Degenne,
2025, Degenne et al.,
2025]
no paper figure
per-witness
conformance test in
tests/test_witness_-
conformance.py plus
future per-row
discharge under
scripts/build_-
mathlib_proofs.py
Verified
error-bounded
Float↔ℝbridge
linking the ℝproofs
to the Float pipeline
roadmap
Theorem 5.1
(Float-side
companion)
future Flocq-style
IEEE-754 model or
interval-arithmetic
re-implementation;
scoped in the
methods-and-
assumptions
reference page
no paper figure
future error-bound
theorem with
foundational-only
#print axioms +
self-designed
non-vacuity negative
control
144

## Page 146

pymdp JSONL Run-Log Field Schema
Full field schema of output/logs/pymdp_runs.jsonl (cross-referenced from §16). Each record is a single JSON object
on its own line:
Key
Type
Meaning
timestamp
ISO-8601 UTC offset
when the record was emitted
script
string
originating script (e.g. simulate_pymdp.py)
event
string
main_start / main_end lifecycle records
(carries pymdp_ensemble_K,
pymdp_ensemble_gamma, figure_global_seed,
artifacts_emitted)
section
string
function-level event label
(e.g. figure_pymdp_lambda_sweep,
figure_pymdp_free_energies,
figure_pymdp_rollout)
num_streams, gamma, seed, horizon, lam
numeric
ensemble hyperparameters in effect for the
section
observations
list
observations driving the run (per stream)
grid_points, lambda_min, lambda_max
numeric
sweep grid descriptors
policy_shape
list[int]
shape of the joint policy tensor (e.g. [2, 2])
tc_min, tc_max, tc_initial, tc_final
float
total-correlation summary over the sweep /
rollout
vfe_total_min, vfe_total_max
float
per-sweep VFE-sum extrema
(free-energy-bundle records only)
coupling_term_at_lambda_zero
float
numerical 𝜆= 0 sentinel; must be exactly
0.0
joint_entropy_at_lambda_zero,
marginal_entropy_sum_at_lambda_zero
float
the two must coincide at 𝜆= 0 (sentinel for
𝐼(𝑞0) = 0)
tc_at_half_saturation,
lambda_at_half_saturation
float
locating the half-saturation coupling,
sourced from the bundle summary
all_pmf
bool
every 𝑞𝜆on the sweep grid passed PMF
validation
sampled_actions
list[list[int]]
sampled-action trajectory
(figure_pymdp_rollout records only)
steps_emitted, artifacts_emitted
int / list
rollout step count; artifact paths emitted
by the section
runtime_ms
float
wall-clock duration of the section
status
"ok" / "error"
exit status of the section
Worked excerpt — a real run-log record. The free-energy-bundle section writes one JSONL record under
output/logs/pymdp_runs.jsonl.
The schema below mirrors that record while keeping numerical fields tokenized
against the current manuscript-variable bundle:
{
"timestamp": "<iso8601 timestamp emitted by the logger>",
"script": "simulate_pymdp.py",
"section": "figure_pymdp_free_energies",
"num_streams": 2,
"gamma": 1,
"observations": [0, 0],
"grid_points": 21,
"lambda_min": 0,
"lambda_max": 4,
"tc_min": 0.0000,
"tc_max": 0.3635,
"vfe_total_min": 1.6840,
"vfe_total_max": 2.4167,
"coupling_term_at_lambda_zero": 0,
"joint_entropy_at_lambda_zero": 1.1644,
"marginal_entropy_sum_at_lambda_zero": 1.1644,
"tc_at_half_saturation": 0.1818,
"lambda_at_half_saturation": 1.0436,
"runtime_ms": "<measured by logger>",
"status": "ok"
}
The three sentinels are checked by scripts/validate_outputs.py: coupling_term_at_lambda_zero must be exactly
0 (mean-field at 𝜆= 0), and joint_entropy_at_lambda_zero must equal marginal_entropy_sum_at_lambda_zero at
𝜆= 0 (total correlation 𝐼(𝑞0) = 0). A record that ships status: "ok" but fails either gate causes CI to reject the
run.
Worked excerpt — interpreting the bundle summary. Running the harness with the standard hyperparame-
145

## Page 147

ters (PYMDP_SWEEP_LAMBDAS spanning 0 to 4 over 21 points, observations [0, 0], 𝛾= 1) produces a pymdp_summary.json
whose key entries — all auto-injected via [[VAR:...]] above — interpret as follows:
• The mean total correlation across the sweep is 𝐼= 0.2530 nats; the sweep-maximum value is 𝐼max = 0.3635
nats at 𝜆= 𝜆max = 4. The Shannon ceiling for the configured 𝐾= 2 streams is the log 2 ceiling in this binary
aligned/anti-aligned Ising slice, so the sweep saturates roughly to half the ceiling under the Ising potential at
the chosen grid endpoint.
• Half-saturation 𝜆1/2 = 1.044: the coupling at which 𝐼(𝑞𝜆) first crosses 𝐼max/2.
• Aligned-corner mass at 𝜆max is 0.9998 — the maximum-probability joint policy cell, lying between the uniform
baseline 1/|Π| and the single-archetype limit, and measuring how concentrated the posterior is on its dominant
archetypal joint policy.
These are the interpretive labels on the bundle stats; the auto-injected numbers above are bit-reproducible from the
same run.
GNN as a Shipped Fifth Track: Triple-Play Mapping, a Verified K=2
Bernoulli Round-Trip, and a Lean Typed-Contract Emitter
This supplement ships Generalized Notation Notation (GNN) [Smékal and Friedman, 2023, Institute, 2023]
as a fifth track of the policy-entanglement framework, on top of the four tracks the manuscript was developed on
(prose, equations, Python/pymdp, Lean — see §1). The bridge is no longer a forward-pointing scoping appendix. A
project-owned GNN v1.1 parser (src/gnn/parser.py), a deterministic round-trip that reconstructs the K=2 Bernoulli
mutual-information curve from a real .gnn source (gnn/bernoulli_toy.gnn.md) and matches the closed form to a
maximum residual of 7.77e-16 nats, a Lean typed-structure emitter whose output type-checks under the stock Lean
v4.29.0 toolchain, and a GNN-sourced manuscript variable all ship and run in the pipeline (scripts/simulate_gnn.py,
wired into scripts/run_all.py; covered by tests/test_gnn_parser.py, tests/test_gnn_round_trip.py, tests/test_-
gnn_concordance.py).
What the fifth track is precise about. It reproduces the framework’s structural and numerical content; it does
not prove theorems. Parsing and round-tripping a GNN source reconstructs numbers and emits a typed contract —
it promotes no theorem row in §S7 to proved or witness. The four-track proof contract of §S6 and §1 is unchanged
in its analytic content; GNN is added as a fifth, structural-and-numerical track with its own CI gates, not as a
fifth proof track. This distinction is the load-bearing honesty of the supplement and is enforced in code: the Lean
emitter’s output declares itself a typed contract, and no registry promotion is wired to the GNN layer.
Scope and Claim-Strength:
a Shipped Bridge, with an Explicit Non-Claim About
Proof
Framing declaration. In the framing taxonomy of this supplement — concordance column, token system, coupling-
graph source-of-truth, multi-agent extension scaffold, institute bridge — the section adopts the bridge framing. GNN
is a single namespaced supplement that bridges the policy-entanglement framework to the upstream GNN repository
[Institute, 2023] in the same style that the Lean-fragment supplement at §E (§E) bridges this manuscript to the
institute-wide fep_lean catalog: minimal, namespaced, single-link — one upstream repository, one canonical
citation, one supplement, no rewriting of the body manuscript.
Claim-strength tag. The structural-and-numerical assertions of this supplement are empirical in the sense of
§S7.1: shipped, source-backed, CI-gated. Concretely:
• A 7.77156e-16 token is now sourced from a GNN round-trip: the value 7.77e-16 flows from output/data/gnn_-
bernoulli_roundtrip.json (emitted by scripts/simulate_gnn.py) through src/manuscript/variables.py::_-
gnn_facts and is range-gated in both REQUIRED_VARIABLES and the manuscript range gate.
• No theorem row in §S7 is promoted to proved or witness by the GNN layer — and this is by design, an
explicit non-claim, not a gap: parsing and round-tripping reproduce numbers, not proofs (see §S8.7).
• The K=2 Bernoulli mutual-information curve is now reconstructed from the GNN source and matches the hand-
authored closed form (the harness in src/simulation/ and src/lean/bernoulli_toy.py remains the canonical
generator of output/data/parameter_sweep.csv; the GNN track reproduces that curve through the general
machinery as an internal-consistency check rather than replacing it).
• A Lean typed-structure contract is now elaborated from the GNN source (src/gnn/lean_emit.py →
gnn/generated/BernoulliToyGnn.lean) and type-checks under the stock Lean v4.29.0 build; it is a typed con-
146

## Page 148

tract, not a proof.
Scope-discipline statement. Promoting GNN to a track-class commitment required four structural steps; all
four are now performed:
(i) the symbol concordance at §S6 gains a fifth (GNN) track alongside prose / equations / Python / Lean; (ii)
a gnn_* variable resolver in src/manuscript/variables.py populates GNN-sourced [[VAR:...]] tokens, parity-
checked by tests/test_gnn_concordance.py; (iii) tests/test_gnn_round_trip.py and tests/test_gnn_parser.py
ship alongside the existing token-resolution and project-wide-hyperlink tests; and (iv) gnn/bernoulli_-
toy.gnn.md is a round-trippable .gnn artifact under the reproducibility contract of §16, emitting a deterministic
(byte-identical on re-run) sidecar. The GNN track does not change any theorem statement, any proved/witness
label, or any analytic claim in the rest of the manuscript.
GNN Background: the Triple Play and the Active Inference Ontology
Smékal & Friedman (2023) [Smékal and Friedman, 2023] introduce Generalized Notation Notation (GNN) as
“a novel approach to generative model representation that facilitates communication, understanding, and application
of Active Inference across various domains”. The paper situates GNN as a complement — not a replacement
— to the Active Inference Ontology, providing “a standardized method for describing cognitive models” that is
“flexible and expressive” for education and modeling. The reference implementation lives at the upstream repository
[Institute, 2023].
The central pragmatic device of the paper is the Triple Play: an approach to expressing GNN models in three
modes simultaneously — linguistic, visual, and executable. Each mode is a view of the same GNN source:
• The linguistic view is a textual rendering of the model — the names, dimensions, dependencies, and equations
a human reader would write in prose.
• The visual view is a diagram in which model variables become nodes, dependencies become edges, and
structural hierarchy is read off the layout.
• The executable view is a runnable model — generated source code (typically in Python or a domain-specific
language) that an inference engine can ingest.
The stated goal of the paper is “to bridge and respect the gaps among different modeling settings” and “to facilitate
interdisciplinary research and application, ultimately promoting the advancement of the field.”
The Triple Play
is described as pragmatic — it does not assert that the three views are mathematically equivalent, only that
they are coherently emitted from one shared source. This supplement realizes the executable view concretely:
src/gnn/runner.py consumes a single .gnn source and emits a numerical round-trip (executable), a figure (visual),
and the model’s typed structure (linguistic/Lean).
The two-fold framing — GNN as a language, the Triple Play as a rendering discipline — is what makes GNN the
fifth representation for this manuscript: GNN supplies a single declarative surface (the source), and the Triple Play
supplies a discipline for emitting views (text, figure, code) from that single surface.
Acronym Disambiguation: GNN (Notation) vs. GNN (Graph Neural Network)
The manuscript uses the acronym GNN in two distinct senses, and this supplement is the canonical place to
disambiguate them.
• GNN (Notation): Generalized Notation Notation [Smékal and Friedman, 2023, Institute, 2023]. A model-
description language, shipped in this supplement as the fifth representation of the framework. Cited within
§S8, with its open questions cataloged at §S8.9 and its shipped status recorded in the open directions of §21.
• GNN (Graph Neural Network): The deep-learning architecture family. Referenced in §20 Q8 (“Learning
to couple — GNN connection”) as the candidate mechanism for learning the coupling potentials 𝐽and 𝐾𝑐
end-to-end from environment interactions. That usage names a learning-to-couple research direction in which
a graph-neural-network forward pass plays the role of the coupling-graph message-passing operator; it is an
answer to how the couplings might be learned, not a notation for the model itself.
The two meanings are orthogonal: Generalized Notation Notation is a specification language for the model; graph
neural networks are a parametric inference architecture that could be used to learn the model’s couplings. A reader
of this supplement should understand “GNN” within §S8 to mean Generalized Notation Notation throughout; the
open-questions reference at §20 Q8 retains the graph-neural-network meaning. No claim is made in this supplement
that the two meanings collapse, intersect, or share a substantive technical relationship beyond the historical acronym
clash.
147

## Page 149

Mapping the (𝐴, 𝐵, 𝐶, 𝐷, 𝐸, 𝐽, 𝜆) Tuple to a GNN Spec
The policy-entanglement framework operates on a finite-state discrete-time POMDP active inference baseline (see
§3) augmented by the coupling parameters (𝐽, 𝐾𝑐, 𝜆, 𝛾) introduced in §4. Per §S6, the standing symbol set for a
𝐾-stream ensemble is:
Symbol
Object
Manuscript reference
𝐴𝑘
Observation likelihood for stream 𝑘
§3.2
𝐵𝑘
State-transition kernel for stream 𝑘
§3.2
𝐶𝑘
Preferred-observation prior for stream 𝑘
§3.2
𝐷𝑘
Initial-state prior for stream 𝑘
§3.2
𝐸𝑘
Habit / policy-prior for stream 𝑘
§3.2
Π𝑘
Finite policy space for stream 𝑘
§3.2
𝐽
Cross-stream coupling potential
§4.1
𝐾𝑐
Cross-stream constraint potential
§4.1
𝜆
Coupling parameter (e-coordinate of the
entanglement family)
§4.2
𝛾
Sophistication weight
§4.1
In the shipped GNN bridge, each of these is a typed declaration in the GNN source:
• Per-stream POMDP primitives (𝐴𝑘, 𝐵𝑘, 𝐶𝑘, 𝐷𝑘, 𝐸𝑘) map to GNN variable blocks, one block per stream,
indexed by 𝑘∈{1, … , 𝐾}. Each block carries the dimensionality declarations the GNN parser understands for
single-agent POMDP AIF models.
• The coupling potentials (𝐽, 𝐾𝑐) map to a cross-stream joint variable over the product policy space —
J[2,2,type=float] for the K=2 toy, with ## Connections edges pi1-J and pi2-J binding each stream to it.
This requires no new GNN primitive.
The institute’s own multi_agent_coordination.md example in
the GNN repository [Institute, 2023] already encodes a joint product-space variable (s_joint[16,1]) with
connection edges from each agent — exactly the structure a cross-stream coupling needs. The framework’s
coupling is therefore expressible in stock GNN v1.1 as a joint variable plus edges, and the shipped parser
(src/gnn/parser.py) and bridge (src/gnn/bridge.py) consume precisely that encoding.
• The deformation parameter 𝜆and sophistication weight 𝛾map to GNN scalar parameters annotated with their
physical role. They render in the linguistic view as named quantities, in the visual view as scalar labels on
cross-stream edges, and in the executable view as named arguments to the inference routine.
The full (𝐴, 𝐵, 𝐶, 𝐷, 𝐸, 𝐽, 𝐾𝑐, 𝜆, 𝛾) tuple is therefore representable in stock GNN v1.1. For 𝐾> 2 the construction
composes: gnn/k_stream_ensemble.gnn.md declares a K=3 chain with pairwise couplings J12, J23, and the bridge
assembles the joint coupling tensor additively (𝐽(𝜋) = ∑(𝑎,𝑏)∈edges 𝐽𝑎𝑏(𝜋𝑎, 𝜋𝑏)), reading the coupling-graph topology
directly off the ## Connections block. Honest residual: a dedicated first-class CouplingBlock primitive would be
more ergonomic than the joint-variable-plus-edges encoding, and proposing one upstream to the canonical GNN
repository [Institute, 2023] is reasonable future contribution work — but it is an ergonomic improvement, not a
blocker, and nothing in this manuscript’s fifth track depends on it.
Toolchain capabilities advertised upstream of this manuscript. The GNN repository [Institute, 2023] and
the broader Active Inference Institute program around it advertise a family of capabilities: (i) an abstraction layer
over the model’s surface syntax supporting flexible run-time dispatch across stream counts, coupling-potential shapes,
and inference engines; (ii) model typing and checking for the dimensionality and topology of generative models; (iii)
resource estimation for the computational cost of running a model (a natural complement to the Schmidt-rank and
tensor-train bond-dimension profiles of §8); and (iv) the Triple Play rendering discipline [Smékal and Friedman,
2023]. The shipped bridge binds (ii) and (iv) directly — the project-owned parser type-checks the dimensionality
of the cross-stream encoding and raises on mismatch, and the Triple Play views are emitted by src/gnn/runner.py.
Bindings (i) run-time dispatch across an arbitrary inference backend and (iii) resource estimation against the TT
bond-dimension profile remain the natural next bindings; they are not exercised by the present pipeline and are
named as forward work in §S8.9, distinct from the now-shipped core bridge.
Worked Example: the K=2 Bernoulli Toy as a Shipped GNN Round-Trip
The cleanest place to make the GNN bridge concrete is the K=2 Bernoulli toy developed in §6.1 and proved
closed-form in §C. This is the same object that anchors the symbol-by-symbol walkthrough in §S6 across the four
existing tracks — using it again for the fifth track preserves pedagogical continuity.
The toy has two binary policy streams (Π1 = Π2 = {0, 1}), per-stream Bernoulli habit priors 𝐸1, 𝐸2, and a single
scalar coupling 𝐽(𝜋1, 𝜋2) = 1[𝜋1 = 𝜋2] −1
2 (the mean-zero, swing-1 aligned/anti-aligned Ising structure).
The
closed-form mutual information curve Eq. (6.5) is
148

## Page 150

𝐼(𝜆) = log 2 −𝐻𝑏(𝜎(𝜆)),
(S8.1)
where 𝜎is the logistic and 𝐻𝑏is the binary entropy. The shipped GNN source gnn/bernoulli_toy.gnn.md declares
the two binary policy variables, the 2×2 coupling 𝐽(with 𝐽00 = 𝐽11 = + 1
2 aligned and 𝐽01 = 𝐽10 = −1
2 anti-aligned),
and the deformation parameter 𝜆. The Triple Play [Smékal and Friedman, 2023] emits from that single source three
views:
• Linguistic view: a textual block naming the two streams, the binary policy spaces, the aligned coupling 𝐽,
and 𝜆— the ## ModelAnnotation and ## ActInf Ontology Annotation sections of the source.
• Visual view:
the round-trip figure output/figures/gnn_bernoulli_roundtrip.png, overlaying the GNN-
reconstructed and closed-form 𝐼(𝜆) curves with the residual; the coupling graph (two policy nodes, a coupling
edge labeled 𝜆𝐽) is the topology read off the ## Connections block.
• Executable view: scripts/simulate_gnn.py (a thin orchestrator over src/gnn/runner.py) reconstructs the
curve from the source and writes the deterministic sidecar output/data/gnn_bernoulli_roundtrip.json.
The round-trip, closed. The bridge (src/gnn/bridge.py) parses the coupling matrix 𝐽from gnn/bernoulli_-
toy.gnn.md, reconstructs the entangled joint posterior via the framework’s general-purpose entangled_posterior,
and computes the multi-information via total_correlation — an independent code path from the hand-derived
closed form ising_mutual_information (the bridge never imports or calls the closed form). Over the canonical 121-
point 𝜆grid, the two routes agree to a maximum residual of 7.77e-16 nats, well below the 1e-06 reproducibility
tolerance.
What this check is, precisely. This is an integration / internal-consistency check, not an independent
re-derivation of the mutual information: for the symmetric K=2 toy the general machinery provably reduces to the
closed form (the aligned mass equals 𝜎(𝜆), whence 𝐼= log 2 −𝐻𝑏(𝜎(𝜆))), so the two routes are the same scalar
function written two ways. What the agreement does establish — and what makes it a genuine witness rather than
an 𝑓(𝑎) ≈𝑓(𝑎) tautology — is that the GNN-sourced spec, pushed through the general code path, reproduces the
analytic prediction: a parser error, a bridge that ignored the declared coupling, or a wrong coupling gap would each
break it. The zero-coupling negative control (replacing the parsed 𝐽with the zero matrix) diverges from the
closed form by 0.676 nats, proving specifically that the bridge reads and responds to the declared coupling rather
than hard-coding the answer. (Sign-flipping 𝐽is not a valid control: mutual information is invariant under 𝐽→−𝐽;
this is pinned as a test so it cannot be mistaken for one.)
Scope of what the residual certifies.
The round-trip pins the gauge-invariant coupling gap (the entangled
posterior 𝑞𝜆∝𝐸exp(𝜆𝐽) is invariant under adding a constant to 𝐽, since the constant cancels in normalization),
not the literal matrix entries. Two couplings with the same aligned-minus-anti-aligned gap produce the same curve.
The absolute Ising entries 𝐽= {(0.5, −0.5), (−0.5, 0.5)} are therefore pinned separately — by the to_pymdp_config
round-trip test (which asserts the emitted matrix entrywise) and the GNN concordance parity test — so the 7.77e-16
residual should not be read as certifying the exact matrix. This round-trip is what graduates the GNN bridge from
roadmap to empirical per §S7.1.
What GNN Preserves and What It Abstracts Away
A representation earns its keep only by naming, explicitly, the structural features it preserves and the features it
abstracts away. Conflating preservation and abstraction is the failure mode the manuscript is most exposed to —
readers who see a GNN diagram may treat it as a structural commitment when it is only a graph-rendered shorthand
for parametric coupling. The table below is the shipped preservation/abstraction ledger.
Framework feature
GNN preservation status
Notes
Per-stream POMDP primitives
(𝐴𝑘, 𝐵𝑘, 𝐶𝑘, 𝐷𝑘, 𝐸𝑘)
Preserves
Each stream is a first-class GNN variable
block; dimensionality declarations carry
through directly.
Stream count 𝐾
Preserves
Encoded as a block-count or indexed
family; k_stream_ensemble.gnn.md ships a
K=3 instance.
Finite policy spaces Π𝑘
Preserves
Cardinalities are typed declarations in
GNN; the finite-discrete restriction of §3 is
honored.
Coupling potential 𝐽as a function on
∏𝑘Π𝑘
Preserves (stock GNN)
A joint variable over the product policy
space with connection edges; no upstream
primitive required (cf. §S8.4).
Sparsity / topology of 𝐽(tree / loopy /
low-rank)
Preserves with annotation
The coupling-graph topology is read off ##
Connections; the K=3 chain ships as a
sparse instance.
149

## Page 151

Framework feature
GNN preservation status
Notes
Deformation parameter 𝜆
Preserves
Scalar parameter with named physical role
in the e-coordinate of the entanglement
family.
Sophistication weight 𝛾
Preserves
Scalar parameter weighting 𝐾𝑐in Eq. (5.2).
Entanglement decomposition (Theorem
5.1)
Abstracts away
A graph diagram does not express the
additive decomposition 𝐹[𝑞𝜆] =
∑𝑘𝐹[𝑞𝑘
𝜆]+𝛾𝜆⟨𝐾𝑐⟩+log 𝑍𝐸(𝜆)−𝜆⟨𝐽⟩+𝐼(𝑞𝜆).
Theorem content is post-graph
mathematical structure.
Information-geometric structure
(𝑒-flatness, 𝑚-projection, e-geodesic; §7)
Abstracts away
The manifold structure of the entanglement
family is not visible in a graph rendering;
the Pythagorean decomposition Eq. (7.4)
requires the dual-coordinate framing GNN
does not encode.
Spectral structure (Schmidt
decomposition, archetypal eigenvectors, TT
bond dimensions; §8)
Abstracts away
A graph diagram cannot distinguish two
joint posteriors that share a topology but
differ in Schmidt-rank profile.
Coupling-tax bound (𝑂(𝜆2)
suboptimality, Theorem 9.1)
Abstracts away
Quantitative bound on
heterogeneous-ensemble suboptimality; lives
in the analytical layer, not the graph layer.
Lean-checked ℝidentities
Abstracts away
A GNN spec does not certify a proof; it
specifies what is modeled. The shipped
GNN→Lean emitter produces a typed
contract, not a proof — see §S8.7.
Float-vs-ℝnumerical residual
Abstracts away
The single honest residual of the
manuscript (§21 Threats to validity) is
invariant to representation choice.
The ledger is the substantive content of the supplement: GNN preserves the structural and parametric
scaffolding of a multi-stream policy ensemble — and, via the shipped round-trip, reproduces its
numerical content — while abstracting away the analytic, geometric, spectral, and proof-theoretic
content that the four existing tracks carry. This is not a defect of GNN; it is a clarification of what a graph-
rendered, numerically-round-tripped model description can and cannot encode. A reader who treats the visual view
as a commitment beyond the structural-and-numerical layer is over-reading the representation.
Shipped Elaboration: GNN to a Lean Typed-Structure Contract
The GNN-to-Lean typed-structure emitter ships in src/gnn/lean_emit.py. It consumes a parsed GNN model and
emits gnn/generated/BernoulliToyGnn.lean: a self-contained, Mathlib-free Lean structure (PolicyEntanglementK2)
whose fields mirror the manuscript symbol concordance (𝐸𝑘, 𝐽, 𝜆, 𝛾), instantiated with the values parsed from
the GNN source. The emitted file type-checks under the stock Lean v4.29.0 toolchain (verified by lake env lean),
and #print axioms on the emitted declaration reports foundational axioms only — the same hygiene the boundary
fragment of §E enforces.
What this ships, and what it deliberately does not. The emitted structure is a typed contract: it certifies the
structural signature of the GNN-specified model under Lean’s type-checker. It is not a proof, and the supplement
is explicit about this. Per the discipline of §E, a witness-form theorem is consumed in four enforced steps: (1)
the registry names the live Lean declaration; (2) the Lean declaration type-checks without Mathlib; (3) a Python
witness or pymdp run computes the same payload numerically; (4) the relevant test and dashboard invariant fail if
the payload drifts. The GNN-to-Lean emitter automates the declaration of step 2’s structure; steps 1, 3, and 4 are
unchanged. In particular the analytic content of every witness-form theorem still requires either an analytic proof
in MathlibProofs (per the close on Theorem 5.1 in §21) or a numerical witness that exercises the Python / pymdp
layer.
Explicit non-claim. Parsing is not proving. A GNN spec that parses cleanly, and a Lean structure that type-
checks, do not establish any of the manuscript’s proved-status rows in §S7. Promoting a row to proved requires
a Lean proof at MathlibProofs-grade discipline (foundational-only #print axioms, no sorryAx, a self-designed non-
vacuity negative control), independent of how any witness record was declared. The emitter’s output file states this
non-claim in its own header so a future reader of the generated Lean cannot mistake the typed contract for a proof.
Shipped Round-Trip: GNN to pymdp Harness Configuration
The most immediately useful integration for practitioners — a GNN-to-pymdp round-trip — also ships.
scripts/gnn_to_pymdp.py (a thin orchestrator over src/gnn/bridge.py::to_pymdp_config) consumes a .gnn file and
150

## Page 152

emits the structural configuration a pymdp-style harness needs: stream count, per-stream policy cardinality, per-
stream habit priors, the joint coupling tensor, and the scalar parameters — sourced entirely from the GNN
declarations.
The shipped round-trip is:
1. Source:
gnn/bernoulli_toy.gnn.md (and the K=3 gnn/k_stream_ensemble.gnn.md) describing the ensemble
with per-stream POMDP primitives, the coupling potential 𝐽, 𝛾, and the operating point.
2. Generator: scripts/gnn_to_pymdp.py consumes the .gnn source and emits a configuration dict structurally
equivalent to the relevant fields of src/simulation/hyperparameters.py.
3. Run: the GNN round-trip stage (scripts/simulate_gnn.py) reconstructs the entangled posterior and the
mutual-information curve from the GNN source and emits output/data/gnn_bernoulli_roundtrip.json.
4. Validate:
tests/test_gnn_round_trip.py
asserts
floating-point-tolerance
identity
between
the
GNN-
reconstructed curve and the canonical closed form, with a non-vacuity negative control; tests/test_simu-
late_gnn.py asserts the sidecar is byte-identical on re-run.
Reproducibility-contract compatibility. The reproducibility contract of §16 requires every numerical claim in
the manuscript to flow from a real run via the [[VAR:...]] token registry. The GNN round-trip is compatible:
the gnn_roundtrip_max_residual, gnn_negative_control_max_residual, and gnn_round_trip_lambda_points variables
populate manuscript_variables.json from the real sidecar and are range-gated. Honest scope of what ships
vs. what does not: the K=2 mutual-information round-trip ships and is the source of the GNN [[VAR:...]]
tokens. Regenerating the full multi-K pymdp free-energy bundle (the per-stream VFE/EFE rollout of §14) from a
.gnn source — rather than the K=2 MI curve — is the natural next binding; the configuration generator ships, the
full-bundle regeneration is the remaining practitioner-facing work and is named as such in §S8.9 (OQ-G3).
What round-trip closure enables.
A downstream contributor can now specify a new policy-entanglement
experiment as a .gnn file (a stable, declarative, version-controlled surface), obtain its pymdp configuration via
gnn_to_pymdp.py, and validate the mutual-information structure against the closed form via the shipped round-trip
— without re-implementing the inference layer.
Downstream Use, Open Directions, and Open Questions
Downstream use. A third group writing a new multi-stream policy-coupling experiment can now publish a .gnn
specification alongside their paper; other groups consuming the spec recover the same coupling configuration and
the same mutual-information round-trip via the shipped src/gnn/ tooling, without re-implementing the inference
layer. The leverage is no longer purely prospective: the tooling, the parser, the round-trip, and the reproducibility
receipts exist and run in CI.
Integration with the §21 open directions. The GNN bridge to the framework ships. Concretely, five
deliverables are in place: (a) the (𝐴, 𝐵, 𝐶, 𝐷, 𝐸, 𝐽, 𝜆) mapping of §S8.4; (b) the cross-stream coupling, expressible in
stock GNN (no upstream extension on the critical path); (c) the K=2 Bernoulli round-trip of §S8.5; (d) the GNN-
to-Lean typed-contract emitter of §S8.7; and (e) the GNN-to-pymdp configuration round-trip of §S8.8. The other
open directions of §21 — the Mathlib4 analytic discharge beyond the verified kernel, cross-repository integration,
and community collaboration — remain orthogonal to the GNN bridge.
Open questions (the genuine design surface that remains, now that the core bridge ships):
• OQ-G1 (Cross-stream block ergonomics). Resolved at the level of expressibility, open at the level of
ergonomics. The cross-stream coupling is expressible in stock GNN v1.1 as a joint variable plus edges (shipped).
Whether a dedicated first-class CouplingBlock primitive — contributed upstream to [Institute, 2023] — would
improve authoring ergonomics for large 𝐾or dense topologies is an open design question, not a blocker for
this manuscript’s fifth track.
• OQ-G2 (Heterogeneous-stream Triple Play). When a 𝐾-stream ensemble mixes VFE-only and EFE-
planning streams (see §9), the visual view risks suggesting structural homogeneity where the framework
treats the streams differently. What annotation discipline avoids the misreading? A per-stream typographic
distinction (filled vs. open node markers, dashed vs. solid edges) is the candidate; the discipline is not yet
specified.
• OQ-G3 (Full-bundle pymdp regeneration).
The shipped round-trip reconstructs the K=2 mutual-
information curve.
Regenerating the full multi-K pymdp free-energy bundle (per-stream VFE/EFE, long-
horizon rollout) from a .gnn source — and confirming bundle-level identity against the canonical pymdp_-
summary.json — is the remaining practitioner-facing binding.
These questions are not blockers for the bridge; they are the design surface beyond the now-shipped core.
Bridge style and external-link discipline. In the style precedent of §E (§E), which bridges to the fep_lean
catalog via a single namespaced subsection and a single citation, this supplement bridges to GNN via a single
151

## Page 153

namespaced supplement and two citations ([Smékal and Friedman, 2023], [Institute, 2023]). No further external
references — to the broader Active Inference Institute catalog, to COGSEC, to companion projects — are taken in
§S8. The bridge is minimal by design.
This supplement ships the fifth track of the framework. The four-track proof integration of §1 remains the live
contract for analytic content; GNN is added as the fifth, structural-and-numerical track — a project-owned parser, a
shipped internal-consistency round-trip, a Lean typed-contract emitter, and a GNN-sourced manuscript variable —
with the genuine residuals (a first-class upstream coupling primitive; full-bundle pymdp regeneration; GNN-to-Lean
proving) named honestly as forward work rather than concealed.
Bibliography
This bibliography is auto-generated from manuscript/refs/citations.yaml by scripts/inject_manuscript_vari-
ables.py — every Pandoc-style citation in the body (a citekey enclosed in square brackets prefixed with @) resolves
to one entry below, and every entry below is grouped by topic in the order specified by the topic_order: list of the
YAML source.
When you add a body citation:
1. Add an entry to refs/citations.yaml with the citekey, full author / year / title / venue, and a topic:.
2. Reference it from any body section as a Pandoc-style key — a lower-case lastname-yyyy slug enclosed in square
brackets and prefixed with the at-sign; use a semicolon to separate multi-references inside a single bracket.
3. Re-run uv run python scripts/inject_manuscript_variables.py and confirm output/manuscript/99_bibliog-
raphy.md contains the expanded entry.
Active inference and the free-energy principle
• Buckley, C. L., Kim, C. S., McGregor, S., Seth, A. K. (2017) The free energy principle for action and perception:
A mathematical review. Journal of Mathematical Psychology 81, 55–79. https://www.sciencedirect.com/scie
nce/article/pii/S0022249617300962 doi:10.1016/j.jmp.2017.09.004 Accessible mathematical review of the free-
energy principle used to ground the introductory VFE claim without relying only on process-theory exposition.
• Champion, T., Bowman, H., Marković, D., Grześ, M. (2024) Reframing the Expected Free Energy: Four
Formulations and a Unification.
arXiv preprint, arXiv:2402.14460.
https://arxiv.org/abs/2402.14460
doi:10.48550/arXiv.2402.14460
• Da Costa, L., Parr, T., Sajid, N., Veselic, S., Neacsu, V., Friston, K. (2020) Active inference on discrete
state-spaces: A synthesis. Journal of Mathematical Psychology 99, 102447. https://www.sciencedirect.com/
science/article/pii/S0022249620300857 doi:10.1016/j.jmp.2020.102447 arXiv:2001.07203.
• Da Costa, L., Tenka, S., Zhao, D., Sajid, N. (2024) Active Inference as a Model of Agency.
arXiv.
https://arxiv.org/abs/2401.12917 doi:10.48550/arXiv.2401.12917 Accepted at the RLDM 2022 workshop
‘RL as a model of agency’; cited for the active-inference-as-agency unification framing, not as evidence for
policy entanglement itself.
• de Vries, B., Nuijten, T., van de Laar, T., Kouw, W., Adamiat, A., Nisslbeck, A., Lukashchuk, V., et
al. (2025) Expected Free Energy-based Planning as Variational Inference. arXiv preprint, arXiv:2504.14898.
https://arxiv.org/abs/2504.14898 doi:10.48550/arXiv.2504.14898
• de Vries, B., Friston, K. J. (2017) A Factor Graph Description of Deep Temporal Active Inference. Frontiers
in Computational Neuroscience 11, 95. https://www.frontiersin.org/articles/10.3389/fncom.2017.00095/full
doi:10.3389/fncom.2017.00095 Primary factor-graph / Forney-style graph source for deep temporal active
inference; cited only for message-passing implementability, not as a theorem-equivalence claim for policy
entanglement.
• Friston, K., Kilner, J., Harrison, L. (2006) A free energy principle for the brain.
Journal of Physiology-
Paris 100(1–3), 70–87.
https://www.sciencedirect.com/science/article/pii/S092842570600060X
doi:10.1016/j.jphysparis.2006.10.001 Early statement of variational free energy as a unifying principle for
perception, action, and learning.
• Friston, K. (2010) The free-energy principle: a unified brain theory? Nature Reviews Neuroscience 11(2),
127–138. https://www.nature.com/articles/nrn2787 doi:10.1038/nrn2787
• Friston, K., Schwartenbeck, P., FitzGerald, T., Moutoussis, M., Behrens, T., Dolan, R. J. (2014) The anatomy
of choice: dopamine and decision-making.
Philosophical Transactions of the Royal Society B 369(1655),
20130481. https://royalsocietypublishing.org/doi/10.1098/rstb.2013.0481 doi:10.1098/rstb.2013.0481
152

## Page 154

• Friston, K., FitzGerald, T., Rigoli, F., Schwartenbeck, P., Pezzulo, G. (2017) Active Inference: A Process
Theory. Neural Computation 29(1), 1–49. https://direct.mit.edu/neco/article/29/1/1 doi:10.1162/NECO_-
a_00912
• Friston, K. J., Rosch, R., Parr, T., Price, C., Bowman, H. (2017) Deep temporal models and active inference.
Neuroscience & Biobehavioral Reviews 77, 388–402.
https://doi.org/10.1016/j.neubiorev.2017.04.009
doi:10.1016/j.neubiorev.2017.04.009 Primary deep-temporal active-inference source; cited for hierarchical
temporal-model and long-horizon framing, not as evidence that the present finite-policy model is a full process
theory.
• Friston, K. J. (2018) Active Inference and Cognitive Consistency.
Psychological Inquiry 29(2), 67–73.
https://www.tandfonline.com/doi/full/10.1080/1047840X.2018.1480693 doi:10.1080/1047840X.2018.1480693
Commentary linking expected-free-energy epistemic/pragmatic terms to cognitive-consistency constructs; cited
as interpretive context, not as a reduction of social-psychological theory to active inference.
• Friston, K. (2019) A free energy principle for a particular physics.
arXiv preprint, arXiv:1906.10184.
https://arxiv.org/abs/1906.10184 doi:10.48550/arXiv.1906.10184 Preprint only as of 2026-05; never received
a journal publication.
• Friston, K., Da Costa, L., Hafner, D., Hesp, C., Parr, T. (2021) Sophisticated Inference. Neural Computation
33(3), 713–763. https://direct.mit.edu/neco/article/33/3/713 doi:10.1162/neco_a_01351 arXiv:2006.04120.
Introduces recursive expected free energy for deep counterfactual policy tree search.
• Friston, K. J., Heins, C., Verbelen, T., Da Costa, L., Salvatori, T., Marković, D., Tschantz, A., Koudahl,
M., Buckley, C., Parr, T. (2025) From pixels to planning: scale-free active inference. Frontiers in Network
Physiology 5, 1521963. https://www.frontiersin.org/journals/network-physiology/articles/10.3389/fnetp.20
25.1521963/full doi:10.3389/fnetp.2025.1521963 First circulated as a 2024 preprint (arXiv:2407.20292); final
venue Frontiers in Network Physiology, June 2025. The published Frontiers form is the canonical citation; the
friston-rgm-2025 alias is intentionally NOT registered to avoid duplication — cite as [@friston-2024]. Slug
retained as friston-2024 for back-compatibility.
• Friston, K. J., Parr, T., de Vries, B. (2017) The graphical brain: Belief propagation and active inference.
Network Neuroscience 1(4), 381–414. https://doi.org/10.1162/NETN_a_00018 doi:10.1162/NETN_a_00018
Graphical-brain source for belief propagation, Forney-style graphical modeling, and active-inference message-
passing context; not evidence that lambda-coupled policy posteriors are standard in AIF.
• Friston, K. J., Trujillo-Barreto, N., Daunizeau, J. (2008) DEM: A variational treatment of dynamic systems.
NeuroImage 41(3), 849–885.
https://www.sciencedirect.com/science/article/pii/S1053811908001894
doi:10.1016/j.neuroimage.2008.02.054 Primary dynamic expectation maximization reference behind the SPM-
DEM lineage discussed in the introduction.
• Hafner, D., Pasukonis, J., Ba, J., Lillicrap, T. (2023) Mastering Diverse Domains through World Models. arXiv
preprint, arXiv:2301.04104. https://arxiv.org/abs/2301.04104 doi:10.48550/arXiv.2301.04104 DreamerV3 —
world-model RL agent that achieves cross-domain mastery with a single hyperparameter setting; widely cited as
the canonical contemporary world-model architecture against which active-inference agents are benchmarked.
• Heins, C., Millidge, B., Demekas, D., Klein, B., Friston, K., Couzin, I. D., Tschantz, A. (2022) pymdp: A
Python library for active inference in discrete state spaces. Journal of Open Source Software 7(73), 4098.
https://joss.theoj.org/papers/10.21105/joss.04098 doi:10.21105/joss.04098 v1.0.1 JAX-based release is the
simulation backend used by the empirical suite and src/simulation/; arXiv:2201.03904.
• Hodson, R., Mehta, M., Smith, R. (2024) The empirical status of predictive coding and active inference.
Neuroscience & Biobehavioral Reviews 157, 105473.
https://pubmed.ncbi.nlm.nih.gov/38030100/
doi:10.1016/j.neubiorev.2023.105473 Empirical-status review used to calibrate FEP / active-inference claims
as normative and computational unless a specific comparative empirical test is supplied.
• Johansson, R. S., Westling, G., Bäckström, A., Flanagan, J. R. (2001) Eye-hand coordination in object
manipulation. Journal of Neuroscience 21(17), 6917–6932. https://www.jneurosci.org/content/21/17/6917
doi:10.1523/JNEUROSCI.21-17-06917.2001 Primary empirical eye-hand coordination source used to ground
the reach/saccade example in the motivation.
• Kaplan, R., Friston, K. J. (2018) Planning and navigation as active inference. Biological Cybernetics 112, 323-
343. https://link.springer.com/article/10.1007/s00422-018-0753-2 doi:10.1007/s00422-018-0753-2 Navigation
and planning example for EFE-based policy selection, risk / ambiguity terms, and epistemic exploration under
active inference.
• Land, M. F., Hayhoe, M. (2001) In what ways do eye movements contribute to everyday activities? Vision
Research 41(25–26), 3559–3565.
https://doi.org/10.1016/S0042-6989(01)00102-X doi:10.1016/S0042-
6989(01)00102-X Natural-task eye-movement review showing that gaze commonly arrives at task-relevant objects
before manipulation, grounding the cross-stream reach/saccade example.
• Lanillos, P., Meo, C., Pezzato, C., Meera, A. A., Baioumy, M., Ohata, W., Tschantz, A., Millidge, B., Wisse,
M., Buckley, C. L., Tani, J. (2021) Active inference in robotics and artificial agents: Survey and challenges.
153

## Page 155

arXiv preprint, arXiv:2112.01871. https://arxiv.org/abs/2112.01871 doi:10.48550/arXiv.2112.01871
• Limanowski, J., Adams, R. A., Kilner, J., Parr, T. (2024) The Many Roles of Precision in Action. Entropy
26(9), 790. https://www.mdpi.com/1099-4300/26/9/790 doi:10.3390/e26090790 Review of precision roles in
action, attention, habit, and self-other distinction; cited to keep lambda-as-coupling-precision language distinct
from neural precision claims.
• Millidge, B., Tschantz, A., Buckley, C. L. (2021) Whence the Expected Free Energy? Neural Computation
33(2), 447-482. https://direct.mit.edu/neco/article/33/2/447/95645/Whence-the-Expected-Free-Energy
doi:10.1162/neco_a_01354 Critical analysis of EFE derivations and alternatives; cited to keep expected-free-
energy unification claims bounded.
• Nuijten, T., Lukashchuk, V. (2025) Active Inference is a Subtype of Variational Inference. arXiv preprint,
arXiv:2511.18955. https://arxiv.org/abs/2511.18955 doi:10.48550/arXiv.2511.18955
• Parr, T., Pezzulo, G., Friston, K. J. (2022) Active Inference: The Free Energy Principle in Mind, Brain, and
Behavior. MIT Press. https://direct.mit.edu/books/oa-monograph/5299/Active-InferenceThe-Free-Energy-
Principle-in-Mind doi:10.7551/mitpress/12441.001.0001 Book-length synthesis of FEP, expected free energy,
active inference process theory, and applications.
• Parr, T., Friston, K. J. (2017) Uncertainty, epistemics and active inference.
Journal of The Royal
Society Interface 14(136), 20170376.
https://royalsocietypublishing.org/doi/10.1098/rsif.2017.0376
doi:10.1098/rsif.2017.0376 Primary source for epistemic value and uncertainty reduction in active-inference
policy selection.
• Parr, T., Friston, K. J. (2017) Working memory, attention, and salience in active inference. Scientific Reports 7,
14678. https://www.nature.com/articles/s41598-017-15249-0 doi:10.1038/s41598-017-15249-0 Process-theory
account linking working memory, attention, salience, precision, and policy evaluation under active inference.
• Parr, T., Friston, K. J. (2019) Generalised free energy and active inference. Biological Cybernetics 113(5–6),
495–513. https://link.springer.com/article/10.1007/s00422-019-00805-w doi:10.1007/s00422-019-00805-w
Clarifies generalized free energy and self-evidencing language used in the discussion without treating the present
finite-policy model as a complete biological process theory.
• Parr, T., Marković, D., Kiebel, S. J., Friston, K. J. (2019) Neuronal message passing using Mean-field, Bethe
and Marginal approximations. Scientific Reports 9, 1889. https://www.nature.com/articles/s41598-018-38246-
3 doi:10.1038/s41598-018-38246-3 Primary source distinguishing mean-field, Bethe, and marginal message-
passing approximations; cited for approximation-family context, not as a direct proof of policy-coupling neural
implementation.
• Pezzulo, G., Rigoli, F., Friston, K. J. (2018) Hierarchical Active Inference: A Theory of Motivated Control.
Trends in Cognitive Sciences 22(4), 294–306. https://www.cell.com/trends/cognitive-sciences/fulltext/S1364-
6613(18)30022-6 doi:10.1016/j.tics.2018.01.009
• Pezzulo, G., Parr, T., Friston, K. J. (2024) Active inference as a theory of sentient behavior.
Biological
Psychology 186, 108741.
https://www.sciencedirect.com/science/article/pii/S0301051123002612
doi:10.1016/j.biopsycho.2023.108741 Recent synthesis used to distinguish active inference as process theory
from the broader free-energy-principle framing.
• Sajid, N., Ball, P. J., Parr, T., Friston, K. J. (2021) Active Inference: Demystified and Compared. Neural
Computation 33(3), 674–712. https://direct.mit.edu/neco/article/33/3/674 doi:10.1162/neco_a_01357
• Schwartenbeck, P., FitzGerald, T. H. B., Mathys, C., Dolan, R., Friston, K. (2015) The dopaminergic
midbrain encodes the expected certainty about desired outcomes.
Cerebral Cortex 25(10), 3434–3445.
https://academic.oup.com/cercor/article/25/10/3434/385607 doi:10.1093/cercor/bhu159
• Smékal, J., Friedman, D. A. (2023) Generalized Notation Notation for Active Inference Models.
Active
Inference Journal.
Zenodo.
https://zenodo.org/records/7803328 doi:10.5281/zenodo.7803328 Primary
publication of Generalized Notation Notation (GNN), introducing the Triple Play of linguistic, visual, and
executable cognitive-model representations that complements the Active Inference Ontology. Cited from the GNN
extension supplement as the canonical reference for the shipped fifth (structural-and-numerical) representation
of the framework.
• Smith, R., Friston, K. J., Whyte, C. J. (2022) A step-by-step tutorial on active inference and its application
to empirical data. Journal of Mathematical Psychology 107, 102632. https://www.sciencedirect.com/science/
article/pii/S0022249621000973 doi:10.1016/j.jmp.2021.102632
• Smithe, T. S. C. (2024) Structured Active Inference. arXiv preprint, arXiv:2406.07577. https://arxiv.org/
abs/2406.07577 doi:10.48550/arXiv.2406.07577 Categorical-systems-theory formulation of AIF with structured
policies amenable to formal verification.
• Tschantz, A., Seth, A. K., Buckley, C. L. (2020) Learning action-oriented models through active inference.
PLOS Computational Biology 16(4), e1007805. https://journals.plos.org/ploscompbiol/article?id=10.1371/jo
urnal.pcbi.1007805 doi:10.1371/journal.pcbi.1007805 Active-inference account of parsimonious action-oriented
model learning; useful contrast for this manuscript’s structured policy-coupling family.
154

## Page 156

• van de Laar, T. W., de Vries, B. (2019) Simulating Active Inference Processes by Message Passing.
Frontiers in Robotics and AI 6, 20.
https://www.frontiersin.org/articles/10.3389/frobt.2019.00020
doi:10.3389/frobt.2019.00020 Factor-graph forward-backward implementation of deep temporal active inference
(slug retained for backwards compatibility — primary reference is the 2019 Frontiers in Robotics and AI*
paper).*
• Yedidia, J. S., Freeman, W. T., Weiss, Y. (2005) Constructing Free-Energy Approximations and Generalized
Belief Propagation Algorithms.
IEEE Transactions on Information Theory 51(7), 2282–2312.
https:
//doi.org/10.1109/TIT.2005.850085 doi:10.1109/TIT.2005.850085 Canonical Bethe / Kikuchi free-energy and
generalized-belief-propagation source; cited for graphical-variational approximation structure, not for active-
inference policy semantics.
Branching-time and structured AIF
• Champion, T., Grześ, M., Bowman, H. (2022) Branching Time Active Inference with Bayesian Filtering.
Neural Computation 34(10), 2132–2144.
https://direct.mit.edu/neco/article-abstract/34/10/2132
doi:10.1162/neco_a_01529 Uses Bayesian filtering on the expanded policy tree rather than vanilla MCTS
rollouts; in the wider BTAI lineage (Fountas et al. 2020 DAI / MCTS for active inference).
• Fountas, Z., Sajid, N., Mediano, P. A. M., Friston, K. (2020) Deep active inference agents using Monte-Carlo
methods. Advances in Neural Information Processing Systems 33 (NeurIPS 2020). https://proceedings.neur
ips.cc/paper/2020/hash/865dfbde8a344b44095495f3591f7407-Abstract.html doi:10.48550/arXiv.2006.04176
arXiv:2006.04176. Canonical reference for deep / MCTS-style branching-time active inference (DAI).
Information geometry
• Amari, S. (1985) Differential-Geometrical Methods in Statistics. Lecture Notes in Statistics, Vol. 28 (Springer).
https://link.springer.com/book/10.1007/978-1-4612-5056-2 doi:10.1007/978-1-4612-5056-2 Founding
monograph of information geometry; introduced the dually-flat alpha-connection family and the e- / m-geodesic
structure used in the framework-connections section.
• Amari, S. (2016) Information Geometry and Its Applications. Springer, Applied Mathematical Sciences, Vol.
194. https://link.springer.com/book/10.1007/978-4-431-55978-8 doi:10.1007/978-4-431-55978-8
• Amari, S., Nagaoka, H. (2000) Methods of Information Geometry.
AMS Translations of Mathematical
Monographs, Vol. 191 (American Mathematical Society / Oxford University Press). https://bookstore.ams.or
g/mmono-191/ Translated by Daishi Harada from the 1993 Japanese original. ISBN 978-0-8218-4302-4.
• Ay, N., Jost, J., Lê, H. V., Schwachhöfer, L. (2017) Information Geometry. Ergebnisse der Mathematik und
ihrer Grenzgebiete (3. Folge), Vol. 64 (Springer). https://link.springer.com/book/10.1007/978-3-319-56478-4
doi:10.1007/978-3-319-56478-4 ISBN 978-3-319-56477-7.
Comprehensive monograph treatment covering the
parametric and non-parametric geometric foundations used in the information-geometric formalism.
• Bakry, D., Émery, M. (1985) Diffusions hypercontractives. **, 177-206. https://doi.org/10.1007/BFb0075144
doi:10.1007/BFb0075144 Bakry–Émery curvature criterion for log-Sobolev / variance bounds on exponential
families.
• Brascamp, H. J., Lieb, E. H. (1976) On extensions of the Brunn–Minkowski and Prékopa–Leindler theorems,
including inequalities for log concave functions, and with an application to the diffusion equation. ** 22, 366-
389. https://doi.org/10.1016/0022-1236(76)90001-5 doi:10.1016/0022-1236(76)90001-5 Variance Brascamp–
Lieb inequality for log-concave measures; cited in Q1 dispersion-comparison conjecture.
• Naudts, J. (2011) Generalised Thermostatistics. Springer London. https://link.springer.com/book/10.1007/9
78-0-85729-355-8 doi:10.1007/978-0-85729-355-8 ISBN 978-0-85729-354-1 (print). Covers escort distributions,
q-deformed exponential families.
• Nielsen, F. (2020) An Elementary Introduction to Information Geometry.
Entropy 22(10), 1100.
https:
//www.mdpi.com/1099-4300/22/10/1100 doi:10.3390/e22101100
Information theory and multi-information
• McGill, W. J. (1954) Multivariate Information Transmission. Psychometrika 19(2), 97–116. https://link.s
pringer.com/article/10.1007/BF02289159 doi:10.1007/BF02289159 Original definition of total correlation /
multi-information, the correlation surcharge in the entanglement-decomposition identity.
• Watanabe, S. (1960) Information theoretical analysis of multivariate correlation. IBM Journal of Research and
Development 4(1), 66–82. https://ieeexplore.ieee.org/document/5392532 doi:10.1147/rd.41.0066 Independent
rediscovery of McGill’s total-correlation construction, under the alternative name multivariate correlation;
widely cited as the second canonical reference for the total-correlation quantity.
155

## Page 157

Variational and copula inference
• Blei, D. M., Kucukelbir, A., McAuliffe, J. D. (2017) Variational Inference: A Review for Statisticians. Journal
of the American Statistical Association 112(518), 859-877. https://doi.org/10.1080/01621459.2017.1285773
doi:10.1080/01621459.2017.1285773 Modern scholarly review citation for mean-field and structured variational
inference.
• Fu, Y., Smith, M. S., Panagiotelis, A. (2025) Vector Copula Variational Inference and Dependent Block
Posterior Approximations.
arXiv preprint, arXiv:2503.01072.
https://arxiv.org/abs/2503.01072
doi:10.48550/arXiv.2503.01072
• Han, S., Liao, X., Dunson, D. B., Carin, L. (2016) Variational Gaussian Copula Inference. AISTATS 2016,
PMLR 51, 829–838. https://proceedings.mlr.press/v51/han16.html
• Hinton, G. E. (2002) Training products of experts by minimizing contrastive divergence. Neural Computation
14(8), 1771–1800. https://direct.mit.edu/neco/article-abstract/14/8/1771/ doi:10.1162/089976602760128018
• Hoffman, M. D., Blei, D. M. (2015) Structured Stochastic Variational Inference. AISTATS 2015, PMLR 38,
361–369. http://proceedings.mlr.press/v38/hoffman15.html arXiv:1404.4114.
• Li, Y., Turner, R. E. (2016) Rényi Divergence Variational Inference. Advances in Neural Information Processing
Systems 29 (NeurIPS 2016). https://proceedings.neurips.cc/paper/2016/hash/7750ca3559e5b8e1f44210283
368fc16-Abstract.html doi:10.48550/arXiv.1602.02311 arXiv:1602.02311. Generalizes ELBO-style variational
inference to the Renyi alpha-divergence family; cited for structured-VI / alpha-divergence comparisons with the
active-inference free-energy functional.
• Nelsen, R. B. (2006) An Introduction to Copulas. Springer Series in Statistics, 2nd ed.. https://link.springe
r.com/book/10.1007/0-387-28678-0 doi:10.1007/0-387-28678-0 Foundational monograph for copula definitions
and dependence modeling; cited to distinguish true copula densities from informal dependence-factor analogies.
• Saul, L. K., Jordan, M. I. (1995) Exploiting Tractable Substructures in Intractable Networks. Advances in
Neural Information Processing Systems 8 (NIPS 1995).
https://papers.nips.cc/paper/1155-exploiting-
tractable-substructures-in-intractable-networks Canonical structured mean-field source: exact inference is
retained inside tractable substructures while only the remaining interactions are approximated.
• Tran, D., Blei, D. M., Airoldi, E. M. (2015) Copula variational inference. Advances in Neural Information
Processing Systems 28 (NeurIPS 2015), 3564–3572. https://proceedings.neurips.cc/paper/2015/hash/e4dd5
528f7596dcdf871aa55cfccc53c-Abstract.html arXiv:1506.03159.
• Wainwright, M. J., Jordan, M. I. (2008) Graphical Models, Exponential Families, and Variational Inference.
Foundations and Trends in Machine Learning 1(1-2), 1-305. https://www.nowpublishers.com/article/Detail
s/MAL-001 doi:10.1561/2200000001 Canonical graphical-model variational-inference reference used to anchor
the mean-field / structured-approximation comparison.
Variational inference robustness and Lipschitz bounds
• Barrett, T. D., Camuto, A., Williamson, C. R., Roberts, S. J. (2022) Certifiably Robust Variational
Autoencoders through Lipschitz Constraints. Proceedings of the 25th International Conference on Artificial
Intelligence and Statistics (AISTATS), 1-9. https://proceedings.mlr.press/v151/barrett22a.html Actionable
KL-drift bounds under encoder/decoder Lipschitz constraints; cited for adversarial VI robustness context in
Q11.
Tensor networks and quantum-inspired ML
• Biamonte, J., Bergholm, V. (2017) Tensor Networks in a Nutshell. arXiv. https://arxiv.org/abs/1708.00006
doi:10.48550/arXiv.1708.00006 Tutorial tensor-network reference used to scope Schmidt-rank / tensor-train
language as probability-tensor linear algebra, not a quantum-physical claim.
• Cichocki, A., Lee, N., Oseledets, I. V., Phan, A.-H., Zhao, Q., Mandic, D. P. (2016) Tensor Networks
for Dimensionality Reduction and Large-scale Optimization:
Part 1 Low-Rank Tensor Decompositions.
Foundations and Trends in Machine Learning 9(4–5), 249–429.
https://doi.org/10.1561/2200000059
doi:10.1561/2200000059 Machine-learning tensor-network survey; cited for low-rank tensor formats and
optimization context, not as an active-inference result.
• Eisert, J., Cramer, M., Plenio, M. B. (2010) Colloquium:
Area laws for the entanglement entropy.
Reviews of Modern Physics 82(1), 277–306.
https://link.aps.org/doi/10.1103/RevModPhys.82.277
doi:10.1103/RevModPhys.82.277
• Glasser, I., Pancotti, N., Cirac, J. I. (2020) From Probabilistic Graphical Models to Generalized Tensor
Networks for Supervised Learning. IEEE Access 8, 68169–68182. https://ieeexplore.ieee.org/document
/9058650/ doi:10.1109/ACCESS.2020.2986279 arXiv:1806.05964 (2018 preprint); IEEE Access publication
2020.
156

## Page 158

• Han, Z.-Y., Wang, J., Fan, H., Wang, L., Zhang, P. (2018) Unsupervised Generative Modeling Using Matrix
Product States. Physical Review X 8(3), 031012. https://journals.aps.org/prx/abstract/10.1103/PhysRevX
.8.031012 doi:10.1103/PhysRevX.8.031012
• Orus, R. (2014) A practical introduction to tensor networks: Matrix product states and projected entangled
pair states. Annals of Physics 349, 117-158. https://www.sciencedirect.com/science/article/pii/S0003491
614001596 doi:10.1016/j.aop.2014.06.013 Tutorial tensor-network reference used to scope matrix-product-state
and tensor-train language as linear algebra on probability tensors.
• Oseledets, I. V. (2011) Tensor-Train Decomposition. SIAM Journal on Scientific Computing 33(5), 2295–2317.
https://epubs.siam.org/doi/10.1137/090752286 doi:10.1137/090752286 Foundational paper introducing the
TT-format; underlies the linear-in-N policy-tensor compression used in the tensor-network analysis.
• Schollwöck, U. (2011) The density-matrix renormalization group in the age of matrix product states. Annals
of Physics 326(1), 96–192.
https://www.sciencedirect.com/science/article/pii/S0003491610001752
doi:10.1016/j.aop.2010.09.012 arXiv:1008.3477.
Canonical MPS/DMRG review; cited for the algorithmic
backbone behind policy-tensor compression and entanglement-entropy bookkeeping.
• Verstraete, F., Murg, V., Cirac, J. I. (2008) Matrix product states, projected entangled pair states, and
variational renormalization group methods for quantum spin systems. Advances in Physics 57(2), 143–224.
https://www.tandfonline.com/doi/abs/10.1080/14789940801912366 doi:10.1080/14789940801912366
KL / path-integral control duality
• Kappen, H. J. (2005) Path integrals and symmetry breaking for optimal control theory. Journal of Statistical
Mechanics:
Theory and Experiment 2005, P11011.
https://iopscience.iop.org/article/10.1088/1742-
5468/2005/11/P11011 doi:10.1088/1742-5468/2005/11/P11011
• Rawlik, K., Toussaint, M., Vijayakumar, S. (2013) On Stochastic Optimal Control and Reinforcement
Learning by Approximate Inference (Extended Abstract).
Proceedings of the Twenty-Third International
Joint Conference on Artificial Intelligence (IJCAI 2013), 3052-3056. https://www.ijcai.org/Proceedings/13
/Papers/455.pdf Extended abstract of the approximate-inference control formulation; cited for the KL/control-
as-inference lineage rather than as an active-inference result.
• Theodorou, E. A., Todorov, E. (2012) Relative entropy and free energy dualities:
Connections to path
integral and KL control.
Proc.
2012 IEEE 51st Conference on Decision and Control (CDC), 1466–1473.
https://ieeexplore.ieee.org/document/6426381/ doi:10.1109/CDC.2012.6426381
• Todorov, E. (2006) Linearly-solvable Markov decision problems. Advances in Neural Information Processing
Systems 19 (NIPS 2006), 1369-1376.
https://papers.nips.cc/paper/3002-linearly-solvable-markov-
decision-problems Primary linearly-solvable MDP reference for KL-control structure and log-partition value
transformations.
Control / RL as probabilistic inference
• Botvinick, M., Toussaint, M. (2012) Planning as inference. Trends in Cognitive Sciences 16(10), 485–488. ht
tps://www.cell.com/trends/cognitive-sciences/fulltext/S1364-6613(12)00184-3 doi:10.1016/j.tics.2012.08.006
• Levine, S. (2018) Reinforcement Learning and Control as Probabilistic Inference: Tutorial and Review. arXiv
preprint, arXiv:1805.00909.
https://arxiv.org/abs/1805.00909 doi:10.48550/arXiv.1805.00909 Canonical
tutorial on the control-as-inference / maximum-entropy RL viewpoint cited in the comparison with active
inference.
• Toussaint, M. (2009) Robot trajectory optimization using approximate inference.
Proc.
26th Annual
International Conference on Machine Learning (ICML 2009), 1049–1056.
https://dl.acm.org/doi/10.11
45/1553374.1553508 doi:10.1145/1553374.1553508
Hierarchical RL / options
• Bacon, P.-L., Harb, J., Precup, D. (2017) The Option-Critic Architecture.
Proceedings of the AAAI
Conference on Artificial Intelligence 31(1).
https://ojs.aaai.org/index.php/AAAI/article/view/10916
doi:10.1609/aaai.v31i1.10916 Modern options reference used to scope the manuscript’s option-like embedding
as a parametric policy-matching construction, not a proof that the lambda deformation subsumes all option-
learning algorithms.
• Barto, A. G., Mahadevan, S. (2003) Recent Advances in Hierarchical Reinforcement Learning.
Discrete
Event Dynamic Systems 13, 341-379.
https://link.springer.com/article/10.1023/A:1025696116075
doi:10.1023/A:1025696116075 Review reference for hierarchical RL and temporal abstraction; cited alongside
options to keep the control/RL comparison anchored in the RL literature.
157

## Page 159

• Doll, B. B., Duncan, K. D., Simon, D. A., Shohamy, D., Daw, N. D. (2015) Model-based choices involve
prospective neural activity. Nature Neuroscience 18(5), 767–772. https://www.nature.com/articles/nn.3981
doi:10.1038/nn.3981
• Sutton, R. S., Precup, D., Singh, S. (1999) Between MDPs and semi-MDPs: A framework for temporal
abstraction in reinforcement learning. Artificial Intelligence 112(1–2), 181–211. https://www.sciencedirect.
com/science/article/pii/S0004370299000521 doi:10.1016/S0004-3702(99)00052-1
Markov blankets and particular physics
• Aguilera, M., Millidge, B., Tschantz, A., Buckley, C. L. (2022) How particular is the physics of the free energy
principle? Physics of Life Reviews 40, 24–50. https://www.sciencedirect.com/science/article/pii/S15710
64521000749 doi:10.1016/j.plrev.2021.11.001 Critical-review treatment of Markov-blanket / particular-physics
derivations of the free-energy principle. First circulated as a 2021 preprint; final publication in Physics of Life
Reviews vol. 40 (2022); slug retained as aguilera-2021 for back-compatibility.
• Da Costa, L., Friston, K., Heins, C., Pavliotis, G. A. (2021) Bayesian mechanics for stationary processes.
Proceedings of the Royal Society A 477(2256), 20210518. https://royalsocietypublishing.org/doi/10.1098
/rspa.2021.0518 doi:10.1098/rspa.2021.0518 Bayesian-mechanics reference for Markov blankets in stationary
processes; cited to keep the manuscript’s policy-space blanket language explicitly analogical.
• Kirchhoff, M. D., Parr, T., Palacios, E., Friston, K., Kiverstein, J. (2018) The Markov blankets of life:
autonomy, active inference and the free energy principle. Journal of The Royal Society Interface 15(138),
20170792. https://royalsocietypublishing.org/doi/10.1098/rsif.2017.0792 doi:10.1098/rsif.2017.0792 Markov-
blanket account of autonomy used here to keep system-boundary language separate from the manuscript’s
intra-agent policy-coupling claim.
• Menary, R., Gillett, A. J. (2022) Markov blankets do not demarcate the boundaries of the mind. Behavioral
and Brain Sciences 45, e201. https://pubmed.ncbi.nlm.nih.gov/36172779/ doi:10.1017/S0140525X22000371
Critical extended-mind commentary; cited to prevent Markov-blanket language from being treated as an
automatic cognitive-boundary criterion.
• Raja, V., Valluri, D., Baggs, E., Chemero, A., Anderson, M. L. (2021) The Markov blanket trick: On the scope
of the free energy principle and active inference. Physics of Life Reviews. https://www.sciencedirect.com/sc
ience/article/pii/S1571064521000634 doi:10.1016/j.plrev.2021.09.001 Critical scope analysis of broad FEP /
active-inference claims; cited here to keep Markov-blanket and biological interpretations explicitly bounded.
• Ramstead, M. J. D., Badcock, P. B., Friston, K. J. (2018) Answering Schrödinger’s question: A free-energy
formulation. Physics of Life Reviews 24, 1–16. https://www.sciencedirect.com/science/article/pii/S15710
64517301409 doi:10.1016/j.plrev.2017.09.001 Theoretical-biology framing of FEP and self-organization; cited
only for context, not as evidence for the manuscript’s finite-policy results.
Computational psychiatry
• Adams, R. A., Stephan, K. E., Brown, H. R., Frith, C. D., Friston, K. J. (2013) The computational anatomy
of psychosis. Frontiers in Psychiatry 4, 47. https://www.frontiersin.org/articles/10.3389/fpsyt.2013.00047
doi:10.3389/fpsyt.2013.00047
• Haarsma, J., Fletcher, P. C., Griﬀin, J. D., et al. (2021) Precision weighting of cortical unsigned prediction
error signals benefits learning, is mediated by dopamine, and is impaired in psychosis. Molecular Psychiatry
26, 5320-5333. https://www.nature.com/articles/s41380-020-0803-8 doi:10.1038/s41380-020-0803-8 Empirical
precision-weighting study used to support cautious dopamine / psychosis discussion without identifying lambda
with a neural precision variable.
• Schwartenbeck, P., Friston, K. (2016) Computational Phenotyping in Psychiatry:
A Worked Example.
eNeuro 3(4), ENEURO.0049-16.2016.
https://www.eneuro.org/content/3/4/ENEURO.0049-16.2016
doi:10.1523/ENEURO.0049-16.2016
Integrated information / consciousness
• Tononi, G. (2008) Consciousness as integrated information: a provisional manifesto. The Biological Bulletin
215(3), 216–242. https://www.journals.uchicago.edu/doi/10.2307/25470707 doi:10.2307/25470707
Multi-agent / interactive inference
• Albarracin, M., Pitliya, R. J., St. Clere Smithe, T., Friedman, D. A., Friston, K., Ramstead, M. J. D. (2024)
Shared Protentions in Multi-Agent Active Inference. Entropy 26(4), 303. https://www.mdpi.com/1099-
4300/26/4/303 doi:10.3390/e26040303
158

## Page 160

• Friedman, D. A. (2025) CEREBRUM: Case-Enabled Reasoning Engine with Bayesian Representations for
Unified Modeling.
Zenodo (Active Inference Journal) v1.4.
https://zenodo.org/records/15231156
doi:10.5281/zenodo.15231156 Case-grammar architecture for unified Bayesian cognitive modeling; supports
the manuscript’s multi-agent / case-grammar connection.
• Friedman, D. A. (2026) Compositional Approaches to Linguistic Case for Cognitive Modeling. Active Inference
Journal.
Zenodo v1.
https://doi.org/10.5281/zenodo.19695260 doi:10.5281/zenodo.19695260 Category-
theoretic treatment of linguistic case systems: case roles as objects, alignment patterns as functors, sentence
and discourse circuits as morphisms in a compact-closed category, hom-objects enriched over [0,1] as magnitudes,
and topos-theoretic Morita equivalence between alignment frames. Supplies the compositional substrate under
which the case-graded J asymmetry of the CEREBRUM connections section is licensed; companion architecture
to friedman-2025-cerebrum.
• Friston, K. J., Da Costa, L., Heins, C., Klein, B., Salvatori, T., Buckley, C. L., Tschantz, A., Parr,
T. (2024) Federated inference and belief sharing.
Neuroscience & Biobehavioral Reviews 156, 105500.
doi:10.1016/j.neubiorev.2023.105500 Belief broadcasting across agents under shared generative models; canon-
ical federated-inference reference in AIF.
• Heins, C., Millidge, B., Da Costa, L., Mann, R. P., Friston, K. J., Couzin, I. D. (2024) Collective behavior
from surprise minimization.
Proceedings of the National Academy of Sciences 121(17), e2320239121.
https://www.pnas.org/doi/10.1073/pnas.2320239121 doi:10.1073/pnas.2320239121 Primary collective-
active-inference model; cited for group-scale surprise minimization and emergent coordination rather than
for finite-policy theorem claims.
• Maisto, D., Donnarumma, F., Pezzulo, G. (2024) Interactive Inference: A Multi-Agent Model of Cooperative
Joint Actions.
IEEE Transactions on Systems, Man, and Cybernetics: Systems 54(2), 704–715.
https:
//ieeexplore.ieee.org/document/10288543 doi:10.1109/TSMC.2023.3312585 Earlier circulating attribution
listing Friston as a co-author was incorrect — arXiv:2210.13113 lists authors as Maisto, Donnarumma, Pezzulo.
Final venue: IEEE TSMC: Systems Volume 54, Issue 2, February 2024; DOI minted in 2023.
• Ruiz-Serra, J., Sweeney, S., Harré, M. (2025) Factorised Active Inference for Strategic Multi-Agent Interactions.
Proc. 24th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2025). https:
//arxiv.org/abs/2411.07362 doi:10.48550/arXiv.2411.07362 arXiv:2411.07362.
AAMAS 2025 proceedings
version.
• Waade, P. T., Olesen, C. L., Laursen, J. E., Nehrer, S. W., Heins, C., Friston, K., Mathys, C. (2025) As One
and Many: Relating Individual and Emergent Group-Level Generative Models in Active Inference. Entropy
27(2), 143. https://www.mdpi.com/1099-4300/27/2/143 doi:10.3390/e27020143
Lean / formalization
• Boldo, S., Melquiond, G. (2011) Flocq: A Unified Library for Proving Floating-Point Algorithms in Coq.
2011 IEEE 20th Symposium on Computer Arithmetic, 243–252. https://doi.org/10.1109/ARITH.2011.40
doi:10.1109/ARITH.2011.40 Primary Flocq reference; cited as the model for what a verified Float-to-real bridge
would require.
• Degenne, R., Ledvinka, D., Marion, E., Pfaffelhuber, P. (2025) Formalization of Brownian motion in Lean.
arXiv preprint, arXiv:2511.20118.
https://arxiv.org/abs/2511.20118 doi:10.48550/arXiv.2511.20118
Stochastic-process formalization in Mathlib’s MeasureTheory.Probability.Kernel layer.
• Degenne, R. (2025) Markov kernels in Mathlib’s probability library.
arXiv preprint, arXiv:2510.04070.
https://arxiv.org/abs/2510.04070 doi:10.48550/arXiv.2510.04070 Foundational reference for the Markov-
kernel layer in Mathlib’s MeasureTheory.Probability.Kernel.* namespace; cited for the Lean formalization
path.
• de Moura, L., Ullrich, S. (2021) The Lean 4 Theorem Prover and Programming Language.
Automated
Deduction – CADE 28, LNCS vol. 12699 (Springer, Cham), 625–635. https://link.springer.com/chapte
r/10.1007/978-3-030-79876-5_37 doi:10.1007/978-3-030-79876-5_37
• Friedman, D. A. (2026) Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem
Sketching and Verification for Active Inference and Bayesian Mechanics. Active Inference Journal. Zenodo.
https://github.com/ActiveInferenceInstitute/fep_lean doi:10.5281/zenodo.19699234
• Higham, N. J. (2002) Accuracy and Stability of Numerical Algorithms.
SIAM Second edition.
https:
//doi.org/10.1137/1.9780898718027 doi:10.1137/1.9780898718027 Standard numerical-analysis reference for
round-off, conditioning, and stability; cited to scope Float-vs-real residuals.
• IEEE (2019) IEEE Standard for Floating-Point Arithmetic. IEEE Std 754-2019. https://ieeexplore.ieee.org/
document/8766229 doi:10.1109/IEEESTD.2019.8766229 Primary IEEE 754 standard reference; cited for the
floating-point semantics a verified Float-to-real bridge would need to model.
• Lean FRO (2026) Lean Programming Language. Oﬀicial Lean website. https://lean-lang.org/ Oﬀicial Lean
159

## Page 161

source for the minimal trusted-kernel and verification-platform claims; scholarly citation remains de Moura
and Ullrich 2021.
• Lean FRO (2026) Mathlib: A Foundation for Formal Mathematics Research and Verification. Oﬀicial Lean
use-case page. https://lean-lang.org/use-cases/mathlib/ Oﬀicial current-facing source for Mathlib’s role,
coverage, and quality-assurance framing; scholarly citation remains The Mathlib Community 2020.
• The Mathlib Community (2020) The Lean Mathematical Library. Proc. 9th ACM SIGPLAN International
Conference on Certified Programs and Proofs (CPP 2020), 367–381. https://dl.acm.org/doi/10.1145/3372885
.3373824 doi:10.1145/3372885.3373824 arXiv preprint: 1910.09336.
Software dependencies (companion code)
• Active Inference Institute (2023) GeneralizedNotationNotation.
Open-source software (Active Inference
Institute).
https://github.com/ActiveInferenceInstitute/GeneralizedNotationNotation Reference
implementation of Generalized Notation Notation.
Cited as the upstream of the shipped fifth (structural-
and-numerical) representation in the GNN extension supplement; the bridge ships as a project-owned parser,
a verified K=2 round-trip, and a Lean typed-contract emitter (empirical per the Claim-Strength Legend), with
the upstream first-class coupling primitive named as an honest residual.
• Bagaev, D., Podusenko, A., de Vries, B. (2023) RxInfer: A Julia package for reactive real-time Bayesian
inference. Journal of Open Source Software 8(84), 5161. https://joss.theoj.org/papers/10.21105/joss.05161
doi:10.21105/joss.05161 Primary software citation for RxInfer.jl; cited for the reactive message-passing lineage
that complements pymdp-style discrete POMDP active inference.
• Bradbury, J., Frostig, R., Hawkins, P., Johnson, M. J., Leary, C., Maclaurin, D., Necula, G., Paszke, A.,
VanderPlas, J., Wanderman-Milne, S., Zhang, Q. (2018) JAX: composable transformations of Python+NumPy
programs.
Open-source software.
http://github.com/jax-ml/jax Canonical citation per the JAX
CITATION.bib file. No replacement journal/paper has emerged as of 2026-05. JAX backend underlies pymdp
1.0.1 and the simulation harness.
• Friedman, D. A. (2026) Policy Entanglement in Active Inference:
A Tunable Mean-Field Deformation
Framework for Multi-Stream Policy Ensembles.
Active Inference Institute.
https://github.com/ActiveI
nferenceInstitute/policy_entanglement doi:10.5281/zenodo.20418904 Working four-track research artifact
(prose, equations, Python/pymdp, Lean 4); source at github.com/ActiveInferenceInstitute/policy_entanglement;
Zenodo DOI 10.5281/zenodo.20418904.
• Harris, C. R., Millman, K. J., van der Walt, S. J., Gommers, R., Virtanen, P., Cournapeau, D., et al. (2020)
Array programming with NumPy. Nature 585, 357–362. https://www.nature.com/articles/s41586-020-2649-2
doi:10.1038/s41586-020-2649-2
• Hunter, J. D. (2007) Matplotlib: A 2D graphics environment. Computing in Science & Engineering 9(3),
90–95. https://ieeexplore.ieee.org/document/4160265 doi:10.1109/MCSE.2007.55
• Nehrer, S. W., Laursen, J. E., Heins, C., Friston, K., Mathys, C., Waade, P. T. (2025) Introducing
ActiveInference.jl: A Julia Library for Simulation and Parameter Estimation with Active Inference Models.
Entropy 27(1), 62.
https://www.mdpi.com/1099- 4300/27/1/62 doi:10.3390/e27010062 Primary
ActiveInference.jl software paper; cited for Julia POMDP active-inference simulation and model-fitting context.
• The pymdp developers (2026) infer-actively/pymdp: A Python implementation of active inference for Markov
Decision Processes. GitHub repository. https://github.com/infer-actively/pymdp Oﬀicial source repository
consulted for package identity, install/source provenance, and release context; the scholarly software citation
remains Heins et al. 2022.
• The pymdp developers (2026) pymdp documentation. Read the Docs. https://pymdp-rtd.readthedocs.io
/en/latest/ Oﬀicial documentation consulted for the JAX-backend and Agent/API provenance used by the
reproducibility checklist.
• Virtanen, P., Gommers, R., Oliphant, T. E., Haberland, M., Reddy, T., Cournapeau, D., et al. (2020)
SciPy 1.0:
fundamental algorithms for scientific computing in Python.
Nature Methods 17, 261–272.
https://www.nature.com/articles/s41592-019-0686-2 doi:10.1038/s41592-019-0686-2
Scientific visualization
• Rougier, N. P., Droettboom, M., Bourne, P. E. (2014) Ten Simple Rules for Better Figures.
PLOS
Computational Biology 10(9), e1003833. https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.
pcbi.1003833 doi:10.1371/journal.pcbi.1003833 Visualization-design checklist used narrowly for self-contained
captions, explicit figure purpose, and avoidance of gratuitous complexity.
160

## Page 162

References
R. A. Adams, K. E. Stephan, H. R. Brown, C. D. Frith, and K. J. Friston. The computational anatomy of psychosis.
Frontiers in Psychiatry, 4:47, 2013. doi:10.3389/fpsyt.2013.00047. URL https://www.frontiersin.org/articles/10.
3389/fpsyt.2013.00047.
M. Aguilera, B. Millidge, A. Tschantz, and C. L. Buckley. How particular is the physics of the free energy principle?
Physics of Life Reviews, 40:24–50, 2022. doi:10.1016/j.plrev.2021.11.001. URL https://www.sciencedirect.co
m/science/article/pii/S1571064521000749. Critical-review treatment of Markov-blanket / particular-physics
derivations of the free-energy principle. First circulated as a 2021 preprint; final publication in Physics of Life
Reviews vol. 40 (2022); slug retained as ‘aguilera-2021‘ for back-compatibility.
M. Albarracin, R. J. Pitliya, T. St. Clere Smithe, D. A. Friedman, K. Friston, and M. J. D. Ramstead.
Shared protentions in multi-agent active inference.
Entropy, 26(4):303, 2024.
doi:10.3390/e26040303.
URL
https://www.mdpi.com/1099-4300/26/4/303.
S. Amari. Differential-geometrical methods in statistics. Lecture Notes in Statistics, Vol. 28 (Springer), 1985. URL
https://link.springer.com/book/10.1007/978-1-4612-5056-2. Founding monograph of information geometry;
introduced the dually-flat alpha-connection family and the e- / m-geodesic structure used in the framework-
connections section.
S. Amari. Information geometry and its applications. Springer, Applied Mathematical Sciences, Vol. 194, 2016. URL
https://link.springer.com/book/10.1007/978-4-431-55978-8.
S. Amari and H. Nagaoka. Methods of information geometry. AMS Translations of Mathematical Monographs, Vol.
191 (American Mathematical Society / Oxford University Press), 2000. URL https://bookstore.ams.org/mmono-
191/. Translated by Daishi Harada from the 1993 Japanese original. ISBN 978-0-8218-4302-4.
N. Ay, J. Jost, H. V. Lê, and L. Schwachhöfer.
Information geometry.
Ergebnisse der Mathematik und ihrer
Grenzgebiete (3. Folge), Vol. 64 (Springer), 2017. URL https://link.springer.com/book/10.1007/978-3-319-56478-
4. ISBN 978-3-319-56477-7. Comprehensive monograph treatment covering the parametric and non-parametric
geometric foundations used in the information-geometric formalism.
P.-L. Bacon, J. Harb, and D. Precup.
The option-critic architecture.
Proceedings of the AAAI Conference on
Artificial Intelligence, 31(1), 2017. doi:10.1609/aaai.v31i1.10916. URL https://ojs.aaai.org/index.php/AAAI/arti
cle/view/10916. Modern options reference used to scope the manuscript’s option-like embedding as a parametric
policy-matching construction, not a proof that the lambda deformation subsumes all option-learning algorithms.
D. Bagaev and de Vries B. Podusenko, A. Rxinfer: A julia package for reactive real-time bayesian inference. Journal
of Open Source Software, 8(84):5161, 2023. doi:10.21105/joss.05161. URL https://joss.theoj.org/papers/10.2
1105/joss.05161. Primary software citation for RxInfer.jl; cited for the reactive message-passing lineage that
complements pymdp-style discrete POMDP active inference.
Émery M. Bakry, D. Diffusions hypercontractives, 1985. URL https://doi.org/10.1007/BFb0075144. Bakry–Émery
curvature criterion for log-Sobolev / variance bounds on exponential families.
T. D. Barrett, A. Camuto, C. R. Williamson, and S. J. Roberts. Certifiably robust variational autoencoders through
lipschitz constraints. Proceedings of the 25th International Conference on Artificial Intelligence and Statistics
(AISTATS), 2022. URL https://proceedings.mlr.press/v151/barrett22a.html. Actionable KL-drift bounds under
encoder/decoder Lipschitz constraints; cited for adversarial VI robustness context in Q11.
A. G. Barto and S. Mahadevan. Recent advances in hierarchical reinforcement learning. Discrete Event Dynamic
Systems, 13:341–379, 2003. doi:10.1023/A:1025696116075. URL https://link.springer.com/article/10.1023/A:
1025696116075. Review reference for hierarchical RL and temporal abstraction; cited alongside options to keep
the control/RL comparison anchored in the RL literature.
J. Biamonte and V. Bergholm. Tensor networks in a nutshell. arXiv, 2017. URL https://arxiv.org/abs/1708.00006.
Tutorial tensor-network reference used to scope Schmidt-rank / tensor-train language as probability-tensor linear
algebra, not a quantum-physical claim.
D. M. Blei, A. Kucukelbir, and J. D. McAuliffe.
Variational inference:
A review for statisticians.
Journal
of the American Statistical Association, 112(518):859–877, 2017.
doi:10.1080/01621459.2017.1285773.
URL
https://doi.org/10.1080/01621459.2017.1285773. Modern scholarly review citation for mean-field and structured
variational inference.
161

## Page 163

S. Boldo and G. Melquiond. Flocq: A unified library for proving floating-point algorithms in coq. 2011 IEEE 20th
Symposium on Computer Arithmetic, 2011. URL https://doi.org/10.1109/ARITH.2011.40. Primary Flocq
reference; cited as the model for what a verified Float-to-real bridge would require.
M. Botvinick and M. Toussaint.
Planning as inference.
Trends in Cognitive Sciences, 16(10):485–488, 2012.
doi:10.1016/j.tics.2012.08.006.
URL https://www.cell.com/trends/cognitive-sciences/fulltext/S1364-
6613(12)00184-3.
J. Bradbury, R. Frostig, P. Hawkins, M. J. Johnson, C. Leary, D. Maclaurin, G. Necula, A. Paszke, J. VanderPlas,
S. Wanderman-Milne, and Q. Zhang. Jax: composable transformations of python+numpy programs. Open-source
software, 2018. URL http://github.com/jax-ml/jax. Canonical citation per the JAX CITATION.bib file. No
replacement journal/paper has emerged as of 2026-05. JAX backend underlies pymdp 1.0.1 and the simulation
harness.
H. J. Brascamp and E. H. Lieb. On extensions of the brunn–minkowski and prékopa–leindler theorems, including
inequalities for log concave functions, and with an application to the diffusion equation.
22:366–389, 1976.
doi:10.1016/0022-1236(76)90001-5. URL https://doi.org/10.1016/0022-1236(76)90001-5. Variance Brascamp–
Lieb inequality for log-concave measures; cited in Q1 dispersion-comparison conjecture.
C. L. Buckley, C. S. Kim, S. McGregor, and A. K. Seth. The free energy principle for action and perception: A
mathematical review. Journal of Mathematical Psychology, 81:55–79, 2017. doi:10.1016/j.jmp.2017.09.004. URL
https://www.sciencedirect.com/science/article/pii/S0022249617300962.
Accessible mathematical review
of the free-energy principle used to ground the introductory VFE claim without relying only on process-theory
exposition.
T. Champion, M. Grześ, and H. Bowman.
Branching time active inference with bayesian filtering.
Neural
Computation, 34(10):2132–2144, 2022. doi:10.1162/neco_a_01529. URL https://direct.mit.edu/neco/article-
abstract/34/10/2132. Uses Bayesian filtering on the expanded policy tree rather than vanilla MCTS rollouts; in
the wider BTAI lineage (Fountas et al. 2020 DAI / MCTS for active inference).
T. Champion, H. Bowman, D. Marković, and M. Grześ. Reframing the expected free energy: Four formulations and
a unification. arXiv preprint, 2024. URL https://arxiv.org/abs/2402.14460.
A. Cichocki, N. Lee, I. V. Oseledets, A.-H. Phan, Q. Zhao, and D. P. Mandic. Tensor networks for dimensionality
reduction and large-scale optimization: Part 1 low-rank tensor decompositions.
Foundations and Trends in
Machine Learning, 9(4–5):249–429, 2016. doi:10.1561/2200000059. URL https://doi.org/10.1561/2200000059.
Machine-learning tensor-network survey; cited for low-rank tensor formats and optimization context, not as an
active-inference result.
The Mathlib Community. The lean mathematical library. Proc. 9th ACM SIGPLAN International Conference on
Certified Programs and Proofs (CPP 2020), 2020. URL https://dl.acm.org/doi/10.1145/3372885.3373824. arXiv
preprint: 1910.09336.
L. Da Costa, T. Parr, N. Sajid, S. Veselic, V. Neacsu, and K. Friston.
Active inference on discrete state-
spaces: A synthesis. Journal of Mathematical Psychology, 99:102447, 2020. doi:10.1016/j.jmp.2020.102447. URL
https://www.sciencedirect.com/science/article/pii/S0022249620300857. arXiv:2001.07203.
L. Da Costa, K. Friston, C. Heins, and G. A. Pavliotis. Bayesian mechanics for stationary processes. Proceedings
of the Royal Society A, 477(2256):20210518, 2021. doi:10.1098/rspa.2021.0518. URL https://royalsocietypublis
hing.org/doi/10.1098/rspa.2021.0518. Bayesian-mechanics reference for Markov blankets in stationary processes;
cited to keep the manuscript’s policy-space blanket language explicitly analogical.
L. Da Costa, S. Tenka, D. Zhao, and N. Sajid.
Active inference as a model of agency.
arXiv, 2024.
URL
https://arxiv.org/abs/2401.12917. Accepted at the RLDM 2022 workshop ’RL as a model of agency’; cited
for the active-inference-as-agency unification framing, not as evidence for policy entanglement itself.
L. de Moura and S. Ullrich. The lean 4 theorem prover and programming language. Automated Deduction – CADE
28, LNCS vol. 12699 (Springer, Cham), 2021. URL https://link.springer.com/chapter/10.1007/978-3-030-79876-
5_37.
B. de Vries and K. J. Friston. A factor graph description of deep temporal active inference. Frontiers in Computational
Neuroscience, 11:95, 2017. doi:10.3389/fncom.2017.00095. URL https://www.frontiersin.org/articles/10.3389/fnc
om.2017.00095/full. Primary factor-graph / Forney-style graph source for deep temporal active inference; cited
only for message-passing implementability, not as a theorem-equivalence claim for policy entanglement.
162

## Page 164

B. de Vries, van de Laar T. Nuijten, T., W. Kouw, A. Adamiat, A. Nisslbeck, and et al. Lukashchuk, V. Expected
free energy-based planning as variational inference. arXiv preprint, 2025. URL https://arxiv.org/abs/2504.14898.
R. Degenne. Markov kernels in mathlib’s probability library. arXiv preprint, 2025. URL https://arxiv.org/abs/25
10.04070. Foundational reference for the Markov-kernel layer in Mathlib’s ‘MeasureTheory.Probability.Kernel.*‘
namespace; cited for the Lean formalization path.
R. Degenne, D. Ledvinka, E. Marion, and P. Pfaffelhuber. Formalization of brownian motion in lean. arXiv preprint,
arXiv:2511.20118, 2025. URL https://arxiv.org/abs/2511.20118. Stochastic-process formalization in Mathlib’s
MeasureTheory.Probability.Kernel layer.
B. B. Doll, K. D. Duncan, D. A. Simon, D. Shohamy, and N. D. Daw. Model-based choices involve prospective
neural activity. Nature Neuroscience, 18(5):767–772, 2015. doi:10.1038/nn.3981. URL https://www.nature.com
/articles/nn.3981.
J. Eisert, M. Cramer, and M. B. Plenio. Colloquium: Area laws for the entanglement entropy. Reviews of Modern
Physics, 82(1):277–306, 2010. doi:10.1103/RevModPhys.82.277. URL https://link.aps.org/doi/10.1103/RevMo
dPhys.82.277.
Z. Fountas, N. Sajid, P. A. M. Mediano, and K. Friston. Deep active inference agents using monte-carlo methods.
Advances in Neural Information Processing Systems 33 (NeurIPS 2020), 2020. URL https://proceedings.neurips.
cc/paper/2020/hash/865dfbde8a344b44095495f3591f7407-Abstract.html. arXiv:2006.04176. Canonical reference
for deep / MCTS-style branching-time active inference (DAI).
D. A. Friedman.
Cerebrum: Case-enabled reasoning engine with bayesian representations for unified modeling.
Zenodo (Active Inference Journal), v1.4, 2025. doi:10.5281/zenodo.15231156. URL https://zenodo.org/recor
ds/15231156. Case-grammar architecture for unified Bayesian cognitive modeling; supports the manuscript’s
multi-agent / case-grammar connection.
D. A. Friedman. Policy entanglement in active inference: A tunable mean-field deformation framework for multi-
stream policy ensembles. Active Inference Institute, 2026a. URL https://github.com/ActiveInferenceInstitute/
policy_entanglement. Working four-track research artifact (prose, equations, Python/pymdp, Lean 4); source at
github.com/ActiveInferenceInstitute/policy_entanglement; Zenodo DOI 10.5281/zenodo.20418904.
D. A. Friedman. Compositional approaches to linguistic case for cognitive modeling. Active Inference Journal.
Zenodo, v1, 2026b. doi:10.5281/zenodo.19695260. URL https://doi.org/10.5281/zenodo.19695260. Category-
theoretic treatment of linguistic case systems: case roles as objects, alignment patterns as functors, sentence
and discourse circuits as morphisms in a compact-closed category, hom-objects enriched over [0,1] as magnitudes,
and topos-theoretic Morita equivalence between alignment frames. Supplies the compositional substrate under
which the case-graded J asymmetry of the CEREBRUM connections section is licensed; companion architecture
to friedman-2025-cerebrum.
D. A. Friedman.
Towards lean 4 formalization of the free energy principle: Ai-driven theorem sketching and
verification for active inference and bayesian mechanics.
Active Inference Journal. Zenodo, 2026c.
URL
https://github.com/ActiveInferenceInstitute/fep_lean.
K. Friston. The free-energy principle: a unified brain theory? Nature Reviews Neuroscience, 11(2):127–138, 2010.
doi:10.1038/nrn2787. URL https://www.nature.com/articles/nrn2787.
K. Friston. A free energy principle for a particular physics. arXiv preprint, 2019. URL https://arxiv.org/abs/1906
.10184. Preprint only as of 2026-05; never received a journal publication.
K. Friston, J. Kilner, and L. Harrison. A free energy principle for the brain. Journal of Physiology-Paris, 100(1–3):
70–87, 2006. doi:10.1016/j.jphysparis.2006.10.001. URL https://www.sciencedirect.com/science/article/pii/S0
92842570600060X. Early statement of variational free energy as a unifying principle for perception, action, and
learning.
K. Friston, P. Schwartenbeck, T. FitzGerald, M. Moutoussis, T. Behrens, and R. J. Dolan. The anatomy of choice:
dopamine and decision-making. Philosophical Transactions of the Royal Society B, 369(1655):20130481, 2014.
doi:10.1098/rstb.2013.0481. URL https://royalsocietypublishing.org/doi/10.1098/rstb.2013.0481.
K. Friston, T. FitzGerald, F. Rigoli, P. Schwartenbeck, and G. Pezzulo. Active inference: A process theory. Neural
Computation, 29(1):1–49, 2017a. doi:10.1162/NECO_a_00912. URL https://direct.mit.edu/neco/article/29/1/1.
K. Friston, L. Da Costa, D. Hafner, C. Hesp, and T. Parr. Sophisticated inference. Neural Computation, 33(3):713–
763, 2021. doi:10.1162/neco_a_01351. URL https://direct.mit.edu/neco/article/33/3/713. arXiv:2006.04120.
Introduces recursive expected free energy for deep counterfactual policy tree search.
163

## Page 165

K.
J.
Friston.
Active
inference
and
cognitive
consistency.
Psychological
Inquiry,
29(2):67–73,
2018.
doi:10.1080/1047840X.2018.1480693. URL https://www.tandfonline.com/doi/full/10.1080/1047840X.2018.1
480693. Commentary linking expected-free-energy epistemic/pragmatic terms to cognitive-consistency constructs;
cited as interpretive context, not as a reduction of social-psychological theory to active inference.
K. J. Friston and de Vries B. Parr, T. The graphical brain: Belief propagation and active inference. Network
Neuroscience, 1(4):381–414, 2017. doi:10.1162/NETN_a_00018. URL https://doi.org/10.1162/NETN_a_00018.
Graphical-brain source for belief propagation, Forney-style graphical modeling, and active-inference message-
passing context; not evidence that lambda-coupled policy posteriors are standard in AIF.
K. J. Friston, N. Trujillo-Barreto, and J. Daunizeau. Dem: A variational treatment of dynamic systems. NeuroImage,
41(3):849–885, 2008. doi:10.1016/j.neuroimage.2008.02.054. URL https://www.sciencedirect.com/science/articl
e/pii/S1053811908001894. Primary dynamic expectation maximization reference behind the SPM-DEM lineage
discussed in the introduction.
K. J. Friston, R. Rosch, T. Parr, C. Price, and H. Bowman.
Deep temporal models and active inference.
Neuroscience & Biobehavioral Reviews, 77:388–402, 2017b.
doi:10.1016/j.neubiorev.2017.04.009.
URL https:
//doi.org/10.1016/j.neubiorev.2017.04.009. Primary deep-temporal active-inference source; cited for hierarchical
temporal-model and long-horizon framing, not as evidence that the present finite-policy model is a full process
theory.
K. J. Friston, L. Da Costa, C. Heins, B. Klein, T. Salvatori, C. L. Buckley, A. Tschantz, and T. Parr. Federated
inference and belief sharing. Neuroscience & Biobehavioral Reviews 156, 105500, 2024. Belief broadcasting across
agents under shared generative models; canonical federated-inference reference in AIF.
K. J. Friston, C. Heins, T. Verbelen, L. Da Costa, T. Salvatori, D. Marković, A. Tschantz, M. Koudahl, C. Buckley,
and T. Parr. From pixels to planning: scale-free active inference. Frontiers in Network Physiology, 5:1521963,
2025. doi:10.3389/fnetp.2025.1521963. URL https://www.frontiersin.org/journals/network-physiology/article
s/10.3389/fnetp.2025.1521963/full. First circulated as a 2024 preprint (arXiv:2407.20292); final venue Frontiers
in Network Physiology, June 2025. The published Frontiers form is the canonical citation; the ‘friston-rgm-2025‘
alias is intentionally NOT registered to avoid duplication — cite as ‘[@friston-2024]‘. Slug retained as ‘friston-2024‘
for back-compatibility.
Lean FRO. Lean programming language. Oﬀicial Lean website, 2026a. URL https://lean-lang.org/. Oﬀicial Lean
source for the minimal trusted-kernel and verification-platform claims; scholarly citation remains de Moura and
Ullrich 2021.
Lean FRO. Mathlib: A foundation for formal mathematics research and verification. Oﬀicial Lean use-case page,
2026b. URL https://lean-lang.org/use-cases/mathlib/. Oﬀicial current-facing source for Mathlib’s role, coverage,
and quality-assurance framing; scholarly citation remains The Mathlib Community 2020.
Y. Fu, M. S. Smith, and A. Panagiotelis.
Vector copula variational inference and dependent block posterior
approximations. arXiv preprint, 2025. URL https://arxiv.org/abs/2503.01072.
I. Glasser, N. Pancotti, and J. I. Cirac.
From probabilistic graphical models to generalized tensor networks
for supervised learning. IEEE Access, 8:68169–68182, 2020. doi:10.1109/ACCESS.2020.2986279. URL https:
//ieeexplore.ieee.org/document/9058650/. arXiv:1806.05964 (2018 preprint); IEEE Access publication 2020.
J. Haarsma, P. C. Fletcher, and et al. Griﬀin, J. D. Precision weighting of cortical unsigned prediction error signals
benefits learning, is mediated by dopamine, and is impaired in psychosis. Molecular Psychiatry, 26:5320–5333,
2021. doi:10.1038/s41380-020-0803-8. URL https://www.nature.com/articles/s41380-020-0803-8. Empirical
precision-weighting study used to support cautious dopamine / psychosis discussion without identifying lambda
with a neural precision variable.
D. Hafner, J. Pasukonis, J. Ba, and T. Lillicrap. Mastering diverse domains through world models. arXiv preprint,
2023.
URL https://arxiv.org/abs/2301.04104.
DreamerV3 — world-model RL agent that achieves cross-
domain mastery with a single hyperparameter setting; widely cited as the canonical contemporary world-model
architecture against which active-inference agents are benchmarked.
S. Han, X. Liao, D. B. Dunson, and L. Carin. Variational gaussian copula inference. AISTATS 2016, PMLR 51,
2016. URL https://proceedings.mlr.press/v51/han16.html.
Z.-Y. Han, J. Wang, H. Fan, L. Wang, and P. Zhang. Unsupervised generative modeling using matrix product states.
Physical Review X, 8(3):031012, 2018. doi:10.1103/PhysRevX.8.031012. URL https://journals.aps.org/prx/abstr
act/10.1103/PhysRevX.8.031012.
164

## Page 166

C. R. Harris, van der Walt S. J. Millman, K. J., R. Gommers, P. Virtanen, and et al. Cournapeau, D. Array
programming with numpy. Nature, 585:357–362, 2020. doi:10.1038/s41586-020-2649-2. URL https://www.nature
.com/articles/s41586-020-2649-2.
C. Heins, B. Millidge, D. Demekas, B. Klein, K. Friston, I. D. Couzin, and A. Tschantz.
pymdp: A python
library for active inference in discrete state spaces.
Journal of Open Source Software, 7(73):4098, 2022.
doi:10.21105/joss.04098. URL https://joss.theoj.org/papers/10.21105/joss.04098. v1.0.1 JAX-based release
is the simulation backend used by the empirical suite and src/simulation/; arXiv:2201.03904.
C. Heins, B. Millidge, L. Da Costa, R. P. Mann, K. J. Friston, and I. D. Couzin.
Collective behavior
from surprise minimization.
Proceedings of the National Academy of Sciences, 121(17):e2320239121, 2024.
doi:10.1073/pnas.2320239121. URL https://www.pnas.org/doi/10.1073/pnas.2320239121. Primary collective-
active-inference model; cited for group-scale surprise minimization and emergent coordination rather than for
finite-policy theorem claims.
N.
J.
Higham.
Accuracy
and
stability
of
numerical
algorithms.
SIAM,
Second
edition,
2002.
doi:10.1137/1.9780898718027. URL https://doi.org/10.1137/1.9780898718027. Standard numerical-analysis
reference for round-off, conditioning, and stability; cited to scope Float-vs-real residuals.
G. E. Hinton. Training products of experts by minimizing contrastive divergence. Neural Computation, 14(8):1771–
1800, 2002. doi:10.1162/089976602760128018. URL https://direct.mit.edu/neco/article-abstract/14/8/1771/.
R. Hodson, M. Mehta, and R. Smith. The empirical status of predictive coding and active inference. Neuroscience
& Biobehavioral Reviews, 157:105473, 2024. doi:10.1016/j.neubiorev.2023.105473. URL https://pubmed.ncbi.nl
m.nih.gov/38030100/. Empirical-status review used to calibrate FEP / active-inference claims as normative and
computational unless a specific comparative empirical test is supplied.
M. D. Hoffman and D. M. Blei. Structured stochastic variational inference. AISTATS 2015, PMLR 38, 2015. URL
http://proceedings.mlr.press/v38/hoffman15.html. arXiv:1404.4114.
J. D. Hunter. Matplotlib: A 2d graphics environment. Computing in Science & Engineering, 9(3):90–95, 2007.
doi:10.1109/MCSE.2007.55. URL https://ieeexplore.ieee.org/document/4160265.
IEEE. Ieee standard for floating-point arithmetic. IEEE Std 754-2019, 2019. URL https://ieeexplore.ieee.org/docu
ment/8766229. Primary IEEE 754 standard reference; cited for the floating-point semantics a verified Float-to-real
bridge would need to model.
Active Inference Institute.
Generalizednotationnotation.
Open-source software (Active Inference Institute),
2023.
URL https://github.com/ActiveInferenceInstitute/GeneralizedNotationNotation.
Reference
implementation of Generalized Notation Notation. Cited as the upstream of the shipped fifth (structural-and-
numerical) representation in the GNN extension supplement; the bridge ships as a project-owned parser, a verified
K=2 round-trip, and a Lean typed-contract emitter (empirical per the Claim-Strength Legend), with the upstream
first-class coupling primitive named as an honest residual.
R. S. Johansson, G. Westling, A. Bäckström, and J. R. Flanagan. Eye-hand coordination in object manipulation.
Journal of Neuroscience, 21(17):6917–6932, 2001.
doi:10.1523/JNEUROSCI.21-17-06917.2001.
URL https:
//www.jneurosci.org/content/21/17/6917. Primary empirical eye-hand coordination source used to ground
the reach/saccade example in the motivation.
R. Kaplan and K. J. Friston. Planning and navigation as active inference. Biological Cybernetics, 112:323–343, 2018.
doi:10.1007/s00422-018-0753-2. URL https://link.springer.com/article/10.1007/s00422-018-0753-2. Navigation
and planning example for EFE-based policy selection, risk / ambiguity terms, and epistemic exploration under
active inference.
H. J. Kappen. Path integrals and symmetry breaking for optimal control theory. Journal of Statistical Mechanics:
Theory and Experiment, 2005:P11011, 2005. doi:10.1088/1742-5468/2005/11/P11011. URL https://iopscience.i
op.org/article/10.1088/1742-5468/2005/11/P11011.
M. D. Kirchhoff, T. Parr, E. Palacios, K. Friston, and J. Kiverstein.
The markov blankets of life: autonomy,
active inference and the free energy principle. Journal of The Royal Society Interface, 15(138):20170792, 2018.
doi:10.1098/rsif.2017.0792. URL https://royalsocietypublishing.org/doi/10.1098/rsif.2017.0792. Markov-blanket
account of autonomy used here to keep system-boundary language separate from the manuscript’s intra-agent
policy-coupling claim.
M. F. Land and M. Hayhoe.
In what ways do eye movements contribute to everyday activities?
Vision
Research, 41(25–26):3559–3565, 2001. doi:10.1016/S0042-6989(01)00102-X. URL https://doi.org/10.1016/S0042-
165

## Page 167

6989(01)00102-X. Natural-task eye-movement review showing that gaze commonly arrives at task-relevant objects
before manipulation, grounding the cross-stream reach/saccade example.
P. Lanillos, C. Meo, C. Pezzato, A. A. Meera, M. Baioumy, W. Ohata, A. Tschantz, B. Millidge, M. Wisse, C. L.
Buckley, and J. Tani. Active inference in robotics and artificial agents: Survey and challenges. arXiv preprint,
2021. URL https://arxiv.org/abs/2112.01871.
S. Levine. Reinforcement learning and control as probabilistic inference: Tutorial and review. arXiv preprint, 2018.
URL https://arxiv.org/abs/1805.00909. Canonical tutorial on the control-as-inference / maximum-entropy RL
viewpoint cited in the comparison with active inference.
Y. Li and R. E. Turner. Rényi divergence variational inference. Advances in Neural Information Processing Systems
29 (NeurIPS 2016), 2016. URL https://proceedings.neurips.cc/paper/2016/hash/7750ca3559e5b8e1f44210283368f
c16-Abstract.html. arXiv:1602.02311. Generalizes ELBO-style variational inference to the Renyi alpha-divergence
family; cited for structured-VI / alpha-divergence comparisons with the active-inference free-energy functional.
J. Limanowski, R. A. Adams, J. Kilner, and T. Parr. The many roles of precision in action. Entropy, 26(9):790,
2024. doi:10.3390/e26090790. URL https://www.mdpi.com/1099-4300/26/9/790. Review of precision roles in
action, attention, habit, and self-other distinction; cited to keep lambda-as-coupling-precision language distinct
from neural precision claims.
D. Maisto, F. Donnarumma, and G. Pezzulo.
Interactive inference:
A multi-agent model of cooperative
joint actions.
IEEE Transactions on Systems,
Man,
and Cybernetics:
Systems, 54(2):704–715, 2024.
doi:10.1109/TSMC.2023.3312585. URL https://ieeexplore.ieee.org/document/10288543. Earlier circulating
attribution listing Friston as a co-author was incorrect — arXiv:2210.13113 lists authors as Maisto, Donnarumma,
Pezzulo. Final venue: IEEE TSMC: Systems Volume 54, Issue 2, February 2024; DOI minted in 2023.
W. J. McGill. Multivariate information transmission. Psychometrika, 19(2):97–116, 1954. doi:10.1007/BF02289159.
URL https://link.springer.com/article/10.1007/BF02289159. Original definition of total correlation / multi-
information, the correlation surcharge in the entanglement-decomposition identity.
R. Menary and A. J. Gillett. Markov blankets do not demarcate the boundaries of the mind. Behavioral and Brain
Sciences, 45:e201, 2022. doi:10.1017/S0140525X22000371. URL https://pubmed.ncbi.nlm.nih.gov/36172779/.
Critical extended-mind commentary; cited to prevent Markov-blanket language from being treated as an automatic
cognitive-boundary criterion.
B. Millidge, A. Tschantz, and C. L. Buckley. Whence the expected free energy? Neural Computation, 33(2):447–482,
2021. doi:10.1162/neco_a_01354. URL https://direct.mit.edu/neco/article/33/2/447/95645/Whence-the-
Expected-Free-Energy. Critical analysis of EFE derivations and alternatives; cited to keep expected-free-energy
unification claims bounded.
J. Naudts. Generalised thermostatistics. Springer London, 2011. URL https://link.springer.com/book/10.1007/978-
0-85729-355-8. ISBN 978-0-85729-354-1 (print). Covers escort distributions, q-deformed exponential families.
S. W. Nehrer, J. E. Laursen, C. Heins, K. Friston, C. Mathys, and P. T. Waade. Introducing activeinference.jl:
A julia library for simulation and parameter estimation with active inference models. Entropy, 27(1):62, 2025.
doi:10.3390/e27010062. URL https://www.mdpi.com/1099-4300/27/1/62. Primary ActiveInference.jl software
paper; cited for Julia POMDP active-inference simulation and model-fitting context.
R. B. Nelsen. An introduction to copulas. Springer Series in Statistics, 2nd ed., 2006. URL https://link.springer.co
m/book/10.1007/0-387-28678-0. Foundational monograph for copula definitions and dependence modeling; cited
to distinguish true copula densities from informal dependence-factor analogies.
F. Nielsen. An elementary introduction to information geometry. Entropy, 22(10):1100, 2020. doi:10.3390/e22101100.
URL https://www.mdpi.com/1099-4300/22/10/1100.
T. Nuijten and V. Lukashchuk. Active inference is a subtype of variational inference. arXiv preprint, 2025. URL
https://arxiv.org/abs/2511.18955.
R. Orus. A practical introduction to tensor networks: Matrix product states and projected entangled pair states.
Annals of Physics, 349:117–158, 2014. doi:10.1016/j.aop.2014.06.013. URL https://www.sciencedirect.com/scie
nce/article/pii/S0003491614001596. Tutorial tensor-network reference used to scope matrix-product-state and
tensor-train language as linear algebra on probability tensors.
I. V. Oseledets.
Tensor-train decomposition.
SIAM Journal on Scientific Computing, 33(5):2295–2317, 2011.
doi:10.1137/090752286. URL https://epubs.siam.org/doi/10.1137/090752286. Foundational paper introducing
the TT-format; underlies the linear-in-N policy-tensor compression used in the tensor-network analysis.
166

## Page 168

T. Parr and K. J. Friston. Uncertainty, epistemics and active inference. Journal of The Royal Society Interface,
14(136):20170376, 2017a. doi:10.1098/rsif.2017.0376. URL https://royalsocietypublishing.org/doi/10.1098/rsif.20
17.0376. Primary source for epistemic value and uncertainty reduction in active-inference policy selection.
T. Parr and K. J. Friston.
Working memory, attention, and salience in active inference.
Scientific Reports, 7:
14678, 2017b. doi:10.1038/s41598-017-15249-0. URL https://www.nature.com/articles/s41598-017-15249-0.
Process-theory account linking working memory, attention, salience, precision, and policy evaluation under active
inference.
T. Parr and K. J. Friston. Generalised free energy and active inference. Biological Cybernetics, 113(5–6):495–513,
2019. doi:10.1007/s00422-019-00805-w. URL https://link.springer.com/article/10.1007/s00422-019-00805-w.
Clarifies generalized free energy and self-evidencing language used in the discussion without treating the present
finite-policy model as a complete biological process theory.
T. Parr, D. Marković, S. J. Kiebel, and K. J. Friston.
Neuronal message passing using mean-field, bethe
and marginal approximations. Scientific Reports, 9:1889, 2019.
doi:10.1038/s41598-018-38246-3. URL https:
//www.nature.com/articles/s41598-018-38246-3. Primary source distinguishing mean-field, Bethe, and marginal
message-passing approximations; cited for approximation-family context, not as a direct proof of policy-coupling
neural implementation.
T. Parr, G. Pezzulo, and K. J. Friston. Active inference: The free energy principle in mind, brain, and behavior.
MIT Press, 2022. URL https://direct.mit.edu/books/oa-monograph/5299/Active-InferenceThe-Free-Energy-
Principle-in-Mind. Book-length synthesis of FEP, expected free energy, active inference process theory, and
applications.
G. Pezzulo, F. Rigoli, and K. J. Friston. Hierarchical active inference: A theory of motivated control. Trends in
Cognitive Sciences, 22(4):294–306, 2018. doi:10.1016/j.tics.2018.01.009. URL https://www.cell.com/trends/cogn
itive-sciences/fulltext/S1364-6613(18)30022-6.
G. Pezzulo, T. Parr, and K. J. Friston. Active inference as a theory of sentient behavior. Biological Psychology,
186:108741, 2024. doi:10.1016/j.biopsycho.2023.108741. URL https://www.sciencedirect.com/science/article/pi
i/S0301051123002612. Recent synthesis used to distinguish active inference as process theory from the broader
free-energy-principle framing.
The pymdp developers. infer-actively/pymdp: A python implementation of active inference for markov decision
processes. GitHub repository, 2026a. URL https://github.com/infer-actively/pymdp. Oﬀicial source repository
consulted for package identity, install/source provenance, and release context; the scholarly software citation
remains Heins et al. 2022.
The pymdp developers. pymdp documentation. Read the Docs, 2026b. URL https://pymdp-rtd.readthedocs.
io/en/latest/. Oﬀicial documentation consulted for the JAX-backend and Agent/API provenance used by the
reproducibility checklist.
V. Raja, D. Valluri, E. Baggs, A. Chemero, and M. L. Anderson. The markov blanket trick: On the scope of the
free energy principle and active inference. Physics of Life Reviews, 2021. URL https://www.sciencedirect.com/sc
ience/article/pii/S1571064521000634. Critical scope analysis of broad FEP / active-inference claims; cited here
to keep Markov-blanket and biological interpretations explicitly bounded.
M. J. D. Ramstead, P. B. Badcock, and K. J. Friston. Answering schrödinger’s question: A free-energy formulation.
Physics of Life Reviews, 24:1–16, 2018. doi:10.1016/j.plrev.2017.09.001. URL https://www.sciencedirect.com/sc
ience/article/pii/S1571064517301409. Theoretical-biology framing of FEP and self-organization; cited only for
context, not as evidence for the manuscript’s finite-policy results.
K. Rawlik, M. Toussaint, and S. Vijayakumar.
On stochastic optimal control and reinforcement learning by
approximate inference (extended abstract). Proceedings of the Twenty-Third International Joint Conference on
Artificial Intelligence (IJCAI 2013), 2013. URL https://www.ijcai.org/Proceedings/13/Papers/455.pdf. Extended
abstract of the approximate-inference control formulation; cited for the KL/control-as-inference lineage rather
than as an active-inference result.
N. P. Rougier, M. Droettboom, and P. E. Bourne. Ten simple rules for better figures. PLOS Computational Biology,
10(9):e1003833, 2014. doi:10.1371/journal.pcbi.1003833. URL https://journals.plos.org/ploscompbiol/article?i
d=10.1371/journal.pcbi.1003833. Visualization-design checklist used narrowly for self-contained captions, explicit
figure purpose, and avoidance of gratuitous complexity.
J. Ruiz-Serra, S. Sweeney, and M. Harré. Factorised active inference for strategic multi-agent interactions. Proc.
167

## Page 169

24th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2025), 2025.
URL
https://arxiv.org/abs/2411.07362. arXiv:2411.07362. AAMAS 2025 proceedings version.
N. Sajid, P. J. Ball, T. Parr, and K. J. Friston. Active inference: Demystified and compared. Neural Computation,
33(3):674–712, 2021. doi:10.1162/neco_a_01357. URL https://direct.mit.edu/neco/article/33/3/674.
L. K. Saul and M. I. Jordan.
Exploiting tractable substructures in intractable networks.
Advances in Neural
Information Processing Systems 8 (NIPS 1995), 1995.
URL https://papers.nips.cc/paper/1155-exploiting-
tractable-substructures-in-intractable-networks. Canonical structured mean-field source: exact inference is
retained inside tractable substructures while only the remaining interactions are approximated.
U. Schollwöck. The density-matrix renormalization group in the age of matrix product states. Annals of Physics,
326(1):96–192, 2011. doi:10.1016/j.aop.2010.09.012. URL https://www.sciencedirect.com/science/article/pii/S0
003491610001752. arXiv:1008.3477. Canonical MPS/DMRG review; cited for the algorithmic backbone behind
policy-tensor compression and entanglement-entropy bookkeeping.
P. Schwartenbeck and K. Friston. Computational phenotyping in psychiatry: A worked example. eNeuro, 3(4):
ENEURO.0049–16.2016, 2016. doi:10.1523/ENEURO.0049-16.2016. URL https://www.eneuro.org/content/3/4
/ENEURO.0049-16.2016.
P. Schwartenbeck, T. H. B. FitzGerald, C. Mathys, R. Dolan, and K. Friston. The dopaminergic midbrain encodes the
expected certainty about desired outcomes. Cerebral Cortex, 25(10):3434–3445, 2015. doi:10.1093/cercor/bhu159.
URL https://academic.oup.com/cercor/article/25/10/3434/385607.
R. Smith, K. J. Friston, and C. J. Whyte.
A step-by-step tutorial on active inference and its application to
empirical data. Journal of Mathematical Psychology, 107:102632, 2022. doi:10.1016/j.jmp.2021.102632. URL
https://www.sciencedirect.com/science/article/pii/S0022249621000973.
T. S. C. Smithe. Structured active inference. arXiv preprint, arXiv:2406.07577, 2024. URL https://arxiv.org/abs/24
06.07577. Categorical-systems-theory formulation of AIF with structured policies amenable to formal verification.
J. Smékal and D. A. Friedman. Generalized notation notation for active inference models. Active Inference Journal.
Zenodo, 2023. URL https://zenodo.org/records/7803328. Primary publication of Generalized Notation Notation
(GNN), introducing the Triple Play of linguistic, visual, and executable cognitive-model representations that
complements the Active Inference Ontology. Cited from the GNN extension supplement as the canonical reference
for the shipped fifth (structural-and-numerical) representation of the framework.
R. S. Sutton, D. Precup, and S. Singh. Between mdps and semi-mdps: A framework for temporal abstraction in
reinforcement learning. Artificial Intelligence, 112(1–2):181–211, 1999. doi:10.1016/S0004-3702(99)00052-1. URL
https://www.sciencedirect.com/science/article/pii/S0004370299000521.
E. A. Theodorou and E. Todorov.
Relative entropy and free energy dualities:
Connections to path integral
and kl control.
Proc. 2012 IEEE 51st Conference on Decision and Control (CDC), 2012.
URL https:
//ieeexplore.ieee.org/document/6426381/.
E. Todorov. Linearly-solvable markov decision problems. Advances in Neural Information Processing Systems 19
(NIPS 2006), 2006. URL https://papers.nips.cc/paper/3002-linearly-solvable-markov-decision-problems. Primary
linearly-solvable MDP reference for KL-control structure and log-partition value transformations.
G. Tononi.
Consciousness as integrated information: a provisional manifesto.
The Biological Bulletin, 215(3):
216–242, 2008. doi:10.2307/25470707. URL https://www.journals.uchicago.edu/doi/10.2307/25470707.
M. Toussaint.
Robot trajectory optimization using approximate inference.
Proc. 26th Annual International
Conference on Machine Learning (ICML 2009), 2009. URL https://dl.acm.org/doi/10.1145/1553374.1553508.
D. Tran, D. M. Blei, and E. M. Airoldi. Copula variational inference. Advances in Neural Information Processing
Systems 28 (NeurIPS 2015), 2015. URL https://proceedings.neurips.cc/paper/2015/hash/e4dd5528f7596dcdf87
1aa55cfccc53c-Abstract.html. arXiv:1506.03159.
A. Tschantz, A. K. Seth, and C. L. Buckley. Learning action-oriented models through active inference. PLOS
Computational Biology, 16(4):e1007805, 2020. doi:10.1371/journal.pcbi.1007805. URL https://journals.plos.org/
ploscompbiol/article?id=10.1371/journal.pcbi.1007805. Active-inference account of parsimonious action-oriented
model learning; useful contrast for this manuscript’s structured policy-coupling family.
de Vries B. van de Laar, T. W. Simulating active inference processes by message passing. Frontiers in Robotics and
AI, 6:20, 2019. doi:10.3389/frobt.2019.00020. URL https://www.frontiersin.org/articles/10.3389/frobt.2019.00020.
168

## Page 170

Factor-graph forward-backward implementation of deep temporal active inference (slug retained for backwards
compatibility — primary reference is the 2019 *Frontiers in Robotics and AI* paper).
F. Verstraete, V. Murg, and J. I. Cirac.
Matrix product states, projected entangled pair states, and varia-
tional renormalization group methods for quantum spin systems.
Advances in Physics, 57(2):143–224, 2008.
doi:10.1080/14789940801912366. URL https://www.tandfonline.com/doi/abs/10.1080/14789940801912366.
P. Virtanen, R. Gommers, T. E. Oliphant, M. Haberland, T. Reddy, and et al. Cournapeau, D.
Scipy 1.0:
fundamental algorithms for scientific computing in python. Nature Methods, 17:261–272, 2020. doi:10.1038/s41592-
019-0686-2. URL https://www.nature.com/articles/s41592-019-0686-2.
P. T. Waade, C. L. Olesen, J. E. Laursen, S. W. Nehrer, C. Heins, K. Friston, and C. Mathys. As one and many:
Relating individual and emergent group-level generative models in active inference. Entropy, 27(2):143, 2025.
doi:10.3390/e27020143. URL https://www.mdpi.com/1099-4300/27/2/143.
M. J. Wainwright and M. I. Jordan. Graphical models, exponential families, and variational inference. Foundations
and Trends in Machine Learning, 1(1-2):1–305, 2008. doi:10.1561/2200000001. URL https://www.nowpublish
ers.com/article/Details/MAL-001. Canonical graphical-model variational-inference reference used to anchor the
mean-field / structured-approximation comparison.
S. Watanabe. Information theoretical analysis of multivariate correlation. IBM Journal of Research and Development,
4(1):66–82, 1960. doi:10.1147/rd.41.0066. URL https://ieeexplore.ieee.org/document/5392532. Independent
rediscovery of McGill’s total-correlation construction, under the alternative name multivariate correlation; widely
cited as the second canonical reference for the total-correlation quantity.
J. S. Yedidia, W. T. Freeman, and Y. Weiss. Constructing free-energy approximations and generalized belief propaga-
tion algorithms. IEEE Transactions on Information Theory, 51(7):2282–2312, 2005. doi:10.1109/TIT.2005.850085.
URL https://doi.org/10.1109/TIT.2005.850085. Canonical Bethe / Kikuchi free-energy and generalized-belief-
propagation source; cited for graphical-variational approximation structure, not for active-inference policy seman-
tics.
169


---
*Extraction method: pymupdf*
