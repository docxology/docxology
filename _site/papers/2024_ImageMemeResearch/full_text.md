# Full Text: ImageMemeResearch

> Extracted from `2024_ImageMemeResearch.pdf`

> 5 figures extracted to `images/`

---

## Page 1

R E S E A R C H A R T I C L E
Bridging gaps in image meme research: A multidisciplinary
paradigm for scaling up qualitative analyses
Mridula Mascarenhas1
|
Daniel Ari Friedman2,3
|
Richard J Cordes3
1School of Humanities & Communication,
California State University, Monterey Bay,
California, USA
2Department of Entomology &
Nematology, University of California,
Davis, California, USA
3COGSEC, New York, New York, USA
Correspondence
Mridula Mascarenhas, School of
Humanities & Communication, California
State University, 100 Campus Center,
Seaside, California 93955, USA
Email: mridula.mascarenhas@gmail.com
Funding information
National Science Foundation,
Grant/Award Numbers: #2010290,
#49100423C0010
Abstract
This paper outlines a multidisciplinary framework (Digital Rhetorical Ecosys-
tem or DRE3) for scaling up qualitative analyses of image memes. First, we
make a case for applying rhetorical theory to examine image memes as quasi-
arguments that promote claims on a variety of political and social issues. Next,
we argue for integrating rhetorical analysis of image memes into an ecological
framework to trace interaction and evolution of memetic claims as they coa-
lesce into evidence ecosystems that inform public narratives. Finally, we apply
a computational framework to address the particular problem of claim identifi-
cation in memes at large scales. Our integrated framework answers the recent
call in information studies to highlight the social, political, and cultural attri-
butes of information phenomena, and bridges the divide between small-scale
qualitative analyses and large-scale computational analyses of image memes.
We present this theoretical framework to guide the development of research
questions, processes, and computational architecture to study the widespread
and powerful influence of image memes in shaping consequential public
beliefs and sentiments.
1
|
INTRODUCTION
In the aftermath of the February 3, 2023 train derailment
disaster in East Palestine, Ohio, outrage exploded as inade-
quate official narratives clashed with first-hand testimonies
and frantic sensemaking in online spaces. The trending
hashtag #OhioChernobyl equated the toxic conditions cre-
ated by the derailment with the 1986 nuclear disaster in
the Soviet Union. Allusions to Chernobyl also implied “that
national and local media were ignoring the disaster”
(Thompson, 2023, para. 19). Mistrust of the rail company
and of government entities dominated public opinion, both
in the affected Ohio communities as well as nationally.
Social media influencers ran amok with speculations about
the extent of the damage and about the federal govern-
ment's efforts to cover up details of the disaster. While offi-
cial messages were insufficient and confusing, online
sensemaking filled in gaps, with “rumors and suspicions…
swirling on Facebook and TikTok accounts all over the
country” (Robertson & Cochrane, 2023, para. 8).
The ubiquity of public sensemaking through social
media networks makes social media chatter a significant
variable in understanding public uptake and rejection of
official messaging and the formation of public opinion
and action in crisis events. However, our capacity to trace
such sensemaking lags behind its incredible power to gal-
vanize publics. Understanding how narratives about
political and social crises rise to the surface requires
Received: 1 May 2023
Revised: 2 April 2024
Accepted: 21 April 2024
DOI: 10.1002/asi.24900
This is an open access article under the terms of the Creative Commons Attribution-NonCommercial-NoDerivs License, which permits use and distribution in any
medium, provided the original work is properly cited, the use is non-commercial and no modifications or adaptations are made.
© 2024 The Author(s). Journal of the Association for Information Science and Technology published by Wiley Periodicals LLC on behalf of Association for Information Sci-
ence and Technology.
J Assoc Inf Sci Technol. 2024;1–17.
wileyonlinelibrary.com/journal/asi
1

## Page 2

studying the entanglements between social media and
legacy media discourses. While capacities exist for identi-
fying narratives emerging from online discourse (Cordes,
Applegate-Swanson, et al., 2021; Snowden, 2002), we are
currently under-estimating a powerful vector of online
narrative creation and dissemination—the image meme
(Highfield & Leaver, 2016).
Figure 1 shows examples of image memes about the
Ohio train derailment, selected from public posts on social
media accounts, and presented without any identifying
information. The examples come from a collection curated
by the authors. Large-scale computational image meme
research (e.g., Tommasini et al., 2023) typically draws
image meme samples from (1) online encyclopedias like
Know Your Meme, which invite crowd-sourced submis-
sions and offer metadata on image memes such as date of
origin, evolution, and cultural background, or (2) from
online image meme sharing platforms like X (formerly
Twitter), Facebook, and Reddit as well as smaller online
communities like HiddenLol, Memedroid and Dump A
Day (e.g., Morina & Bernstein, 2022), or (3) through Google
Image search (e.g., Sharma et al., 2023b). Many of the
meme examples presented in this paper are not cataloged
on the Know Your Meme database, underscoring the
importance of expanding and collating various image
meme collections and catalogs for research.
Current events are regularly and rapidly absorbed
into
image
meme
discourse
(Dancygier
&
Vandelanotte, 2017; Grundlingh, 2017). Beyond serving
simply as a vehicle for transmitting narratives con-
structed on other media, image memes themselves can
develop and amplify narratives by engineering quasi-
arguments (Mascarenhas, 2021). These narratives have
documented impacts on public belief, sentiment, and
action (Cordes, David, et al., 2021). For example, image
memes function as an “important element of participa-
tion in digital publics” engaged in environmental dis-
course
(Jones
et
al.,
2022).
During
the
2016
US
presidential election, Internet memes “enabled users to
rapidly take a stand on and react to developing political
events in real time; they provided alternative parallel dis-
courses to mainstream media viewpoints; and they
enabled mobilizing voters outside of official political dis-
courses” (Heiskanen, 2017, Abstract). Image memes also
correlate with public health choices. Rates of HPV vacci-
nation were lower in states where “memes expressing
safety concerns, misinformation, and conspiracies com-
prised a higher proportion of Tweets” (Isaacs, 2020,
p. 497). In fact, memetic circulation of such content cor-
related more strongly with vaccine uptake than other fac-
tors known to influence this choice, such as “race,
ethnicity, education, and income” (Isaacs, 2020, p. 497).
In this paper, we present a rhetorical-ecological
framework for studying image memes, as an effort to pre-
serve the health of information ecosystems. We explain
why examining image memes as quasi-arguments that
advance claims, as well as tracing how those memetic
claims develop, circulate, and evolve within information
ecosystems, can give us a richer picture of the threats that
image memes pose to information ecosystems by pollut-
ing them with misinformation and disinformation. Infor-
mation ecosystems have been studied along multiple
dimensions, including “information needs, information
landscape,
production
and
movement,
dynamics
of
access, use of information, impact of information, social
trust and influencers” (Kuehn, 2022, p. 438). Our work
draws attention to an additional dimension within infor-
mation
ecosystems,
namely
the
rhetorical
form
of
FIGURE 1
These sample image memes illustrate attempts to make sense of the Ohio train derailment by situating narratives about the
event within other contemporaneous circulating narratives that signal distrust of the government.
2
MASCARENHAS ET AL.
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

![page2_img1.jpeg](images/page2_img1.jpeg)

## Page 3

