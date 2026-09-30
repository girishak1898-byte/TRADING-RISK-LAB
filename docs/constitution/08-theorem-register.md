# 08 — Theorem Register (v0.1.1-draft)

Status vocabulary: **PROVED** (written proof of the stated proposition under the stated assumptions; *paper proof about the
specification*, pending independent review — Art. 14) · **PROVED BY CONSTRUCTION** (true because the specification defines it so;
the substantive risk is implementation conformance) · **DISPROVED** · **COUNTEREXAMPLE FOUND** · **REQUIRES ADDITIONAL
ASSUMPTION** · **UNDEFINED** · **NOT YET PROVEN**. No entry is promoted by tests. "Observed" marks a counterexample reproduced
numerically in this session (Python 3.11, exact rationals as reference).

## Summary

| ID | Name | Status |
|---|---|---|
| T-01 | Hard Risk Dominance | PROVED (specified composition); COUNTEREXAMPLE FOUND (naive float/Decimal-method composition) |
| T-02 | Integer Sizing Safety | PROVED (exact, monotone $g$); COUNTEREXAMPLE FOUND (closed form with non-linear fees; half-up; binary64) |
| T-03 | Hard Quantity Dominance | PROVED (monotone constraints); COUNTEREXAMPLE FOUND (non-monotone constraints) |
| T-04 | No-Trade Under Missing Authority | PROVED BY CONSTRUCTION; registry completeness NOT YET PROVEN |
| T-05 | Drawdown-Throttle / Wealth Monotonicity | PROVED (candidate forms) |
| T-06 | Maximum-Drawdown Shutdown | (a) PROVED; (b) "MDD ≤ $d^{\max}$" DISPROVED; (c) REQUIRES ADDITIONAL ASSUMPTION — PROVED under it (restated per epoch, R1) |
| T-07 | Liquidity Monotonicity | REQUIRES ADDITIONAL ASSUMPTION (monotone cost model; no $\Lambda$ credit in open risk) — PROVED under it; COUNTEREXAMPLE FOUND for the v0.1 form (R1) |
| T-08 | Transaction-Cost Monotonicity | PROVED (hard layer; own-cost perturbations of $\Delta J$); NOT YET PROVEN (market-wide cost perturbations of $\Delta J$ under concave $u$) |
| T-09 | Uncertainty Monotonicity | PROVED (feasibility-defined caps); COUNTEREXAMPLE FOUND (argmax-defined sizing) |
| T-10 | Capital-Floor Preservation | REQUIRES ADDITIONAL ASSUMPTION (tier assumptions, strengthened in R1) — PROVED under them; COUNTEREXAMPLE FOUND for the v0.1 hypotheses and without each hypothesis |
| T-11 | Risk-Reservation Conservation | PROVED (ledger model, atomicity, limit entry); COUNTEREXAMPLE FOUND (mid-based reservation, market orders, races, non-monotone fees) |
| T-12 | No-Trade Under Insufficient Robust Advantage | PROVED BY CONSTRUCTION; certificate validity UNDEFINED; P-12a PROVED + COUNTEREXAMPLE; P-12b PROVED; P-12c NOT YET PROVEN |
| T-13 | Safe-Action Membership | PROVED BY CONSTRUCTION (specification); implementation NOT YET PROVEN |
| T-14 | Replay Determinism | PROVED BY CONSTRUCTION (Art. 8); implementation NOT YET PROVEN |
| T-15 | Economic Cost Accounting Identity | PROVED (05 §2–§3) |
| T-16 | Expected-value sizing is cap sizing | PROVED |
| T-17 | Stop-Risk Insufficiency | PROVED (constructive; restated in R1 — bounded, though possibly $\gg W$, under an exit-cost floor) |
| T-18 | Comonotone (dependence-free) aggregation | PROVED |
| T-19 | Log-growth domain | PROVED ($W^{\min}$ corrected in R1) |
| T-20 | Floor invariance under hold | PROVED (static floor); DISPROVED (ratcheting floor, incl. daily/weekly calendar reset — R1) |
| T-21 | Cushion necessity and sufficiency | PROVED (under attainability of bounds) |
| T-22 | Binary64 floor safety condition | PROVED (condition); COUNTEREXAMPLE FOUND (outside it, observed) |
| T-23 | Sequential allocation order-dependence | PROVED (by example) |
| T-24 | Rounding Conservatism | PROVED |
| T-25 | Floor-breach decomposition | PROVED (missing premise added in R1) |
| T-26 | VaR non-subadditivity | PROVED (counterexample; classical) |
| OPEN-1 | Multi-step viability kernel equals tier invariant sets | NOT YET PROVEN |
| OPEN-2 | Certified-advantage lower bound validity | UNDEFINED (needs $J$, $\mathcal P$) |

**Revision R1 (v0.1 → v0.1.1).** An independent adversarial review of this register found 4 blockers, 9 major and 11 minor defects; the four
blocker counterexamples were re-verified in exact arithmetic before fixing. Blockers: T-10 failed for add-ons to held positions (super-additive exit
costs) → one exposure per instrument (G11); T-07 was false because open risk credited $\Lambda$ → credit removed (DC-5, OC-1); tier U under-charged
pending orders' fees → $Z^{\mathrm{res}}$ at full $L^{\mathrm{abs}}$; T-25 lacked its cushion premise. Major: triggered-but-unfilled stops and stop liveness (A-TRIG
broadened, A-STOPLIVE), per-execution fees (A-EXE-04), tier-G bound weaker than tier S (min form), withdrawals vs $F^{\mathrm{abs}}$ ($X=0$), T-21 hypotheses,
T-06(c) vacuity, T-17 over-statement, $W^{\min}$ with future terms and no flows, missing corporate-action term (05 §1). Minor items fixed in place.

Common standing assumptions (unless a theorem says otherwise): exact arithmetic in $\mathbb Q$; v0 scope (long-only, cash account,
$d=+1$); $g_k(\cdot,0)=0$; $\bar N<\infty$; lattice $\mathbb L=\delta_q\mathbb Z$.

---

### T-01 Hard Risk Dominance

**ASSUMPTIONS.** $R^{\mathrm{hard}}=(\min_{k\in\mathcal K_R}b_k)^{+}$ over the stop-risk budget family, computed exactly;
$\mathfrak s$ as in S-120; $R^{\mathrm{allow}}=\min(R^{\mathrm{hard}},\mathfrak s(R^{\mathrm{mod}}))$ where $\min$ is exact comparison on validated values.

