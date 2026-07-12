# Full Text: SinglePheromone

> Extracted from `2023_SinglePheromone.pdf`

---

## Page 1

Cognitive Systems Research 80 (2023) 81–89
Available online 17 February 2023
1389-0417/© 2023 The Author(s). Published by Elsevier B.V. This is an open access article under the CC BY license (http://creativecommons.org/licenses/by/4.0/).
A single-pheromone model accounts for empirical patterns of ant colony 
foraging previously modeled using two pheromones 
Eric Saund a, Daniel Ari Friedman b,c,* 
a Saund Laboratories, USA 
b University of California, Davis. Department of Entomology & Nematology, USA 
c Active Inference Institute, USA   
A R T I C L E  I N F O   
Keywords: 
Ant 
Colony 
Foraging 
Pheromone 
Decision-making 
Psychophysics 
A B S T R A C T   
In a 2009 paper, Dussutour et al. proposed that big headed ants (Pheidole megacephala) employ two attractant 
pheromones during foraging: one for exploration and another during food gathering. This claim was consistent 
with, and argued to be supported by, laboratory studies of ant exploration and food-gathering in a Y-maze 
apparatus. The authors measured foraging activity and colony foraging choice in terms of the number of ants 
choosing different branches over time, where experimental conditions modified the history of food availability at 
the end of each branch. They built a two-pheromone mathematical model to account for observed rates and 
proportions of ants traversing the left versus right branch. Here we show that the main reported experimental 
observations can be explained by a one-pheromone model. Our findings show that it is plausible, but unnec­
essary, to hypothesize that these ants employ two distinct pheromones in order to account for the two principal 
results of the Dussutour et al. study, and therefore, the study falls short of dispositive evidence for a two- 
pheromone model. More broadly, we highlight that patterns of animal behavior can be ambiguous with 
respect to sensory and cognitive mechanisms, hopefully motivating future modeling efforts that perform formal 
comparison across models with different structure.   
1. Introduction 
Understanding the sensory, cognitive, and behavioral strategies 
employed by animals is difficult because direct measurements of rele­
vant mechanisms (e.g. chemical, neural) are often impossible to obtain. 
In such cases, investigators can engage in indirect inference via statis­
tical modeling based on limited evidence. These indirect inferences 
about behavioral and cognitive processes are limited by the types of 
measurements available for any given experimental setup, as well as 
constrained by investigators’ conceptions of the possible strategies 
available to organisms in their evolutionary context. In the case of 
eusocial insects such as ants, a great body of field observational data 
supports theoretical frameworks that relate ecological considerations to 
nestmate and colony-level behaviors, and the apparent strategic ratio­
nales behind them (Friedman et al., 2020; Gordon, 2014, 2019; Lanan, 
2014). 
Eusocial insects communicate directly, via physical interactions, as 
well as indirectly through chemical (i.e. pheromone) signaling. This type 
of mass communication via pheromone deposition is a stigmergic 
process, in that it belongs to a class of collective behavioral algorithms 
involving entity-niche feedback processes (Heylighen, 2016a, 2016b; 
Theraulaz & Bonabeau, 1999). To investigate the cognitive bases of ant 
behavior, observational and manipulative experiments can be carried 
out in the field (Fleischmann et al., 2018; Friedman et al., 2018), as well 
as under controlled laboratory settings (Entler et al., 2016; Gordon & 
Mehdiabadi, 1999). 
One well-used experimental paradigm in the behavioral sciences is 
the Y-maze (similar to the T-maze), which presents a binary path choice 
to individuals in the context of a foraging trip. The decisions of any 
forager at the branch point can be influenced by their own history (via 
learning and memory), as well as influenced by prior actions of nest­
mates depositing pheromones near the decision point (Czaczkes, 2018). 
For Y-maze setups and behavioral experiments, direct chemical and 
neurological measurements are often lacking, though the focal phe­
nomena of the study is often related to the chemical or neural basis of 
behavior. In such cases, the qualities and effects of pheromones must be 
inferred from gross behavioral outcomes, and thus importantly hinge on 
degrees of freedom employed in the statistical modeling of empirical 
* Corresponding author. Address: One Shields Avenue, 383 Briggs Hall, Dept. of Entomology, Davis, CA 95616, USA. 
E-mail address: DanielAriFriedman@gmail.com (D. Ari Friedman).  
Contents lists available at ScienceDirect 
Cognitive Systems Research 
journal homepage: www.elsevier.com/locate/cogsys 
https://doi.org/10.1016/j.cogsys.2023.02.005 
Received 27 June 2022; Received in revised form 6 December 2022; Accepted 13 February 2023

## Page 2

Cognitive Systems Research 80 (2023) 81–89
82
results. 
It is well established that some ants deposit pheromone trails as 
behavioral cues to others in foraging for food (Czaczkes et al., 2015; 
Feinerman & Korman, 2017; Gissis et al., 2018; Lanan, 2014). Multi- 
component trail pheromones and other glandular secretions have been 
characterized in many insects including termites (Sillam-Duss`es et al., 
2010; Wen et al., 2014) and ants (Cerd´a et al., 2014) (e.g. in pharaoh 
ants, (Jackson et al., 2006, 2007), in Pheidole (Ali et al., 2007)). In 
multiple ant species, multiple pheromones and blends of pheromones 
are used in different contexts, serving different behavioral functions 
(Czaczkes et al., 2015; Robinson et al., 2008). Confidence in these 
conclusions, specifically about the type and influence of pheromones 
that ants use, depends on an inferential chain of evidence and assump­
tions that are best continually re-examined for soundness. 
Here we consider the stigmergic regulation of foraging activity in the 
ant species Pheidole megacephala. We review the two-pheromone model 
(2PM) of foraging activity proposed by Dussutour et al. 2009 (Dussutour 
et al., 2009), and provide an alternative one-pheromone model (1PM) 
involving plausible sensory-cognitive mechanisms. This work, in the 
spirit of methodological refinement, suggests specific followup experi­
ments that could disambiguate the 1PM and 2PM, and highlights that 
alternative models of animal cognition (including stigmergic mecha­
nisms of collective cognition) must be formally compared in order to 
draw well-founded conclusions. 
2. The two-pheromone model (2PM) 
This section reviews the two-pheromone model (2PM) presented in 
Dussutour et al. (2009), as well as the primary behavioral experiments 
involving the ant species Pheidole megacephala performed in that work. 
The 2PM model of ant colony foraging proposes that there are two 
chemically-distinct pheromones, both of which are attractants for for­
agers (e.g. biasing the nestmate to forage in the direction where 
attractant pheromones are at higher concentration). The first hypothe­
sized pheromone is named the “exploration pheromone” (E), and is 
described as “a long-lived signal that acts as an ‘external long-term 
memory’ of the environment allowing the colony to rapidly establish a 
new trail.” Functionally, this E pheromone is hypothesized to allow “the 
colony to more quickly mobilize foragers when food is discovered.” The 
second hypothesized pheromone is named “foraging pheromone” (F) 
which “evaporate[s] quickly allowing the colony to abandon a depleted 
food source.” 
The exponential decay times of the E and F pheromones are esti­
mated. However, direct chemical measurements are not presented in 
this study (and from literature searching, we were unable to find fol­
lowup experiments providing any chemical measurements of 
P. megacephala trails). Additionally in the 2PM, the authors make “two 
assumptions about the interaction between the pheromones.” The first 
assumption is that “the exploration pheromone [E] has a positive feed­
back on the deposition of foraging pheromone [F].” The second 
assumption made by the authors is that “the foraging pheromone [F] has 
a negative feedback on the deposition of exploration pheromone [E].” 
The authors use this 2PM to fit empirical behavioral observations of 
P. megacephala made in the laboratory in the Y-maze paradigm. Below, 
we will describe and evaluate the relevant empirical findings, and 
contrast the 2PM with a 1PM. The 1PM model we propose accounts for 
the observed data in a way that is both parsimonious and biologically 
realistic. The important note to make here, which will be explored in 
greater detail in the Discussion, is that the assertion of a model’s a priori 
plausibility and consistency with empirical data does not constitute 
dispositive evidence that the model is superior to alternative models, 
absent direct consideration among specified plausible models. 
3. Experimental patterns of colony foraging 
Here we present the experiments conducted by Dussutour et al. 
(2009), and describe how the 2PM is used to interpret the results. The 
authors conducted four experiments, numbered 1–4. The 2PM is intro­
duced through the first two experiments, then shown to be consistent 
with the fourth. Their Experiment 3 is tightly coupled to assumptions of 
their model hypothesis and we do not address it here. 
3.1. Experiment 1 and Experiment 2 
Experiment 1 and Experiment 2 compare ant colony foraging 
behavior under different combinations of three treatments of the Y-maze 
branches (Exploration plus Foraging [E + F], Exploration [E], and Not 
explored [N]). In both experiment 1 and 2, the colony engages first in 
exploration of one of the maze branches (Branch A), followed by a one 
hour “foraging phase.” In each experiment, following the foraging 
phase, a second branch (Branch B) is added at the decision line, giving 
rise to a “test phase.” During the test phase, after choosing a branch, 
“ants walking towards each branch were gently removed with a paint­
brush as they crossed the decision line to prevent reinforcement of either 
branch.” 
The E + F treatment is consistent on Branch A between the two ex­
periments, which differ in the history of the second branch, Branch B. 
The experimental paradigm is illustrated in their Fig. 1 (reproduced here 
in Fig. 1a*). 
In Experiment 1, Branch B was novel and unexplored (N treatment), 
and there was no opportunity for ants to mark the path in advance of the 
experimental trial. The authors measure and plot the proportion of ants 
choosing the E + F versus N branches during the test phase. Essentially 
this experiment measures the effect of pheromone deposited during 
food-gathering on decision-making at the decision juncture, comparing 
marked and unmarked branches. 
In Experiment 2, Branch B at test time had been explored, and pre­
sumably marked by some stigmergic mechanism, by a sister subcolony 
during the Exploration-foraging phase (E treatment). The authors mea­
sure and plot the proportion of ants choosing the E + F versus E branches 
during the test phase, where the E branch had the opportunity to be 
marked under exploration but no food had been placed. 
The results from Experiment 1 and 2 are shown in their Fig. 2 (Fig. 1b 
here). The salient observation is that in the E + F vs E condition, pref­
erence for the E + F branch drops off within 25 min, while in the E + F vs 
N condition, preference for the E + F branch persists for about 90 min. 
They proceed to build a mathematical model assuming two distinct 
pheromones, one for exploration (E) and another for exploitation 
(foraging, F). Under this 2PM model, they estimate decay rates for these 
respective hypothesized pheromones. 
In their Discussion, with respect to the divergence between the paths 
in their Fig. 2 (Fig. 1b here) the authors write, “the observation that the 
initial frequency of ants choosing the E + F branch is the same in the E +
F vs N and E + F vs E experiments but these frequencies diverge after 15 
min ([Dussutour et al.] Fig. 2) is difficult to explain with a single 
pheromone.” That the (unpublished) difficulty of constructing a single 
pheromone model is taken as part of the “behavioral evidence that 
P. megacephala uses two different pheromones,” is our central contention 
and focus of the following modeling. 
4. A One-Pheromone Model (1PM) 
In contrast with the authors’ claims that these patterns are “difficult 
to explain with a single pheromone,” here we formulate a one- 
pheromone Model (1PM) that accounts for the observed experimental 
results using a single attractant pheromone. 
The 1PM model incorporates four main assumptions, which are 
grounded in biologically plausible mechanisms of insect perception, 
* Dussutour et al. (2009) Figs. 1, 2, 10 reproduced with permission, Journal 
of Experimental Biology. 
E. Saund and D. Ari Friedman

## Page 3

Cognitive Systems Research 80 (2023) 81–89
83
cognition, and action.  
1. First, we posit that ants deposit a single attractant pheromone 
whether exploring (E) or exploiting/gathering food (which Dussu­
tour et al. call foraging, F). This is the crux of the difference between 
the 2PM and 1PM. We assume that ants deposit more of the phero­
mone when returning from a found resource (this could be on the 
return trip, verifying the presence of a seed) than if they do not find 
food, leaving stronger pheromone trails on paths leading to food.  
2. Second, as with the 2PM, we assume that pheromone concentration 
decays exponentially with time.  
3. Third, we model the perception of the downstream pheromone signal 
(e.g. behavioral impact) as a nonlinear amplification of pheromone 
concentrations. Amplification is stronger at lower pheromone levels, 
so the amplification curve will be concave downward (see Fig. 3). 
This type of signal amplification has been found commonly to govern 
sensory perception across species (Billock & Havig, 2018), and it is 
an established feature of the insect olfactory system (Gorur-Shandi­
lya et al., 2017; Singh et al., 2019). Such methods have previously 
been applied to ant foraging (e.g. in the case of path selection in 
Argentine ants by (von Thienen et al., 2015)).  
4. Fourth, we model branch preference (choice behavior) as related to 
the absolute difference in perceived pheromone concentration, 
rather than the ratio of pheromone perceived on each branch. This 
difference measurement is modulated by the robustness of the signal; 
under weaker levels of pheromone overall, deciding about the 
stronger branch is less certain and so the foragers behave as to hedge 
their bets by allocating traversals down both branches. 
In the following paragraphs, we provide a qualitative overview of the 
1PM. Following that, we present the mathematical details and compu­
tational implementation of the 1PM and perform parameter fitting based 
upon the experimental results of Dussutour et al., 2009. 
4.1. A qualitative overview of the 1PM 
Qualitatively, the pattern observed in Experiment 1 and Experiment 
2 of Dussutour et al. (their Fig. 2) is explained under a 1PM as follows. 
Assume that exploration (E) involves depositing pheromone, but 
exploitation (E + F) deposits substantially more so. At the outset, the 
pheromone signal from the E + F treatment is robustly stronger than 
either the E treatment or N (no prior ant traversal). The initial preference 
is therefore strong for the E + F branch under both experimental 
conditions. 
Then, under exponential decay of pheromone (an assumption com­
mon to 1PM and 2PM), even initially high amounts of pheromone 
rapidly decay in strength. In Experimental condition 2, the E + F and E 
signals both weaken, but under nonlinear amplification, the signal dif­
ference between the measurements becomes smaller rapidly, reducing 
to negligible within 25 min. By contrast, in Experiment 1 the difference 
between the weakened – yet amplified – E + F signal and background 
noise level (N treatment), persists until the pheromone evaporates 
almost completely at 90 min. The following sections elaborate on this 
qualitative explanation with a one-pheromone mathematical and 
simulation model, based upon the exact empirical results presented by 
Dussutour et al. (2009). 
4.2. Mathematical formulation and simulation of the One-Pheromone 
Model 
Mathematically, the One-Pheromone Model (1PM) presented here 
consists of two stages, a measurement stage which includes non-linear 
signal amplification, and a preference stage which leads to action se­
lection. We choose functional forms and parameters for each of these 
stages based on the data presented in Dussutour’s Fig. 2. 
In general, the overall composed preference function (including both 
amplification and preference stages) can be expressed as: 
Fig. 1. a. Dussutour et al. Fig. 1, showing the setup of Experiment 1 and 2. b. Dussutour et al. Fig. 2 showing the results of Experiment 1 and 2.  
E. Saund and D. Ari Friedman

## Page 4

Cognitive Systems Research 80 (2023) 81–89
84
pA = f(phA, phB)
(1)  
where pA is the probability of an ant choosing Branch A, estimated by the 
fraction of ants observed on Branch A in any interval (as per the Y-axis of 
Fig. 1B). The variables phA and phB are the amount of pheromone 
physically present on branches A and B, respectively. 
The preference function can be visualized as a surface in two- 
dimensions (where phA and phB are the X and Y axes, and pA is the 
elevation on that landscape). The Dussutour et al. experiments do not 
tell the entire shape of this surface, but they do provide data points for 
two paths across it. This data is sufficient to constrain a plausible 
analytical one-pheromone model entailing a handful of degrees of 
freedom whose parameters can be chosen to fit the data. 
To motivate the functional form of a single pheromone model, 
consider a plot of the observed preference fraction on a two-dimensional 
plane, as shown in Fig. 2. The horizontal (phA) axis is the amount of 
pheromone present on the E + F branch. The vertical (phB) axis is the 
amount of pheromone on the other branch. Under the N treatment 
(Experiment 1), this is always at some noise level. Under the E treatment 
(Experiment 2) phB will decay from some non-negligible amount of 
pheromone. 
Since we have no direct measurement of the amount of pheromone 
present, for the purposes of modeling we assume some initial amount of 
pheromone at the outset, with exponential decay through time down to 
the noise level. Pheromone decay or evaporation produces tracks of 
circles in Fig. 2. In Fig. 2, we choose an arbitrary scale for the initial 
pheromone amount, such that initially the E + F treatment has a value of 
10. Under an assumption that exploration deposits less pheromone than 
exploitation, we choose the value 1 for the initial E treatment phero­
mone amount. These precise values do not matter for the structure of the 
argument; what matters is the assumption that the E branch has less 
pheromone than the E + F branch. 
The exponential decay rate can be estimated from the time it takes 
for pheromone to evaporate from the initial value to the noise level. For 
example, if the initial F + E decays to a noise level 1/500 as strong over 
90 min, then the decay rate is approximately −0.069 per minute. Due to 
exponential decay, most of the pheromone amounts are very small. 
Hence we display the values at three different scales, successively from 
left to right. 
Biological sensors are in general designed to cover great dynamic 
range in the values of the property measured. For ecological utility, it is 
likely that ants have evolved to measure very scant amounts of phero­
mone. In other words, an ant’s pheromone sensor is likely, to some 
extent, to invert the exponential loss of signal strength over time seen in 
Fig. 2. We suggest that this inversion takes the form of a power law 
amplification as shown in Fig. 3. 
Under this amplification, the paths of Experiment 1 and 2 shown in 
Fig. 2, spread out more evenly as shown in Fig. 4. 
The transition from biased preference (large circles) to equal pref­
erence (small circles) is neither sharp nor a linear relationship. Instead, 
it presents more like a soft threshold whose height profile (in the range 
0.5–1.0) in the ph′
A-ph′
B plane can be modeled by a product of two sig­
moid squashing functions as illustrated in Fig. 5, and as explained below. 
f(ph′
A, ph′
B) = σ′
m(dm(ph′
A, ph′
B)) × σ′
r(dr(ph′
A, ph′
B)) + 1
2
(2) 
The two sigma functions σ′are the standard logistic function, with 
parameters for slope, offsets, and range. 
σ′
m(x) =
1
1 + exp(−sm(x −d0m)) −
1
1 + exp(smd0m))
(3)  
σ′
r(x) = s0 + (1 −s0)
1
1 + exp(−sr(x −d0r))
(4) 
The distance functions, dm(ph′
A,ph′
B)and dr(ph′
A,ph′
B), are distances on 
the ph′
A- ph′
B plane to the sigmoid functions’ offset curves, d0m, and d0r, 
respectively. 
The σ′
m term gauges distance from the midline ph′
A = ph′
B, where 
there is equal amount of pheromone on each branch, and hence, ants 
will prefer neither branch. The offset term, d0m, sets the width of a 
channel of proximity to the midline, within which the amounts of 
pheromone are considered similar enough to drive preference for 
Fig. 2. Empirical observations from Dussutour experiments assuming a one-pheromone model. Horizontal axis is the concentration of pheromone on branch A (phA), 
vertical axis is the concentration of pheromone on branch B (phB) – Note the Y axis scale changes across the 3 graphs. Circles depict tracks of amount of hypothesized 
pheromone over time, for Experiments 1 and 2, under exponential evaporation. Lacking empirical data, we choose plausible relative initial values (farthest right 
circles in the leftmost, zoomed out plot) of 10 and 1, respectively, for phA and phB in the E + F versus E condition (Experiment 2). Circle diameter is choice preference, 
where large diameter is 1.0 (total preference) and small diameter is 0.5 (no preference). The values depicted as circle sizes were read off from Dussutour Fig. 2. 
E. Saund and D. Ari Friedman

## Page 5

Cognitive Systems Research 80 (2023) 81–89
85
Fig. 3. Proposed pheromone measurement function M is a power-law amplification of the raw pheromone level ph, subtracting a small base level noise factor, B.  
Fig. 4. The data of Fig. 2 (derived from Dussutour et al. Fig. 2) under power law sensory amplification using parameter values A = 5.5, B = 0.02, C = 0.25.  
E. Saund and D. Ari Friedman

## Page 6

Cognitive Systems Research 80 (2023) 81–89
86
neither branch versus the other. 
The σ′
r term gauges robustness in the combined amount of phero­
mone present in terms of distance from the origin where ph′
A = ph′
B = 0. 
The offset term, d0r, sets the amount of pheromone above which the 
difference between the two branches becomes robustly distinguishable. 
Below pheromone amounts d0r, there is a limit imposed (by the s0 term) 
on the degree of preference for either branch. A typical value for this 
parameter sets this limit at about 0.8, or a ceiling of 80% preference 
when the total pheromone level is weak. 
The product of these terms in Eq. (2) models that strong branch 
preference occurs under a conjunction of two factors: (r) sufficient 
amplified pheromone signal is transmitted to robustly measure any 
differences between the two branches, and (m) the signal difference 
between the two branches is significant. 
Consequently, the model expresses preference for the E + F branch 
(larger circles) when the amplified E + F signal is significantly greater 
Fig. 5. Modeling the branch preference function as a product of sigmoid squashing functions.  
Fig. 6. a. Simulated trajectories of pheromone amounts and measurements under the one-pheromone model. Blue: Hypothetical physical pheromone amount for E +
F branch. Orange: Hypothetical physical pheromone amount for E branch. Lower magenta: physical pheromone amount for N branch (noise level). Green: amplified 
pheromone measurement for E + F branch. Upper magenta: amplified pheromone measurement for E branch. b. Preference fractions for the E + F vs N (Blue, 
Experiment 1) and E + F vs E (Red, Experiment 2) conditions, plotted over Dussutour et al. Fig. 2. Parameter values were found by manual adjustment and are listed 
in the Table of Parameter Values, below. (For interpretation of the references to colour in this figure legend, the reader is referred to the web version of this article.). 
E. Saund and D. Ari Friedman

## Page 7

Cognitive Systems Research 80 (2023) 81–89
87
than the alternative signal, that is, for data points at greater distance 
from the ph′
A = ph′
B midline. And, the strongest preference for the E + F 
branch (largest circles) occurs when the total signal is greatest, as re­
flected in distance from the origin. This consideration is reflected in the 
“bump” in the decay of the E + F vs N plot in Dussutour’s Fig. 2. Values 
for the free parameters of the model can be found by manual adjustment 
or by numerical optimization. 
With respect to their Fig. 2, Dussutour et al. write: “For example, the 
observation that the initial frequency of ants choosing the E + F branch 
is the same in the E + F vs N and E + F vs E experiments but these 
frequencies diverge after 15 min (Fig. 2) is difficult to explain with a 
single pheromone.” Under the single-pheromone measurement and 
preference model presented here, a simulation of ant behavior yields 
trajectories of pheromone amounts and amplified signals as shown in 
Fig. 6a. The resulting preference curves are shown in Fig. 6b, plotted on 
top of Dussutour Fig. 2 to demonstrate the close fit. 
Clearly, a one-pheromone model can very handily account for the 
observation that the initial frequency of ants choosing the E + F branch 
is the same in the E + F vs N and E + F vs experiments but these fre­
quencies diverge after 15 min. 
4.3. Dynamic environment experiment 
Dussutour et al. performed another experiment, Experiment 4, called 
“dynamic environment,” in which they switch food between left and 
right branches and observe the time course of ant preference for each 
branch. This data is presented in their Fig. 10. They postulate that 
redirection to the food-containing branch is due to feedback modulation 
of the deposit of exploitation pheromone (F) in relation to exploration 
pheromone (E): “The model showed that the existence of negative 
feedback of foraging pheromone on the production of exploration 
pheromone allows an efficient switch back to the path where the source 
was located previously, after the intermediate period of unavailability of 
this source (2nd switch in our experiment).” 
We find that a one-pheromone model is also able to account for the 
dynamic environment experimental result. We conducted a simulation 
of Dussutour et al. Experiment 4, with ant preference following the 
model above, and pheromone deposit occurring at a rate of 0.01 per ant 
on food branches (exploitation, F) and 0.001 per ant on no-food 
branches (exploration, E). Going by Dussutour’s report, we set total 
ant traffic in the range of 50/min. Under the model parameters used to 
fit Dussutour’s Fig. 2, we arrive at the preference curve of Fig. 7a. 
Notably, ant preference does flip with change of food location. But 
this curve shows some different features such as a significant branch 
indifference “shelf” when switching branches. It is possible however to 
fit model parameters using numerical optimization methods, still using 
the one-pheromone model formulation (see Numerical Method, Code & 
Data Availability section, for details). An example is shown in Fig. 7b. 
Here, a constrained BFGS method was used to optimize model param­
eters for dynamic environment experimental data read from Dussutour 
et al. Fig. 10. The parameters, dexploit and dexplore are simulated phero­
mone deposit rates for ants on Food and No-food branches, respectively. 
Obviously, any empirical curves can be fit under appropriate model 
structure given enough parameters. The model proposed here may be 
considered a member of a family of analytical forms whose parameters 
are relatively few and based in the principles of the domain. In general, 
good fits are obtained when parameter values are adjusted by 50% or 
more in trade-off with one another. In this way, the model is not 
dependent on precise adjustment of any parameter. Rather, well-fitting 
parameter values form a lower-dimensional manifold that is a projection 
down from the full parameter space. Through numerical optimization, a 
single set of values can be found that reasonably fits both Dussutour 
et al. Fig. 2 and Fig. 10. This is shown in Fig. 8. 
5. Discussion & conclusions 
Here we have described the two-pheromone model (2PM) that was 
used by Dussutour et al. (2009) to model the stigmergic regulation of 
colony foraging behavior in big headed ants (Pheidole megacephala). We 
then propose an alternative one-pheromone model (1PM), which ac­
counts for experimental evidence that was previously used to justify a 
conclusion that P. megacephala uses two pheromones to manage group 
exploration and exploitation of a food source (Dussutour et al., 2009). 
Our approach brings a two-stage computational model that decouples 
signal amplification from choice preference decision. Methodologically, 
we placed the computation in a general framework, then worked 
backward from experimental data to infer a plausible decision strategy 
that could easily be implemented in a simple nervous system. 
In their abstract the authors write that they “establish that the ants’ 
behavior is consistent with the use of two different pheromone signals, 
both of which recruit nestmates.” We bring no contention against the 
claim that the empirical findings are “consistent” with a 2PM, and we 
also concur with the authors in that it is plausible that foraging trails 
consist of multiple chemical components with differential volatility and 
behavioral impacts (Czaczkes et al., 2015). Indeed, to the limited extent 
that glandular contents have been chemically analyzed in P. megacephala 
Fig. 7. a. Simulation of Dussutour et al. Experiment 4 under a one-pheromone model, using parameters estimated above to match empirical results from their 
Experiments 1 and 2. Simulated branch preference (Red) is plotted on top of Dussutour Fig. 10. b. Simulation of Dussutour et al. Experiment 4 using parameters found 
by numerical optimization to better fit the observed time course of branch preference switching. Optimized parameter values are listed in the table. (For inter­
pretation of the references to colour in this figure legend, the reader is referred to the web version of this article.) 
E. Saund and D. Ari Friedman

## Page 8

Cognitive Systems Research 80 (2023) 81–89
88
(e.g. Dufour gland in (Ali et al., 2007)), there are multiple components. 
Our concern arises from the Discussion section, where the claim is made 
that the modeled results provide “behavioral evidence that 
P. megacephala uses two different pheromones, a long-lasting phero­
mone during exploration and a short-lasting foraging pheromone during 
recruitment to a food source.” Our concern is both methodological and 
substantive. Without explicit comparison among alternative models 
with different number of pheromone components, the finding that the 
2PM is consistent with the empirical results (per the claim in the Ab­
stract) cannot be taken to constitute positive evidence for a two- 
pheromone foraging mechanism (as claimed in the Discussion). 
Regardless of the direct reading or interpretation of the original text, in 
subsequent literature, the experiments of Dussutour et al. have been 
widely cited specifically as positive evidence that ants use two phero­
mones in their foraging trails (e.g. (Czaczkes et al., 2015; Flanagan et al., 
2013; Hills et al., 2015; Jeanson et al., 2012; Kolay et al., 2020; Lanan, 
2014; Ma et al., 2013; Malíˇckov´a et al., 2015; Middleton & Latty, 2016; 
Vogel et al., 2015; Zabzina et al., 2014)). 
Our model is certainly subject to overhaul, and the small number of 
free parameters would benefit from further adjustment with more data. 
In particular, the Dussutour et al. experiments cover only a small portion 
of the phA - phB plane of differential pheromone levels on the two 
branches of the Y-maze. It would be informative to gather branch 
preference data for other regions of this space. 
In their paper, Dussutour et al. do not show predictions from their 
2PM model charting the time course of ants’ collective Y-maze branch 
choice as measured and presented in their Figs. 2 and 10, so it is 
impossible to compare our 1PM model with theirs on this basis. None­
theless, yet other experiments could be performed to distinguish our 
1PM models from theirs or others. For example, Dussuotour et al. report 
that, under some circumstances, their 2PM model predicts oscillations of 
pheromone concentrations when ants are presented with two branches 
both containing food. Our model makes a different prediction, namely 
that traffic and pheromone deposition equalizes without oscillation. 
Additionally, the two branch Y-maze experimental setup could be 
extended to three or more branches. Other experimental variations 
would involve lengthening or shortening branches, and varying envi­
ronmental conditions such as temperature, lighting, surface properties, 
etc. In such cases, our current 1PM aggregate simulation would need to 
be enhanced toward an agent-based modeling framework, whereby in­
dividual simulated ants would traverse simulated paths and make sto­
chastic decisions at branches. 
The Y-maze paradigm itself merits methodological reflection, as well 
as consideration of the best practices for this experimental setup 
(Czaczkes, 2018). It assumes that ant traffic is primarily governed by the 
physical presence of pheromone underfoot, and further, that this pher­
omone is unaffected by individuals during the experimental test phase. 
This assumption would not necessarily hold, however, if ants deposit 
some pheromone on their outgoing trip before being brushed off the 
trail. Ideally, the presence and composition of pheromone would be 
measured independently by a physical sensing apparatus throughout the 
experiment. 
Another consideration is the microstructure of sensing and decision- 
making at the decision line. How does an ant know how much phero­
mone lies ahead on each alternative path? Do they interrogate each path 
for some distance, then backtrack to test the other? Methods such as 
high-speed, high-resolution video capture and analysis offer promise in 
deciphering insects’ sensory-decision machinery (Mueller et al., 2019; 
Walter & Couzin, 2021). 
Limited gross behavioral data places only weak constraint on hy­
potheses about the physical, sensory, and cognitive mechanisms un­
derlying complex observed behaviors. For this reason, it is incumbent to 
formally and rigorously consider alternative accounts. Similar to sta­
tistical power analysis, behavioral experiments need to search in 
experimental phase space in an informed way. Another path forward is 
to use integrated frameworks for ant colony cognitive modeling such as 
Active InferAnts (Friedman et al., 2021), that can be elaborated to 
encompass various sensory-cognitive phenomena as technology ad­
vances and new experiments are performed. 
Table of Parameter Values.  
Ref. Figure 
Figs. 6, 7a 
Fig. 7b 
Fig. 8 
parameter selection 
method 
manual 
adjustment 
num. optimization 
num. optimization 
A 
5.5 
2.27 
4.92 
B (noise level) 
0.02 
0.02 
0.02 
C 
0.25 
0.264 
0.298 
phA0 
10.0 
10.0 
10.0 
phB0 
1.0 
1.0 
1.55 
sm 
4.0 
0.687 
1.58 
d0m 
2.0 
2.1 
1.61 
s0 
0.6 
0.261 
0.617 
sr 
0.8 
1.93 
1.81 
d0r 
8.0 
9.4 
7.71 
dexploit 
0.011 
1.0 
0.0082 
dexplore 
0.0011 
0.001 
0.001  
Fig. 8. One-pheromone model simulations using a common set of parameter values optimized for Dussutour et al.’s Experiments 1, 2, and 4 as provided in their Figs. 
2 and 10. Parameter values are listed in the table. 
E. Saund and D. Ari Friedman

## Page 9

Cognitive Systems Research 80 (2023) 81–89
89
Numerical Method, Code & Data Availability 
Code and Data for this article can be found at https://github. 
com/docxology/ant-pheromone. 
The program is written in Python. Numerical optimization is done 
using the optimize.minimize function of the SciPy scientific computing 
library. Optimization method used is l-BFGS-B (Limited-memory Broy­
den–Fletcher–Goldfarb–Shanno method with Box constraints). This 
method allows for hard bounding of certain parameter values. noise_­
level was clamped at 0.02. Value optimized is sum squared error be­
tween model prediction and empirical data as read from Dussutour et al. 
figures. Starting parameter values for optimization were the initial 
parameter values of Fig. 6 set by manual adjustment. 
Funding 
DAF was supported by the USA National Science Foundation (grant 
award 2010290). 
Declaration of Competing Interest 
The authors declare that they have no known competing financial 
interests or personal relationships that could have appeared to influence 
the work reported in this paper. 
References 
Ali, M. F., Jackson, B. D., & Morgan, E. D. (2007). Contents of the poison apparatus of 
some species of Pheidole ants. Biochemical Systematics and Ecology, 35(10), 641–651. 
https://doi.org/10.1016/j.bse.2007.03.025 
Billock, V. A., & Havig, P. R. (2018). A simple power law governs many sensory 
amplifications and multisensory enhancements. Scientific Reports, 8(1), 7645. 
https://doi.org/10.1038/s41598-018-25973-w 
Cerd´a, X., van Oudenhove, L., Bernstein, C., & Boulay, R. R. (2014). A list of and some 
comments about the trail pheromones of ants. Natural Product Communications, 9(8), 
1115–1122. https://www.ncbi.nlm.nih.gov/pubmed/25233585. 
Czaczkes, T. J. (2018). Using T- and Y-mazes in myrmecology and elsewhere: A practical 
guide. Insectes Sociaux, 65(2), 213–224. https://doi.org/10.1007/s00040-018-0621- 
z 
Czaczkes, T. J., Grüter, C., & Ratnieks, F. L. W. (2015). Trail pheromones: An integrative 
view of their role in social insect colony organization. Annual Review of Entomology, 
60(October), 581–599. https://doi.org/10.1146/annurev-ento-010814-020627 
Dussutour, A., Nicolis, S. C., Shephard, G., Beekman, M., & Sumpter, D. J. T. (2009). The 
role of multiple pheromones in food recruitment by ants. The Journal of Experimental 
Biology, 212(Pt 15), 2337–2348. https://doi.org/10.1242/jeb.029827 
Entler, B. V., Cannon, J. T., & Seid, M. A. (2016). Morphine addiction in ants: A new 
model for self-administration and neurochemical analysis. The Journal of 
Experimental Biology, 219(Pt 18), 2865–2869. https://doi.org/10.1242/jeb.140616 
Feinerman, O., & Korman, A. (2017). Individual versus collective cognition in social 
insects. The Journal of Experimental Biology, 220(Pt 1), 73–82. https://doi.org/ 
10.1242/jeb.143891 
Flanagan, T. P., Pinter-Wollman, N. M., Moses, M. E., & Gordon, D. M. (2013). Fast and 
flexible: Argentine ants recruit from nearby trails. PloS One, 8(8), e70888. 
Fleischmann, P. N., R¨ossler, W., & Wehner, R. (2018). Early foraging life: Spatial and 
temporal aspects of landmark learning in the ant Cataglyphis noda. Journal of 
Comparative Physiology. A, Neuroethology, Sensory, Neural, and Behavioral Physiology, 
204(6), 579–592. https://doi.org/10.1007/s00359-018-1260-6 
Friedman, D. A., Johnson, B. R., & Linksvayer, T. A. (2020). Distributed physiology and 
the molecular basis of social life in eusocial insects. Hormones and Behavior, 122, 
Article 104757. https://doi.org/10.1016/j.yhbeh.2020.104757 
Friedman, D. A., Pilko, A., Skowronska-Krawczyk, D., Krasinska, K., Parker, J. W., 
Hirsh, J., & Gordon, D. M. (2018). The role of dopamine in the collective regulation 
of foraging in harvester ants. iScience, 8, 283–294. https://doi.org/10.1016/j. 
isci.2018.09.001 
Friedman, D., Tschantz, A., Ramstead, M. J. D., Friston, K., & Constant, A. (2021). Active 
inferants: The basis for an active inference framework for ant colony behavior. 
Frontiers in Behavioral Neuroscience, 15, 126. https://doi.org/10.3389/ 
fnbeh.2021.647732 
Gissis, S. B., Lamm, E., & Shavit, A. (2018). Landscapes of Collectivity in the Life 
Sciences. MIT Press. https://play.google.com/store/books/details?id=WPp 
FDwAAQBAJ. 
Gordon, D. M. (2014). The ecology of collective behavior. PLoS Biology, 12(3), e1001805. 
Gordon, D. M. (2019). The ecology of collective behavior in ants. Annual Review of 
Entomology, 64, 35–50. https://doi.org/10.1146/annurev-ento-011118-111923 
Gordon, D. M., & Mehdiabadi, N. J. (1999). Encounter rate and task allocation in 
harvester ants. Behavioral Ecology and Sociobiology, 45(5), 370–377. https://doi.org/ 
10.1007/s002650050573 
Gorur-Shandilya, S., Demir, M., Long, J., Clark, D. A., & Emonet, T. (2017). Olfactory 
receptor neurons use gain control and complementary kinetics to encode 
intermittent odorant stimuli. eLife, 6. https://doi.org/10.7554/eLife.27670 
Heylighen, F. (2016a). Stigmergy as a universal coordination mechanism I: Definition 
and components. Cognitive Systems Research, 38, 4–13. https://doi.org/10.1016/j. 
cogsys.2015.12.002 
Heylighen, F. (2016b). Stigmergy as a universal coordination mechanism II: Varieties 
and evolution. Cognitive Systems Research, 38, 50–59. https://doi.org/10.1016/j. 
cogsys.2015.12.007 
Hills, T. T., Todd, P. M., Lazer, D., Redish, A. D., Couzin, I. D., & Cognitive Search 
Research Group. (2015). Exploration versus exploitation in space, mind, and society. 
Trends in Cognitive Sciences, 19(1), 46–54. https://doi.org/10.1016/j. 
tics.2014.10.004 
Jackson, D. E., Martin, S. J., Holcombe, M., & Ratnieks, F. L. W. (2006). Longevity and 
detection of persistent foraging trails in Pharaoh’s ants, Monomorium pharaonis (L.). 
Animal Behaviour, 71(2), 351–359. https://doi.org/10.1016/j.anbehav.2005.04.018 
Jackson, D. E., Martin, S. J., Ratnieks, F. L. W., & Holcombe, M. (2007). Spatial and 
temporal variation in pheromone composition of ant foraging trails. Behavioral 
Ecology: Official Journal of the International Society for Behavioral Ecology, 18(2), 
444–450. https://doi.org/10.1093/beheco/arl104 
Jeanson, R., Dussutour, A., & Fourcassi´e, V. (2012). Key factors for the emergence of 
collective decision in invertebrates. Frontiers in Neuroscience, 6, 121. https://doi.org/ 
10.3389/fnins.2012.00121 
Kolay, S., Boulay, R., & d’Ettorre, P. (2020). Regulation of ant foraging: A review of the 
role of information use and personality. Frontiers in Psychology, 11, 734. https://doi. 
org/10.3389/fpsyg.2020.00734 
Lanan, M. (2014). Spatiotemporal resource distribution and foraging strategies of ants 
(Hymenoptera: Formicidae). Myrmecological News / Osterreichische Gesellschaft Fur 
Entomofaunistik, 20, 53–70. https://www.ncbi.nlm.nih.gov/pubmed/25525497. 
Malíˇckov´a, M., Yates, C., & Boďov´a, K. (2015). A stochastic model of ant trail following 
with two pheromones. In arXiv [physics.bio-ph]. arXiv. http://arxiv.org/abs/1 
508.06816. 
Ma, Q., Johansson, A., Tero, A., Nakagaki, T., & Sumpter, D. J. T. (2013). Current- 
reinforced random walks for constructing transport networks. Journal of the Royal 
Society, Interface / the Royal Society, 10(80), 20120864. https://doi.org/10.1098/ 
rsif.2012.0864 
Middleton, E. J. T., & Latty, T. (2016). Resilience in social insect infrastructure systems. 
Journal of the Royal Society, Interface / the Royal Society, 13(116). https://doi.org/ 
10.1098/rsif.2015.1022 
Mueller, J. M., Ravbar, P., Simpson, J. H., & Carlson, J. M. (2019). Drosophila 
melanogaster grooming possesses syntax with distinct rules at different temporal 
scales. PLoS Computational Biology, 15(6), e1007105. 
Robinson, E. J. H., Green, K. E., Jenner, E. A., Holcombe, M., & Ratnieks, F. L. W. (2008). 
Decay rates of attractive and repellent pheromones in an ant foraging trail network. 
Insectes Sociaux, 55(3), 246–251. https://doi.org/10.1007/s00040-008-0994-5 
Sillam-Duss`es, D., S´emon, E., Robert, A., Cancello, E., Lenz, M., Valterov´a, I., & 
Bordereau, C. (2010). Identification of multi-component trail pheromones in the 
most evolutionarily derived termites, the Nasutitermitinae (Termitidae). Biological 
Journal of the Linnean Society. Linnean Society of London, 99(1), 20–27. https://doi. 
org/10.1111/j.1095-8312.2009.01348.x 
Singh, V., Murphy, N. R., Balasubramanian, V., & Mainland, J. D. (2019). Competitive 
binding predicts nonlinear responses of olfactory receptors to complex mixtures. 
Proceedings of the National Academy of Sciences of the United States of America 116(19), 
9598–9603. https://doi.org/10.1073/pnas.1813230116. 
Theraulaz, G., & Bonabeau, E. (1999). A brief history of stigmergy. Artificial Life, 5(2), 
97–116. https://doi.org/10.1162/106454699568700 
Vogel, D., Nicolis, S. C., Perez-Escudero, A., Nanjundiah, V., Sumpter, D. J. T., & 
Dussutour, A. (2015). Phenotypic variability in unicellular organisms: From calcium 
signalling to social behaviour. Proceedings. Biological Sciences / The Royal Society, 282 
(1819), 20152322. https://doi.org/10.1098/rspb.2015.2322 
von Thienen, W., Metzler, D., & Witte, V. (2015). Modeling shortest path selection of the 
ant Linepithema humile using psychophysical theory and realistic parameter values. 
Journal of Theoretical Biology, 372, 168–178. https://doi.org/10.1016/j. 
jtbi.2015.02.030 
Walter, T., & Couzin, I. D. (2021). TRex, a fast multi-animal tracking system with 
markerless identification, and 2D estimation of posture and visual fields. eLife, 10. 
https://doi.org/10.7554/eLife.64000 
Wen, P., Ji, B.-Z., & Sillam-Duss`es, D. (2014). Trail communication regulated by two trail 
pheromone components in the fungus-growing termite Odontotermes formosanus 
(Shiraki). PloS One, 9(3), e90906. 
Zabzina, N., Dussutour, A., Mann, R. P., Sumpter, D. J. T., & Nicolis, S. C. (2014). 
Symmetry restoring bifurcation in collective decision-making. PLoS Computational 
Biology, 10(12), e1003960. 
E. Saund and D. Ari Friedman


---
*Extraction method: pymupdf*
