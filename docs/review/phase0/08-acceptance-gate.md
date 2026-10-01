# Phase-0 Review — Acceptance Gate (brief §13) and Correction Record (brief §14)

Scope: the constitution after the correction commit that adds this file (v0.2), checked against the brief's Phase-0 acceptance gate.
Pre-correction state: [07-mechanical-checks-pre-correction.md](07-mechanical-checks-pre-correction.md).

## 1. Commit chain

| Stage | Commit | Content |
|---|---|---|
| BASELINE | `69a381d` | Phase-0 constitution v0.1 (not modified) |
| Pre-registry corrections | `8198877` | v0.1.1; fixes for REV-001 … REV-024, made before the registry existed (mapped per finding in [01](01-reviewer-finding-registry.md)) |
| REVIEW FINDINGS | `ad1a884` | this directory's registries, red team, audits, pre-correction checker output and the checker; no constitution change |
| CORRECTIONS | the commit adding this file | v0.2; smallest documentation corrections for the confirmed findings (§4) |

The corrections commit cannot record its own SHA; it is reported in the Phase-0 final report and is the child of `ad1a884` in `git log`.

## 2. Acceptance gate

| Criterion (brief §13) | Result | Evidence |
|---|---|---|
| UNREGISTERED_SYMBOLS = 0 | **0** | checker §3 |
| SILENT_DIMENSIONAL_ERRORS = 0 | **0** (DIMENSIONAL_CONFLICTS = 0; the two silent errors found, AUD-031, are corrected) | checker §5; 03 E-18, E-19 |
| UNRECORDED_ASSUMPTIONS = 0 | **0** (43 assumptions, each with one of the seven classes and a fail-closed check or a named "limit" owner; every theorem cites IDs) | checker §3c; 04 |
| UNREVIEWED_THEOREMS = 0 | **0** (46 entries, each with the eight canonical fields, exactly one of the five statuses, and a status consistent with the classes of the cited assumptions) | checker §3b; 08 |
| UNRESOLVED_CRITICAL_REVIEW_FINDINGS = 0 | **0** (CRITICAL: REV-001, 002, 003, 005, 006, 007, 008 corrected in `8198877`; AUD-001, AUD-002 and REV-028 corrected here) | §4, §5 below |
| DUPLICATE_ECONOMIC_COSTS 0 or documented | **documented**: OC-1 … OC-4 (deliberate, conservative); one idempotency item UNRESOLVED with owner (integration contract); 18-row conservation table | 05 §4a, §4b |
| No executable trading code | **met** — the only code file is the documentation linter `tools/doccheck/check_constitution.py` (reads Markdown; no trading logic, no market data, no network) | checker §7: NON_DOCUMENTATION_FILES = 0, FORBIDDEN_IMPORTS = 0 |
| No broker integration | **met** | no such file; forbidden-import check |
| No Alpaca contact | **met** | no network access to any broker host in this session |
| No Trading OS integration | **met** | no reference to, or inspection of, Trading OS code |
| No parameter optimisation | **met** | every value in $\theta$ remains UNDEFINED |
| No backtest-driven formula selection | **met** | no data, no backtest; no final formula adopted |

## 3. Mechanical checker output (after correction)

```
MISSING_DELIVERABLES = 0
UNDEFINED_CROSS_REFERENCES = 0
DUPLICATE_MEANING_SYMBOLS = 0
INCOMPLETE_REGISTRY_ROWS = 0
UNREGISTERED_SYMBOLS = 0
_SHADOWED_LOCAL_SYMBOLS (explicitly namespaced) = 0
THEOREMS_MISSING_FIELDS_OR_STATUS = 0
THEOREM_STATUS_ASSUMPTION_INCONSISTENCIES = 0
UNRECORDED_ASSUMPTIONS = 0
COST_CONSERVATION_TABLE_MISSING = 0
UNTAGGED_EQUATIONS = 0
INCOMPLETE_FORMULA_ROWS = 0
FORMULAS_NOT_REFERENCED_IN_ANY_DOCUMENT = 0
DIMENSIONAL_CONFLICTS = 0
_BIBLIOGRAPHY_TOTAL = 115
BIBLIOGRAPHY_DUPLICATES = 0
NON_DOCUMENTATION_FILES = 0
FORBIDDEN_IMPORTS = 0
GATE_TOTAL = 0
```

**Checker validation (mutation test, run in a scratch copy).** Each of 15 injected defects was detected by the intended count and the
unmodified copy returned `GATE_TOTAL = 0`: a missing theorem field; a status outside the vocabulary ("PROVED BY CONSTRUCTION"); a PROVED
theorem citing a MARKET assumption; an unregistered symbol; a dimensional error in a `dim` expression; the naive `floor(R/ell)`; an
untagged display equation; an untagged `:=` definition; a duplicate registry key; an assumption without a fail-closed check; an undefined
theorem reference; an undefined formula reference; a renamed cost-table column; a code file; a forbidden import.

