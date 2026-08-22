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

## Direct model delegation

When the owner explicitly requests delegation, sub-agents, parallel work, or Luna, keep Sol as the
control plane and create model-selected Luna sub-agents directly. Do not require the owner to open
separate chats or copy results between them.

- Use Luna High for routine diagnostics, corrections, documentation, tests, and scoped implementation.
- Use Luna xhigh for complex multi-file engineering, architecture tracing, long read-only work, and
  fresh engineering review.
- Keep Sol responsible for task splitting, boundaries, progress, synthesis, and the owner-facing result.
- Reserve premium reasoning for scientific ambiguity, leakage, frozen-contract changes, hard
  architecture, and irreversible promotion decisions.

Each delegated task must have one concrete deliverable, exact ownership, allowed inputs, a stop
condition, and a budget. Select the worker model explicitly and pass only the bounded context it
needs. Use parallel workers only for independent tasks. Do not let workers edit the same files,
silently fall back to another model, recursively spawn agents, or certify their own work. A fresh
verifier must be independent of the maker. Wait at a bounded checkpoint instead of polling.

If direct model selection is unavailable, record `BLOCK` and the missing capability. Do not turn a
capability failure into repeated manual cross-chat handoffs. Recheck this route when model access,
rates, delegation support, or a bounded benchmark changes.

## Higher-capacity session profile

Extra capacity increases bounded throughput only. It does not increase authority, context ceilings,
retry count, reviewer count, or the human owner's decision rights. Select one mode in the task packet.

| Mode | Route | Total wall-time budget |
| --- | --- | ---: |
| `quick` | Sol/high controller; at most one Luna High explorer; Luna High maker; deterministic evaluator; fresh Luna xhigh only at promotion. | 45 minutes |
| `standard` (default) | Sol/high controller; two independent Luna High explorers; Luna xhigh maker; deterministic evaluator; one fresh Luna xhigh reviewer. | 90 minutes |
| `deep` | Sol/high controller; up to three independent Luna xhigh explorers; one accountable maker (Luna xhigh, or explicitly selected Claude Sonnet high; Opus high only for a named hard-architecture or frozen-contract decision); deterministic evaluator; one fresh independent reviewer. | 120 minutes |
| `scientific/live` | Up to two read-only Luna xhigh readiness explorers; no parallel workers during live execution; deterministic metrics; fresh premium scientific reviewer only for the named decision; human owner authorization before data access, live execution, or promotion. | Task-specific owner budget |

An owner command may authorize one engineering-only chain: plan → independent explorers → frozen
evidence handoff → exclusive maker → deterministic evaluator → fresh reviewer → Sol synthesis. After
exploration, stages are sequential. The reviewer receives the contract, artifact, deterministic
receipts, and attack matrix, not the maker transcript. Stop on a maker, evaluator, or reviewer
`BLOCK`; do not auto-repair after a reviewer `BLOCK`.

The controller plus workers uses two workers by default and never more than three. Use one writer
per repository, no overlapping writes, no recursive spawn, no silent fallback, and one bounded wait
per stage. Scientific/live execution has zero parallel workers after readiness exploration.

## Capacity and context limits

Context ceilings remain 25K tokens for ordinary sessions and 40K for premium sessions. Targets are
4–8K for routine work, 8–15K for implementation, and 12–25K for premium review or architecture.
Start a fresh session at 60–80K accumulated tokens. Capacity is not permission to exceed these
limits or to burn allowance without a decision-relevant deliverable.

| Boundary | Budget |
| --- | --- |
| Routine maker | 32 tool calls / 60 minutes |
| Complex maker | 40 tool calls / 90 minutes |
| Engineering reviewer | 20 tool calls / 45 minutes |
| Scientific/live reviewer | 12 tool calls / 25 minutes |
| Failed attempts | Maximum 2, unchanged |

Reserve 25% of higher-capacity premium allowance for scientific, leakage, hard-architecture, or
irreversible decisions. Do not spend that reserve on routine throughput or burn capacity without a
decision-relevant deliverable.

Overnight mode requires an explicit owner command. It permits only read-only or reversible
engineering, at most three workers, a fixed queue of at most eight tasks, and a default four-hour
window. Checkpoint every 30 minutes or 100K fresh tokens, whichever comes first. It forbids live,
scientific, and promotion work, forbids queue refill, and stops on `BLOCK`.

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

Repeat model review after 10 completed bounded chains or 14 days. Repeat sooner after a model,
rate, or plan change; two routing `BLOCK`s; average context above 40K; or reviewer correction above
20%. This review cadence is a maintenance control, not a performance claim.

## Task packet

Each task identifies the decision, uncertainty, allowed inputs, permitted actions, time and context budget, attempt limit, stop condition, acceptance check, and handoff owner. Use [the essential task template](.planning/templates/ESSENTIAL-TASK.md).

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

The first engineering `BLOCK` triggers a consolidated attack matrix and one bundled maker repair.
A second `BLOCK` at the same interface triggers architecture simplification, not another local
patch. Remove unnecessary input freedom and prefer a constrained interface that makes invalid
states impossible. Then use one deterministic receipt and one fresh integrated review.

The controller must reject packets that create a review for each local defect, stop at an
intermediate artifact without an authority boundary, or measure progress only through tests,
tokens, files, or review count. The required outcome is the named user-visible or scientific
milestone that the engineering work unlocks.

Before dispatching an engineering maker or reviewer, the controller must obtain a PASS receipt
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

Start with `scripts/ai-context.sh`. Read the exact planning artifact named by `.claude-memory.md`. Do not load private transcripts or broad history by default. Use `.claude-memory.md` for current verified state and the Obsidian Brain for durable curated knowledge.

## Stop rules

- Stop after two failed attempts and record `BLOCK`.
- Do not repeat unchanged evidence merely because a new session starts.
- Do not advance past a contract, coverage, temporal-order, or verification gate.
- Treat `PASS`, `NULL`, and `BLOCK` as valid outcomes.
