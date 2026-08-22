#!/usr/bin/env sh
set -eu

DOCTOR_ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

# This function is also sourced by copied context scripts. Keep the legacy
# verifier in one place so every copied consumer enforces the same contract.
agent_plus_check_legacy_adoption() {
  [ "$#" -eq 1 ] || {
    printf '%s\n' 'Usage: agent_plus_check_legacy_adoption DIRECTORY' >&2
    return 2
  }
  TARGET_DIR="$1" python3 - <<'PY'
import hashlib
import json
import os
import stat
import subprocess
from pathlib import Path

root = Path(os.environ["TARGET_DIR"])
agent = root / ".agent-plus"
declaration_path = agent / "legacy-adoption.json"
managed_files = {
    "AGENTS.md",
    "CLAUDE.md",
    "AI_WORKFLOW.md",
    "AI_AGENT_OUTPUT_POLICY.md",
    "ESSENTIAL_WORK_PROTOCOL.md",
    ".cursor/rules/agent-plus-output.mdc",
    ".agent-plus/PROFILE.md",
    ".planning/templates/ESSENTIAL-TASK.md",
    "scripts/ai-context.sh",
    "scripts/anti_loop_guard.py",
    "scripts/interface_consumer_guard.py",
    "scripts/agent-plus-doctor.sh",
    "tests/test_interface_consumer_guard.py",
}

def no_duplicates(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError("duplicate JSON object key")
        value[key] = item
    return value

if agent.is_symlink() or not agent.is_dir():
    raise SystemExit("Agent+ legacy adoption directory is not a regular directory")
if declaration_path.is_symlink() or not declaration_path.is_file():
    raise SystemExit("Legacy adoption declaration must be a regular file")
try:
    declaration = json.loads(
        declaration_path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates
    )
except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
    raise SystemExit(f"Invalid legacy adoption declaration: {exc}") from exc
if not isinstance(declaration, dict):
    raise SystemExit("Invalid legacy adoption declaration")
if set(declaration) != {"schema_version", "mode", "profile", "startup_check_path"}:
    raise SystemExit("Invalid legacy adoption declaration fields")
if declaration.get("schema_version") != "agent-plus-legacy-adoption/v1":
    raise SystemExit("Unsupported legacy adoption declaration")
if declaration.get("mode") != "legacy-adopted":
    raise SystemExit("Invalid legacy adoption mode")
if declaration.get("profile") not in {"research", "product", "scouting"}:
    raise SystemExit("Invalid legacy adoption profile")
if declaration.get("startup_check_path") != ".agent-plus/project-startup-check.sh":
    raise SystemExit("Legacy adoption startup-check path is not fixed")

manifest_path = root / ".agent-plus" / "install-manifest.json"
if manifest_path.is_symlink() or not manifest_path.is_file():
    raise SystemExit("Legacy adoption manifest is missing or unsafe")
try:
    manifest = json.loads(
        manifest_path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates
    )
except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
    raise SystemExit(f"Invalid install manifest: {exc}") from exc
if not isinstance(manifest, dict):
    raise SystemExit("Invalid install manifest")
if set(manifest) != {
    "schema_version",
    "agent_plus_version",
    "profile",
    "source_repository",
    "managed_files",
}:
    raise SystemExit("Unsupported install manifest")
if manifest.get("schema_version") != "agent-plus-install/v1":
    raise SystemExit("Unsupported install manifest")
if manifest.get("source_repository") != "https://github.com/traftonobrien/agent-plus":
    raise SystemExit("Invalid Agent+ source identity")
if manifest.get("profile") != declaration["profile"]:
    raise SystemExit("Legacy adoption profile does not match install manifest")
managed = manifest.get("managed_files")
if not isinstance(managed, dict) or set(managed) != managed_files:
    raise SystemExit("Install manifest managed-file set is not exact")
for relative, expected in managed.items():
    if not isinstance(expected, str):
        raise SystemExit(f"Invalid managed digest: {relative}")
    if len(expected) != 64 or any(character not in "0123456789abcdef" for character in expected):
        raise SystemExit(f"Invalid managed digest: {relative}")
    path = root / relative
    if path.is_symlink() or not path.is_file():
        raise SystemExit(f"Unsafe or missing managed file: {relative}")
    try:
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise SystemExit(f"Cannot read managed file: {relative}") from exc
    if actual != expected:
        raise SystemExit(f"Managed file drift: {relative}")

hook = root / ".agent-plus" / "project-startup-check.sh"
try:
    hook_fd = os.open(
        hook,
        os.O_RDONLY
        | os.O_NONBLOCK
        | os.O_NOFOLLOW
        | getattr(os, "O_CLOEXEC", 0),
    )
except OSError as exc:
    raise SystemExit("Legacy adoption requires the fixed project startup check") from exc
try:
    details = os.fstat(hook_fd)
    if not stat.S_ISREG(details.st_mode):
        raise SystemExit("Project startup check must be a regular file")
    if not details.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
        raise SystemExit("Project startup check must be executable")
    try:
        result = subprocess.run(
            ["/bin/sh", f"/dev/fd/{hook_fd}"],
            cwd=root,
            check=False,
            pass_fds=(hook_fd,),
        )
    except OSError as exc:
        raise SystemExit("Cannot execute project startup check") from exc
finally:
    os.close(hook_fd)
if result.returncode != 0:
    raise SystemExit(f"Project startup check failed with exit status {result.returncode}")
PY
}

if [ "${AGENT_PLUS_DOCTOR_SOURCE_ONLY-}" = '1' ]; then
  return 0 2>/dev/null || exit 0
fi

# The canonical checkout routes doctor through the Python lifecycle manager. A
# copied project doctor has no canonical manager beside it and uses the
# standalone checks below.
if [ "${AGENT_PLUS_DOCTOR_FALLBACK-}" != '1' ] && [ -f "$DOCTOR_ROOT_DIR/scripts/agent_plus_manager.py" ] && [ -f "$DOCTOR_ROOT_DIR/bootstrap/base/scripts/ai-context.sh" ]; then
  exec python3 "$DOCTOR_ROOT_DIR/scripts/agent_plus_manager.py" doctor "$@"
fi

usage() {
  printf '%s\n' 'Usage: scripts/agent-plus-doctor.sh --target DIRECTORY'
  exit 2
}

TARGET_DIR=''
while [ "$#" -gt 0 ]; do
  case "$1" in
    --target) TARGET_DIR=${2-}; shift 2 ;;
    *) usage ;;
  esac