**STATEMENT.** For every input (including $R^{\mathrm{mod}}$ = NaN, $\pm\infty$, negative, missing, wrong type):
$0\le R^{\mathrm{allow}}\le R^{\mathrm{hard}}$; and $R^{\mathrm{allow}}=0$ whenever a REQUIRED model output is invalid.

**PROOF.** $R^{\mathrm{hard}}\ge0$ by $(\cdot)^+$ and finite since each $b_k$ is finite. $\mathfrak s$ maps into $[0,\infty]$, and to $0$ for invalid
REQUIRED outputs. The minimum of a finite element of $[0,\infty)$ and an element of $[0,\infty]$ lies in $[0,R^{\mathrm{hard}}]$. ∎

**COUNTEREXAMPLE (naive forms).** (i) Python float `min(R_hard, nan)` → `R_hard`, `min(nan, R_hard)` → `nan` (observed): result depends
on argument order; NaN then reaches $\lfloor\cdot\rfloor$. (ii) `R_hard.min(Decimal('NaN'))` → `R_hard` (observed): numerically inside the
envelope, but a REQUIRED model's failure silently becomes "no model limit" (violates Art. 4). (iii) Without $(\cdot)^+$: exhausted
budgets give $R^{\mathrm{hard}}<0$ and $\lfloor R/\ell\rfloor<0$ — a negative quantity readable as a sell/short.

**NUMERICAL IMPLICATION.** Sanitise at the boundary; exact types; explicit clamp; never IEEE minNum/maxNum semantics.

**TESTABLE INVARIANT.** ∀ generated snapshots: `0 ≤ R_allow ≤ R_hard`. Oracle (corrected after review): invalid `R_mod` (NaN, sNaN, ±Inf, None,
non-numeric, $>\bar M$) ⇒ `R_allow == 0` if REQUIRED, `== R_hard` if OPTIONAL; finite negative ⇒ `0` in both cases; finite in $[0,\bar M]$ ⇒
`min(R_hard, R_mod)`. Property-based + fuzz.

---

### T-02 Integer Sizing Safety

**ASSUMPTIONS.** $g:\mathbb L_{\ge0}\to\mathbb Q$ non-decreasing, $g(0)=0$; $b\in\mathbb Q$; exact arithmetic;
$Q:=\max(\{0\}\cup\{n\in\mathbb L_{>0}:n\le\bar N,\ g(n)\le b\})$.

**STATEMENT.** (a) $Q\in\mathbb L_{\ge0}$. (b) $Q>0\Rightarrow g(Q)\le b$. (c) *Downward closure (Lemma L-1):* $0<n\le Q,\ n\in\mathbb L\Rightarrow g(n)\le b$.
(d) Maximality: $Q+\delta_q\le\bar N\Rightarrow g(Q+\delta_q)>b$. (e) Linear case $g(n)=n\ell$, $\ell>0$, $b\ge0$:
$Q=\min(\bar N,\ \delta_q\lfloor b/(\delta_q\ell)\rfloor)$.

**PROOF.** (a),(b),(d): the candidate set is finite ($\mathbb L\cap[0,\bar N]$) and contains $0$; $Q$ is its maximum. (c) $g(n)\le g(Q)\le b$ by
monotonicity. (e) $\delta_qk\,\ell\le b\iff k\le b/(\delta_q\ell)\iff k\le\lfloor b/(\delta_q\ell)\rfloor$ for integer $k$. ∎

**COUNTEREXAMPLES (observed).**
- *Closed form with non-linear fees.* $L(n)=0.10\,n+2\max(1.00,\,0.005\,n)$ (minimum commission each side), $b=2.50$. Naive
  $\lfloor 2.50/(0.10+0.01)\rfloor=22$ gives $L(22)=4.20>2.50$. True $Q=5$ ($L(5)=2.50$).
- *Half-up rounding.* $b=1000.00$, $\ell=2.90$: $b/\ell=344.83\ldots$; half-up $345$, loss $1000.50>b$; floor $344$, loss $997.60$.
- *Binary64 division.* $b=172{,}808{,}193.53$, $\ell=65.68583269$: float $\lfloor b/\ell\rfloor=2{,}630{,}829$, exact $2{,}630{,}828$; the float
  quantity is infeasible (see T-22 for the condition under which this cannot occur).
- *Zero/negative per-share loss.* $\ell\le0$ ⇒ $g(n)\le0\le b$ for all $n$ ⇒ $Q=\bar N$: unbounded sizing. Gate G7 must reject it.

