---
name: git-new-worktree
description: Create a new git worktree and branch using the local `git new` command. Use when asked to create a worktree from a name, set upstream via git new, cd into the new directory, and summarize what was created.
---

# Git New Worktree

## Overview
Create a new branch via `git new`, add a worktree under `<project>-wt/<name>`, and cd into the new directory.

## Quick start
- Run: `source scripts/git-new-worktree.sh <name>`
- If not sourced, it will still work but the cwd change won’t persist.

## Output
- Base branch or detached ref
- New branch name
- Worktree path (`<repo-parent>/<project>-wt/<name>`)
- Upstream (if set by `git new`)
