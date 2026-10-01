# 04 — Assumption Registry and Decision Register (v0.2-draft)

Status: DRAFT. Status vocabulary per the operating protocol: **CONFIRMED** (evidence-backed) · **PROVISIONAL** (working assumption)
· **OPEN** (unresolved) · **BLOCKED** · **SUPERSEDED**. An assumption that a theorem relies on is never silently strengthened.

v0.2 changes (review corrections): every assumption carries one of the seven classes MATHEMATICAL / MARKET / EXECUTION /
STATISTICAL / NUMERICAL / OPERATIONAL / RESEARCH and a fail-closed check (AUD-016); hidden assumptions registered as A-MATH-01,
A-ACC-06, A-ACC-07, A-MKT-06, A-NUM-03, A-AUTH-04, A-AUTH-05, A-EXE-05, A-EXE-06 (AUD-017, AUD-014, AUD-033); closure: A-AUTH-02 carries the order state, A-AUTH-05 is ledger bookkeeping only (AUD-034); A-TRIG restated as a position-level
exit-value bound (AUD-001); A-EXE-04 stated on cumulative filled quantity (AUD-015); A-MKT-05 extended to partial fills (AUD-017).
IDs are stable: the former type labels are replaced by the class column, no ID is renamed.

"Fail-closed check" states the check and the decision it forces when the assumption cannot be established. Assumptions about the
future (e.g. A-STOP) cannot be checked ex ante: their fail-closed mapping is the next-weaker tier (the tier-G and tier-U constraints
remain in force) plus ex-post detection. "Limit" marks assumptions the pure engine cannot check (stated as a limit, Art. 17).

## Part A — Assumptions

### A.1 MATHEMATICAL

| ID | Statement | Class | Status | Used by | How it can fail | Fail-closed check |
|---|---|---|---|---|---|---|
| A-MATH-01 | Standing conventions of the specification: exact arithmetic in $\mathbb Q$; lattice $\mathbb L=\delta_q\mathbb Z$; $\bar N<\infty$; each hard constraint is $g_k(n)\le b_k$ with $g_k(0)=0$ and existing exposure in $b_k$ (06 §5); every $\max$ is over a finite lattice set | MATHEMATICAL | CONFIRMED (definition) | F001, F024, F094; T-01, T-02, T-03, T-13, T-24 | an implementation departs from the specification (not a failure of the mathematics) | type and bound checks of 01 §9; $n>\bar N$ or non-lattice $n$ ⇒ reject |

### A.2 MARKET

| ID | Statement | Class | Status | Used by | How it can fail | Fail-closed check |
|---|---|---|---|---|---|---|
| A-MKT-01 | Prices are $\ge0$ | MARKET | CONFIRMED (structural for equities) | tier U, H16, T-10 (tier U), T-19 | — | negative price in input ⇒ $\alpha_t=0$ |
| A-MKT-06 | For an admitted instrument: $\mathrm{ADV}_{i,t}>0$; $p^{\min}\le m_{i,t}\le p^{\max}$; quotes not crossed ($p^{\mathrm{bid}}\le p^{\mathrm{ask}}$, $\varsigma>0$) | MARKET | PROVISIONAL (added v0.2) | H12, H13, G10, F031, F032, F087, F088 | stale or zero volume; crossed/locked quotes; penny stocks | G10 and the anomaly check; ADV missing or $\le0$ ⇒ $\alpha_t=0$ |
| A-ACC-04 | $\Lambda_t=\sum_i\Lambda_{i,t}$ (no cross-instrument liquidation interaction) | MARKET | PROVISIONAL (R1) | T-10, F035 | correlated liquidation in stress | limit (stress study RQ-22); no engine check |
| A-GAP | Position-level tier-G exit-value bound: $\mathrm{XV}_i\ge q^{\mathrm{exp}}_ip^{\mathrm{gx}}_i(q^{\mathrm{exp}}_i)-\phi^{\mathrm{sell}}_i(q^{\mathrm{exp}}_i)$ (F072); per-share sufficient form: triggered stops exit at $\ge p^{\mathrm{gx}}=\min((1-\Gamma_i)p^{\mathrm{stop}},p^{\mathrm{stop}}-\kappa^{\mathrm{out}})$ (F060) | MARKET | PROVISIONAL — calibration OPEN; fails beyond stress | tier G, H5, H6, T-10 (tier G) | single-name events (earnings, biotech readouts, fraud) | $\Gamma_i\ge\Gamma^{\min}$ (F111); tier U (H16) if adopted; ex post: breach logged, HALT |
| A-LIQ | Future tradable volume $\ge$ policy fraction of trailing ADV over the exit horizon | MARKET | PROVISIONAL — fails in liquidity collapse | H12, H13, tier L | halts, delistings, market-wide stress | frozen ADV estimator (F111); ex post: breach logged |

