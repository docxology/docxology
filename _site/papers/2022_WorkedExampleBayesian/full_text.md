# Full Text: A Worked Example of the Bayesian Mechanics of Classical Objects

> Extracted from `ActInf_Livestream_49_'A Worked Example of the Bayesian Mechanics of Classical Objects'.odt`

---

ActInf Livestream #049.0 ~ “A Worked Example of the Bayesian Mechanics of Classical Objects”

Discussions2 preprint

https://arxiv.org/abs/2206.12996

Presented by Active Inference Institute in 2022

https://www.youtube.com/watch?v=OtX2Fpzn7KA

This video is an introduction for some of the ideas in the paper.

Daniel Friedman, Ali Rahmjoo, Jakub Smékal

02:51

Introductions and warm-ups.

08:28

How is Bayesian Mechanics relevant?

15:34

Derivation of classical physics from the Principle of Maximum Constraint

17:31

The journey from Bayesian Mechanics to quantum biology

18:07

A question of quantum ontology

21:12

Historical perspectives

49:50

Introduction of the concept of blanket index

54:17

Three faces of Bayesian mechanics

56:50

The dynamics of a system

1:01:26

The Principle of Stationary Action

1:05:31

Newtonian mechanics

1:10:37

James' Maximum Entropy Principle

1:12:34

The Heisenberg Uncertainty Principle

1:17:23

Bayesian mechanics

1:20:10

Constrains by the maximum entropy principle

1:23:17

Three phases of Bayesian mechanics

1:26:03

Classical physics

1:31:48

Mode matching

1:33:59

Mode tracking

1:34:49

Terminal mode matching

1:38:18

Bayesian mechanics: Path tracking and G-theory

00:29 Daniel:

Hello, everyone. Welcome. This is Active Livestream number 49.0. We're discussing the paper, "A worked example of the Bayesian mechanics of classical objects." Welcome to the active inference institute.

We're a participatory online institute that is communicating, learning, and practicing applied Active Inference. This is recorded in an active Livestream, so please provide us with feedback so we can improve our work. All backgrounds and perspectives are welcome, and we'll be following video etiquette for live streams. Head over Active Inference.org to learn more about participating in different projects and learning groups at the institute. Well, we're here today in Livestream number 490, where we're providing some background and context for the paper, a worked example of the Bayesian mechanics of classical objects.

01:29 This paper was submitted to the archive preprint server in June 2022, and we're going to be discussing and looking at a slightly revised version that was uploaded earlier this month on the 6 September. It's a single author paper by Dalton AR Sakdiva. Daniel, and this video, although all dot zero are, this one is too. It's an introduction and just a preliminary discussion of some of the ideas. It's not a review or a synthesis or a final word, and we'll explain a little bit more about our dot zero zero approach in a couple of slides.

But suffice to say that with Yaqu Align and also Andersen, we had a great time over the last two months really pulling back and trying to think deeply about how to frame this paper and really this whole area of research and development, because there's a lot happening, there's a lot being tied together.

02:32 And so we hope that some of that sense making translates into the ways that we've laid out 49.0. And we're very much looking forward to having Dalton join for the dot one and the dot two. So, Dalton, thanks for all the work and for listening to this dot zero zero. Let's head to introduction and warmups so we can just say hello and any other features of what we're excited about in this discussion.

I'm Daniel. I'm a researcher in California, and I think there's a lot that is exciting about this paper. I didn't have much of a physics background before heading towards active inference in the free free energy principle. Taking a first look at a lot of these physics ideas was interesting. Like, seeing them as part of something that already could or had been integrated, rather than starting with the puzzle pieces, I think was a little bit interesting.

03:34 And I'll pass to ali.

03:38 ALI

Hi, I'm Ali. I'm an independent researcher from Iran. Actually, what gravitated me towards active inference paper I mean, SAP or active inference literature, and particularly this paper, was, you see, I've been fascinated by doing the kind of elegant abstractions on some physical concepts or some doing a kind of bird's eyed view over the methodological way of doing physical modeling. And I believe this

04:54 And yeah, that's why I'm pretty excited to be here, actually. It's been a very fascinating and thrilling journey during the past couple of months since we began discussing this paper. And so I'm very much looking forward to it.

05:17 JAKUB

Hello, I'm Jacob, I'm a student and researcher in the UK. There are also many...

05:30 Daniel:

Okay, lost Jakub

05:48 Jakub:

Sorry, I got ya.

05:49 Daniel:

Go for it. Just start again, Jakub

05:53 Jakub:

Where was I cut off?

06:18 Daniel:

Just start at the beginning. It's all good.

06:20 Jakub:

Okay. Sorry, I got randomly disconnected, so hello, I'm Jacob, I'm a student and researcher in the UK.

I was really excited about this paper, specifically coming from physics background, which I must say didn't help that much in initially understanding the paper on the first pass. But I think it's really exciting that this kind of implication of physics and cognitive sciences is formed through works like this paper or prior work that Karl First and colleagues have been working on. And I'm really excited about how this work might influence the future synergy of physics and cognitive sciences, or neurosciences, which I think previously were quite disjoint Fields.

07:26 But now with the more focus towards like, complexity sciences, we're seeing these similar patterns across a wide range of topics, which I find really exciting. So really looking forward to the discussion and the rest of the Livestream.

07:53 Daniel:

Great Brea. Thanks. So we're going to go to the big question Ames claims abstract and roadmap. And then before we head off off on that road trip and way field together, we're going to pull back to our approach and set a lot of context. And that will be most of this dot zero video.

And then we'll briefly touch on some points from the paper. But most of this video is going to be

Are we talking about physical mechanisms underlying cognitive agents or are we talking about something else? It's the second what is of epistemic and pragmatic value about Bayesian mechanics?

08:55 If we're going to be using active inference in the free energy principle as the gripper and the grip, then how can we understand what is valuable and relevant and salient in terms of active inference ways of thinking about it? What would you fellows and what felt like really big questions that would lead somebody to want to be exploring this paper?

Yeah, Ali.

09:25 Ali:

Well, actually, before talking about the specific from pragmatic value of doing Bayesian mechanics. I think what at least in my view, what's really interesting about basically a mechanical way of doing these kind of probabilistic formulations and mathematical modeling is just pure elegance in.

10:08 Daniel:

Pick up again from.

10:09 Ali:

Your different elements.

10:14 Daniel:

Sorry, Ali. Pick up from pure elegance.

10:17 Ali:

Okay, yeah. As I was saying, I think one of its main interests is its pure elegance in unifying the different approaches to FEP in a kind of allencompassing framework called ambassian mechanics, by which it can possibly the other frameworks and other viewpoints and even other kinds of mechanics can be recovered. So at least for me personally, this is the most interesting part and exciting part of doing Bayesian mechanics.

But I'm sure there will be much pragmatic value and much more applications that can potentially derive from this kind of viewpoint.

11:12 Daniel:

Awesome. Where's beauty and elegance in epistem and pragma. Yaco.

11:20 Jakub:

I definitely agree with all these points. And maybe to add to that, I think it's really elegant that within Bayesian mechanics you have a unifying formalism with which you can recover much of the same loss that we see in classical physics. Also, we can also talk about the quantum mechanics as being enclosed within the Bayesian mechanic formalism, but at the same time, using those same concepts, we can also

12:27 Daniel:

Awesome.

Beauty as elegance as indicators of scope and scale. So the paper is a worked example of the Bayesian mechanics of classical objects. We've mentioned some details about it before. I'll just highlight a few claims, some coming earlier in the middle and later in the paper. So earlier in the paper, it's often claimed that the free energy principle is as simple in general as the principle of stationary action.

And that is a citation to a paper that we're going to discuss in just a few slides. Simpler, but not too simple. And it's claimed about the FEP that it can be sketched out how Bayesian mechanics of internal states of classical objects might look. And that's a citation to Frist in 2019 free energy principle for a particular physics, which we're also going to look at. Nevertheless, there's yet to be a systematic investigation of even the Bayesian mechanics of classical physics, despite it being readily available due to recent formulations as a least action principle.

13:38 So we've talked a lot about on these streams and elsewhere about the free energy principle as a variational principle of least action for cognitive systems. So there was an opportunity that Dalton identified, which is to make a systematic investigation of classical physics and provide worked examples. Towards the middle of the paper, there are some important aims, such as we begin with the aim of showing that classical physics can be derived from Bayesian mechanics. So we'll work with different metaphors and ways of exploring it. But this is not like a layer two on physics.

This is a generalization that in special cases includes classical statistical thermodynamic and quantum mechanics. We can derive Bayesian mechanics from the idea that a system is classical on average, just as we can derive classical mechanics from the idea that systems obey Bayesian mechanics force classical averages. We're going to unpack that later, but it's a key claim.

14:39 And then later in the paper there is the aim to eventually formulate chaotic or Itinerant systems under Bayesian mechanics, as has been done for earlier forms of the free energy principle. And that's kind of what the paper is going to be leading towards and suggesting for future work, including that of g theory, anything that you fellows would add.

All right, could somebody read the abstract?

15:09 Ali:

Yeah, but before going into abstract, I wanted to point out one of the main goals of the paper I think would be there are a couple of new results in this paper that wasn't introduced as far as I know in the previous literature, one of which is the derivation of classical physics from the principle of constraint, maximum entropy and the reintroduction of supersymmetry as an explanation for classical chaos, as indicated on page five of the paper. So I think this is in some way this paper is a kind of expanded footnote to the previous papers, but also adding some new results. I Dean it's a very important appendix to that paper by making some of the theoretical claims of specifically on Bayesian mechanics paper more concrete.

16:18 So, yeah, I just wanted to point that out as well.

16:20 Daniel:

Great point.

This should be of interest to people who are following the development and applications, active inference lab and free energy principle. But it will become clear that the scope is very broad and people, even outside of what might be perceived as just this community, will hopefully find interest and apply scrutiny and continue the conversation with us. So somebody may read the abstract.

16:48 Ali:

Sure.

16:49 Jakub:

So Bayesian mechanics is a new approach to studying the mathematics and physics of interacting stochastic processes.

Here we provide a worked example of the physical mechanics for classical objects which derives from a simple application thereof. We summarize the current state of the art of Bayesian mechanics. In doing so, we also give a sketch of his connections to classical chaos owing to a particular N equals two supersymmetry.

17:15 Daniel:

Short and sweet to the roadmap. Alright, so the paper begins with I'm putting us our video over the top flow on this stack.

So the paper begins with an introduction and then dives into the concept of mechanics, which we'll be talking more about. The subsections there are covering classical physics in one dimension, the basics of Bayesian mechanics, a physics of beliefs and then a physics by beliefs, which is going to be kind of taking us into this cognitive lens. Then a general equation, equation 15 for Bayesian classical mechanics is presented and that'll be a really exciting equation in formalism to lead up to and unpack the following section four is a question of quantum biology. This is going to touch on discussions that we've had including in Livestream 40 on the free energy principle for generic quantum systems and about what quantum means and how we can think about things that are often described as being at the atomic scale, whether it's the idea of quantum mechanics itself or bosons and fermions and all these other kind of like weight.

18:37 But I thought that was at the atom scale.

And what does it mean to apply it to cognitive systems. There's then several cases that are addressed and those are the worked examples that's the matching of modes, the tracking of modes with the subdivision into terminal mode matching and infinite mode tracking. And then towards the end there's the adventuring into path tracking. These are the three phases of Bayesian mechanics mode matching, mode tracking, and path tracking. We're going to look into it and a simple case of g theory.

And so that is where one gets to by the end of this journey. But before we head off, as promised, we're going to dwell for a second on how we can set context to even head off on this journey. So would anyone like to just describe like what the sections that we're about to jump into are about and what led us to use this approach?

19:50 Ali:

Yes, actually, as we discussed before, we begin by looking at some historical perspectives and historical concepts of all the developments of FEP literature throughout the past two decades. And then we'll look at some of the key literature on which this particular paper beliefs upon. And then we'll look at some the three kinds of theories that's been introduced in on Bayesian mechanics paper as the way of anchoring all the theoretical arguments there. And finally, we'll talk about the free nonbayesian mechanics before delving into what Bayesian mechanics is and what are the differences and similarities between all the different kinds of doing physics or mechanics.

20:56 Daniel:

Awesome, we hope sets the discussion within historical and integrationist framing.

And it's going to be quite a journey. So let's head into this section. First, let's talk about some historical perspectives and different epochs of research. Broadly, we can think about what happened before the free energy principles emergence in the pre 2000, the pre millennial era, without going too specifically into the what citation the free energy principle originates in then we can think about the free energy principle between roughly 2005 all the way up through 2020 around. And then lastly some of the changes and developments in free energy principle literature since about 2019 to 20, and some of Dalton's contributions.

21:57 So, starting with the free energy principle before 2000, there's no definitive history yet for the antecedents of the free energy principle and surely a presentation or project more focused on that history could and should and will happen. But a few of the places to search for in terms of the personal history of key contributors and also places where peripheral contributions and important foundational precursors are described. Some places to look include the statistical parametric mapping textbook and documentation, and the decades of research that went into the Neuroimaging work on SPM, as well as a Karl Friston 2012 article, The History of the Future of the Bayesian Brain, and an interview with Karl J. Friston, Woodlice and Men, as well as the auxiliary supplement to the above interview.

22:57 Am I autistic and intellectual autobiography?

So that'll take somebody from the sort of zero to eight and then eight to 28 and then 28 and beyond of Karl Fristin's work and development with Copious references. Out on the right is a slide from live stream 14 where we explore just one aspect of tracing the thread, which was from the analytical formalizations of, for example, Markov in terms of statistics and matrices all the way. On through perl and the computational implementation Bayesian statistics physics on through to Modern developments that integrate those kinds of Bayesian formulations of statistics with action, which encompasses a variety of Fields such as Cybernetics, complex systems, synergetics information theory, control theory, ecological psychology, four cognition, extended, embodied, et cetera, et cetera.

24:02 Autonomous systems and all other types of frameworks. So it would be a history of the world to talk about everything that happened before 2000, but these are just some threats.

Anything else that people want to add?

24:18 Jakub:

Yeah, maybe that as the theory gets more integrated to various different field, I think it's going to be

24:53 Daniel:

Nice align.

24:57 Ali:

And also related to this historical context, I wanted to point out the heated discussions that's going on during the last couple of years about the use of some established vocabulary or terminology in active inference or SAP literature, one of which is using the markup blanket in a kind of different context. But as Maxwell Ramstead's Twitter thread from yesterday pointed out to a very interesting example, we can say the same for a lot of mathematical constructs. For example, we can look at the concept of zero as a purely mathematical construct, but used in different contexts.

For example, it can be used as a null container or a null counter, but on the other hand, it can be seen as the solution of a polynomial or a function.

26:10 And the same goes here for using the same mathematical construct or theoretical construct markup blanket, but in a different concept. But that doesn't mean markup blankets or any other theoretical concepts used in FEP literature are denying the or somehow are contradictory with the previous usage of that terminology. It's just used in different context.

26:47 Daniel:

Awesome.

So as a really concise way to summarize again something where further presentations and work can do a much more comprehensive job, there's a Maxwell Ramstead Tweet thread from 711 2020 and Maxwell breaks down developments in the free energy principle modeling into several waves. And the Tweet thread is readable here. The first wave doesn't have policy selection per se. The dynamics of internal and active states was determined in a stepwise fashion through gradient descent on variational free energy. And so that was very much like a pure OneStep gradient descent framework.

Second wave model started around 2012, equipped agents with beliefs about state transitions and the sensory consequences of movement that allows the calculation of expected free energy like values. And third wave models use a recursive expected free energy functional, which opens up all of these related avenues.

27:55 So Maxwell's threat here summarizes some of the waves of development, and there's so much more to add and unpack because there's been developments on multiple different fronts or I wouldn't even know what word to say. There has been formal developments and technical exploration as well as generalizations, and also, of course, a huge area of philosophical discussion around these topics. So there's been a lot happening since 2005 to 2020 in free energy principle, and this is going to agent us up to where we're ready to explore what's happened in the last few years from this kind of building momentum and progress in the space.

Anything to add, Jacob?

Maybe just a short comment that I think a lot of the first and perhaps even the second wave we can probably see more influence of Carl's Preston's prior work on STM and all the literature that surrounds it. Whereas in the kind of third h or third wave we are seeing more integrations into other field like physics and overall complexity. Science.

29:41 Daniel:

Great point. As the literature builds and as other collaborators begin to upskill and contribute, then we start seeing some different approaches.

But there's initially a lot of similarities with SPM and it's really still quite a useful framework to use, of course, but also point back towards alright then onto the third epoch that's post 2020 and Dalton's contributions. So we laughed and had a great time reviewing many of the fascinating developments over the last few years in a range of topics made by Dalton, ranging from fundamental physics to neuroscience and most recently Bayesian mechanics and g theory. A lot of the work is single author. Other papers and works of note are collaborations, for example with Ramstead, Friston, Blanket, others, and this is just a few, this is some subset screenshots from our Coda knowledge integration work, where we have a bunch of papers, blog posts, videos, tweets.

30:57 We were just bringing together a lot of different information and we'll look forward to hearing it from the source soon enough.

The specific papers that we want to discuss, we're going to in the next session, but this is all to say that it's been a quite productive streak for Dalton and an awesome learning experience for us all. So we really appreciate all that work and we're looking forward to the conversations. Anything you want to add on this outside of the literature?

All right, next we will go to the literature. We're going to go through about four or five papers that are important steps on the way to getting to the work example. So let's just go right into it. This is going to be a paper from outside of the Friston sphere in one sense, but not in another sense. It's a 2012 paper by UDA ciphert.

31:59 And the paper is called Stochastic thermodynamics Fluctuation Theorems and molecular machines. Surely the paper is worth a deeper take. But just to highlight at the very high level, stochastic thermodynamics as reviewed here systematically provides a framework for extending the notion of classical thermodynamics such as work heat and entropy production to the level of individual trajectories of, welldefined, nonequilibrium ensembles. That is going to be a key move and theme, which is a move from a kind of differentiate mass action or mean field approximation physics and finding compatibility between that kind of an averaging and recovering that averaging outcome via individual trajectories of well defined nonequilibrium ensemble.

33:02 One can imagine that if they're interested in the consideration of specific counterfactuals policies or in the behavior of multiagent ensembles simply having a mean field approximation, the kind of which classical thermodynamics has provided for work heat in entropy.

Production. It will be another step and potentially an unprincipled or intractable one to ever go from that mean field down to the trajectory level. And so the kind of synthesis work that has to occur and is pointed towards here is to understand how a special case or abridging formalism can connect this kind of mean field population scale summary statistic aggregate worlds to individual trajectories of well

33:59 Ali:

Well, actually, I think one of its central importance of this paper to Sakurai's print paper is the definition of the past probability measure in the abstract Wiener space, namely equation number five, which I believe is a very significant preliminary stage toward deriving the general equation of Bayesian mechanics or equation 15.

34:33 Daniel:

Excellent. Onto the next paper. The next paper is a single author paper by Karl Friston in 2019, a free energy principle for a particular physics. So it's a little small on the slide, but this is like and 148 page paper. And you'll note there on the header, this work is under consideration for publication by the MIT Press.

So there's an interesting story whose middle and end is unknown about the recent active inference textbook and the way in which that is providing kind of a handbook of active inference. But then there's something more like a theoretical physics book that is going to be presented in some future time, particular physics is a multieantra or a pun in a few different ways. This is a particular physics in the sense that because it's being specified, it's like a specified or a specific physics, like any dinner that you make is a particular dinner in that sense.

35:36 Also really key to this notion of individual trajectories of, welldefined, nonequilibrium ensembles is the notion of the particle and the particular states. The particular states are referring to when we have a partition that uses the Markov blanket.

So blanket states making internal and external states conditionally independent, we can then talk about the blanket and the internal states as the particular states because they're like the particle that's floating around. So in the brownian mechanics world, then you have the dust molecule floating around in the water, and the particle is the dust molecule, and then the external states are the water. And along those lines, the cognitive particle is going to be the internal and the blanket states. That's what's going to have cognitive mass and inherit all of these physics terms that might be kind of like billiard balls are to classical mechanics.

36:38 We're going to be looking at what that particular form is for cognitive systems.

This was an extremely important work, conceptually as well as socially maximal. Ramstead facilitated and organized a really amazing discussion group over many months, working with a lot of people to go through chapters and surfacing a lot of important dots that could be connected, technical contributions raised by many participants in that reading group. And the work itself is a theory of everything, but perhaps in a way that people might not expect. So I'll just pause there if either of you want to give and overview thoughts on the monograph. What does it mean by a theory of everything?

Or what else would you add about this precursor paper?

37:40 Ali:

In fact, I wanted to point out an important note stated in the footnote number one of the classical physics paper.

In this paper by Karl Friston, the word particle is used, as you mentioned, for the combination or the

38:41 The word particle is used as the joint set of the internal and blanket states, but not in this one.

38:50 Daniel:

Thank you. Jockey want to add anything on the paper.

38:55 Jakub:

Maybe just to slightly add on the theory of everything, that refers to the notion that anything that exists needs to have some kind of statistical independent from its environment, which constitutes a Markov blanket. And I think we'll see in the coming slides that some contributions from Dalton have also shown this to be the case in cases where the FEP has previously been criticized for not actually applying generally to systems which don't reach that threshold. So yeah, I just wanted to add that nice.

39:58 Daniel:

When people talk about a theory of everything and they leave out the space, they might mean like a theory of all of it. But this is actually a theory of all of the open parentheses, observer dependent, modeler, independent, closed parentheses things that can be distinguished. Again, that's where the observer is in the distinguishing from other things. In a statistical sense, if you can't distinguish it over the time scale of observation, it's just not a thing. It's not to say that it's not part of someone else's theory of all of it, but in this sense it's not a thing.

And that's what is also setting up at a very fundamental level for this notion of systems engaging in the boundary of surprise because systems that don't bound surprise will not be observed to be that kind of thing in the way that the surprise was limiting. And the work also points importantly towards compatibility among quantum, statistical and classical mechanics.

41:06 Those are the three non Bayesian mechanics that we're going to be going into. Bayesian mechanics is going to generalize and encompass and integrate across all of these. And it may offer a formal description of lifelike particles.