**Limits of the checker.** It verifies *closure and form*, not truth: it cannot tell whether a proof is correct. Inline equalities are
checked only for `:=`; a heuristic sweep found 110 inline equalities without an ID on the same line — each was reviewed manually and is
a restatement of a registered formula with its ID in the same paragraph, a worked-example parameter assignment, a proof step or a
hypothesis; four were tagged, and one inconsistency found by the sweep was corrected (01 §3, admissibility of decisions: $\mathcal D$ returns a
record whose action component is $a_t$, F006).

## 4. Correction map (file → why → findings)

| File | Why it changed | Findings resolved |
|---|---|---|
| 01 Mathematical Constitution | Art. 6 amendment (hard-layer inputs are frozen, policy-bounded components); §5 T-25 restated with premise and A-TRIG; §3.3 ledger block with $Z^{\mathrm{res}},Q^{\mathrm{res}}$; §7 tier-U set with fees and the T-21 qualification; §9 items 12–16 (parser, $-0$, no mixed types, money quantisation, division guard); formula tags; renames | AUD-002, 003, 007, 009, 010, 018, 025, 027, 032; REV-025, 036 |
| 02 Symbol Registry | full rewrite: every row complete, parameters individually registered, aliases and compound rows marked, proof-local namespaces with scope, new symbols of v0.2 ($\mathrm{XV}$, $q^{\mathrm{rem}}$, $q^{\mathrm{exp}}$, $\mathcal J^{\mathrm{ex}}$, $\phi^{\mathrm{split}}$, $N^{\mathrm{ex}}$, $R^{\mathrm{led}}_o$, $\Lambda^{\mathrm{floor}}$, $\kappa^{\min}$, …); rename map | AUD-006, 007, 008, 009, 023; REV-027, 028, 029 |
| 03 Units / Dimensions | machine-readable `dimtable` linked to registry IDs; E-18 (naive floor), E-19 (volatility target); $\ell^{\min}$ as a fraction of $p^{\mathrm{lim}}$ | AUD-011, 031 |
| 04 Assumption Registry | seven classes; fail-closed column; new A-MATH-01, A-ACC-06, A-ACC-07, A-MKT-06, A-NUM-03, A-AUTH-04, A-AUTH-05, A-EXE-05, A-EXE-06 (widened to triggered-but-unexecuted stops); A-TRIG position-level at the $\tau_t$ inputs with the $N^{\mathrm{ex}}$ sufficient condition; A-EXE-04 on cumulative filled quantity; A-MKT-05 for partial fills | AUD-001, 014, 015, 016, 017, 033; REV-026, 027, 028, 029 |
| 05 Wealth Dynamics | $\Lambda$ composition (A-ACC-06) and floor; OC register OC-1 … OC-4; economic cost conservation table; position-level exit-value bound F072 (three exposure cases) and split envelope F140 over $N^{\mathrm{ex}}+1$ parts, also in F070; add-on numbers under OC-1; formula tags; renames | AUD-001, 007, 010, 012, 022, 033; REV-027, 029, 030, 033, 034, 035 |
| 06 Hard-Safety Architecture | tier table aligned with T-10 and 04; lattice-correct naive form; H15 → H14; input floors F111; reservations re-evaluated (F144); $\mathrm{SL}$ fail-closed rule; consumption/budget wording; G11 in the evaluation order; assumption IDs per constraint; T-21 qualification; formula tags | AUD-002, 004, 005, 010, 016, 025, 026, 028, 031, 032; REV-025, 028, 029, 032, 036 |
| 07 Research Questions | symbol, theorem-ID and assumption references only | AUD-007, 013; REV-036 |
| 08 Theorem Register | canonical eight-field format; split IDs; five-status vocabulary; T-10 proof under the position-level A-TRIG with case 2′ and F144; T-20a with the widened A-EXE-06; T-21 restated and restricted; T-19 with the envelope; T-11 ledger semantics; assumption IDs per entry | AUD-001, 013, 014, 015, 016, 017, 032, 033; REV-025 … REV-036 |
| 09 Failure Modes | F-01 … F-36 re-keyed to RT-01 … RT-36 with formula IDs; FM-NUM-13 … 17, FM-OPS-9, FM-OPS-10, FM-DIM-1, 2 | AUD-018, 021, 031; REV-028, 029 |
| 10 Alternative Architectures | the six baseline names, BL-5 advanced robust model, BL-1 wording, volatility-target formula, A-TRIG wording | AUD-020, 031, 032; REV-025, 036 |
| 11 Literature / Novelty | provenance qualified (subagent-verified, independent re-verification OPEN, L-9); novelty in the five categories | AUD-019, 029 |
| 12 Roadmap, 13 Next Task | review status recorded; exactly one next task kept | AUD-024 |
| 14 Formula Registry (new) | single authority for equations F001 … F144 with the brief's fields and a machine-checked `dim` column | AUD-010, 011; REV-028, 029, 032 |
| README | index with 14 and the review record; status | AUD-030 |
| `docs/review/phase0/01-reviewer-finding-registry.md` | REV-025 … REV-036 appended (second independent review of the correction draft) | — |
| `docs/review/phase0/02-self-audit-finding-registry.md` | AUD-031, AUD-032, AUD-033 appended (found during correction, marked as such) | — |
| `tools/doccheck/check_constitution.py` | formula-registry row scoping; family IDs of split theorems; dimension rules; theorem-field, assumption-class and cost-table checks | — |

