# Find Duplicate Ownership

Find duplicate ownership, hidden second sources of truth, and contract drift in layered codebases.

## Install

```bash
# Codex
npx skills add instructa/agent-skills --skill find-duplicate-ownership --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill find-duplicate-ownership --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill find-duplicate-ownership --agent cursor
```

## Use When

- A system may have duplicate validation, normalization, defaulting, canonicalization, or persistence mapping.
- Frontend, backend, shared core, and adapter layers may each be owning the same rule.
- You need to classify whether duplication is a real SSOT bug, local dedupe cleanup, legitimate boundary adapter, or legitimate domain constraint.

## Included Resources

- `agents/` contains optional read-only subagent definitions for taxonomy mapping, exploration, and SSOT judging.
- `references/audit-prompts.md` contains reusable prompt patterns.

See `SKILL.md` for the full agent workflow.
