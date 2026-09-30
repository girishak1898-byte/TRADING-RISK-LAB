# 08 — Theorem Register (v0.2-draft)

**Canonical format (v0.2, AUD-013).** Every entry has exactly the eight fields THEOREM ID, STATEMENT, ASSUMPTIONS, PROOF STATUS, PROOF,
COUNTEREXAMPLE ATTEMPT, NUMERICAL EDGE CASES, MACHINE-TESTABLE INVARIANT, and exactly one status:

- **PROVED** — the statement follows by the written proof from definitions, A-MATH-01 and hypotheses written into the statement
  itself (conditional statements whose hypotheses are checkable conditions on inputs).
- **PROOF REQUIRES ADDITIONAL ASSUMPTIONS** — the proof also uses at least one MARKET, EXECUTION, STATISTICAL, OPERATIONAL or
  RESEARCH assumption of [04](04-assumption-and-decision-registry.md) (listed); it is proved under them and can fail when they fail.
- **DISPROVED** — a counterexample, reproduced in exact arithmetic, refutes the statement.
- **UNDEFINED** — the statement cannot be evaluated because an object it names is undefined.
- **NOT YET PROVEN** — well defined; neither proof nor counterexample.

v0.1.1 entries with compound statuses are split: suffix **N** is the naive or negated variant that is DISPROVED; letters **a, b, c** are
parts with different status. Proofs are paper proofs about the *specification* (Art. 14); PROVED never means "implemented correctly".
"Observed" = reproduced numerically (Python 3.11, exact rationals as reference; review record `docs/review/phase0/03-numerical-red-team.md`).
Formula IDs refer to [14](14-formula-registry.md). Symbols local to one theorem are registered in 02 §M with that theorem as scope.
Worked examples use $\delta_q=1$ sh and USD prices unless stated.

## Summary

| ID | Name | Status | Formulas |
|---|---|---|---|
| T-01 | Hard risk dominance | PROVED | F047, F049, F074 |
| T-01N | Naive min / clamp compositions | DISPROVED | F049 |
| T-02 | Integer sizing safety | PROVED | F094, F095 |
| T-02N | Naive closed forms and rounding | DISPROVED | F095 |
| T-03 | Hard quantity dominance | PROVED | F096, F097, F126, F127 |
| T-03N | Min-of-caps with non-monotone constraints | DISPROVED | F096 |
| T-04 | No-trade under missing authority | PROVED | F045, F046 |
| T-05 | Wealth monotonicity of budgets and caps | PROVED | F073, F098 |
| T-06a | Maximum-drawdown gate | PROVED | F038, F040, F092 |
| T-06b | "MDD ≤ $d^{\max}$" from the gate alone | DISPROVED | F039 |
| T-06c | Per-epoch drawdown bound under trailing | PROOF REQUIRES ADDITIONAL ASSUMPTIONS | F139 |
| T-07 | Liquidity monotonicity | PROOF REQUIRES ADDITIONAL ASSUMPTIONS | F064, F111 |
| T-08 | Transaction-cost monotonicity | PROVED | F061–F063 |
| T-09 | Uncertainty monotonicity of feasibility-defined caps | PROVED | F125 |
| T-09N | Argmax sizing monotone in ambiguity | DISPROVED | F017 |
| T-10 | Capital-floor preservation (one period, tiered) | PROOF REQUIRES ADDITIONAL ASSUMPTIONS | F072, F120–F122 |
| T-10N | Floor preservation without the v0.2 hypotheses | DISPROVED | F120 |
| T-11 | Risk-reservation conservation | PROOF REQUIRES ADDITIONAL ASSUMPTIONS | F108, F119 |
| T-11N | Naive reservation schemes | DISPROVED | F108 |
| T-12 | No-trade under insufficient certified advantage | PROVED | F027 |
| T-12a | Infimum of a difference | PROVED | F117 |
| T-12N | Difference of infima as a certificate | DISPROVED | F117 |
| T-12b | Additive error allowance | PROVED | F118 |
| T-12c | Tighter bound for correlated estimation errors | NOT YET PROVEN | F118 |
| T-13 | Safe-action membership | PROVED | F024, F126 |
| T-14 | Replay determinism | PROVED | F006 |
| T-15 | Economic cost accounting identity | PROVED | F055–F058 |
| T-16 | Expected-value sizing is cap sizing | PROVED | F130 |
| T-17a | Naive stop-risk envelope admits unbounded notional | PROVED | F110, F128 |
| T-17b | Stop-risk budget with an exit-cost floor | PROVED | F111, F128 |
| T-18 | Comonotone aggregation | PROVED | F134 |
| T-19 | Log-growth domain | PROOF REQUIRES ADDITIONAL ASSUMPTIONS | F019, F070 |
| T-20a | Cushion invariance under hold, static floor | PROOF REQUIRES ADDITIONAL ASSUMPTIONS | F124 |
| T-20b | Cushion invariance under a ratcheting floor | DISPROVED | F040–F042 |
| T-21 | Cushion necessity and sufficiency | PROOF REQUIRES ADDITIONAL ASSUMPTIONS | F120 |
| T-22 | Binary64 floor safety condition | PROVED | F115, F116 |
| T-22N | Binary64 floor without the condition | DISPROVED | F116 |
| T-23 | Sequential allocation order-dependence | PROVED | F096 |
| T-24 | Rounding conservatism | PROVED | F129 |
| T-24N | Rounding in other directions | DISPROVED | F129 |
| T-25 | Floor-breach decomposition | PROOF REQUIRES ADDITIONAL ASSUMPTIONS | F123 |
| T-26 | VaR non-subadditivity | PROVED | F009 |
| OPEN-1 | Multi-step viability kernel | NOT YET PROVEN | F120, F122 |
| OPEN-2 | Certified-advantage validity | UNDEFINED | F027 |
| OPEN-3 | Required-input registry completeness | NOT YET PROVEN | F046 |
| OPEN-4 | Market-wide cost perturbations of $\Delta J$ | NOT YET PROVEN | F025 |

Counts: PROVED 22 · PROOF REQUIRES ADDITIONAL ASSUMPTIONS 8 · DISPROVED 11 · NOT YET PROVEN 4 · UNDEFINED 1 · total 46.

**Revision R1 (v0.1 → v0.1.1).** An independent adversarial review found 4 blockers, 9 major and 11 minor defects (registered as
REV-001 … REV-024 in `docs/review/phase0/`). Blockers: T-10 failed for add-ons (→ G11); T-07 was false because open risk credited $\Lambda$ (→ OC-1);
tier U under-charged pending orders' fees (→ $Z^{\mathrm{res}}$ at full $L^{\mathrm{abs}}$); T-25 lacked its cushion premise.

**Revision R2 (v0.1.1 → v0.2, Phase-0 independent mathematical review).** T-10 was still false for a stop partially executed at the cut
(per-order minimum fee counted twice; AUD-001) → A-TRIG restated as the position-level exit-value bound F072, proof reduced to one case,
split envelope F140 for non-super-additive fees; T-20a needs "every stop triggered in the period fully executed by the cut" (A-EXE-06, AUD-014, REV-026); A-EXE-04 on
cumulative filled quantity (AUD-015); the "only if" of T-21 was false under OC-1 whenever $\Lambda_t>0$ (AUD-032, found during correction) →
restated with $E_t-F_t$; canonical eight-field format, split IDs, assumption IDs per entry (AUD-013, AUD-016, AUD-017). A second
independent review of the correction draft (REV-025 … REV-036) led to: reservations charged at the $\tau_t$ inputs (F144; a stale reservation
breached the floor by 40, REV-028); F140 over $N^{\mathrm{ex}}+1$ fee-bearing parts (REV-029); A-EXE-06 widened to triggered-but-unexecuted stops
(REV-026); $q^{\mathrm{exp}}$ for a partially filled order (REV-027); T-21's necessity restricted (REV-025); F070 with the envelope (REV-034).

**Revision R3 (Phase-0 closure).** Realised costs are no longer charged twice: a partially filled order is charged the exact exposure charge
F145 (fees already paid excluded), reservations are re-evaluated from the order state (F144), pending cash is deducted once (F048) and the
strategy budget uses its window-start base (F078) — OC-2, OC-3, OC-4 eliminated (AUD-034, AUD-035). T-21 is restated as separate sufficiency,
necessity and equivalence, each proved; the hard layer always uses F140. Only OC-1 remains, proved necessary for T-07. A third independent
review of `f37c1b6` (16 findings; 15 confirmed, 1 rejected) led to: per-share distances of pending orders clamped at $0$ (a trailed stop breached
the floor by $29$; AUD-039); ADV capped by policy, a merge-only statistical cluster map and the cap invariant restated (AUD-040); a missing
estimate ⇒ $\alpha_t=0$ (AUD-041); stopless exposures in tier S via A-ACC-05 (AUD-042); T-19 with T-10's common hypotheses (AUD-043); undefined
fail-closed charges replaced by $\alpha_t=0$ (AUD-044); floor references rounded up (AUD-045); one $-0$ rule and a strict canonical document
(AUD-036, AUD-046); hard budgets clamped at $0$ (AUD-047); A-TRIG's model component named (AUD-048); cross-references, F121 and T-06c's epoch
high-water mark (AUD-049); terminal = venue-confirmed (AUD-050). T-21 (b) and (c) now require inactive clamps. The closure's manual review
restored the ANOMALY rule for the held part of a partially filled order, which F145 had dropped (AUD-051).

---

### T-01 Hard Risk Dominance

**THEOREM ID.** T-01

**STATEMENT.** For every input — including $R^{\mathrm{mod}}$ = NaN, $\pm\infty$, negative, missing, wrong type — $0\le R^{\mathrm{allow}}_t\le R^{\mathrm{hard}}_t$ with
$R^{\mathrm{allow}}_t=\min(R^{\mathrm{hard}}_t,\mathfrak s(R^{\mathrm{mod}}_t))$ (F049) and $R^{\mathrm{hard}}_t$ from F074; and $R^{\mathrm{allow}}_t=0$ whenever a REQUIRED model output is
invalid. The same holds for every $b^{\mathrm{allow}}_k=\min((b^{\mathrm{hard}}_k)^+,\mathfrak s(b^{\mathrm{mod}}_k))$, with $(b^{\mathrm{hard}}_k)^+$ in place of $R^{\mathrm{hard}}_t$ (F049; a hard budget
can be negative, e.g. H14, AUD-047).

**ASSUMPTIONS.** A-MATH-01; $\mathfrak s$ as in F047; $\min$ is exact comparison of validated values; every hard input is validated as finite
(01 §9).

**PROOF STATUS.** PROVED

**PROOF.** $R^{\mathrm{hard}}\ge0$ by $(\cdot)^+$ and finite since each $b_k$ is finite. $\mathfrak s$ maps into $[0,\infty]$, and to $0$ for invalid
REQUIRED outputs. The minimum of an element of $[0,\infty)$ and an element of $[0,\infty]$ lies in $[0,R^{\mathrm{hard}}]$. ∎

**COUNTEREXAMPLE ATTEMPT.** All invalid classes (NaN, sNaN, $\pm\infty$, None, non-numeric, negative, $>\bar M$) under the specified
composition: none. The naive compositions fail: T-01N.

**NUMERICAL EDGE CASES.** $R^{\mathrm{mod}}=-0$ (at the boundary not in the canonical grammar, hence invalid; an internal $-0$ is mapped to $0$ by F047;
01 §9 items 13, 17; AUD-046); $b^{\mathrm{hard}}_k<0$ (clamped to $0$); $R^{\mathrm{mod}}=R^{\mathrm{hard}}$ exactly; exhausted $R^{\mathrm{hard}}=0$;
$R^{\mathrm{mod}}>\bar M$ (invalid).

**MACHINE-TESTABLE INVARIANT.** ∀ generated snapshots `0 ≤ R_allow ≤ R_hard`. Oracle: invalid `R_mod` ⇒ `R_allow == 0` if REQUIRED,
`== R_hard` if OPTIONAL; finite negative ⇒ `0`; finite in $[0,\bar M]$ ⇒ `min(R_hard, R_mod)`. Metamorphic (AUD-002, restated at closure,
AUD-040): $Q^{\mathrm{hard}}$ computed with any estimator outputs is $\le Q^{\mathrm{hard}}$ computed with every estimated input at its policy bound
($\kappa^{\min}p^{\mathrm{stop}}$, $\Gamma^{\min}$, $\Lambda^{\mathrm{floor}}$, $\mathrm{ADV}^{\max}$, the human-set cluster map); a missing estimate gives $\alpha_t=0$. (The former wording
"an arbitrarily optimistic estimate never increases $Q^{\mathrm{hard}}$" is false: $666$ vs $953$ sh, 06 §5.) Property-based and fuzz.

