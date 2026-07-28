# Full Text: Reimagining Maps

> Extracted from `Reimagining Maps.pdf`

> 4 figures extracted to `images/`

---

## Page 1

Concept White Paper 
 
 
 
 
 
Reimagining Maps 
 
 
 
 
 
 
 
 
 
 
  
 
RJ Cordes1,2,3, DA Friedman1,2,4, M Maron5 
DanielAriFriedman@gmail.com, RichardJ.Cordes@gmail.com, Mikel@Mapbox.com 
Oct 31st, 2020 
 National Geospatial-Intelligence Polyplexus Incubator: Reimagining Maps 
1. 
COGSEC  
2. 
Remotor Consulting Group 
3. 
Atlantic Council GeoTech Center 
4. 
University of California, Davis, Department of Entomology & Nematology 
5. 
Mapbox

## Page 2

Reimagining Maps 
 
 
 
Driving and Inspiring Questions................................................................................... 1 
Introduction ........................................................................................................................ 2 
Part I Current State of Geospatial Maps .................................................................... 4 
Interoperability ..................................................................................................................... 5 
Skill Gaps ............................................................................................................................. 6 
User Awareness .................................................................................................................... 7 
Mapping Uncertainty ............................................................................................................. 7 
Threat Actors ........................................................................................................................ 8 
Volume of Data ..................................................................................................................... 8 
Accessibility ......................................................................................................................... 9 
Key Challenge Areas ........................................................................................................... 10 
Rapid Generation of Relevant Maps .................................................................................. 10 
Informational Compression  and User Experience .............................................................. 11 
Security, Governance, and Trust  of Maps and Data ........................................................... 12 
Part II Maps in other Fields ......................................................................................... 13 
Process Mapping ................................................................................................................ 13 
Software and Software Development..................................................................................... 14 
Complex Systems ............................................................................................................... 15 
Communications ................................................................................................................. 15 
Knowledge Management and Information Systems ................................................................ 17 
Education, Curriculum, and Learning ................................................................................... 19 
Ecology and Biology ........................................................................................................... 20 
Mathematics ....................................................................................................................... 21 
Part III “Reimagining Maps” ........................................................................................ 23 
The Map is Not the Territory ................................................................................................ 23 
Contents

## Page 3

Reimagining Maps 
User/Role/Actor-Centric and Mission-Aware Maps ................................................................ 24 
BOLTS ............................................................................................................................... 25 
Fuzzy and Incomplete Data .................................................................................................. 26 
Case study for Future Maps .................................................................................................... 27 
Conclusion ............................................................................................................................. 30 
Acknowledgements ................................................................................................................. 31 
Works Cited ........................................................................................................................... 31

## Page 4

Reimagining Maps 
 
 
1 
 
 
 
 
Reimagining Maps was written in response to the National Geospatial-Intelligence 
Incubator of the same name hosted on the platform Polyplexus and was done so with 
the intent of discussing the questions outlined below. 
Driving and Inspiring Questions 
▪ Can emerging knowledge in mathematics, perception, design, and other 
related disciplines help us make better, more flexible, more understandable 
maps and governance? What is possible now or soon that was not possible 
before?  
▪ What if we suddenly found ourselves forced to explain where things are or 
how to get from A to B without historic maps? How would advances in abstract 
mathematics, psychology, cognitive neuroscience, art, augmented reality, and 
other technologies and disciplines be used to inspire cartography if it were a 
new field?  
▪ Can map systems accommodate various users and facilitate modern action 
affordances? 
▪ Can maps be dynamically customized using emerging knowledge in 
mathematics, perception, design, and other related disciplines?  
▪ Can best practices in computer science fuse with insights from 
phenomenology and ecological psychology to make human-computer 
interactions healthy and meaningful?  
▪ Can governance of datasets and map generators be transparent, effective, and 
secure?  
▪ Can responses to disasters be rapid, contextual, and human-in-the-loop?  
▪ What is possible now or soon due to changes in the use and availability of 
geospatial hardware and software technologies? 
 
Reimagining Maps

## Page 5

Reimagining Maps 
 
 
2 
 
Introduction 
The field of cartography sits at the intersection of applied mathematics, engineering, 
geology, geography, user experience, and graphic design. Methodologies and 
concepts from cartography have been creatively applied in a variety of fields, such as 
the application of spatial mapping techniques to information in knowledge 
management, or the use of itinerary visualization methods in non-spatial journeys 
such as learning maps in learning management systems. These fields have been 
subjected to their own forms of development and evolution leading to new 
methodologies and concepts somewhat removed from their origins [1]. Cartography 
itself has undergone a great deal of technology-driven development [2] but would 
look very different today had it been developed as a new field through the creative 
application of methodologies and concepts from those it inspired. As the modern 
information and logistical context presents new challenges and thus new demands 
for maps, we propose a “reimagining of maps” through an interdisciplinary synthesis 
inspired by the interdisciplinary origins of maps themselves. 
While geospatial mapping has traditionally fallen solely within the scope of 
cartography, this relationship is subject to a number of common misunderstandings. 
The most general of these misunderstandings may be the assumption that 
cartography is a field which is solely concerned with the preparation of geospatial 
maps. Modern cartography is indeed concerned with geospatial representation but 
the origins of the practice are primarily found in the production of maps that were 
non-geographic, such as maps of the stars, maps that informed cultural and religious 
practice, and maps that stressed relationship and categorization over precision in 
spatial representation [3–5]. Further, there is a misunderstanding that, historically, 
maps were in regular use for navigational purposes in transit, which was rarely the 
case [1,6]. In actuality, medieval and ancient maps were considered “precious” 
artifacts [5] often used for archival purposes and interdisciplinary (military, 
geopolitical, scientific, and commercial) reference but most parties traveled by 
itineraries that were informed by maps or by those with knowledge of them [1,6]. 
Histories of cartography indicate reasonable efforts taken by their authors to ensure 
clarity when discussing the subject, regularly using terms like “geographical”, 
“maritime”, and “terrestrial” [7,8] to indicate what kind of map is being spoken about, 
as each came with its own quirks and utility [1,7–9]. The objectives of spatial mapping 
are not always about explicit representations of territory, instead, the contemporary

## Page 6

Reimagining Maps 
 
 
3 
 
and historical focus is often more aligned with the connection of data to the missions 
and needs of other disciplines, in order to accomplish goals through primarily static, 
graphic representations of space and time. 
In this paper we define the key dimensions of the Geospatial Problem Space 
before drawing associations between the traditional foci of cartography (the 
production of maps and archival sets) and fields such as abstract mathematics, 
complexity science, and information governance. The objectives of this paper are to 
first consider the key dimensions of the Geospatial Problem Space and the limitations 
of the field of cartography in its current state and at its cutting edge, and then to 
consider the objectives, strengths, and limitations of diverse fields adjacent to 
cartography such as applied mathematics, engineering, and digital pedagogy. These 
adjacent fields are intended to serve as a basis for exploration of the potential future 
of cartography. Finally, direction is provided for future research activities, specifically 
concerning the development of integrative frameworks for geospatial intelligence 
production and user experiences involving: 
• Rapid generation and customization of user-aware maps 
• Signal processing techniques 
• Role-based access systems for collaborative production of artifacts 
• Open Source Intelligence (OSINT) 
• Next Generation Analytics 
• Artificial Intelligence (AI) in the Loop with Humans & Humans in the Loop 
with AI 
• Action-oriented usage of geospatial artifacts

## Page 7

Reimagining Maps 
 
 
4 
 
Part I 
Current State of Geospatial Maps 
Recent changes in medium, mobility, data availability, and infrastructure have greatly 
impacted the field of cartography. These technological evolutions have accordingly 
changed the strengths, limitations and objectives of maps, reflected by developments 
in the affordances that cartographers are able offer to users through their map 
products. Here, we consider the strengths, limitations, and objectives of modern 
Cartography in the context of ongoing technological changes, before exploring areas 
of non-geospatial mapping to understand where insights for geospatial maps may be 
gleaned. First, we reflect on the current state of maps, with focus on ecological, 
social, and COVID-19-related use cases and challenges of 2020 (Figure 1). 
Figure 1. Use cases for maps in 2020. A) Fire map image from [10] . B) COVID-19 case map from [11] 
(10/20/2020). C) Marine conservation maps From Figure 2 of [12]. D) Map of protests around the United 
States from [13], last updated June 16th, 2020.

![page7_img1.jpeg](images/page7_img1.jpeg)

## Page 8

Reimagining Maps 
 
 
5 
 
Interoperability 
The availability of spatial data online is increasing rapidly, largely through catalogs 
or standalone APIs. These data catalogs fit into traditional map production workflows: 
beginning with the sourcing, cleaning, and organization of data, followed by care ful 
cartographic manipulations and stylings, resulting in an end product that is a static 
or standalone interactive map (see Figure 2) [14]. The specifics of how this pipeline 
is carried out, depend on the specific features of the situation such as the volume of 
data, update frequency, security model, end user platform specifications. At best, the 
data manipulation processes are shared and documented within a code repository 
like GitHub. This transparency and reproducibility help make tools and datasets more 
useful across situations, and thus more interoperable. Large, complex datasets often 
need custom pipelines in order to be transformed into useful and interoperable 
formats. With limited standards for aggregation of data prepared without Geospatial 
consideration (flexible attachment to grid, locations, or boundaries) or assessment 
frameworks for geographic coverage, consistency, and change in value over time 
(related to user dynamics of different source mobile apps), the potential power of 
heterogeneous datasets has not been realized or leveraged. If the work is 
collaborative or intended to be auditable, it is essential that data manipulation 
processes are shared and documented within a code repository framework such as 
GitHub.  
The global COVID-19 response in 2020 has accelerated several trends related 
to the processing and sharing of private sector aggregated location data. 
Governments and companies such as Facebook, Mapbox, Simtable and SafeGraph 
are involved in map products that summarize population movement, and data from 
these efforts have been leveraged by researchers to study various outcomes, 
including relating epidemiological outcomes with compliance with movement 
restrictions, with an eye towards developing a leading edge prediction of viral 
resurgence. This urgency and heterogeneous uptake across different areas has led to 
significant challenges related to interoperability as well as privacy. COVID-19 has 
revealed both problems and opportunities regarding institutional trust and data 
sharing. The value of individual health data in helping governments and civilians plan 
for and react to the spread of disease is inarguable, but the lack of a standardized 
framework for individual governance of personal data has led to mixed sentiments 
regarding sharing, which is potentially related to the success of national governance 
in combating the pandemic [15–21].

## Page 9

Reimagining Maps 
 
 
6 
 
 
Skill Gaps 
The computer science and artificial intelligence communities are often concerned with 
best practices for “mapping” data from one structure to another to take advantage of 
efficiencies or advantages of one representation of the data versus another, but the 
GIS trained workforce is broadly unprepared to implement these best practices or 
work with code, databases, or Artificial Intelligence (AI) [22]. Due to the specialization 
silos and changing hiring practices that emphasize machine learning, computer, and 
data science backgrounds, the GIS workforce may be in danger of simply being 
displaced by software developers. For example, common general questions facing 
developers using tools by the company Mapbox are: “how is our data loaded into the 
client side for manipulation?” and “how will we pre-process this data on our platform 
into vector1 tiles?”. Expertise in cartographic methodologies and practice are rare to 
find in the aforementioned communities [24–27]. The resulting lack of synthesis in 
the best practices among the domains of computer science, data science, and GIS, 
as well as those between these domains and graphic design and user experience 
engineering (UX), has notable impacts on the consumers of maps, who are liable to 
 
 
1 A data standard for terrain and traffic data [23] 
Figure 2. Map Production Pipeline

