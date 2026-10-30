# StudyGraph

**A local LLM-powered study assistant using Retrieval-Augmented Generation (RAG).**

StudyGraph helps students understand and revise their course material through an AI assistant grounded in their actual lecture slides and notes.

The application uses a predefined knowledge base built from course slides converted from PDF to Markdown. Students can ask questions, request explanations of difficult concepts, and generate practice questions based on the available course material. They can also upload additional materials to extend the knowledge base.

The project explores how locally running language models and Retrieval-Augmented Generation can support learning by grounding AI-generated answers in relevant course materials.

## Key Features

- **Course-specific answers:** Retrieve relevant information from predefined course materials before generating responses.
- **Source references:** Help students trace answers back to the relevant course materials.
- **Study assistance:** Get explanations and generate practice questions based on course content.
- **Optional document uploads:** Extend the knowledge base with personal notes and supplementary materials.
- **Local inference:** Explore running the language model and retrieval pipeline locally without relying on external LLM APIs.

## Technology

- **Python** — Primary programming language
- **LangChain** — LLM application and retrieval framework

Additional technologies and implementation details will be decided during the design and architecture phases.

## Project Documentation

Additional documentation is maintained in the [`docs/`](docs/) directory:

- **Design:** Product goals, user needs, scope, and design decisions.
- **Architecture:** System components, data flow, and RAG implementation.
- **Requirements:** Functional and non-functional requirements.
- **Synopsis:** Project overview, implementation, evaluation, and reflection.

## Project Status

StudyGraph is an educational software prototype exploring local LLMs and Retrieval-Augmented Generation for course-specific study assistance.