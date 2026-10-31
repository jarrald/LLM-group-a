# Week 3 Societal Aspects — Ambiguity and Semantic Drift

**Related source:** `Ambiguity1.pdf`, *LLMs Get Lost in Multi-Turn Conversation* (arXiv:2505.06120, 9 May 2025).  
**Related source:** `Ambiguity2.pdf`, a paper about semantic drift in text generation. The Week 3 resource list links to Meta AI Research and arXiv:2603.05801.

> This file is a study-oriented summary, not a reproduction of the papers. The findings below are attributed to the supplied research and should be interpreted within their experimental settings.

## 1. Ambiguity and underspecified instructions

An instruction is ambiguous when it supports multiple plausible interpretations. An instruction is underspecified when it leaves out information required to confidently determine the intended output. These concepts overlap but are not identical: an underspecified request may simply omit a constraint without having two directly conflicting meanings.

The Week 3 lecture asks students to test ambiguity by writing prompts with different tone, language, or framing while asking essentially the same question. They should run the prompts against several models, observe differences, and report what they find.

## 2. Multi-turn conversations and the “lost in conversation” effect

The supplied paper *LLMs Get Lost in Multi-Turn Conversation* studies how models perform when requirements are spread across multiple turns rather than stated together in one fully specified instruction.

The paper's abstract reports an average performance drop of **39% across six generation tasks** when comparing multi-turn settings with single-turn fully specified instructions. It analyzes more than 200,000 simulated conversations and separates performance degradation into:
- **Aptitude:** the model's ability to produce a correct result under a given setup.
- **Unreliability:** how inconsistently the model performs across repeated attempts.

The paper reports that models often make assumptions early, attempt final solutions prematurely, and then rely too heavily on those early assumptions. When the conversation takes a wrong turn, the model may fail to recover. The abstract reports this pattern across both open-weight and closed-weight models tested in the study.

These are findings of that paper's experimental setup, not a guarantee that every multi-turn conversation performs worse or that all products behave identically.

### Practical implication

When a conversation becomes confused, consolidate the requirements into one explicit instruction before retrying. A useful recovery prompt is:

> Please summarize and consolidate all requirements I have stated so far. Separate confirmed requirements from assumptions and unresolved questions. Do not implement or answer the task yet.

Then verify the consolidated summary and use it as the basis for the next request. Starting a new conversation can also reduce reliance on a long, confused context, but it does not itself guarantee correctness.

## 3. Semantic drift

Semantic drift concerns meaning changing over time or across generated text. In a multi-turn dialogue, the intended task can gradually shift as the model introduces assumptions, paraphrases requirements, or responds to a mistaken interpretation.

The Week 3 assignment asks students to research ambiguity and semantic drift, synthesize evidence, and discuss how these issues can affect the trustworthiness of AI-generated information and decisions.

A robust analysis should distinguish:
- **User-intent drift:** the conversation no longer reflects what the user originally meant.
- **Interpretation drift:** the model's interpretation changes across turns.
- **Generated-content drift:** claims or themes change as text is generated or continued.

These are useful analytical categories; the assignment handout itself does not define them as a formal taxonomy.

## 4. Risks and mitigations

### Risks

- The model silently assumes an interpretation the user did not intend.
- Early assumptions become embedded in later answers.
- Requirements spread across turns are forgotten or contradicted.
- A user accepts a fluent answer without checking whether it addresses the intended question.
- An agentic system acts on an incorrect interpretation, potentially producing consequences beyond text.

### Mitigations

- State key requirements explicitly and consolidate them periodically.
- Ask clarifying questions when ambiguity materially affects the result.
- Mark assumptions as assumptions rather than facts.
- Verify important claims against trusted sources.
- Test prompts across paraphrases and conversation lengths.
- For consequential tasks, require confirmation before external actions.

## 5. Suggested experiment based on the lecture

1. Create two prompts with the same underlying request but different tone, language, or framing.
2. Test each prompt against more than one LLM.
3. Record how the response interpretation changes.
4. Start a multi-turn conversation with an underspecified request; add requirements over later turns.
5. Compare the result with a single consolidated prompt containing all requirements.
6. Note errors, omitted requirements, assumptions, and recovery behavior.

Record the model, date, exact prompts, settings if known, and observed outputs. Do not generalize from one response to all models.

## 6. Review questions

1. How do ambiguity and underspecification differ?
2. What is semantic drift?
3. What does the “lost in conversation” paper report about single-turn versus multi-turn performance?
4. How does the paper distinguish aptitude from unreliability?
5. Why can early assumptions be difficult to correct later?
6. How can consolidating requirements improve a conversation?
7. What limitations apply when generalizing from a research benchmark to a real product?
8. What evidence would you collect to test whether a model has misunderstood a prompt?
