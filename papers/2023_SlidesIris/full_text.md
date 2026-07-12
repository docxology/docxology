# Full Text: Slides for Iris

> Extracted from `Slides for Iris April 17 2023.pdf`

> 8 figures extracted to `images/`

---

## Page 1

G
D
B
A
A
C
π
s2
s1
E
o2
o1
A = Emission matrix of States
B = Transition matrix of States
C = Preferences 
D = Prior on State estimates
E = Affordances
G = Expected Free Energy 
π = Policy
ot = Observations through time 
st = State estimates through time
Here is an Active Inference 
Generative Model, expressed 
as a Bayesian Graph

## Page 2

D
s
o
Let’s consider this model in terms of what GPT does right now –
Prior: Training set 
and parameters
Latent state – 
Semantic state space 
that is “all at once” 
and not separated 
by speaker.  
Observation – this is 
strings of words.

![page2_img1.jpeg](images/page2_img1.jpeg)

## Page 3

D
B
s2
s1
o2
o1
First let’s add in temporal dynamics, using the “Perceptual Inference” 
part of the full Active Inference model (there is no Action Selection in 
this model, just Hidden States changing through time & emitting 
Observations at each time)
B is the transition matrix – describes how Hidden 
(semantic) Spaces evolve through time. This leads 
to the question of how time is treated, which we 
have discussed a few approaches for!
Here is the Figure 4.3 
from Parr et al. 2022 
Textbook – Top is 
Discrete time, Bottom is 
Continuous. We can do 
anything we want with 
embeddings, wavelets, 
Generalized Coordinates, 
etc.

![page3_img1.jpeg](images/page3_img1.jpeg)

![page3_img2.jpeg](images/page3_img2.jpeg)

![page3_img3.jpeg](images/page3_img3.jpeg)

## Page 4

Now that the model has a temporal aspect, we can see a possible way to address the second issue, that all 
speakers are admixed (and hence cannot have differential weighting or attention). Here is one possibility – 
using the renormalization group approach towards modeling collective behavior from Friston et al. 2023
Figure 2 
https://arxiv.org/abs/2303.04898
Friston, Friedman, et al. 2023
The multiple meme accounts (aliases, or subideas) one person operates
The group of people
The set of groups
The Biophysical Eco-Niche
Black line is Thickness of Attention
It is a portfolio (regime) of nested attentions at all levels.
Here, one person has 5 ideas, the left one (their right!) is the most attended to
That person is most regarded in their group, which is the most regarded group of groups.
Overall though, the biophysical/energetic reality of this whole mobile only has a single root (at least in this map).

![page4_img1.jpeg](images/page4_img1.jpeg)

![page4_img2.jpeg](images/page4_img2.jpeg)

## Page 5

To-Do 
●
Adding in examples of Visualizations and Dashboard (“you scan a 
context and some sort of model can give a summary with charts and visualizations”)
●
Specification of this model in GNN so that we can move it towards 
implementation.
●
Adding in Action component (e.g. “Given my current estimates of Hidden 
States, and Preference over Observations, what Actions can/should I take?”
●
…..
●
.
●
.
●

## Page 6

*[Page 6 appears to be blank or image-only]*

![page6_img1.jpeg](images/page6_img1.jpeg)

## Page 7

*[Page 7 appears to be blank or image-only]*

![page7_img1.jpeg](images/page7_img1.jpeg)

## Page 8

*[Page 8 appears to be blank or image-only]*


---
*Extraction method: pymupdf*
