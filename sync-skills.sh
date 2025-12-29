#!/usr/bin/env bash
set -euo pipefail

# Source-of-truth skills directory (each skill is a folder)
# Default assumes this script lives at repo root with ./skills/
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="${SRC:-$ROOT/skills}"

if [ ! -d "$SRC" ]; then
  echo "Error: SRC directory not found: $SRC" >&2
  exit 1
fi

CLAUDE_SKILLS="${CLAUDE_SKILLS:-$HOME/.claude/skills}"
CODEX_SKILLS="${CODEX_SKILLS:-${CODEX_HOME:-$HOME/.codex}/skills}"

mkdir -p "$CLAUDE_SKILLS" "$CODEX_SKILLS"

sync_one_dest() {
  local dest="$1"
  echo "Syncing into: $dest"

  # Only iterate real directories directly under SRC
  shopt -s nullglob
  for d in "$SRC"/*/; do
    local name
    name="$(basename "$d")"

    mkdir -p "$dest/$name"

    # -aL: archive + dereference symlinks (copy targets)
    # --delete: ONLY deletes inside $dest/$name, never the whole dest
    rsync -aL --delete "$d" "$dest/$name/"
  done
  shopt -u nullglob
}

sync_one_dest "$CLAUDE_SKILLS"
sync_one_dest "$CODEX_SKILLS"

echo "Done."
echo "Claude skills: $CLAUDE_SKILLS"
echo "Codex skills:  $CODEX_SKILLS"
