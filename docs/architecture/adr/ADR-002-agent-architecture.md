# ADR-002: Parallel agent architecture

- **Status:** Accepted
- **Date:** 2026-10-02

## Context

The assignment's functional requirements span six responsibilities (architecture,
tech lead, implementation, testing/quality, documentation, deployment validation)
plus four non-functional reviews. Each responsibility must be covered, and the
implementation responsibility must support multiple workers (N ≥ 2) or a credible
parallel/partitioned equivalent.

## Decision

Model each responsibility as a **specialised agent** (ten in total) and execute them
**in parallel** with a `ThreadPoolExecutor` bounded by `MAX_PARALLEL_AGENTS`. Results
are collected and sorted back into a fixed order for deterministic presentation.

## Consequences

- **Positive:** covers all responsibilities, and the bounded thread pool is a
  credible equivalent of "multiple coding workers" partitioning work concurrently.
- **Positive:** `MAX_PARALLEL_AGENTS` is a RAM guard for local hardware.
- **Negative:** agents run independently with a shared framing context only; richer
  cross-agent handoffs would require explicit artifact passing (see context
  management in the synopsis).
