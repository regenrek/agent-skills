# Hard Cut

Keep one canonical implementation and delete compatibility, fallback, shim, coercion, and dual-shape code.

## Install

```bash
# Codex
npx agentrig install codex agentrig/regenrek.agentic-engineer-core --pick skill:hard-cut

# Claude
npx agentrig install claude agentrig/regenrek.agentic-engineer-core --pick skill:hard-cut

# Cursor
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:hard-cut
```

## Use When

- A pre-release or internal-draft refactor changes schemas, contracts, persisted state, routing, config, flags, enums, or architecture.
- Old-shape support would add fallback branches or compatibility code.
- The desired outcome is one final shape with obsolete code deleted.

## Exception Rule

Keep compatibility only for real external or persisted boundaries: user data, database state, wire formats, public contracts, or active outside dependencies. Name the exact boundary when an exception exists.

See `SKILL.md` for the full agent workflow.
