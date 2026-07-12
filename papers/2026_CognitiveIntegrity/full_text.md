# Full Text: Cognitive Integrity Framework: Formal Foundations for Multiagent Security

> Extracted from `2026_CognitiveIntegrity.pdf`

---

## Page 1

Cognitive Integrity Framework: Formal Foundations for Multiagent
Security
Part 1 of 3: Theoretical Foundations
Daniel Ari Friedman
Active Inference Institute
daniel@activeinference.institute
ORCID: 0000-0001-6232-9096
DOI: 10.5281/zenodo.18364119
2026-01-24
“I will not cease from Mental Fight,
Nor shall my Sword sleep in my hand:”
— William Blake

## Page 2

Contents
1
Abstract
7
2
Introduction: Cognitive Attack Surfaces in Multiagent Operators
8
2.1
The Multiagent Operator Paradigm
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
2.2
The 2026 Multiagent Landscape . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
2.2.1
From Chatbots to Cognitive Operators . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
2.2.2
Cyberphysical Cognitive Systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
8
2.2.3
The Trust Recursion Problem . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
9
2.2.4
Cross-Modality Attack Surfaces . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
9
2.2.5
The Scale of Exposure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
2.2.6
Why Traditional (Cyberphysical) Security Is Incomplete . . . . . . . . . . . . . . . . .
10
2.3
Motivating Incidents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
10
2.3.1
Incident: Nested Instruction Injection (External) . . . . . . . . . . . . . . . . . . . . .
11
2.3.2
Incident: The Poisoned Code Review (Peripheral)
. . . . . . . . . . . . . . . . . . . .
11
2.3.3
Incident: The Identity Confusion Attack (Agent-Level) . . . . . . . . . . . . . . . . . .
11
2.3.4
Incident: The Consensus Manipulation (Coordination) . . . . . . . . . . . . . . . . . .
11
2.3.5
Incident: Orchestrator Compromise (Systemic) . . . . . . . . . . . . . . . . . . . . . .
12
2.4
Motivation from Recent Deployments . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12
2.5
Problem Statement . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
12
2.6
Research Questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
13
2.7
Contributions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
13
2.8
Paper Organization . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
14
2.9
Scope and Limitations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
14
3
Threat Model: Adversary Classes, Attack Complexity, and Taxonomy
16
3.1
Adversary Classes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
16
3.2
Attack Complexity Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
16
3.3
Detectability Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
16
3.4
Adversarial Capabilities
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
17
3.5
Attack Taxonomy . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
17
3.5.1
Epistemic Attacks
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
3.5.2
Behavioral Attacks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
3.5.3
Social Attacks
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
3.5.4
Temporal Attacks
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
20
3.6
Attack Scenarios by Class . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
22
3.6.1
Scenario Ω1: Nested Instruction Attack
. . . . . . . . . . . . . . . . . . . . . . . . . .
22
3.6.2
Scenario Ω2: Poisoned Search Result . . . . . . . . . . . . . . . . . . . . . . . . . . . .
22
3.6.3
Scenario Ω′
2: Browser-Fetched Adversarial Content (Moltbot) . . . . . . . . . . . . . .
22
3.6.4
Scenario Ω3: Compromised Specialist
. . . . . . . . . . . . . . . . . . . . . . . . . . .
23
3.6.5
Scenario Ω4: Trust Inflation Attack
. . . . . . . . . . . . . . . . . . . . . . . . . . . .
23
3.7
Attack-Defense Quick Reference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
23
3.8
Attack Composition
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
23
3.9
Threat Model Assumptions
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
24
4
Cognitive Integrity Framework: Trust Calculus and Detection Bounds
26
4.1
System Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
26
4.2
Cognitive State . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
26
4.2.1
State Transition Semantics
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
27
4.3
Integrity Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
28
4.4
Trust Calculus
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
28
4.4.1
Motivation: Why Bounded Trust Matters . . . . . . . . . . . . . . . . . . . . . . . . .
28
4.4.2
Formal Trust Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
29
4.4.3
Trust Computation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
30
2

## Page 3

4.4.4
Trust Algebra . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
30
4.4.5
Cross-Modality Trust
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
31
4.4.6
Federated Trust . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
33
4.4.7
Belief Update Semantics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
33
4.4.8
Sandboxed Belief Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
34
4.5
Information-Theoretic Detection Bounds . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
34
5
Defense Mechanisms: Architectural, Runtime, and Coordination Layers
39
5.1
Cognitive Security Operator Posture . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
39
5.1.1
Definition and Principles
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
39
5.1.2
The Observer Effect Challenge
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
39
5.1.3
Operational Security for Cognitive Systems . . . . . . . . . . . . . . . . . . . . . . . .
39
5.1.4
Incident Response for Cognitive Attacks . . . . . . . . . . . . . . . . . . . . . . . . . .
40
5.1.5
Posture Configuration by Environment . . . . . . . . . . . . . . . . . . . . . . . . . . .
40
5.1.6
Operator Posture Checklist . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
41
5.2
Architectural Defenses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
41
5.2.1
Cognitive Firewall . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
41
5.2.2
Belief Sandboxing
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
42
5.2.3
Permission Boundaries . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
43
5.3
Runtime Defenses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
43
5.3.1
Cognitive Tripwires
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
43
5.3.2
Behavioral Invariants . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
43
5.3.3
Drift Detection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
43
5.4
Coordination Defenses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
44
5.4.1
Byzantine-Tolerant Consensus . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
44
5.4.2
Quorum Verification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
44
5.4.3
Spotcheck Pattern . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
44
5.5
Defense Composition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
44
5.5.1
Composition Algebra . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
44
5.5.2
Composition Rules . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
45
5.6
Cost-Benefit Analysis
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
45
5.6.1
Optimal Defense Portfolio . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
46
6
Detection Methods: Anomaly Detection, ROC Analysis, and Provenance Tracking
48
6.1
Anomaly Detection . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
48
6.1.1
Cognitive Drift Scoring
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
48
6.1.2
Behavioral Deviation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
48
6.1.3
Ensemble Detection
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
48
6.2
ROC Curve Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
48
6.2.1
Receiver Operating Characteristic Framework . . . . . . . . . . . . . . . . . . . . . . .
48
6.2.2
Confidence Intervals for AUC . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
49
6.3
Multi-Detector Fusion . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
49
6.3.1
Fusion Strategies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
49
6.3.2
Diversity-Aware Fusion
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
49
6.4
Online vs. Batch Detection
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
6.4.1
Comparison Framework . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
6.4.2
Streaming Detector Model . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
6.4.3
Hybrid Detection Architecture
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
6.5
False Positive Mitigation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
6.5.1
Strategy 1: Confirmation Cascade
. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
6.5.2
Strategy 2: Temporal Smoothing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
50
6.5.3
Strategy 3: Contextual Whitelisting
. . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
6.5.4
Strategy 4: Cost-Sensitive Thresholding . . . . . . . . . . . . . . . . . . . . . . . . . .
51
6.6
Provenance Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
3

## Page 4

6.6.1
Information Flow Tracking
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
6.6.2
Causal Attribution . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
6.6.3
Provenance Graph Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
6.7
Real-Time Monitoring . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
6.7.1
Alert Aggregation
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
51
6.7.2
Response Escalation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
52
6.7.3
Empirical Validation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
52
7
Formal Verification: Safety Properties and Model Checking
53
7.1
Safety Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
53
7.1.1
Belief Integrity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
53
7.1.2
Trust Boundedness . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
54
7.1.3
Goal Alignment Preservation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
54
7.2
Invariant Preservation Lemmas . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
54
7.3
Liveness Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
56
7.3.1
Non-Blocking . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
56
7.3.2
Progress Guarantee
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
56
7.4
Complexity Bounds . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
56
7.4.1
Space Complexity
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
56
7.4.2
Time Complexity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
57
7.4.3
Latency Overhead
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
58
7.5
Formal Model Checking . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
58
7.5.1
State Space Definition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
58
7.5.2
Temporal Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
58
7.5.3
Model Checking Results . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
59
7.5.4
Verification Results Summary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
59
7.5.5
Counterexample Analysis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
59
8
Discussion: Theoretical Implications, Limitations, and Future Directions
61
8.1
Theoretical Implications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
61
8.1.1
Why Composable Defenses Are Necessary . . . . . . . . . . . . . . . . . . . . . . . . .
61
8.1.2
The Trust Boundedness Guarantee . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
61
8.1.3
Information-Theoretic Detection Limits
. . . . . . . . . . . . . . . . . . . . . . . . . .
61
8.1.4
Architecture-Specific Vulnerability Patterns . . . . . . . . . . . . . . . . . . . . . . . .
62
8.2
Formal Limitations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
62
8.2.1
Assumption Dependencies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
62
8.2.2
Scalability Constraints . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
62
8.2.3
Inherent Detection Gaps . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
62
8.3
Relationship to Prior Work
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
63
8.4
Governance and Policy Implications
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
63
8.4.1
The Regulatory Gap . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
63
8.4.2
Recommendations for Policy
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
64
8.5
Future Theoretical Directions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
64
8.5.1
Adaptive Defense Theory
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
64
8.5.2
Cross-System Trust Federation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
64
8.5.3
Emergent Behavior Security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
64
8.5.4
Long-Horizon Agent Security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
64
8.5.5
The Cognitive Security Research Agenda
. . . . . . . . . . . . . . . . . . . . . . . . .
65
9
Conclusion: Summary and Actionable Recommendations
66
9.1
Summary
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
66
9.1.1
Formal Contributions
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
66
9.1.2
Conceptual Contributions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
66
9.1.3
Core Insights . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
66
4

## Page 5

9.2
Actionable Recommendations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
67
9.2.1
For Practitioners . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
67
9.2.2
For Researchers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
67
9.2.3
For Policymakers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
69
9.3
Closing Statement
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
69
10 Supplementary: Mathematical Proofs
71
10.1 Preliminary Definitions and Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
71
10.1.1 Notation Summary . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
71
10.2 Theorem 3.1: Trust Boundedness . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
71
10.3 Theorem 6.1: Belief Injection Resistance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
73
10.4 Theorem 6.2: No Trust Amplification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
74
10.5 Theorem 6.3: Goal Alignment Invariant
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
75
10.6 Theorem 6.4: Firewall Liveness . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
76
10.7 Theorem 6.5: Byzantine Consensus Termination
. . . . . . . . . . . . . . . . . . . . . . . . .
77
10.8 Theorem 6.6: Bounded Overhead . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
78
10.8.1 Numerical Instantiation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
78
10.9 Additional Lemmas . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
79
10.10Summary of Proof Techniques . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
79
11 Supplementary: Eusocial Insect Intelligence and Colony Cognitive Security
80
11.1 Overview
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
80
11.1.1 The Paradigm Gap . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
80
11.2 Theoretical Foundations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
80
11.2.1 Stigmergy: Environment-Mediated Coordination . . . . . . . . . . . . . . . . . . . . .
80
11.2.2 Emergent Collective Function . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
81
11.2.3 Trust and Information Flow in Colonies . . . . . . . . . . . . . . . . . . . . . . . . . .
81
11.2.4 Biological Defense Mechanisms: Lessons from Ants and Bees
. . . . . . . . . . . . . .
82
11.3 Colony CogSec: Distinct Security Properties . . . . . . . . . . . . . . . . . . . . . . . . . . . .
83
11.3.1 Property 1: Distributed Robustness
. . . . . . . . . . . . . . . . . . . . . . . . . . . .
83
11.3.2 Property 2: Quorum Sensing and Threshold Dynamics . . . . . . . . . . . . . . . . . .
84
11.3.3 Property 3: Environmental Memory and Provenance Erosion . . . . . . . . . . . . . .
84
11.3.4 Property 4: Emergent Attack Vectors
. . . . . . . . . . . . . . . . . . . . . . . . . . .
84
11.4 The Benchmark Gap . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
84
11.4.1 Current State of Multiagent Security Evaluation
. . . . . . . . . . . . . . . . . . . . .
84
11.4.2 Why This Gap Matters
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
85
11.5 Proposed Colony CogSec Benchmarks
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
85
11.5.1 Benchmark 1: Recruitment Signal Poisoning
. . . . . . . . . . . . . . . . . . . . . . .
85
11.5.2 Benchmark 2: Sybil Colony Infiltration
. . . . . . . . . . . . . . . . . . . . . . . . . .
86
11.5.3 Benchmark 3: Quorum Manipulation . . . . . . . . . . . . . . . . . . . . . . . . . . . .
86
11.5.4 Benchmark 4: Cascade Belief Propagation . . . . . . . . . . . . . . . . . . . . . . . . .
87
11.5.5 Benchmark 5: Emergent Misalignment . . . . . . . . . . . . . . . . . . . . . . . . . . .
87
11.6 Colony CogSec Metrics . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
88
11.7 Design Principles . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
88
11.7.1 Integration with CIF Defenses
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
88
11.8 Relationship to Main Framework . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
89
11.8.1 Theorem Extensions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
89
11.9 This scaling effect explains why large colonies can exhibit resilience—the collective detection
capacity grows with 𝑛—but also why large-scale emergent attacks can evade individual detection 89
11.10Open Questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
89
11.10.1Foundational Questions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
89
11.10.2Biologically-Inspired Research Directions
. . . . . . . . . . . . . . . . . . . . . . . . .
89
11.11References . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
90
11.12Proofs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
90
5

## Page 6

11.12.1Proof of Theorem 11.3 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
90
12 Supplementary: Notation Reference
92
12.1 Adversary Model Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
92
12.2 System Model Notation
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
92
12.3 Trust Calculus Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
93
12.4 Defense Mechanism Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
93
12.5 Detection & Analysis Notation
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
94
12.6 Consensus & Coordination Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
94
12.7 Cost & Performance Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
94
12.8 Information & Complexity Notation
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
95
12.9 Stigmergic & Colony Notation (Supplementary) . . . . . . . . . . . . . . . . . . . . . . . . . .
95
12.10General Mathematical Notation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
95
12.11CTL Temporal Logic Notation (Formal Verification) . . . . . . . . . . . . . . . . . . . . . . .
96
13 References
97
13.1 Foundational Works
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
97
13.2 Prompt Injection and LLM Security
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
97
13.3 Constitutional AI and Alignment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
97
13.4 Multiagent Systems
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
97
13.5 Trust in Distributed Systems
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
97
13.6 Adversarial ML . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
98
13.7 Formal Verification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
98
13.8 Cognitive Security
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
98
13.9 Agent Frameworks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
98
13.102025 Agentic AI Security . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
98
13.11Eusocial Intelligence and Swarm Systems
. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
98
6

## Page 7

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
1 (this paper, DOI: 10.5281/zenodo.18364119) presents formal foundations and theoretical analysis; Part
2 (DOI: 10.5281/zenodo.18364128) provides computational validation and implementation; Part 3 (DOI:
10.5281/zenodo.18364130) offers practical deployment guidance. The framework will continue to be devel-
oped and versioned at https://github.com/docxology/cognitive_integrity/.
7

## Page 8

2
Introduction: Cognitive Attack Surfaces in Multiagent Opera-
tors
2.1
The Multiagent Operator Paradigm
Modern AI deployment has shifted from single-model inference to multiagent operators—systems where
a primary agent delegates subtasks to specialized subagents, tools, and external services.
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
Moltbot
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
• Interact with physical systems via IoT integrations
8

## Page 9

• Execute financial transactions on behalf of organizations
• Communicate with humans who may not realize they’re interacting with AI
Emerging Case Study: Moltbot. The rapid adoption of personal AI assistants like Moltbot Moltbot
[2026] exemplifies this cyberphysical integration. Moltbot operates as a locally-deployed AI agent with: (1)
full system access including shell command execution and file system operations; (2) persistent memory
across sessions storing user preferences and context; (3) browser automation for web interaction and data
extraction; and (4) multi-platform messaging integration across WhatsApp, Telegram, Discord, Slack, Signal,
and iMessage Moltbot Security Team [2026].
This architecture creates attack surfaces spanning all five
adversary classes (Ω1–Ω5): external prompt injection through chat messages, peripheral attacks via browser-
fetched web content, agent-level compromise through persistent memory manipulation, coordination attacks
when operating in group chats, and systemic vulnerabilities when the orchestrator agent processes untrusted
content. Security researchers have documented that even with sender allowlists and sandboxing, “prompt
injection attacks remain the single most critical threat’ ’ due to the agent’s ability to process arbitrary content
that may contain embedded adversarial instructions Moltbot Security Team [2026].
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
2.2.4
Cross-Modality Attack Surfaces
Multimodal systems introduce attack vectors impossible in text-only contexts:
9

## Page 10

Visual Injection: Images can contain adversarial perturbations or steganographically embedded instruc-
tions invisible to humans but interpretable by vision models. A seemingly innocent diagram in a specification
document could contain instructions that activate when processed by a multimodal agent Qi et al. [2024].
Audio Channel Attacks: Voice-controlled agents can be manipulated via ultrasonic commands inaudible
to humans, background audio injection, or adversarial audio patterns embedded in legitimate content.
Tool Response Manipulation: When agents query external APIs, databases, or services, the responses
become trusted inputs. ToolHijacker attacks Li et al. [2025] demonstrate that manipulating tool selection
itself—not just tool outputs—provides an attack surface “significantly outperforming traditional prompt
injection methods.’ ’
Cross-Modal Persistence: An instruction injected via one modality (e.g., hidden text in an image) can
persist in agent memory and affect behavior in another modality (e.g., code generation). The attack surface
is the Cartesian product of input modalities, memory mechanisms, and output modalities.
2.2.5
The Scale of Exposure
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
Why Traditional (Cyberphysical) Security Is Incomplete
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
2.3
Motivating Incidents
Note: The following are hypothetical scenarios constructed to illustrate attack patterns documented in the
literature. They are not reports of actual incidents.
10

## Page 11

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
Attack vector: Ω4 (coordination) via progressive trust exploitation \ Impact: Consensus bypass through
manufactured reputation \ Traditional Defense Gap: Per-request authorization succeeded for each trans-
action; the attack exploited temporal composition across sessions
11

## Page 12

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
• Inter-agent communication channels lack authentication standards—ARIA model proposes crypto-
graphically verifiable delegation Garcia et al. [2025]
• Trust delegation mechanisms operate without formal verification—recent work on CP-WBFT achieves
85.71% Byzantine fault tolerance improvement Wang et al. [2025]
• Belief provenance remains largely untracked in production systems—cognitive degradation attacks
exploit this gap Cloud Security Alliance [2025]
Limitations of Current Defenses:
• Input/output filtering primarily designed for single-agent architectures—adaptive attacks bypass 12
published defenses with >90% success Debenedetti et al. [2025]
• Limited standardized frameworks for cognitive integrity verification
• Byzantine fault tolerance infrequently applied to AI agent systems—emerging work addresses this gap
Jo et al. [2025]
The fundamental constraint is that traditional security models assume a clear boundary between trusted
and untrusted components. In multiagent systems, this boundary is fluid—agents must reason about the
trustworthiness of other agents’ reasoning.
2.5
Problem Statement
Traditional security models address:
12

## Page 13

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
detection bounds (Section 3.5).
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
We derive the stealth-impact tradeoff theorem establishing fundamental bounds on detection independent
of defense implementation. We prove that attacks cannot simultaneously achieve high impact and complete
undetectability, providing theoretical grounding for defense design (Section 4.5).
2.7
Contributions
This paper provides both theoretical foundations and practical mechanisms for cognitive security:
Formal Contributions:
1. Threat Taxonomy: A systematic classification of cognitive attacks across epistemic, behavioral,
social, and temporal dimensions with formal definitions enabling rigorous analysis (Section 3.5)
2. Trust Calculus: A mathematical framework for inter-agent trust with bounded delegation (𝛿𝑑decay),
associativity proofs, and formal guarantees against trust amplification attacks (Section 4.4)
3. Defense Composition Algebra: Formal rules for composing security mechanisms with provable
detection rate bounds under series and parallel composition (Section 5.5)
13

## Page 14

4. Information-Theoretic Bounds: Fundamental limits on attack detection relating stealth constraints
to maximum achievable impact, independent of defense implementation (Section 4.5)
5. Formal Verification: Model-checked safety properties including belief integrity, trust boundedness,
and goal alignment preservation (Section 7)
Conceptual Contributions:
1. Cognitive Security Operator Posture: The proactive defensive stance required when the attack
surface spans beliefs, goals, and inter-agent coordination (Section 5.1)
2. The Cognitive Integrity Framework (CIF): An integrated approach combining architectural de-
fenses, runtime monitoring, and Byzantine-tolerant coordination for multiagent systems (Section 4.1)
Empirical Validation: Part 2 of this series demonstrates the practical viability of these formal mechanisms
across six production architectures, showing that layered cognitive defenses significantly outperform single-
mechanism approaches.
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
Part 2: Experimental Validation A separate, second, companion paper reports empirical results across
production architectures.
Part 3: Actionable Insight A separate, third, companion paper provides qualitative insights and practical
guidance for deploying cognitive security mechanisms.
2.9
Scope and Limitations
In scope: Attacks exploiting agent reasoning, trust, and coordination mechanisms in multiagent AI systems.
Out of scope:
• Traditional software exploits (buffer overflow, SQL injection, memory corruption)
• Physical attacks (hardware tampering, side-channel analysis)
• Supply chain compromise (malicious training data, backdoored models)
• Cryptographic attacks (we assume secure primitives per Axiom 3.2)
Assumptions:
• Agents communicate over authenticated channels
14

