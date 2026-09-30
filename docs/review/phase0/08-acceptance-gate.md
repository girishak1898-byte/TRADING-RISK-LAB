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
