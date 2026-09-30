# 10 — Alternative Mathematical Architectures Worth Comparing (v0.2-draft)

Every alternative below operates **inside** the same deterministic hard envelope (06) — they differ only in the model and
optimisation layers, except where marked. None is adopted. Comparison protocol: §3. Art. 15 applies: a more complex architecture
must beat the simpler ones on the safety-first metric (RQ-26) under the validation doctrine (01 §11).

## 1. Baselines (Phase 17 — mandatory)

v0.2 (AUD-020): the brief's six baseline names are explicit, and the advanced robust model is a comparison row of its own. Every
baseline's quantity is verified against the envelope by F126; none may exceed $Q^{\mathrm{hard}}$.

| ID | Brief's name | Definition inside the envelope | Formula | Why it is a baseline |
|---|---|---|---|---|
| BL-0 | NO TRADE | $Q^{\mathrm{fin}}=0$ (the action $a^{\varnothing}$) | F142 | the no-trade reference every advantage claim is measured against |
| BL-1 | FIXED ONE SHARE | $Q^{\mathrm{fin}}=\min(\delta_q\lfloor 1\,\mathrm{sh}/\delta_q\rfloor,\ Q^{\mathrm{hard}})$ — one share rounded down to the lattice (v0.2: replaces the ill-formed "$\delta_q\cdot$one share") | F135 | isolates signal quality from sizing |
| BL-2 | FIXED FRACTIONAL RISK | $Q^{\mathrm{fin}}=\min(Q_k,Q^{\mathrm{hard}})$ with $k=$ H1 only | F136 | the conventional practitioner rule |
| BL-3 | CAPPED STOP-RISK SIZING | $Q^{\mathrm{fin}}=Q^{\mathrm{hard}}$ (full envelope, no model layer) | F137 | what the hard layer alone delivers (T-16: also what an expected-value objective delivers) |
| BL-4 | FRACTIONAL KELLY WHERE VALID | $\varpi\,n^{\log}$ floored to $\mathbb L$ and clipped to $Q^{\mathrm{hard}}$, only where the T-19 domain condition ($W^{\min}_{t+1}>0$, F070) holds; otherwise $0$ | F138 | classical growth benchmark; exposes estimation-error sensitivity (RT-17) |
| BL-5 | ADVANCED ROBUST MODEL | $Q^{\mathrm{fin}}=V(\tilde n)$ for the proposal $\tilde n$ of one pre-registered advanced architecture of §2 (AA-4 … AA-10, AA-12) | F126 | the candidate a more complex architecture must be: it is admitted only if it beats BL-0 … BL-4 on the §3 metric (Art. 15) |

## 2. Candidate advanced architectures