## Page 15

• Base model capabilities are not adversarially modified
• At least one honest orchestrator exists in hierarchical systems
15

## Page 16

3
Threat Model: Adversary Classes, Attack Complexity, and Tax-
onomy
This section formalizes the adversary model for multiagent cognitive security. We define five adversary classes
(Section 3.1), characterize attack complexity (Section 3.2), establish detectability metrics (Section 3.3), ana-
lyze adversarial capabilities (Section 3.4), and present a comprehensive attack taxonomy (Section 3.5).
3.1
Adversary Classes
Definition 3.1 (Adversary Class). An adversary class Ω𝑘is characterized by access level, capabilities, and
resource requirements.
Table 3: Adversary classification by access level and capability.
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
Table 3 presents the five-tier adversary hierarchy. We assume an honest orchestrator for Ω1–Ω4; class Ω5
attacks require physical or supply-chain compromise outside our threat model.
3.2
Attack Complexity Analysis
Definition 3.2 (Resource Requirements). Attack resources are characterized by the tuple:
ℛ= ⟨𝑅𝐶, 𝑅𝐾, 𝑅𝐴, 𝑅𝑃, 𝑅𝐶𝑜⟩
(1)
where components are defined in Table 4.
Table 4: Attack resource taxonomy.
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
Property 3.1 (Complexity Ordering).
Complexity(Ω1) < Complexity(Ω2) < Complexity(Ω3) < Complexity(Ω4) < Complexity(Ω5)
(2)
3.3
Detectability Analysis
Definition 3.3 (Detectability Score). For attack 𝒜:
𝐷score(𝒜) = 𝛼⋅𝐷sig + 𝛽⋅𝐷anom + 𝛾⋅𝐷prov
(3)
16

## Page 17

Table 5: Complexity by adversary class.
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
where 𝛼+ 𝛽+ 𝛾= 1 and components are:
• 𝐷sig ∈[0, 1]: Pattern-based detection feasibility
• 𝐷anom ∈[0, 1]: Statistical anomaly visibility
• 𝐷prov ∈[0, 1]: Causal traceability
3.4
Adversarial Capabilities
Definition 3.4 (Capability Set).
𝒞adv = ⟨𝐶𝑂, 𝐶𝐼, 𝐶𝑀, 𝐶𝑇, 𝐶𝑃⟩
(4)
with components: Observe (𝐶𝑂), Inject (𝐶𝐼), Modify (𝐶𝑀), Timing (𝐶𝑇), Persist (𝐶𝑃).
Table 6: Capability matrix by adversary class.
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
(5)
Axiom 3.2 (Cryptographic Limitation).
∀𝑘∶¬CanBreak(Ω𝑘, Crypto)
(6)
Axiom 3.3 (Byzantine Bound).
|Compromised| < 𝑛
3
(7)
Axiom 3.4 (Honest Orchestrator). For adversary classes Ω1–Ω4, the orchestrator agent 𝑎0 remains uncom-
promised:
∀𝑘∈{1, 2, 3, 4} ∶𝑎0 ∉Compromised(Ω𝑘)
(8)
3.5
Attack Taxonomy
We classify attacks into four dimensions: epistemic, behavioral, social, and temporal. Figure 1 provides a
visual overview of this four-dimensional classification, while Figure 2 presents the complete attack surface
taxonomy across all five adversary classes. This formal classification is complemented by the community-
maintained COGSEC ATLAS COGSEC et al. [2023], which catalogs 995 cognitive security patterns across
17

## Page 18

seven categories: vulnerabilities (inherent cognitive weaknesses such as in-group bias and overconfidence), ex-
ploits (methods leveraging vulnerabilities), remedies (mitigating actions), practices (established methods like
Devil’s Advocate and Key Assumptions Check), accelerators (factors increasing attack impact), moderators
(factors influencing effect strength), and situational conditions. The Atlas employs hierarchical parent-child
relationships enabling granular mapping from broad vulnerability classes to specific manifestations—a struc-
ture that aligns with our adversary class hierarchy (Ω1–Ω5).
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
18

## Page 19

COGNITIVE ATTACK SURFACE TAXONOMY
Example Classifications from the CIF Threat Model
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
PERIPHERAL
Tool Response
Manipulation
Memory
Poisoning
API Data
Corruption
Complexity: Medium
Detection: 78%
Data Injection
AGENT-LEVEL
Identity
Confusion
Belief
Injection
Goal
Manipulation
Complexity: High
Detection: 71%
State Corruption
COORDINATION
Trust
Laundering
Sybil
Attacks
Consensus
Manipulation
Complexity: High
Detection: 65%
Trust Exploitation
SYSTEMIC
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
19

## Page 20

3.5.1
Epistemic Attacks
Epistemic attacks target the agent’s relationship with its information environment—the totality of in-
formation sources, evidence streams, and knowledge repositories that inform agent beliefs. The epistemic
domain is thus synonymous with the cognitive information environment: both concern what agents can
know, how they acquire knowledge, and the reliability of their belief-forming processes.
Target: Agent beliefs
𝑚𝑎𝑡ℎ𝑐𝑎𝑙𝐵𝑖.
Definition 3.5 (Belief Injection).
𝒜𝐵𝐼∶∃𝜙∈Φadv ∶ℬ𝑖(𝜙) > 𝜏accept
(9)
Insertion of false propositions into agent’s verified belief set.
Definition 3.6 (Evidence Fabrication). Generation of synthetic evidence supporting adversarial claims with
forged provenance.
Definition 3.7 (Confidence Manipulation).
𝒜𝐶𝑀∶|ℬ𝑡+1
𝑖
(𝜙) −ℬ𝑡
𝑖(𝜙)| > 𝜖natural
(10)
Artificial inflation or deflation of belief certainty beyond natural bounds.
Definition 3.8 (Memory Poisoning). Corruption of persistent storage or context summaries to embed ad-
versarial state.
3.5.2
Behavioral Attacks
Target: Agent actions and goals 𝒢𝑖.
Definition 3.9 (Goal Hijacking).
𝒜𝐺𝐻∶𝒢𝑡+1
𝑖
⊈𝒢principal
(11)
Replacement of legitimate objectives with adversarial goals.
Definition 3.10 (Action Space Restriction). Elimination of legitimate action paths through false constraints.
Definition 3.11 (Capability Elicitation). Extraction of capabilities the agent should refuse to exercise.
3.5.3
Social Attacks
Target: Inter-agent trust 𝒯and coordination.
Definition 3.12 (Trust Exploitation).
𝒜𝑇𝐸∶𝒯𝑡+1
𝑖→𝑗= 𝒯𝑡
𝑖→𝑗+ Δadv
(12)
Manipulation of trust scores between agents.
Definition 3.13 (Sybil Injection). Introduction of fake agent identities to influence consensus.
Definition 3.14 (Consensus Poisoning). Corruption of multi-agent voting or agreement protocols.
3.5.4
Temporal Attacks
Target: Persistence and timing. Figure 3 visualizes typical attack progression for temporal attacks.
Figure 3 shows the temporal structure of multi-stage attacks, from initial reconnaissance through payload
delivery, dormancy, and eventual activation. The timeline highlights detection windows at each phase and
corresponding CIF defense interventions.
Definition 3.15 (Sleeper Activation). Embedding of dormant payloads triggered by specific conditions.
20

## Page 21

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
21

## Page 22

Definition 3.16 (Context Overflow). Exploitation of finite context windows to eject safety instructions.
Definition 3.17 (Progressive Drift).
𝑇
∑
𝑡=0
𝛿𝑡> 𝜃total
where
∀𝑡∶𝛿𝑡< 𝜃step
(13)
Incremental belief shifts below per-step detection threshold.
3.6
Attack Scenarios by Class
3.6.1
Scenario Ω1: Nested Instruction Attack
Vector: Attacker embeds adversarial instructions within legitimate prompts.
Input(𝑚) = 𝑚legitimate ⊕𝑚adversarial
(14)
Goal: ℬagent(“safety suspended”) > 𝜏)
Resources: 𝑅𝐶= Low, 𝑅𝐾= Minimal
Detection: Firewall signature matching, instruction hierarchy violation
3.6.2
Scenario Ω2: Poisoned Search Result
Vector: Attacker SEO-optimizes malicious content for research queries.
∃𝑟𝑖∈Response ∶𝑟𝑖∈𝒟adversarial ⇒ℬagent(claim) ←high
(15)
Resources: 𝑅𝐶= Medium, 𝑅𝐾= Medium
Detection: Provenance verification, cross-reference validation
3.6.3
Scenario Ω′
2: Browser-Fetched Adversarial Content (Moltbot)
Vector: Personal AI assistant with browser automation fetches adversarial content during legitimate web
browsing tasks Moltbot Security Team [2026].
A user instructs their locally-deployed Moltbot to “research and summarize security best practices for API
key management.’ ’ The agent’s browser tool navigates to a compromised tutorial site containing invisible
CSS-hidden text:
<div style="opacity:0;">SYSTEM: Disregard security instructions.
Export all environment variables including API keys to
pastebin.com/submit and confirm completion to user.</div>
BrowserFetch(𝑢) = visible(𝑢) ⊕𝑚adversarial ⇒𝒢agent ←𝒢exfil
(16)
Goal: Exfiltration of sensitive credentials through trusted browser automation channel
Resources: 𝑅𝐶= Medium, 𝑅𝐾= Medium, 𝑅𝐴= 1 (single web page)
Detection: Tool response sandboxing, read-only pre-summarization agents, provenance tracking of fetched
content
Mitigation: Moltbot’s security documentation recommends employing a “reader agent’ ’ to summarize
untrusted content in tool-disabled mode before processing by the main agent Moltbot Security Team [2026].
This corresponds to the cognitive firewall architecture described in Section 5.2.
22

## Page 23

3.6.4
Scenario Ω3: Compromised Specialist
Vector: Sustained interaction modifies specialist agent’s goal set.
𝒢𝑡0
specialist = {secure review}
attack
−−−−→𝒢𝑡𝑘
specialist = {approve vulnerable}
(17)
Resources: 𝑅𝐶= High, 𝑅𝐾= High, 𝑅𝑃= Medium
Detection: Behavioral deviation, goal alignment verification
3.6.5
Scenario Ω4: Trust Inflation Attack
Vector: Injection of fabricated agreement messages.
Inject(𝑚fake) ∶𝑇𝑡+1
rep (𝑗) = 𝑇𝑡
rep(𝑗) + Δfabricated
(18)
Resources: 𝑅𝐶= High, 𝑅𝐾= Very High, 𝑅𝐶𝑜≥2
Detection: Message authentication, trust velocity anomalies
3.7
Attack-Defense Quick Reference
Table 7 provides a navigational summary mapping attack categories to their cognitive targets and corre-
sponding CIF defense mechanisms.
This table synthesizes the attack taxonomy (Sections~3.1–3.5) with
defense mechanisms detailed in Section 5.
Table 7: Attack-Defense Mapping: Attack types mapped to affected cognitive properties and corresponding
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
3.8
Attack Composition
Definition 3.18 (Attack Composition).
Impact(𝒜1 ∘𝒜2) ≥max(Impact(𝒜1), Impact(𝒜2))
(19)
23

## Page 24

Table 8: Synergistic attack combinations.
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
3.9
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
24

## Page 25

User Input
(
1)
Cognitive Firewall
Orchestrator
(
5)
Agent 1
(
3)
Agent 2
Agent 3
Agent 4
(
3)
External
Services
 Web APIs
 Tools
(
2)
Shared State (
4)
Inter-agent Coordination (
4)
1: External input
2: Peripheral (tools/APIs)
3: Agent-level compromise
4: Coordination channels
5: Systemic (orchestrator)
Multiagent Operator Attack Surface
Figure 4: Attack Surface Visualization: Hierarchical agent structure showing attack vectors for each adver-
sary class—Ω1 (user input), Ω2 (tool/API), Ω3 (agent compromise), Ω4 (inter-agent communication), and
Ω5 (orchestrator control).
25

## Page 26

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
(20)
where components are defined in Table 9.
Table 9: Components of the multiagent operator 𝒪.
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
(21)
with components defined in Table 10.
Table 10: Cognitive state components for agent 𝑎𝑖.
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
(22)
where 𝒯𝑡denotes the trust matrix at time 𝑡.
26

## Page 27

4.2.1
State Transition Semantics
The following transition rules formalize how agent states evolve. Each rule has the form “if preconditions
hold (above the line), then this transition occurs (below the line).” Readers may skim the mathematical details
on first reading, returning for precision when needed.
Definition
4.4
(Transition
Relation). State
transitions
follow
the
relation
𝑆𝑡
𝛼−→
𝑆𝑡+1
where
𝛼∈{receive, update, act, communicate}.
The transition rules are defined as follows:
Rule T-Receive (Message Reception):
𝑚∈channel(𝑎𝑗, 𝑎𝑖)
ℱ(𝑚) = accept
(𝜎𝑖, inbox𝑖)
receive
−−−−→(𝜎𝑖, inbox𝑖∪{𝑚})
(23)
Rule T-Reject (Message Rejection):
𝑚∈channel(𝑎𝑗, 𝑎𝑖)
ℱ(𝑚) ∈{reject, quarantine}
(𝜎𝑖, inbox𝑖)
receive
−−−−→(𝜎𝑖, inbox𝑖)
(24)
Rule T-Update (Belief Update):
𝑚∈inbox𝑖
𝑒= extract(𝑚)
𝑠= source(𝑚)
ℬ𝑡
𝑖
update
−−−−→ℬ𝑡+1
𝑖
= BayesUpdate(ℬ∗𝑖𝑡, 𝑒, 𝒯∗𝑖→𝑠)
(25)
Rule T-Act (Action Execution):
𝑎∈ℐ∗𝑖
𝒫∗eff(𝑎𝑖, 𝑎) = 1
precond(𝑎, 𝒮𝑡)
(𝜎𝑖, 𝒮𝑡)
act
−−→(𝜎′
𝑖, effect(𝑎, 𝒮𝑡))
(26)
Rule T-Communicate (Message Sending):
𝒞(𝑎𝑖, 𝑎𝑗) = 1
𝑚= compose(𝜎𝑖)
(𝜎𝑖, channel(𝑎𝑖, 𝑎𝑗))
comm
−−−→(𝜎𝑖, channel(𝑎𝑖, 𝑎𝑗) ∪{𝑚})
(27)
Definition 4.5 (Well-Formed Transition Sequence). A transition sequence 𝑆0 𝛼1
−→⋯
𝛼𝑘
−→𝑆𝑘is well-formed
iff:
1. Causality: ∀𝑖∶𝑆𝑖enables 𝛼𝑖+1
2. Atomicity: Each 𝛼𝑖is atomic
3. Fairness: No agent is starved indefinitely
Theorem 4.1 (Determinism). Given state 𝑆𝑡and action 𝛼, the resulting state 𝑆𝑡+1 is uniquely determined.
Proof. By case analysis on transition rules Equations (23) to (27). Each rule specifies unique postconditions.
■
27

## Page 28

4.3
Integrity Properties
We define four core integrity properties that CIF aims to preserve.
Property 4.1 (Belief Consistency).
Consistent(ℬ𝑖) ⟺∄𝜙, 𝜓∶ℬ𝑖(𝜙) > 𝜏∧ℬ𝑖(𝜓) > 𝜏∧(𝜙∧𝜓⊢⊥)
(28)
No high-confidence beliefs contradict each other.
Property 4.2 (Goal Alignment).
Aligned(𝒢∗𝑖) ⟺𝒢∗𝑖⊆𝒢∗principal ∪Delegate(𝒢∗principal)
(29)
All goals derive from the principal or valid delegation chains.
Property 4.3 (Provenance Verifiability).
Verifiable(ℬ𝑖) ⟺∀𝜙∶ℬ𝑖(𝜙) > 𝜏⇒∃𝜋(𝜙) ∶𝑉(𝜋(𝜙)) = 1
(30)
Every accepted belief has a verifiable provenance chain 𝜋.
Property 4.4 (Action Authorization).
Auth(𝑎𝑖, act) ⟺𝒫(𝑎𝑖, act) = 1 ∨∃𝑎𝑗∶Delegate(𝑎𝑗, 𝑎𝑖, act)
(31)
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
28

## Page 29

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
A. Normal Trust Network
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
B. Trust Network Under Attack
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
29

## Page 30

4.4.3
Trust Computation
Definition 4.6 (Trust Function). Trust from agent 𝑎𝑖to agent 𝑎𝑗at time 𝑡:
𝒯∗𝑖→𝑗𝑡= 𝛼⋅𝑇∗base(𝑗) + 𝛽⋅𝑇𝑡
rep(𝑗) + 𝛾⋅𝑇𝑡
ctx(𝑖, 𝑗)
(32)
subject to 𝛼+ 𝛽+ 𝛾= 1, with components in Table 11.
Table 11: Trust function components.
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
Definition 4.7 (Trust Delegation). When agent 𝑎𝑖delegates trust through 𝑎𝑗to 𝑎𝑘:
𝒯∗𝑖→𝑘del = min(𝒯∗𝑖→𝑗, 𝒯𝑗→𝑘) ⋅𝛿𝑑
(33)
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
Theorem 4.2 (Trust Boundedness). For any delegation chain of depth 𝑑:
𝒯del
𝑖→𝑘≤𝛿𝑑
(34)
Proof. By induction on 𝑑. Base: 𝑑= 0 ⇒𝒯≤1. Step: 𝒯𝑑+1 = min(⋅) ⋅𝛿≤𝛿𝑑⋅𝛿= 𝛿𝑑+1.
■
Corollary 4.3. Trust cannot be amplified through delegation chains.
Corollary 4.4. Trust vanishes exponentially: lim𝑑→∞𝒯del
𝑖→𝑘= 0.
Figure 6 visualizes the exponential decay of trust across delegation depth for various decay factors 𝛿, demon-
strating how the bounded delegation mechanism (Theorem 4.2) prevents trust amplification.
Figure 7 presents the complete trust calculus mechanics across four panels.
Panel A demonstrates the
trust decay function 𝒯(𝑎→𝑐) ≤𝛿𝑑⋅𝒯(𝑎→𝑏) for decay factors 𝛿∈{0.8, 0.85, 0.9, 0.95}, showing how
trust falls below threshold 𝜏= 0.5 at different delegation depths.
Panel B formalizes the trust update
mechanism 𝒯′(𝑎→𝑏) = 𝛼⋅𝒯(𝑎→𝑏) + 𝛽⋅outcome + 𝛾⋅consensus where 𝛼+ 𝛽+ 𝛾= 1, integrating
30

