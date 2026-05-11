#!/usr/bin/env bash

set -euo pipefail
set -f

VERSION="2.1.0"

DEFAULT_ALLOWED_TYPES=(feat fix refactor build ci chore docs style perf test)

usage() {
  cat <<'USAGE'
Agentic PR committer

Usage:
  pr-commiter plan   -m "type(scope): message" -- <paths...>
  pr-commiter commit -m "type(scope): message" -- <paths...>
  pr-commiter -m "type(scope): message" -- <paths...>
  pr-commiter "type(scope): message" <paths...>   # legacy mode

Options:
  -m, --message <msg>       Commit message
  --files-from <path>       File list (one path per line)
  --config <path>           Policy config (default: .committerrc at repo root)
  --json                    Emit machine-readable output
  --dry-run                 Validate + plan only (no staging/commit)
  --reset-staged            Clear staged changes before staging files
  --allow-empty             Allow empty commit (no diff)
  --no-verify               Skip git hooks
  --no-pr                   Skip PR creation
  --push                    Push branch before creating PR
  --force-lock              Remove stale .git/index.lock and retry once
  -h, --help                Show help

Config (.committerrc) keys:
  require_conventional=true|false
  require_scope=true|false
  allowed_types=feat,fix,refactor,build,ci,chore,docs,style,perf,test
  max_files=200
  max_diff_lines=5000
  deny_paths=dist/*,**/*.pem
  allow_paths=src/*,docs/*
  fail_on_staged=true|false
  allow_empty=true|false
  create_pr=true|false
  base_branch=main
  protected_branches=main,master,trunk,develop
  branch_prefix=pr
USAGE
}

die() {
  printf 'Error: %s\n' "$1" >&2
  exit 1
}

warn() {
  printf 'Warn: %s\n' "$1" >&2
}

trim() {
  local s=$1
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  printf '%s' "$s"
}

json_escape() {
  local s=$1
  s=${s//\\/\\\\}
  s=${s//"/\\"}
  s=${s//$'\n'/\\n}
  s=${s//$'\r'/\\r}
  s=${s//$'\t'/\\t}
  printf '%s' "$s"
}

bool_or_die() {
  local value
  value=$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')
  case "$value" in
    true|1|yes|on) printf 'true' ;;
    false|0|no|off|'') printf 'false' ;;
    *) die "invalid boolean for $2: $1" ;;
  esac
}

int_or_die() {
  local value=$1
  if [[ ! "$value" =~ ^[0-9]+$ ]]; then
    die "invalid integer for $2: $value"
  fi
  printf '%s' "$value"
}

abs_path() {
  local path=$1
  if command -v python3 >/dev/null 2>&1; then
    python3 - "$path" <<'PY'
import os, sys
path = sys.argv[1]
if os.path.isabs(path):
    base = path
else:
    base = os.path.join(os.getcwd(), path)
print(os.path.normpath(base))
PY
    return
  fi

  if [ -d "$path" ]; then
    (cd "$path" && pwd -P)
  else
    local dir
    dir=$(dirname "$path")
    (cd "$dir" && printf '%s/%s' "$(pwd -P)" "$(basename "$path")")
  fi
}

join_json_array() {
  local -a values=()
  values=("$@")
  local out='['
  local first=true
  for value in "${values[@]}"; do
    if [ "$first" = true ]; then
      first=false
    else
      out+=','
    fi
    out+="\"$(json_escape "$value")\""
  done
  out+=']'
  printf '%s' "$out"
}

sum_add=0
sum_del=0
binary_count=0

slugify() {
  local value=$1
  value=$(printf '%s' "$value" | tr '[:upper:]' '[:lower:]')
  value=$(printf '%s' "$value" | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/-+/-/g')
  printf '%s' "$value"
}

pick_base_branch() {
  if [ -n "$base_branch" ]; then
    printf '%s' "$base_branch"
    return
  fi

  local origin_head
  origin_head=$(git symbolic-ref -q refs/remotes/origin/HEAD 2>/dev/null || true)
  if [ -n "$origin_head" ]; then
    printf '%s' "${origin_head##*/}"
    return
  fi

  for candidate in main master trunk develop; do
    if git show-ref --verify --quiet "refs/heads/$candidate" || git show-ref --verify --quiet "refs/remotes/origin/$candidate"; then
      printf '%s' "$candidate"
      return
    fi
  done

  if [ -n "$current_branch" ]; then
    printf '%s' "$current_branch"
    return
  fi

  printf 'main'
}

