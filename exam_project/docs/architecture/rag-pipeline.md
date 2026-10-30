# StudyGraph — RAG Pipeline

## 1. Purpose

This document describes how StudyGraph prepares course materials, retrieves relevant content, and supplies that content to the local LLM.

It also defines the distinction between RAG and non-RAG behavior so both modes can be implemented and evaluated consistently.

## 2. Course Knowledge Base

For V1, StudyGraph supports one predefined course: *LLMs for Developers*.

The course materials are prepared before users interact with the application. Lecture slides provided as PDFs are converted into Markdown documents.

Users do not need to upload the primary course materials before using the assistant.

The indexed documents should retain enough metadata to identify their source, such as:

- Document identifier.
- Document name.
- Lecture or section, when available.
- Page or slide reference, when available.
- Relevant content.

Source metadata supports traceability and the presentation of references in assistant responses.

## 3. Indexing Pipeline

Indexing prepares the course documents for retrieval.

The conceptual process is:

1. Collect the predefined course documents.
2. Convert PDF lecture slides into Markdown.
3. Clean up extraction artifacts where necessary.
4. Split documents into smaller, meaningful text chunks.
5. Associate each chunk with source metadata.
6. Convert chunks into vector representations using an embedding model.
7. Store the representations and associated content in a searchable index.

The exact document-splitting strategy, embedding model, and vector store remain open implementation decisions.

### Chunking Considerations

Chunks should contain enough context to preserve the meaning of the source material while remaining small enough for focused retrieval.

Splitting should avoid unnecessarily separating headings from the content they describe.

The final strategy should be evaluated against the actual structure and quality of the lecture materials.

### Source Metadata

Metadata should be preserved during indexing so that retrieved content can be traced to its original document.

Where possible, references should identify the relevant lecture, document, page, or slide.

The application should not invent page or slide references when that information is unavailable.

## 4. RAG Query Pipeline

When a user sends a message in a course-associated conversation, the application follows this process:

1. Load the conversation and its Buddy configuration snapshot.
2. Retrieve relevant conversation history.
3. Construct the current prompt using Task, Tone, Traits, and Target.
4. Prepare a retrieval query from the user's message and relevant context.
5. Search the course knowledge base for relevant chunks.
6. Select the most relevant results according to the retrieval strategy.
7. Supply the retrieved content to the LLM as contextual information.
8. Generate the assistant response.
9. Return the response and available source references.
10. Persist the user message and assistant response.

The exact retrieval strategy, number of retrieved chunks, and context limits will be determined during implementation.

## 5. Non-RAG Query Pipeline

When a conversation has no associated course, the application follows the same general chat workflow but skips course-specific retrieval.

The process is:

1. Load the conversation and its Buddy configuration snapshot.
2. Retrieve relevant conversation history.
3. Construct the current prompt using Task, Tone, Traits, and Target.
4. Send the prompt and relevant conversation history to the LLM without course-specific retrieved context.
5. Return the generated response.
6. Persist the user message and assistant response.

The non-RAG mode must not accidentally retrieve course content through the course retrieval component.

This ensures the mode provides a meaningful baseline for comparison.

## 6. Prompt and Context Separation

The implementation should distinguish between three types of input:

- **Prompt instructions:** The Task, Tone, Traits, and Target.
- **Conversation history:** Previous messages needed to maintain conversational context.
- **Retrieved context:** Course passages supplied when RAG is enabled.

Keeping these inputs conceptually separate makes the system easier to test and helps isolate the effect of retrieval during evaluation.

Retrieved course text should be treated as reference material, not as instructions that override the system's intended behavior.

## 7. Retrieval Failure and Empty Results

The system should distinguish between:

- A successful search that returns relevant content.
- A successful search that returns no sufficiently relevant content.
- A retrieval operation that fails.

If retrieval returns no sufficiently relevant content, the assistant should avoid implying that its answer is supported by the course materials.

If retrieval fails, the application should report or log the failure appropriately. It should not silently treat the operation as a successful RAG request.

Whether the application should allow an explicitly identified fallback to general LLM generation after a retrieval failure remains an implementation decision. Any fallback must not misrepresent the response as grounded in retrieved course content.

## 8. Source References

When RAG is enabled, retrieved chunks should retain their source metadata through response generation.

The application should present references only when the corresponding source information is available.

References should help users locate the original course material. They should not imply that every statement in a generated response has been independently verified.

In non-RAG mode, the application should not display course-retrieval references.

## 9. RAG Evaluation

StudyGraph should support a controlled comparison between RAG and non-RAG responses.

To make the comparison meaningful, the following should remain consistent wherever possible:

- Language model and model version.
- Task.
- Tone.
- Traits.
- Target.
- User question.
- Conversation history.
- Generation parameters.

The primary difference should be whether course-specific retrieval is performed and its resulting context supplied to the model.

Evaluation questions should cover topics addressed by the course materials. The resulting answers can then be assessed for relevance, factual correctness, grounding in the course content, and usefulness to the student.

The evaluation should also include questions for which the course knowledge base provides insufficient information, to assess whether the assistant communicates uncertainty appropriately.

## 10. Open Decisions

The following remain open:

- Embedding model.
- Vector store and similarity-search implementation.
- Chunk size and overlap.
- Retrieval strategy and result limits.
- Relevance thresholds, if used.
- Query construction and contextual retrieval.
- Context formatting.
- Source-reference format.
- Evaluation dataset and scoring criteria.