information artifacts. By tracking the role that a particu-
lar type of artifact (e.g., the image meme) plays within an
information ecosystem, we gain insights into the other
systemic
dimensions
outlined
above.
For
example,
high-level image meme activity contradicting mainstream
narratives, in niche information ecosystems, can signal
siphoning of social trust away from consensus-approved
sources. Additionally, the virality of specific image meme
content can also identify particular public needs for infor-
mation, and therefore opportunities for engagement or
intervention with publics.
We encourage taking image memes seriously as arti-
facts of public influence and posit that social media users
become persuaded by the additive and interactive effects
of memetic content, over time. Therefore, the capacity to
trace cumulative impacts of image meme content can be
useful. Kuehn (2022) conceptualized information ecosys-
tems as dynamic aggregations of evidence across particu-
lar domains of knowledge. Accumulation of information
about a topic over time builds latent potential for evi-
dence synthesis, that is, comparing and contrasting infor-
mation to extract evidentiary patterns, accumulating an
evidence ecosystem for that topic. While the concept of
evidence ecosystems in Kuehn's work pertains to knowl-
edge domains like health sciences, we extend the concept
of the evidence ecosystem to image meme circulation. As
we explain later in this paper, memes function as quasi-
arguments by furnishing or alluding to evidence, whether
valid or not. The ability to identify traces of evidence
aggregating across image memes sheds light on how pub-
lic beliefs that contradict mainstream narratives come to
hold persuasive power. Observing accumulation and
change in evidence patterns can strengthen intervention
efforts that seek to combat spurious beliefs because cor-
rective messages can be refined by a deeper understand-
ing of the cumulative and shared evidence patterns that
underlie those beliefs. By situating images memes within
an evidence ecosystem framework, we heed Ma's (2021)
observation that “problematic information phenomena”
such as misinformation and disinformation “have an
individual transcending quality” (p. 1297), inhabiting,
infecting, and driving collective epistemologies, instead.
By focusing on an artifact of information pollution, that
is, the image meme, we gain insight into the emergence
and evolution of these collective epistemologies, without
needing to access individuals' cognitions or beliefs.
2
|
STATE OF THE ART IN IMAGE
MEME RESEARCH
Image meme research is occurring at different scales and
across methodologies. We can situate this breadth of
work in approximately three areas—(1) smaller-scale
qualitative analyses dedicated to understanding the cog-
nitive processes that underlie sensemaking from image
memes, (2) smaller-scale critical analyses that examine
image memes as cultural artifacts, and (3) larger-scale
computational analyses that leverage machine learning
to detect and classify image memes, specifically according
to sentiment.
Qualitative research on image memes focuses on
understanding memes as patterns of language. For exam-
ple, Zenner and Geeraerts (2018) applied a Cognitive Lin-
guistics
framework
to
examine
wordplay
in
image
memes. Some qualitative research has examined the
mechanisms by which image memes function as speech
acts—for example, Dynel's (2016) exposition of how
image macros (memes with captions superimposed on
visuals) reflect a “continuity with the classic joke format”
(p. 668). Shifman (2014) applied a critical-cultural per-
spective, identifying key “logics” of participatory digital
culture in photo-based meme genres (p. 341). Huntington
(2013) used visual rhetoric which “combines elements of
the semiotic and discursive approaches to analyze the
persuasive elements of visual texts” for analyzing memes
as “a form of subversive communication in a participa-
tory media culture” (p. 2). Hahner (2013) made the case
for treating memes as “visual arguments” (p. 153). And
Milner and Wolff (2023) illustrated how image memes
“hail participants into a collective identity” (p. 4). Quali-
tative approaches such as those taken in cognitive lin-
guistics focus on memes as linguistic constructions,
identifying “the cornerstones and building blocks” of
image memes (Zenner & Geeraerts, 2018, p. 174), while
rhetorical studies, including the one we propose, draw
attention ultimately to the interpretive outcomes that
emerge from the configurations of the building blocks
within the image meme. In our framework, we explain
how content and form within the image meme activate
lines of reasoning to assert arguments.
Qualitative studies generate important insights about
how memes create public sensemaking. However, they
do not address the scale of social cognition forged by the
sheer volume of image meme content generated and cir-
culated online. Computational analyses, on the other
hand, have observed image memes at large scales, using
techniques such as image classifiers and optical character
recognition (OCR) of text in images. Some of this work is
dedicated to tracing where image memes originate from
and how they spread across web platforms (Morina &
Bernstein, 2022). Computational work has also focused
on training automated systems to combine analysis of
text and image modalities to detect offensive content, par-
ticularly
hate
speech
(Afridi
et
al.,
2021;
Koutlis
et al., 2023; Tung et al., 2023). In addition to focusing on
text and image, the spatial placement of “faces, visual
objects, and text clusters” in image memes has been
MASCARENHAS ET AL.
3
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

## Page 4

studied
to
conduct
sentiment
analysis
(Hazman
et al., 2023, p. 5). Computational image meme studies
have also examined their virality (Barnes et al., 2021;
Ling et al., 2021) and their evolution over time and across
platforms (Beskow et al., 2020), including short-lived evo-
lutionary trajectories described as memetic moments
(Smith & Copland, 2022). Some studies have explored
large-scale cataloging and analysis of memes (Kougia
et al., 2023; Sharma et al., 2023b; Tommasini et al., 2023).
While the bulk of computational studies on image
memes focuses on detecting and categorizing them
according to sentiment, some computational research has
attempted to unveil the sensemaking that produces senti-
ment effects, for example by identifying “whether the
meme glorifies, vilifies, or victimizes each entity it refers
to” (Sharma, Kulkarni, et al., 2023, p. 1). The latter study
is an example of combining a qualitative paradigm, in
this case “narrative framing” (p. 2), with tracking the sen-
semaking process across a large corpus of image memes.
The need for bridging work between qualitative, critical,
and quantitative research is particularly relevant cur-
rently, when image memes are playing a substantial role
in the formation of beliefs and attitudes across digital
publics. This opportunity is especially ripe in the field of
information studies, which has begun the turn toward
recognizing socio-cultural processes that underlie sense-
making in information ecosystems.
Tang et al. (2021) have urged paradigm shifts in infor-
mation studies to address unprecedented changes in the
“social, political, economic, and cultural dimensions” of
“information as phenomena” (p. 253), including the pol-
lution
of
information
ecosystems
by
mis-
or
dis-
information. In particular, they emphasized the need to
move from individual user cognition and experience
to models of “shared/distributed… cognition” (p. 254) and
to “understand the sociomateriality of information arti-
facts embedded in various social-technical contexts”
(p. 256). Recent scholarship in information studies has
begun to examine social media contexts and modes of
communication
(Hagen
et
al.,
2021;
Potnis
&
Tahamtan, 2021).
We argue that image memes are a rich resource for
understanding consequential collective social cognition,
especially in information contexts that breed extremism.
Studying the impact of image memes requires a combina-
tion of approaches. Researchers have underscored “the
need to bridge… the computational and the cultural anal-
ysis of visual social media” (Highfield & Leaver, 2016).
Cross-disciplinary collaboration can leverage multiple
methodologies to grasp the widespread influence that
image memes exert in developing shared public cogni-
tion. We join other voices in urging serious study of
image meme-driven sensemaking and its potential to
influence
information
ecosystems.
Our
framework
contributes to efforts that span the gap between small-
scale qualitative and large-scale computational analyses,
to stimulate research on the impacts of image memes at
varying scales.
Specifically, we combine rhetorical and ecological
theoretical frameworks to encourage the development of
analysis architecture and research questions for studying
image memes. While image memes have already received
attention as rhetorical artifacts (e.g., Hahner, 2013;
Huntington, 2013), our paper furthers the application of
rhetorical theory to the study of image memes by demon-
strating how and why image memes should be analyzed
as artifacts of public quasi-argumentation using the Toul-
minian argument framework (Toulmin, 1958). We also
insert rhetorical analysis of image memes into a broader
analytic framework guided by ecological theory in order
to scale up the volume of image meme analysis. The inte-
grated rhetorical-ecological framework holds promise for
surfacing patterns of belief and sentiment formation
across a wide range of public-interest topics, which in
turn can help us understand the formation of consequen-
tial digital publics that become aligned around interests
and worldviews forged through circulation of image
memes on social media platforms.
3
|
KEY TERMS AND
ASSUMPTIONS
Before we present our approach for studying image
memes, we clarify the terminology and assumptions used
in this paper. First, we intentionally pluralize the term
“ecosystem.” Kuehn (2022) contrasts conceptions of the
information ecosystem as a universal context of “infor-
mation that is present in one's daily and public life” with
recent usages of the term referring to “specific systems of
social media and online communities” (p. 435). Because
image meme sensemaking on social media intentionally
feeds off official and mainstream sources of information,
we assume fragmentation of the ecosystem, to recognize
the entanglements between these disparate information
contexts. Image memes also live more abundantly on
some social media platforms rather than others due to
the platforms' varied structural affordances and con-
straints. Accordingly, a study of the sensemaking role of
image memes requires acknowledgment of these niche
information ecosystems. Nonetheless, image meme sen-
semaking that originates in specific digital public spaces
influences beliefs, opinions, and actions of other publics
(digital and non-digital), thus transcending specific eco-
systems of origin and perturbing the universal informa-
tion ecosystem, as well.
Secondly, we clarify our definition of the term “image
meme.”
Well-known
meme
creator,
Saint
Hoax,
4
MASCARENHAS ET AL.
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

## Page 5

