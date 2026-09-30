# Phase-0 Review — Self-Audit Finding Registry (AUD)

Scope: all 13 deliverables at commit `8198877` (baseline `69a381d` + pre-registry corrections), audited against one another, against the
brief's Phase-0 acceptance criteria, and with the mechanical checker `tools/doccheck/check_constitution.py` (pre-correction output:
[07-mechanical-checks-pre-correction.md](07-mechanical-checks-pre-correction.md)). Severity scale as in
[01-reviewer-finding-registry.md](01-reviewer-finding-registry.md). Every numeric claim is reproduced in
[03-numerical-red-team.md](03-numerical-red-team.md).

## A. Deliverable-set and cross-document audit (brief §2)

| Deliverable | Present at `8198877` | Contradictions found |
|---|---|---|
| 01 Mathematical Constitution | yes | 01 §5 restates T-25 without its premise and cites non-existent "P-PB" (AUD-003); §3.3 ledger block omits Z^res, Q^res (AUD-025); §7 tier-U set omits fees (AUD-027) |
| 02 Symbol Registry | yes | 29 incomplete rows, 21 duplicate keys, parameters not individually registered (AUD-006/007/008) |
| 03 Units / Dimensions Matrix | yes | no machine-readable table; mixed-unit rows; ℓ^min units undefined (AUD-011) |
| 04 Assumption Registry | yes | assumption classes absent; theorem → assumption mapping incomplete; hidden assumptions (AUD-016/017) |
| 05 Wealth Dynamics | yes | no cost-conservation table; undocumented conservative duplicates (AUD-012); symbol collisions (AUD-007) |
| 06 Hard-Safety Architecture | yes | §2 tier table stale vs T-10 (AUD-004); §3 row 6 wrong ID (AUD-005); §5 g_k(0)=0 wording (AUD-026); §10 omits G11 (AUD-025); H3 depends on UNDEFINED SL (AUD-028); central-invariant leak via model-supplied inputs (AUD-002) |
| 07 Research Questions | yes | none found |
| 08 Theorem Register | yes | T-10 still false for partial exits (AUD-001); T-20(a) partial-state gap (AUD-014); non-canonical format/statuses (AUD-013); A-EXE-04 wording (AUD-015) |
| 09 Failure Modes | yes | formula IDs F-xx collide with the canonical formula-ID scheme (AUD-021) |
| 10 Alternative Architectures | yes | the brief's six baseline names not all explicit (AUD-020) |
| 11 Literature / Novelty Plan | yes | verification provenance overstated (AUD-019); novelty table not in required categories (AUD-029) |
| 12 Research Roadmap | yes | does not record Phase-0 review status (AUD-024) |
| 13 Next Task | yes | as 12 (AUD-024) |
| Formula Registry | **no** | required by the brief §4 (AUD-010) |

---

### AUD-001
| Field | Value |
|---|---|
| Severity | **CRITICAL** |
| Document / section | 08 T-10 (v0.1.1), 04 A-TRIG, A-EXE-04 |
| Formula / proposition | Tier-S floor preservation with a partially executed stop |
| Finding | The v0.1.1 case split applies A-TRIG to the *remaining* quantity with its own hypothetical exit fee, while the partial fill already paid the per-order fee: fees are counted as φ(filled) + φ(remaining) > φ(q). |
| Independent reproduction | q = 100 at 50, stop 49, κ^out = 0.1, per-order fee max(1, 0.005n), Λ_t = 0 (admissible), open risk 111 = K. Stop fills 50 at 48.9 paying fee 1 (A-STOP and A-EXE-04 hold); remaining 50 valued at the A-TRIG bound 2,444. Wealth change −112 ⇒ W_{t+1} = F_t − 1. |
| Status | **CONFIRMED** |
| Mathematical consequence | T-10 (and T-21 ⇐, T-25, T-06(c)) false under the v0.1.1 hypotheses. |
| Required correction | Replace A-TRIG by a **position-level exit-value bound**: exit proceeds + liquidation value of the remainder − all exit fees ≥ q(p^stop − κ^out(q)) − φ^sell(q). The v0.1.1 counterexample violates it (4,888 < 4,889), and the proof becomes a single case. |
| Test / proof obligation | Regression scenario; rewritten proof in 08 T-10. |

