# Document Blueprints

Use these blueprints to generate the spec package. Adapt section names to the app, but preserve the substance.

## README.md

```markdown
# [App Name] Specification Package

## Purpose
[One paragraph explaining what this package enables coding agents to build.]

## Package contents
[List files with one-line purpose.]

## Global assumptions
- [Assumption 1]

## Global non-goals
- [Non-goal 1]

## Critical invariants
- [Invariant 1]

## How coding agents should use this package
1. Read README.md, PRODUCT_SPEC.md, TECH_ARCHITECTURE.md, and TASKS.md first.
2. Load specialized docs only when implementing that area.
3. Treat TASKS.md acceptance criteria as the source of completion truth.
```

## PRODUCT_SPEC.md

Required sections:

```markdown
# Product Specification

## Vision
## Product promise
## Target users
## Problems solved
## Product principles
## V1 scope
## Explicit non-goals
## User personas
## Core objects and vocabulary
## Core user journeys
## Feature requirements
### [Feature]
- REQ-PROD-001: [testable requirement]
## Plans, tiers, monetization
## Integrations
## Content, moderation, and safety boundaries
## Success metrics
## Analytics constraints
## Open decisions
```

Rules:
- Include product principles that guide tradeoffs.
- List non-goals early. Coding agents need boundaries.
- Do not include timelines or storypoints unless requested.
- Make monetization behavior precise: free vs paid, rate limits, trial behavior, cancellation behavior.

## UX_FLOWS.md

Required sections:

```markdown
# UX Flows

## Navigation model
## Screen map
## State machine
## Onboarding flow
## Primary creation/setup flow
## Home or dashboard states
## Detail states
## Error, empty, offline, loading states
## Paywall and entitlement states
## Settings, export, delete, account flows
## Accessibility behavior
## Localization behavior
## Acceptance criteria
```

State machine format:

```text
STATE_A -> STATE_B
Trigger: [event]
Guard: [condition]
Side effects: [state writes, API calls, notifications]
Failure behavior: [what happens if it fails]
```

## DESIGN_SYSTEM_SPEC.md

Required sections:

```markdown
# Design System Specification

## Design principles
## Brand tone
## Visual direction
## Color system
## Typography
## Spacing and layout
## Component system
## Motion and haptics
## Iconography and illustration
## Data visualization rules
## Accessibility requirements
## Platform-specific UI conventions
## Do not do
```

Rules:
- Do not merely say "modern" or "clean". Define concrete UI behavior.
- Include dark mode/light mode if relevant.
- Include reduced motion, dynamic type/text scaling, contrast, keyboard navigation, and screen reader behavior.

## TECH_ARCHITECTURE.md

Required sections:

```markdown
# Technical Architecture

## Architecture goals
## System context diagram
## Client architecture
## Backend architecture
## Data architecture
## AI architecture
## Auth and identity
## Payment/subscription architecture
## Integrations
## Security architecture
## Privacy architecture
## Observability
## Deployment environments
## Failure modes and fallback behavior
## Scalability assumptions
## Open technical decisions
```

Diagram format example:

```text
Client
  -> API Gateway
  -> Backend Service
  -> Database
  -> Queue/Worker
  -> Third-party Provider
```

Rules:
- Separate client, backend, provider, and analytics data flows.
- Specify what is not stored.
- Specify rate limits and idempotency where relevant.
- Specify environment separation: local, staging, production.

## ADRS.md

Use Architecture Decision Records for major irreversible or expensive decisions.

```markdown
# ADRs

## ADR-001: [Decision title]

Status: Proposed | Accepted | Superseded

### Context
### Decision
### Alternatives considered
### Consequences
### Risks
### Follow-up tasks
```

Common ADRs:
- Native vs cross-platform client.
- Backend vs no backend.
- Local-first vs server-first storage.
- Auth strategy.
- Payment provider.
- AI provider and model routing.
- No chat/content logging.
- Analytics limitations.
- Cloud region and compliance posture.

## AI_SPEC.md

Include only if AI, automation, recommendations, agents, semantic search, LLMs, embeddings, or chat are relevant.

```markdown
# AI Specification

## AI product role
## AI modes
## Model/provider strategy
## Prompt architecture
## System prompts
## Tool/function calling
## Context construction
## Memory policy
## Safety policy
## Rate limits and plan limits
## Evaluation plan
## Red-team cases
## Fallback behavior
## Logging and retention
## User consent copy
```

