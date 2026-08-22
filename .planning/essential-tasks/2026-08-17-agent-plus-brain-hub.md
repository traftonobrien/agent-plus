---
task: "Create a durable Agent+ project and activation hub in the local Obsidian Brain"
owner_role: "maker"
tier: "1"
time_budget: "45 minutes"
attempt_limit: 2
orchestration_mode: "quick"
exact_model: "Sol maker; deterministic wiki-link and retrieval checks"
reasoning: "routine"
authorization_scope: "Owner requested Agent+ project, tooling, activation, and new-project pages in the local Brain vault"
ownership_map: "Sol owns curated Agent+ Brain pages; live repositories remain authoritative; owner owns project and release decisions"
chain_stages: "inspect routes -> create project hub -> create activation and tooling pages -> update indexes -> verify retrieval"
concurrency: "zero workers; one writer"
tool_budget: "20 calls or 45 minutes"
context_budget: "25K ceiling; 4K-8K target"
reserve_use: "not used"
checkpoint_interval: "one checkpoint after link and retrieval validation"
overnight: "no"
evaluator_commands: "targeted wikilink checker and brain-find Agent+ retrieval"
fresh_verifier_contract: "not required for local curated navigation pages"
---

# Essential Task Card

## Necessity

- **Decision:** Decide whether a new chat has one durable Agent+ orientation and activation route.
- **Uncertainty:** The Brain had SECOND LOOK and Agent Tooling pages but no canonical Agent+ project hub.
- **Existing evidence:** Agent+ repository controls existed, but the Brain did not route to them as one system.
- **Minimum action:** Add one project hub, one activation page, one improvement workflow, one tooling route, and one new-project page.
- **Unlock:** Codex or Claude can retrieve Agent+ commands, prompts, skills, and boundaries from one Brain route.

## Boundary

- **Allowed artifacts:** Curated Brain wiki pages and routing indexes.
- **Allowed actions:** Create pages, add wiki links, validate links, and test retrieval.
- **Forbidden actions:** Modify Brain raw inputs or scripts, rewrite unrelated pages, run a bulk import, or change Agent+ scientific authority.
- **Review mode:** Engineering sweep.
- **Failure-class coverage:** Project route, home route, tooling route, activation, prompts, skills, commands, source priority, and retrieval.
- **Simplification trigger:** If guidance duplicates live repository state, replace details with a live-source link.
- **User-visible outcome:** One Agent+ Brain hub routes new projects, audits, implementation, and release work.
- **Stop condition:** All new pages have required structure, targeted links resolve, and `brain-find` returns the hub.
- **Stop behavior:** Collect all targeted route failures before repair.
- **Attack matrix:** Missing project hub, missing home link, missing tooling link, broken new-page link, absent key takeaways, and retrieval failure.
- **Named coverage:** Master index, Start Here, new-project route, quick context, Agent Tooling, skills reference, and Agent+ hub.
- **Repeat trigger:** Agent+ interface, skill inventory, release workflow, or Brain routing changes.
- **Acceptance:** Targeted validation passes and Agent+ pages occupy the first retrieval results.

## Decision branches

- **If PASS:** Use the Agent+ hub as durable orientation for new chats.
- **If BLOCK or FAIL:** Continue using live repository files and repair only the missing Brain route.

## Closeout

```yaml
decision_changed: yes
blocker_closed: missing Agent Plus Brain route
work_unlocked: durable Agent Plus orientation and activation retrieval
user_visible_outcome: Agent Plus project, tooling, audit, release, and new-project pages are linked and retrievable
repeat_trigger: Agent Plus interface, skill inventory, release workflow, or Brain routing changes
```
