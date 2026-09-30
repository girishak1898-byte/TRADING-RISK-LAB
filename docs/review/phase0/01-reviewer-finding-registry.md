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

## Second independent review (of the uncommitted v0.2 correction draft)

Source: a second independent agent, launched in this session after the first correction draft, reviewed the new mathematics adversarially
(no CRITICAL by its own rating; 5 IMPORTANT, 7 MINOR). Every numeric claim was **reproduced independently** in exact rational arithmetic before
a status was assigned; the assessed severity is this audit's own. All twelve are corrected in the correction commit.

### REV-025
| Field | Value |
|---|---|
| Reviewer severity / assessed | IMPORTANT / IMPORTANT |
| Document / section | 08 T-21 (v0.2 draft); 14 F143; 06 §7; 01 §7; 10 AA-1 note |
| Formula / proposition | T-21 "only if" with the OC-4 double charge |
| Reviewer claim | With an order partially filled at τ_t the charge exceeds the attainable worst loss, so the restated iff is false. |
| Independent reproduction | Exact: 100 sh held marked 52, order 200 at limit 50, stop 49, κ^out(n)=0.001n, no fees, Λ_t=1, K_t=439: charge 310+240=550 > K_t+Λ_t=440, worst attainable change −439 ⇒ W_{t+1}=F_t (no breach). |
| Status | **CONFIRMED** |
| Mathematical consequence | False necessity claim in the draft; sufficiency unaffected. |
| Required correction | Restrict (⇒) to ledgers without partially filled orders and without stale-reservation excess; state the general slack as Λ_t + OC-4 over-charge + ledger excess. |
| Correction location | correction commit (v0.2). |
| Test / proof obligation | Boundary scenario per case. |

### REV-026
| Field | Value |
|---|---|
| Reviewer severity / assessed | IMPORTANT / IMPORTANT |
| Document / section | 08 T-20a; 04 A-EXE-06 (v0.2 draft; the gap exists since the baseline) |
| Formula / proposition | Cushion invariance under hold, static floor |
| Reviewer claim | A stop triggered with nothing executed at the cut is neither untriggered nor fully exited; the proof misses it and the invariant fails. |
| Independent reproduction | Exact: q=100, stop 49, κ^out=0.1, no fees; τ_t bid/ask 49.99/50.01 (Λ_t=1), K_t=R^open_t=110; τ_{t+1} triggered, unexecuted, bid/ask 48.9/49.0 (Λ=5): XV=4,890 ≥ 4,890 (A-TRIG holds), ΔW=−109, K_{t+1}=1 < r^open_{t+1}=5. |
| Status | **CONFIRMED** |
| Mathematical consequence | T-20a false under its listed hypotheses. |
| Required correction | A-EXE-06: every stop triggered in the period is fully executed by the cut; fail-closed: triggered or partially executed stop ⇒ RECOVERY. |
| Correction location | correction commit (v0.2). |
| Test / proof obligation | Regression scenario above. |

### REV-027
| Field | Value |
|---|---|
| Reviewer severity / assessed | IMPORTANT / IMPORTANT |
| Document / section | 02 S-290; 05 §5; 04 A-TRIG (v0.2 draft) |
| Formula / proposition | Exposure quantity q^exp in T-10 case (2′) |
| Reviewer claim | The definition gives q^exp=q_{i,t} for a held position, so A-TRIG says nothing about shares filled in the period on a partially filled order. |
| Independent reproduction | Text comparison: case (2′) uses q^exp=q_{i,t}+e, not covered by S-290's two cases. |
| Status | **CONFIRMED** |
| Mathematical consequence | Proof step (2′) not supported by the assumption as defined. |
| Required correction | Third case: held position with a pending remainder of the same order, q^exp=q_{i,t}+e. |
| Correction location | correction commit (v0.2). |
| Test / proof obligation | Definition check. |