---

### T-01N Naive min / clamp compositions

**THEOREM ID.** T-01N

**STATEMENT.** "Composing $R^{\mathrm{allow}}$ with (i) Python float `min`, (ii) `Decimal.min`/`Decimal.max`, or (iii) without the clamp $(\cdot)^+$ satisfies T-01."

**ASSUMPTIONS.** The documented semantics of the operations (IEEE-754 minNum/maxNum; Python built-ins).

**PROOF STATUS.** DISPROVED

**PROOF.** (i) `min(R_hard, nan)` → `R_hard`, `min(nan, R_hard)` → `nan` (observed): argument-order dependent; NaN then reaches
$\lfloor\cdot\rfloor$. (ii) `R_hard.min(Decimal('NaN'))` → `R_hard` (observed): a REQUIRED model's failure silently becomes "no model limit"
(Art. 4). (iii) Exhausted budgets give $R^{\mathrm{hard}}<0$ and a negative lattice count, readable as a sell (review B05: `floor(-0.01/1) = -1`). ∎

**COUNTEREXAMPLE ATTEMPT.** The counterexamples are the proof.

**NUMERICAL EDGE CASES.** `max(0.0, -0.0)` = `0.0` but `min(-0.0, 0.0)` = `-0.0` (review Z01–Z02).

**MACHINE-TESTABLE INVARIANT.** Lint: no float `min`/`max` and no `Decimal.min`/`max` on the authority path; each counterexample is a
regression test that must fail against the naive form.

---

### T-02 Integer Sizing Safety

**THEOREM ID.** T-02

**STATEMENT.** Let $g:\mathbb L_{\ge0}\to\mathbb Q$ be non-decreasing with $g(0)=0$, $b\in\mathbb Q$ and
$Q:=\max(\{0\}\cup\{n\in\mathbb L_{>0}:n\le\bar N,\ g(n)\le b\})$ [F094]. Then (a) $Q\in\mathbb L_{\ge0}$; (b) $Q>0\Rightarrow g(Q)\le b$; (c) downward
closure: $0<n\le Q$, $n\in\mathbb L\Rightarrow g(n)\le b$; (d) maximality: $Q+\delta_q\le\bar N\Rightarrow g(Q+\delta_q)>b$; (e) linear case $g(n)=n\ell$,
$\ell>0$, $b\ge0$: $Q=\min(\bar N,\delta_q\lfloor b/(\delta_q\ell)\rfloor)$ (F095).

**ASSUMPTIONS.** A-MATH-01; the hypotheses on $g$ and $b$ in the statement.

**PROOF STATUS.** PROVED

**PROOF.** (a), (b), (d): the candidate set is finite ($\mathbb L\cap[0,\bar N]$) and contains $0$; $Q$ is its maximum. (c) $g(n)\le g(Q)\le b$ by
monotonicity. (e) $\delta_qk\ell\le b\iff k\le b/(\delta_q\ell)\iff k\le\lfloor b/(\delta_q\ell)\rfloor$ for integer $k$; the argument of $\lfloor\cdot\rfloor$ is
dimensionless (03 E-05). ∎ *Application:* for fee-bearing constraints the monotonicity hypothesis is supplied by A-EXE-01 and
A-EXE-02, so every use of T-02 on H1–H16 inherits them.

**COUNTEREXAMPLE ATTEMPT.** Differential enumeration for small $\bar N$ with random monotone $g$: none. Leaving the hypotheses: T-02N.

**NUMERICAL EDGE CASES.** $b<0$ ⇒ $Q=0$; $b=g(n)$ exactly (admitted; FM-NUM-3); $\ell\le0$ excluded by G7 (else $Q=\bar N$); fractional
$\delta_q$; $b$ huge ($Q=\bar N$).

**MACHINE-TESTABLE INVARIANT.** `g(Q) ≤ b` and (`Q + δ_q > N̄` or `g(Q + δ_q) > b`) — the maximality witness is recorded as evidence;
`Q ∈ 𝕃, Q ≥ 0`; differential test against brute-force enumeration.

---

### T-02N Naive closed forms and rounding

**THEOREM ID.** T-02N

**STATEMENT.** "Each of (i) the closed form with a per-share fee added to $\ell$ under a minimum commission, (ii) round-half-up or
round-half-even quantisation, (iii) binary64 evaluation, (iv) the closed form with $\ell\le0$, yields $g(Q)\le b$."

**ASSUMPTIONS.** As T-02 except the relaxed element named in each item.

**PROOF STATUS.** DISPROVED

**PROOF.** (i) $g(n)=0.10n+2\max(1.00,0.005n)$, $b=2.50$: naive $\lfloor2.50/0.11\rfloor=22$, $g(22)=4.20>2.50$; true $Q=5$, $g(5)=2.50$ (review B06).
(ii) $b=1000.00$, $\ell=2.90$: half-up and half-even both give $345$, $g=1000.50>b$; floor $344$, $g=997.60$ (B03, B04). (iii) $b=172{,}808{,}193.53$,
$\ell=65.68583269$: binary64 gives $2{,}630{,}829$, exact $2{,}630{,}828$ (T-22N). (iv) $\ell\le0$ ⇒ every $n$ feasible ⇒ $Q=\bar N$. ∎

**COUNTEREXAMPLE ATTEMPT.** The counterexamples are the proof.

**NUMERICAL EDGE CASES.** As in the proof.

**MACHINE-TESTABLE INVARIANT.** Each case is a regression test in which the exact search and the naive form must disagree.

---

### T-03 Hard Quantity Dominance

**THEOREM ID.** T-03

**STATEMENT.** With finite $\mathcal K$, every $g_k$ as in T-02, 0/1 gates, $Q_k$ by F094 and $Q^{\mathrm{hard}}$ by F096: (a) if all gates pass,
$\{0\}\cup\{n\in\mathbb L_{>0}:n\le\bar N,\ \forall k\ g_k(n)\le b_k\}=\mathbb L\cap[0,Q^{\mathrm{hard}}]$; (b) $\lfloor\min_ky_k\rfloor_{\mathbb L}=\min_k\lfloor y_k\rfloor_{\mathbb L}$ (F097);
(c) for every proposal $\tilde n$ (non-numeric, NaN, $\infty$, negative, non-lattice, huge) the verifier F126 returns $0\le V(\tilde n)\le Q^{\mathrm{hard}}$ and
$V(\tilde n)$ satisfies every hard constraint.

**ASSUMPTIONS.** A-MATH-01; the monotonicity hypotheses of T-02 for every $g_k$.

**PROOF STATUS.** PROVED

**PROOF.** (a) By T-02(c) each feasible set is $\mathbb L\cap[0,Q_k]$; the intersection of initial segments is the initial segment up to the
minimum. (b) $\lfloor\cdot\rfloor_{\mathbb L}$ is non-decreasing, so $\lfloor\min y\rfloor\le\lfloor y_k\rfloor$ for all $k$; and $\min_k\lfloor y_k\rfloor$ is a lattice point
$\le\min_ky_k$, hence $\le\lfloor\min y\rfloor$. (c) By construction and (a). For a non-monotone consumption the monotone upper envelope
$\bar g(n)=\max_{n'\le n}g_k(n')$ (F127) is non-decreasing and $\ge g_k$, so using $\bar g$ restores the hypothesis conservatively (T-24). ∎

**COUNTEREXAMPLE ATTEMPT.** Exhaustive search on small lattices with random monotone $g_k$: none. Non-monotone constraints: T-03N.

**NUMERICAL EDGE CASES.** A gate fails ⇒ $0$; one $Q_k=0$; $\tilde n\in\{\text{NaN},\infty,-1,10^{400},2.5\}$ with $\delta_q=1$ sh ⇒ $0,0,0,0,2$ (clipped
to $Q^{\mathrm{hard}}$); float-typed $\tilde n$ rejected at parse (01 §9 items 1, 12, 17); $\tilde n=-0$ is not in the canonical grammar, hence invalid ⇒ $0$.

**MACHINE-TESTABLE INVARIANT.** $\forall k:\ g_k(Q^{\mathrm{fin}})\le b_k$ and $Q^{\mathrm{fin}}\le Q_k$; $V$ fuzzed; an independent slow checker re-evaluates
every constraint (differential).

---

### T-03N Min-of-caps with non-monotone constraints

**THEOREM ID.** T-03N

**STATEMENT.** "T-03(a) holds without monotonicity of the $g_k$."

**ASSUMPTIONS.** As T-03 without monotonicity.

**PROOF STATUS.** DISPROVED

**PROOF.** (i) Minimum order notional $n\,p\ge1000$ USD at $p=50$: the feasible set is $\{0\}\cup\{20,\dots,Q\}$ — not an initial segment.
(ii) Tiered per-order fee $0.005$ USD/sh below $1000$ sh and $0.003$ USD/sh from $1000$ sh, $\ell=0.5$, budget $504$: consumptions at
$998,999,1000,1001,1002$ are $503.99,\ 504.495,\ 503.00,\ 503.503,\ 504.006$; $999$ is infeasible between feasible points, and an order sized
$1001$ that partially fills $999$ consumes $504.495>504$. ∎

**COUNTEREXAMPLE ATTEMPT.** The counterexamples are the proof.

**NUMERICAL EDGE CASES.** Partial fills landing on an infeasible point.

**MACHINE-TESTABLE INVARIANT.** Fee-schedule monotonicity check at load (A-EXE-01); regression tests (i), (ii); minimum size only as the
post-filter F093.

---

### T-04 No-Trade Under Missing Authority

**THEOREM ID.** T-04

**STATEMENT.** $\alpha_t=0\Rightarrow\mathcal D(\mathsf S_t,\cdot)=$ NO\_TRADE with $\mathsf{rc}\supseteq\{\text{failed validators}\}\ne\varnothing$ (F046).

**ASSUMPTIONS.** A-MATH-01; $\mathcal R^{\mathrm{req}}$ finite; each validator decides presence, type, domain, freshness ($\mathrm{age}\le\mathrm{TTL}$, F045),
account scope and internal consistency; $\alpha_t$ is the conjunction of validators; $\mathcal D$ evaluates G1 first (06 §10).

**PROOF STATUS.** PROVED

**PROOF.** By construction of $\mathcal D$. ∎

**COUNTEREXAMPLE ATTEMPT.** A deserialiser that defaults a missing $R^{\mathrm{res}}$ to $0$ passes presence checks; two strategies then
double-spend. This violates Art. 4 at schema level rather than the theorem: the theorem is only as strong as $\mathcal R^{\mathrm{req}}$ is complete
(OPEN-3).

**NUMERICAL EDGE CASES.** $\mathrm{age}=\mathrm{TTL}$ exactly (admitted); clock regression (A-TIME-01 ⇒ $\alpha_t=0$).

**MACHINE-TESTABLE INVARIANT.** For every valid snapshot and every single-field mutation {delete, null, stale, wrong scope, wrong type,
out-of-domain}: NO\_TRADE and the reason names that field; instrumented read-set $\subseteq\mathcal R^{\mathrm{req}}$.

---

### T-05 Wealth Monotonicity of Budgets and Caps

**THEOREM ID.** T-05

