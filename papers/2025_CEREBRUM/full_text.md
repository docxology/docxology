# Full Text: CEREBRUM: Case-Enabled Reasoning Engine with Bayesian Representations for Unified Modeling

> Extracted from `2025_CEREBRUM.pdf`

---

## Page 1

Case-Enabled Reasoning Engine with Bayesian
Representations for Unified Modeling (CEREBRUM)
Daniel Ari Friedman
Version 1.0 (2025-04-07)
-.-. . .-. . -... .-. ..- – —... / -.-. .- ... . -....- . -. .- -... .-.. . -.. / .-. . .- ... — -. .. -. –. / . -. –. .. -. . / .– .. - .... /
-... .- -.– . ... .. .- -. / .-. . .–. .-. . ... . -. - .- - .. — -. ... / ..-. — .-. / ..- -. .. ..-. .. . -.. / – — -.. . .-.. .. -. –.
DOI: 10.5281/zenodo.151709081
-.-. . .-. . -... .-. ..- – —... / -.-. .- ... . -....- . -. .- -... .-.. . -.. / .-. . .- ... — -. .. -. –. / . -. –. .. -. . / .– .. - .... /
-... .- -.– . ... .. .- -. / .-. . .–. .-. . ... . -. - .- - .. — -. ... / ..-. — .-. / ..- -. .. ..-. .. . -.. / – — -.. . .-.. .. -. –.
Contents
1
Abstract
3
2
Overview
3
3
Background
3
3.1
Cognitive Systems Modeling . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
3
3.2
Active Inference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
4
3.3
Linguistic Case Systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
4
3.4
Intelligence Case Management Systems . . . . . . . . . . . . . . . . . . . . . . . . . .
5
4
Towards Languages for Generative Modeling
5
5
Conceptual Foundations: The Intersection of Four Domains
5
6
Methods and Materials
7
6.1
Formal Framework Development
. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
6.2
Mathematical Foundation . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
7
7
Core Concept: Cognitive Models as Case-Bearing Entities
7
8
Case Functions in Cognitive Modeling
7
9
A Preliminary Example of a Case-Bearing Model: Homeostatic Thermostat
10
1https://doi.org/10.5281/zenodo.15170908
1

## Page 2

10 Declinability of Active Inference Generative Models
11
10.1 Morphological Transformation of Generative Models . . . . . . . . . . . . . . . . . .
11
10.2 Active Inference Model Declension Example . . . . . . . . . . . . . . . . . . . . . . .
13
11 Model Workflows as Case Transformations
14
12 Category-Theoretic Formalization
14
13 Computational Linguistics, Structural Alignment, and Model Relationships
17
14 Implementation in Intelligence Production
19
15 Active Inference Integration
19
16 Formal Case Calculus
19
17 Cross-Domain Integration Benefits
19
18 Related Work
24
18.1 Cognitive Architectures
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
25
18.2 Category-Theoretic Cognition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
25
18.3 Active Inference Applications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
25
18.4 Linguistic Computing
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
25
19 Practical Applications of Model Declension in Cognitive Ecosystems
25
19.1 Model Pipeline Optimization
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
25
19.2 Computational Resource Optimization . . . . . . . . . . . . . . . . . . . . . . . . . .
26
19.3 Model Ecosystem Adaptability
. . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
26
19.4 Cross-Domain Integration . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
27
19.5 Knowledge Graph Enhancement
. . . . . . . . . . . . . . . . . . . . . . . . . . . . .
27
19.6 Emergent Behaviors in Model Collectives
. . . . . . . . . . . . . . . . . . . . . . . .
28
20 Future Directions
30
21 Conclusion
30
22 Mathematical Appendix
31
22.1 Variational Free Energy and Case Transformations . . . . . . . . . . . . . . . . . . .
31
22.2 Message Passing Rules for Different Cases . . . . . . . . . . . . . . . . . . . . . . . .
32
22.3 Precision Allocation and Resource Optimization
. . . . . . . . . . . . . . . . . . . .
33
22.4 Novel Case Formalizations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
33
23 Discovering and Creating New Linguistic Cases Through CEREBRUM
35
23.1 Emergence of Novel Case Functions . . . . . . . . . . . . . . . . . . . . . . . . . . . .
35
23.2 Speculative Novel Case: The Emergent “Conjunctive” Case . . . . . . . . . . . . . .
36
23.3 Speculative Novel Case: The “Recursive” Case
. . . . . . . . . . . . . . . . . . . . .
36
23.4 Speculative Novel Case: The “Metaphorical” Case
. . . . . . . . . . . . . . . . . . .
36
23.5 Implications of Novel Cases for Computational Cognition
. . . . . . . . . . . . . . .
37
CEREBRUM: Case-Enabled Reasoning Engine with Bayesian Representations for Unified Modeling
2

## Page 3

Daniel Ari Friedman
Active Inference Institute
ORCID: 0000-0001-6232-9096
Email: daniel@activeinference.institute
Version 1.0 (2025-04-07) ~ CC BY-NC-ND 4.0
1
Abstract
This paper introduces Case-Enabled Reasoning Engine with Bayesian Representations for Unified
Modeling (CEREBRUM). CEREBRUM is a synthetic intelligence framework that integrates lin-
guistic case systems with cognitive scientific principles to describe, design, and deploy generative
models in an expressive fashion. By treating models as case-bearing entities that can play multiple
contextual roles (e.g. like declinable nouns), CEREBRUM establishes a formal linguistic-type calcu-
lus for cognitive model use, relationships, and transformations. The CEREBRUM framework uses
structures from category theory and modeling techniques related to the Free Energy Principle, in
describing and utilizing models across contexts. CEREBRUM addresses the growing complexity in
computational and cognitive modeling systems (e.g. generative, decentralized, agentic intelligences),
by providing structured representations of model ecosystems that align with lexical ergonomics, sci-
entific principles, and operational processes.
2
Overview
CEREBRUM implements a comprehensive approach to cognitive systems modeling by applying
linguistic case systems to model management. This framework treats cognitive models as entities
that can exist in different “cases”, as in a morphologically rich language, based on their functional
role within an intelligence production workflow. This enables more structured representation of
model relationships and transformations.
The code to generate this paper, and further open source development from this 1.0 milestone
release, is available at https://github.com/ActiveInferenceInstitute/CEREBRUM .
3
Background
3.1
Cognitive Systems Modeling
Cognitive systems modeling approaches cognition as a complex adaptive system, where cognitive
processes emerge from the dynamic interaction of multiple components across different scales. This
perspective draws from ecological psychology’s emphasis on organism-environment coupling, where
cognitive processes are fundamentally situated in and shaped by their environmental context. The
4E cognition framework (embodied, embedded, enacted, and extended) provides a theoretical foun-
3

## Page 4

