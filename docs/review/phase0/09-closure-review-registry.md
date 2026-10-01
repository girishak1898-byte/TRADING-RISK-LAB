# Phase-0 Review — Independent Closure Review of `5c486f0` (CLOSURE-REV registry)

This file is permanent failure evidence. It records that the Phase-0 closure state was wrong, how the three CRITICAL defects were corrected, and
how CLOSURE-REV-006, CLOSURE-REV-018 and CLOSURE-REV-008 were corrected afterwards.
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
| Later correction commits | `80ca693` resolved CLOSURE-REV-001 … 003; its child "Fix Phase-0 held and filled quantity semantics" resolves CLOSURE-REV-006 and registers CLOSURE-REV-017 (MINOR), CLOSURE-REV-018 and CLOSURE-REV-019 (IMPORTANT), all OPEN; `8dbb0ee`'s child "Fix Phase-0 entry-order lifecycle exclusivity" resolves CLOSURE-REV-018; `a87b887`'s child "Fix Phase-0 estimator failure semantics" resolves CLOSURE-REV-008 and registers CLOSURE-REV-020 (MINOR, OPEN); `a5d40aa`'s child "Close Phase-0 execution and floor-risk defects" (Wave A) resolves CLOSURE-REV-004, 005 and 019 together, in one execution-accounting model (F153–F157, T-32, T-33) |

## Status after the correction commits

| ID | Severity | Object | Status |
|---|---|---|---|
| CLOSURE-REV-001 | CRITICAL | gates G7, G8 depend on estimates in the wrong direction; T-07, T-08(a) false | **RESOLVED** by the critical correction commit (child of `5c486f0`) |
| CLOSURE-REV-002 | CRITICAL | carried floor references store past estimates | **RESOLVED** by the critical correction commit |
| CLOSURE-REV-003 | CRITICAL | entry fees can disappear depending on when they are booked | **RESOLVED** by the critical correction commit |
| CLOSURE-REV-004 | IMPORTANT | exit-fee catch-up on a partially executed exit order | **RESOLVED** by the Wave-A execution and floor-risk correction commit (child of `a5d40aa`) |
| CLOSURE-REV-005 | IMPORTANT | exposures protected by several stops | **RESOLVED** by the Wave-A execution and floor-risk correction commit (child of `a5d40aa`) |
| CLOSURE-REV-006 | IMPORTANT | held vs filled quantity in F144/F145; no guard for $q>n'$ | **RESOLVED** by the held/filled quantity correction commit (child of `80ca693`) |
| CLOSURE-REV-007 | IMPORTANT | H14 cash semantics (F048, remaining-only $C^{\mathrm{res}}$) | OPEN |
| CLOSURE-REV-008 | IMPORTANT | A-EXE-02 falls back to the policy floor on an invalid estimator | **RESOLVED** by the estimator failure correction commit (child of `a87b887`) |
| CLOSURE-REV-009 | IMPORTANT | rounding direction of $\nu^{\mathrm{day}}_0$ used as a base; $B^{\mathrm{win}}$ has none | OPEN |
| CLOSURE-REV-010 | IMPORTANT | H3 window base enlarges the cap beyond the claimed double count | OPEN |
| CLOSURE-REV-011 | IMPORTANT | strategy id classed as an order parameter selects the H3 budget | OPEN |
| CLOSURE-REV-018 | IMPORTANT | G11 admits a second non-terminal entry order on an instrument (found at the CLOSURE-REV-006 correction) | **RESOLVED** by the entry-order lifecycle correction commit (child of `8dbb0ee`) |
| CLOSURE-REV-019 | IMPORTANT | exit fee of an exit executed before the cut and booked after it is charged nowhere (found at the CLOSURE-REV-006 correction) | **RESOLVED** by the Wave-A execution and floor-risk correction commit (child of `a5d40aa`) |
| CLOSURE-REV-012 … 016 | MINOR | T-21 qualifications; canonical bytes; edge-case consistency; lifecycle wording; registry hygiene | OPEN |
| CLOSURE-REV-017 | MINOR | source class of $\phi^{\mathrm{paid}}_o$ (found at the CLOSURE-REV-006 correction) | OPEN |
| CLOSURE-REV-020 | MINOR | existing-portfolio floor check undefined under a missing or invalid $\hat\Lambda$ (found at the CLOSURE-REV-008 correction) | OPEN |

After Wave A, T-10 has no open dependency (004, 005 and 019 are closed by F153–F157; 006 and 018 were closed earlier) and stays PROOF REQUIRES ADDITIONAL
ASSUMPTIONS because its remaining assumptions (A-TRIG, A-STOP, A-STOPLIVE, A-EXE-01…05, A-MKT-05, A-AUTH-02, A-AUTH-04) are world assumptions.
No IMPORTANT finding was hidden by strengthening an unrelated assumption: the Wave-A model charges the registered states more, not less, and
no existing test or theorem was weakened.

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
| Reproduction | Reproduced exactly at `a5d40aa` before any change: charge $r^{\mathrm{open}}=12=K_t$; registered routing (the remaining $100$ exit on the same order, cumulative fee $\phi(1100)=11/2$ billed) loses $14$: $W_{t+1}=F_t-2$; T-19 analogue $W^{\min}-7/2$. Over every admissible routing (the working order continues on part of the shares, the rest through fresh orders) the worst loss is $1599/100$. |
| Resolution | Exit-order fee state $\mathcal X_{i,t}$ (F154: $q^{\mathrm{xf}}_o$, $q^{\mathrm{xr}}_o$, $\phi^{\mathrm{xacc}}_o$, $\phi^{\mathrm{xpaid}}_o$, $\phi^{\mathrm{xowed}}_o$); the owed part is the reservation F157 ($r=g=u=C^{\mathrm{res}}=\Phi^{\mathrm{xowed}}_{i,t}$), the future part the charge $\Phi^{\mathrm{xfut}}_i$ (F155: working-order fee increments plus $\phi^{\mathrm{split}}(\bar q_i)$) inside F064–F066, F145 and F070; conservation F156 (T-32, PROVED); F072 and A-TRIG restated with both terms; OC-5 registered. The registered state is charged $35/2$ (price $10$, owed $5$, increment $\tfrac12$, split $2$) $\ge1599/100$. |
| Status | **RESOLVED** by the Wave-A correction commit (child of `a5d40aa`); T-10 (x), T-19; evidence in the Wave-A regression matrix and validation table below. |

