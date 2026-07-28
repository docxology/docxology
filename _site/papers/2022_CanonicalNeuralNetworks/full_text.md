# Full Text: Canonical neural networks perform active inference

> Extracted from `ActInf Livestream.odt`

---

ActInf Livestream #051 ~ 'Canonical neural networks perform active inference'

A three-session series of discussions of the paper by T

https://www.nature.com/articles/s42003-021-02994-2

Presented by Active Inference Institute in 2022

Active Inference Institute information:

Website: https://activeinference.org/

Twitter: https://twitter.com/InferenceActive

Discord: https://discord.gg/8VNKNp4jtx

https://www.youtube.com/c/ActiveInference

https://coda.io/@active-inference-institute/livestreams

LS #051.0: Background and context. https://www.youtube.com/watch?v=ZASG-rtkXDk

LS #051.1: First participatory group discussion. https://www.youtube.com/watch?v=IM_NlUzyq8M

LS #051.2: Second participatory group discussion. https://www.youtube.com/watch?v=hY_CajLpt9Q

https://www.youtube.com/watch?v=ZASG-rtkXDk

Background and context.

Daniel Ari Friedman

Intro to the paper.

The paper’s abstract.

On the interface with neural networks.

Variations of the complete class theorem.

The previous paper.

A canonical neural network.

Canonical neural networks perform active inference.

00:29 Daniel Friedman:

All right, welcome. It is ActInf LDot 0and a fComura

It's October 26, 2022. Welcome to the active inference institute. We're a participatory online institute that is communicating, learning and plasticity applied active inference. You can find us at some of the links on the page. This is recorded in an archive livestream, so please provide us with feedback so we can improve our work.

All backgrounds and perspectives are welcome and will be following video etiquette for Solo Livestreams head to Active Inference.org to learn how to get involved with Active Inference Institute projects today. It's the first of several discussions that we'll have on the paper. Canonical neural networks perform active inference. 2022 by Tequia Isomura, Hijacki Shimazaki and Karl Friston The video is just an introduction to some of the ideas. It's not a review or final word.

01:43 There will be an overview of the structure of the paper and then we'll go through many of the set point. Also just to disclaim, there's many, many other and better resources to learn about neural networks. So I would very much welcome those with a technical understanding of neural networks and or some of the more applied computational or otherwise aspects of neural networks. It would be awesome to have them on for the dot one and the dot two, because it was not an area I was familiar with and so hope that I can hear more from the authors in our coming weeks and others. I'm Daniel, I'm a researcher in California, and this will just be a solo zero, which I guess hasn't happened in a while in the making of this.

Here are some of the generated art prompts area 51 Active Inference Brea. 51 neural network. Area 51 active inference. Ant Brea. 51 Active Inference Neural Network just some interesting images coming out of stable diffusion.

02:56 So as to some big questions that the paper is addressing and that one might be interested in to come to the paper. How can artificial neural networks be understood as generic optimization processes and what is the correspondence between hemodynamics and modern statistical inference methods? Other big questions are about the history and next steps of the enmeshment of natural intelligence, eg. Neuroscience and artificial intelligence, as well as, of course, whether to even play into this kind of distinction at all and have different integrated intelligence frameworks. And one paper where any of the authors or anyone who has kind of resonated with this work is recent by Zidore at all 2022 towards the Next Generation artificial Intelligence catalyzing the NeuroAI Revolution and so this is a bunch of authors.

And so it's interesting just to quote in terms of what some areas of discourse are saying right now, which is neuroscience has long been an important driver of progress in artificial intelligence AI. We propose that to accelerate progress in AI, we must invest in fundamental research in NeuroAI. So that's one way to lead some of the developments that are happening in the paper we'll discuss what does it mean to be particular but generic? That's a phrase used in the paper, so maybe that's kind of a jumping off point. And then how can active inference help us understand the past, present and future here of the interface with neural networks, statistics and neural AI?

We corroborated this proposition using numerical analyses of maze tasks. This theory offers a universal characterization of canonical neural networks in terms of Bayesian belief updating and provides insight into the neuronal mechanisms underlying planning and adaptive behavioral control.

05:53 Here is the roadmap I'll be driving. On the right side of the road, there's an introduction and a table with glossary of different expressions used. Then there's the Results sections, which has first an overview of equivalence between neural networks and variational base active inference formulated using a postdiction of past decisions. Canonical neural networks perform active inference and numerical simulations. So they work on the interface between neural networks and variational Bayesian methods and start with a more theoretical and mathematical background and then eventually present some maze simulations that are in MATLAB.

Then there's a discussion, and then the methods section is following the discussion and it has the subsections generative model variational free energy inference and learning, neural networks, simulations and data analysis. And I think that I have kept to the right color codes consistently from here on forward. The black quotes are the direct quotes from the paper Bleu quotes quotes are related to perception, orange for action, complete class theorems and neural networks together in purple. And then red is commentary and then the highlighting for red is related to the variational methods, but it's kind of redish.

07:29 Okay, the papers canonical neural networks perform active inference by the authors listed previously. It's in communications biology from 2022. And the key aims of the paper are laid out well in the first paragraph. So that's in black and other colors. And here the red is just kind of settling point initial conversation with the paper and connecting a little bit more to some previous streams before we go more into the specifics of the paper.

