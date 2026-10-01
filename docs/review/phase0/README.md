# Phase-0 Independent Mathematical Review

Purpose: close Phase 0 by independently reviewing the mathematical constitution. No implementation, no broker integration, no Alpaca
contact, no parameter optimisation, no backtesting, no Trading OS integration.

## 1. Commit chain (history is not rewritten)

| Stage | Commit | Content |
|---|---|---|
| BASELINE | `69a381d` | Phase-0 constitution v0.1 (immutable) |
| Pre-registry corrections | `8198877` | Fixes for the 24 reviewer findings, applied **before** this registry existed (v0.1.1). Retained, not rewritten. Every change in it is mapped to a REV ID in [01](01-reviewer-finding-registry.md). |
| REVIEW FINDINGS | `ad1a884` (the commit adding this directory) | Finding registries, numerical red team, bibliography and cap audits, pre-correction mechanical check output, and the documentation checker. **No constitution document is changed in this commit.** |
| CORRECTIONS | `f37c1b6` | Smallest documentation corrections for confirmed findings (v0.2), AUD-031 … AUD-033 found during correction, REV-025 … REV-036 from a second independent review, and the acceptance gate ([08-acceptance-gate.md](08-acceptance-gate.md)). |
| FINAL PHASE-0 CLOSURE CORRECTIONS | `5c486f0` | Closure re-derivation and a third independent review: realised costs no longer charged twice (F144, F145, F048, F078, F070), T-21 separated into sufficiency / necessity / equivalence, input classification of every hard cap, canonical numeric rule, committed mutation suite; AUD-034 … AUD-038 and the third independent review of `f37c1b6` (16 findings: AUD-039 … AUD-050, AUD-036 extended, one rejected), including the clamp of pending orders' per-share distances and the policy cap on ADV ([08-acceptance-gate.md](08-acceptance-gate.md) §9). |
| INDEPENDENT CLOSURE REVIEW | (no commit) | Review of `f37c1b6..5c486f0`: PHASE 0 **NOT PASSED** at `5c486f0` — 3 CRITICAL, 8 IMPORTANT, 5 MINOR ([09-closure-review-registry.md](09-closure-review-registry.md)). |
| CRITICAL CLOSURE CORRECTIONS | `80ca693` | Resolves CLOSURE-REV-001 (estimate-free gates, T-27; T-07, T-08 restated), CLOSURE-REV-002 (references at $W^{\mathrm{R}}$, F146, T-28) and CLOSURE-REV-003 (fee booking, F148, F149, T-29; T-10, T-19 rebuilt); IMPORTANT findings left open ([08-acceptance-gate.md](08-acceptance-gate.md) §10). |
| HELD/FILLED QUANTITY CORRECTION | `8dbb0ee` | Resolves CLOSURE-REV-006: held quantity, cumulative fill, order quantity and unfilled remainder kept apart (S-308, S-309), F145 rebuilt, F144 re-audited, validity and fail-closed charge F150, T-10 dependency (iii) closed; registers CLOSURE-REV-017 (MINOR), CLOSURE-REV-018 and 019 (IMPORTANT), not corrected ([08-acceptance-gate.md](08-acceptance-gate.md) §11). |
| ENTRY-ORDER LIFECYCLE CORRECTION | `a87b887` | Resolves CLOSURE-REV-018: entry-order lifecycle states (S-310, S-311, F151), G11 requires no `NON_TERMINAL` entry order on the instrument, A-SCOPE-05 restated, T-30 added, T-10 dependency (iv) closed ([08-acceptance-gate.md](08-acceptance-gate.md) §12). |
| ESTIMATOR FAILURE CORRECTION | the child of `a87b887` | Resolves CLOSURE-REV-008: `VALID` / `MISSING` / `INVALID` estimator status (F152), validation before the policy bound, a missing or invalid estimate gives $\alpha_t=0$; T-08, T-27 over valid estimates, T-31 added; checker gate ESTIMATOR_FAILURE_NOT_FAIL_CLOSED; registers CLOSURE-REV-020 (MINOR) ([08-acceptance-gate.md](08-acceptance-gate.md) §13). |
| EXECUTION / FLOOR-RISK CLOSURE (Wave A) | the child of `a5d40aa` | Resolves CLOSURE-REV-004, 005 and 019 together: stop-lots (F153), exit-order fee state (F154), future exit-fee charge (F155), exit-fee conservation (F156, T-32), owed exit-fee reservation (F157), one-stop charge admissible only at the minimum stop (T-33); F064–F066, F070, F072, F145, G8, A-TRIG and dependent assumptions restated; T-10 and T-19 rebuilt with no open dependency; checker gate EXIT_FEES_OR_STOP_LOTS_NOT_CHARGED; $7$ mutations ([08-acceptance-gate.md](08-acceptance-gate.md) §14). |