described the meme “as a piece of media that is repur-
posed to deliver a cultural, social or political expression,
mainly through humor” (Benveniste, 2022) and as an
artifact that “has the ability to capture insight in a way
that is in complete alignment with the zeitgeist,” (as cited
in Benveniste, 2022). The word “meme” has become
semantically elastic—stretching from a general “unit of
culture” to the specific form of the image-macro, which
refers to “captioned images that typically consist of a pic-
ture and a witty message or a catchphrase” (Image
Macros, 2020, para. 1). We use the term image meme to
refer to a specific visual artifact that has become ubiqui-
tous on social media platforms like Facebook, X (for-
merly Twitter) and Reddit (Morina & Bernstein, 2022).
We distinguish this artifact by two features—form and
function, that is, the rectangular box that demarcates the
artifact as a discrete communication unit and the use of
this communication unit to participate in public argu-
mentation. Unlike image macros which necessarily com-
prise a combination of both images and verbal text, our
definition of the image meme includes artifacts that rely
on just images, just text, or a combination of both.
Although image memes execute a variety of rhetorical
functions
(Guenther
et
al.,
2020;
Taecharungroj
&
Nueangjamnong, 2015), and many instances of image
memes communicate humor on mundane issues rather
than engage with social or political topics, we focus on a
sub-genre of image memes that participate in public
argumentation by advancing claims about political,
social, or cultural issues (Tindale, 2017).
The presence of image memes online is mostly local-
ized to three types of sites—meme generators for creation
of image memes, social media platforms (e.g., forums,
message boards, and media sharing sites) for circulation,
and databases for image meme documentation. Although
meme developers often create image memes anony-
mously with meme generator sites, most audiences
encounter previously created image memes on social
media rather than post self-created ones. Finally, sites
like Know your Meme and databases like the Internet
Meme Knowledge Graph (Joshi et al., 2023) house collec-
tions of memes with some cataloging and analysis capa-
bilities. For purposes of understanding how politically
and socially relevant claims shape the beliefs and opin-
ions of various online publics, social media platforms
emerge as a key focal ground for observing image memes.
Different platforms tend to host different types of
memes. Zannettou et al. (2018) collected memes from
“Twitter, Reddit, 4chan's Politically Incorrect board
(/pol/), and Gab” and found “a substantial number of
politics-related memes on both mainstream and fringe
Web communities” (Abstract) but racist memes were
more present on the fringe online social communities
such as /pol/ and Gab.
Given that image memes capture cultural trends and
address current issues, memetic ecosystems are highly
dynamic. Some image memes have demonstrated longer
lifespans than others. For example, according to the
Know Your Meme website, the Condescending Wonka
image meme, “featuring a screen capture of actor Gene
Wilder in the 1971 musical Willy Wonka and the Choco-
late Factory” and for which “the captions can be charac-
terized as patronizing and sarcastic,” has been in
circulation since 2010 (“Condescending Wonka/Creepy
Wonka,” 2012). That particular image meme has been
remixed in various iterations with text captions that sig-
nal condescension on a variety of topics. Figure 2 shows
a version that circulated during the 2020 pandemic. Even
though the image content can have a long-life, different
text overlays repurpose the image content to create differ-
ent memetic claims, thus ensuring the ongoing evolution
of memes. Typically, image memes have shorter lifespans
and pass out of circulation even if they have been popular
for a while. Ford et al. (2021) in a study of 352 text
memes, selected from Know Your Meme for their popu-
larity and then followed across their circulation on Red-
dit between 2010 and 2020, found that meme lifespans
have grown significantly shorter over time. While the cre-
ation and circulation of new memes is increasing, the
memes are staying relevant for shorter durations. Here, it
becomes crucial to distinguish between what Tommasini
et al. (2023) refer to as “the template” which is the under-
lying cultural unit that can be repurposed (i.e., the Con-
descending Wonka image) from what they refer to as an
“instance” where the template is deployed to make a
statement in a particular case (p. 5), as in Figure 2. In our
FIGURE 2
Image meme using the “Condescending Wonka”
template that claims masks are ineffective against Covid-19.
MASCARENHAS ET AL.
5
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

![page5_img1.jpeg](images/page5_img1.jpeg)

## Page 6

framework, we foreground the identification of memetic
claims which are typically present in instances of tem-
plate deployment and require interpretation of the visual
or verbal components, including of the template, within
the instance. However, since we also consider image
memes that may contain mostly or only text within the
rectangular frame, our definition of the term applies even
in those instances that may not use a culturally relevant
template.
4
|
COMBINING RHETORICAL
AND ECOLOGICAL FRAMEWORKS
The objective of our paper is to instigate systematic stud-
ies, at various scales, of image memes and their role in
public sensemaking. We outline a theoretical framework
(the Digital Rhetorical Ecosystem framework or DRE3)
to inspire the building of digital architecture and pro-
cesses for meme collection and analysis across platforms
and subject matter. Although the framework can inform
a stand-alone pipeline for meme collection and analysis,
it can also guide smaller-scale analyses of how memes
shape public belief and sentiment in specific topic areas
of public controversy, such as the COVID-19 pandemic,
vaccine skepticism, and climate change.
Our theoretical framework begins with rhetorical
analysis of memes, particularly through the application
of Toulminian argument theory (Toulmin, 1958), to trace
sensemaking possibilities emerging out of image meme
circulation. As rhetorical analysis is a critical-qualitative
small-scale approach, we also cross disciplinary bound-
aries to widen our analytic framework by integrating bio-
logical ecosystem metaphors for guiding
large-scale
studies of the aggregate impacts of memes on informa-
tion ecosystems over time. The usefulness of the theoreti-
cal framework outlined in this paper is not restricted to
adopting the entire integrated model. We encourage
teams of researchers to draw, as needed, from the rhetori-
cal and ecological frameworks or combinations of both.
4.1
|
Rhetorical analysis of memes as
quasi-arguments
Philosopher Bruno Latour observed that “whether or not
a statement is believed depends far less on its veracity
than on the conditions of its ‘construction’—that is, who
is making it, to whom it's being addressed and from
which institutions it emerges and is made visible”
(Kofman, 2018). We add that the believability of a state-
ment also accrues from the rhetorical form in which the
statement is presented, a phenomenon that is particularly
vivid in the role that images memes play in the develop-
ment of public beliefs. We advocate attention not only to
the content of memes but to their structural logics that
demonstrate the argument potential of the content. One
type of discourse to which such an analysis can make sig-
nificant contribution is the growth of conspiracism across
online communities.
Introne et al. (2020) have advocated studying con-
spiracism not as a “deficient epistemic process” but
rather as a “diverse and dynamic collective sensemaking
process, transacted in public on the web” (p. 184). They
applied a narrative paradigm to argue that conspiracy
theories should be understood as stories that make sense
of events by implicating “deceptive, coordinated actors
working together to achieve a goal through an action or
series of actions that have consequences that intention-
ally disenfranchise or harm an individual or population”
(p. 186). They distinguish narrative cognition from the
other primary type of human cognition—argumentation,
because narratives are “liberated from slower, more
deliberate verification processes” (p. 189). Our work con-
tests this premise by blurring the distinction between
narrative and argument as cognitive processes. Introne
et al. examined text-based messages on online forums
and found an “extraordinary diversity of… story elements
that sustain… overall narrative[s]” (p. 188). We argue that
image memes promoting conspiracism reveal such story
elements in the form of small quasi-arguments that both
reflect and aggregate into higher-order narratives. Image
memes function as the argumentative building blocks of
eventual conspiratorial narratives and of the cognitive
process by which individuals are drawn into identifica-
tion (Milner & Wolff, 2023) with online conspiratorial
discourse communities.
We advocate the use of Toulminian argument theory
(Toulmin, 1958) to understand the persuasive potential of
image memes. Attending to the rhetorical form of image
memes reveals the argumentative cognition compelled by
the meme's components. Although image memes are typ-
ically perceived as light-hearted artifacts of humor, we
advocate focusing on the persuasive dimensions of image
memes circulated by social media users as a means of
participating in public argument. While the rhetorical
form of such image memes can and does infuse humor,
the form can also structure the content into an argument.
That is, the image meme can go beyond provoking a
chuckle to assert a claim that the viewer is drawn to
either accept or reject. Treating image memes as argu-
ments allows us to identify the claim(s) advanced by
them, as well as how those claims are bolstered by evi-
dence and warrants that are either explicit or implicit in
the meme. While the processing of an image meme may
not simulate the painstaking process of argumentation
6
MASCARENHAS ET AL.
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

## Page 7

one exercises in an academic or legal setting, for example,
we treat image memes as quasi-arguments because they
do persuade by deploying components and processes of
argumentation (Mascarenhas, 2021). Tracking memes as
purveyors of argument can explain why they hold persua-
sive power in certain online discursive spaces, like con-
spiratorial communities that describe themselves as
upholders of epistemic authenticity and truth-telling in
opposition to “conventional and privileged ways of know-
ing” (Introne et al., 2020, p. 185). Our rhetorical approach
is consistent with Grundlingh's (2017) assertion that
memes are not just artifacts of speech, but that they
should be regarded as “speech acts” themselves (p. 148).
Image memes not only signify meaning but they accom-
plish social functions like asserting arguments and audi-
ence identity.
4.2
|
Application of rhetorical analysis to
extract memetic claims
Image memes tend to advance partial or implicit argu-
ments, which makes the artifact especially potent in dis-
rupting
mainstream
media
messages
by
providing
targeted counter-claims that are exempt from the obliga-
tions of rigorous elaboration required of more formal
information artifacts. The truncated arguments in image
memes create ambiguity and, accordingly, flexibility for
audience interpretation. Across formats such as text-only,
image-only, screenshot, and image-text juxtaposition,
image memes “create the possibility of extracting multi-
ple and multi-layered interpretations within a range of
meanings” (Mascarenhas et al., 2021)—a semantic condi-
tion captured by the term polysemy (Boxman-Shabtai &
Shifman, 2014). The semantic and syntactic elements of
an image meme jointly generate rich and varied significa-
tion. However, meaning-making is ultimately guided by
structural features in the meme, including strategic place-
ment of images in relation to each other, or of the
placement of text in relation to images. Another struc-
tural feature—the ubiquitous rectangular boundary of
the meme—not only demarcates the meme's content but
insulates it from the attack of counter-arguments, by cre-
ating the illusion of a self-evident non-porous argument.
The visual boundary that restricts the amount of content
that can be contained in an image meme, along with the
expectations of limited textual material, and a logic that
emerges out of image-text juxtaposition allow for image
memes to assert truncated arguments. Because the arti-
fact constructs an argument with limited information, it
relies on audience engagement for decoding, and this
cognitive investment makes the audience more impervi-
ous
to
counter-arguments.
We
show
below,
using
Toulmin's argument framework, how truncated argu-
mentation makes the image meme both a strong rhetori-
cal
force
and
simultaneously
highly
vulnerable
to
advancing spurious arguments.
A Toulminian approach can unravel the cognition
demanded by an image meme to accept a particular belief
proposition. The three major elements of an argument in
the Toulmin model are the claim (the proposition the
audience is required to accept), evidence (data supporting
the
proposition),
and
warrant(s)
(assumption
(s) connecting evidence to claim) (Toulmin, 1958). We
analyze the image meme in Figure 1, Panel 3, using this
approach. The meme juxtaposes a line of text above a
photograph of a man whispering into the ear of former
US President G.W. Bush. The text articulates what the
man is presumably telling the president. The photograph
is key to decoding the argument made by the meme. That
image template is widely recognized for capturing the
moment that White House Chief of Staff Andrew Card
informed then-President Bush about the terrorist attack
of September 11, 200, during the president's visit to a
Florida classroom. The meme, as a whole, advances the
claim that the February 2023 Ohio train derailment was
a deliberate act orchestrated by the government. The
argument is assembled by drawing an analogy between
the Ohio derailment and the September 11 attacks, and
relies on the audience's knowledge of another conspiracy
theory about the US government's role in masterminding
the September 11 attacks despite assigning responsibility
to Osama Bin Laden. A Toulminian analysis of the argu-
ment assembled by the meme reveals the following struc-
ture: Since the Ohio train derailment is like the terrorist
attack (evidence invoked by the photograph), the derail-
ment is a US government conspiracy against its own people
(claim), because the 9/11 attacks were a government
inside-job (warrant). The meme constructs this argument
parsimoniously, with minimal image and text content.
Since the meme is boxed within its rectangular bound-
aries, audiences drawn to this line of reasoning are inhib-
ited from interrogating the implied evidence, that is,
questioning why the two tragedies must in fact be similar
to each other. The meme offers no reasons for asserting
the analogy. Likewise, the meme does not furnish evi-
dence (referred to as backing in the Toulminian frame-
work) in support of the warrant. Rather, the meme
counts on the audience believing that the 9/11 attacks
were pre-planned by the US government and that, in the
iconic photograph, the president was merely being
informed about the execution of the plan. Warrants are
often taken-for-granted assumptions that the audience is
expected to fill in. Nonetheless, in a robustly constructed
argument, backing is typically added to tighten the argu-
ment and make it resistant to counter-attack. Since image
MASCARENHAS ET AL.
7
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

