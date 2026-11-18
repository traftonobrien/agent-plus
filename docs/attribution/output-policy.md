# Output Policy Attribution

Agent+ adapts the action-first response shape from Ayoub Ghriss's `i-have-adhd` skill.

- Upstream: [`ayghri/i-have-adhd`](https://github.com/ayghri/i-have-adhd)
- Inspected commit: [`72c33eee81ea439cf01991e93729adfce2ffc99e`](https://github.com/ayghri/i-have-adhd/tree/72c33eee81ea439cf01991e93729adfce2ffc99e)
- Upstream skill: [`skills/i-have-adhd/SKILL.md`](https://github.com/ayghri/i-have-adhd/blob/72c33eee81ea439cf01991e93729adfce2ffc99e/skills/i-have-adhd/SKILL.md)
- Upstream license: [MIT](AYOUB-GHRISS-LICENSE.txt)
- Copyright: Copyright (c) 2026 Ayoub Ghriss

The upstream skill emphasizes concrete next actions, visible state, bounded lists, factual errors,
and low-friction restart. Agent+ changes the contract to lead with a verified result or current
action, preserve scientific and authorization boundaries, avoid unsupported time estimates, and
keep exact receipts available without requiring them in every update.

The full upstream MIT notice is also reproduced in the canonical and bootstrap output-policy files
so a generated project retains the notice without depending on this documentation directory.