The sentient behavior of biological organisms is characterized by optimization biological organisms recognize the state of their environment by optimizing internal representations of the external environmental dynamics generating sensory inputs. So that's the sensory recognition model. In addition, they optimize their behavior for adaptation to the environment thereby increasing their probability of survival and reproduction. So that is bringing the entire active and inactive control theory. Formal theories of action.

08:35 Action selections. Planning and planning as inference all of these actionoriented pragmatic term type ideas come into play when this actionorange aspect is brought in and it is. Must be. Should be. Etc oriented towards survival and persistence otherwise we don't see that kind of thing for long over appropriate definitions for thing and long.

Et cetera. And this few sentences that the paper begins with summarizes a common theme in actinF which is that there's basically two pathways towards proficiency in the niche. There's changing the mind, which is the perceptual and learning and then there's changing the world through action. And that kind of integration of

09:49 So they are working with a framework where the way that this perception action flow is tractable computationally either just for our current computers so that we can implement simulations and data fitting or whether more fundamentally like this is the computational context of action they're suggesting there's a way to think of it in terms of a cost function minimization and also note like minimization maximization. In a way they're interchangeable because there's just sometimes negative signs that can flip them. So it's the same energy and fitness landscape that is being navigated whether you're minimizing to the bottom of the bowl and thinking of action selection that way and inference or whether you're climbing to the top of the hill gradient descent. Gradient ascent they're both kind of two sides of the same .2 fundamental issues remain to be established. Namely so this is what the paper is saying they're filling the gap in literature the characterization of the dynamics of an arbitrary neural network as a generic optimization process and the correspondence between such neural dynamics and statistical inference found in applied mathematics and machine learning.

11:05 The present work addresses these issues by demonstrating that a class of canonical neural networks of rate coding models is functioning as and thus universally characterized in terms of variational bayesian inference under a particular but generic form of the generative model.

This is maybe the only slide that has resources from too far a field from paper. Well, almost a few more. It's just on neural networks. The search on a very common search tool resulted in five plus million results for what are neural networks? And the first one was three Bleu one brown in 2017 which is just a nice YouTube video as they very often make with these beautiful renditions, and it's a very great video.

And there's many, many others. A neural network is a network or circuit of biological neurons, and that is variously purely computational and or biological map territory stuff. And they can be thought of as nodes and edges, which are the firing rates and the connections between the biological neurons being modeled as weights between nodes. A positive weight reflects an excitatory connection, while negative values mean inhibitory connections. And here is data coming in and ending up activating different neurons in this final layer.

12:40 So this is kind of doing inference in a neural network, and then there's an action part. Okay, the paper says variational Bayesian inference offers a unified explanation for inference learning, prediction, decision making and the evolution of biological form, which can be considered over multiple timescales. So this returns to the earlier theme of like exteroception action and persistence within and among generations. And the citations that are provided here for this are Friston, Kilner Harrison 2006 and Friston 2010, both very classic acne FEP papers, just to show one figure from each here's from the first citation with a winged snowflake, where if the snowflake ends up being somewhere that's too warm, that's not able for it to maintain the structure, then it melts, melts into a dew, etc. And it must be acting as if in one way or another, it's staying above that phase boundary.

13:53 That's how it's statistically identified, it's how it's autogenetically identified, functionally identified. And then here is one of the kind of path setting figures in the first and 2010 paper with a tree of many different areas

The kind of inference variational basing methods use rests upon a generative model that expresses a hypothesis about the generation of sensory input. Perception and behavior can then be read as optimizing the evidence for a generative model inherent in sensory exchanges for the environment, and that's the integration of perception and action within a single imperative in terms of if only computation. And that is described more on this slide, which one can pause and read, but the rest of the quotes are from the paper.

15:20 One eformalism that I had no familiarity with before this paper and associated readings and conversations with Ali was the Complete Class Theorem. So it would be great for anyone who's familiar with Complete Class Theorem to help a little bit here, but here's some interesting things that I came across crucially from the paper as a corollary of the Complete Class Theorem citations 19 through 21. Any neural network minimizing a class function can be viewed as performing variational Bayesian inference under some prior beliefs. Here are the citations 19 through 21 from 1940 719 81 2013, and also found some interesting resources. So quoting from this less wrong post linked here, dutch book defines belief as willingness to bet and Money Pump defines preference as willingness to pay.

16:28 This is in terms of the foundational arguments for a Bayesian Epistemological worldview. Hope that's correct. Again, it would be good to hear from anyone who knows more here, but in terms of different ways that one can consider the Bayesian proposition, which perhaps these are even better to use than referencing any person's last name. Because the interesting thing will be the different lenses that these different framings on Bayesian probabilities are interpreted as. Just like what a Pvalue is interpreted as in the frequentist worldlessly, like a beta factor interpretation.

So Dutch book defines belief as willingness to bet and Money pump defines preferences willingness to pay. In doing so, both arguments put the justification of decision theory into hypothetical exploitation scenarios which are not quite the same as the actual decisions we face. If these were the best justifications for consequentialism we could muster, I would be somewhat dissatisfied, but would likely leave it alone. Fortunately, a better alternative exists. The complete Class theorem.

17:46 So here's an image from that post possible world states observation likelihood maps to the possible observations hashtag a matrix, then decisionmaking rule may be probabilistic action selection as inference a possible actions affordances. And here we commonly see the loop being closed from actions to world states like through the B matrix changing how the world changes through time. And here these are both going to be mapped to a loss function l a real valued score from taking an action A when the world turned out to be theta realized theta. So that's quite an interesting framing and there were some other useful posts online. And from this Zhang blog the argument boils down to if you agree with expected utility as your objective, then you have to be Bayesian.

