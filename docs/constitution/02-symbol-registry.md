# 02 — Complete Symbol Registry (v0.2-draft)

Status: DRAFT — for human review. This registry is the **single authority for notation**. No symbol may appear in any
other document of this programme unless it is registered here. A symbol whose definition is incomplete is marked
**UNDEFINED — REQUIRES RESOLUTION** and may not be used in a safety-critical equation until resolved. Formulas that *define*
symbols are canonical in [14-formula-registry.md](14-formula-registry.md) (F-IDs cited in the Meaning column).
v0.2 changes (AUD-006/007/008/009/023): every row complete; renames resolving duplicate meanings; individual policy parameters,
index letters, dummies, spaces and operators registered; aliases and proof-local namespaces made explicit. Closure is checked
mechanically by `tools/doccheck/check_constitution.py`.

## 0. Conventions

**Source / class codes** (the brief's "deterministic or stochastic" column, made precise):

| Code | Class | Meaning | Known at decision time $\tau_t$? |
|---|---|---|---|
| P | Policy constant | Set by the human controller, versioned, never estimated by the engine | Yes (deterministic) |
| O | Observed authoritative input | Supplied by the authority boundary inside the snapshot $\mathsf S_t$ | Yes ($\mathcal F_t$-measurable); stochastic as a process |
| D | Derived | Deterministic function of O and P (and of earlier D carried as state) | Yes ($\mathcal F_t$-measurable) |
| E | Estimate / proxy | Deterministic statistic of admissible historical data that stands in for an *unknown* quantity | Yes as a number; its *meaning* is uncertain |
| R | Random / future | Realised only in $(\tau_t,\tau_{t+1}]$; not $\mathcal F_t$-measurable | No |
| M | Model object | Mathematical construct (measure, σ-algebra, functional, operator, bound variable) — not data | n/a |

**Sign conventions (global).** Quantities: $q>0$ long, $q<0$ short; fill quantity $n^{\mathrm{fill}}_j>0$ buy, $<0$ sell. Cash flows into
the account are positive. **Loss, cost, consumption and risk quantities are non-negative where larger = worse** (loss-positive);
P&L quantities are profit-positive.

**Units.** $[\mathrm{USD}]$ money; $[\mathrm{sh}_i]$ shares of instrument $i$ (shares of different instruments are **not** commensurable);
$[\mathrm T]$ calendar time; $[\mathrm{day}]$ trading day; $[\mathrm{unit}]$ fund unit; $[1]$ dimensionless. "n/a" = the object has no
physical unit (set, identifier, operator). Machine-readable dimensions: 03 `dimtable`.

**Namespace rules.**
1. Upright multi-letter names ($\mathrm{DD}$, $\mathrm{BP}$, $\mathrm{ADV}$, …) are single symbols, never products.
2. A superscript in upright type ($r^{\mathrm{open}}$) or a single-letter / $\min$ / $\max$ / $\log$ / $(k)$ superscript label names a distinct
   symbol. Subscripts are indices unless upright.
3. **Prime convention:** $X'$ denotes the same registered quantity $X$ evaluated in a comparison state (metamorphic pairs, perturbations).
   It is not a new symbol. Exception: $n'_o$, the quantity of a pending entry order, is its own symbol (S-308).
4. Rows whose Type starts with "alias" document another notation for an existing symbol; rows whose Type starts with "compound" name an
   expression built from registered symbols. Neither introduces a new key.
5. **Proof-local namespaces** (§M) are valid only inside the named theorem block of 08.
6. Standard operators ($\max,\min,\inf,\sup,\log,\exp,\sqrt{\cdot}$, floor, ceiling, $\sum,\prod,\int$, $\arg\max$, derivative) and set/logic
   symbols are not registered; project-specific operators are (§K).

---

## A. Index sets, time, lattice, indices, dummies

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-001 | $t$ | Decision epoch index | integer | n/a | $\mathbb N_0$ | [1] | n/a | $t\le T^{\mathrm{hor}}$ | snapshot sequence number | O |
| S-002 | $\tau_t$ | Wall-clock instant of epoch $t$ | timestamp | $\mathbb T$ | UTC instants (integer ns) | [T] | n/a | strictly increasing in $t$ | authority clock in $\mathsf S_t$ | O |
| S-003 | $\mathbb I_t$ | Instrument universe admissible at $t$ | finite set | $\mathbb T$ | finite sets of instrument IDs | n/a | n/a | as-of $\tau_t$ (no survivorship) | versioned reference data | O |
| S-004 | $N_t$ | Cardinality of $\mathbb I_t$ | integer | $\mathbb T$ | $\mathbb N_0$ | [1] | n/a | $\ge0$ | derived | D |
| S-005 | $\mathbb S$ | Strategy identifiers | finite set | n/a | sets of IDs | n/a | n/a | non-empty if any trade | policy | P |
| S-006 | $\mathbb C,\ \mathrm{cl}$ | Cluster set; map $\mathrm{cl}:\mathbb I\to\mathbb C$ ("correlation groups") | set, function | $\mathbb I$ | $\mathbb C$ | n/a | n/a | total map; versioned; human-set; a statistical clustering may only merge clusters of it (closure, AUD-040); **construction UNDEFINED — REQUIRES RESOLUTION** (RQ-10) | policy | P |
| S-007 | $\delta_q$ | Quantity lattice step | rational | n/a | $\mathbb Q_{>0}$ | [sh$_i$] | + | $1$ or $10^{-k}$ — **UNDEFINED — REQUIRES RESOLUTION** (D-04) | policy | P |
| S-008 | $\mathbb L$ | Quantity lattice $\delta_q\mathbb Z$; $\mathbb L_{\ge0}$, $\mathbb L_{>0}$ its parts; $\mathbb L^{N}$ vectors | set | n/a | subsets of $\mathbb Q$ | [sh$_i$] | n/a | n/a | derived (F097) | D |
| S-009 | $\bar N$ | Maximum admissible order quantity | rational | n/a | $\mathbb L_{>0}$ | [sh$_i$] | + | value **UNDEFINED — REQUIRES RESOLUTION** | policy | P |
| S-010 | $\bar M$ | Maximum admissible magnitude of any monetary quantity | rational | n/a | $\mathbb Q_{>0}$ | [USD] | + | value **UNDEFINED — REQUIRES RESOLUTION** | policy | P |
| S-011 | $h$ | Intended holding horizon of an opportunity | duration | opportunities | $\mathbb Q_{>0}$ | [day] | + | horizon classes **UNDEFINED — REQUIRES RESOLUTION** (D-09) | opportunity | O |
| S-189 | $i$ | Instrument index | bound variable | n/a | $\mathbb I_t$ | n/a | n/a | n/a | notation | M |
| S-190 | $j$ | Fill index | bound variable | n/a | $\mathcal J_{t+1}$ | n/a | n/a | n/a | notation | M |
| S-191 | $k$ | Generic integer index / counter (constraint index over $\mathcal K$, chain step, exponent, count) — always bound where used | bound variable | n/a | $\mathbb Z$ | [1] | n/a | n/a | notation | M |
| S-192 | $s$ | Strategy index | bound variable | n/a | $\mathbb S$ | n/a | n/a | n/a | notation | M |
| S-193 | $c$ | Cluster index | bound variable | n/a | $\mathbb C$ | n/a | n/a | n/a | notation | M |
| S-194 | $u$ | Dummy epoch index | bound variable | n/a | $\mathbb T$ | n/a | n/a | n/a | notation | M |
| S-195 | $y,\ y_k$ | Generic real dummy (bound in inf/min/sup, set-builder, generic statements) | bound variable | n/a | $\mathbb R$ | as context | n/a | n/a | notation | M |
| S-196 | $\upsilon$ | Integration variable | bound variable | n/a | $(0,1)$ | [1] | n/a | n/a | notation | M |
| S-197 | $\mathbb T$ | Set of decision epochs | set | n/a | subsets of $\mathbb N_0$ | n/a | n/a | n/a | definition | M |
| S-198 | $T^{\mathrm{hor}}$ | Terminal epoch of a research horizon | integer | n/a | $\mathbb N_0$ | [1] | n/a | $\ge0$ | research design | P |
| S-199 | $\mathbb N,\ \mathbb Z,\ \mathbb Q,\ \mathbb R$ | Number sets (naturals, integers, rationals, reals); subscripts $\ge0$, $>0$ restrict | set | n/a | n/a | n/a | n/a | n/a | mathematics | M |

## B. Authority and provenance

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-020 | $\mathsf S_t$ | Authoritative immutable snapshot (consistent cut) | record | $\mathbb T$ | $\mathfrak S$ | n/a | n/a | schema-valid, hash-identified | authority boundary | O |
| S-021 | $\mathrm{hash}$ | Content hash over canonical serialisation | function | byte strings | $\{0,1\}^{256}$ | n/a | n/a | SHA-256 (PROVISIONAL) | derived | D |
| S-022 | $A_{\mathrm{id}}$ | Account/scope identifier bound in the snapshot | identifier | $\mathbb T$ | IDs | n/a | n/a | equals requested scope; **binding method UNDEFINED — REQUIRES RESOLUTION** | authority boundary | O |
| S-023 | $t^{\mathrm{know}}$ | Knowledge time of a datum $\mathsf d$ | timestamp | data items | UTC | [T] | n/a | $\le\tau_t$ for admission (F003) | provenance metadata | O |
| S-024 | $\mathrm{age}_t$ | $\tau_t-t^{\mathrm{know}}(\mathsf d)$ (F045) | duration | data items | $\mathbb Q_{\ge0}$ | [T] | + | $\le\mathrm{TTL}$ | derived | D |
| S-025 | $\mathrm{TTL}$ | Maximum admissible age per datum class | duration | datum classes | $\mathbb Q_{>0}$ | [T] | + | values **UNDEFINED — REQUIRES RESOLUTION** (RQ-19) | policy | P |
| S-026 | $\mathcal R^{\mathrm{req}}$ | Required-input registry (field, validator) | finite set | n/a | n/a | n/a | n/a | completeness **NOT YET PROVEN** (T-04) | policy | P |
| S-027 | $\alpha_t$ | Authority indicator (F046) | boolean | $\mathfrak S$ | $\{0,1\}$ | [1] | n/a | n/a | derived | D |
| S-028 | $\mathsf v$ | Version tuple (constitution, formula, parameter set, schema, code, estimator definitions) | tuple | n/a | $\mathcal V$ | n/a | n/a | all present | policy/build | P |
| S-200 | $\mathsf d$ | A datum (element of a snapshot) | record | n/a | data items | n/a | n/a | bitemporal | data | O |
| S-201 | $\mathfrak S$ | Space of schema-valid snapshots | set | n/a | canonical byte strings | n/a | n/a | countable | schema | M |

## C. Portfolio and accounting state

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-030 | $C_t$ | Cash ledger balance | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + asset | cash account $\ge0$; $\lvert C_t\rvert\le\bar M$ | ledger | O |
| S-031 | $C^{\mathrm{set}}_t,\ C^{\mathrm{uns}}_t$ | Settled / unsettled cash | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + asset | **semantics UNDEFINED — REQUIRES RESOLUTION** (RQ-20) | ledger | O |
| S-032 | $q_{i,t}$ | Quantity of instrument $i$ held at the cut: the authoritative position after every fill, partial exit, reduction, execution correction and reconciliation (the *held* quantity; never the cumulative fill $q^{\mathrm{fill}}_o$ of an order, F150) | lattice | $\mathbb T\times\mathbb I$ | $\mathbb L$ | [sh$_i$] | + long | v0: $\ge0$ (D-01); with a pending entry order $o$ on $i$: $q_{i,t}\le q^{\mathrm{fill}}_o$ (F150) | positions | O |
| S-033 | $\bar c_{i,t}$ | Cost basis per share (attribution only) | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{\ge0}$ | [USD/sh$_i$] | n/a | method **UNDEFINED — REQUIRES RESOLUTION**; not safety-relevant | ledger | O |
| S-034 | $p^{\mathrm{stop}}$ | Protective stop trigger price of a held position ($p^{\mathrm{stop}}_{i,t}$) or of an opportunity ($p^{\mathrm{stop}}_o$) | scalar | positions ∪ opportunities | $\mathbb Q_{>0}\cup\{\bot\}$ | [USD/sh$_i$] | n/a | long: below the mark, else ANOMALY; $\bot$ ⇒ D-06 | order state / opportunity | O |
| S-035 | $Y_t$ | Accrued liabilities (F053) | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + owed | $\le\bar M$ | ledger | O |
| S-036 | $X_{t+1}$ | Net external capital flow in the period | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + deposit | floor theorems require $0$ | ledger | R |
| S-037 | $\mathrm{Inc}_{t+1}$ | Income credited (dividends, interest) | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | n/a | ledger | R |
| S-038 | $\mathrm{Fin}_{t+1}$ | Financing / borrow charges | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + cost | v0: $0$ | ledger | R |
| S-039 | $U_t$ | Fund units outstanding (F069) | scalar | $\mathbb T$ | $\mathbb Q_{>0}$ | [unit] | + | changes only on flows | unitisation ledger | D |
| S-040 | $E_t$ | Mark-to-mid equity (F033) | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + | any sign | derived | D |
| S-041 | $\Lambda_{i,t},\ \Lambda_t$ | Liquidation cost of holding $i$ from mid, and total (F035; A-ACC-04) | scalar | $\mathbb T(\times\mathbb I)$ | $\mathbb Q_{\ge0}$ | [USD] | + cost | $\ge\Lambda^{\mathrm{floor}}_{i,t}$ (F111); model **UNDEFINED — REQUIRES RESOLUTION** (RQ-05) | model with floor | E |
| S-042 | $W_t$ | Net liquidation wealth (F034) | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + | any sign | derived | D |
| S-043 | $\nu_t$ | NAV per unit (F036) | scalar | $\mathbb T$ | $\mathbb Q$ | [USD/unit] | + | n/a | derived | D |
| S-044 | $\Pi^{R}_t,\ \Pi^{U}_t$ | Cumulative realised / unrealised P&L (attribution only, DC-4) | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + profit | never an authority input | derived | D |
| S-045 | $\mathrm{Accr}_{t+1}$ | Liabilities accrued in the period (not in fees or Fin) | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + owed | floor theorems assume $0$ | ledger | R |
| S-046 | $\mathrm{Pay}_{t+1}$ | Payments of previously accrued liabilities | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + outflow | $\le Y_t+\mathrm{Accr}_{t+1}$ | ledger | R |
| S-122 | $\mathrm{BP}_t$ | Broker-reported buying power | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + | authority for broker acceptance only | authority boundary | O |
| S-123 | $\mathrm{BP}^{\mathrm{avail}}_t$ | Buying power available to a new order (F048) | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + | n/a | derived | D |
| S-124 | $\mathrm{IM}_t,\ \mathrm{MM}_t$ | Initial / maintenance margin requirement | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | out of v0 scope (D-02): **UNDEFINED — REQUIRES RESOLUTION** | authority boundary | O |
| S-166 | $C^{\mathrm{avail}}_t$ | Cash available for purchases under settlement rules | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + | **UNDEFINED — REQUIRES RESOLUTION** (RQ-20) | derived | D |

## D. Market state

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-050 | $p^{\mathrm{bid}},\ p^{\mathrm{ask}}$ | Best bid / ask ($p^{\mathrm{bid}}_{i,t}$, $p^{\mathrm{ask}}_{i,t}$) | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{>0}$ | [USD/sh$_i$] | n/a | $0<p^{\mathrm{bid}}<p^{\mathrm{ask}}$ | market data | O |
| S-051 | $m_{i,t}$ | Mid (F031); also at an instant: $m_{\tau}$ | scalar | $(\mathbb T\cup\text{instants})\times\mathbb I$ | $\mathbb Q_{>0}$ | [USD/sh$_i$] | n/a | n/a | derived | D |
| S-052 | $\varsigma_{i,t}$ | Quoted spread (F032) | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{>0}$ | [USD/sh$_i$] | + cost | $>0$ | derived | D |
| S-053 | $m^{\mathrm{arr}}$ | Arrival mid of the opportunity's instrument | scalar | opportunities | $\mathbb Q_{>0}$ | [USD/sh$_i$] | n/a | $=m_{i,t}$ | derived | D |
| S-054 | $\mathrm{ADV}_{i,t}$ | Average daily volume used by the hard layer: $\min(\mathrm{ADV}^{\mathrm{est}}_{i,t},\mathrm{ADV}^{\max}_i)$ (F111) | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{>0}$ | [sh$_i$/day] | + | $>0$; missing estimate ⇒ $\alpha_t=0$ | derived | D |
| S-055 | $\hat\sigma_{i,t}$ | Volatility estimate of mid log-returns | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{\ge0}$ | [day$^{-1/2}$] | + | estimator **UNDEFINED** | statistic | E |
| S-056 | $\hat\Sigma_t$ | Covariance estimate of daily log-returns | matrix | $\mathbb T$ | PSD matrices | [day$^{-1}$] | n/a | model layer only | statistic | E |
| S-247 | $\hat\rho_{i,t}$ | Correlation estimate (pair of instruments indexed by the subscript) | scalar | $\mathbb T\times\mathbb I^2$ | $[-1,1]$ | [1] | n/a | model layer only | statistic | E |
| S-057 | $\mathrm{st}_{i,t}$ | Trading status | enum | $\mathbb T\times\mathbb I$ | {TRADING, HALTED, LULD\_PAUSE, UNKNOWN} | n/a | n/a | only TRADING admits new risk | market data | O |
| S-058 | $\mathrm{ev}_{i,t}$ | Scheduled-event flag within the horizon | enum | $\mathbb T\times\mathbb I$ | {NONE, EVENT, UNKNOWN} | n/a | n/a | **source UNDEFINED — REQUIRES RESOLUTION** (RQ-04) | reference data | O |
| S-059 | $r_{i,t+1}$ | Simple mid return | scalar | $\mathbb T\times\mathbb I$ | $[-1,\infty)$ | [1] | + gain | $\ge-1$ | market | R |

## E. Opportunity, action, decision spaces

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-060 | $o$ | Opportunity (instrument, direction, limit, stop, target, strategy, horizon, id); $o_1,o_2$ distinct opportunities | record | n/a | $\mathcal O$ | n/a | n/a | all fields valid | strategy | O |
| S-061 | $d$ | Direction | enum | opportunities | $\{+1,-1\}$ | [1] | +1 buy | v0: $+1$ (D-01) | opportunity | O |
| S-062 | $p^{\mathrm{lim}}$ | Entry limit price = worst admissible entry fill | scalar | opportunities | $\mathbb Q_{>0}$ | [USD/sh$_i$] | n/a | G7 (F092) | opportunity | O |
| S-063 | $p^{\mathrm{stop}}_o$ | Stop of the new position | alias of S-034 | opportunities | $\mathbb Q_{>0}$ | [USD/sh$_i$] | n/a | G7 | opportunity | O |
| S-064 | $p^{\mathrm{tgt}}$ | Target price (model layer only; forbidden in the hard layer, Art. 6) | scalar | opportunities | $\mathbb Q_{>0}$ | [USD/sh$_i$] | n/a | n/a | opportunity | O |
| S-065 | $n$ | Candidate increment quantity for $o$ | lattice | n/a | $\mathbb L_{\ge0}$ | [sh$_i$] | + | $\le\bar N$ | decision variable | D |
| S-066 | $a_t$ | Action: signed quantity-change vector; $a$ generic action | vector | $\mathbb T$ | $\mathbb L^{N_t}$ | [sh$_i$] per component | + buy | n/a | decision output | D |
| S-067 | $\omega_t$ | Order parameters attached to the action (limit, stop, TIF) | record | $\mathbb T$ | orders | n/a | n/a | n/a | decision output | D |
| S-068 | $a^{\varnothing}$ | No-trade action $0$ (brief's $a_0$) | vector | n/a | $\{0\}$ | [sh$_i$] | n/a | always admissible as a decision | definition | D |
| S-069 | $\mathcal A^{+},\ \mathcal A^{-},\ \mathcal A^{h}$ | Risk-increasing / risk-reducing / hold action classes (F005) | sets | states | subsets of $\mathbb L^{N}$ | n/a | n/a | partition | derived | D |
| S-070 | $\mathcal A^{\mathrm{safe}}$ | Safe risk-increasing action set (F024) | set | states | subsets of $\mathcal A^{+}$ | n/a | n/a | may be empty ⇒ NO TRADE / RECOVERY | derived | D |
| S-071 | $e$ | Executed (cumulative filled) quantity of an order for $n$ | lattice | orders | $\mathbb L_{\ge0}$ | [sh$_i$] | + | $0\le e\le n$ | execution | R |
| S-202 | $\mathcal O$ | Space of opportunities | set | n/a | records | n/a | n/a | n/a | schema | M |
| S-203 | $\Theta$ | Admissible policy-parameter set (F109) | set | n/a | parameter vectors | n/a | n/a | n/a | policy | P |
| S-204 | $\mathcal V$ | Space of version tuples | set | n/a | tuples of IDs | n/a | n/a | n/a | schema | M |
| S-205 | $\mathfrak D$ | Space of decision records | set | n/a | records | n/a | n/a | schema **UNDEFINED — REQUIRES RESOLUTION** | schema | M |
| S-209 | $V$ | Exact verifier of an optimiser proposal (F126) | function | proposals | $\mathbb L_{\ge0}$ | [sh$_i$] | + | $0\le V\le Q^{\mathrm{hard}}$ | derived | D |
| S-210 | $\tilde n$ | Optimiser proposal (any value, possibly invalid) | scalar | n/a | $\mathbb R\cup\{\text{invalid}\}$ | [sh$_i$] | + | unconstrained | optimiser | E |

## F. Execution, costs, scenario losses

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-080 | $\mathcal J_{t+1}$ | Set of fills in $(\tau_t,\tau_{t+1}]$ | finite set | $\mathbb T$ | sets of fills | n/a | n/a | n/a | execution reports | R |
| S-081 | $n^{\mathrm{fill}}_j,\ p^{\mathrm{fill}}_j,\ \phi_j,\ \tau^{\mathrm{fill}}_j$ | Fill signed quantity, price, fee, instant; instrument $i(j)$ | tuple | $\mathcal J_{t+1}$ | $\mathbb L\setminus\{0\}$, $\mathbb Q_{>0}$, $\mathbb Q_{\ge0}$, instants | mixed (sh, USD/sh, USD, T) | $n^{\mathrm{fill}}_j>0$ buy | n/a | execution reports | R |
| S-082 | $\pi^{\mathrm{ref}}_j,\ \pi^{\mathrm{ref}}_{j,k}$ | Reference price of fill $j$ and its decomposition chain ($\pi^{\mathrm{ref}}_{j,0}=\pi^{\mathrm{ref}}_j$, $\pi^{\mathrm{ref}}_{j,k_j}=p^{\mathrm{fill}}_j$) | scalar | $\mathcal J\times\mathbb N_0$ | $\mathbb Q_{>0}$ | [USD/sh$_i$] | n/a | convention 05 §3 | derived | D |
| S-083 | $\mathcal C_{j,k}$ | $k$-th execution-cost component of fill $j$ (F057) | scalar | $\mathcal J\times\mathbb N$ | $\mathbb Q$ | [USD] | + cost | may be negative (improvement) | derived ex post | D |
| S-084 | $\phi^{\mathrm{buy}},\ \phi^{\mathrm{sell}},\ \phi^{\mathrm{sell}}_{\cdot,0}$ | Per-order fee schedules as functions of cumulative filled quantity; sell fee evaluated at price 0 | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD] | + cost | $\phi(0)=0$, non-decreasing (A-EXE-01, A-EXE-04); values **UNDEFINED — REQUIRES RESOLUTION** | versioned schedule | P |
| S-085 | $\kappa^{\mathrm{out}}$ | Per-share exit cost below the stop trigger under normal execution ($\kappa^{\mathrm{out}}_i(n)$), floored by policy (F111) | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD/sh$_i$] | + cost | $\ge\kappa^{\min}p^{\mathrm{stop}}$; non-decreasing in $n$; model **UNDEFINED — REQUIRES RESOLUTION** (RQ-05) | model with floor | E |
| S-086 | $\kappa^{\mathrm{liq}}$ | Per-share cost to liquidate from mid | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD/sh$_i$] | + cost | $\ge\varsigma/2$ | model | E |
| S-087 | $\iota$ | Ex-ante expected market impact per share (model layer only, DC-6) | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD/sh$_i$] | + cost | **UNDEFINED** | model | M |
| S-088 | $\Gamma_i$ | Gap-stress fraction (F111) | scalar | $\mathbb I$ | $(0,1]$ | [1] | + worse | $\ge\Gamma^{\min}$; **UNDEFINED — REQUIRES RESOLUTION** (RQ-04) | policy floor ∨ estimate | E |
| S-089 | $\gamma_j$ | Realised gap/slippage beyond stop for a stop-exit fill | scalar | stop fills | $\mathbb Q$ | [USD/sh$_i$] | + adverse | n/a | execution | R |
| S-090 | $L^{\mathrm{stop}}$ | Stop-scenario loss bound of a new entry, $L^{\mathrm{stop}}(n)$ (F061) | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD] | + loss | conditional on tier S | derived | D |
| S-091 | $L^{\mathrm{gap}}$ | Gap-scenario loss bound (F062) | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD] | + loss | conditional on tier G | derived | D |
| S-092 | $L^{\mathrm{abs}}$ | Absolute loss bound, price → 0 (F063) | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD] | + loss | long only | derived | D |
| S-093 | $\ell^{\mathrm{stop}}$ | Per-share stop loss when $L^{\mathrm{stop}}$ is linear; in the brief's naive formula the stop distance only (F110) | scalar | n/a | $\mathbb Q_{>0}$ | [USD/sh$_i$] | + loss | G7 | derived | D |
| S-094 | $\mathrm{ER}$ | Execution-assumption risk increment $\mathrm{ER}(n)$ (F067) | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD] | + | $\ge0$ by construction | derived | D |
| S-095 | $r^{\mathrm{open}},\ g^{\mathrm{open}},\ u^{\mathrm{open}}$ | Open stop / gap / absolute risk of held position $i$ (F064–F066; no $\Lambda$ credit, OC-1) | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{\ge0}$ | [USD] | + loss | negative raw value ⇒ ANOMALY | derived | D |
| S-096 | $R^{\mathrm{open}},\ G^{\mathrm{open}},\ Z^{\mathrm{open}},\ N^{\mathrm{open}}$ | Aggregates of open risks and gross notional; restrictions by $s$ / $c$ subscript (F050) | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | n/a | derived | D |
| S-097 | $R^{\mathrm{res}},\ G^{\mathrm{res}},\ Z^{\mathrm{res}},\ N^{\mathrm{res}},\ C^{\mathrm{res}}$ | Reserved stop-risk, gap-risk, absolute risk (full $L^{\mathrm{abs}}$ incl. fees), notional, cash of pending orders; restrictions by $i$ / $s$ / $c$ | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | computed at $p^{\mathrm{lim}}$ | reservation ledger | O |
| S-248 | $Q^{\mathrm{res}}_{i,t}$ | Unfilled quantity of pending orders on instrument $i$ (F144: $q^{\mathrm{unf}}_o=n'_o-q^{\mathrm{fill}}_o$ per order, never $n'_o-q_{i,t}$) | lattice | $\mathbb T\times\mathbb I$ | $\mathbb L_{\ge0}$ | [sh$_i$] | + | v0: $0$ for a new order (G11) | reservation ledger | O |
| S-211 | $p^{\mathrm{in}},\ p^{\mathrm{out}}$ | Realised average entry / exit fill price of a round trip | scalar | round trips | $\mathbb Q_{\ge0}$ | [USD/sh$_i$] | n/a | $p^{\mathrm{in}}\le p^{\mathrm{lim}}$ (A-MKT-05) | execution | R |
| S-184 | $p^{\mathrm{gx}}$ | Tier-G exit-price bound (F060) | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD/sh$_i$] | n/a | $\le p^{\mathrm{stop}}-\kappa^{\mathrm{out}}$ | derived | D |
| S-172 | $p_{\mathrm{last}}$ | Last tradable price before a jump (A-GAP derivation) | scalar | paths | $\mathbb Q_{\ge0}$ | [USD/sh$_i$] | n/a | $\ge p^{\mathrm{stop}}$ while untriggered | market | R |
| S-214 | $\hat\Gamma_i,\ \hat\kappa^{\mathrm{out}}_i,\ \hat\Lambda_{i,t}$ | Estimates entering the hard layer only through the floors of F111 | scalar / function | $\mathbb I$ | $\mathbb Q_{\ge0}$ | [1], [USD/sh$_i$], [USD] respectively | + worse | frozen versioned estimators | statistic | E |
| S-249 | $\Lambda^{\mathrm{floor}}_{i,t}$ | Lower bound on liquidation cost: half-spread plus exit fee (F111) | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{\ge0}$ | [USD] | + cost | n/a | derived | D |
| S-288 | $\mathrm{XV}_{i,t+1}$ | Position-level realised exit value of exposure $i$ over the period: exit proceeds minus all exit fees paid plus liquidation value of the remainder (F072) | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q$ | [USD] | + value | A-TRIG lower bound | ledger + $\Lambda$ | R |
| S-289 | $q^{\mathrm{rem}}_{i,t+1}$ | Quantity of exposure $i$ still held at $\tau_{t+1}$ | lattice | $\mathbb T\times\mathbb I$ | $\mathbb L_{\ge0}$ | [sh$_i$] | + long | $\le q^{\mathrm{exp}}_i$ | positions | R |
| S-290 | $q^{\mathrm{exp}}_i$ | Exposure quantity of $i$ in the period: $q_{i,t}$ for a held position without a pending order; cumulative entry-fill quantity $e$ for a new or pending order on a fresh instrument; $q_{i,t}+e$ for a held position with a pending remainder of the same order (one exposure per instrument, G11) | lattice | $\mathbb I$ | $\mathbb L_{\ge0}$ | [sh$_i$] | + long | $\le$ the order quantity when an order is involved | positions / execution | R |
| S-291 | $\mathcal J^{\mathrm{ex}}_{i,t+1}$ | Exit (sell) fills of exposure $i$ in $(\tau_t,\tau_{t+1}]$ | finite set | $\mathbb T\times\mathbb I$ | subsets of $\mathcal J_{t+1}$ | n/a | n/a | n/a | execution reports | R |
| S-292 | $\phi^{\mathrm{split}}$ | Split envelope of a fee schedule: worst total fee when an exit of $n$ is split into at most $N^{\mathrm{ex}}+1$ fee-bearing parts (up to $N^{\mathrm{ex}}$ exit orders plus a part still held at the cut) (F140) | function | $\mathbb L_{\ge0}$ | $\mathbb Q_{\ge0}$ | [USD] | + cost | $\ge\phi(n)$; non-decreasing | derived from fee schedule | D |
| S-293 | $R^{\mathrm{led}}_{o}$ | Stop-risk reservation recorded in the ledger for pending order $o$ (ledger bookkeeping, T-11; not an input to engine budgets, which re-evaluate by F144) | scalar | pending orders | $\mathbb Q_{\ge0}$ | [USD] | + | n/a | reservation ledger | O |
| S-294 | $N^{\mathrm{ex}}$ | Maximum number of exit (sell) orders per exposure per period, declared by the execution integration and versioned in $\mathsf v$ | integer | n/a | $\mathbb N$ | [1] | + | **UNDEFINED — REQUIRES RESOLUTION** (RQ-35); unknown ⇒ per-execution worst case | integration contract | P |
| S-295 | $B^{\mathrm{win}}_{s}$ | Risk base at the start of strategy $s$'s loss window (fixed within the window; window defined with $\mathrm{SL}$, RQ-11) | scalar | $\mathbb S$ | $\mathbb Q$ | [USD] | + | **UNDEFINED — REQUIRES RESOLUTION** with $\mathrm{SL}$ (RQ-11) | derived | D |
| S-296 | $\phi^{\mathrm{paid}}_{o}$ | Entry fees of order $o$ already economically booked into $W_t$ at the cut: debited in $C_t$ or recorded as payable in $Y_t$ of the same snapshot (A-AUTH-04) — not fees reported, assessed or expected (F148, CLOSURE-REV-003) | scalar | entry orders not yet fee-final | $\mathbb Q_{\ge0}$ | [USD] | + cost | $0\le\phi^{\mathrm{paid}}_o\le\phi^{\mathrm{acc}}_o$, else $\alpha_t=0$ (F148) | ledger | R |
| S-297 | $r^{\mathrm{pf}}_{i},\ g^{\mathrm{pf}}_{i},\ u^{\mathrm{pf}}_{i}$ | Stop / gap / absolute exposure charge of instrument $i$ carrying an order that is pending with part of it already filled (F145); replaces open risk plus reservation for that instrument; in an invalid quantity state the F150 charge, the same value in every tier | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{\ge0}$ | [USD] | + loss | exact worst case under the tier's hypotheses | derived | D |
| S-298 | $\bar q_i$ | Largest quantity of instrument $i$ that can be held in the period: $q_{i,t}+q^{\mathrm{unf}}_o$ with a pending entry order $o$ on $i$, else $q_{i,t}$ (F070, F145); $q_{i,t}+n'_o$ in an invalid quantity state (F150) | lattice | $\mathbb I$ | $\mathbb L_{\ge0}$ | [sh$_i$] | + long | $\ge q_{i,t}$ | derived | D |
| S-299 | $\mathrm{ADV}^{\mathrm{est}}_{i,t}$ | Trailing average daily volume from a frozen, versioned estimator | scalar | $\mathbb T\times\mathbb I$ | $\mathbb Q_{\ge0}$ | [sh$_i$/day] | + | estimator **UNDEFINED — REQUIRES RESOLUTION** (RQ-06) | statistic | E |
| S-300 | $\mathrm{ADV}^{\max}_i$ | Policy cap on the volume used by H12, H13 (per instrument or instrument class) | scalar | $\mathbb I$ | $\mathbb Q_{>0}$ | [sh$_i$/day] | + | value **UNDEFINED — REQUIRES RESOLUTION** | policy | P |
| S-301 | $W^{\mathrm{R}}_t$ | Reference wealth: mark-to-mid equity less the liquidation cost at its policy floor, $E_t-\Lambda^{\mathrm{floor}}_t$ (F146); contains no estimate | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + | $\ge W_t$ | derived | D |
| S-302 | $\nu^{\mathrm{R}}_t$ | Reference NAV per unit $W^{\mathrm{R}}_t/U_t$ (F146); the only valuation used for carried references (F037, F041, F069) | scalar | $\mathbb T$ | $\mathbb Q$ | [USD/unit] | + | $\ge\nu_t$ | derived | D |
| S-303 | $\mathrm{DD}^{\mathrm{R}}_t$ | Reference drawdown $1-\nu^{\mathrm{R}}_t/H_t$ (F147) | scalar | $\mathbb T$ | $[0,\infty)$ | [1] | + worse | $\le\mathrm{DD}_t$ | derived | D |
| S-304 | $q^{\mathrm{fill}}_o$ | Cumulative venue fill of entry order $o$ at the cut (execution reports), including shares since exited; entry fees accrue on it (F148); not the held quantity | lattice | entry orders | $\mathbb L_{\ge0}$ | [sh$_i$] | + | $q_{i,t}\le q^{\mathrm{fill}}_o\le n'_o$ (A-EXE-03, F150), else $\alpha_t=0$ | execution reports (order state) | O |
| S-305 | $\phi^{\mathrm{acc}}_o$ | Largest entry fee the fills of order $o$ can cost, $\phi^{\mathrm{buy}}(q^{\mathrm{fill}}_o)$ (F148, A-EXE-04) | scalar | entry orders | $\mathbb Q_{\ge0}$ | [USD] | + cost | $\ge\phi^{\mathrm{paid}}_o$, else $\alpha_t=0$ | derived | D |
| S-306 | $\phi^{\mathrm{owed}}_o$ | Entry fee of order $o$ owed but not yet booked into $W_t$: $\phi^{\mathrm{acc}}_o-\phi^{\mathrm{paid}}_o$ until its fees are confirmed final, then $0$ (F148) | scalar | entry orders | $\mathbb Q_{\ge0}$ | [USD] | + cost | reserved in F144, F145 until booked (T-29) | derived | D |
| S-307 | $\bar Q^{\mathrm{hard}}_t$ | Hard quantity cap with every estimated input at its policy bound at every epoch (policy-bound envelope, T-28) | lattice | $\mathbb T$ | $\mathbb L_{\ge0}$ | [sh$_i$] | + | $\ge Q^{\mathrm{hard}}_t$ (T-28) | derived | D |
| S-308 | $n'_o$ | Total quantity ordered by entry order $o$ as submitted, fixed for the order's life; written $n'$ where $o$ is clear | lattice | entry orders | $\mathbb L_{>0}$ | [sh$_i$] | + | $\ge q^{\mathrm{fill}}_o$ (F150), else $\alpha_t=0$ | order state | O |
| S-309 | $q^{\mathrm{unf}}_o$ | Unfilled remainder of entry order $o$: $n'_o-q^{\mathrm{fill}}_o$, the most it can still fill (A-EXE-03); exited shares are not in it (named "unf" because $q^{\mathrm{rem}}$ is S-289) | lattice | entry orders | $\mathbb L_{\ge0}$ | [sh$_i$] | + | $0\le q^{\mathrm{unf}}_o\le n'_o$ in a valid quantity state (F150) | derived | D |