![page9_img1.png](images/page9_img1.png)

## Page 10

Reimagining Maps 
 
 
7 
 
be overwhelmed with volume of data or misled by its presentation. Existing processes 
and complicated delineations of responsibility may, at the least, cause general 
misunderstandings about course of action analysis, and, at the worst, lead to tragic 
failures such as those caused by errors in emergency (US 911, UK 999) dispatch 
orders or motorists being left stranded in deserts [28–31]. The skills needed for 
modern cartography are those that facilitate the answering of these questions. 
User Awareness 
Overly prescriptive, robotic guidance systems are among the worst signal-to-noise 
ratio offenders in everyday life (e.g. frequent and salient “false positive” notifications 
reduce user vigilance and thus impair navigation). At this point, navigational guidance 
has limited intimations of human-level experience and understanding, for example 
providing ambiguous guidance during complicated maneuvers, or being disconnected 
from obvious surrounding phenomena in situations encountered on a daily basis. 
These systems have a limited ability to incorporate users' cognitive awareness, and 
any introduction of existing knowledge as a filter would vastly reduce the cognitive 
load for navigation. Further, likely due to a lack of trust in both intent and capability 
of users [32], there are limited affordances for users to update details about their 
environment in order to improve the experiences of others and where these 
affordances exist they often don’t implement best practices on crowd sourcing [33], 
consequently generating a variety of complex threat surfaces for the purposeful and 
accidental introduction of uncertainty [34]. 
Mapping Uncertainty 
There is the eternal challenge of determining whether blank spots on the map 
represent absence of presence or lack of knowledge. In OpenStreetMap, an empty 
place may have already been surveyed for structures and none were found, or it is 
possible that it was never evaluated before or recently (and thus may actually have 
or not have a structure at that location). During the 2014-2015 Ebola response, West 
African communities that expanded rapidly in recent decades were found to be 
unmapped, a challenging situation for public health and resource allocation. The 
urban edge and new settlements are ever expanding, particularly in newer cities of 
Global South. We need to track the meaning of blank spots globally, perhaps through

## Page 11

Reimagining Maps 
 
 
8 
 
the use of generative models that take uncertainty into account. Some techniques do 
exist that allow for inference in unmapped or poorly-mapped areas, for example 
approaches that soften the boundaries of point and vector data [35]. However, the 
approaches for mapping uncertainty thus far have not lent themselves to meaningful 
to action facilitation in challenging situations [36].  
Existing infrastructure is rapidly overturning as well in response to crisis from 
climate, conflict, and public health emergencies. The impact of COVID-19 lockdowns 
on business closures means that wide parts of our existing maps are suddenly out of 
date. It should be feasible to identify entire districts that have overall less certainty 
of continued function. The inability to handle uncertainty, combined with larger 
volume of diversified source data, in rapid production, makes maps more vulnerable 
to unintentional or maliciously injected noise. 
Threat Actors 
In a global world, the security, governance, and trust of maps and data becomes even 
more important. Fundamental data such as GPS is vulnerable to spoofing [37]. 
Intentional map data spoofing has occurred in augmented reality games such as 
Pokémon Go and games which use real-world spatial data to generate their 
environments, such as Microsoft Flight Simulator, both have been known to show 
distorted segments of OpenStreetMap [38,39]. An increasing fraction of real-life is 
enacted online in “social media”, in the gray-zone between games and reality. The 
Ukraine/Russia conflict presents a (possibly apocryphal) story about the introduction 
of intentional changes in OpenStreetMap to divert forces into less strategic points on 
the landscape. More well-known are the security risks of wearable GPS-enabled 
trackers, which can leak information about sensitive assets [40]. In cities and military 
operations, where maps are in constant use to facilitate decision making, the 
consequences of inaccurate maps can be dire. As user-input influenced maps become 
spaces for conflict themselves, there is a critical need for map quality assurance, 
based upon data and pipeline trustworthiness. 
Volume of Data 
Implementation of user-informed systems that account for quality assurance and 
trustworthiness means leveraging huge volumes of data in a manner that is

## Page 12

Reimagining Maps 
 
 
9 
 
sufficiently responsive to on the ground situations (e.g. within the expected timescale 
of interacting with a smartphone app, less than seconds). The need for fast decisions 
means that analysis of data must also in part migrate to the edge of the computing 
network, away from centralized server farms and towards the end-user’s networks and 
devices. Increasing power of devices and geospatial processing libraries means less 
round-trip travel for gathering insights. Some projects are beginning to explicitly 
address these challenges, for example the US Wind Turbine Database [41] calculates 
power capacity using Turfjs [42,43].  
As the data environment becomes more complex, along with a growing 
necessity to leverage new open sources, the ability to communicate data certainty 
and chain-of-custody to the end product is paramount. The pursuit of these goals 
has led to problems in data analysis as an ever-increasing number of sensors and 
information-producing devices is making data volumes expensive or untenable to 
store in totality. This necessitates action-oriented, privacy-preserving, and flexible 
low-dimensional representations of data, a topic returned to later in the paper. In 
2020, location and environmental sensors are becoming embedded into our devices, 
vehicles, infrastructure and objects in the logistics flow. These sensors are 
proliferating in number, reporting time-tagged location data to multiple aggregators. 
In 2019, hundreds of millions of GPS chips were in use, most commonly attached to 
a networked device, reflecting a market of around $100 Billion USD. New geo-
positioning systems are coming online in all of the major powers. Nearly all new 
vehicles ship with GPS and network components. With a vehicle fleet turnover of 15-
20 years [44], it is safe to predict that a majority of vehicles will be generating location 
data by the end of the 2020s, either through onboard sensors, or smart devices 
carried by passengers. 
Accessibility 
As technological platforms increase in scale and intricacy, accessibility for users and 
institutions is a key concern. Many contemporary projects are making significant 
strides in spatial mapping reach and accessibility however there is still a long way to 
go. To provide a few examples: the NOAA Big Data Program makes very large and 
ever-growing imagery and analysis projects accessible directly in networked cloud 
computing environments [45,46]. Other maritime use-cases of large geospatial 
datasets are also becoming increasingly important for global ecological and legal

## Page 13

Reimagining Maps 
 
 
10 
 
governance [47–49]. Leveraging specifications like Cloud Optimized GeoTIFF 
(Geospatial Tagged Image File Format) [50] enables the efficient utilization of large 
data stores by offering the ability to share select views of raster data available over 
the network. Simple specifications like Spatio Temporal Asset Catalogs [51] can solve 
the problem of manually searching for needed geography, time and quality over many 
different holders of satellite imagery, both commercial and government.  
These developments in software and database technology are all occurring 
within the landscape of proliferation of government and corporate sensor platforms, 
in particular, large constellations of small satellites like Planet [52]. CARTO’s 
BigQuery Tiler [53] eases the flow from massive data storage and analysis to map 
production through automated transformation of results into efficient network centric 
formats like Vector Tiles [23]. ML enabler [54] reuses the common distribution format 
of web maps (spherical Mercator tiles) to standardize and scale ML processing and 
integration into collaborative mapping tools. Edge data capture and processing. 
“Pixel8.earth” uses commodity mobile phone hardware to capture 3d point cloud 
models [55]. The Mapbox VisionSDK allows for on-device image segmentation and 
extraction of real time street level view [56]. These projects and others are pointing 
the way towards accessible and powerful geospatial platforms for use by citizens, 
researchers, and policy-makers. 
Key Challenge Areas 
Here we distill the challenges listed above into three key contemporary challenge 
areas for geospatial mapping, where significant technological advances would not 
only be plausible and provide remedy for current limitations, but may also offer 
opportunity for a transformative reimagining of the potential for the capabilities and 
generation of maps in the future: 
Rapid Generation of Relevant Maps 
The challenge of generating relevant maps is linked to the difficulty 
of integrating user-specific analytics with multidimensional, real-time 
information about the world, local ecosystem, mission, and team. 
Maps are used for missions, but when map information is outdated or 
is inaccurate when compared with reality, the use of the map can

## Page 14

Reimagining Maps 
 
 
11 
 
become counterproductive. The wider the gap between the map and 
the territory (due to outdated or otherwise incorrect information), the 
more risk there is for missions. The purpose of maps is not just to 
provide information about a user’s environment, but instead to provide 
relevant information to facilitate action—if each user or team involved 
in a mission has different roles to perform, then maps need to be 
rapidly rescoped and regenerated in order to properly to optimize 
communication of information, uncertainty, and affordances relevant 
to each of their respective tasks. 
Informational Compression  
and User Experience 
The users of maps are humans—spatiotemporal technologies reflect 
a case of human-in-the-loop augmented collective intelligence 
systems. Even the “right map at the right time” needs to have the 
correct informational compression for the appropriate user (e.g. an 
evacuating family, a grocery delivery driver, a recreational gamer). 
Too much information presented to the user at once, or unintentional 
noise in the representation of the data, can be cognitively expensive 
or distracting, thus contributing to risk of misinterpretation, analysis 
paralysis, or mission failure. The fundamental challenges of 
sensemaking and semantics are fused with the unique strengths and 
weaknesses of large datasets in the spatial mapping paradigms of 
today and tomorrow. Additionally, maps are geopolitical conflict 
spaces, which means they are often influenced by threat actors 
engaged in the strategic generation of deliberate noise and 
perturbations.

## Page 15

Reimagining Maps 
 
 
12 
 
Security, Governance, and Trust  
of Maps and Data 
The increasing reach and accessibility of maps is highlighting 
problems related to governance, privacy, and security. In some cases, 
the tension between user-annotated and automatically-annotated 
features can decrease trust in the entirety of the mapping processes 
and data sets. At the same time, generative algorithms are being used 
to create novel data, to extrapolate what street level view is like from 
satellite imagery [57], or intentionally deep fake landscapes and 
infrastructure [58]. Google’s Kartta Labs is looking to recreate historic 
street scenes employing a combination of crowdsourced historic maps 
and deep learning [59]. Research in the domain of computer vision is 
yielding frameworks that are becoming more competent at extracting 
meaning from imagery. Notably Facebook produced global population 
data sets [60], and road networks for integration into OpenStreetMap 
[61]. Despite this increase in reach of automated annotated map 
products, in an internal Mapbox study, it was found that within a 
package of over 100 million Machine Learning derived building 
objects released by Microsoft for geospatial use cases within the US, 
there were notable cases of natural features, such as boulders and 
ponds, being incorrectly labeled as human structures. In all these 
cases in others, questions about the security, privacy, and governance 
of data are front and center. Without reliable and authenticated data, 
stored in well-governed repository frameworks, complex mapping 
projects will be difficult to collaborate on and potentially untenable or 
insecure. 
Spatial maps aren’t just geospatial. We can “Reimagine Maps” and find cartographic 
insight by understanding various types of maps outside the traditional reach of map-
making.

## Page 16

Reimagining Maps 
 
 
13 
 
