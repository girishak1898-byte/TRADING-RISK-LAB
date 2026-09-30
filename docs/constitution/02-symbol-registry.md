# 02 — Complete Symbol Registry (v0.1.1-draft)

Status: DRAFT — for human review. This registry is the **single authority for notation**. No symbol may appear in any
other document of this programme unless it is registered here. A symbol whose definition is incomplete is marked
**UNDEFINED — REQUIRES RESOLUTION** and may not be used in a safety-critical equation until resolved.

## 0. Conventions

**Source / class codes** (the brief's "deterministic or stochastic" column, made precise):

| Code | Class | Meaning | Known at decision time $\tau_t$? |
|---|---|---|---|
| P | Policy constant | Set by the human controller, versioned, never estimated by the engine | Yes (deterministic) |
| O | Observed authoritative input | Supplied by the authority boundary inside the snapshot $\mathsf S_t$ | Yes ($\mathcal F_t$-measurable); stochastic as a process |
| D | Derived | Deterministic function of O and P (and of earlier D carried as state) | Yes ($\mathcal F_t$-measurable) |
| E | Estimate / proxy | Deterministic statistic of admissible historical data that stands in for an *unknown* quantity; carries estimation and model error | Yes as a number; its *meaning* is uncertain |
| R | Random / future | Realised only in $(\tau_t,\tau_{t+1}]$; not $\mathcal F_t$-measurable | No |
| M | Model object | Mathematical construct (measure, σ-algebra, functional) — not data | n/a |

**Sign conventions (global).**
- Quantities: $q>0$ long, $q<0$ short. Fill quantity $n_j>0$ buy, $n_j<0$ sell.
- Cash flows into the account are positive.
- **Loss, cost, consumption and risk quantities are non-negative numbers where larger = worse** (loss-positive convention). P&L quantities are profit-positive.
- Direction $d\in\{+1,-1\}$ multiplies prices so that $d\,(x-y)>0$ means "adverse for the position" only where stated.

**Units.** $[\mathrm{USD}]$ money; $[\mathrm{sh}_i]$ shares of instrument $i$ (shares of different instruments are **not**
commensurable — see 03); $[\mathrm{T}]$ time; $[\mathrm{day}]$ trading day; $[\mathrm{unit}]$ fund unit; $[1]$ dimensionless.

**Number types.** $\mathbb Q$ = exact rational (finite decimals are a subset); $\mathbb L=\delta_q\mathbb Z$ = quantity lattice;
$\mathbb L_{\ge 0}$ its non-negative part. "Exact" means representable without rounding (see 01 §9).

**Collision avoidance.** The brief's no-trade action "$a_0$" is written $a^{\varnothing}$ (because $a_0$ is the action at epoch 0).
Tail confidence level is $\beta$ (because $\alpha_t$ is the authority indicator). Spread is $\varsigma$ (because $s$ indexes strategies).
Throttle is $\vartheta$ (because $\theta$ is the policy-parameter vector).

---

## A. Index sets, time, lattice

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-001 | $t$ | Decision epoch index | integer | — | $\mathbb N_0$ | [1] | — | $t\le T_H$ | snapshot sequence number | O |
| S-002 | $\tau_t$ | Wall-clock instant of epoch $t$ | timestamp | $\mathbb T$ | UTC instants (integer ns) | [T] | — | strictly increasing in $t$ | authority clock recorded in $\mathsf S_t$ | O |
| S-003 | $\mathbb I_t$ | Instrument universe admissible at $t$ | finite set | $\mathbb T$ | finite sets of instrument IDs | — | — | as-of $\tau_t$ (no survivorship) | versioned reference data | O |
| S-004 | $N_t$ | Cardinality of $\mathbb I_t$ | integer | $\mathbb T$ | $\mathbb N_0$ | [1] | — | $\ge 0$ | derived | D |
| S-005 | $\mathbb S$ | Strategy identifiers | finite set | — | IDs | — | — | non-empty if any trade | policy | P |
| S-006 | $\mathbb C,\ \mathrm{cl}$ | Cluster set and map $\mathrm{cl}:\mathbb I\to\mathbb C$ ("correlation groups") | set, function | $\mathbb I$ | $\mathbb C$ | — | — | total map; versioned | policy — **construction method UNDEFINED — REQUIRES RESOLUTION** (RQ-10) | P |
| S-007 | $\delta_q$ | Quantity lattice step | rational | — | $\mathbb Q_{>0}$ | [sh] | + | $1$ (whole shares) or $10^{-k}$ — **UNDEFINED — REQUIRES RESOLUTION** (D-04) | policy | P |
| S-008 | $\mathbb L$ | Quantity lattice $\delta_q\mathbb Z$ | set | — | — | [sh] | — | — | derived from $\delta_q$ | D |
| S-009 | $\bar N$ | Maximum admissible order quantity (representation/sanity bound) | rational | — | $\mathbb L_{>0}$ | [sh] | + | value **UNDEFINED — REQUIRES RESOLUTION** | policy | P |
| S-010 | $\bar M$ | Maximum admissible magnitude of any monetary quantity | rational | — | $\mathbb Q_{>0}$ | [USD] | + | value **UNDEFINED — REQUIRES RESOLUTION** | policy | P |
| S-011 | $h$ | Intended holding horizon of an opportunity | duration | opportunities | $\mathbb Q_{>0}$ | [T] | + | horizon classes (intraday / overnight / multi-day) **UNDEFINED — REQUIRES RESOLUTION** (D-09) | opportunity | O |

## B. Authority and provenance

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-020 | $\mathsf S_t$ | Authoritative immutable snapshot (consistent cut) | record (canonical bytes + schema id) | $\mathbb T$ | $\mathfrak S$ (schema-valid snapshots) | — | — | schema-valid, hash-identified | authority boundary (external to engine) | O |
| S-021 | $\mathrm h(\cdot)$ | Content hash over canonical serialisation | function | byte strings | $\{0,1\}^{256}$ | — | — | SHA-256 (PROVISIONAL) | derived | D |
| S-022 | $A_{\mathrm{id}}$ | Account/scope identifier bound into $\mathsf S_t$ | identifier | $\mathbb T$ | IDs | — | — | must equal the scope the decision is requested for; **binding proof method UNDEFINED — REQUIRES RESOLUTION** (integration phase) | authority boundary | O |
| S-023 | $t^{\mathrm{know}}(\mathsf d)$ | Knowledge time of datum $\mathsf d$ (bitemporal) | timestamp | data items | UTC | [T] | — | $\le\tau_t$ for admission to $\mathsf S_t$ | data provenance metadata | O |
| S-024 | $\mathrm{age}_t(\mathsf d)$ | $\tau_t-t^{\mathrm{know}}(\mathsf d)$ | duration | data items | $\mathbb Q_{\ge0}$ | [T] | + | $\le \mathrm{TTL}_{\mathsf d}$ | derived | D |
| S-025 | $\mathrm{TTL}_{\mathsf d}$ | Maximum admissible age per datum class | duration | datum classes | $\mathbb Q_{>0}$ | [T] | + | values **UNDEFINED — REQUIRES RESOLUTION** (RQ-19) | policy | P |
| S-026 | $\mathcal R^{\mathrm{req}}$ | Required-input registry: finite set of (field path, validator) | finite set | — | — | — | — | completeness **NOT YET PROVEN** (T-04) | policy (versioned) | P |
| S-027 | $\alpha_t$ | Authority indicator: $1$ iff every validator in $\mathcal R^{\mathrm{req}}$ passes on $\mathsf S_t$ | boolean | $\mathfrak S$ | $\{0,1\}$ | [1] | — | — | derived | D |
| S-028 | $\mathsf v$ | Version tuple (constitution, formula, parameter set, schema, code) | tuple of IDs | — | — | — | — | all present and known | policy/build | P |

## C. Portfolio and accounting state

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-030 | $C_t$ | Cash ledger balance | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + asset | cash account: $C_t\ge 0$ (D-02); $\lvert C_t\rvert\le\bar M$ | authoritative ledger | O |
| S-031 | $C^{\mathrm{set}}_t,\ C^{\mathrm{uns}}_t$ | Settled / unsettled cash | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + asset | $C=C^{\mathrm{set}}+C^{\mathrm{uns}}$; **settlement semantics UNDEFINED — REQUIRES RESOLUTION** (RQ-20) | authoritative ledger | O |
| S-032 | $q_{i,t}$ | Position quantity | lattice | $\mathbb T\times\mathbb I$ | $\mathbb L$ | [sh$_i$] | + long / − short | v0: $q\ge 0$ (D-01) | authoritative positions | O |
| S-033 | $\bar c_{i,t}$ | Cost basis per share (attribution only) | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{\ge0}$ | [USD/sh$_i$] | — | method (FIFO/average) **UNDEFINED — REQUIRES RESOLUTION**; not safety-relevant | ledger | O |
| S-034 | $p^{\mathrm{stop}}_{i,t}$ | Protective stop trigger price of the open position | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{>0}\cup\{\bot\}$ | [USD/sh$_i$] | — | long: $p^{\mathrm{stop}}<m_{i,t}$ else ANOMALY; $\bot$ = no stop ⇒ treated per D-06 (never as zero risk) | authoritative order state | O |
| S-035 | $Y_t$ | Accrued liabilities (fees payable, interest, borrow); $Y_{t+1}=Y_t+\mathrm{Accr}_{t+1}-\mathrm{Pay}_{t+1}$ | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + owed | $\le\bar M$ | ledger | O |
| S-036 | $X_{t+1}$ | Net external capital flow during $(\tau_t,\tau_{t+1}]$ | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + deposit / − withdrawal | — | ledger | R (O once realised) |
| S-037 | $\mathrm{Inc}_{t+1}$ | Income credited (dividends, interest) | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | — | ledger | R |
| S-038 | $\mathrm{Fin}_{t+1}$ | Financing / borrow charges debited | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + cost | v0: $0$ if no margin/short (D-01, D-02) | ledger | R |
| S-039 | $U_t$ | Fund units outstanding (unitisation for flow-neutral performance) | scalar | $\mathbb T$ | $\mathbb Q_{>0}$ | [unit] | + | changes only on external flows | unitisation ledger | D |
| S-040 | $E_t$ | Mark-to-market equity $C_t+\sum_i q_{i,t}m_{i,t}-Y_t$ | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + | any sign | derived | D |
| S-041 | $\Lambda_{i,t},\ \Lambda_t$ | Modelled cost to liquidate holding $i$ from current mark; $\Lambda_t:=\sum_i\Lambda_{i,t}$ (A-ACC-04) | scalar | $\mathbb T(\times\mathbb I)$ | $\mathbb Q_{\ge0}$ | [USD] | + cost | model **UNDEFINED — REQUIRES RESOLUTION** (RQ-05) | model | E/M |
| S-042 | $W_t$ | Net liquidation wealth $E_t-\Lambda_t$ | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + | any sign (negative ⇒ all budgets 0) | derived | D (conditional on $\Lambda$) |
| S-043 | $\nu_t$ | NAV per unit $W_t/U_t$ | scalar | $\mathbb T$ | $\mathbb Q$ | [USD/unit] | + | — | derived | D |
| S-044 | $\Pi^{R}_t,\ \Pi^{U}_t$ | Cumulative realised / unrealised P&L | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + profit | attribution only — **never an input to authority** (DC-4) | derived | D |
| S-045 | $\mathrm{Accr}_{t+1}$ | Liabilities accrued during the period (not already in $\phi_j$ or $\mathrm{Fin}$) | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + owed | floor theorems assume $0$ | ledger | R |
| S-046 | $\mathrm{Pay}_{t+1}$ | Cash payments of previously accrued liabilities | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + outflow | $\le Y_t+\mathrm{Accr}_{t+1}$ | ledger | R |

## D. Market state

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-050 | $p^{\mathrm{bid}}_{i,t},\ p^{\mathrm{ask}}_{i,t}$ | Best bid / ask (consolidated) | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{>0}$ | [USD/sh$_i$] | — | $0<p^{\mathrm{bid}}<p^{\mathrm{ask}}$; locked/crossed ⇒ invalid | market data in $\mathsf S_t$ | O |
| S-051 | $m_{i,t}$ | Mid $\tfrac12(p^{\mathrm{bid}}+p^{\mathrm{ask}})$ | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{>0}$ | [USD/sh$_i$] | — | — | derived | D |
| S-052 | $\varsigma_{i,t}$ | Quoted spread $p^{\mathrm{ask}}-p^{\mathrm{bid}}$ | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{>0}$ | [USD/sh$_i$] | + cost | $>0$ | derived | D |
| S-053 | $m^{\mathrm{arr}}$ | Arrival mid of the opportunity's instrument at $\tau_t$ | scalar | opportunities | $\mathbb Q_{>0}$ | [USD/sh$_i$] | — | $=m_{i,t}$ | derived | D |
| S-054 | $\mathrm{ADV}_{i,t}$ | Trailing average daily volume | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{>0}$ | [sh$_i$/day] | + | window/estimator **UNDEFINED — REQUIRES RESOLUTION**; proxy for future liquidity (A-LIQ) | deterministic statistic of admissible volume history | E |
| S-055 | $\hat\sigma_{i,t}$ | Volatility estimate of mid log-returns | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{\ge0}$ | [day$^{-1/2}$] | + | estimator **UNDEFINED** | statistic | E |
| S-056 | $\hat\Sigma_t,\ \hat\rho_{ij,t}$ | Covariance / correlation estimates | matrix | $\mathbb T$ | PSD matrices; $[-1,1]$ | [day$^{-1}$]; [1] | — | model layer only (Art. 6) | statistic | E |
| S-057 | $\mathrm{st}_{i,t}$ | Trading status | enum | $\mathbb T\times\mathbb I$ | {TRADING, HALTED, LULD\_PAUSE, UNKNOWN} | — | — | only TRADING admits new risk | market data | O |
| S-058 | $\mathrm{ev}_{i,t}$ | Scheduled-event flag within the holding horizon (e.g. earnings) | enum | $\mathbb T\times\mathbb I$ | {NONE, EVENT, UNKNOWN} | — | — | **source UNDEFINED — REQUIRES RESOLUTION** (RQ-04) | reference data | O |
| S-059 | $r_{i,t+1}$ | Simple mid return $m_{i,t+1}/m_{i,t}-1$ | scalar | $\mathbb T\times\mathbb I$ | $[-1,\infty)$ | [1] | + gain | $\ge -1$ (A-MKT-01) | market | R |

## E. Opportunity and action

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-060 | $o$ | Opportunity $(i,d,p^{\mathrm{lim}},p^{\mathrm{stop}}_o,p^{\mathrm{tgt}},s,h,\mathrm{id})$ | record | — | — | — | — | all fields present & valid | strategy (not an authority on portfolio state) | O |
| S-061 | $d$ | Direction | enum | opportunities | $\{+1,-1\}$ | [1] | +1 buy-to-open long | v0: $+1$ only (D-01) | opportunity | O |
| S-062 | $p^{\mathrm{lim}}$ | Entry limit price = worst admissible entry fill | scalar | opportunities | $\mathbb Q_{>0}$ | [USD/sh$_i$] | — | long: $p^{\mathrm{stop}}_o<p^{\mathrm{lim}}\le p^{\mathrm{ask}}(1+\chi)$; collar $\chi$ **UNDEFINED — REQUIRES RESOLUTION**; absence ⇒ invalid (D-05) | opportunity | O |
| S-063 | $p^{\mathrm{stop}}_o$ | Stop trigger price for the new position | scalar | opportunities | $\mathbb Q_{>0}$ | [USD/sh$_i$] | — | long: $0<p^{\mathrm{stop}}_o<m^{\mathrm{arr}}$ | opportunity | O |
| S-064 | $p^{\mathrm{tgt}}$ | Target price | scalar | opportunities | $\mathbb Q_{>0}$ | [USD/sh$_i$] | — | **forbidden in the hard layer** (Art. 6); model layer only | opportunity | O |
| S-065 | $n$ | Candidate increment quantity for $o$ | lattice | — | $\mathbb L_{\ge0}$ | [sh$_i$] | + | $\le\bar N$ | decision variable | D |
| S-066 | $a_t$ | Action: signed quantity-change vector | vector | $\mathbb T$ | $\mathbb L^{N_t}$ | [sh$_i$] per component | + buy | — | decision output | D |
| S-067 | $\omega_t$ | Order parameters attached to $a_t$ (limit, stop, TIF) | record | $\mathbb T$ | — | mixed | — | — | decision output | D |
| S-068 | $a^{\varnothing}$ | No-trade action $0\in\mathbb L^{N_t}$ (brief's $a_0$) | vector | — | $\{0\}$ | [sh] | — | always admissible as a *decision* (Art. 2) | — | D |
| S-069 | $\mathcal A^{+},\mathcal A^{-},\mathcal A^{h}$ | Risk-increasing / risk-reducing / hold action classes | sets | states | subsets of $\mathbb L^{N}$ | — | — | partition of $\mathbb L^N$ given $q_t$ (01 §3.4) | derived | D |
| S-070 | $\mathcal A^{\mathrm{safe}}(x_t)$ | Safe risk-increasing action set | set | states | subsets of $\mathcal A^{+}$ | — | — | may be $\varnothing$ ⇒ NO TRADE / RECOVERY | derived | D |
| S-071 | $e$ | Executed quantity of an order for $n$ | lattice | orders | $\mathbb L_{\ge0}$ | [sh$_i$] | + | $0\le e\le n$ (A-EXE-03) | execution | R |

## F. Execution, costs, scenario losses

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-080 | $\mathcal J_{t+1}$ | Set of fills in $(\tau_t,\tau_{t+1}]$ | finite set | $\mathbb T$ | — | — | — | — | execution reports | R |
| S-081 | $n_j, f_j, \phi_j, \tau_j, i(j)$ | Fill signed quantity, price, fee, time, instrument | tuple | $\mathcal J$ | $\mathbb L\setminus\{0\},\mathbb Q_{>0},\mathbb Q_{\ge0},\mathbb T,\mathbb I$ | [sh],[USD/sh],[USD],[T],— | $n_j>0$ buy; $\phi_j\ge0$ cost | — | execution reports | R |
| S-082 | $\pi^{\mathrm{ref}}_j$ | Reference price for cost decomposition of fill $j$ | scalar | $\mathcal J$ | $\mathbb Q_{>0}$ | [USD/sh] | — | convention fixed per fill type (05 §3) | derived | D |
| S-083 | $c_{j,k}$ | $k$-th execution-cost component of fill $j$ | scalar | $\mathcal J\times\mathbb N$ | $\mathbb Q$ | [USD] | + cost | may be negative (price improvement) | derived ex post | D |
| S-084 | $\phi^{\mathrm{buy}}_i(n),\ \phi^{\mathrm{sell}}_i(n)$ | Fee schedule (commission + regulatory + venue) for an order of size $n$; $\phi^{\mathrm{sell}}_{i,0}(n)$ denotes the sell fee evaluated at price $0$ (used in $L^{\mathrm{abs}}$, $u^{\mathrm{open}}$) | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD] | + cost | $\phi(0)=0$, non-decreasing (A-EXE-01); schedule values **UNDEFINED — REQUIRES RESOLUTION** | versioned fee schedule | P/O |
| S-085 | $\kappa^{\mathrm{out}}_i(n)$ | Modelled per-share exit cost below the stop trigger under *normal* stop execution | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD/sh$_i$] | + cost | non-decreasing in $n$; model **UNDEFINED — REQUIRES RESOLUTION** (RQ-05) | model | E/M |
| S-086 | $\kappa^{\mathrm{liq}}_i(n)$ | Modelled per-share cost to liquidate from current mid | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD/sh$_i$] | + cost | $\ge\varsigma/2$ | model | E/M |
| S-087 | $\iota_i(n)$ | Ex-ante expected market impact per share | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD/sh$_i$] | + cost | model layer only; **UNDEFINED** | model | M |
| S-088 | $\Gamma_i$ | Gap-stress fraction: triggered-stop exits fill at $\ge(1-\Gamma_i)\,p^{\mathrm{stop}}$ | scalar | $\mathbb I$ (× horizon class) | $(0,1]$ | [1] | + worse | $\Gamma_i=\max(\Gamma^{\min},\hat\Gamma_i)$ (Art. 6); values **UNDEFINED — REQUIRES RESOLUTION** (RQ-04) | policy floor ∨ estimate | P∨E |
| S-089 | $\gamma_j$ | Realised gap/slippage beyond stop for stop-exit fill $j$ (long: $p^{\mathrm{stop}}-f_j$) | scalar | stop fills | $\mathbb Q$ | [USD/sh] | + adverse | — | execution | R |
| S-090 | $L^{\mathrm{stop}}(n)$ | Ex-ante loss bound of new entry if stop executes normally: $n(p^{\mathrm{lim}}-p^{\mathrm{stop}}_o+\kappa^{\mathrm{out}}(n))+\phi^{\mathrm{buy}}(n)+\phi^{\mathrm{sell}}(n)$ | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD] | + loss | conditional on A-STOP, A-TRIG, A-MKT-05 | derived | D |
| S-091 | $L^{\mathrm{gap}}(n)$ | $n(p^{\mathrm{lim}}-p^{\mathrm{gx}}(n))+\phi^{\mathrm{buy}}(n)+\phi^{\mathrm{sell}}(n)$ with $p^{\mathrm{gx}}(n)=\min((1-\Gamma_i)p^{\mathrm{stop}}_o,\ p^{\mathrm{stop}}_o-\kappa^{\mathrm{out}}(n))$ | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD] | + loss | conditional on A-GAP | derived | D |
| S-092 | $L^{\mathrm{abs}}(n)$ | $n\,p^{\mathrm{lim}}+\phi^{\mathrm{buy}}(n)+\phi^{\mathrm{sell}}_{0}(n)$ (price → 0) | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD] | + loss | long only; unconditional given A-MKT-01/05 | derived | D |
| S-093 | $\ell^{\mathrm{stop}}$ | Per-share stop loss when $L^{\mathrm{stop}}$ is linear | scalar | — | $\mathbb Q_{>0}$ | [USD/sh$_i$] | + loss | $\ge\ell^{\min}>0$ else INVALID | derived | D |
| S-094 | $\mathrm{ER}(n)$ | Execution-assumption risk increment $L^{\mathrm{gap}}(n)-L^{\mathrm{stop}}(n)$ | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge 0}$ (always, by the $\min$ in $p^{\mathrm{gx}}$) | [USD] | + | — | derived | D |
| S-095 | $r^{\mathrm{open}}_{i,t},\ g^{\mathrm{open}}_{i,t},\ u^{\mathrm{open}}_{i,t}$ | Open stop / gap / absolute risk of held position $i$ (05 §5; **no $\Lambda$ credit** — OC-1) | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{\ge0}$ | [USD] | + loss | negative raw value ⇒ ANOMALY (not "free budget") | derived | D |
| S-096 | $R^{\mathrm{open}}_t,\ G^{\mathrm{open}}_t,\ Z^{\mathrm{open}}_t,\ N^{\mathrm{open}}_t$ | Aggregates $\sum_i r^{\mathrm{open}}_i$, $\sum_i g^{\mathrm{open}}_i$, $\sum_i u^{\mathrm{open}}_i$, $\sum_i\lvert q_i\rvert m_i$; restrictions to strategy $s$ / cluster $c$ written $R^{\mathrm{open}}_{s,t}$, $R^{\mathrm{open}}_{c,t}$ | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | — | derived | D |
| S-097 | $R^{\mathrm{res}}_t,\ G^{\mathrm{res}}_t,\ Z^{\mathrm{res}}_t,\ N^{\mathrm{res}}_t,\ C^{\mathrm{res}}_t,\ Q^{\mathrm{res}}_{i,t}$ | Reserved (pending-order) stop-risk, gap-risk, absolute risk ($L^{\mathrm{abs}}$ incl. fees), notional, cash, and share quantity; restrictions to instrument $i$ / strategy $s$ / cluster $c$ written with that subscript (e.g. $N^{\mathrm{res}}_{i,t}$, $R^{\mathrm{res}}_{c,t}$) | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | computed at worst-case entry ($p^{\mathrm{lim}}$) | authoritative reservation ledger | O |

