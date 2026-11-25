# Synopsis – StudyGraph: A Local LLM-Powered Study Assistant

*Groupe members:* \
Ahmad Alkaseb - cph-aa540@stud.ek.dk \
Aleksandr Uktamovich Sorokin - also1002@stud.ek.dk \
Jafar Alsukafi - jaal0002@stud.ek.dk \
Jeppe Jeppsson - jeje1006@stud.ek.dk \
Frederik Nicolajsen - frni1004@stud.ek.dk \
Roman Ghazi - rogh1000@stud.ek.dk

Character count: 15795

## 1. Problem, Target Users, Purpose and MVP Scope

Students often work with large amounts of course material distributed across lecture slides, notes and supplementary documents. Finding relevant information, understanding difficult concepts and preparing for examinations can be time-consuming. While general-purpose AI assistants can help explain concepts, their responses are not necessarily grounded in the material taught in a specific course. This can lead to inaccurate explanations, hallucinations or answers that do not reflect the curriculum.

StudyGraph addresses this problem by combining a locally running Large Language Model (LLM) with Retrieval-Augmented Generation (RAG). Rather than relying solely on the model's pretrained knowledge, the application retrieves relevant information from course materials and uses it as context when generating responses.

The primary target users are university students who want assistance understanding and revising their course material. The purpose of the project is to investigate whether a local LLM combined with RAG can provide useful, course-specific learning assistance while maintaining privacy and reducing dependence on external AI services. The project also explores how prompt engineering and retrieval influence the quality and reliability of generated responses.

### MVP Scope

The Minimum Viable Product (MVP) focuses on one predefined course, *LLMs for Developers*, and includes the following features:

- A conversational interface for interacting with the AI assistant.
- Reusable assistant profiles, called Buddies, with configurable teaching characteristics.
- Persistent conversations and conversation history.
- Local language model inference through Ollama.
- Retrieval of course material using ChromaDB, including source references.
- A general-chat mode without course-specific retrieval.
- Support for explanations, summaries and practice questions.

An About page also provides information about the models, knowledge-base index and local data storage.

The MVP deliberately focuses on a limited scope rather than becoming a complete learning management system. Features such as unrestricted course management and supplementary document uploads are outside the initial scope.

## 2. Architecture and Implementation

### 2.1 Overall Architecture

StudyGraph is implemented in Python 3.12 using a modular architecture that separates the user interface, application services, domain models, prompt construction, retrieval, language model integration and persistence.

The main technologies are:

| Technology | Purpose |
|---|---|
| Streamlit | Multi-page web interface |
| LangGraph | Conversation workflow and RAG orchestration |
| Ollama | Local language model and embedding model |
| ChromaDB | Storage and retrieval of embedded course material |
| SQLite | Persistence of Buddies, conversations, messages and configuration snapshots |
| Python and uv | Application development and dependency management |

The selected chat model is `llama3.2:3b`, while `nomic-embed-text` generates 768-dimensional embeddings. Both models run locally through Ollama, allowing the application's core functionality to operate without external hosted LLM APIs.

### 2.2 Application Flow

The application consists of three main pages:

- **Chat:** Students select a Buddy, start conversations, submit questions and receive streaming responses. Retrieved sources can be inspected alongside the answers.
- **Buddies:** Students create and configure reusable assistant profiles based on their preferred teaching style and knowledge level.
- **About:** Displays information about the models, knowledge-base index and local storage.

When a student starts a conversation, the application saves a snapshot of the selected Buddy's configuration. The student can then submit a question and select the desired Task.

The application retrieves the conversation history and constructs a prompt using the four T's, the current message and relevant previous messages. LangGraph determines whether the conversation requires course-specific retrieval.

For course-related conversations, ChromaDB retrieves relevant passages from the indexed material. These passages are included in the prompt sent to Ollama, which generates and streams the response to the interface. Both the user's message and the generated response are stored in SQLite.

For general-chat conversations, the retrieval step is skipped while the same prompt-engineering configuration is maintained. This separation allows the application to support both RAG-based and general LLM interactions.

### 2.3 Local LLM and RAG Implementation

StudyGraph uses RAG to provide the language model with relevant information from the course material. The pipeline consists of two main stages: indexing and retrieval.

**Indexing:** Course documents are collected, converted from PDF to Markdown and cleaned to correct extraction artifacts. The documents are then divided into smaller chunks, transformed into embeddings and stored in ChromaDB together with their source metadata.