## G. Capital, floors, drawdown, budgets, caps

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-100 | $B_t$ | Risk base (candidates F073) | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + | **UNDEFINED — REQUIRES RESOLUTION** (06 §4; RQ-02) | derived | D |
| S-101 | $H_t$ | High-water mark of the reference NAV $\nu^{\mathrm{R}}$ (F037, F146; never of an estimate-inclusive NAV, CLOSURE-REV-002) | scalar | $\mathbb T$ | $\mathbb Q_{>0}$ | [USD/unit] | + | observation set $\mathcal H_t$ **UNDEFINED** (RQ-03) | state | D |
| S-102 | $\mathrm{DD}_t$ | Drawdown (F038) | scalar | $\mathbb T$ | $[0,\infty)$ | [1] | + worse | $\ge1$ iff $\nu\le0$ | derived | D |
| S-103 | $\mathrm{MDD}_t$ | Maximum drawdown (F039) | scalar | $\mathbb T$ | $[0,\infty)$ | [1] | + worse | n/a | derived | D |
| S-104 | $\nu^{\mathrm{day}}_0,\ \nu^{\mathrm{wk}}_0$ | Reference NAV per unit $\nu^{\mathrm{R}}$ (F146) at the start of the trading day / week | scalar | $\mathbb T$ | $\mathbb Q$ | [USD/unit] | n/a | boundaries **UNDEFINED** (RQ-31) | state | D |
| S-105 | $F^{\mathrm{abs}}$ | Absolute capital floor | scalar | n/a | $\mathbb Q_{\ge0}$ | [USD] | n/a | value **UNDEFINED — REQUIRES RESOLUTION** | policy | P |
| S-106 | $F^{\mathrm{dd}}_t$ | Drawdown floor (F040) | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | n/a | n/a | derived | D |
| S-107 | $F^{\mathrm{day}}_t,\ F^{\mathrm{wk}}_t$ | Daily / weekly floors (F041) | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | n/a | n/a | derived | D |
| S-108 | $F^{\mathrm{lock}}_t$ | Profit-lock floor (F042) | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | n/a | n/a | derived | D |
| S-109 | $F_t$ | Effective floor (F043) | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | n/a | n/a | derived | D |
| S-110 | $K_t$ | Cushion (F044) | scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + room | $\le0$ ⇒ no risk increase | derived | D |
| S-111 | $\vartheta$ | Throttle function; $\vartheta_K$ the cushion-induced throttle (F098) | function | states | $[0,1]$ | [1] | n/a | separate throttle **UNDEFINED** | derived | D |
| S-112 | $\theta$ | Policy-parameter vector (components S-250 … S-274) | vector | n/a | $\Theta$ | mixed | n/a | F109 | policy | P |
| S-113 | $g_k,\ b_k$ | Consumption $g_k(x,n)$ and remaining budget $b_k(x)$ of hard constraint $k$ | function, scalar | states × $\mathbb L_{\ge0}$ | $\mathbb Q$ | per constraint | + | $g_k(x,0)=0$, non-decreasing in $n$ | derived | D |
| S-114 | $Q$ | Cap quantity: $Q_k$ from constraint $k$ (F094); unindexed in worked examples | lattice | constraints | $\mathbb L_{\ge0}$ | [sh$_i$] | + | n/a | derived | D |
| S-115 | $Q^{\mathrm{hard}}$ | Hard cap (F096) | lattice | n/a | $\mathbb L_{\ge0}$ | [sh$_i$] | + | n/a | derived | D |
| S-116 | $Q^{\mathrm{fin}}$ | Final maximum quantity (F001) | lattice | n/a | $\mathbb L_{\ge0}$ | [sh$_i$] | + | $\le Q^{\mathrm{hard}}$ | derived | D |
| S-117 | $R^{\mathrm{hard}}_t$ | Hard stop-risk budget (F074) | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | n/a | derived | D |
| S-118 | $G^{\mathrm{hard}}_t$ | Hard gap-risk budget (F075) | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | n/a | derived | D |
| S-119 | $R^{\mathrm{mod}}_t$ | Model-layer proposed budget | scalar | $\mathbb T$ | $\mathbb R\cup\{\text{invalid}\}$ | [USD] | + | sanitised by $\mathfrak s$ | model | E |
| S-120 | $\mathfrak s$ | Sanitiser (F047) | function | $\mathbb R\cup\{\text{invalid}\}$ | $[0,\infty]$ | [USD] | n/a | per-model REQUIRED/OPTIONAL flag is policy | derived | D |
| S-121 | $R^{\mathrm{allow}}_t$ | Allowed stop-risk budget (F049) | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | $\le R^{\mathrm{hard}}_t$ (T-01) | derived | D |
| S-164 | $b^{\mathrm{hard}}_k,\ b^{\mathrm{mod}}_k,\ b^{\mathrm{allow}}_k$ | Hard, model-proposed, allowed budget of constraint $k$ (F049) | scalar | $\mathcal K$ | $\mathbb Q$ | per constraint | + | $0\le b^{\mathrm{allow}}_k\le b^{\mathrm{hard}}_k$ | derived / model / derived | D |
| S-165 | $\mathrm{SL}_{s,t}$ | Strategy realised-loss term | scalar | $\mathbb S\times\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + loss | **UNDEFINED — REQUIRES RESOLUTION** (RQ-11); fail-closed rule F074 note | derived | D |
| S-167 | $\mathcal H_t$ | Epochs eligible for the high-water mark | set | $\mathbb T$ | subsets of $\mathbb T$ | n/a | n/a | **UNDEFINED** (RQ-03) | policy | P |
| S-168 | $\mathrm{DD}^{*}$ | Drawdown at which $\vartheta_K$ first falls below 1 (F100) | scalar | n/a | $[0,1)$ | [1] | n/a | n/a | derived | D |
| S-246 | $\vartheta_K$ | Cushion-induced throttle | alias of S-111 | drawdowns | $[0,1]$ | [1] | n/a | n/a | derived | D |
| S-169 | $\zeta$ | Decay rate of the exponential throttle family (comparison only) | scalar | n/a | $\mathbb Q_{>0}$ | [1] | n/a | n/a | comparison | P |
| S-236 | $\mathcal I_k,\ \vartheta^{\mathrm{step}}_k$ | Intervals and levels of a step throttle (comparison only, F103) | set, scalar | $\mathbb N$ | intervals of $[0,\infty)$; $[0,1]$ | [1] | n/a | n/a | comparison | P |
| S-188 | $\mathrm{OC}$ | Register of deliberate conservative over-charges OC-1 … (05 §4) | register | n/a | n/a | n/a | n/a | n/a | policy | P |

