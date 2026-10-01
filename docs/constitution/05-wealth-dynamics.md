# 05 — Candidate Wealth Dynamics and Economic Cost Accounting Identity (v0.2-draft)

Status: DRAFT. The identities in §2–§3 are PROVED (algebraic, under the stated accounting assumptions). The models inside
$\Lambda$, $\kappa^{\mathrm{out}}$, $\Gamma$ are **UNDEFINED — REQUIRES RESOLUTION**. No objective of the form
$\mathbb E[\log(W_{t+1}/W_t)]$ may be used before §7 is satisfied. Formula IDs refer to [14](14-formula-registry.md).

Accounting assumptions used here (registered in 04): A-ACC-01 single currency (USD); A-ACC-02 corporate actions split the period
(§1); A-ACC-03 every fill, fee, income, financing charge, accrual, payment and flow is reported exactly once in the authoritative
ledger; A-ACC-04 $\Lambda_t=\sum_i\Lambda_{i,t}$ (no cross-instrument liquidation interaction); A-ACC-06 composition and lower bound of
$\Lambda$ (§1, added v0.2).

v0.2 changes (review corrections): symbol renames (`n_j, f_j` → `n^fill_j, p^fill_j`; `f^in, f^out` → `p^in, p^out`;
`r_{j,k}` → `π^ref_{j,k}`; `c_{j,k}` → `𝒞_{j,k}`) — AUD-007; formula tags — AUD-010; $\Lambda$ composition, OC register and cost
conservation table — AUD-012, AUD-022; position-level exit-value bound — AUD-001.

---

## 1. Primitive transitions over $(\tau_t,\tau_{t+1}]$

Let $\mathcal J_{t+1}$ be all fills and fee postings in the period (entries from $a_t$, stop exits, any other orders), each with signed quantity
$n^{\mathrm{fill}}_j$, price $p^{\mathrm{fill}}_j$, fee $\phi_j\ge0$, instrument $i(j)$. A fee booked after its fill — later in the period, in a later period, or after the
order is terminal — is a posting with $n^{\mathrm{fill}}_j=0$; a fee recorded by the broker as a payable is the same posting with the liability in $Y$ (it is
not an accrual $\mathrm{Accr}$ of A-ACC-07). A fee is *booked* when it is in $W$ through $C$ or $Y$ (F148, CLOSURE-REV-003).

$$
q_{i,t+1}=q_{i,t}+\sum_{j\in\mathcal J_{t+1}:\,i(j)=i}n^{\mathrm{fill}}_j
$$
[F051]

$$
C_{t+1}=C_t-\sum_{j}n^{\mathrm{fill}}_jp^{\mathrm{fill}}_j-\sum_j\phi_j+\mathrm{Inc}_{t+1}-\mathrm{Fin}_{t+1}-\mathrm{Pay}_{t+1}+X_{t+1},\qquad Y_{t+1}=Y_t+\mathrm{Accr}_{t+1}-\mathrm{Pay}_{t+1}
$$
[F052, F053]

$$
E_{t+1}=C_{t+1}+\sum_i q_{i,t+1}m_{i,t+1}-Y_{t+1},\qquad W_{t+1}=E_{t+1}-\Lambda_{t+1}.
$$
[F033, F034]

**Liquidation cost $\Lambda$ (composition defined in v0.2, A-ACC-06).** $\Lambda_t=\sum_i\Lambda_{i,t}$ with the candidate composition
$\Lambda_{i,t}=q_{i,t}\kappa^{\mathrm{liq}}_i(q_{i,t})+\phi^{\mathrm{sell}}_i(q_{i,t})$ **[F035]**: $\Lambda$ *includes* the exit fee of the
holding, so the scope of OC-1 (§4a) is exact. The hard layer uses $\Lambda_{i,t}=\max(\Lambda^{\mathrm{floor}}_{i,t},\hat\Lambda_{i,t})$ with
$\Lambda^{\mathrm{floor}}_{i,t}=q_{i,t}\varsigma_{i,t}/2+\phi^{\mathrm{sell}}_i(q_{i,t})$ **[F111]** (01 Art. 6: a model may raise $\Lambda$, never
lower it below the policy floor). Consistency with A-ACC-05 ($\Lambda_{i}\le q_im_i+\phi^{\mathrm{sell}}_{i,0}(q_i)$) requires
$\phi^{\mathrm{sell}}_i(q_i)-\phi^{\mathrm{sell}}_{i,0}(q_i)\le q_ip^{\mathrm{bid}}_i$ (since $m_i-\varsigma_i/2=p^{\mathrm{bid}}_i$ by F031, F032); checked at load, else $\alpha_t=0$.

**Corporate actions (revised after review).** The position equation above has no corporate-action term, so a period containing a
corporate action at $\tau^{\mathrm{CA}}\in(\tau_t,\tau_{t+1}]$ is **split** at $\tau^{\mathrm{CA}}$. At that instant a restatement operator maps
$(q_i,m_i,p^{\mathrm{stop}}_i)\mapsto(\psi q_i,\ m_i/\psi,\ p^{\mathrm{stop}}_i/\psi)$ **[F054]** for a split ratio $\psi$ (value-neutral), with cash-in-lieu and
cash distributions booked to $\mathrm{Inc}$. Without the split, a 2:1 split with no fills would be booked as a loss of half the position
(e.g. $100\times(25-50)=-2{,}500$). Restatement rules for other corporate-action types: **UNDEFINED — REQUIRES RESOLUTION**.

## 2. The wealth transition $G$ (PROVED identity)

Substituting §1:

$$
\boxed{\;W_{t+1}=W_t+\underbrace{\sum_i q_{i,t}\,(m_{i,t+1}-m_{i,t})}_{\text{holding P\&L}}+\underbrace{\sum_{j}n^{\mathrm{fill}}_j\,(m_{i(j),t+1}-p^{\mathrm{fill}}_j)}_{\text{trade P\&L to end mark}}-\sum_j\phi_j+\mathrm{Inc}_{t+1}-\mathrm{Fin}_{t+1}-\mathrm{Accr}_{t+1}-\Delta\Lambda_{t+1}+X_{t+1}\;}
$$
[F055]