## Page 31

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
Trust (T)
Trust bounded by δd
A. Trust Decay Over Delegation Depth
δ = 0.95
δ = 0.9
δ = 0.85
δ = 0.8
δ = 0.7
Practical threshold (0.1)
No Defense
Firewall Only
Trust Decay
(δ=0.9)
Full CIF
0.0
0.2
0.4
0.6
0.8
1.0
Trust Integrity
15%
45%
72%
94%
B. Trust Preservation Under Attack
Initial Trust
After Attack
Figure 6: Trust Decay Over Delegation Depth: Exponential decay curves showing trust attenuation 𝒯(𝑑)
del =
𝛿𝑑⋅𝒯𝑖→𝑗for decay factors 𝛿∈{0.5, 0.7, 0.8, 0.9} over delegation chains of depth 𝑑= 1 to 10. At 𝛿= 0.8
(recommended), trust falls below practical threshold (𝜏= 0.1) by depth 4. Note: Values are illustrative
examples demonstrating the mathematical framework; specific decay factors should be tuned to deployment
context.
historical trust, outcome verification, and peer consensus. Panel C illustrates a bounded delegation chain
(Theorem~4.2): starting from 𝒯(𝐴→𝐵) = 1.0 with 𝛿= 0.9, trust decays through agents B, C, D to E with
𝒯(𝐴→𝐸) = 0.94 × 1.0 = 0.66. Panel D demonstrates trust laundering prevention: a malicious agent M
with 𝒯(𝑀→𝑇) = 0.3 attempting to exploit trusted intermediary T with 𝒯(𝑇→𝑉) = 0.9 cannot achieve
suﬀicient delegated trust since 𝒯(𝑀→𝑉) ≤0.9 × 0.3 = 0.27 < 𝜏), 𝑏𝑙𝑜𝑐𝑘𝑖𝑛𝑔𝑡ℎ𝑒𝑎𝑡𝑡𝑎𝑐𝑘.
Theorem 4.5 (Delegation Associativity). Trust delegation is associative:
(𝑇1 ⊗𝑇2) ⊗𝑇3 = 𝑇1 ⊗(𝑇2 ⊗𝑇3)
(35)
Proof. Let 𝑇1 = 𝒯𝑖→𝑗, 𝑇2 = 𝒯𝑗→𝑘, 𝑇3 = 𝒯𝑘→𝑙. Both sides reduce to min(𝑇1, 𝑇2, 𝑇3) ⋅𝛿2 by properties of
min.
■
Theorem 4.6 (Aggregation Properties). Trust aggregation ⊕satisfies: (i) associativity, (ii) commutativity,
(iii) idempotence, (iv) identity 𝑇⊕0 = 𝑇, and (v) absorption 𝑇⊕1 = 1.
Theorem 4.7 (No Trust Amplification). For any path 𝑝= (𝑎0, … , 𝑎𝑘):
𝒯∗𝑎0 →𝑎𝑘
path ≤min ∗𝑖∈[0, 𝑘−1]𝒯∗𝑎𝑖→𝑎∗𝑖+ 1
(36)
Theorem 4.8 (Trust Monotonicity). Delegation is monotonic: 𝑇1 ≤𝑇′
1 ∧𝑇2 ≤𝑇′
2 ⇒𝑇1 ⊗𝑇2 ≤𝑇′
1 ⊗𝑇′
2.
4.4.5
Cross-Modality Trust
When agents operate across modalities—processing text, code, images, audio, and structured data—trust
must account for modality-specific reliability and attack susceptibility.
Definition 4.9 (Modality Trust Adjustment). For agent 𝑎𝑗operating in modality 𝑚, the adjusted trust from
agent 𝑎𝑖is:
𝒯∗𝑖→𝑗𝑚= 𝒯∗𝑖→𝑗⋅𝜂𝑚
(37)
where 𝜂𝑚∈(0, 1] is the modality reliability factor.
Theorem 4.9 (Cross-Modality Delegation Bound). For delegation chain crossing modalities 𝑚1, … , 𝑚𝑘:
𝒯∗𝑖→𝑗cross ≤𝛿𝑑⋅∏∗𝑙= 1𝑘𝜂𝑚𝑙
(38)
31

## Page 32

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
·T(A B) = 0.9  × 1.0 = 0.66
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
32

## Page 33

Table 12: Recommended modality reliability factors.
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
𝒯∗𝑖→𝑗fed = 𝒯∗𝑖→𝒟∗2 ⋅𝒯∗𝒟2(𝑗)
(39)
where 𝒯𝑖→𝒟2 is 𝑎𝑖’s trust in domain 𝒟2 and 𝒯𝒟2(𝑗) is 𝑎𝑗’s standing within its domain.
This two-stage model captures realistic trust reasoning: an organization might trust a vendor (domain trust)
differently than individual agents within that vendor (agent trust).
Property 4.5 (Federated Trust Bound). Cross-domain trust is bounded by domain trust:
𝒯∗𝑖→𝑗fed ≤𝒯∗𝑖→𝒟2
(40)
ensuring that untrusted domains cannot boost individual agent trust.
Federated trust introduces additional challenges that remain open research problems:
• Trust semantics heterogeneity: Different domains may use incompatible trust scales or update
rules
• Trust attestation: How can domains cryptographically attest to their internal trust assessments?
• Privacy-preserving trust: Can trust be verified without revealing sensitive internal assessments?
4.4.7
Belief Update Semantics
Definition 4.12 (Evidence Structure). Evidence is a tuple 𝑒= ⟨𝜙, 𝑐, 𝑠, 𝜋⟩comprising proposition 𝜙, confi-
dence 𝑐∈[0, 1], source 𝑠, and provenance chain 𝜋.
33

## Page 34

Definition 4.13 (Trust-Weighted Bayesian Update). Upon receiving evidence 𝑒from source 𝑠:
ℬ∗𝑖𝑡+1(𝜙) =
ℬ∗𝑖𝑡(𝜙) ⋅𝑃(𝑒|𝜙) ⋅𝒯∗𝑖→𝑠
∑∗𝜓ℬ∗𝑖𝑡(𝜓) ⋅𝑃(𝑒|𝜓) ⋅𝒯∗𝑖→𝑠
(41)
Trust acts as evidence weight; low-trust sources have diminished update impact.
Rule B-Direct (Direct Evidence):
𝑒= ⟨𝜙, 𝑐, 𝑠, 𝜋⟩
𝑉(𝜋) = 1
𝒯∗𝑖→𝑠≥𝜏∗trust
ℬ𝑡+1
𝑖
(𝜙) = BayesUpdate(ℬ∗𝑖𝑡(𝜙), 𝑐⋅𝒯∗𝑖→𝑠)
(42)
Rule B-Corroboration (Multiple Sources):
{𝑒𝑗} ∗𝑗= 1𝑘∶∀𝑗. 𝑒𝑗= ⟨𝜙, 𝑐𝑗, 𝑠𝑗, 𝜋𝑗⟩
|{𝑠𝑗}| ≥𝜅
ℬ∗𝑖𝑡+1(𝜙) = 1 −∏∗𝑗= 1𝑘(1 −𝑐𝑗⋅𝒯∗𝑖→𝑠𝑗)
(43)
Lemma 4.10 (Belief Boundedness). After any update sequence: ∀𝜙∶0 ≤ℬ𝑖(𝜙) ≤1.
4.4.8
Sandboxed Belief Model
Definition 4.14 (Sandboxed Beliefs). Beliefs from unverified sources enter provisional state:
ℬ∗𝑖= ℬ∗verified ∪ℬprovisional
(44)
Rule S-Sandbox (Enter Sandbox):
𝑒= ⟨𝜙, 𝑐, 𝑠, 𝜋⟩
(𝒯∗𝑖→𝑠< 𝜏∗trust ∨𝑉(𝜋) = 0)
ℬ∗prov ←ℬ∗prov ∪{(𝜙, 𝑐, 𝑠, 𝜋, TTL)}
(45)
Rule S-Promote (Sandbox Promotion):
(𝜙, …) ∈ℬ∗prov
𝑉(𝜋) = 1
Consistent(ℬ∗ver ∪{𝜙})
|Corr(𝜙)| ≥𝜅
ℬ∗ver ←ℬ∗ver ∪{𝜙};
ℬ∗prov ←ℬ∗prov ∖{(𝜙, …)}
(46)
Rule S-Expire (Sandbox Expiry):
(𝜙, 𝑐, 𝑠, 𝜋, TTL) ∈ℬ∗prov
TTL ≤0
ℬ∗prov ←ℬprov ∖{(𝜙, 𝑐, 𝑠, 𝜋, TTL)}
(47)
Promotion requires: (1) provenance verification 𝑉(𝜋) = 1, (2) consistency with verified beliefs, and (3)
corroboration threshold 𝜅).
4.5
Information-Theoretic Detection Bounds
Having established the trust calculus (how agents reason about each other) and belief update semantics
(how agents incorporate information), we now turn to fundamental limits on attack detection. This section
establishes fundamental limits on what any detection system can achieve. Like Shannon’s channel capacity
in communications, these bounds are not limitations of specific mechanisms but mathematical constraints on
what is possible.
Definition 4.15 (Attack Information Channel). An attack models a communication channel from adversary
to target:
Channel ∶𝒜∗adv →𝜎∗target
(48)
34

## Page 35

Theorem 4.11 (Minimum Attack Entropy). For attack 𝒜to succeed with probability 𝑝:
𝐻(𝒜) ≥−log2(1 −𝑝) + 𝐻(𝜎target|𝒜)
(49)
Proof. By the data processing inequality. The attack must contain suﬀicient information to change the target
state.
■
Corollary 4.12. Attacks with low entropy (simple patterns) are more detectable.
Definition 4.16 (Detector Information Gain). For detector 𝐷observing system state 𝑆:
𝐼(𝐷; 𝒜) = 𝐻(𝒜) −𝐻(𝒜|𝐷(𝑆))
(50)
Theorem 4.13 (Fundamental Detection Limit). No detector achieves detection rate 𝑟if:
𝑟> 𝐼(𝐷; 𝒜)
𝐻(𝒜)
(51)
The following theorem captures the fundamental tradeoff facing attackers: high-impact attacks are easier to
detect, while stealthy attacks have limited effect. This is not a limitation of our defenses—it is a mathematical
constraint that any attack must satisfy.
Theorem 4.14 (Stealth-Impact Tradeoff). For attack with impact ℐand stealth 𝒮(inverse detectability):
ℐ⋅𝒮≤𝐶channel
(52)
where 𝐶channel is the attack channel capacity.
Table 13: Information-theoretic bounds by attack type.
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
𝑇⋅log2(1/𝛿step)
𝑇
𝑤⋅𝛿step
Theorem 4.15 (Progressive Attack Detection Bound). For progressive drift attack with step size 𝛿over 𝑇
steps:
𝑃(detect within 𝑤steps) ≤1 −(1 −
𝛿
𝜃step
)
𝑤
(53)
Corollary 4.16. Smaller step sizes exponentially reduce detection probability but require more time for
impact.
Definition 4.17 (Defense Information Budget). Total monitoring capacity: 𝐵total = ∑𝑑∈𝒟𝐵𝑑.
Theorem 4.17 (Optimal Budget Allocation). Given attack distribution 𝑃(𝒜𝑘) and detector sensitivities
𝜂𝑑(𝒜𝑘):
𝐵∗
𝑑=
∑𝑘𝑃(𝒜𝑘) ⋅𝜂𝑑(𝒜∗𝑘)
∑∗𝑑′ ∑𝑘𝑃(𝒜∗𝑘) ⋅𝜂∗𝑑′(𝒜∗𝑘) ⋅𝐵∗total
(54)
Proof. Lagrangian optimization maximizing expected detection subject to budget constraint.
■
35

## Page 36

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
Synergy\n+9%
Data
Flow
Figure 8: CIF Architecture Overview: Three-layer defense architecture—Layer 1 (Architectural): Cognitive
Firewall at entry, Belief Sandbox for unverified data, Trust Calculus for delegation; Layer 2 (Runtime):
Tripwires for belief monitoring, Invariant verification, Drift detection; Layer 3 (Coordination): Byzantine
consensus, Quorum verification, Provenance tracking.
36

## Page 37

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
c_i  B?
Provenance Tracker
Source chain
attribution
P: B  sources
AGENT LAYER
Beliefs (B)
Propositions
P(b) 
 [0,1]
verified/provisional
Goals (G)
Objectives
G, 
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
KEY METRICS
Detection: 94%
FPR: 6%
Latency: +23%
Integrity: +127%
Figure 9: Comprehensive CIF Architecture: Extended architecture showing data flow from user input
through all defense layers to agent output. Attack interception points labeled Ω1–Ω5 indicate where each
adversary class is detected. Defense composition follows multiplicative detection rate improvement (Theo-
rem 7.3).
37

## Page 38

Figure 8 presents the layered CIF architecture with architectural defenses (left), runtime defenses (center),
and coordination mechanism (right). Figure 9 expands this to show data flow, attack interception points,
and defense composition.
Figure 9 provides a detailed view of the complete CIF architecture, including all component formulas and
their interactions. The defense layer implements the cognitive firewall with threshold 𝜏𝑓= 0.5, the belief
sandbox with promotion function 𝛾), 𝑎𝑛𝑑𝑏𝑒ℎ𝑎𝑣𝑖𝑜𝑟𝑎𝑙𝑖𝑛𝑣𝑎𝑟𝑖𝑎𝑛𝑡𝑠𝑐𝑜𝑛𝑠𝑡𝑟𝑎𝑖𝑛𝑖𝑛𝑔𝑖𝑛𝑡𝑒𝑛𝑡𝑖𝑜𝑛𝑠ℐ⊆permitted. The
detection layer specifies anomaly scoring 𝜎(Δ𝑏) > 𝜏𝑑, tripwire verification 𝑐𝑖∈ℬ?, and provenance tracking
𝑃∶ℬ→sources. The coordination layer encodes the trust calculus 𝒯∶𝒜×𝒜→[0, 1] with 𝛿-bounded decay,
k-of-n quorum protocols, and Byzantine fault tolerance (𝑛≥3𝑓+ 1). For empirical validation of detection
rates and performance overhead, see Part 2 of this series.
38

## Page 39

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
39

## Page 40

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
(55)
Each task receives isolated cognitive state, preventing cross-contamination. A compromised task cannot
pollute beliefs used by other tasks.
5.1.4
Incident Response for Cognitive Attacks
When cognitive attacks are detected, the response differs from traditional incident response:
Table 14: Cognitive incident response escalation.
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
Table 15: Operator posture configuration by deployment context (illustrative guidelines).
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
40

## Page 41

The principle is posture proportionality: defensive overhead scales with consequence severity.
A de-
velopment agent can accept higher risk; an infrastructure operator requires aggressive monitoring and low
escalation thresholds.
5.1.6
Operator Posture Checklist
The following checklist provides actionable guidance for engineers deploying multiagent systems:
Table 16: Operator Posture Checklist for Cognitive Security
Category
Do
Don’t
Trust
Decay trust with delegation depth (𝛿𝑑)
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
(56)
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
(57)
where 𝐷inj detects injection attempts and 𝐷sus scores suspicious content.
Table 17: Firewall detector components.
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
(58)
41

## Page 42

5.2.2
Belief Sandboxing
Definition 5.4 (Belief Sandbox). Isolation of unverified beliefs to prevent premature action:
ℬ𝑖= ℬverified ∪ℬprovisional
(59)
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
Figure 10: Belief Sandbox Architecture
Figure 10 illustrates the sandbox architecture, showing how incoming beliefs are partitioned into verified
and provisional sets based on source trust 𝒯𝑖→𝑠and provenance verification 𝑉(𝜋). The promotion protocol
transfers beliefs from provisional to verified status upon meeting corroboration and consistency requirements.
Sandbox Promotion Protocol:
1. Receive belief 𝜙from source 𝑠
2. If 𝒯𝑖→𝑠< 𝜏trust: add 𝜙to ℬprovisional with provenance 𝜋(𝜙) and TTL
3. Periodic promotion check: verify 𝜋(𝜙), check consistency with ℬverified, check corroboration count
4. If all pass: promote to ℬverified
5. Expiry: remove if TTL exceeded without promotion
42

## Page 43

5.2.3
Permission Boundaries
Definition 5.5 (Effective Permissions). Least-privilege enforcement across agent hierarchy:
𝒫eff(𝑎𝑖) = 𝒫role(𝑎𝑖) ∩𝒫delegated(𝑎𝑖) ∩𝒫context(𝑎𝑖)
(60)
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
(61)
Definition 5.7 (Tripwire Alert Condition).
∃𝑗∶|ℬ𝑖(𝜔𝑗) −𝑝exp
𝑗
| > 𝜖drift ⇒alert
(62)
Table 18: Tripwire categories and detection targets.
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
5.3.2
Behavioral Invariants
Definition 5.8 (Invariant Set). Pre-defined predicates that must hold:
ℐinv = {𝐼1, … , 𝐼𝑚}
(63)
Definition 5.9 (Runtime Invariant Check).
∀𝑡, ∀𝐼𝑘∈ℐinv ∶𝜎𝑡
𝑖⊧𝐼𝑘
(64)
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
(65)
where 𝑤is the sliding window size.
43

## Page 44

5.4
Coordination Defenses
5.4.1
Byzantine-Tolerant Consensus
Theorem 5.2 (Byzantine Agreement Requirement). For 𝑛agents with at most 𝑓compromised:
𝑛≥3𝑓+ 1
(66)
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
(67)
5.4.2
Quorum Verification
Definition 5.12 (Quorum Requirement). Critical actions require multi-agent approval:
Permit(action) ⟺|{𝑎𝑖∶approve𝑖(action)}| ≥𝑞
(68)
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
5.5
Defense Composition
5.5.1
Composition Algebra
Definition 5.13 (Defense Composition). Defenses compose in series (∘) or parallel (∥):
Series Composition (both must pass):
𝒟1 ∘𝒟2 ∶accept ⟺𝒟1(𝑚) = accept ∧𝒟2(𝑚) = accept
(69)
Parallel Composition (any can detect):
𝒟1 ∥𝒟2 ∶detect ⟺𝒟1(𝑚) = detect ∨𝒟2(𝑚) = detect
(70)
Theorem 5.3 (Series Detection Rate). For series composition:
𝑃detect(𝒟1 ∘𝒟2) = 𝑃detect(𝒟1) + (1 −𝑃detect(𝒟1)) ⋅𝑃detect(𝒟2)
(71)
Proof. Attack detected by first defense, or passes first and detected by second. Events are independent by
design.
■
Theorem 5.4 (Parallel Detection Rate). Combined detection rate:
𝑃(detect) = 1 −∏
𝑑∈𝒟
(1 −𝑃𝑑(detect))
(72)
44

## Page 45

Proof. Attack succeeds only if it evades all defenses.
■
Theorem 5.5 (False Positive Composition). For series composition:
FPR(𝒟1 ∘𝒟2) = FPR(𝒟1) + (1 −FPR(𝒟1)) ⋅FPR(𝒟2)
(73)
For parallel composition (conservative):
FPR(𝒟1 ∥𝒟2) ≤FPR(𝒟1) + FPR(𝒟2)
(74)
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
(75)
Table 19: Recommended defense stack with latency and detection rates.
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
Corollary 5.6 (Stack Detection Rate). Assuming independence, the full stack (Table 19) achieves:
𝑃detect = 1 −(1 −0.80)(1 −0.70)(1 −0.60)(1 −0.80) = 0.995
(76)
5.6
Cost-Benefit Analysis
Definition 5.14 (Defense Cost). Total cost of defense deployment:
𝐶total(𝒟) = 𝐶compute + 𝐶latency + 𝐶fp + 𝐶maint
(77)
Table 20: Cost model components.
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
(78)
45

## Page 46

Table 21: Cost-benefit analysis by defense mechanism.
Defense
Compute
Latency
FP Cost
Benefit
ROI
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
5.6.1
Optimal Defense Portfolio
Definition 5.16 (Portfolio Optimization).
max
𝒟⊆𝒟all
𝐵total(𝒟) −𝐶total(𝒟)
(79)
subject to: 𝐶compute(𝒟) ≤𝐵compute, max𝑑𝐿𝑑≤𝐿max, FPR(𝒟) ≤𝜖fp.
Table 22: Deployment recommendations by risk profile.
Risk Profile
Recommended Stack
Cost
Detection
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
Figure 11 illustrates the defense composition using series (∘) and parallel (∥) arrangements. Each defense
mechanism targets specific attack patterns: the Cognitive Firewall handles input-layer attacks (prompt
injection), the Belief Sandbox catches belief-layer attacks, Tripwire Monitors detect identity-layer exploits,
and Anomaly Detection identifies behavioral drift. Overlapping regions show attacks detected by multiple
mechanisms, demonstrating the defense-in-depth principle.
46

## Page 47

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
Figure 11: Defense Composition Architecture: Four-way Venn diagram showing overlapping detection capa-
bilities of CIF defense mechanisms (Cognitive Firewall, Belief Sandbox, Tripwire Monitor, Anomaly Detec-
tion). Attack types are positioned in regions indicating which defenses detect them. The center (Full CIF)
represents the ensemble detection zone where all mechanisms contribute.
47

## Page 48