is_protected_branch() {
  local branch=$1
  for protected in "${protected_branches[@]}"; do
    if [ "$branch" = "$protected" ]; then
      return 0
    fi
  done
  return 1
}

build_branch_name() {
  local msg=$1
  local msg_line type_part subject scope raw slug candidate
  msg_line=${msg%%$'\n'*}
  type_part=${msg_line%%:*}
  type_part=${type_part%%(*}
  subject=${msg_line#*:}
  subject=$(trim "$subject")
  scope=""
  scope_regex='^[a-z]+\\(([^)]+)\\)'
  if [[ $msg_line =~ $scope_regex ]]; then
    scope=${BASH_REMATCH[1]}
  fi
  raw=$type_part
  if [ -n "$scope" ]; then
    raw+="-$scope"
  fi
  raw+="-$subject"
  slug=$(slugify "$raw")
  if [ -z "$slug" ]; then
    slug="update"
  fi
  candidate="$branch_prefix/$slug"
  printf '%s' "$candidate"
}

unique_branch_name() {
  local base=$1
  local candidate=$base
  local index=2
  while git show-ref --verify --quiet "refs/heads/$candidate" || git show-ref --verify --quiet "refs/remotes/origin/$candidate"; do
    candidate="$base-$index"
    index=$((index + 1))
  done
  printf '%s' "$candidate"
}

ensure_branch() {
  local target_branch
  local branch_created=false

  if [ -z "$current_branch" ] || is_protected_branch "$current_branch"; then
    target_branch=$(build_branch_name "$message")
    target_branch=$(unique_branch_name "$target_branch")
    git checkout -b "$target_branch" >/dev/null
    branch_created=true
  else
    target_branch="$current_branch"
  fi

  printf '%s|%s' "$target_branch" "$branch_created"
}

ensure_pr() {
  local branch=$1
  local base=$2
  local pr_url=""

  if ! command -v gh >/dev/null 2>&1; then
    die "gh CLI required for PR creation; install gh or pass --no-pr"
  fi

  local origin_url
  origin_url=$(git remote get-url origin 2>/dev/null || true)
  if [[ "$origin_url" != *github.com* ]]; then
    die "origin remote is not GitHub; pass --no-pr or update origin"
  fi

  if gh pr view --json url --jq '.url' >/dev/null 2>&1; then
    pr_url=$(gh pr view --json url --jq '.url')
    printf '%s' "$pr_url"
    return
  fi

  local upstream
  upstream=$(git rev-parse --abbrev-ref --symbolic-full-name "@{u}" 2>/dev/null || true)
  if [ -z "$upstream" ]; then
    if [ "$push_branch" = true ]; then
      git push -u origin "$branch"
    else
      die "branch has no upstream; run with --push or push manually"
    fi
  fi

  local pr_title
  pr_title="$message"
  local pr_body
  pr_body=$(
    cat <<'PR_BODY'
Automated PR from pr-commiter.

Summary:
- REPLACE_MESSAGE
PR_BODY
  )
  pr_body=${pr_body/REPLACE_MESSAGE/$message}

  pr_url=$(gh pr create --title "$pr_title" --body "$pr_body" --base "$base" --head "$branch")
  printf '%s' "$pr_url"
}

reset_diff_stats() {
  sum_add=0
  sum_del=0
  binary_count=0
}

accumulate_numstat() {
  local content=$1
  local add del path
  while IFS=$'\t' read -r add del path; do
    [ -z "$add" ] && continue
    if [ "$add" = "-" ] || [ "$del" = "-" ]; then
      binary_count=$((binary_count + 1))
      continue
    fi
    sum_add=$((sum_add + add))
    sum_del=$((sum_del + del))
  done <<< "$content"
}

compute_diff_stats() {
  local mode=$1
  reset_diff_stats

  local diff_out
  if [ "$mode" = "cached" ]; then
    diff_out=$(git diff --cached --numstat -- "${files[@]}" || true)
    accumulate_numstat "$diff_out"
    return
  fi

  diff_out=$(git diff --numstat -- "${files[@]}" || true)
  accumulate_numstat "$diff_out"

  local untracked
  untracked=$(git ls-files --others --exclude-standard -- "${files[@]}" || true)
  if [ -n "$untracked" ]; then
    while IFS= read -r path; do
      [ -z "$path" ] && continue
      diff_out=$(git diff --no-index --numstat -- /dev/null "$path" 2>/dev/null || true)
      accumulate_numstat "$diff_out"
    done <<< "$untracked"
  fi
}

mode="commit"
message=""
message_from_flag=false
json=false
dry_run=false
reset_staged=false
allow_empty=false
no_verify=false
force_lock=false
create_pr=true
push_branch=false
base_branch=""
branch_prefix="pr"
protected_branches=(main master trunk develop)
config_path=""
files_from=""

if [ "$#" -eq 0 ]; then
  usage
  exit 2
fi

case "${1:-}" in
  plan|commit)
    mode=$1
    shift
    ;;
  help|-h|--help)
    usage
    exit 0
    ;;
  *)
    ;;
