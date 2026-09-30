# Phase-0 Review — Reviewer Finding Registry (REV)

Source: the independent adversarial review of the theorem register launched in this session. It reviewed the **baseline
69a381d** and reported 4 BLOCKER, 9 MAJOR and 11 MINOR findings. Each finding below was **reproduced independently** in exact rational
arithmetic (evidence: [03-numerical-red-team.md](03-numerical-red-team.md) §B) before any status was assigned. No finding was accepted
because another model produced it.

Severity mapping: reviewer BLOCKER / MAJOR / MINOR is recorded as given; the **assessed severity** is this audit's own judgement
(CRITICAL = a stated safety guarantee or safety monotonicity property is false under its own stated assumptions; IMPORTANT = a false or
vacuous mathematical statement without a direct unsafe computation, or a missing assumption; MINOR = wording, notation, edge case).

Correction location: commit `8198877` applied corrections for these findings **before** this registry existed (see
[README](README.md) §2). Residual defects discovered while verifying those corrections are registered as AUD findings in
[02-self-audit-finding-registry.md](02-self-audit-finding-registry.md) and corrected in the follow-up correction commit.

---

### REV-001
| Field | Value |
|---|---|
| Reviewer severity / assessed | BLOCKER / **CRITICAL** |
| Document / section | 08 Theorem Register, T-10 (inherited by T-21 ⇐, T-25, T-06(c)) |
| Formula / proposition | T-10 tier S: open risk + reserved risk + new-order loss ≤ cushion ⇒ next wealth ≥ floor |
| Reviewer claim | Adding to a held position breaks the proof: exit cost and liquidation cost are super-additive in quantity, so per-lot charges under-state the combined position. |
| Independent reproduction | q=100 at 50, stop 49, exit cost 0.001n per share, liquidation cost 0.001n², no fees. Baseline open risk 100 (with liquidation credit), new-order loss 110, cushion 210. Untriggered close at 49.01: wealth change −228 ⇒ floor breached by 18. Combined-holding A-TRIG holds (9,762 ≥ 9,760). Under v0.1.1 definitions (no credit): cushion 220, breach 8. Incremental combined charge = 130; 100+130 = 230 = true worst case. |
| Status | **CONFIRMED** |
| Mathematical consequence | T-10 is false for scaling into a held instrument; every theorem resting on it inherits the defect. |
| Required correction | One exposure per instrument (gate G11) until an incremental combined-bound charge is proved including pending orders. |
| Correction location | `8198877`: G11, A-SCOPE-05, D-12, RQ-34. Residual partial-exit defect: AUD-001. |
| Test / proof obligation | Regression scenario (above) must be rejected by G11; RQ-34 proof of the incremental charge. |

### REV-002
| Field | Value |
|---|---|
| Reviewer severity / assessed | BLOCKER / **CRITICAL** |
| Document / section | 08 T-07; 05 DC-5 (baseline) |
| Formula / proposition | Liquidity monotonicity: Q^hard non-decreasing in ADV, non-increasing in spread |
| Reviewer claim | Open risk credited the liquidation cost Λ; budgets then rise with Λ (∂(f·B − R^open)/∂Λ = 1 − f > 0), so worse liquidity enlarges size. |
| Independent reproduction | Hold 1,000 sh at 50, stop 45, κ^out = 0.05, cash 200,000, f = 2%, new order loss 5.05n. Λ=500: W=249,500, open risk 4,550, budget 440, Q=87. Λ=100: W=249,900, open risk 4,950, budget 48, Q=9. Without the credit: budget −60 (Λ=500) vs −52 (Λ=100) — correct direction. |
| Status | **CONFIRMED** |
| Mathematical consequence | A safety monotonicity property of the hard envelope was false: deteriorating liquidity increased permitted size. |
| Required correction | Remove the Λ credit from open risk; register the resulting conservative over-charge. |
| Correction location | `8198877`: DC-5 revised, OC-1, T-07 restated. OC-1 had no defining table entry (AUD-022). |
| Test / proof obligation | Metamorphic test on held-instrument liquidity; T-07 proof under OC-1. |

