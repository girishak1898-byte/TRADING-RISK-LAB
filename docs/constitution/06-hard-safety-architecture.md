# 06 — Candidate Deterministic Hard-Safety Architecture (v0.2-draft)

Status: DRAFT. Structure is PROVISIONAL; all parameter **values** are **UNDEFINED — REQUIRES RESOLUTION** (human policy).
Scope assumed: v0 long-only, cash account, US-listed equities/ETFs, limit-price entries (decisions D-01..D-05 in 04 — not yet
taken). Theorem references point to [08](08-theorem-register.md); formula IDs to [14](14-formula-registry.md); assumption IDs to [04](04-assumption-and-decision-registry.md).

v0.2 changes (review corrections): tier table aligned with T-10 (AUD-004); §3 lattice-correct naive form (AUD-031) and H14 reference
(AUD-005); hard-layer input floors (AUD-002); H3 fail-closed rule (AUD-028); consumption/budget split wording (AUD-026); G11 in the
evaluation order (AUD-025); assumption IDs per constraint (AUD-016); formula tags (AUD-010); symbol renames (AUD-007, AUD-009).

---

## 1. What "deterministic" means here

The hard envelope is **deterministic in computation**: an exact, pure function of authoritative inputs and policy constants.
Its **protective meaning is conditional**: each constraint guarantees a wealth outcome only under a named assumption about
the world. Conflating the two is the central error this architecture is designed to prevent (T-17a, T-17b).

## 2. Guarantee tiers (aligned with T-10 in v0.2)

