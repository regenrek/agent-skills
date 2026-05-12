# Stage Review

Stage a finished feature, run local verification, create a Conventional Commit, then send it through the `no-mistakes` gated review and fix loop.

## Install

```bash
# Codex
npx agentrig skill install codex agentrig/regenrek.stage-review

# Claude
npx agentrig skill install claude agentrig/regenrek.stage-review

# Cursor
npx agentrig skill install cursor agentrig/regenrek.stage-review
```

## Required Companion

This workflow depends on the `no-mistakes` gate. Install the companion skill too:

```bash
# Codex
npx agentrig skill install codex agentrig/regenrek.no-mistakes

# Claude
npx agentrig skill install claude agentrig/regenrek.no-mistakes

# Cursor
npx agentrig skill install cursor agentrig/regenrek.no-mistakes
```

The target repo also needs the `no-mistakes` CLI and a `no-mistakes` remote before the final gated push can run.

## Use When

- The user says a feature is done and wants a professional pre-push review flow.
- You need to inspect changes, run local checks, stage explicit files, and create a Conventional Commit.
- The real upstream push or PR should happen only after the `no-mistakes` gate passes.

## Included Helper

Plan or create the local commit with the bundled script:

```bash
python3 scripts/stage_review.py --cwd . plan
python3 scripts/stage_review.py --cwd . commit -m "feat(scope): summary" path/to/file
```

See `SKILL.md` for the full agent workflow.