### REV-003
| Field | Value |
|---|---|
| Reviewer severity / assessed | BLOCKER / **CRITICAL** |
| Document / section | 08 T-10 tier U; 06 H16; 06 §8 reservation vector |
| Formula / proposition | Tier-U floor preservation with pending orders charged at notional |
| Reviewer claim | Pending orders' fees are omitted when they are charged at notional; the reservation vector lacks the absolute-loss component. |
| Independent reproduction | Pending 100 @ 5 charged 500; new 100 @ 5.94 with $1 minimum commissions, L^abs = 596; cushion 1,096. Both fill, price → 0, both sold: loss 1,098 ⇒ wealth 2 below floor. |
| Status | **CONFIRMED** |
| Mathematical consequence | The only unconditional (tier U) floor guarantee was false. |
| Required correction | Reserve and charge pending orders at full L^abs (incl. fees). |
| Correction location | `8198877`: Z^res, H16 restated, reservation vector extended. |
| Test / proof obligation | Regression scenario; T-10 tier-U proof with Z^res. |

### REV-004
| Field | Value |
|---|---|
| Reviewer severity / assessed | BLOCKER / **IMPORTANT** (no hard-layer computation depends on T-25; it directs research) |
| Document / section | 08 T-25; also restated in 01 §5 |
| Formula / proposition | Floor breach ⊆ union of stop-assumption failures |
| Reviewer claim | Missing premise (state inside the cushion). |
| Independent reproduction | W_t = F_t − 1, no positions, no trade ⇒ W_{t+1} < F_t with no stop that could fail. |
| Status | **CONFIRMED** |
| Mathematical consequence | Statement false as written. |
| Required correction | Add the cushion premise wherever the statement appears. |
| Correction location | `8198877` fixed 08 only. **01 §5 still states it without the premise** and cites a non-existent ID "P-PB" → AUD-003. |
| Test / proof obligation | Counterexample as regression; corrected statement proved from T-10. |

### REV-005
| Field | Value |
|---|---|
| Reviewer severity / assessed | MAJOR / **CRITICAL** (T-10 false under its own assumptions) |
| Document / section | 08 T-10, T-20, T-21 |
| Formula / proposition | Case split triggered / untriggered |
| Reviewer claim | A stop triggered but not fully filled at the cut, and an entry fill whose stop is not yet live, are uncovered. |
| Independent reproduction | Hold 100 at 50, stop 49, κ = 0.1 (open risk 110); trigger just before the cut, mark 45 at the cut: wealth drop 500 > 110 while the later fill satisfies A-STOP. |
| Status | **CONFIRMED** |
| Mathematical consequence | Floor guarantee void for in-flight stops. |
| Required correction | Cover still-held quantities regardless of trigger state; require stop liveness from the fill. |
| Correction location | `8198877`: A-TRIG broadened, A-STOPLIVE added. **Residual:** partial-exit fee double count (AUD-001). |
| Test / proof obligation | Scenario library of triggered-unfilled and partially-filled stops. |

### REV-006
| Field | Value |
|---|---|
| Reviewer severity / assessed | MAJOR / **CRITICAL** (T-10 false under its own assumptions) |
| Document / section | 08 T-10, T-11(c); 05 §1 (fees per fill) |
| Formula / proposition | Fee bound φ(n) per order vs φ_j per fill |
| Reviewer claim | Per-execution minimum fees exceed the per-order schedule. |
| Independent reproduction | φ = max(1, 0.005k) per execution; exit 34/33/33 pays 3 > φ(100) = 1. |
| Status | **CONFIRMED** |
| Mathematical consequence | Loss exceeds open risk by the extra fees. |
| Required correction | Assume per-order fee semantics or use the worst case over splits. |
| Correction location | `8198877`: A-EXE-04. **Residual:** wording ("order of total quantity n") ambiguous between ordered and filled quantity (AUD-015). |
| Test / proof obligation | Fee-schedule load check (RQ-35). |

### REV-007
| Field | Value |
|---|---|
| Reviewer severity / assessed | MAJOR / **CRITICAL** (tier-G guarantee false) |
| Document / section | 08 T-10 tier G; 05 §5 |
| Formula / proposition | Tier-G exit bound (1−Γ)·p^stop |
| Reviewer claim | A-TRIG implies the tier-G valuation bound only if Γ·p^stop ≥ κ^out. |
| Independent reproduction | Γ = 1%, p^stop = 10, κ^out = 0.2, q = 100: A-TRIG allows 980; tier G needs 990; gap open risk short by 10. |
| Status | **CONFIRMED** |
| Mathematical consequence | Tier G weaker than tier S for small Γ; tier-G guarantee false. |
| Required correction | Exit bound min((1−Γ)p^stop, p^stop − κ^out). |
| Correction location | `8198877`: p^gx min form. **Residual:** 06 §2 tier table still states the old bound (AUD-004). |
| Test / proof obligation | Property: tier-G loss ≥ tier-S loss for all Γ. |

