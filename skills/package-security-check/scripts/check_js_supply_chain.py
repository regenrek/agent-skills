#!/usr/bin/env python3
"""Audit JS package-manager state for baseline supply-chain safety."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PACKAGE_MANAGER_FILES = {
    "package.json",
    "pnpm-lock.yaml",
    "package-lock.json",
    "npm-shrinkwrap.json",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
}
CONFIG_FILES = {"pnpm-workspace.yaml", ".npmrc", ".yarnrc.yml", "bunfig.toml"}
CI_FILES = {".yml", ".yaml"}
LIFECYCLE_SCRIPTS = {"preinstall", "install", "postinstall", "prepare", "prepublish", "prepublishOnly"}
PNPM_POLICY_KEYS = {
    "minimumReleaseAge": ("minimumReleaseAge", "minimum-release-age"),
    "minimumReleaseAgeStrict": ("minimumReleaseAgeStrict", "minimum-release-age-strict"),
    "minimumReleaseAgeIgnoreMissingTime": (
        "minimumReleaseAgeIgnoreMissingTime",
        "minimum-release-age-ignore-missing-time",
    ),
    "blockExoticSubdeps": ("blockExoticSubdeps", "block-exotic-subdeps"),
    "trustPolicy": ("trustPolicy", "trust-policy"),
    "trustPolicyIgnoreAfter": ("trustPolicyIgnoreAfter", "trust-policy-ignore-after"),
    "dangerouslyAllowAllBuilds": ("dangerouslyAllowAllBuilds", "dangerously-allow-all-builds"),
    "savePrefix": ("savePrefix", "save-prefix"),
}
SEMVER_RE = re.compile(r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)")


def parse_since(value: str | None) -> datetime | None:
    if not value:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def should_skip_dir(name: str, include_node_modules: bool) -> bool:
    if name in {".git", ".hg", ".svn", ".turbo", ".next", "dist", "build", "coverage"}:
        return True
    return name == "node_modules" and not include_node_modules


def walk_files(root: Path, include_node_modules: bool = False):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d, include_node_modules)]
        current = Path(dirpath)
        for filename in filenames:
            yield current / filename


def read_text(path: Path) -> str:
    try:
        return path.read_text(errors="ignore")
    except OSError:
        return ""


def load_json(path: Path) -> Any:
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError:
        return None


def file_mtime(path: Path) -> datetime:
    return datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(cmd, cwd=cwd, check=False, capture_output=True, text=True, timeout=8)
    except (OSError, subprocess.TimeoutExpired):
        return None


def parse_semver(value: str) -> tuple[int, int, int] | None:
    match = SEMVER_RE.search(value)
    if not match:
        return None
    return (int(match.group("major")), int(match.group("minor")), int(match.group("patch")))


def pnpm_cli_version(root: Path) -> str | None:
    result = run(["pnpm", "--version"], root)
    if not result or result.returncode != 0:
        return None
    return result.stdout.strip() or None


def detected_manager(policy: dict[str, Any]) -> str:
    package_manager = policy.get("packageManager")
    if isinstance(package_manager, str):
        for name in ("pnpm", "bun", "npm", "yarn"):
            if package_manager.startswith(f"{name}@"):
                return name
    dev_engine_pm = policy.get("devEnginesPackageManager")
    if isinstance(dev_engine_pm, dict) and isinstance(dev_engine_pm.get("name"), str):
        return str(dev_engine_pm["name"])
    lockfiles = policy.get("lockfiles")
    if isinstance(lockfiles, dict):
        enabled = [name for name, present in lockfiles.items() if present]
        if len(enabled) == 1:
            return enabled[0]
        if enabled:
            return "mixed"
    return "unknown"


def is_risky_spec(spec: str) -> str | None:
    value = spec.strip()
    if value in {"latest", "*", "x", "X"}:
        return "floating"
    if value.startswith(("^", "~", ">", "<", ">=", "<=")) or re.search(r"\|\|| - ", value):
        return "range"
    if value.startswith(("git+", "github:", "gitlab:", "bitbucket:", "http:", "https:")):
        return "exotic"
    if value.startswith("file:") and not value.startswith(("file:.", "file:..")):
        return "external-file"
    return None


def package_json_risks(root: Path, path: Path, data: Any) -> list[dict[str, str]]:
    if not isinstance(data, dict):
        return []
    risks: list[dict[str, str]] = []
    for section in ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies"):
        deps = data.get(section)
        if not isinstance(deps, dict):
            continue
        for name, raw_spec in deps.items():
            if not isinstance(raw_spec, str):
                continue
            reason = is_risky_spec(raw_spec)
            if reason:
                risks.append(
                    {
                        "file": rel(root, path),
                        "section": section,
                        "package": name,
                        "specifier": raw_spec,
                        "reason": reason,
                    }
                )
    return risks


def package_json_script_risks(root: Path, path: Path, data: Any) -> list[dict[str, str]]:
    if not isinstance(data, dict):
        return []
    scripts = data.get("scripts")
    if not isinstance(scripts, dict):
        return []
    risks: list[dict[str, str]] = []
    for name in sorted(LIFECYCLE_SCRIPTS & scripts.keys()):
        value = scripts.get(name)
        risks.append({"file": rel(root, path), "script": name, "command": str(value)})
    return risks


def effective_pnpm_config(root: Path) -> dict[str, str | None]:
    values: dict[str, str | None] = {}
    for canonical, aliases in PNPM_POLICY_KEYS.items():
        value: str | None = None
        for key in aliases:
            result = run(["pnpm", "config", "get", key], root)
            if not result or result.returncode != 0:
                continue
            candidate = result.stdout.strip()
            if candidate and candidate != "undefined":
                value = candidate
                break
        values[canonical] = value
    return values


def package_manager_policy(root: Path) -> dict[str, Any]:
    package_json = root / "package.json"
    package_manager = ""
    dev_engine_pm: dict[str, Any] | None = None
    if package_json.is_file():
        data = load_json(package_json)
        if isinstance(data, dict):
            if isinstance(data.get("packageManager"), str):
                package_manager = data["packageManager"]
            dev_engines = data.get("devEngines")
            if isinstance(dev_engines, dict) and isinstance(dev_engines.get("packageManager"), dict):
                dev_engine_pm = dev_engines["packageManager"]
    lockfiles = {
        "pnpm": (root / "pnpm-lock.yaml").exists(),
        "npm": (root / "package-lock.json").exists() or (root / "npm-shrinkwrap.json").exists(),
        "yarn": (root / "yarn.lock").exists(),
        "bun": (root / "bun.lock").exists() or (root / "bun.lockb").exists(),
    }
    effective = effective_pnpm_config(root)
    policy = {
        "packageManager": package_manager,
        "devEnginesPackageManager": dev_engine_pm,
        "effective_pnpm_version": pnpm_cli_version(root),
        "lockfiles": lockfiles,
        "effective_pnpm_config": effective,
        "uses_pnpm": package_manager.startswith("pnpm@")
        or (isinstance(dev_engine_pm, dict) and dev_engine_pm.get("name") == "pnpm")
        or lockfiles["pnpm"],
        "non_pnpm_lockfiles": [name for name in ("npm", "yarn", "bun") if lockfiles[name]],
    }
    policy["manager"] = detected_manager(policy)
    return policy


def repo_config_text(root: Path) -> dict[str, str]:
    return {p.name: read_text(p) for p in walk_files(root) if p.name in CONFIG_FILES}


def has_pnpm_setting(text: str, canonical: str) -> bool:
    return any(alias in text for alias in PNPM_POLICY_KEYS[canonical])


def repo_config_findings(root: Path) -> list[str]:
    files = repo_config_text(root)
    policy = package_manager_policy(root)
    pnpm_workspace = files.get("pnpm-workspace.yaml", "")
    npmrc = files.get(".npmrc", "")
    bunfig = files.get("bunfig.toml", "")
    findings: list[str] = []
    manager = policy["manager"]
    if manager == "npm":
        findings.append("npm fallback: recommend migration to pnpm 11 unless repo has a documented reason")
        findings.extend(npm_config_findings(npmrc))
        return findings
    if manager == "bun":
        bun_findings = bun_config_findings(bunfig)
        if bun_findings:
            findings.append("bun fallback: accepted only with bunfig hardening")
            findings.extend(bun_findings)
        return findings
    if manager in {"yarn", "mixed", "unknown"}:
        findings.append("repo must use pnpm 11, or hardened Bun when intentionally chosen")
        return findings
    findings.extend(pnpm_version_findings(policy))
    if policy["non_pnpm_lockfiles"]:
        findings.append(f"non-pnpm lockfiles present: {', '.join(policy['non_pnpm_lockfiles'])}")
    if not pnpm_workspace:
        findings.append("pnpm-workspace.yaml missing")
    for setting in PNPM_POLICY_KEYS:
        if not has_pnpm_setting(pnpm_workspace, setting):
            findings.append(f"pnpm-workspace.yaml missing {setting}")
    if "minimumReleaseAgeExclude" in pnpm_workspace or "minimum-release-age-exclude" in pnpm_workspace:
        findings.append("minimumReleaseAgeExclude requires written justification")
    if "trustPolicyExclude" in pnpm_workspace or "trust-policy-exclude" in pnpm_workspace:
        findings.append("trustPolicyExclude requires written justification")
    if re.search(r"dangerouslyAllowAllBuilds:\s*true|dangerously-allow-all-builds\s*=\s*true", pnpm_workspace):
        findings.append("dangerouslyAllowAllBuilds must not be true")
    if "allowBuilds" not in pnpm_workspace:
        findings.append("pnpm-workspace.yaml missing allowBuilds")
    return findings


def effective_config_findings(root: Path) -> list[str]:
    policy = package_manager_policy(root)
    findings: list[str] = []
    manager = policy["manager"]
    if manager == "npm":
        findings.append("npm fallback: use npm ci, committed package-lock.json, and exact specs while migrating to pnpm 11")
        return findings
    if manager == "bun":
        files = repo_config_text(root)
        bun_findings = bun_config_findings(files.get("bunfig.toml", ""))
        if bun_findings:
            findings.append("bun fallback: use bun install --frozen-lockfile and hardened bunfig.toml")
            findings.extend(bun_findings)
        return findings
    if manager in {"yarn", "mixed", "unknown"}:
        findings.append("repo must use pnpm 11, or hardened Bun when intentionally chosen")
        return findings
    findings.extend(pnpm_version_findings(policy))
    if policy["non_pnpm_lockfiles"]:
        findings.append(f"non-pnpm lockfiles present: {', '.join(policy['non_pnpm_lockfiles'])}")
    effective = policy["effective_pnpm_config"]
    for setting in PNPM_POLICY_KEYS:
        if effective.get(setting) is None:
            findings.append(f"effective pnpm missing {setting}")
    if effective.get("dangerouslyAllowAllBuilds", "").lower() == "true":
        findings.append("effective dangerouslyAllowAllBuilds is true")
    return findings


def npm_config_findings(npmrc: str) -> list[str]:
    findings: list[str] = []
    if not re.search(r"(?m)^\s*save-exact\s*=\s*true\s*$", npmrc):
        findings.append(".npmrc missing save-exact=true")
    return findings


def bun_config_findings(bunfig: str) -> list[str]:
    findings: list[str] = []
    if not bunfig:
        return ["bunfig.toml missing"]
    min_age = re.search(r"(?m)^\s*minimumReleaseAge\s*=\s*(\d+)\s*$", bunfig)
    if not min_age:
        findings.append("bunfig.toml missing install.minimumReleaseAge")
    elif int(min_age.group(1)) < 604800:
        findings.append(f"bunfig.toml minimumReleaseAge below 7 days: {min_age.group(1)}")
    if not re.search(r"(?m)^\s*exact\s*=\s*true\s*$", bunfig):
        findings.append("bunfig.toml missing exact=true")
    if not re.search(r"(?m)^\s*frozenLockfile\s*=\s*true\s*$", bunfig):
        findings.append("bunfig.toml missing frozenLockfile=true")
    if not re.search(r"(?m)^\s*saveTextLockfile\s*=\s*true\s*$", bunfig):
        findings.append("bunfig.toml missing saveTextLockfile=true")
    if re.search(r"(?m)^\s*minimumReleaseAgeExcludes\s*=", bunfig):
        findings.append("bunfig.toml minimumReleaseAgeExcludes requires written justification")
    return findings


def pnpm_version_findings(policy: dict[str, Any]) -> list[str]:
    findings: list[str] = []
    package_manager = policy.get("packageManager")
    if isinstance(package_manager, str) and package_manager.startswith("pnpm@"):
        version = package_manager.removeprefix("pnpm@")
        parsed = parse_semver(version)
        if not parsed:
            findings.append(f"packageManager must pin an exact pnpm 11 version: {package_manager}")
        elif parsed[0] < 11:
            findings.append(f"legacy-pnpm-major: packageManager uses {package_manager}")
    dev_engine_pm = policy.get("devEnginesPackageManager")
    if isinstance(dev_engine_pm, dict) and dev_engine_pm.get("name") == "pnpm":
        raw_version = dev_engine_pm.get("version")
        if isinstance(raw_version, str):
            parsed = parse_semver(raw_version)
            if parsed and parsed[0] < 11 and ">=" not in raw_version:
                findings.append(f"legacy-pnpm-major: devEngines.packageManager allows {raw_version}")
            if "11" not in raw_version:
                findings.append(f"devEngines.packageManager must require pnpm >=11: {raw_version}")
    effective_version = policy.get("effective_pnpm_version")
    if isinstance(effective_version, str):
        parsed = parse_semver(effective_version)
        if parsed and parsed[0] < 11:
            findings.append(f"legacy-pnpm-major: effective pnpm is {effective_version}")
    return sorted(set(findings))


def ci_install_findings(root: Path, path: Path, text: str) -> list[dict[str, str]]:
    if ".github/workflows" not in rel(root, path) or path.suffix not in CI_FILES:
        return []
    findings: list[dict[str, str]] = []
    checks = {
        "npm-install": r"\bnpm\s+install\b",
        "yarn-install": r"\byarn\s+install\b",
        "bun-install-not-frozen": r"\bbun\s+install\b(?![^\n]*--frozen-lockfile)",
        "pnpm-install-not-frozen": r"\bpnpm\s+install\b(?![^\n]*--frozen-lockfile)",
        "secret-json-export": r"toJSON\(secrets\)",
        "npm-publish": r"\bnpm\s+publish\b|\bpnpm\s+publish\b",
    }
    for reason, pattern in checks.items():
        if re.search(pattern, text):
            findings.append({"file": rel(root, path), "reason": reason})
    workflow_risks = github_workflow_risks(text)
    findings.extend({"file": rel(root, path), "reason": reason} for reason in workflow_risks)
    return findings


def github_workflow_risks(text: str) -> list[str]:
    reasons: list[str] = []
    has_pull_request_target = bool(re.search(r"(?m)^\s*pull_request_target\s*:", text))
    has_cache = bool(
        re.search(r"actions/cache(?:@|/)|cache-dependency-path|restore-keys:", text)
        or re.search(r"\b(turbo|turbo\.json|TURBO_|nx|NX_)\b", text)
    )
    has_publish = bool(
        re.search(r"\b(npm|pnpm|bun)\s+publish\b", text)
        or re.search(r"\bnpm\s+publish\b", text)
        or re.search(r"\bid-token:\s*write\b", text)
        or re.search(r"\b(npm publish|trusted publishing|release)\b", text, re.IGNORECASE)
    )
    if has_pull_request_target:
        reasons.append("workflow uses pull_request_target; verify it never checks out or runs untrusted PR code")
    if has_cache and has_publish:
        reasons.append("publish/release workflow uses shared cache; verify PR-contaminated caches cannot feed publishing")
    elif has_cache:
        reasons.append("workflow uses shared cache; verify cache keys cannot be poisoned by untrusted PR jobs")
    if has_pull_request_target and has_cache:
        reasons.append("pull_request_target combined with shared cache; high-risk if cache reaches privileged jobs")
    return sorted(set(reasons))


def installed_package_metadata(root: Path) -> list[Path]:
    files: list[Path] = []
    for nm in root.rglob("node_modules"):
        pnpm = nm / ".pnpm"
        if not pnpm.is_dir():
            continue
        for package_json in pnpm.glob("*/node_modules/**/package.json"):
            files.append(package_json)
    return files


def installed_package_findings(root: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for package_json in installed_package_metadata(root):
        data = load_json(package_json)
        if not isinstance(data, dict):
            continue
        scripts = data.get("scripts")
        if not isinstance(scripts, dict):
            continue
        for name in sorted(LIFECYCLE_SCRIPTS & scripts.keys()):
            findings.append(
                {
                    "file": rel(root, package_json),
                    "package": f"{data.get('name', '<unknown>')}@{data.get('version', '<unknown>')}",
                    "script": name,
                }
            )
    return findings


def load_ioc_profiles(paths: list[str]) -> list[dict[str, Any]]:
    profiles: list[dict[str, Any]] = []
    for raw in paths:
        path = Path(raw).expanduser().resolve()
        data = load_json(path)
        if not isinstance(data, dict):
            raise ValueError(f"invalid IOC profile JSON: {path}")
        data["_path"] = str(path)
        profiles.append(data)
    return profiles


def profile_version_hits(profile: dict[str, Any], text: str) -> list[str]:
    versions = profile.get("package_versions", {})
    if not isinstance(versions, dict):
        return []
    hits: list[str] = []
    for package, raw_versions in versions.items():
        if not isinstance(package, str) or not isinstance(raw_versions, list):
            continue
        for version in raw_versions:
            if not isinstance(version, str):
                continue
            package_pattern = re.escape(package)
            version_pattern = re.escape(version)
            patterns = (
                f"{package}@{version}",
                f'"{package}": "{package}@{version}"',
                f"{package}: {version}",
            )
            json_spec_match = re.search(rf'"{package_pattern}"\s*:\s*"{version_pattern}"', text)
            if json_spec_match or any(pattern in text for pattern in patterns):
                hits.append(f"{package}@{version}")
    return hits


def scan_iocs(root: Path, profiles: list[dict[str, Any]], path: Path, text: str) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    relative = rel(root, path)
    for profile in profiles:
        name = str(profile.get("name", profile.get("_path", "ioc-profile")))
        for marker in profile.get("fingerprints", []):
            if isinstance(marker, str) and marker in text:
                hits.append({"profile": name, "file": relative, "type": "fingerprint", "value": marker})
        for token in profile_version_hits(profile, text):
            hits.append({"profile": name, "file": relative, "type": "package-version", "value": token})
        for pattern in profile.get("workflow_patterns", []):
            if isinstance(pattern, str) and pattern in text:
                hits.append({"profile": name, "file": relative, "type": "workflow-pattern", "value": pattern})
        for filename in profile.get("payload_file_names", []):
            if isinstance(filename, str) and path.name == filename:
                hits.append({"profile": name, "file": relative, "type": "payload-file", "value": filename})
        for persistence in profile.get("persistence_paths", []):
            if isinstance(persistence, str) and relative == persistence:
                hits.append({"profile": name, "file": relative, "type": "persistence-path", "value": persistence})
    return hits


def scan(root: Path, since: datetime | None, ioc_profiles: list[dict[str, Any]], include_installed: bool) -> dict[str, Any]:
    package_files: list[Path] = []
    recent_package_files: list[dict[str, str]] = []
    risky_specs: list[dict[str, str]] = []
    package_lifecycle_scripts: list[dict[str, str]] = []
    ci_findings: list[dict[str, str]] = []
    ioc_hits: list[dict[str, str]] = []

    for path in walk_files(root):
        text = ""
        if path.name in PACKAGE_MANAGER_FILES or path.name in CONFIG_FILES or path.suffix in CI_FILES:
            text = read_text(path)
            ioc_hits.extend(scan_iocs(root, ioc_profiles, path, text))
        else:
            ioc_hits.extend(scan_iocs(root, ioc_profiles, path, ""))
        if path.name in PACKAGE_MANAGER_FILES:
            package_files.append(path)
            if path.name == "package.json":
                data = load_json(path)
                risky_specs.extend(package_json_risks(root, path, data))
                package_lifecycle_scripts.extend(package_json_script_risks(root, path, data))
            if since and file_mtime(path) >= since:
                recent_package_files.append({"file": rel(root, path), "mtime": file_mtime(path).isoformat()})
        if text:
            ci_findings.extend(ci_install_findings(root, path, text))

    installed_lifecycle_scripts = installed_package_findings(root) if include_installed else []

    return {
        "root": str(root),
        "package_manager_policy": package_manager_policy(root),
        "package_manager_files_scanned": len(package_files),
        "risky_direct_specs": risky_specs,
        "package_lifecycle_scripts": package_lifecycle_scripts,
        "installed_lifecycle_scripts": installed_lifecycle_scripts,
        "ci_install_findings": ci_findings,
        "recent_package_manager_files": sorted(recent_package_files, key=lambda x: x["mtime"]),
        "ioc_profiles": [p.get("name", p.get("_path")) for p in ioc_profiles],
        "ioc_hits": ioc_hits,
        "repo_config_findings": repo_config_findings(root),
        "effective_config_findings": effective_config_findings(root),
    }


def print_report(report: dict[str, Any]) -> None:
    print(f"root: {report['root']}")
    print(f"package-manager policy: {json.dumps(report['package_manager_policy'], sort_keys=True)}")
    print(f"package-manager files scanned: {report['package_manager_files_scanned']}")
    print(f"ioc profiles: {json.dumps(report['ioc_profiles'], sort_keys=True)}")
    for key in (
        "ioc_hits",
        "risky_direct_specs",
        "package_lifecycle_scripts",
        "installed_lifecycle_scripts",
        "ci_install_findings",
        "recent_package_manager_files",
        "repo_config_findings",
        "effective_config_findings",
    ):
        values = report[key]
        print(f"\n## {key} ({len(values)})")
        for value in values[:200]:
            if isinstance(value, dict):
                print(json.dumps(value, sort_keys=True))
            else:
                print(value)
        if len(values) > 200:
            print(f"... {len(values) - 200} more")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repo/workspace root to scan")
    parser.add_argument("--since", help="UTC cutoff for recent package-manager file mtimes")
    parser.add_argument("--ioc", action="append", default=[], help="Incident IOC JSON profile to apply")
    parser.add_argument("--include-installed", action="store_true", help="Scan installed node_modules package metadata")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on IOC hits or hardening gaps")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(f"root does not exist: {root}", file=sys.stderr)
        return 2
    try:
        profiles = load_ioc_profiles(args.ioc)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 2

    report = scan(root, parse_since(args.since), profiles, args.include_installed)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)

    hardening_gap = bool(
        report["risky_direct_specs"]
        or report["package_lifecycle_scripts"]
        or report["ci_install_findings"]
        or report["repo_config_findings"]
        or report["effective_config_findings"]
    )
    if report["ioc_hits"]:
        return 1
    if args.strict and hardening_gap:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
