# Full Text: Active Inference in Modeling Conflict

> Extracted from `2021_ModelingConflict.pdf`

---

## Page 1

Active Inference in Modeling Conflict 
 
 
December 2, 2021 
 
Scott David 1,2 
R.J. Cordes 1,3,4 
Daniel A. Friedman 1,3,5 
(1) Active Inference Lab, 
(2) Information Risk and Synthetic Intelligence Research Initiative (IRSIRI),  
University of Washington - Applied Physics Laboratory, 
(3) COGSEC, 
(4) Atlantic Council GeoTech Center,  
(5) University of California, Davis, Dept. of Entomology & Nematology  
A B S T R A C T
 
In this paper, we integrate conflict studies with Active Inference, a developing 
framework which provides an integrative and systems-level perspective on 
cognition and behavior. This formalization, the Active Inference Conflict 
(AIC) model, situates conflict in terms of a multiscale process of 
communication, trust, and relationship management enacted by interacting 
entities. The AIC model helps capture and extend the insights of previous 
models applied to aspects of conflict and war, such as OODA loops (observe -
orient-decide-act), the generations of warfare model, and the Rumsfeld Matrix. 
The AIC model aids in the analysis of pertinent aspects of modern conflict, 
such as cyber, psychological, biological, informational, financial, and 
ideological conflict, that are not amenable to coherent or consistent analysis 
using traditional models of human conflict. AIC is demonstrated to be of use 
in both monitoring and studying conflict, as well as in designing systems 
intended to facilitate controlled or managed conflict in scenarios characterized 
by business, operations, legal, technical, and social (BOLTS) components. 
Insights and implications from qualitative use are used as a foundation for 
offering recommendations for future research and social systems design. 
 
Active Inference in Modeling Conflict

## Page 2

Active Inference in Modeling Conflict, 2021 
 
 
 
Contents 
Introduction ............................................................................................................................................................ 1 
Previous Models of Military Conflict ................................................................................................................ 2 
Narrative Models of Conflict ......................................................................................................................... 3 
Collections of Heuristics ........................................................................................................................... 3 
Military Revolutions Model ...................................................................................................................... 7 
Generations of Warfare Framework .................................................................................................... 11 
Linn’s Model of Strategic Narrative ..................................................................................................... 15 
Quantitative Models of Conflict ................................................................................................................. 15 
Lanchester Models.................................................................................................................................... 15 
Fault Tree Analysis ................................................................................................................................... 16 
Effects Based Operations ....................................................................................................................... 16 
DoDAF ....................................................................................................................................................... 16 
Systems Warfare ........................................................................................................................................ 16 
Models of Conflict Information Flows and Decision-Making ............................................................ 17 
Observe–Orient–Decide–Act (OODA) Model ................................................................................ 17 
Rumsfeld Matrix of Knowing ................................................................................................................ 18 
Essential Features and Limitations of Past Conflict Models ................................................................ 20 
Active Inference Conflict Model ...................................................................................................................... 28 
Active Inference Overview, Terms, and Features .................................................................................. 31 
ActInf Terms ............................................................................................................................................. 31 
ActInf Features ......................................................................................................................................... 35 
Use of the AIC Model ................................................................................................................................... 37 
Entity Action Loop and Alignment with OODA ............................................................................. 37 
Unifying Quantitative and Formal Models of Conflict .................................................................... 38 
Moving Beyond Generations of Warfare ............................................................................................ 39 
Modeling and Discovering BOLTS Conflict ...................................................................................... 39 
Modeling Cognitive Security .................................................................................................................. 47 
Implications from Use: Future Information Structures and Rumsfeld’s Neglected Quadrant .......... 47 
Discussion ............................................................................................................................................................. 52 
Contribution Statements .................................................................................................................................... 56 
Funding and Acknowledgements ..................................................................................................................... 56 
Works Cited .......................................................................................................................................................... 57

## Page 3

Active Inference in Modeling Conflict, 2021 
 
1 
Introduction 
Human-scale conflict constituting “war” in its various incarnations has 
been studied from a variety of perspectives, including, but not limited 
to, statistical, ethnographic, logistical, sociological, legal, and 
philosophical frameworks. However, with the notable advances made 
in the capabilities of weapons systems and the introduction of global 
defense pacts made in the 20th Century, the risk calculus of triggering 
an official declaration of war has changed. The resulting dramatic 
increase in costs and displacements of kinetic war compels state and 
non-state actors to pursue their conflicting interests through 
alternative means. The resulting complex threat surfaces are not always 
well-described or modeled by existing frameworks for conflict (which 
usually have a military or domain-specific focus), which further 
amplifies risk even in tractable scenarios [1]. In this paper, we make 
use of Active Inference (ActInf), a framework which provides an 
integrative and systems-level perspective on cognition and behavior, to 
propose a new formalization of conflict in terms of a multiscale process 
of communication, trust, and relationship management enacted by 
interacting entities. This application of ActInf to questions of conflict, 
called the Active Inference Conflict (AIC) Model, extends recent work 
on Active Inference and human-robot trust system [2], cyberphysical 
systems [3], and societies as cognitive agents [4] to the domains of 
human conflict in expanding shared information environments.  
The AIC model is grounded in several previous frameworks for action 
and conflict from military science, including the generations of warfare 
(GW) model, observe-orient-decide-act (OODA) loop, and the 
Rumsfeld Matrix. Additionally, the AIC extends these models to better 
describe, frame, and offer recommendations for the current and 
projected future nature of war and other forms of conflict, whic h is 
increasingly non-kinetic. The AIC model is intended to offer 
generalization beyond conflict itself, helping not just to describe 
nation-state conflicts, but also complex multi-scale conflicts involving 
individuals and communities in contexts characterized by their 
business, operations, legal, technical, and social (BOLTS) components. 
The essential historical insights gleaned from the GW model offer a 
useful foundation from which this paper’s ActInf framing can be 
understood, and establishes a new chapter in the GW model’s framing 
of the timeless yet ever-changing aspects of human conflict. 
In this paper, we begin by offering a survey of past qualitative and 
quantitative models of conflict and the insights they provide. After this 
survey, we consider the essential features of the reviewed models, and

## Page 4

Active Inference in Modeling Conflict, 2021 
 
2 
highlight the need for models which offer more interoperability and 
generalization in order to stay relevant in the face of an ever-changing 
expression of conflict. We then offer a primer on the ActInf framew ork 
in terms of core terms and features. Following this description, we 
explore how the AIC model can extend previous models such as OODA 
and GW while still capturing their essential insights. In this 
exploration, special attention is given to how the AIC model relates to 
the Rumsfeld Matrix, and what this relationship may reveal about 
Rumsfeld’s oft-neglected quadrant, the “unknown-knowns”. We 
suggest that management of relationship and conflict with a 
prioritization of the often neglected “unknown-knowns” quadrant 
provides a pathway to multi-scale risk mitigation and leverage points 
for human interactions online. In summary, AIC is revealed to be more 
than just a powerful new model of war and conflict. AIC framing also 
invites consideration of how humans can harness the destructive 
energies of prior conflagrations of conflict at all levels into 
constructive systems that can perform useful “work” by converting the 
underlying information differentials of conflict into new forms of value 
the benefits of which can be distributed in managed ways to maintain 
the generative AIC apparatus (analogous to how an engine extracts 
useful work from heat gradients). The AIC model is an applied Active 
Inference approach for mitigating risk and enhancing value from the 
ever-increasing informational component of modern interactions. 
Finally, we conclude with a summary of insights and recommendations 
for future research and application. 
Previous Models of Military Conflict 
Being of obvious, existential importance to state sovereigns, war and 
conflict has been a subject of interest to historians, scholars, and artists 
since the birth of civilization. As evidenced by the hundreds of 
thousands of books written about the American Civil War alone [5], 
and a history of scholarship which extends back to some of the earliest 
books ever written [6], the subject of war has an unfathomably large 
literary and oral corpus. The vastness of the body of literature on war 
suggests that even if only a small fraction of the corpus is dedicated to 
generalizing and modeling war (the rest being historical documentation 
and analysis of instances of war), it would still constitute a significant 
body of literature in itself. For purposes of this article, and in the 
interest of presenting a referenceable review of past models and 
generalizations of war (while acknowledging that it is an impossible 
task to describe them all), we present past models of war and conflict 
in the following categories:

## Page 5

Active Inference in Modeling Conflict, 2021 
 
3 
• Narrative Models 
• Quantitative Models 
• Conflict Information Flows and Decision-Making Models 
Narrative Models of Conflict 
The term narrative model is used here to describe formal and 
semiformal models of conflict which were intended to provide guidance 
and actionable insight to strategic commanders through the use of 
qualitative, non-technical methods such as storytelling, aphorism, 
historical example, parables, and slogans. 
Collections of Heuristics 
The earliest attempts to create and compile informative representations 
of conflict and war do not offer integrated models in a modern sense, 
instead they offer collections of axioms, idioms, recipes, rules, 
principles, and patterns - rules of thumb, based on insights drawn from 
the experiences of the offeror. One of the oldest examples of these 
collections is Flavius Vegetius Renatus’ Epitome Rei Militaris, or 
“Epitome of Military Science” [7]. It is one of the few surviving 
Roman-era works on military science and art from its time and was 
routinely used during the Middle Ages to augment and inform writings 
on warfare [7].  
Though much of its content deals with specific questions about routine 
situations in which Roman commanders may have found themselves, 
such as in what kind of places camps should be built or how a suitable 
place might be chosen for battle, a section of the Epitome titled 
“General Rules of Warfare” also supplies “basic principles in an 
unspecific form which could be adapted to serve a great variety of 
military situations” [7]. These include: 
• “It is difficult to beat someone who can form a true estimate of 
his own and the enemy’s forces” 
• “He who spends more time watching in outposts and puts more 
effort into training soldiers, will be less subject to danger”  
• “Never lead forth a soldier to a general engagement except when 
you see that he expects victory” 
[7]

## Page 6

Active Inference in Modeling Conflict, 2021 
 
4 
Examples from other well-known collections of timeless heuristics 
relating to war throughout history and across cultures provide similar 
sorts of insights, such as the following: 
From Sun Tzu’s Art of War 
• “A skillful soldier does not raise a second levy” 
• “In order to kill the enemy, our men must be roused to anger” 
• “If equally matched, we can offer battle; if slightly inferior in 
numbers, we can avoid the enemy; if quite unequal in every way, 
we can flee” 
• “If you know the enemy and know yourself, you need not fear 
the result of a hundred battles. If you know yourself but not the 
enemy, for every victory gained you will also suffer a defeat. If 
you know neither the enemy nor yourself, you will succumb in 
every battle.” 
[6] 
From Moltke’s Art of War 
• “Excessive extension of the front brings danger of a 
breakthrough.” 
• “Engagements in forests last for a long time” 
• “One must immediately prepare supporting points captured in an 
engagement for defense in order to thwart the enemy’s efforts to 
recapture them” 
[8] 
Countless other works elaborating the art of war, provide detailed rules, 
patterns, and axioms of human armed conflict, such as those by Mao 
Tse-tung, Machiavelli, and Sun Bin [9–11]. When these collections are 
viewed as part of a common ensemble of axioms, bundled together, 
they may be argued to constitute nascent narrative models of warfare, 
helping generals, real or armchair, better understand the complex and 
challenging scenarios of conflict they are encountering, simulating, or 
studying. 
Also included within these collections of heuristics are later works from 
the 1800’s, such as Antoine-Henri Jomini’s Art of War [12] and Carl von 
Clausewitz’s On War [13]. While both these books provide their fair 
share of axioms and rules like earlier works, they also move beyond 
simple heuristics in an attempt to capture more generalizable models

## Page 7

Active Inference in Modeling Conflict, 2021 
 
5 
and frameworks for understanding and describing the underlying causes 
and motivations of warfare as an aid to formulating strategy and tactics 
for engagement. These developments signal an increasing awareness of 
the behaviors of war as part of the larger set of behaviors associated 
with human interactions and the conflict that they generate.  
For 
example, 
Jomini 
provides 
the 
following 
frameworks 
for 
understanding the nature of conflict, moving beyond a mere description 
of the practices of war to its underlying contexts of conflict to 
encourage an enhancement of the understanding of how best to engage 
[12]. Several of Jomini’s classification schemes are excerpted here:  
Eight types of motivations for states to engage in warfare: 
• “To reclaim rights or defend them... 
• to protect and maintain the great interests of the state...  
• To uphold neighboring states… 
• To fulfill obligations… 
• To propagate political or religious theories… 
• To increase the influence and power of the state… 
• To defend the threatened independence of the state… 
• To avenge insulted honor… 
• From a mania for conquest.” 
Two kinds of international Intervention: 
• “Intervention in the internal affairs of neighboring states… 
• intervention in external relations” 
And four kinds of war which result from such an intervention:  
• “Where the intervention is merely auxiliary, and with a force 
specified by former treaties… 
• where the intervention is to uphold a feeble neighbor by 
defending his territory, thus shifting the scene of war to other 
soil… 
• A state interferes as a principal party when near the theater of 
war, - which supposes the case of a coalition of several powers 
against one…

## Page 8

Active Inference in Modeling Conflict, 2021 
 
6 
• a state interferes either in a struggle already in progress, or 
interferes before declaration of war” 
[12] 
Clausewitz offers similar context-enhancing frameworks for war, but 
goes farther, arguing that even more generalizable analysis is needed 
and that those who “never rise above anecdote” will “never get down 
to the general factors that govern the matter… indeed they will 
consider a philosophy that encompasses the general run of cases as a 
mere dream” [13]. Clausewitz recognized that theory informs practice, 
and that awareness of context and causation of war as a form of huma n 
conflict provides valuable insights into the strategies and tactics for its 
effective engagement. Clausewitz was well aware of the limitations of 
prior descriptions of warfare, and made explicit the benefits of more 
comprehensive and multi-dimensional models that situated warfare 
among other forms of human conflict. 
Trinity of War 
Carl von Clausewitz, in pursuit of deeper generalizations, proposed 
what may be the earliest framework for describing warfare that is 
recognizable, on its face, as a generalizable model. He suggests that war 
is an extension of state policy, and as such, it is ruled by a “paradoxical 
trinity” of forces [13]. His description of this trinity is excerpted here: 
“The first of these three aspects mainly concerns the 
people; the second the commander and his army; the third 
the government. The passions that are to be kindled in war 
must already be inherent in the people; the scope which 
the play of courage and talent will enjoy in the realm of 
probability and chance depends on the particular character 
of the commander and the army; but the political aims are 
the business of government alone. 
These three tendencies are like three different codes of 
law, deep-rooted in their subject and yet variable in their 
relationship to one another. A theory that ignores any one 
of them or seeks to fix an arbitrary relationship between 
them would conflict with reality to such an extent that for 
this reason alone it would be totally useless... 
Our task therefore is to develop a theory that maintains a 
balance between these three tendencies, like an object 
suspended between three magnets.” 
[13]

## Page 9

Active Inference in Modeling Conflict, 2021 
 
7 
The trinity of war model captures the multi-node complexity that yields 
the nonlinear aspects of what motivates and channels the expression of 
those motivations in kinetic conflict. Further, it helps described certain 
non-combat oriented insights regarding conflict, such as war being 
conceptualized as an extension of political conflict [14], that it is 
motivated by state interest or raison d'état, and is moderated by a state’s 
ability to channel the motivations of both civilians and military 
personnel toward conflict [15]. 
What may be the most important aspect of Clausewitz’s model however, 
is that it was far ahead of its time in framing war as something akin  to 
a complex system rather than a mechanistic process, in which a trinity 
of “chance, uncertainty, and friction… will make anticipation of even 
the first-order consequences of military action highly conjectural” 
[16,17]. 
Military Revolutions Model 
Among the various categories of qualitative planning and descriptive 
models which have come into (and gone out of) fashion within the 
United States military was a collection of models centered on 
“revolutions in military affairs”, which grew to “increasing promin ence 
in Washington’s Byzantine budgetary and procurement struggles'' in the 
1990s [18], and served to rhetorically bind together technical and 
modeling advances. Initially just a reference by Western historians and 
Soviet military theorists to the notion of key historical inflection points 
in which there were unforeseeable, “fundamental [and] systemic” 
changes in the expression of war, the “military revolutions model” was 
picked up by the US defense community as a concept that was also 
considered valuable for doctrine and planning [18]. Since that time, 
numerous attempts have been made to model and chart these 
revolutions in order to help military leadership better understand their 
place both in history and in current affairs, and to help them plan for 
the future. Some examples of these models are surveyed below. 
Krepinevich Model 
The model presented by Krepinevich was one of the earlier 
attempts at formalization of the historical revolutions in 
military affairs. While the revolutions specifically noted 
by Krepinevich have been greatly modified or even 
abandoned in later models, his formalization of the 
elements underneath military revolutions has stayed 
relevant [18]. These elements were said to consist of 
technological change, systems development, operationa l

