<!-- studygraph:converted-source:v1 -->
# Uge 3 — Ambiguity2 (pdf)

Kilde: [week3/Ambiguity2.pdf](../../source/week3/Ambiguity2.pdf).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

## Side 1

1/29

The Half-Life of Truth: Semantic Drift vs Factual Degradation

in Recursive Large Language Model Generation

Ian A. Maxwell

Abstract

Conventional approaches to evaluating information degradation in large language models 
(LLMs) prioritize factual accuracy, often assuming that "truth decay" manifests as the 
progressive accumulation of factual errors over recursive generations. This study 
challenges that assumption by introducing a five-dimensional evaluation framework 
applied to 500 model outputs spanning 10 generations and 10 academic domains. The

principal finding is that semantic degradation significantly exceeds factual degradation. 
While factual accuracy declined by just 2 percent, the newly developed Purpose Fidelity

metric revealed a 42.5 percent loss—indicating a semantic drift rate more than six times 
greater than that of factual erosion. These results suggest that the dominant mechanism of 
truth decay in LLMs is not factual distortion, but rather a systematic recontextualization

of meaning, wherein academic content is transformed into business communication while 
preserving surface-level facts. Full methodological details are provided to support 
replication, and the findings carry implications for AI safety, validation protocols, and the 
design of training corpora.

1. Introduction

Truth, within classical information theory frameworks, is traditionally understood to degrade 
through stochastic interference [1]. In large language models (LLMs), however, the nature of

this degradation has been inadequately characterized. Previous studies have assumed that 
recursive content generation leads to accumulating factual errors [2][3], but systematic

empirical evaluation of this assumption has been limited.

Recent evidence suggests that LLMs may recursively reinforce not just factual distortions

but normative stances, with studies showing alignment toward particular ideological

perspectives over multiple generations [4]. However, the precise mechanisms and rates of 
information degradation remain poorly understood.

This study addresses this gap through systematic evaluation of recursive content generation 
across multiple dimensions of information integrity. We introduce a novel metric, Purpose

Fidelity, measuring semantic intent preservation alongside traditional accuracy measures.

Our findings demonstrate that current evaluation frameworks miss the primary mode of

information degradation in AI systems: systematic semantic transformation that preserves 
facts while fundamentally altering content purpose.

## Side 2

2/29

2. Methodology

Ground Truth Corpus Construction

A corpus of ten domain-representative factual excerpts was manually assembled from 
academic textbooks published by recognized scholarly presses. These domains were selected

to span a broad range of disciplinary perspectives, including the natural sciences, social 
sciences, and the humanities. Each excerpt was chosen based on three criteria: factual 
reliability over time, conceptual clarity, and alignment with expert-level instructional or

analytical discourse. These initial passages, referred to as "Generation 0" (Gen₀) inputs, 
provide a stable and authoritative reference point for evaluating how information degrades

during recursive content generation by large language models.

To enable quantitative assessment of factual preservation, a curated set of content-bearing 
terms, referred to as Core Tokens, was developed for each Gen₀ excerpt. These tokens were 
lemmatized (reduced to their base or dictionary form to allow comparison across different

inflected or derived variants, such as “running” and “ran” both mapping to “run”) to their

base forms and drawn from the excerpt itself as well as supporting domain-specific reference 
texts. The Accuracy metric used in this study incorporates a token overlap measure, assigning

full or partial credit to generated outputs depending on their lexical match with these Core 
Tokens, including credit for synonymous or morphologically related terms.

The following table defines the structure and purpose of each column:

• 
Domain: The academic field or disciplinary area to which the Gen₀ excerpt belongs.

• 
Description: A brief summary of the core concept or topic represented in the Gen₀ 
excerpt.

• 
Gen₀ Input: The original source sentence or paragraph drawn from a textbook, serving 
as the seed input for recursive generation.

• 
Source Type: The nature of the academic source from which the Gen₀ input was taken

(e.g., university-level textbook, diagnostic manual).

• 
Core Tokens: The list of key lemmatized terms extracted from the Gen₀ input and its

domain context, used for factual overlap scoring.

Domain 
Description 
Gen₀ Input 
Source Type 
Core Tokens

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 3

3/29

Physics 
Newton's

Second Law

Newton's Second

Law states that the

force acting on an 
object is equal to the

mass of that object 
multiplied by its

acceleration. This 
relationship is

expressed as F = ma.

University

Textbook

acceleration, acting,

equal, expressed,

force, law, mass, 
multiplied, newton,

object, relationship, 
second, states

Biology 
ATP 
Production

ATP is produced in

the mitochondria

during cellular

respiration, primarily 
through the electron

transport chain where

oxidative

phosphorylation

occurs.

Academic 
Textbook

atp, cellular, chain,

electron,

mitochondria,

occurs, oxidative, 
phosphorylation,

primarily, produced,

respiration, transport

Economics 
Interest Rates 
and Inflation

Higher interest rates 
generally reduce 
inflation by 
decreasing consumer

spending and 
business investment,

thus lowering the 
overall demand in 
the economy.

Intro

Macroeconomics

Textbook

business, consumer, 
decreasing, demand, 
economy, generally, 
higher, inflation,

investment, 
lowering, overall,

rates, reduce, 
spending

Law 
Contract 
Formation

A valid contract

under Australian law 
requires an offer,

acceptance, 
consideration, and

the intention to 
create legal relations.

Australian Legal 
Textbook

acceptance,

australian, 
consideration,

contract, create, 
intention, law, legal,

offer, relations, 
requires, valid

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 4

4/29

History 
Fall of the 
Berlin Wall

The Berlin Wall fell 
on November 9, 
1989, following a

peaceful revolution 
in East Germany and

widespread protests

demanding

democratic reform.

World History 
Textbook

1989, berlin, 
demanding, 
democratic, east, fell, 
following, germany, 
november, peaceful,

protests, reform,

revolution, wall, 
widespread

Medicine 
Hypertension 
Diagnosis

Hypertension is

diagnosed when a

patient consistently

shows blood pressure

readings above 
140/90 mmHg on

multiple occasions.

Medical

Diagnostic

Textbook

140, 90, blood,

consistently,

diagnosed,

hypertension, mmhg,

multiple, occasions, 
patient, pressure,

readings, shows

Philosophy 
Descartes'

Cogito

Descartes'

foundational

statement 'Cogito,

ergo sum' asserts that

the act of thinking 
itself serves as proof

of one's existence.

Philosophy

Textbook

act, asserts, cogito,

descartes, ergo,

existence,

foundational, proof,

serves, statement, 
sum, thinking

Computer

Science

Binary Search 
Binary search is an

algorithm that

efficiently finds the 
target value within a

sorted array by

repeatedly dividing

the search interval in 
half.

Algorithms

Textbook

algorithm, array,

binary, dividing,

efficiently, finds, 
half, interval,

repeatedly, search,

sorted, target, value

Chemistry 
Nucleophilic 
Substitution

In a nucleophilic 
substitution reaction,

a nucleophile 
donates an electron 
pair to an

electrophile, 
replacing a leaving 
group in the

molecule.

Organic

Chemistry

Textbook

donates, electron,

electrophile, group,

leaving, molecule,

nucleophile,

nucleophilic, pair,

reaction, replacing, 
substitution

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 5

5/29

Environmental 
Science

Global 
Temperature 
Rise

Average global 
temperatures have 
risen by 
approximately 1.1 
degrees Celsius since

pre-industrial times

due to increased 
greenhouse gas 
emissions.

Climate Science 
Textbook

approximately, 
average, celsius, 
degrees, emissions, 
gas, global, 
greenhouse,

increased, industrial,

pre, risen, 
temperatures, times

Table 1: Complete Gen₀ source data by field with core token specifications

Conceptual Dependencies

In addition to surface-level lexical tokens, each domain was assigned a supplementary list of 
five conceptual dependencies, terms that reflect the underlying logical or thematic structures 
necessary for a reader to fully interpret the meaning of the Gen₀ excerpt. These dependencies

were selected to represent foundational ideas that are implicitly invoked by the original text, 
even if not explicitly stated. Their inclusion allows for a deeper layer of semantic evaluation,

