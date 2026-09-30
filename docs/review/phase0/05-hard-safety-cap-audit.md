# Phase-0 Review — Hard-Safety Cap Audit (brief §7)

Scope: 06 at `8198877`. For each cap the audit asks: mathematically defined? monotone in the intended direction? bounded? redundant?
double-counted? independent of or correlated with another cap? Monotonicity directions: non-increasing in candidate size n is **not** the
question (all consumptions are non-decreasing in n by A-EXE-01/02); the question is the direction of the *cap* Q_k with respect to
wealth W (should not decrease when W rises), costs (should not rise when costs rise), liquidity (should not fall when liquidity rises),
open/reserved risk (should not rise when they rise).

| Brief cap | Constraint(s) | Defined? | Monotone (W ↑ / cost ↑ / liquidity ↑ / open risk ↑) | Bounded? | Redundancy | Double counting | Correlated with |
|---|---|---|---|---|---|---|---|
| risk (per trade) | H1 | **modulo** B (UNDEFINED, RQ-02) and κ^out (UNDEFINED, RQ-05) | ↑ / ↓ / ↑ / n.a. — correct (T-05, T-08, T-07 after OC-1) | yes: G7 gives per-share loss ≥ ℓ^min > 0 ⇒ Q ≤ f·B/ℓ^min; also N̄ | dominated whenever another R-family term is smaller (collapsed into R^hard by min — harmless) | none | identical consumption L^stop with H2, H3, H4, H10 |
| notional | H7 (order), H11 (gross) | modulo B | ↑ / n.a. / n.a. / ↓ — correct | yes | under G11, H8 reduces to n·p^lim ≤ f^conc·B, so exactly one of H7, H8 is redundant (whichever fraction is larger); H11 overlaps H14 in a cash account | none | H7, H8, H9, H11, H14 share consumption n·p^lim |
| liquidity | H12 (entry), H13 (exit) | modulo ADV estimator (E-class; AUD-002 requires a frozen definition) | n.a. / n.a. / ↑ / n.a. — correct | yes (ADV finite) | under G11 both are n ≤ const·ADV; one is redundant (larger of ρ^in·w^in and ρ^ex·h^ex) | none | both linear in ADV |
| buying power | H14 | modulo C^avail (UNDEFINED, RQ-20) | ↑ (consistent cash perturbation) / ↓ / n.a. / ↓ — correct | yes | overlaps H11 | **possible**: broker BP may already net open orders while H14 subtracts C^res (conservative; to register as OC-2) | H11 |
| margin | H15 | **NOT DEFINED** — excluded by D-02 | — | — | — | — | — |
| portfolio | H2 (stop), H5 (gap), H11 (gross) | modulo B, Γ | ↑ / ↓ / ↑ / ↓ — correct | yes | H2 vs H4 (binding one depends on f^port·B vs μ_K·K); H5 vs H6 likewise | OC-1 (no Λ credit) inside R^open, G^open — registered conservative | H4, H10 |
| correlation | H9 (cluster notional), H10 (cluster risk) | modulo cluster map (RQ-10) | ↑ / ↓ / ↑ / ↓ — correct | yes | H10 redundant if f^clr ≥ f^port (admissibility requires ≤); single-member cluster ⇒ H9 = H8 | none; aggregation is comonotone (sum), no diversification credit (T-18) | H2, H8 |
| daily loss | H4 via F^day (also H5, H16) | modulo calendar (RQ-31) and RQ-32 | ↑ / ↓ / ↑ / ↓ — correct | yes | subsumed in the single cushion K | none | all floors share K |
| weekly loss | H4 via F^wk | as daily | as daily | yes | as daily | none | as daily |
| strategy loss | H3 | **NOT DEFINED** — SL_{s,t} UNDEFINED (RQ-11); fail-closed rule missing (AUD-028) | as H2 once defined | — | — | realised strategy loss reduces B (through W) and is subtracted again as SL (second-order, conservative; to register as OC-3) | H2 |
| drawdown | H4 via F^dd; gate G4 | yes (given H observation set, RQ-03) | ↑ / n.a. / n.a. / ↓ — correct | yes | G4 is redundant with K ≤ 0 when F^dd is in the max — intentional defence in depth | none | all floors |
| gap (not in brief) | H5, H6 | modulo Γ (UNDEFINED calibration) | as H2 | yes | H5 vs H6 | none (DC-3: disjoint from stop distance within one budget family) | H2 via shared positions |
| concentration (not in brief) | H8 | modulo B | ↑ / n.a. / n.a. / ↓ | yes | see notional | none | H7 |
| unconditional floor (optional) | H16 | defined (pending orders at full L^abs after REV-003) | ↑ / ↓ / n.a. / ↓ | yes | dominates H5 at Γ = 1 | none | H5 |

## Central invariant

"Advanced models may reduce permissible action; they may never enlarge deterministic hard safety limits."

| Channel | At `8198877` | Verdict |
|---|---|---|
| Budgets | b^allow = min(b^hard, sanitised b^mod) for every k (Art. 5) | holds (T-01) |
| Gates | models may add NO_TRADE conditions; cannot remove hard gates | holds |
| Optimiser proposals | floored, clipped to Q^hard, verified exactly (T-03(c)) | holds |
| Policy parameters θ | human-set only (Art. 16) | holds |
| **Hard-layer inputs** (κ^out, Λ, ADV, Γ̂) | only Γ has a policy floor; a model could supply optimistic κ^out or ADV | **VIOLATED by design ambiguity — AUD-002 (CRITICAL)** |

## Independence of caps

The caps are not independent: they fall into two comonotone families sharing one consumption each — the stop-risk family
{H1, H2, H3, H4, H10} (consumption L^stop(n)) and the notional family {H7, H8, H9, H11, H14} (consumption n·p^lim) — plus the gap family
{H5, H6}, the liquidity family {H12, H13} and H16. Because the envelope takes the **minimum** of caps rather than a sum, shared
consumption never double-counts; the binding cap is simply the tightest member of each family. Correlation between caps is therefore a
redundancy question (which member binds), not a safety question.
