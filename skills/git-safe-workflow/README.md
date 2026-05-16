# Git Safe Workflow

Safely inspect, stage, commit, and push only when explicitly requested, without destructive git operations.

## Install

```bash
# Codex
npx skills add instructa/agent-skills --skill git-safe-workflow --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill git-safe-workflow --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill git-safe-workflow --agent cursor
```

## Use When

- The user asks for a commit, push, checkpoint, or merge conflict resolution.
- You need to inspect branch, worktree, staged changes, and recent commit state safely.
- You need to decide whether amend, follow-up commit, or a normal commit is appropriate.

## Core Safety Rules

- Inspect repo state before staging or committing.
- Use explicit paths when staging.
- Do not use `git add .` unless the user explicitly confirms all changes belong.
- Do not run destructive commands such as `git reset --hard`, `git clean -fd`, or force push unless explicitly requested.
- Only push when the user asks.

See `SKILL.md` for the full agent workflow.