## Page 10

Active Inference in Modeling Conflict, 2021 
 
8 
innovation, and organizational adaptation [18,19]. The 
historical 
revolutions 
noted 
by 
Krepinevich, 
in 
chronological order, are as follows: 
• Infantry Revolution 
• Artillery Revolution 
• Revolution of Sail and Shot 
• Fortress Revolution 
• Gunpowder Revolution 
• Napoleonic Revolution 
• Land warfare Revolution 
• Naval Revolution 
• Revolutions in Mechanization, Aviation, and 
Information 
• Nuclear Revolution 
[19] 
Krepinevich’s model is unique among the other historical 
revolution models for its focus on warfare alone. 
Notwithstanding the focus on war, he recognized that 
changes in technology, which are themselves generated by 
the larger social and historical context, affect the nature 
of engagement in war. In a sense, he saw technology as the 
vehicle through which large scale social and historical 
changes affect war. Among the more valuable insights he 
derives from this model is that technological innovation 
does not guarantee a revolution in military affairs - 
instead, these revolutions occur when states change their 
process, systems, and organization in order to incorporate 
those innovations [19]. 
Knox and Murray Model 
Knox and Murray’s take on the revolutions in military 
affairs model [20] was built from its predecessors, 
incorporating key elements from Krepinevich, which they 
considered “typical” and fundamental to models of this 
kind [18]. What sets Knox and Murray’s model apart from 
its predecessors however, is three-fold. First, they

## Page 11

Active Inference in Modeling Conflict, 2021 
 
9 
explicitly included non-military systemic changes within 
the scope of revolutions in military affairs, such as those 
related to economies beyond the ability to supply 
armament. Second, they see each of the revolutions as 
reflecting, not just the innovations of its time, but also the 
novel combination and integration of the innovations and 
resulting changes of its predecessors. Third, they include 
two separate tracks of revolutions, seemingly inspired by 
Krepinevich’s suggestion that the inflection points in 
expression 
of 
warfare 
were 
separable 
from 
the 
implementations and incorporations of technological 
innovations. One was termed “military revolutions”, the 
other, “revolutions in military affairs”, referring to 
abstract 
inflection 
points 
and 
revolutionary 
implementations, respectively [18]. A summary of their 
charting of revolutions is included here: 
• Precursory, or “anticipatory” Revolutions in Military 
Affairs 
o The introduction of the longbow, gunpowder, 
and fortress architecture 
• Military Revolution I: The Modernization of the State 
and its Military Institutions 
o Associated revolutions of military affairs: 
▪ Dutch, Swedish, and French tactical and 
organizational reforms 
▪ Britain’s financial revolution 
• Military Revolutions II and III: The French and 
Industrial Revolutions 
o Associated revolutions of military affairs: 
▪ Napoleonic warfare and the complete 
battlefield annihilation of the enemy’s 
armed forces) 
▪ Transportation: railroads, steamships 
▪ Armament: combination of quick-firing 
small arms and artillery 
▪ Communications: telegraph

## Page 12

Active Inference in Modeling Conflict, 2021 
 
10 
• The Fisher Revolution 
o The introduction of “all-big-gun” battleships 
• Military Revolution IV: The First World War and its 
Irrevocable Combination of Preceding Revolutions 
o Associated revolutions of military affairs: 
▪ Combined Arms Tactics 
▪ Blitzkrieg Operations 
▪ Carrier, 
Submarine, 
and 
Amphibious 
Warfare 
▪ Radar and Signals Intelligence 
• Military Revolution V: Nuclear Weapons and Ballistic 
Delivery Systems 
o Associated revolutions of military affairs: 
▪ Precision Reconnaissance and Strike 
▪ Stealth Systems 
▪ Increased 
Lethality 
of 
Conventional 
Munitions 
[20] 
Hoffman Model 
Hoffman, a former US Marine Corps infantry Officer with 
4 decades of experience as a national security analyst, 
offers one of the most recent models of military 
revolutions which expands on and challenges aspects of 
the Knox and Murray model [21]. Hoffman focuses on 
what comes after the five revolutions within the Knox and 
Murray model through the lens of the Clausewitz trinity, 
considering how human-machine teaming, the end of the 
“heroic age” of the military, and automated systems might 
affect various aspects of war, social stability, and public 
sentiment toward policy [21]. He expands the Knox and 
Murray model to seven revolutions, with a more explicit 
emphasis on non-violent phenomena, such as ideological 
extremism [21]. A summary of the Hoffman model of 
military revolutions (and their key features) is included 
here:

## Page 13

Active Inference in Modeling Conflict, 2021 
 
11 
• Westphalian System  
o Revenue generation, banking and taxes, and 
the introduction of professional militaries 
• French Revolution 
o National mobilization and levy en masse 
• Industrial Revolution 
o Mass production, standardization, and large-
scale economic exploitation 
• World Wars 
o Combined arms, armored blitzkrieg, carriers, 
bombers, and jets 
• Nuclear Revolution 
o Nuclear 
weapons 
and 
intercontinental 
ballistic missiles 
• Information Revolution 
o Command and control, connectivity and 
global reach, imagery, and ideological levy en 
masse 
• Autonomous Revolution 
o Autonomous weapons, swarms of robotic 
vehicles, self-organizing defense systems, big 
data analytics, and deep-learning systems. 
[21] 
Generations of Warfare Framework 
In the late 1980s, William Lind and a collection of US Military officers 
from the US Army and Marine Corps presented what is now known as 
the “Generations of Warfare” (GW) framework in an article published 
in the Marine Corps Gazette [22]. It is notably similar to the military 
revolutions model both in terms of its intentions and structure. The 
GW framework is built on the notion of linear sequential development 
over time, marked by key inflection points driven by technology and 
ideas. The GW framework has arguably achieved broad use and has 
received a great deal of commentary and adaptation, for example the 
projection of a fifth generation of war (5GW) beyond the four initially

## Page 14

Active Inference in Modeling Conflict, 2021 
 
12 
described [23]. A summary of the initial conception of th e four 
generations of warfare is provided here: 
• First generation: Line and Column Tactics 
o Driven by technological changes 
o Operational Art practiced by individual commanders  
(e.g., Napoleon) 
o Reliance on indirect fire (e.g., artillery) 
• Second generation: Fire and Movement 
o Driven primarily by technological changes, but also by 
ideological changes 
o Operational art practiced by high-ranking officers 
o Reliance on massed firepower, and manpower 
• Third generation: Nonlinear Tactics 
o Driven primarily by ideological changes, but also 
technological changes 
o Operational art practiced by low-ranking officers (e.g., 
tank commanders) 
o Reliance on maneuvers and non-linear tactics 
• Fourth generation: Whole of Society 
o Driven primarily by ideological changes 
o Operational art practiced in small-teams and in the gray 
zone between military and civilian 
o Reliance on gray zone warfare (e.g., psychological and 
informational operations, targeting a society’s culture) 
[22] 
Gradients of Warfare 
The “gradients” of warfare model (xGW) proposed by 
Daniel Abbott is a reimagining of the generations and 
revolutions models of framing changes in warfare [23]. 
Although the gradient and generation are often used 
interchangeably, 
the 
gradient 
model 
abandons 
chronological development (generations) and instead 
describes movement along a single finite, abstract axis,

## Page 15

Active Inference in Modeling Conflict, 2021 
 
13 
representing an arbitrary gradient of diffusion or 
concentration related to a particular conflict [23]. The 
gradients described by Abbott [23] are summarized below: 
• The Zeroth Gradient 
o Genocide and all-of-society warfare (e.g., ant 
colonies, ethnic cleansings) 
• The First Gradient 
o Physical concentration of resources (e.g., 
chimpanzee border patrols, medieval warfare) 
o Placing troops in the same place at the same 
time 
• The Second Gradient 
o Concentration of effort (e.g., coordinated fire) 
o Directing effort toward the same place at the 
same time 
• The Third Gradient 
o Coordination and concentration of operational 
art (e.g., blitzkrieg) 
• The Fourth Gradient 
o Focus on “degrading the opponent into an 
earlier generation of warfare” 
o Decentralized gray zone conflict 
• The Fifth Gradient 
o Coordination and concentration of ideology 
[23] 
Kohalyk’s Projection of xGW 
An interesting result of abandoning chronology as a 
primary axis and replacing it with axes related to abstract 
state features is that Abbot’s gradients may be “projected” 
onto other models to yield additional insights from 
existing models. For example, Kohalyk, based on Abbott’s 
assertions about the nature of the gradients, projects the 
gradients onto John Boyd’s famous OODA (observe,

## Page 16

Active Inference in Modeling Conflict, 2021 
 
14 
orient, decide, act) loop (see Figure 1) [24,25]. This 
exercise demonstrates that Abbot’s gradients can be 
repurposed, not just to describe levels of diffusion, but 
also the basis for that diffusion and the changes to that  
basis over time, providing a more stable view on the 
generations of warfare model that gradients were 
originally intended to replace [24]. This projection can be 
summarized as follows: 
• The First Gradient 
o “Characterized by prioritizing the transition 
between decision and action” 
• The Second Gradient 
o “Characterized 
by 
prioritizing 
the 
gap 
between orientation and decision” 
• The Third Gradient 
o “Characterized by prioritizing the disruption 
of orientation” 
• The Fourth Gradient 
o “Characterized 
by 
prioritizing 
the 
gap 
between observation and orientation” 
• The Fifth Gradient 
o “Prioritization 
of 
the 
disruption 
of 
observation itself” 
Figure 1. Abbott’s Gradients of Warfare projected onto John Boyd’s 
OODA loop. Adapted from [25]. 0GW not included in original figure.

## Page 17

Active Inference in Modeling Conflict, 2021 
 
15 
Linn’s Model of Strategic Narrative 
Breaking rank from chronologically or technology driven models of 
war, Linn offers a heuristic model of approaches to modeling war and 
the narratives which accompany those approaches. He proposes three 
general, abstract narratives encoded into the theoretical groups which 
would hold them: guardians, heroes, and managers [26]. Guardians are 
those who model war primarily as a science that is “subject to laws and 
principles” which can offer the means to predict the consequences of 
specific policies. Heroes model war primarily as an art, dependent upon 
military genius, experience and training, morale, and discipline. The 
final group, managers, model war as a “logical outgrowth” of politics 
and economics, dependent on logistics, mobilization of resources, 
standardized and effective equipment, and the assignment of well -
educated professionals. 
Quantitative Models of Conflict 
The term quantitative models of conflict is used here to describe the 
models of conflict which sit in clear separation from qualitative and 
narrative models, attempting to frame conflict in terms of formalized 
mathematics and computational structure. Several of these models are 
summarized here. 
Lanchester Models 
The Lanchester model is likely the earliest substantial quantitative 
model of warfare, being introduced in the early 1900s in the book 
Aircraft in Warfare: The Dawn of the Fourth Arm by Frederick Lanchester 
[27]. Lanchester introduced a series of quantitative rules, such as the 
N-squared law (“the measure of the total of fighting strength of a force 
will be the square of the sum of the square roots of the strengths of its 
individual units”), and differential equations to describe concepts like 
attritional dynamics and predict the likelihood of outcomes of 
engagements [27]. In addition, he used geometry to illustrate the 
resulting models of these equations in numerous examples across air, 
naval, and land warfare with consideration for various kinds o f 
armament [27]. Though introduced in the early 20th Century, 
Lanchester models are still being adapted today to represent things such 
as force ratios and information importance in guerilla warfare and 
insurgencies [28] despite the model’s shortcomings in describing real-
world dynamics [29].

## Page 18

Active Inference in Modeling Conflict, 2021 
 
16 
Fault Tree Analysis 
Fault tree analysis was developed to decompose potential failure states 
of a system or operation into subevents to better understand potential 
for cascading failures [30]. Each of these subevents can be given 
probabilities and relationships with other events, allowing risk analysts 
to calculate the probability of compound events and specific outcomes 
[30,31]. Using fault tree analysis, conflicts can be modeled in terms of 
various system states and their likelihood to trigger undesired system 
states or cause cascading failures via complex threat surfaces [1].  
Effects Based Operations 
Effects Based Operations (EBO) planning, is a form of course of action 
planning for military operations which is characterized by its use of 
Bayesian graphical models (“Bayes nets”) and models of complex 
systems [32]. While EBO is primarily a planning tool, it embraces a 
systems warfare approach by modeling an area of operations as a series 
of components which may be acted on to generate effects which cascade 
throughout the system. As a consequence of this approach, conflict 
becomes more general and less weighted with connotations of violence, 
instead being better described as friction or disruption, making it 
particularly useful for planning within and describing gray zone and 
narrative warfare [32,33]. 
DoDAF 
The US Department of Defense Architecture Framework (DoDAF) and 
its variants are “military architecture” frameworks intended to improve 
planning, procurement, and the deployment of various military systems 
[34,35]. While it is not intended to model conflict explicitly, the 
DoDAF system incidentally generates a model of conflict consistent 
with Linn’s conception of a “Manager’s” view of war [26] as a 
consequence of its modeling of future military needs. Under this view, 
various kinds of conflict can be described and analyzed by modeling 
the resources, sub-organizations, missions, and logistics of a military 
organization itself as a system-of-systems interacting with constraints 
and limitations (e.g., adversaries and their military organization).  
Systems Warfare 
Western network-centric warfare, Chinese systems confrontation 
warfare, and the Russian Gerasimov Doctrine are all examples of 
modern updates to military doctrine necessitated by the rise of gray 
zone warfare. Each focuses on permanent conflict, a fusion of hard and

## Page 19

Active Inference in Modeling Conflict, 2021 
 
17 
soft power across numerous domains, and describing war in terms of 
whole-of-system conflict over networks, such as those of influence 
(media) and exchange (supply chains and economies) [36–40]. While the 
details and documentation of modeling approaches for describing 
systems of interest within Chinese and Russian doctrine are not easily 
available [38], those used within network-centric warfare are extensive 
and often make use of agent-based, Bayesian, and complex system-of-
systems modeling methodologies to describe and analyze the structure 
and risks of abstract conflicts [40–42]. 
Models of Conflict Information Flows and 
Decision-Making 
The preceding categories of conflict models focused on the historical 
and qualitative (Narrative Models of Conflict) and the quantitative and 
data-driven (Quantitative Models of Conflict). In this section, we 
describe models that have been developed with a behavioral focus, 
whether they take a qualitative or quantitative approach. These models 
of information flows are not just explanatory - they are used in national 
militaries to inform design and decision-making and as such, they have 
real impacts and need to accurately and appropriately describe systems 
[39]. Many information flow and decision-making models have been 
considered for use within national militaries, such as Shewhart’s Plan -
Do-Check-Act (PDCA) model [43], Wohl’s Stimulus-Hypothesis-
Option-Response (SHOR) model [43,44], and the Endsley model 
[43,45] (see Figure 2). However, two models in particular, the Observe -
Orient-Decide-Act and Rumsfeld’s Triad of “Knowns,” have seen 
broader adoption and adaptation than others. Here, these two models 
are summarized. 
Observe–Orient–Decide–Act (OODA) Model 
The Observe-Orient-Decide-Act loop (OODA) model is among the 
most familiar and commonly used decision-making frameworks in 
modern times and is used “ubiquitously throughout the branch -specific 
and Joint doctrinal publications of the US Military” [46]. While the 
OODA loop is now contained within a scholarly corpus, its creator, 
John Boyd, never directly published on the topic, instead choosing to 
share the ideas behind OODA primarily through his presentations [46 –
49].  
The OODA loop was originally designed to help describe and inform 
real-time decision making by pilots, wherein a “pilot observes the 
variable and surrounding, orients the aircraft to an advantageous

## Page 20

Active Inference in Modeling Conflict, 2021 
 
