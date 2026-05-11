---
name: codex-sandbox
description: Create and manage per-task isolated git clones (sandboxes) for Codex CLI sessions, with automatic branch creation and safety hooks that block committing/pushing on main/master. Use when running multiple Codex sessions or parallel tasks and you want to avoid git worktree friction, cwd/branch mixups, or environment collisions.
---

# Codex Sandboxes

Create one directory per task and run the agent inside that directory. Prefer this over git worktrees when:

- Codex or other agents sometimes use the wrong current working directory.
- You want full isolation for .env, node_modules, build outputs, ports, and dev servers.
- You want a simple mental model: one task equals one folder equals one branch.

This skill bundles a small Python CLI plus a Bash wrapper:

- `scripts/codex_sandbox.py` (primary)
- `scripts/codex-task` (convenience)

## Locate the skill directory

Run the scripts from the skill folder, depending on where you installed it:

- Repo-scoped: `$REPO_ROOT/.codex/skills/codex-sandboxes`
- User-scoped: `$CODEX_HOME/skills/codex-sandboxes` (macOS/Linux default: `~/.codex/skills/codex-sandboxes`)

Use `git rev-parse --show-toplevel` to get `$REPO_ROOT`.

## Quick start (agent-only)

This skill is always invoked by an agent. Do not run it manually.

Example command the agent should run:

```bash
SKILL_DIR="$(git rev-parse --show-toplevel)/.codex/skills/codex-sandboxes"
python3 "$SKILL_DIR/scripts/codex_sandbox.py" new fix-123
```

The command will:

1. Detect the repo remote (default: `origin`).
2. Create or update a local bare mirror.
3. Clone a sandbox directory under a base directory.
4. Create/switch to a task branch from `origin/main`.
5. Set upstream tracking to `origin/<branch>` (pushes once if needed).
6. Install safety hooks that block commit/push on `main`/`master`.

## How to instruct the agent

Always request this via the agent. Provide:

- Task name (used for sandbox + branch name).
- Any non-default base directory (e.g. `--base-dir ~/projects`).
- Any non-default base branch or remote.

If you do not provide extra details, the agent should use defaults. If the task name is ambiguous or missing, the agent should ask back.

Example prompt to the agent:

```
Use codex-sandbox to create a sandbox for task "fix-123".
Place it under ~/projects, base branch main.
Command: python3 <skill_dir>/scripts/codex_sandbox.py new fix-123 --base-dir ~/projects --base-branch main
```

## Concepts

Use these terms consistently in prompts and logs:

- **Workset**: Logical grouping for a ticket/feature (optional label only).
- **Sandbox**: One clone directory used by one writing agent.
- **Session**: One Codex process running in one sandbox.

Prefer: one writing session per sandbox.

## Create a sandbox

```bash
python3 <skill_dir>/scripts/codex_sandbox.py new <task> [options]
```

Common patterns:

```bash
# Create sandbox + branch and print its path
python3 <skill_dir>/scripts/codex_sandbox.py new feat-auth

# Use a different base branch
python3 <skill_dir>/scripts/codex_sandbox.py new fix-123 --base-branch develop

# Copy .env.example to .env on creation
python3 <skill_dir>/scripts/codex_sandbox.py new feat-auth --env-copy
```

Key options:

- `--base-dir DIR`: Where to place sandboxes (default: `~/wip`).
- `--bare-dir DIR`: Where to keep the bare mirror (default: `~/.cache/codex-sandboxes/<repo>.git`).
- `--remote NAME`: Which remote to use (default: `origin`).
- `--remote-url URL`: Override remote URL discovery.
- `--base-branch NAME`: Base branch to branch from (default: `main`).
- `--branch NAME`: Explicit branch name (default: derived from `<task>`).
- `--env-copy`: Copy `.env.example` to `.env` if present and `.env` missing.

## List, inspect, remove

```bash
python3 <skill_dir>/scripts/codex_sandbox.py list
python3 <skill_dir>/scripts/codex_sandbox.py path <task>
python3 <skill_dir>/scripts/codex_sandbox.py status <task>
python3 <skill_dir>/scripts/codex_sandbox.py rm <task>
```

## Safety rules

Follow these rules in every run:

- Never run a write-capable agent in the primary checkout.
- Always create a sandbox for a write task.
- Keep one writer per sandbox.
- Keep `main`/`master` protected on the remote (PR-only merges).

If the sandbox is currently on `main`/`master`, the tool will refuse to proceed unless you pass `--allow-main`.

## Multiple sessions

If you want multiple sessions for one workset, create multiple sandboxes:

```bash
python3 <skill_dir>/scripts/codex_sandbox.py new feat-auth-ui-1
python3 <skill_dir>/scripts/codex_sandbox.py new feat-auth-ui-2
python3 <skill_dir>/scripts/codex_sandbox.py new feat-auth-core-1
```

Avoid running two writing sessions in the same sandbox.

## Troubleshooting

- Remote URL detection failed: pass `--remote-url`.
- Sandbox already exists: choose a unique `<task>` name or remove with `rm`.
- You want deterministic naming: read `references/naming.md`.