For example, classical mechanics could tell you what happens when a 200 pound object falls out of a plane. But I think, as Dean has raised, what happens when that entity has a parachute. So there's something different there. And what could the reductionist physicist do other than try to make a physics model of the elbow and of the ions coming in and out of the neurons? Reductionism is kind of the way in that situation.

And so we're gain to be talking about potentially a way to see that active particle falling out of the plane as something that could engage in agent decisions. Next Paper this next paper is the free energy principle made simpler but not too simple.

42:10 Be careful. It is a paper from Karl Friston Costa, Sajid, Heins, Oldsuffer, Pavliotis and Par. We discussed this Parr in several discussions earlier this year.

In Livestream number 45. We have 45.0 background and context and we have the dot one and the dot two with Thomas Parr, Andy Clark force in joining for the discussion and saying many interesting and

This paper rehearses key steps using standard results from statistical physics.

43:14 Those steps are going to be one establish a particular partition of states based upon conditional independent inheriting from sparse coupling. Again, particular is. Being used in the pun sense as it was before. This is like one specific partition that you could choose to implement, and it's the one that results in particles.

Two, unpacking the implications of that particular partition. In terms of Bayesian inference, one of the kinds of inference that's really important is about internal states doing inference on external states mediated through sense states on the blanket. And then three, describing the paths of particular states with a variational principle of least action, which is going to tie us towards understanding individual trajectories of well defined nonequilibrium ensembles.

This paper was discussed elsewhere. So here's Brock and I in the dot zero talking about nonequilibrium birds.

44:18 And then here we have Bleu and Karl and Thomas, and we're just trying to catch up with what they're adding. Anything that you fellows would add about this paper.

All right, now we're going to enter into the Dalton zone. So this is in Anil 2022. Dalton presents a single author paper towards a Geometry and Analysis for Bayesian Mechanics. The paper presents a simple case of Bayesian mechanics under the free energy principle and formulates it axiomatically. There's going to be a lot of interesting things to unpack.

Does anyone want to just give their read on the importance of this paper?

45:14 Ali:

I think this is one of the first papers Dalton has attempted to provide the rigorous mathematical foundation for FEP by providing some formal proofs of relevant theorems, but without, I mean, going into a lot of technical jargon. I mean, this paper is pretty accessible for people even not specialized in mathematical proofs and so on. But I Dean by skipping those technical mathematical proofs, the whole conceptual framework or the gist of the paper is totally accessible, in my opinion. So I think this is one of the very significant and important steps toward developing the more comprehensive theory provided in their next paper on Bayesian mechanics.

46:27 Daniel:

Great.

This is going to be connecting the random dynamical systems formalization and takes a further step towards comprehensive statement of the physics of selforganization in formal mathematical language, which is presented using gauge theory and some geometric notions. And that's going to create a concordance that can be at least stated qualitatively but has a lot of technical underpinnings, which is the relationship between the dynamical systems action of selforganization in terms of bounded surprise connecting that to a gauge theoretical formalism of selforganization in which gage forces are ActInf lab. The system and others can, and please should help us unpack this and do math streams with us.

47:27 Here we're going to point a little bit more briefly to two recent papers.

Well, they're all recent. It's only September, 2022. This was only five months ago. Here is a paper from August. Actually, both of them are from August, but the first one was first published in July.

The first paper is Weak Markov blanket's in high dimensional, sparsely coupled random dynamics systems. That's a paper by Dalton and then a paper with Maxwell, Dalton and Karl on the map territory fallacy fallacy. Would either of you like to just pick one of them and just describe like what was Conor or important about these papers?

48:11 Jakub:

I would maybe say on the week mark of blankets in high dimension, sparsely couple random dynamics systems. I think that paper is really crucial because it does unpack a lot of a lot of uncertainty that many people might have had with the FEP before, especially the spark Parr coupling conjecture that finally received a formal formal proof.

And I think it's also important in this paper that we are going to going to discuss, especially when we are talking about systems at the quantum scale or beyond the quantum scale, where sparse coupling is a much more present notion than non sparse coupling.

49:22 Yeah, I think this is a key paper in all of these prerequisite papers.

49:32 Daniel:

Thank you Ollie. Feel free to say something you like about either or both.

49:39 Ali:

Adding to what Jacob said about week mark of blanket's paper. I think one other significant contribution of this paper to the FEP literature is introduction of the concept of blanket index, which was a very sorely needed concept because by foraging the mark of blankets, by this concept, we can see that when we talk about any markup blanket. It's not a singular or, I don't know, necessarily 100% consistent concept, but it can be graded encoding to this blanket index. Namely, when the blanket index is zero, we have the strongest markup blanket. I mean, that also recovers the spark's coupled conjecture.

50:40 But when it maximizes, we have this concept of weak markup blankets, which is basically what most linear systems have, most linear systems have. But when we discuss the higher dimension systems or more complex systems, the mark of the blanket index somehow minimizes or in fact goes to zero in sparse coupled system.

51:13 Daniel:

Awesome. Yes, it is an important contribution and maybe we can unpack this paper more as there also become more perhaps worth examples of weekly mixing Markov blanket zones and anything to add on map territory fallacy. Fallacy.

51:40 Ali:

Is also kind of, I believe, a response to some of the criticisms going on about what's exactly the map

52:50 So the concept of map fallacy fallacy comes from this viewpoint by which this socalled fallacy is itself another level of.

53:07 Daniel:

Awesome. All right, on to the next paper. This is Gain to be a key recent paper from May 2022. It is on Bayesian mechanics of physics, of and by beliefs of the beliefs, by the beliefs for the beliefs, with Ramstead et al. This is active guest stream number 23.1.

So on the right here's, Dalton, Maxwell, and Lars. And I talking about what looks to be like it's going to be an American baseball field, but actually it's a path of least action. And this paper introduces or reintroduces a field of study that has emerged over the last decade called Bayesian mechanics. And it's that introduction and like, nice to meet you again for the first time, which is why Maxwell called the streaming that we did rebooting the free energy principle literature. The paper is extremely accessible and engagingly written.

It reviews the state of the art in the literature on the free energy principle.

54:12 And then in this very nice figure that we're going to return to multiple times, introduces the three faces of Bayesian mechanics. We're going to go into them more in the worked example paper, but they are fixed mode on the left, dynamics mode in the middle, and then path tracking on the right side. And the broader or the higher order, like generative or family level distinction is the fixed mode seeking. And then the dynamics.

Mode tracking are regarding modes of densities over states, whereas path tracking moves us into a path native formalism rather than like a point and state space formalism. And they're all faces of the Bayesian mechanics under the free energy principle. And this paper not only discusses those three phases of Bayesian mechanics, but it examines the duality of the free energy principle and the constrained maximum entropy principle, developed and derived and explored in other Dalton work, which we're not going to talk about here.

55:17 Moving on, that was the key literature. Now we're going to stick on this Bayesian mechanics paper and talk about three kinds of theories.

So the three kinds of theories that we're going to discuss are dynamics, mechanics, and principles. And because theory can take on many meanings, it's important to quote the authors on how they use and therefore how well try to use the term. So they wrote, the word theory is polysimus. It has many meanings. What we have called dynamics, mechanics, and principles are ultimately mathematical structures.

In mathematics, these are called mathematical theories. The content of a mathematical theory or structure is purely formal. What are usually called scientific theories or empirical theories comprise a mathematical structure and what might be called an empirical application, interpretation, or control of that system, which relates the constructs of the mathematical structure to things in the world.

First two dynamics.

Go for it. Whoever would like to walk through these next three.

56:43 Ali:

Yeah. As indicated in Gain, mechanics paper, we can think about the dynamics of a system as a kind of descriptive or phenomenological, let's say, description of the system, or the kind of description that tries to answer the what questions of the system. So if we look at it by the lens of many different physics or mechanics, in classical physics, we might characterize it as kind of galilean or prenewtonian dynamics. Or in statistical physics, we can say the behavior of particles under diffusion as an example of the dynamics of the system. In quantum physics, we can talk about quantum dynamics as this kind of phenomenological description.

57:46 And actually, we're talking the other day about this term Bayesian physics, which I've used on this slide. I'm not sure how Dalton would react to that. But in order not to duplicate the other slide, which talks about Bayesian mechanics explicitly, I use that term here. So, yeah, in Bayesian physics, we're dealing with the system, the systems by which the dynamics are the self organized, self organizing system, or some authors would call auto organizing systems.

58:29 Daniel:

Awesome.

So dynamics are describing the what. And we're showing Bayesian physics again with the caveat Ali just mentioned alongside the three other physics that we're going to be discussing integration among. So dynamics are the what. That's how the billiards are moving on the table. What is happening?

The next level is mechanics. So somebody else may describe mechanics.

58:57 Jakub:

Yes.

So moving from understanding what the systems that we want to describe, the mechanics can help us answer the how questions or actually create the mathematical formalism that will be able to make predictions about what is going to happen and how it happens. So in classical physics, we have classical mechanics, either Newtonian, Lagrangian or Hamiltonian. In statistical physics, we have statistical mechanics, quantum mechanics describing Hohwy things behave on a quantum scale, which we're also going to unpack a bit further in the coming slides and then Bayesian mechanics with the mathematical formalism from the paper, physics of beliefs and also the work example.

1:00:04 So the equations that come out of the mechanics are ones that can be used in a predictive sense and also in further trying to understand or in creating new systems that work on similar principles. And I think mentioning principles might continue the good transition into the third distinction, the why questions, which are kind of these overarching theorems, or rather principles that say why things, why the what, and how questions or topics work the way they do.

1:01:06 And principles usually form this kind of axiomatic or take this kind of axiomatic stance where from the principle, everything else can be derived or can be put under the blanket off. In classical

The same thing is present Bayesian statistics physics and quantum physics with quantum physics having the correspondence principle, which is very relevant in this paper, where in the limits of large numbers, quantum systems approximate to classical systems, which I think speaks to is also related to the work here in the work example, where quantum systems performing approximate Bayesian inference in a quantum setting follow classical paths on average, which we'll get into later.

1:02:50 And then Bayesian physics, of course, having the free energy principle.

1:02:57 Daniel:

Awesome. And just to put up what that table looks like, we also had a ton of other correspondences and rows and columns. So anyone who is interested in this kind of concordance building work would be encouraged to participate in the institute because this is a really awesome tool and helps show us potentially areas where statistical mechanics has been applied as a mechanics.

Can we bring Bayesian mechanics to bear? Or areas where stationary action was applied for classical systems? Can we talk about how the free energy principle might be able to reformulate that or provide access to new tools or new perspectives? So this was our part of our table. Let's go a little bit deeper into those three non Bayesian mechanics or the three non Bayesian physics.

Again, I'm really looking forward to exploring different ways that we can think and talk about these different physics and mechanics, but just one kind of way to think about how the special case of one physics could be an entire other physics.

1:04:07 Like Dacov just described. Like in the Socalled classical limit quantum systems behave classically, but then also it has a space that goes beyond classical, but that doesn't negate the relevance or utility or simplicity of classical mechanics. So how can something be encompassing but also provide identity for the special case? And it reminded me of the anatomy of mammalian muscle fiber with this kind of hierarchical organization of blankets.

It even looks so much like the blanket illustrations that we've seen. And so we can think about classical as then being a limit case of statistical and statistical being a limit case of quantum. And then that is where Bayesian mechanics is going to come into play. Okay, first, classical mechanics. Who would like to do their short one slide or presentation?

Yes, Markov?

1:05:07 Jakub:

So classical mechanics, as the name implies, describes the behavior of classical objects. And I think the kind of two main threats to highlight here that are relevant even for understanding. The paper on the work example of Bayesian mechanics is the Newtonian mechanics, which is usually the classical mechanics. That's the first that people hear about with force, describing how with the description of the movements of objects, describe how based on how forces are acting upon them and the three fundamental laws. And then the Lagrangian mechanics, which takes this more energy principle of these active states where the main thing of interest is the Lagrangian, which is just the kinetic energy minus the potential energy of the system.

And in this case, that would be the red path, where if you dropped a ball on that surface, the Bull following the red cue would take the least amount of time to travel between those two points.

1:07:44 Daniel:

Why is everyone in a hurry? Okay, on to statistical mechanics. Well here ali. Do you want to go for it?

1:07:58 Ali:

Well, yes.

Statistical mechanics actually deals with the theories producing the behavior of systems with probabilistic degrees of freedom, especially the ensemble level behavior of large numbers of functionally identical things, at least according to, um, Bayesian mechanics paper. But I wanted to point out a comment made in one of Dalton's posts about the status of statistical mechanics in relation to all the other areas of physics. He writes, Beginning from Einstein, theoretical physicists were interested in formulating all these physical theories in terms of purely mathematical and rigorous formalisms. And so we have rigorous theory of classical mechanics and quantum mechanics and so on. But one conspicuous absence in this list is this is statistical mechanics here, or thermodynamics, because although we have some physicists in the century, physicist, mathematicians like James and Cosmograph and so on, but up to now, statistical physics remains mystery.

1:09:32 Not that all the related areas of physics, for examples, the thermodynamical systems, condensed matter and soft matter or biological systems, they remains complete mysteries. So one of Dalton's aims in producing this literature throughout the past several months is, at least to the best of my understanding, is to somehow cover up this yawning gap in the literature and doing that via formulating this Bayesian mechanics, which can encompass purely mathematical formalism of statistical mechanics as well. And also, one of the most fundamental principle of least action physics, which Dalton has used in these papers in order to formulate the basic mechanics is James's maximum entropy principle, which is the principle by which the mechanics of statistical objects lead to diffusion or the descriptive dynamics of the systems.

1:10:51 Daniel:

Great. Thank you.

And from this paper by Abad in 2012, we can start to bridge quantum and statistical mechanics by looking at how, on different criteria, they have some concordances. So this is like going one layer deeper. Hinton those concordances. Let's go on to quantum. Okay, so quantum.

We've discussed quantum a few times on these live streams. We've discussed some relevant topics in Livestream 17 with Chris Fields and then more recently in Livestream number 40 with Field, Glazebrook, Friston and Levin. And would either of you like to describe quantum in terms of where it

1:11:49 Jakub:

Yeah, I think as physics developed over time and we were trying to describe smaller and smaller systems that higher precisions at some point we realize that systems don't obey these classical laws set forth by Newton or LaGrange or others. And quantum mechanics is the formalism for describing systems on a subatomic scale. I think one of the two major concepts to mention is the Heisenberg's Uncertainty Principle, which states that when you have a subatomic particle, there's always and uncertainty on its position in physical space and its velocity, where there's actually this kind of entanglement of the two in the sense that if you know one with certainty, you know the other with uncertainty and vice versa.

1:13:08 And you have this kind of and you can move along this line where you can partially know the position or partially know the velocity but not both at the same time. Which I think is really interesting from the point of Bayesian mechanics because quantum mechanics is really one of the first subfields of science where the notion of an observer and the act of observation has needed to be ingrained in the actual mathematical theory.

Because you can't just shine a light on an electron because that will ultimately change the system. And so the interaction of the observer and the environment and performing inference over how do individual things in the environment.

1:14:11 Ali:

Behave.

1:14:14 Jakub:

I think that's something that Bayesian mechanics is trying to unify. And I think the quantum ontology is very relevant in this case. And of course, we have quantum mechanics is obviously a large field that's also connected to various other Fields. One other notion to mention would be the double slit experiment that's depicted in the image on the right which was one of the first, if not the first, I'm actually not sure at the moment. Instances showing the wave particle duality of subatomic particles in this case electrons where particles display behaviors of both waves and particles and the behavior is very dependent on the way that we do our observations.

1:15:20 If we want to observe the electrons passing through a sled before they reach the screen that influences the behavior of the electrons then when we look at the screen after all the electrons has passed through the slits.

So we have these kind of weak Markov blanket but without the actual introduction before the introduction of week Markov blanket.

1:15:50 Daniel:

Awesome. It's kind of like all the jokes around how people behaving differently when you're observing them. Now there's a cognitive analog. So some of those intuitions weren't so far off after all.

And we won't talk about the paper too much. But there's a recent paper from September 2022 connecting the free energy principle with quantum cognition, where they introduced this concept of

1:16:57 Whereas these applications of quantum cognition to larger cognitive systems may be absolutely compatible with those kind of orcor or quantum microtubule theories, but they do not require that to happen. It is more going to be referring to their ability to engage in counterfactuals spaces and the relationality that Yakut mentioned. All of that brings us to Bayesian mechanics. Okay, who wants to go for Bayesian mechanics?

1:17:36 Ali:

Mechanics we are dealing with couple systems that perform inference over the systems to which they coupled. In other words, we're dealing with particular partitions in the sense of pristine's 2019 paper or the rest of the literature. Or we're looking at the systems that minimize their own surprising. When the systems minimize their own surprising, they must somehow know something about their environment. I mean, inferring something about the external state is the classical view of the FEP, at least as it initially formulated.

But this surprising minimization follows from a kind of synchronization between the internal and external states via synchrony map or sigma, which is simply the statement of things which exist reflect data about their environments, which is the other way of saying the about a statement as well.

1:18:55 And also things that are surprising are things that are not happen as we expect, like brain the laws of physics. In other words, it might look as kind of tautology for a system that would not, we will not expect for a system to behave in a way in a very surprising way. In other words, behave in a way that obey the laws of physics. But one of the main points of the Bayesian mechanics is to formulate this exact viewpoint by not focusing on a single trajectory of a behavior, but by somehow generalizing that statement to a whole fiber bundles of behavior, as they say in the gauge theory.

And systems in this sense can somehow be duly described instead of the traditional view of the FEP.

1:20:05 They can be described from the other way around by using the constraint maximum entropy principle. I mean, instead of looking at the system or agent from the inside and trying to somehow formulate its inference of its external states, we can put the observer in the external environment looking at the system and deriving the exact same correlation by just flipping around or inverting the sigma synchrony map. So that's one of the I believe, central ideas of Bayesian mechanics jacob.

1:20:57 Jakub:

I would just kind of summarize that by pointing attention to the image on the slide.

1:21:10 Daniel:

Action. I'll read the caption and you can provide an image meme analysis. The left side says, when the tree blows and shakes a tree branch, it is because the tree branch has inertia, but not enough to resist the force of a wind. On another, DAG DA, DA DA DA. And then on the right side, it says, when the wind flow and shakes a tree branch, it is because the tree branch reduces its surprising about the state of the

1:21:38 Jakub:

Yes. So these are essentially equivalent statements, one from the classical perspective, another from the Bayesian mechanical perspective. I think this notion might initially sound counterintuitive, which is why I think it's good to start talking about it now so that it has time to settle by the time we reach G theory.

I think that pretty much summarizes it.

1:22:22 Daniel:

Yes, it's pan inferentialist without being panpsychist per se. Ali also pointed to that extremely important theoretical duel between the free energy principle and constrained maximum entropy principle, which then was mapped onto this view from the inside, which is kind of a strategic agent trying to synchrony with external states or learn or reduce their surprise about external states as mediated by the blanket states. That's the view from the inside and the view from the outside, which brings us to the relationality Yaakup raised in the quantum space. The view from the outside is as an experimenter, and the fact that Dalton has shown that these two frameworks are dual to each other is provided some of the most important theoretical synthesis in the area.

Now, the three phases of Bayesian mechanics. So I'll bring larger a slide that was shared at Iy recently, the 2022 Coherence, and it shows the three faces of Bayesian mechanics.

1:23:33 Mode matching, mode tracking, path tracking. Those are the three faces that also are reflected in the earlier paper. And that was Gueststream 20 free point one.

In addition, here we see on the right is this chaos, and that is kind of a little bit beyond where we're going to go today, but it's an exciting direction. So does anyone want to describe the three faces? And then we'll head into the topics.

1:24:01 Jakub:

And papers have, like, detailed slides for each of the yeah, just to say.

1:24:20 Daniel:

That these are three different phases of basing mechanics and we'll talk more about them soon.

Okay, here are some topics. We're not going to talk about them at all. At all, but we left some open slides and space to add even more because they're topics that we want to talk with Dalton and you all about. So, supersymmetry. This was the citation in the paper.

Free energy principle and constrained maximum entropy principle as theoretical duels, Bayesian firmions bosons and ghost Fields and anything else that people bring up. We made it to the paper.

Let's review the roadmap before we really head off on this journey and to make this a reasonable dot zero and not go out too far beyond what we all understand here. We're just going to be really looking at a few key points.

1:25:22 And if either of you want to highlight something, please just raise your hand and highlight it on that slide. Otherwise, we're just going to take a brief stroll through the paper. So again, just raise your hand on the slide if you want to say something.

1:26:32 No more and no less.

Section two a continuum along on this direction and talks about different ways that mechanics can be specified around motion in gravitational Fields like moving objects and also approximations arising from fluid flow.

Section two B is the basics of Bayesian mechanics. Bayesian mechanics can be seen as an account with the laws of motion deriving from the FEP concerning how Bayesian beliefs that is, systems with beliefs such as coupled random dynamical systems which perform coherence over the things to which they couple behave under certain determinants of probabilistic motion. And this is another really interesting note. Much like classical mechanics, serves as an account of systems that obey Newton's second law by minimizing classical action.

1:27:32 Bayesian mechanics is an account of systems that engage in approximate Bayesian inference by minimizing surprisal. So the ball minimizes energy by falling. The candle minimizes Gibbs free energy by burning. Cognitive systems are minimizing free energy by way of minimizing. Surprising.

Otherwise they would fail to be that thing. To be continues on to to be or not to be. The pure physics of the FEP arguably dates back to two landmark papers in the literature a free energy principle for particular physics wrist in 2019 and Markov blanket information geometry and stochastic thermodynamics, which we didn't review here. The FEP has gestured at a new sort of physics. And that is what this work is recently bringing a quite exciting crescendo and examples of and here is a referral to the dual nature of FEP and constrained maximum entropy.

1:28:41 Continuing on in section two B, we see a little bit of an unpacking around the idea that the FEP is a least action principle applied to surprisal. Where the application of least surprisal principle to specific objects mathematical or determines the mechanical theory about these objects. So would be awesome for those. Who are familiar with Edocalculus and Stochastic differentiate equations, lagrangian mechanics, and path probability measures. Here we get to equation 15.