with $\Delta\Lambda_{t+1}=\Lambda_{t+1}-\Lambda_t$. (Payments of accrued liabilities cancel: $-\mathrm{Pay}$ in cash, $+\mathrm{Pay}$ in $-\Delta Y$.)

*Proof.* $\sum_i q_{i,t+1}m_{i,t+1}=\sum_i q_{i,t}m_{i,t+1}+\sum_j n^{\mathrm{fill}}_j m_{i(j),t+1}$. Subtract $E_t=C_t+\sum_iq_{i,t}m_{i,t}-Y_t$ and insert
$C_{t+1}-C_t$ and $Y_{t+1}-Y_t$ from §1; then subtract $\Lambda_{t+1}-\Lambda_t$. ∎

Hence $W_{t+1}=G(W_t,x_t,a_t,\xi_{t+1})$ where $\xi_{t+1}$ supplies $(m_{\cdot,t+1},\mathcal J_{t+1},\mathrm{Inc},\mathrm{Fin},\mathrm{Accr},X)$ and
$\Lambda_{t+1}$ is the (model) liquidation-cost functional applied to $(q_{t+1},\text{quotes}_{t+1})$. The dependence on $a_t$ enters
**only** through the entry fills in $\mathcal J_{t+1}$ (quantity $e\le n$, price $p^{\mathrm{in}}\le p^{\mathrm{lim}}$) and the order parameters that
determine stop exits.

Flow-adjusted loss (loss-positive): $\mathcal L_{t+1}:=W_t+X_{t+1}-W_{t+1}$ **[F008]**.

**Position closed within the period (sanity check).** For a long $q$ exited entirely at $p^{\mathrm{out}}$ by a stop ($n^{\mathrm{fill}}_j=-q$):
holding + trade terms $=q(m_{t+1}-m_t)-q(m_{t+1}-p^{\mathrm{out}})=q(p^{\mathrm{out}}-m_t)=\underbrace{q(p^{\mathrm{stop}}-m_t)}_{\text{move to trigger}}+\underbrace{q(p^{\mathrm{out}}-p^{\mathrm{stop}})}_{-\,q\gamma_j}$.
The end mark $m_{t+1}$ cancels, as it must for a position no longer held.

## 3. Economic Cost Accounting Identity (ECAI)

**Reference prices.** Each fill $j$ is assigned exactly one reference price $\pi^{\mathrm{ref}}_j$ by fill type
(PROVISIONAL convention):

| Fill type | $\pi^{\mathrm{ref}}_j$ | Chain of intermediate references $\pi^{\mathrm{ref}}_{j,0}=\pi^{\mathrm{ref}}_j\to\cdots\to \pi^{\mathrm{ref}}_{j,k_j}=p^{\mathrm{fill}}_j$ |
|---|---|---|
| Entry originating from decision at $\tau_t$ | arrival mid $m^{\mathrm{arr}}$ | $m^{\mathrm{arr}}\to m_{\tau^{\mathrm{fill}}_j}$ (delay) $\to m_{\tau^{\mathrm{fill}}_j}+\operatorname{sgn}(n^{\mathrm{fill}}_j)\varsigma_{\tau^{\mathrm{fill}}_j}/2$ (spread) $\to p^{\mathrm{fill}}_j$ (residual execution) |
| Protective-stop exit | $p^{\mathrm{stop}}$ | $p^{\mathrm{stop}}\to p^{\mathrm{fill}}_j$ (gap + exit execution; split further only if a post-trigger quote is authoritative) |
| Other (manual, risk-reducing) | mid at order arrival | as for entries |

Cost components $\mathcal C_{j,k}:=n^{\mathrm{fill}}_j\,(\pi^{\mathrm{ref}}_{j,k}-\pi^{\mathrm{ref}}_{j,k-1})$ **[F057]** (positive = cost for buys filled above reference and for
sells filled below it, because $n^{\mathrm{fill}}_j<0$ for sells). By telescoping, $\sum_k \mathcal C_{j,k}=n^{\mathrm{fill}}_j(p^{\mathrm{fill}}_j-\pi^{\mathrm{ref}}_j)$.

**Identity (PROVED).** Splitting the trade term of §2 as $n^{\mathrm{fill}}_j(m_{t+1}-p^{\mathrm{fill}}_j)=n^{\mathrm{fill}}_j(m_{t+1}-\pi^{\mathrm{ref}}_j)-n^{\mathrm{fill}}_j(p^{\mathrm{fill}}_j-\pi^{\mathrm{ref}}_j)$ **[F056]**:

$$
W_{t+1}-W_t-X_{t+1}=\underbrace{\sum_i q_{i,t}(m_{i,t+1}-m_{i,t})+\sum_j n^{\mathrm{fill}}_j(m_{i(j),t+1}-\pi^{\mathrm{ref}}_j)}_{\mathcal M_{t+1}\ \text{(market component, "paper" P\&L)}}
-\underbrace{\sum_j\sum_k \mathcal C_{j,k}}_{\text{execution cost}}
-\underbrace{\sum_j\phi_j}_{\text{fees}}
+\mathrm{Inc}_{t+1}-\mathrm{Fin}_{t+1}-\mathrm{Accr}_{t+1}-\underbrace{\Delta\Lambda_{t+1}}_{\text{valuation adj.}}
$$
[F058]

Each primitive cash or price event appears exactly once on the right-hand side. The delay segment
$m^{\mathrm{arr}}\to m_{\tau^{\mathrm{fill}}_j}$ appears in $\mathcal M$ (paper P&L) and in $\mathcal C_{j,1}$ (implementation shortfall) with opposite signs; this is
the Perold (1988) paper-vs-actual partition, not double counting — its net contribution to actual wealth is zero, which is
correct because the account did not hold the shares before the fill.

**Identifiability (honest limits).**
- Ex post, *impact* and *slippage beyond the touch* are **not separately identifiable** (the no-trade counterfactual price is
  unobservable). The identity therefore carries a single residual $\mathcal C_{j,3}$; any split is a model output (class M), not an observation.
