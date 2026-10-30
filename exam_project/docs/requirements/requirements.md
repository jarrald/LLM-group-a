# StudyGraph — Requirements

## 1. Purpose

StudyGraph is a study assistant that uses a locally running Large Language Model (LLM) to help students understand and revise course material.

The application allows students to create reusable study profiles called **Buddies**. Each Buddy defines a preferred Target, Tone, and Traits, allowing students to customize how the AI teaches and communicates.

When creating a Buddy, users can optionally associate it with a course. Course-associated Buddies use Retrieval-Augmented Generation (RAG) to retrieve relevant course material, while Buddies without a course act as general AI assistants without course-specific retrieval.

For V1, the application supports one predefined course: **LLMs for Developers**.

This design enables users to compare AI responses generated with and without RAG while keeping the prompt-engineering configuration consistent.

## 2. Core Concepts

### 2.1 Buddy

A Buddy is a reusable configuration that defines how the AI assistant should communicate and teach.

Each Buddy contains:

- **Name:** A name that helps the user identify the Buddy.
- **Target:** The intended audience or knowledge level.
- **Tone:** The preferred communication style.
- **Traits:** The characteristics the AI should exhibit.
- **Course:** An optional association with a course that determines whether course-specific RAG is used.

Users can create, view, edit, and reuse their Buddies across application sessions.

Examples include:

- **Patient Tutor:** Beginner-friendly, encouraging, and patient.
- **Exam Coach:** Exam-focused, challenging, and concise.
- **Socratic Mentor:** Guides the student through questions instead of immediately providing answers.

### 2.2 Course

A course represents a collection of learning materials that can be used to ground AI responses through RAG.

For V1, the application supports one predefined course:

- **LLMs for Developers**

Users cannot create additional courses in V1.

Selecting this course enables retrieval from its associated knowledge base. Leaving the course unselected disables course-specific retrieval.

### 2.3 Conversation

A conversation is an individual chat session between a user and the AI assistant.

Each conversation contains:

- A message history.
- A reference to the Buddy used to create it, where applicable.
- A snapshot of the Buddy configuration used when the conversation was created.
- The context needed to answer follow-up questions.
- Access to course material through RAG when the conversation's Buddy snapshot has an associated course.

Users can start new conversations using existing Buddies or create new Buddies for different learning goals.

Conversations and their message histories must persist across application sessions.

### 2.4 Buddy Configuration Snapshot

A Buddy configuration snapshot preserves the Buddy settings used when a conversation is created.

The snapshot includes the Buddy's name, Target, Tone, Traits, and optional course association.

Editing the reusable Buddy affects new conversations but does not silently change the configuration of existing conversations.

Snapshots support consistent behavior when revisiting conversations and improve reproducibility when comparing RAG and non-RAG responses.

A configuration snapshot does not, by itself, guarantee identical model outputs. Model versions, generation parameters, conversation history, and retrieved content can also affect responses.

### 2.5 Task

Task defines what the user wants the AI to do in a particular interaction.

Examples include:

- Explain a concept.
- Summarize a lecture.
- Generate practice questions.
- Compare two concepts.
- Review an answer.
- Quiz the student.

Task is separate from the Buddy configuration because the same Buddy should be able to perform different study activities without requiring a new Buddy.

## 3. Functional Requirements

### FR-01: AI Chat

The system shall provide a chat interface through which users can submit messages and receive responses from the AI assistant.

### FR-02: Conversation Management

The system shall allow users to start new conversations and access their saved conversations across application sessions.

The system shall persist conversation messages and maintain their ordering so that conversation history can be reconstructed.

The system should use relevant conversation history to support follow-up questions.

### FR-03: Buddy Creation

The system shall allow users to create a Buddy by providing:

- A name.
- A Target.
- A Tone.
- One or more Traits.
- An optional course selection.

### FR-04: Buddy Management

The system shall allow users to view, edit, and reuse saved Buddies.

Buddy configurations shall persist across application sessions.

Editing a Buddy shall update the reusable configuration without silently modifying the snapshots of existing conversations.

### FR-05: Course Selection

The Buddy creation and editing interface shall provide a course dropdown containing:

- **No course:** The default option.
- **LLMs for Developers:** The predefined course.

The system shall not require users to select a course when creating a Buddy.

Adding, removing, or dynamically managing courses is outside the scope of V1.

### FR-06: Buddy Selection

The system shall allow users to select a Buddy when starting a conversation.

The selected Buddy's configuration shall guide the assistant's responses throughout that conversation.

### FR-07: Buddy Reuse

The system shall allow the same Buddy to be associated with multiple conversations.

Creating a new conversation shall not require creating a new Buddy.

### FR-08: Buddy Configuration Snapshot

When a conversation is created using a Buddy, the system shall save a snapshot of that Buddy's configuration.

