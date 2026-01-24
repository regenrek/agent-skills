---
name: codex-analysis
description: Run Codex CLI for deep code analysis and second-opinion reviews. Use when the user explicitly asks for Codex analysis, Codex help, or wants a second opinion from Codex on code, architecture, or debugging questions.
---

# Codex Analysis

Run the Codex CLI to get deep analysis using gpt-5.2-codex with high reasoning effort. This model can spawn subagents for parallel exploration.

## When to Use

- User asks for "Codex analysis" or "Codex help"
- User wants a second opinion on code or architecture
- User needs deep reasoning on a complex problem

## Running the Analysis

Execute this command, replacing `{PROMPT}` with the user's question or analysis request:

```bash
codex exec -m gpt-5.2-codex \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --skip-git-repo-check \
  "{PROMPT}"
```

## Command Parameters

| Flag | Purpose |
|------|---------|
| `-m gpt-5.2-codex` | Use gpt-5.2-codex model (default worker model, can spawn subagents) |
| `--config model_reasoning_effort="high"` | Maximum reasoning depth |
| `--sandbox read-only` | Safe read-only sandbox |
| `--skip-git-repo-check` | Skip git repository validation |

## Subagent Spawning

For complex analysis tasks, include "spawn subagents" in your prompt to enable parallel exploration:

```bash
codex exec -m gpt-5.2-codex \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --skip-git-repo-check \
  "Analyze {topic}. Spawn subagents to explore different areas in parallel."
```

## After Running

1. **Summarize** the Codex analysis output
2. **Highlight** key suggestions and findings
3. **Ask** if the user wants to:
   - Implement any suggested changes
   - Get more details on specific points
   - Run additional analysis

## Example Usage

User asks: "Use Codex to analyze the authentication flow"

Run:
```bash
codex exec -m gpt-5.2-codex \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --skip-git-repo-check \
  "Analyze the authentication flow in this codebase. Spawn subagents to explore security issues, improvement opportunities, and best practices in parallel."
```

Then summarize findings and offer follow-up actions.