### REV-008
| Field | Value |
|---|---|
| Reviewer severity / assessed | MAJOR / **CRITICAL** (T-10 false as stated) |
| Document / section | 08 T-10 ("or all quantities unitised") |
| Formula / proposition | Flow handling in floor preservation |
| Reviewer claim | Unitisation does not protect the absolute floor. |
| Independent reproduction | F = F^abs = 90, W = 100, open risk 10 = K, withdrawal 5, stop fills at bound: W = 85 < 90. |
| Status | **CONFIRMED** |
| Mathematical consequence | Theorem false with intra-period withdrawals. |
| Required correction | Require X = 0 within the period. |
| Correction location | `8198877`: X = 0 in T-10; A-FLOW-01 extended. |
| Test / proof obligation | Regression scenario. |

### REV-009
| Field | Value |
|---|---|
| Reviewer severity / assessed | MAJOR / IMPORTANT |
| Document / section | 08 T-21 |
| Formula / proposition | Cushion necessity and sufficiency |
| Reviewer claim | The outcome set must import all T-10 hypotheses; otherwise (⇐) fails (e.g. withdrawal). |
| Independent reproduction | REV-008 scenario is an element of the baseline outcome set and violates (⇐). |
| Status | **CONFIRMED** |
| Mathematical consequence | (⇐) false as stated. |
| Required correction | Define the outcome set with all tier-S hypotheses. |
| Correction location | `8198877`. |
| Test / proof obligation | Proof re-check under the full hypothesis list. |

### REV-010
| Field | Value |
|---|---|
| Reviewer severity / assessed | MAJOR / IMPORTANT |
| Document / section | 08 T-06(c) |
| Formula / proposition | Conditional drawdown bound |
| Reviewer claim | Vacuous (continuous open risk ≤ cushion with open risk ≥ 0 already implies W ≥ F), unused assumptions, conflict with "no other orders", omits reserved risk. |
| Independent reproduction | Open risk ≥ 0 and open risk ≤ K ⇒ K ≥ 0 ⇒ W ≥ F ≥ F^dd ⇒ DD ≤ d^max, without A-STOP. Confirmed by inspection. |
| Status | **CONFIRMED** |
| Mathematical consequence | The theorem was true but circular. |
| Required correction | Restate per epoch with pre-cut adjustments and tier-S hypotheses within periods. |
| Correction location | `8198877`. |
| Test / proof obligation | Epoch-level Monte Carlo invariant. |

### REV-011
| Field | Value |
|---|---|
| Reviewer severity / assessed | MAJOR / IMPORTANT |
| Document / section | 08 T-17 |
| Formula / proposition | "Stop-risk-only envelope admits unbounded notional" |
| Reviewer claim | False when the exit-cost term has a positive floor or per-share fees exist. |
| Independent reproduction | f = 0.1%, p = 10, κ₀ = 0.01 ⇒ notional ≤ f·W·p/κ₀ = W. |
| Status | **CONFIRMED** |
| Mathematical consequence | Over-statement (the qualitative conclusion — stop budgets alone do not bound notional usefully — survives). |
| Required correction | Split into the naive stop-distance statement and the bounded-but-large statement. |
| Correction location | `8198877`. The bound introduced an unregistered symbol κ₀ (AUD-006). |
| Test / proof obligation | Parametric check of the bound. |

### REV-012
| Field | Value |
|---|---|
| Reviewer severity / assessed | MAJOR / IMPORTANT |
| Document / section | 08 T-19; 05 §7 |
| Formula / proposition | W^min lower bound |
| Reviewer claim | Omits flows and financing; contains future quantities while registered as derived. |
| Independent reproduction | Cash-only W = 100, withdrawal 100 ⇒ W_{t+1} = 0 while baseline W^min = 100. |
| Status | **CONFIRMED** |
| Mathematical consequence | "Surely" false; domain check not computable at decision time. |
| Required correction | Build W^min from time-t quantities; require X = 0 and Fin = 0. |
| Correction location | `8198877`. Residual: the corrected expression uses unregistered primed symbols (AUD-006); rewritten with Z^res in the correction commit. |
| Test / proof obligation | Property: W_{t+1} ≥ W^min on all tier-U paths. |