18 
position… [decides] the following course of actions in order to engage” 
and then acts them out (see Figure 3) [50]. The generalizability and 
simplicity of this “loop” of factors in decision making led it to enjoy 
reasonably high levels of adoption, not just in the military, but also in 
areas such as business and healthcare [50]. However, this simplicity, 
paired with the lack of published clarifications and formalizations by 
Boyd, means that it is constantly being reinvented, reconsidered, 
reinterpreted, and modified to fit various situations leaving it lacking 
consistent definition and coherent development as a model that could 
further enhance its usefulness [43,50,51]. 
Rumsfeld Matrix of Knowing 
The Rumsfeld “Matrix” [52], “Paradox” [53], or “Quadrants” of 
knowing, was not initially formally proposed as a framewo rk for action 
and perception, but rather was merely a response provided by Secretary 
of Defense Donald Rumsfeld to a question asked about the lack of 
evidence of weapons of mass destruction in Iraq: 
“Reports that say something hasn’t happened are always 
interesting to me, because as we know, there are known-
knowns; there are things we know we know. We also know 
there are known-unknowns; that is to say we know there 
are some things we do not know. But there are also 
unknown-unknowns – the ones we don't know we don't 
know. And if one looks throughout the history of our 
country and other free countries, it is the latter category 
that tend to be the difficult ones.” 
[54] 
Though Rumsfeld only offered 3 informational states in the direct 
quotation, the suggestion of known-knowns, known-unknowns, and 
unknown-unknowns implies a combinatorial requirement for an 
additional fourth state: unknown-knowns, which has led this framework 
to be referred to as “Rumsfeld’s Matrix” [55]. Interestingly, many 
analyses ignore the presence of this 4th implied category [53,56–59].  
While other decision making and information flow frameworks 
discussed above focus on linear steps in the decision making process 
itself, the Rumsfeld Matrix of known-knowns, known-unknowns, 
unknown-unknowns, and unknown-knowns is different. The matrix is 
invoked to help describe the static abstract information spaces and 
voids that decision makers must navigate and explore (see Figure 3) 
with gradients of greater or lesser information and lack of awareness 
of degrees of ignorance - a double hurdle to situational awareness.

## Page 21

Active Inference in Modeling Conflict, 2021 
 
19 
Rumsfeld’s strategic categorization has since been adopted as a 
rhetorical framework for considering information gathering and 
prioritizations in planning and decision making in the military and 
elsewhere. The Rumsfeld Matrix, like John Boyd’s OODA loop, enjoys 
an informal rhetorical ubiquity - it is a popular reference across other 
fields, such as in science [59,60] and energy infrastructure [52].  
Figure 2. Various Decision-Making Models. Plan-Do-Check-Act Model from [43], 
Stimulus-Hypothesis-Option-Response from [44], Endsley Model from [45]

## Page 22

Active Inference in Modeling Conflict, 2021 
 
20 
Essential Features and Limitations of Past Conflict 
Models 
This brief survey of conflict-oriented models used within military 
contexts reveals an arc of abstraction across time from simple pattern 
collection, to formalisms, and finally toward generalized models. The 
survey also reveals a persistent challenge through time of the problems 
of change management in the conduct of warfare, i.e., of inconsistency 
and adjustment to new paradigms and changed historical circumstances. 
While each of the models described had an important place in the 
Figure 3. OODA and Rumsfeld Quadrants

## Page 23

Active Inference in Modeling Conflict, 2021 
 
21 
history of the development of theory and within military scholarship, 
each also suffers from weaknesses which prevent it from offering 
sufficiently comprehensive predictive and descriptive power in the gray 
zone conflicts of the 21st century and beyond. However, each prior 
model has strengths and offers insights which should be captured by 
new models. Below, we consider some key insights to be preserved and 
brought forward from previous models. These insights will inform the 
AIC model introduced herein. 
Changing Expression of Conflict 
Numerous models show signs of aging as the expression 
of conflict changes. As a first example, aspects of 
Clausewitz’s trinity are still quoted as a basis for informing 
doctrine at the highest levels of the US Armed Forces [17] 
in a way which is consistent with Clausewitz’s view of his 
theories as a “basis for study, not as doctrine” [15]. 
However, even when used in a limited way as a basis of 
study or theory, it still faces serious challenges in 
capturing significant aspects of modern conflict. While  
some argue many aspects of the trinity may be applied 
through analogy to asymmetric and low intensity conflict, 
the model may have to be somewhat contorted to be 
applied in many conflict scenarios; for example, in the 
conflicts between the Medellin Cartel and the Colombian 
Government [15]. Further, Clausewitz’s trinity simply 
cannot explicitly or sufficiently describe the categories of 
conflict most relevant to modern organizations, such as 
narrative warfare and terrorism where many actors may be 
individuals motivated by ideology [14,32]. Even within 
defenses of the trinity model and of Clausewitz we find 
the suggestion that attempting to torture the model into 
explicitly describing aspects of modern conflict may be 
“profoundly confused” [61] and stem from the likelihood 
that Clausewitz “has been more often quoted than read 
and understood” [14]. While the underlying components 
of reason, genius or strategy, and passion are still valid, 
the central tension, or as Clausewitz described it, the 
“balance between these three tendencies”, will no longer 
express itself in the same way and may need to be paired 
with other models in order to continue to provide value 
and insight [21].  
While the Clausewitz trinity has seemingly received the 
most attention in terms of adaptation for the changing

## Page 24

Active Inference in Modeling Conflict, 2021 
 
22 
expression of war, approaches such as Lanchester models 
and Generations of Warfare, have also seen numerous 
adaptations in order to fit new paradigms. Replacements, 
such as models of conflict within the purview of network -
centric warfare, fare far better in describing these new 
paradigms but might make a polemologist or military 
historian wonder if they describe old ones well. Even with 
the Generations and Revolutions of Warfare models, 
which are intended to capture the development of war 
historically, may unfortunately create a unidimensional or 
linear view of war as consistently developing in 
sophistication. Further, they place all conflict prior to the 
first millennium as “precursor activities'', creating a 
paradigm of study and thought similar to that which is 
found in “traditional Western historiography, in which all 
of prehistory — the bulk of the history of our species on 
earth — [is] consigned as an afterthought on the far left 
side of any historical diagram — the historical terra 
incognita before classical antiquity” [62].  
It is important to consider how models built for new 
expressions of war might represent old ones given what is 
suggested by Abbott’s Gradients of War: that the 
expression of war may degrade in sophistication rather 
than increase linearly. There is a need to address how we 
represent conflicts within abstract space in order to 
capture not only the essence of previous and current 
expressions of warfare, but also to help project and 
consider what may come next. 
Limited Interoperability 
The value of a model of a system might be derived not just 
from how well it handles updates to information about 
that system, but also from how well it interfaces with other 
models. How does a system reflecting one model come to 
“know” what is already “known” to a different model? For 
example, 
it 
would 
offer 
tremendous 
value 
via 
interoperability to be able to project or map models onto 
each other. However, among all the models considered 
above, only limited capacity for backwards- or forwards-
compatibility was found (the exception proving the rule 
was the mapping between OODA and the Gradients of 
Warfare in Figure 1). Though some models seem quite 
general, they have poor interoperability with others, for

## Page 25

Active Inference in Modeling Conflict, 2021 
 
23 
example, the value of computational systems such as those 
within EBO and Lanchester models is siloed from the 
insights within information flow and decision-making 
models. Though some work has been done elsewhere to 
map heuristics and narrative models to computational 
frameworks in gray zone and narrative warfare through the 
use of “pattern languages” [63], or collections of practice 
and risk heuristics which can be layered into EBO-like 
frameworks, it isn’t apparent that any substantial work has 
been done to generalize this approach to conflict in 
general [32].  
Separate from attempts to map relationships among 
narrative 
models 
and 
their 
computational 
and 
informational counterparts, there is also significant 
dissonance within each of these categories. For example, 
Lanchester equations, by merit of their structure, cannot 
easily interface with EBO or systems warfare models. 
Further, within narrative models we find rampant 
disagreement on how to describe conflict in terms of 
priority. In addition, within informational models it is 
unclear how models like OODA can scale from local or 
single-actor tactical decision-making to strategic or multi-
actor decision-making with adversaries in-the-loop as 
EBO or systems warfare models would indicate may be 
required. Inconsistencies or incompatibilities within and 
among models hinders the ability of applied composite 
models to provide superior insights into the origins and 
operations of human conflict.  
There is a need for a computational integrative framework 
that connects tactical (micro) and strategic (macro) 
timescales, and builds on the strengths of narrative, 
quantitative, informational, and decision-making focused 
(meso) models. In the next sections, trends in the 
understanding of human interactions generally are brought 
to the challenges of analyzing human conflict, including 
war, and the synthesis introduces multiple new metrics of 
system performance from previously neglected contiguous 
domains of human behavior from which a richer, and more 
extensible, computational model of human conflict and 
war emerges.

## Page 26

Active Inference in Modeling Conflict, 2021 
 
24 
Generalization 
In addition to being able to handle updates to information 
and interface well with other models about a particular 
system, the potential value of a model might be further 
discerned based on how faithfully it is able to describe and 
integrate with other systems with one or more similar 
attributes. The history of conflict modeling, as illustrated 
in the summary of warfare literature above, reflects an 
ever-increasing awareness and integration of variables 
from the studies of interactions in conflict beyond those 
traditionally classified as “war.” As humans migrate their 
interactions from physical space to abstract online 
“information” space, the potential for integration of other 
knowledge about managing interactions and conflict in 
non-warfare contexts becomes increasingly relevant - and 
increasingly possible.  
In fact, as the human species migrates an ever increasing 
portion of its interactions from physical interaction 
pathways to information-rich digital and online networks, 
the nature of conflict, including war as conflict, is 
changing. In traditional interactions and conflicts, the 
physical landscape and kinetic actions of stakeholders had 
the greatest influence on the models used to study those 
systems. In digital online information interactions, the 
“landscapes” are not physical, but instead are conceptual, 
narrative, and even memetic [64]. At one level, conceptual 
conflict might be seen as more amenable to dissipation 
without resort to irreversible destruction of rivalrous 
physical objects of value. On another level, abstract spaces 
lend 
themselves 
to 
myriad 
different 
simultaneous 
characterizations, each of which can provide pathways to 
conflict resolution, together or in combinations.  
In the past, conflict might be explained with reference to 
people speaking different languages or seeking control of 
rivalrous physical territories. Increasingly, however, 
conflict can be described with reference to different 
paradigms, argots (trade languages), and risk concerns. 
Much as prior conflict might arise between speakers of 
different languages, so too might future conflict be 
analyzed as conflict between and among the different 
languages, 
paradigms 
and 
interactions 
patterns 
of

## Page 27

Active Inference in Modeling Conflict, 2021 
 
25 
business, operating, legal, technical and social domains 
(BOLTS).  
Since war is a subcategory of human conflict, BOLTS-
based parsing can also help to introduce potential 
pathways to integration for models of nation state level 
conflict, including war. As the proportion of of conflicts 
between and among people, organizations and nations 
becomes less focused on violent physical conflict, it is 
increasingly better described as occurring over surfaces 
characterized using business [65,66], operations [67], legal 
[68,69], technical [67,70], and social [32,71] (BOLTS) 
components. As the case for traditional battlefields, the 
ability for modern models to capture both violent and 
nonviolent aspects of conflict at varied scales of 
organization in myriad contexts, digital and physical, 
becomes existentially important. BOLTS has become an 
approach to analyze this continuation of (information) 
warfare by other means. 
While the popular models of conflict described thus far 
tend to focus on describing and providing insight into 
violent conflict, outside of the warfare-oriented corpus 
there is fortunately a rich history of models developed in 
an effort to understand and address non-violent, non-
physical, or indirect conflict [72,73]. These traditional 
models of human conflict management are nonetheless 
non-traditional models of warfare. As warfare is migrating 
from physical to informational domains these non-
traditional models present themselves as candidates for 
integration with traditional models of warfare.  
Unfortunately, at first glance,these non-warfare models of 
conflict tend to appear to be focused on interpersonal and 
intragroup conflict, rather than inter-organizational or 
violent conflict, and some may explicitly avoid discussion 
of these topics [72,73]. However, within this corpus of 
non-warfare conflict work, concepts have been developed 
that can be helpfully brought to the study of war. For 
example, non-warfare conflict research includes research 
on negotiation and intragroup organizational conflict 
presenting concepts which are ripe for generalization to 
interorganizational business and legal contexts [73–75], 
research on task and process conflict directly applicable 
to understanding larger scale operations frictions [73], and

## Page 28

Active Inference in Modeling Conflict, 2021 
 
26 
research on relational and diversity conflict which has 
already been applied to better understanding cultural and 
social frictions [72,73]. 
Other potentially useful non-warfare models of human 
conflict and its management include those models that 
analyze conflicts within a “commons”, which has its own 
storied computational and narrative corpus. Research on 
commons management focuses on conflicts which can 
arise in markets (both abstract and real) and the access to 
resources in which varied groups and actors have 
individual interests but collective ownership or stake 
[76,77]. For example, the oceans, the polar regions, the 
atmosphere, outer space, and non-earth heavenly bodies, 
are beyond the direct control of any nation, but provide 
resources and spaces in which nation states, and their 
resident citizens and companies, increasingly interact. In 
those spaces, conflicts of interests among stakeholders are 
bound to arise as competition for resources and conflicts 
of interactions emerge.  
Elinor Ostrom won the Nobel Prize in Economic Sciences 
in 2009 [78] for her work in describing co-management 
regimes for addressing conflict in historical settings such 
as the conflicts that arise in the context of shared grazing 
and forestry resources, fisheries, and riparian (water) 
rights. Her work has been instrumental in the international 
management 
of 
fisheries 
and 
other 
resources 
in 
international waters, and for models of managing both 
outer space and knowledge space as well. Hess and 
Ostrom, in their book, Understanding Knowledge as a 
Commons [79] lay out eight principles for “robust, long -
enduring, common-pool resource institutions”, which are: 
• Clearly defined boundaries 
• Rules that are well matched to local needs and 
conditions 
• Individuals affected by these rules can participate 
in their modification 
• The right of community members to devise their 
own rules is respected by external authorities 
• A system for self-monitoring members’ behavior 
has been established

## Page 29

Active Inference in Modeling Conflict, 2021 
 
27 
• A graduated system of sanctions is present 
• Community members have access to low-cost 
conflict-resolution mechanisms 
• Nested enterprises - the “appropriation, provision, 
monitoring and sanctioning, conflict resolution, 
and other governance activities” are organized in a 
“nested structure with multiple layers of activities”.  
To help communicate the impact of these principles, Hess 
and Ostrom present the “Institutional Analysis and 
Development” (IAD) framework (see Figure 4). This 
framework presents a map of the relevant variables to the 
expression of friction, or conflict, within what it calls the 
“Action Arena” and represents a key example of a model 
comprised of elements which are generalizable to a great 
number of kinds of non-violent conflict. In addition, it 
makes use of narrative models regarding common 
“patterns of interaction”, such as “freeriding or misuse”, 
which can be layered into the model with probabilities and 
expectations about outcome, offering implications for 
how narrative models and pattern collections may be 
generalized to interface better with computational models. 
Figure 4. Institutional Analysis and Development Framework, modified 
from [79]. Biophysical characteristics refer to ideas, artifacts, and 
facilities, the relevant factors which relate to the physical or quasi-physical
affordances, boundaries, capacities, and limitations of a particular 
commons. The attributes of the community, refer not just to measurable 
qualities of the community, but also to those which comprise it, such as 
users, consumers, providers, and policymakers. Rules in use refer to 
administrative procedures, legislation, and contracts, as well as other 
activities considered to be pro forma even where they may not be codified 
or observable.

## Page 30

Active Inference in Modeling Conflict, 2021 
 
