Synopsis – StudyGraph: A Local LLM-Powered Study Assistant
1. Problem, Target Users, Purpose and MVP Scope

Students often work with large amounts of course material distributed across lecture slides, notes and supplementary documents. Finding relevant information, understanding difficult concepts and preparing effectively for examinations can be time-consuming. General-purpose AI assistants can help explain concepts, but their answers are not necessarily grounded in the specific material taught in a course. This can result in inaccurate explanations, hallucinations or answers that do not reflect the course curriculum.

StudyGraph addresses this problem by providing a locally running AI study assistant that combines a Large Language Model (LLM) with Retrieval-Augmented Generation (RAG). Instead of relying exclusively on the language model's pretrained knowledge, the application retrieves relevant passages from course materials and supplies them as context when generating answers.

The primary target users are university students who want assistance understanding and revising their course material. The application is particularly relevant to students who want personalised explanations, summaries, practice questions and interactive study support.

The purpose is to investigate whether a local LLM combined with RAG can provide useful, course-specific learning assistance while maintaining privacy and reducing dependence on external AI services. Another objective is to explore how prompt engineering and retrieval influence the quality and reliability of generated responses.

The MVP focuses on one predefined course, LLMs for Developers. Its main features are:

A conversational interface for interacting with the AI assistant.
Reusable study profiles, called Buddies, with configurable teaching characteristics.
Persistent conversations and conversation history.
A locally running language model through Ollama.
Retrieval of relevant course material using ChromaDB.
References to retrieved course material to improve transparency.
An alternative general-chat mode without course-specific retrieval.
The ability to request explanations, summaries and practice questions.

The application also includes an About page for inspecting model information, index size and data locations.

The MVP deliberately limits the number of supported courses and does not attempt to become a complete learning management system. Features such as unrestricted course management and supplementary document uploads are outside the essential initial scope.

2. Architecture and Implementation
2.1 Overall architecture

StudyGraph is implemented in Python 3.12 and uses a modular architecture that separates the user interface, application services, domain models, prompt construction, retrieval, language model integration and persistence.

The main technologies are:

Streamlit: Provides the multi-page web interface.
LangGraph: Orchestrates the conversation workflow and controls the RAG and non-RAG execution paths.
Ollama: Runs the local language model and embedding model.
ChromaDB: Stores and retrieves embedded course-material chunks.
SQLite: Persists Buddies, conversations, messages and configuration snapshots.
Python and uv: Provide the application environment and dependency management.

The selected chat model is llama3.2:3b, while nomic-embed-text generates 768-dimensional embeddings. The models run locally through Ollama.

2.2 Application flow

The application is organised into three main pages:

Chat: Students select a Buddy, start conversations, submit questions and receive streaming responses. Retrieved sources can be inspected alongside the answers.
Buddies: Students create and edit reusable assistant profiles by configuring their preferred teaching style and intended audience.
About: Displays information about the models, knowledge-base index and local data storage.

A typical interaction follows this sequence:

The student selects an existing Buddy and starts a conversation.
The application creates a conversation and saves a snapshot of the Buddy configuration.
The student submits a message and selects the desired Task.
The application retrieves the conversation history and configuration.
The prompt builder combines the four T's with the current message and relevant history.
If the Buddy is associated with a course, LangGraph executes the retrieval branch.
The retrieval component searches ChromaDB for relevant course-material chunks.
Retrieved passages and their source information are supplied to the language model.
Ollama generates the response, which is streamed to the interface.
The response and user message are persisted in SQLite.

If the Buddy has no associated course, the retrieval step is skipped. The same prompt-engineering configuration is retained, allowing a comparison between general LLM responses and RAG-supported responses.

2.3 Local LLM and RAG implementation

The local-first approach means that core inference does not depend on an external hosted LLM API. Ollama provides the runtime for both text generation and embeddings.

The chat model generates natural-language explanations, while the embedding model transforms text into numerical vector representations that capture semantic information.

RAG consists of two main stages:

Indexing stage:

Course documents are collected from lecture materials.
Original PDF material is converted into Markdown.
Extraction artifacts are checked and corrected where necessary.
Documents are divided into smaller, meaningful chunks.
Source metadata is retained.
Each chunk is converted into an embedding.
Embeddings and associated text are stored in ChromaDB.

Query stage:

The student's question is converted into an embedding.
ChromaDB searches for semantically similar chunks.
The most relevant passages are returned.
Retrieved content is inserted into the LLM prompt as contextual information.
The LLM generates an answer based on the question and retrieved material.
Available source references are presented to the student.

The current course corpus contains 85 Markdown documents and approximately 1,660 chunks, covering eight available teaching weeks. The material is written in English to align with the embedding model.

