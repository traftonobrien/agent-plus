#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

# Validate the fixed project-owned seam before producing any managed context.
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

printf '%s\n' '# Agent+ public context packet'
printf '%s\n' ''
if [ -e "$ROOT_DIR/.agent-plus/legacy-adoption.json" ] || [ -L "$ROOT_DIR/.agent-plus/legacy-adoption.json" ]; then
  CONTEXT_FILES='AGENTS.md AI_WORKFLOW.md'
  for optional_file in .claude-memory.md .planning/STATE.md; do
    if [ -e "$ROOT_DIR/$optional_file" ] || [ -L "$ROOT_DIR/$optional_file" ]; then
      [ -f "$ROOT_DIR/$optional_file" ] && [ ! -L "$ROOT_DIR/$optional_file" ] || {
        printf 'Managed context file is missing or unsafe: %s\n' "$optional_file" >&2
        exit 1
      }
      CONTEXT_FILES="$CONTEXT_FILES $optional_file"
    fi
  done
else
  CONTEXT_FILES='AGENTS.md AI_WORKFLOW.md .claude-memory.md .planning/STATE.md'
fi
for file in $CONTEXT_FILES; do
  printf '%s\n' "## ${file}"
  sed -n '1,220p' "${ROOT_DIR}/${file}"
  printf '%s\n' ''
done
