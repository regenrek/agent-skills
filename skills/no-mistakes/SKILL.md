---
name: no-mistakes
description: Use the no-mistakes gated push workflow in Git repositories. Use when the user wants to check no-mistakes readiness, initialize or inspect a gate, configure .no-mistakes.yaml, push through the no-mistakes remote, attach to runs, interpret/fix pipeline findings, rerun status/runs/doctor, or use no-mistakes with Codex/Claude/OpenCode/Pi/ACP agents. Install guidance is secondary and only for missing or broken no-mistakes binaries.
---

# No Mistakes

## Overview

Use `no-mistakes` as the repo's finished-feature workflow: inspect readiness, verify the local branch, push through the `no-mistakes` remote when approved, attach to the run, and help the user react to pipeline findings until PR/CI is ready.

## Guardrails

- Treat `git push no-mistakes`, bare `no-mistakes -y`, and CI auto-fix runs as remote-affecting operations. Ask before running them unless the user explicitly requested a push/PR flow.
- Prefer explicit repo commands in `.no-mistakes.yaml` over agent auto-detection for repeatable gates.
- Use bundled scripts with a generic Python runner (`python3` first, then `python`) and no external dependencies.
- Run commands from the target Git repo root when initializing, configuring, or checking status.
- Use `command -v` and `no-mistakes doctor` for prerequisites. Avoid hard-coded local binary paths in reusable instructions.
- Treat install commands as a fallback only when `no-mistakes` is missing or broken.

## Deterministic Check

Start with the bundled health check when inspecting an existing repo. Resolve `scripts/check_no_mistakes.py` relative to this skill folder, then run it with whichever Python command exists:

```sh
python3 <skill-dir>/scripts/check_no_mistakes.py --cwd .
python <skill-dir>/scripts/check_no_mistakes.py --cwd .
```

Use `--json` when you need machine-readable output:

```sh
python3 <skill-dir>/scripts/check_no_mistakes.py --cwd . --json
```

The script is read-only and standard-library only. It checks `git`, `no-mistakes`, provider CLIs, supported agent binaries, `origin` and `no-mistakes` remotes, `.no-mistakes.yaml`, and `no-mistakes doctor`.

## Finished Feature Workflow

Use this flow when the user says the feature is done and would normally run `git push`.

### 1. Inspect readiness

Run the deterministic check from the repo root:

```sh
python3 <skill-dir>/scripts/check_no_mistakes.py --cwd .
```

If `python3` is unavailable, use:

```sh
python <skill-dir>/scripts/check_no_mistakes.py --cwd .
```

Then inspect Git state:

```sh
git status --short --branch
git branch --show-current
git remote -v
no-mistakes status
no-mistakes runs --limit 10
```

Stop and ask before continuing if:

- the branch is dirty and the user did not ask you to commit
- the current branch is `main`, `master`, `develop`, or another protected base branch
- `origin` is missing
- the `no-mistakes` remote is missing and `no-mistakes init` has not been approved
- `no-mistakes doctor` reports a hard failure

### 2. Confirm the intended push

Before any remote-affecting command, state the exact branch and command:

```text
Ready to push <branch> through no-mistakes with:
git push no-mistakes <branch>
```

Ask for confirmation unless the user already explicitly requested the no-mistakes push.

### 3. Push through the gate

Run:

```sh
git push no-mistakes <branch>
```

Do not use `git push origin` in this workflow.

### 4. Attach and drive the run

Open or attach to the active run:

```sh
no-mistakes
```

If the run is not active or you need a specific run:

```sh
no-mistakes attach
```

### 5. Handle findings

For each blocking finding:

- summarize the exact step (`rebase`, `review`, `test`, `document`, `lint`, `push`, `pr`, or `ci`)
- quote the important error/finding text
- decide whether it is user-decision, code-fix, config-fix, or external-service failure
- implement code/config fixes only when the user asked you to fix
- rerun or continue the no-mistakes flow after fixes

If the run needs another attempt:

```sh
no-mistakes rerun
```

### 6. Report outcome

End with:

- branch pushed or not pushed
- PR URL if no-mistakes created/updated one
- CI state if available
- remaining blockers, if any

## Bypass And Wizard

Use skip only for an explicitly accepted one-off bypass:

```sh
no-mistakes --skip test,lint
git push -o no-mistakes.skip=test,lint no-mistakes <branch>
```

Use the wizard for uncommitted work only when the user wants no-mistakes to guide branch/commit/push:

```sh
no-mistakes
no-mistakes -y
```

## Missing Binary

First check whether it is already available:

```sh
command -v no-mistakes
no-mistakes --version
```

If it is missing or broken, choose one install path:

```sh
# macOS/Linux release binary; installs/restarts daemon
curl -fsSL https://raw.githubusercontent.com/kunchenguid/no-mistakes/main/docs/install.sh | sh

# Go install; telemetry off by default unless configured at runtime
go install github.com/kunchenguid/no-mistakes/cmd/no-mistakes@latest

# Source checkout
make build
make install
```

After install:

```sh
no-mistakes doctor
```

Required: `git` and at least one supported agent binary (`claude`, `codex`, `opencode`, `acli` for Rovo Dev, `pi`) or `acpx` for an ACP target. For PR/CI steps, GitHub uses `gh`, GitLab uses `glab`, and Bitbucket Cloud uses `NO_MISTAKES_BITBUCKET_EMAIL` plus `NO_MISTAKES_BITBUCKET_API_TOKEN`.

## Repo Setup

Initialize a repo that already has an `origin` remote:

```sh
git remote -v
no-mistakes init
```

This adds a local `no-mistakes` remote and creates gate state under `~/.no-mistakes` unless `NM_HOME` is set. It does not remove `origin`.

Remove a gate from the current repo:

```sh
no-mistakes eject
```

## Configure

Prefer a repo-level `.no-mistakes.yaml` with explicit commands:

```yaml
agent: codex

commands:
  test: "go test -race ./..."
  lint: "go vet ./..."
  format: "gofmt -w ."

ignore_patterns:
  - "*.generated.go"
  - "vendor/**"

auto_fix:
  rebase: 3
  review: 0
  test: 3
  document: 3
  lint: 3
  ci: 3
```

Adjust commands to the repo's real test/lint/format entrypoints. If commands are omitted, the selected agent tries to detect checks.

Use global config for machine-local agent paths or flags:

```yaml
# ~/.no-mistakes/config.yaml
agent: auto

agent_path_override:
  codex: /absolute/path/to/codex
```

Do not put machine-local paths, approval modes, or personal model choices into `.no-mistakes.yaml` unless the repo intentionally owns that policy.

## Pipeline Mental Model

The pipeline order is:

```text
intent -> rebase -> review -> test -> document -> lint -> push -> pr -> ci
```

Key distinctions:

- Local deterministic checks come from `commands.test`, `commands.lint`, and `commands.format`.
- AI judgment covers diff review, missing-doc checks, auto-fix attempts, and check detection when commands are absent.
- Remote CI still belongs to the Git provider; no-mistakes watches it and can ask the agent to fix failed jobs.

## Troubleshooting

- If `doctor` cannot find an agent, check `PATH` first, then set `agent_path_override` in `~/.no-mistakes/config.yaml`.
- If the daemon misses environment variables, put them in shell startup files loaded by a login shell, then restart the daemon.
- If PR or CI steps skip, verify `gh`/`glab` authentication or Bitbucket env vars.
- If tests are flaky because optional CLIs exist on the machine, rerun with a scoped `PATH` and report the exact command and failure.
- If the user asks what "clean" means, explain it as "the branch passed the configured local and remote gates"; do not imply perfection.
