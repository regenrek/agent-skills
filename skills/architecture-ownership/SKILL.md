---
name: architecture-ownership
description: Determine runtime owner, first-fix layer, and canonical long-term module or package owner in layered codebases. Use when placing code across UI vs platform shell vs runtime orchestration vs domain or application vs shared core vs adapter or integration layers, debugging ownership issues, removing duplicate policy paths, or answering "where should this live?" architecture questions.
---

# Architecture Ownership

Use this skill for repo-specific ownership and placement decisions in layered systems.

Focus on long-term canonical ownership, not only the layer where the current bug appears.

## Required Discovery

Before deciding ownership:

- Read the repo docs that define architecture, boundaries, or responsibilities.
- Read ADRs or design docs that define runtime flow, request flow, or package boundaries.
- Inspect the top-level project structure to map the repo's concrete module or package names onto the generic layers in this skill.

When docs are incomplete:

- infer the current layer model from the codebase
- state the assumption explicitly
- keep the recommendation aligned to one canonical owner

## Required Output

When answering an ownership or placement question, explicitly separate:

- `Runtime owner`
- `First fix owner`
- `Canonical long-term owner`
- `Competing owners that are wrong`
- `Cleanup direction`

Do not collapse these into a single answer.

## Decision Order

1. Identify the runtime concern:
   - visible UI state
   - platform shell or OS bridge
   - runtime composition or request dispatch
   - canonical domain or application workflow
   - pure shared logic
   - concrete adapter or integration behavior
2. Name the layer where the wrong behavior currently happens.
3. Decide whether that layer is only the `First fix owner` or also the `Canonical long-term owner`.
4. If the behavior is reusable product or business policy, move the long-term owner out of the runtime orchestration layer.
5. Remove duplicate policy, fallback logic, or dual paths once the canonical owner is clear.

## Layer Map

- `UI layer`
  - owns visible UI state, navigation, rendering, presentation-oriented derived state, and view composition
- `Platform shell`
  - owns native shell concerns, OS bridges, local device integrations, filesystem or permission bridges, process or session plumbing, and platform-local persistence helpers
- `Runtime orchestration layer`
  - owns runtime composition, request dispatch, background coordination, worker management, event publication, and process-level orchestration
  - this is often the `First fix owner`
  - this is not automatically the `Canonical long-term owner`
- `Domain or application layer`
  - owns canonical product workflow, business rules, reusable application services, and cross-interface behavior
- `Shared core layer`
  - owns shared types, enums, validation, normalization, capability logic, and pure logic used across runtimes
- `Adapter or integration layer`
  - owns concrete protocol, provider, vendor, transport, or API integration behavior
  - does not own cross-provider or cross-integration product policy

Translate these generic layers into the repo's actual module, package, crate, or service names before making a recommendation.

## Hard-Cut Rules

- Do not leave reusable domain policy in the runtime orchestration layer just because the wrong behavior currently happens there.
- Do not put UI state, layout state, restore state, or user-facing presentation ownership in the runtime orchestration layer.
- Do not put platform shell or native integration concerns in the domain or application layer.
- Do not put cross-provider or cross-vendor product policy in adapter or integration layers.
- Do not put pure validation, normalization, or capability logic in orchestration code when it can live in shared core or a narrow domain module.

## Common Judgments

- If the question is "who should decide this for all future interfaces?" the answer is usually the domain or application layer, a narrow domain package, or shared core, not the runtime orchestration layer.
- If the question is "where do I patch this bug first so the product stops doing the wrong thing?" the answer may still be the runtime orchestration layer.
- If the question is "who owns the wire shape or payload type?" the answer is usually the shared API or core type layer, not the runtime orchestration layer.
- If the question is "who owns vendor-specific behavior?" the answer is the relevant adapter or integration layer, but only for adapter behavior, not canonical product policy.

## Example Pattern

Example: a planning policy bug currently lives in a runtime runner module.

- `Runtime owner`: runtime orchestration layer
- `First fix owner`: runtime orchestration layer
- `Canonical long-term owner`: domain or application layer
- `Type or capability owner`: shared core layer
- `Competing owners that are wrong`: UI layer, platform shell, adapter or integration layers

## Additional Resource

For a reusable classification matrix and example splits, see [references/ownership-matrix.md](references/ownership-matrix.md).
