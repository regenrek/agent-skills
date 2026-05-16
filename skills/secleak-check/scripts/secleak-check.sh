#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"

if ! command -v git >/dev/null 2>&1; then
  echo "Missing required CLI: git" >&2
  exit 127
fi

for cmd in betterleaks trivy; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Missing required CLI: $cmd" >&2
    exit 127
  fi
done

if ! REPO_ROOT="$(git -C "$ROOT" rev-parse --show-toplevel 2>/dev/null)"; then
  echo "Not a git repository: $ROOT" >&2
  exit 2
fi

cd "$REPO_ROOT"

errors=0
betterleaks_args=(git --no-banner --redact=100)
if [ -f .betterleaks.toml ]; then
  betterleaks_args+=(--config .betterleaks.toml)
elif [ -f .gitleaks.toml ]; then
  betterleaks_args+=(--config .gitleaks.toml)
fi
betterleaks_args+=(.)

echo "== betterleaks =="
if ! betterleaks "${betterleaks_args[@]}"; then
  errors=$((errors + 1))
fi

echo "== trivy =="
if ! trivy fs --scanners vuln,secret,misconfig --exit-code 1 .; then
  errors=$((errors + 1))
fi

if [ "$errors" -gt 0 ]; then
  echo "$errors security check(s) failed" >&2
  exit 1
fi

echo "All security checks passed"
