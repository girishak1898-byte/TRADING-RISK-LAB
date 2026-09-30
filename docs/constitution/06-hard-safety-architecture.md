# 06 — Candidate Deterministic Hard-Safety Architecture (v0.1-draft)

Status: DRAFT. Structure is PROVISIONAL; all parameter **values** are **UNDEFINED — REQUIRES RESOLUTION** (human policy).
Scope assumed: v0 long-only, cash account, US-listed equities/ETFs, limit-price entries (decisions D-01..D-05 in 04 — not yet
taken). Theorem references point to [08](08-theorem-register.md).

---

## 1. What "deterministic" means here

The hard envelope is **deterministic in computation**: an exact, pure function of authoritative inputs and policy constants.
Its **protective meaning is conditional**: each constraint guarantees a wealth outcome only under a named assumption about
the world. Conflating the two is the central error this architecture is designed to prevent (T-17).

## 2. Guarantee tiers

| Tier | Guarantee holds if … | Constraint family | Assumption strength |
|---|---|---|---|
| **U** — unconditional | prices $\ge0$ (A-MKT-01), limits respected (A-MKT-05), ledger/custody integrity (A-AUTH-01) | notional, gross, concentration, buying power, absolute-loss cushion | weakest (structural facts for long cash equities) |
| **S** — stop | every triggered stop exits at $\ge p^{\mathrm{stop}}-\kappa^{\mathrm{out}}$ (A-STOP) with consistent trigger semantics (A-TRIG) | stop-risk budgets ($R$-family) | strong; **known to fail** in gaps and halts |
| **G** — gap stress | every triggered stop exits at $\ge(1-\Gamma_i)p^{\mathrm{stop}}$ (A-GAP) | gap-risk budgets ($G$-family) | medium; fails beyond the stress level |
| **L** — liquidity proxy | future tradable volume is not below the policy fraction of trailing ADV (A-LIQ) | participation and exit-horizon caps | medium; fails in liquidity collapse |

A decision record MUST state, for the chosen quantity, which tiers' constraints were **binding** and which tiers are
**guaranteed** (all constraints of a tier satisfied).

## 3. Why $R_{\mathrm{hard}}=\text{Equity}\times f$ is not sufficient (derivation)

Take $R=E_t\,f$ and size $Q=\lfloor R/\ell\rfloor$ with $\ell$ the stop distance. Each item below is a counterexample or a missing term;
together they determine the structure of §4–§6.

| # | Defect | Counterexample | Consequence for the design |
|---|---|---|---|
| 1 | Uses mark-to-mid equity $E$, not liquidation wealth $W$ | Illiquid holding: $E$ overstates exitable wealth by $\Lambda$ | base budgets on $W$ |
| 2 | Ignores open risk and reservations | Two opportunities evaluated from the same snapshot each receive the full $R$; aggregate $2R$ | aggregate budgets with $R^{\mathrm{open}}+R^{\mathrm{res}}$ (H2–H4) and snapshot-bound decisions (T-11) |
| 3 | Ignores capital floors | $k$ consecutive full stop-outs: $E_k=E_0(1-f)^k$ crosses any floor $F>0$ for $k>\log(F/E_0)/\log(1-f)$ | cushion constraint H4 |
| 4 | Stop distance is not a loss bound | $E=100{,}000$, $f=1\%$, stop $0.01$ below $50$: $Q=100{,}000$ sh $=5{,}000{,}000$ notional; a $5\%$ gap loses $\approx250{,}000\approx2.5E$ | gap budget H5–H6 and notional caps H7–H11 (T-17) |
| 5 | No liquidity bound | Same example: order may exceed daily volume of the instrument | H12–H13 |
| 6 | No cash bound | Notional can exceed buying power | H15 |
| 7 | Sign | $E\le0$ ⇒ $R\le0$ ⇒ $\lfloor R/\ell\rfloor<0$, readable as a sell / short | clamp $(\cdot)^+$ (T-01) |
| 8 | Non-linear fees | Minimum commission: naive $\lfloor R/(\ell+\text{fee rate})\rfloor$ can exceed $R$ (08 T-02: $22$ sh, loss $4.20>2.50$) | define $Q_k$ by exact monotone search (T-02) |
| 9 | Rounding / float | Half-up and binary64 overshoots (observed, 01 §9) | directed rounding, exact arithmetic (T-22, T-24) |
| 10 | Entry reference | $\ell$ from mid while fill is at limit: realised risk exceeds budget by $n(p^{\mathrm{lim}}-m)$ | use $p^{\mathrm{lim}}$ as worst-case entry (DC-1, T-11(c)) |

