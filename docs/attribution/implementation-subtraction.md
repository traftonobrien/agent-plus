# Implementation Subtraction Attribution

Agent+ adapts the subtraction-first decision ladder from Dietrich Gebert's Ponytail project.

- Upstream: [`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail)
- Inspected commit: [`2ed6c52c9d7e5e56942508591085fd45dea277d3f`](https://github.com/DietrichGebert/ponytail/tree/2ed6c52c9d7e5e56942508591085fd45dea277d3f)
- Upstream rules: [`AGENTS.md`](https://github.com/DietrichGebert/ponytail/blob/2ed6c52c9d7e5e56942508591085fd45dea277d3f/AGENTS.md)
- Upstream license: [MIT](DIETRICH-GEBERT-LICENSE.txt)
- Copyright: Copyright (c) 2026 DietrichGebert

Ponytail checks whether work is necessary and whether the repository, standard library, platform,
or an installed dependency already supplies the behavior. Agent+ places that decision inside its
necessity, authority, evidence, safety, and independent-review controls. The adaptation does not
install Ponytail's hooks or inject its complete rules into every Agent+ worker.