Part II 
Maps in other Fields 
In order to understand where we can go with maps, we need to consider the state of 
progress in various fields. Here we review disparate areas in which “maps” are 
applied, and consider examples, objectives, and limitations of each area. Across fields 
and use cases, the map is a tool that facilitates rapid reduction of uncertainty, often 
by conveying narratives, objectives, constraints, and threats [9]. We can consider an 
abstract map as a relation between data, information, and goals. In this light, 
similarities between geospatial maps of various kinds (archival and reference or 
itinerary) and non-geospatial maps can become apparent and provide actionable 
intelligence for reimagining the future of maps. For each section, we discuss the goal 
of the mapping system in focus, in relation to stakeholder requirements, and then 
inadequacies are addressed or identified. 
Process Mapping 
Process mapping is the application of spatial metaphors to the design of models of 
“relationships between activities, people, data, and objects” [62]. Where geospatial 
maps intend to inform the optimization of movement of objects in literal space, 
process maps intend to optimize organizational outcomes by helping to navigate the 
process of the production of a deliverable [63,64]. Process mapping has been applied 
inward, to the development of process maps themselves, resulting in a variety of 
methodologies [62], such as the Cobra six-stage method [63], BPR (Business 
Process Reengineering) project-stage-activity framework [65], and BPI (Business 
Process Improvement) [66]. Many navigation-oriented artifacts may be described as 
process maps, such as Operations Orders, which are used in Military, Intelligence, 
and Civilian teams to navigate toward successful missions [67–69], travel itineraries, 
communications frameworks, server architecture and distributed computing [70,71], 
and software. Process mapping has been noted to be of crucial importance to the 
improvement of the efficiency, reliability, and auditability of business operations [62–
64,66,72–76]. The strict mapping of the passing of precursors and products-in-
development to end-deliverables has allowed for the development of methodologies 
that help to clarify to map-readers exact expectations of input and output as well as

## Page 17

Reimagining Maps 
 
 
14 
 
variability and uncertainty at each stage of the process being described [77,78]. 
However, process mapping also has strong limitations, such as its linearity and 
inability to rigorously deal with complex systems beyond the scale of the process 
mapper’s scope. The value of the process map has an inverse relationship with the 
complexity of the process and the potential for novelty, and may contribute to a false 
sense of knowing about the nature of the business processes they intend to represent 
[62], leaving organizations vulnerable due to the lack of preparation for novelty. 
Software and Software Development 
This potential for novelty in process mapping is not so much a limitation in the 
description of software and business logic, where process maps are composed of 
algorithms and strict data structures for the reliable exchange and manipulation of 
data with expectations for linearity and reproducibility at each stage of the process 
[79]. In these domains, process mapping languages such as UML can be incredibly 
expressive [80]. This has resulted in wide adoption in the computer and data science 
communities to express software in development and have been adapted in the 
SCRUM and AGILE frameworks to express the workflow of developing the software 
as well as the software itself [81,82]. These communities are not immune from all of 
the limitations associated with process mapping languages however, such as the 
notoriously steep learning curves, strict standardizations, and lack of interoperability 
between not just the standards themselves but between models produced by them. 
This is exacerbated by the lack of codified or interoperable ontologies for the state 
and mechanisms of the systems they wish to model [83–85]. A common comment is 
that it can be more difficult to code the representation of abstract objects in process 
languages than it is to code the abstract objects themselves [83]. The standard in 
common use for UML is hundreds of pages long [86] and interpretations of the 
standard are often debated, making it inexpressive to individuals who are not already 
familiar with the standard.  
As software projects become larger and include components beyond the 
scope of the development team (e.g. open-source libraries used as dependencies), 
process maps can create more burden then they relieve. Where process maps for 
business processes leak value proportional to the complexity and potential for novelty 
within a process, process maps for software see diminishing returns and, after some 
threshold, negative returns. This reduction in value is related to the level of

## Page 18

Reimagining Maps 
 
 
15 
 
complication of the process being described. In the engineering of complicated 
systems, it is best practice to institute a separation of concerns regarding the various 
mechanisms within the system [87]. In order to meet this demand, many UML maps 
would have to be generated in order to maintain low signal-to-noise ratios for 
developers working on their sections of a project. At the cutting edge of process 
mapping are solutions to these limitations, embedded in frameworks like cadCAD 
[88]. In cadCAD, the entire modeling process can be mapped and simulated, and 
maps can be generated rapidly with scope defined to any particular mechanism or 
the flow of state between them. The cadCAD package was developed in the interest 
of providing a generalizable framework for the modeling of Complex Systems but can 
apply to other systems as well. 
Complex Systems 
In Complexity Science, the “map” is a nomadic metaphor that relates actors and 
actions of various kinds [89]. The idea of a map is applied across systems and scales, 
in order to highlight analogies [90–94]. Some shared methodologies across these 
use cases include Bayesian modeling, network science, and predictive/counterfactual 
approaches [95,96]. The objective of these maps are to enable understanding, 
control, and design of large emergent or autopoietic systems [97,98]. These kinds of 
maps are used qualitatively as metaphors or homologous structures that suggest 
system leverage points for control. These maps can variously take the form of system 
engineering diagrams [99,100], complex system modeling platforms [88,101], or 
causal “world modelers” as per several recent projects, but also can be used as 
quantitative tools. Causal diagrams are often used in complex systems maps because 
these kinds of models can lead to reduced uncertainty about key leverage points for 
action. Similar to the geospatial problem space, interoperable encoding of complex 
ontologies and pipelines for transformation of data seem to be key limiting factors 
within these domains. 
Communications 
In the gray-zone between Geospatial and process maps lie the applications of 
mapping 
metaphors 
and 
methodologies 
to 
represent 
communications. 
Communications maps which intend to represent connectivity in physical locations

## Page 19

Reimagining Maps 
 
 
16 
 
have had to overcome key limitations of two- and even three-dimensional Geospatial 
representations in order to include non-terrestrial entities such as satellites which 
are never static in position and are not fixed in position to the Earth. Methods to 
remedy this have included three-dimensional colored overlays, re-rendering the map 
based on timestamp, and including supplementary non-spatial maps [49,102,103]. 
These accompanying non-spatial maps are especially important to understanding the 
flow of maritime communications, where most of the communication is being done 
between a series of objects which are in motion and communicating information 
which needs to be routed to a variety of destinations over a variety of channels. Some 
of these destinations are spatial, such as a Port Authority, but many destinations can 
be abstract, such as the set of all servers within a company which can parse some 
kind of incoming sensor data from a vessel. Key challenges of this mapping are a 
lack of data standardization and a pileup of low-integrity data from the introduction 
of Internet of Things (IoT) sensor-technology producing billions of data points per 
vessel annually [49].  
Communications maps are being implemented as a part of workflow maps in 
other domains which also have abstract, non-spatial paradigms, such as in server 
architecture, distributed computing tasks [70,71], and in the embodied and remote 
information processes that are increasingly enacted in the small-group online settings 
(research, education, innovation, etc.), where novel individual and collective 
affordances are available [34,104]. In such situations, team communication maps are 
network representations of the channels of information flow among teammates [100]. 
Team communication maps can be reflected visually as a graphical layout, or using 
other visualization techniques from topology, network analysis, and big data analytics. 
The objectives of team communication maps are several-fold: to clarify how 
collaborators are informationally connected, to design improved paradigms for 
teamwork, and to reduce redundant or spurious links within a group. Team 
communication maps are specifically designed to deal with the challenges of many 
interacting agents, some aligned and some adversarial/external teammates. Modern 
team communication protocols are primarily through the internet, though can also be 
through other electromagnetic spectrums or physical objects. Current limitations of 
team communication mapping tools include the scarcity of usable yet flexible tools, 
and friction with integrating such tools into current team tech stacks and behavioral 
repertoires.

## Page 20

Reimagining Maps 
 
 
17 
 
Knowledge Management and Information Systems 
Knowledge mapping has a variety of definitions, but all reference common objectives, 
which include the facilitation of exploration, discovery, navigation, and recovery of 
information [105–107]. Knowledge maps help to connect ideas and observations 
within a framework that allows for disciplinary (e.g. accounting, legal) or 
interdisciplinary teams (e.g. research, military) to make sense of the relationships 
between topics and concepts. Knowledge mapping is generally a qualitative, visual 
task composed of adding and arranging different ideas on a canvas to suggest new 
associations to make, or analyses to perform. Knowledge mapping of this kind has 
become popularized as a note-taking tool under the name “mind-mapping” for 
individuals who are looking to improve their work-flow in business, research, and 
education contexts [108,109]. Enterprise Knowledge Management Systems (KMS), 
such as those employed by Palantir and similar companies, include the generation of 
maps that can be extremely quantitative and formalized, especially in specific 
subfields or where extensive semantic data already exist [104,110]. The creators and 
users of these maps generally face the same challenges as those found in cartography 
and software development: learning curves, generalizability of data, requirements for 
versioning, access control, and the need for rapid generation of new maps in order 
to allow for separation of concerns or scope for mission by the reader. Enterprise 
KMS have overcome some of these challenges by creating mechanisms for 
interoperability and versioning, and by creating query systems which regenerate maps 
based on stated objectives of the user and the information they’re already aware of, 
but these systems require a great deal of work in initial set-up and data integration 
in order to become feasible.  
In the relatively new domain of Open-Source Intelligence (OSINT), knowledge 
mapping is being implemented in order to facilitate the opening of the intelligence 
production cycle to include both members of the public and sources of information 
which are available to the public [111]. The “eyes and ears” model which dominated 
most domestic and foreign intelligence operations prior to the 20th century was 
successfully implemented at global scale by the city state of Ragusa around the 15th 
& 16th centuries [112], but the style of implementation is not amenable today given 
the number of individuals and amount of information sources available. While OSINT 
is often noted to be solely concerned with the inclusion of public resources in the 
intelligence production cycle, its focus on aggregation and interdisciplinary 
collaboration has led the domain to create a set of methods which help to fuse a

## Page 21

Reimagining Maps 
 
 
18 
 
variety of traditional intelligence gathering methods (see Figure 3) into a generalized 
framework for organizational sensemaking at a scale that traditional implementations 
of the eyes and ears model cannot [112,113]. Knowledge mapping in OSINT faces 
many of the same challenges as those found in enterprise KMS with the added 
difficulties from lack of affiliation and pre-existing trust between collaborators, as 
well as concerns with the inclusion of sensitive and highly technical materials in 
workspaces and individuals who have various levels of clearance and disparate 
domain expertise. It has been recommended that challenges of this kind may be 
overcome through the use of role-based access, user-aware work-spaces, better data 
standards, and gamification of tasks [100,104,114]. 
 
Figure 3. OSINT Fusion

![page21_img1.png](images/page21_img1.png)

## Page 22

Reimagining Maps 
 
 
19 
 
