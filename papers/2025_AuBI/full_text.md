# Full Text: Adaptive Basic Income (AuBI): Integrating AI, Decentralized Infrastructure, and Active Inference for Next-Generation Economic Systems

> Extracted from `2025_AuBI.pdf`

---

## Page 1

Adaptive Basic Income (AuBI): Integrating AI,
Decentralized Infrastructure, and Active Inference
for Next-Generation Economic Systems
Adaptive Basic Income (AuBI): Integrating AI, Decentralized 
Infrastructure, and Active Inference for Next-Generation Economic 
Systems
Authors
Die Schwarze Katze (
, 
) 
email Telegram
Andrew Djuwidja, 0009-0006-9402-2412
Daniel Friedman, 0000-0001-6232-9096
CC BY-NC-SA 4.0
DOI: 10.5281/zenodo.17228946
Abstract
Universal Basic Income (UBI) is defined as a transformative economic policy designed to provide all citizens with a regular, 
unconditional sum of money, regardless of their circumstances. 
Here we argue that the overlay of several modern technologies on UBI can help enhance its relevance, effectiveness, and 
impact. We review applications of artificial intelligence (AI) and decentralized infrastructure in UBI application, and describe 
prospects for a cognitive ecosystems approach towards modeling. 
Here we describe a version 0.1 specification for an Adaptive (Universal) Basic Income system called AuBI, describing a systems 
engineering-grade toolkit/sandbox/design suite for specifying, modeling, and designing economic systems. 
Keywords for AuBI include decentralized infrastructure, active inference modules, informed adaptive income, Bayesian 
community income floors, LLM, AI, data storage, data sovereignty, micro UBI, adaptive economic agents, collective predictive 
processing and more. 
 
Introduction
 
Background
 
Active Inference & Generalized Economics Systems
 
AuBI System Architecture
 
Comparing AuBI Variants
 
AuBI Architecture Specification
 •
 •
 •

## Page 2

Discussion
⁠
Supplement: An Indonesian Thought Experiment
⁠
Supplement: Thought Experiments
 
Supplement: Additional Links and Resources

## Page 3

Introduction
Universal Basic Income (UBI) has emerged as a powerful response to the widespread economic disruptions wrought by 
automation and artificial intelligence, yet traditional distribution models often struggle with rigidity, opacity, and uneven impact.
The convergence of advanced machine learning, decentralized ledger technologies, and active inference theory presents a 
transformative opportunity to overcome these challenges by creating adaptive, transparent, and participatory economic 
systems. This paper introduces a new concept, a systems-engineering toolkit designed to specify, model, and deploy next-
generation UBI frameworks that leverage predictive analytics, tamper-proof distributed infrastructure, and cognitive feedback 
loops. Please note that this is only Paper #1 - an introduction and a primer. 
By embedding real-time learning and decentralized governance into UBI program design, UBI x AI x Actinf empowers 
policymakers, researchers, and implementers to experiment with modular policy configurations, continuously refine 
interventions based on observed outcomes, and build more resilient, flexible systems for an evolving global economy.
This paper is an experimental marriage of biologically-grounded theories like Active Inference and the Free Energy Principle, 
decentralized approaches to Artificial Intelligence (AI), meeting unclassical parameters in public goods like Universal Basic 
Income (henceforth referred to as UBI). AI enters the chat to make things computationally efficient for if you’re a social or 
government worker wanting to free up your time and accuracy for more important things. As we dive deeper in the AI x UBI, we 
introduce and flow with a new concept called Adaptive (Universal) Basic Income (henceforth referred to as AuBI) that helps 
us nip the misnomer of unconditionality and universality in the proverbial bud.
For, let’s face it, all public and social experiments, all randomized control trials have conditionality to fulfill for assessment 
reasons. That’s how you select the included population, assess the data, form the hypothesis, and extrapolate conclusions. So 
let’s morph the U on the BI and dive into the realm of AuBI for the purposes of this paper - an Adaptive Basic Income that shifts, 
actively inferencing and dynamically bettering itself, for the benefit of the greater good. 
The Potential Target Audience of this Whitepaper:
AuBI is designed for the doer - (i) the government wanting to experiment with their public goods, (ii) the economists wanting to 
run RCT experiments, (iii) the benevolently wealthy who’d like to give back to society, (iv) the NGO that won funding to 
implement a project on Basic Income, (v) the Foundation that would like to run this on a niche/specific audience, (vi) startups 
who’d like the run microUBI (explained later) experiments in their niche, and (vii) more.
This paper details what running multiple experiments in an enterprise environment, whilst enjoying the benefits of 
decentralization and all the delicious, inferencable data that comes with it, can look like. 
We invite collaborators, clarifications, crypto forks et al. Take this document and make it your own. We only ask that you share 
anonymized data with us, so that the academic pursuit of Active inference and its related theories can be so applied on what 
we believe to be a dynamically changing problem. We assure you with the constant flux of psychographics, sociographics, 
demographics, measurements of micro and macroeconomics, this will only add to substance of your work. 
This thing called B2B2C. We see it, we use it, but we seldom understand it
The technological architecture is designed on a B2B2C model (Business >> to >> Business >> to >> Consumer). Think large 
marketplaces, enterprise software, government banks and more - they all follow a a B2B2C model; one that combines the 
funnel of B2B products and B2C outlets i.e we build the platform that will be used by other businesses, governments, 
enterprises, NGOs, etc, not directly by the consumer. These entities will in turn run and customize the product we’ve built, to 
suit their audience, budget, timelines and more. They will also be responsible for the marketing, outreach, legality, and security 
of the project they are running. 
As a technology creator/provider, AuBI as a concept holds no power or control over the project itself. Think of it as the software 
company you come to when interested in running a AuBI program. It gives you the tools, you do the rest. The specs of this

## Page 4

document may include, but are not limited to, features that may request data purging, private computation, blockchain on and 
off ramps and other such edge-case features as deemed fit. 
The Rabbit-hole Approach for the Uninitiated
Unlike standard papers, this paper is littered with concepts that we encourage you to jump down the Rabbit Hole of. Catch 
some phrases, ideas and make them your own. Seed and sprout them further, radicalize or deradicalize them as you see fit. 
This paper hopes to initiate you into the myriad of permutations that the world is going to need as socio-economic paradigms 
shift around us. Remove the how-it-should-be’s and set methods from your mind, and enter the realm of the humanitarian - 
because at it’s core, that’s what UBI has always been. The purely economic, scientific or socialist lens will fail here.  
Users of this paper are requested to do their own due diligence, include their own extra specs as per 
their applicable local laws, and hold themselves responsible for the projects run. This is a 
speculative design paper and the authors are not responsible for offshoots thereof.

## Page 5

Background
While you could always place these keywords into a Search Bar, here’s a quick background on the 
.
Core AuBI elements

Universal Basic Income (UBI) 
Universal Basic Income embodies dignity, charity, and pragmatic realism by providing individuals a regular, unconditional 
income floor that recognizes a basic right to economic existence. It aims to alleviate poverty at the individual level while 
also mitigating regional cycles of debt and systemic inequalities. More about the world’s most recent UBI experiments can 
be found on 
 and other corners of the internet. 
