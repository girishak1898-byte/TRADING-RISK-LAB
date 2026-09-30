# 09 — Known Mathematical Failure Modes and Red-Team Classification (v0.1.1-draft)

Classification vocabulary (per brief): **PROVED · DISPROVED · COUNTEREXAMPLE FOUND · REQUIRES ADDITIONAL ASSUMPTION · UNDEFINED ·
NOT YET PROVEN.** "Observed" = reproduced numerically in this session.

## Part A — Formula-level classification

| ID | Formula / object | Classification | Evidence |
|---|---|---|---|
| F-01 | $R_{\mathrm{hard}}=E\times f$ as a sufficient hard envelope | **DISPROVED** | 06 §3 (ten defects); T-17 |
| F-02 | $R^{\mathrm{hard}}_t$ (06 §4) — computation | **PROVED** ($\ge0$, finite, monotone: T-01, T-05) | 08 |
| F-03 | $R^{\mathrm{hard}}_t$ — protective meaning | **REQUIRES ADDITIONAL ASSUMPTION** (A-STOP, A-TRIG) | T-10, T-25 |
| F-04 | $Q=\lfloor R/\ell\rfloor$ | **PROVED** for linear $g$ in exact arithmetic; **COUNTEREXAMPLE FOUND** for min-commission fees, half-up, binary64 (observed) | T-02, T-22 |
| F-05 | $Q^{\mathrm{hard}}=\lfloor\min_k Q_k^{*}\rfloor$ | **PROVED** under monotone constraints; **COUNTEREXAMPLE FOUND** for non-monotone constraints | T-03 |
| F-06 | $L^{\mathrm{stop}}(n)$ as a loss bound | **REQUIRES ADDITIONAL ASSUMPTION** (A-STOP, A-TRIG, A-MKT-05) | T-10 |
| F-07 | $L^{\mathrm{gap}}(n)$ | **REQUIRES ADDITIONAL ASSUMPTION** (A-GAP); $\Gamma$ **UNDEFINED** | RQ-04 |
| F-08 | $L^{\mathrm{abs}}(n)$ (long) | **PROVED** under A-MKT-01/05; short analogue **UNDEFINED** (unbounded) | 05 §5 |
| F-09 | $W=E-\Lambda$ | **UNDEFINED** until $\Lambda$ is specified | RQ-05 |
| F-10 | Wealth transition $G$ | **PROVED** (identity) under A-ACC-01..03 | 05 §2 |
| F-11 | ECAI | **PROVED**; ex-post impact/slippage split **UNDEFINED** (not identifiable) | 05 §3 |
| F-12 | $DD=1-\nu/H$ | **PROVED** well-defined iff $H>0$ (requires $\nu_0>0$); $DD\ge1\iff\nu\le0$ | 02 S-102 |
| F-13 | Cushion-induced throttle $\vartheta_K$ | **PROVED** continuous, monotone, zero at $d^{\max}$ | 06 §7, T-05 |
| F-14 | Step throttle | **PROVED** discontinuous (unbounded sensitivity at thresholds) — admissible only below the cushion line | 06 §7 |
| F-15 | Exponential throttle as floor mechanism | **DISPROVED** (never reaches zero) | 06 §7 |
| F-16 | "MDD ≤ $d^{\max}$" from shutdown alone | **DISPROVED** | T-06(b) |
| F-17 | Kelly $f^{*}=p-(1-p)/b$ with estimated $p,b$ | **COUNTEREXAMPLE FOUND**: $\hat p=1$ from a short all-win sample gives $f^{*}=1$ (all wealth at risk); **UNDEFINED** under estimation error without a robust formulation | FM-STAT-3 |
| F-18 | $\mathbb E[\log(W_{t+1}/W_t)]$ | **REQUIRES ADDITIONAL ASSUMPTION** ($W^{\min}_{t+1}>0$) | T-19 |
| F-19 | Wasserstein-DRO log growth | **REQUIRES ADDITIONAL ASSUMPTION** (support restriction; radius justification under heavy tails/dependence — A-STAT-01/02 likely false) | T-19, 01 §4 |
| F-20 | KL/φ-divergence ES as tail model | **COUNTEREXAMPLE FOUND** (cannot exceed worst observed outcome) | FM-TAIL-2 |
| F-21 | VaR as aggregatable budget | **DISPROVED** (non-subadditive) | T-26 |
| F-22 | $\mathrm{ES}_\beta$ as optimisable measure | coherence is a standard literature result (Acerbi & Tasche 2002) — **not re-proved in this register**; high-$\beta$ estimator **UNDEFINED** | 01 §5 |
| F-23 | Nested CVaR for multi-period | **NOT YET PROVEN** appropriate (conservatism compounding) | RQ-23 |
| F-24 | CVaR surrogate of floor chance constraint | **PROVED** conservative: $\mathrm{VaR}_{1-\epsilon}(Z)\le\mathrm{ES}_{1-\epsilon}(Z)$, so $\mathrm{ES}_{1-\epsilon}(F_t-W_{t+1})\le0\Rightarrow\mathbb P(W_{t+1}<F_t)\le\epsilon$; needs a law ⇒ model layer only | 01 §5 |
| F-25 | Correlation-adjusted risk multiplier (e.g. $1/\sqrt{1+(k-1)\bar\rho}$) | **COUNTEREXAMPLE FOUND** ($\hat{\bar\rho}<0$ ⇒ multiplier $>1$ enlarges budget; calm-regime $\hat\rho$ understates crash correlation) | FM-COR-1, T-18 |
| F-26 | Robust advantage as difference of infima | **COUNTEREXAMPLE FOUND** | P-12a |
| F-27 | Additive error allowance in advantage test | **PROVED** for deterministic bounds; **REQUIRES ADDITIONAL ASSUMPTION** for statistical bounds (confidence, union bound); **UNDEFINED** for misspecification | P-12b |
| F-28 | Volatility-targeted size $fW/\hat\sigma$ | **COUNTEREXAMPLE FOUND**: $\hat\sigma=0$ (halted or stale flat series) ⇒ division by zero / unbounded size | FM-NUM-6 |
| F-29 | Buying-power cap with market orders | **UNDEFINED** (no price bound) | D-05 |
| F-30 | Gambler's-ruin closed forms for PoR | **UNDEFINED** in this architecture (assume i.i.d. fixed bets; sizing here is state-dependent) — replaced by T-25 decomposition | 01 §5 |
| F-31 | Argmax-defined model sizing monotone in ambiguity | **COUNTEREXAMPLE FOUND** | T-09 |
| F-32 | Floor invariance under hold with ratcheting floor | **DISPROVED** | T-20(b) |
| F-33 | Binary64 floor of $R/\ell$ | **PROVED** safe under $r\,d_\ell<2^{51}$; **COUNTEREXAMPLE FOUND** outside (observed) | T-22 |
| F-34 | Greedy sequential allocation | **PROVED** order-dependent | T-23 |
| F-35 | Open risk with $\Lambda$ credit (v0.1 DC-5) | **COUNTEREXAMPLE FOUND** (budgets rise as liquidity worsens) — replaced by OC-1 | T-07 |
| F-36 | Per-lot risk for add-ons, $r^{\mathrm{open}}(q)+L^{\mathrm{stop}}(n)$ | **COUNTEREXAMPLE FOUND** (super-additive exit costs) — G11 | T-10 |

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
| FM-NUM-9 | Solver tolerance | constraint satisfied to $10^{-6}$ | exact cap violated | exact post-verification (T-03(c)) | known |
| FM-NUM-10 | Global numeric context mutation | other code changes default precision/rounding | non-reproducible results | local contexts only | known |
| FM-NUM-11 | Hash-seed-dependent iteration | iterating a set of strings | order-dependent sums/allocations | sorted iteration | known |
| FM-NUM-12 | Float-typed input parsed as authority | `Decimal(0.1)` from a float | value ≠ intended decimal | reject float type at boundary | observed |

