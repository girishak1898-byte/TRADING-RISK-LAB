# TRADING RISK LAB

A greenfield mathematical research programme for a deterministic, independently testable **risk-control engine**.

**Governing question.** Given an opportunity, authoritative portfolio state, market state and uncertainty state, what is the maximum
action that remains inside every accepted safety constraint — including the possibility that the correct action is zero?

**Authority hierarchy.** AUTHORITY → SAFETY → MATHEMATICAL VALIDITY → NUMERICAL CORRECTNESS → STATISTICAL ROBUSTNESS → PERFORMANCE.
A later layer never overrides an earlier one.

## Status

**Phase 0 — Mathematical Constitution v0.2: NOT PASSED.** An independent review of the closure commit `5c486f0` found 3 CRITICAL,
8 IMPORTANT and 5 MINOR defects ([docs/review/phase0/09-closure-review-registry.md](docs/review/phase0/09-closure-review-registry.md)); the PASS
recorded at `5c486f0` is superseded. The three CRITICAL defects are corrected (acceptance gate §10), and so are CLOSURE-REV-006 (held vs filled
quantity, §11), CLOSURE-REV-018 (entry-order lifecycle exclusivity, §12) and CLOSURE-REV-008 (estimator failure semantics, §13); the other IMPORTANT
findings, including CLOSURE-REV-019, are open. Not adopted.
Revised after independent reviews:
v0.1.1 (adversarial review, revision note in 08), v0.2 (Phase-0 independent mathematical review) and the Phase-0 closure corrections
(revisions R3–R7 in 08; record and acceptance gate in [docs/review/phase0/](docs/review/phase0/README.md)). No trading code exists. No formula has
been adopted. No parameters have been chosen. The only code in the repository is documentation tooling: the linter
`tools/doccheck/check_constitution.py` and its mutation suite `tools/doccheck/mutation_suite.py` (no trading logic, no network).

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
| 14 | Formula Registry (single authority for equations; added v0.2) | [docs/constitution/14-formula-registry.md](docs/constitution/14-formula-registry.md) |
| — | Phase-0 independent review record (findings, red team, bibliography and cap audits, acceptance gate) | [docs/review/phase0/README.md](docs/review/phase0/README.md) |

Math is written in GitHub-flavoured Markdown with `$…$` notation.

## Status vocabulary

Project items: CONFIRMED · PROVISIONAL · OPEN · BLOCKED · SUPERSEDED.
Theorem statuses (08, v0.2): PROVED · DISPROVED · PROOF REQUIRES ADDITIONAL ASSUMPTIONS · UNDEFINED · NOT YET PROVEN.
Red-team classification (09) additionally uses COUNTEREXAMPLE FOUND (= the unrestricted claim is DISPROVED). Unresolved objects are marked
**UNDEFINED — REQUIRES RESOLUTION**.
