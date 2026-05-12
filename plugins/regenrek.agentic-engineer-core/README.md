# Agentic Engineer Core

Core skills for agentic software engineering work:

- `architecture-ownership`: decide the runtime, first-fix, and canonical long-term owner for behavior in layered codebases.
- `consolidate-test-suites`: place test coverage in one owning layer and remove weaker duplicate tests.
- `find-duplicate-ownership`: audit codebases for hidden second sources of truth and contract drift.
- `hard-cut`: enforce one canonical implementation during pre-release or internal-draft refactors.
- `github-reference-context`: find, clone, inspect, and summarize GitHub reference repositories.
- `root-cause-finder`: trace downstream failures back to the first unintended side effect before changing contracts.

## Install

Install the full plugin with AgentRig:

```bash
npx agentrig plugin install cursor agentrig/regenrek.agentic-engineer-core
```

Install only selected skills when you do not need the full bundle:

```bash
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:root-cause-finder
npx agentrig install cursor agentrig/regenrek.agentic-engineer-core --pick skill:architecture-ownership --pick skill:hard-cut
```

Replace `cursor` with another supported provider when needed.