### G.1 Policy parameters (components of $\theta$; every value **UNDEFINED — REQUIRES RESOLUTION**, human authority, Art. 16)

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-250 | $f^{\mathrm{trd}}$ | Per-trade stop-risk fraction of $B$ | scalar | n/a | $\mathbb Q$ | [1] | + | $(0,f^{\mathrm{port}}]$ | policy | P |
| S-251 | $f^{\mathrm{port}}$ | Portfolio stop-risk fraction | scalar | n/a | $\mathbb Q$ | [1] | + | $(0,1]$ | policy | P |
| S-252 | $f^{\mathrm{strat}}_s$ | Strategy stop-risk fraction | scalar | $\mathbb S$ | $\mathbb Q$ | [1] | + | $(0,f^{\mathrm{port}}]$ | policy | P |
| S-253 | $f^{\mathrm{gap}}$ | Per-trade gap-risk fraction | scalar | n/a | $\mathbb Q$ | [1] | + | $>0$ | policy | P |
| S-254 | $f^{\mathrm{ord}}$ | Per-order notional fraction | scalar | n/a | $\mathbb Q$ | [1] | + | $>0$ | policy | P |
| S-255 | $f^{\mathrm{conc}}$ | Instrument concentration fraction | scalar | n/a | $\mathbb Q$ | [1] | + | $>0$ | policy | P |
| S-256 | $f^{\mathrm{clu}}$ | Cluster notional fraction | scalar | n/a | $\mathbb Q$ | [1] | + | $>0$ | policy | P |
| S-257 | $f^{\mathrm{clr}}$ | Cluster stop-risk fraction | scalar | n/a | $\mathbb Q$ | [1] | + | $(0,f^{\mathrm{port}}]$ | policy | P |
| S-258 | $\lambda^{\mathrm{gross}}$ | Gross-exposure ratio | scalar | n/a | $\mathbb Q$ | [1] | + | $(0,1]$ under D-02 | policy | P |
| S-259 | $\rho^{\mathrm{in}}$ | Entry participation fraction of ADV | scalar | n/a | $\mathbb Q$ | [1] | + | $(0,1]$ | policy | P |
| S-260 | $w^{\mathrm{in}}$ | Order working window | scalar | n/a | $\mathbb Q$ | [day] | + | $>0$ | policy | P |
| S-261 | $\rho^{\mathrm{ex}}$ | Exit participation fraction of ADV | scalar | n/a | $\mathbb Q$ | [1] | + | $(0,1]$ | policy | P |
| S-262 | $h^{\mathrm{ex}}$ | Maximum exit horizon | scalar | n/a | $\mathbb Q$ | [day] | + | $>0$ | policy | P |
| S-263 | $\varsigma^{\max}$ | Maximum relative spread | scalar | n/a | $\mathbb Q$ | [1] | + | $>0$ | policy | P |
| S-264 | $\ell^{\mathrm{day}},\ \ell^{\mathrm{wk}}$ | Daily / weekly loss fractions | scalar | n/a | $\mathbb Q$ | [1] | + | $(0,1)$ | policy | P |
| S-265 | $d^{\max}$ | Maximum drawdown fraction | scalar | n/a | $\mathbb Q$ | [1] | + | $(0,1)$ | policy | P |
| S-266 | $\eta^{\mathrm{lock}}$ | Profit-lock fraction | scalar | n/a | $\mathbb Q$ | [1] | + | $[0,1)$ | policy | P |
| S-267 | $\nu^{\mathrm{ref}}$ | Profit-lock reference NAV | scalar | n/a | $\mathbb Q$ | [USD/unit] | + | independent of current $W$ | policy | P |
| S-268 | $\mu^{K},\ \mu^{G}$ | Cushion utilisation fractions for stop and gap risk | scalar | n/a | $\mathbb Q$ | [1] | + | $(0,1]$ (T-21) | policy | P |
| S-269 | $n^{\min}$ | Minimum order size | lattice | n/a | $\mathbb L_{\ge0}$ | [sh$_i$] | + | n/a | policy | P |
| S-270 | $\chi$ | Limit-price collar above the ask | scalar | n/a | $\mathbb Q$ | [1] | + | $\ge0$ | policy | P |
| S-271 | $\Gamma^{\min}$ | Policy floor on the gap-stress fraction | scalar | n/a | $\mathbb Q$ | [1] | + | $(0,1]$ | policy | P |
| S-272 | $\ell^{\min}$ | Minimum per-share stop loss as a fraction of the limit price (G7) | scalar | n/a | $\mathbb Q$ | [1] | + | $>0$ | policy | P |
| S-273 | $\kappa^{\min}$ | Policy floor on exit cost as a fraction of the stop price (F111) | scalar | n/a | $\mathbb Q$ | [1] | + | $\ge0$ | policy | P |
| S-274 | $p^{\min},\ p^{\max}$ | Admissible instrument price bounds | scalar | n/a | $\mathbb Q_{>0}$ | [USD/sh$_i$] | n/a | $p^{\min}<p^{\max}$ | policy | P |