18:50 In a nutshell, a strategy is inadmissible if there exists another state that is as good in all situations and strictly better in at least one. If you want your strategy to be admissible, it should be equivalent to a Bayes estimator Complete Class Theorems. Only Bayes strategies are admissible and admissible strategies are Bayes. So there's probably a lot of interpretations of this, but it seems kind of related to optimal control or Bayes

19:57 And then also there's some quite interesting logical structures which can be read here in terms of their premise, theorem and conclusion. In the areas of arguments for Bayesianism being representation theorem, argument for probabilism, the dutch book argument for probabilism and the Gradational accuracy argument for probabilism. So pretty interesting. Back to the paper they wrote we have previously introduced a reverse engineering approach that identifies a class of biologically plausible cost functions for neural networks. Citation 22 previous Paper of Isomura Karl Friston 2020 the paper was reverse engineering neural networks to characterize their cost functions, the abstracts shown here.

But this letter considers a class of biologically plausible cost functions for neural networks using generative models based on partially observable Markov decision processes. We show that neural activity and plasticity perform Bayesian inference and learning respectively by maximizing model evidence. So this is a precursor paper from 2020 that is cited and foundational for the 2022 paper. Here are some figures from that paper. They have comparisons among Markov decision process scheme and a neural network.

21:33 For example, a Markov decision process scheme expressed as a formy factor graph based on the formulation in Friston. So here is the Markov decision process as a formy factor graph and on the right side is the neural network with the hidden state sensory inputs and neural activity and some figures and concordances.

And they wrote in this context, the neural network can in principle be used as a dynamic causal model to estimate threshold, constants and implicit priors. This reverse engineering speaks to estimating the priors used by real neuronal systems under ideal Bayesian assumptions, sometimes referred to as metabasian inference. So they're laying out their research agenda and much of the work is going to reference this earlier paper and other work. And then there's also some new integrations and especially the maze simulation in this paper, and probably more so let's find out.

22:51 Referring to the earlier paper, this foundational work identified a class of cost functions for single layer field feed forward neural networks of state coding models with a sigmoid or logistic activation function. We subsequently demonstrated that mathematical equivalence between the class of cost functions for such neural networks and variational free energy under a particular form of the generative model, which is similar broadly to what the 22 paper dot. Two, this equivalent licenses variational Bayesian inference as a fundamental optimization process that underlies both the dynamics and function of such neural networks.

However, it remains to be established whether the active inference is an apt explanation for any given neural network that actively exchanges with its environment. In this paper, we address this inactive or control aspect to complete the formal equivalent of neural network optimization and the free energy principle. So this earlier work was not including action. And so this paper's key addition, as I understand it, hopefully, is that they bring action more formally into the model. And it would be interesting to know like what else is that change associated with?

24:17 Or what else happens or doesn't?

Here's table one glossary of expressions, so these will also be broadly addressed later on.

Maybe it's useful though just to read the first one a canonical neural network in this work, the canonical neural network is defined by differential equations of neural activity derived as reduction of realistic neuron models through some approximations which give a network of rate coding neurons with a sigmoid activation function. In particular, we consider networks comprising a middle layer that involves recurrent connections and the output layer that provides feedback responses to the environment. So some category of neural network architecture or anatomy, physiology, whatever with sensory, cognitive and actionlike features in an environment or a generative process. So the results section, they write an overview of equivalence between neural networks and variational base. First we summarize the formal correspondence between neural networks and variational base.

25:56 A biological agent is formulated here as an autonomous system comprising a network of rate coding neurons. Figure one A so here's a small figure one A. We'll see it larger based upon the assumptions which will be brought up later on in a different fuller form. The update rule for the ith component of phi, which is the internal states so the cognitive states and the output layer y. So middle layer x and output layer y, these can be seen as the cognitive and the actinF selective aspects which are the autonomous states in contrast to the particular state of the active inference entity which is the whole blanket, and the cognitive states so including the sensory state.

But the sensory states can't be directly controlled, however action can influence them. And so that's what closes the causal loop and that set of the particular states comprising the autonomous states the update rule for the ith component of phi is derived as the gradient descent on the cost function. So the change in that by sub I is proportional to a derivative on the loss function. This determines the dynamics of neural networks including their activity and plasticity. So.

27:24 L common loss function O observations sensory states by internal state comprising the middle and output layer neural activity that's the rate coding part and synaptic strength w the parameterization and other free parameters including that that characterize L. Then there's the output layer activity y is determining the network's actions or decisions delta o x and y y is outputting action environment generative process hidden state passing observations to the sensory cognitive active layers the neural network and that is analogous topologically to the variational Bayesian formulation in figure one B. And so left side gradient descent on a neural network cost function L determines the dynamics of neural activity and plasticity. Thus L is sufficient to characterize the neural network and then being shown next to on the right side variational free energy minimization allows an agent to self organize, to encode the hidden states of the external milieu and to make decisions minimizing future risk. Here, variational free energy F is sufficient to characterize active inference and behaviors of the agent.

28:47 So sentence structure parallelism, and these two schemes or approaches being Linsker and applied is a focus of this area.

