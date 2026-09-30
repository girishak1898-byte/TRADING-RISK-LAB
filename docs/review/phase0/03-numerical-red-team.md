# Phase-0 Review — Numerical Red Team

Environment: Python 3.11.15, standard library only (`decimal` default context: precision 28, traps InvalidOperation, DivisionByZero,
Overflow; `fractions.Fraction` as the exact reference). The probes are evidence expressions, not engine code, and are not committed as
code; each row gives the exact expression so it can be re-run by copy-paste. "Expected" is the mathematically correct value (or the
behaviour the numerical contract requires).

## A. Numerical-semantics experiments

| ID | Exact input | Arithmetic path | Actual result | Expected mathematical result / required behaviour | Safety consequence |
|---|---|---|---|---|---|
| N01 | R = 5.0, M = nan | `min(5.0, nan)` | `5.0` | undefined → must fail closed | model failure silently ignored (order-dependent) |
| N02 | M = nan, R = 5.0 | `min(nan, 5.0)` | `nan` | as N01 | NaN propagates into sizing |
| N03 | 0.0, nan | `max(0.0, nan)` | `0.0` | undefined | clamp hides NaN (accidentally safe) |
| N04 | nan, 0.0 | `max(nan, 0.0)` | `nan` | undefined | clamp fails to clamp |
| N05 | Decimal NaN, 1 | `Decimal('NaN') < 1` | raises `InvalidOperation` | undefined → error | fails loud (good) |
| N06 | Decimal NaN, 1 | `Decimal('NaN') == 1` | `False` | undefined | equality tests silently false |
| N07 | Decimal sNaN, 1 | `Decimal('sNaN') == 1` | raises `InvalidOperation` | error | fails loud |
| N08 | Decimal 5, NaN | `min(Decimal(5), Decimal('NaN'))` | raises `InvalidOperation` | error | fails loud (good) |
| N09 | Decimal NaN, 5 | `Decimal('NaN').max(Decimal(5))` | `Decimal('5')` | undefined → fail closed | IEEE maxNum drops NaN: "model failed" ⇒ "no model limit" |
| N10 | Decimal 5, NaN | `Decimal(5).min(Decimal('NaN'))` | `Decimal('5')` | as N09 | as N09 |
| N11 | Fraction 1, float nan | `Fraction(1) < nan` | `False` | undefined | silent false comparison |
| N12 | float nan | `Fraction(nan)` | raises `ValueError` | error | fails loud |
| N13 | float nan | `int(nan)` | raises `ValueError` | error | fails loud |
| I01 | R = +inf (float), ℓ = 2.0 | `math.floor(inf/2.0)` | raises `OverflowError` | budget +∞ is inadmissible | exception must map to NO_TRADE (Art. 18) |
| I02 | R = Decimal('Infinity'), ℓ = 2 | `(R/ℓ).quantize(Decimal(1), ROUND_FLOOR)` | raises `InvalidOperation` | inadmissible | as I01 |
| I03 | Decimal('Infinity') | `int(...)` | raises `OverflowError` | inadmissible | as I01 |
| I04 | R_hard = 100.0, model = −inf | `max(0.0, min(100.0, -inf))` | `0.0` | 0 (invalid model ⇒ 0 if REQUIRED) | accidentally correct |
| I05 | −inf | `math.floor(-inf)` | raises `OverflowError` | inadmissible | as I01 |
| I06 | R = 1.0, ℓ = +inf | `math.floor(1.0/inf)` | `0` | ℓ = ∞ inadmissible (should be rejected, not sized to 0) | masks an invalid input as a legitimate zero |
| I07 | +inf − +inf | float | `nan` | undefined | NaN generation (P-12a edge case) |
| Z01 | −0.0, 0.0 | `max(0.0, -0.0)` | `0.0` | 0 | — |
| Z02 | −0.0, 0.0 | `min(-0.0, 0.0)` | `-0.0` | 0 | sign-dependent output |
| Z03 | Decimal('-0') | `str(Decimal('-0').quantize(Decimal('0.01')))` | `'-0.00'` | "0.00" | canonical serialisation / evidence hash differ for equal values |
| Z04 | Decimal('-0'), Decimal('0') | `==` | `True` | True | equality hides the representational difference |
| Z05 | Decimal('-0') × 5 | `str(Decimal('-0')*Decimal(5))` | `'-0'` | "0" | −0 is *produced* internally, so boundary rejection is insufficient |
| Z06 | float −0.0 | `json.dumps(-0.0)` | `'-0.0'` | "0" | as Z03 |
| T01 | R = 1000, ℓ = 5e-324 (subnormal) | `1000/5e-324` | `inf` | 2×10³²⁶ (exact) | overflow to ∞ → exception path |
| T02 | R = Decimal(1000), ℓ = Decimal('1e-28') | `R/ℓ` | `Decimal('1.000E+31')` | 10³¹ shares | unbounded sizing absent G7 / N̄ |
| T03 | R = 1000, ℓ ∈ {0.01, 1e-4, 1e-8} | exact `floor(R/ℓ)` | `100000, 10000000, 100000000000` | same | size explodes as the per-share loss → 0 |
| T04 | R = 1000, ℓ = 0 | `Fraction(1000)/Fraction(0)` | raises `ZeroDivisionError` | undefined | G7 must reject ℓ < ℓ^min before division |
| L01 | 1e308 × 10 | float | `inf` | 10³⁰⁹ | silent overflow |
| L02 | Decimal('9e999999') × 10 | default context | raises `Overflow` | 9×10¹⁰⁰⁰⁰⁰⁰ | fails loud (trap on) |
| L03 | Decimal(12345678901234567890123456789) + 1 | precision 28 | `'1.234567890123456789012345679E+28'` | 12345678901234567890123456790 | silent rounding (half-even) at 29 digits |
| L04 | 2⁵³ + 1 | `float(2**53+1) == 2**53` | `True` | False | integers above 2⁵³ not representable in binary64 |
| L05 | R = 172,808,193.53, ℓ = 65.68583269 | `floor(float(R)/float(ℓ))` vs exact | `2630829` vs `2630828` | 2,630,828 | one share over the cap (infeasible) |
| L06 | same | T-22 condition r·d_ℓ vs 2⁵¹ | 1.728×10¹⁸ vs 2.25×10¹⁵ | condition violated | overshoot consistent with T-22 |
| HC01 | 10.005 to cents | HALF_EVEN, HALF_UP, FLOOR, CEILING | `10.00, 10.01, 10.00, 10.01` | direction must be chosen per quantity | a limit price (worst-case entry) rounded down understates risk |
| HC02 | float 10.005 | `round(10.005, 2)`; exact value | `10.01`; 5632314283980227/562949953421312 | the float is not 10.005 | float rounding reflects the binary value, not the decimal |
| HC03 | fee 0.005 to cents | HALF_EVEN vs CEILING | `0.00` vs `0.01` | fee must round up | half-even removes a fee |
| HC04 | fee 0.015 to cents | HALF_EVEN vs HALF_UP | `0.02` vs `0.02` | round up (0.02) | coincidentally equal; not a rule |
| B01 | R = 0.3, ℓ = 0.1 (float) | `floor(0.3/0.1)` vs exact | `2` vs `3` | 3 | under-sizing (safe) but float ≠ exact: differential tests disagree |
| B02 | R = 0.7, ℓ = 0.1 (float) | as B01 | `6` vs `7` | 7 | as B01 |
| B03 | R = 1000.00, ℓ = 2.90 | HALF_UP quantity, loss | `345`, `1000.50` | 344, 997.60 | budget exceeded |
| B04 | same | HALF_EVEN quantity | `345` | 344 | budget exceeded (REV-020) |
| B05 | R = −0.01, ℓ = 1 | `math.floor(-0.01/1)` | `-1` | 0 after clamp | sign flip: a negative quantity readable as a sell |
| B06 | L(n) = 0.1n + 2·max(1, 0.005n), b = 2.5 | naive `floor(b/0.11)` vs exact search | `22` vs `5` | 5 | naive closed form exceeds budget (loss 4.20) |
| C01 | 100.07 − 99.97 | float | `0.09999999999999432` | 0.10 | stop distance understated ⇒ size overstated |
| C02 | Decimal('100.07') − Decimal('99.97') | decimal | `'0.10'` | 0.10 | exact |
| X01 | Fraction(1,10) + 0.2 | mixed | `0.30000000000000004` (float) | 3/10 | exactness silently lost when a float leaks in |
| X02 | Decimal('0.1') + 0.2 | mixed | raises `TypeError` | error | fails loud (good) |
| X03 | Decimal('0.1') == 0.1 | compare | `False` | (0.1 ≠ binary 0.1) | correct but surprising |
| X04 | Decimal(0.1) | from float | `0.1000000000000000055511151231257827021181583404541015625` | 0.1 intended | float-derived decimal is not the intended value |
| X05 | Fraction(0.1) | from float | `3602879701896397/36028797018963968` | 1/10 | as X04 |
| R01 | Decimal(2).sqrt(), .ln() at precision 5, FLOOR vs CEILING | context rounding | `1.4142, 1.4142, 0.69315, 0.69315` | ceiling sqrt = 1.4143 | directed rounding unavailable via context; certify instead |
| R02 | Decimal(0).ln() | decimal | `Decimal('-Infinity')` | −∞ with signal | silent −∞ into a log objective |
| R03 | Decimal(−1).ln() | decimal | raises `InvalidOperation` | undefined | fails loud |
| R04 | math.log(0.0) | float | raises `ValueError` | error | fails loud |
| R05 | Decimal(1)/Decimal(0) | decimal | raises `DivisionByZero` | error | fails loud |
| R06 | Decimal(0)/Decimal(0) | decimal | raises `InvalidOperation` | error | fails loud |
| P01 | Decimal('123456789012345.12345678') × Decimal('1000000.0000001') | precision 28 | `123456789012357469135.6812345`, Inexact flag True | exact product has more digits | silent rounding unless Inexact trapped |
| P02 | global `getcontext().prec = 5` set by other code | `Decimal(1)/Decimal(3)` | `'0.33333'` | context-independent result | non-reproducible output (Art. 8) |
| J01 | `json.loads('{"x": NaN}')` | default parser | `{'x': nan}` | reject | **NaN enters through the parser** |
| J02 | `json.loads('{"x": Infinity}')` | default parser | `{'x': inf}` | reject | ∞ enters through the parser |
| J03 | `json.loads('{"x": 1e400}')` | default parser | `{'x': inf}` | reject or exact decimal | overflow to ∞ at parse time |
| J04 | `json.loads('{"x": 0.1}', parse_float=Decimal)` | exact parse | `{'x': Decimal('0.1')}` | 0.1 | correct pattern |
| J05 | `json.dumps(0.1+0.2)` | float serialisation | `'0.30000000000000004'` | "0.3" | float artefacts in evidence |
| S01 | set of six tickers, PYTHONHASHSEED 1 vs 2 | `list(set)` order | two different orders | order-independent computation | allocation order (T-23) and evidence differ across processes |

