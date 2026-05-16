# Consolidate Test Suites

Decide where bug-fix coverage belongs and keep each invariant in one owning test layer.

## Install

```bash
# Codex
npx agentrig install codex agentrig/regenrek.agentic-engineer-core --pick skill:consolidate-test-suites

# Claude
npx agentrig install claude agentrig/regenrek.agentic-engineer-core --pick skill:consolidate-test-suites

# Cursor
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:consolidate-test-suites
```

## Use When

- A bug fix or architectural change needs test coverage.
- You need to choose between unit, integration, and end-to-end ownership.
- Existing tests overlap and weaker duplicates should be merged or removed.

## Core Rule

Identify the invariant first, then place it in the lowest test layer that truly owns and proves that rule. Prefer existing canonical suites and existing files.

See `SKILL.md` for the full agent workflow.