### AUD-002
| Field | Value |
|---|---|
| Severity | **CRITICAL** (violates the central invariant by design ambiguity) |
| Document / section | 01 Art. 6; 06 §5; 02 S-054, S-085, S-041 |
| Formula / proposition | "Models may reduce permissible action; never enlarge hard limits" |
| Finding | The hard caps consume estimate/model quantities (κ^out, Λ, ADV, Γ̂). Only Γ has a policy floor. Nothing forbids an advanced model from supplying an optimistic κ^out or ADV, which would enlarge H1–H6, H12, H13 through the *inputs* rather than through b^mod. |
| Independent reproduction | By construction: Q_k is non-increasing in κ^out (T-08) and non-decreasing in ADV (T-07); an optimistic model value therefore raises Q^hard. |
| Status | **CONFIRMED** |
| Mathematical consequence | The invariant 0 ≤ b^allow ≤ b^hard holds only relative to inputs a model may control. |
| Required correction | Hard-layer statistics are hard-layer components: frozen, versioned definitions under human authority, each combined with a policy bound in the conservative direction (κ^out ≥ κ^min, Γ ≥ Γ^min, Λ ≥ Λ^floor, ADV by a fixed estimator). Advanced models may only propose b^mod. |
| Test / proof obligation | Metamorphic: replacing any model with an arbitrarily optimistic one never increases Q^hard. |

### AUD-003
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 01 §5 "Structural decomposition" |
| Finding | Restates T-25 without the cushion premise (REV-004 was fixed in 08 only), mentions only A-STOP, and cites the non-existent ID "P-PB". |
| Independent reproduction | Text inspection at `8198877`. |
| Status | **CONFIRMED** |
| Required correction | Restate with premise and A-TRIG; cite T-25. |
| Test / proof obligation | Cross-reference check. |

### AUD-004
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 06 §2 tier table |
| Finding | Tier S lists only A-STOP/A-TRIG (T-10 also needs A-STOPLIVE, A-EXE-04, G11, X = 0); tier G still states the exit bound (1−Γ)p^stop instead of the min form. |
| Independent reproduction | Text comparison 06 §2 vs 08 T-10 and 05 §5. |
| Status | **CONFIRMED** |
| Required correction | Align tier table with T-10. |
| Test / proof obligation | Assumption-ID cross-check (tier rows cite the same IDs as T-10). |

### AUD-005
| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 06 §3 row 6 |
| Finding | "No cash bound → H15"; buying power is H14 (H15 is margin). Present in baseline and `8198877`. |
| Status | **CONFIRMED** |
| Required correction | H15 → H14. |
| Test / proof obligation | — |

### AUD-006
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 02 and all documents using math |
| Finding | UNREGISTERED_SYMBOLS = 103 keys (checker). Includes: every individual policy parameter (registered only as a list inside θ); spaces 𝔖, 𝒪, Θ, 𝒱, 𝔇, Ξ; the wealth-transition map G; verifier V; proposal ñ; index letters (s, u, …); number sets; σ(·); state blocks x^A…x^U; generic example symbols (R, p, L); brief-name aliases (Q_risk …); theorem-local symbols (T-11 ledger, T-22, T-24, P-12a/b); κ₀; estimates Γ̂, ℙ̂; primed comparison copies. |
| Independent reproduction | [07-mechanical-checks-pre-correction.md](07-mechanical-checks-pre-correction.md). |
| Status | **CONFIRMED** |
| Required correction | Complete the registry (global rows, alias rows, proof-local namespaces with explicit scope); rename where a local symbol shadows a global one without need. |
| Test / proof obligation | UNREGISTERED_SYMBOLS = 0 in the checker. |

