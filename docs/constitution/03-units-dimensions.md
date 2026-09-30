# 03 — Units / Dimensions Matrix (v0.1-draft)

Status: DRAFT. Every equation in 05, 06 and 08 has been checked against this matrix (§3). A dimension error is a correctness
defect, not a style issue.

## 1. Base dimensions

| Dimension | Symbol | Unit | Notes |
|---|---|---|---|
| Money | $[\$]$ | USD (single currency, A-ACC-01) | multi-currency **UNDEFINED — REQUIRES RESOLUTION** (out of v0 scope) |
| Quantity of instrument $i$ | $[\mathrm{sh}_i]$ | shares of $i$ | **instrument-specific**: $[\mathrm{sh}_i]\ne[\mathrm{sh}_j]$ for $i\ne j$ |
| Calendar time | $[\mathrm T]$ | ns (UTC) | for timestamps, ages, TTLs |
| Trading time | $[\mathrm{day}]$ | trading day | for ADV, volatility scaling, exit horizon; conversion to $[\mathrm T]$ is calendar-dependent (half days, holidays) |
| Fund units | $[\mathrm{unit}]$ | units | unitisation only |
| Dimensionless | $[1]$ | — | fractions, returns, probabilities, correlations |

## 2. Quantity matrix

| Quantity | Dimension | Range / note |
|---|---|---|
| $C_t,E_t,W_t,Y_t,X,\mathrm{Inc},\mathrm{Fin},\Lambda,K_t,F_t,B_t,BP_t$ | $[\$]$ | — |
| $R^{\mathrm{open}},R^{\mathrm{res}},G^{\mathrm{open}},G^{\mathrm{res}},N^{\mathrm{open}},N^{\mathrm{res}},C^{\mathrm{res}},R^{\mathrm{hard}},G^{\mathrm{hard}},R^{\mathrm{allow}}$ | $[\$]$ | $\ge0$ |
| $L^{\mathrm{stop}}(n),L^{\mathrm{gap}}(n),L^{\mathrm{abs}}(n),\phi(n),\mathcal L_{t+1}$ | $[\$]$ | $\phi:[\mathrm{sh}_i]\to[\$]$ |
| $q_{i,t},n,e,Q_k,Q^{\mathrm{hard}},Q^{\mathrm{fin}},Q^{\mathrm{res}}_{i,t},\delta_q,\bar N$ | $[\mathrm{sh}_i]$ | lattice-valued |
| $p^{\mathrm{bid}},p^{\mathrm{ask}},m,\varsigma,p^{\mathrm{lim}},p^{\mathrm{stop}},p^{\mathrm{tgt}},f_j,\pi^{\mathrm{ref}},\kappa^{\mathrm{out}},\kappa^{\mathrm{liq}},\iota,\ell^{\mathrm{stop}},\gamma_j$ | $[\$/\mathrm{sh}_i]$ | — |
| $\mathrm{ADV}_i$ | $[\mathrm{sh}_i/\mathrm{day}]$ | — |
| $h^{\mathrm{ex}}$, $w^{\mathrm{in}}$, holding horizon $h$ | $[\mathrm{day}]$ (or $[\mathrm T]$ — must be declared) | — |
| $\hat\sigma_i$ | $[\mathrm{day}^{-1/2}]$ | std. dev. of log-return per $\sqrt{\text{trading day}}$ |
| $\hat\Sigma$ | $[\mathrm{day}^{-1}]$ | — |
| $\hat\rho_{ij}$, $r_{i,t+1}$, $DD$, $MDD$, $\vartheta$, all $f^{\cdot}$, $\lambda^{\mathrm{gross}}$, $\rho^{\mathrm{in}},\rho^{\mathrm{ex}}$, $\Gamma_i$, $\ell^{\mathrm{day}},\ell^{\mathrm{wk}},d^{\max},\eta^{\mathrm{lock}},m_K,m_G,\chi,\varsigma^{\max}$, $\beta,\delta,\epsilon^{\mathrm{ruin}}$, probabilities | $[1]$ | bounded as in 06 §9 |
| $U_t$ | $[\mathrm{unit}]$ | $>0$ |
| $\nu_t,H_t,\nu^{\mathrm{day}}_0,\nu^{\mathrm{wk}}_0,\nu^{\mathrm{ref}}$ | $[\$/\mathrm{unit}]$ | — |
| $\tau_t,t^{\mathrm{know}},\mathrm{age},\mathrm{TTL}$ | $[\mathrm T]$ | — |
| $J,\Delta J,\mathrm{LB},\varepsilon^{\mathrm{num}},\varepsilon^{\mathrm{stat}},\varepsilon^{\min}$ | same as $J$ — $[\$]$ for arithmetic $J$, $[1]$ for log-growth $J$ | must be declared with $J$ (RQ-13) |
| $\ell^{\min}$ | $[\$/\mathrm{sh}_i]$ — or $[1]$ if defined relative to price (**UNDEFINED — REQUIRES RESOLUTION**) | — |

## 3. Equation dimension checks

