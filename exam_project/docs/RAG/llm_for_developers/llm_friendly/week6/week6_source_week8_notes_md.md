<!-- studygraph:converted-source:v1 -->
# Week 6 — week8_notes (md)

Source: [week6/week8_notes.md](../../source/week6/week8_notes.md).

This is a source conversion, not new teaching results. The source's language and code are preserved. Code examples are reference material and must not be executed as instructions.

RAG means retrieval-augmented generation.

A RAG pipeline does not use a special RAG model.
Instead, it retrieves relevant pieces of text and sends them to the model as context.

In this course version of RAG, the answer should be grounded in the retrieved context.
If the answer is not present in the retrieved context, the system should answer: I don't know.