Rules:
- Never define AI as magical. Define exact inputs, outputs, and constraints.
- Define pre-checks and post-checks for safety-critical AI.
- Include provider abstraction unless user requires a single provider.
- Specify what context is sent and what is not sent.

## SAFETY_PRIVACY_SECURITY.md

Required for production apps.

```markdown
# Safety, Privacy, and Security

## Data inventory
## Data classification
## Local data
## Server data
## Third-party/provider data
## Analytics data
## Consent and disclosure requirements
## Retention policy
## Export and deletion policy
## Logging policy
## Security controls
## Abuse prevention
## Safety risk taxonomy
## Crisis/escalation behavior if relevant
## Compliance notes
## Legal/platform review checklist
```

Rules:
- Treat unknown sensitive data as sensitive until proven otherwise.
- Separate "we store" from "provider may process".
- Include deletion/export for user data.
- Include no-content logging if AI or sensitive data exists.

## API_AND_DATA_MODEL.md

Required when backend, sync, APIs, payments, or integrations exist.

```markdown
# API and Data Model

## API principles
## Authentication and authorization
## Endpoint summary
## Endpoint definitions
### POST /v1/example
Request:
Response:
Errors:
Rate limits:
Idempotency:
Security notes:
## Client data models
## Server data models
## Provider data models
## Database schema
## State transitions
## Migrations
## Retention and deletion behavior
```

Rules:
- Use explicit JSON schemas or TypeScript-like interfaces.
- Include error codes and rate limit responses.
- Include idempotency for payments, creation flows, and webhooks.

## CLIENT_IMPLEMENTATION_SPEC.md

Use for iOS, Android, web, desktop, or cross-platform clients.

```markdown
# Client Implementation Specification

## Platform target
## App structure
## Navigation
## State management
## Local persistence
## Networking
## Auth/session handling
## Payment/entitlement handling
## Notifications
## Accessibility
## Localization
## Error handling
## Offline behavior
## Testing requirements
```

For multi-platform apps, either create one file per client or include platform subsections.

## BACKEND_IMPLEMENTATION_SPEC.md

Required for server, API, AI proxy, subscriptions, sync, or admin operations.

```markdown
# Backend Implementation Specification

## Service structure
## API routing
## Database and migrations
## Auth/identity
## Rate limits
## Background jobs
## Webhooks
## Provider adapters
## Logging
## Observability
## Security controls
## Data deletion/export jobs
## Deployment requirements
## Testing requirements
```

## SUBSCRIPTION_BILLING_SPEC.md

Required for subscriptions, purchases, credits, paid AI, usage-based billing, or enterprise plans.

```markdown
# Subscription and Billing Specification

## Plans and entitlements
## Free plan behavior
## Paid plan behavior
## Trials and promotions
## Upgrade/downgrade/cancel behavior
## Payment provider architecture
## Webhooks and idempotency
## Entitlement caching
## Usage limits
## Refund and billing failure behavior
## Analytics constraints
## Acceptance tests
```

## ANALYTICS_OBSERVABILITY_SPEC.md

```markdown
# Analytics and Observability

## Product analytics principles
## Allowed events
## Forbidden events/properties
## Event schema
## Error monitoring
## Performance monitoring
## Security audit events
## AI/provider usage monitoring
## Cost monitoring
## Alerting
## Dashboards
```

Rules:
- For sensitive apps, never include raw user content, sensitive categories, prompts, private notes, messages, health info, financial details, or exact locations in analytics.

## QA_ACCEPTANCE_TESTS.md

```markdown
# QA and Acceptance Tests

## Test strategy
## Unit tests
## Integration tests
## UI/E2E tests
## Accessibility tests
## Security tests
## Privacy tests
## AI evals and safety red-team tests
## Billing tests
## Offline/failure tests
## Release smoke test
## Feature acceptance matrix
```

Feature acceptance matrix:

```text
Feature | Requirements | Tasks | Tests | Status
```

## RELEASE_READINESS.md

```markdown
# Release Readiness

## Environment checklist
## Build/release process
## App store or deployment checklist
## Privacy disclosures
## Legal review items
## Security review items
## Monitoring and incident response
## Rollback plan
## Provider outage plan
## Launch smoke tests
```

## TASKS.md

Write after all other docs. Use `references/task-taxonomy.md`.

Required sections:

```markdown
# Build Tasks

## Global instructions for coding agents
## Global non-goals
## Task dependency map
## Tasks
### TASK-[AREA]-001: [Title]
...
```