## B. Reproduction of reviewer claims (REV) and self-audit claims (AUD)

| Ref | Exact input | Result | Expected by the claim |
|---|---|---|---|
| REV-001 | q = 100, m = 50, stop 49, κ(n) = 0.001n, Λ(n) = 0.001n²; add 100 at 50; close 49.01 | r = 100, L = 110, K = 210, ΔW = −228, breach 18; A-TRIG 9,762 ≥ 9,760; v0.1.1: K = 220, breach 8; incremental charge 130 | confirmed |
| REV-002 | 1,000 sh at 50, stop 45, κ = 0.05, cash 200,000, f = 2%, L = 5.05n | Λ = 500: b = 440, Q = 87; Λ = 100: b = 48, Q = 9; without credit b = −60 / −52 | confirmed |
| REV-003 | pending 100 @ 5; new 100 @ 5.94; $1 minimum commissions | K = 1,096, loss 1,098, W − F = −2 | confirmed |
| REV-004 | W_t = F_t − 1, no positions | W − F = −1 | confirmed |
| REV-005 | 100 at 50, stop 49, κ = 0.1; mark 45 at the cut | r = 110, drop 500 | confirmed |
| REV-006 | φ = max(1, 0.005k) per execution; 34/33/33 | fees 3 vs φ(100) = 1 | confirmed |
| REV-007 | Γ = 1%, stop 10, κ = 0.2, q = 100 | A-TRIG 980 vs tier-G 990 | confirmed |
| REV-008 | F^abs = 90, W = 100, r = K = 10, X = −5 | W_{t+1} = 85 | confirmed |
| REV-011 | f = 0.1%, p = 10, κ₀ = 0.01 | notional bound = 1 × W | confirmed |
| REV-012 | cash-only W = 100, X = −100 | W_{t+1} = 0 | confirmed |
| REV-013 | 2:1 split / 1:2 reverse split, no fills | booked −2,500 / +5,000; true 0 | confirmed; reverse split anti-conservative |
| REV-014 | d = 0.1, DD = 2 | (d − DD)/(1 − DD) = 19/10 | confirmed |
| REV-016 | ℓ^day = 2%, cash 50 + 1 sh at 50, stop 49 | K 2 → 7 (r 6) → 2.1 next day | confirmed |
| REV-020 | 1000.00/2.90 | HALF_EVEN 345, HALF_UP 345, FLOOR 344 | confirmed |
| REV-022 | −∞ − (−∞) | NaN | confirmed |
| T-17 | W = 100,000, f = 1%, ℓ = 0.01, p = 50, Γ = 5% | loss 250,950 | reviewer figure confirmed |
| T-06 ratchet | W 100 → 140 → 90.5 | DD = 99/280 ≈ 35.4% | confirmed |
| AUD-001 | q = 100 at 50, stop 49, κ = 0.1, per-order fee max(1, 0.005n), Λ_t = 0; 50 filled at 48.9 fee 1; remainder at A-TRIG bound | r = K = 111, ΔW = −112, W − F = −1; position-level bound requires 4,889, attained 4,888 | confirmed |
| AUD-014 | same, static floor | K' = 0, remaining open risk 1 | confirmed |

## C. Consequences for the numerical contract (feed AUD-018)

1. Parse snapshots with a strict parser: reject the tokens NaN, Infinity, −Infinity and any numeral that does not parse exactly to a
   finite decimal; parse numbers as decimals (J01–J04).
2. Normalise negative zero to zero before quantisation and serialisation (Z02–Z06).
3. Forbid mixed-type arithmetic on the authority path (X01); exact types only.
4. Quantise money to the declared scale with the directed-rounding table: fees and consumptions up, capacities down, and never round
   a limit price down (HC01–HC04).
5. Division by a per-share loss occurs only after G7 has established ℓ ≥ ℓ^min > 0 (T01–T04, I06).
6. Differential testing compares the exact implementation with an exact oracle, never with a float implementation (B01–B02).