## H. Probability, statistics, objectives

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-130 | $\Omega,\ \mathcal F,\ \mathbb P$ | Sample space, σ-algebra (with sub-σ-algebras $\mathcal F_t$), unknown true law | measure space | n/a | n/a | n/a | n/a | existence is A-STAT-00 | postulate | M |
| S-131 | $\mathbb F$ | Decision filtration $(\mathcal F_t)$, $\mathcal F_t$ generated by $\mathsf S_0..\mathsf S_t$ | filtration | $\mathbb T$ | sub-σ-algebras of $\mathcal F$ | n/a | n/a | n/a | definition | M |
| S-132 | $\mathbb G,\ \mathcal G_t$ | Full market filtration and its members | filtration | $\mathbb T$ | sub-σ-algebras | n/a | n/a | $\mathcal F_t\subseteq\mathcal G_t$ | definition | M |
| S-133 | $\xi_{t+1}$ | Exogenous randomness on $(\tau_t,\tau_{t+1}]$ | random element | $\Omega$ | $\Xi$ | n/a | n/a | n/a | model | R |
| S-206 | $\Xi$ | Path space (quote/trade paths, halts, fill outcomes) | set | n/a | n/a | n/a | n/a | n/a | model | M |
| S-134 | $\mathcal P$ | Ambiguity set of laws of $\xi_{t+1}$ ($\mathcal P_t$ at epoch $t$) | set of measures | $\mathbb T$ | sets of laws on $\Xi$ | n/a | n/a | $\mathcal F_t$-measurable; **UNDEFINED — REQUIRES RESOLUTION** (RQ-12) | model | E |
| S-177 | $\mathcal P^{\mathrm{conf}}_t$ | Ambiguity set built to contain the true law with probability $\ge1-\delta^{\mathrm{conf}}$ | set of measures | $\mathbb T$ | sets of laws | n/a | n/a | **UNDEFINED** | model | E |
| S-135 | $z_t,\ \mathcal Z,\ \hat\pi_t$ | Latent regime, regime set, regime posterior | random / set / vector | $\mathbb T$ | $\mathcal Z$; simplex | [1] | n/a | **UNDEFINED — REQUIRES RESOLUTION** | model | R |
| S-136 | $\mathcal L_{t+1}$ | One-period flow-adjusted loss $\mathcal L_{t+1}(a)$ (F008) | random scalar | actions | $\mathbb R$ | [USD] | + loss | n/a | derived from $G$ | R |
| S-137 | $\beta$ | Tail confidence level | scalar | n/a | $(0,1)$ | [1] | n/a | **UNDEFINED — REQUIRES RESOLUTION** | policy | P |
| S-138 | $\mathrm{VaR},\ \mathrm{ES}$ | Value-at-Risk and Expected Shortfall at level $\beta$ (F009–F011) | functional | laws of losses | $\mathbb R\cup\{+\infty\}$ | [USD] | + loss | n/a | definition | M |
| S-139 | $\mathrm{PB}_t$ | Floor-breach probability (F012) | scalar | actions | $[0,1]$ | [1] | + worse | n/a | model | E |
| S-140 | $\mathrm{PoR}$ | Probability of ruin over a horizon (F014) | scalar | n/a | $[0,1]$ | [1] | + worse | ruin definition **UNDEFINED** (RQ-30) | model | E |
| S-230 | $\mathrm{Ruin}$ | Ruin event over a horizon (F014) | event | n/a | $\mathcal F$ | n/a | n/a | n/a | definition | M |
| S-141 | $\mathrm{DaR},\ \mathrm{CDaR}$ | Drawdown-at-risk, conditional drawdown-at-risk (F015) | functional | path laws | $[0,\infty]$ | [1] | + worse | estimation **UNDEFINED** | definition | M |
| S-142 | $\epsilon^{\mathrm{ruin}}$ | Tolerated floor-breach / ruin probability | scalar | n/a | $(0,1)$ | [1] | n/a | **UNDEFINED — REQUIRES RESOLUTION** | policy | P |
| S-143 | $J$ | Optimisation objective $J_t(a)$, $J_{\mathbb Q}(a)$ under law $\mathbb Q$ (F018–F023) | functional | actions | $\mathbb R\cup\{-\infty\}$ | [USD] (arithmetic forms) or [1] (log forms) — declared per candidate | + better | **UNDEFINED — REQUIRES RESOLUTION** (RQ-13) | definition | M |
| S-144 | $\Delta J_t$ | $J_t(a)-J_t(a^{\varnothing})$ (F025) | compound | actions | $\mathbb R\cup\{\pm\infty\}$ | as $J$ | + better | n/a | derived | D |
| S-145 | $\mathrm{LB}_t$ | Certified lower bound on $\Delta J_t(a)$ (F027) | scalar | actions | $\mathbb R\cup\{-\infty\}$ | as $J$ | + | **UNDEFINED — REQUIRES RESOLUTION** (RQ-14) | derived | D |
| S-146 | $\varepsilon^{\mathrm{num}},\ \varepsilon^{\mathrm{stat}},\ \varepsilon^{\min}$ | Certified numerical allowance; statistical allowance; policy margin for advantage | scalar | n/a | $\mathbb Q_{\ge0}$ | as $J$ | n/a | **UNDEFINED — REQUIRES RESOLUTION** | derived / policy | D |
| S-228 | $\delta^{\mathrm{conf}}$ | Confidence parameter of statistical statements | scalar | n/a | $(0,1)$ | [1] | n/a | **UNDEFINED** | policy | P |
| S-147 | $\hat J$ | Numerical estimate of $J$ | scalar | actions | $\mathbb R$ | as $J$ | n/a | n/a | computation | E |
| S-176 | $\hat e,\ \Phi$ | Generic estimate in a snapshot and the estimator map producing it (F003) | scalar, function | admitted data | $\mathbb R$ | as estimated quantity | n/a | NLA rule | statistic | E |
| S-179 | $n^{\log}$ | Log-growth-optimal size (when defined) | lattice | n/a | $\mathbb L_{\ge0}$ | [sh$_i$] | + | T-19 domain | derived | D |
| S-180 | $\varpi,\ \lambda^{\mathrm{ES}},\ \varrho$ | Fractional-Kelly multiplier; mean–ES weight; risk-sensitivity coefficient (preferences; comparison only) | scalar | n/a | $\mathbb Q_{>0}$ | [1] | n/a | $\varpi\in(0,1]$ | comparison | P |
| S-181 | $\mathrm{LB}^{\mathrm{naive}}$ | Difference-of-infima advantage (inadmissible, T-12a) | scalar | actions | $\mathbb R$ | as $J$ | n/a | n/a | derived | D |
| S-221 | $\mathfrak W$ | Wasserstein (optimal-transport) distance between laws | function | pairs of laws | $[0,\infty]$ | as transported quantity | n/a | n/a | definition | M |
| S-222 | $\varepsilon^{W}$ | Wasserstein radius | scalar | n/a | $\mathbb Q_{>0}$ | as $\mathfrak W$ | n/a | **UNDEFINED** (RQ-12) | model | E |
| S-223 | $M^{\mathrm{obs}}$ | Sample size of an empirical law | integer | n/a | $\mathbb N$ | [1] | n/a | n/a | data | O |
| S-224 | $D^{\mathrm{dim}}$ | Dimension of the data vector | integer | n/a | $\mathbb N$ | [1] | n/a | n/a | model | M |
| S-225 | $\hat{\mathbb P}$ | Empirical law (subscript: sample size) | measure | n/a | laws on $\Xi$ | n/a | n/a | n/a | statistic | E |
| S-229 | $\mathcal U$ | Non-decreasing utility function (T-08) | function | $\mathbb R$ | $\mathbb R$ | n/a | + better | non-decreasing | preference | M |
| S-215 | $\sigma^{\mathrm{target}}$ | Target volatility for volatility-targeted sizing (comparison only) | scalar | n/a | $\mathbb Q_{>0}$ | [day$^{-1/2}$] | + | n/a | comparison | P |
| S-216 | $P^{\mathrm{win}},\ \hat P^{\mathrm{win}}$ | Win probability of a two-outcome trade and its estimate (Kelly comparison) | scalar | n/a | $[0,1]$ | [1] | n/a | n/a | model / estimate | E |
| S-217 | $b^{\mathrm{K}}$ | Payoff ratio (win per unit risked) in the Kelly formula | scalar | n/a | $\mathbb Q_{>0}$ | [1] | n/a | n/a | model | E |
| S-218 | $f^{\mathrm{K}}$ | Kelly fraction of wealth risked (F131) | scalar | n/a | $\mathbb Q$ | [1] | + | may be $\le0$ | derived | D |
| S-219 | $n^{\mathrm{pos}}$ | Number of open positions (correlation-multiplier comparison) | integer | $\mathbb T$ | $\mathbb N$ | [1] | n/a | n/a | derived | D |
| S-220 | $\hat{\bar\rho}$ | Estimated average pairwise correlation (comparison only) | scalar | $\mathbb T$ | $[-1,1]$ | [1] | n/a | n/a | statistic | E |
| S-226 | $\epsilon^{\mathrm{tol}}$ | A numerical tolerance (forbidden in hard checks, 01 §9.7) | scalar | n/a | $\mathbb Q_{>0}$ | as compared quantity | n/a | n/a | notation | M |
| S-227 | $\epsilon^{\mathrm{mix}}$ | Mixture weight in the T-19 construction | scalar | n/a | $(0,1)$ | [1] | n/a | n/a | notation | M |
| S-233 | $\varphi$ | Convex generator of a φ-divergence ambiguity set | function | $\mathbb R_{\ge0}$ | $\mathbb R_{\ge0}$ | [1] | n/a | convex, $\varphi(1)=0$ | model | M |

