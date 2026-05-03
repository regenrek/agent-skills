# Platform Modules

Use this reference to add platform-specific requirements without making the core spec bloated. Include only modules relevant to the user's application.

## Universal production concerns

Include for every production application:

- Authentication or identity strategy, even if the answer is "anonymous/no account".
- Data storage locations: client, server, provider, analytics.
- Privacy and security controls.
- Error, empty, loading, offline, and degraded states.
- Accessibility requirements.
- QA acceptance tests.
- Observability and incident handling.
- Release readiness.

## iOS / iPadOS / macOS apps

Add sections for:

- Native stack decision: SwiftUI/UIKit/AppKit, deployment target, package structure.
- App Store review constraints and metadata assumptions.
- StoreKit or external payment constraints.
- Local persistence: SwiftData, Core Data, SQLite, Keychain, file protection.
- Privacy: App Privacy details, user consent, data export/deletion.
- Platform integrations: notifications, widgets, App Intents, Shortcuts, HealthKit, Screen Time, Apple Watch, iCloud, Face ID/Touch ID.
- Accessibility: VoiceOver, Dynamic Type, Reduce Motion, contrast, focus order.
- Offline behavior and sync conflict behavior.
- TestFlight/release notes if release spec is included.

Decision default:
- Use native iOS for premium Apple-platform UX or deep Apple integrations.
- Do not add HealthKit, Screen Time, precise location, biometrics, or iCloud sync unless justified and specified.

## Android apps

Add sections for:

- Native stack: Kotlin, Jetpack Compose, Android target/min SDK.
- Google Play policy and app content rating assumptions.
- Billing: Google Play Billing or external payments where allowed.
- Local persistence: Room, DataStore, encrypted storage.
- Notifications, foreground services, permissions, biometric auth.
- Accessibility: TalkBack, scalable text, contrast, keyboard focus.
- Offline/sync behavior.

Decision default:
- Use native Android when platform experience, permissions, or Play policy constraints matter.

## Web apps / SaaS

Add sections for:

- Frontend stack: framework, routing, rendering, state, forms, validation.
- Backend/API boundary: BFF vs API-first vs server actions.
- Auth: email/password, passkeys, OAuth, SSO, magic links, anonymous users.
- Billing: Stripe, Paddle, Lemon Squeezy, enterprise invoicing, tax/VAT handling.
- Hosting: CDN/edge, server hosting, region, environment separation.
- Browser compatibility and responsive breakpoints.
- Accessibility: WCAG target, keyboard navigation, screen readers, focus management.
- Security: CSRF, XSS, CSP, cookies, session expiration, rate limits.
- Observability: logs, traces, metrics, RUM if allowed.

Decision default:
- For production SaaS, prefer typed code, explicit API schemas, migrations, secret management, and server-side authorization checks.

## Backend / API products

Add sections for:

- API style: REST, GraphQL, gRPC, event-driven.
- Service boundaries and dependency direction.
- Database selection, migrations, backup/restore.
- Cache and queues.
- AuthN/AuthZ, RBAC/ABAC if needed.
- Idempotency for creation, payments, webhooks, and retries.
- Rate limiting, abuse prevention, and quota enforcement.
- Error model and status codes.
- Secrets, encryption, audit logs, no-content logs.
- Deployment environments and rollback.

Decision default:
- Use Postgres for most production app data unless the domain needs a different primary datastore.
- Use Redis or an equivalent for rate limits, short-lived locks, and cache when needed.
- Use queues/workers for slow provider calls, emails, exports, and webhook retries.

## AI products and AI features

Add sections for:

- AI role: assistant, classifier, recommender, generator, summarizer, agent, search, automation.
- Provider strategy: direct provider, gateway, self-hosted, on-device, hybrid.
- Model routing by use case and plan.
- Prompt architecture and prompt versioning.
- Context minimization and memory policy.
- Tool/function calling contract.
- Safety pre-checks and post-checks.
- Evals, red-team tests, refusal behavior, and escalation behavior.
- Logging and retention: user content, prompts, responses, embeddings, traces.
- User consent and disclosures.
- Cost controls: rate limits, token budgets, fallback models.

Decision default:
- Do not call AI providers directly from client apps in production.
- Use backend mediation for API keys, rate limits, safety, provider routing, and billing limits.
- Do not store full AI chat history unless the user explicitly needs it and privacy requirements define retention.

## Payments and monetization

Add sections for:

- Monetization model: subscriptions, one-time purchases, credits, usage-based, enterprise, ads.
- Plans and entitlement matrix.
- Provider and platform constraints.
- Webhooks, idempotency, billing retry, refunds, grace periods.
- Entitlement cache and offline behavior.
- Paywall states and copy assumptions.
- Revenue analytics without sensitive data.

Decision default:
- Do not use ads for sensitive apps unless the user explicitly asks and tracking implications are specified.
- For mobile apps, respect platform payment rules. Mark app-review/legal review items explicitly.

## B2B / enterprise products

Add sections for:

- Organization/workspace model.
- Roles and permissions.
- SSO/SAML/OIDC if required.
- Audit logs.
- Admin console.
- Data residency, retention, export, DPA, security review package.
- Enterprise billing and invoicing.
- Multi-tenant isolation.

## Marketplace, community, or UGC products

Add sections for:

- UGC types and moderation rules.
- Reporting, blocking, appeals, takedowns.
- Trust levels, spam prevention, abuse rate limits.
- Content retention and deletion.
- Minors and age gating.
- Legal/platform review items.

Decision default:
- Avoid UGC/community in V1 for safety-sensitive apps unless it is central to the product.

## Sensitive or regulated domains

Domains include health, mental health, addiction, minors, finance, legal, insurance, employment, education, biometric data, precise location, sexuality, political opinions, religion, and high-risk decision systems.

Add sections for:

- Domain boundaries and disclaimers.
- Eligibility and age gating.
- Risk taxonomy.
- Escalation/referral behavior.
- Compliance notes.
- Human review if needed.
- Data minimization and retention.
- Legal review and safety testing.

Decision default:
- Do not claim diagnosis, treatment, legal advice, investment advice, guaranteed outcomes, or regulatory compliance without explicit legal signoff.
