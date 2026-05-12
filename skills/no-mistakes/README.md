# No Mistakes

Use the `no-mistakes` gated push workflow for finished feature branches.

## Install

```bash
# Codex
npx agentrig skill install codex agentrig/regenrek.no-mistakes

# Claude
npx agentrig skill install claude agentrig/regenrek.no-mistakes

# Cursor
npx agentrig skill install cursor agentrig/regenrek.no-mistakes
```

## Use When

- The user wants to inspect, initialize, or use a `no-mistakes` gate.
- A finished branch should be pushed through `git push no-mistakes <branch>` instead of directly to origin.
- You need to attach to runs, interpret findings, fix pipeline issues, rerun, or check `no-mistakes doctor`.

## Requirements

- `git`
- The `no-mistakes` CLI
- At least one supported agent binary, such as `codex`, `claude`, `opencode`, `acli`, `pi`, or an ACP target through `acpx`
- For PR/CI steps: `gh` for GitHub, `glab` for GitLab, or Bitbucket Cloud credentials

## Included Helper

The readiness check is read-only:

```bash
python3 scripts/check_no_mistakes.py --cwd .
python3 scripts/check_no_mistakes.py --cwd . --json
```

## Missing CLI

Install the `no-mistakes` CLI only when it is missing or broken:

```bash
command -v no-mistakes
no-mistakes --version
no-mistakes doctor
```

See `SKILL.md` for install fallbacks, gate setup, configuration examples, and the full agent workflow.
