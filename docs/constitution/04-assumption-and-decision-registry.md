# 04 — Assumption Registry and Decision Register (v0.1.1-draft)

Status: DRAFT. Status vocabulary per the operating protocol: **CONFIRMED** (evidence-backed) · **PROVISIONAL** (working assumption)
· **OPEN** (unresolved) · **BLOCKED** · **SUPERSEDED**. An assumption that a theorem relies on is never silently strengthened.

## Part A — Assumptions

| ID | Statement | Type | Status | Used by | How it can fail | Test / falsification |
|---|---|---|---|---|---|---|
| A-SCOPE-01 | Single base currency USD | scope | PROVISIONAL (D-07) | all | FX exposure via ADRs/foreign ETFs' NAV is still USD-quoted — acceptable; multi-currency accounts not | schema rejects non-USD |
| A-SCOPE-02 | Instruments: US-listed common stock and ETFs | scope | PROVISIONAL (D-03) | 06 | leveraged/inverse ETFs, OTC | universe filter |
| A-SCOPE-03 | Long-only in v0 | scope | OPEN (D-01) | T-10 tier U, T-19, 06 | — | G9 |
| A-SCOPE-04 | Cash account; no margin, no leverage ($\lambda^{\mathrm{gross}}\le1$) | scope | OPEN (D-02) | H11, H14, T-19 | — | policy box |
| A-SCOPE-05 | One exposure per instrument: no new order on $i$ while $q_{i,t}\ne0$ or $Q^{\mathrm{res}}_{i,t}\ne0$ | scope | OPEN (D-12; added R1) | T-10, T-21, T-25 | add-ons: super-additive exit costs break per-lot risk (08 T-10) | gate G11 |
| A-ACC-01 | All money in one currency; exact decimal ledger | accounting | PROVISIONAL | 05 | — | schema |
| A-ACC-02 | A period containing a corporate action is split at $\tau^{\mathrm{CA}}$; value-neutral restatement of $(q,m,p^{\mathrm{stop}})$; cash parts booked to Inc | accounting | PROVISIONAL (revised R1) | 05 §1–§2 | CA between decision and fill; special dividends; spin-offs | reconciliation tests (external) |
| A-ACC-04 | $\Lambda_t=\sum_i\Lambda_{i,t}$ (no cross-instrument liquidation interaction) | accounting/model | PROVISIONAL (R1) | T-10 | correlated liquidation in stress | stress study (RQ-22) |
| A-ACC-05 | Liquidation value never below minus exit fees: $\Lambda_i\le q_im_i+\phi^{\mathrm{sell}}_{i,0}(q_i)$ | model | PROVISIONAL (R1) | T-10 tier U, T-19 | ill-specified $\Lambda$ model | check at model load |
| A-ACC-03 | Every fill, fee, income, charge, flow reported exactly once in the authoritative ledger | accounting | PROVISIONAL | T-15 | duplicate/missing execution reports | external reconciliation (outside engine) |
| A-AUTH-01 | $\mathsf S_t$ is a consistent cut produced by the authority boundary; the engine cannot detect a wrong-but-consistent snapshot | authority | PROVISIONAL | all | upstream defects | out of engine scope; stated as a limit |
| A-AUTH-02 | Reservation ledger in $\mathsf S_t$ is complete for the account scope (all strategies) | authority | PROVISIONAL | T-10, T-11 | a strategy bypasses the ledger | integration contract |
| A-AUTH-03 | Decisions are applied only against the snapshot/ledger version they were computed from (CAS) | authority | PROVISIONAL | T-11(b) | stale-decision reuse | integration contract |
| A-MKT-01 | Prices are $\ge0$ | market | CONFIRMED (structural for equities) | tier U, T-19 | — | — |
| A-MKT-05 | A limit buy never fills above its limit | market/operational | PROVISIONAL (regulatory/venue rule; broker error possible) | T-10, T-11(c), H14 | broker/venue error | execution reconciliation (external) |
| A-STOP | A triggered protective stop exits at $\ge p^{\mathrm{stop}}-\kappa^{\mathrm{out}}$ per share | market/execution | PROVISIONAL — **known to fail** (gaps, halts, LULD pauses, fast markets) | tier S, T-10, T-21 | overnight gaps, news, halts | empirical stop-slippage study (RQ-05) |
| A-TRIG | Every quantity still held at $\tau_{t+1}$ — untriggered, **or triggered but not fully filled** — has liquidation value $\ge q(p^{\mathrm{stop}}-\kappa^{\mathrm{out}}(q))-\phi^{\mathrm{sell}}(q)$ | market/model | OPEN (broadened R1) — trigger reference (last sale / bid / consolidated) **UNDEFINED** | T-10 | quote-based valuation below a trade-triggered stop; slow stop execution | RQ-21 |
| A-STOPLIVE | Each entry fill is protected by its stop from the instant of the fill (bracket / one-triggers-other semantics) | execution | OPEN (added R1) | T-10 | stop placed only after the whole order fills | execution-semantics review (RQ-21) |
| A-GAP | Triggered stops exit at $\ge(1-\Gamma_i)p^{\mathrm{stop}}$ | market/stress | PROVISIONAL — calibration OPEN; fails beyond stress | tier G, T-10 | single-name events (earnings, biotech readouts, fraud) | EVT study of gap-through-stop (RQ-04) |
| A-LIQ | Future tradable volume $\ge$ policy fraction of trailing ADV over the exit horizon | market/proxy | PROVISIONAL — fails in liquidity collapse | H12, H13 | halts, delistings, market-wide stress | liquidity-drought study (RQ-06) |
| A-EXE-01 | Fee functions $\phi$ are non-decreasing with $\phi(0)=0$ | execution | OPEN — must be verified per schedule version | T-02, T-03, T-11 | tiered/rebate schedules (T-03 counterexample) | schedule-load check; monotone envelope |
| A-EXE-02 | $\kappa^{\mathrm{out}},\kappa^{\mathrm{liq}},\iota$ non-decreasing in $n$, non-increasing in ADV, non-decreasing in spread | model | OPEN | T-02, T-07 | fitted non-monotone models | grid check at model load |
| A-EXE-03 | Partial fills: $0\le e\le n$, same direction | execution | PROVISIONAL | T-10, T-11 | over-fills (broker error) | reconciliation |
| A-EXE-04 | Fees over all fills of one order of total quantity $n$ are $\le\phi(n)$ (per-order fee semantics); otherwise $\phi$ must be replaced by its worst case over splits | execution | OPEN (added R1) | T-10, T-11 | per-execution minimum commissions (34/33/33 split pays 3 vs 1) | fee-schedule review (RQ-35) |
| A-STAT-00 | A (unknown) probability law generating markets exists | modelling | PROVISIONAL (postulate; not testable) | 01 §3.2 | — | — |
| A-STAT-01 | Within a regime, returns/gaps are stationary and weakly dependent (mixing) | statistical | OPEN — likely violated | bootstrap, DRO radii, EVT | regime change, structural breaks | stationarity/break tests on training data only |
| A-STAT-02 | Light tails (exponential moments) | statistical | OPEN — **likely false** for single-name equity returns | Wasserstein finite-sample radii | heavy tails | tail-index estimation |
| A-STAT-03 | Uncorrelated increments for $\sqrt h$ volatility scaling | statistical | OPEN | E-15 | volatility clustering, intraday seasonality | variance-ratio tests |
| A-NLA | No-look-ahead admission rule (NLA, 01 §3.2) | data | PROVISIONAL — requires bitemporal data | Art. 9, all research | vendor restatements, survivorship | knowledge-time audit |
| A-NUM-01 | Authority arithmetic exact or conservatively directed | numerical | PROVISIONAL (design rule) | T-01..T-03, T-24 | float leakage | type checks; differential tests |
| A-NUM-02 | Magnitudes bounded by $\bar M,\bar N$ | numerical | PROVISIONAL; values OPEN | 01 §9 | — | boundary tests |
| A-TIME-01 | $\tau_t$ from the authority clock; monotone; exchange calendar versioned | time | PROVISIONAL | TTL, day/week floors | clock skew, DST, half-days | calendar tests |
| A-SET-01 | Settlement lag for US equities is T+1 (SEC rule effective 28 May 2024) | regulatory | PROVISIONAL — verify at integration | $C^{\mathrm{avail}}$ | rule change | primary-source check (RQ-20) |
| A-FLOW-01 | External flows recorded authoritatively with timestamps; floor theorems additionally require $X_{t+1}=0$ inside a period (flows at epoch boundaries only) | accounting | PROVISIONAL | unitisation, T-10, T-19 | withdrawal inside a period breaches $F^{\mathrm{abs}}$ | reconciliation |

