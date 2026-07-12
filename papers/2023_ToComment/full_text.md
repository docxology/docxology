# Full Text: ToComment

> Extracted from `2023_ToComment.pdf`

---

## Page 1

Digital Rhetorical 
Ecosystem Analysis 
 
Sensemaking of Digital Memetic Discourse 
 
October 16, 2021 
 
Mridula Mascarenhas 1 
Richard J. Cordes 2,3  
Daniel A. Friedman 2,4 
(1) California State University Monterey Bay , School of Humanities & Communication  
(2) COGSEC, 
(3) Atlantic Council GeoTech Center , 
(4) University of California, Davis, Dept. of Entomology & Nematology  
A B S T R A C T
 
This paper makes a case for integrating frameworks from two different knowledge 
domains, rhetorical studies and ecological studies, to catalog, monitor, and study 
digital image meme data, in order to support a more robust understanding of how 
memes produce and disseminate online narratives. In the digital public sphere, the 
primacy of image-based communication motivates an over-reliance on the image 
meme for public argumentation. Despite its ubiquity, the image meme format is 
currently understudied in large scale digital data analyses, relative to text-based 
formats such as natural language and hashtags. We argue that using a rhetorical 
approach (which emphasizes message form and audience) in large-scale analyses of 
multimedia and other digital artifacts can enhance analytic tools for categorizing, 
indexing, searching, and modeling online discourse. Further, by integrating a 
rhetorical and an ecosystem approach to studying digital discourse, we can formally 
trace multimedia rhetorical artifacts like image memes across platforms, media types, 
and languages. Combined rhetorical and ecosystem analyses can reveal how digital 
artifacts like image memes create, sustain, and disrupt public narratives and, thereby, 
socio-political dynamics. Three key elements of our approach are a) recognizing how 
parsimony and polysemy give image memes narrative power, b) focusing on how 
image memes engage audiences through identity construction, and c) applying 
“Rhetorical Ecosystem” mapping, based upon toolkit transfer and system design 
implications. Drawing from concepts in rhetoric, ecology, and complex systems 
analysis we introduce a Digital Rhetorical Ecosystem three-tiered model (DRE3) to 
explain how memes impact public narratives and beliefs. We then explore 
implications of this DRE3 model for the design and development of systems for 
computational analysis of digital discourse. 
 
Digital Rhetorical 
Ecosystem Analysis

## Page 2

Digital Rhetorical Ecosystem Analysis, 2021 
 
 
 
Contents 
I. A Rhetorical Approach to Understanding the Impact of Image Memes ..... 1 
What does a rhetorical approach to the study of memes entail? ................. 3 
Rhetorical Anatomy of an Image-Meme ....................................................... 5 
II. Ecological Extensions of Rhetorical Analysis: Trends and Theory ......... 10 
III. The Digital Rhetorical Ecosystem Three-Tier (DRE3) Model ............... 12 
Ecology: Key concepts and mappings ..................................................... 14 
Implications .................................................................................................. 23 
IV. The Digital Rhetorical Ecosystem three-tier model ................................ 28 
Example I ..................................................................................................... 30 
Example II.................................................................................................... 33 
V. Toward a High-Throughput Rhetorical Analysis (Meme SCADA) .......... 37 
Narrative Intelligence .................................................................................. 38 
Toward a Meme SCADA ............................................................................. 49 
VI. Discussion .................................................................................................. 53 
Conclusions and Recommendations ........................................................... 55 
Funding and Acknowledgements .................................................................... 57 
Works Cited ..................................................................................................... 58

## Page 3

Digital Rhetorical Ecosystem Analysis, 2021 
 
1 
I. A Rhetorical Approach to Understanding 
the Impact of Image Memes 
We are in the throes of a widespread epistemic crisis that is damaging 
individual and collective sensemaking function and capacity ([1,2]). The 
crisis, articulated as “a state of affairs in which partisans disagree not 
simply on policy, but on facts themselves” [3], is attributed to a set of 
conditions including a “combination of political polarization, declining 
trust in media institutions, and asymmetric media ecosystems” ([3], 
para. 
1). 
Concern 
about 
fake 
news, 
alternative 
facts, 
and 
misinformation has been escalating. Despite legitimate concerns about 
the degradation of public information due to the infusion of spurious 
content, we argue that viewing the information crisis as a competition 
between truth and falsity obscures the nature of the digital info rmation 
crisis we are facing and, worse still, hamstrings efforts to restore trust 
and rework social consensus, which are essential for collective social 
action. Rather than approach the digital information problem as a battle 
between true and fake information, we urge attention to the rhetorical 
conditions and processes that contribute to eroding trust in established 
channels of information, and mainstream institutions and publics.  
Framing the crisis as a battle between true and fake information has 
not proved effective in regaining the trust of those disaffected by 
mainstream channels of information. A simplistic true/fake dichotomy 
ignores the rhetorical conditions that have allowed competing 
narratives to displace mainstream ones. The hyper-complexity of digital 
information ecosystems is one such condition that makes achieving 
consensus on facticity and truth highly challenging [4], a condition that 
has, indeed, been exploited by malevolent actors. Nevertheless, 
addressing our epistemic crisis requires more than targeting and 
neutralizing sources of misinformation. We advocate a framework that 
combines rhetorical analysis with an ecosystem approach to trace the 
ebb and flow of narratives across digital publics. A rhetorical approach 
to understanding the information crisis focuses on message features 
that target audience vulnerabilities. An ecosystem approach goes 
beyond analysis of specific messages and audiences to highlight 
complex and long-term message-audience interactions, which can 
illuminate the changing web of narratives that influence public beliefs, 
opinions, and actions. Accordingly, we recommend addressing the 
epistemic crisis by developing a fine-grained understanding of the 
rhetorical forms and processes through which information circulates in

## Page 4

Digital Rhetorical Ecosystem Analysis, 2021 
 
2 
the digital public sphere and introducing rhetorical intervention as 
needed, rather than focusing exclusively on source control.  
Contemporary digital information ecosystems create particular burdens 
on individual and collective capacities for reliable sensemaking and 
robust public discourse. The increased volume and diversity of 
information on the Internet create unprecedented cognitive complexity, 
and challenge clarity and social agreement on issues of public concern 
[5]. The default mode of online engagement—rapid surfing through 
endless streams of information, rather than focused deep immersion in 
selective limited information—further curtails information-processing 
capacity. Platform affordances and constraints, such as limited 
expressivity in communication (e.g., being encouraged to use a “like” 
reaction button in lieu of natural language elaboration on a post), the 
ability to rapidly scroll on digital screens, and the glut of emotionally 
charged material can also encourage peripheral rather than centra l 
processing of information [6–8]. 
Digital infrastructures also shape digital artifacts. The rhetorical 
features of these artifacts further encourage superficial engagement 
with online information. In our paper, we focus on one particular 
online artifact form—the image meme—that has played a crucial, yet 
understudied role, in destabilizing former epistemic foundations and 
traditional sources for public sensemaking. As we demonstrate below, 
the image meme has evolved into a ubiquitous unit of public discours e. 
Moreover, image memes function consistently as quasi-arguments in 
digital public spheres. 
The word “meme” has gathered a great deal of semantic elasticity at 
this point [9,10], stretching from a general “unit of culture” to the 
specific genre and form of the image-macro [11,12]. We adopt a narrow 
definition of the image meme that allows us to capture and trace its 
role in public sensemaking. While the image macro refers to “captioned 
images that typically consist of a picture and a witty message or a 
catchphrase” [13], we use the term “image meme,” instead, because 
many specimens that draw from the image macro genre are devoid of 
text. In those cases, a juxtaposition of images within the meme 
compensates for its lack of textual elements. In image memes, 
configuration of the images themselves create meaning by making or 
implying arguments. We define the image meme by two features —form 
and function. The form of the image meme is established by the 
rectangular box frame which circumscribes one or more rhetorical 
elements, demarcating the meme as a discrete communication unit on 
platforms like Facebook, Instagram, and Twitter. While image memes 
perform a variety of rhetorical functions [14,15], we restrict our

## Page 5

Digital Rhetorical Ecosystem Analysis, 2021 
 
3 
attention to image memes that play a particular rhetorical role—i.e., 
they participate in public argumentation by advancing claims [9]. In 
sum, the rhetorical artifact at the center of our paper is the ubiquitous 
rectangular box that is deployed to make a claim about a public issue.  
The image meme has proved remarkably effective as a currency for 
public discourse, especially on Facebook and Instagram [16]. In 
particular, image memes have become integral to the destabilizing 
projects of the digital radical. They have been deployed strenuously in 
efforts to challenge and disrupt official and institutional discourses. 
The rhetorical dominance of image memes can be attributed to their 
ability to function argumentatively and, thereby, persuasively in the 
public sphere, constituting radical communities of discourse that are 
engaged in decoding, sharing, and amplifying their contents [17].  
What does a rhetorical approach to the study of memes 
entail? 
Aristotle defined rhetoric as “the ability to see what is possibly 
persuasive in every given case” [18]. Rhetorical study emphasizes the 
how of persuasion. Therefore, a rhetorical approach to addressing our 
epistemic crisis moves us past solutions like banning digital sources of 
information or playing fact-check whack-a-mole with spurious message 
content, to focus on the persuasiveness of the message medium. While 
rhetorical critics are invested in analyzing message content, they are 
also invested in analyzing message form. The digital artifact at the 
center of our paper, the image meme, is a powerful example of the 
persuasiveness of rhetorical form. Repetition of form contributes to 
the crystallization of a rhetorical genre [19]. The widespread and 
increasing deployment of the image meme in digital public spaces has 
elevated the image meme into a rhetorical genre, one tha t is capable of 
charging a large scope of content with persuasive appeal.  
Image memes have immense rhetorical power to shape online and 
offline sensemaking and action. During the 2016 United States election, 
Internet memes “enabled users to rapidly take a stand on and react to 
developing political events in real time; they provided alternative 
parallel discourses to mainstream media viewpoints; and they enabled 
mobilizing voters outside of official political discourses” [20].  The 
rhetorical power of multimedia memes has strengthened since 2016 
[21,22]. Therefore, we argue for treating these artifacts as serious 
agents that shape public narrative and action. 
A rhetorical approach to analyzing image memes can advance our 
understanding of their persuasive influence beyond the current

## Page 6

Digital Rhetorical Ecosystem Analysis, 2021 
 
4 
practices of syntactic tagging of memes, for example by text recognition 
[23]. A rhetorical approach fills in the gaps endemic to tagging practices 
by enriching analysis of image memes with rich semantic information 
embedded in the parsimonious combination of the meme components. 
Symbolic cues in the memes not only advance logical claims but also 
encode ambiguous yet intense emotional charge that could spur public 
action. Interpreting cues within the meme against contextual knowledge  
surrounding the meme is vital for the process of rhetorical analysis, 
and, as we will discuss later, computational analysis of digital discourse 
using a rhetorical approach. 
A rhetorical approach encourages attention to the ways in which memes 
galvanize specific audiences to change their thoughts and actions. 
Image memes have constitutive potential; that is, they simultaneously 
call into being (constitute) audience groups while influencing audience 
thinking and possibly action—a process which rhetoricians call 
interpellation [24]. This constitutive potential is contained in the 
argument potential of the meme—its ability to advance claims, 
provide/imply evidence, and rely heavily on a discursive community to 
supply the necessary warrants (assumptions) to complete the argument 
[17]. The capacity of image memes to compel audience participation in 
semantic decoding contributes to the persuasive appeal of memes 
because the act of figuring out the meme’s claim constructs the 
experience of truth-seeking, and consequently a sense of shared in-
group identity, for the audience. Having successfully completed the 
decoding effort, audiences are interpellated as truth-seekers which 
enhances their investment in the meme’s claim. 
Another rhetorical feature of image memes that makes them conducive 
to interpellating audiences as truth seekers is that image memes are 
often free-floating. They seem to appear out of nowhere and do not 
typically disclose their sources unlike other digital content. As such, 
image memes represent an epistemic break. They gain credibility not 
because they arise from authoritative sources but precisely because they 
claim no source. The rejection of source credibility makes image memes 
a very powerful parallel discourse to more formal media channels and,  
in many cases, a direct challenge to information, claims, or narratives 
that emerge from publicly-vetted sources. When interpellated audiences 
decode and share image memes and engage in discourse about memes 
on forum threads, they build credibility for the meme in the absence of 
authoritative source credibility. 
Therefore, tracking image memes (the claims they advance and the 
audiences they interpellate) in digital public spheres has become 
essential. Robust and far-reaching alternative and counter narratives

## Page 7

Digital Rhetorical Ecosystem Analysis, 2021 
 
5 
circulate through social media platforms displacing mainstream 
narratives and flow under the radar of traditional mechanisms for 
capturing public belief and opinion. These online parallel currents of 
public discourse grew on social media platforms in relative obscurity 
between 2016 and 2020. The 2020 pandemic year, however, surfaced 
the proliferation of underground narratives when they started to 
manifest as widespread overt resistance to official COVID -19 
narratives and policies, among large noticeable sections of the public. 
Towards the end of 2020, the galvanization of digital memetic energy 
around the visible public agitation against the 2020 US election results, 
culminating in the events at the United States Capitol on January 6 
2021, initially caught public officials and mainstream media off guard 
but subsequently drew further attention to the robust discursive spaces 
in which competing narratives have been spawning and flourishing. 
Competing narratives have had and continue to have global impacts, as 
digital public spheres transcend the national boundaries of mainstream 
and official media channels. As researchers and organizations, 
interested in improving the immunity of digital public spheres to 
misinformation, invest in understanding the emergence of competing 
narratives, we urge attention not simply to the content of the narratives 
but, equally, to understanding of how those narratives are constructed 
through the circulation of digital artifacts, such as image memes. The 
philosopher Bruno Latour has noted that “whether or not a statement 
is believed depends far less on its veracity than on the conditions of its 
‘construction’ — that is, who is making it, to whom it’s being addressed 
and from which institutions it emerges and is made visible.”[25] T o 
Latour’s list, we add the importance of attending to the rhetorical form 
in which the statement is packaged, i.e. the form of the image meme . 
Understanding the rhetorical form and function of image memes is 
crucial for any effort to observe, model, and respond to memetically-
driven narratives. 
Rhetorical Anatomy of an Image-Meme 
Although digital image memes can be used to circulate official 
narratives online, they have more successfully been deployed 
disruptively, across the political spectrum. Their truncated or 
compressed form is well-suited to inject targeted challenges to 
mainstream claims. The parsimonious form of the image meme provides 
a great deal of capacity for semantic encoding to advance persuasive 
claims while diminishing burdens of proof and elaboration that other 
rhetorical artifacts, like news articles, require. Various image meme 
formats such as text-only, image-only, screenshot, and image-text 
juxtaposition can all create polysemic affordances [26]; that is, the

## Page 8

Digital Rhetorical Ecosystem Analysis, 2021 
 
6 
possibility of extracting multiple and multi-layered interpretations 
within a range of meanings. The strategic ambiguity inherent in 
memetic artifacts allows for rich semantic encoding. At the same time, 
the structural features of the memetic form (i.e., the containment of its 
content in a box, and the text/image syntax) strategically constrain 
meaning-making by setting up the key elements of an argument and 
cutting off counter-arguments. Below, in Figure 1 we illustrate the 
construction of an argument contained in one sample image-text meme. 
Figure 1 above constructs an argument with the simple juxtaposition of 
two lines of text above and below a stock photo. The choice of the 
photo combined with the double textual framing relies on the 
contextual knowledge of discursive communities to decode the 
argument. While the explicit memetic content is sparse, its signifying 
layers are rich, thus allowing the meme to argue a clear and persuasive 
claim. 
The primary claim distilled from this image-text meme is that the 
official narratives about the origins of the SARS-CoV-2 virus, and the 
official masking policies to combat the virus, are not to be trusted. The 
rhetorical power of the meme draws from its strategy of juxtaposing 
two official narratives that appear to be mutually exclusive—that is, if 
the virus is virulent enough to escape the strict safety protocols of a 
world-class laboratory, then it can definitely penetrate the ordinary 
masks that the public has been asked to wear to stem the spread of the 
virus. The meme simultaneously alleges dissonance in official claims 
and expresses a snide disdain for those who accept the official 
narratives and are oblivious to the dissonance. The meme carries 
Figure 1. Rhetorical analysis Example 1. A “Condescending Willy Wonka” image meme, 
with top text reading “Tell me more about how a virus can escape from a level 4 bio-lab”,
and bottom text reading “But can’t get past a mask with little duckies on it...”

## Page 9

Digital Rhetorical Ecosystem Analysis, 2021 
 
7 
content designed to appeal to audiences’ logical reasoning as well as to 
activate an emotional charge in the audience. The logic and emotion 
evoked by the meme are abetted by the meme’s use of the 
“Condescending Wonka” image deployed memetically since 2011 to 
convey patronizing sarcasm [27]. 
The two lines of text interspersed with the image interpellate an 
audience into the persona of Condescending Wonka, questioning with 
disdain, not only the official COVID-19 narratives but also the 
intelligence of those who have not yet figured out the contradiction. 
The meme positions the audience that agrees with its claim on one side 
against lying officials and people that trust official narratives on the 
other. The rhetorical deftness of this particular image text meme lies 
in its ability to swoop an audience, in the course of a single engagement 
with the meme, into both the line of reasoning set up by the meme and 
into an interpellated audience identity. That is, even as a viewer might 
be encountering the meme’s reasoning for the first time, having 
followed the reasoning and accepted it, the viewer comes to embody 
the persona of the one questioning the official narrative and 
condemning the naiveté of those who don’t. The semantic decoding 
effort demanded by the meme works to enhance the credibility of the 
meme’s claim by interpellating audiences as truth-discoverers. By 
advancing claims, memes not only shape public beliefs but also 
constitute powerful rhetorical audiences, knitting together discursive 
communities that share memes and bond over decoding and accepting 
memetic claims. 
Furthermore, the boundedness of the image meme above (i.e. its 
containment with the rectangular box frame) and the parsimony of the 
rhetorical elements within the meme inhibit central processing and 
encourage peripheral processing of the meme’s claim. The particular 
rhetorical form of the meme thwarts further questioning into possible 
reasons why the two supposedly contradictory claims may, in fact, not 
contradict each other. The success of the meme’s argument relies on 
its ability to evoke the assumption that the initial event of the virus’s 
escape signals its inability to be contained in any way. The possibility 
that initial spread was virulent because the virus encountered an 
unsuspecting maskless population is elided by the memetic structure. 
Likewise the claim that masks only mitigate but do not necessarily 
prevent infection, entirely, is also obscured by the certainty evoked in 
the meme’s juxtaposition of claims. Memes often simultaneously 
function as assertive yet weak arguments. Their weakness lies in the 
fact that their parsimonious form limits elaboration. However, this 
form feature is also responsible for obscuring the weakness of memes. 
The limited information, visually bounded by the meme’s rectangular

