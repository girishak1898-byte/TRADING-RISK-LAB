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

### AUD-034

*Found during Phase-0 closure (re-derivation of the partial-fill construction, after commit `f37c1b6`).*

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 05 §4a OC-4, §4b; 06 §5 F144; 08 T-10 case (2′), T-21; 14 F144 (at `f37c1b6`) |
| Formula / proposition | Charge of a partially filled order: $r^{\mathrm{open}}_i$ plus the full-order reservation $L^{\mathrm{stop}}(n')$ (OC-4) |
| Finding | The construction is safe but counts **realised** costs a second time: the entry fees already paid (in $W_t$ through cash) and the filled quantity's entry-to-stop risk are charged again inside the full-order reservation. It also made T-21's "only if" false (REV-025) and kept a ledger value (max with $R^{\mathrm{led}}$) that is not the worst case. |
| Independent reproduction | Exact: order $6$ sh at $50$, stop $49$, $\kappa^{\mathrm{out}}(n)=0.1+0.01n$, fee $\max(1,0.005k)$ per order, $N^{\mathrm{ex}}=2$; $2$ filled (fee $1$ paid), mark $52$, $\Lambda=1.02$: worst loss $12.94$; draft charge $19.20$, over-charge $5.24=q(p^{\mathrm{lim}}-p^{\mathrm{stop}}+\kappa(q))+\phi^{\mathrm{split}}(q)+\phi^{\mathrm{paid}}$ — contains the paid fee. |
| Status | **CONFIRMED** |
| Mathematical consequence | A realised cost counted twice (conservative); T-21 necessity false in the presence of such orders. |
| Required correction | Exact exposure charge F145 ($r^{\mathrm{pf}},g^{\mathrm{pf}},u^{\mathrm{pf}}$, fees paid excluded); F144 re-evaluates every reservation from the order state (remaining quantity, remaining cost) without a ledger floor; OC-4 eliminated; T-10 case (2′) and T-21 restated; A-AUTH-02 carries the order state; A-AUTH-05 ledger-only. |
| Test / proof obligation | Exhaustive enumeration: worst loss $=$ charge $-\Lambda$ in every state; two-period chains: realised plus remaining never below the total worst case (08 T-10 (o)). Third-review findings 3 and 8 (reproduced against `f37c1b6`: reading F144's quantity as the remainder gives $W_{t+1}=F_t-179$; the full ledger vector counts $5{,}001$ of realised cash twice in H14) have this root; the closure F144 names the total quantity $n'$ and charges only remaining quantity, notional and cash. |

### AUD-035

*Found during Phase-0 closure (review of the OC register against "no realised cost counted twice").*

| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 05 §4a OC-2, OC-3; 06 §4–§5 F048, F074, H3; 14 F048, F074, F078 (at `f37c1b6`) |
| Formula / proposition | $\mathrm{BP}^{\mathrm{avail}}=\min(\mathrm{BP},C^{\mathrm{avail}})-C^{\mathrm{res}}$; H3 with the current base $B_t$ |
| Finding | Two registered over-charges were avoidable: pending cash is deducted twice when the broker figure already nets open orders (OC-2), and a realised strategy loss reduces $B_t$ and is subtracted again as $\mathrm{SL}$ (OC-3, a realised loss counted twice). Neither was needed for any theorem. |
| Independent reproduction | Algebra: with $\mathrm{BP}=C^{\mathrm{avail}}-C^{\mathrm{res}}$ (broker nets orders) the draft gives $C^{\mathrm{avail}}-2C^{\mathrm{res}}$; with loss $\ell$ in window, the draft H3 budget falls by $f^{\mathrm{strat}}_s\ell+\ell$. |
| Status | **CONFIRMED** |
| Mathematical consequence | Conservative double deductions, one of a realised loss. |
| Required correction | F048 $=\min(\mathrm{BP}_t,C^{\mathrm{avail}}_t-C^{\mathrm{res}}_t)$ (broker figure only restricts); H3 and F074 use the window-start base $B^{\mathrm{win}}_s$; OC-2, OC-3 eliminated. T-05 unaffected ($B^{\mathrm{win}}_s$ constant; F048 falls by $\Delta$ under a consistent cash reduction). |
| Test / proof obligation | Metamorphic: broker figure raised ⇒ H14 cap not raised. |

### AUD-036

*Found during Phase-0 closure (numerical-boundary requirement); extended and upgraded by the third independent review (finding 10).*

| Field | Value |
|---|---|
| Severity | IMPORTANT (upgraded from MINOR at closure: two conforming parsers could read different snapshots from identical bytes) |
| Document / section | 01 §9 items 1, 10, 12, 13 (at `f37c1b6`) |
| Formula / proposition | Canonical numeric form |
| Finding | "Decimal string at a declared scale" did not fix the grammar: exponent notation (a decimal library may print `1E+2`), a strictly parsed `1e400` (finite `1E+400`), input with more digits than the scale, and `-0.00` on input were not excluded, so two conforming implementations could produce different bytes. |
| Independent reproduction | Probes: strict decimal JSON parse of `1e400` yields `Decimal('1E+400')`, finite; `Decimal('1E+2')` accepted; `-0.00` preserved by a decimal parse. |
| Status | **CONFIRMED** |
| Mathematical consequence | Replay determinism (T-14) not guaranteed across implementations. |
| Required correction | 01 §9 item 17: exact grammar per declared scale, rejection rules, exact-rational parse, trapped decimal contexts, directed rounding only, serialisation grammar. |
| Test / proof obligation | Grammar test vectors (accept/reject lists) at R5. Third-review extension (reproduced): a common JSON parser keeps the last duplicate key (`{"cash":"100","cash":"-5"}` reads $-5$); a decimal constructor accepts `nan`, `-iNfInItY`, `' 1.5 '`, `1_000` and non-ASCII digits; `Fraction ** Fraction(1, 2)` and `math.sqrt(Fraction)` return floats; decimal `//` truncates ($-7\,/\!/\,2=-3$) and yields $-0$. Correction: 01 §9 item 17 (g)–(j) (duplicate keys rejected, ASCII digits, key order by code point, minimal escaping, SHA-256, UTC integer nanoseconds, runtime-type invariant, floor not truncation). |

### AUD-037

*Found during Phase-0 closure (manual review of every "iff" claim after the checker reached zero).*

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 06 §7 throttle-family table, row "Linear in DD" (present since the baseline) |
| Formula / proposition | "Floor-safe alone: single trade iff $f^{\mathrm{trd}}\le\mu^{K}d^{\max}$" |
| Finding | The "only if" direction is false. With $B=W$, only $F^{\mathrm{dd}}$ active and no other risk, safety of one trade needs $f^{\mathrm{trd}}H(1-\mathrm{DD})(1-\mathrm{DD}/d^{\max})\le H(d^{\max}-\mathrm{DD})$ for all $\mathrm{DD}\in[0,d^{\max})$, i.e. $f^{\mathrm{trd}}\le d^{\max}$; $\mu^{K}$ does not enter. |
| Independent reproduction | Exact grid ($1{,}000$ points of DD): $d^{\max}=10\%$, $\mu^{K}=0.5$: $f^{\mathrm{trd}}=5\%$ safe, $f^{\mathrm{trd}}=10\%$ safe although $f^{\mathrm{trd}}>\mu^{K}d^{\max}$, $f^{\mathrm{trd}}=10.1\%$ unsafe. |
| Status | **CONFIRMED** |
| Mathematical consequence | A false equivalence in a comparison table (no hard-layer computation uses it). |
| Required correction | State the exact condition $f^{\mathrm{trd}}\le d^{\max}$ with its hypotheses; qualify the cushion row's "iff" as "in every state". |
| Test / proof obligation | Grid check above. |

### AUD-038

*Found during Phase-0 closure (manual review of reservation identities).*

| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 05 §7 F070; 08 T-19; 14 F070 (at `f37c1b6`) |
| Formula / proposition | $W^{\min}_{t+1}=C_t-Y_t-Z^{\mathrm{res}}_t-L^{\mathrm{abs}}(n)-\sum_i\phi^{\mathrm{sell}}_{i,0}(q_{i,t})-\bar A_{t+1}$ |
| Finding | With the full reservation held until terminal, $Z^{\mathrm{res}}_t$ of a partially filled order subtracts the whole order's cost although the filled part's cost and fees are already out of $C_t$; its exit fee is also charged in both $Z^{\mathrm{res}}_t$ and the sum over holdings. A realised cost is subtracted twice (conservative). |
| Independent reproduction | Order $6$ sh at $50$, $2$ filled (cost $100$, fee $1$ paid): `f37c1b6`'s $W^{\min}$ subtracts $6\cdot50+\phi^{\mathrm{buy}}(6)+\phi_0(6)$ plus $\phi_0(2)$, i.e. $100$ of filled cost and $1$ of paid fee again; exhaustive enumeration of the closure form (prices to $0$, remaining fills, up to $N^{\mathrm{ex}}+1$ fee-bearing parts): $W_{t+1}\ge W^{\min}_{t+1}$ always, with equality attained. |
| Status | **CONFIRMED** |
| Mathematical consequence | $W^{\min}$ too low (log-domain condition T-19 more restrictive than necessary); no unsafe result. |
| Required correction | $W^{\min}_{t+1}=C_t-Y_t-C^{\mathrm{res}}_t-L^{\mathrm{abs}}(n)-\sum_i\phi^{\mathrm{split}}_{i,0}(\bar q_i)-\bar A_{t+1}$ with remaining commitments (F144) and $\bar q_i$ the largest quantity that can be held. |
| Test / proof obligation | Enumeration above. |

### AUD-039

*Found by the third independent review of `f37c1b6` (finding 1); reproduced independently.*

| Field | Value |
|---|---|
| Severity | **CRITICAL** (a load-bearing theorem false inside its own hypotheses) |
| Document / section | 08 T-10 case (2′) and case (2), T-21, T-25, T-06c; 05 §5; 06 §5; 14 F144, F145 (at `f37c1b6` and in the closure draft) |
| Formula / proposition | Per-share distance $p'^{\mathrm{lim}}-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(n')$ of the unfilled part of a pending order |
| Finding | G7 checks $p^{\mathrm{stop}}_o<p^{\mathrm{lim}}$ only when the order is placed; a stop trailed to or above the limit later (T-06c asks for trailing) makes the distance negative, and the proof's "using $p'^{\mathrm{lim}}>p^{\mathrm{stop}}_i$" has no hypothesis behind it. The unfilled part may not fill, so a negative term is not a credit. |
| Independent reproduction | Exact: order $n'=200$ at $50$, stop $49$ at reservation ($\kappa=0.1$, ledger $220$), $100$ filled; at $\tau_t$ $m=52$, $\Lambda_t=1$, stop $51$, $\kappa^{\mathrm{out}}(n)=0.00005n^2$: `f37c1b6` charge $150+220=370=K_t$, worst loss $399$ ⇒ $W_{t+1}=F_t-29$. Closure draft F144 without the clamp on a fresh pending order (stop $51$, limit $50$, $\kappa=0.1$, \$1 minimum fees, $100$ sh): charge $-87$ against worst loss $1.2$. Randomised search: $1{,}126$ breaches in $5{,}882$ trials with the stop at or above the limit (reviewer); $1{,}772$ understatements in $8{,}795$ such trials of the unclamped closure F145 (this audit). |
| Status | **CONFIRMED** |
| Mathematical consequence | T-10 (and with it T-21 (a), T-25, T-06c) false for such states at `f37c1b6`; no other theorem affected. |
| Required correction | Clamp the unfilled part's per-share distance at $0$ in F144 and F145 (tier G likewise); T-10 cases (2), (2′) prove $e\,x\le(n'-q)x^+$; T-21 (b), (c) require inactive clamps; T-10N regression; FM-OPS-11. |
| Test / proof obligation | Clamped charge: $0$ understatements in $46{,}200$ enumerated scenarios (stops $2$ below to $3$ above the limit) and in $20{,}000$ randomised trials; the T-10N scenario must breach without the clamp. |