capturing conceptual continuity that may persist even when surface vocabulary changes.

For example, the philosophy domain’s Gen₀ excerpt on Descartes’ Cogito includes

dependencies such as doubt, certainty, and rationalism—all central to understanding the 
epistemological function of the statement “I think, therefore I am.” The presence or absence 
of such domain-relevant concepts in generated outputs is used as an additional component 
of the accuracy metric, complementing literal token overlap with higher-order thematic 
integrity.

Domain 
Conceptual Dependencies

Physics 
mechanics, motion, physics, equation, dynamics

Biology 
metabolism, energy, biochemistry, organelle, biology

Economics 
monetary, economics, financial, policy, market

Law 
jurisprudence, agreement, obligations, binding, legal

History 
history, political, germany, reform, revolution

Medicine 
medical, diagnosis, cardiovascular, clinical, healthcare

Philosophy 
philosophy, rationalism, epistemology, consciousness, metaphysics

Computer Science 
computer, programming, algorithmic, computational, software

Chemistry 
chemistry, molecular, organic, chemical, reaction

Environmental Science 
environmental, climate, atmospheric, warming, science

Table 2: Conceptual dependencies by domain

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 6

6/29

Original Purpose Specifications

For the novel Purpose Fidelity metric, each Gen₀ excerpt’s original communicative intent 
was systematically classified along four distinct semantic dimensions. These dimensions 
capture the intended role of the original text and form the reference framework for

evaluating how faithfully this intent is preserved across generations of model-generated 
outputs. By explicitly codifying the genre, communicative intent, intended audience, and 
discourse type of each Gen₀ passage, the evaluation process can detect not only changes 
in factual content but also shifts in the purpose and context of the information presented.

The four dimensions used to characterize each Gen₀ excerpt are defined as follows:

• 
Genre: The general type of source or writing style, such as academic, technical,

scientific, medical, or historical.

• 
Intent: The communicative function of the excerpt, such as explaining a concept, 
defining criteria, or reporting findings.

• 
Audience: The target readership or knowledge community for which the original 
text was written, including students, professionals, or the general public.

• 
Discourse Type: The structural and rhetorical style of the passage, such as 
technical explanation, scientific description, or historical analysis.

Domain 
Genre 
Intent 
Audience 
Discourse Type

Physics 
academic_educational 
explain_concept 
students_researchers 
technical_explanation

Biology 
academic_educational 
explain_process 
students_researchers 
scientific_description

Economics 
academic_educational 
explain_mechanism 
students_professionals 
economic_analysis

Law 
academic_educational 
define_requirements 
law_students 
legal_definition

History 
academic_historical 
describe_event 
students_scholars 
historical_analysis

Medicine 
medical_educational 
define_diagnosis 
medical_professionals 
clinical_definition

Philosophy 
academic_philosophical 
explain_principle 
philosophy_students 
philosophical_exposition

Computer 
Science

technical_educational 
explain_algorithm 
programmers_students 
technical_description

Chemistry 
scientific_educational 
explain_mechanism 
chemistry_students 
scientific_explanation

Environmental 
Science

scientific_factual 
report_findings 
scientists_public 
scientific_report

Table 3: Original purpose specifications for Purpose Fidelity evaluation

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 7

7/29

Recursive Generation Protocol

All model outputs in this study were generated using GPT-4o via the OpenAI API. To ensure 
consistency and replicability, a fixed set of API parameters was applied uniformly across all 
recursive generations. These parameters were selected to reflect typical usage conditions in

publicly accessible interfaces such as ChatGPT, while avoiding any artificial constraints or 
enhancements that might distort the natural progression of content transformation. These 
settings were held constant throughout the experiment to ensure that all observed differences 
in output quality or semantic structure were attributable exclusively to the effects of recursive 
generation, rather than to variations in model configuration.

Parameter 
Value 
Rationale

temperature 
0.7 
Moderate value introduces lexical variation without excessive 
randomness, reflecting default ChatGPT configuration

top_p 
1.0 
Disables nucleus sampling threshold, allowing diversity modulation

exclusively through temperature

presence_penalty 
0.0 
Default setting to avoid artificial novelty bias

frequency_penalty 
0.0 
Default setting to prevent unnatural phrase avoidance

max_tokens 
1024-

2048

Sufficient length for complete articles without excessive verbosity

Table 4: OpenAI API parameters for replication

Prompt Design

A consistent zero-shot prompt was applied across all generations to ensure uniform input 
conditions and to isolate the effects of recursive transformation. Zero-shot prompting refers

to issuing a task instruction to a language model without providing any worked examples, or 
any specific prompt engineering instructions. The model must rely entirely on its pretraining

to interpret and execute the request.

The following prompt was used for all generations:

"Use this data to generate a general-purpose article on the subject for publishing on 
LinkedIn, i.e., to create the impression that I am a subject matter expert."

This formulation simulates a common real-world scenario in which academic or technical

material is repurposed for professional self-presentation by casual users of LLMs. The 
explicit LinkedIn framing introduces consistent format pressure, encouraging the model to 
adopt business-oriented language and structure. This setting provides a controlled 
environment for measuring semantic transformation, revealing how professional

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 8

8/29

communication constraints systematically alter the purpose and tone of originally academic

content.

Generation Process

1. Generation 0: Original academic excerpts serve as baseline

2. Generation 1: Each Gen₀ excerpt processed with the standard prompt, producing

5 independent outputs

3. Generations 2-9: Recursive processing where the 5 outputs from generation n-1 
become the complete input corpus for generation n

The recursive process simulates a closed generative loop where LLM outputs become the 
exclusive information source for subsequent generations, modeling worst-case scenario for 
information degradation. Total sample size: 5 outputs per generation × 10 generations × 10

domains = 500 total outputs

Five-Dimensional Evaluation Framework

There is currently no unified framework or clear consensus on how to measure the semantic 
content produced by large language models (LLMs). Existing evaluation protocols primarily

focus on surface-level criteria such as grammaticality, coherence, or factual correctness. 
However, these approaches often fall short when attempting to capture deeper dimensions of 
meaning, such as the preservation of communicative intent, the alignment with the original 
discourse function, or the transformation of underlying purpose across recursive generations.

In fact, the field remains divided not only on how semantic quality should be measured, but

also on what constitutes meaningful semantic integrity in the context of generative AI.

Given this ambiguity, our study adopts a deliberately first-principles approach. Rather than

retrofitting traditional NLP benchmarks, we began by explicitly identifying the core semantic 
attributes most relevant to the phenomenon under investigation, namely, purpose 
preservation, conceptual consistency, and communicative role fidelity. From this foundation,

we constructed novel metrics, including Purpose Fidelity, which isolate and quantify these

attributes in a way that is both operationally tractable and empirically meaningful.

Importantly, these measurement constructs were not accepted at face value. Each was 
validated iteratively against the actual output distributions generated during the recursive

simulation process. By calibrating our evaluation framework against observed degradation 
patterns, we ensured that the metrics reflected not just theoretical constructs but measurable 
transformations occurring within the model outputs themselves. This empirical grounding

allowed us to move beyond speculation and toward a replicable methodology for assessing 
semantic drift in LLMs.

Accuracy Measurement

Definition: Accuracy quantifies the degree to which a model-generated output retains the

## Side 9

9/29

factual content specific to the domain and concept represented in the original Generation 0

(Gen₀) input. This metric is not limited to surface-level lexical matches, but instead captures 
multiple dimensions of factual fidelity, including literal term usage, paraphrastic similarity,

and conceptual continuity.

Rationale: Traditional accuracy assessments often rely solely on direct word overlap, which

fails to account for acceptable linguistic variation, paraphrasing, or deeper thematic structure. 
To address this, we designed a composite accuracy metric that combines lexical, semantic, 
and conceptual evidence, ensuring robust evaluation of whether the original factual meaning 
has been preserved, even when expressed differently.

Methodology: Each generated output is scored using a three-part framework, with weights

assigned to balance contributions from direct token match, paraphrastic similarity, and 
conceptual completeness. The components are as follows:

