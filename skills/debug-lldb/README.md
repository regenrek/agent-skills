# Debug LLDB

Capture and analyze thread backtraces to debug hangs, deadlocks, UI freezes, IPC stalls, and high-CPU loops.

## Install

```bash
# Codex
npx skills add instructa/agent-skills --skill debug-lldb --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill debug-lldb --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill debug-lldb --agent cursor
```

## Use When

- An app becomes unresponsive or switching contexts stalls.
- You need to distinguish deadlock, blocking I/O, blocked IPC, and busy-loop behavior.
- A normal log or stack trace is not enough because the process is still running.

## Requirements

- macOS: `lldb`
- Linux: `gdb`
- Windows: WinDbg or `cdb`

## Included Helpers

- `scripts/collect_stacks.sh` captures repeated stack samples by PID or process name.
- `references/triage.md` explains common hang signatures.

See `SKILL.md` for the full agent workflow.