Ali, if you want to unpack a little bit what's happening here.

1:29:22 Ali:

It'S actually equation 15 is a kind of generalization of equation five for a modal path given by the equation twelve. And this equation is described as the general equation for Bayesian classical mechanics. Or we can see that as the most central equation by which all the other results or their derivations can potentially be derived, I guess. So here Q represents the position. But as a slight caveat here, because in most other literature, q is used for designating the recognition density.

But in this paper, cognition density is designated with R, so the Q is reserved for position, and obviously T is also the time.

In particular, in the limit lambda one, it goes to infinity. There is no uncertainty at all. And the most likely path under those constraints, the classical path of least action by construction is the only path we lend any nonzero probability to. So all the other classical and even quantum derivations can potentially be, again, be derived from this central equation here.

1:31:31 Daniel:

Great.

We have all the equations prepared to explore further. Now we're going to go into those three phases of Bayesian mechanics. So let's just start with mode notching. Jacques, do you want to describe mode notching?

1:31:48 Jakub:

Yeah.

So mode matching is the simplest case of Bayesian mechanics for stationary objects. The interesting thing that Dalton mentioned in the paper is that mode matching is only really valid for brief active states, implying that nothing ever really stays stationary. I would be interested to unpack this further. In the one and the dot two, how brief these timescales can actually be. Is it just instantaneous?

Is anything ever stationary? And how are different reference frames involved? But in the simplest case, we can. Mode matching considers objects that ant least in the approximate sense are stationary, like a ball resting on the ground, where the ball is essentially doing approximate Bayesian inference on its gravitational pull and on the normal force that is acting to resist that gravitational Bull.

1:33:05 And in the Bayesian mechanical sense, if it wouldn't do that, that would be surprising, and therefore it wouldn't be a ball because it would fail to act within the confines of the environment.

And therefore, in mode matching, Bayesian mechanics does reduce to, or rather imply mutant's first law, where for every applied force, there is a force of equal magnitude applied in the opposite direction. Or for every action, there's a action.

1:33:46 Daniel:

Great. Like why don't you ever change your mind I'm mode matching. What are you talking about?

I'm doing optimal Bayesian inference. I've Beren doing it all day. Okay. Mode tracking. So in mode tracking, we're going to now generalize from that ball resting on the ground to what setting?

Bali or Yakup.

1:34:16 Ali:

Well, yeah, in the mood tracking, unlike the case of mood matching, we have the target mode or the desired mode toward which the systems are tracking. So that's, I believe, the main difference between the mode matching and the mode tracking approaches.

But within the mode tracking, we also have two subtypes of mode tracking, one of which is the

1:35:20 But in the case of infinite mode tracking, we don't have some endpoints because it's a kind of analogous to a circular satellite motion by which we don't have the beginning and the and of the trajectory. Also, this kind of mode tracking has been described as an alternative term chasing. So I believe we can elaborate and unpack the details of that with Dalton.

1:35:58 Daniel:

Great.

1:36:01 Jakub:

I would just add to the infinite mode tracking case. One very interesting thing that Dalton mentioned in the paper is that when you have a constant path that you're performing, the infinite mode tracking on the state of the surprising of your states are always non zero, which I find really interesting, because for me, it kind of implies that there's always a certain level of uncertainty. But at the same time, this contrasts with the infinite case where for the case of planets orbiting the sun, there shouldn't be that much uncertainty about the path because you know you're going to follow that path Anil the end of time.

1:37:08 Just one thing that I found interesting.

1:37:13 Daniel:

Awesome. So again, just to recap, for those who are looking for those worked examples, in the mode matching case, we have a ball on the ground, the mass is not moving. We then have a situation where the equilibrium steady state, so to say, is not where the mass is. Now the center of gravity is in motion. In the mode matching case, the center of gravity is not in motion.

The two cases of mode tracking, where the center of gravity needs to be moving, cognitive center of gravity is terminal mode matching, which is equivalent to a ball thrown in a parabola where there's some defined endpoint, but it's moving along a path of least action towards that endpoint. And infinite mode tracking, where it's in a continuous dynamical or oscillatory acceleration process. And again, it's super interesting to think about what these actually entail cognitively.

1:38:17 I'm sure we'll get there. On to section seven.

So, section seven broadens the discussion from the state tracking framework of modes. Remembering this image where all of the modes, whether fixed mode or dynamics mode are regarding densities over states. Now we have densities over paths enabled by the gauge theoretic formalisms. So here are some equations and quotes related to path tracking. Anything to add?

1:39:00 Ali:

Yes, go ahead.

1:39:02 Jakub:

So I would just explicitly mention one point on the slide that the correlation that path tracking is

1:40:03 Daniel:

Ollie?

1:40:06 Ali:

Yes, I also wanted to mention that active inference is kind of subsumed in this type of path tracking systems. And also the initial formulations of FEP up to 2019, especially the 2019 Car Force Instance monograph implicitly deals with this path tracking approach, as far as I know. But somehow this typology of different kind of Bayesian mechanics is pretty new to these recent literature. And before that, there was a lot of confusion and misunderstanding about what kind of systems are we dealing with in each paper.

1:41:12 Daniel:

Awesome.

Then at the very end, there is a first idea of G theory. So, just like variational, free energy has F equation two five in the textbook, and expected free energy is G equation 2.6 in the textbook. Here we move from F free energy principle Friston to G to beyond. And we'll talk more about this with Dalton. But if anybody wants to add anything, they're welcome too.

1:41:50 Jakub:

I think one thread that was open towards the end of the paper was with the application of G theory to chaos, with the notion that we can use Bayesian mechanics to study systems that are dependent on the initial conditions. And even though this was so far purely describing the context of nonbiological entities, I think it's really exciting to see the potential applications in applied active inference where your initial belief states do influence your trajectory through the high dimensional state space.

1:42:52 And I think it will be very interesting to see how G theory develops in that way, and to see more connections between how we can use notions from asymmetry and chaos to studying cognitive systems or physical systems. Cognitively.

1:43:18 Daniel:

Awesome. Very well. Sajid. There are phase transitions or critical moments where when the ball falls on one side of the roof, it goes that way, and when it falls on the other side of the roof, it goes a different way. And there are just noticeable differences in terms of our psychophysics.

And this is really bringing the physics to psychophysics. And it's been quite a journey. If either of you have any penultimate thoughts, please provide them.

1:43:52 Ali:

1:44:13 Daniel:

Thank you.

1:44:14 Jakub:

Align jacob yeah, I think I made my over my kind of ending remark with the last comment, but, yeah, it's been an incredible journey so far and extremely fun experience to try to unpack this and in our discussions. And I look forward to unpacking even more and seeing how this thread develops.

1:44:55 Daniel:

Yes, thanks both and I'll for all the work leading up to it. And until next time.

1:45:03 Ali:

Thanks.

1:45:04 Daniel:

https://www.youtube.com/watch?v=dAtC-Enmc8M

First participatory group discussion, with the author, of the 2022 preprint "A Worked Example of the Bayesian Mechanics of Classical Objects" by Dalton A R Sakthivadivel.

Dalton Sakthivadivel, Daniel Friedman, Ali Rahmjoo, Jakub Smékal

00:28

Actinf Livestream.

01:09

Bayesian mechanics of classical objects.

04:41

Exploring the mathematics of nonequilibrium systems.

09:49

Bayesian Mechanics of Systems.

17:33

Bayesian Mechanics: Law of Motion and Inference.

22:49

Bayesian Mechanics and approximate Bayesian Inference.

32:40

Bayesian Mechanics and the Non Bayesian Mechanics.

39:50

Classical, Bayesian, and Quantum Mechanics.

48:26

Statistical Mechanics.

53:02

Unbiased Inference.

55:38

Quantum Mechanics and Bayesian inference.

1:01:52

Bayesian mechanics and quantum physics.

1:04:43

Quantum information theory and information theory.

1:06:10

Quantum chaos and the indistinguishability of particles.

1:07:48

Cognitive Science and the Instant Question.

1:09:45

Bayesian mechanics and information in physics.

1:16:50

Bayesian Inference, Physics of Beliefs.

1:23:43

Modes and synchronization.

1:26:57

Path Tracking and Moving Frames of Reference.

1:29:28

Bayesian Mechanics and path tracking.

1:30:47

Bayesian Mechanics: Reference Frames.

1:32:36

Markov Blankets and inference under the free energy principle.

1:37:45

Inclination to a physical theory of synchronization.

1:40:29

Bayesian Inference: The Dynamics of Blankets.

1:43:41

Markov Blankets and Multiscale Systems.

1:51:24

Progressive differentiation and the Markov Blanket.

1:56:14

A discussion of the paper draft.

00:28 DANIEL:

Hello and welcome everyone. This is ActInf Livestream number 49 DotI

This is recorded and an archive Livestream, so please provide feedback so we can improve our work. All backgrounds and perspectives are welcome, and we'll be following video etiquette for Live streams. Head over Active Inference Lab to learn more about the institute and how to get involved in projects such as the Live Streams and others. Okay, we are here in Livestream number 49.1. We are having our second discussion on the paper, a worked example of the Bayesian mechanics of classical objects in number 49.0.

Along with Markov and Ali, we did some background and context, and now the gloves come off, the curtain comes up, and we'll begin continue our discussion.

01:38 And we're really appreciative Dalton that you've joined today. Looking forward to how these discussions go. So we can begin just by saying hello and anything that we want to explore or discuss today, and then we'll just jump right into it. So I'm Daniel, I'm a researcher in California, and I think some of the questions that are really motivating me today is what is mechanical about Bayesian mechanics and how do we take concepts that have physical interpretations, like center of gravity or even some of these more atomic level terms that were brought into play?

How do we apply those kinds of terms and ideas to cognitive science? And I'll pass to Ali.

02:32 ALI:

Hello. I'm Ali. I'm an independent researcher from Iran, and I ant find enough words to express how excited I am to be here. Actually, we talk a lot about Dalton's work and how groundbreaking it is. And personally, I had immersed myself for the past several months in Dalton's paper, and for the past couple of months, we had fascinating discussions around this particular paper.

So I'm feeling kind of starstruck right now, and I'm very much looking forward to our discussion. And I'll pass it to yakob.

03:17 JAKUB:

Hello, I'm Jakub. I'm a student in the UK. And I suppose I'm also very excited to be here today and to discuss the different implications of Bayesian mechanics and how it's related to other areas in contemporary physics and how that can then be applied to cognitive evidence and neuroscience.

03:50 Daniel:

Awesome. So welcome. Thanks again, Dalton. Feel free to just begin where you'd like and bring us to the paper.

03:59 DALTON:

Of course.

Yeah, I guess I'll also introduce myself just in case there are people in the audience that don't recognize me or have a force to a name. I'm Dalton. I'm a researcher. I'm based at Stony Brook University in New York, where I spend most of my time in the Department of Mathematics and the Department of physics and Astronomy. I'm also at the Mercy's Lab, where I'm the mathematics and the physics of the free free energy principle.

It's a pleasure to meet all three of you. And thank you, of course, for the kind words. I think we can

05:13 And one of the interesting things to me is the idea that within cognitive science or neuroscience, there are some algorithms that have been developed over time that have been built specifically to cope with these kinds of problems, which are problems that we don't know really how to make sense of mathematically, even physically.

We're on the back foot.

But in neuroscience, then, the primary object of study is a nonequilibrium system. It is nonequilibria and understanding nonequilibrium phenomena in the brain. And so one supposes that the methods that have been developed over time in this area, just maybe by trial and error, or at least trial and error by the standards of perhaps a pure mathematician may have some insights.

06:15 Into math and physics in the same way that there's a very rich history of physics inspiring more advanced mathematics and then mathematics circling back and making physics more rigorous. I think there's a great opportunity to do that in biophysical systems.

And I think the free energy principle is a source of great inspiration along those lines. So with that metacommentary out of the way, one of the things that I wanted to do with this paper is to actually drill down on that point, because I think it's something that maybe gets lost in translation if you just read kind of traditional active inference papers that are all about modeling cognition. I think there's something on the other side of the aisle to be said about what do those models of cognition say about modeling systems that are cognitive, or what does it say about complex systems that are cognitive like and how can we make sense of those things mathematically that's in some sense the motivation for basic mechanics?

07:26 And that goes back to well, it goes back a long time. It goes back to probably Karl himself.

He mentions something like this at a couple of points in the 2019 monograph. But it was worth writing a paper specifically with the motivation that if we consider what's been written about the free energy principle so far, there's a very nice foundation for better understanding the mathematics and physics of coupled or nonequilibrium stochastic processes. And so that was the motivation for this particular paper. And in addition to building out the fundamental mathematics in the first few sections, it's then possible to contextualize all that work with a kind of nice work example of what does this Dean for some kind of simple systems? How can we actually take this foundational math and make it algorithmic again and then foreshadowing maybe even greater complexity in the very last section?

08:30 So, yes, a lot of this goes back to a paper that I co authored with a number of other people earlier in the summer called On Bayesian Mechanics, where it's proposed that complex systems have a kind of informational physics about them and that maybe the material physics or the maths for these systems is quite challenging in general. But maybe if you map these systems into the informational world, you can utilize new techniques and make sense of these kinds of systems by approaching it from a different kind of viewpoint. That is, I think, the strength of Bayesian mechanics, as again, Karl and others have construed it, is it is a way of talking about informational physics or the physics of Bayesian beliefs, the laws of motion on a statistical manifold, various ways of kind of couching that in more formal language. But again, that was the motivation for the paper.

09:31 And then as that gets developed, eventually there's a point where we really get into the trenches

I think those are really the kind of two aims that come together in some sense.

09:49 Daniel:

Thank you for the summary. Well, there's many ways to begin and start. Perhaps we could start with the context that we brought, which was thinking about this and you touched on some of these threads as well, such as the key literature and some of the history. Let's continue on in this context setting before we get to the formalisms and the worked examples and talk about the three kinds of theories, including what you mean by a theory and then the three non Bayesian mechanics. And that'll set us up really well to see where Bayesian mechanics comes into play.

So this was in that paper just mentioned On Bayesian mechanics of physics oven by beliefs. So what are dynamics, mechanics and principles? And how were you using theory and why was it so important to be clear about what a theory was and the distinctions amongst these three terms?

10:48 Dalton:

Yeah, of course. So in that paper there is this kind of trichotomy that gets introduced where we talk both about dynamics and mechanics and principles and disentangle them in a very particular way.

So we think about dynamics as a kind of observational thing and it's important to separate that from mechanics because complex systems as a science is very interested in dynamics. Can I kind of infer the laws of these kinds of systems just by modeling them using some kind of curve fitting or using some kind of set of canonical models that I know sort of fits this situation? But at the end of the day, yes, dynamics are mostly about the particular trajectories that a system takes through state space or physical space. And this is conflated sometimes with what I call mechanics in that paper, which is something a little bit different.

11:53 It is the laws from which these trajectories are determined.

So, for instance, dynamics systems, people, especially in pure mass really like the example of Ballard. So you send one billiard ball crashing into another one and you could talk about the trajectory that the ball takes and you could write down the equations of motion for this system and just add up all the forces acting on it and figure out what direction is this the ball that got collided with? What direction is that going to go into with what momentum and all of these things. But then figuring out that trajectory once you plug in all of these kind of boundary conditions the mass of the ball, the angle of the initial contact and so forth, the way that you can kind of computer all that information together that needs to come from somewhere.

12:55 And that's what we call or what I call a mechanical principle.

And this is not a distinction that is new to the literature. I'm not breaking new ground here, but I think it is one of those things that's not made sufficiently clear in the FEP literature or at least in the physical places where it's adjacent to physics. So mechanics are about the laws that give you those trajectories. So we know that the force is acting on one or another. Ballard Bull some together because of Newton's law of motion.

That's a mechanical theory. If I have F, then I get M times A and I can plug in F and I can plug in A and I can get a trajectory. But if I abstract away from those particulars, I get some kind of law that tells me, okay, how a trajectory is generated in the physical world. Abstracting one more step, we can then

13:58 And this is about the kinds of very fundamental laws that we know hold everywhere in the universe at a given scale. These are principles like conservation of energy. And this gives you the behavior of collisions or the principle of stationary action which actually gives you back Newton's law. So you can now chain these things together and say one ball hits the other one. It goes in this direction because if you summon the forces and you add up all the directions, you get a net movement.

And you can do that because these Millidge Bull minimize or at least make stationary their action. So their motion must follow this particular mechanical law. And that's the law that generates these trajectories. So the reason why this is mentioned in the Bayesian Mechanics paper is because these have, I think, been conflated in the literature previously because you have the idea of the free energy principle, which is a principle.

15:00 It's a thing that gives you back some kind of generative rule for the dynamics of specific systems.

And that is usually something to do with the motion of internal states on a statistical manifold in the sense of for instance, Thomas PA, Lansa Castle and Karl Friston article stochastic thermodynamics Markov Blanket and Information Geometry. I think that's the title anyway. So if you say, okay, the dynamics of a system whose parameter performs approximate DAGs in inference minimizes the surprising, then you get approximate DAGs and inference as a law of motion or the dynamics of some object. And this law is usually written as a particular gradient flow relation on the space of beliefs. So it tells you how to beliefs change as those parameters doing the coherence change.

And then if you add in progressively more details, okay, what do those internal states actually mean in the context of the system?

16:04 What are those beliefs about? These are the kind of boundary conditions that give you the trajectories the specific dynamics of the system. There's an interesting sense in which these boundary conditions are literal boundary cognition because understanding what's internal and what's external and being inferred is precisely the specification of a Markov blanket. So as soon as you actually give the system a very particular partition, as soon as you carve it up in a specific way, you start to get a sense of the actual evolution of a system as one might see it in the real world.

But this is I think separating things out in a formal sense like this is useful because it avoids skipping from step one, which is minimize variation of free energy or surprising. And then going straight away to this is how something like an active inference system does prediction and action. There are some steps in the middle that haven't really been filled out if you just go from A to B directly.

17:05 And when you begin to talk about the maths and physics collapsing things together like that starts to throw away some important details that actually do make a difference in the way that you tell the story.

17:21 Daniel:

Awesome. Ellie or Markov, anything you want to add in or ask there?

Yeah.

17:33 Jakub:

I would maybe ask regarding the kind of laws of motion of Bayesian mechanics, you mentioned

17:58 Dalton:

You could say that, yeah. I think at this point the distinctions gets very fine and so there is a place to usefully truncated. These are three different kinds of approximate Bayesian coherence.

And so they are three different kinds of motion under free energy principle minimization. And so this is kind of, I guess, a middle area between dynamics and mechanics. You've started to specify some things like am I doing approximate Bayesian inference over states or am I doing it over paths? But you're still lacking actual dynamical details about what do those states and paths mean. So this is maybe a middle area that blends the idea of approximate Bayesian inference as a law of motion under surprise minimization and actually getting down to the very bottom up this pyramid.

So if I were to put it somewhere into this figure, I'd maybe slot it in.

19:05 That's pretty much what I'm imagining is you have approximate Bayesian coherence sort of roughly up here. And then there are different expressions of that, just as there are different expressions of Newton's laws, depending on if you're in fluids or rigid bodies or celestial mechanics. So you can introduce even finer partitions than these three.

19:29 Daniel:

There's many places to go. One question is, what are these modes about? Who or what is tracking what and when?

19:42 Dalton:

Yeah. So this is kind of about the idea being approximate Bayesian inference tells you that systems match their parameters in such a way that they perform inference, right?

So when we think about Bayesian inference, we can talk about it as simply inferring the parameters of a probability density. So in the free energy principle, when you get approximate Bayesian inference, saying, okay, systems that are coupled synchronize certain parameters, this is Bayesian inference. And conversely, if you have that synchronization, you have Bayesian inference, or you have approximate Bayesian inference. If you're inferring the parameters of an approximate density, which is where you get into the factorization of the free energy functional that we are familiar with, where you have a variational density match to a joint density, but you can split it into the variational density match to a conditional density plus an extra surprising term that kind of measures how good that approximation is.

20:55 So this descends from that idea that you can deduce what a system is doing just by saying, okay, it's performing a proxy inference because that allows you to say its parameters are synchronizing to the parameters of the environment or of another system.

So that's what we mean when we say modes. In this case, a mode is just a parameter of the distribution. And it comes from some of Carl's earlier literature where he uses the LaPlace approximation. So specifically, we're matching the we're kind of fitting a Gaussian density to some arbitrary probability, and then the mode of that Gaussian is one of the parameters because it tells you, okay, where is the center of that density? And if you also get a sense of where the variance of that density is, now

22:06 This gets you back much of statistical physics, because it's all about how does a system reflect the statistics of another system probabilistically? How does this look? But this is kind of upgraded in Bayesian mechanics to noting that, well, that inference happens because the physical parameters of the system are matching the physical parameters of the environment, and that's where the probabilities come from. That's why we talk about beliefs. So when we say modes, we're referring to parameters that are fit for synchronization.

22:45 Daniel:

Excellent. Thank you. Yakka.

22:49 Jakub:

Since we have the schema on the slide there, I just wanted to ask, where do you think that the G theory formulation fits into this diagram? Because with G theory, there is approximate Bayesian inference, but it's not necessarily the city overstate. So is it another node directly from the Bayesian mechanics?

23:19 Dalton:

Yeah. So in this figure, the approximate Bayesian inference comma is a very specific thing that originally goes back to, I believe originally it's in a 2012 paper by Karl in entropy called the free energy principle for biological systems.

But certainly a much bigger deal is made in the 2019 monograph. And the approximate Bayesian inference lemma, as he calls it, is specifically about mode matching. Approximate Bayesian inference is a bit more general. So if you were to kind of slot that in somewhere in here, it would maybe be parallel to Bayesian mechanics. Because just like classical mechanics, the law of motion is Newton's laws.

For Bayesian mechanics, the law of motion, the thing that generates specific physical dynamics is approximate Bayesian coherence, or the law that when you do have synchronized systems, you can write it as variational free energy minimization in virtue of the parameters of the two systems matching up.

