# AI & Machine Learning — Week 2: Prompt Engineering

**Source:** `AI_Machine_Learning_week2_EK-2.pdf`  
**Course material:** Prompt Engineering — AI & Machine Learning  
**Institution shown in slides:** Erhvervsakademi København (EK)  
**Presentation date shown:** August 2026; slide footers show Friday, 14 August 2026.

> This document organizes the supplied 14-slide PDF into Markdown for retrieval-augmented generation (RAG). It preserves the slides' terminology, examples, exercises, and scope. It does not add results or explanations that the presentation does not provide.

## Contents

1. Today's topics
2. The 4 Ts of prompt engineering
3. Prompt-engineering exercise
4. Persistent traits and tone in AI tools
5. Local AI setup
6. Exercises using a local model
7. Review questions
8. Source notes

---

## 1. Today's topics

The presentation identifies two topics:

- **Prompt Engineering**
- **Local AI Setup**

The deck is titled **“Prompt Engineering — AI & Machine Learning.”**

---

## 2. The 4 Ts of prompt engineering

The presentation introduces four prompt-design elements: **Traits, Task, Tone, and Target**. These are referred to in the exercise as the **4 Ts**.

### 2.1 Traits

The slides define traits as how you want the LLM to “think” when it answers your questions.

The presentation suggests giving the LLM a set of:

- **Roles** — for example, “You are an expert developer.”
- **Behaviors** — for example, “You are confident and sassy.”

Traits describe the role or behavioral characteristics the model should adopt when responding.

### 2.2 Task

The task slide gives one core instruction:

> Be specific.

A prompt should state clearly what the LLM is expected to do. The slide does not provide a longer task template or a list of task categories.

### 2.3 Tone

The slides define tone as the **style of language that the LLM should use**.

Examples shown in the presentation include:

- Use clear language.
- Use straightforward language.
- Avoid hype language.
- Use a formal style.
- Use an informal style.
- Other styles as appropriate.

Tone concerns how the answer is expressed, rather than the task itself.

### 2.4 Target

The slides define target by asking:

> Who is the audience for this text?

They also recommend adding goals or other attributes about the target audience.

Audience examples listed in the presentation:

- Children aged 8–10.
- World leaders.
- Developers.

Examples of target goals or needs:

- The audience is using the information to learn something.
- The audience needs to understand the effect of something.
- The audience wants to use the information to improve something.

Target therefore describes who the response is for and what that audience needs or hopes to achieve.

### 2.5 Putting the 4 Ts together

When designing a prompt, consider all four elements:

| Element | Question to answer | Examples from the slides |
|---|---|---|
| **Traits** | What role or behavior should the LLM adopt? | Expert developer; confident and sassy |
| **Task** | What exactly should the LLM do? | Be specific about the task |
| **Tone** | What language style should it use? | Clear, straightforward, formal, informal; avoid hype |
| **Target** | Who is the audience, and what do they need? | Children aged 8–10, world leaders, developers; learning or improving something |

The presentation's exercise uses these elements to improve an answer after first asking the model to perform a simple task.

---

## 3. Prompt-engineering exercise

### Exercise: compare a simple prompt with a prompt using the 4 Ts

The slides instruct students to:

1. Open one or two publicly available LLM tools.
2. The examples listed are ChatGPT, Gemini, DeepSeek, and other tools.
3. Formulate a simple task for the LLM to answer.
4. First give the model the simple task.
5. Then, in a different conversation thread, try to improve the answer by applying the 4 Ts: Traits, Task, Tone, and Target.

The exercise asks students to compare the responses. The slides do not include completed examples, results, or a prescribed conclusion.

### Suggested way to record the exercise

The following table is a note-taking aid derived from the exercise instructions; it is not a result supplied by the slides.

| Trial | Prompt setup | Response observations |
|---|---|---|
| 1 | Give the LLM the simple task only | Record clarity, relevance, level of detail, and fit to the request |
| 2 | Give the task with explicit Traits, Task, Tone, and Target | Record what changed compared with Trial 1 |