## Page 10

Digital Rhetorical Ecosystem Analysis, 2021 
 
8 
box, seals a particular conclusion while deflecting attention from 
warrants (assumptions) that could challenge the meme’s claims.  
A second image meme example below in Figure 2 illustrates the 
profound intertextuality that undergirds memetic sensemaking. Image 
memes are richly polysemic, despite their minimalistic rhetorical 
elements, because elements within the meme often produce meaning 
through intertextuality, that is, by their reference to and association 
with cultural symbols that gain significance, themselves, through 
memetic spread.  
In the second example (Figure 2), we see intertextuality of memetic 
discourse at work because of the ways in which the image meme deploys 
another previously established meme, namely the Karen persona. This 
image meme attacks the claims that Antifa are responsible for some or 
most instances of violent unrest in the United States, for example 
during 2020. The primary claim available for decoding by an 
interpellated audience is that right wing hysteria both deludes and fuels 
itself by using Antifa as a bogeyman. The claim and inherent 
interpellation of a left-wing audience are achieved through multiple 
semiotic layers encoded in the meme’s rhetorical choices.  
The image features a male hand writing in a notebook, in the 
foreground, while the blurred figure of a reclining woman occupies the 
background of the meme box. The image by itself is polysemic and does 
not induce a clear interpretation. However, the addition of the text 
above: “So is ‘Antifa’ in the room right now with us, Karen?” performs 
complex rhetorical work to constrain the interpretation of the image 
 
Figure 2. Rhetorical analysis Example 2. The image foreground has hands that are using 
a pencil to write in a small book. The image background is blurred and appears to show 
a person on the left. The top text of the image reads: “So is ‘Antifa’ in the room with us 
right now, Karen?”.

## Page 11

Digital Rhetorical Ecosystem Analysis, 2021 
 
9 
and make multiple claims about the political right-wing. For example, 
the use of the name Karen is an indexical cue meaningful to anyone 
aware of the cultural meme of referring to white women who 
demonstrate hysterical fears about people of color and liberal causes as 
“Karens.” The choice of name combined with the choice of a white 
woman in the image is salient. The visual cue and the textual cue 
operate in tandem to activate a semiotic network of meanings that 
guides the interpretation of the rest of the image. The text caption leads 
the viewer to interpret the image as a therapy scene. The enclosure of 
Antifa in quotation marks and the use of a familiar phrase to question 
someone who might suffer from hallucinations constructs the claim 
that the concern over Antifa is merely a figment of the hysterical 
imagination of the political right. The gender-coding in the image is 
another semiotic layer. While plenty of male politicians on the right 
have publicly announced their anxieties over Antifa, the choice to 
feminize that fear is a rhetorical move meant to draw on associations 
of femininity with hysteria and lack of rationality or sanity. The 
question: “Is ‘Antifa’ in the room with us right now?” might be asked 
of adults suffering from hallucinations, but it is also reminiscent of a 
question that might be asked of a child whose imagination is running 
rampant. Thus the text infantilizes the concern as well as feminizes and 
pathologizes it. Since Karens are typically framed as immature women, 
the infantilization is consistent with the contextual cues that would be 
provided by the left-leaning discursive community interpellated by this 
meme. In this case, the audience is not interpellated as truth -seekers 
but rather into an intellectual and moral superiority that is antithetical 
to the hysteria of a Karen. As such, memes are incredibly rich sources 
of meaning that can shape public opinion and create and strengthen 
discursive communities in which claims and narratives become 
sedimented over time. 
Whether the memetic content is sombre or lighthearted, explicit or 
implicit, memes are overwhelmingly deployed in the digital public 
sphere to assert and persuade through claim-making. The foundational 
intertextuality of memetic discourse demands that any study of memes 
as public sensemaking needs to go beyond rhetorical analysis of 
individual memes and consider how memes interact with and draw from 
each other to constitute, sustain, or destroy claims, and thereby 
narrative patterns, in response to unfolding events over time. 
Therefore, applying an ecosystem framework becomes essential to 
understanding how memes produce public sensemaking. Our next  
section details the rich potential in leveraging the ecosystem as a 
metaphor for studying the production and circulation of memes.

## Page 12

Digital Rhetorical Ecosystem Analysis, 2021 
 
10 
Ultimately, we coalesce a rhetorical analysis of memes and a digital 
ecosystem framework into our proposed Supervisory Control and Data 
Acquisition (SCADA) model for meme analysis. The SCADA focuses 
on identifying key claim(s) embedded in image memes and the 
connections between memetic claims in order to trace the emergence, 
proliferation, and demise of public narratives on issues of public 
concern. The proposed SCADA system would provide a rich, real-time 
monitoring and analysis of narrative formation and propagation that 
circumvents limitations imposed by syntax and natural language -
focused approaches. Further, open access to such a system would 
provide a counterbalance to both coordinated narrative influence 
campaigns and organic perturbations in memetic ecosystems, and 
provide 
more 
reliable 
analytic 
foundations 
for 
considering 
interventions to quell their effects. 
II. Ecological Extensions of Rhetorical 
Analysis: Trends and Theory 
Ecological metaphors for socio-technical systems have been applied 
productively to describe the physical and information aspects of the 
global operating environment, and recently notions of narrative , digital, 
and rhetorical ecologies are also gaining in popularity (Figure 3) [1,28 –
30]. Ecological or ecosystem metaphors for digital systems are applied 
as an integrative framework in different systems such as large-scale data 
analytics [31], “app ecosystems” [32] corporate strategy [33], and 
interactive role-playing games [34]. Across these diverse fields, 
ecosystem metaphors can encourage holistic analysis and connect 
abstract concepts to tangible systems and accessible experiences.  
The idea and terminology of a “digital ecosystem” has been used since 
at least the 1980s, and has seen exponentially increasing use since the 
early 2000s (Figure 3B). A search using Google Books Ngram viewer 
revealed the recent growth of research interest in applying the 
ecosystem metaphor to online discourse (Figure 3A). While there is new 
interest in "digital ecosystems" as a term, as well as "narrative 
ecosystem" perspectives, the term "rhetorical ecosystem" is entirely 
absent from the literature corpus (Figure 3B). 
Multiple previous works have applied the ecosystem metaphor to 
address questions related to digital discourse and memes. For example, 
empirical work on various popular websites has deployed the ecosystem 
metaphor to study the dynamics of the “meme ecosystem”. These 
studies have analyzed copyable plain text memes, sometimes referred

## Page 13

Digital Rhetorical Ecosystem Analysis, 2021 
 
11 
to as “copypasta”, [35] as well as shareable image memes [36]. In these 
studies, the text and/or image data are downloaded en masse from 
publicly-accessible platforms. The ecosystem metaphor stands in the 
background referring more to the broad scope of data collection, rather 
than in the foreground as an appeal to see the data emerging from an 
ecosystem (e.g., analyzing the data in terms of interaction types among 
agents in an ecosystem). 
This suggests that the ecological metaphor applied to rhetoric 
(especially online rhetoric) has been conceptual and qualitative, 
drawing on conceptual similarities with ecology but not formulating 
ecosystem models or deploying recent developments in ecological 
toolkits. Thus we worked from the assumption that pragmatic 
implications for high-throughput rhetorical analysis of online discourse 
might be found in ecology, if the connections could be drawn out more 
clearly. 
Figure 3. Trends in the usage of keywords in the Google Books Ngram search engine. 
Search terms used were (digital/rhetorical/narrative) + (ecology/ecosystem).  
A) Google Books Ngram search for “rhetorical ecology” (green), “digital ecology” (blue), 
and “narrative ecology” (red), from 1960-2019.  
B) Google Books Ngram search for “rhetorical ecosystem” (green), “digital ecosystem” 
(blue), and “narrative ecosystem” (red), from 1960-2019.

## Page 14

Digital Rhetorical Ecosystem Analysis, 2021 
 
12 
III. The Digital Rhetorical Ecosystem Three-
Tier (DRE3) Model: Mappings, Applications, 
and Implications 
For research into socio-technical systems and digital discourse, the field 
of ecology provides much more than qualitative metaphors. Others have 
offered a variety of fundamental points of contact between ecology and 
rhetoric, noting that both fields explore how systems exhibit multiscale 
patterns of organization arising from interactions among many subunits 
[37]. Both rhetoric and ecology study how information is communicated 
through time, and how agents interact with or modify their context. In 
the case of rhetoric, this is through the production, perception, and 
interactions with artifacts and social entities, and in the case of ecology , 
this is the phenomena of niche modifications or stigmergy [38]). Here 
we extend the interface between rhetoric and ecology to argue that the 
mapping between these two domains can find productive application in 
the monitoring and design of digital ecosystems. The specific 
implications of ecosystem metaphors for digital discourse are explored 
in the following section. 
“Rhetorical ecology” is an established term (Figure 3A) that refers to the 
context-dependent rhetorical implications of texts as they are deployed 
in changing spatio-temporal contexts. The concept of “rhetorical 
ecologies” has been used to describe the level of modeling and 
abstraction that generalizes above any given rhetorical situation or 
element [39]. The ecological framework surfaces relationships between 
texts. For example, in ecology, the concept of a predator-prey 
relationship refers broadly to a type of behavioral interaction between 
two species, where one species consumes the other. Understanding that 
two species are in a predator-prey relationship helps make sense of an 
otherwise-disconnected set of questions and observations in the world, 
for example the daily activities of both species and their bodily 
morphology. In the case of rhetoric, we can also imagine predator-prey 
type relationships—for example two digital communities connected 
because one systematically follows and attacks the other, through 
memes. Additionally, online ecosystems may present totally new kinds 
of relationships among interacting agents; so any framework for 
rhetorical ecosystems should be able to infer novel types of relationships 
without being limited to the archetypes present in wild ecosystems (e.g., 
predator-prey as above, symbiosis, mutualism, parasitism). We 
hypothesize that with appropriate ecological-rhetorical mappings in 
hand, new sets of frameworks and tools developed to study ecosystems 
could become rapidly useful for analysis of online discourse.

## Page 15

Digital Rhetorical Ecosystem Analysis, 2021 
 
13 
Here we introduce the Digital Rhetorical Ecosystem three-tier (DRE3) 
model (Figure 4) which expands previous work on the ecosystem 
metaphor for online systems and builds towards system design 
implications for analysis of memetic discourse. 
The DRE3 model was inspired by the three-tier model of ecosystem 
integrity (3TEI) developed by Equihua et al. 2020 [40] (Figure 4A). In 
their 3TEI, the topmost tier is the Instrumental tier, reflecting 
measurements from the world, for example by sensors or cameras. The 
middle tier of the 3TEI is the Contextual level, reflecting the network of 
interacting agents in the niche that give rise to the observed information 
at the Instrumental tier. The bottom tier in the 3TEI are the Hidden 
variables of the ecosystem, such as risk of fire or capacity for agriculture. 
These variables are not directly observable through the use of any kind of 
physical instrument—hence statistical tools must be used to infer these 
states from the Contextual states that are in turn estimated from the 
empirical data at the Instrumental tier. 
For the DRE3 model applied to digital ecosystems (Figure 4), we translate 
each of the tiers from the 3TEI into corresponding domains related to 
online discourse. The Instrumental tier of the DRE3 reflects the empirical 
observations of digital activity, for example rhetorical artifacts such as 
image memes, as well as metadata and other platform information (e.g., 
traffic logs, user ratings or responses to content). The middle tier of the 
DRE3 is the Rhetorical tier. This Rhetorical tier reflects the networks of 
entities, claims, and warrants evoked by artifacts at the Instrumental tier. 
Figure 4. Ecosystem integrity model & the Rhetorical Ecosystem three-tier (DRE3) model. 
A) Figure 1 reproduced from Equihua et al. 2020 [40]. B) Digital Rhetorical Ecosystem 
Three-tier model.

## Page 16

Digital Rhetorical Ecosystem Analysis, 2021 
 
14 
The bottom tier in the DRE3 reflects the multiple possible Hidden layers 
which might be significant targets of analysis, for example the risk of 
extremism, production of subcultures, degree of innovation, quality of 
public information, trust in government, and process of governance. 
Importantly, the information in the Instrumental tier is mediated and 
augmented by a Rhetorical tier in the process of Hidden State inference. 
The direct mapping from rhetorical artifacts to hidden state inferences 
can be challenging and noisy (e.g., in the case of hashtags or syntax-driven 
analyses used to identify conspiracy theories [41]), or essentially 
impossible (in the case of image and multimedia artifacts). A better 
approach to high-throughput analysis of multi-media digital discourse is 
needed. We suggest that the introduction of a rhetorical layer (consisting 
of entities, claims, and warrants) in between the instrumental and hidden 
layers is a useful direction to pursue. 
Ecology: Key Concepts and Mappings 
This section applies the DRE3 model in the context of the modern global 
information environment. Like insights gleaned from regional ecosystems 
[42], analyses of rhetorical ecosystems ideally should be use-oriented, in 
close-to-real-time, and able to be represented differently for different 
stakeholders. Contemporary and future analysis of online discourse will 
involve the use of heterogeneous data to detect, monitor, and perturb 
discourse. This requires a significant amount of actionable and estimative 
intelligence regarding the real-time state of online discourse, especially if 
the goal is to ameliorate the aforementioned epistemic crisis and increase 
the capacity to understand and respond to the use of image memes in 
online discourse. 
In this work we do not present any formalisms or explore all possible 
ecosystem-rhetoric connections, but rather focus on deriving implications 
for rhetorical analysis and online system design by focusing on three key 
areas of ecological theory and application: 
• Multiscale perspective on ecosystems 
• Ecosystem antifragility 
• Ecosystem services 
For each of these three ecological topics, we 1) define the term, 2) clarify 
the mapping from ecology to rhetoric, 3) consider which concepts might 
transfer from ecology to rhetoric, and 4) provide a preliminary 
investigation of the implication of these mappings in terms of systems 
design.

## Page 17

Digital Rhetorical Ecosystem Analysis, 2021 
 
15 
Multiscale perspective on Ecosystems 
What is the Multiscale perspective on ecosystems? 
• Modern ecological frameworks are built around the 
idea that biological systems present as nested scales 
of organization [43]. At each scale of organization 
such as cell, organism, and population, the system 
consists of interacting agents of various types 
[44,45]. System subunits can interact in non-linear 
ways, and the integrated function of the ecosystem 
as a whole can be considered as cognitive in its own 
right in that the system can learn, integrate 
information, display persistent memory, and act in 
an anticipatory fashion [46]. 
What is the mapping from the multiscale perspective on 
ecosystems to online digital discourse? 
• Today’s digital landscapes consist of human and 
non-human agents, interacting with each other and 
with textual artifacts, as if they were on rhetorical 
landscapes. Ecosystems and landscapes are rich and 
generative metaphors that help capture the many 
ways in which agents of various types and in various 
roles 
interact 
massively 
in 
parallel. 
These 
distributed rhetorical interactions contribute to 
information integration, collective decision making, 
memory, education, and anticipation across the 
digital public sphere. Rhetorical ecosystems exhibit 
structure and regularities across multiple scales of 
analysis, for example the individual, relationship, 
group, and community. Thus digital rhetorical 
ecologies can be considered as an integrated 
multiscale cognitive system. 
• The case of an image meme posted on a social media 
platform can be seen as a niche modifying action of 
mobile agents, with the intention of signaling to 
similar or dissimilar agents, resulting in functional 
consequences for the further evolution of the 
biosemiotics 
of 
the 
niche. 
These 
stigmergic 
processes in nature, such as an ant depositing

## Page 18

Digital Rhetorical Ecosystem Analysis, 2021 
 
16 
pheromone, or large mammal making territorial 
markings [47,48], are essential for ecosystem 
function. Digital platforms present affordances for 
niche modifications, whether extremely limited 
(e.g., only a “like” button”), or more extensive (e.g., 
a Wiki model where content can be edited, or even 
a platform where the code and affordances can be 
modified by users). The availability and incentives 
for using different kind of digital affordances will 
be user-, platform-, and context-specific. This 
corresponds 
to 
ecosystem 
contexts 
where 
contextual niche modification processes play out 
over rapid behavioral timescales versus slower 
evolutionary timescales. 
Which key ideas and tools from the multiscale perspective 
of biological ecosystems transfer to digital discourse 
spaces? 
• Ecosystems around the world vary in fundamental 
ways but still can be modeled with common 
frameworks. Similarly, in the case of online 
discourse, we are interested in the similarities and 
differences 
across 
languages, 
platforms, 
and 
settings. The multiscale perspective in ecology 
highlights how interacting agents and situations can 
generate emergent patterns that are stable (or 
metastable/oscillatory) within acceptable attractor 
states, rather than causing cascading failures 
[49,50]. In ecology, even antagonistic interactions 
such as predator-prey may be stabilizing at the 
macro scale. In the case of online rhetoric, we might 
map individual-level interactions to behavioral 
ecology, 
and 
group-level 
dynamics 
to 
macroecological outcomes. For example, a pairwise 
relationship might be unstable or antagonistic 
among two users of an online platform (behavioral 
ecological scale) yet be a part of a stable broader 
online community of users (macroecological scale).  
• The idea of niche modification from ecology 
translates to the kinds of changes that agents make 
to their information niche. In the case of online 
communication, this is known as digital stigmergy

## Page 19

Digital Rhetorical Ecosystem Analysis, 2021 
 
17 
[51,52]. Just as the behavior of individual animals is 
nested within (and in feedback with) surrounding 
ecosystem dynamics, rhetorical agents are actively 
exploring and modifying their informational niche.  
• Various ecological toolkits exist to infer agent 
states and actions across spatial-temporal scales and 
use these inferences to understand how agent 
behavior is in feedback with broader trends. These 
toolkits include software packages and approaches 
related to movement tracking, multi-scale network 
analysis 
[53], 
system 
simulation 
[54], 
and 
characterization of the relationship between animal 
behavior and the animal’s niche [55–57]. In the case 
of online discourse, agents are moving across 
informational landscapes, updating their models of 
the world, interacting with other agents, and 
increasing 
or 
decreasing 
their 
likelihood 
of 
engaging in different kinds of action. In both 
ecological and rhetorical settings, one may be 
interested in modeling how interaction among 
agents influence individual and collective behavior, 
as a function of context in the niche. 
Figure 5. Representation of the multiscale perspective on Ecosystems. At left, 
ecological modeling of the world can proceed via decomposition into 
disparate ecosystems. At right, online rhetoric occurs within the global 
information environments, via increasingly-fragmented platforms, channels, 
and chats. The common mapping, in the middle, is the notion of overlapping 
and nested systems.

## Page 20

Digital Rhetorical Ecosystem Analysis, 2021 
 
