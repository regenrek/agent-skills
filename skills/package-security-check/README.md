# Package Security Check

Run a JavaScript supply-chain security baseline with pnpm-first hardening, release-age gating, lifecycle-script controls, CI checks, and optional incident IOC profiles.

## Install

Install with the open Agent Skills CLI:

```bash
# List skills in this repo
npx skills add instructa/agent-skills --list

# Codex
npx skills add instructa/agent-skills --skill package-security-check --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill package-security-check --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill package-security-check --agent cursor
```

Use `-g` for a global install, or omit it for a project-local install. Add `--copy` if you prefer copied files instead of symlinks.

Manual fallback with `giget`:

```bash
# Codex or Cursor project install
npx giget@latest gh:instructa/agent-skills/skills/package-security-check .agents/skills/package-security-check

# Claude Code project install
npx giget@latest gh:instructa/agent-skills/skills/package-security-check .claude/skills/package-security-check
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
  --ioc data/iocs/npm-supply-chain-2026-05.json
```

## Policy Notes

- Prefer pnpm 11 or newer as the canonical baseline.
- Do not run installs, updates, publishes, or lockfile rewrites before reporting the read-only findings and getting approval.
- Stop normal package work if IOC hits appear.

See `SKILL.md` for the full agent workflow.