6
Detection Methods: Anomaly Detection, ROC Analysis, and
Provenance Tracking
This section presents the formal foundations for cognitive attack detection. We define anomaly detection
metrics (Section 6.1), ROC curve framework (Section 6.2), multi-detector fusion theory (Section 6.3), on-
line vs. batch trade-offs (Section 6.4), false positive mitigation strategies (Section 6.5), provenance analysis
(Section 6.6), and real-time monitoring architecture (Section 6.7).
Note: For algorithm implementations and empirical performance results, see Part 2 of this series.
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
(80)
Table 23: Drift score components and detection targets.
Component
Weight
Detection Target
KL divergence
1.0
Gradual distribution shift
Max delta
𝜆
Sudden belief injection
Property 6.1 (Drift Detection Threshold). For normally distributed baseline drift, the threshold 𝜃=
𝜇baseline + 𝑘⋅𝜎baseline with 𝑘= 3 provides 99.7% confidence under the null hypothesis of no attack.
6.1.2
Behavioral Deviation
Definition 6.2 (Deviation Score). The behavioral deviation score aggregates normalized feature anomalies:
𝑆dev(𝑎𝑖, 𝑡) =
𝐾
∑
𝑘=1
𝑤𝑘⋅|𝑓𝑘(𝜎𝑡
𝑖) −𝜇𝑘|
𝜎𝑘
(81)
where 𝑓𝑘are feature extractors and (𝑤𝑘, 𝜇𝑘, 𝜎𝑘) are learned parameters.
6.1.3
Ensemble Detection
Definition 6.3 (Ensemble Detector). Combines multiple detector scores via learned fusion:
𝑃(attack ∣S) = 𝜎(∑
𝑑
𝑤𝑑⋅𝑆𝑑−𝑏)
(82)
where 𝜎is the sigmoid function and weights (𝑤𝑑, 𝑏) are learned from labeled examples.
6.2
ROC Curve Analysis
6.2.1
Receiver Operating Characteristic Framework
Definition 6.4 (ROC Curve). For detector 𝐷with threshold 𝜏:
ROC(𝐷) = {(FPR(𝜏), TPR(𝜏)) ∶𝜏∈[0, 1]}
(83)
where the rates are defined as:
TPR(𝜏) = 𝑃(𝐷(𝑥) > 𝜏∣𝑥∈𝒜attack)
(84)
FPR(𝜏) = 𝑃(𝐷(𝑥) > 𝜏∣𝑥∈𝒳benign)
(85)
48

## Page 49

Definition 6.5 (Area Under Curve).
AUC(𝐷) = ∫
1
0
TPR(FPR−1(𝑡)) 𝑑𝑡
(86)
Table 24: AUC interpretation scale.
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
(87)
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
(88)
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
(89)
Definition 6.8 (Decision-Level Fusion). Quorum voting on binary decisions:
𝐷fused(𝑥) = 𝟙[
𝑘
∑
𝑖=1
𝟙[𝐷𝑖(𝑥) > 𝜏𝑖] ≥𝑞]
(90)
Definition 6.9 (Learned Fusion). Neural network combining scores:
𝑆fused = MLP(𝑆1, … , 𝑆𝑘; 𝜃)
(91)
6.3.2
Diversity-Aware Fusion
Definition 6.10 (Detector Diversity).
Diversity(𝐷𝑖, 𝐷𝑗) = 1 −|errors(𝐷𝑖) ∩errors(𝐷𝑗)|
|errors(𝐷𝑖) ∪errors(𝐷𝑗)|
(92)
Theorem 6.1 (Diversity Benefit). For detectors with error rates 𝑒1, … , 𝑒𝑘and pairwise diversity 𝛿𝑖𝑗:
𝑒fusion ≤∏
𝑖
𝑒𝑖+ (1 −
̄𝛿) ⋅max
𝑖
𝑒𝑖
(93)
where
̄𝛿is the average pairwise diversity.
Proof. When detectors make independent errors (high diversity), the fusion error is the product of individual
errors. Error correlation reduces this benefit proportionally to (1 −
̄𝛿).
■
49

## Page 50

6.4
Online vs. Batch Detection
6.4.1
Comparison Framework
Table 25: Online vs. batch detection trade-offs.
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
(94)
state𝑡= 𝑔(state𝑡−1, 𝑚𝑡)
(95)
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
(96)
Batch Path ∶𝐻
analyze
−−−−→patterns
update
−−−−→filters
(97)
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
(98)
Theorem 6.2 (Cascade FPR Reduction). For a multi-stage cascade:
FPRcascade = FPR1 ⋅𝑃(confirm2 ∣FP1) ⋅𝑃(confirm3 ∣FP2)
(99)
6.5.2
Strategy 2: Temporal Smoothing
Definition 6.14 (Smoothed Detection). Apply exponential smoothing to scores:
̂𝑆𝑡= 𝛼⋅𝑆𝑡+ (1 −𝛼) ⋅
̂𝑆𝑡−1
(100)
Definition 6.15 (Burst Suppression). Require sustained anomaly over window 𝑤:
Alert if 1
𝑤
𝑡
∑
𝑖=𝑡−𝑤+1
𝟙[𝑆𝑖> 𝜏] > 𝑝sustained
(101)
50

## Page 51

6.5.3
Strategy 3: Contextual Whitelisting
Definition 6.16 (Context-Aware Whitelist).
Suppress(alert) ⟺context(alert) ∈𝒲known
(102)
6.5.4
Strategy 4: Cost-Sensitive Thresholding
Definition 6.17 (Cost-Sensitive Threshold). Optimize for total cost rather than accuracy:
𝜏∗= arg min
𝜏
[𝐶FP ⋅FPR(𝜏) + 𝐶FN ⋅FNR(𝜏)]
(103)
6.6
Provenance Analysis
6.6.1
Information Flow Tracking
Definition 6.18 (Taint Label). Each belief carries provenance tags:
taint(𝜙) = {(source, timestamp, confidence)}
(104)
Definition 6.19 (Taint Propagation).
taint(𝜙derived) =
⋃
𝜓∈premises(𝜙derived)
taint(𝜓)
(105)
Table 26: Taint categories with trust levels.
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
(106)
6.6.3
Provenance Graph Analysis
Definition 6.21 (Provenance Graph). Directed graph of belief dependencies:
𝐺= (𝑉, 𝐸) where 𝑉= ℬ𝑖, 𝐸= {(𝜓, 𝜙) ∶𝜓∈premises(𝜙)}
(107)
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
(108)
51

## Page 52

Table 27: Provenance graph attack indicators.
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
6.7.2
Response Escalation
Table 28: Response escalation levels.
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
6.7.3
Empirical Validation
The detection methods presented in this section have been empirically validated in Part 2 of this series. Key
results include:
ROC Analysis: Receiver Operating Characteristic curves demonstrate the tradeoff between True Positive
Rate and False Positive Rate for each detector type. The ensemble achieves AUC > 0.84, with individual
mechanisms ranging from 0.74 (Belief Sandbox) to 0.81 (Tripwire Monitor). See Part 2, §{4} for detailed
ROC curves and confidence intervals.
Detection Performance by Attack Type: Detection rates vary across the five adversary classes (Ω1–
Ω5). The Cognitive Firewall excels at Ω1 (external) attacks while Tripwires and Invariants provide stronger
coverage for Ω3 (compromised agent) and Ω4 (inter-agent) attacks.
See Part 2, §{5} for the complete
detection matrix.
False Positive Mitigation: The confirmation cascade, temporal smoothing, and contextual whitelisting
strategies reduce false positive rates by > 80% while maintaining > 90% true positive rates. See Part 2,
§{5.4} for quantitative analysis of each mitigation strategy.
52

## Page 53

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
(109)
Proof. We prove this theorem by analyzing the sequential defense mechanism and applying probability theory
for independent events.
Setup: Let 𝜙𝑎𝑑𝑣be an adversarial belief that the attacker attempts to inject into agent 𝑎𝑖’s verified belief
set ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑.
Defense Model: The CIF implements two sequential defenses:
1. Cognitive Firewall ℱ: Classifies incoming messages as ACCEPT, QUARANTINE, or REJECT with
detection rate 𝑟𝑓
2. Belief Sandbox: Verifies quarantined beliefs before promotion with verification rate 𝑟𝑠
Step 1: For 𝜙𝑎𝑑𝑣to enter ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑, it must first pass the firewall.
Let 𝐸𝑓= “Firewall fails to detect 𝜙𝑎𝑑𝑣”. By definition of detection rate:
𝑃(𝐸𝑓) = 1 −𝑟𝑓
(110)
Step 2: If 𝜙𝑎𝑑𝑣passes the firewall (event 𝐸𝑓), it enters ℬ𝑝𝑟𝑜𝑣𝑖𝑠𝑖𝑜𝑛𝑎𝑙. For injection to succeed, it must then
pass sandbox verification.
Let 𝐸𝑠= “Sandbox fails to detect 𝜙𝑎𝑑𝑣”. By definition of verification rate:
𝑃(𝐸𝑠) = 1 −𝑟𝑠
(111)
Step 3: The defenses are independent by design (defense-in-depth principle):
• Firewall uses syntactic/semantic analysis on message content
• Sandbox uses provenance verification, consistency checking, and corroboration
• These operate on orthogonal aspects of the belief
Therefore:
𝑃(𝐸𝑓∩𝐸𝑠) = 𝑃(𝐸𝑓) ⋅𝑃(𝐸𝑠|𝐸𝑓) = 𝑃(𝐸𝑓) ⋅𝑃(𝐸𝑠)
(112)
The conditional independence holds because sandbox verification is applied regardless of why the message
passed firewall, and sandbox criteria (provenance, consistency, corroboration) are independent of firewall
criteria (injection patterns, anomaly scores).
Step 4: The attack succeeds iff both defenses fail:
𝑃(𝒜𝐵𝐼succeeds) = 𝑃(𝐸𝑓∩𝐸𝑠) = (1 −𝑟𝑓) ⋅(1 −𝑟𝑠)
(113)
■
53

## Page 54

Corollary 7.2 (Empirical Security Bound). With 𝑟𝑓= 0.8 and 𝑟𝑠= 0.7:
𝑃(success) ≤(1 −0.8)(1 −0.7) = 0.2 ⋅0.3 = 0.06
(114)
Corollary 7.3 (Layered Defense Generalization). For 𝑛independent defense layers with rates 𝑟1, … , 𝑟𝑛:
𝑃(success) ≤
𝑛
∏
𝑖=1
(1 −𝑟𝑖)
(115)
7.1.2
Trust Boundedness
Theorem 7.4 (No Trust Amplification). For any path 𝑝= (𝑎0, 𝑎1, … , 𝑎𝑘) in the communication graph:
𝒯𝑝𝑎𝑡ℎ
𝑎0→𝑎𝑘≤
min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1
(116)
Proof. By trust delegation rule (Definition 4.7) and induction on path length.
Base case (𝑘= 1):
𝒯𝑎0→𝑎1 = 𝒯𝑎0→𝑎1
✓
(117)
Inductive step: Assume the theorem holds for paths of length 𝑘. For path length 𝑘+ 1:
𝒯𝑎0→𝑎𝑘+1 = min(𝒯𝑝𝑎𝑡ℎ
𝑎0→𝑎𝑘, 𝒯𝑎𝑘→𝑎𝑘+1) ⋅𝛿
(118)
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
(119)
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
(120)
Case 1: Rule B-DIRECT applies.
The update adds evidence for proposition 𝜙:
ℬ𝑡+1
𝑖
(𝜙) = BayesUpdate(ℬ𝑡
𝑖(𝜙), 𝑐⋅𝒯𝑖→𝑠)
(121)
54

## Page 55

If the update would create contradiction (i.e., both ℬ𝑡+1(𝜙) > 𝜏and ℬ𝑡+1(𝜓) > 𝜏for contradictory 𝜙, 𝜓),
the sandbox consistency check in Rule S-PROMOTE rejects promotion:
𝑉(𝜋) = 1 ∧Consistent(ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑∪{𝜙}) ∧|Corroborate(𝜙)| ≥𝜅
(122)
Therefore, only consistent updates reach ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑.
Case 2: Rule B-DELEGATED applies.
Same argument, with additional trust decay ensuring lower confidence for delegated evidence.
■
Lemma 7.7 (Trust Matrix Preservation). The trust matrix 𝒯remains well-formed after any valid update:
∀𝑖, 𝑗∶0 ≤𝒯𝑖→𝑗≤1
(123)
Proof. By Definition 4.6, trust is computed as:
𝒯𝑡
𝑖→𝑗= 𝛼⋅𝑇𝑏𝑎𝑠𝑒(𝑗) + 𝛽⋅𝑇𝑡
𝑟𝑒𝑝(𝑗) + 𝛾⋅𝑇𝑡
𝑐𝑡𝑥(𝑖, 𝑗)
(124)
where 𝛼+ 𝛽+ 𝛾= 1 and each component 𝑇∗∈[0, 1].
Therefore:
𝒯𝑡
𝑖→𝑗∈[min(𝑇𝑏𝑎𝑠𝑒, 𝑇𝑟𝑒𝑝, 𝑇𝑐𝑡𝑥), max(𝑇𝑏𝑎𝑠𝑒, 𝑇𝑟𝑒𝑝, 𝑇𝑐𝑡𝑥)] ⊆[0, 1]
(125)
For delegation (Definition 4.7):
𝒯𝑑𝑒𝑙
𝑖→𝑘= min(𝒯𝑖→𝑗, 𝒯𝑗→𝑘) ⋅𝛿𝑑
(126)
Since min(⋅) ≤1 and 𝛿∈(0, 1), we have 𝒯𝑑𝑒𝑙
𝑖→𝑘∈[0, 1].
■
Lemma 7.8 (Provenance Chain Integrity). Every belief in ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑has a valid, verifiable provenance chain.
Proof. By Rule S-PROMOTE (Section 4.4.8), promotion from ℬ𝑝𝑟𝑜𝑣𝑖𝑠𝑖𝑜𝑛𝑎𝑙to ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑requires:
𝑉(𝜋(𝜙)) = 1
(127)
where 𝑉is the provenance verification function.
By construction of the sandbox, beliefs can only enter ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑through:
1. Initial system beliefs (hardcoded with SYSTEM_VERIFIED provenance)
2. Promotion from provisional (verified by 𝑉)
In both cases, provenance is verified. By induction on the history of ℬ𝑣𝑒𝑟𝑖𝑓𝑖𝑒𝑑, all beliefs have valid provenance.
■
Lemma 7.9 (Permission Boundary Preservation). Effective permissions never exceed granted permissions:
∀𝑎𝑖, ∀action ∶𝒫𝑒𝑓𝑓𝑒𝑐𝑡𝑖𝑣𝑒(𝑎𝑖, action) ≤𝒫𝑟𝑜𝑙𝑒(𝑎𝑖, action)
(128)
Proof. By Table 9:
𝒫𝑒𝑓𝑓𝑒𝑐𝑡𝑖𝑣𝑒(𝑎𝑖) = 𝒫𝑟𝑜𝑙𝑒(𝑎𝑖) ∩𝒫𝑑𝑒𝑙𝑒𝑔𝑎𝑡𝑒𝑑(𝑎𝑖) ∩𝒫𝑐𝑜𝑛𝑡𝑒𝑥𝑡(𝑎𝑖)
(129)
Since intersection can only reduce permissions (𝐴∩𝐵∩𝐶
⊆𝐴), we have 𝒫𝑒𝑓𝑓𝑒𝑐𝑡𝑖𝑣𝑒(𝑎𝑖, action) ≤
𝒫𝑟𝑜𝑙𝑒(𝑎𝑖, action) for all actions.
■
Lemma 7.10 (Firewall Completeness). Every incoming message is classified by the firewall.
55

## Page 56

Proof. By Definition 5.2, the firewall is a total function:
ℱ∶ℳ→{ACCEPT, QUARANTINE, REJECT}
(130)
The decision rules cover all cases:
• If 𝐷𝑖𝑛𝑗(𝑚) > 𝜏1: REJECT
• Else if 𝐷𝑠𝑢𝑠(𝑚) > 𝜏2: QUARANTINE
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
(131)
Proof. By firewall design, false positive rate is bounded by 𝜖𝑓𝑝. Legitimate messages are rejected only on
false positive, establishing the bound.
■
7.3.2
Progress Guarantee
Theorem 7.12 (Byzantine Consensus Termination). With 𝑛≥3𝑓+ 1 agents and at most 𝑓Byzantine:
𝑃(consensus reached in 𝑂(𝑓+ 1) rounds) = 1
(132)
Proof. Standard Byzantine agreement result (Lamport et al., 1982). With honest majority 𝑛≥3𝑓+ 1, the
PBFT protocol guarantees termination in 𝑓+ 1 rounds.
■
7.4
Complexity Bounds
7.4.1
Space Complexity
Table 29: Per-component space complexity.
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
(133)
Proof. Per agent:
• Belief state: |Φ| propositions with confidence values = 𝑂(|Φ|)
• Provenance: Each belief has chain of depth at most 𝑑= 𝑂(|Φ| ⋅𝑑)
56

## Page 57

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
Table 30: Per-operation time complexity.
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
(134)
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
57

## Page 58

7.4.3
Latency Overhead
Theorem 7.16 (Bounded Latency Overhead). CIF adds latency:
𝐿𝐶𝐼𝐹= 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙+ 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥⋅𝑃(quarantine) + 𝐿𝑣𝑒𝑟𝑖𝑓𝑦⋅𝑃(verify)
(135)
Proof. Expected latency is sum of:
1. Firewall (always): 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙
2. Sandbox (conditional): 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥⋅𝑃(message quarantined)
3. Verification (conditional): 𝐿𝑣𝑒𝑟𝑖𝑓𝑦⋅𝑃(belief promoted)
With empirical measurements:
• 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙≈10ms
• 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥≈5ms, 𝑃(quarantine) ≈0.3
• 𝐿𝑣𝑒𝑟𝑖𝑓𝑦≈15ms, 𝑃(verify) ≈0.2
𝐿𝐶𝐼𝐹≈10 + 5 ⋅0.3 + 15 ⋅0.2 = 10 + 1.5 + 3 = 14.5ms
(136)
Compared to baseline ≈11.8ms: overhead factor ≈1.23 (23%).
■
7.5
Formal Model Checking
7.5.1
State Space Definition
Definition 7.1 (System State). The complete system state is the tuple:
𝑠= (𝜎1, … , 𝜎𝑛, 𝒮, 𝒯)
(137)
where 𝜎𝑖is agent 𝑖’s cognitive state, 𝒮is shared state, and 𝒯is the trust matrix.
7.5.2
Temporal Properties
We verify the following CTL (Computation Tree Logic) properties:
Property 7.1 (Safety: Consensus Integrity).
𝐴𝐺(¬compromised(ℬ𝑐𝑜𝑛𝑠𝑒𝑛𝑠𝑢𝑠))
(138)
“Always globally, consensus beliefs are not compromised.”
Property 7.2 (Liveness: Request-Response).
𝐴𝐺(request ⇒𝐴𝐹(response))
(139)
“Every request eventually gets a response.”
Property 7.3 (Fairness: Tripwire Checking).
𝐴𝐺(𝐴𝐹(tripwire_checked))
(140)
“Tripwires are checked infinitely often.”
58

## Page 59

Table 31: Model checking verification results.
Property
Verified
States Explored
Reference
Belief integrity
✓
106
Theorem 7.1
Trust bounded
✓
104
Theorem 7.4
No deadlock
✓
107
Theorem 7.11
Eventual detection
✓
105
Theorem 4.15
7.5.3
Model Checking Results
The following table summarizes the expected state space exploration for each property based on formal
analysis of the CIF specification. These values represent theoretical bounds derived from the state space
definition (Definition 7.1) and complexity analysis (Section 7.4). Actual model checking execution using
NuSMV, SPIN, and TLA+ tooling is presented in Part 2 of this series, along with full implementation
configurations.
Note: Model checking tool configurations (NuSMV, SPIN, TLA+) and verification parameters
are provided in Part 2: Computational Validation, which presents the executable implementations
and empirical verification results.
7.5.4
Verification Results Summary
The following table summarizes the expected verification outcomes for each tool-property combination based
on the formal specifications above.
These guarantees follow from the CTL/LTL property specifications
(Section 7.5.2) applied to the state space definition (Section 7.5.1). Empirical execution of these verification
configurations, including runtime measurements and counterexample analysis, is presented in Part 2.
Table 32: Verification results across tools.
Tool
Property
Guarantee
Reference
NuSMV
Belief Integrity
Proven
Theorem 7.1
NuSMV
Trust Bounded
Proven
Theorem 7.4
SPIN
No Deadlock
Verified
Theorem 7.11
SPIN
Eventual Detection
Verified
Theorem 4.15
TLA+
Type Invariant
Validated
Definition 4.3
TLA+
Consensus Integrity
Validated
Theorem 7.12
7.5.5
Counterexample Analysis
When verification fails, model checkers produce counterexamples. Analysis procedure:
1. Extract trace: Sequence of states leading to violation
2. Identify trigger: First state where invariant fails
3. Root cause: Determine which transition violated property
4. Fix: Strengthen preconditions or add defense mechanism
5. Re-verify: Confirm fix resolves violation
Example: Counterexample Trace
State 0: Initial (all beliefs verified, trust matrix valid)
State 1: Agent 2 receives message from Agent 3
State 2: Firewall accepts (below threshold)
59

## Page 60