## G. Capital, floors, drawdown, budgets

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-100 | $B_t$ | Risk base multiplying policy fractions | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + | **UNDEFINED — REQUIRES RESOLUTION** (candidates in 06 §4; RQ-02) | derived | D |
| S-101 | $H_t$ | High-water mark of $\nu$: $\max_{u\in\mathcal H_t}\nu_u$ | scalar | $\mathbb T$ | $\mathbb Q_{>0}$ | [USD/unit] | + | observation set $\mathcal H_t$ (EOD vs intraday) **UNDEFINED — REQUIRES RESOLUTION** (RQ-03) | state carried in $\mathsf S_t$ | D |
| S-102 | $DD_t$ | Drawdown $1-\nu_t/H_t$ | scalar | $\mathbb T$ | $[0,\infty)$ | [1] | + worse | requires $H_t>0$; $DD_t\ge1\iff\nu_t\le0$ | derived | D |
| S-103 | $MDD_t$ | Maximum drawdown $\max_{u\le t}DD_u$ | scalar | $\mathbb T$ | $[0,\infty)$ | [1] | + worse | — | derived | D |
| S-104 | $\nu^{\mathrm{day}}_0,\ \nu^{\mathrm{wk}}_0$ | NAV/unit at start of trading day / week | scalar | $\mathbb T$ | $\mathbb Q$ | [USD/unit] | — | calendar boundaries **UNDEFINED — REQUIRES RESOLUTION** (RQ-31) | state | D |
| S-105 | $F^{\mathrm{abs}}$ | Absolute capital floor | scalar | — | $\mathbb Q_{\ge0}$ | [USD] | — | value **UNDEFINED — REQUIRES RESOLUTION** | policy | P |
| S-106 | $F^{\mathrm{dd}}_t$ | Drawdown floor $(1-d^{\max})H_tU_t$ | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | — | — | derived | D |
| S-107 | $F^{\mathrm{day}}_t,\ F^{\mathrm{wk}}_t$ | $(1-\ell^{\mathrm{day}})\nu^{\mathrm{day}}_0U_t$, $(1-\ell^{\mathrm{wk}})\nu^{\mathrm{wk}}_0U_t$ | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | — | — | derived | D |
| S-108 | $F^{\mathrm{lock}}_t$ | Profit-lock floor $U_t\big(\nu^{\mathrm{ref}}+\eta^{\mathrm{lock}}(H_t-\nu^{\mathrm{ref}})^+\big)$ | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | — | $\nu^{\mathrm{ref}}$ **UNDEFINED — REQUIRES RESOLUTION** | derived | D |
| S-109 | $F_t$ | Effective floor $\max(F^{\mathrm{abs}},F^{\mathrm{dd}}_t,F^{\mathrm{day}}_t,F^{\mathrm{wk}}_t,F^{\mathrm{lock}}_t)$ | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | — | — | derived | D |
| S-110 | $K_t$ | Cushion $W_t-F_t$ | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + room | $K_t\le0$ ⇒ no risk increase | derived | D |
| S-111 | $\vartheta$ | Throttle function (multiplier on a base budget) | function | states | $[0,1]$ | [1] | — | induced form in 06 §7; separate throttle **UNDEFINED** | derived/policy | D/P |
| S-112 | $\theta$ | Policy-parameter vector: $f^{\mathrm{trd}},f^{\mathrm{port}},f^{\mathrm{strat}}_s,f^{\mathrm{gap}},f^{\mathrm{ord}},f^{\mathrm{conc}},f^{\mathrm{clu}},f^{\mathrm{clr}},\lambda^{\mathrm{gross}},\rho^{\mathrm{in}},w^{\mathrm{in}},\rho^{\mathrm{ex}},h^{\mathrm{ex}},\varsigma^{\max},\ell^{\mathrm{day}},\ell^{\mathrm{wk}},d^{\max},\eta^{\mathrm{lock}},m_K,m_G,n^{\min},\chi,\Gamma^{\min},\ell^{\min}$ | vector | — | admissible box (06 §9) | mixed | + | **all values UNDEFINED — REQUIRES RESOLUTION** (human policy; never fitted on test data) | policy | P |
| S-113 | $g_k(x,n),\ b_k(x)$ | Consumption and remaining budget of hard constraint $k$ | function, scalar | states × $\mathbb L_{\ge0}$ | $\mathbb Q$ | per constraint | + | $g_k(x,0)=0$, $g_k$ non-decreasing in $n$ (required) | derived | D |
| S-114 | $Q_k$ | Cap from constraint $k$: $\max(\{0\}\cup\{n\in\mathbb L_{>0},n\le\bar N:g_k(n)\le b_k\})$ | lattice | constraints | $\mathbb L_{\ge0}$ | [sh$_i$] | + | — | derived | D |
| S-115 | $Q^{\mathrm{hard}}$ | $\min_k Q_k$ if all gates pass, else $0$ | lattice | — | $\mathbb L_{\ge0}$ | [sh$_i$] | + | — | derived | D |
| S-116 | $Q^{\mathrm{fin}}$ | Final maximum quantity after model tightening, verification, advantage test, minimum-order filter | lattice | — | $\mathbb L_{\ge0}$ | [sh$_i$] | + | $0\le Q^{\mathrm{fin}}\le Q^{\mathrm{hard}}$ (T-03) | derived | D |
| S-117 | $R^{\mathrm{hard}}_t$ | Hard stop-risk budget for the decision (scalar) | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | 06 §4 | derived | D |
| S-118 | $G^{\mathrm{hard}}_t$ | Hard gap-risk budget | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | 06 §4 | derived | D |
| S-119 | $R^{\mathrm{mod}}_t$ | Model-layer proposed budget (may be absent/invalid) | scalar | $\mathbb T$ | $\mathbb R\cup\{\text{invalid}\}$ | [USD] | + | sanitised by $\mathfrak s$ | model | E |
| S-120 | $\mathfrak s$ | Sanitiser: finite $\ge0$ ↦ itself; finite $<0$ ↦ 0; invalid ↦ 0 (REQUIRED model) or "no constraint" (OPTIONAL model) | function | $\mathbb R\cup\{\text{invalid}\}$ | $[0,\infty]$ | [USD] | — | per-model REQUIRED/OPTIONAL flag is policy | derived | D |
| S-121 | $R^{\mathrm{allow}}_t$ | $\min(R^{\mathrm{hard}}_t,\mathfrak s(R^{\mathrm{mod}}_t))$ | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | $0\le R^{\mathrm{allow}}\le R^{\mathrm{hard}}$ (T-01) | derived | D |
| S-122 | $BP_t$ | Broker-reported buying power | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + | authority for *broker acceptance* only | authority boundary | O |
| S-123 | $BP^{\mathrm{avail}}_t$ | $\min(BP_t,\ C^{\mathrm{avail}}_t)-C^{\mathrm{res}}_t$ | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + | $C^{\mathrm{avail}}$ **UNDEFINED — REQUIRES RESOLUTION** (RQ-20) | derived | D |
| S-124 | $IM_t,\ MM_t$ | Initial / maintenance margin requirement | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | out of v0 scope (D-02): **UNDEFINED — REQUIRES RESOLUTION** | authority boundary | O |

