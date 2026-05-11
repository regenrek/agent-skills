---
name: pr-commiter
description: Agentic PR committer with deterministic commits, enforced branch/PR workflow, and explicit paths (no git add .).
---

# PR Committer

Use bundled script `scripts/pr-commiter` for a deterministic commit that enforces branches and PR creation.

## Flow

1) Preflight
- `git status --porcelain=v1 -b`
- `git branch --show-current`
- If merge/rebase/cherry-pick in progress, stop.
- If on protected branch, the script will create a new branch automatically.

2) Pick files
- Use explicit paths only. Never use `.`.
- If unsure, list candidates from `git status` and ask for selection.

3) Run commit script
- `./scripts/pr-commiter commit -m "type(scope): summary" -- path/to/file1 path/to/file2`
- If you need a dry run: `./scripts/pr-commiter plan -m "type(scope): summary" -- path/to/file1`
- If PR should be skipped: add `--no-pr`
- If PR creation needs push: add `--push` (explicit consent)

## Flags
- `--reset-staged` clear existing staged changes before staging listed paths
- `--no-pr` skip PR creation
- `--push` push branch before creating PR
- `--force-lock` remove stale `.git/index.lock` and retry
- `--json` machine-readable output
- `--dry-run` validate + plan only

## Behavior
- Stages only provided paths.
- Refuses merge/rebase/cherry-pick in progress.
- Creates a new branch if current is protected or detached.
- Refuses if staged changes exist unless `--reset-staged`.
- Fails if nothing staged for provided paths.
- Creates PR via `gh` unless `--no-pr`. Requires `--push` if no upstream.
- Uses `.committerrc` for policy.

## Errors
- Quote exact error text back to user.
- Ask for next action if blocked.

## Optional verification
- `git show --stat --oneline HEAD`
- `git status --porcelain=v1 -b`
- `gh pr view --json url --jq '.url'`