## I. Decision objects

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-150 | $x_t$ | State vector (F004) | tuple | $\mathbb T$ | product space | mixed | n/a | n/a | $\mathsf S_t$ | D |
| S-207 | $x^{A},\ x^{P},\ x^{M},\ x^{H},\ x^{B},\ x^{U}$ | State blocks: authority, portfolio, market, history, budget ledger, uncertainty | tuple | $\mathbb T$ | product spaces | mixed | n/a | n/a | $\mathsf S_t$ | D |
| S-151 | $\mathcal D$ | Decision function (F006) | function | $\mathfrak S\times\mathcal O\times\Theta\times\mathcal V$ | $\mathfrak D$ | n/a | n/a | pure, total | engine | D |
| S-152 | $\mathsf{RD}_t$ | Risk-decision record | record | $\mathbb T$ | $\mathfrak D$ | n/a | n/a | schema **UNDEFINED — REQUIRES RESOLUTION** | engine | D |
| S-153 | $\mathsf{rc}$ | Reason-code set | set | n/a | subsets of codes | n/a | n/a | list **UNDEFINED — REQUIRES RESOLUTION** | engine | D |
| S-208 | $G$ | Wealth-transition map $W_{t+1}=G(W_t,x_t,a_t,\xi_{t+1})$ (F055) | function | $\mathbb Q\times$ states × actions × $\Xi$ | $\mathbb Q$ | [USD] | + | n/a | identity | D |