**NUMERICAL IMPLICATION.** Compute $Q$ by exact monotone search, or by the closed form only where linearity is proved. **Floor only**: every
round-to-nearest mode (half-up, and Python's default half-even) gives $345$ in the example above. Never binary64 on the authority path.

**TESTABLE INVARIANT.** `g(Q) ≤ b` and (`Q + δ > N̄` or `g(Q + δ) > b`) — the maximality witness is part of the evidence record;
`Q ∈ 𝕃, Q ≥ 0`; differential test against brute-force enumeration for small $\bar N$.

---

### T-03 Hard Quantity Dominance

**ASSUMPTIONS.** Finite $\mathcal K$; each $g_k$ as in T-02; gates are 0/1; $Q_k$ per T-02 with $b^{\mathrm{allow}}_k$;
$Q^{\mathrm{hard}}=\min_kQ_k$ if all gates pass, else $0$. Verifier $V$: given any proposal $\tilde n$ (possibly non-numeric), return
$\max\{n\in\mathbb L_{\ge0}: n\le\min(\tilde n,Q^{\mathrm{hard}})\}$ if $\tilde n$ is a finite number $\ge0$, else $0$.

**STATEMENT.** (a) $\{0\}\cup\{n\in\mathbb L_{>0}:n\le\bar N,\ \forall k,\ g_k(n)\le b_k\}=\mathbb L\cap[0,Q^{\mathrm{hard}}]$ (gates passing). (b) For reals $x_k$,
$\lfloor\min_kx_k\rfloor_{\mathbb L}=\min_k\lfloor x_k\rfloor_{\mathbb L}$. (c) $0\le V(\tilde n)\le Q^{\mathrm{hard}}$ and $V(\tilde n)$ satisfies every hard constraint.

**PROOF.** (a) By L-1 each feasible set is $\mathbb L\cap[0,Q_k]$; the intersection of initial segments is the initial segment to the
minimum. (b) $\lfloor\cdot\rfloor_{\mathbb L}$ is non-decreasing, so $\lfloor\min x\rfloor\le\lfloor x_k\rfloor\ \forall k$; and $\min_k\lfloor x_k\rfloor$ is a lattice point
$\le\min_kx_k$, hence $\le\lfloor\min x\rfloor$. (c) By construction and (a). ∎

**COUNTEREXAMPLES (non-monotone constraints).**
- *Minimum order notional* $n\,p\ge\$1000$ with $p=50$: feasible set $\{0\}\cup[20,Q]$ — not an initial segment; "min of caps" is meaningless.
  Remedy: post-filter (06 §5).
- *Per-order tiered fee schedule (hypothetical):* $\phi(n)=0.005n$ for $n<1000$, $0.003n$ for $n\ge1000$; $\ell=0.5$; $b=504$.
  $g(998)=503.99$, $g(999)=504.495$, $g(1000)=503.00$, $g(1001)=503.503$, $g(1002)=504.006$. Feasible: $\{\dots,998,1000,1001\}$, $999$ infeasible.
  An order sized at $1001$ that **partially fills 999** consumes $504.495>b$ — non-monotone fees break partial-fill safety (also T-11).

**NUMERICAL IMPLICATION.** Monotonicity of every $g_k$ (incl. fee schedules) is a *precondition* checked when a schedule version is
loaded; a non-monotone schedule is replaced by its monotone upper envelope $\bar g(n)=\max_{m\le n}g(m)$ (conservative) or rejected.

**TESTABLE INVARIANT.** $\forall k:\ g_k(Q^{\mathrm{fin}})\le b_k$ and $Q^{\mathrm{fin}}\le Q_k$; $V$ fuzzed with NaN/∞/negative/huge/float/non-lattice
proposals; independent slow checker re-evaluates all constraints (differential).

---

### T-04 No-Trade Under Missing Authority

**ASSUMPTIONS.** $\mathcal R^{\mathrm{req}}$ finite; each validator decides presence, type, domain, freshness ($\mathrm{age}\le\mathrm{TTL}$), scope
($A_{\mathrm{id}}$) and internal consistency; $\alpha=\bigwedge$ validators; $\mathcal D$ evaluates G1 first.

**STATEMENT.** $\alpha(\mathsf S)=0\Rightarrow\mathcal D(\mathsf S,\cdot)=$ NO\_TRADE with $\mathsf{rc}\supseteq\{\text{failed validators}\}\neq\varnothing$.

**PROOF.** By construction of $\mathcal D$. ∎

**SUBSTANTIVE GAP.** The theorem is only as strong as $\mathcal R^{\mathrm{req}}$ is complete. Completeness criterion (NOT YET PROVEN):
*read-set* of the computation (every field any $g_k$, $b_k$, gate or derivation reads) $\subseteq\mathcal R^{\mathrm{req}}$.

**COUNTEREXAMPLE.** A deserialiser that defaults a missing $R^{\mathrm{res}}$ to $0$ passes presence checks while authority is absent;
two strategies then double-spend the budget. Hence absence ≠ zero at the schema level (Art. 4).

**NUMERICAL IMPLICATION.** None beyond parse rules.

**TESTABLE INVARIANT.** For every valid snapshot and every single-field mutation {delete, null, stale, wrong scope, wrong type,
out-of-domain}: NO\_TRADE and the reason names that field. Instrumented read-set $\subseteq\mathcal R^{\mathrm{req}}$ (static + dynamic check).

---

### T-05 Drawdown-Throttle / Wealth Monotonicity

**ASSUMPTIONS.** Two snapshots $x,x'$ identical except for a *consistent* cash reduction $\Delta\ge0$
($C'=C-\Delta$, $BP'=BP-\Delta$, $C^{\mathrm{avail}\prime}=C^{\mathrm{avail}}-\Delta$), so $W'=W-\Delta$; $H_t=\max(H_{t-1},\nu_t)$;
$B$ is one of B1–B4 (06 §4); floor parameters $d^{\max},\ell^{\mathrm{day}},\ell^{\mathrm{wk}}\in(0,1)$, $\eta^{\mathrm{lock}}\in[0,1)$.

**STATEMENT.** $K$, $B$, every $b_k$, and $Q^{\mathrm{hard}}$ are non-decreasing in $W$ (hence non-increasing in $DD$ below the prior HWM; above it
$DD\equiv0$ while $K$ still varies). The induced throttle $\vartheta_K$ (06 §7) is continuous and non-increasing on $[0,d^{\max}]$ and defined as $0$ beyond.

**PROOF.** $F^{\mathrm{abs}}$ does not depend on $W$; $F^{\mathrm{day}}$, $F^{\mathrm{wk}}$ do not, except at the first epoch of a day/week, where they have slope
$1-\ell^{\mathrm{day}}$ / $1-\ell^{\mathrm{wk}}\in(0,1)$; $\nu^{\mathrm{ref}}$ is assumed independent of $W$; the rule $H_t=\max(H_{t-1},\nu_t)$ presumes the current epoch
is HWM-eligible (RQ-03 — if not, $F^{\mathrm{dd}}$ has slope $0$ and the conclusion is unchanged). $F^{\mathrm{dd}}=(1-d^{\max})U\max(H_{t-1},\nu)$ has slope $0$
below the prior HWM and $1-d^{\max}$ above it; $F^{\mathrm{lock}}$ has slope $0$ or $\eta^{\mathrm{lock}}$. Hence $K=W-\max(\cdots)$ has slope in
$\{1,d^{\max},1-\eta^{\mathrm{lock}},\ell^{\mathrm{day}},\ell^{\mathrm{wk}}\}\subset[0,1]$ piecewise: non-decreasing. B1–B4 are non-decreasing. Each $b_k$ is a non-decreasing
function of $(B,K,BP^{\mathrm{avail}})$ minus terms independent of $W$; $\min$, $(\cdot)^+$ and $Q_k$ (as a function of $b_k$) preserve
monotonicity; gates G3 ($K>0$) and G4 ($DD<d^{\max}$) are monotone. Derivative of $\vartheta_K$: 06 §7. ∎

**COUNTEREXAMPLE (rejected families).** "Recovery boost" rules (raise risk after losses) violate the statement; limits on realised
P&L only violate it when unrealised losses grow (DC-4); multiplicative per-loss rules are not functions of $(W,H)$.

**NUMERICAL IMPLICATION.** Directed rounding preserves monotonicity (floor and ceiling are monotone).

**TESTABLE INVARIANT.** Metamorphic: consistent cash reduction ⇒ each $b_k$ and $Q^{\mathrm{hard}}$ do not increase. (Inconsistent
perturbations, e.g. $C$ changed but $BP$ not, are invalid test inputs.)

---

### T-06 Maximum-Drawdown Shutdown

**ASSUMPTIONS.** Gate G4; $F^{\mathrm{dd}}$ included in $F$.

**STATEMENT.** (a) $DD_t\ge d^{\max}\Rightarrow Q^{\mathrm{hard}}=0$. (b) "$MDD_t\le d^{\max}$ for all paths." (c) *(restated after review)* Suppose that at
every epoch $t$, after any adjustments made **before** the cut $\mathsf S_t$ by an external risk-reducing authority (stop modifications and/or
risk-reducing sales), $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t\le K_t$ holds, and that every period satisfies the tier-S hypotheses of T-10. Then
$DD_t\le d^{\max}$ at every epoch.

**PROOF.** (a) G4 fails; independently $K\le W-F^{\mathrm{dd}}=UH(d^{\max}-DD)\le0$ (defence in depth). (c) T-10 with $n=0$ gives
$W_{t+1}\ge F_t\ge(1-d^{\max})H_tU$. If $\nu_{t+1}\le H_t$ then $H_{t+1}=H_t$ and $DD_{t+1}\le d^{\max}$; otherwise $DD_{t+1}=0$. ∎ The bound holds at
epochs only; intra-period drawdown is not covered. Trailing by stop modification alone can be infeasible (if $K_t/q_i<\kappa^{\mathrm{out}}$ the required stop
is above the mark), so the external authority must be able to sell.
(b) **DISPROVED**:

**COUNTEREXAMPLES to (b).** *Gap:* $d^{\max}=10\%$, $W=H=100{,}000$, one long of $1{,}000$ sh at $100$ with stop $90$ (open risk $\approx K=10{,}000$);
overnight open at $70$ ⇒ $W=70{,}000$, $DD=30\%$. *Ratchet without gap:* $d^{\max}=10\%$, $W=H=100$, cash $50$, one share at $50$ with stop
$40.5$ ($r=9.5\le K=10$). Price rises to $90$: $W=H=140$, $K=14$, $r=49.5>K$. Price falls to $40.5$, stop fills exactly: $W=90.5$,
$DD=1-90.5/140=35.4\%$ — no new trade, A-STOP held exactly. *Halt:* exit impossible during a halt; same effect as a gap.

**NUMERICAL IMPLICATION.** None specific.

**TESTABLE INVARIANT.** (a) property test; (c) Monte Carlo on paths satisfying the tier-S hypotheses with the pre-cut adjustment rule applied ⇒
$DD\le d^{\max}$ at epochs; paths violating them are reported as assumption violations, not as failures of (c).

---

### T-07 Liquidity Monotonicity

**ASSUMPTIONS.** $\kappa^{\mathrm{out}}_i$, $\Lambda_i$ non-increasing in $\mathrm{ADV}_i$ and non-decreasing in $\varsigma_i$ (property of the chosen cost
model — e.g. a square-root form $\propto\hat\sigma\sqrt{n/\mathrm{ADV}}$ is decreasing in ADV); H12–H13 budgets increasing in ADV; G5;
**open-risk terms carry no $\Lambda$ credit** (DC-5 revised, OC-1).

**STATEMENT.** Holding all else fixed, $Q^{\mathrm{hard}}$ is non-decreasing in the ADV of any instrument and non-increasing in its spread.

**PROOF.** Higher ADV / lower spread lowers $\Lambda$ (raising $W$, hence $B$ and $K$), lowers $\kappa^{\mathrm{out}}$ (lowering every consumption and every
open-risk term), and raises H12–H13 budgets. Every $b_k$ is non-decreasing and every $g_k$ non-increasing in liquidity; feasible sets are
nested; $\min$ preserves order; G5 is monotone in $\varsigma$. ∎

**COUNTEREXAMPLE (the pre-review version, with $\Lambda$ credit in open risk — found by independent review, re-verified exactly).** Hold 1,000 sh at
$50$, stop $45$, $\kappa^{\mathrm{out}}\equiv0.05$, cash $200{,}000$, $B=W$, $f^{\mathrm{trd}}=f^{\mathrm{port}}=2\%$, new order $L^{\mathrm{stop}}=5.05n$. Low ADV ($\Lambda=500$):
$W=249{,}500$, $R^{\mathrm{open}}=4{,}550$, H2 budget $440$, $Q=87$. High ADV ($\Lambda=100$): $W=249{,}900$, $R^{\mathrm{open}}=4{,}950$, budget $48$, $Q=9$. The
credit makes $\partial(f B-R^{\mathrm{open}})/\partial\Lambda=1-f>0$: worse liquidity, larger budget. Other failures: a regression-fitted impact model
non-monotone in ADV; displayed depth used as a cap (volatile, manipulable — inadmissible in the hard layer).

**NUMERICAL IMPLICATION.** If $\sqrt{\ }$ is used, certified upper bounds only (01 §9.4).

**TESTABLE INVARIANT.** Metamorphic: ADV ↑ ⇒ $Q^{\mathrm{hard}}$ not ↓; spread ↑ ⇒ $Q^{\mathrm{hard}}$ not ↑ — for the opportunity's instrument **and for held
instruments**; cost-model monotonicity verified on a grid when a model version is loaded.

---

### T-08 Transaction-Cost Monotonicity

**ASSUMPTIONS.** Pointwise cost increase: $\phi'\ge\phi$, $\kappa^{\mathrm{out}\prime}\ge\kappa^{\mathrm{out}}$; for part (b), $J(a)=\mathbb E[u(W_{t+1}(a))]$
with $u$ non-decreasing and the perturbation affecting only the fills generated by $a$.

**STATEMENT.** (a) $Q^{\mathrm{hard}\prime}\le Q^{\mathrm{hard}}$. (b) $\Delta J'(a)\le\Delta J(a)$.

**PROOF.** (a) $L^{\mathrm{stop}},L^{\mathrm{gap}},L^{\mathrm{abs}}$ and H14 consumption increase pointwise; feasible sets shrink. (b) $W_{t+1}(a^{\varnothing})$ is
unchanged and $W_{t+1}(a)$ decreases pointwise (costs enter $G$ negatively); $u$ non-decreasing. ∎

**OPEN.** Market-wide perturbations (a spread widening that also raises exit costs of existing positions) change $J(a^{\varnothing})$ too;
for concave $u$ the sign of the change in $\Delta J$ is NOT YET PROVEN.

**TESTABLE INVARIANT.** Metamorphic on fee schedule and $\kappa^{\mathrm{out}}$ scaling.

---

### T-09 Uncertainty Monotonicity

**ASSUMPTIONS.** Model-layer budget defined by robust feasibility:
$b^{\mathrm{mod}}_k(\mathcal P)=\sup\{b:\ \forall\mathbb Q\in\mathcal P,\ c_{\mathbb Q}(b)\ \text{holds}\}$; nested sets $\mathcal P\subseteq\mathcal P'$.

**STATEMENT.** $b^{\mathrm{mod}}_k(\mathcal P')\le b^{\mathrm{mod}}_k(\mathcal P)$, hence $Q^{\mathrm{fin}}(\mathcal P')\le Q^{\mathrm{fin}}(\mathcal P)$; also
$\inf_{\mathcal P'}J\le\inf_{\mathcal P}J$.

**PROOF.** A constraint required for all $\mathbb Q\in\mathcal P'$ is required for all $\mathbb Q\in\mathcal P$; the feasible set of $b$ shrinks. ∎

**COUNTEREXAMPLE (argmax sizing is not monotone).** Actions $n\in\{0,1,2\}$. $\mathbb Q_1$: $J=(0,5,4)$, argmax $1$. Add $\mathbb Q_2$: $J=(0,1,3)$.
Robust $\min_{\mathbb Q}J=(0,1,3)$, argmax $2$. Enlarging the ambiguity set **increased** the chosen size.

**NUMERICAL IMPLICATION.** Safety-relevant model outputs MUST be feasibility-defined caps; argmax outputs are proposals inside caps.

**TESTABLE INVARIANT.** Nested radii $\varepsilon'>\varepsilon$ ⇒ $b^{\mathrm{mod}}(\varepsilon')\le b^{\mathrm{mod}}(\varepsilon)$.

---

### T-10 Capital-Floor Preservation (one period, tiered)

**ASSUMPTIONS (tier S; revised after review).** Long-only; **one exposure per instrument** (A-SCOPE-05, gate G11); $X_{t+1}=0$ (unitisation does *not*
protect $F^{\mathrm{abs}}$); $\mathrm{Fin}=0$; $\mathrm{Accr}=0$; $\mathrm{Inc}\ge0$; A-ACC-04 ($\Lambda=\sum_i\Lambda_i$); A-MKT-05 (entry fills $\le p^{\mathrm{lim}}$, quantity $\le$
reserved); **A-STOPLIVE** (each entry fill is protected by its stop from the instant of the fill); **A-STOP** (a triggered stop exits at
$\ge p^{\mathrm{stop}}-\kappa^{\mathrm{out}}$); **A-TRIG** (every quantity still held at $\tau_{t+1}$ — untriggered, or triggered but not fully filled — has liquidation
value $\ge q\,(p^{\mathrm{stop}}-\kappa^{\mathrm{out}}(q))-\phi^{\mathrm{sell}}(q)$); **A-EXE-04** (fees over all fills of one order of total quantity $n$ are
$\le\phi(n)$); no other orders; open risk per DC-5 (no $\Lambda$ credit) with no anomaly.

**STATEMENT.** $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t\ \Rightarrow\ W_{t+1}\ge F_t$. Tier G: same with $g^{\mathrm{open}},G^{\mathrm{res}},L^{\mathrm{gap}}$
under A-GAP (exit bound $p^{\mathrm{gx}}$, 05 §5). Tier U: same with $Z^{\mathrm{open}}=\sum u^{\mathrm{open}}$, $Z^{\mathrm{res}}$ (pending orders at full
$L^{\mathrm{abs}}$), $L^{\mathrm{abs}}$, under A-MKT-01 and A-ACC-05 ($\Lambda_i\le q_im_i+\phi^{\mathrm{sell}}_{i,0}(q_i)$).

**PROOF (tier S).** Decompose $W_{t+1}-W_t$ by instrument (05 §2; A-ACC-04 makes $\Lambda$ additive across instruments and G11 makes each instrument
a single exposure). Held $i$, fully exited: change $=q(f-m_t)-\phi^{\mathrm{sell}}+\Lambda_{i,t}\ge-[q(m_t-p^{\mathrm{stop}}+\kappa^{\mathrm{out}})+\phi^{\mathrm{sell}}]=-r^{\mathrm{open}}_i$
(using $\Lambda_{i,t}\ge0$). Held $i$, not fully exited: change $=(qm_{t+1}-\Lambda_{i,t+1})-(qm_t-\Lambda_{i,t})\ge-r^{\mathrm{open}}_i$ by A-TRIG and
$\Lambda_{i,t}\ge0$ (a partial exit splits into the two cases with fees bounded by A-EXE-04). New or pending order on a fresh instrument filled
$e\le n$ at $f^{\mathrm{in}}\le p^{\mathrm{lim}}$ and protected from the fill (A-STOPLIVE): change $\ge-L^{\mathrm{stop}}(e)\ge-L^{\mathrm{stop}}(n)$ by the same two
cases and monotonicity; unfilled: $0$. Summing and adding $\mathrm{Inc}\ge0$: $W_{t+1}\ge W_t-(R^{\mathrm{open}}+R^{\mathrm{res}}+L^{\mathrm{stop}}(n))\ge F_t$.
Tiers G, U: identical with the corresponding exit bounds. ∎

**COUNTEREXAMPLES (each hypothesis removed; the first five found by independent review and re-verified exactly).**
- *Add-on (no G11):* hold $100$ at $50$, stop $49$, $\kappa^{\mathrm{out}}(n)=0.001n$, $\Lambda(n)=0.001n^2$ ($r=110$); add $100$ at $50$ ($L=110$);
  $K=220$; untriggered close at $49.01$ ⇒ $\Delta W=-228$, floor breached by $8$ (by $18$ under the pre-review $\Lambda$ credit), while A-TRIG holds for the combined holding ($9{,}762\ge9{,}760$).
- *Pending order at notional (tier U):* pending 100 @ 5 charged $500$; new 100 @ 5.94 with \$1 minimum commissions, $L^{\mathrm{abs}}=596$; $K=1{,}096$;
  both fill, price → 0, both sold: $W_{t+1}=F_t-2$.
- *Triggered but unfilled at $\tau_{t+1}$ (old A-TRIG):* hold $100$ at $50$, stop $49$, $\kappa=0.1$ ($r=110$); trigger just before $\tau_{t+1}$, mark $45$: $W$ falls $500$.
- *Per-execution fees (no A-EXE-04):* $\phi=\max(1,0.005k)$ per execution; a 100-share exit filled 34/33/33 pays $3>\phi(100)=1$.
- *Withdrawal (no $X=0$):* $F=F^{\mathrm{abs}}=90$, $W=100$, $r=10=K$, $X=-5$, stop fills at its bound: $W_{t+1}=85<90$.
- *Gap* (A-STOP fails): T-06 gap example. *Race* (reservation not atomic): two decisions from one snapshot each sized to $L=K$ ⇒ loss $2K$.
  *Missing stop treated as zero risk* (violates D-06): unbounded breach. *Non-monotone fees:* T-03 example.

**NUMERICAL IMPLICATION.** Sums rounded up, $K$ rounded down (T-24).

**TESTABLE INVARIANT.** Simulator with adversarial paths drawn *inside* the tier's disturbance set (including the comonotone all-stops scenario,
triggered-unfilled states and split fills) ⇒ $W_{t+1}\ge F_t$ always; each counterexample above is a regression test that must *fail* when its
hypothesis is removed; paths outside are labelled assumption violations and their breach magnitude logged.