dation for understanding how cognitive systems extend beyond individual agents to include envi-
ronmental structures and social interactions. In this view, cognitive models are not merely internal
representations but active participants in a broader cognitive ecosystem, where they adapt and
evolve through interaction with other models and environmental constraints. This systems-level
perspective is particularly relevant for intelligence production, where multiple analytical models
must coordinate their activities while maintaining sensitivity to changing operational contexts and
requirements. The complex adaptive systems approach emphasizes self-organization, emergence,
and adaptation, viewing cognitive processes as distributed across multiple interacting components
that collectively produce intelligent behavior through their coordinated activity (including language
use).
3.2
Active Inference
Active Inference is a first-principles account of perception, learning, and decision-making based on
the Free Energy Principle. In this framework, cognitive systems minimize variational free energy
— bounded surprise, reflecting the difference between an organism’s internal model and its environ-
ment — through perception (updating internal models) and action (changing action and ultimately
sensory inputs). The Active Inference framework formalizes uncertainty in terms of entropy and
precision weighting, enabling dynamic adaptive processes. While many model architectures are
possible, hierarchical message passing is a common implementation that implements predictions
as top-down flows and prediction errors as bottom-up flows, creating a bidirectional inference sys-
tem that iteratively minimizes surprise across model levels. Active Inference treats all cognitive
operations as Bayesian model update, providing a unifying mathematical formalism for predictive
cognition.
3.3
Linguistic Case Systems
Linguistic case systems represent grammatical relationships between words through morphologi-
cal marking. Case systems operate as morphosyntactic interfaces between semantics and syntax,
encoding contextualized relationship types rather than just sequential ordering.
This inherent
relationality makes case systems powerful abstractions for modeling complex dependencies and
transformations between conceptual entities. Cases under consideration here include nominative
(subject), accusative (object), dative (recipient), genitive (possessor), instrumental (tool), locative
(location), and ablative (origin), all serving different functional roles within sentence structures.
Languages implement these differently: nominative-accusative systems distinguish subjects from
objects, while ergative-absolutive systems group intransitive subjects with direct objects. While
English has largely lost its morphological case system, the underlying case relationships still exist
and are expressed through word order and prepositions.
For example, in “The cat chased the
mouse,” the nominative case is marked by position (subject before verb) rather than morphology,
while in “I gave him the book,” the dative case is marked by the preposition “to” (implied) and
word order. This demonstrates that (the semantics/semiosis/pragmatics of) case relationships are
fundamental to language structure, even when not overtly marked morphologically (e.g. expressed
in writing or spoken language).
4

## Page 5

3.4
Intelligence Case Management Systems
Intelligence case management systems organize investigative workflows and analytical processes
in operational contexts. These systems structure information collection, analysis, evaluation, and
dissemination while tracking provenance and relationships between intelligence products. Modern
implementations increasingly must manage complex model ecosystems where analytical tools, data
sources, and products interact within organizational workflows. However, current frameworks lack
formal mathematical foundations for representing model relationships, leading to ad hoc integration
approaches that become unwieldy at scale. As artificial intelligence components proliferate in these
systems, a more rigorous basis for model interaction becomes essential for maintaining operational
coherence and analytical integrity.
4
Towards Languages for Generative Modeling
The Active Inference community has extensively explored numerous adjectival modifications of
the base framework, including Deep, Affective, Branching-Time, Quantum, Mortal, Structured
Inference, among others. Each adjectival-prefixed variant emphasizes specific architectural aspects
or extensions of the core formalism. Building on this, CEREBRUM focuses on a wider range of
linguistic formalism (e.g. in this paper, declensional semantics) rather than adjectival modifications.
In this first CEREBRUM paper, there is an emphasis on the declensional aspects of generative
models as noun-like entities, separate from adjectival qualification.
This approach aligns with
category theoretic approaches to linguistics, where morphisms between objects formalize gram-
matical relationships and transformations. By applying formal case grammar to generative models,
CEREBRUM extends and transposes structured modeling approaches to ecosystems of shared intel-
ligence, while preserving the underlying (partitioned, flexible, variational, composable, interfacial,
inter-active, empirical, applicable, communicable) semantics.
5
Conceptual Foundations: The Intersection of Four Domains
CEREBRUM integrates four key domains to create a unified framework for model management
(Figure 1):
1. Cognitive Systems Modeling offers the entities that take on case relationships
2. Active Inference supplies the predictive processing mechanics that drive case transforma-
tions
3. Linguistic Case Systems provide the grammatical metaphor for how models relate to each
other
4. Intelligence Production furnishes the practical application context and workflows
5

## Page 6

Figure 1: Foundation Domains of CEREBRUM. The diagram shows the four key domains (Cog-
nitive Systems Modeling, Active Inference, Linguistic Case Systems, and Intelligence Production)
and their integration through the CEREBRUM core to produce enhanced model management ca-
pabilities.
6

## Page 7

6
Methods and Materials
6.1
Formal Framework Development
The CEREBRUM framework was developed as a part of a broader synthetic intelligence frame-
work, combining linguistic theory, cognitive science, category theory, and operations research. Key
methodological approaches included:
1. Linguistic Formalization: Adapting morphosyntactic case theory into computational rep-
resentations through abstract algebraic structures.
2. Category-Theoretic Mapping: Implementing category theory to formalize morphisms
between case states as functorial transformations.
3. Algorithmic Implementation: Developing algorithmic specifications for case transforma-
tions compliant with the Free Energy Principle.
4. Variational Methods: Applying variational free energy calculations to optimize model
inference as well as structural transformations.
6.2
Mathematical Foundation
The mathematical foundation of CEREBRUM builds on formalizations of case transformations
using category theory and variational inference. Case transformations are modeled as morphisms in
a category where objects are models with specific case assignments. The framework employs metrics
including Kullback-Leibler divergence, Fisher information, and Lyapunov functions to quantify
transformation eﬀicacy and system stability. This approach provides both theoretical guarantees of
compositional consistency and practical optimization methods for computational implementation.
7
Core Concept: Cognitive Models as Case-Bearing Entities
Just as nouns in morphologically rich languages take different forms based on their grammatical
function, cognitive models in CEREBRUM can exist in different “states” or “cases” depending on
how they relate to other models or processes within the system. Figure 2 illustrates this linguistic
parallel.
8
Case Functions in Cognitive Modeling
Each case defines a specific relationship type between models or between models and data (Table
1). The basic framework is depicted in Figure 3.
Table 1: Case Functions in Cognitive Model Systems
7

## Page 8

Figure 2: Case Relationships - Model and Linguistic Parallels. The diagram illustrates parallel case
relationships between a generative model and linguistic examples, demonstrating how model cases
mirror grammatical roles in natural language.
Figure 3: Cognitive Model Case Framework. The hierarchical organization of case types in CERE-
BRUM, showing primary, source, and contextual declensions with their functional relationships to
the core generative model.
8

## Page 9

Abbr
Case
Function in CEREBRUM
Example Usage
[NOM]
NominativeModel as active agent; acts as the
primary producer of predictions and
exerts causal influence on other models
Model X [NOM] generates
predictions about data
distributions; controls
downstream processing
[ACC]
Accusative Model as object of process; receives
transformations and updates from
other models or processes
Process applies to Model
X [ACC]; optimization
procedures refine Model
X’s parameters
[GEN]
Genitive
Model as source/possessor; functions
as the origin of outputs, products, and
derived models
Output of Model X
[GEN]; intelligence
products derived from
Model X’s inferences
[DAT]
Dative
Model as recipient; specifically
configured to receive and process
incoming data flows
Data fed into Model X
[DAT]; Model X receives
information from external
sources
[INS]
InstrumentalModel as method/tool; serves as the
means by which analytical operations
are performed
Analysis performed via
Model X [INS]; Model X
implements analytical
procedures
[LOC]
Locative
Model as context; provides
environmental constraints and
situational parameters
Parameters within Model
X [LOC]; environmental
contingencies modeled by
X
[ABL]
Ablative
Model as origin/cause; represents
historical conditions or causal
precursors
Insights derived from
Model X [ABL]; causal
attributions traced to
Model X
[VOC]
Vocative
Model as addressable entity; functions
as a directly callable interface with
name-based activation
“Hey Model X” [VOC];
direct invocation of Model
X for task initialization;
documentation reference
point
Within intelligence production systems, these case relationships serve critical functional roles: nom-
inative models act as primary analytical engines driving the intelligence case; accusative models
become targets of quality assessment and improvement; multimodal genitive models generate docu-
mentation and reports; dative models receive and process collected intelligence data; instrumental
models provide the methodological framework for investigations; locative models establish situa-
9