Common hypotheses of every floor tier (T-10): A-MATH-01, A-SCOPE-03 (long-only), A-SCOPE-05 with gate G11 (one exposure per
instrument), A-FLOW-01 ($X_{t+1}=0$ inside the period), A-ACC-01…04, A-ACC-06 ($\Lambda\ge0$), A-ACC-07 ($\mathrm{Fin}=\mathrm{Accr}=0$, $\mathrm{Inc}\ge0$),
A-MKT-05 (every entry fill $\le p^{\mathrm{lim}}$), A-EXE-01, A-EXE-02, A-EXE-03 (cumulative fill $\le$ order quantity), A-EXE-04 (fees on cumulative
filled quantity, booked into $W$ at the fill or later; owed fees reserved until booked, F148), A-EXE-05 (no other orders), A-AUTH-02 (complete
ledger, including each pending order's filled quantity and fees booked, and terminal entry orders whose fees are not final),
A-AUTH-04 (snapshot and ledger form one cut); reservations and partially filled orders charged by F144 and F145 (per-share distances clamped
at $0$); an exposure without an authoritative stop charged $u^{\mathrm{open}}$ (D-06) and covered in every tier by the tier-U bound (A-MKT-01, A-ACC-05).

| Tier | Guarantee holds if, in addition … | Constraint family | Assumption strength |
|---|---|---|---|
| **U** — unconditional | prices $\ge0$ (A-MKT-01); position-level tier-U exit value $\mathrm{XV}_i\ge-\phi^{\mathrm{sell}}_{i,0}(q^{\mathrm{exp}}_i)$ (A-ACC-05, F072); ledger/custody integrity (A-AUTH-01) | notional, gross, concentration, buying power, absolute-loss cushion H16 | weakest (structural facts for long cash equities) |
| **S** — stop | position-level exit-value bound $\mathrm{XV}_i\ge q^{\mathrm{exp}}_i(p^{\mathrm{stop}}_i-\kappa^{\mathrm{out}}_i(q^{\mathrm{exp}}_i))-\phi^{\mathrm{sell}}_i(q^{\mathrm{exp}}_i)$ (A-TRIG, F072, at the $\tau_t$ inputs), for which A-STOP, A-STOPLIVE, A-EXE-04, at most $N^{\mathrm{ex}}$ exit orders per exposure with $\phi^{\mathrm{split}}$ (F140), and a remainder at the cut valued no lower than its stop bound are sufficient (04 A-TRIG); the remainder's valuation uses the estimate $\hat\Lambda_{t+1}$, so the bound has a model component (AUD-048) | stop-risk budgets ($R$-family) | strong; **known to fail** in gaps and halts |
| **G** — gap stress | position-level bound with exit price $p^{\mathrm{gx}}=\min((1-\Gamma_i)p^{\mathrm{stop}},p^{\mathrm{stop}}-\kappa^{\mathrm{out}})$ (A-GAP, F060, F072) | gap-risk budgets ($G$-family) | medium; fails beyond the stress level |
| **L** — liquidity proxy | future tradable volume is not below the policy fraction of trailing ADV (A-LIQ, A-MKT-06) | participation and exit-horizon caps | medium; fails in liquidity collapse |

A decision record MUST state, for the chosen quantity, which tiers' constraints were **binding** and which tiers are
**guaranteed** (all constraints of a tier satisfied).

## 3. Why $R_{\mathrm{hard}}=\text{Equity}\times f^{\mathrm{trd}}$ is not sufficient (derivation)

Take $R_{\mathrm{hard}}=E_t\,f^{\mathrm{trd}}$ and size $Q=\delta_q\lfloor R_{\mathrm{hard}}/(\delta_q\ell^{\mathrm{stop}})\rfloor$ with $\ell^{\mathrm{stop}}$ the stop distance only
**[F110]**. (v0.2: the brief's form $\lfloor R/\ell\rfloor$ applies $\lfloor\cdot\rfloor$ to a share-dimensioned quantity and is valid only for
$\delta_q=1$ sh; AUD-031, 03 E-18.) Each item below is a counterexample or a missing term; together they determine the structure of §4–§6.

| # | Defect | Counterexample | Consequence for the design |
|---|---|---|---|
| 1 | Uses mark-to-mid equity $E$, not liquidation wealth $W$ | Illiquid holding: $E$ overstates exitable wealth by $\Lambda$ | base budgets on $W$ |
| 2 | Ignores open risk and reservations | Two opportunities evaluated from the same snapshot each receive the full $R_{\mathrm{hard}}$; aggregate $2R_{\mathrm{hard}}$ | aggregate budgets with $R^{\mathrm{open}}+R^{\mathrm{res}}$ (H2–H4) and snapshot-bound decisions (T-11) |
| 3 | Ignores capital floors | $k$ consecutive full stop-outs: $E$ after $k$ losses is $E_t(1-f^{\mathrm{trd}})^k$ and crosses any floor $F>0$ for $k>\log(F/E_t)/\log(1-f^{\mathrm{trd}})$ (F110) | cushion constraint H4 |
| 4 | Stop distance is not a loss bound | $E=100{,}000$, $f^{\mathrm{trd}}=1\%$, stop $0.01$ below $50$, $\delta_q=1$ sh: $Q=100{,}000$ sh $=5{,}000{,}000$ notional; a $5\%$ gap loses $\approx250{,}000\approx2.5E$ | gap budget H5–H6 and notional caps H7–H11 (T-17a) |
| 5 | No liquidity bound | Same example: order may exceed daily volume of the instrument | H12–H13 |
| 6 | No cash bound | Notional can exceed buying power | H14 (v0.2: was mis-cited as H15, AUD-005) |
| 7 | Sign | $E\le0$ ⇒ $R_{\mathrm{hard}}\le0$ ⇒ the floor is negative, readable as a sell / short | clamp $(\cdot)^+$ (T-01) |
| 8 | Non-linear fees | Minimum commission: the naive form with a per-share fee added to $\ell^{\mathrm{stop}}$ can exceed $R_{\mathrm{hard}}$ (08 T-02N: $22$ sh, loss $4.20>2.50$) | define $Q_k$ by exact monotone search (T-02) |
| 9 | Rounding / float | Half-up and binary64 overshoots (observed, 01 §9) | directed rounding, exact arithmetic (T-22, T-24) |
| 10 | Entry reference | $\ell^{\mathrm{stop}}$ from mid while fill is at limit: realised risk exceeds budget by $n(p^{\mathrm{lim}}-m)$ | use $p^{\mathrm{lim}}$ as worst-case entry (DC-1, T-11) |

Conclusion: the single-scalar form $0\le R^{\mathrm{allow}}\le R^{\mathrm{hard}}$ is **necessary but not sufficient**. The invariant
must be vector-valued over every constraint family (Art. 5).

## 4. Budgets

**Risk base** $B_t$: **UNDEFINED — REQUIRES RESOLUTION** (RQ-02). Candidates **[F073]** and properties:

| Candidate | Non-decreasing in $W_t$ (needed by T-05) | $B_t\le W_t$ | Intraday procyclicality | Note |
|---|---|---|---|---|
| B1: $W_t$ | yes | yes | high (budgets rise with intraday gains) | simplest |
| B2: $\min(W_t,\ \nu^{\mathrm{day}}_0U_t)$ | yes | yes | gains do not raise budgets intraday; losses reduce them | conservative |
| B3: $K_t$ | yes (T-05) | yes if $F_t\ge0$ | follows cushion | merges sizing with floor; fractions then mean "of cushion" |
| B4: $\nu^{\mathrm{day}}_0U_t$ | yes (constant intraday) | **no** | none | violates $B\le W$ after intraday loss; H11 must then use $W_t$ directly |

**Hard stop-risk budget** (all $R$-family constraints have the form $L^{\mathrm{stop}}(n)\le b$, so they collapse to one scalar):

$$
R^{\mathrm{hard}}_t=\Big(\min\big\{\,f^{\mathrm{trd}}B_t,\ \ f^{\mathrm{port}}B_t-R^{\mathrm{open}}_t-R^{\mathrm{res}}_t,\ \ f^{\mathrm{strat}}_sB^{\mathrm{win}}_s-R^{\mathrm{open}}_{s,t}-R^{\mathrm{res}}_{s,t}-\mathrm{SL}_{s,t},\ \ f^{\mathrm{clr}}B_t-R^{\mathrm{open}}_{c,t}-R^{\mathrm{res}}_{c,t},\ \ \mu^{K}K_t-R^{\mathrm{open}}_t-R^{\mathrm{res}}_t\,\big\}\Big)^{+}
$$
[F074]

with $s$ the opportunity's strategy and $c=\mathrm{cl}(i)$. The strategy term uses the risk base at the start of the strategy's loss window,
$B^{\mathrm{win}}_s$, so a realised strategy loss enters once, through $\mathrm{SL}_{s,t}$, not again through a falling $B_t$ (closure, AUD-035).

**Fail-closed rule for $\mathrm{SL}_{s,t}$ (v0.2, AUD-028).** $\mathrm{SL}_{s,t}$ is **UNDEFINED** (RQ-11). Until it is defined, the strategy term of F074
(and H3) is omitted **only** if the human policy explicitly disables strategy budgets (policy flag "strategy budgets = OFF", recorded in
$\mathsf v$); otherwise every decision is NO\_TRADE with reason STRATEGY\_LOSS\_UNDEFINED (Art. 4). Omitting the term silently, or
setting $\mathrm{SL}_{s,t}=0$, is forbidden (UNKNOWN ≠ ZERO).

**Hard gap-risk budget:**

$$
G^{\mathrm{hard}}_t=\Big(\min\big\{\,f^{\mathrm{gap}}B_t,\ \ \mu^{G}K_t-G^{\mathrm{open}}_t-G^{\mathrm{res}}_t\,\big\}\Big)^{+}
$$
[F075]

**Model tightening** (Art. 5): $b^{\mathrm{allow}}_k=\min\big((b^{\mathrm{hard}}_k)^+,\ \mathfrak s(b^{\mathrm{mod}}_k)\big)$ for every $k$ — every hard budget is clamped at $0$,
since some can be negative (e.g. H14 when $C^{\mathrm{res}}_t>C^{\mathrm{avail}}_t$; closure, AUD-047); in particular
$R^{\mathrm{allow}}_t=\min(R^{\mathrm{hard}}_t,\mathfrak s(R^{\mathrm{mod}}_t))$ **[F049]**, with the sanitiser $\mathfrak s$ of F047 (invalid model output: $0$ if the
model is REQUIRED, no constraint if OPTIONAL). The REQUIRED/OPTIONAL flag of each model is policy.

**Unification of floors.** Daily, weekly, drawdown, absolute and profit-lock limits are all expressed as floors on $W$ and enter
through the single cushion $K_t=W_t-F_t$ **[F044]**, $F_t=\max(F^{\mathrm{abs}},F^{\mathrm{dd}}_t,F^{\mathrm{day}}_t,F^{\mathrm{wk}}_t,F^{\mathrm{lock}}_t)$ **[F043]**, with
$F^{\mathrm{day}}_t=(1-\ell^{\mathrm{day}})\nu^{\mathrm{day}}_0U_t$ and $F^{\mathrm{wk}}_t=(1-\ell^{\mathrm{wk}})\nu^{\mathrm{wk}}_0U_t$ **[F041]**, where $\nu^{\mathrm{day}}_0,\nu^{\mathrm{wk}}_0$ are reference NAVs (F146, §7).
The daily limit is therefore enforced *prospectively* ("even if every open stop is hit today, $W\ge F^{\mathrm{day}}$"), not after the
fact on realised P&L (DC-4). Whether charging *pre-existing* open risk against today's floor is intended policy is **UNDEFINED —
REQUIRES RESOLUTION** (RQ-32); it is the conservative reading.

## 5. Constraint catalogue (single long opportunity on instrument $i$, candidate size $n$)

**Consumption and budget (v0.2 wording, AUD-026).** Each constraint is written $g_k(n)\le b_k$ where $g_k$ is the **new order's** consumption,
with $g_k(0)=0$ and $g_k$ non-decreasing in $n$ under A-EXE-01/02 — this is what makes T-02/T-03 apply. Terms describing **existing**
exposure (held positions, reservations, realised loss) belong to $b_k$: e.g. H8 reads $g_k(n)=n\,p^{\mathrm{lim}}$, $b_k=f^{\mathrm{conc}}B_t-q_{i,t}m_{i,t}-N^{\mathrm{res}}_{i,t}$.
Existing exposure uses the current mark; the new order uses $p^{\mathrm{lim}}$. Open-risk terms carry no $\Lambda$ credit (DC-5, OC-1).
Aggregates: $R^{\mathrm{open}}_t=\sum_ir^{\mathrm{open}}_{i,t}$, $G^{\mathrm{open}}_t=\sum_ig^{\mathrm{open}}_{i,t}$, $Z^{\mathrm{open}}_t=\sum_iu^{\mathrm{open}}_{i,t}$, $N^{\mathrm{open}}_t=\sum_i\lvert q_{i,t}\rvert m_{i,t}$ **[F050]**;
available buying power $\mathrm{BP}^{\mathrm{avail}}_t=\min(\mathrm{BP}_t,\ C^{\mathrm{avail}}_t-C^{\mathrm{res}}_t)$ **[F048]** — pending cash is deducted once, from own
ledger cash, and the broker figure can only restrict (closure: the former form double-deducted when $\mathrm{BP}$ nets open orders, AUD-035).
**Reservations in budgets (closure form, REV-028, AUD-034).** Every reservation component is re-evaluated at $\tau_t$ from the order state —
current F111 inputs, fee schedule and stop, total quantity $n'_o$ ordered, cumulative fill $q^{\mathrm{fill}}_o$, unfilled remainder $q^{\mathrm{unf}}_o=n'_o-q^{\mathrm{fill}}_o$, fees already booked into $W_t$, $\phi^{\mathrm{paid}}_o$ (F148) **[F144]** — and an instrument whose
order is partially filled is charged the exact exposure charge $r^{\mathrm{pf}}_i,g^{\mathrm{pf}}_i,u^{\mathrm{pf}}_i$ **[F145]** (05 §5) instead of open risk plus a reservation.
Its held part uses the held quantity $q_{i,t}$ and its pending part the unfilled remainder $q^{\mathrm{unf}}_o$; exited shares are in neither. A state outside
$0\le q_{i,t}\le q^{\mathrm{fill}}_o\le n'_o$, or with a quantity missing or off the lattice, gives $\alpha_t=0$ and the fail-closed charge of F150 — a finite upper
charge when every quantity is well formed, otherwise no finite charge (RECOVERY); never $0$, never a quantity inferred from another (CLOSURE-REV-006).
The per-share distance of the unfilled part, $p'^{\mathrm{lim}}-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(\bar q_i)$ (and $p'^{\mathrm{lim}}-p^{\mathrm{gx}}_i(\bar q_i)$), is clamped at $0$: G7 checks the stop
only when the order is placed, and a stop trailed to or above the limit afterwards made the unclamped charge negative (third review:
$W_{t+1}=F_t-29$ at `f37c1b6`; AUD-039). An order is pending until it is venue-confirmed terminal (AUD-050). $\phi^{\mathrm{paid}}_o$ is the part of the
order's entry fees booked into $W_t$ (F148); a venue-confirmed terminal entry order whose fees are not yet final stays in the order state with the
reservation $r=g=u=C^{\mathrm{res}}=\phi^{\mathrm{owed}}_o$ until the fees are booked or confirmed final, so an owed fee is never dropped (CLOSURE-REV-003, T-29).
Ledger values are not engine inputs. A reservation computed with older inputs (or before a stop was widened) would under-charge the order
(08 T-10N: floor breached by $40$); a full-order reservation kept beside the held part's open risk would charge realised entry fees and the
filled quantity's risk twice (05 §4a, OC-4 eliminated).

