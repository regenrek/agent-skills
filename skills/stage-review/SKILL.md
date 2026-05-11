---
name: stage-review
description: Stage a finished local feature, run local verification, create a Conventional Commit, then send it through the no-mistakes gated review/fix loop before real upstream push/PR. Use when the user says a feature is done, asks for a professional stage-review flow, wants Codex to git add and commit safely, or wants no-mistakes review/verify/fix before pushing to origin.
---

# Stage Review

## Overview

Use this as the finished-feature workflow: inspect changes, verify locally, stage explicit files, create a Conventional Commit, push through `no-mistakes`, attach to the run, fix findings, rerun, and let no-mistakes perform the real upstream push/PR only after the gate passes.

## Core Rules

- Never use `git push origin` in this workflow.
- Never force-push.
- Do not stage with `git add .`; use explicit paths or the bundled script's `--all` only after the user explicitly wants all current changes included.
- Stop before committing on protected or detached branches.
- Ask before any remote-affecting command, including `git push no-mistakes`.
- Use Conventional Commits: `feat|fix|refactor|build|ci|chore|docs|style|perf|test`.
- Prefer repo-local check commands from `.no-mistakes.yaml`, `justfile`, `package.json`, `Makefile`, `go.mod`, `Cargo.toml`, or equivalent project config.
- Quote exact local check and pipeline errors before diagnosing.

## Workflow

### 1. Preflight

Resolve `scripts/stage_review.py` relative to this skill folder, then run:

```sh
python3 <skill-dir>/scripts/stage_review.py --cwd . plan
python <skill-dir>/scripts/stage_review.py --cwd . plan
```

Also run:

```sh
git status --short --branch
git diff --stat
```

Stop and ask if:

- branch is protected or detached
- merge/rebase/cherry-pick is in progress
- changed files include unrelated work
- no `origin` exists
- no `no-mistakes` remote exists and `no-mistakes init` has not been approved

### 2. Local Checks

Run the repo's real local checks before staging. Prefer explicit commands from `.no-mistakes.yaml`:

```yaml
commands:
  test: "..."
  lint: "..."
  format: "..."
```

If no config exists, inspect repo-local command surfaces and choose the canonical one. Examples:

- `just test`, `just lint`, `just fmt`
- `make test`, `make lint`, `make fmt`
- `pnpm test`, `pnpm lint`, `pnpm typecheck`
- `go test ./...`, `go vet ./...`
- `cargo test`, `cargo clippy --all-targets -- -D warnings`

Do not commit if relevant local checks fail unless the user explicitly wants a broken checkpoint.

### 3. Stage And Commit

Pick the Conventional Commit subject from the actual diff:

```text
feat(scope): concise summary
fix(scope): concise summary
refactor(scope): concise summary
```

Stage explicit files:

```sh
python3 <skill-dir>/scripts/stage_review.py --cwd . commit \
  -m "feat(scope): concise summary" \
  --body "Tests: <commands run>" \
  path/to/file1 path/to/file2
```

Use all changed files only when the user explicitly confirms all changes belong in the feature:

```sh
python3 <skill-dir>/scripts/stage_review.py --cwd . commit \
  -m "feat(scope): concise summary" \
  --body "Tests: <commands run>" \
  --all
```

### 4. Push Through no-mistakes

Confirm the exact command first:

```text
Ready to push <branch> through no-mistakes:
git push no-mistakes <branch>
```

After confirmation:

```sh
git push no-mistakes <branch>
no-mistakes
```

### 5. Review/Verify/Fix Loop

For each no-mistakes finding:

- identify the step: `rebase`, `review`, `test`, `document`, `lint`, `push`, `pr`, or `ci`
- quote the exact finding/error
- fix code/config only when the user wants you to fix it
- run targeted local verification after fixing
- commit follow-up fixes with the same script
- run `no-mistakes rerun` or continue/attach as appropriate

Useful commands:

```sh
no-mistakes status
no-mistakes runs --limit 10
no-mistakes attach
no-mistakes rerun
```

### 6. Done Criteria

Finish only when you can report:

- local checks run and result
- commit SHA and Conventional Commit subject
- no-mistakes run state
- PR URL if created/updated
- CI state if available
- remaining blockers, if any
