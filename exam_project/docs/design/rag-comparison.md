# StudyGraph — RAG Comparison Design

## 1. Purpose

One of StudyGraph's objectives is to demonstrate how Retrieval-Augmented Generation (RAG) affects the responses produced by a Large Language Model (LLM).

The application supports two configurations:

- **RAG:** The LLM receives relevant retrieved content from the *LLMs for Developers* course knowledge base.
- **Non-RAG:** The LLM generates responses without course-specific retrieved content.

The comparison should help evaluate whether retrieval improves the relevance, factual correctness, and usefulness of responses about the course material.

## 2. Experimental Principle

To evaluate the effect of RAG, other relevant variables should remain consistent wherever possible.

The two configurations should use the same:

- Language model and model version.
- Task.
- Tone.
- Traits.
- Target.
- User question.
- Conversation history.
- Generation parameters.

The primary intended difference is whether course-specific retrieval is performed and its results are supplied to the LLM.

This isolates the contribution of retrieval more effectively than comparing unrelated Buddies or prompts.

## 3. Configuration Through Buddies

The existing Buddy concept provides a straightforward way to create the two configurations.

For example, a student can create:

| Setting | RAG Buddy | Non-RAG Buddy |
|---|---|---|
| Name | Course Tutor | General Tutor |
| Target | Beginner | Beginner |
| Tone | Friendly and encouraging | Friendly and encouraging |
| Traits | Patient and explanatory | Patient and explanatory |
| Course | LLMs for Developers | No course |
| Retrieval | Enabled for course-related questions | Disabled |

The two Buddies differ only in their course association and name.

The names are for user identification; they should not be included in a way that unintentionally changes the model's behavioral instructions.

When comparing responses, the student should use the same question in separate conversations with each Buddy.

The conversation snapshots preserve the configuration used for each run.

## 4. RAG Mode

In RAG mode, the application retrieves relevant content from the course knowledge base before generating a response.

The intended process is:

1. The user submits a question.
2. The application identifies the conversation's Buddy configuration.
3. The application retrieves relevant course content.
4. The retrieved content is supplied to the LLM alongside the prompt and relevant conversation history.
5. The LLM generates a response.
6. The application presents the response and available source references.

The retrieved content provides course-specific context that may not be present in the model's original training data or general knowledge.

RAG does not guarantee correctness. Retrieval may return irrelevant information, miss useful material, or provide incomplete context.

## 5. Non-RAG Mode

In non-RAG mode, the application uses the same general chat workflow without course-specific retrieval.

The intended process is:

1. The user submits a question.
2. The application identifies the conversation's Buddy configuration.
3. The application constructs the prompt and includes relevant conversation history.
4. The LLM generates a response without retrieved course context.
5. The application presents the response.

The model may still know relevant information from its training. The distinction is that the application does not retrieve and supply the course's indexed materials.

Non-RAG responses should not be presented as if they were grounded in the course knowledge base.

## 6. Suggested Evaluation Method

A small, predefined set of evaluation questions can be used to compare both configurations.

Questions should cover several categories:

- **Direct factual questions:** Ask for information explicitly covered in the lecture materials.
- **Conceptual questions:** Ask for explanations of important concepts.
- **Comparison questions:** Ask the assistant to compare related concepts.
- **Application questions:** Ask the assistant to apply a course concept to a scenario.
- **Insufficient-information questions:** Ask questions that cannot be answered adequately from the available course material.

For each question, generate a response using both configurations.

Where practical, use separate conversations with identical Buddy settings except for course association.

Record the question and both responses so that they can be evaluated consistently.

## 7. Evaluation Criteria

Responses can be evaluated using the following criteria.

### Factual Correctness

Does the response contain correct information?

### Course Alignment

Does the response accurately reflect the terminology, explanations, and emphasis used in the course material?

### Relevance

Does the response answer the question asked without introducing unnecessary or unrelated information?

### Grounding

For RAG responses, are the claims supported by the retrieved course material?

### Completeness

Does the response cover the important aspects of the question?

### Source Quality

When references are available, do they point to relevant material that supports the response?

### Uncertainty Handling

Does the assistant communicate uncertainty when the available course material does not adequately support an answer?

A simple qualitative rating scale can be used for the initial evaluation. More formal metrics can be introduced if required by the assignment.

## 8. Recording Results

The evaluation should record enough information to make the comparison understandable.

A simple results table could contain:

| Field | Description |
|---|---|
| Question ID | Identifier for the evaluation question. |
| Question | The submitted question. |
| Buddy configuration | Target, Tone, and Traits used. |
| Mode | RAG or non-RAG. |
| Response | The generated answer. |
| Retrieved sources | Sources supplied to the model, when applicable. |
| Factual correctness | Evaluation of factual accuracy. |
| Course alignment | Evaluation against the course materials. |
| Relevance | Evaluation of how well the answer addresses the question. |
| Notes | Observations about the result. |

This table can initially be maintained manually. An automated evaluation interface is not required for V1.

If practical, also record the model version and generation parameters to improve reproducibility.

## 9. Expected Outcomes

RAG may improve responses when the question concerns information explicitly covered by the course material.

Potential benefits include:

- Better alignment with course-specific terminology.
- More accurate references to lecture content.
- Access to information that may not be reliably recalled from the model's general knowledge.
- Improved traceability through source references.

However, RAG may also fail to improve a response when:

- The model already knows the answer.
- Retrieval returns irrelevant passages.
- Relevant information is missing from the knowledge base.
- Document conversion or chunking loses important context.
- The retrieved content is incomplete or ambiguous.

The evaluation should report observed results rather than assuming RAG always performs better.

## 10. Interpretation and Limitations

The comparison evaluates the system's behavior under the tested conditions. It does not establish that RAG will always improve answer quality.

The evaluation dataset may be small, subjective scoring may introduce bias, and individual model responses can vary.

Using the same model and prompt configuration helps isolate retrieval as the main experimental variable, but other differences may remain.

The results should therefore be interpreted in the context of the selected model, course materials, retrieval configuration, and evaluation questions.