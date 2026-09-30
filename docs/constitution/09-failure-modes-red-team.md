# 09 — Known Mathematical Failure Modes and Red-Team Classification (v0.2-draft)

Classification vocabulary (per brief): **PROVED · DISPROVED · COUNTEREXAMPLE FOUND · REQUIRES ADDITIONAL ASSUMPTION · UNDEFINED ·
NOT YET PROVEN.** "Observed" = reproduced numerically in this session.

## Part A — Formula-level classification

v0.2 (AUD-021): the former IDs F-01 … F-36 collided with the formula-registry namespace and are re-keyed one-to-one to RT-01 … RT-36;
each row points to the formula ID(s) in [14](14-formula-registry.md). Vocabulary mapping to the theorem register (08): COUNTEREXAMPLE
FOUND = the unrestricted claim is DISPROVED; REQUIRES ADDITIONAL ASSUMPTION = PROOF REQUIRES ADDITIONAL ASSUMPTIONS.

| ID | Formula / object | Formula ID | Classification | Evidence |
|---|---|---|---|---|
| RT-01 | $R_{\mathrm{hard}}=E_tf^{\mathrm{trd}}$ as a sufficient hard envelope | F110 | **DISPROVED** | 06 §3 (ten defects); T-17a |
| RT-02 | $R^{\mathrm{hard}}_t$ — computation | F074 | **PROVED** ($\ge0$, finite, monotone: T-01, T-05) | 08 |
| RT-03 | $R^{\mathrm{hard}}_t$ — protective meaning | F074, F120 | **REQUIRES ADDITIONAL ASSUMPTION** (A-TRIG position level) | T-10, T-25 |
| RT-04 | $Q=\delta_q\lfloor R/(\delta_q\ell)\rfloor$ | F095 | **PROVED** for linear $g$ in exact arithmetic; **COUNTEREXAMPLE FOUND** for min-commission fees, half-up, binary64 (observed); the lattice-free form $\lfloor R/\ell\rfloor$ is dimensionally invalid unless $\delta_q=1$ sh (FM-DIM-1) | T-02, T-02N, T-22, T-22N |
| RT-05 | $Q^{\mathrm{hard}}=\min_kQ_k$ and $\lfloor\min_ky_k\rfloor_{\mathbb L}=\min_k\lfloor y_k\rfloor_{\mathbb L}$ | F096, F097 | **PROVED** under monotone constraints; **COUNTEREXAMPLE FOUND** for non-monotone constraints | T-03, T-03N |
| RT-06 | $L^{\mathrm{stop}}(n)$ as a loss bound | F061 | **REQUIRES ADDITIONAL ASSUMPTION** (A-TRIG, A-MKT-05, A-EXE-04) | T-10 |
| RT-07 | $L^{\mathrm{gap}}(n)$ | F062 | **REQUIRES ADDITIONAL ASSUMPTION** (A-GAP); $\Gamma_i$ beyond $\Gamma^{\min}$ **UNDEFINED** | RQ-04 |
| RT-08 | $L^{\mathrm{abs}}(n)$ (long) | F063 | **PROVED** under A-MKT-01, A-MKT-05, A-ACC-05; short analogue **UNDEFINED** (unbounded) | 05 §5 |
| RT-09 | $W=E-\Lambda$ | F034, F035 | **UNDEFINED** until $\Lambda$ is specified beyond its floor F111 | RQ-05 |
| RT-10 | Wealth transition $G$ | F055 | **PROVED** (identity) under A-ACC-01..03 | 05 §2 |
| RT-11 | ECAI | F058 | **PROVED**; ex-post impact/slippage split **UNDEFINED** (not identifiable) | 05 §3 |
| RT-12 | $\mathrm{DD}=1-\nu/H$ | F038 | **PROVED** well-defined iff $H>0$ (requires $\nu_0>0$); $\mathrm{DD}\ge1\iff\nu\le0$ | 02 S-102 |
| RT-13 | Cushion-induced throttle $\vartheta_K$ | F098 | **PROVED** continuous, monotone, zero at $d^{\max}$ | 06 §7, T-05 |
| RT-14 | Step throttle | F103 | **PROVED** discontinuous (unbounded sensitivity at thresholds) — admissible only below the cushion line | 06 §7 |
| RT-15 | Exponential throttle as floor mechanism | F105 | **DISPROVED** (never reaches zero) | 06 §7 |
| RT-16 | "MDD ≤ $d^{\max}$" from shutdown alone | F039 | **DISPROVED** | T-06b |
| RT-17 | Kelly $f^{\mathrm{K}}=P^{\mathrm{win}}-(1-P^{\mathrm{win}})/b^{\mathrm{K}}$ with estimated inputs | F131 | **COUNTEREXAMPLE FOUND**: $\hat P^{\mathrm{win}}=1$ from a short all-win sample gives $f^{\mathrm{K}}=1$ (all wealth at risk); **UNDEFINED** under estimation error without a robust formulation | FM-STAT-3 |
| RT-18 | $\mathbb E[\log(W_{t+1}/W_t)]$ | F019, F070 | **REQUIRES ADDITIONAL ASSUMPTION** ($W^{\min}_{t+1}>0$) | T-19 |
| RT-19 | Wasserstein-DRO log growth | F007, F022 | **REQUIRES ADDITIONAL ASSUMPTION** (support restriction; radius justification under heavy tails/dependence — A-STAT-01/02 likely false) | T-19, 01 §4 |
| RT-20 | KL/φ-divergence ES as tail model | F010 | **COUNTEREXAMPLE FOUND** (cannot exceed worst observed outcome) | FM-TAIL-2 |
| RT-21 | VaR as aggregatable budget | F009 | **DISPROVED** (non-subadditive) | T-26 |
| RT-22 | $\mathrm{ES}_\beta$ as optimisable measure | F010, F011 | coherence is a standard literature result (Acerbi & Tasche 2002) — **not re-proved in this register**; high-$\beta$ estimator **UNDEFINED** | 01 §5 |
| RT-23 | Nested CVaR for multi-period | F010 | **NOT YET PROVEN** appropriate (conservatism compounding) | RQ-23 |
| RT-24 | CVaR surrogate of the floor chance constraint | F016 | **PROVED** conservative: $\mathrm{ES}_{1-\epsilon^{\mathrm{ruin}}}(F_t-W_{t+1})\le0\Rightarrow\mathrm{PB}_t\le\epsilon^{\mathrm{ruin}}$ (VaR ≤ ES); needs a law ⇒ model layer only | 01 §5 |
| RT-25 | Correlation-adjusted risk multiplier $1/\sqrt{1+(n^{\mathrm{pos}}-1)\hat{\bar\rho}}$ | F132 | **COUNTEREXAMPLE FOUND** ($\hat{\bar\rho}<0$ ⇒ multiplier $>1$ enlarges budget; calm-regime estimates understate crash correlation) | FM-COR-1, T-18 |
| RT-26 | Robust advantage as difference of infima | F117 | **COUNTEREXAMPLE FOUND** | T-12a |
| RT-27 | Additive error allowance in the advantage test | F118 | **PROVED** for deterministic bounds; **REQUIRES ADDITIONAL ASSUMPTION** for statistical bounds (confidence, union bound); **UNDEFINED** for misspecification | T-12b |
| RT-28 | Volatility-targeted size, notional $=W_t\sigma^{\mathrm{target}}/\hat\sigma_i$ | F133 | **COUNTEREXAMPLE FOUND**: $\hat\sigma_i=0$ (halted or stale flat series) ⇒ division by zero / unbounded size; the v0.1 form "risk fraction × $W/\hat\sigma$" is dimensionally invalid (FM-DIM-2, 03 E-19) | FM-NUM-6 |
| RT-29 | Buying-power cap with market orders | F089 | **UNDEFINED** (no price bound) | D-05 |
| RT-30 | Gambler's-ruin closed forms for PoR | F014 | **UNDEFINED** in this architecture (assume i.i.d. fixed bets; sizing here is state-dependent) — replaced by T-25 decomposition | 01 §5 |
| RT-31 | Argmax-defined model sizing monotone in ambiguity | F017 | **COUNTEREXAMPLE FOUND** | T-09N |
| RT-32 | Floor invariance under hold with ratcheting floor | F124 | **DISPROVED** | T-20b |
| RT-33 | Binary64 floor of the lattice count | F115, F116 | **PROVED** safe under the T-22 condition (F116); **COUNTEREXAMPLE FOUND** outside it (observed) | T-22, T-22N |
| RT-34 | Greedy sequential allocation | F096 | **PROVED** order-dependent | T-23 |
| RT-35 | Open risk with $\Lambda$ credit (v0.1 DC-5); tolerance in a hard check | F064, F030 | **COUNTEREXAMPLE FOUND** (budgets rise as liquidity worsens; a tolerance enlarges the cap) — replaced by OC-1 and exact comparison | T-07 |
| RT-36 | Per-lot risk for add-ons, $r^{\mathrm{open}}(q)+L^{\mathrm{stop}}(n)$ | F064, F061, F068 | **COUNTEREXAMPLE FOUND** (super-additive exit costs) — G11 | T-10N |