https://basicincometoday.com/
Recent UBI initiatives worldwide (reviewed in 
) have yielded results showing 
improvements in psychological well-being, labor market flexibility, and community cohesion. These studies affirm UBI’s 
potential but also highlight the difficulty of pinpointing which program features drive specific outcomes. Scaling such 
interventions sustainably hinges on clarifying these causal pathways.
Supplement: Additional Links and Resources
Translating diverse pilot results into robust policy requires an analytical and statistical framework capable of mapping 
causal links across economic, demographic, and behavioral dimensions. By employing advanced modeling techniques and 
machine learning, policymakers would be better able to continuously refine UBI configurations based on real-world impact 
metrics. The evidence-driven approach in this work casts UBI in terms of a modular, adaptive system rather than a static 
transfer mechanism. 
Artificial Intelligence (AI) 
With Artificial Intelligence (AI) features becoming more widely available, AI algorithms have been proposed to optimize UBI 
deployment by analyzing fund disbursement, audience selection, and cross-project learnings to identify the most effective 
resource allocation strategies. This data-driven approach, if implemented in an adaptive, compliant fashion, would 
streamline administration and uncovers latent correlations between socioeconomic indicators and program performance. 
Continuous model retraining and rigorous feature selection could ensure that optimization remains robust against bias and 
overfitting.
→ Tip: Push the AI to give you variants, change parameters yourself, question sources and don’t believe the first result it 
gives you.
AI-driven analytics segment beneficiaries and track longitudinal outcomes across diverse demographics to refine UBI 
design for maximum impact. Sole reliance on purely data-driven predictions risks misalignment when confronted with 
complex human behaviors and economic heterogeneity. Embedding explicit probabilistic models and active inference 
principles bolsters interpretability and supports continuous adaptive policy adjustments.
→ Tip: Feed your LLM some topical or target conversation before you expect it to model perfect analysis for you. Correct it 
and feed it academia as and when needed. 
At the macroeconomic level, machine learning models could be used forecast economic shifts-such as labor market 
dynamics, inflationary pressures, and geopolitical risks-enabling real-time adjustments to AuBI amounts and distribution. 
Charity
Core basis of UBI
Artificial Intelligence (AI)
Descriptive and predictive analytics. 
Decentralized Infrastructure
Private/Secure compute methods
Active Inference
Cognitive economics. Multi-agent. 
Name
Implications
Core AuBI elements
 •
 •
 •
 •
 •
 •

## Page 6

These predictive capabilities fortify safety nets against systemic shocks and enhance policy agility in changing contexts. 
Incorporating explainability and auditability safeguards decision-making integrity and maintains public trust.
→ Tip: Localize and update LLM questions to reflect current affairs for the region in question for higher efficacy. 
Decentralized Infrastructure: 
In AuBI, we suggest that decentralized infrastructure can be used to leverage blockchain-based distributed ledgers to 
create instances of specific systems, dealing with UBI payments and spending behavior, reducing the risk of fraud while 
ensuring transparency and system sovereignty. Drawing on “
”, this approach could support system 
designers to record transactions in cryptographically linked blocks, and employ smart contracts to eliminate intermediaries 
and curb corruption, as shown in 
“Universal basic income on blockchain: the case of 
circles UBI” and 
 “Universal Basic Income in a Blockchain-Based Community Currency”.
→ Tip: Build decentralized redundancy in more open economic geographies for nodes. Ensure your data warehouses are 
not on centralized systems as much as possible. 
Five reasons why Universal Basic Income (UBI) and cryptocurrency are a perfect fit
Papadimitropoulos & Perperidis 2024
Avanzo et al. 2023
By enabling direct digital-wallet payments to unbanked populations, the system enhances financial inclusion and adapts 
seamlessly to shifting global contexts, while decentralized data storage across multiple nodes ensures censorship 
resistance and individual sovereignty. Inspired by the principles of 
 “a belief system asserting that cognition and 
knowledge are fundamental rights that must be protected through transparent, decentralized infrastructures”. While exact 
details of the decentralized infrastructure used would be situation, having some framework in place would empower 
recipients with control over their data and strengthen the integrity of the program administration.
→ Tip: Research existing decentralized, microfinancial systems in the region before you construct your architecture. Learn 
from their mistakes and change platforms, partners and protocols as needed. 
Cognicism
Active Inference
Active Inference is a framework for modeling perception, cognition, and action across systems (
).
Parr et al. 2022
Previously Active Inference modeling has been applied in contexts relevant for AuBI including Microeconomics (
), 
Epistemic commons (
), Cognitive auditing settings (
), Epistemic communities (
), Attention economies (
), and Federated inference (
). 
Kuhn 2025
Friedman et al. 2022
Smékal & Friedman 2022
Albarracin et al. 2022
Bruinberg 2023
Friston et al. 2024
More connections between Active Inference and Economics systems are explored in 
.
Active Inference & Generalized Economics Systems
Here we argue that integrating these methods into the framework of standard UBI presents a promising pathway toward 
equitable economic systems. By harnessing them, one can create a robust, transparent, and efficient system that addresses 
the challenges of poverty and inequality, whilst also adapting to the evolving economic landscape shaped by automation and 
digital transformation.
 •
 •
 •
 •
 •

## Page 7

Active Inference & Generalized Economics
Systems
Active inference theory extends well beyond its biological origins into several domains of artificial intelligence, robotics, 
cognitive science, and even social systems. At its core, active inference provides a unified framework for understanding how 
systems maintain their integrity through prediction and action.
Active inference describes how any system can minimize ‘surprise’ (or free energy) by engaging in the twin processes of:
Updating its internal model to better predict observations
Acting on the environment to make observations match predictions
In both of the above scenarios, it fits squarely into the social and public goods domain of economics (e.g. 
, 
, 
, 
) and Universal Basic Income. 
Kuhn 2025
Henriksen 2020 Fox 2021 Institute 2025
Active Inference and Universal Basic Income
Active Inference theory, a neuroscientific framework that explains how biological systems minimize surprise by predicting their 
sensory inputs, can offer interesting insights when applied to Universal Basic Income (UBI), thereby morphing it gracefully into 
Adaptive Basic Income (AuBI). Building on complex systems science, Active Inference suggests that organisms maintain 
homeostasis by minimizing the difference between expected and actual outcomes. When we apply this to economic policy like 
standard UBI, several connections emerge:
Reducing Uncertainty in Economic Environments
In Active Inference terms, standard UBI could serve as a mechanism for reducing environmental uncertainty. By providing a 
predictable income floor, individuals can better form accurate predictions about their financial future, reducing "prediction 
errors" that lead to stress and suboptimal decision-making.
Enabling Exploratory Behavior
Active Inference proposes that organisms balance exploitative (using known strategies like standard economic parameters) and 
exploratory behaviors (changing social and demographic parameters). AuBI could support what neuroscientists call the 
‘epistemic value’ of actions - allowing individuals to explore new career paths, education, or entrepreneurial ventures with 
reduced financial risk, potentially leading to greater innovation.
Creating Adaptive Economic Agents
In 2025's rapidly evolving economy with increasing automation and AI integration, AuBI could help humans remain adaptive 
agents. From an Active Inference perspective, a financial safety net allows people to update their "generative models" (internal 
representations of how the world works) more effectively when economic conditions change.
Collective Predictive Processing
Societies can be viewed as collective predictive processing systems. AuBI might help synchronize individual economic 
expectations, creating more cohesive societal predictions that reduce economic volatility - similar to how coordinated 
predictions in neural networks stabilize perception.
This framework suggests that beyond addressing immediate poverty concerns, AuBI might fundamentally alter how individuals 
model their economic environment and make decisions under uncertainty - potentially leading to more adaptive economic 
 1.
 2.

## Page 8