### Double counting and accounting (FM-DC)

| ID | Failure | Effect | Rule |
|---|---|---|---|
| FM-DC-1 | Entry spread added on top of a limit/fill price that already contains it | overstated risk (conservative but inconsistent) or, in the reverse error, understated risk when using mid | DC-1 |
| FM-DC-2 | Exit cost charged in $W$ (via $\Lambda$) and again in open risk | budget understated (conservative) — **now deliberate** (OC-1) because the credit breaks liquidity monotonicity (F-35) | DC-5 revised |
| FM-DC-7 | Add-on risk summed per lot | combined exit cost $(q+n)\kappa(q+n)$ exceeds $q\kappa(q)+n\kappa(n)$; floor breach (F-36) | G11; RQ-34 |
| FM-DC-8 | Pending orders charged at notional in tier U | their fees are omitted; floor breach by the fees | $Z^{\mathrm{res}}$ at full $L^{\mathrm{abs}}$ |
| FM-DC-3 | Gap loss inside stop risk and again as gap risk in one budget | double charge | DC-3 |
| FM-DC-4 | Realised + unrealised + $\Delta W$ summed | double count | DC-4 |
| FM-DC-5 | Open risk measured from entry price rather than current mark | untrailed winners' give-back ignored; understated risk relative to $W$ | DC-5 (open risk from current mark) |
| FM-DC-6 | Model re-estimation of $\Lambda$ booked as trading P&L | spurious P&L | DC-9 |

### Drawdown and floors (FM-DD)

| ID | Failure | Effect | Mitigation |
|---|---|---|---|
| FM-DD-1 | HWM on raw $W$ with deposits/withdrawals | false new highs / false drawdowns and spurious halts | unitisation (05 §6) |
| FM-DD-2 | Ratcheting floor without trailing | invariant breaks on gains (T-20); later $DD>d^{\max}$ without any new trade | RECOVERY + external trailing obligation (RQ-09) |
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
| FM-TAIL-3 | Gaps beyond stop (overnight, events, halts) | A-STOP fails; floor breach (T-06 gap example) | tier G; event gates; T-25 research focus |
| FM-TAIL-4 | Heavy tails invalidate light-tail concentration radii | DRO radius under-covers | RQ-12 |
| FM-TAIL-5 | Tight stops allow huge notional | loss $\gg$ risk budget (T-17) | H5–H11 |