## J. Auxiliary and derived-notation symbols

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-160 | $\mathbf 1_i$ | Unit vector of instrument $i$ | vector | $\mathbb I$ | $\mathbb L^{N_t}$ | [1] | n/a | n/a | notation | M |
| S-161 | $\mathcal A^{(0)},\ \mathcal A^{(1)},\ \mathcal A^{(2)},\ \mathcal A^{(3)},\ \mathcal A^{(4)},\ \mathcal A^{(5)}$ | Action sets admitted by authority layers 0 … 5 (F002) | sets | states | subsets of $\mathbb L^{N}$ | n/a | n/a | nested | derived | D |
| S-162 | $\mathcal K$ | Index set of hard constraints H1–H16 | set | n/a | subsets of IDs | n/a | n/a | n/a | policy | P |
| S-163 | $\mathrm{Gates}$ | Set of zero–one gates G1–G11 (F092) | set | n/a | predicates | n/a | n/a | n/a | policy | P |
| S-234 | $\Upsilon$ | Generic predicate (a gate, or a model constraint in T-09) | predicate | states | $\{0,1\}$ | n/a | n/a | n/a | notation | M |
| S-170 | $\mathcal M_{t+1}$ | Market ("paper") component in ECAI (F058) | random scalar | $\mathbb T$ | $\mathbb Q$ | [USD] | + profit | n/a | derived | R |
| S-171 | $\pi^{\mathrm{ref}}_{j,k}$ | Cost-decomposition chain | alias of S-082 | $\mathcal J\times\mathbb N_0$ | $\mathbb Q_{>0}$ | [USD/sh$_i$] | n/a | n/a | derived | D |
| S-173 | $\nu^{\star}$ | Reference NAV per unit $\nu^{\mathrm{R}}$ (F146) at the instant of an external flow (F069) | scalar | flows | $\mathbb Q$ | [USD/unit] | n/a | timing **UNDEFINED** (RQ-31) | derived | D |
| S-174 | $W^{\min}$ | Worst-case next-period wealth under tier U, $W^{\min}_{t+1}(a)$ (F070) | scalar | actions | $\mathbb Q$ | [USD] | + | $\mathcal F_t$-measurable | derived | D |
| S-175 | $\Delta$ | First difference prefix: $\Delta y_{t+1}=y_{t+1}-y_t$ | operator | sequences | sequences | as operand | n/a | n/a | notation | M |
| S-178 | $a^{\star}_t$ | Optimiser proposal / argmax (F017) | vector | $\mathbb T$ | $\mathbb L^{N_t}$ | [sh$_i$] | n/a | verified before use | optimiser | D |
| S-182 | $\mathcal W^{\mathrm{S}},\ \mathcal W^{\mathrm{G}},\ \mathcal W^{\mathrm{U}}$ | Disturbance sets of tiers S, G, U (outcomes consistent with the tier's hypotheses, bounds attainable) | set | n/a | subsets of $\Xi$ | n/a | n/a | n/a | definition | M |
| S-183 | $\mathbb E$ | Expectation (subscript: law) | operator | random variables | $\mathbb R\cup\{\pm\infty\}$ | as operand | n/a | integrability | mathematics | M |
| S-185 | $\bar A_{t+1}$ | $\mathcal F_t$-measurable upper bound on $\mathrm{Accr}_{t+1}$ | scalar | $\mathbb T$ | $\mathbb Q_{\ge0}$ | [USD] | + | n/a | derived | D |
| S-186 | $\ell,\ \ell_k$ | Per-share consumption when a constraint is linear ($g_k(n)=n\ell_k$); unindexed in worked examples | scalar | $\mathcal K$ | $\mathbb Q$ | [USD/sh$_i$] | + | $>0$ for sizing | derived | D |
| S-187 | $\tau^{\mathrm{CA}},\ \psi$ | Instant of a corporate action; split ratio of the value-neutral restatement (F054) | timestamp, scalar | corporate actions | instants; $\mathbb Q_{>0}$ | [T]; [1] | n/a | n/a | reference data | O |

## K. Project-specific operators

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-231 | $\mathbb 1$ | Indicator of an event or condition | operator | events | $\{0,1\}$ | [1] | n/a | n/a | mathematics | M |
| S-232 | $\sigma$ | Generated σ-algebra $\sigma(\cdot)$ | operator | random elements | σ-algebras | n/a | n/a | n/a | mathematics | M |
| S-237 | $\operatorname{sgn}$ | Sign function | operator | $\mathbb Q$ | $\{-1,0,1\}$ | [1] | n/a | n/a | mathematics | M |
| S-238 | $\mathrm{RN}$ | Round-to-nearest in IEEE-754 binary64 | operator | $\mathbb R$ | binary64 values | as operand | n/a | no overflow/underflow | IEEE 754 | M |
| S-239 | $\lfloor\cdot\rfloor_{\mathbb L}$ | Floor to the quantity lattice (F097) | compound operator (floor with lattice $\mathbb L$) | $\mathbb Q$ | $\mathbb L$ | [sh$_i$] | n/a | n/a | definition | M |

## L. Worked-example and brief-name symbols

| ID | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|
| S-240 | $R$ | Generic scalar risk budget in worked examples and in the brief's naive formula | scalar | n/a | $\mathbb Q$ | [USD] | + | n/a | example | M |
| S-241 | $p$ | Generic price per share in worked examples and dimension checks | scalar | n/a | $\mathbb Q_{>0}$ | [USD/sh$_i$] | n/a | n/a | example | M |
| S-242 | $R_{\mathrm{hard}}$ | The brief's naive budget "Equity × maximum risk fraction" (F110; disproved as sufficient) | scalar | n/a | $\mathbb Q$ | [USD] | + | n/a | brief | M |
| S-243 | $Q_{\mathrm{risk}},\ Q_{\mathrm{notional}},\ Q_{\mathrm{liquidity}},\ Q_{\mathrm{BP}},\ Q_{\mathrm{margin}},\ Q_{\mathrm{portfolio}},\ Q_{\mathrm{correlation}},\ Q_{\mathrm{gap}},\ Q_{\mathrm{concentration}}$ | The brief's cap names, mapped to constraint families in 06 §6 | lattice | n/a | $\mathbb L_{\ge0}$ | [sh$_i$] | + | n/a | brief | M |

## M. Proof-local namespaces (valid only inside the named theorem block of 08)

| ID | Scope | Symbol | Meaning | Type | Domain | Codomain | Units | Sign | Valid range | Source | Class |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S-280 | 08:T-11 | $\mathrm{Av},\ \mathrm{Rs},\ \mathrm{Op},\ \mathrm{Tot}$ | Ledger components: available, reserved, open, total budget of one family | scalar | ledger states | $\mathbb Q$ | [USD] | + | $\mathrm{Av}\ge0$ | ledger model | M |
| S-281 | 08:T-12a | $J^{(1)},\ J^{(2)}$ | Two generic families indexed by laws in T-12a | function | $\mathcal P$ | $\mathbb R$ | as $J$ | n/a | finite infima | notation | M |
| S-282 | 08:T-12b | $\varepsilon^{\mathrm{err}}$ | Error bounds $\varepsilon^{\mathrm{err}}_a$, $\varepsilon^{\mathrm{err}}_0$ in T-12b | scalar | n/a | $\mathbb Q_{\ge0}$ | as $J$ | n/a | n/a | notation | M |
| S-283 | 08:T-22 | $A,\ D$ | Integer numerators $A_R, A_\ell$ and denominators $D_R, D_\ell$ of $R$ and $\ell$ | integer | n/a | $\mathbb N$ | [1] | + | n/a | notation | M |
| S-284 | 08:T-22 | $q^{*},\ q^{\mathrm{fl}}$ | Exact lattice count $R/(\delta_q\ell)$ and its binary64 evaluation (dimensionless: $\delta_q$ carries the share unit) | scalar | n/a | $\mathbb Q$ | [1] | + | $<2^{53}$ | notation | M |
| S-285 | 08:T-22 | $\varepsilon^{\mathrm{rd}},\ \epsilon^{\mathrm{mach}}$ | Relative rounding errors $\varepsilon^{\mathrm{rd}}_{1..3}$; unit roundoff $2^{-53}$ | scalar | n/a | $\mathbb R$ | [1] | n/a | $\lvert\varepsilon^{\mathrm{rd}}\rvert\le\epsilon^{\mathrm{mach}}$ | IEEE 754 | M |
| S-286 | 08:T-24 | $\hat g,\ \hat b,\ \hat Q$ | Rounded consumption, budget and cap (hats here mean "rounded", not "estimated") | function / scalar | as $g_k,b_k,Q_k$ | $\mathbb Q$ | as unrounded | + | n/a | notation | M |
| S-287 | 08:T-03 | $\bar g$ | Monotone upper envelope of a non-monotone consumption (F127) | function | $\mathbb L_{\ge0}$ | $\mathbb Q$ | as $g_k$ | + | n/a | notation | M |

## N. Registry-level open items

1. $W_t$ depends on the liquidation-cost model $\Lambda$ (S-041). The floor $\Lambda^{\mathrm{floor}}$ (F111) makes $W$ conservative with respect to
   an optimistic model, but $\Lambda$ itself remains **UNDEFINED — REQUIRES RESOLUTION** (RQ-05).
2. The brief's "entry" is split into three objects: arrival mid $m^{\mathrm{arr}}$ (accounting reference), limit $p^{\mathrm{lim}}$ (worst-case entry for
   safety), realised fill $p^{\mathrm{fill}}_j$ / $p^{\mathrm{in}}$ (ex post).
