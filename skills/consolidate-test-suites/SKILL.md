---
name: consolidate-test-suites
description: Decide exactly where bug-fix test coverage belongs. Use before adding, moving, or deleting tests after a bug fix or architectural change. Select one owning layer, reuse existing canonical suites, block redundant or weakly placed tests, and remove weaker duplicates.
---

# Consolidate Test Suites

Purpose: place each invariant in one owning test layer only.

Definitions:
- Invariant: the rule that must stay true.
- Owning layer: the lowest layer that truly owns and can prove that rule.
- Canonical suite: the normal existing suite for that owning layer.

Default: reuse an existing canonical suite. Do not create a new standalone regression test unless the exception rule below allows it.

## Hard Rules

- You MUST identify the invariant before adding or moving any test.
- You MUST identify exactly one owning layer: unit, integration, or end-to-end.
- You MUST first try to place coverage in an existing canonical suite for that layer.
- You MUST prefer editing an existing test file over creating a new test file.
- You MUST NOT add the same invariant in multiple layers unless each layer covers a different failure mode. If you keep more than one layer, name the distinct failure mode for each.
- You MUST NOT add tests that lock in implementation details unless that implementation unit itself owns the invariant.
- You MUST NOT create a standalone regression test because it is faster or easier.
- If you cannot name the invariant and the owning layer, STOP. Report that placement is not justified.

## Required Decision Order

Choose the first option that fits:

1. Add to an existing test in an existing file in the owning layer.
2. Add a new test to an existing canonical file in the owning layer.
3. Create a new file inside the existing canonical suite in the owning layer.
4. Create a standalone regression-style test only if the Exception Rule passes.

## Owning Layer Rules

Choose unit when:
- one module owns the rule, and
- the bug reproduces without I/O, transport, persistence, retries, IPC, orchestration, or lifecycle coupling.

Choose integration when:
- the rule lives at a boundary between components, or
- the bug depends on serialization, persistence, ordering, replay, retries, IPC, process lifecycle, or multi-component coordination.

Choose end-to-end only when:
- the user-visible contract cannot be trusted from lower-layer tests alone.

Tie-breakers:
- If torn between unit and integration, choose integration.
- Never choose end-to-end to compensate for uncertainty.
- Never choose a higher layer just because it is easier to reproduce there.

## Exception Rule for Standalone Regression Tests

A standalone regression-style test is allowed only if ALL are true:

- no existing canonical suite can express the case cleanly
- the reproduction is deterministic
- the case has durable incident or contract value
- adding it to the canonical suite would make that suite less clear

If any condition is false, fold the coverage into the canonical suite.

## Duplicate Cleanup

After placing coverage:

1. Search for tests that assert the same invariant.
2. Keep the strongest owned location.
3. Merge any unique assertions into that location.
4. Delete or simplify weaker duplicates.
5. Rename tests by behavior and owner, not by ticket number or bug history.

## Verification

Before finishing:

1. Run the narrowest relevant test target first.
2. Run required typecheck, build, or lint steps for touched code.
3. Report exactly what was run and whether it passed.

## Required Output

Reply in exactly this format:

Invariant: <rule that failed>

Owning layer: <unit | integration | end-to-end>

Target suite/file: <path or suite name>

Action: <reuse existing test | add to existing suite | create file in canonical suite | keep standalone regression>

Why this layer owns it: <one short paragraph>

Duplicates to merge/delete: <list or "none">

Verification run: <commands and result>

Residual risk: <what is still not covered, if anything>