24:26 And that's the parameter that minimizes the distance between a held density and an observed density. So approximate Bayesian inference lemma is that result specifically. But that's more general. The idea of approximate Bayesian inference is more general.

And probably someone needs to write down a generalization of the approximate Bayesian coherence dilemma to path specifically to talk about path tracking. But once you have a path that fits the bill as a mode, and once you have two systems evolving together, tracking each other's modes or each other's paths, and if you have a probability density over those paths, you can now talk about approximation inference in the path setting. Now, whether has to do with G theory. G theory, the name and kind of the vision is actually due to Maxwell Ramstead, a colleague of mine also here in the Berseys lab. And he has suggested that G theory kind of lies in the introduction between a few different things that fall out of the path based formalism.

That's a specific example. I think more generally, path tracking deals with nonstationary systems very well because you're allowed to talk about now how does the density, how does the belief change in time? How does the mode of a single belief change over time to make a kind of modal path? And what are the marginals? If you slice up the density along that path, what do you get?

26:41 So you can talk about non stationary systems, you can talk about systems out of equilibrium this way because you can relate the free energy principle over paths to what's called the principle of maximum caliber in statistical physics, which is all about nonequilibria and entry production and nonequilibrium steady states. I think, as we have written about it, G theory is the duality between path integral and the FEP over paths or the duality between max cal and maxim caliber and the FEP overpaths. But I think that's selling it short a little bit because it's also the thing that brings in all these other ideas. And Stochastic thermodynamics is a really interesting one as well. Right.

Also falls out of the path based force very well, also does very well with nonequilibria.

27:43 So G theory is kind of this larger object that makes sense of why that column of Bayesian mechanics actually works and explains a little of the true power of the path tracking as opposed to mode tracking. Why are we interested in forgetting about states? And that's the explanation for that or the justification for that resides in G theory, which is supposed to explain why do all of these things just come out of the path based formalism? Why does it make sense and why does the FEP overpass lie at the center of a lot of disparate Fields, which I think is one of the real, very powerful statements that may be possible in the near culture?

Is the FEP actually canonical the theory of everything? In the sense that there are lots of approaches in statistical physics and Stochastic purpose theory that traced back to the FEP or the FEP subsumes or implies or something like this.

28:55 G theory is supposed to kind of plug Hinton that last column, but it's somewhat outside of the hierarchy in that sense.

29:05 Daniel:

Excellent. Thank you. Ali?

29:10 Ali:

Well, yeah, when I was reading about you theory, I thought it somehow relates to Rock Land's principle, which basically says that if an observer loses information about a system, the corresponding entropy in noninformation bearing degrees of freedom of the information processing system or its environment is increased because Landlord belief that information is physical. So he somehow put it in terms of a kind of thermodynamical point of view. But how does it fit? Or can G theory be viewed through the lens of Landar's principle, which I think is not a completely non controversial principle as well?

Yeah, that's an interesting question.

I think insofar as it does give you some technology to talk about entry production at non equilibrium steady state. So it does give you a way of saying, okay, if I'm exchanging with my environment, if information is flowing out and flowing back in, then there is some increase in the entropy. And with respect to things like control theory, this is pretty interesting as it allows you to talk about, okay, if the system is observing something about its environment, if it's constantly maintaining a steady state, so engaging in control, then you can talk about that entropically and you can talk about the irreversibility of processes, even at steady state. And there are things that connect to that, like the Crooks fluctuation theorem or Yosinsky equality and things of that nature.

31:15 So my guess would be it probably covers something like Landauer's principle.

In that context, talking about the energy required to erase a bit of information, say, is ultimately the energy required to insulate yourself from the environment that minimizes your surprisingly, it means the environment does not offer information to you. But that does take energy and sometimes quite a lot. So that's probably where that connects to blendhouse principle is talking about and quantifying the kind of cost of maintaining a mockoff blanket in probably entropic terms.

Great.

32:01 Daniel:

I think this points towards somewhere we may explore over this multiscale engagement, which is unconventional computing and low energy computing. For example, the often remarked upon energy expenditure of the brain compared to, say, a neural network operating on traditional computational architectures using many, many light Bull, many, many calories of energy versus the brain, which is able to carry out some tasks with seemingly low energy expenditure while other tasks it does not seem to be able to perform at all. I want to pull back before we go into the three non Bayesian mechanics and ask, what is Bayesian? What does it mean for something to be Bayesian?

32:55 Dalton:

Yeah, in my mind, Bayesian is about inference. It's about a particular method of doing coherence that gives you consistent, unbiased results and fits in very nicely with the rest of probability theory. In the context of Bayesian mechanics, it is the idea that the physics of material systems, or the material physics of complex systems, maps into a physics of beliefs. So you can talk about the parameters that are doing approximate Bayesian inference, or you can talk about approximate Bayesian coherence. You can talk about, okay, what are the beliefs parameterized by that mode doing and how does that reflect something about the dynamics of the system?

The reason why this is interesting is not just because it's a different approach to the problem and dealing with interacting systems and systems out of equilibrium is an area that does need new approaches because it is a very poorly understood area within mathematics and physics.

34:13 It still is. It has been for some time, I think. But it's also interesting because complex systems are informational. So there's some sense in which this brings us closer to the metal.

So it's not just a new view, it is the right new view, because complex systems are systems that compute and capture data. There are systems that have memory. So it's not as simple as even here's a new way

Understanding the dynamics of things like the brain is contingent upon understanding what the brain is doing.

35:19 And the brain is capturing and computing over data. It is storing memories, it is learning and sensing and inferring. So it's not just that it's a new view. It's really the right view because it gets to the idea that complex systems do things physically because they are doing something in informational space.

And the brain is a wonderful example of that. The brain is a couple of random dynamics system. It's coupled to its environment. So you can talk about this parameterization thing, this synchronization thing, but it's even more insightful than just that because the brain is doing approximate inference. So I suppose it's no coincidence that the synchronization of coupled random dynamical systems gets you back this idea because I think that is empirically, just based on observations.

I think that is as close to a physical law as one might be able to get at this stage in complex systems.

36:21 Theory is that things that synchronize do perform a fox of basic inference because things are synchronized, are things that are controlled systems or computational systems. So in that sense, I think it's right on the mark. And as I Sajid, it's interesting that this goes way back to trying to figure out things about the brain. It goes way back to Karl Fristin's original work on generative filtering and STM and these kinds of algorithms that were designed to make sense of what is the brain doing physically based on what we think it's doing inferentially right the relationship between structural and functional connectivity and the relationship between neural representations and neural firing paddles.

But it has become something massively more general because it is the right kind of math to talk about these sorts of systems. And that's in turn because these sorts of systems do this kind of approximate Bayesian inference.

37:25 So when you ask what is Bayesian about Bayesian mechanics? It is about the relationship between Bayesian beliefs and Bayesian inference and physical parameters representing something about the information available to that system or the statistics of a system coupled to that system.

37:50 Daniel:

Awesome. Just a few notes before we then go into the non Bayesian mechanics. One is from ecological psychology where many of our terms are drawn from, such as affordances. People have long pointed to the way that we use language like can you grasp it? Optimal grasp of ideas and so tangible and peri personal spatial ways of talking about ideas and cognitive processes.

And then, well, what is the first thing you want to know after you get optimal grasp? How much does it. Weigh. And you said it has become massively more general. Well, is that in grams or in what?

So I see this as part of the development of the physicality of cognition, in that the ecological psychology brought in relationality and action orientation, the pragmatic turn. And then now what about those objects? If we drop the idea, what happens? If we drop it from the discussion, what happens?

38:52 And then the second piece is a very interesting historical note about the development of complex systems and about the appropriateness of this kind of a formalism.

39:53 Let us go to the Bayesian mechanics.

So the non Bayesian mechanics are classical, statistical, and quantum. So however you'd like, maybe just on each of the following three slides, just what are classical mechanics? Statistical mechanics and quantum mechanics kind of steal person in the agreement and just what do they explain? What will they continue to be useful for? And how can we see them as special cases or adjacencies or however you'd like to frame it with respect to basing mechanics?

40:33 Dalton:

Sure. Yeah. So beginning with classical mechanics, I think is probably the simplest example. You have kind of the physics of very large, very slow things. Large is kind of a relative term.

Large compared to atoms, maybe, and slow compared to the speed of light. But nonetheless, this is a broad region of physics that describes things that don't have relativistic affect, things where observations commute. So it's non quantum things that are not noisy, so there's no probability that's not statistical, and things that do not require relativistic corrections, so things that are below the speed of light. When you have all four of those ingredients I think I listed four anyway, you have classical physics, or at least you have a classical object.

41:35 And the physics of that thing is classical mechanics.

So this arises from you may have inferred four limits of other kinds of physics. So you want to be now infinitely precise. This is the kind of no noise limit of statistical mechanics. It's the slow speeds limit of special relativity. And it's a very interesting limit of quantum mechanics that I can get into a little bit, but it begins to get a bit complicated.

Maybe I'll save that for the third slide. So, yes, but until then, I'll say there is a classical limit of quantum mechanics that you take a quantum field theory, and you can produce a classical theory out of that in a relatively well defined way. And again, I can talk a little about the nuances to that statement.

42:37 There are some. But regardless, classical physics is about large things, really.

The interesting thing is that all four of these limits kind of coincide to some extent when you have a very large system. So very large systems allow you to use the law of large numbers to kind of sharpen your beliefs about a system. So you can imagine this as placing greater precision on the measurement of your system. And that recreates sort of the no noise limit because you get more and more precise in your estimate of the dynamics of the system. Many body systems with very small objects are systems where you start to see quantum action.

So particles, like atomic particles, for instance, you begin to run into things, a regime where things are small enough that quantum physics becomes relevant.

43:49 And also large systems tend to move pretty slowly as just a general rule in what's called effective field theory, which talks about how one theory is a limit of another theory. And in particular, it talks about as you increase in scale, you get simpler theories. So I think we would probably all agree

One expression of that is kind of the momentum scale is inverse to the mass scale. So larger things generally have lower momentum, lower energy. Very small things whizz around at very fast speeds. They have high momentum. So once you start to talk about large systems, things begin simplifying in such a way that more often than not, you run into classical physics as a sufficient description of the scale of observation that you're at classical physics.

45:01 That's where it comes from. It is about Newton's Law. Classical mechanics. Newtonian mechanics, as you might call it, is about Newton's law. It says that.

Well, Newton's Three Laws, I suppose I should say. They say that every action has an equal and opposite reaction. So this is the idea that things that make so contact forces have, at the classical level, an equivalent force in the opposite direction. You can think of this as a kind of if you're familiar with sort of exercises in school in this area, you're often asked to calculate the normal force of something. The normal force is just what pushes up on me when I push down on something else.

So this is why I don't phase through the ground when I stand up is because there is an equal and opposite reaction.

46:03 I'm not only putting a force on the ground, but the ground is acting on me and keeping me up.

That's one of them. The other one is the very famous F equals Ma. It says that the force acting on a system is the mass times the acceleration of the system. And likewise, you can deduce the acceleration of the system by taking the force, acting on it and dividing out the mass. So this tells you, okay, how do we generate dynamics out of some boundary conditions?

Like what is the mass, what direction is the force acting in? Classical mechanics comes from what we call least action principle. And there are a number of equivalent ways of writing this. But this generalizes to what some people call lagrangian mechanics. And that tells you imagining what are the energies that those force came from, how does the system behave with respect to its energies?

47:04 And if you talk about stationary action, you talk about minimizing energy, then you can recover Newton's laws as a system accelerates along force gradients. And it doesn't waste energy by going any faster or going any slower. It does exactly what it is told to do. So it uses precisely the energy budget available to it. There's a very nice well, maybe I should say that my own paper, but there's a very lengthy exposition of this in the Physics Oven by Beliefs paper that we've talked about once already.

I think it's action two where I run through why is the analogy to classical mechanics even useful here? And it's because of the stuff that we talked about previously with a very nice dichotomy or dichotomy between principles, mechanics and dynamics. But anyway, more broadly than that, classical mechanics is a very good example of a least action principle because it's the idea that the dynamics of classical things comes from a particular scale appropriate, limiting least action principle.

48:17 Daniel:

Excellent. Ali or Markov, anything to add? Or we'll move to statistical mechanics.

Okay, classical descriptions. On to statistical.

48:34 Dalton:

Yeah, so statistical mechanics is a bit of an interesting one. Statistical mechanics is a lot broader than I

Probability theory is just maths. So anywhere you can use probability theory to describe some system, you can use statistical mechanics. And we know that this generality does exist because you can talk about quantum statistical mechanics. You can take the physics of very small, very fast things and use statistical mechanical methods. You can use probability theory and entropy in these things, and you can also go all the way up to black hole thermodynamics and you can do the same.

49:39 You can talk about so black holes are very large things, but you can still talk about the thermodynamics or statistical mechanics of black holes. So it's worth saying that we can talk about the noise limit of a particular kind of statistical mechanics, but then we need to be a little bit more precise about what that generates. In this case, I'm thinking of classical statistical mechanics. So it's the statistical mechanics of interacting particles or systems with microstates that relate to allostat via some kind of Gibbs correlation and things that have free energy, and in particular, Shannon entropy. So this is a little bit more of a narrower idea of what statistical mechanics is just because we need to constrain ourselves a little bit, even to get off the ground.

50:44 Otherwise we'd be covering way too much. But it is the case that if you take statistical descriptions of ensembles of objects and you become more and more precise and you get rid of the noise, then you can reproduce kind of classical equations of motion. And there are ways of doing that. One such thing is called mean field theory. So in mean field theory, you get rid of the noise in a system and you just say, okay, here is the trajectory of the system in the same way as we might do with classical mechanics.

I'm skipping some details there, and the analogy is a little bit more nuanced than that. But it's kind of a useful mental picture, I think. And one of the interesting things to note, I think, is what you've written here is that there is a principle that's relevant for statistical mechanics because statmac is very general, it's very mathematical.

51:51 It requires an equally mathematical principle. And so in probability theory, we have what's called the maximum entropy principle, which is just a way of designing probability densities around inferences that satisfy some mathematical deciderado.

So they should be consistent. They should be unbiased, they should lead back to Bayesian inferences under suitable conditions. And maximum is that thing. And we know due to well, work by James, but more recently work by people like Ken Dill, also here at Stony Brook, and before him, mathematicians like McParlin, woods, and Guilani. All of this is a large body of work that points to the idea that if you maximize entropy, you get the mechanics of diffusion, so you get the mechanical rules that generate mass action like diffusing particles.

53:02 Daniel:

Excellent. I just want to ask about one word which was unbiased.

53:06 Dalton:

So does unbiased Dean here, unbiased, I think you can think of it as avoiding overfitting. So one of the things that you can consider Max end to be is a recipe for doing inference that maximizes ignorance subject to some constraints. So if you have some known unknowns, then you want to incorporate those.

54:11 But either way, it is the idea that you don't want to introduce extraneous information into your inference because that extraneous information biases you in a direction that the data doesn't support.

That's really the idea behind Unbiased. And one of the things that James did. And not only James, but also Shannon before him, who worked on the probabilistic aspects of this. And then after James and Shannon SAFRON Johnson, who also were probability theorists and worked on Max and Axiomatically. Not like James, who took it more as a physical rule for a long time and then got into the probability theory of it.

Either way, all of these people are able to justify with rigorous proofs that maximum entropy is the best way of making unbiased inferences.

55:18 And there's lots of bit of show on this. Those are our three useful names, but there's a lot more due to Ariel, Katiecha, I already mentioned Ken Dill, Adam Giffen. Lots of people have taken an interest in this area. Rightly.

So I think.

55:38 Daniel:

Awesome, we're going to keep moving to now quantum. And then already many of the seeds that bring us to Bayesian are planted. So quantum, how did it come into play in your work?

55:54 Dalton:

Yeah, so quantum mechanics is, I think, qualitatively different from classical and statistical physics.

It's about very small things or very fast things. And as I was saying, effective field theory tells us these things usually go together.

And it talks about kind of when you get things that are not classical. Well, at least it started as when you get things that are not classical. What do you need to add to your theory to make the right predictions? So quantum mechanics began as a kind of modeling effort.

It grew from what we might call semiclassical physics, which is just about quantum correlation to classical stuff. It grew from semiclassical physics to its own genuine branch of physics in and around the suppose, certainly the early 1900s.

57:00 Anyway.

So one of the things that becomes relevant is probability theory, because quantum mechanics, you may have heard about Heisenberg uncertainty. It's about the fact that measurements do not commute. So the order that you do a measurement in matters, a consequence of this is that there is always some inherent uncertainty when you measure socalled conjugate variables, which are just things that fit into the theory as noncommuting pairs. So you measure two noncommuting Parr, there is some uncertainty if you measure one precisely. You can't measure both precisely.

And moreover, there's a trade off. If you measure one with infinite precision, you know absolutely nothing about the other one. If you try and play half and half, then that's what you get.

This doesn't come out of nowhere, but it is one of those things where it just happens to be right because it's so elegant that it wouldn't make a lot of sense if it weren't much like, I guess, the coincidence of synchronization and Bayesian inference in complex systems theory because non commuting variables gives us all of the rest of quantum mechanics the stuff that we really know and love and also is a relatively well defined way of getting back classical physics. Because all you have to do is take the theory and make things commute, and then you get classical physics back.

I'm brushing some difficulties under the rug, as you might imagine.

59:04 It's not that simple, and technically it doesn't work, but it sort of does. And if you're interested, I guess you can look into what's called defamation quantization, which is exactly the idea that if you take a classical system and you deform it in such a way that things no longer computer, then you get that quantum physics, but you can't really do it the other way around. There's a bit of subtlety to the other direction. Nonetheless, that is one route to making quantum stuff, classical stuff.

Another route is just focusing on the probabilities. So because of this inherent uncertainty, quantum particles, their equations of action, have what we call transition attributes, which gives the probability of moving from one state to another. But again, nothing is certain in quantum mechanics.

1:00:05 If you, however, make it certain mathematically, you can go in and just take the no noise limit more properly. You should do something called Wick rotation first, which just allows that limit to make sense.

Although, yes, you should do that first.

If you do that, you take the kind of no noise limits, then you get certain state transitions. And this just gives you back a classical dynamics system that you know where it's going once you have the equations of motion. And this is the route that I take in the paper because it fits very nicely into the path integral formulation in a way that kind of just makes things make sense. And one of the nice things that I then go on to say is if you have a parameter sitting inside that path intergroup, then you can make sense of why classical physics comes from the noise limit by writing it as a Bayesian mechanical problem.

1:01:07 You can write about synchronization and get back the Bayesian mechanics of classical stuff just by doing this very well defined procedure.

This is something that already exists in physics and is fairly uncontroversial.

That's what you get in quantum mechanics. It's about small stuff. It's fundamentally probabilistic because there's fundamental uncertainty. And again, this traces back to empirical facts.

I think that about covers it. I don't know if I should have said more or if you have other questions. I think that's sufficient at this bench. Classified oh, it's great.

1:01:48 Jakub:

Jacob yeah.

I realized the paper dealt mainly with Bayesian mechanics for classical objects, but do you see Bayesian mechanics being applied to non classical phenomena like quantum tunneling or entanglement, which cannot really be explained in the limit of large numbers. And then also second question, which is kind of on the intersection of quantum mechanics and statistical physics. Is there any

1:02:31 Dalton:

Sure, well, those are really good questions, I think. Yes, there is probably an idea of quantum tunneling that could be achieved maybe because quantum tunneling, if you're a physicist, this is something that you're familiar with on the nose.

If you're a mathematician, this is what you would think of as an instantan. So instantaneous solutions to the equations of motion of a quantum field theory are tunneling dynamics. So the idea becomes, okay, can we describe instantaneous solutions using Bayesian mechanics? And the answer is I don't know. But it seems like it should maybe be possible because there is at least an understanding of where points A and B are, if not how to get from A to B.

But that is something that would be interesting to do more work with.

1:03:37 And more generally it would be interesting to think about quantum physics through the Bayesian mechanical Heins just because you do recover this classical limit of the path integral and morally path integral quantization should be equivalent to things like defamation quantization and geometric quantization and other methods even. And actually one other one is worth saying. There's a thing called Stochastic quantization which begins from real valued probabilities and then makes quantum stuff out of that. And the Bayesian mechanics as it is construed today is very close to Stochastic quantization in a few very key senses.

So one suppose it should be possible and that would be nice that's the answer to one question should be, but I don't know, it would be cool.

1:04:43 As far as entanglement and other kinds of information theory, I actually don't know very much about this. Quantum information theory is something that is relatively new and a lot of people kind of in and adjacent to things like condensed matter theory are very interested in this. But I am behind on the literature. I think one of the things that does kind of lend itself to information theory in general is the fact that Bayesian mechanics has these connections to maximum and Bayesian coherence and these are of course ways of talking about information and information theory.

So yes, my thought is something like entanglement, which has information theoretic undertones, should also be possible. But again, I don't know initially what precisely that would look like. There is some literature out there that has to do with the free energy principle in the context of information theory.

1:05:49 I am thinking of work due to Karl James Blazebrook and Chris Fields. They've published a lot of work in this direction, which is also something I'm not totally familiar with.

But again, it seems like a very rich area to eventually pursue connections in. Great.

1:06:10 Daniel:

And then the second question was about indistinguishability of particles and then Ali?

1:06:16 Dalton:

Yes. Okay.

Yeah. So I suppose you're thinking of passing to these kinds of bosonic field theories where you just pack a whole bunch of equivalent field states into your Fox space and see if you can make that make sense. I think you may notice this when we get into the super asymmetry results, is there is a

1:07:19 So, yes, there is a reason to distinguish between the behavior of the particles in each theory. I think the precise nature that will become clearer once someone actually knuckles down and does a Bayesian quantum mechanics where we'll be able to couple directly to that kind of idea.

1:07:47 Daniel:

Awesome. Lot of fun topics. The tunneling.

Do we have to visit every belief on the way from A to B or as it sometimes can seem, are we in one position and then we are in a different cognitive position? All different kinds of experimenter, experimented questions in cognitive science, even potentially collective thought and ways of communication in terms of these formalisms.

1:08:20 Dalton:

Yeah, and the instant question is pretty interesting as well because it talks about, okay, if we have a system with multiple classical minima. So if we can say, okay, there are multiple optimal based in beliefs, instantaneous are the things that zip between those minima. So it's a qualitatively different way of thinking about dynamical systems.

It's not a single minima and it's not a single classical trajectory. It's multiple minima. And it's almost like phase transitions between the two. So certainly that's interesting from the point of view of physics excuse me, from physics, but tracing it back to something like cognitive science thinking about, okay, what are the sort of phase transitions between our beliefs? And can we actually access other phases?

1:09:23 Like do those instantaneous solutions actually exist and do they describe some kind of zipping between maybe generative models or perceptory regimes or something of that nature? It's very kind of nebulous, but it's a provocative question.

1:09:41 Daniel:

Excellent, ollie?

1:09:45 Ali:

Well, I was on the understanding that as we go from classical to statistical and ultimately to quantum mechanics, the role of information and uncertainty in describing and formulating the dynamics and mechanics of the physical systems becomes more explicit. So is it a correct assumptions to say that Bayesian mechanics somehow aims to put information back in the game and make it equally explicit through all of those mechanics?

1:10:25 Dalton:

Yeah, absolutely. I think that's a good way of thinking about it. Right.

The reason why Bayesian mechanics is so general, much like statistical mechanics, is very general, is because it's just about information. And lots of things have information. Even at the classical level. We

What Bayesian mechanics allows you to do is actually keep track of how does information change between these different scales which is one particular payoff that I think makes it very valuable.

1:11:26 But not just Bridging scales, also applying to many different scales because lots of things do have information. Information is just a mathematical apparatus that we can use to describe lots of things. So if that's all that your physics is built on then it will be by coherence something very general.

1:11:48 Daniel:

Awesome.

The way that it's coming to me today is in classical mechanics, especially once we understand these limits, which classical mechanics is like a point within a broader space of physics or mechanics, we get principle of least action and stationarity and laws of large numbers, not unlike the central limit theorem in statistics and a lot of the Esoteric Gaussian statistics. In statistical mechanics the probabilistic nature becomes formal. For example, in the Billiards case in classical mechanics you might want to do statistics across many slightly similar billiards games. And so at that point you could either do the plug and chug frequentist statistics or at some point you're going to want to think a little bit more broadly about the distribution of Billiards. And then Quantum especially makes the relationality and the modeler modeled bioelectric formal because just by doing statistics you're already in an area of explicit relationality map territory distinguishing.

1:13:06 And then Quantum takes that to another level. And could it be said that with Bayesian we're even going a layer deeper into the modeler's approach to the system? Where do you see this?

1:13:28 Dalton:

I think so. The idea would be eventually we introduce an actual idea of information which naturally kind of depends on the observer or the modeler because information is kind of modeler dependent.

Information has context, it has contingent on observation. So when we start talking about surprising and the dynamics of beliefs and inference all of these are very explicitly putting the modeler back in the situation. And that may be in the very metaphorical sense of a system synchronizing with its environment. It doesn't necessarily have to be a cognitive observer or a panpsychist kind of modeler. I don't really think there's limit for that within the maths.

1:14:29 But the point is that the maths works with or without those assumptions. So in a sense it's actually agnostic to that. And you can conjure an image of a modeler that is pure metaphor just talking about synchronization. However, the language is pretty instructive and it does relate back to the idea that lots of systems have and can culture information. Maybe in a very trivial, cognitive, not consciouslike sense, but nonetheless, they do capture and synchrony to information and therefore they do model and they do coherence.

Great.

1:15:17 Daniel:

1:15:22 Dalton:

Exactly.

1:15:23 Daniel:

If a tree falls, does it make a noise?

1:15:26 Dalton:

Yeah, I think the answer would be it depends on what's synchronizing to the tree. Right? If the tree falls on okay, this is going to be a pretty grim example, I guess, but if a tree falls on some sort of small woodland critter, then, yes, I think the tree definitely fell because the statistics of one thing synchronizing to the other. One would say, yeah, pretty unequivocally, the tree just fell. But if you're not there, you're not synchronizing to the tree.

And so that information has no meaning to you whatsoever. So it is very much about, as you've written, modeler independent information in a very mathematically rigorous way.

1:16:08 Daniel:

Really powerful, and also connects to a lot of qualitative and contemporary ideas. So it's really exciting to think about where and how Bayesian mechanics can be applied. This brings us as we head into the Z score of plus one downhill on the gaussian of the dot one into the paper itself.

So we'll pause Ali and Jacob if you have any questions. Otherwise we're going to go to the roadmap and have some overview notes on the paper and its structure. Does that sound good? All right. So part in the meme, but here's the roadmap of the paper, the sections and subsections.

So maybe just the general comments. What did you include in the paper? What did you not include in the paper? Why did you structure it, how you structured it?

1:17:11 Dalton:

Yeah, absolutely.

So the structure was kind of meant to reflect, I think, an unmet need in the literature, which is both a single place for all of these results to be reviewed, and then once that review has been done, an application of all those results. So organize everything and then use it in a kind of insightful way. And having all the rigorous stuff in the beginning makes the application make sense and having the application or provides context for all the very rigorous stuff at the beginning. So to do that, it's kind of split almost down the middle. You have the sections one through four, all the foundational stuff, and then sections five, six and seven are the actual applications.

So I began with a very brief introduction, just motivating precisely this.

1:18:19 Here are the questions that we're going to answer. Here's how we're going to answer them. Here's why it even matters in section two, I just very briefly review classical physics to set the stage for some of the stuff that we've already discussed. Then I talk about Bayesian mechanics itself.

And two B through 2D are fairly long because this sets up all the basic machinery we begin with. I believe, to begin with, we talk about. What does it mean for Bayesian mechanics to be like classical

And then in C and D, these basic ideas can be used to figure out, okay, what does it mean then to minimize surprising?

1:19:22 How does that matter to Bayesian inference physics of beliefs? Physics by beliefs is then inverting the story and talking about, okay, so we know now that systems, when they minimize their free energy or minimize their surprising, they synchronize to their environment. So you can write this nice story about parameters. Can you do it the other way around?

Can you begin from the I think I gave that in the wrong direction. So when systems synchrony, they minimize their French. So you can read this as Bayesian inference. Then I ask, okay, can you do this the other way around? Can you begin from Bayesian coherence?

And can you get the dynamics of parameters, which is just kind of flipping the story, but it involves a bit of work to actually make it follow through. In the end, however, it does and the relationship between the two. So I say physics of beliefs because one is taking the motion of parameters and relating to the motion on statistical manifold Bayesian inference, physics by beliefs, to say, okay, if we begin with some information theoretic idea of Bayesian inference, do we get back the mechanic subsystems carrying those beliefs?

1:20:38 That relies on some work that I did earlier this year which espoused a kind of duality between the free energy principle and maximum entropy. So using that as a kind of technology, you can flip the story and say, okay, if I start from an influential principle, can I get physical stuff back?

Whereas the FEP I would think of it more as if I start with physical stuff, can I then understand the beliefs? They are two sides of the same coin and on the nose, it's a very trivial symmetry between the two. Of course, it takes a lot more work to make it formally make sense, but in the end it does. So that's section two, section three moves us into the first idea of actual results in the papers to say, okay, so if I have a classical system doing Bayesian inference or approximate Bayesian coherence, what does that look like?

1:21:44 And does it look like the free energy principle?

And then conversely, if I have an inferential principle or if I have an informational physics, can I use agent as the dual to the FEP to get back the physical mechanics of this classical object? And in both cases, the answer is yes. And at the end of that section, I give an equation that does precisely that. It takes the idea of mode matching and says, okay, here's how probabilities behave when you do mode matching. And conversely, here is how modes behave when you minimize the free energy of those probabilities.

So in section four, I then talk about, okay, does this actually make sense in a physical setting? Does it tell us anything insightful? Or is it just a tautology that if you build in a classical mode and then take the limit to the mode, then you get classical physics?

1:22:49 If you phrase it just like that, it doesn't seem very remarkable. But for the reasons that I described about path integrals and the classical limit of the path integral, it becomes a little bit more subtle.

And so we can actually derive something kind of interesting from the idea that classical stuff is the mode of quantum stuff. So in the classical limit of quantum mechanics, systems that do approximate Bayesian inference exhibit classical physics. I think that's really the payoff of that section. And so it

So once that's done, we cool off a little bit, and we just do an example of what does it mean to do mode matching.

1:23:52 This is simple enough to formulate, and you can see in this case, the mode. So mode matching is about stationary modes, and it makes sense to talk about the classical physics of something at Brett. Now, things that are at rest don't move. So synchronization in this case is matching a mode to a stationary environment.

When a force is not acting on you, you don't move. And this requires very little maths. And at the end, one of Newton's other laws pops out that objects in action stay in motion, objects at rest stay at rest. So you get that back from section five, from action six. You can talk about modes that move.

Well, you can talk about systems that move. And there's actually a finer distinction in there that I precipitated just saying, which is, in one case, you can talk about a system that moves towards a mode.

1:25:03 So a system that tracks a mode but eventually finishes in a stationary place. And you can also talk about a system that chases a mode. So we call this infinite mode tracking, or what you could think of this as mode chasing.

You could think of this as a primitive form of path tracking. It's just the idea that things that go around in a circle, you can look at it one or two ways. You can look at it as an object. And the example I use is satellite motion. So the classical physics of celestial bodies say one thing orbiting around another.

You can either talk about this as a mode that is being tracked, that is constantly in motion, so you get infinite mode tracking, or you can talk about this as path tracking, where the path is the circular path around the object, and what we track is just that path.

1:26:06 And that is what is in seven A. So I say in six b. You can talk about this example as infinite mode tracking, but it's kind of ugly. It doesn't work very well.

So this justifies going to path tracking instead, which is a much more elegant picture conceptually. It makes a lot more sense. And one of the problems specifically with six B is that the idea of minimizing the surprising of a mode becomes kind of difficult because the system is nonstationary, the mode is constantly moving, and so the surprising is constantly fluctuating. But when you talk about the surprising overpaths, it's much easier. You can say, okay, we are actually genuinely minimizing the surprise of paths because we are picking the path of least surprising.

One thing that I didn't include in this section, which is possibly interesting, and I don't know, one of the nice things about pre prints is they are to some extent living documents.

1:27:10 So I could come back and add this in if I was so inclined, and in fact, I might, is the idea of moving centers of mass. So path tracking combined with some kind of moving frame of reference. The reason why I didn't include this is because the math for that is not quite worked out yet. But since then, Lancelot Costa and others in a paper that is probably about to be released.

It's coauthored between myself, Lancelot Costa, Karl Friston, Thomas Par, Conor Heins and Grigorios Pavliotis. So all of the big mathematical minds behind the last few years of the FTP, I think I named all the names. If I forgot anyone, then you'll have to excuse me.

1:28:10 There's some work in that preprint, or that paper to be preprinted, that formulates path tracking in the context of moving frames of reference. So not just moving modes along a path, but also moving

So keep an eye out for that because there will be something about moving frames of reference in that paper. And I may decide to go back and add something like if I'm orbiting a body that is itself in motion. So if the center of mass that I'm orbiting is itself orbiting around something else, what does that look like from the perspective of the thing in orbit?

1:29:15 That's an interesting case. It's something that I didn't include because it was still that I think there wasn't an elegant way forward with that.

Now there probably is. But carrying on seven B is now relating the idea of path tracking. So the idea of a surprising overpass, relating that to the path integral approach to Bayesian mechanics and extracting some insights from what it means to be a path integral. And one of the things that one is allowed to do in that context is to then develop a story about classical chaos. And I think we have probably some slides later about that that deserves a much longer conversation.

But the idea of that section is to say, okay, we've done all this arguably pretty trivial stuff.

1:30:16 Now, what about interesting systems like systems that exhibit chaos? Can we actually describe those things using Bayesian mechanics? And the answer is we can. And it comes out of the path integral description in the nice way that we have gestured at with the name G theory.

1:30:42 Daniel:

Nice. Thank you, Jacob.

1:30:47 Jakub:

I was waiting to ask this a bit later on, but since you mentioned reference frames, I'm wondering what different sorts of coherence frame Bayesian mechanics deals with, especially in connection to recovering classical mechanics from Bayesian mechanics. The way I understand right now, reference frame is basically imposed by the Markov blanket. So when we're talking about the free branch performing inference over its environment and being shaken by the incoming wind, that's from the reference frame of the tree. How would that be different if we considered our own reference frame looking at the tree? Could that still have a formulation within Bayesian mechanics?

And also, how could this relate to multi agent systems? Where we have the classic example that comes to mind is clock synchronization, where clocks, pendulum clocks initially start out of phase, but over time go get in phase.

1:32:02 I think there's a lot of different ways to partition that system. One clock is performing inference over the other, is performing inference over the other. But then maybe we can also treat it as a couple system altogether where we consider both at the same time.

So I'm thinking there might be some equivalent of like and inertial reference frame in Bayesian mechanics versus an inertial one given by the Markov blanket on that specific system. So it would be interested to hear your thoughts on that.

1:32:33 Dalton:

There's reason to believe that that kind of multi scale self organization, that multi scale patterning behavior, that multi scale separation and being able to infer not only what my neighbors are doing, but being able to infer what the scale above me is doing. There's reason to believe that that is where self communication comes from under the free energy principle. And one of the reasons to believe that is work by, for instance, Mike Levin in the context of the cognitive nature of developing cells, right?

1:33:42 Cells that are in a kind of soup of things. How do they know to develop into tissues, there must be some kind of notion of Friston blanket, not only knowing what am I in relation to others, but what are we in relation to a larger scale other.

So that's very important. Nesting blankets. Another really good example of this is in paper by Maxwell Alex Chance, some other people that I don't remember offhand, so I apologize, called neural and phenotypic representations under the free energy principle. And it's exactly the same sort of thing. If you have a soup and they know something about themselves and also something about something at a higher level, then you get self organization.

So it's not just about kind of self organization at the constituent level, but it's knowing something about the pattern that one is organizing into.

1:34:56 And these are two good examples of that. There are lots of others. So one imagine the arbitrariness of the Markov blanket is important because it allows you to nest things more generally, it allows you to change context. And, you know, the context of information is kind of observer dependent.

So in a way, you do want to be able to introduce kind of arbitrary frames and get different kinds of context for a given observation set, right? You want to be able to reassign self and other and still get approximate Bayesian inference. This is what we would think of as a gauge theory. It's asymmetry at the level of the system that is not reflected in the physics of the system, by which I mean you can make free changes at the level of the system that don't change the physics of the system.

1:36:06 So in this case, it's the idea that we can change a reference thing.

We can change the context of an inference, but it shouldn't change the idea that systems do approximate phase of inference, much in the same way that we can change the way we label coordinates in general relativity. But it shouldn't change the idea that gravitation is the curvature of space time in some suitable sense that has to do with metric tensors that I won't talk too much about. So something like that is absolutely, I think, not only kind of useful, but is absolutely essential to not only making basic mechanics make sense. It would be kind of suspicious if coherence just fell apart. If you redrew the boundaries, especially given our conversation about the scale friendliness of the SAP, it should apply and reapply, but also that application and reapplication and contextualizing inferences within inferences is kind of right.

1:37:10 Now, what is reflected in the literature when we really think about, okay, how does self communication work in these situations, and how does individuation work in these situations, or how are patterns formed? And I think there's lots of work in this direction about reference frames and the contextuality of information outside the FEP as well. And I happen to be familiar with very specific literature about this in category theory, but I'm sure it's more general than that. So you can talk about

In the case of synchronizing pendulums, you can imagine, okay, maybe the pendulums do infants on each other, or maybe they do inference on the kind of if they're on some sort of cable or moving beam, maybe they do inference on the beam and they synchrony with the beam, and therefore they synchronize with each other.

1:38:29 That's one frame the other forage is one kind of looking at the rhythmic motions of the other one and just matching up like that. In both cases, you get inference. We probably prefer one reference frame or another, but both are in principle, mathematically valid, even if they tell kind of different physical stories about what's being synchronized to. And the example of half tracking in a moving frame of coherence is interesting as well, because if you think about something like the Moon orbiting the Earth, you can zoom way out, and you can look at it as the Moon spiraling around the Earth, as the Earth goes around the sun.

But you can also pick a reference frame where the Earth is stationary and the Moon is just orbiting around the Earth. So this is the relativity of motion, right? Or if you want to imagine sitting in a train, it looks like the outside is moving and you're stationary.

1:39:38 That would be mode matching. You're not moving, but from the perspective of the outside, the train has just gone past pretty quickly, and you're in the train, and so you're moving, but from your perspective you're not.

So the relativity of what is being matched to is an important consideration. For those reasons, just to produce a consistent theory, we have to acknowledge that we can freely assign Active Inference. The important aspect is that we get the same inferences back, or at least we get inference. They might not be the Active Inference if you wrote them down. They might be in different coordinates, so to speak.

But at the end of the day, you should still get baited inference. Now, I don't remember your second question, so you'll have to ask it again.

1:40:38 Jakub:

I'm actually not aware if there was a second question, but I do have a follow up question to your answer. Since you mentioned nested Markov blanket.

1:40:53 Dalton:

I'm.

1:40:54 Jakub:

Just wondering whether in the formalism of Bayesian mechanics, we can also admit a kind of dynamics on the topological structure of of hae Parr, the blanket itself. Because in the case of cells forming other layers, intuitively, it seems to me that it's a kind of discreet way of thinking about how we're adding an extra layer of the Markov blanket. And maybe the mark of blanket initially admits some non integer index connected to work on the week mark of blankets and then it evolves over time to form into actually statistically significant Markov blanket. But perhaps there might be also a way for having just one Markov blanket that evolves through time and that might also change active inference lab I'm wondering whether the dynamics of particular blankets can also be taken into account in the path

1:42:13 Dalton:

Yeah, so there are a couple of interesting things there. For one thing, the idea that perspective matters, the idea that you pick a reference frame and carve up your environment that way does kind of go back to this question of how do we understand blankets forming in developing cells, say? And the idea would be that blankets have characteristic scales. The reason why we see something like a stone in nature and not a lattice of crystalline molecules is because at our level of observation, the blankets that allow these molecules to be self organized is completely meaningless. But what is interesting to our level of observation, our kind of canonical reference forage is the stone itself, the blanket around the stone itself.

1:43:16 It's the stone's blanket. It's not the blankets that make the molecules that make the stone. So yeah, eventually we would want a much more complete theory of individuation that covers not just dynamics blankets, but Friston blanket and blankets with perspective and things of that nature. The perspective based idea is an interesting one force me, because it allows you to talk about things like star coupling at certain levels. And if we acknowledge that the Markov blanket is coming to a blanket store in the area yeah, exactly.

If we acknowledge that the blanket is somewhat arbitrary, then we're free to say that any system with enough couplings has a blanket at some scale. Because the kind of multiscale systems in physics that we're interested in at some scale are sparsely coupled.

1:44:21 Probably not every scale. And certainly within a blanket there's not sparse coupling given a particular reference frame, because given Active Inference frame of myself looking at the stone, looking at the stones blanket within that blanket, I would want to see the stones molecules coherent in a way that is not sparsely coupled. Otherwise I wouldn't see things.

But then at the level of the stone, it is sparsely coupled. So this kind of arbitrariness allows us to actually do the carving up in a very interesting way. As for dynamics systems, perspectives on Markov blankets, I think this is also possible. I am working on something right now that takes the whole story about physical boundaries and conditional independence and writes it in terms of random variables.

1:45:22 So you have a whole suite of possible blanket states and you can look at blankets kind of flickering on and off, or blanket states occupy different states over time.

This is not nested yet, but it's one step towards that direction where you can think about how the blanket at a higher level turns on or off given the dynamics of its constituents, whether they're cohering or not. So yeah, maybe that answers your question.

1:45:55 Daniel:

This is a great topic to chill on for a few more minutes in our final bit of the dot one. There's really a lot here. I'll just give a few dot one then I'll be happy to hear your perspective as well.

You even discussed it as scale friendly, but it's almost like a one and a half layer model and that is actually preceded by even simple Bayesian hidden state, observed variable distinctions, expectation maximization, just partially observable. Bayesian models in general under an interpretation where observables are happening at a given scale of a system of interest and a hidden phenomena or a hidden cause is at a higher level of organization, connects the sort of multiscale systems approach with a self

1:46:57 There's the nest mates interacting laterally and then there's the real or as if colony level organization. Another point I think it's really interesting to pull out and explore is you discussed how important it is to be able to redraw blankets and still get coherence.

It made me feel that there has to be some kind of a locally distributed local sense making process such that potentially a vast range of partitioning can also remain valid. Like you can think of different metaphors there and that potentially the blanket provides exactly that partitioning. Surprise, surprise. And then moving towards all these features that had been in the expectation seats at the math conference, dynamical nested multi perspective systems.

1:48:01 And the way that some of these formalisms are pointing towards an integration that's quite far out in some ways, yet also may bring an intuitiveness to a lot of the ways of talking about different physical systems, including the physics of cognition.

And as far as nature at the joints, perspectives would be one, not the only one, but one of those joints, or sparse connectivity or factorizabilities various ways of thinking about it, but multiple entities encoding in a multiplexival multiscale inference question. It's like two people looking at the boat. They might disagree on how to partition different parts of the boat or the boat from the water, but at least their perspectives and their communication interface with each other and their observation inference interfaces with the boat could be specified.

1:49:10 And so then it could be like my map of me, my map of you, my map of the boat, your map of you, your map of me, your map of the boat and then there's a conversation with all six of those features instead of us only looking at the boat. And you did it one way, I did it differently and that's the end of the discussion.

So I think it's going to open up degrees of freedom in perspective harmonizing that wouldn't be classically understood and that will be seen as extremely nonlinear and unconventional behavior. And it's just from seeing what that is.

1:49:52 Dalton:

I agree. I'll take this opportunity to point out there are other people in the virus lab who are thinking about that kind of question. How does collaboration and information synthesis and kind of agreement or goal emergence, how all these things fit into Bayesian mechanics?