**Hard-layer inputs (v0.2, AUD-002; 01 Art. 6).** The inputs through which a model could enlarge a cap are bounded by policy in the
conservative direction and computed by frozen, versioned estimators under human authority **[F111]**:
$\kappa^{\mathrm{out}}=\max(\kappa^{\min}p^{\mathrm{stop}},\hat\kappa^{\mathrm{out}})$; $\Gamma_i=\max(\Gamma^{\min},\hat\Gamma_i)$;
$\Lambda_{i,t}=\max(\Lambda^{\mathrm{floor}}_{i,t},\hat\Lambda_{i,t})$ with $\Lambda^{\mathrm{floor}}_{i,t}=q_{i,t}\varsigma_{i,t}/2+\phi^{\mathrm{sell}}_i(q_{i,t})$;
$\mathrm{ADV}_{i,t}=\min(\mathrm{ADV}^{\mathrm{est}}_{i,t},\mathrm{ADV}^{\max}_i)$ with $\mathrm{ADV}^{\mathrm{est}}$ from a frozen estimator whose version is part of $\mathsf v$ and $\mathrm{ADV}^{\max}_i$ a policy cap
(closure, AUD-040: without it H13 grew from $500$ to $1{,}000{,}000$ sh as the estimate went from $5{,}000$ to $10^7$). Each $Q_k$ is non-increasing in
$\kappa^{\mathrm{out}},\Gamma_i,\Lambda$ and non-decreasing in ADV (T-07, T-08), so an optimistic estimate can at most reach the cap's value at the policy
bound; an advanced model may only propose $b^{\mathrm{mod}}_k$ (F049). A statistical cluster map may only merge clusters of the human-set map
$\mathrm{cl}$ (S-006): merging never lowers a cluster aggregate, splitting could enlarge H9, H10. Metamorphic obligation (restated at closure; the
former "an arbitrarily optimistic estimate never increases $Q^{\mathrm{hard}}$" was false: H1 with $f^{\mathrm{trd}}B=1{,}000$, limit $50$, stop $49$, $\kappa^{\min}=0.001$ gives
$666$ sh at $\hat\kappa^{\mathrm{out}}=0.5$ and $953$ at $\hat\kappa^{\mathrm{out}}=0$): $Q^{\mathrm{hard}}$ with any estimates $\le Q^{\mathrm{hard}}$ with every estimated input at its policy
bound (testable invariant of T-01). A **missing** estimate ($\hat\kappa^{\mathrm{out}},\hat\Gamma,\hat\Lambda$ or $\mathrm{ADV}^{\mathrm{est}}$) gives $\alpha_t=0$: the policy bound is the
most permissive admissible value, so using it on an outage would loosen the caps (closure, AUD-041; Art. 4; UNKNOWN ≠ SAFE).

**Input classification and independence from models (closure, §5a).** Every input of every hard cap and gate is one of: AUTHORITATIVE
DETERMINISTIC INPUT (ledger, execution reports, versioned policy and reference data), EXTERNAL OBSERVATION (quotes, trading status, event
flags, broker figures), STATISTICAL ESTIMATE (frozen, versioned estimators of admissible historical data, Art. 6 amendment), MODEL OUTPUT,
OPTIMISER OUTPUT. The order parameters of the opportunity ($i,d,s,p^{\mathrm{lim}},p^{\mathrm{stop}}_o$) are the *action being evaluated*: they select the point at
which the deterministic function $Q^{\mathrm{hard}}$ is evaluated and do not change that function.