28 
With this discussion about models of warfare above, there appears to 
be a need to account for new frameworks that encompass modern 
expressions of conflict, are interoperable across domains, and 
generalize well enough to encompass peaceful and rapidly -changing 
times as well as classical forms of conflict and related operations other 
than war (OOTW). An open challenge is for a computational model to 
capture the value and insights provided by various forms of previous 
narrative, quantitative, and information flow models of conflict. In the 
following sections we address this need by proposing a framework 
based on Active Inference. Active Inference is a framework arising 
from cognitive science, which has had demonstrable value in unifying 
certain aspects of cognition and sensemaking, and which may be used 
both computationally and qualitatively at different scales (e.g., single 
agent or multi-agent) [80–82]. The following sections present an 
overview of Active Inference, followed by its application towards the 
domain of conflict – the Active Inference Conflict (AIC) model. 
Active Inference Conflict Model 
Here we propose a framework for modeling modern multiscale conflict, 
based upon an application of Active Inference (ActInf). ActInf is a 
behavioral modeling framework that integrates perception, cognition, 
and strategic action under a common currency – the reduction of 
expected free energy. As discussed below, expected free energy has 
several different compatible phrasings which facilitate its use in decision 
support in different systems and situations. Across these formal 
phrasings of free energy, a commonality is the emphasis on selecting 
actions that finesse both the epistemic (knowledge-oriented) and 
pragmatic (utility- or reward-oriented) aspects of action. Broadly, ActInf 
can be considered an approach that builds on quantitative approaches to 
action (e.g., cybernetics and control theory) with modern insights from 
cognitive sciences [83,84]. This action-oriented view casts the active 
sensing of systems as fundamentally about reduction of uncertainty. The 
sensemaking process goes wrong when inappropriate uncertainty-
reducing behaviors are implemented, or the variability of the area of 
operations is too variable to be tracked effectively.  
The Active Inference Conflict (AIC) model is an approach which unifies 
some aspects of previous models of conflict, and generalizes conflict in 
order to help capture business, operations, legal, technical, and social 
aspects relevant to modern gray zone warfare. Additionally, the AIC 
model has sufficient flexibility to be used both qualitatively or 
quantitatively across different timescales (e.g., tactical, strategic), 
structural scales (e.g., individuals, organizations, communities, and 
states), domains, and scenarios. Recently it has been suggested that

## Page 31

Active Inference in Modeling Conflict, 2021 
 
29 
autoethnographic organizational approaches (e.g., reflection upon one’s 
own experiences and surroundings) provide an amenable on-ramp to the 
ActInf framework [85]. Multiple informal and technical introductions to 
ActInf and the broader Free Energy Principle exist [81,86–90], here we 
introduce some of the salient features and descriptions of key terms 
within the ActInf framework which predisposes it towards effective 
application to the domain of conflict and for use within AIC. 
From a military science perspective, AIC provides a bridge between 
single-agent real-time tactical decision-making models (such as OODA), 
and broader strategic analyses (such as those provided by the GW 
framework). As ActInf itself is a development on Bayesian graphical 
modeling to accommodate multi-level cognitive processes, the AIC 
model can be seen as the integration of this ActInf framework with other 
key existing models of conflict and models of cognition more broadly. 
Due to its descriptive bottom-up modeling approach, AIC also provides 
an avenue for integrating the analysis of military, non-military, and non-
kinetic models of conflict (as well as cooperation, and other categories 
of interactions). Below, we provide a primer on ActInf with a focus on 
how key ideas are applied in the AIC model. Figure 5 summarizes the 
scope of AIC and Table 1 provides a map for the territory we explore in 
the following sections (the core terms and features of ActInf as deployed 
in AIC). 
 
Figure 5. Scope of Active Inference Conflict (AIC) model along the dimensions of 
qualitative to quantitative (X-axis) and tactical to strategic scale (Y-axis). From the top-
right and going clockwise: Lanchester models, DoDAF (Department of Defense 
Architecture Framework), EBO (Effects Based Operations), OODA (Observe-Orient-
Decide-Act), the Rumsfeld Matrix, and Generations of Warfare (GW) model.

## Page 32

Active Inference in Modeling Conflict, 2021 
 
30 
Table 1. Core terms in ActInf (left column) 
ActInf Core 
Terms 
Usage at Tactical 
scale in AIC model 
Usage at Strategic 
scale in AIC model 
Tactical and Strategic 
scale in AIC model 
Entity  
Human, human – 
with tech in the 
loop, squads, teams 
State or non-state 
group 
Larger entities are 
made up of smaller 
entities 
Generative 
Model 
Short-term 
expectations for a 
given scenario, 
enacted & 
embodied by a 
tactical agent 
Long-term 
expectation at a 
diplomatic or 
geopolitical level, 
of a strategic agent 
Strategic-level 
generative models 
constrain/enable the 
function of tactical-
level models.  
Perception 
& Action 
Perception: Bodily 
senses and 
(meta)cognition. 
Action: Physical 
movement including 
tools 
Perception: 
Informational 
ingress, 
observations from 
e.g., markets, 
environment 
Action: 
Communications, 
operations orders 
Scales can interact and 
influence each other 
through Action (one 
scale/system’s action 
is another’s 
Perception)  
Affordances 
& Policy 
Selection 
Decision of which 
button to press, 
what to say, or 
which route to take 
Decision of which 
sanctions to apply, 
communications to 
release.  
Large scale outcomes 
(movement of a 
legion) are jointly 
influenced by top-
down and bottom-up 
implications and 
decisions 
Expected 
Free Energy 
(FE) 
Implicit or explicit 
prediction over a 
time horizon of the 
uncertainty 
associated with a 
given sequence of 
actions 
Implicit or explicit 
prediction over a 
time horizon of 
the uncertainty 
associated with a 
given sequence of 
actions 
Systems driven by 
tactical minimization 
of FE may not achieve 
strategic aims. 
Strategic minimization 
of FE may entail novel 
regimes for tactical 
elements (e.g., waking 
up early, or 
experiencing surprise) 
Action-
Perception 
Loop  
Continuous flow of 
bodily sensory 
information and 
personal physical 
movements  
Continuous flow 
of 
organizational/inf
ormational inputs 
and outputs 
Action loops of 
tactical entities are 
faster/smaller nested 
systems within 
strategic entities (like 
players on a soccer 
team)

## Page 33

Active Inference in Modeling Conflict, 2021 
 
31 
Active Inference Overview, Terms, and Features 
There are several core features and relevant terms from ActInf that are 
necessary in communicating the AIC model (Table 1). Here we provide 
an overview of ActInf topics and terms, with an eye towards how the 
concept will be applied in the AIC model and the general implications 
for the term’s quantitative and qualitative use. 
ActInf Terms 
Here, the terms necessary for communicating the AIC model are 
described. 
ActInf Entity 
An ActInf entity is the minimal system description or 
model that is partitioned off as a separate (but interacting) 
thing from its environment or niche. The “thing-ness” of 
the system is specified by how relevant system variables 
are partitioned into several kinds of states. The scale of 
the entity might represent, for simulation and modeling 
purposes, anything from individuals to communities [91–
93].  
Some 
presentations 
and 
applications 
of 
ActInf 
differentiate two categories of Entities: “Mere” and 
“Adaptive” [94,95]. A “Mere” ActInf entity is one that 
passively synchronizes or reacts to external stimuli or 
causes. Relevant Mere ActInf entities in a model of 
conflict might include inanimate objects, smart contacts 
or blockchains, or any system with a well-defined, passive, 
or completely understood input-output relationship. In 
contrast an “Adaptive” ActInf entity is one that interacts 
with 
its 
environment 
in 
an 
embodied, 
agentic, 
anticipatory, cybernetic, and anti-dissipative fashion. 
Relevant Adaptive Entities in a model of conflict might 
include 
humans, 
teams, 
organizations, 
companies, 
countries, and non-state groups.  
ActInf entities can be considered “generic” patterns that 
partition the statistical dependencies of agents into 
internal, external, and blanket (incoming: sense, and 
outgoing: action) states. This characterization of a generic 
entity type is useful for several reasons:

## Page 34

Active Inference in Modeling Conflict, 2021 
 
32 
• ActInf entities have tractable interfaces for lateral 
interaction as well as nesting within other ActInf 
entities, 
allowing 
for 
modeling 
of 
complex 
heterarchical 
synthetic 
intelligence, 
or 
macro-
cognition and organizational behavior [3,80,96].  
• So long as ActInf entities have action affordances 
which can interface with external entities and sense 
affordances which interface with external stimulus, 
the representation of their internal state and policies 
can be modified in any way appropriate for the nature 
of that entity and the simulation or modeling task at 
hand.  
• Even without full quantitative integration, the 
process of framing a system in terms of its entities 
and nested entities can help illuminate its structure as 
exercise in system modeling and sensemaking [85].  
Generative model 
The generative model of an ActInf entity refers to the 
ongoing creation by internal states of expectations, for 
example the states that the organism or organization 
expects itself to be in. Entity actions are selected in order 
to reduce uncertainty about the realization of those 
expectations, 
as 
the 
generative 
model 
includes 
expectations over sense, action, internal, and external 
states. In application across systems, the imperative for 
behavior in ActInf entities is not the maximization of 
reward but rather the reduction of uncertainty [97]. 
Reduction of uncertainty is always in reference to a 
specific generative model possessed or enacted by a 
system of interest, be it an organism or organization 
[3,92].  
Perception & Action 
ActInf entities are continually engaged in perception and 
action. ActInf builds on the predictive processing, 
embodied cognitive frameworks, as well as other Bayesian 
and 
computational 
models 
of 
perception 
[98,99]. 
Perception is the ongoing process by which sensory 
observations are predicted or inferred by the generative 
model of an ActInf entity. Action refers to the enacted 
outcomes or outgoing statistical dependencies of the

## Page 35

Active Inference in Modeling Conflict, 2021 
 
33 
system, whether they are digital, social, financial, or 
physical.  
Affordances & Policy Selection 
Policy selection, or action selection, is the process by 
which the entity will (act as if they) decide upon a course 
of actions (a policy). For a body, the action states might 
refer to the exact angles of each joint, while the policy 
selection “to walk” could entail a complex sequence of 
changes to action states. The space of possible policies for 
an ActInf entity at a given time is known as their 
affordances (opportunities for action and interaction in 
the niche), drawing on the use of the term in ecological 
psychology [100]. Policy selection is carried out in light of 
a preferences over sensory observations (e.g., having a 
preference for warm temperatures over cold, and then 
acting to light a fire to reduce surprise about temperature). 
Thus policy selection is cast not in terms of finding highly -
rewarding states, but rather inferring which option from a 
given limited set of affordances is expected to lead to the 
lowest expected difference between expectations and 
experience (lowest expected “free energy”) through time, 
in terms of pragmatic (utility) value as well as epistemic 
(uncertainty-reducing) value. When these expectations and 
preferences are for rewarding states, then ActInf models 
can recapitulate behaviors found in other kinds of reward -
maximizers and reinforcement learners [81,97]. The 
selection of policy is in ActInf because entities can rapidly 
transition from utility-oriented behaviors to epistemic 
actions, as the flow of received information changes 
moment by moment. 
Expected Free Energy 
This expected free energy quantity used for policy 
selection, can be variously framed as achieving evidence 
for a successful self, resistance to dissipation, or the 
general reduction of uncertainty [98,101]. Several useful 
mathematical decompositions and equivalences exist for 
expected free energy, for example energy minus entropy 
(similar to Gibbs free energy), surprise plus informational 
divergence, accuracy minus complexity (as used in 
Bayesian statistics and machine learning) [102]. Classical 
decision-making constructs such as expected utility,

## Page 36

Active Inference in Modeling Conflict, 2021 
 
34 
informational foraging, risk-sensitive policy inference, 
and optimal control are special cases or derivations of 
more general formulations of ActInf entity behavior 
[81,103].  
Action-Perception Loop 
The action-perception loop in ActInf describes how 
Internal states (constituting the generative model of an 
entity) update in response to incoming sensory stimuli, 
and how actions (outgoing influences of the entity on the 
niche) define the outcoming interfaces of the systems. 
This problem of real-time control occurs in the domain of 
robotics, public health, command and control systems, and 
elsewhere. To model these heterogeneous yet structurally -
analogous scenarios with an ActInf entity, the entity can 
be modelled as a Partially Observable Markov Decision 
Process (POMDP) [88]. This POMDP specification is a 
Bayesian graphical model that lays out all variables 
required for minimal modeling of an ActInf agent (Figure 
6). At each timestep of the POMDP model, the entity 
receives new observations from the niche, updates the 
parameters of its internal generative model, performs 
policy selection, then enacts an action consistent with the 
selected policy. 
Figure 6. Partially Observable Markov Decision Process (POMDP) model
of an ActInf entity.

## Page 37

Active Inference in Modeling Conflict, 2021 
 
35 
ActInf Features 
The ActInf framework builds on the key terms towards several essential 
features. These components and generalized structures offer myriad 
affordances to researchers and analysts. Here we discuss several ActInf 
core components, placing them in the context of the AIC model as a 
formal model of interacting systems in conflict. 
Interactions with the Niche 
Niche refers broadly to the surroundings or context of an 
entity, be it biological, social, or informational. The niche 
is the unobserved generative process that passes sensory 
observations to the entity (akin to how the location of the 
sun is not directly observed, but is instead inferred from 
the angle and type of impinging photons) ActInf entities 
interface with their niche through sense (incoming stimuli) 
and action (outgoing effects) states. Entity actions can  
modify their niche, reflected by changes in how the states 
of the niche change through time (for example tightening 
a screw so it doesn’t wiggle in the future). This type of 
active 
co-construction 
between 
entities 
and 
their 
surroundings is known as niche construction or stigmergy 
[104]. This partitioning of the Internal, Action, and Sense 
states of the system of interest (the “particular states” 
[105]) entails that all features or data outside of the system 
of interest are external or niche states. We can consider 
the POMDP of the ActInf entity from Figure 5 as it 
interacts with its niche (Figure 6). The internal states of 
some system of interest can be modeled such that the 
external states provide observations (o t) to the entity, and 
the selection of policies (π) are upstream of the 
enactment of action state. 
Interacting Entities 
This same ActInf framework can apply whether the 
external states (external from the point of view or 
partitioning of the entity) are of a very different kind than 
the entity (e.g., an ant colony inferring a raincloud) or a 
similar kind (e.g., two humans and their mental models of 
each other). Interacting entities can select policies with 
long-term expectation of net-positive interactions (e.g., 
trusted interactions from a game theory perspective), and 
this framing can suggest the formation of new kinds of

## Page 38

Active Inference in Modeling Conflict, 2021 
 
36 
organizations. The concept of Thinking Through Other 
Minds (TTOM) describes how the internal general model 
includes each Entity’s own actions as well as the actions 
of the partner [106,107]. 
N-Dimensional Modeling of Abstract Space 
The advantage of a domain-flexible description of entities 
and their interactions, is that it facilitates the modeling of 
high-dimension interaction spaces, and detection of 
patterns 
across 
different 
interfaces 
or 
types 
of 
observations across BOLTS surfaces in way that may be 
Figure 7. ActInf entity interfacing with external states. At right, external
states are influenced by entity action states, and also external states may 
have endogenous dynamics. External states pass observations to internal 
states via entity sense states. Uncertainty in the flow of incoming sensory 
observation can be reduced through updating the internal model of the 
entity (learning) and action. 
Figure 8. Two ActInf entities A and B, interacting via a shared niche
(ecological, informational, or otherwise). The generative process of the 
niche is influenced by endogenous dynamics as well as actions from both 
entities.

## Page 39

Active Inference in Modeling Conflict, 2021 
 
37 
considered analogous to the integration of different kinds 
of neuroimaging data (fMRI, EEG, and MEG) in the 
Statistical Parametric Mapping (SPM) framework [108]. 
General ActInf modeling, along the lines of complex 
systems models described above, can capture the dynamics 
of classical cooperation/conflict situations as well as 
extend to model heterogeneous, unconventional, and yet-
unseen mechanisms and patterns. With the use of an event 
reporting framework, this ability to capture cooperation 
and conflict across myriad surfaces may help to identify 
not just yet-unseen mechanisms and patterns, but also 
difficult to detect opportunities for strategic attention and 
action [109,110]. 
Use of the AIC Model 
Here we build on fundamentals and recent applications of the ActInf 
framework to work towards new models of systems in managed and 
unmanaged conflict, cooperation, and every sort of human and 
institutional interaction in between. 
Entity Action Loop and Alignment with OODA 
To understand the cycle of inferences and actions entailed by each 
timestep for an ActInf entity, it is helpful to consider this ActInf model 
and POMDP specification alongside the stages of the OODA model 
(discussed above). In contrast with OODA, the ActInf framework 
provides a model for “regimes of attention” [111,112], niche 
modification, and long-range/predictive/anticipatory policy selection 
in deep or nested generative models.  
In both OODA and ActInf, the perception-cognition-action cycle is 
continuously unfolding, and can be thought of as beginning with the 
perception of new observations. Here we align ActInf terms and 
framings with the OODA sequence, with reference to Figure 9.  
• Observe: incoming observations (o) are received by sensors, 
sense organs, measuring tools, or other signal channels.  
• Orient: These observations are integrated with prior beliefs (D) 
about hidden causes or states of the world (s) through the 
bidirectional Bayesian mapping (e.g., constituting a generative 
model and recognition model) of the matrix (A) connecting 
observations to hidden states.

