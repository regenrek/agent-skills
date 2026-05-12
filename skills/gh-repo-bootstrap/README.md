# GH Repo Bootstrap

Create a new GitHub repository and bootstrap a matching local project with git, README, remote setup, and initial push.

## Install

```bash
# Codex
npx agentrig skill install codex agentrig/regenrek.gh-repo-bootstrap

# Claude
npx agentrig skill install claude agentrig/regenrek.gh-repo-bootstrap

# Cursor
npx agentrig skill install cursor agentrig/regenrek.gh-repo-bootstrap
```

## Use When

- The user wants to create a new GitHub repo in their account or org.
- A local project under `~/projects/<name>` should be initialized and pushed.
- The repo needs an optional description, gitignore template, license, README choice, or custom remote name.

## Requirements

- `gh` installed and authenticated.
- `git` installed with `user.name` and `user.email` configured.
- A target projects directory, usually `~/projects`.

## Included Helper

Run from this skill directory:

```bash
python3 scripts/gh_repo_bootstrap.py <name> --visibility public
python3 scripts/gh_repo_bootstrap.py <name> --visibility private --description "My project"
```

See `SKILL.md` for the full agent workflow.
