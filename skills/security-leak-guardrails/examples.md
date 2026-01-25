# Examples

## Example A: CLI repo with local runtime dirs

Add runtime directories specific to the CLI in .forbidden-paths.regex and .gitignore:

```
(^|/)\\.agentrig/
(^|/)\\.claude/
(^|/)\\.codex/
```

## Example B: Web app with build artifacts

Add build artifacts and local env dirs:

```
(^|/)\\.next/
(^|/)\\.vercel/
(^|/)\\.env\\.local$
```

## Example C: Terraform repo

Add Terraform state and plan files:

```
\\.tfstate($|\\.|/)
\\.tfplan$
\\.tfvars$
```

## Example D: Allowlist for fixtures only

Use path-based allowlist entries in .gitleaks.toml:

```
[allowlist]
paths = [
  '''tests/fixtures/''',
  '''scripts/test-data/'''
]
```