### A.3 EXECUTION

| ID | Statement | Class | Status | Used by | How it can fail | Fail-closed check |
|---|---|---|---|---|---|---|
| A-MKT-05 | Every fill of a limit buy — including every partial fill — is at a price $\le p^{\mathrm{lim}}$ | EXECUTION | PROVISIONAL (venue rule; broker error possible; extended to partial fills v0.2) | T-10, T-11, H14, F059 | broker/venue error | limit (external execution reconciliation); every entry carries $p^{\mathrm{lim}}$ (D-05) |
| A-STOP | A triggered protective stop exits at $\ge p^{\mathrm{stop}}-\kappa^{\mathrm{out}}$ per share | EXECUTION | PROVISIONAL — **known to fail** (gaps, halts, LULD pauses, fast markets) | per-share sufficient condition for A-TRIG (F060); T-21 attainability | overnight gaps, news, halts | tier G and U constraints remain; $\kappa^{\mathrm{out}}\ge\kappa^{\min}p^{\mathrm{stop}}$ (F111); ex post: breach logged, HALT |
| A-TRIG | **Position-level exit-value bound (v0.2):** for each exposure $i$ of the period, $\mathrm{XV}_{i,t+1}\ge q^{\mathrm{exp}}_i\big(p^{\mathrm{stop}}_i-\kappa^{\mathrm{out}}_i(q^{\mathrm{exp}}_i)\big)-\phi^{\mathrm{sell}}_i(q^{\mathrm{exp}}_i)$ (F072), with $\kappa^{\mathrm{out}}$ and the fee schedule taken at the $\tau_t$ hard-layer inputs (F111), covering untriggered, fully and partially exited exposures in one inequality ($q^{\mathrm{exp}}$ per S-290, including a held position with a pending remainder). Sufficient: A-STOP, A-STOPLIVE, A-EXE-04, at most $N^{\mathrm{ex}}$ exit orders per exposure with $\phi^{\mathrm{split}}$ (F140) in the hard layer whenever fees are not super-additive, and a remainder at the cut valued no lower than its stop bound | EXECUTION | OPEN (restated v0.2) — trigger reference (last sale / bid / consolidated) **UNDEFINED** | T-10 (tier S), T-20a, T-21, T-25, H1–H4, H10 | quote-based valuation below a trade-triggered stop; slow stop execution; partial exit at the cut with per-order minimum fees (AUD-001: $4{,}888<4{,}889$); one child stop per entry fill ($3$ exit fees, REV-029); a jump of the model estimate $\hat\Lambda_{i,t+1}$ that values a remainder at the cut, with no price move ($q=100$, $K_t=110$, $\hat\Lambda_{t+1}=200$ ⇒ $W_{t+1}=F_t-89$; AUD-048) — the bound has a model-dependent component | the hard layer always uses $\phi^{\mathrm{split}}$ (F140) with the declared $N^{\mathrm{ex}}$; unknown $N^{\mathrm{ex}}$ ⇒ F140 with $n/\delta_q$ parts (every lot a separate execution); ex post: breach logged, HALT |
| A-STOPLIVE | Each entry fill is protected by its stop from the instant of the fill (bracket / one-triggers-other semantics) | EXECUTION | OPEN (added R1) | sufficient condition for A-TRIG on new exposures | stop placed only after the whole order fills | limit (execution-semantics review RQ-21); integration contract |
| A-EXE-01 | Fee functions $\phi$ are non-decreasing with $\phi(0)=0$ | EXECUTION | OPEN — must be verified per schedule version | T-02, T-03, T-11, F140 | tiered/rebate schedules (T-03N counterexample) | schedule-load check on the lattice up to $\bar N$; failure ⇒ monotone envelope F127 or $\alpha_t=0$ |
| A-EXE-02 | $\kappa^{\mathrm{out}},\kappa^{\mathrm{liq}},\iota$ non-decreasing in $n$, non-increasing in ADV, non-decreasing in spread | EXECUTION | OPEN | T-02, T-07, T-08 | fitted non-monotone models | grid check at model load; failure ⇒ policy floor only (F111) |
| A-EXE-03 | Partial fills: $0\le e\le n$, same direction | EXECUTION | PROVISIONAL | T-10, T-11 | over-fills (broker error) | limit (reconciliation) |
| A-EXE-04 | **Per-order fee semantics on cumulative filled quantity, with booking lag (v0.2; booking semantics at the critical closure correction, CLOSURE-REV-003):** the fees over all fills of one order, over its lifetime, are $\le\phi(e)$, $e$ the cumulative filled quantity of that order; they may be booked into $W$ at the fill, later, or after the order is terminal; $\phi^{\mathrm{paid}}_o$ is the part booked into $W_t$ at the cut (F148), so the remaining fees are $\le\phi(e)-\phi^{\mathrm{paid}}_o$ and stay reserved (F144, F145) until booked; if fees are charged per execution, the exit side uses $\phi^{\mathrm{split}}$ with $n/\delta_q$ parts (F140) and the entry side is not covered ($\alpha_t=0$) | EXECUTION | OPEN (reworded v0.2) | T-10, T-11, F059, F140, F145 | per-execution minimum commissions (34/33/33 split pays 3 vs 1); per-execution buy fees ($100$ one-share executions at a \$1 minimum pay \$100 against $\phi^{\mathrm{buy}}(100)=1$) | fee-schedule review (RQ-35); per-execution or undetermined **entry**-fee semantics ⇒ $\alpha_t=0$ (no buy-side split envelope in v0; closure, AUD-044); exit side: F140 with $n/\delta_q$ parts |
| A-EXE-05 | The period contains no orders other than the entry of $a_t$, pending orders carried in the reservation ledger, and protective stop exits | EXECUTION | PROVISIONAL (added v0.2) | T-10, T-20a, T-21 | manual orders, other strategies bypassing the engine | limit (A-AUTH-02 integration contract) |
| A-EXE-06 | Every protective stop triggered in the period is fully executed by the epoch cut $\tau_{t+1}$ (no stop is triggered-but-unexecuted or partially executed at the cut) | EXECUTION | OPEN (added v0.2, AUD-014; widened after REV-026) | T-20a | a stop fills in parts, or has not filled, at the cut | triggered or partially executed stop in the snapshot ⇒ RECOVERY (no new risk) until terminal |