Conclusion: the single-scalar form $0\le R^{\mathrm{allow}}\le R^{\mathrm{hard}}$ is **necessary but not sufficient**. The invariant
must be vector-valued over every constraint family (Art. 5).

## 4. Budgets

**Risk base** $B_t$: **UNDEFINED — REQUIRES RESOLUTION** (RQ-02). Candidates and properties:

| Candidate | Non-decreasing in $W_t$ (needed by T-05) | $B_t\le W_t$ | Intraday procyclicality | Note |
|---|---|---|---|---|
| B1: $W_t$ | yes | yes | high (budgets rise with intraday gains) | simplest |
| B2: $\min(W_t,\ \nu^{\mathrm{day}}_0U_t)$ | yes | yes | gains do not raise budgets intraday; losses reduce them | conservative |
| B3: $K_t$ | yes (T-05) | yes if $F_t\ge0$ | follows cushion | merges sizing with floor; fractions then mean "of cushion" |
| B4: $\nu^{\mathrm{day}}_0U_t$ | yes (constant intraday) | **no** | none | violates $B\le W$ after intraday loss; H11 must then use $W_t$ directly |

**Hard stop-risk budget** (all $R$-family constraints have the form $L^{\mathrm{stop}}(n)\le b$, so they collapse to one scalar):

$$
R^{\mathrm{hard}}_t=\Big(\min\big\{\,f^{\mathrm{trd}}B_t,\ \ f^{\mathrm{port}}B_t-R^{\mathrm{open}}_t-R^{\mathrm{res}}_t,\ \ f^{\mathrm{strat}}_sB_t-R^{\mathrm{open}}_{s,t}-R^{\mathrm{res}}_{s,t},\ \ f^{\mathrm{clr}}B_t-R^{\mathrm{open}}_{c,t}-R^{\mathrm{res}}_{c,t},\ \ m_KK_t-R^{\mathrm{open}}_t-R^{\mathrm{res}}_t\,\big\}\Big)^{+}
$$

with $s$ the opportunity's strategy and $c=\mathrm{cl}(i)$.

**Hard gap-risk budget:**

$$
G^{\mathrm{hard}}_t=\Big(\min\big\{\,f^{\mathrm{gap}}B_t,\ \ m_GK_t-G^{\mathrm{open}}_t-G^{\mathrm{res}}_t\,\big\}\Big)^{+}
$$

**Model tightening** (Art. 5): $b^{\mathrm{allow}}_k=\min\big(b^{\mathrm{hard}}_k,\ \mathfrak s(b^{\mathrm{mod}}_k)\big)$ for every $k$; in particular
$R^{\mathrm{allow}}_t=\min(R^{\mathrm{hard}}_t,\mathfrak s(R^{\mathrm{mod}}_t))$. The REQUIRED/OPTIONAL flag of each model is policy.

**Unification of floors.** Daily, weekly, drawdown, absolute and profit-lock limits are all expressed as floors on $W$ and enter
through the single cushion $K_t=W_t-F_t$, $F_t=\max(F^{\mathrm{abs}},F^{\mathrm{dd}}_t,F^{\mathrm{day}}_t,F^{\mathrm{wk}}_t,F^{\mathrm{lock}}_t)$.
The daily limit is therefore enforced *prospectively* ("even if every open stop is hit today, $W\ge F^{\mathrm{day}}$"), not after the
fact on realised P&L (DC-4). Whether charging *pre-existing* open risk against today's floor is intended policy is **UNDEFINED —
REQUIRES RESOLUTION** (RQ-32); it is the conservative reading.

