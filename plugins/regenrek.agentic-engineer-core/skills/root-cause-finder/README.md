# Root Cause Finder

Trace expected behavior to the first unintended side effect before changing contracts, parsing, schemas, or types.

## Install

```bash
# Codex
npx agentrig install codex agentrig/regenrek.agentic-engineer-core --pick skill:root-cause-finder

# Claude
npx agentrig install claude agentrig/regenrek.agentic-engineer-core --pick skill:root-cause-finder

# Cursor
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:root-cause-finder
```

## Use When

- Debugging protocol errors, deserialization failures, null payloads, missing fields, restore issues, or hydration bugs.
- A downstream error may only be a symptom of an unintended request, mutation, restore, retry, observer, or background write.
- Reviewing code where a visible failure might hide an upstream state ownership bug.

## Core Rule

Before fixing the error, prove whether the code path that produced it was intended.

See `SKILL.md` for the full agent workflow.