behaviors aligned with 2025's changing employment landscape (job loss, climate migration, inflation, currency depreciation, 
asset value flux, etc). 
Societies as Collective Predictive Processing Systems
When we view societies through an Active Inference lens, we can think of them as large-scale networks where individuals are 
constantly predicting, acting, and updating their models based on feedback. Just as the brain uses hierarchical predictive 
processing to make sense of sensory input, societies process economic and social information collectively.
In this framework:
Individual people make predictions about their economic future
These predictions influence their actions (spending, saving, career choices)
Their actions impact others in the network
Collective actions create economic outcomes
These outcomes provide feedback that updates individual predictions
The following section, 
, lays out the core infrastructural modules of the proposed AuBI model, 
which can be used to describe, explore, design, and deploy such systems. 
AuBI System Architecture
 •
 •
 •
 •
 •

## Page 9

AuBI System Architecture
The 
  serves as a blueprint for understanding the structure and functionality of an integrated AuBI 
administrative system, where AI coupled with decentralized modules keep track of the variable baseline and their validations, 
and the recommendations that come from this modular blend. 
AuBI System Architecture
This diagram outlines its various components, their interactions, and the overall flow of data within the system, providing a 
visual representation that will aid in both design and technical implementation of this concept.
Module 1: UBI functionality and dashboard
This module is a controlled setup and maintenance environment for a UBI project to be executed. It includes, but is not limited 
to the following features:
 User Registration and Authentication:
Secure sign-up and login for beneficiaries with an identity verification processes
Manage beneficiary profiles, including personal details, eligibility status, and payment preferences.
 Data Management:
Centralized database to store information, payment history, and transaction records with privacy measures for 
protection of sensitive data
Data lake and data warehousing sections
Reporting and Analytics:
Tools for generating reports on UBI distribution, expenditure, demographics, psychographics, sociographics,
Analytics dashboard for real-time insights into program effectiveness and reach. This can Interface with Active 
Inference modules and AI algorithms. 
Compliance and Regulatory Features
Mechanisms to ensure adherence to government regulations, eg audit trails, policy inclusion
Hard coded allowances for 2-3 features in Version 0.0
User Support and Communication:
Integrated support channels like AI chatbot, email, FAQs, knowledgebase, etc
Notifications Engine regarding payment status and program changes, etc
Payment Management Module:
Handle payment schedules, amounts, and methods.
Track payment statuses and resolve discrepancies.
 Eligibility Assessment Module:
 Automate the evaluation of beneficiaries’ eligibility based on predefined criteria.
Integrate with external databases for verification (e.g., income, residency).
 Feedback and Survey Module:
Collect feedback from beneficiaries to assess satisfaction and gather insights for improvements.
Conduct surveys to measure the impact of UBI on recipients’ lives.
Integration Module:
APIs for connecting with external systems (e.g., government databases, financial institutions).
Support for blockchain or other technologies for secure transactions.
 1.
 a.
 b.
 2.
 a.
 b.
 3.
 a.
 b.
 4.
 a.
 b.
 5.
 a.
 b.
 6.
 a.
 b.
 7.
 a.
 b.
 8.
 a.
 b.
 9.
 a.
 b.

## Page 10

Administrative Dashboard
A centralized interface for administrators to manage the UBI program.
Tools for monitoring system performance, user activity, and financial metrics.
Module 2 : AI and Active Inference Functionalities
This component leverages AI to optimize UBI implementation and decision-making processes by focusing on baseline 
prediction, parameter validation, and action confirmation. The process is structured as follows:
Baseline and Parameter Validation
Establish baseline predictions about the impact of the specific program.
Validate these predictions through data collection and real-time adjustments.
Continuously monitor key parameters (e.g., economic trends, inflation, demographic changes) to ensure accuracy
2. Action and Confirmation
Implement actions based on validated predictions, such as adjusting UBI disbursement rates or targeting specific 
communities.
Continuously compare expected outcomes with actual results to confirm the efficacy of actions.
Use this feedback loop to make iterative improvements and maintain system robustness.
3. Generating Recommendations
We can then test out policy recommendations
Policy suggestions are kept with their case-based nuances 
Inferences on other learnable aspect of the program
Overall we try to enhance the dashboard by ensuring that predictions are consistently validated, and actions are aligned with 
real-world outcomes, from then, onto suggestions to manage the program.
 10.
 a.
 b.
 1.
 •
 •
 •
 •
 •
 •
 •
 •
 •

## Page 11

Comparing AuBI Variants
Here we explore two variant deployment archetypes of AuBI: 
Baseline-Oriented Predictive Systems (BOPS) and Generative 
Predictive Integration (GPI).
⁠
Example Specification A: Baseline-Oriented Predictive System (BOPS)
The proposed system integrates surface-level predictive analytics into the design of income distribution or social support trials. 
The predictive layer is built primarily for low-friction insight generation—tracking user interaction trends, outcome alignment, 
and the distribution of optional participant-reported goals. No complex modeling is assumed in the initial rollout; rather, the 
system begins with observational heuristics and a simple reporting scheme (such as 1–5 scales, keyword tagging, or opt-in 
activity logs).
This design prioritizes two outcomes: (1) creating a robust participation index that helps signal system accessibility and 
emotional resonance, and (2) offering program designers a “soft map” of where interventions are thriving or struggling across 
time or region. By modeling participation as both an engagement and insight metric, even surface-level reporting enables 
gradual tuning of delivery methods. As more data accumulates, predictive models may optionally evolve to help shape program 
adaptations—such as alerting facilitators to localized drops in engagement or surfacing correlation patterns between certain 
self-set goals and longer-term outcome success.
Example Specification B: General Predictive Integration (GPI)
This system design outlines a lightweight approach for integrating predictive tooling into Universal Basic Income (UBI) or direct-
aid schemes. The primary function of the predictive layer is to enhance participation feedback, improve structural reporting, 
and provide adaptive signals for future policy refinement. Instead of enforcing behavior, the system leverages anonymized, opt-
in reporting and pattern inference to observe correlations between engagement, environmental conditions, and outcome 
metrics (such as spending utilization, stability, or well-being proxies).
By adopting a “model-light” predictive approach, participation itself becomes a source of valuable feedback. Users may rate 
their experience, describe challenges, or optionally link their use of funds to goals. Over time, these inputs feed into a rolling 
model of engagement predictors—allowing for early detection of friction points (like access issues or mismatch in aid timing) 
and surfacing hidden promotive factors (like peer influence or seasonal variability). These feedback loops can help 
administrators visualize shifts in real-world efficacy and participant sentiment in a non-invasive, continuously updating way.
GPI could significantly enhance UBI models by combining predictive modeling with generative adaptation. While not yet widely 
applied to economic policy, this framework offers several advantages for UBI implementation:
Enhanced Predictive Capacity
Standard UBI models often rely on static economic projections. GPI would continuously integrate real-time data to generate 
dynamic predictions about individualized impact forecasting, where they predict how specific demographic groups will

## Page 12

