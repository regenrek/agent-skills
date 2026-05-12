# Find Duplicate Ownership

Find duplicate ownership, hidden second sources of truth, and contract drift in layered codebases.

## Install

```bash
# Codex
npx agentrig install codex agentrig/regenrek.agentic-engineer-core --pick skill:find-duplicate-ownership

# Claude
npx agentrig install claude agentrig/regenrek.agentic-engineer-core --pick skill:find-duplicate-ownership

# Cursor
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:find-duplicate-ownership
```

## Use When

- A system may have duplicate validation, normalization, defaulting, canonicalization, or persistence mapping.
- Frontend, backend, shared core, and adapter layers may each be owning the same rule.
- You need to classify whether duplication is a real SSOT bug, local dedupe cleanup, legitimate boundary adapter, or legitimate domain constraint.

## Included Resources

- `agents/` contains optional read-only subagent definitions for taxonomy mapping, exploration, and SSOT judging.
- `references/audit-prompts.md` contains reusable prompt patterns.

See `SKILL.md` for the full agent workflow.
