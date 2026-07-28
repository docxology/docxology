# Full Text: Interoception as modeling, allostasis as control

> Extracted from `ActInf Livestream.odt`

---

ActInf Livestream #050 ~ “Interoception as modeling, allostasis as control”

Discussions2

https://www.sciencedirect.com/science/article/abs/pii/S0301051121002350

Presented by Active Inference Institute in 2022

https://www.youtube.com/watch?v=l7r0ISlr-Hc

This video provides background and context for some of the ideas in the paper.

Daniel Friedman, Dean Tickles

00:28

Intelligence Exteroception as modeling allostasis.

02:21

Allostasis and exteroception in decision-making.

05:44

On Claims and the appraisal process.

07:44

Brain regulation of the viscera.

08:53

This is a roadmap for Intelligent Brain.

12:11

Inferring the brain's body.

14:07

Interceptive Inference in the Brain.

19:15

Systems, Errors and Allostasis.

20:31

Active Inference for Allostasis.

23:46

Relationships in physiology and neuroscience.

28:41

Regulation of blood pressure through generative models.

37:58

Bayesian Systems of Foraging and Regulation.

40:32

Control Theory for Physiology, Motor Control and Decision Making.

43:00

Referential Control of Action and Perception.

47:57

Functional block diagram for motor control.

52:25

The APIC model of All.

53:15

Transforming Capacity Curve into Objective Functions.

59:47

Generative control with stochastic optimal control.

1:02:00

Feedback Control with generative action.

1:04:28

Bellman Equation, Analysis and Discussion.

1:08:40

An Active Inference Model for the Brain.

1:09:26

APIC model of the body and the brain.

1:13:04

Bayesian mechanics and the path-integration problem.

1:15:01

Epic Decision Making.

00:28 Daniel:

All right, welcome to ActInf Livestream, number 500. It is October 17, 2022 and we are starting the series on intel exteroception as modeling allostasis as control. Welcome to the active inference institute. We're a participatory online institute that is communicating, learning and practicing applied active inference. This is recorded in an archive Livestream, so please provide us with feedback so we can improve our work.

All backgrounds and perspectives are welcome and we'll be following good video etiquette for live streams today. In 50.0, we're starting this series discussing the paper interception as modeling Allostasis as control. The authors are Eli Sanesh, Jordan Thuryalt, data Brooks, john Wilhelm von de Mint, Lisa Feldman Barrett and Karen S. Wiggley. It is a paper published in the journal Biological Psychology in January of 2022.

And this is just an introduction and context video as Dean here and I worked through this paper and discuss some related topics.

01:39 We're going to go over some big questions, basic aims and abstract roadmap of the paper, then go into the paper, touch on a few key points and images and themes, and then primarily look forward to discussing it with any authors or anyone else who would like to join in the coming weeks. Alright, so I'm Daniel, I'm a researcher in California and the paper was selected by decentralized upvote. It was fun to read and it brings some new topics into our regime of attention. So I'm looking forward to this.

And I'll pass to Dean.

02:20 Dean:

Excellent. I'm Dean, I'm here in Calgary. I think what's interesting about any paper that pulls two seemingly discrete things and puts them proximal and gets them entangling and then pulls them apart again and tries to look at sort of what happens when things get combined is always something that I'm always interested in that in fact it was the title of this. And the fact that they were bringing allostasis and exteroception together and what does that mean?

Was the reason why I agent a little bit of time on this and really am quite interested in hearing what the authors have to say now that they put this idea to work.

03:04 Daniel:

Right. How would you describe the big question?

03:09 Dean:

Well, I think the focus here is on what happens and what we can say about control requirements necessary to carry out biological tasks, varying degrees of complexity.

I've never been really sure how the specificity of different outcomes and behavior looks in aggregate. But I think one of the things that we can say is if there's a predictive component and there's a feedback component, and they're focusing on two particular types of that, it's interesting perhaps, what kind of generalities we can walk away with, sort of not getting lost in the weeds of, well, this happened here, and then that happened there. But just on that general level, what sorts of things, when those two things are put together, should we say, has a certain pattern or commonality nice?

04:06 Daniel:

I agree. I would put it in the category of asking how a given system independent or modality independent phenomena like allostasis, which is anticipatory changes in physiology, concepts with a domain or a use case like interception.

And it does seem like a lot of the models that we've explored have been visual or concept or symbolic, and the interceptive modality has popped up again and again in discussions. And so this is a cool opportunity to look at some formalisms for interception. Okay, here's the paper as described earlier, just a few of the highlights that were written by the authors on the publication page. Interception enables the brain to anticipate the body's, encoding metabolic needs. exteroception provides performance metrics for visceral motor regulation.

05:10 We connect control theory with decision making and motor control of the body. We model allostasis control as optimal control with the time varying reference signal. They talk about some limitations of previous models and some unique aspects of what their model does and the way that they formulate the APIC model. Anything to add?

05:40 Dean:

Nothing straight forward.

05:43 Daniel:

Okay. On claims. So Dean and I Beren looking Hinton thinking of ourselves in terms of claims adjusters, appraisers examiners and investigators as we pulled out a whole handful of really important and salient within the arguments of this relatively long and technically. Scaffolded paper and pulling out a bunch of claims that are written that connect the dots and set some of the relevant interpretations for the formalisms. Do you want to highlight any of them or it's fine to just have them for anyone who wants to.

06:35 Dean:

Yeah, I'm not going to read off of this, but I will say this. There is, I think, a parallel trying to be drawn here between predictive processing. I'm not saying that predictive processing, but processing as a predictive device and feelings and control and feedback. And so I think there are a lot of claims that can be made, but that's a really nuanced and also a very complex space to play in. And so I can

Again, whether or not or how far those claims can hold before they Brea down will be an interesting thing to talk to with the authors.

07:31 Daniel:

Yeah, well, Sajid it's a very intertwined area. Maybe that's what you're pointing towards when you say complexity brain.

07:40 Dean:

Yeah, I've got a lot of hair, so it's tricky for me.

07:44 Daniel:

All right, abstract.

Okay, I'll read the first three. The brain regulates the body by anticipating its needs and attention to meet them before they arise, a process called allostasis. Allostasis requires a model of the changing sensory conditions within the body, a process called interception. In this paper, we examine how interception may provide performance feedback for allostasis. We suggest studying allostasis in terms of control theory, reviewing control theory's applications to related issues in biology, motor control, and decision making.

08:24 Dean:

We synthesize these by relating them to the important properties of allostasis regulation as a control problem. We then sketch a novelism for how the brain might perform allostasis control of the viscera by analogy to skeletal motor control, including a mathematical view on Hohwy. Interception acts as a performance feedback for allostasis. Finally, we suggest ways to test implications of our hypothesis.

08:53 Daniel:

Okay, onto the roadmap.

The paper starts with introduction the function of the brain in the body and then introduces some of the key pillars or function of their synthesis and interpretation, which is interception control theory as an approach for unifying physiology, motor control, decision making, and allostasis as a trajectory tracking stochastic optimal control. The fifth section is a discussion, and then there's an appendix B and C. And in their words, four sections in this paper connect interception to allostasis. Section two establishes how interception enables the brain to estimate the physiological efficiency of the body in the present moment, which is precisely what it needs to know to evaluate and refine action. Section three introduces control theory.

Action four applies the principles of control theory to derive a novel format model of how the brain might estimate the desirability of physiological trajectories and make prospective regulatory decisions.

10:04 Finally, section five synthesizes the previous three sections to explore the direct implications of the proposed formalism. Appendix A provides a glossary of terms, but this is moved up and it's no longer an appendix, so there's no appendix A. Appendix B one provides mathematical details related to section three. And appendix C one provides mathematical details related to section four.

11:06 So here's the first nomenclature, terms one through 25.

And then here's the second half of the nomenclature, 26 to 49 sorted alphabetically.

Anything to and on the nomenclature other than to say that it's good that they provided it and it will be used in the coming sections.

11:35 Dean:

Well, I think it's interesting that you pointed out that they pull the definitions forward and then they look at the formalisms. And so I think from the standpoint of what they ant to message around this braiding requires us to at least get a common sense around what things mean before we start trying to pull Parr what they equal. So. Yeah, I like that.

12:09 Daniel:

Well Sajid. Alright, section one, introduction the functions of the brain in the body. Okay, there's an evocative beginning to this paper. Playing a simple game of dodgeball then requires your brain to continually coordinate the systems of your body. And this motif of dodgeball is going to be returning again.

And on the left is a hugging face implementation of a stable diffusion algorithm. The prompt of the image was dodgeball, playful ants, active inference, free energy principle. And while we were making the slides, we were engaged active inference lab with some of these image generating affordances and allowing that to do what?

13:06 Dean:

I think it's really interesting that this what the generator said this would be the result of a coordinated what's the word I'm looking for? Entanglement of these prompts.

But it doesn't talk anything about what strategy each one of those silhouettes is now employing. And I think that there is an implied sense that there's a strategy going on as well. So, again, when you bring some of these really interesting things together, I guess it depends on how deep you want to go, how much you ant to dimension the space. So what is that right there?

13:49 Daniel:

Yeah, this is the same prompt.

This was just another one. This one's a little more photo realistic, a little bit more like elusive. Are they playing dodgeball?

14:01 Dean:

Yeah. Are they just inferred?

All right, next keyword. You can go for it. People can read the definition here, but just give your own take. What is exteroception?

14:16 Dean:

Well, I think at the end of the day, there's a certain amount of signaling going on that we become aware of.

Sometimes young people or old people might sort of categorize them all under the umbrella of feelings. And I grabbed this from tops on target just because I always worked in that kind of space of how do we keep this as simple as we can? And so when you get these signals, these sensory signals originate from within the body. These are the feelings you get. And whether or not you connect them to the world outside of your skin or your margins, sometimes you do, sometimes you don't.

You just wake up with a tummy ache. Right. So what does that mean about today?

15:09 Daniel:

Nice. I would say a little narrowly interception is referring to some observation and inference on hidden states with a coherence that's in tarot inside of the body as opposed to extro outside the body.

But there's probably also a lot of, like, blurring. And what is the retina really doing? Is it doing inference on itself? And where is it actually doing inference on the outside world structure? All right, interceptive internal models.

You added some images. So what are they?

15:45 Dean:

Yeah, so I'll just read this real quick. Psychologist referred to the turn on, including exteroception by many terms. I think that's important because there hasn't always been agreement about clearly defining what an internal model is.

Things like unconscious inference seems to fit under this umbrella. Embodied simulation, concepts and categories. Controller hallucination, which was new to me because I don't know what that even means. And regardless of what it's called, the brain's hypothesis, to construct a dynamic model of its body in the world, in this paper, we use the terms prediction, simulation, and concept. And so for somebody with sort of my deep research background in terms of abduction, the signal, the interpreted, the object, what is that model?

How do we avoid getting into another great debate about whether that's representational axel constant filled or not?

16:47 Or is there something that we sense from the inside every single time data is coming at us and being poured onto our different sensory surfaces from the outside, I think that there's a piece that comes from the outside. I know when the temperature goes up in the room, but my temperature might also be going up because they ate a bad shrimp. And it's sometimes difficult to figure out whether or not it's because the heat gone up or whether my body is responding with an inflammatory gesture.

17:28 Daniel:

Yeah, that's a nice point.

17:54 Dean:

Knows. I can't tell whether the image on the left via the image on the left, what speed the image on the right is actually moving down the road. And that's kind of why I wanted the ambiguity there for an interceptive model, because the MaCio talks a lot about what can we really describe in precise terms and what remains somewhat ambiguous. And the authors in this paper talk a little bit about that as well.

18:25 Daniel:

Yeah, when active coherence is external, it's objective, then there's the opportunity for multiple external perspectives to align.

Not even saying that's better, but just the opportunity to whereas if the embodied behavior of your physiological set point for some physiological regulation is changed, it doesn't have the same opportunity for external alignment. Again, for better and for worse, and almost always with difficulty communicating or sometimes measuring in laboratory settings as well and quote, controlling. So speaking with authors on this and why they study this modality will be interesting. Alright. As for the computational or system independent phenomena that they're going to be trying to integrate with, errors is allostasis.

19:28 They define this term as allostasis to anticipate changing needs, evaluate priorities and prepare the organism to satisfy them before they lead to errors. A process called allostasis. So let's just say that you have an allostatic model of the temperature in the room and the core body temperature doesn't change. So then can one look back and say it didn't change because it was expected to change and somebody will just say, well, how do you know it worked then? Because it didn't raise the body temperature.

20:03 Dean:

I focused on the part, the fact that they describe it as a three part process. So me being always talking about what's the minimum here? What's the minimum here we need in order to be able to do this. I found that really quite interesting, why three, not four or five or breaking it out into smaller slices. That's again, another one of those questions.

I'd like to be able to talk to the office.

20:31 Daniel:

All right. Active inference, they wrote, before diving into formal modeling details below, which we're going to get to later in the paper, it might be helpful to compare and contrast the approach here APIC with the prominent modeling framework, active inference, and we're going to return to some of these details, and I'm sure have a lot of discussion on it. But you made a really interesting point in our preparation about how they're not treating their model as downstream or a corollary of any commitment to a particular physics, which is how we often hear about free energy principle basic mechanics, but rather they're treating the model as a first order construction. Anything you want to add on that?

21:29 Dean:

Yeah, that's straightforward. I think that the fourth bullet. Unlike most active models in the culture material below considers an indefinite time or infinite horizon control. Setting is interesting because that makes it really clear between what they're talking about and what we often see in a lot of the representations, which is t zero, T one to T, whatever in terms of being able to figure out what is going on sequentially.

22:02 Daniel:

Right. Cool. This section in the introduction talks about some issues with other models. They talk about how existing models of interception have either formulated allostasis as a prospective decisionmaking problem without considering how these decisions are enacted, which has a bunch of different interpretations, but maybe, for example, requiring the enumeration of policies and then the selection from policies or as a motor control problem without considering where motor commands come from. Another issue they have with other models, rather than treat metabolic efficiency as the objective, they discuss homeostatic the regulation of bodily variables to fix set points with fixed tolerance for error.

So this is really going to be a cool theme, which is rather than fix the set point and variability, see that outcome as being due to some other process that does result in an attracting set or a point with a fixed set point and an empirical tolerance for error as well as maybe some points of no return and so on.

23:16 But seeing all those outcomes as the realization of a dynamics system that actually doesn't pursue a set point but rather pursues a slope on a graph that will explore and that like zone of maximum controllability and reduction of surprising around the zone of maximum controllability over evolutionary time will come to be associated with this kind of a survival variable and some other points. Okay, anything else?

23:48 Dean:

Well, it's relationship, relationship, relationship. And then they say this paper aims to fill this gap.

I think relationship doesn't necessarily imply that things have to get closed in terms of whatever the gap is by filling something in. I think the fact that they talk about targeting I think the fact that they see relationship as playing kind of the key role in what they think is happening here means that maybe the gap continuum I mean, they're putting stuff in here for us to consider and contemplate, but I'm not sure if we're actually filling a gap or if we're just sort of understanding what's in this space.

24:36 Daniel:

Right. Section two. So at the beginning of section two, the top paragraphs interception modeling the body, estimating its efficiency. And then the below the fold, section two five, the summary. So both of these pre and post 2022 contains a lot of structural information about the key points in this paper.

Anything to add on this specific slide to or will just go into the section.

25:15 Dean:

Just a quick start down ant the very bottom there. People might want to have a read on that because I

25:27 Daniel:

That the movement towards the responsive range of a capacity curve could be potentially obviating the need for a dedicated neural circuit or module that specifically calculates the behavioral constructs of reward and cost. So what does it mean to move into non reward centric understanding of physiology or reinterpreting reward?

Okay. Section 2.1 introduces a distinction that is gain to be key in the rest of the paper, which is the difference between two types of visceral sensory variables intercepted those which represent quantities of resources, regulated resources, and those which represents rates at which processes act. Controlled process processes. Regulated resources are kept stable, relatively stable over time. Examples include blood glucose and core body temperature.

So of note is they don't have to be a depleted resource.

26:28 The regulated resource is kind of like the bounded variable in a physiology in a homeostasis context. It's not necessarily a depleted like, metabolite regulated resource like blood glucose or core body temperature represents a physical quantity or substance like glucose. Its quantity cannot change instantaneously. So I think it will be interesting to ask like, what different regulated resources of different modalities are and then the controller processes are the rates at which physiological processes operate.

So in that case would be like the kind of input output relationships of blood glucose.

27:10 Dean:

Okay, yeah, we just talk about that. We talk about that recently is what's the difference between gripper and gripped and can both exist at once?

27:20 Daniel:

Nice. Two two.

Back to the dodgeball examples. The heart rate and the blood pressure must increase during aerobic exercise, as noted in the Dodgeball example. So there has to be some biological adaptation in order to start exercising and continue exercising upon resting conditions. The barrow receptor, that's pressure receptor heart rate reflex would normally counter any rise in blood pressure by slowing the heartbeat. However, with exertion, your blood pressure and heart rate both must increase to support the needed increase in blood flow required by your exercising muscles.

And so then there's a discussion of how this kind of modulation of reflex allows for shifting of an entire function relating a change in blood pressure to a change in your heart rate. So this is describing like a dynamics systems approach and biological model for how the causal or correlational structure of different physiological variables can be modeled pretty generally, but it's going to get more specific.

28:35 Dean:

Yeah, a little bit of conversation there. And physiology and where we go.

28:41 Daniel:

This is describing some of the parameters of the curve, the thresholds and saturation points which partly define curves that are derived from functions which physiologists commonly use to model the connection between perturbations and regulatory responses, usually naming them response curves or transfer functions. And then the term capacity cue will be used to emphasize the fact that while such curves can shift over time in any one instant, they represent the current range of limited regulatory resources available to an organism. So one could imagine like a financial capacity curve to maintain some market at some point, like kind of like the depth but by analogy and then this idea of modeling how a system responds to perturbations doesn't necessarily require modeling the internal model of that system.

29:49 But as you build a better generative model of the system being perturbed then the better experiments and the further you can have kind of perturbability of the system. It allows you to approach a system without a strong hypothesis about its structure.

The capacity curve in figure one has a mathematical form and then figure one is shown alongside. With equation one the parameters are defined. The function y is taking in u mu k, big R, big B and combining those into an equation. The figure one on the x axis is showing the blood pressure and then the y axis is showing the baseline activation percentage of the reflex modulating this physiological variable. So at 100, which is the target blood pressure, or sort of what would be called the homeostatic set point because it seems to be an attractor at that point the baseline activation of the barrel reflex is happening.

30:59 When the blood pressure increases, then the barrel reflex activates up to two x thresholding at two x activation of baseline and then as the blood pressure decreases, the barrel reflex again with this sigmoid symmetry decreases.

That's a dynamics model of regulation of blood pressure.

Equations two, three and four outline the form of a generative model, a procedure for probabilistically predicting observed variables in terms of unobserved variables. The variables listed are unobserved variables which are sampled from an Anil probability distinctions not dependent on data. So that's referring to using a generative models and how these equations constituted. The proposal here has an unusual feature. The equations for x, the mean arterial blood pressure and y the barrow reflux activation as the percentage of baseline.

32:02 So figure one, x and Y are in terms of the quantile variable U. The quantile variable uniformly represents the relationship between the blood pressure and the barrel reflex activation, irrespective of changes in the capacity curve's, operating point, mu and gain k. The quantile depends only on the functional form of the capacity curve and not on the parameters. So we'll unpack that a little more technically, but they point to that as a feature of their model.

Here again is figure one, a little bigger with more space to discuss later. And here's figure two, which is the capacity curve from figure one in Bleu with a linearized response in orange around the operating point, the Bleu diamond marker. So one can see this as the maximum positive slope of this sigmoid curve. And that under the specification that the reflex is going to be activated in a sigmoidal way.

33:06 Then depending on whether one is in like a curving up part or a curving down part, or thinks about it as pursuing the maximum positive slope, then pursuing that point and being rewarded by movements towards maximum maneuverability and control would have the equivalent of pursuing a

So it puts the kind of bottom of the bowl in this forage line being maximized in slope, rather than the Bleu diamond being reduced in its distance from 100.

Right.

I think we COVID this section twice. It was so unusual, we copied it twice.

Two, three return to the Dodgeball example and they're going to widen their scope beyond just the barrow reflex blood pressure to circulating levels of oxygen, glucose and carbon dioxide.

34:18 Next, we focus on blood glucose as a regulated resource, with glucagon as the controller process encoding secretion of glucose into the blood, and insulin as the controller process enabling removal of glucose from the blood. So the barrel reflex was like a single volume knob or a triage nurse that can lower or raise the single response. So if some physiological variable is high, it's like it can be removed. Glucose regulation has multiple hormones.