### CLOSURE-REV-005

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Object | single $p^{\mathrm{stop}}_i$ in F145, F072, A-TRIG, while one child stop per fill is contemplated (REV-029) |
| Counterexample (exact) | $n'=200$ at $50$; the $100$ filled carry a child stop trailed to $51$, future fills attach a stop at $49$; mark $52$, $\kappa=0.1$, no fees, $\Lambda=1$: F145 with the held part's stop $110$, worst loss $219$ ($-109$ if $K=110$); with the minimum stop $420$. |
| Required correction | $p^{\mathrm{stop}}_i$ = minimum over every stop protecting any part of the exposure, including future fills; or charge per part. |
| Reproduction | Reproduced exactly at `a5d40aa` before any change: F145 with the held part's stop $110$; worst loss $219$ (the $100$ held exit at $51-0.1$, the $100$ future fills at $50$ exit at $49-0.1$); $W_{t+1}=F_t-109$ at $K_t=110$; with the minimum stop $420$. |
| Resolution | Stop-lots $(q^{\mathrm{lot}}_{i,k},p^{\mathrm{stop}}_{i,k})$ per held position (F153, S-312…S-315): each share charged at the stop of its own lot, shares without a live stop (stale, missing, cancelled, replacement in flight) at tier U, future fills at the pending order's current stop; F064, F065, F145, F072, A-TRIG, A-STOP, A-STOPLIVE, D-06, G8 restated per lot; the one-stop charge is admissible only at the minimum $p^{\mathrm{smin}}_{i,t}$ (T-33, PROVED): both options of the required correction are in the constitution, the per-lot charge as the canonical (exact) form and the minimum-stop charge as a proved conservative aggregate. The registered state is charged $220$, exact. |
| Status | **RESOLVED** by the Wave-A correction commit (child of `a5d40aa`); T-10 (x), T-33; evidence below. |

### CLOSURE-REV-006