### AUD-040

*Found by the third independent review (finding 2); reproduced independently.*

| Field | Value |
|---|---|
| Severity | **CRITICAL** (a statistical estimate could enlarge a hard cap without limit) |
| Document / section | 01 Art. 6 amendment; 06 §5, §5a; 08 T-01 invariant; 14 F111; 02 S-006, S-054 (at `f37c1b6`) |
| Formula / proposition | $\mathrm{ADV}_{i,t}$ in H12, H13; the cap invariant; the cluster map |
| Finding | ADV had no policy bound, so H12, H13 grow with the estimate; 06 §5 itself said none exists. The stated invariant "an arbitrarily optimistic estimate never increases $Q^{\mathrm{hard}}$" is false for $\hat\kappa^{\mathrm{out}}$ below a pessimistic value. A statistical cluster map (RQ-10) could split clusters and enlarge H9, H10. |
| Independent reproduction | H13 with $\rho^{\mathrm{ex}}h^{\mathrm{ex}}=0.1$ day, $q=Q^{\mathrm{res}}=0$: ADV $5{,}000$ ⇒ $500$ sh; ADV $10^7$ ⇒ $1{,}000{,}000$ sh. H1 with $f^{\mathrm{trd}}B=1{,}000$, limit $50$, stop $49$, $\kappa^{\min}=0.001$: $\hat\kappa^{\mathrm{out}}=0.5$ ⇒ $666$ sh, $\hat\kappa^{\mathrm{out}}=0$ ⇒ $953$ sh. |
| Status | **CONFIRMED** |
| Mathematical consequence | "No estimate can enlarge a hard cap beyond policy" did not hold for H12, H13 (and H9, H10 under a statistical cluster map). |
| Required correction | $\mathrm{ADV}=\min(\mathrm{ADV}^{\mathrm{est}},\mathrm{ADV}^{\max})$ (F111; S-299, S-300); statistical cluster maps merge-only (S-006); invariant restated: $Q^{\mathrm{hard}}$(any estimates) $\le Q^{\mathrm{hard}}$(every estimated input at its policy bound). |
| Test / proof obligation | Metamorphic test of the restated invariant over all estimated inputs. |