So neural networks are minimizing the cost function L. In contrast, variational Bayesian inference depicts a process of updating the prior distribution of external states P of theta, so the corresponding posterior distribution Q of theta based upon the sequence of observations. And we see other familiar terms from discussions on variational DAGs like minimization of surprise. And there's some more model details shown here. A few points

29:54 For example, choosing a linear regression with an L two norm. At the very least, you can say that it has a simple decision rule for being fit. I'm sure there's like also counter arguments and other algorithms that are better and so on. But just to say that a simple decision rule in a known family of distributions can often be good enough as an approximation, if not more crucially. According to the Complete Class theorem from earlier, a dynamical system that minimizes its cost function can be viewed as performing Bayesian inference under some generative model and prior beliefs.

The Complete Class theorem goes on to describe it ensures the presence of a generative model that formally corresponds to the above defined neural network characterized by L. Hence, this speaks to the equivalence between the class of neural network cost functions and variational free energy under such a generative model equation one loss function on the time series of observations comma parameters. Three ines is defined as f the free energy function on the same O through time comma parameters. So there's a parallel being shown defined wherein the internal states of a network by encode or parameterize the posterior expectation theta. This mathematical equivalence means that an arbitrary neural network in the class under consideration is implicitly performing active inference through variational free energy minimization and more is written.

31:41 But this is one of many statements that will be made corresponding to correspondences between neural network loss function, generative model, active free energy minimization, and associated formalisms.

Note that being able to characterize the neural network in terms of maximizing model evidence lends it in explainability in the sense that internal neural network states and parameters encode Bayesian beliefs or expectations about the causes of observations. In other words, the generative model explains how outcomes were generated. However, the Complete Class theorem does not specify the form of a generative model for any given neural network. To address this issue in the remainder of the paper, we formulate active inference using a particular form of partially observable Markov decision processes PMDP models whose states take binary values. So this is one of several simplifications is one way to see it or areas for later generalization.

32:52 Figure Two in this section, we define a generative model and ensuing variational free energy that corresponds to a class of canonical neural networks that will be considered in the subsequent section. The internal model is expressed as a discrete state space in the form of a POMDP figure two. So to make figure two larger, there's a lot to probably say about this bigger. I'll just note that the caption is informative and some of the highlighted lines. It'll be awesome to have the author and other people who's familiar with some of the differences and symmetries between the, for example, bottom and top, above and below the observations, and also about the role of time and what these two risks are.

33:56 What is fictive causality?

Here's more details on that POMDP then equation two. This is in this section active inference formulated using a postdiction of past decisions. So if it was a prediction of future decisions, it's the opposite, a postdiction of past decisions. Hence, we define the generative model as follows PO delta s gamma theta, which is the model of observations decisions, observations decisions, hidden states risk and theta theta equals A, b and C constitutes a

34:56 And equation two reflects the factorizability and the dimensions and the kind of computational tractability expression. So that would be interesting to also learn about like under what conditions can this joint distribution be factorized? Under what simplifications or constructions the agent is making decisions to minimize a risk function capital gamma that's on the bottom of figure two, victim causality. Leading to this gamma. Coming from that gamma, equation three is shown.

And to characterize the optimal decisions as minimizing expected risk in our POMDP model, we use effective mapping from the current risk gamma to past decisions that's that retro addictive fictive causality. Although this is not the true causality in the real generative process that generates sensory data. Here we intend to model the manner that an agent subjectively evaluates its previous decisions after experiencing their consequences. This fictive causality is expressed in the form of a canonical distribution. So it could be other families hypothetically.

36:21 But this equation three is describing fictive causality and this interesting sign indicates the element noise division operator. Also note throughout the manuscript the overline variable indicates one minus that variable. So gamma bar equals one minus gamma. Or it can be understood as the complement of a statistical probability probability of a happening and the probability of not a happening in that one way.

Importantly, the agent needs to keep selecting good decisions while avoiding bad decisions. To this end, equation three supposes that the agent learns from the failure of decisions by assuming that the bad decisions were sampled from the opposite of the optimal policy. Mapping some more details and then by convention, active inference uses C to denote the prior preference. That's how we've seen the C variable in many models as preferences. Prior Preference this work uses C to denote a mapping to determine a decision depending on the previous state.

37:37 Herein the prior preference is implicit in the risk function due to construction. C does not explicitly appear in the inference. Thus it is omitted in the following formulations. So that's a key point about the notation of the variable C and something kind of maybe interesting to explore. Equation Four variational Bayesian inference refers to the process that optimizes the posterior belief q of theta based on the mean field approximation q of theta is expressed as and here is the factorization representation of the q of theta variational and another notation.

Note throughout the manuscript, bold case variables such as bold s subtow denote the posterior expectations of the corresponding italic case random variables and some more details about the model. For example, for simplicity, here we suppose that state and decision prior D and E are fixed, so one could imagine they don't have to be, but for simplicity they will be. Here, under the abovedefined generative model and posterior beliefs, the ensuing variational free energy is analytically expressed as follows equation Five this is a variational free energy F and recall equation one that it is being connected to, juxtapose with, etc. The loss function the gradient descent on variational free energy updates the posterior beliefs about hidden states s decisions, delta and parameters theta. The optimal posterior beliefs that minimize variational free energy are obtained as the fixed point of the implicit gradient descent, which ensures that change in F with respect to the change in hidden state through time equals zero.