## Part B — Decision Register (human authority required)

Each decision is the human controller's (Art. 16). Recommendations are given only where a mathematical reason supports them.

| ID | Decision | Options | Recommendation and mathematical reason | Consequence if deferred |
|---|---|---|---|---|
| D-01 | Direction scope for v0 | long-only / long+short | **Long-only.** Only for longs does a structural loss bound exist ($L^{\mathrm{abs}}=n\,p^{\mathrm{lim}}+$fees; tier U, T-19); short loss is unbounded and adds borrow/recall/dividend liabilities | tier U, T-19 and H16 undefined |
| D-02 | Account semantics for v0 | cash / margin | **Cash account, $\lambda^{\mathrm{gross}}\le1$.** Removes $IM/MM$ (broker-defined, not derivable without inventing authority) and keeps $W_{t+1}\ge0$ | H15 undefined; buying-power semantics ambiguous |
| D-03 | Instrument universe for v0 | as below | US-listed common stock + unlevered ETFs; exclude OTC, leveraged/inverse ETFs, instruments below a price floor (value **UNDEFINED**) — leveraged ETFs have path-dependent NAV and larger gap profiles | universe filter undefined |
| D-04 | Quantity lattice | whole / fractional | **Whole shares ($\delta_q=1$).** Whether protective stops can be attached to fractional quantities is unverified; fractional parts would be tier U only | lattice undefined |
| D-05 | Entry order semantics | limit-bounded / market | **Every entry carries $p^{\mathrm{lim}}$** (marketable limit allowed). Required by H14 and T-11(c): market orders have no deterministic price bound | buying-power and reservation dominance unprovable |
| D-06 | Positions without an authoritative stop | abs-risk / reject | **Charge tier-U risk $u^{\mathrm{open}}$** (UNKNOWN ≠ ZERO); never zero | open-risk aggregates undefined |
| D-07 | Base currency | USD | USD (single) | — |
| D-08 | Adopt unconditional-floor constraint H16 | yes / no / reporting-only | No recommendation — it is the only floor guarantee independent of stop execution, but binds deployment to $\le K_t$ long notional | tier U floor not guaranteed |
| D-09 | Holding-horizon classes | intraday-only / overnight / multi-day | No recommendation — determines whether overnight gaps enter $\Gamma_i$; strategy-dependent | $\Gamma_i$ uncalibratable |
| D-10 | Is certified advantage a hard gate for TRADE? | required / advisory | Required for eventual integration (Phase 10 intent); **advisory** while the hard layer is researched in isolation — otherwise every v0.1 decision is NO\_TRADE (01 §1, 06 §10 step 10) | ambiguity in what $Q^{\mathrm{fin}}$ means |
| D-11 | Authority of this constitution | adopt v0.1.1 as baseline for review / revise | — | all downstream work provisional |
| D-12 | One exposure per instrument in v0 (no scaling in) | yes / no | **Yes.** Exit costs are super-additive in quantity, so per-lot risk under-states an add-on (08 T-10 counterexample: floor breached by 8); the incremental formula is not yet proved with pending orders (RQ-34) | T-10 unproved for add-ons |
