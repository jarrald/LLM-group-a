context window exceeded — compacting and retrying

overflow-recovery-compacting

overflow-recovery-compaction-skipped

The request exceeds the model's context window and there is no conversation history to compact — the system prompt, tools, and current input alone are too large. Reduce attached content or switch to a model with a larger context window. (provider reported: Your input exceeds the model's maximum context length. Please shorten your messages and try again.)


# Notes
Context window is 262.1k Tokens, perhaps it read the file and ran out prematurely.

LLM used: Leanstral-1-5, Zero Knowledge European free model.