## Page 8

memes offer limited visual space and benefit from con-
tainment within visual boundaries, they are rarely
expected to elaborate warrants. Instead, they derive rhe-
torical power precisely by activating the audience's previ-
ous engagement with other related claims.
Barnes et al. (2021) found that text and image jointly
enhance predictive power of a meme's virality. We note
that text and image juxtapositions can enhance another
impact of memes—their argument potency. In the meme
in Figure 1, Panel 3, the logic of the argument is con-
structed by the iconic 9/11 image template. Audiences
that follow the meme's logic do so because they are
already aware of the alleged government conspiracy
related to 9/11. The meme pits the audience that agrees
with its claim against devious officials and gullible people
who trust official narratives about the train derailment.
The rhetorical deftness of this particular meme lies in its
ability to draw an audience, in the course of a single
engagement with the meme, into both the line of reason-
ing set up by the meme and into an audience identity.
Even as a viewer encounters the meme's reasoning for
the
first
time, having followed the
reasoning
and
accepted it, the viewer comes to embody the persona of a
skeptic of official narratives.
Image memes have constitutive potential; that is, they
simultaneously call into being (constitute) audience
groups while influencing their thinking and possibly
action—a process that rhetoricians call interpellation
(Charland, 1987). This constitutive potential is contained
in the meme's ability to advance claims, provide/imply
evidence, and rely heavily on a discursive community to
supply the necessary warrants (assumptions) to complete
the argument (Mascarenhas, 2021). The capacity of image
memes to compel audience participation in semantic
decoding enhances the persuasive strength of memes
because deducing the meme's claim constructs a truth-
seeking experience, and consequently a sense of shared
in-group identity, for the audience. Having successfully
decoded the meme, audiences are interpellated as truth-
seekers which deepens their investment in the meme's
claim.
Another rhetorical feature of image memes which
makes them conducive to interpellating audiences as
truth seekers is that image memes are often free-floating,
appearing out of nowhere, and rarely disclosing their
sources,
unlike
other
digital
content
(Milner
&
Wolff, 2023). Image memes represent “an epistemic
break” (Mascarenhas et al., 2021, p. 4). They gain credi-
bility not because they are vetted by authoritative sources
but precisely because they are sourceless. This attribute
makes image memes “a powerful parallel discourse to
more formal media channels and, in many cases, a direct
challenge to information, claims, or narratives that
emerge
from
publicly-vetted
sources”
(Mascarenhas
et al., 2021, p. 4).
Figure 3 provides additional illustration of the argu-
mentative potential of image memes. In this case, the
visual compartmentalization of the meme-box is vital to
the enactment of the argument. The sequence guides the
viewer from the top to the bottom and from the left to
the right. The image at top center shows the actor Bill
Murray. The text superimposed on this image issues a
dare from the person sharing the meme to the viewer.
The assertion “Call me crazy all you want” alludes to the
trope of the conspiracy theorist, a label typically applied
to those who believe the government is guilty of large-
scale wrongdoing. The rest of the meme-box assembles
arguments to rebut the conspiracy theorist label.
The meme goes on to provide claim-evidence pairs in
the smaller boxes on the left-hand side. Four claims
about
government
malfeasance
are
supported
with
images meant to provide evidence. The first claim accuses
the U.S. government of lying about medical treatments.
The textual claim is placed over an image that invokes
the Tuskegee syphilis study which abused black Ameri-
cans in a deceptive government intervention (Tuskegee
Study – Timeline – CDC – OS, 2022). The second claim
accuses the government of destroying the planet and is
substantiated with the paired image of a mushroom
cloud that represents the atomic bombing of Hiroshima
(The Editors of Encyclopedia Britannica, 2023). The third
claim accuses the government of involvement in drug
trafficking. The accompanying image evidence references
the plane crash that exposed alleged CIA drug trafficking
activities
in
Panama
(Ex-CIA
Airline
Tied
to
Cocaine, 1987). The fourth box in the left-hand column
claims the US government carries $21 trillion in debt.
The paired image shows a vortex of dollar bills evoking
the metaphor of “money down the drain.” The preceding
images which draw from historical archives establish a
degree of credibility for the meme's claims, priming the
viewer to accept the truth of the final claim, even though
the fourth argument does not provide any direct empiri-
cal evidence.
The placement of image and text in the meme opti-
mizes the restricted space of the meme-box to arrange a
relatively complex argument comprising multiple claims
and pieces of evidence. Each text-image pairing on the
left aligns with the text-image pairing on the right to ver-
bally and visually accomplish an if-then argument pat-
tern. The claim-evidence pairs on the left act as evidence
for the broader claims on the right. For example, the gov-
ernment's deception in the Tuskegee study acts as evi-
dence for the claim that the government cannot be
trusted to provide health care. The argument relies on
the warrant that a nationalized health care system would
8
MASCARENHAS ET AL.
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

## Page 9

provide cover for the government to continue abuse of
unsuspecting citizens. Likewise, the government's will-
ingness to use military power to imperil the planet by
deploying nuclear weapons is provided as evidence that
the government should not be trusted to regulate gun
ownership. This argument rests on the warrant that
gun ownership provides security against military abuse.
The boundary around the image meme suppresses con-
sideration of contradictory warrants, such as the assump-
tion that guns would be powerless in the face of nuclear
destruction.
The goal of rhetorical analysis then becomes the iden-
tification of the primary and sub-claims within a meme,
as well as of the evidentiary tropes that support those
memetic claims. Focusing on claim-evidence-warrant in
image memes allows us to track public sensemaking
independent of demographic or psychographic data about
discourse communities. Rhetorical analysis foregrounds
the what rather than the who of public sensemaking,
opening
up
potentially
valuable
information
for
intervention messages to target lines of reasoning that
produce public beliefs and sentiments.
After explaining how single-image memes can be ana-
lyzed rhetorically, we turn toward the field of ecology for
inspiration to scale up rhetorical analyses of memes. An
ecological framework can allow us to trace how memetic
claims interact with each other to produce evidence eco-
systems that inform broader public narratives. Borrowing
from ecological concepts, we can study the life cycle,
movement, interaction, and impacts of image memes at
broader scales.
4.3
|
Ecological framework
Previous studies have described online discourse as infor-
mation ecologies, drawing attention to striking similari-
ties between features of virtual communication spaces
and those of concrete physical ecosystems (Kuehn, 2022).
For instance, both domains exhibit intricate networks of
FIGURE 3
Bill Murray image
meme. Described in text.
MASCARENHAS ET AL.
9
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

![page9_img1.jpeg](images/page9_img1.jpeg)

## Page 10