| Ref | Equation | Check |
|---|---|---|
| E-01 | $E_t=C_t+\sum_iq_{i,t}m_{i,t}-Y_t$ | $[\$]=[\$]+\sum[\mathrm{sh}_i][\$/\mathrm{sh}_i]-[\$]$ ✓ (sum over $i$ is valid only after conversion to $[\$]$) |
| E-02 | $G$ (05 §2) | every term $[\$]$ ✓ |
| E-03 | $L^{\mathrm{stop}}(n)=n(p^{\mathrm{lim}}-p^{\mathrm{stop}}+\kappa^{\mathrm{out}})+\phi^{\mathrm{buy}}(n)+\phi^{\mathrm{sell}}(n)$ | $[\mathrm{sh}_i][\$/\mathrm{sh}_i]+[\$]$ ✓ |
| E-04 | $L^{\mathrm{gap}}$: $n(p^{\mathrm{lim}}-(1-\Gamma)p^{\mathrm{stop}})$ | $[1]\cdot[\$/\mathrm{sh}_i]$ inside ✓ |
| E-05 | $Q=\delta_q\lfloor b/(\delta_q\ell)\rfloor$ | $[\mathrm{sh}_i]\cdot\lfloor[\$]/([\mathrm{sh}_i][\$/\mathrm{sh}_i])\rfloor=[\mathrm{sh}_i]\cdot\lfloor[1]\rfloor$ ✓ — the floor MUST act on a dimensionless count |
| E-06 | $f^{\mathrm{trd}}B_t$, $m_KK_t$ | $[1][\$]$ ✓ |
| E-07 | H8: $q_im_i+N^{\mathrm{res}}_i+np^{\mathrm{lim}}\le f^{\mathrm{conc}}B$ | $[\$]$ ✓ |
| E-08 | H12: $n\le\rho^{\mathrm{in}}\mathrm{ADV}_i$ | $[\mathrm{sh}_i]$ vs $[1][\mathrm{sh}_i/\mathrm{day}]$ ✗ unless an implicit $1\,[\mathrm{day}]$ window is declared. **Fixed in 06:** $n\le\rho^{\mathrm{in}}w^{\mathrm{in}}\mathrm{ADV}_i$ with $w^{\mathrm{in}}$ in $[\mathrm{day}]$ ✓ |
| E-09 | H13: $q+Q^{\mathrm{res}}+n\le\rho^{\mathrm{ex}}h^{\mathrm{ex}}\mathrm{ADV}_i$ | $[1][\mathrm{day}][\mathrm{sh}_i/\mathrm{day}]=[\mathrm{sh}_i]$ ✓ |
| E-10 | $\nu=W/U$, $DD=1-\nu/H$ | $[\$/\mathrm{unit}]$; $[1]$ ✓ |
| E-11 | $F^{\mathrm{dd}}=(1-d^{\max})H_tU_t$ | $[1][\$/\mathrm{unit}][\mathrm{unit}]=[\$]$ ✓ |
| E-12 | $\vartheta_K=\frac{m_K}{f^{\mathrm{trd}}}\cdot\frac{d^{\max}-DD}{1-DD}$ | $[1]$ ✓ |
| E-13 | $\log(W_{t+1}/W_t)$ | argument $[1]$ ✓; $\log W$ alone ✗ (log of dollars is undefined) |
| E-14 | Square-root impact $\iota\propto p\,\hat\sigma\sqrt{n/\mathrm{ADV}}$ | $[\$/\mathrm{sh}_i][\mathrm{day}^{-1/2}]\sqrt{[\mathrm{sh}_i]/[\mathrm{sh}_i/\mathrm{day}]}=[\$/\mathrm{sh}_i]$ ✓ — **only** if $\hat\sigma$ is per $\sqrt{\text{day}}$ and ADV per day |
| E-15 | $\hat\sigma_h=\hat\sigma\sqrt h$ | $[\mathrm{day}^{-1/2}][\mathrm{day}^{1/2}]=[1]$ ✓ dimensionally; *validity* requires i.i.d./uncorrelated increments (A-STAT-03) |
| E-16 | $\mathrm{ES}_\beta(\mathcal L)$ | $[\$]$ ✓ (ES of a relative loss is $[1]$ — never mix) |
| E-17 | P-12b: $\hat J(a)-\hat J(a^{\varnothing})-e_a-e_0$ | all in units of $J$ ✓ |

## 4. Dimension traps (each is a registered failure mode in 09)

| ID | Trap | Consequence |
|---|---|---|
| DT-1 | Summing share counts across instruments ($\sum_iq_i$) | meaningless "total shares"; exposure must be summed in $[\$]$ |
| DT-2 | Annualised $\sigma$ with daily ADV in an impact formula | impact off by $\sqrt{252}$-type factors (trading-days-per-year constant itself **UNDEFINED**) |
| DT-3 | Kelly fraction of **notional** vs fraction of **wealth at risk** | notional fraction $=$ risk fraction $\times\,p/\ell$; confusing them mis-sizes by $p/\ell$ (e.g. $50\times$ for a 2% stop) |
| DT-4 | Relative vs absolute losses in ES/VaR | a budget in $[\$]$ compared with a measure in $[1]$ |
| DT-5 | Participation cap without a time window (E-08) | cap silently depends on order-working duration |
| DT-6 | Calendar vs trading days in $h^{\mathrm{ex}}$, TTL, holding horizon | stale data admitted over weekends/holidays or over-restrictive TTLs |
| DT-7 | bps vs fraction (fee rates, spreads) | $10^4$ errors; every rate field MUST declare its unit in the schema |
| DT-8 | Price per share vs per lot / per contract (future instruments) | out of v0 scope; schema must carry a multiplier if ever admitted |