## Page 40

Active Inference in Modeling Conflict, 2021 
 
38 
• Decide: The updated Internal generative model of hidden states 
is used to perform inference on action, akin to other cybernetic 
or control theoretic framings. This selection of policy procee ds 
by the integration of preferences over outcomes (C) and 
constraints over action possibilities (E) in the calculation of 
expected free energy (G) in terms of pragmatic and epistemic 
value, as conditioned on different possible policies.  
• Act: Having selected the policy with the lowest expected free 
energy over the time frame of analysis, action states are updated.  
Unifying Quantitative and Formal Models of Conflict 
The AIC model does not replace prior quantitative models of conflict, 
it instead integrates them and offers a new medium for their expression 
(as well as a new environment for testing and formal development). For 
example, given that AIC can be nested into and applied in agent-based 
models [80,113,114], methods such as game theory matrices and 
Lanchester equations can be calculated at snapshots and be used to 
predict and project the outcomes of simulations and iterated games - 
as well as test other formalizations and counterfactuals. AIC isn’t 
limited to integration with agent-based models, it can also plausibly be 
nested into EBO and network-centric warfare graphs and planning 
cycles. Additionally, given that ActInf is a development on Ba yesian 
graphical network methodologies, AIC itself, without any integrations, 
can be represented as a graph akin to those found in other graph -based 
models. Further, it can extend these quantitative and formal approaches 
(EBO for cognitive effects) or provide a surface for interoperability 
Figure 9. Comparison of Action-Perception loops for ActInf and OODA entities

## Page 41

Active Inference in Modeling Conflict, 2021 
 
39 
between them (e.g., Lanchester variations for both infantry- and 
artillery-driven conflict within the same larger model) in myriad 
conflict settings. 
Moving Beyond Generations of Warfare 
The AIC model has the capacity to model structurally flexible, nested, 
and interacting entities and embedded decision-making processes. This 
allows for standardized and formal representation of conflict, whether 
it be between ant colonies or nation states, or between ant colonies and 
nation states. This formal representation allows n-dimensional 
measures of features and organizations within historical conflicts and 
thus opens the door to methodologies such as component factor 
analysis, which can allow for classifications and archetypes of c onflicts 
that aren’t limited by their place in history or by their placement on a 
single dimension. The analysis provided by AIC does not necessarily 
render previous narrative models of conflict classification obsolete - 
instead, it may offer opportunities to support and extend, and offer 
more insight into the similarities between these various models (for 
example returning to Flavius Vegetius Renatus’ aphorisms discussing 
estimation, uncertainty, and expectation). In this same vein, AIC can 
be used to generate new narrative models akin to Generations of 
Warfare, as war evolves and adapts along numerous axes - for example, 
along axes such as the relative distribution of decision-making or the 
growth of intelligence requirements. 
The decisions that are made today in this period of rapid transition will 
affect human conflict for many years. In this regard, AIC offers a 
potentially useful paradigm that can be extended, beyond the 
Generations of Warfare Model, into the past, anchoring it as a potential 
analytic tool to help predict efficient and effective strategies for future 
conflict analysis and resolution at multiple scales.  
Modeling and Discovering BOLTS Conflict 
As discussed, modern conflict is coming to be better characterized as 
occurring over surfaces with combinations of conflict measurement and 
risk mitigation structures drawn from multiple, previously -isolated 
domains. In this paper, we have applied the rhetorical mnemonic device 
“BOLTS” to invite simultaneous consideration of multiple separate 
paradigms, measurements, and languages to a given conflict use case. 
The analytical parsing encouraged by BOLTS is one of many possible 
mechanisms for such a multi-faceted analysis, and is useful because the 
individual B-O-L-T-S components are broadly familiar, and the 
conflicts among the silos (e.g., technological vs. legal considerations of

## Page 42

Active Inference in Modeling Conflict, 2021 
 
40 
data use, business vs. social goals of online social networks) are well 
known - even if they remain unresolved. The business, operations, 
legal, technical, and social components therefore provide a familiar 
backdrop against which AIC can be rendered more accessible. The 
visual integration of AIC with BOLTS is shown in Figure 10. Below, 
we note examples which emphasize each of these aspects and consider 
AIC’s use in these settings. 
Business 
Business 
and 
economic 
relationships 
have 
always 
influenced human interactions from the earliest agoras to 
today’s global online markets. The emphasis on metrics is 
driven by systems of risk mitigation and leverage 
associated with such business phenomena as production, 
resource accumulation, monetization, zero-trust trading, 
remote 
dealing, 
financialization, 
and 
myriad 
other 
“Business” concerns. Consider, for example, the many 
current structural global conflict surfaces that can be 
fruitfully 
analyzed 
as 
artifacts 
of 
the 
long 
term 
Figure 10. Two conflicting ActInf entities (A and B), a third entity outside of the direct 
conflict (C), and the abiotic niche interact via a BOLTS commons along specified 
interfaces.

## Page 43

Active Inference in Modeling Conflict, 2021 
 
41 
implications of once-admired cost cutting strategies (such 
as foreign production of domestic goods) associated with 
the historical transition from physical to information 
dependencies. For example, the domination of China in 
manufacturing (and the consequent dependencies of 
consumer societies such as the US) is a product of US 
companies seeking lower labor costs (and compliance with 
environmental, labor, and other domestic laws) in the past 
decades. The US became dependent on information and 
finance to maintain access to and control of such remote 
production activities, creating a period of relative order 
(in terms of environment and labor gains within the US), 
but deepening the dependencies on access to foreign labor 
and production apparatus - which creates disadvantages 
for the US in the event of conflict with China affecting 
trade. AIC can be applied to analyze, consider and identify 
developing price leverage within larger business and 
economic structures and their relationship to economic 
policy, or to help infer internal model or policy of 
adversaries (based on their policy “pings”), and can also 
be of use in identifying de facto adversaries that may not 
have coherent structure under the law or be otherwise be 
detectable through standard business or legal metrics (e.g., 
informal consortium-like entities, such as a category of 
businesses operating within a common niche, nascent 
cartels, mutually-dependent trading arrangements, online 
Distributed Autonomous Organization [DAO] structures). 
Looking at Business interactions through an AIC lens 
helps to reveal existing and potential interactions and their 
respective threats, vulnerabilities, and opportunities for 
new value creation, which will drive innovation in 
multilateral risk mitigating structures and in business 
entrepreneurship and innovation. 
Operations 
The concept of “Operations” in BOLTS overlaps with 
other BOLTS notions, but its separate consideration yields 
novel insights into conflict, particularly when brought 
together with the AIC model. Operations includes 
concepts such as supply chains, scaling of operations, 
organizational change management, operating efficiencies, 
human resources, and a host of other notions of human 
organizations that reflect attempts by humans to manage

## Page 44

Active Inference in Modeling Conflict, 2021 
 
42 
conflict for rule-driven behaviors across interactions at 
arbitrarily-large scales. In these contexts, the AIC model 
provides a coherent and comprehensive lens through 
which to analyze “operations in conflict.” For example, 
consider that many current “supply chain” related 
conflicts and challenges are a result, in part, of “just-in-
time” manufacturing, lean inventories, and other less-
capital-intensive forms of doing business ushered in by the 
enthusiasm for outsourcing in the mid-1980s, and 
accelerated 
by 
the 
“bricks-to-bits” 
commercial 
information revolution. Those trends have continued and 
been accelerated by the overall migration from physical to 
information-based interactions and transactions. Consider 
that there is a large and still growing set of operations 
protocols that eliminate the need for organizations to 
maintain large and expensive inventories. The continuing 
advances of the information revolution allow the 
virtualization of internal supply chains and of the 
provision of access to parts, ingredients and subassemblies 
when as needed further disintermediating previous supply 
chain interactions - which changes can lead to conflict. 
With respect to the labor element of operations, the 
“outsourcing” of labor to other, less regulated, countries 
is also a part of this cost-cutting effort. The modern 
expression of this outsourcing is found in innovations 
such as eBay, UBER, or Lyft where the value steps in the 
management and structure of inventory and service 
provision, routing, and delivery are becoming increasingly 
separated. AIC can be used to model the structure and 
distribution of decision-making processes both in BOLTS 
and traditional conflict arenas and developing points of 
affordance and access leverage in relation to policy. 
Further, it allows for the modeling of operational niche 
and the processes and protocols associated with managing 
the potential conflicts within a given niche. 
Legal 
The laws of physics are universal, but the laws of people 
are not. The technology of the Internet is based on 
physics, but the regulation of the internet is not based on 
the laws of physics. The result of all this is that the 
Internet has the potential to be deployed globally (and 
beyond) with technical standards, but the laws of the 195

## Page 45

Active Inference in Modeling Conflict, 2021 
 
43 
sovereign countries which are not globally standardized, 
creates conflict. Of course, it is not just the laws and 
regulations themselves that are in disputes, but also the 
interactions 
of 
the 
billions 
of 
individuals 
and 
organizations acting every hour of every day under such 
laws. The legal focus is fruitful in measuring and managing 
conflict since that is the intended effect of all legal 
systems. However, non-legal conflicts, such as political, 
economic, social, cultural, aesthetic, and other non-legal 
interactions, are beyond the reach of the risk mitigating 
help of legal systems. AIC applied with BOLTS can help 
to bridge the gap by bringing legal forms of conflict 
management into closer contact and interoperability with 
other BOLTS forms. In addition, legal confrontations in 
civil, criminal, and international disputes are in and of 
themselves conflicts which can be modeled by AIC. 
However, law is not just a source of conflict mitigation - 
it is increasingly a source of agenda-laden conflict 
engagement. Consider that beyond its role in helping to 
resolve individual conflicts, confrontations that apply law 
as a sword (and not just as a shield) are increasingly 
becoming a chosen avenue for conducting gray zone 
conflict and disruption between and among nation states 
and other entities. In the case of nation states, each of 
which as a sovereign can, by definition, create its own 
laws, legal warfare or “lawfare” [68,115,116] can be said 
to be composed of the development, amendment, and 
mobilization of “domestic and international laws” for 
geopolitical and military gain [117]. These forms of 
aggression are not typically characterized as “war,” but 
rather in such forms as trade negotiations, immigration 
policies, tax and financial regulations, bilateral treaty 
negotiations, regional pacts, cartel arrangements and other 
similar forms. The development of legal standards for the 
protection of statutory and contractual rights, the 
enforcement of legal duties and the reliance on predictable 
legal processes when exploited as a means of deterring, 
binding, and protecting individual and organizational 
interests’ actions in conflict with others is often difficult 
to detect in the churning and dynamic landscape of legal 
conflict. While legal notions such as “abuse of process” 
are intended to curb excessive and socially-destructive 
application of law as a sword, the subjective and 
contextual aspects of legal forms of conflict can obscure

## Page 46

Active Inference in Modeling Conflict, 2021 
 
44 
root causes and intentions of conflict in many cases. AIC, 
with its affordances for modeling and inferring internal 
models and policy, could be of use in classifying and 
detecting patterns of legal actions and consequent leverage 
within myriad interaction niches in order to more 
effectively measure, moderate, and manage legal conflict 
affordances at tactical, campaign or theater, and strategic 
levels.  
Technical 
Technical infrastructure, standards, and protocol are 
bounded by both computational and legal rules. The 
dynamic technical edge between these two areas is of 
particular importance for the future of conflict as human 
attention turns from a focus on data secrecy as a basis for 
conflict 
mitigation 
strategies, 
toward 
a 
focus 
on 
information integrity as a pathway to reducing information 
risk and interaction conflict.  
Data plus meaning yields information. Data security is 
necessary, but insufficient, to yield information reliability 
and distributed security. “Meaning” security is needed to 
complement data security to manage information network 
conflicts. While data security is the focus of technical 
features of the Internet and modern computer science, 
“meaning” security is the focus of law. Consider that all 
contracts and laws can be viewed as enforceable “stories” 
about the past, present, and future. When those stories are 
agreed upon and acted upon, they de-risk future 
interactions in ways that no one person can achieve by 
themselves 
(for 
example 
the 
laws 
and 
technical 
specifications that interact to de-risk otherwise hazardous 
situations such as highways and exchanges). Such 
enforceable stories are the way that humans achieve 
“meaning security.” Contracts and laws are all promises 
that we make to ourselves and others about the future, and 
the law is a mechanism to test our performance against 
those agreed upon parameters. In this way, it is not unlike 
technical 
specifications 
that 
set 
rules 
of 
general 
application for the technical performance and behaviors 
of engineered systems. 
As the desire for verifiable 
information 
integrity 
supersedes yesterday’s satisfaction with data security, the

## Page 47

Active Inference in Modeling Conflict, 2021 
 
45 
human and organizational components of systems will be 
increasingly recognized as critical system components, not 
just as users of systems. Legal and technical paradigms are 
tightly 
intertwined 
in 
information 
systems, 
where 
technical specifications help assure data system integrity 
and legal rules help assure meaning system integrity, with 
the result of enhanced information system integrity. Such 
“tools and rules” leveraging will be accelerated through 
application of AIC framings that will quickly reveal the 
potential alignments of such systems. Such analyses will 
be critical to the advancement of various information 
integrity structures to help manage the conflicts that are 
bound to arise through the introduction of such new 
distributed 
information 
integrity 
structures 
as 
decentralized management of intellectual property, the 
introduction 
of 
digital 
“twins”, 
smart 
contracts, 
computer-aided governance, and the progression of data 
privacy- and information integrity-related legal structures.  
Emerging interaction structures provide a sense of the 
challenges and opportunities that reveal themselves at the 
intersection of technical and legal interaction and conflict 
management use cases. Historically, notions of intellectual 
property law (involving copyright, patent, trademark, 
certification mark, and trade secret) have always blurred 
the boundaries between physical and intangible value of 
goods and services in commerce. In terms of decentralized 
management of intellectual property, consider that nation 
states and the Westphalian system are based on physical 
boundaries 
and 
borders, 
hence 
the 
exclusivity 
(rivalrousness) of ownership of real property (e.g., land). 
At its base, the Westphalian paradigm of enclosure and 
exclusive jurisdiction may be fundamentally inconsistent 
with the infinite duplication that is possible with 
information. This may mean torturing new technical 
expressions of intellectual property to fit this previous 
legal, business, and operations paradigms, for example 
through primarily interpreting and designing non-fungible 
tokens (NFTs) as an expression of ownership of a given 
represented object (e.g., a particular artistic image), or by 
developing 
new 
systems 
which 
acknowledge 
these 
changes, for example through primarily interpreting and 
designing NFTs as an expression of rights, stake, and 
affordances related to some given represented object. In 
terms of digital twins, the notion of the identity

## Page 48

Active Inference in Modeling Conflict, 2021 
 
46 
entanglement between the referent human and their digital 
extension, as well as tangible and intangible property and 
their digital extensions (e.g., NFTs), introduces just one 
category of many fundamental shifts ushered in by the 
transition from physical to digital worlds - similar in 
potential impact to the introduction of corporate 
depersonalization or personhood, or of nation states 
themselves. 
Further, 
consider 
the 
introduction 
of 
decentralized autonomous organizations (DAOs) which 
may 
be 
composed 
of 
both 
human 
and 
adaptive 
autonomous entities and what this means for legal 
accountability, internationally and domestically. The legal 
handling of these transitions is thoroughly non-trivial - as 
one path might lead to serious implications for nation 
states and the foundation of their sovereignty (e.g., no one 
can force or coerce a public blockchain to grant and 
revoke an affordance) while another might lead to a 
substantially more powerful, and consequently, dangerous 
foundation for sovereignty (e.g., governments able to 
computationally force or bar interaction in a digital-
focused society). 
Social 
Simulation and modeling of narrative and social conflict 
can be notably difficult due to underlying challenges in 
accurately characterizing and modeling situational features 
that are relevant for ActInf agents [32]. AIC’s nested 
ActInf entities and their affordances for 
flexible 
representation of internal models and policy offers a 
common avenue for various extant and new approaches in 
representing ideological, psychological, narrative, and 
memetic conflict, as well as deterrence. Recently various 
models of dyadic and collective social interactions have 
been implemented using ActInf entities [112,118–120], 
suggesting a strong possibility for these kinds of models 
to be deployed in the case of conflict. The implications of 
using AIC in work on cognitive security and narrative 
management is discussed further in the discussion of 
modeling cognitive security.

## Page 49

Active Inference in Modeling Conflict, 2021 
 