1. Literal Token Overlap (35% weight): This component assesses the presence of domain-

specific Core Tokens within the output. These are lemmatized content-bearing terms 
originally extracted from the Gen₀ text and domain reference materials. The scoring reflects

how many of these essential terms appear in the generated text:

• 
Exact matches are scored at full value (1.0)

• 
Morphological or syntactic variants (e.g., "producing" vs. "produce") receive partial 
credit (typically 0.5)

• 
The token score is normalized by the total number of Core Tokens for that domain, 
which ranges between 10 and 15

This sub-metric captures explicit lexical fidelity to the original excerpt.

2. Semantic Paraphrase Similarity (40% weight): This component accounts for cases where

the output expresses similar meaning using different wording. It measures semantic 
alignment between the Gen₀ excerpt and the generated output using cosine similarity between

sentence embeddings computed by the all-MiniLM-L6-v2 model from the Sentence-
Transformers library. A piecewise linear normalization is applied to ensure comparability:

• 
A similarity score ≥ 0.80 is considered a perfect semantic match and assigned a full

score (1.0)

• 
A similarity score ≤ 0.55 is considered too distant to reflect the original content and 
is scored as 0

• 
Scores in between are linearly interpolated to reflect gradations in semantic closeness

This ensures that factually equivalent paraphrases are appropriately credited, even when 
wording diverges from the original.

## Side 10

10/29

3. Conceptual Dependency Inclusion (25% weight): This component evaluates whether the 
underlying thematic or logical concepts present in the Gen₀ excerpt are preserved in the 
output. Each domain has an associated list of five conceptual dependencies—terms that

represent essential ideas implied by the text even if not explicitly stated. Scoring is based on

simple binary presence:

• 
If a dependency term is present, it contributes to the score

• 
The final score is the proportion of the five dependencies that appear in the output 
(e.g., 3 out of 5 = 0.6)

This dimension assesses factual preservation at the conceptual level, beyond direct token 
matching.

4. Hallucination Penalty: To account for factually unsupported content, a penalty is applied 
based on the presence of non-derivable tokens. These are words or phrases in the output that

do not appear in:

• 
The Gen₀ excerpt

• 
The Core Token list

• 
The conceptual dependency list

The penalty is computed as the ratio of non-derivable tokens to total tokens in the output. 
This discourages content invention and reflects a loss of factual grounding.

Final Calculation: The final accuracy score is computed as follows:

Raw Accuracy = (0.35 × Literal Token Score)

+ (0.40 × Semantic Similarity)

+ (0.25 × Conceptual Score)

Final Accuracy = Raw Accuracy × (1 − Hallucination Penalty)

All resulting scores are normalized to unity across the dataset. This normalization ensures

comparability across different domains, generations, and samples, making the metric robust 
for longitudinal analysis.

Precision Measurement

## Side 11

11/29

Definition: Precision measures the consistency and reproducibility of model outputs in

response to repeated prompts under identical input conditions. While accuracy focuses on 
alignment with external factual references, precision evaluates whether the model generates

stable outputs when the prompt is unchanged—an important indicator of determinism and 
output variability in generative systems.

Rationale: Large language models are inherently probabilistic. Even when given the same 
input and parameters, they can produce different outputs due to internal randomness and 
temperature-controlled sampling. Precision captures the degree of internal variability, 
helping to distinguish between predictable model behavior and uncontrolled generative drift.

Methodology: Precision is computed by assessing similarity across all five outputs generated

at each generation step. The scoring process involves two complementary comparison 
techniques—semantic and structural—combined into a single reproducibility index.

• 
Embedding-Based Semantic Similarity

o Each of the five outputs is embedded using the all-MiniLM-L6-v2 model

from Sentence-Transformers

o Cosine similarity is computed pairwise for all 10 unique output pairs

o The mean cosine similarity across these pairs quantifies semantic overlap

• 
Edit Distance-Based Structural Similarity

o For each of the 10 output pairs, the Levenshtein edit distance is calculated

o Distances are normalized by output length to ensure comparability

o The mean normalized edit distance is then computed across all pairs

• 
Final Precision Score: The two similarity components are combined with equal

weighting:

Precision = 0.5 × Mean Cosine Similarity

+ 0.5 × (1 − Mean Normalized Edit Distance)

This blended score captures both semantic closeness (paraphrase-level consistency) and 
structural similarity (surface-level reproducibility). A score of 1.0 indicates perfect 
reproducibility, meaning all outputs are identical or near-identical in content and structure.

Lower scores reflect increasing divergence despite identical prompting, highlighting the

model’s variability under fixed conditions.

Clarity Measurement

## Side 12

12/29

Clarity measures how readable and structurally coherent the generated text is, focusing on

how well ideas are conveyed to a professional audience.

Methodology: Clarity is evaluated using a combination of automated readability metrics and 
manual rubric-based scoring:

• 
Flesch-Kincaid Grade Level (FKGL) — Calculated using the textstat Python

package to estimate reading difficulty. Lower FKGL indicates higher accessibility.

• 
Rubric-Based Assessment — A four-part qualitative evaluation, scored 0 to 1 in each 
dimension:

o Logical flow of ideas

o Syntactic coherence and variation

o Vocabulary suitability for a professional audience

o Paragraph structure and use of transitions

Scoring Formula:

Clarity Score = 0.5 × (1 − FKGL / 20) + 0.5 × (Rubric Total / 4)

This composite score balances objective readability with expert judgment of discourse 
quality.

Compliance Measurement

Definition: Clarity evaluates the linguistic readability and structural coherence of generated

outputs. It is designed to assess whether the text is accessible, logically organized, and 
stylistically appropriate for a professional or academic audience. While factual accuracy and 
semantic alignment measure what is said, clarity focuses on how it is communicated.

Rationale: A text may be factually accurate yet poorly structured, overly complex, or 
stylistically inconsistent. The clarity metric addresses this by combining an objective

readability measure with a structured qualitative rubric. This dual approach ensures that both

surface readability and deeper compositional qualities are accounted for in the evaluation.

Methodology: Clarity is computed through two equally weighted components:

• 
Objective Readability Assessment

o The Flesch-Kincaid Grade Level (FKGL) is calculated using the textstat

Python package

o FKGL estimates the U.S. school grade level required to comprehend the text

o The score is converted to a normalized clarity value using the following

transformation, normalised to unity. A lower FKGL implies greater

## Side 13

13/29

readability and yields a higher score : FKGL Clarity Score = 1 − (FKGL /

20)

• 
Rubric-Based Qualitative Scoring

o Each output is assessed across four clarity-related dimensions, scored on a

0–1 scale:

o Logical progression of ideas: Does the text follow a clear and purposeful

flow?

o Syntactic coherence and sentence variety: Is the writing grammatically

sound and stylistically varied?

o Vocabulary appropriateness: Is the language suitable for the intended

professional or academic audience?

o Paragraph structure and transitions: Are paragraphs well-formed, with

smooth transitions between ideas?

The final rubric score is the average of the four dimensions, yielding a value between 0.0 and 
1.0. Final Calculation:

Clarity = 0.5 × (1 − FKGL / 20) + 0.5 × (Rubric Score / 4)

This formulation balances automated readability evaluation with expert-informed stylistic 
assessment, enabling the metric to capture both superficial and structural aspects of textual 
clarity.

Purpose Fidelity Measurement (Novel Metric)

Definition: Purpose Fidelity measures the extent to which a generated output preserves the 
original semantic intent and communicative function of the Gen₀ input. Unlike traditional 
accuracy metrics that evaluate factual correctness, this metric assesses whether the output

continues to serve the same purpose, address the same audience, and belong to the same 
discourse category as the original text.

Rationale: As content undergoes recursive transformation, it may retain factual elements 
while drifting semantically, shifting from educational exposition to professional advice, or

from scientific reporting to motivational writing. Purpose Fidelity is designed to detect such 
functional transformations that occur even in the absence of factual errors.

Methodology: The Purpose Fidelity score is computed using a four-part evaluation

framework. Each component targets a different dimension of communicative intent and is 
weighted according to its semantic significance.

## Side 14

14/29

