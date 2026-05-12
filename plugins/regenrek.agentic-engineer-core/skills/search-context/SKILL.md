---
name: github-reference-context
description: Find, clone, inspect, and summarize high-quality GitHub reference repositories for coding agents. Use when a user asks for GitHub reference projects, examples, prior art, inspiration, implementation patterns, or includes "$search-context" in a coding prompt.
license: MIT
metadata:
  version: "0.1.0"
  requires:
    - gh
    - git
    - rg
    - node
---

# GitHub Reference Context

Use this skill when the user wants an agent to find useful GitHub reference projects for a feature, UI pattern, implementation pattern, platform, framework, or library.

Trigger examples:

- `$search-context visual progress indicator ring for ios app latest 2026`
- `find GitHub references for a SwiftUI circular progress ring`
- `how do good projects implement this pattern?`
- `clone a few reference repos and tell me which files to inspect`
- `give this agent GitHub context before implementing the feature`

The goal is not faster raw code search. The goal is better reference selection, fewer cloned repositories, less context noise, and a clean manifest that tells the coding agent what to inspect.

## Default workflow

1. Convert the user request into concise GitHub search phrases.
2. If the user asks for local/third-party references, search the local reference library first.
3. Use GitHub repository discovery for fresh references, not GitHub code search.
4. Prefer recent, maintained, readable repositories.
5. Clone only the top candidates using blobless shallow clone.
6. Inspect local and cloned repositories with `rg`.
7. Write a compact Markdown reference manifest.
8. Tell the agent which files are worth reading and why.

## Required local tools

This skill expects these tools to be available in the shell:

- `gh`, authenticated with GitHub
- `git`
- `rg`, also known as ripgrep
- `node` version 18 or newer

Before running a search, use:

```bash
node scripts/search-context.mjs check
```

## Main command

From the skill directory:

```bash
node scripts/search-context.mjs run "visual progress indicator ring for ios app latest 2026" \
  --preset ios-swift \
  --max-repos 5
```

If the package has been linked with `npm link`, use:

```bash
search-context run "visual progress indicator ring for ios app latest 2026" --preset ios-swift
```

## Presets

Use a preset when the platform or stack is clear.

- `ios-swift`: iOS, Swift, SwiftUI, UIKit, Apple UI components.
- `web-react`: React, Next.js, Vite, Tailwind, component patterns.
- `generic`: fallback when the stack is unknown.

The preset controls GitHub language filters, query expansion, local `rg` terms, file globs, and scoring hints.

## Local reference library

Use the local library for existing third-party folders or previously curated references:

```bash
node scripts/search-context.mjs library add ../third-party/some-repo --tags react,ui --presets web-react --project current
node scripts/search-context.mjs library search "ProgressRing"
node scripts/search-context.mjs run "React progress ring" --sources library,github --project current
```

Library metadata is stored in the OS user cache at `<cache>/library/repositories.json`. Project-specific clusters are stored in the same registry when `--project current` or `--project <id>` is used.

Keep FFF or any future long-lived index as an optional search backend under this library workflow. Do not make FFF a hard requirement and do not split this into a separate skill unless the goal changes from reference selection to general code search.

## Clone policy

Use blobless shallow clones for reference repositories:

```bash
git clone --depth=1 --filter=blob:none --single-branch --no-tags <repo-url> <user-cache>/github-reference-context/refs/owner__repo
```

Do not use normal full clones by default.
Do not clone more than 5 repositories unless the user explicitly asks.
Do not install dependencies from cloned reference repos.
Do not execute cloned project code.
Do not copy large code blocks into the agent context.

By default, keep cloned repositories and manifests in the OS user cache, not in the current project. Use `--project-local` only when the user explicitly wants `.refs/` and `.context/` in the current directory. Inside a Git worktree, those project-local paths must be ignored or the CLI will refuse to write them.

## Search policy

Use repository discovery first.
Avoid using `gh search code` as the primary source.
Use local `rg` after cloning to verify that the repository actually contains relevant implementation files.

Good reference selection beats raw search speed.

Score repositories by:

- intent match
- language and stack match
- recent `pushed_at`
- not archived
- not a fork unless explicitly useful
- readable size
- license presence
- examples, demos, samples, or preview apps
- local matches in relevant implementation files

## Output contract

Always produce a Markdown manifest. The default output is:

```text
<user-cache>/github-reference-context/runs/<timestamp>/reference-context.md
```

The manifest must include:

- user goal
- preset used
- GitHub search phrases used
- top reference repositories
- why each repository is useful
- local path for each cloned repository
- relevant files with short snippets only
- what to study
- what not to copy
- any failures or uncertainty

Do not dump full repositories or long file contents into the response.

## Recommended agent behavior after the manifest

After the manifest is written, the coding agent should:

1. Open only the relevant files listed in the manifest.
2. Study implementation patterns, API choices, animation structure, state handling, and styling.
3. Adapt the pattern to the current project.
4. Respect licensing and avoid copying large sections of code.
5. Implement the requested feature in the user's project.
6. Run tests or build checks if available.

## Useful commands

Run a reference search:

```bash
node scripts/search-context.mjs run "SwiftUI progress ring animation" --preset ios-swift
```

Preview searches without cloning:

```bash
node scripts/search-context.mjs run "SwiftUI progress ring animation" --preset ios-swift --dry-run
```

Use SSH for cloning:

```bash
node scripts/search-context.mjs run "SwiftUI progress ring animation" --preset ios-swift --ssh
```

Search the local reference library:

```bash
node scripts/search-context.mjs library search "Circle().trim"
```

Clean cached reference repos older than 30 days:

```bash
node scripts/search-context.mjs clean --older-than 30d
```

## Safety and licensing

Treat cloned repositories as untrusted code.
Never run project scripts, package managers, tests, binaries, or install commands inside a reference repository unless the user explicitly asks and the risk is understood.
Use reference repos for ideas, structure, and comparison, not for blind copying.
Surface license information in the manifest when available.
