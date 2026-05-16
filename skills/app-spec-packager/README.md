# App Spec Packager

Create production-ready Markdown specification packages for apps, SaaS products, APIs, AI products, and internal tools.

## Install

```bash
# Codex
npx skills add instructa/agent-skills --skill app-spec-packager --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill app-spec-packager --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill app-spec-packager --agent cursor
```

## Use When

- The user wants a complete PRD, product spec, ADR set, technical architecture, or coding-agent build package.
- The idea needs UX flows, data model, API design, QA acceptance tests, release readiness, and executable tasks.
- The output should be concrete enough for coding agents to implement with minimal follow-up.

## What It Produces

- A structured spec folder with product, UX, design, architecture, API/data, implementation, QA, release, and task documents.
- Optional AI, safety/privacy, billing, analytics, and backend specs when relevant.
- Stable requirement IDs and task checklists with acceptance criteria and tests.

## Included Helpers

- `scripts/create_spec_package.py` scaffolds the default package structure.
- `references/` contains document blueprints, platform modules, safety/privacy guidance, task taxonomy, and validation checklists.

See `SKILL.md` for the full agent workflow.
