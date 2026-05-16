---
name: secleak-check
description: Run or install repo security leak checks with BetterLeaks and Trivy. Use when asked to scan for leaked secrets, vulnerable dependencies, misconfigurations, add secret-leak guardrails, add BetterLeaks, add forbidden-path hooks, or run secleak-check before release.
---

# Secleak Check

## Workflow
1. Confirm cwd and repo root.
2. For a scan request, run the bundled script from this skill, not a target-repo script.
3. For a setup request, add repo-local guardrails from `references/guardrails.md`.
4. Quote exact failing tool output, but never print raw secret values.
5. If the bundled script is unavailable, use the manual fallback commands below.

## Bundled command
Resolve `scripts/secleak-check.sh` relative to this `SKILL.md`.

Common installed path:

```bash
/Users/kregenrek/.agents/skills/secleak-check/scripts/secleak-check.sh
```

## Manual fallback
```bash
betterleaks git --no-banner --redact=100 .
trivy fs --scanners vuln,secret,misconfig --exit-code 1 .
```

Prefer `.betterleaks.toml` when present. If only `.gitleaks.toml` exists, pass `--config .gitleaks.toml`; BetterLeaks supports it for compatibility.

## Reporting
- `betterleaks` findings are blockers until verified false-positive or remediated.
- For historical leaks, report file, line, commit, rule, and fingerprint only.
- `trivy` dependency vulnerabilities should be summarized by severity and top fixed versions.
- Misconfig findings inside `node_modules` are dependency artifact noise unless that file is built or shipped by the repo.

## Guardrail setup
When asked to harden a repo against secret leaks:

1. Inventory existing `.betterleaks.toml`, `.gitleaks.toml`, secret-scan workflows, Dependabot, and hook tooling.
2. Add `.forbidden-paths.regex` and a staged-file hook.
3. Add `.betterleaks.toml` with path-based filters only for fixtures.
4. Add repo-local `scripts/secleak-check.sh` only when the repo wants a first-class local script.
5. Add CI secret scanning and Dependabot when GitHub Actions are in scope.
6. Update `.gitignore` for runtime dirs, env files, credentials, keys, and infra state.

Templates live in `references/guardrails.md`; small examples live in `references/examples.md`.