Education, Curriculum, and Learning 
At the intersection of process mapping and information mapping are mapping 
metaphors in the domains of education, continuing professional development, and 
human resources. The ability to communicate competencies and knowledge attained 
and mapping them to the requirements of roles and continuing education has been 
becoming increasingly difficult as fields of study, roles, and credentials become more 
specialized, which is consistent with early 20th century predictions [24–26,115]. The 
effects of this increasing granularization of specialization are exacerbated by two 
major factors. First, learning has become more personalized and decentralized, often 
being done online and outside the context of the traditional classroom. Second, 
deeply tied to the problem of specialization silos themselves, is that the communities 
concerned with the development of education and personnel data standards are 
generally composed of individuals who have a strong background in computer 
science with limited understanding of pedagogy or vice versa. As a consequence, 
many competency standards such as xAPI [116,117], SCORM [118], and LOM [119] 
are highly linear and inflexible. Attempts to update these standards have generally 
caused the standards ecosystem to become only more byzantine, causing problems 
with adoption.  
The objectives of many of these efforts was either to optimize competency 
development by rapidly generating and monitoring personalized learning pathways in 
order to identify and overcome skill and knowledge gaps, or to integrate approaches 
found in research from outside the realm of traditional organizational psychology in 
order to develop organization-level competencies and performance [120] such 
“serious games” [104,120] and collaborative creative work [121]. In order to 
overcome current limitations to achieve these objectives, it has been suggested that 
research be directed toward developing mechanisms for crowd-sourcing the 
cataloging of learning resources and relationships between learning resources and 
competencies, 
managing 
incentivization 
of 
crowd-sourcing 
through 
microtransactions, managing trust within crowd-sourced networks, and better 
understanding self-forming human networks, rapid optimization of collaborative work, 
and rapid formation of virtual organizations [120,122,123].

## Page 23

Reimagining Maps 
 
 
20 
 
Ecology and Biology 
The natural world, and the study of it, can inform the study of maps. Maps are used 
in Ecology to map species distributions [124], ecosystem services [125], and 
regulated areas for human use through space and time. In basic or theoretical 
ecology, maps exist as abstract or idealized spaces in which processes like 
succession, gene flow, and guild formation occur. For applied or conservation 
ecologists, maps are essential in providing information on corridors for animal 
movement, information on the location of genetic diversity, and potential sensitivity 
of different populations to projected climate changes. The objectives in ecological 
studies of maps are to determine how features or aspects of ecosystems such as their 
patchiness or resource distribution, influence biodiversity, system resilience, and 
organismal behavior [126,127]. Other goals of ecosystem mapping include 
characterizing the dynamics and (informational, geospatial, ecological) components 
of the niche. Modeling of ecological niches can assist in sampling for conservation 
or utilization. Ecological analyses are often at the regional or global scale, and 
increasingly being used in conjunction with sensor or GPS data, to regulate maritime 
and terrestrial activity [48]. Machine learning schemes based upon biogeography are 
transferable into other domains, perhaps because biogeographic maps integrate 
multiscale spatial and temporal phenomena, and can integrate predictive and Bayesian 
methods. [128].  
Some limitations of ecological modeling include microheterogeneity of the 
niche (e.g. temperature at one level of the rainforest different from temperature on 
the ground), and accurate historical/future prediction of climatic trends. 
Microheterogeneity of the niche can confound regional-level predictions, for example 
in the case where local temperature highs/lows can be outside the confidence interval 
of the larger area, it is unclear whether the confidence interval of the larger area 
should be expanded, or how to otherwise include this information on variability. The 
challenge of past and future projections of climate, used in niche occupancy 
prediction models [124,129], are similar to issues arising in large-scale climate 
modeling [130]. At the cutting-edge of addressing these challenges in ecology, are 
large consortium projects, globally-replicated long-term experiments, and 
spatiotemporal analytics algorithms borrowed from other fields [131]. In behavioral 
ecology, dynamic network representations are mapping out the interaction patterns 
of agents in systems like ant colonies and schools of fish [132,133]. Beyond 
ecological cases, there is a long history of “map” metaphors in developmental and

## Page 24

Reimagining Maps 
 
 
21 
 
evolutionary biology, such as the case of Waddington’s epigenetic landscape [134], 
the genotype-phenotype map [135,136], and fitness landscapes [137–139]. Map 
metaphors for biological systems are linked to causal analyses (e.g. mapping between 
cause and effect) and therefore influence policy and culture [9,140,141]. 
Mathematics 
Maps in mathematics often take the form of metaphors for projections of data or the 
results of functions onto visual planes, but these metaphors are tied to a generalizable 
ontology and set of methods for managing transformations of data between planes 
[142,143]. Functions are kinds of maps that connect inputs to outputs, for example, 
the function y=2x maps values of y onto values of x that are twice as large. Metaphor, 
ontology, and methods alike provide helpful lenses for application and understanding 
the nature of functions and their domain (the objects and values which can be acted 
on) and range (the objects and values which can be produced) [143]. The ontology 
within the mathematics mapping domain diverges a great deal from other mapping 
domains described, most notably in the definition of the term “map” itself. The “map” 
does not refer to the visual projection of data on “Plane Y” from data sourced from 
“Plane X”, instead, the “map” is the function through which “Plane X” data are passed 
in order to generate or locate the data which sit on “Plane Y”.  
Mathematical mapping methods have been well generalized to work outside 
the realm of theoretical math and abstraction in physics and applied engineering. For 
example, in the gray-zone of computer science and mechanical engineering, these 
methods allow the “map” to be an algorithm, enabling the mapping of complex, n-
dimensional objects, an example being the mapping of stress-tensors2 to any other 
measure of strain [145]. These kinds of maps enable interoperability between 
standards without the addition of new standards or frameworks as well as enable the 
rapid generation of visualizations and models [145]. These mathematical intimations 
regarding maps overcome the limitations found within other map domains described, 
as maps become “generators” of visualizations rather than the visualizations 
 
 
2 Tensors are high-dimensional objects that are increasingly being used in machine learning across 
different domains, through transferable algorithms such as TensorFlow [144]

## Page 25

Reimagining Maps 
 
 
22 
 
themselves. Freed from focus on fixed products, mathematical maps can be linear, 
non-linear, chaotic, stochastic, or whole computer programs with humans in the loop, 
such as AI, and can contain multiple layers of maps contained within Markov blankets 
[146,147]. This is akin to modern paradigms in cartography where “maps” are 
increasingly becoming user-informed and user-aware, and being presented in terms 
of dynamical connectors, rather than simply being low-dimensional projections of 
higher-dimensional data.  
The application of mathematical maps represents the cutting edge of a number 
of fields. For example, underpinning the field of cryptology, which is concerned with 
the security and encoding of data, is the ontology and methodology associated with 
maps [148,149]. The “hashing” of an object, or the reproducible, algorithmic 
conversion of data into a string of a specified length of random characters is a type 
of “non-homotopic” data transformation or mapping. Non-homotopic transformations 
are those which occur using a map for which there is no defined inverse or reciprocal 
(we can transform the data from plane XY onto plane WZ, but there is no defined map 
that will project the resulting WZ data back into its original position on the XY plane). 
Where reverse transformations are implausible or computationally intractable, non-
homotopic mappings can be used as a one-way encryption, or hashing, technique. 
On the other hand, the encryption of data is an explicitly “homotopic” transformation 
in which there is one map for encoding data into cipher-data and another for 
conversion from cipher-data back to its original state. Underneath the business logic 
of advanced data manipulation and integration frameworks, such as those used by 
Palantir, are transformations described as “isomorphisms”, which are structure- and 
order-preserving maps [150,151], and transformations over special kinds of maps 
like “functors”, which allow for the coherent transformation of objects from one set 
or category to another [152,153]. In cases where mapping transformation is able to 
convey some knowledge about the strategies available for a specific the starting state 
and action (e.g. “this account has enough money to pay the bill”) while strongly 
protecting other dimensions of the data (such as specific amounts or previous 
transactions), the relationship is known as “zero knowledge”. Zero knowledge 
cryptographic proofs are increasingly relevant for Internet of Things (IoT) [154] and 
cryptocurrency uses [155,156].

## Page 26

Reimagining Maps 
 
 
23 
 
Part III 
“Reimagining Maps” 
The application of mapping metaphor and methodology in many of the domains and 
subdomains described have converged on some combination of the three key areas 
of limitations of modern spatial maps raised in the Introduction. However, each 
domain has approached the development of next-generation solutions to their shared 
limitations in unique ways, and these advanced approaches will be considered in the 
reimagining of maps with respect to each key area of limitations. 
The Map is Not the Territory 
Many of the domains described faced similar requirements for the necessity of rapidly 
generated maps for managing detail and scope, producing maps for a variety of users 
and stakeholders, viewing maps at a variety of scales, and managing the integration 
of changing parameters, user input, and constant flows of real time data. Mapping 
paradigms in mathematics and at the cutting edge of the mapping of complex systems 
and workflow, are potentially helpful conceptions and methodologies for the rapid 
generation of relevant Geospatial maps.  
The application of static reference maps in many tasks is now outdated, as 
reference data living in databases can simply be projected on command to any 
number of visualizations or directed to analysis frameworks. Now that the data can 
more easily live at their source or in accessible collections, they are frequently used 
or updated through transformations into a more fit for purpose data structure. This 
fundamental turn in cartography towards dynamic data structures moves beyond the 
practice of the mapmaker as collecting data to their workspace for human evaluation, 
to the mapmaker applying cartographic transformations to ever updating sources 
outside their control. The static map no longer serves a single arbiter of truth. Rather, 
mapping can now primarily consist of sculpting the processes by which user- and 
mission-specific maps are generated and delivered. This shift toward holding the map 
in the data allows for the interactive visual representations of complex or 
mechanistically complicated systems where no single static representation could

## Page 27

Reimagining Maps 
 
 
24 
 
possibly communicate all of the meaningful components or processes without 
overwhelming the user.  
Using conceptions of maps from within mathematics, where maps are 
generators of the projection rather than the projection itself, paired with the 
gamification and temporary, Instantaneous Remote Teams (IRTs) of experts found at 
the cutting edge of OSINT practice [34,100,104]. The traditional mapping procedure 
of data preparation, model creation, cartographic design, layout, quality control, print, 
and dissemination [14] could be greatly expedited and more easily delegated to a 
variety of teams of collaborators and contributors. For each encountered map request, 
temporary teams could be formed from domain experts and relevant stakeholders to 
produce generators for the transformations and projections necessary at various 
stages of the procedure [104]. Prioritizing the production of generators rather than 
the production of visualizations has already led to a great deal of progress in the 
enterprise mapping community, converting more organizations to this prioritization 
and creating non-proprietary standards for generators and the data which they use 
could yield a great deal of value. In addition, the use of Instantaneous Remote Teams 
(IRTs) helps to overcome previously stated problems regarding the difficult to attain 
skill combinations required for successful navigation of the entire procedure by a 
single team or individual. Select data scientists and domain experts can be enlisted 
to focus on case-specific generators for the often non-routine data preparation and 
model generation or be considered the generators themselves, and cartographers and 
graphic designers can focus temporarily enlist the help of software developers or 
data scientists in generators of layout and projections without these skill-sets 
dominating these areas of the procedure. 
User/Role/Actor-Centric and Mission-Aware Maps 
With the correct generators, systems can have a model of the end-user built-in and 
use a map production procedure that not only takes end user characteristics into 
account, but also their objectives and feedback through the use of gamification. This 
gamification, through playful mechanisms found in Pokémon Go can be used to 
incentivize crowd-sourced development of features and notable improvement of 
mapping products.  In the domain of linguistics, Duolingo, a language learning 
platform, has mechanisms to allow expert users to help adapt and add to curriculum 
as a part of their own language learning. However, these user-contributed additions

## Page 28

Reimagining Maps 
 
 
25 
 