Renames (AUD-007, AUD-009): the map is recorded at the end of [02](../../constitution/02-symbol-registry.md).

## 5. Finding status after correction

| Registry | Total | CONFIRMED | REJECTED | Resolved | Remaining (not critical) |
|---|---|---|---|---|---|
| REV (two independent reviewers) | 36 | 36 | 0 | 36 (REV-001 … 024 in `8198877`, residuals continued as AUD-001, 003, 004, 006, 007, 015, 022, 028 and corrected here; REV-025 … 036 corrected here) | 0 |
| AUD (this audit) | 33 | 33 | 0 | 30 fully | AUD-019 bibliography re-verification — OPEN research obligation (L-9; egress blocked here); AUD-028 definition of $\mathrm{SL}$ — UNDEFINED, fail-closed rule in force (06 §4); AUD-012 reservation idempotency — UNRESOLVED, owner: integration contract (05 §4b) |

CRITICAL findings: REV-001, 002, 003, 005, 006, 007, 008, REV-028, AUD-001, AUD-002 — all resolved.

## 6. Central invariant after correction

"Advanced models may reduce permissible action; they may never enlarge deterministic hard limits."

| Channel | v0.2 | Verdict |
|---|---|---|
| Budgets | $b^{\mathrm{allow}}_k=\min(b^{\mathrm{hard}}_k,\mathfrak s(b^{\mathrm{mod}}_k))$ (F049) | holds (T-01) |
| Gates | models may add NO_TRADE conditions only | holds |
| Optimiser proposals | verified by F126 | holds (T-03, T-13) |
| Policy parameters | human-set (Art. 16) | holds |
| Hard-layer inputs ($\kappa^{\mathrm{out}}$, $\Gamma$, $\Lambda$, ADV) | frozen, versioned estimators under human authority, bounded by policy in the conservative direction (F111; 01 Art. 6 amendment); models have no input channel | **holds** (was VIOLATED, AUD-002) — metamorphic test obligation in T-01 |

## 7. Theorem status (08)

PROVED 22 · PROOF REQUIRES ADDITIONAL ASSUMPTIONS 8 (T-06c, T-07, T-10, T-11, T-19, T-20a, T-21, T-25) · DISPROVED 11 (T-01N, T-02N, T-03N,
T-06b, T-09N, T-10N, T-11N, T-12N, T-20b, T-22N, T-24N) · NOT YET PROVEN 4 (T-12c, OPEN-1, OPEN-3, OPEN-4) · UNDEFINED 1 (OPEN-2) · total 46.

## 8. Decision

**PHASE 0 = PASSED** at the documentation level: every gate count is zero, no CRITICAL finding is unresolved, and the remaining open items
are registered research obligations with fail-closed rules or named owners. PASSED does not mean any hard-layer guarantee is
unconditional: every floor theorem is PROOF REQUIRES ADDITIONAL ASSUMPTIONS, and A-STOP / A-TRIG / A-GAP are known to fail in gaps and
halts. The proofs are paper proofs, reviewed by this audit and one independent agent, not mechanised (Art. 14).

## 9. Phase-0 closure (final closure-correction commit)

> **Superseded.** The independent closure review of `5c486f004feb3835a43e40b6970ef3f452adbf73` found PHASE 0 **NOT PASSED** at that SHA
> (3 CRITICAL, 8 IMPORTANT, 5 MINOR; [09-closure-review-registry.md](09-closure-review-registry.md)). The decision of §9.11 and the verdicts
> of §9.3, §9.6 and §9.9 below were wrong at that SHA and are kept as written. The current record is §10.

§1–§8 record the state at `f37c1b6` and are kept as written. Two of their verdicts were wrong at that commit and are superseded here: §6
"hard-layer inputs … holds" (ADV had no policy bound, AUD-040) and §8 "PHASE 0 = PASSED" (a third independent review found two CRITICAL
defects, AUD-039 and AUD-040).

### 9.1 Commit chain

