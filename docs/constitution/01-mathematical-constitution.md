# 01 — Mathematical Constitution (v0.2-draft)

Status: DRAFT for human review. Normative text uses **MUST / MUST NOT**. Candidate constructions are marked
**PROVISIONAL**. Unresolved objects are marked **UNDEFINED — REQUIRES RESOLUTION**. Symbols are defined only in
[02-symbol-registry.md](02-symbol-registry.md).

---

## 1. Governing question (formal statement)

Given an authoritative snapshot $\mathsf S_t$ (which determines the state $x_t$), an opportunity $o$ on instrument $i$ with
direction $d$, the policy vector $\theta$ and the version tuple $\mathsf v$, compute

$$
Q^{\mathrm{fin}}_t(o)\;=\;\max\Big\{\,n\in\mathbb L_{\ge0}\;:\;n=0\ \ \text{or}\ \ \big(d\,n\,\mathbf 1_i\in\mathcal A^{\mathrm{safe}}(x_t)\ \wedge\ \mathrm{LB}_t(d\,n\,\mathbf 1_i)>\varepsilon^{\min}\big)\Big\}
$$
**[F001]**

together with the evidence that justifies it. $Q^{\mathrm{fin}}_t(o)=0$ is a **valid, successful answer** (NO TRADE), never an
error. The objects $\mathcal A^{\mathrm{safe}}$ and $\mathrm{LB}_t$ are defined in §7 and §8; in v0.2 $\mathrm{LB}_t$ is
**UNDEFINED — REQUIRES RESOLUTION**, so only the safety half of this definition is specified.

Note: the $\max$ above is well defined only if the feasible set is finite and contains $0$ — guaranteed by $n\le\bar N$ and by
Art. 2.

## 2. Articles (normative)

**Art. 1 — Lexicographic authority.** Layers are ordered AUTHORITY → SAFETY → MATHEMATICAL VALIDITY → NUMERICAL CORRECTNESS →
STATISTICAL ROBUSTNESS → PERFORMANCE. Formally the decision is computed by a chain of set filters

$$
\mathcal A^{(0)}\supseteq\mathcal A^{(1)}\supseteq\mathcal A^{(2)}\supseteq\mathcal A^{(3)}\supseteq\mathcal A^{(4)}\supseteq\mathcal A^{(5)},\qquad a^{\varnothing}\in\mathcal A^{(0)}\cap\cdots\cap\mathcal A^{(5)},
$$
**[F002]**

where the set with superscript $(k)$ is the set admitted by layers $0..k$. A lower layer MAY only select within, or shrink, the set admitted
by all higher layers. No lower layer may add an element. Performance selects the final element of $\mathcal A^{(5)}$.

**Art. 2 — No-trade is first-class.** $a^{\varnothing}$ is a member of every layer's set as a *decision*. Returning $a^{\varnothing}$
is a successful outcome carrying a non-empty reason set $\mathsf{rc}$.

**Art. 3 — No-trade is not a safety certificate.** $a^{\varnothing}$ means "no new risk is authorised". It does **not** assert that the
existing portfolio satisfies any floor. (Counterexamples: T-06b, T-20b in [08](08-theorem-register.md).) When the existing
state violates a floor-safety invariant the output is RECOVERY — an advisory statement of the violated invariant and the
risk-reducing obligation — and the engine takes no action to discharge it (Art. 17).

**Art. 4 — UNKNOWN ≠ ZERO ≠ SAFE.** A required quantity that cannot be established from $\mathsf S_t$ MUST NOT be replaced by $0$
(for exposure, loss, cost, reservation) nor by $+\infty$ / "no limit" (for a budget). It is either replaced by its worst admissible
value as specified in the registry, or the decision is $a^{\varnothing}$. Absence and zero MUST be distinguishable in every schema.

**Art. 5 — Hard dominance.** Every model / statistical / AI layer MAY only tighten budgets: componentwise
$0\le b^{\mathrm{allow}}_k\le b^{\mathrm{hard}}_k$ for every hard constraint $k$. In particular $0\le R^{\mathrm{allow}}_t\le R^{\mathrm{hard}}_t$.
The scalar form alone is insufficient; the vector form is required (06 §4).

**Art. 6 — Forecast independence of the hard layer.** The hard layer MUST NOT depend on: win probability, target price,
expected return, estimated correlation below $1$, or any fitted parameter — *except* a deterministic statistic of admissible
historical data that enters only in the conservative direction and is bounded by a policy constant
(e.g. $\Gamma_i=\max(\Gamma^{\min},\hat\Gamma_i)$). Such statistics make the constraint's *computation* deterministic but its
*protective meaning* conditional; the condition MUST be named (tiers U/S/G/L, 06 §2).
**Amendment (v0.2, AUD-002).** Every estimate or model quantity that the hard layer consumes ($\kappa^{\mathrm{out}}$, $\Lambda$, $\mathrm{ADV}$,
$\Gamma$) is a *hard-layer component*: its estimator definition is frozen, versioned in $\mathsf v$ and set under human authority, and it
enters only through a policy bound in the conservative direction (F111): a floor for a cost ($\kappa^{\mathrm{out}}$, $\Gamma$, $\Lambda$) and a cap for a
capacity ($\mathrm{ADV}=\min(\mathrm{ADV}^{\mathrm{est}},\mathrm{ADV}^{\max})$; closure, AUD-040); a statistical cluster map may only merge clusters of the human-set
map (S-006). A missing estimate gives $\alpha_t=0$, never the policy bound (AUD-041). Invariant: every hard cap computed with any estimates is $\le$
the same cap with every estimated input at its policy bound. Advanced models MUST NOT supply or replace these inputs;
their only channel is a proposed budget $b^{\mathrm{mod}}_k$ (Art. 5). Otherwise a model could enlarge hard caps through their inputs.

