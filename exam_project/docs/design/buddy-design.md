# StudyGraph — Buddy Design

## 1. Purpose

Buddies are the primary personalization mechanism in StudyGraph.

A Buddy represents a reusable AI teaching configuration. Instead of requiring students to repeatedly describe how they want the assistant to behave, the application allows them to configure a Buddy once and reuse it across conversations.

The design also provides a practical way to demonstrate the four prompt-engineering dimensions required by the project: Task, Tone, Traits, and Target.

## 2. The Buddy Concept

A Buddy should feel like a configurable study companion rather than a technical prompt template.

Users create Buddies for different learning preferences and goals.

Examples include:

### Patient Tutor

- **Target:** Beginner.
- **Tone:** Friendly and encouraging.
- **Traits:** Patient, supportive, and explanatory.
- **Course:** LLMs for Developers, if course-specific grounding is desired.

### Exam Coach

- **Target:** Student preparing for an examination.
- **Tone:** Concise and direct.
- **Traits:** Critical, challenging, and analytical.
- **Course:** LLMs for Developers, if course-specific grounding is desired.

### Socratic Mentor

- **Target:** Student familiar with the fundamentals.
- **Tone:** Conversational.
- **Traits:** Curious, analytical, and Socratic.
- **Course:** Optional.

These examples illustrate how the dimensions can be combined. They do not need to be implemented as predefined templates in V1.

## 3. The Four Prompt-Engineering Dimensions

### 3.1 Task

Task describes the activity the user wants the AI to perform.

Examples:

- Explain a concept.
- Summarize a lecture.
- Generate practice questions.
- Compare two approaches.
- Review an answer.
- Ask questions to test the student's understanding.

Task belongs to the current interaction rather than the reusable Buddy configuration.

This separation allows the same Buddy to support different study activities.

For example, a student can ask a Patient Tutor to explain a concept and later ask the same Buddy to generate practice questions.

### 3.2 Tone

Tone describes the communication style of the assistant.

Examples:

- Formal and academic.
- Friendly and conversational.
- Encouraging and supportive.
- Concise and direct.

Tone should influence how information is expressed without changing the underlying factual content intentionally.

### 3.3 Traits

Traits describe the characteristics the assistant should exhibit while interacting with the student.

Examples:

- Patient.
- Analytical.
- Critical.
- Supportive.
- Socratic.
- Detail-oriented.

Multiple Traits can be combined.

The design should help users understand that Traits describe behavior rather than the topic being discussed.

For example, a Socratic Buddy should guide the student through questions, while a patient Buddy should explain difficult concepts without rushing.

### 3.4 Target

Target describes the intended audience or the student's expected knowledge level.

Examples:

- Beginner with no prior knowledge.
- Student familiar with the fundamentals.
- Advanced student.
- Student preparing for an examination.

Target should influence the depth of explanations, terminology, and assumptions about prior knowledge.

It should not prevent the user from asking questions outside the expected level.

## 4. Buddy Configuration Interface

The Buddy creation form should provide the following fields.

| Field | Purpose | Suggested interaction |
|---|---|---|
| Name | Identifies the Buddy. | Text input. |
| Target | Defines the intended audience and knowledge level. | Selectable options with optional custom input. |
| Tone | Defines the communication style. | Selectable options with optional custom input. |
| Traits | Defines the assistant's characteristics. | Multi-select options with optional custom input. |
| Course | Enables optional course-specific retrieval. | Dropdown with a no-course option. |

These controls are design recommendations. The final input types can be adjusted during implementation.

The interface should favor understandable settings over exposing raw prompt syntax.

## 5. Course Association

Course association is separate from the four prompt-engineering dimensions.

For V1, users can select:

- **No course:** The Buddy uses the LLM without course-specific retrieval.
- **LLMs for Developers:** The Buddy uses the associated course knowledge base for RAG.

The no-course option should be the default.

The course selector should explain its effect in plain language. Users should understand that course selection changes the information supplied to the AI, not the Buddy's fundamental teaching style.

The system should not infer course association from a Buddy's name or Traits.

## 6. Reuse and Persistence

Buddies should be saved and available across application sessions.

Users should be able to create a Buddy once and select it for multiple conversations.

Editing a Buddy changes the reusable configuration for future conversations.

Existing conversations retain their saved configuration snapshots. They should not silently inherit changes made to the reusable Buddy.

If the original Buddy is deleted, existing conversations should retain enough information in their snapshots to preserve their configuration and remain understandable.

## 7. Prompt Construction

The prompt construction process should combine the dimensions consistently.

Conceptually, the model input contains:

1. The instructions defining the current Task.
2. The Tone, Traits, and Target from the conversation's Buddy snapshot.
3. Relevant conversation history.
4. Retrieved course material, when RAG is enabled.

These inputs serve different purposes and should remain logically distinct.

The implementation should avoid relying on a single opaque string containing all configuration data, because separating the inputs improves validation, testing, and future changes.

The exact prompt template is an implementation detail and does not need to be part of the Buddy interface.

## 8. Design Goals

The Buddy experience should:

- Make personalization understandable to non-technical users.
- Support reusable configurations.
- Allow different Tasks without requiring new Buddies.
- Keep course grounding independent of teaching style.
- Preserve existing conversation configurations.
- Support a fair comparison of RAG and non-RAG behavior.
- Avoid unnecessary complexity in the initial prototype.

## 9. V1 Boundaries

V1 focuses on creating, editing, saving, selecting, and reusing Buddies.

Advanced features such as sharing, publishing, importing, and community-created Buddies are outside the initial scope.

The design should leave room for these features without requiring them in the initial implementation.