# Reference Context Workflow

This skill intentionally optimizes for better reference context, not for maximum code search speed.

## Why repository discovery first

Repository metadata is useful before cloning anything. It tells us whether a project is archived, recently pushed, language-matched, maintained, licensed, small enough to inspect, and likely to contain examples.

## Why blobless clone

A reference workflow usually needs only a few files from each selected repository. Blobless shallow clone avoids pulling full history and all file contents up front.

## Why local inspection

A repository can look relevant from its name and README but contain no useful implementation files. Local `rg` inspection verifies the repo before it enters the manifest.

## Why a local reference library

Some useful third-party projects are already checked out locally. Register those folders in the user-cache library instead of cloning them again. Project-specific clusters let an agent prefer references that were useful for the current worktree while keeping the manifest format unchanged.

FFF or another long-lived index can accelerate this library layer later, but it should stay optional. The portable baseline remains `rg` so the skill works without installing a search server.

## Why a manifest

A coding agent should not read 5 full repositories. It should get a concise guide:

- what the user is trying to build
- which repositories are best
- why they are relevant
- which files to inspect
- what to study
- what not to copy

## Non-goals

- Do not run cloned code.
- Do not install dependencies from cloned repos.
- Do not provide legal advice.
- Do not replace a dedicated long-term code search index.
- Do not make raw search speed the primary goal.