---

### T-11 Risk-Reservation Conservation

**ASSUMPTIONS.** Ledger per budget family with local variables available $Av$, reserved $Rs$, open $Op$ and total $T$; transitions
RESERVE($x$) [requires $x\le Av$, atomically with the version read], FILL, CANCEL/EXPIRE/REJECT, CLOSE; reservations computed at
$p^{\mathrm{lim}}$ with the order's stop; full reservation held until the order is terminal; $g$ monotone (T-03).

**STATEMENT.** (a) $Av+Rs+Op=T$ after every transition (for fixed $T$). (b) $Av\ge0$ always. (c) *Dominance:* for any fill $e\le n$ at
$f\le p^{\mathrm{lim}}$, realised open risk $\le$ reserved $L^{\mathrm{stop}}(n)$. (d) On terminal state, release $L^{\mathrm{stop}}(n)-L^{\mathrm{stop}}(e)\ge0$.

**PROOF.** (a) Each transition moves an amount between components. (b) Induction with the atomic guard. (c) Entry at $f\le p^{\mathrm{lim}}$
and monotonicity: $e(f-p^{\mathrm{stop}}+\kappa^{\mathrm{out}}(e))+\phi^{\mathrm{buy}}(e)+\phi^{\mathrm{sell}}(e)\le L^{\mathrm{stop}}(e)\le L^{\mathrm{stop}}(n)$, with fees per order (A-EXE-04). (d) Monotonicity. ∎

