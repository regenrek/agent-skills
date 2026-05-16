# Architecture Ownership

Determine runtime owner, first-fix layer, and canonical long-term owner in layered codebases.

## Install

```bash
# Codex
npx skills add instructa/agent-skills --skill architecture-ownership --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill architecture-ownership --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill architecture-ownership --agent cursor
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