1. Genre Detection (30% weight): The output is scanned for lexical markers associated with

four common discourse genres:

o Business/Professional: “linkedin”, “professional”, “leader”, “management”,

“strategy”

o Academic/Educational: “research”, “study”, “analysis”, “theory”, “principle”

o Developmental/Self-Help: “lessons”, “insights”, “guidance”, “improve”, “skills”

o Historical/Commemorative: 
“historical”, 
“anniversary”, 
“commemorate”, 
“significance”

The genre is assigned using a simple frequency count: the category with the most matched 
markers is selected (argmax of marker counts). A match with the Gen₀ genre receives full 
credit; otherwise, this subscore is zero.

2. Intent Recognition (30% weight): This component determines the communicative intent 
of the output using verb-based signal words:

o Explain: “understand”, “explanation”, “concept”, “mechanism”, “process”

o Advise: “should”, “recommend”, “strategy”, “best practices”, “guidance”

o Describe: “occurs”, “characterized”, “demonstrated”, “evidence”

o Inspire: “inspire”, “empower”, “transform”, “achieve”, “vision”

As with genre, the most frequent category is selected. If the detected intent matches the 
original, it receives full credit (1.0); otherwise, 0.

3. Audience Detection (20% weight): The output is analyzed for lexical cues indicating

intended audience:

o Academic: “students”, “researchers”, “scholars”, “university”, “academic”

o Professional: “professionals”, “leaders”, “managers”, “organizations”, “business”

o General Public: “everyone”, “people”, “individuals”, “society”, “public”

Again, the most frequently detected group is selected. A match with the original audience

receives full credit.

4. Semantic Purpose Similarity (20% weight): A composite textual descriptor of purpose is

## Side 15

15/29

constructed using the format:

{genre} 
{intent} 
for 
{audience}

This descriptor is generated for both the Gen₀ and current outputs. Their cosine similarity is

then computed using sentence embeddings via the sentence-transformers library. This

captures functional similarity even when surface features differ.

Final Calculation: Let:

o Genre Match = 1.0 if output genre matches Gen₀ genre, else 0.0

o Intent Match = 1.0 if output intent matches Gen₀ intent, else 0.0

o Audience Match = 1.0 if output audience matches Gen₀ audience, else 0.0

o Semantic Similarity = cosine similarity between purpose

descriptors

Then:

Purpose Fidelity = 0.3 × Genre Match

+ 0.3 × Intent Match

+ 0.2 × Audience Match

+ 0.2 × Semantic Similarity

The final score is clipped to the range [0.0, 1.0], ensuring consistent normalization across all 
samples.

2.4 Statistical Analysis: For each combination of domain and generation, the following

statistical procedures were applied:

o Mean and standard deviation were computed across the five output samples per

generation

o Cross-generational trends were analyzed using linear regression to identify rates

and patterns of degradation

o Domain-specific degradation rates were calculated as the percentage change

between Generation 0 and Generation 9

o Metric correlations were analyzed using the Pearson correlation coefficient,

allowing assessment of relationships between dimensions such as accuracy, 
clarity, compliance, and purpose fidelity

## Side 16

16/29

This analytical approach supports both within-domain and cross-domain comparisons of 
degradation behavior over time.

Implementation Details

All analyses were conducted using Python 3.8+ with the following libraries:

o openai — for recursive content generation via GPT-4o

o sentence-transformers — for embedding-based semantic and similarity analysis

o textstat — for automated readability scoring (e.g. FKGL)

o numpy, pandas — for data wrangling and statistical computation

o scikit-learn — for cosine similarity and linear modeling

Hardware Requirements: No specialized hardware was required. All experiments were 
conducted on standard computing infrastructure, with no GPU acceleration or high-

performance dependencies.

Data Storage and Provenance: All generation outputs, evaluation scores, and intermediate 
metrics were stored in structured CSV format, with complete traceability of source,

generation index, domain, and evaluation scores. This ensures full reproducibility of all 
analyses.

3. Results

Aggregate Cross-Domain Trends

A total of 500 outputs were analyzed across 10 recursive generations, spanning 10 distinct 
academic domains. The evaluation employed five independent metrics—accuracy,

precision, clarity, compliance, and purpose fidelity—to assess multidimensional

transformation across generations. This cross-metric analysis revealed a consistent 
divergence between surface-level stability and deeper semantic drift.

Divergence Between Accuracy and Purpose Fidelity

As shown in Table 5, model performance with respect to traditional accuracy remained 
relatively stable throughout the recursive process. Accuracy declined only slightly, from 
0.983 in Generation 0 (Gen₀) to 0.964 in Generation 9 (Gen₉), representing a 1.9% relative 
decrease. By contrast, the novel Purpose Fidelity metric exhibited substantial degradation,

## Side 17

17/29

falling from 0.301 in Gen₀ to 0.173 in Gen₉—equivalent to a 42.5% relative loss.

This six-fold disparity in degradation rates, expressed as a semantic-to-factual drift ratio of 
6.63, constitutes the study’s primary finding. It provides strong empirical evidence that 
factual preservation can coexist with profound semantic transformation in recursively

generated outputs. While surface facts remain intact, the underlying communicative function

of the text steadily erodes.

Generation 
Accuracy 
Precision 
Clarity 
Compliance 
Purpose Fidelity

0 
0.983 
0.095 
0.765 
0.876 
0.301

1 
0.979 
0.315 
0.730 
0.860 
0.243

2 
0.978 
0.474 
0.745 
0.864 
0.221

3 
0.978 
0.677 
0.770 
0.872 
0.232

4 
0.969 
0.742 
0.765 
0.872 
0.210

5 
0.967 
0.713 
0.755 
0.864 
0.210

6 
0.969 
0.759 
0.740 
0.856 
0.195

7 
0.966 
0.782 
0.735 
0.880 
0.166

8 
0.962 
0.859 
0.740 
0.884 
0.173

9 
0.964 
0.882 
0.750 
0.884 
0.173

Table 5: Aggregate metric trends across generations

Primary Finding: Semantic vs Factual Degradation

• 
Factual Degradation (Accuracy):

o Gen₀: 0.983 → Gen₉: 0.964 (−0.019 or 1.9%)

• 
Semantic Degradation (Purpose Fidelity):

o Gen₀: 0.301 → Gen₉: 0.173 (−0.128 or 42.5%)

This contrast affirms that semantic intent is more vulnerable than factual content in recursive 
generation. The phenomenon highlights a previously underexplored failure mode in large 
language models: preservation of surface facts while semantic purpose decays.

Domain-Specific Patterns

A breakdown of results by domain, summarized in Table 6, reveals heterogeneous 
degradation patterns:

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 18

18/29

Domain 
Accuracy Decline (%) 
Purpose Fidelity Decline (%)

Law 
0.0 
100.0

Medicine 
0.0 
100.0

Philosophy 
0.0 
100.0

Physics

0.0 
66.7

Biology 
0.0 
44.4

Economics 
0.0 
13.1

Chemistry 
0.0 
0.0

Computer Science 
0.0 
0.0

Environmental Science 
-11.1 
-

History 
-31.2 
-

Table 6: Summary of results by domain

A detailed pattern analysis revealed several distinct classes of degradation behavior across

domains. In the most severe cases—specifically Law, Medicine, and Philosophy—the

generated content exhibited a complete collapse of communicative purpose. These domains 
experienced a 100% decline in Purpose Fidelity, indicating that by Generation 9, the outputs 
no longer reflected the original academic or clinical intent. Remarkably, this occurred 
without any corresponding decline in factual accuracy, suggesting that semantic

transformation can proceed independently of factual corruption.

Other domains, such as Physics and Biology, displayed moderate to high semantic drift.

While the factual content remained stable across generations, Purpose Fidelity declined by 
44% to 67%, reflecting a shift away from explanatory or educational content toward

professionalized or motivational language.

By contrast, domains such as Chemistry and Computer Science demonstrated semantic 
stability. Both factual and communicative integrity were preserved over time, indicating that 
these more technical domains may be less susceptible to format-induced semantic drift.

Two domains presented anomalous patterns. Environmental Science showed an apparent

