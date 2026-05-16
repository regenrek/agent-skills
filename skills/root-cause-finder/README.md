# Root Cause Finder

Trace expected behavior to the first unintended side effect before changing contracts, parsing, schemas, or types.

## Install

```bash
# Codex
npx skills add instructa/agent-skills --skill root-cause-finder --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill root-cause-finder --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill root-cause-finder --agent cursor
```

## Use When

- Debugging protocol errors, deserialization failures, null payloads, missing fields, restore issues, or hydration bugs.
- A downstream error may only be a symptom of an unintended request, mutation, restore, retry, observer, or background write.
- Reviewing code where a visible failure might hide an upstream state ownership bug.

## Core Rule

Before fixing the error, prove whether the code path that produced it was intended.

See `SKILL.md` for the full agent workflow.
