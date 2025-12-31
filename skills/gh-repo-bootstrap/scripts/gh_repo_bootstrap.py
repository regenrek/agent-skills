#!/usr/bin/env python3
"""
Create a GitHub repository via gh and bootstrap a local project in ~/projects.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,99}$")
OWNER_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")
REMOTE_RE = re.compile(r"^[A-Za-z0-9._-]+$")


def die(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    sys.exit(1)


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
    )


def run_checked(cmd: list[str], cwd: Path | None = None, context: str | None = None) -> str:
    result = run(cmd, cwd=cwd)
    if result.returncode != 0:
        detail = context or "command failed"
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        pieces = [detail]
        if stderr:
            pieces.append(stderr)
        if stdout:
            pieces.append(stdout)
        die("; ".join(pieces))
    return result.stdout.strip()


def ensure_tool(tool: str) -> None:
    if shutil.which(tool) is None:
        die(f"{tool} is not installed or not on PATH")


def validate_repo_name(name: str) -> str:
    trimmed = name.strip()
    if not trimmed:
        die("repository name is required")
    if "/" in trimmed or "\\" in trimmed:
        die("repository name must not contain slashes; use --owner for organization")
    if not REPO_NAME_RE.match(trimmed):
        die("repository name must match [A-Za-z0-9][A-Za-z0-9._-]{0,99}")
    return trimmed


def validate_owner(owner: str) -> str:
    trimmed = owner.strip()
    if not trimmed:
        die("owner cannot be empty")
    if not OWNER_RE.match(trimmed):
        die("owner must match GitHub login rules (letters/numbers/hyphens, no leading/trailing hyphen)")
    return trimmed


def validate_remote(remote: str) -> str:
    trimmed = remote.strip()
    if not trimmed:
        die("remote name cannot be empty")
    if not REMOTE_RE.match(trimmed):
        die("remote name must match [A-Za-z0-9._-]+")
    return trimmed


def ensure_gh_auth() -> None:
    result = run(["gh", "auth", "status", "-h", "github.com"])
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        message = "gh is not authenticated; run 'gh auth login'"
        if stderr:
            message = f"{message} ({stderr})"
        die(message)


def ensure_git_identity(repo_dir: Path) -> None:
    name = run(["git", "config", "--get", "user.name"], cwd=repo_dir).stdout.strip()
    email = run(["git", "config", "--get", "user.email"], cwd=repo_dir).stdout.strip()
    if not name:
        name = run(["git", "config", "--global", "--get", "user.name"]).stdout.strip()
    if not email:
        email = run(["git", "config", "--global", "--get", "user.email"]).stdout.strip()
    if not name or not email:
        die("git user.name and user.email must be configured before committing")


def ensure_repo_dir(projects_dir: Path, name: str) -> Path:
    projects_dir.mkdir(parents=True, exist_ok=True)
    if not projects_dir.is_dir():
        die(f"projects directory is not a directory: {projects_dir}")
    repo_dir = (projects_dir / name).resolve()
    if repo_dir.parent != projects_dir.resolve():
        die("resolved repository path is outside projects directory")
    if repo_dir.exists():
        if not repo_dir.is_dir():
            die(f"target path exists and is not a directory: {repo_dir}")
        if any(repo_dir.iterdir()):
            die(f"target directory is not empty: {repo_dir}")
    else:
        repo_dir.mkdir(parents=False)
    return repo_dir


def gh_repo_exists(repo: str) -> bool:
    result = run(["gh", "repo", "view", repo])
    return result.returncode == 0


def write_file(path: Path, content: str, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        die(f"file already exists: {path}")
    path.write_text(content, encoding="utf-8")


def fetch_gitignore(template: str) -> str:
    output = run_checked(
        ["gh", "api", f"/gitignore/templates/{template}"],
        context="failed to fetch gitignore template",
    )
    data = json.loads(output)
    source = data.get("source")
    if not source:
        die("gitignore template response missing source")
    return source.strip() + "\n"


def fetch_license(license_key: str) -> str:
    output = run_checked(
        ["gh", "api", f"/licenses/{license_key}"],
        context="failed to fetch license template",
    )
    data = json.loads(output)
    body = data.get("body")
    if not body:
        die("license response missing body")
    return body.strip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a GitHub repo with gh and bootstrap a local project in ~/projects.",
    )
    parser.add_argument("name", help="Repository name (no slashes)")
    parser.add_argument(
        "--visibility",
        required=True,
        choices=["public", "private"],
        help="Repository visibility",
    )
    parser.add_argument("--owner", help="GitHub owner/org (defaults to authenticated user)")
    parser.add_argument("--description", help="Repository description")
    parser.add_argument("--projects-dir", default="~/projects", help="Projects root directory")
    parser.add_argument("--remote", default="origin", help="Remote name")
    parser.add_argument("--gitignore", help="GitHub gitignore template name")
    parser.add_argument("--license", dest="license_key", help="License key (e.g., mit)")
    parser.add_argument(
        "--readme",
        dest="readme",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Create README.md (default: true)",
    )
    parser.add_argument(
        "--commit-message",
        default="Initial commit",
        help="Initial commit message",
    )
    parser.add_argument(
        "--overwrite-files",
        action="store_true",
        help="Allow overwriting README/.gitignore/LICENSE if they already exist",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    name = validate_repo_name(args.name)
    remote = validate_remote(args.remote)
    owner = validate_owner(args.owner) if args.owner else None

    ensure_tool("git")
    ensure_tool("gh")
    ensure_gh_auth()

    projects_dir = Path(os.path.expanduser(args.projects_dir)).resolve()
    repo_dir = ensure_repo_dir(projects_dir, name)

    if gh_repo_exists(f"{owner}/{name}" if owner else name):
        die("repository already exists on GitHub")

    if not (repo_dir / ".git").exists():
        run_checked(["git", "init"], cwd=repo_dir, context="git init failed")

    if args.readme:
        readme_path = repo_dir / "README.md"
        write_file(readme_path, f"# {name}\n", overwrite=args.overwrite_files)

    if args.gitignore:
        gitignore_path = repo_dir / ".gitignore"
        content = fetch_gitignore(args.gitignore)
        write_file(gitignore_path, content, overwrite=args.overwrite_files)

    if args.license_key:
        license_path = repo_dir / "LICENSE"
        content = fetch_license(args.license_key)
        write_file(license_path, content, overwrite=args.overwrite_files)

    ensure_git_identity(repo_dir)

    status = run_checked(["git", "status", "--porcelain"], cwd=repo_dir)
    if status:
        run_checked(["git", "add", "-A"], cwd=repo_dir, context="git add failed")
        run_checked(
            ["git", "commit", "-m", args.commit_message],
            cwd=repo_dir,
            context="git commit failed",
        )
    else:
        head = run(["git", "rev-parse", "--verify", "HEAD"], cwd=repo_dir)
        if head.returncode != 0:
            die("no files to commit; create files or enable --readme")

    if run(["git", "remote", "get-url", remote], cwd=repo_dir).returncode == 0:
        die(f"remote already exists: {remote}")

    repo_ref = f"{owner}/{name}" if owner else name
    gh_cmd = [
        "gh",
        "repo",
        "create",
        repo_ref,
        f"--{args.visibility}",
        "--source",
        str(repo_dir),
        "--remote",
        remote,
        "--push",
        "--confirm",
    ]
    if args.description:
        gh_cmd.extend(["--description", args.description])

    run_checked(gh_cmd, context="gh repo create failed")

    upstream = run(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"], cwd=repo_dir)
    if upstream.returncode != 0:
        run_checked(["git", "push", "-u", remote, "HEAD"], cwd=repo_dir, context="git push failed")

    remote_url = run_checked(["git", "remote", "get-url", remote], cwd=repo_dir)
    branch = run_checked(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=repo_dir)

    print("Created repository and local project:")
    print(f"- local: {repo_dir}")
    print(f"- remote: {remote_url}")
    print(f"- branch: {branch}")


if __name__ == "__main__":
    main()