### AUD-007
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 02, 01, 05, 06, 08, 09 |
| Finding | Genuine duplicate meanings: n (candidate size vs fill quantity n_j); f (policy fractions vs fill price f_j, f^in, f^out); r (return vs cost-chain r_{j,k}); τ (epoch instant vs fill instant τ_j); δ (lattice step vs confidence); ℓ (layer index in Art. 1 vs per-share loss); c (cluster vs cost component c_{j,k} vs step level c_k vs RU dummy); u (epoch dummy vs unit roundoff vs utility); m (mid vs m_K/m_G vs data dimension); W (wealth vs Wasserstein W_p); ε (tolerance vs chance level vs mixture weight); K (cushion vs chain length); T (horizon T vs time unit); π (policy π_t vs π^ref vs π̂); p, b in the Kelly formula (price family and budget); γ (realised gap vs gate dummy); x_k (state vs generic reals). Plus alias rows registered as separate keys (p^stop, 𝒫, ϑ_K, ℙ). |
| Independent reproduction | Checker DUPLICATE_MEANING_SYMBOLS = 21 plus manual review of bound variables. |
| Status | **CONFIRMED** |
| Required correction | Rename (the rename map is recorded with the correction commit); mark aliases. |
| Test / proof obligation | DUPLICATE_MEANING_SYMBOLS = 0. |

### AUD-008
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 02 §J (S-160 … S-188) |
| Finding | 29 rows lack type, domain, codomain, units, sign, valid range, source. S-056 and S-146 carry two different units in one row. |
| Status | **CONFIRMED** |
| Required correction | Full columns for every row; split mixed-unit rows. |
| Test / proof obligation | INCOMPLETE_REGISTRY_ROWS = 0. |

### AUD-009
| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 01, 02, 06, 08 |
| Finding | Multi-letter names in italic math (DD, MDD, BP, PB, IM, MM) read as products of single-letter symbols. |
| Status | **CONFIRMED** (checker keys D, M, B, P) |
| Required correction | Upright operator names (\mathrm). |
| Test / proof obligation | Symbol closure. |

### AUD-010
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | whole constitution |
| Finding | No canonical formula registry; equations have no stable IDs; the same formula is stated in several documents (e.g. R^hard in 06 §4 and H1–H4, L^stop in 02, 05, 06). |
| Status | **CONFIRMED** |
| Required correction | Create 14-formula-registry.md (F001…) with the brief's fields; tag every display equation and every inline ":=" definition. |
| Test / proof obligation | UNTAGGED_EQUATIONS = 0; INCOMPLETE_FORMULA_ROWS = 0. |

### AUD-011
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 03 |
| Finding | Dimension checks (E-01…E-17) are manual prose; no machine-readable dimension table; ℓ^min units undefined ([$/sh] or [1]); S-056/S-146 mixed units. No silent dimensional error was found in the formulas themselves (E-08 was already fixed in baseline). |
| Status | **CONFIRMED** |
| Required correction | Canonical `dimtable` in 03 linked to registry IDs; every formula-registry row carries a machine-checked `dim:` expression; fix ℓ^min units. |
| Test / proof obligation | DIMENSIONAL_CONFLICTS = 0. |

### AUD-012
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 05, 06 |
| Finding | No economic cost conservation table. Undocumented duplicates: (i) broker buying power may already net open orders while H14 subtracts C^res again; (ii) realised strategy loss reduces B (through W) and is subtracted again as SL; (iii) composition of Λ (does it include exit fees?) is unspecified, so the scope of OC-1 is unclear; (iv) reservation idempotency: an opportunity already reserved and re-evaluated as new is charged twice (conservative) or, if the ledger entry is dropped, not at all (unsafe). |
| Status | **CONFIRMED** |
| Required correction | Conservation table in 05; OC register (OC-1 … OC-3); Λ composition defined; idempotency obligation recorded for the integration contract. |
| Test / proof obligation | Every row of the table has one state-transition location; duplicates are OC-registered or UNRESOLVED with an owner. |

### AUD-013
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 08 |
| Finding | Statuses outside the brief's five-value vocabulary (PROVED BY CONSTRUCTION, COUNTEREXAMPLE FOUND, REQUIRES ADDITIONAL ASSUMPTION); compound statuses on one ID (T-01, T-02, T-03, T-06, T-08, T-09, T-10, T-11, T-12, T-20, T-22); "COUNTEREXAMPLE ATTEMPT" and "NUMERICAL EDGE CASES" fields missing for most entries; T-14–T-16, T-18, T-23, T-24 abbreviated. |
| Status | **CONFIRMED** |
| Required correction | Rewrite 08 in the canonical eight-field format; split compound statements into separate IDs (e.g. T-01 / T-01N). |
| Test / proof obligation | UNREVIEWED_THEOREMS = 0 (every ID carries all eight fields and exactly one status). |

