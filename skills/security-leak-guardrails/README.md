# Security Leak Guardrails

Add secret-leak prevention guardrails with forbidden path checks, gitleaks config, CI secret scanning, and dependency update hygiene.

## Install

```bash
# Codex
npx agentrig skill install codex agentrig/regenrek.security-leak-guardrails

# Claude
npx agentrig skill install claude agentrig/regenrek.security-leak-guardrails

# Cursor
npx agentrig skill install cursor agentrig/regenrek.security-leak-guardrails
```

## Prerequisites

Install the following tools to use this skill:

### Required

| Tool | Install | Purpose |
|------|---------|---------|
| **gitleaks** | `brew install gitleaks` | Scans git history for secrets |
| **Node.js** | `brew install node` | Runs the forbidden-path hook script |

### Recommended

| Tool | Install | Purpose |
|------|---------|---------|
| **trivy** | `brew install trivy` | Scans for secrets, misconfigs, and vulnerabilities |
| **lefthook** | `npm i -D lefthook` | Git hooks manager (Node repos) |

### Verify Installation

```bash
gitleaks version
trivy --version
node --version
```

## What Gets Set Up

1. **Forbidden path checks** — blocks commits containing secrets, keys, or sensitive files
2. **Gitleaks config** — scans git history with customizable allowlists
3. **Local security script** — one command to run all security checks
4. **CI secret scanning** — GitHub workflow with TruffleHog + Gitleaks
5. **Dependabot** — keeps dependencies updated to reduce vulnerabilities

## Usage

Ask your AI agent:

> "Set up security guardrails for this repo"

Or reference the skill directly:

> "Use the security-leak-guardrails skill to harden this project"

## Included Resources

- `reference.md` contains templates for forbidden paths, gitleaks, CI, hooks, and Dependabot.
- `examples.md` contains usage examples.
- `scripts/secleak-check.sh` runs the local security check once configured.

## Files Created

```
.forbidden-paths.regex          # Patterns to block from commits
.gitleaks.toml                  # Gitleaks configuration
scripts/hooks/block-forbidden-staged-files.mjs
scripts/secleak-check.sh
.github/workflows/secret-scan.yml
.github/dependabot.yml
lefthook.yml                    # Node repos only
```

## Quick Validation

After setup, run these to verify everything works:

```bash
# Check forbidden paths hook
node scripts/hooks/block-forbidden-staged-files.mjs

# Run gitleaks
gitleaks git --no-banner --redact=100 --config .gitleaks.toml .

# Run trivy (if installed)
trivy fs --scanners secret,misconfig --exit-code 1 .
```

See `SKILL.md` for the full agent workflow.
