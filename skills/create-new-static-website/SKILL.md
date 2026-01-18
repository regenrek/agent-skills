---
name: create-new-static-website
description: Create a new GitHub repo from instructa/astro-website-starter using gitpick, initialize git, and push to GitHub. Use when asked to spin up a new Astro static/SSR site starter from instructa/astro-website-starter, set repo visibility/owner, and then configure Alchemy.
---

# Create New Static Website

## Workflow

1) Collect inputs (ask first)
- Project folder name (for `npx gitpick instructa/astro-website-starter <name>`)
- GitHub owner/org + repo name
- Visibility: public or private
- Whether to push immediately after init (default: yes)

2) Scaffold from template
- From `~/projects`, run:
  - `npx gitpick instructa/astro-website-starter <project-name>`
  - `cd <project-name>`
- If folder exists, ask to rename or delete (use `trash`).

3) Initialize git + create GitHub repo
- `git init`
- `git add -A`
- `git commit -m "feat: init"`
- `gh repo create <owner>/<repo> --public|--private --source . --remote origin --push`
  - If user says no push: omit `--push` and inform them how to push later.

4) Alchemy config (ask after repo creation)
- Ask if they want to configure Alchemy now.
- If yes:
  - `cp .env.example .env`
  - Set `ALCHEMY_PASSWORD` in `.env` (ask for value or instruct user to set).
  - `pnpm exec alchemy login`
  - Confirm any Cloudflare/Alchemy prompts and ensure `pnpm run dev` works.

## Notes
- Keep commands non-interactive when possible.
- Use `gh` for repo creation.
- Don’t delete without confirmation (use `trash`).