interrelated elements, diverse populations, and dynamic
interactions
that
shape
and
are
shaped
by
their
environments.
Ecosystem
metaphors
can
be
valuable
tools
in
researching information flows. They enable scholars to
more effectively apprehend abstractions by providing
concrete frames of reference from the natural world.
Such metaphors can be helpful when investigating phe-
nomena such as online communities, where interactions
among users resemble symbiotic relationships in natural
ecosystems, or when examining the spread of informa-
tion and ideas, which can mirror the propagation of spe-
cies within a habitat. The use of ecosystem metaphors
can play a central role in facilitating communication
among researchers from different disciplinary back-
grounds. By drawing upon ecology, scholars can bridge
the
gaps
between
their
respective
fields,
fostering
collaboration and the exchange of knowledge. This cross-
disciplinary approach ultimately enriches our under-
standing of online information ecologies, revealing new
insights and fostering innovation in the study of digital
landscapes. Ecological perspectives have already been
applied to image meme research. For instance, Morina
and Bernstein (2022) conducted an ecosystem-level anal-
ysis to track where image memes originated and how
they spread online.
Our framework, the Digital Rhetorical Ecosystem
three-tier model (DRE3) (Figure 4), articulates a basic
architecture for collecting, classifying, and analyzing
memes to generate data about public beliefs and attitudes
accruing from image meme circulation (Mascarenhas
et al., 2021, 2022). Similar work has been operationalized,
for example by Tommasini et al. (2023) who created the
Internet Meme Knowledge Graph (IMKG) and Sharma
et al. (2023) who created MemeX. Below, we identify how
DRE3 can offer insights that are different from those pro-
duced by these existing analytic tools.
The DRE 3 theoretical framework comprises three
layers of analysis that move from observations of con-
crete detail in image memes to inferences about the pub-
lic sensemaking that arises from the circulation of and
interaction between memes. The initial Instrumental
layer describes empirical observations of the image meme
artifacts (i.e., entities such as people, places, events repre-
sented in an image meme). The Rhetorical layer identifies
the claims that emerge from an analysis of the semantic
and syntactic interactions between entities in image
memes. The Hidden layer traces broader narratives (that
reveal beliefs and sentiments) coalescing from interac-
tions between memetic claims. The DRE3 model fills in a
gap in the current landscape of image meme research, by
highlighting an intermediate rhetorical-semantic layer
between the instrumental layer of data collection and the
inferential layer that identifies deeper hidden states such
as public narratives.
If the DRE3 framework is used to guide an image
meme analysis pipeline, by making argument claims the
key analytic feature, the analysis can trace not just
the movement and evolution of specific image memes
but rather the claims they generate, which result in evi-
dence ecosystems that ultimately influence public sense-
making.
Currently,
many
large-scale
computational
studies of image memes identify broader sentiments that
image memes produce (e.g., racial hatred). As Tommasini
et al. (2023) have noted, studies of image memes have
thus far primarily examined “their spread over time” or
engaged in “high-level classification tasks like hate
speech detection, while a principled analysis of their
stratified semantics is missing” (p. 1). Their creation, the
Internet Meme Knowledge Graph, does arrive at a
semantic analysis of image memes. In comparison, the
DRE3 model refines semantic analysis by honing in on
the claims produced by image memes, that is, their per-
suasive potential. The image meme of G.W. Bush being
informed about 9/11 is important to recognize as a cul-
tural touchstone. However, more important are the
implicit claims this image evokes each time it is deployed
in a meme that includes text (i.e., the claim that the gov-
ernment has lied about a particular public event). There-
fore an uptick in public distrust of the government
(sentiment) can be traced back to specific trending claims
that help explain how the government's role in current
events is being perceived in online ecosystems and con-
tributing to the uptick in distrust.
In order to arrive at meaningful inferences in the hid-
den layer, the DRE3 framework invites the development
of two processes—a method for collecting image memes
as they appear across social media networks to generate
image meme data at large scales, and the automation of
claim identification by moving from trained human
FIGURE 4
The Digital Rhetorical Ecosystem three-tier model
(DRE3). The Instrumental, Rhetorical, and Hidden layers are
described in the text.
10
MASCARENHAS ET AL.
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

![page10_img1.png](images/page10_img1.png)

## Page 11

coders to trained machine learning systems. To note,
DRE3 could complement other approaches (e.g., already
existing computational studies using entity recognition
and Optical Character Recognition). In fact, DRE3 could
be integrated with existing image meme knowledge
graphs such as the previously mentioned Internet Meme
Knowledge Graph and MemeX. DRE3's unique offering,
however, is its foregrounding of the rhetorical layer of
analysis, namely the articulation of quasi-arguments that
build evidence ecosystems with claims, a focus which is
not currently represented among computational analyses
of memes or meme encyclopedias. Once capabilities are
developed for capturing and tracing the emergence,
movement, and decline of memetic claims across digital
publics, inferences about public beliefs and sentiments
can be more closely tied to the underlying persuasive
mechanisms (specifically the evidence ecosystems) that
produce these hidden state effects.
Besides conceptualizing the impact of image meme
circulation in terms of evidence ecosystems, ecological
theory can inform the generation of research questions to
yield rich data about the ways in which image memes
and the arguments they assert interact to produce social
cognition. Some ecosystem concepts that can provide use-
ful parallels for queries in a large-scale computational
analysis of image memes are Life History, Niche Succes-
sion, and Complex Interactions. Below, we define each of
these concepts and transpose the ecological perspective
onto image meme analysis. While previous work has
examined memes ecologically (e.g., Ford et al., 2021;
Morina & Bernstein, 2022), the advantage of the DRE3
framework is the application of argumentation analysis
to trace memetic claims. As such, while other studies
have examined the evolution of memes (templates and
captions), the interaction of memes with their semiotic
backgrounds, and the competition between memes,
DRE3 pushes the inquiry further to ask about the devel-
opment and eclipse of memetic claims as well as how
claims might interact with each other and with their
semiotic environments to produce dynamic evidence eco-
systems that drive belief, sentiment, and action in differ-
ent online publics.
4.3.1
|
Life history of image memes
arguments
Life history, in ecology, refers to the series of events an
organism goes through from birth to death. While web-
sites like Know Your Meme maintain records of the ori-
gin,
evolution,
and
spread
of
image
memes,
the
application of DRE3 can trace the same dynamics for
memetic claims. Life history analysis could also yield
insights about how cultural and social events produce
semiotic contexts that influence the emergence, develop-
ment, or decline of image memes and their claims.
4.3.2
|
Niche succession in online
communities
Niche succession is the process by which the composition
of species in a particular ecological community changes
over time in response to changes in the physical or bio-
logical environment. This concept could be applied to
trace changes in the rhetorical composition (i.e., patterns
of claims) through time, for a given sampling location
(e.g., a forum or content channel). Changes in diversity
of memetic claims could also yield useful insights about
how online communities may be converging around spe-
cific beliefs or if there is competition between memetic
claims in online communities.
4.3.3
|
Complex interactions between
memetic claims
Complex interactions refer to the many ways in which
ecological entities interact with each other and with their
environments. These interactions can be direct or indi-
rect, and can occur at many different spatial and tempo-
ral scales. Likewise, within image meme ecosystems,
researchers could trace collaboration, competition, or
conflict between memetic claims gaining insight into
how evidence ecosystems for particular beliefs crystallize,
endure, or dissolve.
5
|
OPERATIONALIZING
COLLABORATIVE ANALYSIS OF
MEMETIC CLAIMS
In previous work (Mascarenhas et al., 2021), we have
offered guidance for operationalizing DRE3 into data col-
lection and analysis architectures. In this paper, we offer
clarification of one particular analytic hurdle that is
likely to accompany large-scale annotation of claims from
image meme data—that is, conflicting interpretations of
memetic content and resulting claims. DRE3 is a rela-
tively
uncomplicated
research
paradigm
to
identify
memetic claims and hidden states for the individual ana-
lyst or small teams of analysts (with the capacity to estab-
lish inter-coder reliability). However, scaling up to make
inferences about massive volumes of image meme data
will require larger-scale and more complex collaboration,
both to gather vast quantities of image memes and to
facilitate human and eventually machine annotation of
entities within image memes and the claims asserted by
MASCARENHAS ET AL.
11
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

## Page 12