respond to AuBI, allowing for more tailored support structures. The come the economic ripple effects where by modeling 
cascading impacts through local economies with greater precision, one can further estimate how quickly different aspects of 
the economy will respond to the AuBI introduction.
Adaptive Implementation
GPI further enables AuBI programs to become self-modifying systems, with responsive payment calibration that automatically 
adjusts AuBI amounts based on changing economic conditions (e.g., increasing during price inflation periods). One can expect 
geographic optimization in identifying areas where AuBI produces the strongest positive multiplier effects and potentially 
targets additional resources there. This could help with complementary policy generation too, where the system could identify 
and suggest supplementary policies when standard UBI alone is insufficient for certain outcomes.
Integration With Other Systems
GPI would facilitate stronger connections between UBI and adjacent systems, some examples of this could include systems like 
healthcare integration (predicting and responding to how UBI affects healthcare utilization and outcomes), education system 
alignment (adapting educational offerings based on how UBI influences career choices and skill development), housing 
market responsiveness (generating early warnings about potential housing inflation and triggering preventative measures).
Researchers are encouraged to choose their ActInf model of preference, layer it with their economic systems of choice and run 
RCTs before finalizing their chosen model. 
GPI Data model
Below is an example schema of the data, system, and process model for a GPI system. 
Example data schema for GPI system (what information the system could utilize)
GPI System model

## Page 13

Example GPI system model 
GPI Process Model

## Page 14