### A.4 STATISTICAL

| ID | Statement | Class | Status | Used by | How it can fail | Fail-closed check |
|---|---|---|---|---|---|---|
| A-STAT-00 | A (unknown) probability law generating markets exists | STATISTICAL | PROVISIONAL (postulate; not testable) | 01 §3.2, F009–F023 | — | none possible; the hard layer does not use it |
| A-STAT-01 | Within a regime, returns/gaps are stationary and weakly dependent (mixing) | STATISTICAL | OPEN — likely violated | bootstrap, DRO radii, EVT, F007 | regime change, structural breaks | model layer only: invalid model output ⇒ $\mathfrak s$ (F047) |
| A-STAT-02 | Light tails (exponential moments) | STATISTICAL | OPEN — **likely false** for single-name equity returns | Wasserstein finite-sample radii (F007) | heavy tails | as A-STAT-01 |
| A-STAT-03 | Uncorrelated increments for $\sqrt h$ volatility scaling | STATISTICAL | OPEN | E-15, F113 | volatility clustering, intraday seasonality | model layer only |

### A.5 NUMERICAL

| ID | Statement | Class | Status | Used by | How it can fail | Fail-closed check |
|---|---|---|---|---|---|---|
| A-NUM-01 | Authority arithmetic exact or conservatively directed | NUMERICAL | PROVISIONAL (design rule) | T-01, T-02, T-03, T-24, F028, F030 | float leakage; mixed exact/float operands | 01 §9 items 12–14 (parser, no mixed types); inexact trap ⇒ NO\_TRADE |
| A-NUM-02 | Magnitudes bounded by $\bar M,\bar N$ | NUMERICAL | PROVISIONAL; values OPEN | 01 §9, F029 | — | out-of-bound input ⇒ reject |
| A-NUM-03 | In T-22: $R$ and $\ell$ are positive normal binary64 numbers, the exact quotient is below $2^{53}$, no overflow or underflow occurs | NUMERICAL | PROVISIONAL (added v0.2) | T-22, F115, F116 | subnormal or huge operands | the specification uses exact arithmetic (A-NUM-01); T-22 applies only to a float cross-check |