the memes. Image meme discourse can be highly subjec-
tive, volatile, fluid, and cloaked in rapidly changing
slang, symbolism, or esoterica, as well as heavily depen-
dent on local information contexts. When multiple agents
analyze claims produced by image memes, conflicts over
both trivial and critical aspects of interpretation will be
inevitable. To resolve this, large scale implementation of
DRE3 could benefit from the use of fuzzy set theory.
Any classification system, because of subjectivity of
meaning and class membership, will have to manage
conflicts
in
classification
of
objects
(Mascarenhas
et al., 2022; Russell, 2009). This problem is generally
addressed using agreed upon evaluative standards. How-
ever, in a highly subjective information space with a
diversity of use-cases, disagreement over standards them-
selves can make universal or near-universal voluntary
adoption of standards impossible, and their forced adop-
tion, counterproductive. Unresolvable conflicts over cri-
teria and classifications would cause difficult-to-measure
information quality problems (Mascarenhas et al., 2022).
The use of fuzzy set theory holds promise for converting
problems of inconsistency among classifications and stan-
dards for identifying memetic claims into a valuable
source of data that can inform the study of image memes
and allow for qualitative analyses at scale.
Set theory is a mathematical field concerned with
measurement of and operations on sets or collections of
abstract elements, where elements might be numbers,
abstract objects, potential outcomes of an event, or other
sets. In standard set theory, there is no ambiguity regard-
ing the member of an element in a set (e.g., The set of
integers less than or equal to 5). However, outside of pure
mathematics, an empirical world of ambiguity often
leaves membership of an object to a category an ongoing
conflict, even where there appear to be clear rules and
evaluative criteria (e.g., “Is a hotdog a sandwich? Or an
exception to the class sandwich?”, “Does this meme refer
to that entity? Or another?”). Fuzzy set formalism is a
scale- and context-agnostic answer to address this incon-
venient inconsistency or fuzziness in evaluation of real-
world object membership to semantic sets and objects
with dynamic values to mathematical sets (Zadeh, 1965;
Zimmermann, 2010). Any individual element can be
described as a 2-dimensional vector, (1) the abstract
object familiar in traditional set theory and (2) the proba-
bility of its membership to a given set. For example, con-
sider the element: “The result of rolling a six sided die”
(d6), which resolves to some number between 1 and
6, and the set: “Numbers which are less than or equal to
3” (set A); d6 can be represented as belonging to set A in
terms of its probability of resolving to a number less than
or equal to 3 (i.e., {d6, 0.5}  A or “d6 has a 50% chance
of belonging to set A”).
Within the context of DRE3, fuzzy formalisms allow an
analyst's process of entity detection and claim identification
from an image meme to produce a fuzzy output in the
form of an entity assertion or claim assertion, wherein the
analyst's assignment is not a final classification, but a con-
tribution to a set of fuzzy annotations about the presence
of an entity or implication of a claim in a given image
meme (Figure 5). Fuzzy annotations could also include
negative values in order to facilitate disputes over classifica-
tion (e.g., where an analyst is disputing another's assertion,
and feels 80% sure that an entity is not present in the
image meme, the divergence might be represented as an
assertion of the entity at a value of 0.8). A final assign-
ment or classification within this scheme is not required.
Instead, conflict in outputs is no longer noise in measure-
ment or a problem of intercoder reliability, but, rather,
valuable data. Disparities in classification and assignment
are rendered valuable measurements, indicating polariza-
tion, volatility in classification, or differences in training
and knowledge of the meme's semantic contexts among
analysts. These disparities offer opportunities beyond the
analysis of image memes, such as the assessment of analyst
bias and the production of structured training data for
automated systems. The fuzzy set approach also circum-
vents the need for universal adoption of one standard, as
any method with outputs that associate claims or entities
with image memes (e.g., machine learning and similar
approaches) could be assigned probability values (either by
manual estimation or calculation) and integrated as asser-
tions. Any relevant data representation which makes use of
fuzzy formalisms would lend itself to interoperability.
Consequently, DRE3 represented through the use of
fuzzy formalisms can both extend the value of other
methods
as
opposed
to replace
them,
and,
where
adopted, can take what used to be an information quality
problem (i.e., disagreement on classification) and convert
it into an opportunity for communities with disparate
views to interoperate and collaborate. In this process, a
diverse sampling of assertions about memetic claims is as
important as a diverse sampling of the memes them-
selves. As such, DRE3 annotation should complement
and enrich the analysis of observation-based models that
focus on variables such as the spread of specific identical
image memes (e.g., as done by Hui et al., 2018).
6
|
PROVOCATIONS FOR FUTURE
RESEARCH USING A RHETORICAL-
ECOLOGICAL-COMPUTATIONAL
FRAMEWORK
We offer DRE3 as a paradigm for research on image
memes as public sensemaking artifacts. DRE3 can inform
12
MASCARENHAS ET AL.
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

## Page 13

the development of a stand-alone pipeline for collecting
image memes, annotating claims, and tracing evidence
ecosystems accruing from interactions between claims.
However, the key feature of DRE3 (identification of argu-
ments and specifically claims in image memes) can also
be incorporated into already developed knowledge graphs
for image memes.
DRE3 builds interdisciplinary synthesis between the
fields of rhetoric, ecology, and information sciences,
benefiting from the transferable insights of these fields.
Large-scale computational analyses can be semantically
enhanced by incorporating the rhetorical layer (identifi-
cation of claims). DRE3 can be human-interfaceable
which ensures that the system can maintain semantic
accessibility even when scaling up. Additionally, DRE3
can be utilized independently at any scale without the
need for internet connectivity or significant computa-
tional resources. DRE3 also goes beyond snapshot ana-
lyses of image memes, which may quickly become
outdated, to offer a research framework that aligns with
the dynamic nature of image meme ecosystems.
We urge cross-disciplinary teams of researchers to
draw from the DRE3 framework to construct collection
and analysis pipelines that foreground memetic claims or
to incorporate claim annotation in existing image meme
encyclopedias or knowledge graphs. A particular use case
for DRE3 application is modeling patterns of emergence
and circulation of image memes and their underlying
claims within information ecosystems, so as to track
abnormalities that may indicate facilitation of informa-
tion pollution by state actors or paid influence groups
(see Cunningham, 2023). DRE3's ecological analysis of
image
memes
may
offer
valuable
data
to
support
intervention efforts. For example, tracing the life history
of image memes and sharing that data publicly could
potentially serve as a more neutral and impactful inter-
vention when compared with current fact-checking prac-
tices. When provided statistics about a meme's content,
origin, and trajectory, audiences could be made aware,
for example, of whether a memetic claim was spread
inorganically by a state actor or influence agent, rather
than by more typical social media circulation patterns.
Access to such data may undermine the meme's impact
in spreading the claim without need for refutation of the
meme's argument, itself.
DRE3's rhetorical focus on the argumentative ele-
ments of the image meme could also offer more targeted
data to support current fact-checking practices. Earlier,
fact-checking was the domain of “news agencies and
other independent vetting organizations such as Snopes,
PolitiFact, factcheck.org [that] posted fact-check notices
on misleading claims… not… in situ alongside the original
misinformation, but […] on the vetting agency's own web-
site
alongside
samples
of
the
misinformation”
(Wasike, 2023, p. 1). However, as information pollution
accelerated on social networking sites, such as Facebook
and X (formerly Twitter), these sites began to issue their
own fact-checking artifacts “via obvious warning labels
that accompany questionable posts” (Wasike, 2023, p. 1)
getting users' attention at the moment of encountering
spurious information, itself. Fact-checking by social
media companies is vigorously debated. The states of
Texas and Florida, in the United States, passed laws, cur-
rently being argued before the U.S. Supreme Court, that
curtail the ability of social media companies to moderate
content on their platforms, citing partisan censorship in
FIGURE 5
Potential fuzzy data
representation of the DRE3 model. An
asterisk represents a pointer to an
external object, and brackets indicate an
array of objects.
MASCARENHAS ET AL.
13
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

![page13_img1.jpeg](images/page13_img1.jpeg)

## Page 14

content moderation (Howe, 2024). Specific fact-checking
practices such as X's Community Notes (Elliott &
Gilbert, 2023) and Facebook's use of particular fact-
checking organizations (Meade, 2023) have also gener-
ated controversy, highlighting the contested and evolving
nature of fact-checking in an information landscape that
itself is increasingly dynamic and difficult to monitor.
Further, research has shown that fact-checking efficacy is
mixed. Walter et al.'s (2020) meta-analysis found some
evidence that “exposure to fact-checking carries positive
influence” in correcting beliefs but that “the effects of
fact-checking on beliefs are quite weak and gradually
become negligible the more the study design resembles a
real-world scenario of exposure to fact-checking” (p. 367).
Wasike (2023) found that “social media fact-checks had a
minimal impact on the likelihood to share misinforma-
tion” p. 5). Self-report data revealed that social media
users “who had been fact-checked before were also more
likely to post misinformation than those who had not
been fact-checked… [similar to] users who had experi-
enced content deletion” (Wasike, 2023, p. 5). Self-report
assertions that individuals who post misinformation are
not deterred by fact-checking may suggest that image
memes are self-consciously used to challenge mainstream
positions, and that spreaders of misinformation may
believe their positions are upheld by reasoning that is
superior to that provided in fact-checks.
Hameleers and van der Meer (2020) found that
responses to fact-checking efforts reflect confirmation
bias (i.e., viewers are drawn to facts they already hold to
be true). Audiences are likely to ignore content that leads
with a claim that counters their own. This possibility
raises the need to study the rhetorical forms common to
fact-checking artifacts and the persuasive efficacy of these
conventions against memetic claims. For example, fact-
checking that tends to focus more heavily on asserting
corrective claims, rather than on debunking arguments
that support spurious claims, leaves intact the spurious
evidence ecosystems that memetic claims build over time.
Efforts to safeguard the health of information ecosystems
could pay closer attention to how memetic arguments
produce evidence ecosystems in support of beliefs. By
analyzing claims across large data sets of image memes,
analyses can go beyond identifying what spurious or
harmful beliefs may be circulating in information ecosys-
tems to tracing why audiences come to accept those
claims because of the evidence ecosystems that grow
from the claims, evidence, and warrants carried by image
memes. Tracing memetic claim circulation can expose
the strength of particular beliefs, potentially before those
beliefs are expressed in public action. For example, retro-
spective analysis of Facebook posts from only a subset of
public groups on the social media site, revealed strong
social belief momentum “attacking the legitimacy of Joe
Biden's victory” alongside “calling for executions or other
political violence,” indicating the potential for disruption
on the January 6th counting of Electoral College votes
(Silverman et al., 2022). An advantage of focusing on
image memes and their claims is that tracking public
beliefs does not require tracking online users because the
memes themselves are regarded as units of social
cognition.
Analyzing the evidence ecosystems that accrue from
the circulation of image meme claims could also provide
in-roads for addressing breakdowns in social consensus
on various public issues, for example climate change
skepticism. Applying Toulminian analysis to identify
claims, evidence and warrants, both explicit and implicit
within image memes, can help trace lines of reasoning
applied by online audiences who challenge mainstream
positions on these issues. Audiences who share image
memes that contradict mainstream positions tend to be
invested in the belief that they think more critically than
the norm. Therefore, the advantage to grasping “how”
online publics support their beliefs is that any interven-
tion efforts, such as fact-checking, can focus on rebutting
particular memetic arguments that are salient to audi-
ences. A new potential avenue for countering disinforma-
tion also opens up. Memes can be used to expose the
weakness of target memes, by addressing missing evi-
dence or implied warrants using the image meme vernac-
ular, itself. With this strategy, corrective image memes
would not introduce competing claims (as current fact-
checking efforts do), but rather they would demonstrate
the weakness of memetic arguments in already circulat-
ing image memes, a strategy that could undermine audi-
ences' confidence in using image memes as displays of
critical
thinking.
Constructing
and
studying
image
memes that attack lines of reasoning in memetic argu-
ments warrants its own future work.
In this paper, we have made the case for why image
memes should be treated as quasi-arguments, how Toul-
minian theory can be applied to analyze arguments made
by image memes, how combining rhetorical and ecologi-
cal approaches can offer analytic advantage, and how
fuzzy set theory can address the problem of ambiguity in
image meme interpretation. Our purpose in articulating
the DRE3 framework is to provoke the construction of an
image meme repository and analysis pipeline that can
add to ongoing development in this area. However, ele-
ments of the framework can also be incorporated piece-
meal into existing computational architectures that study
image memes. In particular, we encourage analyses to
regard image memes as argument artifacts that assert
14
MASCARENHAS ET AL.
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