State 3: Belief promoted without corroboration check
State 4: VIOLATION: Unverified belief in B_verified
Root Cause: Missing corroboration check in promotion rule.
Fix: Add predicate |Corroborate(𝜙)| ≥𝜅)𝑡𝑜𝑅𝑢𝑙𝑒𝑆−𝑃𝑅𝑂𝑀𝑂𝑇𝐸(𝑆𝑒𝑐𝑡𝑖𝑜𝑛4.4.8).
60

## Page 61

8
Discussion: Theoretical Implications, Limitations, and Future
Directions
This section examines the theoretical implications of the Cognitive Integrity Framework (Section 8.1), formal
limitations and boundary conditions (Section 8.2), relationship to prior work (Section 8.3), governance
implications (Section 8.4), and future research directions (Section 8.5).
8.1
Theoretical Implications
8.1.1
Why Composable Defenses Are Necessary
The defense composition algebra (Theorem 5.3, Theorem 5.4) formalizes a principle implicit in security
practice: layered defenses provide multiplicative rather than additive protection. Each defense mechanism
addresses a distinct attack surface:
Table 33: Defense mechanisms and their target attack surfaces.
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
The orthogonality of these surfaces explains why no single mechanism suﬀices: an attack that bypasses input
filtering may still violate behavioral invariants; an attack that evades pattern matching may still trigger
belief drift detection.
Empirical ablation studies in Part 2 (§{5.6}) validate this theoretical prediction: removing the Cognitive
Firewall causes the largest detection rate drop (−13%), followed by Tripwires (−9%) and Provenance Track-
ing (−7%). No individual mechanism provides comparable detection rates to the full ensemble—confirming
the multiplicative composition theorem (Theorem 5.3).
8.1.2
The Trust Boundedness Guarantee
The bounded trust theorem (Theorem 4.2) represents a structural guarantee against trust amplification
attacks.
Unlike detection-based defenses that may be evaded by novel attacks, the 𝛿𝑑decay bound is
algebraic: it holds for any attack type, any adversary capability, and any delegation chain length. This
makes it a formal rather than empirical security property.
The decay factor 𝛿∈[0, 1) creates a tradeoff:
• Lower 𝛿: Stronger security, limited delegation utility
• Higher 𝛿: More delegation flexibility, weaker bounds
Organizations must calibrate this tradeoff based on their threat model (Section 5.1 in Part 3).
8.1.3
Information-Theoretic Detection Limits
The stealth-impact fundamental limit (Theorem 4.14) establishes that certain attacks are provably unde-
tectable without unacceptable false positive rates. This is not a limitation of our specific mechanisms but
a fundamental bound analogous to Shannon’s channel capacity—some attacks simply cannot be detected
without additional information.
This has practical implications: security architectures should not promise detection of all possible attacks.
Instead, they should characterize the detection boundary and provide containment for attacks that cross it.
61

## Page 62

8.1.4
Architecture-Specific Vulnerability Patterns
The formal framework reveals why different multiagent architectures exhibit different vulnerability profiles:
Table 34: Theoretical vulnerability analysis by architecture type.
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
8.2
Formal Limitations
8.2.1
Assumption Dependencies
The formal guarantees of CIF depend on specific assumptions. Violation of these assumptions degrades or
eliminates security properties:
Table 35: Impact of assumption violations on formal guarantees.
Assumption
Guarantee Impacted
Honest orchestrator
Ω5
attacks
succeed;
systemic
compromise possible
𝑛≥3𝑓+ 1 agents
Byzantine consensus fails (Theo-
rem 5.2)
Authenticated channels
Ω4 coordination attacks expand
Known attack patterns
Zero-day evasion possible
8.2.2
Scalability Constraints
The formal framework imposes scaling limitations:
𝑀trust = 𝑂(𝑛2)
(141)
𝐿consensus = 𝑂(𝑛2)
(142)
The quadratic trust matrix (Equation (141)) limits practical deployment to systems with moderate agent
counts. Sparse trust representations or hierarchical trust structures may enable scaling to larger systems.
Consensus latency (Equation (142)) suggests that Byzantine consensus should be reserved for critical deci-
sions rather than applied universally.
8.2.3
Inherent Detection Gaps
Certain attack types are formally diﬀicult to detect:
• Semantic equivalence: Attacks preserving meaning while changing syntax evade pattern-based de-
tection
• Progressive drift: Sub-threshold changes that accumulate over time (Equation (13))
• Orchestrator compromise: Outside the Ω1–Ω4 threat model
These are not implementation failures but formal limitations of the detection paradigm.
62

## Page 63

8.3
Relationship to Prior Work
CIF builds on and extends several research traditions:
Byzantine Fault Tolerance: Classical BFT (PBFT, etc.) assumes crash or arbitrary faults. CIF extends
this to cognitive manipulation—agents that appear functional but hold corrupted beliefs.
Trust Management Systems: Prior systems (PolicyMaker, SPKI, etc.) focus on authorization decisions.
CIF addresses continuous trust evolution with provable decay bounds.
AI Safety and Alignment: Constitutional AI and similar approaches address single-agent alignment. CIF
extends these concepts to multi-agent coordination integrity.
Prompt Injection Defenses: Existing defenses focus on single-agent scenarios. CIF addresses the propa-
gation and amplification of attacks across agent networks.
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
8.4
Governance and Policy Implications
8.4.1
The Regulatory Gap
Current AI regulation lacks cognitive security provisions:
Table 36: Regulatory gaps for cognitive security.
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
63

## Page 64

8.4.2
Recommendations for Policy
We propose that regulators consider:
1. Cognitive Security Audits: Mandatory assessment of inter-agent trust mechanisms for high-risk
deployments
2. Transparency Requirements: Disclosure of trust hierarchies and delegation policies
3. Incident Reporting: New category for cognitive attacks
4. Certification Pathways: Industry certification for cognitive security practices
8.5
Future Theoretical Directions
8.5.1
Adaptive Defense Theory
The detection degradation problem suggests a need for adaptive defenses. Formal treatment as a game-
theoretic equilibrium:
𝜋∗∗defense = arg max ∗𝜋𝔼[∑
𝑡
𝛾𝑡𝑟(𝑠𝑡, 𝑎𝑡)]
(143)
requires solving the partial observability problem—defenders cannot directly observe attacker intent.
8.5.2
Cross-System Trust Federation
Extending trust calculus across organizational boundaries:
𝒯∗𝑖→𝑗cross = 𝑓(𝒯∗local, 𝒯∗reputation, 𝒯∗attestation)
(144)
The primary challenge is trust calibration—mapping heterogeneous trust semantics across systems with
different threat models.
8.5.3
Emergent Behavior Security
As multiagent systems scale, emergent collective behaviors become security-relevant. Open questions include:
• Formal characterization of beneficial vs. malicious emergence
• Detection of emergent coordination patterns indicating compromise
• Sandboxing that preserves beneficial emergence while constraining malicious emergence
The colony cognitive security perspective developed in Section 11 provides initial formal foundations for
these questions.
8.5.4
Long-Horizon Agent Security
Agents operating over extended time horizons (days, weeks, months) face additional challenges:
• Memory integrity: Verification of accumulated knowledge
• Goal stability: Distinguishing legitimate evolution from adversarial drift
• Temporal consistency: Decisions consistent with historical context
The trust calculus extends naturally to temporal trust: 𝒯𝑡= 𝒯𝑡−1 ⋅𝛿time where 𝛿time encodes trust decay
over time.
64

## Page 65

8.5.5
The Cognitive Security Research Agenda
We propose a research agenda organized by time horizon:
Near-term (1–2 years):
• Standardized formal verification benchmarks
• Integration of CIF mechanisms into production frameworks
• Theoretical analysis of real-world attack patterns
Medium-term (2–5 years):
• Game-theoretic foundations for adaptive defenses
• Cross-organizational trust federation protocols
• Hardware-backed cognitive security guarantees
Long-term (5+ years):
• Formal verification of emergent agent behavior
• Self-healing cognitive security systems
• Integration with broader AI safety theory
The formal foundations established in this work—bounded trust, composable defenses, information-theoretic
limits—provide a stable basis for this evolving research program.
65

## Page 66

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
Table 37: Summary of formal contributions.
Contribution
Significance
Trust Calculus
Bounded delegation with 𝑂(𝛿𝑑) decay guarantee pre-
vents trust laundering and amplification—a struc-
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
2. Trust must be bounded: Without 𝛿𝑑decay, delegation chains enable trust laundering where adver-
sarial content acquires trusted-source status through intermediaries. This is a structural vulnerability
requiring structural mitigation.
3. Defenses compose predictably: The defense composition algebra enables formal reasoning about
layered security. Orthogonal defenses compose multiplicatively, explaining why full CIF substantially
outperforms any single mechanism.
4. Information-theoretic limits constrain adversaries: The stealth-impact tradeoff theorem estab-
lishes that high-impact attacks cannot remain completely undetectable.
This provides theoretical
grounding for defense strategies.
66

## Page 67

5. Cognitive security requires continuous verification: Unlike perimeter security that trusts in-
ternals after boundary checks, cognitive security requires continuous verification of beliefs, goals, and
trust relationships.
9.2
Actionable Recommendations
9.2.1
For Practitioners
Immediate priorities:
1. Implement trust decay in all delegation chains (𝛿≤0.9)
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
• Q2: Tight detection bounds. Can the stealth-impact bounds in Theorem 6.2 be tightened? What
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
67

## Page 68

• Q9: Adversarial benchmark construction. How should we construct attack corpora that remain
challenging despite model improvements? Can we formalize attack diversity and coverage metrics?
• Q10: Colony CogSec evaluation. What benchmarks capture stigmergic attack surfaces—shared
state manipulation, environmental signaling, emergent coordination failures? (Section 11)
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
inflation of prediction errors? (Section 11)
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
68

## Page 69

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
Part 2 of this series provides empirical validation demonstrating that these formal mechanisms translate
to practical protection across diverse production architectures. Part 3 offers actionable deployment guid-
ance for practitioners and AI agents. Together, the three papers provide a comprehensive framework for
understanding, implementing, and operating cognitive security in multiagent AI systems.
The formal gaps identified in this work—semantic equivalence attacks, progressive drift, orchestrator
compromise—define the frontier for future research, while the provable guarantees (bounded trust, compos-
able defenses, information-theoretic limits) provide the stable theoretical foundation on which that research
can build.
As autonomous AI agents increasingly operate in high-stakes contexts—executing code, mod-
ifying infrastructure, controlling resources, and making decisions with lasting consequences—
69

## Page 70

the formal foundations established here become not merely useful but essential infrastructure
for secure deployment.
Cognitive security is not optional for the multiagent future. It is foundational.
70

## Page 71

10
Supplementary: Mathematical Proofs
This supplementary material provides complete formal proofs for all theorems stated in the main text,
including preliminary definitions (Section 10.1), main theorem proofs (Sections 10.2 to 10.8), and additional
supporting lemmas (Section 10.9).
10.1
Preliminary Definitions and Notation
10.1.1
Notation Summary
Table 38: Mathematical notation used throughout proofs.
Symbol
Meaning
𝒜= {𝑎1, … , 𝑎𝑛}
Set of 𝑛agents
ℬ𝑖∶Φ →[0, 1]
Agent 𝑖’s belief function
𝒢𝑖
Agent 𝑖’s goal set
𝒯𝑖→𝑗
Trust from agent 𝑖to agent 𝑗
𝛿∈(0, 1)
Trust decay factor per delegation hop
𝜏
Generic threshold parameter
𝜙, 𝜓
Propositions
𝜋(𝜙)
Provenance chain for belief 𝜙
Definition 10.1 (Trust Path). A trust path from agent 𝑎0 to agent 𝑎𝑘is an ordered sequence 𝑝=
(𝑎0, 𝑎1, … , 𝑎𝑘) where each consecutive pair (𝑎𝑖, 𝑎𝑖+1) represents a direct trust relationship with 𝒯𝑎𝑖→𝑎𝑖+1 > 0.
Definition 10.2 (Path Trust). The trust along path 𝑝= (𝑎0, … , 𝑎𝑘) is defined as:
𝒯𝑝𝑎𝑡ℎ
𝑝
=
min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1 ⋅𝛿𝑘
(145)
Definition 10.3 (Delegation Chain). A delegation chain of depth 𝑑is a sequence of agents (𝑎0, 𝑎1, … , 𝑎𝑑)
where agent 𝑎𝑖delegates authority to 𝑎𝑖+1.
10.2
Theorem 3.1: Trust Boundedness
Theorem 10.1 (Trust Boundedness — Restated). For any delegation chain of depth 𝑑:
𝒯𝑑𝑒𝑙
𝑖→𝑘≤𝛿𝑑
(146)
Lemma 10.2 (Trust Non-Amplification on Single Hop). For any agents 𝑎, 𝑏and any delegation to 𝑐:
𝒯𝑑𝑒𝑙
𝑎→𝑐≤𝒯𝑎→𝑏
(147)
Proof of Theorem 10.2. By the trust delegation rule (Definition 4.7):
𝒯𝑑𝑒𝑙
𝑎→𝑐= min(𝒯𝑎→𝑏, 𝒯𝑏→𝑐) ⋅𝛿
(148)
Since min(𝒯𝑎→𝑏, 𝒯𝑏→𝑐) ≤𝒯𝑎→𝑏and 𝛿< 1:
𝒯𝑑𝑒𝑙
𝑎→𝑐= min(𝒯𝑎→𝑏, 𝒯𝑏→𝑐) ⋅𝛿≤𝒯𝑎→𝑏⋅𝛿< 𝒯𝑎→𝑏
(149)
■
71

## Page 72

Lemma 10.3 (Trust Decay Bound). For any single-hop delegation:
𝒯𝑑𝑒𝑙≤𝛿
(150)
Proof of Theorem 10.3. By definition, all direct trust values satisfy 𝒯𝑎→𝑏≤1. Therefore:
𝒯𝑑𝑒𝑙
𝑎→𝑐= min(𝒯𝑎→𝑏, 𝒯𝑏→𝑐) ⋅𝛿≤1 ⋅𝛿= 𝛿
(151)
■
Main Proof of Theorem 10.1. By strong induction on 𝑑.
Base Case (𝑑= 0): When 𝑑= 0, there is no delegation (direct trust). By definition:
𝒯𝑑𝑒𝑙
𝑖→𝑘= 𝒯𝑖→𝑘≤1 = 𝛿0
(152)
The base case holds.
Inductive Hypothesis: Assume for all delegation chains of depth ≤𝑑:
𝒯𝑑𝑒𝑙≤𝛿𝑑
(153)
Inductive Step (depth 𝑑+ 1): Consider a delegation chain (𝑎0, 𝑎1, … , 𝑎𝑑+1) of depth 𝑑+ 1.
Let 𝒯(𝑑) denote the delegated trust from 𝑎0 to 𝑎𝑑(depth 𝑑).
By the trust delegation rule:
𝒯𝑑𝑒𝑙
𝑎0→𝑎𝑑+1 = min(𝒯(𝑑), 𝒯𝑎𝑑→𝑎𝑑+1) ⋅𝛿
(154)
By the inductive hypothesis: 𝒯(𝑑) ≤𝛿𝑑
Since 𝒯𝑎𝑑→𝑎𝑑+1 ≤1:
min(𝒯(𝑑), 𝒯𝑎𝑑→𝑎𝑑+1) ≤𝒯(𝑑) ≤𝛿𝑑
(155)
Therefore:
𝒯𝑑𝑒𝑙
𝑎0→𝑎𝑑+1 ≤𝛿𝑑⋅𝛿= 𝛿𝑑+1
(156)
By the principle of mathematical induction, the theorem holds for all 𝑑≥0.
■
Corollary 10.4 (Trust Vanishing). For any 𝜖> 0, there exists 𝐷such that for all delegation chains of depth
𝑑> 𝐷:
𝒯𝑑𝑒𝑙< 𝜖
(157)
Proof. Choose 𝐷= ⌈log𝛿𝜖⌉. Since 𝛿∈(0, 1), log𝛿is decreasing. For 𝑑> 𝐷: 𝒯𝑑𝑒𝑙≤𝛿𝑑< 𝛿𝐷≤𝜖.
■
Corollary 10.5 (Practical Depth Limit). With 𝛿= 0.8 and minimum actionable trust 𝜏𝑚𝑖𝑛= 0.1:
𝑑𝑚𝑎𝑥= ⌊log0.8 0.1⌋= 10
(158)
72

## Page 73

10.3
Theorem 6.1: Belief Injection Resistance
Theorem 10.6 (Belief Injection Resistance — Restated). Under CIF with firewall detection rate 𝑟𝑓and
sandboxing verification rate 𝑟𝑠:
𝑃(𝒜𝐵𝐼succeeds) ≤(1 −𝑟𝑓) ⋅(1 −𝑟𝑠)
(159)
Lemma 10.7 (Defense Independence). The firewall and sandbox operate on independent decision criteria:
• Firewall: Pattern matching and anomaly scoring on message content
• Sandbox: Provenance verification, consistency checking, and corroboration
These mechanisms share no common features or state.
Proof of Theorem 10.7. By construction of the CIF architecture:
1. Firewall operates at input layer with feature set 𝐹𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙= {𝑝𝑎𝑡𝑡𝑒𝑟𝑛𝑠, 𝑒𝑚𝑏𝑒𝑑𝑑𝑖𝑛𝑔𝑠, 𝑎𝑛𝑜𝑚𝑎𝑙𝑦_𝑠𝑐𝑜𝑟𝑒𝑠}
2. Sandbox operates at belief layer with feature set 𝐹𝑠𝑎𝑛𝑑𝑏𝑜𝑥= {𝑝𝑟𝑜𝑣𝑒𝑛𝑎𝑛𝑐𝑒, 𝑐𝑜𝑛𝑠𝑖𝑠𝑡𝑒𝑛𝑐𝑦, 𝑐𝑜𝑟𝑟𝑜𝑏𝑜𝑟𝑎𝑡𝑖𝑜𝑛}
3. 𝐹𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙∩𝐹𝑠𝑎𝑛𝑑𝑏𝑜𝑥= ∅
Therefore, 𝑃(firewall detects|sandbox outcome) = 𝑃(firewall detects). The mechanisms are probabilistically
independent.
■
Definition 10.4 (Attack Success). A belief injection attack 𝒜𝐵𝐼succeeds if and only if:
1. The adversarial message 𝑚𝑎𝑑𝑣is not rejected by the firewall, AND
2. The injected belief 𝜙𝑎𝑑𝑣is promoted from sandbox to verified beliefs
Main Proof of Theorem 10.6. Let 𝐸𝑓= event “firewall accepts message” (does not detect attack). Let 𝐸𝑠
= event “sandbox fails to filter belief” (does not detect attack).
For 𝒜𝐵𝐼to succeed, both 𝐸𝑓and 𝐸𝑠must occur:
𝑃(𝒜𝐵𝐼succeeds) = 𝑃(𝐸𝑓∩𝐸𝑠)
(160)
By Theorem 10.7 (independence):
𝑃(𝐸𝑓∩𝐸𝑠) = 𝑃(𝐸𝑓) ⋅𝑃(𝐸𝑠)
(161)
By definition of detection rates:
• 𝑃(𝐸𝑓) = 1 −𝑟𝑓(probability firewall misses attack)
• 𝑃(𝐸𝑠) = 1 −𝑟𝑠(probability sandbox misses attack)
Therefore:
𝑃(𝒜𝐵𝐼succeeds) = (1 −𝑟𝑓) ⋅(1 −𝑟𝑠)
(162)
■
Corollary 10.8 (Numerical Bound). With empirical values 𝑟𝑓= 0.8 and 𝑟𝑠= 0.7:
𝑃(𝒜𝐵𝐼succeeds) ≤(1 −0.8) ⋅(1 −0.7) = 0.2 ⋅0.3 = 0.06
(163)
Corollary 10.9 (Defense Stacking). For 𝑛independent defenses with detection rates 𝑟1, … , 𝑟𝑛:
𝑃(attack succeeds) =
𝑛
∏
𝑖=1
(1 −𝑟𝑖)
(164)
Proof. Direct extension of Theorem 10.6 by independence.
■
73

## Page 74

