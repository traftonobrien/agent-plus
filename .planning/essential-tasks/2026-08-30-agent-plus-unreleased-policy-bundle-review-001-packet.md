# Agent+ unreleased policy bundle review 001 packet

Date: 2026-08-30

Status: `READY FOR FRESH INDEPENDENT REVIEW`.

## Review decision

Decide whether the unreleased policy-refinement bundle is internally consistent, public-safe, and
strict enough to ship in a later owner-authorized release. The reviewer must assess semantics and
authority boundaries, not merely the presence of required phrases.

The reviewer must use the frozen live files, review JSON, ledger, necessity cards, and deterministic
evaluation. The reviewer must not use the maker transcript and must not repair the candidate.

## Required scope

- Complete all `22` attack items in
  `.agent-plus/agent-plus-unreleased-policy-bundle-review-001.json`.
- Complete all `10` named coverage items.
- Probe the single small-correction rule against substantive, ambiguous, repeated, reviewer-found,
  behavior-changing, dependency-changing, and authority-changing defects.
- Assess whether continuous repair remains bounded to routine reversible work and escalates at the
  named scientific, data, authority, promotion, release, and repeated-failure boundaries.
- Assess R parity beyond visible outputs: missing/unknown values, exclusions, exceptional cases,
  downstream consumers, representative volume, vectorized large-table work, cost-separated
  targets, exact dependency graphs, and retained failed attempts.
- Confirm complexity remains a diagnostic and cannot become a universal score gate, score-only
  dependency, or helper-splitting game.
- Confirm patch-versus-minor guidance preserves the separate owner release decision and downstream
  synchronization boundary.
- Return `PASS` or `BLOCK` with Critical, Important, and Minor findings.

## Frozen policy identities

| Path | SHA-256 |
| --- | --- |
| `AI_WORKFLOW.md` | `689ce6e8c826af3526f4de8ff1aa17799851d552c2b9edf7811d10ecb285d249` |
| `bootstrap/base/AI_WORKFLOW.md` | `4642e00c969f605cbdc146a9128c3344ea1cdfbb51cee62b558300eacfaaf743` |
| `ESSENTIAL_WORK_PROTOCOL.md` | `e7705493da2ae917701d2e3cf5c184950b0526fab5f85e05e4ec82143219b97d` |
| `bootstrap/base/ESSENTIAL_WORK_PROTOCOL.md` | `e7705493da2ae917701d2e3cf5c184950b0526fab5f85e05e4ec82143219b97d` |
| `bootstrap/profiles/research/PROFILE.md` | `132c4b34efc729d14ca865373beb3593d2bf42fcfe3a62ffe9f9ca829a0da02c` |
| `skills/outcome-audit/SKILL.md` | `7df6248d0e58c1d6d60930f44efc52d1c66ccdceff214366f2479cc05ff77880` |
| `tests/test_workflow_defaults.py` | `26c28d499bb3fe302367c227c3be091549d8ac6aca99689c765835832771faba` |
| `AGENTS.md` | `e7a500d03ffe3e4e13269c43847764a654b774580ab4baabda8c5b1c00656738` |
| `docs/project-integration-and-upstream.md` | `9cc203f66fb10d97a91d476bf868e2061d4a049a49a9c13fc85f13557c4f9850` |
| `.agent-plus/engineering-boundaries.json` | `c9d7549ee913fa9e87e913649d886a141481f5765a897c9d4fa66df76d43d4ce` |
| `.agent-plus/agent-plus-unreleased-policy-bundle-task-001.json` | `c0125bf10ef7c28cad0a8c368b3c5d3e4458b9de072aa7fd17bce94d55b8286d` |
| R migration necessity | `f9e69d76b13d55636269a8ebfd470ba38be4526df0a255bdbb81145ca9bc9360` |
| Complexity necessity | `728967f3bc0f20844ccb279b92692527f9ae865f4f84cd123f7d8a97c38aaade` |
| Combined review necessity | `8c69ac37bb9398ad7a54a56d80a4d08768c430882838aa0571433a1f7de4bb22` |
| Deterministic evaluation | `f53fa669a4657d9146962fcd07aab33edac7e953bb4b3b229bed9cce4e814e26` |

The two essential-work protocol files must be byte-identical. The canonical and bootstrap workflow
documents intentionally differ in presentation and breadth; the reviewer must verify equivalent
authority semantics for the changed rules instead of requiring whole-file byte identity.

## Deterministic baseline

- Task admission: `PASS` with receipt
  `sha256:3a9458c5004852adfd21fe3978f0b02cb3676b7f449fbb061835ac6a3477c2c5`.
- Workflow defaults: `7/7`.
- Complete public suite: `163/163`.
- Public validation, guard bindings, links, privacy, and diff checks: `PASS`.
- One eligible mechanical admission correction was consumed. A second evaluator correction is not
  authorized in this chain.

## Accepted boundaries not reopened

- Active-chain/cost-isolation review 002 remains accepted at receipt
  `sha256:3ceb5acd7637c4568663a2c93216aa8b065d0ace32a723485fda1ea51be9ecfc`.
- Lifecycle-delivery review 001 remains accepted at receipt
  `sha256:c77ba7104f89e9ebbaa693c342a3dd940b9e8576b2457032252c7a1038136d10`.
- The reviewer must report if a frozen policy surface contradicts those controls, but must not
  rerun or rewrite their implementation reviews solely because they share public documents.

## Stop conditions

- Stop with `BLOCK` for any authority expansion, ambiguous correction permission, visible-only
  parity, broad rebuild default, erased failure evidence, complexity score gate, implicit release,
  missing attack, or incomplete coverage.
- Do not modify policy, tests, ledger, implementation, state, version, Git, release, or consumers.

## Closeout command

After the review JSON contains the complete exact matrices, run:

```sh
python3 scripts/anti_loop_guard.py \
  --ledger .agent-plus/engineering-boundaries.json \
  --packet .agent-plus/agent-plus-unreleased-policy-bundle-review-001.json \
  --require-complete-engineering-review
```