## Part B — Failure-mode catalogue

### Numerical (FM-NUM)

| ID | Failure | Trigger | Effect | Mitigation | Status |
|---|---|---|---|---|---|
| FM-NUM-1 | NaN ordering in `min` | model output NaN | budget = NaN or silently = hard (order-dependent) | sanitiser; exact types | observed |
| FM-NUM-2 | IEEE minNum/maxNum drop NaN (`Decimal.min/max`) | REQUIRED model fails | "unknown" becomes "no limit" | forbid these methods | observed |
| FM-NUM-3 | Half-up rounding overshoot | $b/\ell$ fractional part $\ge0.5$ | budget exceeded ($1000.50>1000$) | floor to lattice | observed |
| FM-NUM-4 | Binary64 floor overshoot | high-resolution or huge inputs | one share over cap | exact arithmetic; T-22 | observed |
| FM-NUM-5 | Catastrophic cancellation in $p^{\mathrm{lim}}-p^{\mathrm{stop}}$ | float prices | `100.07-99.97 = 0.09999999999999432` (observed) — stop distance understated ⇒ quantity overstated | exact decimals | observed |
| FM-NUM-6 | Division by zero | $\ell=0$, $\hat\sigma=0$, $H=0$, $\mathrm{ADV}=0$ | unbounded size / exception | gates G7; domain checks; Decimal DivisionByZero trapped (observed default) | known |
| FM-NUM-7 | Silent precision loss | 28-digit default context, large products | rounding in unknown direction (half-even) | trap `Inexact` on exact paths; precision sizing | observed |
| FM-NUM-8 | $\log 0$ / $\log$ of negative | full investment, gaps to zero, leverage | $-\infty$ (`Decimal(0).ln()` silent, observed) or exception | T-19 domain gate | observed |
| FM-NUM-9 | Solver tolerance | constraint satisfied to $10^{-6}$ | exact cap violated | exact post-verification (T-03, F126) | known |
| FM-NUM-10 | Global numeric context mutation | other code changes default precision/rounding | non-reproducible results | local contexts only | known |
| FM-NUM-11 | Hash-seed-dependent iteration | iterating a set of strings | order-dependent sums/allocations | sorted iteration | known |
| FM-NUM-12 | Float-typed input parsed as authority | `Decimal(0.1)` from a float | value ≠ intended decimal | reject float type at boundary | observed |
| FM-NUM-13 | Special values admitted by the parser | default JSON parser accepts `NaN`, `Infinity` and overflows `1e400` to `inf` (review J01–J03) | "reject NaN at the boundary" is bypassed at parse time | strict parser: numbers parsed as exact decimals, special tokens rejected (01 §9 item 12) | observed |
| FM-NUM-14 | Negative zero produced internally | `Decimal('-0')*5` gives `-0`; quantised `-0.00` serialises differently from `0.00` (Z03, Z05, Z06) | evidence hashes differ for equal values; boundary rejection alone is insufficient | normalise $-0\to0$ before quantisation and serialisation (01 §9 item 13) | observed |
| FM-NUM-15 | Mixed exact/float arithmetic | `Fraction(1,10)+0.2` returns a float (X01) | exactness silently lost | forbid mixed-type operands on the authority path (01 §9 item 14) | observed |
| FM-NUM-16 | Half-cent quantisation in the wrong direction | limit price or fee exactly at a half cent (HC01–HC04) | half-even removes a fee; a limit price rounded down understates worst-case entry | directed quantisation: fees and limit prices up, budgets down (01 §9 item 15) | observed |
| FM-NUM-17 | Float oracle in differential tests | float floor under-sizes (`floor(0.3/0.1)=2`, B01–B02) | exact implementation and float oracle disagree; tests become unreliable | differential tests against an exact oracle only | observed |