## 5. Constraint catalogue (single long opportunity on instrument $i$, candidate size $n$)

All consumptions $g_k(n)$ satisfy $g_k(0)=0$ and are non-decreasing in $n$ under A-EXE-01/02 — this is what makes T-02/T-03 apply.
Existing exposure terms use the current mark; the new order uses $p^{\mathrm{lim}}$.

| ID | Brief's cap | Constraint $g_k(n)\le b_k$ | Tier | Required inputs |
|---|---|---|---|---|
| H1 | risk (per trade) | $L^{\mathrm{stop}}(n)\le f^{\mathrm{trd}}B_t$ | S | $p^{\mathrm{lim}},p^{\mathrm{stop}}_o,\kappa^{\mathrm{out}},\phi$ |
| H2 | portfolio risk | $L^{\mathrm{stop}}(n)\le f^{\mathrm{port}}B_t-R^{\mathrm{open}}_t-R^{\mathrm{res}}_t$ | S | all open stops; ledger |
| H3 | strategy loss/risk | $L^{\mathrm{stop}}(n)\le f^{\mathrm{strat}}_sB_t-R^{\mathrm{open}}_{s,t}-R^{\mathrm{res}}_{s,t}-\mathrm{SL}_{s,t}$; strategy realised-loss term $\mathrm{SL}_{s,t}$ **UNDEFINED — REQUIRES RESOLUTION** (RQ-11) | S | strategy attribution |
| H4 | daily / weekly loss, drawdown, capital floor | $L^{\mathrm{stop}}(n)\le m_KK_t-R^{\mathrm{open}}_t-R^{\mathrm{res}}_t$ | S | $W,F$ components |
| H5 | gap loss (portfolio) | $L^{\mathrm{gap}}(n)\le m_GK_t-G^{\mathrm{open}}_t-G^{\mathrm{res}}_t$ | G | $\Gamma$ for all positions |
| H6 | gap loss (per trade) | $L^{\mathrm{gap}}(n)\le f^{\mathrm{gap}}B_t$ | G | $\Gamma_i$ |
| H7 | notional (per order) | $n\,p^{\mathrm{lim}}\le f^{\mathrm{ord}}B_t$ | U | — |
| H8 | concentration | $q_{i,t}m_{i,t}+N^{\mathrm{res}}_{i,t}+n\,p^{\mathrm{lim}}\le f^{\mathrm{conc}}B_t$ | U | — |
| H9 | correlation (cluster notional) | $\sum_{j\in c}q_{j,t}m_{j,t}+N^{\mathrm{res}}_{c,t}+n\,p^{\mathrm{lim}}\le f^{\mathrm{clu}}B_t$ | U (given the cluster map) | $\mathrm{cl}$ |
| H10 | correlation (cluster risk, comonotone) | $L^{\mathrm{stop}}(n)\le f^{\mathrm{clr}}B_t-R^{\mathrm{open}}_{c,t}-R^{\mathrm{res}}_{c,t}$ (folded into $R^{\mathrm{hard}}$) | S | $\mathrm{cl}$ |
| H11 | gross exposure / leverage | $N^{\mathrm{open}}_t+N^{\mathrm{res}}_t+n\,p^{\mathrm{lim}}\le\lambda^{\mathrm{gross}}\min(B_t,W_t)$, $\lambda^{\mathrm{gross}}\le1$ under D-02 | U | — |
| H12 | liquidity (entry) | $n\le\rho^{\mathrm{in}}\,w^{\mathrm{in}}\,\mathrm{ADV}_{i,t}$, $w^{\mathrm{in}}$ = order working window in trading days (the window-free form fails the dimension check E-08) | L | ADV |
| H13 | liquidity (exit) | $q_{i,t}+Q^{\mathrm{res}}_{i,t}+n\le\rho^{\mathrm{ex}}\,h^{\mathrm{ex}}\,\mathrm{ADV}_{i,t}$ | L | ADV |
| H14 | buying power | $n\,p^{\mathrm{lim}}+\phi^{\mathrm{buy}}(n)\le BP^{\mathrm{avail}}_t$ | U | $BP_t$, $C^{\mathrm{avail}}_t$, $C^{\mathrm{res}}_t$ |
| H15 | margin | **UNDEFINED — REQUIRES RESOLUTION**; excluded by D-02 (cash account ⇒ H14 suffices) | — | $IM,MM$ |
| H16 | unconditional floor (optional) | $\sum_j u^{\mathrm{open}}_j+N^{\mathrm{res}}_t+L^{\mathrm{abs}}(n)\le K_t$ | U | — ; adoption **UNDEFINED — REQUIRES RESOLUTION** (D-08) |

