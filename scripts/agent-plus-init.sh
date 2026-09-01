#!/usr/bin/env sh
set -eu

usage() {
  printf '%s\n' 'Usage: scripts/agent-plus-init.sh --target DIRECTORY --profile research|product|scouting --brain-note NOTE [--github-actions]'
  exit 2
}

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
TARGET_DIR=''
PROFILE=''
BRAIN_NOTE=''
WITH_GITHUB_ACTIONS=false

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target) TARGET_DIR=${2-}; shift 2 ;;
    --profile) PROFILE=${2-}; shift 2 ;;
    --brain-note) BRAIN_NOTE=${2-}; shift 2 ;;
    --github-actions) WITH_GITHUB_ACTIONS=true; shift ;;
    *) usage ;;
  esac
done

[ -n "$TARGET_DIR" ] && [ -n "$PROFILE" ] && [ -n "$BRAIN_NOTE" ] || usage
[ -d "$TARGET_DIR" ] || { printf 'Target directory does not exist: %s\n' "$TARGET_DIR" >&2; exit 1; }
case "$PROFILE" in research|product|scouting) ;; *) printf 'Unknown profile: %s\n' "$PROFILE" >&2; exit 1;; esac

TARGET_DIR=$(cd "$TARGET_DIR" && pwd)
case "$TARGET_DIR" in /|"$HOME") printf 'Refusing broad target: %s\n' "$TARGET_DIR" >&2; exit 1;; esac

for directory in scripts tests; do
  if [ -L "$TARGET_DIR/$directory" ]; then
    printf 'Refusing symlinked target directory: %s\n' "$directory" >&2
    exit 1
  fi
done
if [ "$WITH_GITHUB_ACTIONS" = true ] && {
  [ -L "$TARGET_DIR/.github" ] || [ -L "$TARGET_DIR/.github/workflows" ];
}; then
  printf '%s\n' 'Refusing symlinked GitHub workflow directory.' >&2
  exit 1
fi

for control in AGENTS.md CLAUDE.md AI_WORKFLOW.md AI_AGENT_OUTPUT_POLICY.md ESSENTIAL_WORK_PROTOCOL.md .cursor .claude-memory.md .agent-plus .planning scripts/ai-context.sh scripts/anti_loop_guard.py scripts/interface_consumer_guard.py scripts/agent-plus-doctor.sh tests/test_interface_consumer_guard.py; do
  if [ -e "$TARGET_DIR/$control" ] || [ -L "$TARGET_DIR/$control" ]; then
    printf 'Refusing to overwrite existing control: %s\n' "$control" >&2
    exit 1
  fi
done

if [ "$WITH_GITHUB_ACTIONS" = true ] && {
  [ -e "$TARGET_DIR/.github/workflows/agent-plus-doctor.yml" ] ||
  [ -L "$TARGET_DIR/.github/workflows/agent-plus-doctor.yml" ];
}; then
  printf '%s\n' 'Refusing to overwrite existing GitHub Action.' >&2
  exit 1
fi

STAGE_DIR=$(mktemp -d "$TARGET_DIR/.agent-plus-init.XXXXXX")
COMMITTED=''
cleanup() {
  exit_code=$?
  trap - EXIT HUP INT TERM
  if [ "$exit_code" -ne 0 ]; then
    for item in $COMMITTED; do
      if [ -e "$TARGET_DIR/$item" ]; then
        mkdir -p "$(dirname "$STAGE_DIR/$item")"
        mv "$TARGET_DIR/$item" "$STAGE_DIR/$item" || true
      fi
    done
  fi
  rm -rf "$STAGE_DIR"
  exit "$exit_code"
}
trap cleanup EXIT
trap 'exit 130' HUP INT TERM

# Build every control in a private staging directory. The target is changed only
# after all copies, substitutions, manifest checks, and optional files succeed.
cp -R "$ROOT_DIR/bootstrap/base/." "$STAGE_DIR/"
cp "$ROOT_DIR/bootstrap/profiles/$PROFILE/PROFILE.md" "$STAGE_DIR/.agent-plus/PROFILE.md"
cp "$ROOT_DIR/scripts/agent-plus-doctor.sh" "$STAGE_DIR/scripts/agent-plus-doctor.sh"
chmod +x "$STAGE_DIR/scripts/ai-context.sh" "$STAGE_DIR/scripts/agent-plus-doctor.sh"