### AUD-041

*Found by the third independent review (finding 4); reproduced.*

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 06 §5 (at `f37c1b6`) versus 01 Art. 4 |
| Formula / proposition | "Missing estimator output ⇒ the policy bound is used for $\kappa^{\mathrm{out}},\Gamma,\Lambda$" |
| Finding | The policy bound is the most permissive admissible value, so an estimator outage loosened every cap it enters. |
| Independent reproduction | H1 example of AUD-040: estimate $0.5$ ⇒ $666$ sh; estimate missing ⇒ floor ⇒ $953$ sh. |
| Status | **CONFIRMED** |
| Mathematical consequence | UNKNOWN treated as the permissive bound (Art. 4 violated); caps stayed within policy, so no hard limit was exceeded. |
| Required correction | A missing $\hat\kappa^{\mathrm{out}}$, $\hat\Gamma$, $\hat\Lambda$ or $\mathrm{ADV}^{\mathrm{est}}$ ⇒ $\alpha_t=0$ (F111; 06 §5; 01 Art. 6). |
| Test / proof obligation | Estimator-outage test ⇒ NO\_TRADE naming the input. |

### AUD-042

*Found by the third independent review (finding 5); reproduced.*

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 08 T-10, T-21, T-10N; 04 A-ACC-05 (at `f37c1b6`) |
| Formula / proposition | Tier S with an exposure without an authoritative stop (D-06) |
| Finding | D-06 charges $u^{\mathrm{open}}$ but A-TRIG is undefined without a stop, and tier S listed neither A-MKT-01 nor A-ACC-05; T-10N listed "D-06 removed" although D-06 was not a hypothesis. |
| Independent reproduction | Algebra: without A-ACC-05 a model value $\Lambda_{t+1}>q\,m+\phi_0(q)$ loses more than $u^{\mathrm{open}}$. |
| Status | **CONFIRMED** |
| Mathematical consequence | T-10 tier S and T-21 did not cover books with stopless positions. |
| Required correction | T-10 case (1′) with A-MKT-01 and A-ACC-05; T-21 attainability and charges include F066. |
| Test / proof obligation | Simulator: stopless position, prices to $0$ ⇒ $\Delta=-u^{\mathrm{open}}+\Lambda$. |