### Double counting and accounting (FM-DC)

| ID | Failure | Effect | Rule |
|---|---|---|---|
| FM-DC-1 | Entry spread added on top of a limit/fill price that already contains it | overstated risk (conservative but inconsistent) or, in the reverse error, understated risk when using mid | DC-1 |
| FM-DC-2 | Exit cost charged in $W$ (via $\Lambda$) and again in open risk | budget understated (conservative) — **now deliberate** (OC-1) because the credit breaks liquidity monotonicity (RT-35) | DC-5 revised |
| FM-DC-7 | Add-on risk summed per lot | combined exit cost $(q+n)\kappa^{\mathrm{out}}(q+n)$ exceeds $q\kappa^{\mathrm{out}}(q)+n\kappa^{\mathrm{out}}(n)$; floor breach (RT-36) | G11; RQ-34 |
| FM-DC-8 | Pending orders charged at notional in tier U | their fees are omitted; floor breach by the fees | $Z^{\mathrm{res}}$ at full $L^{\mathrm{abs}}$ |
| FM-DC-3 | Gap loss inside stop risk and again as gap risk in one budget | double charge | DC-3 |
| FM-DC-4 | Realised + unrealised + $\Delta W$ summed | double count | DC-4 |
| FM-DC-5 | Open risk measured from entry price rather than current mark | untrailed winners' give-back ignored; understated risk relative to $W$ | DC-5 (open risk from current mark) |
| FM-DC-6 | Model re-estimation of $\Lambda$ booked as trading P&L | spurious P&L | DC-9 |