### REV-013
| Field | Value |
|---|---|
| Reviewer severity / assessed | MAJOR / IMPORTANT (the engine reads W from the snapshot, not from G; the defect invalidates analyses and proofs that use G across a corporate action) |
| Document / section | 05 §1–§2; T-15 |
| Formula / proposition | Position transition without corporate-action term |
| Reviewer claim | A 2:1 split with no fills is booked as a loss. |
| Independent reproduction | Forward split: booked −2,500 vs true 0. **Extension (this audit):** a 1:2 reverse split is booked as +5,000 — the anti-conservative direction. |
| Status | **CONFIRMED** (extended) |
| Mathematical consequence | G and ECAI false across corporate actions; reverse splits overstate wealth. |
| Required correction | Split periods at corporate-action instants with value-neutral restatement. |
| Correction location | `8198877` (05 §1). |
| Test / proof obligation | Ledger replay across split and reverse split. |

### REV-014
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 06 §7; T-05 |
| Formula / proposition | Induced throttle "0 beyond d^max" |
| Reviewer claim | Formula positive again for DD > 1. |
| Independent reproduction | d = 0.1, DD = 2: (d − DD)/(1 − DD) = 19/10. |
| Status | **CONFIRMED** |
| Mathematical consequence | No safety impact (budgets clamp to 0) but the stated property was false. |
| Required correction | Define the throttle as 0 for DD ≥ d^max. |
| Correction location | `8198877`. |
| Test / proof obligation | Unit check at DD ∈ {d, 1, 2}. |

### REV-015
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 08 T-05 proof |
| Formula / proposition | Monotonicity of the cushion in W |
| Reviewer claim | (i) day/week floors depend on W at the first epoch of a day/week; (ii) ν^ref independence unstated; (iii) "equivalently non-increasing in DD" false above the prior HWM; (iv) HWM update presumes intraday eligibility. |
| Independent reproduction | (i) slope 1 − ℓ at the first epoch — conclusion survives; (ii) by inspection; (iii) DD ≡ 0 above the HWM while K varies; (iv) by inspection of RQ-03. |
| Status | **CONFIRMED** (all four) |
| Mathematical consequence | Proof wording incomplete; conclusion holds. |
| Required correction | Amend proof. |
| Correction location | `8198877`. |
| Test / proof obligation | Metamorphic test including first-epoch-of-day states. |

### REV-016
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / **IMPORTANT** (it falsifies the scope of T-20(a) and of the "static floor" claim) |
| Document / section | 08 T-20(b); 06 §7 |
| Formula / proposition | Floor invariance under hold |
| Reviewer claim | Daily/weekly calendar resets ratchet the floor like a HWM. |
| Independent reproduction | ℓ^day = 2%, cash 50 + one share at 50, stop 49: K = 2, r = 1; close at 55: K = 7, r = 6; next day F^day = 102.9, K = 2.1 < r = 6. |
| Status | **CONFIRMED** |
| Mathematical consequence | "Static floor" must exclude calendar resets. |
| Required correction | Restrict T-20(a); add to ratchet list. |
| Correction location | `8198877`. |
| Test / proof obligation | Multi-day scenario. |

### REV-017
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 06 §7 |
| Formula / proposition | Per-trade budget = f^trd·W·ϑ_K |
| Reviewer claim | Requires f^trd ≤ f^strat and f^trd ≤ f^clr; the admissibility box allows otherwise. |
| Independent reproduction | By inspection of R^hard (min over five terms). |
| Status | **CONFIRMED** |
| Mathematical consequence | Statement conditional. |
| Required correction | State the condition. |
| Correction location | `8198877`. |
| Test / proof obligation | None beyond wording. |

### REV-018
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 06 §4 R^hard vs H3 |
| Formula / proposition | Strategy term in R^hard |
| Reviewer claim | R^hard omitted −SL present in H3. |
| Independent reproduction | By inspection. |
| Status | **CONFIRMED** |
| Mathematical consequence | Two definitions of the same budget disagreed. |
| Required correction | Align. |
| Correction location | `8198877`. SL itself remains UNDEFINED (AUD-028). |
| Test / proof obligation | Formula registry single definition (F-ID). |