Ordering note: because `8198877` preceded the registry, the strict order BASELINE → FINDINGS → CORRECTIONS holds for the second
correction round; for the first round the registry documents, per finding, which lines of `8198877` correct it and whether the correction
was complete. Diffs `69a381d..8198877` and `<findings>..<corrections>` are each independently inspectable.

## 2. The independent reviewer

The review agent referred to in the Phase-0 closing instruction had already completed within this session before the instruction
arrived; its report (4 BLOCKER, 9 MAJOR, 11 MINOR) is registered verbatim in substance as REV-001 … REV-024 and every load-bearing claim
was reproduced independently in exact arithmetic ([03](03-numerical-red-team.md) §B). A second independent agent reviewed the
uncommitted correction draft; its twelve findings are registered as REV-025 … REV-036 (each reproduced independently, one upgraded to
CRITICAL) and corrected in the same correction commit.

## 3. Contents

| File | Brief section |
|---|---|
| [01-reviewer-finding-registry.md](01-reviewer-finding-registry.md) | §1 reviewer findings (REV) |
| [02-self-audit-finding-registry.md](02-self-audit-finding-registry.md) | §2 deliverable audit; §3–§12 findings from this audit (AUD) |
| [03-numerical-red-team.md](03-numerical-red-team.md) | §9 numerical red team; reproduction of REV/AUD numbers |
| [04-bibliography-audit.md](04-bibliography-audit.md) | §11 bibliography and novelty |
| [05-hard-safety-cap-audit.md](05-hard-safety-cap-audit.md) | §7 hard-safety cap audit |
| [07-mechanical-checks-pre-correction.md](07-mechanical-checks-pre-correction.md) | §3–§5 mechanical checks before correction |
| [08-acceptance-gate.md](08-acceptance-gate.md) | §13 acceptance gate and §14 correction record (added by the correction commit) |
| [09-closure-review-registry.md](09-closure-review-registry.md) | independent closure review of `5c486f0` (CLOSURE-REV-001 … 016), status NOT PASSED at that SHA, regression matrices of the critical corrections and of CLOSURE-REV-006, 018, 008 and of Wave A (004, 005, 019); CLOSURE-REV-017 … 020 found later |

Mechanical checker: `python3 tools/doccheck/check_constitution.py [--verbose]` — a documentation linter (no trading logic, no network,
no market data). Exit status 0 iff every gate count is zero. Its sensitivity is tested by `python3 tools/doccheck/mutation_suite.py`
(each injected defect must be detected; exit status 0 iff all are).

## 4. Limits of this review

- Independent re-verification of the bibliography was not possible: this session's egress policy blocks doi.org, api.crossref.org and
  the publisher hosts tried (onlinelibrary.wiley.com, dblp.org, www.sciencedirect.com, econpapers.repec.org, joss.theoj.org,
  marco-campi.unibs.it). The earlier subagent's verification and evidence URLs are recorded, labelled as such.
- Proofs are paper proofs about the specification, reviewed by this audit and by one independent agent. They are not mechanised and do
  not transfer to any future implementation (Art. 14).
