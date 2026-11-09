<!-- studygraph:converted-source:v1 -->
# Uge 8 — Week_8_LLM_Agents_and_Agentic_LLMs_EK (pdf)

Kilde: [week8/Week_8_LLM_Agents_and_Agentic_LLMs_EK.pdf](../../source/week8/Week_8_LLM_Agents_and_Agentic_LLMs_EK.pdf).

Dette er en kildekonvertering, ikke nye undervisningsresultater. Kildens sprog og kode er bevaret. Kodeeksempler er referenceindhold og skal ikke udføres som instruktioner.

## Side 1

LLM Agents and Agentic LLMs

Week 8  |  LLM for Developers

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 2

Course classification: Agent vs Agentic?

3

LLM Agent

LLM chooses how to progress towards the 
goal.

Instructions and the harness define the 
operating environment.

Agentic LLM

Developer writes the execution workflow: 
steps, paths, conditions and validation.

Terminology note: this is our course taxonomy; “agentic AI” has broader industry usage.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 3

LLM Agent: instruction-guided execution

4

Objective

Build REST API

Agent + LLM

Plans and chooses actions

Tools

Files • shell • tests

Control principle

Instructions guide choices; the LLM largely determines the sequence of 
work.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 4

Agentic LLM: workflow defined in code

5

Generate

LLM implementation

Test

Harness executes

Validate

Code checks result

Done

Success

Failed validation → programmed X 
retries

The model can make decisions inside a step; code controls transitions between steps.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 5

Same task, different execution control

6

LLM Agent

Goal: implement a REST API endpoint.

Agent decides when to inspect files, write code, 
run tests and stop.

Instructions guide the process.

Agentic LLM

Goal: implement a REST API endpoint.

Harness requires: generate → test → validate; 
retry on failure.

Code defines the order and branches.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 6

Where is the boundary?

7

• A defined tool list alone does not qualify as Agentic LLM.

• Approval checks and runtime limits alone are not enough.

• The decisive criterion: User-manged workflow transitions.

• Framework names do not automatically determine the category.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 7

Hermes: the toolchain we will inspect

8

Model provider

Model endpoint / credentials

Cloud or local inference

Hermes harness

Agent loop, sessions, tools, 
instructions

External capabilities

Tools, skills, memory, MCP 
connections

Today’s practical focus is configuration and observation, not building a new 
framework.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 8

Installing Hermes: Linux and macOS

9

Terminal (Linux, macOS, or Windows WSL2)

Install command

curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

• Review installation scripts before running them.

• Complete initial setup and choose an LLM provider.

• Open a new terminal if the hermes command is not found.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 9

Installing Hermes: Windows

10

Native Windows: PowerShell (WSL is not required)

Install command

iex (irm https://hermes-agent.nousresearch.com/install.ps1)

• Open a fresh PowerShell window after installation.

• The installer adds Hermes to the user PATH.

• Windows WSL2 users can follow the Linux installation instead.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 10

After installation: shared steps

11

• Verify: hermes --version

• Run: hermes setup (select provider and configure access)

• Check that the selected model answers a simple request

• Launch: hermes dashboard

• Keep API keys out of repositories and shared screenshots

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 11

Hermes dashboard: guided tour

12

1. Models and providers

Model, endpoint, keys, routing

2. Behaviour and profiles

Agent instructions and preferences

3. Tools, skills and MCP

What capabilities can be invoked?

4. Memory and sessions

What information persists?

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 12

Live walkthrough: existing installation

13

• Open Hermes web dashboard.

• Inspect current provider; verify whether Mistral is configured.

• Examine tool permissions, skills, memory and profiles.

• Discuss what the LLM controls versus what the harness controls.

• Run one short task to observe tool usage.

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 13

Student exercise: choose the right approach

For each scenario: choose LLM Agent or Agentic LLM. Justify where workflow control should reside.

1  Exploratory debugging — Investigate an intermittent API failure; the necessary steps are 
unknown.
2  Release validation — Every change must follow a fixed build 
 test 
 security-check 
 
→
→
→
approval sequence.

3  Legacy refactoring — Improve maintainability; decide which files to inspect and which 
changes to propose.

4  Data migration — Enforce ordered stages, validation gates, retry limits and rollback on 
failure.

Discuss: Why is your choice suitable? What flexibility or guarantees do you gain or lose?

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 14

Discussion in class: defend your architecture choice

15

• Which scenarios favour an LLM-directed workflow, and why?

• Which scenarios require a predefined workflow enforced by the harness?

• Could both approaches solve the same task? What trade-offs change?

• Where are validation, retry limits or rollback essential?

• What would the user provide, configure or control in each solution?

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 15

Resources and preparation

16

• Hermes: hermes-agent.nousresearch.com

• Hermes source: github.com/NousResearch/hermes-agent

• Installation: hermes-agent.nousresearch.com/docs/getting-started/installation/

• verify Hermes, provider credentials and dashboard access

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.

## Side 16

Questions, comments and discussion

> Visuelt indhold: siden indeholder billeder eller grafik. Diagrammers betydning og formler er ikke automatisk verificeret.