esac

files=()

while [ "$#" -gt 0 ]; do
  case "$1" in
    -m|--message)
      [ "$#" -lt 2 ] && die "missing value for $1"
      message=$2
      message_from_flag=true
      shift 2
      ;;
    --files-from)
      [ "$#" -lt 2 ] && die "missing value for $1"
      files_from=$2
      shift 2
      ;;
    --config)
      [ "$#" -lt 2 ] && die "missing value for $1"
      config_path=$2
      shift 2
      ;;
    --json)
      json=true
      shift
      ;;
    --dry-run)
      dry_run=true
      mode="plan"
      shift
      ;;
    --reset-staged)
      reset_staged=true
      shift
      ;;
    --allow-empty)
      allow_empty=true
      shift
      ;;
    --no-verify)
      no_verify=true
      shift
      ;;
    --no-pr)
      create_pr=false
      shift
      ;;
    --push)
      push_branch=true
      shift
      ;;
    --force|--force-lock)
      force_lock=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      files+=("$@")
      break
      ;;
    -* )
      die "unknown flag: $1"
      ;;
    *)
      if [ -z "$message" ] && [ "$message_from_flag" = false ] && [ "$mode" = "commit" ]; then
        message=$1
        shift
      else
        files+=("$1")
        shift
      fi
      ;;
  esac
done

if [ -z "$message" ]; then
  die "commit message required"
fi

if [[ "$message" != *[![:space:]]* ]]; then
  die "commit message must not be empty"
fi

if [ -e "$message" ]; then
  die "first argument looks like a file path; provide the commit message first"
fi

if [ -n "$files_from" ]; then
  if [ ! -f "$files_from" ]; then
    die "files-from not found: $files_from"
  fi
  while IFS= read -r line || [ -n "$line" ]; do
    line=$(trim "$line")
    [ -z "$line" ] && continue
    case "$line" in
      \#*) continue ;;
    esac
    files+=("$line")
  done < "$files_from"
fi

if [ "${#files[@]}" -eq 0 ]; then
  die "no paths provided"
fi

# Defaults
require_conventional=true
require_scope=false
allowed_types=("${DEFAULT_ALLOWED_TYPES[@]}")
max_files=200
max_diff_lines=5000
deny_paths=()
allow_paths=()
fail_on_staged=true

repo_root=$(git rev-parse --show-toplevel 2>/dev/null) || die "not inside a git repository"
repo_root_abs=$(abs_path "$repo_root")