## Page 10

tional boundaries; ablative models represent the historical origins of analytical conclusions; and
vocative models serve as directly addressable interfaces for command initiation and documenta-
tion reference. Together, these case relationships create a comprehensive framework for structured
intelligence workflows.
Figure 4 illustrates how this core framework integrates with intelligence case management.
Figure 4: Generative Model Integration in Intelligence Case Management. Illustrates how CERE-
BRUM’s generative model core orchestrates intelligence production and case management through
case-specific transformations.
9
A Preliminary Example of a Case-Bearing Model: Homeostatic
Thermostat
Consider a cognitive model of a homeostatic thermostat that perceives room temperature with
a thermometer, and regulates temperature through connected heating and cooling systems.
In
nominative case [NOM], the thermostat model actively generates temperature predictions and dis-
patches control signals, functioning as the primary agent in the temperature regulation process.
When placed in accusative case [ACC], this same model becomes the object of optimization pro-
cesses, with its parameters being updated based on prediction errors between expected and actual
temperature readings. In dative case [DAT], the thermostat model receives environmental tempera-
ture data streams and occupant comfort preferences as inputs. The genitive case [GEN] transforms
the model into a generator of temperature regulation reports and system performance analytics
(“genitive AI”). When in instrumental case [INS], the thermostat serves as a computational tool
10

## Page 11

implementing control algorithms for other systems requiring temperature management. The loca-
tive case [LOC] reconfigures the model to represent the contextual environment in which temper-
ature regulation occurs, modeling building thermal properties, or discussing something within the
model as a location. Finally, in ablative case [ABL], the thermostat functions as the origin of his-
torical temperature data and control decisions, providing causal explanations for current thermal
conditions. This single cognitive model thus assumes dramatically different functional roles while
maintaining its core identity as a thermostat.
10
Declinability of Active Inference Generative Models
At the core of CEREBRUM lies the concept of declinability - the capacity for generative models
to assume different morphological and functional roles through case transformations, mirroring the
declension patterns of nouns in morphologically rich languages. Unlike traditional approaches where
models maintain fixed roles, or variable roles defined by analytical pipelines, CEREBRUM treats
cognitive models as flexible entities capable of morphological adaptation to different operational
contexts.
10.1
Morphological Transformation of Generative Models
When an active inference generative model undergoes case transformation, it experiences orches-
trated systematic changes summarized in Table 2:
1. Functional Interfaces: Input/output specifications change to match the case role require-
ments
2. Parameter Access Patterns: Which parameters are exposed or constrained changes based
on case
3. Prior Distributions: Different cases employ different prior constraints on parameter values
4. Update Dynamics: The ways in which the model updates its internal states vary by case
role
5. Computational Resources: Different cases receive different precision-weighted computa-
tional allocations
Table 2: Transformational Properties of Active Inference Generative Models Under
Case Declensions
Case
Parametric Changes
Interface Transformations
Precision Weighting
[NOM]
Fully accessible
parameters; all degrees
of freedom available for
prediction generation;
strongest prior
constraints on
likelihood mapping
Outputs predictions; exposes
forward inference pathways;
prediction interfaces activated
Highest precision on
likelihood; maximizes
precision of generative
mapping from internal
states to observations
11

## Page 12

Case
Parametric Changes
Interface Transformations
Precision Weighting
[ACC]
Restricted parameter
access; plasticity gates
opened; learning rate
parameters prioritized
Receives transformations;
update interfaces exposed;
gradient reception pathways
active
Highest precision on
parameters; maximizes
precision of parameter
updates based on
prediction errors
[DAT]
Input-focused
parameterization;
sensory mapping
parameters prioritized;
perceptual
categorization
parameters activated
Receives data flows; input
processing interfaces exposed;
sensory reception channels
active
Highest precision on
inputs; maximizes
precision of incoming
data relative to
internal expectations
[GEN]
“Genitive AI”;
Output-focused
parameterization;
production parameters
activated; generative
pathway emphasis
Generates products; output
interfaces prioritized;
production pathways activated
Highest precision on
outputs; maximizes
precision of generated
products relative to
internal models
[INS]
Method-oriented
parameters exposed;
algorithmic parameters
accessible; procedural
knowledge emphasized
Implements processes;
computational interfaces active;
procedural execution pathways
open
Highest precision on
operations; maximizes
precision of procedural
execution relative to
methodological
expectations
[LOC]
Context parameters
emphasized;
environmental
modeling parameters
prioritized; situational
knowledge emphasized
Provides environmental
constraints; contextual
interfaces active; environmental
modeling pathways prioritized
Highest precision on
contexts; maximizes
precision of contextual
representation relative
to environmental
dynamics
[ABL]
Origin states
emphasized; historical
parameters accessible;
causal attribution
pathways strengthened
Source of information; historical
data interfaces active; causal
explanation pathways open
Highest precision on
historical data;
maximizes precision of
causal attributions and
historical
reconstructions
12

## Page 13

Case
Parametric Changes
Interface Transformations
Precision Weighting
[VOC]
Identity parameters
prioritized; naming and
identification
parameters activated;
interface exposure
emphasized
Maintains addressable
interfaces; name recognition
pathways activated; command
reception channels open
Highest precision on
identification cues;
maximizes precision of
name recognition
relative to calling
patterns
10.2
Active Inference Model Declension Example
Consider a perception-oriented generative model M with parameters theta, internal states s, and
observational distribution p(o|s,theta). When declined across cases, this single model transforms
as follows:
• M[NOM]: Actively generates predictions by sampling from p(o|s,theta), with all parameters
fully accessible
• M[ACC]: Becomes the target of updates, with parameter gradients calculated from predic-
tion errors
• M[DAT]: Configured to receive data flows, with specific input interfaces activated
• M[GEN]: Optimized to generate outputs, with output interfaces prioritized
• M[INS]: Functions as a computational method, exposing algorithmic interfaces
• M[LOC]: Provides contextual constraints for other models, with environmental parameters
exposed
• M[ABL]: Serves as an information source, with historical data accessible
• M[VOC]: Functions as an addressable entity responding to direct invocation, with naming
parameters activated
The Vocative case [VOC] represents a unique functional role where models serve as directly ad-
dressable entities within a model ecosystem. Unlike other cases that focus on data processing or
transformational aspects, the vocative case specifically optimizes a model for name-based recogni-
tion and command reception. This has particular relevance in synthetic intelligence environments
where models must be selectively activated or “woken up” through explicit address, similar to how
humans are called by name to gain their attention. The vocative case maintains specialized in-
terfaces for handling direct commands, documentation references, and initialization requests. In
practical applications, models in vocative case might serve as conversational agents awaiting acti-
vation, documentation reference points within technical specifications, or system components that
remain dormant until explicitly addressed. This pattern mimics the linguistic vocative case where
a noun is used in direct address, as in “Hey Siri” or “OK Google” activation phrases for digital
assistants, creating a natural bridging pattern between human language interaction and model
orchestration.
This systematic pattern of transformations constitutes a complete “declension paradigm” for cog-
nitive models, using precision-modulation to fulfill diverse functional roles while maintaining their
13

## Page 14