The snapshot shall contain the values required to reconstruct the conversation's original prompt configuration, including:

- Buddy name.
- Target.
- Tone.
- Traits.
- Optional course association.

The system shall use the conversation snapshot rather than the current reusable Buddy configuration when determining the configuration of an existing conversation.

The system should preserve the snapshot even if the original Buddy is subsequently edited or deleted.

### FR-09: Task Configuration

The system shall allow users to communicate the Task they want the AI to perform.

The Task may be expressed through the user's message, an explicit task selector, or a combination of these approaches.

The final interface design will determine how Task selection is presented.

The Task may change between messages without requiring the user to create a new Buddy.

### FR-10: Target Configuration

The system shall allow users to define the Target audience or knowledge level when creating or editing a Buddy.

Examples include:

- A beginner with no prior knowledge.
- A student familiar with the fundamentals.
- An advanced student.
- A student preparing for an examination.

### FR-11: Tone Configuration

The system shall allow users to define the Tone of a Buddy's responses.

Examples include:

- Formal and academic.
- Friendly and conversational.
- Encouraging and supportive.
- Concise and direct.

### FR-12: Traits Configuration

The system shall allow users to define the Traits a Buddy should exhibit.

Examples include:

- Patient.
- Analytical.
- Critical.
- Supportive.
- Socratic.

The system should support combining multiple Traits.

### FR-13: Prompt Construction

The system shall combine the four prompt-engineering dimensions when constructing prompts for the LLM:

- **Task:** What the AI should do.
- **Tone:** How the AI should communicate.
- **Traits:** What characteristics the AI should exhibit.
- **Target:** Who the AI is teaching or communicating with.

Task shall be derived from the current interaction or explicit task selection. Tone, Traits, and Target shall come from the selected conversation's Buddy snapshot.

The prompt construction logic shall remain independent of whether RAG is enabled, allowing the same prompt-engineering approach to be used in both configurations.

### FR-14: Default Configuration

The system shall provide a default Buddy or equivalent default configuration so users can start chatting without first creating a Buddy.

The default configuration should use sensible values for Tone, Traits, and Target. Task is
not part of the Buddy: it is chosen per message (FR-09) and defaults to the first preset.

### FR-15: Course-Specific RAG

When a conversation's Buddy snapshot is associated with *LLMs for Developers*, the system shall retrieve relevant information from that course's knowledge base when generating course-related answers.

Retrieved information shall be supplied to the LLM as contextual information for response generation.

The system should preserve source metadata for retrieved content so that relevant references can be presented to the user.

### FR-16: General AI Mode

When a conversation's Buddy snapshot has no associated course, the system shall generate responses without retrieving context from the course knowledge base.

The assistant shall still use the conversation's Buddy configuration and current Task.

This mode provides the baseline for comparing responses generated with and without RAG.

### FR-17: Source References

When RAG is enabled, the system should provide references to relevant course materials when sufficient source information is available.

The system shall not present course-retrieval sources as if they had been consulted when RAG is disabled.

The system should distinguish between a successful retrieval that finds no relevant content and a retrieval operation that fails.

### FR-18: Predefined Course Materials

The system shall use predefined course materials for *LLMs for Developers*, prepared from lecture slides converted from PDF to Markdown.

Users shall not need to upload the primary course materials before using a course-associated Buddy.

The course knowledge base shall be prepared and indexed before the corresponding materials are used for retrieval.

### FR-19: Supplementary Materials

The system may allow users to upload supplementary documents to extend the available knowledge base.

This functionality is optional for the initial prototype.

### FR-20: Local Language Model

The system shall support a locally running LLM for core response generation without depending on an external hosted LLM API.

The specific model and runtime shall be selected during the architecture and implementation phases.

### FR-21: RAG Evaluation Support

The system shall support comparing RAG and non-RAG behavior using the same prompt-engineering configuration.

The implementation should allow the model, Buddy configuration, user question, conversation history, and generation settings to remain consistent while course-specific retrieval is enabled or disabled.

The system should retain sufficient information to identify the configuration used for an evaluated conversation.

## 4. Non-Functional Requirements

### NFR-01: Usability

The interface shall make creating Buddies, selecting a course, and starting conversations understandable without requiring users to understand prompt engineering or RAG.

### NFR-02: Modularity

The implementation should separate the following responsibilities:

- User interface.
- Buddy management.
- Conversation management.
- Prompt construction.
- Retrieval logic.
- Language model integration.
- Persistence.

### NFR-03: Reliability

The system should handle the following situations gracefully:

- Empty messages.
- Missing or invalid configuration values.
- LLM errors.
- Retrieval failures.
- Retrieval returning no relevant results.
- Persistence failures.
- Missing or invalid conversation references.

Common errors should not cause the application to crash or silently lose saved data.

### NFR-04: Grounded Responses