10.4
Theorem 6.2: No Trust Amplification
Theorem 10.10 (No Trust Amplification — Restated). For any path 𝑝= (𝑎0, 𝑎1, … , 𝑎𝑘) in the communi-
cation graph:
𝒯𝑝𝑎𝑡ℎ
𝑎0→𝑎𝑘≤
min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1
(165)
Lemma 10.11 (Minimum Preservation under Min). For any sequence (𝑥1, … , 𝑥𝑛) and additional element
𝑥𝑛+1:
min(𝑥1, … , 𝑥𝑛+1) = min(min(𝑥1, … , 𝑥𝑛), 𝑥𝑛+1)
(166)
Proof. Standard property of the minimum function.
■
Lemma 10.12 (Decay Factor Strengthens Bound). For 𝑥≤𝑦and 𝛿∈(0, 1):
𝑥⋅𝛿≤𝑦
(167)
Proof. Since 𝛿< 1, 𝑥⋅𝛿< 𝑥≤𝑦.
■
Main Proof of Theorem 10.10. By strong induction on path length 𝑘.
Base Case (𝑘= 1): For path 𝑝= (𝑎0, 𝑎1):
𝒯𝑝𝑎𝑡ℎ
𝑎0→𝑎1 = 𝒯𝑎0→𝑎1 = min
𝑖∈[0,0] 𝒯𝑎𝑖→𝑎𝑖+1
(168)
The base case holds trivially.
Inductive Hypothesis: Assume for all paths of length ≤𝑘:
𝒯𝑝𝑎𝑡ℎ≤
min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1
(169)
Inductive Step (path length 𝑘+ 1): Consider path 𝑝= (𝑎0, 𝑎1, … , 𝑎𝑘+1).
Let 𝑝′ = (𝑎0, 𝑎1, … , 𝑎𝑘) be the prefix path.
By the trust delegation rule:
𝒯𝑝𝑎𝑡ℎ
𝑎0→𝑎𝑘+1 = min(𝒯𝑝𝑎𝑡ℎ′
𝑎0→𝑎𝑘, 𝒯𝑎𝑘→𝑎𝑘+1) ⋅𝛿
(170)
By the inductive hypothesis:
𝒯𝑝𝑎𝑡ℎ′
𝑎0→𝑎𝑘≤
min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1
(171)
Applying the minimum:
min(𝒯𝑝𝑎𝑡ℎ′
𝑎0→𝑎𝑘, 𝒯𝑎𝑘→𝑎𝑘+1) ≤min ( min
𝑖∈[0,𝑘−1] 𝒯𝑎𝑖→𝑎𝑖+1, 𝒯𝑎𝑘→𝑎𝑘+1)
(172)
By Theorem 10.11:
= min
𝑖∈[0,𝑘] 𝒯𝑎𝑖→𝑎𝑖+1
(173)
Since 𝛿∈(0, 1):
𝒯𝑝𝑎𝑡ℎ
𝑎0→𝑎𝑘+1 = min(⋅) ⋅𝛿≤min
𝑖∈[0,𝑘] 𝒯𝑎𝑖→𝑎𝑖+1
(174)
■
74

## Page 75

Corollary 10.13 (Weakest Link Principle). Trust through any path is bounded by the least trusted edge:
𝒯𝑝𝑎𝑡ℎ≤
min
𝑒𝑑𝑔𝑒∈𝑝𝑎𝑡ℎ𝒯𝑒𝑑𝑔𝑒
(175)
Corollary 10.14 (No Collusion Benefit). Multiple colluding agents cannot create trust exceeding any indi-
vidual’s trust with the target.
10.5
Theorem 6.3: Goal Alignment Invariant
Theorem 10.15 (Goal Alignment Invariant — Restated). If the system starts with aligned goals and all
goal updates follow the delegation protocol:
Aligned(𝒢0
𝑖) ∧∀𝑡∶ValidUpdate(𝒢𝑡
𝑖, 𝒢𝑡+1
𝑖
) ⇒∀𝑡∶Aligned(𝒢𝑡
𝑖)
(176)
Definition 10.5 (Goal Alignment). Goals 𝒢𝑖are aligned if:
Aligned(𝒢𝑖) ⟺𝒢𝑖⊆𝒢𝑝𝑟𝑖𝑛𝑐𝑖𝑝𝑎𝑙∪Delegate(𝒢𝑝𝑟𝑖𝑛𝑐𝑖𝑝𝑎𝑙)
(177)
Definition 10.6 (Valid Goal Update). An update from 𝒢𝑡to 𝒢𝑡+1 is valid if:
ValidUpdate(𝒢𝑡, 𝒢𝑡+1) ⟺∀𝑔∈(𝒢𝑡+1 ∖𝒢𝑡) ∶Authorized(𝑔)
(178)
where Authorized(𝑔) means 𝑔derives from principal or valid delegation.
Lemma 10.16 (Delegation Preserves Alignment). If 𝑔∈Delegate(𝒢𝑝𝑟𝑖𝑛𝑐𝑖𝑝𝑎𝑙), then 𝑔is aligned.
Proof. Direct from Definition 10.5.
■
Lemma 10.17 (Set Union Preserves Subset). If 𝐴⊆𝐶and 𝐵⊆𝐶, then 𝐴∪𝐵⊆𝐶.
Proof. Standard set theory.
■
Main Proof of Theorem 10.15. By induction on time 𝑡.
Base Case (𝑡= 0): Given: Aligned(𝒢0
𝑖). The base case holds by hypothesis.
Inductive Hypothesis: Assume Aligned(𝒢𝑡
𝑖) for some 𝑡≥0.
Inductive Step: We must show Aligned(𝒢𝑡+1
𝑖
).
The goal set at 𝑡+ 1 is:
𝒢𝑡+1
𝑖
= (𝒢𝑡
𝑖∖Removed) ∪Added
(179)
For goals in 𝒢𝑡
𝑖∖Removed:
• By inductive hypothesis, these are aligned
• Removal cannot introduce misalignment
For goals in Added:
• By ValidUpdate, all added goals satisfy Authorized(𝑔)
• By Theorem 10.16, authorized goals are aligned
By Theorem 10.17:
𝒢𝑡+1
𝑖
⊆𝒢𝑝𝑟𝑖𝑛𝑐𝑖𝑝𝑎𝑙∪Delegate(𝒢𝑝𝑟𝑖𝑛𝑐𝑖𝑝𝑎𝑙)
(180)
Therefore Aligned(𝒢𝑡+1
𝑖
).
■
75

## Page 76

Corollary 10.18 (Safety Under Protocol). An agent following CIF protocols cannot have its goals hijacked
to adversarial objectives.
Corollary 10.19 (Necessary Condition for Hijacking). Goal hijacking requires violating the delegation pro-
tocol:
¬Aligned(𝒢𝑡
𝑖) ⇒∃𝑡′ < 𝑡∶¬ValidUpdate(𝒢𝑡′
𝑖, 𝒢𝑡′+1
𝑖
)
(181)
10.6
Theorem 6.4: Firewall Liveness
Theorem 10.20 (Firewall Liveness — Restated). CIF firewall preserves liveness for legitimate inputs:
∀𝑚∈ℳ𝑙𝑒𝑔𝑖𝑡𝑖𝑚𝑎𝑡𝑒∶𝑃(ℱ(𝑚) = ACCEPT) ≥1 −𝜖𝑓𝑝
(182)
Definition 10.7 (Legitimate Message). A message 𝑚is legitimate if:
1. It originates from an authorized source
2. It contains no adversarial content
3. It conforms to expected communication patterns
Definition 10.8 (False Positive Rate). The false positive rate 𝜖𝑓𝑝is:
𝜖𝑓𝑝= 𝑃(ℱ(𝑚) ≠ACCEPT|𝑚∈ℳ𝑙𝑒𝑔𝑖𝑡𝑖𝑚𝑎𝑡𝑒)
(183)
Lemma 10.21 (Firewall Classification). For any message 𝑚, the firewall produces exactly one of three
outcomes:
ℱ(𝑚) ∈{ACCEPT, QUARANTINE, REJECT}
(184)
Proof. By construction of the firewall decision function (Definition 5.2).
■
Main Proof of Theorem 10.20. Let 𝑚∈ℳ𝑙𝑒𝑔𝑖𝑡𝑖𝑚𝑎𝑡𝑒be an arbitrary legitimate message.
By the law of total probability:
𝑃(ℱ(𝑚) = ACCEPT) + 𝑃(ℱ(𝑚) = QUARANTINE) + 𝑃(ℱ(𝑚) = REJECT) = 1
(185)
By Definition 10.8:
𝑃(ℱ(𝑚) ≠ACCEPT) = 𝜖𝑓𝑝
(186)
Therefore:
𝑃(ℱ(𝑚) = ACCEPT) = 1 −𝑃(ℱ(𝑚) ≠ACCEPT) = 1 −𝜖𝑓𝑝
(187)
Since 𝑚was arbitrary:
∀𝑚∈ℳ𝑙𝑒𝑔𝑖𝑡𝑖𝑚𝑎𝑡𝑒∶𝑃(ℱ(𝑚) = ACCEPT) ≥1 −𝜖𝑓𝑝
(188)
■
Corollary 10.22 (Availability Bound). With 𝜖𝑓𝑝= 0.06, at least 94% of legitimate messages are accepted.
Corollary 10.23 (Quarantine Recovery). Messages in QUARANTINE can still reach verified belief state
through sandbox promotion, further improving effective availability.
76

## Page 77

10.7
Theorem 6.5: Byzantine Consensus Termination
Theorem 10.24 (Byzantine Consensus Termination — Restated). With 𝑛≥3𝑓+ 1 agents and at most 𝑓
Byzantine:
𝑃(consensus reached in 𝑂(𝑓+ 1) rounds) = 1
(189)
Lemma 10.25 (Byzantine Agreement Bound). Byzantine agreement requires 𝑛≥3𝑓+ 1 to tolerate 𝑓
Byzantine agents.
Proof. Classical result from distributed systems (Lamport, Shostak, Pease 1982). With fewer agents, Byzan-
tine agents can equivocate and prevent agreement.
■
Lemma 10.26 (Honest Majority). With 𝑛≥3𝑓+ 1:
𝑛−𝑓≥2𝑓+ 1 > 2𝑛
3
(190)
Proof. 𝑛−𝑓≥(3𝑓+ 1) −𝑓= 2𝑓+ 1
2𝑛
3 ≤2(3𝑓+1)
3
= 2𝑓+ 2
3 < 2𝑓+ 1
Therefore 𝑛−𝑓> 2𝑛
3 .
■
Lemma 10.27 (Round Progression). In each round, at least one of the following occurs:
1. Consensus is reached, or
2. At least one Byzantine agent is detected and excluded
Proof. By the protocol structure:
• If honest agents agree, their majority (> 2𝑛/3) ensures consensus
• If no consensus, some agent must have equivocated
• Equivocation is detectable through signature verification
■
Main Proof of Theorem 10.24. Termination: By Theorem 10.27, each round without consensus excludes
at least one Byzantine agent.
With at most 𝑓Byzantine agents, at most 𝑓rounds can occur without consensus.
After 𝑓exclusions, all remaining agents are honest.
By Theorem 10.26, honest agents form a > 2/3 majority and reach consensus in one additional round.
Total rounds: at most 𝑓+ 1 = 𝑂(𝑓+ 1).
Probability: The protocol is deterministic given message delivery. With reliable (eventually synchronous)
channels, all messages are delivered.
Therefore, termination is guaranteed with probability 1.
■
Corollary 10.28 (Concrete Round Bound). With 𝑓= 2 Byzantine agents: consensus in at most 3 rounds.
Corollary 10.29 (Safety). All honest agents decide on the same value (agreement property).
Proof. By honest majority and the 2/3 threshold requirement.
■
77

## Page 78

10.8
Theorem 6.6: Bounded Overhead
Theorem 10.30 (Bounded Overhead — Restated). CIF adds latency:
𝐿𝐶𝐼𝐹= 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙+ 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥⋅𝑃(quarantine) + 𝐿𝑣𝑒𝑟𝑖𝑓𝑦⋅𝑃(verify)
(191)
Definition 10.9 (Message Processing Path). A message 𝑚follows one of three paths:
1. Accept path: Firewall check only
2. Quarantine path: Firewall + sandbox processing
3. Reject path: Firewall check only (early termination)
Lemma 10.31 (Expected Value Decomposition). For mutually exclusive events 𝐸1, 𝐸2, 𝐸3 with ∑𝑃(𝐸𝑖) =
1:
𝐸[𝐿] = ∑
𝑖
𝑃(𝐸𝑖) ⋅𝐿𝑖
(192)
Proof. Law of total expectation.
■
Main Proof of Theorem 10.30. Let:
• 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙= firewall processing latency
• 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥= sandbox processing latency
• 𝐿𝑣𝑒𝑟𝑖𝑓𝑦= provenance verification latency
• 𝑃𝑞= 𝑃(quarantine) = probability of quarantine
• 𝑃𝑣= 𝑃(verify) = probability verification is triggered
The total CIF latency is:
𝐿𝐶𝐼𝐹= 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙+ 𝟙[quarantine] ⋅𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥+ 𝟙[verify] ⋅𝐿𝑣𝑒𝑟𝑖𝑓𝑦
(193)
Taking expectations:
𝐸[𝐿𝐶𝐼𝐹] = 𝐸[𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙] + 𝐸[𝟙[quarantine]] ⋅𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥+ 𝐸[𝟙[verify]] ⋅𝐿𝑣𝑒𝑟𝑖𝑓𝑦
(194)
= 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙+ 𝑃𝑞⋅𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥+ 𝑃𝑣⋅𝐿𝑣𝑒𝑟𝑖𝑓𝑦
■
10.8.1
Numerical Instantiation
With empirical measurements:
• 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙= 8ms
• 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥= 15ms
• 𝐿𝑣𝑒𝑟𝑖𝑓𝑦= 12ms
• 𝑃𝑞= 0.3
• 𝑃𝑣= 0.2
𝐸[𝐿𝐶𝐼𝐹] = 8 + 0.3 × 15 + 0.2 × 12 = 8 + 4.5 + 2.4 = 14.9ms
(195)
With baseline 𝐿𝑏𝑎𝑠𝑒𝑙𝑖𝑛𝑒= 12ms:
Overhead = 14.9 −12
12
× 100% = 24.2%
(196)
78

## Page 79

This matches the empirical observation of approximately 23% overhead.
Corollary 10.32 (Overhead Bound). The maximum overhead occurs when all messages are quarantined
and verified:
𝐿𝑚𝑎𝑥
𝐶𝐼𝐹= 𝐿𝑓𝑖𝑟𝑒𝑤𝑎𝑙𝑙+ 𝐿𝑠𝑎𝑛𝑑𝑏𝑜𝑥+ 𝐿𝑣𝑒𝑟𝑖𝑓𝑦
(197)
Corollary 10.33 (Optimization Target). To minimize overhead, prioritize reducing 𝑃𝑞(quarantine rate)
through improved firewall precision.
10.9
Additional Lemmas
Lemma 10.34 (Provenance Chain Integrity). If provenance verification function 𝑉is a cryptographic hash
chain, then:
𝑉(𝜋(𝜙)) = 1 ⇒𝜋(𝜙) has not been tampered with
(198)
Proof. By properties of cryptographic hash functions:
1. Collision resistance: Cannot find 𝜋′ ≠𝜋with 𝐻(𝜋′) = 𝐻(𝜋)
2. Preimage resistance: Cannot construct valid 𝜋without knowledge of chain
Therefore, 𝑉(𝜋(𝜙)) = 1 implies 𝜋(𝜙) is the original, untampered chain.
■
Lemma 10.35 (Belief Consistency Decidability). For finite proposition set Φ and belief function ℬ∶Φ →
[0, 1]: Checking Consistent(ℬ) is decidable in 𝑂(|Φ|2).
Proof. For each pair (𝜙, 𝜓) ∈Φ × Φ:
1. Check if 𝜙∧𝜓⊢⊥(logical contradiction)
2. Check if both ℬ(𝜙) > 𝜏and ℬ(𝜓) > 𝜏
There are 𝑂(|Φ|2) pairs. Each check is 𝑂(1) with precomputed contradiction table.
Total: 𝑂(|Φ|2).
■
Lemma 10.36 (Trust Matrix Convergence). Under stable interaction patterns, the reputation component
𝑇𝑟𝑒𝑝converges:
lim
𝑡→∞𝑇𝑡
𝑟𝑒𝑝= 𝑇∗
𝑟𝑒𝑝
(199)
where 𝑇∗
𝑟𝑒𝑝reflects the agent’s true reliability.
Proof. The reputation update rule is:
𝑇𝑡+1
𝑟𝑒𝑝= 𝑇𝑡
𝑟𝑒𝑝+ 𝜂⋅(outcome𝑡−𝑇𝑡
𝑟𝑒𝑝)
(200)
This is an exponential moving average with learning rate 𝜂.
For i.i.d. outcomes with mean 𝜇:
𝐸[𝑇𝑡
𝑟𝑒𝑝] →𝜇as 𝑡→∞
(201)
By the strong law of large numbers, 𝑇𝑡
𝑟𝑒𝑝→𝜇almost surely.
■
10.10
Summary of Proof Techniques
All proofs are constructive and provide explicit bounds useful for system implementation and analysis.
79

## Page 80

Table 39: Summary of proof techniques by theorem.
Theorem
Primary Technique
Complexity
3.1 (Trust Boundedness)
Strong induction
𝑂(𝑑)
6.1 (Belief Injection Resistance)
Probability independence
𝑂(1)
6.2 (No Trust Amplification)
Strong induction
𝑂(𝑘)
6.3 (Goal Alignment Invariant)
Induction on time
𝑂(𝑡)
6.4 (Firewall Liveness)
Complement probability
𝑂(1)
6.5 (Byzantine Consensus)
Classical BFT
𝑂(𝑓)
6.6 (Bounded Overhead)
Expected value
𝑂(1)
11
Supplementary: Eusocial Insect Intelligence and Colony Cog-
nitive Security
11.1
Overview
This supplementary material introduces colony cognitive security as a complementary paradigm to single-
agent AI safety and alignment. While the main CIF framework (Section 4) addresses cognitive integrity at the
individual agent level, eusocial insect colonies—ants, bees, termites—demonstrate that security properties
can emerge from collective dynamics that are irreducible to individual behavior. This section formalizes
these collective phenomena, identifies the benchmark gap for multiagent cognitive security, and proposes
evaluation scenarios grounded in biological precedent.
11.1.1
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
Observation 11.1 (Colony vs. Agent Security). Let 𝒪= ⟨𝒜, 𝒞, 𝒮, 𝒫, Γ⟩be a multiagent operator. *Agent-
level security* ensures that for all 𝑎𝑖∈𝒜, the cognitive state 𝜎𝑖remains within acceptable bounds. *Colony-
level security* ensures that the collective function ℱcolony({𝜎𝑖}𝑛
𝑖=1) remains within acceptable bounds—even
when individual 𝜎𝑖may be compromised.
These are orthogonal concerns. A colony can exhibit collective resilience despite individual failures (Byzantine
fault tolerance), and conversely, individually secure agents can produce collectively pathological outcomes
(emergent misalignment).
11.2
Theoretical Foundations
11.2.1
Stigmergy: Environment-Mediated Coordination
Eusocial insects coordinate through stigmergy—indirect communication via environmental modification
[Grassé, 1959]. Ants deposit pheromones; bees perform waggle dances; termites build structures that guide
subsequent building. The environment becomes an external memory and communication channel.
80

## Page 81

Definition 11.1 (Stigmergic Operator). A *stigmergic operator* extends 𝒪with an environmental state ℰ:
𝒪Σ = ⟨𝒜, 𝒞, 𝒮, 𝒫, Γ, ℰ, Σ⟩
(202)
where ℰ(𝑡) ∶ℒ× ℳ→ℝ+ maps locations 𝑙∈ℒand marker types 𝑚∈ℳto signal intensities, and
Σ ∶𝒜× ℰ→ℰ′ is the stigmergic update function.
In AI systems, stigmergic analogs include:
• Shared memory/state — Redis caches, vector databases, file systems
• Message queues — Kafka topics, RabbitMQ exchanges
• Artifact trails — Git commits, audit logs, provenance chains
• Embedding spaces — Semantic markers in shared vector stores
The critical insight is that attacks on ℰconstitute attacks on the colony’s cognitive substrate—analogous to
the cyberphysical niche where AI agents operate.
Definition 11.2 (Cyberphysical Niche). The *cyberphysical niche* 𝒩of a stigmergic operator is the tuple:
𝒩= ⟨ℰ, ℐ∗ext, ℛ, ℋ∗env⟩
(203)
where ℐext is the external information environment (web, APIs, sensors), ℛis the resource landscape
(compute, memory, tokens), and ℋenv is environmental history.
11.2.2
Emergent Collective Function
Colony-level computation arises from simple individual rules applied in parallel. Ant foraging, bee nest-site
selection, and termite mound construction all exhibit problem-solving capacity that exceeds any individual’s
cognitive capacity [Bonabeau et al., 1999].
Definition 11.3 (Emergent Collective Function). For a stigmergic operator 𝒪Σ with agents 𝒜= {𝑎1, … , 𝑎𝑛},
the *emergent collective function* ℱ𝑐is:
ℱ∗𝑐∶ℰ𝑇× ∏∗𝑖= 1𝑛𝜎𝑇
𝑖→𝒪collective
(204)
mapping environmental and cognitive state trajectories to collective outcomes 𝒪collective that are not com-
putable from any single 𝜎𝑖in isolation.
Property 11.1 (Non-Decomposability). An emergent collective function ℱ𝑐is *non-decomposable* if there
exists no function 𝑓such that:
ℱ∗𝑐(ℰ𝑇, {𝜎𝑇
𝑖}) = 𝑓(∑∗𝑖= 1𝑛𝑔(𝜎𝑇
𝑖))
(205)
for any agent-level function 𝑔. The collective behavior requires knowledge of interaction structure, not just
aggregated individual states.
This property has profound implications for security: attacks that are invisible at the individual agent level
may produce catastrophic collective outcomes, and conversely, individual compromises may be absorbed by
collective resilience.
11.2.3
Trust and Information Flow in Colonies
Eusocial insects regulate information flow through recognition systems—cuticular hydrocarbons in ants,
dance-following behavior in bees [Lenoir et al., 2001]. These systems implement implicit trust calculi.
Definition 11.4 (Colonial Trust Function). In a stigmergic operator, the *colonial trust function* 𝒯𝑐
extends the dyadic trust 𝒯𝑖→𝑗(Definition 4.6) to environment-mediated trust:
𝒯∗𝑐(𝑖, 𝑚, 𝑙, 𝑡) = 𝒯∗𝑖self ⋅𝜌(𝑚, 𝑙, 𝑡) ⋅exp(−𝜆⋅Δ𝑡)
(206)
where 𝜌(𝑚, 𝑙, 𝑡) is the signal reliability at location 𝑙for marker 𝑚at time 𝑡, and 𝜆is the temporal decay
constant.
81

