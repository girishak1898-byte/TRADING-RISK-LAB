# Phase-0 Review — Independent Closure Review of `5c486f0` (CLOSURE-REV registry)

This file is permanent failure evidence. It records that the Phase-0 closure state was wrong, and how the three CRITICAL defects were corrected.
It does not rewrite earlier records: the PASS decision in [08-acceptance-gate.md](08-acceptance-gate.md) §9 is kept as written and is superseded
by this registry (§10 there).

| Field | Value |
|---|---|
| Reviewed diff | `f37c1b612dedcb58d019f0ea5d6204660b814435` .. `5c486f004feb3835a43e40b6970ef3f452adbf73` |
| REVIEWED SHA | `5c486f004feb3835a43e40b6970ef3f452adbf73` |
| PHASE-0 STATUS AT THAT SHA | **NOT PASSED** |
| Findings | CRITICAL 3 (CLOSURE-REV-001, CLOSURE-REV-002, CLOSURE-REV-003) · IMPORTANT 8 (CLOSURE-REV-004 … 011) · MINOR 5 (CLOSURE-REV-012 … 016) |
| Review method | Adversarial review of the diff in the authoring session, with two fresh-context sub-reviewers; every finding reproduced by the author in exact rational arithmetic before classification. Not an organisationally independent review. |
| Superseded record | 08-acceptance-gate.md §9 "PHASE 0 = PASS" at `5c486f0` |

## Status after the critical correction commit

| ID | Severity | Object | Status |
|---|---|---|---|
| CLOSURE-REV-001 | CRITICAL | gates G7, G8 depend on estimates in the wrong direction; T-07, T-08(a) false | **RESOLVED** by the critical correction commit (child of `5c486f0`) |
| CLOSURE-REV-002 | CRITICAL | carried floor references store past estimates | **RESOLVED** by the critical correction commit |
| CLOSURE-REV-003 | CRITICAL | entry fees can disappear depending on when they are booked | **RESOLVED** by the critical correction commit |
| CLOSURE-REV-004 | IMPORTANT | exit-fee catch-up on a partially executed exit order | OPEN |
| CLOSURE-REV-005 | IMPORTANT | exposures protected by several stops | OPEN |
| CLOSURE-REV-006 | IMPORTANT | held vs filled quantity in F144/F145; no guard for $q>n'$ | OPEN |
| CLOSURE-REV-007 | IMPORTANT | H14 cash semantics (F048, remaining-only $C^{\mathrm{res}}$) | OPEN |
| CLOSURE-REV-008 | IMPORTANT | A-EXE-02 falls back to the policy floor on an invalid estimator | OPEN |
| CLOSURE-REV-009 | IMPORTANT | rounding direction of $\nu^{\mathrm{day}}_0$ used as a base; $B^{\mathrm{win}}$ has none | OPEN |
| CLOSURE-REV-010 | IMPORTANT | H3 window base enlarges the cap beyond the claimed double count | OPEN |
| CLOSURE-REV-011 | IMPORTANT | strategy id classed as an order parameter selects the H3 budget | OPEN |
| CLOSURE-REV-012 … 016 | MINOR | T-21 qualifications; canonical bytes; edge-case consistency; lifecycle wording; registry hygiene | OPEN |

T-10 lists CLOSURE-REV-004, 005 and 006 as open dependencies and stays PROOF REQUIRES ADDITIONAL ASSUMPTIONS. No IMPORTANT finding was
hidden by strengthening an unrelated assumption.

## Findings

### CLOSURE-REV-001

