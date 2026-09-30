# 05 — Candidate Wealth Dynamics and Economic Cost Accounting Identity (v0.1-draft)

Status: DRAFT. The identities in §2–§3 are PROVED (algebraic, under the stated accounting assumptions). The models inside
$\Lambda$, $\kappa^{\mathrm{out}}$, $\Gamma$ are **UNDEFINED — REQUIRES RESOLUTION**. No objective of the form
$\mathbb E[\log(W_{\text{future}}/W_{\text{now}})]$ may be used before §5 is satisfied.

Accounting assumptions used here (registered in 04): A-ACC-01 single currency (USD); A-ACC-02 corporate actions are
value-neutral adjustments of $(q,m)$ at the instant they occur, with cash components booked to $\mathrm{Inc}$;
A-ACC-03 every fill, fee, income, financing charge and flow is reported exactly once in the authoritative ledger.

---

## 1. Primitive transitions over $(\tau_t,\tau_{t+1}]$

Let $\mathcal J_{t+1}$ be all fills in the period (entries from $a_t$, stop exits, any other orders), each with signed quantity
$n_j$, price $f_j$, fee $\phi_j\ge0$, instrument $i(j)$.

$$
q_{i,t+1}=q_{i,t}+\sum_{j\in\mathcal J_{t+1}:\,i(j)=i}n_j
$$

$$
C_{t+1}=C_t-\sum_{j}n_jf_j-\sum_j\phi_j+\mathrm{Inc}_{t+1}-\mathrm{Fin}_{t+1}+X_{t+1}
$$

$$
E_{t+1}=C_{t+1}+\sum_i q_{i,t+1}m_{i,t+1}-Y_{t+1},\qquad W_{t+1}=E_{t+1}-\Lambda_{t+1}.
$$

## 2. The wealth transition $G$ (PROVED identity)

Substituting §1:

$$
\boxed{\;W_{t+1}=W_t+\underbrace{\sum_i q_{i,t}\,(m_{i,t+1}-m_{i,t})}_{\text{holding P\&L}}+\underbrace{\sum_{j}n_j\,(m_{i(j),t+1}-f_j)}_{\text{trade P\&L to end mark}}-\sum_j\phi_j+\mathrm{Inc}_{t+1}-\mathrm{Fin}_{t+1}-\Delta Y_{t+1}-\Delta\Lambda_{t+1}+X_{t+1}\;}
$$

with $\Delta Y_{t+1}=Y_{t+1}-Y_t$, $\Delta\Lambda_{t+1}=\Lambda_{t+1}-\Lambda_t$.

*Proof.* $\sum_i q_{i,t+1}m_{i,t+1}=\sum_i q_{i,t}m_{i,t+1}+\sum_j n_j m_{i(j),t+1}$. Subtract $E_t=C_t+\sum_iq_{i,t}m_{i,t}-Y_t$ and insert
$C_{t+1}-C_t$ from §1; then subtract $\Lambda_{t+1}-\Lambda_t$. ∎

Hence $W_{t+1}=G(W_t,x_t,a_t,\xi_{t+1})$ where $\xi_{t+1}$ supplies $(m_{\cdot,t+1},\mathcal J_{t+1},\mathrm{Inc},\mathrm{Fin},\Delta Y,X)$ and
$\Lambda_{t+1}$ is the (model) liquidation-cost functional applied to $(q_{t+1},\text{quotes}_{t+1})$. The dependence on $a_t$ enters
**only** through the entry fills in $\mathcal J_{t+1}$ (quantity $e\le n$, price $f\le p^{\mathrm{lim}}$) and the order parameters that
determine stop exits.

Flow-adjusted loss (loss-positive): $\mathcal L_{t+1}:=W_t+X_{t+1}-W_{t+1}$.

**Position closed within the period (sanity check).** For a long $q$ exited entirely at $f$ by a stop ($n_j=-q$):
holding + trade terms $=q(m_{t+1}-m_t)-q(m_{t+1}-f)=q(f-m_t)=\underbrace{q(p^{\mathrm{stop}}-m_t)}_{\text{move to trigger}}+\underbrace{q(f-p^{\mathrm{stop}})}_{-\,q\gamma_j}$.
The end mark $m_{t+1}$ cancels, as it must for a position no longer held.

