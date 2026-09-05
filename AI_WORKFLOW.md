# Agent+ AI Workflow

This is the binding public workflow for Agent+. It mirrors the control structure of a production research program without exposing private project state.

## Operating rule

Use deterministic tools first. Give AI systems narrow, reviewable assignments. Human scientific judgment owns research claims and promotion decisions.

## Routing matrix

| Tier | Use | Required control | Cannot certify |
| --- | --- | --- | --- |
| 0 | Search, parse, count, hash, validate, test, score. | Record exact command or artifact. | Narrative conclusion. |
| 1 | Reversible extraction, classification, summary, and drafting. | Human or deterministic check. | Data coverage, scientific safety, or promotion. |
| 2 | Bounded implementation and integration. | Named acceptance check. | Its own work. |
| 3 | Leakage, hard architecture, adversarial, or fresh review. | Independent context and changed evidence. | Deterministic evidence or human decision. |

## Model and task routing

Classify work through the Task applicability rules in `AGENTS.md`. A routine task does not become
a formal engineering chain merely because the controller edits a file or runs a deterministic check.
Use the owner-selected runtime model. For Astra, record `gpt-6-astra` and preserve effective reasoning
effort. High is the initial tuning baseline, not a claim that it is optimal for every task.
Compare lower effort on representative tasks before changing that baseline. Never use unsupported
`none` or `minimal` effort for Astra. Do not silently change models or fallback routes.

## Direct model delegation

Delegate only when the owner requests it or applicable project instructions explicitly require an
independent role. The controller owns task splitting, boundaries, progress, synthesis, and the result.
Use Luna High for bounded routine workers and Luna xhigh for complex workers or fresh engineering
review. Retain these cost-sensitive routes until a bounded comparison supports a change.
Each task names its exact model, deliverable, ownership, permitted inputs, stop condition, and budget.
Pass only needed context. A fresh verifier receives the contract, changed artifact, deterministic
evidence, and attack matrix, not the maker transcript. The maker cannot certify its own work.

Parallelize independent read-only exploration only when it can improve the named outcome. Use at
most three workers, one writer per repository, no overlapping writes, and no recursive spawn.
The default is zero workers without delegation authority. Once authorized, use only the workers
needed, commonly one or two; worker limits are ceilings, not mandatory staffing.
If exact required model selection is unavailable, report the missing capability and BLOCK that
delegated stage. Continue independent authorized work where possible; do not silently substitute.

## Bounded session modes

Extra capacity increases bounded throughput only. It does not increase authority, retry count,
reviewer count, or the human owner's decision rights. Select one mode in a formal task packet.

| Mode | Route | Total wall-time budget |
| --- | --- | ---: |
| `quick` | Selected controller; focused deterministic check; optional authorized worker; fresh review at promotion. | 45 minutes |
| `standard` (default) | Selected controller; authorized independent exploration if useful; exclusive maker; deterministic evaluator; one fresh reviewer at the required boundary. | 90 minutes |
| `deep` | Selected controller; up to three authorized read-only explorers; one maker; deterministic evaluator; one fresh independent reviewer. | 120 minutes |
| `scientific/live` | At most two authorized readiness explorers; zero parallel workers during live execution; deterministic metrics; independent scientific review; human authorization for data, execution, or promotion. | Task-specific owner budget |

An owner command may authorize one engineering-only chain: plan → independent explorers → frozen
evidence handoff → exclusive maker → deterministic evaluator → fresh reviewer → controller synthesis. After
exploration, stages are sequential. The reviewer receives the contract, artifact, deterministic
receipts, and attack matrix, not the maker transcript. Stop on a maker or reviewer `BLOCK`; do not
auto-repair after a reviewer `BLOCK`. Handle an eligible mechanical evaluator finding through the
single small-correction rule below; otherwise stop on evaluator `BLOCK` too.

For a multi-stage chain, keep one `.agent-plus/active-chain.json` routing capsule. It contains the
objective, ordered stages, roles, terminal status, failure count, authority references, and closed
hard-boundary categories. It does not contain scientific values, schemas, thresholds, hashes, or
artifact identities. Every stage reads the live repository authority named by relative path.

Run `scripts/active_chain_guard.py --capsule .agent-plus/active-chain.json --mode continue` before
each next stage. Run it with `--mode closeout` before ending the chain. The guard accepts honest
`PASS`, `NULL`, and `BLOCK` closeouts and rejects early success, stale or unsafe authority paths,
out-of-order stages, missing durable evidence, and a third local repair after two failures.

The capsule is routing state only. `same_interface_failures` is the ledger count observed when the
chain starts. The anti-loop ledger and guard remain authoritative for repair, reset, execution, and
review admission. The active-chain guard does not record a `BLOCK` or grant another attempt.

### Small correction rule

