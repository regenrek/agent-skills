---
name: root-cause-finder
description: Performs root-cause-first debugging and review by tracing expected behavior to the first unintended side effect before changing contracts, parsing, or types. Use when debugging protocol errors, deserialization failures, null payloads, missing fields, restore or hydration issues, state-ownership bugs, unexpected requests, background mutations, or reviewing junior-created code where the visible failure may be downstream noise.
---

# Root-Cause Finder

## Core Instruction

Before fixing the error, prove whether the code path that produced it was intended.

Do not stop at the first contract, parsing, type, null, or schema error. Treat it as a possible symptom.

## Default Workflow

1. State the expected behavior in plain language.
2. State the invariant in one sentence.
3. State what definitely did not happen.
4. Trace the causal chain from the intended action or system event to the observed system effect.
5. Ask whether the request or mutation should have happened at all.
6. Identify the canonical source of truth and every competing source.
7. Find the first unintended side effect or write.
8. Only then decide whether a downstream contract fix is still necessary.

## Questions To Answer In Order

1. What user action or system event was supposed to happen?
2. What exact call path caused this request or response?
3. Should this request, mutation, or side effect have happened at all under the expected behavior and invariants?
4. Who owns the state at each layer?
5. Is there observer-driven syncing, lifecycle startup code, persistence restore, retry logic, background work, or multiple sources of truth causing an unintended side effect?
6. If a contract is violated, is the contract wrong, or did unintended logic reach the contract?

## Rules

- Do not make the contract more permissive unless you can prove the observed payload is intended in the final design.
- Prefer fixing the upstream logic bug over accepting bad downstream data.
- Separate symptom, trigger, root cause, minimal safe fix, and architectural follow-up.
- If a low-level fix is still needed, explain why the upstream fix is not sufficient or why both are required.
- Identify the correct layer to fix first.
- Name the first visible wrong behavior, not only the final error.

## Hidden Write Checks

Treat non-explicit writes as suspicious by default.

- Audit lifecycle hooks, callbacks, subscribers, watchers, interceptors, middleware, retries, background jobs, cache refreshers, persistence restore, scheduled tasks, and startup code.
- Check whether derived data is being mirrored into another store, cache, file, queue, session, or database through an observer or helper layer.
- Prefer explicit command handlers, request handlers, job runners, or user actions as writers; treat startup-time and background writes as suspects until proven intentional.
- If a framework has automatic reactivity or lifecycle execution, map this rule onto its equivalent constructs without assuming the framework behavior is correct.

## Output Format

Use this structure:

- Expected behavior
- Invariant
- What definitely did not happen
- Bug class
- Causal chain from intended action to system effect
- First unintended side effect
- Canonical source of truth
- Competing sources of truth
- Symptom
- Trigger
- Root cause
- Correct layer to fix first
- Minimal safe fix
- Architectural follow-up
- Proposed patch