**COUNTEREXAMPLES.** *Reservation at mid:* realised risk exceeds reservation by $e(p^{\mathrm{lim}}-m)$. *Market order:* no price bound, (c) fails.
*Non-atomic check-then-reserve:* $Av=1000$, two concurrent reserves of $1000$ ⇒ $Av=-1000$. *Stop widened after fill:* open risk grows
beyond reservation unless re-reserved. *Non-monotone fees:* T-03.

**SCOPE NOTE.** The engine is pure; (a),(b),(d) are properties of the external ledger. The engine's obligations: consume $Rs$ as input;
emit the reservation vector at worst-case entry (06 §8).

**TESTABLE INVARIANT.** Ledger replay property tests with random interleavings; engine: emitted reservation $\ge L^{\mathrm{stop}}(e)$ for all
$e\le Q$ and all $f\le p^{\mathrm{lim}}$ (enumerated for small cases).

---

### T-12 No-Trade Under Insufficient Robust Advantage

**ASSUMPTIONS.** A certificate $\mathrm{LB}_t(a)$ and margin $\varepsilon^{\min}\ge0$; decision rule "trade $a$ only if $\mathrm{LB}_t(a)>\varepsilon^{\min}$".

**STATEMENT.** $\mathrm{LB}_t(a)\le\varepsilon^{\min}\Rightarrow$ $a$ is not chosen; a TRADE decision implies $\mathrm{LB}_t(a)>\varepsilon^{\min}$.