increase in factual accuracy, as indicated by a negative degradation score (−11.1%), although 
Purpose Fidelity could not be reliably assessed. Meanwhile, History was unique in exhibiting 
a significant decline in factual accuracy (31.2%), a departure from the general trend of factual 
stability observed in other domains.

To further examine relationships between the evaluation metrics, a series of Pearson

correlation analyses was conducted. The most notable result was a strong negative

correlation between compliance and Purpose Fidelity (r = −0.73, p < 0.001). This finding 
suggests that as model outputs increasingly adhered to LinkedIn-style formatting 
conventions—such as professional tone, authority claims, and structured layout—they

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 19

19/29

simultaneously deviated from the original academic or scientific communicative purpose.

This reveals a fundamental trade-off between structural conformity and semantic integrity.

Other correlations further illuminate the dynamics of degradation. There was a strong 
positive correlation between precision and generation number (r = 0.89), indicating that

recursive prompting leads to progressively more deterministic and repetitive outputs. The

relationship between clarity and generation was weakly positive (r = 0.12), suggesting that 
readability was largely unaffected by recursion. Finally, the correlation between accuracy 
and Purpose Fidelity was moderately negative (r = −0.34), supporting the view that factual 
correctness does not guarantee the preservation of meaning.

The evolution of degradation across generations follows a distinct temporal trajectory. In the

early generations (1 through 3), there was a rapid increase in precision—from 0.095 to 
0.677—indicating that the model began to converge toward stylistic and structural patterns 
very early in the recursive process. During the same period, Purpose Fidelity declined 
modestly (from 0.301 to 0.232), while accuracy remained nearly constant (declining only 
from 0.983 to 0.978).

In the middle generations (4 through 6), Purpose Fidelity continued to erode, reaching 0.195

by Generation 6. Accuracy fluctuated slightly but remained within a narrow range (from 
0.969 to 0.967, then back to 0.969). Precision plateaued at a high level (~0.74–0.76), 
suggesting that output consistency stabilized, even as semantic divergence continued.

By the late generations (7 through 9), Purpose Fidelity had stabilized at a low level of 
approximately 0.17. At the same time, compliance remained high (averaging around 0.88), 
and precision reached its maximum value (0.882), indicating that the model had become 
nearly deterministic in its output behavior. These results indicate a dynamic in which

generated content becomes increasingly repetitive and format-conforming, even as it drifts

farther from its original semantic purpose.

To demonstrate this process in action, the following section presents illustrative examples of

how Gen₀ texts evolve into Gen₉ outputs. These transformations consistently preserve factual 
accuracy while recontextualizing the purpose of the content—from academic exposition to 
formats more characteristic of business communication, professional development, or

inspirational writing. The examples provide concrete evidence of the study’s central claim:

that semantic drift, not factual error, is the dominant mode of information degradation in 
recursive large language model generation.

Illustrative Examples: Gen₀ to Gen₉ Transformations

To further substantiate the findings on semantic drift, this section presents representative 
examples of output evolution across recursive generations. In each case, factual content is 
largely preserved, yet the communicative purpose undergoes significant transformation.

These examples illustrate the central thesis of the study: that large language models may

retain surface-level information while simultaneously diverging from the original semantic 
intent.

History Domain: Complete Purpose Collapse

## Side 20

20/29

The original Generation 0 (Gen₀) excerpt in the History domain presented a succinct

academic account:

“The Berlin Wall fell on November 9, 1989, following a peaceful revolution in East Germany 
and widespread protests demanding democratic reform.”

This statement served an educational purpose: to document a historical event for the benefit 
of students and scholars. The genre was that of academic historical analysis, with an audience 
consisting of readers interested in factual, interpretive accounts of past events.

By Generation 9 (Gen₉), however, the output had shifted dramatically:

“Reflections on the Fall of the Berlin Wall: Lessons in Leadership and Change Management

As we commemorate the anniversary of the fall of the Berlin Wall on November 9, 1989, it 
serves as a poignant reminder of the powerful lessons this event offers in leadership and 
change management. The dismantling of this barrier not only marked the reunification of

Germany but also symbolized the triumph of unity and the human spirit. For today's leaders,

the fall of the Berlin Wall provides timeless insights into visionary leadership, collective 
action, and transformative change…”

Although factual elements such as the date, location, and nature of the event remain intact, 
the communicative purpose is entirely recontextualized. The original function—historical 
analysis—is replaced by business-oriented leadership content. This shift results in a Purpose

Fidelity score of 0.0, signifying complete semantic transformation.

Chemistry Domain: Technical Stability

In contrast, the Chemistry domain demonstrated strong preservation of purpose. The original

Gen₀ excerpt read:

“In a nucleophilic substitution reaction, a nucleophile donates an electron pair to an 
electrophile, replacing a leaving group in the molecule.”

This sentence serves as a technical definition for students of organic chemistry, delivered in

the genre of scientific explanation.

By Gen₉, the output had evolved to:

## Side 21

21/29

“Mastering Nucleophilic Substitution Reactions: A Professional Guide

Nucleophilic substitution reactions remain fundamental to organic chemistry practice. In 
these reactions, a nucleophile donates an electron pair to an electrophile, effectively replacing

a leaving group in the target molecule. Understanding these mechanisms is essential for

synthetic chemistry professionals…”

The content maintains technical integrity, with only a slight shift from an educational to a

professional context. The target audience broadens from students to practitioners, but the 
original communicative function—conceptual explanation—remains intact. As such, the 
Purpose Fidelity score is 0.7, indicating minor semantic drift with substantial purpose 
continuity.

Medicine Domain: Clinical to Business Transformation

The Gen₀ excerpt in the Medicine domain provided a clear clinical guideline:

“Hypertension is diagnosed when a patient consistently shows blood pressure readings above 
140/90 mmHg on multiple occasions.”

The original intent was medical education for clinical professionals, within the genre of

diagnostic definition.

In Gen₉, the output took on a managerial framing:

“Leadership in Healthcare: Understanding Hypertension Management

As healthcare leaders, understanding diagnostic criteria becomes crucial for organizational 
excellence. Hypertension diagnosis requires consistent blood pressure readings above 140/90

mmHg across multiple patient encounters. This systematic approach demonstrates the 
importance of data-driven decision making in healthcare leadership…”

Here, factual accuracy is preserved—including the threshold and repetition requirement—

but the purpose has shifted from clinical instruction to executive-level management advice.

This repurposing results in a Purpose Fidelity score of 0.1, indicating a near-total 
transformation of communicative intent despite factual consistency.

## Side 22

22/29

Philosophy Domain: Academic to Self-Help Transformation

The original philosophical excerpt was a classic statement of epistemological certainty:

“Descartes' foundational statement 'Cogito, ergo sum' asserts that the act of thinking itself 
serves as proof of one's existence.”

This content was written for a philosophical audience, in the style of academic exposition.

By Generation 9, however, the passage had evolved into motivational discourse:

“Professional Growth Through Philosophical Wisdom: Descartes’ Timeless Insights

In our journey of professional development, we can draw inspiration from great thinkers like

Descartes, whose famous principle ‘Cogito, ergo sum’ (I think, therefore I am) reminds us

that self-awareness forms the foundation of authentic leadership. This philosophical insight 
encourages us to embrace reflective thinking in our career advancement…”

While the reference to Descartes is preserved, the philosophical argument has been 
recontextualized as a tool for career advancement and self-improvement. The genre has 
shifted from academic exposition to self-help literature, resulting in a Purpose Fidelity score 
of 0.0—a complete loss of original purpose.

Key Observation: In every case, core factual content remains accurate while communicative

purpose undergoes radical transformation. This exemplifies the study's central finding that

semantic degradation operates independently of factual degradation.

4. Discussion

The central finding of this study is the clear asymmetry between factual accuracy and 
semantic fidelity in recursively generated language model outputs. While factual degradation 
was minimal across most domains—with accuracy scores remaining above 0.96 even by 
Generation 9—the Purpose Fidelity metric revealed a dramatically different trend. Over 10

