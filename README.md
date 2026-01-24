<div align="center">

# 🧠 Agent Skills

**One repo. All your AI agents. Always in sync.**

Keep your skills in a single source of truth and automatically sync them to Claude, Codex, and other AI agents.

</div>

---

## ✨ Why?

- 📁 **Single source of truth** — one skills repo to rule them all
- 🔄 **Auto-sync via Git hooks** — commit, pull, or switch branches and you're done
- ⚡ **Optional file watcher** — instant sync while editing

---

## 📦 Available Skills

| Skill | Description |
|-------|-------------|
| **codex-analysis** | Run Codex CLI for deep code analysis and second-opinion reviews using GPT-5.2 with high reasoning effort. |
| **codex-sandbox** | Create and manage per-task isolated git clones (sandboxes) for Codex CLI sessions, with automatic branch creation and safety hooks that block committing/pushing on main/master. |
| **create-new-static-website** | Create a new GitHub repo from instructa/astro-website-starter using gitpick, initialize git, and push to GitHub. |
| **debug-lldb** | Capture and analyze thread backtraces with LLDB/GDB to debug hangs, deadlocks, UI freezes, IPC stalls, or high-CPU loops. |
| **gh-repo-bootstrap** | Create a new GitHub repository with the gh CLI and bootstrap a local project with git init, README, remote setup, and initial push. |
| **git-safe-workflow** | Safely inspect, stage, commit, and (only if asked) push changes made by an AI agent. Includes worktree safety and merge conflict handling. |
| **gitwhat** | Concise git workspace snapshot for the current directory showing branch, repo root, worktree status, and dirty state. |
| **go-local-health** | Run local Go health checks (tests, coverage, lint) using tools like lazygotest, gocovsh, tparse, and golangci-lint. |
| **homebrew-publish** | Publish CLIs/TUIs to Homebrew via a personal tap. Create formulae for Go, Rust, Node/TypeScript, Python, or prebuilt binaries. |
| **pr-commiter** | Agentic PR committer with deterministic commits, enforced branch/PR workflow, and explicit paths (no git add .). |
| **redesign-my-landingpage** | Build, critique, and iterate high-converting landing pages using React + Vite + TypeScript + Tailwind + shadcn/ui with Iconify icons. |
| **shellck** | Run shellcheck on shell scripts to catch issues like unset vars, bad subshell usage, or quoting mistakes. |

---

## 🚀 Quick Start

### 1. Fork this repo

Click the **Fork** button above, then clone your fork:

> 💡 Each developer maintains their own skills — fork it, make it yours!

### 2. Add your skills

```
skills/
└── <skill-name>/
    └── SKILL.md
```

### 3. Run the sync

```bash
chmod +x ./sync-skills.sh
./sync-skills.sh
```

Your skills are now synced to:
- `~/.claude/skills/`
- `~/.codex/skills/`

---

## 🔧 How It Works

The `sync-skills.sh` script uses `rsync` to mirror your skills folder:

| Flag | Purpose |
|------|---------|
| `-a` | Preserves structure and timestamps |
| `-L` | Follows symlinks (copies real files) |
| `--delete` | Removes files in destination not in source |

---

## ⚙️ Automation

### Option A: Git Hooks (recommended)

Already configured in `.githooks/`. Enable them with:

```bash
git config core.hooksPath .githooks
chmod +x .githooks/post-commit .githooks/post-merge .githooks/post-checkout
```

Now your skills sync automatically when you:
- ✅ `git commit`
- ✅ `git pull` / `git merge`
- ✅ `git checkout`

### Option B: File Watcher (instant sync)

For live sync while editing, run a watcher in your terminal:

**Using [watchexec](https://github.com/watchexec/watchexec)** (cross-platform):

```bash
watchexec -w skills -- ./sync-skills.sh
```

**Using [entr](https://eradman.com/entrproject/)** (simple):

```bash
find skills -type f | entr -r ./sync-skills.sh
```

---

## 💡 Recommendation

| Workflow | Solution |
|----------|----------|
| Normal development | **Git hooks** — set it and forget it |
| Rapid iteration | **File watcher** — see changes instantly |
| Best of both | Use Git hooks + run watcher when actively editing |

---

## Links

- X/Twitter: [@kregenrek](https://x.com/kregenrek)
- Bluesky: [@kevinkern.dev](https://bsky.app/profile/kevinkern.dev)

## Courses
- Learn Cursor AI: [Ultimate Cursor Course](https://www.instructa.ai/en/cursor-ai)
- Learn to build software with AI: [AI Builder Hub](https://www.instructa.ai)

## See my other projects:

* [codefetch](https://github.com/regenrek/codefetch) - Turn code into Markdown for LLMs with one simple terminal command
* [instructa](https://github.com/orgs/instructa/repositories) - Instructa Projects