core identity.
11
Model Workflows as Case Transformations
Case transformations represent operations that change the functional role of a model in the system,
reflecting active inference principles of prediction and error minimization.
Figure 5 provides a
sequence diagram of a typical transformation cycle, and Figure 6 shows the intelligence production
workflow where these transformations occur.
Figure 5: Model Workflows as Case Transformations - Sequence Diagram 1. Illustrates the tempo-
ral sequence of case transformations as models transition through different functional roles in an
intelligence workflow.
12
Category-Theoretic Formalization
CEREBRUM employs category theory to formalize case relationships between cognitive models,
creating a rigorous mathematical foundation, illustrated in Figure 7 and Figure 8.
14

## Page 15

Figure 6: Intelligence Production Workflow with Case-Bearing Models. Illustrates the intelligence
production cycle, showing the stages where models with different case assignments participate.
Figure 7: CEREBRUM Category Theory Framework. Demonstrates the category-theoretic formal-
ization of case relationships and transformations between cognitive models.
15

## Page 16

Figure 8:
Category Theory Framework (Alternative View).
Further illustrates the category-
theoretic components and properties within CEREBRUM.
16

## Page 17

13
Computational Linguistics, Structural Alignment, and Model
Relationships
CEREBRUM supports different alignment systems for model relationships, mirroring linguistic mor-
phosyntactic structures (Figure 9). These alignment patterns determine how models interact and
transform based on their functional roles. Figure 9 illustrates the core alignment patterns derived
from linguistic theory, showing how models can be organized based on their case relationships.
This includes nominative-accusative alignment (where models are distinguished by their role as
agents or patients), ergative-absolutive alignment (where models are grouped by their relationship
to actions), and tripartite alignment (where each case is marked distinctly).
Figure 9: Morphosyntactic Alignments in Model Relationships. Shows how CEREBRUM imple-
ments different alignment patterns for model relationships based on linguistic morphosyntactic
structures.
Figure 10 demonstrates the practical implementation of these alignment patterns in model ecosys-
tems, showing how different alignment systems affect model interactions and transformations. The
diagram illustrates the computational implications of each alignment pattern, including resource
allocation, message passing, and transformation eﬀiciency. This implementation view complements
the theoretical alignment patterns shown in Figure 9 by demonstrating their practical application
in cognitive model management.
17

## Page 18

Figure 10: Computational Implementation of Model Relationships. Illustrates the practical imple-
mentation details of model relationships in CEREBRUM, including resource allocation patterns,
message passing eﬀiciency, and transformation optimization strategies.
18

## Page 19

14
Implementation in Intelligence Production
As mentioned, CEREBRUM integrates with intelligence case management through structured work-
flows (see Figures 4 and 6). Figure 11 and Figure 12 provide alternative state-based visualizations
of these workflows.
The intelligence production workflow begins with raw data collection, where models in instrumental
case [INS] serve as data collection tools, implementing specific methods for information gathering.
As data moves through preprocessing, models transition to nominative case [NOM], taking on active
processing roles to clean, normalize, and prepare the data for analysis. During analysis, models
assume locative case [LOC], providing contextual understanding and environmental parameters
that shape the analytical process.
Integration represents a critical transition point where models in genitive case [GEN] generate
intelligence products by synthesizing information from multiple sources. These products then un-
dergo evaluation by models in accusative case [ACC], which assess quality and identify areas for
improvement.
The refinement phase employs models in dative case [DAT] to process feedback
and implement necessary changes, while deployment returns models to nominative case [NOM] for
active implementation of refined solutions.
This cyclical process demonstrates how case transformations enable models to maintain their core
identity while adapting to different functional requirements throughout the intelligence production
lifecycle. Each case assignment optimizes specific aspects of model behavior, from data collection
and processing to product generation and quality assessment, creating a flexible yet structured
approach to intelligence production.
15
Active Inference Integration
CEREBRUM aligns with active inference frameworks by treating case transformations as predictive
processes within a free energy minimization framework, as illustrated in Figure 13. Figure 14 details
the associated message passing rules.
16
Formal Case Calculus
The relationships between case-bearing models follow a formal calculus derived from grammatical
case systems, presented in Figure 15.
17
Cross-Domain Integration Benefits
The CEREBRUM framework delivers several advantages through its integration of the four foun-
dational domains:
Table 4: Cross-Domain Integration Benefits in CEREBRUM Framework
19

## Page 20

Figure 11: Implementation in Intelligence Production - State Diagram. Provides a state-based view
of the intelligence workflow highlighting model case assignments at each stage.
20

## Page 21

Figure 12: Intelligence Workflow (Alternative View). Presents another perspective on the intelli-
gence production cycle and feedback loops, emphasizing case roles.
21

## Page 22

Figure 13: Active Inference Integration Framework.
Shows how active inference principles are
integrated with case transformations through precision-weighted message passing and free energy
minimization.
22

## Page 23

Figure 14: Case-Specific Message Passing in Active Inference.
Illustrates how message passing
dynamics change based on the model’s current case assignment within an active inference hierarchy.
Figure 15: Model Case Calculus Framework. Presents the formal mathematical relationships and
transformation rules that govern case transitions in the CEREBRUM framework.
23

## Page 24

Domain
Contribution
Benefit to CEREBRUM
Theoretical Significance
Linguistic
Case
Systems
Systematic
relationship
framework;
grammatical role
templates;
morphosyntactic
structures
Structured representation
of model interactions;
formalized functional
transitions; systematic
role assignment
Provides formal semantics for
model relationships; enables
compositional theory of model
interactions; grounds functions
in linguistic universals
Cognitive
Systems
Model-
ing
Entity
representation
and processing;
model
formalization;
information-
processing
structures
Flexible model
instantiation across
functional roles; adaptive
model morphology;
unified modeling
paradigm
Advances theory of cognitive
model composition; formalizes
functional transitions in
cognitive systems; bridges
symbolic and statistical
approaches
Active
Infer-
ence
Predictive
transformation
mechanics; free
energy principles;
precision-
weighted learning
Self-optimizing workflows
with error minimization;
principled uncertainty
handling; bidirectional
message passing
Extends active inference to
model ecosystems; provides
mathematical foundation for
case transformations; unifies
perception and model
management
Intelligence
Produc-
tion
Practical
operational
context;
analytical
workflows;
intelligence cycle
formalisms
Real-world application in
case management systems;
operational coherence;
analytical integrity
Bridges theoretical and applied
intelligence; enhances
intelligence workflow coherence;
improves analytical product
quality
18
Related Work
CEREBRUM builds upon several research traditions while offering a novel synthesis. In this first
paper, there are no specific works linked or cited. Later work will provide more detail in reference
and derivation. The work stands transparently on the shoulders of nestmates and so is presented
initially as a speculative design checkpoint in the development of certain cognitive modeling prac-
tices.
Related approaches include:
24

## Page 25