It's going to be like buffers from two different sides in a slightly different way, but using a lot of the same formalisms and logic to introduce a slightly different and more complex physiological system. Okay, the section discusses some findings that blood blood glucose levels are not actively defended at a biologically hard coded set point, and more than heart rate is instead glucagon and insulin. Two hormones activity balance each other's affect to bring the blood glucose to a point within its settling Lagrange, with glucose entering the blood after the person ingests food and glucose then crossing from the blood into other bodily tissues to support their function.

35:35 Anything to add on this slide?

35:38 Dean:

Not specifically.

I'll wait till we get to the end of section two stuff.

35:44 Daniel:

So here is figure three they're writing. Figure three shows plots of the resulting functions of this equation applied to the insulin case, which can be interpreted as capacity. Cue orange sigmoid is insulin. Bleu sigmoid is glucagon.

They have different hormone levels at different x axis, which is the level of glucose in the blood. So you kind of see familiar behavior. When glucose is high, then insulin is at high secretion, which drives the absorption of glucose. And when glucose gets low, in this case below two, five or three or so, then glucagon is secreted to elicit glucose to enter the blood. Okay?

And so one can imagine that the glucose level will be oscillating in this space, but not exactly set point with a residual being minimized.

36:59 Section 2.4 is where they move from discussing this kind of a regulatory model into viable ranges and capacities could obviate a modular reward system. Here's an agreement or appeal to neuroanatomy. There's no single brain site that specifically encodes, appetitive or aversive reinforcement value. It is useful to reframe discrete reward and decision systems as domain general allostatic control systems. The domain generality of interception provides further theoretical support for the idea that we do not need mental modules or faculty psychology concepts to understand how brain works.

37:56 Dean:

No. Let's get to 37.

37:58 Daniel:

All right. The rewards of control. So here I wanted to highlight two papers with some nice images by both papers involving Tobias Moreville. And these papers are cited in the paper under discussion and they all show some pretty interesting features. So just to highlight some of these graphs here's, movements within a glucose and temperature space.

So, regulation of multiple physiological variables. Here on the bottom left is the integration of interception, homeostatic set point and motor commands like related to foraging. Here is some Bayesian visualizations with a prior posterior unlikelihood and about this two way relationship of inference and a form of a dynamics model. The tail of two densities. And then last one, this is another body temperature glucose modeling approach that gets to that notion that we describe as going to the bottom of the bowl where the shape of this napkin could be designed or evolved or selected so that the marble spends most of its time in a certain zone.

39:23 And this is like just one other way to think about these types of attractor systems rather than as like traces or so on. Okay. Anything to add?

39:34 Dean:

I think section two basically confirms that if you're going to be doing any kind of predictive performance that has an element of continuity to it, that depends on sort of recognizable finite limits and also variability within whatever those limits are. And I think that kind of speaks to the idea that there's sort of a twofactor situation, there's signaling that looks like this and they sort of pointed.

Out a couple of examples of the barrel reflex and the glucagon thing, and they also are trying to avoid oversimplifying or over reducing like they tried to keep the complexity of those two examples retained in terms of what they were trying to hold up as something that allows us to start looking at these capacity curves.

40:32 Daniel:

All right. Section three control theory. The unifying lens for physiology, motor control and decisionmaking. And then one of their summaries of the chapter. This section introduces concepts from engineering control theory, then reviews its applications in the life sciences.

These include physiology section three one, skeletal motor movement. Section three two. And decision making section three three. Section three four will concept future inter active states to present movements, illuminating what makes allostasis regulation more energy efficient than homeostatic regulation. The next section four will build off the account of control used in physiology to suggest how exteroception supports allostasis.

Okay, here we're not going to read everything on the slide, but this is from section 3.1, control Theory

41:32 Dean:

No. People just want to read this?

41:35 Daniel:

Yep. I'll just call out. For a controller to perform well, it must contain some sort of copy or mirror of the plant's expected behavior, which is referred to as an internal model. Control theorists call the driven system the plant and its desired trajectory, the reference trajectory. And there's some interesting discussion of this kind of threat of control theory.

Figure four. So figure four is a functional block diagram of modelbased controller system. The plant in orange is the object or system whose motion or other behavior is controlled. The controller purple sends signals, controls, solid black arrows. The change how the plant moves and signals the expected outcome predictions solid yellow arrow to the state, estimator in yellow, and so on.

People can read the rest of it for these figures.

42:28 Dean:

Daniel, as we get further down in the slides, why don't I read and then you can run the cursor over the different parts of the model so people can kind of see in real time how the two things line.

42:40 Daniel:

Sounds good. We'll do that for the future ones. And this is going to revoke or recall some of our earlier discussions in Live Stream 23 skillful performance and interactionism and instructionism and how to think about motor plants and so on.

43:00 Dean:

Right.

43:02 Daniel:

Section three two, moving the body, the reference control hypothesis. So the reference control hypothesis, the citations provided were to Feldman 2015 and Latash 2021. And the referent control hypothesis describes the skeletal motor system in terms of a hierarchy of controllers with higher level controllers in the brain prescribing coherence trajectories to the lower level reflexes in the spinal COVID. These reflexes then compare the actual length of the muscle as signal by exafferent proprioceptor neurons to the reference length sent down by the brain and contracts the muscle to bring the two into agreement.

And so here is the top part of the table of content of Feldman's 2015 book Coherence Control of Action and Perception and the paper of Latash in Physics of Life Review 2021. With some graphics around this type of approach, you can start this slide on the real world.

44:09 Dean:

Okay, well, I'll just point out a couple of things the authors say because they do not want to be accused

For example, in the game of dock volume, if you unexpectedly step on a hard, sharp block or object, you just don't purposely impale yourself who chaos stepped on it. So I just wanted to go through my foot now because my focus is still on stabilizing my posture.

45:11 Rather you recoil in pain. You feel that interceptively and the unplanned disturbance of any tissue damage requires you to make a decision about what to do next. Excuse yourself to nurse your foot or play through the gain.

I think the fact that they're trying to limit what they are saying is the extent to which the goal piece of this can be said to apply is a good thing because I think there's a couple of areas around. So in this relationship between a command system or a control system and a demand system, where do things like when your body is starting to suffer from mild hypothermia and people know that your brain stops functioning correctly, how do you differentiate between, for example, I'm getting a slurpee headache and you put the slurpee down and stop drinking it.

46:14 Because you know that that's the effect versus you have your limbs which aren't phosphate at this point, or at least hopefully not phosphate and continue to move so that you don't stop. You avoid stopping moving altogether, which essentially is death. So here we've got to wonder whether or not without getting into the argument of because it's pretty obvious if your brain is dead, you're dead.

But if your hands are dead and you are still alive, that clear distinction between a command center consequence and a demand center consequence. What does that mean in terms of, okay, so there's things that happen that you do automatically in order to keep yourself alive in some of the most critical situations. And it's not like your hand has a brain and yet it may in just simply moving around beyond a reflexive thing be able to keep you alive long enough until somebody comes to your rescue as a for example.

47:21 So I don't know if that's confusing or not, but I think that there's a reconciliation that goes on between command and demand. And maybe some of control is the ability to give up command at times in order for a new response to take over and keep you alive.

And you may not necessarily know how to do that from a command center. So we'll have to talk to the authors about that because these are questions that I have because I got a bit of a physiological background. So I wonder about these extreme situations.

47:57 Daniel:

All right. Section free Markov decision constructing future reference trajectories they use the word demands, so we'll talk about it later.

More quotes from 33 for those who want to screenshot talking about Arrogant City, which is also raised in the appendix B, which we're not going to focus on. Okay, you can read figure five and I'll use the mouse.

Go for it. So a functional block diagram for an experiment experimental psychologist task oriented view of motor control. The diagram shows a formal logic structure here at a conceptual level.

The boxes and errors do not map onto the anatomy of the brain or nervous system. In contrast to Figure four, this diagram differentiate between skeletal motor brain and peripheral stretch reflex controllers, between sensory state estimators, brain and peripheral sense organs. Sensory surfaces. Sensory surfaces. The diagram shows an engineering perspective important to note that on a psychology experiment in which the experiment prescribes a task for behavior to participants.

So there's an externality and a participant's brain then access control system to achieve the prescribed behavior. Systems that maintain the body therefore serve systems that move the body, which in turn serve a prescribed behavior.

49:30 So again, focus on the prescriptive the external states. Information coming in.

All right, functional black diagram. Yep. Next one. Function block diagram for a control theory view of all of thesis in control. To figure five.

This diagram shows a closedloop control system designed for autonomous regulation of the body and experimenters desired task behavior is replaced with or by sorry, the allostatic capacity estimator, which sends predictions of capacity cue, which we've already looked at, to the interceptive state estimator and receives prediction errors with which to update its estimates. The updated estimates are issued as a reference signal to the visceral motor controller. This diagram shows a formal logical structure, a conceptual load. The hypothesis depicted is constrained by the inferred anatomical structures in Vera 2017.

50:34 But the boxes and arrows do not map, I'll repeat, do not map one to one onto the anatomy of the brain and nervous system.

50:43 Daniel:

All right, great. So just to highlight the difference here, the left is almost like an instructionalist agreement and this is how the experimental psychologist thinks about this task, which is like we write down the instructions, the pseudo code for the task. Keep your heart rate within this range. And then there's some decision making with the skeletal motor system, whether capable of conscious action and stretching or more subconscious, and then ActInf through physiology in the body or in the external world, that interceptive state estimator comes into alignment with the desired implementation of the skeleton motor decision. In contrast, the role of the task instructions, so to speak, is substituted in this control theoretic view with the allostasis capacity estimator as the imperative.

51:52 And that feeds on through a very similar set on the right side. But here we actually have the Viserra motor decision control errors contrast to a skeleton motor decision controller, because this is more focused on like, choose the left button or the right button. And figure six is focused more on the kind of barrow reflex control theory view, but that also generalizes beyond.

Okay, I think that's just another view. Section Four allostasis as trajectory tracking stochastic optimal control.

This section will describe our formal model of allostasis decisionmaking, the Allostasis path integral Control APIC model. APIC has a simple idea at its core. Just as perceptual concepts serve as internal models of the body's sensory surfaces, action concepts also serve as internal models of potential

52:56 Section four one derives an SoC objective function from the mathematical form by which section two represented capacity cue. Then section 4.24.3 and 4.4 are described, flushing out this APIC model.

Anything to add? No.

53:14 Dean:

Let's go there.

53:15 Daniel:

All right. 4.1.

Transforming capacity curve into objective functions. Since any given capacity curve, such as the one in figure one above, which is a maximum value on the vertical axis, it can be divided by its maximum y value to normalize it to range between zero and one. Once normalized in this way, it can be interpreted as a cumulative distribution function from probability theory. This is precisely, in fact, precisely what Shen, Loughlin and Dubs did to interpret the firing of retinal neurons and flies as a form of predictive coding. See there figure one, the derivative of a CDF cumulative distribution function field a probability density function PDF.

So the derivative of a CDF gives a PDF. This is the more familiar way of representing a probability distribution where the height on the vertical axis corresponds to likelihood in the PDF.

54:18 But for a PDF derived from a capacity curve, it represents relative responsiveness to perturbation. We will call such distribution a reference distribution. So this is a transformation of statistical distributions between the PDF, which is the probability density function, and CDF cumulative distribution function.

It might be very familiar to some, it might be totally new to some, so it's all good. Hopefully this is useful still to consider the relationship between the two. So here on the left of these three images, the PDF, which is the Jorge familiar way of representing a probability distribution, we would say this is a uniform distribution. There's a one in six chance of getting each outcome from a six sided die or in the Gaussian Bull cue situation which both of these two middle and right images show. The PDF of the bell curve is the bell curve.

So the PDF is the most familiar one. The uniform distribution is like a flat line in the PDF.

55:21 The bell curve is like a bell curve in the PDF. But since you know the maximum and minimum values if only asymptotically then you can make a cumulative distribution function which starts basically as low as the function can go the support for that distinctions and it just accumulates cumulatively. So it's like useful to answer the question what is the probability of getting four or three or two or one that is two thirds or what is the probability of getting a zscore of below two like two standard deviations positive?

What fraction of the curve is below that zscore on the PDF? And that is addressable by quickly just looking up a point on this CDF. It turns out that that relationship between the PDF and the CDF which is more familiar to again like rolling a die or evaluating like height in the classroom can be used on the capacity curve discussed earlier to move to a distribution which when maximized is in this spot of maximum control.

56:38 So here the CDF from figure two gets the derivative and then it becomes the PDF with this sort

Figure eight shows the objective function log density corresponding to the original barrel reflex capacity curve.

57:43 Figure nine further clarifies the relationship between the various force of capacity curve by showing all three alongside each other. So this is really nice figure on the top left of the figure is the figure one with a reflex that gets dialed up or dialed down to regulate blood pressure that's when interpreted as a CDF can result in a PDF and that is a single peak that you can maximize. Instead of trying to calculate a residual. The shape of this curve becomes slightly nicer to optimize computational when you make it so that it's like a smoother bowl rather than this kind of like inverted funnel shape.

It just we can go into more detail why I think that'll be cool. Why does this log step matter or doesn't matter but suffice to say that this is the big move that lets you turn the sigmoid juggling act into the mountain climb.

58:50 Table one summarizes some key.

Table one summarizes some key notations. We do not claim our graphical model accurately captures the anatomy of the brain. It captures reference based sensory motor control across a hierarchy of timescales. A single feature shared with the brain. Variables in the table, equations five and six, about the instantaneous capture rate.

We'll discuss it in the one two, section 4.2 also will be nice to discuss. It is optimal foraging theory suggests a functional form force allostasis control. Do you want to add anything upfront about optimal foraging?

59:37 Dean:

No, other than I want to talk with the authors about what does that even mean?

59:46 Daniel:

That'll be great. All right. Equation eight, Global capture eight, section four three feedback feedforward control with generative action concepts. So here's some more formalisms, and this is within not the experimental psychologist framework, but rather the control theory framework with allostatic capacity estimator on the left. Section four, three, equation ten.

Equation eleven, more variables stochastic optimal control SoC, which was mentioned earlier. Equation twelve, figure ten. This one will be nice to discuss. A hierarchical generative model capturing multiple timescales and coherence distinctions at each level without addressing empirical questions about neural hierarchies. Here we employ a model with L equal four models to match figure six.

1:00:50 It defines what some of these nodes mean. But the yaxis is increasing time scale, so perhaps slower things higher up. And then on the right is the passage of time. So what does this make you think about or what is like a way we can approach the interpretation of this?

1:01:11 Dean:

Well, I'm not trying to be a smart apple, but I do find it interesting that all four gives you quite a bit of information.

They talk about the fact that there's more than four levels, but they want to focus on those work. Where my brain goes is, okay, so we got the water, we got the yeast, we got the hops and we got the grains. And that can create quite the product. So you can go past that, you can add juice or whatever, but you got the four basic ingredients. So now moving through time, what does that enable so gain?

It would be nice for them to pull that apart because I think even in this there's enough there to figure a lot of stuff out, right?

1:02:00 Daniel:

4.4. Feedback control with generative action concepts. Still there is equation 13, equation 14, and then a nice quote. Readers familiar with predictive processing and active inference will recognize the form of the above equation 14 as a negative free energy or a variational lower bound.

For discussion, see some citations. Since objectives can typically be written out and interpreted in several equivalent ways, each of which can come with its own intuitions, there are arguments for the computational and thermodynamic efficiency of minimizing this specific divergence in the course of neural processing. But to date, the available evidence does not rule out other more complex information divergences for penalizing feedback correction of movements. So it's pretty interesting how different lower bounds variational, lower bounds negative free energies exist. Like there's expected free energy and then there's free energy of the expected future and there's all of these variants and then each of those energies can be decomposed differently, like equation two six in the textbook.

1:03:17 So it's interesting to see how, first off, how did they converge to this kind of a bound and from why should it have such resonance with free energy principle and what does that mean? And then how can different partitionings of these energy boundary help us think about systems that survive?

1:03:45 Dean:

I'll just add here, Daniel, that we're going to get to these things. But up Hinton this point in the paper, I guess I had a bit of familiarity and I didn't really struggle with the sort of the lockstep where they were going through this. But as soon as we got to equations 13 and the jump to equation 15 and 16, somebody brighter than me is going to have to be able to explain that jump in real simple terms, because even though I've read it a number of times, I'm still not exactly sure how it works.

So again, the authors will really want to bring their softest gloves because I need my handheld.

1:04:24 Daniel:

Yeah, agreed.

Section 4.4, still here's, equation 15.

Section 4.4 here's equation 16 substituting the augmented objective fancy j, equation 14, and the analytical expression for the optimal feedback controller alone, equation 15 into the Bellman equation. Equation twelve would yield equation 16. Let's learn what it is.

Yeah.

1:05:04 Daniel:

Now the intractable recursive term in the equation is etc.

Finding a way to replace this term will field a more computationally tractable problem. The information divergence term in fancy j provides just such a way since it can be written as precisely the difference between the intractable hard maximum under star sub phi and the more tractable smooth maximum under the preplanned action concept in symbols, equation 17. Pretty interesting.

Equation 17 through 21.

Then the final section, section five, discussion.

1:05:52 Dean:

Maybe you can help me today. So we're 13 through 17 and then 1819 and 20, a way of being able to put together some of the scale free formalisms with the scale specific or scale friendly details. In particulars. When you read this, is that what you saw them trying to clarify?

1:06:25 Daniel:

That's a great question because they talk.

1:06:29 Dean:

About Global and I think they have to be able to spell that out. And I think it did. But again, it was all of a sudden things went off into the ditch. Force me.

1:06:41 Daniel:

Here's what I would venture.

In the early section, there's a contrasting of homeostasis with allostasis and about how reward systems are no longer required under certain distributed models of brain neuroanatomy and a function. So I believe that the following formalisms substitute the augmented objective into an optimality and optimization framework like the Bellman equation, which is often used for reward maximization. So I'm rewarded by getting to the top of the mountain. So I'm going to evaluate paths based upon how much reward they accrue, and then curiosity or so on will be valuable to the extent over the time horizon that I considered. It facilitates reward in terms of elevation, whereas we here are seeing the move towards that, like optimal maneuverability maximization with a PDF CDF relationship.

1:07:54 Like instead of trying to reduce emergence to the midpoint of the CDF, you maximize your responsiveness in terms of maximizing the log PDF. So I think that's the augmented reward function which is tractable and then some work remains to specify that function and how it behaves. Perhaps.

1:08:23 Dean:

Okay.

1:08:27 Daniel:

People can look at the quotes. Anything to summarize here?

1:08:39 Dean:

No?

1:08:40 Daniel:

All right. Five one viewing the brain as an allostasis optimal controller.

The allostasis path integral control APIC model in section four implies a number of specific hypotheses beyond those generic to stochastic optimum control. There's some discussion of shared modeling choices with active inference models, perhaps enough for APIC to be considered an active inference model of sorts. And then a few other features that are shared with active inference models in a straight sense, if one even exists, and also related modeling efforts. Anything to add?

1:09:22 Dean:

No.

Probably spell that out pretty clearly here. You just want to read through this.

1:09:26 Daniel:

Alright. 5.1. Provide some predictions and some contrasts with the APIC model.

Five two the body and the brain through the lens of control theory. Figure six show how visceral sense data ascend in effect to become exafferent interceptive prediction errors.

1:09:53 Dean:

Do you want to explain briefly what and exafferent means? Because people might they do explain that in the glossary, but it's basically an apprentice signal on an appraisal signal. There's a bit of recursion there. Do you want to add anything to that?

1:10:10 Daniel:

I see the distinction just to highlight what afferent is.

Afferent is conducting or conducted inwards or towards something for the nerves, the central nervous system, for blood vessels, the Ozan supplied. And how would you distinguish ExAC after?

1:10:31 Dean:

It's just that it's that sort of cumulative. It's not sort of the initial is what I took away from that the accumulation of those affordance signals.

1:10:50 Daniel:

Interesting.

1:10:51 Dean:

I might be wrong. That's what I took away.

1:10:54 Daniel:

Five free interception and capacity cue theories of peripheral predictive coding reason that a neurons most metabolically cheap responses should represent the predictable stimuli, whereas expensive responses are reserved for the most surprising stimuli. Some predictions and suggestions from Barrett 2017 and findings of Dwarken 2013.

Certain peripheral interceptors in humans reduce their exafferent firing rate to zero under a constant stimulus. So that's kind of interesting. Like if no change, don't tell me about it. And that should be cheap under a model where something is changing less often than not.

And there's some more hypotheses. We have hypothesized that increases in such responsiveness, which is the generative in this APIC model, could function as rewards, positively reinforcing behavior trajectories, while decreases in responsiveness could function as costs negatively reinforcing behavior trajectories.

1:12:00 So keeping options open over the infinite time horizon becomes equivalent to keeping the business floating or keeping physiology bounded.

1:12:14 Dean:

Continuity.

1:12:15 Daniel:

