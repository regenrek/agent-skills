---
name: hard-cut
description: "Enforce a hard-cut cleanup policy: keep one canonical implementation and delete compatibility, migration, fallback, adapter, coercion, and dual-shape code. Use for pre-release or internal-draft refactors where the goal is one final shape, especially when changing schemas, contracts, persisted state, routing, configuration, feature flags, enum/value sets, or architecture."
---

# Hard-Cut Policy

Apply a hard-cut policy by default for refactors or behavior changes that alter schemas, contracts, persisted state, routing, configuration, feature flags, enum/value sets, or architecture where old-state preservation might otherwise be retained.

Keep one canonical codepath. Remove old-shape handling. Do not preserve draft or legacy behavior unless there is concrete evidence of a real external compatibility boundary.

## Default assumption

Treat previous shapes as internal draft shapes unless there is concrete evidence they are already:
- persisted external or user data
- on-disk or database state that must still load
- a wire format used across process or service boundaries
- a documented or publicly supported contract
- actively depended on outside the refactor boundary

Mere existence of old code is not proof of a compatibility obligation.

## Core policy

When an old shape appears, remove that path and convert the codebase to the canonical shape. Do not add code to support it. Do not add code specifically to reject it just because it once existed.

## Hard rules

Apply these rules in order:

1. Do not add fallback behavior.
2. Do not add compatibility branches.
3. Do not add shims, adapters, coercions, aliases, or dual-shape support.
4. Do not add fail-fast guards whose purpose is to detect or reject old shapes.
5. Do not add tests whose purpose is to assert rejection of old or legacy shapes.
6. Prefer deleting old-shape handling over preserving or policing it.
7. Update producers, consumers, fixtures, and tests to use only the canonical shape.
8. Remove dead code, dead conditionals, obsolete comments, and translation helpers related to old shapes.
9. Keep validation only for the current canonical contract. Validation may reject malformed current-shape input, but must not branch on legacy discriminators, old field names, aliases, old enum members, or draft formats.
10. When choosing between backward compatibility and simplification, choose simplification.

## Execution workflow

1. Identify the canonical target shape.
2. Trace every producer and consumer of that shape.
3. Update all live codepaths to emit and consume only the canonical shape.
4. Update fixtures, test data, builders, and snapshots to the canonical shape.
5. Delete legacy handling, branching, comments, and helpers.
6. Keep only current-shape validation that is still required for correctness.
7. If a real external compatibility boundary exists, isolate it and call out the exact file, function, boundary, and reason it cannot be removed yet.

## Review checklist

- Reject changes that preserve old-shape behavior behind conditionals.
- Reject translation layers between old and new shapes.
- Reject validation branches added only to reject legacy inputs.
- Reject tests added only to memorialize abandoned draft formats.
- Remove dead helpers and comments that describe removed draft formats.
- Keep one owner for the canonical contract.

## Deliverables

Deliver only:
- a minimal implementation that supports the canonical shape
- updated tests for the canonical shape only
- removal of obsolete legacy-shape tests
- no new rejection tests for old shapes
- no runtime logic dedicated to recognizing legacy formats

## Exception rule

Make an exception only when removing the old shape would break already persisted external or user data, on-disk or database state, cross-boundary wire formats, or a real public contract.

If such a boundary exists:
- do not invent new compatibility layers elsewhere
- name the exact file and function
- describe the concrete persisted or public dependency
- limit any compatibility discussion to that boundary only