#!/usr/bin/env python3
"""codex_sandbox.py

Create per-task sandbox clones to run Codex CLI safely.

Goals
- Zero third-party Python dependencies
- Deterministic directory naming
- Safety hooks to block committing/pushing on main/master
- Optional `codex` launch with cwd pinned to the sandbox
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional


MAIN_BRANCHES = {"main", "master"}


@dataclass(frozen=True)
class RunError(Exception):
    cmd: List[str]
    returncode: int
    stdout: str
    stderr: str


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def die(msg: str, code: int = 2) -> None:
    eprint(f"Error: {msg}")
    raise SystemExit(code)


def run(
    cmd: List[str],
    cwd: Optional[Path] = None,
    check: bool = True,
    capture: bool = True,
) -> str:
    """Run a command and return stdout (trimmed)."""
    if capture:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd else None,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out = (proc.stdout or "").strip()
        err = (proc.stderr or "").strip()
        if check and proc.returncode != 0:
            raise RunError(cmd=cmd, returncode=proc.returncode, stdout=out, stderr=err)
        return out
    else:
        proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
        if check and proc.returncode != 0:
            raise RunError(cmd=cmd, returncode=proc.returncode, stdout="", stderr="")
        return ""


def shlex_join(cmd: List[str]) -> str:
    return " ".join(shlex_quote(c) for c in cmd)


def shlex_quote(s: str) -> str:
    # minimal quoting for readable errors
    if re.fullmatch(r"[A-Za-z0-9_./:=+-]+", s):
        return s
    return "'" + s.replace("'", "'\\''") + "'"


def ensure_exe(name: str) -> None:
    if shutil.which(name) is None:
        die(f"Required executable not found in PATH: {name}")


def expand_path(p: str) -> Path:
    return Path(os.path.expanduser(p)).resolve()


def default_cache_dir() -> Path:
    xdg = os.environ.get("XDG_CACHE_HOME")
    if xdg:
        return Path(xdg).resolve()
    return expand_path("~/.cache")


def sanitize_token(s: str) -> str:
    s = s.strip()
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s)
    s = s.strip("-._")
    return s or "task"


def repo_slug_from_url(url: str) -> str:
    # supports git@host:org/repo.git and https://host/org/repo.git
    u = url.strip()
    if u.endswith("/"):
        u = u[:-1]
    # take last path segment
    if ":" in u and not u.startswith("http"):
        u = u.split(":", 1)[1]
    slug = u.split("/")[-1]
    if slug.endswith(".git"):
        slug = slug[:-4]
    return sanitize_token(slug)


def detect_remote_url(cwd: Path, remote: str) -> Optional[str]:
    try:
        return run(["git", "remote", "get-url", remote], cwd=cwd, check=True, capture=True)
    except RunError:
        return None


def detect_repo_root(cwd: Path) -> Optional[Path]:
    try:
        top = run(["git", "rev-parse", "--show-toplevel"], cwd=cwd)
        return Path(top).resolve()
    except RunError:
        return None


def ensure_bare_mirror(bare_dir: Path, remote_url: str) -> None:
    if bare_dir.exists() and not bare_dir.is_dir():
        die(f"Bare dir exists but is not a directory: {bare_dir}")

    if not bare_dir.exists():
        bare_dir.parent.mkdir(parents=True, exist_ok=True)
        run(["git", "clone", "--bare", remote_url, str(bare_dir)], capture=False)
        return

    # ensure origin exists and points to the real remote
    try:
        existing = run(["git", "--git-dir", str(bare_dir), "remote", "get-url", "origin"])
        if existing != remote_url:
            run([
                "git",
                "--git-dir",
                str(bare_dir),
                "remote",
                "set-url",
                "origin",
                remote_url,
            ])
    except SystemExit:
        run(["git", "--git-dir", str(bare_dir), "remote", "add", "origin", remote_url])

    run(["git", "--git-dir", str(bare_dir), "fetch", "--prune", "origin"], capture=False)


def remote_branch_exists(repo_dir: Path, branch: str) -> bool:
    try:
        run(["git", "show-ref", "--verify", f"refs/remotes/origin/{branch}"], cwd=repo_dir)
        return True
    except RunError:
        return False


def ensure_branch_upstream(repo_dir: Path, branch: str) -> None:
    upstream_ref = f"origin/{branch}"
    try:
        current = run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}"],
            cwd=repo_dir,
        )
        if current == upstream_ref:
            return
    except RunError:
        pass

    if remote_branch_exists(repo_dir, branch):
        run(
            ["git", "branch", "--set-upstream-to", upstream_ref, branch],
            cwd=repo_dir,
            capture=False,
        )
    else:
        run(["git", "push", "-u", "origin", branch], cwd=repo_dir, capture=False)


def sandbox_dir(base_dir: Path, repo_slug: str, task: str) -> Path:
    return base_dir / f"{repo_slug}-{sanitize_token(task)}"


HOOK_PRE_COMMIT = """#!/usr/bin/env bash
set -euo pipefail
b="$(git branch --show-current 2>/dev/null || true)"
if [[ "$b" == "main" || "$b" == "master" ]]; then
  echo "Refusing commit on $b. Create a feature branch." >&2
  exit 1
