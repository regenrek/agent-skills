# Architecture Ownership

Determine runtime owner, first-fix layer, and canonical long-term owner in layered codebases.

## Install

```bash
# Codex
npx agentrig install codex agentrig/regenrek.agentic-engineer-core --pick skill:architecture-ownership

# Claude
npx agentrig install claude agentrig/regenrek.agentic-engineer-core --pick skill:architecture-ownership

# Cursor
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:architecture-ownership
```

## Use When

- You need to decide where code or behavior should live.
- A bug appears in one layer but may be owned by another layer long term.
- Duplicate policy paths need to be removed after identifying one canonical owner.

## Output Contract

The agent should explicitly separate:

- Runtime owner
- First fix owner
- Canonical long-term owner
- Competing owners that are wrong
- Cleanup direction

See `SKILL.md` for the full agent workflow.