### AUD-043

*Found by the third independent review (finding 6); reproduced.*

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 08 T-19 (at `f37c1b6`) |
| Formula / proposition | $W_{t+1}\ge W^{\min}_{t+1}$ "surely" |
| Finding | The assumption list omitted A-MKT-05, A-EXE-05, A-AUTH-02, A-AUTH-04, A-ACC-01…04 and F144. |
| Independent reproduction | $C=1{,}000$, pending $10$ @ $10$ ($W^{\min}=900$): fill at $12$ then prices → $0$ ⇒ $880$; manual buy $90$ @ $10$ ⇒ $W_{t+1}=0$. |
| Status | **CONFIRMED** |
| Mathematical consequence | Theorem stated with missing hypotheses. |
| Required correction | T-19 imports T-10's common hypotheses (A-ACC-07 with $\mathrm{Accr}\le\bar A$). |
| Test / proof obligation | The two scenarios as assumption-violation regressions. |

### AUD-044

*Found by the third independent review (finding 7); reproduced.*

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 04 A-ACC-07, A-FLOW-01, A-EXE-04, A-TRIG (at `f37c1b6`) |
| Formula / proposition | Fail-closed rules "known accrual charged before $K_t$", "pending withdrawal charged against $K_t$", "per-execution fees ⇒ worst case over splits" |
| Finding | No formula implemented any of the three charges; F140 covers only the exit side. |
| Independent reproduction | $K_t=r^{\mathrm{open}}=110$, accrual $5$, stop exits at its bound ⇒ $W_{t+1}=F_t-5$; $100$ one-share entry executions at a \$1 minimum pay \$100 against $\phi^{\mathrm{buy}}(100)=1$. |
| Status | **CONFIRMED** |
| Mathematical consequence | Fail-closed rules without a defined computation. |
| Required correction | Each becomes $\alpha_t=0$ (no new risk), and the period is outside T-10 for exposure already held (breach logged, HALT); exit side under per-execution fees: F140 with $n/\delta_q$ parts. |
| Test / proof obligation | Accrual, withdrawal and per-execution-fee flags ⇒ NO\_TRADE. |

