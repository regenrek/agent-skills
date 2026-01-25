---
name: security-leak-guardrails
description: Sets up secret-leak prevention guardrails with forbidden path checks, gitleaks config, CI secret scanning, and dependency updates. Use when hardening repos against credential leaks or when adding gitleaks, trufflehog, git hooks, or security checks.
---

# Security Leak Guardrails

Reusable workflow for preventing secrets from entering git and for continuously scanning a repo for leaks.

## Quick start

1. Inventory existing security tooling (gitleaks/trufflehog, hooks, workflows, dependabot).
2. Add forbidden-path checks and the hook script.
3. Add gitleaks config and a local security check script.
4. Add CI secret scanning and Dependabot.
5. Update .gitignore and document the policy.

## Workflow

### Step 1: Inventory
- Check for existing .gitleaks.toml, .github/workflows/*secret*, dependabot.yml, and hook tooling.
- If the repo already uses hooks (husky/lefthook/pre-commit), integrate instead of replacing.

### Step 2: Forbidden paths + hook
- Add .forbidden-paths.regex and keep it strict (no secrets in allowlists).
- Add scripts/hooks/block-forbidden-staged-files.mjs.
- If the repo is Node-based, add lefthook.yml and a prepare script to install hooks.

### Step 3: Gitleaks
- Add .gitleaks.toml with path-based allowlists only for test fixtures.

### Step 4: Local security check
- Add scripts/secleak-check.sh.
- If Node-based, add scripts in package.json: security:check and security:hooks.

### Step 5: CI secret scanning
- Add a workflow that runs TruffleHog (diff and full history) and Gitleaks.
- Pin actions by SHA and use --only-verified for TruffleHog.

### Step 6: Dependabot
- Add dependabot.yml for npm and GitHub Actions.

### Step 7: .gitignore
- Add runtime dirs and credential patterns to avoid accidental commits.

## Validation
- Run: node scripts/hooks/block-forbidden-staged-files.mjs
- Run: gitleaks git --no-banner --redact=100 --config .gitleaks.toml .
- Run: trivy fs --scanners secret,misconfig --exit-code 1 .

## References
- Templates: reference.md
- Examples: examples.md