18 
Ecosystem Antifragility 
What is ecosystem antifragility? 
• Ecosystem antifragility refers to the vibrancy, stability, and 
dynamic variability of a system. Recently, Equihua et al [40] 
have used various approaches from Complexity science to 
describe ecosystem antifragility as “beyond resilience and 
integrity”. Their working definition is that an “ecosystem is 
antifragile if it benefits from environmental variability” [40]. 
Antifragility is similar to the notion of resilience, which 
captures how a system resists change or returns to functional 
capacity after a perturbation [58]. However, antifragile 
systems are those that actively grow or increase in capacity 
after stressors, as opposed to merely returning to previous 
operating modes. 
What is the mapping from ecosystem antifragility to online digital 
discourse? 
• Health. The stability and flourishing of the rhetorical 
commons is a primary goal for participatory communities 
and societies. This is akin to the concept of ecosystem 
health: even where different regions or seasons may have 
distinctly different healthy modes, maintenance of 
ecosystem vitality may be an overarching regional goal. 
While humans have long relied on qualitative or felt 
measures of ecological health, quantitative data collection 
allows for entirely new measurable notions of health only 
enabled by instrumentation and modeling [59–61]. We 
highlight the need to develop statistical indicators for the 
health and vitality of digital ecosystems so that policy for 
and management of digital commons spaces can be driven 
by shared empirical understanding rather than the 
potentially discordant experience of individuals.  
• Resilience. The resilience of a rhetorical ecology might be 
defined in terms of the system’s maintain function during a 
crisis, informational update, or structural change. The 
resilience metaphor draws attention not just to the regular 
or functional operating modes of rhetorical ecosystems, but 
also to the emergency and recovery modes available to these 
systems. Ecosystem resilience is critical when humans have

## Page 21

Digital Rhetorical Ecosystem Analysis, 2021 
 
19 
a vital dependence on continued ecosystem function, as in 
the case for agriculture [62]. Increasingly, online 
communications are a lifeline, and thus also need to be 
managed carefully with uninterrupted service and content 
integrity in mind. Disruption of internet services can occur 
through physical damage to infrastructure, as well as 
software intrusions (e.g., ransomware, denial of service 
attacks). Even when hardware and software are running 
according to performance standards, breakdowns of 
sensemaking (e.g., due to spam, targeted disinformation) can 
lead to perturbations on digital platforms and breakdowns 
in their typical functioning. 
Which key ideas and tools from antifragility perspectives of 
biological ecosystems transfer to digital discourse spaces? 
• Ecological antifragility has several kinds of ideas and tools to 
offer to the domain of rhetoric. Equihua et al. [40] characterize 
antifragile systems as those that benefit from variability, which 
provides a valuable parallel for measuring the health of the 
rhetorical commons by its type and extent of diversity (here of 
rhetorical claims and perspectives, rather than, for example, a 
species number). That the variability of rhetorical claims can 
be a source of collective vitality provides a helpful starting 
point for viewing online discourse and dissuades approaches 
that promote total consensus as a goal, or reflexive suppression 
of alternative viewpoints. 
• Some approaches towards ecosystem antifragility feature 
participatory roles for ecosystem inhabitants, for example local 
cleanup events, long-running citizen science projects related to 
birdwatching [63] and regional ecosystem biodiversity events 
like a BioBlitz (“an event that focuses on finding and 
identifying as many species as possible in a specific area over a 
short period of time” [64]). In the context of digital 
ecosystems, these kinds of local programs for ecosystem 
improvement can scale to include large numbers of 
participants, for a Wiki editathon, for example [65,66]. 
Coordinated efforts to “fix trails” in digital ecosystems could 
contribute to antifragility by providing a scalable approach for 
reducing risks from cascading or complex failure modes related 
to out-of-date information, fragile network structures, or 
incapacity to deal with anomalous system usage.

## Page 22

Digital Rhetorical Ecosystem Analysis, 2021 
 
20 
• Quantitative tools also exist to help stakeholders measure and 
model ecosystem antifragility from a Complexity perspective 
[67]. Dynamic models allow for simulation and analysis of 
various kinds of systems and their stability in different 
situations [68,69]. In the context of ecosystem health, these 
kinds of analysis ask how it might be possible to build stable 
networks rather than network structures. An exclusive focus 
on network structures might lead to fragility of network 
function when edges are lost or nodes change. Modeling 
ecosystem health as a phenomenon arising from interacting 
networks, offers new and potentially more-effective ways of 
thinking about how multiple ecosystem stressors interact [70]. 
Network models also can be expanded to include “games on 
graphs” models, which use the tools of game theory to explore 
how strategies interact on landscapes and how information 
propagates through groups [71,72]. In the context of digital 
ecosystems these kinds of models could provide descriptive, 
prescriptive, and proscriptive information on the general 
function and well-being of digital platforms. 
Figure 6. Representation of the concept of Ecosystem antifragility. At left, 
a forest experiences a perturbation such as a fire event. This event may 
either lead to devastation of the forest (top), or result in a forest that 
either burns completely and/or grows back stronger (bottom). At right, 
using a city as an analogy for the online rhetorical commons, a 
perturbation event can result in a destroyed commons (top), or a 
strengthened and vibrant community (bottom). The common mapping, 
in the middle, connecting biological ecosystem antifragility to digital 
ecosystems is that complex systems can undergo various recovery or 
response dynamics in response to perturbations, broadly classified as 
fragile (failure-prone, top) or antifragile (resilient and regenerative, 
bottom). For digital discourse platforms, fragility would refer to the 
inability to adapt or recover function following technological or rhetorical 
perturbation.

## Page 23

Digital Rhetorical Ecosystem Analysis, 2021 
 
21 
Ecosystem services 
What are Ecosystem services? 
• Ecosystem services are the functions that ecosystems 
provide which are useful for humans directly or 
incidentally, for example the provision of food, erosion 
control, composting of decaying matter, recreational 
spaces, or generation of natural resources, [73]. As is the 
case with ecosystem antifragility and health, many types 
and measures of ecosystem services exist. 
What is the mapping from ecosystem services to online digital 
discourse? 
• If we imagine rhetorical ecosystems to encompass the 
biotic and abiotic aspects of the system that contribute to 
its function and regulation, “rhetorical ecosystem 
services'' could include a broad range of outcomes, 
including education, communication, innovation, and 
development of cultural norms and practices. Just as high-
level biological ecosystem services, like the production of 
food, arise from direct interactions among many kinds of 
actors (e.g., plant, pollinator, microbes), and might be 
influenced by indirect factors as well (e.g., noise/light 
pollution, presence of predators), rhetorical ecosystem 
services emerge from the direct and indirect interactions 
of many actors and artifacts in the space. Understanding 
these influences can support modeling and management 
of the valuable outputs of a rhetorical ecosystem. 
• We can consider image memes as a special case of 
ecosystem services, in that image memes are valued or 
relevant products of an underlying ecological process. 
The image meme format reflects the intersection of 
digital 
content 
production 
affordances, 
and 
the 
rhetorical cross-pollination occurring online. The 
services that image memes provide in the rhetorical 
ecosystem can include advertising, information sharing, 
governance, entertainment, persuasion, and more– 
essentially any functional outcome of the deployment of 
image memes that can be tracked and valued.

## Page 24

Digital Rhetorical Ecosystem Analysis, 2021 
 
22 
• Other studies have investigated the dynamics by which 
images memes originate and diffuse through time among 
communities [36]. This is akin to a source-sink analysis 
common in ecology: source locations are net exporters 
(of image memes on digital platforms) while sink 
locations are net importers (on digital platforms 
reflecting image meme consumption) [74]. This source-
sink analysis of image memes can link the dynamics of 
memetic spread to their function for different audiences, 
and thus shed more light on the causes, context, and 
consequences of particular image memes for the 
rhetorical commons. 
Which key ideas and tools from ecosystem services transfer to 
digital discourse spaces? 
• Conservation & management of ecosystem services is an 
area of practice with a long history of analyzing the 
intersection of human individuals, human groups, and 
the rest of the biotic and abiotic surroundings. Some of 
the legal, mathematical, scientific, and game theoretic 
approaches to ecosystem services might transfer usefully 
to cases of online rhetoric. For example, when 
considering the design or regulation of digital platforms, 
various areas of law and policy interact, for example 
finance, business, and privacy. Framing digital platforms 
(and the functions they perform) as ecological commons 
introduces precedent for addressing legal dimensions of 
individual/public/private ownership, and processes for 
dispute resolution related to common resources [75]. 
• Ecosystem antifragility (discussed above) plays directly 
into the stability and accessibility of vital and valuable 
services [76]. Healthy rhetorical ecosystems will display 
variability in productivity through time. However, an 
ecosystem at high risk of catastrophic failure cannot be 
considered as valuable as a dependable ecosystem (e.g., 
a forest at risk of destructive fire presents higher 
uncertainty 
about 
its 
future 
productivity). 
The 
relationship between ecosystem health and productivity 
provides an economic motivation for policies that 
balance multiple contrasting requirements, by thinking 
about system function through time.

## Page 25

Digital Rhetorical Ecosystem Analysis, 2021 
 
23 
Implications 
We argue that insights from modern Ecology can help scaffold the future 
of computational systems for rhetorical analysis. Ecological perspectives 
can retain the semiotic insights from rhetoric analysis while tracing 
meanings and their interactions within a quantitative framework [37]. At 
this time, manual rhetorical analysis requires trained experts who identify 
how artifacts produce meanings for different audiences, or, in the case of 
image memes, how memes generate claims. This process of rhetorical 
analysis is analogous to a natural historian observing a species operating 
skillfully in their niche, in that a specific occurrence (observation of a 
bird, or a digital text) is modeled in terms of its relationship to the context 
and niche (whether biological or rhetorical). Computational frameworks 
for rhetoric provide a set of ideas and tools that, if properly designed, 
could help accelerate rhetorical claim analysis. This type of “next-
generation natural history” [77] for rhetorical ecosystems would integrate 
well with existing computational frameworks, apply well to the multimedia 
setting, and also work toward grounding analysis of digital discourse in 
rhetorical principles. Functionally, Ecology is the bridge that would allow 
rhetorical information to play a more central role in the computationally-
aided analysis of contextualized digital discourse. We suggest that, in 
addition to the quantitative tools it provides (such as network analysis, 
sparse sampling, agent-based modeling, meta-community dynamics), 
Ecology can supplement rhetorical analysis by foregrounding concepts 
Figure 7. Representation of the concept of Ecosystem services. At left,
physical ecosystem services such as natural resources and pollination are 
enacted by various actors within ecosystems. At right, online rhetorical 
commons can be considered to enact or emit services such as education 
and innovation. The common mapping, in the middle, is that value and 
valuable outcomes are generated through the function of the target 
system. Putting quantitative value on “intangible” outcomes can be 
challenging. Seeing online outcomes as analogous to ecosystem services 
is not a solution in and of itself, but rather a framework for approaching 
system management and design.

## Page 26

Digital Rhetorical Ecosystem Analysis, 2021 
 
24 
like ecosystem health, biodiversity, anti-fragility, and more. Below are 
some possible implications arising out of the application of the Ecological 
perspective to online rhetorical commons (by no means comprehensive). 
• Create and adapt within the niche. Online platform 
and systems designers can ask what services they are 
providing 
to 
stakeholders 
and 
the 
broader 
ecosystem (defined as the entities, audiences, and 
cyberphysical systems constituting the stakeholders 
and zone of influence of the target platform). 
Platforms provide and interact with the rhetorical 
commons, and thus services of value are being 
provided or modified by them. As digital platforms 
require inputs from the broader ecosystem in terms 
of energy, attention, and other resources, platforms 
must be anticipatory and responsive to changes in 
their operating ecosystem.  
• Trace artifacts and claims to understand function. 
The DRE3 model of digital discourse has the 
capacity 
of 
creating 
clustering, 
detecting 
thresholds, or permitting inference at the level of 
rhetorical claims, an extension of approaches built 
solely on syntactic inputs (e.g., hashtags, keywords) 
or 
lexical 
semantics 
(e.g., 
natural 
language 
processing, 
sentiment 
analysis). 
We 
need 
to 
integrate artifacts and claims (beyond, or instead of 
tracking individuals) for effective sensemaking of 
digital discourse. Thinking of claims in terms of 
functional patterns in the ecosystem, platform 
designers could analyze the relative fitness and 
spreading/mutation/co-occurrence 
dynamics 
of 
memetic claims, across communities, languages, 
media formats, and platforms. 
• Consider dynamics, not just snapshots. Some of the 
dynamical systems and network analysis tools 
developed 
for 
ecosystem 
management 
could 
generate models that may transfer directly to online 
datasets. Similar kinds of observations can be made 
in the ecological as well as digital situation (e.g., 
about the movement or communications among 
agents through a space described as a network) and 
similar kinds of questions might be asked (e.g., 
which 
initial 
conditions 
and 
patterns 
of

## Page 27

Digital Rhetorical Ecosystem Analysis, 2021 
 
25 
relationships might result in stable vs. unstable 
regimes). For example, migration can occur among 
geographical distances as well as among digital 
communities on social media. Complementary tools 
and perspectives for the analysis of migrations 
might be found across research on patterns of 
ecological and digital migrations [78,79].  
• Design for multiscale interactions. Online platform 
design could take the multiscale perspective directly 
into account, for example by making certain peer-
to-peer interaction mechanisms transparent, so that 
agents at various scales (e.g., individuals, groups, 
communities) 
are 
aware 
of 
how 
user-level 
affordances influence the niche and system as a 
whole. Top-down (e.g., platform-dictated) and 
bottom-up 
(e.g., 
user-generated) 
signaling 
mechanisms could be clearly marked (or if not 
marked, could be annotated as such by analytics 
platforms).  
• Fit generative models (of rhetoric) that can deal 
with sparse as well as complete data. The task of 
ecosystem characterization is to go from sparse and 
heterogeneous observations (for example ambient 
conditions and bird sightings through time), to a 
useful and communicable model. This task of 
ecosystem characterization, depending on the scope 
of the analysis and desired level of detail, may 
require multiple kinds of models to be specified: the 
cellular, 
organismal, 
social, 
community, 
and 
ecosystem. For online discourse, integrating the 
multiple scales at which decisions are made (human 
internet user, community, networks of networks), 
ecologically-informed models might provide a 
principled path for modeling various phenomena of 
interest. 
• Think about the ecosystem’s leverage points and 
failure modes when designing an intervention. 
Ecosystem modification efforts are famously non-
linear—careless interventions may be ineffectual or 
even have deleterious effects (as in the case of using 
broad-spectrum toxins in an attempt to eradicate 
the fire ant in the Southern USA [80]). For social

## Page 28

Digital Rhetorical Ecosystem Analysis, 2021 
 
26 
discourse, influence operations used to be evaluated 
in terms of a direct rhetoric source, such as 
centralized media. Now the operating landscape is 
much 
more 
akin 
to 
a 
complex 
ecosystem, 
contextualizing diverse social strategies as types of 
social ecosystem modification [81]. Modifications 
of the rhetorical ecosystem through various means 
(e.g., 
algorithmic 
distortion, 
misleading 
information) might have behavioral consequences 
rippling out far beyond the locus of direct action, 
akin to the introduction of a new species to an 
ecosystem. The relative efficacy and risk of 
different ecological interventions is variable across 
different 
regions. 
Proactive, 
long-term 
interventions such as restoring native habitat are 
often at odds with short-term interventions like 
intentional introduction of novel predators (as in 
the case of the cane toad in Australia [82]) or 
application of broadly-acting chemicals. Ecosystem 
interventions are irreversible, and often have non-
linear consequences for different kinds of actors 
and audiences [83,84]. 
• Consider humans in the design of platforms, as well 
as non-human and computational actors. Taking a 
human-centric perspective on ecosystem function 
would be incomplete or even fallacious, depending 
on the region and goals of ecological modeling. 
Similarly, today for online discourse, given the 
prevalence and influence of purely-computational 
agents or computationally-augmented humans, it is 
essential that platforms be designed for use by 
human and non-human agents. Already a significant 
fraction of internet activity is carried out by purely 
computational agents or networks (e.g., chatbots 
and automated accounts). While the exact amount 
of human and computer activity likely varies among 
destinations, already in 2016 it was estimated that 
certain types of internet activity might be majority 
non-human 
[85,86]. 
The 
multiscale 
cognitive 
perspective on ecosystems provides a framework 
for modeling rhetorical ecosystems consisting of 
only human actors, only computational actors, and 
any conceivable composition in-between [87].

## Page 29

Digital Rhetorical Ecosystem Analysis, 2021 
 
27 
Already falling within this scope are existing tools 
that distinguish the activity of human vs. bot actors 
online in games, forums, and other platforms 
[88,89].  
• Frame healthy and antifragile rhetorical ecosystems 
as a common pursuit. Promoting antifragility is a 
broad social goal that can apply across systems and 
scales. Ecosystem health as a concept helps 
humanize 
otherwise-unrelated 
environmental 
phenomena and might be able to play a similar role 
in making online rhetoric more tangible. Exact 
specifications of “health” for the digital commons 
may differ, just as they do for ecosystems. 
Analyzing the health of a given ecosystem might 
require 
the consideration of the abundance, 
composition, diversity, function, and tolerance of 
various kinds of life forms in the system (such as 
microbes, invertebrates, plants, etc.) [60]. And even 
in this case, individuals may still disagree on the 
health of a given ecosystem, if for example they 
diverge on the optimal usage of the region (e.g., for 
development vs. recreation vs. agriculture). When 
designing platforms for digital discourse, it would 
be valuable to consider how differences in opinion 
about “what is healthy” among users could be 
harnessed and channeled, rather than lead to system 
failure. 
• Use rhetorical measures as a diagnostic when 
modeling digital discourse by framing the resulting 
artifacts and functions in terms of ecosystem 
services. Failure of rhetorical ecosystem services 
could occur from an adversarial or unhealthy 
dynamic, such as an inability to communicate 
leading to breakdown of trust among otherwise-
cooperative individuals. To thwart, or recover from, 
such failures, it could be helpful to search for 
analogous situations in ecology. For example, 
ecosystem services could be threatened by the 
introduction of an invasive new species, a toxic 
chemical, 
habitat 
fragmentation, 
light/sound 
pollution, or loss of biodiversity [90,91]. In the case 
of rhetorical ecosystems, being able to connect 
failures of services to past ecosystem interventions

## Page 30

Digital Rhetorical Ecosystem Analysis, 2021 
 
