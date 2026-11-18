# Evidence Record — Template

Update the existing record for this evidence or bounded result. Link authoritative inputs, checks
and reviewer artifacts instead of copying them. A check does not require its own Markdown file.
Ordinary work uses the existing task record unless its controls require separate evidence. Preserve
required exact run history and distinct evidence identities.
Fill only applicable fields. A contract, hash or independent reviewer is required only when the owning workflow requires it. This template does not create those requirements.

## Identity

- Record ID: `[ID]`
- Contract ID and version: `[reference when applicable]`
- Artifact path or ID: `[reference; hash when exact identity is required]`
- Tested code revision or file version: `[identifier or existing source-snapshot reference]`
- Status: `PASS | NULL | BLOCK`

## Inputs and checks

- Approved inputs: `[identifiers only]`
- Deterministic checks: `[exact command and exit status; link existing check output]`
- Exercised scenario: `[real producer/consumer path, actual result and relevant known-bad check; mark anything not run]`
- Check result: `[result]`
- Reviewer evidence: `[existing reference when the workflow requires independent review]`

## Interpretation

- Evidence supports: `[bounded statement]`
- Evidence does not support: `[explicit limit, including material untested behavior]`
- Downstream action: `[next action]`

## If BLOCK

- Missing or failed evidence: `[exact fact]`
- Why it prevents continuation: `[effect]`
- Resume condition: `[exact proof required]`
