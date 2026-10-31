<!-- studygraph:converted-source:v1 -->
# Uge 6 — week8_notes (md)

Kilde: [week6/week8_notes.md](../../source/week6/week8_notes.md).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

RAG means retrieval-augmented generation.

A RAG pipeline does not use a special RAG model.
Instead, it retrieves relevant pieces of text and sends them to the model as context.

In this course version of RAG, the answer should be grounded in the retrieved context.
If the answer is not present in the retrieved context, the system should answer: I don't know.
