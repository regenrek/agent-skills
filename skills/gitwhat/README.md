# Gitwhat

Print a compact git workspace snapshot for the current directory.

## Install

```bash
# Codex
npx skills add instructa/agent-skills --skill gitwhat --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill gitwhat --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill gitwhat --agent cursor
```

## Use When

- The user asks what branch or repo they are in.
- You need a quick current working directory, repo root, branch, dirty status, or worktree summary.
- You want to inspect sibling worktrees without mutating anything.

## Included Helper

Run from the target repository:

```bash
scripts/gitwhat.sh
```

The script reports cwd, branch or detached SHA, repo root, worktree status, dirty counts, and sibling worktree state.

See `SKILL.md` for the full agent workflow.