**PROOF.** By construction. ∎ Validity of $\mathrm{LB}_t$ ($\mathrm{LB}_t\le\Delta J_t$ with stated confidence) is **UNDEFINED** (OPEN-2).

**P-12a (infimum of difference).** For any family $(A_{\mathbb Q},B_{\mathbb Q})_{\mathbb Q\in\mathcal P}$ with $\inf A$ and $\inf B$ finite:
$\inf_{\mathbb Q}(A_{\mathbb Q}-B_{\mathbb Q})\le\inf_{\mathbb Q}A_{\mathbb Q}-\inf_{\mathbb Q}B_{\mathbb Q}$.
*Proof:* for any $\mathbb Q'$, $\inf(A-B)\le A_{\mathbb Q'}-B_{\mathbb Q'}\le A_{\mathbb Q'}-\inf B$; take $\inf$ over $\mathbb Q'$. ∎
*Counterexample to using the right-hand side ($\mathrm{LB}^{\mathrm{naive}}$):* $\mathbb Q_1$: $J(a)=1$, $J(a^{\varnothing})=0$; $\mathbb Q_2$: $J(a)=2$,
$J(a^{\varnothing})=3$. $\inf J(a)-\inf J(a^{\varnothing})=1-0=1>0$ ("certified"), but $\inf(J(a)-J(a^{\varnothing}))=\min(1,-1)=-1$: under $\mathbb Q_2$ not
trading is better.

**P-12b (additive error bounds).** If $\lvert\hat J(a)-J(a)\rvert\le e_a$ and $\lvert\hat J(a^{\varnothing})-J(a^{\varnothing})\rvert\le e_0$ surely, then
$\hat J(a)-\hat J(a^{\varnothing})-e_a-e_0\le\Delta J(a)$. If each bound holds with probability $\ge1-\delta_a$, $\ge1-\delta_0$, the conclusion holds with
probability $\ge1-\delta_a-\delta_0$ (union bound). Over $m$ decisions the family-wise error is up to $m(\delta_a+\delta_0)$. *Proof:* triangle
inequality; union bound. ∎

**P-12c (correlated errors).** When the same parameter error drives $\hat J(a)$ and $\hat J(a^{\varnothing})$, bounding them separately is
conservative; bounding $\hat J(a)-\hat J(a^{\varnothing})$ directly can be tighter. (Remark; quantification NOT YET PROVEN.)

**NUMERICAL IMPLICATION.** $\varepsilon^{\mathrm{num}}$ from certified evaluation at the *returned* action; solver tolerances are not part of the certificate.

**TESTABLE INVARIANT.** Decision TRADE ⇒ recorded $\mathrm{LB}>\varepsilon^{\min}$; unit test reproducing the P-12a counterexample.

---

### T-13 Safe-Action Membership

**STATEMENT.** For every input, the output action is $a^{\varnothing}$ or an element of $\mathcal A^{\mathrm{safe}}(x_t)$, and $\mathcal D$ terminates.

