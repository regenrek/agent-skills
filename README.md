# Agent Skills

A curated source repo for agent skills and plugin bundles.

This repo is organized around the open Agent Skills CLI (`npx skills`) instead of local sync scripts:

- `plugins/`: plugin manifests that bundle a set of top-level skills (AgentRig distribution is not ready yet — install bundled skills individually for now).
- `skills/`: all installable skills, both standalone and the ones referenced by a plugin bundle. Each can be listed and installed independently.
- `internal/`: personal or experimental workflows that are not part of the public install surface.

## Install

Use the open Agent Skills CLI. List everything in the repo, then install per skill:

```bash
# List skills in this repo
npx skills add instructa/agent-skills --list
```

Use `-g` for a global install, or omit it for a project-local install. Add `--copy` if you prefer copied files instead of symlinks.

<details>
<summary>Codex</summary>

Install bundled skills from `regenrek.agentic-engineer-core`:

```bash
npx skills add instructa/agent-skills --skill architecture-ownership --agent codex
npx skills add instructa/agent-skills --skill consolidate-test-suites --agent codex
npx skills add instructa/agent-skills --skill find-duplicate-ownership --agent codex
npx skills add instructa/agent-skills --skill hard-cut --agent codex
npx skills add instructa/agent-skills --skill root-cause-finder --agent codex
npx skills add instructa/agent-skills --skill search-context --agent codex
```

Install one standalone skill:

```bash
npx skills add instructa/agent-skills --skill app-spec-packager --agent codex
npx skills add instructa/agent-skills --skill debug-lldb --agent codex
npx skills add instructa/agent-skills --skill gh-repo-bootstrap --agent codex
npx skills add instructa/agent-skills --skill git-safe-workflow --agent codex
npx skills add instructa/agent-skills --skill gitwhat --agent codex
npx skills add instructa/agent-skills --skill go-local-health --agent codex
npx skills add instructa/agent-skills --skill homebrew-publish --agent codex
npx skills add instructa/agent-skills --skill no-mistakes --agent codex
npx skills add instructa/agent-skills --skill package-security-check --agent codex
npx skills add instructa/agent-skills --skill redesign-my-landingpage --agent codex
npx skills add instructa/agent-skills --skill secleak-check --agent codex
npx skills add instructa/agent-skills --skill shellck --agent codex
npx skills add instructa/agent-skills --skill stage-review --agent codex
```
</details>

<details>
<summary>Claude Code</summary>

Install bundled skills from `regenrek.agentic-engineer-core`:

```bash
npx skills add instructa/agent-skills --skill architecture-ownership --agent claude-code
npx skills add instructa/agent-skills --skill consolidate-test-suites --agent claude-code
npx skills add instructa/agent-skills --skill find-duplicate-ownership --agent claude-code
npx skills add instructa/agent-skills --skill hard-cut --agent claude-code
npx skills add instructa/agent-skills --skill root-cause-finder --agent claude-code
npx skills add instructa/agent-skills --skill search-context --agent claude-code
```

Install one standalone skill:

```bash
npx skills add instructa/agent-skills --skill app-spec-packager --agent claude-code
npx skills add instructa/agent-skills --skill debug-lldb --agent claude-code
npx skills add instructa/agent-skills --skill gh-repo-bootstrap --agent claude-code
npx skills add instructa/agent-skills --skill git-safe-workflow --agent claude-code
npx skills add instructa/agent-skills --skill gitwhat --agent claude-code
npx skills add instructa/agent-skills --skill go-local-health --agent claude-code
npx skills add instructa/agent-skills --skill homebrew-publish --agent claude-code
npx skills add instructa/agent-skills --skill no-mistakes --agent claude-code
npx skills add instructa/agent-skills --skill package-security-check --agent claude-code
npx skills add instructa/agent-skills --skill redesign-my-landingpage --agent claude-code
npx skills add instructa/agent-skills --skill secleak-check --agent claude-code
npx skills add instructa/agent-skills --skill shellck --agent claude-code
npx skills add instructa/agent-skills --skill stage-review --agent claude-code
```
</details>

<details>
<summary>Cursor</summary>

Install bundled skills from `regenrek.agentic-engineer-core`:

```bash
npx skills add instructa/agent-skills --skill architecture-ownership --agent cursor
npx skills add instructa/agent-skills --skill consolidate-test-suites --agent cursor
npx skills add instructa/agent-skills --skill find-duplicate-ownership --agent cursor
npx skills add instructa/agent-skills --skill hard-cut --agent cursor
npx skills add instructa/agent-skills --skill root-cause-finder --agent cursor
npx skills add instructa/agent-skills --skill search-context --agent cursor
```