## 3. Economic Cost Accounting Identity (ECAI)

**Reference prices.** Each fill $j$ is assigned exactly one reference price $\pi^{\mathrm{ref}}_j$ by fill type
(PROVISIONAL convention):

| Fill type | $\pi^{\mathrm{ref}}_j$ | Chain of intermediate references $r_{j,0}=\pi^{\mathrm{ref}}_j\to\cdots\to r_{j,K}=f_j$ |
|---|---|---|
| Entry originating from decision at $\tau_t$ | arrival mid $m^{\mathrm{arr}}$ | $m^{\mathrm{arr}}\to m_{\tau_j}$ (delay) $\to m_{\tau_j}+\operatorname{sgn}(n_j)\varsigma_{\tau_j}/2$ (spread) $\to f_j$ (residual execution) |
| Protective-stop exit | $p^{\mathrm{stop}}$ | $p^{\mathrm{stop}}\to f_j$ (gap + exit execution; split further only if a post-trigger quote is authoritative) |
| Other (manual, risk-reducing) | mid at order arrival | as for entries |

Cost components $c_{j,k}:=n_j\,(r_{j,k}-r_{j,k-1})$ (positive = cost for buys filled above reference and for sells filled below it,
because $n_j<0$ for sells). By telescoping, $\sum_k c_{j,k}=n_j(f_j-\pi^{\mathrm{ref}}_j)$.

**Identity (PROVED).** Splitting the trade term of §2 as $n_j(m_{t+1}-f_j)=n_j(m_{t+1}-\pi^{\mathrm{ref}}_j)-n_j(f_j-\pi^{\mathrm{ref}}_j)$:

$$
W_{t+1}-W_t-X_{t+1}=\underbrace{\sum_i q_{i,t}(m_{i,t+1}-m_{i,t})+\sum_j n_j(m_{i(j),t+1}-\pi^{\mathrm{ref}}_j)}_{\mathcal M_{t+1}\ \text{(market component, "paper" P\&L)}}
-\underbrace{\sum_j\sum_k c_{j,k}}_{\text{execution cost}}
-\underbrace{\sum_j\phi_j}_{\text{fees}}
+\mathrm{Inc}_{t+1}-\mathrm{Fin}_{t+1}-\Delta Y_{t+1}-\underbrace{\Delta\Lambda_{t+1}}_{\text{valuation adj.}}
$$

Each primitive cash or price event appears exactly once on the right-hand side. The delay segment
$m^{\mathrm{arr}}\to m_{\tau_j}$ appears in $\mathcal M$ (paper P&L) and in $c_{j,1}$ (implementation shortfall) with opposite signs; this is
the Perold (1988) paper-vs-actual partition, not double counting — its net contribution to actual wealth is zero, which is
correct because the account did not hold the shares before the fill.

**Identifiability (honest limits).**
- Ex post, *impact* and *slippage beyond the touch* are **not separately identifiable** (the no-trade counterfactual price is
  unobservable). The identity therefore carries a single residual $c_{j,3}$; any split is a model output (class M), not an observation.
- The delay component may contain own information leakage; also not identifiable.
- Realised and unrealised P&L are a cost-basis-dependent **re-partition** of $\mathcal M$ and costs; they never appear in ECAI.

## 4. Double-counting prevention rules