### AUD-045

*Found by the third independent review (finding 9); reproduced.*

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Document / section | 01 §9 item 3 (at `f37c1b6`) |
| Formula / proposition | Rounding of carried floor references $H_t$, $\nu^{\mathrm{day}}_0$, $\nu^{\mathrm{wk}}_0$, $\nu^{\mathrm{ref}}$ and of $U_t$ |
| Finding | No direction was specified; rounding a reference down lowers the floor. |
| Independent reproduction | $W=10^8$, $U=3\cdot10^6$, $d^{\max}=0.1$: $H$ stored as $33.33$ gives $K=10{,}009{,}000$ instead of $10{,}000{,}000$. |
| Status | **CONFIRMED** |
| Mathematical consequence | A cushion enlarged by rounding. |
| Required correction | References rounded toward $+\infty$ when stored at a scale; $U_t$, $\nu_t$ carried as exact integer pairs (01 §9 item 3; FM-DD-9). |
| Test / proof obligation | Non-terminating $W/U$ test vector. |

### AUD-046

*Found by the third independent review (finding 11); reproduced.*

| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 01 §9 items 5, 12, 13; 08 T-01, T-03; 14 F047 (at `f37c1b6`) |
| Formula / proposition | Treatment of $-0$ |
| Finding | Rejected (item 5), accepted as finite (item 12) and normalised (item 13, T-01, T-03): an OPTIONAL model output $-0$ gives $b^{\mathrm{hard}}$ if rejected and $0$ if normalised. |
| Independent reproduction | `Decimal('-0.00')` parses as a finite value; the two readings give different $b^{\mathrm{allow}}$. |
| Status | **CONFIRMED** |
| Mathematical consequence | Non-deterministic specification (both readings are within the hard cap). |
| Required correction | One rule: $-0$ rejected at the boundary (grammar 17 (a)); an internal $-0$ normalised to $0$; F047 maps finite $y\le0$ to $0$. |
| Test / proof obligation | Boundary and internal $-0$ vectors. |