fi
"""

HOOK_PRE_PUSH = """#!/usr/bin/env bash
set -euo pipefail
b="$(git branch --show-current 2>/dev/null || true)"
if [[ "$b" == "main" || "$b" == "master" ]]; then
  echo "Refusing push from $b. Use a PR." >&2
  exit 1
fi
"""


def install_safety_hooks(repo_dir: Path) -> None:
    hooks_dir = repo_dir / ".git" / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)

    for name, content in {
        "pre-commit": HOOK_PRE_COMMIT,
        "pre-push": HOOK_PRE_PUSH,
    }.items():
        p = hooks_dir / name
        p.write_text(content, encoding="utf-8")
        p.chmod(0o755)


def maybe_copy_env(repo_dir: Path) -> None:
    env_example = repo_dir / ".env.example"
    env_file = repo_dir / ".env"
    if env_example.exists() and not env_file.exists():
        shutil.copy2(env_example, env_file)


@dataclass
class SandboxMeta:
    repo_slug: str
    task: str
    branch: str
    remote_url: str
    base_branch: str
    created_at: str

    def to_dict(self) -> dict:
        return {
            "repo_slug": self.repo_slug,
            "task": self.task,
            "branch": self.branch,
            "remote_url": self.remote_url,
            "base_branch": self.base_branch,
            "created_at": self.created_at,
        }


def write_meta(repo_dir: Path, meta: SandboxMeta) -> None:
    p = repo_dir / ".codex_sandbox.json"
    p.write_text(json.dumps(meta.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_meta(repo_dir: Path) -> Optional[dict]:
    p = repo_dir / ".codex_sandbox.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


def is_dirty(repo_dir: Path) -> bool:
    out = run(["git", "status", "--porcelain"], cwd=repo_dir)
    return bool(out.strip())


def current_branch(repo_dir: Path) -> str:
    return run(["git", "branch", "--show-current"], cwd=repo_dir)


def ensure_branch_safe(repo_dir: Path, allow_main: bool) -> None:
    b = current_branch(repo_dir)
    if b in MAIN_BRANCHES and not allow_main:
        die(
            f"Sandbox is on {b}. Refusing to proceed. "
            "Create/switch to a feature branch or pass --allow-main."
        )


def cmd_new(args: argparse.Namespace) -> int:
    ensure_exe("git")

    cwd = Path.cwd()
    repo_root = detect_repo_root(cwd)

    remote_url = args.remote_url
    if remote_url is None:
        if repo_root is None:
            die("Not inside a git repo. Provide --remote-url.")
        remote_url = detect_remote_url(repo_root, args.remote)
        if not remote_url:
            die(f"Failed to detect remote URL for remote '{args.remote}'. Provide --remote-url.")

    repo_slug = args.repo_slug or repo_slug_from_url(remote_url)

    base_dir = expand_path(args.base_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    bare_dir = expand_path(args.bare_dir) if args.bare_dir else (
        default_cache_dir() / "codex-sandboxes" / f"{repo_slug}.git"
    )

    ensure_bare_mirror(bare_dir, remote_url)

    base_branch = args.base_branch or "main"

    branch = args.branch or sanitize_token(args.task)

    sb_dir = sandbox_dir(base_dir, repo_slug, args.task)

    if sb_dir.exists():
        if not args.force:
            die(f"Sandbox already exists: {sb_dir} (use --force to reuse)")
    else:
        run(["git", "clone", str(bare_dir), str(sb_dir)], capture=False)

    # Ensure the sandbox pushes to the real remote, not the bare mirror
    run(["git", "remote", "set-url", "origin", remote_url], cwd=sb_dir)

    # Update remote refs in the sandbox
    run(["git", "fetch", "--prune", "origin"], cwd=sb_dir, capture=False)

    # Create/switch to branch at origin/<base_branch>
    start_ref = f"origin/{base_branch}"
    try:
        run(["git", "rev-parse", "--verify", start_ref], cwd=sb_dir)
    except RunError:
        start_ref = base_branch

    # If branch exists, just switch
    try:
        run(["git", "show-ref", "--verify", f"refs/heads/{branch}"], cwd=sb_dir)
        run(["git", "switch", branch], cwd=sb_dir, capture=False)
    except RunError:
        run(["git", "switch", "-c", branch, start_ref], cwd=sb_dir, capture=False)

    ensure_branch_upstream(sb_dir, branch)

    install_safety_hooks(sb_dir)

    if args.env_copy:
        maybe_copy_env(sb_dir)

    meta = SandboxMeta(
        repo_slug=repo_slug,
        task=args.task,
        branch=branch,
        remote_url=remote_url,
        base_branch=base_branch,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    write_meta(sb_dir, meta)

    ensure_branch_safe(sb_dir, allow_main=args.allow_main)

    print(str(sb_dir))

    if args.launch:
        ensure_exe("codex")
        codex_args = getattr(args, "codex_args", None) or []
        cmd = ["codex", *codex_args]
        eprint(f"Launching: {shlex_join(cmd)} (cwd={sb_dir})")
        proc = subprocess.run(cmd, cwd=str(sb_dir))
        return proc.returncode

    return 0


def cmd_path(args: argparse.Namespace) -> int:
    ensure_exe("git")

    cwd = Path.cwd()
    repo_root = detect_repo_root(cwd)

    remote_url = args.remote_url
    if remote_url is None:
        if repo_root is None:
            die("Not inside a git repo. Provide --remote-url.")
        remote_url = detect_remote_url(repo_root, args.remote)
        if not remote_url:
            die(f"Failed to detect remote URL for remote '{args.remote}'. Provide --remote-url.")

    repo_slug = args.repo_slug or repo_slug_from_url(remote_url)
    base_dir = expand_path(args.base_dir)
    sb_dir = sandbox_dir(base_dir, repo_slug, args.task)
    print(str(sb_dir))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    ensure_exe("git")

    cwd = Path.cwd()
    repo_root = detect_repo_root(cwd)

    remote_url = args.remote_url
    if remote_url is None:
        if repo_root is None:
            die("Not inside a git repo. Provide --remote-url.")
        remote_url = detect_remote_url(repo_root, args.remote)
        if not remote_url:
            die(f"Failed to detect remote URL for remote '{args.remote}'. Provide --remote-url.")

    repo_slug = args.repo_slug or repo_slug_from_url(remote_url)
    base_dir = expand_path(args.base_dir)

    if not base_dir.exists():
        return 0

    prefix = f"{repo_slug}-"
    entries = []
    for p in sorted(base_dir.iterdir()):
        if not p.is_dir():
            continue
        if not p.name.startswith(prefix):
            continue
        if not (p / ".git").exists():
            continue
        meta = read_meta(p)
        branch = None
        dirty = None
        try:
            branch = current_branch(p)
            dirty = is_dirty(p)
        except RunError:
            pass
        entries.append({
            "dir": str(p),
            "branch": branch,
            "dirty": dirty,
            "meta": meta,
        })

    if args.json:
        print(json.dumps(entries, indent=2))
    else:
        for e in entries:
            b = e.get("branch") or "?"
            d = e.get("dirty")
            ds = "dirty" if d else "clean" if d is not None else "?"
            print(f"{e['dir']}\t{b}\t{ds}")

    return 0


def cmd_status(args: argparse.Namespace) -> int:
    ensure_exe("git")
    sb_dir = Path(args.path).resolve() if args.path else None

    if sb_dir is None:
        # derive from task
        cwd = Path.cwd()
        repo_root = detect_repo_root(cwd)
        remote_url = args.remote_url
        if remote_url is None:
            if repo_root is None:
                die("Not inside a git repo. Provide --remote-url or --path.")
            remote_url = detect_remote_url(repo_root, args.remote)
            if not remote_url:
                die(f"Failed to detect remote URL for remote '{args.remote}'. Provide --remote-url.")
        repo_slug = args.repo_slug or repo_slug_from_url(remote_url)
        base_dir = expand_path(args.base_dir)
        sb_dir = sandbox_dir(base_dir, repo_slug, args.task)

    if not sb_dir.exists():
        die(f"Sandbox not found: {sb_dir}")

    ensure_branch_safe(sb_dir, allow_main=args.allow_main)

    b = current_branch(sb_dir)
    d = is_dirty(sb_dir)
    meta = read_meta(sb_dir)

    out = {
        "dir": str(sb_dir),
        "branch": b,
        "dirty": d,
        "meta": meta,
    }
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"dir: {sb_dir}")
        print(f"branch: {b}")
        print(f"dirty: {d}")
        if meta:
            print(f"task: {meta.get('task')}")
            print(f"remote_url: {meta.get('remote_url')}")
            print(f"created_at: {meta.get('created_at')}")

    return 0


def cmd_rm(args: argparse.Namespace) -> int:
    ensure_exe("git")

    cwd = Path.cwd()
    repo_root = detect_repo_root(cwd)

    remote_url = args.remote_url
    if remote_url is None:
        if repo_root is None:
            die("Not inside a git repo. Provide --remote-url.")
        remote_url = detect_remote_url(repo_root, args.remote)
        if not remote_url:
            die(f"Failed to detect remote URL for remote '{args.remote}'. Provide --remote-url.")

    repo_slug = args.repo_slug or repo_slug_from_url(remote_url)
    base_dir = expand_path(args.base_dir)
    sb_dir = sandbox_dir(base_dir, repo_slug, args.task)

    if not sb_dir.exists():
        return 0

    if not args.force:
        try:
            if is_dirty(sb_dir):
                die(f"Sandbox has uncommitted changes: {sb_dir} (use --force to remove)")
        except RunError:
            pass

    shutil.rmtree(sb_dir)
    print(str(sb_dir))
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="codex_sandbox.py")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(sp: argparse.ArgumentParser) -> None:
        sp.add_argument("--base-dir", default="~/wip", help="where to put sandboxes")
        sp.add_argument("--remote", default="origin", help="remote name for discovery")
        sp.add_argument("--remote-url", default=None, help="override remote URL")
        sp.add_argument("--repo-slug", default=None, help="override derived repo name")

    sp_new = sub.add_parser("new", help="create a sandbox")
    add_common(sp_new)
    sp_new.add_argument("task", help="task name (also used for folder suffix)")
    sp_new.add_argument("--branch", default=None, help="branch name (defaults to sanitized task)")
    sp_new.add_argument("--base-branch", default=None, help="base branch to branch from")
    sp_new.add_argument("--bare-dir", default=None, help="where to keep bare mirror")
    sp_new.add_argument("--env-copy", action="store_true", help="copy .env.example -> .env")
    sp_new.add_argument("--force", action="store_true", help="reuse existing sandbox directory")
    sp_new.add_argument("--allow-main", action="store_true", help="allow running on main/master")
    sp_new.add_argument("--launch", action="store_true", help="launch codex inside sandbox")
    sp_new.set_defaults(func=cmd_new)

    sp_path = sub.add_parser("path", help="print the sandbox path for a task")
    add_common(sp_path)
    sp_path.add_argument("task", help="task name")
    sp_path.set_defaults(func=cmd_path)

    sp_list = sub.add_parser("list", help="list sandboxes")
    add_common(sp_list)
    sp_list.add_argument("--json", action="store_true", help="json output")
    sp_list.set_defaults(func=cmd_list)

    sp_status = sub.add_parser("status", help="show sandbox status")
    add_common(sp_status)
    sp_status.add_argument("task", nargs="?", default=None, help="task name")
    sp_status.add_argument("--path", default=None, help="explicit sandbox path")
    sp_status.add_argument("--json", action="store_true", help="json output")
    sp_status.add_argument("--allow-main", action="store_true", help="allow main/master")
    sp_status.set_defaults(func=cmd_status)

    sp_rm = sub.add_parser("rm", help="remove sandbox directory")
    add_common(sp_rm)
    sp_rm.add_argument("task", help="task name")
    sp_rm.add_argument("--force", action="store_true", help="remove even if dirty")
    sp_rm.set_defaults(func=cmd_rm)

    return p


def main() -> int:
    parser = build_parser()
    argv = sys.argv[1:]
    codex_args: List[str] = []
    if "--" in argv:
        idx = argv.index("--")
        codex_args = argv[idx + 1 :]
        argv = argv[:idx]

    try:
        args = parser.parse_args(argv)
        if args.cmd == "new":
            args.codex_args = codex_args
        return args.func(args)
    except RunError as e:
        msg = f"Command failed ({e.returncode}): {shlex_join(e.cmd)}"
        if e.stderr:
            msg += "\n" + e.stderr
        die(msg)


if __name__ == "__main__":
    raise SystemExit(main())