- The delay component may contain own information leakage; also not identifiable.
- Realised and unrealised P&L are a cost-basis-dependent **re-partition** of $\mathcal M$ and costs; they never appear in ECAI.

## 4. Double-counting prevention rules

| ID | Rule | Failure it prevents |
|---|---|---|
| DC-1 | Entry spread/slippage/impact is charged ex post only through $p^{\mathrm{fill}}_j$ vs $\pi^{\mathrm{ref}}_j$, and ex ante only through the bound $p^{\mathrm{in}}\le p^{\mathrm{lim}}$. Ex-ante hard losses use $p^{\mathrm{lim}}$ and add **no** separate entry spread or impact. | Charging spread twice (price that already contains it + explicit spread term) |
| DC-2 | Fees appear only in $\phi$; never embedded in prices, cost basis used for authority, or $\kappa^{\mathrm{out}}$. | Fee counted in price and in $\phi$ |
| DC-3 | For a stop exit, the stop distance ($p^{\mathrm{lim}}\to p^{\mathrm{stop}}$) and the gap/exit cost ($p^{\mathrm{stop}}\to p^{\mathrm{out}}$) are disjoint segments. | Gap counted inside "stop risk" and again as "gap risk" in the same budget |
| DC-4 | Limits are defined on changes of $W$ (flow-adjusted), never on $\Pi^R$ alone and never on $\Pi^R+\Delta W$. | Unrealised losses bypassing daily limits (FM-DD-3); or realised loss counted twice |
| DC-5 (revised) | Open risk of a held position is $r^{\mathrm{open}}_i=q_i\,(m_i-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(q_i))+\phi^{\mathrm{sell}}_i(q_i)$ **[F064]** **without** a credit for $\Lambda_{i,t}$, although $W_t$ already deducts $\Lambda_{i,t}$. This is a deliberate, registered conservative over-charge (**OC-1**): granting the credit makes every budget *increase* when liquidity worsens (review counterexample, 08 T-07) | Liquidity non-monotonicity of budgets; the accounting identity ECAI is unaffected (Art. 12 governs identities, not conservative bounds) |
| DC-6 | Model-layer expected costs (e.g. expected impact $\iota$, F112) are used for $J$ only; the hard layer uses bounds. The two are never summed. | Mixing an expectation and a bound for the same segment |
| DC-7 | Dividends: the ex-date price drop is market P&L in $\mathcal M$; the cash is $\mathrm{Inc}$; both are real and distinct. For shorts (out of v0 scope) the payment is $\mathrm{Fin}$. | Ignoring or double-booking dividend flows |
| DC-8 | External flows $X$ are excluded from P&L, loss limits, and high-water marks (unitisation, §6). | Deposits creating false new highs; withdrawals creating false drawdowns (FM-DD-1) |
| DC-9 | $\Delta\Lambda$ (change of a model estimate) is reported as a valuation adjustment, separate from market P&L and execution cost. | Model re-estimation masquerading as trading loss/gain |

### 4a. Register of deliberate conservative over-charges (OC)

An over-charge is a term deducted twice (once in state, once in a hard budget) **on purpose**. Each is conservative (it can only reduce
$Q^{\mathrm{hard}}$), is never used by an identity (Art. 12), and is listed with its size and removal condition. **Closure status:** OC-2, OC-3 and
OC-4 were eliminated at Phase-0 closure (AUD-034, AUD-035) — two of them charged an already *realised* cost again. Only OC-1 remains: it
over-charges a *future* exit cost, never a realised one, and it is necessary for T-07 (below).

| ID | Term charged twice | First charge (state) | Second charge (hard budget) | Size of over-charge | Why kept | Removal condition |
|---|---|---|---|---|---|---|
| OC-1 | Liquidation cost of held positions (incl. exit fee, F035) — a future cost, not a realised one | $W_t=E_t-\Lambda_t$ (F034) ⇒ $K_t$ | $r^{\mathrm{open}},g^{\mathrm{open}},u^{\mathrm{open}},r^{\mathrm{pf}},g^{\mathrm{pf}},u^{\mathrm{pf}}$ carry $\kappa^{\mathrm{out}}$ and the exit fee without $+\Lambda_{i,t}$ credit | exactly $\Lambda_t$ (T-21) | **necessary for T-07**: crediting $\Lambda$ makes the floor room *grow* when liquidity worsens — in budgets of the form $f^{\mathrm{port}}B$ (08 T-07) and in the cushion at a new high, where (references by F146) $F^{\mathrm{dd}}=(1-d^{\max})W^{\mathrm{R}}$ gives $K+\Lambda=d^{\max}E+(1-d^{\max})\Lambda^{\mathrm{floor}}$, growing when liquidity worsens through $\Lambda^{\mathrm{floor}}$ (exact, with $\Lambda=\Lambda^{\mathrm{floor}}$: cash $100{,}000$, $1{,}000$ sh at $50$, stop $45$, $\kappa^{\mathrm{out}}=0.05$, $d^{\max}=10\%$: H4 room $10{,}040$ at $\Lambda=100$ but $10{,}400$ at $\Lambda=500$; without the credit $9{,}940$ and $9{,}900$) | none in v0 |
| OC-2 | Cash committed to pending buy orders | — | — | — | **ELIMINATED at closure (AUD-035):** F048 is now $\min(\mathrm{BP}_t,\ C^{\mathrm{avail}}_t-C^{\mathrm{res}}_t)$; pending cash is deducted once, from own ledger cash, and the broker figure can only restrict | — |
| OC-3 | Realised strategy loss | — | — | — | **ELIMINATED at closure (AUD-035):** H3 uses the window-start base $B^{\mathrm{win}}_s$ (F078), so realised strategy loss enters once, through $\mathrm{SL}_{s,t}$ | — |
| OC-4 | Filled part of a partially filled order | — | — | — | **ELIMINATED at closure (AUD-034):** the instrument is charged the exact exposure charge F145 (held part and remainder together, fees already paid excluded) instead of open risk plus the full-order reservation, which counted the paid entry fee and the filled quantity's risk twice | — |

