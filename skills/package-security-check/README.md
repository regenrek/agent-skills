# Package Security Check

Run a JavaScript supply-chain security baseline with pnpm-first hardening, release-age gating, lifecycle-script controls, CI checks, and optional incident IOC profiles.

## Install

```bash
# Codex
npx agentrig skill install codex agentrig/regenrek.package-security-check

# Claude
npx agentrig skill install claude agentrig/regenrek.package-security-check

# Cursor
npx agentrig skill install cursor agentrig/regenrek.package-security-check
```

## Use When

- A JavaScript, TypeScript, Node, Bun, or pnpm repo needs package supply-chain review.
- You need a traffic-light analysis before installs or lockfile changes.
- A current npm incident needs IOC profile scanning.
- The repo needs hardened package manager and CI install policy.

## Included Scanner

Run from this skill directory:

```bash
python3 scripts/check_js_supply_chain.py --root <repo-or-workspace-root>
python3 scripts/check_js_supply_chain.py --root <repo-or-workspace-root> --strict
```

For incident-specific checks:

```bash
python3 scripts/check_js_supply_chain.py \
  --root <repo-or-workspace-root> \
  --ioc data/iocs/mini-shai-hulud-2026-05.json
```

## Policy Notes

- Prefer pnpm 11 or newer as the canonical baseline.
- Do not run installs, updates, publishes, or lockfile rewrites before reporting the read-only findings and getting approval.
- Stop normal package work if IOC hits appear.

See `SKILL.md` for the full agent workflow.