Instead of just maximizing amount of USD or calories, but rather having reduced or bounded surprising about a range and a trajectory and a strategy. Not in this model as stated here to generate that 5.3 interception and capacity cue. More 5.4 conclusions finally, we return to the amateur dodgeball player, the ant mature yeah, and some summarizations of the APIC model and suggestions about its compatibility with active inference control hypothesis and some of its tractability.

That's the discussion then Appendix B ergodicity, which we've talked about before, but it's kind of a cool topic. So just to skip through these appendices, just discussing them with the authors, we hope then some more equations in equation B formulating perception and control errors gototically leads to the free energy principle FEP more of Appendix D.

1:13:29 Appendix C APIC model derivation details equations C one two full derivation of optimal value function and transition dynamics. More equations the path integral form for the value desirability function gives its name to the technique of path integral control and so on. A kind of closing note, we wondered how this connects to the Bayesian mechanics and to the path formulation, the rightmost of the three phases of Bayesian mechanics and about how coming potentially from quite a different starting point and with different approaches and constraints.

Some similar features might have arisen and been highlighted in APIC that are also highlighted and relevant for basing mechanics in the path communication.

1:14:34 And maybe there's like a kind of unmapped Venn diagram there and some similarities and differences.

1:14:44 Dean:

Proximity to the last Livestream, whether by accident or by intent makes the way that you look at this

1:14:57 Daniel:

I'll just say yeah, agreed. Well, anything you want to close with?

1:15:06 Dean:

I think the idea of being able to look at modeling and brain modeling and sort of the correlation of that either, again, kind of as a minimum two other as a risk management or risk minimizing exercise. Therefore, a limiting strategy or as an option generating or an expanding strategy would be something really interesting to talk to the authors about. Because gain I can't really figure out whether or not the epic model works in both domains until I get past the jump between formalism 13 and all the way up to 17, 1819 and 20. But I mean, with an explanation of that and a gentle prod, it'd be interesting to find out how that works when those things seem to be we as physiological entities are able to juggle both the risk management and the action generating or option expanding sorry.

1:16:14 I'm really actually quite excited about that.

Here's what I'm feeling. How should I read that in terms of how far out I can make my next bet? From an allostasis perspective, I think that's really exciting. Like I said, if I can get a better sense of how that jump works in their model.

1:16:43 Daniel:

Yeah, definitely interested in that infinite time horizon and that mentality of like, what's the best physiological decision over the infinite horizon?

1:17:01 Dean:

That's a great question.

1:17:03 Daniel:

And yeah, the eternal now, the presence and then also just a little bit more mundanely. Like, what kind of data are relevant for this type of model? Is it data that already exists for people? Is it something where you can extrapolate a lot from a sparse data set?

Or do you need a bunch of implication to get good statistical confidence on the model parameter and extract findings that are like, nontrivial? And where's this technology or approach being used or where could it be used? There's like, a lot of things that will be interesting to talk about. Well, thank you for all the preparation and help on this one, Dean. And see you in the one and beyond.

1:17:54 Dean:

Alright, my friend. Take care.

1:17:55 Daniel:

Bye!

https://www.youtube.com/watch?v=tGd-mgSdbio

First participatory group discussion of the 2022 paper “Interoception as modeling, allostasis as control” by Sennesh et al.

Eli Sennesh, Jordan Theriault, Daniel Friedman, Dave Douglass, Dean Tickles

01:14

Exteroception and Allostasis.

07:37

Cognitive Science in the Light of Science.

11:29

A Review of the First 50 Papers.

12:06

Inactive Inference and its biology.

26:13

Homeostasis and Allostasis.

29:36

Immunity and interception in the nervous system.

31:31

The Out of Stasis and the Impact.

35:38

The slippery part of mathematical tractability.

37:21

Inferring from Action and Control.

39:31

Optimal Control in Active Inference.

47:46

Inferring motor movements from the brain.

56:49

Intelligence and the body.

58:22

Induction at the Hard Limits.

1:09:24

Optimal control with active coherence.

1:16:00

Physiology, Systems and their dynamics.

1:19:56

Ideas for the Reward Currency.

1:28:18

Kicking Off the Quiz.

1:28:41

Diseases of Civilization.

1:30:13

The Inclusion of Scientists and Engineers.

1:39:59

Inferring the Interceptive Networks.

1:53:46

An Evaluation of the Value Function.

00:27 Daniel:

Hello everyone. We're in Active Inference Livestream Number 50 Dot One, on October 22, 2022. We're discussing the paper interception as modeling, as control.

Welcome to active inference lab institute. We're a participatory online institute that is communicating, learning and practicing applied active inference. This is recorded in an archived Livestream, so please provide feedback so we can improve our work. All backgrounds and perspectives are welcome and

We're here in Livestream number 51 with our second discussion of the paper, exteroception as Modeling Allostasis as Control. Previously we had number 50.0 where Dean and I provided some background and context.

01:32 And now we're really appreciative that we'll have some authors joining for dot one and two to unpack and explore some ideas. And today it'll be great to hear from multiple authors, see a little presentation and dive Hinton the middle of things, the thick of things, as we do in the dot one one. And so we'll begin with introductions, then we will have a presentation and then discussion.

So we'll begin with introductions with non authors first and they can feel free to introduce, say hi and anything that they're excited to explore today. So, I'm Daniel, I'm a researcher in California, and I'm looking forward to understanding some of the formalisms in the model and how they connect to active inference and Bayesian mechanics. And I'll pass to Dave.

02:31 Dave:

Hi, I'm Dave. I'm a discourse curator, a student of Jaak Panksepp

I live in the mhBaguio

02:48 Daniel:

Dean.

02:50 Dean:

Thanks, Dave. I'm Dean. I'm in Calgary.

What's interesting to me is that on a metaphorical level, this started out me in an open field and I got into a forest, and that forest got denser and denser. By the time I dot two, section four of this paper, I started reading it over and over again, which is a fantastic sign, because if I have to read something many times to really get my head around it, that's good, because I don't question things unless I don't get them. And that doesn't mean that it wasn't spelled out correctly. It just means that you got my attention. So I'm not sure which author to pass it to first.

Maybe Eli, if you'd like to say hi.

03:35 Eli:

Hello everyone. I'm Eli. I'm the first offer on this paper. So a bit before the live stream started, jordan was mentioning that this work comes out of what we were sort of studying together in our lab at an energetics working group, brain energetics reading group, before the pandemic really did us.

And so when I was confined, I effectively started reading and rereading everything that we had gone through and trying to come up with some way to think about allostasis because in our group and in our previous publications as a group, the Interdisciplinary Effective Science Lab. We've referenced allostasis a lot. And every time I would ask, how can we give a mathematical or computational characterization of allostasis, I would basically be told, well, we thought Peter Sterling had one.

04:39 And then I would go look at Peter Sterling, and he's the originator of the concept of Allostasis, by the way. So there's numerous works by him on the subject.

And when I would look at Sterling's work, I would sort of spot a contradiction or contradiction in terms. On one side, he's specifically charting the variation in physiological parameters and regulation over time, where time can be the course of a lifetime, the course of development, or even just the course of a single day. And yet, on the other hand, if you ask him, well, how is this done? He would effectively say this is done by reinforcement learning via the Dopaminergic systems in the brain.

05:43 Now, the Dopaminergic systems in the brain don't track a shifting signal over time.

They just maximize reward. And so actually, in my view, at least as a computationalist, they were more homeostatic than allostatic. And from that contradiction and what followed on from it really came this whole paper.

But to reemphasize, I would say, and before we jump into slides material inside the paper, I think it's really worth emphasizing, just based on watching the 50.0 Livestream, that our group are more, let's say, biologists and physiologists in orientation than physicists. So Bayesian, the paper on Bayesian mechanics came out while we were writing this, and I don't think we really managed to integrate the two sets of Attial yet together.

06:45 Or together yet. That's not to say they can't or shouldn't be integrated. It's to say we don't actually have, so to speak, we don't always have the physics and dynamical systems expertise of someone like Thomas Parr or Maxwell Ramstead, Ozan Catal Friston.

On the other hand, we have very concrete notions of what biology and physiology we need to fit to.

And really, the bulk of this paper, the reason it's not just a short section four with some math is because we have to fit to the physiology and anatomy that we know about.

07:31 Daniel:

Thank you, Jordan. Feel free to intro and then eli off to you for some presentation for sure.

07:37 Jordan:

So I'm a postdoc in the lab here, so I think maybe I'll just give some context of where we're both looking, too, and how we've got here. So for me, I've had a bit of a weird path to get to this point in that I did my PhD in social psychology and moral psychology. It's then sort of got really interested in predictive processing perspectives, active coherence lab, and then really wanted to dig into that and find someone who's working on it around here in Boston.

So I'm working with Lisa Bellman, Barrett and Karen Quickly, who co direct the interdisciplinary cognitive science lab here. And like you guys saying, the perspective that we have is really more of a biologically grounded one or more of one that's based in physiology and neuroscience. So Lisa and Beren will joke that Lisa sort of handles everything from the neck up and Karen handles everything from the neck down, so together they form a whole person. And what I was really lucky to do was I stumbled into an existing collaboration that's been going on for about a decade here, which we call the Psychology Engineering Neuroscience Group, or the Penn Group, where there's been an ongoing collaboration with professors in the electrical engineering department.

08:51 Probably most importantly, Dana Brooks has really helped run it a lot, that Dennis Dogmas and Jennifer D have both also been really, really involved in this.

And so what they would do is they'd meet every week and they would sort of pour through active

09:55 So I've done a bit of work on thinking about how we can think about indoctrination or energetic Costa of information processing as a way of how individuals exercise control over a social environment by conforming to expectations within it.

And then at the same time, I've been interested in going to the other end and thinking about some of the details of brain metabolism and brain glucose metabolism that are associated with the bold fMRI signal so that we can really dig down deeper into the metabolism that's underlying the neuroimaging literature. But in the process of basically forming this energetics reading group where we've been digging into all of those topics to try to understand the brain biology. Eli and I really ended up working together in this paper to try to apply some of that energetics and biological work, again with a ton of health from Karen and Lisa, who really know the details of the neuroscience and the actual physiology.

10:56 I think Karen a specialty that Eli would probably say has been really, really critical for understanding these physiological systems. But basically, yeah, how we can have some of the parameters and assumptions of these active coherence models grounded in real biological terms so that we can start to look to the empirical literature, the biological literature, and sort of gain some more inspiration from that rather than just living entirely at an abstract level.

Cool. And with that, I'll hand it over to you.

11:32 Daniel:

Excellent. All right, I've unsured. Feel free to go for it.

Thanks for that context. And just a note, this paper does bring in some topics that we haven't discussed on any of the preceding 50 papers, many of which were also motivators of what you Seth out to explore. So I'll just crop in resize and so on. And Eli, please go for it.

12:03 Eli:

Alright.

So before I really get into the material of the paper, I think it might be useful to follow on from what Jordan said in order to additionally motivate sort of our turn towards biology and physiology here, which is that most of the time, active inference lab modeling. Note that I say modeling or active coherence lab physics, so to speak. You need a term in your expected free energy or in your joint density. That is sorry, the generative joint density, not the recognition one, which you would call often. I've heard it called the prior preferences, essentially a probability density over sensory outcomes.

That describes what it's hard to avoid entropomorphic language here, but well, what you want to observe now in real biological systems, that as we sort of can hear from Peter Sterling or numerous other authors, that cannot be fixed.

13:16 Prior preferences can't be fixed. I prefer different observations when I'm about to go to sleep

I saw that you discussed it last week in the Zero episode. Thank you for catching on to that and thank you to anyone in the audience and the listenership who caught onto that. The ergodicity assumption essentially allows you to exchange uncertainty about time or overtime for uncertainty in the moment.

14:19 So you can just say there's gaussian prior preference density, it has this much precision or this much variance, depending on which way you prefer to put your division sign. And then it's the same for all time.

Now, if you're doing a path space formulation, then you lose the tie between the free energy principle and conventional biological notions of homeostasis. Because now, after all, can't the set point be anything or everything? You need to know something about physiology, anatomy to tie it back. And so that's really the motivation we're coming from in this paper, is what if you have to acquire or learn prior preferences throughout development? How little can you bake in?

15:20 And so we start by sort of reviewing in the paper and in these slides the sort of perspectives that we study from study the nervous system, study the brain. One of them is predictive processing. I think that's probably going to be the important one for this audience. And in predictive processing, we talk about the perceptual systems of the brain, really the sensory systems, as performing approximate Bayesian coherence. So then you'll have top down prediction signals, bottom up prediction error signals.

15:59 Dean:

And.

15:59 Eli:

There'S this notion of active inference which says that we essentially treat motor outputs as parameters to the recognition model. In one of it in one of the earliest formulations before there was any expected free energy. But ultimately it still says in any new or recent formulation, we have some notion of prediction errors between densities, and this is an information theoretic quantity. So really we're talking about a divergence or an entropy or a crossentropy.

We want to minimize that. And we're not only going to minimize that by changing the top action prediction that flow through, say, the sensory cortex. We're also going to change these extra parameters that correspond to motor predictions, motor commands, motor references, depending on the terminology you want to use to refer to them.

17:01 So then in our lab, where we are sort of biologists of emotion, we often study interception. And that's really it's given a fairly vague definition on the slide here because there's a lot of debate among neuroanatomists about sort of where interception ends and exter reception begins, which exact modalities should be classified which way or another.

But really exteroception is still a set of or category of sensory modalities. And when I say sensory modalities, I am mentioning that specifically because the literature on interceptive active coherence

18:05 I have a recognition density. Action becomes effectively a parameter to fit the recognition density to the generative density.

And there isn't really a notion of an internal generative model that is separate, that separates belief and desire. So in a lot of the literature on interceptive active inference, you'll find coherence to having very precise priors or even innate priors about interceptive parameters. And you'll see this notion that you use active inference in the interceptive domain more than you use it in the somatic domain because you're trying to fit your internal physiology to a notion of apriori set points that are determined by evolution.

19:07 Jordan:

Do you think you could give an example of that eli what sort of set points people might think are?

19:15 Eli:

Let's see, I've seen carbon dioxide levels in the blood mentioned, glucose levels. Core body temperature is really the one that I tend to go back to because it really does remain constant most of the time. It can vary, but really, that's an inextremist type of situation.

So if you think about core body temperature, there's a circuit, and I believe. Jordan, correct me if I'm wrong, but this is the NTS again, isn't it? The nucleus? solitarius yeah. Okay.

19:56 Jordan:

Yeah.

19:58 Eli:

Essentially in the brain stem there's a circuit that codes the typical set point for core body temperature. And from active coherence lab perspective, you could say that is a fixed likelihood. It can't be reparameterized by some prediction flowing from higher up, or rather, most of the time it is not re parameterized. So that flows down as a prediction.

And then every temperature sensor in the body can compare actual temperature to desired temperature, calculate a precision weighted prediction error between them, send those errors back up, and then the brain can say, AHA, I need to find a way to minimize these errors. And doing so will effectively keep you in an environment where you can maintain your core body temperature around, you know, I think it's 98.6 Fahrenheit is the stereotype.

21:01 It varies for individuals. Now, the reason my next slide was about allostasis is because while there are bodily parameters like core temperature that usually behave according to a set point, really physiologically, most parameters do not have a setpoint. They move.

The regulated levels move all the time. So that includes heart rate, blood pressure, blood sugar, blood oxygen levels, various hormone levels. In the endocrine systems, inclination levels shift over time. And I mentioned inflammation because from the body's perspective, inflammation is not something with a set point of zero.

22:06 Inflammation is sometimes appropriate.

23:17 So this is a pretty wellobserved fact of physiology.

Informally, Peter Sterling, I would say, having invented allostasis as an observation that gets made, he then editorializes a little bit about it and says it should replace homeostasis as a mode of regulation. So rather than having set points, you should be comparing to something like a set trajectory. And in the ideal case, when you're theorizing, you should assume that there is no Global set point of any parameter. And of course, as we mentioned before, in extremists this is true, if you get ill, your body does actually override that circuit in the brain stem to raise the core temperature. That's why you'll get chills.

You're at the same temperature, but the regulated level has been shifted up.

24:23 Jordan:

There's also an interesting point to make if you go back for one SEC. You lately just that in the way that the sort of language of science evolves here too. It's worth pointing out because some people might be listening and might be thinking, well, homeostasis doesn't have to include set points either. You can have sort of hierarchical notion of homeostatic. You can have sort of multiple levels of control involved in that.

And some people made the same criticism of allostasis as an Ozan. So there's a paper by Carpenter. Yeah, there's a paper we cite by Carpenter that does exactly this. Right.

But the problem is that even if that's technically true and people who really know what they're doing and are using a concept of homeostasis in that way might already understand that you don't necessarily need set points. But the reality is that the way homeostasis tends to get used in the way that it tends to be understood, is it's come to have some of this association with setpoints sort of the simple thermostat model as opposed to something broader that includes multiple levels of control.

25:35 And so some people might be curbudging and want to say that homeostasis already includes all of these notions, so we should just reclaim the term homeostasis for that. I think we're more of the perspective that we're willing to just give that up and it might be time to just start using a different term to remind people of those other associations. So we're seeding ground a little bit when we're using the term allostasis to just not have to fight with people about what homeostatic really means.

26:13 Eli:

Yes, so Jordan is completely correct there, but I would actually even recommend that everyone listening if you can go find the paper Homeostasis a Plea for a Unified Approach by RHS. Carpenter. It's in our citations, and you should be able to type the name into Google Scholar. Go look at it because it'll really explain where our paper is coming from. As a short summary of what's relevant, what Carpenter says in his paper is that back in the good old days, they taught control theory and controls

And by back in the day, he really means back in like the 1940s to the 1960s before another new approach took over. And she says, hey, if you're an educated, mathematically mature and fluent controls engineer, then these awkward names are all really just different ways of cutting the same cake.

27:28 It's all a control system. It's a hierarchical control system. This is very evident, he says, in the anatomy and physiology that you'll look at.

He's even writing for a physiology education journal. And then he effectively starts complaining that everyone sort of strawman homeostasis down to this thermostat model. And he has to complain like this in 2004 because indeed, everyone really has sort of associated the word homeostatic with this homeostat model. Global set points, things like body temperature rather than blood glucose. And as a result, there's as a result, much of the actual control theory got simplified away.

So even as someone who is housed in a computer science department took a class on reinforcement learning and can work the equations of optimal control theory, I was not introduced to the concept of a reference signal as a time varying function until Carpenter, and that was actually pretty revelatory for me.

28:49 That rather than having an errors function whose minimum whose Global minimum is fixed for all time, you can have an error function that measures the difference between your actual trajectory and a desired trajectory. You can do trajectory tracking control when you have the mathematics. So we could say for our paper, for our purposes, if Homeostasis refers to this, thermostat style point tracking control, then allostasis refers to trajectory tracking control.

So moving on a little bit and getting back on the main track from our perspectives, informed by physiology and anatomy and a little bit of EvoDevo interception, and allostasis have both pretty well demonstrated themselves to be really central to how the nervous system is actually structured and seemingly largely concerned with the metabolism and efficient functioning of the visceral.

30:11 So for anyone who wants citations for this, I think it's Jordan. It would be Barrett. And who? 2015.

30:22 Jordan:

Oh, barrett and Simmons 2015 yes. Barrett and simultaneous Neuroscience.

30:26 Eli:

Casper hesp nature reviews neuroscience interceptive predictions in the brain there's a more recent review written by Beren Quigley, our other senior author on interception came out in, so you can really go check for yourself. And I would advise it just how central interception and visceral regulation are empirically to the nervous system. You could possibly design a nervous system for a robot that works differently, but the ones that evolved are ubiquitously, centered on keeping the internal Millidge of the body efficient.

So yes. Dan Pickles, do you mind if I.

31:18 Dean:

Have a quick question here?

Of course.

31:22 Dean:

The two offices here maybe can just confirm that my parachute is packed properly.

That's what I'm basically wanting to be comfortable with. So just stepping back for a second in that slide that you would just have up there, the warp and the weft here, the kind of the weave that you guys were working on on this paper was the out of stasis and the intersection. Those were your focal point, right? And then you've spent quite a bit in sort of prepping us for the difference between the discrete time aspect of what you're looking at and the Global capture rate because you say we can't get fixed. This is what I'm saying.

I want to make sure my shoot is packed properly. And then you're talking about biology and physiology. So just on that great big am I going to go splat or am I going to be able to land this relatively softly?

32:25 Can you maybe just tell me whether or not that is in fact, is it a comparison? Is it an intersection.

Are these things running in parallel? How much of this is risk management versus how much of this is strategic?

32:43 Eli:

I would think of it more as an intersection, okay? And when we're specifically referring to quantities like the Global culture rate, those are intended to be strategic rather than risk management or epistemic value.