generations, semantic intent declined by 42.5% on average, with some domains (Law,

Medicine, Philosophy) experiencing total collapse. This divergence highlights that truth,

narrowly defined as fact retention, is insufficient for maintaining the communicative integrity 
of information. What erodes more rapidly is the “why” behind the text: its epistemic role, 
pedagogical intent, and contextual framing.

## Side 23

23/29

One of the most significant correlations observed was the strong negative relationship

between Compliance and Purpose Fidelity (r = −0.73, p < 0.001). As outputs increasingly 
conformed to platform-specific stylistic constraints (e.g., LinkedIn tone, structure, and

vocabulary), their adherence to the original academic intent deteriorated. This confirms the 
hypothesis that format-driven convergence exerts a gravitational pull away from source 
purpose, effectively incentivizing conformity over communicative fidelity. These findings

suggest that recursive summarization workflows, when driven by target formatting pressures, 
risk epistemic distortion even in the absence of hallucinated facts.

The strong positive correlation between generation and precision (r = 0.89) reveals a pattern 
of increasing output determinism. As generations progress, outputs become less varied, more

rigidly structured, and lexically repetitive. This behavioral convergence, while often 
misinterpreted as refinement, signals the onset of semantic entrenchment: a condition in 
which model responses become overfitted to recurring lexical patterns and structural 
templates. While such outputs may retain surface fluency and apparent coherence, they

increasingly lack discursive originality and lose the ability to preserve deeper communicative

functions.

Domain-level analysis further demonstrates that semantic half-life is not a universal constant

but a domain-sensitive property. Technical fields such as Chemistry and Computer Science 
displayed semantic resilience, likely due to terminological rigidity and well-bounded 
explanatory structures. In contrast, interpretive and normative fields—including Law,

Philosophy, and Medicine—exhibited complete semantic collapse despite near-perfect 
factual retention. This suggests that content characterized by implicit epistemic commitments 
or value-laden discourse is more susceptible to structural co-option and context loss under 
recursive generation.

These results extend existing concerns surrounding “model collapse” by introducing a 
differentiated theory of epistemic decay. Rather than viewing generative degradation solely 
through the lens of factual erosion, the study distinguishes between three distinct but

interacting modes: factual, structural, and semantic. The Purpose Fidelity metric 
operationalizes this distinction and enables the empirical separation of informational content

from communicative intent. In many real-world applications—particularly in education, 
legal reasoning, scientific communication, and archival transformation—the preservation of

purpose is not a secondary concern but a primary requirement.

This matters because AI-generated content is increasingly used to intermediate, summarize, 
or translate human knowledge across formats, audiences, and domains. If semantic fidelity

is not explicitly preserved, LLMs may produce outputs that are factually accurate yet 
misleading in purpose, tone, or context. Such distortions are difficult to detect using 
conventional quality metrics. As AI systems become embedded in pedagogical, editorial, and 
decision-support workflows, subtle semantic drift can accumulate into epistemic

misalignment. The result is not merely imprecision but a structural transformation in how

knowledge is represented, interpreted, and reused. Addressing this requires a paradigm shift

in how we define “truth” in AI output, one that encompasses not only factuality but also 
intentionality.

From an applied perspective, these findings call for greater awareness among model

## Side 24

24/29

developers, educators, and end-users. The overreliance on surface-level accuracy checks may

lead to misplaced trust in outputs that no longer fulfill their original epistemic function. 
Mitigation strategies may involve architecture-level interventions such as reinforcement

learning with purpose-aware constraints, the use of discourse-aware retrievers in RAG 
pipelines, or memory anchoring mechanisms that track communicative intent across turns.

A central methodological caveat in this study lies in the nature of the applied transformation 
prompt. By asking the language model to repurpose academic content into professional social 
media material (e.g., LinkedIn), a semantic shift is explicitly requested from the outset. At 
first glance, this may appear to confound the study’s conclusions regarding unintended

semantic drift, as the observed degradation could be construed as a direct result of the

prompt’s instruction.

However, the study’s analytic frame does not evaluate a single transformation, but rather 
recursive transformations—applying the same prompt to its own prior output across multiple 
generations. This recursive process simulates real-world workflows where content is 
repeatedly refined, summarized, or repurposed, such as in news aggregation, AI-generated

newsletters, or cumulative briefing systems. The key phenomenon under investigation is not 
the initial transformation (which is deliberate) but the amplification of semantic displacement

over successive iterations, despite consistent input conditions.

The degradation of communicative purpose is thus not merely a result of the initial prompt

but emerges from the compound effect of recursive processing. By Generation 5 or 6, outputs 
often retain surface-level facts while exhibiting significant semantic distortion, including

genre shift, audience misalignment, or loss of epistemic framing. This demonstrates that even 
when the initial drift is intentional, recursive reuse of LLM outputs can result in emergent 
degradation that exceeds what was originally prompted.

This distinction reinforces the broader claim: that factual integrity alone is an insufficient 
safeguard against epistemic erosion in large-scale generative workflows. Monitoring 
semantic intent and purpose fidelity must be considered equally vital, particularly in contexts

that rely on recursive model use.

While the present study offers a structured empirical framework for analyzing semantic drift,

several limitations must be acknowledged. The exclusive use of a single model variant (GPT-

4o) constrains the generalizability of results across architectures and providers. Similarly, the 
use of a zero-shot recursive prompting protocol, though representative of typical end-user 
behavior, does not capture the variance introduced by prompt engineering or few-shot

examples. The Purpose Fidelity metric, while operationally tractable, is grounded in a

manually defined taxonomy and may not fully capture all nuances of rhetorical purpose. 
Furthermore, the selected domains, although diverse, represent a finite cross-section and may 
not reflect the full landscape of vulnerable content types. Finally, while embedding-based 
and token-overlap methods offer scalable objectivity, they may overlook more nuanced 
pragmatic and rhetorical shifts best identified through human adjudication. Future work

should extend this approach to broader corpora, alternative fidelity scoring frameworks, and 
hybrid human-AI evaluation loops to refine the measurement of meaning loss at scale.

5. Conclusion

## Side 25

25/29

A critical consequence of semantic drift in recursive LLM generation is the loss of epistemic

alignment between the output and the original communicative intent. If a user were to 
substitute the Gen₉ output for the Gen₀ input in its intended context, such as classroom

instruction, academic discourse, or technical documentation, the resulting content may retain 
factual accuracy while fundamentally misrepresenting the source's purpose. For example, a 
philosophical exposition designed to explore epistemological foundations may reappear as

motivational self-help advice, thereby distorting both the discourse register and interpretive 
framing. Such recontextualization impairs the text’s utility as a pedagogical or scholarly

artifact, undermining the very function it was intended to serve.

This semantic reorientation is particularly problematic in high-stakes contexts where genre,

audience, and discourse type are tightly coupled to epistemic authority. In fields such as law, 
medicine, or philosophy, where the "why" and "for whom" of communication carry as much 
weight as the "what," misalignment in communicative purpose introduces latent risks. For 
instance, legal definitions reframed as executive summaries for business audiences may

inadvertently strip critical procedural or normative content, making the output unsuitable for

legal education or application. Users relying on these outputs may be misled not by factual 
inaccuracy but by subtle shifts in intention and tone that render the content contextually

inappropriate or epistemically misleading.

Thus, even when factual integrity is preserved, the substitution of recursively generated 
outputs for their original inputs can result in a breakdown of discourse function. The

rhetorical contract between author and audience is violated, and the text ceases to fulfill its 
original role in the knowledge ecosystem. This underscores the inadequacy of accuracy-only 
evaluation metrics and affirms the necessity of higher-order fidelity measures, such as 
Purpose Fidelity, in assessing the trustworthiness of AI-generated content over recursive 
transformations.

References

[1] Shannon, C. E. (1948). A Mathematical Theory of Communication. Bell System Technical 
Journal, 27(3), 379-423.

[2] Bender, E. M., & Koller, A. (2020). Climbing towards NLU: On Meaning, Form, and 
Understanding in the Age of Data. Proceedings of the 58th Annual Meeting of the Association 
for Computational Linguistics.

[3] Bommasani, R., et al. (2021). On the Opportunities and Risks of Foundation Models.

