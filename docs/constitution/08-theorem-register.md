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
| T-06c | Per-epoch drawdown bound under trailing | PROOF REQUIRES ADDITIONAL ASSUMPTIONS | F139, F147 |
| T-07 | Liquidity monotonicity | PROOF REQUIRES ADDITIONAL ASSUMPTIONS | F064, F111, F146 |
| T-08 | Transaction-cost monotonicity | PROVED | F061–F063, F092 |
| T-09 | Uncertainty monotonicity of feasibility-defined caps | PROVED | F125 |
| T-09N | Argmax sizing monotone in ambiguity | DISPROVED | F017 |
| T-10 | Capital-floor preservation (one period, tiered) | PROOF REQUIRES ADDITIONAL ASSUMPTIONS | F072, F120–F122, F148, F150 |
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
| T-19 | Log-growth domain | PROOF REQUIRES ADDITIONAL ASSUMPTIONS | F019, F070, F148 |
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
| T-27 | Gate monotonicity in estimates | PROVED | F092, F111 |
| T-28 | Estimate dominance at every epoch (instantaneous and temporal) | PROVED | F146, F037, F069 |
| T-29 | Entry-fee booking conservation | PROVED | F148, F149 |
| T-30 | Entry-gate lifecycle monotonicity | PROVED | F092, F151 |
| T-31 | Estimator-validity fail-closed admission | PROVED | F092, F152 |
| OPEN-1 | Multi-step viability kernel | NOT YET PROVEN | F120, F122 |
| OPEN-2 | Certified-advantage validity | UNDEFINED | F027 |
| OPEN-3 | Required-input registry completeness | NOT YET PROVEN | F046 |
| OPEN-4 | Market-wide cost perturbations of $\Delta J$ | NOT YET PROVEN | F025 |

Counts: PROVED 27 · PROOF REQUIRES ADDITIONAL ASSUMPTIONS 8 · DISPROVED 11 · NOT YET PROVEN 4 · UNDEFINED 1 · total 51.

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

**Revision R4 (critical closure corrections).** An independent review of the closure commit `5c486f0` found Phase 0 NOT PASSED, with three
CRITICAL defects (registered in `docs/review/phase0/09-closure-review-registry.md`). CLOSURE-REV-001: G7 and G8 depended on estimates in the
wrong direction — G7 now uses the policy floor $\kappa^{\min}p^{\mathrm{stop}}_o$, G8 tests the mark against the stop; gate monotonicity is T-27; T-07 and
T-08 are restated to what holds. CLOSURE-REV-002: carried references stored past estimates — references now use the policy-floor valuation
$W^{\mathrm{R}}$ (F146), units are issued at $\nu^{\mathrm{R}}$, T-06c is restated with $\mathrm{DD}^{\mathrm{R}}$ (F147), and dominance across epochs is T-28.
CLOSURE-REV-003: fee booking — $\phi^{\mathrm{paid}}_o$ is what is booked in $W_t$, owed fees stay reserved until booked, including for terminal orders
(F148, F149, T-29); T-10 and T-19 are rebuilt with the booking semantics stated. CLOSURE-REV-004 … 016 remain open; T-10 lists 004–006 as open
dependencies.

**Revision R5 (held and filled quantities, CLOSURE-REV-006).** F144 and F145 used one symbol for the held quantity and the cumulative fill. The
quantities are now separate — held $q_{i,t}$ (S-032), fill $q^{\mathrm{fill}}_o$ (S-304), order $n'_o$ (S-308), unfilled remainder $q^{\mathrm{unf}}_o=n'_o-q^{\mathrm{fill}}_o$ (S-309);
F145 is rebuilt on the held quantity and the remainder with $\bar q_i=q_{i,t}+q^{\mathrm{unf}}_o$; F144's pending-portion terms use the remainder and the owed
fee is identified as a liability of the filled shares; F150 makes $0\le q_{i,t}\le q^{\mathrm{fill}}_o\le n'_o$ a validity condition ($\alpha_t=0$ and a fail-closed
charge otherwise). T-10's open dependency (iii) is closed; (i) CLOSURE-REV-004 and (ii) CLOSURE-REV-005 remain, and (iv) CLOSURE-REV-018 (one
non-terminal entry order per instrument) and (v) CLOSURE-REV-019 (exit fees booked after the cut), both found during this correction and not
corrected, are added; its status is unchanged. T-21 is updated
mechanically. No theorem is added; counts are unchanged.

**Revision R6 (entry-order lifecycle exclusivity, CLOSURE-REV-018).** G11 tested $Q^{\mathrm{res}}_{i,t}=0$, which a fully filled order awaiting its terminal
confirmation satisfies while it is still pending. The lifecycle state of an entry order is now explicit — `NON_TERMINAL` or `TERMINAL_CONFIRMED`,
$\bot$ when the evidence is missing, ambiguous or contradictory (F151, S-310, S-311) — and G11 also requires that no entry order on the
instrument is `NON_TERMINAL`; A-SCOPE-05 is restated as one entry-order authority per instrument. Terminal confirmation and fee finality stay
distinct: a terminal order's owed fee stays in the F144 reservation (CLOSURE-REV-003). T-30 (gate lifecycle monotonicity, PROVED) is added; T-10's
open dependency (iv) is closed, (i), (ii) and (v) remain, its status is unchanged. T-19's statement, proof and dependencies are unchanged; one
counterexample-attempt line records that the overlapping state had also made $\bar q_i$ in F070 ambiguous.

**Revision R7 (estimator failure semantics, CLOSURE-REV-008).** A-EXE-02 read a failed estimator check as the policy floor, the most
permissive admissible value ($666\to953$ sh). Each hard-layer estimate now has a status — `VALID`, `MISSING` or `INVALID` (F152) — and validation
precedes the policy bound; `MISSING` or `INVALID` gives $\alpha_t=0$. T-08 (a) and T-27 are stated over valid estimates only; the failure rule is the
separate authority-validity theorem T-31 (PROVED). T-28 is unchanged: carried references contain no estimate, so a failure cannot reach them.

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
($\kappa^{\min}p^{\mathrm{stop}}$, $\Gamma^{\min}$, $\Lambda^{\mathrm{floor}}$, $\mathrm{ADV}^{\max}$, the human-set cluster map); a missing or invalid estimate gives $\alpha_t=0$ (F152). (The former wording
"an arbitrarily optimistic estimate never increases $Q^{\mathrm{hard}}$" is false: $666$ vs $953$ sh, 06 §5.) The comparison holds at every epoch,
including through carried references (T-28), and each gate predicate is tested separately (T-27). Property-based and fuzz.

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
modifications or sales), $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t\le K_t$ holds, and every period satisfies the tier-S hypotheses of T-10, then the
reference drawdown satisfies $\mathrm{DD}^{\mathrm{R}}_t\le d^{\max}$ at every epoch (F147), and $\mathrm{DD}_t\le d^{\max}$ at every epoch that sets no new
reference high; at an epoch that does, $\mathrm{DD}_t=(\Lambda_t-\Lambda^{\mathrm{floor}}_t)/W^{\mathrm{R}}_t$, the estimate premium (G4 blocks new risk
if it reaches $d^{\max}$).

**ASSUMPTIONS.** All tier-S assumptions of T-10 (A-TRIG, A-FLOW-01, A-ACC-07, …) in every period; the pre-cut adjustment rule; $F^{\mathrm{dd}}\in F$;
the high-water mark is updated at epochs only, $H_{t+1}=\max(H_t,\nu^{\mathrm{R}}_{t+1})$ (F037 with F146; $\mathcal H_t$ = epoch marks; AUD-049).

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF.** T-10 with $n=0$ gives $W_{t+1}\ge F_t\ge F^{\mathrm{dd}}_t=(1-d^{\max})H_tU_t$; $U$ is constant ($X=0$) and $W^{\mathrm{R}}_{t+1}\ge W_{t+1}$
($\Lambda\ge\Lambda^{\mathrm{floor}}$, F111, F146), so $\nu^{\mathrm{R}}_{t+1}\ge\nu_{t+1}\ge(1-d^{\max})H_t$ (F139). If $\nu^{\mathrm{R}}_{t+1}\le H_t$ then $H_{t+1}=H_t$ and
$\mathrm{DD}^{\mathrm{R}}_{t+1}\le\mathrm{DD}_{t+1}\le d^{\max}$; otherwise $H_{t+1}=\nu^{\mathrm{R}}_{t+1}$, $\mathrm{DD}^{\mathrm{R}}_{t+1}=0$ and
$\mathrm{DD}_{t+1}=1-\nu_{t+1}/\nu^{\mathrm{R}}_{t+1}=(\Lambda_{t+1}-\Lambda^{\mathrm{floor}}_{t+1})/W^{\mathrm{R}}_{t+1}$ (F147). ∎

**COUNTEREXAMPLE ATTEMPT.** Trailing by stop modification alone can be infeasible (if $K_t/q_{i,t}<\kappa^{\mathrm{out}}$ the required stop lies above
the mark), so the authority must be able to sell; intra-period drawdown is not covered; the v0.1 form without the pre-cut rule was vacuous.
If $\mathcal H_t$ also contained intra-period highs the bound fails: $H_t=100$, intra-period peak $120$, $\nu_{t+1}=95\ge(1-0.1)H_t$ gives $\mathrm{DD}_{t+1}=20.8\%>10\%$
(third review, AUD-049). With the pre-closure unclamped charge a trailed stop gave $\mathrm{DD}_{t+1}=410/38{,}100>1\%=d^{\max}$ (AUD-039).
With references from estimate-inclusive $\nu_u$ (`5c486f0`) a past estimate lowered the floor itself (CLOSURE-REV-002, T-28). The
estimate-inclusive $\mathrm{DD}_t$ exceeds $d^{\max}$ at a new reference high exactly when the estimate premium exceeds $d^{\max}W^{\mathrm{R}}_t$ — a
conservative outcome (G4 blocks), not a floor breach.

