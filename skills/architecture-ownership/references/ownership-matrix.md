# Architecture Ownership Reference

Use this reference to classify common ownership questions in layered codebases.

Before making a final call:

- read the repo's architecture and boundary docs
- map the generic layers below onto the repo's concrete package, module, crate, or service names
- prefer one canonical owner for each rule or policy

## Runtime Ownership

- `UI layer`
  - visible UI state
  - navigation
  - rendering
  - presentation-oriented derived state
- `Platform shell`
  - desktop shell, mobile shell, browser bridge, or OS bridge
  - local device integration
  - filesystem, permission, or process/session plumbing
  - platform-local persistence helpers
- `Runtime orchestration layer`
  - request routing
  - background coordination
  - worker or agent lifecycle management
  - event publication
- Shared or pure layers
  - parsing
  - normalization
  - validation
  - reusable services without runtime ownership

## Canonical Ownership

- `Domain or application layer`
  - canonical business rules and product workflow
  - reusable application services
  - cross-interface behavior and policy
- `Shared core layer`
  - shared structs, types, enums, value objects, validation, and normalization
  - pure logic used in multiple places
- `Runtime orchestration layer`
  - runtime composition
  - dispatch
  - process-level orchestration
  - not the default home for reusable product policy
- `Adapter or integration layer`
  - concrete protocol integration
  - provider-specific or vendor-specific behavior
  - not cross-provider product policy

## Fast Classification

Ask these in order:

1. Is this visible UI state or presentation logic?
   - `UI layer`
2. Is this shell, device, OS, browser, or platform bridge logic?
   - `Platform shell`
3. Is this runtime composition, request dispatch, lifecycle management, or background coordination?
   - `Runtime orchestration layer`
4. Is this reusable product behavior or canonical business policy?
   - `Domain or application layer`
5. Is this pure shared type, validation, normalization, or capability logic?
   - `Shared core layer`
6. Is this concrete provider, protocol, transport, or vendor integration?
   - `Adapter or integration layer`

## Ownership Language

Always distinguish:

- `Runtime owner`
- `First fix owner`
- `Canonical long-term owner`

These are often different.

## Typical Examples

### Workflow execution policy

- Common layers:
  - domain or application layer
  - shared core layer
  - runtime orchestration layer
- Typical split:
  - runtime orchestration layer for runtime entry and sequencing
  - domain or application layer for reusable workflow policy
  - shared core layer for shared types and capability rules

### UI state and restore state

- Primary layers:
  - UI layer
  - optional platform shell helpers for local restore plumbing
- Not owner:
  - runtime orchestration layer

### Native or platform session behavior

- Primary layers:
  - platform shell
  - optional UI layer for presentation state
- Not owner:
  - domain or application layer unless the behavior is reusable product policy

### Vendor-specific behavior

- Capability or type definitions:
  - shared core layer
- Concrete provider or vendor integration:
  - adapter or integration layer
- Reusable cross-provider product policy:
  - domain or application layer
- Runtime patch point:
  - often runtime orchestration layer

## Cleanup Rule

When current placement is wrong:

- patch the wrong behavior where it currently happens
- move reusable policy to the canonical owner
- remove the duplicate, fallback, or compatibility path