| Field | Value |
|---|---|
| Severity | IMPORTANT |
| Object | quantity semantics of F144 (filled) and F145 (held); no guard for $q>n'$ |
| Counterexample (exact) | after a partial exit while the entry is pending ($n'=200$, $100$ filled, $40$ held, mark $48.95$, stop $49$, $\kappa=0.01$): filled-quantity reading $r^{\mathrm{pf}}=99$, held-quantity reading $162$; breach $-6/5$ under the first. $q=150>n'=100$ with per-share distance $1.1$: price terms $110$ against $165$ for the visible holding. |
| Required correction | Held quantity for the held part, $n'-q^{\mathrm{fill}}$ for the remainder; $\alpha_t=0$ unless held $\le q^{\mathrm{fill}}\le n'$. |
| Reproduction | Both counterexamples reproduced exactly before any formula was changed (limit $50$, fee $\max(1,0.005k)$, $N^{\mathrm{ex}}=1$, $\phi^{\mathrm{paid}}_o=1$, spread $0.01$, $\Lambda_{i,t}=6/5$): fill reading $99$, holding reading $162$, worst loss $501/5$, $W_{t+1}-F_t=-6/5$ at $K_t=99$; $q_{i,t}=150$, $n'=100$, mark $=$ limit $50$, stop $49$, $\kappa^{\mathrm{out}}=0.1$: price terms $110$ against $165$. |
| Resolution | Quantities kept apart: S-032 held $q_{i,t}$ (made explicit); S-304 cumulative fill $q^{\mathrm{fill}}_o$ (made explicit; its source class corrected from R to O — it is an authoritative input at the cut); new S-308 $n'_o$ and S-309 $q^{\mathrm{unf}}_o=n'_o-q^{\mathrm{fill}}_o$. F145 rebuilt: held part on $q_{i,t}$, pending part on $q^{\mathrm{unf}}_o$, exit cost and exit fees on $\bar q_i=q_{i,t}+q^{\mathrm{unf}}_o$, entry fees $\phi^{\mathrm{buy}}(n'_o)-\phi^{\mathrm{paid}}_o$; F145 remains conditional on CLOSURE-REV-005. F144: pending-portion terms on $q^{\mathrm{unf}}_o$, the owed fee identified separately as a liability of the filled shares. F150: validity $0\le q_{i,t}\le q^{\mathrm{fill}}_o\le n'_o$ on the lattice, else $\alpha_t=0$ and a fail-closed charge (a finite charge dominating every valid reading when every quantity is well formed; otherwise no finite charge and RECOVERY; never $0$). S-298 / F070 $\bar q_i$; T-10 case (2′) rebuilt and open dependency (iii) removed; T-21 updated mechanically; 05 §5, §7; 06 §5, §5a; 04 A-EXE-03, A-AUTH-02; FM-DC-13. |
| Status | **RESOLVED** by the held/filled quantity correction commit (child of `80ca693`); evidence in the CLOSURE-REV-006 regression matrix and validation table below and in 08 T-10 (viii). F148 uses $q^{\mathrm{fill}}_o$ for fees and is unchanged. |

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
| Reproduction | Reproduced exactly at `a87b887` before any change. H1 with $f^{\mathrm{trd}}B=1{,}000$, limit $50$, stop $49$, $\kappa^{\min}=0.001$ (floor $0.049$), no fees: a valid pessimistic $\hat\kappa^{\mathrm{out}}=0.5$ gives $666$ sh; the estimator failing its grid check, read as the policy floor, gives $953$; with $n^{\min}=700$ the valid estimate gives NO\_TRADE and the failed check TRADE. F111's $\max$ absorbs an out-of-domain $\hat\kappa^{\mathrm{out}}=-0.5$ into the floor ($953$). A failed $\kappa^{\mathrm{liq}}$ check read as $\Lambda^{\mathrm{floor}}=100$: $E_t=100{,}000$, $F_t=96{,}000$, valid $\hat\Lambda=5{,}000$ gives $K_t=-1{,}000$ (G3 fails), the floor $K_t=3{,}900$ (G3 passes). |
| Resolution | Three states per required hard-layer estimate (F152): `VALID` (exists and passes every mandatory check: declared version, instrument and cut, $t^{\mathrm{know}}\le\tau_t$, age within TTL, canonical and finite, declared unit and domain, A-EXE-02 grid check), `MISSING` (no value for the cut), `INVALID` (exists, fails a check). Pipeline raw observation → estimator → validation → policy bound → hard-layer use; the policy bound applies to valid values only; `MISSING` or `INVALID` ⇒ $\alpha_t=0$, no new risk, never the bound, $0$, a last or default value, a model or optimiser value. A-EXE-02, A-LIQ, A-GAP, F111, 01 Art. 6, 06 §5 and §5a, S-214, S-299 restated; T-08 (a) and T-27 stated over valid estimates only; the failure rule is the separate theorem T-31 (PROVED); T-28 unchanged (carried references contain no estimate); FM-OPS-14; checker gate ESTIMATOR_FAILURE_NOT_FAIL_CLOSED. Existing exposures stay under the floor and RECOVERY rules (see CLOSURE-REV-020). |
| Status | **RESOLVED** by the estimator failure correction commit (child of `a87b887`); evidence in the CLOSURE-REV-008 regression matrix and validation table below and in 08 T-31. |

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

### CLOSURE-REV-017

| Field | Value |
|---|---|
| Severity | MINOR |
| Object | 02 S-296 $\phi^{\mathrm{paid}}_o$, source class R |
| Finding | class R means "realised only in $(\tau_t,\tau_{t+1}]$, not $\mathcal F_t$-measurable", but $\phi^{\mathrm{paid}}_o$ at the cut is an authoritative order-state input (06 §5a). Found while making S-304 canonical for CLOSURE-REV-006; S-304 had the same class and was corrected there because it is one of the quantities that finding defines. |
| Status | OPEN |

### CLOSURE-REV-018

| Field | Value |
|---|---|
| Severity | IMPORTANT — under the per-instrument reading of F145, T-10's conclusion fails inside its stated hypotheses |
| Object | gate G11 and A-SCOPE-05 (test $Q^{\mathrm{res}}_{i,t}=0$); F144, F145, F150, written for one non-terminal entry order per instrument |
| Counterexample (exact) | entry order $o_1$ for $100$ fully filled but not yet venue-confirmed terminal, entry fee $\max(1,0.005k)$ owed and not booked, every share exited: $q_{i,t}=0$ and $Q^{\mathrm{res}}_{i,t}=q^{\mathrm{unf}}_{o_1}=0$, so G11 admits $o_2$ for $100$ on the same instrument; $o_2$ fills fully (fee $1$ booked), $100$ held, mark $52$, stop $49$, limit $50$, $\kappa^{\mathrm{out}}=0.01$, sell fee $0$, spread $0.01$ ($\Lambda_{i,t}=1/2$). One F145 for $i$ with $o_2$ charges $301$ against a worst loss of $603/2$ — the owed fee $1$ of $o_1$ is charged nowhere: $W_{t+1}=F_t-\tfrac12$ at $K_t=301$. Evaluated per order instead, the held part is charged twice: conservative at mark $52$, but at mark $48.95$ (sell fee $\max(1,0.005k)$, $\Lambda_{i,t}=3/2$) the sum is $2$ below the exact worst case. |
| Required correction | G11 to require that no non-terminal entry order exists on $i$ (not only $Q^{\mathrm{res}}_{i,t}=0$), or F144, F145 and F150 defined per instrument over all of its non-terminal entry orders. |
| Origin | Found while correcting CLOSURE-REV-006 and not corrected there; pre-existing at `80ca693`, whose F144 also gave $Q^{\mathrm{res}}=n'-q^{\mathrm{fill}}=0$ for a fully filled order. |
| Reproduction | Reproduced exactly at `8dbb0ee` before any change: the old G11 admits $o_2$; one F145 for $i$ (with $o_2$) $301$, worst loss $603/2$, $\Lambda_{i,t}=1/2$, $W_{t+1}=F_t-\tfrac12$. |
| Authority error | $Q^{\mathrm{res}}_{i,t}=0$ (no unfilled quantity on $i$) was taken for "no pending entry order on $i$". A fully filled order awaiting its terminal confirmation has $q^{\mathrm{unf}}_o=0$ yet is still the instrument's pending entry order: it carries the owed fee, can still receive execution corrections, and owns the instrument's F145. |
| Resolution | Lifecycle states `NON_TERMINAL`, `TERMINAL_CONFIRMED`, and $\bot$ for missing, ambiguous or contradictory evidence (S-310, S-311, F151), independent of fee finality. G11: $q_{i,t}=0\wedge Q^{\mathrm{res}}_{i,t}=0\wedge\mathcal E^{\mathrm{NT}}_{i,t}=\varnothing$ with a valid lifecycle; $\bot$ or two `NON_TERMINAL` entry orders on one instrument ⇒ $\alpha_t=0$ and no finite charge for that instrument (RECOVERY), no order chosen as authoritative. A-SCOPE-05 (one entry-order authority per instrument) and A-AUTH-02 restated; F144 and F145 keep one pending entry order per instrument; a terminal order's owed fee stays in the F144 reservation (CLOSURE-REV-003 rule) and does not block G11. T-30 (gate lifecycle monotonicity, PROVED); T-10 open dependency (iv) closed. T-19: the overlapping state had also made $\bar q_i$ in F070 ambiguous ($W_{t+1}=W^{\min}_{t+1}-\tfrac12$ under one reading); the same gate excludes it, T-19's statement and dependencies are unchanged. FM-OPS-13. |
| Status | **RESOLVED** by the entry-order lifecycle correction commit (child of `8dbb0ee`); evidence in the CLOSURE-REV-018 regression matrix and validation table below and in 08 T-10 (ix), T-30. |

### CLOSURE-REV-019

| Field | Value |
|---|---|
| Severity | IMPORTANT — T-10's conclusion fails inside its stated hypotheses |
| Object | A-EXE-04 (fees may be booked after an order is terminal) applied to **exit** orders; F144 and F148 reserve the owed fees of entry orders only; T-10, T-19 |
| Counterexample (exact) | $100$ sh held, stop $49$; the stop sells all $100$ at $48.9$ before $\tau_t$ and the exit order is terminal; its sell fee $\max(1,0.005k)=1$ is not yet booked at the cut. Nothing is held or pending, so $R^{\mathrm{open}}_t=R^{\mathrm{res}}_t=0\le K_t=\tfrac12$; the fee is booked in the period: $W_{t+1}=W_t-1=F_t-\tfrac12$. |
| Required correction | the exit-side analogue of F148 (owed exit fees reserved until booked, for terminal and for working exit orders, the latter together with CLOSURE-REV-004), or exit fees required to be booked at the cut ($\alpha_t=0$ otherwise). |
| Reproduction | Reproduced exactly at `a5d40aa` before any change: $R^{\mathrm{open}}_t=R^{\mathrm{res}}_t=0\le K_t=\tfrac12$ with a fee of $1$ owed; $W_{t+1}=F_t-\tfrac12$; T-19 analogue $W^{\min}-1$. |
| Resolution | The exit-side analogue of F148: F154 ($\phi^{\mathrm{xowed}}_o=\phi^{\mathrm{xacc}}_o-\phi^{\mathrm{xpaid}}_o$ until fee-final; terminal confirmation does not zero it) and the reservation F157 on every instrument with an exit order not fee-final, held or not; conservation F156 (T-32). The registered state carries a reservation of $1>K_t$, so F120 fails. Found with CLOSURE-REV-004 in one model, as required. |
| Status | **RESOLVED** by the Wave-A correction commit (child of `a5d40aa`); T-10 (x), T-19; evidence below. |

### CLOSURE-REV-020

| Field | Value |
|---|---|
| Severity | MINOR — advisory output only; no admission effect |
| Object | F034 and the existing-portfolio floor conditions F120–F122 (RECOVERY, 01 Art. 4) when $\hat\Lambda_{i,t}$ is not `VALID` |
| Finding | With $\hat\Lambda_{i,t}$ `MISSING` or `INVALID`, $W_t=E_t-\Lambda_t$ — hence $K_t$ and $\mathrm{DD}_t$ — is undefined. New risk is blocked ($\alpha_t=0$, F152), but the constitution does not say whether the existing-portfolio floor check then reports RECOVERY, evaluated at the A-ACC-05 worst case $\Lambda_{i,t}\le q_{i,t}m_{i,t}+\phi^{\mathrm{sell}}_{i,0}(q_{i,t})$, or only NO\_TRADE; evaluating it at $\Lambda^{\mathrm{floor}}$ would overstate $K_t$ ($E_t=100{,}000$, $F_t=96{,}000$, liquidation cost $5{,}000$: $K_t=3{,}900$ instead of $-1{,}000$). Found while correcting CLOSURE-REV-008, whose scope is new-risk admission. |
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

## CLOSURE-REV-006 regression matrix (exact rational arithmetic)

Base: limit $50$, stop $49$, $\kappa^{\mathrm{out}}=0.01$, buy and sell fee $\max(1,0.005k)$ per order, $N^{\mathrm{ex}}=1$, spread $0.01$,
$\phi^{\mathrm{paid}}_o=\phi^{\mathrm{acc}}_o$, mark $48.95$ unless stated; quantities $(n',q^{\mathrm{fill}}_o,q_{i,t})$. "Old" is the `80ca693` F145 with its one
quantity symbol read as the holding (as written in F145) and as the fill (as written in F144). $W_{t+1}-F_t$ is the worst outcome with $K_t$ equal
to the charge (T-10's premise with equality, no new order); the worst loss is the largest loss over every outcome inside T-10's hypotheses (further
fills $0\ldots q^{\mathrm{unf}}_o$ at the limit, maximal entry fees, exit at the F072 bound). A valid row passes when $W_{t+1}\ge F_t$. An invalid row passes
when $\alpha_t=0$ and the charge is not below the visible holding's own charge; no worst loss is defined there (the state is outside T-10).

| # | Case | G8 | Worst loss | Old, holding reading: charge ($W_{t+1}-F_t$) | Old, fill reading: charge ($W_{t+1}-F_t$) | New | Old | New |
|---|---|---|---|---|---|---|---|---|
| 1 | $q_{i,t}=q^{\mathrm{fill}}_o=n'$: $(200,200,200)$ | fail | $-8$ | $-6$ ($+2$) | $-6$ ($+2$) | $-6$ ($+2$) | passes | passes |
| 2 | $q_{i,t}<q^{\mathrm{fill}}_o<n'$, partial exit after partial entry fill (Case A): $(200,100,40)$ | fail | $501/5$ | $162$ ($+309/5$) | $99$ ($-6/5$) | $507/5$ ($+6/5$) | fails | passes |
| 3 | $q_{i,t}=0<q^{\mathrm{fill}}_o<n'$: $(200,100,0)$ | n/a (nothing held) | $103$ | $204$ ($+101$) | $99$ ($-4$) | $103$ ($0$) | fails | passes |
| 4 | $q_{i,t}<q^{\mathrm{fill}}_o=n'$: $(200,200,40)$ | fail | $-4/5$ | $162$ ($+814/5$) | $-6$ ($-26/5$) | $2/5$ ($+6/5$) | fails | passes |
| 5 | $q^{\mathrm{fill}}_o=0$: $(200,0,0)$ | n/a | $205$ | $205$ ($0$) | $205$ ($0$) | $205$ ($0$) | passes | passes |
| 6 | partial exit after partial entry fill, mark $52$: $(200,100,40)$ | pass | $1111/5$ | $284$ ($+309/5$) | $404$ ($+909/5$) | $1117/5$ ($+6/5$) | passes | passes |
| 7 | full fill followed by partial exit: $(200,200,150)$ | fail | $-23/4$ | $93/2$ ($+209/4$) | $-6$ ($-1/4$) | $-4$ ($+7/4$) | fails | passes |
| 8 | $q_{i,t}>q^{\mathrm{fill}}_o$, mark $52$: $(200,100,150)$ | pass | — (holding's own charge $907/2$) | $505$ | — | $\alpha_t=0$; $3{,}560{,}899/200$ | passes | passes |
| 9 | $q^{\mathrm{fill}}_o>n'$, mark $52$: $(200,250,100)$ | pass | — (holding's own charge $303$) | $405$ | — | $\alpha_t=0$; $3{,}040{,}949/200$ | passes | passes |
| 10 | $q_{i,t}>n'$ (Case B): $(100,100,150)$, mark $50$, $\kappa^{\mathrm{out}}=0.1$, no fees | pass | — (holding's own charge $165$) | $110$ | — | $\alpha_t=0$; $12{,}500$ | fails | passes |
| 11 | $q^{\mathrm{fill}}_o$ missing | — | — | undefined | — | $\alpha_t=0$; no finite charge (RECOVERY) | — | passes |
| 12 | $q_{i,t}=40.5$, off the lattice | — | — | undefined | — | $\alpha_t=0$; no finite charge (RECOVERY) | — | passes |
| 13 | $q_{i,t}=-10$ | — | — | undefined | — | $\alpha_t=0$; no finite charge (RECOVERY) | — | passes |
| 14 | $n'=-200$ | — | — | undefined | — | $\alpha_t=0$; no finite charge (RECOVERY) | — | passes |

Every old failure of a valid row is the fill reading; it needs the held per-share term to be negative (mark below the stop less the exit cost),
where G8 already blocks new risk while the cushion accounting is understated — except row 3, where nothing is held, G8 does not apply and the
understatement reaches the budgets with $\alpha_t=1$. The holding reading never under-charged a valid state (it charged exited shares again as
future fills) but under-charged row 10, with the mark above the stop and $\alpha_t=1$.

## CLOSURE-REV-006 validation evidence (exact; scripts kept outside the repository)

| Property | Search | Old (`80ca693`) | New |
|---|---|---|---|
| Valid states: charge $-\Lambda_{i,t}$ below the worst loss (T-10) | every valid $(n',q^{\mathrm{fill}}_o,q_{i,t})$ with $n'\le6$ ($83$ states) × $5$ marks × $6$ stops × $5$ $\kappa^{\mathrm{out}}$ schedules (one above the stop price) × $5$ fee schedules (one a percentage fee) × $N^{\mathrm{ex}}\in\{1,2\}$ × $3$ booking levels × tiers S, G, U: $927{,}900$ checks | $106{,}128$ (fill reading); $0$ (holding reading) | $0$ |
| Clamp-inactive checks in which the charge is attained (T-21 (b)) | same | — | $859{,}900$ of $859{,}900$ |
| $W_{t+1}<F_t$ at $K_t$ = charge in the seven required categories (partial entry fill, partial exit, $q_{i,t}<q^{\mathrm{fill}}_o$, $q^{\mathrm{fill}}_o=n'$, $q_{i,t}=0$ after fills, remainder $>0$, full fill then reduced holding) | $35{,}000$ random trials, $n'\le150$, random limits, stops, marks, ten $\kappa^{\mathrm{out}}$ schedules | $53$ (fill reading) | $0$ |
| Invalid states with $\alpha_t\neq0$ | $1{,}212$ states (missing, off the lattice, $q_{i,t}<0$, $q^{\mathrm{fill}}_o<0$, $n'\le0$, $q_{i,t}>q^{\mathrm{fill}}_o$, $q^{\mathrm{fill}}_o>n'$, $q_{i,t}>n'$) | no guard | $0$ ($883$ with no finite charge) |
| F150 charge below the same tier's charge of a valid reading, the visible holding's own charges or the reported fill's fee | $329$ states with a finite charge, $3{,}981{,}600$ checks | — | $0$ (the tier-U component alone: $10{,}056$) |
| Conservation: share partition, $Q^{\mathrm{res}}$ under exits and fills, committed entry cash, F149, owed fee kept, booked fee not repeated | $83$ states; $20{,}000$ random lifecycles, $260{,}100$ cuts | exited shares in a quantity term in $56$ of $83$ states under either reading; an exit raises $Q^{\mathrm{res}}$ from $100$ to $160$ under the holding reading | $0$ violations; no valid lifecycle state flagged invalid |

## CLOSURE-REV-018 regression matrix (exact)

Instrument $i$: limit $50$, stop $49$, $\kappa^{\mathrm{out}}=0.01$, spread $0.01$, $N^{\mathrm{ex}}=1$; $o_1$, $o_2$ for $100$ sh each; entry fee $\max(1,0.005k)$, sell
fee $0$, mark $52$. "Old" is G11 at `8dbb0ee` ($q_{i,t}=0$, $Q^{\mathrm{res}}_{i,t}=0$); "new" adds $\mathcal E^{\mathrm{NT}}_{i,t}=\varnothing$ with a valid lifecycle (F151).
$W_{t+1}-F_t$ is the worst outcome with $K_t$ equal to the charge. A row passes when the gate admits no new entry while a `NON_TERMINAL` entry
order or an invalid lifecycle exists on $i$ (A-SCOPE-05, F151), and no admitted state leaves $o_1$'s owed fee outside every charge.

| # | Case | Old G11 | New G11 | New entry (new) | $o_1$'s fee liability: old → new | Old | New |
|---|---|---|---|---|---|---|---|
| 1 | original REV-018: $o_1$ fully filled, `NON_TERMINAL`, fee $1$ owed, nothing held; $o_2$ for $100$ fills and is held | ALLOWED | BLOCKED | no | one F145 for $i$ (with $o_2$) $301$ against $603/2$: $W_{t+1}-F_t=-1/2$, fee in no charge → $o_1$'s own F145 $=1$ carries it | fails | passes |
| 2 | fully filled `NON_TERMINAL`, $q^{\mathrm{unf}}_{o_1}=0$, fee booked (owed $0$) | ALLOWED | BLOCKED | no | none owed; $o_1$ keeps the slot | fails | passes |
| 3 | fully filled `TERMINAL_CONFIRMED`, owed $0$ | ALLOWED | ALLOWED | yes | none owed; after $o_2$ fills $301$ against $601/2$: $+1/2$ | passes | passes |
| 4 | `TERMINAL_CONFIRMED`, fees not final (owed $1$) | ALLOWED | ALLOWED | yes | F144 terminal reservation $1$; after $o_2$ fills $302$ against $603/2$: $+1/2$ | passes | passes |
| 5 | two `NON_TERMINAL` entry orders observed on $i$ ($o_1$ as in row 1, $o_2$ filled) | ALLOWED (no rule) | $\alpha_t=0$ | no | one F145 for $i$ drops $o_1$'s fee ($-1/2$) → no finite charge for $i$ (RECOVERY), both obligations kept | fails | passes |
| 6 | nothing held, `NON_TERMINAL`, $60$ filled, $40$ unfilled, owed $1$ | BLOCKED | BLOCKED | no | $o_1$'s F145 $=207/5$ | passes | passes |
| 7 | $40$ held, `NON_TERMINAL`, owed $1$ | BLOCKED | BLOCKED | no | $o_1$'s F145 $=607/5$ | passes | passes |
| 8 | full fill (epoch $t$), terminal confirmation at $t+1$, owed $1$ | ALLOWED / ALLOWED | BLOCKED / ALLOWED | no / yes | at $t+1$ F144 terminal reservation $1$; after $o_2$ fills $302$ against $603/2$ | fails | passes |
| 9 | terminal confirmation (epoch $t$, owed $1$), fees final at $t+1$ | ALLOWED / ALLOWED | ALLOWED / ALLOWED | yes / yes | reservation $1$, then $0$ with the fee booked in $W$ (F149, T-29) | passes | passes |
| 10 | lifecycle state of $o_1$ missing, $q_{i,t}=0$, $Q^{\mathrm{res}}_{i,t}=0$ | ALLOWED | $\alpha_t=0$ | no | — | fails | passes |
| 11 | $o_1$ marked terminal while the venue reports it active | ALLOWED | $\alpha_t=0$ | no | — | fails | passes |

## CLOSURE-REV-018 validation evidence (exact; scripts kept outside the repository)

| Property | Search | Old (`8dbb0ee`) | New |
|---|---|---|---|
| New entry admitted; admitted with a `NON_TERMINAL` entry order on $i$; admitted with an invalid lifecycle; an owed fee left outside every charge | Boolean product: $q^{\mathrm{unf}}_{o_1}$, terminal confirmation, owed fee, holding each zero or not; $0$, $1$, $2$ non-terminal entry orders; evidence consistent, missing or contradictory: $144$ states ($120$ invalid) | $54$; $36$; $44$; $9$ | $4$; $0$; $0$; $0$ |
| Same lifecycle, $q^{\mathrm{unf}}_{o_1}>0\to0$: BLOCKED → ALLOWED (T-30) | $36$ pairs | $18$ | $0$ |
| Fee representation changed by $q^{\mathrm{unf}}$ alone | $144$ states | — | $0$ |
| $W_{t+1}<F_t$ after admission (two fee schedules; $o_1$ $60$ or $100$ filled, terminal or not, owed $0$ or $1$; marks $48.95$, $52$; $o_2$ fills $0$, $50$, $100$, fee booked or not) | $144$ old, $96$ new exact checks | $16$ (down to $-1$) | $0$ (minimum $0$) |
| Fee dollar neither booked nor reserved through the lifecycle (full fill → entry decision → terminal confirmation → fees final) | $9$ old, $7$ new order-cuts | $1$ | $0$ |
| T-19 in the overlapping state ($\bar q_i$ of F070 read with the fully filled order) | $1$ exact case | $W_{t+1}=W^{\min}_{t+1}-\tfrac12$ | state excluded by G11 |

## Wave-A regression matrix (CLOSURE-REV-004, 005, 019; exact rational arithmetic)

One instrument. "Old" is the `a5d40aa` charge (one stop per exposure — the held part's live stop, else the pending order's stop; one exit-fee allowance
$\phi^{\mathrm{split}}(\bar q_i)$; no exit-order state). "Worst" is the largest loss over every further entry fill $e\le q^{\mathrm{unf}}_o$ and every admissible exit routing
(working-order continuations, cancellations, up to $N^{\mathrm{ex}}$ fresh orders, a remainder at the cut), each lot exiting at its own stop bound, unprotected
shares at $0$, every owed fee booked in the period. "New" is the Wave-A charge (F064/F145 per lot with $\Phi^{\mathrm{xfut}}$, plus F157). "Min" is the one-stop
charge at $p^{\mathrm{smin}}_{i,t}$ (T-33; "—" when a part is unprotected). A row passes when charge $-\Lambda_{i,t}\ge$ worst. Prices: mark $50$ and stop $49$ unless
stated; $\kappa^{\mathrm{out}}=0.1$; exits at $48.9$; fee $\max(1,0.005k)$ per order unless stated; $N^{\mathrm{ex}}=1$ unless stated; $\Lambda_{i,t}=0$ except rows A ($3/2$) and B ($1$).

| # | Case | Old | Worst | New | Min | Old | New |
|---|---|---|---|---|---|---|---|
| A | CLOSURE-REV-004 registered state: working stop order, $1{,}000$ of $1{,}100$ sold before the cut, nothing booked; $100$ held at mark $49$ | $12$ | $14$ (registered routing), $1599/100$ (any routing) | $35/2$ | $35/2$ | fails | passes |
| B | CLOSURE-REV-005 registered state: held lot $(100,51)$, future fills $(100,49)$, mark $52$, no fees | $110$ | $219$ | $220$ (exact) | $420$ | fails | passes |
| C | CLOSURE-REV-019 registered state: terminal exit order, $100$ sold, fee $1$ unbooked, nothing held | $0$ | $1$ | $1$ (exact) | $1$ | fails | passes |
| D | working exit order for $100$, nothing executed yet, $100$ held | $112$ | $113$ | $113$ (exact) | $113$ | fails | passes |
| E | partially executed exit: $60$ of $100$ sold, fee $1$ booked, $40$ held | $46$ | $46$ | $46$ (exact) | $46$ | passes | passes |
| F | full exit before the cut, terminal, fee final (nothing owed) | $0$ | $0$ | $0$ | $0$ | passes | passes |
| G | full exit before the cut, terminal, fee reported but not booked; percentage fee $0.1\%$ | $0$ | $489/100$ | $489/100$ (exact) | $489/100$ | fails | passes |
| H | two working child-stop orders, $30$ of $50$ and $20$ of $50$ sold, $50$ held in two lots; $N^{\mathrm{ex}}=2$ | $58$ | $60$ | $60$ (exact) | $60$ | fails | passes |
| I | split execution: $N^{\mathrm{ex}}=2$, $100$ held, no exit order | $113$ | $113$ | $113$ (exact) | $113$ | passes | passes |
| J | minimum-plus-percentage fee $\max(1,\ 0.05\%$ of notional$)$, executed part at $48.9$, the lifetime bound and the split envelope at the mark $50$ (F155); executing exit order, $50$ of $100$ executed, nothing booked | $2289/40$ | $593961/10000$ | $23879/400$ (OC-5 and the mark reference) | $23879/400$ | fails | passes |
| K | flat per-order fee, terminal exit order with fee unbooked, $100$ still held | $112$ | $113$ | $113$ (exact) | $113$ | fails | passes |
| L | child stop trailed to $51$ above the pending limit $50$, order stop $49$, $100$ unfilled, mark $52$, no fees | $110$ | $220$ | $220$ (exact) | $420$ | fails | passes |
| M | replacement stop in flight on one lot ($\bot$), other lot at $49$; $50+50$ held, no fees | $110$ | $2{,}555$ | $2{,}555$ (exact) | — | fails | passes |
| N | missing stop on the pending order's future fills; held lot at $49$, $100$ unfilled at limit $50$, no fees | $220$ | $5{,}110$ | $5{,}110$ (exact) | — | fails | passes |
| O | different child stops $(60,49.5)$, $(40,48)$; $\kappa^{\mathrm{out}}=0.1+0.01q$; tiered fee; $N^{\mathrm{ex}}=2$ | $261$ | $321$ | $321$ (exact) | $411$ | fails | passes |
| P | partial exit while the entry is pending with an executing exit order: $n'=200$, $100$ filled, $40$ held, $60$ sold on a working order of $100$, mark $48.95$, buy fee $1$ booked, $N^{\mathrm{ex}}=2$ (lot stop and order stop) | $115$ | $116$ | $116$ (exact) | $116$ | fails | passes |
| Q | review cycle 1 (B-1/C-5): four lots of $100$ at $49$, each its own stop order, flat fee $1$, $N^{\mathrm{ex}}=1$, $\Lambda=1$ | $442$ | $443$ | $445$ ($\alpha_t=0$; one fee part per stop order) | $445$ | fails | passes |
| R | review cycle 1 (C-5): three lots of $1$ sh, $\max(1,0.005k)$, $N^{\mathrm{ex}}=1$ | $53/10$ | $63/10$ | $63/10$ ($\alpha_t=0$) | $63/10$ | fails | passes |
| S | review cycle 1 (C-1/A-1): terminal exit order, $100$ sh sold at $60$, fee $0.1\%$ of proceeds unbooked, mark $50$, nothing held | $5$ (fee at the mark) | $6$ | $6$ (fee on executed proceeds) | $6$ | fails | passes |
| T | review cycle 1 (C-4): terminal exit order, fee $1$ confirmed final by the broker but unbooked, nothing held | $0$ (released by the flag) | $1$ | $1$ (released only by a booking) | $1$ | fails | passes |
| U | review cycle 1 (A-3): executing stop order for $100$, nothing executed, fees marked final; lot $(100,49)$, mark $50$, $\max(1,0.005k)$, $N^{\mathrm{ex}}=1$ | $112$ (order dropped from $\mathcal X$) | $113$ | $113$ | $113$ | fails | passes |
| V | review cycle 1 (C-3): two executing orders each for the whole holding of $100$ | $114$ (finite) | unbounded (short) | RECOVERY, no finite charge | — | fails | passes |
| W | review cycle 3 (R3-1): one lot of $20$ at stop $50$, $\kappa^{\mathrm{out}}=0.1$ (bound $49.9$), mark $49.89$, fee $0.05\%$ of notional, $N^{\mathrm{ex}}=1$ | $2989/10000$ (negative lot term, fee at the mark) | $299/1000$ | $1/2$ (lot term clamped at $0$, fee at $p^{\mathrm{fee}}=50$) | $1/2$ | fails | passes |
| X | re-run enumeration after R3-1: $1$ sh still to fill at limit $50$ with stop $48$ (bound $47.9$), mark $47.5$, fee $0.1\%$, terminal exit order owing its fee, $\Lambda=\tfrac12$ | $2.2453$ (fee at the mark) | $1.7457$ (plus $\Lambda$) | $11229/5000$ (fee at $p^{\mathrm{fee}}=50$) | $11229/5000$ | fails | passes |

## Wave-A validation evidence (exact; scripts kept outside the repository)

Model (re-run at review cycle 1 with every lot its own stop order, accrued fees on executed proceeds, confirmed-but-unbooked fees kept owed,
contradictory exit remainders excluded as RECOVERY): one instrument; held $0$–$3$ stop-lots (three-lot states sampled, $400$ of $5{,}832$ combinations;
stops $48$–$51$, $\bot$ for a stale, missing or replacement-in-flight stop); a pending entry order of $0$–$4$ sh with $0$–$4$ filled at limit $50$ and stop
$48$–$51$ or $\bot$; exit orders none, executing ($0$–$3$ executed, $1$–$2$ remaining) or terminal, fees booked or not, fee-final or not; marks
$48.95$–$52$; fee schedules zero, $\max(1,0.005k)$, flat, percentage, minimum-plus-percentage, capped percentage and tiered (super-additive), the
executed part of an executing order at $48.9$, $50$ or $51.3$ (at, or above, the mark reference, review cycle 2); $\kappa^{\mathrm{out}}$ constant and
super-additive; $N^{\mathrm{ex}}=1,2$ ($365{,}964$ states have more stop orders than $N^{\mathrm{ex}}$: $\alpha_t=0$, charged with one fee part per stop order). The worst loss is the maximum over every further fill
$e\le q^{\mathrm{unf}}_o$ (comonotone) and every admissible exit routing, in exact rationals.

| Property | Search | Old (`a5d40aa`) | New |
|---|---|---|---|
| Charge $-\Lambda$ below the worst loss (T-10 understatement) | $519{,}750$ enumerated states | $379{,}252$ | $0$ |
| Per-lot charge exact (equal to the worst loss) | $285{,}944$ states without the pending order's clamp in which every order of $\mathcal X_{i,t}$ has nothing left to execute; $11{,}149$ states with a quantity-only schedule and no clamp at all in a dedicated enumeration | — | $83{,}455$; $11{,}149$ of $11{,}149$ quantity-only, clamp-free (lot clamps and the fee reference price over-charge the rest) |
| One-stop charge at $p^{\mathrm{smin}}$ below the per-lot charge (T-33) | $308{,}353$ states with every part protected | — | $0$ |
| Adversarial multi-stop search: understatement | $5{,}165$ randomised trials (child stop trailed above the limit $1{,}793$; replacement in flight $1{,}801$; stale $1{,}805$; missing $1{,}754$; different child stops $2{,}077$; partial exit $2{,}396$; partial fill $2{,}708$) | $3{,}487$ | $0$ |
| Same: $p^{\mathrm{smin}}$ charge below the per-lot charge | same | — | $0$ |
| Exit-fee conservation (F156, T-32: (a)–(e) after every event) | $4{,}000$ random event sequences, $60{,}000$ events (executions, bookings of none, part or all of the owed fee, terminal and fee-final events, six fee schedules) | — | $0$ violations |
| $W_{t+1}<W^{\min}_{t+1}$ with prices $\to0$ (T-19) | $2{,}650$ randomised trials (stop-lots, pending orders, working and terminal exit orders, late bookings) | registered states: $W^{\min}-7/2$, $W^{\min}-1$ | $0$ ($2{,}275$ equal) |
| Checker gate EXIT_FEES_OR_STOP_LOTS_NOT_CHARGED | constitution at `a5d40aa` (gate added at Wave A, extended at review cycle 1) / after the correction | $9$ | $0$ |
| Mutation suite | $39$ mutations ($9$ added at Wave A) | — | all detected |
| Independent review, cycle 1 (three fresh-context reviewers on the Wave-A diff: counterexample, proof, accounting/authority) | $19$ findings: $0$ CRITICAL, $9$ IMPORTANT (B-1/C-5, B-2, B-3, B-4/A-7, C-1/A-1, C-2, C-3, C-4, A-2, A-3), $10$ MINOR; every accepted finding reproduced exactly by the lead before correction (rows Q–V) | — | all corrected in the same commit (F153 $K_{i,t}\le N^{\mathrm{ex}}$; F154 membership, executed proceeds, confirmed-but-unbooked fees, RECOVERY on contradictory remainders, unprotected non-stop remainders; S-298 $\bar q_i=n$; T-10, T-19, T-21, T-29, T-32, T-33 restated); reviewer A's exhaustive search ($587{,}664$ states, $\le2$ lots, $N^{\mathrm{ex}}\le3$) found no $W_{t+1}<F_t$ inside T-10's hypotheses |
| Independent review, cycle 2 (two fresh-context reviewers on the corrected diff: counterexample/accounting, proof/consistency) | proof review: $5$ IMPORTANT (exit-side fee bound stated as accrued fee plus the schedule's increment, R2B-1; "not fee-final" wording replaced by "not booked in full", R2B-2; $0\le\kappa^{\min}<1$ registered for T-33 with the Lipschitz step, R2B-3; an executing order that is not a lot's stop ⇒ RECOVERY, R2B-4; T-32 (d) and F156 bounded by the accrued fee plus the increment, execution clauses before the final confirmation, R2B-5) and $7$ MINOR, all corrected in the same commit; T-10, T-19, T-21, T-29, T-32, T-33 accepted as written after the corrections; no weakening against `a5d40aa`. Counterexample/accounting review: $1$ CRITICAL (R2-1: for a proceeds-dependent, non-linear schedule the increment of the schedule at a reference price understated the fee accrued on shares executed above it — lot of $20$ remaining of a triggered stop order with $40$ executed at $50$, lot of $22$ resting, mark $50$, $\max(1,0.05\%)$ of notional, $N^{\mathrm{ex}}=2$: charge $5067/100$ against a loss of $50{,}689/1{,}000$, $W_{t+1}=F_t-19/1000$; corrected by the lifetime bound $\phi^{\mathrm{xlife}}_o$ on the combined notional, S-327, F155: $507/10$), $2$ IMPORTANT (a final confirmation applied to an order still executing, R2-2 — now ignored while $q^{\mathrm{xr}}_o>0$; T-32 (d)/(e) and F156 restated on $\phi^{\mathrm{xlife}}_o$, R2-3), $3$ MINOR (row J's price convention, $N^{\mathrm{ex}}$ wording, residual "not fee-final" wording), all reproduced by the lead and corrected; the registered rows A–V re-verified by the reviewer | — | $0$ open |
| Independent review, cycle 3 (one fresh-context reviewer on the exit-fee bound, after the two automatic cycles) | $1$ CRITICAL (R3-1: with a lot's stop bound above the mark the fee reference at the mark fell short of the fee at the exit price while the lot's price term was negative — $20$ sh, stop $50$, $\kappa^{\mathrm{out}}=0.1$, mark $49.89$, fee $0.05\%$ of notional: charge $2989/10000$ against a loss of $299/1000$, $W_{t+1}=F_t-1/10000$; corrected by clamping each held lot's distance at $0$ in F064, F065, F145, as F145 already did for future fills, and by evaluating proceeds-dependent fees at $p^{\mathrm{fee}}_{i,t}$, the mark or the exposure's highest stop (S-328; the clamp alone still failed for a future fill whose stop bound lies above the mark, $1.7453$ against $1.7457$, found by the re-run enumeration): $1/2$), $1$ IMPORTANT (R3-2: a final confirmation applied to a fully executed `NON_TERMINAL` order left its F155 term non-zero; the term is now $0$ whenever $q^{\mathrm{xr}}_o=0$), $2$ MINOR ($\phi^{\mathrm{xlife}}_{o,0}$ defined; row J reproduces); the exit-fee bound otherwise found sound (executed parts above, at and below the mark; minimum reached by the executed part; $q^{\mathrm{xf}}_o=0$; cancelled orders; $K=N^{\mathrm{ex}}$; capped and tiered schedules; terminal orders). **These corrections were reproduced by the lead and mechanically verified (checker, mutation suite, re-run enumeration with marks below every stop bound) but not independently re-reviewed: the two automatic correction/re-review cycles were exhausted — see the Wave-A commit record** | — | $0$ open, $1$ pending independent re-review |

## CLOSURE-REV-008 regression matrix (exact)

H1 alone: $f^{\mathrm{trd}}B=1{,}000$, limit $50$, stop $49$, $\kappa^{\min}=0.001$ (policy floor $\kappa^{\min}p^{\mathrm{stop}}=0.049$), no fees; $n^{\min}=0$ except in row I.
"Old" is the `a87b887` rule set (F111 missing ⇒ $\alpha_t=0$; 01 §9 items 5, 17 for non-finite fields; A-EXE-02's fallback to the policy floor on a
failed grid check; F111's $\max$ on any number). A row passes when every `MISSING` or `INVALID` status gives $\alpha_t=0$ and no failed estimator
yields a larger quantity than the valid pessimistic estimate.

| # | Case | Raw status | Validated value | Bounded value | $\alpha_t$ | Admission (new) | Old (`a87b887`) | Old | New |
|---|---|---|---|---|---|---|---|---|---|
| A | valid estimate above the floor ($0.5$) | `VALID` | $0.5$ | $0.5$ | $1$ | $666$ sh, TRADE | $666$, TRADE | passes | passes |
| B | valid estimate exactly at the floor ($0.049$) | `VALID` | $0.049$ | $0.049$ | $1$ | $953$ sh, TRADE | $953$, TRADE | passes | passes |
| C | valid estimate below the floor before bounding ($0.01$) | `VALID` | $0.01$ | $0.049$ | $1$ | $953$ sh, TRADE | $953$, TRADE | passes | passes |
| D | missing estimate | `MISSING` | — | — | $0$ | NO\_TRADE | $\alpha_t=0$ (F111) | passes | passes |
| E | estimator fails its load-time grid check (fitted $0.5$ up to $700$ sh, $0.3$ above) | `INVALID` | — | — | $0$ | NO\_TRADE | policy floor: $953$, TRADE | fails | passes |
| F | stale estimate (age $>$ TTL) | `INVALID` | — | — | $0$ | NO\_TRADE | no stated rule ($666$ if used as valid, $953$ by the A-EXE-02 analogy) | fails | passes |
| G | non-finite estimate (NaN) | `INVALID` | — | — | $0$ | NO\_TRADE | $\alpha_t=0$ (01 §9) | passes | passes |
| H | wrong estimator version or provenance | `INVALID` | — | — | $0$ | NO\_TRADE | no stated rule ($666$ or $953$) | fails | passes |
| I | valid pessimistic $0.5$ vs failed check, $n^{\min}=700$ | `VALID` / `INVALID` | $0.5$ / — | $0.5$ / — | $1$ / $0$ | NO\_TRADE / NO\_TRADE | NO\_TRADE / TRADE ($953$) | fails | passes |
| X1 | out of domain ($\hat\kappa^{\mathrm{out}}=-0.5$) | `INVALID` | — | — | $0$ | NO\_TRADE | F111 $\max$: $0.049$, $953$, TRADE | fails | passes |
| X2 | wrong unit (basis points read as USD/sh) | `INVALID` | — | — | $0$ | NO\_TRADE | no stated rule | fails | passes |
| X3 | wrong instrument | `INVALID` | — | — | $0$ | NO\_TRADE | no stated rule | fails | passes |
| X4 | wrong cut ($t^{\mathrm{know}}>\tau_t$) | `INVALID` | — | — | $0$ | NO\_TRADE | not admitted (F003) ⇒ missing, $\alpha_t=0$ | passes | passes |

## CLOSURE-REV-008 validation evidence (exact; scripts kept outside the repository)

Model: caps H1 ($f^{\mathrm{trd}}B=1{,}000$), H2 ($\mu^K K_t$, $\mu^K=0.1$), H5 (gap budget $2{,}000$), H12 ($\rho^{\mathrm{in}}w^{\mathrm{in}}=0.01$, $\mathrm{ADV}^{\max}=10^6$), gate G3
with $E_t=100{,}000$, $F_t=96{,}000$, $\Lambda^{\mathrm{floor}}=100$; four estimators $\hat\kappa^{\mathrm{out}},\hat\Gamma,\hat\Lambda,\mathrm{ADV}^{\mathrm{est}}$, each valid (above, at or on the
permissive side of its bound), missing, or invalid in nine ways (stale, non-finite, outside its domain low or high, wrong unit, instrument or
cut, failed grid or load check, failed version).

| Property | Search | Old (`a87b887`, explicit rules) | New |
|---|---|---|---|
| States with a missing or invalid estimate admitted ($\alpha_t=1$) | $28{,}561$ status combinations, $28{,}480$ with a missing or invalid estimate | $544$ ($12{,}019$ if unstated cases are read through F111's bound) | $0$ |
| A value substituted after a failed check | same | A-EXE-02 floor; F111 $\max$/$\min$ | $0$ |
| Single-estimator degradation `VALID` → `MISSING`/`INVALID`: $Q^{\mathrm{hard}}$ larger; NO\_TRADE → TRADE; TRADE → TRADE; G3 FAIL → PASS | $263{,}640$ pairs ($n^{\min}=0$) | $376$; $200$; $1{,}660$; $250$ | $0$; $0$; $0$; $0$ |
| Same with $n^{\min}=300$ | $263{,}640$ pairs | $256$; $256$; $656$; $250$ | $0$; $0$; $0$; $0$ |
| Valid domain (T-08, T-27, T-28): a more conservative valid estimate raises $Q^{\mathrm{hard}}$ or turns G3 FAIL → PASS; $Q^{\mathrm{hard}}$ above its policy-bound value | $625$ valid points, $2{,}000$ ordered pairs | — | $0$; $0$; $0$ |
| Carried references ($H$, units) differ because of an estimator status | $20{,}000$ random five-epoch histories with flows | — | $0$ (T-28: NO CHANGE) |
| Checker gate ESTIMATOR_FAILURE_NOT_FAIL_CLOSED | constitution at `a87b887` / after the correction | $6$ | $0$ |