**PROOF.** The last step before emission is $V$ (T-03(c)); every other path emits $a^{\varnothing}$ (Art. 18). Search terminates in
$\lceil\log_2(\bar N/\delta_q)\rceil+1$ exact evaluations per constraint. ∎ (Specification-level.)

**TESTABLE INVARIANT.** Independent slow oracle re-checks membership of every emitted TRADE (differential testing); fuzzed inputs
never raise out of $\mathcal D$.

### T-14 Replay Determinism

**STATEMENT.** $\mathcal D$ applied twice to byte-identical $(\mathsf S_t,o,\theta,\mathsf v)$ yields byte-identical records, across processes, machines
and restarts. **PROOF.** Art. 8 + 01 §9.11. ∎ **TESTABLE INVARIANT.** Golden-record replay across processes with different hash seeds,
locales and pre-mutated global decimal contexts.

### T-15 Economic Cost Accounting Identity — see 05 §2–§3 (PROVED). **TESTABLE INVARIANT:** for simulated ledgers, both sides agree exactly.

### T-16 Expected-value sizing is cap sizing

**STATEMENT.** If $J(n)=\mathbb E[W_{t+1}(n\mathbf 1_i)-W_t]$ is affine in $n$ on $\mathbb L\cap[0,Q^{\mathrm{hard}}]$ (linear costs, no impact), then
$\arg\max J\ni 0$ or $Q^{\mathrm{hard}}$. **PROOF.** An affine function on an interval attains its maximum at an endpoint. ∎
**IMPLICATION.** Under expected-value objectives the caps *are* the sizing rule; risk preferences must come from the caps or from
a concave objective.

### T-17 Stop-Risk Insufficiency (restated after review)

**STATEMENT.** (a) For the naive envelope $Q=\lfloor f^{\mathrm{trd}}W/\ell^{\mathrm{stop}}\rfloor$ with $\ell^{\mathrm{stop}}$ the stop distance only, admissible notional is
unbounded as $\ell^{\mathrm{stop}}\to0$ and a gap of fraction $\Gamma$ can lose more than $W$. (b) For H1 with a per-share exit-cost floor
$\kappa^{\mathrm{out}}\ge\kappa_0>0$ (or a per-share fee), notional is bounded by $f^{\mathrm{trd}}Wp/\kappa_0$ — bounded, but possibly $\gg W$; a gap loss $>W$
remains possible iff $\ell^{\mathrm{stop}}+\kappa_0<f^{\mathrm{trd}}\Gamma p$ (approximately).
**PROOF.** (a) Let entry $p$, stop $p-\ell^{\mathrm{stop}}$, $Q=f^{\mathrm{trd}}W/\ell^{\mathrm{stop}}$ (take it integral). A gap exit at $(1-\Gamma)(p-\ell^{\mathrm{stop}})$ loses
$\Gamma p+(1-\Gamma)\ell^{\mathrm{stop}}\ge\Gamma p$ per share, total $\ge f^{\mathrm{trd}}W\Gamma p/\ell^{\mathrm{stop}}>W$ whenever $\ell^{\mathrm{stop}}<f^{\mathrm{trd}}\Gamma p$.
Numeric: $W=100{,}000$, $f^{\mathrm{trd}}=1\%$, $\ell^{\mathrm{stop}}=0.01$, $p=50$ ⇒ $Q=100{,}000$ sh, notional $5{,}000{,}000$; with $\Gamma=5\%$ the loss is
$250{,}950\approx2.5W$. (b) $n(\ell^{\mathrm{stop}}+\kappa_0)\le f^{\mathrm{trd}}W$. Example of (b) with no breach: $f^{\mathrm{trd}}=0.1\%$, $p=10$, $\kappa_0=0.01$ ⇒
notional $\le W$ for every stop distance. ∎
**IMPLICATION.** Stop-risk budgets alone do not bound notional usefully; H5–H11 are necessary.

### T-18 Comonotone (dependence-free) aggregation

**STATEMENT.** If $\mathcal L_i\le b_i$ surely for each $i$, then $\sum_i\mathcal L_i\le\sum_ib_i$ for every joint law; and if each bound is attainable
with no dependence restriction, $\sup\big(\sum_i\mathcal L_i\big)=\sum_ib_i$. **PROOF.** Summation; the joint scenario where every
bound is attained is admissible. ∎ **IMPLICATION.** The hard layer aggregates by sum; any diversification credit requires a
dependence assumption and belongs to the model layer, where it can only *tighten* (Art. 5) — so it can never be granted.

### T-19 Log-growth domain (revised after review)

**STATEMENT.** Long-only, prices $\ge0$, $X_{t+1}=0$, $\mathrm{Fin}_{t+1}=0$, A-ACC-05: $W_{t+1}(a)\ge W^{\min}_{t+1}(a)$ surely, with $W^{\min}$ as in 05 §7 (all
terms $\mathcal F_t$-measurable). If $W^{\min}_{t+1}(a)>0$ then $\log(W_{t+1}/W_t)\ge\log(W^{\min}_{t+1}/W_t)>-\infty$ under every law supported on prices $\ge0$
(including every ambiguity set whose support is so restricted). If some admissible law charges $\{W_{t+1}\le0\}$, the (robust) log objective is
$-\infty$; a Wasserstein ball with unrestricted support contains such a law for any position with positive exposure.
**PROOF.** Tier-U bound (every position worthless, exit fees paid); monotonicity of $\log$; the ball contains
$(1-\epsilon)\hat{\mathbb P}+\epsilon\delta_{\xi_0}$ for small $\epsilon$ at finite transport cost. ∎
**COUNTEREXAMPLE (pre-review form).** A withdrawal: $W_t=100$ cash only, $X=-100$ ⇒ $W_{t+1}=0$ although the old $W^{\min}$ (no flow term) was $100$.
**NUMERICAL IMPLICATION.** Domain check before evaluation; `Decimal(0).ln()` is `-Infinity` without a signal (observed).

### T-20 Floor invariance under hold