**Art. 7 — Exact authority arithmetic.** Every quantity on the authority path is computed exactly in $\mathbb Q$ or with rounding
directed toward the conservative side (§9). Binary floating point MUST NOT appear on the authority path.

**Art. 8 — Purity and determinism.** $\mathcal D$ is a pure function of (canonical bytes of $\mathsf S_t$, $o$, $\theta$, $\mathsf v$). It reads no
clock, network, file, environment variable or global numeric context. Randomness, if any, is seeded from and recorded in the
inputs. Same inputs ⇒ byte-identical output.

**Art. 9 — Measurability / no look-ahead.** Every datum admitted to $\mathsf S_t$ satisfies $t^{\mathrm{know}}(\mathsf d)\le\tau_t$
(bitemporal admission rule, §3.2). Every estimate in $\mathsf S_t$ is computed only from admitted data.

**Art. 10 — Single authority per quantity.** Every registered symbol has exactly one source class (02). The engine MUST NOT
re-derive an authoritative input it is given (e.g. $\mathrm{BP}_t$) and treat its own derivation as authority; it MAY combine an
authoritative input with an internal bound only through a conservative operator ($\min$ for capacities, $\max$ for
consumptions), and MUST record both operands as evidence.

**Art. 11 — Budget conservation.** For each budget family, every unit is in exactly one of {available, reserved, open,
consumed} (T-11). The engine is pure; conservation is enforced by the external ledger, whose state is an input.

**Art. 12 — Economic cost identity.** Every cost and loss appears exactly once in the wealth transition (05 §3, ECAI). Hard-layer *bounds* may
over-charge a cost only through a registered conservative over-charge (OC-$k$, 05 §4) with a stated reason; they may never under-charge.

**Art. 13 — Separation of safety and optimisation.** The optimiser receives the safe set as read-only data, returns a *proposal*,
and the proposal is re-verified exactly (T-03, part c). The optimiser can neither create, relax, nor evaluate the hard envelope's
existence. Optimiser failure of any kind ⇒ $a^{\varnothing}$.

**Art. 14 — Proof discipline.** A claim is PROVED only by a written proof of a stated proposition under stated assumptions, reviewed
independently. Passing tests or examples never promotes a claim. A paper proof about a specification does not transfer to an
implementation; implementation conformance is a separate claim (validated by differential and property testing).

**Art. 15 — Complexity must earn its existence.** Every construct beyond the Phase-17 baselines must demonstrate a benefit that
survives the validation doctrine (§11). Otherwise the simpler construct is preferred.

**Art. 16 — Human policy authority.** Every component of $\theta$ is set by the human controller, versioned, and never fitted on a
final test sample. Research may *propose* values with evidence; it may not *set* them.

**Art. 17 — No execution capability.** The engine's outputs are data: bounds, reasons, evidence. It cannot submit, approve,
modify or cancel orders, cannot bypass human approval, cannot mutate broker or ledger state, and cannot invent account state
(any field absent from $\mathsf S_t$ ⇒ Art. 4).

**Art. 18 — Fail-closed totality.** $\mathcal D$ is total: every input (including malformed input) yields exactly one decision record.
Internal failure (exception, non-termination bound exceeded, invalid intermediate) yields $a^{\varnothing}$ with a reason code. No
partial outputs.

---

## 3. Decision model

### 3.1 Time and event ordering

Decision epochs $t\in\mathbb T=\{0,1,\dots\}$ at instants $\tau_0<\tau_1<\cdots$. The period $(\tau_t,\tau_{t+1}]$ contains, in
order of causality: (i) the decision at $\tau_t^{+}$; (ii) order acceptance/rejection; (iii) fills of entry orders (possibly partial);
(iv) market evolution, including triggering and filling of protective stops; (v) corporate actions and cash events;
(vi) the next authoritative cut at $\tau_{t+1}$.

Because stops are **path-dependent**, $\xi_{t+1}$ MUST contain the intra-period path (at minimum the sequence of tradable
prices and halt states), not only $m_{\cdot,t+1}$. A model that uses only endpoints cannot represent stop execution and is
inadmissible for anything that reasons about $L^{\mathrm{stop}}$.

Epoch spacing is not assumed uniform. Whether decisions are event-driven or clock-driven is **UNDEFINED — REQUIRES
RESOLUTION** (RQ-28); nothing in this document depends on it except multi-period tail measures (§5).

### 3.2 Probability space, filtrations, measurability (Phase 6)

- $(\Omega,\mathcal F,\mathbb P)$: a probability space on which all market and execution randomness is defined. $\mathbb P$ is
  **unknown**; its existence is a modelling postulate (A-STAT-00), not an empirical fact.
- $\mathbb G=(\mathcal G_t)$: the full market filtration (everything that has happened by $\tau_t$).
- $\mathbb F=(\mathcal F_t)$, $\mathcal F_t:=\sigma(\mathsf S_0,\dots,\mathsf S_t)\subseteq\mathcal G_t$ [F141]: the **decision filtration** — what
  the engine is permitted to know.