So specifically, there there's a whole book on this, let's say Vigor the Neuroeconomics of Movement Control by Reza Shadmir, and it chronicles in very long form extensively the empirical evidence that real organisms will timeaverage their reward rate. So in order to move from an episodic setting to a continual control setting to a continual lifelong setting, you need some notion of indefinite time control. Obviously, you're not going to live until T reaches infinity.

33:47 But in the limit, you do need to have a coherent control problem, at least for modeling purposes, because you can't fix the end of, say, a bird's life in the lab on a laptop.

And there's two ways conventionally to do that. One is this notion of the Global capture rate. So the time average, the sum of all benefits minus the sum of all Costa divided by the total amount of time, and the other is exponential discounting. Now, for engineering purposes, exponential discounting makes the math and the computations much more tractable. And so in the early 2000s, they essentially found that real brains like basal ganglia and dopaminergic firing are best fitted by time averaging.

34:50 And then on the computational side, everyone ignored that and did exponential discounting. And so really, when we talk about something like a Global capture rate, we're just saying we're going with the biological evidence and writing down a model that accounts best for the empirical findings. If you want to, quote, unquote, try this at home, you are perfectly welcome to go ahead and switch to exponential discounting. It's fine. Or the machine learning community is starting to come out with papers on time averaging lately, the past couple of years.

35:33 Dean:

35:35 Eli:

Of course. Yeah.

35:36 Dean:

Thank you for that exploration. So if we're raising the question around tractability, that assumes that there's some sort of slippery or some fluidity piece to this thing that we're looking at.

What is that? What is that thing, that's fluid, that's slippery, that's causing us to not normally be able to model? Is that a feature or is that a flaw?

36:08 Eli:

I would say the slippery this is the slippery is the slip between map and territory. Okay?

So when talking about real brains, we know that we observe time foraging in the territory. What we don't know how to do is write an algorithm that provably, produces correct time averaging and works in practice, in engineering. So let's even say rather than map and territory because the scientist has a map as well, let's say the slippage is between empirical science and engineering.

And when we write out our model, we are really trying to address the empirical science. And we don't mind if engineers want to make their little slippage and use something that just makes the algorithmics easier, that's fine.

37:13 And in fact, that is what the deep active coherence community does.

Okay, so heading back a little more towards active inference when we read all of this stuff, this is sort of a bit of a Bible for our lab, Sterling and Loughlin. So Simon Loughlin was involved in some of the earliest publications on predictive encoding in the fly retina. Peter Sterling is the originator of the concept of allostasis. And what we actually notice, as mentioned a bit earlier, is this sort of slippage, another slippage or introduction. So they say when you get a reward, some dopamine is released.

This invokes a reinforcement learning principal algorithm.

38:14 Let's be careful with neural circuits that we're not studying in detail for the moment. That is, let's be careful how strong a statement we make about their function. And then most of the empirical evidence they review in the book is about the energy efficiency of sensory firing.

So we're really trying to say we want to move from something grounded in minimizing a prediction error, variational inference to something grounded ideally with an optimality principle in control.

So then there are some arguments for neuroscientists which are more or less intended to convince the viewing neuroscientist that people studying interception and people studying motor neuroscience need to work together on studying the viscera.

39:19 You can't study the viscera and ignore the motor branch of the visceral nervous system and the functions of that motor branch.

Now, regarding our statement of you can't just minimize prediction error. One might ask, what about active inference? And there we have to start being careful with the term active inference because as I have had it personally explained to me at length, there are at least the two different kinds of active inference. There's this very old, I think it was DAGs 2013, motor active inference predictions, not commands, active inference in the motor in the motor system. And then there's this notion of decision

40:25 And if you talk to the active inference community, read the papers that they can write for their own community. I would particularly recommend the International Workshop on Active Inference, which I believe is going to be a conference next year. They have three years of very good papers where many authors Seth out the explicit connections between active inference, control as inference, optimal control, etc. So really, when we bang on saying don't use active coherence to reduce motor function to sensory function, we're talking to some biology and philosophy who have been, let's say, quite enthusiastic about predictive processing, but a bit eliminated is about some of the mathematical constructs that are actually used in active inference.

41:29 So then for our psychologist audience, we have once again the. Argument that we are basically showing that you can and should do a fully probabilistic notion of optimal control in order to sort out what is going on with allostatic regulation. And we're going to take some inspiration from motor neuroanatomy in doing it.

So, looking at a simple model system, and this is getting into figures from the paper, we have our barrow reflex exafferent response curve. You have a kerated barrel receptor. It's in the keratin artery in the neck. It measures blood pressure projects to a circuit in the ants, in the brain stem.

42:29 And we bring this up here because the barrow receptor is often used as a model interceptor.

When I talked to Karen and asked for model systems of interception, she actually said, well, let's think about the paralyceptor first and again with contradiction. What we actually find, looking at the anatomy, is that the barrel receptor, the keratin barrel receptor, is the sensory branch of a lowlevel control circuit. So the NTS will then have, I believe the middle inflection point is coded in the ants here and doesn't really change much. But what does happen is that you can get topdown comma flowing into the ants and then changing the gain of this circuit so the slope of the curve.

43:31 And if you widen that slope so that the curve is shallower, then you're preserving responsiveness, you're widening the approximately linear portion of the curve while allowing for the blood pressure to rise and fall.

And so again, we see for the interception people that you really need to think about, you know, what is the role of this exteroception in control of the body and of the bicera? You can't just look at it and say it's a sensor. Well, okay, it's a sensor. Where does it project to interceptive cortex? No, not necessarily like, you know, the prediction errors signals that reach in teresceptive cortex to say I can't pump enough blood or something like that, might actually have already been processed by what I believe in the motor active inference literature is called a reflex arc.

44:41 So there might already be a reflex controller that has operated on that signal by the time it reaches the higher portions of the brain.

So in our paper, we set out some vocabulary for people to use if they want to, don't have to capacity curve in particular, we're going to tie it to the notion of a cumulative distinctions function. Later on there's some physiology terminology for people who want to learn it. And then we note the same thing that Carpenter does. Carpenter and a number of other papers, which is that this is a massively hierarchical control system.

Lots of regulated substances, let's say, or regulated variables are going to have multiple controller influencing them.

They can appear to compete sometimes, but actually it's cooperative regulation based on the fact that, so to speak, chemical species can't encode negative numbers the way a digital signal can. So when you do things with chemical signals, having these pairs turns out to be the way to monitor and control the dynamic range with the greatest sensitivity.

46:44 So then using this examples of leucagon and insulin, we can see that sort of normal glycemia is really more of a Lagrange and it's a range where you're going to have approximately linear response of insulin activity and you're going to have saturated out or really you're going to have thresholded out glucagon activity. So at a normal level of blood sugar, glucagon does not have to retrieve additional blood sugar from the intestine or the liver. It doesn't have to call for burning fat reserves. Essentially, you've eaten enough for the day, you're fine. Insulin is responsive in a highly responsive mode where it can give a linear response to a linear change in order to compensate for noise.

47:46 So now we can actually get towards, now that we have a controls way to think about physiology, we can get more towards these notions of active inference. And here we're going to go back to some of the sources that gave us motor active inference. One way to think about motor active inference is the brain sends a prediction. The reflex arc in the spinal cord attempts to minimize prediction error by comparing the prediction with the value read off of appropriate.

So again, one way to think about that is having a few extra ways to minimize prediction error, really entropy. Another way to think about that is to think of having a very elementary control system at the reflex arc level and then the brain prescribes the reference length that is the reference signal for that controller.

48:55 And it just tries to minimize the difference between what it gets off appropriator what it reads, the actual muscle length and tension and active inference signal. And this is actually a very I'd almost call it a fun circuit to study because of just how well documented it is, that there's something very much like, I would almost say, like a precision weighted pig controller in there. If you're a math person, then a muscle is kind of like a spring.

A spring can be the dynamics for a spring metal spring, stretch it and crunch it can be linearized around certain points. And so you can just about write down an LTI pit controller for an individual muscle spindle and you'll get two parameters coming down from the brain, one of which says the reference length and the other of which says, what's the sensitivity or gain against perturbation that you should exercise?

50:08 And this is actually how your voluntary movements are engaged. So really all of this stuff about references that we're talking about here is just putting forward the hypothesis that maybe visceral motor control works on the same computational and anatomical principles as voluntary. somatomotor control.

Of course, instead of the commands coming down from say somata motor cortex, they might be coming from ganglia in the autonomic nervous system with the higher level central nervous system basically just prescribing rough levels of activity, activation or deactivation for the two different sides of the autonomic nervous system, which then again, in this opponent fashion, semi opponent, fully cooperative fashion allow us to avoid encoding digital negative numbers and thereby give you very

51:23 So we eventually get to our figure, which essentially says, if I know what resource supplies, metabolic resource supplies, nutrients, oxygen, carbon dioxide, that sort of thing I'm going to have in the future, then my goal is going to be, let's not say to maximize uncertainty, nor to minimize uncertainty, but really to maximize resilience or freedom to stay in the linear portion of a cumulative distribution function where you can be responsive to any remaining to any remaining or upcoming perturbation. And so we draw here that you can have this capacity estimator close the loop and start directing motor actions.

52:23 Active inference lab in order to follow this preference for resilience against perturbation of the internal Millidge, which is then tied to interceptive state estimation, your other state estimators, your actual sensory services and this whole wiring diagram.

52:52 Jordan:

Maybe one thing just to and to right, just to underscore a point. Is that what I think? If you go back one slide here how this relates to the sort of adaptive range of the settling point too. And what I think is really interesting about this, right, is that you're not defining like when we started out talking about how you might traditionally think about set points for homeostatic like a very traditional thermostat model, right. What you're talking about here is that there's actually if the overall goal of the brain if the brain is essentially there to help regulate and adapt the sort of entire biological system of the body to circumstances outside of it that are constantly going to be changing different challenges that it's going to have to be responsive to.

Then you don't necessarily have a set point, but you have a range where you can where the physiology can be most adaptable to those perturbations and challenges.

54:00 Right?

I think that idea is really at the core of what we're trying to talk about radiolife, that you essentially want to have a range where the physiology can be adaptive. And you would imagine that if some of these parameters are pushed way, way far outside of the center of that sigmoid, then you're going to have a problem in that they will not be able to adapt to changes. You're not going to be able to be at that linear point of maximum adaptability.

54:39 Eli:

If you're down here near the threshold and you get some random white noise that pushes you over that threshold. Obviously there isn't a discrete catastrophic failure but also, obviously you can no longer mount a proportional response.

Your body is made of physical instruments which have a limited range of responsiveness.

And so our notion of allostasis to say when you can widen the range of responsiveness rather than narrowing it or rather widen the range of responsiveness when possible while narrowing the set of states or the distribution of states that you actually fall into yeah. So you look like doing somewhat opposite things.

55:39 Jordan:

And so would it be the case too right. That you could have there's different ways that you can have

Another potential problem can be when the sort of baseline level like you're saying is pushed far outside of that threshold, then also you're going to require a lot more work and a lot more control of that system needed to really push it far outside of that range, to actually adapt, really. And to push it back again. Yes. Which could cause other problems downstream as well. Right, but the point is just that the sort of range that you want the system to settle into is a range where it can be adaptive to changes and prepare for fluctuating certain circumstances, right?

56:48 Eli:

Yeah. So I think a good intuition to leave with, since we are drawing towards the end of the hour, is that if you were to try to minimize inter generative uncertainty, then what you might do is just stay home all the time, your heart rate will never vary, too much up and down. And we're living in the Modern world where you don't have to run away from tigers. So why deal with the uncertainty of going out and exercising or the perturbation of going out and exercising? And what our notion of allostasis here might tell you in reply is to say when you go out and exercise the curve gets wider and so the adaptive range where you can mount a proportional response gets wider.

So go out and exercise because it actually increases your resilience to biology, to future physiological challenge.

57:53 So it's still within the active coherence set of intuitions but we're really baking in this assumption that you should preemptively prepare yourself against possible challenge rather than effective rather than ActInf to avoid possible challenge. We've moved the handling of challenge into the body.

Dean, go ahead.

58:22 Dean:

As you get to those extremes of those crisis moments, we talked a little bit about this in the Dot zero. How does the interplay or the introduction proportion change between something that's interactive and range seeking to range reentering? I'm curious if the formalisms change as those extremes are reached because as you said, things don't always become irreversibly, catastrophically set. So based on what you guys have obviously looked at, what's your sense about how that relationship between interaction and instruction shifts as we get to those really hard limits?

59:18 Eli:

Jordan, you're often a little better on physiology than me. Do you want to take this?

59:24 Jordan:

I'm not sure. I think you might have it.

Let's see.

I'm honestly not so great on physiology because I rely on Karen for it.

59:43 Eli:

This is expensive metabolically, and it feels bad compared to how you normally function, but it should cook the germs.

1:00:46 And then when the extreme state, when that emergency is over, supposedly, hopefully, usually you'll be able to go back to normal function. There are, of course, exceptions, such as, say, Long Covet, right.

1:01:08 Dean:

Just to make sure that do you see a change in the amount of literally commands and the amount of back and forth as you approach those limits?

Or do you think they kind of just realize that they're getting closer and closer to a fall off point?

1:01:36 Eli:

I think that's actually an open and empirical question. So one of the reasons that we went as far as writing a full mathematical model in this paper is because there isn't that much empirical computational work on introduction at all. So if you ask very basic questions like is interception predictably coded below the neck? That's still an open question.

It could be that peripheral and terraceptors are just transducing a stimulus signal and then it's only predictably encoded when it hits the brain. We don't know yet. So we'd rather have some.

1:02:33 Daniel:

Briefly lost eli while Eli is rejoining. Okay, very interesting. A different path through the same material. Dave, if your question is for Eli, we can wait a few seconds.

1:02:55 Dave:

Not necessarily.

I have just a side comment. You don't necessarily have to respond to this. The discussion reminds me of two different fallacies. One is the dark room fallacy. If you want to minimize it's, a kind of a parody active inference lab.

If you don't ant to be surprised and just stay in a dark room where nothing changes, which has been dismissed pretty thoroughly by active coherence lab activity. Also, there was a fallacy, kind of a social Darwinist tinged interpretation of the observation that every species has a fixed number of heartbeats and therefore valuable people, members of parliament and clergymen should not work because you're eating up your lifetime, which of course isn't true because your heart beats more slowly. So it's stretched out more if you're in good shape, right?

1:03:56 But more relevant, the steepness of the reflex curve. I sometimes feel that folks working active inference lab cover maybe too much with the notion of precision.

1:04:37 Jordan:

That's interesting.

So normally the precision right, is normally applied to the predictions. So there's an idea of the precision of action prediction being applied. And in this case I think the idea is more of so it comes back to where the.

1:05:01 Eli:

You might talk.

1:05:02 Jordan:

About higher preferences being targeted in active inference models and I think the slopes, the response curve varies instead trying to target that use of prior preferences.

1:05:15 Daniel:

Right?

1:05:16 Jordan:

So it's trying to target specifically.

1:05:22 Eli:

Where.

1:05:23 Jordan:

Is the system trying to be navigated?

When people talk about prior preferences, they've talked about it sometimes in terms of the system having strong precise priors being encoded, like April I prior to being encoded to be targeted. And in this case I think we're trying to give an account of where some of those errors can come from and how these system and how sort of opponent processes or opponent chemicals can help regulate the physiology.

And we're trying to get a more natural approach of where this can come about from. But I think if it is replaced, I'm just trying to think to talk aloud, to think through the question. So if it is replacing basically a prior preference and if normally that prior preference would be handled by a sort of precision account of it, then to some extent the steepness of that curve is trying to tackle somewhat of a replacement of the precision.

1:06:54 But yeah, it's giving a different way of maybe it is a replacement for the cognition in that case. Eli's Back, maybe I can try to.

Answer your question, eli, do you want to complete your presentation?

1:07:16 Eli:

Sure. But just to answer the question, if we're talking about the gain on one of these sigmoid curves, then yeah, that's sort of a replacement for the precision, but it's really thinking about it's thinking about it the other way around.

So a variance quantifies your tolerance for error, a precision or a gain quantifies response to errors?

1:07:49 Daniel:

Yes.

1:07:51 Eli:

So when you're talking about purely sensory these extra receptive signals, the ones that aren't prescribing references to you in and way, then of course you want to save the neural response, which is metabolically expensive for precise signals.

If you're talking about an internal physiological curve, say reaction to a change in blood pressure. Then you want to try and make the gain shallower. You want to tolerate variance.

Sorry about getting my home modem. I think just restarted itself for no apparent reason.

1:08:46 Daniel:

We call that a sleep wake cycle.

1:08:50 Eli:

Yeah, it did some sleep phase gradient.

1:08:54 Daniel:

Updates, but it's simpler, it's refreshed.

It's ready for you to complete the presentation and then we'll return. Very interesting though.

1:09:13 Eli:

Okay, see share screen. Here we are.

1:09:21 Daniel:

Alright, continue.

1:09:23 Eli:

Yeah. So now we start getting into really what scant visual material is available for section four, which I think we'll have to go over in detail in a more Q and A format a little bit.

So if we then want to talk about how do we integrate decision active coherence into this allostasis view, then we can say decisionmaking is to this notion of optimal control subject to a set of expectations about the future.

1:10:28 Then part of how we're going to get into what this objective function is actually made up out of is to first take the intuition that if we start from neural circuits that can only do predictive processing as we know it, then one thing we can do with them is simulate some ensemble or population of potential state trajectories. Or really state action trajectories, starting from some initial state. Then given an objective function, we can estimate the time average. Given our ensemble, we can turn that into feedback control. Getting the stability in control theory, the closed loop stability derived from using feedback by then having a cognition model.

1:11:36 And then we can say ah, I'm going to update my entire ensemble or population of simulations by taking them from the recognition model which is conditional upon observed sensory outcomes.

And then having predictions from the recognition density which we're super scripting here with super script parentheses two in comparison to SuperScript parentheses one here.

We can then penalize a notion of distance. So really we can penalize the quote unquote size of the update in information theoretic terms. And if you've seen a free energy or an expected free energy written out term by term before, you should have seen one of these.

1:12:42 It's a kale divergence.

But what that gives us is feedback stabilized control using probability models and that actually gets to more or less the end of the slides per se.

So as a few summary points, our computational model gives us a useful notion of affordance competition. Basically run a bunch of forward simulations. Pick the ones that are going to have good expected values over time. Averaging to actually enact as motor references the sigmoidal curves after we've taken their derivatives to convert them to probability.

1:13:44 Densities, then taken the logarithm of those to convert to log densities, which is much more typical for active inference like a log prior preference.

Those actually provide a notion of common currency because now we've normalized all notion of probability mass to one. So a density over one variable and a density over the other variable have the same units. We don't need any more notion of a reward currency in this model.

Then there's some encouragement for the anatomists and physiologists to say, hey, let's go look at autonomic and visceral motor regulation and see if we can understand it in terms of these motor control circuits at the low level.

1:14:47 And that just brings us to some very overall conclusions.

Ideally, our work should be placed in dialogue with active coherence as control work by other authors and of course, acknowledgements. You can really see here how much work went into this on behalf of absolutely everyone in the team and references.

So I'll stop sharing and we can shift to a more interactive format.

1:15:28 Daniel:

Awesome. Well, thanks for sharing that. And so where was that previously shared? In what context?

1:15:40 Eli:

1:15:42 Daniel:

All right, cool.

1:15:44 Jordan:

The College of Engineering group your time.

1:15:47 Eli:

Yeah. So the slides are really made for this, like biologist psychology with a few engineers group.

1:15:57 Daniel:

Cool. Okay. Well, many, many ways, many ads to go just to kind of highlight a few pieces under this broad umbrella of physiology. One important point you raised was how much homeostatic same stasis is in affect versus a mechanism of actually is that stabilization sometimes empirically of stasis and even homeostatic, is that Underlane by a drive to a set point as it has been simplified or understood, as in that simple thermometer model? And then to what extent do we bring in allostasis hornesis arousal and different biological phenomena?

1:17:01 And consider these all part of just the dynamic and multimodal homeostatic engagements of complex bodies versus discard the old and with the new and how much to lump and split physiology when even at the single cellular life form level they're engaging from a computational or control information theoretic perspective in processes that are analogous to some of these.

That's one point that we can explore. Another area to explore is on that theme of what are these systems doing and how do we model it? The Map territory or the engineering basic research question? We could talk about a given physiological process, body temperature stabilization or the barrow receptor, the glucose and so on.

1:18:05 Is there the minimization of a difference, for example, between preferred and observed?

Is there a maximization of reward according to some reward function? Is there a maximization of precision? Precision on what? Is there a maximization of responsivity which corresponds in the sigmoidal curve family to the linearized region? Are there cases where all four of these things are going to be happening indistinguishably?

Is there a case where some of these phenomena are occurring at the detriment of others? Can we differentiate models and actually make unique predictions, explanations and control systems if we move our emphasis from one of these lenses to another lens?