47 
Modeling Cognitive Security 
Cognitive security (COGSEC) here refers to the study, development, 
and implementation of “practices, methodologies, and efforts made to 
defend 
against 
social 
engineering 
attempts 
- 
intentional 
and 
unintentional manipulations of and disruptions to cognition and 
sensemaking” [121]. COGSEC is difficult to measure and model for the 
same reason simulation and modeling of narrative and social conflict is 
- there are distinct, underlying challenges in representing and 
predicting the effects and attributes of internal states. AIC, as 
previously stated, offers opportunities for representing internal states 
of entities in relation to external conflicts, emphasizing impacts on 
cognition and sensemaking. However, AIC’s potential uses in the study 
of COGSEC go further: recent work on scripts and context-driven 
reflexes in ActInf [119] rely on the same structure and meth odologies 
as AIC and have great potential in being applied better understanding 
relevant threat surfaces, given that so much of the threat surfaces 
relevant to COGSEC and social engineering are related to development 
and exploitation of reflex for both offensive and defensive purposes 
[122]. COGSEC methodologies found in social engineering and 
counter-deception literature could be simulated and considered using 
AIC, to better model and measure COGSEC and also consider how 
traditional methods such as the “reduction of the complexity of 
problems, introduction of routine and bureaucratic procedures, the 
choosing of satisfactory solutions rather than optimal ones, [and] 
giving preference to partial solutions at the expense of comprehensive 
ones and avoidance of new problems'', and more recent approaches 
such 
as 
narrative 
information 
management 
[123], 
common 
vulnerabilities and exploits (CVE) databasing of narrative influence 
techniques [32], and engagement with narrative content [64,124] might 
affect state and expression of COGSEC in a variety of entities. 
Implications from Use: Future Information 
Structures and Rumsfeld’s Neglected 
Quadrant 
Usage of AIC to represent modern conflict and the BOLTS structures 
which interact within it provides insights beyond the pro jection of 
winners and losers in iterated games. Of particular interest are 
implications regarding the nature of the BOLTS structures themselves 
and the prioritization of their objectives in the reduction of uncertainty 
in their niche. Here we consider these implications before concluding 
and offering recommendations for future technology development.

## Page 50

Active Inference in Modeling Conflict, 2021 
 
48 
One of the implications of the move of the human species from physical 
toward information-based interaction landscapes is the reduction in 
efficacy and relevance of those historical institutions that provided 
reliability and protection for humans in physical spaces. As conflict 
becomes more abstract and less obvious, these traditional institutions 
are revealing their lack of fitness for governing in non -physical 
domains. While physical existence still precedes and is prerequisite for 
the achievement of other states and satisfaction of other needs, as 
reflected in Maslow’s hierarchy of needs [125], human interactions will 
continue to be increasingly dependent on the information landscapes 
in which nation states, and other organizational structures, are 
struggling to replicate the status quo. This struggle of legacy 
institutions to understand and manage conflict in an inherently 
incompatible information landscape, is forcing individuals to seek 
alternative structures of risk reduction to help them navigate.  
Using AIC as a qualitative lens renders all conflict as a form of 
information generation for the participating agents, with violent 
conflict constituting a “costly ping”. In the past, the information 
generated from conflict might have been found in the numerous post-
mortems and experience-informed treatises after campaigns [26] or in 
what could be called proactive intelligence, information about the 
enemy assembled after engagements [126] - however, now that conflict 
is increasingly situated in the information landscape and that the 
underlying “assets” and “territories” that are the objects of social, 
political, economic, and legal attention have shifted from physi cal 
emphasis to information emphasis, new structures are offered the 
opportunity for unparalleled management, monitoring, and facilitation 
of conflict. As well as the opportunity to define, via BOLTS norms, 
rules, and infrastructure, how conflict can be approached and resolved. 
AIC may be of use in both the design and implementation stages in 
these pursuits, and can provide alternative pathways that can be applied 
in those settings.  
Another consequence of this move from physical to information 
emphasis is the non-rivalrous nature of informational assets. Physical 
property (whether real estate or tangible personal property) is rivalrous 
- its use and enjoyment cannot be simultaneously and exclusively 
enjoyed by multiple parties. Territorial expansion and the  plunder of 
property reveal the rivalrousness of historical nation state conflict. In 
terms of digital materials - it is possible for two people to enjoy the 
use of the same software simultaneously, to read the same book, to 
watch the same movie, or to access the same data for different uses in 
different contexts without diminishment of the use and enjoyment of 
another. Further, physical assets are generally scarce and increase in

## Page 51

Active Inference in Modeling Conflict, 2021 
 
49 
scarcity over time - whereas the amount and complexity of information 
which can be generated as well as the rate of its growth is infinite. Both 
are expanding rapidly and creating structural hurdles to both individual 
and organizational situational awareness - the ability for organizations 
to manage this information effectively is strained [123].  
Using Rumsfeld’s Quadrants, which frame the information spaces and 
voids of value to organizations, as a lens over conflict both between 
organizations and between organizations and abstract phenomena (e.g., 
“war” on cancer, drugs, COVID-19), highlights Rumsfeld’s neglected 
quadrant, “unknown-knowns”. Further, it suggests that this neglected 
quadrant is a doorway from the static to the dynamic perspective on 
knowledge systems. The first three quadrants are described from the 
perspective of a centralized hierarchical party or bureaucracy - things 
are either known or not to that party, without reference to interaction 
with other parties that might alter the status of knowns and unknowns. 
On the other hand, this neglected quadrant appears to be a paradox: 
How can a given party not know a given “known”? 
For any individual ActInf entity, an unknown-known appears to be an 
impossibility - its known-knowns and known-unknowns are accessible 
within its internal state and its unknown-unknowns represent relevant 
voids within its internal state that it does not yet identify as such - 
which begs the question: Where is there room for an unknown -known? 
The AIC model helps to formalize several situations in which unknown-
knowns exist: 
Known but Inaccessible 
An ActInf entity may hold relevant information that goes 
unused in policy formulation as a result of it not being 
immediately accessible. 
Failure of Curation 
An ActInf entity may hold relevant information that is 
technically accessible but goes unused because of poor 
cues or the absence of indications of relevance. 
Back Turning 
An ActInf entity may ignore relevant information because 
it may contribute to policy formation which conflicts with 
some other existing policy, prior belief, or contextual 
model.

## Page 52

Active Inference in Modeling Conflict, 2021 
 
50 
Selective Disclosure 
An ActInf entity may have information that is accessible 
but will not access it in the interest of security or 
efficiency. 
Known but Undeciphered 
An ActInf entity may have latent information available 
which has not yet been deciphered, extracted, or codified. 
Insufficient Communication Dynamics.  
An ActInf entity composed of nested Entities, each with 
their own internal models, may fail to make use of relevant 
information due to insufficient internal communication 
dynamics. 
Most important among these several dynamics, is the notion of 
unknown-knowns within multi-agent systems. The moment that the 
ActInf entity interfaces with another in cooperation, they become a 
new perceivable entity, each with internal states that may be more or 
less synergized. Each has known-knowns and known-unknowns that the 
other is not necessarily aware of, constituting unknown-knowns in the 
context of the organization. The AIC model provides support for the 
argument that, in a turbulent and information-rich environment, top-
down management of information dynamics is no longer sufficient - 
that Rumsfeld’s initial prioritization of unknown-unknowns must give 
way to a prioritization of unknown-knowns, where “more than 
sufficient knowledge” exists but goes unused or misused in policy 
formulation due insufficient communication protocols, leading some to 
call for knowledge and rhetorical ecosystem approaches in the design 
of more decentralized information systems [123,127]. 
In this vein, the primary focus of the field of knowledge management 
might be considered to be addressing the problem of unknown -knowns. 
As has been addressed elsewhere, when the information management 
system in question begins to include parties outside the confines of a 
traditional organizational structure, the management of trust becomes 
a key concern [123]. The AIC model, in its use as a lens, demonstrates 
the value of trust in sharing unknown-knowns in a knowledge 
ecosystem in the form of several notable insights:

## Page 53

Active Inference in Modeling Conflict, 2021 
 
51 
Trust is Synonymous with  
Reliability 
Through an ActInf lens, trust is best characterized as 
projected 
reliability 
(e.g., 
high 
precision, 
or 
low 
uncertainty) of both other ActInf entities and indicators 
which inform projection.  
Trust can be Externalized to  
Interfaces 
ActInf entities don’t necessarily need to trust one another, 
but instead, can externalize trust to interfaces and related 
protocols among them in their niche to reduce costs of 
communication. 
Trust can be Externalized to  
Symbols and Signals 
Given that trust is best interpreted within an ActInf 
context as projected reliability, symbols and signals can 
thus be “trusted”. For example, traffic signals allow 
drivers to externalize their trust to signals which inform 
the projection of other drivers’ behavior, as opposed to 
being left to develop trust with other drivers in order to 
share the road. 
Trust is a Prerequisite for  
Efficient Information Sharing 
ActInf entities that question the motives or quality of 
communications, have high costs in interpreting or 
accepting those communications. 
Trust is a Prerequisite for  
Collaborative Enterprise. 
ActInf 
entities 
require 
trust, 
commensurate 
with 
associated risks, in order to engage in collaborative 
enterprise. Recently this has been explored in the context 
of human-robotic interactions [2]. 
We argue that these insights about unknown-knowns, trust, and the 
non-rivalrous nature of the objects relevant to modern conflict should 
inform the development of new structures, and offer recommendations 
for how in the discussion below.

## Page 54

Active Inference in Modeling Conflict, 2021 
 
52 
Discussion 
In this paper, we have briefly surveyed models of conflict, considered 
their strengths and inadequacies, proposed a unifying model based 
upon the application of Active Inference (ActInf), and considered the 
implications of use of the Active Inference Conflict (AIC) model. The 
initial survey revealed that the study and modeling of warfare 
progressed generally through time from inventories of tactics toward 
more theoretical and ultimately more abstracted and context-informed 
analyses. That evolution of the models could be framed as mirroring 
the parallel development through time of human understanding of 
human structures of information, as well as structures of cognition, 
organization, and interaction across the sciences and social sciences, 
including patterns of conflict in those disciplinary domains. For 
example, as discussed above, early quantitative models of conflict such 
as the Lanchester model used mathematical tools that were modern at 
the time, such as linear regressions and differential equations.  
Today, similar analytical and paradigmatic (r)evolutions are taking place 
in research and understanding about human commerce, behaviors, 
political governance, and other related domains, ultimately positioning 
the subset of behaviors and interactions associated with “war” as 
categories of a subset of patterns of human history and society - albeit 
patterns that are a non-linear in relation to others. Clausewitz’s 
observation about politics and war is consistent with this notion of the 
evolution of the human understanding of the human condition, but 
following the results of the survey, we contend his famous quote, that 
“war is the continuation of politics by other means”, is incomplete 
within this context as it would appear that both war and politics are a 
continuation of conflict by other means (and, in fact, conflict is a 
continuation of the normal function of living systems in just another 
analytical framing). 
The survey revealed an increasing abstraction and formalism in the 
modeling and study of conflict and war, evolving from catalogs of 
physical battlefield heuristics toward broader and more detailed 
analytical framings of context and motivations for physical forms of 
conflict. However, it also indicated that many of the models are 
underdeveloped for current applications and struggle to address the 
changing expression of war and the migration of human interactions 
from predominantly physical interactions (i.e., kinetic warfare) toward 
abstract, symbolic, and intangible interactions within information 
landscapes. Further, the survey disclosed that existing warfare models 
did not have the necessary generalizability to be broadly applicable to

## Page 55

Active Inference in Modeling Conflict, 2021 
 
53 
the relevant expressions of conflict in other social contexts, and that 
the models are rarely interoperable. 
Following this survey, we proposed the use of ActInf methodologies 
and terms in modeling conflict and named this application the Active 
Inference Conflict (AIC) model. The AIC model is intended to 
represent a needed updating of conflict framing to reflect changes in 
human interaction patterns, and also provides built-in mathematical 
rigor that could be used to facilitate the organization and operation of 
future conflict management architectures. The AIC model, as a 
consequence of it being founded on the matured quantitative models 
of ActInf, is tractable to simulate, can incorporate empirical data, and 
also can immediately be implemented qualitatively to produce novel 
insights about various forms of conflict. We discussed how this 
approach, with its affordances for sense and action loops, multi-entity 
interactions, entity nesting, and policy selection offers old models a 
new medium for their expression and interoperability while also 
providing avenues for generalizing conflict modeling which can capture 
relevant aspects of modern conflict.  
Specifically connecting the AIC model to OODA and GW demonstrated 
the relevance of integrating previous tactical and strategic frameworks 
within a single multi-scale formal model. Of particular interest was the 
consideration for the ability of AIC to capture conflicts which have 
business, operations, legal, technical, and social components, to move 
beyond generations and gradients of war and offer a new medium for 
capturing metrics for classifying and clustering myriad forms of 
conflict, and to model emerging conflict surfaces involving cognitive 
security and narrative warfare. 
Finally, we considered broader implications suggested by qualitative 
application of the AIC model to conflict generally. We reflected on the 
state of the information environment, noting the difficulties that 
traditional institutional and governance structures are having in 
handling modern information-based conflict and that new, alternative 
structures for risk reduction are being offered the opportunity to 
provide value. In addition, we reflected on the non-rivalrous nature of 
information-as-asset and the infinite potential for information growth, 
and how these factors affect organizations - mainly in terms of 
processing information load - which is a useful surrogate for risk. 
Within these reflections, we suggested that the AIC model is not just 
useful for the study of conflict but also in the design of systems which 
manage it. Finally, we applied the AIC model to reveal latent insights 
about trust and knowledge environments within the Rumsfeld

## Page 56

Active Inference in Modeling Conflict, 2021 
 
54 
Quadrants, 
specifically 
regarding 
its 
oft-neglected 
quadrant, 
“unknown-knowns”. 
The AIC model, as previously discussed, provides an avenue for formal 
modeling of systems - but this same affordance also facilitates design 
and evaluation of the design of systems, and to implement and test 
BOLTS norms and rules. This is to say that a socio-technical system 
modeled with the AIC model can effectively be a “twin” of that socio-
technical system, and thus can be used for more than just studying its 
conflicts, but also for managing and facilitating endogenous 
information conflict and friction itself. It took humans millennia to 
figure out how to convert the random motion of atoms energized by 
heat from fire into useful “work” through the use of heat engines. The 
AIC framing invites consideration of how the equivalent of a 
“combustion chamber” might be configured for converting the friction 
of disagreement into useful work within a knowledge environment in 
terms of developing new information, repairing faulty or incomplete 
information, discovering unknown-knowns and unknown-unknowns, 
and helping entities within develop trust and healthy information flows. 
Within this context, de-risking of interactions in which information 
exchanges occur could be seen not as a state, but as an ongoing process 
- which places pressure on designers of information systems to develop 
simple rules and effective protocols.  
Past work has considered how humans and human organizations 
collaboratively organize, annotate, and structure claims as a form of 
narrative information management [64,123,128], and could be of use in 
conjunction with the AIC model to build tools which document, 
facilitate, and resolve informational conflicts with an objective 
dimensionality from the AIC model that leverages existing approaches. 
Further, these pairings of approaches could help give new life to the 
older narrative models of conflicts and unify them with the work on 
commons management [79], as it could provide a new medium for 
formalizing, documenting, and sharing of heuristics and practices for 
risk mitigation [32].  
As the rate of information growth continues to explode outward in both 
volume and complexity, the AIC model reveals that the search for 
unknown-unknowns or known-unknowns may need to be deprioritized, 
as this information may fail to be disseminated and integrated - 
rendering most relevant information as unknown-knowns. Where 
“hope” was left in Pandora’s box, it might be said that “trust” was left 
in Rumsfeld’s matrix. The AIC model helps to demonstrate and codify 
the value of trust in knowledge ecosystems which facilitate the sharing 
of unknown-knowns, and demonstrates how trust can be externalized

## Page 57

Active Inference in Modeling Conflict, 2021 
 