- **Admissibility of decisions.** A decision rule is admissible iff $a_t$ is the action component of $\mathsf{RD}_t=\mathcal D(\mathsf S_t,o,\theta,\mathsf v)$ (F006; the only policy is $\mathcal D$). This makes
  $a_t$ $\sigma(\mathsf S_t)$-measurable, hence $\mathcal F_t$-measurable. All path-dependent quantities ($H_t$, $\nu^{\mathrm{day}}_0$,
  $\nu^{\mathrm{wk}}_0$, reservations, $\mathrm{MDD}_t$) MUST be carried *inside* $\mathsf S_t$; the engine is therefore Markov in the
  snapshot, which is what makes replay possible.
- Because $\mathsf S_t$ takes values in a countable set of canonical byte strings, *any* function of it is measurable; the substantive
  content of "no look-ahead" is therefore the **admission rule**, not measure theory:

$$
\textbf{(NLA)}\qquad \forall\,\mathsf d\in\mathsf S_t:\ t^{\mathrm{know}}(\mathsf d)\le\tau_t,\qquad
\forall\ \text{estimates } \hat e\in\mathsf S_t:\ \hat e=\Phi(\{\mathsf d: t^{\mathrm{know}}(\mathsf d)\le\tau_t\}).
$$
**[F003]**

  Consequences: data MUST be bitemporal (event time, knowledge time); later corrections/restatements MUST NOT overwrite earlier
  knowledge; the admissible universe $\mathbb I_t$ is as-of $\tau_t$ (no survivorship).

### 3.3 State vector

$$
x_t=\big(x^{A}_t,\ x^{P}_t,\ x^{M}_t,\ x^{H}_t,\ x^{B}_t,\ x^{U}_t\big)
$$
**[F004]**

| Block | Content (registry IDs) | Class |
|---|---|---|
| $x^{A}$ authority | $\mathrm{hash}(\mathsf S_t)$, $A_{\mathrm{id}}$, $\tau_t$, ages, $\alpha_t$ (S-020..S-028) | O/D |
| $x^{P}$ portfolio | $C_t$, $C^{\mathrm{set}}_t$, $C^{\mathrm{uns}}_t$, $q_{\cdot,t}$, $p^{\mathrm{stop}}_{\cdot,t}$, $Y_t$, $U_t$, $\mathrm{BP}_t$ (S-030..S-039, S-122) | O/D |
| $x^{M}$ market | $p^{\mathrm{bid}},p^{\mathrm{ask}}$, $\mathrm{st}$, $\mathrm{ev}$, $\mathrm{ADV}$ (S-050..S-058) | O/E |
| $x^{H}$ history | $H_t$, $\nu^{\mathrm{day}}_0$, $\nu^{\mathrm{wk}}_0$, $\mathrm{MDD}_t$ (S-101..S-104) | D (carried) |
| $x^{B}$ budget ledger | $R^{\mathrm{res}},G^{\mathrm{res}},Z^{\mathrm{res}},N^{\mathrm{res}},C^{\mathrm{res}}$ by instrument, strategy and cluster; $Q^{\mathrm{res}}_{i,t}$ (S-097, S-248) | O |
| $x^{U}$ uncertainty | $\mathcal P_t$, $\hat\sigma$, $\hat\Sigma$, $\hat\pi_t$, $\hat\Gamma$ (S-055, S-056, S-088, S-134, S-135) | E |

$\theta$ (policy) and $\mathsf v$ (versions) are **not state**: they do not evolve with the market and are changed only by human
authority.

### 3.4 Action space and action classes

- $a_t\in\mathbb L^{N_t}$, with order parameters $\omega_t$. For one opportunity: $a=d\,n\,\mathbf 1_i$, $n\in\mathbb L_{\ge0}$ (F001, F024).
- Classification relative to $q_t$ (component $i$): $a$ is **risk-reducing** ($\mathcal A^{-}$) iff for every $i$,
  $\lvert q_i+a_i\rvert\le\lvert q_i\rvert$ and $\operatorname{sgn}(q_i+a_i)\in\{\operatorname{sgn}(q_i),0\}$; **hold** ($\mathcal A^{h}$) iff $a=0$;
  otherwise **risk-increasing** ($\mathcal A^{+}$) **[F005]**.
- v0 scope: the engine evaluates only $\mathcal A^{+}$ actions of the form $d\,n\,\mathbf 1_i$ with $d=+1$ (subject to D-01).
- **Recovery liveness principle (PROVISIONAL).** No constraint designed to cap risk *increases* may be applied to a
  risk-reducing action. Otherwise the system can trap itself in a state where it can neither add nor remove risk. Risk-reducing
  actions are outside the v0 engine; this principle binds the future integration contract.

### 3.5 Decision function and outputs

$$
\mathcal D:\ \mathfrak S\times\mathcal O\times\Theta\times\mathcal V\longrightarrow\mathfrak D,\qquad
\mathsf{RD}_t=\mathcal D(\mathsf S_t,o,\theta,\mathsf v).
$$
**[F006]**

Output classes: **TRADE**($Q^{\mathrm{fin}}>0$, caps vector, binding constraints, reservation vector, evidence),
**NO\_TRADE**($\mathsf{rc}$, evidence), **RECOVERY**($\mathsf{rc}$, violated invariant, advisory obligation, evidence). Final schema:
**UNDEFINED — REQUIRES RESOLUTION** (Phase 19).

