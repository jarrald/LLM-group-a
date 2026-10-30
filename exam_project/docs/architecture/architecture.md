# StudyGraph — System Architecture

## 1. Overview

StudyGraph is a local LLM-powered study assistant that combines conversational AI, configurable study Buddies, and optional Retrieval-Augmented Generation (RAG).

The application allows users to create reusable Buddies that define how the AI communicates and teaches. When starting a conversation, the user selects a Buddy whose configuration is captured in a snapshot for that conversation.

A Buddy can optionally be associated with a course. For V1, the only available course is *LLMs for Developers*. Course-associated Buddies use RAG to retrieve relevant course material, while Buddies without a course use the LLM without course-specific retrieval.

The system is designed to support a direct comparison between these two modes while keeping the prompt-engineering configuration consistent.

## 2. Architectural Principles

The architecture follows these principles:

- **Separation of concerns:** User interaction, prompt construction, retrieval, persistence, and model inference have distinct responsibilities.
- **Local-first processing:** Core application functionality should run locally without depending on an external hosted LLM API.
- **Configurable behavior:** Task, Tone, Traits, and Target are represented as distinct prompt-engineering dimensions.
- **Reusable configuration:** Buddies can be saved and associated with multiple conversations.
- **Conversation consistency:** Each conversation stores a snapshot of the Buddy configuration used when it was created.
- **Optional retrieval:** Course-specific retrieval can be enabled or disabled according to the selected Buddy's course association.
- **Replaceable components:** Technology-specific implementations should be isolated behind clear interfaces where practical.

## 3. System Components

### 3.1 User Interface

The user interface provides the main interaction points for StudyGraph.

Responsibilities:

- Display the conversation history.
- Allow users to send messages and receive responses.
- Create, view, and edit Buddies.
- Configure a Buddy's name, Target, Tone, Traits, and optional course.
- Select a Buddy when starting a conversation.
- Display saved conversations.
- Present source references when available.

The interface should not implement retrieval logic or construct model prompts directly.

### 3.2 Buddy Management

The Buddy management component handles reusable study profiles.

Responsibilities:

- Create and validate Buddy configurations.
- Retrieve and update saved Buddies.
- Associate a Buddy with an optional course.
- Persist configurations across application sessions.
- Provide configuration data when a conversation is created.

A Buddy represents a reusable configuration, not an individual chat session.

### 3.3 Conversation Management

The conversation management component handles chat sessions and their histories.

Responsibilities:

- Create conversations using a selected Buddy.
- Capture the Buddy configuration in a conversation snapshot.
- Persist conversations and messages.
- Retrieve conversation history.
- Associate messages with the appropriate conversation.
- Supply relevant history when generating follow-up responses.

Existing conversations should retain their original Buddy snapshot when the reusable Buddy is edited.

### 3.4 Prompt Construction

The prompt construction component combines the current interaction with the selected conversation configuration.

It incorporates the four prompt-engineering dimensions:

- **Task:** The activity the AI should perform.
- **Tone:** The desired communication style.
- **Traits:** The characteristics the AI should exhibit.
- **Target:** The intended audience or knowledge level.

The component should construct prompts consistently for both RAG and non-RAG conversations.

Retrieved course material is supplied as contextual information when RAG is enabled. It is not itself a replacement for the Buddy configuration or the current Task.

### 3.5 Retrieval

The retrieval component provides course-specific context for conversations associated with a course.

Responsibilities:

- Accept a user query and relevant conversation context.
- Retrieve relevant content from the selected course's knowledge base.
- Return retrieved passages and their associated source metadata.
- Handle cases where no relevant content is found.
- Provide source information for citations.

For V1, the retrieval component supports the predefined course *LLMs for Developers*.

When a conversation has no associated course, the application bypasses course-specific retrieval.

### 3.6 Language Model Integration

The language model integration component communicates with the locally running LLM.

Responsibilities:

- Accept constructed prompts and contextual information.
- Generate responses.
- Return generated text to the application.
- Handle model errors and unavailable services.

The chosen model and runtime remain implementation decisions.

### 3.7 Persistence

The persistence component stores the application's durable data.

It is responsible for saving and retrieving:

- Buddy configurations.
- Conversations and their configuration snapshots.
- Conversation messages.
- Course metadata.
- Any additional metadata required by the implementation.

The persistence technology has not yet been selected.

## 4. High-Level Data Flow

A typical interaction follows this sequence:

1. The user selects an existing Buddy and starts a conversation.
2. The application creates a conversation and stores a snapshot of the Buddy's configuration.
3. The user submits a message.
4. The application retrieves the conversation's configuration and relevant message history.
5. The prompt construction component combines the Task, Tone, Traits, and Target.
6. If the conversation has an associated course, the retrieval component searches the course knowledge base.
7. Retrieved passages are included in the model input when available.
8. The local LLM generates a response.
9. The application returns the response and any applicable source references.
10. The user message and assistant response are persisted.

If no course is associated with the conversation, steps involving course-specific retrieval are skipped.

## 5. RAG and Non-RAG Modes

StudyGraph supports two modes through the same chat workflow.

### RAG Mode

A conversation uses RAG when its Buddy snapshot contains an association with *LLMs for Developers*.

The system retrieves relevant course content and supplies it to the LLM as context.

The assistant can then generate answers grounded in the available course material and provide source references where supported.

### Non-RAG Mode

A conversation uses non-RAG mode when its Buddy snapshot has no associated course.

The system sends the constructed prompt and relevant conversation history to the LLM without retrieving course-specific context.

The assistant continues to follow the same Task, Tone, Traits, and Target configuration.

### Comparison Requirements

The architecture should make it possible to compare the two modes while keeping the model and prompt-engineering configuration consistent.

Differences in retrieval behavior should be isolated from unrelated changes in prompt construction.

## 6. Data Persistence and Consistency

Buddies and conversations must persist across application restarts.

When a conversation is created, its Buddy configuration is copied into a snapshot. The snapshot contains the configuration required to reconstruct the conversation's original prompt behavior, including:

- Buddy name or identifying reference.
- Target.
- Tone.
- Traits.
- Optional course association.

Editing the reusable Buddy affects future conversations but does not automatically modify existing conversation snapshots.

This approach improves consistency when revisiting conversations and evaluating RAG behavior.

The snapshot does not, by itself, guarantee identical generated responses. Model versions, generation settings, retrieved content, and other runtime details can also affect the output.

## 7. Error Handling

The application should handle the following situations gracefully:

- The local LLM is unavailable.
- Model generation fails.
- Retrieval fails or returns no relevant content.
- A conversation or Buddy cannot be loaded.
- Persistence operations fail.
- A user submits an empty message.
- The selected course has no indexed content.

A retrieval failure should be distinguishable from a successful retrieval that returns no relevant results.

The application should not silently treat a retrieval failure as a successful RAG operation.

## 8. Open Architecture Decisions

The following decisions remain open:

- Local LLM runtime and model.
- Embedding model.
- Vector store and retrieval implementation.
- Persistence technology.
- User interface framework.
- Document chunking and indexing strategy.
- Conversation-history management strategy.
- Model generation parameters.
- Testing and evaluation methodology.

These decisions should be made during implementation planning based on project constraints, local hardware, maintainability, and the assignment's evaluation requirements.