## Page 15

claims and to trace how these memetic claims assemble
into evidence ecosystems for a variety of issues, especially
those impacted by breakdowns in social consensus.
ORCID
Mridula Mascarenhas
https://orcid.org/0000-0002-
3458-1590
REFERENCES
Afridi, T. H., Alam, A., Khan, M. N., Khan, J., & Lee, Y.-K. (2021).
A multimodal memes classification: A survey and open
research issues. Innovations in Smart Cities Applications, 4,
1451–1466. https://doi.org/10.1007/978-3-030-66840-2_109
Barnes, K., Riesenmy, T., Trinh, M. D., Lleshi, E., Balogh, N., &
Molontay, R. (2021). Dank or not? Analyzing and predicting
the popularity of memes on Reddit. Applied Network Science,
6(1), 21. https://doi.org/10.1007/s41109-021-00358-7
Benveniste, A. (2022, January 26). The meaning and history of
memes. The New York Times. https://www.nytimes.com/2022/
01/26/crosswords/what-is-a-meme.html
Beskow, D. M., Kumar, S., & Carley, K. M. (2020). The evolution of
political memes: Detecting and characterizing internet memes
with multi-modal deep learning. Information Processing &
Management, 57(2), 102170. https://doi.org/10.1016/j.ipm.2019.
102170
Boxman-Shabtai, L., & Shifman, L. (2014). Evasive targets: Deci-
phering polysemy in mediated humor. The Journal of Commu-
nication, 64(5), 977–998. https://doi.org/10.1111/jcom.12116
Charland, M. (1987). Constitutive rhetoric: The case of the peuple
québécois. The Quarterly Journal of Speech, 73(2), 133–150.
https://doi.org/10.1080/00335638709383799
Condescending Wonka / Creepy Wonka. (2012, January 13). Know
your meme. https://knowyourmeme.com/memes/condescending-
wonka-creepy-wonka
Cordes,
R.
J.,
Applegate-Swanson,
S.,
Friedman,
D.
A.,
Knight, V. B., & Mikhailova, A. (2021). Narrative information
management. In R. J. Cordes & D. A. Friedman (Eds.), Narra-
tive information ecosystems: Conflict and trust on the endless
frontier (pp. 1–64). COGSEC.
Cordes, R. J., David, S., Maan, A., Ruiz, A., Sapp, E., Scannell, P., &
Shah, S. (2021). In R. J. Cordes (Ed.), The narrative campaign
field guide – First edition (1st ed.). Narrative Strategies Ink.
https://www.narrative-strategies.com/ncfg
Cunningham, A. (2023). Image warfare: The use of memes in the
production of misinformation. http://www.cornellpolicyreview.
com/image-warfare-the-use-of-memes-in-the-production-of-
misinformation/
Dancygier, B., & Vandelanotte, L. (2017). Internet memes as multi-
modal constructions. Cognitive Linguistics, 28(3), 565–598.
https://doi.org/10.1515/cog-2017-0074
Dynel, M. (2016). “I has seen image macros!” Advice animals
memes as visual-verbal jokes. International Journal of Commu-
nication Systems, 10, 29.
Elliott, V., & Gilbert, D. (2023). Elon Musk's main tool for fighting
disinformation on X is making the problem worse, insiders
claim.
Wired.
https://www.wired.com/story/x-community-
notes-disinformation/
Ex-Cia
Airline
Tied
to
Cocaine.
(1987,
January
20).
The
Washington Post. https://www.washingtonpost.com/archive/
politics/1987/01/20/ex-cia-airline-tied-to-cocaine/d7e5a04f-
462f-479f-bf45-11502e772082/
Ford, T., Krohn, R., & Weninger, T. (2021). Competition Dynamics
in the Meme Ecosystem. arXiv [cs.SI]. http://arxiv.org/abs/
2102.03952
Grundlingh, L. (2017). Memes as speech acts. Social Semiotics, 28,
147–168. https://doi.org/10.1080/10350330.2017.1303020
Guenther, L., Ruhrmann, G., Bischoff, J., Penzel, T., & Weber, A.
(2020). Strategic framing and social media engagement: Analyz-
ing memes posted by the German Identitarian movement on
Facebook. Social Media + Society, 6(1), 2056305119898777.
https://doi.org/10.1177/2056305119898777
Hagen, L., Greyson, D., Fox, A., Koltai, K., & Dumas, C. (2021).
Social media, vaccines, and partisan division of health informa-
tion. Proceedings of the Association for Information Science and
Technology, 58(1), 594–597. https://doi.org/10.1002/pra2.506
Hahner, L. A. (2013). The riot kiss: Framing memes as visual argu-
ment. Argumentation and Advocacy, 49(3), 151–166. https://doi.
org/10.1080/00028533.2013.11821790
Hameleers, M., & van der Meer, T. G. L. A. (2020). Misinformation
and Polarization in a High-Choice Media Environment: How
Effective
Are
Political
Fact-Checkers?
Communication
Research, 47(2), 227–250. https://doi.org/10.1177/0093650218
819671
Hazman, M., McKeever, S., & Griffith, J. (2023). Meme sentiment
analysis enhanced with multimodal spatial encoding and face
embedding. Artificial Intelligence and Cognitive Science, 318–
331. https://doi.org/10.1007/978-3-031-26438-2_25
Heiskanen, B. (2017). Meme-ing electoral participation. European
Journal of American Studies, 12(2). https://doi.org/10.4000/ejas.
12158
Highfield, T., & Leaver, T. (2016). Instagrammatics and digital
methods: Studying visual social media, from selfies and GIFs to
memes and emoji. Communication Research and Practice, 2(1),
47–62. https://doi.org/10.1080/22041451.2016.1155332
Howe, A.
(2024).
Supreme court skeptical
of
Texas, Florida
regulation of social media moderation. SCOTUSblog. https://
www.scotusblog.com/2024/02/supreme-court-skeptical-of-
texas-florida-regulation-of-social-media-moderation/
Hui, P.-M., Weng, L., Sahami Shirazi, A., Ahn, Y.-Y., & Menczer, F.
(2018). Scalable detection of viral memes from diffusion pat-
terns. In S. Lehmann & Y.-Y. Ahn (Eds.), Complex spreading
phenomena in social systems: Influence and contagion in real-
world social networks (pp. 197–211). Springer International
Publishing. https://doi.org/10.1007/978-3-319-77332-2_11
Huntington, H. E. (2013). Subversive memes: Internet memes as a
form of visual rhetoric. https://spir.aoir.org/ojs/index.php/spir/
article/view/8886/pdf
Image Macros. (2020). Know your meme. https://knowyourmeme.
com/memes/image-macros
Introne, J., Korsunska, A., Krsova, L., & Zhang, Z. (2020). Mapping
the narrative ecosystem of conspiracy theories in online anti-
vaccination discussions. International Conference on Social
Media and Society, 184–192. https://doi.org/10.1145/3400806.
3400828
Isaacs, D. (2020). Memes. Journal of Paediatrics and Child Health,
56(4), 497–498. https://doi.org/10.1111/jpc.14755
MASCARENHAS ET AL.
15
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

## Page 16