### Correlation (FM-COR)

| ID | Failure | Effect | Mitigation |
|---|---|---|---|
| FM-COR-1 | Correlation multiplier $>1$ from negative/unstable $\hat\rho$ | budget enlarged beyond hard | forbidden (Art. 5, T-18) |
| FM-COR-2 | Calm-regime correlation understates crash co-movement | concentrated gap losses | comonotone hard aggregation; RQ-22 |
| FM-COR-3 | ETF/constituent overlap across clusters | hidden concentration | look-through (RQ-10) |

### Statistical (FM-STAT)

| ID | Failure | Effect | Mitigation |
|---|---|---|---|
| FM-STAT-1 | Look-ahead via restated vendor data, survivorship | optimistic research results | NLA admission rule; bitemporal data (RQ-29) |
| FM-STAT-2 | Regime change / parameter instability | calibrated $\Gamma,\kappa$ too optimistic | policy floors; sub-period stability tests |
| FM-STAT-3 | Kelly with estimated edge | $\hat p=1$ ⇒ $f^{*}=1$; overbetting beyond $\approx2f^{*}$ destroys growth | robust/fractional forms; certificate |
| FM-STAT-4 | Multiple testing across opportunities | false certifications | RQ-15 |
| FM-STAT-5 | Parameter selection on the test sample | invalid evidence | 01 §11 |

### Optimisation (FM-OPT)

| ID | Failure | Effect | Mitigation |
|---|---|---|---|
| FM-OPT-1 | Unbounded objective (affine $J$ without caps) | size → cap or ∞ (T-16) | caps; concave $J$ |
| FM-OPT-2 | Empty feasible set → solver exception → fallback guess | unsafe action | Art. 13/18: $a^{\varnothing}$ |
| FM-OPT-3 | Argmax non-monotone in ambiguity | more uncertainty ⇒ larger size (T-09) | feasibility-defined caps |
| FM-OPT-4 | Standalone Kelly for incremental decision | ignores existing portfolio | incremental $\Delta J$ |

### Authority and operations (FM-AUTH / FM-OPS)

| ID | Failure | Effect | Mitigation |
|---|---|---|---|
| FM-AUTH-1 | Missing field defaulted to 0 | budget double-spend (T-04 counterexample) | absence ≠ zero |
| FM-AUTH-2 | Stale snapshot / decision reused after state change | double-spend (T-11 race) | CAS on snapshot/ledger version |
| FM-AUTH-3 | Wrong account scope | decision about another account | $A_{\mathrm{id}}$ binding (UNDEFINED method) |
| FM-OPS-1 | Crossed/locked market | mid ill-defined | G7/validity: invalid |
| FM-OPS-2 | Corporate action between decision and fill | $q$/price scale mismatch vs reservation | UNDEFINED handling (05 §9) |
| FM-OPS-3 | Held position with $m<p^{\mathrm{stop}}$ and no trigger | negative "risk" frees budget | ANOMALY ⇒ $\alpha=0$ |
| FM-OPS-4 | DST / half-day / holiday boundaries | wrong daily floor reset | versioned exchange calendar (RQ-31) |
| FM-OPS-5 | Sequential allocation order | non-replayable allocations (T-23) | authoritative ordering key |
| FM-OPS-6 | Stop triggered but not filled at the cut; stop not live on early partial fills | loss beyond $r^{\mathrm{open}}$ with A-STOP technically intact | A-TRIG broadened; A-STOPLIVE |
| FM-OPS-7 | Per-execution minimum fees on split fills | fees exceed $\phi(n)$ | A-EXE-04; RQ-35 |
| FM-OPS-8 | Corporate action inside a period | split booked as a loss (05 §1) | split the period at $\tau^{\mathrm{CA}}$ |

## Part C — Coverage of the brief's mandatory search list

| Brief item | Entries |
|---|---|
| division by zero | FM-NUM-6, F-28, T-02 note |
| unbounded objective | FM-OPT-1, T-16 |
| negative wealth | FM-DD-6, F-12 |
| log of zero / log of negative wealth | FM-NUM-8, T-19 |
| tail losses | FM-TAIL-1..4 |
| gaps beyond stop | FM-TAIL-3, T-06, T-17, T-25 |
| liquidity collapse | A-LIQ, RQ-06, T-07 |
| correlated risk multipliers | FM-COR-1..3, F-25 |
| double counting | FM-DC-1..6, 05 §4 |
| rounding overshoot | FM-NUM-3, FM-NUM-4, T-02, T-22, T-24 |
| solver tolerance violations | FM-NUM-9, T-03(c) |
| model uncertainty | P-12a, T-09, 01 §4 |
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
| T-02 | $L(n)=0.10n+2\max(1,0.005n)$, $b=2.50$ | naive $22$ ($L=4.20$); true $5$ ($L=2.50$) |
