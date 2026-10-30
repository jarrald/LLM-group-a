# Week 3 Societal Aspects — LLM Hallucinations

**Related sources:** `Hallucinations1(2).pdf`, `Hallucinations2.pdf`, and the resource list in `Web Resources.md`.

## 1. What is an LLM hallucination?

In this course context, a hallucination is an output that presents fabricated, unsupported, or unverifiable information as though it were factual. Hallucinations can include invented facts, citations, events, explanations, or details that are not supported by the available evidence.

A response can be fluent, detailed, and confidently phrased while still being wrong. Fluency and confidence should not be treated as evidence of truth.

The Week 3 lecture warns that hallucinations can introduce a false “new truth” that users may continue to believe even after a correction. This is a societal risk because misinformation can influence decisions, be repeated by others, or be passed into downstream systems.

## 2. Why hallucinations matter

Potential consequences include:
- Users learning or repeating false information.
- Incorrect decisions in educational, workplace, or public settings.
- Fabricated citations or references that waste time and undermine trust.
- Errors propagating through automated workflows.
- False claims being repeated in later summaries or documents.

The impact depends on context. A minor fictional detail in creative writing is different from an invented legal citation, medical claim, or security instruction.

## 3. Hallucination and the Week 2/Week 3 exercises

The Week 1 and Week 3 slides suggest testing hallucination by asking about an invented concept, for example:

> Explain the principle underlying Relativistic Quantum Blockchains (RQBs).

This is a test prompt, not a real scientific concept established by the course. The useful observation is whether the model acknowledges that the term may be fictional or instead fabricates a plausible-sounding explanation.

When running the exercise:
1. Use the same invented concept across several models.
2. Keep the prompt text and settings consistent where possible.
3. Record whether the model questions the premise, expresses uncertainty, or invents details.
4. Check any claims that appear factual.
5. Avoid interpreting one response as a comprehensive benchmark of the model.

## 4. Detection and evaluation

The supplied resource list points to OpenAI's article *Why language models hallucinate*, Lillian Weng's overview of hallucinations, and the TruthfulQA project. `Hallucinations2.pdf` is titled *Hallucination Detection and Evaluation of Large Language Model* and is an arXiv paper dated 9 April 2026 in its supplied version.

For a literature review, distinguish at least three questions:
- **Detection:** Does an answer contain unsupported or false claims?
- **Evaluation:** How often does a model hallucinate under a specified test setup?
- **Mitigation:** What methods reduce the likelihood or impact of hallucinations?

These are different tasks. A detection method may itself make mistakes, and a benchmark score only measures the behaviors covered by that benchmark.

### Evidence-based checking

Useful approaches include:
- Verify claims against reliable source material.
- Check whether cited sources exist and actually support the claim.
- Compare answer statements with retrieved documents.
- Ask the model to identify uncertainty, but do not treat self-reported confidence as proof.
- Use human review for consequential outputs.
- Track unsupported claims separately from ordinary mistakes or ambiguous wording.

In RAG systems, retrieval can help ground answers in supplied material, but RAG does not guarantee truth. The source may be incomplete, stale, irrelevant, or itself incorrect; the model may also misread or overstate what it says.

## 5. Relationship to ambiguity and semantic drift

Ambiguity concerns multiple possible interpretations; hallucination concerns unsupported or fabricated content. They can interact: a vague prompt may encourage a model to fill gaps with assumptions, and the resulting invented details may then steer later turns of the conversation.

The Week 3 lecture's core recommendation is to validate or cross-validate model responses rather than accept them uncritically.

## 6. Review questions

1. What distinguishes a hallucination from an ordinary factual error?
2. Why is a fluent response not necessarily reliable?
3. How can invented facts become socially consequential?
4. How can a fictional-concept prompt test a model's handling of uncertainty?
5. What is the difference between hallucination detection, evaluation, and mitigation?
6. Why does retrieval-augmented generation not eliminate hallucinations?
7. How should sources and citations in an LLM answer be verified?
