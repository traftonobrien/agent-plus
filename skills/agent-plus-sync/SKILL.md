---
name: agent-plus-sync
description: Audit and safely synchronize an installed Agent+ project against an exact official release without overwriting project-owned state.
---

# Agent+ Sync

## Trigger

Use when the user asks whether Agent+ is current, requests an Agent+ calibration check, or wants to
update an existing Agent+ project from an official release.

## Purpose

Audit first. Synchronize only after explicit authorization. Use the canonical transactional
lifecycle instead of copying control files by hand.

For an existing project that has no Agent+ manifest, use the separate exact-byte admission route:
`scripts/agent-plus adopt --target "/absolute/path/to/project" --profile research|product|scouting`.
Adoption is not synchronization. It writes `.agent-plus/legacy-adoption.json` only after all
managed bytes match the current canonical source and never overwrites project-owned state.

## Required inputs

- The target project root. Use the current Git root only when it is unambiguous.
- An exact official Agent+ release tag or a clean checkout at that tag.
- The requested mode: `audit`, `sync`, or `verify`. Default to read-only `audit`.

## Allowed actions

### Audit

1. Read the target's `.agent-plus/install-manifest.json`, `.agent-plus/PROFILE.md`, and
   `.agent-plus/PROJECT.md` when present.
2. If the manifest is absent and the target declares `.agent-plus/legacy-adoption.json`, validate
   that declaration and the fixed required `.agent-plus/project-startup-check.sh` seam. A malformed
   or partial declaration is `BLOCK`; do not infer adoption from directory names.
3. Confirm that the manifest names `https://github.com/traftonobrien/agent-plus` as its source.
4. Resolve an exact stable Agent+ tag. Do not use an untagged branch or dirty checkout as release
   authority.
5. From that release checkout, run:

   ```sh
   scripts/agent-plus status --target "/absolute/path/to/project"
   scripts/agent-plus doctor --target "/absolute/path/to/project"
   ```

6. Classify the result as `CURRENT`, `UPDATE_AVAILABLE`, `LOCAL_DRIFT`, `PENDING_RECOVERY`, or
   `BLOCK`.
7. Report installed version, available version, profile, source tag, and the exact next command.

### Sync

1. Require explicit owner authorization that names the target and exact release tag.
2. Stop if audit found local drift, a pending transaction, an invalid manifest, an untrusted source,
   or a dirty release checkout.
3. Before mutation, hash the project-owned control files that exist:
   `.agent-plus/PROJECT.md`, `.claude-memory.md`, `.planning/STATE.md`, and
   `.agent-plus/engineering-boundaries.json`.
4. Run one authorized transaction from the exact release checkout:

   ```sh
   scripts/agent-plus upgrade --target "/absolute/path/to/project"
   ```

5. If the command fails, stop. The authorization is spent. Report the durable journal and exact
   `recover --target` command. Do not recover, retry, copy files, or fall back in the same chain.
6. If the command succeeds, continue directly to verification.

### Verify

1. Run `status` and `doctor` from the same exact release checkout.
2. Require `AGENT_PLUS_CURRENT` at the requested version and no pending transaction.
3. Recheck the hashes captured before sync. Project-owned controls must be unchanged.
4. Read the project profile and local project rules. Report calibration gaps without editing them.
5. Record the installed version, release tag or commit, commands, results, preserved hashes, limits,
   and one next action in project-local state.

## Required outputs

- Mode and target root.
- Installed and available Agent+ versions.
- Exact release tag or commit used as authority.
- Status classification and doctor result.
- Local drift, pending recovery, or calibration findings.
- Mutation receipt and preservation checks when sync was authorized.
- Exact next action or typed `BLOCK`.

## Acceptance checks

- Release authority is an exact official tag from the canonical repository.
- Audit occurs before any mutation.
- Sync has explicit target-and-version authorization.
- The canonical lifecycle command performs the update.
- Project-owned controls remain byte-identical.
- Post-sync status is `AGENT_PLUS_CURRENT`, and doctor passes.
- No fallback or same-chain recovery follows an error.

## Handoff requirements

Record current state, completed checks, blocker, next action, installed version, release authority,
and exact restart command. Keep consumer-project state in the consumer project.

## Explicit limits

- This skill does not treat `main`, an untagged commit, or a dirty checkout as release authority.
- It does not overwrite local drift or project-owned memory, plans, evidence, data, or ledgers.
- It does not authorize Git changes, release publication, scientific work, modeling, or promotion.
- It does not copy consumer-project state back into canonical Agent+.
- It does not claim calibration for surfaces that were not checked.