So people like Maxwell and Maholt are thinking about, if I write down these kinds of problems, is there a way to talk about agreement as it emerges through collective discussions or collaboration? And it is likely something like this. It's agreeing on a reference forage for our collective observations and agreeing on not just sense making, but it's agreeing on how to make sense of something. So there's a kind of two step process. I learned something figured out.

1:50:53 I tell you, you have your own picture of what this thing looks like. We agree on a picture that serves us best. We agree on a best reference. Fridge.

1:51:08 Daniel:

Yes. Agreeing on the sense made is deciding what to order after the dish has been cooked. We need to have a conversation about the recipe and so many other things.

Ali.

1:51:24 Ali:

Well, I believe this whole argument around Markup blanket and especially the Nested Markov blanket, or the dynamics nature of them, can potentially be connected to somehow the opposing stances, one of which is the preformism or preformationism. The other one is the progressive differentiate mechanism, which in the preformism, some people believed that the topology of the whole state space manifold is completely preformed. We just don't have enough data to model that accuracy, model the state space accurately. But for the advocates of the progressive differentiation viewpoint, they, on the other hand, believe that it literally goes I mean, the state space manifold literally undergoes lots of transformations according to some inflection points or some singularities, and it's not preformed at all.

1:52:47 And the dynamics nature of the state space manifold is something inherent to that.

It's not because of our lack of enough data to model that. So I'm not sure how much you agree with that viewpoint, but that's something that yeah, sure.

1:53:09 Dalton:

I think the kind of drawing and redrawing of Markov blanket is probably a point in support of the idea of progressive differentiate because at one level we think of drawing and redrawing as development or, yes, development. And one of the things that drives development is something like fitness pressure. So fitness changes the constraints on what sort of patterns are available to you, what ought to organize into.

And these are not things that we know are priori at the level of the system. It may be possible that if you write down a whole kind of world model of the entire universe from the very first point in time after the Big Bang, or maybe even at the instant at which the singularity expanded and you had enough computational power to trace it all through that, you could get to something like what is it?

1:54:23 preformationism? But that strikes me quite a lot as a kind of super determinism or determinism argument. It sounds a lot like some kind of argument that there is no uncertainty in how you will develop, there is just uncertainty in what you're aware of as to your development or some kind of hidden variables theory that says there is something mediating the way your state space looks, you just don't know it.

And so you have the illusion of free will. So this becomes a bit of a philosophical question. I myself don't really buy into determinism. So I would be tempted to say that the Markov blanket story, especially dynamic blankets, or however you want to call them, are to do with progressive differentiation as we live our lives. We draw and redraw our own blankets as we mesh and individual ourselves from other systems and the environment.

1:55:28 And this is something that we are in control of, certainly locally in the state space, we're in control of it. Whether there is some hidden variable guiding our own actions is something that is, I think strictly speaking, a different question. The nice thing about it is whether it's true or not, it doesn't break the locality of the Markov blanket construction. So we get this idea of locally progressive differentiation as a Markov blanket and then when we zoom way out, it may be kind of a different story, but certainly locally it works as this kind of dynamic process.

1:56:14 Daniel:

But we almost got to the paper.

This was an awesome discussion. So Ali and Yakuz, if you would like to have any closing remarks.

1:56:27 Ali:

Well, I just want to say that I truly enjoyed our discussion today and I very much look forward to that too because I have a bunch of questions that I didn't have a chance to ask about some of the sections of the paper. So I just wanted to thank Dalton for his time and also for Jacob and Daniel for organizing these extremely fruitful and useful discussion sessions and live streams. So yeah, I'm very much looking forward to the next one.

1:57:13 Daniel:

Thank you Jacob.

1:57:15 Jakub:

Yeah, this was an amazing one.

Thanks a lot Dalton, for all the great answers and overviews. Of course Ali and Daniel for doing bulk of the work on the slides and yeah, looking forward to the dot two.

1:57:42 Daniel:

Dalton, any last thoughts?

1:57:45 Dalton:

No, just thank you for having me. I did really enjoy it and thank you of course for all of the background work that you put in.

As I said, it's very flattering to see such detailed working through of my work. So thank you for that and I am looking forward to the next episode.

1:58:11 Daniel:

Excellent. Well, next week, us and anyone else who like to join, just get in touch or submit any questions or topics. So thank you fellow.

See you later.

1:58:22 Dalton:

Okay! - Cheers! - Thank you!

https://www.youtube.com/watch?v=2SuBJBEg9LI

Second participatory group discussion, with the author, of the 2022 preprint "A Worked Example of the Bayesian Mechanics of Classical Objects" by Dalton A R Sakthivadivel.

Dalton Sakthivadivel, Daniel Friedman, Jakub Smékal, Ali Rahmjoo

00:26

Active Inference Institute Livestream.

03:35

The Road Map to Bayesian Mechanics.

06:45

Introducing Bayesian Mechanics.

12:26

The Last Words in Math Papers.

14:26

Bayesian Mechanics (Section 2).

17:43

Bayesian Mechanics and Newton's Second Law.

22:24

Bayesian Mechanics, Section 1.

31:32

The Irrationality of Bayesian Mechanics.

33:27

The least-action paths.

35:56

Selection of random dynamical systems.

38:30

Synchronization and control systems.

40:10

Systems that synchronize and are surprising.

41:26

Martin Bio: x of T and gamma in Bayesian Mechanics.

45:08

Taking energy from the brain.

48:58

Physysics of Belief and Bayesian Inference.

52:44

How do Bayesian Systems fit within Bayesian Mechanics?

1:04:16

Bayesian Mechanics and Physics of Beliefs.

1:11:38

Bayesian claustal mechanics.

1:15:12

Bayesian Mechanics, Explained in 3.

1:19:27

Section 4 of the Constitution.

1:19:55

Quantum Darwinism and Bayesian Mechanics.

1:26:46

Bayesian Mechanics, the Cognitive Systems.

1:34:36

Bayesian Mode Matching.

1:42:15

Bayesian Mechanics and Path Tracking.

1:51:40

A Bayesian Mechanics talk.

1:54:07

What are the best ways to catch up to the frontier of Bay.

1:59:00

A Little Bit About 49.

00:26 Daniel:

Hello, everyone. Welcome. It's ActInf Livestream Number 49 Dot Two on October 12, 2022. Welcome to the active inference institute. We're a participatory on online institute that is communicating, learning, and practicing applied active inference.

Jacob and Ali and I provided some background in context.

01:30 Then last week in 49 Dot One with Dalton, we all convened, and we had a great discussion and went through a lot of that context again, and that set us up very well today for 49.2 to be primarily going through the paper, which is very exciting. So we'll begin with just saying hello and anything else we'd like to add on this Wednesday, and then we will head right in. So, I'm Daniel. I'm a researcher in California, and I guess I'm excited to get to the paper and understand what points are touched upon and why.

And I'll pass to Markov.

02:16 Jakub:

Hello, I'm Jakob. I'm a student in the UK. And I'm excited to talk about the different faces of Bayesian mechanics, how they are related, how they are different. I'll pass it to align.

02:35 Ali:

Hello. I'm ali. I'm an independent researcher from Iran. Again, I'm very excited to be here as well. Last week, we had a truly amazing discussion with Dalton.

I'm very much looking forward to continue our journey through this fascinating paper today. I also have a bunch of questions I'd like to ask, especially when we come to section four on quantum biology, and I'll pass it to Dalton.

03:06 Dalton:

Okay. Well, I'm Dalton. I'm a mathematician and a physicist, currently based at Stony Brook University.

I'm also at the Berseys Lab, where a large part of my research program right now is to do with the math and physics of the free free energy principle. I'm pleased to be here. Thank you for having me. I'm happy to get the conversation on the way.

03:35 Daniel:

All right, well, we've looked previously at the road map, so let's just take one last glimpse at our map before we go.

You know, white knuckle on the steering wheel, maybe just one overview. Dalton, if you could provide what sections are addressed and what is the general anatomy and physiology of the paper.

04:00 Dalton:

Yeah, of course. So, as we were talking about last time, the structure of the paper partially reflects the environment that it was written in, in a way that is or has come to characterize the free energy

And there are a few key papers that are then kind of summarized and put on stage in the first, maybe four sections. And then sections five through seven are actually taking all of that summary and putting it into a worked example of what Bayesian mechanics looks like.

05:09 So we have a lot of rigorous development to begin with, and then we actually use some of that in the wild and show, okay, so if you're actually to treat this algorithmically and go and computer something using this framework, what would it look like? So in a way, it's kind of split roughly along mathematical and physical lines, if you'd like to think of it that way. Mathematicians really like foundational, rigorous stuff, and then physicists really like to be able to compute things and say something about models of the physical world.

So in a way, it's trying to meet both of those kind of metallurgical needs and that's the reason why it's structured this way. So as we go through, you'll see at some point there's a bit of a phase transition. Where we go from here are all the basic ingredients here, what they mean and how they ought to be used to hear us, how we actually use them.

06:12 Daniel:

We'll keep an eye out for that signpost, and we'll be paying attention to the equations as part of our preparatory work here. It's just those on the live stream will see a subset of our Coda page where we have all of the equations and some awesome annotations by Ali. So we'll be able to look at the paper and also bring in some pre screenshotted formalisms, and we'll journey forth. So beginning with the introduction, what did you aim to set up in the introductions?

What did you want people to have prepared or their state when they entered the introduction and leave it? And also, I'm a little curious about the acknowledgements at the end of the first section.

07:09 Dalton:

Of course. Yeah. So if you go and it might benefit me to have a copy of this in front of me as well.

So give me one moment to bring that up. But one of the things that I wanted to do with the introduction was really roadmap exactly what I had just described, which is that in the last couple of years, and especially the last six months, there's been a lot written about this thing called Bayesian mechanics. And it is a bit of a different take on what has traditionally been written as the free energy principle. So if you're in the active inference literature or if you're in the predictive processing literature, this is probably new to you. And likewise, if you're coming from computational stochastic process theory, then you're probably not familiar with the specific technique or philosophy underlying Bayesian mechanics.

08:09 So that's probably new to you as well. So the idea of the introduction is just to set out, okay, here is basic mechanics. We've talked a lot about it in these previous papers, and it was probably time to Seth out in detail what is it and why are we interested in it and how do we use it, which is, of course, later on in the papers, the work example. So in the beginning of the introduction, I just lay out, okay, here is what we have called Bayesian mechanics. And here is, under what circumstances is it useful?

Which introduces the idea of synchronization in the first and second paragraphs and then in the third

09:14 Some of them are coauthored with other people. Some of them are from Carl's group at the welcome center at UCL. But in all of those papers, they're primarily theoretical, except for certain kind of algorithmic papers, mostly out of the control theory literature.

So it is worth complimenting this unified view that I try and describe taking in the introduction with an application of that unified view, if for no other reason than to give it some concrete particulars. So that's actually a phrase from category theory, which is probably appropriate given that category theory is very interested in the general and the abstract and not so much in the concrete particular. In fact, I think that was a phrase from Laver, who's one of the most famous well known category theorists.

10:23 So it is kind of appropriate. And that part of the motivation for at least the second half of the paper is to say, okay, we've done all this theory work and we've laid out here's precisely what this thing basic mechanics is.

And then to give it some kind of meat to grab onto. If you're someone that likes to actually write models or understand how to shuffle symbols around in an equation and really work with things, then here is something for you that will actually kind of make things make sense to you.

10:59 Daniel:

Awesome. And yes, this is quite not an indictment, but just reflecting the very rapid pace of development that much has been discussed around the role of Bayesian mechanics as a conceptual integrator or unifier, yet the concrete particulars remained to be demonstrated, of course.

11:24 Dalton:

Yeah.

And as you say, it's not an indictment because there is a place for both. And of course, I'm biased, coming from a very strong mathematical background, but I think it is better to go with the more general, more abstract, and it's better to build theory rather than just deploy it. But there's room for both and they serve different needs. So doing exclusively one or the other is in my opinion and in my research, not the best way to approach a problem because you need to be able to build the techniques that solve the problems, then you also need to use them to solve problems. So yes, not an indictment but maybe a striking observation that there's been a lot of the abstract stuff and maybe something more concrete has been missing historically in the literature.

12:26 Daniel:

Awesome. And then any thoughts on the last paragraph or the unusual positioning of the acknowledgements paragraph?

12:39 Dalton:

No thoughts on the last one. I think the last one just draws all of those ideas together and also says one of the reasons why this approach is interesting is it recovers some things of independent mathematical interest, which is what I gesture at in the last sentence. I put all of my acknowledgments at the end of

I like it though. I like it right after the introduction because I think it gives credit more visibly. Mathematical writing is kind of unique in that often you are writing alone by thinking together.

13:46 And so the end product, the paper itself is not always reflected and in fact it's rarely reflective of the mathematical thinking that went into it. So it's good to front load that information.

It's good to say straight away, here are the people that I thought about this problem with and that's what went into this papers. Contributions, intellectual contributions from all of these people that I had conversations with or bounced ideas off of. And so the acknowledgements is right there in the beginning.

14:23 Daniel:

Awesome. Makes a lot of sense.

Okay, so into section two on mechanics. For each section I'll just kind of start up a new page and we can bring in equations and quotations as seen fit. So let's just begin with action two A, classical physics in one dimension. Why start here? And what does this section say?

14:49 Dalton:

Yeah, so section two A is just a very brief summarization of what is classical mechanics. So this is important for two reasons really. One is it allows me to talk a little about the basic building blocks that I'm going to use in the second half of the paper. So we start off on a point of familiarity and if not, then all of that is built up so that later on the rest of the paper is at least referencing something that has already been discussed. So just in terms of layout, it makes sense to get these preliminaries done first.

The other thing is of course, one of the points of the paper, or at least one of the motivations, is that Bayesian mechanics is a mechanical theory just like any other mechanical theory.

15:53 And so to really make that analogy come across, it was good to investigate, okay, well, what are mechanical theories? What does that really mean? So in the context of classical mechanics, what do we mean by the interaction of stationary action principles and laws of motion and dynamics and all these things that we talked about in the previous episode? What do all those look like in classical mechanics and then kind of the metallurgical point of the paper in some sense?

Well, I don't know. You could argue that this is the point of the paper is to make the analogy precise, to point out that, okay, all these things that live in basic mechanics are things that live in mechanical theories that map onto something like classical mechanics and that you can prove. This is really, in some sense, the papers an extended exercise in proving that that map between something that we know very well and something that we maybe don't exist.

17:01 But I would argue at least that that's only window dressing the real point of the paper being proving stuff about basic mechanics. Andy Clark mechanics is just a useful analogy, but I think the way it shaped up, it kind of does both.

And you could argue that, yeah, it does one or the other with one in service on the other. But how that relationship goes, I think, is maybe open to interpretation just the way that the paper revolves.

17:43 Daniel:

Awesome. So equation one and 1.1, just using the decimal point to reflect on numbered formulas that follow numbered formula.

Where do we get on the first page with these equations one through two?

18:00 Dalton:

Yeah. Equation one is starting really from the very basics. So this is the action functional, and in particular, it's the action function for classical mechanics in the Lagrangian setting, equation 1.1 is the result of finding the path of least action or the stationary action. So mathematically, the way that is done is by finding what's called the oil and Lagrange equation.

And that's what this is. So if you apply the oil or Lagrange equation to the action, then one one is the result. And what is interesting about that is that gives you back Newton's second law, f equals Ma.

19:01 And the reason why is because the derivative of V with respect to Q. So the gradient of a scalar potential is a force ActInf lab something.

And the Euler Lagrange equation tells us that our force is equal to the mass times the time derivative of velocity, which is the acceleration. So the chain of reasoning goes that beginning from an optimization principle. You get a law of motion. And that kind of embodies classical mechanics in the case when you begin from the classical action and you get Newton's second law. So the idea is and the reason why this is mentioned is it calls back the reasoning in the paper on Bayesian mechanics physics of in by beliefs.

I think it's the full title, which tells us that in the same way that this exists in classical physics, Bayesian mechanics has its own analogy to this.

20:13 So if we want to regard this as a kind of informational physics, then we can begin with some kind of action functional. In this case, the surprising but a free energy functional depending on the situation. And then somehow the thing that optimizes that is a law of action that describes some kind of dynamical system. And in the informational case, that is approximate Bayesian inference.

And then once you have that law of motion, you can start plugging things in and get dynamical theories based on certain boundary conditions, like the initial conditions or data about what these symbols actually mean. So in the classical case, you're wondering, okay, what is precisely the potential that I'm interested in? What is the mass? What is the initial velocity and cognition? And in Bayesian mechanics, you might be interested in, okay, where is the boundary or the Markov blanket?

21:15 What do my internal states mean? So what kinds of systems am I actually interested in? What are they doing inference over? So what is the environment states they're trying to infer? Or at least what do they look like to the system?

Once you do that, you can start getting from this general law of action, this general approximation inference idea. You can get Attial dynamics things and models of real situations. The reason why that's kind of nice is because then the whole last half of the paper is exactly well, what does it mean to produce a dynamics system out of this law of motion? I have this very general idea of approximately inference. What does it mean to actually start writing down models of things?

22:11 Daniel:

Awesome. Jacob early anything or will continue to be?

22:19 Ali:

Not for now, but okay, I'll definitely have some questions later.

22:24 Daniel:

Okay, classic section. Two b or dot two B question, but let's go two B.

22:31 Dalton:

Yes, that's always good. I think in this section, it is basically running through the same reasoning at a very high level.

And so this subsection to B is all about, okay, what is Bayesian mechanics? What do we mean by Bayesian mechanics? And in a way, it plays on this theme of the paper. I just mentioned this on Bayesian mechanics paper very nicely because this gives us here are the basics of what we're talking about. Here are all the important ingredients, and then the subsections that follow are trying to build out, okay, what do we mean by it's a physics of beliefs?

And then what do we mean by it's a physics by beliefs? Because both of these are kind of imprecise terms.

23:32 And so defining these phrases in a way that is a little more enlightening is a nice way of fleshing out this action and the contributions of the paper. So two B is about the basics of Bayesian mechanics and it just kind of introduces the idea, what do we want from Bayesian mechanics? What is it trying to do?

How does it fit into the free energy principle? Hohwy does it fit into stochastic process theory? And so you'll see in this section, a lot of it is just building up the idea that systems that minimize surprising as the kind of law or the optimization principle they follow exhibit a kind of law of motion, like Newton's law, and it's approximate coherence. And that follows from this reasoning about things that synchronize and minimize surprisal do approximate coherence about the parameters of the probability density of the system to which they're coupled.

24:41 So a lot of the section is just the very fundamentals and we can go through, I think, equation by equation and maybe clarify what those things mean.

That might be a good way of extracting some insight from this. So this is exactly what I was describing. What are the kind of important ingredients? What's the basic setting of Bayesian mechanics? And you'll see on equation on what is it?

Page five in equation three, we begin just from a stochastic differential equation. So this is some kind of random variable that evolves through time according to not only a drift, so some kind of average path or vector field on the value of the random variable at a given time, but also this noise term at the other end of it.

25:48 So these are modeled on what we call controller rough paths in stochastic process theory. So you can think of this as just an ordinary differential equation with an incoming signal. And the signal is the

It's this DW thing is what's called a vena process. It's just white noise. So you have your differential equation and then you have some kind of random signal coming into it. The idea of stochastic process theory is, okay, how do we make sense of the kind of equation that we're looking at here? And in particular, there are a couple of ways of making sense of it.

One of the interesting ones is looking at as this thing produces trajectories, so random sample paths, how do we understand the statistics of those sample paths and thereby understand something about what the system is doing at an ensemble level?

26:56 One of the ways of doing that, and this gets into the next page and the following equations is by understanding, okay, so what is the probability of a path? And that's equation five, but that needs some machinery. We can't just fabricate kind of arbitrary probability over paths. So where do we get that from? And that comes from a least action principle, just the same as it did in classical physics.

So that's really the, I think, primary point of this section is just to begin with, or at least one of the primary points of this section is just to begin with. Already some of the analogies is taking shape because we begin from a least action principle. So S is again an action functional, just like it was in the previous subsection.

27:56 And Omega is a realization of noise.

You can imagine it as just being one of these kind of encoding signals. So what is the noise that I'm putting into the system? And of course, that's where your randomness is coming from. So that's what we're interested in when we're interested in probabilities over paths is really how does a realization of noise or a configuration of noise affect the underlying sample path? And that comes from this action.

So the probability is just kind of the exponentiation of this thing, which comes from stochastic process theory. The same thing arises in the path integral formulation of quantum physics.

28:56 So in that context, we're often interested in what is the transition probability of a particle through spacetime. So that's nothing but asking what is the probability that a particle moves from point A to point B? Given a particular fixed initial point, what is the probability that it takes a particular path from A to B?

So path integrals are like path probability densities, or at least they produce these things. So it's interesting, and it's not a coincidence that the same thing shows up there, that if you take the action on paths and you just put E to the minus S, then you get a path integral. Although I've kind of left some details out because that's a path integral for a statistical field theory in kind of what we call after Wick rotation.

30:01 And so in quantum field theory, we add an I. It's an imaginary variable, but these things are mathematically transferable.

So it doesn't really matter for our purposes in what context we talk about them. That's where equation five comes from, is if we have this action and we just do E to the minus S, then what we get is a path probability density. And as you've written there, again, it doesn't come out of nowhere. It's consistent with stochastic process theory. So all of the sample paths of a stochastic process, if they're continuum, they live in what's called an abstract meter space.

And the probability density over an abstract mean of space is exactly this E to the minus S thing. So that's where that comes from. And it's nice that that kind of falls out of Bayesian mechanics very naturally.

So I talk a little about, okay, what does this mean and how is this equivalent to a surprising? Because I think that's important, too.

The action that I talked about previously, I guess we'll call it 4.1, does come from the yes, 4.1, that S is equivalent to the surprising. And that comes from if you just put a logarithm on both sides of the equation five, you get log p equals minus s.

32:13 If you put A on both sides, then you get minus log p equals s. So the surprising of a trajectory is equivalent to this integral over time of the noise squared. So, by the way, I don't know that I defined those brackets, but the brackets just means you take the two things inside the bracket and you multiply them by each other.