Jones,
M.,
Beveridge,
A.,
Garrison,
J.
R.,
Greene,
A.,
&
MacDonald, H. (2022). Tracking memes in the wild: Visual rhe-
toric and image circulation in environmental communication.
Frontiers in Communication, 7. https://doi.org/10.3389/fcomm.
2022.883278
Joshi, S., Ilievski, F., & Luceri, L. (2023). Contextualizing internet
memes across social media platforms. arXiv [cs.SI]. http://arxiv.
org/abs/2311.11157
Kofman, A. (2018, October 25). Bruno Latour, the post-truth philos-
opher, mounts a defense of science. The New York Times.
https://www.nytimes.com/2018/10/25/magazine/bruno-latour-
post-truth-philosopher-science.html
Kougia, V., Fetzel, S., Kirchmair, T., Çano, E., Baharlou, S. M.,
Sharifzadeh, S., & Roth, B. (2023). MemeGraphs: Linking
memes to knowledge graphs. arXiv [cs.LG]. http://arxiv.org/
abs/2305.18391
Koutlis, C., Schinas, M., & Papadopoulos, S. (2023). MemeFier:
Dual-stage modality fusion for image meme classification. arXiv
[cs.CV]. http://arxiv.org/abs/2304.02906
Kuehn, E. F. (2022). The information ecosystem concept in infor-
mation literacy: A theoretical approach and definition. Journal
of the Association for Information Science and Technology, 74,
434–443. https://doi.org/10.1002/asi.24733
Ling,
C.,
AbuHilal,
I.,
Blackburn,
J.,
De
Cristofaro,
E.,
Zannettou, S., & Stringhini, G. (2021). Dissecting the meme
magic: Understanding indicators of virality in image memes.
Proceedings of the ACM Human-Computer Interaction, 5-
(CSCW1), 1–24. https://doi.org/10.1145/3449155
Ma, Y. (2021). Understanding Information: Adding a Non-individual-
istic Lens. Journal of the Association for Information Science and
Technology, 72(10), 1295–1305. https://doi.org/10.1002/asi.24441
Mascarenhas, M. (2021). Memes as quasi-argument: An insidious
threat to public debate. In Local theories of argument (1st ed.,
pp. 385–390). Routledge. https://doi.org/10.4324/9781003149026-65
Mascarenhas, M., Cordes, R. J., Bleu Knight, V., Murphy, S., &
Friedman, D. A. (2022). Tracking public Sensemaking through
rhetorical annotation of memes. In S. David, R. J. Cordes, &
D. A. Friedman (Eds.), Structuring the information commons:
Open standards and cognitive security (pp. 310–350). COGSEC.
Mascarenhas, M., Cordes, R. J., & Friedman, D. A. (2021). Digital
rhetorical ecosystem analysis: Sensemaking of digital memetic
discourse. In R. J. Cordes & D. A. Friedman (Eds.), Narrative
information ecosystems: Conflict and trust on the endless frontier
(pp. 65–134). COGSEC.
Meade, A. (2023). RMIT's fact check reinstated by Facebook two
months after suspension over News Corp voice complaints. The
Guardian. https://www.theguardian.com/australia-news/2023/
nov/08/rmit-factlab-fact-check-service-reinstated-facebook-
suspension-voice-referendum
Milner, R. M., & Wolff, P. (2023). On the meme train to Sylt: Meme-
tic becoming and ambivalent identification online. Social Media
+ Society, 9(1), 20563051231158825. https://doi.org/10.1177/
20563051231158825
Morina, D., & Bernstein, M. S. (2022). A web-scale analysis of the
community origins of image memes. arXiv [cs.HC]. http://
arxiv.org/abs/2204.05439
Potnis, D., & Tahamtan, I. (2021). Hashtags for gatekeeping of
information on social media. Journal of the Association for
Information Science and Technology, 72(10), 1234–1246. https://
doi.org/10.1002/asi.24467
Robertson, C., & Cochrane, E. (2023, February 15). In Ohio town
where train derailed, anxiety and distrust are running deep.
The New York Times. https://www.nytimes.com/2023/02/15/
us/ohio-train-derailment-anxiety.html
Russell, B. (2009). The philosophy of logical atomism. Routledge.
https://play.google.com/store/books/details?id=
jNOLAgAAQBAJ
Sharma, S., Kulkarni, A., Suresh, T., Mathur, H., Nakov, P.,
Akhtar, M. S., & Chakraborty, T. (2023). Characterizing the
entities in harmful memes: Who is the hero, the villain, the vic-
tim? arXiv [cs.CL]. http://arxiv.org/abs/2301.11219
Sharma, S., Ramaneswaran, S., Arora, U., Akhtar, M. S., &
Chakraborty, T. (2023). MEMEX: Detecting explanatory evi-
dence for memes via knowledge-enriched contextualization.
arXiv [cs.CL]. http://arxiv.org/abs/2305.15913
Shifman, L. (2014). The cultural logic of photo-based meme genres.
Journal of Visual Culture, 13(3), 340–358. https://doi.org/10.
1177/1470412914546577
Silverman, C., Timberg, C., Kao, J., & Merrill, J. B. (2022, January
4). Facebook hosted surge of misinformation and insurrection
threats in months leading up to Jan. 6 attack, records show.
https://www.propublica.org/article/facebook-hosted-surge-of-
misinformation-and-insurrection-threats-in-months-leading-
up-to-jan-6-attack-records-show
Smith, N., & Copland, S. (2022). Memetic moments: The speed of
twitter memes. Journal of Digital Social Research, 4(1), 23–48.
https://doi.org/10.33621/jdsr.v4i1.95
Snowden, D. (2002). Narrative patterns: Uses of story in the third
age of knowledge management. Journal of Information &
Knowledge Management, 01(1), 1–6. https://doi.org/10.1142/
S021964920200011X
Taecharungroj, V., & Nueangjamnong, P. (2015). Humour 2.0:
Styles and types of humour and virality of memes on Facebook.
Journal of Creative Communications, 10(3), 288–302. https://
doi.org/10.1177/0973258615614420
Tang, R., Mehra, B., Du, J. T., & Zhao, Y. C. (2021). Framing a dis-
cussion on paradigm shift(s) in the field of information. Journal
of the Association for Information Science and Technology, 72(2),
253–258. https://doi.org/10.1002/asi.24404
The Editors of Encyclopedia Britannica. (2023). Atomic bombings
of Hiroshima and Nagasaki. Encyclopedia Britannica. https://
www.britannica.com/event/atomic-bombings-of-Hiroshima-
and-Nagasaki
Thompson, S. A. (2023, February 16). “Chernobyl 2.0”? Ohio train
derailment spurs wild speculation. The New York Times.
https://www.nytimes.com/2023/02/16/technology/ohio-train-
derailment-chernobyl.html
Tindale, C. W. (2017). Replicating reasons: Arguments, memes, and
the cognitive environment. Philosophy & Rhetoric, 50(4), 566–
588. https://doi.org/10.5325/philrhet.50.4.0566
Tommasini, R., Ilievski, F., & Wijesiriwardene, T. (2023). IMKG:
The internet meme knowledge graph. The Semantic Web, 20th
International
Conference,
354–371.
https://doi.org/10.1007/
978-3-031-33455-9_21
Toulmin, S. E. (1958). The uses of argument. Cambridge University
Press. https://philpapers.org/rec/TOUTUO-2
16
MASCARENHAS ET AL.
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

## Page 17

Tung, P. T. H., Viet, N. T., Anh, N. T., & Hung, P. D. (2023). Semi-
Memes: A semi-supervised learning approach for multimodal
memes
analysis.
arXiv
[cs.LG].
http://arxiv.org/abs/2304.
00020
Tuskegee Study – Timeline – CDC – OS. (2022, December 20). The
untreated syphilis study at Tuskegee timeline. https://www.cdc.
gov/tuskegee/timeline.htm
Walter, N., Cohen, J., Holbert, R. L., & Morag, Y. (2020). Fact-
checking: A meta-analysis of what works and for whom. Politi-
cal Communication, 37(3), 350–375. https://doi.org/10.1080/
10584609.2019.1668894
Wasike, B. (2023). You've been fact-checked! Examining the
effectiveness of social media fact-checking against the
spread
of
misinformation.
Telematics
and
Informatics
Reports,
11,
100090.
https://doi.org/10.1016/j.teler.2023.
100090
Zadeh, L. A. (1965). Fuzzy sets. Information and Control, 8(3), 338–
353. https://doi.org/10.1016/S0019-9958(65)90241-X
Zannettou, S., Caulfield, T., Blackburn, J., De Cristofaro, E.,
Sirivianos, M., Stringhini, G., & Suarez-Tangil, G. (2018). On
the origins of memes by means of fringe web communities.
Proceedings of the Internet Measurement Conference, 2018, 188–
202. https://doi.org/10.1145/3278532.3278550
Zenner, E., & Geeraerts, D. (2018). One does not simply process
memes: Image macros as multimodal constructions. In Cultures
and traditions of wordplay and wordplay research (pp. 167–194).
De Gruyter. https://doi.org/10.1515/9783110586374-008/html?
lang=en
Zimmermann, H.-J. (2010). Fuzzy set theory. WIREs Computational
Statistics, 2(3), 317–332. https://doi.org/10.1002/wics.82
How to cite this article: Mascarenhas, M.,
Friedman, D. A., & Cordes, R. J. (2024). Bridging
gaps in image meme research: A multidisciplinary
paradigm for scaling up qualitative analyses.
Journal of the Association for Information Science
and Technology, 1–17. https://doi.org/10.1002/asi.
24900
MASCARENHAS ET AL.
17
 23301643, 0, Downloaded from https://asistdl.onlinelibrary.wiley.com/doi/10.1002/asi.24900, Wiley Online Library on [16/05/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License


---
*Extraction method: pymupdf*