### A.6 OPERATIONAL

| ID | Statement | Class | Status | Used by | How it can fail | Fail-closed check |
|---|---|---|---|---|---|---|
| A-SCOPE-01 | Single base currency USD | OPERATIONAL | PROVISIONAL (D-07) | all | multi-currency accounts | schema rejects non-USD |
| A-SCOPE-02 | Instruments: US-listed common stock and ETFs | OPERATIONAL | PROVISIONAL (D-03) | 06 | leveraged/inverse ETFs, OTC | universe filter G10 |
| A-SCOPE-03 | Long-only in v0 | OPERATIONAL | OPEN (D-01) | T-10 tier U, T-19, 06 | — | G9 |
| A-SCOPE-04 | Cash account; no margin, no leverage ($\lambda^{\mathrm{gross}}\le1$) | OPERATIONAL | OPEN (D-02) | H11, H14, T-19 | — | policy box F109 |
| A-SCOPE-05 | One exposure per instrument: no new order on $i$ while $q_{i,t}\ne0$ or $Q^{\mathrm{res}}_{i,t}\ne0$ | OPERATIONAL | OPEN (D-12; added R1) | T-10, T-21, T-25 | add-ons: super-additive exit costs break per-lot risk (T-10N) | gate G11 |
| A-ACC-01 | All money in one currency; exact decimal ledger | OPERATIONAL | PROVISIONAL | 05 | — | schema |
| A-ACC-02 | A period containing a corporate action is split at $\tau^{\mathrm{CA}}$; value-neutral restatement of $(q,m,p^{\mathrm{stop}})$ (F054); cash parts booked to $\mathrm{Inc}$ | OPERATIONAL | PROVISIONAL (revised R1) | 05 §1–§2 | CA between decision and fill; special dividends; spin-offs | unknown CA type in period ⇒ $\alpha_t=0$ |
| A-ACC-03 | Every fill, fee, income, charge, flow reported exactly once in the authoritative ledger | OPERATIONAL | PROVISIONAL | T-15 | duplicate/missing execution reports | limit (external reconciliation) |
| A-ACC-07 | Within a period: $\mathrm{Fin}_{t+1}=0$, $\mathrm{Accr}_{t+1}=0$, $\mathrm{Inc}_{t+1}\ge0$ | OPERATIONAL | PROVISIONAL (added v0.2; $\mathrm{Fin}=0$ follows from D-02) | T-10, T-20a, T-21 | platform or regulatory accruals inside a period (with $K_t=r^{\mathrm{open}}=110$ and an accrual of $5$: $W_{t+1}=F_t-5$) | a known, possible or unknown accrual in the period ⇒ $\alpha_t=0$; exposure already held is then outside T-10 for that period (breach logged, HALT). $\bar A_{t+1}$ enters only the log-domain bound F070 (T-19), not $K_t$ (closure, AUD-044) |
| A-AUTH-01 | $\mathsf S_t$ is a consistent cut produced by the authority boundary; the engine cannot detect a wrong-but-consistent snapshot | OPERATIONAL | PROVISIONAL | all | upstream defects | limit (stated, Art. 17) |
| A-AUTH-02 | Reservation ledger in $\mathsf S_t$ is complete for the account scope (all strategies), including for every pending order its quantity, limit, current stop, cumulative filled quantity and fees booked ($\phi^{\mathrm{paid}}_o$, F148), and every venue-confirmed terminal entry order whose fees are not yet confirmed final, with the same fee state | OPERATIONAL | PROVISIONAL (order state added at closure) | T-10, T-11, F144, F145 | a strategy bypasses the ledger; order state missing | limit (integration contract; idempotency obligation 05 §4b); a pending order without filled quantity or fees paid ⇒ $\alpha_t=0$ |
| A-AUTH-03 | Decisions are applied only against the snapshot/ledger version they were computed from (CAS) | OPERATIONAL | PROVISIONAL | T-11 | stale-decision reuse | limit (integration contract) |
| A-AUTH-04 | Positions, marks, cash and the reservation ledger in $\mathsf S_t$ refer to one cut (one version) | OPERATIONAL | PROVISIONAL (added v0.2) | T-10, T-11, T-21 | ledger read at a different instant than positions | version mismatch in $\mathsf S_t$ ⇒ $\alpha_t=0$ |
| A-AUTH-05 | The reservation ledger holds each order's full reservation vector (F108) until the order is terminal — **terminal = venue-confirmed** filled, cancelled, expired or rejected; a cancel request is not terminal, since a fill can race it (AUD-050); releases occur only then, by $L^{\mathrm{stop}}(n)-L^{\mathrm{stop}}(e)$ (T-11 (d)) | OPERATIONAL | PROVISIONAL (added v0.2, AUD-033; closure: ledger bookkeeping only) | T-11 | ledger releases the filled part early and its available budget is then overstated | ledger-side check (integration contract); engine budgets do not read ledger reservation values — they re-evaluate from the order state (F144, F145) |
| A-TIME-01 | $\tau_t$ from the authority clock; monotone; exchange calendar versioned | OPERATIONAL | PROVISIONAL | TTL, F041, F045 | clock skew, DST, half-days | non-monotone clock ⇒ $\alpha_t=0$ |
| A-SET-01 | Settlement lag for US equities is T+1 (SEC rule effective 28 May 2024) | OPERATIONAL | PROVISIONAL — verify at integration | $C^{\mathrm{avail}}$, H14 | rule change | primary-source check (RQ-20) |
| A-FLOW-01 | External flows recorded authoritatively with timestamps; floor theorems additionally require $X_{t+1}=0$ inside a period (flows at epoch boundaries only) | OPERATIONAL | PROVISIONAL | unitisation, T-10, T-19 | withdrawal inside a period breaches $F^{\mathrm{abs}}$ | a pending or possible withdrawal inside the period ⇒ $\alpha_t=0$; exposure already held is then outside T-10 for that period (closure, AUD-044; no formula charges a withdrawal against $K_t$) |
| A-NLA | No-look-ahead admission rule (F003) | OPERATIONAL | PROVISIONAL — requires bitemporal data | Art. 9, all research | vendor restatements, survivorship | knowledge-time audit; missing $t^{\mathrm{know}}$ ⇒ datum rejected |