### Drawdown and floors (FM-DD)

| ID | Failure | Effect | Mitigation |
|---|---|---|---|
| FM-DD-1 | HWM on raw $W$ with deposits/withdrawals | false new highs / false drawdowns and spurious halts | unitisation (05 §6) |
| FM-DD-2 | Ratcheting floor without trailing | invariant breaks on gains (T-20b); later $\mathrm{DD}>d^{\max}$ without any new trade | RECOVERY + external trailing obligation (RQ-09) |
| FM-DD-3 | Daily limit on realised P&L only | unrealised losses bypass the limit | prospective cushion H4 (DC-4) |
| FM-DD-4 | Throttle chattering at step thresholds | budget flips with tiny P&L moves | continuous cushion throttle |
| FM-DD-5 | "Recovery boost" (raise risk after losses) | non-monotone; ruin-seeking | forbidden by T-05 |
| FM-DD-6 | Negative wealth | $B\le0$ ⇒ negative budgets without clamp | $(\cdot)^+$; RECOVERY |
| FM-DD-7 | Daily/weekly floor reset after a gain day | cushion invariant breaks without a new high (06 §7) | RECOVERY + trailing obligation |
| FM-DD-8 | Withdrawal inside a period with an absolute floor | $F^{\mathrm{abs}}$ breached although every stop held | flows only at epoch boundaries |

### Tail and gap (FM-TAIL)

| ID | Failure | Effect | Mitigation |
|---|---|---|---|
| FM-TAIL-1 | VaR aggregation | diversification appears to *add* no risk while risk increases (T-26) | ES; sum-aggregation in hard layer |
| FM-TAIL-2 | φ-divergence ambiguity cannot place mass beyond observed support: if the worst observed gap is 8%, no law in a KL ball has a 9% gap | tail risk capped at history | Wasserstein/EVT/moment sets for tails; policy floor $\Gamma^{\min}$ |
| FM-TAIL-3 | Gaps beyond stop (overnight, events, halts) | A-STOP fails; floor breach (T-06b gap example) | tier G; event gates; T-25 research focus |
| FM-TAIL-4 | Heavy tails invalidate light-tail concentration radii | DRO radius under-covers | RQ-12 |
| FM-TAIL-5 | Tight stops allow huge notional | loss $\gg$ risk budget (T-17a) | H5–H11 |

### Correlation (FM-COR)

