# 07 — Research Questions (v0.1.1-draft)

Each question is tagged with what it **blocks**. Method lines state *how* the question will be answered, not the answer.
"Data" questions require a historical data source, which is itself open (RQ-29). No question may be answered using the final
test sample (01 §11).

## A. Scope, definitions, policy (mostly human decisions informed by analysis)

| ID | Question | Blocks | Method | Acceptance criterion |
|---|---|---|---|---|
| RQ-01 | Resolve scope decisions D-01..D-07 | nearly everything | decision record (13) | signed decision per item |
| RQ-02 | Which risk base $B_t$ (B1–B4)? | all $f\cdot B$ budgets | analytic comparison (monotonicity, $B\le W$, procyclicality) + Phase-16 simulation | chosen $B$ satisfies T-05 and $B\le W$ (or H11 rewritten) |
| RQ-03 | HWM observation set $\mathcal H_t$: end-of-day or intraday marks? | $F^{\mathrm{dd}},F^{\mathrm{lock}}$, $DD$ | analytic (intraday HWM ratchets harder ⇒ more RECOVERY events) + simulation | documented trade-off; human choice |
| RQ-11 | How is strategy loss $\mathrm{SL}_{s,t}$ attributed (fills, costs, shared positions)? | H3 | accounting design; conservation check (attribution sums to total) | attribution identity proved |
| RQ-24 | Parameter governance: who may change $\theta$, with what evidence, with what versioning? | Art. 16 | process design | written procedure |
| RQ-30 | Ruin definition: floor breach vs $W\le0$; horizon | PoR, $\epsilon^{\mathrm{ruin}}$ | definitional | chosen and registered |
| RQ-31 | Calendar semantics: trading-day/week boundaries (exchange time zone, half days, holidays); flow-timing convention for unitisation | $F^{\mathrm{day}},F^{\mathrm{wk}}$, $U_t$ | specification against a versioned exchange calendar | boundary tests specified |
| RQ-32 | Should pre-existing open risk be charged against today's daily floor (prospective reading) or only risk opened today? | H4 semantics | analytic: prospective reading is the only one that guarantees $W\ge F^{\mathrm{day}}$ under A-STOP (T-21) | human confirmation |

## B. Market-microstructure and tail evidence (data required)

| ID | Question | Blocks | Method | Acceptance criterion |
|---|---|---|---|---|
| RQ-04 | Distribution of **gap-through-stop** severity by instrument class, horizon class (intraday/overnight/weekend) and scheduled events; how to set $\Gamma_i$ and $\Gamma^{\min}$ | tier G, H5–H6, T-25 | event study of adverse jumps relative to prior last price; peaks-over-threshold (GPD) with declustering; block-bootstrap CIs; separate event/non-event samples; source for event calendar | calibrated $\Gamma$ with uncertainty; stability across sub-periods; documented exceedance frequency |
| RQ-05 | Normal-condition stop exit cost $\kappa^{\mathrm{out}}(n)$ and liquidation-cost model $\Lambda$ | $W_t$, tier S, DC-5 | empirical slippage of stop-triggered market orders vs trigger price, conditioned on spread, volatility, size/ADV; monotone model class | monotone model passing A-EXE-02 checks; out-of-sample error bounds |
| RQ-06 | ADV estimator for hard caps (window, robust statistic, min of short/long windows) and liquidity-drought frequency | H12–H13, A-LIQ | historical study of volume collapses relative to trailing ADV | estimator with documented A-LIQ failure rate |
| RQ-07 | Which constraints bind empirically for the target universe and account sizes (stop, gap, notional, liquidity, BP)? | prioritisation of calibration effort | simulation over historical opportunity sets (train period only) | binding-frequency table per constraint |
| RQ-21 | Stop-trigger semantics and halts/LULD pauses: what does A-TRIG require, and how long can exit be impossible? | A-TRIG, T-10 | market-rule review (primary sources) + halt-duration statistics | written trigger model; halt-duration distribution |
| RQ-22 | Joint gap stress: how often do many held names gap together (crash co-movement)? | H5 aggregation, $m_G$ | co-exceedance analysis; tail dependence estimates (model layer only) | stress scenario set with frequencies |

## C. Uncertainty, tail risk, objective, advantage