Evaluation order (normative): authority gate → input-validity gate → hard caps (exact) → model tightening (exact
composition) → optimiser proposal (optional) → exact verification → certified-advantage test → minimum-order filter → record.

---

## 4. Uncertainty frame (Phase 6)

**Adopted model: none.** Every candidate below is **UNDEFINED — REQUIRES RESOLUTION** as a production component. The hard
layer uses no probability law at all.

| Candidate | Represents | Statistical justification requires | Can put mass on unseen tail outcomes? | Dependence handling | Known weakness |
|---|---|---|---|---|---|
| Empirical law $\hat{\mathbb P}_{M^{\mathrm{obs}}}$ | Sample frequencies | Stationarity + ergodicity | No | None | Tail = worst observed; regime blind |
| Block / stationary bootstrap | Sampling variability of statistics | Stationarity + mixing; block-length choice | No (resamples observed blocks) | Yes (blocks) | Not a model of regime change |
| Wasserstein ball $\{\mathbb Q:\mathfrak W(\mathbb Q,\hat{\mathbb P}_{M^{\mathrm{obs}}})\le\varepsilon^{W}\}$ **[F007]** | Distribution shift within transport budget | Finite-sample radius from concentration results that assume i.i.d. data and **light tails**; radius decays like $(M^{\mathrm{obs}})^{-1/\max(D^{\mathrm{dim}},2)}$ in data dimension $D^{\mathrm{dim}}$ (verified: Mohajerin Esfahani & Kuhn 2018, via Fournier & Guillin 2015) | Yes, if support is unrestricted | Only via extensions (mixing) | Equity returns are heavy-tailed and dependent ⇒ finite-sample radius not justified as stated; unrestricted support can make log objectives $-\infty$ (T-19) |
| $\varphi$-divergence ball (KL, $\chi^2$) | Reweighting of observed outcomes | Asymptotic empirical-likelihood calibration, i.i.d. | **No** — absolute continuity w.r.t. $\hat{\mathbb P}_{M^{\mathrm{obs}}}$ | No | Cannot represent a gap larger than any observed (FM-TAIL-2) |
| Moment ambiguity | All laws with moments in a confidence region | Finite moments; stable moment estimates | Yes (extremal laws) | Via moment estimator | Heavy tails ⇒ unstable variance estimates; very conservative |
| Regime-conditioned laws | $\mathbb P(\cdot\mid z_t)$ mixture | Correct regime model; regime-posterior uncertainty | Depends on components | Via regime dynamics | Misclassification; regime change not in history |
| Extreme-value (POT/GPD) tail | Tail beyond threshold | Tail stationarity; threshold choice | Yes (extrapolation) | Declustering needed | Parameter uncertainty large; few exceedances |
| Bayesian posterior | Parameter uncertainty | Prior specification | Via predictive | Model-dependent | Prior sensitivity |

Rules:
1. An ambiguity set MUST be $\mathcal F_t$-measurable (constructed from admitted data only).
2. A distributionally robust construction MUST NOT be adopted unless its radius / level has a stated statistical justification
   whose assumptions are tested on the target data (RQ-12), or is calibrated by walk-forward validation that never touches
   the final test sample (§11).
3. For tail quantities, candidates that cannot place mass outside the observed support are inadmissible as sole models.

## 5. Tail-risk frame (Phase 7)

**Loss convention.** One-period, flow-adjusted, loss-positive:
$\mathcal L_{t+1}(a):=W_t+X_{t+1}-W_{t+1}(a)$ **[F008]** with $W_{t+1}(a)$ given by the wealth transition $G$ (05). Tail measures are functionals
of the law of $\xi_{t+1}$ pushed through $G$; no separate P&L model is permitted (single-authority rule for losses).

- $\mathrm{VaR}_\beta(\mathcal L):=\inf\{y\in\mathbb R:\mathbb P(\mathcal L\le y)\ge\beta\}$ **[F009]**.
- $\mathrm{ES}_\beta(\mathcal L):=\frac1{1-\beta}\int_\beta^1\mathrm{VaR}_\upsilon(\mathcal L)\,d\upsilon$ **[F010]**
  $=\min_{y\in\mathbb R}\Big\{y+\tfrac1{1-\beta}\mathbb E[(\mathcal L-y)^+]\Big\}$ (Rockafellar–Uryasev) **[F011]**.
- Floor-breach probability $\mathrm{PB}_t(a):=\mathbb P(W_{t+1}(a)<F_t\mid\mathcal F_t)$ **[F012]**; chance constraint $\mathrm{PB}_t(a)\le\epsilon^{\mathrm{ruin}}$ **[F013]**.
- Ruin over horizon $h$: $\mathrm{Ruin}_h:=\{\exists u\in(t,t+h]:W_u<F_u\}$ (floor ruin) or $\{\exists u: W_u\le0\}$ (absolute ruin) —
  choice **UNDEFINED — REQUIRES RESOLUTION** (RQ-30). $\mathrm{PoR}_h:=\mathbb P(\mathrm{Ruin}_h\mid\mathcal F_t)$ **[F014]**.
- $\mathrm{DaR}_\beta:=\mathrm{VaR}_\beta\big(\max_{u\in(t,t+h]}\mathrm{DD}_u\big)$, $\mathrm{CDaR}_\beta$ analogously with ES **[F015]**.