18.1
Cognitive Architectures
Existing cognitive architectures such as ACT-R, Soar, and CLARION provide comprehensive frame-
works for modeling cognitive processes but lack formal mechanisms for representing functional role
transitions. Unlike these systems, CEREBRUM explicitly models the morphological transforma-
tions of computational entities as they move through different processing contexts.
18.2
Category-Theoretic Cognition
Recent work applying category theory to cognitive science has established mathematical founda-
tions for cognitive processes. CEREBRUM extends this tradition by applying categorical structures
specifically to case relationships and active inference, focusing on practical applications in intelli-
gence production rather than purely theoretical constructs.
18.3
Active Inference Applications
Prior applications of active inference to artificial intelligence have focused primarily on perception
and action in individual agents. CEREBRUM expands this domain by applying active inference
principles to model ecosystems, where multiple models interact within structured workflows guided
by case-based transformations.
18.4
Linguistic Computing
Computational linguistics has extensively employed case grammar for natural language processing,
but rarely extended these principles to model management. CEREBRUM repurposes linguistic
case theory as a structural framework for model relationships rather than textual analysis.
19
Practical
Applications
of
Model
Declension
in
Cognitive
Ecosystems
The declension paradigm for cognitive models offers practical benefits in complex model ecosys-
tems spanning multiple cognitive domains. This section outlines specific applications where the
morphological adaptability of models provides significant advantages.
19.1
Model Pipeline Optimization
Complex cognitive workflows typically involve sequences of models arranged in processing pipelines.
Traditional approaches require specialized interface layers between models, leading to ineﬀiciencies
and compatibility challenges.
By applying case declensions to models in these pipelines, each
component can seamlessly adapt its interfaces:
Consider a pipeline where Model￿exhibits a case transition from [ACC] (receiving data) to [DAT]
(forwarding results), demonstrating how a single model can adapt its functional interfaces based on
its position in the processing sequence.
25

## Page 26

19.2
Computational Resource Optimization
In resource-constrained environments, the precision allocation mechanism provided by case declen-
sion enables dynamic distribution of computational resources:
Table 5: Resource Allocation Strategy by Cognitive Task Type
Use Case
Resource Strategy
Case Priority
Optimization Objective
Real-time
decision
making
Prioritize prediction
generation; allocate
resources to forward
inference; minimize
predictive latency
[NOM] > [DAT] >
[ACC] > others
Minimize latency; maximize
predictive accuracy; optimize
decision boundaries
Data
ingestion
and
processing
Prioritize input
handling; allocate
resources to perceptual
categorization;
maximize throughput
[DAT] > [ACC] >
[GEN] > others
Maximize throughput;
optimize filter eﬀiciency;
minimize information loss
Report
generation
Prioritize output
production; allocate
resources to synthesis;
optimize presentation
clarity
[GEN] > [NOM] >
[LOC] > others
Optimize fidelity; maximize
clarity; ensure appropriate
detail level
Method
development
Prioritize process
refinement; allocate
resources to algorithm
optimization; focus on
error reduction
[INS] > [ACC] >
[NOM] > others
Minimize error; improve
algorithmic eﬀiciency; enhance
procedural robustness
This dynamic resource allocation is formalized through the precision-weighted free energy equation
(Equation 14 in the Mathematical Appendix), where models are allocated computational resources
proportional to their precision weights for their current case assignment.
19.3
Model Ecosystem Adaptability
Cognitive ecosystems must adapt to changing environments and requirements.
The declension
paradigm enables flexible reconfiguration of model relationships without architectural redesign.
Conceptually, this means the same set of models can reconfigure their functional roles through case
reassignment, adapting to new requirements without changing the underlying model implementa-
tions.
26

## Page 27

19.4
Cross-Domain Integration
The CEREBRUM framework facilitates integration between disparate cognitive domains by pro-
viding a unified grammatical structure for model interactions:
Table 6: Cross-Domain Integration Patterns in CEREBRUM Framework
Domain
Primary Cases
Integration Pattern
Error Propagation
Perception [NOM] (senses),
[ACC] (percepts)
Sensory models [NOM] →
Perceptual models [ACC];
hierarchical feature
extraction; predictive sensing
Bottom-up; prediction
errors flow from sensors to
percepts;
precision-weighted by
sensory reliability
Reasoning [INS] (logic),
[LOC] (context)
Logical models [INS] →
Contextual models [LOC];
context-sensitive inference;
situational logic
Bidirectional; coherence
errors propagate between
logical rules and
contextual constraints;
mutual constraints
Planning
[GEN] (goals),
[ABL] (history)
Historical models [ABL] →
Goal models [GEN];
experience-informed
planning; trajectory
optimization
Top-down; goal-directed
errors influence historical
interpretation; teleological
constraints
Action
[DAT] (commands),
[NOM] (execution)
Command models [DAT] →
Execution models [NOM];
imperative processing; motor
control
Circular; execution errors
feed back to command
refinement; continuous
adjustment loop
By mapping these domain-specific interactions to standardized case relationships, previously in-
compatible models can be integrated into cohesive cognitive systems.
19.5
Knowledge Graph Enhancement
The case declension system enhances knowledge representation by providing richer relational se-
mantics in model-based knowledge graphs. This enhancement operates at multiple levels:
1. Semantic Role Labeling:
• Models in [NOM] case represent active knowledge producers
• Models in [ACC] case represent knowledge targets/recipients
• Models in [DAT] case represent knowledge transfer endpoints
• Models in [GEN] case represent knowledge sources/origins
• Models in [INS] case represent methodological knowledge
• Models in [LOC] case represent contextual knowledge
27

## Page 28

• Models in [ABL] case represent historical/causal knowledge
2. Relationship Typing:
• Morphosyntactic edges encode relationship types
• Case assignments provide edge directionality
• Case transitions represent knowledge flow patterns
• Multi-case paths represent complex knowledge transformations
3. Example Knowledge Propagation Rules:
• Case-preserving transformations maintain semantic roles
• Case-changing transformations represent functional shifts
• Case alignment patterns guide knowledge integration
• Case-based precision weighting prioritizes knowledge flow (see Equation 13 in Mathe-
matical Appendix)
This enhanced knowledge graph shows how case-declined models provide explicit relationship se-
mantics between entities, creating richer knowledge representations that mirror the way natural
language encodes semantic relationships through case systems.
19.6
Emergent Behaviors in Model Collectives
When multiple case-bearing models interact within an ecosystem, emergent collective behaviors
arise from their case-driven interactions, analogous to how linguistic communities develop shared
understanding through dialog:
1. Self-organizing workflows:
• Models dynamically form processing chains based on complementary case assignments
• Like speakers in dialogue naturally assuming complementary roles (questioner/answerer)
• Case alignment creates natural processing pipelines
• Processing chains form spontaneously through case compatibility
2. Adaptive resource allocation:
• Precision-weighted competition for computational resources drives eﬀicient task distri-
bution
• Similar to attention allocation in linguistic communities
• Resources are allocated based on case-specific precision weights (see Equation 13 in the
Mathematical Appendix)
• Dynamic reallocation follows free energy gradients
3. Collective learning:
• Error signals propagate through case relationships
• Like linguistic communities converging on shared meanings
• Learning rates are modulated by case compatibility
• System-wide adaptation through message passing (see Equations 8-12 in the Mathemat-
ical Appendix)
4. Fault tolerance:
• Models can adopt alternative cases when certain cognitive functions are degraded
28

## Page 29

• Similar to linguistic communities adapting to speaker limitations
• Case reassignment follows free energy minimization
• Graceful degradation through case flexibility
5. Semantic Consensus Formation:
• Models converge on shared representations through case-mediated interactions
• Parallels linguistic communities developing shared vocabularies
• Consensus emerges through case-specific alignment
• Alignment strength varies by case type
6. Hierarchical Organization:
• Case relationships naturally create processing hierarchies
• Like linguistic communities developing formal/informal speech levels
• Hierarchy levels emerge from case distributions
• Case assignments reflect hierarchical position
These emergent properties demonstrate how the declension paradigm enables robust, adaptive
collective behaviors in complex cognitive ecosystems, mirroring the way linguistic communities
develop and maintain shared understanding through structured interactions. The mathematical
formalization of these properties provides a rigorous foundation for analyzing and optimizing model
collective behavior.
The parallel between model collectives and linguistic communities extends to:
1. Information Flow Patterns:
• Case-based routing: Messages flow according to case compatibility
• Community structure: Models cluster by case aﬀinity
• Flow eﬀiciency depends on case-specific precision weights
2. Adaptation Mechanisms:
• Local adjustments: Models modify case assignments based on neighbors
• Global optimization: System-wide free energy minimization (see Equation 1 in the Math-
ematical Appendix)
• Adaptation rates follow temporal decay patterns
3. Stability Properties:
• Case equilibrium: Stable distributions of case assignments
• Dynamic resilience: Recovery from perturbations
• Stability emerges from case distribution entropy
This framework provides a formal basis for understanding how collections of case-bearing models can
develop sophisticated collective behaviors analogous to linguistic communities, while maintaining
mathematical rigor through precise formalization of the underlying mechanisms.
(See Appendix 2: Novel Linguistic Cases for a discussion of how CEREBRUM can discover and
create new linguistic cases beyond traditional case systems.)
29

