# Phase-0 Review — Mechanical Checks Before Correction

Output of `python3 tools/doccheck/check_constitution.py --verbose` run against commit `8198877` (the documents as they stood before the
correction commit) plus this review record. Counts and lists feed AUD-006 … AUD-011 and AUD-022. The formula registry and dimension
table did not yet exist, so formula and dimension gates report their absence. References to RT-xx and OC-2/OC-3 are forward
references from the finding registry to identifiers introduced by the correction commit.

```text
MISSING_DELIVERABLES = 1
    14 (Formula Registry)
UNDEFINED_CROSS_REFERENCES = 5
    RT:RT-01
    RT:RT-36
    OC:OC-1
    OC:OC-2
    OC:OC-3
DUPLICATE_MEANING_SYMBOLS = 21
    B -> S-100, S-122, S-123, S-139
    D -> S-102, S-102, S-103, S-103, S-168
    Delta -> S-144, S-175
    J -> S-143, S-144
    M -> S-103, S-124, S-124, S-124
    P -> S-122, S-139
    W -> S-042, S-174
    a -> S-066, S-136, S-139, S-143, S-144, S-145, S-174
    delta -> S-007, S-146
    ell -> S-161, S-186
    mathbb:P -> S-130, S-183
    mathcal:A -> S-069, S-069, S-161
    mathcal:F -> S-130, S-131
    mathcal:P -> S-134, S-177
    mathsf:d -> S-023, S-024
    n -> S-065, S-081, S-084, S-084, S-085, S-086, S-087, S-090, S-091, S-092, S-094, S-113, S-184
    p^stop -> S-034, S-063
    r -> S-059, S-171
    tau -> S-002, S-081
    vartheta -> S-111, S-168
    x -> S-070, S-113, S-113, S-150
INCOMPLETE_REGISTRY_ROWS = 29
    S-160: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-161: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-162: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-163: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-164: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-165: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-166: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-167: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-168: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-169: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-170: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-171: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-172: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-173: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-174: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-175: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-176: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-177: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-178: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-179: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-180: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-181: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-182: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-183: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-184: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-185: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-186: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-187: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
    S-188: missing ['Type', 'Domain', 'Codomain', 'Units', 'Sign', 'Valid range', 'Source']
UNREGISTERED_SYMBOLS = 103
    A [02, 08:T-11, 08:T-12, 08:T-23]
    C' [08:T-05]
    G [01, 02, 03, 05, 06, 07, 08:T-08, 09]
    J' [08:T-08]
    L [08:T-02, 08:T-10, 08:T-22, 09]
    O [08:T-11]
    P' [08:T-05]
    Q^* [09]
    Q_buying power [06]
    Q_concentration [06]
    Q_correlation [06]
    Q_gap [06]
    Q_liquidity [06]
    Q_margin [06]
    Q_notional [06]
    Q_portfolio [06]
    Q_risk [06]
    R [01, 06, 08:T-01, 08:T-11, 08:T-22, 08:T-23, 09]
    R_hard [06, 09]
    S [02, 08:T-21]
    T [02, 05, 08:T-11]
    Theta [01, 02]
    V [08:T-03, 08:T-13]
    W' [08:T-05]
    Xi [02]
    Z [02, 09]
    bar:g [08:T-03]
    bar:rho [09]
    chi [01, 02, 03, 06]
    ell^day [02, 03, 06, 08:T-05]
    ell^wk [02, 03, 06, 08:T-05]
    epsilon [01, 08:T-19, 09, 10]
    eta^lock [02, 03, 06, 08:T-05]
    f^* [09]
    f^clr [02, 06]
    f^clu [02, 06]
    f^conc [02, 03, 06]
    f^gap [02, 06]
    f^in [05, 08:T-10]
    f^ord [02, 06]
    f^out [05]
    f^port [02, 06, 08:T-07]
    f^strat [02, 06]
    f^trd [02, 03, 06, 08:T-07, 08:T-17]
    h^ex [02, 03, 06]
    hat:Gamma [01, 02]
    hat:Q [08:T-24]
    hat:b [08:T-24]
    hat:bar:rho [09]
    hat:g [08:T-24]
    hat:mathbb:P [01, 08:T-19]
    hat:p [09]
    kappa [05, 08:T-08, 08:T-10, 08:T-17, 09]
    lambda^gross [02, 03, 04, 06, 13]
    macro:begin [06]
    macro:end [06]
    macro:leftrightarrow [06]
    macro:ni [08:T-16]
    macro:tfrac [02]
    mathbb:1 [06]
    mathbb:L^N [02]
    mathbb:N [02]
    mathbb:Q [01, 02, 05, 08, 08:T-02, 08:T-09, 08:T-12, 10]
    mathbb:Q' [08:T-12]
    mathbb:R [01, 02]
    mathbb:T [01, 02]
    mathbb:Z [02, 08, 08:T-22]
    mathcal:O [01, 02]
    mathcal:P' [08:T-09]
    mathcal:V [01, 02]
    mathfrak:D [01, 02]
    mathfrak:S [01, 02]
    mathrm:RN [08:T-22]
    mathrm:Ruin [01]
    mathrm:avail [08:T-05]
    mathrm:hard [08:T-08]
    mathrm:id [02]
    mathrm:out [08:T-08]
    n' [05]
    nu^ref [02, 03, 08:T-05]
    p [01, 03, 08:T-03, 08:T-11, 08:T-17, 09]
    p'^lim [05]
    phi' [08:T-08]
    pi [01]
    q^* [08:T-22]
    rho^ex [02, 03, 06]
    rho^in [02, 03, 06]
    s [02, 06, 07, 08:T-11]
    sigma [01, 02, 03]
    tilde:n [08:T-03]
    u [01, 02, 06, 08, 08:T-08, 08:T-22]
    v [08:T-11]
    varepsilon' [08:T-09]
    varphi [01]
    w^in [02, 03, 06]
    x' [08:T-05]
    x^A [01, 02]
    x^B [01, 02]
    x^H [01, 02]
    x^M [01, 02]
    x^P [01, 02]
    x^U [01, 02]
    y [01, 02]
_SHADOWED_LOCAL_SYMBOLS (explicitly namespaced) = 0
UNTAGGED_EQUATIONS = 1
    formula registry 14 missing
INCOMPLETE_FORMULA_ROWS = 0
FORMULAS_NOT_REFERENCED_IN_ANY_DOCUMENT = 0
DIMENSIONAL_CONFLICTS = 1
    no dimtable in 03
_BIBLIOGRAPHY_TOTAL = 115
BIBLIOGRAPHY_DUPLICATES = 0
NON_DOCUMENTATION_FILES = 0
FORBIDDEN_IMPORTS = 0
GATE_TOTAL = 161
```
