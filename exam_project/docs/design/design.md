# StudyGraph — Product Design

## 1. Product Vision

StudyGraph is a local AI study assistant designed to help students learn course material through personalized conversations.

Unlike a general-purpose chatbot, StudyGraph allows students to create reusable study assistants called **Buddies**. Each Buddy has a configurable teaching style and can optionally be connected to a course knowledge base.

The application combines conversational AI, the four prompt-engineering dimensions Task, Tone, Traits, and Target, and Retrieval-Augmented Generation (RAG).

The goal is to create a simple learning experience while demonstrating how prompt engineering and retrieval can influence AI-generated responses.

## 2. Target Users

### Primary User: Student

The primary user is a student who wants to understand course material, prepare for examinations, and explore difficult concepts.

The student may have different learning preferences depending on the subject, difficulty, or learning objective.

Typical goals include:

- Understanding unfamiliar concepts.
- Reviewing lecture material.
- Practicing questions before an examination.
- Receiving explanations adapted to their current knowledge level.
- Exploring the difference between general AI answers and answers grounded in course materials.

### Secondary User: Project Evaluator

The project evaluator needs to understand how the application demonstrates the assignment's technical and academic objectives.

The application should make it possible to demonstrate:

- The four prompt-engineering dimensions.
- The use of a local LLM.
- Retrieval from predefined course materials.
- The difference between RAG and non-RAG responses.

## 3. Problem Statement

Students have different learning needs, but a generic chatbot may not consistently adapt its explanations, communication style, or teaching approach to those needs.

Furthermore, a general-purpose LLM may provide answers based on its existing knowledge rather than the specific material taught in a course.

StudyGraph addresses these problems through two complementary mechanisms:

1. **Personalization:** Reusable Buddies let students configure how the assistant communicates and teaches.
2. **Course grounding:** Optional course associations enable retrieval from predefined course materials before generating answers.

The application also provides a practical setting for examining how these mechanisms affect the usefulness and accuracy of AI-generated responses.

## 4. Product Concept

The product is organized around three core concepts.

### Buddies

A Buddy is a reusable study assistant configuration.

It defines:

- **Target:** Who the assistant is teaching.
- **Tone:** How the assistant communicates.
- **Traits:** Which characteristics the assistant should exhibit.
- **Course:** Which course knowledge base to use, if any.

Users can create multiple Buddies for different learning preferences.

### Conversations

A conversation is an individual chat session associated with a Buddy.

Users can reuse Buddies across conversations. Each conversation preserves a snapshot of the Buddy configuration used when it was created.

This keeps existing conversations consistent when a reusable Buddy is subsequently edited.

### Tasks

A Task defines what the student wants the assistant to do in a particular interaction.

Examples include explaining a concept, summarizing lecture notes, or generating practice questions.

Tasks are independent of Buddy configurations, allowing students to perform different learning activities without creating a new Buddy for each one.

## 5. Design Principles

### 5.1 Simplicity First

The application should prioritize the core study workflow over advanced configuration.

Students should be able to start a conversation quickly, while Buddy customization remains accessible when needed.

### 5.2 Personalization Without Repetition

Users should configure a Buddy once and reuse it across conversations.

The interface should make it easy to identify and select the appropriate Buddy without repeatedly entering the same preferences.

### 5.3 Explicit Course Grounding

Users should understand whether a conversation uses course-specific retrieval.

Course selection should be visible during Buddy creation and identifiable when using a conversation.

The application should not imply that a response is grounded in course materials when retrieval has not been performed.

### 5.4 Transparent AI Behavior

The interface should distinguish generated responses from retrieved source material.

Where practical, users should be able to inspect the course materials supporting an answer.

The application should communicate when relevant course information is unavailable rather than presenting unsupported claims as course facts.

### 5.5 Local-First Processing

The core experience should use a locally running LLM and avoid unnecessary external data transfers.

The interface should remain understandable even when local model inference takes time or encounters an error.

### 5.6 Testable Design

The product should make it possible to compare different prompt configurations and RAG behavior.

The interface and underlying data model should preserve enough information to understand which configuration produced a response.

## 6. Scope of the Initial Product

The initial version focuses on a small, coherent learning workflow.

Users should be able to:

1. Create and save a Buddy.
2. Configure its Target, Tone, and Traits.
3. Optionally select the course *LLMs for Developers*.
4. Start a conversation using a saved Buddy.
5. Ask questions and receive AI-generated responses.
6. Revisit conversations after restarting the application.
7. Reuse Buddies across multiple conversations.
8. Compare course-grounded and general AI responses.

Only one course is available in the initial version. Adding courses dynamically is outside the current scope.

## 7. Success Criteria

The product should be considered successful as a prototype if:

- A student can understand the Buddy concept without technical guidance.
- Creating and selecting a Buddy is straightforward.
- Buddy configurations and conversations persist across sessions.
- The four prompt-engineering dimensions can be demonstrated clearly.
- Course-associated conversations retrieve relevant course material.
- Conversations without a course do not use course-specific retrieval.
- The two modes can be compared without unnecessarily changing other variables.

## 8. Future Opportunities

Potential improvements beyond the initial version include:

- Additional courses.
- More predefined Buddy templates.
- Importing supplementary study materials.
- Better source exploration.
- Saved Task presets.
- Comparison tools for evaluating different Buddy configurations.
- Progress tracking and study-session summaries.

These opportunities should not delay implementation of the core prototype.