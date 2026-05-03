# Task Taxonomy

Use this file before writing `TASKS.md`. The goal is to create executable work items for coding agents, not project management tickets.

## Task ID prefixes

```text
TASK-FND: foundation, repo setup, tooling, CI
TASK-DES: design system, components, visual language
TASK-UX: flows, navigation, state machines
TASK-IOS: iOS/iPadOS/macOS client
TASK-AND: Android client
TASK-WEB: web frontend
TASK-DESK: desktop client
TASK-BE: backend/API/service work
TASK-DATA: database, migrations, data lifecycle
TASK-AI: AI orchestration, prompts, providers, evals
TASK-SEC: privacy, security, consent, deletion/export
TASK-PAY: subscriptions, payments, entitlements
TASK-ANA: analytics, observability, monitoring
TASK-QA: tests, fixtures, acceptance suites
TASK-REL: release, app store, deployment readiness
```

## Task template

```markdown
### TASK-[PREFIX]-[NUMBER]: [Action-oriented title]

Goal:
[One sentence describing the outcome.]

Context:
[Relevant product/architecture references and why the task exists.]

Requirements:
- [Concrete requirement]
- [Concrete requirement]

Files or areas likely involved:
- [Path or area]

Acceptance criteria:
- [Observable criterion]
- [Observable criterion]

Tests:
- [Unit/integration/UI/eval/security test]

Dependencies:
- [Task IDs or "None"]

Do not do:
- [Important boundary]
```

## Good task qualities

- One agent can complete the task without interpreting a vague epic.
- Acceptance criteria can be verified manually or by tests.
- The task says what must not be done.
- Dependencies are explicit.
- The task references requirements or docs by ID where possible.
- The task avoids hidden product decisions.

## Bad task examples

```text
Build backend.
Make UI nice.
Implement AI.
Add security.
Create onboarding.
```

Replace with scoped tasks:

```text
Implement POST /v1/sessions with idempotency and validation.
Create onboarding stepper with persisted draft state and resume behavior.
Implement AI provider adapter interface with Claude and OpenAI implementations.
Add no-content log scrubber middleware and tests.
```

## Task ordering

Default ordering:

1. Foundation and repo structure.
2. Data models and state machines.
3. Client shell and navigation.
4. Backend/API contracts and migrations.
5. Core product flows.
6. AI/provider flows if relevant.
7. Payments/subscriptions if relevant.
8. Safety/privacy/security tasks.
9. Analytics/observability.
10. QA, release, and app store/deployment readiness.

Do not force chronological sprint planning. Ordering is for dependency clarity only.

## Required task groups

Every production spec should include at least:

- Foundation setup.
- Core product flow implementation.
- Persistence/data lifecycle.
- Error/offline/loading states.
- Privacy/security tasks.
- QA acceptance tasks.
- Release readiness tasks.

Add these when relevant:

- AI tasks.
- Billing/payment tasks.
- Backend/API tasks.
- Admin/enterprise tasks.
- Moderation/UGC tasks.
- Mobile app store tasks.

## Acceptance criteria style

Use observable outcomes:

```text
- Creating a draft persists after app restart.
- Unauthorized requests return 401 and do not modify data.
- Free users receive RATE_LIMITED after exceeding their monthly AI limit.
- The backend logs request metadata but not prompt or response content.
- Screen reader announces the modal title and primary action.
```

Avoid vague criteria:

```text
- Works well.
- Looks good.
- Handles errors.
- Is secure.
```

## Test categories

Use the relevant categories per task:

```text
Unit tests: pure functions, reducers, validators, model transitions.
Integration tests: API + DB, provider adapters, webhooks, auth.
UI tests: navigation, form validation, accessibility labels, state restoration.
E2E tests: complete critical journeys.
Contract tests: API request/response schemas.
Security tests: authz, rate limits, log scrubbing, secret handling.
Privacy tests: deletion/export, no-content analytics/logging.
AI evals: prompt behavior, refusal behavior, safety cases, regression examples.
Billing tests: entitlement updates, webhook idempotency, grace periods.
Release tests: smoke tests, environment config, rollback path.
```

## Global "Do not do" patterns

Include these where relevant:

- Do not store sensitive user content in analytics or logs.
- Do not call provider APIs from the client if backend mediation is required.
- Do not add unaudited dependencies for auth, payments, cryptography, or AI safety.
- Do not create unbounded background jobs or retries.
- Do not expose secrets in client bundles, mobile apps, logs, or crash reports.
- Do not make product, legal, medical, or financial claims beyond the spec.
