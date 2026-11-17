# Knowledge and Memory

Agent+ separates stable instructions, current state and retained evidence. One existing record can
serve both project memory and task restart when it is sufficient. Create a separate handoff only
when needed, then link to it rather than copying its changing state.

| Layer | Record | Purpose | Update rule |
| --- | --- | --- | --- |
| Project instructions | `AGENTS.md` | Stable rules for every runtime. | Change deliberately and review. |
| Runtime profile | `CLAUDE.md` | Claude-specific execution boundary. | Change when the runtime policy changes. |
| Hot state | `.claude-memory.md` | Current verified state, limit, and next action. | Rewrite after verified state changes. |
| Curated knowledge | Obsidian Brain | Durable methods, sources, decisions, and links. | Update when knowledge becomes reusable. |
| Task restart | Existing memory or task handoff | Exact state for one bounded task. | Update when restart state changes. |
| Archive | Raw sessions and logs | Historical record only. | Do not load by default. |

Trust order is: live deterministic evidence, exact artifact, verified hot state, curated knowledge, then archive. The memory file is a pointer to evidence, not evidence itself.