| ID | Failure | Effect | Mitigation |
|---|---|---|---|
| FM-COR-1 | Correlation multiplier $>1$ from negative/unstable $\hat{\bar\rho}$ (F132) | budget enlarged beyond hard | forbidden (Art. 5, T-18) |
| FM-COR-2 | Calm-regime correlation understates crash co-movement | concentrated gap losses | comonotone hard aggregation; RQ-22 |
| FM-COR-3 | ETF/constituent overlap across clusters | hidden concentration | look-through (RQ-10) |

### Statistical (FM-STAT)

| ID | Failure | Effect | Mitigation |
|---|---|---|---|
| FM-STAT-1 | Look-ahead via restated vendor data, survivorship | optimistic research results | NLA admission rule; bitemporal data (RQ-29) |
| FM-STAT-2 | Regime change / parameter instability | calibrated $\Gamma_i,\kappa^{\mathrm{out}}$ too optimistic | policy floors; sub-period stability tests |
| FM-STAT-3 | Kelly with estimated edge | $\hat P^{\mathrm{win}}=1$ ⇒ $f^{\mathrm{K}}=1$; overbetting beyond $\approx2f^{\mathrm{K}}$ destroys growth (F131) | robust/fractional forms; certificate |
| FM-STAT-4 | Multiple testing across opportunities | false certifications | RQ-15 |
| FM-STAT-5 | Parameter selection on the test sample | invalid evidence | 01 §11 |

### Optimisation (FM-OPT)

| ID | Failure | Effect | Mitigation |
|---|---|---|---|
| FM-OPT-1 | Unbounded objective (affine $J$ without caps) | size → cap or ∞ (T-16) | caps; concave $J$ |
| FM-OPT-2 | Empty feasible set → solver exception → fallback guess | unsafe action | Art. 13/18: $a^{\varnothing}$ |
| FM-OPT-3 | Argmax non-monotone in ambiguity | more uncertainty ⇒ larger size (T-09N) | feasibility-defined caps |
| FM-OPT-4 | Standalone Kelly for incremental decision | ignores existing portfolio | incremental $\Delta J$ |

### Authority and operations (FM-AUTH / FM-OPS)

| ID | Failure | Effect | Mitigation |
|---|---|---|---|
| FM-AUTH-1 | Missing field defaulted to 0 | budget double-spend (T-04 counterexample) | absence ≠ zero |
| FM-AUTH-2 | Stale snapshot / decision reused after state change | double-spend (T-11 race) | CAS on snapshot/ledger version |
| FM-AUTH-3 | Wrong account scope | decision about another account | account-identifier binding in $x^{A}_t$ (UNDEFINED method) |
| FM-OPS-1 | Crossed/locked market | mid ill-defined | G7/validity: invalid |
| FM-OPS-2 | Corporate action between decision and fill | $q$/price scale mismatch vs reservation | UNDEFINED handling (05 §9) |
| FM-OPS-3 | Held position with $m<p^{\mathrm{stop}}$ and no trigger | negative "risk" frees budget | ANOMALY ⇒ $\alpha=0$ |
| FM-OPS-4 | DST / half-day / holiday boundaries | wrong daily floor reset | versioned exchange calendar (RQ-31) |
| FM-OPS-5 | Sequential allocation order | non-replayable allocations (T-23) | authoritative ordering key |
| FM-OPS-6 | Stop triggered but not filled at the cut; stop not live on early partial fills | loss beyond $r^{\mathrm{open}}$ with A-STOP technically intact | A-TRIG (position level, F072); A-STOPLIVE |
| FM-OPS-7 | Per-execution minimum fees on split fills | fees exceed $\phi(n)$ | A-EXE-04; RQ-35 |
| FM-OPS-8 | Corporate action inside a period | split booked as a loss (05 §1) | split the period at $\tau^{\mathrm{CA}}$ |
| FM-OPS-9 | Exit split into several fee-bearing parts under per-order minimum fees (partial fill at the cut; one child stop per entry fill) | fees paid plus the remainder's valuation fee exceed $\phi^{\mathrm{sell}}(q)$; floor breached by 1 for a new order (AUD-001 fill pattern, REV-029) | position-level A-TRIG (F072); split envelope F140 with the declared $N^{\mathrm{ex}}$ |
| FM-OPS-10 | Reservation computed with inputs older than the epoch's (exit-cost estimate raised, stop widened) | pending order under-charged; floor breached by 40 in the T-10N example | F144: charge the larger of ledger and re-evaluated reservation |

