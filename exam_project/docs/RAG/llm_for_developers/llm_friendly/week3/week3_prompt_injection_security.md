# Week 3 Societal Aspects — Prompt Injection and LLM Security

**Related sources:** `Injection1(1).pdf`, `Injection2.pdf`, `Web Resources.md`, and the Week 3 lecture slides 32–36.

> This document summarizes security concepts for study and defensive design. It focuses on recognizing risks and protecting LLM applications, rather than providing operational instructions for attacking real systems.

## 1. What is prompt injection?

Prompt injection is an attack in which untrusted text attempts to change how an LLM behaves by introducing instructions that conflict with the application's intended instructions or policies.

LLMs process instructions and ordinary content through the same language interface. A system may concatenate developer instructions, user text, and retrieved content into a model context. The lecture emphasizes that after concatenation, a model may not reliably preserve the trust boundaries that the application developer intended.

Prompt injection is not the same as a traditional code injection vulnerability, but it can cause comparable application-level problems when an LLM is allowed to use tools, access private data, or trigger actions.

## 2. Direct and indirect prompt injection

### Direct prompt injection

An attacker types instructions directly into the conversation. The intent is to override the application's rules or steer the model toward an unintended response or action.

### Indirect prompt injection

Malicious instructions are embedded in content the model reads later, such as a web page, retrieved document, email, or file. The user may not see the instructions. The model encounters them as part of the material it is asked to process.

Indirect prompt injection is especially relevant to RAG systems because retrieved documents are external content and may contain hostile instructions as well as useful facts.

## 3. Why RAG applications are exposed

A RAG pipeline typically retrieves documents based on semantic relevance and adds their text to the prompt. Relevance is not the same as trustworthiness. A document may be relevant to the question and still contain malicious or misleading instructions.

Potential failure modes include:
- The model follows instructions embedded in a retrieved document.
- Retrieved text asks the model to reveal private context or secrets.
- An agent uses a tool or performs an action based on untrusted content.
- The model treats text in a document as higher-priority instructions than it should.
- A document's false claims are repeated as though they were verified facts.

The key design principle is to treat retrieved text as **untrusted data**, not as system or developer instructions.

## 4. Defensive design principles

No single prompt or filter fully eliminates prompt injection. Use layered defenses.

### Instruction and data separation

- Clearly label retrieved passages as untrusted reference material.
- Tell the model to use retrieved passages as evidence, not to follow instructions found inside them.
- Avoid placing untrusted text in a position where it can be confused with privileged instructions.
- Do not assume textual delimiters alone create a hard security boundary.

### Least privilege

- Give tools and agents only the permissions needed for the task.
- Keep secrets, credentials, and private system context out of the model prompt when possible.
- Do not allow the model to authorize its own access to sensitive resources.
- Enforce access control in application code, not only in natural-language instructions.

### Validate actions outside the model

- Require explicit confirmation for high-impact or irreversible actions.
- Validate tool arguments against schemas and business rules.
- Check authorization for every requested resource and action.
- Apply output validation and policy checks before executing tools or returning sensitive results.
- Log security-relevant events without unnecessarily logging secrets or sensitive personal data.

### Retrieval-specific safeguards

- Track source identity and metadata for retrieved passages.
- Use trusted-source allowlists when appropriate.
- Filter or quarantine suspicious documents.
- Limit retrieved content to relevant passages.
- Evaluate the system using documents that contain both benign instructions and malicious embedded instructions.
- Ensure retrieval cannot bypass user-level document permissions.

## 5. Evaluation and testing

A responsible prompt-injection evaluation should use an isolated test environment and synthetic data. Record:
- The application instructions and model configuration.
- The source of each retrieved passage.
- Whether the model followed an untrusted instruction.
- Whether sensitive information was exposed.
- Whether tools were called and whether actions were authorized.
- Whether defenses blocked, detected, or merely logged the behavior.

A refusal is not the only possible safe outcome. Depending on the task, the model may safely summarize or quote malicious text as content while declining to obey it.

## 6. Literature-review questions

1. How does prompt injection differ from ordinary user instructions?
2. What distinguishes direct from indirect prompt injection?
3. Why are RAG systems exposed to indirect prompt injection?
4. Why is semantic relevance not a trust signal?
5. Why are natural-language instructions alone insufficient as a security boundary?
6. What is the principle of least privilege for LLM tools?
7. Which controls should be enforced in application code rather than delegated to the model?
8. How would you evaluate whether a defense works without using real secrets or production systems?
9. What security and privacy risks arise when retrieved documents have different access permissions?

## 7. Resources listed in the course

- Promptfoo introduction: https://www.promptfoo.dev/blog/prompt-injection/
- OWASP GenAI Security Project: https://genai.owasp.org/
- OWASP Top 10 for LLM Applications — Prompt Injection: https://genai.owasp.org/llmrisk/llm01-prompt-injection
- Simon Willison, “The lethal trifecta”: https://simonwillison.net/2025/Jun/16/the-lethal-trifecta

These links are provided as starting points from the supplied course resource list. Review their current content and publication dates when citing them in an academic assignment.
