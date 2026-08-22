# Agent+ Discovery Integration Audit

Outcome: `PASS_WITH_FRESH_REVIEW_REQUIRED`

## Synchronization status

- Agent+ version: `0.2.0` maker worktree; no release action authorized or performed.
- Proving project: SECOND LOOK, used only for bounded metadata inventory. Its scientific state and
  project adapters did not move upstream.
- Canonical/local discovery skill: recursive diff is empty.
- Original upstream skills: installed `grill-me`, installed `grilling`, and the bundled MIT license
  match inspected commit `9c9f36ccd3995266cd675468af71639c8dde1ec5` byte-for-byte. The two skill
  files also match current upstream `main` at audit time.
- Current gate: deterministic integration checks pass; the previously required fresh behavioral
  review still blocks commit, push, tag, release, or announcement.

## Surfaces inspected

- Canonical and installed `agent-plus-discovery-grill` skill folders.
- Installed upstream `grill-me` and `grilling` skills.
- Attribution, upstream MIT license, OpenAI metadata, and discovery template.
- Agent+ router, README, integrated-tools guide, bootstrap guide, initializer, generated project
  instructions, memory, and state.
- Public-package validator and lifecycle tests.
- Curated Brain new-project, activation, and Agent Tooling pages.
- SECOND LOOK inventory metadata only. No baseball data, evidence, model, or scientific artifact was
  inspected or copied.

## Findings

### UPSTREAM_CANDIDATE — Conditional discovery route was incomplete

- **Evidence:** The README named discovery, but the shared router assumed an active contract, the
  generated project began at a contract-only BLOCK, and bootstrap/Brain start instructions told the
  user to draft a contract immediately.
- **Failure class:** An unclear idea could bypass the decision brief or be forced into a premature
  contract.
- **Change:** Router, generated project gate, bootstrap guide, initializer handoff, and curated Brain
  start pages now select discovery only when the idea is not contract-ready.
- **Acceptance check:** Generated-project lifecycle tests assert the discovery-or-contract gate and
  the public validator binds the router and bootstrap references.

### UPSTREAM_CANDIDATE — Discovery-specific package binding was absent

- **Evidence:** Generic skill-section validation did not require the discovery asset, attribution,
  license, OpenAI metadata, typed exits, router, or bootstrap route.
- **Failure class:** A package could pass validation while shipping an incomplete or uncredited
  discovery integration.
- **Change:** The public validator and lifecycle tests bind all named discovery files, attribution,
  license, typed states, router, and project-start route.
- **Acceptance check:** Public validation and all 49 tests pass.

### PROJECT_ADAPTER — SECOND LOOK remains past discovery

- **Evidence:** SECOND LOOK already has an accepted research question and active Phase 3 gate.
- **Why local:** Reopening discovery would relitigate accepted scientific authority and would not
  change the current F-16 next action.
- **Action:** None. No SECOND LOOK file was changed by this audit.

### PRIVATE_STATE — Project and conversation material excluded

- **Evidence:** The inventory scanner read hashes and metadata only.
- **Action:** No project memory, evidence, private path, transcript, model result, or scientific
  record moved into Agent+.

### NO_ACTION — Discovery skill and attribution already correct

- **Evidence:** Canonical and installed adaptation copies match. Original upstream skill and license
  hashes match their inspected source. Attribution distinguishes the derivative from Matt Pocock's
  originals and preserves the MIT notice.
- **Action:** No skill behavior or third-party byte was changed.

### NO_ACTION — External `grill-me` validator compatibility

- **Evidence:** OpenAI's current generic quick validator rejects upstream's unchanged
  `disable-model-invocation` frontmatter key. The separately installed Codex metadata exists, the
  skill is callable, and both pinned and current upstream use the same bytes.
- **Why no local patch:** Editing the third-party original would break the unchanged-source and
  attribution guarantee. This does not affect the Agent+ adaptation, which passes validation.
- **Repeat trigger:** Upstream changes the skill metadata or the OpenAI validator adds the legacy key.

## Validation evidence

- Public-package validator: PASS.
- Public unit tests: 49 PASS.
- Lifecycle tests: 4 PASS.
- Canonical/bootstrap anti-loop bindings: PASS.
- Internal public Markdown links: PASS.
- Canonical and installed discovery adaptation quick validation: PASS.
- Canonical/local discovery adaptation recursive diff: empty.
- Upstream pinned skill and license hashes: exact match.
- Targeted curated Brain links: PASS.
- Shell syntax and Python compilation for changed validator/test surfaces: PASS.

## Remaining blocker

One fresh behavioral and integration review must still exercise one-question flow, incremental
persistence, resume, unknown/evidence/prototype branches, typed exits, privacy, owner confirmation,
and research-contract handoff. Deterministic maker validation cannot certify those behaviors.

## Next action

Run that one fresh behavioral review against the integrated project-start route. Do not create a
separate review for the router, bootstrap, Brain pages, or validator.

## Restart

```sh
cd agent-plus && scripts/ai-context.sh
```