1:19:06 And how should we think about different physiological systems ranging from the implicit and very ancient mechanisms to those which consciously may even feel like, for example, error, minimization, reward maximization, precision maximization, responsivity maximization. So I'll pause there and either authors may make some remarks or anyone may raise a question or thought.

1:19:56 Jordan:

I wanted to ask you maybe just a director than this cue you talked at the end about that. This gets us away from having to have a reward currency.

1:20:09 Eli:

Yeah.

1:20:11 Jordan:

And maybe I'd be interested if you can elaborate on that a little bit.

What would the typical role of a reward currency would be and how does the framework that you're proposing change that? Right?

1:20:27 Eli:

Yeah. So really I back off and say what changes? This is the active inference point of view, right?

Typically if you're doing something like if you're someone like Cycle Deneve or Sam Gershman, then you think about reward as in a reinforcement learning terms as something that the brain has to maximize and then you would say, all right, well, I want the uncertainty of my beliefs to be minimized while I maximize reward. So those are then two separate modular computations that have almost opposite goals. One of them is to minimize uncertainty right now and the other is to maximize reward over the long term and income's active coherence and really says no. No. If you phrase this as a variational optimization problem, then you can get a unified objective for this where the common currency is, so to speak, evidence, really evidence that you're following the correct trajectory, evidence that you're executing a behavior correctly.

1:21:47 And evidence varies in terms of, I guess we would call them nuts or bits of the units and information theory. So if you're using E as the basis of your logarithm, then it's not if you're using a log tomb base, it's BIFs.

My dogs are getting picked up for their walk.

1:22:17 Daniel:

Yes, this is a very interesting complexity perspective where we'll get reward maximization over time when we increase our precision. Now everybody agrees on that. And is it going to be the cart before the horse or the horse before the cart? And which one's the horse and which one's the cart? And framing the unified objective function in information therapeutic terms as a surprising bounding heuristic as has been done in Bayesian evidence lower bounds for a long time by framing surprise inclination bounding as the unified objective function and currency.

Then there is the realized maintenance of homeostatic or however you want to call that without needing a traditionally structured maximization of reward as defined by a reward or time discounted reward function.

1:23:26 And it's also very interesting like we're not trying to accumulate body temperature, we're not trying to accumulate glucose. If we were playing a game where simply more points were better like some social and subsocial games, then a unilateral optimization via maximization paradigm makes a lot of sense. But for the kind of physiological infinite games that we play, as you highlighted with the infinite horizon, then it may make more sense to have a bounded responsibility and an emphasis on controllability under inherited errors that those controllable ranges are the survival ranges. Otherwise, how could one have existed for generative rather than try to stack up glucose?

1:24:30 Eli:

Yeah. So I think it's always really interesting to go back and read Peter Sterling in this light because beyond just the formal physiological material, there are these stories that he can tell of, for instance, people living in longterm stressful. Situations and they develop what we would now call the diseases of civilization, which, you know, Sterling sort of implies are the diseases of homeostasis living. Too much the same too much of the time.

And indeed, speaking of not wanting to stack up glucose, this is an actual disease that happens to people. That is called diabetes. It is considered a pathology. And so there's almost an interesting misfit between that intuitive notion of reward or at least let's sneer slightly and say that economic notion of reward, which has to be a form of accumulative wealth in a common currency versus physiology, in which too much of a good thing is actually a bad thing again.

1:25:50 Jordan:

Right.

And that actually comes back to if you part of what this is contributing, then right in one way is a sort of shift in metaphor.

1:26:01 Eli:

Right.

1:26:03 Jordan:

I think that point about an economic conception of value and a reward is useful to have a counterpoint to that. Because as Eli is saying, there is no upper limit to economic reward. There's a benefit to accumulating it.

If you think about sort of accumulating capital to spend it in this case, what we're focusing on is how to basically keep balanced and adaptable so that future challenges can be actually encountered and dealt with. And that sometimes means packing light, not keeping so much glucose on hand so that you can deal with the reward or deal with changing circumstances and adapt to them. But you can't.

It's maybe been a pretty serious problem to have this completely abstracted notion of value that is endlessly accumulative and.

1:27:12 Eli:

Doesn'T.

1:27:13 Jordan:

Interface with any of the biological realities of what systems are actually doing. Right.

1:27:20 Eli:

Yeah.

1:27:22 Jordan:

1:27:30 Eli:

Yeah. Before we go to the question, let's sum that up by saying bank accounts are unbounded and they're useful because they're unbounded. Like an economist can conceive of trillions of dollars in assets in a way that my body cannot. Bodies are bounded, they are physically bounded. They are made of a finite amount of matter at once.

If you try to put too much more into them, something bad will happen.

1:28:07 Jordan:

Actually, after setting us off on that channel discussion, I've got a duck. Off a little bit early, but I'm going to try to be back Force 50.2 next week and I'm really interested to see where this conversation goes. I'll catch up on the rehab.

1:28:18 Daniel:

Thank you.

1:28:19 Jordan:

All right, thanks.

1:28:21 Eli:

If nobody minds, I'd like to ask Dave his question first just because I was about to when I got kicked off.

1:28:29 Daniel:

Yes. Go for it, Dave.

1:28:32 Dave:

Is that one that I said? Yeah, I know which one that was.

1:28:37 Daniel:

If you have a new question, is fine.

1:28:38 Dave:

Oh, yeah, that's probably better.

1:28:41 Eli:

Yeah.

1:28:41 Dave:

Just to what we were speaking of just now, the diseases of civilization. There is the rumor, and maybe this was just a fallacy or a misunderstanding, that people who managed to stay in London during the

People were just preposterously saying because they didn't have time to be sick, they didn't have time to be crazy, did that really happen?

Did the sense of mission override what otherwise would have been general stress syndrome causing breakdowns?

1:29:34 Eli:

Does someone know the detailed history of the London Blitz in World War II? Because I really don't. It's all right.

1:29:41 Daniel:

Not English dot 1.5 journey for us to explore, but to speak to it generally. It's an interesting question as well.

To what extent by comforting and regularizing we even work against that and let alone neglect other trade offs and incur externalities Dean.

1:30:13 Dean:

This has been fantastic. Here's my thing. Maybe in the Dot two, we'll get into the I mentioned at the end of the Dot zero. I was hoping you really had some really velvet gloves to walk me through the 4.4 because and especially after the context you've been able to provide us today around the idea that engineers and psychologists came into a room. Now, I don't know if that once you got into that room, it became an intersection with red light, green light, and you guys kind of played a red rover comma over thing or whether.

1:30:52 Eli:

You know it so well.

1:30:54 Dean:

Here's the thing, because I actually did work with CFOs and engineers, what you discover is there's a bit of an isomorphist I want to be able to diagram this out for you view that has to be biased for engineers. And then there's the spatially enveloped view of the psychologist, right? Like they're in their phenomenological space. And what you've done is you've tried to say, when those two worlds come together, I don't know if it's a collision, I don't know if it's cooperation.

It's a variety of things, right? It's complicated. We'll just leave it there. But my question is this as I got to 4.4, it felt like if I was skiing, I went from a beautiful powder field to some sparsely distance trees to tighter and tighter. And finally I was like, I don't know how it's going to keep going because there doesn't seem to be any more gaps here.

1:31:56 It's just getting too tight for me. And the reconciliation, like when you're skiing as a metaphor is you're not looking at the trees, you're looking ant, the nonsense, the non objects. It's a reconciliation. And when we're talking about dodgeball as your metaphor or whether we're talking about glucogon control these to me, what you were describing up until that point was essentially you were saying for us

We can say that in order for the process to carry forward, to continue, there has to be some addressing of those factors and then there has to be the reconciliation. Just like when the engineers and the psychologists are proximal to one another. It's an entanglement. And it's not that the engineers get to tell the psychologists what to do any more than the psychologists get to tell the engineers what to do.

1:33:01 Right?

So if the behavior piece, if the idea of the biology and the physiology is if I do this now in real terms, I have to look at that. And you guys had an L, four different time frames, right? I can manage that. You spoke clearly to that. I read that and it was clear to me I can coordinate that.

Again, that was very clear. And then I got the 4.4 and I simply lost the thread because what I was looking for was the reconciliation. I will align this next move with the range recapitulator. That's what I was expecting next. And then so I went, okay, so where is the strategy?

Because that's there when psychologists and engineers get into a room, they don't just abandon their strategy.

1:34:04 It comes with them. It follows them into that space and carries them to that question of I reconcile an advantage and all of the above until I choose this choice while always keeping all of the above. So you guys talked about that in other parts of it. You said we can't just abandon it.

But I couldn't understand how the formalism reconciled it. So I'm sorry that's such a long winded question, but your paper always spend 6 hours of my life going, these guys have dot two be much closer to answering this because I've never been able to answer it. But then I got lost and I just felt like, oh man, what am I missing?

1:34:51 Eli:

Okay, so I'm going to disappoint you slightly and say what you're missing is.

1:34:58 Dean:

That.

1:35:01 Eli:

I think what's missing from our writing is really being clear that we're working under a very unusual set of constraints in how we formulated this model. So specifically, unlike say, Sam Gershman or Cycle Deneve or unlike the literature on deep active inference in computers, we're assuming that you essentially don't need an extra set of computational ingredients for reinforcement learning.

So we're saying, assuming that you can do only the computational operations known to be involved action prediction processing, what can you come up with that will handle a control problem? And the answer is this very specific thing with these nastily involved derivations called pathogen role control.

1:36:08 And you'll notice that when I was going over those slides, I basically said, let's just say you can simulate possible futures, like possible episode length courses of future activity, and you can evaluate them in terms of your objective function. And then you can update them by means of a recognition model or by integrating prediction errors and using predictive coding. Then how do we build a formalism out of just those?

1:37:16 That is, if you have to penalize how much you change neural foraging over time, or how much you change your mind and update your beliefs over time because you only have so much metabolic power in your head, then we include a penalty term for that. And we can say this can all just be done by embodied simulation and reference configuration motor control. Does that mean this is how the brain actually does things?

Of course not.

It does mean that if you want to do your modeling with I think Andy Clark tends to quote Blei and say, if you want to do if you have a taste for desert landscapes, then we've given you a computational model that is basically just sand and rocks. And as such, yes, it's something of a hostile environment.

1:38:22 Walk without rhythm. You won't attract the worm.

1:38:28 Daniel:

In the planes of Active.

1:38:33 Eli:

Yes, if you live behind the shield wall where we have TD estimated value function. Good for you.

1:38:42 Daniel:

In the stretched sigmoid with broad variability, so stretched that it is flat and plain like, but still highly controller within large bounds, that's where we're oscillating. Yeah, very interesting. It'll be, I think, great in our lab to pick up a few points.

1:39:07 Eli:

From am I the one cutting out again?

1:39:10 Daniel:

I still see you.

It's okay.

1:39:15 Dean:

Yeah, you're back.

1:39:16 Eli:

Alright. You flickered a bit.

1:39:18 Daniel:

Okay.

In the last minutes we can talk about some ideas from earlier in the paper. Look at any of the figures, and then in the dot two. That will be awesome to really approach the formalism and help Dean on that

What would be something to go to in these last minutes?

Justine.

1:39:54 Dean:

Maybe I'll be able to get a chance to elaborate with this bit more with Jordan in the next one. But I'm curious. You took pains at Great Lakes to say, look, this doesn't map directly onto all the complexities that we know exist because you said you started this in 2019. You had a bit of time on your hands, and Dean did kind of allude to this at the beginning. Were there discoveries that you made that you didn't anticipate because you were very also very respectful in who you acknowledged as sort of laying the groundwork here.

You had a bit of stability to work off of, but did you find yourself being introduced to things that weren't there prior to you guys coalescing around this?

1:40:56 And do you think it continues to evolve, or does it just stay on a theoretical level?

1:41:06 Eli:

So actually, I'd say for me personally, the big unanticipated discovery was just how little we know about interceptive neuroanatomy and neurophysiology and I mean in the periphery. So our lab with Lisa and Karen, lisa handles the stuff above the neck. And so we've got Barrett and Simmons 2015. There's a number of other good papers saying essentially you look at the brain architectures and it looks like the at least in cortex, you know, the interceptive and visceral motor cortices are fairly central to the architectures. And then you ask, okay, so what kinds of signals are coming in from the periphery to then be subjected to predictive processing in cortex?

And you basically get told, well, interceptive signals, obviously.

1:42:07 So there was that moment when I was working with Karen and realized, oh, okay, so it looks like there's actually this close analogy that we could hypothesize between the known function of a somata motor circuit for voluntary motor control and this way of handling barrel reflex function. And it looks like for the barrel reflex, you know, you can voluntarily change the gain or the tolerance, those being inverse of each other. Changing the operating point voluntarily doesn't seem to happen, but it does seem to shift. And it does begin to look as though we can stop just saying there are interceptive signals, we don't know anything about them. Right?

1:43:07 And instead ask, how could we break down the autonomic nervous system and the exteroception periphery into these control circuits where there's a reference that flows from above or is possibly built in as a prior and then a sensor and then a motor neuron or an effector.

1:43:33 Daniel:

That, again, total speculating. One can imagine that loop could be ultra local or even get cellular electrical junction. So as local as could be to close the motor control loop. And then there would be potentially a more meso scale purely within the periphery, maybe some sort of motor coordination or vasoconstriction type actions that are being enacted through local neural networks and other systems. And then when you dot two make the call to the central nervous system and engage at that level, it's the highest capacity of inner modal memory computation, all these other complex phenomena which then

1:44:36 But the entire integrated dodgeball performance is not going to be located to a brain region any more than it would be located to a fingertip because it all needs to be coordinated and not every call can be local and not every call can be Global. So finding out how bodies as territories and our models as maps wire things up is going to make models that are more interpretable, better aligned with empirical data, making more useful predictions and explanations. It's a very interesting angle and I.

1:45:25 Eli:

Would say, just to piggyback a little as a modeling paradigm, I think this is one of the real strengths of active inference, is that once you're dealing with these probability densities and log probability densities, you are able to start sketching out these hierarchical structures. And that doesn't mean that every hierarchical active inference model is automatically a map of the nervous system, but it does mean that you have a language that is at least minimally capable of expressing what we so abundantly find in the empirical evidence.

1:46:05 Daniel:

Yeah, one part of the paper that was very interesting in reading it remarked how although most papers are written in words, this one was very wordforward. Each action had a preamble content summary sandwiching technique, as did the paper. At a higher scale, the nomenclature was upfront and clear and then the relationship between the cumulative distributions and the classical PDF type probability densities was made clear. But this exactly connects something that has, in the generic case, a guaranteed inflection point interpretable thresholded values.

1:47:07 This is why Sigmoid functions are used as activation functions in artificial neural networks with and optimizable Laplacian approximation like inverted quadratic form that is able to be used as a log probability.

And so really, like, especially with figure nine showing the stepwise relationship opens the door to like hey, if you've seen a Sigmoid somewhere, now you can think about that as like a PDF hiding a PDF bell curve. And then where you have seen a Gaussian or bell curve or a Lagrangian approximation, you can go the other direction and think about that in terms of a Sigmoidal response action.

They're rarely connected so clearly, though, those with familiarity, it's almost the water that they swim in and those without familiarity wouldn't see the connection and the challenge and the opportunity is like to stick in the middle and stay in the connection space to raise attention to some of these relationships.

1:48:30 Which again, otherwise you could have a whole subfield of physiology working on the Sigmoid response curve and a whole subfield of hierarchical predictive processing models working in the PDF space or log PDF space. And it's just a derivative and a log or an exponentiation and a derivation away from those two Fields being formally connected, not just as like a speculative review paper. Someone could or should do this, but it's done. We just didn't know.

Cool.

1:49:09 Eli:

So I think regarding the writing, I really have to hand credit to Lisa and Karen for a lot of things where

And then I think the actual insight that you can take one of these sigmoids and turn it into a PDF I think came after hammering our heads on some of the embodied predictive processing literature a bunch of times because it is one of those things that is literally embodied.

1:50:21 Dean:

Yeah, I just wanted to get this in. What attracted me to the paper in the first place was the allostasis and the interception. What kept me going back to it was and we talked about this in the dot zero was wayfinder, that rule perspective swaps versus a way finder. When I first started reading this paper, I saw the metamorphosis from identifying a way to find things. And now, after having this conversation with you today and Jordan and, of course, the usual suspects, it's clearer to me that this paper is trying to play that role of being wayfinder, prospective identifier, as opposed to we found our way or this is our way to solve all the world's ills.

1:51:30 Which, of course, I don't think it was ever your intention. But when you pull things that are seemingly quite far apart, like Palestine and interception, I get excited. But as you pointed out, pump the brakesteem, don't get too excited here. We're doing the best we can. So on that level, my Amygdala is still functioning correctly.

1:51:59 Daniel:

In our Closing thoughts with a driving example are we accumulating speed or minimizing the amount of time? Or are speed limits even set as exteriorized norms and stigmaic marks on the niche, such that a variety of cars from a sports car to and 18 wheeler can be within a zone of optimal controllability, taking into account the presence of crosswalks and so on? And so alongside as we think about what we want to explore in the Dot, two alongside diving into formalisms, trying to do some excavation and exteroception on how and where the economic optimization as maximization is implicitly used and where some of these other notions that were being raised without needing to be polemical or replace value maximization, but where we can see these other survivability criterion as potentially different decompositions of unified objective function that are informational and so on.

1:53:29 I think that's going to be quite far ranging because there's more situations, I would venture where we would rather have controllability and expectation bounding and meeting rather than point stacking. So, final comments you like?

1:53:52 Eli:

Yeah, so I just really want to close by reemphasizing that I think I have this joke on my Twitter profile abolish the value function. And that's really just a pun for the people who can get it. But we're not trying to tell people, contrary to their subjective experience, oh, you don't really have value in your brain. There's actually just trying to track your reference trajectory. So in the .2, we can talk about which specific kinds of feedback control, what kinds of feedback mechanisms are really being spoken

And I think as a preview, it's negative. Both negative in the sense of avoiding negative reinforcement and in the sense of trying to flatten out a response function and be able to proportionally respond.

1:55:01 With the benefit of hindsight, this paper is going to have a pretty limited domain of application, but it's helpful in that it gives us a language to turn around to the empiricists and say, this is what we want to actually look for.

1:55:25 Daniel:

Any closing comments? Otherwise, it's a great note. Well, Eli and Jordan as well, thanks for coming out and for engaging in one Brea, and we'll see you next week.

1:55:39 Dean:

Thanks, guys.

1:55:41 Eli:

See you next week.

https://www.youtube.com/watch?v=4o-LmkycAC0

Second participatory group discussion of the 2022 paper “Interoception as modeling, allostasis as control” by Sennesh et al.

Eli Sennesh, Jordan Theriault, Daniel Friedman, Dean Tickles, Ian Tennant

01:17

Intelligence as modeling, allostasis as control.

06:21

Interceptive Exposure Therapy.

09:16

Hormetic Stressors and the Future.

14:31

Ergodicity and the Future of Human Systems.

16:20

Social Networks and the Allostasis Response.

20:55

The laser on runners.

23:59

Laser in Human Tasks.

26:41

Limits to pacing during a marathon.

38:34

Proposition 7: Perspective Swaps.

40:14

Philosopher and Engineer's Perspective Swap.

53:05

Active Inference and the Social Space.

58:40

Brain metabolism and its costs.

1:03:15

No More Uncertainty: Brain Regulation.

1:06:45

Uncertainty about the immediate lived environment.

1:14:18

How is the nervous system built in specific?

1:23:57

Autopayesis and Living Systems.

1:29:48

Dean's Bridges and the epigenetic story.

1:33:38

Inferring the Markov Blanket.

1:37:11

The Metaphor of Active Inference.

1:42:55

In the World of Math and Dodgeball.

1:49:34

Control and affect in neuroscience.

1:52:18

A Mixed Feedback Control System.

00:32 Daniel:

Hello and welcome. This is ActInf Livestream number 50.2. It's November 3, 2022, and it's it's our third discussion on this paper. Welcome to active coherence lab institute. We're a participatory online institute that is communicating, learning and practicing applied active inference.

This is recorded and archived Livestream. Please provide feedback so we can improve our work. All backgrounds and perspectives are welcome and will follow video etiquette for live streams. Head over

And we had a dot zero background and context video.

01:33 And two weeks ago now, we had a great number 51 discussion. So we're just going to have introductions of people who were here last week, and then Iain will share something for a few minutes, and then we'll be discussing whatever people want so we can each just say hello and anything that we want to explore today or some reflection from the last two weeks. So I'm Daniel. I'm a researcher in California and I'll pass to Dean.

02:11 Dean:

Thanks, Daniel. I'm Dean. I'm here in Calgary, in Canada, and not much to say other than I'm looking forward to getting past the content, which was the zero, the context, which was the one, and figuring out what we can conceptualize into in this two. I'll pass it over to Jordan.