28 
or modifications (influx of new users, introduction 
of 
toxic 
rhetoric, 
alteration 
of 
platform 
affordances, etc.) could provide a useful lens for 
protecting 
the 
valuable 
outcomes 
of 
digital 
discourse. 
IV. The Digital Rhetorical Ecosystem three-
tier model 
The Digital Rhetorical Ecosystem three-tier (DRE3) model (Figure 4) 
integrates enriched rhetorical analysis of multimedia discourse with 
ecological theory and modern computational analytics pipelines. In this 
section, we present examples of rhetorical analysis using the DRE3 
model. Specifically, we describe three analytic phases in the context of 
“boutique meme analysis” using two examples. At the end of the 
section, we provide a bridge between the traditional meth odology of 
rhetoric and the types of computational representations that are useful 
for modern digital sensemaking systems. 
There is a lack of usable platforms for computational rhetorical 
analysis, although several prescient calls have been made for such 
frameworks and tools [92–94]). Partially, this gap exists due to the 
challenge of accurately and effectively scaling expert rhetorical 
analysis. While multiple complicated sub-tasks are required for 
rhetorical analysis, digital tools exist today to carry out some similar 
functions (such as face-, voice- and text-recognizing algorithms, and 
natural language processing). We suggest that modern software 
algorithms are adequate to perform many of the sub-tasks required for 
the rhetorical analyses of image memes, and that crowd-sourced 
annotations (via participatory research, or micro-task platforms) could 
be used to support algorithms where the software alone are as yet 
insufficient. Already in the case of digital discursive ecosystems today, 
some fraction of users contribute their time and energy to improving 
discourse, for example by providing context or reporting behavioral 
violations. Approaches for online platforms that combine gamified 
participation with behind-the-scenes machine learning have been 
successful in advancing research in biochemistry and a variety of other 
fields. These crowd sourced projects can take a variety of f orms, and 
can be designed to operate directly on the engaging digital platforms 
that people already use [95]. 
Here we present what a case-by-case rhetorical analysis of image memes 
might look like, within a framework that is ultimately designed to scale

## Page 31

Digital Rhetorical Ecosystem Analysis, 2021 
 
29 
up to high-throughput ecosystemic annotation, while retaining the 
semantic richness afforded by case-by-case rhetorical analysis. These 
analyses are performed in three phases: 
Phase 1. Entity Identification. The first phase of 
analyzing the rhetorical function of a meme entails 
recognizing visual entities embedded in the meme. Entities 
can be of different types and are interchangeable across 
memes.  
Phase 2. Rhetorical Analysis. The second phase of 
decoding the function of a meme entails identifying its 
semantic and consequently persuasive potential. This 
phase begins with tracing relationships between the 
entities implied by their arrangement within the meme. 
The relationships will typically synthesize into an implied 
(or stated, if the meme includes text) claim, sometimes 
accompanied by evidence included in the meme. The claim 
often rests on implied warrants (assumptions) supplied by 
the viewer who is aware of the rhetorical context that the 
meme invokes.  
Phase 3. Hidden State Identification. The third phase 
of decoding the function of a meme is hidden state 
identification. The exact nature of the hidden state 
inference will be situational and depend on what the 
analyst is attempting to reduce their uncertainty about; for 
example, the extent to which the image meme in context 
is consistent with social values, providing specific valuable 
services, or eliciting violence. What distinguishes the 
various possible hidden state inferences from rhetorical 
inferences in Phase 2, is that hidden states are deeper than 
specific claims about entities, and reflect underlying 
attributes of the rhetorical ecosystem that gives rise to and 
are strengthened by such claims. 
Two examples below (Figure 8 and Figure 9) represent the qualitative 
application of the DRE3 model to shareable image memes. The 
rhetorical analyses below uncover preferred readings of these image 
memes [96], and are not exhaustive in terms of entity or claim 
identification. Memes, as identified earlier, are polysemic. They are able 
to generate multiple and varied interpretations. A rhetorical analysis 
cannot comprehensively decode all meaning possibilities embedded in 
an image meme. Nevertheless, by following the rhetorical use of 
symbolic content within the meme, attending to the discursive contexts 
in which a meme may be harvested (such as a Facebook post thread or

## Page 32

Digital Rhetorical Ecosystem Analysis, 2021 
 
30 
a Twitter thread), crowdsourcing the claims advanced by memes, and 
determining interpretation consensus across trained rhetorical analysts, 
we can identify likely, core, or agreed-upon, in other words the 
preferred arguments that memes advance [96]. In this case, we define 
preference by what a meme was originally designed to argue or the 
meanings that are most easily accessible (obvious) to the target 
audience. Even though the meaning of a meme can be altered by its 
discursive context (i.e., a meme can be deployed ironically to undermine 
its own message), such a subversive reading of the meme relies on 
consensus about its dominant meaning. Therefore, despite inherent 
polysemy, we believe it is both possible and useful to identify the 
dominant argument(s) that are encoded in an image meme. 
Example I 
Phase I. Entity Identification 
In the above meme, the following entity categories are 
rhetorically significant: 
Persons: Bob Ross, G.W. Bush  
Attributes: Hair, shirt, hand of Bob Ross, Face of G.W. 
Bush 
Objects: Twin Towers of the World Trade Center, 
Painting materials (palette, paintbrush, canvas, easel) 
Figure 8. Illustration of the DRE3 model as applied to an image meme
without text. A) a target image meme under analysis. B) Application of
DRE3 model, breaking down the meme in terms of the Instrumental 
tier (what was observed), the Rhetorical tier (entities, warrants, claims), 
and the Hidden State tier (implications and use-specific inferences).

## Page 33

Digital Rhetorical Ecosystem Analysis, 2021 
 
31 
Location: New York City skyline 
Action/Relationship: Individual painting on canvas 
Phase II. Rhetorical Analysis 
In the above example, decoding the meme rhetorically by 
analyzing 
relationships 
between 
entities 
requires 
distinction between host images and parasitic images. The 
incorporation of the parasitic images to replace parts of 
the host images produces a parodic relationship between 
host and parasite entities. The insertion of G.W. Bush’s 
face into the identifiable hair of the artist Bob Ross 
parodies the parasitic entity—Bush. The host image is the 
one that dominates the meme. An enculturated viewer 
recognizes the image as a still from the iconic Bob Ross 
televised painting class. Ross’s hair, shirt, hand, palette, 
brush, and canvas on the easel are easily recognizable 
attributes/objects and constitute the majority of the 
image. The viewer is clear that it is G.W. Bush’s face that 
is intruding within the Bob Ross image rather than reading 
the artist entity as the intruder. Having identified the host-
parasite relationship, the viewer must now extract the 
semantic implications of this parody. 
In deciding what the host-parasite parody means, the 
viewer recognizes that the visual juxtapositions in the 
meme are meant to paint former president G.W. Bush as 
an artist. The parasitic image that has taken over Ross’s 
typical placid landscape scene on the canvas provides a 
stark contrast to what those familiar with Ross expect him 
to paint. The peaceful landscape of a Ross painting is 
replaced by a real scene of terror (the fall of the Twin 
Towers on 9/11) that is also highly recognizable because 
it has become widely circulated memetic content. 
The face of G.W. Bush and the destruction of the World 
Trade Center towers in New York City are clearly linked 
in the rhetorical context available to the enculturated and 
interpellated viewer. The structuring of entities within the 
meme, however, superimposes an additional relationship 
that emerges out of the parodic analogy between G.W. 
Bush and Bob Ross. The parody is underscored with the 
use of an exaggerated expression on the face of G.W. 
Bush. This is the point at which the viewer arrives at the

## Page 34

Digital Rhetorical Ecosystem Analysis, 2021 
 
32 
claim embedded in the image structure of the meme. The 
claim could be articulated as follows: Like Bob Ross paints 
a landscape from imagination, G.W. Bush fabricated the 
9/11 terror attacks. In this case, the memetic argument 
advances only a claim. The meme contains no evidence. 
Instead, the meme operates intertextually. To unpack the 
meme’s claim, the viewer must be aware of multiple 
rhetorical contexts, such as the 9/11 truther movement 
that has sought to expose the terrorist attacks of 9/11 as 
a plan of the United States’ own government, and the 
imputed role of the Bush family within the construct of a 
global cabal that controls worldwide events. In this way, 
the rhetorical analysis of memes leads us to identifying 
salient hidden states (e.g., social, political, and cultural 
beliefs/practices) that both influence and are shaped by 
memetic arguments. 
Phase III. Hidden State identification: 
A rhetorical decoding of the Bob Ross-G.W. Bush meme 
both relies on and perpetuates claims about the Bush 
family, the G.W. Bush administration, the events of 9/11 
and 
other 
global 
destructive 
events. 
Memetic 
argumentation analysis is ultimately useful to the extent to 
which it permits tracing evolving public beliefs and 
practices that could have real-world implications. We 
expect that, over time, the identification of rhetorical 
claims from varied memes will reveal patterns of 
connected beliefs that correspond to higher-order hidden 
states such as confidence in the government, or beliefs 
about the causes of past events. A hidden state in our 
framework refers to an implicit and volatile state of public 
belief, sentiment, or action. A belief that the United States 
government lies to its people is an example of a hidden 
state. This higher-order claim represents a public belief 
that produces a sentiment of distrust in the government. 
Tracing hidden state dynamics is useful because they can 
activate overt action in unrelated contexts, such as vaccine 
refusal because of a previously established distrust in 
government. Such a relationship between hidden states 
and public action can potentially be identified by tracing 
co-occurrence of memetic claims within networks.

## Page 35

Digital Rhetorical Ecosystem Analysis, 2021 
 
33 
Example II 
In this example, the higher-order claim that the United 
States government cannot be trusted is advanced by 
submitting lower-order arguments. The text-image pairing 
in this meme enacts argumentation differently than in 
Example 1. While the first example illustrates argument by 
analogy, this example supports its claims with visual 
evidence and follows an “if-then” pattern. 
 
Figure 9. Example of the DRE3 model as applied to an image meme with
text. A) a target image meme under analysis. B) Application of DRE3 
model, breaking down the meme in terms of the Instrumental tier (what 
was observed), the Rhetorical tier (entities, warrants, claims), and the 
Hidden State tier (implications and use-specific inferences).

## Page 36

Digital Rhetorical Ecosystem Analysis, 2021 
 
34 
Phase I. Entity Identification 
In the above meme, the following entity categories are 
rhetorically significant: 
Persons: Actor Bill Murray 
Scenes: Tuskegee syphilis study, mushroom cloud, drug 
heist. 
Objects: Dollar bills with a stethoscope, stock of guns, 
marijuana plants, vortex of dollar bills, dollar bills with 
social security card. 
Phase II. Rhetorical Analysis 
The visual segmentation of the meme-box is crucial to how 
the argument is enacted. The visual sequencing relies on 
the viewer moving from the top to the bottom and from 
the left to the right. The top centered image features the 
actor Bill Murray. The text superimposed on this image 
invites the viewer into a dare with the person sharing the 
meme. The challenge “Call me crazy all you want” invokes 
the trope of the conspiracy theorist, a label typically 
branded on those who accuse the government of large-
scale wrongdoing. The rest of the meme-box is set up to 
enact that challenge and rebut the conspiracy theorist 
label. Bill Murray, known for his antics that speak truth to 
power, functions as a symbol of interpellation for the 
conspiracy-minded, who are not taken seriously by the 
mainstream but are convinced of the truth to which they 
have awoken.  
The lower order arguments are presented in claim-
evidence pairs, each contained in smaller boxes in the left -
hand column of the meme. Four claims about government 
malevolence are substantiated with images meant to 
provide evidence.  
The first claim accuses the U.S. government of lying about 
medical treatments of STDs. The image over which the 
textual claim is superimposed features African Americans, 
a visual sign meant to invoke the Tuskegee syphilis study 
that abused black American bodies in a deceptive 
government intervention. The image in fact is an iconic 
historical photograph of the study. But, even in the 
absence of audience knowledge about the provenance of

## Page 37

Digital Rhetorical Ecosystem Analysis, 2021 
 
35 
the photograph, knowledge about the Tuskegee study 
itself is enough to decode the image as representing that 
particular instance of government dishonesty and failure.  
The second claim accuses the government of the ability to 
destroy the planet and is substantiated with the paired 
image of a mushroom cloud that invokes the Hiroshima 
atomic bomb disaster.  
The third claim accuses the government of trafficking in 
drugs. The textual claim is superimposed on an image 
meant to invoke the plane crash that exposed alleged CIA 
involvement in drug trafficking in Panama.  
The fourth box in the left-hand column claims that the 
U.S. government has $21 trillion in debt. Here the paired 
image simply shows a giant vortex of dollar bills 
illustrating the metaphor of “money down the drain”. The 
preceding images which pull from historical archives 
construct the credibility of the meme, leading the viewer 
to implicitly assume the facticity of the final allegation, 
even though the fourth argument departs from the claim-
visual evidence pattern established by the previous three. 
The visual segmentation and sequencing in the meme 
optimizes the constrained space of the meme-box to 
deliver a relatively complex argument with multiple claims 
and pieces of evidence. Each text-image pairing on the left 
works in conjunction with the text-image pairing on the 
right to both verbally and visually enact the if-then 
argument pattern. The boxes on the left provide evidence 
for the claims on the right. For example, the government’s 
dishonesty in the Tuskegee study is presented as evidence 
for the claim that a nationalized health care system cannot 
be trusted because of the ways in which it might abuse 
unsuspecting citizens. Likewise, its willingness to bring 
the planet to the brink of destruction by deploying nuclear 
weapons is provided as evidence that the government 
should not be allowed to regulate gun ownership. The 
strategic use of the meme-box to bound the argument is 
especially stark in this sequence. While evidence of the 
government’s disregard for human life can be leveraged to 
support curtailing the government’s military power, the 
corresponding claim instead attacks gun regulation, 
implying that citizens need to be prepared to defend 
themselves 
against 
an 
untrustworthy 
government.

## Page 38

Digital Rhetorical Ecosystem Analysis, 2021 
 
36 
However, the implication that guns are powerless in the 
face of nuclear destruction, which would undermine the 
meme argument, is suppressed by the visual alignment of 
evidence and claim side-by-side. This visual formatting 
contained within the meme box constrains the possibility 
of additional lines of reasoning even more powerfully than 
a similar argument made through other forms, such as 
orally in a speech or verbally in a news article. The visual 
demarcation of the meme box has the powerful potential 
to restrict reasoning to the elements displayed within the 
box. Because of how distinctly recognizable the meme-box 
has become and how unique it is in appearance compared 
to other visual modes of public discourse, the meme-box 
is able to separate itself from the rest of the landscape of 
public argumentation and create both discrete instances of 
argument unique to its own content and structure, as well 
as to interact within the ecosystem of related memetic 
arguments. 
Phase III. Hidden State Identification 
The four boxes on the left in alignment with each of their 
counterparts on the right together advance the higher-
order claims that the U.S. government is dangerous, 
unethical, and inept and its interventions should be 
substantially curtailed. This claim reifies the hidden-state 
sentiment of distrust in the government. It is important to 
note, also, how the argumentation enacted by the meme 
relies on some but not extensive contextual knowledge in 
the viewer. The parsimony of the symbols within the meme 
(restricted to a few words and images) relies on the 
audience's background knowledge and ability to supply 
warrants. For example, audience knowledge about the 
Tuskegee study and its targeting of African Americans is 
essential to reading the first image on the left-hand side 
as evidence for its paired textual claim. However, even 
minimal recognition of some elements is sufficient for the 
viewer to then accept the other image text pairings and 
submit to the lines of reasoning traced by the memetic 
elements. Likewise, the meme relies on an interpellated 
audience to supply the necessary assumptions (warrants) 
to complete the arguments. For example, the leap from the 
government’s moral failing in the Hiroshima bombing 
does not automatically lead to an argument against gun

## Page 39

Digital Rhetorical Ecosystem Analysis, 2021 
 
37 
regulations, unless the viewer is already concerned about 
the erosion of Second Amendment rights and is thus 
primed to read the atomic bomb image as evidence that 
the government does not have its citizens’ best interests 
at heart and would therefore regulate gun ownership to 
reduce the threat of self-defense from its citizens.  
The two examples elaborated above show the kinds of information 
about memetic claims and hidden states that can be inferred with a 
rhetorical approach. In the following section we integrate the in sights 
from rhetoric and ecology to outline some considerations for the design 
of online discourse monitoring systems. 
V. Toward a High-Throughput Rhetorical 
Analysis (Meme SCADA) 
The example applications of the DRE3 model in the prior section show 
the kinds of information about hidden underlying states inferable with 
a rhetorical approach, that are impossible using syntax -driven analysis 
such as keyword extraction or entity recognition alone. Digital 
discourse moves at a very fast pace. Rapid changes in digital discourse 
(e.g., during an unfolding political event) are likely the times when 
monitoring and analysis are most needed. Unfortunately, the DRE3 
model, as applied above, is low-throughput. This problem is not 
unsolvable. The field of ecology offers a hopeful precedent, because it 
emerged from low-throughput observation of natural history, and later 
increased in scope and rigor through the application of quantitative 
frameworks and large-scale monitoring networks. We propose that 
rhetorical ecosystem analysis is capable of making a similar transition 
to a higher through-put research phase, in the case of some digital 
artifacts. 
The value of developing capabilities for cataloging, indexing, searching, 
mapping, monitoring, and modeling digital discourse is also not limited 
to facilitating research. Just as better ecological understanding and 
monitoring has enabled forecasts, such as those related to algal blooms, 
disease, wildfires, and the potential risks of construction or 
development [97], better understanding and monitoring of digital 
discourse could forecast outbreaks of violence, acceptance of 
government initiatives, the spread of ideology, and the potential risks 
involved in narrative influence [98]. A wide variety of disciplines 
undoubtedly have interest in tools for modeling, mapping, and 
monitoring digital discourse, such as public relations, public health

## Page 40

Digital Rhetorical Ecosystem Analysis, 2021 
 
38 
policy, and military information support operations (MISO) [98]. Man y 
high reliability organizations, or organizations which must maintain 
low-failure rates or risk cascading failure [50], have expressed or 
demonstrated a need for tools which perform these functions [99–103]. 
While recent crisis events have drawn particular interest to the 
potential application of these functions in monitoring and modeling 
digital discourse about public health and political extremism, there has 
been a long-standing need for these functions in areas which are 
entirely 
apolitical, 
such 
as 
of 
multimodal 
content 
regarding 
interpretations of emergency situations like forest fires, floods, and 
earthquakes [104].  
Transitioning from low-throughput to high-throughput, and from 
theory and research to forecasting and decision-making support, will 
only be accomplished by considering the related requirements of the 
outputs, of the processes and methods which lead to them, and of the 
tools and infrastructure which enable them. Here we explore and frame 
these requirements, consider methodology, and propose the structure 
of a monitoring system best categorized as a type of SCADA 
(Supervisory Control and Data Acquisition) system for digital discourse 
which incorporates the DRE3 model and modern computational 
techniques [105]. Addressing the use-case specific requirements of the 
many domains which might have interest in monitoring tools has been 
considered elsewhere [81]. Instead, the focus here will be on the 
requirements for more general sensemaking about public narratives 
generated by image memes. 
Narrative Intelligence 
The general requirements for sensemaking common to all intelligent 
systems are the abilities to capture relevant data from the environment 
(sense), fit the data to expectations or adapt those expectations to fit 
the data (model), and use the expectations to consider or frame choices 
(policy) as a basis for informing action [87]. Various frameworks exist 
to convert these general requirements into formal processes and 
specific requirements for systems which facilitate sensemaking. These 
frameworks are often built for activities which require special 
consideration beyond the fundamental sense-model-policy framework, 
such as in militaries [106–108], teams [107–109], intimate relationships 
[110], machines and AI [111,112], and businesses [113]. Of th e many 
sensemaking frameworks available, intelligence production may be the 
most appropriate for sensemaking related to digital discourse.  
Intelligence production is an organizational sensemaking process which 
is intended to produce deliverables to inform policy that achieves or