## H. Probability, statistics, objectives

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-130 | $(\Omega,\mathcal F,\mathbb P)$ | Probability space; $\mathbb P$ unknown | measure space | — | — | — | — | existence is postulate A-STAT-00 | — | M |
| S-131 | $\mathbb F=(\mathcal F_t)$ | Decision filtration $\mathcal F_t=\sigma(\mathsf S_0,\dots,\mathsf S_t)$ | filtration | $\mathbb T$ | sub-σ-algebras | — | — | — | — | M |
| S-132 | $\mathbb G=(\mathcal G_t)$ | Full market filtration, $\mathcal F_t\subseteq\mathcal G_t$ | filtration | $\mathbb T$ | sub-σ-algebras | — | — | — | — | M |
| S-133 | $\xi_{t+1}$ | Exogenous randomness on $(\tau_t,\tau_{t+1}]$: quote/trade paths, halts, fill outcomes | random element | $\Omega$ | path space $\Xi$ | — | — | — | — | R |
| S-134 | $\mathcal P_t$ | Ambiguity set of conditional laws of $\xi_{t+1}$ given $\mathcal F_t$ | set of measures | $\mathbb T$ | subsets of $\mathcal M_1(\Xi)$ | — | — | $\mathcal F_t$-measurable; construction **UNDEFINED — REQUIRES RESOLUTION** (RQ-12) | model | E |
| S-135 | $z_t,\ \mathcal Z,\ \hat\pi_t$ | Latent regime, regime set, regime posterior | random / set / vector | $\mathbb T$ | $\mathcal Z$; simplex | — | — | **UNDEFINED — REQUIRES RESOLUTION** | model | R/M/E |
| S-136 | $\mathcal L_{t+1}(a)$ | One-period flow-adjusted loss $W_t+X_{t+1}-W_{t+1}(a)$ | random scalar | actions | $\mathbb R$ | [USD] | + loss | — | derived from $G$ (05) | R |
| S-137 | $\beta$ | Tail confidence level | scalar | — | $(0,1)$ | [1] | — | value **UNDEFINED — REQUIRES RESOLUTION** | policy | P |
| S-138 | $\mathrm{VaR}_\beta,\ \mathrm{ES}_\beta$ | Value-at-Risk, Expected Shortfall of a loss | functional | laws of losses | $\mathbb R\cup\{+\infty\}$ | [USD] | + loss | 01 §5 | — | M |
| S-139 | $PB_t(a)$ | Floor-breach probability $\mathbb P(W_{t+1}(a)<F_t\mid\mathcal F_t)$ | scalar | actions | $[0,1]$ | [1] | + worse | — | model | E |
| S-140 | $\mathrm{PoR}_{h}$ | Probability of ruin over horizon $h$ | scalar | — | $[0,1]$ | [1] | + worse | definition of "ruin" (floor breach vs $W\le0$) **UNDEFINED — REQUIRES RESOLUTION** (RQ-30) | model | E |
| S-141 | $\mathrm{DaR}_\beta,\ \mathrm{CDaR}_\beta$ | Drawdown-at-risk, conditional drawdown-at-risk | functional | path laws | $[0,\infty]$ | [1] | + worse | estimation **UNDEFINED** | — | M |
| S-142 | $\epsilon^{\mathrm{ruin}}$ | Tolerated ruin / floor-breach probability | scalar | — | $(0,1)$ | [1] | — | **UNDEFINED — REQUIRES RESOLUTION** | policy | P |
| S-143 | $J_t(a)$ | Optimisation objective | functional | actions | $\mathbb R\cup\{-\infty\}$ | per candidate | + better | **UNDEFINED — REQUIRES RESOLUTION** (RQ-13) | — | M |
| S-144 | $\Delta J_t(a)$ | $J_t(a)-J_t(a^{\varnothing})$ | functional | actions | $\mathbb R\cup\{\pm\infty\}$ | as $J$ | + better | — | — | D |
| S-145 | $\mathrm{LB}_t(a)$ | Certified lower bound on $\Delta J_t(a)$ | scalar | actions | $\mathbb R\cup\{-\infty\}$ | as $J$ | + | construction **UNDEFINED — REQUIRES RESOLUTION** (RQ-14) | derived | D/E |
| S-146 | $\varepsilon^{\mathrm{num}},\varepsilon^{\mathrm{stat}},\varepsilon^{\min},\delta$ | Numerical allowance, statistical allowance, policy margin, confidence parameter | scalars | — | $\mathbb Q_{\ge0}$; $(0,1)$ | as $J$; [1] | — | **UNDEFINED — REQUIRES RESOLUTION** | derived/policy | D/P |
| S-147 | $\hat J_t$ | Numerical estimate of $J_t$ | scalar | actions | $\mathbb R$ | as $J$ | — | — | computation | E |