### AUD-014
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 08 T-20(a) |
| Finding | After a worst-case partial stop exit under a static floor, the remaining position's open risk (its exit fee) exceeds the new cushion. |
| Independent reproduction | Scenario of AUD-001 with a static floor: K' = 0, remaining open risk 1. |
| Status | **CONFIRMED** |
| Required correction | T-20(a) requires "no partially executed stop at the cut" → PROOF REQUIRES ADDITIONAL ASSUMPTIONS. |
| Test / proof obligation | Scenario regression. |

### AUD-015
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 04 A-EXE-04; 08 T-10, T-11(c) |
| Finding | "Fees over all fills of one order of total quantity n are ≤ φ(n)" is ambiguous between ordered and filled quantity; the proof step "change ≥ −L^stop(e)" needs fees ≤ φ(e) for filled quantity e. The final bound ≥ −L^stop(n) survives either reading. |
| Status | **CONFIRMED** |
| Required correction | State A-EXE-04 on cumulative filled quantity. |
| Test / proof obligation | Fee-schedule check (RQ-35). |

### AUD-016
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 04; 08; 06 |
| Finding | Assumptions carry type labels but not the brief's seven classes; theorems T-01–T-05, T-13, T-14, T-22, T-24 rely on "standing assumptions" without IDs; hard constraints H1–H16 do not cite assumption IDs; no assumption is mapped to a fail-closed check. |
| Status | **CONFIRMED** |
| Required correction | Reclassify; add "used by" and "fail-closed check" columns; cite IDs in 08 and 06. |
| Test / proof obligation | UNRECORDED_ASSUMPTIONS = 0 (every theorem and constraint cites IDs; every risk-relevant assumption has a check or a named research owner). |

### AUD-017
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 05, 06, 08 |
| Finding | Hidden assumptions used in proofs or definitions but not registered: Λ ≥ 0; A-MKT-05 also for partial fills; ADV > 0; price bounds p^min/p^max referenced ("prices within policy bounds") but never defined; no overflow/underflow in T-22; snapshot and reservation ledger form one consistent cut; the period contains no other orders; exact arithmetic (A-NUM-01) not cited by T-01–T-03. |
| Status | **CONFIRMED** |
| Required correction | Register each with class and fail-closed check. |
| Test / proof obligation | As AUD-016. |

### AUD-018
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 01 §9 numerical contract |
| Finding | Red team ([03](03-numerical-red-team.md) §A) shows contract gaps: (J01–J03) Python's JSON parser accepts NaN, Infinity and 1e400 → inf by default — a fail-open path for the "reject NaN at the boundary" rule; (Z03, Z05) negative zero can be *produced* internally (−0 × 5) and serialises as "-0.00", so boundary rejection alone does not guarantee canonical output; (X01) Fraction + float silently yields a float; (HC01–HC04) half-cent rounding of prices and fees is not covered by the direction table (fees must round up; limit prices must never round down); (B01–B02) float under-sizing makes a float and an exact implementation disagree, which breaks differential testing. |
| Status | **CONFIRMED** |
| Required correction | Extend 01 §9 (parser rules, −0 normalisation, no mixed-type arithmetic, cent quantisation directions). |
| Test / proof obligation | Each red-team case becomes a boundary test. |

### AUD-019
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 11 §0 |
| Finding | "115 checked: 111 verified, 4 corrected" was produced by a subagent via web search; the evidence URLs were not recorded in the repository; this audit could not re-verify any reference independently because the session's egress policy blocks doi.org, api.crossref.org and the publisher hosts tried. |
| Status | **CONFIRMED** |
| Required correction | Qualify the claim; record evidence URLs; mark re-verification as open. |
| Test / proof obligation | Future session with the listed hosts allowed re-runs the check mechanically. |

### AUD-020
| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 10 §1 |
| Finding | Baselines are present but not under the brief's six names; "advanced robust model" is not an explicit comparison row; BL-1 wording "δ_q·one share" is ill-formed for fractional lattices. |
| Status | **CONFIRMED** |
| Required correction | Add the explicit six-name list and mapping. |

### AUD-021
| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 09 Part A |
| Finding | IDs F-01 … F-36 collide with the canonical formula-ID namespace required by the brief. |
| Status | **CONFIRMED** |
| Required correction | Re-key to RT-01 … RT-36 and point each to F### IDs. |