if [ -z "$config_path" ]; then
  if [ -f "$repo_root/.committerrc" ]; then
    config_path="$repo_root/.committerrc"
  fi
fi

if [ -n "$config_path" ]; then
  if [ ! -f "$config_path" ]; then
    die "config not found: $config_path"
  fi
  while IFS= read -r line || [ -n "$line" ]; do
    line=${line%%#*}
    line=$(trim "$line")
    [ -z "$line" ] && continue
    if [[ "$line" != *"="* ]]; then
      warn "ignored config line: $line"
      continue
    fi
    key=$(trim "${line%%=*}")
    value=$(trim "${line#*=}")
    value=${value%\"}
    value=${value#\"}
    value=${value%\'}
    value=${value#\'}
    case "$key" in
      require_conventional)
        require_conventional=$(bool_or_die "$value" "$key")
        ;;
      require_scope)
        require_scope=$(bool_or_die "$value" "$key")
        ;;
      allowed_types)
        IFS=',' read -r -a allowed_types <<< "$value"
        ;;
      max_files)
        max_files=$(int_or_die "$value" "$key")
        ;;
      max_diff_lines)
        max_diff_lines=$(int_or_die "$value" "$key")
        ;;
      deny_paths)
        IFS=',' read -r -a deny_paths <<< "$value"
        ;;
      allow_paths)
        IFS=',' read -r -a allow_paths <<< "$value"
        ;;
      fail_on_staged)
        fail_on_staged=$(bool_or_die "$value" "$key")
        ;;
      allow_empty)
        allow_empty=$(bool_or_die "$value" "$key")
        ;;
      create_pr)
        create_pr=$(bool_or_die "$value" "$key")
        ;;
      base_branch)
        base_branch=$value
        ;;
      protected_branches)
        IFS=',' read -r -a protected_branches <<< "$value"
        ;;
      branch_prefix)
        branch_prefix=$value
        ;;
      *)
        warn "unknown config key: $key"
        ;;
    esac
  done < "$config_path"
fi

# Normalize allow/deny patterns
for i in "${!allow_paths[@]}"; do
  # shellcheck disable=SC2004
  allow_paths[$i]=$(trim "${allow_paths[$i]}")
  if [ -z "${allow_paths[$i]}" ]; then
    unset 'allow_paths[$i]'
  fi
done
for i in "${!deny_paths[@]}"; do
  # shellcheck disable=SC2004
  deny_paths[$i]=$(trim "${deny_paths[$i]}")
  if [ -z "${deny_paths[$i]}" ]; then
    unset 'deny_paths[$i]'
  fi
done

for i in "${!protected_branches[@]}"; do
  # shellcheck disable=SC2004
  protected_branches[$i]=$(trim "${protected_branches[$i]}")
  if [ -z "${protected_branches[$i]}" ]; then
    unset 'protected_branches[$i]'
  fi
done

branch_prefix=$(trim "$branch_prefix")
if [ -z "$branch_prefix" ]; then
  branch_prefix="pr"
fi

# Deduplicate files
unique_files=()
declare -A seen
for file in "${files[@]}"; do
  if [ -n "${seen[$file]+x}" ]; then
    continue
  fi
  seen[$file]=1
  unique_files+=("$file")
done
files=("${unique_files[@]}")

if [ "${#files[@]}" -gt "$max_files" ]; then
  die "too many paths (${#files[@]} > $max_files)"
fi

git_dir=$(git -C "$repo_root" rev-parse --git-dir)
if [ -f "$git_dir/MERGE_HEAD" ] || [ -f "$git_dir/CHERRY_PICK_HEAD" ] || [ -d "$git_dir/rebase-apply" ] || [ -d "$git_dir/rebase-merge" ]; then
  die "merge/rebase/cherry-pick in progress; resolve first"
fi

# Staged changes guard
if [ "$fail_on_staged" = true ]; then
  if ! git diff --cached --quiet; then
    if [ "$reset_staged" = true ]; then
      git restore --staged :/
    else
      staged_list=$(git diff --cached --name-only)
      die "staged changes present; use --reset-staged. Staged: $staged_list"
    fi
  fi