**ASSUMPTIONS.** Long-only; every position has a stop; no fills except stop exits; A-STOP, A-TRIG; per-share cost terms and $\Lambda$
constant over the period; $\mathrm{Inc}\ge0$; $X=\mathrm{Fin}=\mathrm{Accr}=0$.
**STATEMENT.** (a) Static floor ($F_{t+1}=F_t$ — no HWM ratchet, no profit-lock ratchet, **no daily/weekly calendar reset** in between):
$R^{\mathrm{open}}_t\le K_t\Rightarrow R^{\mathrm{open}}_{t+1}\le K_{t+1}$. (b) Ratcheting floor ($F^{\mathrm{dd}}$ or $F^{\mathrm{lock}}$ at a new high, or a calendar reset
of $F^{\mathrm{day}}/F^{\mathrm{wk}}$ after a gain): the implication is **false**.
**PROOF (a).** Untriggered: $\Delta r_i=q_i\Delta m_i$ and $\Delta W=\sum q_i\Delta m_i+\mathrm{Inc}\ge\Delta R^{\mathrm{open}}$, $\Delta K=\Delta W$. Triggered $i$: $R^{\mathrm{open}}$
falls by $r_i$, $W$ falls by at most $r_i$ (A-STOP). ∎ **COUNTEREXAMPLES (b).** T-06 ratchet example ($r=49.5>K=14$ after a gain); calendar reset
(06 §7: $K=2.1<r=6$ the day after a gain day, found in review).
**IMPLICATION.** Ratcheting floors create an exit obligation the engine cannot discharge (Art. 17): RECOVERY output.

### T-21 Cushion necessity and sufficiency

**STATEMENT.** Let $\mathcal W_S$ be all period outcomes consistent with **all tier-S hypotheses of T-10** (incl. $X=\mathrm{Fin}=\mathrm{Accr}=0$, G11,
A-STOPLIVE, A-EXE-04, no other orders), with the bounds attainable (every
order may fill fully at $p^{\mathrm{lim}}$; every stop may fill exactly at $p^{\mathrm{stop}}-\kappa^{\mathrm{out}}$; no dependence restriction). Then
$W_{t+1}\ge F_t$ for all outcomes in $\mathcal W_S$ **iff** $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t$.
**PROOF.** (⇐) T-10. (⇒) The comonotone outcome in which every bound is attained yields $W_{t+1}=W_t-(R^{\mathrm{open}}+R^{\mathrm{res}}+L^{\mathrm{stop}}(n))$. ∎
**IMPLICATION.** $m_K\le1$ is necessary for robust floor safety; the cushion line is the unique maximal floor-safe throttle (06 §7).

### T-22 Binary64 floor safety condition

**ASSUMPTIONS.** $R=r/d_R$, $\ell=L/d_\ell$ with positive integers; IEEE-754 binary64, round-to-nearest, no overflow/underflow; unit roundoff
$u=2^{-53}$; computation $q_f=\mathrm{RN}(\mathrm{RN}(R)/\mathrm{RN}(\ell))$.
**STATEMENT.** If $r\,d_\ell<1/(4u)=2^{51}\approx2.25\times10^{15}$, then $\lfloor q_f\rfloor\le\lfloor R/\ell\rfloor$.
**PROOF.** $q_f=q^*(1+e_1)(1+e_3)/(1+e_2)$, $\lvert e_i\rvert\le u$, so $q_f-q^*\le4u\,q^*$ with $q^*=R/\ell=r d_\ell/(L d_R)\le r d_\ell$. If $q^*\in\mathbb Z$,
overshoot needs $4uq^*\ge1$, contradicting $q^*<2^{51}$. Otherwise $\lceil q^*\rceil-q^*\ge1/(Ld_R)$ and overshoot needs
$4u\,r d_\ell/(Ld_R)\ge1/(Ld_R)$, i.e. $r d_\ell\ge1/(4u)$. ∎
**COUNTEREXAMPLE (observed, outside the condition).** $R=172{,}808{,}193.53$ ($r d_\ell\approx1.7\times10^{18}$), $\ell=65.68583269$. A random search of
$2\times10^6$ realistic cent/basis-point inputs found none — consistent with the condition.
**IMPLICATION.** Float is safe for *one* division of *exact-decimal* inputs of bounded resolution; authority chains, derived
quantities and non-rational cost terms violate the hypothesis. Art. 7 stands.

### T-23 Sequential allocation order-dependence

**STATEMENT.** Greedy sequential sizing of several opportunities against one shared budget is order-dependent.
**PROOF (example).** $R=1000$, $\ell_A=3$, $\ell_B=7$. Order A,B: $Q_A=333$, $Q_B=0$. Order B,A: $Q_B=142$, $Q_A=2$. ∎
**IMPLICATION.** An authoritative ordering key belongs in the snapshot; batch semantics must be specified (RQ-27).

### T-24 Rounding Conservatism

**STATEMENT.** If $\hat g_k(n)\ge g_k(n)$ for all $n$ and $\hat b_k\le b_k$, then $\{n:\hat g_k(n)\le\hat b_k\}\subseteq\{n:g_k(n)\le b_k\}$ and $\hat Q_k\le Q_k$.
**PROOF.** $g_k(n)\le\hat g_k(n)\le\hat b_k\le b_k$. ∎ **COUNTEREXAMPLE (other directions).** Half-up (T-02).

### T-25 Floor-breach decomposition (premise added after review)

**STATEMENT.** Under the tier-S hypotheses of T-10 except A-STOP/A-TRIG, **and** $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t$:
$\{W_{t+1}<F_t\}\subseteq\bigcup_i\{\text{A-STOP}_i\text{ or A-TRIG}_i\text{ fails}\}$; hence $PB_t\le\sum_i\mathbb P(\text{fail}_i)$.
**PROOF.** Contrapositive of T-10; union bound. ∎ **COUNTEREXAMPLE (without the premise).** $W_t=F_t-1$, no positions, no trade: breach with no stop to fail.
**IMPLICATION.** Probability-of-ruin research reduces to stop-failure research (gaps, halts), 01 §5 — for states inside the cushion.

### T-26 VaR non-subadditivity (classical)

**STATEMENT.** $\mathrm{VaR}_\beta$ is not subadditive. **PROOF (counterexample).** Two independent positions each lose $100$ with probability
$0.04$, else $0$. $\mathrm{VaR}_{0.95}$ of each is $0$; the sum loses $\ge100$ with probability $1-0.96^2=0.0784>0.05$, so $\mathrm{VaR}_{0.95}(\text{sum})=100>0$. ∎
**IMPLICATION.** VaR is not used as an aggregatable budget.

### OPEN-1 Multi-step viability

Conjecture: under tier-S disturbances with an available trailing/de-risking control, the robust viability kernel of
$\{W\ge F\}$ equals $\{R^{\mathrm{open}}\le K\}$; under the maximal disturbance set with exits impossible, it equals
$\{\sum u^{\mathrm{open}}\le K\}$. **NOT YET PROVEN.**

### OPEN-2 Certificate validity

Requires $J$ (RQ-13), $\mathcal P_{t,\delta}$ (RQ-12), and an error model (RQ-14). **UNDEFINED.**