Zero–one **gates** (independent of $n$): G1 $\alpha_t=1$; G2 $\mathrm{st}_i=\text{TRADING}$; G3 $K_t>0$; G4 $DD_t<d^{\max}$;
G5 $\varsigma_i/m_i\le\varsigma^{\max}$; G6 event policy on $\mathrm{ev}_i$ (**UNDEFINED — REQUIRES RESOLUTION**); G7 opportunity validity
($0<p^{\mathrm{stop}}_o<m^{\mathrm{arr}}$, $p^{\mathrm{stop}}_o<p^{\mathrm{lim}}\le p^{\mathrm{ask}}(1+\chi)$, per-share stop loss $\ge\ell^{\min}$);
G8 no anomalies in held positions; G9 $d=+1$ (D-01); G10 $i\in\mathbb I_t$ and instrument admissible.

**Post-filter (non-monotone, never a cap):** minimum order size $n^{\min}$: $Q^{\mathrm{fin}}=Q$ if $Q\ge n^{\min}$ else $0$ (T-03 counterexample
explains why it cannot be folded into the min-of-caps).

**On correlation.** Worst-case aggregation of per-position loss bounds is the **sum**, for every dependence structure
(T-18). The hard layer therefore grants **no diversification credit**; statistical correlation estimates may only tighten budgets
(e.g. by forcing near-duplicate instruments into one cluster). A correlation-adjusted multiplier that can exceed $1$ (negative
estimated correlation) is inadmissible (FM-COR-1).

## 6. Quantity caps and $Q^{\mathrm{hard}}$ (Phase 4)

For each constraint:
$Q_k:=\max\big(\{0\}\cup\{n\in\mathbb L_{>0}:\ n\le\bar N,\ g_k(n)\le b^{\mathrm{allow}}_k\}\big)$, computed by exact monotone search over the
lattice (bisection terminates in $\lceil\log_2(\bar N/\delta_q)\rceil+1$ steps), or by an exact closed form **only** where $g_k$ is proved
linear: $g_k(n)=n\,\ell_k$, $\ell_k>0$ ⇒ $Q_k=\min\big(\bar N,\ \delta_q\lfloor b_k/(\delta_q\ell_k)\rfloor\big)$ for $b_k\ge0$.

$$
Q^{\mathrm{hard}}=\begin{cases}\min_k Q_k & \text{all gates pass}\\ 0&\text{otherwise}\end{cases}
\qquad\text{and}\qquad \Big\lfloor\min_k x_k\Big\rfloor_{\mathbb L}=\min_k\lfloor x_k\rfloor_{\mathbb L}\ \ (\text{T-03(b)}).
$$