### REV-019
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 08 T-01 testable invariant |
| Formula / proposition | Test oracle for the sanitiser |
| Reviewer claim | Finite negative ↦ 0 even for OPTIONAL models; a valid large value ↦ min for REQUIRED models; the stated either/or oracle was wrong. |
| Independent reproduction | By the sanitiser definition S-120. |
| Status | **CONFIRMED** |
| Mathematical consequence | A test built from the old oracle would have been wrong. |
| Required correction | Three-way oracle. |
| Correction location | `8198877`. |
| Test / proof obligation | Property test with the corrected oracle. |

### REV-020
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 08 T-02 |
| Formula / proposition | "Never half-up" |
| Reviewer claim | Half-even (Python default) also gives 345. |
| Independent reproduction | 1000.00/2.90 = 344.83…: HALF_EVEN 345, HALF_UP 345, FLOOR 344. |
| Status | **CONFIRMED** |
| Mathematical consequence | Rule must be "floor only". |
| Required correction | Reword. |
| Correction location | `8198877`. |
| Test / proof obligation | Red-team case B03/B04. |

### REV-021
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 08 T-03(a), (c) |
| Formula / proposition | Feasible set equality; verifier V |
| Reviewer claim | (a) needs n ≤ N̄ and non-negative budgets; (c) V undefined for finite negative proposals. |
| Independent reproduction | Negative budget: left side empty, right side {0}; negative proposal: max of the empty set. |
| Status | **CONFIRMED** |
| Mathematical consequence | Edge-case gaps. |
| Required correction | Include {0} and N̄ in (a); V(ñ<0) = 0. |
| Correction location | `8198877`. |
| Test / proof obligation | Fuzz V with negatives. |

### REV-022
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 08 P-12a |
| Formula / proposition | inf(A − B) ≤ inf A − inf B |
| Reviewer claim | Needs finite infima. |
| Independent reproduction | −∞ − (−∞) is undefined (float gives NaN, red-team case I07). |
| Status | **CONFIRMED** |
| Mathematical consequence | Edge case. |
| Required correction | Add finiteness. |
| Correction location | `8198877`. |
| Test / proof obligation | None. |

### REV-023
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 02, 06 §3, 08 |
| Formula / proposition | Notation and cross-references |
| Reviewer claim | (a) S-111 cites 06 §6 (should be §7); (b) S-100 cites §3 (should be §4); (c) plain ℓ unregistered; (d) 06 §3 uses f for a fraction, colliding with fill price f_j; (e) T-11(c) writes φ(e) for buy+sell fees; (f) summary omits P-12c. |
| Independent reproduction | All six verified by inspection of the baseline text. |
| Status | **CONFIRMED** |
| Mathematical consequence | Notation ambiguity. |
| Required correction | Fix each. |
| Correction location | `8198877` fixed (a), (b), (c), (e), (f) and the 06 §3 instance of (d). **Residual:** the fill-price symbol f_j still collides with the fraction family f^· (AUD-007). |
| Test / proof obligation | Mechanical symbol-closure check. |

### REV-024
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 05 §1 |
| Formula / proposition | Cash equation vs liabilities |
| Reviewer claim | No term for paying accrued liabilities; the identity closes only if payments sit in φ or Fin. |
| Independent reproduction | Payment P: true ΔC = ΔY = −P; baseline G gives +P overstatement. |
| Status | **CONFIRMED** |
| Mathematical consequence | G overstated wealth by liability payments. |
| Required correction | Add Pay and Accr. |
| Correction location | `8198877`. |
| Test / proof obligation | Ledger replay with payments. |

## Summary

| Status | Count | IDs |
|---|---|---|
| CONFIRMED | 24 | REV-001 … REV-024 |
| REJECTED | 0 | — |
| PARTIALLY CONFIRMED | 0 | — |
| REQUIRES ADDITIONAL ASSUMPTION | 0 | — |
| UNRESOLVED | 0 | — |

Assessed severity: CRITICAL 7 (REV-001, 002, 003, 005, 006, 007, 008) · IMPORTANT 7 (REV-004, 009, 010, 011, 012, 013, 016) ·
MINOR 10 (REV-014, 015, 017–024). Severity disagreements with the reviewer: REV-004 downgraded; REV-005, 006, 007, 008 and 016 upgraded.
Residual defects in the corrections: REV-001/005 → AUD-001; REV-004 → AUD-003; REV-006 → AUD-015; REV-007 → AUD-004;
REV-011/012/023 → AUD-006/007; REV-002 → AUD-022.