| Input | Class | Enters | Effect on caps |
|---|---|---|---|
| $q_{i,t}$, $C_t$, $Y_t$, pending orders ($n'_o,p'^{\mathrm{lim}}$, stop, $q^{\mathrm{fill}}_o$, $\phi^{\mathrm{paid}}_o$), live stops $p^{\mathrm{stop}}_i$, $\mathrm{SL}_{s,t}$, $B^{\mathrm{win}}_s$ | AUTHORITATIVE | $W,K,B$, F050, F144, F145, H3, H8–H16 | defines the state |
| $\theta$ (all fractions, $\mu^K,\mu^G$, $d^{\max}$, $\Gamma^{\min},\kappa^{\min},\ell^{\min}$, $\chi$, $n^{\min}$, $\bar N,\bar M$, $p^{\min},p^{\max}$, $F^{\mathrm{abs}}$, $N^{\mathrm{ex}}$), fee schedules $\phi$, cluster map $\mathrm{cl}$, $\mathrm{ADV}^{\max}_i$, calendar | AUTHORITATIVE (human-set, versioned) | every budget and gate | defines the envelope |
| quotes $p^{\mathrm{bid}},p^{\mathrm{ask}}$ (hence $m,\varsigma$), $\mathrm{st}_i$, $\mathrm{ev}_i$, corporate actions | EXTERNAL OBSERVATION | $W$, open risks, G2, G5, G6, G8, G10 | state of the world; gates only block |
| $\mathrm{BP}_t$ | EXTERNAL OBSERVATION | F048 only through $\min(\cdot)$ | **restrictive only** |
| $\hat\kappa^{\mathrm{out}},\hat\Gamma_i,\hat\Lambda_i$ | STATISTICAL ESTIMATE | only through $\max$ with a policy floor (F111); never in a gate predicate (G7 uses $\kappa^{\min}$) and never in a carried reference (F146) | every cap is non-increasing in $\kappa^{\mathrm{out}},\Gamma_i,\Lambda$ (T-08), no gate passes at a larger estimate where it fails at a smaller one (T-27), and no estimate is stored for a later epoch (T-28): **restrictive only**, at every epoch |
| carried references $H_t$, $\nu^{\mathrm{day}}_0$, $\nu^{\mathrm{wk}}_0$, $U_t$ | DERIVED from AUTHORITATIVE state ($E_u$, flows), EXTERNAL OBSERVATION (spread) and POLICY (fee schedule) through $W^{\mathrm{R}}=E-\Lambda^{\mathrm{floor}}$ (F146) | floors F040–F042, bases B2, B4, G4 | identical for every estimate path; at least as high as with any estimate (floors at least as high): **estimate-free** (T-28; CLOSURE-REV-002) |
| $\phi^{\mathrm{paid}}_o$, $q^{\mathrm{fill}}_o$, fee-final confirmation | AUTHORITATIVE (order state, A-AUTH-02) | F144, F145, F148, F150 | domain-checked ($0\le\phi^{\mathrm{paid}}_o\le\phi^{\mathrm{acc}}_o$, else $\alpha_t=0$, no credit); owed fees reserved until booked (CLOSURE-REV-003); quantity state checked ($0\le q_{i,t}\le q^{\mathrm{fill}}_o\le n'_o$ on the lattice, else $\alpha_t=0$ and the F150 charge; CLOSURE-REV-006) |
| $\mathrm{ADV}^{\mathrm{est}}_{i,t}$ | STATISTICAL ESTIMATE (frozen estimator) | H12, H13 only through $\min(\cdot,\mathrm{ADV}^{\max}_i)$ (F111) | caps are non-decreasing in ADV, so the cap never exceeds its value at $\mathrm{ADV}^{\max}_i$: **restrictive only** relative to the policy cap; no model may supply it (Art. 6 amendment) |
| statistical cluster map (RQ-10) | STATISTICAL ESTIMATE | H9, H10 only by merging clusters of $\mathrm{cl}$ | merging only enlarges cluster aggregates: **restrictive only** |
| $b^{\mathrm{mod}}_k$, $R^{\mathrm{mod}}_t$ | MODEL OUTPUT | only through $\min(b^{\mathrm{hard}}_k,\mathfrak s(b^{\mathrm{mod}}_k))$ (F049) | **restrictive or neutral** (T-01) |
| $\mathrm{LB}_t$ (certificate) | MODEL OUTPUT | only as an extra condition for TRADE (F027) | **restrictive or neutral** (T-12) |
| proposal $\tilde n$ | OPTIMISER OUTPUT | only through the verifier F126 | $V(\tilde n)\le Q^{\mathrm{hard}}$: **restrictive or neutral** (T-03) |

Per cap (A = authoritative, X = external observation, S = statistical estimate floored by policy (F111) unless marked, O = order parameters of
the action evaluated; every cap additionally passes through F049 for MODEL OUTPUT and F126 for OPTIMISER OUTPUT):

| Cap / gate | Inputs by class |
|---|---|
| H1 | O: $p^{\mathrm{lim}},p^{\mathrm{stop}}_o$; A: $f^{\mathrm{trd}}$, $\phi$ (F140); S: $\kappa^{\mathrm{out}}$; A+X: $B$ (from $W$; $\Lambda$ is S) |
| H2, H10 | as H1, plus A: $f^{\mathrm{port}},f^{\mathrm{clr}}$, $\mathrm{cl}$ (merge-only statistical refinement), pending orders; A+X+S: $R^{\mathrm{open}},R^{\mathrm{res}}$ (F050, F144, F145) |
| H3 | as H2, plus A: $f^{\mathrm{strat}}_s$, $B^{\mathrm{win}}_s$, $\mathrm{SL}_{s,t}$ (UNDEFINED ⇒ fail-closed rule §4) |
| H4 | as H2, plus A: $\mu^{K}$, floor parameters; A+X+S: $K_t$ |
| H5, H6 | O: $p^{\mathrm{lim}},p^{\mathrm{stop}}_o$; S: $\Gamma_i$, $\kappa^{\mathrm{out}}$; A: $\mu^{G},f^{\mathrm{gap}}$; A+X+S: $K_t$, $G^{\mathrm{open}},G^{\mathrm{res}}$ |
| H7, H8, H9, H11 | O: $p^{\mathrm{lim}}$; A: $f^{\mathrm{ord}},f^{\mathrm{conc}},f^{\mathrm{clu}},\lambda^{\mathrm{gross}}$, $q$, pending orders, $\mathrm{cl}$; X: $m$; A+X+S: $B,W$ |
| H12, H13 | A: $\rho^{\mathrm{in}},w^{\mathrm{in}},\rho^{\mathrm{ex}},h^{\mathrm{ex}}$, $q$, $Q^{\mathrm{res}}$, $\mathrm{ADV}^{\max}_i$; S (capped by policy): $\mathrm{ADV}_{i,t}=\min(\mathrm{ADV}^{\mathrm{est}}_{i,t},\mathrm{ADV}^{\max}_i)$ |
| H14 | O: $p^{\mathrm{lim}}$; A: $\phi^{\mathrm{buy}}$, $C^{\mathrm{avail}}$, $C^{\mathrm{res}}$ (F144); X: $\mathrm{BP}_t$ (only restrictive) |
| H16 | O: $p^{\mathrm{lim}}$; A: $\phi$, $q$, pending orders; X: $m$; A+X+S: $K_t$ |
| G1–G11, post-filter | A: validators, $\theta$, universe, $q$, $Q^{\mathrm{res}}$, $n^{\min}$, live stops (G8); X: $\mathrm{st}_i,\varsigma_i,m_i,\mathrm{ev}_i$; A+X+S: $K_t,\mathrm{DD}_t$ (non-increasing in conservativeness, references estimate-free); O: $d$, $p^{\mathrm{lim}},p^{\mathrm{stop}}_o$; P: $\kappa^{\min},\ell^{\min},\chi$ (G7) — no gate predicate uses an estimate directly; FAIL→PASS under a more conservative estimate is impossible (T-27) |

Hence no MODEL OUTPUT or OPTIMISER OUTPUT can raise any $Q_k$ or $Q^{\mathrm{hard}}$ for a given order: each enters only through $\min$, a verifier
bounded by $Q^{\mathrm{hard}}$, or an additional blocking condition; and no STATISTICAL ESTIMATE can raise $Q^{\mathrm{hard}}_t$ above the policy-bound envelope
$\bar Q^{\mathrm{hard}}_t$ at any epoch, through a cap, a gate or a carried reference (T-27, T-28). The stop of the order is not a model channel: S-family caps are evaluated
against the stop that will be live with the order (A-STOPLIVE); G-family caps are bounded over *all* admissible stops because
$L^{\mathrm{gap}}(n)\ge n\Gamma_ip^{\mathrm{lim}}\ge n\Gamma^{\min}p^{\mathrm{lim}}$ (from $p^{\mathrm{stop}}_o<p^{\mathrm{lim}}$, G7), so $n\,p^{\mathrm{lim}}\le f^{\mathrm{gap}}B_t/\Gamma^{\min}$; H7–H9, H11, H12–H14, H16
do not depend on the stop.

| ID | Brief's cap | Constraint $g_k(n)\le b_k$ | Formula | Tier | Assumptions | Required inputs |
|---|---|---|---|---|---|---|
| H1 | risk (per trade) | $L^{\mathrm{stop}}(n)\le f^{\mathrm{trd}}B_t$ | F076 | S | A-TRIG, A-EXE-01, A-EXE-02 | $p^{\mathrm{lim}},p^{\mathrm{stop}}_o,\kappa^{\mathrm{out}},\phi$ |
| H2 | portfolio risk | $L^{\mathrm{stop}}(n)\le f^{\mathrm{port}}B_t-R^{\mathrm{open}}_t-R^{\mathrm{res}}_t$ | F077 | S | as H1; A-AUTH-02, A-AUTH-04 | all open stops; ledger |
| H3 | strategy loss/risk | $L^{\mathrm{stop}}(n)\le f^{\mathrm{strat}}_sB^{\mathrm{win}}_s-R^{\mathrm{open}}_{s,t}-R^{\mathrm{res}}_{s,t}-\mathrm{SL}_{s,t}$; $\mathrm{SL}_{s,t}$ **UNDEFINED — REQUIRES RESOLUTION** (RQ-11) ⇒ fail-closed rule of §4 | F078 | S | as H2 | strategy attribution |
| H4 | daily / weekly loss, drawdown, capital floor | $L^{\mathrm{stop}}(n)\le \mu^{K}K_t-R^{\mathrm{open}}_t-R^{\mathrm{res}}_t$ | F079 | S | T-10 hypotheses (§2) | $W,F$ components |
| H5 | gap loss (portfolio) | $L^{\mathrm{gap}}(n)\le \mu^{G}K_t-G^{\mathrm{open}}_t-G^{\mathrm{res}}_t$ | F080 | G | A-GAP, §2 common | $\Gamma$ for all positions |
| H6 | gap loss (per trade) | $L^{\mathrm{gap}}(n)\le f^{\mathrm{gap}}B_t$ | F081 | G | A-GAP | $\Gamma_i$ |
| H7 | notional (per order) | $n\,p^{\mathrm{lim}}\le f^{\mathrm{ord}}B_t$ | F082 | U | A-MKT-05 | — |
| H8 | concentration | $q_{i,t}m_{i,t}+N^{\mathrm{res}}_{i,t}+n\,p^{\mathrm{lim}}\le f^{\mathrm{conc}}B_t$ | F083 | U | A-MKT-05, A-AUTH-02 | — |
| H9 | correlation (cluster notional) | $\sum_{i':\,\mathrm{cl}(i')=c}q_{i',t}m_{i',t}+N^{\mathrm{res}}_{c,t}+n\,p^{\mathrm{lim}}\le f^{\mathrm{clu}}B_t$ | F084 | U (given the cluster map) | A-MKT-05, A-AUTH-02 | $\mathrm{cl}$ |
| H10 | correlation (cluster risk, comonotone) | $L^{\mathrm{stop}}(n)\le f^{\mathrm{clr}}B_t-R^{\mathrm{open}}_{c,t}-R^{\mathrm{res}}_{c,t}$ (folded into $R^{\mathrm{hard}}$) | F085 | S | as H2 | $\mathrm{cl}$ |
| H11 | gross exposure / leverage | $N^{\mathrm{open}}_t+N^{\mathrm{res}}_t+n\,p^{\mathrm{lim}}\le\lambda^{\mathrm{gross}}\min(B_t,W_t)$, $\lambda^{\mathrm{gross}}\le1$ under D-02 | F086 | U | A-SCOPE-04, A-MKT-05 | — |
| H12 | liquidity (entry) | $n\le\rho^{\mathrm{in}}\,w^{\mathrm{in}}\,\mathrm{ADV}_{i,t}$, $w^{\mathrm{in}}$ = order working window in trading days (the window-free form fails the dimension check E-08) | F087 | L | A-LIQ, A-MKT-06 | ADV |
| H13 | liquidity (exit) | $q_{i,t}+Q^{\mathrm{res}}_{i,t}+n\le\rho^{\mathrm{ex}}\,h^{\mathrm{ex}}\,\mathrm{ADV}_{i,t}$ | F088 | L | A-LIQ, A-MKT-06 | ADV |
| H14 | buying power | $n\,p^{\mathrm{lim}}+\phi^{\mathrm{buy}}(n)\le \mathrm{BP}^{\mathrm{avail}}_t$ | F089 | U | A-MKT-05, A-SET-01, A-EXE-04 | $\mathrm{BP}_t$, $C^{\mathrm{avail}}_t$, $C^{\mathrm{res}}_t$ |
| H15 | margin | **UNDEFINED — REQUIRES RESOLUTION**; excluded by D-02 (cash account ⇒ H14 suffices) | F090 | — | A-SCOPE-04 | $\mathrm{IM},\mathrm{MM}$ |
| H16 | unconditional floor (optional) | $Z^{\mathrm{open}}_t+Z^{\mathrm{res}}_t+L^{\mathrm{abs}}(n)\le K_t$ — pending orders charged their full $L^{\mathrm{abs}}$ incl. fees, not their notional (review fix: charging $N^{\mathrm{res}}$ left the floor breached by the pending order's fees) | F091 | U | A-MKT-01, A-ACC-05, §2 common | — ; adoption **UNDEFINED — REQUIRES RESOLUTION** (D-08) |

Zero–one **gates** **[F092]** (independent of $n$): G1 $\alpha_t=1$; G2 $\mathrm{st}_i=\text{TRADING}$; G3 $K_t>0$; G4 $\mathrm{DD}_t<d^{\max}$;
G5 $\varsigma_i/m_i\le\varsigma^{\max}$; G6 event policy on $\mathrm{ev}_i$ (**UNDEFINED — REQUIRES RESOLUTION**); G7 opportunity validity
($0<p^{\mathrm{stop}}_o<m^{\mathrm{arr}}$, $p^{\mathrm{stop}}_o<p^{\mathrm{lim}}\le p^{\mathrm{ask}}(1+\chi)$, per-share stop loss
$p^{\mathrm{lim}}-p^{\mathrm{stop}}_o+\kappa^{\min}p^{\mathrm{stop}}_o\ge\ell^{\min}p^{\mathrm{lim}}$ — the policy floor of the exit cost, never an estimate: $\kappa^{\mathrm{out}}(n)\ge\kappa^{\min}p^{\mathrm{stop}}_o$ for every
quantity and every admissible estimate (F111), so the clause bounds the sizing per-share loss from below for every estimate, while a larger
estimate can never make it pass; with $\kappa^{\mathrm{out}}$ in its place a pessimistic $\hat\kappa^{\mathrm{out}}=0.1$ turned $Q=0$ into $9{,}090$, CLOSURE-REV-001); G8 protective-stop
state: for every held quantity with a live stop, $m_{i,t}>p^{\mathrm{stop}}_i$ (long); a mark at or below the stop fails G8 ($\alpha_t=0$ for new risk) whatever
costs, fees or estimates (05 §5; it covers every negative raw value of F064, F065, F145; the `5c486f0` sign test was masked by a larger estimate
or fee and missed $m=48.99<49$, CLOSURE-REV-001); gate monotonicity in estimates: T-27; G9 $d=+1$ (D-01); G10 $i\in\mathbb I_t$ and
$p^{\min}\le m^{\mathrm{arr}}\le p^{\max}$ (A-MKT-06); **G11** $q_{i,t}=0$ and $Q^{\mathrm{res}}_{i,t}=0$ (one exposure per instrument, A-SCOPE-05 — per-lot risk is not
additive under super-additive exit costs, 05 §5).

**Post-filter (non-monotone, never a cap):** minimum order size $n^{\min}$: $Q^{\mathrm{fin}}=Q$ if $Q\ge n^{\min}$ else $0$ **[F093]** (T-03N counterexample
explains why it cannot be folded into the min-of-caps).

**On correlation.** Worst-case aggregation of per-position loss bounds is the **sum**, for every dependence structure
(T-18, F134). The hard layer therefore grants **no diversification credit**; statistical correlation estimates may only tighten budgets
(e.g. by forcing near-duplicate instruments into one cluster). A correlation-adjusted multiplier that can exceed $1$ (negative
estimated correlation, F132) is inadmissible (FM-COR-1).

## 6. Quantity caps and $Q^{\mathrm{hard}}$ (Phase 4)

For each constraint:
$Q_k:=\max\big(\{0\}\cup\{n\in\mathbb L_{>0}:\ n\le\bar N,\ g_k(n)\le b^{\mathrm{allow}}_k\}\big)$ **[F094]**, computed by exact monotone search over the
lattice (bisection terminates in $\lceil\log_2(\bar N/\delta_q)\rceil+1$ steps), or by an exact closed form **only** where $g_k$ is proved
linear: $g_k(n)=n\,\ell_k$, $\ell_k>0$ ⇒ $Q_k=\min\big(\bar N,\ \delta_q\lfloor b_k/(\delta_q\ell_k)\rfloor\big)$ for $b_k\ge0$ **[F095]** (the floor's argument
is dimensionless: [USD]/([sh$_i$]·[USD/sh$_i$]), 03 E-05; the lattice-free form is E-18).

$$
Q^{\mathrm{hard}}=\begin{cases}\min_k Q_k & \text{all gates pass}\\ 0&\text{otherwise}\end{cases}
\qquad\text{and}\qquad \Big\lfloor\min_k y_k\Big\rfloor_{\mathbb L}=\min_k\lfloor y_k\rfloor_{\mathbb L}\ \ (\text{T-03}).
$$
[F096, F097]

The brief's names (aliases, S-243) map as: $Q_{\mathrm{risk}}\leftrightarrow$ H1–H4, H10 (via $R^{\mathrm{allow}}$); $Q_{\mathrm{notional}}\leftrightarrow$ H7, H11;
$Q_{\mathrm{liquidity}}\leftrightarrow$ H12–H13; $Q_{\mathrm{BP}}$ (buying power) $\leftrightarrow$ H14; $Q_{\mathrm{margin}}\leftrightarrow$ H15;
$Q_{\mathrm{portfolio}}\leftrightarrow$ H2, H5, H11; $Q_{\mathrm{correlation}}\leftrightarrow$ H9–H10; plus $Q_{\mathrm{gap}}\leftrightarrow$ H5–H6 and
$Q_{\mathrm{concentration}}\leftrightarrow$ H8, which the brief did not list and which §3 shows are necessary.

**Edge cases (normative handling).**

| Case | Handling | Reference |
|---|---|---|
| Integer shares | $\delta_q=1$ sh | D-04 |
| Fractional shares | $\delta_q=10^{-k}$ sh; whether a protective stop can be attached to the fractional part is **UNKNOWN**; if not, that part is tier U only | D-04, RQ-25 |
| Decimal arithmetic | exact; directed rounding table | 01 §9, T-24 |
| Rounding | floor to lattice; never half-up | T-02 |
| Zero / negative loss per share | G7 rejects $p^{\mathrm{stop}}_o\ge m^{\mathrm{arr}}$ and a policy-floor per-share loss $p^{\mathrm{lim}}-p^{\mathrm{stop}}_o+\kappa^{\min}p^{\mathrm{stop}}_o<\ell^{\min}p^{\mathrm{lim}}$; otherwise $Q_k$ would equal $\bar N$ | T-02, T-27 |
| Negative budgets | clamp to $0$ ⇒ $Q_k=0$ | T-01 |
| Negative wealth | $B_t\le0$, $K_t\le0$ ⇒ all budgets $0$; RECOVERY reason | T-05 |
| NaN / Infinity | rejected at parse; never compared | 01 §9 |
| Overflow | magnitude bounds $\bar M,\bar N$ (F029); decimal Overflow trapped | 01 §9 |
| Tiny account | $R^{\mathrm{allow}}<L^{\mathrm{stop}}(\delta_q)$ ⇒ $Q=0$, reason INSUFFICIENT\_CAPITAL (correct, not an error) | T-02 |
| Huge account | liquidity/concentration caps bind; binary64 overshoot region avoided by exactness | T-22 |

## 7. Drawdown, floors and capital preservation (Phase 5)

**Reference construction (critical closure correction, CLOSURE-REV-002).** Every quantity carried from one epoch to a later one and used
there in a floor or a budget is valued at the *reference wealth* $W^{\mathrm{R}}_t=E_t-\Lambda^{\mathrm{floor}}_t$ [USD] and the *reference NAV* $\nu^{\mathrm{R}}_t=W^{\mathrm{R}}_t/U_t$
[USD/unit] **[F146]**: mark-to-mid equity less the liquidation cost at its policy floor (half-spread plus exit fee, F111) — authoritative state, an
observed spread and the policy fee schedule, never an estimate. These are the high-water mark $H_t$ (F037), the day and week references
$\nu^{\mathrm{day}}_0,\nu^{\mathrm{wk}}_0$ (F041) and the units $U_t$ (issued and redeemed at $\nu^{\mathrm{R}}$, F069); $\nu^{\mathrm{ref}}$ is a policy value. Because
$\Lambda_t=\max(\Lambda^{\mathrm{floor}}_t,\hat\Lambda_t)\ge\Lambda^{\mathrm{floor}}_t$, $W^{\mathrm{R}}_t\ge W_t$: references are at least as high as with any estimate (floors at
least as high) and equal to their policy-bound values, while the current $W_t$ keeps the estimate, which can only lower it. At `5c486f0` the
references used the estimate-inclusive $\nu_u$: $E_u=10^6$, $\hat\Lambda_u=50{,}000$ (floor $1{,}000$), later $E_t=990{,}000$, $\Lambda_t=1{,}000$, $d^{\max}=10\%$,
$U=1$ gave $H=989{,}000$ and $K_t=98{,}900$ instead of $H=999{,}000$ and $K_t=89{,}900$ — a past estimate enlarged a later cushion by $9{,}000$. A system
that is monotone today but stores a permissive reference for tomorrow is not safe; T-28 proves both the instantaneous and the temporal
dominance.

**Definitions.** $\nu_t=W_t/U_t$ **[F036]**; $H_t=\max_{u\in\mathcal H_t}\nu^{\mathrm{R}}_u$ **[F037]** (requires $\nu^{\mathrm{R}}_0>0$, hence $H_t>0$); $\mathrm{DD}_t=1-\nu_t/H_t$ **[F038]**,
the current drawdown against the reference high, $\mathrm{DD}_t=\mathrm{DD}^{\mathrm{R}}_t+(\Lambda_t-\Lambda^{\mathrm{floor}}_t)/(H_tU_t)\ge\mathrm{DD}^{\mathrm{R}}_t=1-\nu^{\mathrm{R}}_t/H_t$ **[F147]**;
$\mathrm{MDD}_t=\max_{u\le t}\mathrm{DD}_u$ **[F039]**; $F^{\mathrm{dd}}_t=(1-d^{\max})H_tU_t$ **[F040]**; $F^{\mathrm{lock}}_t=U_t\big(\nu^{\mathrm{ref}}+\eta^{\mathrm{lock}}(H_t-\nu^{\mathrm{ref}})^+\big)$ **[F042]**;
cushion $K_t=W_t-F_t$ (F044).

**Induced throttle.** With $F_t=F^{\mathrm{dd}}_t$, $U\equiv1$, no open risk and $B=W$:
$K_t=H_t(d^{\max}-\mathrm{DD}_t)$ **[F102]**, so the per-trade budget is $f^{\mathrm{trd}}W_t\,\vartheta_K(\mathrm{DD}_t)$ with

$$
\vartheta_K(\mathrm{DD})=\min\Big\{1,\ \Big(\frac{\mu^{K}}{f^{\mathrm{trd}}}\cdot\frac{d^{\max}-\mathrm{DD}}{1-\mathrm{DD}}\Big)^{+}\Big\},\qquad
\frac{d}{d\,\mathrm{DD}}\,\frac{d^{\max}-\mathrm{DD}}{1-\mathrm{DD}}=-\frac{1-d^{\max}}{(1-\mathrm{DD})^2}<0 .
$$
[F098, F099]

(defined as $\vartheta_K:=0$ for $\mathrm{DD}\ge d^{\max}$ [F098]; the formula alone turns positive again for $\mathrm{DD}>1$). This is the per-trade budget when H1 is the
binding stop-risk term (e.g. $f^{\mathrm{trd}}\le f^{\mathrm{strat}}_s$ and $f^{\mathrm{trd}}\le f^{\mathrm{clr}}$). $\vartheta_K$ is continuous, non-increasing, equal to $1$ up to
$\mathrm{DD}^{*}=\frac{\mu^{K}d^{\max}-f^{\mathrm{trd}}}{\mu^{K}-f^{\mathrm{trd}}}$ **[F100]** (when $\mu^{K}d^{\max}>f^{\mathrm{trd}}$), and exactly $0$ at $\mathrm{DD}=d^{\max}$. The
**aggregate** capacity $\mu^{K}K_t=\mu^{K}H_tU_t(d^{\max}-\mathrm{DD}_t)$ (F102) is linear in $\mathrm{DD}$.

**Why the cushion line, not a chosen shape.** T-21 (closure form): under the disturbance set of tier S with attainable bounds and no active
clamp on a pending order, $W_{t+1}\ge F_t$ for every admissible scenario is **equivalent** to aggregate stop-risk $\le K_t+\Lambda_t=E_t-F_t$
(sufficiency by summation, necessity by the comonotone "all stops hit" scenario; both proved; with an active clamp only sufficiency holds). The hard layer's condition with $K_t$ is sufficient and conservative by exactly $\Lambda_t$ (OC-1, kept
for T-07); it is also necessary exactly when $\Lambda_t=0$, e.g. on a flat book. Hence a
throttle that must be floor-safe in every state lies pointwise below the cushion line; choosing *among* safe throttles is a
preference/performance question for Phase 16, not a safety question.