In what follows, we demonstrate that the internal states of canonical neural networks encode posterior beliefs. Here's figure three on the top from the caption figure three is the mathematical equivalence between variational free energy and neural network cost functions depicted by one to one correspondence of their components. Top variational free energy transformed from equation five using the Bayes theorem and foreshadowing. Equation seven. Using this relationship, equation seven is transformed into the form presented at the bottom of the figure.

41:20 So here's f variational free energy and L the neural network cost function and different elements as they're represented here with some resonances and concordance and beyond which we can explore, they're being shown to be equivalent. And it was in the conversation preparing for this dot zero with Dean, where we saw this as some chromosomes.

In this section, canonical Neural Networks Perform Active Inference in this section we identify the neuronal substrates that correspond to components of the active inference scheme defined above. We consider a class of two layered neural networks with reafferent connections in the middle layer. Figure one a those are those connections with loops recurrent in the middle layer. The modeling of the networks in this section, referred to as canonical neural networks, is based on the following three assumptions that reflect physiological knowledge. One gradient descent on a cost function l, determines the updates of neural activity and synaptic weights.

42:34 Method Section neural Networks Neural Two assumption two neural activity is updated by the weighted sum of inputs and its fixed point is expressed in a form of a sigmoid or logistic function. And assumption three, a modulatory factor mediate synaptic plasticity in a post hoc manner.

They write based upon assumption two, which is neural activity is updated by the weighted sum of inputs and its fixed point is expressed in the form of a sigmoid or logistic function. Based on assumption two, we formulate neural activity in the middle layer and output layer the autonomous states as follows equation six without loss of generality, equation six can be cast as the gradient descent on cost function l. Such a cost function can be identified by simply integrating the righthand side of equation six with respect to x and y, consistent with previous treatments. Citations because neural activity and synaptic plasticity minimize the same cost function l, the derivatives of l must generate the modulated synaptic plasticity under these constraints, reflecting assumptions one through three, a class of cost functions is identified as follows equation seven loss function. Awesome to hear somebody read this directly.

44:10 So there's a firing rate aspect that's related to neural firing in the short term more perceptual aspect of function. And there's a slower neurotransmitter neuroglial factormediated learning over perhaps a different time scale and with some different features, and they're being included as a joint model of inference. And here that is being connected to doing inference on action. Synaptic Plasticity in Neural Networks so synaptic plasticity rules conjugate to the above rate coding model can now be expressed as a gradient descent on the same cost function l,

45:13 Cost Functions and Variational Free Energy Based on the above considerations, we now establish the formal correspondence between the neural network cost function and variational free energy. Using under the aforementioned three minimal assumptions, we identified the neural network cost function as equation seven. Equation seven can be transformed. Hinton the form shown in figure three bottom using sigmoid functions of synaptic strengths. So equation seven loss function transformed into the form shown in figure three bottom.

Hence, this class of cost functions for canonical neural networks is formally homologous to variational free energy under the particular form of the POMDP generative model defined in the previous section. We obtain this result based on analytic derivations without reference to the complete class theorem, thereby confirming the proposition of equation one loss function and free energy. This in turn suggests that any canonical neural network in this class is implicitly performing active inference. Table two summarizes the correspondence between the quantities of the neural network and their homologues in variational Bayes. So two, a great concordance table.

46:51 On the left side, neural network formation. On the right side, variational Bayes formulation. So just like in figure three, we had the two long lines. Then table two, we have rotated 90 degrees and the variables for different parts of these models are laid next to each other.

So what papers of neural networks can we make active models for? Is it already done or is there just one script that needs to be done? And then conversely, what interesting, variational Bayesian models have interesting applications or some other value or information gain from being cast as neural networks or integrating neural networks into what had previously been only analytical variational Bayesian models as well as the empirical data fitting aspect which is related that's highlighted by the authors. So, in summary, when a neural network minimizes the cost function with respect to its activity and plasticity the network selforganizes to furnish responses that minimize the risk implicit in the cost function, this biological optimization is identical to variational free energy minimization under a particular form of the POMDP model. Hence, this equivalence indicates that minimizing the expected risk through variational free energy minimization is an inherent property of canonical neural networks featuring delayed modulation of hebion plasticity.

48:49 Okay, brief seconds to view some image memes and take a breath in a stretch.

On the left side, the top panel says Epineural network is implicitly performing active inference. That's awesome. In the middle image meme, one simply makes a neural network and it is implicitly performing active inference. Also question mark. And then in the right image meme, there are two pieces of paper neural network and implicit performance of active inference.

Corporate needs you to find the differences between this picture and this picture. And here is the paper. They're the same picture. So the previous sections have successfully extended the variational Bayes meets inference. Neural network results from the 2020 paper with an action loop and a loss function only on the autonomous states.

Figure four a thus it implicitly performs active inference by minimizing variational free energy. So now some entity or agent is going to be constructed and numerically simulated to support some of the aspects of their model and point towards utility in other settings. So here's figure four simulation of neural networks solving maze tasks. In part A, there is the architecture of the agent sensory input layer O of T synaptic weights into the middle layer x internal states and the output layer y decision action with risk gamma of T.

51:57 The sensation comes in a neural network then outputs a decision. There's some task that the entity must perform which is to move towards the goal from the start across this lateral maze. So one could imagine that if it were just a hallway with no maze features, simple strategies would be very overfit but effective like always move simply towards the goal. Whereas in more complex settings, which this is an example of where there's uncertainty as well as many local optima. So one has to sometimes take one or two or three or four or more steps or however many to get closer to the goal and sometimes may not know, for example how long those backtracking situations are going to be and all these other complexities for which this maze example is symbolic of.