done

[ -n "$TARGET_DIR" ] || usage
[ -d "$TARGET_DIR" ] || { printf 'Target directory does not exist: %s\n' "$TARGET_DIR" >&2; exit 1; }
TARGET_DIR=$(cd "$TARGET_DIR" && pwd)

# Legacy-adopted projects intentionally do not need initializer-only examples.
# Keep this route strict: the declaration, manifest, managed regular files, and
# required fixed startup seam must all be valid before doctor can pass.
if [ -e "$TARGET_DIR/.agent-plus/legacy-adoption.json" ] || [ -L "$TARGET_DIR/.agent-plus/legacy-adoption.json" ]; then
  agent_plus_check_legacy_adoption "$TARGET_DIR"
  printf 'Agent+ doctor: PASS (%s) [legacy-adopted]\n' "$TARGET_DIR"
  exit 0
fi

TARGET_DIR="$TARGET_DIR" python3 - <<'PY'
import os
import stat
from pathlib import Path

hook = Path(os.environ["TARGET_DIR"]) / ".agent-plus" / "project-startup-check.sh"
if hook.exists() or hook.is_symlink():
    details = hook.lstat()
    if stat.S_ISLNK(details.st_mode) or not stat.S_ISREG(details.st_mode):
        raise SystemExit("Project startup check must be a regular file")
    if not details.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
        raise SystemExit("Project startup check must be executable")
PY

for file in AGENTS.md CLAUDE.md AI_WORKFLOW.md AI_AGENT_OUTPUT_POLICY.md ESSENTIAL_WORK_PROTOCOL.md .cursor/rules/agent-plus-output.mdc .claude-memory.md .agent-plus/project.yaml .agent-plus/PROFILE.md .agent-plus/PROJECT.md .agent-plus/install-manifest.json .agent-plus/claim-evidence-register.md .agent-plus/engineering-boundaries.json .agent-plus/engineering-closure-example.json .agent-plus/interface-consumer-closure-example.json scripts/anti_loop_guard.py scripts/interface_consumer_guard.py tests/test_interface_consumer_guard.py .planning/PROJECT.md .planning/ROADMAP.md .planning/STATE.md .planning/templates/ESSENTIAL-TASK.md scripts/ai-context.sh; do
  [ -f "$TARGET_DIR/$file" ] || { printf 'Missing required control: %s\n' "$file" >&2; exit 1; }
done

python3 "$TARGET_DIR/scripts/anti_loop_guard.py" \
  --ledger "$TARGET_DIR/.agent-plus/engineering-boundaries.json" \
  --packet "$TARGET_DIR/.agent-plus/engineering-closure-example.json" >/dev/null
python3 "$TARGET_DIR/scripts/interface_consumer_guard.py" \
  --root "$TARGET_DIR" \
  --receipt "$TARGET_DIR/.agent-plus/interface-consumer-closure-example.json" >/dev/null

grep -qE '^Updated: [0-9]{4}-[0-9]{2}-[0-9]{2}$' "$TARGET_DIR/.claude-memory.md" || {
  printf '%s\n' 'Hot memory must contain an ISO Updated date.' >&2
  exit 1
}
grep -qE '^profile: "(research|product|scouting)"$' "$TARGET_DIR/.agent-plus/project.yaml" || {
  printf '%s\n' 'Project profile is missing or invalid.' >&2
  exit 1
}
grep -q '^claim_ceiling:' "$TARGET_DIR/.agent-plus/project.yaml" || {
  printf '%s\n' 'Project claim ceiling is missing.' >&2
  exit 1
}

if find "$TARGET_DIR" \
  -path "$TARGET_DIR/.git" -prune -o \
  -path "$TARGET_DIR/node_modules" -prune -o \
  -path "$TARGET_DIR/.venv" -prune -o \
  -type f \( -name '*.md' -o -name '*.sh' -o -name '*.yml' -o -name '*.yaml' \) -print0 \
  | xargs -0 grep -n -E '/[U]sers/|/[L]ibrary/Application Support/|sk-[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}'; then
  printf '%s\n' 'Safety scan failed: remove a local path or apparent credential.' >&2
  exit 1
fi

TARGET_DIR="$TARGET_DIR" python3 - <<'PY'
from pathlib import Path
import os, re
root = Path(os.environ['TARGET_DIR'])
for path in root.rglob('*.md'):
    if any(part in {'.git', 'node_modules', '.venv'} for part in path.parts):
        continue
    for raw in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        target = raw.split('#', 1)[0].strip('<>')
        if target and '://' not in target and not target.startswith('mailto:'):
            if not (path.parent / target).resolve().exists():
                raise SystemExit(f'Broken local link: {path.relative_to(root)} -> {raw}')
print('Internal Markdown links: PASS')
PY

printf 'Agent+ doctor: PASS (%s)\n' "$TARGET_DIR"
