# Week 8 — LLM Agents and Agentic LLMs

Source: `source/week8/Week_8_LLM_Agents_and_Agentic_LLMs_EK.pdf`, 16 PDF pages. See the [source conversion](week8_source_week_8_llm_agents_and_agentic_llms_ek_pdf.md). Page numbers refer to the position in the PDF; the printed slide numbers differ in a few places.

## The course's distinction is about control

In the course's terminology, an LLM Agent chooses for itself how to work towards a goal. Instructions and a harness define the environment, but the model largely chooses the order of actions.

An Agentic LLM, by contrast, follows an execution path that the developer has programmed: steps, transitions, conditions and validation. The model can still make decisions inside a step. The slides emphasise that this is the course's taxonomy; the words are used more broadly outside the course.

## Same task, different steering

The example is the implementation of a REST API endpoint. An agent can decide for itself when to read files, write code, test and stop. In the programmed flow the harness instead requires generation, testing and validation with a fixed number of new attempts on failure.

A list of tools, approval steps or a time limit does not by itself make a system an Agentic LLM in this definition. What matters is whether the user or the developer defines the transitions in the workflow. The name of the framework is not enough to decide the category either.

## Hermes as an example of a harness

The slides distinguish between model provider and endpoint, the agent loop of the Hermes harness, and external capabilities such as tools, skills, memory and MCP. The practical part examines installation, provider setup and the dashboard, including model choice, instructions, permissions and persistent sessions.

The installation commands in the full source are historical teaching examples. They are preserved as source text; the conversion has neither installed nor started Hermes.

## The architecture exercise

Choose an approach for the described scenarios and argue where control should sit. Among other things the slides mention exploratory debugging and release validation. Discuss what a flexible model-steered flow gives you, and when fixed test, validation and retry steps are necessary.

## Review questions

1. Who decides the next action in the two approaches?
2. Why are tools and runtime constraints not in themselves a programmed workflow?
3. What is the difference between a model provider and a harness?
4. When does it make sense to fix testing and validation in code?