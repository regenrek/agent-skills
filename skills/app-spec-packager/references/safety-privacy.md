# Safety, Privacy, and Security Reference

Use this file whenever an app handles accounts, payments, AI, personal data, sensitive data, UGC, minors, regulated domains, or high-safety-risk workflows.

## Data classification

Classify all data before writing architecture or tasks.

```text
PUBLIC: marketing copy, public docs, public product metadata.
INTERNAL: operational metrics, non-sensitive logs, feature flags.
PERSONAL: email, name, account ID, device ID, IP address.
SENSITIVE: health, mental health, addiction, sexuality, biometrics, precise location, financial data, legal data, minors' data, private messages, AI prompts/responses.
SECRET: API keys, tokens, encryption keys, credentials.
```

## Data inventory template

```text
Data item:
Classification:
Collected from:
Stored where:
Sent to:
Used for:
Retention:
Deletion behavior:
Export behavior:
Analytics allowed: yes/no
Logging allowed: yes/no
```

## Privacy requirements

Default production requirements:

- Define local data, server data, provider data, and analytics data separately.
- Minimize data sent to third parties.
- Avoid storing sensitive full-text content on servers unless central to the product.
- Include user-facing consent for third-party AI, payments, location, health, biometrics, contacts, or device permissions.
- Include data deletion and export flows.
- Include retention windows for every server-side data type.
- Include a no-content logging rule for sensitive text, prompts, private notes, chat messages, medical/legal/financial info, and exact locations.
- Specify whether backups retain deleted data temporarily and for how long.
- Specify privacy policy and platform disclosure requirements as release tasks.

## Security requirements

Default production requirements:

- Use server-side authorization for every protected action.
- Keep secrets out of clients.
- Encrypt sensitive data in transit and at rest.
- Use secure cookie/session settings for web apps.
- Use Keychain/encrypted storage for mobile secrets.
- Use rate limits for auth, AI, payments, exports, and write-heavy endpoints.
- Use idempotency keys for payments, webhooks, and retried create operations.
- Scrub PII and content from logs, traces, crash reports, and analytics.
- Use environment separation: local, staging, production.
- Define backup, restore, and migration testing.
- Define incident response and provider outage behavior.

## AI privacy and safety

Required for AI features:

- Define every AI mode: chat, classify, summarize, generate, recommend, agentic tool use.
- Define exact context sent to model providers.
- Define what must never be sent.
- Define whether prompts/responses are stored locally, server-side, provider-side, or not at all.
- Prefer a provider abstraction through backend services for production.
- Include a user consent screen for cloud AI when personal or sensitive data may be sent.
- Include safety pre-checks for risky input and post-checks for risky output.
- Include prompt injection defenses for tool-using or retrieval-augmented AI.
- Include model fallback behavior that preserves safety constraints.
- Include evals and red-team cases in QA.

## Safety risk taxonomy

Use these categories when relevant:

```text
S0: No meaningful safety risk.
S1: Mild user harm possible through confusion, frustration, or wrong output.
S2: Sensitive personal content, but low immediate harm.
S3: High-impact domain: health, finance, legal, employment, education, minors, addiction, sexuality, biometrics, precise location.
S4: Acute risk: self-harm, violence, dangerous substances, medical emergency, stalking, fraud, illegal activity, crisis.
```

For S3/S4 apps, include explicit boundaries, refusal/escalation behavior, legal/platform review, and red-team tests.

## Sensitive domain defaults

### Health or mental health

- Do not claim diagnosis, treatment, prevention, cure, or emergency support unless the product is legally and clinically built for that.
- Include crisis boundaries and emergency guidance for acute risk.
- Do not let AI replace professionals in high-risk contexts.

### Finance

- Do not provide personalized investment, tax, insurance, or lending advice unless compliance requirements are specified.
- Include risk disclosures and jurisdiction assumptions.

### Legal

- Do not provide legal advice or attorney-client claims unless legal review and jurisdiction constraints are specified.
- Include "information only" boundaries where appropriate.

### Minors

- Include age gates, parental consent logic if needed, data minimization, and app store/platform content ratings.
- Do not collect sensitive data from minors without explicit legal requirements.

### Location and biometrics

- Ask whether precise location or biometrics are truly needed.
- Prefer coarse location or on-device biometric auth over storing biometric data.

### UGC/community

- Include moderation, reporting, blocking, escalation, spam prevention, and legal takedown flows.
- Do not add community features by default to sensitive products.

## Logging policy template

```text
Allowed logs:
- request ID
- user/account ID hash
- endpoint
- status code
- latency
- plan/tier
- rate limit bucket
- provider/model name
- token count or cost estimate

Forbidden logs:
- user messages
- AI prompts/responses
- private notes
- exact sensitive categories
- medical/legal/financial details
- payment card details
- secrets or tokens
```

## Consent copy template

Use neutral, precise language:

```text
To use [feature], [App Name] sends [specific data] to [provider/type of provider] to [purpose]. We [do/do not] store this content on our servers. You can disable this feature in Settings. See Privacy for details.
```

## Release review items

Always list the following when relevant:

- Privacy policy.
- Terms of service.
- Data processing agreements with providers.
- App store privacy labels or web cookie disclosures.
- Security review.
- DPIA or equivalent assessment for high-risk processing.
- AI provider retention settings.
- Incident response owner and escalation path.