### AUD-022
| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 01 Art. 12, 05 DC-5, 02 S-188 |
| Finding | OC-1 is referenced but has no defining table (checker: UNDEFINED_CROSS_REFERENCES = 1). |
| Status | **CONFIRMED** |
| Required correction | OC register table in 05. |

### AUD-023
| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 02 |
| Finding | Alias rows registered as separate keys: p^stop (S-034/S-063), 𝒫 (S-134/S-177), ϑ (S-111/S-168), ℙ (S-130/S-183). |
| Status | **CONFIRMED** |
| Required correction | Mark aliases explicitly. |

### AUD-024
| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 12, 13 |
| Finding | Roadmap does not record that an independent review of Phase 0 has been performed and corrected; 13 states "no further mathematical work can safely proceed past R1" without reflecting this review. |
| Status | **CONFIRMED** |
| Required correction | Record status; keep exactly one next task. |

### AUD-025
| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 01 §3.3; 06 §10 |
| Finding | x^B omits Z^res and Q^res; the evaluation order checks G7–G10 but omits G11. |
| Status | **CONFIRMED** |
| Required correction | Add both. |

### AUD-026
| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 06 §5 |
| Finding | "All consumptions satisfy g_k(0) = 0" while H8, H9, H11, H13 are written with existing exposure on the consumption side. |
| Status | **CONFIRMED** |
| Required correction | State that existing terms belong to b_k. |

### AUD-027
| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 01 §7 |
| Finding | Tier-U invariant set stated as "long notional ≤ K"; after REV-003 it must include fees (Z^open + Z^res ≤ K). |
| Status | **CONFIRMED** |
| Required correction | Restate. |

### AUD-028
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 06 §4 R^hard, H3 |
| Finding | The central hard budget R^hard contains SL_{s,t}, which is UNDEFINED; no rule says what happens meanwhile. |
| Status | **CONFIRMED** |
| Required correction | Fail-closed rule: while SL is undefined the strategy term is inactive only if the human policy explicitly disables strategy budgets; otherwise every decision is NO_TRADE (Art. 4). |
| Test / proof obligation | Authority test: SL absent ⇒ NO_TRADE unless the policy flag disables H3. |

### AUD-029
| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 11 §3 |
| Finding | Novelty table uses free-text statuses, not the brief's categories (KNOWN / KNOWN COMBINATION / POSSIBLE SYSTEMS NOVELTY / POSSIBLE MATHEMATICAL NOVELTY — REQUIRES FORMAL COMPARISON / UNSUPPORTED NOVELTY CLAIM). |
| Status | **CONFIRMED** |
| Required correction | Re-map every component to closest prior literature and one category. |

### AUD-030
| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | README |
| Finding | Document index lacks the formula registry and the review record. |
| Status | **CONFIRMED** |
| Required correction | Update index. |

### AUD-031

*Found during correction (after the findings commit), while building the machine-checked dimension table; recorded here so that the
chain findings → corrections stays auditable.*

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 06 §3 (naive form), 08 T-17, 09 F-04/F-28, 10 AA-2 (at `8198877`) |
| Formula / proposition | $\lfloor R/\ell\rfloor$ and the volatility-targeted size "risk fraction × $W/\hat\sigma$" |
| Finding | (i) $\lfloor\cdot\rfloor$ is applied to $R/\ell$, which has dimension [sh]; the expression is meaningful only for $\delta_q=1$ sh, where the unit is silently dropped — the one-share special case hides the inconsistency. (ii) risk fraction × $W/\hat\sigma$ has dimension [USD·day$^{1/2}$], not a notional. |
| Independent reproduction | Dimension evaluator (`dim_eval` in the checker): `floor(R/ell)` raises "floor of a dimensioned quantity {sh: 1} … (floor must act on a dimensionless count)"; `f_trd*W/sigma_hat` evaluates to USD·day^(1/2). With $\delta_q=0.1$ sh, $R=1$ USD, $\ell=0.3$ USD/sh the naive form returns $3$ (read as 3 sh) while the lattice-correct $\delta_q\lfloor R/(\delta_q\ell)\rfloor=3.3$ sh. |
| Status | **CONFIRMED** |
| Mathematical consequence | Formulas silently depend on the choice $\delta_q=1$ sh; the volatility-target formula has no numeric meaning. |
| Required correction | $\delta_q\lfloor R/(\delta_q\ell)\rfloor$ everywhere (F095, F110); notional $=W\sigma^{\mathrm{target}}/\hat\sigma$ (F133); register as 03 E-18, E-19 and FM-DIM-1, FM-DIM-2. |
| Test / proof obligation | DIMENSIONAL_CONFLICTS = 0 with the floor rule enforced. |

