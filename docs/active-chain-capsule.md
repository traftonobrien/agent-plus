# Active-Chain Capsule

Use one active-chain capsule to route an owner-authorized multi-stage chain. The capsule makes stage
order and closeout deterministic. It does not grant task, scientific, repair, review, promotion, or
release authority.

## Authority boundary

The engineering ledger, accepted contracts, live policy, deterministic evidence, and explicit
owner decisions remain authoritative. The capsule references these files by repository-relative
path. It does not copy scientific values, schemas, thresholds, hashes, artifact identities, or
private evidence.

`same_interface_failures` is the ledger count observed when the chain starts. The anti-loop guard,
not the active-chain guard, decides whether a local repair, architecture reset, execution, or review
is authorized. The active-chain guard only rejects a route that claims another local repair after
the capsule already records two failures.

## File location

New Agent+ projects receive the managed guard and sanitized example. Copy
`.agent-plus/active-chain-example.json` to `.agent-plus/active-chain.json`. The active capsule is
ignored by Git because it is mutable local routing state. The guard rejects any capsule outside
these two exact project-local paths and rejects a capsule reached through a symlink.

## Stage contract

- `active`: every completed stage is `pass`; the first pending stage is `current_stage`; all later
  stages remain pending.
- `pass`: every stage is `pass` and carries a live durable evidence path.
- `null` or `block`: prior stages are `pass`, exactly one stage has the terminal status, and later
  stages remain pending.
- A pending stage has an empty evidence field. A completed or terminal stage references one regular,
  non-symlink file inside the project root.
- `authority_refs` and `hard_boundaries` are sorted and unique. Authority references resolve to
  regular, non-symlink files inside the project root.

## Commands

Before each stage:

```sh
python3 scripts/active_chain_guard.py \
  --root . \
  --capsule .agent-plus/active-chain.json \
  --mode continue
```

Before a final response that ends the chain:

```sh
python3 scripts/active_chain_guard.py \
  --root . \
  --capsule .agent-plus/active-chain.json \
  --mode closeout
```

An early closeout is `BLOCK_CHAIN_EARLY_CLOSEOUT`. A terminal capsule cannot continue. Unknown or
duplicate JSON fields, unsafe paths, symlinks, missing evidence, invalid order, unsupported status,
non-exact failure counts, alternate capsule locations, and capsules larger than 64 KiB fail closed.

## Explicit limits

- The capsule does not replace `scripts/anti_loop_guard.py` or its ledger.
- The capsule does not record or increment an engineering `BLOCK`.
- The capsule does not authenticate scientific artifacts or runtime data.
- The capsule does not authorize another maker after reviewer `BLOCK`.
- The capsule does not authorize release, publication, Git mutation, or consumer synchronization.