**Retrieval:** When a student submits a question, the application generates an embedding of the query and searches ChromaDB for semantically similar chunks. Relevant passages are included in the LLM prompt, allowing the model to generate responses informed by course-specific material.

The current knowledge base contains 85 Markdown documents and approximately 1,660 chunks, covering eight available teaching weeks. The application uses a heading-first chunking strategy with a configured chunk size of 900 and an overlap of 120 to preserve contextual relationships between passages.

The system also distinguishes between retrieval failures and successful retrieval that produces no sufficiently relevant results. This distinction is important because the assistant should not present an answer as course-grounded when retrieval has failed.

## 3. Application of the Four T's and Key Design Decisions

A central design principle of StudyGraph is the application of the four T's: Task, Tone, Traits and Target. These dimensions provide a structured approach to prompt engineering, allowing students to customise how the assistant behaves and communicates.

- **Task:** Defines what the assistant should do, such as explaining concepts, summarising lectures, generating practice questions or reviewing answers.
- **Tone:** Determines the communication style, such as friendly, formal, encouraging or academic.
- **Traits:** Describes behavioural characteristics, such as being patient, analytical, critical or Socratic.
- **Target:** Specifies the intended audience and knowledge level, ranging from beginners to students preparing for examinations.

These dimensions are implemented through reusable assistant profiles called Buddies. Each Buddy stores its Tone, Traits and Target, while Task is selected independently for each message. This allows students to perform different learning activities without creating separate profiles for every task.

Another important design decision is saving a snapshot of the Buddy configuration when a conversation begins. Consequently, editing a Buddy does not automatically change the behaviour of existing conversations. This improves consistency and makes comparisons more reproducible.

The application also separates RAG and non-RAG execution while retaining the same prompt construction process. This makes it possible to investigate the contribution of retrieval without unnecessarily changing other prompt-engineering variables.

## 4. Machine Learning Concepts, Data Preparation and Retrieval Choices

StudyGraph applies several concepts from machine learning and natural language processing, particularly embeddings, semantic similarity and Retrieval-Augmented Generation.

### Embeddings and Semantic Retrieval

An embedding model transforms text into numerical vectors that represent semantic information. Texts with similar meanings generally have vectors that are closer together in the embedding space.

StudyGraph uses `nomic-embed-text` to generate 768-dimensional embeddings for both course-material chunks and student questions. This enables the system to retrieve relevant information even when a student uses different wording from the original lecture material.

ChromaDB was selected as the vector database because it provides a straightforward local solution for semantic search and supports metadata filtering.

### Data Preparation and Retrieval Strategy

The dataset consists of lecture materials from the *LLMs for Developers* course, covering weeks 1, 2, 3, 4, 6, 8, 9 and 10. Weeks 5 and 7 contained no material.

The original PDF documents are converted into Markdown to make them easier to process while preserving headings and textual structure. The extracted content is cleaned, divided into chunks and associated with metadata so retrieved passages can be traced to their original sources.

A heading-first chunking strategy is used to preserve the relationship between headings and their content. Overlapping chunks help reduce the risk of losing information at chunk boundaries.

The application currently retrieves semantically similar chunks and supplies them to the language model as contextual information. However, the optimal number of retrieved chunks and an appropriate relevance threshold remain subject to further evaluation.

Although RAG can improve the relevance of generated responses, it does not guarantee correctness. The quality of the results depends on the source material, chunking strategy, embedding model, retrieval process and language model.

## 5. Results and Reflection: Linear Regression versus Local LLM + RAG

### 5.1 Experimental Setup

A separate experiment was conducted to compare a traditional machine learning model with a local LLM using RAG. The objective was to predict the daily revenue of an ice-cream stand based on temperature.

The dataset contained 500 observations with two variables: temperature as the input feature and revenue as the prediction target.

The data was divided into training, validation and test sets using a 70/15/15 split with `random_state=42`, resulting in 361 training observations, 64 validation observations and 75 test observations.

Three held-out test observations were selected to represent the coldest, median and warmest temperatures. Their actual revenue values were hidden from both prediction approaches until evaluation.

### 5.2 Prediction Approaches

**Linear Regression**

The first approach used Scikit-learn's `LinearRegression`, trained on the 361 training observations.

The fitted regression equation was:

**Revenue = 21.2581 × Temperature + 49.8138**

Linear regression learns the relationship between temperature and revenue by minimising the sum of squared residuals. It provides an interpretable and relatively simple prediction model for this numerical task.