| Stage | Commit | Content |
|---|---|---|
| BASELINE | `69a381dd44da2b0c9feca1f99bc049604a2c622b` | v0.1 (not modified) |
| PRE-REGISTRY ADVERSARIAL CORRECTION | `8198877eed4614ca889187794b0a4e79f1c26c38` | v0.1.1 |
| FORMAL FINDINGS | `ad1a884e631a942067d0c1ec9637fe69e521faf9` | registries, red team, audits, checker |
| CORRECTIONS | `f37c1b612dedcb58d019f0ea5d6204660b814435` | v0.2 (§1–§8 of this file) |
| FINAL PHASE-0 CLOSURE CORRECTIONS | the child of `f37c1b6` | this section; SHA reported in the Phase-0 final report |

History was not rewritten: no amend, squash, rebase or reorder.

### 9.2 What the closure changed

1. **Realised costs charged once** (AUD-034, AUD-035, AUD-038): exact exposure charge F145 for a partially filled order (fees already paid
   excluded); F144 re-evaluates every reservation from the order state (total quantity $n'$, remaining quantity, remaining cost; no ledger
   floor); F048 deducts pending cash once; H3 uses the window-start base; F070 subtracts remaining commitments only. OC-2, OC-3, OC-4
   eliminated; OC-1 kept (future-cost over-charge, proved necessary for T-07).
2. **Third independent review of `f37c1b6`** (16 findings; mapping in [02](02-self-audit-finding-registry.md)): unfilled per-share
   distances clamped at $0$ (AUD-039); $\mathrm{ADV}=\min(\mathrm{ADV}^{\mathrm{est}},\mathrm{ADV}^{\max})$, merge-only statistical cluster maps and the cap invariant
   restated (AUD-040); missing estimate ⇒ $\alpha_t=0$ (AUD-041); stopless exposures in tier S (AUD-042); T-19 hypotheses (AUD-043); undefined
   fail-closed charges replaced by $\alpha_t=0$ (AUD-044); floor references rounded up (AUD-045); one $-0$ rule (AUD-046); hard budgets clamped at
   $0$ (AUD-047); A-TRIG's model component (AUD-048); cross-references and T-06c (AUD-049); terminal = venue-confirmed (AUD-050); strict
   canonical document (AUD-036, upgraded to IMPORTANT). Finding 16 REJECTED with reasons. The manual review (§9.9) found one regression of the
   closure draft itself and restored the rule (AUD-051).
3. **T-21** separated into sufficiency, necessity and equivalence; T-10 case (1′); the 06 §7 linear-throttle "iff" corrected (AUD-037).
4. **Input classification** of every hard cap (06 §5a) and the **canonical numeric rule** (01 §9 item 17).
5. **Checker**: four new gates (theorem fields and status, status–assumption consistency, assumption classes and fail-closed checks,
   cost-conservation table) and a committed mutation suite.

### 9.3 PASS rule

| Condition | Result | Evidence |
|---|---|---|
| GATE_TOTAL = 0 | **0** | §9.8 |
| UNRESOLVED_CRITICAL_FINDINGS = 0 | **0** | CRITICAL: REV-001, 002, 003, 005, 006, 007, 008, 028 and AUD-001, 002 (resolved by `f37c1b6`); AUD-039, AUD-040 (resolved here) |
| Load-bearing theorem statements internally consistent | **yes** (manual review §9.9) | T-10, T-19, T-21, T-25, T-06c restated; statuses unchanged: 22 / 8 / 11 / 4 / 1 |
| No dimensional contradiction | **yes** | DIMENSIONAL_CONFLICTS = 0; F145 and F111 `dim` expressions updated |
| No known cost double count | **yes** | 05 §4b (no realised cost charged twice); OC-1 is a registered, necessary future-cost over-charge, not a realised-cost double count |
| No known risk understatement | **yes** | §9.5 (0 understatements in every enumeration and randomised search) |
| Hard limits cannot be enlarged by model output | **yes** | §9.6 |
| Non-finite numeric states fail closed | **yes** | §9.7 |
| No executable trading functionality | **yes** | only `tools/doccheck/check_constitution.py` and `tools/doccheck/mutation_suite.py` (documentation linters); NON_DOCUMENTATION_FILES = 0, FORBIDDEN_IMPORTS = 0 |

### 9.4 Independent re-derivations (exact arithmetic, this audit; scripts kept outside the repository)

