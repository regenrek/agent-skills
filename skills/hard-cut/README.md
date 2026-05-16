# Hard Cut

Keep one canonical implementation and delete compatibility, fallback, shim, coercion, and dual-shape code.

## Install

```bash
# Codex
npx skills add instructa/agent-skills --skill hard-cut --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill hard-cut --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill hard-cut --agent cursor
```

## Use When

- A pre-release or internal-draft refactor changes schemas, contracts, persisted state, routing, config, flags, enums, or architecture.
- Old-shape support would add fallback branches or compatibility code.
- The desired outcome is one final shape with obsolete code deleted.

## Exception Rule

Keep compatibility only for real external or persisted boundaries: user data, database state, wire formats, public contracts, or active outside dependencies. Name the exact boundary when an exception exists.

See `SKILL.md` for the full agent workflow.