53:18 So maybe there's some interesting mythos maze connections and computational and here's some performance measures on the maze task with the neural network entity. This way, before training, the agent moved to a random direction, each step resulting in a failure to reach the goal position right end within the time limit. During training, the neural network updated synaptic strengths depending on its neural activity and ensuing outcomes I e. Risk. This training comprised a cycle of action and learning phases.

This treatment renders neural activity and adaptive behaviors of the agent highly explainable and manipulatable in terms of the appropriate prior beliefs implicit in firing thresholds for a given task or environment. In other words, these results suggest that firing thresholds are the neuronal substrates that encode state and decision priors as predicted. Mathematically big if true.

54:24 Furthermore, when the updating of parameters is slow across these two now linked domains parameters of the variational Bayesian autonomous state inference and the neural network loss function parameters when the updating of these parameters are slow in relation to the experimental observations, the parameters can be estimated through Bayesian inference based on empirically observed neuronal response curve method. Section data Analysis for details using this approach, we estimated implicit prior E, which is encoded by PSI from sequences of neural activity generated from the synthetic neural networks used in the simulations reported in figure four. We confirmed that this estimator was a good approximation to the true e. So that's also pretty interesting. This is showing they don't just lay out this architecture and show that it's possible to fulfill this maze task with the best whatever.

55:37 It's not a classification accuracy imperative alone. They're describing that from empirically observed neuronal responses, which is to say the experimenters observation the sequences of neural activity generated

So that's pretty interesting and will be great to hear what each of the axes are and what all the variables mean.

With this setup in place, they did some numerical validation and talked a little bit more about fitting data from this simulation model.

56:51 Here's the discussion section. So the first paragraph of the discussion biological organisms formulate plans to minimize future risks. In this work, we captured this characteristic in biologically plausible terms under minimal assumptions. We Deneve simple differential equations that can be plausibly interpreted in terms of a neural network architecture that entails degrees of freedom with respect to certain free parameters, e. G firing threshold.

These three parameters play the role of prior beliefs in variational Bayesian formulation. Thus, the accuracies of inferences and decisions depend upon prior beliefs implicit in neural networks. And here's some more stable diffusion ant neural network ant gain neural network so some more summarization of what they did based on the view of the brain as an agent that performs Bayesian inference. Internal representation of Bayesian belief updating have been proposed which enables neural networks to store and recall spiking sequences eight learn temporal dynamics and causal hierarchy nine. Extract hidden causes ten, solve maze tasks eleven, and make plans to control robots twelve.

58:11 So citations eight through twelve listed here. In these approaches, the update rules are generally derived from Bayesian cost functions e. G variational free energy. However, the precise relationship between these update rules and the neural activity and plasticity of canonical neural networks has yet to be fully established.

We identified a onetoone correspondence between neural network architecture and a specific POMDP implicit in that network. Equation two speaks to a unique POMDP model consistent with the neural network architecture defined in equation six, where their correspondences are summarized in table two and the figures. This means that our scheme can be used to identify the form of the POMDP given an observable circuit structure. Moreover, the free parameters zhat parameterize equation six can be estimated using equation 24. This means that the generative model and ensuring variational free energy can in principle be reconstructed from empirical data.

59:24 This offers a formal characterization of implicit Bayesian models entailed by neural circuits, thereby enabling a prediction of subsequent learning. So what can be done with this? What is this new? What is new here? Does this second selection fully establish the precise relationship between these update rules and the neural activity and plasticity of canonical neural networks.

Here is a discussion section on hebion plasticity, neurotransmitters and glia with a lot of citations listed. And here is just one interesting followon discussion from the computational aspects. Neurocognitive and computational aspects of heavy and plasticity is these modulations have been observed empirically with various neuromodulators and neurotransmitters such as Dopamine, Noradrenaline, Lescreen, and GABA, as well as glial factors. So here's a picture by Alexandra Michaelova Cultured astrocytes release, signaling and growth factors that regulate proper neuronal development so Cool, Glial, Pick, Dopamine and reinforcement learning. In

1:01:07 Those citations are listed here. This speaks to a learning scheme that is conceptually distinct from standard reinforcement learning algorithms, such as the temporal difference learning with actorcritic model based on state action value objective function. Please see the previous work citation 50 for a detailed comparison between active inference and reinforcement learning that is state ball par Karl Friston active inference demystified and compared from 2021 and that's also active model stream number two. One, we mathematically demonstrated that such plasticity enhances the association between the pre post mapping and the future value of the modulatory factor, where the latter is cast as a risk function. This means that postsynaptic neurons selforganized to react in a manner that minimizes future risk.

So the neural network had three layers. It's the second and the third layer, not the initial sensory layer, but the second and the third layer, the cognitive and the active states, which are the autonomous states of the particular state. So that's quite interesting the self organization of synaptic neurons to react in a manner that minimizes future risk. Crucially, this computation corresponds formally to variational Bayesian inference under a particular form of Pom DP generative model, suggesting that the delayed modulation of Hebbian plasticity is a realization of active inference and regionally specific projections of neuromodulators may allow each brain region to optimize activity to minimize risk and leverage a hierarchical generative model implicit in cortical and subcortical hierarchies. This is reminiscent of theories of neuromodulator and meta learning developed previously.