### A.7 RESEARCH

| ID | Statement | Class | Status | Used by | How it can fail | Fail-closed check |
|---|---|---|---|---|---|---|
| A-ACC-05 | Liquidation value never below minus exit fees: $\Lambda_i\le q_im_i+\phi^{\mathrm{sell}}_{i,0}(q_i)$; position level: $\mathrm{XV}_i\ge-\phi^{\mathrm{sell}}_{i,0}(q^{\mathrm{exp}}_i)$ (F072 tier U) | RESEARCH | PROVISIONAL (R1) | T-10 tier U and tier S case (1′) (positions without a stop, D-06; AUD-042), T-19, F070 | ill-specified $\Lambda$ model | check at model load; consistency with F111 (05 §1) else $\alpha_t=0$ |
| A-ACC-06 | $\Lambda_{i,t}=q_{i,t}\kappa^{\mathrm{liq}}_i(q_{i,t})+\phi^{\mathrm{sell}}_i(q_{i,t})\ge\Lambda^{\mathrm{floor}}_{i,t}\ge0$ (F035, F111): $\Lambda$ includes the exit fee | RESEARCH | PROVISIONAL (added v0.2; model RQ-05) | T-07, T-10, OC-1 | model omits fees or impact | hard layer uses $\max(\Lambda^{\mathrm{floor}},\hat\Lambda)$ (F111) |

## Part B — Decision Register (human authority required)