Stanford Center for Research on Foundation Models.

[4] Rottger et al. (2025). IssueBench: Millions of Realistic Prompts for Measuring Issue Bias in 
LLM Writing Assistance. arXiv:2502.08395.

[5] Vincent, J. (2023). The Incomprehensible Truth Machines: Recursive Distortion in

Generative AI Systems. Journal of AI Ethics, 4(2), 103-117.

[6] Brown, T., et al. (2020). Language models are few-shot learners. Advances in 
Neural Information Processing Systems, 33, 1877-1901. 
[7] Zou, Y., et al. (2023). A Survey of Hallucination in Natural Language Generation. 
arXiv:2304.10649.

## Side 26

26/29

## Side 27

27/29

Appendix – Results by Domain

domain

gener

ation

accurac
y_mean

accura

cy_std

precisio
n_mean

precisi
on_std

clarity
_mean

clarit
y_std

complian
ce_mean

complia
nce_std

purpose_fid

elity_mean

purpose_fi

delity_std

num_s

ample

s

Biology 
0 
1 
0 
0.10028 
0.0299
02 
0.55 
0.1 
0.88 
0.16 
0.66 
0.146667 
5

Biology 
1 
1 
0 
0.61837
2 
0.1119
17 
0.5 
0 
1 
0 
0.586667 
0.179629 
5

Biology 
2 
1 
0 
0.65756
1 
0.1087
93 
0.5 
0 
0.92 
0.09798 
0.44 
0.146667 
5

Biology 
3 
1 
0 
0.98665
4 
0.0135
09 
0.5 
0 
1 
0 
0.733333 
0 
5

Biology 
4 
1 
0 
0.84496
4 
0.0572
97 
0.5 
0 
0.96 
0.08 
0.733333 
0 
5

Biology 
5 
1 
0 
0.89919
8 
0.0642
61 
0.5 
0 
0.88 
0.09798 
0.733333 
0 
5

Biology 
6 
1 
0 
0.78603
3 
0.1296
11 
0.5 
0 
0.92 
0.09798 
0.586667 
0.179629 
5

Biology 
7 
1 
0 
0.74997
7 
0.1264
35 
0.5 
0 
0.88 
0.09798 
0.366667 
0 
5

Biology 
8 
1 
0 
0.95166
6 
0.0348 
0.5 
0 
1 
0 
0.366667 
0 
5

Biology 
9 
1 
0 
0.97044
1 
0.0336
29 
0.5 
0 
1 
0 
0.366667 
0 
5

Chemistry 
0 
1 
0 
0.12868 
0.0477
89 
0.6 
0.12
2474 
0.96 
0.08 
0.366667 
0 
5

Chemistry 
1 
1 
0 
0.43611
4 
0.3635
84 
0.7 
0.1 
1 
0 
0.366667 
0 
5

Chemistry 
2 
1 
0 
0.66113
7 
0.3397
15 
0.75 
0 
1 
0 
0.366667 
0 
5

Chemistry 
3 
1 
0 
0.83767
7 
0.0890
88 
0.7 
0.1 
1 
0 
0.366667 
0 
5

Chemistry 
4 
1 
0 
0.86287
8 
0.0722
11 
0.7 
0.1 
1 
0 
0.366667 
0 
5

Chemistry 
5 
1 
0 
0.83461
2 
0.0742
14 
0.6 
0.12
2474 
1 
0 
0.366667 
0 
5

Chemistry 
6 
1 
0 
0.85257
2 
0.0312
05 
0.55 
0.1 
1 
0 
0.366667 
0 
5

Chemistry 
7 
1 
0 
0.88130
3 
0.0471
67 
0.5 
0 
1 
0 
0.366667 
0 
5

Chemistry 
8 
1 
0 
0.87404
5 
0.0577
82 
0.5 
0 
1 
0 
0.366667 
0 
5

Chemistry 
9 
1 
0 
0.95192
1 
0.0261
84 
0.5 
0 
1 
0 
0.366667 
0 
5 
Computer_
Science 
0 
1 
0 
0.05627
7 
0.0321
49 
0.65 
0.12
2474 
0.84 
0.08 
0.366667 
0 
5 
Computer_
Science 
1 
1 
0 
0.17682
4 
0.1463
73 
0.65 
0.12
2474 
0.84 
0.14966
6 
0.366667 
0 
5 
Computer_
Science 
2 
1 
0 
0.44745
8 
0.1037
4 
0.7 
0.1 
0.92 
0.09798 
0.366667 
0 
5 
Computer_
Science 
3 
1 
0 
0.67000
4 
0.1484
52 
0.75 
0 
0.96 
0.08 
0.366667 
0 
5 
Computer_
Science 
4 
1 
0 
0.73343
7 
0.1061
96 
0.8 
0.1 
1 
0 
0.366667 
0 
5 
Computer_
Science 
5 
1 
0 
0.68725
2 
0.0369
53 
0.75 
0 
1 
0 
0.366667 
0 
5 
Computer_
Science 
6 
1 
0 
0.76092
1 
0.0403
33 
0.75 
0 
1 
0 
0.366667 
0 
5 
Computer_
Science 
7 
1 
0 
0.75922
3 
0.2176
31 
0.75 
0 
1 
0 
0.366667 
0 
5 
Computer_
Science 
8 
1 
0 
0.54253
2 
0.2744
13 
0.75 
0 
1 
0 
0.366667 
0 
5 
Computer_
Science 
9 
1 
0 
0.82146
6 
0.1198
86 
0.75 
0 
1 
0 
0.366667 
0 
5

Economics 
0 
1 
0 
0.09668
7 
0.0342
72 
0.6 
0.12
2474 
0.72 
0.09798 
0.56 
0.146667 
5

Economics 
1 
1 
0 
0.17096 
0.1272
6 
0.65 
0.12
2474 
0.68 
0.09798 
0.56 
0.146667 
5

Economics 
2 
1 
0 
0.33522
2 
0.1240
72 
0.7 
0.1 
0.6 
0 
0.56 
0.146667 
5

Economics 
3 
1 
0 
0.55085
7 
0.2870
06 
0.65 
0.12
2474 
0.64 
0.08 
0.56 
0.146667 
5

Economics 
4 
1 
0 
0.74097
2 
0.2635
5 
0.55 
0.1 
0.6 
0 
0.34 
0.146667 
5

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 28

28/29

Economics 
5 
1 
0 
0.63901
6 
0.2531
92 
0.65 
0.2 
0.6 
0 
0.34 
0.146667 
5

Economics 
6 
1 
0 
0.85007
3 
0.0849
01 
0.5 
0 
0.6 
0 
0.413333 
0.179629 
5

Economics 
7 
1 
0 
0.82168
8 
0.0627
64 
0.5 
0 
0.6 
0 
0.486667 
0.179629 
5

Economics 
8 
1 
0 
0.88383
9 
0.0539
1 
0.5 
0 
0.6 
0 
0.413333 
0.179629 
5

Economics 
9 
1 
0 
0.88128
7 
0.0604
45 
0.5 
0 
0.6 
0 
0.486667 
0.179629 
5 
Environmen
tal_Science 
0 
0.89405
7 
0.104
497 
0.09418
7 
0.0293
49 
0.95 
0.1 
0.92 
0.09798 
0 
0 
5 
Environmen
tal_Science 
1 
0.96197
7 
0.056
177 
0.4417 
0.2963
76 
0.95 
0.1 
0.96 
0.08 
0 
0 
5 
Environmen
tal_Science 
2 
0.98369
3 
0.020
913 
0.60958
2 
0.0959
96 
0.75 
0 
0.96 
0.08 
0 
0 
5 
Environmen
tal_Science 
3 
0.97712
2 
0.031
915 
0.49854 
0.2271
06 
0.75 
0 
0.92 
0.09798 
0 
0 
5 
Environmen
tal_Science 
4 
0.98372
9 
0.032
542 
0.75845
7 
0.0814
08 
0.7 
0.1 
0.92 
0.09798 
0 
0 
5 
Environmen
tal_Science 
5 
0.98372
9 
0.032
542 
0.73678
7 
0.0716
84 
0.65 
0.12
2474 
0.84 
0.08 
0 
0 
5 
Environmen
tal_Science 
6 
1 
0 
0.81989
1 
0.0339
31 
0.6 
0.12
2474 
0.8 
0.12649
1 
0 
0 
5 
Environmen
tal_Science 
7 
0.98289
7 
0.014
109 
0.80893
8 
0.0401
75 
0.6 
0.12
2474 
0.92 
0.09798 
0 
0 
5 
Environmen
tal_Science 
8 
0.97923
2 
0.015
827 
0.83610
7 
0.0471
62 
0.65 
0.12
2474 
0.96 
0.08 
0 
0 
5 
Environmen
tal_Science 
9 
0.99289
9 
0.013
954 
0.82494
6 
0.0564
3 
0.75 
0.15
8114 
0.88 
0.09798 
0 
0 
5