## Page 30

20
Future Directions
Future work on the CEREBRUM framework will focus on both theoretical expansions and practical
implementations:
• Programming Libraries:
Developing robust programming libraries implementing the
CEREBRUM framework across multiple languages to facilitate adoption
• Visualization Tools: Creating interactive visualization tools for case transformation pro-
cesses to enhance understanding and analysis
• Linguistic Extensions: Expanding the framework to incorporate additional linguistic fea-
tures such as aspect, tense, and modality into model relationship representations
• Open Source Stewardship: Establishing open source governance and community develop-
ment practices through the Active Inference Institute
• Computational Complexity: Deriving formal computational complexity estimates for case
transformations in various model ecosystem configurations
• Multiple Dispatch Systems: Implementing multiple dispatch architectures for program-
ming languages to eﬀiciently handle case-based polymorphism
• Database Methods: Developing specialized database structures and query languages for
eﬀicient storage and retrieval of case-bearing models
• Cognitive Security: Exploring security implications of case-based systems, including au-
thorization frameworks based on case relationships
21
Conclusion
CEREBRUM provides a structured framework for managing cognitive models by applying linguistic
case principles to represent different functional roles and relationships. This synthesis of linguis-
tic theory, category mathematics, active inference, and intelligence production creates a powerful
paradigm for understanding and managing complex model ecosystems. By treating models as case-
bearing entities, CEREBRUM enables more formalized transformations between model states while
providing intuitive metaphors for model relationships that align with human cognitive patterns and
operational intelligence workflows.
The formal integration of variational free energy principles with case transformations establishes
CEREBRUM as a mathematically rigorous framework for active inference implementations. The
precision-weighted case selection mechanisms, Markov blanket formulations, and hierarchical mes-
sage passing structures provide computationally tractable algorithms for optimizing model interac-
tions. These technical formalizations bridge theoretical linguistics and practical cognitive modeling
while maintaining mathematical coherence through category-theoretic validation.
The CEREBRUM framework represents another milestone in a long journey of how we conceptu-
alize model relationships, moving from ad hoc integration approaches, on through seeking the first
principles of persistent, composable, linguistic intelligences. This journey, really an adventure, con-
tinues to have profound implications for theory and practice. By here incipiently formalizing the
30

## Page 31

grammatical structure of model interactions, CEREBRUM points towards enhancement of current
capabilities and opens new avenues for modeling emergent behaviors in ecosystems of shared intel-
ligence. As computational systems continue to grow in complexity, frameworks like CEREBRUM
that provide structured yet flexible approaches to model management will become increasingly
essential for maintaining conceptual coherence and operational effectiveness.
Appendix 1: Mathematical Formalization
22
Mathematical Appendix
This appendix contains all mathematical formalizations referenced throughout the paper, organized
by equation number.
22.1
Variational Free Energy and Case Transformations
Equation 1: Variational Free Energy for Case Transformation
𝐹= 𝐷𝐾𝐿[𝑞(𝑠|𝑇(𝑚))||𝑝(𝑠|𝑚)] −𝔼𝑝[log 𝑝(𝑜|𝑠, 𝑇(𝑚))]
(1)
where T(m) represents the transformed model, s are internal states, and o are observations.
Equation 2: Markov Blanket and Case Relationship
Case(𝑀) ⊆MB(𝑀)
(2)
where MB(M) denotes the Markov blanket of model M.
Equation 3: Precision Weighting for Case Selection
𝛽(𝑐, 𝑚) =
exp(−𝐹(𝑐, 𝑚))
∑𝑖exp(−𝐹(𝑐𝑖, 𝑚))
(3)
where ￿(c,m) is the precision weight for case c and model m.
Equation 4: Case-Specific Gradient Descent on Free Energy
𝜕𝑚
𝜕𝑡= −𝜅𝑐⋅𝜕𝐹
𝜕𝑚
(4)
where 𝜅𝑐is the case-specific learning rate.
Equation 5: Expected Free Energy Reduction in Case Transitions
𝔼[Δ𝐹] = ∑
𝑠,𝑎
𝑇(𝑠′|𝑠, 𝑎)𝜋[𝑎|𝑠](𝐹(𝑠, 𝑐) −𝐹(𝑠′, 𝑐′))
(5)
31

## Page 32

where c and c’ represent the initial and target cases respectively.
Equation 6: Bayes Factor for Case Selection
𝐵𝐹= 𝑝(𝑜|𝑚, 𝑐1)
𝑝(𝑜|𝑚, 𝑐2)
(6)
Equation 7: Free Energy Minimization in Case Transitions
𝐹= 𝐷𝐾𝐿[𝑞(𝑠|𝑐, 𝑚)||𝑝(𝑠|𝑚)] −𝔼𝑞(𝑠|𝑐,𝑚)[log 𝑝(𝑜|𝑠, 𝑐, 𝑚)]
(7)
22.2
Message Passing Rules for Different Cases
These equations illustrate how case assignments modulate standard hierarchical message passing
(e.g., in predictive coding) where beliefs/predictions (𝜇) and prediction errors (𝜀) flow between
adjacent levels (denoted by superscripts 0 and 1). The case-specific weights (𝜅𝑐) determine the
influence of each message type based on the model’s current functional role.
Equations 8-12: Case-Specific Message Passing Rules
Nominative [NOM] ∶𝜇0 = 𝜇0 + 𝜅𝑁𝑂𝑀⋅(𝜇1 −𝜇0)
(8)
(Lower-level prediction 𝜇0 updated by top-down prediction 𝜇1, weighted by 𝜅𝑁𝑂𝑀)
Accusative [ACC] ∶𝜀1 = 𝜀1 + 𝜅𝐴𝐶𝐶⋅(𝜀0 −𝜀1)
(9)
(Higher-level error 𝜀1 updated by bottom-up error 𝜀0, weighted by 𝜅𝐴𝐶𝐶)
Dative [DAT] ∶𝜇0 = 𝜇0 + 𝜅𝐷𝐴𝑇⋅(𝑑𝑎𝑡𝑎−𝜇0)
(10)
(Lower-level prediction 𝜇0 updated directly by incoming ‘data’, weighted by 𝜅𝐷𝐴𝑇)
Genitive [GEN] ∶𝑜𝑢𝑡𝑝𝑢𝑡= 𝜇0 + 𝜅𝐺𝐸𝑁⋅𝜂
(11)
(Output generated based on lower-level prediction 𝜇0, weighted by 𝜅𝐺𝐸𝑁, potentially with noise 𝜂)
Instrumental [INS] ∶𝑝𝑟𝑜𝑐𝑒𝑠𝑠= 𝑓(𝜇1, 𝜀0) ⋅𝜅𝐼𝑁𝑆
(12)
(A process output determined by some function 𝑓of top-down prediction 𝜇1 and bottom-up error
𝜀0, weighted by 𝜅𝐼𝑁𝑆)
Vocative [VOC] ∶𝑎𝑐𝑡𝑖𝑣𝑎𝑡𝑖𝑜𝑛= 𝜎(𝜅𝑉𝑂𝐶⋅𝑠𝑖𝑚(𝑖𝑑, 𝑎𝑑𝑑𝑟𝑒𝑠𝑠))
(12a)
32