The brief's names map as: $Q_{\mathrm{risk}}\leftrightarrow$ H1–H4, H10 (via $R^{\mathrm{allow}}$); $Q_{\mathrm{notional}}\leftrightarrow$ H7, H11;
$Q_{\mathrm{liquidity}}\leftrightarrow$ H12–H13; $Q_{\mathrm{buying\ power}}\leftrightarrow$ H14; $Q_{\mathrm{margin}}\leftrightarrow$ H15;
$Q_{\mathrm{portfolio}}\leftrightarrow$ H2, H5, H11; $Q_{\mathrm{correlation}}\leftrightarrow$ H9–H10; plus $Q_{\mathrm{gap}}\leftrightarrow$ H5–H6 and
$Q_{\mathrm{concentration}}\leftrightarrow$ H8, which the brief did not list and which §3 shows are necessary.

**Edge cases (normative handling).**

| Case | Handling | Reference |
|---|---|---|
| Integer shares | $\delta_q=1$ | D-04 |
| Fractional shares | $\delta_q=10^{-k}$; whether a protective stop can be attached to the fractional part is **UNKNOWN**; if not, that part is tier U only | D-04, RQ-25 |
| Decimal arithmetic | exact; directed rounding table | 01 §9, T-24 |
| Rounding | floor to lattice; never half-up | T-02 |
| Zero / negative loss per share | G7 rejects $p^{\mathrm{stop}}_o\ge m^{\mathrm{arr}}$ and per-share loss $<\ell^{\min}$; otherwise $Q_k$ would equal $\bar N$ | T-02 note |
| Negative budgets | clamp to $0$ ⇒ $Q_k=0$ | T-01 |
| Negative wealth | $B_t\le0$, $K_t\le0$ ⇒ all budgets $0$; RECOVERY reason | T-05 |
| NaN / Infinity | rejected at parse; never compared | 01 §9 |
| Overflow | magnitude bounds $\bar M,\bar N$; decimal Overflow trapped | 01 §9 |
| Tiny account | $R^{\mathrm{allow}}<L^{\mathrm{stop}}(\delta_q)$ ⇒ $Q=0$, reason INSUFFICIENT\_CAPITAL (correct, not an error) | T-02 |
| Huge account | liquidity/concentration caps bind; binary64 overshoot region avoided by exactness | T-22 |

## 7. Drawdown, floors and capital preservation (Phase 5)

**Definitions.** $\nu_t=W_t/U_t$; $H_t=\max_{u\in\mathcal H_t}\nu_u$ (requires $\nu_0>0$, hence $H_t>0$); $DD_t=1-\nu_t/H_t$;
$MDD_t=\max_{u\le t}DD_u$. Floors as in 02 (S-105..S-109), cushion $K_t=W_t-F_t$.

**Induced throttle.** With $F_t=F^{\mathrm{dd}}_t$, $U\equiv1$, no open risk and $B=W$:
$K_t=H_t(d^{\max}-DD_t)$, so the per-trade budget is $f^{\mathrm{trd}}W_t\,\vartheta_K(DD_t)$ with

$$
\vartheta_K(DD)=\min\Big\{1,\ \Big(\frac{m_K}{f^{\mathrm{trd}}}\cdot\frac{d^{\max}-DD}{1-DD}\Big)^{+}\Big\},\qquad
\frac{d}{dDD}\,\frac{d^{\max}-DD}{1-DD}=-\frac{1-d^{\max}}{(1-DD)^2}<0 .
$$

$\vartheta_K$ is continuous, non-increasing, equal to $1$ up to $DD^{*}=\frac{m_Kd^{\max}-f^{\mathrm{trd}}}{m_K-f^{\mathrm{trd}}}$ (when
$m_Kd^{\max}>f^{\mathrm{trd}}$), and exactly $0$ at $DD=d^{\max}$. The **aggregate** capacity $m_KH_t(d^{\max}-DD_t)$ is linear in $DD$.