When a deterministic evaluator finds one obvious syntax, command-spelling, or test-harness false
positive, fix it once and rerun the same bounded check without another owner prompt. Use this only
when production behavior, data access, dependencies, authority, scientific meaning, and the
acceptance boundary remain unchanged. Stop if the rerun fails, another correction is needed, the
finding is substantive or ambiguous, or it came from a reviewer.

### Continuous repair default

For routine reversible work, keep momentum through small, obvious mechanical defects. Fix the
localized issue, run the smallest check that proves the path still works, and continue the same
bounded task. Do not create a formal stop, review, or new artifact for each minor correction.

Escalate only when the defect is ambiguous, two adjacent failures appear at the same boundary, or
the task reaches scientific meaning, real-data access, authority, promotion, release, or reviewer
evidence. At those boundaries, use the applicable sweep, review, or first-error stop rule.

Two consecutive launches that expose adjacent deterministic failures at one boundary, before any
scientific result exists, are `LOOP_DETECTED`. Stop patch-and-run behavior. Record both symptoms in
the existing ledger or receipt, complete one bounded read-only boundary sweep, and make one bundled
correction. Do not create a new tracker for this signal.

## Capacity and context limits

Context budgets measure task material deliberately retrieved, separately from host-injected rules,
cached input, and cumulative tokens. The existing planning targets remain 4–8K for routine work,
8–15K for implementation, and 12–25K for premium review. Ordinary retrieved context has a 25K ceiling
and premium retrieved context a 40K ceiling unless the owner supplies a different bounded budget.
Do not claim exact token usage when the runtime only exposes bytes or estimates.

Use native compaction and a durable handoff at a clean task or independent-review boundary.
Cumulative usage alone does not force a restart. Resume from live authority and evidence, not an
expanded transcript. Never override model context size to bypass these task budgets.

| Boundary | Budget |
| --- | --- |
| Routine maker | 32 tool calls / 60 minutes |
| Complex maker | 40 tool calls / 90 minutes |
| Engineering reviewer | 20 tool calls / 45 minutes |
| Scientific/live reviewer | 12 tool calls / 25 minutes |
| Failed attempts | Maximum 2, unchanged |

These are per-role ceilings inside the total session budget, not targets to consume. Batch independent
reads and deterministic checks. Repeat a check only after changed inputs, implementation, environment,
or a specific unresolved concern. Complete every required acceptance check before claiming success.

A 25% premium reserve applies only when a task has a measurable premium allowance. Otherwise mark
it not applicable; do not invent remaining account capacity. Review limits through measured outcomes.
Overnight mode still requires an explicit owner command, a fixed queue of at most eight tasks,
at most three workers, and a default four-hour window. Checkpoint at completed task boundaries and
within 30 minutes for attended orchestration. It forbids live, scientific, and promotion work, queue
refill, and continuation after BLOCK. Unattended processes follow the stricter zero-poll rule below.

## Unattended execution

Use unattended execution only when one bounded process can own the complete run and write durable
evidence without AI supervision. The task card must name the exact command, one authorized launch,
the durable progress and terminal evidence paths, the expected return point, and one result check.

After launch, the AI controller must not poll the process, terminal, logs, or evidence files. The
process writes its own progress and terminal state. On return, the controller performs one result
check against the named terminal evidence and acceptance rule.

A launch error, process error, missing terminal evidence, or failed return check consumes the
authorization and returns `BLOCK`. Do not fall back, relaunch, or retry. Resume only after bounded
repair, any required fresh review, and new explicit authorization. Process-written evidence does
not grant promotion authority or replace independent verification.

Use the project-specific model-review procedure after 10 completed bounded chains or 14 days.
This is prospective workflow comparison, not automatic collection of global session history. Repeat sooner after a model,
rate, or plan change; two routing `BLOCK`s; average context above 40K; or reviewer correction above
20%. This review cadence is a maintenance control, not a performance claim.

## Task packet

Each formal task identifies the decision, uncertainty, allowed inputs, permitted actions, time and context budget, attempt limit, stop condition, acceptance check, and handoff owner. Use [the essential task template](.planning/templates/ESSENTIAL-TASK.md).

## Role separation

- The maker creates one bounded artifact.
- The evaluator runs deterministic checks.
- The fresh verifier assesses changed evidence independently.
- The human owner accepts, narrows, defers, or blocks the resulting claim.

No model self-certifies. No model silently changes its tier or falls back to another model.

## Engineering closure and review

Engineering diagnostics and scientific execution use different stop behavior. Scientific, live,
destructive, and irreversible work stops at the first invalid condition. An engineering diagnostic
blocks promotion at the first defect but continues read-only attacks across its named boundary so
one repair packet contains the complete reachable defect class.

