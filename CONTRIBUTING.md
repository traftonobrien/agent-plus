# Contributing

Agent+ accepts improvements that make AI-assisted baseball research easier to inspect and safer to reuse.

## Before opening a change

1. Do not add raw data, secrets, personal information, local paths, private artifacts, or chat transcripts.
2. Mark illustrative material as `Example`, `Template`, or `Placeholder`.
3. Do not convert model fit into a future-prediction, decision-value, or real-world-impact claim.
4. Preserve the distinction between custom Agent+ skills and integrated external tools.
5. Check every internal Markdown link and every stated command.

## Change standard

State the purpose, affected files, evidence used, and limits of the change. Keep procedures bounded. Each new skill must contain the required sections in the existing skills. Each example must include an explicit synthetic-data notice.

If a proving project reveals the improvement, port only the generic control and synthetic test.
Do not copy the proving project's state or evidence. Follow
[project integration and upstream improvements](docs/project-integration-and-upstream.md).

## Review standard

Reviewers check public safety, accurate authority boundaries, link integrity, and whether a `BLOCK` outcome remains possible. A contribution is not accepted because it sounds plausible. It must be inspectable and safe to publish.