**Selection (PROVISIONAL).**
- ES (coherent) is the candidate *optimisable* tail measure for the model layer; VaR is reporting/backtesting only
  (not subadditive — counterexample FM-TAIL-1).
- The chance constraint is the *semantic* target of the floor; its convex conservative surrogate is
  $\mathrm{ES}_{1-\epsilon^{\mathrm{ruin}}}(F_t-W_{t+1})\le0\Rightarrow \mathrm{PB}_t\le\epsilon^{\mathrm{ruin}}$ (Nemirovski–Shapiro style CVaR approximation) **[F016]**.
- Nested / dynamic CVaR only if multi-period optimisation is adopted (it is not in v0); static CVaR of terminal wealth is
  time-inconsistent under re-optimisation and is excluded.
- **Structural decomposition (T-25; corrected in v0.2, AUD-003).** For a state inside the cushion ($R^{\mathrm{open}}_t+R^{\mathrm{res}}_t+L^{\mathrm{stop}}(n)\le K_t$) and
  under the other tier-S hypotheses of T-10, $\{W_{t+1}<F_t\}\subseteq\bigcup_i\{\text{A-TRIG fails for }i\}$ (A-TRIG is the position-level
  exit-value bound F072; A-STOP is its per-share sufficient condition), hence $\mathrm{PB}_t\le\sum_i\mathbb P(\text{A-TRIG fails for }i)$ **[F123]**. For states inside the cushion, tail modelling effort
  therefore belongs to the probability and severity of **stop failure** (gaps, halts), not to generic return tails.

## 6. Optimisation frame (Phase 8)

$$
a^{\star}_t\in\arg\max_{a\in\mathcal A^{\mathrm{safe}}(x_t)\cup\{a^{\varnothing}\}} J_t(a),\qquad J_t:\ \textbf{UNDEFINED — REQUIRES RESOLUTION}.
$$
**[F017]**

| Candidate $J_t(a)$ (formula ID) | Domain requirement | Structural consequence | Red flag |
|---|---|---|---|
| $\mathbb E_{\mathbb P}[W_{t+1}(a)-W_t]$ (F018) | integrability | Affine in $n$ under linear costs ⇒ argmax $\in\{0,Q^{\mathrm{hard}}\}$ (bang-bang) — "expected-value sizing" is cap sizing | No risk aversion; unbounded without caps |
| $\mathbb E_{\mathbb P}[\log(W_{t+1}(a)/W_t)]$ (F019) | $W_{t+1}(a)>0$ a.s. (T-19) | Concave in $n$ ⇒ interior optimum possible | Estimation-error sensitivity; overbetting |
| Fractional Kelly $\varpi\,n^{\log}$, $\varpi\in(0,1]$ (F020) | as above | Growth–security trade-off (MacLean–Ziemba–Blazenko) | $\varpi$ is a preference, not derived |
| $\mathbb E[W_{t+1}-W_t]-\lambda^{\mathrm{ES}}\,\mathrm{ES}_\beta(\mathcal L)$ (F021) | integrable tail | Convex programme for linear losses | $\lambda^{\mathrm{ES}}$ is a preference |
| $\inf_{\mathbb Q\in\mathcal P_t}\mathbb E_{\mathbb Q}[\log(W_{t+1}/W_t)]$ (F022) | support restricted so $W_{t+1}>0$ | Robust growth | Radius justification (§4) |
| $-\frac1\varrho\log\mathbb E[\exp(-\varrho(W_{t+1}-W_t)/W_t)]$ (F023) | exponential moments of loss | Risk-sensitive control | Infinite for unbounded losses (fine for long-only unlevered; not for shorts) |

For log-type objectives the incremental value $\Delta J_t(a)$ depends on the **whole existing portfolio** (non-separability);
standalone-trade Kelly fractions are not the incremental optimum.

## 7. Safe action set (Phase 9)

For the single-opportunity case (instrument $i$, $d=+1$):

$$
\mathcal A^{\mathrm{safe}}(x_t):=\Big\{\,n\,\mathbf 1_i:\ n\in\mathbb L_{>0},\ n\le\bar N,\ \alpha_t=1,\ \textstyle\bigwedge_{\Upsilon\in\mathrm{Gates}}\Upsilon(x_t)=1,\ \forall k\in\mathcal K:\ g_k(x_t,n)\le b^{\mathrm{allow}}_k(x_t)\Big\}.
$$
**[F024]**

- If every $g_k$ is non-decreasing in $n$ with $g_k(\cdot,0)=0$, then $\mathcal A^{\mathrm{safe}}=\{n\mathbf 1_i: n\in\mathbb L, 0<n\le Q^{\mathrm{hard}}\}$ (T-03, F096)
  (T-03): the safe set is an initial segment and sizing reduces to computing one number.
- $\mathcal A^{\mathrm{safe}}(x_t)=\varnothing$ ⇒ NO\_TRADE (or RECOVERY if a floor-safety invariant of the *existing* portfolio fails).
  Never an exception, never a fallback guess.