## Page 41

Digital Rhetorical Ecosystem Analysis, 2021 
 
39 
maintains the interests of an organization [114,115]. Formal 
intelligence 
production 
processes 
are 
particularly 
helpful 
for 
organizations that are large enough to make the natural emergence of 
synthetic intelligence or macrocognition unlikely or illusory, and for 
organizations which are interacting with systems of interest that are 
sufficiently complex to prevent existing synthetic intelligence from 
being able to manage available sense data appropriately [109,114,116 –
118]. The process of intelligence production was originally semi-
formalized by the Roman military [118] and has been iteratively 
developed throughout history in response to situations where 
conditions complicating macrocognition arose or became exacerbated 
[114,119–123].  
Intelligence production is a helpful way to frame the requirements of 
sensemaking in digital domains given that intelligence production was 
formalized to face similar challenges, such as voluminous collections 
across myriad surfaces, multimodal data [124,125], deception and 
intentional disruption of data collections (counterintelligence) [126], 
and difficulty of detecting, monitoring, and interpreting counterpublic 
membership and activity [50,127–129]. Since intelligence production is 
usually performed by high reliability organizations [50] and faces the 
aforementioned challenges, it has been iteratively developed over time 
to maintain reliability and cope with imperfect data and uncertainty. 
While various specifications exist for particular use-cases, such as in 
business and commercial intelligence [113], generally intelligence 
production is modeled using 5 distinct stages: 1) planning and direction 
(requirements setting), 2) collection, 3) processing and evaluation, 4) 
production and analysis, and 5) dissemination [113,125,130,131]. These 
5 stages provide opportunities for separations of concern between 
categories of function and process, as well as between personnel and 
access to information [131,132] to limit the possibility of “having either 
the facts or the conclusions warped by the inevitable and even proper 
prejudices” of those involved [133]. However, it should be noted that 
the steps formalized in the intelligence production model are not 
necessarily implemented in discrete phases, and that even where 
separate steps are intended, they still occur in parallel with blurs 
between processes [134,135]. 
Ecological and rhetorical metaphors and methodologies may offer 
unique and valuable approaches to monitoring and analyzing digital 
discourse, but no metaphor is a perfect mapping [136]. Here we apply 
the 
intelligence 
production 
framework 
to 
facilitate 
practical 
considerations for “mapping the gap” between ecology- and rhetoric- 
inspired methodology and the needs of a meme analysis pipeline at each 
stage.

## Page 42

Digital Rhetorical Ecosystem Analysis, 2021 
 
40 
Planning and Direction 
The first step of the intelligence production cycle is planning and 
requirements setting. This stage entails considering what kinds 
of intelligence products are needed and in what time frame, and 
translating 
these 
needs 
into 
technical 
and 
personnel 
requirements, scope, and expectations for the following steps 
[130–132]. In the case of a meme analysis pipeline, we suggest 
that the relevant products be broken into 5 broad categories:  
• Data Sets. While raw datasets do not constitute a 
formal intelligence product, the data collected and 
used for projections and other features are 
nonetheless a product which should be made 
available both internally and externally, similar to 
the 
provision 
of 
Twitter’s 
streaming 
API 
(application programming interface) and “Firehose” 
[137,138]. These releases are essential for 3 primary 
reasons. First, the analysis pipeline should never be 
considered entirely complete; data used and 
produced by various features should be available for 
both quality testing and use in the development of 
new features. Second, datasets of content with 
semantic annotations could be invaluable for the 
development and training of AI. Finally, the 
capability 
to 
release 
data 
used 
allows 
for 
reproducibility and transparency in the case that 
outputs are considered partisan or questionable. 
• Research 
Intelligence. 
Research 
intelligence 
refers to information that may provide context or 
support for other intelligence products or help in 
further analysis or sensemaking, such as wikis, or 
“fact books” which might provide details about 
content and communities of interest in the context 
of digital discourse [114,139], field guides for 
providing education on common patterns and 
processes [98], exploratory search features for 
analysts and researchers, and research products 
such as academic articles or white papers. 
• Estimative Intelligence. Estimative intelligence 
refers 
to 
information 
regarding 
uncertain 
phenomena, such as the likelihood of an object 
impacting a particular hidden state, though some 
definitions place a larger emphasis on projection

## Page 43

Digital Rhetorical Ecosystem Analysis, 2021 
 
41 
[140–143]. In the monitoring of digital discourse, 
helpful 
estimative 
intelligence 
might 
include 
metrics and projections regarding the state, rate of 
change, and impact, of beliefs, communities, 
patterns of activity, or content, informed by 
methodologies from ecology and rhetoric. 
• Warning intelligence. Warning intelligence refers 
to information about anomalous phenomena or 
rapid or unexpected changes to system state 
[139,144,145]. 
In 
the 
monitoring 
of 
digital 
discourse, useful examples of warning intelligence 
would include the detection of anomalous activity, 
the emergence of what may be coordinated, 
aggressive, and strategic activity associated with 
untracked or tracked objects or communities, 
notifications about other organized activity such as 
the censorship of content on a platform, or the 
presence of harassment, threats, or explicitly illegal 
activity. 
• Actionable Intelligence. Actionable intelligence 
suffers from a lack of consistent usage or a 
consistent definition, but generally refers to 
information which needs to be addressed urgently 
and informs or enables actions that might be or 
need to be taken [146]. In the monitoring of digital 
discourse, 
actionable 
intelligence 
would 
help 
inform interventions such as the removal of 
content, inform design of content or messaging 
based on current trends, and guide sensemaking by 
providing new routes to consider when presented 
with ambiguity or structurally complex information. 
Collection 
The second step is broadly referred to as “collection”. This term 
is sometimes used to refer to the entirety of the intelligence 
production cycle [133,147]. However, in the context of the 
production cycle and its processes, it refers to the conversion of 
requirements set during planning and direction into tangible 
targeting, selection, and instrumentation choices in order to 
collect data [125,130,148]. At this stage, the focus is on the 
collection of “raw intelligence”, or unanalyzed information, in 
accordance with requirements—as such, it is sometimes referred

## Page 44

Digital Rhetorical Ecosystem Analysis, 2021 
 
42 
to as collation [132]. In the past, organization of raw intelligence 
was fairly disorganized [118–120,134,149]. But with the increase 
in volume, and the need to collect multimodal data from myriad 
surfaces, came a need for specialization not just in analysis but 
in the collection of raw intelligence as well, resulting in various 
formal categories of tradecraft, or types of intelligence collection 
and annotation methodologies [130,150]. 
There are a series of ethical and practical challenges to the 
development of collection requirements and procedure for image 
memes in the interest of developing an image meme analysis 
pipeline. A root problem, worth addressing first, is that even at 
the cutting edge of machine learning applications in analyzing 
memes, there are serious limitations imposed by the lack of 
existing annotated collections to use as training data [23]. Thus, 
the use of AI at this time for automated collections would likely 
be inappropriate given that even the ability to differentiate 
between an “image meme” and “just an image” is a difficult, 
semantic challenge—let alone the ability to analyze it. However, 
given the rate of change, complexity, and volume of image 
memes, collection would place too high a burden on researchers, 
experts, and analysts. Crowd-sourcing may therefore be the best 
avenue of approach. While crowd-sourcing approaches have 
come under criticism, recent successes indicate that more 
complex tasks may now be ready to be outsourced to crowds [95]. 
Choices in incentivization mechanisms and user experience 
design would need to be considered in depth elsewhere, but there 
is a rich history of crowd-sourcing data in ecology which could 
be of use in framing collection requirements. For example, 
millions of entries for bird sightings are generated by citizen bird 
watchers each month [151] and data from bird sighting 
submissions can be used by analysts for real-time monitoring of 
animal activity as well as for forecasting phenomena such as 
outbreaks of West Nile virus [152]. The frameworks used for 
crowd-sourcing in ecology may allow for a direct transfer to 
other domains, such as those which provide data management 
principles [153] and offer methods for improving information 
quality or “Crowd IQ” [154]. 
Among the approaches developed in ecology and ecology-
adjacent fields from learning-by-doing in crowd-sourcing, three 
stand out as both valuable and immediately applicable. First, 
based on crowd-sourced classification of plants and birds, 
quality of collections can be greatly improved simply by 
improving the quality and scope of the class structures (schema)

## Page 45

Digital Rhetorical Ecosystem Analysis, 2021 
 
43 
and data standards the crowd will interact with [154]. Second, 
the study of crowd-sourcing fish classifications and remote-
sensing in hydro-ecology has shown that quality can be improved 
over time by segmenting users by expertise and using these 
segmentations to provide different levels of responsibility 
[155,156]. 
Third, 
work 
on 
crowd-sourcing 
biomedical 
annotations has revealed that expert contributions can be used 
to train and tune user contributions, particularly to detect 
anomalies and unexpected deviations from patterns. Similarly, 
user contributions can be used to train and tune automated 
systems and be assisted and guided by them in performing 
contribution tasks (see figure 10) [95]. These approaches could 
be directly applied to “field” collections of image memes. Given 
that collections are occurring online, most relevant information, 
such as where the object was collected, the object’s file type, and 
reaction or “impact” data if it was collected from social media, 
could be automatically fit to pre-existing data standards with no 
need for experts involved in collections before being placed in a 
buffer for classification. The collected objects could then be 
used to train AI to determine what and what does not constitute 
a meme. 
While it might be reasonably assumed that data about the user 
who posted the collected object should be automatically parsed 
and collected as well, this may not be necessary. As noted 
elsewhere in this article, memes, particularly political memes, are 
often presented without attribution. Further, user data may need 
to be bypassed because creating or sharing political or even 
Figure 10. The flow of benefits offered between types of user contributions. 
Contributions by user segments with higher levels of competency in a task can be 
used as training data for those of a lower competency, while contributions from 
segments with lower levels of competency can be used to help provide guidance 
to those of a higher competency (e.g., suggested classifications).

## Page 46

Digital Rhetorical Ecosystem Analysis, 2021 
 
44 
quasi-political memes or other content, especially within 
counter-publics where meme-activity is rich and of interest to 
researchers, 
is 
increasingly 
being 
accompanied 
by 
the 
expectation of potential consequences from peers [157], 
employers [158,159], and institutions [160,161], as well as by 
potential punitive consequences from media-sharing platforms 
[162–165] and governments [166,167]. The DRE3 model’s focus 
on claims in memes informed by a rhetorical approach, and on 
relationships, placement, and change of that content informed 
by an ecological approach, as opposed to a focus on the identity 
of the poster, prevents misattribution or association inferred by 
posting history (e.g. a CDC official sharing an anti-vaccination 
meme for educational purposes), reduces the potential for harm 
by “outing” or “doxxing” internet users, especially in countries 
with higher potential for consequences for sharing political 
content, and reduces the potential for critical misuse of the 
analysis pipeline. For the purposes of understanding movement 
of memes specifically, the channel over which the meme travels 
is sufficient. If the collector of the meme in context with a 
particular platform constitutes a channel, then this channel can 
be considered a location—leaving no reason to deanonymize the 
collector and making the generation of an “identity” within the 
pipeline an opt-in exercise. 
Processing and Evaluation 
The third step of the cycle is often referred to as processing 
and evaluation and refers to a pre-analysis stage in which data 
is cleaned, refined [148], and filtered [130] and the reliability 
and credibility of sources of the information are considere d 
[132,134,168]. The raw intelligence assembled in the collection 
phase is now altered or reassembled for usability, “coded data 
is 
decrypted, 
foreign 
languages 
[are] 
translated, 
and 
photographic material [is] interpreted” [148]. The importance 
of processing and filtering cannot be overlooked. Without 
comparable measures, accessible reference information, or 
compression into usable formats, much of the data could 
essentially become meaningless [169]. When this processing is 
done in concert with proper scope and orientation introduced 
in the planning and direction phase, it also reduces the potential 
for endless abstraction by making the means and intentions of 
the process clear [87,170]. 
It is at this stage in an image meme analysis pipeline that experts 
would be needed to begin classifying objects and improving

## Page 47

Digital Rhetorical Ecosystem Analysis, 2021 
 
45 
information quality as the pipeline begins to move beyond 
syntax and metadata toward semantic annotations. Even with 
the use of crowd-sourced and automated collections, the load 
would still be far too great for experts and trained analysts to 
handle alone. This being the case, the same framework of 
training, guidance, and segmentation between the kinds of 
contributors described in the prior section would offer 
continued utility (see figure 10). Automated systems would be 
given responsibilities such as detecting quantitative features 
that are correlated with virality and longevity of the image 
meme, which can then be used to direct the attention of both 
experts and average users [23]. These systems would make use 
of data from the contributions of human users to train for more 
complex 
tasks. 
Expert 
users 
would 
have 
the 
primary 
responsibility of developing and detecting claim and argument 
patterns and applying these labels to content, which could then 
be used to train average users or even AI to do the same. 
Claim 
identification 
presents 
the 
largest 
challenge 
to 
crowdsourcing the DRE3 model due to the subjectivity of the 
extraction whether it comes from rhetorical experts or average 
users. Image memes, as discussed in prior sections, tend to have 
an ambiguity which offers the poster plausible deniability about 
the assertion of claims. Therefore, simple automation of feature 
recognition cannot be relied on for extracting claims from 
images. However, this challenge may instead be seen as an 
opportunity. There are many viable methods for extracting and 
aggregating arguments from text [171–173], allowing for the 
substance of these common arguments in various phrasings to 
be aggregated and clustered. The remaining disparity between 
interpretations would not, and should not, be considered 
noise—but instead valuable data for producing metrics related 
to the subjectivity and complexity of the content and of diverse 
perspectives interpreting it. Average users would share 
responsibility for claim extraction, though their primary 
responsibility would be the extraction of relevant entities from 
the content. 
Once experts have provided sufficient labeling of rhetorical 
pattern and structure, average users could be slowly trai ned. 
Segments of those users may even eventually be trusted with 
contributing rhetorical or other expert classifications, though 
the provision of greater responsibilities would likely require 
new tools or frameworks for managing trust in crowd -sourcing 
systems. Automated features however, would likely need to stay

## Page 48

Digital Rhetorical Ecosystem Analysis, 2021 
 
46 
in a guidance role regarding most semantic analysis of image 
memes. Semantics on the internet are prone to rapid change and 
often require contextual knowledge. For example, triple 
brackets around an organization or person’s name is now often 
considered an antisemitic symbol marking Jewish background 
or influence. But obviously, not all uses of triple brackets 
indicate this—and worse, prior to this association, the same 
triple brackets were used to indicate a “cyberhug”. This does 
not mean that automated features would be useless. For 
example, the ability to note that some typographical feature may 
mean something to specific audiences and to direct a user's 
attention to that symbol is a valuable guidance feature. 
Production and Analysis 
The fourth stage of the cycle is referred to as production and 
analysis, wherein experts begin to produce the intelligence 
products requested, given the collected, processed, and 
evaluated information available and relevant to them [148]. At 
this stage in a meme analysis pipeline, data and content 
cataloged throughout the collection and processing stages can 
now be structured into data sets for developing, improving, 
and replicating automated features at all stages in t he pipeline 
and for more specific exploratory analysis by experts. More 
importantly, it is also at this stage in the meme -analysis 
pipeline that rhetorical and ecological framing and techniques 
begin to have their most valuable contributions. 
• Research Intelligence. The content labels, entity 
extractions, and identified claims informed by 
rhetoric now have a role in enabling semantics -
driven 
exploratory 
search. 
The 
bottom-up 
detection of patterns and topological motifs allow 
analysts to view single pieces of content as a part 
of memetic clusters, not just of other pieces of 
content, but of entities, claims, and subclaims 
expressed in that content, and of the hidden states 
that may be signaled by them. With the metrics 
and features which accompany the objects labeled 
within these memetic clusters, the analyst is able 
to monitor a semantic field, or rhetorical 
ecosystem, as described in previous sections, 
before analysis has even been performed. The data 
is now available to enable methods of analysis 
from 
ecology 
discussed 
elsewhere 
in 
this

## Page 49

Digital Rhetorical Ecosystem Analysis, 2021 
 
47 
document. In addition, the content, patterns, and 
aforementioned ecological motifs can now be 
structured into coherent and navigable wikis, field 
guides, and fact books, modeled after the large, 
robust identification systems and guides found in 
ecology—helping improve methods and standards 
at all stages of the pipeline and increasing the 
likelihood of novel genres or features being 
detected.  
• Estimative Intelligence. The use of ecological 
frameworks and methods for identifying and 
communicating state features of content and 
claims, and considering the relationships between 
entities, 
memes, 
and 
claims, 
as 
discussed 
previously, could be of great value. The ability to 
classify and quantify state features implies the 
ability to consider potential for impact and 
spread, as well as the ability to measure rate. The 
provision of data regarding these changes to 
content and claims and related rates of changes 
may allow analysts to not only communicate 
current state, but also project future state of both 
claims 
and 
associated 
hidden 
states. 
This 
information can be leveraged in order to generate 
reports regarding underlying ecosystem hidden 
state features and their potential for change. 
• Warning Intelligence. The ability to classify and 
quantify state features, and project future states, 
further implies the ability to use those projections 
in the production of warning intelligence or 
general alerts. First, with the presence of patterns 
of spread, rhetorical structure, and state changes, 
comes the ability to detect breaks from expected 
patterns, or anomaly signaling. These anomalies 
can be prioritized and reviewed in ex post analysis 
to reveal and catalog new patterns, allowing for 
indications of phenomena which urgently require 
attention, such as swarm-behavior in 
political 
happenings, communications, harassment, censorship 
events, or organized activity. In addition, the 
ability to simply index content paired with the 
ability to classify and quantify state features 
means an ability to tag or “track” content.

## Page 50

Digital Rhetorical Ecosystem Analysis, 2021 
 