1:03:16 Citation 52 Doya 2002 metal learning and neuromodulator cool. Our work may be potentially useful when casting these theories in terms of generative model and variational free energy minimization.

They then return the discussion to the complete class theorem and neural networks. So the Complete Class Theorem same citations from before ensures that any neural network whose activity and plasticity minimize the same cost function can be cast as performing Bayesian inference. However, identifying the implicit generative model that underwrites any canonical neural network is a more delicate problem, because the theorem does not specify a form of the generative model for a given canonical neural network. Which is pretty interesting. Is that to say that the form of the generative model as modeled is different in what ways?

1:04:22 From the given canonical neural network, the posterior beliefs are largely shaped by prior beliefs, making it challenging to identify the generative model by simply observing systemic dynamics. To this end, it is necessary to commit to a particular form of the generative model and elucidate how posterior beliefs are encoded or parameterized by the neural network states. This work addresses these issues by establishing a reverse engineering approach to identify a generative model implicit in a canonical neural network, thereby establishing onetoone correspondences between their components. Remarkably, a network of rate coding models with sigmoid activation function formally corresponds to a class of POMDP models, which provide an analytically trackable example of the present equivalents. Please refer to the previous paper citation 22 for further discussion.

So some of the analytical details, especially on the inferential side cognitive side burr captured in the earlier paper. This paper goes further into mapping the potentially necessary and sufficient aspects of the particular entity, which is to say the risk minimizing features of the autonomous states with respect to the entire particular states, including sensory states. Connecting that back of the envelope verbally expressible formulation to some

1:06:33 It is remarkable that the proposed equivalence can be leveraged to identify a generative model zhat an arbitrary neural network implicitly employs this contrast with naive neural network models that address only the dynamics of neural activity and plasticity. If the generative model differs from the true generative process that generates the sensory input, inferences and decisions are biased, ie. Suboptimal relative to base optimal inferences and decisions based upon the right sort of beliefs. Prior beliefs in general, the implicit priors may or may not be equal to the true priors. Thus, a generic neural network is typically suboptimal.

Nevertheless, these implicit priors can be optimized by updating free parameters e. G threshold factors, phi PSI based on the gradient descent on cost function l. By updating the free parameters, the network will eventually in principle become Bayes optimal for any given task. In essence, when the cost function is minimized with respect to neural activity, synaptic strengths, and any other constants that characterize the cost function, the cost function becomes equivalent to variational free energy with the optimal prior beliefs.

1:08:00 So the cost function for the neural network activity and synaptic strengths underlying the loss function are equivalent to the kind of gradient descent enabled variational free energy minimization under the Bayes optimality scenario from a risk perspective. Simultaneously, the expected risk is minimized because variational free energy is minimized only when the precision of the risk gamma is maximized. C method section generative model for further details. Very interesting.

They then say the class of neural networks we consider can be viewed as a class of reservoir networks. Citation 54 citation 55 here, the proposed equivalents could render such reservoir networks explainable and may provide the optimal plasticity rules for these networks to minimize future risk by using the formal analogy to variational free energy minimization under the particular form of PMDP models. A clear interpretation of reservoir networks remains an important open issue in computational neuroscience and machine learning.

1:09:38 So from Wikipedia reciprocal computing is a framework for computation derived from recurrent neural network theory that maps input signals into higher dimensional computational spaces through the dynamics of a fixed nonlinear system called a reservoir. After the input signal is fed into the reservoir, which is treated as a black box, a simple readout mechanism is trained to read the state of the reservoir and map it to the desired output. Then there's two key benefits of this approach. The first key benefit of this framework is that training is performed only at the readout stage as the reservoir dynamics are fixed. The second is that the computational power of naturally available systems, both classical and quantum mechanical, can be used to reduce the effective computational cost.

Here some stable diffusion reservoir computing, active inference neural network so this would be interesting to discuss. And I remember some Octave institute participants who are specifically interested empirical analysis and hypotheses. They write the equivalent between neural network dynamics and gradient flows on variational free energy is empirically testable using electrophysiological recordings or functional imaging of brain activity. So then another summarization crucially the proposed equivalence guarantees that an arbitrary neural network that minimizes its cost function, possibly implemented in biological organisms or neuromorphic hardware, can be cast as performing variational Bayesian inference. So to state it a few more times in the final paragraph, in

1:11:45 Formal correspondences exist between priors posteriors and cost functions. This means that canonical neural networks that optimize their cost functions implicitly perform active inference. This approach enables identification of the implicit generative model and reconstruction of variational free energy that neural networks employ. This means that in principle, neural activity, behavior and learning through plasticity can be predicted under Bayes optimality assumptions.

There's a code availability statement. The MATLAB scripts are available at GitHub in the repo of the first author, and it would be awesome for the author or anyone to bring this working MATLAB script up and see if we could do some realtime active inference. Then, as mentioned earlier, from the roadmap the methods are following the discussion. I'll just show the equations but not go into any details because there is not time nor familiarity. So those who have more of one or the other would be welcome to fill in some dots because this is a really awesome and important paper.

1:13:18 So I hope that it can be interpreted and critiqued and elaborated on and so on by those with familiarity in both sides of that free energy loss function.

Equation one generative model section, many details are provided. Equation ten is shown. So larger unpacking of the generative model section variational free energy many details are provided, equation 1112, 1314 and 15 section inference and learning details are provided. Equations 16 1718 then section on neural networks so there's just some interesting writing here. So I wanted to highlight that in this section we elaborate the one to one correspondences between components of the canonical neural networks and variational Bayes via an analytically tractable model.

