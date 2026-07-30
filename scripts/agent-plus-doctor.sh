#!/usr/bin/env sh
set -eu

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

for file in AGENTS.md CLAUDE.md AI_WORKFLOW.md ESSENTIAL_WORK_PROTOCOL.md .claude-memory.md .agent-plus/project.yaml .agent-plus/PROFILE.md .agent-plus/claim-evidence-register.md .planning/PROJECT.md .planning/ROADMAP.md .planning/STATE.md .planning/templates/ESSENTIAL-TASK.md scripts/ai-context.sh; do
  [ -f "$TARGET_DIR/$file" ] || { printf 'Missing required control: %s\n' "$file" >&2; exit 1; }
done

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
