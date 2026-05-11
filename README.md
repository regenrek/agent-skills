# Agent Skills

A curated source repo for AgentRig plugins and standalone skills.

This repo is organized around AgentRig distribution instead of local sync scripts:

- `plugins/`: installable AgentRig plugin bundles.
- `skills/`: standalone skills that can be listed and installed independently.
- `internal/`: personal or experimental workflows that are not part of the public install surface.

## Install

Install the core engineering bundle:

```bash
agentrig plugin install cursor agentrig/regenrek.agentic-engineer-core
```

Install selected skills from the bundle:

```bash
agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:root-cause-finder
agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:architecture-ownership --pick skill:hard-cut
```

Replace `cursor` with another supported provider when needed.

## Plugins

### `regenrek.agentic-engineer-core`

Core agentic engineering skills for architecture, debugging, refactoring, and test ownership.

Included skills:

- `architecture-ownership`: determine the right runtime, first-fix, and canonical long-term owner.
- `consolidate-test-suites`: place bug-fix coverage in one owning test layer.
- `find-duplicate-ownership`: audit duplicate ownership and hidden second sources of truth.
- `hard-cut`: keep one canonical implementation during pre-release refactors.
- `root-cause-finder`: trace downstream errors to the first unintended side effect.

## Standalone Skills

These skills are kept as separate artifacts because they are useful independently:

- `app-spec-packager`: create production-ready app specification packages for coding agents.
- `debug-lldb`: capture and analyze LLDB/GDB backtraces for hangs and high-CPU loops.
- `gh-repo-bootstrap`: create a GitHub repo and bootstrap a local project.
- `git-safe-workflow`: inspect, stage, commit, and push safely when explicitly requested.
- `gitwhat`: print a compact git workspace snapshot.
- `go-local-health`: run local Go test, coverage, and lint health checks.
- `homebrew-publish`: prepare Homebrew tap formulae for CLI/TUI releases.
- `redesign-my-landingpage`: build and critique shadcn/Vite/Iconify landing pages.
- `security-leak-guardrails`: add secret-leak prevention guardrails.
- `shellck`: run shellcheck over shell scripts.

## Repository Layout

```text
plugins/
  regenrek.agentic-engineer-core/
    .plugin/plugin.json
    README.md
    skills/

skills/
  app-spec-packager/
  debug-lldb/
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