When RAG is enabled, the assistant should prioritize retrieved course material when answering course-specific questions.

It should communicate uncertainty when the available material does not adequately support an answer rather than presenting unsupported claims as facts from the course.

The system should not imply that an answer is grounded in retrieved content when retrieval has failed or has not been performed.

### NFR-05: Privacy

Core conversations, Buddy configurations, and inference should remain local where practical.

Any functionality that sends data to external services should be clearly identified.

### NFR-06: Persistence

Buddy configurations, conversations, messages, and conversation snapshots shall persist across application sessions.

The system shall support application restarts without losing previously saved data.

### NFR-07: Maintainability

The codebase should use clear component boundaries, consistent naming, and automated tests for important behavior.

Particular attention should be given to prompt construction, snapshot consistency, persistence, and retrieval integration.

### NFR-08: Testability

The system should make it possible to test RAG and non-RAG behavior independently.

Prompt construction and retrieval selection should be testable without requiring a live LLM for every test.

### NFR-09: Configuration Consistency

An existing conversation's Buddy configuration shall remain stable when the reusable Buddy is edited.

Any future functionality that allows users to change a conversation's configuration should make that change explicit.

### NFR-10: Local Resource Awareness

The implementation should consider the hardware requirements and resource usage of the selected local LLM and embedding model.

Model and retrieval choices should be appropriate for the development environment and the scope of the prototype.

## 5. Scope and Priorities

### 5.1 Required for V1

- Chat interface.
- Locally running LLM.
- Persistent Buddy configurations.
- Create, view, and edit Buddies.
- Configure Target, Tone, and Traits.
- Optional course selection when creating or editing a Buddy.
- One predefined course: *LLMs for Developers*.
- Persistent conversations and message history.
- Buddy selection when starting a conversation.
- Buddy reuse across multiple conversations.
- Conversation-specific Buddy configuration snapshots.
- Prompt construction using Task, Tone, Traits, and Target.
- Course-specific RAG when a Buddy has a course selected.
- General AI mode without course-specific retrieval.
- A default Buddy or equivalent default configuration.
- Basic error handling.
- Sufficient separation between components to support testing both modes.

### 5.2 Desirable if Time Permits

- Source references in responses.
- Supplementary document uploads.
- Buddy duplication.
- Buddy deletion.
- Conversation renaming and management.
- Predefined Task options.
- Recording model and generation settings for evaluation.
- Additional evaluation tooling for comparing RAG and non-RAG responses.

### 5.3 Out of Scope for V1

- Creating and managing additional courses through the interface.
- Multiple independently managed course knowledge bases.
- User accounts and multi-user collaboration, unless required by the implementation environment.
- Advanced sharing or publishing of Buddies.
- Guaranteed reproduction of identical LLM responses.

## 6. Acceptance Criteria

The initial prototype will be considered functionally complete when:

1. A user can submit messages and receive AI responses.
2. A user can create a Buddy with a name, Target, Tone, and Traits.
3. A user can optionally associate a Buddy with *LLMs for Developers*.
4. The course dropdown provides the predefined course and a no-course option.
5. Buddy configurations persist across application restarts.
6. A user can select and reuse a saved Buddy across conversations.
7. Conversations and their message histories persist across application restarts.
8. Each conversation stores a snapshot of its Buddy configuration.
9. Editing a Buddy does not silently change the configuration of existing conversations.
10. Existing conversations retain their configuration snapshot even if the original Buddy is edited or deleted.
11. A Buddy associated with *LLMs for Developers* triggers course-specific retrieval for course-related questions.
12. A Buddy without a course generates responses without course-specific retrieval.
13. Both modes use the selected conversation configuration and current Task.
14. The implementation supports comparing responses generated with and without RAG while keeping other relevant variables consistent.
15. The application handles common errors without crashing or silently losing saved data.
16. The prototype can demonstrate how the four prompt-engineering dimensions influence assistant behavior.

## 7. Open Design Decisions

> **Status (2026-10-30):** the technology-level decisions are resolved in
> [`../architecture/tech-stack.md`](../architecture/tech-stack.md) and
> [`../plan/decision-log.md`](../plan/decision-log.md). The items below are kept as the
> original requirement record.

The following decisions remain open and will be addressed during the design and architecture phases:

- Which persistence technology to use for Buddies, conversations, messages, and snapshots.
- How Traits are represented and validated.
- The format and versioning strategy for Buddy snapshots.
- Which local LLM runtime and model to use.
- Which embedding model and vector store to use.
- How course documents are split, indexed, and retrieved.
- How the interface presents Task selection.
- How conversation history is incorporated into subsequent prompts.
- Whether supplementary document uploads are included in V1.
- Which model metadata and generation parameters should be recorded for evaluation.
- How the RAG and non-RAG configurations will be evaluated fairly.
- Whether and how the system should fall back to general LLM generation when retrieval fails.