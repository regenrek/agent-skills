#!/usr/bin/env python3
"""Inspect no-mistakes readiness without mutating the repo."""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def run(cwd: Path, args: List[str]) -> Tuple[int, str]:
    try:
        proc = subprocess.run(
            args,
            cwd=str(cwd),
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except FileNotFoundError:
        return 127, f"{args[0]} not found"
    return proc.returncode, proc.stdout.strip()


def repo_root(cwd: Path) -> Optional[Path]:
    code, output = run(cwd, ["git", "rev-parse", "--show-toplevel"])
    if code != 0:
        return None
    return Path(output)


def remote_url(root: Path, name: str) -> Optional[str]:
    code, output = run(root, ["git", "remote", "get-url", name])
    if code != 0:
        return None
    return output


def simple_config_summary(config_path: Path) -> Dict[str, object]:
    if not config_path.exists():
        return {"exists": False}

    summary: Dict[str, object] = {"exists": True, "agent": None, "commands": {}}
    in_commands = False
    commands: Dict[str, str] = {}

    for raw in config_path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("agent:"):
            summary["agent"] = line.split(":", 1)[1].strip().strip('"').strip("'")
        if line.startswith("commands:"):
            in_commands = True
            continue
        if in_commands:
            if not raw.startswith((" ", "\t")):
                in_commands = False
                continue
            stripped = line.strip()
            if ":" in stripped:
                key, value = stripped.split(":", 1)
                commands[key.strip()] = value.strip().strip('"').strip("'")

    summary["commands"] = commands
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect no-mistakes install, repo gate, and config readiness."
    )
    parser.add_argument("--cwd", default=os.getcwd(), help="Repository path to inspect")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()

    cwd = Path(args.cwd).resolve()
    root = repo_root(cwd)
    no_mistakes = shutil.which("no-mistakes")

    report: Dict[str, object] = {
        "cwd": str(cwd),
        "repo_root": str(root) if root else None,
        "tools": {
            "git": shutil.which("git"),
            "no-mistakes": no_mistakes,
            "gh": shutil.which("gh"),
            "glab": shutil.which("glab"),
            "claude": shutil.which("claude"),
            "codex": shutil.which("codex"),
            "opencode": shutil.which("opencode"),
            "acli": shutil.which("acli"),
            "pi": shutil.which("pi"),
            "acpx": shutil.which("acpx"),
        },
        "remotes": {},
        "config": None,
        "doctor": None,
        "warnings": [],
    }

    warnings: List[str] = []
    if not root:
        warnings.append("not inside a git repository")
    else:
        report["remotes"] = {
            "origin": remote_url(root, "origin"),
            "no-mistakes": remote_url(root, "no-mistakes"),
        }
        report["config"] = simple_config_summary(root / ".no-mistakes.yaml")

        remotes = report["remotes"]
        if isinstance(remotes, dict) and not remotes.get("origin"):
            warnings.append("missing origin remote")
        if isinstance(remotes, dict) and not remotes.get("no-mistakes"):
            warnings.append("missing no-mistakes remote; run no-mistakes init")

    if not no_mistakes:
        warnings.append("no-mistakes binary not found on PATH")
    else:
        code, output = run(root or cwd, ["no-mistakes", "doctor"])
        report["doctor"] = {"exit_code": code, "output": output}
        if code != 0:
            warnings.append("no-mistakes doctor returned non-zero")

    report["warnings"] = warnings

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return 1 if warnings else 0

    print(f"cwd: {report['cwd']}")
    print(f"repo_root: {report['repo_root'] or '-'}")
    tools = report["tools"]
    if isinstance(tools, dict):
        available = ", ".join(name for name, path in tools.items() if path)
        missing = ", ".join(name for name, path in tools.items() if not path)
        print(f"available: {available or '-'}")
        print(f"missing: {missing or '-'}")
    if root:
        print(f"origin: {remote_url(root, 'origin') or '-'}")
        print(f"no-mistakes remote: {remote_url(root, 'no-mistakes') or '-'}")
        config = report["config"]
        if isinstance(config, dict):
            print(f".no-mistakes.yaml: {'yes' if config.get('exists') else 'no'}")
            if config.get("agent"):
                print(f"agent: {config['agent']}")
            commands = config.get("commands")
            if isinstance(commands, dict) and commands:
                print("commands: " + ", ".join(sorted(commands)))
    for warning in warnings:
        print(f"warning: {warning}")
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