are slowly adapted for larger populations by more trustworthy users and staff—these 
mechanisms could be used to help inform trust management in crowd-sourced 
development of catalogs and map products as well.  
A key generalized objective across all mapping domains is hodological 
facilitation: they need to facilitate pathfinding and sensemaking for users intending 
to orient themselves or their assets toward action. Within the domain of this 
generalized objective are benign use-cases, such as finding a place to buy an iced 
coffee or trying to circumvent traffic where failures are measured in minutes wasted, 
alongside far more serious use-cases, such as evacuation during forest-fires, 
avoiding riots and roadblocks during civil unrest, and ambulances circumventing 
traffic, where failure is measured in human bodies and success in lives saved. In 
critical modern use-cases, maps must be generated just in time, not with just a visual 
layout, but rather with a mission-aware interface providing a sculpted set of 
representations and options that will either have outsized impacts on mission-success 
or quickly incorporate feedback from failures to do so. 
BOLTS 
Across nearly every mapping domain reviewed, there were limitations at the cutting 
edge concerning, not the availability of data, but the ability to rapidly integrate it. At 
the cutting edge of each of these domains, there appears to be an overwhelming 
consensus that standardization of data is prerequisite to the rapid generation of maps. 
Synthesizing the requirements from each domain indicates a need for data 
specifications which are reasonable for Business, Operational, Legal, Technical, and 
Social (BOLTS, see Figure 4) use-cases.  
One of the primary obstacles to developing such standards in the past has 
been adoption and the inflexibility that, axiomatically, accompanies the introduction 
of hard-coded standards. Universal standards for the exact schemas of all data objects 
that could be of use is unachievable, however, borrowing from concepts regarding 
transformations within mathematics may provide interesting insights. It is not 
necessary that all data be universally fit to specific schematics in order to be BOLTS 
reasonable, instead, all that is necessary is that the objects referenced within a data 
object (maritime vessels, individuals, documents), the instantiated data object itself, 
and the schematic which is used are accompanied by metadata in order to inform 
transformations. Standards regarding this type of meta-data would allow for greatly

## Page 29

Reimagining Maps 
 
 
26 
 
increased data sharing and cross-platform compatibility while also enabling the 
highest standards of privacy and governance if the standards were paired with 
encryption and decentralized consensus protocols.  
Just as mathematics defines maps as the functions which project the data, 
rather than the projection itself, BOLTS standards have the potential to provide an 
infralanguage by providing the standards for metadata to inform access and rapid 
transformation of data across frameworks. The presence of such an infralanguage and 
clear metadata would also allow for easier integration of AI into workflows to facilitate 
cross-referencing, discovery, and production, and transformations into varied, lower-
dimensional forms while maintaining sourcing and context. 
Fuzzy and Incomplete Data 
One of the great challenges to universal data catalogs is the presence of disagreement 
over not only what should be present in the schema, but also on how to handle 
disagreements and uncertainty within the data itself. This extends from somewhat 
benign cases of “what version of the book are we referring to in this library?” to 
“where is this national border?”, the practical impacts of these disagreements can 
range from dangerous to meaningless. Future data and metadata standards should 
incorporate the potential for disagreement and heresy within collections and 
acknowledge sourcing. Further, user-informed maps have already become conflict 
spaces and subject to threat-actors. It is possible that the future of maps doesn’t 
Figure 4. BOLTS

![page29_img1.png](images/page29_img1.png)

## Page 30

Reimagining Maps 
 
 
27 
 
prioritize crowd-sourcing, but instead “network-sourcing”. Based on the actual 
practice of data collaboration in OpenStreetMap and Wikipedia: reputation is foremost 
in the level of scrutiny any contribution receives. The anonymous crowd is treated 
with suspicion. Social networks, both in online and real spaces, are useful for 
assessment of the utility or validity of a contribution to a network-sourced map 
product. This requires the development of tools that offer algorithms or affordances 
to users to assess and assign the reputation needed for certain actions or 
visualizations to be accessible. 
Case study for Future Maps 
We now consider the potential impacts of a future of maps which includes these 
priorities and findings through the use of a narrative use-case based on a scenario 
offered by the United Kingdom’s Defence and Security Accelerator (DASA) “Map the 
Gap” competition [157,158]. 
In the “Map the Gap” competition, teams were tasked with surmounting 
realistic in-field challenges. The context is as follows: when expeditionary forces 
navigate within enemy territory, it is critical to mission success that physical 
boundaries be overcome, not just in the short term by advance units  (e.g. 
reconnaissance and special forces which operate at the operational reach of the field 
army), but also in the long term by units which have trouble navigating physical 
boundaries such as mechanized support and logistics units [159,160]. In the case of 
logistics and support units, these physical boundaries cannot just be overcome once, 
but must be reliably overcome many times with efficiency and robustness [161]. 
Some of the most notably difficult terrain features to overcome are known as “wet 
gaps”, such as streams, rivers, and bogs [157]. 
Rivers in particular offer a great number of unique challenges to expeditionary 
forces. From an engineering perspective, rapid construction of bridges requires 
knowing a number of difficult to ascertain variables which include but are not limited 
to, the profile, depth, and other characteristics of the river bed and riparian banks, 
the ground bearing capacity on both the near and far bank, the gradients and material 
compositions of the banks, and the logistics of material and equipment access. From 
a military perspective, bridge building requires allocation of equipment which

## Page 31

Reimagining Maps 
 
 
28 
 
immediately alerts the enemy to intent and location of potential river crossings. In 
addition, all current methods of bridge construction in the field place reconnaissance 
engineers and their equipment in vulnerable positions and take a large amount of 
time with a high probability of having to abandon the site. At the intersection of 
military, engineering, and joint operations contexts is the inclusion of numerous 
stakeholders and domain experts: reconnaissance engineers to identify and choose 
potential sites, expeditionary and joint operations command staff who select sites 
based on current unit positions as well as intent and threats after crossing, logistics 
staff who are involved in this process helping to define requirements, and field 
intelligence who inform stakeholders with intelligence products such as briefs and 
maps. 
In a reimagining of maps informed by BOLTS data specifications, allowances 
for fuzzy data, user/role-centric and mission aware maps, and IRTs, this procedure 
could be greatly expedited and far less dangerous. When the obstacle is identified 
(e.g. a “wet gap needs to get mapped”), two discrete calls might be made. The first 
call would go out to a number of individuals from the relevant organizations who have 
the appropriate clearance and domain expertise to form an Instantaneous Remote 
Team (IRT) with the purpose of choosing a bridge site, given what is known from 
remote sensing data and eyes on the ground. The second call goes out to create a 
digital workspace which can integrate data and coordinate work between the 
individuals and liaisons of units which are involved in the choosing the site. This 
workspace includes a variety of geospatial data-sets which offer the ability to project 
uncertainty over the structures and details they intend to represent. 
When field intelligence liaisons access the project-specific workspace, they 
select a role-based view which offers them data-sets, interactive dashboards, and 
situation reports from various reconnaissance teams and unmanned aerial vehicles 
in the area of operations. Local video and satellite reconnaissance data are blended 
with public source data to provide catalogs to users of the workspace to generate two 
and three-dimensional renderings of the terrain and relevant objects in the area of 
operations. Situation reports and intelligence data are processed to present 
interactive views that create high-sensitivity and high-specificity warnings regarding 
the potential for enemy activity. Reconnaissance engineers accessing the workspace 
see none of the detection alerts, situation reports, or positions of unmanned vehicles, 
but they do see warnings reflecting the potential for enemy activity and probability of 
detection. If involved engineers want to understand further, and have the clearance

## Page 32

Reimagining Maps 
 
 
29 
 
to obtain this information, they may change their role and see additional information. 
Otherwise, engineers weigh the warnings while making decisions regarding where to 
order the deployment of a variety of semi-autonomous, amphibious vehicles which 
carry combinations of sensors and sampling tools for the mapping of the variables 
associated with grading locations for site selection. Remote vehicle operators 
accessing the space, only see deployment orders, the positions of other remote 
vehicles, and warnings regarding enemy activity. When operators spot suspicious 
activity, they can submit situation reports which will be seen by field intelligence, 
their command, and other operators.  
 
Throughout this process support, communications, logistics, and command 
elements are in the loop watching for distress calls and requests. Cartographers, 
graphic designers, and domain experts work in concert to respond to requests for 
information and develop models and visualizations that are not available via extant 
generators. They document and enact their process and procedure for developing 
these artifacts in versioned repositories where new after-action IRTs can be formed 
with software developers and domain experts around creating generators for them in 
future operations. The workspace is an extension of a Knowledge Management and 
Command and Control System (C2) which allows for the integration of data-streams 
from other related operations and creates special work views for liaisons who need 
to be aware of the overlap between operations, preventing friendly fire and other silo-
related errors. Command and staff elements, related and unrelated to the operation 
can watch over the area of operations and take the view of any user or role to see 
what they see in order to intervene or redirect effectively.  
While this example is from the military domain, the approach applies as well 
to similar use in domains of city planning, where joint operations command, field 
intelligence, and military engineers are replaced by their civilian counterparts, such 
as local governing bodies, community planners, concerned citizens, and civil 
engineers. Both domains are often caught in a protracted process fraught with non-
productive cycles of arguments exacerbated by hardened interests and conflicting 
goals. In the city planning domain, there may be a large amount of existing and 
acquirable data, such as traffic studies, service and infrastructure impact studies, 
zoning regulations, and legal processes to synthesize and evaluate for accuracy and 
relevance, but the planning process itself is necessarily speculative. An IRT model 
that incorporates city officials, developers, residents, and land owners in a role-based 
workspace design that allows them to iteratively comment on, evaluate, and develop

## Page 33

Reimagining Maps 
 
 
30 
 
compromises regarding the possible cityscape increases the likelihood of results that 
are consistently beneficial to all stakeholders. 
Each role has overlap with every other, no two maps are the same as each 
map is curating the information required for sensemaking within each role’s 
information niche. Engineers hot-swap generators for projecting different sets of data 
over the map, allowing them to dial in to specific factors at different times without 
the need to request laborious production of multiple maps. Given a clear separation 
between datasets and map generators, information can be shared in a 
compartmentalized and secure fashion with trusted and untrusted actors on the 
ground. Joint operations command and city planners alike could have full access to 
add experimental generators for projections built from agent-based models and 
recommendation engines. Maps intended for human understanding should be 
personalized and tailored towards role-specific reduction of uncertainty. Map 
generation can be iterated—if the maps presented are not useful, the generators can 
adapt and adjust to that feedback either automatically or with human preferences in 
the loop. Maps intended for use by autonomous vehicles are action-oriented reduced 
representations of local or regional conditions and would be customized to run on 
minimal hardware or in offline settings.  Running through the entirety of these 
systems are some of the pillars of the future of maps: advanced analytical capacity, 
action-orientation, flexibility, modularity, accessibility, and interoperability. 
Conclusion 
In this paper we have surveyed the current state of cartography, with consideration 
for the pressures applied by COVID-19 as well as the changes in cartographic 
affordances for areas such as movement data, and addressed recent advances in 
technology are rapidly shaping the landscape of maps. We then reviewed a variety of 
fields adjacent to cartography where “maps” play a key role, such as mathematics, 
ecology, project management, and complex adaptive systems. Across fields and 
through history, maps and mappers are beset by similar challenges such as: 
integration of multimodal data, representation of uncertainty, user customization, and 
designing for action rather than archiving. We synthesized insights and practices from 
disparate areas in order to provide direction for research to realize a reimagining of 
maps and offered a use-case related to bridge construction in adversarial settings to 
convey what that reimagining might look like.

