# Agent+ proving-system audit and maker receipt

Date: 2026-08-30

Outcome: `PASS` at the maker and deterministic-evaluator boundary. Fresh independent review and
release remain `BLOCKED` until separately authorized.

## Synchronization status

- Released Agent+ version: `0.3.0`.
- Proving project: registered local `second-look` consumer.
- Consumer synchronization: not performed.
- Reusable findings implemented: four connected generic controls in one bundle.
- Private or project-specific material copied upstream: none.

## Exact audit surface

- Owner-named current and older proving-task histories, inspected locally only.
- Proving controls: `AGENTS.md`, `.agent-plus/PROJECT.md`, `.claude-memory.md`,
  `.planning/STATE.md`, `.agent-plus/active-chain.json`, and `scripts/active_chain_guard.py`.
- Canonical controls: `AGENTS.md`, `AI_WORKFLOW.md`, `ESSENTIAL_WORK_PROTOCOL.md`, the research
  profile, essential-task template, validators, bootstrap copies, docs, and focused tests.
- Metadata-only system inventory: 197 proving surfaces. No baseball data, model, notebook, result,
  scientific receipt, or saved artifact was inspected through the inventory.

## Findings

### `UPSTREAM_CANDIDATE` — active-chain closeout control

The proving system used one small chain capsule to keep stages ordered and prevent premature
closeout. Canonical Agent+ had the stage contract in prose but no deterministic route validator.

Implemented public boundary:

- `scripts/active_chain_guard.py` and its byte-identical bootstrap copy.
- Closed `agent-plus-active-chain/v1` schema.
- Live safe authority references by repository-relative path.
- Ordered active-stage routing and terminal `PASS`, `NULL`, or `BLOCK` validation.
- Completed-stage evidence requirements.
- Rejection of early closeout, unknown fields, duplicate keys, unsafe paths, invalid stage order,
  and a third local repair after two same-interface failures.

### `UPSTREAM_CANDIDATE` — exact target-graph cost isolation

The proving system succeeded when it proved that expensive ancestors were current and ran only the
smallest outdated downstream target. Canonical Agent+ already required cost-separated targets but
did not require the pre-run graph receipt.

Implemented public boundary:

- Record current and outdated named targets before an expensive run.
- Run the smallest named target that reaches the decision endpoint.
- Reuse current expensive ancestors.
- Treat a downstream reset as distinct only when graph evidence proves it cannot reach an exhausted
  upstream interface.

### `UPSTREAM_CANDIDATE` — live authority instead of copied state

The proving system kept policy, contracts, code, and deterministic evidence authoritative while
memory, planning state, Brain notes, and transcripts only routed work.

Implemented public boundary:

- Chain capsules and task packets reference live repository files.
- They do not copy scientific values, schemas, thresholds, hashes, or artifact identities.
- Fresh sessions resume from durable state and live authority rather than transcript reconstruction.

### `UPSTREAM_CANDIDATE` — loop and owner-decision escalation

The proving system stopped repeated patch-and-run behavior after two adjacent deterministic launch
failures. It also stopped for an owner decision when further subtraction would change accepted
identity or authority semantics.

Implemented public boundary:

- Two qualifying consecutive launch failures produce `LOOP_DETECTED`.
- One bounded read-only sweep precedes one bundled correction.
- `OWNER_DECISION_REQUIRED` replaces another repair when simplification would reinterpret an
  accepted scientific, privacy, security, authority, or claim boundary.

### `PROJECT_ADAPTER`

Scientific runtime rules, target definitions, data authority, exact stage names, project ledger
entries, identity semantics, and local release design remain in the proving project.

### `PRIVATE_STATE`

Task transcripts, local paths, counts, hashes, plans, receipts, scientific results, saved artifacts,
and owner-specific project state were used only as local evidence and were not copied upstream.

### `NO_ACTION`

Agent+ already contained maker/evaluator/verifier separation, complete engineering sweeps,
two-BLOCK architecture reset, closed-interface recovery, zero-poll unattended work, outcome
retention, lean R defaults, complexity-as-diagnostic guidance, and fresh-review boundaries.

### `DOWNSTREAM_DRIFT`

None is declared. The new control is unreleased and not independently accepted, so no consumer may
be called behind or synchronized yet.

## Deterministic acceptance

- Active-chain focused attacks: `15/15` passed.
- Anti-loop focused tests: `54/54` passed.
- Workflow-default checks: `7/7` passed.
- Complete public suite: `147/147` passed.
- Canonical and bootstrap guard, example, protocol, and template bindings: `PASS`.
- Python compilation: `PASS`.
- Public privacy scan: `PASS`.
- Internal Markdown links: `PASS`.
- Complete public-package validator: `PASS`.
- Planned ledger-bound review dispatch: `PASS`, receipt
  `sha256:5db138c260311831b093175bbe38939c39a41bac31390a49d3c7fae7c793ba00`.

The first focused command used a non-package unittest import route and did not run tests. The same
focused matrix then passed through the repository's existing unittest discovery interface. One
Markdown line-wrap assertion was corrected without changing product behavior or policy meaning.
The completion audit then found and closed one external-capsule path. Its first negative test exposed
one wrapped error code, which received the permitted single mechanical correction before the same
focused matrix passed.

## Limits

- No independent reviewer assessed this new public capability.
- The ledger-bound review is planned but not independently completed.
- No version, commit, push, tag, release, consumer synchronization, data access, scientific work,
  dependency change, or proving-project mutation occurred.

## Next action

Run one fresh integrated review of the closed schema, path safety, stage semantics, bootstrap
binding, and policy consistency. If accepted, request a separate owner release decision. Because
this is a new public control capability, apply the repository's minor-release rule at that later
decision boundary.

Restart: `./scripts/ai-context.sh`
