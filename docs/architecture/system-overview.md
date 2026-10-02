# System Overview

The workflow is a local, open-source multi-LLM coordinator that asks ten
specialised agents to analyse a requirement **in parallel** and produce software
artifacts, using two separate local Ollama endpoints as model backends.

## Purpose

Given a single user requirement (for example *"build a todo app with login"*), the
workflow fans the requirement out to ten agents, each with one bounded
responsibility, and returns a structured result that can be saved, versioned and
reviewed.

## High-level architecture

```text
                    ┌─────────────────────┐
                    │     User (CLI/web)  │
                    └──────────┬──────────┘
                               │ requirement
                               ▼
                    ┌─────────────────────┐
                    │  Workflow manager   │  model/ollama_workflow.py
                    │  (ThreadPoolExecutor│
                    │   + endpoint router)│
                    └──────────┬──────────┘
              ┌────────────────┼────────────────┐
              │                │                │
     ARCHITECT_ENDPOINT   WORKER_ENDPOINT   (configurable)
     (architect-role)     (reviewer/worker)
              │                │
    ┌─────────▼───┐      ┌─────▼──────────────┐
    │ Ollama host │      │ Ollama host        │
    │ port 11434  │      │ port 11435         │
    │ qwen2.5-coder│     │ llama3.2:3b        │
    └─────────────┘      └────────────────────┘
```

## Responsibilities

Ten agents, split across two roles:

| Role | Endpoint | Default model | Agents |
| --- | --- | --- | --- |
| Architect | `ARCHITECT_ENDPOINT` | `qwen2.5-coder:7b` | architecture, tech_lead, implementation |
| Worker / reviewer | `WORKER_ENDPOINT` | `llama3.2:3b` | testing_quality, documentation, deployment, predictability, reproducibility, context_management, security |

## Hard requirement: two endpoints

Endpoint selection is configuration-driven via environment variables
(`ARCHITECT_ENDPOINT`, `WORKER_ENDPOINT`), never by editing code. See
`ADR-001-model-routing.md`.
