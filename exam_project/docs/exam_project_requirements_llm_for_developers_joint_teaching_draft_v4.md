# Exam Project — LLM for Developers

## Objective

Design and implement a working software prototype based on a problem of your choice. The application must use a **local LLM** and **retrieval-augmented generation (RAG)** to provide a meaningful solution, not merely demonstrate a prompt and response.

Define the problem, intended users, value of the solution, and the LLM's role. Keep the project focused on a clearly defined **minimal viable product (MVP)**: the smallest working version that demonstrates the core idea. Production readiness and additional features are not required.

## Project Scope

- **Minimum viable product (MVP):** Deliver a usable MVP with a clear flow from user input to output, such as a web application, API-backed application, or another suitable interface.
- **Local LLM:** The delivered and demonstrated application must generate its core answers using a locally running LLM. Online models may support development but cannot replace this requirement.
- **RAG:** The application must retrieve relevant source material and use it to inform the LLM's answers. You may use Ollama, OpenWebUI Knowledge, or your own RAG implementation. Be able to demonstrate how retrieval affects an answer.
- **4T's prompt engineering:** Apply **Traits, Task, Tone, and Target** meaningfully in the application's prompts or prompt strategy. Show where they are implemented and explain the choices.
- **Project scope:** Describe the main features of your MVP and, where relevant, what is outside its scope. Aim for a focused, demonstrable MVP rather than unnecessary complexity.
- **Technical understanding and reflection:** Relate the solution to relevant concepts from the course. Briefly explain how the RAG source material is prepared and how retrieval works (for example, embeddings and similarity measures). Reflect on a relevant connection to machine learning concepts, such as training, model behaviour, or data quality, and mention a limitation you encountered or identified. Use examples from your project where possible.
- **Traditional ML versus local LLM + RAG (small comparison):** In addition to your chosen application, complete a short, separate experiment comparing a linear regression model trained on numerical data with a local LLM using RAG to make predictions for the **same numerical task**. Select a suitable dataset and follow the comparison instructions below. This experiment does **not** have to be integrated into your application.

## Comparison Exercise — Linear Regression vs. Local LLM with RAG

Use a numerical prediction problem suitable for linear regression (for example, predicting a value from one numerical input). Keep this exercise small; **one or a few well-chosen test cases** are sufficient.

- **Prepare data:** Choose or generate a dataset, describe the inputs and target, and separate training/reference data from test cases. Do not expose test targets to either solution.
- **Train a regression model:** Fit a linear regression model using a library such as scikit-learn or your existing gradient-descent code. Predict the held-out values.
- **Use the local LLM + RAG:** Give the local LLM the same input values and ask it to predict the target. Its RAG collection may contain relevant background information and examples **from the training/reference portion only**, but not the test answers. Document what was retrieved. Do not let the LLM call the regression model or execute regression code to produce its predictions; the aim here is to compare different approaches, not two interfaces to the same algorithm.
- **Compare and explain:** Show the actual values and both sets of predictions for your selected test cases. Formulate and calculate a suitable error measure for each approach (for example, absolute error for a single case or mean absolute error for multiple cases). Explain why the approaches differ, whether RAG was useful, and when a specialised trained model may be preferable to an LLM.

**Scope:** A small table of results and a short discussion are enough. No automated evaluation harness or new user interface is required. The experiment supports comparison and discussion; it is not expected that an LLM will outperform linear regression at linear regression.

## AI-Assisted Development — Allowed

You **may use LLMs and coding agents throughout development** for planning, architecture, programming, debugging, testing, and documentation. This includes free online services; you do not need to run your development assistant locally.

Examples of online services with free access or free-tier options (subject to current limits and availability):

- [ChatGPT](https://chatgpt.com/) — development assistance and code review.
- [Google Gemini](https://gemini.google.com/) — programming assistance and technical discussion.
- [Claude](https://claude.ai/) — programming assistance, design, and code review.
- [GitHub Copilot](https://github.com/features/copilot) — IDE-based coding assistance; free-plan limits may apply.
- [Google AI Studio](https://aistudio.google.com/) — experimenting with models and prompts; usage limits apply.
- [Ollama Cloud](https://ollama.com/pricing) — hosted LLMs for development and coding agents; the free plan includes limited monthly usage of starter models.

You may also use other tools or agentic development workflows, including agents that edit files or execute tests. **You remain responsible for the delivered code** and must be able to explain, validate, and demonstrate the solution, including AI-generated parts. Do not upload secrets or sensitive data to online tools.

**Important distinction:** Online LLMs are allowed *as development tools*. The *final application's core answer generation* must use a local LLM.

## Deliverables

Submit the following:

- **MVP project:** Source code, prompts, configuration examples, dependencies, and any RAG source material needed to reproduce the solution.
- **Setup guide (`README.md` or equivalent):** Prerequisites, installation, configuration, model setup, loading RAG material, starting the application, and instructions for testing it.
- **Synopsis (maximum 5 pages):**
   - Problem, target users, purpose, and MVP scope.
   - Architecture and implementation, including application flow, local LLM, and RAG.
   - How the 4T's are applied and the key design decisions.
   - Relevant machine learning concepts, data preparation, and retrieval choices.
   - Results and reflection from the linear regression versus local LLM + RAG comparison, relevant limitations, and possible improvements.

The setup guide is **not included** in the five-page synopsis limit. Document the system sufficiently for another developer to understand and run it.

## Optional Extensions

Additional agents or orchestration (e.g. AutoGen Studio or LangGraph), custom interfaces, alternative locally hosted models, and extra integrations are welcome **but not required**. They should not compromise completion of the MVP.

**Comparison note:** The regression experiment is separate from the self-chosen application. Use the same held-out inputs and the same target values to assess both approaches. Be explicit about the information available to the LLM through RAG, and report measured results rather than assumed outcomes.

**Assessment focus:** Demonstrate a well-scoped MVP in which the local LLM, RAG, and 4T's are genuinely integrated. Explain the relevant underlying concepts, compare the two prediction approaches, and reflect on the implementation and its limitations.