| Family | Form | Continuous | Monotone in $\mathrm{DD}$ | Zero at $d^{\max}$ | Floor-safe alone (tier S) | Sensitivity | Path-dependent |
|---|---|---|---|---|---|---|---|
| Cushion-induced (CPPI-type) | $\vartheta_K$ above | yes | yes | yes | in every state iff $\mu^{K}\le1$ (necessity on a flat book, T-21 (c)) | bounded: $\le\frac{\mu^{K}}{f^{\mathrm{trd}}(1-d^{\max})}$ on $[0,d^{\max}]$ (F101) | no (function of $W,H$) |
| Linear in $\mathrm{DD}$ | $(1-\mathrm{DD}/d^{\max})^+$ (F104) | yes | yes | yes | single trade (with $B=W$, only $F^{\mathrm{dd}}$ active, no other risk) iff $f^{\mathrm{trd}}\le d^{\max}$ — the loss $f^{\mathrm{trd}}H(1-\mathrm{DD})(1-\mathrm{DD}/d^{\max})$ must not exceed $K=H(d^{\max}-\mathrm{DD})$, i.e. $f^{\mathrm{trd}}(1-\mathrm{DD})\le d^{\max}$ for all $\mathrm{DD}$ (closure, AUD-037; the former condition $f^{\mathrm{trd}}\le\mu^{K}d^{\max}$ is sufficient only); aggregate still needs H4 | $1/d^{\max}$ | no |
| Piecewise step | $\sum_k\vartheta^{\mathrm{step}}_k\mathbb 1[\mathrm{DD}\in\mathcal I_k]$ (F103) | **no** | if $\vartheta^{\mathrm{step}}_k$ non-increasing | if last $\vartheta^{\mathrm{step}}_k=0$ | only if below cushion line pointwise | **unbounded** at steps (chattering) | no |
| Exponential | $e^{-\zeta\,\mathrm{DD}}$ (F105) | yes | yes | **never** | **no** — cannot enforce a floor | $\zeta$ | no |
| Multiplicative per loss | e.g. halve after each loss, reset at new high | n/a | not a function of $(W,H)$ | no | no | — | **yes** (needs extra state) |
| Additive loss budget | budget minus loss since reset | yes | yes | at exhaustion | yes (= a floor) | 1 | reset rule |