### AUD-047

*Found by the third independent review (finding 12); reproduced.*

| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 06 §4; 14 F049; 08 T-01 (at `f37c1b6`) |
| Formula / proposition | $0\le b^{\mathrm{allow}}_k\le b^{\mathrm{hard}}_k$ |
| Finding | Impossible when $b^{\mathrm{hard}}_k<0$ (H14 with $C^{\mathrm{res}}>C^{\mathrm{avail}}$); safe through F094's $\{0\}$, but a closed form with truncating division returns a negative quantity. |
| Independent reproduction | H14 budget $-500$ at limit $50$: a closed form $b/p^{\mathrm{lim}}$ with integer division gives $-10$ sh. |
| Status | **CONFIRMED** |
| Mathematical consequence | Invariant unsatisfiable as stated; no unsafe result through F094. |
| Required correction | $b^{\mathrm{allow}}_k=\min((b^{\mathrm{hard}}_k)^+,\mathfrak s(b^{\mathrm{mod}}_k))$ (F049). |
| Test / proof obligation | Negative hard budget ⇒ $Q_k=0$. |

### AUD-048

*Found by the third independent review (finding 13); reproduced.*

| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 04 A-TRIG; 08 T-25 (at `f37c1b6`) |
| Formula / proposition | $\Lambda_{i,t+1}$ inside $\mathrm{XV}$ (F072) |
| Finding | A jump in the model estimate $\hat\Lambda_{t+1}$ alone breaches the floor, with no price move or stop event, but A-TRIG was classed as purely EXECUTION. |
| Independent reproduction | $q=100$, $K_t=110$, $\Lambda_t=1$, price unchanged, $\hat\Lambda_{t+1}=200$ ⇒ $\Delta=-199$, $W_{t+1}=F_t-89$. |
| Status | **CONFIRMED** |
| Mathematical consequence | T-25's attribution correct but its probability has a model component. |
| Required correction | Name the failure in A-TRIG and T-25. |
| Test / proof obligation | Valuation-jump scenario attributed to A-TRIG. |

### AUD-049

*Found by the third independent review (finding 14); reproduced.*

| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 08 T-14, T-03, T-06c; 14 F121 (at `f37c1b6`) |
| Formula / proposition | Cross-references and assumption lists |
| Finding | T-14 cited 01 §9 "item 11 (canonical serialisation)" (item 10); T-03 cited item 14 for float rejection (items 1, 12); F121 listed only A-GAP; T-06c did not state $H_{t+1}=\max(H_t,\nu_{t+1})$. |
| Independent reproduction | T-06c with an intra-period high: $H_t=100$, peak $120$, $\nu_{t+1}=95$ ⇒ $\mathrm{DD}=20.8\%>10\%$. |
| Status | **CONFIRMED** |
| Mathematical consequence | Mis-citations; T-06c needs the epoch-only high-water mark. |
| Required correction | References corrected; F121 lists the common hypotheses; T-06c assumes the epoch high-water mark. |
| Test / proof obligation | Checker cross-reference gate; T-06c counterexample as regression. |

### AUD-050

*Found by the third independent review (finding 15); reproduced by argument.*

| Field | Value |
|---|---|
| Severity | MINOR |
| Document / section | 04 A-AUTH-05; 08 T-11; 14 F144 (at `f37c1b6`) |
| Formula / proposition | "Terminal" order state |
| Finding | Undefined: if a cancel request counted as terminal, a fill racing the cancel after release would be unreserved. |
| Independent reproduction | Sequence: cancel requested → reservation released → fill confirmed: exposure with no reservation. |
| Status | **CONFIRMED** |
| Mathematical consequence | Reservation conservation (T-11) could fail at the integration boundary. |
| Required correction | Terminal = venue-confirmed filled, cancelled, expired or rejected; pending otherwise (F144). |
| Test / proof obligation | Cancel/fill race in the ledger replay tests. |

### AUD-051

*Found during the closure's manual review (after the checker reached zero); a regression of the uncommitted closure draft, never committed.*

| Field | Value |
|---|---|
| Severity | IMPORTANT (a fail-closed rule lost) |
| Document / section | 05 §5 F145 paragraph; 06 G8; 14 F092, F145 (closure draft) |
| Formula / proposition | ANOMALY rule: a negative raw open-risk value ⇒ $\alpha_t=0$ (05 §5, FM-OPS-3) |
| Finding | At `f37c1b6` the held part of a partially filled order was charged $r^{\mathrm{open}}(q)$ (F064), which carries the ANOMALY rule. The closure's F145 replaced that charge and the rule no longer applied: a held part marked far below its stop contributes a negative term that frees budget. |
| Independent reproduction | $q=100$ held at mark $45$, stop $49$, $\kappa^{\mathrm{out}}=0.1$, remainder $100$ at limit $50$: held-part term $100(45-49+0.1)=-390$, remainder $110$, so $r^{\mathrm{pf}}<0$ before fees; under F064 the held part alone ($-390+\phi$) is an ANOMALY. |
| Status | **CONFIRMED** |
| Mathematical consequence | Exact under A-TRIG, but A-TRIG is implausible exactly in this state (mark below a stop); the draft would have credited cushion from it. |
| Required correction | The ANOMALY rule applies to $r^{\mathrm{open}}(q_{i,t})$, $g^{\mathrm{open}}(q_{i,t})$ of the held part and to $r^{\mathrm{pf}},g^{\mathrm{pf}},u^{\mathrm{pf}}$ (05 §5; G8 in 06 and F092). |
| Test / proof obligation | Held part marked below its stop ⇒ NO\_TRADE (G8). |
| Superseded | The sign test introduced here could be masked by a larger estimate or fee and missed a mark just below the stop; it was replaced by the estimate-free mark test of G8 ($m_{i,t}\le p^{\mathrm{stop}}_i$ fails) at the critical closure correction (CLOSURE-REV-001, [09-closure-review-registry.md](09-closure-review-registry.md)). |

## Third independent review of `f37c1b6` — mapping

Every finding was reproduced independently in exact arithmetic (or by argument where stated) before a status was assigned; no reviewer
output was accepted on authority.