02:30 Jordan:

Sure.

So I'm jordan. I'm a postdoc working with the sophalgen Barrett and Beren quickly at Northeastern. And I think I said the last time that we've done this, this paper sort of emergence out of the cybernetics reading group that we've done. So I'm gradually interested in brain energy metabolism. I've been doing some other work on that and was not here last week in the week between these sessions because I was at the International Conference on Brain Energy Metabolism, which was very fun.

And, yeah, I think I'm excited to get to the conceptual details of this paper here, too, and interest in thinking about what a control theory model of the brain and then the exteroception looks like.

Pass it over to Elaine.

03:15 Eli:

Hi, I'm Eli. I'm the first author on the paper, grad student with Theon villain Domain, who is sort of our undermentioned co author, and with Lisa Field and Barrett and Karen. Quickly, I would say that I just got away from a conversation with Maxwell Ramstead, so I'm actually a bit excited about active Inference. He really clarified for me what it is and what it means.

03:42 Jordan:

Yeah.

03:42 Eli:

And I think I could pass to is that all of us or Iain, do you still need to go?

03:50 Ian:

Hi. Yes, thank you. So I'm in I'm based in England, UK, and so my background many years ago was in kind of undergraduate of biochemistry and then PhD in molecular biology applied to immunology and how white blood cells can determine between molecular signals of safety and threat.

I didn't stay very long with that. Moved on to working on environmental management projects and

04:56 So when I a few years ago discovered there was a group of small group of researchers studying exteroception, I got very excited very quickly.

And I've been involved recently in a little bit of research on training for improved Interceptive awareness with a university nearby here. And when Daniel shared that this paper and said it was going to be on the Active Coherence Institute, I got diddly excited and wasn't quite sure why that was. When I was trying to figure it out and watching 55.0, I asked if I could share a few pictures, which maybe I'll do now. If I can share screen to, is that going to be possible?

05:43 Daniel:

Share it and I'll crop it so that it's the whole screen.

05:46 Ian:

Okay. So I thought, why was I so excited to see this paper and why I hope it might be able to help people in the therapeutic world? Because I know that you've sort of talked about physiology, meeting engineering, but then this is a slightly different, maybe a slightly different take.

06:07 Daniel:

Go full screen or just give me 1 second. Give me 1 second.

06:13 Ian:

Can you see that now?

06:14 Daniel:

Yup. I'm just going to make it big.

Just give me 1 second to get it finished. All right, go for it.

06:21 Ian:

So in the dot zero, I heard people talk about baked in reflexes and they've made me think of these pictures which have been going around on the internet of why sorry, why are cats scared of cucumbers? Is it because they're both Beren with to be scared of snakes? So kind of some kind of genetic cucumbers look like snakes, so they go from feeding mode into forward model?

Or is it that their cruel owners have just put something surprising behind them so it's just stimulating a startle reflex either way. I don't know what the cat's interceptive experience is, but there certainly seems to be something that is automatic is happening there. So thinking about in the therapeutic world, what we're often trying to achieve is if a behavior has become maladaptive and starts to feel like it's reflexive for a person.

07:23 So let's say a phobia against spiders, or a phobia against public speaking, or a phobia, a fear of going into public spaces, then the person may feel like, I know I'm going to suffer in this situation. It's

But with Interceptive Exposure therapy, what I find is interesting is that people are able to, in a safe space, able to say, okay, when this thing happens to me, I feel maybe short of breath tightness in my chest. So if we can recreate that sensation in a safe environment can gradually they learn to change whatever their predictions or their beliefs are about what that sensation means. And it seems to work. One method of doing that, if breathing is an issue for people with anxiety, is to recreate it by breathing through a straw. So the aim really is to turn something maladaptive into a more adaptive behavior or a vicious cycle into a virtuous circle.

08:26 So instead of triggering this kind of reaction which feels unpleasant and involved, reflexes or supposed reflexes are being triggered that are linked to shortness of breath or increased heart rate instead. So they can learn to create some changes in the body that might be associated with something more pleasurable, such as relaxing with family on a beach or some kind of pleasant situation. So different changes in their autonomic nervous system. And in general, what we are sort of interested in doing is using interception as an access point to be able to untangle the story, the thoughts that people have from the situation they're in and the bodily sensations that they're sensing or that are arising. So Dean, you mentioned about packing your parachute.

This was another kind of image that came to mind. Most babies are probably born with some kind of reaction that stops them throwing themselves out of high places.

09:29 But it does seem to be possible to override any interceptive fear and for some people even to enjoy throwing themselves off high places. Likewise, we can learn that situations such as maybe sitting in front of a laptop with an email box full of emails for some people can lead to an interceptive sensation that's like a sinking feeling or a cramping or a heavy feeling. Then they weren't born with that.

But they've learned to associate these situations with something really stressful.

This was from the paper, I think Jordan or Eli you referred to last year. Sorry, last week, the dot one. I haven't digested it fully but it really becomes apparent that the direction of these circles and the loops within loops are quite, quite complex.

10:37 But I really liked the way that you describe these are my reflections now from what where you ended in one, which was this idea of generative control or optimal control.

And I was sort of taught about feedback loops as being like thermostats and maybe fat levels in a person's body, being influenced just by the hormone leptin, for example. But it seems that the set points and the settling ranges are much more mobile than once was thought and we see that now with and involved a lot more cross talk. So rather than just targeting something like leptin as the problem for the obesity sort of crisis, then this is just a stat taken from UK government office which created an obesity systems map that identified 108 interconnected variables that determine people's energy balancing in correlation to obesity.

11:43 And some of those things might include marketing and advertising social pressures. So how do we bring all of those things into these types of models that are being created?

And then there's epigenetic factors as well. So, you know, people can inherit their exposome through epigenetic changes and can that change their intraceptive predictions? And how I think about this from a kind of health mentoring or coaching, I'm not quite sure. I've wrapped my head around time averaged the concept of time averaging completely. But if I have someone comes to me and they say we're

13:09 How do those two different kind of competing desires work with each other? Is it a battle of will or some of them seem really deeply reflex. They both seem deeply reflexive, but they are often at odds with each other.

And again, with this kind of time averaging I was thinking about in the allotment, this isn't from my allotment, but plants. When they're stressed, they bolt early and flower early if they think their environment is dry or not, haven't got enough nutrients or enough space for the roots, and they will flow early, go to seed early. So is that what time averaging is related to? And the other thoughts was about this idea of someone mentioned about exercise being good for you because it's a short term stressor and it helps your heartbeat slower over the long term. I see lots of people talking about hornesis in the health and fitness and hormetic stresses in the health and fitness kind of arena, but we don't seem to have a good model of it or a way of telling what the sweet spot is for a hormetic stressor.

14:24 Yes, and there's lots of people doing hormetic stresses at the moment, wim HOF and hot and cold therapy and so on. And the last thing the last thing that interested me after was this idea of ergodicity and the distinctions you made in this paper between ergotic and ergotic systems. And I was at a park on last Saturday and talking to some of the people, my friends at Finnish about how difficult it is to you can feel like you're intraceptively, feel like you're running really bad one day, but then your time is actually quicker than what you expect another day. You can be really up for it and excited and feel buzzing and you get to the finish line and realize you've gone slower this picture is from someone who broke the world record, shipped a marathon in under 2 hours. And part of the tools in their toolbox was to have a laser to keep their speed constant throughout the marathon.

So ant any point, either in one instance or throughout the whole marathon, their time was constant.

15:29 So I guess my question is technology. If we're trying to design systems based on the idea of Ergodicity, are we reverse engineering that into our lives? Maybe. And where would that lead?

If you've seen the film Don't Look Up and it's all about prediction and modeling.

What will we be evolving into if we don't have the right systems that are truly matching biological what's actually happening with our biology? And yeah, that was there my reflections.

16:09 Jordan:

That's great.

Awesome.

16:13 Daniel:

Iain, thanks for bringing all of that. That's really insightful. So I think we have more than enough to just begin. So let's just start with whoever wants to reflect, please.

Jordan, first.

16:25 Jordan:

16:49 Ian:

Some.

16:49 Jordan:

Of the sort of social feedback that you get for maintaining allostasis you Beren bringing up the example of email and the sort of interceptive response that you can get from anticipating stress, from email, from communication, these sorts of things. And you're talking about how there is how external references and you were given the examples of technology and a laser to keep pace on a marathon can help, can basically act as an external you can use external reference signals, right? And I think one way to think about social influence or some of the social forces on intercepted experience is also as like external reference signals, rhytraids at least as external factors.

You can think about the example of the email that you were giving is it's an interesting case, right? Because you basically have in some ways you're kind of opening yourself up to this portal of potential interceptive disruption that can active at any moment.

17:58 And that's not going to be, it's not going to have some of the usual contingencies that would allow you to predict it like you would in other cases. Like if you're going to a meeting, you're going to go meet with your boss at 04:00, you know, that none of the sort of social signals from that. That could potentially be something you have to react to, something that you have to adapt and terrace ant the state to something that's going to cause you to have to leverage or basically mobilize your body to respond to that situation.

Those aren't going to happen till the 04:00 when you go to that meeting. If you're open to email, you're basically going to be able to be prompted within any sort of work hours. So you need to be prepared for that potential mobilization at any point, right? If your boss is like a real you know, if your boss is really awful, then maybe you're going to get emails in the middle of the night. And if that's the case, then you need to be prepared for some sort of some sort of allostasis mobilization at literally any point of the day, which is going to bring with itself some sort of consequences of needing to have this system in a state of preparedness because disruptions could come at any point.

19:14 Right? And so I think if one of the principles that's and Eli's paper here, right, is that we're defining putting together an allostasis response as keeping variables at multiple levels of this control system in a state where they can be maximally responsive to the sorts of threats that could occur, then that's going to look very different. If you're constantly in a state where you need to be prepared for a lot of different disruptions that could come in from social sources versus if you're in a state where you can rule some of those things out, you know it's the weekend and you know your boss or colleagues aren't going to call you. And so you can not have to have some of these variables in a state of preparedness to immediately react to those sorts of things, right? But that made me immediately think of and I think I could go on and on because I have some other work that's on social blanket states or social influence and how we can impact people to that.

20:38 Ian:

Thank you.

20:46 Jordan:

Eli ant to go for it.

I think you're muted sorry.

20:55 Eli:

I found really interesting the thing with the laser actually and I'm sort of wondering how those metabolic trade offs are taking place in the brain of a runner because normally the evidence shows that people will adjust their gain or their running speed to sort of optimize their allostasis challenge and therefore their energy efficiency. And here it looks as though the point of the laser is that you keep the actual speed constant, which means you're letting the level of allostasis challenge of the interceptive sensations vary a lot or at least a lot more in order to keep the actual speed constant. And I'm wondering how this can happen in the brain like that. You construct this generative sensory variable that you control instead of the interceptive sensations and how motivation can be grounded in interception to spend this extended time undergoing interceptive challenge.

22:08 Jordan:

Could it also be, too, that you're because part of this, right, is that we talk about and this was Bijan you were talking a bit about with interceptive feedback of the social therapies that you can do with this. That you can try to train people to have some more interceptive awareness on the sensory end of it than they typically attune people to having some interceptive awareness and then eli. Do you think with the laser maybe are you giving people you're giving people something that might be a more high fidelity like sensory signal. Like if they're going to try to keep this laser at sort of center of eye fixation, they need to move at a certain speed. And there's other variables that can follow from something that's more easily tracked in the external environment, whereas it might be more difficult to keep on.

23:14 Ian:

Tight, tight.

23:14 Jordan:

Like sensory control over some of the interceptive signals. You can structure that for people. So it's a little bit easier maybe.

23:25 Ian:

Sorry. I was just thinking that the laser is teaching them to ignore their interceptive signals, actually to place more emphasis on a constant speed required to win than it is on. My legs are feeling a bit heavy,

23:59 Dean:

Can I just ask a question? Because I know I always take it from the real novice here and I think sometimes that can add something to this. What if the laser is as an off loading so the top down, bottom up, that back and forth that you guys with your paper really clearly said there's two directions here in this interception. What if the offloading interrupts that back and forth and simply because you're offloading it now you agent creating that it's not external, it's added not even as a move to that center point on the Sigmoid curve. It's simply acting as a proxy and approximating for you that's taking less energy for yourself.

25:07 Now, you can consume the calories in running or you can consume the calories in trying to keep things within a range. And if you're not burning up calories to try to keep things within a Lagrange, you can now apply those calories to the running.

25:26 Daniel:

If I could give a thought on just that. There's so much to add to. I'm thinking of where else are there lasers in tasks like running? And it makes me think about the task as the offloading that principle of a small task expanding to the amount of time that you have that's more in the cognitive domain. Like if you have 5 minutes to write the email, you have 5 minutes.

If you have an hour, you have an hour. And then similarly with moving a pile of dirt or doing some physical task when the only thing that's being considered is the decision to do it, somebody might surprise himself with backpacking or undertaking allostasis challenge under the task structure of something that's external. So like the laser, it's already set versus without that desire or capacity to undertake that allostatic challenge, it doesn't present itself as in affordance at all.

26:41 And then also really interesting was the note about Iain you added about how some days you feel very good, but your speed or amount lifted might be lower and vice versa. So in the models as presented, does the entity have a true interception? So what is that difference with the experience and performance and valence of a given allostasis load?

27:27 Jordan:

Well, I'm not sure if I can answer that question, but I think the one thing that's going to happen if you're going to continue to run for a long time right. Is that there's going to be certain there's going to be certain motor signals you're going to have to give, and there's going to be certain sensory feedback that are going to come from that. Partly in terraceptive information. And the problem is that if you're wearing yourself out over the course of a marathon, those are going to be moving targets, right? There's not going to be some consistent amount of force that you're going to need to apply.

And as your muscle weakens, as you're running for longer and longer, the amount of force is potentially going to have to change. So it's going to become difficult to keep even a consistent speed, right? You're going to have to actually vary the amount of force and the actual motor commands they're going to have to be given.

And if you don't get if a lot of the feedback that you're getting from that isn't especially precise, right,

28:41 And so what the laser is doing, right, is it's basically giving you some sort of constant that you can regulate in lieu of having to perform the calculations to regulate a lot of other stuff that's changing in your body over the entire period of it, right? And I'm thinking about it in terms of you do a similar thing with, like, a metronome or something like that as well, right, where if you're trying to coordinate a lot of different people to perform musical notes in time, you'd want to have a conductor. You'd want to have there's a real use in having external reference points for managing those things, because literally everything in your body is changing as you're performing this stuff, and commands need to be given to regulate in the face of all of that change. Eli's pointing I think Eli's got a point.

29:35 Eli:

Yes. I mean, I was just going to say, like, we know that as you move, a bunch of your sensory and interceptive signals change, so they're basically never actually constant in the first place. If there's something you want to hold constant, then yeah, you need something like laser that effectively gives you an artificial source of constancy outside the body because you don't have one internally.

30:04 Ian:

Yes. And what's also occurring to me as you're saying that is as well as the internal conditions changing, the external conditions are changing and maybe getting windier at various points of the course. And there may be Daniel, you talked about when we spoke a while ago about ants, when it appropriate for them to react to weather changes. And there may be we want American Runner to essentially ignore all the weather changes and just keep running at the desired speed.

The last slide I put there was a bit of a distraction, really.

30:47 Jordan:

I don't think it's a distraction at all, though, because I think that the no, I think it's super, super useful because Parr of, again, this whole idea of multiple variables in the body changing all at once, that's kind of core of what we mean when we're saying, allostasis right, we're saying that there aren't any particular constants that, are there? There's a lot of variables that are moving and changing. And what Eli is making the point in this paper is that in lieu of set points, in a lot of those cases, what you want is some variables to try to occupy a zone of maximal flexibility to changing circumstances.

But at some point, there might be some variables deep, deep down in terms like very, very central to regulating the body that are going to need to be kept at some close to homeostatic level. And so one of the things that was coming up for me and working with the Brain Energy Metabolism Conference is that variables like blood oxygenation might be one of those, right?

31:52 Those are very tightly regulated. If that strays outside of some very narrow parameters, you're going to have really serious problems. But if you think about your runner running the marathon, that blood oxygenation level is going to be fluctuating, it's going to be challenged, there's going to have to be responses or other compromises made in the body to maintain that.

And if that's one variable that's being kept at a tight, that's being tightly regulated at the core of interceptive information. Other compromises that are going to happen to regulate that down the line

32:57 So you can think of it as the entire control hierarchy that Eli is describing.

In this paper, we have some very closely regulated and terraced its values far to the left, we have a deep net of predictions and prediction error throughout the entire cortex that's performing some regulation across the entire network. And then we have exter generative information at the other end of it. And what you're doing with the lasers, you're basically giving the organism the goal of fixing some of those values at the exterceptive layer to give some more structure as they move throughout this entire deep, deep network and all the space between it. Right?

33:43 Ian:

Yes.

And what I'm thinking also there what the marathon runner did before that marathon. So the marathon was made predictable. His breaking that record was made easier for him by the laser. But also maybe he influenced his blood, his blood oxygenation, the upper and lower limits of the acceptable settling range by doing altitude training to stimulate more red blood cells. He might have done hyperbaric therapy to all those things, which will make it easier for him just to follow that later.

34:26 Jordan:

Right. And I guess in Eli's framework, right, that's not necessarily changing the settling point of blood oxygenation, but what it is doing is at variables that are just slightly levels down from that. Eli, would this be right to say you're basically widening out that sigmoid function so that there's more adaptability from that additional training for increasing red blood cells, that sort of thing? Is that right?

34:52 Eli:

Yeah, definitely.

I'd also sort of add that some physiological variables are very tightly regulated. But one of the open questions is sort of Hohwy many removes are they from a disturbance? So like blood oxygenation or the PH in the brain that you mentioned, what does it actually take to disturb those?

35:24 Jordan:

Right.

35:25 Eli:

Like what oxygenation you can probably disturb by just having greater or lesser uptake of oxygen from the blood brain PH. I honestly, I'd imagine that you have to disturb a lot of things, sort of disturb your way through the outer control system, like the outer several layers of control systems before you can actually perturb that.

But you can think about things like the fact that you have a blood brain barrier in the first place is one thing that might help keep that sort of thing tightly regulated.

35:59 Eli:

Right, exactly that's what I mean is that living systems tend to be sort of homeostatic or allostatic at every level.

Like a cell maintains its own internal homeostasis in some sense, or allostasis by interchange with its environment. Then an organ system may also have such as the brain may have the blood brain barrier and sort of other levels of protection that insulated from its environment.

36:30 Jordan:

Right.

36:32 Eli:

Because it has to be in cooperation with other organ systems.

36:36 Jordan:

For sure.

And I guess the thing that I'm saying is just that for some of those parameters that do need to be really tightly regulated like that right. You might see some naturally developing biological structures like the blood brain. Barrier that are there to help keep those values tightly regulated as opposed to having it be more under behavioral control in which case there's some flexibility, there's some allostat flexibility in those. Right. What you want is if there's something that really, really has to be kept at a certain level, you would ideally have some of the evolved biology work to fix some of those parameters in the physiology itself.

Maybe. What do you think?

37:31 Eli:

I'm sorry, actually, can I just take my dog out for 5 minutes? Sorry. She's really begging me quite a lot and the thing is getting to me.

37:46 Jordan:

I was thinking earlier oh, sorry.

37:47 Daniel:

No, go ahead, go ahead, go ahead, Jordan.

37:50 Jordan:

I was just going to joke about it. I want to go find a cucumber and try that out of my cat too.

37:55 Daniel:

There are no snakes in Ireland. Seriously, I've tried it with our cat.

Not all cats.

38:06 Jordan:

Well, and our cats lived in Doris for her entire life except for the first six weeks or so, which is probably blind for half of that. So I should try it out on her too and see if there was some learning component to it or if she has it in me. Sorry, Dean.

38:23 Daniel:

Go ahead, Dean.

38:25 Dean:

I just wanted to kind of throw this in here. And I don't know, I'm feeling kind of back as Eli's walking his dog, but I'm sure he'll pick up the threat here in Hae. Parr one, I brought up this idea, and I'm not sure how often it's not ubiquitous yet, but I think that the focus in this paper is about perspective swaps. So what do I mean by that? I wanted to do a quick lap around that periodically and then see what you guys think about this.

So uploading to a laser as a perspective in the dot zero, Daniel saying staying within the connection space as talking about CDF to PDF as being another type of perspective. Taker the idea of bringing psychologists and their perspectives and engineers and their perspectives together in an institute or a lab setting as a different type of that different perspectives colliding or at least paralleling DAGs Dodgeball opposing teams each having a different perspective because they're wearing a different color.

