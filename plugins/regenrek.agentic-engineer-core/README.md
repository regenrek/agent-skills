# Agentic Engineer Core

Core skills for agentic software engineering work.

Plugin category: `Development`.

Architecture / Ownership:

- `architecture-ownership`: decide the runtime, first-fix, and canonical long-term owner for behavior in layered codebases.
- `find-duplicate-ownership`: audit codebases for hidden second sources of truth and contract drift.
- `hard-cut`: enforce one canonical implementation during pre-release or internal-draft refactors.

Debugging / Investigation:

- `root-cause-finder`: trace downstream failures back to the first unintended side effect before changing contracts.
- `search-context`: search external repositories and reference code before guessing.

Testing:

- `consolidate-test-suites`: place test coverage in one owning layer and remove weaker duplicate tests.

## Bundle Contents

Bundled skills live in the top-level `skills/` folder of this repo. The bundle is defined in `.plugin/plugin.json` via the `skills` array. When AgentRig is ready, the full bundle will install in one command; until then, install each skill individually.

## Install

AgentRig is not ready yet. For now, install each bundled skill individually with the open Agent Skills CLI:

```bash
# List skills available in this repo
npx skills add instructa/agent-skills --list

# Install bundled skills (replace --agent with codex, claude-code, or cursor)
npx skills add instructa/agent-skills --skill architecture-ownership --agent cursor
npx skills add instructa/agent-skills --skill consolidate-test-suites --agent cursor
npx skills add instructa/agent-skills --skill find-duplicate-ownership --agent cursor
npx skills add instructa/agent-skills --skill hard-cut --agent cursor
npx skills add instructa/agent-skills --skill root-cause-finder --agent cursor
npx skills add instructa/agent-skills --skill search-context --agent cursor
```

Use `-g` for a global install, or omit it for a project-local install. Add `--copy` if you prefer copied files instead of symlinks.

Once AgentRig ships, the full bundle will be installable as:

```bash
# Future, once AgentRig is live
npx agentrig plugin install cursor agentrig/regenrek.agentic-engineer-core
```