Theory support for the cushion form: Grossman & Zhou (1993) show that when wealth must never fall below a fixed fraction of its
running maximum, the optimal risky investment is proportional to the surplus over that floor (CRRA, continuous trading); with discrete trading and gaps the floor can be breached
(Balder, Brandl & Mahayni 2009), which in this architecture is exactly the role of the gap cushion H5 (gap-exposed notional $\le K_t/\Gamma_i$, F106).
Claims about their content are from abstracts; bibliographic verification status: 11 §0.

**Recommendation (PROVISIONAL).** No additional throttle beyond the cushion constraints in v0 (Art. 15). A separate throttle is
**UNDEFINED** until Phase-16 evidence shows a benefit.

**Sensitivity and asymmetry.** $\partial(\mu^{K}K)/\partial W=\mu^{K}$ below the HWM, but $\mu^{K}d^{\max}$ at a new high when $F^{\mathrm{dd}}$ binds **[F107]**.
Consequently favourable moves raise remaining stop-risk of an untrailed long one-for-one while the cushion rises only by the
fraction $d^{\max}$. **The invariant $R^{\mathrm{open}}\le K$ is not preserved by holding under a ratcheting floor** (T-20b; numeric
counterexample: $W$ 100→140, $\mathrm{DD}$ ends at $35.4\%$ with $d^{\max}=10\%$, no new trade, no gap). Maintaining it requires a
stop-trailing or de-risking obligation executed by an authority outside the engine; the engine emits RECOVERY with the
required reduction $R^{\mathrm{open}}-K$. Profit-lock floors ($F^{\mathrm{lock}}$, slope $\eta^{\mathrm{lock}}$) have the same structure with
$d^{\max}$ replaced by $1-\eta^{\mathrm{lock}}$. **Calendar resets ratchet too** (found in review): $\ell^{\mathrm{day}}=2\%$, $W=100$ (cash $50$ + one share at $50$,
stop $49$): $F^{\mathrm{day}}=98$, $K=2\ge r^{\mathrm{open}}=1$; the share closes at $55$: $K=7$, $r^{\mathrm{open}}=6$; next day $F^{\mathrm{day}}=102.9$, $K=2.1<r^{\mathrm{open}}=6$ — no new
high, no trade.

