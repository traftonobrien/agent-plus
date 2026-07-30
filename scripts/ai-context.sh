#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

printf '%s\n' '# Agent+ public context packet'
printf '%s\n' ''
for file in AGENTS.md AI_WORKFLOW.md .claude-memory.md .planning/STATE.md; do
  printf '%s\n' "## ${file}"
  sed -n '1,220p' "${ROOT_DIR}/${file}"
  printf '%s\n' ''
done
