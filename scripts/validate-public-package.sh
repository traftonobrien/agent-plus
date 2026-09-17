#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT_DIR"

required_files='
README.md
VERSION
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
bootstrap/base/AGENTS.md
bootstrap/base/CLAUDE.md
bootstrap/base/AI_AGENT_OUTPUT_POLICY.md
bootstrap/base/AI_WORKFLOW.md
bootstrap/base/ESSENTIAL_WORK_PROTOCOL.md
bootstrap/base/.claude-memory.md
bootstrap/base/.agent-plus/project.yaml
bootstrap/base/.agent-plus/PROJECT.md
bootstrap/base/.agent-plus/claim-evidence-register.md
bootstrap/base/.agent-plus/engineering-boundaries.json
bootstrap/base/.agent-plus/engineering-closure-example.json
bootstrap/base/.agent-plus/active-chain-example.json
bootstrap/base/.agent-plus/interface-consumer-closure-example.json
bootstrap/base/.planning/PROJECT.md
bootstrap/base/.planning/ROADMAP.md
bootstrap/base/.planning/STATE.md
bootstrap/base/.planning/templates/ESSENTIAL-TASK.md
bootstrap/base/scripts/ai-context.sh
bootstrap/base/scripts/active_chain_guard.py
bootstrap/base/scripts/anti_loop_guard.py
bootstrap/base/scripts/interface_consumer_guard.py
bootstrap/base/tests/test_interface_consumer_guard.py
bootstrap/base/.cursor/rules/agent-plus-output.mdc
bootstrap/profiles/research/PROFILE.md
bootstrap/profiles/product/PROFILE.md
bootstrap/profiles/scouting/PROFILE.md
bootstrap/github/workflows/agent-plus-doctor.yml
docs/bootstrap-a-baseball-project.md
docs/active-chain-capsule.md
docs/attribution/implementation-subtraction.md
docs/attribution/DIETRICH-GEBERT-LICENSE.txt
docs/project-integration-and-upstream.md
docs/release-candidate-verification.md
scripts/agent-plus
scripts/agent-plus-init.sh
scripts/agent-plus-doctor.sh
scripts/agent_plus_manager.py
tests/test_agent_plus_lifecycle.py
tests/test_agent_plus_legacy_adoption.py
tests/test_outcome_audit.py
skills/agent-plus/SKILL.md
skills/outcome-audit/SKILL.md
skills/outcome-audit/outcome_audit.py
skills/agent-plus-sync/SKILL.md
skills/agent-plus-sync/agents/openai.yaml
skills/agent-plus-discovery-grill/SKILL.md
skills/agent-plus-discovery-grill/agents/openai.yaml
skills/agent-plus-discovery-grill/assets/PROJECT-DISCOVERY.md
skills/agent-plus-discovery-grill/references/attribution.md
skills/agent-plus-discovery-grill/references/MATT-POCOCK-LICENSE.txt
skills/editorial-pass/SKILL.md
skills/editorial-pass/references/editorial-method.md
skills/editorial-pass/references/attribution.md
skills/editorial-pass/references/PETER-YANG-LICENSE.txt
skills/editorial-pass/references/EHMO-LICENSE.txt
skills/editorial-pass/references/MATT-SILVERLOCK-LICENSE.txt
scripts/editorial_preservation_check.py
scripts/anti_loop_guard.py
scripts/active_chain_guard.py
scripts/interface_consumer_guard.py
scripts/verify_release_candidate.py
tests/test_active_chain_guard.py
tests/test_anti_loop_guard.py
tests/test_interface_consumer_guard.py
tests/test_release_candidate_verifier.py
tests/test_editorial_pass.py
tests/test_workflow_defaults.py
tests/test_astra_workspace.py
docs/astra-workspace-tuning.md
docs/astra-host-setup.md
docs/releases/0.4.1.md
.agent-plus/interface-consumer-closure-example.json
.agent-plus/active-chain-example.json
.agent-plus/release-candidate.json
assets/agent-plus-system-map.png
assets/routing-work-by-authority.png
assets/verification-system.png
.cursor/rules/agent-plus-output.mdc
'

printf '%s\n' "$required_files" | while IFS= read -r file; do
  [ -z "$file" ] && continue
  [ -f "$file" ] || { printf 'Missing required file: %s\n' "$file" >&2; exit 1; }
