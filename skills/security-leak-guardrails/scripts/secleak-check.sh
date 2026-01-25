#!/usr/bin/env bash
# Security leak check script
# Runs gitleaks and trivy if installed

set -euo pipefail

echo "=== Security Check ==="

ERRORS=0

if command -v gitleaks >/dev/null 2>&1; then
  echo "Running gitleaks..."
  if gitleaks git --no-banner --redact=100 --config .gitleaks.toml .; then
    echo "gitleaks: OK"
  else
    echo "gitleaks: FAIL"
    ERRORS=$((ERRORS + 1))
  fi
else
  echo "gitleaks not installed, skipping"
fi

if command -v trivy >/dev/null 2>&1; then
  echo "Running trivy secret scan..."
  if trivy fs --scanners secret,misconfig --exit-code 1 --quiet .; then
    echo "trivy secret scan: OK"
  else
    echo "trivy secret scan: FAIL"
    ERRORS=$((ERRORS + 1))
  fi

  echo "Running trivy vulnerability scan (HIGH/CRITICAL)..."
  if trivy fs --scanners vuln --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 --quiet .; then
    echo "trivy vulnerability scan: OK"
  else
    echo "trivy vulnerability scan: FAIL"
    ERRORS=$((ERRORS + 1))
  fi
else
  echo "trivy not installed, skipping"
fi

if [ $ERRORS -eq 0 ]; then
  echo "All security checks passed"
  exit 0
else
  echo "$ERRORS security check(s) failed"
  exit 1
fi