### REV-028
| Field | Value |
|---|---|
| Reviewer severity / assessed | IMPORTANT / **CRITICAL** (upgraded: the floor is breached under the theorem's own hypotheses; same class as AUD-001) |
| Document / section | 08 T-10 cases (2), (2′); 06 §5; 04 A-AUTH-05 (the gap exists since the baseline) |
| Formula / proposition | Pending-order reservation vs A-TRIG inputs |
| Reviewer claim | The reserved L^stop was computed with reservation-time inputs (κ^out, fees, stop) while A-TRIG and r^open use τ_t inputs; nothing ties them. |
| Independent reproduction | Exact: pending 100 at limit 50, stop 49, reserved with κ^out=0.1 ⇒ R^res=110=K_t; at τ_t F111 gives κ^out=0.5; fill and exit at the A-TRIG bound 48.5 ⇒ ΔW=−150, W_{t+1}=F_t−40. |
| Status | **CONFIRMED** |
| Mathematical consequence | T-10 false as stated; the hard layer could admit a floor breach inside its assumptions (also after a stop is widened). |
| Required correction | Charge each pending order the larger of the ledger reservation and its F108 vector re-evaluated at τ_t (F144); cite in T-10. |
| Correction location | correction commit (v0.2). |
| Test / proof obligation | Metamorphic: raising any F111 input or widening a stop after reservation never lowers the charged reservation. |

### REV-029
| Field | Value |
|---|---|
| Reviewer severity / assessed | IMPORTANT / IMPORTANT |
| Document / section | 04 A-TRIG sufficient conditions; 05 §5; 06 §2; 09 FM-OPS-9; 14 F140 (v0.2 draft) |
| Formula / proposition | Two-part split envelope F140 |
| Reviewer claim | With several exit orders per exposure (a child stop per entry fill) more than two fee-bearing parts arise; the stated sufficient conditions then do not imply A-TRIG. |
| Independent reproduction | Exact: new order 100 at 50, stop 49, κ^out=0.1, fee max(1,0.005k) per order, L^stop=110+1+2=113=K_t; fills 34/33/33 each with its own stop exiting at 48.9: XV=4,890−3=4,887 < 4,888, ΔW=−114 ⇒ W_{t+1}=F_t−1. With N^ex=3: charge 115, F072 holds. |
| Status | **CONFIRMED** |
| Mathematical consequence | False sufficiency claim; T-10 itself unaffected (assumes A-TRIG). |
| Required correction | Generalise F140 to N^ex+1 parts (N^ex declared, unknown ⇒ per-execution worst case); align 06 §2 with 04. |
| Correction location | correction commit (v0.2). |
| Test / proof obligation | Regression scenario above. |

### REV-030
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 05 §5; 08 T-10, T-10N, T-20a; 09 FM-OPS-9 (v0.2 draft) |
| Formula / proposition | AUD-001 example with Λ_t=0 |
| Reviewer claim | v0.2 forces Λ_t ≥ φ^sell(100)=1, so the held-position example no longer breaches; the v0.2-relevant breach is a new order. |
| Independent reproduction | Exact: Λ_t=1, K=111: ΔW=−111 ⇒ W_{t+1}=F_t; new order with L^stop=112: ΔW=−113 ⇒ F_t−1; with F140 L^stop=113 ⇒ F_t. |
| Status | **CONFIRMED** |
| Mathematical consequence | Examples mislabelled for v0.2 accounting. |
| Required correction | Label Λ_t=0 as v0.1.1 accounting; restate v0.2 examples as a new order. |
| Correction location | correction commit (v0.2). |
| Test / proof obligation | — |

### REV-031
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 08 T-10 case (2′) (v0.2 draft) |
| Formula / proposition | Final inequality of case (2′) |
| Reviewer claim | The displayed bound drops +Λ_{i,t}, which step (3) and T-21 (⇐) need. |
| Independent reproduction | The intermediate line carries +Λ_{i,t}; the final one does not. |
| Status | **CONFIRMED** |
| Mathematical consequence | Presentation gap. |
| Required correction | Keep +Λ_{i,t} in the final bound. |
| Correction location | correction commit (v0.2). |
| Test / proof obligation | — |

### REV-032
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 08 T-10, T-10N; 14 F120; 06 §2 (v0.2 draft) |
| Formula / proposition | Assumption lists |
| Reviewer claim | T-10 omits A-ACC-01…03 needed by F055; the race counterexample removes A-AUTH-02, not A-AUTH-04; F120 omits A-AUTH-02, A-AUTH-05, A-ACC-04, A-ACC-06, A-EXE-01…03; 06 §2 folds the quantity bound into A-MKT-05; "without anomaly" unused. |
| Independent reproduction | Text comparison of the four lists. |
| Status | **CONFIRMED** |
| Mathematical consequence | Lists incomplete or mis-attributed. |
| Required correction | Align the lists; relabel the race item; drop the unused condition. |
| Correction location | correction commit (v0.2). |
| Test / proof obligation | Checker THEOREM_STATUS_ASSUMPTION_INCONSISTENCIES. |

### REV-033
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 05 §5 add-on paragraph (baseline numbers) |
| Formula / proposition | Add-on numbers |
| Reviewer claim | "Per-lot charges 210" and "100+130=230" use the rejected Λ credit. |
| Independent reproduction | Exact: r^open(100)=110, L^stop(100)=110 ⇒ per-lot 220; combined worst 230 = r^open−Λ+F068 = 110−10+130; r^open+F068 = 240. |
| Status | **CONFIRMED** |
| Mathematical consequence | Stale numbers. |
| Required correction | Restate with OC-1. |
| Correction location | correction commit (v0.2). |
| Test / proof obligation | — |

### REV-034
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / **IMPORTANT** (upgraded: T-19's bound was false under its v0.1.1 hypotheses) |
| Document / section | 05 §7 F070; 08 T-19 |
| Formula / proposition | W^min with non-super-additive fees |
| Reviewer claim | Selling part of a holding at price 0 and valuing the remainder with its own fee gives two fees where F070 charges one. |
| Independent reproduction | Exact: fee max(1,0.005k), 100 sh, 50 sold at 0 (fee 1), remainder Λ=1 (A-ACC-05 with equality): W_{t+1}=C−Y−2 < W^min=C−Y−1. |
| Status | **CONFIRMED** |
| Mathematical consequence | T-19's lower bound false without the envelope. |
| Required correction | Apply F140 to φ^sell_{·,0} in F070; cite in T-19. |
| Correction location | correction commit (v0.2). |
| Test / proof obligation | Regression scenario above. |

### REV-035
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 05 §4b; 08 T-11 |
| Formula / proposition | Cost table and ledger semantics |
| Reviewer claim | No row for execution cost of other (manual) exits; the fees row does not mention F140; T-11 does not say what FILL does under A-AUTH-05 or that the ledger's Op is not R^open_t. |
| Independent reproduction | Text inspection. |
| Status | **CONFIRMED** |
| Mathematical consequence | Documentation gaps; no missing economic term or unregistered duplicate. |
| Required correction | Add the row and the two sentences. |
| Correction location | correction commit (v0.2). |
| Test / proof obligation | Checker COST_CONSERVATION_TABLE_MISSING. |

### REV-036
| Field | Value |
|---|---|
| Reviewer severity / assessed | MINOR / MINOR |
| Document / section | 10 AA-1 row; 07 RQ-32; 06 §6; 08 T-02; 10 AA-1 note; 01 §7 |
| Formula / proposition | Cross-document wording |
| Reviewer claim | A-STOP where A-TRIG is meant; E-18 cited for F095 instead of E-05; OC-4 slack missing in the T-21 qualifications. |
| Independent reproduction | Text inspection. |
| Status | **CONFIRMED** |
| Mathematical consequence | Wording inconsistencies. |
| Required correction | Replace references and add the qualification. |
| Correction location | correction commit (v0.2). |
| Test / proof obligation | Cross-reference check. |

## Summary

| Status | Count | IDs |
|---|---|---|
| CONFIRMED | 36 | REV-001 … REV-036 |
| REJECTED | 0 | — |
| PARTIALLY CONFIRMED | 0 | — |
| REQUIRES ADDITIONAL ASSUMPTION | 0 | — |
| UNRESOLVED | 0 | — |

Assessed severity: CRITICAL 8 (REV-001, 002, 003, 005, 006, 007, 008, 028) · IMPORTANT 12 (REV-004, 009, 010, 011, 012, 013, 016, 025, 026, 027,
029, 034) · MINOR 16 (REV-014, 015, 017–024, 030, 031, 032, 033, 035, 036). Severity disagreements with the reviewers: REV-004 downgraded; REV-005, 006, 007, 008, 016, 028 and 034 upgraded.
Residual defects in the corrections: REV-001/005 → AUD-001; REV-004 → AUD-003; REV-006 → AUD-015; REV-007 → AUD-004;
REV-011/012/023 → AUD-006/007; REV-002 → AUD-022.
