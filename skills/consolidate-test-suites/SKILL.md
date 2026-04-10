---
name: consolidate-test-suites
description: Decide where automated test coverage belongs after a bug fix or architectural change. Use when Codex needs to choose between unit, integration, end-to-end, or standalone regression tests; fold scattered regression tests into canonical suites; reduce duplicate bug guards; or keep test ownership aligned with the layer that owns the invariant.
---

# Consolidate Test Suites

Keep bug-fix coverage in the smallest set of canonical suites that proves the owned invariant. Prefer integration or behavior tests at the ownership boundary over creating scattered standalone regression suites.

## Decision Rule

1. Identify the invariant that actually failed.
2. Identify the layer that owns that invariant.
3. Put the test in the canonical suite for that layer.
4. Add a standalone regression test only if no existing canonical suite can cover the case cleanly and deterministically.
5. Remove duplicated tests that assert the same invariant at weaker or noisier layers.

## Ownership Heuristics

- Use a unit test when one module owns the rule and the bug can be reproduced without transport, I/O, or orchestration.
- Use an integration test when the bug appears at a boundary between components, or the invariant depends on ordering, replay, persistence, IPC, retries, serialization, or lifecycle.
- Use an end-to-end test only when the user-visible contract cannot be trusted from lower-layer tests alone.
- Keep protocol, schema, and validation rules in the suite that owns the contract.
- Do not duplicate the same invariant in unit, integration, and end-to-end tests unless each layer owns a different failure mode.

## Early-Stage Bias

When architecture is still moving, bias toward fewer high-signal tests:

- Fold bug-fix coverage into existing standard suites when possible.
- Avoid creating a new `regression` test file or suite for every architecture change.
- Keep tests close to the single source of truth for the rule.
- Prefer behavior-focused names over bug-history names.

This is not "test less". It is "reduce test scatter and drift".

## When To Keep A Separate Regression Test

Keep or add a dedicated regression-style test when one of these is true:

- The bug is historically fragile and easy to reintroduce.
- The reproduction is narrow, deterministic, and hard to express naturally inside an existing suite.
- The canonical suite would become confusing or overloaded by absorbing it.
- The test documents an external contract or incident with long-term support value.

If these do not apply, fold the coverage into the normal suite.

## Consolidation Workflow

When asked to clean up test sprawl:

1. Inventory the tests that cover the same behavior.
2. Group them by owned invariant, not by file name.
3. Keep the strongest canonical test location.
4. Merge useful assertions into that suite.
5. Delete or collapse duplicates.
6. Rename tests to describe behavior and ownership, not ticket history.
7. Re-run the relevant test and typecheck/build flows.

## Output Shape

When advising or editing, state:

- the invariant
- the owning layer
- the target suite
- whether to fold, keep, or delete existing regression-style coverage
- the residual risk if coverage remains intentionally thin