55 
to protocol and signals through their being reliable indicators of quality 
and behavior. Ultimately, a primary suggestion of this work is that 
facilitating 
mutual 
interdependencies, 
interfaces, 
and 
trust -
management frameworks, key prerequisites to sharing unknown-
knowns, could attract an increasing subset of information conflicts into 
generative structures (perhaps best framed as structures which operate 
in the manner of what might be called a “risk commons”) which can 
capture value and grow trust, rather than accelerate discord. Below, we 
distill these and other insights within this work into recommendations 
for future research and the design of new systems: 
• Develop more work on the use of the AIC model in extending 
the value of OODA loops in simulation and decision-making 
models. This could utilize complex systems modeling software 
such as cadCAD [129], and those specifically for ActInf such as 
ForneyLab [130] or infer-actively [131]. 
• Explore the use of the AIC model in modeling past conflicts as 
a basis for measuring various attributes of those conflicts, and 
the use of those attributes for new classifications and 
“generations” or gradients of conflict. 
• Explore the use of the AIC model and the integration of 
commons management principles and compensating controls 
across business, operations, legal, technical, and social (BOLTS) 
surfaces. 
• In the design of information exchange systems: 
o Acknowledge de-risking as an ongoing process, rather than 
as a static attribute. 
o Consider trust as synonymous with perceived reliability. 
o Make use of the fact that trust can be externalized to 
signals and symbols so long as those signals and symbols 
are reliable indicators of behavior and state. 
o Consider disagreement, inconsistency, and incoherence as 
events which can be mined for value via shared protocols 
and standards rather than creating an illusion of security 
through attempts at their removal. 
• Across many domains (e.g., war, scholarship, and design), 
reprioritize Rumsfeld’s neglected quadrant of unknown-knowns.

## Page 58

Active Inference in Modeling Conflict, 2021 
 
56 
 
Contribution Statements 
Administration and Facilitation: R.J. Cordes 
Writing, Editing, and Revision: All authors made substantial 
contributions to writing, editing, and revisions across all sections. 
Funding and Acknowledgements 
Scott David is funded by the NSF Convergence Accelerator Trust and 
Authenticity in Communication Systems Program (NSF 21-572), under 
award ID #49100421C0036. 
R.J. Cordes is funded by the NSF Convergence Accelerator Trust and 
Authenticity in Communication Systems Program (NSF 21-572), under 
award ID #49100421C0036 and is supported in research efforts 
through a Nonresident Fellowship with the Atlantic Council on 
appointment to the GeoTech Center.  
Daniel A. Friedman is funded by the NSF program Postdoctoral 
Research Fellowships in Biology (NSF 20-077), under award ID 
#2010290.

## Page 59

Active Inference in Modeling Conflict, 2021 
 
57 
Works Cited 
Generated using a reference manager. 
1. 
Cordes RJ, Friedman DA. Emergent Teams for Complex Threats. The Great 
Preset: Remote Teams and Operational Art. COGSEC; 2020. 
2. 
Schoeller F, Miller M, Salomon R, Friston K. Trust as Extended Control: 
Active Inference and User Feedback During Human-Robot Collaboration. 
ArXiv. 2021 [cited 21 Sep 2021]. Available: 
https://www.semanticscholar.org/paper/7c39921b6050d7be82e18df2a31973f
2c3f864ea 
3. 
Vyatkin A, Metelkin I, Mikhailova A, Cordes RJ, Friedman DA. Active 
Inference & Behavior Engineering for Teams. 2020. 
doi:10.5281/zenodo.4021163 
4. 
Guénin--Carlut A. Thinking like a State - Embodied intelligence in the deep 
history of our collective minds. 2021 [cited 21 Sep 2021]. Available: 
https://osf.io/dxnzt/ 
5. 
Collier JL, Collier C. Slavery and the Coming of the Civil War: 1831 - 1861. 
Blackstone Publishing; 2012. Available: 
https://play.google.com/store/books/details?id=8Mt47-uzDH0C 
6. 
Tzu S. Sun Tzu Art of War. Vij Books India Pvt Ltd; 2012. Available: 
https://play.google.com/store/books/details?id=VPSpCQAAQBAJ 
7. 
Milner NP. Vegetius: Epitome of military science. Liverpool: Translated Texts 
for Historians. 1993;16: 14. 
8. 
von Moltke H, Hughes DJ. Moltke on the Art of War: Selected Writings. 
Ballantine Books; 1993. 
9. 
Machiavelli N. Art of War. New edition. University of Chicago Press; 2005. 
Available: https://www.amazon.com/Art-War-Niccol%C3%B2-
Machiavelli/dp/0226500462 
10. 
Bin S. Sun Bin: The Art of Warfare: A Translation of the Classic Chinese 
Work of Philosophy and Strategy (SUNY Series in Chinese Philosophy and 
Culture). State University of New York Press; 2003. Available: 
https://www.amazon.com/Sun-Bin-Translation-Philosophy-
Strategy/dp/0791454967 
11. 
Tse-Tung M. The Art of War by Mao Tse-tung - Special Edition. El Paso 
Norte Press; 2011. Available: 
https://play.google.com/store/books/details?id=2uVIYgEACAAJ 
12. 
Jomini A-H, Mendell GH, Craighill WP. The Art of War. Courier 
Corporation; 2007. Available: 
https://play.google.com/store/books/details?id=mdI6AwAAQBAJ 
13. 
Carl Von Clausewitz, Howard M, Paret P, Howard M, Brodie B. On War. 
Howard M, Paret P, editors. Princeton University Press; 1989. 
14. 
van Creveld M. More on War. Oxford University Press; 2016. Available: 
https://play.google.com/store/books/details?id=oWLODQAAQBAJ

## Page 60

Active Inference in Modeling Conflict, 2021 
 
58 
15. 
Villacres EJ, Bassford C. Reclaiming the Clausewitzian Trinity. West Point 
Military Academy; 1995 Jan. Available: 
https://apps.dtic.mil/sti/citations/ADA528269 
16. 
Kelly J, Kilcullen D. Chaos Versus Predictability: A Critique of Effects-Based 
Operations. Security Challenges. 2006;2: 63–73. Available: 
http://www.jstor.org/stable/26458837 
17. 
Mattis J. Commander’s Guidance for Effects-Based Operations. US Joint 
Forces Command; 2018. 
18. 
Knox BMW, Murray W. The Dynamics of Military Revolution, 1300-2050. 
Cambridge University Press; 2001. Available: 
https://play.google.com/store/books/details?id=zIIbUmwXitAC 
19. 
Krepinevich AF. Cavalry to Computer: The Pattern of Military Revolutions. 
The National Interest. 1994; 30–42. Available: 
http://www.jstor.org/stable/42896863 
20. 
Knox BMW, Murray W. The Dynamics of Military Revolution, 1300-2050. 
Cambridge University Press; 2001. Available: 
https://play.google.com/store/books/details?id=zIIbUmwXitAC 
21. 
Hoffman FG. Will War’s Nature Change in the Seventh Military Revolution? 
Parameters. 2017;47: 19–31. Available: 
https://publications.armywarcollege.edu/pubs/3554.pdf 
22. 
Lind WS, Nightengale K, Schmitt JF, Sutton JW, Wilson GI. The changing 
face of war: Into the fourth generation. The Marine Corps Gazette. 1989: 22–
26. Available: 
https://www.academia.edu/download/15486651/thechangingfaceofwar-
onscreen.pdf 
23. 
Abbott DH, editor. The Handbook of Fifth-Generation Warfare (5GW). 
Nimble Books; 2010. Available: https://www.amazon.com/Handbook-Fifth-
Generation-Warfare-5gw/dp/1934840173 
24. 
Cordes RJ. The Next Generation of Security: Prioritizing Information Warfare 
Defense. 7 Aug 2021 [cited 12 Aug 2021]. Available: 
https://www.hstoday.us/subject-matter-areas/intelligence/the-next-
generation-of-security-prioritizing-information-warfare-defense/ 
25. 
Kohalyk C. 5GW as Netwar 2.0. In: Abbott DH, editor. The Handbook of 
Fifth-Generation Warfare (5GW). Nimble Books; 2010. pp. 38–52. Available: 
https://www.amazon.com/Handbook-Fifth-Generation-Warfare-
5gw/dp/1934840173 
26. 
Linn BM. The Echo of Battle. Harvard University Press; 2009. Available: 
https://play.google.com/store/books/details?id=clKtd4O3MOgC 
27. 
Lanchester FW. Aircraft in Warfare: The Dawn of the Fourth Arm. Constable 
limited; 1916. Available: 
https://play.google.com/store/books/details?id=fIZCAAAAIAAJ 
28. 
Kress M. Lanchester Models for Irregular Warfare. Sci China Ser A Math. 
2020;8: 737. doi:10.3390/math8050737

## Page 61

Active Inference in Modeling Conflict, 2021 
 
59 
29. 
González E, Villena M. Spatial Lanchester models. Eur J Oper Res. 2011;210: 
706–715. doi:10.1016/j.ejor.2010.11.009 
30. 
Nicolae F, Cotorcea A, Ristea M, Atodiresei D. Human Reliability Using the 
Fault Tree Analysis. A Case Study of a Military Accident Investigation. 
International conference KNOWLEDGE-BASED ORGANIZATION. 
researchgate.net; 2016. Available: 
https://www.researchgate.net/profile/Dinu-
Atodiresei/publication/305760875_Human_Reliability_Using_the_Fault_Tree
_Analysis_A_Case_Study_of_a_Military_Accident_Investigation/links/58d2b
e9da6fdccd24d43bc41/Human-Reliability-Using-the-Fault-Tree-Analysis-A-
Case-Study-of-a-Military-Accident-Investigation.pdf 
31. 
La Band RA, Andrews JD. Phased mission modelling using fault tree analysis. 
Proc Inst Mech Eng Part E J Process Mech Eng. 2004;218: 83–91. 
doi:10.1243/095440804774134262 
32. 
Cordes RJ, David S, Maan A, Ruiz A, Sapp E, Scannell P, et al. The Narrative 
Campaign Field Guide - First Edition. 1st ed. Cordes RJ, editor. Narrative 
Strategies Ink; 2021. Available: https://www.narrative-strategies.com/ncfg 
33. 
Wagenhals LW, Alex L, Haider S. Planning, Execution, and Assessment of 
Effects-Based Operations (EBO). GEORGE MASON UNIV FAIRFAX VA 
CENTER OF EXCELLENCE IN COMMAND CONTROL 
COMMUNICATIONS AND INTELLIGENCE; 2006 May. Available: 
https://apps.dtic.mil/sti/citations/ADA451493 
34. 
Hause M. The Unified Profile for DoDAF/MODAF (UPDM) enabling 
systems of systems on many levels. 2010 IEEE International Systems 
Conference. ieeexplore.ieee.org; 2010. pp. 426–431. 
doi:10.1109/SYSTEMS.2010.5482450 
35. 
Handley HAH. Incorporating the NATO human view in the DoDAF 2.0 meta 
model. Syst Eng Electr. 2012;15: 108–117. doi:10.1002/sys.20206 
36. 
Rumer E. The Primakov (not Gerasimov) doctrine in action. Carnegie 
Endowment for International Peace; 2019. Available: 
https://carnegieendowment.org/files/Rumer_PrimakovDoctrine_final1.pdf 
37. 
Morris V. Grading Gerasimov: Evaluating Russian Nonlinear War Through 
Modern Chinese Doctrine. Small Wars Journal. 2015. Available: 
https://smallwarsjournal.com/jrnl/art/grading-gerasimov-evaluating-russian-
nonlinear-war-through-modern-chinese-doctrine. Accessed 18 Oct 2021. 
38. 
Engstrom J. Systems Confrontation and System Destruction Warfare: How 
the Chinese People’s Liberation Army Seeks to Wage Modern Warfare. 
RAND; 2018. Report No.: RR-1708-OSD. 
39. 
Grant T, Kooter B. Network-centric warfare: Its origin and future. Future of 
C2. academia.edu; 1998. Available: 
https://www.academia.edu/download/36514207/1_NCW_Origin_and_Futur
eVice_Admiral_Arthur_K._Cebrowski.pdf 
40. 
Yang A, Curtis N, Abbass HA, Sarker R, Barlow M. WISDOM-II: A network 
centric model for warfare. Complex Science for a Complex World: Exploring 
Human Ecosystems with Agents. 2006; 149–173. Available:

## Page 62

Active Inference in Modeling Conflict, 2021 
 
60 
https://library.oapen.org/bitstream/handle/20.500.12657/33791/458885.pdf
?sequence=1#page=167 
41. 
Park S-Y, Shin H-Y, Lee T-S, Choi B-W. Design of the Agent-based Network-
Centric Warfare Modeling System. Journal of the Korea Society for 
Simulation. 2010;19: 271–280. Available: 
https://www.koreascience.or.kr/article/JAKO201016450102380.page 
42. 
Kang BG, Choi SH, Kwon SJ, Lee JH, Kim TG. Simulation-Based 
Optimization on the System-of-Systems Model via Model Transformation and 
Genetic Algorithm: A Case Study of Network-Centric Warfare. Complexity. 
2018;2018. doi:10.1155/2018/4521672 
43. 
Grant T, Kooter B. Comparing ooda & other models as operational view c2 
architecture topic: C4isr/c2 architecture. ICCRTS2005, Jun. 2005. Available: 
https://www.researchgate.net/profile/Tim-Grant-
9/publication/237674561_Comparing_OODA_other_models_as_Operational
_View_C2_Architecture/links/584dbdde08aeb9892526444d/Comparing-
OODA-other-models-as-Operational-View-C2-Architecture.pdf 
44. 
Mees W, Debatty T. An attempt at defining cyberdefense situation awareness 
in the context of command & control. 2015 [cited 18 Oct 2021]. 
doi:10.1109/ICMCIS.2015.7158674 
45. 
Endsley MR. A taxonomy of situation awareness errors. Human factors in 
aviation operations. 1995;3: 287–292. Available: 
https://www.researchgate.net/profile/Mica-
Endsley/publication/285731357_A_taxonomy_of_situation_awareness_errors
_human_factors_in_aviation_operations/links/58322a6f08ae138f1c07a4e3/A-
taxonomy-of-situation-awareness-errors-human-factors-in-aviation-
operations.pdf 
46. 
Plehn MT. Control warfare: Inside the OODA Loop. AIR UNI MAXWELL 
AFB AL SCHOOL OF ADVANCED AIRPOWER STUDIES; 2000 Jun. 
Available: https://apps.dtic.mil/sti/citations/ADA391774 
47. 
Hammond GT. Reflections on the Legacy of John Boyd. Contemporary 
Security Policy. 2013;34: 600–602. doi:10.1080/13523260.2013.842297 
48. 
Kalloniatis A, Rowe C, La P, Holder A, Bennier J, Mitchell B. Network 
Analysis of Decision Loops in Operational Command and Control 
Arrangements. Data and Decision Sciences in Action. Springer International 
Publishing; 2018. pp. 343–355. doi:10.1007/978-3-319-55914-8_25 
49. 
Boyd J. A discourse on winning and losing. Hammond GT, editor. Air 
University Press; 2018. Available: 
https://www.airuniversity.af.edu/Portals/10/AUPress/Books/B_0151_Boyd
_Discourse_Winning_Losing.pdf 
50. 
Vettorello M, Eisenbart B, Ranscombe C. Toward Better Design-Related 
Decision Making: A Proposal of an Advanced OODA Loop. Proceedings of 
the Design Society: International Conference on Engineering Design. 2019;1: 
2387–2396. doi:10.1017/dsi.2019.245 
51. 
Silvander J, Angelin L. Introducing intents to the OODA-loop. Procedia 
Comput Sci. 2019;159: 878–883. doi:10.1016/j.procs.2019.09.247

## Page 63

Active Inference in Modeling Conflict, 2021 
 