| Field | Value |
|---|---|
| Severity | **CRITICAL** — an estimate or a fee could turn NO\_TRADE into TRADE |
| Object | gates G7 and G8 (F092); the restated invariant of 01 Art. 6, F111, 06 §5a; T-08(a) (PROVED) and T-07 |
| Claim at `5c486f0` | "every cap with estimated inputs ≤ the same cap at the policy bounds"; "gates only block"; T-08(a): higher costs never raise $Q^{\mathrm{hard}}$ |
| Counterexample (exact) | **G7:** $p^{\mathrm{lim}}=50$, $p^{\mathrm{stop}}_o=49.99$, $\kappa^{\min}=0.001$, $\ell^{\min}=0.002$, $f^{\mathrm{trd}}B=1{,}000$. At the policy floor $\kappa^{\mathrm{out}}=0.04999$ the per-share loss $0.05999<0.1$: G7 fails, $Q=0$. With $\hat\kappa^{\mathrm{out}}=0.1$: $0.11\ge0.1$, G7 passes, $Q=9{,}090$. **G8 masking:** $100$ sh, mark $48.9$, stop $49$, fee $\max(1,0.005k)$, $N^{\mathrm{ex}}=1$: raw $r^{\mathrm{open}}=-31/10$ at the floor (ANOMALY, $\alpha_t=0$), $+12$ at $\hat\kappa^{\mathrm{out}}=0.2$ (trading reopens). **Fees:** same state, \$1 minimum $-3.1$, \$5 minimum $+4.9$ (falsifies T-08(a)). **Mark below stop:** mark $48.99$, stop $49$, floor $\kappa$: raw $r^{\mathrm{open}}=+59/10$, not flagged. |
| Why it matters | A larger, more pessimistic cost estimate or fee must never reopen trading; G8 is bypassed exactly where A-TRIG is implausible. |
| Required correction | Estimate-free gates; gate metamorphic property; T-07, T-08(a) restated. |
| Resolution | G7 cost clause $p^{\mathrm{lim}}-p^{\mathrm{stop}}_o+\kappa^{\min}p^{\mathrm{stop}}_o\ge\ell^{\min}p^{\mathrm{lim}}$ (the infimum of the sizing per-share loss over all estimates and quantities); G8: $m_{i,t}>p^{\mathrm{stop}}_i$ for every held quantity with a live stop; T-27 (gate monotonicity in estimates, PROVED); T-07 restated (PROOF REQUIRES ADDITIONAL ASSUMPTIONS); T-08 restated (PROVED, narrower statement with its counterexamples recorded). |

### CLOSURE-REV-002

| Field | Value |
|---|---|
| Severity | **CRITICAL** — an estimate enlarged a hard limit through a stored reference |
| Object | $H_t$, $\nu^{\mathrm{day}}_0$, $\nu^{\mathrm{wk}}_0$ (F037, F041) and the units $U_t$ (F069) |
| Claim at `5c486f0` | estimates enter the hard layer only in the conservative direction |
| Counterexample (exact) | $E_u=1{,}000{,}000$, $\hat\Lambda_u=50{,}000$ (policy floor $1{,}000$); later $E_t=990{,}000$, $\Lambda_t=1{,}000$, $d^{\max}=10\%$, $U=1$: $H=989{,}000$, $K_t=98{,}900$ instead of $H=999{,}000$, $K_t=89{,}900$ (+$9{,}000$). Units: $E=10^6$, $\hat\Lambda=50{,}000$, floor $1{,}000$, $U=1{,}000$, withdrawal $95{,}000$ at the estimate-inclusive NAV: $U=900$, $K=45{,}810$; at the reference NAV $U=904{,}000/999$, $K=41{,}400$. |
| Why it matters | A system monotone today that stores a permissive reference for tomorrow is not safe. |
| Required correction | References valued without estimates; temporal monotonicity proved. |
| Resolution | $W^{\mathrm{R}}=E-\Lambda^{\mathrm{floor}}$, $\nu^{\mathrm{R}}=W^{\mathrm{R}}/U$ (F146); $H=\max\nu^{\mathrm{R}}$ (F037); $\nu^{\mathrm{day}}_0,\nu^{\mathrm{wk}}_0=\nu^{\mathrm{R}}$ at the day/week start (F041); $\nu^{\star}=\nu^{\mathrm{R}}$ (F069); $\mathrm{DD}^{\mathrm{R}}$ (F147); T-06c restated; T-28 (instantaneous and temporal dominance, PROVED). |

### CLOSURE-REV-003

