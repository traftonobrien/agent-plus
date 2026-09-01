# Project Integration and Upstream Improvements

Agent+ is the canonical system. Baseball projects are consumers and proving projects.

## Ownership model

| Owner | Artifacts |
| --- | --- |
| Agent+ | Generic policies, bootstrap controls, reusable skills, lifecycle commands, and validators. |
| Consumer project | Research contracts, data authority, memory, plans, evidence, models, and project-specific controls. |
| Human owner | Scientific questions, claim promotion, live authorization, and release decisions. |

SECOND LOOK or another proving project can reveal a general system improvement. It does not become
the canonical source of that improvement.

## Improvement flow

1. Identify the general failure class in the proving project.
2. Separate project evidence from the reusable control.
3. Write a sanitized Agent+ change with synthetic tests.
4. Run the Agent+ public validator and request fresh review.
5. Version and publish the accepted Agent+ change.
6. Upgrade the proving project from that version.
7. Keep any project-only adapter local.

Use the current `0.3.x` patch line for small compatible fixes, documentation, and control
refinements. Use a new `0.x.0` minor release only for a genuinely new public capability or authority
boundary.

Do not copy private plans, data, receipts, paths, or transcripts into Agent+. Do not copy an
unreviewed proving-project control directly into the canonical repository.

## Local Agent Plus Brain registry

The canonical checkout can keep a private registry at `.agent-plus/local-projects.json`. This file
is ignored by Git. Copy `.agent-plus/local-projects.example.json`, then add local project roots.

```sh
scripts/agent-plus projects
scripts/agent-plus context PROJECT_NAME
```

This registry gives one Agent Plus Brain task a deliberate view into local proving projects. It
does not merge their memory or authority with Agent+.