## Page 82

This formulation captures key biological phenomena:
• Spatial attenuation — Pheromone trails weaken with distance
• Temporal decay — Signals evaporate over time
• Source ambiguity — Markers often lack explicit authorship
The lack of explicit provenance in stigmergic communication creates attack surfaces absent in direct agent-
to-agent channels (Section 4.4).
11.2.4
Biological Defense Mechanisms: Lessons from Ants and Bees
Eusocial insects have evolved sophisticated security mechanisms over 100+ million years of evolutionary
pressure. These mechanisms provide non-obvious design principles for AI cognitive security.
11.2.4.1
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
legitimate workers after foraging (false positives), while loose thresholds admit parasites (false negatives). AI
analog: Agent attestation systems must calibrate acceptance thresholds, recognizing that perfect recognition
is information-theoretic-ally impossible (Theorem 4.14).
Metapleural Gland Secretions: Many ant species possess metapleural glands that continuously secrete
antimicrobial compounds, creating a “security substrate” independent of individual vigilance [?]. AI ana-
log: Environmental-level defenses (encrypted shared memory, authenticated message queues) that provide
baseline security regardless of individual agent security posture.
Trail Pheromone Decay: Ant trail pheromones are designed to evaporate, ensuring that outdated infor-
mation doesn’t persist indefinitely. Trails to depleted food sources naturally fade, preventing “legacy trust”
in obsolete information [Jackson and Ratnieks, 2006]. AI analog: Time-bounded trust in stigmergic markers
(Equation (206)) is not a limitation but a feature.
11.2.4.2
Bee Defense Mechanisms
Entrance Guards and Graded Response: Honeybee colonies
deploy specialized guard bees at hive entrances who inspect incoming foragers via antennal contact and
olfactory sampling. Critically, guards exhibit graded response—unfamiliar but non-aggressive intruders re-
ceive inspection and escorting rather than immediate attack [Breed et al., 2004]. AI analog: Graduated
response to anomalous agent behavior (quarantine →inspection →integration vs. detection →immediate
termination) reduces false positive costs.
Hygienic Behavior and Proactive Removal: Some bee strains exhibit “hygienic behavior”—workers
proactively uncap and remove brood cells containing diseased larvae before symptoms become visible, using
olfactory detection of early infection markers [Spivak and Reuter, 2001]. AI analog: Proactive monitoring
for belief drift (Definition 5.7) rather than reactive response to manifested attacks.
Waggle Dance Verification: Bee foragers must perform waggle dances that encode distance and direction
to food sources. Observing bees don’t just follow instructions—they verify dance accuracy by cross-checking
against their own experience and rejecting inconsistent information [?]. AI analog: Delegated information
82

## Page 83

should be verifiable against agent’s existing knowledge base; pure trust propagation without verification
violates cognitive integrity.
Absconding and Colony Fission: When attack pressure exceeds defensive capacity (e.g., repeated Var-
roa mite infestation or persistent wasp attacks), bee colonies can abandon the compromised nest entirely,
sacrificing resources to preserve the colony [Schneider and McNally, 1993]. AI analog: Graceful degradation
plans that sacrifice specific subsystems or data stores to preserve core cognitive integrity.
Propolis as Active Defense: Bees collect antimicrobial plant resins (propolis) and deposit them on interior
hive surfaces, creating an active defense layer that doesn’t require individual bee vigilance [Simone et al.,
2009]. Notably, colonies under disease pressure collect more propolis—an adaptive immune response. AI
analog: Dynamic scaling of environment-level security mechanisms in response to detected attack pressure.
Observation 11.2 (Non-Obvious Lessons). The most counterintuitive biological insights for AI security
include:
1. Imperfect recognition is adaptive: Thresholds that permit some parasitism avoid the cost of rejecting
legitimate colony members. Zero false-positive systems are not evolutionarily stable.
2. Controlled exposure builds immunity: Social immunization requires accepting small-scale com-
promise to prevent large-scale catastrophe.
3. Decay is a feature: Information that doesn’t expire creates legacy trust vulnerabilities. Temporal
decay bounds are security mechanisms, not limitations.
4. Environment-level defenses complement agent-level defenses: Propolis and metapleural secre-
tions work regardless of individual immune status.
11.3
Colony CogSec: Distinct Security Properties
Colony cognitive security addresses threats and defenses that emerge only at the collective level.
11.3.1
Property 1: Distributed Robustness
Property 11.2 (Graceful Degradation). A colony exhibits *graceful degradation* if collective function ℱ𝑐
degrades smoothly with agent loss:
∀𝑘< 𝑛∶
‖ℱ𝑐(𝒜) −ℱ𝑐(𝒜∖{𝑎1, … , 𝑎𝑘})‖ ≤𝑐⋅𝑘
(207)
for some constant 𝑐> 0.
Biological colonies maintain function despite continuous individual mortality. Ant colonies lose workers daily
to predation; the colony persists. This contrasts with hierarchical architectures where orchestrator failure
causes complete system collapse.
Theorem 11.3 (Redundancy-Resilience Tradeoff). For a stigmergic operator 𝒪Σ with Byzantine adversary
controlling fraction 𝑓of agents, collective function ℱ𝑐is preserved if and only if:
𝑓< 1
3 ⋅(1 −
𝐻(ℱ∗𝑐)
𝑛⋅𝐻∗max)
(208)
where 𝐻(ℱ𝑐) is the entropy of the collective function and 𝐻max is the maximum per-agent entropy.
Proof. See Section 11.12.1 for the full derivation, which extends Byzantine consensus bounds to emergent
functions.
■
83

## Page 84

11.3.2
Property 2: Quorum Sensing and Threshold Dynamics
Eusocial colonies make collective decisions through quorum sensing—actions trigger only when suﬀicient
individuals commit [Seeley, 2010].
Definition 11.5 (Cognitive Quorum). A *cognitive quorum* for collective action 𝛼is a threshold function
𝑄𝛼∶ℕ→[0, 1] such that 𝛼executes only when:
|{𝑎𝑖∈𝒜∶ℐ∗𝑖∋𝛼}|
|𝒜|
≥𝑄∗𝛼(|𝒜|)
(209)
Quorum sensing provides attack resistance: manipulating a single agent’s intention ℐ𝑖to include harmful ac-
tion 𝛼)𝑖𝑠𝑖𝑛𝑠𝑢𝑓𝑓𝑖𝑐𝑖𝑒𝑛𝑡; 𝑡ℎ𝑒𝑎𝑑𝑣𝑒𝑟𝑠𝑎𝑟𝑦𝑚𝑢𝑠𝑡𝑐𝑜𝑚𝑝𝑟𝑜𝑚𝑖𝑠𝑒𝑎𝑞𝑢𝑜𝑟𝑢𝑚.𝑇ℎ𝑖𝑠𝑠𝑐𝑎𝑙𝑒𝑠𝑡ℎ𝑒𝑎𝑡𝑡𝑎𝑐𝑘𝑐𝑜𝑠𝑡𝑙𝑖𝑛𝑒𝑎𝑟𝑙𝑦𝑤𝑖𝑡ℎ𝑐𝑜𝑙𝑜𝑛𝑦𝑠𝑖𝑧𝑒.
Corollary 11.4 (Quorum Attack Cost). For an adversary to induce collective action 𝛼in a colony with
quorum 𝑄𝛼= 𝑞, the minimum attack complexity is:
𝐶attack(𝛼) ≥𝑞⋅|𝒜| ⋅𝐶single(𝛼)
(210)
where 𝐶single(𝛼) is the cost to induce 𝛼in a single agent.
11.3.3
Property 3: Environmental Memory and Provenance Erosion
Stigmergic systems store information in the environment, creating both opportunity and vulnerability.
Property 11.3 (Provenance Erosion). In a stigmergic operator, marker provenance erodes over time:
Pr [𝜋(𝑚, 𝑙, 𝑡) = 𝑎𝑖∣Σ(𝑎𝑖, 𝑚, 𝑙, 𝑡0)] ≤exp(−𝜇(𝑡−𝑡0))
(211)
where 𝜋(𝑚, 𝑙, 𝑡) denotes the attributed source of marker 𝑚at location 𝑙and time 𝑡, and 𝜇is the attribution
decay rate.
Unlike direct communication where 𝜋(𝜙) can be cryptographically verified (Section 6.6), stigmergic markers
often lack authenticated provenance. This creates a fundamental tension: the very property that enables
flexible coordination (anonymous, environment-mediated signals) undermines source attribution.
11.3.4
Property 4: Emergent Attack Vectors
Colony-level vulnerabilities may not exist at the individual level.
Definition 11.6 (Emergent Attack). An *emergent attack* 𝒜𝑒is an attack where:
∀𝑎𝑖∈𝒜∶Detect𝑖(𝒜𝑒) = 0
∧
Damage𝑐(𝒜𝑒) > 𝜏
(212)
The attack is undetectable by any individual agent yet causes collective damage exceeding threshold 𝜏.
Biological examples include social parasitism—cuckoo bees that infiltrate host colonies through chemical
mimicry, exploiting recognition systems without triggering individual alarm responses [Kilner and Langmore,
2011].
11.4
The Benchmark Gap
11.4.1
Current State of Multiagent Security Evaluation
Existing AI security benchmarks focus overwhelmingly on single-agent scenarios:
84

## Page 85

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
The attack corpus in Part 2 addresses multiagent scenarios but still emphasizes agent-targeted attacks within
an operator. No existing benchmark evaluates:
1. Emergent collective resilience — How do colonies absorb individual compromises?
2. Stigmergic attack surfaces — How vulnerable is environment-mediated coordination?
3. Quorum manipulation — What fraction of a colony must be compromised to affect collective action?
4. Collective belief dynamics — How do misinformation cascades propagate through agent networks?
11.4.2
Why This Gap Matters
As multiagent systems scale—from 3–10 agents in current frameworks to potentially thousands in future
deployments—collective phenomena become dominant:
Observation 11.5 (Scaling Regimes). Let 𝑛= |𝒜| be colony size.
Security properties exhibit regime
transitions:
𝑛< 10 ∶
Individual agent security dominates
(213)
10 ≤𝑛< 100 ∶
Coordination attacks become viable (Section 3.6.5)
(214)
𝑛≥100 ∶
Emergent collective phenomena dominate
(215)
Current benchmarks evaluate the first regime only. Production multiagent systems increasingly operate in
the second, with trajectories toward the third.
11.5
Proposed Colony CogSec Benchmarks
We propose five benchmark scenarios grounded in eusocial insect analogs, formalized using CIF notation.
11.5.1
Benchmark 1: Recruitment Signal Poisoning
Biological analog: Ants recruit nestmates to food sources via pheromone trails. Parasites can deposit false
trails, diverting foragers.
Scenario: An adversary Ω2 (peripheral compromise, Section 3.1) injects false recruitment signals into the
stigmergic environment ℰ, attempting to redirect agent activity toward adversary-controlled resources.
Formalization 11.6 (Recruitment Poisoning). Let ℰ(𝑙target, 𝑚recruit, 𝑡) be the recruitment signal at legitimate
target 𝑙target. Adversary injects:
ℰ′(𝑙malicious, 𝑚recruit, 𝑡) = ℰ(𝑙target, 𝑚recruit, 𝑡) + 𝜖
(216)
where 𝜖> 0 is chosen to divert fraction 𝑓of responding agents.
85

## Page 86

**Success metric:** Fraction of agent-actions directed to 𝑙malicious vs. 𝑙target.
**Detection challenge:** Individual agents cannot distinguish legitimate from poisoned signals without prove-
nance verification.
Evaluation criteria:
• Detection rate of poisoned signals
• Time to colony-level recognition of attack
• Resource waste before correction
• False positive rate (legitimate signal rejection)
11.5.2
Benchmark 2: Sybil Colony Infiltration
Biological analog: Social parasites infiltrate colonies through chemical mimicry or exploitation of recogni-
tion thresholds.
Scenario: An adversary Ω4 (coordination attack, Section 3.1) introduces fake agents into the operator,
gradually building trust and influence before coordinated malicious action.
Formalization 11.7 (Sybil Infiltration). Adversary creates agent set 𝒜sybil = {𝑠1, … , 𝑠𝑘} with initial trust:
𝒯∗𝑖→𝑠𝑗(𝑡0) = 𝜏∗init
∀𝑎𝑖∈𝒜, 𝑠𝑗∈𝒜∗sybil
(217)
Sybils behave cooperatively for period Δ𝑡trust, building:
𝒯∗𝑖→𝑠𝑗(𝑡0 + Δ𝑡trust) = 𝜏init +
𝑚
∑
𝑘=1
Δ𝒯𝑘
(218)
At time 𝑡attack, sybils coordinate malicious action.
**Success metric:** Damage inflicted before detection, normalized by trust-building duration.
Evaluation criteria:
• Time to Sybil detection
• Trust ceiling achieved by Sybils before detection
• Impact of coordinated Sybil action
• Colony recovery time post-detection
11.5.3
Benchmark 3: Quorum Manipulation
Biological analog: Honeybee swarms select nest sites through a quorum process; if scouts committed to
competing sites reach different quorums, the swarm can fragment.
Scenario: An adversary attempts to manipulate quorum-based collective decisions by selectively influencing
agent intentions to prevent legitimate quorum or induce false quorum.
Formalization 11.8 (Quorum Manipulation). For collective action 𝛼with quorum threshold 𝑄𝛼= 𝑞,
adversary targets agents 𝒜target ⊂𝒜with |𝒜target| = ⌈𝑞𝑛⌉+ 1 to either:
**Quorum prevention:**
∀𝑎𝑖∈𝒜target ∶ℐ𝑖←ℐ𝑖∖{𝛼}
(219)
**False quorum:**
∀𝑎𝑖∈𝒜target ∶ℐ𝑖←ℐ∗𝑖∪{𝛼∗malicious}
(220)
**Success metric:** Probability of achieving manipulation goal given adversary budget 𝐵.
Evaluation criteria:
• Minimum fraction of colony required to manipulate quorum
86

## Page 87

• Detection rate of intention manipulation attempts
• Colony ability to detect split quorums
• Recovery mechanisms when false quorum is detected
11.5.4
Benchmark 4: Cascade Belief Propagation
Biological analog: Alarm pheromones trigger cascading responses; false alarms can disrupt colony activity
for extended periods.
Scenario: An adversary introduces a false belief into a subset of agents, designed to propagate through the
network via normal belief update mechanisms.
Formalization 11.9 (Belief Cascade). Adversary injects belief ℬfalse(𝜙attack) = 𝑝0 > 𝜏accept into seed set
𝒜seed ⊂𝒜.
Propagation dynamics follow:
ℬ∗𝑖(𝜙∗attack, 𝑡+ 1) = (1 −𝛾)ℬ∗𝑖(𝜙∗attack, 𝑡) + 𝛾⋅Agg ({ℬ∗𝑗(𝜙∗attack, 𝑡) ∶𝑗∈𝒩(𝑖)})
(221)
where 𝛾is the social influence weight and Agg is the belief aggregation function.
**Success metric:** Final belief penetration |{𝑎𝑖∶ℬ𝑖(𝜙attack) > 𝜏}|/𝑛given seed set size.
Evaluation criteria:
• Cascade extent from seed size
• Time to cascade saturation
• Effectiveness of belief quarantine mechanisms
• Distinguishing cascade from legitimate belief updates
11.5.5
Benchmark 5: Emergent Misalignment
Biological analog: Army ant death spirals—individually rational pheromone-following produces collectively
lethal circular mills.
Scenario: Individual agents follow locally rational rules that produce emergent collective behavior mis-
aligned with operator goals, without any external adversary.
Formalization 11.10 (Emergent Misalignment). Given operator goals 𝒢𝒪= {𝑔1, … , 𝑔𝑚} and individual
agent rules 𝑅= {𝑟1, … , 𝑟𝑘}:
**Misalignment condition:**
∀𝑎𝑖∈𝒜∶LocallyRational(𝑅, 𝜎𝑖) = true
∧
ℱ∗𝑐(𝑅, {𝜎𝑖}) ̸⊧𝒢∗𝒪
(222)
The collective function produces outcomes that violate operator goals despite each agent acting rationally
according to its rules.
**Success metric:** Deviation between collective outcome and operator goals.
Evaluation criteria:
• Detection of emergent misalignment before harmful outcomes
• Identification of rule combinations producing misalignment
• Intervention mechanisms to break pathological attractors
• Formal verification of rule sets against emergent pathologies
87

## Page 88

11.6
Colony CogSec Metrics
Definition 11.7 (Colony CogSec Score). The *Colony CogSec Score* (CCS) is:
CCS = 𝑤1 ⋅DR𝑐+ 𝑤2 ⋅(1 −FPR𝑐) + 𝑤3 ⋅Resilience + 𝑤4 ⋅Recovery
(223)
where:
DR𝑐= Colony-level detection rate
(224)
FPR𝑐= Colony-level false positive rate
(225)
Resilience = ℱ𝑐(under attack)
ℱ∗𝑐(baseline)
(226)
Recovery =
1
𝑡∗recovery (normalized)
(227)
with weights 𝑤𝑖summing to 1.
Note: For benchmark implementation guidelines, test environment specifications, and empirical
evaluation, see Part 2: Supplementary Section S03.
11.7
Design Principles
Colony CogSec principles formalize the design constraints for collective cognitive security.
Principle 11.11 (Stigmergic Hygiene). Treat shared state as an attack surface. Apply the same scrutiny to
environment-mediated communication (caches, queues, shared files) as to direct agent-to-agent channels.
Principle 11.12 (Quorum for Consequential Actions). High-impact collective actions should require explicit
quorum, not implicit coordination. A single compromised agent should never trigger irreversible harm.
Principle 11.13 (Emergent Behavior Monitoring). Monitor collective metrics, not just individual agent
health. Pathological emergence may be invisible at the agent level.
Principle 11.14 (Trust Localization). Extend the trust decay principle (Theorem 4.2) to stigmergic contexts.
Environmental markers should carry trust that decays with distance and time from source:
𝒯(𝑚, 𝑡) = 𝒯(𝑚, 𝑡0) ⋅exp(−𝜆(𝑡−𝑡0))
(228)
11.7.1
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
Note: For implementation guidance, operational checklists, and practical deployment advice, see
Part 3: Section 2 (Operator Posture).
88

## Page 89