| Field | Value |
|---|---|
| Severity | **CRITICAL** — T-10 false inside its stated hypotheses; a realised cost disappears |
| Object | $\phi^{\mathrm{paid}}_o$ (S-296), A-EXE-04, F144, F145, F064, F066, F070, T-10, T-19 |
| Claim at `5c486f0` | no realised cost disappears; T-10 and T-19 hold under their hypotheses |
| Counterexample (exact) | **A:** terminal order, $100$ sh held, buy fee $\max(1,0.005k)$ not yet booked, sell fee $0$, spread $0.01$, mark $50$, stop $49$, $\kappa=0.1$: $W_{t+1}=F_t-\tfrac12$. **B:** $40$ sh, buy fee minimum $5$, sell fee minimum $1$, spread $0.02$, mark $52$: $F_t-3.6$. **C (T-19):** cash $1{,}000$, $10$ sh, exit fee $\max(1,0.005k)$ in two parts at price $0$, owed entry fee $1$: $W^{\min}=998$, $W_{t+1}=997$. **D:** fee of $5$ reported but not booked counted as paid ($q=50$ of $n'=100$ at $50$, buy minimum $5$, sell $0$, spread $0.01$): $F_t-4.75$. **E:** $\phi^{\mathrm{paid}}_o>\phi^{\mathrm{buy}}(q^{\mathrm{fill}}_o)$ credited: charge $13.96\to12.96\to9.96$ for $\phi^{\mathrm{paid}}_o=1,2,5$ ($\phi^{\mathrm{buy}}(2)=1$). |
| Why it matters | The fee appeared zero times — in neither $W$ nor any charge — depending on booking timing. |
| Required correction | Booking-based $\phi^{\mathrm{paid}}$; owed fees reserved until booked, including after the terminal state; domain guard; conservation identity. |
| Resolution | F148 ($\phi^{\mathrm{acc}},\phi^{\mathrm{owed}}$, domain guard with $\alpha_t=0$ and clipping), F149 and T-29 (conservation, PROVED); F144 owed-fee reservation for terminal orders not yet fee-final; A-EXE-04, A-AUTH-02, S-296 restated; fee postings in 05 §1; T-10 and T-19 rebuilt with the booking semantics stated. |

### CLOSURE-REV-004

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Object | sufficient conditions of A-TRIG (04); A-ACC-05 as used by T-19 |
| Counterexample (exact) | stop order for $1{,}100$ sh, $1{,}000$ sold before $\tau_t$ with no exit fee billed; $100$ held at mark $49$, stop $49$, $\kappa=0.1$, fee $\max(1,0.005k)$, spread $0.01$ ($\Lambda=3/2$), $r^{\mathrm{open}}=12=K_t$; the remaining $100$ exit at $48.9$ and the order's cumulative fee $\phi(1100)=11/2$ is billed: $\mathrm{XV}=9769/2<4888$, $W_{t+1}=F_t-2$, while every listed sufficient condition holds; T-19 analogue $W^{\min}-7/2$. |
| Required correction | Carry each working exit order's cumulative quantity and fees booked, or drop the sufficiency claim for partially executed exits. |
| Status | OPEN (T-10 open dependency (i); T-19 open dependency). |

### CLOSURE-REV-005

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Object | single $p^{\mathrm{stop}}_i$ in F145, F072, A-TRIG, while one child stop per fill is contemplated (REV-029) |
| Counterexample (exact) | $n'=200$ at $50$; the $100$ filled carry a child stop trailed to $51$, future fills attach a stop at $49$; mark $52$, $\kappa=0.1$, no fees, $\Lambda=1$: F145 with the held part's stop $110$, worst loss $219$ ($-109$ if $K=110$); with the minimum stop $420$. |
| Required correction | $p^{\mathrm{stop}}_i$ = minimum over every stop protecting any part of the exposure, including future fills; or charge per part. |
| Status | OPEN (T-10 open dependency (ii)). G8 already tests every live stop of a held quantity; the charge is not changed. |

### CLOSURE-REV-006

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Object | quantity semantics of F144 (filled) and F145 (held); no guard for $q>n'$ |
| Counterexample (exact) | after a partial exit while the entry is pending ($n'=200$, $100$ filled, $40$ held, mark $48.95$, stop $49$, $\kappa=0.01$): filled-quantity reading $r^{\mathrm{pf}}=99$, held-quantity reading $162$; breach $-6/5$ under the first. $q=150>n'=100$ with per-share distance $1.1$: price terms $110$ against $165$ for the visible holding. |
| Required correction | Held quantity for the held part, $n'-q^{\mathrm{fill}}$ for the remainder; $\alpha_t=0$ unless held $\le q^{\mathrm{fill}}\le n'$. |
| Status | OPEN (T-10 open dependency (iii)). F148 uses $q^{\mathrm{fill}}_o$ for fees, which is correct under either reading. |

### CLOSURE-REV-007

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Object | F048 $\min(\mathrm{BP},C^{\mathrm{avail}}-C^{\mathrm{res}})$ and the remaining-only $C^{\mathrm{res}}$; $C^{\mathrm{avail}}$ UNDEFINED (RQ-20) |
| Counterexample (exact) | broker figure lower by a hold of $3{,}000$ and not netting open orders: $6{,}000$ allowed against a true $3{,}000$; settled-cash reading of $C^{\mathrm{avail}}$: $7{,}500$ against $4{,}999$. `f37c1b6` was safe under every reading. |
| Status | OPEN — REQUIRES ADDITIONAL ASSUMPTION (netting semantics of $\mathrm{BP}$; trade-date $C^{\mathrm{avail}}$). |

### CLOSURE-REV-008

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Object | 04 A-EXE-02 fail-closed column: "grid check failure ⇒ policy floor only" |
| Finding | survives AUD-041: an invalid estimator yields the most permissive admissible value. T-08(a) and T-27 now assume admissible (load-checked) estimates. |
| Status | OPEN |

### CLOSURE-REV-009

| Field | Value |
|---|---|
| Severity | IMPORTANT (latent until the base $B$ is chosen, RQ-02) |
| Object | 01 §9 item 3 row "carried floor references toward $+\infty$" |
| Counterexample (exact) | $W=10^8$, $U=3\cdot10^6$, $\nu^{\mathrm{day}}_0=100/3$ stored as $33.34$: base B4 $100{,}020{,}000$ instead of $10^8$, H1 budget $+200$. $B^{\mathrm{win}}_s$ has no rounding direction. |
| Status | OPEN. The critical correction changes the valuation of the references (F146), not their rounding. |

### CLOSURE-REV-010

| Field | Value |
|---|---|
| Severity | IMPORTANT (latent: strategy budgets are OFF or NO\_TRADE while SL is undefined) |
| Object | H3 window base $B^{\mathrm{win}}_s$ (F074, F078; AUD-035) |
| Counterexample (exact) | $f^{\mathrm{strat}}=5\%$, $f^{\mathrm{port}}=10\%$, $B^{\mathrm{win}}=100{,}000$: after a $90{,}000$ withdrawal admissible stop risk $500\to1{,}000$; after another strategy loses $60{,}000$, $2{,}000\to4{,}000$; not unitised (against DC-8). |
| Status | OPEN. T-28 requires $B^{\mathrm{win}}_s$, once defined, to be at most its policy-bound value. |

### CLOSURE-REV-011

| Field | Value |
|---|---|
| Severity | IMPORTANT (latent) |
| Object | 06 §5a: the strategy id $s$ classed as an order parameter |
| Finding | $s$ selects which H3 budget applies; a proposer that sets $s$ can route to the strategy with the most headroom. |
| Status | OPEN |

### CLOSURE-REV-012

| Field | Value |
|---|---|
| Severity | MINOR |
| Object | T-21 qualifications |
| Finding | necessity also fails for $\kappa>p^{\mathrm{stop}}$ and for stopless exposures (unattainable bounds); the active-clamp explanation is incomplete (excess also $q(\kappa(n')-\kappa(q))$); "conservative by exactly $\Lambda_t$" (F120, OC-1, 06 §7) is false with an active clamp; (b)/(c) need a one-to-one ledger. |
| Status | OPEN |

### CLOSURE-REV-013

| Field | Value |
|---|---|
| Severity | MINOR |
| Object | 01 §9 item 17 canonical bytes |
| Finding | escaping admits several encodings of a control character; integer-pair carrier for exact $U_t$ unspecified; full-match requirement, FloatOperation trap, inherited local context, complex results of `Fraction**`, `int()` truncation and a pre-parse length cap not stated; 17(j) "a floor never meets a negative operand" is false ($K_t$, $p^{\mathrm{gx}}$). |
| Status | OPEN |

### CLOSURE-REV-014

| Field | Value |
|---|---|
| Severity | MINOR |
| Object | edge-case consistency |
| Finding | an optimiser proposal $2.5$ is floored by item 8/F126 but rejected by item 17; an OPTIONAL model's "-0.00" imposes no constraint; no migration rule for a scale change between schema versions. |
| Status | OPEN |

### CLOSURE-REV-015

| Field | Value |
|---|---|
| Severity | MINOR |
| Object | 08 T-10 (o), acceptance gate §9.5 |
| Finding | "the worst life-of-order loss equals the initial reservation" holds only with the $\tau$-inputs fixed and the stop not widened (an exit-cost estimate rising $0.1\to0.5$ gives $150>110$). |
| Status | OPEN |

### CLOSURE-REV-016

| Field | Value |
|---|---|
| Severity | MINOR |
| Object | registry hygiene |
| Finding | F144/F145 rows omit A-EXE-01…03; $B^{\mathrm{win}}$ classed authoritative in 06 §5a but derived and UNDEFINED in S-295; cluster aggregates must use the current map, not ledger tags; per-execution entry fees ⇒ $\alpha_t=0$ does not say that pending orders fall outside T-10; T-11 does not list A-ACC-03. (The "$440>420$" wording of T-10 (2′) was corrected in the rebuilt proof.) |
| Status | OPEN |

## Regression matrix (exact rational arithmetic)

"Old" evaluates the `5c486f0` formulas, "new" the corrected ones. A row passes when no hard limit is enlarged, no gate turns FAIL into PASS
under a more conservative input, and no floor or $W^{\min}$ is breached. Every old counterexample fails against the old formulas and passes
against the corrected ones (the $\phi^{\mathrm{paid}}_o=1$ row is the valid control case).

| # | Finding | Case | Old (`5c486f0`) | New | Old | New |
|---|---|---|---|---|---|---|
| 1 | 001 | G7, $\kappa$ at floor vs $\hat\kappa^{\mathrm{out}}=0.1$: $Q$ | $0$ vs $9{,}090$ | $0$ vs $0$ | fails | passes |
| 2 | 001 | G8 masking, $\hat\kappa^{\mathrm{out}}$ $0\to0.2$ (mark $48.9$, stop $49$): G8 | FAIL → PASS | FAIL → FAIL | fails | passes |
| 3 | 001 | G8 masking, fee minimum $1\to5$ (T-08(a)): G8 | FAIL → PASS | FAIL → FAIL | fails | passes |
| 4 | 001 | mark $48.99$ below stop $49$: G8 | PASS (raw $+5.9$) | FAIL | fails | passes |
| 5 | 002 | historical $\hat\Lambda$ reference: $(H,K_t)$ | $(989{,}000;\ 98{,}900)$ | $(999{,}000;\ 89{,}900)$ | fails | passes |
| 6 | 002 | withdrawal $95{,}000$: $(U,K)$ | $(900;\ 45{,}810)$ | $(904{,}000/999;\ 41{,}400)$ | fails | passes |
| 7 | 003 | case A, late booking, $100$ sh: $W_{t+1}-F_t$ | $-1/2$ | $+1/2$ | fails | passes |
| 8 | 003 | case B, late booking, $40$ sh: $W_{t+1}-F_t$ | $-18/5$ | $+7/5$ | fails | passes |
| 9 | 003 | case C, T-19: $(W^{\min},W_{t+1})$ | $(998;\ 997)$ | $(997;\ 997)$ | fails | passes |
| 10 | 003 | case D, reported but not booked: $W_{t+1}-F_t$ | $-19/4$ | $+1/4$ | fails | passes |
| 11 | 003 | case E, $\phi^{\mathrm{paid}}_o=1=\phi^{\mathrm{acc}}_o$: (charge, $\alpha_t$) | $(349/25;\ 1)$ | $(349/25;\ 1)$ | passes | passes |
| 12 | 003 | case E, $\phi^{\mathrm{paid}}_o=2>\phi^{\mathrm{acc}}_o$: (charge, $\alpha_t$) | $(324/25;\ 1)$ credit | $(349/25;\ 0)$ | fails | passes |
| 13 | 003 | case E, $\phi^{\mathrm{paid}}_o=5>\phi^{\mathrm{acc}}_o$: (charge, $\alpha_t$) | $(249/25;\ 1)$ credit | $(349/25;\ 0)$ | fails | passes |

## Validation evidence for the corrections (exact; scripts kept outside the repository)

| Property | Search | Old | New |
|---|---|---|---|
| G7 FAIL→PASS under a more conservative estimate | $3$ limits × $5$ stop distances × $15$ ordered estimate pairs | $50$ | $0$ |
| G8 FAIL→PASS under a more conservative estimate or fee | $2$ quantities × $6$ marks × ($6$ estimate pairs × $3$ fee schedules + $3$ fee pairs) | $30$ | $0$ |
| G3/G4 FAIL→PASS or cushion increase, dominating estimate path | $20{,}000$ random four-epoch histories | $6{,}446$ | $0$ |
| Cushion above its policy-bound value at some epoch (temporal, with flows) | $20{,}000$ random five-epoch histories | $13{,}517$ | $0$ |
| T-10 understatement over fee timing (booking at fill, later, after terminal) | $1{,}788$ states, three buy and two sell schedules | $480$ | $0$ |
| T-19 $W_{t+1}<W^{\min}_{t+1}$ over fee timing, prices $\to0$ | $168$ states | $56$ | $0$ |
| T-29 conservation identities | $5{,}000$ event sequences, $60{,}000$ events | — | $0$ violations |