The application uses a heading-first chunking strategy with a configured chunk size of 900 and an overlap of 120. This aims to preserve contextual relationships while avoiding chunks that are unnecessarily large.

The architecture also distinguishes between retrieval failure and successful retrieval that produces no sufficiently relevant results. This is important because the assistant should not claim that an answer is course-grounded when the retrieval process has failed.

3. Application of the Four T's and Key Design Decisions

An important design principle in StudyGraph is the use of the four T's: Task, Tone, Traits and Target. These dimensions provide a structured approach to prompt engineering and allow students to customise the assistant without having to understand the technical details of prompt construction.

Task – What should the AI do?

Task defines the activity requested in an individual interaction. Examples include explaining a concept, summarising a lecture, generating practice questions, comparing concepts or reviewing a student's answer.

Task is selected separately for each message. This allows students to reuse the same Buddy for different learning activities.

Tone – How should the AI communicate?

Tone defines the communication style. Examples include friendly, formal, encouraging, concise or academic.

This helps adapt the assistant's responses to the student's preferred learning experience.

Traits – What characteristics should the AI exhibit?

Traits describe the assistant's behavioural characteristics. Examples include being patient, analytical, critical, supportive or Socratic.

Multiple traits can be combined to create different teaching approaches.

Target – Who is the AI communicating with?

Target defines the intended audience or knowledge level. For example, the assistant can be configured to explain concepts to beginners, students with fundamental knowledge or students preparing for an examination.

Key design decisions

The four T's are implemented through reusable Buddies. Each Buddy stores its Tone, Traits and Target, while Task is selected independently for each message.

This separation was an important architectural decision because it avoids requiring students to create a new assistant every time they want to perform a different learning activity.

Another important decision was to save a snapshot of the Buddy configuration when a conversation starts. Consequently, editing a Buddy does not silently change the behaviour of existing conversations. This improves consistency and makes comparisons more reproducible.

The project also deliberately separates RAG and non-RAG execution while retaining the same prompt construction process. This makes it possible to investigate the contribution of retrieval without unnecessarily changing other prompt-engineering variables.

4. Relevant Machine Learning Concepts, Data Preparation and Retrieval Choices

StudyGraph combines several important machine learning and natural language processing concepts.

Embeddings and semantic similarity

An embedding model transforms text into a numerical vector. Text with similar semantic meaning should generally have vectors that are closer together in the embedding space.

StudyGraph uses nomic-embed-text to represent both course-material chunks and student questions as 768-dimensional vectors.

This makes it possible to retrieve relevant passages even when the student uses different wording from the original lecture material.

Retrieval-Augmented Generation

RAG combines information retrieval with generative AI.

A conventional LLM generates responses primarily from its pretrained parameters and the supplied prompt. RAG supplements this process with information retrieved from an external knowledge base.

The principal advantage is that responses can be grounded in specific course material rather than relying exclusively on potentially incomplete or outdated pretrained knowledge.

However, RAG does not guarantee correctness. Its effectiveness depends on the quality of the source material, chunking, embeddings, retrieval and final generation.

Data preparation

The primary dataset consists of lecture material for LLMs for Developers.

The original documents are converted from PDF into Markdown. This makes the content easier to process and preserves headings and textual structure.

The documents are cleaned, divided into chunks and associated with metadata that allows retrieved passages to be traced to their sources.

The current corpus covers weeks 1, 2, 3, 4, 6, 8, 9 and 10, from our LLM course. Weeks 5 and 7 were empty.

Retrieval choices

ChromaDB was selected as the vector database because it provides a relatively straightforward local vector-search solution and supports metadata filtering.

The heading-first chunking strategy aims to preserve the relationships between headings and the content they introduce. The overlap helps reduce the risk of losing relevant information at chunk boundaries.

The system currently retrieves semantically similar chunks and supplies them to the language model as contextual information.

The final retrieval configuration, including the optimal number of retrieved chunks and a relevance threshold, remains subject to further evaluation.

5. Results and Reflection: Linear Regression versus Local LLM + RAG
5.1 Experimental setup

A separate experiment was conducted to compare a conventional machine learning model with a local LLM using RAG.

The task was to predict the daily revenue of an ice-cream stand based on temperature.

The dataset contained 500 observations with two variables:

Temperature: input feature.
Revenue: prediction target.

The dataset was divided into training, validation and test sets using a 70/15/15 split with random_state=42.

This produced 361 training observations, 64 validation observations and 75 test observations.

Three held-out test observations were selected: the coldest, median and warmest temperatures. Their actual revenue values were hidden from both prediction approaches until evaluation.