- **Viability interpretation (PROVISIONAL; T-21, T-20a, T-20b).** The tiers of 06 correspond to robust controlled-invariant sets under
  nested disturbance sets (sufficient forms; when no clamp of F144/F145 is active on a pending order the exact one-step condition replaces $K$ by
  $E-F=K+\Lambda$, T-21, F143): $\{R^{\mathrm{open}}+R^{\mathrm{res}}\le K\}$ under tier S, $\{G^{\mathrm{open}}+G^{\mathrm{res}}\le K\}$ under tier G, and
  $\{Z^{\mathrm{open}}+Z^{\mathrm{res}}\le K\}$ (notional plus exit fees; v0.2, AUD-027) under the maximal disturbance set (any path with prices
  $\ge0$, exits impossible). One-step
  invariance is proved for static floors; with ratcheting floors it holds only if a risk-reducing / stop-trailing obligation is
  discharged by an authority outside the engine. Whether the multi-step viability kernel equals these sets is **NOT YET
  PROVEN**.

## 8. Certified advantage over no-trade (Phase 10)

- $\Delta J_t(a):=J_t(a)-J_t(a^{\varnothing})$ **[F025]**; for an ambiguity set, the robust advantage is
  $\inf_{\mathbb Q\in\mathcal P}\big[J_{\mathbb Q}(a)-J_{\mathbb Q}(a^{\varnothing})\big]$ **[F026]** — the **infimum of the difference**, not the
  difference of infima (which is never smaller and can certify a non-robust trade; T-12a, T-12N in 08).
- Candidate certificate (PROVISIONAL, not adopted):
  $\mathrm{LB}_t(a):=\inf_{\mathbb Q\in\mathcal P^{\mathrm{conf}}_{t}}\big[\hat J_{\mathbb Q}(a)-\hat J_{\mathbb Q}(a^{\varnothing})\big]-\varepsilon^{\mathrm{num}}(a)$;
  trade only if $\mathrm{LB}_t(a)>\varepsilon^{\min}$ **[F027]**.

| Error source | Nature | Bound type | Combination rule |
|---|---|---|---|
| Floating-point / series evaluation of $\hat J$ | Deterministic | Interval / directed rounding | Additive: valid (T-12b) |
| Solver sub-optimality | Affects *which* $a$ is proposed, not the validity of a certificate evaluated at the returned $a$ | None needed for safety | Re-evaluate $\hat J$ at the returned $a$ with certified numerics; never trust solver-internal tolerances |
| Sampling / estimation error | Probabilistic | $(1-\delta^{\mathrm{conf}})$ confidence | Union bound or joint confidence set; accumulates across decisions (multiple testing, RQ-15) |
| Model misspecification | Not bounded by sampling theory | Only via $\mathcal P$ (assumption "true law $\in\mathcal P$") | Not additive; if unrepresented the certificate is conditional and MUST say so |
| Cost model error | Fees exact; entry bounded by $p^{\mathrm{lim}}$; exit modelled | Deterministic for fees/entry, modelled for exit | Worst-case where deterministic |

Open issue (RQ-14): with realistic per-trade signal-to-noise, the sample size needed to certify $\Delta J>0$ at useful confidence
may be very large; the certificate may reject almost all trades. That outcome would be a **result**, not a defect.

## 9. Numerical contract (Phase 13)

1. **Domain.** Authority quantities are elements of $\mathbb Q$: integers, and finite decimals parsed from strings. Binary floats
   are rejected at the boundary by type (not by value) — a float-derived decimal is not an authority value
   (`float('0.1')` is $3602879701896397/2^{55}\ne 1/10$; observed).
2. **Arithmetic.** $+,-,\times$ exact. Division exact in $\mathbb Q$, or directed-rounded with the direction fixed per variable.
   In any fixed-precision decimal context the `Inexact` condition MUST be trapped wherever exactness is claimed
   (observed: default 28-digit precision silently rounds large products and sets only a flag).
3. **Directed rounding table.**

| Quantity class | Direction | Reason |
|---|---|---|
| Budgets, capacities, cushions, buying power | toward $-\infty$ | smaller capacity is conservative |
| Losses, costs, consumptions, reservations, open risk | toward $+\infty$ | larger consumption is conservative |
| Quantities | floor to lattice $\mathbb L$ | never exceed a cap |
| Gap exit bound $p^{\mathrm{gx}}$ (F060, long) | toward $-\infty$ | larger loss |
| Carried floor references $H_t$, $\nu^{\mathrm{day}}_0$, $\nu^{\mathrm{wk}}_0$, $\nu^{\mathrm{ref}}$ (when stored at a scale) | toward $+\infty$ | a higher reference raises the floor; rounding $H$ down enlarged $K$ by $9{,}000$ USD at $W=10^8$, $U=3\cdot10^6$ (AUD-045) |
| Units $U_t$ and NAV per unit $\nu_t=W_t/U_t$ | not rounded: exact rationals carried as integer pairs | $U$ raises the floor in F040 and lowers $\nu$ in F037, so no single direction is conservative |
| Reporting / display only | half-even (or half-up) | never fed back into authority |

   Rounding Conservatism (T-24): if every consumption is rounded up and every budget down, the rounded feasible set is a subset of
   the exact feasible set. `ROUND_HALF_UP` on a quantity or budget is **forbidden**: $R=1000.00$, $\ell=2.90$ gives
   half-up $345$ shares with risk $1000.50>1000$ (observed).
4. **Non-rational functions** ($\sqrt{\ }$ in impact models, $\log$ in objectives) are excluded from the hard layer where possible. If
   required, compute a candidate and **certify** it exactly (a candidate $y_2\ge0$ is accepted as an upper bound of $\sqrt{y_1}$ only if
   $y_2^2\ge y_1$ in exact arithmetic **[F028]**). Observed: Python `Decimal.sqrt` and `Decimal.ln` ignore the context rounding mode (floor and ceiling give
   identical results), so directed rounding cannot be obtained by setting the context.
