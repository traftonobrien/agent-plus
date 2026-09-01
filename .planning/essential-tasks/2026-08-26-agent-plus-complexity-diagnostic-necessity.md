# Agent+ complexity diagnostic — necessity

- **Decision:** Whether code-path complexity should become a lean subtraction prompt in Agent+.
- **Uncertainty:** A universal cyclomatic-complexity gate may reduce branching, but it can also be
  gamed by scattering the same logic across helpers or adding an unnecessary lint dependency.
- **Existing evidence:** Agent+ already requires implementation subtraction and boring code, but it
  does not state how to interpret a high branch count.
- **Minimum action:** Add one generic diagnostic rule and a focused text check. Do not add a package,
  numeric threshold, new lint stage, service, or ledger.
- **Unlock:** Agents must simplify decision paths when that clarifies the real flow without treating
  a score as proof of quality.
- **Stop condition:** Canonical/bootstrap parity and existing public validation pass.
- **Repeat trigger:** Measured evidence from another project shows a useful language-specific limit.
- **Budget:** One documentation-sized patch. No release, synchronization, Git operation, data access,
  or scientific execution.

Failure class: `COMPLEXITY_SCORE_GAMED_WITHOUT_FLOW_SIMPLIFICATION`.
