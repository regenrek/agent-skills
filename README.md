# Agent Skills

A curated source repo for AgentRig plugins and standalone skills.

This repo is organized around AgentRig distribution instead of local sync scripts:

- `plugins/`: installable AgentRig plugin bundles.
- `skills/`: standalone skills that can be listed and installed independently.
- `internal/`: personal or experimental workflows that are not part of the public install surface.

## Install

Use `--pick` when installing skills from a plugin bundle. Standalone skill refs already point at one skill, so they install without `--pick`.

<details>
<summary>Codex</summary>

Install the full engineering plugin:

```bash
npx agentrig plugin install codex agentrig/regenrek.agentic-engineer-core
```

Install one bundled skill:

```bash
npx agentrig install codex agentrig/regenrek.agentic-engineer-core --pick skill:architecture-ownership
npx agentrig install codex agentrig/regenrek.agentic-engineer-core --pick skill:consolidate-test-suites
npx agentrig install codex agentrig/regenrek.agentic-engineer-core --pick skill:find-duplicate-ownership
npx agentrig install codex agentrig/regenrek.agentic-engineer-core --pick skill:github-reference-context
npx agentrig install codex agentrig/regenrek.agentic-engineer-core --pick skill:hard-cut
npx agentrig install codex agentrig/regenrek.agentic-engineer-core --pick skill:root-cause-finder
```

Install one standalone skill:

```bash
npx agentrig skill install codex agentrig/regenrek.app-spec-packager
npx agentrig skill install codex agentrig/regenrek.debug-lldb
npx agentrig skill install codex agentrig/regenrek.gh-repo-bootstrap
npx agentrig skill install codex agentrig/regenrek.git-safe-workflow
npx agentrig skill install codex agentrig/regenrek.gitwhat
npx agentrig skill install codex agentrig/regenrek.go-local-health
npx agentrig skill install codex agentrig/regenrek.homebrew-publish
npx agentrig skill install codex agentrig/regenrek.no-mistakes
npx agentrig skill install codex agentrig/regenrek.package-security-check
npx agentrig skill install codex agentrig/regenrek.redesign-my-landingpage
npx agentrig skill install codex agentrig/regenrek.security-leak-guardrails
npx agentrig skill install codex agentrig/regenrek.shellck
npx agentrig skill install codex agentrig/regenrek.stage-review
```
</details>

<details>
<summary>Claude</summary>

Install the full engineering plugin:

```bash
npx agentrig plugin install claude agentrig/regenrek.agentic-engineer-core
```

Install one bundled skill:

```bash
npx agentrig install claude agentrig/regenrek.agentic-engineer-core --pick skill:architecture-ownership
npx agentrig install claude agentrig/regenrek.agentic-engineer-core --pick skill:consolidate-test-suites
npx agentrig install claude agentrig/regenrek.agentic-engineer-core --pick skill:find-duplicate-ownership
npx agentrig install claude agentrig/regenrek.agentic-engineer-core --pick skill:github-reference-context
npx agentrig install claude agentrig/regenrek.agentic-engineer-core --pick skill:hard-cut
npx agentrig install claude agentrig/regenrek.agentic-engineer-core --pick skill:root-cause-finder
```

Install one standalone skill:

```bash
npx agentrig skill install claude agentrig/regenrek.app-spec-packager
npx agentrig skill install claude agentrig/regenrek.debug-lldb
npx agentrig skill install claude agentrig/regenrek.gh-repo-bootstrap
npx agentrig skill install claude agentrig/regenrek.git-safe-workflow
npx agentrig skill install claude agentrig/regenrek.gitwhat
npx agentrig skill install claude agentrig/regenrek.go-local-health
npx agentrig skill install claude agentrig/regenrek.homebrew-publish
npx agentrig skill install claude agentrig/regenrek.no-mistakes
npx agentrig skill install claude agentrig/regenrek.package-security-check
npx agentrig skill install claude agentrig/regenrek.redesign-my-landingpage
npx agentrig skill install claude agentrig/regenrek.security-leak-guardrails
npx agentrig skill install claude agentrig/regenrek.shellck
npx agentrig skill install claude agentrig/regenrek.stage-review
```
</details>

<details>
<summary>Cursor</summary>

Install the full engineering plugin:

```bash
npx agentrig plugin install cursor agentrig/regenrek.agentic-engineer-core
```

Install one bundled skill:

```bash
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:architecture-ownership
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:consolidate-test-suites
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:find-duplicate-ownership
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:github-reference-context
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:hard-cut
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:root-cause-finder
```

Install one standalone skill:

```bash
npx agentrig skill install cursor agentrig/regenrek.app-spec-packager
npx agentrig skill install cursor agentrig/regenrek.debug-lldb
npx agentrig skill install cursor agentrig/regenrek.gh-repo-bootstrap
npx agentrig skill install cursor agentrig/regenrek.git-safe-workflow
npx agentrig skill install cursor agentrig/regenrek.gitwhat
npx agentrig skill install cursor agentrig/regenrek.go-local-health
npx agentrig skill install cursor agentrig/regenrek.homebrew-publish
npx agentrig skill install cursor agentrig/regenrek.no-mistakes
npx agentrig skill install cursor agentrig/regenrek.package-security-check
npx agentrig skill install cursor agentrig/regenrek.redesign-my-landingpage
npx agentrig skill install cursor agentrig/regenrek.security-leak-guardrails
npx agentrig skill install cursor agentrig/regenrek.shellck
npx agentrig skill install cursor agentrig/regenrek.stage-review
```
</details>

## Skills

### `regenrek.agentic-engineer-core`

Core agentic engineering skills for architecture, debugging, refactoring, and test ownership. Each bundled skill also has its own `README.md` in the plugin skill folder.

- `architecture-ownership`: determine the right runtime, first-fix, and canonical long-term owner.
- `consolidate-test-suites`: place bug-fix coverage in one owning test layer.
- `find-duplicate-ownership`: audit duplicate ownership and hidden second sources of truth.
- `github-reference-context`: find, clone, inspect, and summarize GitHub reference repositories.
- `hard-cut`: keep one canonical implementation during pre-release refactors.
- `root-cause-finder`: trace downstream errors to the first unintended side effect.

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
- `security-leak-guardrails`: add secret-leak prevention guardrails.
- `shellck`: run shellcheck over shell scripts.
- `stage-review`: commit a finished feature locally, then run it through no-mistakes.

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
