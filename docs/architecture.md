# Architecture

Agent+ turns a baseball research question into documented, reviewable work. It does not automate scientific judgment.

```mermaid
flowchart LR
    Q["Question"] --> C["Contract and sources"]
    C --> M["Knowledge and memory"]
    M --> W["Skills and bounded work"]
    W --> D["Deterministic evidence"]
    D --> V["Fresh verification"]
    V --> R{"Outcome"}
    R -->|PASS| P["Evidence-bound statement"]
    R -->|Null| N["Documented null result"]
    R -->|BLOCK| B["Missing evidence recorded"]
    P --> H["Handoff"]
    N --> H
    B --> H
```

## Components

**Research contract.** States the decision, question, population, temporal boundary, target, comparator, evidence needed, and permitted claim before result review.

**Curated knowledge and memory.** The Obsidian Brain holds durable sources, decisions, and methods. Project memory holds changing verified state. Handoffs preserve one task boundary.

**Specialized skills.** Skills encode small repeatable procedures. They do not grant scientific authority or bypass the contract.

**Bounded model work.** A model receives only the files, authority, budget, and acceptance rule needed for a task.

**Deterministic evidence.** Code, schemas, source logs, hashes, fixtures, and tests establish facts that can be independently checked.

**Fresh verification.** A reviewer examines changed evidence from a clean context. The reviewer may accept, reject, narrow, or block the work.

**Human decision.** A person owns the decision to promote a verified result into a research or operational claim.

## Role separation

| Role | May do | May not do |
| --- | --- | --- |
| Maker | Produce a bounded artifact. | Certify its own result. |
| Evaluator | Run approved deterministic checks. | Interpret beyond the contract. |
| Verifier | Independently inspect changed evidence. | Rewrite the maker artifact silently. |
| Human owner | Accept, narrow, defer, or stop a claim. | Treat generated prose as proof. |
