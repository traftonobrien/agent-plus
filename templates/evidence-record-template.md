# Evidence Record — Template

Update the existing record for this evidence or bounded result. Link authoritative inputs, checks
and reviewer artifacts instead of copying them. A check does not require its own Markdown file.
Ordinary work uses the existing task record unless its controls require separate evidence. Preserve
required exact run history and distinct evidence identities.

## Identity

- Record ID: `[ID]`
- Contract ID and version: `[ID]`
- Artifact ID or hash: `[ID]`
- Status: `PASS | NULL | BLOCK`

## Inputs and checks

- Approved inputs: `[identifiers only]`
- Deterministic checks: `[command, schema, count, hash, or test]`
- Check result: `[result]`
- Reviewer evidence: `[reference]`

## Interpretation

- Evidence supports: `[bounded statement]`
- Evidence does not support: `[explicit limit]`
- Downstream action: `[next action]`

## If BLOCK

- Missing or failed evidence: `[exact fact]`
- Why it prevents continuation: `[effect]`
- Resume condition: `[exact proof required]`
