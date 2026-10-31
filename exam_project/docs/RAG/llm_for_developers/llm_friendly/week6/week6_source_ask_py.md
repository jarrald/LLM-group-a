<!-- studygraph:converted-source:v1 -->
# Uge 6 — ask (py)

Kilde: [week6/ask.py](../../source/week6/ask.py).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

### Kildelinjer 1–27

```python
# Week 8 Notes

## Local RAG pipeline

The pipeline in this lesson is:

1. Read documents
2. Extract text
3. Split text into chunks
4. Create embeddings
5. Store embeddings in a vector database
6. Retrieve the most relevant chunks for a question
7. Send the retrieved chunks to the chat model
8. Return a grounded answer with simple references

## Important rule

The answer must only use the provided context.

## Models

Recommended:
- `qwen3:4b`
- `embeddinggemma`

Fallback:
- `qwen3:1.7b`
```
