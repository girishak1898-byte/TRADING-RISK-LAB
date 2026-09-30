# TRADING RISK LAB

A greenfield mathematical research programme for a deterministic, independently testable **risk-control engine**.

**Governing question.** Given an opportunity, authoritative portfolio state, market state and uncertainty state, what is the maximum
action that remains inside every accepted safety constraint — including the possibility that the correct action is zero?

**Authority hierarchy.** AUTHORITY → SAFETY → MATHEMATICAL VALIDITY → NUMERICAL CORRECTNESS → STATISTICAL ROBUSTNESS → PERFORMANCE.
A later layer never overrides an earlier one.

## Status

**Phase 0 — Mathematical Constitution v0.1 (DRAFT, awaiting human review).** No code exists. No formula has been adopted. No
parameters have been chosen.

## Hard prohibitions (this phase)

No broker or Alpaca connectivity · no order submission · no live or paper trading · no credentials · no production Trading OS integration ·
no dependency on, or imitation of, any previous Trading OS risk implementation.

## Documents

| # | Deliverable | File |
|---|---|---|
| 1 | Mathematical Constitution | [docs/constitution/01-mathematical-constitution.md](docs/constitution/01-mathematical-constitution.md) |
| 2 | Complete Symbol Registry | [docs/constitution/02-symbol-registry.md](docs/constitution/02-symbol-registry.md) |
| 3 | Units / Dimensions Matrix | [docs/constitution/03-units-dimensions.md](docs/constitution/03-units-dimensions.md) |
| 4 | Assumption Registry (+ Decision Register) | [docs/constitution/04-assumption-and-decision-registry.md](docs/constitution/04-assumption-and-decision-registry.md) |
| 5 | Candidate Wealth Dynamics (+ Economic Cost Accounting Identity) | [docs/constitution/05-wealth-dynamics.md](docs/constitution/05-wealth-dynamics.md) |
| 6 | Candidate Hard-Safety Architecture | [docs/constitution/06-hard-safety-architecture.md](docs/constitution/06-hard-safety-architecture.md) |
| 7 | Research Questions | [docs/constitution/07-research-questions.md](docs/constitution/07-research-questions.md) |
| 8 | Theorem Register | [docs/constitution/08-theorem-register.md](docs/constitution/08-theorem-register.md) |
| 9 | Known Mathematical Failure Modes (red team) | [docs/constitution/09-failure-modes-red-team.md](docs/constitution/09-failure-modes-red-team.md) |
| 10 | Alternative Mathematical Architectures | [docs/constitution/10-alternative-architectures.md](docs/constitution/10-alternative-architectures.md) |
| 11 | Literature / Novelty Research Plan | [docs/constitution/11-literature-novelty-plan.md](docs/constitution/11-literature-novelty-plan.md) |
| 12 | Dependency-Ordered Research Roadmap | [docs/constitution/12-research-roadmap.md](docs/constitution/12-research-roadmap.md) |
| 13 | Exactly One Smallest Next Task | [docs/constitution/13-next-task.md](docs/constitution/13-next-task.md) |

Math is written in GitHub-flavoured Markdown with `$…$` notation.

## Status vocabulary

Project items: CONFIRMED · PROVISIONAL · OPEN · BLOCKED · SUPERSEDED.
Mathematical claims: PROVED · PROVED BY CONSTRUCTION · DISPROVED · COUNTEREXAMPLE FOUND · REQUIRES ADDITIONAL ASSUMPTION · UNDEFINED ·
NOT YET PROVEN. Unresolved objects are marked **UNDEFINED — REQUIRES RESOLUTION**.