1:14:26 So that's the figure three that we've been returning to. Neurons respond quickly to a continuous stimulus stream with a time scale faster than typical changes in sensory input. For instance, a peak of spiking neurons in the visual cortex of V one appears within 50 and 80 milliseconds after a visual stimulation citation 62 63, which is substantially faster than the temporal autocorrelation timescale of natural image sequences about 500 milliseconds. Citation 64 65. So that's pretty interesting.

What is the temporal autocorrelation timescale of natural sequences?

What timescale do neural firing and neuroplasticity etc processes actually occur at? And when might some type of function at a given time scale be understood to be functional or not?

1:15:41 Thus, in other words, downstream of the fact that neurons respond quickly at a time scale faster than typical changes in sensory input, we consider the case where the neural activity converges to a fixed point given a sensory stimulus. We note that the present equivalence is derived from the differential equations equation six, but not from its fixed point. Thus, the equivalence holds true irrespective of the time constant of neurons to rephrase neural networks with a large time constant formally correspond to Bayesian belief updating with a large time constant, which implies an insufficient coverage of the posterior beliefs. Pretty interesting related to learning rates and Bayesian updating rates and all of the nooks and crannies of Bayesian inference and the

1:17:05 In the variational Bayesian and in the neural cases, they have to deal with time. And so all of those different nooks and crannies mentioned, like catastrophic learning, catastrophic forgetting, simply memory, anticipation, attention, local maxima, choosing when to play all these higher order questions are connected here does that maze it? What kind of a problem space now or just what kind of space? Pretty interesting. And equation 19 202-021-2223 they have some more details on the simulation.

Maybe we could see the simulation go and in the last section data analysis. So this is kind of returning to that point about the time constants in Bayesian and neural network systems when the belief updating of implicit priors D and E is slow in relation to experimental observations, d and E, which are encoded by phi and PSI, can be viewed as being fixed over a short period of time as an analogy to homeostatic plasticity over longer time scales. 66 homeostatic Plasticity in the developing nervous System 2004 very interesting in light of our recent discussions on allostasis and other topics. Thus by and PSI can be statistically estimated by a conventional Bayesian inference or maximum likelihood estimation given a flat prior based on empirically observed neuronal responses. In this case, the estimators of phi and PSI are obtained as follows Nice equation number 24 mentioned earlier, so that will be definitely one to look into more.

1:19:27 Well, I hope you found this a useful and interesting zero. I'm looking forward to the discussion with the author and again, any other institute participants or those with knowledge or strong feelings to express about neural networks, active inference, applied, active inference, computational modeling of perception, cognition and action, neural networks in the wild, AI ethics, all these different areas can hopefully have a nice discussion in 51.1 and .2. That'll be the last paper streams for 2022. And yeah, if you want to be more involved with live streams whenever you're listening to this, join or recommend someone to join or help in any number of other ways. Just listening and learning is awesome.

1:20:55 And we also really look forward to those who want to help make some of these connections that are latent and sometimes exposed in these papers and conversations, and with a few motivated people who want to connect, for example, to the neural network communities and those who can facilitate discussions on these topics, that would be awesome. Just using my final thoughts on this dot zero, because it's always great to have others also join in the preparation for the dot zero. So just want to add that note on this rare solo stream. So thanks again, looking forward to talking or seeing you later. Bye.

https://www.youtube.com/watch?v=IM_NlUzyq8M

First participatory discussion on the2022 paper "Canonical neural networks perform active inference" by Takuya Isomura, Hideaki Shimazaki & Karl J. Friston.

Daniel Ari Friedman, Takuya Isomura

00:39

Intro and welcome.

01:25

Canonical neural networks perform active inference.

02:58

Welcome to the discussion.

03:46

The universal characterization of neural networks.

05:55

The mathematical equivalence between neural networks and active inference models.

09:58

The complete class theorem.

18:32

Decision rules in neural networks.

31:21

Do we need to know all possible states?

40:45

Forward and reverse engineering.

1:05:47

Interpreting unobserved neural states.

1:11:36

What is a program?

1:14:40

Impinging on the s self-arc.

1:30:24

Wvk, k, and gamma.

1:35:18

Gamma and action selection.

1:41:47

Critical time window for dopamine actions.

1:50:26

Matt's interest in neural networks.

1:56:53

Anything else you want to add?

00:39 DANIEL FRIEDMAN:

https://www.youtube.com/watch?v=hY_CajLpt9Q

Second participatory discussion on the2022 paper "Canonical neural networks perform active inference" by Takuya Isomura, Hideaki Shimazaki & Karl J. Friston.

Daniel Ari Friedman, Takuya Isomura

00:33

Intro to the active inference institute.

01:16

“Canonical neural networks perform active inference” from 2022.

03:23

The fundamental parallel.

05:58

The informational free energy expression.

16:14

Activity dynamics and plasticity.

38:17

The code availability statement.

43:13

The checker board represents decision.

1:00:00

Neural networks to POMDP

1:07:58

Mass block matrix.

1:09:49

Sparse matrix design.

1:31:00

Introduction to experimental systems.

1:33:50

Other interesting sections.

1:47:19

Final thoughts and questions.

00:33 DANIEL FRIEDMAN:

c


---
*Extraction method: odt_xml*