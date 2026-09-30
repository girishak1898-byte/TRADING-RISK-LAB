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
| FINAL PHASE-0 CLOSURE CORRECTIONS | the child of `f37c1b6` | Closure re-derivation and a third independent review: realised costs no longer charged twice (F144, F145, F048, F078, F070), T-21 separated into sufficiency / necessity / equivalence, input classification of every hard cap, canonical numeric rule, committed mutation suite; AUD-034 … AUD-038 and the third independent review of `f37c1b6` (16 findings: AUD-039 … AUD-050, AUD-036 extended, one rejected), including the clamp of pending orders' per-share distances and the policy cap on ADV ([08-acceptance-gate.md](08-acceptance-gate.md) §9). |

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

Mechanical checker: `python3 tools/doccheck/check_constitution.py [--verbose]` — a documentation linter (no trading logic, no network,
no market data). Exit status 0 iff every gate count is zero. Its sensitivity is tested by `python3 tools/doccheck/mutation_suite.py`
(each injected defect must be detected; exit status 0 iff all are).

## 4. Limits of this review

- Independent re-verification of the bibliography was not possible: this session's egress policy blocks doi.org, api.crossref.org and
  the publisher hosts tried (onlinelibrary.wiley.com, dblp.org, www.sciencedirect.com, econpapers.repec.org, joss.theoj.org,
  marco-campi.unibs.it). The earlier subagent's verification and evidence URLs are recorded, labelled as such.
- Proofs are paper proofs about the specification, reviewed by this audit and by one independent agent. They are not mechanised and do
  not transfer to any future implementation (Art. 14).