**Why the cushion line, not a chosen shape.** T-21: under the disturbance set of tier S, a policy guarantees $W_{t+1}\ge F_t$ for
every admissible scenario **iff** aggregate stop-risk $\le K_t$ (sufficiency by summation, necessity by the comonotone
"all stops hit" scenario). Hence every floor-safe throttle lies pointwise below the cushion line; choosing *among* safe throttles is a
preference/performance question for Phase 16, not a safety question.

| Family | Form | Continuous | Monotone in $DD$ | Zero at $d^{\max}$ | Floor-safe alone (tier S) | Sensitivity | Path-dependent |
|---|---|---|---|---|---|---|---|
| Cushion-induced (CPPI-type) | $\vartheta_K$ above | yes | yes | yes | yes iff $m_K\le1$ with aggregate risk | bounded: $\le\frac{m_K}{f^{\mathrm{trd}}(1-d^{\max})}$ on $[0,d^{\max}]$ | no (function of $W,H$) |
| Linear in $DD$ | $(1-DD/d^{\max})^+$ | yes | yes | yes | single trade iff $f^{\mathrm{trd}}\le m_Kd^{\max}$; aggregate still needs H4 | $1/d^{\max}$ | no |
| Piecewise step | $\sum_k c_k\mathbb 1[DD\in I_k]$ | **no** | if $c_k$ non-increasing | if last $c_k=0$ | only if below cushion line pointwise | **unbounded** at steps (chattering) | no |
| Exponential | $e^{-\zeta\,DD}$ | yes | yes | **never** | **no** — cannot enforce a floor | $\zeta$ | no |
| Multiplicative per loss | e.g. halve after each loss, reset at new high | n/a | not a function of $(W,H)$ | no | no | — | **yes** (needs extra state) |
| Additive loss budget | $b-\text{loss since reset}$ | yes | yes | at exhaustion | yes (= a floor) | 1 | reset rule |

Theory support for the cushion form: Grossman & Zhou (1993) show that when wealth must never fall below a fixed fraction of its
running maximum, the optimal risky investment is proportional to the surplus over that floor (CRRA, continuous trading); with discrete trading and gaps the floor can be breached
(Balder, Brandl & Mahayni 2009), which in this architecture is exactly the role of the gap cushion H5 (multiplier $\le 1/\Gamma$). Both
sources verified bibliographically; claims about their content are from abstracts (see 11).

**Recommendation (PROVISIONAL).** No additional throttle beyond the cushion constraints in v0 (Art. 15). A separate throttle is
**UNDEFINED** until Phase-16 evidence shows a benefit.

**Sensitivity and asymmetry.** $\partial(m_KK)/\partial W=m_K$ below the HWM, but $m_Kd^{\max}$ at a new high when $F^{\mathrm{dd}}$ binds.
Consequently favourable moves raise remaining stop-risk of an untrailed long one-for-one while the cushion rises only by the
fraction $d^{\max}$. **The invariant $R^{\mathrm{open}}\le K$ is not preserved by holding under a ratcheting floor** (T-20; numeric
counterexample: $W$ 100→140, $DD$ ends at $35.4\%$ with $d^{\max}=10\%$, no new trade, no gap). Maintaining it requires a
stop-trailing or de-risking obligation executed by an authority outside the engine; the engine emits RECOVERY with the
required reduction $R^{\mathrm{open}}-K$. Profit-lock floors ($F^{\mathrm{lock}}$, slope $\eta^{\mathrm{lock}}$) have the same structure with
$d^{\max}$ replaced by $1-\eta^{\mathrm{lock}}$.

**Maximum-drawdown shutdown.** Gate G4 blocks all new risk when $DD_t\ge d^{\max}$ (T-06(a), PROVED). The *bound* $MDD\le d^{\max}$
is **DISPROVED** in general and PROVED only under A-STOP plus the external trailing obligation (T-06(b,c)).

## 8. Reservation vector emitted with a TRADE decision

