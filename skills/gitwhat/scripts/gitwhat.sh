#!/usr/bin/env bash
set -euo pipefail

print_header() {
  printf "%s\n" "gitwhat"
}

status_summary() {
  local path="$1"
  local status staged=0 unstaged=0 untracked=0

  status="$(git -C "$path" status --porcelain 2>/dev/null || true)"
  if [[ -z "$status" ]]; then
    printf "clean"
    return 0
  fi

  while IFS= read -r line; do
    [[ -z "$line" ]] && continue
    local x="${line:0:1}"
    local y="${line:1:1}"
    if [[ "$x" == "?" && "$y" == "?" ]]; then
      untracked=$((untracked + 1))
      continue
    fi
    if [[ "$x" != " " ]]; then
      staged=$((staged + 1))
    fi
    if [[ "$y" != " " ]]; then
      unstaged=$((unstaged + 1))
    fi
  done <<< "$status"

  printf "dirty (staged: %d, unstaged: %d, untracked: %d)" "$staged" "$unstaged" "$untracked"
}

print_header

cwd="$(pwd -P 2>/dev/null || pwd)"
printf -- "- CWD: %s\n" "$cwd"

if ! git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf -- "- Repo: not a git repo\n"
  exit 0
fi

repo_root="$(git -C "$cwd" rev-parse --show-toplevel)"
branch="$(git -C "$cwd" symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
if [[ -z "$branch" ]]; then
  head_ref="$(git -C "$cwd" rev-parse --short HEAD 2>/dev/null || echo "unknown")"
  branch="detached@${head_ref}"
fi

git_dir="$(git -C "$cwd" rev-parse --absolute-git-dir)"
worktree_flag="no"
worktree_name="main"
if [[ "$git_dir" == *"/worktrees/"* ]]; then
  worktree_flag="yes"
  worktree_name="$(basename "$git_dir")"
fi

printf -- "- Branch: %s\n" "$branch"
printf -- "- Repo root: %s\n" "$repo_root"
printf -- "- Worktree: %s (%s)\n" "$worktree_flag" "$worktree_name"
printf -- "- Status: %s\n" "$(status_summary "$cwd")"

worktree_list="$(git -C "$repo_root" worktree list --porcelain 2>/dev/null || true)"
if [[ -z "$worktree_list" ]]; then
  printf -- "- Other worktrees: none\n"
  exit 0
fi

current_worktree="$repo_root"
other_count=0
printf -- "- Other worktrees:\n"

while IFS= read -r line; do
  case "$line" in
    worktree\ *)
      path="${line#worktree }"
      if [[ "$path" == "$current_worktree" ]]; then
        continue
      fi
      other_count=$((other_count + 1))
      if [[ ! -d "$path" ]]; then
        printf -- "  - %s: missing\n" "$path"
        continue
      fi
      printf -- "  - %s: %s\n" "$path" "$(status_summary "$path")"
      ;;
  esac
done <<< "$worktree_list"

if [[ "$other_count" -eq 0 ]]; then
  printf -- "  - none\n"
fi