The first engineering `BLOCK` requires a consolidated attack matrix and one bundled repair plan.
This specifies the required evidence and repair scope, not authority to restart. A reviewer BLOCK
ends the current chain. New explicit owner authorization is required before a repair maker starts.
The single eligible deterministic-evaluator correction remains the exception described above.
A second `BLOCK` at the same interface triggers architecture simplification, not another local
patch. Remove unnecessary input freedom and prefer a constrained interface that makes invalid
states impossible. Then use one deterministic receipt and one fresh integrated review.

If the required simplification would weaken or reinterpret an accepted scientific, privacy,
security, authority, or claim boundary, return `OWNER_DECISION_REQUIRED`. Give the smallest
mutually exclusive choices and the evidence each choice needs. The owner decision starts a new
chain; it is not a repair retry.

The controller must reject packets that create a review for each local defect, stop at an
intermediate artifact without an authority boundary, or measure progress only through tests,
tokens, files, or review count. The required outcome is the named user-visible or scientific
milestone that the engineering work unlocks.

Before dispatching a formal engineering maker or reviewer, the controller must obtain a PASS receipt
from the anti-loop guard for a packet whose boundary and failure class already exist in the
ledger. An unregistered boundary is a `BLOCK`, not an informal task. A reviewer may start with a
`planned` packet, but its verdict cannot unlock another maker or owner decision until the same
ledger-bound review is closed with complete attack-matrix and named-coverage status:

```text
python3 scripts/anti_loop_guard.py \
  --ledger .agent-plus/engineering-boundaries.json \
  --packet REVIEW-CLOSEOUT.json \
  --require-complete-engineering-review
```

An engineering defect blocks promotion immediately but does not end safe read-only attacks in the
declared matrix. Record a review `BLOCK` in the ledger only after the closeout command passes. Do
not dispatch the next maker from a partial reviewer narrative.

Keep one active promotion-boundary dossier. Update its task contract, cumulative finding matrix,
current acceptance receipt, and integrated review in place. Preserve historical evidence, but do
not create a new packet set for every local correction.

## Anti-loop guard packet

The deterministic guard in `scripts/anti_loop_guard.py` checks the machine-readable
`.agent-plus/engineering-boundaries.json` ledger against each task or review packet. Schema
`anti-loop-guard/v2` is closed and strictly structured. Every packet names a stable boundary and
failure class, one `change_kind` (`local_repair`, `architecture_reset`, or `execution`), one
`outcome_kind` from a closed category enum, one ledger-approved `outcome_id`, ledger-declared
failure-class coverage, one stop policy, and both ledger-bound matrices. Engineering reviews marked
complete must show complete attack-matrix and named-coverage items that exactly match the ledger.
After two BLOCKs, only an architecture-reset packet with the ledger-approved `reset_namespace`,
`attempt_id`, and `removed_caller_choices` can pass. Scientific and live packets must use the
first-error stop policy.

After a closed-interface recovery passes its required review, keep the constrained interface as the
default for that failure class. Do not restore removed caller choices or open inputs without a new
necessity card, a named consumer, deterministic acceptance checks, and required review.

The ledger, not packet wording, decides authorization. The guard owns a closed exact outcome
catalog; the ledger may select only a subset of its IDs and must preserve each catalog ID's one
fixed category. Unknown, renamed, case-changed, path-like, and recategorized IDs fail closed. There
is no free-text field, so a description, note, or nested caller value cannot relabel a local repair
as an architecture reset. Process work such as passing tests, passing lint, written files, updated
documents, completed reviews, or receipts has no catalog entry and cannot be declared as a user or
scientific result.

The guard rejects duplicate JSON keys at every depth, non-string mapping keys at every depth,
unknown fields, unsupported schema versions, wrong types, malformed JSON, NaN and infinity, and
non-exact BLOCK counts, all as typed guard errors. PASS receipts bind the canonical packet and the
complete ledger state and do not change when a caller mutates its inputs afterward. BLOCK updates
use a lock plus durable atomic replacement; lock, corruption, and write failures are typed guard
errors.

Run it with:

```text
python3 scripts/anti_loop_guard.py --ledger .agent-plus/engineering-boundaries.json --packet PACKET.json
```

## Context and memory

Start with `scripts/ai-context.sh`. Read the exact planning artifact named by `.claude-memory.md`.
Do not load private transcripts or broad history by default. Live policy, contracts, code, and
deterministic evidence outrank hot memory, planning state, the Brain, and transcripts. Memory and
planning state route work; they do not grant authority. Reference live authority files instead of
copying their values into task packets or chain capsules. Use `.claude-memory.md` for current
verified state and the Obsidian Brain for durable curated knowledge.

## Stop rules

- Apply the routine/formal/scientific classification before selecting a stop rule.
- Stop after two failed attempts at the same interface and record `BLOCK`.
- Do not repeat unchanged evidence merely because a new session starts.
- Do not advance past a contract, coverage, temporal-order, or verification gate.
- Treat `PASS`, `NULL`, and `BLOCK` as valid outcomes.
