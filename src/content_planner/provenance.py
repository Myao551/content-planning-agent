"""Immutable execution provenance, distinct from the version exporting evidence."""
import copy
import hashlib
import json
import platform
import subprocess
from datetime import datetime, timezone
from importlib.metadata import version
from importlib.resources import files
from pathlib import Path


IMPLEMENTATION_PATHS = ["src", "data", "scripts", "tests", "pyproject.toml", "requirements.txt"]


def capture_runtime_version(*, phase="task_creation"):
    package = files("content_planner")
    sources = {p.name: p.read_text(encoding="utf-8") for p in package.iterdir() if p.name.endswith(".py")}
    snapshot = {
        "status": "captured", "capture_phase": phase, "captured_at": datetime.now(timezone.utc).isoformat(),
        "implementation_hash": hashlib.sha256(json.dumps(sources, sort_keys=True).encode()).hexdigest(),
        "hash_scope": "content_planner top-level Python source files; catalog data has its separate hash",
        "python": platform.python_version(), "pydantic": version("pydantic"),
        "package_version": version("content-planning-agent"), "git_commit": None, "git_dirty": None,
        "git_worktree_dirty": None, "git_dirty_scope": list(IMPLEMENTATION_PATHS),
    }
    # Do not attribute an installed wheel to the Git repository of the caller's cwd.
    try:
        package_path = Path(str(package)).resolve()
        root = package_path.parent.parent
        if package_path != root / "src" / "content_planner" or not (root / ".git").exists():
            return snapshot
        def git(*args):
            return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.DEVNULL, timeout=5).decode().strip()
        snapshot["git_commit"] = git("rev-parse", "HEAD")
        snapshot["git_dirty"] = bool(git("status", "--porcelain", "--untracked-files=all", "--", *IMPLEMENTATION_PATHS))
        snapshot["git_worktree_dirty"] = bool(git("status", "--porcelain", "--untracked-files=all"))
    except (OSError, subprocess.SubprocessError):
        snapshot.update(git_commit=None, git_dirty=None, git_worktree_dirty=None)
    return snapshot


def execution_version(state):
    if state is None:
        return {"status": "not_started", "implementation_hash": None, "git_commit": None, "git_dirty": None}
    if state.get("execution_version"):
        return copy.deepcopy(state["execution_version"])
    return {"status": "unknown_legacy", "implementation_hash": None, "git_commit": None, "git_dirty": None,
            "note": "历史任务没有执行时快照；不从当前源码或旧导出摘要反推执行版本"}