**Maximum-drawdown shutdown.** Gate G4 blocks all new risk when $\mathrm{DD}_t\ge d^{\max}$ (T-06a, PROVED). The *bound* $\mathrm{MDD}\le d^{\max}$
is **DISPROVED** in general (T-06b) and holds per epoch only under the tier-S hypotheses plus the external trailing obligation (T-06c).

## 8. Reservation vector emitted with a TRADE decision

For the chosen $Q=Q^{\mathrm{fin}}$: $\big(L^{\mathrm{stop}}(Q),\ L^{\mathrm{gap}}(Q),\ L^{\mathrm{abs}}(Q),\ Q\,p^{\mathrm{lim}},\ Q\,p^{\mathrm{lim}}+\phi^{\mathrm{buy}}(Q),\ Q\big)$ **[F108]**, tagged with
strategy $s$ and cluster $c$, all rounded up. Computed at the worst-case entry $p^{\mathrm{lim}}$, it dominates the realised open risk
of any fill $e\le Q$ at any price $\le p^{\mathrm{lim}}$ (T-11). The ledger — not the engine — performs the reservation.

## 9. Policy-parameter admissibility (a validity check on $\theta$, not values) [F109]

$0<f^{\mathrm{trd}}\le f^{\mathrm{port}}$; $0<f^{\mathrm{strat}}_s\le f^{\mathrm{port}}$; $0<f^{\mathrm{clr}}\le f^{\mathrm{port}}$; $f^{\mathrm{gap}}>0$;
$0<f^{\mathrm{ord}},f^{\mathrm{conc}},f^{\mathrm{clu}}$; $0<\lambda^{\mathrm{gross}}\le1$ (D-02); $\mu^{K},\mu^{G}\in(0,1]$ (values $>1$ admit floor breach when all stops
hit — T-21); $d^{\max},\ell^{\mathrm{day}},\ell^{\mathrm{wk}}\in(0,1)$; $\eta^{\mathrm{lock}}\in[0,1)$; $\Gamma^{\min}\in(0,1]$; $\kappa^{\min}\ge0$; $\rho^{\mathrm{in}},\rho^{\mathrm{ex}}\in(0,1]$;
$h^{\mathrm{ex}},w^{\mathrm{in}}>0$; $\varsigma^{\max}>0$; $\chi\ge0$; $\ell^{\min}>0$; $0<p^{\min}<p^{\max}$; $n^{\min}\in\mathbb L_{\ge0}$; $F^{\mathrm{abs}}\ge0$; $\bar N,\bar M>0$.
A $\theta$ outside this box ⇒ every decision is NO\_TRADE (reason INVALID\_POLICY). Redundant (never-binding) settings are
permitted but reported.