61 
52. 
McManus N, Haddad AN. Incident Records: Understanding the Past to 
Prevent Future Hazardous Energy Incidents. Prof Saf. 2014;59: 34–43. 
Available: https://onepetro.org/PS/article-abstract/59/12/34/33209 
53. 
Pawson R, Wong G, Owen L. Known Knowns, Known Unknowns, Unknown 
Unknowns: The Predicament of Evidence-Based Policy. American Journal of 
Evaluation. 2011;32: 518–546. doi:10.1177/1098214011403831 
54. 
Alles M. Governance in the age of unknown unknowns. International Journal 
of Disclosure and Governance. 2009;6: 85–88. doi:10.1057/jdg.2009.2 
55. 
Birkemo GA. Is Norwegian long term defence planning risk based? ffi-
publikasjoner.archive …; 2013. Available: https://ffi-
publikasjoner.archive.knowledgearc.net/handle/20.500.12242/929 
56. 
Žižek S. Philosophy, the “unknown knowns,” and the public use of reason. 
Topoi. 2006;25: 137–142. doi:10.1007/s11245-006-0021-2 
57. 
Jackson R. Unknown knowns: the subjugated knowledge of terrorism studies. 
Critical Studies on Terrorism. 2012;5: 11–29. 
doi:10.1080/17539153.2012.659907 
58. 
Sarewitz D. Unknown Knowns. Issues Sci Technol. 2020;37: 18–19. Available: 
https://issues.org/wp-content/uploads/2020/09/18-19-Sarewitz-Editors-
Journal-Fall-2020-ISSUES.pdf 
59. 
Logan DC. Known knowns, known unknowns, unknown unknowns and the 
propagation of scientific enquiry. Journal of experimental botany. 
academic.oup.com; 2009. pp. 712–714. doi:10.1093/jxb/erp043 
60. 
Loxdale HD, Davis BJ, Davis RA. Known knowns and unknowns in biology. 
Biol J Linn Soc Lond. 2016;117: 386–398. doi:10.1111/bij.12646 
61. 
Bassford C. Christopher Bassford: Tiptoe Through the Trinity. In: 
https://www.clausewitzstudies.org/ [Internet]. 2016 [cited 28 Sep 2021]. 
Available: https://www.clausewitzstudies.org/mobile/trinity8.htm 
62. 
Nielsen JN. The Generational Warfare Model. In: 
geopolicraticus.wordpress.com [Internet]. 27 Oct 2010 [cited 22 Sep 2021]. 
Available: https://geopolicraticus.wordpress.com/2010/10/26/the-
generational-warfare-model/ 
63. 
Alexander C. A Pattern Language: Towns, Buildings, Construction. Oxford 
University Press; 1977. Available: 
https://play.google.com/store/books/details?id=mW7RCwAAQBAJ 
64. 
Mascarenhas M, Cordes RJ, Friedman DA. Digital Rhetorical Ecosystem 
Analysis: Sensemaking of Digital Memetic Discourse. Zenodo. 2021. 
doi:10.5281/zenodo.5573947 
65. 
Naylor RT. Economic Warfare: Sanctions, Embargo Busting, and Their 
Human Cost. UPNE; 2001. Available: 
https://play.google.com/store/books/details?id=fkcGKb8jLXMC 
66. 
Clemens J. An analysis of economic warfare. Am Econ Rev. 2013. Available: 
https://www.aeaweb.org/articles?id=10.1257/aer.103.3.523

## Page 64

Active Inference in Modeling Conflict, 2021 
 
62 
67. 
Tang M. Huawei Versus the United States? The Geopolitics of Exterritorial 
Internet Infrastructure. Int J Commun Syst. 2020;14: 22. Available: 
https://ijoc.org/index.php/ijoc/article/view/12624 
68. 
Cheng D. Winning without fighting: Chinese legal warfare. Backgrounder. 
2012. Available: http://thf_media.s3.amazonaws.com/2012/pdf/bg2692.pdf 
69. 
Kotani T. Freedom of navigation and the US-Japan alliance: Addressing the 
threat of legal warfare. US-Japan Papers. 2011; 1–6. Available: 
https://www.jcie.org/researchpdfs/USJapanPapers/Kotani.pdf 
70. 
Atlantic Council GeoTech Center. Standardizing the future: How can the 
United States navigate the geopolitics of international technology standards? 
In: Atlanticcouncil.org [Internet]. 14 Oct 2021 [cited 21 Oct 2021]. Available: 
https://www.atlanticcouncil.org/in-depth-research-
reports/report/standardizing-the-future-how-can-the-united-states-navigate-
the-geopolitics-of-international-technology-standards/ 
71. 
Atlantic Council GeoTech Center. Report of the Commission on the 
Geopolitical Impacts of New Technologies and Data - GeoTech Commission 
Report. 2021. Report No.: v51j. 
72. 
Caputo A, Marzi G, Maley J, Silic M. Ten years of conflict management 
research 2007-2017: An update on themes, concepts and relationships. 
International Journal of Conflict Management. 2018;30: 87–110. 
doi:10.1108/IJCMA-06-2018-0078 
73. 
Kimbrough EO, Sheremeta RM. Theories of conflict and war. J Econ Behav 
Organ. 2019;159: 384–387. doi:10.1016/j.jebo.2019.02.007 
74. 
Walton RE, McKersie RB. A Behavioral Theory of Labor Negotiations: An 
Analysis of a Social Interaction System. Cornell University Press; 1991. 
Available: https://play.google.com/store/books/details?id=dW02zPVX9rQC 
75. 
Burchill F. Walton and McKersie, A Behavioral Theory of Labor Negotiations 
(1965). Historical Studies in Industrial Relations. 1999; 137–168. 
doi:10.3828/hsir.1999.8.7 
76. 
Werbach K. Supercommons: Toward a Unified Theory of Wireless 
Communication. 2003. doi:10.2139/ssrn.456020 
77. 
Prainsack B. Logged out: Ownership, exclusion and public value in the digital 
data and information commons. Big Data & Society. 2019;6: 
2053951719829773. doi:10.1177/2053951719829773 
78. 
nobelprize.org. Elinor Ostrom Facts. In: nobelprize.org [Internet]. 2021 [cited 
4 Nov 2021]. Available: https://www.nobelprize.org/prizes/economic-
sciences/2009/ostrom/facts/ 
79. 
Hess C, Ostrom E. Understanding Knowledge as a Commons: From Theory 
to Practice. MIT Press; 2011. Available: 
https://play.google.com/store/books/details?id=5UCCkgAACAAJ 
80. 
Friedman D, Tschantz A, Ramstead MJD, Friston K, Constant A. Active 
inferants: The basis for an active inference framework for ant colony 
behavior. Front Behav Neurosci. 2021;15: 126. 
doi:10.3389/fnbeh.2021.647732

## Page 65

Active Inference in Modeling Conflict, 2021 
 
63 
81. 
Da Costa L, Parr T, Sajid N, Veselic S, Neacsu V, Friston K. Active inference 
on discrete state-spaces: A synthesis. J Math Psychol. 2020;99: 102447. 
doi:10.1016/j.jmp.2020.102447 
82. 
Parr T, Pezzulo G, Friston KJ. Active Inference: The Free Energy Principle in 
Mind, Brain, and Behavior. 2022. 
83. 
Linson A, Clark A, Ramamoorthy S, Friston K. The Active Inference 
Approach to Ecological Perception: General Information Dynamics for 
Natural and Artificial Embodied Cognition. Frontiers in Robotics and AI. 
2018;5: 21. doi:10.3389/frobt.2018.00021 
84. 
Gallagher S, Allen M. Active inference, enactivism and the hermeneutics of 
social cognition. Synthese. 2018;195: 2627–2648. doi:10.1007/s11229-016-
1269-8 
85. 
Fox S. Accessing Active Inference Theory through Its Implicit and 
Deliberative Practice in Human Organizations. Entropy . 2021;23: 1521. 
doi:10.3390/e23111521 
86. 
Millidge B. Combining active inference and hierarchical predictive coding: A 
tutorial introduction and case study. PsyArXiv. 2019. 
doi:10.31234/osf.io/kf6wc 
87. 
Active Inference Lab. ActInfLab ModelStream #001.1: “A Step-by-Step 
Tutorial on Active Inference.” Youtube; 15 Jan 2021 [cited 11 Aug 2021]. 
Available: https://www.youtube.com/watch?v=H5AolqFl2Nw 
88. 
Smith R, Friston K, Whyte C. A Step-by-Step Tutorial on Active Inference 
and its Application to Empirical Data. 2021. doi:10.31234/osf.io/b4jm6 
89. 
Millidge B, Seth A, Buckley CL. Predictive Coding: a Theoretical and 
Experimental Review. arXiv [cs.AI]. 2021. Available: 
http://arxiv.org/abs/2107.12979 
90. 
ActInfLab. [cited 16 Nov 2021]. Available: https://www.activeinference.org/ 
91. 
Rubin S, Parr T, Da Costa L, Friston K. Future climates: Markov blankets and 
active inference in the biosphere. J R Soc Interface. 2020;17: 20200503. 
doi:10.1098/rsif.2020.0503 
92. 
Ramstead MJD, Kirchhoff MD, Constant A, Friston KJ. Multiscale 
integration: beyond internalism and externalism. Synthese. 2021;198: 41–70. 
doi:10.1007/s11229-019-02115-x 
93. 
Hipólito I, Ramstead MJD, Convertino L, Bhat A, Friston K, Parr T. Markov 
blankets in the brain. Neurosci Biobehav Rev. 2021;125: 88–97. 
doi:10.1016/j.neubiorev.2021.02.003 
94. 
Kirchhoff M, Parr T, Palacios E, Friston K, Kiverstein J. The Markov 
blankets of life: autonomy, active inference and the free energy principle. J R 
Soc Interface. 2018;15. doi:10.1098/rsif.2017.0792 
95. 
Sims M. How to count biological minds: symbiosis, the free energy principle, 
and reciprocal multiscale integration. Synthese. 2020. doi:10.1007/s11229-
020-02876-w

## Page 66

Active Inference in Modeling Conflict, 2021 
 
64 
96. 
Fox S. Active Inference: Applicability to Different Types of Social 
Organization Explained through Reference to Industrial Engineering and 
Quality Management. Entropy . 2021;23: 198. doi:10.3390/e23020198 
97. 
Sajid N, Ball PJ, Parr T, Friston KJ. Active inference: demystified and 
compared. arXiv [cs.AI]. 2019. Available: http://arxiv.org/abs/1909.10863 
98. 
Friston K, Fortier M, Friedman DA. Of woodlice and men. ALIUS Bulletin. 
2018;2: 17. Available: 
https://www.aliusresearch.org/uploads/9/1/6/0/91600416/alius_bulletin_n
%C2%B02__2018_.pdf#page=27 
99. 
Ramstead MJD, Kirchhoff MD, Friston KJ. A tale of two densities: active 
inference is enactive inference. Adapt Behav. 2019;28: 1059712319862774. 
doi:10.1177/1059712319862774 
100. 
Lobo L, Heras-Escribano M, Travieso D. The History and Philosophy of 
Ecological Psychology. Front Psychol. 2018;9: 2228. 
doi:10.3389/fpsyg.2018.02228 
101. 
Friston K. The free-energy principle: a unified brain theory? Nat Rev 
Neurosci. 2010;11: 127–138. doi:10.1038/nrn2787 
102. 
Friston K, Heins C, Ueltzhöffer K, Da Costa L, Parr T. Stochastic Chaos and 
Markov Blankets. Entropy . 2021;23. doi:10.3390/e23091220 
103. 
Parr T, Friston KJ. Generalised free energy and active inference. Biol Cybern. 
2019;113: 495–513. doi:10.1007/s00422-019-00805-w 
104. 
Ramstead MJD, Constant A, Badcock PB, Friston KJ. Variational ecology and 
the physics of sentient systems. Phys Life Rev. 2019. 
doi:10.1016/j.plrev.2018.12.002 
105. 
Friston K. A free energy principle for a particular physics. arXiv [q-bio.NC]. 
2019. Available: http://arxiv.org/abs/1906.10184 
106. 
Bolis D, Schilbach L. “Through others we become ourselves”: The dialectics 
of predictive coding and active inference. 2019. doi:10.31234/osf.io/6uwyn 
107. 
Veissière SPL, Constant A, Ramstead MJD, Friston KJ, Kirmayer LJ. 
Thinking through other minds: A variational approach to cognition and 
culture. Behav Brain Sci. 2019;43: 1–97. doi:10.1017/S0140525X19001213 
108. 
Penny WD, Friston KJ, Ashburner JT, Kiebel SJ, Nichols TE. Statistical 
Parametric Mapping: The Analysis of Functional Brain Images. Elsevier; 2011. 
Available: https://play.google.com/store/books/details?id=G_qdEsDlkp0C 
109. 
Friston K, Mattout J, Kilner J. Action understanding and active inference. 
Biol Cybern. 2011;104: 137–160. doi:10.1007/s00422-011-0424-z 
110. 
Butz MV, Bilkey D, Humaidan D, Knott A, Otte S. Learning, planning, and 
control in a monolithic neural event inference architecture. Neural Netw. 
2019;117: 135–144. doi:10.1016/j.neunet.2019.05.001 
111. 
Ramstead MJD, Veissière SPL, Kirmayer LJ. Cultural Affordances: 
Scaffolding Local Worlds Through Shared Intentionality and Regimes of 
Attention. Front Psychol. 2016;7: 1090. doi:10.3389/fpsyg.2016.01090

## Page 67

Active Inference in Modeling Conflict, 2021 
 
65 
112. 
Constant A, Ramstead MJD, Veissière SPL, Friston K. Regimes of 
Expectations: An Active Inference Model of Social Conformity and Human 
Decision Making. Front Psychol. 2019;10: 679. doi:10.3389/fpsyg.2019.00679 
113. 
Tschantz A, Seth AK, Buckley CL. Learning action-oriented models through 
active inference. PLoS Comput Biol. 2020;16: e1007805. 
doi:10.1371/journal.pcbi.1007805 
114. 
Kaufmann R, Gupta P, Taylor J. An Active Inference Model of Collective 
Intelligence. Entropy . 2021;23. doi:10.3390/e23070830 
115. 
Kittrie OF. Lawfare: Law as a Weapon of War. Oxford University Press; 2016. 
Available: https://play.google.com/store/books/details?id=r1jhCgAAQBAJ 
116. 
Dunlap CJ Jr. Lawfare 101: A Primer. 2017 [cited 8 Jun 2021]. Available: 
https://scholarship.law.duke.edu/faculty_scholarship/3742/ 
117. 
Lee S. China’s “Three Warfares”: Origins, Applications, and Organizations. 
Journal of Strategic Studies. 2014;37: 198–221. 
doi:10.1080/01402390.2013.870071 
118. 
Isomura T, Parr T, Friston K. Bayesian Filtering with Multiple Internal 
Models: Toward a Theory of Social Intelligence. Neural Comput. 2019; 1–42. 
doi:10.1162/neco_a_01239 
119. 
Albarracin M, Constant A, Friston K, Ramstead M. A variational approach to 
scripts. 2020. Available: https://psyarxiv.com/67zy4/download 
120. 
Bouizegarene N, Ramstead M, Constant A, Friston K, Kirmayer L. Narrative 
as active inference. 2020. doi:10.31234/osf.io/47ub6 
121. 
cogsec.org. What is Cognitive Security? In: cogsec.org [Internet]. 2021 [cited 
22 Nov 2021]. Available: https://www.cogsec.org/what-is-cognitive-security 
122. 
Bezuidenhout M, Mouton F, Venter HS. Social engineering attack detection 
model: SEADM. 2010 Information Security for South Africa. 
ieeexplore.ieee.org; 2010. pp. 1–8. doi:10.1109/ISSA.2010.5588500 
123. 
Cordes RJ, Applegate-Swanson S, Friedman DA, Knight VB, Mikhailova A. 
Narrative Information Management. Zenodo. COGSEC; 2021. 
doi:10.5281/zenodo.5573287 
124. 
Wood W. Attitude change: persuasion and social influence. Annu Rev 
Psychol. 2000;51: 539–570. doi:10.1146/annurev.psych.51.1.539 
125. 
Maslow A, Lewis KJ. Maslow’s hierarchy of needs. Salenger Incorporated. 
1987;14: 987–990. Available: 
https://www.researchhistory.org/2012/06/16/maslows-hierarchy-of-needs/ 
126. 
Austin NJE, Rankov NB. Exploratio: Military and Political Intelligence in the 
Roman World from the Second Punic War to the Battle of Adrianople. 
Psychology Press; 1998. Available: 
https://play.google.com/store/books/details?id=NqIeIoHqezUC 
127. 
Bray DA. Knowledge Ecosystems: A Theoretical Lens for Organizations 
Confronting Hyperturbulent Environments. 2007. Available: 
https://papers.ssrn.com/abstract=984600

## Page 68

Active Inference in Modeling Conflict, 2021 
 
66 
128. 
Friedman DA, Cordes RJ. Infinite Games for Infinite Teams. DARPA; 2020 
Jul. 
129. 
cadCAD – A Python package for designing, testing and validating complex 
systems through simulation. [cited 26 Mar 2020]. Available: 
https://cadcad.org/ 
130. 
ForneyLab.jl: Julia package for automatically generating Bayesian inference 
algorithms through message passing on Forney-style factor graphs. Github; 
Available: https://github.com/biaslab/ForneyLab.jl 
131. 
infer-actively. Github; Available: https://github.com/infer-actively


---
*Extraction method: pymupdf*