**Local LLM with RAG**

The second approach used `qwen2.5-coder:7b` through Ollama, together with `nomic-embed-text` for embeddings.

A separate ChromaDB collection was created containing 12 reference observations selected exclusively from the training data. For each prediction, the system retrieved the three most semantically similar observations and provided them to the LLM as context.

The model was instructed to return a numerical prediction without executing code or using regression formulas.

An additional experiment used the same LLM without retrieval to investigate the contribution of RAG.

### 5.3 Experimental Results

The recorded results were:

| Temperature | Actual Revenue | Linear Regression | LLM + RAG | LLM without RAG |
|---|---:|---:|---:|---:|
| 0.27 | 32.55 | 55.49 | 55.39 | 100 |
| 23.59 | 542.61 | 551.31 | 552.82 | 1500 |
| 40.47 | 918.39 | 910.21 | 630.00 | 1000 |
| **Mean Absolute Error** | | **13.28** | **107.15** | **368.82** |

Linear regression achieved the lowest Mean Absolute Error (MAE) of 13.28, compared with 107.15 for the LLM with RAG and 368.82 for the LLM without retrieval.

Measured by MAE, linear regression performed approximately eight times better than the LLM with RAG. However, RAG reduced the LLM's prediction error by approximately 71% compared with generation without retrieval.

### 5.4 Reflection and Interpretation

The experiment demonstrates an important distinction between traditional predictive machine learning and generative language models.

Linear regression learns numerical coefficients from training data and uses them to calculate predictions. Its objective directly matches the numerical task, making it more suitable for this type of structured data.

The LLM, in contrast, generates predictions based on the information provided in its context. Retrieving relevant examples does not necessarily enable it to identify or reproduce the underlying numerical relationship.

This limitation was particularly visible in the warmest-temperature test case. The retrieved reference observations were all below approximately 26 degrees, while the test input was 40.47 degrees. As a result, the LLM predicted a revenue of 630 compared with the actual value of 918.39.

The experiment also revealed a limitation of semantic retrieval for numerical data. The embedding model retrieved nearly identical reference observations for all three temperature questions rather than prioritising values based on numerical distance.

For structured numerical tasks, numerical nearest-neighbour retrieval would therefore be more appropriate than relying exclusively on semantic similarity.

Overall, the findings suggest that model selection should depend on the problem being solved. Traditional machine learning is better suited to numerical prediction tasks requiring accuracy, reproducibility and interpretability, while LLMs are more useful for natural-language explanations and interactions with unstructured information.

### 5.5 Limitations and Future Improvements

The experiment has several limitations. Only three held-out observations were used for the final LLM comparison, which is insufficient for drawing broad statistical conclusions. Additionally, the experiment was limited to one dataset, one local LLM configuration and one embedding model.

The results may therefore differ when using other models, datasets or retrieval strategies.

Possible improvements include:

- Evaluating predictions on a larger number of test observations.
- Comparing additional regression models and local LLMs.
- Investigating hybrid retrieval that combines semantic search with numerical nearest-neighbour methods.
- Testing different chunk sizes, overlap settings and retrieval depths.
- Introducing relevance thresholds and reranking to improve retrieval quality.
- Evaluating generated answers for factual correctness, relevance, grounding and usefulness.
- Improving how the assistant communicates uncertainty when information is missing.

It is important to distinguish the completed regression experiment from the broader evaluation of StudyGraph. While the regression experiment provides measured results, the formal evaluation of course-related RAG responses remains unfinished. Consequently, the numerical findings should not be interpreted as a direct measurement of the educational assistant's overall effectiveness.

## 6. Conclusion

StudyGraph demonstrates how a locally running LLM can be combined with Retrieval-Augmented Generation to create a personalised study assistant grounded in course-specific learning materials.

The application integrates local language model inference, semantic retrieval, prompt engineering through the four T's and persistent conversation management into a modular system.

The regression experiment highlights both the potential and limitations of RAG. Although retrieval improved the LLM's numerical predictions compared with generation without retrieval, linear regression performed substantially better for the structured prediction task. This demonstrates the importance of selecting appropriate machine learning methods based on the problem.

Overall, StudyGraph provides a functional prototype that explores the use of local LLMs and RAG in educational applications. Further evaluation of retrieval quality, answer correctness and the student learning experience is necessary before drawing conclusions about its effectiveness as a complete learning solution.