| ID | Architecture | Core construct | Assumptions it needs | Guarantee type | Data burden | Main failure mode | Key references (verified — see 11) |
|---|---|---|---|---|---|---|---|
| AA-1 | Cushion-proportional (CPPI / drawdown-surplus) | aggregate risk $\propto K_t$ | A-TRIG (tier S) or A-GAP (tier G) | deterministic under tier assumption | low | gap risk under discrete trading | Black & Perold 1992; Grossman & Zhou 1993; Balder, Brandl & Mahayni 2009 |
| AA-2 | Volatility-targeted sizing | notional $=W_t\sigma^{\mathrm{target}}/\hat\sigma_i$ (F133; v0.2 dimension fix, AUD-031) | volatility forecastability; $\hat\sigma_i>0$ | none beyond envelope | low | $\hat\sigma_i\to0$ (RT-28); regime lag | — (practitioner; literature search task L-2) |
| AA-3 | Fractional Kelly with estimation-error shrinkage | $\varpi n^{\log}$ with shrunk edge | stationary edge; $W^{\min}>0$ | asymptotic growth (only if model correct) | medium | edge overestimation | Kelly 1956; Breiman 1961; MacLean, Ziemba & Blazenko 1992; Thorp 2006 |
| AA-4 | Risk-constrained Kelly | max log growth s.t. drawdown-probability bound (convex restriction) | known return law (or scenarios) | probabilistic (model-conditional) | medium | model misspecification | Busseti, Ryu & Boyd 2016 |
| AA-5 | Distributionally robust growth | $\inf_{\mathbb Q\in\mathcal P}\mathbb E_{\mathbb Q}\log$ | justified ambiguity set; support restriction | robust within $\mathcal P$ | high | radius under heavy tails (A-STAT-02) | Sun & Boyd 2018; Rujeerapaiboon, Kuhn & Wiesemann 2016; Mohajerin Esfahani & Kuhn 2018 |
| AA-6 | Mean–ES / CVaR-constrained | $\max\mathbb E[\Delta W]-\lambda^{\mathrm{ES}}\mathrm{ES}_\beta$ or ES budget | tail estimate at level $\beta$ | coherent risk control (model-conditional) | high (tail samples) | ES estimation variance | Rockafellar & Uryasev 2000, 2002; Acerbi & Tasche 2002 |
| AA-7 | Chance-constrained floor via scenarios | $\mathrm{PB}_t\le\epsilon^{\mathrm{ruin}}$ (F013) with scenario-sample guarantees | i.i.d. scenarios from the right law | probabilistic with sample-size bound | high | scenario law ≠ reality | Calafiore & Campi 2006; Nemirovski & Shapiro 2006 |
| AA-8 | Risk-sensitive control | exponential-of-loss criterion | exponential moments (true for long-only unlevered) | model-conditional | medium | parameter $\varrho$ arbitrary | Howard & Matheson 1972; Whittle 1981; Bielecki & Pliska 1999 |
| AA-9 | Robust / tube MPC with constraint tightening | multi-period plan, constraints tightened by disturbance bounds | bounded disturbances (≈ tier G) | robust constraint satisfaction under bounds | medium | horizon/tightening design | Mayne, Seron & Raković 2005 |
| AA-10 | Viability-kernel / reachability safe set | compute largest invariant subset of $\{W\ge F\}$ | disturbance set; dynamics model | set-invariance (robust or probabilistic) | high (computational) | curse of dimensionality | Aubin 1991; Bertsekas 1972; Abate et al. 2008; Summers & Lygeros 2010 |
| AA-11 | Safety filter / shield around an arbitrary proposer (incl. ML/AI) | any proposer; exact projection onto $\mathcal A^{\mathrm{safe}}$ | correctness of the safe set only | inherits hard-layer guarantee | proposer-dependent | safe set mis-specified | Wabersich & Zeilinger 2021; Alshiekh et al. 2018; Ames et al. 2019 |
| AA-12 | Bayesian decision-theoretic sizing | posterior-predictive expected utility; model averaging | prior; likelihood | coherent under the prior | medium | prior sensitivity | Garlappi, Uppal & Wang 2007 (multi-prior); Hansen & Sargent 2008 (robustness) |

Observations that shape the comparison:
- **AA-11 is the architecture this constitution already is**: the hard layer is a safety filter with exact projection (T-03, F126); every
  other entry is a candidate *proposer* inside it. Its novelty is therefore low (see 11 §3) — the value lies in exactness and the
  tiered-guarantee accounting, not in the filter idea.
- **AA-1 is not merely a throttle choice**: T-21 shows the cushion line is the maximal floor-safe policy under tier S (exactly so on a flat
  book; with held positions the exact condition has slack $\Lambda_t$, OC-1); AA-1 is the
  boundary case of BL-3 with $\mu^{K}=1$.
- **AA-10 may be unnecessary** if OPEN-1 is proved: the tier sets would *be* the viability kernels in closed form.
- AA-4/AA-5/AA-6/AA-7 require a return or gap law; their guarantees are conditional on RQ-12 and RQ-04.

## 3. Comparison protocol (requirements, fixed before any comparison is run)

1. Same opportunity stream, same envelope, same costs, same gap model, same data splits for every candidate.
2. Chronological train / validation / test; walk-forward; purging/embargo; the final test sample is touched once.
3. **Safety-first lexicographic metric (RQ-26):** (i) floor-breach frequency and severity, (ii) assumption-violation frequency by tier,
   (iii) max drawdown and CDaR, (iv) ES of period losses; only among candidates statistically indistinguishable on (i)–(iv), compare
   (v) log growth of unitised NAV, (vi) turnover and cost drag.
4. Block-bootstrap confidence intervals; multiple-testing correction across candidates (White 2000; Hansen 2005;
   Romano & Wolf 2005); deflated performance statistics where Sharpe-type ratios are reported (Bailey & López de Prado 2014).
5. Parameter sensitivity: each candidate's result reported over a pre-registered parameter grid, not at its best point.
6. Stress scenarios: historical crash windows, synthetic gap clusters, liquidity droughts, halts.
7. Decision rule: prefer the simplest candidate not dominated on (i)–(iv) (Art. 15). DeMiguel, Garlappi & Uppal (2009) is the
   cautionary precedent: in portfolio choice, estimation error frequently erases the advantage of optimised over naive rules.