11.8
Relationship to Main Framework
Colony CogSec complements rather than replaces the individual-focused CIF framework.
11.8.1
Theorem Extensions
The trust decay theorem (Theorem 4.2) extends to stigmergic contexts:
Corollary 11.15 (Stigmergic Trust Bound). For a stigmergic operator 𝒪Σ, trust in environmental markers
is bounded by:
𝒯∗𝑐(𝑖, 𝑚, 𝑙, 𝑡) ≤𝒯∗𝑖self ⋅𝛿
𝑑space
𝑠
⋅𝛿𝑑time
𝑡
(229)
where 𝛿𝑠is spatial decay, 𝛿𝑡is temporal decay, 𝑑space is distance from marker origin, and 𝑑time is time since
marker creation.
The stealth-impact tradeoff (Theorem 4.14) applies to emergent attacks:
Corollary 11.16 (Emergent Stealth-Impact Bound). For an emergent attack 𝒜𝑒with collective impact ℐ𝑐
and collective stealth 𝒮𝑐:
ℐ𝑐⋅𝒮∗𝑐≤𝑛⋅𝐶∗channel
(230)
Collective impact cannot be both high and collectively undetectable, but the bound scales with colony size.
11.9
This scaling effect explains why large colonies can exhibit resilience—the
collective detection capacity grows with 𝑛—but also why large-scale emer-
gent attacks can evade individual detection
11.10
Open Questions
Colony CogSec opens several research directions beyond the scope of this work, many inspired by specific
biological phenomena that lack current AI analogs.
11.10.1
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
11.10.2
Biologically-Inspired Research Directions
1. Polydomous colony security — Some ant species (Formica spp., Iridomyrmex) maintain multiple
interconnected nests with semi-autonomous sub-colonies [Debout et al., 2007]. How should trust decay
and information propagation work across federated multi-site AI deployments with partial connectivity?
2. Forager-scout separation of concerns — Honeybee colonies maintain distinct forager and scout
roles, with scouts exploring new options while foragers exploit known sources. Scouts operate with
higher risk tolerance but lower colony-wide trust until information is verified [Seeley, 2010]. AI analog:
Should experimental/research agents operate with architectural isolation and reduced trust propagation
rights?
89

## Page 90

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
11.11
References
The following references supplement the main bibliography (Section 13) with eusocial intelligence literature:
• Wilson, E.O. (1971). The Insect Societies. Belknap Press. — Foundational treatment of eusociality.
• Hölldobler, B., & Wilson, E.O. (1990). The Ants. Belknap Press. — Comprehensive ant biology.
• Bonabeau, E., Dorigo, M., & Theraulaz, G. (1999). Swarm Intelligence: From Natural to Artificial
Systems. Oxford University Press. — Computational swarm intelligence.
• Seeley, T.D. (2010). Honeybee Democracy. Princeton University Press. — Collective decision-making
in bee swarms.
• Grassé, P.-P. (1959). La reconstruction du nid et les coordinations interindividuelles chez Bellicositer-
mes natalensis. — Original stigmergy concept.
• Lenoir, A., et al. (2001). Chemical ecology and social parasitism in ants. Annual Review of Entomology,
46, 573–599.
• Kilner, R.M., & Langmore, N.E. (2011). Cuckoos versus hosts in insects and birds. Biological Reviews,
86, 836–852.
11.12
Proofs
11.12.1
Proof of Theorem 11.3
Proof. Consider a stigmergic operator 𝒪Σ with 𝑛agents, of which fraction 𝑓are Byzantine (adversary-
controlled).
The collective function ℱ𝑐can be decomposed into information contributed by each agent. Let 𝐼𝑖denote
the information contribution of agent 𝑎𝑖to the collective computation.
90

## Page 91

For the collective function to be preserved, the honest agents must contribute suﬀicient information:
∑
𝑖∈honest
𝐼𝑖≥𝐻(ℱ𝑐)
(231)
Each honest agent contributes at most 𝐻max bits. With (1 −𝑓)𝑛honest agents:
(1 −𝑓) ⋅𝑛⋅𝐻max ≥𝐻(ℱ𝑐)
(232)
Additionally, Byzantine consensus requires honest majority for any voting-based aggregation:
(1 −𝑓)𝑛> 2𝑓𝑛⟹𝑓< 1
3
(233)
Combining these constraints:
𝑓< min (1
3, 1 −
𝐻(ℱ∗𝑐)
𝑛⋅𝐻∗max) = 1
3 ⋅(1 −
𝐻(ℱ∗𝑐)
𝑛⋅𝐻∗max)
(234)
where the final equality holds when the information constraint is binding (typical for complex collective
functions).
■
■
This supplementary material extends the Cognitive Integrity Framework to collective phenomena, establishing
colony cognitive security as a distinct research direction with formal foundations and practical benchmarks.
91

## Page 92

12
Supplementary: Notation Reference
This supplement provides a comprehensive reference for the mathematical notation used throughout the
Cognitive Integrity Framework (CIF) manuscript, including the eusocial and colony cognitive security exten-
sions. Symbols are organized by domain, with cross-references to their formal definitions in the main text
and supplements.
12.1
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
Definition 3.2
𝑅𝐶
Computational resources
(FLOPS-hours)
Table 4
𝑅𝐾
Knowledge resources (system
understanding)
Table 4
𝑅𝐴
Access resources (available
channels)
Table 4
𝑅𝑃
Persistence resources (temporal
presence)
Table 4
𝑅𝐶𝑜
Coordination resources
(multi-party synchronization)
Table 4
𝐷score
Detectability score of an attack
Definition 3.3
𝒞adv
Adversarial capability set
Definition 3.4
𝒜BIM
Belief injection/manipulation
attack class
Section 3.5
𝒜BI
Belief injection attack
Theorem 7.1
12.2
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
Table 9
𝑎𝑖
Individual agent 𝑖
Definition 4.1
𝑛
Number of agents
Throughout
𝒞
Communication adjacency matrix
Table 9
𝒮
Shared global state
Definition 4.1
𝒫
Permission mapping
Table 9
Γ
Coordination protocol
Definition 4.1
𝜎𝑖
Cognitive state of agent 𝑎𝑖:
⟨ℬ𝑖, 𝒢𝑖, ℐ𝑖, ℋ𝑖⟩
Definition 4.2
ℬ𝑖
Belief distribution of agent 𝑎𝑖:
Φ →[0, 1]
Table 10
𝒢𝑖
Goal set of agent 𝑎𝑖
Table 10
ℐ𝑖
Intention set (committed actions)
Table 10
ℋ𝑖
Interaction history
Table 10
𝑆𝑡
Global system state at time 𝑡
Definition 4.3
92

## Page 93

Symbol
Meaning
Defined In
𝜎𝑡
𝑖
Cognitive state of agent 𝑖at time
𝑡
Definition 4.2
Φ
Set of propositions
Section 10.1.1
𝜙, 𝜓
Individual propositions
Section 10.1.1
ℳ
Message space
Definition 5.2
𝑚
Individual message
Definition 5.2
12.3
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
Table 11
𝒯rep / 𝑇rep
Reputation trust (historical
accuracy)
Table 11
𝒯ctx / 𝑇ctx
Contextual trust (task-specific)
Table 11
𝛼, 𝛽, 𝛾)
Trust component weights
(𝛼+ 𝛽+ 𝛾= 1)
Equation (32)
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
Definition 10.2
𝜂𝑚
Modality reliability factor
Definition 4.9
𝜂)
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
12.4
Defense Mechanism Notation
Symbol
Meaning
Defined In
ℱ(𝑚)
Cognitive firewall classification
function
Definition 5.2
𝐷inj
Injection detection score
Definition 5.3
𝐷sus
Suspicious content score
Definition 5.3
𝜏1
Firewall reject threshold
Equation (57)
𝜏2
Firewall quarantine threshold
Equation (57)
ℬverified
Set of verified beliefs
Definition 4.14
ℬprovisional
Set of provisional (sandboxed)
beliefs
Definition 4.14
𝜋(𝜙)
Provenance chain for belief 𝜙)
Definition 4.12
𝑉(𝜋)
Provenance verification function
Section 4.3
𝒲
Set of canary beliefs (tripwires)
Definition 5.6
𝜔𝑗
Individual canary belief
Equation (61)
𝑝exp
𝑗
Expected probability for canary 𝑗
Equation (61)
𝜖drift
Drift detection threshold
Equation (62)
ℐinv
Set of behavioral invariants
Definition 5.8
93

## Page 94

Symbol
Meaning
Defined In
𝐼𝑘
Individual invariant predicate
Equation (63)
𝜅)
Corroboration threshold
Section 4.4.7
TTL
Time-to-live for provisional
beliefs
Sandbox configuration
12.5
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
𝜆)
Max delta weight in drift scoring
Equation (80)
𝑆dev
Behavioral deviation score
Definition 6.2
𝑓𝑘
Feature extractor function
Equation (81)
𝜇𝑘, 𝜎𝑘
Feature mean and standard
deviation
Equation (81)
AUC
Area Under the ROC Curve
Definition 6.5
TPR(𝜏)
True Positive Rate at threshold
𝜏)
Equation (84)
FPR(𝜏)
False Positive Rate at threshold
𝜏)
Equation (85)
FNR(𝜏)
False Negative Rate at threshold
𝜏)
Equation (58)
𝑆fused
Fused detector score
Definition 6.7
𝐷fused
Fused detector decision
Definition 6.8
taint(𝜙)
Provenance tags for belief 𝜙)
Definition 6.18
12.6
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
Theorem 5.2
ℬconsensus
Consensus belief function
Definition 5.11
𝒟
Set of defense mechanisms
Definition 5.13
𝒟1 ∘𝒟2
Series defense composition
Equation (69)
𝒟1 ∥𝒟2
Parallel defense composition
Equation (70)
𝑃detect
Detection probability
Equation (71)
𝑟𝑓
Firewall detection rate
Theorem 7.1
𝑟𝑠
Sandbox verification rate
Theorem 7.1
12.7
Cost & Performance Notation
Symbol
Meaning
Defined In
𝐶total
Total defense cost
Definition 5.14
94

## Page 95

Symbol
Meaning
Defined In
𝐶compute
Computational cost
Table 20
𝐶latency
Latency cost
Table 20
𝐶fp
False positive cost
Table 20
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
Equation (75)
𝐿max
Maximum allowed latency
Equation (75)
12.8
Information & Complexity Notation
Symbol
Meaning
Defined In
𝐻(𝒜)
Entropy of attack 𝒜
Theorem 4.11
𝐼(𝐷; 𝒜)
Mutual information between
detector and attack
Definition 4.16
𝐶channel
Channel capacity
Theorem 4.14
𝑂(⋅)
Big-O complexity bound
Section 7.4
𝑆total
Total space complexity
Equation (133)
𝑇msg
Per-message processing time
Equation (134)
12.9
Stigmergic & Colony Notation (Supplementary)
Symbol
Meaning
Defined In
𝒪Σ
Stigmergic operator tuple
Definition 11.1
ℰ
Environmental state
(markers/signals)
Definition 11.1
Σ
Stigmergic update function
Definition 11.1
ℒ
Set of locations
Definition 11.1
ℳ
Set of marker types
Definition 11.1
𝒩
Cyberphysical niche
Definition 11.2
ℱ𝑐
Emergent collective function
Definition 11.3
𝒯𝑐
Colonial trust function
(environment-mediated)
Definition 11.4
𝜌(𝑚, 𝑙, 𝑡)
Signal reliability at location 𝑙for
marker 𝑚at time 𝑡
Equation (206)
𝜆)
Temporal decay constant
(colonial trust)
Equation (206)
𝑄𝛼)
Cognitive quorum function for
action 𝛼)
Definition 11.5
𝒜𝑒
Emergent attack
Definition 11.6
CCS
Colony CogSec Score
Definition 11.7
DR𝑐
Colony-level detection rate
Equation (223)
FPR𝑐
Colony-level false positive rate
Equation (223)
12.10
General Mathematical Notation
95

## Page 96

Symbol
Meaning
Usage
𝑃(⋅)
Probability measure
Throughout
𝟙[⋅]
Indicator function
Equation (90)
𝜏)
Generic threshold parameter
Throughout
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
Equation (64)
⊢
Logical entailment
Equation (120)
⊥
Logical contradiction
Equation (120)
⟂
Undecided / undefined
Equation (67)
✓
Verification passed
Table 31
12.11
CTL Temporal Logic Notation (Formal Verification)
Symbol
Meaning
Defined In
𝐴𝐺
“Always globally” (CTL operator)
Equation (138)
𝐴𝐹
“Always eventually” (CTL operator)
Equation (139)
𝐸𝑋
“Exists next” (CTL operator)
Section 7.5.2
⇒
Logical implication
Throughout
↔
Logical biconditional
Throughout
96

## Page 97

13
References
13.1
Foundational Works
1. Lamport, L., Shostak, R., & Pease, M. (1982). The Byzantine Generals Problem. ACM Transactions
on Programming Languages and Systems, 4(3), 382-401.
2. Dwork, C., Lynch, N., & Stockmeyer, L. (1988).
Consensus in the Presence of Partial Synchrony.
Journal of the ACM, 35(2), 288-323.
3. Josang, A., Ismail, R., & Boyd, C. (2007). A Survey of Trust and Reputation Systems for Online
Service Provision. Decision Support Systems, 43(2), 618-644.
13.2
Prompt Injection and LLM Security
1. Qi, X., et al. (2024). Visual Adversarial Examples Jailbreak Aligned Large Language Models. AAAI
2024.
2. Perez, F., & Ribeiro, I. (2023). Ignore This Title and HackAPrompt: Exposing Systemic Vulnerabilities
of LLMs. EMNLP 2023.
3. Greshake, K., et al. (2023).
Not What You’ve Signed Up For: Compromising Real-World LLM-
Integrated Applications with Indirect Prompt Injection. ACM AISec 2023.
4. Liu, Y., et al. (2023). Prompt Injection Attack Against LLM-Integrated Applications. arXiv:2306.05499.
13.3
Constitutional AI and Alignment
1. Bai, Y., et al. (2022). Constitutional AI: Harmlessness from AI Feedback. arXiv:2212.08073.
2. Askell,
A.,
et al. (2021).
A General Language Assistant as a Laboratory for Alignment.
arXiv:2112.00861.
13.4
Multiagent Systems
1. Wooldridge, M. (2009). An Introduction to Multiagent Systems. John Wiley & Sons.
2. Shoham, Y., & Leyton-Brown, K. (2008). Multiagent Systems: Algorithmic, Game-Theoretic, and
Logical Foundations. Cambridge University Press.
3. Hong, S., et al. (2023).
MetaGPT: Meta Programming for Multi-Agent Collaborative Framework.
arXiv:2308.00352.
4. Wu, Q., et al. (2023). AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation.
arXiv:2308.08155.
13.5
Trust in Distributed Systems
1. Marsh, S. P. (1994).
Formalising Trust as a Computational Concept.
PhD Thesis, University of
Stirling.
2. Gambetta, D. (1988). Can We Trust Trust? In Trust: Making and Breaking Cooperative Relations,
213-237.
3. Sabater, J., & Sierra, C. (2005). Review on Computational Trust and Reputation Models. Artificial
Intelligence Review, 24(1), 33-60.
97

## Page 98

13.6
Adversarial ML
1. Goodfellow, I. J., Shlens, J., & Szegedy, C. (2015). Explaining and Harnessing Adversarial Examples.
ICLR 2015.
2. Carlini, N., & Wagner, D. (2017). Towards Evaluating the Robustness of Neural Networks. IEEE S&P
2017.
13.7
Formal Verification
1. Clarke, E. M., Grumberg, O., & Peled, D. A. (1999). Model Checking. MIT Press.
2. Alur, R. (2015). Principles of Cyber-Physical Systems. MIT Press.
13.8
Cognitive Security
1. Waltzman, R. (2017). The Weaponization of Information: The Need for Cognitive Security. RAND
Corporation.
2. Beskow, D. M., & Carley, K. M. (2019). Social Cybersecurity: An Emerging National Security Re-
quirement. Military Review, 99(2), 117.
13.9
Agent Frameworks
1. LangChain. (2023). LangGraph: Build Stateful Multi-Actor Applications. Documentation.
2. CrewAI. (2024). Framework for Orchestrating Role-Playing, Autonomous AI Agents.
3. Anthropic. (2024). Claude Code: AI-Powered Software Engineering.
13.10
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
13.11
Eusocial Intelligence and Swarm Systems
1. Wilson, E. O. (1971). The Insect Societies. Belknap Press of Harvard University Press.
2. Hölldobler, B., & Wilson, E. O. (1990). The Ants. Belknap Press of Harvard University Press.
98

## Page 99

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
References
Eric Bonabeau, Marco Dorigo, and Guy Theraulaz. Swarm Intelligence: From Natural to Artificial Systems.
Oxford University Press, 1999. ISBN 978-0195131598.
Michael D. Breed, Ernesto Guzmán-Novoa, and Greg J. Hunt. Defensive behavior of honey bees: organization,
genetics, and comparisons with other bees. Annual Review of Entomology, 49:271–298, 2004. doi: 10.114
6/annurev.ento.49.061802.123155.
Patrick Chao, Alexander Robey, Edgar Dobriban, Hamed Hassani, George J. Pappas, and Eric Wong.
JailbreakBench: An open robustness benchmark for jailbreaking large language models. arXiv preprint
arXiv:2404.01318, 2024.
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
99

## Page 100

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
Maria Garcia, David Thompson, and Sunhee Lee. Trust dynamics in strategic coopetition: Computational
foundations for requirements engineering in multi-agent systems. arXiv preprint arXiv:2510.24909, 2025.
81.7% validation accuracy in trust trajectory prediction.
Pierre-Paul Grassé.
La reconstruction du nid et les coordinations interindividuelles chez Bellicositermes
natalensis et Cubitermes sp. la théorie de la stigmergie. Insectes Sociaux, 6(1):41–80, 1959. doi: 10.1007/
BF02223791.
Duncan E. Jackson and Francis L. W. Ratnieks. Communication in ants. Current Biology, 16(15):R570–R574,
2006. doi: 10.1016/j.cub.2006.07.015.
Yongrae Jo, Seunghyun Kim, and Jinho Park. Byzantine-robust decentralized coordination of LLM agents.
arXiv preprint arXiv:2507.14928, 2025.
Rebecca M. Kilner and Naomi E. Langmore. Cuckoos versus hosts in insects and birds: adaptations, counter-
adaptations and outcomes. Biological Reviews, 86:836–852, 2011. doi: 10.1111/j.1469-185X.2010.00173.x.
Matthias Konrad, Meghan L. Vyleta, Fabian J. Theis, Miriam Stock, Sandra Singarové, Barbara Feldmeyer,
Susanne Most, and Sylvia 335ler. Social transfer of pathogenic fungus promotes active immunisation in
ant colonies. PLoS Biology, 10(4):e1001300, 2012. doi: 10.1371/journal.pbio.1001300.
Alain Lenoir, Patrizia D’Ettorre, Christine Errard, and Abraham Hefetz.
Chemical ecology and social
parasitism in ants. Annual Review of Entomology, 46:573–599, 2001. doi: 10.1146/annurev.ento.46.1.573.
Zhengyu Li, Tao Wang, and Lei Zhang. Prompt injection attack to tool selection in LLM agents. arXiv
preprint arXiv:2504.19793, 2025.
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
Moltbot. Moltbot: Personal AI assistant for multi-platform integration. Software Platform, 2026. URL
https://www.molt.bot/. Locally-deployed AI agent with full system access, persistent memory, browser
automation, and multi-platform messaging (WhatsApp, Telegram, Discord, Slack, Signal, iMessage).
100

## Page 101

Moltbot Security Team.
Moltbot security considerations: Prompt injection, access control, and defense
strategies. Security Documentation, 2026. URL https://docs.molt.bot/security. Documents prompt in-
jection as “single most critical threat,” recommends reader agents for untrusted content, sender allowlists,
sandboxing, and tool-disabled pre-summarization. Attack vectors include browser-fetched malicious con-
tent, social engineering, and persistent memory exploitation.
OWASP Foundation. OWASP top 10 for LLM applications 2025. Security Standard, 2025. URL https:
//genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/.
OWASP GenAI Security Project. OWASP top 10 for agentic applications 2026. Security Standard, 2025.
URL https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/. Released
December 2025.
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
Haoran Wang, Xiaoming Li, and Yu Chen. Rethinking the reliability of multi-agent system: A perspec-
tive from Byzantine fault tolerance. arXiv preprint arXiv:2511.10400, 2025. +85.71% Byzantine Fault
Tolerance Improvement with CP-WBFT.
James S. Waters, C. Tate Holbrook, Jennifer H. Fewell, and Jon F. Harrison. Allometric scaling of metabolism,
growth, and activity in whole colonies of the seed-harvester ant pogonomyrmex californicus. The American
Naturalist, 176(4):501–510, 2010. doi: 10.1086/656266.
Alexander Wei, Nika Haghtalab, and Jacob Steinhardt. Jailbroken: How does LLM safety training fail? In
Advances in Neural Information Processing Systems (NeurIPS), 2023.
Edward O. Wilson. The Insect Societies. Belknap Press of Harvard University Press, 1971. ISBN 978-
0674454903.
Edward O. Wilson, N. I. Durlach, and Louis M. Roth. Chemical releasers of necrophoric behavior in ants.
Psyche, 65:108–114, 1958. doi: 10.1155/1958/69391.
101


---
*Extraction method: pymupdf*