fi

current_branch=$(git symbolic-ref --short -q HEAD 2>/dev/null || true)
base_branch=$(pick_base_branch)

if ! git show-ref --verify --quiet "refs/heads/$base_branch" && ! git show-ref --verify --quiet "refs/remotes/origin/$base_branch"; then
  if [ -n "$current_branch" ]; then
    warn "base branch not found; using current branch: $current_branch"
    base_branch="$current_branch"
  else
    die "base branch not found: $base_branch"
  fi
fi

# Validate message format
if [ "$require_conventional" = true ]; then
  conventional_regex='^([a-z]+)(\\([^)]+\\))?(!)?:[[:space:]]+.+'
  if [[ ! $message =~ $conventional_regex ]]; then
    die "commit message must follow Conventional Commits: type(scope): subject"
  fi
  msg_type=${BASH_REMATCH[1]}
  msg_scope=${BASH_REMATCH[2]}
  type_ok=false
  for allowed in "${allowed_types[@]}"; do
    if [ "$msg_type" = "$allowed" ]; then
      type_ok=true
      break
    fi
  done
  if [ "$type_ok" = false ]; then
    die "commit type not allowed: $msg_type"
  fi
  if [ "$require_scope" = true ] && [ -z "$msg_scope" ]; then
    die "commit scope required by policy"
  fi
fi