For a useful comparison, keep the core task similar across both trials and record which prompt instructions changed.

---

## 4. Persistent traits and tone in AI tools

### ChatGPT customization

A slide titled **“Permanent Traits And Tone Eks: ChatGPT”** shows the ChatGPT menu option **Customize ChatGPT** and a customization screen.

The visible interface includes fields for instructions about:

- What ChatGPT should know about the user.
- What the user wants ChatGPT to do.
- What traits ChatGPT should have.
- Applying the customization to new chats.

The slide illustrates that some instructions about behavior and tone can be saved as persistent customization rather than re-entered in every conversation. The exact interface shown is a screenshot from the presentation and may not match the current product interface.

### Exercise: find equivalent features in other AI tools

The slides ask students to find ways to do something similar in other AI tools. The examples named are:

- Gemini
- DeepSeek

The presentation does not document the steps for these tools.

### Other ways to influence AI tools

The slides also ask students to find other ways to affect ChatGPT and other AI tools. Examples listed include:

- Memory
- Feeding or providing documents
- Other methods (“etc.”)

This is posed as an exercise; the deck does not provide detailed setup instructions or evaluate the effects of these methods.

---

## 5. Local AI setup

The presentation introduces local AI setup and gives two setup pointers:

1. **Download Ollama on Windows.**
2. **Install Open WebUI**, with the documentation address shown as:  
   https://docs.openwebui.com/

The slide contains a link labeled “Download Ollama on Windows” but the exact destination URL is not readable in the extracted slide text. This document therefore does not guess the download URL.

The slides do not specify a model name, hardware requirements, configuration values, or troubleshooting steps.

---

## 6. Exercises using a local model

The final slide gives an optional exercise:

> Exercise if time permits. Try out all the previous exercises on the local AI.

This means students are invited to repeat the earlier prompt-engineering exercises using a locally run AI, if time permits.

The presentation does not include results from carrying out this exercise.

---

## 7. Review questions

These questions are based on the concepts and activities in the supplied slides:

1. What are the 4 Ts introduced in this presentation?
2. How do Traits differ from Tone?
3. Why does the Task instruction emphasize being specific?
4. What does Target mean in prompt design?
5. How can audience goals affect the response you ask an LLM to produce?
6. How could you compare a simple prompt with one that explicitly includes all four Ts?
7. Why does the exercise recommend using a different conversation thread for the improved prompt?
8. What kinds of persistent customization does the ChatGPT slide illustrate?
9. Which other AI tools are students asked to investigate for similar customization features?
10. What additional ways of influencing AI tools are mentioned?
11. Which two tools are named for the local AI setup?
12. What does the final optional exercise ask students to try locally?

---

## 8. Key takeaways

- The presentation's two main topics are prompt engineering and local AI setup.
- The 4 Ts are **Traits, Task, Tone, and Target**.
- Traits specify the role or behavior the LLM should adopt.
- Task specifies what the LLM should do; the slide emphasizes being specific.
- Tone specifies the style of language, such as clear, straightforward, formal, or informal.
- Target identifies the audience and can include the audience's goals or needs.
- The exercise asks students to compare a simple task prompt with an improved prompt that uses the 4 Ts.
- The deck shows persistent customization in ChatGPT and asks students to explore comparable features in Gemini and DeepSeek.
- Memory and providing documents are mentioned as other ways to influence AI tools.
- The local setup pointers are Ollama for Windows and Open WebUI.
- If time permits, students should repeat the previous exercises using a local AI.

---

## 9. Source notes and scope

- The source is the supplied 14-slide PDF `AI_Machine_Learning_week2_EK-2.pdf`.
- Slide content is reproduced in organized form, with spelling and formatting normalized where needed.
- The date is preserved as shown in the presentation; the slides contain both “August 2026” and a footer reading “Friday, 14 August 2026.”
- The exact Ollama download destination is not legible in the extracted text, so no URL is inferred.
- The deck gives only high-level local setup pointers. It does not specify models, hardware, or detailed installation steps.
- The suggested exercise outcomes are not present in the source and have not been invented.