| ID | Rule | Failure it prevents |
|---|---|---|
| DC-1 | Entry spread/slippage/impact is charged ex post only through $f_j$ vs $\pi^{\mathrm{ref}}_j$, and ex ante only through the bound $f\le p^{\mathrm{lim}}$. Ex-ante hard losses use $p^{\mathrm{lim}}$ and add **no** separate entry spread or impact. | Charging spread twice (price that already contains it + explicit spread term) |
| DC-2 | Fees appear only in $\phi$; never embedded in prices, cost basis used for authority, or $\kappa$. | Fee counted in price and in $\phi$ |
| DC-3 | For a stop exit, the stop distance ($p^{\mathrm{lim}}\to p^{\mathrm{stop}}$) and the gap/exit cost ($p^{\mathrm{stop}}\to f$) are disjoint segments. | Gap counted inside "stop risk" and again as "gap risk" in the same budget |
| DC-4 | Limits are defined on changes of $W$ (flow-adjusted), never on $\Pi^R$ alone and never on $\Pi^R+\Delta W$. | Unrealised losses bypassing daily limits (FM-DD-3); or realised loss counted twice |
| DC-5 | Open risk of a held position is measured as the drop in $W_t$ (which already deducts $\Lambda_{i,t}$): $r^{\mathrm{open}}_i=q_i\,(m_i-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(q_i))+\phi^{\mathrm{sell}}_i(q_i)-\Lambda_{i,t}$. | Exit cost charged once in $W_t$ and again in open risk |
| DC-6 | Model-layer expected costs (e.g. expected impact $\iota$) are used for $J$ only; the hard layer uses bounds. The two are never summed. | Mixing an expectation and a bound for the same segment |
| DC-7 | Dividends: the ex-date price drop is market P&L in $\mathcal M$; the cash is $\mathrm{Inc}$; both are real and distinct. For shorts (out of v0 scope) the payment is $\mathrm{Fin}$. | Ignoring or double-booking dividend flows |
| DC-8 | External flows $X$ are excluded from P&L, loss limits, and high-water marks (unitisation, §6). | Deposits creating false new highs; withdrawals creating false drawdowns (FM-DD-1) |
| DC-9 | $\Delta\Lambda$ (change of a model estimate) is reported as a valuation adjustment, separate from market P&L and execution cost. | Model re-estimation masquerading as trading loss/gain |

## 5. Ex-ante scenario losses for a new long entry (PROVISIONAL definitions)

Round-trip wealth drop for an entry of $e$ shares filled at $f^{\mathrm{in}}$ and exited at $f^{\mathrm{out}}$, relative to pre-trade $W_t$:
$e(f^{\mathrm{in}}-f^{\mathrm{out}})+\phi^{\mathrm{buy}}(e)+\phi^{\mathrm{sell}}(e)$ (no $\Lambda$ term: flat before and after).
Bounding $f^{\mathrm{in}}\le p^{\mathrm{lim}}$ (A-MKT-05) and $f^{\mathrm{out}}$ by tier:

| Tier | Exit bound (assumption) | Scenario loss |
|---|---|---|
| S (stop) | $f^{\mathrm{out}}\ge p^{\mathrm{stop}}_o-\kappa^{\mathrm{out}}(n)$ (A-STOP, A-TRIG) | $L^{\mathrm{stop}}(n)=n\big(p^{\mathrm{lim}}-p^{\mathrm{stop}}_o+\kappa^{\mathrm{out}}(n)\big)+\phi^{\mathrm{buy}}(n)+\phi^{\mathrm{sell}}(n)$ |
| G (gap) | $f^{\mathrm{out}}\ge(1-\Gamma_i)\,p^{\mathrm{stop}}_o$ (A-GAP) | $L^{\mathrm{gap}}(n)=n\big(p^{\mathrm{lim}}-(1-\Gamma_i)p^{\mathrm{stop}}_o\big)+\phi^{\mathrm{buy}}(n)+\phi^{\mathrm{sell}}(n)$ |
| U (absolute) | $f^{\mathrm{out}}\ge0$ (A-MKT-01) | $L^{\mathrm{abs}}(n)=n\,p^{\mathrm{lim}}+\phi^{\mathrm{buy}}(n)+\phi^{\mathrm{sell}}_0(n)$ |

Why A-GAP is written against $p^{\mathrm{stop}}$: a stop not yet triggered implies the last tradable price $p_{\mathrm{last}}\ge p^{\mathrm{stop}}$; a
single adverse jump of fraction at most $\Gamma_i$ from $p_{\mathrm{last}}$ gives $f^{\mathrm{out}}\ge(1-\Gamma_i)p_{\mathrm{last}}\ge(1-\Gamma_i)p^{\mathrm{stop}}$.
$\Gamma_i=1$ recovers tier U, so the tiers are one monotone family in the exit bound.