### AUD-032

*Found during correction, while rewriting 08 in canonical form.*

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 08 T-21 (at `8198877`); 06 §7 "why the cushion line"; 10 AA-1 |
| Formula / proposition | "$W_{t+1}\ge F_t$ on all tier-S outcomes **iff** $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t$" |
| Finding | R1 removed the $\Lambda$ credit from open risk (OC-1) but left T-21's necessity proof unchanged. The attainable worst case is $W_t-(R^{\mathrm{open}}_t-\Lambda_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n))$, so the "only if" direction is false whenever $\Lambda_t>0$. |
| Independent reproduction | Exact: $q=100$ at $50$, stop $49$, $\kappa^{\mathrm{out}}=0.1$, no fees, $\Lambda_t=5$, $K_t=106<r^{\mathrm{open}}=110$; the worst attainable outcome (stop filled at $48.9$) gives $W_{t+1}=F_t+1$. |
| Status | **CONFIRMED** |
| Mathematical consequence | A false theorem in the register (necessity direction); the safety direction (sufficiency) is unaffected, so no hard-layer decision was unsafe. Claims that the cushion line is *the* maximal floor-safe policy hold exactly only on a flat book. |
| Required correction | Restate T-21 with $K_t+\Lambda_t=E_t-F_t$ (F143); state that F120 is sufficient and conservative by exactly $\Lambda_t$ (OC-1); qualify 06 §7, 10 AA-1, 01 §7 and OPEN-1. |
| Test / proof obligation | Simulator: at the exact boundary the attained comonotone outcome gives $W_{t+1}=F_t$; one lattice step more breaches. |

### AUD-033

*Found during correction, while re-deriving the T-10 proof in canonical form.*

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 08 T-10 proof (at `8198877`: cases "held", "new or pending order on a fresh instrument"); 04/06 hypotheses |
| Formula / proposition | Tier-S floor preservation when an order is partially filled at $\tau_t$ |
| Finding | An order partially filled before the cut is a held quantity *and* a pending remainder on the same instrument; the proof covered neither case for it. The conclusion holds only because the full reservation $L^{\mathrm{stop}}(n')$ is held until the order is terminal (T-11), a hypothesis T-10 did not state. Releasing the filled part early is unsafe under super-additive exit costs. |
| Independent reproduction | Exact: $\kappa^{\mathrm{out}}(n)=0.001n$, no fees, order $n'=200$ at limit $50$, stop $49$; $100$ filled and marked at $52$; the remaining $100$ fill at $50$ and the whole exposure exits at its A-TRIG bound: loss $440$. Charge with remainder-only reservation: $r^{\mathrm{open}}(100)+L^{\mathrm{stop}}(100)=310+110=420<440$; with the full reservation: $310+240=550\ge440$. |
| Status | **CONFIRMED** |
| Mathematical consequence | The v0.1.1 proof of T-10 was incomplete; the theorem needs the full-reservation hypothesis, which also creates a registered conservative duplicate. |
| Required correction | Add case (2′) and the hypothesis to T-10; register OC-4 in 05 §4a; state in the cost conservation table that reservations are released only at terminal state. |
| Test / proof obligation | Regression scenario above: remainder-only reservation must breach; full reservation must not. |

## Summary

| Severity | Count | IDs |
|---|---|---|
| CRITICAL | 2 | AUD-001, AUD-002 |
| IMPORTANT | 20 | AUD-003, 004, 006, 007, 008, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019, 028, 029, 031, 032, 033 |
| MINOR | 11 | AUD-005, 009, 020, 021, 022, 023, 024, 025, 026, 027, 030 |

All 33 are CONFIRMED (AUD-031, AUD-032 and AUD-033 were found during correction and are marked as such). None is REJECTED. All are addressed in
the correction commit except where the correction is itself a research obligation (AUD-019 independent bibliography re-verification;
AUD-028 definition of SL), which remain explicitly UNRESOLVED with a fail-closed rule or owner.