For the chosen $Q=Q^{\mathrm{fin}}$: $\big(L^{\mathrm{stop}}(Q),\ L^{\mathrm{gap}}(Q),\ Q\,p^{\mathrm{lim}},\ Q\,p^{\mathrm{lim}}+\phi^{\mathrm{buy}}(Q),\ Q\big)$, tagged with
strategy $s$ and cluster $c$, all rounded up. Computed at the worst-case entry $p^{\mathrm{lim}}$, it dominates the realised open risk
of any fill $e\le Q$ at any price $\le p^{\mathrm{lim}}$ (T-11(c)). The ledger — not the engine — performs the reservation.

## 9. Policy-parameter admissibility (a validity check on $\theta$, not values)

$0<f^{\mathrm{trd}}\le f^{\mathrm{port}}$; $0<f^{\mathrm{strat}}_s\le f^{\mathrm{port}}$; $0<f^{\mathrm{clr}}\le f^{\mathrm{port}}$; $f^{\mathrm{gap}}>0$;
$0<f^{\mathrm{ord}},f^{\mathrm{conc}},f^{\mathrm{clu}}$; $0<\lambda^{\mathrm{gross}}\le1$ (D-02); $m_K,m_G\in(0,1]$ (values $>1$ admit floor breach when all stops
hit — T-21); $d^{\max},\ell^{\mathrm{day}},\ell^{\mathrm{wk}}\in(0,1)$; $\eta^{\mathrm{lock}}\in[0,1)$; $\Gamma^{\min}\in(0,1]$; $\rho^{\mathrm{in}},\rho^{\mathrm{ex}}\in(0,1]$;
$h^{\mathrm{ex}},w^{\mathrm{in}}>0$; $\varsigma^{\max}>0$; $\chi\ge0$; $\ell^{\min}>0$; $n^{\min}\in\mathbb L_{\ge0}$; $F^{\mathrm{abs}}\ge0$; $\bar N,\bar M>0$.
A $\theta$ outside this box ⇒ every decision is NO\_TRADE (reason INVALID\_POLICY). Redundant (never-binding) settings are
permitted but reported.

## 10. Normative evaluation order (specification, not code)

1. Parse; reject non-exact numeric types and special values.
2. Gate G1 (authority) — on failure NO\_TRADE with the failed validators.
3. Validity (G7–G10) and anomaly checks on held positions.
4. Derive $E,\Lambda,W,\nu,DD,F,K,B$, open-risk aggregates (directed rounding).
5. Gates G2–G6.
6. Hard budgets $b^{\mathrm{hard}}_k$; $R^{\mathrm{hard}}$, $G^{\mathrm{hard}}$.
7. Model tightening via $\mathfrak s$ and $\min$ (never `Decimal.min`).
8. $Q_k$ by exact monotone search; $Q^{\mathrm{hard}}=\min_kQ_k$.
9. Optional optimiser proposal → floor to $\mathbb L$ → clip to $[0,Q^{\mathrm{hard}}]$ → exact verification of every $g_k$.
10. Certified-advantage test (**UNDEFINED in v0.1**; if declared REQUIRED, every decision is NO\_TRADE until defined — D-10).
11. Minimum-order post-filter.
12. Emit record: decision class, $Q^{\mathrm{hard}}$, $Q^{\mathrm{fin}}$, every $Q_k$ and $b_k$, binding set, tiers guaranteed, reservation vector,
    reasons, $\mathrm h(\mathsf S_t)$, $\mathsf v$.

## 11. Unresolved objects in this document

$B_t$ (RQ-02); $\mathrm{SL}_{s,t}$ (RQ-11); cluster map (RQ-10); $\kappa^{\mathrm{out}},\Lambda$ (RQ-05); $\Gamma_i$ (RQ-04); ADV estimator (RQ-06);
$C^{\mathrm{avail}}$ (RQ-20); event policy (RQ-04); adoption of H16 (D-08); whether pre-existing open risk is charged to the daily floor (RQ-32);
all values in $\theta$ — each **UNDEFINED — REQUIRES RESOLUTION**.