Monotonicity in $e\le n$ (partial fills): all three are non-decreasing in quantity if $\phi$ and $\kappa^{\mathrm{out}}$ are
(A-EXE-01, A-EXE-02) — required by T-02 and T-11.

**Held positions** (relative to $W_t$, DC-5): $r^{\mathrm{open}}_i$ as in DC-5;
$g^{\mathrm{open}}_i=q_i\big(m_i-(1-\Gamma_i)p^{\mathrm{stop}}_i\big)+\phi^{\mathrm{sell}}_i(q_i)-\Lambda_{i,t}$;
$u^{\mathrm{open}}_i=q_im_i+\phi^{\mathrm{sell}}_{i,0}(q_i)-\Lambda_{i,t}$. A negative raw value is an ANOMALY (e.g. $m_i<p^{\mathrm{stop}}_i$
without a trigger) ⇒ $\alpha_t=0$, never "negative risk". $p^{\mathrm{stop}}_i=\bot$ ⇒ D-06 (tier U value), never zero.

## 6. Flow neutrality: unitisation

Units change only on external flows, at the prevailing NAV: $U_{t+1}=U_t+X_{t+1}/\nu^{\star}$ where $\nu^{\star}$ is the NAV at the flow
instant (**timing convention UNDEFINED — REQUIRES RESOLUTION**, RQ-31). Then $\nu$ is unaffected by flows, and high-water marks,
drawdowns and daily/weekly floors are defined on $\nu$ and scaled by $U_t$ (02 S-101..S-108). Absolute-dollar quantities
($F^{\mathrm{abs}}$) are *not* scaled — a withdrawal can therefore legitimately drive $K_t\le0$.

## 7. Conditions under which $\mathbb E[\log(W_{t+1}/W_t)]$ is defined (Phase-2 gate for Phase 8)

1. $W_t>0$ (otherwise the ratio is undefined; every budget is already $0$).
2. $W_{t+1}(a)>0$ $\mathbb Q$-a.s. for **every** $\mathbb Q$ in the model / ambiguity set. For long-only, unlevered portfolios with prices
   $\ge0$: $W_{t+1}\ge W_t-\sum(\text{long notional at worst-case prices})-\text{fees}-\Delta Y-\Delta\Lambda^{+}=:W^{\min}_{t+1}(a)$; a
   sufficient condition is $W^{\min}_{t+1}(a)>0$ (T-19).
3. The argument is dimensionless (ratio); $\log W$ alone is dimensionally invalid (03).
4. Evaluation uses certified numerics (01 §9 item 4); `Decimal(0).ln()` returns `-Infinity` silently (observed), so domain checks precede
   evaluation.

Until an objective is chosen (RQ-13) these conditions are necessary, not sufficient.

## 8. Multi-period composition

$\nu_T/\nu_0=\prod_{t<T}\nu_{t+1}/\nu_t$, so $\log(\nu_T/\nu_0)=\sum_t\log(\nu_{t+1}/\nu_t)$ — additive per-period log growth is valid
**on the unitised NAV**, not on raw $W$ when flows occur. Time consistency of multi-period risk measures is an open question
(RQ-23) and is not needed for the one-step hard layer.

## 9. Unresolved objects in this document

- $\Lambda_{i,t}$ (liquidation-cost model): **UNDEFINED — REQUIRES RESOLUTION** (RQ-05).
- $\kappa^{\mathrm{out}}_i(n)$ (normal stop-execution cost): **UNDEFINED — REQUIRES RESOLUTION** (RQ-05).
- $\Gamma_i$ and horizon classes: **UNDEFINED — REQUIRES RESOLUTION** (RQ-04, D-09).
- Stop-trigger semantics (last trade vs bid vs consolidated): **UNDEFINED — REQUIRES RESOLUTION** (A-TRIG, RQ-21).
- Corporate-action handling between decision and fill: **UNDEFINED — REQUIRES RESOLUTION** (FM-OPS-2).
- Unitisation flow-timing convention: **UNDEFINED — REQUIRES RESOLUTION** (RQ-31).