## I. Decision objects

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-150 | $x_t$ | State vector $(x^{A}_t,x^{P}_t,x^{M}_t,x^{H}_t,x^{B}_t,x^{U}_t)$ — see 01 §3.3 | tuple | $\mathbb T$ | product space | mixed | — | — | $\mathsf S_t$ | O/D/E |
| S-151 | $\mathcal D$ | Decision function $\mathfrak S\times\mathcal O\times\Theta\times\mathcal V\to\mathfrak D$ | function | inputs | decision records | — | — | pure, total (Art. 8, 18) | engine | D |
| S-152 | $\mathsf{RD}_t$ | Risk-decision record | record | — | $\mathfrak D$ | — | — | schema **UNDEFINED — REQUIRES RESOLUTION** (Phase 19) | engine | D |
| S-153 | $\mathsf{rc}$ | Reason codes for NO\_TRADE / RECOVERY | enum set | — | — | — | — | list **UNDEFINED — REQUIRES RESOLUTION** | engine | D |

## J. Auxiliary and derived-notation symbols

| ID | Symbol | Meaning | Where used | Class |
|---|---|---|---|---|
| S-160 | $\mathbf 1_i$ | Unit vector of instrument $i$ in $\mathbb L^{N_t}$ (so a single-opportunity action is $d\,n\,\mathbf 1_i$) | 01, 06 | D |
| S-161 | $\mathcal A_\ell$, $\ell=0..5$ | Action set admitted by authority layers $0..\ell$ (Art. 1) | 01 | D |
| S-162 | $\mathcal K$ | Index set of hard constraints H1–H16 | 01, 06, 08 | P |
| S-163 | $\mathrm{Gates}$ | Set of zero–one gates G1–G11 | 01, 06 | P |
| S-164 | $b^{\mathrm{hard}}_k,\ b^{\mathrm{mod}}_k,\ b^{\mathrm{allow}}_k$ | Hard, model-proposed, and allowed budget of constraint $k$; $b^{\mathrm{allow}}_k=\min(b^{\mathrm{hard}}_k,\mathfrak s(b^{\mathrm{mod}}_k))$ | 06, 08 | D/E/D |
| S-165 | $\mathrm{SL}_{s,t}$ | Strategy realised-loss term charged against the strategy budget — **UNDEFINED — REQUIRES RESOLUTION** (RQ-11) | 06 | D |
| S-166 | $C^{\mathrm{avail}}_t$ | Cash available for new purchases under settlement rules — **UNDEFINED — REQUIRES RESOLUTION** (RQ-20) | 02, 06 | D |
| S-167 | $\mathcal H_t$ | Set of epochs whose NAV is eligible for the high-water mark (EOD vs intraday) — **UNDEFINED** (RQ-03) | 02, 06 | P |
| S-168 | $\vartheta_K,\ DD^{*}$ | Throttle induced by the cushion constraint; drawdown at which it first falls below 1 | 06 | D |
| S-169 | $\zeta$ | Decay rate of the exponential throttle family (comparison only) | 06 | P |
| S-170 | $\mathcal M_{t+1}$ | Market ("paper") component in ECAI | 05 | R |
| S-171 | $r_{j,k}$ | $k$-th reference price in the cost-decomposition chain of fill $j$ ($r_{j,0}=\pi^{\mathrm{ref}}_j$, $r_{j,K}=f_j$) | 05 | D |
| S-172 | $p_{\mathrm{last}}$ | Last tradable price before a jump (A-GAP derivation) | 05 | R |
| S-173 | $\nu^{\star}$ | NAV per unit at the instant of an external flow | 05 | D |
| S-174 | $W^{\min}_{t+1}(a)$ | Worst-case next-period wealth under tier U bounds, built only from $\mathcal F_t$-measurable terms (05 §7) | 05, 08 | D |
| S-175 | $\Delta$ (prefix) | First difference: $\Delta Z_{t+1}=Z_{t+1}-Z_t$; $(\cdot)^{+}=\max(\cdot,0)$ | all | — |
| S-176 | $\hat e,\ \Phi$ | Generic estimate in $\mathsf S_t$ and the estimator map producing it (NLA rule) | 01 | E |
| S-177 | $\mathcal P_{t,\delta}$ | Ambiguity set constructed to contain the true law with probability $\ge1-\delta$ | 01, 08 | E |
| S-178 | $a^{\star}_t$ | Optimiser proposal / argmax | 01 | D |
| S-179 | $n^{\log}$ | Log-growth-optimal size (when defined) | 01 | D |
| S-180 | $\varpi,\ \lambda^{\mathrm{ES}},\ \varrho$ | Fractional-Kelly multiplier; mean–ES trade-off weight; risk-sensitivity coefficient (preferences; comparison only) | 01 | P |
| S-181 | $\mathrm{LB}^{\mathrm{naive}}$ | Difference-of-infima advantage (shown inadmissible, P-12a) | 08 | D |
| S-182 | $\mathcal W_S,\ \mathcal W_G,\ \mathcal W_U$ | Disturbance sets: all period outcomes consistent with the tier-S, tier-G, tier-U assumptions respectively (attainable bounds, no dependence restriction) | 08 (T-21), 01 §7 | M |
| S-183 | $\mathbb E_{\mathbb Q}[\cdot],\ \mathbb P(\cdot)$ | Expectation under law $\mathbb Q$ (default $\mathbb P$); probability | all | M |
| S-184 | $p^{\mathrm{gx}}(n)$ | Tier-G exit-price bound $\min((1-\Gamma_i)p^{\mathrm{stop}},\ p^{\mathrm{stop}}-\kappa^{\mathrm{out}}(n))$ | 05, 06 | D |
| S-185 | $\bar A_{t+1}$ | $\mathcal F_t$-measurable upper bound on $\mathrm{Accr}_{t+1}$ | 05 §7 | D |
| S-186 | $\ell_k$ | Per-share consumption of constraint $k$ when $g_k$ is linear ($g_k(n)=n\ell_k$); $\ell^{\mathrm{stop}}$ is the H1 instance | 06 §6, 08 | D |
| S-187 | $\tau^{\mathrm{CA}},\ \psi$ | Instant of a corporate action; split ratio of the value-neutral restatement | 05 §1 | O |
| S-188 | OC-$k$ | Register of deliberate conservative over-charges in hard bounds (OC-1: no $\Lambda$ credit in open risk) | 05 §4 | P |

