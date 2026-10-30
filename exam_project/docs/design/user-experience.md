# StudyGraph — User Experience Design

## 1. Overview

StudyGraph should provide a straightforward interface for managing study Buddies, starting conversations, and interacting with the AI assistant.

The experience should prioritize the chat while making Buddy configuration and course selection easy to access.

The design should avoid exposing unnecessary technical details such as embeddings, vector stores, retrieval parameters, or prompt templates to the student.

## 2. Main User Journeys

### 2.1 First-Time User

A first-time user should be able to start studying without configuring every setting manually.

The intended journey is:

1. Open StudyGraph.
2. View the available Buddies or a default Buddy.
3. Select a Buddy or create a new one.
4. Start a conversation.
5. Ask a question about a course topic or another subject.
6. Receive an AI-generated response.

The application should provide sensible defaults so the user is not required to understand prompt engineering before getting started.

### 2.2 Creating a Buddy

The intended journey is:

1. Open the Buddy management interface.
2. Choose to create a Buddy.
3. Enter a name.
4. Define the Target.
5. Choose a Tone.
6. Select one or more Traits.
7. Optionally select a course.
8. Save the Buddy.
9. Start a conversation using the new Buddy.

The course selector should offer:

- No course.
- LLMs for Developers.

The interface should explain that selecting the course enables course-specific retrieval, while leaving the course unselected creates a general AI Buddy without course-specific RAG.

### 2.3 Starting a Conversation

The intended journey is:

1. Choose to start a new conversation.
2. Select a saved Buddy.
3. Review the selected Buddy's identity and, where useful, its course association.
4. Start chatting.
5. Receive responses based on the Buddy configuration and the selected retrieval mode.

The application creates a conversation-specific snapshot of the selected Buddy configuration.

Users should not need to configure the Buddy again for each conversation.

### 2.4 Continuing an Existing Conversation

The intended journey is:

1. Open the conversation list.
2. Select a previous conversation.
3. Review the existing message history.
4. Continue asking questions.
5. Receive responses using the conversation's saved configuration.

The conversation should remain associated with its original configuration snapshot even if the reusable Buddy has since been edited.

### 2.5 Comparing RAG and Non-RAG

The intended journey is:

1. Create a Buddy associated with *LLMs for Developers*.
2. Create a second Buddy with the same Target, Tone, and Traits, but without a course.
3. Ask the same question in separate conversations.
4. Compare the responses.
5. Inspect available course references in the RAG conversation.
6. Evaluate differences in relevance, factual correctness, and alignment with the course material.

The interface does not need a dedicated experimental dashboard for V1. The comparison can be performed through ordinary conversations.

## 3. Main Application Areas

### 3.1 Chat

The chat is the primary working area.

It should contain:

- The conversation history.
- A message input field.
- A send action.
- An indication of the selected Buddy.
- An indication of whether course-specific retrieval is enabled.
- Source references when available.
- Clear feedback while a response is being generated.

The message input should support ordinary natural-language requests, allowing the user to express a Task directly.

### 3.2 Buddy Management

The Buddy management area allows users to:

- View saved Buddies.
- Create a Buddy.
- Edit a Buddy.
- Select a Buddy for a new conversation.

Each Buddy should have a recognizable name and a concise summary of its configuration.

The course association should be visible enough that users can distinguish course-grounded Buddies from general AI Buddies.

### 3.3 Buddy Creation and Editing

The Buddy form should group related settings together:

**Identity**
- Buddy name.

**Teaching style**
- Target.
- Tone.
- Traits.

**Course grounding**
- Optional course selection.

The interface should use clear labels and examples to help users understand each field.

A user should not need to write a complete system prompt manually.

### 3.4 Conversation History

The conversation list should make previously saved conversations accessible.

At minimum, users should be able to identify and reopen conversations.

Conversation titles, renaming, and advanced organization can be added if time permits.

## 4. Interaction States

The application should communicate important states clearly.

### Loading

While a response is being generated, the interface should indicate that processing is in progress.

The interface should prevent accidental duplicate submissions where appropriate.

### Empty Conversation

A new conversation should display a clear invitation to ask a question.

Suggested example prompts can help first-time users understand the assistant's capabilities.

### Empty Knowledge Base

If a course is selected but its knowledge base contains no indexed documents, the application should communicate that course-grounded answers are currently unavailable.

It should not silently imply that RAG has successfully grounded a response.

### Retrieval Without Relevant Results

If retrieval succeeds but finds no sufficiently relevant material, the interface should avoid presenting the response as supported by the course knowledge base.

### Error

If the local LLM is unavailable or a request fails, the interface should provide understandable feedback and allow the user to retry where appropriate.

### Saving

The interface should communicate save failures rather than silently losing Buddy or conversation data.

## 5. Usability Guidelines

- Use plain language rather than implementation-specific terminology.
- Keep Buddy configuration separate from the chat interface.
- Make the selected Buddy easy to identify.
- Make course selection optional and explicit.
- Provide sensible defaults.
- Preserve user input when recoverable errors occur.
- Keep the chat history readable.
- Distinguish source references from generated text.
- Avoid unnecessary configuration before a user can start chatting.

## 6. Accessibility

The interface should aim to provide:

- Clear labels for form controls.
- Keyboard-accessible navigation and submission.
- Sufficient contrast between text and background.
- Visible focus indicators.
- Readable typography and spacing.
- Clear error messages associated with the relevant input.
- A layout that remains usable at different window sizes.

## 7. V1 UX Boundaries

The initial experience does not require:

- Multiple courses.
- Sharing Buddies between users.
- A dedicated evaluation dashboard.
- Advanced conversation organization.
- Custom visual themes.
- Complex prompt editing.

The priority is a usable chat experience with persistent Buddies, optional course grounding, and a clear demonstration of the four prompt-engineering dimensions.