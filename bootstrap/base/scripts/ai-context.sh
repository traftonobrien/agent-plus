#!/usr/bin/env sh
set -eu

# ai-context.sh emits complete current records and references binding procedures.

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

# The copied doctor owns legacy declaration, manifest, and hook validation.
if [ -e "$ROOT_DIR/.agent-plus/legacy-adoption.json" ] || [ -L "$ROOT_DIR/.agent-plus/legacy-adoption.json" ]; then
  AGENT_PLUS_DOCTOR_SOURCE_ONLY=1 . "$ROOT_DIR/scripts/agent-plus-doctor.sh"
  agent_plus_check_legacy_adoption "$ROOT_DIR"
else
  ROOT_DIR="$ROOT_DIR" python3 - <<'PY'
import os
import stat
import subprocess
from pathlib import Path

root = Path(os.environ["ROOT_DIR"])
agent = root / ".agent-plus"
hook = agent / "project-startup-check.sh"
if hook.exists() or hook.is_symlink():
    try:
        hook_fd = os.open(
            hook,
            os.O_RDONLY
            | os.O_NONBLOCK
            | os.O_NOFOLLOW
            | getattr(os, "O_CLOEXEC", 0),
        )
    except OSError as exc:
        raise SystemExit(f"Cannot securely open project startup check: {exc}") from exc
    try:
        details = os.fstat(hook_fd)
        if stat.S_ISLNK(details.st_mode) or not stat.S_ISREG(details.st_mode):
            raise SystemExit("Project startup check must be a regular file")
        if not details.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
            raise SystemExit("Project startup check must be executable")
        result = subprocess.run(
            ["/bin/sh", f"/dev/fd/{hook_fd}"],
            cwd=root,
            check=False,
            pass_fds=(hook_fd,),
        )
    finally:
        os.close(hook_fd)
    if result.returncode != 0:
        raise SystemExit(f"Project startup check failed with exit status {result.returncode}")
for relative in ("AGENTS.md", "AI_WORKFLOW.md", ".claude-memory.md", ".planning/STATE.md"):
    path = root / relative
    if path.is_symlink() or not path.is_file():
        raise SystemExit(f"Managed context file is missing or unsafe: {relative}")
PY
fi

# Read complete current files; never silently truncate instructions or restart state.
ROOT_DIR="$ROOT_DIR" python3 - <<'PY_CONTEXT'
import os
import stat
from pathlib import Path

root = Path(os.environ["ROOT_DIR"])
legacy = (root / ".agent-plus/legacy-adoption.json").exists()
files = ["AGENTS.md", "AI_AGENT_OUTPUT_POLICY.md", ".claude-memory.md", ".planning/STATE.md"]
packet = []
for relative in files:
    path = root / relative
    if legacy and relative in {".claude-memory.md", ".planning/STATE.md"} and not path.exists() and not path.is_symlink():
        continue
    if any(parent.is_symlink() for parent in path.parents if parent != root and root in parent.parents):
        raise SystemExit(f"Managed context parent is unsafe: {relative}")
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
        with os.fdopen(fd, "r", encoding="utf-8") as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                raise SystemExit(f"Managed context file is unsafe: {relative}")
            content = source.read()
    except (OSError, UnicodeError) as exc:
        raise SystemExit(f"Cannot read managed context: {relative}") from exc
    packet.append(f"## {relative}\n{content.rstrip()}\n")
packet.append("## Procedure references\nRead ESSENTIAL_WORK_PROTOCOL.md for implementation and verification. "
              "Read AI_WORKFLOW.md before model assignment, a formal chain, review, or unattended execution. "
              "Both remain binding. Read the exact active artifact named above.\n")
print("\n".join(packet))
PY_CONTEXT