48 
Ecology already has robust methods for the 
tagging of animals, some of which are used to 
enable early warning and risk alert systems. 
Similar methods could help inform the translation 
of changes to state into relevant notifications and 
warnings [174].  
• Actionable Intelligence. State features and 
context provided by hidden state analysis could 
generate 
intelligence 
products 
to 
improve 
decision-making around digital discourse in a 
number of ways. First, design and timing of 
content could be informed by the hidden states 
behind the claims dominating the environments 
they are intended to be deployed in. Second, if 
certain activities presented in warning intelligence 
require action, state features and hidden states can 
inform 
interventions. 
Finally, 
organizations 
whose decisions are meant to be informed by the 
interests 
of 
their 
constituencies 
can 
learn, 
through the tracking of claims, what those 
interests are, to increase the relevance of, and 
avoid 
negative 
externalities 
in, 
content 
deployments. 
Dissemination 
The final step of the cycle is the dissemination of intelligence 
products 
to 
stakeholders 
and 
decision-makers 
[102,104,113,119] and integration of those products into 
existing knowledge-bases for future use [96,119]. The various 
categories of individuals who would receive these intelligence 
products are often broadly referred to as “consumers'' or 
“users” [104]. These intelligence products are traditionally 
written 
or 
oral 
reports 
intended 
to 
be 
periodically 
disseminated [148]. However, an insight which may be gleaned 
from ecological and ecology-adjacent forecasting is that when 
threats tend to be fast-moving or ongoing, and cannot be 
solved, only managed, intelligence needs to be consistently 
available, updated in real-time, and automatically disseminated 
and tailored based on expected need or upon request [59,175]. 
While the release of both periodical and non-periodical 
publications, newsletters, and briefings would be of value, they 
could not be relied on as the only method of dissemination to 
stakeholders.

## Page 51

Digital Rhetorical Ecosystem Analysis, 2021 
 
49 
In addition to these static disseminations, intelligence 
products would have to be tailored and presented in several 
ways. First and foremost, would be automated and other on-
demand reports, that could be made available when requested, 
on particular claims, clusters, or other queryable objects. The 
ability to have dissemination via notification would be 
significant as well, given that warning intelligence is, by its 
nature, emergent and non-periodic, and is therefore in need of 
a channel over which it can be provided to those to whom it 
would be most relevant. Further, who may need this warning 
intelligence can change greatly with context. For example, 
warning intelligence regarding purported foreign influence of 
memetic content would only become relevant to some users of 
pipeline outputs upon their viewing of that content. Thus, 
intelligence would also have to be made available upon 
encounter. On-encounter dissemination could also be useful in 
terms 
of 
actionable 
intelligence, 
to 
help 
facilitate 
interventions, or, in terms of estimative intelligence and 
research intelligence, to allow analysts to use the content in 
front of them to direct the exploratory search of the existing 
corpus in developing new intelligence products, or to allow 
contributors during the processing and evaluation phase to 
better understand how to perform classification. Finally, given 
the rate of change in digital discourse, the ability to watch 
intelligence update in real time becomes essential. This type of 
real-time analysis of large volumes of digital discourse would 
be useful for a range of individuals, for example, public health 
officials observing the dynamics of public sentiment and 
impact of government messaging [81]. 
Toward a Meme SCADA 
With these requirements in mind, there is one approach in particular 
which presents the affordances and flexibility necessary to handle all 
of the challenges posed by the production cycle discussed above: the 
use of dashboard-based SCADA (Supervisory, Control, and Data 
Acquisition) systems. SCADAs are used to supervise state, acquire 
data from remote sensors, and control operations in real time [176]. 
While SCADA systems were traditionally intended for use in 
industrial operations, approaches from this area of research and 
application have recently gained traction in ecology [177,178]. 
Framing image meme analysis pipeline as part of a SCADA 
infrastructure is potentially the most practical approach for two 
primary reasons. First, SCADA infrastructure is built with real -time

## Page 52

Digital Rhetorical Ecosystem Analysis, 2021 
 
50 
use in mind and designed to facilitate the production of dashboard -
like presentations of multimodal data and hidden states which are 
often difficult to communicate. Second, SCADA infrastructure 
design methodologies assume the need to collect and aggregate data 
from myriad sensors, and help inform information fusion protocols 
needed to generate forecasts, estimates, and current state features in 
real-time. In the case of the meme-analysis pipeline, supervisory and 
data acquisition features would be most prominent, though control 
features might be expressed in the form of prioritizations for users 
performing classifications and collections (such as during political  
happenings or swarm-behavior events), and in the form of explicit 
direction of automated collections and classifications. Here we 
present the rough blueprint of a meme analysis pipeline built in the 
style of an ecological or industrial SCADA system, from the 
requirements and outputs discussed within the previous section (see 
Figures 11 and 12). 
Figure 11 shows the process by which artifacts (image memes) are 
collected, processed, analyzed, and disseminated. It begins with 
automated 
and 
manual 
collections 
of 
artifacts 
being 
given 
standardized annotations related to the location, structure (data 
type), and impact of the item. Next, these yet-to-be-processed 
artifacts are placed into a buffer; experts, average users, and 
automated features select artifacts from this buffer to identify their 
(i) 
statistically 
or 
quantitatively 
derived 
attributes 
and 
classifications, (ii) featured entities, (iii) claims, and rhetorical 
structure. The artifacts are annotated with these classifications using 
rhetorical and format annotation standards before being placed into 
an indexed and queryable catalog. Automated features and experts 
can draw from this catalog to perform analyses offered through a 
dashboard system for dissemination and monitoring. In addition, 
developers could use the catalog for training and test data in the 
development of new automated features. Finally, experts can make 
requests through the dashboard for prioritizations on manual 
collections and could direct the prioritization of automated 
collections (e.g., on certain kinds of content or from specific 
communities). Figure 12 shows the various forms of analysis and 
products which should be made available both through the dashboard 
and otherwise.

## Page 53

Digital Rhetorical Ecosystem Analysis, 2021 
 
51 
 
 
 
Figure 11. A rough blueprint of a meme-analysis pipeline. Color is used to indicate areas 
of the pipeline related to specific aspects of SCADA systems (blue), DRE3 analysis layers 
(purple), and intelligence analysis stages (red). The blueprint shows the various steps of 
content collection, processing, and analysis leading to the management of final intelligence 
products within a dashboard.

## Page 54

Digital Rhetorical Ecosystem Analysis, 2021 
 
52 
 
 
 
Figure 12. A map of desired outputs from a meme-analysis pipeline.

## Page 55

Digital Rhetorical Ecosystem Analysis, 2021 
 
53 
VI. Discussion 
In this paper, we have reviewed the relevance of rhetorical and 
ecological approaches for analyzing multimedia digital discourse, 
such as shareable image memes. While rhetorical analysis captures 
the nuanced relationships between artifacts and audiences, e cological 
analysis captures the complex relationships among organisms and 
their niche. Others have explored similarities between the fields of 
ecology and rhetoric [37,179]. We have elaborated this connection 
through three key themes from modern ecology: the multilevel 
systems perspective, antifragility, and ecosystem services. These key 
themes integrated into the Digital Rhetorical Ecosystem three -tier 
(DRE3) model, providing a framework for incorporating rhetoric 
into computational pipelines for analyzing digital discourse, with 
ecological toolkits and frameworks as intermediaries.  In addition to 
the transfer of concepts used in ecology into the digital discourse 
space and specific implications for SCADA design, here we conclude 
by exploring some broader implications.  
We go so far as to hypothesize that a disruption or correction of 
narratives forged through memetic circulation needs to adopt the 
memetic form itself, sometimes known as a counter-meme [180]. We 
advocate re-deploying the memetic form to interrupt the credibility 
of a specific meme argument by illustrating why the claim advanced 
by the original meme does not rest soundly on the evidence or the 
warrants (assumptions) signaled explicitly or implicitly within the 
meme. Current efforts to fact-check memes address memes with a 
different genre of rebuttal discourse (e.g., the Facebook fact-check 
box that often links to news articles of official credibility). Digital 
audiences that have become vulnerable to the influence of memetic 
argument have also grown a staunch resistance to this particular form 
of fact-checking. Therefore, we argue that any attempt to neutralize 
memetically 
constructed 
narratives 
needs 
to 
understand 
the 
rhetorical power encoded within the memetic form and to use that 
form strategically to restructure public discourse. We urge, however, 
that counter-memetic efforts acknowledge the conditions of 
cognitive complexity endemic to digital knowledge environments and 
avoid the pitfalls of easy fact/fiction dichotomy for issues that are 
murky, complex, or ambiguous. Counter-memetic strategy should 
expose how memes mistakenly create narratives of certainty in the 
face of situational ambiguity and complexity. That is, counter memes 
should avoid making new issue-based arguments themselves, and 
instead reveal the argument weaknesses in memes deployed to 
advance public argument. Simply put, memes can be used to

## Page 56

Digital Rhetorical Ecosystem Analysis, 2021 
 
54 
demonstrate the argument weaknesses of memes. The repeated 
circulation of rebuttal memes to demonstrate the inferiority of 
memetic argument has potential to eventually decelerate reliance on 
the memetic form in public discourse. In addition, asking users to 
identify claims embedded within image memes during the stage of 
data processing and evaluation (Figure 11), could induce a more 
critical or meta-cognitive engagement with the memetic content and 
its deficits. 
Rhetorical analysis has traditionally focused on single cases. 
Advances in computational technology provide the possibility of 
scaling up rhetorical analysis, for at least certain k inds of artifacts, 
such as image memes. Such high-throughput automated possibilities 
are evident in AI software such as Project Debater [181] and 
SwarmCheck [182] which can make sense of voluminous amounts of 
argument data using argumentation principles. T he integration of 
rhetorical analysis with ecosystem tracking into a SCADA can enrich 
the field of rhetorical study by growing data -driven rhetorical theory. 
In 1969, Chaim Perelman and Lucy Olbrechts Tyteca published the 
influential 
New 
Rhetoric—a 
comprehensive 
compendium 
of 
argument strategies that relied not on formal logic but on everyday 
rhetorical practices [183]. Their catalog was built upon meticulous 
collection and analysis of real specimens of persuasion. Likewise, 
with the building of the proposed SCADA, we have the possibility 
of identifying and cataloging argument patterns across large amounts 
of image meme data, in a partially-automated fashion. The incidental 
value to argumentation theory of tracking the emergence, interaction, 
proliferation, and demise of image memes through discursive 
ecosystems is significant. We can determine whether argument 
patterns in image memes replicate documented argument patterns or 
assemble new ones. We can assess whether the unique genre of the 
image meme privileges certain argument patterns over others. An 
over-reliance on certain argument patterns (like argument by 
exposing hypocrisy [17]) may signal epistemic trends that are being 
exploited in the digital public sphere because they make minimal 
attention demands. When audiences are conditioned to argue in 
certain ways, their receptivity to other argument patterns that 
demand more central processing may diminish. We may observe at 
scale, with the intelligence that emerges from the SCADA, that one 
significant answer to the epistemic crisis we are currently battling is 
to understand the problem not just through a content framework 
(e.g., the fake news-real news dichotomy) but rather to problematize 
the medium, in this case the rhetorical form of the image meme, as 
one of the primary drivers of the crisis.

## Page 57

Digital Rhetorical Ecosystem Analysis, 2021 
 
55 
Another way to address the crisis is by examining ethical frameworks 
for managing a resource commons. In ecological philosophy, the 
“land ethic” [184] captures a sense of duty and responsibility towards 
ecosystem interactions. In the eponymous book, Aldo Leopold 
contrasted the land ethic with alternative frameworks that might be 
used to guide decisions around resource use, such as economic 
valuation, pragmatic use, and libertarian or egalitarian ideology. The 
land ethic serves as a conceptual nexus that integrates actors with 
different interests, and bridges world knowledge traditions. The 
application of a land ethic to online spaces might help ground 
otherwise-abstract digital communities and give a framework for 
service through deep time to these spaces. The ecological land ethic 
begins from a scientific foundation, then introduces insights from 
psychology and philosophy to characterize the nature of proper 
human-ecosystem relationships. In the case of a digital comm ons 
ethic, the system is physically grounded in the software and hardware 
that are the enabling architecture of the online platform. Framing an 
empirical (computational) basis as a starting point for studying 
online discourse could allow a “rhetorical commons” ethic to emerge, 
as driven and structured by psychological and ethical preferences.  
Approaches to collective governance of ecological and resource 
commons have also integrated the economic insights of Elinor 
Ostrom and others [185]. As with these ecological commons, digital 
governance and economic systems could be designed with specified 
functions, performance metrics, and a stated collective purpose 
[186]. This model of “digital commons as public good” has already 
been applied to online communities [187,188]. Connecting the notion 
of “rhetorical commons” to the economic game theoretic setting of 
the “tragedy of the commons” helps connect the behavior of users, 
to outcomes at the level of the commons [189].  
Conclusions and Recommendations 
Can an ecological framework layered on rhetorical analysis help 
bridge the world of meaning and the capacities of computational 
pipelines? The ongoing and changing nature of the epistemic cris is 
requires new technological approaches towards scaling the modeling 
and understanding of our rhetorical commons. Here we expanded on 
previous appeals to rhetorical ecology and observations of the 
fundamental similarities between these fields [37], to posit the 
foundation for a type of system which might be able to infer, model, 
and intervene in multimedia digital discourse. With such a system, it 
could be possible to move beyond syntactic and user -driven 
understandings of digital discourse, to better observe and codify

## Page 58

Digital Rhetorical Ecosystem Analysis, 2021 
 
56 
cycles and patterns within it, and to make progress towards 
ecologically-framed platform policies which can be more clearly 
informed by social preferences and values.  
Recommendations: 
• Review best practices in improving information 
quality of crowdsourced subject-matter tagging in 
physical, digital, and rhetorical ecosystem contexts. 
• Review and synthesize research on argument mining 
methodologies using crowdsourced annotations. 
• Research the implementation and limitations of 
applications and web extensions for providing 
lenses (e.g., enriched augmented views of an object) 
on content displayed on various electronic devices. 
• Curate a list of qualitative and quantitative patterns 
in the rhetorical structure and use of image memes.  
• Consider users a part of an information commons 
rather than simply affected by an information 
system in future work on misinformation dynamics. 
• Ensure that the identity, privacy, and preferences of 
users 
are 
protected 
in 
rhetorical 
cataloging 
schemes.

## Page 59

Digital Rhetorical Ecosystem Analysis, 2021 
 
57 
Funding and Acknowledgements 
Richard J. Cordes is funded by the NSF Convergence Accelerator Trust 
and Authenticity in Communication Systems Program (NSF 21-572), 
under award ID #49100421C0036 and is supported in research efforts 
through a Nonresident Fellowship with the Atlantic Council on 
appointment to the GeoTech Center.  
Daniel A. Friedman is funded by the NSF program Postdoctoral 
Research Fellowships in Biology (NSF 20-077), under award ID 
#2010290.

## Page 60

Digital Rhetorical Ecosystem Analysis, 2021 
 
58 
Works Cited 
Generated using a reference manager. 
1. 
Benkler Y, Faris R, Roberts H. Network Propaganda: 
Manipulation, Disinformation, and Radicalization in American 
Politics. Oxford University Press; 2018. 
2. 
Rowell L, Call-Cummings M. Knowledge Democracy, Action 
Research, the Internet and the Epistemic Crisis. Journa l of 
Futures Studies. 2020;24: 73–81. 
3. 
Miller M, Kirwan J. The Modern Origins of Our Epistemic 
Crisis: A Media & Democracy Workshop. 7 May 2019 [cited 24 
Jun 2021]. Available: https://items.ssrc.org/from-our-
programs/the-modern-origins-of-our-epistemic-crisis-a-media-
democracy-workshop/ 
4. 
Firth J, Torous J, Stubbs B, Firth JA, Steiner GZ, Smith L, et al. 
The “online brain”: how the Internet may be changing our 
cognition. World Psychiatry. 2019;18: 119–129. 
5. 
Menczer F, Hills T. Information Overload Helps Fake Ne ws 
Spread, and Social Media Knows It. Scientific American. 
doi:10.1038/scientificamerican1220-54 
6. 
Morris JD, Woo C, Singh AJ. Elaboration likelihood model: A 
missing intrinsic emotional implication. Journal of Targeting, 
Measurement and Analysis for Marketing. 2005;14: 79–98. 
7. 
SanJosé-Cabezudo R, Gutiérrez-Arranz AM, Gutiérrez-Cillán J. 
The combined influence of central and peripheral routes in the 
online persuasion process. Cyberpsychol Behav. 2009;12: 299 –
308. 
8. 
Dunbar NE, Connelly S, Jensen ML, Adame BJ, Rozzell B, 
Griffith JA. Fear Appeals, Message Processing Cues, and 
Credibility in the Websites of Violent, Ideological, and 
Nonideological Groups. J Comput Mediat Commun. 2014;19: 
871–889. 
9. 
Tindale CW. Replicating Reasons: Arguments, Memes, and the 
Cognitive Environment. Philosophy & Rhetoric. 2017;50: 566–
588. 
10. 
Denisova A. Meme. [cited 6 Aug 2021]. Available: 
https://sk.sagepub.com/reference/the-sage-encyclopedia-of-
mass-media-and-society/i10854.xml

## Page 61

Digital Rhetorical Ecosystem Analysis, 2021 
 
59 
11. 
Shifman L. Memes in a Digital World: Reconciling with a 
Conceptual Troublemaker. J Comput Mediat Commun. 2013;18: 
362–377. 
12. 
Shifman L. The Cultural Logic of Photo-Based Meme Genres. 
Journal of Visual Culture. 2014;13: 340–358. 
13. 
Catchphrases. 7 Mar 2012 [cited 24 Jun 2021]. Available: 
https://knowyourmeme.com/memes/cultures/catchphrases 
14. 
Taecharungroj V, Nueangjamnong P. Humour 2.0: Styles and 
Types of Humour and Virality of Memes on Facebook. Journal 
of Creative Communications. 2015;10: 288–302. 
15. 
Guenther L, Ruhrmann G, Bischoff J, Penzel T, Weber A. 
Strategic Framing and Social Media Engagement: Analyzing 
Memes Posted by the German Identitarian Movement on 
Facebook. Social Media + Society. 2020;6: 2056305119898777.  
16. 
Facebook: From Election to Insurrection. [cited 11 Aug 2021]. 
Available: 
https://secure.avaaz.org/campaign/en/facebook_election_insurr
ection/?slideshow 
17. 
Mascarenhas M. Memes as Quasi-Argument. Local Theories of 
Argument. 2021. pp. 385–390. doi:10.4324/9781003149026-65 
18. 
Rapp C. Aristotle’s Rhetoric. Zalta EN, editor. The Stanford 
Encyclopedia of Philosophy. Metaphysics Research Lab, Stanford 
University; 2010. Available: 
https://plato.stanford.edu/archives/spr2010/entries/aristotle -
rhetoric/ 
19. 
Harrell J, Linkugel WA. On Rhetorical Genre: An Organizing 
Perspective. Philosophy & Rhetoric. 1978;11: 262–281. 
20. 
Heiskanen B. Meme-ing electoral participation. Eur J Am Stud. 
2017;12. doi:10.4000/ejas.12158 
21. 
Hakoköngäs E, Halmesvaara O, Sakki I. Persuasion Through 
Bitter Humor: Multimodal Discourse Analysis of Rhetoric in 
Internet Memes of Two Far-Right Groups in Finland. Social 
Media + Society. 2020;6: 2056305120921575. 
22. 
Huntington HE. Affect and effect of Internet memes: assessing 
perceptions and influence of online user-generated political 
discourse as media, The. Colorado State University. 2017. 
Available: 
https://mountainscholar.org/bitstream/handle/10217/183936/
Huntington_colostate_0053A_14303.pdf 
23. 
Ling C, AbuHilal I, Blackburn J, De Cristofaro E, Zannettou S, 
Stringhini G. Dissecting the Meme Magic: Understanding

