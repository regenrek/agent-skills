# Audit Prompts

## Generic Full Audit

```text
Use $find-duplicate-ownership to audit this codebase for duplicate ownership and hidden second sources of truth.

Goal:
Find places where the same business rule, normalization, validation, canonicalization, defaulting, mapping, or persistence policy is owned in more than one place.

Focus on:
- frontend and backend owning the same contract differently
- runtime mutators re-applying boundary repair or coercion
- duplicate helpers with the same semantics but different names
- thin wrappers that hide a second path
- validation or default constants duplicated across layers
- serialization or canonicalization logic copied across modules
- local helper clones in hooks, components, controllers, or services instead of one domain owner
- persistence shapes that differ from runtime shapes and require translation glue
- query, cache, or store logic acting as a second owner of domain rules

Do not flag as problems by default:
- pure UI-only formatting
- security or path sandbox canonicalization with one clear owner
- vendor or protocol adapters that are clearly boundary-only
- necessary runtime clamp or math logic with one clear owner

For each finding, output:
1. severity
2. rule or contract being multiply owned
3. current competing owners
4. why this is duplicate ownership rather than legitimate boundary work
5. exact files or symbols
6. recommended single owner
7. hard-cut cleanup plan: delete / keep / rename
8. classification

Start with a taxonomy, then concrete findings ordered by severity.
```

## Layered-App Audit

```text
Use $find-duplicate-ownership to audit this layered application for duplicate ownership.

Primary targets:
- runtime state versus durable state
- API contract ownership
- persistence mapping
- query, cache, or store ownership
- duplicated helper ownership in UI, services, domain libraries, and adapters

Repository policy:
- hard cut only
- one canonical current-state implementation
- no shims
- no fallbacks
- no compatibility glue
- fail fast
- one source of truth per business rule

Deliver:
- a taxonomy first
- then concrete findings with file paths and symbols
- then a prioritized refactor backlog by impact versus effort
- clearly separate real SSOT bugs from harmless local utilities

Be especially suspicious of code that normalizes after reading trusted state or after mutating already-canonical runtime state.
```

## Parallel Subagent Audit

```text
Use $find-duplicate-ownership to audit this codebase for duplicate ownership.
Spawn one `ownership-taxonomy-mapper`, three `duplicate-ownership-explorer` agents for disjoint slices, and one `ssot-judge`.
Wait for all of them and merge the result.

Slices:
1. runtime state and persistence
2. contracts, helpers, and canonicalization
3. adapters, queries, and caches

Return:
- shared taxonomy
- concrete findings by slice
- merged severity order
- winning owner for each finding
- hard-cut delete or keep or rename plan
```
