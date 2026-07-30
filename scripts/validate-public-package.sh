#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT_DIR"

required_files='
README.md
LICENSE
CONTRIBUTING.md
AGENTS.md
CLAUDE.md
.claude-memory.md
AI_WORKFLOW.md
AI_AGENT_OUTPUT_POLICY.md
ESSENTIAL_WORK_PROTOCOL.md
.planning/PROJECT.md
.planning/ROADMAP.md
.planning/STATE.md
.planning/templates/ESSENTIAL-TASK.md
.planning/phases/01-public-example-research/01-01-PLAN.md
.planning/phases/01-public-example-research/01-01-EVALUATION.md
.planning/phases/01-public-example-research/01-01-INDEPENDENT-REVIEW.md
.planning/phases/01-public-example-research/01-01-BLOCK-RECORD.md
assets/agent-plus-system-map.png
assets/routing-work-by-authority.png
assets/verification-system.png
'

printf '%s\n' "$required_files" | while IFS= read -r file; do
  [ -z "$file" ] && continue
  [ -f "$file" ] || { printf 'Missing required file: %s\n' "$file" >&2; exit 1; }
done

for skill in skills/*/SKILL.md; do
  for section in '## Trigger' '## Purpose' '## Required inputs' '## Allowed actions' '## Required outputs' '## Acceptance checks' '## Handoff requirements' '## Explicit limits'; do
    grep -qF "$section" "$skill" || { printf 'Missing skill section: %s in %s\n' "$section" "$skill" >&2; exit 1; }
  done
done

if grep -R -n -E '/[U]sers/|/[L]ibrary/Application Support/|sk-[A-Za-z0-9]{20,}|AIza[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{20,}' \
  --include='*.md' --include='*.sh' .; then
  printf '%s\n' 'Public-safety scan failed.' >&2
  exit 1
fi

if grep -R -n -E '[[:blank:]]+$' --include='*.md' --include='*.sh' .; then
  printf '%s\n' 'Whitespace scan failed.' >&2
  exit 1
fi

python3 - <<'PY'
from pathlib import Path
import re
root = Path.cwd()
for path in root.rglob('*.md'):
    for raw in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        target = raw.split('#', 1)[0].strip('<>')
        if target and '://' not in target and not target.startswith('mailto:'):
            if not (path.parent / target).resolve().exists():
                raise SystemExit(f'Broken local link: {path.relative_to(root)} -> {raw}')
print('Internal Markdown links: PASS')
PY

printf '%s\n' 'Public package validation: PASS'
