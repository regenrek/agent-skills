# Secleak Check Guardrail Templates

Use these templates as a starting point. Customize runtime directories and allowlists to match each repo.

## .forbidden-paths.regex

```
# Local runtime directories
(^|/)\\.your-runtime-dir/
(^|/)\\.agentrig/
(^|/)\\.codex/
(^|/)\\.claude/

# Environment files
(^|/)\\.env$
(^|/)\\.env\\.
(^|/)\\.envrc$

# Credential files
(^|/)\\.aws/credentials$
(^|/)\\.npmrc$
(^|/)\\.netrc$
(^|/)\\.git-credentials$
(^|/)\\.docker/config\\.json$

# Private keys
\\.pem$
\\.key$
\\.p12$
\\.jks$
\\.keystore$
(^|/)id_rsa$
(^|/)id_ed25519$
(^|/)id_ecdsa$
(^|/)id_dsa$
\\.agekey$

# Infrastructure state
\\.tfstate($|\\.|/)
\\.tfplan$
\\.tfvars$

# Secrets and tokens
(^|/)secrets\\.json$
(^|/)tokens\\.json$
(^|/)credentials\\.json$
(^|/)service-account.*\\.json$

# IDE/Editor local files
(^|/)\\.idea/
(^|/)\\.vscode/settings\\.json$
(^|/)\\.vscode/launch\\.json$
```

## scripts/hooks/block-forbidden-staged-files.mjs

```
#!/usr/bin/env node
import { execSync } from 'node:child_process'
import { readFileSync, existsSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = dirname(fileURLToPath(import.meta.url))
const projectRoot = join(__dirname, '..', '..')

function loadForbiddenPatterns() {
  const patternsFile = join(projectRoot, '.forbidden-paths.regex')
  if (!existsSync(patternsFile)) {
    console.log('No .forbidden-paths.regex found, skipping check.')
    return []
  }

  const content = readFileSync(patternsFile, 'utf-8')
  return content
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line && !line.startsWith('#'))
    .map((pattern) => new RegExp(pattern))
}

function getStagedFiles() {
  try {
    const output = execSync('git diff --cached --name-only --diff-filter=ACMR', {
      encoding: 'utf-8',
      cwd: projectRoot,
    })
    return output.trim().split('\n').filter(Boolean)
  } catch {
    return []
  }
}

function main() {
  const patterns = loadForbiddenPatterns()
  if (patterns.length === 0) process.exit(0)

  const stagedFiles = getStagedFiles()
  if (stagedFiles.length === 0) process.exit(0)

  const forbidden = []
  for (const file of stagedFiles) {
    for (const pattern of patterns) {
      if (pattern.test(file)) {
        forbidden.push({ file, pattern: pattern.source })
        break
      }
    }
  }

  if (forbidden.length > 0) {
    console.error('Forbidden files detected in staging area:')
    for (const { file, pattern } of forbidden) {
      console.error(`- ${file}`)
      console.error(`  Pattern: ${pattern}`)
    }
    console.error('Fix: git reset HEAD <file> and update .gitignore if needed.')
    process.exit(1)
  }

  console.log('No forbidden files in staging area')
  process.exit(0)
}

main()
```

## lefthook.yml (Node repos)

```
pre-commit:
  parallel: true
  commands:
    block-forbidden-files:
      run: node scripts/hooks/block-forbidden-staged-files.mjs

pre-push:
  parallel: false
  commands:
    block-forbidden-files:
      run: node scripts/hooks/block-forbidden-staged-files.mjs
    # Optional: run a full security scan
    # security-check:
    #   run: pnpm security:check
```

## .betterleaks.toml

```
# BetterLeaks configuration

title = "repo betterleaks config"

prefilter = '''
matchesAny(attributes[?"path"].orValue(""), [
  r"""(?:^|/)node_modules(?:/.*)?$""",
  r"""(?:^|/)dist(?:/.*)?$""",
  r"""(?:^|/)target(?:/.*)?$"""
])
'''

filter = '''
containsAny(finding["secret"], [
  "EXAMPLE",
  "CHANGEME",
  "YOUR_API_KEY_HERE"
])
'''

[[rules]]
id = "ssh-test-headers"
description = "SSH PEM headers in non-fixture files"
regex = '''-----BEGIN (OPENSSH |RSA )?PRIVATE KEY-----'''
keywords = ["PRIVATE KEY"]
filter = '''
matchesAny(attributes[?"path"].orValue(""), [
  r""".*\.test\.ts$""",
  r""".*\.spec\.ts$""",
  r""".*fixtures.*"""
])
'''
```

