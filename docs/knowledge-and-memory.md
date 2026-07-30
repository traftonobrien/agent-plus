# Knowledge and Memory

Agent+ uses different records for different jobs. Combining them creates stale context and weak audit trails.

| Layer | Record | Purpose | Update rule |
| --- | --- | --- | --- |
| Project instructions | `AGENTS.md` | Stable rules for every runtime. | Change deliberately and review. |
| Runtime profile | `CLAUDE.md` | Claude-specific execution boundary. | Change when the runtime policy changes. |
| Hot state | `.claude-memory.md` | Current verified state, limit, and next action. | Rewrite after verified state changes. |
| Curated knowledge | Obsidian Brain | Durable methods, sources, decisions, and links. | Update when knowledge becomes reusable. |
| Task restart | Handoff | Exact state for one bounded task. | Write at pause or closeout. |
| Archive | Raw sessions and logs | Historical record only. | Do not load by default. |

Trust order is: live deterministic evidence, exact artifact, verified hot state, curated knowledge, then archive. The memory file is a pointer to evidence, not evidence itself.