## Page 34

Reimagining Maps 
 
 
31 
 
Funding and Acknowledgements 
Daniel A. Friedman is funded by the NSF program Postdoctoral Research Fellowships 
in Biology (NSF 20-077), under award ID #2010290.  
Richard J. Cordes is supported in research efforts through a Nonresident Fellowship 
with the Atlantic Council on appointment to the GeoTech Center. 
The paper was written as a result of participation in an incubator named “Reimagining 
Maps”, hosted by the National Geospatial-Intelligence Agency on the platform 
Polyplexus. 
Works Cited 
1. 
Olsson G. Abysmal: A Critique of Cartographic Reason. University of 
Chicago Press; 2010. 
2. 
maps4news.com. Maps4News. In: maps4news.com [Internet]. 30 Jan 
2019 [cited 15 Oct 2020]. Available: 
https://maps4news.com/blog/cartography-change-technology/ 
3. 
North J. The Norton history of astronomy and cosmology. 1995. 
4. 
Aveni A, Romano G. Orientation and Etruscan ritual. Antiquity. 1994;68: 
545–563. 
5. 
Brown LA. The Story of Maps. Courier Corporation; 1979. 
6. 
Casson L. Travel in the Ancient World. JHU Press; 1994. 
7. 
Bagrow L. History of Cartography. Transaction Publishers; 2010. 
8. 
Woodward D, Harley JB, Others. The History of Cartography, Volume 1: 
Cartography in Prehistoric, Ancient, and Medieval Europe and the 
Mediterranean. Wiley Online Library; 1987.

## Page 35

Reimagining Maps 
 
 
32 
 
9. 
Winther RG. When Maps Become the World. University of Chicago 
Press; 2020. 
10. 
Whitewater Baldy Fire 2012. [cited 30 Oct 2020]. Available: 
https://www.flickr.com/photos/66435184@N02/7287321294 
11. 
COVID-19 Map - Johns Hopkins Coronavirus Resource Center. [cited 30 
Oct 2020]. Available: https://coronavirus.jhu.edu/map.html 
12. 
White TD, Ong T, Ferretti F, Block BA, McCauley DJ, Micheli F, et al. 
Tracking the response of industrial fishing fleets to large marine 
protected areas in the Pacific Ocean. Conserv Biol. 2020. 
doi:10.1111/cobi.13584 
13. 
George Floyd Protests - George Floyd Protests. [cited 30 Oct 2020]. 
Available: https://risk-analytics.io/pages/george_floyd_protests.html 
14. 
Kovarik V, Talhofer V. General procedure of thematic map production 
using GIS technology. International Conference on Military Technologies 
Proceeding, ICMT. 2013. pp. 1401–1408. 
15. 
Rowson R. Brits more comfortable sharing data with pharma since 
COVID-19 – survey. Pharmaphorum; 28 Jul 2020 [cited 30 Oct 2020]. 
Available: https://pharmaphorum.com/views-and-analysis/brits-data-
sharing-pharma-covid-19-survey/ 
16. 
Ghafur S, Van Dael J, Leis M, Darzi A, Sheikh A. Public perceptions on 
data sharing: key insights from the UK and the USA. Lancet Digit Health. 
2020;2: e444–e446. 
17. 
Gerdon F, Nissenbaum H, Bach RL, Kreuter F. Individual Acceptance of 
Using Health Data for Private and Public Benefit: Changes During the 
COVID-19 Pandemic. Harvard Data Science Review. 2020. Available: 
https://hdsr.mitpress.mit.edu/pub/3uc0p5dq 
18. 
Gramigna J. Institutional trust, mental distress increase in New Zealand 
following COVID-19 lockdown. In: healio.com [Internet]. Jun 2020 [cited 
30 Oct 2020]. Available:

## Page 36

Reimagining Maps 
 
 
33 
 
https://www.healio.com/news/psychiatry/20200610/institutional-trust-
mental-distress-increase-in-new-zealand-following-covid19-lockdown 
19. 
Cordes RJ. Transfer of EU user data to the United States halted - 
Atlantic Council. In: atlanticcouncil.org [Internet]. 25 Sep 2020 [cited 30 
Oct 2020]. Available: https://www.atlanticcouncil.org/blogs/geotech-
cues/transfer-of-eu-user-data-to-the-united-states-halted/ 
20. 
Anyaso H. Americans’ trust in institutions to handle COVID-19 is fading. 
In: northwestern.edu [Internet]. 8 Jun 2020 [cited 30 Oct 2020]. 
Available: https://news.northwestern.edu/stories/2020/06/americans-
trust-in-institutions-to-handle-covid-19-is-fading/ 
21. 
Drees J. How the COVID-19 pandemic has shifted patients’ support for 
health data sharing: Pew survey. In: beckershospitalreview.com/ 
[Internet]. 16 Sep 2020 [cited 30 Oct 2020]. Available: 
https://www.beckershospitalreview.com/healthcare-information-
technology/how-the-covid-19-pandemic-has-shifted-patients-support-
for-health-data-sharing-pew-survey.html 
22. 
lstomsl. Do I need to know how to code to be a GIS professional? 15 
May 2017 [cited 6 Oct 2020]. Available: 
http://millermountain.com/geospatialblog/2017/05/15/coding-for-gis-
professionals/ 
23. 
Mapbox. Vector Tiles Documentation. In: Mapbox.com [Internet]. [cited 
19 Oct 2020]. Available: https://docs.mapbox.com/vector-
tiles/reference/ 
24. 
Sloman S, Fernbach P. The Knowledge Illusion: Why We Never Think 
Alone. Penguin; 2018. 
25. 
Tett G. The Silo Effect: The Peril of Expertise and the Promise of 
Breaking Down Barriers. Simon and Schuster; 2015. 
26. 
Hanauer SB. A poor view from specialty silos. Nat Rev Gastroenterol 
Hepatol. 2010;7: 1–2.

## Page 37

Reimagining Maps 
 
 
34 
 
27. 
Kelly YP, Goodwin D, Wichmann L, Mendu ML. Breaking Down Health 
Care Silos. Harvard Business Review. 1 Jul 2019. Available: 
https://hbr.org/2019/07/breaking-down-health-care-silos. Accessed 25 
Aug 2020. 
28. 
Morse D, Moyer JW. A teenager was drowning. 911 sent help to the 
wrong place. The Washington Post. 21 Aug 2020. Available: 
https://www.washingtonpost.com/dc-md-va/2020/08/21/drowning-
death-911-response/. Accessed 6 Oct 2020. 
29. 
Gayle D. Australian police warn Apple maps “could kill”: Users looking 
for city directed to barren outback more than 40 miles away. In: 
dailymail.co.uk [Internet]. Dec 2012 [cited 8 Oct 2020]. Available: 
https://www.dailymail.co.uk/sciencetech/article-2245773/Drivers-
stranded-Aussie-desert-Apple-glitch-Australian-police-warn-Apple-
maps-kill.html 
30. 
Merchant B. This Is the Remote Desert Where Apple Maps Is Stranding 
Australian Drivers. In: vice.com [Internet]. Dec 2012 [cited 8 Oct 2020]. 
Available: https://www.vice.com/en/article/qkkvzv/this-is-the-hellhole-
that-apple-maps-is-sending-australians-into 
31. 
Van Staaveren J. Gradual Failure: The Air War Over North Vietnam, 
1965-1966. Lulu.com; 2011. 
32. 
Nielsen Norman Group. Are Users Stupid? In: 
https://www.nngroup.com/ [Internet]. 2001 [cited 20 Oct 2020]. 
Available: https://www.nngroup.com/articles/are-users-stupid/ 
33. 
Olleros FX. Learning to Trust the Crowd: Some Lessons from Wikipedia. 
2008 International MCETECH Conference on e-Technologies (mcetech 
2008). 2008. pp. 212–216. 
34. 
Cordes RJ, Friedman DA. Emergent Teams for Complex Threats. 2020. 
Available: 
https://www.remotorconsulting.com/uploads/4/8/4/2/48428829/emergen
t_teams_for_complex_threats__1_.pdf

## Page 38

Reimagining Maps 
 
 
35 
 
35. 
Nelson J. How to Visualize Uncertainty With Know-It-All Vector Data. 2 
Apr 2020 [cited 6 Oct 2020]. Available: https://www.esri.com/arcgis-
blog/products/arcgis-pro/mapping/how-to-visualize-uncertainty-with-
know-it-all-vector-data/ 
36. 
Cairo A, Schlossberg T. Those Hurricane Maps Don’t Mean What You 
Think They Mean. The New York Times. 29 Aug 2019. Available: 
https://www.nytimes.com/interactive/2019/08/29/opinion/hurricane-
dorian-forecast-map.html. Accessed 6 Oct 2020. 
37. 
Tullis P. GPS Is Easy to Hack, and the U.S. Has No Backup. Scientific 
American. doi:10.1038/scientificamerican1219-38 
38. 
Williams A. Microsoft Flight Simulator’s Data Insanity Spawns Enormous 
Buildings And Anomalies From OpenStreetMap. 21 Aug 2020 [cited 6 
Oct 2020]. Available: https://hackaday.com/2020/08/21/microsoft-flight-
simultors-data-insanity-spawn-enourmous-buildings-an-anomalies-
from-openstreetmap/ 
39. 
Reddit Handle u/Spanholz. r/TheSilphRoad - About OpenStreetMap and 
Pokemon Go. In: reddit.com [Internet]. 24 Jan 2017 [cited 29 Oct 
2020]. Available: 
https://www.reddit.com/r/TheSilphRoad/comments/5pvkkn/about_openst
reetmap_and_pokemon_go/ 
40. 
Hsu J. The Strava heat map and the end of secrets. WIRED, Jan. 2018 
[cited 7 Oct 2020]. Available: https://www.wired.com/story/strava-heat-
map-military-bases-fitness-trackers-privacy/ 
41. 
Viewer. [cited 6 Oct 2020]. Available: 
https://eerscmap.usgs.gov/uswtdb/viewer/#3/37.25/-96.25 
42. 
Turf.js [cited 23 Oct 2020]. Available: http://turfjs.org/ 
43. 
Turf. Github; Available: https://github.com/Turfjs/turf 
44. 
Keith DR, Houston S, Naumov S. Vehicle fleet turnover and the future of 
fuel economy. Environ Res Lett. 2019;14: 021001.

## Page 39

Reimagining Maps 
 
 
36 
 
