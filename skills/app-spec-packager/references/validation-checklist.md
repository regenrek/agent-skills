# Validation Checklist

Run this checklist before finalizing a generated application spec package.

## Package completeness

- [ ] The package includes a README or index explaining how coding agents should use the docs.
- [ ] The product spec defines vision, scope, non-goals, personas, features, monetization if relevant, and open decisions.
- [ ] UX flows include state machines, empty/loading/error/offline states, and settings/account/privacy flows.
- [ ] Technical architecture separates client, backend, provider, data, analytics, and observability.
- [ ] ADRs cover major stack and data decisions.
- [ ] API/data models include request/response schemas, storage location, retention, and error behavior.
- [ ] Client/backend specs exist when applicable.
- [ ] AI spec exists if any AI, automation, recommendations, agents, or model calls are involved.
- [ ] Safety/privacy/security spec exists for production builds.
- [ ] QA acceptance tests cover the critical journeys.
- [ ] TASKS.md converts all major requirements into buildable tasks.

## Consistency

- [ ] File names are consistent across docs.
- [ ] Requirements IDs are stable and referenced by tasks/tests where useful.
- [ ] State names match across UX, data model, and tasks.
- [ ] Plan/tier names match across product, billing, API, and tasks.
- [ ] API endpoints match across architecture, data model, backend spec, and tasks.
- [ ] Data retention statements match across privacy, architecture, API/data model, and tasks.
- [ ] AI provider/model decisions match across AI spec, architecture, privacy, and tasks.

## Production readiness

- [ ] Auth/identity is specified, even if anonymous/no-account.
- [ ] Authorization rules are specified for protected resources.
- [ ] Migrations, backups, restore, and environment separation are addressed if backend data exists.
- [ ] Rate limits exist for auth, AI, payments, exports, and write-heavy endpoints as relevant.
- [ ] Idempotency exists for payments, webhooks, retried creation flows, and provider callbacks as relevant.
- [ ] Observability includes errors, performance, provider failures, and cost monitoring if relevant.
- [ ] Release readiness includes smoke tests, rollback/deployment behavior, and app store/platform notes if relevant.

## Privacy and safety

- [ ] Every data item has classification, storage location, retention, deletion, and export behavior.
- [ ] Sensitive content is not logged or sent to analytics.
- [ ] Third-party data sharing is disclosed and minimized.
- [ ] Consent flows exist for AI, payments, location, health, biometrics, contacts, and other sensitive permissions as relevant.
- [ ] Deletion/export flows are specified.
- [ ] High-risk domains include explicit boundaries and escalation/refusal behavior.
- [ ] Legal/platform review items are listed where needed.

## AI readiness

- [ ] AI modes are explicitly defined.
- [ ] Context sent to providers is minimized and documented.
- [ ] Memory/storage policy is explicit.
- [ ] Safety pre-checks and post-checks exist for high-risk AI.
- [ ] Prompt injection defenses exist for tool-using or retrieval AI.
- [ ] Provider fallback does not bypass safety.
- [ ] AI evals/red-team cases are included.
- [ ] AI rate limits and cost controls exist.

## Task quality

- [ ] Each task has goal, context, requirements, likely files/areas, acceptance criteria, tests, dependencies, and do-not-do constraints.
- [ ] No task is only "build X" or "make Y nice".
- [ ] There are tasks for privacy, security, QA, release readiness, and observability, not only feature work.
- [ ] Tasks avoid storypoints, estimates, budget, or staffing.
- [ ] Tasks are small enough for coding agents to implement independently.

## Source freshness

- [ ] Current-dependent claims are researched.
- [ ] Official sources are preferred for platform, SDK, payment, legal, and provider facts.
- [ ] REFERENCES.md lists sources, dates, and what facts were used.
- [ ] Unverified assumptions are marked as assumptions, not facts.

## Final handoff

- [ ] The final answer links to the folder or zip.
- [ ] The final answer mentions key assumptions.
- [ ] The final answer calls out legal, privacy, security, or platform-review items without overstating certainty.
