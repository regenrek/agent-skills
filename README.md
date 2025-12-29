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