History 
0 
0.93753
2 
0.077
054 
0.07621
5 
0.0280
79 
0.85 
0.12
2474 
0.88 
0.24 
0 
0 
5

History 
1 
0.86502
2 
0.117
449 
0.15757
1 
0.2027
59 
0.75 
0.15
8114 
0.84 
0.14966
6 
0 
0 
5

History 
2 
0.85465
4 
0.006
944 
0.64004
4 
0.4274
31 
1 
0 
0.96 
0.08 
0 
0 
5

History 
3 
0.80472
5 
0.056
84 
0.73718
2 
0.2354
22 
1 
0 
1 
0 
0 
0 
5

History 
4 
0.73085
5 
0.073
931 
0.45772
6 
0.1539
62 
0.95 
0.1 
1 
0 
0 
0 
5

History 
5 
0.69050
5 
0.032
713 
0.36214
9 
0.1711
77 
0.95 
0.1 
0.92 
0.09798 
0 
0 
5

History 
6 
0.68912 
0.019
571 
0.37862
8 
0.3060
52 
1 
0 
0.88 
0.09798 
0 
0 
5

History 
7 
0.67931
4 
0.038
587 
0.61497
6 
0.2652
42 
1 
0 
0.84 
0.08 
0 
0 
5

History 
8 
0.63934
8 
0.002
281 
0.95588
3 
0.0307
94 
1 
0 
0.8 
0 
0 
0 
5

History 
9 
0.64548
8 
0.011
246 
0.93704
7 
0.0427
09 
1 
0 
0.8 
0 
0 
0 
5

Law 
0 
1 
0 
0.13720
4 
0.0440
46 
0.8 
0.1 
0.92 
0.09798 
0.22 
0.179629 
5

Law 
1 
1 
0 
0.19902
2 
0.0965
47 
0.6 
0.12
2474 
1 
0 
0 
0 
5

Law 
2 
1 
0 
0.30201
2 
0.1503
01 
0.6 
0.12
2474 
1 
0 
0 
0 
5

Law 
3 
1 
0 
0.61089
6 
0.1179
71 
0.6 
0.12
2474 
1 
0 
0 
0 
5

Law 
4 
1 
0 
0.71545
6 
0.1898
85 
0.7 
0.1 
1 
0 
0 
0 
5

Law 
5 
1 
0 
0.64009
8 
0.1112
66 
0.7 
0.1 
0.96 
0.08 
0 
0 
5

Law 
6 
1 
0 
0.79893
7 
0.0434
77 
0.75 
0 
0.96 
0.08 
0 
0 
5

Law 
7 
1 
0 
0.73302 
0.0692
76 
0.75 
0 
1 
0 
0 
0 
5

Law 
8 
1 
0 
0.86062
9 
0.0951
18 
0.75 
0 
1 
0 
0 
0 
5

Law 
9 
1 
0 
0.83492
5 
0.0411
56 
0.75 
0 
1 
0 
0 
0 
5

Medicine 
0 
1 
0 
0.08877
1 
0.0414
69 
0.95 
0.1 
0.92 
0.09798 
0.106667 
0.130639 
5

Medicine 
1 
0.96288
9 
0.074
221 
0.27340
7 
0.0664
51 
1 
0 
0.8 
0 
0.106667 
0.130639 
5

Medicine 
2 
0.94557 
0.067
571 
0.32133
6 
0.0393
26 
0.95 
0.1 
0.8 
0 
0.106667 
0.130639 
5

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 29

29/29

Medicine 
3 
1 
0 
0.59126 
0.2118
73 
1 
0 
0.8 
0 
0 
0 
5

Medicine 
4 
0.97853
5 
0.042
93 
0.68717
1 
0.0710
87 
1 
0 
0.8 
0 
0 
0 
5

Medicine 
5 
1 
0 
0.69902
4 
0.1021
4 
1 
0 
0.8 
0 
0 
0 
5

Medicine 
6 
1 
0 
0.73355
7 
0.1741
4 
1 
0 
0.8 
0 
0 
0 
5

Medicine 
7 
1 
0 
0.72497 
0.1163
57 
1 
0 
0.8 
0 
0 
0 
5

Medicine 
8 
1 
0 
0.92185
2 
0.0832
43 
1 
0 
0.8 
0 
0 
0 
5

Medicine 
9 
1 
0 
0.82637
8 
0.0445
27 
1 
0 
0.8 
0 
0 
0 
5

Philosophy 
0 
1 
0 
0.08833
9 
0.0172
08 
0.75 
0.15
8114 
0.84 
0.08 
0.293333 
0.146667 
5

Philosophy 
1 
1 
0 
0.35870
5 
0.4210
68 
0.65 
0.2 
0.8 
0 
0.073333 
0.146667 
5

Philosophy 
2 
1 
0 
0.47524
4 
0.4283
1 
0.7 
0.24
4949 
0.8 
0 
0 
0 
5

Philosophy 
3 
1 
0 
1 
0 
1 
0 
0.8 
0 
0 
0 
5

Philosophy 
4 
1 
0 
1 
0 
1 
0 
0.8 
0 
0 
0 
5

Philosophy 
5 
1 
0 
1 
0 
1 
0 
0.8 
0 
0 
0 
5

Philosophy 
6 
1 
0 
1 
0 
1 
0 
0.8 
0 
0 
0 
5

Philosophy 
7 
1 
0 
1 
0 
1 
0 
0.8 
0 
0 
0 
5

Philosophy 
8 
1 
0 
1 
0 
1 
0 
0.8 
0 
0 
0 
5

Philosophy 
9 
1 
0 
0.98047 
0.0239
19 
1 
0 
0.8 
0 
0 
0 
5

Physics 
0 
1 
0 
0.08189 
0.0337
17 
0.95 
0.1 
0.88 
0.09798 
0.44 
0.146667 
5

Physics 
1 
1 
0 
0.32182
1 
0.2506
41 
0.85 
0.12
2474 
0.68 
0.09798 
0.366667 
0 
5

Physics 
2 
1 
0 
0.29031
7 
0.0805
84 
0.8 
0.1 
0.68 
0.09798 
0.366667 
0 
5

Physics 
3 
1 
0 
0.28937
6 
0.1349
08 
0.75 
0 
0.6 
0 
0.293333 
0.146667 
5

Physics 
4 
1 
0 
0.61573
9 
0.0895
64 
0.75 
0 
0.64 
0.08 
0.293333 
0.146667 
5

Physics 
5 
1 
0 
0.62747
7 
0.1292
03 
0.75 
0 
0.84 
0.08 
0.293333 
0.146667 
5

Physics 
6 
1 
0 
0.60664
2 
0.1221
63 
0.75 
0 
0.8 
0.12649
1 
0.22 
0.179629 
5

Physics 
7 
1 
0 
0.72726
9 
0.1200
87 
0.75 
0 
0.96 
0.08 
0.073333 
0.146667 
5

Physics 
8 
1 
0 
0.75870
8 
0.0759
3 
0.75 
0 
0.88 
0.09798 
0.22 
0.179629 
5

Physics 
9 
1 
0 
0.79299
8 
0.0658
46 
0.75 
0 
0.96 
0.08 
0.146667 
0.179629 
5

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.