done

for script in scripts/*.sh bootstrap/base/scripts/*.sh; do
  sh -n "$script"
done

python3 -m unittest discover -s tests -p 'test_*.py' >/dev/null
python3 scripts/anti_loop_guard.py \
  --ledger .agent-plus/engineering-boundaries.json \
  --packet .agent-plus/engineering-closure-example.json >/dev/null
python3 bootstrap/base/scripts/anti_loop_guard.py \
  --ledger bootstrap/base/.agent-plus/engineering-boundaries.json \
  --packet bootstrap/base/.agent-plus/engineering-closure-example.json >/dev/null
python3 scripts/active_chain_guard.py \
  --root . \
  --capsule .agent-plus/active-chain-example.json \
  --mode closeout >/dev/null
python3 bootstrap/base/scripts/active_chain_guard.py \
  --root bootstrap/base \
  --capsule bootstrap/base/.agent-plus/active-chain-example.json \
  --mode closeout >/dev/null
python3 scripts/interface_consumer_guard.py \
  --root . \
  --receipt .agent-plus/interface-consumer-closure-example.json >/dev/null

python3 - <<'PY'
from hashlib import sha256
from pathlib import Path

root = Path.cwd()
for relative in (
    "AI_AGENT_OUTPUT_POLICY.md",
    ".cursor/rules/agent-plus-output.mdc",
    "scripts/anti_loop_guard.py",
    "scripts/active_chain_guard.py",
    "scripts/interface_consumer_guard.py",
    ".planning/templates/ESSENTIAL-TASK.md",
    "ESSENTIAL_WORK_PROTOCOL.md",
):
    canonical = sha256((root / relative).read_bytes()).hexdigest()
    bootstrap = sha256((root / "bootstrap/base" / relative).read_bytes()).hexdigest()
    if canonical != bootstrap:
        raise SystemExit(f"Guard binding mismatch: {relative}")
print("Canonical/bootstrap guard bindings: PASS")
PY

for skill in skills/*/SKILL.md; do
  for section in '## Trigger' '## Purpose' '## Required inputs' '## Allowed actions' '## Required outputs' '## Acceptance checks' '## Handoff requirements' '## Explicit limits'; do
    grep -qF "$section" "$skill" || { printf 'Missing skill section: %s in %s\n' "$section" "$skill" >&2; exit 1; }
  done
done

grep -qF '$agent-plus-discovery-grill' skills/agent-plus/SKILL.md || {
  printf '%s\n' 'Agent+ router does not expose the discovery route.' >&2
  exit 1
}
grep -qF '$agent-plus-discovery-grill' docs/bootstrap-a-baseball-project.md || {
  printf '%s\n' 'Bootstrap guide does not expose the discovery route.' >&2
  exit 1
}
grep -qF '$editorial-pass' skills/agent-plus/SKILL.md || {
  printf '%s\n' 'Agent+ router does not expose the editorial route.' >&2
  exit 1
}
grep -qF '$editorial-pass' docs/bootstrap-a-baseball-project.md || {
  printf '%s\n' 'Bootstrap guide does not expose the editorial route.' >&2
  exit 1
}
grep -qF '$agent-plus-sync' skills/agent-plus/SKILL.md || {
  printf '%s\n' 'Agent+ router does not expose the sync route.' >&2
  exit 1
}
grep -qF '$agent-plus-sync' docs/bootstrap-a-baseball-project.md || {
  printf '%s\n' 'Bootstrap guide does not expose the sync route.' >&2
  exit 1
}
grep -qF '$outcome-audit' skills/agent-plus/SKILL.md || {
  printf '%s\n' 'Agent+ router does not expose the outcome-audit route.' >&2
  exit 1
}
grep -qF 'outcome-audit' docs/bootstrap-a-baseball-project.md || {
  printf '%s\n' 'Bootstrap guide does not expose the outcome-audit route.' >&2
  exit 1
}
grep -qF 'scripts/agent-plus adopt' README.md || {
  printf '%s\n' 'README does not expose the legacy-adoption route.' >&2
  exit 1
}
grep -qF 'python3 scripts/verify_release_candidate.py' README.md || {
  printf '%s\n' 'README does not expose the fixed release-candidate verifier.' >&2
  exit 1
}
grep -qF 'python3 scripts/verify_release_candidate.py' docs/release-candidate-verification.md || {
  printf '%s\n' 'Release-candidate documentation does not expose the fixed command.' >&2
  exit 1
}
python3 - <<'PY'
import importlib.util
from pathlib import Path

