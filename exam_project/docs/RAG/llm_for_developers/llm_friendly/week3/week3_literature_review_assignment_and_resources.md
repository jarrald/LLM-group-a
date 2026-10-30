# Week 3 — Literature Review Assignment: LLM Prompting and Societal Implications

**Source:** `HandInPromptingArtifacts(1).pdf` and `Web Resources.md`.

## 1. Assignment purpose

The handout is titled **“Literature Review on LLM Prompting and Societal Implications.”** It focuses on how interaction with LLMs through prompting can influence the quality, reliability, and societal impact of AI-generated information.

The group project examines three challenges:

1. **Ambiguity and semantic drift:** Can an unclear AI response lead to the wrong conclusion or progressively renewed conclusions?
2. **Hallucination:** Can a false AI answer become accepted as truth?
3. **Prompt injection:** Can AI systems be compromised and manipulated through prompts?

The assignment's background frames these as issues that can affect individuals, organizations, and society.

## 2. Learning objectives

Students are asked to search and evaluate existing literature and to:

- Explain ambiguity, semantic drift, hallucination, and prompt injection.
- Synthesize literature in the context of LLM training and inference/prompting.
- Discuss potential implications of these artifacts.
- Communicate findings to peers in a simulated company setting, as though the group were an IT department reporting to the CEO, CSO, and CHRO.

The handout says to focus on analysis and synthesis of existing research, **not new experiments**.

## 3. Deliverables and logistics

The handout specifies:

- One PowerPoint presentation per group, maximum 6 slides and maximum 10 minutes.
- One synopsis per group, maximum 6 pages plus cover page.
- Group size: 4–6 students.
- Estimated workload: approximately 0.5 FTE week per group, described as about 23 hours for a group of five.
- Per-group hand-in: Thursday evening of Week 5, listed as **24 September**, by email to `jatr@ek.dk`.
- The Week 3 lecture says the group exercise should finish Friday 25 September (Week 5).

**Deadline caution:** verify the exact deadline with the course instructor if needed. The supplied handout and lecture date wording should not be silently reconciled.

The handout permits cautious use of AI but says students must be able to account for and discuss their deliberations.

## 4. Suggested structure for the synopsis

This is a practical structure consistent with the assignment's objectives; it is a suggestion, not a required structure printed in the handout.

1. **Executive summary:** main risks and implications.
2. **Scope and method:** databases searched, search terms, inclusion criteria, and limits.
3. **Ambiguity and semantic drift:** definitions, key studies, findings, limitations, and implications.
4. **Hallucination:** definitions, detection/evaluation methods, evidence, and implications.
5. **Prompt injection:** attack categories, vulnerabilities, defenses, and implications.
6. **Cross-topic synthesis:** interactions among the three topics.
7. **Recommendations:** proportionate controls for an organization.
8. **Limitations and conclusion:** what the literature does and does not establish.
9. **References:** consistent academic citation style.

For the six-slide presentation, prioritize the most important evidence and recommendations rather than trying to summarize every paper.

## 5. Literature-search guidance

The handout suggests Google Scholar, ACM Digital Library, and arXiv. It recommends prioritizing articles, conference proceedings, blogs, and reviews, preferably from the previous 5–7 years, and refers students to additional inspiration in ItsLearning.

The supplied `Web Resources.md` lists the following resources.

### Ambiguity and semantic drift

- Meta AI Research: https://ai.meta.com/research/publications/know-when-to-stop-a-study-of-semantic-drift-in-text-generation/
- arXiv PDF: https://arxiv.org/pdf/2603.05801

### Hallucination

- OpenAI, “Why language models hallucinate”: https://openai.com/index/why-language-models-hallucinate
- Lillian Weng, “Hallucination in Large Language Models”: https://lilianweng.github.io/posts/2024-07-07-hallucination
- TruthfulQA repository: https://github.com/sylinrl/TruthfulQA/tree/main

### Prompt injection

- Promptfoo: https://www.promptfoo.dev/blog/prompt-injection
- OWASP GenAI Security Project: https://genai.owasp.org/
- OWASP prompt injection risk: https://genai.owasp.org/llmrisk/llm01-prompt-injection
- Simon Willison, “The lethal trifecta”: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta

These are starting points, not an exhaustive bibliography. Verify publication details, research methods, and claims in the original sources before citing them.

## 6. How to evaluate sources critically

For each paper or article, record:

- Full citation and publication date.
- Research question.
- Whether it is an empirical study, benchmark, survey/review, opinion piece, or technical blog.
- Models and datasets evaluated.
- Definition and measurement of the target behavior.
- Main findings and evidence.
- Limitations, assumptions, and possible conflicts of interest.
- Relevance to real-world deployment.
- Whether the results are reproducible or independently supported.

Do not treat a blog post, benchmark, and peer-reviewed empirical study as interchangeable evidence. Use the source type and evidence strength to qualify conclusions.

## 7. Suggested synthesis matrix

| Topic | Core question | Evidence to compare | Potential implications |
|---|---|---|---|
| Ambiguity / semantic drift | Can interpretation shift or become unreliable across prompts and turns? | Definitions, multi-turn evaluations, error rates, recovery strategies | Incorrect decisions, user confusion, unreliable agent workflows |
| Hallucination | When do models produce unsupported claims, and how can they be evaluated? | Benchmarks, human verification, source-grounding methods, calibration | Misinformation, fabricated citations, over-trust |
| Prompt injection | Can untrusted text manipulate model behavior or tool use? | Attack taxonomies, evaluations, defense studies, application-level controls | Data exposure, unauthorized actions, policy bypass |

## 8. Suggested recommendations to discuss

Recommendations should be tied to evidence gathered in the literature review. Possible areas to investigate include:

- Clarify and consolidate requirements when prompts are underspecified.
- Verify factual claims and citations before consequential use.
- Use retrieval and citations carefully, while recognizing that retrieval does not guarantee correctness.
- Treat retrieved content as untrusted data rather than privileged instructions.
- Enforce access control and tool permissions in application code.
- Require confirmation for high-impact actions.
- Test systems against realistic failure modes and monitor them after deployment.
- Communicate uncertainty and limitations to users.

These are discussion prompts, not claims that any single control fully solves the problems.

## 9. Review questions

1. What distinguishes a literature review from a new experiment?
2. What are the three core topics required by the handout?
3. What are the deliverable limits?
4. Which search sources are recommended?
5. How can evidence quality differ across papers, benchmarks, and blog posts?
6. How can the three topics interact in a deployed LLM system?
7. Which recommendations can be supported by the literature your group finds?