# Validate file paths
for file in "${files[@]}"; do
  if [ "$file" = "." ] || [ "$file" = ".." ]; then
    die "path not allowed: $file"
  fi

  abs=$(abs_path "$file")
  case "$abs" in
    "$repo_root_abs"|"$repo_root_abs"/*)
      ;;
    *)
      die "path outside repo: $file"
      ;;
  esac

  if [ ! -e "$file" ]; then
    if ! git ls-files --error-unmatch -- "$file" >/dev/null 2>&1; then
      if ! git cat-file -e "HEAD:$file" >/dev/null 2>&1; then
        die "file not found: $file"
      fi
    fi
  fi

  if [ "${#allow_paths[@]}" -gt 0 ]; then
    matched=false
    for pattern in "${allow_paths[@]}"; do
      # shellcheck disable=SC2254
      case "$file" in
        $pattern) matched=true ;;
      esac
    done
    if [ "$matched" = false ]; then
      die "path not allowed by policy: $file"
    fi
  fi

  for pattern in "${deny_paths[@]}"; do
    # shellcheck disable=SC2254
    case "$file" in
      $pattern)
        die "path denied by policy: $file"
        ;;
    esac
  done
done

compute_diff_stats "worktree"

sum_lines=$((sum_add + sum_del))
if [ "$max_diff_lines" -gt 0 ] && [ "$sum_lines" -gt "$max_diff_lines" ]; then
  die "diff too large (${sum_lines} > $max_diff_lines)"
fi

planned_branch="$current_branch"
planned_branch_created=false
if [ -z "$current_branch" ] || is_protected_branch "$current_branch"; then
  planned_branch=$(build_branch_name "$message")
  planned_branch=$(unique_branch_name "$planned_branch")
  planned_branch_created=true
fi

if [ "$mode" = "plan" ] || [ "$dry_run" = true ]; then
  if [ "$json" = true ]; then
    printf '{"status":"ok","mode":"plan","message":"%s","repo":"%s","branch":"%s","base":"%s","create_branch":%s,"files":%s,"diff":{"add":%d,"del":%d,"binary":%d}}\n' \
      "$(json_escape "$message")" \
      "$(json_escape "$repo_root")" \
      "$(json_escape "$planned_branch")" \
      "$(json_escape "$base_branch")" \
      "$planned_branch_created" \
      "$(join_json_array "${files[@]}")" \
      "$sum_add" "$sum_del" "$binary_count"
  else
    printf 'Plan ok\n'
    printf 'version: %s\n' "$VERSION"
    printf 'repo: %s\n' "$repo_root"
    printf 'message: %s\n' "$message"
    printf 'branch: %s\n' "$planned_branch"
    printf 'base: %s\n' "$base_branch"
    if [ "$planned_branch_created" = true ]; then
      printf 'branch_action: create\n'
    else
      printf 'branch_action: keep\n'
    fi
    printf 'files (%d): %s\n' "${#files[@]}" "${files[*]}"
    printf 'diff: +%d -%d (binary %d)\n' "$sum_add" "$sum_del" "$binary_count"
  fi
  exit 0
fi

branch_info=$(ensure_branch)
selected_branch=${branch_info%%|*}
branch_created=${branch_info#*|}
current_branch=$selected_branch

git add -A -- "${files[@]}"

compute_diff_stats "cached"
sum_lines=$((sum_add + sum_del))
if [ "$max_diff_lines" -gt 0 ] && [ "$sum_lines" -gt "$max_diff_lines" ]; then
  die "diff too large (${sum_lines} > $max_diff_lines)"
fi

if git diff --cached --quiet; then
  if [ "$allow_empty" = true ]; then
    warn "no staged changes; committing empty by policy"
  else
    die "no staged changes"
  fi
fi

commit_stderr=$(mktemp)
commit_cmd=(git commit)
if [ "$no_verify" = true ]; then
  commit_cmd+=(--no-verify)
fi

commit_tmp=
if [[ "$message" == *$'\n'* ]]; then
  commit_tmp=$(mktemp)
  printf '%s' "$message" > "$commit_tmp"
  commit_cmd+=(-F "$commit_tmp")
else
  commit_cmd+=(-m "$message")
fi

run_commit() {
  if "${commit_cmd[@]}" 2> >(tee "$commit_stderr" >&2); then
    return 0
  fi
  return 1
}

if ! run_commit; then
  if [ "$force_lock" = true ]; then
    lock_path=$(awk -F"'" '/index\\.lock/ { print $2; exit }' "$commit_stderr")
    if [ -n "$lock_path" ] && [ -e "$lock_path" ]; then
      rm -f "$lock_path"
      warn "removed stale lock: $lock_path"
      run_commit || true
    fi
  fi
fi

if [ -n "$commit_tmp" ]; then
  rm -f "$commit_tmp"
fi

if ! git diff --cached --quiet; then
  die "commit failed; staged changes remain"
fi

short_sha=$(git rev-parse --short HEAD)
pr_url=""
if [ "$create_pr" = true ]; then
  pr_url=$(ensure_pr "$current_branch" "$base_branch")
fi
if [ "$json" = true ]; then
  printf '{"status":"ok","mode":"commit","sha":"%s","message":"%s","branch":"%s","base":"%s","create_pr":%s,"pr_url":"%s","files":%s,"diff":{"add":%d,"del":%d,"binary":%d}}\n' \
    "$(json_escape "$short_sha")" \
    "$(json_escape "$message")" \
    "$(json_escape "$current_branch")" \
    "$(json_escape "$base_branch")" \
    "$create_pr" \
    "$(json_escape "$pr_url")" \
    "$(join_json_array "${files[@]}")" \
    "$sum_add" "$sum_del" "$binary_count"
else
  printf 'Commit ok\n'
  printf 'version: %s\n' "$VERSION"
  printf 'sha: %s\n' "$short_sha"
  printf 'message: %s\n' "$message"
  printf 'branch: %s\n' "$current_branch"
  printf 'base: %s\n' "$base_branch"
  if [ "$branch_created" = true ]; then
    printf 'branch_action: create\n'
  else
    printf 'branch_action: keep\n'
  fi
  if [ "$create_pr" = true ]; then
    printf 'pr: %s\n' "$pr_url"
  else
    printf 'pr: skipped\n'
  fi
  printf 'files (%d): %s\n' "${#files[@]}" "${files[*]}"
  printf 'diff: +%d -%d (binary %d)\n' "$sum_add" "$sum_del" "$binary_count"
fi