39:41 One of the things we talk about a lot, active inference lab is instrumentalism and in action. Or the idea of sort of the embodied space versus the theoretical, the math perspective and the territory perspective and in this paper's case, the specific feedback control focus as a perspective. Right. What I'd like to do is take that idea that there's all these perspectives that one can be swapped in and swapped it within the idea of regulation within ranges. Yes, but I'd like to talk a little bit about what Iain brought up, which is I think is a really critical point and maybe quite complexity, not corollary but complexity to what the paper was talking about.

You said if we do something in a safe space now to me, I'm going to ask you this to me safe sometimes means controlled meaning the agents set the condition or at least they perceive they have some control over that cognition.

40:46 Jordan:

Okay?

40:47 Dean:

So that's a perspective that's sometimes perceived as our got it because it's predictable. Right. Then we have a sense of how do we strategize from that set condition one, that's variability reduced to one that's condition set or variability retained.

42:08 Jordan:

Right?

42:09 Dean:

So the bringing of the two together to me I want to kind of be clear what I mean by perspective swap. I don't think it contradicts what you've written in the paper. I think the move from CDF to PDF is a perfect example of that perspective swap and I'm not sure it's just a derivative because as I said in the last Livestream you bring psychologists and engineers into the same space and one doesn't get to rule over the other. You need both to create that swapping condition.

42:43 Jordan:

Right?

Right. So.

42:49 Dean:

Is that essentially what specific feedback control helps us get a better sense of not just a grip or an optimality but sort of a clear separation so that we can do the oscillating so that we can do the swapping and so that when we're having these kinds of interactions we're not doing a transdisciplinary thing here. We're really trying to get our heads around why did the laser work?

43:17 Jordan:

Right?

43:20 Dean:

Because we can prospective swap that we might get closer to something satisfactory.

43:26 Jordan:

So I'm trying to understand so when you're talking about a perception swap I don't know if I'm going to answer your question satisfaction that we might have to wait for you but I'm going to try my best here.

43:42 Dean:

That's all I want cue I try my best to nobody's gain to be perfect.

43:46 Jordan:

If I answered your question right now, let's pretend that I answered your question in a way that precisely got to the core of it and just stopped the conversation and you just said, oh yeah, I got it. That answers it in a word, right. Then I might have perception swapped, spoke so closely to the way that you would frame this question and so perfectly understood the way that you'd asked it, right, that we don't actually explore the space around it in a way for other people to come in to understand anything of what's going on.

44:55 Eli:

Exactly.

44:57 Jordan:

If I actually didn't totally understand your question and I need to ask questions and we need to bounce this back and forth for like several minutes, then we might still come to a settling point and we might perform some gradient descent to come to an actual answer here.

But because it's going to take longer, it might end up bouncing around through different parts of the space of answers that we could look at and end up capturing other ways that other perspectives might be able to understand. It, right, so that they can catch some element of it that was predictable or that fit with some internal model that they'd already generated. And then to be able to follow along to the gradient descent to reach down to that point. Right. So I think that part of the advantage of having interdisciplinary conversations and we've done this a lot, especially in working with Eli and then working with the engineers at Northeastern, these psychology interdisciplinary collaborations is that there will be a really long and frustrating period where people just do not understand each other.

46:00 And you need to actually work through that, because that's a period where you can do some learning and you can actually get some understanding of other perspectives, other ways to build a model of the environment, other ways to sort of take a perspective on events that are actually happening. But there will be a temptation through the entire thing to cut your losses and leave it because it is frustrating and it is metabolically costly. I'd say, to do all of that information processing and to follow that process. And it's not always obvious when the gradient descent is going to end either, or when you do understand each other, or when everyone is sort of followed into the loop and are able to follow that down to make the environment predictable, to come to a shared understanding.

You might know when you're getting close, but until you get to that point, you might be in a really long and frustrating process of search prediction error, basically bouncing around through the environment, of trying to come up with some model that can predict it.

47:07 Right? Yeah. So I feel like that was a very metaway of trying to answer your question, but does that help? I think it gives it part of the use of interdisciplinary work right.

And how having these different perspectives are going to help us explore the space more fully. Because if we just had an internal language to each other and if we perfectly understood each other in the first place, then you don't actually end up exploring the space in that case because you descend to sort of

47:48 Dean:

You've basically described the capitulation to a reproductive or an active logical process. That's all you've done and I don't think there's anything to ask you about that. It's been around for over 100 years and I think it's having a renaissance.

So thank you.

48:15 Ian:

Yes, as you were talking there about this different disciplines coming together, it was reminding me of one of the Active Instruments Institute papers that were covered a few weeks ago on social communication as control, I think it was, and also reminded me of the difficulty of a newborn child and a parent. All the child can do is cry when it feels some sort of discomfort and then the parent has to try and figure out what that cry means. Does it mean it's hungry? Doesn't mean it's nappy, needs changing? Does it mean it's too hot or cold?

So there's a period of learning each other's language and learning what each other's cues are, regulating each other and controlling each other.

Arguably that's all we're doing all the time as socially, as adults, we just got a more bigger set of vocabulary and we can influence our environment more than the baby.

49:24 Jordan:

Well then we can tell each other what our expectations are too. Right? Like the baby is giving a really diffuse signal that there is some interceptive states disrupted and then the adult has to, like we were saying, right, explore around and bounce around until they can converge on that and get the baby satisfied. Satisfied that in a exafferent state.

Right?

So some of the other work that I've done is looking at how I really want to look at this paper then of social communication is controller because that's related to some other stuff that I've been doing too, but is that I think that you can think of social influence as basically people regulating uncertainty in a social environment by conforming action prediction that other agents have in it. So you can think of a social norm as a set of collective expectations that people might have in an environment.

50:27 And if you conform to those expectations and you can minimize prediction error for people and you can minimize the likelihood that their behavior is going to change, that your environment is going to become disrupted, more entropic, anything like that. And so the baby is basically creating entropy in their environment for the adults in the room to try to minimize by satisfying and terracetive needs for them as an adult. Once you can communicate, maybe get around some of those problems by saying you ask someone to pass the salt at Thanksgiving or pass the butter, you've made an expectation extremely clear and then people can satisfy that expectation and everything continues on predictably.

Right. They could also refuse and say, no, I'm not going to pass this on. But if you do that, you will move things onto a more unpredictable trajectory. Right. You're going to push things out of the sort of bounds that people are used to navigating and you're going to potentially move off into this space of having to explore each other's reactions like Dean was talking about, right?

51:41 Ian:

And what you're sort of saying now. It's reminded me of some of the work Greek researcher called Demetrius Zaled data. I think he's done a lot of work on ritual and how rituals basically he's put heart rate monitors on people and measured Jorge cell levels and so on over the weeks and days following rituals and showing that it's, you know, there's a lot of synchronization that occurs during rituals. So there's synchronization of physiology, but it's bound up in these kind of codes or rules about how our clan or our group or our society should operate.

So it's kind of my interpretation on that is it's training a person's physiology to align itself with social behaviors.

52:35 Jordan:

Wait. Was this Demetrius Bolus?

52:37 Ian:

Demetrius surname is spelled X-Y-G-A-L-A-T-A-S. He wrote a book recently called Ritual how Seemingly Senseless Ants Make Life Worth living.

He's done some study with measuring heart rate variability and stuff for firewalking kind of rituals and so on.

53:03 Jordan:

That's really cool.

53:05 Daniel:

Jordan, you did mention Demetrius Bolas and the work from 2020 through Others we Become Ourselves, the action prediction coding, active inference also hinging on a shared first name, but a very relevant paper as well. And then one thought to connect this idea of synchrony uncertainty controller novelty in communication and in rituals. That's when people are the laser for each other with their attention.

So then it's like, okay, we're going to do a role play where this is going to be the case. All synchrony this perspective you'll have, this perspective will just be like it will be just two stubborn characters having this argument. It'll be very funny and then that is a predictable play. It could even be scripted or at the very least you can have fun and so on.

54:09 So it's very interesting that that is reflected in the social space.

Whereas the marathoning and going for the record, which few people ant to do, most people can take a much more relaxed approach than the person trying to set the world record. But in the social space, as Dean brought up, there's a lot that we can bring to bear on the social space from variability reduced settings like laboratory studies on cognition, fMRI studies with social stimuli. But the social space is a variability retained area of application. Right. But we understand with the translation yes.

55:02 Jordan:

Right. So as long as you're adhering to some predictions that other agents would have in that environment, then you're going to stay in a variability reduced state. And you can say you can stay for lots of purposes sort of socially invisible to other agents.

56:03 You don't need to create new disruptions to an environment that you're going to need to be prepared to adapt to. Right.

56:13 Daniel:

Thank you, Dean.

56:16 Dean:

Sorry, I'm blowing my hand again. So the fascinating thing about the paper was I use a basic heuristic that says when in doubt and we're pretty much always in doubt. Zoom in, zoom out. And so when I look at the scale of what that would mean from the perspective of interception, those timescales are much tighter than if I zoom it out to the allostasis involved in running a marathon.

My zoom in, zoom out range and potential gain is much different for the allostasis than it is for the exteroception that's involved over that same course of time. And so that's where I found the specific feedback control, which implies that there must be a general feedback control as well. So, interesting, that's where Eli's part about the four different time segmentation possibilities allows for that zoom in, zoom out.

57:24 Am I contradicting what the point was that you were trying to make in the paper, Eli?

57:30 Eli:

I am slightly wondering where you got four specific scales.

57:35 Dean:

Well, you have the L four in.

57:37 Eli:

Terms of oh, yeah, well, that was for modeling purposes.

57:42 Dean:

No, I understand that, but I mean, you can still inflate that to yeah.

57:48 Eli:

But I think that's a pretty standard part of the hierarchical active inference literature, isn't it?

57:54 Dean:

Okay, but do you think the idea that, again, we can swap from the specific to the general is again, it just seems to be again and again, it's that ability to move within ranges, but the range doesn't necessarily remain consistent unless, of course, you're following a laser. But that goes back to my original question is because we offload the metabolic commitment that we would have to stay at that level of consistency, we can then turn those resources over to other aspects of that endeavor.

58:40 Daniel:

Let me try to ask a different way to jordan, I think would be how would different patterns in this type of multi time scale framing reflect different metabolic or energetic costs? Like does the brain use more oxygen, glucose, ketone bodies, micronutrients, who knows during what kind of activity, such that there is, what kind of a link between the physiological costs in gold versus cognitive angle.

59:25 Jordan:

I mean, I think the way to do it and this was I think I was thinking this thing you ask a dot two is that the trick is, right, is that if you're regulating some of the input to the intercept of input that you're trying to regulate, that might be really central to allostasis regulation, right? Could be from sensed interceptive variables like blood oxygenation, like blood glucose. But the trick is, right, is that and this is that I think more what I'm interested in, what I'm trying to develop, the thing about brain metabolism is that all of the steps and all of the communication that has to be done at some of these lower orders of this hierarchical scale isn't free.

It has metabolic costs itself, right? And so in the human brain, the actual resting state cost of the human brain when it's just when you're just sitting still in the MRI scanner is about 20% of your body's metabolic budget.

1:00:36 It fluctuates a little bit as you're doing sensory processing, as you're dealing with unpredictable information, the details of how it fluctuates, like those matter too, and we can get into those. There's relative changes in how much glucose you're consuming versus whether you're consuming the glucose with oxygen for like a more efficient yield of ATP energy. But the point is just that neuronal signaling itself is super expensive.

And if you're navigating an unpredictable environment, then you can expect to have some of those expenses kick up or have them change in ways that are going to have to be regulated. So what that means, right, is that even though there's a hierarchy of processing here where you're taking in sensory signals, you're passing them up a cortical hierarchical and you're compressing them. If you're doing that more and more and if you're in an environment where you have to be passing potentially more and more prediction error up this chain that can itself then be changing important and terraceive sense variables that might enter at different points of the hierarchy.

1:01:46 Because there's still sense information. But they might be more centrally regulated and they might have downstream effects if they start to go out of whack.

Right? So basically I think you brought up to that, you know, thinking about this from an allocatetic perspective instead of a computational perspective. And I think the computer metaphor that people

The brain ant ignore that because it is an actual biological system.

1:02:49 And its whole point is that it's going to have to keep that system working, navigate the environment and grab metabolic resources to keep the cycle going. And so all of this computation that you're doing yeah, isn't free. It adds up and then can potentially have downstream effects on sense metabolic variables that are critical.

Great.

1:03:15 Daniel:

Thank you, Bijan.

1:03:21 Ian:

Thank you. Yeah, I was just thinking then after what Jordan was saying about climate change, and if that's a prediction that's maybe two decades ago wasn't going to affect my life, but it might affect the lives of my children or my children's children to act now with that, that's a very abstract for most people. There's nothing in their environment that would give them that prediction of future threats in 5100 years time. So they have to create a very abstract sort of image of what the planet is going to be like. And then to all the huge energy expenditure that's required to switch to renewables, to organize society differently, that's going to require a massive allostasis load in the short term or interceptive sort of demand, chronic low level interceptive disturbance to create that shift through generations, right?

1:04:40 Jordan:

And so I think you see, right, like there is if what your brain is regulating is at the core of it, some of the interceptive parameters that are necessary to keep your body and your whole organism moving forward, right, then being thrown. Hinton a constant state of uncertainty is going to be Costa. If we think it's true that processing all of that uncertainty is going to have a metabolic cost attached to it, there's going to be some I think the way that your sort of brain as a regulator is going to work is probably going to want to return you to some relatively predictable state. The issue is that if you can model and understand externally, right? Like if you can understand that in a long the long term trajectory that you're on in terms of climate change is going to lead to disaster, right?

1:05:46 It can still be really difficult to divert from that because the trajectory is a predictable trajectory that you're on until it hits some of these critical exponential points where it's suddenly going to Brea, right? And so I think you can see that with climate change. I think you can see that with the pandemic. You can see a lot of cases where there's a temptation to return to some sort of trajectory where when things are going moment to moment, they're relatively predictable. They don't require a relatively large amount of attention.

And if you're going to enter into some uncertain change state, I think there's going to be a sort of

1:06:45 Eli:

So I would have to ask uncertainty about what?

1:06:49 Jordan:

Uncertainty about the immediate lived environment.

So what's going on around you? What are you doing? When I got up today, like I made coffee, I got on the computer, I have a predictable set of sensory signals that I'm going to be running into. I have daily routine. These things I don't mean.

1:07:13 Eli:

Because, let's see, so what was it? Climate change, pandemic. Most of these are not actually things that make your day to day life that unpredictable.

1:07:27 Jordan:

That's exactly what I'm saying. I'm saying that those long term events, those things that you might be worrying about, those things that we're talking about, being worried about, climate chance, they don't actually impact your day to day life right now very much.

And so changing your day to day life substantially now to deal with them is going to be difficult. That's all I'm saying.

1:07:51 Eli:

Well, not necessarily because the reference trajectory for actually dealing with them is not necessarily that unpredictable either. Different from what you're already doing doesn't mean unpredictable.

1:08:05 Jordan:

It's true.

But the period where you shift what you're doing to something different is and so I guess what I'm saying is that a change is something that requires a difference in trajectory from where something was already going.

1:08:24 Eli:

Yeah, but I think the thing about our trajectory based formulation of allostasis is that well, the whole point is that let's say you plan to go to the store, you're driving on the road, you make a right turn. Is the right turn unpredictable? No, it's not. It's a predicted baked in part of the reference trajectory.

Change does not have to be unpredictable. And I think we should avoid conflating those two.

1:09:04 Jordan:

Sure.

1:09:08 Dean:

Can I bring you back examples of things we talked about in the Dodge Zero? So Daniel brought up a really interesting point when he talked about glucose stacking and automatically sort of brought me to the idea of people who have diabetes and those that are, I think it's hypoglycemic, unawareness they're the most brittle diabetics. And essentially what that speaks to is they have a large blind spot to sort of the cumulative effects of what's going on because the pancreas isn't working correctly, doing that kind of regulation piece, that blind spot. And the severe consequences of that blind spot again, I don't want to beat this like a dead animal, but because you are blind to something implies that you cannot take up that perspective. And then the consequences of that are more severe when you absolutely don't know how your body is going to respond to that, Donut, or not.

1:10:16 Right. So again, we talked about it in the context of it. Jordan was really good in clarifying. We can't think of this in economic terms, but I think we can think of it in terms of blind spot terms. If we have a blind spot to this, how do we respond to it?

Hohwy do 7 billion people respond to it? Well, what they do is they revert back to the now that's what they do about their blind spot, right? Because they just don't want to take up the perspective slot because it's way too challenging.

1:10:53 Jordan:

They might also sense there might be you might think of it as right of this control hierarchy of that if you're missing an ability to sort of sense and regulate some parameters in the hierarchy, there might be downstream consequences of glucose use that can be sensed. But the problem is that it's going to mean that you don't have as tight control like you're saying you have a blind spot in that hierarchy that isn't as tightly regulated. And so it could potentially wander out of some of the bounds that are going to be adaptive or safe because you're performing some sort of second order control on it instead of controlling it more tightly with some of the sensors that you would normally use. Right? What do you think?

1:11:42 Daniel:

Ela if I could just give one quick response, actually, on this idea. The leverage point of the control system is the true control variable. So beyond being a good regulator, having a volume knob in your head, if there's a volume knob in the generative process, the ultimate control situation is to just have the actual control of the volume knob. And there's cases where that's possible and there's case where it's not, but where it is possible, it's the leverage point. And then, Jordan, you just pointed to if you're missing this ability to either sense X, like we can't directly perceive our glucagon circulating level or responsivity across different tissues.

It's just too multifaceted and subliminal of an interception, directly different hormone balances and so on. The technology and measurements are increasingly allowing that to be laser focused.

1:12:47 Without the ability to directly control those subliminal factors to either sense or act on them, we can only apply upstream or downstream control. So we could modify our niche or use signposting or stigma g so that our environment dissuades us or make something impossible like time boxing or just putting something away, or downstream consequences like having some kind of supplement that

And so actually being able to have a framework such as you're describing, where we can talk about the true physiological variable, the actual substance of the essential variable, but also recognize that we're only going to have interceptive access into potentially noisy or.

1:14:01 Variable proxies that are influenced by many things and they're going to be like sometimes multiple steps up or downstream, like lightheadedness in the context of glucose regulation. But that can happen for a lot of reasons. So it can't be simply the queue. So really interesting there Eli or anyone else.

1:14:27 Dean:

So.

1:14:30 Eli:

I think we have to differentiate between how could you build active coherence lab control system in general and how our nervous system is built in specific.

How our nervous system is built in specific is an empirical question. And I have pretty strong doubts that it's all just a matter of leverage for pretty much the same reason that I have my doubts about it's all about avoiding change.

Like there's just such wide variability of behavior in real life. There are people who embrace change, there are people who challenge themselves, there are people who give up some of their leverage or control over some things.

And if we don't look at those, if we sweep those Attial behavior instances under the rug of a sort of general principle that says well, everyone ought to be very controlling and conservative all the time, then I can't help but think it's a sort of scientific sin.

1:15:57 Jordan:

Dean and I were talking when you were out too about sorry about that by the way.

1:16:02 Eli:

Normally she's a bit more alistatically resilient but she might be ill.

1:16:08 Jordan:

She'S feeling better. But we were talking about because I think that maybe there's a misunderstanding because I don't think that we're saying that people only want to control or make their environment perfectly predictable. Right? I think part of what we were talking about right, we were talking about this idea of shifting perspectives or this idea of how do we are coming at it from the perspective of what a exploration between psychology and engineering really gets you in the first place even. Right?

And what we are talking about is that part of what it does if people have the goal of trying to understand each other at the end of it and reach some sort of mutual predictability so that they've developed some understanding that they can build a forward model from that. They can actually they have a model of the environment that incorporates some understanding from the other collaborator.

If you quickly just gravitate, you know, if I answer a question and the other person just like immediately understood what I meant by it. It might be because I answered it in a way that just happened to nail it for that one person, but no one else in the audience is going to be able to understand it. No one else is listening and is going to be able to understand it. And so by having some sort of imperfect process of gravitating towards making things predictable for each other, we actually active some more exploration and we sort of get a better sense of the space that we're actually moving through.

1:18:25 And we might generate a better model than we would if we just immediately converge.

Right.

1:18:32 Eli:

Yeah, of course.

1:18:36 Jordan:

Yes. I'm sorry. No, go ahead.

1:18:39 Daniel:

You raised the difference between these two questions how is the nervous system built in specific or in particulars? And how can you build or what is an active inference model in general?

So maybe return to the top question.

1:18:55 Eli:

Sure, yeah.

I think this is one of those things that can get a little conflated when we have these collaborations with psychologists and engineers where, from the engineering side, if you're building something for, so to speak, the other acronym that you can form out of active inference AI instead of Active, then you don't ant something that works like a human nervous system necessarily. Well, you may want it to share a few properties, but actually you're building it to solve some sort of task or to exhibit some sort of relatively well specified behavior routine. And therefore it's going to be, in most respects, very completely different from a human being. And that's actually not just because you're trying to avoid what is it?

