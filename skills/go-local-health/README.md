# Go Local Health

Run repeatable local Go test, coverage, and lint checks for repositories that contain `go.mod`.

## Install

```bash
# Codex
npx agentrig skill install codex agentrig/regenrek.go-local-health

# Claude
npx agentrig skill install claude agentrig/regenrek.go-local-health

# Cursor
npx agentrig skill install cursor agentrig/regenrek.go-local-health
```

## Use When

- The repo is a Go project and the user wants local health checks.
- You need a fast test, coverage, and lint snapshot.
- You need an interactive Go test loop or coverage exploration and the user explicitly wants that mode.

## Requirements

- Quick snapshot: `go`, `tparse`, and `golangci-lint`
- Interactive test loop: `lazygotest`
- Coverage explorer: `gocovsh`

Ask before installing missing tools unless the repo pins versions.

## Included Helper

```bash
scripts/go-local-health --scope ./...
```

See `SKILL.md` for the full agent workflow.
