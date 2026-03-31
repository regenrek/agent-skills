---
name: hard-cut
description: "Enforce a hard-cut cleanup policy: keep one canonical implementation and delete compatibility, migration, fallback, adapter, coercion, and dual-shape code. Use when refactoring pre-release or internal-draft codepaths to one final shape, or when a task changes product behavior, persisted state, routing, contracts, configuration, schema or enum shapes, feature flags, or architecture where old-state compatibility might otherwise be preserved. Default assumption: prior shapes are internal drafts unless the code proves a real external compatibility boundary."
---

# Hard-Cut Policy

Apply a hard-cut policy as the default decision filter for product and architecture changes.

Keep one canonical codepath. Remove old-shape handling. Do not preserve draft or legacy behavior unless the code proves there is a real external or public compatibility boundary.

## Core policy

Treat previous shapes as internal draft shapes unless the code proves they are already persisted external or user data, or a public supported contract.

When an old shape appears, remove that path and convert the codebase to the canonical shape. Do not add code to support it. Do not add code specifically to reject it just because it once existed.

## Hard rules

Apply these rules in order:

1. Do not add fallback behavior.
2. Do not add compatibility branches.
3. Do not add shims, adapters, coercions, or dual-shape support.
4. Do not add fail-fast guards whose purpose is to detect or reject old shapes.
5. Do not add tests whose purpose is to assert rejection of old or legacy shapes.
6. Prefer deleting old-shape handling over preserving or policing it.
7. Update producers, consumers, fixtures, and tests to use only the canonical shape.
8. Remove dead code, dead conditionals, and obsolete comments related to old shapes.
9. Keep validation only when it is already needed for correctness of the current canonical contract.
10. When choosing between backward compatibility and simplification, choose simplification.

## Execution workflow

1. Identify the canonical target shape.
2. Trace every producer and consumer of that shape.
3. Update all live codepaths to emit and consume only the canonical shape.
4. Update fixtures, test data, builders, and snapshots to the canonical shape.
5. Delete legacy handling, branching, comments, and helpers.
6. Keep only current-shape validation that is still required for correctness.
7. If a real external compatibility boundary exists, stop and call out the exact file, data boundary, and reason it cannot be removed yet.

## Review Checklist

- Reject changes that preserve old-shape behavior behind conditionals.
- Reject translation layers between old and new shapes.
- Reject validation branches added only to reject legacy inputs.
- Remove dead helpers and comments that describe removed draft formats.
- Keep one owner for the canonical contract.

## Deliverables

Deliver only:

- A minimal implementation that supports the canonical shape.
- Updated tests for the canonical shape only.
- Removal of obsolete legacy-shape tests.
- No new rejection tests for old shapes.
- No runtime logic dedicated to recognizing legacy formats.

## Exception rule

Make an exception only when removing the old shape would break already persisted external or user data, or a real public contract.

In that case, do not invent a shim. Call out the exact location and explain why it is a true external compatibility boundary.