1:19:55 Rossam's universal robots.

Right. Where, of course, those were actually made of flesh and blood. Like, it's not because you don't want your computer to grow feelings and decide to go on strike. It's because ant priori there's no reason to build a machine that works like a person in the first place. Maybe it would decide to go on strike, but the space of things that you can build is just so much larger that what you would usually do as an

And that also implies a sort of converse proposition, which is that the human nervous system is a pretty specific point in a space of things that could have evolved or even in the space of things that did evolve. Human being versus what is it?

1:20:57 It's not a sponge. It's that sea organism mentioned in one of those Friston papers that, you know, when it goes through a certain life transition, it latches itself down onto a rock and goes through a whole stage of metamorphosis where it eats its nervous system.

1:21:15 Jordan:

Yeah.

1:21:15 Eli:

Sea squirt. Thank you, Anne Bijan. Those both evolved. There is some space of possibilities that includes both the C squared and the human being. This implies that it's a pretty broad space of possibilities.

And if we're using active coherence to model them both, this implies a very, very large space of possible active inference models, formalisms controllers.

1:21:50 Ian:

So, Eli, if I heard you correctly there, you're sort of saying that artificial intelligence or tools that humans make that may or may not be modeled using active inference, there's usually an outcome or a goal that's quite clear why we build them. So it might be, I don't know, I want to build a coffee maker to make me coffee, and I might use some very intelligent methods to build that coffee machine, but the outcome is clear. It seems to me that with the nervous system, we're still not clear on what the outcome is. So if the FEP is right, then it's just to minimize free energy, minimize surprise. But am I right?

You're sort of questioning whether that is the cup of coffee we're after at the end.

1:22:55 Jordan:

Yeah.

1:22:56 Eli:

And so we always have to sort of remember that dog walker just got here. We always sort of have to remember that surprise means under a certain generative models. And so the models that are present in free energy can involve sort of epistemic value, like what's it called varishimilitude to the sensory world, accurate modeling. They can also involve a reference trajectory.

And so they can also they can involve both perception and action. And that's a really broad space of things.

1:23:39 Ian:

Why are they doing that?

1:23:40 Eli:

Chang Kim means minimize. It means optimize this information theoretic functional, whose meaning is actually pretty strictly mathematical.

1:23:57 Ian:

And is the outcome always to be auto poetic? So to make another nervous system?

1:24:06 Eli:

I mean, is it?

1:24:08 Ian:

I don't know. That's why I'm wondering what I would.

1:24:13 Eli:

Think it usually is. If you're making a coffee maker, it probably isn't like coffee makers. Sometimes you have to disassemble them slightly to replace the parts or to clean them. And so you don't necessarily want it to be self organizing in the sense of trying to make another carafe when you take the carafe away to wash it.

1:24:39 Jordan:

But I think that if Ian's asking about other places, he's asking about is this something?

So you're making a distinction between a living and a non living system or between a living system and a tool that you've made to give it a certain input and give a certain output back. Right. So maybe just to repeat this question and say for a living system, then, do you think that some of the fundamental controlled variables here are autopilotic?

1:25:11 Eli:

And there I think I have to say I don't know because I am not a biological and I haven't seen the full range of weird stuff that other organisms do. And I ant to be very, very cautious about the idea that we can sort of introspect gather what we think are a free energy principle of human behavior. And as introspections go, they may be pretty good ones, and they may generalize pretty broadly and then expand that to the entire rest of the kingdom of living organisms like the entire rest of the tree of life. So just as an easy counter example, there are insects that die when they mate. This is an ordinary baked in part of their life cycle and if you want to talk about that as autopayesis then I think we have to autopoesis then we have to ask what is being self organized?

1:26:16 The parent or the child? Because the parent empirically is Heins disorganized.

1:26:26 Jordan:

That's fair. Sorry. Not Dean first. Dean.

1:26:33 Dean:

I'm just as happy listen, but I'll just throw this in here because I don't know if Eli would describe it this

I've always said that if we're talking about living math now don't make me define that we're talking about living math. Math that's alive that's much to me more easily described as a leap of faith embedded within a step function rather than being provided the functional requirements as a case use and then building the algos to carry that through. That's a very clear difference between the two things. One is a bridge and the other is we all get in a bus, build a ramp and then fly over the divide and then if we're really good and we land it, we go back the other way and go wee because we're still allostatically and homeostatically existing. But to your point, I think we have to be clear that those two things are quite different.

1:27:35 One is active and the other is not and both require math but not.

1:27:41 Eli:

The same math and Beren among I would actually caution even among living systems. Living involves metamorphosis, it involves death at a certain point, it involves reproduction, it doesn't just involve individual survival. That is not how an ecosystem works.

1:28:08 Jordan:

No, for sure.

And I think what I was just going to add was that I think from an autopilotic perspective I don't think anyone would disagree with that. I think that what someone would say is that you need to think about from a perspective of reproducing the relationships that create an organism. Introduction in that process could be a process of recreating the organism or recreating the structures that create that organism when there's components of it that couldn't be repaired without reconstructing the entire thing, basically. Right? So you'll have death.

Any one of these systems are going to have components of it that ant be repaired. If parts of it can't be repaired, then a way of basically ensuring that that system continues to exist in the relationships that compose it is to reproduce and create a new system that has those relationships, but has the parts that are going to terminally fall into disrepair over a certain period of time.

1:29:19 Start fresh so it can begin that cycle again. Right?

1:29:23 Eli:

Yeah, absolutely.

That's actually an empirical claim about the evolution of aging which is that aging came first at, say, the single cell level and then reproduction follows to cope with that. And I don't know enough about the history of life to know whether that's true or not.

1:29:48 Daniel:

If I could connect this very interesting theme to dean's Bridges and ramps which are two different engineering projects and have two different sets of structures to modify the niche with. And also Ian's original point about the epigenome and the exposome and taking ecological, developmental and evolution perspectives on human health. So the process of epigenetic canalization and the way in which epigenetic variability can become entrenched through genomic changes like one protein that has a bi

1:31:14 So the Bridges are on the continuum towards modifying the environment, modifying the anatomy to embody the constraints of the environment like the buoyancy of a fish. Something where the anatomy even without going into the morphological computation angle just the scale of the femur is such that it ends up being able to do plausible actions which gets you in the ballpark by being that kind of thing.

And then behavior takes us closer and closer to that person jumping off the plane that Iain showed whether it's like one footstep which is many times a challenge for all kinds of various reasons I mean, it could be really anything. And that's kind of the challenge of movement to the social risk settings and people having different profiles or envelopes of their risk in different areas of being alone and being with other people all these different settings.

1:32:36 But those are more ramp like because in the end, especially when it's socially extended, you can't have the actual bodily you can't embody the content of social variability but your physical body can embody the content of being regularized with the abiotic niche. But the brain can only be prepared in a way that is different from the body. Hope that kind of brought it back to that epigenetics angle because behavior is even more EPI than epigenetics and so allostasis are changes that are faster than it. So it makes sense to put it within a broader evolutionary perspective on how our errors got honed in to even this modality.

1:33:30 Eli:

Yeah.

1:33:38 Daniel:

Well, last 25 minutes or so, where do we go from two?

Either the researchers or Iain?

1:33:51 Ian:

Wherever you feel the point you made, Daniel, about evolutionary I didn't attention evolutionary biology specifically at the beginning but.

1:34:03 Daniel:

For.

1:34:03 Ian:

Me that seems like maybe a blind spot here.

I'm thinking also about Markov blanket and if gut microbiome influencing my neurotransmitters that I produce, and do I include my gut microbiome within my Markov blanket? And if so, what am I feeding my gut microbiome? Do I include the food that I'm selecting within that Markov blanket? And if so, do I include the field that the food is growing in because that will affect the food? And if so, do I include

1:35:08 So it's more of a kind of communion of subjects rather than bound objects, but we have to start somewhere.

1:35:30 Eli:

So as a bit of a jumping off from that, I think with all active inference work, there's always this incredibly important question, which is we can use the framework across so many different scales. I just had Maxwell Ramstead tell me that they derived a theorem that literally every physical system has a Markov blanket. And then I asked him, well, how do you pick out the ones that Beren interested in studying? And basically he said, well, there isn't necessarily a theorem directing you to the most interesting or metric that tells you which ones are interesting. So that's still in the realm of just an investigator's choice.

And I think there we really have to figure out how to ask when do we think we're going to get something interesting out of applying this framework to a given object of study or to a specific object of study?

1:36:35 And when do we think we'll be doing something sort of like rederiving evolution where it's useful to do as a formal exercise? But to my knowledge, we haven't learned anything new about evolution from the free energy principle or active inference that we didn't know before, mainly because people had already described evolution in terms of inference prior to describing it in terms active inference. Lab.

1:37:11 Jordan:

I think another thing that's useful to think about, and I've been thinking about this a lot lately, is in terms of what are some of the metaphors that we're using to scaffold the scientific questions that we're asking. Because I think one of the things that one of the things that's a big strength of this paper of Eli's, right, is that the title itself is actually a sequence of two metaphors, which is interceptionist modeling allostasis as control. So I think there's a sense that if we have particular question, if we set ourselves up to think, what is the sort of framework that we're using for thinking about the questions that are interesting or not, as Eli is saying, what are the systems that are interesting? What sort of metaphor is a Markov blanket? What sort of metaphor is active inference?

What are the sort of things that these are directing us to look at? And does thinking of control in the way that this paper has been doing direct us in a different direction, to think about things in a slightly different way, maybe.

1:38:21 Dean:

Can I take on that right away? Can I just get your response to this, Jordan? So is the metaphor consistently is one of the elements baked into the metaphor noncontinuity meaning whether we build a bridge over it or whether we all leap across the creek hand in hand and then the second time we do it, we all go, we because we did it twice. And now we have some conversation that we can do. It is the consistency within the metaphor, the non continuity?

I know we perceive it sometimes as being continuous and progressive, but are we talking whether we're

1:39:23 Because that space that Eli spoke to, that possibilities thing that really matters in terms of staying alive, right?

It's not when you get out of the particulars max Ramstead says there is no rule for that yet. That's what you have to self organize. So what do you think?

1:39:46 Jordan:

I don't know. I don't know how to answer that.

I'm trying to familiarize Jordan.

1:39:55 Eli:

I think you should prep what you're saying for a moment and I'll give an answer to that for sure.

1:40:01 Jordan:

Or you just take over.

1:40:04 Eli:

So I think the thing is that at least in our lab, we are a physiologically focused affective science lab. And so we sort of come to active inference with a set of systems of interest and a set of phenomena of interest in mind already.

And that doesn't necessarily help other people pick out what they want, but it does indicate that you can bring what you want to. I think active coherence ends up being a bit of a potluck field at a certain point.

1:40:41 Jordan:

That's a good answer.

1:40:42 Dean:

Yeah.

1:40:44 Daniel:

One thought on that is the structure of a lab with a system or a question in mind is an epistemic framework that allows the investigators to actually take on bold new theoretical choices and explore different frameworks that are investigating a specified system of interest. Like we're studying blood pressure regulation in the context of professional Dodgeball players or interceptive awareness in intramural Dodgeball players when there's already a project or a need specified in potentially even a variability retained setting, then the lab exists to funnel that into different kinds of analyses and scenarios that help address that system.

1:41:45 Like all of the lab studying different human diseases and sometimes and with challenges and successes making their work in the lab connect back to the real world and being able to take on new theoretical perspectives, some which might not initially appear to be helpful until years of basic

So yeah, that's very interesting. What maxwell added, and I think speaks a lot to many of the notions that we've been discussing, like pushing not having two realms in the metabasian with a highly rule based and then leaving the outer level with where there is no strategy. We just accept the prior without having metacognition on that level because that's just the limits of how far the model was extended out.

1:42:49 Eli:

Yeah.

1:42:55 Daniel:

Do either of you authors want to add anything about dodgeball?

1:43:01 Eli:

Oh, yes, I was going to tell I was going to tell everyone why it was dodgeball. So essentially in basketball you have to shoot to the hoop. So you throw, the ball goes, it either goes into the hoop or it misses. If you're passing, the person either catches or you missed.

In dodgeball the Bull is coming at you. And so the idea here is that you're picturing yourself trying to dodge. And this lets us sort of merge the intuitions about predictive processing and control where the reference signal is to avoid contact with the ball. So therefore the stimulus becomes both a prediction error and an actual control error.

1:43:57 Jordan:

So in life you're always playing dodgeball with something?

1:44:04 Eli:

I Dean if you walk out into the middle of a traffic, yes, there's always some obscure possibility of being hit by a rock out of nowhere, but hopefully most of the time in life you're not actually playing dodgeball with something.

1:44:23 Jordan:

Well, there's always something that can disrupt you, right? Yeah, there's always you have a system that can be disrupted in many ways. I'm just picking on it because I think, again, it's about metaphors, right. And I think when you're talking about basketball, you're talking about having a goal, you're talking about having some sort of externally defined goal that you're trying to perform actions to satisfy and then you tally up the score in some way of it.

Right. Versus in dodgeball you can get hit and you're out. Then the same thing is true of your biological systems can get disrupted and you're out. You're Dean, right?

1:45:07 Eli:

Yeah.

But I guess my intuition is that in dodgeball the ball is coming for you in a way that most of the time it isn't physiologically.

1:45:17 Jordan:

No, that's true metaphors agent perfect. But I'm just saying that you have.

1:45:21 Eli:

Physiology is not adversarial.

1:45:23 Jordan:

No, sorry, go ahead.

1:45:28 Daniel:

Just remind me of each sport provides kind of a different metaphor. None of them total or of course exact, but there's games where you're avoiding the ball. There's games where you have to hit an inanimate object and then it bounces off like ball ball. There's games with implements without implements. There's marathoning, there's sprinting, there's throwing things.

Then there's just one, 2311, all numbers of different players on ice, as Dean knows. And each of these settings have their interceptive challenges and social included in that model.

1:46:12 Dean:

Dean yeah, I was just going to say the metaphor. You can have a lattice of rope that makes you a bridge, and you can have a lattice of rope that makes you a fishing net. One captures, one allows you to cross, one is in between, one is enveloping.

And I think that's why we use metaphors. But the point that I would make is that when you mesh something, you still have those gaps. And I think it's important to see the non continuity in this. I think that's where the math, the theoretical, the ability to bring it down to that level, if it's not only one, if it's not perceived as only being one math, if there are maths involved, I think you create the conditions around which better understanding can move forward. Now, to Jordan's point, it takes longer if you don't have the proper gauge of mesh to catch the smaller fish.

1:47:14 And that's, I think, what Maxwell was speaking to. It's up to you to decide whether you're catching guppies or tuna.

There's your metaphor for the adaptive one.

1:47:33 Daniel:

Short thought is a zero to one, which is a boundary we can talk about in the future, is when the entire or large subsets of the active inference ontology and frankly, just the use of statistical modeling. These kinds of transformations are not 2022 synesh at all inventions with respect to control processes. Once one undertakes the statistics toolkit, they enable new visibilities into what was already latent. Every time somebody had shown something in terms of a CDF, they didn't always show this.

But this is also taking logs of variables and interchanging CDF and PDF. Some of these atomic units already exist, and this paper does. And incredible job of putting the setting of interception and the function of allostasis into the intersecting legacies of control theory and cybernetic approaches, as well as more recent developing threads, many of which don't have a formal basis initially, like ecological

1:49:01 And so bringing those two areas together is kind of that psychologist engineer conversation that was brought up. And that's like the dodgeball game.

Now, if they hit each other, do they knock each other out or are they sending each other? And as we explore initially, it's not clear. And in that uncertainty in the beginning of the exchange, it's not like the dodge balls are particles. They're more like waves.

What will Jordan and Eli your post paper directions be? Or how long are you going to be continuing? Or what distinctions here?

1:49:48 Eli:

Jordan, I think you should tell them about our lab meeting next week.

1:49:52 Jordan:

Oh, yeah, we're covering.

So I think one of the things is we've talked about controlling variables here. We were interested in, or I'm interested at least in thinking about other control perspectives. There's a perspective perceptual control theory to think about whether basically the behavior is a means of controlling inputs or controlling sensory inputs to a system. But more specifically, I'm interested in thinking about Hohwy. We can apply control systems thinking to neuroscience more generally.

So I think people are very used to taking an fMRI image, for example, bold imaging, and then treating it as an input output system where they deliver some sort of stimuli to the brain, they'll observe some output, which will be a bold response in some region.

1:50:57 And then they'll interpret that as causal, that they deliver stimuli, they see an effect in the brain and they've identified some cause effect relationship. And the problem is that people have been doing that for 2030 years now. You have a million different strands of these supposed relationships and you don't have a whole lot to structure them. And a different way to think about it is that the brain is the negative feedback controlled system that's trying to regulate some homeostatic variables within it, or allostatic when we consider them in the context that we're doing.

So if we deliver some sort of stimulation to the brain, we're basically perturbing sensory input to it and then we're seeing some perceptual response or we're seeing some restabilization within the brain to bring it back to homeostasis within a region. And we're not really getting a causal relationships, we're looking at control systems that are being perturbed. So that's coming off of a chapter that was by Henry Yin called The Crisis in Neuroscience, which there's also a really great brain inspired podcast episode about that too, which is worth checking out.

1:52:11 You have some Dean too to follow up to think about control and affect, right?

1:52:18 Eli:

Yeah. So to start with that, I would sort of make a small amendment to the notion of a negative feedback control system. Jordan, can you Dutch the podcast link?

1:52:33 Jordan:

Yeah.

1:52:34 Ian:

Sorry.

1:52:36 Eli:

I've got it. And say maybe we should be thinking about nervous systems as mixed feedback control systems. So sometimes you need to stabilize a state of sensitivity to the environment rather than resilience against the environment. And that would involve positive feedback.

And that's sort of where I get into thinking about affect, is that if you say that there's sort of these two modes of control, positive feedback, stabilized control for states that are very sensitive to the environment and then negative feedback, purely negative feedback, really, it's positive feedback in the service of negative feedback over the long run. And then purely generative feedback states that are trying to be insensitive to the environment and you have failure and success for either of them. And all of a sudden it sort of starts to look and you can structure the feedback loops in different ways.

1:53:40 It starts to look more like some of the core properties of assets that jump out in our data. And sorry, that's a very hand wavy explanation.

And it's because we really don't have I don't have this in the form of more than a few notes on my iPad.

1:54:00 Jordan:

But there is should I link the other brain inspired episode that got the dollar?

1:54:04 Eli:

Yes, that one's good enough that I included a quote from it. I. Think in my slides from here that we had the Rudolph Sapolka quote.

Yes. Control is to engineering what philosophy is to the humanities.

1:54:29 Daniel:

Wow. Very interesting directions. Iain and Dean, what are your next research and education directions?

1:54:44 Ian:

I'll go first. I'm going to listen to the podcasts is my next steps, and I've just really enjoyed this conversation. And what I think you're all trying to achieve is amazing stuff. And whether studying humans is going to help us make better AI and robotics, or whether attempting to make better engineer better machines is going to help us understand humans, or whether we're going to, as you said, Jordan, banks off each other and improve our understanding both ways. I think it's a good thing.

Over to Dean.

1:55:30 Dean:

Thanks, Iain. Thank you, Bijan. Thank you, Eli. Thank you, Jordan.

Always. Thank you, Daniel.

I think the last two, and I want to thank Dave Douglas, although he's not on a title today as well, because he was there for the one. It's really rewarding when you can actually have a conversation with

1:56:35 And we're trying to do active coherence lab, which is, you know, create a bigger tent, create a sense that people with different backgrounds don't have to feel strange, because they don't. I don't know as much about active coherence as Max Rams did, so I'm going to spend ten 0 hour to have a conversation about this. That's not what we're about. What we're trying to do is pull a bunch of people into the room and let them translate together, swap those perspectives, actually go away, as Iain said. I'm going to go away now and figure out why.

Really? Why does this laser idea work not just sort of in a hypothesis in my brain, but really go away and think about that for a bit. And I think if we can do that more in a semiformal way, you still have to COVID the content and you still need to get the contextual background, but to get to this place where we are today, jordan, to your point, it takes time, but, man, the rewards and the payoffs, it's just huge.

1:57:35 And again, Daniel, all the work that he puts into doing this, it's awesome. So thank you.

1:57:44 Daniel:

Thank you.

1:57:46 Ian:

Thank you.

1:57:46 Jordan:

This is really fun.

1:57:48 Daniel:

Yeah. Great conversation.

So really appreciate it. Also, as always, alright. Till the dot three, anytime you or anyone else want to continue or present any other time, always welcome. So very well.

1:58:03 Ian:

Thank you very much.

Bye.

1:58:04 Jordan:

Awesome!


---
*Extraction method: odt_xml*