Each decision is the human controller's (Art. 16). Recommendations are given only where a mathematical reason supports them.

| ID | Decision | Options | Recommendation and mathematical reason | Consequence if deferred |
|---|---|---|---|---|
| D-01 | Direction scope for v0 | long-only / long+short | **Long-only.** Only for longs does a structural loss bound exist ($L^{\mathrm{abs}}=n\,p^{\mathrm{lim}}+$fees; tier U, T-19); short loss is unbounded and adds borrow/recall/dividend liabilities | tier U, T-19 and H16 undefined |
| D-02 | Account semantics for v0 | cash / margin | **Cash account, $\lambda^{\mathrm{gross}}\le1$.** Removes $\mathrm{IM}/\mathrm{MM}$ (broker-defined, not derivable without inventing authority) and keeps $W_{t+1}\ge0$ | H15 undefined; buying-power semantics ambiguous |
| D-03 | Instrument universe for v0 | as below | US-listed common stock + unlevered ETFs; exclude OTC, leveraged/inverse ETFs, instruments below a price floor (value **UNDEFINED**) — leveraged ETFs have path-dependent NAV and larger gap profiles | universe filter undefined |
| D-04 | Quantity lattice | whole / fractional | **Whole shares ($\delta_q=1$ sh).** Whether protective stops can be attached to fractional quantities is unverified; fractional parts would be tier U only | lattice undefined |
| D-05 | Entry order semantics | limit-bounded / market | **Every entry carries $p^{\mathrm{lim}}$** (marketable limit allowed). Required by H14 and T-11: market orders have no deterministic price bound | buying-power and reservation dominance unprovable |
| D-06 | Positions without an authoritative stop | abs-risk / reject | **Charge tier-U risk $u^{\mathrm{open}}$** (UNKNOWN ≠ ZERO); never zero | open-risk aggregates undefined |
| D-07 | Base currency | USD | USD (single) | — |
| D-08 | Adopt unconditional-floor constraint H16 | yes / no / reporting-only | No recommendation — it is the only floor guarantee independent of stop execution, but binds deployment to $\le K_t$ long notional | tier U floor not guaranteed |
| D-09 | Holding-horizon classes | intraday-only / overnight / multi-day | No recommendation — determines whether overnight gaps enter $\Gamma_i$; strategy-dependent | $\Gamma_i$ uncalibratable |
| D-10 | Is certified advantage a hard gate for TRADE? | required / advisory | Required for eventual integration (Phase 10 intent); **advisory** while the hard layer is researched in isolation — otherwise every decision is NO\_TRADE (01 §1, 06 §10 step 11) | ambiguity in what $Q^{\mathrm{fin}}$ means |
| D-11 | Authority of this constitution | adopt v0.2 as the reviewed Phase-0 baseline / revise | — | all downstream work provisional |
| D-12 | One exposure per instrument in v0 (no scaling in) | yes / no | **Yes.** Exit costs are super-additive in quantity, so per-lot risk under-states an add-on (T-10N counterexample: floor breached by 8); the incremental formula F068 is not yet proved with pending orders (RQ-34) | T-10 unproved for add-ons |

## Part C — Class summary

| Class | IDs | Count |
|---|---|---|
| MATHEMATICAL | A-MATH-01 | 1 |
| MARKET | A-MKT-01, A-MKT-06, A-ACC-04, A-GAP, A-LIQ | 5 |
| EXECUTION | A-MKT-05, A-STOP, A-TRIG, A-STOPLIVE, A-EXE-01, A-EXE-02, A-EXE-03, A-EXE-04, A-EXE-05, A-EXE-06 | 10 |
| STATISTICAL | A-STAT-00, A-STAT-01, A-STAT-02, A-STAT-03 | 4 |
| NUMERICAL | A-NUM-01, A-NUM-02, A-NUM-03 | 3 |
| OPERATIONAL | A-SCOPE-01…05, A-ACC-01, A-ACC-02, A-ACC-03, A-ACC-07, A-AUTH-01…05, A-TIME-01, A-SET-01, A-FLOW-01, A-NLA | 18 |
| RESEARCH | A-ACC-05, A-ACC-06 | 2 |

Total 43. Every assumption has a fail-closed check or is marked "limit" with the owner of the check.
