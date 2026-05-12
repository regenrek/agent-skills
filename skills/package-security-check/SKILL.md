---
name: package-security-check
description: Run a reusable JavaScript supply-chain security baseline with pnpm-first hardening, release-age gating, lifecycle-script controls, exotic dependency checks, CI install checks, and optional incident IOC profiles.
---

# Package Security Check

## Workflow

1. Treat this as a base JS supply-chain check first. Do not force the result around one CVE, vendor, package family, or incident.
2. Before running installs, package-manager mutation commands, or file edits, perform only read-only inspection and present a traffic-light issue analysis:
   - 🔴 Blocker: compromise signal, unsafe install path, secret exposure, or policy that allows unreviewed code execution.
   - 🟡 Risk: hardening gap, stale package-manager major, broad spec, lifecycle script needing review, or CI weakness.
   - 🟢 OK: verified control or no finding.
3. After the traffic-light analysis, ask for approval before changing files or executing package-manager operations that can install, update, publish, or rewrite lockfiles.
4. From this skill directory, run the baseline scanner against the repo or workspace root:

```bash
python3 scripts/check_js_supply_chain.py --root <repo-or-workspace-root>
```

Use `--strict` when the check should fail on hardening gaps. Use `--json` when another tool needs machine-readable output. Use `--include-installed` only when `node_modules` exists and installed package lifecycle metadata matters.

5. For a specific active incident, add one or more IOC profiles:

```bash
python3 scripts/check_js_supply_chain.py \
  --root <repo-or-workspace-root> \
  --ioc data/iocs/npm-supply-chain-2026-05.json \
  --since 2026-05-11T19:20:00Z
```

Refresh incident facts from current advisory sources before relying on a profile. IOC profiles are detection data, not the base policy.

6. Inspect the report in this order:
   - `package_manager_policy`
   - `repo_config_findings` and `effective_config_findings`
   - `risky_direct_specs`
   - `package_lifecycle_scripts`, then `installed_lifecycle_scripts` when requested
   - `ci_install_findings`, including GitHub Actions privilege/cache warnings
   - `ioc_hits`
   - `recent_package_manager_files`
7. If any IOC hits appear, stop normal package work. Do not run installs or lifecycle scripts. Report exact files/packages and recommend isolation, credential rotation, and reinstall from a known-good lockfile.
8. If no compromise is visible but policy is weak and the user approves changes, patch toward the canonical pnpm 11 policy. Keep one package manager, one lockfile, and one repo-local policy source.

## Canonical Policy

Use pnpm 11 or newer as the single package manager because it has the best current pnpm security model: release-age gating, lifecycle-script approval, exotic-subdependency blocking, and trust policy controls.

Verify the current pnpm release before writing `packageManager`:

```bash
npm view pnpm dist-tags --json
```

Require pnpm 11 or newer. As of 2026-05-12, npm reports `latest` as pnpm `11.1.1`. Do not hardcode that value without rechecking. If the repo's Node runtime cannot run pnpm 11, report it as a compatibility blocker instead of silently falling back to pnpm 10.

Use `devEngines.packageManager` to declare the required major:

```json
{
  "devEngines": {
    "packageManager": {
      "name": "pnpm",
      "version": ">=11.0.0",
      "onFail": "download"
    }
  }
}
```

Also pin the verified current stable version in `packageManager` for reproducibility:

```json
{
  "packageManager": "pnpm@11.1.1"
}
```

Treat pnpm 10 or older as `legacy-pnpm-major` unless the user explicitly approves a temporary exception.

## Package Manager Posture

- `pnpm >=11`: canonical baseline. Prefer this for new hardening work.
- `bun`: accepted only when the repo intentionally uses Bun and has equivalent local hardening.
- `npm`: fallback only. Recommend migration to pnpm 11 unless the repo has a clear documented reason to stay npm.
- `yarn`: not accepted baseline for this skill. Recommend pnpm 11 or hardened Bun.

Do not present npm as equivalent to pnpm 11. Bun can be accepted as a project-level choice, but still gets checked against Bun-specific hardening.

For npm fallback repos, require exact saves and reproducible CI while recommending pnpm migration:

```ini
save-exact=true
```

Do not claim npm has a supported release-age gate unless verified in current npm docs and local `npm config ls -l`.

For Bun fallback repos, require repo-local `bunfig.toml`:

```toml
[install]
minimumReleaseAge = 604800
exact = true
frozenLockfile = true
saveTextLockfile = true
```

Do not set `minimumReleaseAgeExcludes` without a reviewed, package-specific reason.

Add or update root `pnpm-workspace.yaml`:

```yaml
minimumReleaseAge: 10080
minimumReleaseAgeStrict: true
minimumReleaseAgeIgnoreMissingTime: false
blockExoticSubdeps: true
trustPolicy: no-downgrade
trustPolicyIgnoreAfter: 43200
dangerouslyAllowAllBuilds: false
savePrefix: ""
allowBuilds: {}
```

Use 7 days (`10080`) for normal repos. Use 3 days only when the repo has a real dependency freshness requirement. Do not set `minimumReleaseAgeExclude` or `trustPolicyExclude` without a reviewed, package-specific reason.

Allow dependency build scripts only after review:

```yaml
allowBuilds:
  esbuild: true
  core-js: false
```

## CI Rules

Require frozen pnpm installs:

```bash
pnpm install --frozen-lockfile
```

Treat these as findings unless the repo has a written reason:

- non-pnpm lockfiles in a pnpm repo
- CI using `npm install`, `yarn install`, unfrozen `bun install`, or unfrozen `pnpm install`
- npm repos that do not use `npm ci` with a committed lockfile while migration is pending
- Bun repos missing `bunfig.toml` release-age, exact, frozen-lockfile, or text-lockfile policy
- `pull_request_target` workflows; these are allowed only with a reviewed reason and must not checkout or run untrusted PR code
- shared caches in publish/release pipelines, including GitHub Actions cache, Turborepo, and Nx cache
- any path where PR-controlled cache content can feed a privileged publish/release workflow
- lockfile rewrite during CI/deploy
- `latest`, `*`, broad ranges, Git/GitHub shorthands, HTTP tarballs, or external `file:` specs
- dependency lifecycle scripts that are not explicitly approved
- `dangerouslyAllowAllBuilds: true`
- workflow use of `toJSON(secrets)` or publish credentials in broad build jobs

## Script

`scripts/check_js_supply_chain.py` performs deterministic local checks:

- detects package-manager and lockfile policy
- checks repo-local and effective pnpm hardening settings
- reports npm fallback and Bun fallback hardening gaps
- reports risky direct dependency specs
- reports lifecycle scripts in workspace manifests and optionally installed packages
- reports risky GitHub Actions install/publish/secret patterns
- warns on `pull_request_target` and shared cache patterns that can become supply-chain escalation paths
- reports package-manager file mtimes after `--since`
- applies optional IOC JSON profiles for incident-specific fingerprints, payload files, persistence paths, workflow markers, and known bad package versions

Keep incident profiles under `data/iocs/`. Do not add incident-specific constants to the scanner unless they are generic across npm supply-chain attacks.