## Page 33

(Activation state determined by similarity between model identity 𝑖𝑑and incoming address, weighted
by 𝜅𝑉𝑂𝐶and passed through activation function 𝜎)
where 𝜅𝑐represents case-specific learning rates or precision weights, 𝜂is a noise term, 𝜇0, 𝜇1 repre-
sent beliefs/predictions, and 𝜀0, 𝜀1 represent prediction errors at adjacent hierarchical levels.
22.3
Precision Allocation and Resource Optimization
Equation 13: Precision Weight Allocation with Temperature
𝛽(𝑐, 𝑚) =
exp(−𝛾⋅𝐹(𝑐, 𝑚))
∑𝑖exp(−𝛾⋅𝐹(𝑐𝑖, 𝑚))
(13)
where ￿is the inverse temperature parameter controlling allocation sharpness.
Equation 14: Resource-Weighted Free Energy
𝐹𝛽(𝑚) = ∑
𝑐
𝛽(𝑐, 𝑚) ⋅𝐹(𝑐, 𝑚) ⋅𝑅(𝑐)
(14)
where R(c) represents the computational resources allocated to case c.
22.4
Novel Case Formalizations
Equation 15: Conjunctive Case Free Energy
𝐹𝐶𝑁𝐽= 𝐷𝐾𝐿[𝑞(𝑠|𝐶𝑁𝐽, 𝑚)||𝑝(𝑠|𝑚)] −𝔼𝑞(𝑠|𝐶𝑁𝐽,𝑚)[log 𝑝(𝑜|𝑠, {𝑚𝑖})]
(15)
where {m_i} represents the assembly of connected models.
Equation 16: Conjunctive Case Message Passing
𝜇𝐶𝑁𝐽= ∑
𝑖
𝑤𝑖⋅𝜇𝑖+ 𝜅𝐶𝑁𝐽⋅(∏
𝑖
𝜇𝑖−∑
𝑖
𝑤𝑖⋅𝜇𝑖)
(16)
where w_i are model-specific weighting factors.
Equation 17: Recursive Case Precision Dynamics
𝛽(𝑅𝐸𝐶, 𝑚) =
exp(−𝛾⋅𝐹(𝑅𝐸𝐶, 𝑚))
∑𝑖exp(−𝛾⋅𝐹(𝑐𝑖, 𝑚)) + exp(−𝛾⋅𝐹(𝑅𝐸𝐶, 𝑚))
(17)
22.4.1
Glossary of Variables
• 𝑎: Action (in MDP context, often selecting a case transition)
• 𝛼: Learning rate (in Neural Process Models context)
33

## Page 34

• 𝐵𝐹: Bayes Factor (for comparing model evidence between cases)
• 𝑐, 𝑐𝑖, 𝑐′, 𝑐1, 𝑐2: Linguistic case assignment (e.g., NOM, ACC, specific case instances)
• Case(𝑀): Case assignment of model 𝑀
• Case Transformation: An operation that changes the functional role (case) of a model
within the system
• CEREBRUM: Case-Enabled Reasoning Engine with Bayesian Representations for Unified
Modeling
• 𝐷𝐾𝐿: Kullback-Leibler divergence
• data: Input data (in Dative case message passing; Eq 10)
• Declinability: The capacity of a generative model within CEREBRUM to assume different
morphological and functional roles (cases) through transformations
• 𝐸𝑝[⋅]: Expectation with respect to distribution 𝑝(Information Geometry)
• 𝔼[⋅]: Expectation operator
• 𝐹: Variational Free Energy
• 𝐹𝛽(𝑚): Resource-weighted free energy for model 𝑚
• 𝐹𝐶𝑁𝐽: Free energy for the speculative Conjunctive case
• 𝑓(...): Function (used generally; e.g., in Instrumental message passing; Eq 12)
• 𝑔𝑖𝑗: Fisher information metric tensor component (Information Geometry)
• 𝑖, 𝑗: Indices for summation or tensor components
• 𝐿(𝑀): Lyapunov function for model 𝑀(Dynamical Systems section)
• 𝑚, 𝑀: Cognitive model
• {𝑚𝑖}: Assembly or set of connected models
• MB(𝑀): Markov blanket of model 𝑀
• Morphological Marker (Computational Analogue): Specific computational properties
(e.g., active interfaces; parameter access patterns; update dynamics) that signal a model’s
current case assignment within CEREBRUM
• 𝑛: Model parameter count (Complexity section)
• 𝑂(...): Big O notation for computational complexity
• 𝑜: Observations or sensory data
• output: Output generated by a model (in Genitive case; Eq 11)
• 𝑝(𝑠|...): Prior distribution over internal states 𝑠
• 𝑝(𝑜|...): Likelihood distribution of observations 𝑜
• 𝑝(𝑥|𝑡ℎ𝑒𝑡𝑎): Probability distribution of data 𝑥given parameters 𝑡ℎ𝑒𝑡𝑎(Information Geometry)
• process: Result of a process executed by a model (in Instrumental case; Eq 12)
• 𝑞(𝑠|...): Approximate posterior distribution over internal states 𝑠
• 𝑅(𝑐): Computational resources allocated to case 𝑐
• 𝑅𝐸𝐶: Speculative Recursive case assignment
• 𝑠: Internal states of a model
• 𝑠′: Next state (in MDP context; target case assignment)
• 𝑡: Time variable (in gradient descent context; Eq 4)
• 𝑇: Transformation function (e.g., 𝑇(𝑚) is a transformed model in Eq 1; also MDP transition
34

## Page 35

function)
• 𝑇(𝑠′|𝑠, 𝑎): State transition function in MDP (probability of transitioning to state 𝑠′ from
state 𝑠given action 𝑎)
• 𝑤𝑖: Model-specific weighting factors (in Conjunctive case; Eq 16)
• Δ𝐹: Change in Free Energy
• Δ𝑤𝑖𝑗: Change in synaptic weight between neuron 𝑖and 𝑗(Neural Process Models section)
• 𝛽(𝑐, 𝑚): Precision weight (allocation) assigned to model 𝑚in case 𝑐
• 𝛾: Inverse temperature parameter (controlling precision allocation sharpness)
• 𝜖𝑖: Error signal of neuron 𝑖(Neural Process Models section)
• 𝜀0, 𝜀1: Error signals used in message passing (representing prediction errors at adjacent hier-
archical levels; Eq 9, 12)
• 𝜂: Noise term (Eq 11)
• 𝜅𝑐: Case-specific learning rate or precision weight (modulating message updates; Eqs 4, 8-12)
• 𝜇0, 𝜇1: Mean values used in message passing (representing predictions or beliefs at adjacent
hierarchical levels)
• 𝜇𝐶𝑁𝐽: Mean value resulting from Conjunctive case message passing
• 𝜋(𝑎|𝑠): Policy in MDP (probability of taking action 𝑎in state 𝑠)
• 𝜎′(𝑎𝑗): Derivative of activation function of neuron 𝑗(Neural Process Models section)
• 𝑡ℎ𝑒𝑡𝑎, 𝑡ℎ𝑒𝑡𝑎𝑖, 𝑡ℎ𝑒𝑡𝑎𝑗: Model parameters # Appendix 2: Novel Linguistic Cases
23
Discovering and Creating New Linguistic Cases Through
CEREBRUM
The CEREBRUM framework not only operationalizes traditional linguistic cases but potentially
enables the discovery of entirely new case archetypes through its systematic approach to model
interactions. As cognitive models interact in increasingly complex ecosystems, emergent functional
roles may arise that transcend the classical case system derived from human languages.
23.1
Emergence of Novel Case Functions
Traditional linguistic case systems evolved to serve human communication needs in physical and
social environments. However, computational cognitive ecosystems face novel challenges and op-
portunities that may drive the emergence of new functional roles. The mathematical formalism of
CEREBRUM provides a scaffold for identifying these emergent case functions through:
1. Pattern detection in model interaction graphs: Recurring patterns of information flow
that don’t fit established cases
2. Free energy anomalies: Unusual optimization patterns indicating novel functional config-
urations
3. Precision allocation clusters: Statistical clustering of precision weightings revealing new
functional categories
4. Transition probability densities: Dense regions in case transition probability spaces sug-
35