### Dimensional (FM-DIM, added v0.2, AUD-031)

| ID | Failure | Effect | Mitigation |
|---|---|---|---|
| FM-DIM-1 | $\lfloor R/\ell\rfloor$ applies the floor to a share-dimensioned quantity | correct only when $\delta_q=1$ sh; for $\delta_q=10^{-k}$ sh the result is off the lattice or wrong by a factor | $\delta_q\lfloor R/(\delta_q\ell)\rfloor$ (F095, F110; 03 E-18) |
| FM-DIM-2 | Volatility target written as risk fraction × $W/\hat\sigma$ | [USD·day$^{1/2}$], not a notional; any numeric use silently mixes units | notional $=W\sigma^{\mathrm{target}}/\hat\sigma$ (F133; 03 E-19) |

## Part C — Coverage of the brief's mandatory search list

| Brief item | Entries |
|---|---|
| division by zero | FM-NUM-6, RT-28, T-02 |
| unbounded objective | FM-OPT-1, T-16 |
| negative wealth | FM-DD-6, RT-12 |
| log of zero / log of negative wealth | FM-NUM-8, T-19 |
| tail losses | FM-TAIL-1..4 |
| gaps beyond stop | FM-TAIL-3, T-06b, T-17a, T-25 |
| liquidity collapse | A-LIQ, RQ-06, T-07 |
| correlated risk multipliers | FM-COR-1..3, RT-25 |
| double counting | FM-DC-1..6, 05 §4 |
| rounding overshoot | FM-NUM-3, FM-NUM-4, FM-NUM-16, T-02N, T-22N, T-24 |
| solver tolerance violations | FM-NUM-9, T-03 |
| model uncertainty | T-12a, T-09N, 01 §4 |
| regime change / parameter instability | FM-STAT-2, FM-STAT-3 |
| empty feasible set | FM-OPT-2, 01 §7 |

## Appendix — reproduction record for "observed" items

Evidence probes only (Python 3.11.15, standard library; not engine code, not committed as code). Exact rationals (`fractions.Fraction`)
serve as the reference.

| Item | Expression | Observed result |
|---|---|---|
| FM-NUM-1 | `min(5.0, nan)`, `min(nan, 5.0)` | `5.0`, `nan` |
| FM-NUM-2 | `Decimal('NaN').max(Decimal(5))`, `Decimal(5).min(Decimal('NaN'))` | `5`, `5` |
| — | `Decimal('NaN') < 1`; `min(Decimal(5), Decimal('NaN'))` | raise `InvalidOperation` (default traps: InvalidOperation, DivisionByZero, Overflow) |
| FM-NUM-3 | `(Decimal('1000.00')/Decimal('2.90')).quantize(Decimal('1'), ROUND_HALF_UP)` | `345` (risk `1000.50`) |
| FM-NUM-4 | `floor(float('172808193.53')/float('65.68583269'))` vs exact | `2630829` vs `2630828` |
| FM-NUM-4 | random search, $2\times10^6$ cases, $R$ to cents ≤ $10^7$, $\ell$ to $10^{-4}$ ≤ $100$ | no overshoot (consistent with T-22) |
| FM-NUM-5 | `100.07 - 99.97` | `0.09999999999999432` |
| FM-NUM-7 | `Decimal('123456789012345.12345678') * Decimal('1000000.0000001')` at prec 28 | rounded result; `Inexact` flag set, no exception |
| FM-NUM-8 | `Decimal(0).ln()`; `math.log(0.0)` | `-Infinity` (no signal); `ValueError` |
| 01 §9.4 | `Decimal(2).sqrt()` and `Decimal(2).ln()` at prec 5 under ROUND_FLOOR vs ROUND_CEILING | identical results (context rounding ignored) |
| FM-NUM-12 | `Fraction(0.1)` | `3602879701896397/36028797018963968` |
| T-02N | $g(n)=0.10n+2\max(1,0.005n)$, budget $2.50$ | naive $22$ ($g=4.20$); true $5$ ($g=2.50$) |