root = Path.cwd()
spec = importlib.util.spec_from_file_location("release_candidate", root / "scripts/verify_release_candidate.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.load_config(root)
assert module.SOURCE_COMMANDS == {"ls-tree", "cat-file", "ls-files"}
assert module.MYPY_VERSION == "2.3.1" and module.RUFF_VERSION == "0.16.5"
print("Detached release-candidate configuration and toolchain: PASS")
PY
grep -qF 'scripts/agent-plus adopt' docs/bootstrap-a-baseball-project.md || {
  printf '%s\n' 'Bootstrap guide does not expose the legacy-adoption route.' >&2
  exit 1
}
grep -qF 'legacy-adoption.json' skills/agent-plus-sync/SKILL.md || {
  printf '%s\n' 'Sync guidance does not describe legacy adoption.' >&2
  exit 1
}
grep -qF 'project-startup-check.sh' bootstrap/base/scripts/ai-context.sh || {
  printf '%s\n' 'Bootstrap context does not expose the fixed startup seam.' >&2
  exit 1
}
grep -qF 'legacy-adoption.json' scripts/agent_plus_manager.py || {
  printf '%s\n' 'Lifecycle manager does not expose legacy adoption.' >&2
  exit 1
}
for commit in \
  d30eddb9e04562234f2070b5ee63ca4649d9a05e \
  b33718bb9283c11b09567dc714f92d90ffb7bd16 \
  36b4a7e8d41b55ff5dff568a22f62bb0214967df; do
  grep -qF "$commit" skills/editorial-pass/references/attribution.md || {
    printf '%s\n' "Editorial attribution is missing inspected commit: $commit" >&2
    exit 1
  }
done
grep -qF '2ed6c52c9d7e5e56942508591085fd45dea277d3f' \
  docs/attribution/implementation-subtraction.md || {
  printf '%s\n' 'Implementation subtraction attribution is missing its inspected commit.' >&2
  exit 1
}
grep -qF '9c9f36ccd3995266cd675468af71639c8dde1ec5' \
  skills/agent-plus-discovery-grill/references/attribution.md || {
  printf '%s\n' 'Discovery attribution is missing its inspected upstream commit.' >&2
  exit 1
}
grep -qF 'Copyright (c) 2026 Matt Pocock' \
  skills/agent-plus-discovery-grill/references/MATT-POCOCK-LICENSE.txt || {
  printf '%s\n' 'Discovery attribution license is incomplete.' >&2
  exit 1
}

python3 scripts/public_safety_scan.py

# Publication text checks use the same inventory as public_safety_scan.py.
python3 - <<'PY_TEXT'
from pathlib import Path
import re
import subprocess

root = Path.cwd()
result = subprocess.run(
    ["git", "-C", str(root), "ls-files", "-co", "--exclude-standard", "-z"],
    capture_output=True,
    check=True,
)
names = sorted(set(result.stdout.decode("utf-8").split("\0")) - {""})
published = {root / name for name in names}
for name in names:
    path = root / name
    if path.suffix not in {".md", ".sh"}:
        continue
    text = path.read_text(encoding="utf-8")
    if re.search(r"[ \t]+$", text, re.MULTILINE):
        raise SystemExit(f"Whitespace scan failed: {name}")
    if path.suffix != ".md":
        continue
    for raw in re.findall(r'\]\(([^)]+)\)', text):
        target = raw.split('#', 1)[0].strip('<>')
        if target and '://' not in target and not target.startswith('mailto:'):
            resolved = (path.parent / target).resolve()
            shipped = resolved in published or (
                resolved.is_dir() and any(resolved in item.parents for item in published)
            )
            if not resolved.exists() or not shipped:
                raise SystemExit(f'Broken public link: {name} -> {raw}')
print('Public Markdown and shell whitespace: PASS')
print('Internal Markdown links: PASS')
PY_TEXT

printf '%s\n' 'Public package validation: PASS'