5. **Special values.** NaN, sNaN, $\pm\infty$ and signed zero are rejected at the boundary (grammar of item 17 (a)). `Decimal.min`/`Decimal.max` MUST NOT be
   used: they follow IEEE minNum/maxNum semantics and silently discard a quiet NaN (observed: `Decimal('NaN').max(5) → 5`),
   converting "model failed" into "model imposes no limit". Python's built-in `min` on floats is order-dependent with NaN
   (observed: `min(5.0, nan) → 5.0`, `min(nan, 5.0) → nan`). `Decimal(0).ln()` returns `-Infinity` without signalling (observed).
6. **Magnitude bounds.** $\lvert\text{money}\rvert\le\bar M$, $n\le\bar N$, $p^{\min}\le$ prices $\le p^{\max}$ **[F029]**; precision MUST exceed the
   digits needed for $\bar M$ at the finest scale plus guard digits, else reject.
7. **Comparison.** Exact: a hard check is $g_k(n)\le b^{\mathrm{allow}}_k$ with no tolerance **[F030]**; a check of the form $y\le b_k+\epsilon^{\mathrm{tol}}$
   enlarges the cap and is forbidden.
8. **Float optimiser boundary.** Proposals are floored to $\mathbb L$, clipped to $[0,Q^{\mathrm{hard}}]$, then verified exactly (T-03 part c, F126).
9. **Float division is not safe by default.** Proposition T-22 gives a sufficient condition for the binary64 floor of $R/(\delta_q\ell)$ never to
   exceed the exact floor; outside it an overshoot exists — observed: $R=172{,}808{,}193.53$, $\ell=65.68583269$ ⇒ float floor
   $2{,}630{,}829$ vs exact $2{,}630{,}828$ (one share infeasible).
10. **Serialisation.** Canonical form with every number encoded as a **decimal string** at a declared per-field scale; sorted keys;
    UTF-8; no insignificant whitespace. General-purpose JSON canonicalisation that serialises numbers as IEEE doubles is
    unsuitable. Evidence hash $=\mathrm{hash}(\text{canonical bytes})$.
11. **Reproducibility.** Explicit local numeric context (never the process-global default, which other code can mutate); no
    iteration over unordered sets on the authority path (string hashing is randomised per process); locale-independent
    parsing; timestamps as UTC integers; exchange-calendar day boundaries from versioned reference data.
12. **Parser rules (v0.2, AUD-018).** Snapshots are parsed with a strict parser that rejects the tokens NaN, Infinity and −Infinity and any
    numeral that does not parse exactly to a finite decimal; numbers are parsed as decimals, never as binary floats (common JSON parsers
    accept NaN and Infinity and map 1e400 to ∞ by default — red-team J01–J03). "Parses to a finite decimal" is not enough: the text must also
    match the grammar of item 17 (a), which excludes `-0`, exponents and non-ASCII digits.
13. **Negative zero (one rule, closure AUD-046).** At the boundary a negative zero is **rejected** (items 5, 17 (a)): the field is invalid, so an
    authoritative input gives $\alpha_t=0$, a REQUIRED model output gives $\mathfrak s=0$ and an OPTIONAL one imposes no constraint (F047). Internally,
    exact rationals have no negative zero; a decimal intermediate can produce one (−0 × 5 = −0, red-team Z05) and it MUST be normalised to zero
    before quantisation, comparison output and serialisation, so equal values have identical canonical bytes. F047 maps a finite $y\le0$,
    including an internal $-0$, to $0$.
14. **No mixed-type arithmetic.** Exact types only on the authority path; mixing an exact rational with a binary float silently yields a float
    (red-team X01) and is forbidden.
15. **Money quantisation.** Quantising to the declared cent scale follows the direction table: fees, losses and consumptions round up;
    budgets, capacities and buying power round down; a limit price is never rounded down (red-team HC01–HC04).
16. **Division guard.** Every division on the authority path has a denominator established as non-zero before it is evaluated: a per-share
    loss only after gate G7 has established it is at least $\ell^{\min}p^{\mathrm{lim}}>0$ (red-team T01–T04, I06); $H_t>0$ and $U_t>0$ (F036–F038);
    $\mu^{K}-f^{\mathrm{trd}}\ne0$ where F100 is evaluated. Otherwise the quantity is undefined and the decision is NO\_TRADE (Art. 4).