**Scoping rule.** Symbols introduced inside a theorem's ASSUMPTIONS block in 08 (e.g. $A_{\mathbb Q}$, $B_{\mathbb Q}$ in P-12a) are local to that
theorem and do not collide with registry symbols.

## K. Registry-level open items

1. $W_t$ depends on the liquidation-cost model $\Lambda$ (S-041). Until $\Lambda$ is resolved, every floor, cushion and budget that
   uses $W_t$ is **conditionally defined**. A conservative placeholder ($\Lambda_i\ge q_i\varsigma_i/2+\phi^{\mathrm{sell}}_i(q_i)$) is a
   *lower bound* on liquidation cost and therefore not conservative for $W$; see RQ-05.
2. The brief's "entry" is split into three distinct objects: arrival mid $m^{\mathrm{arr}}$ (accounting reference), limit $p^{\mathrm{lim}}$
   (worst-case entry for safety), and realised fill $f_j$ (ex post). Conflating them is failure mode FM-DC-1 (09).
3. The brief's "equity" and "wealth" are distinct: $E_t$ (mark-to-mid) vs $W_t$ (net liquidation). The safety layer uses $W_t$.
4. The brief's "positions" are $q_{i,t}$; "execution risk" is represented by $\mathrm{ER}(n)$, A-STOP, A-GAP and $e$ (partial fills), not by a
   single scalar.