### 4b. Economic cost conservation table (added v0.2, AUD-012)

Every economic term has exactly one state-transition location (F052–F058). "Objective location": all candidate objectives (F018–F023)
consume $W_{t+1}$ from F055, so every state term reaches $J$ through F055 exactly once; model-layer expectations are listed where they differ.
"Risk location": the hard-layer charge. A duplicate is either an OC entry (conservative, registered), a layer separation (DC-6, never
summed) or UNRESOLVED with an owner.

| Term | Unit | State transition location | Objective location | Risk location | Duplicate elsewhere? | Resolution |
|---|---|---|---|---|---|---|
| Market move of held quantity $q_{i,t}\Delta m_i$ | [USD] | F055 holding term | via F055 | $r^{\mathrm{open}}$ distance $m_i-p^{\mathrm{stop}}_i$ (F064) | no | single location |
| Entry spread, residual slippage, impact ($p^{\mathrm{fill}}_j-\pi^{\mathrm{ref}}_j$) | [USD] | F057 inside $p^{\mathrm{fill}}_j$ (F052) | via F055; model layer adds expected $\iota$ (F112) only when no fill is simulated | bound $p^{\mathrm{in}}\le p^{\mathrm{lim}}$ in $L^{\mathrm{stop}},L^{\mathrm{gap}},L^{\mathrm{abs}}$ (DC-1) | expectation in $J$ and bound in risk | layer separation (DC-6); never summed |
| Delay ($m^{\mathrm{arr}}\to m_{\tau^{\mathrm{fill}}_j}$) | [USD] | $\mathcal M$ and $\mathcal C_{j,1}$ with opposite signs (F058) | via F055 (net zero) | inside the $p^{\mathrm{lim}}$ bound | appears twice by construction | Perold partition; nets to zero in $W$ (§3) |
| Fees $\phi_j$ (buy and sell) | [USD] | F052, at the fill or as a later posting (05 §1) | via F055 | $\phi^{\mathrm{buy}},\phi^{\mathrm{sell}}$ in $L^{\mathrm{stop}},L^{\mathrm{gap}},L^{\mathrm{abs}}$ (F061–F063); $\phi^{\mathrm{buy}}$ in H14 (F089); owed-but-unbooked entry fees $\phi^{\mathrm{owed}}_o$ in F145 or the F144 owed-fee reservation until booked (F148) | loss budgets and cash budget count the same fee | separate constraint families, one charge per family (not a duplicate within any budget); non-super-additive schedules are charged through $\phi^{\mathrm{split}}$ (F140), which bounds the fees actually paid, not a second charge; each entry-fee dollar is booked in $W$ or owed in exactly one charge, never both (T-29) |
| Stop exit cost $\kappa^{\mathrm{out}}$ ($p^{\mathrm{stop}}\to p^{\mathrm{out}}$) | [USD] | realised in the exit $p^{\mathrm{fill}}_j$ (F057 stop chain) | via F055 | $L^{\mathrm{stop}}$, $r^{\mathrm{open}}$ (F061, F064); floor F111 | no (DC-3) | single location per tier |
| Gap beyond stop ($p^{\mathrm{stop}}\to p^{\mathrm{gx}}$) | [USD] | realised in the exit $p^{\mathrm{fill}}_j$ | via F055 | $L^{\mathrm{gap}}$, $g^{\mathrm{open}}$ (F062, F065) — tier G only | tiers S and G are alternative scenarios, never added | tier families are separate budgets (06 §2) |
| Execution cost of other (manual, risk-reducing) exits | [USD] | F057 ('other' chain) inside $p^{\mathrm{fill}}_j$ | via F055 | none ex ante: such orders are outside the floor theorems (A-EXE-05) | no | single location; a period with such an order is outside T-10 |
| Liquidation cost of holdings $\Lambda_t$ (incl. exit fee, F035) | [USD] | F034; $\Delta\Lambda$ in F055 | via F055 | not credited in $r^{\mathrm{open}},g^{\mathrm{open}},u^{\mathrm{open}}$ | **yes** | **OC-1** |
| Model re-estimation $\Delta\Lambda$ | [USD] | F055 valuation adjustment | via F055 | through $K_t$ only | no | DC-9 |
| Pending-order cash $C^{\mathrm{res}}$ | [USD] | none until fill (then F052) | none | H14 via F048, remaining cost $(n'-q)p'^{\mathrm{lim}}+\phi^{\mathrm{buy}}(n')-\phi^{\mathrm{paid}}_o$ (F144), and the owed entry fees of terminal orders (F148) | no | deducted once from own cash; broker $\mathrm{BP}$ only restricts (F048) |
| Pending-order risk $R^{\mathrm{res}},G^{\mathrm{res}},Z^{\mathrm{res}},N^{\mathrm{res}},Q^{\mathrm{res}}$ | [USD], [sh$_i$] | none until fill; filled parts enter $q$ (F051), paid fees enter cash (F052) | none | re-evaluated at $\tau_t$ from the order state (F144): remaining quantity and remaining cost only; a partially filled order is charged $r^{\mathrm{pf}},g^{\mathrm{pf}},u^{\mathrm{pf}}$ (F145) and its held part no separate open risk | no (realised entry price and fees are in $W$ only) | single charge per exposure; re-evaluating an already reserved opportunity as new is blocked by G11 ($Q^{\mathrm{res}}_{i,t}\ne0$); a dropped order violates A-AUTH-02 and is undetectable by the pure engine — **UNRESOLVED: idempotency obligation of the integration contract** (owner: Phase-10 integration contract; fail-closed there: an opportunity identifier present in the ledger is never re-reserved). The ledger's own full-reservation rule (A-AUTH-05) is bookkeeping for T-11, not an engine input |
| Realised strategy loss $\mathrm{SL}_{s,t}$ | [USD] | inside $W$ via F055 | via F055 | H3 (F078) against the window-start base $B^{\mathrm{win}}_s$ | no | counted once in H3; $\mathrm{SL}$ undefined ⇒ AUD-028 rule (06 §4) |
| Income $\mathrm{Inc}$ | [USD] | F052 | via F055 | not credited ex ante (T-10 assumes $\ge0$) | ex-date drop in $\mathcal M$ vs cash | DC-7 (distinct real events) |
| Financing $\mathrm{Fin}$ | [USD] | F052 | via F055 | v0: $0$ (cash account, D-02); T-10 assumes $0$ | no | single location |
| Accruals $\mathrm{Accr}$, payments $\mathrm{Pay}$ | [USD] | F052, F053 | via F055 ($\mathrm{Pay}$ cancels) | $\bar A_{t+1}$ in $W^{\min}$ (F070); T-10 assumes $\mathrm{Accr}=0$ | $\mathrm{Pay}$ in cash and in $Y$ | cancels exactly (§2) |
| External flows $X$ | [USD] | F052; units F069 | excluded ($\mathcal L$ is flow-adjusted, F008) | floors scaled by $U_t$; T-10 assumes $X=0$ | no | DC-8 |
| Corporate action | [USD] (zero net) | F054 restatement | via F055 (value-neutral) | stop restated with the position | no | A-ACC-02 |
| Borrow, short dividends, margin interest, FX, taxes | [USD] | not modelled | — | — | — | out of v0 scope (A-SCOPE-01, A-SCOPE-03, A-SCOPE-04); **UNDEFINED** if scope widens |

Result (closure): every row has exactly one state-transition location; **no realised cost is charged twice**; the only state/risk
duplicate is OC-1 (a future exit cost, conservative by exactly $\Lambda_t$, necessary for T-07); the expectation/bound pair is a layer
separation; one idempotency item is UNRESOLVED with an owner outside the pure engine.

## 5. Ex-ante scenario losses for a new long entry (PROVISIONAL definitions)

Round-trip wealth drop for an entry of $e$ shares filled at $p^{\mathrm{in}}$ and exited at $p^{\mathrm{out}}$, relative to pre-trade $W_t$:
$e(p^{\mathrm{in}}-p^{\mathrm{out}})+\phi^{\mathrm{buy}}(e)+\phi^{\mathrm{sell}}(e)$ **[F059]** (no $\Lambda$ term: flat before and after).
Bounding $p^{\mathrm{in}}\le p^{\mathrm{lim}}$ (A-MKT-05, every partial fill) and $p^{\mathrm{out}}$ by tier (sufficient per-share conditions **[F060]**):

| Tier | Exit bound (assumption) | Scenario loss |
|---|---|---|
| S (stop) | $p^{\mathrm{out}}\ge p^{\mathrm{stop}}_o-\kappa^{\mathrm{out}}(n)$ (A-STOP; position level: A-TRIG, F072) | $L^{\mathrm{stop}}(n)=n\big(p^{\mathrm{lim}}-p^{\mathrm{stop}}_o+\kappa^{\mathrm{out}}(n)\big)+\phi^{\mathrm{buy}}(n)+\phi^{\mathrm{sell}}(n)$ **[F061]** |
| G (gap) | $p^{\mathrm{out}}\ge p^{\mathrm{gx}}(n)$ with $p^{\mathrm{gx}}$ as in F060 (A-GAP) | $L^{\mathrm{gap}}(n)=n\big(p^{\mathrm{lim}}-p^{\mathrm{gx}}(n)\big)+\phi^{\mathrm{buy}}(n)+\phi^{\mathrm{sell}}(n)$ **[F062]** |
| U (absolute) | $p^{\mathrm{out}}\ge0$ (A-MKT-01) | $L^{\mathrm{abs}}(n)=n\,p^{\mathrm{lim}}+\phi^{\mathrm{buy}}(n)+\phi^{\mathrm{sell}}_{\cdot,0}(n)$ **[F063]** |

Tier-G exit bound: $p^{\mathrm{gx}}(n)=\min\big((1-\Gamma_i)p^{\mathrm{stop}}_o,\ p^{\mathrm{stop}}_o-\kappa^{\mathrm{out}}(n)\big)$ [F060].

Why A-GAP is written against $p^{\mathrm{stop}}$: a stop not yet triggered implies the last tradable price $p_{\mathrm{last}}\ge p^{\mathrm{stop}}$; a
single adverse jump of fraction at most $\Gamma_i$ from $p_{\mathrm{last}}$ gives $p^{\mathrm{out}}\ge(1-\Gamma_i)p_{\mathrm{last}}\ge(1-\Gamma_i)p^{\mathrm{stop}}$.
The $\min$ (added after review) makes tier G dominate tier S for every $\Gamma_i$, so A-TRIG also implies the tier-G valuation bound; without it,
$\Gamma_ip^{\mathrm{stop}}<\kappa^{\mathrm{out}}$ gives a tier-G bound *weaker* than tier S (e.g. $\Gamma=1\%$, $p^{\mathrm{stop}}=10$, $\kappa^{\mathrm{out}}=0.2$: $9.90>9.80$).
$\Gamma_i=1$ recovers tier U (up to the sell-fee evaluation), so the tiers are one monotone family in the exit bound. Execution-assumption
risk increment: $\mathrm{ER}(n)=L^{\mathrm{gap}}(n)-L^{\mathrm{stop}}(n)\ge0$ **[F067]**.

Monotonicity in $e\le n$ (partial fills): all three are non-decreasing in quantity if $\phi$ and $\kappa^{\mathrm{out}}$ are
(A-EXE-01, A-EXE-02) — required by T-02 and T-11 (c).

**Held positions** (DC-5, no $\Lambda$ credit): $r^{\mathrm{open}}_i$ as in DC-5 [F064];
$g^{\mathrm{open}}_i=q_i\big(m_i-p^{\mathrm{gx}}_i(q_i)\big)+\phi^{\mathrm{sell}}_i(q_i)$ **[F065]**;
$u^{\mathrm{open}}_i=q_im_i+\phi^{\mathrm{sell}}_{i,0}(q_i)$ **[F066]**. None of them carries an entry fee: owed entry fees are charged in F144 (F148). **ANOMALY**
(gate G8, closure correction CLOSURE-REV-001): a held exposure whose authoritative mark has reached or crossed its live stop, $m_i\le p^{\mathrm{stop}}_i$
(long) ⇒ $\alpha_t=0$ for new risk, whatever $\hat\kappa^{\mathrm{out}}$, $\hat\Gamma$, $\hat\Lambda$ or the fee schedule. Every negative raw value of F064 or F065 implies
it ($m_i-p^{\mathrm{stop}}_i<-\kappa^{\mathrm{out}}_i(q_i)-\phi^{\mathrm{split}}_i(q_i)/q_i\le0$, and $p^{\mathrm{gx}}_i\le p^{\mathrm{stop}}_i$ by F060), so the `5c486f0` sign test is subsumed; the
converse fails — mark $48.99$ below stop $49$ gives $r^{\mathrm{open}}=+5.9$ with $\kappa^{\mathrm{out}}$ at its floor, and a larger estimate or fee could make a negative
raw value positive (CLOSURE-REV-001) — which is why the gate tests the mark, not a cost-dependent sign. $p^{\mathrm{stop}}_i=\bot$ ⇒ D-06 (tier U value),
never zero.

**Position-level exit-value bound (A-TRIG, v0.2, AUD-001).** For each exposure $i$ of the period — a held position without a pending order
($q^{\mathrm{exp}}_i=q_{i,t}$); a new or pending order on a fresh instrument ($q^{\mathrm{exp}}_i=e$); or a held position with a pending remainder of the
same order ($q^{\mathrm{exp}}_i=q_{i,t}+e$, REV-027) — with exit fills $\mathcal J^{\mathrm{ex}}_{i,t+1}$ and remainder $q^{\mathrm{rem}}_{i,t+1}$, and with $\kappa^{\mathrm{out}}$ and the
fee schedule taken at the $\tau_t$ hard-layer inputs (F111):

$$
\mathrm{XV}_{i,t+1}=\sum_{j\in\mathcal J^{\mathrm{ex}}_{i,t+1}}\big(\lvert n^{\mathrm{fill}}_j\rvert p^{\mathrm{fill}}_j-\phi_j\big)+q^{\mathrm{rem}}_{i,t+1}m_{i,t+1}-\Lambda_{i,t+1}\ \ge\ q^{\mathrm{exp}}_i\big(p^{\mathrm{stop}}_i-\kappa^{\mathrm{out}}_i(q^{\mathrm{exp}}_i)\big)-\phi^{\mathrm{sell}}_i(q^{\mathrm{exp}}_i)
$$
[F072]

(tier G: right-hand side $q^{\mathrm{exp}}_ip^{\mathrm{gx}}_i(q^{\mathrm{exp}}_i)-\phi^{\mathrm{sell}}_i(q^{\mathrm{exp}}_i)$; tier U: $-\phi^{\mathrm{sell}}_{i,0}(q^{\mathrm{exp}}_i)$). One inequality covers
untriggered, fully exited and partially exited exposures, so every exit fee is counted once against one allowance $\phi^{\mathrm{sell}}(q^{\mathrm{exp}})$.
The v0.1.1 per-case form (remainder valued with its own fee) double-counted fees. Scenario (AUD-001 fill pattern, stated for a new order
because v0.2 forces $\Lambda_t\ge1$ on a held position, REV-030): new order $100$ at $50$, stop $49$, $\kappa^{\mathrm{out}}=0.1$, fee $\max(1,0.005k)$ per
order; $50$ filled at $48.9$ by the stop, remainder valued at $2{,}444$: $\mathrm{XV}=4{,}888<4{,}889$ **violates** F072 and, with $L^{\mathrm{stop}}=112=K_t$,
$W_{t+1}=F_t-1$ — a real market/fee outcome, so F072 is an assumption that can fail. Rule (A-EXE-04, RQ-35; closure form): the hard layer
**always** uses, in place of $\phi^{\mathrm{sell}}$ and $\phi^{\mathrm{sell}}_{\cdot,0}$ in F061–F066, F070, F145 and on the right-hand side of F072, the split envelope
$\phi^{\mathrm{split}}(n)=\max\{\sum_{k=1}^{N^{\mathrm{ex}}+1}\phi^{\mathrm{sell}}(n_k):n_k\in\mathbb L_{\ge0},\sum_kn_k=n\}$ **[F140]**, where $N^{\mathrm{ex}}$ is the maximum number of exit
orders per exposure per period ($N^{\mathrm{ex}}+1$ parts: those orders plus a part still held at the cut). With one exit order the scenario
satisfies F072 with equality ($4{,}888\ge4{,}890-2$), $L^{\mathrm{stop}}=113$ and $W_{t+1}=F_t$. The two-part form is not enough when an exposure is
exited by several orders: one child stop per entry fill ($34/33/33$, each paying the \$1 minimum) gives $\mathrm{XV}=4{,}887<4{,}888$ and
$W_{t+1}=F_t-1$ with $L^{\mathrm{stop}}=113$ (REV-029); with $N^{\mathrm{ex}}=3$ the charge is $115$ and F072 holds. Unknown $N^{\mathrm{ex}}$ ⇒ F140 with $n/\delta_q$ parts (every lot a
separate execution).
For a super-additive schedule ($\phi(k)+\phi(n-k)\le\phi(n)$ for all $k$) the envelope equals $\phi^{\mathrm{sell}}(n)$, so the rule changes nothing there.

**Partially filled order (closure, AUD-033, AUD-034).** An instrument holding $q_{i,t}>0$ from an order of total $n'$ at limit $p'^{\mathrm{lim}}$ that is still
pending is one exposure. It is charged the exact worst case of the held part and the unfilled remainder together, with the entry fees already
paid, $\phi^{\mathrm{paid}}_o$, excluded because they are realised and already in $W_t$:
$r^{\mathrm{pf}}_i=q_{i,t}(m_{i,t}-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(n'))+(n'-q_{i,t})(p'^{\mathrm{lim}}-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(n'))^++\phi^{\mathrm{split}}(n')+\phi^{\mathrm{buy}}(n')-\phi^{\mathrm{paid}}_o$ **[F145]**
(tier G with $p^{\mathrm{gx}}_i(n')$, tier U with exit price $0$), in place of $r^{\mathrm{open}}_i$ plus the order's reservation (F144). The clamp $(\cdot)^+$ is needed
because the unfilled part may not fill ($e=0$) while the stop can have been trailed to or above the limit after G7 checked it; the worst case over
$0\le e\le n'-q_{i,t}$ of a term linear in $e$ is at an end point (AUD-039). Exhaustive exact enumeration (full, partial and multiple partial fills;
per-order minimum fees; up to $N^{\mathrm{ex}}=3$ exit orders plus a remainder at the cut; fees billed at once or late) gives worst loss $=r^{\mathrm{pf}}_i-\Lambda_{i,t}$ in
every state with the stop below the limit; with stops from $2$ below to $3$ above the limit ($46{,}200$ scenarios, $1{,}800$ states) the clamped
charge is never understated and is exact in $1{,}250$ states. No realised cost is inside it. The ANOMALY rule applies to the held part in the same
form: its mark at or below the exposure's live stop fails G8 (CLOSURE-REV-001; this replaces the sign test of AUD-051, which a larger estimate or
fee could mask). Every negative value of $r^{\mathrm{pf}}_i$ or $g^{\mathrm{pf}}_i$ implies it, because the clamped term and $\phi^{\mathrm{split}}(n')+\phi^{\mathrm{buy}}(n')-\phi^{\mathrm{paid}}_o$
are $\ge0$ ($\phi^{\mathrm{paid}}_o\le\phi^{\mathrm{acc}}_o\le\phi^{\mathrm{buy}}(n')$, F148), so a negative charge forces $m_{i,t}<p^{\mathrm{stop}}_i-\kappa^{\mathrm{out}}_i(n')\le p^{\mathrm{stop}}_i$. Example:
order $6$ sh at $50$, stop $49$, $\kappa^{\mathrm{out}}(n)=0.1+0.01n$, fee $\max(1,0.005k)$ per order, $N^{\mathrm{ex}}=2$; $2$ sh filled (fee $1$ paid), mark $52$,
$\Lambda_{i,t}=1.02$: worst loss $12.94$, $r^{\mathrm{pf}}_i=13.96$; the draft's $r^{\mathrm{open}}_i+L^{\mathrm{stop}}(6)=19.20$ over-charged by $5.24$, which includes the paid
fee $1$ a second time.

**Entry-fee booking state (critical closure correction, CLOSURE-REV-003).** For every entry order $o$ whose fees are not yet confirmed final —
pending, or venue-confirmed terminal — with cumulative filled quantity $q^{\mathrm{fill}}_o$ (execution reports):
$\phi^{\mathrm{acc}}_o=\phi^{\mathrm{buy}}_o(q^{\mathrm{fill}}_o)$, the largest entry fee its fills can cost (A-EXE-04); $\phi^{\mathrm{paid}}_o$, the part of it *booked into* $W_t$ at the cut —
debited in $C_t$ or recorded as payable in $Y_t$ of the same snapshot (A-AUTH-04), not the fees reported, assessed or expected; and
$\phi^{\mathrm{owed}}_o=\phi^{\mathrm{acc}}_o-\phi^{\mathrm{paid}}_o$, set to $0$ when the broker confirms the fees final **[F148]**. Domain: $0\le\phi^{\mathrm{paid}}_o\le\phi^{\mathrm{acc}}_o$. A negative
value, or more booked than the schedule allows ($\phi^{\mathrm{paid}}_o>\phi^{\mathrm{acc}}_o$, which violates A-EXE-04), is an impossible accounting state: $\alpha_t=0$, and
every charge uses $\phi^{\mathrm{paid}}_o$ clipped to $[0,\phi^{\mathrm{acc}}_o]$, so the excess is never credited. *Where it is charged, exactly once:* for a pending
order inside F145 and $C^{\mathrm{res}}$ (F144), through $\phi^{\mathrm{buy}}(n')-\phi^{\mathrm{paid}}_o=\big[\phi^{\mathrm{buy}}(n')-\phi^{\mathrm{acc}}_o\big]+\phi^{\mathrm{owed}}_o$; for a terminal order whose fees
are not final, as an F144 reservation $r=g=u=C^{\mathrm{res}}=\phi^{\mathrm{owed}}_o$ (notional and quantity $0$); held positions (F064–F066) carry no entry fee; F070
subtracts it through $C^{\mathrm{res}}_t$. *Conservation:* $\phi^{\mathrm{paid}}_o+\phi^{\mathrm{owed}}_o=\phi^{\mathrm{acc}}_o$; a booking of $b$ moves $b$ from $\phi^{\mathrm{owed}}_o$ to $\phi^{\mathrm{paid}}_o$ and
lowers $W_t$ by $b$, so $W_t-\sum_o\phi^{\mathrm{owed}}_o$ is unchanged **[F149]** (T-29): before booking the fee is a reservation, after booking it is in $W_t$,
never in both and never in neither. At `5c486f0` a terminal order dropped its owed fee ($W_{t+1}=F_t-\tfrac12$ with $100$ sh, buy fee $\max(1,0.005k)$,
sell fee $0$) and a reported but unbooked fee was counted as paid ($F_t-4.75$); 08 T-10 (vii), T-19.

**One exposure per instrument (A-SCOPE-05, added after review).** $\kappa^{\mathrm{out}}$ and $\Lambda$ are super-additive in quantity, so the
risk of adding $n$ to a held $q$ is **not** $r^{\mathrm{open}}(q)+L^{\mathrm{stop}}(n)$. Counterexample (exact): $q=100$ at $50$, stop $49$,
$\kappa^{\mathrm{out}}(n)=0.001n$, $\Lambda(n)=0.001n^2$; add $100$ at $50$: the per-lot charges total $r^{\mathrm{open}}(100)+L^{\mathrm{stop}}(100)=110+110=220$ but the
combined worst case is $230$, and an
untriggered outcome at $49.01$ already loses $228$. v0 therefore admits a new order on $i$ only if $q_{i,t}=0$ and $Q^{\mathrm{res}}_{i,t}=0$ (gate G11).
The incremental charge for a future add-on is F068
($=130$ in the example; $r^{\mathrm{open}}(100)-\Lambda_{i,t}+130=110-10+130=230$, so $r^{\mathrm{open}}+130=240$ is conservative by $\Lambda_{i,t}$, OC-1),
proposed only — pending orders on the same instrument are not yet covered (RQ-34).

## 6. Flow neutrality: unitisation

Units change only on external flows, at the reference NAV: $U_{t+1}=U_t+X_{t+1}/\nu^{\star}$ **[F069]** where $\nu^{\star}$ is the reference NAV
$\nu^{\mathrm{R}}=(E-\Lambda^{\mathrm{floor}})/U$ (F146) at the flow instant (**timing convention UNDEFINED — REQUIRES RESOLUTION**, RQ-31). Then $\nu^{\mathrm{R}}$ is
unaffected by flows; high-water marks and day/week references are defined on $\nu^{\mathrm{R}}$, drawdowns compare the current $\nu$ with them, and
floors are scaled by $U_t$ (F037–F042). Units are a carried reference: at an estimate-inclusive $\nu^{\star}$ a withdrawal redeems more units when
$\hat\Lambda$ is high and lowers every $U$-scaled floor ($E=10^6$, $\hat\Lambda=50{,}000$, $\Lambda^{\mathrm{floor}}=1{,}000$, $U=1{,}000$, withdrawal $95{,}000$:
$U=900$ and $K=45{,}810$, instead of $U=904{,}000/999$ and $K=41{,}400$; CLOSURE-REV-002, 08 T-28). Absolute-dollar quantities
($F^{\mathrm{abs}}$) are *not* scaled — a withdrawal can therefore legitimately drive $K_t\le0$.

## 7. Conditions under which $\mathbb E[\log(W_{t+1}/W_t)]$ is defined (Phase-2 gate for Phase 8)

1. $W_t>0$ (otherwise the ratio is undefined; every budget is already $0$).
2. $W_{t+1}(a)>0$ $\mathbb Q$-a.s. for **every** $\mathbb Q$ in the model / ambiguity set. For long-only, unlevered portfolios with prices
   $\ge0$, $X_{t+1}=0$, $\mathrm{Fin}_{t+1}=0$ and liquidation values $\ge-$exit fees (A-ACC-05), every position may become worthless, so
   $W_{t+1}\ge W^{\min}_{t+1}(a)$ with $W^{\min}_{t+1}(a)=C_t-Y_t-C^{\mathrm{res}}_t-L^{\mathrm{abs}}(n)-\sum_i\phi^{\mathrm{split}}_{i,0}(\bar q_i)-\bar A_{t+1}$ **[F070]**
   (closure form, AUD-038), where $C^{\mathrm{res}}_t$ is the remaining cash commitment of pending orders (F144: remaining quantity at the limit plus
   remaining entry fees; fees already booked and the filled part's cost are in $C_t$ and are not subtracted again) plus the owed entry fees of
   terminal orders (F148; omitting them gave $W_{t+1}=W^{\min}_{t+1}-1$, CLOSURE-REV-003), $\bar q_i$ is the largest quantity of
   $i$ that can be held in the period ($q_{i,t}$, or the total $n'$ of a pending order on $i$), $\phi^{\mathrm{split}}_{i,0}$ is F140 applied to the sell fee at price
   $0$ (a sale of part of a holding at price $0$ plus the remainder's valuation fee otherwise gives $W_{t+1}=W^{\min}_{t+1}-1$, REV-034), and
   $\bar A_{t+1}$ is an $\mathcal F_t$-measurable upper bound on
   $\mathrm{Accr}_{t+1}$. Every term is known at $\tau_t$ (revised after review: the earlier form contained future quantities and omitted flows). A
   sufficient condition is $W^{\min}_{t+1}(a)>0$ (T-19).
3. The argument is dimensionless (ratio); $\log W$ alone is dimensionally invalid (03).
4. Evaluation uses certified numerics (01 §9 item 4); `Decimal(0).ln()` returns `-Infinity` silently (observed), so domain checks precede
   evaluation.

Until an objective is chosen (RQ-13) these conditions are necessary, not sufficient.

## 8. Multi-period composition

$\nu_{T^{\mathrm{hor}}}/\nu_0=\prod_{t<T^{\mathrm{hor}}}\nu_{t+1}/\nu_t$, so $\log(\nu_{T^{\mathrm{hor}}}/\nu_0)=\sum_t\log(\nu_{t+1}/\nu_t)$ **[F071]** — additive per-period log growth is valid
**on the unitised NAV**, not on raw $W$ when flows occur. Time consistency of multi-period risk measures is an open question
(RQ-23) and is not needed for the one-step hard layer.

## 9. Unresolved objects in this document

- $\Lambda_{i,t}$ (liquidation-cost model beyond the floor F111): **UNDEFINED — REQUIRES RESOLUTION** (RQ-05).
- $\kappa^{\mathrm{out}}_i(n)$ (normal stop-execution cost beyond the floor F111): **UNDEFINED — REQUIRES RESOLUTION** (RQ-05).
- $\Gamma_i$ and horizon classes: **UNDEFINED — REQUIRES RESOLUTION** (RQ-04, D-09).
- Stop-trigger semantics (last trade vs bid vs consolidated): **UNDEFINED — REQUIRES RESOLUTION** (A-TRIG, RQ-21).
- Corporate-action restatement for types other than splits, and between decision and fill: **UNDEFINED — REQUIRES RESOLUTION** (FM-OPS-2).
- Add-on (scaling-in) risk with pending orders on the same instrument: **UNDEFINED — REQUIRES RESOLUTION** (RQ-34).
- Unitisation flow-timing convention: **UNDEFINED — REQUIRES RESOLUTION** (RQ-31).
- Reservation idempotency across re-evaluations: integration-contract obligation (§4b).