Example process model, centered around operations involved in a participant submitting feedback
Simulated Application
In a city-level implementation, a GPI-enhanced AuBI might:
Begin with standard payments to all residents (standard UBI)
Continuously analyze spending patterns, employment changes, and wellbeing metrics
Generate predictions about emerging needs in specific neighborhoods
Automatically adjust payment timing or amounts for different groups based on observed outcomes (conversion to AuBI)
Identify complementary services needed in specific areas (job training, childcare, etc.)
Create feedback loops that allow the system to become increasingly accurate in its predictions
This approach transforms UBI from a static safety net into an intelligent, responsive system that evolves alongside the 
community it serves, potentially delivering significantly improved outcomes with the same financial investment.
A Comparison of Approaches:
Primary Focus
Maintaining consistent economic floor
System-wide optimization & adaptation
Aspect
BOPS (Baseline-Oriented Predictive SystemGPI (Generative Predictive Integration)
Comparing BOPS and GPI
 •
 •
 •
 •
 •
 •

## Page 15

Prediction Use
Ensure baseline needs met
Generate novel interventions & 
configurations
Aim
Stability & predictability
Dynamic responsiveness & emergent 
outcomes
Adjustments
Threshold based around preset baselines
Continuous multivariate without fixed
Data Utilization
Verifies baseline maintenance 
(poverty line checks)
Identifies patterns & explores 
system configurations
Adjustment Style
Simple threshold triggers 
(inflation > X%)
Complex multi-parameter changes
Learning Capacity
Improves baseline prediction 
accuracy
Evolves understanding of 
economic dynamics
Payment Structure
Fixed payments based on 
local COL
Variable payments across 
neighborhoods
Success Metrics
Poverty reduction statistics
Social mobility, resilience, 
ecosystem health
Resource Allocation
Periodic inflation 
adjustments
Dynamic shifts between payments 
& services
System Focus
Essential goods access 
monitoring
Network effect analysis between 
economic actors
Short-Term
Faster deployment with existing 
infrastructure
N/A (long-term focus)
Long-Term
Predictable budgeting
Better resource allocation & 
consequence mitigation
Implementation 
Speed
Quick rollout needed
Sophisticated 
implementation 
timeline exists
Category
BOPS Implementation
GPI Implementation
Implementation Featu BOPS Approach
GPI Approach
Efficiency Type
BOPS Advantages
GPI Advantages
Factor
BOPS Preferred When GPI Preferred When
Operational Comparison
Implementational Comparison
Efficiency Analysis
Contextual Suitability

## Page 16

The core distinction remains: BOPS uses prediction to maintain static economic security targets, while GPI employs prediction 
to dynamically optimize welfare across evolving systems. 
Hybrid Approach
For a real-world implementation, a staged hybrid approach might be most efficient, because why not?! That’s the whole point of 
including modular design and Active Inference. It could look as follows: 
Begin with a BOPS framework to establish the program quickly and reliably - BOPs x UBI
Build GPI capabilities in parallel, focusing initially on data collection - GPI x UBI
Gradually introduce adaptive elements as the system matures - UBI >> AuBI
Transition to a more fully generative approach over time - AuBI conversion complete
Starting with a BOPS foundation would provide immediate benefits while the more sophisticated GPI infrastructure develops. 
Any of the city's existing digital infrastructure and any strong university partnerships that can be fostered, could support a 
relatively quick transition to more generative approaches.
The most efficient model isn't necessarily one or the other, but rather the right sequence of approaches that balances 
immediate impact with long-term optimization.
Infrastructure
Limited tech 
capabilities
Strong data 
infrastructure 
available
Political Environment
Simple explanations 
required
Innovation-friendly 
climate
Budget Constraints
Strict predictable 
limits
Flexible funding for 
complex challenges
 1.
 2.
 3.
 4.

## Page 17

AuBI Architecture Specification
This specification section provides an initial, technical specification for a decentralized platform capable of designing, 
deploying, and operating an AuBI-type system, as described in previous sections.
System Overview 
Adaptive Basic Income (AuBI) system overview
Core Design Principles
Modularity: Each UBI initiative operates independently while sharing core infrastructure.
Adaptability: Active Inference enables continuous learning and policy optimization.
Transparency: All transactions and decisions are auditable on the blockchain.
Resilience: Decentralized architecture prevents single points of failure.
Privacy: Zero-knowledge proofs and decentralized identity protect participant data.
Scalability: Edge computing and hierarchical consensus enable global deployment.
Architectural Layers
1. User Interface Layer (UX)
Purpose: Provides multiple access points for different user types and technical capabilities.
Components:
Web Portal: Full-featured dashboard for administrators and participants.
Mobile Application: Native iOS/Android apps with offline capability.
API Gateway: RESTful and GraphQL endpoints for third-party integrations.
SMS/USSD Gateway: Basic feature phone access for low-connectivity regions.
Voice Interface: AI-powered voice commands for accessibility.
Key Features:
Multi-language support with real-time translation.
 1.
 2.
 3.
 4.
 5.
 6.
 •
 •
 •
 •
 •
 •

## Page 18

Progressive Web App (PWA) functionality for low-bandwidth areas.
Biometric authentication integration.
Offline transaction queuing with sync capabilities.
2. Application Services Layer
Purpose: Core business logic and service orchestration.
Components:
UBI Initiative Manager: Handles multiple concurrent programs.
Municipal UBI (city-level programs).
Community UBI (local token economies).
Carbon UBI (sustainability-linked payments).
Global UBI DAO (cross-border universal programs).
Identity Verification Service: Multi-factor identity confirmation.
Payment Processing Service: Multi-currency transaction handling.
Governance Module: Decentralized decision-making tools.
Inter-Service Communication:
Event-driven architecture using message queues.
Service mesh for secure inter-service communication.
Circuit breaker patterns for fault tolerance.
3. AI/LLM + Active Inference Layer
Purpose: Intelligent optimization with adaptive learning.
AI Components:
Predictive Models: Economic impact forecasting using time-series analysis.
Behavioral Analytics: Machine learning for spending pattern recognition.
Fraud Detection: Anomaly detection using unsupervised learning.
Personalization Engine: Individual-level optimization algorithms.
Active Inference Engine:
Generative Models: Probabilistic world models for each UBI initiative.
Policy Selection: Expected free energy minimization for optimal actions.
Belief Updating: Continuous model refinement based on outcomes.
Exploration-Exploitation Balance: Information-gathering vs. goal-directed behavior.
Integration Points:
Real-time data ingestion from all system layers.
Policy recommendation pipeline to governance modules.
Automated parameter adjustment within predefined bounds.
4. Decentralized Infrastructure Layer
 •
 •
 •
 •
 ◦
 ◦
 ◦
 ◦
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •

## Page 19

Purpose: Trustless, resilient foundation for all operations.
Blockchain Network:
Consensus Mechanism: Proof-of-Stake with identity verification.
Transaction Processing: High-throughput with sub-second finality.
Interoperability: Cross-chain bridges for multi-blockchain deployment.
Smart Contracts:
Payment Contracts: Automated disbursement logic.
Governance Contracts: Voting and proposal management.
Identity Contracts: Decentralized identity verification.
Distributed Storage:
IPFS Integration: Content-addressed storage for documents.
Encrypted Data Lakes: Privacy-preserving analytics storage.
Redundancy: Geographic distribution across multiple nodes.
Decentralized Identity (DID):
Self-Sovereign Identity: User-controlled identity management.
Verifiable Credentials: Cryptographically-signed attestations.
Zero-Knowledge Proofs: Privacy-preserving identity verification.
Tip: Think beyond existing giants for cloud storage. Think validator networks with decentralized redundancy, colocation and 
more, so that hostile governments and private corps can’t harvest data or snoop into your cloud dockers, or worse, outright 
confiscate them. 
5. Data Layer
Purpose: Secure, privacy-preserving data management.
Components:
Participant Database: Encrypted personal information storage.
Transaction History: Immutable payment records.
AI Model Storage: Versioned machine learning models.
Economic Indicators: External data feeds and market data.
Analytics Warehouse: Privacy-preserving aggregate analytics.
Data Security:
End-to-end encryption for all sensitive data.
Differential privacy for statistical analysis.
Data minimization and automatic expiration policies.
Tip: Think of blockchain protocols to leave anonymized or stuffed, locked tokens to ensure your data has copies and can be 
retrieved or protected, in the unfortunate event of malicious attacks - known and unknown.
Key Technical Innovations
1. Multi-Initiative Coordination
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •

## Page 20

The platform enables multiple UBI programs to operate simultaneously while preventing double-spending and ensuring fair 
resource allocation. Each initiative maintains its own parameters while benefiting from shared infrastructure and cross-program 
learning. This is where the aforementioned B2B2C format comes in. Platforms that are currently B2B2C involve Amazon, Etsy, 
Temu, etc..
2. Active Inference Integration
Unlike traditional AI systems that optimize for predefined objectives, the Active Inference engine continuously updates its 
understanding of what constitutes optimal outcomes based on real-world feedback, enabling truly adaptive economic policy.
3. Privacy-Preserving Analytics
The system employs advanced cryptographic techniques including homomorphic encryption and secure multi-party 
computation to enable powerful analytics while protecting individual privacy.
4. Economic Modeling
Sophisticated agent-based models simulate the economic effects of different UBI parameters, enabling evidence-based policy 
optimization before real-world implementation.
Security Architecture
Identity and Access Management
Multi-factor authentication with biometric options.
Role-based access control with least-privilege principles.
Regular security audits and penetration testing.
Data Protection
Encryption at rest and in transit.
Key rotation and hardware security modules.
Privacy by design principles throughout.
Network Security
DDoS protection and rate limiting.
Secure communication protocols.
Intrusion detection and response systems.
Scalability Considerations
Horizontal Scaling
Microservices architecture enables independent scaling.
Container orchestration with Kubernetes.
Auto-scaling based on demand patterns.
Performance Optimization
Edge computing for reduced latency.
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •

## Page 21

Content delivery networks for global distribution.
Database sharding and read replicas.
Governance Model
Technical Governance
Open-source development with community contributions.
Technical advisory board for architectural decisions.
Formal specification and testing procedures.
Economic Governance
Decentralized autonomous organization (DAO) structure.
Token-based voting for major policy decisions.
Transparent budget allocation and spending.
Risk Assessment and Mitigation
Technical Risks
Blockchain congestion: Layer-2 solutions and sidechains.
AI bias: Continuous monitoring and algorithmic auditing, or correction, as needed
Security vulnerabilities: Regular audits and bug bounty programs, community ethical hacker invites, as needed, if the 
project is largely pro bono
Economic Risks
Inflation: Dynamic adjustment algorithms and economic monitoring, even speculative shrinkflation projections, as needed.
Fraud: Multi-layered detection and prevention systems, get a pro bono consult from red-teams if needed.
Funding sustainability: Diversified funding sources and reserves. Don’t rely on a single private, govt or decentralized 
source. 
Regulatory Risks
Compliance: Built-in regulatory reporting and audit trails. Keep things compliant so experiments and RCTs can be 
replicated in the future.
Cross-jurisdiction operations: Legal framework development. The experts are worth the investment here, especially in an 
increasingly complex world. 
Data protection: Privacy by design and GDPR compliance. You should not need a law to protect your data. It has been 
given to you with trust. Make yourself worth of its collection and handling. 
User Experience and System Interactions
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •

## Page 22

Example Data architecture

## Page 23

Example Dashboard

## Page 24

Conclusion
This architecture provides a robust, scalable, and adaptive foundation for implementing Universal Basic Income at scale, 
thereby living up to its AuBI moniker. By combining efficiency-driven LLMs, blockchain technology, and Active Inference theory, 
the platform can evolve and improve over time while maintaining security, privacy, and decentralization principles.
This is our version of a potential model. Feel free to make it your own. Ask extra questions, add extra widgets, remove that 
which you don’t need - sacrifice making it perfect, for getting it done.

## Page 25

Discussion
The exploration of AuBI, in this paper allows us to envision it as an innovative system that merges AI, decentralized 
infrastructure, and active inference theory to create a more adaptive and personalized approach to resource distribution 
(social, public, private, economic, causal, et al).
At its core, this system is conceptualized to continuously learn and predict individual and community needs based on patterns 
of resource utilization and outcomes, via LLMs. Rather than applying a one-size-fits-all solution, the system would function as a 
predictive engine that constantly updates its understanding of what resources are needed where and when. This could change 
monthly payment denominations suited to the dynamic results from the active inference, for example. 
The decentralized infrastructure would ensure that decision-making and resource allocation aren't controlled by a single entity 
or vulnerable to single points of failure. This could involve blockchain or similar distributed ledger technologies to maintain 
transparency, security, and trust while reducing administrative overhead.
Expected guidance through Active Inference and cognitive modeling includes, but isn’t limited to:
Modeling each participant's needs and preferences to form collective patterns for income deployment
Predicting resource requirements before they become critical, allowing for better budgetary allocation
Adapting allocations based on observed outcomes and timing them as needed
The system would essentially function as a self-organizing network that continuously learns from interactions, adjusts resource 
flows based on changing circumstances, and maintains equilibrium through predictive modeling rather than reactive policies.
This approach could potentially address common criticisms of standard UBI distribution systems by being more efficient, 
responsive to individual needs, resistant to corruption, and capable of evolving as societal needs change.
Many specifications would be needed for (positive/beneficial) regional application, we have merely provided some ideas for 
templates, schema, and patterns .  
Potential Deployment Example with their own adaptations
Several recent papers have mentioned the need for continuity, inference, and predictive support (described in 
. 
Supplement: Additional Links and Resources
To characterize an example deployment, in 
 we do so by proposing a 
packaging framework built around micro studies (using Bayesian trial techniques as per e.g. 
). These small-
scale pilots not only test AuBI’s effects but also create participatory environments where self-reporting and community 
engagement enhance both outcome tracking and user agency. The assumption here is that predictive frameworks work better 
when supported by ongoing, human-centered input, and that inference itself requires continuity—not just of income, but of 
story.
Supplement: An Indonesian Thought Experiment
Parr et al. 2024
To make this actionable, we propose deploying targeted micro-UBI studies, such as an Indonesian pilot for encouraging 
language oriented self study, where cash support is given with an encouragement to spend a small % on self reported monthly 
study, the amount of which is optional, and without penalty. Or a rotation-based village AuBI where a few families receive 
support at a time, contributing light observational data in return. These designs highlight how UBI, when coupled with soft 
participation, builds not only economic value but also trust, verification, and shared purpose.
Bonus: Questions to ask oneself before conceptualizing a custom AuBI Initiative
Ethical and Philosophical Foundations
What constitutes a "basic" income in different geographical and social contexts? - Study local trends
How do we balance universal standardization with localized needs? - Think Global, Act Local
 •
 •
 •
 •
 •

## Page 26

What values should guide the system's decision-making processes? - Value align
Should the system aim for equality (same for all) or equity (proportional to need)? - Which one is missing?
What is the primary objective of this initiative at this place and time? - What are you solving for?
AI/LLM Implementation Choices
How can we ensure the AI doesn't perpetuate existing biases in resource allocation? - training the data
What data should be collected to inform the system, and what are the privacy implications? - data sovereignty 
How transparent should the AI's decision-making processes be to recipients? - what to anonymize?
What oversight mechanisms should exist for the AI component? - after all, LLM models need ActInf thinking too
How can we design the system to learn from outcomes while respecting individual autonomy? - Is there an LLM prompt 
specific to address this problem that can be coded in?
Active Inference Applications
How should the system balance predicted needs versus expressed preferences?
What feedback mechanisms will help the system update its models effectively? - these set your primary ActInf parameters
How can we incorporate both individual and community-level predictions? - could splitting the Data Lake help?
What metrics should indicate "surprise" that requires system adaptation? - where does the dynamicity rest the most?
Practical Applicability
What mechanisms prevent gaming or exploitation of the system? - fraud prevention
How should the transition from current welfare systems be managed? - socio-public considerations
What happens when predictions fail or resources are constrained? - budgetary constraints
How can we design the system to be resilient to economic shocks? - global pattern recognition
Governance and Participation
Who has input into the system's parameters and how often are they reviewed? - who is the tech governing counsel?
How much agency should recipients have in how the system evolves? - how much is hard-coded and how much is soft-
coded, and therefore, malleable?
What appeal processes should exist when the system makes mistakes? - how quickly can you undo or repeal something
How do we ensure the system remains aligned with evolving societal values? - who’s responsible for keeping up with the 
social times. 
Long-term Considerations
How might the system affect work incentives and economic productivity? - how does this change the economy
What mechanisms should prevent dependency while ensuring needs are met? - are there aspects that might cripple the 
economy
How will the system adapt to technological and economic transformation? - are you using a fluid enough programming 
language that can evolve and update?
How can a experiment/pilot project ensure longevity as this being included in all our future CivicTech modules?
These questions highlight the complexity of merging AuBI policy with advanced AI and active inference principles, pointing to 
the need for thoughtful design that centers human welfare while leveraging technological capabilities.
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •

## Page 27

Next/Possible Steps
Develop the AuBI v0.1 toolkit modules covering UBI administration, AI-driven analytics, automated payments, and cognitive 
modeling.
Deploy small-scale, culturally tailored “micro-UBI” studies to validate behavioral models and engagement strategies. Small 
micro-studies are important to test efficacy of pilot concepts. 
Conduct a structured meta-analysis of existing UBI trials to identify intervention designs, outcomes, and research gaps. 
Form a practitioner network to share protocols, anonymized data and best practices for iterative refinement. Gate the Data 
Lake to only those you trust. 
Host technical workshops and training programs to onboard implementers and build a community of practice.
Expand the AuBI and make it Your own:
Are you a government, NGO, private body trying to experiment with UBI and Basic Income as concepts for your communities? 
You’re welcome to reach out to our community and team of experts on the topics of Active Inference, the Free Energy Principle, 
its use in the new concept of AuBI, and more, to add depth to your projects. 
For consulting inquiries, clarifications, and on-boarding any experts to your initiative, write to 
. 
blanket@activeinference.institute
 •
 •
 •
 •
 •

## Page 28

Supplement: An Indonesian Thought Experiment
Here we’ve taken the liberty to add some conceptualized thought experiments on Micro-Studies from an AuBI perspective and 
what they could look like in post-colonial countries, with a view to benefiting the existing frames of society.
They have been conceptualized by an Indonesian native, as an attempt to see what Hybrid-Adaptive Basic Income could look 
like in a country with a deeply depreciated currency, amongst other different socio-cultural norms. 
A Quick Indonesian Examples Look:
Dana Bahasa (Language Fund)-giving children disposable funds to write reports on language learning (any casual)
Guru Honorer (Supplementing Supplemental Teaching Staff)- Indonesia has a semi unfortunate sector of teaching staff, 
which is paid less than $100 per month on average (because these are subsidized by the state budget), a decades old 
practice stemming from a past that needed emergency teachers in underdeveloped regions. This type of AuBI would seek 
to be proactive pre-government initiative to supplement and help, to also bring light onto how tragic this neglected (un-
adjusted) aspect of national reform.
Rural Cooperative UBI (Gotong Rotasi)- hypothetical village level adoption example, to subsidize / fund a coordinator that 
shares some village tools or shareable technological (but expensive) implements, it is suggested to be deployed in a setting 
where it is more about introduction and helping kickstarter / cooperative spirit, in this case , some preventive measure for 
abuse / bad habits should be set, such as short limits of borrowing time, priority for learners, and reciprocal sharing. overall, 
hope to be more of a bare necessities/ bare minimum supporting program.
Pasar (Market) Moms UBI (research / data gathering oriented), a more study & basic type of UBI that just seeks to 
document how usual spending is made for mothers of a family, comes in to supplement disposable income & document the 
spending habits / what might be troubling in general for the area, comes and goes readily in small study.
Diving in a bit more: 
Example #1: Dana Bahasa – Micro UBI for Language Learning
Possible Target: Youth/Students (age 12–22)
Delivery:
Amount: $10/month
Requirement: Spend $5 on any language-learning related activity
Reporting: Light, optional (self-report via message or form)
Purpose:
To explore how small unconditional cash transfers (UBI) can motivate micro-efforts toward education, especially language 
learning.
Using aUBI as a tool of development-of-choice (language in this case), with the lightest touch.
Projected Metrics (for 100 mini studies):
Recipients: 10,000
Total Budget: $1,000,000
Study Period: 10 months
Data Collected:
Language proficiency baseline & final
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 ◦

## Page 29

Self-reported satisfaction
Spending categories (books, apps, tutors, etc.)
Promoters & inhibitors of success modeled
Expected Benefits:
70% engagement in voluntary followup
90% reporting continuity
50% expressing career/educational aspirations increase
 N %  increase in Language Test , over the three period
Identification of key inhibitors (e.g., lack of time, access, peer support)
Cultural alignment through fun, low-pressure engagement 
Summary
In this pilot, students receive $10 monthly and are encouraged (but not required) to spend at least $5 on language-learning 
activities. The concept is simple: low-stakes support for micro-goals, framed in a fun, casual tone. Participants self-report how 
they used the funds, and their language skill progress is tested at the start and end.
The approach aims to build routine engagement without behavioral pressure—making support feel like a gift, not a task. Across 
10,000 participants, we estimate a 70% volunteering rate and 50% reported positive shifts in motivation. Spending data and 
self-reports are used to infer patterns of success or drop-off, helping us model key behavioral promoters and blockers over 
time.
Rationale:
A light and culturally resonant design taps into Indonesia’s communal and low-conflict values. Predictive modeling layered onto 
such engagement reveals what encourages or inhibits progress—with no coercion needed.
Example #2: Guru Honorer – UBI Support for Informal Teaching Staff
Possible Target: Informal or contract teachers (Guru Honorer) in rural or underserved areas
Delivery:
Amount: $15/month
Requirement: Light weekly self-check-in (message or app)
Reporting: Optional, reflective on activities or challenges in teaching
Background:
Guru Honorer is a state-sponsored teaching staff member, a concept that came from the post-colonial emergency staffing 
program, but one that the government ended up continuing to rely on to this day and age. With every administration, they keep 
denying/postponing their acknowledgement as a “formal teaching staff”, in order to not bloat the wages / the staffing budget 
and stiff them on benefits too. They earn typically less than $100 USD a month, and their current numbers come to around 1.3 
million people.
Purpose:
To provide modest income support to long-overlooked informal educators (Guru Honorer), and observe its effects on 
motivation, well-being, and continued teaching engagement.
Using AuBI as a tool of pre-emptive problem highlighting, and likewise, problem solving tool.
Projected Metrics (for 100 participants):
Recipients: 100 informal teachers
 ◦
 ◦
 ◦
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •

## Page 30

Total Budget: $15,000
Study Period: 10 months
Data Collected:
Self-reported teaching activities
Motivation and well-being reflections
Time use and financial stability reports
Narrative data on challenges and creativity in teaching
Expected Benefits:
75% sustain or improve informal teaching activity
60% report improved emotional resilience or motivation
50% reflect positively on time use or household dynamics
Evidence of behavioral continuity under low-income stability
Summary:
This micro-UBI study supports a neglected population of informal teachers with $15 monthly.
While formally presented as a study, the intervention functions more as pre-emptive relief and social recognition. Through 
narrative data and self-check-ins, the pilot documents the impact of minimal income on a persistently marginalized professional 
group.
Rationale:
UBI can act not just as a research instrument, but a moral acknowledgment. This initiative highlights the lived realities of 
underpaid public service workers and suggests pathways for sustainable aid without bureaucratic complexity.
Example #3: Gotong Rotasi – Rotational Rural UBI for Community Tools and Schooling
Possible Target: Rural farming families
Delivery:
Amount: $30/month per family
Requirement: Maintain shared family logbook
Reporting: Weekly entries (spending, education, collaboration stories)
Purpose:
To explore how staggered, rotating UBI supports rural cooperation, particularly in schooling, farming, and tool-sharing.
Using aUBI as a tool of experimentation & habit-building scaffold.
Projected Metrics (for 10 families):
Recipients: 10 families (rotated monthly)
Total Budget: $3,600
Study Period: 12 months
Data Collected:
Family narratives on changes in decision-making
Tool-sharing frequency and collaborations
Education-related expenditures
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •

## Page 31

Peer-to-peer support dynamics
Expected Benefits:
90% compliance with logbook reporting
65% report improved schooling access or shared farming resources
Identification of key enablers of cooperation
Modeling of low-friction, culturally familiar redistribution methods
Summary:
In this pilot, rural families receive UBI in a rotational pattern, fostering micro-observation of behavioral shifts over time. While 
framed around household spending, the deeper intent is to catalyze and document traditional cooperative behaviors—
especially in tool-sharing and education.
Participation requires keeping a weekly logbook, which blends economic notes with storytelling. These accounts will help trace 
how even short-lived support shapes rural networks of exchange, trust, and adaptation.
Rationale:
By aligning with gotong royong (mutual aid) values, this design lets UBI reinforce—not replace—existing cultural mechanisms. 
Such framing permits both ethical delivery and observational research on informal economies and adaptive survival strategies.
Example #4: Pasar Moms – Emotional Well-being through Free-Spend UBI
Possible Target: Rural/village housewives or mothers
Delivery:
Amount: $20/month
Requirement: None
Reporting: Optional weekly reflection via voice or message
Purpose:
To study how unconditional, minimally directed cash transfers influence spending related to : emotional well-being, household 
stability, and perceived financial stress.
Using aUBI as a tool of generic sense-making, scouting, and confirmation.
Projected Metrics (for 100 participants):
Recipients: 100 mothers
Total Budget: $20,000
Study Period: 10 months
Data Collected:
Weekly reflections on emotional state
Themes such as food security, debt, childcare relief
Emergent narratives of empowerment or stress reduction
Seasonal variations in well-being linked to cash flow
Expected Benefits:
85% engage in voluntary weekly check-ins
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •

## Page 32

Insights into commonly unspoken worries and coping strategies
Data pool to enrich understanding of household stress indicators
Cultural visibility into emotional health and economic autonomy
Summary:
This initiative provides mothers with no-strings-attached monthly support, emphasizing emotional rather than economic 
metrics. Participants reflect—through voice or message—on “what they didn’t worry about this week,” yielding insight into how 
micro-stability affects daily life.
Rather than enforce spending targets, this pilot captures what happens in the absence of direction. The narratives help shape 
an understanding of how emotional and financial pressures co-evolve in family life.
(also acts as a more generic sense-making / habit establishing study)
Rationale:
On top of accounting for personal remarks of emotional relief as a basis of sense-making (or would-be-reference to data), 
we also operate / pitch this version as a routine for confirming habits & preferences.
Tip: Localize: This supplement has been conceptualized by our Indonesian contributor who lives and thrives in that 
economy. We cannot stress the need to localize these experiments enough - please do! 
 •
 •
 •

## Page 33

Supplement: Thought Experiments
Now that we’ve introduced AuBI as a framework, we thought we’d litter the path with nuggets of related ideas to chew on. This 
Master rabbit hole is captioned Thought Experiments (hereon referred to as TEs) - a supplemental section full of introductory 
brainwaves that you can iterate on further. 
The objective of this section is to look at standard UBI as a dynamic spectrum. From here on, feel free to fork any of these 
ideas, generate newer ones from them or spin them off completely - open playground of free energy, all principled puns 
intended. 
TE #1: Society as a Collective Prediction System:
A social reinterpretation of standard UBI through active inference lens could look 
like viewing society as a collective prediction machine that minimizes free energy.
From an ActInf perspective, society functions as a hierarchical generative model 
where institutions form higher-level priors that constrain individual expectations. 
Social policies can act as collective predictions about citizen needs and behaviors, 
which make economic interventions serve as actions that attempt to make societal 
outcomes match these predictions. Win-win.
TE #2: UBI as a Free Energy Minimization Mechanism
Under this framework, UBI could use collective action to minimize societal free 
energy (uncertainty/surprise) through various mechanisms, thereby reducing 
surprise at individual, community, institutions and systemic levels. Think constant 
feedback loops, townhalls and tie ins with government to monitor the avenues of 
release of Free Energy. Further think FEP in local economic stabilization.

## Page 34

TE #3: Bayesian Community Income Floors
When communities implement local income guarantees (community-level UBI), they 
establish predictable consumption baselines that reduce variance in revenue 
forecasts for essential businesses (rice, fuel, healthcare), create persistent 
minimum demand for local goods and services and enable more accurate business 
planning with known consumption floors.
This minimum guaranteed consumption acts as a strong prior in the community's 
generative model, significantly reducing free energy by narrowing the range of 
possible economic states. By reducing information asymmetries, these systems 
allow all economic actors to form better predictions, thereby minimizing surprise.
TE #4: Complementary Tokenized Economies
AuBI on the blockchain could allow local currencies or token systems to operate 
alongside national currency can function as powerful free energy minimization 
tools. They create closed feedback loops within the community, helping local 
economic activity become partially insulated from external volatility through the 
tokenization supplement.
Depreciated currency economies (eg: Turkey, Nigeria, Vietnam, Indonesia) can 
benefit from add digital, CBDC, Bitcoin or similar variants as a shield against socio-
economic collapse.

## Page 35

TE #5: Graduated Basic Income with Choice Architecture
This concept envisions Policy Design that implements a multi-tier local income floor 
with graduated benefits, thereby allowing recipients to choose different distribution 
schedules (weekly, monthly, quarterly), optional earmarking features for housing, 
education, or healthcare.
The ActInf elements would create multiple prediction streams that allow the system 
to learn individual preference patterns through revealed choices. Timely data 
ensures active adaption.
TE #6: Community Information Commons
Subject to local data privacy laws in the region, this concept envisions policy 
design that develops a local digital platform sharing anonymized economic data. 
The Active Inference element can create a shared predictive model that all local 
actors can access and contribute to. Needless to say this data would be 
anonymized and safeguarded with guarantees given by the warehousing authority 
- a great concept the pilot in countries like Finland, Norway, Singapore, etc where 
populations are small enough, governments are rich enough and laws are upheld 
enough for the design to make an actual difference. This could evolve into a 
Countercyclical Community Fund eventually, where the fund automatically adjusts 
support levels based on local economic indicators. It releases additional resources 
when leading indicators suggest economic contraction and likely funds through a 
percentage of local business revenues during growth periods.

## Page 36

TE #7:  Precision-Weighted Intervention System
This policy design envisions deploying multiple small-scale interventions 
simultaneously rather than single largescale policies. It allocates resources 
dynamically based on which interventions show strongest evidence of 
effectiveness - maintaining minimum support for all approaches while scaling those 
with best outcomes. For this it explicitly treats policy as prediction testing and 
assigns "precision weights" to different approaches based on evidence. A balance 
of exploration (finding better interventions) with exploitation (using what works).
TE #8: Updating Models of Human Behaviour 🧠
We close things out with leaving you to think of AuBI x AI x ActInf as helping update models of human behaviour through 
economic dynamics. This approach transforms institutions from static policy enforcers into adaptive, predictive systems. From 
precision-weighted evidence accumulation to heirarchical model refinement, active policy experimentation is the future of 
Society as we know it. 
These will require an open mind, reduction in policy entrenchment, cross contextual learning, and multiscale feedback loops. 
Difficult, yes, complicated, yes, impossible, No.
💮We hope these brainwaves will help you design pilots that increase epistemic humility and build more intelligent 
institutions. By re-conceptualizing themselves as prediction machines engaged in active inference, social institutions can 
develop increasingly accurate models of human behavior and economic dynamics - for the greater good. 💮

## Page 37

Supplement: Additional Links and Resources
Here’s a running Registry of papers, articles, experiments, prototypes that cuts across global parameters and nation state 
borders. Feel free to sift through:
Basic Income Training 2025 (BIEN).
⁠
https://basicincome.org/news/2025/04/basic-income-training-2025-bit-2025/
Unconditional Basic Income – UBI4ALL
https://www.ubi4all.org/post/unconditional-basic-income-ubi-implementation-and-experiments-insights-from-pilot-
programs-and-case-studies
UBI Experiments Around the World – Thorsten Meyer
⁠
https://thorstenmeyerai.com/universal-basic-income/ubi-experiments-2/
A Sustainable Global UBI – Al Jazeera Opinion
⁠
https://www.aljazeera.com/opinions/2024/10/15/a-sustainable-global-universal-basic-income-can-be-done-here-is-how
Basic Income Today – UBI News Hub
⁠
https://basicincometoday.com/
9 Successful UBI Pilot Programs - UBI Advocates
⁠
https://ubiadvocates.org/9-successful-ubi-pilot-programs-that-will-change-your-views-on-free-money/
Rethinking UBI & SDGs – Basic Income News
https://basicincome.org/news/2024/11/rethinking-universal-basic-income-economic-productivity-quality-of-life-and-the-
sustainable-development-goals/
The Prospects of UBI in Indonesia – Indonesia Development Forum
https://indonesiadevelopmentforum.com/en/2022/knowledge-center/detail/12093-12093-the-prospects-of-universal-
basic-income-in-indonesia
UBI & AI: Perspectives from Tech Leaders – Business Insider
⁠
https://www.businessinsider.com/universal-basic-income-ai
Ireland Artists’ UBI Pilot Results – Business Insider
⁠
https://www.businessinsider.com/ireland-artists-basic-income-pilot-results-2025-6
Universal Basic Income In The Developing World (including nobel laurates) 
⁠
https://www.nber.org/system/files/working_papers/w25598/w25598.pdf
A Mathematical Model of Universal Basic Income and Its Numerical Simulations
https://www.researchgate.net/publication/356163548_A_Mathematical_Model_of_Universal_Basic_Income_and_Its_Numeric
al_Simulations
A mix of Crypto and Country-specific Pilots: 
Crypto: 
An Ethereum project: 
 
https://ubi.eth.limo/
Impact Markets and their idea of Unconditional Basic Income: 
 
https://www.impactmarket.com/ubi
Crypto based attempt with a one-time paid model: 
 
https://www.myubicoin.com/
Circles UBI: 
 
https://handbook.joincircles.net/docs/developers/whitepaper/
Circles Indonesia: 
 
https://www.circlesubi.id/
Proof of Humanity, a Spanish crypto project: 
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •
 •

## Page 38

Ctrl + F for UBI if needed, but the overall 
article articulates DemocracyOS and other interesting concepts too
https://greenash.net.au/thoughts/2022/04/on-the-proof-of-humanity-project/
⁠
https://www.proofofhumanity.org/
⁠
https://gov.proofofhumanity.id/c/universal-basic-income/6
 (private project) 
⁠
Local Community Cryptocurrencies with Universal Basic Income
https://arxiv.org/abs/1912.12141
 
⁠
The long-term impact of unconditional cash transfers on psychological wellbeing
https://haushofer.ne.su.se/publications/Haushofer_Shapiro_UCT2_2018.pdf
: Creating Wealth with On-Chain Staking and Fixed-Rate Protocols:  
⁠
Decentralized Basic Income
https://arxiv.org/abs/2107.14312
Regional:
Denver’s Basic Income Project: 
 
https://www.denverbasicincomeproject.org/
A proposition for New Zealand:  
⁠
https://www.top.org.nz/universal-basic-income-policy
 
https://www.basicincomenz.net/faq
University Basic Income Trial Findings - London, UK: 
https://www.london.gov.uk/who-we-are/what-london-assembly-does/questions-mayor/find-an-answer/universal-basic-
income-trial-findings
Proposed UBI Trial, England: 
https://www.theguardian.com/society/2023/jun/04/universal-basic-income-of-1600-pounds-a-month-to-be-trialled-in-
england
Finland’s Basic Income Experiment:  
 
https://ec.europa.eu/social/BlobServlet?docId=20846&langId=en
Ontario Basic Income Pilot Project: 
⁠
https://www.ontario.ca/page/ontario-basic-income-pilot
 ◦
 ◦
 ◦
 •
 •
 •
 •
 •
 ◦
 •
 •
 •
 •


---
*Extraction method: pymupdf*