45. 
Big Data Program. [cited 6 Oct 2020]. Available: 
https://www.noaa.gov/organization/information-technology/big-data-
program 
46. 
Dempsey C. What is a GeoTIFF? 13 Dec 2019 [cited 8 Oct 2020]. 
Available: https://www.gislounge.com/what-is-a-geotiff/ 
47. 
White TD, Carlisle AB, Kroodsma DA, Block BA, Casagrandi R, De Leo 
GA, et al. Assessing the effectiveness of a large marine protected area 
for reef shark conservation. Biol Conserv. 2017;207: 64–71. 
48. 
White TD, Ferretti F, Kroodsma DA, Hazen EL, Carlisle AB, Scales KL, et 
al. Predicted hotspots of overlap between highly migratory fishes and 
industrial fishing fleets in the northeast Pacific. Sci Adv. 2019;5: 
eaau3761. 
49. 
Låg S, Knutsen KE, Vartdal BJ. Ship Connectivity. 2015 [cited 25 Oct 
2020]. doi:10.13140/RG.2.1.4429.2961 
50. 
Cloud Optimized GeoTIFF. [cited 6 Oct 2020]. Available: 
https://www.cogeo.org/ 
51. 
SpatioTemporal Asset Catalog. [cited 6 Oct 2020]. Available: 
https://stacspec.org/ 
52. 
Daily Satellite Imagery and Insights. 16 Oct 2020 [cited 23 Oct 2020]. 
Available: https://www.planet.com/ 
53. 
CARTO. Improving Healthcare Access with BigQuery Tiler — CARTO 
Blog. [cited 6 Oct 2020]. Available: https://carto.com/blog/improving-
healthcare-access-bigquery-tiler/ 
54. 
Anwar S. ML Enabler — completing the Machine Learning pipeline for 
mapping. In: Development Seed [Internet]. 11 Jul 2019 [cited 6 Oct 
2020]. Available: https://medium.com/devseed/ml-enabler-completing-
the-machine-learning-pipeline-for-mapping-3aae94fa9e94 
55. 
Pixel8.earth. [cited 6 Oct 2020]. Available: https://www.pixel8.earth/ 
56. 
Vision. [cited 6 Oct 2020]. Available: https://www.mapbox.com/vision/

## Page 40

Reimagining Maps 
 
 
37 
 
57. 
Emerging Technology from the arXiv. Given a satellite image, machine 
learning creates the view on the ground. MIT Technology Review. 
Available: 
https://www.technologyreview.com/2018/07/05/141591/given-a-
satellite-image-machine-learning-creates-the-view-on-the-ground/. 
Accessed 6 Oct 2020. 
58. 
Tucker P. The Newest AI-Enabled Weapon: “Deep-Faking” Photos of the 
Earth. 31 Mar 2019 [cited 6 Oct 2020]. Available: 
https://www.defenseone.com/technology/2019/03/next-phase-ai-deep-
faking-whole-world-and-china-ahead/155944/ 
59. 
Recreating historical streetscapes using deep learning and 
crowdsourcing. [cited 6 Oct 2020]. Available: 
https://opensource.googleblog.com/2020/09/recreating-historical-
streetscapes.html 
60. 
Population Density Maps. [cited 6 Oct 2020]. Available: 
https://dataforgood.fb.com/tools/population-density-maps/ 
61. 
Mapping roads through deep learning and weakly supervised training. 
[cited 6 Oct 2020]. Available: https://ai.facebook.com/blog/mapping-
roads-through-deep-learning-and-weakly-supervised-training/ 
62. 
Biazzo S. Process mapping techniques and organisational analysis: 
Lessons from sociotechnical system theory. Business Process 
Management Journal. 2002;8: 42–52. 
63. 
Coulson-Thomas CJ. Business process re-engineering: the development 
requirements and implications. Executive Development. 1995;8: 3–6. 
64. 
Harrington. Business Process Improvement. McGraw-Hill Education 
(India) Pvt Limited; 2005. 
65. 
Kettinger WJ, James T. C. Teng, Guha S. Business Process Change: A 
Study of Methodologies, Techniques, and Tools. Miss Q. 1997;21: 55–
80.

## Page 41

Reimagining Maps 
 
 
38 
 
66. 
Povey B. The development of a best practice business process 
improvement methodology. Benchmarking for Quality Management & 
Technology. 1998;5: 27–44. 
67. 
Cordes RJ, Friedman DA. The Facilitator’s Catechism. 2020. 
doi:10.5281/zenodo.4062541 
68. 
Filiberti EJ. The Standard Operations Order Format: Is Its Current Form 
and Content Sufficient for Command and Control? ARMY COMMAND 
AND GENERAL STAFF COLL FORT LEAVENWORTH KS 1987. Available: 
https://apps.dtic.mil/dtic/tr/fulltext/u2/a191781.pdf 
69. 
Smith ML. The Five Paragraph Field Order: Can a Better Format Be 
Found to Transmit Combat Information to Small Tactical Units? School 
of Advanced Military Studies, US Army Command and General Staff 
College of Fort Leavenworth Kansas; 1988. Available: 
https://apps.dtic.mil/dtic/tr/fulltext/u2/a210966.pdf 
70. 
Deelman E, Blythe J, Gil Y, Kesselman C, Mehta G, Vahi K, et al. 
Mapping Abstract Complex Workflows onto Grid Environments. Int J 
Grid Util Comput. 2003;1: 25–39. 
71. 
Sakellariou R, Zhao H, Deelman E. Mapping Workflows on Grid 
Resources: Experiments with the Montage Workflow. Grids, P2P and 
Services Computing. 2010. pp. 119–132. doi:10.1007/978-1-4419-
6794-7_10 
72. 
Daniel Hunt V. Process Mapping: How to Reengineer Your Business 
Processes. John Wiley & Sons; 1996. 
73. 
Johansson HJ. Business process reengineering: Breakpoint strategies 
for market dominance. John Wiley & Sons; 1993. 
74. 
Manganelli RL, Klein MK. The reengineering handbook: a step-by-step 
guide to business transformation. 1994. Available: 
http://agris.fao.org/agris-search/search.do?recordID=XL2012000177 
75. 
Melan EH. Process Management: Methods for Improving Products and 
Service. McGraw-Hill; 1993.

## Page 42

Reimagining Maps 
 
 
39 
 
76. 
Morris DC, Brandon J. Re-engineering your business. McGraw-Hill 
Companies; 1993. 
77. 
Kim B, McCullough MB, Simmons MM, Bolton RE, Hyde J, Drainoni M-
L, et al. A novel application of process mapping in a criminal justice 
setting to examine implementation of peer support for veterans leaving 
incarceration. Health Justice. 2019;7: 3. 
78. 
Braglia M, Frosolini M, Zammori F. Uncertainty in value stream mapping 
analysis. Int J Logist Res Appl. 2009;12: 435–453. 
79. 
Wang M, Wang H. From process logic to business logic—A cognitive 
approach to business process management. Information & Management. 
2006;43: 179–193. 
80. 
Koch N, Kraus A. The expressive power of uml-based web engineering. 
Second International Workshop on Web-oriented Software Technology 
(IWWOST02). CYTED; 2002. pp. 105–119. 
81. 
Bass JM. Scrum master activities: process tailoring in large enterprise 
projects. Commun ACM. 2010;53: 126–130. 
82. 
Al-Ali AG, Phaal R. Design Sprints for Roadmapping an Agile Digital 
Transformation. 2019 IEEE International Conference on Engineering, 
Technology and Innovation (ICE/ITMC). 2019. pp. 1–6. 
83. 
Church A. Limitations of UML? In: 
softwareengineering.stackexchange.com [Internet]. 2014 [cited 24 Aug 
2020]. Available: 
https://softwareengineering.stackexchange.com/questions/145949/limita
tions-of-uml/227763 
84. 
Kumar A, Zhao JL. Dynamic Routing and Operational Controls in 
Workflow Management Systems. Manage Sci. 1999;45: 253–272. 
85. 
Kang I, Park Y, Kim Y. A framework for designing a workflow‐based 
knowledge map. Business Process Management Journal. 2003;9: 281–
294.

## Page 43

Reimagining Maps 
 
 
40 
 
86. 
Booch G, Jacobson I, Rumbaugh J. OMG unified modeling language 
specification. Object Management Group ed: Object Management Group. 
2000;1034. 
87. 
Walter L. Hürsch CVL. Separation of Concerns. 1995 [cited 24 Aug 
2020]. Available: 
http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.29.5223 
88. 
cadCAD. cadCAD – A Python package for designing, testing and 
validating complex systems through simulation. In: https://cadcad.org/ 
[Internet]. [cited 22 Oct 2020]. Available: https://cadcad.org/ 
89. 
Latour B. Reassembling the social. An introduction to actor-network-
theory. Am J Econ Sociol. 2013;14: 73–87. 
90. 
Cohen PR. The Big Mechanism Program and the Future of Scholarship. 
DARPA Biological Technologies Office Symposium; 2015 Feb 11. 
Available: https://www.youtube.com/watch?v=GCaXSyY_C9Y 
91. 
Cohen PR. DARPA’s Big Mechanism program. Phys Biol. 2015;12. 
doi:10.1088/1478-3975/12/4/045008 
92. 
Cohen PR. Acquiring Big Mechanisms by Reading Primary Literature 
Seminar. John Hopkins Whiting School of Engineering; 2015. Available: 
https://www.clsp.jhu.edu/events/acquiring-big-mechanisms-by-reading-
primary-literature-paul-cohen-information-innovation-office-darpa-and-
the-university-of-arizona/#.XL0nLehKiUk 
93. 
Dunne C, Shneiderman B, Gove R, Klavans J, Dorr B. Rapid 
understanding of scientific paper collections: Integrating statistics, text 
analytics, and visualization. Journal of the American Society for 
Information Science and Technology. 2012;63: 2351–2369. 
94. 
Davis PK, O’Mahony A, Pfautz J. Social-Behavioral Modeling for 
Complex Systems. John Wiley & Sons; 2019. 
95. 
Friston KJ, Parr T, de Vries B. The graphical brain: Belief propagation 
and active inference. Netw Neurosci. 2017;1: 381–414.

## Page 44

Reimagining Maps 
 
 
41 
 
96. 
Parr T, Markovic D, Kiebel SJ, Friston KJ. Neuronal message passing 
using Mean-field, Bethe, and Marginal approximations. Sci Rep. 2019;9: 
1889. 
97. 
Zeleny M. SELF-ORGANIZATION OF LIVING SYSTEMS: A FORMAL 
MODEL OF AUTOPOIESIS. Int J Gen Syst. 1977;4: 13–28. 
98. 
Luhmann N. The autopoiesis of social systems. Sociocybernetic 
paradoxes. 1986. 
99. 
cadCAD – A Python package for designing, testing and validating 
complex systems through simulation. [cited 26 Mar 2020]. Available: 
https://cadcad.org/ 
100. 
Vyatkin A, Metelkin I, Mikhailova A, Cordes RJ, Friedman DA. Active 
Inference & Behavior Engineering for Teams. 2020. 
doi:10.5281/zenodo.4021163 
101. 
Fang Z, Zhou X, Song A. Architectural Models Enabled Dynamic 
Optimization for System-of-Systems Evolution. Complexity. 2020;2020. 
doi:10.1155/2020/7534819 
102. 
VSAT - TecOffshore. In: tecoffshore.com [Internet]. [cited 25 Oct 2020]. 
Available: http://www.tecoffshore.com/communications/vsat/ 
103. 
Inga E, Cespedes S, Hincapie R, Cardenas CA. Scalable Route Map for 
Advanced Metering Infrastructure Based on Optimal Routing of Wireless 
Heterogeneous Networks. IEEE Wirel Commun. 2017;24: 26–33. 
104. 
Friedman D, Cordes RJ. Infinite Games for Infinite Teams. DARPA; 2020 
Jul. 
105. 
Ebener S, Khan A, Shademani R, Compernolle L, Beltran M, Lansang M, 
et al. Knowledge mapping as a technique to support knowledge 
translation. Bull World Health Organ. 2006;84: 636–642. 
106. 
Vail EF. Knowledge Mapping: Getting Started with Knowledge 
Management. Information Systems Management. 1999;16: 16–23.

