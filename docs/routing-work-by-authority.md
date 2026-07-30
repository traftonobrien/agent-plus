# Routing Work by Authority

Route work by the authority it needs, not by which model is available. Use the lowest-cost method that can safely close the uncertainty.

![Routing work by authority](../assets/routing-work-by-authority.png)

| Tier | Typical work | Evidence rule | Prohibited authority |
| --- | --- | --- | --- |
| 0: deterministic | Search, parse, count, hash, test, score. | Tool output is recorded. | Narrative scientific judgment. |
| 1: reversible assistance | Extraction, classification, summaries, draft logs. | A human or test checks the result. | Certification, promotion, or unchecked mutation. |
| 2: bounded implementation | Approved code and integration work. | Narrow acceptance checks are required. | Self-certification. |
| 3: independent review | Leakage, hard design, adversarial review. | Fresh review of changed evidence is required. | Replacing deterministic evidence or human ownership. |

Each work order names its files, inputs, owner, model or tool, time budget, attempt limit, stop condition, and acceptance check. Silent model fallback is not allowed.