**STATEMENT.** For two snapshots identical except for a consistent cash reduction $\Delta\ge0$ ($C'=C-\Delta$, $\mathrm{BP}'=\mathrm{BP}-\Delta$,
$C^{\mathrm{avail}\prime}=C^{\mathrm{avail}}-\Delta$, so $W'=W-\Delta$): $K$, $B$, every $b_k$ and $Q^{\mathrm{hard}}$ are not larger in the reduced snapshot, hence
non-increasing in $\mathrm{DD}$ below the prior high-water mark. $\vartheta_K$ (F098) is continuous and non-increasing on $[0,d^{\max}]$ and $0$ beyond.

**ASSUMPTIONS.** A-MATH-01; $H_t=\max(H_{t-1},\nu_t)$ with the current epoch HWM-eligible (RQ-03); $B$ one of F073; $\theta$ in the box F109;
$\nu^{\mathrm{ref}}$ independent of $W$.

**PROOF STATUS.** PROVED

**PROOF.** $F^{\mathrm{abs}}$ does not depend on $W$; $F^{\mathrm{day}},F^{\mathrm{wk}}$ do not, except at the first epoch of a day/week, where they have slope
$1-\ell^{\mathrm{day}}$ / $1-\ell^{\mathrm{wk}}\in(0,1)$. $F^{\mathrm{dd}}=(1-d^{\max})U\max(H_{t-1},\nu)$ has slope $0$ below the prior HWM and $1-d^{\max}$ above;
$F^{\mathrm{lock}}$ has slope $0$ or $\eta^{\mathrm{lock}}$. Hence $K=W-F$ has slope in $\{1,d^{\max},1-\eta^{\mathrm{lock}},\ell^{\mathrm{day}},\ell^{\mathrm{wk}}\}\subset[0,1]$: non-decreasing.
B1–B4 are non-decreasing. Each $b_k$ is a non-decreasing function of $(B,K,\mathrm{BP}^{\mathrm{avail}})$ minus terms independent of $W$; $\min$, $(\cdot)^+$
and $Q_k$ (as a function of $b_k$) preserve order; G3 and G4 are monotone. Derivative of $\vartheta_K$: F099. ∎

**COUNTEREXAMPLE ATTEMPT.** "Recovery boost" rules violate the statement (excluded by design); limits on realised P&L only (DC-4);
multiplicative per-loss rules are not functions of $(W,H)$. Inconsistent perturbations ($C$ changed, $\mathrm{BP}$ not) are outside the hypothesis.
None found within.

**NUMERICAL EDGE CASES.** $\mathrm{DD}=d^{\max}$ exactly ($\vartheta_K=0$, G4 fails); $\mathrm{DD}>1$ (formula positive again; defined $0$);
$\mu^{K}=f^{\mathrm{trd}}$ (F100 denominator $0$: division guard, 01 §9 item 16); directed rounding is monotone.

**MACHINE-TESTABLE INVARIANT.** Metamorphic: consistent cash reduction ⇒ no $b_k$ and not $Q^{\mathrm{hard}}$ increases.

---

### T-06a Maximum-Drawdown Gate

**THEOREM ID.** T-06a

**STATEMENT.** $\mathrm{DD}_t\ge d^{\max}\Rightarrow Q^{\mathrm{hard}}=0$.

**ASSUMPTIONS.** A-MATH-01; G4 in the gate set (F092); $F^{\mathrm{dd}}$ included in $F$ (F043).

**PROOF STATUS.** PROVED

**PROOF.** G4 fails. Independently (defence in depth) $K\le W-F^{\mathrm{dd}}=U_tH_t(d^{\max}-\mathrm{DD}_t)\le0$ by F038, F040, F044, so H4's budget is $\le0$. ∎

**COUNTEREXAMPLE ATTEMPT.** None.

**NUMERICAL EDGE CASES.** $\mathrm{DD}_t=d^{\max}$ exactly (strict gate fails ⇒ $0$); $\mathrm{DD}$ for the gate rounded up, never down.

**MACHINE-TESTABLE INVARIANT.** Property test: $\mathrm{DD}_t\ge d^{\max}$ ⇒ `Q_hard == 0`.

---

### T-06b "MDD ≤ d^max" from the gate alone

**THEOREM ID.** T-06b

**STATEMENT.** "$\mathrm{MDD}_t\le d^{\max}$ on every path when G4 is enforced."

**ASSUMPTIONS.** G4 only.

**PROOF STATUS.** DISPROVED

**PROOF.** *Gap:* $d^{\max}=10\%$, $W=H=100{,}000$, $1{,}000$ sh at $100$ with stop $90$; overnight open at $70$ ⇒ $W=70{,}000$, $\mathrm{DD}=30\%$.
*Ratchet without gap:* $d^{\max}=10\%$, $W=H=100$, cash $50$, one share at $50$ with stop $40.5$ ($r^{\mathrm{open}}=9.5\le K=10$); price rises to $90$:
$W=H=140$, $K=14<r^{\mathrm{open}}=49.5$; price falls to $40.5$, stop fills exactly: $W=90.5$, $\mathrm{DD}=1-90.5/140=35.4\%$ — no new trade, stop held
exactly. *Halt:* exit impossible during a halt; same effect as a gap. ∎

**COUNTEREXAMPLE ATTEMPT.** The counterexamples are the proof.

**NUMERICAL EDGE CASES.** None specific.

**MACHINE-TESTABLE INVARIANT.** Regression scenarios above report $\mathrm{MDD}>d^{\max}$ (the specification must not claim otherwise).

---

### T-06c Per-Epoch Drawdown Bound Under Trailing

**THEOREM ID.** T-06c

**STATEMENT.** If at every epoch $t$, after adjustments made **before** the cut $\mathsf S_t$ by an external risk-reducing authority (stop
modifications or sales), $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t\le K_t$ holds, and every period satisfies the tier-S hypotheses of T-10, then
$\mathrm{DD}_t\le d^{\max}$ at every epoch.

**ASSUMPTIONS.** All tier-S assumptions of T-10 (A-TRIG, A-FLOW-01, A-ACC-07, …) in every period; the pre-cut adjustment rule; $F^{\mathrm{dd}}\in F$;
the high-water mark is updated at epochs only, $H_{t+1}=\max(H_t,\nu_{t+1})$ ($\mathcal H_t$ = epoch marks in F037; AUD-049).

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF.** T-10 with $n=0$ gives $W_{t+1}\ge F_t\ge F^{\mathrm{dd}}_t=(1-d^{\max})H_tU_t$; $U$ is constant ($X=0$), so $\nu_{t+1}\ge(1-d^{\max})H_t$ (F139). If
$\nu_{t+1}\le H_t$ then $H_{t+1}=H_t$ and $\mathrm{DD}_{t+1}\le d^{\max}$; otherwise $\mathrm{DD}_{t+1}=0$. ∎

**COUNTEREXAMPLE ATTEMPT.** Trailing by stop modification alone can be infeasible (if $K_t/q_{i,t}<\kappa^{\mathrm{out}}$ the required stop lies above
the mark), so the authority must be able to sell; intra-period drawdown is not covered; the v0.1 form without the pre-cut rule was vacuous.
If $\mathcal H_t$ also contained intra-period highs the bound fails: $H_t=100$, intra-period peak $120$, $\nu_{t+1}=95\ge(1-0.1)H_t$ gives $\mathrm{DD}_{t+1}=20.8\%>10\%$
(third review, AUD-049). With the pre-closure unclamped charge a trailed stop gave $\mathrm{DD}_{t+1}=410/38{,}100>1\%=d^{\max}$ (AUD-039).

**NUMERICAL EDGE CASES.** $W_{t+1}=F_t$ gives $\mathrm{DD}_{t+1}=d^{\max}$ exactly — then T-06a blocks new risk.

**MACHINE-TESTABLE INVARIANT.** Monte Carlo on paths inside the tier-S set with the pre-cut rule ⇒ $\mathrm{DD}\le d^{\max}$ at epochs; paths outside
are logged as assumption violations.

---

### T-07 Liquidity Monotonicity

**THEOREM ID.** T-07

**STATEMENT.** Holding everything else fixed, $Q^{\mathrm{hard}}$ is non-decreasing in the ADV of any instrument and non-increasing in its spread.

**ASSUMPTIONS.** A-MATH-01; A-EXE-02 ($\hat\kappa^{\mathrm{out}}$, $\kappa^{\mathrm{liq}}$, $\hat\Lambda$ non-increasing in ADV, non-decreasing in spread); A-ACC-06 with the
floors F111 (monotone in spread); OC-1 (open risk without $\Lambda$ credit, F064); H12–H13 budgets increasing in ADV; G5.

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF.** Higher ADV or lower spread lowers $\Lambda$ (raising $W$, hence $B$ and $K$), lowers $\kappa^{\mathrm{out}}$ (lowering every consumption and every
open-risk term), and raises the H12–H13 budgets; the maximum of a constant policy floor and a monotone estimate (F111) is monotone. Every
$b_k$ is non-decreasing and every $g_k$ non-increasing in liquidity; feasible sets are nested; $\min$ preserves order; G5 is monotone. ∎

**COUNTEREXAMPLE ATTEMPT.** The v0.1 form with $\Lambda$ credit in open risk (review, re-verified exactly): hold $1{,}000$ sh at $50$, stop $45$,
$\kappa^{\mathrm{out}}=0.05$, cash $200{,}000$, $B=W$, $f^{\mathrm{trd}}=f^{\mathrm{port}}=2\%$, new order consumption $5.05n$. Low ADV ($\Lambda=500$): $W=249{,}500$,
credited open risk $4{,}550$, H2 budget $440$, $Q=87$. High ADV ($\Lambda=100$): $W=249{,}900$, credited open risk $4{,}950$, budget $48$, $Q=9$. Worse
liquidity, larger cap. Under OC-1 both budgets are $\le0$ and $Q=0$ (monotone). Other failures: fitted impact models non-monotone in ADV;
displayed depth used as a cap (inadmissible).

**NUMERICAL EDGE CASES.** $\mathrm{ADV}\to0$ (A-MKT-06 ⇒ $\alpha_t=0$); $\sqrt{\ }$ in impact models only with certified upper bounds (01 §9 item 4).

**MACHINE-TESTABLE INVARIANT.** Metamorphic: ADV ↑ ⇒ $Q^{\mathrm{hard}}$ not ↓; spread ↑ ⇒ $Q^{\mathrm{hard}}$ not ↑ — for the opportunity's instrument and for held
instruments; cost-model monotonicity checked on a grid at model load.

---

### T-08 Transaction-Cost Monotonicity

**THEOREM ID.** T-08

**STATEMENT.** (a) If $\phi'\ge\phi$ and $\kappa^{\mathrm{out}\prime}\ge\kappa^{\mathrm{out}}$ pointwise, then $Q^{\mathrm{hard}\prime}\le Q^{\mathrm{hard}}$. (b) If moreover
$J(a)=\mathbb E[\mathcal U(W_{t+1}(a))]$ with $\mathcal U$ non-decreasing and the perturbation affects only the fills generated by $a$, then $\Delta J'(a)\le\Delta J(a)$.

**ASSUMPTIONS.** A-MATH-01; the hypotheses in the statement.

**PROOF STATUS.** PROVED

**PROOF.** (a) $L^{\mathrm{stop}},L^{\mathrm{gap}},L^{\mathrm{abs}}$ (F061–F063) and the H14 consumption increase pointwise; feasible sets shrink. (b) $W_{t+1}(a^{\varnothing})$ is
unchanged and $W_{t+1}(a)$ decreases pointwise (costs enter F055 negatively); $\mathcal U$ is non-decreasing. ∎

**COUNTEREXAMPLE ATTEMPT.** None within the hypotheses. Market-wide perturbations (which also change $J(a^{\varnothing})$) are OPEN-4.

**NUMERICAL EDGE CASES.** Fee quantisation upward (01 §9 item 15) preserves (a).

**MACHINE-TESTABLE INVARIANT.** Metamorphic on the fee schedule and on a scaling of $\kappa^{\mathrm{out}}$.

---

### T-09 Uncertainty Monotonicity of Feasibility-Defined Caps

**THEOREM ID.** T-09

**STATEMENT.** For model budgets defined by robust feasibility, $b^{\mathrm{mod}}_k(\mathcal P)$ as in F125, and nested sets $\mathcal P\subseteq\mathcal P'$:
$b^{\mathrm{mod}}_k(\mathcal P')\le b^{\mathrm{mod}}_k(\mathcal P)$, hence $Q^{\mathrm{fin}}(\mathcal P')\le Q^{\mathrm{fin}}(\mathcal P)$; also $\inf_{\mathcal P'}J\le\inf_{\mathcal P}J$.

**ASSUMPTIONS.** A-MATH-01; F125.

**PROOF STATUS.** PROVED

**PROOF.** A constraint required for every $\mathbb Q\in\mathcal P'$ is required for every $\mathbb Q\in\mathcal P$; the feasible set of budgets shrinks,
so its supremum does not increase; F049 and T-03 transmit the order. The infimum over a larger set is not larger. ∎

**COUNTEREXAMPLE ATTEMPT.** None for feasibility-defined caps. Argmax-defined sizing: T-09N.

**NUMERICAL EDGE CASES.** Empty ambiguity set (supremum $+\infty$): must be an invalid model output ⇒ $\mathfrak s$ (F047); unbounded supremum ⇒ no
model constraint (OPTIONAL) or $0$ (REQUIRED).

**MACHINE-TESTABLE INVARIANT.** Nested radii $\varepsilon^{W\prime}>\varepsilon^{W}$ ⇒ $b^{\mathrm{mod}}_k(\varepsilon^{W\prime})\le b^{\mathrm{mod}}_k(\varepsilon^{W})$.

---

### T-09N Argmax Sizing Monotone in Ambiguity

**THEOREM ID.** T-09N

**STATEMENT.** "The maximiser of the robust objective is non-increasing in the ambiguity set."

**ASSUMPTIONS.** Robust objective $\min_{\mathbb Q\in\mathcal P}J_{\mathbb Q}$, sizing by its argmax (F017).

**PROOF STATUS.** DISPROVED

**PROOF.** Sizes $n\in\{0,1,2\}$ sh. $\mathbb Q_1$: $J=(0,5,4)$, argmax $1$. Adding $\mathbb Q_2$ with $J=(0,1,3)$: robust $\min_{\mathbb Q}J=(0,1,3)$, argmax $2$. A
larger ambiguity set increased the chosen size. ∎

**COUNTEREXAMPLE ATTEMPT.** The counterexample is the proof.

**NUMERICAL EDGE CASES.** Ties in the argmax (tie-break rule required for determinism, T-14).

**MACHINE-TESTABLE INVARIANT.** Regression: safety-relevant model outputs are feasibility caps; argmax outputs are proposals verified by F126.

---

### T-10 Capital-Floor Preservation (one period, tiered)

**THEOREM ID.** T-10

**STATEMENT.** Tier S: $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t\ \Rightarrow\ W_{t+1}\ge F_t$ (F120). Tier G: $G^{\mathrm{open}}_t+G^{\mathrm{res}}_t+L^{\mathrm{gap}}(n)\le K_t\Rightarrow W_{t+1}\ge F_t$
(F121). Tier U: $Z^{\mathrm{open}}_t+Z^{\mathrm{res}}_t+L^{\mathrm{abs}}(n)\le K_t\Rightarrow W_{t+1}\ge F_t$ (F122).

**ASSUMPTIONS.** Tier S: A-MATH-01; A-SCOPE-03; A-SCOPE-05 with G11; A-FLOW-01 ($X_{t+1}=0$); A-ACC-01, A-ACC-02, A-ACC-03 (transition F055);
A-ACC-07 ($\mathrm{Fin}=\mathrm{Accr}=0$, $\mathrm{Inc}\ge0$); A-ACC-04; A-ACC-06 ($\Lambda\ge0$); A-MKT-05 (every entry fill $\le p^{\mathrm{lim}}$); A-EXE-01, A-EXE-02;
A-EXE-03 (cumulative fill $\le$ order quantity); A-EXE-04 (fees on cumulative filled quantity); A-EXE-05 (no other orders); A-AUTH-02 (complete
ledger, including each pending order's filled quantity and fees paid); A-AUTH-04 (one cut); **A-TRIG** (position-level exit-value bound F072 at the
$\tau_t$ inputs); open risk by F064, reservations by F144 and partially filled orders by F145 (all at the $\tau_t$ inputs, REV-028, AUD-034);
hard-layer inputs by F111; the split envelope F140 in place of $\phi^{\mathrm{sell}}$ throughout (equal to it for super-additive schedules); per-share
distances of pending orders clamped at $0$ in F144, F145 (AUD-039); an exposure without an authoritative stop charged $u^{\mathrm{open}}$ (D-06) and covered by
A-MKT-01 and A-ACC-05 (tier-U form of F072) instead of A-TRIG (case (1′), AUD-042).
Tier G: A-GAP (tier-G form of F072) instead of A-TRIG. Tier U: A-MKT-01 and A-ACC-05 (tier-U form of F072) instead of A-TRIG.

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF (tier S; one case since v0.2).** By A-ACC-04 and G11, $W_{t+1}-W_t=\sum_i\Delta_i+\mathrm{Inc}_{t+1}$, where $\Delta_i$ is the change of cash plus
liquidation value attributable to exposure $i$ (F055 with $X=\mathrm{Fin}=\mathrm{Accr}=0$).
(1) *Held exposure* ($q^{\mathrm{exp}}_i=q_{i,t}$): it contributed $q_{i,t}m_{i,t}-\Lambda_{i,t}$ before the period and contributes $\mathrm{XV}_{i,t+1}$ after it
(exit proceeds net of all exit fees plus liquidation value of any remainder). By A-TRIG,
$\Delta_i\ge q_{i,t}\big(p^{\mathrm{stop}}_i-\kappa^{\mathrm{out}}_i(q_{i,t})\big)-\phi^{\mathrm{sell}}_i(q_{i,t})-q_{i,t}m_{i,t}+\Lambda_{i,t}=-r^{\mathrm{open}}_i+\Lambda_{i,t}\ge-r^{\mathrm{open}}_i$ (F064, A-ACC-06).
(1′) *Held exposure without an authoritative stop* (D-06; AUD-042): charged $u^{\mathrm{open}}_i=q_{i,t}m_{i,t}+\phi^{\mathrm{split}}_{i,0}(q_{i,t})$ (F066 with F140) in $R^{\mathrm{open}}_t$.
A-TRIG is undefined without a stop; by A-MKT-01 and A-ACC-05, $\mathrm{XV}_{i,t+1}\ge-\phi^{\mathrm{split}}_{i,0}(q_{i,t})$, so $\Delta_i\ge-u^{\mathrm{open}}_i+\Lambda_{i,t}$. (A partially filled order
whose stop is missing is charged $u^{\mathrm{pf}}_i$ in the same way.)
(2) *New or pending order on a fresh instrument* (G11), cumulative fill $e\le n$ (A-EXE-03) at prices $\le p^{\mathrm{lim}}$ (A-MKT-05) with entry fees
$\le\phi^{\mathrm{buy}}(e)$ (A-EXE-04): cash paid $\le e\,p^{\mathrm{lim}}+\phi^{\mathrm{buy}}(e)$ and, by A-TRIG with $q^{\mathrm{exp}}_i=e$,
$\mathrm{XV}_{i,t+1}\ge e(p^{\mathrm{stop}}_o-\kappa^{\mathrm{out}}(e))-\phi^{\mathrm{split}}(e)$; hence $\Delta_i\ge-L^{\mathrm{stop}}(e)\ge-L^{\mathrm{stop}}(n)$ (F061 with F140; monotone by
A-EXE-01, A-EXE-02, F140 and $p^{\mathrm{lim}}>p^{\mathrm{stop}}_o$ from G7). A pending order without fills is bounded with its limit, its current stop and the $\tau_t$
inputs — the same inputs A-TRIG uses. Its current stop may have been trailed to or above its limit after G7 checked it, so with
$x=p'^{\mathrm{lim}}-p^{\mathrm{stop}}+\kappa^{\mathrm{out}}(n')$ of either sign, $e\,x\le n'x^+$ for $0\le e\le n'$ and
$\Delta_i\ge-\big[n'x^++\phi^{\mathrm{split}}(n')+\phi^{\mathrm{buy}}(n')\big]$, which is exactly its F144 charge ($r^{\mathrm{pf}}$ with $q=0$; AUD-039); so these orders together are
bounded by their part of $R^{\mathrm{res}}_t$. (A value computed with older inputs is not enough: REV-028. Without the clamp the charge can be negative:
stop $51$, limit $50$, $\kappa^{\mathrm{out}}=0.1$, \$1 minimum fees, $n'=100$: $-87$ against a worst loss of $1.2$.) Unfilled orders give $\Delta_i=0$.
(2′) *Order partially filled before $\tau_t$* (AUD-033; closure form AUD-034): held $q_{i,t}>0$ and a pending remainder of the same order of
total quantity $n'$ at limit $p'^{\mathrm{lim}}$, fees $\phi^{\mathrm{paid}}_o$ already paid — one exposure (G11), charged $r^{\mathrm{pf}}_i$ (F145) in $R^{\mathrm{res}}_t$ and nothing in
$R^{\mathrm{open}}_t$. With $e\le n'-q_{i,t}$ filled in the period (A-EXE-03) at prices $\le p'^{\mathrm{lim}}$, the entry fees paid in the period are at most
$\phi^{\mathrm{buy}}(q_{i,t}+e)-\phi^{\mathrm{paid}}_o\le\phi^{\mathrm{buy}}(n')-\phi^{\mathrm{paid}}_o$ (A-EXE-04: all fees of the order $\le\phi^{\mathrm{buy}}$ of its cumulative fill). A-TRIG with
$q^{\mathrm{exp}}_i=q_{i,t}+e$ and $\kappa^{\mathrm{out}}_i(q^{\mathrm{exp}}_i)\le\kappa^{\mathrm{out}}_i(n')$, $\phi^{\mathrm{split}}(q^{\mathrm{exp}}_i)\le\phi^{\mathrm{split}}(n')$ gives
$\Delta_i\ge-\big[q_{i,t}(m_{i,t}-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(n'))+e(p'^{\mathrm{lim}}-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(n'))+\phi^{\mathrm{split}}(n')+\phi^{\mathrm{buy}}(n')-\phi^{\mathrm{paid}}_o\big]+\Lambda_{i,t}\ge-r^{\mathrm{pf}}_i+\Lambda_{i,t}$,
using $0\le e\le n'-q_{i,t}$, so $e\,x\le(n'-q_{i,t})x^+$ for $x=p'^{\mathrm{lim}}-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(n')$ of either sign — the current stop may have been
trailed to or above the limit (AUD-039; the unclamped `f37c1b6` charge breached the floor by $29$, T-10N). The paid fees and the filled quantity's entry price are realised and already in $W_t$; they are
not charged again. Two alternatives fail: charging only the unfilled remainder under-charges ($\kappa^{\mathrm{out}}(n)=0.001n$, no fees, $n'=200$,
$q_{i,t}=100$ marked at $52$, limit $50$, stop $49$: worst loss $440>r^{\mathrm{open}}_i+L^{\mathrm{stop}}(100)=420$); keeping the full-order reservation beside the held
part's open risk ($550$ here) charges realised fees and the filled quantity's risk twice (05 §5 example: over-charge $5.24$ including the paid
fee).
(3) Summing with $\mathrm{Inc}\ge0$: $W_{t+1}\ge W_t-(R^{\mathrm{open}}_t-\Lambda_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n))\ge W_t-K_t=F_t$.
Tiers G and U: identical with the tier's form of F072. ∎

**COUNTEREXAMPLE ATTEMPT.** (o) Closure re-derivation: exhaustive exact enumeration of one exposure (order of $6$ sh; $0$–$6$ filled at $\tau_t$;
marks $49,50,52$; further fills in the period at the limit or better; per-order minimum or linear fees, paid at once or late; constant or
super-additive $\kappa^{\mathrm{out}}$; $N^{\mathrm{ex}}=1,2,3$ exit orders plus a remainder at the cut; up to $3{,}456$ scenarios per configuration): worst loss $=$ charge
$-\Lambda_{i,t}$ in every state, never above it; two-period chains ($1{,}260$): realised loss plus remaining charge never below the total worst case,
and the worst life-of-order loss equals the initial reservation. (i) AUD-001 fill pattern on a new order (stop partially filled at the cut, per-order minimum fee, 05 §5):
$\mathrm{XV}=4{,}888<4{,}889$ violates A-TRIG, so it is outside the hypotheses; with F140 the charge is $113$ and the scenario satisfies both A-TRIG
and the conclusion ($W_{t+1}=F_t$). (ii) Several exit orders (one child stop per entry fill): with the two-part envelope A-TRIG fails
($4{,}887<4{,}888$); with $N^{\mathrm{ex}}=3$ in F140 it holds (REV-029). (iii) Inputs changed after reservation: F144 re-evaluates (REV-028).
(iv) The second independent review's randomised exact search inside the hypotheses (20,000 trials per case, tiers S, G, U) found no
violation, but it did not place the current stop at or above a pending limit; the third review's search did, and found $1{,}126$ breaches in
$5{,}882$ such trials of the `f37c1b6` charge (AUD-039). (v) Removing any hypothesis: T-10N. (vi) Closure with the clamp: exhaustive
enumeration with stops from $2$ below to $3$ above the limit, constant, super-additive and convex $\kappa^{\mathrm{out}}$, minimum and linear fees,
$N^{\mathrm{ex}}=1,2$ ($46{,}200$ scenarios, $1{,}800$ states): no understatement, exact in $1{,}250$ states; randomised exact search of F145 and F144
($20{,}000$ trials, $8{,}795$ with the stop at or above the limit): no understatement, against $1{,}772$ understatements without the clamp.

**NUMERICAL EDGE CASES.** Equality in the premise (floor attained, not breached); aggregates rounded up and $K_t$ rounded down (T-24); fees
quantised up (01 §9 item 15); $e=0$; a stop exactly at the limit ($x=\kappa^{\mathrm{out}}(n')>0$, clamp inactive); $-0$ rejected at the boundary.

**MACHINE-TESTABLE INVARIANT.** Simulator with adversarial paths drawn inside the tier's disturbance set (comonotone all-stops scenario,
triggered-unfilled states, split fills, partial exits at the cut) ⇒ $W_{t+1}\ge F_t$; F072 checked per exposure ex post; each T-10N
counterexample is a regression test that must fail when its hypothesis is removed; paths outside are logged as assumption violations with
breach magnitude.

---

### T-10N Floor Preservation Without the v0.2 Hypotheses

**THEOREM ID.** T-10N

**STATEMENT.** "T-10's conclusion holds under the v0.1 hypotheses, under the v0.1.1 hypotheses, or with any one of G11, A-TRIG, A-EXE-04,
A-FLOW-01, A-AUTH-02, F144, the clamp of F144 and F145, or D-06 removed."

**ASSUMPTIONS.** T-10's assumptions with the named element replaced or removed.

**PROOF STATUS.** DISPROVED

**PROOF (exact counterexamples).**
- *v0.1.1 per-case A-TRIG (AUD-001; v0.1.1 accounting, where $\Lambda_t=0$ was admissible):* $q=100$ at $50$, stop $49$, $\kappa^{\mathrm{out}}=0.1$, fee
  $\max(1,0.005k)$ per order, $\Lambda_t=0$, $r^{\mathrm{open}}=111=K_t$; the stop fills $50$ sh at $48.9$ paying $1$; the remaining $50$ sh are valued at their own
  per-case bound $2{,}444$; change $2{,}445-1+2{,}444-5{,}000=-112$ ⇒ $W_{t+1}=F_t-1$. Under v0.2 accounting ($\Lambda_t\ge1$) the held case gives $W_{t+1}=F_t$;
  the same fill pattern on a new order with $L^{\mathrm{stop}}=112=K_t$ gives $W_{t+1}=F_t-1$ (REV-030).
- *Add-on (no G11):* hold $100$ at $50$, stop $49$, $\kappa^{\mathrm{out}}(n)=0.001n$, $\Lambda(n)=0.001n^2$ ($r^{\mathrm{open}}=110$); add $100$ at $50$ ($L^{\mathrm{stop}}=110$);
  $K_t=220$; untriggered close at $49.01$ ⇒ change $-228$, floor breached by $8$, although A-TRIG holds for the combined holding ($9{,}762\ge9{,}760$).
- *Pending order at notional (v0.1 tier U):* pending $100$ @ $5$ charged $500$; new $100$ @ $5.94$ with \$1 minimum commissions, $L^{\mathrm{abs}}=596$;
  $K_t=1{,}096$; both fill, price → 0, both sold: $W_{t+1}=F_t-2$.
- *Triggered but unfilled at the cut (v0.1 A-TRIG):* hold $100$ at $50$, stop $49$, $\kappa^{\mathrm{out}}=0.1$ ($r^{\mathrm{open}}=110$); trigger just before $\tau_{t+1}$,
  mark $45$: $W$ falls $500$.
- *Per-execution fees (no A-EXE-04):* $\max(1,0.005k)$ per execution; a $100$-share exit filled $34/33/33$ pays $3>\phi(100)=1$.
- *Withdrawal (no A-FLOW-01):* $F=F^{\mathrm{abs}}=90$, $W=100$, $r^{\mathrm{open}}=10=K$, $X=-5$, stop fills at its bound: $W_{t+1}=85<90$.
- *Race (no A-AUTH-02 for the second decision; prevented by the integration rule A-AUTH-03):* two decisions from one snapshot each sized to
  $L^{\mathrm{stop}}=K_t$; each decision's ledger omits the other order ⇒ loss $2K_t$.
- *Stale reservation (ledger value instead of F144, REV-028):* pending $100$ at limit $50$, stop $49$, reserved with $\kappa^{\mathrm{out}}=0.1$: $R^{\mathrm{res}}=110=K_t$;
  at $\tau_t$ the F111 input is $\kappa^{\mathrm{out}}=0.5$; the order fills and exits at the A-TRIG bound $48.5$ ⇒ change $-150$, $W_{t+1}=F_t-40$.
- *Trailed stop without the clamp (`f37c1b6` F144, third review, AUD-039):* order $n'=200$ at limit $50$, stop $49$ at reservation ($\kappa^{\mathrm{out}}=0.1$,
  ledger value $220$), $100$ filled earlier; at $\tau_t$ bid/ask $51.99/52.01$ ($m=52$, $\Lambda_t=1$), stop trailed to $51$, F111 input
  $\kappa^{\mathrm{out}}(n)=0.00005n^2$: charge $r^{\mathrm{open}}+\max(220,\,200(50-51+2))=150+220=370=K_t$; the remainder fills at $50$ and all $200$ exit at $49$ (F072 with
  equality): change $-399$, $W_{t+1}=F_t-29$. The clamped F145 charges $400$ for the same state.
- *Gap (A-TRIG fails):* T-06b gap example. *Missing stop charged zero (violates D-06):* unbounded breach. *Non-monotone fees:* T-03N. ∎

**COUNTEREXAMPLE ATTEMPT.** The counterexamples are the proof.

**NUMERICAL EDGE CASES.** Per-order minimum fees; partial fills at the cut.

**MACHINE-TESTABLE INVARIANT.** Each item is a regression scenario.

---

### T-11 Risk-Reservation Conservation

**THEOREM ID.** T-11

**STATEMENT.** For a ledger of one budget family with components $\mathrm{Av}$ (available), $\mathrm{Rs}$ (reserved), $\mathrm{Op}$ (open) and fixed total
$\mathrm{Tot}$: (a) $\mathrm{Av}+\mathrm{Rs}+\mathrm{Op}=\mathrm{Tot}$ after every transition (F119); (b) $\mathrm{Av}\ge0$ always; (c) for any fill $e\le n$ at prices $\le p^{\mathrm{lim}}$, the
realised open risk is $\le$ the reserved $L^{\mathrm{stop}}(n)$; (d) on the terminal state, the release $L^{\mathrm{stop}}(n)-L^{\mathrm{stop}}(e)\ge0$.

**ASSUMPTIONS.** A-MATH-01; transitions RESERVE($y$) [requires $y\le\mathrm{Av}$, atomically with the version read — A-AUTH-03], FILL,
CANCEL/EXPIRE/REJECT, CLOSE; reservation vector F108 at $p^{\mathrm{lim}}$ with the order's stop (D-05), held until terminal — venue-confirmed filled, cancelled, expired or
rejected; a cancel request is not terminal (A-AUTH-05, AUD-050; ledger bookkeeping — the engine's budgets re-evaluate from the order state, F144, F145): FILL records the
fill and moves nothing out of $\mathrm{Rs}$; at the terminal state $L^{\mathrm{stop}}(e)$ moves to $\mathrm{Op}$ and the rest is released. The ledger's $\mathrm{Op}$ is a
book entry, not the mark-based $R^{\mathrm{open}}_t$ (F050). A-MKT-05; A-EXE-01, A-EXE-02, A-EXE-03, A-EXE-04.

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF.** (a) Each transition moves an amount between components. (b) Induction with the atomic guard. (c) Entry at $p^{\mathrm{in}}\le p^{\mathrm{lim}}$
(A-MKT-05) and monotonicity: $e(p^{\mathrm{in}}-p^{\mathrm{stop}}+\kappa^{\mathrm{out}}(e))+\phi^{\mathrm{buy}}(e)+\phi^{\mathrm{sell}}(e)\le L^{\mathrm{stop}}(e)\le L^{\mathrm{stop}}(n)$, with fees on cumulative
filled quantity (A-EXE-04). (d) Monotonicity. ∎

**COUNTEREXAMPLE ATTEMPT.** None within the hypotheses; naive schemes: T-11N.

**NUMERICAL EDGE CASES.** $y=\mathrm{Av}$ exactly (admitted); reservations rounded up, releases rounded down (T-24).

**MACHINE-TESTABLE INVARIANT.** Ledger replay property tests with random interleavings; engine: emitted reservation $\ge L^{\mathrm{stop}}(e)$ for all
$e\le Q$ and all entry prices $\le p^{\mathrm{lim}}$ (enumerated for small cases). The engine is pure: (a), (b), (d) are obligations of the external
ledger; the engine's obligation is F108.

---

### T-11N Naive Reservation Schemes

**THEOREM ID.** T-11N

**STATEMENT.** "Conservation and dominance hold for (i) reservation at mid, (ii) market orders, (iii) non-atomic check-then-reserve,
(iv) a stop widened after the fill without re-reservation, (v) non-monotone fees."

**ASSUMPTIONS.** T-11's with the named element replaced.

**PROOF STATUS.** DISPROVED

**PROOF.** (i) Realised risk exceeds the reservation by $e(p^{\mathrm{lim}}-m)$. (ii) No price bound: (c) fails. (iii) Available budget $1000$, two concurrent
reserves of $1000$ ⇒ available budget $-1000$. (iv) Open risk grows beyond the reservation. (v) T-03N example. ∎

**COUNTEREXAMPLE ATTEMPT.** The counterexamples are the proof.

**NUMERICAL EDGE CASES.** None specific.

**MACHINE-TESTABLE INVARIANT.** Each item is a regression scenario of the ledger model.

---

### T-12 No-Trade Under Insufficient Certified Advantage

**THEOREM ID.** T-12

**STATEMENT.** Under the rule "trade $a$ only if $\mathrm{LB}_t(a)>\varepsilon^{\min}$" (F027): $\mathrm{LB}_t(a)\le\varepsilon^{\min}\Rightarrow a$ is not chosen; a TRADE
decision implies $\mathrm{LB}_t(a)>\varepsilon^{\min}$.

**ASSUMPTIONS.** A-MATH-01; the decision rule; D-10 set to REQUIRED.

**PROOF STATUS.** PROVED

**PROOF.** By construction. ∎ The validity of $\mathrm{LB}_t$ ($\mathrm{LB}_t\le\Delta J_t$ with stated confidence) is OPEN-2.

**COUNTEREXAMPLE ATTEMPT.** None; the rule is vacuous if $\mathrm{LB}_t$ is invalid (OPEN-2).

**NUMERICAL EDGE CASES.** $\mathrm{LB}_t=\varepsilon^{\min}$ exactly (not traded); $\mathrm{LB}_t=-\infty$ (T-19) or NaN ⇒ not traded.

**MACHINE-TESTABLE INVARIANT.** TRADE ⇒ recorded $\mathrm{LB}_t>\varepsilon^{\min}$.

---

### T-12a Infimum of a Difference

**THEOREM ID.** T-12a

**STATEMENT.** For families $J^{(1)}_{\mathbb Q},J^{(2)}_{\mathbb Q}$ indexed by $\mathbb Q\in\mathcal P$ with finite infima:
$\inf_{\mathbb Q}(J^{(1)}_{\mathbb Q}-J^{(2)}_{\mathbb Q})\le\inf_{\mathbb Q}J^{(1)}_{\mathbb Q}-\inf_{\mathbb Q}J^{(2)}_{\mathbb Q}$ (F117).

**ASSUMPTIONS.** A-MATH-01; finite infima.

**PROOF STATUS.** PROVED

**PROOF.** For any $\mathbb Q'$: $\inf(J^{(1)}-J^{(2)})\le J^{(1)}_{\mathbb Q'}-J^{(2)}_{\mathbb Q'}\le J^{(1)}_{\mathbb Q'}-\inf J^{(2)}$; take the infimum over $\mathbb Q'$. ∎

**COUNTEREXAMPLE ATTEMPT.** The inequality can be strict; using the right-hand side as a certificate fails: T-12N.

**NUMERICAL EDGE CASES.** Infinite infima ($-\infty-(-\infty)$) excluded by hypothesis and must be checked (T-19).

**MACHINE-TESTABLE INVARIANT.** Property test over random finite families.

---

### T-12N Difference of Infima as a Certificate

**THEOREM ID.** T-12N

**STATEMENT.** "$\mathrm{LB}^{\mathrm{naive}}=\inf_{\mathbb Q}J_{\mathbb Q}(a)-\inf_{\mathbb Q}J_{\mathbb Q}(a^{\varnothing})>0$ implies that $a$ is better than $a^{\varnothing}$ under every $\mathbb Q\in\mathcal P$."

**ASSUMPTIONS.** Finite $\mathcal P$.

**PROOF STATUS.** DISPROVED

**PROOF.** $\mathbb Q_1$: $J(a)=1$, $J(a^{\varnothing})=0$; $\mathbb Q_2$: $J(a)=2$, $J(a^{\varnothing})=3$. $\mathrm{LB}^{\mathrm{naive}}=1-0=1>0$, but
$\inf(J(a)-J(a^{\varnothing}))=\min(1,-1)=-1$: under $\mathbb Q_2$ not trading is better. ∎

**COUNTEREXAMPLE ATTEMPT.** The counterexample is the proof.

**NUMERICAL EDGE CASES.** None specific.

**MACHINE-TESTABLE INVARIANT.** Unit test reproducing the example; the certificate uses the infimum of the difference (F027).

---

### T-12b Additive Error Allowance

**THEOREM ID.** T-12b

**STATEMENT.** If $\lvert\hat J(a)-J(a)\rvert\le\varepsilon^{\mathrm{err}}_a$ and $\lvert\hat J(a^{\varnothing})-J(a^{\varnothing})\rvert\le\varepsilon^{\mathrm{err}}_0$ surely, then
$\hat J(a)-\hat J(a^{\varnothing})-\varepsilon^{\mathrm{err}}_a-\varepsilon^{\mathrm{err}}_0\le\Delta J(a)$ (F118). If each bound holds with probability $\ge1-\delta^{\mathrm{conf}}_a$,
$\ge1-\delta^{\mathrm{conf}}_0$, the conclusion holds with probability $\ge1-\delta^{\mathrm{conf}}_a-\delta^{\mathrm{conf}}_0$; over $k$ decisions the family-wise error is at
most $k(\delta^{\mathrm{conf}}_a+\delta^{\mathrm{conf}}_0)$.

**ASSUMPTIONS.** A-MATH-01; the error bounds as hypotheses.

**PROOF STATUS.** PROVED

**PROOF.** Triangle inequality; union bound. ∎

**COUNTEREXAMPLE ATTEMPT.** None; whether realistic bounds exist is RQ-14/RQ-15, misspecification is outside the statement.

**NUMERICAL EDGE CASES.** $\varepsilon^{\mathrm{num}}$ certified at the returned action; solver tolerances are not part of the certificate.

**MACHINE-TESTABLE INVARIANT.** Property test with synthetic objectives and injected errors inside the bounds.

---

### T-12c Tighter Bound for Correlated Estimation Errors

**THEOREM ID.** T-12c

**STATEMENT.** For estimators in which a common parameter error drives both $\hat J(a)$ and $\hat J(a^{\varnothing})$, a confidence bound on the
error of $\hat J(a)-\hat J(a^{\varnothing})$ can be computed that is strictly tighter than the sum of the two separate T-12b bounds.

**ASSUMPTIONS.** A model class for $J$ (RQ-13) and an error model (RQ-14).

**PROOF STATUS.** NOT YET PROVEN

**PROOF.** None. (Elementary facts only: the difference error never exceeds the sum of the separate errors, and identical errors cancel.)

**COUNTEREXAMPLE ATTEMPT.** None found.

**NUMERICAL EDGE CASES.** n/a until the model class is chosen.

**MACHINE-TESTABLE INVARIANT.** n/a (research question RQ-14).

---

### T-13 Safe-Action Membership

**THEOREM ID.** T-13

**STATEMENT.** For every input, the emitted action is $a^{\varnothing}$ or an element of $\mathcal A^{\mathrm{safe}}(x_t)$ (F024), and $\mathcal D$ terminates.

**ASSUMPTIONS.** A-MATH-01; T-03; Art. 18 (every non-TRADE path emits $a^{\varnothing}$).

**PROOF STATUS.** PROVED

**PROOF.** The last step before emission is $V$ (F126, T-03(c)); every other path emits $a^{\varnothing}$. The search terminates in
$\lceil\log_2(\bar N/\delta_q)\rceil+1$ exact evaluations per constraint. ∎ (Specification level; implementation conformance is R7b.)

**COUNTEREXAMPLE ATTEMPT.** None at specification level.

**NUMERICAL EDGE CASES.** Very large $\bar N/\delta_q$ (bounded bisection count); exceptions inside $\mathcal D$ ⇒ $a^{\varnothing}$.

**MACHINE-TESTABLE INVARIANT.** An independent slow oracle re-checks membership of every emitted TRADE; fuzzed inputs never raise out of $\mathcal D$.

---

### T-14 Replay Determinism

**THEOREM ID.** T-14

**STATEMENT.** $\mathcal D$ applied twice to byte-identical $(\mathsf S_t,o,\theta,\mathsf v)$ yields byte-identical records, across processes, machines and restarts.

**ASSUMPTIONS.** A-MATH-01; Art. 8; 01 §9 items 10 and 17 (canonical serialisation, strict document, key order, SHA-256), 11 (reproducibility)
and 13 (one $-0$ rule); sorted iteration; local numeric contexts.

**PROOF STATUS.** PROVED

**PROOF.** $\mathcal D$ is a function of its inputs (F006) and the serialisation is canonical. ∎

**COUNTEREXAMPLE ATTEMPT.** Implementation-level threats (hash-seed iteration order FM-NUM-11, mutated global decimal context FM-NUM-10,
`-0.00` serialisation FM-NUM-14, float representation) are excluded by the listed rules; none at specification level.

**NUMERICAL EDGE CASES.** $-0$ versus $0$ (review Z03–Z06); locale-dependent formatting.

**MACHINE-TESTABLE INVARIANT.** Golden-record replay across processes with different hash seeds, locales and pre-mutated global decimal contexts.

---

### T-15 Economic Cost Accounting Identity

**THEOREM ID.** T-15

**STATEMENT.** For the transitions F051–F055 and the reference-price chains F057, the identity F058 holds exactly and every primitive cash or
price event appears once on its right-hand side (05 §3).

**ASSUMPTIONS.** A-MATH-01; definitions F033–F035, F051–F057; a corporate action splits the period (F054).

**PROOF STATUS.** PROVED

**PROOF.** 05 §2 (F055) and §3 (telescoping of F057). ∎ *Scope:* the identity is about the transition model; that the real ledger
follows the model is A-ACC-03, which is outside the statement.

**COUNTEREXAMPLE ATTEMPT.** A corporate action inside a period without the split books a 2:1 split as a loss (05 §1) — excluded by F054.

**NUMERICAL EDGE CASES.** Exact arithmetic; fees quantised before booking so both sides use the booked value.

**MACHINE-TESTABLE INVARIANT.** For simulated ledgers both sides agree exactly.

---

### T-16 Expected-Value Sizing Is Cap Sizing

**THEOREM ID.** T-16

**STATEMENT.** If $J(n)=\mathbb E[W_{t+1}(n\mathbf 1_i)-W_t]$ is affine in $n$ on $\mathbb L\cap[0,Q^{\mathrm{hard}}]$, then $\arg\max J$ contains $0$ or $Q^{\mathrm{hard}}$ (F130).

**ASSUMPTIONS.** A-MATH-01; affinity (linear costs, no impact) as hypothesis.

**PROOF STATUS.** PROVED

**PROOF.** An affine function on a finite ordered set attains its maximum at an endpoint. ∎

**COUNTEREXAMPLE ATTEMPT.** None within the hypothesis.

**NUMERICAL EDGE CASES.** Constant $J$ (every size maximises): a deterministic tie-break rule is required (T-14) and is **UNDEFINED**.

**MACHINE-TESTABLE INVARIANT.** Property test with affine objectives.

---

### T-17a Naive Stop-Risk Envelope Admits Unbounded Notional

**THEOREM ID.** T-17a

**STATEMENT.** For the naive envelope $Q=\delta_q\lfloor f^{\mathrm{trd}}W/(\delta_q\ell^{\mathrm{stop}})\rfloor$ with $\ell^{\mathrm{stop}}$ the stop distance only (F110), admissible
notional is unbounded as $\ell^{\mathrm{stop}}\to0$, and one gap of fraction $\Gamma_i$ loses more than $W$ whenever $\ell^{\mathrm{stop}}<f^{\mathrm{trd}}\Gamma_ip$ (up to lattice
rounding; F128).

**ASSUMPTIONS.** A-MATH-01.

**PROOF STATUS.** PROVED

**PROOF.** Entry $p$, stop $p-\ell^{\mathrm{stop}}$, $Q=f^{\mathrm{trd}}W/\ell^{\mathrm{stop}}$ (take it on the lattice). A gap exit at $(1-\Gamma_i)(p-\ell^{\mathrm{stop}})$ loses
$\Gamma_ip+(1-\Gamma_i)\ell^{\mathrm{stop}}\ge\Gamma_ip$ per share, in total $\ge f^{\mathrm{trd}}W\Gamma_ip/\ell^{\mathrm{stop}}>W$ when $\ell^{\mathrm{stop}}<f^{\mathrm{trd}}\Gamma_ip$. Numeric:
$W=100{,}000$, $f^{\mathrm{trd}}=1\%$, $\ell^{\mathrm{stop}}=0.01$, $p=50$ ⇒ $Q=100{,}000$ sh, notional $5{,}000{,}000$; $\Gamma_i=5\%$ ⇒ loss $250{,}950\approx2.5W$. ∎

**COUNTEREXAMPLE ATTEMPT.** n/a (existence statement).

**NUMERICAL EDGE CASES.** $\ell^{\mathrm{stop}}\to0$ is a division hazard; G7 rejects per-share loss below $\ell^{\min}p^{\mathrm{lim}}$.

**MACHINE-TESTABLE INVARIANT.** Regression scenario.

---

### T-17b Stop-Risk Budget With an Exit-Cost Floor

**THEOREM ID.** T-17b

**STATEMENT.** If $\kappa^{\mathrm{out}}\ge\kappa^{\min}p^{\mathrm{stop}}$ with $\kappa^{\min}>0$ (F111) and $B\le W$ (B1–B3), every $n$ admitted by H1 satisfies
$n\,p^{\mathrm{lim}}\le f^{\mathrm{trd}}Wp^{\mathrm{lim}}/(\kappa^{\min}p^{\mathrm{stop}})$ (F128). The bound exceeds $W$ iff $f^{\mathrm{trd}}p^{\mathrm{lim}}>\kappa^{\min}p^{\mathrm{stop}}$.

**ASSUMPTIONS.** A-MATH-01; F111; $B\le W$.

**PROOF STATUS.** PROVED

**PROOF.** $L^{\mathrm{stop}}(n)\ge n\kappa^{\mathrm{out}}\ge n\kappa^{\min}p^{\mathrm{stop}}$ (the other terms of F061 are $\ge0$ by G7) and H1 gives $L^{\mathrm{stop}}(n)\le f^{\mathrm{trd}}B\le f^{\mathrm{trd}}W$.
Examples: $f^{\mathrm{trd}}=0.1\%$, $p^{\mathrm{lim}}=10$, $\kappa^{\min}p^{\mathrm{stop}}=0.01$ ⇒ notional $\le W$; $f^{\mathrm{trd}}=1\%$, $p^{\mathrm{lim}}=50$, $\kappa^{\min}p^{\mathrm{stop}}=0.01$ ⇒
notional $\le50W$. ∎

**COUNTEREXAMPLE ATTEMPT.** $\kappa^{\min}=0$ returns to T-17a (no bound).

**NUMERICAL EDGE CASES.** $\kappa^{\min}p^{\mathrm{stop}}$ tiny ⇒ bound huge; notional caps H7–H11 are therefore necessary.

**MACHINE-TESTABLE INVARIANT.** For random admissible inputs, the H1-only cap never exceeds the bound.

---

### T-18 Comonotone Aggregation

**THEOREM ID.** T-18

**STATEMENT.** If $\mathcal L_i\le b_i$ surely for each $i$, then $\sum_i\mathcal L_i\le\sum_ib_i$ for every joint law; and if each bound is attainable
with no dependence restriction, the supremum of $\sum_i\mathcal L_i$ is $\sum_ib_i$ (F134).

**ASSUMPTIONS.** A-MATH-01.

**PROOF STATUS.** PROVED

**PROOF.** Summation; the joint scenario in which every bound is attained is admissible. ∎

**COUNTEREXAMPLE ATTEMPT.** None; any diversification credit needs a dependence assumption and belongs to the model layer, where it can
only tighten (Art. 5).

**NUMERICAL EDGE CASES.** Sums rounded up.

**MACHINE-TESTABLE INVARIANT.** The simulator's all-bounds-attained scenario equals $\sum_ib_i$ exactly.

---

### T-19 Log-Growth Domain

**THEOREM ID.** T-19

**STATEMENT.** $W_{t+1}(a)\ge W^{\min}_{t+1}(a)$ surely (F070, all terms $\mathcal F_t$-measurable). If $W^{\min}_{t+1}(a)>0$ then
$\log(W_{t+1}/W_t)\ge\log(W^{\min}_{t+1}/W_t)>-\infty$ under every law supported on prices $\ge0$. If some admissible law charges $\{W_{t+1}\le0\}$ the
(robust) log objective is $-\infty$; a Wasserstein ball with unrestricted support contains such a law for any position with positive exposure.

**ASSUMPTIONS.** A-MATH-01; T-10's common hypotheses (AUD-043): A-SCOPE-03, A-SCOPE-05 with G11, A-FLOW-01, A-ACC-01…04, A-ACC-06,
A-MKT-05 (fills at or below the limit), A-EXE-01…05 (A-EXE-05: no other orders), A-AUTH-02, A-AUTH-04, pending orders by F144; A-ACC-07
with $\mathrm{Fin}=0$, $\mathrm{Inc}\ge0$ and $\mathrm{Accr}_{t+1}\le\bar A_{t+1}$ (S-185) in place of $\mathrm{Accr}=0$; A-MKT-01; A-ACC-05 (tier-U form of F072 with F140); $W_t>0$.

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF.** Tier-U bound: every position worthless, each exposure's exit fees at most $\phi^{\mathrm{split}}_{i,0}(\bar q_i)$ (A-ACC-05, F140, monotone), pending orders filled
at their limits with at most their remaining fees and the new order at $L^{\mathrm{abs}}(n)$; realised costs are already in $C_t$ (AUD-038); monotonicity of
$\log$. The ball contains the mixture of $\hat{\mathbb P}$ (weight $1-\epsilon^{\mathrm{mix}}$) with a point mass at a scenario $\xi_0$ in which every price is
$0$, at finite transport cost for small $\epsilon^{\mathrm{mix}}$. ∎

**COUNTEREXAMPLE ATTEMPT.** The pre-review $W^{\min}$ without a flow term: $W_t=100$ cash only, $X=-100$ ⇒ $W_{t+1}=0$ while the old bound was $100$
(REV-012). With per-order minimum fees and a holding sold in part at price $0$ (fee $1$) while the remainder is valued with its own fee
($\Lambda=1$), $W_{t+1}=W^{\min}_{t+1}-1$ unless F070 uses $\phi^{\mathrm{split}}$ (REV-034). Without the common hypotheses (third review, AUD-043): $C=1{,}000$,
pending $10$ @ $10$, $W^{\min}=900$; a fill at $12$ above the limit (A-MKT-05 fails) then prices → $0$ gives $880<900$; a manual buy of $90$ @ $10$
(A-EXE-05 fails) gives $W_{t+1}=0$ and an undefined logarithm.

**NUMERICAL EDGE CASES.** `Decimal(0).ln()` returns `-Infinity` without a signal (observed): the domain check precedes evaluation;
$W^{\min}=0$ exactly is excluded (strict inequality).

**MACHINE-TESTABLE INVARIANT.** For random admissible actions, $W_{t+1}\ge W^{\min}_{t+1}$ with equality in the all-prices-zero scenario;
evaluation refuses $\log$ when $W^{\min}_{t+1}\le0$.

---

### T-20a Cushion Invariance Under Hold, Static Floor

**THEOREM ID.** T-20a

**STATEMENT.** If the floor is static ($F_{t+1}=F_t$: no HWM or profit-lock ratchet, no daily/weekly reset in between), then
$R^{\mathrm{open}}_t\le K_t\Rightarrow R^{\mathrm{open}}_{t+1}\le K_{t+1}$ (F124).

**ASSUMPTIONS.** A-MATH-01; A-SCOPE-03; every position has a live stop; A-EXE-05 with no fills other than stop exits (no new or pending
orders); A-TRIG; **A-EXE-06** (every stop triggered in the period is fully executed by the cut; added v0.2, AUD-014, widened after REV-026);
$\kappa^{\mathrm{out}}$, $\phi^{\mathrm{sell}}$ and $\Lambda$ of untriggered positions constant over the period; A-ACC-06; A-ACC-07; A-FLOW-01.

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF.** Untriggered $i$: $\Delta r^{\mathrm{open}}_i=q_i\Delta m_i$ and the change of its value is $q_i\Delta m_i$ ($\Lambda$ constant). Triggered $i$: by A-EXE-06 fully
executed by the cut, so $r^{\mathrm{open}}_{i,t+1}=0$, and by A-TRIG (with $q^{\mathrm{rem}}=0$) and $\Lambda_{i,t}\ge0$ the value lost on $i$ is at most $r^{\mathrm{open}}_{i,t}$. Hence
$\Delta W\ge\Delta R^{\mathrm{open}}$ (using $\mathrm{Inc}\ge0$) and $\Delta K=\Delta W$ (static floor), so $K_{t+1}-R^{\mathrm{open}}_{t+1}\ge K_t-R^{\mathrm{open}}_t\ge0$. ∎

**COUNTEREXAMPLE ATTEMPT.** Stop triggered but not executed at the cut (REV-026, exact): $q=100$, stop $49$, $\kappa^{\mathrm{out}}=0.1$, no fees; at $\tau_t$
bid $49.99$, ask $50.01$ ($\Lambda_t=1$), $K_t=R^{\mathrm{open}}_t=110$, static floor; at $\tau_{t+1}$ the stop has triggered, nothing is executed, bid $48.9$, ask $49.0$
($\Lambda_{t+1}=5$): A-TRIG holds ($\mathrm{XV}=4{,}890\ge4{,}890$) but $K_{t+1}=1<r^{\mathrm{open}}_{t+1}=5$. A stop partially executed at the cut breaks the
invariant in the same way (AUD-014). Both violate A-EXE-06, which shows the hypothesis is needed.

**NUMERICAL EDGE CASES.** Equality $R^{\mathrm{open}}_t=K_t$ is preserved as equality when nothing triggers.

**MACHINE-TESTABLE INVARIANT.** Simulator under a static floor; snapshots with a triggered or partially executed stop are flagged RECOVERY.

---

### T-20b Cushion Invariance Under a Ratcheting Floor

**THEOREM ID.** T-20b

**STATEMENT.** "T-20a's implication holds when the floor ratchets ($F^{\mathrm{dd}}$ or $F^{\mathrm{lock}}$ at a new high, or a daily/weekly reset after a gain)."

**ASSUMPTIONS.** T-20a's, with a ratcheting floor (F040–F042).

**PROOF STATUS.** DISPROVED

**PROOF.** T-06b ratchet example: $r^{\mathrm{open}}=49.5>K=14$ after the gain. Calendar reset (06 §7): $\ell^{\mathrm{day}}=2\%$, $W=100$ (cash $50$ + one share at $50$,
stop $49$): $K=2\ge r^{\mathrm{open}}=1$; the share closes at $55$: $K=7$, $r^{\mathrm{open}}=6$; next day $F^{\mathrm{day}}=102.9$, $K=2.1<6$. ∎

**COUNTEREXAMPLE ATTEMPT.** The counterexamples are the proof.

**NUMERICAL EDGE CASES.** None specific.

**MACHINE-TESTABLE INVARIANT.** Regression scenarios; the engine emits RECOVERY with the required reduction $R^{\mathrm{open}}-K$ (RQ-09).

---

### T-21 Cushion Necessity and Sufficiency

**THEOREM ID.** T-21

**STATEMENT (closure form; F143).** Let $\mathcal W^{\mathrm{S}}$ be all period outcomes consistent with the tier-S hypotheses of T-10, with the bounds
attainable (every order may fill fully at its limit with the maximal fees allowed by A-EXE-04; every exposure may realise its A-TRIG bound
F072 with equality, and every exposure without a stop its tier-U bound; no dependence restriction), and let the charges be those of F064, F066
(D-06), F144, F145 and F061 at the $\tau_t$ inputs.
(a) *Sufficient condition:* $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t+\Lambda_t$ implies $W_{t+1}\ge F_t$ for every outcome in $\mathcal W^{\mathrm{S}}$.
(b) *Necessary condition, when no clamp is active* ($p'^{\mathrm{lim}}-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(n')\ge0$ for every pending order): if $W_{t+1}\ge F_t$ for every
outcome in $\mathcal W^{\mathrm{S}}$, then $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t+\Lambda_t$.
(c) *Equivalence:* when no clamp is active, by (a) and (b), floor safety on $\mathcal W^{\mathrm{S}}$ holds **iff** $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t+\Lambda_t=E_t-F_t$.
With an active clamp only (a) holds: the charge includes the unfilled part's fees, which no outcome with $e=0$ incurs.
(d) *The hard-layer condition* F120 ($\le K_t$) is sufficient. It is **not** necessary when $\Lambda_t>0$: states with
$K_t<R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t+\Lambda_t$ are floor-safe. When $\Lambda_t=0$ (e.g. a flat book) it coincides with (c).

**ASSUMPTIONS.** Those of T-10 (including case (1′)); attainability and inactive clamps (for (b) and (c) only).

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF.** (a) Step (3) of T-10 gives $W_{t+1}\ge W_t-(R^{\mathrm{open}}_t-\Lambda_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n))\ge W_t-K_t=F_t$. (b) In the attainable comonotone outcome
every held exposure realises $\Delta_i=-r^{\mathrm{open}}_i+\Lambda_{i,t}$ (without a stop: $-u^{\mathrm{open}}_i+\Lambda_{i,t}$, prices → $0$), every partially filled order $\Delta_i=-r^{\mathrm{pf}}_i+\Lambda_{i,t}$ (it fills fully at its limit, pays
$\phi^{\mathrm{buy}}(n')-\phi^{\mathrm{paid}}_o$, and exits at its bound with fees $\phi^{\mathrm{split}}(n')$), every other pending order and the new order $\Delta_i=-L^{\mathrm{stop}}$, and
$\mathrm{Inc}=0$; so $W_{t+1}=W_t-(R^{\mathrm{open}}_t-\Lambda_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n))$, which is $<F_t$ whenever the condition fails. (c) (a) and (b); $K_t+\Lambda_t=E_t-F_t$
by F034, F044. (d) $\Lambda_t\ge0$ (A-ACC-06) gives sufficiency; the AUD-032 example below is a floor-safe state violating F120. ∎

**COUNTEREXAMPLE ATTEMPT.** The v0.1.1 form ("iff $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t$") is false in the "only if" direction whenever
$\Lambda_t>0$: $q=100$ at $50$, stop $49$, $\kappa^{\mathrm{out}}=0.1$, no fees, $\Lambda_t=5$, $K_t=106<r^{\mathrm{open}}=110$, yet the worst attainable outcome leaves
$W_{t+1}=F_t+1$ (AUD-032). The v0.2 draft's "iff" also failed while a partially filled order was charged open risk plus the full reservation
(REV-025: charge $550>K_t+\Lambda_t=440$, worst outcome $W_{t+1}=F_t$); with F145 that charge is exact. The exhaustive enumeration of T-10 (o) found the
charge minus $\Lambda$ equal to the attained worst loss in every state, which is (b) instance by instance. The `f37c1b6` statement "F120 is
sufficient" was false for a stop trailed above a pending limit (AUD-039; T-10N); with the clamp (a) holds in all $46{,}200$ enumerated scenarios.

**NUMERICAL EDGE CASES.** At the boundary the attained outcome gives $W_{t+1}=F_t$ exactly.

**MACHINE-TESTABLE INVARIANT.** Simulator: at $R^{\mathrm{open}}_t-\Lambda_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)=K_t$ the attained comonotone outcome gives $W_{t+1}=F_t$; one lattice
step more gives a breach.

---

### T-22 Binary64 Floor Safety Condition

**THEOREM ID.** T-22

**STATEMENT.** Let $R$ (in USD) $=A_R/D_R$ and $\delta_q\ell$ (in USD) $=A_\ell/D_\ell$ with positive integers, $q^{*}=R/(\delta_q\ell)$ (dimensionless) and
$q^{\mathrm{fl}}=\mathrm{RN}(\mathrm{RN}(R)/\mathrm{RN}(\delta_q\ell))$ in IEEE-754 binary64 with round-to-nearest, positive normal operands and no overflow or
underflow. If $A_RD_\ell<2^{51}\approx2.25\times10^{15}$ then $\lfloor q^{\mathrm{fl}}\rfloor\le\lfloor q^{*}\rfloor$ (F116).

**ASSUMPTIONS.** A-MATH-01; the conditions of A-NUM-03, written into the statement.

**PROOF STATUS.** PROVED

**PROOF.** $q^{\mathrm{fl}}=q^{*}(1+\varepsilon^{\mathrm{rd}}_1)(1+\varepsilon^{\mathrm{rd}}_3)/(1+\varepsilon^{\mathrm{rd}}_2)$ with $\lvert\varepsilon^{\mathrm{rd}}_k\rvert\le\epsilon^{\mathrm{mach}}=2^{-53}$, so
$q^{\mathrm{fl}}-q^{*}\le4\epsilon^{\mathrm{mach}}q^{*}$ (F115; $(1+u)^2/(1-u)-1\le4u$ for $0\le u\le1/5$), and $q^{*}=A_RD_\ell/(A_\ell D_R)\le A_RD_\ell$. If $q^{*}\in\mathbb Z$,
an overshoot needs $4\epsilon^{\mathrm{mach}}q^{*}\ge1$, i.e. $q^{*}\ge2^{51}$ — impossible. Otherwise $\lceil q^{*}\rceil-q^{*}\ge1/(A_\ell D_R)$, and an overshoot needs
$4\epsilon^{\mathrm{mach}}A_RD_\ell/(A_\ell D_R)\ge1/(A_\ell D_R)$, i.e. $A_RD_\ell\ge2^{51}$. ∎

**COUNTEREXAMPLE ATTEMPT.** Random search over $2\times10^6$ realistic cent/basis-point inputs inside the condition: none (observed).
Outside the condition: T-22N.

**NUMERICAL EDGE CASES.** Exact quotient an integer (e.g. $0.3/0.1$: binary64 floor $2$ versus exact $3$ — under-sizing, safe, but a float
oracle disagrees with the exact implementation, review B01); subnormal or huge operands excluded.

**MACHINE-TESTABLE INVARIANT.** On inputs satisfying the condition, the binary64 floor never exceeds the exact floor (property test).

---

### T-22N Binary64 Floor Without the Condition

**THEOREM ID.** T-22N

**STATEMENT.** "The binary64 evaluation of the floor of $R/(\delta_q\ell)$ never exceeds the exact floor, for all positive decimal inputs."

**ASSUMPTIONS.** IEEE-754 binary64 semantics only.

**PROOF STATUS.** DISPROVED

**PROOF.** $R=172{,}808{,}193.53$, $\ell=65.68583269$, $\delta_q=1$ sh: binary64 gives $2{,}630{,}829$, exact $2{,}630{,}828$ (observed); the product of numerator
and denominator in the T-22 condition is $\approx1.7\times10^{18}>2^{51}$. ∎

**COUNTEREXAMPLE ATTEMPT.** The counterexample is the proof.

**NUMERICAL EDGE CASES.** High-resolution prices; large budgets.

**MACHINE-TESTABLE INVARIANT.** Regression; binary64 is never used on the authority path (Art. 7).

---

### T-23 Sequential Allocation Order-Dependence

**THEOREM ID.** T-23

**STATEMENT.** Greedy sequential sizing of several opportunities against one shared budget is not order-independent.

**ASSUMPTIONS.** A-MATH-01.

**PROOF STATUS.** PROVED

**PROOF (example).** Shared budget $R=1000$; opportunity $o_1$ with $\ell=3$, opportunity $o_2$ with $\ell=7$. Order $o_1,o_2$ gives $Q=333$ then $Q=0$;
order $o_2,o_1$ gives $Q=142$ then $Q=2$. ∎

**COUNTEREXAMPLE ATTEMPT.** n/a (existence statement).

**NUMERICAL EDGE CASES.** Ties in the ordering key.

**MACHINE-TESTABLE INVARIANT.** Replays with the authoritative ordering key (RQ-27) are identical; permuted inputs without it may differ.

---

### T-24 Rounding Conservatism

**THEOREM ID.** T-24

**STATEMENT.** If $\hat g_k(n)\ge g_k(n)$ for all $n$ and $\hat b_k\le b_k$, then $\{n:\hat g_k(n)\le\hat b_k\}\subseteq\{n:g_k(n)\le b_k\}$ and $\hat Q_k\le Q_k$ (F129).

**ASSUMPTIONS.** A-MATH-01.

**PROOF STATUS.** PROVED

**PROOF.** $g_k(n)\le\hat g_k(n)\le\hat b_k\le b_k$. ∎

**COUNTEREXAMPLE ATTEMPT.** Other rounding directions: T-24N.

**NUMERICAL EDGE CASES.** Fees and limit prices rounded up, budgets down (01 §9 item 15; review HC01–HC04).

**MACHINE-TESTABLE INVARIANT.** Every rounding site is checked against the direction table (01 §9); property test.

---

### T-24N Rounding in Other Directions

**THEOREM ID.** T-24N

**STATEMENT.** "Round-to-nearest (half-up or half-even) of quantities, consumptions or budgets is conservative."

**ASSUMPTIONS.** T-24's with nearest rounding.

**PROOF STATUS.** DISPROVED

**PROOF.** $b=1000.00$, $\ell=2.90$: half-up and half-even give $345$ sh, consumption $1000.50>b$ (review B03, B04); a fee of $0.005$ rounded half-even to
cents becomes $0.00$ (HC03). ∎

**COUNTEREXAMPLE ATTEMPT.** The counterexamples are the proof.

**NUMERICAL EDGE CASES.** Exact half-cent values.

**MACHINE-TESTABLE INVARIANT.** Regression tests.

---

### T-25 Floor-Breach Decomposition

**THEOREM ID.** T-25

**STATEMENT.** Under the tier-S hypotheses of T-10 except A-TRIG, and the premise $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t$:
$\{W_{t+1}<F_t\}\subseteq\bigcup_i\{\text{A-TRIG fails for exposure }i\}$, hence $\mathrm{PB}_t\le\sum_i\mathbb P(\text{A-TRIG fails for }i)$ (F123).

**ASSUMPTIONS.** T-10's except A-TRIG; the premise.

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF.** If A-TRIG holds for every exposure, T-10 gives $W_{t+1}\ge F_t$ (contrapositive); union bound. ∎

**COUNTEREXAMPLE ATTEMPT.** Without the premise: $W_t=F_t-1$, no positions, no trade — a breach with no exposure (REV-004). "A-TRIG fails" includes a
jump of the model estimate $\hat\Lambda_{i,t+1}$ that values a remainder at the cut, with no price move and no stop event: $q=100$, $K_t=110$,
$\hat\Lambda_{t+1}=200$ ⇒ $W_{t+1}=F_t-89$ (AUD-048); the failure probability in F123 therefore has a model component.

**NUMERICAL EDGE CASES.** None specific.

**MACHINE-TESTABLE INVARIANT.** In simulation every breach is attributed to at least one exposure whose $\mathrm{XV}$ violated F072.

---

### T-26 VaR Non-Subadditivity

**THEOREM ID.** T-26

**STATEMENT.** $\mathrm{VaR}_\beta$ (F009) is not subadditive.

**ASSUMPTIONS.** A-MATH-01.

**PROOF STATUS.** PROVED

**PROOF (counterexample).** Two independent positions each lose $100$ with probability $0.04$, else $0$. $\mathrm{VaR}_{0.95}$ of each is $0$; the sum loses
$\ge100$ with probability $1-0.96^2=0.0784>0.05$, so $\mathrm{VaR}_{0.95}$ of the sum is $100>0$. ∎

**COUNTEREXAMPLE ATTEMPT.** n/a (existence statement).

**NUMERICAL EDGE CASES.** None.

**MACHINE-TESTABLE INVARIANT.** VaR is never used as an aggregatable budget.

---

### OPEN-1 Multi-Step Viability Kernel

**THEOREM ID.** OPEN-1

**STATEMENT.** Under tier-S disturbances with an available trailing/de-risking control, the robust viability kernel of $\{W\ge F\}$ equals
$\{R^{\mathrm{open}}\le E-F\}$ on states without pending orders (cf. T-21); under the maximal disturbance set with exits impossible it equals $\{Z^{\mathrm{open}}\le E-F\}$ (F122).

**ASSUMPTIONS.** Tier-S (resp. tier-U) hypotheses in every period; control set of the external authority.

**PROOF STATUS.** NOT YET PROVEN

**PROOF.** None.

**COUNTEREXAMPLE ATTEMPT.** None found.

**NUMERICAL EDGE CASES.** n/a.

**MACHINE-TESTABLE INVARIANT.** Kernel computation on small discretised models (AA-10) compared with the conjectured sets.

---

### OPEN-2 Certified-Advantage Validity

**THEOREM ID.** OPEN-2

**STATEMENT.** $\mathrm{LB}_t(a)\le\Delta J_t(a)$ with probability $\ge1-\delta^{\mathrm{conf}}$ (F027).

**ASSUMPTIONS.** $J$ (RQ-13), $\mathcal P^{\mathrm{conf}}_t$ (RQ-12), an error model (RQ-14).

**PROOF STATUS.** UNDEFINED

**PROOF.** None: the objects are undefined.

**COUNTEREXAMPLE ATTEMPT.** n/a.

**NUMERICAL EDGE CASES.** n/a.

**MACHINE-TESTABLE INVARIANT.** n/a until defined (D-10 advisory meanwhile).

---

### OPEN-3 Required-Input Registry Completeness

**THEOREM ID.** OPEN-3

**STATEMENT.** The read-set of $\mathcal D$ (every field any $g_k$, $b_k$, gate or derivation reads) is contained in $\mathcal R^{\mathrm{req}}$ (F046).

**ASSUMPTIONS.** A specification of $\mathcal D$ at field level (R6).

**PROOF STATUS.** NOT YET PROVEN

**PROOF.** None (method RQ-18).

**COUNTEREXAMPLE ATTEMPT.** The defaulted-field example of T-04 shows what a gap causes; no gap is known in the current specification.

**NUMERICAL EDGE CASES.** n/a.

**MACHINE-TESTABLE INVARIANT.** Static and dynamic read-set instrumentation (R6).

---

### OPEN-4 Market-Wide Cost Perturbations of ΔJ

**THEOREM ID.** OPEN-4

**STATEMENT.** For concave non-decreasing $\mathcal U$, a market-wide cost increase (which also changes $J(a^{\varnothing})$) does not increase $\Delta J(a)$ (F025).

**ASSUMPTIONS.** T-08(b) without the restriction to the fills of $a$.

**PROOF STATUS.** NOT YET PROVEN

**PROOF.** None.

**COUNTEREXAMPLE ATTEMPT.** None found.

**NUMERICAL EDGE CASES.** n/a.

**MACHINE-TESTABLE INVARIANT.** Metamorphic test once $J$ is chosen (RQ-13).