5.2 Linear regression

The first approach used Scikit-learn's LinearRegression, trained on the 361 training observations.

The resulting fitted equation was:

Revenue = 21.2581 × Temperature + 49.8138

Linear regression learns a relationship between the input feature and target variable by minimising the sum of squared residuals.

It provides a relatively simple, interpretable and deterministic prediction model for this dataset.

5.3 Local LLM with RAG

The second approach used qwen2.5-coder:7b through Ollama, together with nomic-embed-text.

A separate ChromaDB collection was created containing 12 reference observations selected exclusively from the training data.

For each question, the system retrieved the three most semantically similar reference rows. The model was instructed to return a numerical prediction without executing code or using regression formulas.

An additional experiment used the same LLM without retrieval to investigate the contribution of RAG.

5.4 Experimental results

The following table presents the actual recorded results.

Temperature	Actual revenue	Linear regression	LLM + RAG	LLM without RAG
0.27	32.55	55.49	55.39	100
23.59	542.61	551.31	552.82	1500
40.47	918.39	910.21	630.00	1000
Mean absolute error		13.28	107.15	368.82

The results demonstrate that linear regression performed substantially better for this numerical prediction task.

Its mean absolute error was 13.28, compared with 107.15 for the local LLM with RAG and 368.82 for the LLM without retrieval.

Linear regression was approximately eight times more accurate than LLM + RAG in terms of mean absolute error.

RAG nevertheless provided a considerable improvement within the LLM approach, reducing its mean absolute error by approximately 71% compared with generation without retrieval.

5.5 Reflection and interpretation

The experiment illustrates an important distinction between predictive machine learning and generative language models.

Linear regression learns numerical coefficients from the training data and uses them to calculate predictions. Its objective directly matches the numerical evaluation task.

The LLM, on the other hand, generates a plausible response based on the information available in its context. It does not automatically learn the underlying numerical relationship simply because it retrieves examples.

This limitation became particularly visible in the warmest-temperature test case. The retrieved observations were all below approximately 26 degrees, while the test input was 40.47 degrees. Consequently, the LLM predicted 630 instead of the actual revenue of 918.39.

The experiment also revealed that semantic similarity is not necessarily appropriate for numerical retrieval. The embedding model retrieved nearly identical reference rows for all three temperature questions. It did not reliably prioritise observations based on numerical distance.

For this type of task, numerical nearest-neighbour retrieval would be more appropriate than semantic embedding similarity.

The findings suggest that the choice of model should depend on the problem being solved. Traditional machine learning is preferable for structured numerical predictions where accuracy, reproducibility and interpretability are important. LLMs are more valuable for tasks involving natural-language explanations, contextual understanding and interaction with unstructured information.

5.6 Limitations and possible improvements

The experiment has several limitations.

First, only three held-out observations were used for the final LLM comparison. Although the train/test separation was maintained, this is too small a sample for broad statistical conclusions.

Second, the experiment used one dataset, one local LLM configuration and one embedding model. Different models and retrieval strategies could produce different results.

Third, semantic embeddings are not designed to perform precise numerical similarity searches. A hybrid retrieval approach combining semantic search with numerical nearest-neighbour retrieval could improve performance for structured data.

Other improvements include:

Increasing the number of evaluation observations.
Comparing additional regression models and local LLMs.
Testing different chunk sizes, overlap settings and retrieval depths.
Introducing relevance thresholds to avoid supplying irrelevant context.
Using reranking to improve the quality of retrieved passages.
Evaluating answers for factual correctness, relevance, grounding and usefulness.
Improving the assistant's ability to communicate uncertainty when information is missing.

It is also important to distinguish the completed regression experiment from the broader evaluation of StudyGraph itself. The regression comparison is documented with measured results, whereas the formal evaluation of course-related RAG answers remains unfinished. Therefore, the numerical results should not be interpreted as a direct measurement of the educational assistant's overall performance.

6. Conclusion

StudyGraph demonstrates how a locally running LLM can be combined with Retrieval-Augmented Generation to create a personalised study assistant grounded in course-specific learning materials.

The implementation integrates prompt engineering through the four T's, semantic retrieval, local language model inference and persistent conversation management into a modular application.

The regression experiment demonstrates that RAG can improve an LLM's ability to use available information, but it does not make a generative model equivalent to a specialised predictive model. Choosing the appropriate machine learning technique for the problem remains essential.

Overall, the project provides a functional prototype and a practical demonstration of the opportunities and limitations of local LLMs and RAG in educational applications. Further evaluation of retrieval quality, answer correctness and the student learning experience would be necessary before drawing conclusions about its effectiveness as a complete learning solution.