Install one standalone skill:

```bash
npx skills add instructa/agent-skills --skill app-spec-packager --agent cursor
npx skills add instructa/agent-skills --skill debug-lldb --agent cursor
npx skills add instructa/agent-skills --skill gh-repo-bootstrap --agent cursor
npx skills add instructa/agent-skills --skill git-safe-workflow --agent cursor
npx skills add instructa/agent-skills --skill gitwhat --agent cursor
npx skills add instructa/agent-skills --skill go-local-health --agent cursor
npx skills add instructa/agent-skills --skill homebrew-publish --agent cursor
npx skills add instructa/agent-skills --skill no-mistakes --agent cursor
npx skills add instructa/agent-skills --skill package-security-check --agent cursor
npx skills add instructa/agent-skills --skill redesign-my-landingpage --agent cursor
npx skills add instructa/agent-skills --skill secleak-check --agent cursor
npx skills add instructa/agent-skills --skill shellck --agent cursor
npx skills add instructa/agent-skills --skill stage-review --agent cursor
```
</details>

## Skills

### `regenrek.agentic-engineer-core`

Core agentic engineering skills for architecture, debugging, refactoring, and test ownership. Bundled skills live in the top-level `skills/` folder; the plugin manifest (`plugins/regenrek.agentic-engineer-core/.plugin/plugin.json`) declares which ones are part of the bundle. Each skill also has its own `README.md`.

Plugin category: `Development`.

Architecture / Ownership:

- `architecture-ownership`: determine the right runtime, first-fix, and canonical long-term owner.
- `find-duplicate-ownership`: audit duplicate ownership and hidden second sources of truth.
- `hard-cut`: keep one canonical implementation during pre-release refactors.

Debugging / Investigation:

- `root-cause-finder`: trace downstream errors to the first unintended side effect.
- `search-context`: search external repositories and reference code before guessing.

Testing:

- `consolidate-test-suites`: place bug-fix coverage in one owning test layer.

### Standalone Skills

These skills are kept as separate artifacts because they are useful independently. Each skill folder also has its own `README.md`.

- `app-spec-packager`: create production-ready app specification packages for coding agents.
- `debug-lldb`: capture and analyze LLDB/GDB backtraces for hangs and high-CPU loops.
- `gh-repo-bootstrap`: create a GitHub repo and bootstrap a local project.
- `git-safe-workflow`: inspect, stage, commit, and push safely when explicitly requested.
- `gitwhat`: print a compact git workspace snapshot.
- `go-local-health`: run local Go test, coverage, and lint health checks.
- `homebrew-publish`: prepare Homebrew tap formulae for CLI/TUI releases.
- `no-mistakes`: use the no-mistakes gated push workflow.
- `package-security-check`: run a reusable JavaScript supply-chain security baseline.
- `redesign-my-landingpage`: build and critique shadcn/Vite/Iconify landing pages.
- `secleak-check`: run BetterLeaks/Trivy scans and add secret-leak guardrails.
- `shellck`: run shellcheck over shell scripts.
- `stage-review`: commit a finished feature locally, then run it through no-mistakes.

## Repository Layout

```text
plugins/
  regenrek.agentic-engineer-core/
    .plugin/plugin.json   # declares which top-level skills are in the bundle
    README.md

skills/
  app-spec-packager/
  architecture-ownership/    # bundled in regenrek.agentic-engineer-core
  consolidate-test-suites/   # bundled in regenrek.agentic-engineer-core
  debug-lldb/
  find-duplicate-ownership/  # bundled in regenrek.agentic-engineer-core
  hard-cut/                  # bundled in regenrek.agentic-engineer-core
  root-cause-finder/         # bundled in regenrek.agentic-engineer-core
  search-context/            # bundled in regenrek.agentic-engineer-core
  ...

internal/
  codex-analysis/
  codex-sandbox/
  create-new-static-website/
  pr-commiter/
```

## Links

- X/Twitter: [@kregenrek](https://x.com/kregenrek)
- Bluesky: [@kevinkern.dev](https://bsky.app/profile/kevinkern.dev)
- Learn Cursor AI: [Ultimate Cursor Course](https://www.instructa.ai/en/cursor-ai)
- Learn to build software with AI: [AI Builder Hub](https://www.instructa.ai)
