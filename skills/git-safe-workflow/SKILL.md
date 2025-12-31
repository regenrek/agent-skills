---
name: git-safe-workflow
description: Safely inspect, stage, commit, and (only if asked) push changes made by an AI agent. Use for commit/push requests, end-of-task checkpoints, merge conflict resolution, worktree safety checks, or deciding whether to use git commit --amend.
---

# Git Safe Workflow

## Core rules (always)

1. Collect repo context first (non-destructive):
   - git rev-parse --show-toplevel
   - git status --porcelain=v1 -b
   - git log -1 --oneline

2. Collect worktree context when relevant (also non-destructive):
   - git branch --show-current
   - git worktree list --porcelain

   Run worktree context when:
   - branch name is unexpected
   - you are in a nested folder and not sure which checkout you are in
   - Git refuses checkout because branch is already checked out elsewhere
   - status shows detached HEAD or unusual metadata

3. Never run destructive or high-risk commands unless explicitly requested:
   - Do NOT use:
     - git reset --hard
     - git clean -fd
     - git push --force or --force-with-lease
     - git worktree prune
     - git worktree remove
     - git rebase (interactive or not) unless explicitly requested
   - If the user requests one:
     - restate the exact command you plan to run
     - explain why it is risky
     - then proceed

4. Avoid interactive prompts and editors unless the user says it is OK:
   - Prefer non-interactive commands
   - Avoid:
     - git add -p
     - editor-based rebase
     - commit message editor prompts
   - Prefer:
     - git commit -m "..." -m "..."

## Worktree safety rules

1. Confirm you are in the intended worktree and branch before staging or committing:
   - git branch --show-current
   - git worktree list --porcelain

2. Detached HEAD safety:
   - If 'git branch --show-current' prints nothing, you are likely in detached HEAD.
   - Default behavior: do not commit immediately.
   - Explain the situation and ask whether to create a branch first, for example:
     - git switch -c <new-branch-name>
   - Only commit in detached HEAD if the user explicitly wants that and understands the risk.

3. Branch checked out in another worktree:
   - If Git refuses because the branch is already checked out elsewhere, do not use force by default.
   - Safe options:
     - switch that other worktree to a different branch, or
     - create a new branch for this worktree (recommended)

4. Worktree lifecycle operations:
   - Do not run these unless explicitly requested:
     - git worktree add
     - git worktree remove
     - git worktree move
     - git worktree lock or unlock
     - git worktree prune

## Make a checkpoint commit (default)

### 1) Summarize the change
- git diff --stat
- git diff --staged --stat (if anything is staged)

### 2) Inspect details when needed
- git diff
- git diff --staged

Guidance:
- Always inspect full diff if changes are large, touch security-sensitive code, or involve config or CI.

### 3) Stage changes safely
Prefer explicit paths when practical:
- git add path/to/file1 path/to/file2

Otherwise stage tracked modifications and deletions:
- git add -u

Avoid staging everything blindly unless user explicitly wants it:
- avoid: git add .

### 4) Commit message
Use Conventional Commits when reasonable:
- type(scope): summary

Include:
- what behavior changed
- tests run, or explicitly note: tests not run

### 5) Commit (non-interactive)
- git commit -m "type(scope): summary" -m "Details... Tests: <what ran or not run>"

### 6) Verify
- git status
- git show --stat --oneline HEAD

## Amend policy (git commit --amend)

### Default rule
- Do not use 'git commit --amend' unless it clearly improves the most recent commit AND the commit has not been pushed.

### Safe uses
Use amend when:
- You just made the last commit locally and immediately noticed:
  - you forgot a file
  - you need a tiny fix
  - the commit message is wrong

Common safe commands:
- Add changes then amend without changing message:
  - git commit --amend --no-edit
- Replace message non-interactively:
  - git commit --amend -m "type(scope): summary" -m "Details... Tests: ..."

### Avoid
Do not amend when:
- the commit is already pushed to a shared remote branch
- amending would require a force push to reconcile the remote

In that case:
- prefer a new follow-up commit
- only rewrite history if the user explicitly requests it and accepts the risk

## Merge conflicts

1. Collect context:
   - git status --porcelain=v1 -b

2. Identify conflicted files:
   - git diff --name-only --diff-filter=U

3. Resolve conflicts carefully (no automation that discards intent).
   - After resolving:
     - git add <resolved files>

4. Continue the operation:
   - If merge:
     - git commit -m "merge: resolve conflicts" -m "Details... Tests: ..."
   - If rebase was explicitly requested and is in progress:
     - git rebase --continue

5. Verify:
   - git status
   - git show --stat --oneline HEAD (if a commit was created)

## Push policy

- Only push if the user explicitly asks.
- Preferred push:
  - git push -u origin HEAD

### Main or master branch rule
- If currently on main or master, do not push directly by default.
- Create a branch first (ask user for branch name if not provided), then push that branch.

### Force push rule
- Never force push unless explicitly requested.
- If requested:
  - restate the exact force push command
  - explain risk (rewriting shared history)
  - then proceed