## Page 62

Digital Rhetorical Ecosystem Analysis, 2021 
 
60 
Indicators of Virality in Image Memes. Proc ACM Hum-Comput 
Interact. 2021;5: 1–24. 
24. 
Charland M. Constitutive rhetoric: The case of the peuple 
québécois. Q J Speech. 1987;73: 133–150. 
25. 
Kofman A. Bruno Latour, the Post-Truth Philosopher, Mounts a 
Defense of Science. The New York Times. 25 Oct 2018. 
Available: 
https://www.nytimes.com/2018/10/25/magazine/bruno-latour-
post-truth-philosopher-science.html. Accessed 11 Aug 2021. 
26. 
Ceccarelli L. Polysemy: Multiple meanings in rhetorical criticism. 
Q J Speech. 1998;84: 395–415. 
27. 
Wikipedia contributors. Condescending Wonka. In: Wikipedia, 
The Free Encyclopedia [Internet]. 1 Jun 2021. Available: 
https://en.wikipedia.org/w/index.php?title=Condescending_Wo
nka&oldid=1026354342 
28. 
Beveridge A, Chemers M. The Game of Game of Thrones : 
Networked Concordances and Fractal Dramaturgy. Reading 
Contemporary Serial Television Universes. Routledge; 2018. pp. 
201–225. 
29. 
Hybrid ecosystem of narratives. 12 Apr 2009 [cited 25 Mar 
2021]. Available: 
https://tihane.wordpress.com/2009/04/12/hybrid-ecosystem-
of-narratives/ 
30. 
Druschke CG. A Trophic Future for Rhetorical Ecologies. 
Enculturation: a journal of rhetoric, writing, and culture. 2019 
[cited 24 Jun 2021]. Available: http://enculturation.net/a -
trophic-future 
31. 
Fiaidhi J, Mohammed S. Virtual care for cyber–physical systems 
(VH_CPS): NODE-RED, community of practice and thick data 
analytics ecosystem. Comput Commun. 2021;170: 84–94. 
32. 
Wang H, Liu Z, Guo Y, Chen X, Zhang M, Xu G, et al. An 
Explorative Study of the Mobile App Ecosystem from App 
Developers’ Perspective. Proceedings of the 26th Intern ational 
Conference on World Wide Web. Republic and Canton of 
Geneva, CHE: International World Wide Web Conferences 
Steering Committee; 2017. pp. 163–172. 
33. 
Fiorina C. HP Carly Fiorina Speech: The Digital Ecosystem. 
[cited 27 Apr 2021]. Available: 
http://www.hp.com/hpinfo/execteam/speeches/fiorina/ceo_wo
rldres_00.html 
34. 
Games SJ. Transhuman Space Toxic Memes. First Ed edition. 
Steve Jackson Games, Incorporated; 2004.

## Page 63

Digital Rhetorical Ecosystem Analysis, 2021 
 
61 
35. 
Ford T, Krohn R, Weninger T. Competition Dynamics in the 
Meme Ecosystem. arXiv [cs.SI]. 2021. Available: 
http://arxiv.org/abs/2102.03952 
36. 
Zannettou S, Caulfield T, Blackburn J, De Cristofaro E, 
Sirivianos M, Stringhini G, et al. On the Origins of Memes by 
Means of Fringe Web Communities. arXiv [cs.SI]. 2018. 
Available: http://arxiv.org/abs/1805.12512 
37. 
Druschke CG, McGreavy B. Why rhetoric matters for ecology. 
Front Ecol Environ. 2016;14: 46–52. 
38. 
Friedman D, Tschantz A, Ramstead MJD, Friston K, Constant A. 
Active inferants: The basis for an active inference framework for 
ant colony behavior. Front Behav Neurosci. 2021;15: 126. 
39. 
Edbauer J. Unframing Models of Public Distribution: From 
Rhetorical Situation to Rhetorical Ecologies. Rhetor Soc Q. 
2005;35: 5–24. 
40. 
Equihua M, Espinosa Aldama M, Gershenson C, López-Corona 
O, Munguía M, Pérez-Maqueo O, et al. Ecosystem antifragility: 
beyond integrity and resilience. PeerJ. 2020;8: e8533.  
41. 
Marcellino W, Helmus TC, Kerrigan J. Detecting Conspiracy 
Theories on Social Media: Improving Machine Learning to 
Detect and Understand Online Conspiracy Theories. RAND 
Corporation; 2021. 
42. 
Cordes RJ, Friedman DA. Reimagining Maps. The Great Preset: 
Remote Teams and Operational Art. COGSEC; 2020. 
43. 
Ramstead MJD, Constant A, Badcock PB, Friston KJ. Variational 
ecology and the physics of sentient systems. Phys Life Rev. 
2019. doi:10.1016/j.plrev.2018.12.002 
44. 
Budaev S, Jørgensen C, Mangel M, Eliassen S, Giske J. Decision -
Making From the Animal Perspective: Bridging Ecology and 
Subjective Cognition. Frontiers in Ecology and Evolution. 
2019;7: 164. 
45. 
Ratcliffe JM, Phelps SM. Twenty-five years of cognitive ecology. 
Anim Behav. 2019;147: 127–128. 
46. 
Power DA, Watson RA, Szathmáry E, Mills R, Powers ST, 
Doncaster CP, et al. What can ecosystems learn? Expanding 
evolutionary ecology with learning theory. Biol Direct. 2015;10: 
69. 
47. 
Sharov AA. Evolutionary biosemiotics and multilevel 
construction networks. Biosemiotics. 2016;9: 399–416.

## Page 64

Digital Rhetorical Ecosystem Analysis, 2021 
 
62 
48. 
Gilbert SF. Ecological Developmental Biology: Interpreting 
Developmental Signs. Biosemiotics. 2016;9: 51–60. 
49. 
Ruhl JB. Governing Cascade Failures in Complex Social-
Ecological-Technological Systems: Framing Context, Strategies, 
and Challenges. 2019. Available: 
https://papers.ssrn.com/abstract=3471945 
50. 
Cordes RJ, Friedman DA. Emergent Teams for Complex Threats. 
The Great Preset: Remote Teams and Operational Art. COGSEC; 
2020. 
51. 
Zhao B. Why Processing is Not Swarm Intelligence. Proceedings 
of the 2019 DigitalFUTURES. Springer Singapore; 2020. pp. 
257–264. 
52. 
Xing X, Rongpeng L, Zhifeng Z, Honggang Z. Stigmergic 
Independent Reinforcement Learning for Multi-Agent 
Collaboration. arXiv preprint arXiv. 2019. Available: 
https://arxiv.org/abs/1911.12504 
53. 
Finn KR, Silk MJ, Porter MA, Pinter-Wollman N. The use of 
multilayer network analysis in animal behaviour. Anim Behav. 
2019;149: 7–22. 
54. 
cadCAD – A Python package for designing, testing and 
validating complex systems through simulation. [cited 26 Mar 
2020]. Available: https://cadcad.org/ 
55. 
Bradbury JW, Vehrencamp SL. Complexity and behavioral 
ecology. Behav Ecol. 2014. Available: 
https://academic.oup.com/beheco/article-
abstract/25/3/435/510920 
56. 
Leonhardt SD, Menzel F, Nehring V, Schmitt T. Ecology and 
Evolution of Communication in Social Insects. Cell. 2016;164: 
1277–1287. 
57. 
Gordon DM. Measuring collective behavior: an ecological 
approach. Theory Biosci. 2019. doi:10.1007/s12064-019-00302-5 
58. 
Chambers JC, Allen CR, Cushman SA. Operationalizing 
Ecological Resilience Concepts for Managing Species and 
Ecosystems at Risk. Frontiers in Ecology and Evolution. 2019;7: 
241. 
59. 
Clua E, Beliaeff B, Chauvet C, David G, Ferraris J, Kronen M, et 
al. Towards multidisciplinary indicator dashboards for coral reef 
fisheries management. Aquat Living Resour. 2005;18: 199 –213. 
60. 
O’Brien A, Townsend K, Hale R, Sharley D, Pettigrove V. How 
is ecosystem health defined and measured? A critical review of 
freshwater and estuarine studies. Ecol Indic. 2016;69: 722–729.

## Page 65

Digital Rhetorical Ecosystem Analysis, 2021 
 
63 
61. 
Jørgensen S, Xu L, Costanza R. Handbook of Ecological 
Indicators for Assessment of Ecosystem Health. CRC Press; 
2016. 
62. 
De Garine-Wichatitsky M, Binot A, Ward J, Caron A, Perrotton 
A, Ross H, et al. “Health in” and “Health of” Social-Ecological 
Systems: A Practical Framework for the Management of Healthy 
and Resilient Agricultural and Natural Ecosystems. Front Public 
Health. 2020;8: 616328. 
63. 
Reporting Bird Sightings. 25 Sep 2015 [cited 13 May 2021]. 
Available: https://ny.audubon.org/about-us/reporting-bird-
sightings 
64. 
National Geographic Society. BioBlitz Program. [cited 7 Oct 
2021]. Available: 
https://www.nationalgeographic.org/projects/bioblitz/  
65. 
Hood N, Littlejohn A. Hacking history: Redressing gender 
inequities on Wikipedia through an editathon. Int Rev Res Open 
Distrib Learn. 2018;19. doi:10.19173/irrodl.v19i5.3549  
66. 
March L, Dasgupta S. Wikipedia Edit-a-thons as Sites of Public 
Pedagogy. Proc ACM Hum-Comput Interact. 2020;4: 1–26. 
67. 
Zamora ME, Espinosa M, Gershenson C, López-Corona O, 
Munguia M, Pérez-Maqueo O, et al. Ecosystem antifragility: 
Beyond integrity and resilience. PeerJ PrePrints. 2019.  
68. 
Falk DA, Watts AC, Thode AE. Scaling Ecological Resilience. 
Frontiers in Ecology and Evolution. 2019;7: 275.  
69. 
Asllani M, Lambiotte R, Carletti T. Structure and dynamical 
behavior of non-normal networks. Sci Adv. 2018;4: eaau9403. 
70. 
Bruder A, Frainer A, Rota T, Primicerio R. The Importance of 
Ecological Networks in Multiple-Stressor Research and 
Management. Front Environ Sci Eng China. 2019;7: 59. 
71. 
Marshall JAR. Generalizations of Hamilton’s rule applied to non -
additive public goods games with random group size. Frontiers 
in Ecology and Evolution. 2014;2: 40. 
72. 
Pangallo M, Heinrich T, Doyne Farmer J. Best reply structure 
and equilibrium convergence in generic games. Sci Adv. 2019;5: 
eaat1328. 
73. 
Fisher B, Turner RK, Morling P. Defining and classifying 
ecosystem services for decision making. Ecol Econ. 2009;68: 
643–653.

## Page 66

Digital Rhetorical Ecosystem Analysis, 2021 
 
64 
74. 
Gravel D, Guichard F, Loreau M, Mouquet N. Source and sink 
dynamics in meta-ecosystems. Ecology. 2010. pp. 2172–2184. 
doi:10.1890/09-0843.1 
75. 
Sievanen L. How do small-scale fishers adapt to environmental 
variability? Lessons from Baja California, Sur, Mexico. Marit 
Stud. 2014;13: 9. 
76. 
Brown ED, Williams BK. Resilience and Resource Management. 
Environ Manage. 2015;56: 1416–1427. 
77. 
Tosa MI, Dziedzic EH, Appel CL, Urbina J, Massey A, Ruprecht 
J, et al. The Rapid Rise of Next-Generation Natural History. 
Frontiers in Ecology and Evolution. 2021;9: 480.  
78. 
Newell E, Jurgens D, Saleem HM, Vala H, Sassine J, Armstrong 
C, et al. User Migration in Online Social Networks: A Case Study 
on Reddit During a Period of Community Unrest. Tenth 
International AAAI Conference on Web and Social Media. 2016. 
Available: 
https://www.aaai.org/ocs/index.php/ICWSM/ICWSM16/paper/
viewPaper/13137 
79. 
Leurs K, Prabhakar M. Doing digital migration studies: 
Methodological considerations for an emerging research focus. 
Qualitative research in European migration studies. Springer, 
Cham; 2018. pp. 247–266. 
80. 
Buhs JB. The Fire Ant Wars: Nature, Science, and Public Policy 
in Twentieth-Century America. University of Chicago Press; 
2004. 
81. 
Cordes RJ, David S, Maan A, Ruiz A, Sapp E, Scannell P, et al. 
The Narrative Campaign Field Guide - First Edition. 1st ed. 
Cordes RJ, editor. Narrative Strategies Ink; 2021. 
82. 
Shine R. The ecological impact of invasive cane toads (Bufo 
marinus) in Australia. Q Rev Biol. 2010;85: 253–291. 
83. 
Roman A, Dasgupta D, Pleimling M. A theoretical approach to 
understand spatial organization in complex ecologies. J Theor 
Biol. 2016;403: 10–16. 
84. 
Jones ME, Apfelbach R, Banks PB, Cameron EZ, Dickman CR, 
Frank A, et al. A Nose for Death: Integrating Trophic and 
Informational Networks for Conservation and Management. 
Frontiers in Ecology and Evolution. 2016;4: 124. 
85. 
LaFrance A. The Internet Is Mostly Bots. The Atlantic. 31 Jan 
2017. Available: 
https://www.theatlantic.com/technology/archive/2017/01/bots
-bots-bots/515043/. Accessed 11 Aug 2021.

## Page 67

Digital Rhetorical Ecosystem Analysis, 2021 
 
65 
86. 
Zeifman I, McKeever G, Hewitt N, Hasson E. Bot Traffic 
Report 2016. Imperva; 31 Mar 2021 [cited 11 May 2021]. 
Available: https://www.imperva.com/blog/bot-traffic-report-
2016/?redirect=Incapsula 
87. 
Vyatkin A, Metelkin I, Mikhailova A, Cordes RJ, Friedman DA. 
Active Inference and Behavior Engineering for Teams. In: 
Friedman DA, Cordes RJ, editors. The Great Preset: Remote 
Teams and Operational Art. COGSEC; 2020. 
88. 
Mitterhofer S, Kruegel C, Kirda E, Platzer C. Server-Side Bot 
Detection in Massively Multiplayer Online Games. IEEE 
Security Privacy. 2009;7: 29–36. 
89. 
Rheault L, Musulan A. Efficient detection of online communities 
and social bot activity during electoral campaigns. Journal of 
Information Technology & Politics. 2021;18: 324–337. 
90. 
Rosenberg KV, Dokter AM, Blancher PJ, Sauer JR, Smith AC, 
Smith PA, et al. Decline of the North American avifauna. 
Science. 2019; eaaw1313. 
91. 
Lafuite A-S, de Mazancourt C, Loreau M. Delayed behavioural 
shifts undermine the sustainability of social-ecological systems. 
Proc Biol Sci. 2017;284: 20171192. 
92. 
Grasso F. Towards Computational Rhetoric. IL. 2002;22. 
doi:10.22329/il.v22i3.2589 
93. 
Wojcik MW. Thesis: Inventing computational rhetoric. 
search.proquest.com. 2013. Available: 
https://search.proquest.com/openview/594bb5e36be4a69803db5
ef14dc7f830/1?pq-origsite=gscholar&cbl=18750 
94. 
Walsh L, Boyle C. Topologies as Techniques for a Post-Critical 
Rhetoric. Walsh L, Boyle C, editors. Palgrave Macmillan, Cham; 
2017. 
95. 
Cordes RJ. Games with serious impacts: The next generation of 
serious games - Atlantic Council. In: atlanticcouncil.org 
[Internet]. 21 May 2021 [cited 3 Jun 2021]. Available: 
https://www.atlanticcouncil.org/blogs/geotech-cues/games-
with-serious-impacts-the-next-generation/ 
96. 
preferred reading. [cited 17 Sep 2021]. 
doi:10.1093/oi/authority.20110803100342875 
97. 
Dietze MC, Fox A, Beck-Johnson LM, Betancourt JL, Hooten 
MB, Jarnevich CS, et al. Iterative near-term ecological 
forecasting: Needs, opportunities, and challenges. Proc Natl 
Acad Sci U S A. 2018;115: 1424–1432.

## Page 68

Digital Rhetorical Ecosystem Analysis, 2021 
 