| Object | Result |
|---|---|
| F072 / A-TRIG | Position-level bound re-derived; the summed form in T-10 step (3) follows by A-ACC-04 and G11. Model component named (AUD-048). |
| F140 | Non-decreasing, $\ge\phi$, equal to $\phi$ for linear and super-additive schedules (checked on the lattice to $n=100$). The 05 §5 figures reproduce: $113$, $115$; $4{,}888$ vs $4{,}887$. |
| Partial-exit fee envelope | Exits in up to $N^{\mathrm{ex}}+1$ fee-bearing parts (exit orders plus a remainder at the cut) are covered; one child stop per entry fill needs $N^{\mathrm{ex}}\ge$ number of fills (REV-029). |
| T-10 | Cases (1), (1′), (2), (2′) re-derived; (2) and (2′) now bound $e\,x\le(n'-q)x^+$ for either sign of the per-share distance. |
| T-21 | (a) by summation; (b) by the attained comonotone outcome, valid only with inactive clamps; (c) = (a) + (b), with inactive clamps; (d) F120 sufficient; it coincides with (c) when $\Lambda_t=0$ and is not necessary when $\Lambda_t>0$. |
| OC-4 / full-reservation rule | The full-order reservation beside the held part's open risk over-charges by $q(p^{\mathrm{lim}}-p^{\mathrm{stop}}+\kappa(q))+\phi^{\mathrm{split}}(q)+\phi^{\mathrm{paid}}$ (example: $5.24$, including the paid fee $1$); the remainder-only reservation under-charges ($2.84$ in the same example). F145 is exact. OC-4 eliminated. |
| A-AUTH-05 | Ledger bookkeeping only; the engine does not read ledger reservation values (F144). Terminal = venue-confirmed (AUD-050). |
| Economic cost conservation table (05 §4b) | Each cost appears once: realised costs in $W_t$ through cash; future costs in open risk or reservations; OC-1 is the only registered duplicate (future exit cost against $\Lambda$). |
| Model-controlled inputs | §9.6. |

### 9.5 Exact-arithmetic coverage of fills and costs

All exact (`Fraction`); worst case over every admissible outcome inside T-10's hypotheses; per-order minimum fee $\max(1,0.005k)$ and linear fees;
constant, super-additive and convex $\kappa^{\mathrm{out}}$.

| Case | Enumeration | Result |
|---|---|---|
| Full fill, partial fill, multiple partial fills, remaining open quantity | one exposure, order of $6$ sh, $0$–$6$ filled at $\tau_t$, further fills in the period, marks $49,50,52$, fees paid at once or late, $N^{\mathrm{ex}}=1,2,3$ ($26{,}088$ scenarios, $252$ states) | worst loss $=$ charge $-\Lambda_{i,t}$ in every state (exact, never understated) |
| Split execution and minimum per-order fee | exits in every partition into up to $N^{\mathrm{ex}}+1$ fee-bearing parts | included above; F140 required (without it: $W_{t+1}=F_t-1$, AUD-001, REV-029) |
| Stop trailed to or above the limit | stops $48$–$53$ around limit $50$ ($46{,}200$ scenarios, $1{,}800$ states); randomised ($20{,}000$ trials, $8{,}795$ with stop $\ge$ limit) | clamped charge: $0$ understatements (exact in $1{,}250$ states); unclamped: $1{,}772$ understatements |
| Realised plus remaining (two periods) | reservation at $\tau_0$, partial fills and mark moves, continuation ($1{,}260$ chains) | realised loss plus remaining charge never below the total worst case; the worst life-of-order loss $39/4$ equals the initial reservation |
| Tiers G and U | same grid with the gap and zero-price bounds | exact in all states; F070 closure form: $0$ violations |

**Adversarial split-fill example (05 §5).** Order $6$ sh at limit $50$, stop $49$, $\kappa^{\mathrm{out}}(n)=0.1+0.01n$, fee $\max(1,0.005k)$ per order, $N^{\mathrm{ex}}=2$;
$2$ sh filled (fee $1$ paid), mark $52$, $\Lambda_{i,t}=1.02$. Worst outcome: $4$ more fill at $50$, exits of $2$ and $2$ sh at $49-\kappa^{\mathrm{out}}(6)=48.84$ each paying $1$, remainder
$2$ valued at the cut: loss $12.94$. Charge $r^{\mathrm{pf}}=13.96$, and $13.96-1.02=12.94$: exact. The paid fee ($1$) and the filled shares' entry cost ($100$) are
in $W_t$ and not in $r^{\mathrm{pf}}$, so no realised cost is counted twice; `f37c1b6`'s charge $19.20$ counted them again ($+5.24$), a remainder-only
reservation ($16.80$) understates by $2.84$.

### 9.6 Hard-safety independence

Every input of every cap is classified in 06 §5a. MODEL OUTPUT enters only through $\min((b^{\mathrm{hard}}_k)^+,\mathfrak s(b^{\mathrm{mod}}_k))$ (F049) or as an extra
blocking condition (F027); OPTIMISER OUTPUT only through the verifier F126 ($\le Q^{\mathrm{hard}}$); STATISTICAL ESTIMATES only through $\max$ with a
policy floor (costs) or $\min$ with a policy cap (ADV), and merge-only for clusters; the broker figure only through $\min$ (F048). Each $Q_k$ is
monotone in each estimated input (T-07, T-08), so $Q^{\mathrm{hard}}$ with any estimates $\le Q^{\mathrm{hard}}$ at the policy bounds; a missing estimate gives
$\alpha_t=0$. Randomised exact check (H1, H4, H5, H13, H14; $9{,}000$ trials with arbitrary estimates, invalid and hostile model budgets and
proposals): $0$ violations. Verdict: **no MODEL or OPTIMISER output can enlarge a hard cap; estimates cannot exceed the policy value.**

### 9.7 Numerical red team

| Input | Rule (01 §9) | Outcome |
|---|---|---|
| NaN, sNaN, $\pm$Infinity, `1e400` | grammar 17 (a) and strict parser (item 12) | field invalid ⇒ $\alpha_t=0$ |
| $-0$ | rejected at the boundary; internal $-0$ normalised (item 13) | invalid ⇒ $\alpha_t=0$ / F047 |
| Binary float into exact arithmetic | rejected by type (items 1, 14, 17 (c)) | invalid |
| Fraction → float coercion from exact operands | runtime-type invariant (17 (i)) | forbidden, asserted |
| Non-finite JSON tokens, duplicate keys, non-ASCII digits | strict document (17 (b), (g)) | invalid |
| Decimal context dependence | explicit local context with traps (17 (c)) | no global dependence |
| Rounding ambiguity | directed rounding only, floor not truncation (items 3, 15, 17 (d), (j)); floor references up (AUD-045) | no ties, no half-rounding |

Per-field scales remain **UNDEFINED — REQUIRES RESOLUTION** (R5). Verdict: **every non-finite or ambiguous numeric state fails closed**.

### 9.8 Mechanical checks

Checker: every gate count $0$, `GATE_TOTAL = 0` (16 gates, output as in §3 with `_BIBLIOGRAPHY_TOTAL = 115`). Mutation suite
(`python3 tools/doccheck/mutation_suite.py`): $19$ mutations (18 documentation defects and one code file with a network import), all
detected; the unmodified copy returns `GATE_TOTAL = 0`.

### 9.9 Manual review after automation

Reviewed by hand after the checker reached zero: all CRITICAL findings (REV and AUD); every theorem statement in 08; every "iff" (T-21 (c)
restricted to inactive clamps; 06 §7 cushion row; the linear-throttle row corrected, AUD-037); every floor and ceiling (lattice floors,
directed rounding, floor references); every min/max (F047, F048, F049, F111, F126, F140); the reservation identities (F144, F145, F108, T-11);
the cost-conservation identities (05 §4b, F055–F058, F070); the hard-cap invariants (06 §5a, T-01, T-03). One further defect was found: F145 had dropped the ANOMALY rule that F064 applied to the held part
of a partially filled order ("negative risk frees budget"); restored in 05 §5, G8 and F092 (AUD-051). No other defect found.

### 9.10 Findings

| Registry | Total | CONFIRMED | REJECTED | PARTIALLY CONFIRMED | UNRESOLVED | Severity |
|---|---|---|---|---|---|---|
| REV | 36 | 36 | 0 | 0 | 0 | CRITICAL 8 · IMPORTANT 12 · MINOR 16 |
| AUD | 51 | 51 | 0 | 0 | 2 research obligations (AUD-019, AUD-028), 1 owner item (AUD-012) — none CRITICAL | CRITICAL 4 · IMPORTANT 29 · MINOR 18 |
| Third review (mapped) | 16 | 15 | 1 | 0 | 0 | as mapped in 02 |

### 9.11 Decision

**PHASE 0 = PASS** at the documentation level: every condition of §9.3 holds. This is not a claim that any floor guarantee is unconditional:
every floor theorem is PROOF REQUIRES ADDITIONAL ASSUMPTIONS, A-TRIG / A-GAP fail in gaps and halts, and the proofs are paper proofs checked by
exact enumeration, not mechanised (Art. 14). The closure corrections themselves (AUD-039 … AUD-051) have been verified by this audit only; each
of the three earlier independent reviews found a CRITICAL defect in the state it reviewed.

## 10. Independent closure review and critical corrections

### 10.1 Record

| Field | Value |
|---|---|
| REVIEWED SHA | `5c486f004feb3835a43e40b6970ef3f452adbf73` |
| PHASE-0 STATUS AT THAT SHA | **NOT PASSED** |
| Critical findings | CLOSURE-REV-001, CLOSURE-REV-002, CLOSURE-REV-003 |
| Correction commit | "Fix Phase-0 critical closure defects", the child of `5c486f0` (SHA reported in the final report) |
| Scope of the correction | the three CRITICAL findings only; IMPORTANT and MINOR findings are left OPEN except where a critical repair required a wording or dependency update |

### 10.2 What the correction changed

| Finding | Correction | Proof / evidence |
|---|---|---|
| CLOSURE-REV-001 | G7 cost clause on the policy floor $\kappa^{\min}p^{\mathrm{stop}}_o$; G8 on the mark ($m_{i,t}\le p^{\mathrm{stop}}_i$ fails); ANOMALY rule restated in 05 §5; T-07 and T-08 restated | T-27 (PROVED): no gate turns FAIL into PASS under a more conservative estimate; exact searches $50\to0$ (G7), $30\to0$ (G8) |
| CLOSURE-REV-002 | references valued at $W^{\mathrm{R}}=E-\Lambda^{\mathrm{floor}}$ (F146): $H$, $\nu^{\mathrm{day}}_0$, $\nu^{\mathrm{wk}}_0$, and units issued at $\nu^{\mathrm{R}}$ (F069); $\mathrm{DD}^{\mathrm{R}}$ (F147); T-06c restated | T-28 (PROVED): instantaneous and temporal dominance; $+9{,}000$ regression; $13{,}517\to0$ histories |
| CLOSURE-REV-003 | $\phi^{\mathrm{paid}}$ = fees booked into $W_t$; owed fees reserved until booked, also for terminal orders (F144, F148); domain guard ($\alpha_t=0$, no credit); fee postings in 05 §1; T-10 and T-19 rebuilt | T-29 (PROVED): each fee dollar booked or reserved exactly once; fee-timing enumerations $480\to0$ (T-10), $56\to0$ (T-19) |

Regression matrix: [09-closure-review-registry.md](09-closure-review-registry.md) — 13 exact cases, 12 failing at `5c486f0` (one valid control
case), all passing after the correction.

### 10.3 Status after the correction

| Condition (Phase-0 PASS rule) | Result |
|---|---|
| GATE_TOTAL = 0 | 0 (checker); the checker verifies form, not truth |
| UNRESOLVED CRITICAL findings = 0 | 0 (CLOSURE-REV-001 … 003 resolved) |
| UNRESOLVED IMPORTANT findings | **8 open** (CLOSURE-REV-004 … 011) |
| No known risk understatement | **not met**: CLOSURE-REV-004 (exit-fee catch-up), 005 (several stops), 006 (held vs filled quantity) and 007 (cash semantics) are known understatements under conditions that T-10 now lists as open dependencies |
| Hard limits cannot be enlarged by estimates or model output | met at every epoch for caps, gates and carried references (T-27, T-28); CLOSURE-REV-008 (invalid estimator ⇒ policy floor) and 011 (strategy id) remain open channels in the fail-closed rule and the H3 budget selection |
| Non-finite numeric states fail closed | met; CLOSURE-REV-013 (canonical bytes) open, MINOR |
| No executable trading functionality | met |

### 10.4 Decision

**PHASE 0 = NOT PASSED.** The three CRITICAL findings are resolved; eight IMPORTANT findings remain open and the Phase-0 acceptance
policy does not permit open IMPORTANT mathematical or safety findings.

## 11. CLOSURE-REV-006 correction (held and filled quantities)

### 11.1 Record

| Field | Value |
|---|---|
| Parent SHA | `80ca6935b708a66f3a28fade6de3de2f9fa63562` |
| Correction commit | "Fix Phase-0 held and filled quantity semantics", the child of `80ca693` (SHA reported in the final report) |
| Scope | CLOSURE-REV-006 only. CLOSURE-REV-004, 005, 007 … 011 and the MINOR findings are unchanged. Two defects found during the correction are registered, not corrected: CLOSURE-REV-017 (MINOR), CLOSURE-REV-018 and CLOSURE-REV-019 (IMPORTANT). |

### 11.2 What the correction changed

| Object | Correction | Proof / evidence |
|---|---|---|
| Quantities | held $q_{i,t}$ (S-032), cumulative fill $q^{\mathrm{fill}}_o$ (S-304), order quantity $n'_o$ (S-308), unfilled remainder $q^{\mathrm{unf}}_o=n'_o-q^{\mathrm{fill}}_o$ (S-309) kept apart | share partition: each share of the order is held, exited or unfilled, and in at most one quantity term ($0$ violations in $83$ states) |
| F145 | held part on $q_{i,t}$, pending part on $q^{\mathrm{unf}}_o$, exit cost and exit fees on $\bar q_i=q_{i,t}+q^{\mathrm{unf}}_o$, entry fees $\phi^{\mathrm{buy}}(n'_o)-\phi^{\mathrm{paid}}_o$; conditional on CLOSURE-REV-005 | T-10 (2′) rebuilt; $927{,}900$ exact checks without understatement, attained in all $859{,}900$ clamp-inactive checks |
| F144 | notional, cash and quantity on $q^{\mathrm{unf}}_o$; the owed fee identified separately as a liability of the filled shares | $C^{\mathrm{res}}$ = remainder notional + remainder fees + owed fee in every one of $260{,}100$ lifecycle cuts; exits never change $Q^{\mathrm{res}}$ |
| F150 | validity $0\le q_{i,t}\le q^{\mathrm{fill}}_o\le n'_o$ on the lattice; otherwise $\alpha_t=0$ and a fail-closed charge — the largest of the three F145 components of the virtual state (holding real, whole order still to fill, no fee credit) when every quantity is well formed, otherwise no finite charge (RECOVERY) | $1{,}212$ invalid states, all $\alpha_t=0$; $3{,}981{,}600$ dominance checks, none violated |
| T-10, T-21 | dependency (iii) closed; (i) CLOSURE-REV-004, (ii) CLOSURE-REV-005 kept; (iv) CLOSURE-REV-018 and (v) CLOSURE-REV-019 added (T-19 also lists 019); T-21 mechanical | statuses unchanged (PROOF REQUIRES ADDITIONAL ASSUMPTIONS) |

Regression matrix: [09-closure-review-registry.md](09-closure-review-registry.md) — 14 exact cases (7 valid, 7 invalid); 5 fail against `80ca693`,
all pass after the correction.

### 11.3 Status after the correction

| Condition (Phase-0 PASS rule) | Result |
|---|---|
| GATE_TOTAL = 0 | 0 (checker); the checker verifies form, not truth |
| UNRESOLVED CRITICAL findings = 0 | 0 |
| UNRESOLVED IMPORTANT findings | **9 open** (CLOSURE-REV-004, 005, 007 … 011, 018, 019) |
| No known risk understatement | **not met**: CLOSURE-REV-004 (exit-fee catch-up), 005 (several stops), 007 (cash semantics), 018 (a second non-terminal entry order on one instrument) and 019 (exit fee booked after the cut) |
| Hard limits cannot be enlarged by estimates or model output | unchanged from §10.3 (CLOSURE-REV-008, 011 open) |
| Non-finite numeric states fail closed | met; an invalid or missing quantity now fails closed as well (F150) |
| No executable trading functionality | met |

### 11.4 Decision

**PHASE 0 = NOT PASSED.** CLOSURE-REV-006 is resolved; nine IMPORTANT findings remain open, two of them (CLOSURE-REV-018, 019) found during
this correction.

## 12. CLOSURE-REV-018 correction (entry-order lifecycle exclusivity)

### 12.1 Record

| Field | Value |
|---|---|
| Parent SHA | `8dbb0ee669ad6816062164716e8b19a594754934` |
| Correction commit | "Fix Phase-0 entry-order lifecycle exclusivity", the child of `8dbb0ee` (SHA reported in the final report) |
| Scope | CLOSURE-REV-018 only. CLOSURE-REV-004, 005, 007 … 011, 019 and the MINOR findings are unchanged. No new finding. |

### 12.2 What the correction changed

| Object | Correction | Proof / evidence |
|---|---|---|
| Lifecycle | `NON_TERMINAL` / `TERMINAL_CONFIRMED` / $\bot$ (S-310, S-311, F151); never inferred from quantities; independent of fee finality | regression rows 1, 2, 8–11 |
| G11, A-SCOPE-05 | $q_{i,t}=0\wedge Q^{\mathrm{res}}_{i,t}=0\wedge\mathcal E^{\mathrm{NT}}_{i,t}=\varnothing$ with a valid lifecycle; one entry-order authority per instrument; $\bot$ or two `NON_TERMINAL` entry orders ⇒ $\alpha_t=0$, RECOVERY | $144$-state product: no admission with a non-terminal order or an invalid lifecycle; T-30 PROVED |
| F144, F145, F148, F149 | unchanged in substance; F144/F145 state that the pending order is the instrument's unique `NON_TERMINAL` entry order; a terminal order's owed fee stays in the F144 reservation | $0$ fee dollars lost through the lifecycle (old: $1$); $0$ floor breaches in $96$ exact two-order checks (old: $16$) |
| T-10, T-19 | T-10 dependency (iv) closed, (i), (ii), (v) kept; T-19 unchanged except one counterexample-attempt line | statuses unchanged (PROOF REQUIRES ADDITIONAL ASSUMPTIONS) |

Regression matrix: [09-closure-review-registry.md](09-closure-review-registry.md) — 11 exact cases; 6 fail against `8dbb0ee`, all pass after the
correction; the original counterexample changes from ALLOWED to BLOCKED.

### 12.3 Status after the correction

| Condition (Phase-0 PASS rule) | Result |
|---|---|
| GATE_TOTAL = 0 | 0 (checker); the checker verifies form, not truth |
| UNRESOLVED CRITICAL findings = 0 | 0 |
| UNRESOLVED IMPORTANT findings | **8 open** (CLOSURE-REV-004, 005, 007 … 011, 019) |
| No known risk understatement | **not met**: CLOSURE-REV-004 (exit-fee catch-up), 005 (several stops), 007 (cash semantics) and 019 (exit fee booked after the cut) |
| Hard limits cannot be enlarged by estimates or model output | unchanged from §10.3 (CLOSURE-REV-008, 011 open) |
| Non-finite numeric states fail closed | met; a missing or contradictory entry-order lifecycle now fails closed as well (F151) |
| No executable trading functionality | met |

### 12.4 Decision

**PHASE 0 = NOT PASSED.** CLOSURE-REV-018 is resolved; eight IMPORTANT findings remain open.
