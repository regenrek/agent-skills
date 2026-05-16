# Consolidate Test Suites

Decide where bug-fix coverage belongs and keep each invariant in one owning test layer.

## Install

```bash
# Codex
npx skills add instructa/agent-skills --skill consolidate-test-suites --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill consolidate-test-suites --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill consolidate-test-suites --agent cursor
```

## Use When

- A bug fix or architectural change needs test coverage.
- You need to choose between unit, integration, and end-to-end ownership.
- Existing tests overlap and weaker duplicates should be merged or removed.

## Core Rule

Identify the invariant first, then place it in the lowest test layer that truly owns and proves that rule. Prefer existing canonical suites and existing files.

See `SKILL.md` for the full agent workflow.
