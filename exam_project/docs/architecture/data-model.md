# StudyGraph — Data Model

## 1. Overview

StudyGraph distinguishes between reusable Buddy configurations, individual conversations, conversation messages, and course metadata.

The data model must support persistent storage, Buddy reuse, optional course associations, and stable conversation configuration snapshots.

This document describes the conceptual data model without committing to a specific database or storage technology.

## 2. Entities

### 2.1 Buddy

A Buddy represents a reusable study assistant configuration.

Conceptual attributes:

| Attribute | Description |
|---|---|
| ID | Unique identifier for the Buddy. |
| Name | User-defined name. |
| Target | Intended audience or knowledge level. |
| Tone | Preferred communication style. |
| Traits | One or more characteristics the AI should exhibit. |
| Course ID | Optional reference to a course. |
| Created At | Creation timestamp. |
| Updated At | Last modification timestamp. |

Buddies must persist across application sessions.

Users should be able to reuse a Buddy across multiple conversations.

### 2.2 Course

A Course represents a collection of learning materials available for retrieval.

Conceptual attributes:

| Attribute | Description |
|---|---|
| ID | Unique identifier for the course. |
| Name | Course name. |
| Description | Optional course description. |
| Knowledge Base Reference | Reference to the associated indexed course materials. |

For V1, the application provides one predefined course:

- LLMs for Developers.

A Buddy's course reference is optional. A missing course association means course-specific retrieval is disabled.

The ability to create or manage additional courses is outside the scope of V1.

### 2.3 Conversation

A Conversation represents a persistent chat session.

Conceptual attributes:

| Attribute | Description |
|---|---|
| ID | Unique identifier for the conversation. |
| Title | Optional conversation title. |
| Buddy ID | Reference to the reusable Buddy, when available. |
| Buddy Snapshot | Copy of the Buddy configuration used when the conversation was created. |
| Created At | Creation timestamp. |
| Updated At | Last modification timestamp. |

The Buddy ID provides a relationship to the reusable Buddy.

The Buddy Snapshot preserves the configuration used by the conversation.

The snapshot must contain the values required to reconstruct the original Target, Tone, Traits, and course association. It should also retain the Buddy name for display and historical context.

The application must not depend exclusively on the current Buddy record to determine how an existing conversation behaves.

### 2.4 Message

A Message represents an individual entry in a conversation.

Conceptual attributes:

| Attribute | Description |
|---|---|
| ID | Unique identifier for the message. |
| Conversation ID | Reference to the containing conversation. |
| Role | Message role, such as user or assistant. |
| Content | Message text. |
| Created At | Creation timestamp. |
| Sources | Optional source references associated with the response. |

Messages belong to a single conversation and should be persisted in an order that supports reconstructing the conversation history.

The implementation may introduce additional metadata if required by the selected LLM integration.

## 3. Relationships

The conceptual relationships are:

- A Buddy can be associated with zero or one course.
- A Buddy can be reused by multiple conversations.
- A conversation can reference a reusable Buddy.
- A conversation stores its own Buddy configuration snapshot.
- A conversation contains multiple messages.
- A course has an associated knowledge base.

The conversation snapshot is independent of subsequent changes to the reusable Buddy.

## 4. Buddy Snapshot Behavior

When a conversation is created:

1. The application loads the selected Buddy.
2. The application validates its configuration.
3. The application copies the configuration into the new conversation's snapshot.
4. The conversation and snapshot are persisted.

When the reusable Buddy is edited, the change applies to new conversations.

Existing conversations continue to use their stored snapshots.

If a Buddy is deleted, the application should preserve existing conversations and their snapshots. Whether the reusable Buddy can be deleted while conversations reference it will depend on the chosen persistence implementation.

## 5. Course and Retrieval Behavior

The course association in the conversation snapshot determines whether course-specific RAG is enabled.

| Snapshot course association | Behavior |
|---|---|
| LLMs for Developers | Use the associated course knowledge base for retrieval. |
| No course | Do not perform course-specific retrieval. |

The course association should be represented explicitly rather than inferred from the Buddy name or prompt text.

This makes retrieval behavior predictable and testable.

## 6. Persistence Requirements

The selected persistence technology must support:

- Saving and loading Buddy configurations.
- Saving and loading conversations.
- Persisting conversation messages.
- Preserving conversation snapshots.
- Maintaining relationships between conversations, Buddies, and courses.
- Handling application restarts without losing saved data.

The implementation should validate data before writing it and handle failed operations without silently losing user data.

## 7. Data Integrity and Security

The implementation should ensure that:

- Every persisted entity has a stable identifier.
- Every message references an existing conversation.
- Course references point to valid courses.
- Buddy snapshots contain valid configuration values.
- User-provided names and configuration fields are validated.
- Conversation history is loaded only within the appropriate conversation context.

If user accounts or multiple users are introduced, authorization must be enforced when reading, modifying, or deleting Buddies and conversations. A client-provided identifier must not be sufficient to access another user's data.

Authentication and multi-user access are not assumed to be required for the initial prototype.

## 8. Open Decisions

The following details remain open until the persistence technology is selected:

- Database schema and field types.
- How Traits are represented in storage.
- Snapshot serialization format and versioning.
- Whether message content and source metadata are stored separately.
- Deletion and retention behavior.
- Whether generation settings and model metadata are stored for experiment reproducibility.