TODAY=$(date +%F)
for state_file in "$STAGE_DIR/.claude-memory.md" "$STAGE_DIR/.planning/STATE.md"; do
  sed "s/YYYY-MM-DD/$TODAY/g" "$state_file" > "$state_file.tmp"
  mv "$state_file.tmp" "$state_file"
done

PROJECT_NAME=$(basename "$TARGET_DIR")
PROJECT_NAME="$PROJECT_NAME" PROFILE="$PROFILE" BRAIN_NOTE="$BRAIN_NOTE" \
  python3 - "$STAGE_DIR/.agent-plus/project.yaml" <<'PY'
import json
import os
import sys
from pathlib import Path

path = Path(sys.argv[1])
values = {
    "project_name": os.environ["PROJECT_NAME"],
    "profile": os.environ["PROFILE"],
    "brain_note": os.environ["BRAIN_NOTE"],
    "data_classification": "private",
    "claim_ceiling": "future_prediction",
}
path.write_text(
    "".join(f"{key}: {json.dumps(value, ensure_ascii=False)}\n" for key, value in values.items()),
    encoding="utf-8",
)
PY

python3 "$ROOT_DIR/scripts/agent_plus_manager.py" record \
  --target "$STAGE_DIR" \
  --profile "$PROFILE"

if [ "$WITH_GITHUB_ACTIONS" = true ]; then
  mkdir -p "$STAGE_DIR/.github/workflows"
  cp "$ROOT_DIR/bootstrap/github/workflows/agent-plus-doctor.yml" "$STAGE_DIR/.github/workflows/agent-plus-doctor.yml"
fi

# Commit by exact path. Existing project-owned directories remain in place.
for control in AGENTS.md CLAUDE.md AI_WORKFLOW.md AI_AGENT_OUTPUT_POLICY.md ESSENTIAL_WORK_PROTOCOL.md .claude-memory.md; do
  mv "$STAGE_DIR/$control" "$TARGET_DIR/$control"
  COMMITTED="$COMMITTED $control"
done
mv "$STAGE_DIR/.cursor" "$TARGET_DIR/.cursor"
COMMITTED="$COMMITTED .cursor"
mv "$STAGE_DIR/.agent-plus" "$TARGET_DIR/.agent-plus"
COMMITTED="$COMMITTED .agent-plus"
mv "$STAGE_DIR/.planning" "$TARGET_DIR/.planning"
COMMITTED="$COMMITTED .planning"
mkdir -p "$TARGET_DIR/scripts"
for control in ai-context.sh active_chain_guard.py anti_loop_guard.py interface_consumer_guard.py agent-plus-doctor.sh; do
  mv "$STAGE_DIR/scripts/$control" "$TARGET_DIR/scripts/$control"
  COMMITTED="$COMMITTED scripts/$control"
done
mkdir -p "$TARGET_DIR/tests"
mv "$STAGE_DIR/tests/test_interface_consumer_guard.py" \
  "$TARGET_DIR/tests/test_interface_consumer_guard.py"
COMMITTED="$COMMITTED tests/test_interface_consumer_guard.py"
if [ "$WITH_GITHUB_ACTIONS" = true ]; then
  mkdir -p "$TARGET_DIR/.github/workflows"
  mv "$STAGE_DIR/.github/workflows/agent-plus-doctor.yml" \
    "$TARGET_DIR/.github/workflows/agent-plus-doctor.yml"
  COMMITTED="$COMMITTED .github/workflows/agent-plus-doctor.yml"
fi

COMMITTED=''
rm -rf "$STAGE_DIR"
trap - EXIT HUP INT TERM

printf 'Initialized Agent+ %s profile at %s\n' "$PROFILE" "$TARGET_DIR"
printf 'Next: cd "%s" && scripts/agent-plus-doctor.sh --target .\n' "$TARGET_DIR"
printf '%s\n' 'Then: use $agent-plus-discovery-grill if the decision is unclear; otherwise draft the first contract.'
