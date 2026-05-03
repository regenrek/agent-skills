---
name: app-spec-packager
description: Use this skill when the user wants to turn an application, product, startup idea, SaaS, mobile app, web app, API, AI product, or internal tool into a production-ready Markdown specification package for coding agents. Creates PRD/product spec, UX flows, design system brief, technical architecture, ADRs, AI/safety/privacy specs, API/data model, client/backend implementation specs, QA acceptance tests, release readiness, and executable task checklists. Do not use for simple one-off coding tasks unless the user asks for a complete spec, PRD, ADR, project plan for coding agents, or build package.
---

# App Spec Packager

Create complete, production-ready specification packages that coding agents can use to build applications without needing timelines, storypoints, budgets, or sprint planning.

## Default output

Create a Markdown package folder and, when artifact/file output is available, also create a zip. Use this default structure unless the user asks otherwise:

```text
[app-slug]-spec/
  README.md
  PRODUCT_SPEC.md
  UX_FLOWS.md
  DESIGN_SYSTEM_SPEC.md
  TECH_ARCHITECTURE.md
  ADRS.md
  AI_SPEC.md                         # only if AI/automation/model behavior is relevant
  SAFETY_PRIVACY_SECURITY.md
  API_AND_DATA_MODEL.md
  CLIENT_IMPLEMENTATION_SPEC.md
  BACKEND_IMPLEMENTATION_SPEC.md      # only if backend/API/server work is relevant
  SUBSCRIPTION_BILLING_SPEC.md        # only if monetization/payments are relevant
  ANALYTICS_OBSERVABILITY_SPEC.md
  QA_ACCEPTANCE_TESTS.md
  RELEASE_READINESS.md
  TASKS.md
  REFERENCES.md                       # include only when research or external facts were used
```

Use `scripts/create_spec_package.py` to scaffold the package when helpful, then fill every file with application-specific content.

## Core workflow

1. Capture the app intent, platform, target users, core workflows, data sensitivity, AI needs, monetization, integrations, and launch constraints.
2. Ask only blocking questions. If the user has already given enough context, proceed and mark assumptions explicitly.
3. Research current facts when the spec depends on recent platform rules, SDK versions, app store rules, laws, payments, AI providers, security requirements, or framework best practices. Prefer official sources. Put citations and source notes in `REFERENCES.md`.
4. Choose the relevant document set. Omit docs that are truly irrelevant, but keep privacy/security, QA, and tasks for production builds.
5. Write requirements as precise, testable statements with stable IDs.
6. Convert the spec into executable tasks for coding agents. Every task needs acceptance criteria and tests.
7. Validate the package against `references/validation-checklist.md` before final output.

## Reference loading

Read these files as needed:

- `references/document-blueprints.md`: full section templates for each generated document.
- `references/platform-modules.md`: platform-specific concerns for iOS, Android, web, backend, AI, payments, B2B, and regulated products.
- `references/safety-privacy.md`: mandatory when the app has accounts, AI, payments, minors, health, mental health, financial/legal advice, location, biometrics, UGC, sensitive data, or safety risk.
- `references/task-taxonomy.md`: mandatory before writing `TASKS.md`.
- `references/validation-checklist.md`: mandatory before finalizing.

## Writing rules

- Do not include storypoints, budget, timelines, Gantt charts, sprint plans, or staffing plans unless explicitly requested.
- Do not produce vague epics. Produce concrete build tasks.
- Do not over-ask. Use assumptions when safe and reversible.
- Do not bury non-goals. Put them near the top of `PRODUCT_SPEC.md` and repeat critical ones in `TASKS.md` as "Do not do" constraints.
- Do not use placeholders for known information. Use placeholders only for genuinely unknown values and list them in an "Open decisions" section.
- Do not make legal, medical, financial, or app-review certainty claims. Specify compliance requirements and mark them for legal or platform review.
- Do not recommend storing sensitive content by default. Minimize data, separate local/server/provider data, and define retention.
- Do not call third-party AI providers directly from client apps unless the app is a prototype and the user explicitly accepts that risk.
- Do not create community, UGC, payments, AI memory, location tracking, biometric capture, or health data flows without explicit safety/privacy requirements.

## Requirements style

Use stable IDs:

```text
REQ-PROD-001
REQ-UX-001
REQ-ARCH-001
REQ-AI-001
REQ-SEC-001
REQ-API-001
REQ-IOS-001
REQ-WEB-001
REQ-BE-001
REQ-QA-001
```

Every major requirement should answer:

```text
What must happen?
When does it happen?
Who or what triggers it?
Where is state stored?
What are the edge cases?
How is it tested?
What must never happen?
```

## Task style

Use the task template from `references/task-taxonomy.md`. A good task includes:

```text
Task ID
Title
Goal
Context
Requirements
Files or areas likely involved
Acceptance criteria
Tests
Dependencies
Do not do
```

Make tasks implementable by coding agents with minimal back-and-forth. Prefer small, verifiable tasks over broad epics.

## Production default assumptions

Use these defaults unless user context contradicts them:

- Prefer native client stacks when platform quality depends on deep platform integration.
- Prefer typed languages, explicit API contracts, migrations, and automated tests.
- Prefer backend mediation for AI, billing, rate limits, and sensitive integrations.
- Prefer local-first or data-minimized designs for sensitive applications.
- Prefer provider abstraction for AI and payments where lock-in is avoidable.
- Prefer no sensitive analytics. Track product events without content or sensitive categories.
- Include accessibility, localization readiness, error states, offline states, observability, deletion/export, and release readiness.

## Final response

Return links to the generated folder or zip. Briefly state what was created and call out any assumptions or items that require legal/platform/security review.
