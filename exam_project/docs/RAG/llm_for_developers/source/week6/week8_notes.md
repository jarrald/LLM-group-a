RAG means retrieval-augmented generation.

A RAG pipeline does not use a special RAG model.
Instead, it retrieves relevant pieces of text and sends them to the model as context.

In this course version of RAG, the answer should be grounded in the retrieved context.
If the answer is not present in the retrieved context, the system should answer: I don't know.