| # | Reviewer severity | Finding (short) | Maps to | Status | Assessed severity |
|---|---|---|---|---|---|
| 1 | CRITICAL | T-10 (2′) breach with the stop trailed at or above the limit ($F_t-29$) | AUD-039 | CONFIRMED | CRITICAL |
| 2 | CRITICAL | ADV unbounded; cap invariant misstated ($666$ vs $953$); cluster splitting | AUD-040 | CONFIRMED | CRITICAL |
| 3 | IMPORTANT | F144 quantity ambiguous ($F_t-179$) | AUD-034 (extended) | CONFIRMED (resolved by the closure F144) | IMPORTANT |
| 4 | IMPORTANT | Missing estimate falls back to the permissive bound | AUD-041 | CONFIRMED | IMPORTANT |
| 5 | IMPORTANT | Stopless positions not covered by tier S | AUD-042 | CONFIRMED | IMPORTANT |
| 6 | IMPORTANT | T-19 assumptions missing | AUD-043 | CONFIRMED | IMPORTANT |
| 7 | IMPORTANT | Three fail-closed rules without a formula | AUD-044 | CONFIRMED | IMPORTANT |
| 8 | IMPORTANT | Realised cash and notional counted twice ($5{,}001$) | AUD-034, AUD-038 (extended) | CONFIRMED (resolved by the closure F144, F070) | IMPORTANT |
| 9 | IMPORTANT | Floor-reference rounding ($+9{,}000$) | AUD-045 | CONFIRMED | IMPORTANT |
| 10 | IMPORTANT | Serialisation and parsing gaps | AUD-036 (extended, upgraded) | CONFIRMED | IMPORTANT |
| 11 | MINOR | $-0$ handled three ways | AUD-046 | CONFIRMED | MINOR |
| 12 | MINOR | Negative $b^{\mathrm{hard}}_k$ | AUD-047 | CONFIRMED | MINOR |
| 13 | MINOR | $\hat\Lambda_{t+1}$ jump ($F_t-89$) | AUD-048 | CONFIRMED | MINOR |
| 14 | MINOR | Cross-references, F121, T-06c high-water mark ($20.8\%$) | AUD-049 | CONFIRMED | MINOR |
| 15 | MINOR | "Terminal" undefined | AUD-050 | CONFIRMED | MINOR |
| 16 | MINOR | "$\mu^{K}>1$ admits floor breach" cites T-21 | — | **REJECTED**: "admits" asserts existence, and T-21 (c) with $\Lambda_t=0$ (flat book) exhibits a breaching state for every $\mu^{K}>1$ (choose $K_t$ so that some lattice size has $K_t<L^{\mathrm{stop}}(n)\le\mu^{K}K_t$); the reviewer itself found the wording correct. No change. | — |

## Summary

| Severity | Count | IDs |
|---|---|---|
| CRITICAL | 4 | AUD-001, AUD-002, AUD-039, AUD-040 |
| IMPORTANT | 29 | AUD-003, 004, 006, 007, 008, 010, 011, 012, 013, 014, 015, 016, 017, 018, 019, 028, 029, 031, 032, 033, 034, 036, 037, 041, 042, 043, 044, 045, 051 |
| MINOR | 18 | AUD-005, 009, 020, 021, 022, 023, 024, 025, 026, 027, 030, 035, 038, 046, 047, 048, 049, 050 |

All 51 are CONFIRMED (AUD-031 … AUD-033 were found during correction, AUD-034 … AUD-038 and AUD-051 during Phase-0 closure, AUD-039 … AUD-050
by the third independent review of `f37c1b6` and reproduced here; each is marked). None is REJECTED; one third-review finding was rejected and has no
AUD entry (mapping above). All are addressed in
the correction commit (`f37c1b6`) or the final closure commit, except where the correction is itself a research obligation (AUD-019 independent bibliography re-verification;
AUD-028 definition of SL), which remain explicitly UNRESOLVED with a fail-closed rule or owner.