66 
98. 
Cordes RJ, David S, Maan A, Ruiz A, Sapp E, Scannell P, et al. 
The Narrative Campaign Field Guide. 1st ed. Cordes RJ, editor. 
Narrative Strategies Ink; 2021. 
99. 
Bradshaw S, Howard PN. The Global Disinformation Order: 
2019 Global Inventory of Organised Social Media Manipulation. 
Project on Computational Propaganda; 2019. 
100. 
Union of Concerned Scientists. The Disinformation Playbook. 
In: UCSUSA.org [Internet]. oct 10 2017 [cited 8 Jan 2021]. 
Available: https://www.ucsusa.org/resources/disinformation -
playbook 
101. 
DisinfoCloud. Disinfo Cloud. In: disinfocloud.com [Internet]. 22 
Apr 2021 [cited 23 Apr 2021]. Available: 
https://disinfocloud.com/ 
102. 
Military Intelligence Professional Bulletin - Collection 
Management. {US Army Intelligence Center of Excellence}; 
2020. 
103. 
Varga S, Brynielsson J, Horndahl A, Rosell M. Automated Text 
Analysis for Intelligence Purposes: A Psychological Operations 
Case Study. In: Tayebi MA, Glässer U, Skillicorn DB, editors. 
Open Source Intelligence and Cyber Crime: Social Media 
Analytics. Cham: Springer International Publishing; 2020. pp. 
221–251. 
104. 
Christianson C, Duncan J, Onyshkevych B. Overview of the 
DARPA LORELEI Program. Machine Translation. 2018;32: 3 –9. 
105. 
Naderpour M, Lu J, Zhang G. A fuzzy dynamic bayesian 
network-based situation assessment approach. 2013 IEEE 
International Conference on Fuzzy Systems (FUZZ-IEEE). 
ieeexplore.ieee.org; 2013. pp. 1–8. 
106. 
Winklerova Z. Ontological approach to the representation of 
military knowledge. MILITARY ACADEMY IN BRNO (CZECH 
REPUBLIC) COMMAND AND STAFF FACULTY; 2004 Mar. 
Available: https://apps.dtic.mil/sti/citations/ADA428705 
107. 
Davis Z, Gac F, Rager C, Reiner P, Snow J, editors. Strategic 
Latency Unleashed: The Role of Technology in a Revisionist 
Global Order and the Implications for Special Operations 
Forces. Center for Global Security Research; 2021. 
108. 
Rosen MA, Fiore SM, Salas E, Letsky M, Warner N. Tightly 
coupling cognition: understanding how communication and 
awareness drive coordination in teams. C2 Journal. 2008;2. 
Available: https://apps.dtic.mil/sti/citations/ADA513557  
109. 
Letsky M, Warner N, Fiore SM, Rosen M, Salas E, OFFICE OF 
NAVAL RESEARCH ARLINGTON VA. Macrocognition in

## Page 69

Digital Rhetorical Ecosystem Analysis, 2021 
 
67 
Complex Team Problem Solving. OFFICE OF NAVAL 
RESEARCH ARLINGTON VA; 2007 Jun. Available: 
https://apps.dtic.mil/sti/citations/ADA481422 
110. 
Alberts JK, Tracy SJ, Trethewey A. An Integrative Theory of the 
Division of Domestic Labor: Threshold Level, Social Organizing 
and Sensemaking. J Fam Commun. 2011;11: 21–38. 
111. 
Goertzel B. The Hidden Pattern: A Patternist Philosophy of 
Mind. Universal-Publishers; 2006. 
112. 
Bach J. Principles of Synthetic Intelligence PSI: An Architecture 
of Motivated Cognition. Oxford University Press, USA; 2009.  
113. 
Bose R. Competitive intelligence process and tools for 
intelligence analysis. Industrial Management & Data Systems. 
2008;108: 510–528. 
114. 
Kent S. Strategic Intelligence for American World Policy. 
Princeton University Press; 1949. 
115. 
Treverton GF, Jones SG, Boraz S, Lipscy P, RAND CORP. 
Toward a theory of intelligence. Workshop report. RAND CORP 
ARLINGTON VA NATIONAL SECURITY RESEARCH DIV; 
2006 Jan. Available: 
https://apps.dtic.mil/sti/citations/ADA449313 
116. 
Kramer RM. A Failure to Communicate: 9/11 and the Tragedy of 
the Informational Commons. International Public Management 
Journal. 2005;8: 397–416. 
117. 
Linn BM. The Echo of Battle. Harvard University Press; 2009.  
118. 
Austin NJE, Rankov NB. Exploratio: Military and Political 
Intelligence in the Roman World from the Second Punic War to 
the Battle of Adrianople. Psychology Press; 1998. 
119. 
Dedijer S. Ragusa Intelligence and Security (1301-1806): A 
Model for the Twenty-First Century? Int J Intell 
CounterIntelligence. 2002;15: 101–114. 
120. 
Šundrica Z. The Intelligence Activities of the Dubrovnik 
Republic in the Austro-Turkish War 1737-1739. Dubrovnik 
Annals; 2001. Report No.: 8299. Available: 
https://hrcak.srce.hr/index.php?id_clanak=8299&show=clanak 
121. 
Sweeney WC. Military Intelligence, a New Weapon in War. 
Frederick A. Stokes Company; 1924. 
122. 
Moore DT. Sensemaking: A Structure for an Intelligence 
Revolution. Center for Strategic Intelligence Research, National 
Defense Intelligence College; 2011.

## Page 70

Digital Rhetorical Ecosystem Analysis, 2021 
 
68 
123. 
Walsh PF. Intelligence and intelligence analysis: Exploring the 
state of intelligence since 9/11. Crehan AC, editor. Charles Sturt 
University. 2013. Available: 
https://researchoutput.csu.edu.au/en/publications/intelligence -
and-intelligence-analysis-exploring-the-state-of-int 
124. 
Waltz E. Knowledge Management in the Intelligence Enterprise. 
Artech House; 2003. 
125. 
Hribar G, Podbregar I, Ivanuša T. OSINT: A “Grey Zone”? Int J 
Intell CounterIntelligence. 2014;27: 529–549. 
126. 
Bennett M, Waltz E. Counterdeception principles and 
applications for national security. Artech House; 2007.  
127. 
Kambere G, Goh PH, Kumar P, Msafir F. The Financing of 
Lashkar-e-Taiba. Combating Terrorism Exchange. 2011;1: 18. 
128. 
Glanz J, Rotella S, Sanger DE. In 2008 Mumbai attacks, piles of 
spy data, but an uncompleted puzzle. In: New York Times 
[Internet]. 2014. Available: 
http://www.nytimes.com/2014/12/22/world/asia/in-2008-
mumbai-attacks-piles-of-spy-data-but-an-uncompleted-
puzzle.html 
129. 
Jackson BA. Groups, Networks, or Movements: A Command-
and-Control-Driven Approach to Classifying Terrorist 
Organizations and Its Application to Al Qaeda. Stud Conflict 
Terrorism. 2006;29: 241–262. 
130. 
Phythian M. Beyond the Intelligence Cycle? In: Phythian  M, 
editor. Understanding the Intelligence Cycle. Routledge; 2013.  
131. 
Gill P, Phythian M. From Intelligence Cycle to Web of 
Intelligence: Complexity and the conceptualisation of 
intelligence. In: Phythian M, editor. Understanding the 
Intelligence Cycle. Routledge; 2013. 
132. 
Herman M. Intelligence Power in Peace and War. Cambridge 
University Press; 1996. 
133. 
Johnson LK. Strategic intelligence: An American perspective. Int 
J Intell CounterIntelligence. 1989;3: 299–332. 
134. 
Warner M. The Past and Future of the Intelligence Cycle. In: 
Phythian M, editor. Understanding the Intelligence Cycle. 
Routledge; 2013. 
135. 
Hulnick AS. Intelligence Theory: Seeking better models. In: 
Phythian M, editor. Understanding the Intelligence Cycle. 
Routledge; 2013.

## Page 71

Digital Rhetorical Ecosystem Analysis, 2021 
 
69 
136. 
Lakoff G, Johnson M. Metaphors we live by. University Of 
Chicago Press; 1980. 
137. 
McCreadie R, Macdonald C, Ounis I, Osborne M, Petrovic S. 
Scalable distributed event detection for Twitter. 2013 IEEE 
International Conference on Big Data. ieeexplore.ieee.org; 2013. 
pp. 543–549. 
138. 
Morstatter F, Pfeffer J, Liu H, Carley KM. Is the sample good 
enough? comparing data from twitter’s streaming api with 
twitter's firehose. Seventh international AAAI conference on 
weblogs and social media. aaai.org; 2013. Available: 
https://www.aaai.org/ocs/index.php/ICWSM/ICWSM13/paper/
viewPaper/6071 
139. 
Office of the Director of National Intelligence. U.S. National 
Intelligence: An Overview. 2011. 
140. 
Margolis JE. Estimating state instability. Studies in Intelligence. 
2012;56: 13–24. 
141. 
Peppler B. Dealing with the longer-term in intelligence practice: 
The application of a foresight approach. Journal of the 
Australian Institute of Professional Intelligence Officers. 
2014;22: 35–51. 
142. 
Stack KP. Competitive intelligence. Intell Natl Sec. 1998;13: 
194–202. 
143. 
Friedman JA, Zeckhauser R. Assessing Uncertainty in 
Intelligence. Intell Natl Sec. 2012;27: 824–847. 
144. 
Wirtz JJ. Indications and Warning in an Age of Uncertainty. Int J 
Intell CounterIntelligence. 2013;26: 550–562. 
145. 
Gentry JA, Gordon JS. Strategic Warning Intelligence: History, 
Challenges, and Prospects. Georgetown University Press; 2019. 
146. 
Goldman J. “Actionable” Intelligence Is Not “Warning” 
Intelligence. Proceedings of the XIXth International Conference. 
iksconference.ro; 2014. Available: https://iksconference.ro/wp -
content/uploads/2017/04/IKS_2014.pdf#page=21 
147. 
Hulnick AS. What’s wrong with the Intelligence Cycle. Intell 
Natl Sec. 2006;21: 959–979. 
148. 
Johnson LK. Making the intelligence “Cycle” work. Int J Intell 
CounterIntelligence. 1986;1: 1–23. 
149. 
Fournie DA. Harsh Lessons: Roman Intelligence in the 
Hannibalic War. Int J Intell CounterIntelligence. 2004;17: 502 –
538.

## Page 72

Digital Rhetorical Ecosystem Analysis, 2021 
 
70 
150. 
Johnson LK. Preface to a Theory of Strategic Intelligence. Int J 
Intell CounterIntelligence. 2003;16: 638–663. 
151. 
Lukyanenko R, Parsons J, Wiersma Y, Wachinger G, Huber B, 
Meldt R. Representing Crowd Knowledge: Guidelines for 
Conceptual Modeling of User-generated Content. Journal of the 
Association for Information Systems. 2017;18: 2. 
152. 
Eidson M, Kramer L, Stone W, Hagiwara Y, Schmit K, New York 
State West Nile Virus Avian Surveillance Team. Dead bird 
surveillance as an early warning system for West Nile virus. 
Emerg Infect Dis. 2001;7: 631–635. 
153. 
Lukyanenko R, Parsons J, Wiersma Y. Citizen Science 2.0: Data 
Management Principles to Harness the Power of the Crowd. 
Service-Oriented Perspectives in Design Science Research. 
Springer Berlin Heidelberg; 2011. pp. 465–473. 
154. 
Lukyanenko R, Parsons J, Wiersma YF. The IQ of the Crowd: 
Understanding and Improving Information Quality in Structured 
User-Generated Content. Information Systems Research. 
2014;25: 669–689. 
155. 
He J, van Ossenbruggen J, de Vries AP. Fish4label: 
accomplishing an expert task without expert knowledge. 
Proceedings of the 10th Conference on Open Research Areas in 
Information Retrieval. groups.inf.ed.ac.uk; 2013. pp. 211 –212. 
156. 
Chasmer LE, Ryerson RA, Coburn CA. Educating the Next 
Generation of Remote Sensing Specialists: Skills and Industry 
Needs in a Changing World. Can J Remote Sens. 2021; 1–16. 
157. 
Ekins E. Poll: 62% of Americans Say They Have Political Views 
They’re Afraid to Share. In: cato.org [Internet]. 22 Jul 2020 
[cited 27 Jul 2021]. Available: https://www.cato.org/survey -
reports/poll-62-americans-say-they-have-political-views-theyre-
afraid-share?queryID=98d4c30397de4e786f8625a2b87a2380  
158. 
Musto J. School principal sues over dismissal for sharing 
conservative memes on Facebook. In: foxnews.com [Internet]. 9 
Dec 2020 [cited 27 Jul 2021]. Available: 
https://www.foxnews.com/us/school-principal-sues-after-being-
fired-for-sharing-conservative-memes 
159. 
Reuters. Disney’s Lucasfilm ditches “The Mandalorian” star Gina 
Carano over social media posts. Reuters. 11 Feb 2021. Available: 
https://www.reuters.com/article/us-walt-disney-lucasfilm-
carano-idUSKBN2AB0PL. Accessed 27 Jul 2021. 
160. 
Zuckerman E. Mistrust, efficacy and the new civics: 
understanding the deep roots of the crisis of faith in journalism.

## Page 73

Digital Rhetorical Ecosystem Analysis, 2021 
 
71 
2017 [cited 27 Jul 2021]. Available: 
https://dspace.mit.edu/handle/1721.1/110987?show=full  
161. 
Alexander S. NYT Is Threatening My Safety By Revealing My 
Real Name, So I Am Deleting The Blog. In: slatestarcodex.com 
[Internet]. 23 Jun 2020 [cited 27 Jul 2021]. Available: 
https://slatestarcodex.com/2020/06/22/nyt-is-threatening-my-
safety-by-revealing-my-real-name-so-i-am-deleting-the-blog/ 
162. 
Middlebrook C. The Grey Area: Instagram, Shadowbanning, and 
the Erasure of Marginalized Communities. Shadowbanning, and 
the Erasure of Marginalized. 2020. doi:10.2139/ssrn.3539721  
163. 
Le Merrer E, Morgan B, Trédan G. Setting the Record Straighter 
on Shadow Banning. arXiv [cs.SI]. 2020. Available: 
http://arxiv.org/abs/2012.05101 
164. 
Jaidka K, Mukerjee S, Lelkes Y. An audit of Twitter’s shadowban 
sanctions in the United States. yahootechpulse.easychair.org; 
2021 [cited 27 Jul 2021]. Available: 
https://yahootechpulse.easychair.org/publications/preprint_dow
nload/z4jt 
165. 
Chambers S. The amazing banned memes from China. In: Index 
on Censorship [Internet]. 1 Mar 2018 [cited 27 Jul 2021]. 
Available: 
https://www.indexoncensorship.org/2018/03/amazing-banned-
memes-china/ 
166. 
Zadrozny B. Twitter troll arrested, accused of election 
interference related to disinformation campaign. In: NBC News 
[Internet]. 27 Jan 2021 [cited 27 Jul 2021]. Available: 
https://www.nbcnews.com/tech/internet/twitter-troll-arrested-
election-interference-related-disinformation-campaign-n1255864 
167. 
Allen-Ebrahimian B. University of Minnesota student jailed in 
China for tweets critical of government. 23 Jan 2020 [cited 27 
Jul 2021]. Available: https://www.axios.com/china-arrests-
university-minnesota-twitter-e495cf47-d895-4014-9ac8-
8dc76aa6004d.html 
168. 
U.S. Army. Open-Source Intelligence ATP 2-22.9. 2012. 
169. 
Tufte ER. Visual Explanations: Images and Quantities, Evidence 
and Narrative. Computers in Physics. 1998;12. 
doi:10.1063/1.168637 
170. 
Cordes RJ, Friedman DA. The Facilitator’s Catechism. In: 
Friedman DA, Cordes RJ, editors. The Great Preset: Remote 
Teams and Operational Art. COGSEC; 2020. 
171. 
Lippi M, Torroni P. Context-Independent Claim Detection for 
Argument Mining. Twenty-Fourth International Joint Conference

## Page 74

Digital Rhetorical Ecosystem Analysis, 2021 
 
72 
on Artificial Intelligence. aaai.org; 2015. Available: 
https://www.aaai.org/ocs/index.php/IJCAI/IJCAI15/paper/vie
wPaper/10942 
172. 
Lawrence J, Reed C. Argument mining: A survey. Comput 
Linguist. 2020. Available: https://direct.mit.edu/coli/article -
abstract/45/4/765/93362 
173. 
Lippi M, Torroni P. Argument mining: A machine learning 
perspective. International Workshop on Theory and Applications 
of. 2015. Available: 
https://link.springer.com/chapter/10.1007/978-3-319-28460-
6_10 
174. 
Peterson C, Rauschnot M, Mc Clain T. Shark alert: Early warning 
system. digitalcommons.calpoly.edu; 2015 [cited 27 Aug 2021]. 
Available: 
http://digitalcommons.calpoly.edu/cgi/viewcontent.cgi?article=
1341&context=eesp 
175. 
Brownstein JS, Freifeld CC. HealthMap: the development of 
automated real-time internet surveillance for epidemic 
intelligence. Euro Surveill. 2007;12: E071129.5.  
176. 
Daneels A, Salter W. What is SCADA? 1999. Available: 
https://accelconf.web.cern.ch/ica99/papers/mc1i01.pdf  
177. 
Yu X, Wu P, Han W, Zhang Z, Others. A remote SCADA system 
for keeping fruits and vegetables fresh with ozone. Int J Food 
Agric Environ. 2013;11: 187–192. 
178. 
Jiang J, Wang P, Nan J, Guo L, Ran M, Others. Songhua River 
monitoring system on point sources and water quality with 
SCADA and GIS. Environ Sci Technol. 2013;36: 132–136. 
179. 
Cannon P. Taking an “Ecological Turn” in the Evaluation of 
Rhetorical Interventions. University of South Florida. 2019. 
Available: https://scholarcommons.usf.edu/etd/8010  
180. 
Godwin M. Meme, Counter-meme. Wired. 1 Oct 1994. Available: 
https://www.wired.com/1994/10/godwin-if-2/. Accessed 12 
Aug 2021. 
181. 
Projet Debater - IBM Research AI. [cited 17 Sep 2021]. 
Available: https://www.research.ibm.com/interactive/project -
debater/ 
182. 
Swarmcheck.ai. Swarmcheck. In: swarmcheck.ai [Internet]. 2021 
[cited 17 Sep 2021]. Available: 
https://www.swarmcheck.ai/home 
183. 
Perelman C, Olbrechts-Tyteca L. The New Rhetoric: A Treatise 
on Argumentation. University of Notre Dame Press; 1971.

## Page 75

Digital Rhetorical Ecosystem Analysis, 2021 
 
73 
184. 
Wikipedia contributors. Land ethic. In: Wikipedia, The Free 
Encyclopedia [Internet]. 11 Dec 2020 [cited 26 Mar 2021]. 
Available: 
https://en.wikipedia.org/w/index.php?title=Land_ethic&oldid=
993635012 
185. 
Ostrom E. Governing the Commons: The Evolution of 
Institutions for Collective Action. Cambridge University Press; 
1990. 
186. 
Boik JC. Science-Driven Societal Transformation, Part I: 
Worldview. Sustain Sci Pract Policy. 2020;12: 6881. 
187. 
Frey S, Schneider N. Effective Voice: Beyond Exit and Affect in 
Online Communities. arXiv [cs.CY]. 2020. Available: 
http://arxiv.org/abs/2009.12470 
188. 
Schneider N, De Filippi P, Frey S, Tan JZ, Zhang AX. Modular 
Politics: Toward a Governance Layer for Online Communities. 
Proc ACM Hum-Comput Interact. 2021;5: 1–26. 
189. 
Jhaver S, Frey S, Zhang A. Designing for Multiple Centers of 
Power: A Taxonomy of Multi-level Governance in Online Social 
Platforms. arXiv [cs.HC]. 2021. Available: 
http://arxiv.org/abs/2108.12529


---
*Extraction method: pymupdf*