## scripts/secleak-check.sh

```
#!/usr/bin/env bash
set -euo pipefail

echo "=== Security Check ==="

ERRORS=0

if command -v betterleaks >/dev/null 2>&1; then
  echo "Running betterleaks..."
  BETTERLEAKS_ARGS=(git --no-banner --redact=100)
  if [ -f .betterleaks.toml ]; then
    BETTERLEAKS_ARGS+=(--config .betterleaks.toml)
  elif [ -f .gitleaks.toml ]; then
    BETTERLEAKS_ARGS+=(--config .gitleaks.toml)
  fi
  BETTERLEAKS_ARGS+=(.)
  if betterleaks "${BETTERLEAKS_ARGS[@]}"; then
    echo "betterleaks: OK"
  else
    echo "betterleaks: FAIL"
    ERRORS=$((ERRORS + 1))
  fi
else
  echo "betterleaks not installed, skipping"
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
```

## .github/workflows/secret-scan.yml

```
name: Secret Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'
  workflow_dispatch:

permissions:
  contents: read

jobs:
  trufflehog:
    name: TruffleHog Secret Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
        with:
          fetch-depth: 0

      - name: TruffleHog (diff scan)
        uses: trufflesecurity/trufflehog@ef6e76c3c4023279497fab4721ffa071a722fd05
        with:
          path: .
          base: ${{ github.event_name == 'pull_request' && github.event.pull_request.base.sha || github.event.before }}
          head: ${{ github.event_name == 'pull_request' && github.event.pull_request.head.sha || github.sha }}
          extra_args: --only-verified

  betterleaks:
    name: BetterLeaks
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
        with:
          fetch-depth: 0

      - name: Install BetterLeaks
        run: |
          set -euo pipefail
          version="1.2.0"
          archive="betterleaks_${version}_linux_x64.tar.gz"
          checksum="5476c1ad776bc884e2b9796f08a44be5a80666833c2987d3d4aadc39cdc6775e"
          curl -fsSL "https://github.com/betterleaks/betterleaks/releases/download/v${version}/${archive}" -o "/tmp/${archive}"
          echo "${checksum}  /tmp/${archive}" | sha256sum -c -
          tar -xzf "/tmp/${archive}" -C /tmp
          sudo install -m 0755 /tmp/betterleaks /usr/local/bin/betterleaks
          betterleaks --version

      - name: BetterLeaks
        run: |
          set -euo pipefail
          args=(git --no-banner --redact=100)
          if [ -f .betterleaks.toml ]; then
            args+=(--config .betterleaks.toml)
          elif [ -f .gitleaks.toml ]; then
            args+=(--config .gitleaks.toml)
          fi
          args+=(.)
          betterleaks "${args[@]}"
```

## .github/dependabot.yml

```
version: 2
updates:
  - package-ecosystem: npm
    directory: /
    schedule:
      interval: weekly
      day: monday
      time: "06:00"
      timezone: UTC
    open-pull-requests-limit: 10
    commit-message:
      prefix: "deps"
    groups:
      production:
        dependency-type: production
        update-types: [minor, patch]
      development:
        dependency-type: development
        update-types: [minor, patch]

  - package-ecosystem: github-actions
    directory: /
    schedule:
      interval: weekly
      day: monday
      time: "06:00"
      timezone: UTC
    open-pull-requests-limit: 5
    commit-message:
      prefix: "ci"
    groups:
      actions:
        patterns: ["*"]
```

## .gitignore snippet

```
# Runtime dirs
.your-runtime-dir/
.agentrig/
.codex/
.claude/

# Env files
.env
.env.*
.envrc

# Credentials
.aws/credentials
.npmrc
.netrc
.git-credentials
.docker/config.json

# Keys
*.pem
*.key
*.p12
*.jks
*.keystore
id_rsa
id_ed25519
id_ecdsa
id_dsa
*.agekey
```

## package.json (Node repos)

```
"scripts": {
  "prepare": "lefthook install",
  "security:check": "./scripts/secleak-check.sh",
  "security:hooks": "node scripts/hooks/block-forbidden-staged-files.mjs"
},
"devDependencies": {
  "lefthook": "^1.10.10"
}
```