3. The brief's "equity" and "wealth" are distinct: $E_t$ (mark-to-mid) vs $W_t$ (net liquidation). The safety layer uses $W_t$.
4. The brief's "execution risk" is represented by $\mathrm{ER}(n)$, A-STOP, A-TRIG, A-GAP and $e$, not by one scalar.
5. Renames in v0.2 (AUD-007), old notation in code font: `n_j`→$n^{\mathrm{fill}}_j$, `f_j`→$p^{\mathrm{fill}}_j$, `f^in`/`f^out`→$p^{\mathrm{in}}$/$p^{\mathrm{out}}$,
   `tau_j`→$\tau^{\mathrm{fill}}_j$, `r_{j,k}`→$\pi^{\mathrm{ref}}_{j,k}$, `c_{j,k}`→$\mathcal C_{j,k}$, `m_K`/`m_G`→$\mu^{K}$/$\mu^{G}$, `delta`→$\delta^{\mathrm{conf}}$,
   `P_{t,delta}`→$\mathcal P^{\mathrm{conf}}_t$, Wasserstein `W_p`→$\mathfrak W$, `T_H`→$T^{\mathrm{hor}}$, `W_S`→$\mathcal W^{\mathrm{S}}$, `h`→$\mathrm{hash}$, italic
   DD/MDD/BP/PB/IM/MM → upright, policy `pi_t`→$\mathcal D$.
