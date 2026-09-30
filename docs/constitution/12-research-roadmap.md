# 12 — Dependency-Ordered Research Roadmap (v0.2-draft)

**Phase-0 review status (v0.2, AUD-024).** An independent mathematical review of the Phase-0 constitution has been performed and its
confirmed findings corrected (reviewer findings REV-001 … REV-036 from two independent reviews, self-audit findings AUD-001 … AUD-033; record and acceptance gate in
`docs/review/phase0/`). It delivered part of R1's exit gate ahead of R0: symbol registry v0.2 with zero unregistered symbols, a formula
registry (14) and a machine-checked dimension table, each verified by `tools/doccheck/check_constitution.py`. Still open in R1: the
human controller's sign-off (D-11) and the definitional UNDEFINED items listed below. The review does not change the critical path:
R0 (13) remains the next task.

Each stage has an **entry gate** (what must be true to start) and an **exit gate** (evidence required to finish). A stage's output is
never "done" because a document or code exists (OUTPUT ≠ COMPLETION). No stage involves a broker, credentials, network access at
execution time, paper trading or live trading.

```
R0 Scope decisions ──► R1 Constitution review & symbol freeze ──► R2 Wealth/ECAI spec ──► R3 Hard-envelope spec
                                                                                           │
             ┌──────────────────────────────┬──────────────────────────────┬──────────────┤
             ▼                              ▼                              ▼              ▼
     R4 Proof review (hard layer)   R5 Numerical contract spec   R6 Input registry +   R8 Data source &
             │                              │                    decision schema       empirical studies
             └──────────────┬───────────────┘                         │               (RQ-04/05/06/21/22)
                            ▼                                         │                     │
                R7 Reference implementation (hard layer only) ◄───────┘                     │
                            │                                                               │
                            ▼                                                               ▼
                R7b Test suite: property / metamorphic / differential / fuzz / replay   R9 Policy proposals (θ)
                            │                                                               │
                            └───────────────────────────┬───────────────────────────────────┘
                                                        ▼
                  R10 Uncertainty & tail layer research ──► R11 Objective + certified advantage (power first)
                                                        │
                                                        ▼
                  R12 Baseline comparison & validation protocol execution ──► R13 Novelty memo ──► R14 Integration contract (spec only)
```

| Stage | Content | Entry gate | Exit gate |
|---|---|---|---|
| **R0** Scope decisions | D-01..D-07 and D-12 (13) | this constitution delivered | signed decision record |
| **R1** Constitution review & symbol freeze | independent adversarial review of 01–14 (**performed for Phase 0**, see status above); resolve definitional UNDEFINED items that do not need data ($B_t$ candidates narrowed, trigger semantics, calendar, ruin definition, $\mathrm{SL}$ definition, D-08..D-11) | R0 | human sign-off (D-11); registry with zero unregistered symbols (**met at v0.2**); every UNDEFINED item either resolved or scheduled |
| **R2** Wealth dynamics & ECAI specification | corporate actions, flows/unitisation timing, day/week boundaries, $\Lambda$ interface (model left pluggable but monotone) | R1 | identities re-proved with the final accounting rules; worked ledger examples |
| **R3** Hard-envelope specification v1 | final constraint catalogue for v0 scope, gates, parameter-admissibility box, reservation vector, reason codes | R2 | every constraint monotone (proved) with tier label; dimension check passes |
| **R4** Proof review | T-01..T-05, T-10, T-11, T-13, T-17a, T-17b, T-18, T-20a..T-25 re-proved against the R3 spec by an independent reviewer; optional mechanised pilot (RQ-33) | R3 | reviewed proofs; each mapped to a testable invariant |
| **R5** Numerical contract v1 | representation choice (RQ-16), rounding table per field, serialisation schema, hashing, magnitude bounds | R3 | T-24 argument per field; canonical-serialisation test vectors |
| **R6** Required-input registry & decision-record schema (engine side) | $\mathcal R^{\mathrm{req}}$, TTLs (RQ-19), read-set check method (RQ-18) | R3, R5 | read-set ⊆ registry demonstrable by construction |
| **R7** Reference implementation — **hard layer only** | pure Python, typed inputs, exact arithmetic, no I/O; outputs $Q^{\mathrm{hard}}$, all $Q_k$, binding set, tiers, reservation vector, evidence hash | R4, R5, R6 **and explicit human approval to begin coding** | builds; import deny-list check passes (no network/broker/persistence modules) |
| **R7b** Test suite | every testable invariant in 08; independent slow oracle; fuzzing; replay across processes/hash seeds/locales | R7 | all invariants machine-checked; mutation testing shows tests detect injected defects |
| **R8** Data and empirical studies | data source with knowledge times (RQ-29); gap-through-stop (RQ-04), stop slippage (RQ-05), liquidity droughts (RQ-06), halts (RQ-21), co-exceedance (RQ-22) — **train/validation periods only** | R0 (source), R2 (definitions) | calibrated distributions with CIs and sub-period stability; test period untouched |
| **R9** Policy proposals | evidence packs proposing values for $\theta$; the human sets values (Art. 16) | R3, R8 | signed parameter set v1 |
| **R10** Uncertainty & tail layer | ambiguity-set justification (RQ-12), ES estimation, feasibility-defined model caps (T-09) | R8 | justified model or documented rejection |
| **R11** Objective & certified advantage | power analysis first (RQ-14); then $J$ (RQ-13), certificate, multiple testing (RQ-15) | R10 | decision on D-10 backed by power curves |
| **R12** Baseline comparison | protocol of 10 §3 executed once on the final test sample | R7b, R9, R11 | report; simplest non-dominated candidate recommended |
| **R13** Novelty memo | L-6 | R12 | documented search; claims only where supported |
| **R14** Integration contract | Phase 19 schema and impossibility properties — specification only, no integration | R12 | contract reviewed; still no connection to Trading OS |

**Critical path:** R0 → R1 → R2 → R3 → {R4, R5, R6} → R7 → R7b. R8 can start after R0 (data sourcing) and R2 (definitions) and runs in
parallel with R3–R7b; it is the long pole for everything statistical.

**Stop conditions (escalate to the human controller):** any theorem in the R4 set is disproved against the final spec; a required input
cannot be sourced without inventing authority; R8 shows A-STOP failure rates that make tier S meaningless for the intended universe
(then tier G/U must carry the guarantee and deployment capacity falls sharply); R11 shows certification is infeasible (then D-10 must be
revisited).
