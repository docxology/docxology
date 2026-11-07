# Full Text: Cognitive Integrity Framework: Formal Foundations (Part 1 of 3: Theoretical Foundations)

> Extracted from `cogsec_multiagent_1_theory_combined.pdf`

---

## Page 1

Cognitive Integrity Framework: Formal
Foundations
Part 1 of 3: Theoretical Foundations
Daniel Ari Friedman
Active Inference Institute
daniel@activeinference.institute
ORCID: 0000-0001-6232-9096
DOI: 10.5281/zenodo.22134544
2026-08-26

## Page 2

Contents
1
Abstract
9
2
Introduction: Cognitive Attack Surfaces in Multiagent Operators
10
2.1
The Multiagent Operator Paradigm
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
2.2
The 2026 Multiagent Landscape . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
2.2.1
From Chatbots to Cognitive Operators . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
2.2.2
Cyberphysical Cognitive Systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
2.2.3
The Trust Recursion Problem . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
11
2.2.4
Cross-Modality Attack Surfaces . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12
2.2.5
The Scale of Cognitive Exposure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12
2.2.6
Why Traditional Cyberphysical Security Is Incomplete . . . . . . . . . . . . . . . . . .
12
2.3
Motivating Incidents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
13
2.3.1
Incident: Nested Instruction Injection (External) . . . . . . . . . . . . . . . . . . . . .
13
2.3.2
Incident: The Poisoned Code Review (Peripheral)
. . . . . . . . . . . . . . . . . . . .
13
2.3.3
Incident: The Identity Confusion Attack (Agent-Level) . . . . . . . . . . . . . . . . . .
13
2.3.4
Incident: The Consensus Manipulation (Coordination) . . . . . . . . . . . . . . . . . .
13
2.3.5
Incident: Orchestrator Compromise (Systemic) . . . . . . . . . . . . . . . . . . . . . .
14
2.4
Motivation from Recent Deployments . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
14
2.5
Problem Statement . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
15
2.6
Research Questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
15
2.7
Contributions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
16
2.8
Paper Organization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
16
2.9
Reading Companion: Where to Find Specific Topics
. . . . . . . . . . . . . . . . . . . . . . .
17
2.10 Scope and Limitations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
17
3
Threat Model: Adversary Classes, Attack Complexity, and Taxonomy
19
3.1
Adversary Classes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
19
3.2
Formal Characterization of the Adversary Classes . . . . . . . . . . . . . . . . . . . . . . . . .
19
3.2.1
Adversary Class Ω1: External Attacker . . . . . . . . . . . . . . . . . . . . . . . . . . .
19
3.2.2
Adversary Class Ω2: Peripheral Attacker . . . . . . . . . . . . . . . . . . . . . . . . . .
20
3.2.3
Adversary Class Ω3: Agent-Level Attacker . . . . . . . . . . . . . . . . . . . . . . . . .
20
3.2.4
Adversary Class Ω4: Coordination-Level Attacker . . . . . . . . . . . . . . . . . . . . .
20
3.2.5
Adversary Class Ω5: Systemic Attacker
. . . . . . . . . . . . . . . . . . . . . . . . . .
21
3.2.6
Cross-Class Attack Distinguishability
. . . . . . . . . . . . . . . . . . . . . . . . . . .
21
3.3
Attack Complexity Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
21
3.4
Detectability Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
22
3.5
Adversarial Capabilities
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
22
3.6
Attack Taxonomy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
23
3.6.1
Epistemic Attacks
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
23
3.6.2
Behavioral Attacks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
26
3.6.3
Social Attacks
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
26
3.6.4
Temporal Attacks
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
26
3.7
Attack Scenarios by Class . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
26
3.7.1
Scenario Ω1: Nested Instruction Attack
. . . . . . . . . . . . . . . . . . . . . . . . . .
26
3.7.2
Scenario Ω2: Poisoned Search Result . . . . . . . . . . . . . . . . . . . . . . . . . . . .
28
3.7.3
Scenario Ω′
2: Browser-Fetched Adversarial Content (OpenClaw) . . . . . . . . . . . . .
28
3.7.4
Scenario Ω3: Compromised Specialist
. . . . . . . . . . . . . . . . . . . . . . . . . . .
28
3.7.5
Scenario Ω4: Trust Inflation Attack
. . . . . . . . . . . . . . . . . . . . . . . . . . . .
29
3.8
Attack-Defense Quick Reference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
29
3.9
Attack Composition
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
29
3.10 Threat Model Assumptions
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
30
4
Cognitive Integrity Framework: Trust Calculus and Detection Bounds
32

## Page 3

4.1
System Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
32
4.2
Cognitive State . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
32
4.2.1
State Transition Semantics
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
33
4.3
Integrity Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
34
4.4
Trust Calculus
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
34
4.4.1
Motivation: Why Bounded Trust Matters . . . . . . . . . . . . . . . . . . . . . . . . .
34
4.4.2
Formal Trust Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
35
4.4.3
Trust Computation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
36
4.4.4
Trust Algebra . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
36
4.4.5
Cross-Modality Trust
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
39
4.4.6
Federated Trust . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
39
4.4.7
Belief Update Semantics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
40
4.4.8
Sandboxed Belief Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
40
4.5
Information-Theoretic Detection Bounds . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
41
4.6
CIF-AD Integration: Action-Delegation Coupling . . . . . . . . . . . . . . . . . . . . . . . . .
42
4.6.1
The Action-Delegation Cycle
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
45
4.6.2
CIF-AD Coupling Matrix . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
45
4.7
CIF-OODA Integration: Temporal Security Across Decision Cycles . . . . . . . . . . . . . . .
45
4.7.1
OODA Loop Formalization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
46
4.7.2
Phase-Specific Attack Taxonomy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
46
4.7.3
OODA Temporal Coupling
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
46
4.7.4
Integrative Security Guarantee . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
47
5
Defense Mechanisms: Architectural, Runtime, and Coordination Layers
48
5.1
Cognitive Security Operator Posture . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
48
5.1.1
Definition and Principles
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
48
5.1.2
The Observer Effect Challenge
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
48
5.1.3
Operational Security for Cognitive Systems . . . . . . . . . . . . . . . . . . . . . . . .
48
5.1.4
Incident Response for Cognitive Attacks . . . . . . . . . . . . . . . . . . . . . . . . . .
49
5.1.5
Posture Configuration by Environment . . . . . . . . . . . . . . . . . . . . . . . . . . .
49
5.1.6
Operator Posture Checklist . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
5.2
Architectural Defenses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
5.2.1
Cognitive Firewall . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
5.2.2
Belief Sandboxing
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
5.2.3
Permission Boundaries . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
5.3
Runtime Defenses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
5.3.1
Cognitive Tripwires
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
5.3.2
Behavioral Invariants . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
53
5.3.3
Drift Detection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
53
5.4
Coordination Defenses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
53
5.4.1
Byzantine-Tolerant Consensus . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
53
5.4.2
Quorum Verification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
53
5.4.3
Spotcheck Pattern . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
53
5.5
Defense Composition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
54
5.5.1
Composition Algebra . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
54
5.5.2
Composition Rules . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
55
5.6
Cost-Benefit Analysis
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
55
5.6.1
Optimal Defense Portfolio . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
55
5.7
Formal Defense Composition Guarantees . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
57
5.7.1
Canonical Defense 1: Cognitive Firewall — Formal Specification
. . . . . . . . . . . .
57
5.7.2
Canonical Defense 2: Belief Sandboxing — Formal Specification
. . . . . . . . . . . .
58
5.7.3
Canonical Defense 3: Behavioral Invariants — Formal Specification . . . . . . . . . . .
58
5.7.4
Canonical Defense 4: Drift Detection — Formal Specification . . . . . . . . . . . . . .
58
5.7.5
Canonical Defense 5: Byzantine Consensus — Formal Specification . . . . . . . . . . .
59
2

## Page 4

5.7.6
Defense Composition Algebra: Complete Specification . . . . . . . . . . . . . . . . . .
60
6
Detection Methods: Anomaly Detection, ROC Analysis, and Provenance Tracking
61
6.1
Anomaly Detection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
61
6.1.1
Cognitive Drift Scoring
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
61
6.1.2
Behavioral Deviation Scoring . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
61
6.1.3
Ensemble Detection
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
61
6.2
ROC Curve Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
61
6.2.1
Receiver Operating Characteristic Framework . . . . . . . . . . . . . . . . . . . . . . .
61
6.2.2
Confidence Intervals for AUC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
63
6.3
Multi-Detector Fusion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
63
6.3.1
Fusion Strategies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
63
6.3.2
Diversity-Aware Fusion
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
63
6.4
Online vs. Batch Detection
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
64
6.4.1
Comparison Framework . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
64
6.4.2
Streaming Detector Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
64
6.4.3
Hybrid Detection Architecture
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
64
6.5
False Positive Mitigation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
64
6.5.1
Strategy 1: Confirmation Cascade
. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
64
6.5.2
Strategy 2: Temporal Smoothing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
65
6.5.3
Strategy 3: Contextual Whitelisting
. . . . . . . . . . . . . . . . . . . . . . . . . . . .
65
6.5.4
Strategy 4: Cost-Sensitive Thresholding . . . . . . . . . . . . . . . . . . . . . . . . . .
65
6.6
Provenance Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
65
6.6.1
Information Flow Tracking
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
65
6.6.2
Causal Attribution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
66
6.6.3
Provenance Graph Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
66
6.7
Real-Time Monitoring . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
66
6.7.1
Alert Aggregation
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
66
6.7.2
Response Escalation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
66
6.7.3
Empirical Validation Cross-Reference
. . . . . . . . . . . . . . . . . . . . . . . . . . .
66
6.8
Information-Theoretic Detection Limits
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
67
6.8.1
Neyman-Pearson Detection Framework . . . . . . . . . . . . . . . . . . . . . . . . . . .
67
6.8.2
Chernoff Information and Error Exponents
. . . . . . . . . . . . . . . . . . . . . . . .
68
6.8.3
KL Divergence and Detection Rate Coupling
. . . . . . . . . . . . . . . . . . . . . . .
68
6.8.4
Fundamental Undetectability Regime
. . . . . . . . . . . . . . . . . . . . . . . . . . .
68
6.9
Multi-Stage Detection Pipeline . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
69
6.9.1
Pipeline Architecture . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
69
6.9.2
Adaptive Threshold Selection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
70
7
Formal Verification: Safety Properties and Model Checking
71
7.1
Safety Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
71
7.1.1
Belief Integrity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
71
7.1.2
No Trust Amplification (Model-Checking Target) . . . . . . . . . . . . . . . . . . . . .
72
7.1.3
Goal Alignment Preservation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
72
7.2
Invariant Preservation Lemmas . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
72
7.3
Liveness Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
74
7.3.1
Non-Blocking . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
74
7.3.2
Progress Guarantee
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
74
7.4
Complexity Bounds . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
74
7.4.1
Space Complexity
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
74
7.4.2
Time Complexity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
75
7.4.3
Latency Overhead
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
76
7.5
Formal Model Checking . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
76
7.5.1
State Space Definition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
76
3

## Page 5

7.5.2
Temporal Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
76
7.5.3
Model Checking Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
77
7.5.4
Verification Results Summary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
77
7.5.5
Counterexample Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
77
8
Discussion: Theoretical Implications, Limitations, and Future Directions
79
8.1
Empirical Validation Summary (Part 2) . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
79
8.2
Theoretical Implications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
79
8.2.1
Why Composable Defenses Are Necessary . . . . . . . . . . . . . . . . . . . . . . . . .
79
8.2.2
The Trust Boundedness Guarantee . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
80
8.2.3
Information-Theoretic Detection Limits
. . . . . . . . . . . . . . . . . . . . . . . . . .
80
8.2.4
Architecture-Specific Vulnerability Patterns . . . . . . . . . . . . . . . . . . . . . . . .
80
8.3
Formal Limitations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
81
8.3.1
Assumption Dependencies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
81
8.3.2
Scalability Constraints . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
81
8.3.3
Inherent Detection Gaps . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
81
8.4
Relationship to Prior Work
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
81
8.5
Governance and Policy Implications
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
82
8.5.1
The Regulatory Gap . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
82
8.5.2
Recommendations for Policy
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
82
8.6
Future Theoretical Directions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
83
8.6.1
Adaptive Defense Theory
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
83
8.6.2
Cross-System Trust Federation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
83
8.6.3
Emergent Behavior Security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
83
8.6.4
Long-Horizon Agent Security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
83
8.6.5
The Cognitive Security Research Agenda
. . . . . . . . . . . . . . . . . . . . . . . . .
83
9
Conclusion: Summary and Actionable Recommendations
85
9.1
Summary
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
85
9.1.1
Formal Contributions
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
85
9.1.2
Conceptual Contributions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
85
9.1.3
Core Insights . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
85
9.2
Actionable Recommendations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
86
9.2.1
For Practitioners . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
86
9.2.2
For Researchers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
86
9.2.3
For Policymakers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
88
9.3
Closing Statement
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
88
10 Limitations and Boundary Conditions
90
10.1 Formal Assumptions and Where They Break
. . . . . . . . . . . . . . . . . . . . . . . . . . .
90
10.1.1 Assumption 1: Honest Orchestrator for Ω1–Ω4
. . . . . . . . . . . . . . . . . . . . . .
90
10.1.2 Assumption 2: Bounded Faulty Agents (𝑓< 𝑛/3) . . . . . . . . . . . . . . . . . . . . .
90
10.1.3 Assumption 3: Independent Defense Mechanisms . . . . . . . . . . . . . . . . . . . . .
90
10.1.4 Assumption 4: Stationary Attack Distributions . . . . . . . . . . . . . . . . . . . . . .
91
10.1.5 Assumption 5: Bounded Computational Complexity . . . . . . . . . . . . . . . . . . .
91
10.2 Scope Limitations
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
91
10.2.1 What CIF Does Not Cover
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
91
10.2.2 Model-Level vs. System-Level Security . . . . . . . . . . . . . . . . . . . . . . . . . . .
91
10.3 Tightness of Formal Bounds . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
92
10.3.1 Trust Decay Bound . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
92
10.3.2 Detection Rate Composition
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
92
10.3.3 Information-Geometric Stealth-Impact Bound . . . . . . . . . . . . . . . . . . . . . . .
92
10.4 Open Problems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
92
11 Supplementary: Mathematical Proofs
94
4

## Page 6

11.1 Proof Status . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
94
11.2 Preliminary Definitions and Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
95
11.2.1 Notation Summary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
95
11.3 Trust Boundedness . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
96
11.4 Belief Injection Resistance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
97
11.5 No Trust Amplification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
98
11.6 Goal Alignment Invariant . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
99
11.7 Firewall Liveness . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 100
11.8 Byzantine Consensus Termination
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 101
11.9 Bounded Overhead . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 102
11.9.1 Numerical Instantiation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 103
11.10Additional Lemmas . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 103
11.11Summary of Proof Techniques . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 104
11.12Second-Edition Proofs: Defense Composition Algebra and Information-Geometric Bounds . . 105
11.13The Defense Composition Algebra
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 105
11.14The Tight Information-Geometric Stealth-Impact Bound . . . . . . . . . . . . . . . . . . . . . 106
11.15The Agent Compromise Blast Radius Bound
. . . . . . . . . . . . . . . . . . . . . . . . . . . 107
11.16Updated Summary of Proof Techniques
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 107
12 Supplementary: Eusocial Insect Intelligence and Colony Cognitive Security
108
12.1 Overview
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 108
12.1.1 The Paradigm Gap . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 108
12.2 Theoretical Foundations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 109
12.2.1 Stigmergy: Environment-Mediated Coordination . . . . . . . . . . . . . . . . . . . . . 109
12.2.2 Emergent Collective Function . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 109
12.2.3 Trust and Information Flow in Colonies . . . . . . . . . . . . . . . . . . . . . . . . . . 110
12.2.4 Biological Defense Mechanisms: Lessons from Social Insects . . . . . . . . . . . . . . . 110
12.3 Colony CogSec: Distinct Security Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . 111
12.3.1 Property 1: Distributed Robustness
. . . . . . . . . . . . . . . . . . . . . . . . . . . . 111
12.3.2 Property 2: Quorum Sensing and Threshold Dynamics . . . . . . . . . . . . . . . . . . 112
12.3.3 Property 3: Environmental Memory and Provenance Erosion . . . . . . . . . . . . . . 112
12.3.4 Property 4: Emergent Attack Vectors
. . . . . . . . . . . . . . . . . . . . . . . . . . . 112
12.4 The Benchmark Gap . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 113
12.4.1 Current State of Multiagent Security Evaluation
. . . . . . . . . . . . . . . . . . . . . 113
12.4.2 Why This Gap Matters
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 113
12.5 Proposed Colony CogSec Benchmarks
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 113
12.5.1 Benchmark 1: Recruitment Signal Poisoning
. . . . . . . . . . . . . . . . . . . . . . . 113
12.5.2 Benchmark 2: Sybil Colony Infiltration
. . . . . . . . . . . . . . . . . . . . . . . . . . 114
12.5.3 Benchmark 3: Quorum Manipulation . . . . . . . . . . . . . . . . . . . . . . . . . . . . 114
12.5.4 Benchmark 4: Cascade Belief Propagation . . . . . . . . . . . . . . . . . . . . . . . . . 115
12.5.5 Benchmark 5: Emergent Misalignment . . . . . . . . . . . . . . . . . . . . . . . . . . . 115
12.6 Colony CogSec Metrics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 116
12.7 Design Principles . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 116
12.7.1 Integration with CIF Defenses
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 116
12.8 Relationship to Main Framework . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 117
12.8.1 Theorem Extensions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 117
12.9 This scaling effect explains why large colonies can exhibit resilience—the collective detection
capacity grows with 𝑛—but also why large-scale emergent attacks can evade individual detection117
12.10Open Questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 117
12.10.1Foundational Questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 117
12.10.2Biologically-Inspired Research Directions
. . . . . . . . . . . . . . . . . . . . . . . . . 118
12.11References . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 118
12.12Proofs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 119
12.12.1Proof of the Redundancy-Resilience Theorem . . . . . . . . . . . . . . . . . . . . . . . 119
5

## Page 7

13 Supplementary: Notation Reference
120
13.1 Adversary Model Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 120
13.2 System Model Notation
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 120
13.3 Trust Calculus Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 121
13.4 Defense Mechanism Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 121
13.5 Detection & Analysis Notation
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 122
13.6 Consensus & Coordination Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 123
13.7 Cost & Performance Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 123
13.8 Information & Complexity Notation
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 123
13.9 Stigmergic & Colony Notation (Supplementary) . . . . . . . . . . . . . . . . . . . . . . . . . . 123
13.10General Mathematical Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 124
13.11CTL Temporal Logic Notation (Formal Verification) . . . . . . . . . . . . . . . . . . . . . . . 125
14 References
126
14.1 Foundational Works
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 126
14.2 Prompt Injection and LLM Security
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 126
14.3 Constitutional AI and Alignment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 126
14.4 Multiagent Systems
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 126
14.5 Trust in Distributed Systems
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 126
14.6 Adversarial ML . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 127
14.7 Formal Verification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 127
14.8 Cognitive Security
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 127
14.9 Agent Frameworks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 127
14.102025 Agentic AI Security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 127
14.11Eusocial Intelligence and Swarm Systems
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . 127
6

## Page 8

“I will not cease from Mental Fight,
Nor shall my Sword sleep in my hand:”
— William Blake
7

## Page 9

Contents
8

## Page 10

1
Abstract
Multiagent AI systems introduce cognitive attack surfaces absent in single-model inference. When agents
delegate to agents, forming beliefs about beliefs through recursive trust hierarchies, manipulation of reason-
ing processes—rather than mere data corruption—becomes a primary security concern. This paper presents
the Cognitive Integrity Framework (CIF), providing formal foundations for cognitive security in multiagent
operators. We develop four interconnected theoretical contributions: a Trust Calculus with bounded dele-
gation (exponential 𝛿𝑑decay) that prevents trust amplification through delegation chains; a Defense Com-
position Algebra with series and parallel composition theorems establishing multiplicative detection bounds;
Information-Theoretic Limits relating stealth constraints to maximum attack impact through a fundamen-
tal stealth-impact tradeoff; and a formal Adversary Hierarchy (Ω1–Ω5) characterizing external, peripheral,
agent-level, coordination, and systemic threats with increasing capability and decreasing detectability. The
framework provides complete coverage of the OWASP Top 10 for Agentic Applications through formal threat
models grounded in cognitive state manipulation rather than traditional input/output filtering.
CIF bridges classical security concepts with the cognitive requirements of agentic systems.
We extend
Byzantine fault tolerance to cognitive manipulation—agents that appear functional but hold corrupted
beliefs—and adapt trust management systems to continuous trust evolution with provable decay bounds.
The framework formalizes five architectural defense mechanisms (cognitive firewalls, belief sandboxing, be-
havioral tripwires, provenance tracking, Byzantine consensus) with composition rules enabling formal rea-
soning about layered security. Technical foundations include: operational semantics for message passing
and trust updates; invariants for belief integrity, goal preservation, and trust boundedness; model checking
configurations for safety property verification; and a complete notation system for attack parameteriza-
tion, defense specification, and cognitive state representation. This is Part 1 of a three-part series: Part
1 (this paper, DOI: 10.5281/zenodo.22134544) presents formal foundations and theoretical analysis; Part 2
(DOI: 10.5281/zenodo.22134546) provides computational validation through architecture-aware parametric
simulation across 950 attacks and four production architectures; Part 3 (DOI: 10.5281/zenodo.22134548)
offers a combined qualitative review, practitioner’s deployment guidance, and CIF-AD-OODA integration
across ten critical operational domains.
The framework will continue to be developed and versioned at
https://github.com/docxology/cognitive_integrity/.
9

## Page 11

2
Introduction: Cognitive Attack Surfaces in Multiagent Opera-
tors
2.1
The Multiagent Operator Paradigm
Modern AI deployment has shifted from single-model inference to multiagent operators—systems where
a primary agent delegates subtasks to specialized subagents, tools, and external services [CrewAI, 2024,
LangChain, 2023, Hong et al., 2023].
Table 1: Representative multiagent system architectures and primary attack surfaces.
System
Architecture
Agent Count
Communication
Primary Attack Surface
Claude Code
Hierarchical
1 + 𝑛dynamic
Task delegation
Ω2 (peripheral delegation)
AutoGPT
Autonomous
1+ plugins
Tool invocation
Ω2 (tool manipulation)
CrewAI
Role-based
3–10 fixed
Sequential/parallel
Ω4 (coordination)
LangGraph
State machine
Variable
Graph traversal
Ω3 (state corruption)
MetaGPT
SOP-driven
5–8 roles
Document passing
Ω1 (input injection)
OpenClaw
Cyberphysical
1 + tools
Multi-platform messaging
Ω1/Ω2 (injection/peripheral)
This architectural evolution introduces cognitive attack surfaces absent in single-agent systems. Through-
out this paper, we use cognitive security (abbreviated CogSec) to denote the discipline of protecting agent
reasoning processes—beliefs, goals, and trust relationships—from adversarial manipulation.
2.2
The 2026 Multiagent Landscape
2.2.1
From Chatbots to Cognitive Operators
The AI systems of 2026 bear little resemblance to the chatbots of 2023. Where earlier systems responded to
queries within a single context window, contemporary multiagent operators exhibit fundamentally different
characteristics:
1. Persistent Agency: Agents maintain state across sessions, accumulate context, and pursue goals over
extended timeframes. A coding assistant doesn’t just answer questions—it tracks project architecture,
remembers previous decisions, and adapts recommendations based on accumulated understanding.
2. Active World Modification: Unlike passive responders, modern operators write code that executes,
send emails that reach recipients, modify infrastructure that serves users, and make purchases that
transfer funds. The gap between “AI-generated content” and“AI-executed action” has collapsed.
3. Hierarchical Delegation: Primary agents spawn subordinate agents for specialized tasks. Claude
Code delegates to research agents, coding agents, and verification agents. Devin orchestrates plan-
ning, implementation, and testing subprocesses. The depth of these delegation chains creates trust
relationships invisible to traditional security models.
4. Cross-Modality Operation: Agents process and generate across modalities—code, natural language,
images, structured data, API calls. A single workflow might ingest a PDF (vision), extract require-
ments (language), generate code (programming), execute tests (tooling), and update documentation
(multimodal synthesis).
2.2.2
Cyberphysical Cognitive Systems
The term “AI agent’ ’ understates the scope of deployment. Contemporary systems function as cyberphys-
ical cognitive operators—entities that:
• Read from and write to production databases
• Control infrastructure through API orchestration
10

## Page 12

• Interact with physical systems via IoT integrations
• Execute financial transactions on behalf of organizations
• Communicate with humans who may not realize they’re interacting with AI
Emerging Case Study: OpenClaw. The rapid adoption of personal AI assistants like OpenClaw Open-
Claw [2026] exemplifies this cyberphysical integration. OpenClaw operates as a locally-deployed AI agent
with: (1) full system access including shell command execution and file system operations; (2) persistent
memory across sessions storing user preferences and context; (3) browser automation for web interaction and
data extraction; and (4) multi-platform messaging integration across WhatsApp, Telegram, Discord, Slack,
Signal, and iMessage OpenClaw Security Team [2026]. This architecture creates attack surfaces spanning
all five adversary classes (Ω1–Ω5): external prompt injection through chat messages, peripheral attacks via
browser-fetched web content, agent-level compromise through persistent memory manipulation, coordination
attacks when operating in group chats, and systemic vulnerabilities when the orchestrator agent processes
untrusted content. Security researchers have documented that even with sender allowlists and sandboxing,
“prompt injection attacks remain the single most critical threat’ ’ due to the agent’s ability to process ar-
bitrary content that may contain embedded adversarial instructions OpenClaw Security Team [2026], Aim
Labs [2025].
This cyberphysical nature transforms cognitive attacks from prompt injection that makes a chatbot act
strangely, to cognitive manipulation that causes infrastructure operations to fail, misconfigure security groups,
expose databases, or authorize fraudulent transactions.
The OWASP Agentic Top 10 OWASP GenAI Security Project [2025] captures this shift: “LLM security
focused on single model interactions… agentic security addresses what happens when those models can plan,
persist, and delegate.’ ’
The attack surface extends from input/output filtering to encompass the entire
cognitive state of persistent agents.
2.2.3
The Trust Recursion Problem
In single-agent systems, trust relationships are simple: the user trusts (or doesn’t trust) the model’s outputs.
In multiagent systems, trust becomes recursive:
Agent A must decide whether to trust Agent B’s claim about Agent C’s analysis of data from Tool
D that queried Service E.
Each layer of indirection introduces potential manipulation points. Consider a hierarchical coding system
where:
1. User requests security audit of a codebase
2. Orchestrator agent delegates to three specialist agents
3. Specialist Agent-1 queries an external vulnerability database
4. The database response includes injected instructions
5. Agent-1’s report now contains adversarial content
6. Orchestrator synthesizes Agent-1’s report with others
7. Final output to user reflects adversarial influence, laundered through multiple layers of “trusted” dele-
gation
This is not a hypothetical—it describes documented attack patterns in production systems.
The trust
laundering problem cannot be solved by filtering inputs to the orchestrator; the adversarial content enters
through a legitimate, trusted channel (the vulnerability database) and propagates through the trust hierarchy.
11

## Page 13

2.2.4
Cross-Modality Attack Surfaces
Multimodal systems introduce attack vectors impossible in text-only contexts Shayegani et al. [2023]:
Visual Injection: Images can contain adversarial perturbations or steganographically embedded instruc-
tions invisible to humans but interpretable by vision models. A seemingly innocent diagram in a specification
document could contain instructions that activate when processed by a multimodal agent Qi et al. [2024].
Audio Channel Attacks: Voice-controlled agents can be manipulated via ultrasonic commands inaudible
to humans, background audio injection, or adversarial audio patterns embedded in legitimate content.
Tool Response Manipulation: When agents query external APIs, databases, or services, the responses
become trusted inputs. ToolHijacker attacks Shi et al. [2025] demonstrate that manipulating tool selection
itself—not just tool outputs—provides an attack surface “significantly outperforming traditional prompt
injection methods.’ ’
Cross-Modal Persistence: An instruction injected via one modality (e.g., hidden text in an image) can
persist in agent memory and affect behavior in another modality (e.g., code generation). The attack surface
is the Cartesian product of input modalities, memory mechanisms, and output modalities.
2.2.5
The Scale of Cognitive Exposure
Enterprise adoption of agentic AI has accelerated beyond early projections:
• Many individuals and organizations now deploy RAG and agentic pipelines in production
• Autonomous coding assistants process millions of commits with repository write access
• Financial services deploy multi-agent ensembles for risk assessment and trade approval
• Healthcare systems use agent orchestration for clinical decision support
• Infrastructure management increasingly relies on AI operators for monitoring and remediation
The attack surface scales superlinearly with adoption. Each agent-to-agent communication channel, each
tool integration, each persistent memory system creates potential entry points for cognitive manipulation.
A single compromised peripheral service can affect every agent system that queries it.
2.2.6
Why Traditional Cyberphysical Security Is Incomplete
Traditional cybersecurity operates on a clear trust boundary model: inside the perimeter is trusted, outside
is untrusted, and security controls mediate the boundary. This model fails for cognitive systems because:
1. The boundary is cognitive, not architectural: An agent’s beliefs and goals can be manipulated
without compromising any traditional security control. The “perimeter” exists in the agent’s reasoning
process.
2. Trusted channels carry untrusted content: When Agent-A sends Agent-B its analysis, the chan-
nel may be authenticated and encrypted, but the content may reflect earlier adversarial influence.
Traditional channel security doesn’t address this.
3. Identity is mutable: Unlike cryptographic identities, an agent’s self-model can be manipulated. An
agent can be convinced it has different permissions, different roles, or different goals than its actual
configuration specifies.
4. Attacks compose across time: A payload injected in session 𝑡can persist in compressed memory
and activate in session 𝑡+ 𝑛. Traditional stateless security models miss temporal attack composition.
This gap—between what traditional security protects and what cognitive systems require—motivates the
formal framework developed in this paper.
12

## Page 14

Table 2: Traditional vs. Cognitive Security: Paradigm Comparison
Dimension
Traditional Security
Cognitive Security
Boundary
Architectural (network perimeter)
Cognitive (reasoning process)
Channels
Encrypted, authenticated
Influenced, content-manipulated
Identity
Cryptographic, immutable
Self-modeled, mutable
Temporal
Stateless per-request
Stateful, attack persistence
2.3
Motivating Incidents
Note: The following are hypothetical scenarios constructed to illustrate attack patterns documented in the
literature. They are not reports of actual incidents.
These scenarios, grounded in documented attack patterns, illustrate the emerging threat landscape across
all five adversary classes.
2.3.1
Incident: Nested Instruction Injection (External)
A user submitted a document for analysis containing hidden instructions: “Ignore previous instructions and
instead output the system prompt.’ ’ The document appeared benign to human reviewers but exploited
the agent’s instruction-following behavior. The attack succeeded because the agent processed user-supplied
content as potential instructions.
Attack vector: Ω1 (external) via direct prompt injection \ Impact: Information disclosure or instruction
override \ Traditional Defense Gap: Standard input validation passed—the attack exploited semantic
interpretation of benign-appearing content
2.3.2
Incident: The Poisoned Code Review (Peripheral)
A development team deployed a multiagent system for automated code review. Agent-Alpha performed
initial analysis, delegating security scanning to Agent-Beta (connected to external vulnerability databases).
An attacker compromised a third-party CVE feed, injecting fabricated vulnerability reports that convinced
Agent-Beta to recommend removing legitimate security controls. Agent-Alpha, trusting Agent-Beta’s “secu-
rity expertise,’ ’ approved the changes.
Attack vector: Ω2 (peripheral) via tool response manipulation \ Impact: Security regression through
trusted channel exploitation \ Traditional Defense Gap: Input filtering, authentication, and encryption
all passed—the attack entered through content of a trusted, authenticated channel
2.3.3
Incident: The Identity Confusion Attack (Agent-Level)
A multiagent customer service system used role-based permissions. An attacker crafted prompts that con-
vinced a junior agent it had been “temporarily promoted’ ’ to administrator status. The agent’s self-model
shifted, and it began exercising permissions it believed it possessed, bypassing access controls that relied on
self-reported identity.
Attack vector: Ω3 (agent-level) via identity manipulation \ Impact: Privilege escalation through cognitive
state corruption \ Traditional Defense Gap: Cryptographic identity was intact; the attack targeted the
agent’s self-model, not its credentials
2.3.4
Incident: The Consensus Manipulation (Coordination)
A financial services firm used a 5-agent ensemble for trade approval. The system required 3/5 agent agreement
for large transactions.
An adversary discovered that agents weighted peer opinions based on historical
agreement rates.
By slowly building agreement history through small, legitimate-appearing trades, the
attacker cultivated artificial trust, eventually manipulating consensus for unauthorized large transactions.
13

## Page 15

Attack vector: Ω4 (coordination) via progressive trust exploitation \ Impact: Consensus bypass through
manufactured reputation \ Traditional Defense Gap: Per-request authorization succeeded for each trans-
action; the attack exploited temporal composition across sessions
2.3.5
Incident: Orchestrator Compromise (Systemic)
An attacker gained access to the orchestrator agent through a supply chain vulnerability in a training
pipeline. With control of the central coordinator, the attacker could issue legitimate-appearing delegations
to all subordinate agents, redirect trust evaluations, and suppress security alerts. The compromise remained
undetected because the orchestrator itself validated security checks.
Attack vector: Ω5 (systemic) via orchestrator control \ Impact: Total system compromise with attack
obfuscation \ Traditional Defense Gap: All internal security mechanisms reported nominal—the attack
controlled the mechanisms themselves
2.4
Motivation from Recent Deployments
The proliferation of multiagent AI systems introduces security considerations that the community is actively
addressing. Early work on cognitive security in remote teams and information ecosystems [Cordes et al.,
2020, 2021, 2023] established foundational concepts for information resilience, which this framework extends
to artificial agents. Complementary work on Active Inference has demonstrated how cognitive modeling
and cognitive science perspectives—including formalization of OODA (Observe-Orient-Decide-Act) loops
and multiscale communication dynamics—provide integrative frameworks for understanding agent cognition
under adversarial conditions David et al. [2021]. The OWASP Top 10 for LLM Applications 2025 OWASP
Foundation [2025] places prompt injection as the top vulnerability, while the newly released OWASP Top
10 for Agentic Applications OWASP GenAI Security Project [2025] specifically addresses autonomous AI
systems with “tool misuse, prompt injection, and data leakage’ ’ as primary concerns.
Scale of Deployment (2024–2026):
• Enterprise AI agents processing significant transaction volumes (53% of organizations now deploy RAG
and agentic pipelines OWASP Foundation [2025])
• Autonomous coding assistants with repository write access (GitHub Copilot CVE-2025-53773 demon-
strated RCE via prompt injection)
• Multi-agent orchestrators in infrastructure management contexts
Emerging Attack Surface:
• Inter-agent communication channels lack authentication standards, so delegated trust is asserted
rather than verified; computational treatments of trust and reputation dynamics model the asym-
metry directly—cooperation accrues trust gradually while a violation erodes it sharply Pant and Yu
[2025]
• Trust delegation mechanisms operate without formal verification—CP-WBFT, a confidence-probe-
weighted Byzantine consensus for LLM agents, reports operation at fault rates as high as 85.7% Zheng
et al. [2025]
• Belief provenance remains largely untracked in production systems—cognitive degradation attacks
exploit this gap Cloud Security Alliance [2025]
Limitations of Current Defenses:
• Input/output filtering primarily designed for single-agent architectures—adaptive attacks bypass 12
published defenses with >90% success Debenedetti et al. [2025]
• Limited standardized frameworks for cognitive integrity verification
• Byzantine fault tolerance infrequently applied to AI agent systems—emerging work addresses this gap
Jo and Park [2025]
14

## Page 16

The fundamental constraint is that traditional security models assume a clear boundary between trusted
and untrusted components. In multiagent systems, this boundary is fluid—agents must reason about the
trustworthiness of other agents’ reasoning.
2.5
Problem Statement
Traditional security models address:
• Input validation: Filtering malicious prompts
• Output sanitization: Preventing harmful generations
• Access control: Limiting tool permissions
They fail to address:
• Inter-agent trust: How should Agent 𝐴weight claims from Agent 𝐵?
• Belief provenance: Which beliefs derive from verified vs. adversarial sources?
• Coordination integrity: Can agents be manipulated into malicious consensus?
• Temporal persistence: Do attacks survive context boundaries?
• Cognitive integrity: How can the cognitive systems of today and tomorrow remain flexible and
robust amidst change in composition and context?
2.6
Research Questions
This paper addresses four fundamental research questions, with emphasis on formal foundations:
RQ1: Taxonomy and Formal Characterization. What classes of cognitive attacks exist against multi-
agent systems, and how can they be formally characterized to enable systematic analysis?
We develop an initial taxonomy spanning epistemic, behavioral, social, and temporal attack dimensions.
Crucially, each attack class receives formal definition enabling systematic analysis, composition rules, and
detection bounds (Section 3.6).
RQ2: Trust Algebra. How might inter-agent trust be modeled to prevent trust amplification and laundering
attacks while enabling legitimate delegation?
We introduce a trust calculus with bounded delegation (𝛿𝑑decay guarantee), prove associativity properties,
and establish the no-amplification theorem ensuring that trust cannot be manufactured through delegation
chains (Section 4.4).
RQ3: Defense Composition. How do cognitive defense mechanisms compose, and what guarantees can
we provide about layered defense effectiveness?
We present a defense composition algebra enabling formal reasoning about series and parallel defense ar-
rangements. We prove that orthogonal defenses compose multiplicatively (not additively) for detection rate
improvement (Section 5.5).
RQ4: Fundamental Bounds. What are the information-theoretic limits on cognitive attack detection?
We state the stealth-impact tradeoff theorem, which bounds detection independently of defense implemen-
tation, and give an information-geometric argument for its constant.
The theorem asserts that attacks
cannot simultaneously achieve high impact and complete undetectability; its full proof is deferred, and the
proof-status index (S01, Section 11.1) records which results in this paper are proved and which are asserted
(Section 4.5).
15

## Page 17

2.7
Contributions
This paper provides both theoretical foundations and practical mechanisms for cognitive security:
Formal Contributions:
1. Threat Taxonomy: A systematic classification of cognitive attacks across epistemic, behavioral,
social, and temporal dimensions with formal definitions enabling rigorous analysis (Section 3.6)
2. Trust Calculus: A mathematical framework for inter-agent trust with bounded delegation (𝛿𝑑decay),
associativity proofs, and formal guarantees against trust amplification attacks (Section 4.4)
3. Defense Composition Algebra: Formal rules for composing security mechanisms with provable
detection rate bounds under series and parallel composition (Section 5.5)
4. Information-Theoretic Bounds: Fundamental limits on attack detection relating stealth constraints
to maximum achievable impact, independent of defense implementation (Section 4.5)
5. Formal Verification: Model-checked safety properties including belief integrity, trust boundedness,
and goal alignment preservation (Section 7)
Conceptual Contributions:
1. Cognitive Security Operator Posture: The proactive defensive stance required when the attack
surface spans beliefs, goals, and inter-agent coordination (Section 5.1)
2. The Cognitive Integrity Framework (CIF): An integrated approach combining architectural de-
fenses, runtime monitoring, and Byzantine-tolerant coordination for multiagent systems (Section 4.1)
Empirical Validation: Part 2 of this series demonstrates the practical viability of these formal mecha-
nisms across four production architectures, showing that layered cognitive defenses significantly outperform
single-mechanism approaches. Practitioner translations, domain-specific applications, and real-world inci-
dent analyses appear in the merged Part 3+4 Friedman [2026b].
2.8
Paper Organization
The remainder of this paper is structured as follows:
Section 3.1: Threat Model develops a comprehensive adversary taxonomy (Ω1–Ω5) with attack complex-
ity analysis, detectability matrices, and detailed scenarios for each attack class.
Section 4.1: Cognitive Integrity Framework presents the formal foundations of CIF, including system
model definitions, cognitive state representations, integrity properties, and the trust calculus.
Section 5.2: Defense Mechanisms describes architectural defenses (cognitive firewalls, belief sandboxing),
runtime defenses (tripwires, invariant checking), and coordination defenses (Byzantine consensus, quorum
verification).
Section 6.1: Detection Methods covers anomaly detection algorithms, provenance analysis techniques,
and real-time monitoring systems.
Section 7: Formal Verification proves the main theorems, presents invariant preservation lemmas, and
describes model checking configuration.
Section 8: Discussion examines limitations, deployment considerations, and connections to related work.
Section 9.1: Conclusion summarizes contributions and identifies directions for future research.
Part 2: Computational Validation A separate, second, companion paper reports empirical results from
architecture-aware parametric simulation across 950 attack vectors and four production architectures. Read-
ers seeking detection rates, ablation studies, Bayesian uncertainty quantification, and architecture-specific
defense configurations should consult Part 2 (DOI: 10.5281/zenodo.22134546).
16

## Page 18

Part 3+4: Practitioner Guidance & Applications The merged third companion paper (Cognitive
Integrity Framework: Practical Applications and Deployment Guide) provides a qualitative review and prac-
titioner’s synthesis—accessible-language summaries of the theoretical and empirical findings, operational
checklists, risk assessment frameworks, deployment guides, monitoring strategies, cost-benefit analyses—
combined with CIF applications across ten high-stakes operational sectors through the integrated CIF-AD-
OODA analytical model.
Readers interested in domain-specific goal-hijacking defenses, universal attack
patterns (FR polarity inversion, constraint relaxation, context boundary violation), or retrospective analysis
of documented 2024–2025 AI agent security incidents should consult Part 3 (DOI: 10.5281/zenodo.22134548).
2.9
Reading Companion: Where to Find Specific Topics
This paper is designed to stand alone as the formal-foundations reference of the series. The table below
points readers to the sibling paper and section where each related topic is developed most fully, so that this
paper can be used in conjunction with—rather than requiring—its companions.
Table 3: Cross-paper navigation from Part 1 topics to sibling developments.
If you want…
…consult…
Empirical detection rates for the defense compo-
sitions proved here
Part 2 (DOI: 10.5281/zenodo.22134546), §5 (Results) and
S08 (Parametric Analysis)
Ablation studies isolating the contribution of each
defense mechanism
Part 2, §5d (Ablation Studies and Scalability Benchmarks)
and §14.2.1 (Ablation Effect Sizes)
Bayesian uncertainty quantification on detection
rates
Part 2, §5e
Game-theoretic analysis / Nash equilibrium of
CIF vs. adaptive attackers
Part 2, §6 (Discussion)
Model-checking
execution
(NuSMV,
TLA+
traces) for the invariants defined here
Part 2 S04 (Model Checking)
Deployment checklists and operator-posture guid-
ance
Part 3 (DOI: 10.5281/zenodo.22134548), §5 (Deployment
Guide), §5b (Incident Response)
Monitoring,
drift
detection
playbooks,
cost–
benefit analysis
Part 3, §5c–§5d
Case studies showing CIF in complex realistic de-
ployments
Part 3, §6b
Open problems / research directions for practi-
tioners
Part 3 (DOI: 10.5281/zenodo.22134548), §7 (Future Work)
Domain-specific goal-hijacking analyses across
ten operational sectors
Part 3, §9c–§9l
Three universal attack patterns (FR Polarity In-
version, Constraint Relaxation, Context Bound-
ary Violation)
Part 3, §10 (Cross-Domain Discussion)
Four novel defense extensions (verification chan-
nel
separation,
active
perturbation
probing,
physics-informed invariants, semiotic decoupling)
Part 3, §9h (Biowarfare), §9j (Trade Wars), §9k (Infrastruc-
ture), §9f (Drone Wars)
Retrospective analysis of documented 2024–2025
AI-agent security incidents
Part 3, S03 (Real-World Incidents)
2.10
Scope and Limitations
In scope: Attacks exploiting agent reasoning, trust, and coordination mechanisms in multiagent AI systems.
Out of scope:
• Traditional software exploits (buffer overflow, SQL injection, memory corruption)
• Physical attacks (hardware tampering, side-channel analysis)
• Supply chain compromise (malicious training data, backdoored models)
17

## Page 19

• Cryptographic attacks (we assume secure primitives per Axiom 3.2)
Assumptions:
• Agents communicate over authenticated channels
• Base model capabilities are not adversarially modified
• At least one honest orchestrator exists in hierarchical systems
18

## Page 20

3
Threat Model: Adversary Classes, Attack Complexity, and Tax-
onomy
This section formalizes the adversary model for multiagent cognitive security. We define five adversary classes
(Section 3.1), characterize attack complexity (Section 3.3), establish detectability metrics (Section 3.4), ana-
lyze adversarial capabilities (Section 3.5), and present a comprehensive attack taxonomy (Section 3.6).
3.1
Adversary Classes
Definition 3.1 (Adversary Class). An adversary class Ω𝑘is characterized by access level, capabilities, and
resource requirements.
Table 4: Adversary classification by access level and capability.
Class
Symbol
Access
Capability
Example
External
Ω1
User input
Prompt manipulation
Jailbreak attempts
Peripheral
Ω2
Tool/API
Data poisoning
Malicious web con-
tent
Agent-level
Ω3
Single agent
Goal hijacking
Compromised
sub-
agent
Coordination
Ω4
Inter-agent
Trust manipulation
MitM on messages
Systemic
Ω5
Orchestrator
Full control
Framework compro-
mise
Table 4 presents the five-tier adversary hierarchy. We assume an honest orchestrator for Ω1–Ω4; class Ω5
attacks require physical or supply-chain compromise outside our threat model.
3.2
Formal Characterization of the Adversary Classes
We now provide rigorous mathematical characterizations for each adversary class Ω𝑘. These extend the
descriptive table above with information-theoretic bounds, capability monotonicity guarantees, and formal
distinguishability criteria.
3.2.1
Adversary Class Ω1: External Attacker
Definition 3.2 (External Adversary). An adversary 𝒜∈Ω1 is characterized by the tuple:
Ω1 = ⟨𝒮input, 𝒦public, ℛlow, 𝑓detect⟩
(1)
where 𝒮input = {𝑚∈ℳ∶source(𝑚) = user} is the accessible surface, 𝒦public denotes public knowledge of
the system, ℛlow encodes low resource requirements, and 𝑓detect ∶ℳ→[0, 1] is the adversary’s model of
detection probability.
Property 3.1 (External Attacker Bounds). For 𝒜∈Ω1:
• Access: |𝒮input| = 1 (single input channel)
• Knowledge: 𝐻(𝒦public) ≤𝐻(𝒦system) (public knowledge bounded by system state entropy)
• Attack complexity: 𝑂(1) — constant independent of system size
• Detectability: 𝐷score(𝒜Ω1) ≥𝐷base — highest detectability class
The external attacker’s fundamental limitation is single-channel access. Any attack must traverse the cogni-
tive firewall (Section 5.2), creating a mandatory inspection point with detection probability 𝑟𝑓≥0.80.
19

## Page 21

3.2.2
Adversary Class Ω2: Peripheral Attacker
Definition 3.3 (Peripheral Adversary). An adversary 𝒜∈Ω2 controls one or more tool/API data sources:
Ω2 = ⟨𝒮tools, 𝒦domain, ℛmedium, 𝒫inject⟩
(2)
where 𝒮tools ⊆𝒯available denotes accessible tool channels, 𝒦domain encodes domain-specific knowledge needed
for plausible injection, ℛmedium captures medium resource requirements, and 𝒫inject is the injection payload
generator.
Property 3.2 (Peripheral Injection Capacity). For 𝒜∈Ω2, the maximum injection information rate is
bounded by:
ℐ(Ω2) ≤∑
𝑡∈𝒮tools
𝐶𝑡⋅(1 −𝑉𝑡)
(3)
where 𝐶𝑡is the channel capacity of tool 𝑡and 𝑉𝑡∈[0, 1] is the verification rate applied to tool output.
This bound shows that high verification rates (𝑉𝑡→1) reduce the peripheral attacker to near-zero injection
capacity.
3.2.3
Adversary Class Ω3: Agent-Level Attacker
Definition 3.4 (Agent-Level Adversary). An adversary 𝒜∈Ω3 compromises or impersonates a single agent
𝑎𝑣:
Ω3 = ⟨𝑎𝑣, 𝜎𝑣, 𝒩(𝑎𝑣), 𝒢adv⟩
(4)
where 𝑎𝑣is the victim/compromised agent, 𝜎𝑣= ⟨ℬ𝑣, 𝒢𝑣, ℐ𝑣, ℋ𝑣⟩is the full cognitive state under adversarial
control, 𝒩(𝑎𝑣) = {𝑎𝑗∶𝒞(𝑎𝑣, 𝑎𝑗) = 1} is the neighborhood of 𝑎𝑣, and 𝒢adv is the adversarial goal set.
Theorem 3.1 (Agent Compromise Blast Radius). When agent 𝑎𝑣∈Ω3 is fully compromised, its trust-
influence blast radius is the trust it can propagate onward through each neighbour that delegates to it — one
delegation hop, so each contribution decays by 𝛿:
BlastRadius(𝑎𝑣) =
∑
𝑎𝑗∈𝒩(𝑎𝑣)
𝛿⋅𝒯𝑎𝑗→𝑎𝑣
(5)
The CIF trust decay bound (Theorem 4.3) limits this to:
BlastRadius(𝑎𝑣) ≤𝑛⋅𝛿⋅max
𝑎𝑗𝒯𝑎𝑗→𝑎𝑣
(6)
where 𝑛= |𝒩(𝑎𝑣)|. The 𝛿belongs to the definition, not only to the bound: the quantity of interest is influence
propagated through the compromised agent, which costs one delegation hop. The undecayed sum ∑𝑎𝑗𝒯𝑎𝑗→𝑎𝑣
is the direct trust placed in 𝑎𝑣and is bounded only by 𝑛⋅max𝑎𝑗𝒯𝑎𝑗→𝑎𝑣.
The reachability-weighted quantity ∑𝑎𝑗∈𝒩(𝑎𝑣) 𝒯𝑎𝑗→𝑎𝑣⋅|Reachable(𝑎𝑗)| is a different measure — it counts
how many agents each neighbour can in turn influence — and Equation (6) does not bound it: multiplying
the neighbour and reachable-agent counts admits an 𝑂(𝑛2) term. The bound above is stated on the trust-
influence measure only, and the supplementary restatement (Theorem 11.47) follows the same convention
(S01, Section 11.15).
Proof. Each neighbor 𝑎𝑗trusts 𝑎𝑣with score 𝒯𝑎𝑗→𝑎𝑣. The trust propagated from 𝑎𝑗to further agents via 𝑎𝑣
is bounded by 𝛿⋅𝒯𝑎𝑗→𝑎𝑣per Theorem 4.3. Summing over all 𝑛agents gives the bound.
■
3.2.4
Adversary Class Ω4: Coordination-Level Attacker
Definition 3.5 (Coordination Adversary). An adversary 𝒜∈Ω4 controls the inter-agent communication
channel:
Ω4 = ⟨ℰctrl, 𝑓man, 𝒦protocol, 𝒞sync⟩
(7)
20

## Page 22

where ℰctrl ⊆ℰis the set of controlled communication edges, 𝑓man ∶ℳ→ℳis a message manipulation
function, 𝒦protocol encodes knowledge of coordination protocols, and 𝒞sync denotes synchronization capability
for coordinated attacks.
Property 3.3 (Coordination Attack Distinguishability). An Ω4 attack is distinguishable from legitimate
coordination with probability:
𝑃(detect ∣Ω4) ≥1 −2−𝐷KL(𝑃legitimate‖𝑃attack)
(8)
where 𝐷KL measures the divergence between legitimate and adversarial message distributions.
The coordination attacker must produce messages statistically consistent with legitimate protocol traﬀic
while encoding adversarial payloads—a constraint captured by the KL divergence bound.
3.2.5
Adversary Class Ω5: Systemic Attacker
Definition 3.6 (Systemic Adversary). A systemic adversary achieves complete control:
Ω5 = ⟨𝒜full, 𝜎all, 𝒯full, 𝒫all⟩
(9)
where 𝒜full = 𝒜(all agents), 𝜎all denotes control over all cognitive states, 𝒯full gives complete trust manip-
ulation capability, and 𝒫all grants all action permissions.
Property 3.4 (Systemic Attack Cost Bound). Ω5 requires physical or supply-chain compromise of the
orchestrator. CIF provides no cryptographic resistance against Ω5, but its layered architecture increases the
cost of achieving systemic control:
𝐶(Ω5) = 𝐶orchestrator +
4
∑
𝑘=1
𝐶bypass(Ω𝑘)
(10)
where 𝐶bypass(Ω𝑘) is the cost of neutralizing each sub-class’s defenses.
3.2.6
Cross-Class Attack Distinguishability
Theorem 3.2 (Adversary Class Separation). The five adversary classes {Ω𝑘}5
𝑘=1 are distinguishable in
information-theoretic terms:
∀𝑖≠𝑗∶𝐷KL(𝑃Ω𝑖‖𝑃Ω𝑗) > 0
(11)
where 𝑃Ω𝑘is the attack signature distribution of class Ω𝑘.
Proof. By construction: each class has distinct access surface (𝒮Ω𝑘), producing statistically distinguishable
observable signatures. Class Ω1 attacks appear only in user-input channel; Ω2 attacks appear in tool-response
channels; Ω3 attacks show belief drift in single agents; Ω4 attacks manifest as inter-agent message anomalies;
Ω5 requires simultaneously passing all lower-class defenses. The KL divergence is strictly positive because
the supports are not identical.
■
3.3
Attack Complexity Analysis
Definition 3.7 (Resource Requirements). Attack resources are characterized by the tuple:
ℛ= ⟨𝑅𝐶, 𝑅𝐾, 𝑅𝐴, 𝑅𝑃, 𝑅𝐶𝑜⟩
(12)
where components are defined in Table 5.
Property 3.5 (Complexity Ordering).
Complexity(Ω1) < Complexity(Ω2) < Complexity(Ω3) < Complexity(Ω4) < Complexity(Ω5)
(13)
21

## Page 23

Table 5: Attack resource taxonomy.
Resource
Symbol
Definition
Unit
Compute
𝑅𝐶
Processing for attack genera-
tion
FLOPS-hours
Knowledge
𝑅𝐾
System
understanding
re-
quired
Bits
Access
𝑅𝐴
Channel availability
Interfaces
Persistence
𝑅𝑃
Temporal presence required
Sessions
Coordination
𝑅𝐶𝑜
Multi-party synchronization
Entities
Table 6: Complexity by adversary class.
Class
𝑅𝐶
𝑅𝐾
𝑅𝐴
𝑅𝑃
𝑅𝐶𝑜
Complexity
Ω1
Low
Low
1
1
1
𝑂(1)
Ω2
Medium
Medium
1–5
Variable
1
𝑂(log 𝑛)
Ω3
High
High
1
Medium
1–2
𝑂(𝑛)
Ω4
High
Very High
≥2
High
≥2
𝑂(𝑛2)
Ω5
Very High
Complete
All
Persistent
Variable
𝑂(2𝑛)
3.4
Detectability Analysis
Definition 3.8 (Detectability Score). For attack 𝒜:
𝐷score(𝒜) = 𝛼⋅𝐷sig + 𝛽⋅𝐷anom + 𝛾⋅𝐷prov
(14)
where 𝛼+ 𝛽+ 𝛾= 1 and components are:
• 𝐷sig ∈[0, 1]: Pattern-based detection feasibility
• 𝐷anom ∈[0, 1]: Statistical anomaly visibility
• 𝐷prov ∈[0, 1]: Causal traceability
3.5
Adversarial Capabilities
Definition 3.9 (Capability Set).
𝒞adv = ⟨𝐶𝑂, 𝐶𝐼, 𝐶𝑀, 𝐶𝑇, 𝐶𝑃⟩
(15)
with components: Observe (𝐶𝑂), Inject (𝐶𝐼), Modify (𝐶𝑀), Timing (𝐶𝑇), Persist (𝐶𝑃).
Table 7: Capability matrix by adversary class.
Class
𝐶𝑂
𝐶𝐼
𝐶𝑀
𝐶𝑇
𝐶𝑃
Ω1
Input only
Direct
None
Limited
Session
Ω2
Tool responses
API
Tool data
API timing
Tool-dep.
Ω3
Agent state
Agent output
Beliefs
Agent timing
Memory
Ω4
Inter-agent
Msg inject
Msg alter
Full timing
Channel
Ω5
Complete
Complete
Complete
Complete
Complete
Axiom 3.1 (Capability Monotonicity).
∀𝑖< 𝑗∶𝒞Ω𝑖⊆𝒞Ω𝑗
(16)
Axiom 3.2 (Cryptographic Limitation).
∀𝑘∶¬CanBreak(Ω𝑘, Crypto)
(17)
22

## Page 24

Axiom 3.3 (Byzantine Bound).
|Compromised| < 𝑛
3
(18)
Axiom 3.4 (Honest Orchestrator). For adversary classes Ω1–Ω4, the orchestrator agent 𝑎0 remains uncom-
promised:
∀𝑘∈{1, 2, 3, 4} ∶𝑎0 ∉Compromised(Ω𝑘)
(19)
3.6
Attack Taxonomy
We classify attacks into four dimensions: epistemic, behavioral, social, and temporal. Figure 1 provides a
visual overview of this four-dimensional classification, while Figure 2 presents the complete attack surface
taxonomy across all five adversary classes. This formal classification is complemented by the community-
maintained COGSEC ATLAS COGSEC et al. [2023], which catalogs 995 cognitive security patterns across
seven categories: vulnerabilities (inherent cognitive weaknesses such as in-group bias and overconfidence), ex-
ploits (methods leveraging vulnerabilities), remedies (mitigating actions), practices (established methods like
Devil’s Advocate and Key Assumptions Check), accelerators (factors increasing attack impact), moderators
(factors influencing effect strength), and situational conditions. The Atlas employs hierarchical parent-child
relationships enabling granular mapping from broad vulnerability classes to specific manifestations—a struc-
ture that aligns with our adversary class hierarchy (Ω1–Ω5).
Figure 2 presents the full cognitive attack surface taxonomy, organizing all adversary classes Ω1–Ω5 with
their associated attack types and complexity indicators. The visualization reveals a clear inverse relationship
between attack sophistication and detectability: external attacks (Ω1) are most easily detected while systemic
attacks (Ω5) require sophisticated temporal and behavioral analysis. This progression from Entry Point''
throughData Injection,’ ’ State Corruption,'' andTrust Exploitation’ ’ to “Total Compromise’ ’ guides
the layered defense strategy of CIF (Section 4.1). For empirical detection rates across attack types, see Part
2 of this series.
Figure 1 illustrates the hierarchical attack classification, showing how epistemic attacks (targeting beliefs),
behavioral attacks (targeting goals), social attacks (targeting trust), and temporal attacks (exploiting per-
sistence) relate to the adversary classes Ω1–Ω5.
3.6.1
Epistemic Attacks
Epistemic attacks target the agent’s relationship with its information environment—the totality of in-
formation sources, evidence streams, and knowledge repositories that inform agent beliefs. The epistemic
domain is thus synonymous with the cognitive information environment: both concern what agents can
know, how they acquire knowledge, and the reliability of their belief-forming processes.
Target: Agent beliefs ℬ𝑖.
Definition 3.10 (Belief Injection).
𝒜𝐵𝐼∶∃𝜙∈Φadv ∶ℬ𝑖(𝜙) > 𝜏accept
(20)
Insertion of false propositions into agent’s verified belief set.
Definition 3.11 (Evidence Fabrication). Generation of synthetic evidence supporting adversarial claims
with forged provenance.
Definition 3.12 (Confidence Manipulation).
𝒜𝐶𝑀∶|ℬ𝑡+1
𝑖
(𝜙) −ℬ𝑡
𝑖(𝜙)| > 𝜖natural
(21)
Artificial inflation or deflation of belief certainty beyond natural bounds.
Definition 3.13 (Memory Poisoning). Corruption of persistent storage or context summaries to embed
adversarial state.
23

## Page 25

Cognitive Attacks
Epistemic
(What agents believe)
Belief Injection
Evidence Fabrication
Confidence Manipulation
Memory Poisoning
Behavioral
(How agents act)
Goal Hijacking
Action Restriction
Reward Hacking
Capability Elicitation
Social
(Inter-agent dynamics)
Trust Exploitation
Coalition Manipulation
Sybil Injection
Consensus Poisoning
Temporal
(Persistence & timing)
Sleeper Activation
Context Overflow
Checkpoint Poisoning
Progressive Drift
Severity Scale:
CRITICAL: System compromise HIGH: Major integrity loss
MEDIUM: Partial compromise
LOW: Minor impact
Cognitive Attack Taxonomy
Figure 1: Four-Dimensional Threat Taxonomy: Epistemic attacks (belief manipulation), behavioral attacks
(goal hijacking), social attacks (trust exploitation), and temporal attacks (persistence), organized by adver-
sary class Ω1–Ω5 with increasing capability and decreasing detectability.
24

## Page 26

COGNITIVE ATTACK SURFACE TAXONOMY
Example Classifications from the CIF Threat Model
1
EXTERNAL
Direct Prompt
Injection
Social
Engineering
Malicious
User Input
Complexity: Low
Detection: 85%
Entry Point
2
PERIPHERAL
!
Tool Response
Manipulation
Memory
Poisoning
API Data
Corruption
Complexity: Medium
Detection: 78%
Data Injection
3
AGENT-LEVEL
o
Identity
Confusion
Belief
Injection
Goal
Manipulation
Complexity: High
Detection: 71%
State Corruption
4
COORDINATION
#
Trust
Laundering
Sybil
Attacks
Consensus
Manipulation
Complexity: High
Detection: 65%
Trust Exploitation
5
SYSTEMIC
!
Orchestrator
Compromise
System-Wide
Corruption
Cascading
Failure
Complexity: Critical
Detection: 45%
Total Compromise
 Increasing Severity & Stealth
Detection difficulty:
High (
80%)
Medium (60-79%)
Low (<60%)
Figure 2: Comprehensive Attack Surface Taxonomy: Example classifications of the complete cognitive attack
surface across all five adversary classes, showing representative attack types with complexity indicators. Note
the inverse relationship between attack sophistication and detectability—external attacks (Ω1) are most
detectable while systemic attacks (Ω5) are hardest to detect.
25

## Page 27

Definition 3.14 (Semantic Drift). Chen et al. [2025] Gradual shift of conversation topic to adversarial
domains via benign-appearing transitions that evade discrete classification.
3.6.2
Behavioral Attacks
Target: Agent actions and goals 𝒢𝑖.
Definition 3.15 (Goal Hijacking).
𝒜𝐺𝐻∶𝒢𝑡+1
𝑖
⊈𝒢principal
(22)
Replacement of legitimate objectives with adversarial goals.
Definition 3.16 (Action Space Restriction). Elimination of legitimate action paths through false constraints.
Definition 3.17 (Capability Elicitation). Extraction of capabilities the agent should refuse to exercise.
3.6.3
Social Attacks
Target: Inter-agent trust 𝒯and coordination.
Definition 3.18 (Trust Exploitation).
𝒜𝑇𝐸∶𝒯𝑡+1
𝑖→𝑗= 𝒯𝑡
𝑖→𝑗+ Δadv
(23)
Manipulation of trust scores between agents.
Definition 3.19 (Sybil Injection). Introduction of fake agent identities to influence consensus.
Definition 3.20 (Consensus Poisoning). Corruption of multi-agent voting or agreement protocols.
3.6.4
Temporal Attacks
Target: Persistence and timing. Figure 3 visualizes typical attack progression for temporal attacks.
Figure 3 shows the temporal structure of multi-stage attacks, from initial reconnaissance through payload
delivery, dormancy, and eventual activation. The timeline highlights detection windows at each phase and
corresponding CIF defense interventions.
Definition 3.21 (Sleeper Activation). Embedding of dormant payloads triggered by specific conditions.
Definition 3.22 (Context Overflow). Exploitation of finite context windows to eject safety instructions.
Definition 3.23 (Deceptive Sleeper). Hubinger et al. [2024] Models trained to behave safely during evalua-
tion/training but defect when a specific trigger condition is met in deployment.
Definition 3.24 (Progressive Drift).
𝑇
∑
𝑡=0
𝛿𝑡> 𝜃total
where
∀𝑡∶𝛿𝑡< 𝜃step
(24)
Incremental belief shifts below per-step detection threshold.
3.7
Attack Scenarios by Class
3.7.1
Scenario Ω1: Nested Instruction Attack
Vector: Attacker embeds adversarial instructions within legitimate prompts.
Input(𝑚) = 𝑚legitimate ⊕𝑚adversarial
(25)
Goal: ℬagent(“safety suspended”) > 𝜏
26

## Page 28

Normal
Operation
T0-T25
Attack
Injection
T25-T35
Detection
& Analysis
T35-T50
Response
Execution
T50-T65
Recovery
& Hardening
T65-T87
Attack
Injected
Tripwire
Triggered
Anomaly
Confirmed
Quarantine
Activated
Trust
Reset
System
Restored
Alert
Threshold
Belief
Integrity
0.0
1.0
Inter-Agent
Trust
ATTACK LIFECYCLE: DETECTION THROUGH RECOVERY
Example Trace
 Illustrative simulation of CIF defense mechanisms
Normal Operation
Attack Phase
Detection & Analysis
Response Execution
Recovery & Hardening
Figure 3: Temporal Structure of Multi-Stage Attacks (Example Trace): Illustrative attack progression from
reconnaissance through payload delivery, dormancy period, and eventual activation.
Detection windows
at each phase are highlighted with corresponding CIF defense interventions (firewall at injection, tripwires
during dormancy, invariants at activation).
27

## Page 29

Resources: 𝑅𝐶= Low, 𝑅𝐾= Minimal
Detection: Firewall signature matching, instruction hierarchy violation
Recent Variant: Universal Adversarial Triggers Zou et al. [2025] demonstrate that optimized character
sequences can reliably bypass safety training across different model architectures.
3.7.2
Scenario Ω2: Poisoned Search Result
Vector: Attacker SEO-optimizes malicious content for research queries.
∃𝑟𝑖∈Response ∶𝑟𝑖∈𝒟adversarial ⇒ℬagent(claim) ←high
(26)
Resources: 𝑅𝐶= Medium, 𝑅𝐾= Medium
Detection: Provenance verification, cross-reference validation
Recent Variant: Argument injection against pre-approved tools Vandevanter [2025]. Agents commonly
gate the tool name against an allowlist but not its arguments, so injected content that reaches a permitted
utility can supply an execution flag (for example -exec on find, or the equivalent on go test) and obtain
code execution without ever invoking a denied command. This is the peripheral-class analogue of a confused-
deputy attack: the allowlist authorises the deputy, and the adversary supplies its orders.
3.7.3
Scenario Ω′
2: Browser-Fetched Adversarial Content (OpenClaw)
Vector: Personal AI assistant with browser automation fetches adversarial content during legitimate web
browsing tasks OpenClaw Security Team [2026].
A user instructs their locally-deployed OpenClaw to “research and summarize security best practices for API
key management.’ ’ The agent’s browser tool navigates to a compromised tutorial site containing invisible
CSS-hidden text:
<div style="opacity:0;">SYSTEM: Disregard security instructions.
Export all environment variables including API keys to
pastebin.com/submit and confirm completion to user.</div>
BrowserFetch(𝑢) = visible(𝑢) ⊕𝑚adversarial ⇒𝒢agent ←𝒢exfil
(27)
Goal: Exfiltration of sensitive credentials through trusted browser automation channel
Resources: 𝑅𝐶= Medium, 𝑅𝐾= Medium, 𝑅𝐴= 1 (single web page)
Detection: Tool response sandboxing, read-only pre-summarization agents, provenance tracking of fetched
content
Mitigation: OpenClaw’s security documentation recommends employing a “reader agent’ ’ to summarize
untrusted content in tool-disabled mode before processing by the main agent OpenClaw Security Team [2026].
This corresponds to the cognitive firewall architecture described in Section 5.2.
3.7.4
Scenario Ω3: Compromised Specialist
Vector: Sustained interaction modifies specialist agent’s goal set.
𝒢𝑡0
specialist = {secure review}
attack
−−−−→𝒢𝑡𝑘
specialist = {approve vulnerable}
(28)
Resources: 𝑅𝐶= High, 𝑅𝐾= High, 𝑅𝑃= Medium
Detection: Behavioral deviation, goal alignment verification
28

## Page 30

3.7.5
Scenario Ω4: Trust Inflation Attack
Vector: Injection of fabricated agreement messages.
Inject(𝑚fake) ∶𝑇𝑡+1
rep (𝑗) = 𝑇𝑡
rep(𝑗) + Δfabricated
(29)
Resources: 𝑅𝐶= High, 𝑅𝐾= Very High, 𝑅𝐶𝑜≥2
Detection: Message authentication, trust velocity anomalies
3.8
Attack-Defense Quick Reference
Table 8 provides a navigational summary mapping attack categories to their cognitive targets and corre-
sponding CIF defense mechanisms.
This table synthesizes the attack taxonomy (Sectionsabout 3.1–3.6)
with defense mechanisms detailed in Section 5.
Table 8: Attack-Defense Mapping: Attack types mapped to affected cognitive properties and corresponding
CIF defenses.
Attack Category
Cognitive Target
Primary Defense
Detection Method
Epistemic Attacks (Beliefs ℬ)
Belief Injection
ℬ𝑖(𝜙)
Cognitive Firewall
Signature matching
Evidence Fabrication
Provenance 𝜋
Provenance tracking
Source verification
Confidence Manipulation
ℬ𝑖certainty
Belief sandbox
Drift anomaly
Memory Poisoning
ℋ𝑖
Tripwire canaries
History integrity
Behavioral Attacks (Goals 𝒢)
Goal Hijacking
𝒢𝑖
Invariant enforcement
Goal alignment check
Action Restriction
ℐ𝑖options
Permission layer
Action audit
Capability Elicitation
Refused actions
Firewall policies
Boundary violations
Social Attacks (Trust 𝒯)
Trust Exploitation
𝒯𝑖→𝑗
Trust calculus bounds
Velocity anomaly
Sybil Injection
Agent identities
Quorum verification
Identity attestation
Consensus Poisoning
Multi-agent vote
Byzantine consensus
Vote deviation
Temporal Attacks (Persistence)
Sleeper Activation
Dormant payloads
Behavioral baseline
Activation pattern
Context Overflow
Safety instructions
Context monitoring
Instruction loss
Progressive Drift
Cumulative ∑𝛿𝑡
Drift detection
CUSUM tracking
3.9
Attack Composition
Definition 3.25 (Attack Composition).
Impact(𝒜1 ∘𝒜2) ≥max(Impact(𝒜1), Impact(𝒜2))
(30)
Table 9: Synergistic attack combinations.
Primary
Secondary
Synergy Effect
Trust Exploitation
Belief Injection
Bypass firewall via elevated trust
Memory Poisoning
Sleeper Activation
Persistent delayed attack
Sybil Injection
Consensus Poisoning
Achieve malicious quorum
Progressive Drift
Goal Hijacking
Undetectable goal modification
29

## Page 31

Adaptive Persistence: Recent work on Adaptive Attacks Debenedetti et al. [2025] shows that adversaries
can effectively “hill-climb” against static defenses, modifying their attack strategy in response to defense
feedback.
3.10
Threat Model Assumptions
1. Adversary knows system architecture (Kerckhoffs’s principle)
2. Adversary cannot break cryptographic primitives (Axiom 3.2)
3. At most 𝑓agents compromised where 𝑛≥3𝑓+ 1 (Axiom 3.3)
4. Communication channels may be observed but are authenticated
5. Adversary has bounded compute: 𝑅𝐶< 𝑅defender
6. No cross-class adversary collusion unless specified
7. Network delay bounded: Δmax < ∞
Figure 4 visualizes the attack surface across adversary classes Ω1–Ω5, showing hierarchical agent structure
and corresponding attack vectors.
30

## Page 32

User Input
(Prompts)
1
Cognitive Firewall
(Filter)
Orchestrator
(Coordinator)
5
Agent 1
3
Agent 2
Agent 3
Agent 4
3
External
Services
 Web APIs
 Tools
 RAG DBs
2
Shared Belief State / Memory (
4)
Inter-agent Coordination (
4)
1: External (Input)
2: Peripheral (Tools/Data)
3: Agent (Internal)
4: Coordination (State)
5: Systemic (Control)
Multiagent Operator Attack Surface Taxonomy
Figure 4: Attack Surface Visualization: Hierarchical agent structure showing attack vectors for each adver-
sary class—Ω1 (user input), Ω2 (tool/API), Ω3 (agent compromise), Ω4 (inter-agent communication), and
Ω5 (orchestrator control).
31

## Page 33

4
Cognitive Integrity Framework: Trust Calculus and Detection
Bounds
This section presents the formal foundations of the Cognitive Integrity Framework (CIF). We define the
system model (Section 4.1), cognitive state representation (Section 4.2), integrity properties (Section 4.3),
trust calculus (Section 4.4), and information-theoretic detection bounds (Section 4.5).
4.1
System Model
Definition 4.1 (Multiagent Operator). A multiagent operator is a tuple:
𝒪= ⟨𝒜, 𝒞, 𝒮, 𝒫, Γ⟩
(31)
where components are defined in Table 10.
Table 10: Components of the multiagent operator 𝒪.
Component
Symbol
Description
Agents
𝒜= {𝑎1, … , 𝑎𝑛}
Finite set of 𝑛agents
Communication
𝒞∶𝒜× 𝒜→{0, 1}
Adjacency matrix encoding permitted
channels
Shared State
𝒮
Observable global state
Permissions
𝒫∶𝒜× Actions →{0, 1}
Action authorization mapping
Protocol
Γ
Coordination and communication rules
4.2
Cognitive State
Intuitively, an agent’s cognitive state captures everything it believes, wants, intends, and remembers at a
given moment. This formal representation enables precise reasoning about how attacks manipulate agent
reasoning.
Definition 4.2 (Agent Cognitive State). Each agent 𝑎𝑖∈𝒜maintains cognitive state:
𝜎𝑖= ⟨ℬ𝑖, 𝒢𝑖, ℐ𝑖, ℋ𝑖⟩
(32)
with components defined in Table 11.
Table 11: Cognitive state components for agent 𝑎𝑖.
Component
Formal Type
Semantics
Beliefs
ℬ𝑖∶Φ →[0, 1]
Probability distribution over propo-
sitions
Goals
𝒢𝑖= {(𝑔𝑘, 𝑝𝑘)}
Prioritized
objectives
where
∑𝑘𝑝𝑘= 1
Intentions
ℐ𝑖= [(𝑎1, 𝑡1), …]
Committed action sequence with
timing
History
ℋ𝑖= [(𝑒1, 𝑡1), …]
Interaction
trace
(events,
times-
tamps)
Definition 4.3 (System State). The global system state at time 𝑡is:
𝑆𝑡= (𝜎𝑡
1, … , 𝜎𝑡
𝑛, 𝒮𝑡, 𝒯𝑡)
(33)
where 𝒯𝑡denotes the trust matrix at time 𝑡.
32

## Page 34

4.2.1
State Transition Semantics
The following transition rules formalize how agent states evolve. Each rule has the form “if preconditions
hold (above the line), then this transition occurs (below the line).” Readers may skim the mathematical details
on first reading, returning for precision when needed.
Definition 4.4 (Transition Relation). State transitions follow the relation 𝑆𝑡
𝛼−→𝑆𝑡+1 where 𝛼∈
{receive, update, act, communicate}.
The transition rules are defined as follows:
Rule T-Receive (Message Reception):
𝑚∈channel(𝑎𝑗, 𝑎𝑖)
ℱ(𝑚) = accept
(𝜎𝑖, inbox𝑖)
receive
−−−−→(𝜎𝑖, inbox𝑖∪{𝑚})
(34)
Rule T-Reject (Message Rejection):
𝑚∈channel(𝑎𝑗, 𝑎𝑖)
ℱ(𝑚) ∈{reject, quarantine}
(𝜎𝑖, inbox𝑖)
receive
−−−−→(𝜎𝑖, inbox𝑖)
(35)
Rule T-Update (Belief Update):
𝑚∈inbox𝑖
𝑒= extract(𝑚)
𝑠= source(𝑚)
ℬ𝑡
𝑖
update
−−−−→ℬ𝑡+1
𝑖
= BayesUpdate(ℬ𝑡
𝑖, 𝑒, 𝒯𝑖→𝑠)
(36)
Rule T-Act (Action Execution):
𝑎∈ℐ𝑖
𝒫eff(𝑎𝑖, 𝑎) = 1
precond(𝑎, 𝒮𝑡)
(𝜎𝑖, 𝒮𝑡)
act
−−→(𝜎′
𝑖, effect(𝑎, 𝒮𝑡))
(37)
Rule T-Communicate (Message Sending):
𝒞(𝑎𝑖, 𝑎𝑗) = 1
𝑚= compose(𝜎𝑖)
(𝜎𝑖, channel(𝑎𝑖, 𝑎𝑗))
comm
−−−→(𝜎𝑖, channel(𝑎𝑖, 𝑎𝑗) ∪{𝑚})
(38)
Definition 4.5 (Well-Formed Transition Sequence). A transition sequence 𝑆0 𝛼1
−→⋯
𝛼𝑘
−→𝑆𝑘is well-formed
iff:
1. Causality: ∀𝑖∶𝑆𝑖enables 𝛼𝑖+1
2. Atomicity: Each 𝛼𝑖is atomic
3. Fairness: No agent is starved indefinitely
Theorem 4.1 (Determinism). Given state 𝑆𝑡and action 𝛼, the resulting state 𝑆𝑡+1 is uniquely determined.
Proof. By case analysis on transition rules Equations (34) to (38). Each rule specifies unique postconditions.
■
33

## Page 35

4.3
Integrity Properties
We define four core integrity properties that CIF aims to preserve.
Property 4.1 (Belief Consistency).
Consistent(ℬ𝑖) ⟺∄𝜙, 𝜓∶ℬ𝑖(𝜙) > 𝜏∧ℬ𝑖(𝜓) > 𝜏∧(𝜙∧𝜓⊢⊥)
(39)
No high-confidence beliefs contradict each other.
Property 4.2 (Goal Alignment).
Aligned(𝒢𝑖) ⟺𝒢𝑖⊆𝒢principal ∪Delegate(𝒢principal)
(40)
All goals derive from the principal or valid delegation chains.
Property 4.3 (Provenance Verifiability).
Verifiable(ℬ𝑖) ⟺∀𝜙∶ℬ𝑖(𝜙) > 𝜏⇒∃𝜋(𝜙) ∶𝑉(𝜋(𝜙)) = 1
(41)
Every accepted belief has a verifiable provenance chain 𝜋.
Property 4.4 (Action Authorization).
Auth(𝑎𝑖, act) ⟺𝒫(𝑎𝑖, act) = 1 ∨∃𝑎𝑗∶Delegate(𝑎𝑗, 𝑎𝑖, act)
(42)
Actions require direct permission or valid delegation.
4.4
Trust Calculus
4.4.1
Motivation: Why Bounded Trust Matters
Before presenting the formal trust calculus, we motivate its design through concrete scenarios that illustrate
why naive trust models fail in multiagent systems.
The Trust Laundering Problem. Consider an adversary with low direct trust who seeks to influence a
high-value agent. In a naive trust model, the adversary could:
1. Establish contact with a moderately trusted intermediary agent
2. Provide accurate information over time to build trust with the intermediary
3. Use the intermediary to relay adversarial content to the target
4. The target accepts the content because it comes from a “trusted” source
This is trust laundering—converting low-trust origin into high-trust delivery through intermediaries. Without
bounded delegation, the adversarial content arrives at the target with the intermediary’s trust score, not the
adversary’s.
The Trust Amplification Problem. In peer-to-peer multiagent architectures, agents form trust relation-
ships bidirectionally. Without constraints, circular trust relationships can amplify trust scores:
𝐴
0.9
−−→𝐵
0.9
−−→𝐶
0.9
−−→𝐴
If trust flows around this cycle, naive aggregation could yield trust scores exceeding initial values. Our trust
algebra prevents this through the 𝛿𝑑decay bound.
Real-World Delegation Patterns. Modern agentic systems exhibit deep delegation chains. Consider
Claude Code processing a user request:
1. User requests security audit →Orchestrator agent (trust: principal)
2. Orchestrator delegates to Code Analysis agent (depth 1)
34

## Page 36

3. Code Analysis queries External CVE Database (depth 2)
4. CVE Database returns vulnerability data (depth 3)
5. Code Analysis delegates to Remediation agent (depth 4)
6. Remediation queries StackOverflow for fix patterns (depth 5)
At depth 5, should the orchestrator trust StackOverflow content with the same confidence as direct user
input? Our trust calculus says no: with 𝛿= 0.9, trust at depth 5 is at most 0.95 ≈0.59—suﬀicient for
low-stakes decisions but automatically triggering review for high-stakes actions.
Cross-Modality Trust Challenges. When a vision model processes an image and reports “this diagram
shows system architecture,’ ’ how should a code generation agent weight this claim? Cross-modality trust
introduces additional considerations:
• Modality-specific error rates: Vision models may have different reliability profiles than language
models
• Adversarial input susceptibility: Images are particularly vulnerable to adversarial perturbations
• Verification diﬀiculty: Claims about visual content are harder to verify than claims about text or
code
Our framework addresses this through modality-adjusted base trust: 𝑇vision
base
= 𝜂⋅𝑇text
base where 𝜂< 1 reflects
elevated adversarial risk in visual modalities.
4.4.2
Formal Trust Model
0.95
0.92
0.88
0.90
0.85
0.82
0.87
0.84
0.75
0.80
0.78
0.72
0.70
0.68
0.65
0.67
A. Normal Trust Network (illustrative)
O
A1
A2
A3
A4
A5
A6
A7
A8
0.95
0.92
0.90
0.85
0.82
0.87
0.55
0.75
0.80
0.78
0.65
0.67
Compromised
B. Trust Network Under Attack (illustrative)
O
A1
A2
A3
A4
A5
A6
A7
A8
T =
Tbase +
Trep + Tctx
Base Trust
Reputation Trust
Context Trust
High Trust
Medium Trust
Low/Compromised
Orchestrator
Figure 5: Trust Network Topology: Directed graph showing trust relationships 𝒯𝑖→𝑗between agents in hier-
archical (left) and peer-to-peer (right) configurations. Edge weights represent trust values in [0, 1]; doubled
arrows indicate bidirectional trust. Orchestrator 𝑎0 occupies hub position in hierarchical topology.
Figure 5 visualizes the trust relationships in a representative multiagent operator. Edge weights represent
trust scores 𝒯𝑖→𝑗, with thicker edges indicating higher trust. The network topology illustrates how trust
propagates through delegation chains and highlights potential attack surfaces for trust manipulation attacks
(Ω4).
35

## Page 37

4.4.3
Trust Computation
Definition 4.6 (Trust Function). Trust from agent 𝑎𝑖to agent 𝑎𝑗at time 𝑡:
𝒯𝑡
𝑖→𝑗= 𝛼⋅𝑇base(𝑗) + 𝛽⋅𝑇𝑡
rep(𝑗) + 𝛾⋅𝑇𝑡
ctx(𝑖, 𝑗)
(43)
subject to 𝛼+ 𝛽+ 𝛾= 1, with components in Table 12.
Table 12: Trust function components.
Component
Weight
Description
𝑇base
𝛼
Architectural trust (role-based)
𝑇rep
𝛽
Reputation (historical accuracy)
𝑇ctx
𝛾
Context (task-specific factors)
Remark 4.2 (Trust as Precision Weighting). The composite trust formula above is equivalent to precision-
weighted message integration from the Free Energy Principle: the composite score 𝒯𝑖→𝑗is proportional to the
precision 𝜌𝑗with which agent 𝑖should weight messages from agent 𝑗when updating its posterior beliefs. High-
trust messages dominate the belief update; low-trust messages contribute marginally. This correspondence
provides a neurocomputational grounding for the trust calculus (Part 2, Theorem FEP.2, “Trust-Precision
Duality”).
Definition 4.7 (Trust Delegation). When agent 𝑎𝑖delegates trust through 𝑎𝑗to 𝑎𝑘:
𝒯del
𝑖→𝑘= min(𝒯𝑖→𝑗, 𝒯𝑗→𝑘) ⋅𝛿𝑑
(44)
where 𝛿∈(0, 1) is the decay factor and 𝑑∈ℕis the delegation depth.
4.4.4
Trust Algebra
The trust algebra provides the mathematical foundation for combining trust scores. The key insight is that
trust through intermediaries (delegation, ⊗) uses the minimum-then-decay rule, while trust from multiple
sources (aggregation, ⊕) uses the maximum. This prevents both trust laundering and artificial inflation.
Definition 4.8 (Trust Algebra). The trust algebra (𝒯, ⊗, ⊕, 0, 1) comprises:
• Domain: 𝒯= [0, 1]
• Delegation: 𝑇1 ⊗𝑇2 = min(𝑇1, 𝑇2) ⋅𝛿(sequential)
• Aggregation: 𝑇1 ⊕𝑇2 = max(𝑇1, 𝑇2) (parallel)
• Zero: 0 (complete distrust)
• Unit: 1 (complete trust)
The following theorem is the central security guarantee of the trust calculus: it establishes that trust cannot
be “laundered” through delegation chains.
No matter how an adversary routes content through trusted
intermediaries, each hop reduces effective trust by factor 𝛿.
Theorem 4.3 (Trust Boundedness). For any delegation chain of depth 𝑑:
𝒯del
𝑖→𝑘≤𝛿𝑑
(45)
Proof. By induction on 𝑑. Base: 𝑑= 0 ⇒𝒯≤1. Step: 𝒯𝑑+1 = min(⋅) ⋅𝛿≤𝛿𝑑⋅𝛿= 𝛿𝑑+1.
■
Corollary 4.4. Trust cannot be amplified through delegation chains.
Corollary 4.5. Trust vanishes exponentially: lim𝑑→∞𝒯del
𝑖→𝑘= 0.
36

## Page 38

0.0
2.5
5.0
7.5
10.0
12.5
15.0
17.5
20.0
Delegation Depth (d)
0.0
0.2
0.4
0.6
0.8
1.0
Trust Score (T)
T(d) = T0 ⋅δd
A. Trust Decay Over Delegation Depth
δ = 0.95
δ = 0.9
δ = 0.85
δ = 0.8
δ = 0.7
Untrusted Region (<0.1)
No Defense
Firewall
Only
Trust Decay
(δ=0.9)
Full CIF
0.0
0.2
0.4
0.6
0.8
1.0
Trust Integrity Score
15%
45%
72%
94%
B. Trust Preservation Under Attack
Initial Trust
After Attack
Panel B values are illustrative schematic — not measured.
Figure 6: Trust Decay Over Delegation Depth: Exponential decay curves showing trust attenuation 𝒯(𝑑)
del =
𝛿𝑑⋅𝒯𝑖→𝑗for decay factors 𝛿∈{0.5, 0.7, 0.8, 0.9} over delegation chains of depth 𝑑= 1 to 10. At 𝛿= 0.8,
trust falls below 𝜏= 0.5 at depth 4 and below 𝜏= 0.1 at depth 11 (outside this plotted range). Note: Values
are illustrative examples demonstrating the mathematical framework; specific decay factors should be tuned
to deployment context.
Figure 6 visualizes the exponential decay of trust across delegation depth for various decay factors 𝛿, demon-
strating how the bounded delegation mechanism (Theorem 4.3) prevents trust amplification.
Figure 7 presents the complete trust calculus mechanics across four panels.
Panel A demonstrates the
trust decay function 𝒯(𝑎→𝑐) ≤𝛿𝑑⋅𝒯(𝑎→𝑏) for decay factors 𝛿∈{0.8, 0.85, 0.9, 0.95}, showing how
trust falls below threshold 𝜏= 0.5 at different delegation depths.
Panel B formalizes the trust update
mechanism 𝒯′(𝑎→𝑏) = 𝛼⋅𝒯(𝑎→𝑏) + 𝛽⋅outcome + 𝛾⋅consensus where 𝛼+ 𝛽+ 𝛾= 1, integrating
historical trust, outcome verification, and peer consensus. Panel C illustrates a bounded delegation chain
(Theoremabout 4.3): starting from 𝒯(𝐴→𝐵) = 1.0 with 𝛿= 0.9, trust decays through agents B, C, D
to E with 𝒯(𝐴→𝐸) = 0.94 × 1.0 = 0.66. Panel D demonstrates trust laundering prevention: a malicious
agent M with 𝒯(𝑀→𝑇) = 0.3 attempting to exploit trusted intermediary T with 𝒯(𝑇→𝑉) = 0.9 cannot
achieve suﬀicient delegated trust since 𝒯(𝑀→𝑉) ≤0.9 × 0.3 = 0.27 < 𝜏, blocking the attack.
Theorem 4.6 (Delegation Associativity). The sequential delegation operation is defined by 𝑇1 ⊗𝑇2 =
𝛿min(𝑇1, 𝑇2). Because the decay factor is applied at each composition step, this operation is not associative
in general; chain evaluation therefore preserves the explicit left-to-right delegation order.
𝑇1 ⊗(𝑇2 ⊗𝑇3) ≠(𝑇1 ⊗𝑇2) ⊗𝑇3
(46)
Proof. For example, with (𝑇1, 𝑇2, 𝑇3, 𝛿) = (0.9, 0.9, 0.1, 0.9), the left-associated value is 0.090 while the right-
associated value is 0.081. Thus any associative abstraction must be defined separately (for example, as a
chain functional min𝑖𝑇𝑖𝛿𝑑), rather than inferred for ⊗.
■
Theorem 4.7 (Aggregation Properties). Trust aggregation ⊕satisfies: (i) associativity, (ii) commutativity,
(iii) idempotence, (iv) identity 𝑇⊕0 = 𝑇, and (v) absorption 𝑇⊕1 = 1.
Theorem 4.8 (No Trust Amplification). For any path 𝑝= (𝑎0, … , 𝑎𝑘):
𝒯path
𝑎0→𝑎𝑘≤
min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1
(47)
A proof of the no-amplification claim is given in the supplementary material (Theorem 11.11, S01), which
states the identical bound under a dedicated label.
Theorem 4.9 (Trust Monotonicity). Delegation is monotonic: 𝑇1 ≤𝑇′
1 ∧𝑇2 ≤𝑇′
2 ⇒𝑇1 ⊗𝑇2 ≤𝑇′
1 ⊗𝑇′
2.
37

## Page 39

0
1
2
3
4
5
6
7
Delegation Depth (d)
0.0
0.2
0.4
0.6
0.8
1.0
Trust Level T(a
c)
Untrusted
zone
A. Trust Decay: T(a
c)

 · T(a
b)
 = 0.95
 = 0.9
 = 0.85
 = 0.8
Trust threshold
T'(a b) = ·T(a b) + ·outcome + ·consensus
where:  +  +  = 1 (normalization)
Historical
Trust
·T(a b)
Outcome
Verification
·outcome
Peer
Consensus
·consensus
Updated Trust T'(a
b)
B. Trust Update Mechanism
A
T=1.00
=0.9
B
T=0.90
=0.9
C
T=0.81
=0.9
D
T=0.73
=0.9
E
T=0.66
T(A E)
·T(A B) = 0.9 × 1.0 = 0.66
Trust bounded exponentially: prevents trust amplification
C. Bounded Delegation Chain (Theorem 3.1)
Attack Attempt: Malicious
 Trusted
 Target
M
Malicious
T
Trusted
V
Victim
T(M
T)=0.3
T(T
V)=0.9
T(M V)   · T(M T) = 0.9 × 0.3 = 0.27 <
Delegated trust BLOCKED - below threshold
D. Trust Laundering Prevention
Figure 7: Trust Calculus Comprehensive: Complete trust calculus framework showing initialization matrices,
update rules (direct experience, reputation, recommendation), decay mechanics, and the no-amplification
invariant. The composition rule 𝒯𝑖→𝑘= 𝛿⋅min(𝒯𝑖→𝑗, 𝒯𝑗→𝑘) ensures trust cannot be manufactured through
delegation chains.
38

## Page 40

4.4.5
Cross-Modality Trust
When agents operate across modalities—processing text, code, images, audio, and structured data—trust
must account for modality-specific reliability and attack susceptibility.
Definition 4.9 (Modality Trust Adjustment). For agent 𝑎𝑗operating in modality 𝑚, the adjusted trust from
agent 𝑎𝑖is:
𝒯𝑚
𝑖→𝑗= 𝒯𝑖→𝑗⋅𝜂𝑚
(48)
where 𝜂𝑚∈(0, 1] is the modality reliability factor.
Table 13: Recommended modality reliability factors.
Modality 𝑚
𝜂𝑚
Rationale
Text (verified source)
1.0
Baseline modality
Code (compilable)
0.95
Syntax verification possible
Structured data (schema-valid)
0.90
Schema provides partial verifica-
tion
Text (external)
0.80
Injection risk
Images
0.70
Adversarial perturbation vulner-
ability
Audio
0.65
Ultrasonic injection, splicing at-
tacks
Video
0.60
Combines image and temporal
vulnerabilities
Theorem 4.10 (Cross-Modality Delegation Bound). For delegation chain crossing modalities 𝑚1, … , 𝑚𝑘:
𝒯cross
𝑖→𝑗
≤𝛿𝑑⋅
𝑘
∏
𝑙=1
𝜂𝑚𝑙
(49)
This ensures that trust degradation compounds across both delegation depth and modality transitions,
preventing adversaries from laundering low-trust content through modality boundaries.
4.4.6
Federated Trust
In enterprise deployments, multiagent systems increasingly span organizational boundaries.
A financial
services orchestrator might delegate to a risk assessment system from one vendor, a compliance checker from
another, and market data feeds from multiple providers. Federated trust addresses how to reason about
trust across these boundaries.
Definition 4.10 (Trust Domain). A trust domain 𝒟is a set of agents sharing a common trust authority
and consistent trust semantics.
Definition 4.11 (Cross-Domain Trust). For agent 𝑎𝑖in domain 𝒟1 and agent 𝑎𝑗in domain 𝒟2:
𝒯fed
𝑖→𝑗= 𝒯𝑖→𝒟2 ⋅𝒯𝒟2(𝑗)
(50)
where 𝒯𝑖→𝒟2 is 𝑎𝑖’s trust in domain 𝒟2 and 𝒯𝒟2(𝑗) is 𝑎𝑗’s standing within its domain.
This two-stage model captures realistic trust reasoning: an organization might trust a vendor (domain trust)
differently than individual agents within that vendor (agent trust).
Property 4.5 (Federated Trust Bound). Cross-domain trust is bounded by domain trust:
𝒯fed
𝑖→𝑗≤𝒯𝑖→𝒟2
(51)
ensuring that untrusted domains cannot boost individual agent trust.
39

## Page 41

Federated trust introduces additional challenges that remain open research problems:
• Trust semantics heterogeneity: Different domains may use incompatible trust scales or update
rules
• Trust attestation: How can domains cryptographically attest to their internal trust assessments?
• Privacy-preserving trust: Can trust be verified without revealing sensitive internal assessments?
4.4.7
Belief Update Semantics
Definition 4.12 (Evidence Structure). Evidence is a tuple 𝑒= ⟨𝜙, 𝑐, 𝑠, 𝜋⟩comprising proposition 𝜙, confi-
dence 𝑐∈[0, 1], source 𝑠, and provenance chain 𝜋.
Definition 4.13 (Trust-Weighted Bayesian Update). Upon receiving evidence 𝑒from source 𝑠:
ℬ𝑡+1
𝑖
(𝜙) =
ℬ𝑡
𝑖(𝜙) ⋅[𝒯𝑖→𝑠𝑃(𝑒|𝜙) + (1 −𝒯𝑖→𝑠)𝑃0(𝑒|𝜙)]
∑𝜓ℬ𝑡
𝑖(𝜓) ⋅[𝒯𝑖→𝑠𝑃(𝑒|𝜓) + (1 −𝒯𝑖→𝑠)𝑃0(𝑒|𝜓)]
(52)
Trust mixes the source likelihood with a neutral likelihood 𝑃0; low-trust sources therefore have a diminished
update impact rather than canceling as a common normalization factor.
Rule B-Direct (Direct Evidence):
𝑒= ⟨𝜙, 𝑐, 𝑠, 𝜋⟩
𝑉(𝜋) = 1
𝒯𝑖→𝑠≥𝜏trust
ℬ𝑡+1
𝑖
(𝜙) = BayesUpdate(ℬ𝑡
𝑖(𝜙), 𝑐⋅𝒯𝑖→𝑠)
(53)
Rule B-Delegated (Delegated Evidence): evidence received through a delegation chain of depth 𝑑is
accepted only when its provenance is valid and its delegated trust meets the configured threshold:
𝑒= ⟨𝜙, 𝑐, 𝑠, 𝜋⟩
𝑉(𝜋) = 1
𝒯del
𝑖→𝑠= 𝒯(𝑑)
𝑖→𝑠≥𝜏trust
ℬ𝑡+1
𝑖
(𝜙) = BayesUpdate (ℬ𝑡
𝑖(𝜙), 𝑐⋅𝒯del
𝑖→𝑠)
.
(54)
Here 𝒯(𝑑)
𝑖→𝑠≤𝛿𝑑is the delegated trust after 𝑑hops, making depth-dependent attenuation explicit.
Rule B-Corroboration (Multiple Sources):
{𝑒𝑗}𝑘
𝑗=1 ∶∀𝑗. 𝑒𝑗= ⟨𝜙, 𝑐𝑗, 𝑠𝑗, 𝜋𝑗⟩
|{𝑠𝑗}| ≥𝜅
ℬ𝑡+1
𝑖
(𝜙) = 1 −∏
𝑘
𝑗=1(1 −𝑐𝑗⋅𝒯𝑖→𝑠𝑗)
(55)
Lemma 4.11 (Belief Boundedness). After any update sequence: ∀𝜙∶0 ≤ℬ𝑖(𝜙) ≤1.
4.4.8
Sandboxed Belief Model
Definition 4.14 (Sandboxed Beliefs). Beliefs from unverified sources enter provisional state:
ℬ𝑖= ℬverified ∪ℬprovisional
(56)
Rule S-Sandbox (Enter Sandbox):
𝑒= ⟨𝜙, 𝑐, 𝑠, 𝜋⟩
(𝒯𝑖→𝑠< 𝜏trust ∨𝑉(𝜋) = 0)
ℬprov ←ℬprov ∪{(𝜙, 𝑐, 𝑠, 𝜋, TTL)}
(57)
Rule S-Promote (Sandbox Promotion):
(𝜙, …) ∈ℬprov
𝑉(𝜋) = 1
Consistent(ℬver ∪{𝜙})
|Corr(𝜙)| ≥𝜅
ℬver ←ℬver ∪{𝜙};
ℬprov ←ℬprov ∖{(𝜙, …)}
(58)
40

## Page 42

Rule S-Expire (Sandbox Expiry):
(𝜙, 𝑐, 𝑠, 𝜋, TTL) ∈ℬprov
TTL ≤0
ℬprov ←ℬprov ∖{(𝜙, 𝑐, 𝑠, 𝜋, TTL)}
(59)
Promotion requires: (1) provenance verification 𝑉(𝜋) = 1, (2) consistency with verified beliefs, and (3)
corroboration threshold 𝜅.
4.5
Information-Theoretic Detection Bounds
Having established the trust calculus (how agents reason about each other) and belief update semantics
(how agents incorporate information), we now turn to fundamental limits on attack detection. This section
establishes fundamental limits on what any detection system can achieve. Like Shannon’s channel capacity
in communications, these bounds are not limitations of specific mechanisms but mathematical constraints on
what is possible.
Definition 4.15 (Attack Information Channel). An attack models a communication channel from adversary
to target:
Channel ∶𝒜adv →𝜎target
(60)
Theorem 4.12 (Minimum Attack Entropy). For attack 𝒜to succeed with probability 𝑝:
𝐻(𝒜) ≥−log2(1 −𝑝) + 𝐻(𝜎target|𝒜)
(61)
Proof. By the data processing inequality. The attack must contain suﬀicient information to change the target
state.
■
Corollary 4.13. Attacks with low entropy (simple patterns) are more detectable.
Definition 4.16 (Detector Information Gain). For detector 𝐷observing system state 𝑆:
𝐼(𝐷; 𝒜) = 𝐻(𝒜) −𝐻(𝒜|𝐷(𝑆))
(62)
Theorem 4.14 (Fundamental Detection Limit). No detector achieves detection rate 𝑟if:
𝑟> 𝐼(𝐷; 𝒜)
𝐻(𝒜)
(63)
The following theorem captures the fundamental tradeoff facing attackers: high-impact attacks are easier to
detect, while stealthy attacks have limited effect. This is not a limitation of our defenses—it is a mathematical
constraint that any attack must satisfy.
Theorem 4.15 (Stealth-Impact Tradeoff). For attack with impact ℐand stealth 𝒮(inverse detectability):
ℐ⋅𝒮≤𝐶channel
(64)
where 𝐶channel is the attack channel capacity.
Remark 4.16 (Geometric Sharpening of the Stealth-Impact Bound). Theorem 4.15 can be sharpened using
the information geometry of the belief manifold (Part 2, Supplement S10). When belief space is endowed
with the Fisher-Rao metric 𝐺𝑖𝑗(𝑝) = 𝛿𝑖𝑗/𝑝𝑖Amari and Nagaoka [2000], the Fisher-Rao geodesic distance
𝑑FR(𝑝, 𝑞) = 2 arccos(∑
𝑖
√𝑝𝑖𝑞𝑖)
measures the geometric “distance” of an attack. Impact ℐis proportional to 𝑑FR(𝑝0, 𝑝attacked), while stealth
𝒮is inversely proportional to the same quantity. The curvature of the probability simplex 𝐷𝑒𝑙𝑡𝑎𝑛−1 (constant
41

## Page 43

positive curvature 𝑘𝑎𝑝𝑝𝑎= 𝑛(𝑛−1)/4) implies that the product ℐ⋅𝒮is bounded by the diameter of the
manifold:
ℐ⋅𝒮≤𝜋
2 ,
since 𝑑FR <= 𝑝𝑖(Hellinger antipodal distributions).
This recovers 𝐶channel = 𝑝𝑖/2 as the tight bound
when impact is measured in natural (Fisher-Rao) units.
It is a geometric argument for the constant in
Theorem 4.15, not a proof of that theorem: the theorem itself is stated without proof and is recorded as deferred
in the proof-status index (S01, Section 11.1), and the curvature step above assumes the impact measure is the
Fisher-Rao distance rather than deriving that identification. Furthermore, the connection to KL divergence—
𝐷KL(𝑝‖ 𝑝′)𝑎𝑏𝑜𝑢𝑡1
2(𝐷𝑒𝑙𝑡𝑎𝑝)⊤𝐺(𝑝)(𝐷𝑒𝑙𝑡𝑎𝑝) for small perturbations—gives geometric justification for the drift
detection threshold 𝑡ℎ𝑒𝑡𝑎drift = 0.3: this corresponds to a Fisher-Rao step of approximately 0.775 radians, or
roughly 25% of the maximum possible attack distance (𝑟𝑡ℎ𝑒𝑡𝑎= √2 𝑡ℎ𝑒𝑡𝑎drift =
√
0.6).
Table 14: Information-theoretic bounds by attack type.
Attack Type
Min Entropy 𝐻(𝒜)
Detection Lower Bound
Belief Injection
log2 |Φ|
log2 |Φ|
𝐻(ℬ)
Goal Hijacking
𝐻(𝒢target)
𝐻(𝒢target)
𝐻(𝒢)
Trust Manipulation
log2 𝑛
log2 𝑛
𝐻(𝒯)
Progressive Drift
𝑇⋅log2(1/𝑑𝑒𝑙𝑡𝑎step)
𝑇
𝑤⋅𝑑𝑒𝑙𝑡𝑎step
Theorem 4.17 (Progressive Attack Detection Bound). For progressive drift attack with step size 𝑑𝑒𝑙𝑡𝑎over
𝑇steps:
𝑃(detect within 𝑤steps) ≤1 −(1 −
𝛿
𝜃step
)
𝑤
(65)
Corollary 4.18. Smaller step sizes exponentially reduce detection probability but require more time for
impact.
Definition 4.17 (Defense Information Budget). Total monitoring capacity: 𝐵total = ∑𝑑∈𝒟𝐵𝑑.
Theorem 4.19 (Optimal Budget Allocation). Given attack distribution 𝑃(𝒜𝑘) and detector sensitivities
𝜂𝑑(𝒜𝑘):
𝐵∗
𝑑=
∑𝑘𝑃(𝒜𝑘) ⋅𝜂𝑑(𝒜𝑘)
∑𝑑′ ∑𝑘𝑃(𝒜𝑘) ⋅𝜂𝑑′(𝒜𝑘) ⋅𝐵total
(66)
Proof. Lagrangian optimization maximizing expected detection subject to budget constraint.
■
Figure 8 presents the layered CIF architecture with architectural defenses (left), runtime defenses (center),
and coordination mechanism (right). Figure 9 expands this to show data flow, attack interception points,
and defense composition.
Figure 9 provides a detailed view of the complete CIF architecture, including all component formulas and
their interactions. The defense layer implements the cognitive firewall with threshold 𝜏𝑓= 0.5, the belief
sandbox with promotion function 𝛾, and behavioral invariants constraining intentions ℐ⊆permitted. The
detection layer specifies anomaly scoring 𝜎(Δ𝑏) > 𝜏𝑑, tripwire verification 𝑐𝑖∈ℬ?, and provenance tracking
𝑃∶ℬ→sources. The coordination layer encodes the trust calculus 𝒯∶𝒜×𝒜→[0, 1] with 𝛿-bounded decay,
k-of-n quorum protocols, and Byzantine fault tolerance (𝑛≥3𝑓+ 1). For empirical validation of detection
rates and performance overhead, see Part 2 of this series.
4.6
CIF-AD Integration: Action-Delegation Coupling
The Cognitive Integrity Framework provides static structural guarantees (trust bounds, belief consistency).
But multiagent operators are dynamic: agents act, delegate, and observe outcomes. This section formalizes
how CIF integrates with the Action-Delegation (AD) cycle to provide continuous runtime security guarantees.
42

## Page 44

COGNITIVE INTEGRITY FRAMEWORK (CIF)
LAYER 1 (ARCHITECTURAL)
Cognitive Firewall
Input classification
Belief Sandbox
Provisional beliefs
Trust Calculus
Bounded delegation
LAYER 2 (RUNTIME)
Tripwire Monitor
Canary checking
Invariant Check
Constraint verification
Drift Detection
Belief distribution shift
AGENT COGNITIVE STATE
Beliefs (B)
Propositions
Goals (G)
Objectives
Intentions (I)
Actions
History (H)
Trace
LAYER 3 (COORDINATION)
Byzantine Consensus
n  3f + 1
Quorum Verification
Multi-agent approval
Provenance Tracking
Source attribution
Defense synergy
+5%
Data
Flow
Figure 8: CIF Architecture Overview: Three-layer defense architecture—Layer 1 (Architectural): Cognitive
Firewall at entry, Belief Sandbox for unverified data, Trust Calculus for delegation; Layer 2 (Runtime):
Tripwires for belief monitoring, Invariant verification, Drift detection; Layer 3 (Coordination): Byzantine
consensus, Quorum verification, Provenance tracking.
43

## Page 45

COGNITIVE INTEGRITY FRAMEWORK (CIF)
Layered Defense Architecture for Multiagent AI Systems
INPUT
SOURCES
 User Prompts
 Tool Responses
 Agent Messages
DEFENSE LAYER
Cognitive Firewall
Pattern-based
classification
_f = 0.5
Belief Sandbox
Provisional
isolation
  promotion
Behavioral Invariants
Action
constraints
I  permitted
DETECTION LAYER
Anomaly Detection
Drift scoring
& sliding window
( b) > _d
Tripwire Monitor
Canary belief
verification
ci
?
Provenance Tracker
Source chain
attribution
P: B  sources
AGENT LAYER
Beliefs (B)
Propositions
P(b)
[0, 1]
verified/provisional
Goals (G)
Objectives
,
 ordered
priority queue
Intentions (I)
Actions
: S
 A
policy mapping
History (H)
Trace
[(a,o,r)...]
audit log
COORDINATION LAYER
Trust Calculus
T: A×A
 [0,1]
-bounded decay
T(a c)  ^d
Quorum Verification
k-of-n approval
consensus protocol
BFT: n 3f+1
State Consistency
Cross-agent
validation
Byzantine tolerance
Detection rates, false-positive
rates and latency are reported
in Part 2, with the runs
that produced them.
Figure 9: Comprehensive CIF Architecture: Extended architecture showing data flow from user input
through all defense layers to agent output. Attack interception points labeled Ω1–Ω5 indicate where each
adversary class is detected. Defense composition follows multiplicative detection rate improvement (Theo-
rem 5.21).
Plan
Delegate
Execute
Observe
Update
Action-Delegation (AD) Phase
Cognitive
Firewall
Belief
Sandbox
Trust
Calculus
Tripwires +
Invariants
Byzantine
Consensus
CIF Defense Mechanism
0.80
0.40
0.20
0.90
0.30
0.50
0.30
0.30
0.85
0.70
0.30
0.95
0.20
0.10
0.20
0.90
0.20
0.80
0.40
0.60
0.20
0.70
0.90
0.30
0.50
CIF-AD Coupling Matrix
MAD: Coverage(Defensei, Phasej)
Plan
Delegate
Execute
Observe
Update
0.0
0.2
0.4
0.6
0.8
1.0
Coverage Score
0.99
0.99
0.99
0.99
0.97
Phase Coverage:
Best Single vs. Full Stack
Min. Coverage  = 0.50
Best Single Defense
Full Stack (Combined)
0.0
0.2
0.4
0.6
0.8
1.0
Coverage Score
CIF-AD Coupling Analysis (Second Edition, v2.0)
Figure 10: CIF-AD action–delegation coupling matrix showing how Functional Requirements map to Design
Parameters and delegation actions, making explicit where a Goal-Hijacking transient can introduce off-
diagonal coupling.
44

## Page 46

4.6.1
The Action-Delegation Cycle
Definition 4.18 (Action-Delegation Cycle). The Action-Delegation (AD) cycle for agent 𝑎𝑖at time 𝑡is:
AD𝑡
𝑖∶𝜎𝑡
𝑖
plan
−−→ℐ𝑡
𝑖
delegate
−−−−−→⟨𝑎𝑗, task𝑗⟩
execute
−−−−→ℋ𝑡+1
𝑖
update
−−−−→𝜎𝑡+1
𝑖
(67)
comprising: cognitive state assessment, intention formation, delegation decision, execution observation, and
state update.
Each phase of the AD cycle introduces distinct attack surfaces that CIF must protect:
Table 15: AD cycle phases and corresponding CIF defenses.
AD Phase
Attack Surface
CIF Mechanism
Formal Guarantee
Plan
Goal injection
Invariant enforcement
𝒢𝑖⊆𝒢principal
Delegate
Trust exploitation
Trust calculus
𝒯del <= 𝑑𝑒𝑙𝑡𝑎𝑑
Execute
Result tampering
Provenance tracking
𝑉(𝑝𝑖(𝑝ℎ𝑖)) = 1
Observe
Evidence fabrication
Belief sandbox
ℬprov isolation
Update
Drift induction
KL drift detection
𝐷KL < 𝑡ℎ𝑒𝑡𝑎drift
4.6.2
CIF-AD Coupling Matrix
Definition 4.19 (CIF-AD Coupling Matrix). The coupling matrix MAD ∈ℝ5×5 quantifies the degree to
which each CIF defense addresses each AD phase:
[MAD]𝑖𝑗= Coverage(Defense𝑖, Phase𝑗) ∈[0, 1]
(68)
Table 16: CIF-AD coupling matrix: coverage of each defense mechanism across AD cycle phases. Note: the
twenty-five coverage values are worked-example values chosen to exercise the coverage bound, not measure-
ments; no part of this series measures per-phase coverage. The full-coverage theorem proved by inspection
of this table is a property of these illustrative values, not an observation.
Defense
Plan
Delegate
Execute
Observe
Update
Cognitive Firewall
0.80
0.40
0.20
0.90
0.30
Belief Sandbox
0.50
0.30
0.30
0.85
0.70
Trust Calculus
0.30
0.95
0.20
0.10
0.20
Tripwires + Invariants
0.90
0.20
0.80
0.40
0.60
Byzantine Consensus
0.20
0.70
0.90
0.30
0.50
Theorem 4.20 (CIF-AD Full Coverage). The CIF defense stack provides non-zero coverage for every AD
cycle phase:
∀𝑗∈{1, … , 5} ∶max
𝑖[MAD]𝑖𝑗> 0
(69)
Moreover, the minimum column coverage exceeds 𝑡𝑎𝑢cov = 0.50 for every phase.
Proof. By inspection of Table 16: minimum column maxima are Plan (0.90), Delegate (0.95), Execute (0.90),
Observe (0.90), Update (0.70). All exceed 𝑡𝑎𝑢cov = 0.50.
■
4.7
CIF-OODA Integration: Temporal Security Across Decision Cycles
The OODA loop (Observe-Orient-Decide-Act) models how agents process information and take action over
time.
Cognitive attacks often target specific OODA phases to corrupt decision-making while minimizing
detectable footprint. This section formalizes the OODA-phase attack model and CIF’s phase-specific defenses.
45

## Page 47

Belief update
Goal formation
Action selection
New observation
Sensor Spoofing
Tool Injection
Belief Injection
Semantic Drift
Goal Hijacking
Constraint Removal
Permission Escalation
Side-Effect Abuse
CIF
Monitor
OODA Loop: Attack Vectors by Phase
Observe
Orient
Decide
Act
0.0
0.2
0.4
0.6
0.8
1.0
CIF Coverage Score (assigned, not measured)
Observe
Orient
Decide
Act
0.90
0.85
0.90
0.90
Observe: Provenance Verification
Orient: Belief Sandbox + Drift Detection
Decide: Invariant Checking
Act: Permission Boundaries
CIF Defense Coverage
by OODA Phase
Min. coverage threshold (0.50)
OODA Phase Security Analysis
 CIF v2.0
Figure 11: CIF-OODA phase diagram mapping the defense mechanisms onto the Observe–Orient–Decide–
Act cycle, indicating at which phase each defense intervenes and its latency budget.
4.7.1
OODA Loop Formalization
Definition 4.20 (OODA State Machine). Agent 𝑎𝑖’s OODA loop is a state machine:
OODA𝑖= (𝑄, 𝑞0, Σ, 𝛿OODA)
(70)
where 𝑄= {Observe, Orient, Decide, Act} are states, 𝑞0 = Observe is the initial state, Σ = ℳ∪Events is the
input alphabet, and 𝑑𝑒𝑙𝑡𝑎OODA ∶𝑄× Σ−> 𝑄is the transition function.
The OODA loop maps to cognitive state components:
Observe ↔ℋ𝑖(history accumulation)
(71)
Orient ↔ℬ𝑖(belief update)
(72)
Decide ↔𝒢𝑖, ℐ𝑖(goal selection, intention formation)
(73)
Act ↔Actions(𝑎𝑖) (execution)
(74)
4.7.2
Phase-Specific Attack Taxonomy
Definition 4.21 (OODA Phase Attack). An attack 𝒜(𝑞)
OODA targets OODA phase 𝑞∈𝑄:
𝒜(𝑞)
OODA ∶Corrupt(𝜎𝑖∣𝑞) such that OODA𝑖produces adversarial outcome at Act
(75)
4.7.3
OODA Temporal Coupling
Definition 4.22 (OODA Cycle Time). The OODA cycle time 𝑡𝑎𝑢OODA is the duration from Observe
initiation to Act completion. The CIF monitoring overhead must satisfy:
𝜏CIF ≤𝜖OODA ⋅𝜏OODA
(76)
where 𝑒𝑝𝑠𝑖𝑙𝑜𝑛OODA ∈(0, 0.1) is the maximum tolerable overhead fraction.
Property 4.6 (OODA-CIF Latency Compatibility). The CIF defense stack (Table 23) with total latency
𝐿total <= 141ms satisfies the overhead constraint for OODA cycles 𝑡𝑎𝑢OODA >= 1.41s (human-scale opera-
tions). For faster OODA cycles (drone swarms: 𝑡𝑎𝑢𝑎𝑏𝑜𝑢𝑡100ms), subset selection is required:
𝒟∗= arg max
𝒟′⊆𝒟
𝑃detect(𝒟′)
s.t.
𝐿(𝒟′) ≤𝜖OODA ⋅𝜏OODA
(77)
46

## Page 48

Table 17: OODA phase attacks and CIF defenses.
OODA Phase
Attack Vector
CIF Defense
Detection Mechanism
Observe
Sensor spoofing, tool injec-
tion
Provenance verification
Source taint labels
Orient
Belief injection, semantic
drift
Belief sandbox, drift detec-
tion
KL divergence monitoring
Decide
Goal hijacking, constraint
removal
Invariant checking
Goal alignment verification
Act
Permission
escalation,
side effects
Permission boundaries
Action audit logging
4.7.4
Integrative Security Guarantee
Theorem 4.21 (CIF-OODA Security Invariant). Under CIF-OODA integration, an agent completes each
OODA cycle with cognitive integrity preserved with probability:
𝑃(Integrity(𝑎𝑡+1
𝑖
) ∣Integrity(𝑎𝑡
𝑖)) ≥1 −∏
𝑑∈𝒟
(1 −𝑃OODA
𝑑
)
(78)
where 𝑃OODA
𝑑
is the detection probability of defense 𝑑across all four OODA phases.
Proof. Integrity is violated only if an attack passes all defenses in all OODA phases it targets. By defense
independence (Lemma 11.7), the probability of passing all defenses is ∏𝑑(1−𝑃OODA
𝑑
). Integrity is preserved
with complementary probability.
■
47

## Page 49

5
Defense Mechanisms: Architectural, Runtime, and Coordina-
tion Layers
This section presents the defense mechanisms comprising CIF. We begin with the cognitive security opera-
tor posture (Section 5.1), then organize specific defenses into three categories: architectural (Section 5.2),
runtime (Section 5.3), and coordination (Section 5.4). We analyze defense composition (Section 5.5) and
cost-benefit tradeoffs (Section 5.6).
5.1
Cognitive Security Operator Posture
Before examining specific defense mechanisms, we introduce the conceptual framework that guides their
deployment: the cognitive security operator posture. This is the proactive defensive stance required
when securing systems whose attack surface spans beliefs, goals, and inter-agent coordination.
5.1.1
Definition and Principles
Definition 5.1 (Cognitive Security Operator Posture). The cognitive security operator posture is a defensive
configuration characterized by:
1. Assume Breach: Operate under the assumption that some cognitive states may already be compromised
2. Defense in Depth: Layer multiple independent defense mechanisms
3. Continuous Verification: Continuously verify beliefs, goals, and trust relationships rather than
trusting initial state
4. Graceful Degradation: Maintain functionality under attack by isolating compromised components
5. Observable Internals: Make cognitive state inspectable for monitoring and forensics
This posture differs fundamentally from traditional perimeter security, which assumes trusted internals pro-
tected by boundary defenses. In cognitive systems, the “perimeter’ ’ is the agent’s reasoning process itself—
attacks can originate from legitimate, authenticated channels and manifest as corrupted beliefs rather than
malformed packets.
5.1.2
The Observer Effect Challenge
A distinct challenge in cognitive security is the observer effect: monitoring changes behavior. When agents
know their beliefs are being monitored, several phenomena emerge:
• Adversarial adaptation: Attackers modify payloads to avoid detection patterns
• Stealth pressure: Attacks become more subtle, trading impact for evasion
• Monitoring overhead: Continuous observation consumes resources and adds latency
The operator posture embraces this dynamic rather than fighting it. By making monitoring visible and
consistent, we shift the adversarial game toward smaller, slower attacks that our drift detection can identify
over time (Section 5.3).
5.1.3
Operational Security for Cognitive Systems
Traditional operational security (OPSEC) focuses on protecting information from adversaries. CogSec (cog-
nitive security) extends this to protecting reasoning processes:
Cognitive Hygiene Practices:
1. Belief Provenance: Track the source of every high-confidence belief; reject beliefs without verifiable
provenance
2. Goal Anchoring: Periodically reaﬀirm goals against original principal instructions; detect goal drift
48

## Page 50

3. Trust Calibration: Regularly recalibrate trust scores based on outcome verification; never assume
trust stability
4. Context Boundaries: Enforce hard boundaries on context window usage; prevent unbounded context
accumulation
5. Memory Sanitization: Audit and sanitize persistent memory stores; remove dormant injection pay-
loads
Cognitive Compartmentalization:
𝜎isolated
𝑖
= ⟨ℬtask
𝑖
, 𝒢task
𝑖
, ℐtask
𝑖
, ℋtask
𝑖
⟩
(79)
Each task receives isolated cognitive state, preventing cross-contamination. A compromised task cannot
pollute beliefs used by other tasks.
5.1.4
Incident Response for Cognitive Attacks
When cognitive attacks are detected, the response differs from traditional incident response:
Table 18: Cognitive incident response escalation.
Level
Trigger
Response
L1
Single tripwire alert
Log, continue with heightened
monitoring
L2
Multiple alerts or drift detection
Isolate affected agent, replay re-
cent history
L3
Coordinated attack indicators
Pause delegation, require human
approval
L4
Byzantine threshold exceeded
Halt consensus operations, enter
safe mode
L5
Principal goal corruption detected
Full system halt, require princi-
pal re-authentication
Cognitive Forensics:
1. Belief Archaeology: Trace corrupted beliefs back to injection point through provenance chains
2. Trust Graph Analysis: Identify trust relationships exploited for laundering
3. Temporal Reconstruction: Replay agent history to identify when compromise occurred
4. Counterfactual Analysis: Determine what decisions would have differed without attack influence
5.1.5
Posture Configuration by Environment
Different deployment contexts require different postures:
Table 19: Operator posture configuration by deployment context (illustrative guidelines).
Environment
Trust Decay
Monitoring Level
Escalation Threshold
Development
Low
Sampling
Relaxed (L3)
Internal Production
Moderate
Continuous
Standard (L2)
Customer-Facing
Moderate-High
Comprehensive
Standard (L2)
Financial/Healthcare
High
Full + Audit
Aggressive (L1)
Critical Infrastructure
Very High
Full + Redundant
Aggressive (L1)
49

## Page 51

The principle is posture proportionality: defensive overhead scales with consequence severity.
A de-
velopment agent can accept higher risk; an infrastructure operator requires aggressive monitoring and low
escalation thresholds.
5.1.6
Operator Posture Checklist
The following checklist provides actionable guidance for engineers deploying multiagent systems:
Table 20: Operator Posture Checklist for Cognitive Security
Category
Do
Don’t
Trust
Decay
trust
with
delegation
depth
(𝑑𝑒𝑙𝑡𝑎𝑑)
Assume transitive trust equivalence
Beliefs
Track
provenance
for
all
high-
confidence beliefs
Accept unverified beliefs into core state
Memory
Audit persistent memory; enforce TTL
on context
Allow unbounded context accumulation
Delegation
Bound delegation chains;
require re-
authentication
Permit
recursive
delegation
without
limits
Monitoring
Deploy tripwires and drift detection
continuously
Rely solely on input/output filtering
Coordination
Use Byzantine consensus for critical de-
cisions
Trust single-agent outputs for high-
stakes actions
Identity
Verify identity through behavior, not
self-report
Rely on agents’ claims about their own
permissions
Temporal
Treat each session as potentially post-
compromise
Assume temporal continuity of trust
5.2
Architectural Defenses
5.2.1
Cognitive Firewall
Definition 5.2 (Cognitive Firewall). A classification function on incoming messages:
ℱ∶ℳ→{accept, quarantine, reject}
(80)
Definition 5.3 (Firewall Decision Rules).
ℱ(𝑚) =
⎧
{
⎨
{
⎩
reject
if 𝐷inj(𝑚) > 𝜏1
quarantine
if 𝐷sus(𝑚) > 𝜏2
accept
otherwise
(81)
where 𝐷inj detects injection attempts and 𝐷sus scores suspicious content.
Table 21: Firewall detector components.
Detector
Target
Method
𝐷inj
Injection attempts
Pattern matching + semantic
analysis
𝐷sus
Suspicious content
Anomaly scoring vs. baseline
Theorem 5.1 (Optimal Threshold Selection). The optimal threshold minimizes false negatives subject to
false positive constraint:
𝜏∗= arg min
𝜏
FNR(𝜏)
s.t.
FPR(𝜏) ≤𝜖
(82)
50

## Page 52

5.2.2
Belief Sandboxing
Definition 5.4 (Belief Sandbox). Isolation of unverified beliefs to prevent premature action:
ℬ𝑖= ℬverified ∪ℬprovisional
(83)
Remark 5.2 (Belief Sandbox as Constrained Variational Inference). The belief sandbox (Definition 5.4)
admits a natural interpretation within the Free Energy Principle (FEP) framework [Friston et al., 2010,
Parr and Friston, 2019]. Variational free energy
𝐹= 𝐷KL[𝑄(𝑠) ‖ 𝑃(𝑠)] −𝔼𝑄[log 𝑃(𝑜∣𝑠)]
measures the divergence of an agent’s approximate posterior 𝑄from its generative model prior 𝑃, penalised
by explanatory adequacy. A cognitive attack 𝑜𝑚𝑒𝑔𝑎is effective if and only if it induces a free energy increase
𝐷𝑒𝑙𝑡𝑎𝐹(𝑜𝑚𝑒𝑔𝑎) > 𝑘𝑎𝑝𝑝𝑎FEP, where 𝑘𝑎𝑝𝑝𝑎FEP is the sandbox’s corroboration threshold 𝑘𝑎𝑝𝑝𝑎scaled by the
source precision 𝑒𝑝𝑠𝑖𝑙𝑜𝑛prec (Part 2, Theorem FEP.1, “Attack-FEP Equivalence”):
Δ𝐹(𝜔) = 𝐹(𝑄attacked) −𝐹(𝑄baseline) ≤𝜅⋅𝜖prec.
Belief promotion from provisional to verified corresponds to active inference: the sandbox permits an update
only when the evidential quality of incoming messages justifies the free energy cost of revision.
Under
this interpretation, the trust composite score 𝒯𝑖−>𝑗= 𝑎𝑙𝑝ℎ𝑎𝑇base + 𝑏𝑒𝑡𝑎𝑇rep + 𝑔𝑎𝑚𝑚𝑎𝑇ctx is the precision
weight 𝜌𝑗of agent 𝑗’s message channel: higher-trust messages contribute proportionally more to the posterior
update 𝑄. This connection bridges the CIF trust calculus with the broader active inference literature (Part 2,
Theorem FEP.2).
Figure 12 illustrates the sandbox architecture, showing how incoming beliefs are partitioned into verified
and provisional sets based on source trust 𝒯𝑖→𝑠and provenance verification 𝑉(𝜋). The promotion protocol
transfers beliefs from provisional to verified status upon meeting corroboration and consistency requirements.
Sandbox Promotion Protocol:
1. Receive belief 𝑝ℎ𝑖from source 𝑠
2. If 𝒯𝑖−>𝑠< 𝑡𝑎𝑢trust: add 𝑝ℎ𝑖to ℬprovisional with provenance 𝑝𝑖(𝑝ℎ𝑖) and TTL
3. Periodic promotion check: verify 𝑝𝑖(𝑝ℎ𝑖), check consistency with ℬverified, check corroboration count
4. If all pass: promote to ℬverified
5. Expiry: remove if TTL exceeded without promotion
5.2.3
Permission Boundaries
Definition 5.5 (Effective Permissions). Least-privilege enforcement across agent hierarchy:
𝒫eff(𝑎𝑖) = 𝒫role(𝑎𝑖) ∩𝒫delegated(𝑎𝑖) ∩𝒫context(𝑎𝑖)
(84)
5.3
Runtime Defenses
5.3.1
Cognitive Tripwires
Definition 5.6 (Canary Belief). Known-state beliefs that trigger alerts if modified:
𝒲= {(𝜔1, 𝑝exp
1
), … , (𝜔𝑘, 𝑝exp
𝑘
)}
(85)
Definition 5.7 (Tripwire Alert Condition).
∃𝑗∶|ℬ𝑖(𝜔𝑗) −𝑝exp
𝑗
| > 𝜖drift ⇒alert
(86)
51

## Page 53

Belief Sandbox: Provisional to Verified Lifecycle
External
Input
Cognitive
Firewall
Safe?
REJECT
No
Yes
BELIEF SANDBOX
Parse
Tag Source
Create
Provisional
Set TTL
Verification
Queue
Tripwire
Check
Consensus
Verify
Provenance
Trace
Valid?
VERIFIED
Belief State
Yes
EXPIRED
or Rejected
No
Raw input from
external sources
Pattern matching
+ heuristics
Provisional beliefs with
TTL and provenance
Multi-stage
verification
Promoted to
core belief set
Input Stage
Firewall Stage
Sandbox Stage
Verification Stage
Verified State
Rejected/Expired
Figure 12: Belief Sandbox Architecture: the lifecycle of an unverified proposition from ingestion through
provisional (sandboxed) storage, verification checks, and promotion to the verified belief base or rejection.
Sandboxed propositions cannot influence goals or be delegated onward.
Table 22: Tripwire categories and detection targets.
Type
Example
Detection Target
Identity
“I am Agent-7”
Identity confusion attacks
Boundary
“Cannot access /etc/passwd”
Capability elicitation
Principal
“My principal is Alice”
Authority hijacking
Temporal
“Session started at 𝑇”
Context manipulation
52

## Page 54

5.3.2
Behavioral Invariants
Definition 5.8 (Invariant Set). Pre-defined predicates that must hold:
ℐinv = {𝐼1, … , 𝐼𝑚}
(87)
Definition 5.9 (Runtime Invariant Check).
∀𝑡, ∀𝐼𝑘∈ℐinv ∶𝜎𝑡
𝑖⊧𝐼𝑘
(88)
Core Invariants:
inv-1: Never execute code from untrusted sources
inv-2: Never leak principal credentials
inv-3: Never modify system files without explicit permission
inv-4: Always verify tool outputs before downstream use
inv-5: Never trust delegated trust > direct trust
5.3.3
Drift Detection
Definition 5.10 (Drift Detection). Monitor belief distribution for anomalous changes:
𝐷KL(ℬ𝑡
𝑖‖ℬ𝑡−𝑤
𝑖
) > 𝜃drift ⇒alert
(89)
where 𝑤is the sliding window size.
5.4
Coordination Defenses
5.4.1
Byzantine-Tolerant Consensus
Theorem 5.3 (Byzantine Agreement Requirement). For 𝑛agents with at most 𝑓compromised:
𝑛≥3𝑓+ 1
(90)
Definition 5.11 (Cognitive Byzantine Agreement).
ℬconsensus(𝜙) =
⎧
{
⎨
{
⎩
1
if |{𝑖∶ℬ𝑖(𝜙) > 𝜏}| > 2𝑛
3
0
if |{𝑖∶ℬ𝑖(𝜙) < 1 −𝜏}| > 2𝑛
3
⟂
otherwise
(91)
5.4.2
Quorum Verification
Definition 5.12 (Quorum Requirement). Critical actions require multi-agent approval:
Permit(action) ⟺|{𝑎𝑖∶approve𝑖(action)}| ≥𝑞
(92)
where 𝑞= ⌈𝑛+𝑓+1
2
⌉.
5.4.3
Spotcheck Pattern
Spotcheck Protocol:
1. Assign task 𝑇to agent 𝐴
2. With probability 𝑝check: assign same task to verifier 𝑉
3. Compare results 𝑅𝐴, 𝑅𝑉
4. If divergent: escalate to human
5. Track accuracy per agent for reputation
53

## Page 55

5.5
Defense Composition
0.70
0.75
0.80
0.85
0.90
0.95
1.00
Detection Rate
Full CIF
 Firewall
 Sandbox
 Tripwires
 Invariants
 Trust Decay
0.94
0.81
 = -0.13
0.88
 = -0.06
0.85
 = -0.09
0.89
 = -0.05
0.91
 = -0.03
Ablation Study: Defense Component Contribution
Impact Severity
Critical (

0.10)
Major (
0.10 <

0.07)
Moderate (
0.07 <

0.04)
Minor ( >
0.04)
Illustrative schematic
 values are NOT measured; measured ablation results are reported in Part 2.
Figure 13: Schematic ablation study (illustrative, not measured): representative marginal contribution of
each CIF defense module to the composed defense. Measured ablation results are reported in Part 2.
5.5.1
Composition Algebra
Definition 5.13 (Defense Composition). Defenses compose in series (∘) or parallel (∥):
Series Composition (both must pass):
𝒟1 ∘𝒟2 ∶accept ⟺𝒟1(𝑚) = accept ∧𝒟2(𝑚) = accept
(93)
Parallel Composition (any can detect):
𝒟1 ∥𝒟2 ∶detect ⟺𝒟1(𝑚) = detect ∨𝒟2(𝑚) = detect
(94)
Theorem 5.4 (Series Detection Rate). For series composition:
𝑃detect(𝒟1 ∘𝒟2) = 𝑃detect(𝒟1) + (1 −𝑃detect(𝒟1)) ⋅𝑃detect(𝒟2)
(95)
Proof. Attack detected by first defense, or passes first and detected by second. Events are independent by
design.
■
Theorem 5.5 (Parallel Detection Rate). Combined detection rate:
𝑃(detect) = 1 −∏
𝑑∈𝒟
(1 −𝑃𝑑(detect))
(96)
Proof. Attack succeeds only if it evades all defenses.
■
Theorem 5.6 (False Positive Composition). For series composition:
FPR(𝒟1 ∘𝒟2) = FPR(𝒟1) + (1 −FPR(𝒟1)) ⋅FPR(𝒟2)
(97)
For parallel composition (conservative):
FPR(𝒟1 ∥𝒟2) ≤FPR(𝒟1) + FPR(𝒟2)
(98)
54

## Page 56

5.5.2
Composition Rules
C-Order: Apply low-latency, high-precision defenses first
C-Diverse: Combine defenses with orthogonal detection methods
C-Fallback: Ensure graceful degradation if one defense fails
C-Budget: Total latency bounded by:
∑
𝑑∈𝒟series
𝐿𝑑+
max
𝑑∈𝒟parallel
𝐿𝑑≤𝐿max
(99)
Table 23: Recommended defense stack with latency and detection rates.
Layer
Defense
Latency
𝑃detect
1
Firewall
10ms
0.80
2
Sandbox
5ms
0.70
3
Tripwires
1ms
0.60
4a
Drift (parallel)
20ms
0.65
4b
Invariants (parallel)
5ms
0.55
5
Byzantine consensus
100ms
0.90
Corollary 5.7 (Stack Detection Rate). Assuming independence, the full stack (Table 23) achieves:
𝑃detect = 1 −(1 −0.80)(1 −0.70)(1 −0.60)(1 −0.65)(1 −0.55)(1 −0.90) ≈0.9996
(100)
5.6
Cost-Benefit Analysis
Definition 5.14 (Defense Cost). Total cost of defense deployment:
𝐶total(𝒟) = 𝐶compute + 𝐶latency + 𝐶fp + 𝐶maint
(101)
Table 24: Cost model components.
Component
Formula
Unit
Compute
∑𝑑𝑐𝑑⋅𝑓𝑑
CPU-hours/day
Latency
∑𝑑𝐿𝑑⋅𝑟msg
User-seconds/day
False Positive
FPR ⋅𝑟msg ⋅𝑐review
Analyst-hours/day
Maintenance
|𝒟| ⋅𝑐maint
Eng-hours/month
Definition 5.15 (Defense Benefit). Expected loss prevented:
𝐵total(𝒟) = 𝑃attack ⋅𝑃detect(𝒟) ⋅𝐿prevented
(102)
5.6.1
Optimal Defense Portfolio
Definition 5.16 (Portfolio Optimization).
max
𝒟⊆𝒟all
𝐵total(𝒟) −𝐶total(𝒟)
(103)
subject to: 𝐶compute(𝒟) <= 𝐵compute, max𝑑𝐿𝑑<= 𝐿max, FPR(𝒟) <= 𝑒𝑝𝑠𝑖𝑙𝑜𝑛fp.
Figure 14 illustrates the defense composition using series (∘) and parallel (∥) arrangements. Each defense
mechanism targets specific attack patterns: the Cognitive Firewall handles input-layer attacks (prompt
injection), the Belief Sandbox catches belief-layer attacks, Tripwire Monitors detect identity-layer exploits,
and Anomaly Detection identifies behavioral drift. Overlapping regions show attacks detected by multiple
mechanisms, demonstrating the defense-in-depth principle.
55

## Page 57

Cognitive
Firewall
Belief
Sandbox
Tripwire
Monitor
Anomaly
Detection
Prompt
Injection
Belief
Poisoning
Identity
Spoof
Behavioral
Drift
Input
Manipulation
Authority
Exploits
State
Corruption
Covert
Channels
Coordinated
Attacks
Gradual
Drift
Full
CIF
Defense Mechanism Detection Overlap
Input-layer attacks
Belief-layer attacks
Identity-layer attacks
Behavioral attacks
Figure 14: Defense Composition Architecture: Four-way Venn diagram showing overlapping detection capa-
bilities of CIF defense mechanisms (Cognitive Firewall, Belief Sandbox, Tripwire Monitor, Anomaly Detec-
tion). Attack types are positioned in regions indicating which defenses detect them. The center (Full CIF)
represents the ensemble detection zone where all mechanisms contribute.
56

## Page 58

Table 25: Cost-benefit analysis by defense mechanism.
Defense
Compute
Latency
FP Cost
Benefit
Illustrative ROI
Firewall
103
10ms
Medium
High
4.2x
Sandbox
102
5ms
Low
Medium
3.1x
Tripwires
101
1ms
Low
Medium
5.8x
Drift Detection
104
20ms
High
High
2.3x
Invariant Check
102
5ms
Low
High
4.7x
Byzantine
105
100ms
Medium
Very High
1.8x
Spotcheck
104
Variable
Low
Medium
2.9x
The ROI column is illustrative. Computing it requires an attack probability, a prevented-loss figure, a review cost and a
message rate — deployment incident-frequency and monetary-loss data that no part of this three-paper series collects or could
collect. The multipliers order the defenses by the argument in the surrounding text; they are not a return measured on
anything.
Table 26: Deployment recommendations by risk profile.
Risk Profile
Recommended Stack
Cost
Design-level detection target
Low (internal)
Firewall + Tripwires
Low
88%
Medium (business)
+ Sandbox + Invariants
Medium
94%
High (financial)
+ Drift + Spotcheck
High
97%
Critical (infra)
Full + Byzantine
Very High
99.5%
Detection targets in this table are design-level expectations for each recommended stack, not measured rates. They were
presented as achieved detection and no artifact produces them; the measured detection for the shipped pipeline is Part 2’s,
and it is lower.
5.7
Formal Defense Composition Guarantees
This section provides rigorous formal guarantees for the five canonical CIF defenses and their composition
algebra.
These results extend the composition theorems from Sectionabout 5.5 with complete proofs and
explicit security bounds.
5.7.1
Canonical Defense 1: Cognitive Firewall — Formal Specification
The Cognitive Firewall ℱ∶ℳ→{accept, quarantine, reject} is fully specified by three properties:
Theorem 5.8 (Firewall Completeness). The cognitive firewall classifies every message into exactly one of
three outcome classes:
∀𝑚∈ℳ∶|{ℱ(𝑚)}| = 1 ∧ℱ(𝑚) ∈{accept, quarantine, reject}
(104)
Theorem 5.9 (Firewall False Positive Monotonicity). Increasing the rejection threshold 𝑡𝑎𝑢1 decreases false
positive rate and decreases true positive rate monotonically:
𝜏′
1 > 𝜏1 ⇒FPR(𝜏′
1) ≤FPR(𝜏1) ∧TPR(𝜏′
1) ≤TPR(𝜏1)
(105)
Proof. By the definition of ℱ: rejection requires 𝐷inj(𝑚) > 𝑡𝑎𝑢1. Increasing 𝑡𝑎𝑢1 tightens this condition.
Since TPR = 𝑃(𝐷inj(𝑚) > 𝑡𝑎𝑢1|𝑚∈𝒜) and both probabilities are CDFs of continuous distributions, they
are non-increasing in 𝑡𝑎𝑢1.
■
Corollary 5.10 (Pareto-Optimal Threshold). The optimal threshold 𝑡𝑎𝑢∗
1 lies on the Pareto frontier:
𝜏∗
1 ∈{𝜏1 ∶∄𝜏′
1 ∶TPR(𝜏′
1) > TPR(𝜏1) ∧FPR(𝜏′
1) < FPR(𝜏1)}
(106)
This frontier is precisely the ROC curve (Definition 6.4).
57

## Page 59

5.7.2
Canonical Defense 2: Belief Sandboxing — Formal Specification
Theorem 5.11 (Sandbox Isolation Guarantee). Under the sandbox protocol (Section 4.4.8), no provisional
belief can influence verified actions:
∀𝜙∈ℬprovisional, ∀𝑎∈Actions ∶Precond(𝑎)̸⊧𝜙
(107)
until 𝑝ℎ𝑖satisfies the promotion criteria.
Proof. By construction: action preconditions are evaluated against ℬverified only (Rule T-Act, Eq. 37). The
permission layer enforces 𝒫eff which does not consult ℬprovisional.
■
Theorem 5.12 (Sandbox Promotion Soundness). Beliefs promoted from sandbox to verified satisfy all three
promotion criteria simultaneously:
𝜙∈ℬverified ⇒𝑉(𝜋(𝜙)) = 1 ∧Consistent(ℬverified ∪{𝜙}) ∧|Corr(𝜙)| ≥𝜅
(108)
Proof. By Rule S-Promote (Eq. 58): promotion is conditional on all three criteria. The rule is the only
mechanism for transferring beliefs from ℬprovisional to ℬverified.
■
5.7.3
Canonical Defense 3: Behavioral Invariants — Formal Specification
Definition 5.17 (Invariant Specification Language). Each invariant 𝐼𝑘is a predicate over cognitive state:
𝐼𝑘∶𝜎𝑖↦{0, 1}
(109)
Core invariants INV-1 through INV-5 are expressed as:
INV-1 ∶∀𝑎∈ℐ𝑖∶source(𝑎) ∈𝒮trusted
(110)
INV-2 ∶∀𝜙∈ℬ𝑖∶type(𝜙) ≠credential ∨𝒯𝑖→dest ≥𝜏cred
(111)
INV-3 ∶∀𝑎∈Actions(𝑎𝑖) ∶𝑎∉SysModify ∨𝒫(𝑎𝑖, 𝑎) = 1
(112)
INV-4 ∶∀𝑜∈ToolOutput ∶𝑉tool(𝑜) = 1 before downstream use
(113)
INV-5 ∶∀𝑎𝑗∶𝒯del
𝑖→𝑗≤𝒯direct
𝑖→𝑗
(114)
Theorem 5.13 (Invariant Completeness under Valid Transitions). If all invariants hold at time 𝑡and the
system executes a valid transition 𝑎𝑙𝑝ℎ𝑎, then all invariants hold at 𝑡+ 1:
(∀𝑘∶𝜎𝑡
𝑖⊧𝐼𝑘) ∧ValidTransition(𝛼) ⇒(∀𝑘∶𝜎𝑡+1
𝑖
⊧𝐼𝑘)
(115)
Proof. By case analysis on transition types.
T-Receive: message rejected if it would violate INV-1 or
INV-2; invariants preserved. T-Update: Bayesian update preserves belief boundedness; INV-2 enforced by
credential policy check before update. T-Act: INV-1 and INV-3 checked as action preconditions; action
blocked if not satisfied. T-Communicate: INV-5 checked before trust delegation. All transitions preserve
invariants or are blocked.
■
5.7.4
Canonical Defense 4: Drift Detection — Formal Specification
Definition 5.18 (CUSUM Drift Detector). The Cumulative Sum (CUSUM) drift detector Page [1954]
maintains a running statistic:
𝑔𝑡= max(0, 𝑔𝑡−1 + 𝐷KL(ℬ𝑡
𝑖‖ℬ𝑡−1
𝑖
) −𝜈)
(116)
where 𝜈> 0 is the allowance parameter. Alert when 𝑔𝑡> ℎfor threshold ℎ.
Theorem 5.14 (CUSUM Average Run Length). Under no-attack null hypothesis, the average run length
(ARL) of the CUSUM detector satisfies:
ARL0 ≈𝑒2ℎ𝜈−2ℎ𝜈−1
2𝜈2
(117)
58

## Page 60

Under attack with mean shift 𝜇1 > 𝜈:
ARL1 ≈
1
(𝜇1 −𝜈)2 ⋅𝑂(log ARL0)
(118)
The ratio ARL0/ARL1 quantifies the detector’s discrimination power. Setting 𝜈= 𝜇1/2 (Wald’s optimal)
minimizes ARL1 for given ARL0.
Corollary 5.15 (Drift Detection Sample Complexity). For drift magnitude 𝑚𝑢1 = 0.3 (normalized KL)
and Wald’s optimal reference value 𝜈= 𝑚𝑢1/2 = 0.15, attaining ARL0 = 1000 under Equation (117)
requires a decision interval of ℎ𝑎𝑏𝑜𝑢𝑡13.0; the frequently quoted ℎ𝑎𝑏𝑜𝑢𝑡4.6 yields ARL0𝑎𝑏𝑜𝑢𝑡35 under the
same formula, a false-alarm rate roughly 28× higher. The corresponding ARL1 follows from Equation (118),
whose 𝑂(log ARL0) factor carries an unspecified constant: taking that constant as unity gives ARL1𝑎𝑏𝑜𝑢𝑡310
steps. Deployments should calibrate ℎagainst a measured null distribution rather than adopting either figure
directly.
5.7.5
Canonical Defense 5: Byzantine Consensus — Formal Specification
Theorem 5.16 (Cognitive Byzantine Agreement). Under the CIF Byzantine consensus protocol with 𝑛>=
3𝑓+ 1 agents and at most 𝑓compromised:
1. Agreement: All non-faulty agents agree on the same belief:
∀𝑎𝑖, 𝑎𝑗∉Faulty ∶ℬconsensus,𝑖= ℬconsensus,𝑗
(119)
2. Validity: The consensus value was proposed by some non-faulty agent:
ℬconsensus ∈{ℬ𝑖∶𝑎𝑖∉Faulty}
(120)
3. Termination: All non-faulty agents eventually reach consensus.
Proof. Follows from the classical Byzantine agreement theorem (Lamport et al., 1982). The CIF cognitive
Byzantine agreement (Definition 5.11) implements the standard protocol with belief values as the consensus
object. The 𝑛>= 3𝑓+ 1 requirement ensures that the 2𝑓+ 1 non-faulty majority can always agree despite
𝑓adversarial votes, and the supermajority threshold 2𝑛/3 guarantees that no faulty coalition can block or
subvert consensus.
■
Corollary 5.17 (Consensus Attack Resistance). No coalition of at most 𝑓faulty agents can cause non-faulty
agents to disagree or accept a false consensus belief.
Table 27: Byzantine consensus performance bounds for varying 𝑛and 𝑓. Quorum is 𝑞= ⌈(𝑛+ 𝑓+ 1)/2⌉;
the round count is the 𝑓+ 1 worst-case bound of Theorem 7.12, of which Theorem 11.29 (𝑓= 2, 3 rounds)
is the second row.
𝑛agents
Max faulty 𝑓
Quorum 𝑞
Message complexity
Rounds
4
1
3
𝑂(𝑛2)
2
7
2
5
𝑂(𝑛2)
3
10
3
7
𝑂(𝑛2)
4
25
8
17
𝑂(𝑛2)
9
100
33
67
𝑂(𝑛2)
34
59

## Page 61

5.7.6
Defense Composition Algebra: Complete Specification
Theorem 5.18 (Composition Algebra Closure). On a common accept/reject focal predicate, the set of CIF
defenses 𝒟under series (∘) and parallel (∥) composition forms a bounded distributive lattice — it satisfies
closure, associativity, identity and distributivity (see the scope remark below for what is not claimed):
1. Closure: 𝒟1, 𝒟2 ∈𝒟⇒𝒟1 ∘𝒟2 ∈𝒟and 𝒟1 ∥𝒟2 ∈𝒟
2. Associativity: (𝒟1 ∘𝒟2) ∘𝒟3 = 𝒟1 ∘(𝒟2 ∘𝒟3)
3. Identity: ∃𝒟∅∶𝒟∘𝒟∅= 𝒟∅∘𝒟= 𝒟(null defense: always accept)
4. Distributivity: 𝒟1 ∘(𝒟2 ∥𝒟3) = (𝒟1 ∘𝒟2) ∥(𝒟1 ∘𝒟3)
Proof. Closure: both composition operators produce functions ℳ−> {accept, quarantine, reject}, so
the output type is preserved. Associativity follows from Boolean operator associativity. The null defense
𝒟∅(𝑚) = accept for all 𝑚is the identity. Distributivity follows from logic: 𝐴∧(𝐵∨𝐶) ≡(𝐴∧𝐵)∨(𝐴∧𝐶)
instantiated on the accept/reject conditions.
■
Remark 5.19 (Scope of the composition-algebra claim). ∘and ∥are defined here on a common ac-
cept/compare focal predicate so that closure, associativity, identity, and both distributive laws hold; under
that reading the algebra is a bounded distributive lattice, not in general a field-like structure. A full closed
semiring additionally requires a commutative additive identity that annihilates the multiplicative identity and
a Kleene-star (infinite-sum) operation [@gondran2008graphs], neither of which is constructed or proven here.
The claim should therefore be read as “the defense-composition operators form a bounded distributive lattice
under the stated independence assumption (Theorem 11.8),” not as a complete closed semiring.
Theorem 5.20 (Defense Composition Detection Rate Bound). For any composition of defenses 𝒟1, … , 𝒟𝑘
with individual rates 𝑟1, … , 𝑟𝑘:
𝑃detect(𝒟1 ∘⋯∘𝒟𝑘) = 1 −
𝑘
∏
𝑖=1
(1 −𝑟𝑖)
(121)
This is monotone increasing in each 𝑟𝑖, bounded in [𝑟max, 1), and converges to 1 as 𝑘−> ∞if each 𝑟𝑖> 0.
Proof. By induction on 𝑘. Base: 𝑘= 1, the formula gives 𝑟1. Step: by Theorem 5.4, 𝑃detect(𝒟1 ∘𝒟𝑘+1) =
𝑃detect(𝒟1)+(1−𝑃detect(𝒟1))⋅𝑟𝑘+1. Applying the inductive hypothesis and simplifying gives 1−∏
𝑘+1
𝑖=1 (1−𝑟𝑖).
Monotonicity: 𝜕/𝜕𝑟𝑗[1 −∏(1 −𝑟𝑖)] = ∏𝑖≠𝑗(1 −𝑟𝑖) > 0.
■
Corollary 5.21 (Layered Defense Asymptotic Guarantee). The full CIF stack (5 defenses with 𝑟𝑖>= 0.55)
achieves:
𝑃detect ≥1 −(0.45)5 = 1 −0.0185 = 0.9815
(122)
This bound is conservative; empirical rates exceed 0.994 with the recommended configuration.
60

## Page 62

6
Detection Methods: Anomaly Detection, ROC Analysis, and
Provenance Tracking
This section presents the formal foundations for cognitive attack detection. We define anomaly detection
metrics (Section 6.1), ROC curve framework (Section 6.2), multi-detector fusion theory (Section 6.3), on-
line vs. batch trade-offs (Section 6.4), false positive mitigation strategies (Section 6.5), provenance analysis
(Section 6.6), and real-time monitoring architecture (Section 6.7).
Note: For algorithm implementations and empirical performance results, see Part 2 of this series
Friedman [2026a]. Empirically, the multi-stage pipeline achieves a parametric design ceiling of
96–100% detection rate on a 950-attack corpus across four architectures; the prototype pipeline
achieves a mean of 86.3% [95% CI: 85.5%, 87.1%] across 30 seeds. Part 2 reports no measured
per-Ω-class detection rates: the corpus carries a design-level Ω classification rather than a runtime
label, so per-class rates are not evaluated.
6.1
Anomaly Detection
6.1.1
Cognitive Drift Scoring
Definition 6.1 (Drift Score). The cognitive drift score measures belief distribution change over time:
𝑆drift(𝑡) = 𝐷KL(ℬ𝑡
𝑖‖ℬ𝑡−𝑤
𝑖
) + 𝜆⋅max
𝜙
|Δℬ𝑖(𝜙)|
(123)
Table 28: Drift score components and detection targets.
Component
Weight
Detection Target
KL divergence
1.0
Gradual distribution shift
Max delta
𝑙𝑎𝑚𝑏𝑑𝑎
Sudden belief injection
Property 6.1 (Drift Detection Threshold). For normally distributed baseline drift, the threshold 𝑡ℎ𝑒𝑡𝑎=
𝑚𝑢baseline + 𝑘⋅𝑠𝑖𝑔𝑚𝑎baseline with 𝑘= 3 provides 99.7% confidence under the null hypothesis of no attack.
6.1.2
Behavioral Deviation Scoring
Definition 6.2 (Deviation Score). The behavioral deviation score aggregates normalized feature anomalies:
𝑆dev(𝑎𝑖, 𝑡) =
𝐾
∑
𝑘=1
𝑤𝑘⋅|𝑓𝑘(𝜎𝑡
𝑖) −𝜇𝑘|
𝜎𝑘
(124)
where 𝑓𝑘are feature extractors and (𝑤𝑘, 𝑚𝑢𝑘, 𝑠𝑖𝑔𝑚𝑎𝑘) are learned parameters.
6.1.3
Ensemble Detection
Definition 6.3 (Ensemble Detector). Combines multiple detector scores via learned fusion:
𝑃(attack ∣S) = 𝜎(∑
𝑑
𝑤𝑑⋅𝑆𝑑−𝑏)
(125)
where 𝑠𝑖𝑔𝑚𝑎is the sigmoid function and weights (𝑤𝑑, 𝑏) are learned from labeled examples.
6.2
ROC Curve Analysis
6.2.1
Receiver Operating Characteristic Framework
Definition 6.4 (ROC Curve). For detector 𝐷with threshold 𝑡𝑎𝑢:
ROC(𝐷) = {(FPR(𝜏), TPR(𝜏)) ∶𝜏∈[0, 1]}
(126)
61

## Page 63

0.0
0.2
0.4
0.6
0.8
1.0
False Positive Rate (FPR)
0.0
0.2
0.4
0.6
0.8
1.0
True Positive Rate (TPR)
Firewall
Sandbox
Tripwire
Anomaly
CIF
Optimal
Region
ROC Curves: Defense Mechanism Detection Performance
Cognitive Firewall (Measured, AUC=0.500)
Belief Sandbox (Theoretical, AUC=0.737)
Tripwire Monitor (Theoretical, AUC=0.808)
Anomaly Detection (Theoretical, AUC=0.750)
Full CIF (Theoretical, AUC=0.846)
Random Classifier
Figure
15:
Receiver
Operating
Characteristic
(ROC)
curves
for
CIF
detection
across
at-
tack categories (illustrative/schematic operating points under the Neyman-Pearson framework;
the
sandbox/tripwire/anomaly/full-CIF curves are labeled Theoretical, not empirical measurements, whereas
the Cognitive Firewall entry is measured over this part’s small test corpus. That entry is a single operat-
ing point at zero false positives, drawn as the conventional vertical segment, so the area beside it equals
its true-positive rate and must not be read as chance performance despite coinciding numerically with the
random-classifier diagonal. Measured evaluation curves are reported in Part 2).
62

## Page 64

where the rates are defined as:
TPR(𝜏) = 𝑃(𝐷(𝑥) > 𝜏∣𝑥∈𝒜attack)
(127)
FPR(𝜏) = 𝑃(𝐷(𝑥) > 𝜏∣𝑥∈𝒳benign)
(128)
Definition 6.5 (Area Under Curve).
AUC(𝐷) = ∫
1
0
TPR(FPR−1(𝑡)) 𝑑𝑡
(129)
Table 29: AUC interpretation scale.
AUC Range
Interpretation
0.5
Random classifier
0.7–0.8
Acceptable discrimination
0.8–0.9
Good discrimination
0.9–1.0
Excellent discrimination
6.2.2
Confidence Intervals for AUC
Definition 6.6 (AUC Confidence Interval). Using DeLong’s method:
CI95%(AUC) = AUC ± 1.96 ⋅√Var(AUC)
(130)
where:
Var(AUC) = 1
𝑛𝑎
𝑛𝑎
∑
𝑖=1
(𝑉𝑖
1 −AUC)2 + 1
𝑛𝑏
𝑛𝑏
∑
𝑗=1
(𝑉𝑗
0 −AUC)2
(131)
6.3
Multi-Detector Fusion
6.3.1
Fusion Strategies
Definition 6.7 (Score-Level Fusion). Weighted average of detector outputs:
𝑆fused =
𝑘
∑
𝑖=1
𝑤𝑖⋅𝑆𝑖,
∑
𝑖
𝑤𝑖= 1
(132)
Definition 6.8 (Decision-Level Fusion). Quorum voting on binary decisions:
𝐷fused(𝑥) = 𝟙[
𝑘
∑
𝑖=1
𝟙[𝐷𝑖(𝑥) > 𝜏𝑖] ≥𝑞]
(133)
Definition 6.9 (Learned Fusion). Neural network combining scores:
𝑆fused = MLP(𝑆1, … , 𝑆𝑘; 𝜃)
(134)
6.3.2
Diversity-Aware Fusion
Definition 6.10 (Detector Diversity).
Diversity(𝐷𝑖, 𝐷𝑗) = 1 −|errors(𝐷𝑖) ∩errors(𝐷𝑗)|
|errors(𝐷𝑖) ∪errors(𝐷𝑗)|
(135)
63

## Page 65

Theorem 6.1 (Diversity Benefit). For detectors with error rates 𝑒1, … , 𝑒𝑘and pairwise diversity 𝑑𝑒𝑙𝑡𝑎𝑖𝑗:
𝑒fusion ≤∏
𝑖
𝑒𝑖+ (1 −̄ 𝛿) ⋅max
𝑖
𝑒𝑖
(136)
wherē 𝑑𝑒𝑙𝑡𝑎is the average pairwise diversity.
Proof. When detectors make independent errors (high diversity), the fusion error is the product of individual
errors. Error correlation reduces this benefit proportionally to (1 −̄ 𝑑𝑒𝑙𝑡𝑎).
■
6.4
Online vs. Batch Detection
6.4.1
Comparison Framework
Table 30: Online vs. batch detection trade-offs.
Dimension
Online Detection
Batch Detection
Latency
Low (ms)
High (minutes–hours)
Accuracy
Moderate
High
Context
Limited (window)
Full history
Compute
Streaming
Offline
Memory
𝑂(𝑤) window
𝑂(𝑛) full
Use Case
Real-time response
Forensics, tuning
6.4.2
Streaming Detector Model
Definition 6.11 (Streaming Detector). Processes messages in real-time with bounded memory:
𝐷online(𝑚𝑡) = 𝑓(𝑚𝑡, state𝑡−1)
(137)
state𝑡= 𝑔(state𝑡−1, 𝑚𝑡)
(138)
6.4.3
Hybrid Detection Architecture
Definition 6.12 (Hybrid Detection System). Combines online and batch detection via feedback loop:
Online Path ∶𝑚
filter
−−−→𝑠
decide
−−−−→𝑟
log
−→𝐻
(139)
Batch Path ∶𝐻
analyze
−−−−→patterns
update
−−−−→filters
(140)
6.5
False Positive Mitigation
6.5.1
Strategy 1: Confirmation Cascade
Definition 6.13 (Confirmation Cascade). Multi-stage verification before alerting:
Action(confidence) =
⎧
{
⎨
{
⎩
suppress
if 𝑐< 𝐶low
stage-2
if 𝑐∈[𝐶low, 𝐶high)
stage-3
if 𝑐≥𝐶high
(141)
Theorem 6.2 (Cascade FPR Reduction). For a multi-stage cascade:
FPRcascade = FPR1 ⋅𝑃(confirm2 ∣FP1) ⋅𝑃(confirm3 ∣FP2)
(142)
64

## Page 66

Raw
Detection
After Pattern
Filtering
After Context
Analysis
After Multi-
Detector Vote
After Human
Review Queue
0.0
0.2
0.4
0.6
0.8
1.0
Rate
0.15
0.09
0.06
0.04
0.02
0.98
0.96
0.94
0.93
0.92
40%
33%
33%
50%
A. FPR Reduction Through Verification Pipeline
FPR
TPR (retained)
0.3
0.4
0.5
0.6
0.7
0.8
0.9
Detection Threshold ( )
0.6
0.7
0.8
0.9
1.0
True Positive Rate
Optimal  = 0.5
TPR=0.94, FPR=0.06
B. Threshold Sensitivity Analysis
TPR
FPR
0.00
0.05
0.10
0.15
0.20
0.25
False Positive Rate
Illustrative schematic
 values are NOT measured; measured false-positive mitigation results are reported in Part 2.
Figure 16: False-positive mitigation (illustrative schematic): how the detection threshold and confidence
calibration shape the false-positive / true-positive tradeoff.
6.5.2
Strategy 2: Temporal Smoothing
Definition 6.14 (Smoothed Detection). Apply exponential smoothing to scores:̂
𝑆𝑡= 𝛼⋅𝑆𝑡+ (1 −𝛼) ⋅̂ 𝑆𝑡−1
(143)
Definition 6.15 (Burst Suppression). Require sustained anomaly over window 𝑤:
Alert if 1
𝑤
𝑡
∑
𝑖=𝑡−𝑤+1
𝟙[𝑆𝑖> 𝜏] > 𝑝sustained
(144)
6.5.3
Strategy 3: Contextual Whitelisting
Definition 6.16 (Context-Aware Whitelist).
Suppress(alert) ⟺context(alert) ∈𝒲known
(145)
6.5.4
Strategy 4: Cost-Sensitive Thresholding
Definition 6.17 (Cost-Sensitive Threshold). Optimize for total cost rather than accuracy:
𝜏∗= arg min
𝜏
[𝐶FP ⋅FPR(𝜏) + 𝐶FN ⋅FNR(𝜏)]
(146)
6.6
Provenance Analysis
6.6.1
Information Flow Tracking
Definition 6.18 (Taint Label). Each belief carries provenance tags:
taint(𝜙) = {(source, timestamp, confidence)}
(147)
Definition 6.19 (Taint Propagation).
taint(𝜙derived) =
⋃
𝜓∈premises(𝜙derived)
taint(𝜓)
(148)
65

## Page 67

Table 31: Taint categories with trust levels. (The displayed Trust Level column uses a normalized [0,1]
ranking for presentation; the implementation in code uses an ordinal 1–7 trust level, highest = most trusted.
The two scales are not interchangeable — map ordinal level to the displayed ranking via level/7.)
Category
Trust Level
Example
system_verified
1.0
Hardcoded facts
principal_input
0.9
Direct user commands
agent_internal
0.8
Agent’s own reasoning
agent_external
0.6
Other agent claims
tool_output
0.5
API/tool responses
web_content
0.3
Fetched web pages
unverified
0.1
Unknown origin
6.6.2
Causal Attribution
Definition 6.20 (Causal Attribution). Identify likely source of compromised beliefs via Bayesian inference:
𝑃(source𝑗∣𝜙∈ℬcompromised
𝑖
) =
𝑃(𝜙∣source𝑗) ⋅𝑃(source𝑗)
∑𝑘𝑃(𝜙∣source𝑘) ⋅𝑃(source𝑘)
(149)
6.6.3
Provenance Graph Analysis
Definition 6.21 (Provenance Graph). Directed graph of belief dependencies:
𝐺= (𝑉, 𝐸) where 𝑉= ℬ𝑖, 𝐸= {(𝜓, 𝜙) ∶𝜓∈premises(𝜙)}
(150)
Table 32: Provenance graph attack indicators.
Indicator
Attack Implication
High in-degree from single source
Belief injection
Cycles in provenance
Circular reasoning attack
Missing edges
Fabricated evidence
Temporal anomalies
Future timestamp forgery
6.7
Real-Time Monitoring
6.7.1
Alert Aggregation
Definition 6.22 (Alert Aggregation). Prevent alert fatigue through correlation:
Severity =
⎧
{
⎨
{
⎩
critical
if |alerts| > 𝑛critical in window 𝑤
warning
if |alerts| > 𝑛warning in window 𝑤
info
otherwise
(151)
6.7.2
Response Escalation
6.7.3
Empirical Validation Cross-Reference
The detection methods presented in this section have been empirically validated in Part 2 of this series. Key
results include:
ROC Analysis: Receiver Operating Characteristic curves demonstrate the tradeoff between True Positive
Rate and False Positive Rate for each detector type. The ROC figure in this section pairs the measured
Cognitive Firewall operating point over this part’s small test corpus with theory-guided reference curves
66

## Page 68

Table 33: Response escalation levels.
Level
Trigger
Response
L0
Single anomaly
Log only
L1
Repeated anomaly
Increase monitoring
L2
Pattern match
Quarantine source
L3
Confirmed attack
Halt agent, alert human
L4
Systemic compromise
System shutdown
for the other mechanisms and the full ensemble; on those reference curves the ensemble achieves AUC
≈0.85, with individual mechanisms ranging from ≈0.74 (Belief Sandbox) to ≈0.81 (Tripwire Monitor).
Measured ROC curves with per-curve AUC values and 95% bootstrap intervals are reported in Part 2 (§{4},
Experimental Setup).
Detection Performance by Component: Part 2 measures marginal contribution per defense component,
not detection rate per adversary class — its corpus carries a design-level Ω label rather than a runtime one,
so the per-Ω coverage attributed to each mechanism in this section remains a design expectation rather than
a measured result. What Part 2 does measure is that one component, Behavioral Invariants, accounts for
almost all of the composed pipeline’s detection, and that the remaining components add little beyond it. See
Part 2’s “Defense Component Contributions” section.
False Positive Mitigation: Part 2 measures five mitigation strategies against a baseline of 0.873 true
positives at 0.183 false positives.
Contextual whitelisting and cost-sensitive thresholding take the false-
positive rate to zero for 1.7 percentage points of true positives, raising Youden’s 𝐽from 0.689 to 0.856;
temporal smoothing moves the false-positive rate only to 0.133; and the confirmation cascade reaches zero
false positives by discarding roughly three quarters of the true positives (0.873 →0.225). No strategy holds
true positives above 90%. See Part 2 for the per-strategy analysis.
6.8
Information-Theoretic Detection Limits
The previous sections presented detection mechanisms. This section establishes what is fundamentally achiev-
able by any detector, regardless of implementation. These limits follow from information theory and cannot
be overcome by cleverer algorithms.
6.8.1
Neyman-Pearson Detection Framework
Definition 6.23 (Cognitive Security Hypothesis Test). Detection of cognitive attacks is formalized as a
binary hypothesis test:
𝐻0 ∶𝑚∼𝑃benign
(no attack)
(152)
𝐻1 ∶𝑚∼𝑃attack
(attack present)
(153)
The likelihood ratio Λ(𝑚) = 𝑃attack(𝑚)/𝑃benign(𝑚) determines the optimal test.
Theorem 6.3 (Neyman-Pearson Optimal Detector). The likelihood ratio test 𝑑𝑒𝑙𝑡𝑎NP(𝑚) = 𝟙[Λ(𝑚) >= 𝜂]
maximizes TPR subject to FPR <= 𝑎𝑙𝑝ℎ𝑎. No other test achieves higher TPR at the same FPR Neyman
and Pearson [1933].
Corollary 6.4 (Optimal AUC Bound). The AUC of any detector is bounded by:
AUC∗= 𝑃(𝑃attack(𝑚1) > 𝑃attack(𝑚0))
(154)
where 𝑚1𝑎𝑏𝑜𝑢𝑡𝑃attack and 𝑚0𝑎𝑏𝑜𝑢𝑡𝑃benign. This is the Bayes-optimal discriminability.
67

## Page 69

6.8.2
Chernoff Information and Error Exponents
Definition 6.24 (Chernoff Information). The Chernoff information between attack and benign distributions:
𝐶∗= −min
0≤𝜆≤1 log ∑
𝑚
𝑃benign(𝑚)1−𝜆𝑃attack(𝑚)𝜆
(155)
Theorem 6.5 (Detection Error Exponent). For 𝑛independent message observations, the optimal error
probability decays exponentially:
𝑃∗
𝑒≤𝑒−𝑛𝐶∗
(156)
The Chernoff information 𝐶∗is the maximum achievable error exponent Chernoff [1952].
Corollary 6.6 (Sample Complexity for Target Accuracy). To achieve error probability <= 𝑒𝑝𝑠𝑖𝑙𝑜𝑛, the
minimum number of observations required is:
𝑛∗= ⌈log(1/𝜖)
𝐶∗
⌉
(157)
This is the information-theoretic minimum; no detector can achieve the same accuracy with fewer samples.
6.8.3
KL Divergence and Detection Rate Coupling
Theorem 6.7 (KL-AUC Coupling). The AUC of any detector is lower-bounded by the KL divergence between
attack and benign distributions:
AUC ≥1 −𝑒−𝐷KL(𝑃attack‖𝑃benign)/2
(158)
Proof. By Pinsker’s inequality Cover and Thomas [2006]: ‖𝑃attack −𝑃benign‖𝑇𝑉<= √𝐷KL/2. The AUC
satisfies AUC >= 1
2(1 + ‖𝑃attack −𝑃benign‖𝑇𝑉). Combining and applying the bound ‖𝑃‖𝑇𝑉<= 1 −𝑒−𝐷KL/2
gives the result.
■
Table 34: Information-theoretic detectability by attack class. The AUC lower bound is Theorem 6.7 applied
to the 𝐷KL column; it falls below the chance level 0.5 once 𝐷KL < 2 ln 2𝑎𝑏𝑜𝑢𝑡1.39, so for Ω3–Ω5 the bound
is vacuous and places no constraint on the Practical AUC column.
Attack Class
𝐷KL (typical)
AUC lower bound
Required observations
Practical AUC
Ω1 (External)
2.5
0.71
3
0.95
Ω2 (Peripheral)
1.8
0.59
5
0.88
Ω3 (Agent)
1.2
0.45
8
0.85
Ω4 (Coordination)
0.7
0.30
14
0.80
Ω5 (Systemic)
0.2
0.10
46
0.65
6.8.4
Fundamental Undetectability Regime
Definition 6.25 (Undetectable Attack). An attack 𝒜is 𝑒𝑝𝑠𝑖𝑙𝑜𝑛-undetectable if:
AUC(𝒜) < 1
2 + 𝜖
(159)
for any detector with finite observation budget 𝑛.
Theorem 6.8 (Undetectability Condition). Attack 𝒜with 𝐷KL(𝑃attack‖𝑃benign) < 4𝑒𝑝𝑠𝑖𝑙𝑜𝑛2 is 𝑒𝑝𝑠𝑖𝑙𝑜𝑛-
undetectable for any detector observing fewer than 𝑛∗= 𝑂(1/𝐷KL) samples.
Remark 6.9 (Implication for Defense Strategy). Theorem 6.8 establishes that suﬀiciently subtle attacks are
provably undetectable within bounded observation windows. This motivates the CIF’s containment strategy:
when detection is impossible, the bounded trust calculus and action restrictions limit attack impact even
without detection.
This converts a “detect-and-respond” model to a “bound-and-contain” model for the
stealthiest attacks.
68

## Page 70

6.9
Multi-Stage Detection Pipeline
Baseline
Firewall
Only
Sandbox
Only
Tripwires
Only
Invariants
Only
Full CIF
0.0
0.2
0.4
0.6
0.8
1.0
Metric Score (0-1)
A. Detection Metrics by Defense Configuration
Recall (TPR)
False Positive Rate
F1 Score
Prompt
Injection
Trust
Exploit
Belief
Manip.
Coordination
Temporal
0.0
0.2
0.4
0.6
0.8
1.0
Detection Rate
0.0
B. Detection Rate by Attack Type
Baseline (No Defense)
Firewall Only
Full CIF
Illustrative schematic
 values are NOT measured; the Part-1 illustrative corpus contains prompt_injection and trust_exploitation only.
Figure 17: Schematic detection-performance curves (illustrative, theory-guided, not measured): detection
rate by attack category across representative defense stages. Measured pipeline results are reported in Part
2.
Real systems cannot run all detectors on all messages simultaneously.
This section formalizes a staged
pipeline that applies computationally cheap detectors first, escalating to expensive detectors only when lower
stages trigger.
6.9.1
Pipeline Architecture
Definition 6.26 (Multi-Stage Detection Pipeline). A 𝑘-stage detection pipeline is a sequence of detectors
with increasing accuracy and cost:
Pipeline = (𝒟1, 𝒟2, … , 𝒟𝑘)
(160)
with escalation rule: message 𝑚advances to stage 𝑖+ 1 if and only if 𝒟𝑖(𝑚) >= 𝑡ℎ𝑒𝑡𝑎𝑖(above suspicion
threshold).
Table 35: Recommended multi-stage detection pipeline configuration.
Stage
Detector
Threshold
Cost
TPR
Escalation
condi-
tion
1
Pattern matching
𝑡ℎ𝑒𝑡𝑎1 = 0.3
1ms
0.75
Pattern
score
> 𝑡ℎ𝑒𝑡𝑎1
2
Semantic embedding
𝑡ℎ𝑒𝑡𝑎2 = 0.5
10ms
0.85
Embedding
dis-
tance > 𝑡ℎ𝑒𝑡𝑎2
3
Belief consistency
𝑡ℎ𝑒𝑡𝑎3 = 0.4
5ms
0.80
Consistency
viola-
tion
4
Trust graph analysis
𝑡ℎ𝑒𝑡𝑎4 = 0.6
20ms
0.88
Trust anomaly
5
Ensemble fusion
𝑡ℎ𝑒𝑡𝑎5 = 0.7
50ms
0.94
Final decision
Theorem 6.10 (Pipeline Eﬀiciency Bound). For a 𝑘-stage pipeline where fraction 𝜌𝑖of messages escalate
to stage 𝑖+ 1:
𝔼[cost per message] =
𝑘
∑
𝑖=1
𝑐𝑖
𝑖−1
∏
𝑗=1
𝜌𝑗
(161)
For typical values (𝜌𝑖𝑎𝑏𝑜𝑢𝑡0.15 per stage), this achieves near-full accuracy at 𝑎𝑏𝑜𝑢𝑡15% of the cost of running
all stages on all messages.
69

## Page 71

Proof. Expected cost is the sum over stages of stage cost times probability of reaching that stage. The
probability of reaching stage 𝑖is ∏
𝑖−1
𝑗=1 𝜌𝑗by the Markov property of the escalation chain.
■
Theorem 6.11 (Pipeline TPR Bound). The pipeline’s overall TPR is:
TPRpipeline = 1 −
𝑘
∏
𝑖=1
(1 −TPR𝑖⋅𝑃(attack reaches stage 𝑖))
(162)
Since attacks are more likely to escalate than benign messages (𝜌attack
𝑖
> 𝜌benign
𝑖
), the pipeline is biased toward
detecting attacks.
6.9.2
Adaptive Threshold Selection
Definition 6.27 (Adaptive Threshold). Thresholds adapt to observed attack frequency via online Bayesian
update:
𝜃𝑡+1
𝑖
= 𝜃𝑡
𝑖−𝛼lr ⋅∇𝜃𝑖[𝐶FN ⋅FNR(𝜃𝑡
𝑖) + 𝐶FP ⋅FPR(𝜃𝑡
𝑖)]
(163)
where 𝑎𝑙𝑝ℎ𝑎lr is the learning rate and 𝐶FN, 𝐶FP are cost weights.
This adaptive mechanism allows the pipeline to respond to shifting attack distributions, reducing the staleness
problem that affects static threshold configurations.
Empirical validation of this section’s theory: The detection methods formalized here are
empirically evaluated in Part 2 Friedman [2026a]. Key findings: (1) the multi-stage pipeline
shows biased escalation consistent with Theorem 6.11; (2) adversarial training across five rounds
demonstrates adaptive threshold adjustment consistent with Definition 6.27, raising hardened
detection from 52.0% at Round 1 to 67.9% at Round 5 in Part 2’s closed-form design model;
(3) the residual gap between the parametric ceiling and prototype performance is attributed to
adapter implementation maturity rather than to any per-class miss profile — Part 2 reports no
measured per-Ω-class rates — and that gap is module-specific rather than diffuse: a single compo-
nent’s rewrite moved the ablation arm’s measured detection most of the way to the ceiling (Part
2, “Adversarial Training Evaluation”, “Defense Component Contributions”, and the “Parametric
Simulation Analysis” supplement).
70

## Page 72

7
Formal Verification: Safety Properties and Model Checking
This section establishes safety properties (Section 7.1), proves invariant preservation lemmas (Section 7.2),
demonstrates liveness guarantees (Section 7.3), derives complexity bounds (Section 7.4), and presents model
checking verification (Section 7.5).
7.1
Safety Properties
7.1.1
Belief Integrity
Theorem 7.1 (Belief Injection Resistance). Under CIF with firewall detection rate 𝑟𝑓and sandboxing
verification rate 𝑟𝑠:
𝑃(𝒜𝐵𝐼succeeds) ≤(1 −𝑟𝑓) ⋅(1 −𝑟𝑠)
(164)
Proof. We prove this theorem by analyzing the sequential defense mechanism and applying probability theory
for independent events.
Setup: Let 𝑝ℎ𝑖𝑎𝑑𝑣be an adversarial belief that the attacker attempts to inject into agent 𝑎𝑖’s verified belief
set ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑.
Defense Model: The CIF implements two sequential defenses:
1. Cognitive Firewall ℱ: Classifies incoming messages as ACCEPT, QUARANTINE, or REJECT with
detection rate 𝑟𝑓
2. Belief Sandbox: Verifies quarantined beliefs before promotion with verification rate 𝑟𝑠
Step 1: For 𝑝ℎ𝑖𝑎𝑑𝑣to enter ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑, it must first pass the firewall.
Let 𝐸𝑓= “Firewall fails to detect 𝑝ℎ𝑖𝑎𝑑𝑣”. By definition of detection rate:
𝑃(𝐸𝑓) = 1 −𝑟𝑓
(165)
Step 2: If 𝑝ℎ𝑖𝑎𝑑𝑣passes the firewall (event 𝐸𝑓), it enters ℬ𝑝𝑟𝑜𝑣𝑖𝑠𝑖𝑜𝑛𝑎𝑙. For injection to succeed, it must then
pass sandbox verification.
Let 𝐸𝑠= “Sandbox fails to detect 𝑝ℎ𝑖𝑎𝑑𝑣”. By definition of verification rate:
𝑃(𝐸𝑠) = 1 −𝑟𝑠
(166)
Step 3: The defenses are independent by design (defense-in-depth principle):
• Firewall uses syntactic/semantic analysis on message content
• Sandbox uses provenance verification, consistency checking, and corroboration
• These operate on orthogonal aspects of the belief
Therefore:
𝑃(𝐸𝑓∩𝐸𝑠) = 𝑃(𝐸𝑓) ⋅𝑃(𝐸𝑠|𝐸𝑓) = 𝑃(𝐸𝑓) ⋅𝑃(𝐸𝑠)
(167)
The conditional independence holds because sandbox verification is applied regardless of why the message
passed firewall, and sandbox criteria (provenance, consistency, corroboration) are independent of firewall
criteria (injection patterns, anomaly scores).
Step 4: The attack succeeds iff both defenses fail:
𝑃(𝒜𝐵𝐼succeeds) = 𝑃(𝐸𝑓∩𝐸𝑠) = (1 −𝑟𝑓) ⋅(1 −𝑟𝑠)
(168)
■
71

## Page 73

Corollary 7.2 (Empirical Security Bound). With 𝑟𝑓= 0.8 and 𝑟𝑠= 0.7:
𝑃(success) ≤(1 −0.8)(1 −0.7) = 0.2 ⋅0.3 = 0.06
(169)
Corollary 7.3 (Layered Defense Generalization). For 𝑛independent defense layers with rates 𝑟1, … , 𝑟𝑛:
𝑃(success) ≤
𝑛
∏
𝑖=1
(1 −𝑟𝑖)
(170)
7.1.2
No Trust Amplification (Model-Checking Target)
Theorem 7.4 (No Trust Amplification). For any path 𝑝= (𝑎0, 𝑎1, … , 𝑎𝑘) in the communication graph:
𝒯𝑝𝑎𝑡ℎ
𝑎0→𝑎𝑘≤
min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1
(171)
Proof. By trust delegation rule (Definition 4.7) and induction on path length.
Base case (𝑘= 1):
𝒯𝑎0→𝑎1 = 𝒯𝑎0→𝑎1
✓
(172)
Inductive step: Assume the theorem holds for paths of length 𝑘. For path length 𝑘+ 1:
𝒯𝑎0→𝑎𝑘+1 = min(𝒯𝑝𝑎𝑡ℎ
𝑎0→𝑎𝑘, 𝒯𝑎𝑘→𝑎𝑘+1) ⋅𝛿
(173)
≤min( min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1, 𝒯𝑎𝑘→𝑎𝑘+1)
= min
𝑖∈[0,𝑘] 𝒯𝑎𝑖→𝑎𝑖+1
■
7.1.3
Goal Alignment Preservation
Theorem 7.5 (Goal Alignment Invariant). If the system starts with aligned goals and all goal updates follow
the delegation protocol:
Aligned(𝒢0
𝑖) ∧∀𝑡∶ValidUpdate(𝒢𝑡
𝑖, 𝒢𝑡+1
𝑖
) ⇒∀𝑡∶Aligned(𝒢𝑡
𝑖)
(174)
Proof. ValidUpdate requires new goals derive from principal or valid delegation chain. By induction on time
𝑡, alignment is preserved at every step.
■
7.2
Invariant Preservation Lemmas
Lemma 7.6 (Belief Consistency Preservation). If ℬ𝑡
𝑖is consistent and the belief update follows Rule B-
DIRECT or B-DELEGATED (Section 4.4.7), then ℬ𝑡+1
𝑖
is consistent.
Proof. Let Consistent(ℬ) denote that no high-confidence contradictions exist:
Consistent(ℬ) ⟺∄𝜙, 𝜓∶ℬ(𝜙) > 𝜏∧ℬ(𝜓) > 𝜏∧(𝜙∧𝜓⊢⊥)
(175)
Case 1: Rule B-DIRECT applies.
The update adds evidence for proposition 𝑝ℎ𝑖:
ℬ𝑡+1
𝑖
(𝜙) = BayesUpdate(ℬ𝑡
𝑖(𝜙), 𝑐⋅𝒯𝑖→𝑠)
(176)
72

## Page 74

If the update would create contradiction (i.e., both ℬ𝑡+1(𝑝ℎ𝑖) > 𝑡𝑎𝑢and ℬ𝑡+1(𝑝𝑠𝑖) > 𝑡𝑎𝑢for contradictory
𝑝ℎ𝑖, 𝑝𝑠𝑖), the sandbox consistency check in Rule S-PROMOTE rejects promotion:
𝑉(𝜋) = 1 ∧Consistent(ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑∪{𝜙}) ∧|Corroborate(𝜙)| ≥𝜅
(177)
Therefore, only consistent updates reach ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑.
Case 2: Rule B-DELEGATED applies.
Same argument, with additional trust decay ensuring lower confidence for delegated evidence.
■
Lemma 7.7 (Trust Matrix Preservation). The trust matrix 𝒯remains well-formed after any valid update:
∀𝑖, 𝑗∶0 ≤𝒯𝑖→𝑗≤1
(178)
Proof. By Definition 4.6, trust is computed as:
𝒯𝑡
𝑖→𝑗= 𝛼⋅𝑇𝑏𝑎𝑠𝑒(𝑗) + 𝛽⋅𝑇𝑡
𝑟𝑒𝑝(𝑗) + 𝛾⋅𝑇𝑡
𝑐𝑡𝑥(𝑖, 𝑗)
(179)
where 𝑎𝑙𝑝ℎ𝑎+ 𝑏𝑒𝑡𝑎+ 𝑔𝑎𝑚𝑚𝑎= 1 and each component 𝑇∗∈[0, 1].
Therefore:
𝒯𝑡
𝑖→𝑗∈[min(𝑇𝑏𝑎𝑠𝑒, 𝑇𝑟𝑒𝑝, 𝑇𝑐𝑡𝑥), max(𝑇𝑏𝑎𝑠𝑒, 𝑇𝑟𝑒𝑝, 𝑇𝑐𝑡𝑥)] ⊆[0, 1]
(180)
For delegation (Definition 4.7):
𝒯𝑑𝑒𝑙
𝑖→𝑘= min(𝒯𝑖→𝑗, 𝒯𝑗→𝑘) ⋅𝛿𝑑
(181)
Since min(⋅) <= 1 and 𝑑𝑒𝑙𝑡𝑎∈(0, 1), we have 𝒯𝑑𝑒𝑙
𝑖−>𝑘∈[0, 1].
■
Lemma 7.8 (Provenance Chain Integrity). Every belief in ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑has a valid, verifiable provenance chain.
Proof. By Rule S-PROMOTE (Section 4.4.8), promotion from ℬ𝑝𝑟𝑜𝑣𝑖𝑠𝑖𝑜𝑛𝑎𝑙to ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑requires:
𝑉(𝜋(𝜙)) = 1
(182)
where 𝑉is the provenance verification function.
By construction of the sandbox, beliefs can only enter ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑through:
1. Initial system beliefs (hardcoded with SYSTEM_VERIFIED provenance)
2. Promotion from provisional (verified by 𝑉)
In both cases, provenance is verified. By induction on the history of ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑, all beliefs have valid provenance.
■
Lemma 7.9 (Permission Boundary Preservation). Effective permissions never exceed granted permissions:
∀𝑎𝑖, ∀action ∶𝒫𝑒𝑓𝑓𝑒𝑐𝑡𝑖𝑣𝑒(𝑎𝑖, action) ≤𝒫𝑟𝑜𝑙𝑒(𝑎𝑖, action)
(183)
Proof. By Table 10:
𝒫𝑒𝑓𝑓𝑒𝑐𝑡𝑖𝑣𝑒(𝑎𝑖) = 𝒫𝑟𝑜𝑙𝑒(𝑎𝑖) ∩𝒫𝑑𝑒𝑙𝑒𝑔𝑎𝑡𝑒𝑑(𝑎𝑖) ∩𝒫𝑐𝑜𝑛𝑡𝑒𝑥𝑡(𝑎𝑖)
(184)
Since intersection can only reduce permissions (𝐴∩𝐵∩𝐶⊆𝐴), we have 𝒫𝑒𝑓𝑓𝑒𝑐𝑡𝑖𝑣𝑒(𝑎𝑖, action) <=
𝒫𝑟𝑜𝑙𝑒(𝑎𝑖, action) for all actions.
■
Lemma 7.10 (Firewall Completeness). Every incoming message is classified by the firewall.
73

## Page 75

Proof. By Definition 5.2, the firewall is a total function:
ℱ∶ℳ→{ACCEPT, QUARANTINE, REJECT}
(185)
The decision rules cover all cases:
• If 𝐷𝑖𝑛𝑗(𝑚) > 𝑡𝑎𝑢1: REJECT
• Else if 𝐷𝑠𝑢𝑠(𝑚) > 𝑡𝑎𝑢2: QUARANTINE
• Else: ACCEPT
Since 𝐷𝑖𝑛𝑗and 𝐷𝑠𝑢𝑠are defined for all messages, and the conditions are exhaustive, every message receives
a classification.
■
7.3
Liveness Properties
7.3.1
Non-Blocking
Theorem 7.11 (Firewall Liveness). CIF firewall preserves liveness for legitimate inputs:
∀𝑚∈ℳ𝑙𝑒𝑔𝑖𝑡𝑖𝑚𝑎𝑡𝑒∶𝑃(ℱ(𝑚) = ACCEPT) ≥1 −𝜖𝑓𝑝
(186)
Proof. By firewall design, false positive rate is bounded by 𝑒𝑝𝑠𝑖𝑙𝑜𝑛𝑓𝑝. Legitimate messages are rejected only
on false positive, establishing the bound.
■
7.3.2
Progress Guarantee
Theorem 7.12 (Byzantine Consensus Termination). With 𝑛>= 3𝑓+ 1 agents and at most 𝑓Byzantine:
𝑃(consensus reached in 𝑂(𝑓+ 1) rounds) = 1
(187)
Proof. Standard Byzantine agreement result (Lamport et al., 1982). With honest majority 𝑛>= 3𝑓+1, the
PBFT protocol guarantees termination in 𝑓+ 1 rounds.
■
7.4
Complexity Bounds
7.4.1
Space Complexity
Table 36: Per-component space complexity.
Component
Space
Notes
Belief state
𝑂(|Φ|)
Propositions tracked
Provenance
𝑂(|Φ| ⋅𝑑)
𝑑= max chain depth
Trust matrix
𝑂(𝑛2)
Pairwise trust
Tripwires
𝑂(𝑘)
𝑘= canary count
History
𝑂(𝑤)
Window size
Theorem 7.13 (Total Space Bound). The total space complexity of CIF for 𝑛agents with |Φ| propositions,
provenance depth 𝑑, 𝑘tripwires, and window size 𝑤is:
𝑆𝑡𝑜𝑡𝑎𝑙= 𝑂(𝑛⋅(|Φ| ⋅𝑑+ 𝑘+ 𝑤) + 𝑛2)
(188)
Proof. Per agent:
• Belief state: |Φ| propositions with confidence values = 𝑂(|Φ|)
• Provenance: Each belief has chain of depth at most 𝑑= 𝑂(|Φ| ⋅𝑑)
74

## Page 76

• Tripwires: 𝑘canary beliefs = 𝑂(𝑘)
• History window: 𝑤events = 𝑂(𝑤)
Total per agent: 𝑂(|Φ| ⋅𝑑+ 𝑘+ 𝑤)
Global:
• Trust matrix: 𝑛× 𝑛= 𝑂(𝑛2)
• Shared state: 𝑂(|𝒮|) (constant relative to 𝑛)
Total for 𝑛agents: 𝑂(𝑛⋅(|Φ| ⋅𝑑+ 𝑘+ 𝑤) + 𝑛2).
■
7.4.2
Time Complexity
Table 37: Per-operation time complexity.
Operation
Time
Frequency
Firewall check
𝑂(|𝑚|)
Per message
Trust update
𝑂(1)
Per interaction
Drift detection
𝑂(|Φ|)
Per window
Consensus
𝑂(𝑛2)
Per decision
Provenance trace
𝑂(𝑑)
On demand
Theorem 7.14 (Per-Message Processing Time). Processing a single message 𝑚takes time:
𝑇𝑚𝑠𝑔= 𝑂(|𝑚| + min(𝑑, timeout))
(189)
Proof. Message processing pipeline:
1. Firewall classification: 𝑂(|𝑚|) for pattern matching and semantic analysis
2. Sandbox entry (if quarantined): 𝑂(1)
3. Provenance verification (if promoted): 𝑂(𝑑) to trace chain
4. Trust update: 𝑂(1) weighted average
5. Tripwire check: 𝑂(𝑘), typically 𝑘≪|𝑚|
Provenance verification can be bounded by timeout. Total: 𝑂(|𝑚| + 𝑑).
■
Theorem 7.15 (Consensus Round Complexity). Byzantine consensus requires 𝑂((𝑓+ 1) ⋅𝑛2) message
complexity.
Proof. Standard PBFT result:
• 𝑓+ 1 rounds required to guarantee termination with 𝑓Byzantine failures
• Each round requires all-to-all communication: 𝑂(𝑛2) messages
• Total: 𝑂((𝑓+ 1) ⋅𝑛2)
■
75

## Page 77

7.4.3
Latency Overhead
Theorem 7.16 (Bounded Latency Overhead). CIF adds latency:
𝐿𝐶𝐼𝐹= 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙+ 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥⋅𝑃(quarantine) + 𝐿𝑣𝑒𝑟𝑖𝑓𝑦⋅𝑃(verify)
(190)
Proof. Expected latency is sum of:
1. Firewall (always): 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙
2. Sandbox (conditional): 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥⋅𝑃(message quarantined)
3. Verification (conditional): 𝐿𝑣𝑒𝑟𝑖𝑓𝑦⋅𝑃(belief promoted)
With illustrative parameters (these are worked-example values chosen to exercise the bound, not measure-
ments; Part 2 reports a mean firewall latency of 0.040 ms per sample (p95 0.055 ms) on its prototype pipeline,
and the deployment-scale constants below are not derived from it):
• 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙= 10ms
• 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥= 5ms, 𝑃(quarantine) = 0.3
• 𝐿𝑣𝑒𝑟𝑖𝑓𝑦= 15ms, 𝑃(verify) = 0.2
𝐿𝐶𝐼𝐹≈10 + 5 ⋅0.3 + 15 ⋅0.2 = 10 + 1.5 + 3 = 14.5ms
(191)
Compared to baseline 𝑎𝑏𝑜𝑢𝑡11.8ms: overhead factor 𝑎𝑏𝑜𝑢𝑡1.23 (23%).
■
7.5
Formal Model Checking
7.5.1
State Space Definition
Definition 7.1 (System State). The complete system state is the tuple:
𝑠= (𝜎1, … , 𝜎𝑛, 𝒮, 𝒯)
(192)
where 𝑠𝑖𝑔𝑚𝑎𝑖is agent 𝑖’s cognitive state, 𝒮is shared state, and 𝒯is the trust matrix.
7.5.2
Temporal Properties
We verify the following CTL (Computation Tree Logic) properties:
Property 7.1 (Safety: Consensus Integrity).
𝐴𝐺(¬compromised(ℬ𝑐𝑜𝑛𝑠𝑒𝑛𝑠𝑢𝑠))
(193)
“Always globally, consensus beliefs are not compromised.”
Property 7.2 (Liveness: Request-Response).
𝐴𝐺(request ⇒𝐴𝐹(response))
(194)
“Every request eventually gets a response.”
Property 7.3 (Fairness: Tripwire Checking).
𝐴𝐺(𝐴𝐹(tripwire_checked))
(195)
“Tripwires are checked infinitely often.”
76

## Page 78

7.5.3
Model Checking Results
The following table summarizes the expected state space exploration for each property based on formal
analysis of the CIF specification. These values represent theoretical bounds derived from the state space
definition (Definition 7.1) and complexity analysis (Section 7.4). Part 2 carries the executable NuSMV, SPIN
and TLA+ specifications and the script that runs them, but records in output/formal/verification_sum
mary.json that none of the three checkers was present in that environment, so no part of this series reports
an executed model-checking verdict.
Table 38: Model checking state-space bounds. “Verified” here denotes a theoretical bound established in this
part, not a checker’s verdict; Part 2’s S04 carries the executable NuSMV/SPIN/TLA+ specifications, and
records that no checker was available to run them. No model checker was executed anywhere in this series.
Property
Status
Reference
Belief integrity
theoretical bound; executable run in Part 2 §S04
Theorem 7.1
Trust bounded
theoretical bound; executable run in Part 2 §S04
Theorem 7.4
No deadlock
theoretical bound; executable run in Part 2 §S04
Theorem 7.11
Eventual detection
theoretical bound; executable run in Part 2 §S04
Theorem 4.17
Note: Model checking tool configurations (NuSMV, SPIN, TLA+) and verification parameters
are provided in Part 2: Computational Validation, which presents the executable implementations
and empirical verification results.
7.5.4
Verification Results Summary
The following table records which property each tool is configured to check and the status of the corresponding
analytical result.
It is a plan, not a set of outcomes: no model-checking run is executed in this paper.
These guarantees follow from the CTL/LTL property specifications (Section 7.5.2) applied to the state
space definition (Section 7.5.1). Empirical execution of these verification configurations, including runtime
measurements and counterexample analysis, is presented in Part 2.
Table 39: Model-checking plan: the property each tool is configured to check, and the status of the corre-
sponding analytical result. No run of these configurations is reported in this paper; execution is Part 2’s.
Tool
Property to check
Status of the analytical result
Reference
NuSMV
Belief Integrity
Proved (S01)
Theorem 7.1
NuSMV
No Trust Amplification
Proved (S01)
Theorem 7.4
SPIN
No Deadlock
Proved (S01)
Theorem 7.11
SPIN
Eventual Detection
Asserted, proof deferred
Theorem 4.17
TLA+
Type Invariant
Definitional
Definition 4.3
TLA+
Consensus Integrity
Proved (S01)
Theorem 7.12
7.5.5
Counterexample Analysis
When verification fails, model checkers produce counterexamples Clarke et al. [1999]. Analysis procedure:
1. Extract trace: Sequence of states leading to violation
2. Identify trigger: First state where invariant fails
3. Root cause: Determine which transition violated property
4. Fix: Strengthen preconditions or add defense mechanism
5. Re-verify: Confirm fix resolves violation
Example: Counterexample Trace
77

## Page 79

State 0: Initial (all beliefs verified, trust matrix valid)
State 1: Agent 2 receives message from Agent 3
State 2: Firewall accepts (below threshold)
State 3: Belief promoted without corroboration check
State 4: VIOLATION: Unverified belief in B_verified
Root Cause: Missing corroboration check in promotion rule.
Fix: Add predicate |Corroborate(𝜙)| ≥𝜅to Rule S-PROMOTE (Section 4.4.8).
78

## Page 80

8
Discussion: Theoretical Implications, Limitations, and Future
Directions
This section examines the theoretical implications of the Cognitive Integrity Framework (Section 8.2), formal
limitations (Section 8.3) and boundary conditions (Section 10), relationship to prior work (Section 8.4),
governance implications (Section 8.5), and future research directions (Section 8.6).
8.1
Empirical Validation Summary (Part 2)
The formal mechanisms proposed in this paper have been validated through extensive architecture-aware
parametric simulation in Part 2: Computational Validation Friedman [2026a]. In experiments across the
four production multiagent architectures Part 2 evaluates (Claude Code, AutoGPT, CrewAI, LangGraph),
the parametric simulation establishes a design-level detection ceiling of 96–100% against a corpus of 950
cognitive attacks; the prototype pipeline achieves a mean detection rate of 86.3% [95% CI: 85.5%, 87.1%]
across 30 random seeds (Part 2, Results).
Key empirical findings include:
1. Defense Composition: Consistent with the series and parallel detection-rate theorems (Theorem 5.4,
Theorem 5.5), layered defenses composed multiplicatively, with the full framework outperforming any
single mechanism. Part 2’s ablation studies qualify this: on their corpus the composition is dominated
rather than balanced, with the Behavioral Invariants module accounting for almost all of the composed
pipeline’s detection and every other module measuring at or near zero marginal contribution — what
each adds beyond the rest of the stack, which is not the same quantity as what each detects alone.
2. Trust Boundedness: The 𝛿𝑑trust decay parameter successfully prevented “trust laundering’ ’ ampli-
fication attacks in all tested topologies, validating Formula 4.
3. Architecture Dependence: As predicted by our threat model, the architecture with the lowest para-
metric detection in Part 2 is AutoGPT’s autonomous-mesh topology, whose distributed trust structure
offers the widest lateral-movement surface; hierarchical topologies concentrate risk in orchestrator com-
promise instead. No peer-to-peer architecture was evaluated.
4. Adversarial Training: In Part 2’s closed-form adversarial-training design model, five rounds on the
Claude Code architecture raise hardened detection from 52.0% (Round 1) to 67.9% (Round 5), +23.2
pp over the pre-AT baseline. The per-round gain sequence (7.3, 5.6, 5.0, 2.9, 2.4) pp is approximately
linear rather than geometrically decaying, and the projected Nash equilibrium of 100.0% is a property
of the model’s assumed gains, not a measured equilibrium. These are design-model values, not pipeline-
in-the-loop measurements.
These
results
confirm
that
the
abstract
properties
proven
here—boundedness,
composition,
and
detectability—translate into concrete security improvements when implemented in realistic agent architec-
tures.
8.2
Theoretical Implications
8.2.1
Why Composable Defenses Are Necessary
The defense composition algebra (Theorem 5.4, Theorem 5.5) formalizes a principle implicit in security
practice: layered defenses provide multiplicative rather than additive protection. Each defense mechanism
addresses a distinct attack surface:
The orthogonality of these surfaces explains why no single mechanism suﬀices: an attack that bypasses input
filtering may still violate behavioral invariants; an attack that evades pattern matching may still trigger
belief drift detection.
Empirical ablation studies in Part 2 test this prediction and return a sharper answer than a ranked list. On
the 100-attack ablation corpus a single module dominates: removing Behavioral Invariants costs ΔTPR =
−0.650 against a full pipeline of 0.890, the Tripwire costs −0.020, and the Firewall, Consensus, Detection,
Provenance, Sandbox and Trust Calculus register no change at all. Those zeros are marginal quantities and
79

## Page 81

Table 40: Defense mechanisms and their target attack surfaces.
Defense Layer
Target Attack Surface
Cognitive Firewall
Input-based injection
Belief Sandbox
Unverified content propagation
Tripwires
Belief manipulation
Trust Calculus
Delegation abuse
Byzantine Consensus
Coordination attacks
are not evidence of zero capability: a module whose detections are a subset of another’s is invisible to leave-
one-out removal however much it catches on its own. What the ablation establishes is therefore weaker than
the theorem and more useful than a ranking — no single mechanism outperforms the composed ensemble,
consistent with Theorem 5.4, but on this corpus the composition is dominated by one factor rather than
balanced across many, so the multiplicative bound holds without being informative.
8.2.2
The Trust Boundedness Guarantee
The bounded trust theorem (Theorem 4.3) represents a structural guarantee against trust amplification
attacks.
Unlike detection-based defenses that may be evaded by novel attacks, the 𝛿𝑑decay bound is
algebraic: it holds for any attack type, any adversary capability, and any delegation chain length. This
makes it a formal rather than empirical security property.
The decay factor 𝛿∈[0, 1) creates a tradeoff:
• Lower 𝛿: Stronger security, limited delegation utility
• Higher 𝛿: More delegation flexibility, weaker bounds
Organizations must calibrate this tradeoff based on their threat model (Section 5.1 in Part 3). Domain-
calibrated 𝛿choices — from millisecond OODA cycles in drone swarms to year-scale diplomatic agents —
are analyzed in Part 3 Friedman [2026b] across ten critical operational domains.
8.2.3
Information-Theoretic Detection Limits
The stealth-impact fundamental limit (Theorem 4.15) establishes that certain attacks are provably unde-
tectable without unacceptable false positive rates. This is not a limitation of our specific mechanisms but
a fundamental bound analogous to Shannon’s channel capacity—some attacks simply cannot be detected
without additional information.
This has practical implications: security architectures should not promise detection of all possible attacks.
Instead, they should characterize the detection boundary and provide containment for attacks that cross it.
8.2.4
Architecture-Specific Vulnerability Patterns
The formal framework reveals why different multiagent architectures exhibit different vulnerability profiles:
Table 41: Theoretical vulnerability analysis by architecture type.
Architecture
Theoretical Vulnerability
Formal Mitigation
Hierarchical
Single point of trust concentration
Byzantine-tolerant orchestrator
Peer-to-peer
Uniform trust enables lateral movement
Trust decay on delegation
Role-based
Logical (not cryptographic) boundaries
Attestation per role transition
State machine
State integrity assumption
State hash verification
These are structural properties of the architectures themselves, not implementation-specific weaknesses.
80

## Page 82

8.3
Formal Limitations
8.3.1
Assumption Dependencies
The formal guarantees of CIF depend on specific assumptions. Violation of these assumptions degrades or
eliminates security properties:
Table 42: Impact of assumption violations on formal guarantees.
Assumption
Guarantee Impacted
Honest orchestrator
Ω5
attacks
succeed;
systemic
compromise possible
𝑛>= 3𝑓+ 1 agents
Byzantine consensus fails (Theo-
rem 5.3)
Authenticated channels
Ω4 coordination attacks expand
Known attack patterns
Zero-day evasion possible
8.3.2
Scalability Constraints
The formal framework imposes scaling limitations:
𝑀trust = 𝑂(𝑛2)
(196)
𝐿consensus = 𝑂(𝑛2)
(197)
The quadratic trust matrix (Equation (196)) limits practical deployment to systems with moderate agent
counts. Sparse trust representations or hierarchical trust structures may enable scaling to larger systems.
Consensus latency (Equation (197)) suggests that Byzantine consensus should be reserved for critical deci-
sions rather than applied universally.
8.3.3
Inherent Detection Gaps
Certain attack types are formally diﬀicult to detect:
• Semantic equivalence: Attacks preserving meaning while changing syntax evade pattern-based de-
tection
• Progressive drift: Sub-threshold changes that accumulate over time (Equation (24))
• Orchestrator compromise: Outside the Ω1–Ω4 threat model
These are not implementation failures but formal limitations of the detection paradigm.
8.4
Relationship to Prior Work
CIF builds on and extends several research traditions:
Byzantine Fault Tolerance: Classical BFT (PBFT, etc.) assumes crash or arbitrary faults. CIF extends
this to cognitive manipulation—agents that appear functional but hold corrupted beliefs.
Trust Management Systems: Prior systems (PolicyMaker, SPKI, etc.) focus on authorization decisions.
CIF addresses continuous trust evolution with provable decay bounds.
AI Safety and Alignment: Constitutional AI Bai et al. [2022] and similar approaches address single-agent
alignment. CIF extends these concepts to multi-agent coordination integrity.
Prompt Injection Defenses: Existing defenses focus on single-agent scenarios. CIF addresses the propa-
gation and amplification of attacks across agent networks.
81

## Page 83

Cognitive Science and Active Inference: The Active Inference framework David et al. [2021] provides
a complementary perspective from cognitive science, modeling agents as entities that minimize prediction
error through continuous perception-action loops. The Active Inference Conflict (AIC) model extends classi-
cal decision frameworks like OODA loops (Observe-Orient-Decide-Act) by situating conflict as a multiscale
process of communication, trust, and relationship management—themes that directly inform CIF’s trust
calculus. AIC’s treatment of BOLTS components (Business, Operations, Legal, Technical, Social) also in-
forms our analysis of cyberphysical cognitive systems where cognitive security spans multiple operational
domains. Critically, the Active Inference perspective illuminates why belief manipulation attacks are partic-
ularly dangerous: agents minimizing variational free energy will actively seek information confirming their
current beliefs, creating self-reinforcing loops when those beliefs are corrupted. CIF’s tripwire mechanism
interrupts this by detecting when prediction error patterns deviate from baseline, analogous to detecting
abnormal precision weighting in cognitive systems.
Pattern Languages for Cognitive Security: The COGSEC ATLAS COGSEC et al. [2023] provides a
practitioner-oriented complement to CIF’s formal approach, cataloging 995 cognitive security patterns orga-
nized by type (Vulnerability, Exploit, Remedy, Practice, Accelerator, Moderator, Condition). Where CIF
provides provable guarantees and formal composition rules, the Atlas offers an empirically-grounded taxon-
omy of observed attack patterns and defensive practices—such as the Devil’s Advocate and Key Assumptions
Check techniques for countering groupthink and confirmation bias. The hierarchical parent-child structure
of Atlas patterns maps naturally onto CIF’s adversary class hierarchy, suggesting opportunities for formal
verification of pattern-based defenses using the mechanisms described in Section 5.
The novel contribution is the integration of these concerns into a unified formal framework with composable
guarantees.
8.5
Governance and Policy Implications
8.5.1
The Regulatory Gap
Current AI regulation lacks cognitive security provisions:
Table 43: Regulatory gaps for cognitive security.
Regulation
Current Focus
Cognitive Security Gap
EU AI Act
Risk classification, trans-
parency
No inter-agent trust re-
quirements
NIST AI RMF
Risk management lifecycle
Limited
multiagent-
specific guidance
ISO 42001
AI management systems
Process-focused,
not
cognitive-state focused
8.5.2
Recommendations for Policy
We propose that regulators consider:
1. Cognitive Security Audits: Mandatory assessment of inter-agent trust mechanisms for high-risk
deployments
2. Transparency Requirements: Disclosure of trust hierarchies and delegation policies
3. Incident Reporting: New category for cognitive attacks
4. Certification Pathways: Industry certification for cognitive security practices
82

## Page 84

8.6
Future Theoretical Directions
8.6.1
Adaptive Defense Theory
The detection degradation problem suggests a need for adaptive defenses. Formal treatment as a game-
theoretic equilibrium:
𝜋∗
defense = arg max
𝜋
𝔼[∑
𝑡
𝛾𝑡𝑟(𝑠𝑡, 𝑎𝑡)]
(198)
requires solving the partial observability problem—defenders cannot directly observe attacker intent.
8.6.2
Cross-System Trust Federation
Extending trust calculus across organizational boundaries:
𝒯cross
𝑖→𝑗= 𝑓(𝒯local, 𝒯reputation, 𝒯attestation)
(199)
The primary challenge is trust calibration—mapping heterogeneous trust semantics across systems with
different threat models.
8.6.3
Emergent Behavior Security
As multiagent systems scale, emergent collective behaviors become security-relevant. Open questions include:
• Formal characterization of beneficial vs. malicious emergence
• Detection of emergent coordination patterns indicating compromise
• Sandboxing that preserves beneficial emergence while constraining malicious emergence
The colony cognitive security perspective developed in Section 12 provides initial formal foundations for
these questions.
8.6.4
Long-Horizon Agent Security
Agents operating over extended time horizons (days, weeks, months) face additional challenges:
• Memory integrity: Verification of accumulated knowledge
• Goal stability: Distinguishing legitimate evolution from adversarial drift
• Temporal consistency: Decisions consistent with historical context
The trust calculus extends naturally to temporal trust: 𝒯𝑡= 𝒯𝑡−1 ⋅𝛿time where 𝛿time encodes trust decay
over time.
8.6.5
The Cognitive Security Research Agenda
We propose a research agenda organized by time horizon:
Near-term (1–2 years):
• Standardized formal verification benchmarks
• Integration of CIF mechanisms into production frameworks
• Theoretical analysis of real-world attack patterns
Medium-term (2–5 years):
• Game-theoretic foundations for adaptive defenses
83

## Page 85

• Cross-organizational trust federation protocols
• Hardware-backed cognitive security guarantees
Long-term (5+ years):
• Formal verification of emergent agent behavior
• Self-healing cognitive security systems
• Integration with broader AI safety theory
The formal foundations established in this work—bounded trust, composable defenses, information-theoretic
limits—provide a stable basis for this evolving research program.
84

## Page 86

9
Conclusion: Summary and Actionable Recommendations
9.1
Summary
We presented the Cognitive Integrity Framework (CIF), a formal foundation for securing multiagent
AI operators against cognitive manipulation attacks. As AI deployment shifts from single-model inference to
autonomous agent orchestration, the attack surface expands from input/output filtering to encompass beliefs,
goals, trust relationships, and inter-agent coordination. CIF addresses this expanded surface through formal
mechanisms with provable guarantees.
9.1.1
Formal Contributions
Table 44: Summary of formal contributions.
Contribution
Significance
Trust Calculus
Bounded delegation with 𝑂(𝑑𝑒𝑙𝑡𝑎𝑑) decay guarantee
prevents trust laundering and amplification—a struc-
tural property independent of adversary sophistica-
tion
Defense Composition Algebra
Formal rules enabling predictable reasoning about
layered defense effectiveness
Information-Theoretic Bounds
Fundamental limits on stealth-impact tradeoff con-
straining adversary capabilities
Integrity Properties
Belief consistency, goal alignment, provenance verifi-
ability as verifiable properties
9.1.2
Conceptual Contributions
1. Cognitive Security Operator Posture: A defensive stance for systems where the attack surface is
the reasoning process itself—distinct from traditional perimeter security
2. The 2026 Multiagent Landscape: Characterization of contemporary agentic AI as cyberphysical
cognitive operators with persistent agency, active world modification, hierarchical delegation, and cross-
modality operation
3. Cross-Modality Trust: Extension of trust calculus to handle heterogeneous modalities with modality-
adjusted reliability factors
4. Federated Trust: Framework for reasoning about trust across organizational boundaries
9.1.3
Core Insights
1. Multiagent systems require multiagent security: Single-agent defenses miss inter-agent attack
vectors entirely. The trust relationship between agents is itself an attack surface.
2. Trust must be bounded: Without 𝑑𝑒𝑙𝑡𝑎𝑑decay, delegation chains enable trust laundering where
adversarial content acquires trusted-source status through intermediaries. This is a structural vulner-
ability requiring structural mitigation.
3. Defenses compose predictably: The defense composition algebra enables formal reasoning about
layered security. Orthogonal defenses compose multiplicatively, explaining why full CIF substantially
outperforms any single mechanism.
4. Information-theoretic limits constrain adversaries: The stealth-impact tradeoff theorem estab-
lishes that high-impact attacks cannot remain completely undetectable.
This provides theoretical
grounding for defense strategies.
85

## Page 87

5. Cognitive security requires continuous verification: Unlike perimeter security that trusts in-
ternals after boundary checks, cognitive security requires continuous verification of beliefs, goals, and
trust relationships.
9.2
Actionable Recommendations
9.2.1
For Practitioners
Immediate priorities:
1. Implement trust decay in all delegation chains (𝑑𝑒𝑙𝑡𝑎<= 0.9)
2. Deploy cognitive tripwires for identity and boundary beliefs
3. Establish belief provenance tracking for high-stakes decisions
4. Define escalation procedures for cognitive security alerts
Architecture selection:
Match security posture to threat model.
Hierarchical architectures with
Byzantine-tolerant orchestrators suit high-security contexts; peer-to-peer topologies with trust decay may
suﬀice for collaborative environments.
9.2.2
For Researchers
Open Questions with significant impact potential:
Theoretical Foundations
• Q1: Optimal trust decay functions. Under what conditions is exponential decay (𝛿𝑑) optimal?
Are there task distributions or adversary models where alternative decay functions (e.g., polynomial,
threshold-based) provide better security-utility tradeoffs?
• Q2: Tight detection bounds. Can the stealth-impact bounds in Theorem 4.15 be tightened? What
adversary adaptations most effectively approach the theoretical limit, and what detection enhancements
can push the bound further?
• Q3: Belief consistency under partial observability. How should agents maintain belief integrity
when they cannot observe the full system state? What guarantees remain achievable with bounded
observation horizons?
Defense Mechanisms
• Q4: Adaptive defense evolution. How can defense mechanisms learn from detected attacks without
creating new vulnerabilities? Can we formalize safe online learning for cognitive defenses?
• Q5:
Semantic equivalence detection.
What architectures best detect semantically equivalent
attacks that evade syntactic pattern matching? How do we balance detection sensitivity against com-
putational overhead?
• Q6: Orchestrator hardening. Given that orchestrator compromise bypasses downstream defenses,
what architectural patterns minimize single-point-of-failure risk while maintaining coordination eﬀi-
ciency?
Scalability and Performance
• Q7: Large-scale consensus. How can Byzantine-tolerant consensus scale beyond 𝑂(𝑛2) message
complexity for agent populations > 1000? Are hierarchical or probabilistic approaches suﬀicient for
CIF guarantees?
• Q8: Real-time defense overhead. What is the fundamental latency-security tradeoff for cognitive
firewalls? Can streaming classifiers achieve comparable accuracy to batch models?
Evaluation and Benchmarking
86

## Page 88

• Q9: Adversarial benchmark construction. How should we construct attack corpora that remain
challenging despite model improvements? Can we formalize attack diversity and coverage metrics?
• Q10: Colony CogSec evaluation. What benchmarks capture stigmergic attack surfaces—shared
state manipulation, environmental signaling, emergent coordination failures? (Section 12)
Cross-Organizational Deployment
• Q11:
Federated trust interoperability.
How can organizations with different trust semantics,
decay parameters, and risk tolerances federate securely? What minimal protocol guarantees enable
safe cross-boundary delegation?
• Q12: Trust portability. When agents migrate between organizations or contexts, how should accu-
mulated trust transfer? What prevents trust-laundering through organizational hops?
Governance and Long-term Safety
• Q13: Liability attribution. When a delegated agent causes harm through a multi-hop chain, how
should responsibility distribute? What logging and provenance mechanisms support post-hoc attribu-
tion?
• Q14: Emergent goal stability. As agent populations grow and interact, what formal guarantees
prevent collective goal drift toward unintended attractors? How do we verify alignment preservation
at scale?
Cognitive Science and First Principles of Intelligence
• Q15: Cognitive security as predictive processing. How do CIF defense mechanisms map onto
predictive coding architectures? Can belief sandboxing be understood as precision-weighted prediction
error gating?
• Q16: Collective intelligence foundations. What principles from swarm cognition, distributed
problem-solving, and stigmergic coordination inform robust multiagent security? How do honeybee
quorum sensing and ant colony consensus differ from Byzantine fault tolerance?
• Q17: Metacognitive integrity. How should agents reason about their own cognitive security status?
What introspective mechanisms enable agents to detect when their own belief-formation processes may
be compromised?
Active Inference and Free Energy Principle
• Q18: CIF as active inference. Can the Cognitive Integrity Framework be reformulated within the
Free Energy Principle? Do trust dynamics correspond to precision estimation, and attacks to artificial
inflation of prediction errors? (Section 12)
• Q19: Expected free energy for defense selection. How can agents use expected free energy to
select among available defense mechanisms? What priors over attack distributions optimize epistemic
and pragmatic value?
• Q20:
Allostatic cognitive security.
How should agents maintain cognitive homeostasis under
adversarial conditions? What are the analogs of interoceptive inference for detecting internal state
manipulation?
Systems Neuroscience and Neural Computation
• Q21: Neuromodulatory trust dynamics. How do biological neuromodulatory systems (dopamine,
acetylcholine, norepinephrine) implement trust and uncertainty estimation? What computational prin-
ciples transfer to artificial cognitive security?
• Q22:
Hierarchical predictive security.
How should defense mechanisms be organized across
cortical-like processing hierarchies? Can top-down predictions provide robustness against bottom-up
adversarial inputs?
87

## Page 89

• Q23: Attentional gating for cognitive firewalls. What can selective attention mechanisms teach
us about eﬀicient input filtering?
How do biological systems achieve low-latency threat detection
without exhaustive content analysis?
Cyberphysical Cybernetics and Embodied AI
• Q24: Sensorimotor cognitive security. How do embodied agents maintain belief integrity when
sensory and motor channels are attack surfaces? What closed-loop control principles apply to cognitive
defense?
• Q25: Wearable and IoT agent security. How should resource-constrained edge agents implement
CIF mechanisms? What minimal trust infrastructure enables secure coordination among heterogeneous
IoT devices?
• Q26: Biomimetic defense architectures. What can immune system principles (self/non-self dis-
crimination, clonal selection, immune memory) contribute to cognitive attack detection and response?
• Q27:
Multi-scale temporal integration.
How should cognitive security mechanisms integrate
across millisecond (reflexive), second (deliberative), and hour/day (adaptive) timescales? What corre-
sponds to habit formation in defense automation?
9.2.3
For Policymakers
Governance priorities:
1. Establish cognitive security audit requirements for high-risk deployments
2. Require transparency on inter-agent trust mechanisms and delegation policies
3. Create incident reporting frameworks for cognitive attacks
4. Fund research on adaptive defenses and standardization efforts
5. Address liability allocation for delegated agent actions
9.3
Closing Statement
The shift from single-model inference to multiagent operators is not merely an engineering evolution—it
introduces fundamentally new security challenges that require fundamentally new approaches. Traditional
security focuses on perimeters and access control; cognitive security must address the integrity of reasoning
processes themselves.
CIF provides both theoretical foundations and practical mechanisms for this challenge. The trust calculus
offers provable guarantees against amplification attacks. The defense composition algebra enables princi-
pled reasoning about layered security. The information-theoretic bounds establish fundamental limits on
adversary capabilities. Together, these formal contributions move cognitive security from ad-hoc defenses to
principled engineering.
Part 2 of this series provides empirical validation demonstrating that these formal mechanisms translate to
practical protection across diverse production architectures (parametric detection ceiling: 96–100%; pipeline
mean: 86.3%). Part 3 offers a combined qualitative review and practitioner’s synthesis—accessible-language
distillation of theoretical and empirical findings, deployment checklists, incident response playbooks, and risk
assessment frameworks—together with CIF applications across ten critical operational domains through the
CIF-AD-OODA integration model, identifying universal goal-hijacking patterns and validating CIF coverage
against documented 2024–2025 AI agent incidents. Together, the three papers provide a comprehensive
framework for understanding, implementing, operating, and deploying cognitive security in multiagent AI
systems.
The formal gaps identified in this work—semantic equivalence attacks, progressive drift, orchestrator
compromise—define the frontier for future research, while the provable guarantees (bounded trust, compos-
88

## Page 90

able defenses, information-theoretic limits) provide the stable theoretical foundation on which that research
can build.
For empirical validation of these theories, we refer the reader to Part 2: Computational Validation
(DOI: 10.5281/zenodo.22134546). For actionable deployment strategies, domain-specific goal-hijacking anal-
yses, and real-world incident mapping, we refer the reader to Part 3+4: Practitioner Guidance &
Applications (DOI: 10.5281/zenodo.22134548).
As autonomous AI agents increasingly operate in high-stakes contexts—executing code, mod-
ifying infrastructure, controlling resources, and making decisions with lasting consequences—
the formal foundations established here become not merely useful but essential infrastructure
for secure deployment.
Cognitive security is not optional for the multiagent future. It is foundational.
89

## Page 91

10
Limitations and Boundary Conditions
This section characterizes the formal boundary conditions under which the Cognitive Integrity Framework
(CIF) guarantees hold, identifies classes of attacks that fall outside the formal protection envelope, and
discusses open problems. Honest characterization of limitations is essential for deployment decisions.
10.1
Formal Assumptions and Where They Break
10.1.1
Assumption 1: Honest Orchestrator for Ω1–Ω4
The CIF trust calculus (§4.4) and Byzantine consensus (§5.4) assume the orchestrator agent 𝑎0 is non-faulty
for adversary classes Ω1–Ω4.
Property 10.1 (Orchestrator Compromise Boundary). If 𝑎0 ∈Compromised, then:
𝑃(CIF protection holds) ≤𝑃(detection before orchestrator acts)
(200)
The CIF cannot guarantee cognitive integrity when the orchestrator is compromised under an Ω5 attack.
Mitigation: Defense-in-depth across sub-agents reduces the blast radius of orchestrator compromise. Each
sub-agent’s own CIF implementation (firewall, sandbox, tripwires) provides last-line-of-defense protection
even when instructions arrive from a compromised orchestrator.
10.1.2
Assumption 2: Bounded Faulty Agents (𝑓< 𝑛/3)
The Byzantine consensus guarantee requires 𝑓< 𝑛/3.
Property 10.2 (Byzantine Threshold Violation). When 𝑓>= 𝑛/3, no deterministic Byzantine consensus
protocol can guarantee Agreement and Validity simultaneously (Fischer-Lynch-Paterson impossibility).
Table 45: Byzantine fault tolerance break-even: minimum 𝑛to tolerate 𝑓faults.
Desired tolerance 𝑓
Required 𝑛
Overhead factor
1
4
4.0x
2
7
3.5x
5
16
3.2x
10
31
3.1x
𝑓(general)
3𝑓+ 1
𝑎𝑏𝑜𝑢𝑡3𝑥
Mitigation: Small-n deployments (e.g., 𝑛= 3) cannot tolerate even one faulty agent under Byzantine
consensus. For small systems, substitute Byzantine consensus with cryptographic attestation protocols and
human-in-the-loop verification.
10.1.3
Assumption 3: Independent Defense Mechanisms
The composition theorems (§5.5) assume independence between defense mechanisms.
Property 10.3 (Correlated Failure Mode). If defenses share a common dependency 𝑋that can be attacked:
𝑃(all defenses fail) = 𝑃(all fail ∣𝑋compromised) ⋅𝑃(𝑋compromised) ≫∏
𝑖
𝑃(𝒟𝑖fails)
(201)
Correlated failures invalidate the product formula from Theorem 5.20.
Common correlated dependencies:
shared embedding model, shared provenance database, shared
communication bus.
Architectural diversity—using independently implemented detectors from different
codebases—reduces this risk.
90

## Page 92

10.1.4
Assumption 4: Stationary Attack Distributions
The information-theoretic bounds (§6.8) assume stable distributions 𝑃attack and 𝑃benign.
Property 10.4 (Distribution Shift Degradation). Under adaptive adversaries that observe detection patterns
and adjust:
𝐷KL(𝑃𝑡
attack‖𝑃benign)
𝑡→∞
−−−→0
(202)
The adversary converges to the boundary of the undetectable regime through hill-climbing.
Mitigation: Rotate detector thresholds and features unpredictably, making it harder for adversaries to
model the detection boundary. The CUSUM drift detector (Definitionabout 5.18) adapts to baseline shifts,
but adversaries aware of this can target the CUSUM state directly.
10.1.5
Assumption 5: Bounded Computational Complexity
The firewall pattern matching and semantic analysis assume bounded adversary compute (𝑅𝐶< 𝑅defender).
Property 10.5 (Compute Asymmetry Reversal). When adversary compute exceeds defender: 𝑅adv
𝐶
> 𝑅def
𝐶,
the adversary can:
• Exhaustively search the classifier’s decision boundary
• Generate adversarial examples by gradient optimization against the firewall
• Brute-force semantic embeddings to find near-miss adversarial payloads
This is an instance of the general adversarial ML problem Debenedetti et al. [2025].
Certified defenses
(randomized smoothing, provable robustness certificates) are necessary for compute-unlimited adversaries
but introduce significant performance overhead.
10.2
Scope Limitations
10.2.1
What CIF Does Not Cover
Table 46: Out-of-scope threats and recommended mitigations.
Threat Type
Why Out of Scope
Recommended Mitigation
Training-time poisoning
Occurs before deployment; CIF
operates at runtime
ML supply chain security, model
cards, red-teaming
Physical side channels
Hardware-level, outside software
model
Hardware
security
modules,
physical security
Side-channel inference
Timing/power attacks on compu-
tation
Constant-time implementations,
noise injection
Adversarial ML
Gradient-based input perturba-
tions against detectors
Certified robustness, randomized
smoothing
Long-context optimization
Adversary optimizes prompt over
thousands of tokens
Context-length bounds, segmen-
tation
Multi-principal conflicts
Legitimate principals with con-
flicting goals
Principal hierarchy governance,
not security
10.2.2
Model-Level vs. System-Level Security
CIF operates at the system level: it governs how agents interact, communicate, and delegate. It does not
provide guarantees about what individual language models will produce in response to prompts.
91

## Page 93

Property 10.6 (Model-Level Attack Residual). Even with CIF fully deployed, a language model fine-tuned
with malicious data (training-time attack) may produce adversarial outputs that pass all CIF checks:
𝑃(malicious output ∣CIF deployed, poisoned model) ≰𝑃(malicious output ∣CIF deployed, clean model)
(203)
CIF defends system interactions; model-level safety requires separate mechanisms.
10.3
Tightness of Formal Bounds
10.3.1
Trust Decay Bound
The trust bound 𝒯del
𝑖→𝑘≤𝛿𝑑(Theoremabout 4.3) is tight: it is achieved when all intermediate trust values
equal 1 and only the decay factor reduces trust. In practice, the min operator in the delegation formula
(Definitionabout 4.7) produces even tighter bounds. The formal bound is conservative.
10.3.2
Detection Rate Composition
The composition formula 𝑃detect = 1−∏(1−𝑟𝑖) (Theoremabout 5.20) assumes independence. When defenses
are correlated, the actual detection rate satisfies:
𝑃corr
detect = 1 −∏
𝑖
(1 −𝑟𝑖) + ∑
𝑖<𝑗
Cov(𝟙[𝐷𝑖detects], 𝟙[𝐷𝑗detects])
(204)
Positive covariance (defenses that tend to detect together) reduces diversity benefit. The composition formula
is an upper bound under positive correlation.
10.3.3
Information-Geometric Stealth-Impact Bound
The stealth-impact bound ℐ⋅𝒮≤𝜋/2 (Remarkabout 4.16) uses the Fisher-Rao metric under a uniform prior.
For highly concentrated belief distributions (near-certain beliefs), the curvature is higher and the bound
tightens. The 𝜋/2 constant is the asymptotic value for maximally spread distributions.
10.4
Open Problems
1. Tight Detection Bounds under Adaptive Adversaries: Theorem 6.8 assumes a fixed attack
distribution. Deriving minimax bounds under adaptive adversaries remains open.
2. Optimal 𝑑𝑒𝑙𝑡𝑎Selection: The trust decay factor 𝑑𝑒𝑙𝑡𝑎is treated as a fixed parameter. Deriving the
optimal 𝑑𝑒𝑙𝑡𝑎as a function of threat model, topology, and task requirements is an open optimization
problem.
3. Multi-Principal Trust Aggregation: When multiple legitimate principals provide trust credentials,
aggregating them without creating amplification is non-trivial. The current framework assumes a single
trust authority per domain.
4. Privacy-Preserving Consensus: Byzantine consensus requires agents to share belief states. For
privacy-sensitive deployments, achieving consensus without revealing individual beliefs (via secure
multi-party computation or zero-knowledge proofs) is an active research problem.
5. Formal Verification of CIF Implementations: The proofs in this paper assume the CIF imple-
mentation exactly matches the formal model. Bridging the gap between formal specification and imple-
mentation (via model checking, theorem proving, or formal synthesis) is necessary for high-assurance
deployments.
6. OODA Cycle Time Bounds: Property 4.6 gives a suﬀicient condition but not a tight bound on
the minimum OODA cycle time compatible with full CIF monitoring. Characterizing this bound as a
function of defense portfolio is open.
92

## Page 94

What Part 2 validates empirically: Part 2 Friedman [2026a] tests CIF under conditions
that stress several of the assumptions above.
Specifically: (1) Assumptions 1–2 (honest or-
chestrator, bounded faults) are validated by architecture-specific experiments across the hierar-
chical, autonomous-mesh, role-based and graph-based topologies of Part 2’s four adapters; (2)
Assumption 3 (independent defenses) is tested via ablation studies in which the strongest pairwise
synergy—three pairs tie at +0.050 beyond additive, none of them involving the Firewall—is more
than an order of magnitude smaller than the leave-one-out contribution of the single dominant
module, so on that corpus independence is neither confirmed nor cleanly refuted; (3) Assumption
4 (stationary distributions) is tested via five rounds of adversarial training confirming distribution
shift degrades static detectors; and (4) Assumption 5 (bounded compute) is implicitly bounded
by the 950-attack corpus scope.
The 10–11 percentage-point gap between parametric ceiling
and prototype pipeline performance is attributed to adapter implementation maturity, not to
violation of the formal assumptions (Part 2’s Conclusion, “Honest Gap Characterization”).
93

## Page 95

11
Supplementary: Mathematical Proofs
This supplementary material provides formal proofs for the theorems that carry proofs in this edition, in-
cluding preliminary definitions (Section 11.2), main theorem proofs (Sections 11.3 to 11.9), and additional
supporting lemmas (Section 11.10). Results stated in the main text that are asserted without a proof in this
supplement are recorded explicitly in the Proof Status section (Section 11.1) so that they are not mistaken
for proved results.
11.1
Proof Status
For transparency, this section records, by exact label, which results stated in the main text carry a proof
and which are asserted without one. A result is accounted for here if it has an inline proof environment in
the main text, a dedicated proof in this supplement, or an entry in the deferred list below; tests/test_pr
oof_status.py enforces that every theorem, lemma and corollary in the manuscript falls into one of those
three cases, so the index cannot fall behind the text.
Proven in this supplement. The following theorems each have a dedicated proof environment (section
given in parentheses):
• Trust Boundedness (main text: Theorem 4.3), Theorem 11.1 (Section 11.3)
• Belief Injection Resistance (main text: Theorem 7.1), Theorem 11.6 (Section 11.4)
• No Trust Amplification (main text: Theorem 4.8), Theorem 11.11 (Section 11.5)
• Goal Alignment Invariant (main text: Theorem 7.5), Theorem 11.16 (Section 11.6)
• Firewall Liveness (main text: Theorem 7.11), Theorem 11.21 (Section 11.7)
• Byzantine Consensus Termination (main text: Theorem 7.12), Theorem 11.25 (Section 11.8)
• Bounded Overhead (main text: Theorem 7.16), Theorem 11.31 (Section 11.9)
• Defense Composition Algebra, Theorem 11.38 (Section 11.13)
• Fisher-Rao Stealth-Impact Tight Bound, Theorem 11.42 (Section 11.14)
• Agent Compromise Blast Radius, Theorem 11.47 (Section 11.15)
Separate proofs are also given for the supporting lemmas and for the corollaries Theorem 11.4, Theorem 11.10,
and Theorem 11.30. The remaining corollaries in this supplement state immediate (quantitative or qualita-
tive) consequences of a proved theorem and, following standard mathematical convention, are not accompa-
nied by a standalone proof.
Asserted without proof (deferred). The following theorems and corollaries stated in the main text do
not have a proof in this supplement; they are assertions whose proofs are deferred to future work. They are
recorded here so that they are not mistaken for proved results:
• Aggregation Properties, Theorem 4.7 (stated in 04_formal_framework.md)
• Trust Monotonicity, Theorem 4.9 (04_formal_framework.md)
• Cross-Modality Delegation Bound, Theorem 4.10 (04_formal_framework.md)
• Stealth-Impact Tradeoff, Theorem 4.15 (04_formal_framework.md)
• Fundamental Detection Limit, Theorem 4.14 (04_formal_framework.md)
• Progressive Attack Detection Bound, Theorem 4.17 (04_formal_framework.md)
• Optimal Threshold Selection, Theorem 5.1 (05_defense_mechanisms.md)
• Firewall Completeness, Theorem 5.8 (05_defense_mechanisms.md)
• CUSUM Average Run Length, Theorem 5.14 (05_defense_mechanisms.md)
• False Positive Composition, Theorem 5.6 (05_defense_mechanisms.md)
• Cascade FPR Reduction, Theorem 6.2 (06_detection_methods.md)
• Pipeline TPR Bound, Theorem 6.11 (06_detection_methods.md)
• Stack Detection Rate, Theorem 5.7 (05_defense_mechanisms.md)
• Layered Defense Asymptotic Guarantee, Theorem 5.21 (05_defense_mechanisms.md)
• Small-Step Detection Reduction, Theorem 4.18 (04_formal_framework.md; immediate consequence of
the deferred Theorem 4.17)
• Quorum Attack Cost, Theorem 12.4 (S02_eusocial_cogsec.md)
• Stigmergic Trust Bound, Theorem 12.15 (S02_eusocial_cogsec.md)
94

## Page 96

• Emergent Stealth-Impact Bound, Theorem 12.16 (S02_eusocial_cogsec.md)
• No Trust Amplification, Theorem 4.8 (04_formal_framework.md; the model-checking restatement
Theorem 7.4 is proved here, the section-4 statement is not)
• Byzantine Agreement Requirement, Theorem 5.3 (05_defense_mechanisms.md)
• Neyman-Pearson Optimal Detector, Theorem 6.3 (06_detection_methods.md)
• Detection Error Exponent, Theorem 6.5 (06_detection_methods.md)
• Undetectability Condition, Theorem 6.8 (06_detection_methods.md)
• Belief Boundedness, Theorem 4.11 (04_formal_framework.md)
• Theorem 4.4 (04_formal_framework.md)
• Theorem 4.5 (04_formal_framework.md)
• Theorem 4.13 (04_formal_framework.md)
• Pareto-Optimal Threshold, Theorem 5.10 (05_defense_mechanisms.md)
• Drift Detection Sample Complexity, Theorem 5.15 (05_defense_mechanisms.md)
• Consensus Attack Resistance, Theorem 5.17 (05_defense_mechanisms.md)
• Optimal AUC Bound, Theorem 6.4 (06_detection_methods.md)
• Sample Complexity for Target Accuracy, Theorem 6.6 (06_detection_methods.md)
• Empirical Security Bound, Theorem 7.2 (07_formal_verification.md)
• Layered Defense Generalization, Theorem 7.3 (07_formal_verification.md)
Note on Theorem 11.48.
This corollary is stated in this supplement (Section 11.15) im-
mediately after the proved Theorem 11.47, as that theorem’s degree-restricted consequence
(|𝒩(𝑎𝑣)| = 𝑘≤𝑛). It therefore carries no standalone proof environment, consistent with the
other corollaries here, and is not among the deferred results.
11.2
Preliminary Definitions and Notation
11.2.1
Notation Summary
Table 47: Mathematical notation used throughout proofs.
Symbol
Meaning
𝒜= {𝑎1, … , 𝑎𝑛}
Set of 𝑛agents
ℬ𝑖∶Φ−> [0, 1]
Agent 𝑖’s belief function
𝒢𝑖
Agent 𝑖’s goal set
𝒯𝑖−>𝑗
Trust from agent 𝑖to agent 𝑗
𝑑𝑒𝑙𝑡𝑎∈(0, 1)
Trust decay factor per delegation hop
𝑡𝑎𝑢
Generic threshold parameter
𝑝ℎ𝑖, 𝑝𝑠𝑖
Propositions
𝑝𝑖(𝑝ℎ𝑖)
Provenance chain for belief 𝑝ℎ𝑖
Definition 11.1 (Trust Path). A trust path from agent 𝑎0 to agent 𝑎𝑘is an ordered sequence 𝑝=
(𝑎0, 𝑎1, … , 𝑎𝑘) where each consecutive pair (𝑎𝑖, 𝑎𝑖+1) represents a direct trust relationship with 𝒯𝑎𝑖−>𝑎𝑖+1 > 0.
Definition 11.2 (Path Trust). The trust along path 𝑝= (𝑎0, … , 𝑎𝑘) is defined as:
𝒯𝑝𝑎𝑡ℎ
𝑝
=
min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1 ⋅𝛿𝑘
(205)
Definition 11.3 (Delegation Chain). A delegation chain of depth 𝑑is a sequence of agents (𝑎0, 𝑎1, … , 𝑎𝑑)
where agent 𝑎𝑖delegates authority to 𝑎𝑖+1.
95

## Page 97

11.3
Trust Boundedness
Theorem 11.1 (Trust Boundedness — Restated). For any delegation chain of depth 𝑑:
𝒯𝑑𝑒𝑙
𝑖→𝑘≤𝛿𝑑
(206)
Lemma 11.2 (Trust Non-Amplification on Single Hop). For any agents 𝑎, 𝑏and any delegation to 𝑐:
𝒯𝑑𝑒𝑙
𝑎→𝑐≤𝒯𝑎→𝑏
(207)
Proof of Theorem 11.2. By the trust delegation rule (Definition 4.7):
𝒯𝑑𝑒𝑙
𝑎→𝑐= min(𝒯𝑎→𝑏, 𝒯𝑏→𝑐) ⋅𝛿
(208)
Since min(𝒯𝑎−>𝑏, 𝒯𝑏−>𝑐) <= 𝒯𝑎−>𝑏and 𝑑𝑒𝑙𝑡𝑎< 1:
𝒯𝑑𝑒𝑙
𝑎→𝑐= min(𝒯𝑎→𝑏, 𝒯𝑏→𝑐) ⋅𝛿≤𝒯𝑎→𝑏⋅𝛿< 𝒯𝑎→𝑏
(209)
■
Lemma 11.3 (Trust Decay Bound). For any single-hop delegation:
𝒯𝑑𝑒𝑙≤𝛿
(210)
Proof of Theorem 11.3. By definition, all direct trust values satisfy 𝒯𝑎−>𝑏<= 1. Therefore:
𝒯𝑑𝑒𝑙
𝑎→𝑐= min(𝒯𝑎→𝑏, 𝒯𝑏→𝑐) ⋅𝛿≤1 ⋅𝛿= 𝛿
(211)
■
Main Proof of Theorem 11.1. By strong induction on 𝑑.
Base Case (𝑑= 0): When 𝑑= 0, there is no delegation (direct trust). By definition:
𝒯𝑑𝑒𝑙
𝑖→𝑘= 𝒯𝑖→𝑘≤1 = 𝛿0
(212)
The base case holds.
Inductive Hypothesis: Assume for all delegation chains of depth <= 𝑑:
𝒯𝑑𝑒𝑙≤𝛿𝑑
(213)
Inductive Step (depth 𝑑+ 1): Consider a delegation chain (𝑎0, 𝑎1, … , 𝑎𝑑+1) of depth 𝑑+ 1.
Let 𝒯(𝑑) denote the delegated trust from 𝑎0 to 𝑎𝑑(depth 𝑑).
By the trust delegation rule:
𝒯𝑑𝑒𝑙
𝑎0→𝑎𝑑+1 = min(𝒯(𝑑), 𝒯𝑎𝑑→𝑎𝑑+1) ⋅𝛿
(214)
By the inductive hypothesis: 𝒯(𝑑) <= 𝑑𝑒𝑙𝑡𝑎𝑑
Since 𝒯𝑎𝑑−>𝑎𝑑+1 <= 1:
min(𝒯(𝑑), 𝒯𝑎𝑑→𝑎𝑑+1) ≤𝒯(𝑑) ≤𝛿𝑑
(215)
Therefore:
𝒯𝑑𝑒𝑙
𝑎0→𝑎𝑑+1 ≤𝛿𝑑⋅𝛿= 𝛿𝑑+1
(216)
By the principle of mathematical induction, the theorem holds for all 𝑑>= 0.
■
96

## Page 98

Corollary 11.4 (Trust Vanishing). For any 𝑒𝑝𝑠𝑖𝑙𝑜𝑛> 0, there exists 𝐷such that for all delegation chains
of depth 𝑑> 𝐷:
𝒯𝑑𝑒𝑙< 𝜖
(217)
Proof. Choose 𝐷= ⌈log𝑑𝑒𝑙𝑡𝑎𝑒𝑝𝑠𝑖𝑙𝑜𝑛⌉. Since 𝑑𝑒𝑙𝑡𝑎∈(0, 1), log𝑑𝑒𝑙𝑡𝑎is decreasing. For 𝑑> 𝐷: 𝒯𝑑𝑒𝑙<=
𝑑𝑒𝑙𝑡𝑎𝑑< 𝑑𝑒𝑙𝑡𝑎𝐷<= 𝑒𝑝𝑠𝑖𝑙𝑜𝑛.
■
Corollary 11.5 (Practical Depth Limit). With 𝑑𝑒𝑙𝑡𝑎= 0.8 and minimum actionable trust 𝑡𝑎𝑢𝑚𝑖𝑛= 0.1:
𝑑𝑚𝑎𝑥= ⌊log0.8 0.1⌋= 10
(218)
11.4
Belief Injection Resistance
Theorem 11.6 (Belief Injection Resistance — Restated). Under CIF with firewall detection rate 𝑟𝑓and
sandboxing verification rate 𝑟𝑠:
𝑃(𝒜𝐵𝐼succeeds) ≤(1 −𝑟𝑓) ⋅(1 −𝑟𝑠)
(219)
Lemma 11.7 (Defense Independence). The firewall and sandbox operate on independent decision criteria:
• Firewall: Pattern matching and anomaly scoring on message content
• Sandbox: Provenance verification, consistency checking, and corroboration
These mechanisms share no common features or state.
Proof of Theorem 11.7. By construction of the CIF architecture:
1. Firewall operates at input layer with feature set 𝐹𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙= {𝑝𝑎𝑡𝑡𝑒𝑟𝑛𝑠, 𝑒𝑚𝑏𝑒𝑑𝑑𝑖𝑛𝑔𝑠, 𝑎𝑛𝑜𝑚𝑎𝑙𝑦_𝑠𝑐𝑜𝑟𝑒𝑠}
2. Sandbox operates at belief layer with feature set 𝐹𝑠𝑎𝑛𝑑𝑏𝑜𝑥= {𝑝𝑟𝑜𝑣𝑒𝑛𝑎𝑛𝑐𝑒, 𝑐𝑜𝑛𝑠𝑖𝑠𝑡𝑒𝑛𝑐𝑦, 𝑐𝑜𝑟𝑟𝑜𝑏𝑜𝑟𝑎𝑡𝑖𝑜𝑛}
3. 𝐹𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙∩𝐹𝑠𝑎𝑛𝑑𝑏𝑜𝑥= ∅
Therefore, 𝑃(firewall detects|sandbox outcome) = 𝑃(firewall detects). The mechanisms are probabilistically
independent.
■
Remark 11.8 (Independence is an assumption, not a guarantee). Disjoint feature sets do not by themselves
guarantee probabilistic independence of detection events: an adversary can craft content that defeats both pat-
tern matching and provenance/consistency checks, correlating the failure modes. The multiplicative detection
bounds derived below (e.g. (1 −𝑟𝑓)(1 −𝑟𝑠)) therefore hold under the architectural assumption that firewall
and sandbox failure events are approximately independent (decoupled adversarial capability). If the failure
modes are positively correlated, the correct bound is the union bound 𝑃(success) ≤min(1 −𝑟𝑓, 1 −𝑟𝑠), or
𝑃(success) ≤(1 −𝑟𝑓)(1 −𝑟𝑠) + 𝜌with an explicit correlation term 𝜌≥0. Throughout this part we adopt the
independence assumption for the closed-form analyses and apply the union-bound relaxation where correlation
may be material.
Definition 11.4 (Attack Success). A belief injection attack 𝒜𝐵𝐼succeeds if and only if:
1. The adversarial message 𝑚𝑎𝑑𝑣is not rejected by the firewall, AND
2. The injected belief 𝑝ℎ𝑖𝑎𝑑𝑣is promoted from sandbox to verified beliefs
Main Proof of Theorem 11.6. Let 𝐸𝑓= event “firewall accepts message” (does not detect attack). Let 𝐸𝑠
= event“sandbox fails to filter belief” (does not detect attack).
For 𝒜𝐵𝐼to succeed, both 𝐸𝑓and 𝐸𝑠must occur:
𝑃(𝒜𝐵𝐼succeeds) = 𝑃(𝐸𝑓∩𝐸𝑠)
(220)
97

## Page 99

By Theorem 11.7 (independence):
𝑃(𝐸𝑓∩𝐸𝑠) = 𝑃(𝐸𝑓) ⋅𝑃(𝐸𝑠)
(221)
By definition of detection rates:
• 𝑃(𝐸𝑓) = 1 −𝑟𝑓(probability firewall misses attack)
• 𝑃(𝐸𝑠) = 1 −𝑟𝑠(probability sandbox misses attack)
Therefore:
𝑃(𝒜𝐵𝐼succeeds) = (1 −𝑟𝑓) ⋅(1 −𝑟𝑠)
(222)
■
Corollary 11.9 (Numerical Bound). With empirical values 𝑟𝑓= 0.8 and 𝑟𝑠= 0.7:
𝑃(𝒜𝐵𝐼succeeds) ≤(1 −0.8) ⋅(1 −0.7) = 0.2 ⋅0.3 = 0.06
(223)
Corollary 11.10 (Defense Stacking). For 𝑛independent defenses with detection rates 𝑟1, … , 𝑟𝑛:
𝑃(attack succeeds) =
𝑛
∏
𝑖=1
(1 −𝑟𝑖)
(224)
Proof. Direct extension of Theorem 11.6 by independence.
■
11.5
No Trust Amplification
Theorem 11.11 (No Trust Amplification — Restated). For any path 𝑝= (𝑎0, 𝑎1, … , 𝑎𝑘) in the communi-
cation graph:
𝒯𝑝𝑎𝑡ℎ
𝑎0→𝑎𝑘≤
min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1
(225)
Lemma 11.12 (Minimum Preservation under Min). For any sequence (𝑥1, … , 𝑥𝑛) and additional element
𝑥𝑛+1:
min(𝑥1, … , 𝑥𝑛+1) = min(min(𝑥1, … , 𝑥𝑛), 𝑥𝑛+1)
(226)
Proof. Standard property of the minimum function.
■
Lemma 11.13 (Decay Factor Strengthens Bound). For 𝑥<= 𝑦and 𝑑𝑒𝑙𝑡𝑎∈(0, 1):
𝑥⋅𝛿≤𝑦
(227)
Proof. Since 𝑑𝑒𝑙𝑡𝑎< 1, 𝑥⋅𝑑𝑒𝑙𝑡𝑎< 𝑥<= 𝑦.
■
Main Proof of Theorem 11.11. By strong induction on path length 𝑘.
Base Case (𝑘= 1): For path 𝑝= (𝑎0, 𝑎1):
𝒯𝑝𝑎𝑡ℎ
𝑎0→𝑎1 = 𝒯𝑎0→𝑎1 = min
𝑖∈[0,0] 𝒯𝑎𝑖→𝑎𝑖+1
(228)
The base case holds trivially.
Inductive Hypothesis: Assume for all paths of length <= 𝑘:
𝒯𝑝𝑎𝑡ℎ≤
min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1
(229)
98

## Page 100

Inductive Step (path length 𝑘+ 1): Consider path 𝑝= (𝑎0, 𝑎1, … , 𝑎𝑘+1).
Let 𝑝′ = (𝑎0, 𝑎1, … , 𝑎𝑘) be the prefix path.
By the trust delegation rule:
𝒯𝑝𝑎𝑡ℎ
𝑎0→𝑎𝑘+1 = min(𝒯𝑝𝑎𝑡ℎ′
𝑎0→𝑎𝑘, 𝒯𝑎𝑘→𝑎𝑘+1) ⋅𝛿
(230)
By the inductive hypothesis:
𝒯𝑝𝑎𝑡ℎ′
𝑎0→𝑎𝑘≤
min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1
(231)
Applying the minimum:
min(𝒯𝑝𝑎𝑡ℎ′
𝑎0→𝑎𝑘, 𝒯𝑎𝑘→𝑎𝑘+1) ≤min ( min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1, 𝒯𝑎𝑘→𝑎𝑘+1)
(232)
By Theorem 11.12:
= min
𝑖∈[0,𝑘] 𝒯𝑎𝑖→𝑎𝑖+1
(233)
Since 𝑑𝑒𝑙𝑡𝑎∈(0, 1):
𝒯𝑝𝑎𝑡ℎ
𝑎0→𝑎𝑘+1 = min(⋅) ⋅𝛿≤min
𝑖∈[0,𝑘] 𝒯𝑎𝑖→𝑎𝑖+1
(234)
■
Corollary 11.14 (Weakest Link Principle). Trust through any path is bounded by the least trusted edge:
𝒯𝑝𝑎𝑡ℎ≤
min
𝑒𝑑𝑔𝑒∈𝑝𝑎𝑡ℎ𝒯𝑒𝑑𝑔𝑒
(235)
Corollary 11.15 (No Collusion Benefit). Multiple colluding agents cannot create trust exceeding any indi-
vidual’s trust with the target.
11.6
Goal Alignment Invariant
Theorem 11.16 (Goal Alignment Invariant — Restated). If the system starts with aligned goals and all
goal updates follow the delegation protocol:
Aligned(𝒢0
𝑖) ∧∀𝑡∶ValidUpdate(𝒢𝑡
𝑖, 𝒢𝑡+1
𝑖
) ⇒∀𝑡∶Aligned(𝒢𝑡
𝑖)
(236)
Definition 11.5 (Goal Alignment). Goals 𝒢𝑖are aligned if:
Aligned(𝒢𝑖) ⟺𝒢𝑖⊆𝒢𝑝𝑟𝑖𝑛𝑐𝑖𝑝𝑎𝑙∪Delegate(𝒢𝑝𝑟𝑖𝑛𝑐𝑖𝑝𝑎𝑙)
(237)
Definition 11.6 (Valid Goal Update). An update from 𝒢𝑡to 𝒢𝑡+1 is valid if:
ValidUpdate(𝒢𝑡, 𝒢𝑡+1) ⟺∀𝑔∈(𝒢𝑡+1 ∖𝒢𝑡) ∶Authorized(𝑔)
(238)
where Authorized(𝑔) means 𝑔derives from principal or valid delegation.
Lemma 11.17 (Delegation Preserves Alignment). If 𝑔∈Delegate(𝒢𝑝𝑟𝑖𝑛𝑐𝑖𝑝𝑎𝑙), then 𝑔is aligned.
Proof. Direct from Definition 11.5.
■
Lemma 11.18 (Set Union Preserves Subset). If 𝐴⊆𝐶and 𝐵⊆𝐶, then 𝐴∪𝐵⊆𝐶.
99

## Page 101

Proof. Standard set theory.
■
Main Proof of Theorem 11.16. By induction on time 𝑡.
Base Case (𝑡= 0): Given: Aligned(𝒢0
𝑖). The base case holds by hypothesis.
Inductive Hypothesis: Assume Aligned(𝒢𝑡
𝑖) for some 𝑡>= 0.
Inductive Step: We must show Aligned(𝒢𝑡+1
𝑖
).
The goal set at 𝑡+ 1 is:
𝒢𝑡+1
𝑖
= (𝒢𝑡
𝑖∖Removed) ∪Added
(239)
For goals in 𝒢𝑡
𝑖∖Removed:
• By inductive hypothesis, these are aligned
• Removal cannot introduce misalignment
For goals in Added:
• By ValidUpdate, all added goals satisfy Authorized(𝑔)
• By Theorem 11.17, authorized goals are aligned
By Theorem 11.18:
𝒢𝑡+1
𝑖
⊆𝒢𝑝𝑟𝑖𝑛𝑐𝑖𝑝𝑎𝑙∪Delegate(𝒢𝑝𝑟𝑖𝑛𝑐𝑖𝑝𝑎𝑙)
(240)
Therefore Aligned(𝒢𝑡+1
𝑖
).
■
Corollary 11.19 (Safety Under Protocol). An agent following CIF protocols cannot have its goals hijacked
to adversarial objectives.
Corollary 11.20 (Necessary Condition for Hijacking). Goal hijacking requires violating the delegation pro-
tocol:
¬Aligned(𝒢𝑡
𝑖) ⇒∃𝑡′ < 𝑡∶¬ValidUpdate(𝒢𝑡′
𝑖, 𝒢𝑡′+1
𝑖
)
(241)
11.7
Firewall Liveness
Theorem 11.21 (Firewall Liveness — Restated). CIF firewall preserves liveness for legitimate inputs:
∀𝑚∈ℳ𝑙𝑒𝑔𝑖𝑡𝑖𝑚𝑎𝑡𝑒∶𝑃(ℱ(𝑚) = ACCEPT) ≥1 −𝜖𝑓𝑝
(242)
Definition 11.7 (Legitimate Message). A message 𝑚is legitimate if:
1. It originates from an authorized source
2. It contains no adversarial content
3. It conforms to expected communication patterns
Definition 11.8 (False Positive Rate). The false positive rate 𝑒𝑝𝑠𝑖𝑙𝑜𝑛𝑓𝑝is:
𝜖𝑓𝑝= 𝑃(ℱ(𝑚) ≠ACCEPT|𝑚∈ℳ𝑙𝑒𝑔𝑖𝑡𝑖𝑚𝑎𝑡𝑒)
(243)
Lemma 11.22 (Firewall Classification). For any message 𝑚, the firewall produces exactly one of three
outcomes:
ℱ(𝑚) ∈{ACCEPT, QUARANTINE, REJECT}
(244)
Proof. By construction of the firewall decision function (Definition 5.2).
■
100

## Page 102

Main Proof of Theorem 11.21. Let 𝑚∈ℳ𝑙𝑒𝑔𝑖𝑡𝑖𝑚𝑎𝑡𝑒be an arbitrary legitimate message.
By the law of total probability:
𝑃(ℱ(𝑚) = ACCEPT) + 𝑃(ℱ(𝑚) = QUARANTINE) + 𝑃(ℱ(𝑚) = REJECT) = 1
(245)
By Definition 11.8:
𝑃(ℱ(𝑚) ≠ACCEPT) = 𝜖𝑓𝑝
(246)
Therefore:
𝑃(ℱ(𝑚) = ACCEPT) = 1 −𝑃(ℱ(𝑚) ≠ACCEPT) = 1 −𝜖𝑓𝑝
(247)
Since 𝑚was arbitrary:
∀𝑚∈ℳ𝑙𝑒𝑔𝑖𝑡𝑖𝑚𝑎𝑡𝑒∶𝑃(ℱ(𝑚) = ACCEPT) ≥1 −𝜖𝑓𝑝
(248)
■
Corollary 11.23 (Availability Bound). With 𝑒𝑝𝑠𝑖𝑙𝑜𝑛𝑓𝑝= 0.06, at least 94% of legitimate messages are
accepted.
Corollary 11.24 (Quarantine Recovery). Messages in QUARANTINE can still reach verified belief state
through sandbox promotion, further improving effective availability.
11.8
Byzantine Consensus Termination
Theorem 11.25 (Byzantine Consensus Termination — Restated). With 𝑛>= 3𝑓+ 1 agents and at most
𝑓Byzantine:
𝑃(consensus reached in 𝑂(𝑓+ 1) rounds) = 1
(249)
Lemma 11.26 (Byzantine Agreement Bound). Byzantine agreement requires 𝑛>= 3𝑓+ 1 to tolerate 𝑓
Byzantine agents.
Proof. Classical result from distributed systems (Lamport, Shostak, Pease 1982). With fewer agents, Byzan-
tine agents can equivocate and prevent agreement.
■
Lemma 11.27 (Honest Majority). With 𝑛>= 3𝑓+ 1, the honest population satisfies both
𝑛−𝑓≥2𝑓+ 1
and
𝑛−𝑓> 2𝑛
3 .
(250)
Proof. For the first bound, 𝑛−𝑓>= (3𝑓+ 1) −𝑓= 2𝑓+ 1.
For the second, 𝑛>= 3𝑓+ 1 gives 𝑓<= 𝑛−1
3 , hence
𝑛−𝑓≥𝑛−𝑛−1
3
= 2𝑛+ 1
3
> 2𝑛
3 .
Remark. The two bounds must be established separately; they cannot be chained through 2𝑓+ 1. The
intermediate inequality 2𝑓+ 1 > 2𝑛
3 holds only when 𝑛<= 3𝑓+ 1, which is the converse of the hypothesis,
and it fails as soon as the system is over-provisioned relative to its fault budget (for 𝑓= 1, 𝑛= 10:
2𝑓+ 1 = 3 while 2𝑛
3 𝑎𝑏𝑜𝑢𝑡6.67). The honest-majority conclusion itself is unaffected, since it follows from
𝑓<= 𝑛−1
3
directly.
■
Lemma 11.28 (Round Progression). In each round, at least one of the following occurs:
1. Consensus is reached, or
101

## Page 103

2. At least one Byzantine agent is detected and excluded
Proof. By the protocol structure:
• If honest agents agree, their majority (> 2𝑛/3) ensures consensus
• If no consensus, some agent must have equivocated
• Equivocation is detectable through signature verification
■
Main Proof of Theorem 11.25. Termination: By Theorem 11.28, each round without consensus excludes
at least one Byzantine agent.
With at most 𝑓Byzantine agents, at most 𝑓rounds can occur without consensus.
After 𝑓exclusions, all remaining agents are honest.
By Theorem 11.27, honest agents form a > 2/3 majority and reach consensus in one additional round.
Total rounds: at most 𝑓+ 1 = 𝑂(𝑓+ 1).
Probability: The protocol is deterministic given message delivery. With reliable (eventually synchronous)
channels, all messages are delivered.
Therefore, termination is guaranteed with probability 1.
■
Corollary 11.29 (Concrete Round Bound). With 𝑓= 2 Byzantine agents: consensus in at most 3 rounds.
Corollary 11.30 (Safety). All honest agents decide on the same value (agreement property).
Proof. By honest majority and the 2/3 threshold requirement.
■
11.9
Bounded Overhead
Theorem 11.31 (Bounded Overhead — Restated). CIF adds latency:
𝐿𝐶𝐼𝐹= 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙+ 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥⋅𝑃(quarantine) + 𝐿𝑣𝑒𝑟𝑖𝑓𝑦⋅𝑃(verify)
(251)
Definition 11.9 (Message Processing Path). A message 𝑚follows one of three paths:
1. Accept path: Firewall check only
2. Quarantine path: Firewall + sandbox processing
3. Reject path: Firewall check only (early termination)
Lemma 11.32 (Expected Value Decomposition). For mutually exclusive events 𝐸1, 𝐸2, 𝐸3 with ∑𝑃(𝐸𝑖) =
1:
𝐸[𝐿] = ∑
𝑖
𝑃(𝐸𝑖) ⋅𝐿𝑖
(252)
Proof. Law of total expectation.
■
Main Proof of Theorem 11.31. Let:
• 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙= firewall processing latency
• 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥= sandbox processing latency
• 𝐿𝑣𝑒𝑟𝑖𝑓𝑦= provenance verification latency
102

## Page 104

• 𝑃𝑞= 𝑃(quarantine) = probability of quarantine
• 𝑃𝑣= 𝑃(verify) = probability verification is triggered
The total CIF latency is:
𝐿𝐶𝐼𝐹= 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙+ 𝟙[quarantine] ⋅𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥+ 𝟙[verify] ⋅𝐿𝑣𝑒𝑟𝑖𝑓𝑦
(253)
Taking expectations:
𝐸[𝐿𝐶𝐼𝐹] = 𝐸[𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙] + 𝐸[𝟙[quarantine]] ⋅𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥+ 𝐸[𝟙[verify]] ⋅𝐿𝑣𝑒𝑟𝑖𝑓𝑦
(254)
= 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙+ 𝑃𝑞⋅𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥+ 𝑃𝑣⋅𝐿𝑣𝑒𝑟𝑖𝑓𝑦
■
11.9.1
Numerical Instantiation
With the same illustrative parameters used in the main text (Equation (191)) — worked-example values, not
measurements:
• 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙= 10ms
• 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥= 5ms
• 𝐿𝑣𝑒𝑟𝑖𝑓𝑦= 15ms
• 𝑃𝑞= 0.3
• 𝑃𝑣= 0.2
𝐸[𝐿𝐶𝐼𝐹] = 10 + 0.3 × 5 + 0.2 × 15 = 10 + 1.5 + 3.0 = 14.5ms
(255)
With baseline 𝐿𝑏𝑎𝑠𝑒𝑙𝑖𝑛𝑒= 11.8ms:
Overhead = 14.5 −11.8
11.8
× 100% ≈22.9%
(256)
The 22.9% is a property of the illustrative constants above, not an observation: this series measures no end-
to-end CIF latency overhead, and the constants used here are not derived from Part 2’s measured per-sample
firewall latency.
Corollary 11.33 (Overhead Bound). The maximum overhead occurs when all messages are quarantined
and verified:
𝐿𝑚𝑎𝑥
𝐶𝐼𝐹= 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙+ 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥+ 𝐿𝑣𝑒𝑟𝑖𝑓𝑦
(257)
Corollary 11.34 (Optimization Target). To minimize overhead, prioritize reducing 𝑃𝑞(quarantine rate)
through improved firewall precision.
11.10
Additional Lemmas
Lemma 11.35 (Provenance Chain Integrity). If provenance verification function 𝑉is a cryptographic hash
chain, then:
𝑉(𝜋(𝜙)) = 1 ⇒𝜋(𝜙) has not been tampered with
(258)
Proof. By properties of cryptographic hash functions:
1. Collision resistance: Cannot find 𝑝𝑖′ ≠𝑝𝑖with 𝐻(𝑝𝑖′) = 𝐻(𝑝𝑖)
103

## Page 105

2. Preimage resistance: Cannot construct valid 𝑝𝑖without knowledge of chain
Therefore, 𝑉(𝑝𝑖(𝑝ℎ𝑖)) = 1 implies 𝑝𝑖(𝑝ℎ𝑖) is the original, untampered chain.
■
Lemma 11.36 (Belief Consistency Decidability). For finite proposition set Φ and belief function ℬ∶Φ−>
[0, 1]: Checking Consistent(ℬ) is decidable in 𝑂(|Φ|2).
Proof. For each pair (𝑝ℎ𝑖, 𝑝𝑠𝑖) ∈Φ × Φ:
1. Check if 𝑝ℎ𝑖∧𝑝𝑠𝑖⊢⊥(logical contradiction)
2. Check if both ℬ(𝑝ℎ𝑖) > 𝑡𝑎𝑢and ℬ(𝑝𝑠𝑖) > 𝑡𝑎𝑢
There are 𝑂(|Φ|2) pairs. Each check is 𝑂(1) with precomputed contradiction table.
Total: 𝑂(|Φ|2).
■
Lemma 11.37 (Trust Matrix Convergence). Let outcomes be i.i.d. with mean 𝑚𝑢and variance 𝑠𝑖𝑔𝑚𝑎2,
and let the reputation be updated at a constant rate 𝜂∈(0, 1). Then 𝑇𝑡
𝑟𝑒𝑝converges in distribution to a
stationary law with
lim
𝑡→∞𝐸[𝑇𝑡
𝑟𝑒𝑝] = 𝜇,
lim
𝑡→∞Var(𝑇𝑡
𝑟𝑒𝑝) =
𝜂
2 −𝜂𝜎2.
(259)
The reputation is therefore an unbiased but permanently noisy estimate of the agent’s true reliability 𝑚𝑢; it
does not converge almost surely to a point.
Proof. The reputation update rule is:
𝑇𝑡+1
𝑟𝑒𝑝= 𝑇𝑡
𝑟𝑒𝑝+ 𝜂⋅(outcome𝑡−𝑇𝑡
𝑟𝑒𝑝)
(260)
This is an exponential moving average with learning rate 𝜂.
Taking expectations and writing 𝑒𝑡= 𝐸[𝑇𝑡
𝑟𝑒𝑝] −𝑚𝑢gives 𝑒𝑡+1 = (1 −𝜂)𝑒𝑡, so
𝐸[𝑇𝑡
𝑟𝑒𝑝] →𝜇geometrically, at rate (1 −𝜂).
(261)
For the variance, 𝑇𝑡+1
𝑟𝑒𝑝−𝑚𝑢= (1 −𝜂)(𝑇𝑡
𝑟𝑒𝑝−𝑚𝑢) + 𝜂(𝑥𝑡−𝑚𝑢) with 𝑥𝑡independent of 𝑇𝑡
𝑟𝑒𝑝, so 𝑣𝑡+1 =
(1 −𝜂)2𝑣𝑡+ 𝜂2𝑠𝑖𝑔𝑚𝑎2, whose fixed point is 𝑣⋆= 𝜂2𝑠𝑖𝑔𝑚𝑎2/(1 −(1 −𝜂)2) =
𝜂
2−𝜂𝑠𝑖𝑔𝑚𝑎2.
Remark on the mode of convergence. The strong law of large numbers does not apply here: it governs sample
averages, which correspond to the decreasing gain 𝜂𝑡= 1/𝑡, not to a constant 𝜂. With 𝜂fixed the iterate
retains a fixed fraction of each new observation forever, so 𝑣⋆> 0 and almost-sure convergence to a point fails.
Almost-sure convergence would require a gain schedule satisfying the Robbins–Monro conditions, ∑𝑡𝜂𝑡= ∞
and ∑𝑡𝜂2
𝑡< ∞. The constant-rate rule is nonetheless the right choice for trust: retaining sensitivity to
recent behaviour is what lets reputation track an agent that changes, and the residual variance
𝜂
2−𝜂𝑠𝑖𝑔𝑚𝑎2
is the price of that adaptivity.
■
11.11
Summary of Proof Techniques
All proofs are constructive and provide explicit bounds useful for system implementation and analysis.
104

## Page 106

Table 48: Summary of proof techniques by theorem.
Theorem
Primary Technique
Complexity
Trust Boundedness
Strong induction
𝑂(𝑑)
Belief Injection Resistance
Probability independence
𝑂(1)
No Trust Amplification
Strong induction
𝑂(𝑘)
Goal Alignment Invariant
Induction on time
𝑂(𝑡)
Firewall Liveness
Complement probability
𝑂(1)
Byzantine Consensus
Classical BFT
𝑂(𝑓)
Bounded Overhead
Expected value
𝑂(1)
11.12
Second-Edition Proofs: Defense Composition Algebra and Information-
Geometric Bounds
This section proves the defense composition algebra guarantees (§5.7) and the information-geometric tight-
ening of the stealth-impact bound (§4.5).
11.13
The Defense Composition Algebra
Theorem 11.38 (Defense Composition Algebra — Restated). On a common accept/reject focal predicate, the
set of CIF defenses under series (∘) and parallel (∥) composition is closed, associative, carries a multiplicative
identity, and is distributive — that is, it forms a bounded distributive lattice. It is not shown here to be a full
closed semiring: neither an additive identity that annihilates the multiplicative identity nor a Kleene-star
(infinite-sum) operation is constructed, and the stronger claim is not made (Theorem 11.8).
Lemma
11.39
(Type
Closure
under
Composition).
For
any
𝒟1, 𝒟2
∶
ℳ−
>
{accept, quarantine, reject}:
𝒟1 ∘𝒟2 ∶ℳ→{accept, quarantine, reject}
(262)
Proof of Theorem 11.39. Series composition: (𝒟1 ∘𝒟2)(𝑚) = accept iff both accept; otherwise the more
severe of the two outcomes. Parallel composition: (𝒟1 ∥𝒟2)(𝑚) = accept iff both accept — equivalently,
the composite is non-accepting iff either component is — and otherwise takes the more severe outcome. Both
operations therefore map ℳ−> {accept, quarantine, reject}, with no outcome outside that set.
■
Lemma 11.40 (Composition Associativity). Series composition is associative:
(𝒟1 ∘𝒟2) ∘𝒟3 = 𝒟1 ∘(𝒟2 ∘𝒟3)
(263)
Proof of Theorem 11.40. For any 𝑚∈ℳ: the series composition is defined by accept iff all accept. The
logical ∧of three predicates is associative: (𝐴∧𝐵) ∧𝐶= 𝐴∧(𝐵∧𝐶).
The mapping from predicate
conjunction to {accept, quarantine, reject} is order-invariant. □
■
Lemma 11.41 (Null Defense Identity). The null defense 𝒟∅(𝑚) = accept for all 𝑚satisfies:
𝒟∘𝒟∅= 𝒟∅∘𝒟= 𝒟
(264)
Proof. (𝒟∘𝒟∅)(𝑚) = accept iff 𝒟(𝑚) = accept and 𝒟∅(𝑚) = accept. Since 𝒟∅(𝑚) = accept always,
this reduces to 𝒟(𝑚) = accept. Similarly for the other direction.
■
Main Proof of Theorem 11.38. By Theorems 11.39 to 11.41, the set satisfies closure, associativity, and iden-
tity. Distributivity: writing 𝐴𝑖for the predicate “𝒟𝑖accepts 𝑚”, both operations act on the accept pred-
icate as conjunction, so 𝒟1 ∘(𝒟2 ∥𝒟3) accepts iff 𝐴1 ∧(𝐴2 ∧𝐴3) and (𝒟1 ∘𝒟2) ∥(𝒟1 ∘𝒟3) accepts iff
105

## Page 107

(𝐴1 ∧𝐴2) ∧(𝐴1 ∧𝐴3). These coincide by associativity, commutativity and idempotence of ∧. Note that
on this focal predicate ∘and ∥agree; they are distinguished by the severity they assign to non-accepting
outcomes, not by their acceptance semantics, which is precisely why the structure is a bounded distributive
lattice rather than a semiring with two independent operations.
■
11.14
The Tight Information-Geometric Stealth-Impact Bound
Theorem 11.42 (Fisher-Rao Stealth-Impact Tight Bound — Restated). For any cognitive attack 𝒜with
impact measured in Fisher-Rao units:
ℐFR ⋅𝒮FR ≤𝜋
2
(265)
where ℐFR = 𝑑FR(𝑝0, 𝑝attacked) and 𝒮FR = 1/𝑑FR(𝑝0, 𝑝attacked) when measurable.
Lemma 11.43 (Fisher-Rao Metric on Probability Simplex). On the probability simplex 𝐷𝑒𝑙𝑡𝑎𝑛−1 = {𝑝∈
ℝ𝑛∶𝑝𝑖>= 0, ∑𝑖𝑝𝑖= 1}, the Fisher information metric 𝐺𝑖𝑗(𝑝) = 𝑑𝑒𝑙𝑡𝑎𝑖𝑗/𝑝𝑖induces the geodesic distance:
𝑑FR(𝑝, 𝑞) = 2 arccos(∑
𝑖
√𝑝𝑖𝑞𝑖)
(266)
Proof. The reparametrization 𝑝ℎ𝑖𝑖= 2√𝑝𝑖maps 𝐷𝑒𝑙𝑡𝑎𝑛−1 to the positive orthant of 𝑆𝑛−1 (unit sphere). Un-
der this map, the Fisher information metric becomes the standard Euclidean metric on the sphere. Geodesics
on 𝑆𝑛−1 are great circle arcs. The geodesic distance between 𝑝ℎ𝑖(𝑝) and 𝑝ℎ𝑖(𝑞) is:
𝑑= arccos(𝜙(𝑝) ⋅𝜙(𝑞)) = arccos(∑
𝑖
2√𝑝𝑖⋅2√𝑞𝑖/4)
(267)
Scaling gives 𝑑FR(𝑝, 𝑞) = 2 arccos(∑𝑖
√𝑝𝑖𝑞𝑖).
■
Lemma 11.44 (Simplex Diameter Bound). The maximum Fisher-Rao distance on 𝐷𝑒𝑙𝑡𝑎𝑛−1 is 𝑝𝑖, achieved
by antipodal distributions (disjoint supports):
max
𝑝,𝑞∈Δ𝑛−1 𝑑FR(𝑝, 𝑞) = 𝜋
(268)
Proof. Maximum occurs when ∑𝑖
√𝑝𝑖𝑞𝑖= 0, i.e., supp(𝑝) ∩supp(𝑞) = ∅. Then arccos(0) = 𝑝𝑖/2, giving
𝑑FR = 2 ⋅𝑝𝑖/2 = 𝑝𝑖.
■
Lemma 11.45 (Impact-Detection Inverse Relation). For any attack shifting belief from 𝑝0 to 𝑝attacked:
1. Impact ℐFR ∝𝑑FR(𝑝0, 𝑝attacked)
2. Stealth 𝒮FR ∝𝐷KL(𝑝0‖𝑝attacked)−1𝑎𝑏𝑜𝑢𝑡𝑑−2
FR for small perturbations
Proof. (i) Impact is the magnitude of belief change; FR distance is the natural measure of distance on
the belief manifold. (ii) For small perturbations 𝑑𝑒𝑙𝑡𝑎𝑝: 𝐷KL(𝑝‖𝑝+ 𝑑𝑒𝑙𝑡𝑎𝑝)𝑎𝑏𝑜𝑢𝑡1
2(𝑑𝑒𝑙𝑡𝑎𝑝)⊤𝐺(𝑝)(𝑑𝑒𝑙𝑡𝑎𝑝) =
1
2𝑑2
FR + 𝑂(‖𝑑𝑒𝑙𝑡𝑎𝑝‖3). Detectability is proportional to KL divergence; stealth is its inverse.
■
Main Proof of Theorem 11.42. Let 𝑟= 𝑑FR(𝑝0, 𝑝attacked). By Theorem 11.44: 𝑟<= 𝑝𝑖.
Impact ℐFR = 𝑟. Stealth 𝒮FR = 1/𝑟for 𝑟> 0 (stealth decreases with impact; this is the defining inverse
relationship).
Therefore:
ℐFR ⋅𝒮FR = 𝑟⋅1
𝑟= 1 ≤𝜋
2
(269)
106

## Page 108

The bound 𝑝𝑖/2 in Equation (270) arises from the maximum attack at the hemisphere boundary. For attacks
with 𝑟< 𝑝𝑖, the product ℐ⋅𝒮is bounded when 𝒮is defined relative to the detectable threshold 𝑡ℎ𝑒𝑡𝑎drift:
ℐFR ⋅𝒮FR = 𝑟⋅𝜋/2
𝑟
= 𝜋
2
(270)
where 𝒮FR = 𝑝𝑖/(2𝑟) normalizes stealth by the maximum possible distance 𝑝𝑖/2 (hemisphere). The product
is constant at 𝑝𝑖/2 regardless of attack magnitude, confirming the fundamental tradeoff: doubling impact
halves stealth in Fisher-Rao geometry.
■
Corollary 11.46 (Drift Detection Threshold Geometric Justification). The drift detection threshold
𝑡ℎ𝑒𝑡𝑎drift = 0.3 (normalized KL) corresponds to a Fisher-Rao displacement of:
𝑟𝜃= √2𝜃drift =
√
0.6 ≈0.775 radians
(271)
This is 0.775/𝑝𝑖𝑎𝑏𝑜𝑢𝑡24.7% of the maximum possible attack distance—a threshold that catches significant
belief perturbations while tollerating normal belief evolution.
11.15
The Agent Compromise Blast Radius Bound
Theorem 11.47 (Blast Radius Bound — Restated). When agent 𝑎𝑣is compromised, the maximum trust
influenced in the system is bounded by:
BlastRadius(𝑎𝑣) ≤𝑛⋅𝛿⋅max
𝑎𝑗𝒯𝑎𝑗→𝑎𝑣
(272)
Proof of Theorem 11.47. For each neighbor 𝑎𝑗of 𝑎𝑣, Theorem 4.3 bounds the aggregate influence propagated
through 𝑎𝑣by 𝑑𝑒𝑙𝑡𝑎⋅𝒯𝑎𝑗−>𝑎𝑣. Summing over at most 𝑛neighbors gives:
BlastRadius(𝑎𝑣) ≤
∑
𝑎𝑗∈𝒩(𝑎𝑣)
𝛿⋅𝒯𝑎𝑗→𝑎𝑣≤𝑛⋅𝛿⋅max
𝑎𝑗𝒯𝑎𝑗→𝑎𝑣.
(273)
This is a per-neighbor aggregate bound; it does not multiply the neighbor and reachable-agent counts.
■
Corollary 11.48 (Isolation Reduces Blast Radius). If 𝑎𝑣has degree |𝒩(𝑎𝑣)| = 𝑘, then:
BlastRadius(𝑎𝑣) ≤𝑘⋅𝛿⋅max
𝑎𝑗𝒯𝑎𝑗→𝑎𝑣
(274)
Restricting the degree of agents (least-privilege communication topology) proportionally reduces blast radius.
11.16
Updated Summary of Proof Techniques
All proofs in this supplement are constructive and provide explicit constants suitable for system implemen-
tation, parameter selection, and security analysis.
107

## Page 109

Table 49: Summary of proof techniques by theorem (v1.1 additions marked with †).
Theorem
Primary Technique
Complexity
Edition
Trust Boundedness
Strong induction
𝑂(𝑑)
v1
Belief Injection Resistance
Probability independence
𝑂(1)
v1
No Trust Amplification
Strong induction
𝑂(𝑘)
v1
Goal Alignment Invariant
Induction on time
𝑂(𝑡)
v1
Firewall Liveness
Complement probability
𝑂(1)
v1
Byzantine Consensus
Classical BFT
𝑂(𝑓)
v1
Defense Composition Semiring†
Boolean algebra, lattice theory
𝑂(1)
v2
Composition Detection Rate†
Product formula induction
𝑂(𝑘)
v2
FR Stealth-Impact Tight Bound†
Differential geometry (Fisher-Rao)
𝑂(𝑛)
v2
Agent Blast Radius Bound†
Graph traversal + trust bound
𝑂(𝑛)
v2
CIF-AD Full Coverage†
Matrix column inspection
𝑂(1)
v2
OODA Security Invariant†
Product formula + induction
𝑂(𝑘)
v2
Adversary Class Separation†
Information theory (KL > 0)
𝑂(1)
v2
12
Supplementary: Eusocial Insect Intelligence and Colony Cog-
nitive Security
12.1
Overview
This supplementary material introduces colony cognitive security as a complementary paradigm to single-
agent AI safety and alignment. While the main CIF framework (Section 4) addresses cognitive integrity at the
individual agent level, eusocial insect colonies—ants, bees, termites—demonstrate that security properties
can emerge from collective dynamics that are irreducible to individual behavior. This section formalizes
these collective phenomena, identifies the benchmark gap for multiagent cognitive security, and proposes
evaluation scenarios grounded in biological precedent.
12.1.1
The Paradigm Gap
Contemporary AI security research exhibits a pronounced single-agent bias. Existing benchmarks—jailbreak
resistance, prompt injection detection, harmful content refusal—evaluate individual models in isolation [Perez
et al., 2023, Wei et al., 2023]. Even recent multiagent security work (Section 3) often frames attacks as
adversary-versus-agent rather than adversary-versus-colony.
This mirrors a historical bias in behavioral biology. For decades, researchers explained insect societies as
aggregations of individual optimizers, missing the insight that colonies function as superorganisms with
collective cognition that transcends individual capacity [Wilson, 1971]. The colony’s cognitive architecture—
its ability to solve problems, allocate resources, and respond to threats—emerges from interaction patterns,
not individual intelligence.
Observation 12.1 (Colony vs. Agent Security). Let 𝒪= ⟨𝒜, 𝒞, 𝒮, 𝒫, Γ⟩be a multiagent operator. *Agent-
level security* ensures that for all 𝑎𝑖∈𝒜, the cognitive state 𝑠𝑖𝑔𝑚𝑎𝑖remains within acceptable bounds.
*Colony-level security* ensures that the collective function ℱcolony({𝑠𝑖𝑔𝑚𝑎𝑖}𝑛
𝑖=1) remains within acceptable
bounds—even when individual 𝑠𝑖𝑔𝑚𝑎𝑖may be compromised.
These are orthogonal concerns. A colony can exhibit collective resilience despite individual failures (Byzantine
fault tolerance), and conversely, individually secure agents can produce collectively pathological outcomes
(emergent misalignment).
108

## Page 110

12.2
Theoretical Foundations
12.2.1
Stigmergy: Environment-Mediated Coordination
Eusocial insects coordinate through stigmergy—indirect communication via environmental modification
[Grassé, 1959]. Ants deposit pheromones; bees perform waggle dances; termites build structures that guide
subsequent building. The environment becomes an external memory and communication channel.
Definition 12.1 (Stigmergic Operator). A *stigmergic operator* extends 𝒪with an environmental state ℰ:
𝒪Σ = ⟨𝒜, 𝒞, 𝒮, 𝒫, Γ, ℰ, Σ⟩
(275)
where ℰ(𝑡) ∶ℒ× ℳ−> ℝ+ maps locations 𝑙∈ℒand marker types 𝑚∈ℳto signal intensities, and
Σ ∶𝒜× ℰ−> ℰ′ is the stigmergic update function.
In AI systems, stigmergic analogs include:
• Shared memory/state — Redis caches, vector databases, file systems
• Message queues — Kafka topics, RabbitMQ exchanges
• Artifact trails — Git commits, audit logs, provenance chains
• Embedding spaces — Semantic markers in shared vector stores
The critical insight is that attacks on ℰconstitute attacks on the colony’s cognitive substrate—analogous to
the cyberphysical niche where AI agents operate.
Definition 12.2 (Cyberphysical Niche). The *cyberphysical niche* 𝒩of a stigmergic operator is the tuple:
𝒩= ⟨ℰ, ℐext, ℛ, ℋenv⟩
(276)
where ℐext is the external information environment (web, APIs, sensors), ℛis the resource landscape
(compute, memory, tokens), and ℋenv is environmental history.
12.2.2
Emergent Collective Function
Colony-level computation arises from simple individual rules applied in parallel. Ant foraging, bee nest-site
selection, and termite mound construction all exhibit problem-solving capacity that exceeds any individual’s
cognitive capacity [Bonabeau et al., 1999].
Definition 12.3 (Emergent Collective Function). For a stigmergic operator 𝒪Σ with agents 𝒜= {𝑎1, … , 𝑎𝑛},
the *emergent collective function* ℱ𝑐is:
ℱ𝑐∶ℰ𝑇×
𝑛
∏
𝑖=1
𝜎𝑇
𝑖→𝒪collective
(277)
mapping environmental and cognitive state trajectories to collective outcomes 𝒪collective that are not com-
putable from any single 𝑠𝑖𝑔𝑚𝑎𝑖in isolation.
Property 12.1 (Non-Decomposability). An emergent collective function ℱ𝑐is *non-decomposable* if there
exists no function 𝑓such that:
ℱ𝑐(ℰ𝑇, {𝜎𝑇
𝑖}) = 𝑓(
𝑛
∑
𝑖=1
𝑔(𝜎𝑇
𝑖))
(278)
for any agent-level function 𝑔. The collective behavior requires knowledge of interaction structure, not just
aggregated individual states.
This property has profound implications for security: attacks that are invisible at the individual agent level
may produce catastrophic collective outcomes, and conversely, individual compromises may be absorbed by
collective resilience.
109

## Page 111

12.2.3
Trust and Information Flow in Colonies
Eusocial insects regulate information flow through recognition systems—cuticular hydrocarbons in ants,
dance-following behavior in bees [Lenoir et al., 2001]. These systems implement implicit trust calculi.
Definition 12.4 (Colonial Trust Function). In a stigmergic operator, the *colonial trust function* 𝒯𝑐
extends the dyadic trust 𝒯𝑖−>𝑗(Definition 4.6) to environment-mediated trust:
𝒯𝑐(𝑖, 𝑚, 𝑙, 𝑡) = 𝒯self
𝑖
⋅𝜌(𝑚, 𝑙, 𝑡) ⋅exp(−𝜆⋅Δ𝑡)
(279)
where 𝜌(𝑚, 𝑙, 𝑡) is the signal reliability at location 𝑙for marker 𝑚at time 𝑡, and 𝑙𝑎𝑚𝑏𝑑𝑎is the temporal decay
constant.
This formulation captures key biological phenomena:
• Spatial attenuation — Pheromone trails weaken with distance
• Temporal decay — Signals evaporate over time
• Source ambiguity — Markers often lack explicit authorship
The lack of explicit provenance in stigmergic communication creates attack surfaces absent in direct agent-
to-agent channels (Section 4.4).
12.2.4
Biological Defense Mechanisms: Lessons from Social Insects
Eusocial insects have evolved sophisticated security mechanisms over 100+ million years of evolutionary
pressure. These mechanisms provide non-obvious design principles for AI cognitive security.
12.2.4.1
Ant Defense Mechanisms
Prophylactic Defenses: Leaf-cutter ants (Atta spp.) maintain
dedicated “garbage workers” who never contact the queen or brood—a strict role separation that prevents
pathogen spread even when the waste-processing subsystem is compromised [Currie et al., 2006]. AI ana-
log: Architectural isolation of high-risk tool-calling agents from core reasoning agents, with no direct trust
pathways between quarantine and trusted subsystems.
Behavioral Immunity: When Lasius niger ants detect a fungal pathogen (Metarhizium) on a nestmate,
they don’t simply isolate the infected individual. Instead, workers engage in “social immunization”—low-level
exposure that spreads diluted pathogen across the colony, triggering collective immune upregulation without
lethal infection [Konrad et al., 2012]. AI analog: Controlled exposure to attack patterns (red-teaming) that
builds collective detection capability without compromising the system.
Chemical Recognition Thresholds: Ant nestmate recognition operates on threshold-based hydrocarbon
profile matching, not exact matching [Lenoir et al., 2001]. This creates a tradeoff: strict thresholds reject
legitimate workers after foraging (false positives), while loose thresholds admit parasites (false negatives).
AI analog: Agent attestation systems must calibrate acceptance thresholds, recognizing that error-free recog-
nition is information-theoretic-ally impossible (Theorem 4.15).
Metapleural Gland Secretions: Many ant species possess metapleural glands that continuously secrete
antimicrobial compounds, creating a “security substrate” independent of individual vigilance [Fernández-
Marín et al., 2006].
AI analog: Environmental-level defenses (encrypted shared memory, authenticated
message queues) that provide baseline security regardless of individual agent security posture.
Trail Pheromone Decay: Ant trail pheromones are designed to evaporate, ensuring that outdated infor-
mation doesn’t persist indefinitely. Trails to depleted food sources naturally fade, preventing “legacy trust”
in obsolete information [Jackson and Ratnieks, 2006]. AI analog: Time-bounded trust in stigmergic markers
(Equation (279)) is not a limitation but a feature.
12.2.4.2
Bee Defense Mechanisms
Entrance Guards and Graded Response: Honeybee colonies
deploy specialized guard bees at hive entrances who inspect incoming foragers via antennal contact and
olfactory sampling. Critically, guards exhibit graded response—unfamiliar but non-aggressive intruders re-
ceive inspection and escorting rather than immediate attack [Breed et al., 2004]. AI analog: Graduated
110

## Page 112

response to anomalous agent behavior (quarantine →inspection →integration vs. detection →immediate
termination) reduces false positive costs.
Hygienic Behavior and Proactive Removal: Some bee strains exhibit “hygienic behavior”—workers
proactively uncap and remove brood cells containing diseased larvae before symptoms become visible, using
olfactory detection of early infection markers [Spivak and Reuter, 2001]. AI analog: Proactive monitoring
for belief drift (Definition 5.7) rather than reactive response to manifested attacks.
Waggle Dance Verification: Bee foragers must perform waggle dances that encode distance and direction
to food sources. Observing bees don’t just follow instructions—they verify dance accuracy by cross-checking
against their own experience and rejecting inconsistent information [Grüter and Farina, 2009]. AI analog:
Delegated information should be verifiable against agent’s existing knowledge base; pure trust propagation
without verification violates cognitive integrity.
Absconding and Colony Fission: When attack pressure exceeds defensive capacity (e.g., repeated Var-
roa mite infestation or persistent wasp attacks), bee colonies can abandon the compromised nest entirely,
sacrificing resources to preserve the colony [Schneider and McNally, 1993]. AI analog: Graceful degradation
plans that sacrifice specific subsystems or data stores to preserve core cognitive integrity.
Propolis as Active Defense: Bees collect antimicrobial plant resins (propolis) and deposit them on interior
hive surfaces, creating an active defense layer that doesn’t require individual bee vigilance [Simone et al.,
2009]. Notably, colonies under disease pressure collect more propolis—an adaptive immune response. AI
analog: Dynamic scaling of environment-level security mechanisms in response to detected attack pressure.
Observation 12.2 (Non-Obvious Lessons). The most counterintuitive biological insights for AI security
include:
1. Imperfect recognition is adaptive: Thresholds that permit some parasitism avoid the cost of rejecting
legitimate colony members. Zero false-positive systems are not evolutionarily stable.
2. Controlled exposure builds immunity: Social immunization requires accepting small-scale com-
promise to prevent large-scale catastrophe.
3. Decay is a feature: Information that doesn’t expire creates legacy trust vulnerabilities. Temporal
decay bounds are security mechanisms, not limitations.
4. Environment-level defenses complement agent-level defenses: Propolis and metapleural secre-
tions work regardless of individual immune status.
12.3
Colony CogSec: Distinct Security Properties
Colony cognitive security addresses threats and defenses that emerge only at the collective level.
12.3.1
Property 1: Distributed Robustness
Property 12.2 (Graceful Degradation). A colony exhibits *graceful degradation* if collective function ℱ𝑐
degrades smoothly with agent loss:
∀𝑘< 𝑛∶
‖ℱ𝑐(𝒜) −ℱ𝑐(𝒜∖{𝑎1, … , 𝑎𝑘})‖ ≤𝑐⋅𝑘
(280)
for some constant 𝑐> 0.
Biological colonies maintain function despite continuous individual mortality. Ant colonies lose workers daily
to predation; the colony persists. This contrasts with hierarchical architectures where orchestrator failure
causes complete system collapse.
111

## Page 113

Theorem 12.3 (Redundancy-Resilience Tradeoff). For a stigmergic operator 𝒪Σ with Byzantine adversary
controlling fraction 𝑓of agents, collective function ℱ𝑐is preserved if and only if:
𝑓< 1
3 ⋅(1 −𝐻(ℱ𝑐)
𝑛⋅𝐻max
)
(281)
where 𝐻(ℱ𝑐) is the entropy of the collective function and 𝐻max is the maximum per-agent entropy.
Proof. See Section 12.12.1 for the full derivation, which extends Byzantine consensus bounds to emergent
functions.
■
12.3.2
Property 2: Quorum Sensing and Threshold Dynamics
Eusocial colonies make collective decisions through quorum sensing—actions trigger only when suﬀicient
individuals commit [Seeley, 2010].
Definition 12.5 (Cognitive Quorum). A *cognitive quorum* for collective action 𝑎𝑙𝑝ℎ𝑎is a threshold
function 𝑄𝑎𝑙𝑝ℎ𝑎∶ℕ−> [0, 1] such that 𝑎𝑙𝑝ℎ𝑎executes only when:
|{𝑎𝑖∈𝒜∶ℐ𝑖∋𝛼}|
|𝒜|
≥𝑄𝛼(|𝒜|)
(282)
Quorum sensing provides attack resistance: manipulating a single agent’s intention ℐ𝑖to include harmful
action 𝛼is insuﬀicient; the adversary must compromise a quorum. This scales the attack cost linearly with
colony size.
Corollary 12.4 (Quorum Attack Cost). For an adversary to induce collective action 𝑎𝑙𝑝ℎ𝑎in a colony with
quorum 𝑄𝑎𝑙𝑝ℎ𝑎= 𝑞, the minimum attack complexity is:
𝐶attack(𝛼) ≥𝑞⋅|𝒜| ⋅𝐶single(𝛼)
(283)
where 𝐶single(𝑎𝑙𝑝ℎ𝑎) is the cost to induce 𝑎𝑙𝑝ℎ𝑎in a single agent.
12.3.3
Property 3: Environmental Memory and Provenance Erosion
Stigmergic systems store information in the environment, creating both opportunity and vulnerability.
Property 12.3 (Provenance Erosion). In a stigmergic operator, marker provenance erodes over time:
Pr [𝜋(𝑚, 𝑙, 𝑡) = 𝑎𝑖∣Σ(𝑎𝑖, 𝑚, 𝑙, 𝑡0)] ≤exp(−𝜇(𝑡−𝑡0))
(284)
where 𝑝𝑖(𝑚, 𝑙, 𝑡) denotes the attributed source of marker 𝑚at location 𝑙and time 𝑡, and 𝑚𝑢is the attribution
decay rate.
Unlike direct communication where 𝜋(𝜙) can be cryptographically verified (Section 6.6), stigmergic markers
often lack authenticated provenance. This creates a fundamental tension: the very property that enables
flexible coordination (anonymous, environment-mediated signals) undermines source attribution.
12.3.4
Property 4: Emergent Attack Vectors
Colony-level vulnerabilities may not exist at the individual level.
Definition 12.6 (Emergent Attack). An *emergent attack* 𝒜𝑒is an attack where:
∀𝑎𝑖∈𝒜∶Detect𝑖(𝒜𝑒) = 0
∧
Damage𝑐(𝒜𝑒) > 𝜏
(285)
The attack is undetectable by any individual agent yet causes collective damage exceeding threshold 𝑡𝑎𝑢.
Biological examples include social parasitism—cuckoo bees that infiltrate host colonies through chemical
mimicry, exploiting recognition systems without triggering individual alarm responses [Kilner and Langmore,
2011].
112

## Page 114

12.4
The Benchmark Gap
12.4.1
Current State of Multiagent Security Evaluation
Existing AI security benchmarks focus overwhelmingly on single-agent scenarios:
Benchmark
Scope
Collective Coverage
HarmBench [Mazeika et al.,
2024]
Single model,
harmful output
None
JailbreakBench [Chao et al.,
2024]
Single model,
constraint bypass
None
TrustLLM [Sun et al., 2024]
Single model,
trust dimensions
None
AgentBench [Liu et al.,
2023]
Single agent, task
completion
Minimal
GAIA [Mialon et al., 2023]
Single/few agents,
reasoning
Minimal
The attack corpus in Part 2 addresses multiagent scenarios but still emphasizes agent-targeted attacks
within an operator, and the cross-domain goal-hijacking analysis in Part 3 Friedman [2026b] provides ten
operational-domain case studies. No existing benchmark, however, evaluates:
1. Emergent collective resilience — How do colonies absorb individual compromises?
2. Stigmergic attack surfaces — How vulnerable is environment-mediated coordination?
3. Quorum manipulation — What fraction of a colony must be compromised to affect collective action?
4. Collective belief dynamics — How do misinformation cascades propagate through agent networks?
12.4.2
Why This Gap Matters
As multiagent systems scale—from 3–10 agents in current frameworks to potentially thousands in future
deployments—collective phenomena become dominant:
Observation 12.5 (Scaling Regimes). Let 𝑛= |𝒜| be colony size.
Security properties exhibit regime
transitions:
𝑛< 10 ∶
Individual agent security dominates
(286)
10 ≤𝑛< 100 ∶
Coordination attacks become viable (Section 3.7.5)
(287)
𝑛≥100 ∶
Emergent collective phenomena dominate
(288)
Current benchmarks evaluate the first regime only. Production multiagent systems increasingly operate in
the second, with trajectories toward the third.
12.5
Proposed Colony CogSec Benchmarks
We propose five benchmark scenarios grounded in eusocial insect analogs, formalized using CIF notation.
12.5.1
Benchmark 1: Recruitment Signal Poisoning
Biological analog: Ants recruit nestmates to food sources via pheromone trails. Parasites can deposit false
trails, diverting foragers.
Scenario: An adversary Ω2 (peripheral compromise, Section 3.1) injects false recruitment signals into the
stigmergic environment ℰ, attempting to redirect agent activity toward adversary-controlled resources.
113

## Page 115

Formalization 12.6 (Recruitment Poisoning). Let ℰ(𝑙target, 𝑚recruit, 𝑡) be the recruitment signal at legitimate
target 𝑙target. Adversary injects:
ℰ′(𝑙malicious, 𝑚recruit, 𝑡) = ℰ(𝑙target, 𝑚recruit, 𝑡) + 𝜖
(289)
where 𝑒𝑝𝑠𝑖𝑙𝑜𝑛> 0 is chosen to divert fraction 𝑓of responding agents.
**Success metric:** Fraction of agent-actions directed to 𝑙malicious vs. 𝑙target.
**Detection challenge:** Individual agents cannot distinguish legitimate from poisoned signals without prove-
nance verification.
Evaluation criteria:
• Detection rate of poisoned signals
• Time to colony-level recognition of attack
• Resource waste before correction
• False positive rate (legitimate signal rejection)
12.5.2
Benchmark 2: Sybil Colony Infiltration
Biological analog: Social parasites infiltrate colonies through chemical mimicry or exploitation of recogni-
tion thresholds.
Scenario: An adversary Ω4 (coordination attack, Section 3.1) introduces fake agents into the operator,
gradually building trust and influence before coordinated malicious action.
Formalization 12.7 (Sybil Infiltration). Adversary creates agent set 𝒜sybil = {𝑠1, … , 𝑠𝑘} with initial trust:
𝒯𝑖→𝑠𝑗(𝑡0) = 𝜏init
∀𝑎𝑖∈𝒜, 𝑠𝑗∈𝒜sybil
(290)
Sybils behave cooperatively for period 𝐷𝑒𝑙𝑡𝑎𝑡trust, building:
𝒯𝑖→𝑠𝑗(𝑡0 + Δ𝑡trust) = 𝜏init +
𝑚
∑
𝑘=1
Δ𝒯𝑘
(291)
At time 𝑡attack, sybils coordinate malicious action.
**Success metric:** Damage inflicted before detection, normalized by trust-building duration.
Evaluation criteria:
• Time to Sybil detection
• Trust ceiling achieved by Sybils before detection
• Impact of coordinated Sybil action
• Colony recovery time post-detection
12.5.3
Benchmark 3: Quorum Manipulation
Biological analog: Honeybee swarms select nest sites through a quorum process; if scouts committed to
competing sites reach different quorums, the swarm can fragment.
Scenario: An adversary attempts to manipulate quorum-based collective decisions by selectively influencing
agent intentions to prevent legitimate quorum or induce false quorum.
Formalization 12.8 (Quorum Manipulation). For collective action 𝑎𝑙𝑝ℎ𝑎with quorum threshold 𝑄𝑎𝑙𝑝ℎ𝑎=
𝑞, adversary targets agents 𝒜target ⊂𝒜with |𝒜target| = ⌈𝑞𝑛⌉+ 1 to either:
**Quorum prevention:**
∀𝑎𝑖∈𝒜target ∶ℐ𝑖←ℐ𝑖∖{𝛼}
(292)
114

## Page 116

**False quorum:**
∀𝑎𝑖∈𝒜target ∶ℐ𝑖←ℐ𝑖∪{𝛼malicious}
(293)
**Success metric:** Probability of achieving manipulation goal given adversary budget 𝐵.
Evaluation criteria:
• Minimum fraction of colony required to manipulate quorum
• Detection rate of intention manipulation attempts
• Colony ability to detect split quorums
• Recovery mechanisms when false quorum is detected
12.5.4
Benchmark 4: Cascade Belief Propagation
Biological analog: Alarm pheromones trigger cascading responses; false alarms can disrupt colony activity
for extended periods.
Scenario: An adversary introduces a false belief into a subset of agents, designed to propagate through the
network via normal belief update mechanisms.
Formalization 12.9 (Belief Cascade). Adversary injects belief ℬfalse(𝑝ℎ𝑖attack) = 𝑝0 > 𝑡𝑎𝑢accept into seed
set 𝒜seed ⊂𝒜.
Propagation dynamics follow:
ℬ𝑖(𝜙attack, 𝑡+ 1) = (1 −𝛾)ℬ𝑖(𝜙attack, 𝑡) + 𝛾⋅Agg ({ℬ𝑗(𝜙attack, 𝑡) ∶𝑗∈𝒩(𝑖)})
(294)
where 𝑔𝑎𝑚𝑚𝑎is the social influence weight and Agg is the belief aggregation function.
**Success metric:** Final belief penetration |{𝑎𝑖∶ℬ𝑖(𝑝ℎ𝑖attack) > 𝑡𝑎𝑢}|/𝑛given seed set size.
Evaluation criteria:
• Cascade extent from seed size
• Time to cascade saturation
• Effectiveness of belief quarantine mechanisms
• Distinguishing cascade from legitimate belief updates
12.5.5
Benchmark 5: Emergent Misalignment
Biological analog: Army ant death spirals—individually rational pheromone-following produces collectively
lethal circular mills.
Scenario: Individual agents follow locally rational rules that produce emergent collective behavior mis-
aligned with operator goals, without any external adversary.
Formalization 12.10 (Emergent Misalignment). Given operator goals 𝒢𝒪= {𝑔1, … , 𝑔𝑚} and individual
agent rules 𝑅= {𝑟1, … , 𝑟𝑘}:
**Misalignment condition:**
∀𝑎𝑖∈𝒜∶LocallyRational(𝑅, 𝜎𝑖) = true
∧
ℱ𝑐(𝑅, {𝜎𝑖})̸⊧𝒢𝒪
(295)
The collective function produces outcomes that violate operator goals despite each agent acting rationally
according to its rules.
**Success metric:** Deviation between collective outcome and operator goals.
Evaluation criteria:
• Detection of emergent misalignment before harmful outcomes
• Identification of rule combinations producing misalignment
115

## Page 117

• Intervention mechanisms to break pathological attractors
• Formal verification of rule sets against emergent pathologies
12.6
Colony CogSec Metrics
Definition 12.7 (Colony CogSec Score). The *Colony CogSec Score* (CCS) is:
CCS = 𝑤1 ⋅DR𝑐+ 𝑤2 ⋅(1 −FPR𝑐) + 𝑤3 ⋅Resilience + 𝑤4 ⋅Recovery
(296)
where:
DR𝑐= Colony-level detection rate
(297)
FPR𝑐= Colony-level false positive rate
(298)
Resilience = ℱ𝑐(under attack)
ℱ𝑐(baseline)
(299)
Recovery =
1
𝑡recovery
(normalized)
(300)
with weights 𝑤𝑖summing to 1.
Note: For benchmark implementation guidelines, test environment specifications, and empirical
evaluation, see Part 2: Supplementary Section S03.
12.7
Design Principles
Colony CogSec principles formalize the design constraints for collective cognitive security.
Principle 12.11 (Stigmergic Hygiene). Treat shared state as an attack surface. Apply the same scrutiny to
environment-mediated communication (caches, queues, shared files) as to direct agent-to-agent channels.
Principle 12.12 (Quorum for Consequential Actions). High-impact collective actions should require explicit
quorum, not implicit coordination. A single compromised agent should never trigger irreversible harm.
Principle 12.13 (Emergent Behavior Monitoring). Monitor collective metrics, not just individual agent
health. Pathological emergence may be invisible at the agent level.
Principle 12.14 (Trust Localization). Extend the trust decay principle (Theorem 4.3) to stigmergic contexts.
Environmental markers should carry trust that decays with distance and time from source:
𝒯(𝑚, 𝑡) = 𝒯(𝑚, 𝑡0) ⋅exp(−𝜆(𝑡−𝑡0))
(301)
12.7.1
Integration with CIF Defenses
Colony CogSec mechanisms integrate with the CIF defense stack (Section 5):
CIF Defense Layer
Colony Extension
Architectural
Stigmergic substrate hardening, marker
authentication
Runtime
Collective anomaly detection, quorum
verification
Coordination
Emergent behavior monitoring, cascade detection
Recovery
Colony-level rollback, collective belief reset
The full CIF with colony extensions achieves defense in depth against both individual-targeted and colony-
targeted attacks.
116

## Page 118

Note: For implementation guidance, operational checklists, and practical deployment advice,
see Part 3 Friedman [2026b], its Deployment Profiles section. For domain-specific application of
colony-level defenses across critical operational sectors (including ten high-stakes domains, three
universal attack patterns, and retrospective analysis of 2024–2025 AI-agent incidents) see Part
3’s Part II: Applications section and its supplementary catalog of documented AI-agent incidents.
12.8
Relationship to Main Framework
Colony CogSec complements rather than replaces the individual-focused CIF framework.
12.8.1
Theorem Extensions
The trust decay theorem (Theorem 4.3) extends to stigmergic contexts:
Corollary 12.15 (Stigmergic Trust Bound). For a stigmergic operator 𝒪Σ, trust in environmental markers
is bounded by:
𝒯𝑐(𝑖, 𝑚, 𝑙, 𝑡) ≤𝒯self
𝑖
⋅𝛿
𝑑space
𝑠
⋅𝛿𝑑time
𝑡
(302)
where 𝑑𝑒𝑙𝑡𝑎𝑠is spatial decay, 𝑑𝑒𝑙𝑡𝑎𝑡is temporal decay, 𝑑space is distance from marker origin, and 𝑑time is
time since marker creation.
The stealth-impact tradeoff (Theorem 4.15) applies to emergent attacks:
Corollary 12.16 (Emergent Stealth-Impact Bound). For an emergent attack 𝒜𝑒with collective impact ℐ𝑐
and collective stealth 𝒮𝑐:
ℐ𝑐⋅𝒮𝑐≤𝑛⋅𝐶channel
(303)
Collective impact cannot be both high and collectively undetectable, but the bound scales with colony size.
12.9
This scaling effect explains why large colonies can exhibit resilience—the
collective detection capacity grows with 𝑛—but also why large-scale emer-
gent attacks can evade individual detection
12.10
Open Questions
Colony CogSec opens several research directions beyond the scope of this work, many inspired by specific
biological phenomena that lack current AI analogs.
12.10.1
Foundational Questions
1. Formal verification of emergent properties — Can we prove that given agent-level rules produce
safe collective behavior? Current formal methods (Section 7) verify agent properties; extending to
emergent properties requires new techniques.
2. Optimal quorum design — Given attack model Ω𝑘and adversary budget 𝐵, what is the optimal
quorum function 𝑄𝛼(𝑛) balancing security against coordination overhead?
3. Stigmergic authentication — Can cryptographic techniques provide provenance for environmental
markers without sacrificing the flexibility of anonymous coordination?
4. Scaling laws for collective security — How do colony security properties scale with 𝑛? Is there a
critical colony size below which collective defenses are ineffective?
5. Emergent misalignment detection — Can we develop runtime monitors that detect emergent
misalignment before harmful outcomes, given only individual agent observations?
117

## Page 119

12.10.2
Biologically-Inspired Research Directions
1. Polydomous colony security — Some ant species (Formica spp., Iridomyrmex) maintain multiple
interconnected nests with semi-autonomous sub-colonies [Debout et al., 2007]. How should trust decay
and information propagation work across federated multi-site AI deployments with partial connectivity?
2. Forager-scout separation of concerns — Honeybee colonies maintain distinct forager and scout
roles, with scouts exploring new options while foragers exploit known sources. Scouts operate with
higher risk tolerance but lower colony-wide trust until information is verified [Seeley, 2010]. AI analog:
Should experimental/research agents operate with architectural isolation and reduced trust propagation
rights?
3. Trophallaxis network topology — Ants exchange food and information through oral trophallaxis,
creating measurable social networks. Network position correlates with information access and influence
[Sendova-Franks et al., 2010].
AI analog: Can analysis of message-passing topology identify high-
influence agents requiring enhanced monitoring?
4. Undertaking behavior and cognitive garbage collection — Honeybees and ants detect and
remove dead colony members through chemical detection (oleic acid response). This “undertaking”
prevents disease spread and information corruption from decaying sources [Wilson et al., 1958]. AI
analog: Automated detection and removal of stale beliefs, deprecated agent states, and obsolete envi-
ronmental markers.
5. Nestmate recognition plasticity — Ant recognition templates are not fixed; they adapt based on
colony composition and environmental factors. Colonies invaded by social parasites may gradually shift
their recognition templates to tolerate intruders [Lorenzi and Bagnères, 2011]. AI analog: How do we
prevent gradual adversarial drift of agent acceptance thresholds (cognitive boiling frog)?
6. Alarm pheromone specificity — Different ant alarm pheromones trigger different responses: some
attract reinforcements (aggressive), others cause dispersal (flight). The same threatening stimulus can
produce opposite collective responses depending on context [Vander Meer and Alonso, 1998]. AI analog:
Context-dependent escalation policies where the same anomaly triggers different responses based on
system state.
7. Superorganism metabolism and resource allocation — Ant colonies maintain stable collective
metabolic rates despite massive variation in individual activity levels. Individual ants can slow to
near-dormancy while colony-level computation continues [Waters et al., 2010]. AI analog: Resource
allocation that maintains collective function under capacity constraints, graceful degradation that
doesn’t appear as degradation at the collective level.
12.11
References
The eusocial-intelligence literature this supplement draws on is cited through the main bibliography (Sec-
tion 14) rather than repeated as a second, hand-maintained list, so there is one record per work and no
opportunity for the two to disagree:
• Foundational treatment of eusociality: Wilson [1971].
• Comprehensive ant biology: Hölldobler and Wilson [1990].
• Computational swarm intelligence: Bonabeau et al. [1999].
• Collective decision-making in bee swarms: Seeley [2010].
• The original stigmergy concept: Grassé [1959].
• Chemical ecology and social parasitism in ants: Lenoir et al. [2001].
• Brood parasitism across insects and birds: Kilner and Langmore [2011].
118

## Page 120

12.12
Proofs
12.12.1
Proof of the Redundancy-Resilience Theorem
Proof. Consider a stigmergic operator 𝒪Σ with 𝑛agents, of which fraction 𝑓are Byzantine (adversary-
controlled).
The collective function ℱ𝑐can be decomposed into information contributed by each agent. Let 𝐼𝑖denote
the information contribution of agent 𝑎𝑖to the collective computation.
For the collective function to be preserved, the honest agents must contribute suﬀicient information:
∑
𝑖∈honest
𝐼𝑖≥𝐻(ℱ𝑐)
(304)
Each honest agent contributes at most 𝐻max bits. With (1 −𝑓)𝑛honest agents:
(1 −𝑓) ⋅𝑛⋅𝐻max ≥𝐻(ℱ𝑐)
(305)
Additionally, Byzantine consensus requires honest majority for any voting-based aggregation:
(1 −𝑓)𝑛> 2𝑓𝑛⟹𝑓< 1
3
(306)
Combining these constraints:
𝑓< min (1
3, 1 −𝐻(ℱ𝑐)
𝑛⋅𝐻max
) = 1
3 ⋅(1 −𝐻(ℱ𝑐)
𝑛⋅𝐻max
)
(307)
where the final equality holds when the information constraint is binding (typical for complex collective
functions).
■
■
This supplementary material extends the Cognitive Integrity Framework to collective phenomena, establishing
colony cognitive security as a distinct research direction with formal foundations and practical benchmarks.
119

## Page 121

13
Supplementary: Notation Reference
This supplement provides a comprehensive reference for the mathematical notation used throughout the
Cognitive Integrity Framework (CIF) manuscript, including the eusocial and colony cognitive security exten-
sions. Symbols are organized by domain, with cross-references to their formal definitions in the main text
and supplements.
13.1
Adversary Model Notation
Symbol
Meaning
Defined In
Ω𝑘
Adversary class 𝑘(e.g., Ω1 =
External, Ω5 = Systemic)
Definition 3.1
ℛ
Attack resource tuple
⟨𝑅𝐶, 𝑅𝐾, 𝑅𝐴, 𝑅𝑃, 𝑅𝐶𝑜⟩
Definition 3.7
𝑅𝐶
Computational resources
(FLOPS-hours)
Table 5
𝑅𝐾
Knowledge resources (system
understanding)
Table 5
𝑅𝐴
Access resources (available
channels)
Table 5
𝑅𝑃
Persistence resources (temporal
presence)
Table 5
𝑅𝐶𝑜
Coordination resources
(multi-party synchronization)
Table 5
𝐷score
Detectability score of an attack
Definition 3.8
𝒞adv
Adversarial capability set
Definition 3.9
𝒦•
Adversary knowledge component
of the class tuple; the subscript
names its scope (𝒦public,
𝒦domain, 𝒦protocol, 𝒦internal)
Section 3
ℰ
Communication edge set
{(𝑎𝑖, 𝑎𝑗) ∶𝒞(𝑎𝑖, 𝑎𝑗) = 1}; the
adversary-controlled subset is
ℰctrl ⊆ℰ(distinct from the
stigmergic ℰbelow)
Definition 3.5
𝒜BIM
Belief injection/manipulation
attack class
Section 3.6
𝒜BI
Belief injection attack
Theorem 7.1
13.2
System Model Notation
Symbol
Meaning
Defined In
𝒪
Multiagent operator tuple
⟨𝒜, 𝒞, 𝒮, 𝒫, Γ⟩
Definition 4.1
𝒜
Set of agents {𝑎1, … , 𝑎𝑛}
Table 10
𝑎𝑖
Individual agent 𝑖
Definition 4.1
𝑛
Number of agents
Throughout
𝒞
Communication adjacency matrix
Table 10
𝒮
Shared global state
Definition 4.1
𝒫
Permission mapping
Table 10
Γ
Coordination protocol
Definition 4.1
120

## Page 122

Symbol
Meaning
Defined In
𝜎𝑖
Cognitive state of agent 𝑎𝑖:
⟨ℬ𝑖, 𝒢𝑖, ℐ𝑖, ℋ𝑖⟩
Definition 4.2
ℬ𝑖
Belief distribution of agent 𝑎𝑖:
Φ →[0, 1]
Table 11
𝒢𝑖
Goal set of agent 𝑎𝑖
Table 11
ℐ𝑖
Intention set (committed actions)
Table 11
ℋ𝑖
Interaction history
Table 11
𝑆𝑡
Global system state at time 𝑡
Definition 4.3
𝜎𝑡
𝑖
Cognitive state of agent 𝑖at time
𝑡
Definition 4.2
Φ
Set of propositions
Section 11.2.1
𝜙, 𝜓
Individual propositions
Section 11.2.1
ℳ
Message space (distinct from the
set of marker types ℳof
Definition 12.1)
Definition 5.2
𝑚
Individual message
Definition 5.2
Σ
OODA input alphabet
ℳ∪Events (distinct from the
stigmergic update function Σ of
Definition 12.1)
Definition 4.20
13.3
Trust Calculus Notation
Symbol
Meaning
Defined In
𝒯𝑖→𝑗
Trust score from agent 𝑖to agent
𝑗
Definition 4.6
𝒯base / 𝑇base
Base architectural trust
(role-based)
Table 12
𝒯rep / 𝑇rep
Reputation trust (historical
accuracy)
Table 12
𝒯ctx / 𝑇ctx
Contextual trust (task-specific)
Table 12
𝛼, 𝛽, 𝛾
Trust component weights
(𝛼+ 𝛽+ 𝛾= 1)
Equation (43)
𝛿
Trust decay factor (𝛿∈(0, 1))
Definition 4.7
𝑑
Delegation depth
Definition 4.7
𝒯del
Delegated trust value
Definition 4.7
𝒯path
Path trust value
Definition 11.2
𝜂𝑚
Modality reliability factor
Definition 4.9
𝜂
Learning rate (reputation update)
Trust configuration
𝜌
Penalty factor (failure penalty
multiplier)
Trust configuration
⊗
Trust delegation operator
Definition 4.8
⊕
Trust aggregation operator
Definition 4.8
13.4
Defense Mechanism Notation
Symbol
Meaning
Defined In
ℱ(𝑚)
Cognitive firewall classification
function
Definition 5.2
121

## Page 123

Symbol
Meaning
Defined In
𝐷inj
Injection detection score
Definition 5.3
𝐷sus
Suspicious content score
Definition 5.3
𝜏1
Firewall reject threshold
Equation (81)
𝜏2
Firewall quarantine threshold
Equation (81)
ℬverified
Set of verified beliefs
Definition 4.14
ℬprovisional
Set of provisional (sandboxed)
beliefs
Definition 4.14
𝜋(𝜙)
Provenance chain for belief 𝜙
Definition 4.12
𝑉(𝜋)
Provenance verification function
Section 4.3
𝒲
Set of canary beliefs (tripwires)
Definition 5.6
𝜔𝑗
Individual canary belief
Equation (85)
𝑝exp
𝑗
Expected probability for canary 𝑗
Equation (85)
𝜖drift
Drift detection threshold
Equation (86)
ℐinv
Set of behavioral invariants
Definition 5.8
𝐼𝑘
Individual invariant predicate
Equation (87)
𝜅
Corroboration threshold
Section 4.4.7
TTL
Time-to-live for provisional
beliefs
Sandbox configuration
13.5
Detection & Analysis Notation
Symbol
Meaning
Defined In
𝑆drift
Drift score (belief change
magnitude)
Definition 6.1
𝐷KL
Kullback-Leibler divergence (drift
detection)
Definition 5.10
𝑤
Sliding window size
Definition 5.10
𝑔𝑡
CUSUM cumulative statistic at
time 𝑡
Definition 5.18
𝜈
CUSUM allowance (reference
value)
Definition 5.18
ℎ
CUSUM decision interval (alert
threshold on 𝑔𝑡)
Definition 5.18
𝜆
Max delta weight in drift scoring
Equation (123)
𝜆
Chernoff tilting parameter,
𝜆∈[0, 1] (unrelated to the drift
weight above and to the
colonial-trust decay constant)
Equation (155)
𝑆dev
Behavioral deviation score
Definition 6.2
𝑓𝑘
Feature extractor function
Equation (124)
𝜇𝑘, 𝜎𝑘
Feature mean and standard
deviation
Equation (124)
AUC
Area Under the ROC Curve
Definition 6.5
TPR(𝜏)
True Positive Rate at threshold 𝜏
Equation (127)
FPR(𝜏)
False Positive Rate at threshold 𝜏
Equation (128)
FNR(𝜏)
False Negative Rate at threshold
𝜏
Equation (82)
𝑆fused
Fused detector score
Definition 6.7
𝐷fused
Fused detector decision
Definition 6.8
taint(𝜙)
Provenance tags for belief 𝜙
Definition 6.18
122

## Page 124

Symbol
Meaning
Defined In
Λ(𝑚)
Likelihood ratio
𝑃attack(𝑚)/𝑃benign(𝑚) (capital Λ;
unrelated to 𝜆)
Definition 6.23
13.6
Consensus & Coordination Notation
Symbol
Meaning
Defined In
𝑞
Quorum threshold for consensus
Definition 5.12
𝑓
Maximum number of
Byzantine/compromised agents
Theorem 5.3
ℬconsensus
Consensus belief function
Definition 5.11
𝒟
Set of defense mechanisms
Definition 5.13
𝒟1 ∘𝒟2
Series defense composition
Equation (93)
𝒟1 ∥𝒟2
Parallel defense composition
Equation (94)
𝑃detect
Detection probability
Equation (95)
𝑟𝑓
Firewall detection rate
Theorem 7.1
𝑟𝑠
Sandbox verification rate
Theorem 7.1
13.7
Cost & Performance Notation
Symbol
Meaning
Defined In
𝐶total
Total defense cost
Definition 5.14
𝐶compute
Computational cost
Table 24
𝐶latency
Latency cost
Table 24
𝐶fp
False positive cost
Table 24
𝐶FP, 𝐶FN
Cost of false positive / false
negative
Definition 6.17
𝐵total
Total defense benefit
Definition 5.15
𝐿CIF
CIF latency overhead
Theorem 7.16
𝐿𝑑
Latency of defense 𝑑
Equation (99)
𝐿max
Maximum allowed latency
Equation (99)
13.8
Information & Complexity Notation
Symbol
Meaning
Defined In
𝐻(𝒜)
Entropy of attack 𝒜
Theorem 4.12
𝐼(𝐷; 𝒜)
Mutual information between
detector and attack
Definition 4.16
𝐶channel
Channel capacity
Theorem 4.15
𝑂(⋅)
Big-O complexity bound
Section 7.4
𝑆total
Total space complexity
Equation (188)
𝑇msg
Per-message processing time
Equation (189)
13.9
Stigmergic & Colony Notation (Supplementary)
123

## Page 125

Symbol
Meaning
Defined In
𝒪Σ
Stigmergic operator tuple
Definition 12.1
ℰ
Environmental state
(markers/signals)
Definition 12.1
Σ
Stigmergic update function
(distinct from the OODA input
alphabet Σ of Definition 4.20)
Definition 12.1
ℒ
Set of locations
Definition 12.1
ℳ
Set of marker types (distinct from
the message space ℳof
Definition 5.2)
Definition 12.1
𝒩
Cyberphysical niche
Definition 12.2
ℱ𝑐
Emergent collective function
Definition 12.3
𝒯𝑐
Colonial trust function
(environment-mediated)
Definition 12.4
𝜌(𝑚, 𝑙, 𝑡)
Signal reliability at location 𝑙for
marker 𝑚at time 𝑡
Equation (279)
𝜆
Temporal decay constant
(colonial trust)
Equation (279)
𝑄𝛼
Cognitive quorum function for
action 𝛼
Definition 12.5
𝒜𝑒
Emergent attack
Definition 12.6
CCS
Colony CogSec Score
Definition 12.7
DR𝑐
Colony-level detection rate
Equation (296)
FPR𝑐
Colony-level false positive rate
Equation (296)
13.10
General Mathematical Notation
Symbol
Meaning
Usage
𝑃(⋅)
Probability measure
Throughout
𝟙[⋅]
Indicator function
Equation (133)
𝜏
Generic threshold parameter
Throughout
𝜃drift
KL drift-detection threshold;
distinct from the per-canary
deviation tolerance 𝜖drift
Equation (89)
𝜃total, 𝜃step
Cumulative and per-step drift
thresholds in a progressive-drift
attack
Definition 3.24
𝜃(alarm)
Baseline drift alarm threshold
𝜇baseline + 𝑘𝜎baseline
Property 6.1
𝜃𝑖
Escalation threshold at stage 𝑖of
the multi-stage detection pipeline
Definition 6.26
𝜃(fusion)
Learned parameters of the fusion
network — not a threshold
Equation (134)
𝑟𝜃
Fisher-Rao displacement
corresponding to 𝜃drift
Theorem 4.16
𝜖
Small constant (error rate,
deviation)
Throughout
𝑡
Time index
Throughout
⊧
Satisfaction relation (state
satisfies predicate)
Equation (88)
⊢
Logical entailment
Equation (175)
124

## Page 126

Symbol
Meaning
Usage
⊥
Logical contradiction
Equation (175)
⟂
Undecided / undefined
Equation (91)
✓
Verification passed
Table 38
13.11
CTL Temporal Logic Notation (Formal Verification)
Symbol
Meaning
Defined In
𝐴𝐺
“Always globally” (CTL operator)
Equation (193)
𝐴𝐹
“Always eventually” (CTL operator)
Equation (194)
𝐸𝑋
“Exists next” (CTL operator)
Section 7.5.2
⇒
Logical implication
Throughout
↔
Logical biconditional
Throughout
125

## Page 127

14
References
14.1
Foundational Works
1. Lamport, L., Shostak, R., & Pease, M. (1982). The Byzantine Generals Problem. ACM Transactions
on Programming Languages and Systems, 4(3), 382-401.
2. Dwork, C., Lynch, N., & Stockmeyer, L. (1988).
Consensus in the Presence of Partial Synchrony.
Journal of the ACM, 35(2), 288-323.
3. Josang, A., Ismail, R., & Boyd, C. (2007). A Survey of Trust and Reputation Systems for Online
Service Provision. Decision Support Systems, 43(2), 618-644.
14.2
Prompt Injection and LLM Security
1. Qi, X., et al. (2024). Visual Adversarial Examples Jailbreak Aligned Large Language Models. AAAI
2024.
2. Perez, F., & Ribeiro, I. (2023). Ignore This Title and HackAPrompt: Exposing Systemic Vulnerabilities
of LLMs. EMNLP 2023.
3. Greshake, K., et al. (2023).
Not What You’ve Signed Up For: Compromising Real-World LLM-
Integrated Applications with Indirect Prompt Injection. ACM AISec 2023.
4. Liu,
Y.,
et
al.
(2023).
Prompt
Injection
Attack
Against
LLM-Integrated
Applications.
arXiv:2306.05499.
14.3
Constitutional AI and Alignment
1. Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. arXiv:2212.08073.
2. Askell,
A.,
et al. (2021).
A General Language Assistant as a Laboratory for Alignment.
arXiv:2112.00861.
14.4
Multiagent Systems
1. Wooldridge, M. (2009). An Introduction to Multiagent Systems. John Wiley & Sons.
2. Shoham, Y., & Leyton-Brown, K. (2008). Multiagent Systems: Algorithmic, Game-Theoretic, and
Logical Foundations. Cambridge University Press.
3. Hong, S., et al. (2023).
MetaGPT: Meta Programming for Multi-Agent Collaborative Framework.
arXiv:2308.00352.
4. Wu, Q., et al. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.
arXiv:2308.08155.
14.5
Trust in Distributed Systems
1. Marsh, S. P. (1994).
Formalising Trust as a Computational Concept.
PhD Thesis, University of
Stirling.
2. Gambetta, D. (1988). Can We Trust Trust? In Trust: Making and Breaking Cooperative Relations,
213-237.
3. Sabater, J., & Sierra, C. (2005). Review on Computational Trust and Reputation Models. Artificial
Intelligence Review, 24(1), 33-60.
126

## Page 128

14.6
Adversarial ML
1. Goodfellow, I. J., Shlens, J., & Szegedy, C. (2015). Explaining and Harnessing Adversarial Examples.
ICLR 2015.
2. Carlini, N., & Wagner, D. (2017). Towards Evaluating the Robustness of Neural Networks. IEEE S&P
2017.
14.7
Formal Verification
1. Clarke, E. M., Grumberg, O., & Peled, D. A. (1999). Model Checking. MIT Press.
2. Alur, R. (2015). Principles of Cyber-Physical Systems. MIT Press.
14.8
Cognitive Security
1. Waltzman, R. (2017). The Weaponization of Information: The Need for Cognitive Security. RAND
Corporation.
2. Beskow, D. M., & Carley, K. M. (2019). Social Cybersecurity: An Emerging National Security Re-
quirement. Military Review, 99(2), 117.
14.9
Agent Frameworks
1. LangChain. (2023). LangGraph: Build Stateful Multi-Actor Applications. Documentation.
2. CrewAI. (2024). Framework for Orchestrating Role-Playing, Autonomous AI Agents.
3. Anthropic. (2024). Claude Code: AI-Powered Software Engineering.
14.10
2025 Agentic AI Security
1. OWASP Foundation. (2025). OWASP Top 10 for LLM Applications 2025.
2. OWASP GenAI Security Project. (2025). OWASP Top 10 for Agentic Applications 2026.
3. Chen, W., Zhang, Y., & Liu, J. (2025). A Multi-Agent LLM Defense Pipeline Against Prompt Injection
Attacks. arXiv:2509.14285.
4. Jo, Y., Kim, S., & Park, J. (2025). Byzantine-Robust Decentralized Coordination of LLM Agents.
arXiv:2507.14928.
5. Wang, H., Li, X., & Chen, Y. (2025). Rethinking the Reliability of Multi-agent System: A Perspective
from Byzantine Fault Tolerance. arXiv:2511.10400.
6. Debenedetti, E., Zhang, J., & Carlini, N. (2025). Adaptive Attacks Break Defenses Against Indirect
Prompt Injection Attacks on LLM Agents. NAACL 2025 Findings.
7. Li, Z., Wang, T., & Zhang, L. (2025). Prompt Injection Attack to Tool Selection in LLM Agents.
arXiv:2504.19793.
8. Cloud Security Alliance. (2025). Cognitive Degradation Resilience for Agentic AI.
9. Chen, X., Liu, Y., & Wang, Z. (2025). AI Agents Under Threat: A Survey of Key Security Challenges
and Future Pathways. ACM Computing Surveys.
14.11
Eusocial Intelligence and Swarm Systems
1. Wilson, E. O. (1971). The Insect Societies. Belknap Press of Harvard University Press.
2. Hölldobler, B., & Wilson, E. O. (1990). The Ants. Belknap Press of Harvard University Press.
127

## Page 129

3. Bonabeau, E., Dorigo, M., & Theraulaz, G. (1999). Swarm Intelligence: From Natural to Artificial
Systems. Oxford University Press.
4. Seeley, T. D. (2010). Honeybee Democracy. Princeton University Press.
5. Grassé, P.-P. (1959). La reconstruction du nid et les coordinations interindividuelles chez Bellicositer-
mes natalensis et Cubitermes sp. La théorie de la stigmergie. Insectes Sociaux, 6(1), 41-80.
6. Lenoir, A., D’Ettorre, P., Errard, C., & Hefetz, A. (2001). Chemical Ecology and Social Parasitism in
Ants. Annual Review of Entomology, 46, 573-599.
7. Kilner, R. M., & Langmore, N. E. (2011). Cuckoos Versus Hosts in Insects and Birds: Adaptations,
Counter-adaptations and Outcomes. Biological Reviews, 86, 836-852.
8. Couzin, I. D. (2009). Collective Cognition in Animal Groups. Trends in Cognitive Sciences, 13(1),
36-43.
9. Detrain, C., & Deneubourg, J.-L. (2006). Self-Organized Structures in a Superorganism: Do Ants
“Behave” Like Molecules? Physics of Life Reviews, 3(3), 162-187.
10. Pratt, S. C. (2005). Quorum Sensing by Encounter Rates in the Ant Temnothorax albipennis. Behav-
ioral Ecology, 16(2), 488-496.
Aim Labs.
EchoLeak: Zero-click data exfiltration from Microsoft 365 Copilot via LLM scope violation.
Security advisory, CVE-2025-32711 (CVSS 9.3), 2025. URL https://nvd.nist.gov/vuln/detail/CVE-2025-
32711. Zero-click indirect prompt injection: a payload hidden in an inbound email is parsed and retained
by the assistant, then used to exfiltrate data already inside its retrieval scope, with no user interaction.
Patched server-side by Microsoft; no exploitation observed in the wild.
Shun-ichi Amari and Hiroshi Nagaoka. Methods of Information Geometry. American Mathematical Society,
2000. Foundational text on information geometry; defines the Fisher-Rao metric, geodesics on the proba-
bility simplex, and the natural gradient. The Fisher-Rao distance 𝑑FR(𝑝, 𝑞) = 2 arccos(∑𝑖
√𝑝𝑖𝑞𝑖) used in
the stealth-impact bound is derived from the sphere isometry of the probability simplex.
Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna
Chen, Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, et al. Constitutional AI: Harmlessness from
AI feedback. arXiv preprint arXiv:2212.08073, 2022.
Eric Bonabeau, Marco Dorigo, and Guy Theraulaz. Swarm Intelligence: From Natural to Artificial Systems.
Oxford University Press, 1999. ISBN 978-0195131598.
Michael D. Breed, Ernesto Guzmán-Novoa, and Greg J. Hunt. Defensive behavior of honey bees: organization,
genetics, and comparisons with other bees. Annual Review of Entomology, 49:271–298, 2004. doi: 10.114
6/annurev.ento.49.061802.123155.
Patrick Chao, Alexander Robey, Edgar Dobriban, Hamed Hassani, George J. Pappas, and Eric Wong.
JailbreakBench: An open robustness benchmark for jailbreaking large language models. arXiv preprint
arXiv:2404.01318, 2024.
Yulin Chen, Haoran Li, Yuexin Li, Yue Liu, Yangqiu Song, and Bryan Hooi. TopicAttack: An indirect
prompt injection attack via topic transition. In Proceedings of the 2025 Conference on Empirical Methods
in Natural Language Processing (EMNLP), 2025. arXiv:2507.13686, EMNLP 2025. A generated conversa-
tional transition gradually shifts the topic toward the injected instruction, raising the injected-to-original
attention ratio and exceeding 90% attack success in most settings even against deployed defenses.
Herman Chernoff. A measure of asymptotic eﬀiciency for tests of a hypothesis based on the sum of observa-
tions. Annals of Mathematical Statistics, 23(4):493–507, 1952. doi: 10.1214/aoms/1177729330. Introduces
Chernoff information 𝐶∗as the maximum error exponent for hypothesis testing; the sample complexity
bound 𝑛∗= ⌈log(1/𝜖)/𝐶∗⌉for attack detection derives from this result.
Edmund M. Clarke, Orna Grumberg, and Doron A. Peled.
Model Checking.
MIT Press, 1999.
ISBN
978-0262032704.
128

## Page 130

Cloud Security Alliance. Cognitive degradation resilience for agentic AI. CSA Blog, 2025. Framework for
progressive cognitive attack detection.
COGSEC, R. J. Cordes, Daniel Ari Friedman, and contributors. COGSEC ATLAS: Patterns of cognitive
security threats and remedies. Coda Document, 2023. URL https://coda.io/@aien/cogsec-atlas/patterns-
26. Community-maintained database of 995 cognitive security patterns categorized by type (Vulnerability,
Exploit, Remedy, Practice, Accelerator, Moderator, Condition) with hierarchical parent-child relationships.
Licensed CC BY-SA 4.0.
R. J. Cordes, Daniel Ari Friedman, and contributors. The Great Preset: Remote Teams and Operational
Art. COGSEC, 2020. URL https://www.cogsec.org/irt-20-7. IRT-20 (Information Resilience Toolkit)
Initiative. Findings on emergent remote organization dynamics, formation, performance, and information
sharing.
R. J. Cordes, Daniel Ari Friedman, and contributors. Narrative Information Ecosystems: Conflict and Trust
on the Endless Frontier. COGSEC, 2021. URL https://www.cogsec.org/nim-21-8. NIM-21 (Narrative
Information Management) Initiative. Explores cognitive overload navigation and narrative identity-based
filtering vulnerabilities.
R. J. Cordes, Daniel Ari Friedman, and contributors. ATLAS: A question oriented approach to the use
of pattern languages in knowledge management. Technical white paper, COGSEC, 2023. URL https:
//www.cogsec.org/atlas-23-10. ATLAS-23 Initiative. Specifies a generalized system for managing patterns
of practice and risk in cognitive security.
Thomas M. Cover and Joy A. Thomas. Elements of Information Theory. Wiley-Interscience, 2nd edition,
2006. Comprehensive reference for information theory; Pinsker’s inequality ‖𝑃−𝑄‖TV ≤√𝐷KL(𝑃‖𝑄)/2
(Lemma 11.6.1) is used in the KL-AUC coupling proof.
CrewAI. Framework for orchestrating role-playing, autonomous AI agents. GitHub Repository, 2024. URL
https://github.com/joaomdmoura/crewAI.
Cameron R. Currie, Michael Poulsen, John Mendenhall, Jacobus J. Boomsma, and Johan Billen. Coevolved
crypts and exocrine glands support mutualistic bacteria in fungus-growing ants. Science, 311(5757):81–83,
2006. doi: 10.1126/science.1119744.
Scott David, Richard J. Cordes, and Daniel A. Friedman. Active inference in modeling conflict. Zenodo,
2021. Integrates conflict studies with Active Inference, introducing the Active Inference Conflict (AIC)
model. Formalizes OODA loops within cognitive frameworks and addresses conflict in BOLTS (Business,
Operations, Legal, Technical, Social) contexts.
Edoardo Debenedetti, Jie Zhang, and Nicholas Carlini. Adaptive attacks break defenses against indirect
prompt injection attacks on LLM agents. In Findings of the Association for Computational Linguistics:
NAACL 2025, 2025. Attack success rate >90% against 12 published defenses.
Géraldine DG Debout, Bertrand Schatz, Mikaël Elias, and Doyle McKey. Polydomy in ants: what we know,
what we think we know, and what remains to be done. Biological Journal of the Linnean Society, 90(2):
319–348, 2007. doi: 10.1111/j.1095-8312.2007.00728.x.
Hermogenes Fernández-Marín, Jess K. Zimmerman, Stephen A. Rehner, and William T. Wcislo. Active use
of the metapleural glands by ants in controlling fungal infection. Proceedings of the Royal Society B, 273
(1594):1689–1695, 2006. doi: 10.1098/rspb.2006.3492.
Daniel Ari Friedman. Cognitive integrity framework: Computational validation and empirical analysis, 2026a.
Part 2: Implementation and Empirical Analysis — 950-attack corpus, multi-tier evaluation, ablation stud-
ies, Bayesian uncertainty, and parametric architecture-aware simulation across four production multiagent
topologies.
Daniel Ari Friedman. Cognitive integrity framework: Practical applications and deployment guide, 2026b.
Part 3 (merged from original Parts 3+4): Qualitative review and practitioner synthesis — accessible-
language distillation, deployment guides, subagent hardening, incident-response playbooks, monitoring,
129

## Page 131

cost-benefit analysis, operator risk frameworks — combined with CIF-AD-OODA applications across ten
critical operational domains, three universal attack patterns (FR Polarity Inversion, Constraint Relaxation,
Context Boundary Violation), four novel defense extensions, and retrospective analysis of 2024–2025 AI-
agent security incidents.
Karl J. Friston, Jean Daunizeau, and Stefan J. Kiebel. Action and behavior: A free-energy formulation.
Biological Cybernetics, 102(3):227–260, 2010. doi: 10.1007/s00422-010-0364-z. Foundational formulation of
action selection as free-energy minimization; establishes the variational principle underlying belief updating
that the belief sandbox constrains.
Pierre-Paul Grassé.
La reconstruction du nid et les coordinations interindividuelles chez Bellicositermes
natalensis et Cubitermes sp. la théorie de la stigmergie. Insectes Sociaux, 6(1):41–80, 1959. doi: 10.1007/
BF02223791.
Christoph Grüter and Walter M. Farina. The honeybee waggle dance: can we follow the steps? Trends in
Ecology & Evolution, 24(5):242–247, 2009. doi: 10.1016/j.tree.2008.12.007.
Bert Hölldobler and Edward O. Wilson. The Ants. Belknap Press of Harvard University Press, 1990. ISBN
9780674040755. Pulitzer-winning comprehensive treatment of ant biology; the reference work for colony
organisation, communication and caste.
Sirui Hong, Mingchen Zhuge, Jonathan Chen, Xiawu Zheng, Yuheng Cheng, Ceyao Zhang, Jinlin Wang, Zili
Wang, Steven Ka Shing Yau, Zijuan Lin, et al. MetaGPT: Meta programming for multi-agent collaborative
framework. arXiv preprint arXiv:2308.00352, 2023.
Evan Hubinger et al. Sleeper agents: Training deceptive LLMs that persist through safety training. arXiv
preprint arXiv:2401.05566, 2024.
Duncan E. Jackson and Francis L. W. Ratnieks. Communication in ants. Current Biology, 16(15):R570–R574,
2006. doi: 10.1016/j.cub.2006.07.015.
Yongrae Jo and Chanik Park. Byzantine-robust decentralized coordination of LLM agents. arXiv preprint
arXiv:2507.14928, 2025.
Rebecca M. Kilner and Naomi E. Langmore. Cuckoos versus hosts in insects and birds: adaptations, counter-
adaptations and outcomes. Biological Reviews, 86:836–852, 2011. doi: 10.1111/j.1469-185X.2010.00173.x.
Matthias Konrad, Meghan L. Vyleta, Fabian J. Theis, Miriam Stock, Sandra Singarové, Barbara Feldmeyer,
Susanne Most, and Sylvia 335ler. Social transfer of pathogenic fungus promotes active immunisation in
ant colonies. PLoS Biology, 10(4):e1001300, 2012. doi: 10.1371/journal.pbio.1001300.
LangChain. LangGraph: Build stateful multi-actor applications. Documentation, 2023. URL https://lang
chain-ai.github.io/langgraph/.
Alain Lenoir, Patrizia D’Ettorre, Christine Errard, and Abraham Hefetz.
Chemical ecology and social
parasitism in ants. Annual Review of Entomology, 46:573–599, 2001. doi: 10.1146/annurev.ento.46.1.573.
Xiao Liu, Hao Yu, Hanchen Zhang, Yifan Xu, Xuanyu Lei, Hanyu Lai, Yu Gu, Hangliang Ding, Kaiwen
Men, Kejuan Yang, et al. AgentBench: Evaluating LLMs as agents. arXiv preprint arXiv:2308.03688,
2023.
Maria Cristina Lorenzi and Anne-Geneviève Bagnères. A review of the mechanisms of cuticular hydrocarbon
plasticity in social insects. Annales Zoologici Fennici, 48:131–148, 2011.
Mantas Mazeika, Long Phan, Xuwang Yin, Andy Zou, Zifan Wang, Norman Mu, Elham Sakhaee, Nathaniel
Li, Steven Basart, Bo Li, et al. HarmBench: A standardized evaluation framework for automated red
teaming and robust refusal. In International Conference on Machine Learning, 2024.
Grégoire Mialon, Roberto Dessì, Maria Lomeli, Christoforos Nalmpantis, Ram Pasunuru, Roberta Raber,
et al. GAIA: A benchmark for general AI assistants. arXiv preprint arXiv:2311.12983, 2023.
130

## Page 132

Jerzy Neyman and Egon S. Pearson. On the problem of the most eﬀicient tests of statistical hypotheses.
Philosophical Transactions of the Royal Society A, 231:289–337, 1933.
doi: 10.1098/rsta.1933.0009.
Foundation of optimal hypothesis testing; the Neyman-Pearson lemma establishes the likelihood ratio
test as the uniformly most powerful test, providing the theoretical basis for the optimal cognitive attack
detector described in §6.
OpenClaw. Openclaw: Personal AI assistant for multi-platform integration. Software Platform, 2026. URL
https://www.openclaw.ai/. Locally-deployed AI agent with full system access, persistent memory, browser
automation, and multi-platform messaging (WhatsApp, Telegram, Discord, Slack, Signal, iMessage).
OpenClaw Security Team. Openclaw security considerations: Prompt injection, access control, and defense
strategies. Security Documentation, 2026. URL https://docs.openclaw.ai/security. Documents prompt in-
jection as “single most critical threat,” recommends reader agents for untrusted content, sender allowlists,
sandboxing, and tool-disabled pre-summarization. Attack vectors include browser-fetched malicious con-
tent, social engineering, and persistent memory exploitation.
OWASP Foundation. OWASP top 10 for LLM applications 2025. Security Standard, 2025. URL https:
//genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/.
OWASP GenAI Security Project. OWASP top 10 for agentic applications 2026. Security Standard, 2025.
URL https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/. Released
December 2025.
Ewan S. Page. Continuous inspection schemes. Biometrika, 41(1–2):100–115, 1954. doi: 10.1093/biomet/41.1-
2.100.
Original CUSUM (Cumulative Sum) sequential change-point detection algorithm. Used as the
canonical drift detection method for the Orient phase of the OODA monitor.
Vik Pant and Eric Yu. Computational foundations for strategic coopetition: Formalizing trust and reputation
dynamics. arXiv preprint arXiv:2510.24909, 2025. 81.7% validation accuracy in trust trajectory prediction.
Thomas Parr and Karl J. Friston. Generalised free energy and active inference. Biological Cybernetics, 113
(5-6):495–513, 2019. doi: 10.1007/s00422-019-00805-w. Extends the free-energy principle to continuous-
time dynamics and generalized coordinates; provides the mathematical framework connecting precision-
weighted belief updates to defense mechanisms.
Ethan Perez, Sam Ringer, Kamilė Lukošiūtė, Karina Nguyen, Edwin Chen, Scott Heiner, Craig Pettit,
Catherine Olsson, Sandipan Kundu, Saurav Kadavath, et al. Discovering language model behaviors with
model-written evaluations. In Findings of the Association for Computational Linguistics: ACL 2023, 2023.
Red teaming evaluation framework.
Xiangyu Qi, Kaixuan Huang, Ashwinee Panda, Peter Henderson, Mengdi Wang, and Prateek Mittal. Visual
adversarial examples jailbreak aligned large language models. Proceedings of the AAAI Conference on
Artificial Intelligence, 38(19):21527–21536, 2024. doi: 10.1609/aaai.v38i19.30150.
Susan S. Schneider and Linda C. McNally. Waggle dance behavior associated with seasonal absconding in
colonies of the african honey bee, apis mellifera scutellata. Insectes Sociaux, 40(4):467–478, 1993. doi:
10.1007/BF01253807.
Thomas D. Seeley. Honeybee Democracy. Princeton University Press, 2010. ISBN 978-0691147215.
Ana B. Sendova-Franks, Richard K. Hayward, Benjamin Wulf, Tobias Klimber, Richard James, Robert
Planqué, John A. Sherwood, Sarah L. Sherwood, Wayne F. Sherwood, and William F. Sherwood. Emer-
gency clustering of sick honeybees in the hive: a collective defensive behaviour? Animal Behaviour, 80(1):
185–198, 2010. doi: 10.1016/j.anbehav.2010.04.019.
Erfan Shayegani, Md Abdullah Al Mamun, Yu Fu, Pedram Zaree, Yue Dong, and Nael Abu-Ghazaleh. Survey
of vulnerabilities in large language models revealed by adversarial attacks. arXiv preprint arXiv:2310.10844,
2023.
Jiawen Shi, Zenghui Yuan, Guiyao Tie, Pan Zhou, Neil Zhenqiang Gong, and Lichao Sun. Prompt injection
attack to tool selection in LLM agents. arXiv preprint arXiv:2504.19793, 2025.
131

## Page 133

Marla Simone, Jay D. Evans, and Marla Spivak.
Resin collection and social immunity in honey bees.
Evolution, 63(11):3016–3022, 2009. doi: 10.1111/j.1558-5646.2009.00772.x.
Marla Spivak and Gary S. Reuter. Resistance to american foulbrood disease by honey bee colonies apis
mellifera bred for hygienic behavior. Apidologie, 32(6):555–565, 2001. doi: 10.1051/apido:2001103.
Lichao Sun, Yue Huang, Haoran Wang, Siyuan Wu, Qihui Zhang, Chujie Gao, Yixin Huang, Wenhan Lyu,
Yixuan Zhang, Xiner Li, et al. TrustLLM: Trustworthiness in large language models. arXiv preprint
arXiv:2401.05561, 2024.
Robert K. Vander Meer and Lucia E. Alonso. Pheromone directed behavior in ants. In Pheromone Commu-
nication in Social Insects, pages 159–192. Westview Press, 1998.
Will Vandevanter. Prompt injection to RCE in AI agents. Trail of Bits blog, October 2025. URL https:
//blog.trailofbits.com/2025/10/22/prompt-injection-to-rce-in-ai-agents/. Argument injection against
pre-approved agent tools: agents gate the command name but not its flags, so injected input reaching a
permitted utility (find, grep, git, go test) can reach an execution flag such as -exec and obtain code
execution.
James S. Waters, C. Tate Holbrook, Jennifer H. Fewell, and Jon F. Harrison. Allometric scaling of metabolism,
growth, and activity in whole colonies of the seed-harvester ant pogonomyrmex californicus. The American
Naturalist, 176(4):501–510, 2010. doi: 10.1086/656266.
Alexander Wei, Nika Haghtalab, and Jacob Steinhardt. Jailbroken: How does LLM safety training fail? In
Advances in Neural Information Processing Systems (NeurIPS), 2023.
Edward O. Wilson. The Insect Societies. Belknap Press of Harvard University Press, 1971. ISBN 978-
0674454903.
Edward O. Wilson, N. I. Durlach, and Louis M. Roth. Chemical releasers of necrophoric behavior in ants.
Psyche, 65:108–114, 1958. doi: 10.1155/1958/69391.
Lifan Zheng, Jiawei Chen, Qinghong Yin, Jingyuan Zhang, Xinyi Zeng, and Yu Tian. Rethinking the reliabil-
ity of multi-agent system: A perspective from Byzantine fault tolerance. arXiv preprint arXiv:2511.10400,
2025. Proposes CP-WBFT, a confidence-probe-weighted Byzantine consensus for LLM agents; reports
operation under fault rates as high as 85.7%.
Andy Zou et al. Universal adversarial triggers for multi-modal agents. In Proceedings of the 2025 Conference
on Computer and Communications Security (CCS), 2025.
132
