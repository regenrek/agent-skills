---
name: find-duplicate-ownership
description: Find duplicate ownership, hidden second sources of truth, and contract drift in layered codebases. Use when reviewing normalization, validation, defaulting, canonicalization, persistence mapping, runtime-vs-durable state, duplicated helpers, query or cache ownership, or any "who owns this rule?" architecture question. Especially useful for SSOT audits across frontend, backend, shared core, and adapter layers, and when the user explicitly asks for duplicate-ownership exploration with subagents.
---

# Find Duplicate Ownership

## Overview

Audit the codebase for multiply-owned rules instead of blindly grepping `normalize`.
Classify each case as real SSOT drift, local dedupe cleanup, legitimate boundary work, or legitimate domain constraint.

## Workflow

1. Define the audit target before searching.
   Narrow by feature, contract, package, service, or file slice when possible.
   Good targets: session state, persistence contracts, runtime geometry, provider options, path helpers, JSON canonicalization.

2. Build a taxonomy first.
   Use these buckets:
   - `architecture / SSOT bug`: same business rule owned in more than one layer
   - `local dedupe cleanup`: same helper semantics copied nearby
   - `legitimate boundary adapter`: wire, vendor, or untrusted input transformation with one clear owner
   - `legitimate domain constraint`: runtime clamp, math, security, or path logic that cannot be removed architecturally

3. Search for ownership smells, not words.
   Look for:
   - validation, defaults, or clamps duplicated across frontend and backend
   - generated bindings or shared type aliases hiding the real contract owner
   - runtime mutators calling boundary repair or coercion
   - persisted shape differing from runtime shape and requiring glue
   - query, store, or cache logic re-owning domain policy
   - two helpers with the same semantics but different names
   - thin wrapper functions that hide a second path
   - copied deterministic serializers or hash inputs
   - local component, hook, or service helper clones instead of one domain owner

4. Separate true duplicates from valid boundaries.
   Do not flag these by default:
   - pure UI formatting or presentation transforms
   - provider or protocol adapters with one clear boundary owner
   - security or path canonicalization with one clear security owner
   - runtime-only clamp or math logic with one clear runtime owner

5. For each finding, name the winning owner.
   Always answer:
   - what exact rule is multiply owned
   - who owns it today
   - who should own it
   - what gets deleted in a hard cut
   - whether anything remains as real boundary adapter code

## Heuristics

- Be suspicious when frontend and backend both shape or repair the same contract.
- Be suspicious when trusted runtime state is "normalized" after every mutation.
- Be suspicious when query glue, cache glue, or store glue maps between two supposedly canonical state shapes.
- Be suspicious when multiple languages or services define the same min, max, enum, or default constants independently.
- Be suspicious when a helper exists in a domain library and again in a hook, component, controller, or service.

## Subagent Use

Only use subagents when the user explicitly asks for them or asks for parallel exploration.

Reusable read-only agent definitions live in this skill's `agents/` directory:

- `ownership-taxonomy-mapper.toml`
  Use first for broad slice mapping and taxonomy.
- `duplicate-ownership-explorer.toml`
  Use one per independent slice: persistence, runtime state, contracts, helpers, adapters.
- `ssot-judge.toml`
  Use after explorers when you need one strict verdict on winning owner and hard-cut cleanup.

Recommended fan-out:

- 1 taxonomy mapper
- 2 to 5 explorers for disjoint slices
- 1 SSOT judge to merge and challenge findings

Tell subagents:

- stay read-only
- cite files and symbols
- do not propose compatibility shims
- distinguish duplicate ownership from legitimate boundary work
- return winner owner plus delete or keep plan

## Output Contract

For each finding, return:

1. severity
2. rule or contract being multiply owned
3. competing owners
4. why it is a duplicate-owner bug or why it is legitimate boundary work
5. exact files or symbols
6. recommended single owner
7. hard-cut cleanup:
   - delete
   - keep
   - rename
8. classification:
   - architecture / SSOT bug
   - local dedupe cleanup
   - legitimate boundary adapter
   - legitimate domain constraint

Order findings by severity, then finish with a prioritized backlog by impact versus effort.

## Prompting

Use prompt patterns from [references/audit-prompts.md](references/audit-prompts.md).

## Guardrails

- Do not reduce the audit to `rg normalize`.
- Do not flag every adapter or clamp as bad architecture.
- Do not recommend wrappers, fallbacks, shims, or dual paths.
- Prefer deleting the losing owner, not introducing a mediator.
- If ownership is ambiguous because the diff is mixed or the contract is unclear, say so explicitly.