## Page 45

Reimagining Maps 
 
 
42 
 
107. 
Wexler MN. The who, what and why of knowledge mapping. Journal of 
Knowledge Management. 2001. pp. 249–264. 
doi:10.1108/eum0000000005868 
108. 
Edwards S, Cooper N. Mind mapping as a teaching resource. Clin 
Teach. 2010;7: 236–239. 
109. 
Mento AJ, Martinelli P, Jones RM. Mind mapping in executive 
education: applications and outcomes. Int J Manage Enterp Dev. 
1999;18: 390–416. 
110. 
Wischner J. How Employees at Palantir Technologies Use Data to Tackle 
Real Problems. In: talentspace.io [Internet]. [cited 21 Sep 2020]. 
Available: https://talentspace.io/advice/deployment-strategist-palantir-
technologies 
111. 
IntelTechniques.com. [cited 23 Oct 2020]. Available: 
https://inteltechniques.com/ 
112. 
Dedijer S. Ragusa Intelligence and Security (1301-1806): A Model for 
the Twenty-First Century? Int J Intell CounterIntelligence. 2002;15: 
101–114. 
113. 
Hribar G, Podbregar I, Ivanuša T. OSINT: A “Grey Zone”? Int J Intell 
CounterIntelligence. 2014;27: 529–549. 
114. 
Kim T-W, Jung J-R, Kim S-W. Implications of the Dunbar Number in 
Collective Intelligence based on Social Network Services. International 
Journal of Contents. 2012;8: 1–6. 
115. 
Avey AE. Function and Forms of Thought. Henry Holt and Company; 
1927. 
116. 
Advanced Distributed Learning. xAPI-Spec. 2017. Available: 
https://github.com/adlnet/xAPI-Spec 
117. 
Betts B. The Learning Technology Manager’s Guide to xAPI. HT2 Labs; 
2018. Available: https://www.ht2labs.com/xapi-guide-
download/#.WgHZmhNSzBI

## Page 46

Reimagining Maps 
 
 
43 
 
118. 
SCORM. SCORM Explained: In Depth Review of the SCORM eLearning 
Standard. 2004. Available: https://scorm.com/scorm-
explained/?utm_source=google&utm_medium=natural_search 
119. 
IEEE. IEEE 1484.12.1-2002 - IEEE Standard for Learning Object 
Metadata. 2002. Available: 
https://standards.ieee.org/standard/1484_12_1-2002.html 
120. 
Cordes RJ, Murphy S. Education and Heuristic Discovery Market 
Analysis. COGSEC; 2019 May. 
121. 
Mikhailova A, Friedman DA. Partner Pen Play in Parallel (PPPiP): A New 
PPPiParadigm for Relationship Improvement. Arts Health. 2018;7: 39. 
122. 
Cordes RJ. DARPA Initiatives in Focus: Heuristic Data and Third Wave 
AI. COGSEC; 2019 Apr. Report No.: COGSEC-DIF-10.19 / TASK 002. 
Available: https://cordes-rj.github.io/pubs/COGSEC_DIF_1_19.pdf 
123. 
Cordes RJ. Problems Unsolved: Incomplete Military and USG Research 
Initiatives on Education, Heuristic Discovery, and NextGen AI. COGSEC; 
2019 Apr. Report No.: COGSEC-PU.EHDAI-3.4 / Task 002. 
124. 
Wiens JJ, Donoghue MJ. Historical biogeography, ecology and species 
richness. Trends Ecol Evol. 2004;19: 639–644. 
125. 
Martínez-Harms MJ, Quijas S, Merenlender AM, Balvanera P. Enhancing 
ecosystem services maps combining field and environmental data. 
Ecosystem Services. 2016;22: 32–40. 
126. 
Westneat DF. Behavioral ecology: 40 years of fusion with ecology. 
Behav Ecol. 2011;22: 234–235. 
127. 
Gordon DM. The ecology of collective behavior. PLoS Biol. 2014;12: 
e1001805. 
128. 
Simon D. Biogeography-Based Optimization. IEEE Trans Evol Comput. 
2008;12: 702–713.

## Page 47

Reimagining Maps 
 
 
44 
 
129. 
Larkin AA, Martiny AC. Microdiversity shapes the traits, niche space, 
and biogeography of microbial taxa. Environ Microbiol Rep. 2017;9: 55–
70. 
130. 
Hajima T, Kawamiya M, Watanabe M, Kato E, Tachiiri K, Sugiyama M, et 
al. Modeling in Earth system science up to and beyond IPCC AR5. 
Progress in Earth and Planetary Science. 2014;1: 29. 
131. 
Benton TG, Solan M, Travis JMJ, Sait SM. Microcosm experiments can 
inform global ecological problems. Trends Ecol Evol. 2007;22: 516–521. 
132. 
Tang W, Davidson JD, Zhang G, Conen KE, Fang J, Serluca F, et al. 
Genetic Control of Collective Behavior in Zebrafish. iScience. 2020;23: 
100942. 
133. 
Friedman DA, Johnson BR, Linksvayer TA. Distributed physiology and 
the molecular basis of social life in eusocial insects. Horm Behav. 2020; 
104757. 
134. 
Baedke J. The epigenetic landscape in the course of time: Conrad Hal 
Waddington’s methodological impact on the life sciences. Studies in 
History and Philosophy of Science Part C: Studies in History and 
Philosophy of Biological and Biomedical Sciences. 2013;44: 756–773. 
135. 
Pigliucci M. Genotype-phenotype mapping and the end of the “genes as 
blueprint” metaphor. Philos Trans R Soc Lond B Biol Sci. 2010;365: 
557–566. 
136. 
Orgogozo V, Morizot B, Martin A. The differential view of genotype-
phenotype relationships. Front Genet. 2015;6: 179. 
137. 
Erwin DH. The topology of evolutionary novelty and innovation in 
macroevolution. Philos Trans R Soc Lond B Biol Sci. 2017;372: 
20160422. 
138. 
Hwang S, Park S-C, Krug J. Genotypic Complexity of Fisher’s Geometric 
Model. Genetics. 2017;206: 1049–1079.

## Page 48

Reimagining Maps 
 
 
45 
 
139. 
Fraïsse C, Gunnarsson PA, Roze D, Bierne N, Welch JJ. The genetics of 
speciation: Insights from Fisher’s geometric model. Evolution. 2016;70: 
1450–1464. 
140. 
Longino HE. Studying Human Behavior. In: University of Chicago Press 
[Internet]. pu3430623_3430810; Jan 2013 [cited 11 Dec 2017]. 
Available: 
http://www.press.uchicago.edu/ucp/books/book/chicago/S/bo13025491.
html 
141. 
Winther RG. Mapping the Deep Blue Oceans. In: Tambassi T, editor. The 
Philosophy of GIS. Cham: Springer International Publishing; 2019. pp. 
99–123. 
142. 
Weisstein EW. Map. In: mathworld.wolfram.com [Internet]. Wolfram 
Research, Inc.; [cited 26 Oct 2020]. Available: 
https://mathworld.wolfram.com/Map.html 
143. 
Arfken GB, Weber HJ, Harris FE. Mathematical Methods for Physicists, 
7th edition. Academic Press; 2013. 
144. 
Rampasek L, Goldenberg A. TensorFlow: Biology’s Gateway to Deep 
Learning? Cell Syst. 2016;2: 12–14. 
145. 
Latorre M, Montáns FJ. Stress and strain mapping tensors and general 
work-conjugacy in large strain continuum mechanics. Appl Math Model. 
2016;40: 3938–3950. 
146. 
Leike J. What is AIXI? In: jan.leike.name [Internet]. 2015 [cited 26 Oct 
2020]. Available: https://jan.leike.name/AIXI.html 
147. 
Hutter M. Universal Artificial Intelligence: Sequential Decisions Based 
on Algorithmic Probability. Springer Science & Business Media; 2004. 
148. 
Rouse M. Definition of Cryptology. In: searchsecurity.techtarget.com 
[Internet]. TechTarget; 21 Sep 2005 [cited 26 Oct 2020]. Available: 
https://searchsecurity.techtarget.com/definition/cryptology 
149. 
Vaudenay S. A Classical Introduction to Cryptography: Applications for 
Communications Security. Springer Science & Business Media; 2005.

## Page 49

Reimagining Maps 
 
 
46 
 
150. 
Muter EM, Maher CA. Recognizing isomorphism and building proof: 
Revisiting earlier ideas. Proceedings of the twentieth annual meeting of 
the North American Chapter of the International Group for the 
Psychology of Mathematics Education. 1998. pp. 461–467. 
151. 
Maher CA, Powell AB, Uptegrove EB. Combinatorics and Reasoning: 
Representing, Justifying and Building Isomorphisms. Springer Science 
& Business Media; 2010. 
152. 
Goerss PG, Jardine JF. Simplicial functors and homotopy coherence. 
Simplicial Homotopy Theory. 2009; 431–462. 
153. 
Goerss PG, Jardine JF. Simplicial Homotopy Theory. Birkhäuser; 2012. 
154. 
Ramzy I, Arora A. Using Zero Knowledge to Share a Little Knowledge: 
Bootstrapping Trust in Device Networks. Stabilization, Safety, and 
Security of Distributed Systems. Springer Berlin Heidelberg; 2011. pp. 
371–385. 
155. 
Bowe S, Gabizon A, Green MD. A Multi-party Protocol for Constructing 
the Public Parameters of the Pinocchio zk-SNARK. Financial 
Cryptography and Data Security. Springer Berlin Heidelberg; 2019. pp. 
64–77. 
156. 
Barta O, Ishai Y, Ostrovsky R, Wu DJ. On Succinct Arguments and 
Witness Encryption from Groups. Advances in Cryptology – CRYPTO 
2020. Springer International Publishing; 2020. pp. 776–806. 
157. 
Defence and Security Accelerator. Competition document: Map the Gap: 
autonomous gap survey crossing. In: gov.uk [Internet]. Mar 2020 [cited 
27 Oct 2020]. Available: 
https://www.gov.uk/government/publications/competition-map-the-gap-
autonomous-gap-crossing-survey/competition-document-map-the-gap-
autonomous-gap-survey-crossing 
158. 
Jacobs co. Jacobs Helps Devise Semi-Autonomous Scouting System for 
British Army to “Map the Gap.” In: Jacobs.com [Internet]. 24 Aug 2020 
[cited 25 Sep 2020]. Available:

## Page 50

Reimagining Maps 
 
 
47 
 
https://www.jacobs.com/newsroom/news/jacobs-helps-devise-semi-
autonomous-scouting-system-british-army-map-gap 
159. 
US Department of the Army. ADP 3-0: Unified Land Operations. 2011. 
160. 
US Department of the Army. ADP 4-0: Sustainment. Washington, DC: 
Government Printing Office; 2019. 
161. 
U.S. Joint Chiefs of Staff. Joint Publication 3-0: Joint Operations. 
Washington, DC: Government Printing Office; 2017. Report No.: 3-0.


---
*Extraction method: pymupdf*