So really this is just the integral through time of the noise squared. And that is equivalent to the surprising is more interesting for our purposes because it means the converse also holds. If you start from the point of the abstract Venus space and you write down the correct action, then you get Bayesian mechanics back as the idea that something that minimizes its action in the Bayesian mechanical setting minimizes its surprising.

33:15 I'll let you write that down and then we can carry on, I think, from page seven, because the rest of page six is just saying all of that.

33:27 Daniel:

Sure, I think surprising may be more conventionally understood in a statistics framework, but what is action? Is this related to me moving my arm action or what do we mean by action here?

33:40 Dalton:

Yeah, so in the concept of physics and mechanics, an action is a function. So it takes a function and it gives you back a number.

And as a functional, what it does is it gives you a kind of a weight or a cost associated with a trajectory. So if you write down a path through space or through space time as a specific function, then the action takes that function and gives you back the cost of taking that path. And so the idea in classical mechanics is the cost associated to a path is based on how much extra energy does it take if you take that path from A to B and extra energy is kind of circular in a sense.

34:41 It kind of presupposes the least action path exists. But then if you allow that for a moment, then the idea is, okay, so there should be a path that uses the least extra energy to get from A to B, and in doing so, it produces the least cost.

So finding the least action path, the path of minimum action, is the optimal way to get from A to B. And in classical physics, paths of least or stationary action more generally are the only acceptable paths. When you start to introduce noise, it becomes a probabilistic judgment. So paths of least surprising are the most likely paths. You have other ways to get from A to B as well.

If there are very large fluctuations, for instance, in that sense you can think of action as kind of a loss functional or something analogous to it in the machine learning world because it is a judgment about how good a path from A to B is.

35:56 Daniel:

Before we go to the next section, Ali or Yahoo, do you want to add anything?

Okay, that was page six. Now we're going to page seven.

36:11 Dalton:

Yeah. So then I go on with this story about synchronization which is introduction here in some greater detail than has previously been done, I think just one of the points of the paper. So I begin by saying, okay, let's take two random dynamical systems which I call Ethan New.

This is kind of well, it's not kind of is an abuse of types. So just be aware when you're reading this, eater and Mu are states of the random dynamical system. But a random dynamical system is a bit more complicated than that. There's more machinery going on in the background. However, just like we would write kind of a big capital X as a random variable.

So we name the SDE after the values of its states.

37:16 We can do the same with the random dynamical system if we wink and nod and remember that that's not quite correct. But it's also worth pointing out that a random dynamics system can be identified with an SDE under the right circumstances and that you do so very easily. So this is totally consistent with the previous discussion and I have a paper forthcoming that does that in a bit more detail. So it's continuing along these lines and saying, okay, if we begin from this phase of mechanical story of systems that are coupled to each other do coherence and if they are random dynamical systems, then that coherence is meaningful and comes with a path of probability density and all this that's in greater detail in this forthcoming paper.

38:17 So anyway, that's kind of technical remarks. But just keep in mind in the first sentence there's a bit more going on there. But I'm allowed to do that because it all works out anyway. And then we begin with this thing about synchronization. So when you consider coupled systems, then those systems synchrony.

So there's some relationship between the statistics of those two systems and that is this sigma function that is given in earlier literature by people like Karl and people in his group. So the sigma is relating the average internal state to the average external states. It's even called the synchronization function in that literature. And in this case we actually also want to be able to say not only a state at a given time, but also that the paths of the.

39:20 System synchronize.

So taking it a little bit more generally than has been written before, we now want to be able to say that, okay, so now the trajectories of the random dynamics systems synchrony. So how one evolves depends on how the other evolves, which is conceptually is fine and relates to things that have already kind of been worked out, like active inference. You know, how an active inference agent evolves through time depends on how its environment evolves through time and vice versa, because active infants agents can act on the environment and change it. Control systems more generally are things that fit into this trajectory based formalism. So then I talk a little about surprising.

So what does it mean that systems that synchronize minimize their surprising?

40:21 And there's a lot to detail in this section. There's a lot of stuff that goes along with that statement. But ultimately it's just saying that systems that synchronize with each other almost by definition are

Your surprising, if surprisingly, is defined as deviations away from the thing that is being synchronized to.

Again, that's almost a topology. But that's, I think, kind of the power of the framework is you begin from the statement that makes almost trivial conceptual sense and then it gives you some kind of actual useful model of what the internal dynamics of the system are doing. And that's at the end of page seven.

41:26 Daniel:

Great. I'll ask a specific and a general question from the chat.

So first the specific question and just let me know which equation to look at. Martin Bio asks what is the relationship between x of T and gamma?

41:45 Dalton:

Gamma is a path. So it's a realization of XT, the random variable. X of T is just another way of writing comma.

I do it in a couple of different ways just to drill down the point that lots of different literature, lots of different ways of seeing this thing are all the same. So for instance, gamma is used in the literature around maximum caliber, there's maximum path entropy. X of T is kind of consistent with this functional idea. So regarding a path as a function and then plugging it into the functional and seeing, okay, what is the surprise, what's the cost associated with this path? And you'll also see, I think, Q of T later in the paper.

And that's interesting because Q is the variable and Q of T is conventionally used in classical physics literature just again as a mathematical convention.

42:51 So anyway, yes, to answer your question, gamma is just this x of T. There are two different labels for the same object.

42:57 Ali:

Okay?

42:58 Daniel:

And McParlin follows up is this synchronization an additional assumptions to Bayesian mechanics or is it part of the assumptions for it?

And then is x of T comma of T?

43:13 Dalton:

Okay, so the idea of synchronization is critical to Bayesian mechanics actually telling you anything useful. Because the whole story about coupled things do inference on each other is something that follows from this synchronization. So the whole story about approxipation inference follows from the coupling. So synchronization is an important assumption. One thing that you can do, however, is to prove that things that synchronize are coupled and vice versa.

44:20 It wasn't difficult to show and it's not really surprising, but that is something that you can show. Gamma of T.

I don't think I use gamma of T in the paper. Maybe I use gamma SubT. So comma T, like offset from the mainline gamma SubT is again the same notation that's used elsewhere.

So it just means a path at a particular time point. So it's just a state, a realization of the random variable at that time.

45:08 Daniel:

Okay, and then there's more general question before we head on was from Dave who wrote, what does using energy mean? For example, is that extracting potential energy and transferring that withdrawal to kinetic energy or the relevant analogs?

45:26 Dalton:

Yeah, in the context of an action functional, that's exactly what it means.

So this transfer of potential energy to energy of motion, which is kinetic energy.

Yeah, I think there is a discussion of this, a kind of conceptual discussion of this in the On Brain and Mechanics paper somewhere in section two, I think. And it's the idea that, okay, when we talk about minimizing action, it's about you have some energy budget, your potential energy, and you want to know, okay, what is the most efficient way of using that budget? What is the way that transfers potential energy to kinetic energy with the least accumulated loss over time? And physically, that is just following a force gradient. So if you try to do extra, if you try to wiggle your way through the force gradient, you now need to invest more tangential energy, but you're getting to the same spot.

46:37 So that's not necessarily what you want to do. So this is why the Oil Lagrange equation is kind of interesting, because it tells us what we intuitively expect is the most efficient way of transferring an energy budget to actual motion is just following along a force gradient. And that's why we see things like Newton's Law, that the acceleration of the system is always the force acting on it, or in proportion to it anyway, because you also have this mass constant.

47:09 Daniel:

Awesome. Onto page eight equations six, seven and eight.

47:16 Dalton:

Yeah. So this is setting up the variational free energy. So we have in six and seven we have the kind of traditional factorization that we've seen in a lot of this literature, which is here is the free energy functional with the joint density, the generative model. And then if we take out this extra surprising term, then we get the variation of free energy in a kind of reduced form which bounds the actual surprising of the internal states of the system or the particular states of the system, the blanket and the internal states. This kind of sets us up to say, okay then if the system is synchronizing well so if it's

48:40 So you have these functions ETA of T, mu of T is about the evolution of the system through time.

48:49 Daniel:

Alright, Jacob early, anything you want to add there?

Okay, now we get to the physics of and by beliefs. We would have completed the constitutional trifecta with the force beliefs. Also some very interesting connections that Markov and I and others have explore with grammatical case. For example, the physics of belief being the generative case. Whereas the physics by belief might be like the instrumental case and that might point towards natural and semi natural languages to describe beliefs.

But just broadly, what is happening in these sections and how do we get towards equation nine?

49:38 Dalton:

Yeah, so in this action at the end of the previous section, synchronization gives you surprise minimization and in section C I'm using the building blocks to actually make that statement. So approximate Bayesian inference is about how a system's beliefs behave, given that they need to match some kind of density over the environment. And where match means not necessarily equal, but synchronized too. So this is what we mean really by physics of beliefs is the context for basic mechanics is certain kinds of systems that are coupled to their environment or that are coupled to another system, synchrony to that other system.

And as a result, we can understand the statistics of one system as synchrony to the statistics of the other system.

50:44 So any kind of belief updating or any kind of large deviations principles or anything that we can use to understand the statistics of one are done implicitly in the context of the statistics of the other. And again, this is what we mean by physics of beliefs is suddenly we have now formulated a kind of law of motion for the beliefs of the system, which is to do with synchronization and the props of Bayesian inference. So the idea that we can understand sometimes literally motion in the sense of motion on a statistical manifold right movement in a space of beliefs, we can understand it as being a response to the pressure to minimize surprising given whatever you are or the system is synchrony to that's really the main thrust of this section.

51:45 And I talk a little about exactly what does that mean and what is the point of synchronization?

I don't think there are a lot of equations in this section, but this is about it's about that. It's about okay, synchronization is a thing that we talked about a lot and we talked about it in the context of minimizing surprising. But it's important to set up the idea that when we talk about basic mechanics it is partially about the system itself. But what makes it kind of special is it's about the beliefs of the system. And it's saying, okay, here is a way of understanding coupled systems by forgetting about the systems themselves and going into synchronized beliefs and understanding how to synchronization affect the probabilities that we assign to system states.

Great, so that's of beliefs and now we go to buy first. Yakka.

52:52 Jakub:

Yeah, I'm just wondering how would you say that active states are formalized within Bayesian mechanics? Because I feel like sometimes there's this kind of duality where we can say that systems can be described by Bayesian mechanics and we say that they act as if they're performing Bayesian inference. Then there are also systems which in this kind of conventional sense do perform Bayesian inference through some active states.

So just wondering how do active or even sensory states fit within Bayesian mechanics?

53:37 Dalton:

Yeah, that's a good question because as you said, sometimes, especially for very simple systems, this is a kind of mathematical technique. It's even a trick in some sense. That's not to say that it doesn't work, but it doesn't have the kind of epistemological sense of belief or if it does, you got to do a lot of work to make that make sense. And there's a lot of philosophical debate about this in the literature.

And I know there's a corner of literature that is specifically about do things actually minimize the free energy or is it just a useful model? I'm kind of agnostic. I think the whole question is basically irrelevant because the reality is whether or not it is true in a literal sense or is just a model or whatever. At the end of the day the maths works. So yes, you have to be careful about acknowledging the limitations of the maths to describe the actual physics and the biology.

54:45 You should be being careful about that anyway. And I acknowledge that maybe I'm being a bit unfair because I'm saying the question is irrelevant and then going on to say you do have to be careful about the question. But at the end of the day it is just maths. And so whether the math is a true model of a system or is a model of what we think the system is doing is kind of a silly question being phrased that way. And the reason why is because the math is always just a model.

I think something like that point was advanced in a paper by Mel Andrews where it said that the FEP is just a model of a system and whether the model is any good or not is strictly separate from whether the model is true or not. And in general models are not true in the sense that no system is actually sitting down and calculating.

55:50 Okay, here is the root of my free energy functional. Here is what nature says I should be doing. I'm going to go do it.

So anyway, that was kind of a digression. That wasn't directly your question. The reality is yes, it is a kind of a mathematical trick and the math works but it doesn't always tell the satisfying concept story that we want to hear. So I think you're right. The big difference is to do with how active the system is because systems that can actually do actions do have a use for storing representations.

And we think about things like controlled systems in this sense, which are systems. That agent just minimizing their surprising as a mathematical truism that unsurprising systems do unsurprising things but they are systems that exist in and environment that is trying to dissipate them actively because they are very far from an equilibrium point and they need to know what the environment is doing in order to know how to respond to it.

56:58 So active states do draw a pretty clear line between and I should say as well, sophisticated active

But sophisticated active states draw a pretty clear line between genuine Bayesian inference and just kind of like applied statistics so to speak. And it's something that I haven't really thought deeply about except to note that this is a place where there is a distinction to be made. I talked a little about this in the geometry and analysis paper that I just mentioned and it shows up quite a lot in the forthcoming paper that I mentioned in last session, which is by Lance and myself and Karl and a few other people.

58:06 And it's called path integrals and particular kinds in that paper, I think I mentioned in the context of an interesting calculation to do with moving frames of coherence. But additionally there's quite a lot of work in that paper and one of the key deliverables of that paper is here are a number of different kinds of free energy functionals which are defined by different kinds of partitions.

So a partition that has active states and a partition that doesn't and what are the qualitatively different kinds of behaviors that we're able to describe. And one thing, one case that that paper tries to make is that there are interesting systems and noninteresting systems and there are lifelike systems and not lifelike systems, and that they exhibit very different behaviors when they minimize their free energy, including lifelike systems are able to minimize their expected free energy.

59:07 So it's not just a case of applied statistics. They're actually one presumes holding a model of the world and making predictions about the world and taking action now that minimize free energy in the future. That's a bit more sophisticated than just a tree branch shaking in the wind, because it would be kind of surprising if it didn't.

That's a law of physics. It would be surprising if the tree branch didn't shake in the wind. But to say that the tree branch is doing Bayesian inference over its environment is only true in this, I guess, instrumentalist sense. I don't know if that's actually the right word for it. I think that's the word from the philosophy literature that I'm not qualified to use properly.

But it is true in the instrumental sense that that is an instrument that we can use to describe the dynamics of the system. It's not true in the kind of literal cognitive sense that the tree is now forming a model and making predictions about its current state and state of the environment.

1:00:11 There may be pan psychist types that would disagree with that, but that's the view I take anyway. So this is a very interesting question. I hope that answered at least part of it.

1:00:24 Jakub:

Yakum yeah, it definitely did. I'm just also wondering whether on your point where we have sophisticated actions and not sophisticated actions, whether that could also be a consequence of the complexity of the environment. Because in the case of just a tree branch being shaken by the wind, we just have one type of mechanical force that the tree branch is synchronizing to. But in a more complex environment with living systems, there are many more of maybe not explicit forces, but maybe cognitive forces or biological forces that the systems might need to couple to. So I'm wondering whether the formalism could also not be adjusted to the complexity of just the individual entity that we're interested in, but also to the complexity of the influences of the environment that the system couples to.

Yeah, I think there's definitely remit to say that simpler systems can only infer simple things, and so they do best in very simple environments, more complex things in a way. And there are arguments that this is why structures like the brain evolved. Actually, I believe I suppose he's listening, martin Field has an interesting paper about this, and I forget the title, but the point of the paper is there's a very neat hypothesis that the brain evolved because it's very good as a biological structure at handling what's called counterfactual information. So the brain evolved as a prediction generation mechanism.

There's remit to say that complexity of an individual scales with the complexity of the environment because something like a human that wants to self organize very far from equilibrium.

1:02:38 Suddenly there's a lot more to keep track of because there's a lot more acting on you to keep you down, so to speak. And so you not only need complex sensory motor loops to respond to all that complexity, but you need a complexity processing hub to actually deal with all of those variables and categorize all that information and decide, okay, what are my sensor motor loops doing in this situation? How am I actually encoding to the things that I'm observing? Definitely there is an interesting story to be told with how the complexity of the outside determines the complexity of the inside.

And it is kind of, again, a very nice meta application of the FEP. Because if you think that if you want to say that things that selforganize are things that mirror their environment, then it is precisely the claim that if you want to be a complex thing and you are subject to very complexity environment forces, then you need to be a complex thing to self organize.

1:03:55 And this is the kind of good regulator type theorem that has come to characterize discussions about the FEP. So, yes, another interesting question. Great.

1:04:07 Daniel:

Well, just to carry forth and get a first pass and everything, although of course, the door is always open for dot threes and beyond. In section physics of beliefs, we have equation 910 eleven and several more.

So where do we get to by the end of action? 2d, what's the key piece here?

1:04:31 Dalton:

Yeah, so in the previous subsection, I spent a lot of time building up the idea that Bayesian mechanics is a kind of a special way of thinking about laws of action in the space of beliefs. So motion on a statistical manifold, which is one really interesting thing about it, and that's of mathematical interest, maybe, because it's now saying, okay, here are some kind of new dynamical systems theories on statistical manifolds, which is quite cool and it does kind of I think that's interesting on its own. But if you are into physics or biology, that's not quite enough.

The nice thing is that there is this idea that, okay, it's not only about laws of motion in information geometry, but it's about mapping a system which has some kind of physics in the real world into and ideally simpler physics in statistical manifold.

1:05:50 So in virtue of talking about synchronization as a law of motion for beliefs, we are now saying, okay, we don't need to talk about the Attial physics underlying the synchronization. We can go into this space of beliefs and we can say, okay, synchronization tells me that the system's beliefs are changing this way and that reflects a physical change of this nature. So it's an equivalent way of talking about

So we should then be able to make inferences about real systems using data, mechanical laws. And this is what is meant by a physics by beliefs is if we invert the story and say, okay, now I want to know what is approximate Bayesian coherence saying about the mode of the system, about the parameters that are doing approximate inference, you can do that.

1:07:01 You can make inferences about the system itself. And if your inferences are good, then you learn something about the system. So that's very general and that's also subject to surprise or minimization.

So if you are unsurprised and you have a good model of the system so now the whole story applies to itself in some sense. If you minimize surprising about your beliefs about a system minimizing surprising, then you can get a model of how that system is self organizing, and you hope that the loop kind of closes. So this is, I think, quite an important point. It's the subject of a duality relationship that I gesture at and write a lot about in the geometry and analysis paper. It also shows up in a paper called the Map Territory fallacy.

Fallacy.

1:08:03 It has fallacy twice in the title. And that's by myself. Maxwell Ramstead, andy Karl Friston. And it investigates the idea that you can actually turn the story on its head and make a model of a system making a model of its environment.

And that that's insightful for various reasons. The interesting thing about that is it now gives you a physics by beliefs in the sense that now my description of what the system is doing so my description of the material physics is inferential. It's based on my beliefs about what the system is synchronizing to and how well is it minimizing surprising. And it's also based on how good my model is. So it's based on whether I can minimize my own surprising and make good inferences about the system.

And this calls back to the principle of constrained maximum entropy, because what that's saying is my model of the system is an coherence of the system subject to Axel Costa, that the model of the system reproduces surprise or minimization.

1:09:23 So any model that I have of the system must say that the model is itself or that the system is itself holding a model of its environment and is minimizing surprising. So that's where the constraint comes from. It's that this is something that we know our priori. So it's something that we should incorporate into our model of the system, this surprising minimization.

And that just working out the math of that is all of these equations. So it's showing that if you put a constraint that your model of the system includes surprise or minimization, then you get back exactly approximate Bayesian inference. So there's this other route to Bayesian mechanics that just says, okay, if we begin from and in reality and the point I try and make is that it's not actually a exafferent route to Bayesian mechanics. Because all this is saying is if my model of the system begins from the point of view that systems that synchrony minimize their surprising, then I get back the minimization of free energy and surprising in the context of the system.

1:10:37 So kind of nuanced.

I think that there's a lot of moving pieces but ultimately that's all that means. When we say physics by beliefs is it's the application of the constrained maximum entropy principle to create a model of a system which is minimizing its surprising. And what's interesting is that that model itself is subject to the laws of Bayesian canx because it is a probabilistic belief. So it's like saying I'm sitting in the

1:11:37 Daniel:

Excellent. On to section three, a general equation for Bayesian claustal mechanics. So it will be helpful for you to situate where it begins and then how we approach equation 15.

1:11:53 Dalton:

Yeah, so this action is kind of taking those building blocks so we have a way of modeling systems that model their environment and it's this kind of dual surprising minimization problem. So how do we actually write that as a problem that we can solve?

How do we do computations with this thing in the context of classical physics especially and also this analogy that we talked about previously, does that go through to this case? So you can build up this idea, you can build up the idea of a classical physical system that couples to its environment and it is in this case a force that ants to separate the thing from its environment. So again, there's a bit of an abuse of types in the sense that we would usually consider a sensory state experiencing or measuring that force.

1:12:59 But we instead I just plug in the force itself under the assumption that it's not a noisy sensor maybe. And that proves to be again, not a taxing assumption because it tells us the same story at the end.

You can deduce everything that you'd need to so you can set up a synchronization function in that case and it just tells the system what the environment is probably like given the force acting on the system. And already you have the ingredients for approximate Bayesian inference because you have a conditional independent. So the system doesn't need to know what the environment is like if it knows the force acting on it. So you can argue that there is a conditional independence there or at least a sparse coupling and you have an inference problem because the system does need to know what to do given the force acting on it.

1:14:08 So it does need to know what is the environment like given that force, and it can only do what it needs to do if it is minimizing surprising.

So all the ingredients are there. And you can also talk about the fact that the classical action is the basic mechanical action in the limit of no uncertainty. So you do get surprising minimization as equivalent to classical action minimization. And that's ultimately the chain of reasoning that gets us down to equation 15 is that the path that minimizes the classical action is the mode. So it is the most likely path.

So the path of least surprising. So you can structure class mechanics as a least surprising problem. And that gets us down to equation 15.

1:15:12 Daniel:

Excellent. While I bring 15 in ali or Yaak. Any thoughts?

So maybe could you read equation 15 with the variables and or the natural language semantics?

Yeah, I'm a big fan of that. I think that's a useful way of breaking things down is explaining the objects being involved. And there are people that really take that philosophy to the extreme. To the extent that I've seen talks where you're not allowed the chair of the session says, okay, you're not allowed to just tell me the name of the thing.

You need to explain to me what the thing is and what it's doing.

1:16:05 Daniel:

Isn't that a case of the chair doing inference on you?

1:16:08 Dalton:

Yeah, well, maybe. In fact, probably it is. How do I best fit this into my world model?

Or tell me in terms that I understand. Explain it to me. That's really what it is. Yeah. So here we have the past probability density.

So it's the probability of a classical position, Q at a time t, which is a joint density. In this case, it equals the exponential of the minus of the action that we saw in the basics of Bayesian mechanics section. So it is the normal path probability density. And the only question is, okay, what is S?

We've plugged in something interesting for us. It's the integral over time of the deviation of the classical path Q from the path of least action, where the path of least action is defined as the double integral of the force divided by the mass.

1:17:20 So the double integral of an acceleration, which is just a position. So given that we know the initial conditions, what is in the vertical bars? So what is being squared is just the deviation of Q, the Claudia Clopath from the expected path or the path of least action.

Excuse me. So this is precisely the classical action in the sense that it gives you back the path of least classical action, gives you back the path that follows Newton's laws.

1:18:05 Daniel:

Excellent. So to bring it closer one level, what variable might we be talking about? Like, what kind of data set or variable might Q be?

1:18:20 Dalton:

In classical physics, we're mostly interested in spatial positions or at least generalized coordinates describing those spatial positions. But more generally, we.

Could talk about a lot of things. Q could be really anything. One of the nice things about random dynamical systems and random variables is there is a great generality in what that state could represent. So in general, it's just a label for something. Here in classical physics we are interested in spatial positions.

1:19:04 Daniel:

Okay? So it could be how excited I am about a song or my belief about the temperature or what this person's next sentiment is going to be.

Yeah.

1:19:19 Daniel:

Anything else on three? Or it'll be great to move to four.

1:19:23 Dalton:

No, I think that's really the story about three.

1:19:27 Daniel:

Awesome. Well, four.

Ali, would you like to set up or introduce how you see section four and what you wanted to ask?

1:19:37 Ali:

Well, yes, actually, if you permit. I wanted to make somewhat lengthy comment here, if I may. Not too long. I promise. We're going to need a zero three.

I think I'm following that with a question. As we know, there are numerous approaches proposed for driving classical properties from quantum matter, so to speak. But I wanted to mention two controls, which to my mind are particularly Congress with Bayesian mechanics bun quantum physics. I'm not sure if you're familiar with causal Fermion systems approach developed by Felix Finster and others because it's not a particularly well known theory. But in any case, it's basically another variational approach for explaining the emergence of a structured spacetime with all of its associated phenomenological properties such as the flow of time, the chain of console events and so on, from an optimal configuration of selforganizing quantum wave functions.

1:20:53 But instead of defining the action functional as the surprising to be minimized in order to active the optimal inference, as we saw in Bayesian mechanics, they define the causal action as the action function of minimizing which leads to the optimal configuration of wave functions which in turn results in the structured spacetime properties. And the other approach I wanted to mention is quantum Darwinism proposed by Voucherc, inspired by the principle of natural selection which attempts to explain how the most stable pointer states which attempt are favored among the many possible quantum states and thereby resulting in the classicality of our everyday observations.

1:21:53 Actually, this approach is also alluded to field ant all's paperfree energy principle for generic quantum systems, I guess. So do you see Bayesian mechanics as ultimately unifying all these different approaches somehow into an Mtheorylike integrated theory? Because in your recent Parr on the map of Territory fallacy fallacy, which you mentioned, SAP is already shown to be the ideal modeling tool for generic systems in statistical physics.

So can this statement be potentially extended to encompass all the other physical systems as well?

1:22:36 Dalton:

Yeah, that's a good question. I'm not familiar with this causal Fermion systems work, although it sounds like it fits into a kind of spirit of question that exists in condensed matter theory asking about, okay, how do things emerge that have a given structure from things that don't have structure. And

It's a different Michael Levin.

1:23:37 Levin and someone called when have developed things like string net condensation, which is all about how do well, I guess at a high level, it's about how does structure arise from the application of constraints to I guess you might call them self organization and you might call them self organizing field series. Although that's not the language of Lebanon. And when you and I think that's kind of telling the wrong story, maybe. But there's something there definitely something to be generalized. And likewise for quantum Darwinism, there is this idea that the things that we measure as the most certain or the classical states arise from a spatial interaction component.

So things that couple to other things have well defined measurements, pointer states, because of this localized interaction.

1:24:50 I apologize as a evolution of, I think the decoherence problem. This is one interpretation and it just remains to kind of make that more mathematically rigorous. And people like Dean Carroll have written about this at length. So in both cases there is kind of an intersection of ideas and they both seem very basic mechanical. I think one of the nice things about Bay mechanics is it's very general.

It's just a story about how constraints and survival minimization and statistics interact to get you a model of a physical system. So in principle that is very general and you start to add extra constraints and things like the Markov blanket and whatnot. But there is probably limit to generalize this even further to something that is purely about how do paths that synchrony behavior probabilistically and that is very general.

1:26:05 And that probably applies to more than just computational Bayesian statistics physics, but maybe other aspects of quantum mechanics and condensed matter theory and so forth.

1:26:21 Daniel:

Great, thank you.

Well, in our last 30 minutes of the dot two with of course the dot three on demand, let's get to those worked examples and we will look forward to a thousand notebooks blooming with people simulating and making generative visualizations and extending some of these examples. It'll be great though, to hear what are the real world situations that you are applying Bayesian mechanics to and then what do each of these equations do on the path towards application in each of these settings? So previously we discussed the three phases of Bayesian mechanics. So could you just review the three phases of Bayesian mechanics in light of where we're gain to go in the coming applications?

1:27:16 Dalton:

Yeah, of course.

So the kind of pyramid that you see here is at the bottom layers. All of these, I guess boundary condition specific applications of the FEP where the boundary condition that we're interested in is whether the mode being matched, whether the thing that we're synchronizing to is a state. And then you have states and paths that's the first split. And within states you're also interested in, okay, is that state

1:28:30 Specifically for the middle one, I think I use a ball thrown in the air and so eventually it comes back down to Earth and rests on the ground and then the celestial body of planet in orbit is your path tracking.

1:28:47 Daniel:

Okay, so we have the analogy very clear and we can say rigorously supported. The left side, we're talking about synchronization to states like parameter values that are instantaneous, whereas the right branch is the density over path. So the synchronization is to a path. On the left side we have fixed and dynamics mode mode the mode mode fallacy, fallacy and that is matching to a ball at rest and a ball thrown in the air on a parabola that will come to rest. And the satellite motion is the infinite chasing.

Now we're talking about cognitive systems. So what are the cognitive analogs or the real world cognitive settings where we're talking about some cognitive entity like a computer or a person or an ant colony rather than perhaps a ball on a hill?

1:29:45 Dalton:

Yeah, so this is a good question. I think in the path tracking case at least, it's pretty obvious that this active inference lab, this is a very general blueprint for what it means to be in a dynamic environment and to constantly be synchronizing to an environment that is changing and that maybe you yourself are changing. And that may be something that's worth commenting on.

It's only this last case that is the kind of stuff that we're interested in in terms of worked examples when it comes to genuinely cognitive systems. And it's this last case that we know the most about in terms of work examples. It's the case that hasn't been really worked out in terms of rigorous maths. Although in the last six months or so, that's what's been being done not only with this paper, but also with the path intervals paper that's about to come out and the free energy principle made simpler but not too simple.

1:30:56 And also Lance and Karl and Greg have a paper called Geometric Sampling Methods in Optimization and Adaptive Agent where this is also talked about.

So in a way, this is the case that we know the most about and it's the case that works the best. It's the case that actually explains the kinds of stuff that we want to explain, but the rigorous math hasn't been done. In that case, the simpler density dynamics formalism is much less useful and to some extent suffers from its own problems in terms of edge cases and maybe mathematical confusions.

So there is some cleaning still to do with the density of the states formalism. But again, ironically, that's the formalism that we care the least about.

1:31:56 And what we're most interested in is making the path tracking make more sense and making it more complicated and generalizing even faster to explain things that synchrony to paths in a more complexity way. So the path tracking is about these kinds of things and one way to think about them is in terms of expected free energy. So not only minimizing my free energy right now, but minimizing my expected free energy along the path.

That's one way of thinking about it. And another way of thinking about it is minimizing the surprising

1:33:10 You can think of it as an instantaneous approximation to the path tracking. And so in that sense, there are things that are cognitive and do fixed mode tracking, or what we call mode matching. But if you think about it, that is again, and instantaneous approximation to the path tracking. Seth so if you think about something like Uri, we're usually not matching a mode because that means we are staying complexity still and our environment is staying completely still. And that happens mostly at death, which is it is something that we can talk about.

We can talk about a system at total rest, but even then the analogy breaks because the environment still isn't at rest. Only on very brief active states can we approximate it as being at rest.

1:34:13 And it's also not the story that we're looking for about coherent agents. So the fixed mode and the dynamic mode are mathematically interesting, but I think when it comes to the biology and to some extent even the physics, they're not very interesting.

1:34:34 Daniel:

Very interesting. So maybe as we scan through these equations, just what are each equation doing within the example? So we're in terminal node matching, section six A, and we see equation primarily 17.

1:34:54 Dalton:

Yeah. So equation 17 is just giving you I think we skipped section five, which is the mode matching.

So maybe I do want to just quickly mention that when you have force at equilibrium and you have an initial condition of zero, this is and equation 16, then the path of least action is not a path at all. It's a stationary object. It's an object at rest. And so you can do this very easily. You'll see, I write Q minus zero squared equals zero.

So the surprising, that is the surprise, right. You're not integrating through time because you're only at one time point. So the integral goes away and the double integral of the force over time is just the is just zero because the forces are at equilibrium. So the surprising is minimized when Q equals zero, when there is no motion and the system is at the mode.

1:35:59 In this case, you can imagine Q as a generalized position corresponding to the height above the ground.

So when Q is on the ground, not moving at that time point, you are minimizing your surprising. And that's what we call mode matching. And again, you see this as a very simple setting because literally nothing is happening. And that's not really fit for describing cognitive agent. But it is a good simple case just to make sure that all the maths works.

1:36:29 Daniel:

In the simple case, I'm imagining this to be our belief about the room is that it's 37 C and the thermometer is giving us 37, 37, 37. So the mode instantaneously is not being updated and that's kind of like a balloon is being inflated and it's pressure matching or the ball is on the ground. So the forces

1:37:03 Dalton:

Yeah, exactly. If you want to imagine again this physics of belief setting, there are no forces acting on me between observations. There are no probabilistic forces changing my beliefs about the system. So the mode is stationary. I'm always matching the same mode.

So nothing's happening, no movement on the statistical manifold, and therefore we get mode matching. It's a very trivial case.

1:37:32 Daniel:

Now we introduction some forces into the picture with mode tracking.

1:37:37 Dalton:

Yeah, so mode tracking is a little bit more complicated because you have an actual inference you're interested in where something is and also how to get to it. And there's kind of an open question somewhere in this section which is about or maybe in the following action, which asks, is a least surprising path to a target mode also an instance of mode tracking?

Right? And I actually don't know that that's something that is open for me. I think we'll encounter it somewhere, I don't know where. We will stumble into it anyway. But anyway, it's the idea of, okay, so we want to do inference about where is a mode that I'm not at and how do I get there.

In this case, the example is of a ball being thrown through the air.

1:38:41 So again, thinking of Q as a generalized position corresponding to the height above the ground, I start at some initial condition above the ground. And gravity is the force acting on me, telling me the mode that you want to be at is at rest on the ground. So in some sense you can read this. You can read a ball being thrown through the air and then falling to the ground as doing inference about what gravity tells it to do.

And if you write this out, there is an equation of motion which is a path of least action and it's just this parabolic path to the ground. And if you plug that in and you minimize the surprising, then you get a system kind of goes like that. And what's more, you can write this as a gradient ascent on surprising. Well, gradient ascent on the probability density, a gradient descent on the surprising.

1:39:46 So it is literally a minimization problem because you can get back the equation of motion from a gradient descent on the surprising.

And that is I think we will call it 17.2. So it's the third equation in this section. Yes, that's the one right after the first labeled one, which is 17. So this gradient descent, this minimization from, gets you exactly the equation of motion that you want so you can prove that surprise minimization tells you something interesting about this case of mode tracking. Cool.

1:40:27 Daniel:

I'm imagining a cognitive entity, a physicist, a Bayesian mechanic, modeling in their perception implication or in their notebook explicitly the path of a ball. And the cleanest situation would be if their factorization and understanding of the sparsity of the territory if their map resembles it. But no matter,

1:41:07 Dalton:

Yeah, that's definitely one way of thinking about it. We talked a little last time about what it looks like to collaborate and to converge on a belief.

And it's a little bit like that if we assume there's no uncertainty about where everyone is headed and you just want to figure out how to get there. So if you're like a bunch of people collaborating on an idea and you know where I am and I know what B is, then this says that the best way to get to B from A is just to minimize your surprising. That's the path of least action from A to B. And in this case that means that it is precisely the most likely path that is the path of the classical object from A to B.

1:41:58 Daniel:

Very interesting since sometimes it seems like we're discussing in a value and preference aligned setting how to do something, policies as inference, whereas there's also a discussion of where to go and all of these other pieces.

We'll just touch on each piece as lightly as possible in a few minutes so we can have a closing round in B six B, we have tracking of mode infinite mode tracking.

1:42:29 Dalton:

Yeah, this is the kind of precursor to the idea of path tracking which is saying, okay, if that mode is constantly in motion, what does that look like? And you can do the same thing if you write out the equation of surprising minimization, you can get the idea of continuum motion as well, but it's slightly more complicated and it is slightly less conceptually satisfying because it's not surprising minimization. It's sort of surfing along level sets of the probability. So the probability isn't minimized and the surprising isn't minimized, the probability isn't maximized.

You're not choosing the most likely path, which is one of the reasons why I then go on to talk about path tracking in the next section is to say, okay, so we tried to do this thing with a continuously moving mode, and it kind of worked, but not really.

1:43:40 So what if we said something about minimizing the surprising paths instead of continuous mode tracking? What if we just talk about continuous action tracking a path? Do these things coincide? Do they tell the same story?

And this is where the initial stuff in the basics of beta mechanics action comes into play, because now we're talking about path probabilities and minimizing action function. And at the end of the story, you say, okay, so the whole thing does go through. You can talk about selecting the path of minimum surprising, and in this case, it is following along in a satellite orbit based on the continuous forces that are being applied to you. So added return, you have a kind of circular force. You have not only a tangential force outwards, but also a centripetal force inwards.

1:44:41 And if you write this down appropriately, you can get the equation for a circular orbit. That's what this is doing, is saying, okay, if you have this continuous force acting on you, then can you match a path of least appraisal? And you can?

Excellent. And just one last note on the first idea of G theory before we take a breath in our closing round.

1:45:14 Dalton:

Yeah. So this is kind of a complicated section. The point of this section is ultimately to say that two things, really.

One is that the case for classical physics is a nice playground, but it's kind of a simple one. And the aspirations of basic mechanics are to talk about non equilibrium, complex, self organizing systems. So can we pull something more interesting out of the maths? And it's also to make the case that the path based formalism is the right thing to look at when we want to pull something interesting out of the maths. So the answer to the first question is yes.

And implicitly that supports the second name because it says, okay, not only can we actually get a description of, in this case, chaos versus integrity or ergodicity versus non ergodicity, but also that it comes out of the path based formalism very naturally.

1:46:20 And in a way, Bayesian mechanics is a little bit special in this sense because the idea of a path integral approach to classical physics comes out of Bayesian mechanics very naturally, and the results in this setting come from that path integral approach. So it implicitly has this kind of third aim that because of this path based formalism in Bayesian mechanics, is what did the job. Ant Bayesian mechanics is the thing that we may want to look at in more complex systems. So that's the aim of this section.

What this section does is it just writes down the path integral for a system in classical physics, given that it does phase and inference as per basic mechanics. So approximate Bayesian inference, if you'd like. So if you write down a system in classical physics doing some kind of synchronization, you get a path integral with a particular kind of form, and then you can transform this a couple of different ways.

1:47:31 I do detail the derivation there, but they're all very standard transformations and you get out of this something called a supersymmetry. Now, the idea of supersymmetry goes back to, I think, the 70s.

It's an observation that in certain quantum field theories you get asymmetry that relates different kinds of particles. So what that means is, if I write down a quantum field theory with two different kinds of particles, and in general they are fermions or bosons, but it doesn't actually quite matter what. At least you can get specific kinds of fermions and bosoms. So the story doesn't have to be totally general. Then sometimes you can exchange the different kinds of particles and you get the same theory, so you can freely swap them and nothing about the physics changes.

1:48:37 This is called a super asymmetry. It's not a usual symmetry in the sense that when we think about symmetries, we think of geometric things that relate, say, two different sides of a shape. So it is asymmetry in that it relates to different things in such a way that nothing changes. But it's a super asymmetry because it's about particles, not shapes, say.

The interesting thing is, supersymmetry breaking always leads to mathematically interesting observations and physically interesting observations. So if we have access to a super asymmetry, then the thought is immediately, OK, what can I say with this? I should keep an eye out for something interesting happening when the supersymmetry breaks. And in this context, the supersymmetry breaking is about having two or more different constants of motion.

So ergotic systems have one constant of motion. It's just the energy or the Hamiltonian that you'd put into the probability measure. But in nonagonic systems, in integral systems, you have multiple constants of motion. So it's not just the energy, but it's some other thing. You don't know what necessarily, but you have additional variables.

And what's interesting about that is then we can make the observation that supersymmetry is about, or is analogous to chaos, because ergotic motion is chaotic. It's about things that mix and things that fill their state space in sometimes unpredictable ways, whereas integrity nonagoticity is about systems that are very predictable.

1:50:42 You just integrate them, and you say where it will be in a future time. So, after all this derivation and concept work, what we end up with is a way of saying, based on mechanics, has an accounting mechanism for chaos and not chaos. And that's where I leave off.

I say, So this is something interesting that we can do with basic mechanics, and it comes out of the path into a formulation very naturally. And this is a very trivial case of just classical physical systems. What can we get when we just start to describe the complex cases of more interesting systems like biological physics or self organizing field theories or things of this nature? And that's the end of the paper.

1:51:34 Daniel:

Well, like paper, like stream, as they say.

So let us spend our last several minutes with Ali and Jacob. Any just closing thoughts or questions or distinctions that you want to continue on?

1:51:58 Ali:

Well, it was an amazingly illuminating learning journey. So I wanted to thank again, Daniel, Jacob, and ander for organizing the discussion sessions leading to these live streams, and especially Dalton for his time and for sharing his brilliant insights and expertise with us. And on a more personal note, Dalton, your work has rekindled my long forgotten, deep passion for theoretical physics. And I know I'll certainly continue to explore this fascinating area of Bayesian mechanics a lot more. So I'm truly grateful for that.

Yes, that's it from me, and I'll pass it to Yahoo.

1:52:51 Jakub:

Yeah. Also, thanks to everyone, Daniel, Ali, who participated in the discussions. I think your input align on the different equations was really invaluable. And, of course, thank you, Dalton, for firstly writing the paper and then spending the time with us, going through it.

I'm really looking forward to future work. I would have many other questions about how Bayesian mechanics is related to other areas of physics, such as relativistic mechanics, or the non classical results within quantum mechanics, which we touched on last time, and then the actual applications to computational models as well.

1:53:57 So I'm looking forward to exploring these more.

1:54:06 Daniel:

1:54:19 Dalton:

Yeah, well, first, let me say it's Beren a pleasure. I've really enjoyed the discussions, and you guys came in very well prepared, so that made it even richer. So thank you for all your hard work, and thank you for having me.

I think DAGs mechanics is becoming very technical side of the free energy principle. And I think that speaks to how ecumenical the FEP has been and how interdisciplinary it has been because people come to it from many different backgrounds, including mathematics and physics, like me, but also computer science and machine learning and also neurobiology and also philosophy. So there's something in it for everyone. And if you are interested in this kind of more technical side, one thing you can do, and to some extent just have to do, is read.

1:55:27 There is a lot of literature being published at a very fast pace in the last few months, so it can seem like a lot to wrap one's head around.

But I think one thing that I have started to be better about, and certainly my co authors have been good about, is road mapping things. So it's easier and easier, I think, to get a handle on what all is being said and how it relates to other things being said. Papers like this are a good example of things that draw everything together really nicely, I think. Anyway, I don't know if I can say that, but I will anyway. And there are other papers and things that kind of break things down and explain things in a more accessible way than the highly mathematical, highly technical work that's also being published.

1:56:27 I write blog posts summarizing some of my papers sometimes, so if you're interested in those, you can find them on my website.

Also on my website I have a kind of Bayesian mechanical bibliography where I organize all of the recent papers in this area and what their contributions are. That's not on my blog. That's under a page on my website called Research. But nonetheless, that's something that you can look at as well. And I think everyone involved is also fairly accessible via email, I think.

In my experience that's been the case anyway, I'm always available at my email. Karl is a very generous person with his time and people like Maxwell and Lance and Thomas Conor, you know, all the people that have been involved are, in my experience, people who are willing to take and answer questions.

1:57:37 So that's also something to do if you're reading something and it just doesn't make sense. Do get in touch with someone and in my experience, people will be very charitable in terms of taking and answering those questions.

The one thing that is tough is kind of building up the background for these. But I think like anything, it is something that you can develop on the fly, so to speak. So as long as something makes sense to you at some level, and maybe you're not an expert on the topic, maybe it only makes sense in isolation and you don't have the whole picture in your head. I think in general that's all right. So yeah, maybe it's not a very satisfying answer, but at least part of the answer to your question is we'll just start reading.

1:58:42 And if you do get stuck, then people in this area are pretty nice people, so don't hesitate to contact one of them if you do get stuck or if you want to bounce ideas around.

Well, as stated, it's been an amazing series and I know it's not. The end of 49, there are decimal to come. So, Dalton, thanks again. Yakapali. Under.

Thanks for all the amazing work. Till the next gradient.

1:59:20 Dalton:

Okay. Thank you. Yeah.


---
*Extraction method: odt_xml*