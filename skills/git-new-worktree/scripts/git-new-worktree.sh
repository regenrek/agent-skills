#!/usr/bin/env bash
set -euo pipefail

usage() {
  printf "usage: source %s <name>\n" "${BASH_SOURCE[0]}"
  printf "  name: branch/worktree name (folder will be <project>-wt/<name>)\n"
}

if [[ $# -lt 1 || "$1" == "-h" || "$1" == "--help" ]]; then
  usage
  exit 1
fi

name="$1"

if [[ "$name" =~ [[:space:]] ]]; then
  printf "error: name must not contain whitespace\n" >&2
  exit 1
fi
if [[ "$name" == /* || "$name" == -* || "$name" == *".."* ]]; then
  printf "error: name must be a relative, safe path (no leading /, -, or ..)\n" >&2
  exit 1
fi

cwd="$(pwd -P 2>/dev/null || pwd)"
if ! git -C "$cwd" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  printf "error: not inside a git repo\n" >&2
  exit 1
fi

repo_root="$(git -C "$cwd" rev-parse --show-toplevel)"
project_name="$(basename "$repo_root")"
repo_parent="$(dirname "$repo_root")"
base_dir="${repo_parent}/${project_name}-wt"

worktree_path="$base_dir/$name"
if [[ -e "$worktree_path" ]]; then
  printf "error: path already exists: %s\n" "$worktree_path" >&2
  exit 1
fi

base_branch="$(git -C "$repo_root" symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
if [[ -z "$base_branch" ]]; then
  base_branch="detached@$(git -C "$repo_root" rev-parse --short HEAD)"
fi

if ! git -C "$repo_root" new "$name"; then
  printf "error: git new failed (is git-new installed/aliased?)\n" >&2
  exit 1
fi

current_branch="$(git -C "$repo_root" symbolic-ref --quiet --short HEAD 2>/dev/null || true)"
if [[ -n "$base_branch" && "$base_branch" != detached@* && -n "$current_branch" && "$current_branch" != "$base_branch" ]]; then
  git -C "$repo_root" switch "$base_branch" >/dev/null 2>&1 || true
fi

mkdir -p "$base_dir"

git -C "$repo_root" worktree add "$worktree_path" "$name"

cd "$worktree_path"
upstream="$(git -C "$worktree_path" rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "none")"

printf "worktree ready\n"
printf -- "- from: %s\n" "$base_branch"
printf -- "- branch: %s\n" "$name"
printf -- "- path: %s\n" "$worktree_path"
printf -- "- upstream: %s\n" "$upstream"

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  printf "note: run via 'source %s %s' to keep cwd\n" "${BASH_SOURCE[0]}" "$name"
fi
