# Shellck

Run ShellCheck on shell scripts after editing scripts or when debugging shell errors.

## Install

```bash
# Codex
npx agentrig skill install codex agentrig/regenrek.shellck

# Claude
npx agentrig skill install claude agentrig/regenrek.shellck

# Cursor
npx agentrig skill install cursor agentrig/regenrek.shellck
```

## Use When

- You edited shell scripts and need a lint pass.
- A shell script fails due to quoting, `set -u`, subshell, globbing, or portability issues.
- A repo has many scripts and you want a consistent filtering pass.

## Requirements

- `shellcheck`

## Included Helper

Run from the target repository:

```bash
scripts/run_shellck.sh
scripts/run_shellck.sh scripts/ other/script.sh
```

See `SKILL.md` for the full agent workflow.