17. **Canonical numeric rule (normative for every future implementation; Phase-0 closure, AUD-036).**
    (a) *Carrier.* Every authority number in a snapshot, policy file or decision record is a JSON **string**, never a JSON number, whose text
    matches `-?(0|[1-9][0-9]*)` when the field's declared scale `s` is 0 and `-?(0|[1-9][0-9]*)\.[0-9]{s}` (exactly `s` fractional digits)
    when `s > 0`, and which is not a negative zero (`-0`, `-0.00`). Hence no exponent, no leading `+`, no leading zeros, no whitespace, no `NaN`,
    `Infinity` or `-Infinity`. A value with a different number of fractional digits is rejected, never rounded or padded.
    (b) *Parse.* A conforming string becomes an exact rational (integer numerator and denominator) and is checked against $\bar M$ or $\bar N$
    (item 6). Any failure — wrong JSON type, non-conforming text, a non-finite token, out of range — makes the field invalid, so $\alpha_t=0$ and the
    decision is NO\_TRADE naming the field (Art. 4, Art. 18). A JSON parser must be configured to reject non-finite tokens: common defaults accept
    `NaN` and `Infinity` and turn `1e400` into infinity (red-team J01–J03); even a strict decimal parse turns `1e400` into a finite `1E+400`, which
    the grammar and the magnitude bound reject.
    (c) *Arithmetic.* Exact rationals only. Binary floats are rejected by type wherever a value enters the authority path; an exact rational
    never meets a float (a rational plus a float silently yields a float, X01) or a decimal object. If a decimal type is used instead of
    rationals, every operation runs in an explicit local context with InvalidOperation, DivisionByZero, Overflow and Inexact trapped, except at
    declared directed-rounding sites, so no result depends on a global context (a 5-digit context silently rounds 1.23456 to 1.2346).
    (d) *Rounding.* The only rounding on the authority path is directed rounding at declared sites (items 3 and 15): toward $-\infty$ for budgets,
    capacities, buying power, lattice quantities ($\delta_q\lfloor\cdot/\delta_q\rfloor$) and the gap exit bound; toward $+\infty$ for losses, costs, fees,
    reservations, open risk and limit prices. Floor and ceiling have no ties, so half-way values are unambiguous; round-to-nearest (half-up,
    half-even) is for display only and is never fed back.
    (e) *Zero.* Exact rationals have no signed zero; an intermediate decimal $-0$ is normalised to $0$ before any comparison output or serialisation
    (item 13).
    (f) *Serialise.* Output uses grammar (a) at the field's declared scale; the sign `-` appears only for values $<0$. A value not exactly
    representable at the declared scale must pass through its directed-rounding site first; otherwise it is an error, never a silent rounding.
    Keys sorted, UTF-8, no insignificant whitespace (item 10). Equal values therefore have identical bytes (T-14). The per-field scales belong to
    the schema version in $\mathsf v$ and are **UNDEFINED — REQUIRES RESOLUTION** (roadmap R5).
    (g) *Strict document (third review, AUD-036).* Duplicate keys in one object are rejected (a common parser keeps the last one and reads
    `{"cash":"100","cash":"-5"}` as $-5$). Numeric strings use ASCII digits `0`–`9` only: a decimal constructor also accepts `nan`, `-iNfInItY`,
    surrounding whitespace, `1_000` and non-ASCII digits, so the grammar check precedes any library parse. The document is valid UTF-8 and
    contains no lone surrogate escapes.
    (h) *Bytes and hash.* Object keys are ordered by Unicode code point of the key; strings are escaped minimally (only `"`, `\` and control
    characters, as `\"`, `\\`, `\n`-style or `\u00XX`); no insignificant whitespace; the evidence hash is SHA-256 of these bytes; timestamps are
    UTC integer nanoseconds since the Unix epoch, carried as integer strings (scale 0).
    (i) *Runtime-type invariant.* Every value on the authority path is an exact rational at run time. Operations that return a binary float from
    exact operands are forbidden (`Fraction ** Fraction(1, 2)` and `math.sqrt(Fraction(2))` return floats with no float operand); a type
    assertion runs at every directed-rounding site and before serialisation. Non-rational functions go through the certification of item 4.
    (j) *Floor is not truncation.* Lattice and money floors are mathematical floors (toward $-\infty$). Truncation toward zero differs for negative
    operands (decimal integer division gives $-7\,/\!/\,2=-3$ and `Decimal('-0.01') // 1` gives $-0$). Hard budgets are clamped at $0$ (F049) before
    any floor, so a floor never meets a negative operand on the authority path.

## 10. Integration boundary (Phase 19) — requirements only, no schema

The eventual consumer receives $\mathsf{RD}_t$ bound to $\mathrm{hash}(\mathsf S_t)$, the reservation-ledger version and $\mathsf v$.
Requirements: (i) a decision is valid only against the exact snapshot and ledger version it was computed from (consumer
performs compare-and-swap before reserving); (ii) the record contains bounds and reasons, never an instruction or approval
field; (iii) the engine package has no network, broker, credential or persistence dependency (enforced by an import deny-list
check); (iv) absent inputs are never defaulted. The schema is **UNDEFINED — REQUIRES RESOLUTION**.

## 11. Validation doctrine (Phases 15–17) — requirements only

- Every theorem with an executable reading maps to at least one machine-checked invariant (08, column "Testable invariant").
- Test classes: unit, property-based, metamorphic, boundary, fuzz, Monte Carlo, numerical precision, replay determinism,
  adversarial scenario, and **differential** testing against an independent slow reference ("oracle independence").
- Quantitative research: chronological train / validation / test; walk-forward; purging and embargo where labels overlap;
  realistic costs, slippage and gaps; regime analysis; block-bootstrap confidence intervals; parameter sensitivity; multiple-
  testing correction; stress scenarios. Parameters are never selected on the final test sample.
- Primary comparison metrics are **safety metrics** (floor-breach frequency and severity, maximum drawdown, tail loss,
  assumption-violation frequency); growth is compared only between candidates of equal safety. Sharpe, win rate, CAGR or
  backtest P&L alone never promote a formula.
- Baselines (Phase 17): zero trading; fixed one share; fixed-fractional risk; capped stop-risk sizing; fractional Kelly where its
  domain requirements hold; the advanced candidate.
