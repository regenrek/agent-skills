# Homebrew Publish

Create or update Homebrew tap repositories and formulae for CLI and TUI releases.

## Install

```bash
# Codex
npx skills add instructa/agent-skills --skill homebrew-publish --agent codex

# Claude Code
npx skills add instructa/agent-skills --skill homebrew-publish --agent claude-code

# Cursor
npx skills add instructa/agent-skills --skill homebrew-publish --agent cursor
```

## Use When

- The user wants to publish a CLI or TUI through Homebrew.
- A tap repo needs to be created or updated.
- A formula needs source URLs, checksums, build steps, install steps, and `test do` coverage.
- A new release needs formula version and `sha256` updates.

## Requirements

- `brew`
- `git`
- `gh` for creating or pushing the tap repo on GitHub
- Language toolchain for the formula being built, such as Go, Rust, Node, Python, or prebuilt assets

## References

The skill includes formula templates for Go, Rust, Node, Python, and prebuilt binaries under `references/`.

See `SKILL.md` for the full agent workflow.