| ID | Question | Blocks | Method | Acceptance criterion |
|---|---|---|---|---|
| RQ-12 | Which ambiguity set (if any) is statistically justified for the model layer, given heavy tails and dependence? | 01 §4 adoption | literature (11) + tests of A-STAT-01/02 on training data + walk-forward radius calibration | justification whose assumptions pass tests, or explicit rejection of DRO |
| RQ-13 | Objective $J$: arithmetic, log-growth, fractional Kelly, mean–ES, robust growth, risk-sensitive? | Phase 8, certificate | analytic (domains, T-16, T-19) + Phase-17 comparison at equal safety | selected $J$ with declared units and domain proof |
| RQ-14 | Can a positive advantage over $a^{\varnothing}$ be certified with realistic data at all? Required sample sizes for given edge/noise | Phase 10, D-10 | power analysis for $\Delta J>0$ under realistic signal-to-noise; P-12b error budget | power curves; decision whether certification is feasible or advisory |
| RQ-15 | Multiple testing across many opportunities per day: how to control false certifications | certificate validity | FWER/FDR control (Romano–Wolf, Benjamini–Hochberg), reality-check style tests | stated error-rate guarantee |
| RQ-23 | If multi-period optimisation is ever adopted: time-consistent risk measure (nested vs static) | Phase 8 extension | literature + counterexamples | not needed for v0 |
| RQ-26 | Evaluation metric for comparing architectures that does not reward risk-taking | Phase 17 | define safety-first lexicographic metric; growth at equal floor-breach frequency | metric specified before any comparison is run |

## D. Numerical and systems questions

| ID | Question | Blocks | Method | Acceptance criterion |
|---|---|---|---|---|
| RQ-16 | Exact representation: rationals throughout vs decimals with trapped `Inexact` and per-variable directed rounding | R-05 | prototype both on the hard layer only; compare proof burden and performance | chosen representation with T-24 argument |
| RQ-17 | Certified bounds for non-rational cost terms (e.g. $\sqrt{\ }$ impact) | T-07 with such models | verify-then-adjust technique (01 §9.4) | exact certificate per evaluation |
| RQ-18 | Method to prove completeness of $\mathcal R^{\mathrm{req}}$ (read-set ⊆ registry) | T-04 | static analysis + runtime instrumentation | automated check in CI |
| RQ-19 | TTL per datum class (quotes, positions, ledger, reference data, estimates) | $\alpha_t$ | analysis of data-update frequencies and decision latency | TTL table |
| RQ-20 | Cash-account buying-power semantics: settled vs unsettled cash, settlement lag, good-faith rules; definition of $C^{\mathrm{avail}}$ | H14 | primary regulatory sources + broker documentation (read-only research; no connectivity) | definition of $C^{\mathrm{avail}}$ that never exceeds broker BP |
| RQ-25 | Fractional shares: lattice, broker rounding, protective-stop support for fractional quantities | D-04 | documentation review | verified semantics or exclusion |
| RQ-27 | Multiple opportunities at one epoch: authoritative ordering key; greedy vs joint allocation | T-23, replay | specification; compare greedy vs small integer programme | deterministic, replayable batch rule |
| RQ-28 | Decision epochs: event-driven vs clock-driven; effect on tail measures | §5 of 01 | specification | chosen and registered |
| RQ-29 | Historical data source with bitemporal (knowledge-time) fidelity, corporate actions, delisted names, quotes for spreads | all data RQs | vendor/source assessment (no broker connectivity) | source meeting NLA and survivorship requirements |
| RQ-34 | Add-on (scaling-in) risk: prove the incremental combined-bound charge (05 §5) including pending orders on the same instrument and a single authoritative stop per instrument | lifting G11 / D-12 | derivation + counterexample search | proof reviewed; G11 relaxable |
| RQ-35 | Fee semantics: per order vs per execution; minimums, caps and rounding of regulatory fees; worst-case-over-splits envelope | A-EXE-04, T-10, T-11 | primary fee-schedule sources (read-only) | fee model with proven upper bound per order |
| RQ-33 | Is mechanised verification (e.g. an interactive theorem prover) worth its cost for T-01..T-03, T-10, T-24? | assurance level | pilot on T-02 | cost/benefit note |

## E. Drawdown and recovery

| ID | Question | Blocks | Method | Acceptance criterion |
|---|---|---|---|---|
| RQ-08 | Does any throttle below the cushion line improve safety-adjusted outcomes? | 06 §7 | Phase-16 simulation comparing families of 06 §7 at equal floor safety | benefit survives multiple-testing correction, or no extra throttle |
| RQ-09 | Design of the stop-trailing / de-risking obligation for ratcheting floors (T-20) and its authority owner | RECOVERY semantics, T-06(c) | analytic (required trailing rate) + simulation | obligation specified; owner assigned outside the engine |
| RQ-10 | Cluster map $\mathrm{cl}$: sector taxonomy vs statistical clustering; stability; handling of ETFs overlapping constituents | H9–H10 | stability analysis over time; look-through for ETFs | versioned map with stability evidence |