**NUMERICAL EDGE CASES.** $W_{t+1}=F_t$ gives $\mathrm{DD}_{t+1}=d^{\max}$ exactly — then T-06a blocks new risk.

**MACHINE-TESTABLE INVARIANT.** Monte Carlo on paths inside the tier-S set with the pre-cut rule ⇒ $\mathrm{DD}^{\mathrm{R}}\le d^{\max}$ at epochs, and
$\mathrm{DD}\le d^{\max}$ at epochs without a new reference high; paths outside
are logged as assumption violations.

---

### T-07 Liquidity Monotonicity

**THEOREM ID.** T-07

**STATEMENT (restated at the critical closure correction, CLOSURE-REV-001).** Holding the authoritative history and every other input fixed:
(a) $Q^{\mathrm{hard}}_t$ is non-decreasing in the estimated ADV of any instrument. (b) For an opportunity whose limit satisfies G7's price clause
$p^{\mathrm{lim}}\le p^{\mathrm{ask}}(1+\chi)$ at the narrower spread, the policy-bound envelope $\bar Q^{\mathrm{hard}}_t$ (S-307) is non-increasing in the spread of
any instrument at a fixed mid. (c) Under the hypotheses of (b), $Q^{\mathrm{hard}}_t$ itself is non-increasing in that spread if the estimates
$\hat\kappa^{\mathrm{out}},\hat\Lambda$ are non-decreasing in spread and, at an epoch whose own reference value sets $H_t$, $\nu^{\mathrm{day}}_0$ or $\nu^{\mathrm{wk}}_0$, the
estimate premium $\hat\Lambda_{i,t}-\Lambda^{\mathrm{floor}}_{i,t}$ is non-decreasing in spread. The v0.2 form ("$Q^{\mathrm{hard}}$ non-decreasing in ADV and
non-increasing in spread") is false; see below.

**ASSUMPTIONS.** A-MATH-01; A-EXE-02 for (a) and (c) ($\hat\kappa^{\mathrm{out}}$, $\hat\Lambda$ non-increasing in ADV, non-decreasing in spread); F111 (policy
bounds, $\mathrm{ADV}=\min(\mathrm{ADV}^{\mathrm{est}},\mathrm{ADV}^{\max})$); F146 (estimate-free references); OC-1 (open risk without $\Lambda$ credit, F064); G7 in its
closure form; G5; for (b) the price-clause hypothesis; for (c) the premium condition.

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF.** (a) A larger estimated ADV lowers $\hat\kappa^{\mathrm{out}}$ and $\hat\Lambda$ (A-EXE-02), hence $\kappa^{\mathrm{out}}$ and $\Lambda$ (F111: the maximum of a fixed
floor and a non-increasing estimate is non-increasing), and raises $\mathrm{ADV}=\min(\mathrm{ADV}^{\mathrm{est}},\mathrm{ADV}^{\max})$. Lower $\Lambda$ raises $W_t$; the
floors use references built from $W^{\mathrm{R}}$ (F146), which contain no estimate, so $K_t$ and every base rise; lower $\kappa^{\mathrm{out}}$ lowers every
consumption and open-risk charge; the H12–H13 budgets rise. G3 and G4 can only pass more easily; G7 and G8 do not depend on ADV (T-27).
Feasible sets are nested and $\min$ preserves order.
(b) Under the policy bounds, $\kappa^{\mathrm{out}}=\kappa^{\min}p^{\mathrm{stop}}$, $\Gamma=\Gamma^{\min}$ and $\mathrm{ADV}=\mathrm{ADV}^{\max}$ do not depend on spread, while
$\Lambda=\Lambda^{\mathrm{floor}}=q\varsigma/2+\phi^{\mathrm{sell}}(q)$ rises with it, so $W_t=W^{\mathrm{R}}_t$ falls. Each floor is $F^{\mathrm{abs}}$, or $c\max(a,W^{\mathrm{R}}_t)$ with
$c\in\{1-d^{\max},1-\ell^{\mathrm{day}},1-\ell^{\mathrm{wk}}\}$ and $a$ an earlier reference times $U_t$ (a reference set at this epoch is $W^{\mathrm{R}}_t$), or
$F^{\mathrm{lock}}$ with $\eta^{\mathrm{lock}}<1$; each $W^{\mathrm{R}}_t-F_j$ equals $\min(W^{\mathrm{R}}_t-ca,(1-c)W^{\mathrm{R}}_t)$ (or has slope $\ge1-\eta^{\mathrm{lock}}>0$ for the lock) and is
non-decreasing in $W^{\mathrm{R}}_t$, so $K_t=\min_j(W^{\mathrm{R}}_t-F_j)$ and every base fall. Open risks use the mark and no $\Lambda$ credit (OC-1);
consumptions use $p^{\mathrm{lim}}$; G5 can only fail more; G7's cost clause uses $\kappa^{\min}$ and its price clause holds at both spreads by hypothesis;
G8 uses the mark. Hence the envelope does not increase.
(c) With estimates, $\Lambda=\max(\Lambda^{\mathrm{floor}},\hat\Lambda)$ rises by at least the rise of $\Lambda^{\mathrm{floor}}$ when the premium is non-decreasing, so
$W_t$ falls at least as much as $W^{\mathrm{R}}_t$, while each floor falls by at most $c<1$ times the fall of $W^{\mathrm{R}}_t$: $K_t$ does not rise. The
consumptions and charges rise with $\hat\kappa^{\mathrm{out}}$ (A-EXE-02). ∎

**COUNTEREXAMPLE ATTEMPT.** The v0.1 form with $\Lambda$ credit in open risk (review, re-verified exactly): hold $1{,}000$ sh at $50$, stop $45$,
$\kappa^{\mathrm{out}}=0.05$, cash $200{,}000$, $B=W$, $f^{\mathrm{trd}}=f^{\mathrm{port}}=2\%$, new order consumption $5.05n$. Low ADV ($\Lambda=500$): $W=249{,}500$,
credited open risk $4{,}550$, H2 budget $440$, $Q=87$. High ADV ($\Lambda=100$): $W=249{,}900$, credited open risk $4{,}950$, budget $48$, $Q=9$. Worse
liquidity, larger cap. Under OC-1 both budgets are $\le0$ and $Q=0$ (monotone). The v0.2 statement is false (CLOSURE-REV-001 and the critical
re-audit): (i) with G7 on $\kappa^{\mathrm{out}}$ (`5c486f0`) a wider spread raises $\hat\kappa^{\mathrm{out}}$ and lets G7 pass (spread $0.0998$: fails; $0.30$: passes,
$Q^{\mathrm{hard}}>0$) — removed by the closure G7; (ii) G7's price clause: mid $50$, $\chi=0.001$, limit $50.08$: at spread $0.02$ ($p^{\mathrm{ask}}=50.01$) it
fails, at spread $0.20$ ($p^{\mathrm{ask}}=50.10$) it passes — an observation, not a cost, hence the hypothesis of (b); (iii) at an epoch that sets the
reference, $E_t=150{,}000$, $U=1$, $d^{\max}=10\%$, $\hat\Lambda=500$ binding and fixed while $\Lambda^{\mathrm{floor}}$ rises $100\to200\to400$ with the spread:
$K_t=14{,}590\to14{,}680\to14{,}860$ while the envelope's cushion falls $14{,}990\to14{,}980\to14{,}960$ — hence the premium condition of (c); $K_t$ stays
below the envelope throughout (T-28). Other failures: fitted impact models non-monotone in ADV; displayed depth used as a cap (inadmissible).

**NUMERICAL EDGE CASES.** $\mathrm{ADV}\to0$ (A-MKT-06 ⇒ $\alpha_t=0$); $\sqrt{\ }$ in impact models only with certified upper bounds (01 §9 item 4).

**MACHINE-TESTABLE INVARIANT.** Metamorphic: estimated ADV ↑ ⇒ $Q^{\mathrm{hard}}$ not ↓; spread ↑ at a fixed mid ⇒ $\bar Q^{\mathrm{hard}}$ not ↑ for
opportunities passing G7's price clause at both spreads — for the opportunity's instrument and for held instruments; A-EXE-02 and the premium
condition checked on a grid at model load.

---

### T-08 Transaction-Cost Monotonicity

**THEOREM ID.** T-08

**STATEMENT (restated at the critical closure correction, CLOSURE-REV-001).** (a) If $\hat\kappa^{\mathrm{out}\prime}\ge\hat\kappa^{\mathrm{out}}$ pointwise in
quantity, both `VALID` (F152) and bounded by F111, and the policy floor $\kappa^{\min}$ unchanged, then $Q^{\mathrm{hard}\prime}\le Q^{\mathrm{hard}}$. (a′) If $\phi'\ge\phi$
pointwise (buy, sell and price-$0$ schedules) and every fee-state and load check passes under $\phi$ ($\alpha_t=1$), then the policy-bound envelope
satisfies $\bar Q^{\mathrm{hard}\prime}\le\bar Q^{\mathrm{hard}}$ (S-307). (b) If moreover $J(a)=\mathbb E[\mathcal U(W_{t+1}(a))]$ with $\mathcal U$ non-decreasing and the
perturbation affects only the fills generated by $a$, then $\Delta J'(a)\le\Delta J(a)$.

**ASSUMPTIONS.** A-MATH-01; the hypotheses in the statement; gates in their closure form (T-27); references by F146; estimates `VALID` (F152) —
the theorem is proved over the valid domain only.

**PROOF STATUS.** PROVED

**PROOF.** (a) $\hat\kappa^{\mathrm{out}}$ enters only $\kappa^{\mathrm{out}}=\max(\kappa^{\min}p^{\mathrm{stop}},\hat\kappa^{\mathrm{out}})$ (F111), which rises pointwise. $\kappa^{\mathrm{out}}$
appears in the consumptions $L^{\mathrm{stop}},L^{\mathrm{gap}}$ (through $p^{\mathrm{gx}}$, F060) and in the charges F064, F065, F144, F145 — each non-decreasing in
it, the clamp $(\cdot)^+$ included — and in no base, cushion, reference, cash term or gate (G7 uses $\kappa^{\min}$, G8 the mark; T-27). Budgets fall,
consumptions rise, feasible sets shrink. The domain of (a) is the set of `VALID` estimates: the policy floor bounds a valid value (F152); a
missing or invalid estimate is not a point of this domain and is not compared — it gives $\alpha_t=0$ (T-31). (a′) Under the policy bounds $\Lambda=\Lambda^{\mathrm{floor}}=q\varsigma/2+\phi^{\mathrm{sell}}(q)$ rises with the sell schedule,
so $W^{\mathrm{R}}_t$ falls and, as in T-07 (b), $K_t$ and every base fall; consumptions, open-risk charges (through $\phi^{\mathrm{split}}$), $C^{\mathrm{res}}$ and the
H14 consumption rise; $\phi^{\mathrm{acc}}_o$ rises, so a fee state valid under $\phi$ stays valid; G7 and G8 contain no fee. (b) $W_{t+1}(a^{\varnothing})$ is
unchanged and $W_{t+1}(a)$ decreases pointwise (costs enter F055 negatively); $\mathcal U$ is non-decreasing. ∎

**COUNTEREXAMPLE ATTEMPT.** The v0.2 statement ("$\phi'\ge\phi$ and $\kappa^{\mathrm{out}\prime}\ge\kappa^{\mathrm{out}}$ pointwise ⇒ $Q^{\mathrm{hard}\prime}\le Q^{\mathrm{hard}}$", PROVED at
`5c486f0`) is false (CLOSURE-REV-001): G7 on $\kappa^{\mathrm{out}}$ failed at the floor and passed at $\hat\kappa^{\mathrm{out}}=0.1$ ($Q=0$ vs $9{,}090$); G8 as a
sign test of F064 turned $-3.1$ (\$1 minimum fee, ANOMALY) into $+4.9$ (\$5 minimum) and re-opened trading. The closure gates remove both. Not
claimed, with counterexamples: (i) $Q^{\mathrm{hard}}$ with estimates in the fee schedule, at an epoch that sets a reference while $\hat\Lambda$ binds and
is held fixed: $K_t=d^{\max}E_t-\hat\Lambda_t+(1-d^{\max})\Lambda^{\mathrm{floor}}_t$ rises with $\phi^{\mathrm{sell}}$ ($E_t=150{,}000$, $\hat\Lambda=500$, $\Lambda^{\mathrm{floor}}$ $100\to200$:
$14{,}590\to14{,}680$); it holds when $\hat\Lambda$ carries the schedule's exit fee one for one (composition F035), and $Q^{\mathrm{hard}}\le\bar Q^{\mathrm{hard}}$ always
(T-28); (ii) a schedule raised so that a previously invalid $\phi^{\mathrm{paid}}_o$ becomes valid ($\phi^{\mathrm{paid}}_o=2$ with $q^{\mathrm{fill}}_o=2$: invalid under a \$1
minimum, valid under \$2) moves $\alpha_t$ from $0$ to $1$ — excluded by the hypothesis $\alpha_t=1$ under $\phi$; (iii) raising the policy floor $\kappa^{\min}$
itself can let G7 pass — a human policy change (Art. 16), not an estimate, excluded by the hypothesis of (a); (iv) at `a87b887` A-EXE-02 read a
failed grid check as the policy floor and so compared a failed estimator with a valid one: H1 with $f^{\mathrm{trd}}B=1{,}000$, limit $50$, stop $49$,
$\kappa^{\min}=0.001$: valid $\hat\kappa^{\mathrm{out}}=0.5$ gives $666$ sh, the failed check $953$ (CLOSURE-REV-008) — outside (a), now $\alpha_t=0$ (T-31). Market-wide perturbations (which
also change $J(a^{\varnothing})$) are OPEN-4.

**NUMERICAL EDGE CASES.** Fee quantisation upward (01 §9 item 15) preserves (a) and (a′).

**MACHINE-TESTABLE INVARIANT.** Metamorphic: $\hat\kappa^{\mathrm{out}}$ scaled up ⇒ $Q^{\mathrm{hard}}$ not up; fee schedule up ⇒ $\bar Q^{\mathrm{hard}}$ not up; each gate
tested separately (T-27).

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

**ASSUMPTIONS.** Tier S: A-MATH-01; A-SCOPE-03; A-SCOPE-05 with G11 (corrected: at most one `NON_TERMINAL` entry order per instrument and a valid
lifecycle state, F151); A-FLOW-01 ($X_{t+1}=0$); A-ACC-01, A-ACC-02, A-ACC-03 (transition
F055, fee postings included in $\mathcal J_{t+1}$, 05 §1); A-ACC-07 ($\mathrm{Fin}=\mathrm{Accr}=0$, $\mathrm{Inc}\ge0$); A-ACC-04; A-ACC-06 ($\Lambda\ge0$); A-MKT-05
(every entry fill $\le p^{\mathrm{lim}}$); A-EXE-01, A-EXE-02; A-EXE-03 (cumulative fill $\le$ order quantity); **A-EXE-04 with the booking semantics of
F148**: the entry fees of one order over its lifetime are at most $\phi^{\mathrm{buy}}$ of its cumulative filled quantity and may be booked into $W$ at the
fill, later, or after the order is terminal. T-10 does **not** assume fill-time booking; it requires that every entry order whose fees are not final
is in the order state with $\phi^{\mathrm{paid}}_o$ equal to the fees booked into $W_t$ at the cut and $0\le\phi^{\mathrm{paid}}_o\le\phi^{\mathrm{acc}}_o$ (F148), so that
owed-but-unbooked fees stay reserved (F144, F145) until they are booked (T-29). A-EXE-05 (no other orders); A-AUTH-02 (complete order state:
quantity, limit, current stop, cumulative fill, fees booked, fee-final confirmation); A-AUTH-04 (one cut); **A-TRIG** (position-level exit-value
bound F072 at the $\tau_t$ inputs); charges F064–F066 (held positions; no entry-fee term), F144 (pending orders and the owed fees of terminal
orders) and F145 (partially filled orders), all at the $\tau_t$ inputs (REV-028, AUD-034, CLOSURE-REV-003); hard-layer inputs by F111; F140 in
place of $\phi^{\mathrm{sell}}$ throughout; per-share distances of pending orders clamped at $0$ (AUD-039); exposures without an authoritative stop by
case (1′) (D-06, A-MKT-01, A-ACC-05; AUD-042). **Open dependencies (not resolved by the critical correction):** (i) A-TRIG is assumed for every
exposure, including one whose exit order is partially executed at $\tau_t$, where the sufficient conditions listed in 04 A-TRIG do not imply it
(exit-fee catch-up, CLOSURE-REV-004); (ii) each exposure has one live stop $p^{\mathrm{stop}}_i$ protecting all of its held and future quantity
(CLOSURE-REV-005; F145 remains conditional on it). **Quantity state (CLOSURE-REV-006, resolved; no longer an open dependency):** every pending
entry order satisfies F150 — held $q_{i,t}$, cumulative fill $q^{\mathrm{fill}}_o$ and order quantity $n'_o$ present, on the lattice, $0\le q_{i,t}\le q^{\mathrm{fill}}_o\le n'_o$;
exits while the entry is pending are covered by case (2′); an invalid state has $\alpha_t=0$ and the F150 charge, for which T-10 claims only the
dominance of (viii). **Open dependency registered at that correction:** (v) every exit fee of an exit executed before $\tau_t$ is booked into $W_t$
at the cut — no exit-side owed-fee reservation exists (CLOSURE-REV-019, OPEN). **Entry-order exclusivity (CLOSURE-REV-018, resolved; former open
dependency (iv)):** G11 admits a new entry order on $i$ only if no entry order on $i$ is `NON_TERMINAL` (F151), so a fully filled order awaiting
its terminal confirmation keeps the instrument's single pending slot; a snapshot with two `NON_TERMINAL` entry orders on one instrument, or a
lifecycle state $\bot$, has $\alpha_t=0$ and no finite charge for that instrument (RECOVERY) and is outside these hypotheses (ix).
Tier G: A-GAP (tier-G form of F072) instead of A-TRIG. Tier U: A-MKT-01 and A-ACC-05 (tier-U form of F072) instead of A-TRIG.

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF (tier S; rebuilt at the critical closure correction).** *Accounting.* By A-ACC-01…04 and G11, $W_{t+1}-W_t=\sum_i\Delta_i+\mathrm{Inc}_{t+1}$,
where $\Delta_i$ collects the fills and fee postings of the period attributable to exposure $i$ and the change of its liquidation value (F055 with
$X=\mathrm{Fin}=\mathrm{Accr}=0$). *Fees.* For an entry order $o$ the fee postings in $(\tau_t,\tau_{t+1}]$ are at most $\phi^{\mathrm{buy}}_o$ of its cumulative fill at
$\tau_{t+1}$ minus $\phi^{\mathrm{paid}}_o$ (A-EXE-04 on lifetime fees; F148: $\phi^{\mathrm{paid}}_o$ is exactly what $W_t$ already contains) — the fees of the period's
fills plus $\phi^{\mathrm{owed}}_o$; for an order without fills in the period, at most $\phi^{\mathrm{owed}}_o$.
(1) *Held exposure with a live stop and no pending entry order:* it contributed $q_{i,t}m_{i,t}-\Lambda_{i,t}$ before the period and contributes
$\mathrm{XV}_{i,t+1}$ (exit proceeds net of all exit fees plus liquidation value of any remainder) after it; by A-TRIG this part of $\Delta_i$ is
$\ge q_{i,t}\big(p^{\mathrm{stop}}_i-\kappa^{\mathrm{out}}_i(q_{i,t})\big)-\phi^{\mathrm{split}}_i(q_{i,t})-q_{i,t}m_{i,t}+\Lambda_{i,t}=-r^{\mathrm{open}}_i+\Lambda_{i,t}$ (F064, A-ACC-06).
(1′) *Held exposure without an authoritative stop* (D-06): by A-MKT-01 and A-ACC-05, $\mathrm{XV}_{i,t+1}\ge-\phi^{\mathrm{split}}_{i,0}(q_{i,t})$, so this part is
$\ge-u^{\mathrm{open}}_i+\Lambda_{i,t}$ (F066 with F140); a partially filled order whose stop is missing is charged $u^{\mathrm{pf}}_i$ in the same way.
(1″) *Owed fee of a terminal entry order* $o$ on any instrument, held or not (CLOSURE-REV-003): no fill can occur, so its fee postings in the period
are at most $\phi^{\mathrm{owed}}_o$, which is exactly its F144 owed-fee reservation; this part of $\Delta_i$ is $\ge-\phi^{\mathrm{owed}}_o$.
(2) *New order, or pending order without fills* (G11): cumulative fill $e\le n'$ (A-EXE-03) at prices $\le p'^{\mathrm{lim}}$ (A-MKT-05), fee postings
$\le\phi^{\mathrm{buy}}(e)$ ($\phi^{\mathrm{paid}}_o=0$), and by A-TRIG with $q^{\mathrm{exp}}_i=e$, $\mathrm{XV}_{i,t+1}\ge e(p^{\mathrm{stop}}-\kappa^{\mathrm{out}}(e))-\phi^{\mathrm{split}}(e)$. With
$x=p'^{\mathrm{lim}}-p^{\mathrm{stop}}+\kappa^{\mathrm{out}}(n')$ of either sign (the current stop may have been trailed to or above the limit after G7 checked it),
$e\,x\le n'x^+$ for $0\le e\le n'$, and monotonicity (A-EXE-01, A-EXE-02, F140) gives $\Delta_i\ge-\big[n'x^++\phi^{\mathrm{split}}(n')+\phi^{\mathrm{buy}}(n')\big]$ — the F144
charge ($r^{\mathrm{pf}}$ with $q=0$); for the new order $x>0$ by G7 and the bound is $L^{\mathrm{stop}}(n)$ (F061 with F140). A value computed with older
inputs is not enough (REV-028); without the clamp the charge can be negative (stop $51$, limit $50$, $\kappa^{\mathrm{out}}=0.1$, \$1 minimum fees, $n'=100$:
$-87$ against a worst loss of $1.2$; AUD-039). Unfilled orders give $\Delta_i=0$.
(2′) *Order partially filled before* $\tau_t$ (AUD-033, AUD-034; quantities CLOSURE-REV-006): pending order $o$ of total $n'_o$ with cumulative fill
$q^{\mathrm{fill}}_o>0$, held $q_{i,t}$ with $0\le q_{i,t}\le q^{\mathrm{fill}}_o\le n'_o$ (F150; $q^{\mathrm{fill}}_o-q_{i,t}$ shares exited before $\tau_t$, their proceeds in $W_t$), unfilled
remainder $q^{\mathrm{unf}}_o=n'_o-q^{\mathrm{fill}}_o\ge0$, $\phi^{\mathrm{paid}}_o$ booked — one exposure (G11), charged $r^{\mathrm{pf}}_i$ (F145) in $R^{\mathrm{res}}_t$ and nothing in
$R^{\mathrm{open}}_t$. With $e\le q^{\mathrm{unf}}_o$ [sh$_i$] filled in the period at prices $\le p'^{\mathrm{lim}}$, the fee postings are at most
$\phi^{\mathrm{buy}}(q^{\mathrm{fill}}_o+e)-\phi^{\mathrm{paid}}_o\le\phi^{\mathrm{buy}}(n'_o)-\phi^{\mathrm{paid}}_o$ [USD], which covers the owed fee of every filled share, held or exited, and the
fees of future fills (F148). The exposure is $q^{\mathrm{exp}}_i=q_{i,t}+e\le\bar q_i=q_{i,t}+q^{\mathrm{unf}}_o$ [sh$_i$]; A-TRIG, $\kappa^{\mathrm{out}}_i(q^{\mathrm{exp}}_i)\le\kappa^{\mathrm{out}}_i(\bar q_i)$
[USD/sh$_i$], $\phi^{\mathrm{split}}(q^{\mathrm{exp}}_i)\le\phi^{\mathrm{split}}(\bar q_i)$ [USD] and $e\,x\le q^{\mathrm{unf}}_ox^+$ [USD] for $x=p'^{\mathrm{lim}}-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(\bar q_i)$
[USD/sh$_i$] of either sign give
$\Delta_i\ge-\big[q_{i,t}(m_{i,t}-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(\bar q_i))+q^{\mathrm{unf}}_ox^++\phi^{\mathrm{split}}(\bar q_i)+\phi^{\mathrm{buy}}(n'_o)-\phi^{\mathrm{paid}}_o\big]+\Lambda_{i,t}=-r^{\mathrm{pf}}_i+\Lambda_{i,t}$.
The filled quantity's entry price, the exited shares' proceeds and the booked fees are in $W_t$ and are not charged again; an exited share is in
neither quantity term, and only $q^{\mathrm{unf}}_o\ge0$ (from $q^{\mathrm{fill}}_o\le n'_o$) and $q_{i,t}\ge0$ are used — $q_{i,t}\le q^{\mathrm{fill}}_o$ is the consistency check of
G11 and A-AUTH-02. Reading the held term with the fill under-charges after a partial exit (CLOSURE-REV-006: $99$ against a worst loss of $100.2$).
Charging only the remainder under-charges
($\kappa^{\mathrm{out}}(n)=0.001n$, no fees, $n'=200$, $q_{i,t}=100$ marked at $52$, limit $50$, stop $49$: worst loss $440-\Lambda_{i,t}>r^{\mathrm{open}}_i+L^{\mathrm{stop}}(100)=420$
whenever $\Lambda_{i,t}<20$); charging open risk plus the full-order reservation charges realised costs twice (05 §5: $5.24$).
(3) Each exposure, each pending order and each owed fee is charged exactly once (an owed fee of a pending order inside F145, of a terminal order
only in F144; F064–F066 carry no entry fee; T-29); each filled share is held (held term) or exited (in $W_t$), each unfilled share is in the
remainder term only (CLOSURE-REV-006). Summing with $\mathrm{Inc}\ge0$ and $\Lambda_t=\sum_i\Lambda_{i,t}$:
$W_{t+1}\ge W_t-(R^{\mathrm{open}}_t-\Lambda_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n))\ge W_t-K_t=F_t$.
Tiers G and U: identical with the tier's form of F072 and the same fee terms (the owed-fee reservation is part of $G^{\mathrm{res}}_t$ and $Z^{\mathrm{res}}_t$). ∎

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
(vii) Fee booking (CLOSURE-REV-003, at `5c486f0`): a terminal order's owed fee was charged nowhere — $100$ sh, buy fee $\max(1,0.005k)$, sell fee
$0$, spread $0.01$: $W_{t+1}=F_t-\tfrac12$; $40$ sh, buy fee minimum $5$, sell fee minimum $1$, spread $0.02$: $W_{t+1}=F_t-3.6$; and a fee reported but
not booked was counted as paid: $W_{t+1}=F_t-4.75$. With F148 the same states give $F_t+\tfrac12$, $F_t+1.4$ and $F_t+\tfrac14$. Exact enumeration of
fee timing (bookings at the fill, within the period, or after the order is terminal; $\phi^{\mathrm{paid}}_o\in\{0,\phi^{\mathrm{acc}}_o/2,\phi^{\mathrm{acc}}_o\}$; three buy and two
sell schedules; $1{,}788$ states): $480$ understatements with the `5c486f0` charges, $0$ with F148.
(viii) Quantity semantics (CLOSURE-REV-006, at `80ca693`, where F144 read $q$ as the fill and F145 as the holding): after a partial exit while the
entry is pending ($n'=200$, $100$ filled, $40$ held, mark $48.95$, stop $49$, limit $50$, $\kappa^{\mathrm{out}}=0.01$, fee $\max(1,0.005k)$, $N^{\mathrm{ex}}=1$,
$\phi^{\mathrm{paid}}_o=1$, spread $0.01$, $\Lambda_{i,t}=1.2$) the fill reading charged $99$ against a worst loss of $100.2$ ($W_{t+1}=F_t-6/5$) and the holding reading
$162$; with $q_{i,t}=150>n'=100$ (mark $50$ above stop $49$, per-share distance $1.1$) the price terms were $110$ against $165$. Rebuilt: $101.4$ (exact),
and $\alpha_t=0$ with the F150 charge $12{,}500$. Exhaustive exact enumeration of every valid $(n',q^{\mathrm{fill}}_o,q_{i,t})$ with $n'\le6$ ($83$ quantity
states; five marks from $48.95$ to $52$, six stops from $48$ to $51$ around the limit $50$, five $\kappa^{\mathrm{out}}$ schedules including one above the
stop price, five fee schedules including a percentage fee, $N^{\mathrm{ex}}=1,2$, three booking levels, tiers S, G, U; $927{,}900$ checks):
no understatement and no $W_{t+1}<F_t$, equality in all $859{,}900$ clamp-inactive checks; the fill reading understated in $106{,}128$.
Randomised exact search ($35{,}000$ trials, $n'\le150$, categories partial entry fill, partial exit, $q_{i,t}<q^{\mathrm{fill}}_o$, $q^{\mathrm{fill}}_o=n'$, $q_{i,t}=0$
after fills, remainder $>0$, full fill then reduced holding): no $W_{t+1}<F_t$ (fill reading: $53$). Invalid states ($q_{i,t}<0$,
$q^{\mathrm{fill}}_o<0$, $n'\le0$, $q_{i,t}>q^{\mathrm{fill}}_o$, $q^{\mathrm{fill}}_o>n'$, $q_{i,t}>n'$, missing, off the lattice; $1{,}212$ states, $329$ with a finite
charge): $\alpha_t=0$ in every one; the F150 charge is at least the same tier's F145 charge of every valid reading $q_{i,t}\le q^{\mathrm{fill}}\le n'$, the visible
holding's own charges and the reported fill's fee ($3{,}981{,}600$ checks, none violated; the tier-U component alone: $10{,}056$ violations).
Dominance: for a valid reading, $\bar q_i\le q_{i,t}+n'$, the remainder is $\le n'$ and $\phi^{\mathrm{buy}}(n')-\phi^{\mathrm{paid}}_o\le\phi^{\mathrm{buy}}(\max(q_{i,t},q^{\mathrm{fill}}_o)+n')$, and
every term of F145 is monotone in these ($\kappa^{\mathrm{out}}$, $\phi$ non-decreasing, $p^{\mathrm{gx}}$ non-increasing).
(ix) Entry-order exclusivity (CLOSURE-REV-018, at `8dbb0ee`, where G11 tested $q_{i,t}=0$ and $Q^{\mathrm{res}}_{i,t}=0$ only): $o_1$ for $100$ fully filled,
`NON_TERMINAL`, entry fee $\max(1,0.005k)=1$ owed, nothing held, so $Q^{\mathrm{res}}_{i,t}=q^{\mathrm{unf}}_{o_1}=0$ and G11 admitted $o_2$ for $100$; $o_2$ filled
(fee $1$ booked), $100$ held, mark $52$, stop $49$, limit $50$, $\kappa^{\mathrm{out}}=0.01$, sell fee $0$, spread $0.01$ ($\Lambda_{i,t}=1/2$): one F145 for $i$
(with $o_2$) charged $301$ against a worst loss of $603/2$, $W_{t+1}=F_t-\tfrac12$. With G11 corrected, $o_2$ is not admitted and $o_1$'s F145 ($1$, its owed
fee) stands until $o_1$ is `TERMINAL_CONFIRMED`; then $o_1$'s owed fee is the F144 terminal reservation, $o_2$ may be admitted, and the charge is
$302=301+1$ against $603/2$ (exact). Lifecycle enumeration ($q^{\mathrm{unf}}_{o_1}$, terminal confirmation, owed fee and holding each zero or not;
$0$, $1$ or $2$ non-terminal entry orders on $i$; consistent, missing or contradictory evidence: $144$ states): the corrected gate admits a new entry
in $4$ states, none with a non-terminal entry order and none with an invalid lifecycle ($120$ invalid states, all $\alpha_t=0$), against $54$, $36$
and $44$ for the old gate; no admitted state leaves an owed fee outside every charge (old: $9$); exact two-order checks after admission ($96$
corrected, $144$ old): no $W_{t+1}<F_t$, against $16$ (down to $W_{t+1}=F_t-1$).

**NUMERICAL EDGE CASES.** Equality in the premise (floor attained, not breached); aggregates rounded up and $K_t$ rounded down (T-24); fees
quantised up (01 §9 item 15); $e=0$; a stop exactly at the limit ($x=\kappa^{\mathrm{out}}(n')>0$, clamp inactive); $-0$ rejected at the boundary;
$\phi^{\mathrm{paid}}_o=\phi^{\mathrm{acc}}_o$ (nothing owed); $\phi^{\mathrm{paid}}_o>\phi^{\mathrm{acc}}_o$ ⇒ $\alpha_t=0$, no credit (F148); $q_{i,t}=0<q^{\mathrm{fill}}_o$ (every filled
share exited: remainder and owed fees only); $q^{\mathrm{fill}}_o=n'_o$ before the terminal confirmation ($q^{\mathrm{unf}}_o=0$); a quantity state outside F150 ⇒
$\alpha_t=0$ and the F150 charge; a fully filled `NON_TERMINAL` entry order ($q^{\mathrm{unf}}_o=0$, still pending: G11 blocks a new entry on $i$);
terminal confirmation and fee finality in different epochs.

**MACHINE-TESTABLE INVARIANT.** Simulator with adversarial paths drawn inside the tier's disturbance set (comonotone all-stops scenario,
triggered-unfilled states, split fills, partial exits at the cut) ⇒ $W_{t+1}\ge F_t$; F072 checked per exposure ex post; each T-10N
counterexample is a regression test that must fail when its hypothesis is removed; fee-timing property test (random fills, bookings at the
fill, later or after the terminal state, fee-final events: each fee dollar in $W_t$ or in exactly one charge, T-29, and $W_{t+1}\ge F_t$); quantity-state
property test (random fills, partial exits and corrections: F150 at every cut, no exited share in a quantity term, $Q^{\mathrm{res}}$ unchanged by exits); paths
outside are logged as assumption violations with breach magnitude.

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
with $\mathrm{Fin}=0$, $\mathrm{Inc}\ge0$ and $\mathrm{Accr}_{t+1}\le\bar A_{t+1}$ (S-185) in place of $\mathrm{Accr}=0$; A-MKT-01; A-ACC-05 (tier-U form of F072 with F140);
A-EXE-04 with the booking semantics of F148 (owed entry fees of terminal orders in $C^{\mathrm{res}}_t$); $W_t>0$. Open dependency: A-ACC-05 is assumed
also for an exposure whose exit order is partially executed at $\tau_t$, whose cumulative exit fee is not modelled (CLOSURE-REV-004); every exit fee of
an exit executed before $\tau_t$ is booked at the cut (CLOSURE-REV-019).

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF.** Tier-U bound: every position worthless, each exposure's exit fees at most $\phi^{\mathrm{split}}_{i,0}(\bar q_i)$ (A-ACC-05, F140, monotone), pending orders filled
at their limits with at most their remaining fees and the new order at $L^{\mathrm{abs}}(n)$; entry-fee postings of the period are at most
$\phi^{\mathrm{buy}}(n')-\phi^{\mathrm{paid}}_o$ for a pending order and $\phi^{\mathrm{owed}}_o$ for a terminal one, both inside $C^{\mathrm{res}}_t$ (F144, F148); realised and
booked costs are already in $C_t$ (AUD-038); monotonicity of
$\log$. The ball contains the mixture of $\hat{\mathbb P}$ (weight $1-\epsilon^{\mathrm{mix}}$) with a point mass at a scenario $\xi_0$ in which every price is
$0$, at finite transport cost for small $\epsilon^{\mathrm{mix}}$. ∎

**COUNTEREXAMPLE ATTEMPT.** The pre-review $W^{\min}$ without a flow term: $W_t=100$ cash only, $X=-100$ ⇒ $W_{t+1}=0$ while the old bound was $100$
(REV-012). With per-order minimum fees and a holding sold in part at price $0$ (fee $1$) while the remainder is valued with its own fee
($\Lambda=1$), $W_{t+1}=W^{\min}_{t+1}-1$ unless F070 uses $\phi^{\mathrm{split}}$ (REV-034). Without the common hypotheses (third review, AUD-043): $C=1{,}000$,
pending $10$ @ $10$, $W^{\min}=900$; a fill at $12$ above the limit (A-MKT-05 fails) then prices → $0$ gives $880<900$; a manual buy of $90$ @ $10$
(A-EXE-05 fails) gives $W_{t+1}=0$ and an undefined logarithm. Owed fee of a terminal order (CLOSURE-REV-003, `5c486f0`): cash $1{,}000$,
$10$ sh held, exit fee $\max(1,0.005k)$ per order in two parts at price $0$, owed entry fee $1$: bound $W^{\min}=998$ against $W_{t+1}=997$; with F148
$W^{\min}=997=W_{t+1}$. Exact fee-timing enumeration ($168$ states, prices $\to0$, bookings at the fill, later or after the terminal state): $56$
violations at `5c486f0`, $0$ with F148. Two pending entry orders on one instrument (the CLOSURE-REV-018 state, admitted by the `8dbb0ee`
G11) left $\bar q_i$ ambiguous: $o_1$ for $100$ fully filled and sold, its fee owed; $o_2$ for $100$ with $50$ filled and held; fees $0.01$ per share;
read with $o_1$, $\bar q_i=50$ instead of $100$ and $W_{t+1}=W^{\min}_{t+1}-\tfrac12$. The corrected G11 (F151) excludes the state; the statement,
proof and dependencies of T-19 are unchanged.

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
(b) *Necessary condition, when no clamp is active* ($p'^{\mathrm{lim}}-p^{\mathrm{stop}}_i+\kappa^{\mathrm{out}}_i(\bar q_i)\ge0$ for every pending order): if $W_{t+1}\ge F_t$ for every
outcome in $\mathcal W^{\mathrm{S}}$, then $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t+\Lambda_t$.
(c) *Equivalence:* when no clamp is active, by (a) and (b), floor safety on $\mathcal W^{\mathrm{S}}$ holds **iff** $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t+\Lambda_t=E_t-F_t$.
With an active clamp only (a) holds: the charge includes the unfilled part's fees, which no outcome with $e=0$ incurs.
(d) *The hard-layer condition* F120 ($\le K_t$) is sufficient. It is **not** necessary when $\Lambda_t>0$: states with
$K_t<R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t+\Lambda_t$ are floor-safe. When $\Lambda_t=0$ (e.g. a flat book) it coincides with (c).

**ASSUMPTIONS.** Those of T-10 (including case (1′)); attainability and inactive clamps (for (b) and (c) only).

**PROOF STATUS.** PROOF REQUIRES ADDITIONAL ASSUMPTIONS

**PROOF.** (a) Step (3) of T-10 gives $W_{t+1}\ge W_t-(R^{\mathrm{open}}_t-\Lambda_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n))\ge W_t-K_t=F_t$. (b) In the attainable comonotone outcome
every held exposure realises $\Delta_i=-r^{\mathrm{open}}_i+\Lambda_{i,t}$ (without a stop: $-u^{\mathrm{open}}_i+\Lambda_{i,t}$, prices → $0$), every partially filled order $\Delta_i=-r^{\mathrm{pf}}_i+\Lambda_{i,t}$ (its remainder $q^{\mathrm{unf}}_o$ fills at its limit, it pays
$\phi^{\mathrm{buy}}(n'_o)-\phi^{\mathrm{paid}}_o$, and $\bar q_i=q_{i,t}+q^{\mathrm{unf}}_o$ exits at its bound with fees $\phi^{\mathrm{split}}(\bar q_i)$), every other pending order and the new order $\Delta_i=-L^{\mathrm{stop}}$, and
$\mathrm{Inc}=0$; so $W_{t+1}=W_t-(R^{\mathrm{open}}_t-\Lambda_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n))$, which is $<F_t$ whenever the condition fails. (c) (a) and (b); $K_t+\Lambda_t=E_t-F_t$
by F034, F044. (d) $\Lambda_t\ge0$ (A-ACC-06) gives sufficiency; the AUD-032 example below is a floor-safe state violating F120. ∎

**COUNTEREXAMPLE ATTEMPT.** The v0.1.1 form ("iff $R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t$") is false in the "only if" direction whenever
$\Lambda_t>0$: $q=100$ at $50$, stop $49$, $\kappa^{\mathrm{out}}=0.1$, no fees, $\Lambda_t=5$, $K_t=106<r^{\mathrm{open}}=110$, yet the worst attainable outcome leaves
$W_{t+1}=F_t+1$ (AUD-032). The v0.2 draft's "iff" also failed while a partially filled order was charged open risk plus the full reservation
(REV-025: charge $550>K_t+\Lambda_t=440$, worst outcome $W_{t+1}=F_t$); with F145 that charge is exact. The exhaustive enumeration of T-10 (o) found the
charge minus $\Lambda$ equal to the attained worst loss in every state, which is (b) instance by instance. The `f37c1b6` statement "F120 is
sufficient" was false for a stop trailed above a pending limit (AUD-039; T-10N); with the clamp (a) holds in all $46{,}200$ enumerated scenarios.
With one symbol for the held quantity and the fill (`80ca693`, CLOSURE-REV-006), (a) failed under the fill reading and (b) under the holding reading
after a partial exit while the entry was pending (Case A: $99$ and $162$ against an attained $101.4$); with F145 rebuilt on $q_{i,t}$ and $q^{\mathrm{unf}}_o$ the charge
is attained in every clamp-inactive check of T-10 (viii).

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

### T-27 Gate Monotonicity in Estimates

**THEOREM ID.** T-27

**STATEMENT.** Among `VALID` estimates (F152), call one more conservative when $\hat\kappa^{\mathrm{out}}$, $\hat\Gamma_i$ or $\hat\Lambda_{i,t}$ is larger, $\mathrm{ADV}^{\mathrm{est}}_{i,t}$ is smaller, or the
statistical refinement of the cluster map is coarser (S-006). Holding every other input fixed, no gate G1–G11 of F092 and no post-filter that
fails at an estimate passes at a more conservative one: the allowed transitions are PASS→PASS, PASS→FAIL and FAIL→FAIL; FAIL→PASS is
impossible. In particular a gate that fails with every estimate at its policy bound — the least conservative admissible value (F111) — fails
for every valid estimate. The theorem compares valid estimates only: an estimate that fails validation is not a point of the estimator domain
and is never replaced by its policy bound; a `MISSING` or `INVALID` required estimate gives $\alpha_t=0$ by the authority-validity rule F152
(T-31), which is not a monotonicity statement.

**ASSUMPTIONS.** A-MATH-01; F092 in its closure form (G7 with $\kappa^{\min}p^{\mathrm{stop}}_o$, G8 on the mark); references by F146; $K_t$ by F044 and
$\mathrm{DD}_t$ by F038.

**PROOF STATUS.** PROVED

**PROOF.** It suffices to list the estimate-dependent gates. G1 ($\alpha_t$): validity and presence of inputs, not their size — a missing or invalid
estimate fails G1 whatever the other estimates are (F152, T-31). G2, G5, G6, G9, G10, G11: trading status, spread and mark observations, event flags,
direction, universe, held and reserved quantities, entry-order lifecycle states (F151) — no estimate. G7 (closure form): $p^{\mathrm{lim}},p^{\mathrm{stop}}_o,m^{\mathrm{arr}},p^{\mathrm{ask}}$ and the policy values
$\kappa^{\min},\ell^{\min},\chi$ — no estimate. Its cost clause is the infimum of the sizing per-share loss $p^{\mathrm{lim}}-p^{\mathrm{stop}}_o+\kappa^{\mathrm{out}}(n)$ over every
quantity and every admissible estimate ($\kappa^{\mathrm{out}}\ge\kappa^{\min}p^{\mathrm{stop}}_o$, F111), so it still establishes the division guard of 01 §9 item 16 for
every estimate. G8: authoritative marks and live stops — no estimate, no fee. G3 ($K_t>0$): $K_t=W_t-F_t$; $W_t$ is non-increasing in
$\hat\Lambda$ (F034, F111) and independent of the other estimates; $F_t$ depends only on references (F146: no estimate) and policy. G4
($\mathrm{DD}_t<d^{\max}$): $\mathrm{DD}_t=1-\nu_t/H_t$ with $H_t$ estimate-free (F037, F146), $U_t$ estimate-free (F069) and $\nu_t=W_t/U_t$ non-increasing in
$\hat\Lambda$. The post-filter acts on $Q^{\mathrm{hard}}$, which is non-increasing in conservativeness (T-28). ∎

**COUNTEREXAMPLE ATTEMPT.** The `5c486f0` gates violate it (CLOSURE-REV-001): G7 on $\kappa^{\mathrm{out}}$ ($p^{\mathrm{lim}}=50$, $p^{\mathrm{stop}}_o=49.99$,
$\kappa^{\min}=0.001$, $\ell^{\min}=0.002$: fails at the floor $0.04999$, passes at $\hat\kappa^{\mathrm{out}}=0.1$ with $Q=9{,}090$); G8 as a sign test of F064
($100$ sh, mark $48.9$, stop $49$: raw $-3.1$ at the floor, $+12$ at $\hat\kappa^{\mathrm{out}}=0.2$); G3 and G4 with references from estimate-inclusive $\nu_u$
(a larger past $\hat\Lambda$ lowers $H$, raises $K$ and lowers $\mathrm{DD}$; CLOSURE-REV-002). Exact searches: G7 over $3$ limits, $5$ stop distances and
$15$ ordered estimate pairs ($225$ cases: $50$ FAIL→PASS with the `5c486f0` predicate, $0$ now); G8 over $2$ quantities, $6$ marks around the stop,
$6$ ordered estimate pairs and $3$ fee schedules, plus fee-schedule pairs ($30$ FAIL→PASS for the sign test, $0$ now); G3 and G4 over $20{,}000$
random four-epoch histories with one estimate path dominating another ($6{,}446$ violations with estimate-inclusive references, $0$ with F146).
Comparing a failed estimator, read as its policy bound, with a valid one is outside the theorem; A-EXE-02 did so at `a87b887` (G3: $E_t=100{,}000$,
$F_t=96{,}000$, valid $\hat\Lambda=5{,}000$ gives $K_t=-1{,}000$, a failed $\kappa^{\mathrm{liq}}$ check read as the floor $100$ gives $K_t=3{,}900$; CLOSURE-REV-008),
now $\alpha_t=0$ (T-31). Valid-domain re-check at the correction: $625$ valid points and $2{,}000$ ordered pairs, no larger $Q^{\mathrm{hard}}$ and no G3
FAIL → PASS under a more conservative valid estimate, no $Q^{\mathrm{hard}}$ above its policy-bound value.

**NUMERICAL EDGE CASES.** Mark exactly at the stop (G8 fails); $\kappa^{\min}=0$ (G7's cost clause becomes the bare stop distance); the cost clause
attained with equality (passes).

**MACHINE-TESTABLE INVARIANT.** For every gate and every estimated input, metamorphic pairs (estimate, more conservative estimate) never show
FAIL→PASS; each gate predicate is tested separately, not only through $Q^{\mathrm{hard}}$; the `5c486f0` cases above are regressions that must fail
with the old predicates and pass with the closure ones.

---

### T-28 Estimate Dominance at Every Epoch (Instantaneous and Temporal)

**THEOREM ID.** T-28

**STATEMENT.** Fix the authoritative history up to $\tau_t$ — positions, cash, liabilities, order state, marks, quotes, flows, fee schedule and
policy. Compare any admissible estimates at every epoch $u\le t$ with the evaluation that puts every estimated input at its policy bound at
every epoch, whose cap is $\bar Q^{\mathrm{hard}}_t$ (S-307). (i) *Temporal:* every carried reference — $H_t$, $\nu^{\mathrm{day}}_0$, $\nu^{\mathrm{wk}}_0$, $U_t$ (F037, F041,
F069) — is the same under both; no estimate is stored for a later epoch. (ii) *Instantaneous:* at $t$, $W_t\le W^{\mathrm{R}}_t$; every budget is at most,
and every consumption at least, its policy-bound value; every gate that fails at the policy bounds fails (T-27). (iii) Hence
$Q^{\mathrm{hard}}_t\le\bar Q^{\mathrm{hard}}_t$ at every epoch, and the final quantity after F049 and F126 is at most $\bar Q^{\mathrm{hard}}_t$.

**ASSUMPTIONS.** A-MATH-01; F111 (policy bounds), F146 (reference valuation), F049, F126, T-27. While $\mathrm{SL}_{s,t}$ and $B^{\mathrm{win}}_s$ are UNDEFINED
the strategy term follows the fail-closed rule of 06 §4; once defined (RQ-11) each must be at most its policy-bound value (e.g. $B^{\mathrm{win}}_s$
computed from $W$), or (iii) is not claimed for H3.

**PROOF STATUS.** PROVED

**PROOF.** (i) Induction over epochs. $\nu^{\mathrm{R}}_u=(E_u-\Lambda^{\mathrm{floor}}_u)/U_u$ (F146) uses marks, cash and liabilities ($E_u$), the observed spread and
the fee schedule ($\Lambda^{\mathrm{floor}}_u$) and $U_u$; $H_t=\max_u\nu^{\mathrm{R}}_u$; $\nu^{\mathrm{day}}_0,\nu^{\mathrm{wk}}_0$ are $\nu^{\mathrm{R}}$ at the day and week start; and
$U_{u+1}=U_u+X_{u+1}/\nu^{\mathrm{R}}$ at the flow (F069). None contains an estimate, so if they agree at $u$ they agree at $u+1$, and they agree at
the start of the history. (ii) $\Lambda_t=\max(\Lambda^{\mathrm{floor}}_t,\hat\Lambda_t)\ge\Lambda^{\mathrm{floor}}_t$ gives $W_t\le W^{\mathrm{R}}_t$, the policy-bound value of
$W_t$ (F034, F146). Floors (F040–F043) depend only on references and policy, so they agree, and $K_t$ is at most its policy-bound value; the
base candidates $W_t$, $\min(W_t,\nu^{\mathrm{day}}_0U_t)$ and $K_t$ are at most theirs and $\nu^{\mathrm{day}}_0U_t$ equals its own (06, base table). The
charges F064–F066, F144, F145 and the consumptions F061–F063 are non-decreasing in $\kappa^{\mathrm{out}}$ and in $\Gamma$ (through $p^{\mathrm{gx}}$, F060) and
contain no $\Lambda$ (OC-1), and $\kappa^{\mathrm{out}}\ge\kappa^{\min}p^{\mathrm{stop}}$, $\Gamma\ge\Gamma^{\min}$ (F111). Cluster aggregates over a coarsening of the
human map are at least those over the map (S-006; sums of non-negative terms). $\mathrm{ADV}\le\mathrm{ADV}^{\max}$ makes the H12–H13 budgets at most
theirs. Cash terms ($C^{\mathrm{res}}$, F048) contain no estimate. Gates: T-27. (iii) For each cap the feasible set $\{n:g_k(n)\le b_k\}$ is contained in
its policy-bound counterpart, so its maximum (F094) is no larger; the minimum over caps preserves this; a failing gate gives $0$. F049 gives
$b^{\mathrm{allow}}_k\le(b^{\mathrm{hard}}_k)^+$ and F126 returns at most $Q^{\mathrm{hard}}$. ∎

**COUNTEREXAMPLE ATTEMPT.** Instantaneous monotonicity alone is not enough. At `5c486f0` the references used estimate-inclusive $\nu_u$
(CLOSURE-REV-002): $E_u=10^6$, $\hat\Lambda_u=50{,}000$ against a floor of $1{,}000$; later $E_t=990{,}000$, $\Lambda_t=1{,}000$, $d^{\max}=10\%$, $U=1$:
$H=989{,}000$ and $K_t=98{,}900$, against $89{,}900$ (with $H=999{,}000$) at the policy bounds — the estimate at $u$ enlarged the cushion at $t$ by
$9{,}000$ although every cap at $t$ was monotone in the estimates at $t$. Units: a withdrawal of $95{,}000$ at the estimate-inclusive NAV
($E=10^6$, $\hat\Lambda=50{,}000$, floor $1{,}000$, $U=1{,}000$) left $U=900$ and $K=45{,}810$; at $\nu^{\mathrm{R}}$ it leaves $U=904{,}000/999$ and $K=41{,}400$, the
policy-bound value. Exact search: $20{,}000$ random five-epoch histories with flows — $13{,}517$ histories with some epoch above the policy-bound
cushion under estimate-inclusive references and units, $0$ with F146.

**NUMERICAL EDGE CASES.** $\hat\Lambda=\Lambda^{\mathrm{floor}}$ (equality); rounding of stored references (01 §9 item 3; the direction for $\nu^{\mathrm{day}}_0$
used as a base is the open CLOSURE-REV-009).

**MACHINE-TESTABLE INVARIANT.** Two evaluations over the same randomly generated authoritative history — arbitrary admissible estimates
versus policy bounds at every epoch: stored references bit-identical at every epoch; $Q^{\mathrm{hard}}_t\le\bar Q^{\mathrm{hard}}_t$ and every gate that fails at
the policy bounds fails; the $+9{,}000$ and the units cases are regressions.

---

### T-29 Entry-Fee Booking Conservation

**THEOREM ID.** T-29

**STATEMENT.** For every entry order $o$ and every sequence of events — fills, fee bookings (to cash or as a payable), the venue-confirmed
terminal state, the confirmation that its fees are final — with $\phi^{\mathrm{paid}}_o$ in its domain (F148): (a) until the fees are final,
$\phi^{\mathrm{paid}}_o+\phi^{\mathrm{owed}}_o=\phi^{\mathrm{acc}}_o$ (F149); (b) a booking of $b\ge0$ raises $\phi^{\mathrm{paid}}_o$ by $b$ and lowers $\phi^{\mathrm{owed}}_o$ by $b$; a fill
raises $\phi^{\mathrm{acc}}_o$ and $\phi^{\mathrm{owed}}_o$ by the same amount; the terminal state changes neither; (c) $W_t-\sum_o\phi^{\mathrm{owed}}_o$ is unchanged by a
booking; (d) at every cut each entry-fee dollar up to $\phi^{\mathrm{acc}}_o$ is either in $W_t$ or in exactly one hard-layer charge — inside
$r^{\mathrm{pf}},g^{\mathrm{pf}},u^{\mathrm{pf}}$ and $C^{\mathrm{res}}$ (F145, F144) for a pending order, in the owed-fee reservation of F144 for a terminal one — never in both and
never in neither; when the fees are confirmed final the unbooked remainder (the unused part of the bound, $\ge0$ by A-EXE-04) is released.

**ASSUMPTIONS.** A-MATH-01; the definitions F144, F145, F148, F149, with $\phi^{\mathrm{paid}}_o$ and $W_t$ taken from the same cut.

**PROOF STATUS.** PROVED

**PROOF.** (a) Definition F148. (b) A booking adds $b$ to the fees in $W_t$, hence to $\phi^{\mathrm{paid}}_o$, and leaves $\phi^{\mathrm{acc}}_o$ unchanged; a fill raises
$q^{\mathrm{fill}}_o$ and $\phi^{\mathrm{acc}}_o=\phi^{\mathrm{buy}}_o(q^{\mathrm{fill}}_o)$ and books nothing; the terminal state changes neither $q^{\mathrm{fill}}_o$ nor the bookings. (c) The
booking lowers $W_t$ by $b$ (F052, F055) and $\sum_o\phi^{\mathrm{owed}}_o$ by $b$. (d) A booked dollar is in $W_t$ and, by (a), no longer in
$\phi^{\mathrm{owed}}_o$; an unbooked one is in $\phi^{\mathrm{owed}}_o$, which appears inside $\phi^{\mathrm{buy}}(n')-\phi^{\mathrm{paid}}_o$ in F145 and $C^{\mathrm{res}}$ for a pending order
and only in the F144 owed-fee reservation for a terminal one (F064–F066 carry no entry fee). ∎

**COUNTEREXAMPLE ATTEMPT.** `5c486f0` violated (d) — "never in neither" — in three ways: a terminal order's owed fee was in no charge and not in
$W_t$ (cases A, B, C of CLOSURE-REV-003); a fee reported but not booked was treated as paid (case D); $\phi^{\mathrm{paid}}_o>\phi^{\mathrm{acc}}_o$ was credited (case
E). Exact event-sequence check ($5{,}000$ random sequences, $60{,}000$ events: fills, bookings of none, half or all of the owed fee at any time,
terminal and fee-final events; $\phi^{\mathrm{paid}}_o$, $\phi^{\mathrm{owed}}_o$ and $W_t-\sum_o\phi^{\mathrm{owed}}_o$ tracked): no violation.

**NUMERICAL EDGE CASES.** $\phi^{\mathrm{paid}}_o=\phi^{\mathrm{acc}}_o$ (nothing owed); a booking larger than $\phi^{\mathrm{owed}}_o$ leaves the domain ($\alpha_t=0$, F148);
fees confirmed final below the bound (release).

**MACHINE-TESTABLE INVARIANT.** Event-sequence property test: (a)–(c) exactly at every step; in the simulated engine every booked fee is in
$W_t$ and every owed fee in exactly one charge; $W_t-\sum_o\phi^{\mathrm{owed}}_o$ constant across bookings.

---

### T-30 Entry-Gate Lifecycle Monotonicity

**THEOREM ID.** T-30

**STATEMENT.** Let two snapshots agree in the authoritative lifecycle state $\mathrm{lc}_{o,t}$ of every entry order, differing at most in quantities
($q^{\mathrm{unf}}_o$, $q^{\mathrm{fill}}_o$, $Q^{\mathrm{res}}_{i,t}$, $q_{i,t}$) or fee state. (a) If $\mathcal E^{\mathrm{NT}}_{i,t}\ne\varnothing$, G11 fails for $i$ in both; in particular
$q^{\mathrm{unf}}_o\to0$ alone, with $o$ `NON_TERMINAL`, never turns G11 from FAIL into PASS. (b) G11 passes for $i$ only if every entry order on $i$ is
`TERMINAL_CONFIRMED` by authoritative evidence; a state $\bot$ never lets a new entry pass. (c) The transition FAIL → PASS of G11 for $i$, with
$q_{i,t}=0$ and $Q^{\mathrm{res}}_{i,t}=0$ unchanged, requires a change of authoritative lifecycle evidence, not of any quantity.

**ASSUMPTIONS.** A-MATH-01.

**PROOF STATUS.** PROVED

**PROOF.** G11 (F092, F151) is the conjunction of $q_{i,t}=0$, $Q^{\mathrm{res}}_{i,t}=0$ and $\mathcal E^{\mathrm{NT}}_{i,t}=\varnothing$, evaluated only when the lifecycle is
valid (otherwise $\alpha_t=0$ and G1 fails). $\mathcal E^{\mathrm{NT}}_{i,t}$ is a function of the lifecycle states alone, so it is the same set in both
snapshots. (a) A non-empty set falsifies the third conjunct in both, whatever the quantities. (b) If G11 passes, the lifecycle is valid, so no
entry order on $i$ has state $\bot$, and $\mathcal E^{\mathrm{NT}}_{i,t}=\varnothing$, so none is `NON_TERMINAL`: each is `TERMINAL_CONFIRMED`. A state $\bot$
makes the lifecycle invalid, $\alpha_t=0$. (c) With the first two conjuncts true in both snapshots, G11 changes value only if
$\mathcal E^{\mathrm{NT}}_{i,t}$ does, i.e. only if some lifecycle state changes. ∎

**COUNTEREXAMPLE ATTEMPT.** Under the `8dbb0ee` gate ($q_{i,t}=0$, $Q^{\mathrm{res}}_{i,t}=0$ only) (a) is false: an order with $40$ unfilled blocks a new
entry, the same order fully filled ($q^{\mathrm{unf}}_o=0$) and still `NON_TERMINAL` admitted one (CLOSURE-REV-018). In the Boolean lifecycle
enumeration of T-10 (ix) (09 closure-review registry), $18$ of $36$ pairs "same lifecycle, $q^{\mathrm{unf}}_o>0\to0$" turn BLOCKED into ALLOWED under the old gate, $0$ under the
corrected one.

**NUMERICAL EDGE CASES.** $q^{\mathrm{unf}}_o=0$ exactly; terminal by cancellation with an unfilled remainder (`TERMINAL_CONFIRMED`, no reservation of the
remainder, F144); terminal confirmation and fee finality in different epochs; a correction contradicting a terminal record ($\bot$).

**MACHINE-TESTABLE INVARIANT.** For every snapshot and every `NON_TERMINAL` entry order $o$ on $i$, setting $q^{\mathrm{unf}}_o$ to $0$ (and $Q^{\mathrm{res}}_{i,t}$
accordingly) leaves G11 FAIL; G11 PASS implies every entry order on $i$ `TERMINAL_CONFIRMED`; a state $\bot$ anywhere implies $\alpha_t=0$.

---

### T-31 Estimator-Validity Fail-Closed Admission

**THEOREM ID.** T-31

**STATEMENT.** Change a snapshot only in the status of one or more required hard-layer estimates (F152), each from `VALID` to `MISSING` or
`INVALID`. Then (a) $\alpha_t=0$ after the change: G1 fails and the decision is NO\_TRADE, so the admission transition is TRADE → NO\_TRADE or
NO\_TRADE → NO\_TRADE; NO\_TRADE → TRADE is impossible, and so is TRADE → TRADE with a substituted value (the policy bound, $0$, a last or default
value, a model or an optimiser value); (b) every cap is $0$, so no cap and no gate result is more permissive than before; (c) every carried reference
($H_t$, $\nu^{\mathrm{day}}_0$, $\nu^{\mathrm{wk}}_0$, $U_t$) is the same as without the change (F146; T-28 (i)), so the failure acts only in the epochs in which it
persists. This is an authority-validity property, not monotonicity in the values of valid estimates (T-27).

**ASSUMPTIONS.** A-MATH-01.

**PROOF STATUS.** PROVED

**PROOF.** (a) By F152 a `MISSING` or `INVALID` required estimate gives $\alpha_t=0$; G1 ($\alpha_t=1$, F092) fails, a failing gate gives $Q=0$, and the
decision is NO\_TRADE. The estimate has no value for authority purposes, so no substitute enters any cap or gate. (b) Immediate from (a). (c) F146
values every carried reference at $W^{\mathrm{R}}=E-\Lambda^{\mathrm{floor}}$ and issues units at $\nu^{\mathrm{R}}$; neither contains an estimate (T-28 (i)). ∎

**COUNTEREXAMPLE ATTEMPT.** With A-EXE-02 as at `a87b887` (a failed grid check read as the policy floor) (a) is false: H1 with $f^{\mathrm{trd}}B=1{,}000$,
limit $50$, stop $49$, $\kappa^{\min}=0.001$, no fees: a valid $\hat\kappa^{\mathrm{out}}=0.5$ gives $666$ sh, the failed check $953$; with $n^{\min}=700$ NO\_TRADE becomes
TRADE. A failed $\kappa^{\mathrm{liq}}$ check read as $\Lambda^{\mathrm{floor}}$: $E_t=100{,}000$, $F_t=96{,}000$, valid $\hat\Lambda=5{,}000$ gives $K_t=-1{,}000$ (G3 fails), the floor
$100$ gives $K_t=3{,}900$ (G3 passes). F111's $\max$ absorbed an out-of-domain $\hat\kappa^{\mathrm{out}}=-0.5$ into the floor ($953$). Exact enumeration of the
four estimators, each valid above, at or below its bound, missing, or invalid in nine ways (stale, non-finite, outside its domain low or high,
wrong unit, instrument or cut, failed grid or load check, failed version): $28{,}561$ states, $28{,}480$ with a missing or invalid estimate, all
$\alpha_t=0$; $263{,}640$ single-estimator degradations: no larger $Q^{\mathrm{hard}}$, no NO\_TRADE → TRADE, no TRADE → TRADE, no G3 FAIL → PASS — against
$376$, $200$, $1{,}660$ and $250$ under the explicit `a87b887` rules ($n^{\min}=0$).

**NUMERICAL EDGE CASES.** A valid estimate exactly at its bound (`VALID`; bounded value equals the bound); a valid estimate on the permissive side
of its bound (`VALID`; the bound acts on a valid value); $\mathrm{age}_t=\mathrm{TTL}$ exactly (valid); $\hat\kappa^{\mathrm{out}}=0$ inside its domain (valid).

**MACHINE-TESTABLE INVARIANT.** For every snapshot and every required estimate, degrading its status to `MISSING` or `INVALID` gives $\alpha_t=0$ and
NO\_TRADE; no evaluation path reads the policy bound after a failed check; carried references are bit-identical with and without the failure.

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
