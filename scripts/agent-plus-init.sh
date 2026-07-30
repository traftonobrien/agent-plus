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

for control in AGENTS.md CLAUDE.md AI_WORKFLOW.md ESSENTIAL_WORK_PROTOCOL.md .claude-memory.md .agent-plus .planning scripts/ai-context.sh; do
  if [ -e "$TARGET_DIR/$control" ]; then
    printf 'Refusing to overwrite existing control: %s\n' "$control" >&2
    exit 1
  fi
done

if [ "$WITH_GITHUB_ACTIONS" = true ] && [ -e "$TARGET_DIR/.github/workflows/agent-plus-doctor.yml" ]; then
  printf '%s\n' 'Refusing to overwrite existing GitHub Action.' >&2
  exit 1
fi

cp -R "$ROOT_DIR/bootstrap/base/." "$TARGET_DIR/"
cp "$ROOT_DIR/bootstrap/profiles/$PROFILE/PROFILE.md" "$TARGET_DIR/.agent-plus/PROFILE.md"
cp "$ROOT_DIR/scripts/agent-plus-doctor.sh" "$TARGET_DIR/scripts/agent-plus-doctor.sh"
chmod +x "$TARGET_DIR/scripts/ai-context.sh" "$TARGET_DIR/scripts/agent-plus-doctor.sh"

TODAY=$(date +%F)
for state_file in "$TARGET_DIR/.claude-memory.md" "$TARGET_DIR/.planning/STATE.md"; do
  sed "s/YYYY-MM-DD/$TODAY/g" "$state_file" > "$state_file.tmp"
  mv "$state_file.tmp" "$state_file"
done

PROJECT_NAME=$(basename "$TARGET_DIR")
{
  printf 'project_name: "%s"\n' "$PROJECT_NAME"
  printf 'profile: "%s"\n' "$PROFILE"
  printf 'brain_note: "%s"\n' "$BRAIN_NOTE"
  printf '%s\n' 'data_classification: "private"'
  printf '%s\n' 'claim_ceiling: "future_prediction"'
} > "$TARGET_DIR/.agent-plus/project.yaml"

if [ "$WITH_GITHUB_ACTIONS" = true ]; then
  mkdir -p "$TARGET_DIR/.github/workflows"
  cp "$ROOT_DIR/bootstrap/github/workflows/agent-plus-doctor.yml" "$TARGET_DIR/.github/workflows/agent-plus-doctor.yml"
fi

printf 'Initialized Agent+ %s profile at %s\n' "$PROFILE" "$TARGET_DIR"
printf 'Next: cd "%s" && scripts/agent-plus-doctor.sh --target .\n' "$TARGET_DIR"