## 10. Normative evaluation order (specification, not code)

1. Parse; reject non-exact numeric types and special values (01 §9 items 12–14).
2. Gate G1 (authority) — on failure NO\_TRADE with the failed validators.
3. Validity (G7–G11) and anomaly checks on held positions.
4. Hard-layer inputs by F111 (policy floors; frozen estimators).
5. Derive $E,\Lambda,W,\nu,\mathrm{DD},F,K,B$, open-risk aggregates (directed rounding).
6. Gates G2–G6.
7. Hard budgets $b^{\mathrm{hard}}_k$; $R^{\mathrm{hard}}$, $G^{\mathrm{hard}}$ (with the $\mathrm{SL}$ fail-closed rule of §4).
8. Model tightening via $\mathfrak s$ and $\min$ (never `Decimal.min`).
9. $Q_k$ by exact monotone search; $Q^{\mathrm{hard}}=\min_kQ_k$.
10. Optional optimiser proposal → floor to $\mathbb L$ → clip to $[0,Q^{\mathrm{hard}}]$ → exact verification of every $g_k$ (F126).
11. Certified-advantage test (**UNDEFINED in v0.2**; if declared REQUIRED, every decision is NO\_TRADE until defined — D-10).
12. Minimum-order post-filter.
13. Emit record: decision class, $Q^{\mathrm{hard}}$, $Q^{\mathrm{fin}}$, every $Q_k$ and $b_k$, binding set, tiers guaranteed, reservation vector,
    reasons, $\mathrm{hash}(\mathsf S_t)$, $\mathsf v$.

## 11. Unresolved objects in this document

$B_t$ (RQ-02); $\mathrm{SL}_{s,t}$ (RQ-11; fail-closed rule §4); add-on sizing (RQ-34); fee semantics per order vs per execution (RQ-35); cluster map (RQ-10);
$\kappa^{\mathrm{out}},\Lambda$ beyond their floors (RQ-05); $\Gamma_i$ beyond $\Gamma^{\min}$ (RQ-04); ADV estimator (RQ-06);
$C^{\mathrm{avail}}$ (RQ-20); event policy (RQ-04); adoption of H16 (D-08); whether pre-existing open risk is charged to the daily floor (RQ-32);
all values in $\theta$ — each **UNDEFINED — REQUIRES RESOLUTION**.
