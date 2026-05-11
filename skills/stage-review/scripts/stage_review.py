#!/usr/bin/env python3
"""Plan and create a deterministic local Conventional Commit."""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


PROTECTED_BRANCHES = {"main", "master", "develop", "dev", "prod", "production"}
COMMIT_RE = re.compile(
    r"^(feat|fix|refactor|build|ci|chore|docs|style|perf|test)(\([a-z0-9._-]+\))?: .{1,72}$"
)


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
        return 127, "%s not found" % args[0]
    return proc.returncode, proc.stdout.strip()


def require_ok(cwd: Path, args: List[str]) -> str:
    code, output = run(cwd, args)
    if code != 0:
        raise SystemExit("%s failed:\n%s" % (" ".join(args), output))
    return output


def repo_root(cwd: Path) -> Path:
    output = require_ok(cwd, ["git", "rev-parse", "--show-toplevel"])
    return Path(output)


def current_branch(root: Path) -> str:
    return require_ok(root, ["git", "branch", "--show-current"])


def status_lines(root: Path) -> List[str]:
    output = require_ok(root, ["git", "status", "--porcelain=v1", "-b"])
    return [line for line in output.splitlines() if line]


def changed_paths(root: Path) -> List[str]:
    paths: List[str] = []
    for line in status_lines(root):
        if line.startswith("## "):
            continue
        path = line[3:]
        if " -> " in path:
            old_path, new_path = path.split(" -> ", 1)
            paths.extend([old_path, new_path])
        else:
            paths.append(path)
    return sorted(set(paths))


def remote_url(root: Path, name: str) -> Optional[str]:
    code, output = run(root, ["git", "remote", "get-url", name])
    if code != 0:
        return None
    return output


def in_progress_state(root: Path) -> List[str]:
    git_dir = Path(require_ok(root, ["git", "rev-parse", "--git-dir"]))
    if not git_dir.is_absolute():
        git_dir = root / git_dir
    markers = {
        "merge": git_dir / "MERGE_HEAD",
        "cherry-pick": git_dir / "CHERRY_PICK_HEAD",
        "rebase-merge": git_dir / "rebase-merge",
        "rebase-apply": git_dir / "rebase-apply",
    }
    return [name for name, path in markers.items() if path.exists()]


def validate_paths(root: Path, requested: List[str]) -> List[str]:
    if not requested:
        raise SystemExit("no paths provided")
    normalized: List[str] = []
    repo = root.resolve()
    for item in requested:
        if item in {".", "*"}:
            raise SystemExit("refusing broad path %r; pass explicit files or --all" % item)
        target = (root / item).resolve()
        try:
            target.relative_to(repo)
        except ValueError:
            raise SystemExit("path escapes repo: %s" % item)
        normalized.append(item)
    return normalized


def collect_report(root: Path) -> Dict[str, object]:
    branch = current_branch(root)
    return {
        "repo_root": str(root),
        "branch": branch,
        "protected_branch": branch in PROTECTED_BRANCHES or branch == "",
        "in_progress": in_progress_state(root),
        "remotes": {
            "origin": remote_url(root, "origin"),
            "no-mistakes": remote_url(root, "no-mistakes"),
        },
        "changed_paths": changed_paths(root),
        "status": status_lines(root),
    }


def print_plan(report: Dict[str, object]) -> None:
    print("repo_root: %s" % report["repo_root"])
    print("branch: %s" % (report["branch"] or "-"))
    print("protected_branch: %s" % report["protected_branch"])
    in_progress = report["in_progress"]
    print("in_progress: %s" % (", ".join(in_progress) if in_progress else "-"))
    remotes = report["remotes"]
    if isinstance(remotes, dict):
        print("origin: %s" % (remotes.get("origin") or "-"))
        print("no-mistakes: %s" % (remotes.get("no-mistakes") or "-"))
    paths = report["changed_paths"]
    print("changed_paths:")
    if paths:
        for path in paths:
            print("  %s" % path)
    else:
        print("  -")


def guard_commit(root: Path, message: str) -> None:
    report = collect_report(root)
    if report["protected_branch"]:
        raise SystemExit("refusing to commit on protected or detached branch: %s" % report["branch"])
    if report["in_progress"]:
        raise SystemExit("refusing during git operation: %s" % ", ".join(report["in_progress"]))
    if not report["changed_paths"]:
        raise SystemExit("nothing to commit")
    if not COMMIT_RE.match(message):
        raise SystemExit("commit message must be Conventional Commit and <=72 chars: %s" % message)


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan or create a local stage-review commit.")
    parser.add_argument("--cwd", default=os.getcwd(), help="Repository path")
    parser.add_argument("--json", action="store_true", help="Print machine-readable plan")

    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("plan")

    commit = sub.add_parser("commit")
    commit.add_argument("-m", "--message", required=True, help="Conventional Commit subject")
    commit.add_argument("--body", default="", help="Commit body")
    commit.add_argument("--all", action="store_true", help="Stage all changed paths from git status")
    commit.add_argument("paths", nargs="*", help="Explicit paths to stage")

    args = parser.parse_args()
    root = repo_root(Path(args.cwd).resolve())

    if args.command == "plan":
        report = collect_report(root)
        if args.json:
            print(json.dumps(report, indent=2, sort_keys=True))
        else:
            print_plan(report)
        return 0

    guard_commit(root, args.message)
    paths = changed_paths(root) if args.all else validate_paths(root, args.paths)
    require_ok(root, ["git", "add", "--"] + paths)

    commit_args = ["git", "commit", "-m", args.message]
    if args.body:
        commit_args.extend(["-m", args.body])
    print(require_ok(root, commit_args))
    print(require_ok(root, ["git", "show", "--stat", "--oneline", "--no-renames", "HEAD"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
