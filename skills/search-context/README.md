# GitHub Reference Context

Find, clone, inspect, and summarize high-quality GitHub reference repositories for coding agents.

## Install

```bash
# Codex
npx skills add instructa/agent-skills --skill search-context --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill search-context --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill search-context --agent cursor
```

## Use When

- The user asks for GitHub references, examples, prior art, inspiration, or implementation patterns.
- A coding agent needs curated repository context before implementation.
- The prompt includes `$search-context`.

## Requirements

- `gh`, authenticated with GitHub
- `git`
- `rg`
- Node.js 18 or newer

## Included Helper

Run from this skill directory:

```bash
node scripts/search-context.mjs check
node scripts/search-context.mjs run "React progress ring" --preset web-react --max-repos 5
```

## Tool Details

It is intentionally boring:

- no npm dependencies
- no MCP server required
- no third-party search index required
- uses `gh`, `git`, `rg`, and `node`

## Local prerequisites

```bash
gh auth status
git --version
rg --version
node --version
```

Then:

```bash
node scripts/search-context.mjs check
```

## Usage

From the skill folder:

```bash
node scripts/search-context.mjs run "visual progress indicator ring for ios app latest 2026" \
  --preset ios-swift \
  --max-repos 5
```

This creates:

```text
<user-cache>/github-reference-context/runs/<timestamp>/reference-context.md
<user-cache>/github-reference-context/runs/<timestamp>/reference-context.json
<user-cache>/github-reference-context/refs/<owner>__<repo>/
```

The default cache root is OS-native:

```text
macOS:   ~/Library/Caches/github-reference-context/
Linux:   $XDG_CACHE_HOME/github-reference-context/ or ~/.cache/github-reference-context/
Windows: %LOCALAPPDATA%\github-reference-context\
```

Use `--project-local` only when you intentionally want `.refs/` and `.context/` in the current directory. Inside a Git worktree those paths must be ignored, or the CLI refuses to write them.

## Optional CLI link

```bash
npm link
search-context check
search-context run "SwiftUI circular progress ring" --preset ios-swift
```

## Commands

```bash
search-context check
search-context run <query> [options]
search-context library add <path> [options]
search-context library list [options]
search-context library search <query> [options]
search-context clean [options]
```

## Run options

```text
--preset <id>          ios-swift, web-react, generic
--sources <list>       github, library, or library,github; default github
--use-library          shorthand for --sources library,github
--project <id>         use a named library cluster; use current for this worktree
--max-repos <n>        number of repos to clone and inspect, default 5
--candidates <n>       number of candidate repos to fetch per search phrase, default 12
--library-candidates <n> local library candidates to inspect, default max repos
--min-stars <n>        minimum stars, default 5
--fresh <yyyy-mm-dd>   pushed-after filter, default is Jan 1 two years ago
--cache-dir <path>     cache root, default OS user cache
--refs-dir <path>      where repos are cloned, default <cache>/refs
--output <path>        markdown manifest output, default <cache>/runs/<timestamp>/reference-context.md
--project-local        use .refs and .context in the current directory
--allow-unignored-worktree  allow writes inside a git worktree even if not ignored
--ssh                  clone using SSH URL instead of HTTPS URL
--include-forks        include forks
--include-archived     include archived repos
--include-private      do not add is:public to GitHub search
--refresh              refresh existing cached repos
--dry-run              search and rank, but do not clone
--json                 print the JSON summary to stdout
--verbose              print commands and scoring details
```

## Local reference library

Register existing third-party folders without cloning them again:

```bash
search-context library add ../third-party/some-repo \
  --tags react,ui \
  --presets web-react \
  --project current
```

Then search the local library:

```bash
search-context library search "ProgressRing"
```

Or mix registered folders with fresh GitHub discovery:

```bash
search-context run "React progress ring" --sources library,github --project current
```

The registry lives in the user cache at `<cache>/library/repositories.json`. Project clustering is stored in the same file under `projects`; use `--project current` to associate references with the current Git worktree or directory.

## Security posture

The script never installs dependencies, never runs cloned project code, and never executes package scripts. It only runs `gh`, `git`, and `rg`.

Reference repos are untrusted input. Use them to study patterns, not to copy blindly.

See `SKILL.md` for the full agent workflow.