## Page 36

gesting stable new cases
23.2
Speculative Novel Case: The Emergent “Conjunctive” Case
One speculative example of a novel case that might emerge within CEREBRUM is what we might
term the “conjunctive” case [CNJ]. This case would represent a model’s role in synthesizing mul-
tiple predictive streams into coherent joint predictions that couldn’t be achieved through simple
composition of existing cases.
The mathematical formalism for a model in conjunctive case would extend the standard free energy
equation as shown in Equation 15 (see Mathematical Appendix), representing the assembly of con-
nected models participating in the joint prediction. The key innovation is that the likelihood term
explicitly depends on multiple models’ predictions rather than a single model’s output, enabling
integration of diverse predictive streams.
In the message-passing formulation, the conjunctive case would introduce unique update rules as
described in Equation 16 (see Mathematical Appendix), with weighting factors for individual model
predictions, as well as a multiplicative integration of predictions that captures interdependencies
beyond simple weighted averaging.
This formulation enables rich joint inference across model
collectives.
23.3
Speculative Novel Case: The “Recursive” Case
Another potential novel case is the “recursive” case [REC], which would enable a model to apply
its transformations to itself, creating a form of computational reflection not captured by traditional
cases.
In the recursive case, a model assumes both agent and object roles simultaneously, creating feedback
loops that enable complex self-modification behaviors. This case would be particularly relevant for
metalearning systems and artificial neural networks that modify their own architectures.
The recursive case would introduce unique precision dynamics as formalized in Equation 17 (see
Mathematical Appendix). The key innovation is that the model appears on both sides of the trans-
formation, creating a form of self-reference that traditional case systems don’t accommodate. This
enables models to introspect and modify their own parameters through self-directed transforma-
tions.
23.4
Speculative Novel Case: The “Metaphorical” Case
A third potential novel case is the “metaphorical” case [MET], which would enable a model to map
structures and relationships from one domain to another, creating computational analogies that
transfer knowledge across conceptual spaces.
In the metaphorical case, a model acts as a transformation bridge between disparate domains,
establishing systematic mappings between conceptual structures. This case would be particularly
36

## Page 37

valuable for transfer learning systems and creative problem-solving algorithms that need to apply
learned patterns in novel contexts.
The metaphorical case would introduce unique cross-domain mapping functions as formalized in
Equation 18 (see Mathematical Appendix). The key innovation is the structured alignment of latent
representations across domains, enabling principled knowledge transfer that preserves relational
invariants while adapting to target domain constraints.
23.4.1
Connections to Human Cognition and Communication
The metaphorical case has rich connections to multiple domains of human cognition and commu-
nication. In affective neuroscience, it models how emotional experiences are mapped onto concep-
tual frameworks, explaining how we understand emotions through bodily metaphors (e.g., “heavy
heart,” “burning anger”). In first and second-person neuroscience, metaphorical mappings enable
perspective-taking and empathy through systematic projection of one’s own experiential models
onto others. Educational contexts leverage metaphorical case operations when complex concepts
are taught through familiar analogies, making abstract ideas concrete through structured mappings.
The way people converse about generative models often employs metaphorical language—describing
models as “thinking,” “imagining,” or “dreaming”—which represents a natural metaphorical map-
ping between human cognitive processes and computational operations. Learning itself fundamen-
tally involves metaphorical operations when knowledge from one domain scaffolds understanding in
another. Perhaps most profoundly, the metaphorical case provides a computational framework for
understanding how symbols and archetypes function in human cognition—as cross-domain map-
pings that compress complex experiential patterns into transferable, culturally-shared represen-
tations that retain their structural integrity across diverse contexts while adapting to individual
interpretive frameworks.
23.5
Implications of Novel Cases for Computational Cognition
The discovery of novel cases through CEREBRUM could have profound implications for computa-
tional cognitive science:
1. Expanded representational capacity: New cases enable representation of functional re-
lationships beyond traditional linguistic frameworks
2. Enhanced model compositionality: Novel cases might enable more eﬀicient composition
of complex model assemblies
3. Computational reflection: Cases like the recursive case enable systematic implementation
of self-modifying systems
4. Cross-domain integration: New cases like the metaphorical case might bridge domains
that are diﬀicult to connect with traditional case systems
These speculative extensions of CEREBRUM highlight its potential not just as an implementation of
linguistic ideas in computational contexts, but as a framework that could expand our understanding
of functional roles beyond traditional linguistic categories. The mathematical rigor of CEREBRUM
37

## Page 38

provides a foundation for systematically exploring this expanded space of possible case functions,
potentially leading to entirely new paradigms for understanding complex model interactions in
cognitive systems.
Table A1: Properties of Speculative Novel Cases in CEREBRUM
Property
Conjunctive Case [CNJ]
Recursive Case [REC]
Metaphorical Case [MET]
Function
Synthesizes multiple
predictive streams into
coherent joint
predictions; integrates
diverse model outputs;
resolves cross-model
inconsistencies
Applies
transformations to
itself; enables
self-modification;
creates meta-level
processing loops
Maps structures and
relationships between
domains; establishes
cross-domain
correspondences; transfers
knowledge patterns across
conceptual spaces
Parametric
Focus
Cross-model correlation
parameters and shared
latent variables;
inter-model weights; joint
distribution parameters
Self-referential
parameters; recursive
transformations;
meta-parameters
governing
self-modification
Structural alignment
parameters; analogical
mapping weights;
cross-domain
correspondence metrics
Precision
Weight-
ing
Highest precision on
inter-model consistency
and joint predictions;
emphasizes mutual
information; optimizes
integration factors
Dynamic
self-allocation;
recursive precision
assignment;
meta-precision
governing
self-modification
Selective precision on
structural invariants;
emphasis on relational
similarities over surface
features; adaptive
mapping precision
Interface
Type
Aggregative interfaces
with multiple connected
models; convergent
communication channels;
integration hubs
Reflexive interfaces;
self-directed
connections; loopback
channels
Bridging interfaces across
domain boundaries;
cross-contextual
mappings; translation
channels
Update
Dynam-
ics
Updates based on joint
prediction errors across
the connected model
assembly; collective error
minimization;
consistency optimization
Self-modification loops;
introspective learning;
meta-learning through
internal feedback
Updates based on
structural alignment
success; transfer
performance feedback;
analogical coherence
optimization
38


---
*Extraction method: pymupdf*
