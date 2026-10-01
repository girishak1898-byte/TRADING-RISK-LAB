# 03 — Units / Dimensions Matrix (v0.2-draft)

Status: DRAFT. v0.2 (AUD-011, AUD-031): the matrix is backed by the machine-readable `dimtable` below; every formula in
[14-formula-registry.md](14-formula-registry.md) carries a `dim:` expression that `tools/doccheck/check_constitution.py` evaluates under this
table (add/subtract and compare require equal dimensions; `log`/`exp` require dimensionless arguments; **floor and ceiling require
dimensionless arguments**; `sum_i` over instruments rejects share-dimensioned terms; the constant 0 is dimension-neutral). The table is
cross-checked against the Units column of 02. A dimension error is a correctness defect, not a style issue.

## 1. Base dimensions

| Dimension | Symbol | Unit | Notes |
|---|---|---|---|
| Money | $[\mathrm{USD}]$ | USD (single currency, A-ACC-01) | multi-currency **UNDEFINED — REQUIRES RESOLUTION** (out of v0 scope) |
| Quantity of instrument $i$ | $[\mathrm{sh}_i]$ | shares of $i$ | **instrument-specific**: shares of different instruments are incommensurable |
| Calendar time | $[\mathrm T]$ | ns (UTC) | timestamps, ages, TTLs |
| Trading time | $[\mathrm{day}]$ | trading day | ADV, volatility scaling, exit horizon, working window, holding horizon |
| Fund units | $[\mathrm{unit}]$ | units | unitisation only |
| Dimensionless | $[1]$ | — | fractions, returns, probabilities, correlations, counts |

The brief's distinctions map as: currency $[\mathrm{USD}]$; currency per share $[\mathrm{USD}/\mathrm{sh}_i]$; shares $[\mathrm{sh}_i]$;
dimensionless fractions, probabilities and returns $[1]$ (bounded as registered); time $[\mathrm T]$ or $[\mathrm{day}]$ (never mixed without an
explicit calendar conversion); volatility $[\mathrm{day}^{-1/2}]$; **risk-budget currency** ($R^{\mathrm{hard}}$, $b_k$, $K$) and **loss currency**
($L^{\mathrm{stop}}$, $r^{\mathrm{open}}$, $\mathcal L$) are both $[\mathrm{USD}]$ and may be compared; **per-share loss** ($\ell$, $\ell^{\mathrm{stop}}$,
$\kappa^{\mathrm{out}}$) is $[\mathrm{USD}/\mathrm{sh}_i]$ and must be multiplied by a quantity before it is compared with a budget.

## 2. Canonical dimension table

The first column is the name used in `dim:` expressions; the second is the registry row whose Units column must agree ("-" = registry
row has several units or units "as J", so no automatic cross-check); the third is the dimension.

```dimtable
# money [USD]
C S-030 USD
C_avail S-166 USD
C_res S-097 USD
E S-040 USD
W S-042 USD
W_min S-174 USD
Y S-035 USD
X S-036 USD
Inc S-037 USD
Fin S-038 USD
Accr S-045 USD
Pay S-046 USD
A_bar S-185 USD
Lam S-041 USD
Lam_i S-041 USD
Lam_floor S-249 USD
XV S-288 USD
R_led S-293 USD
Lam_hat - USD
K S-110 USD
F S-109 USD
F_abs S-105 USD
F_dd S-106 USD
F_day S-107 USD
F_wk S-107 USD
F_lock S-108 USD
B S-100 USD
BP S-122 USD
BP_avail S-123 USD
R_open S-096 USD
G_open S-096 USD
Z_open S-096 USD
N_open S-096 USD
R_res S-097 USD
G_res S-097 USD
Z_res S-097 USD
N_res S-097 USD
R_hard S-117 USD
G_hard S-118 USD
R_mod S-119 USD
R_allow S-121 USD
R S-240 USD
SL S-165 USD
L_stop S-090 USD
L_gap S-091 USD
L_abs S-092 USD
ER S-094 USD
r_open S-095 USD
g_open S-095 USD
u_open S-095 USD
phi_buy S-084 USD
phi_sell S-084 USD
phi_sell0 S-084 USD
phi_split S-292 USD
N_ex S-294 1
B_win S-295 USD
phi_paid S-296 USD
r_pf S-297 USD
q_bar S-298 sh
g_pf S-297 USD
u_pf S-297 USD
phi_fill - USD
Cjk S-083 USD
M_mkt S-170 USD
Loss S-136 USD
M_bar S-010 USD
Av S-280 USD
Rs S-280 USD
Op S-280 USD
Tot S-280 USD
J_usd - USD
# quantity [sh]
n S-065 sh
q S-032 sh
q_rem S-289 sh
q_exp S-290 sh
e S-071 sh
Q S-114 sh
Q_hard S-115 sh
Q_fin S-116 sh
Q_res S-248 sh
N_bar S-009 sh
delta_q S-007 sh
n_min S-269 sh
n_fill - sh
n_tilde S-210 sh
n_log S-179 sh
V S-209 sh
SH1 - sh
# price per share [USD/sh]
p_bid S-050 USD/sh
p_ask S-050 USD/sh
m S-051 USD/sh
m_arr S-053 USD/sh
spread S-052 USD/sh
p_lim S-062 USD/sh
p_stop S-034 USD/sh
p_tgt S-064 USD/sh
p_gx S-184 USD/sh
p_in S-211 USD/sh
p_out S-211 USD/sh
p_fill - USD/sh
p_last S-172 USD/sh
pi_ref S-082 USD/sh
p S-241 USD/sh
p_min S-274 USD/sh
p_max S-274 USD/sh
kappa_out S-085 USD/sh
kappa_liq S-086 USD/sh
kappa_hat - USD/sh
iota S-087 USD/sh
ell S-186 USD/sh
ell_stop S-093 USD/sh
gamma_gap S-089 USD/sh
# liquidity, time, volatility
ADV S-054 sh/day
ADV_est S-299 sh/day
ADV_max S-300 sh/day
W_R S-301 USD
nu_R S-302 USD/unit
DD_R S-303 1
q_fill S-304 sh
phi_acc S-305 USD
phi_owed S-306 USD
Q_bar S-307 sh
n_o S-308 sh
q_unf S-309 sh
w_in S-260 day
h_ex S-262 day
h S-011 day
sigma_hat S-055 day^(-1/2)
sigma_target S-215 day^(-1/2)
Sigma_hat S-056 day^(-1)
tau S-002 T
t_know S-023 T
age S-024 T
TTL S-025 T
# per unit
nu S-043 USD/unit
H S-101 USD/unit
nu_day0 S-104 USD/unit
nu_wk0 S-104 USD/unit
nu_ref S-267 USD/unit
nu_star S-173 USD/unit
U S-039 unit
# dimensionless
DD S-102 1
MDD S-103 1
DD_star S-168 1
theta_K S-111 1
vartheta_step - 1
zeta S-169 1
f_trd S-250 1
f_port S-251 1
f_strat S-252 1
f_gap S-253 1
f_ord S-254 1
f_conc S-255 1
f_clu S-256 1
f_clr S-257 1
lambda_gross S-258 1
rho_in S-259 1
rho_ex S-261 1
spread_max S-263 1
ell_day S-264 1
ell_wk S-264 1
d_max S-265 1
eta_lock S-266 1
mu_K S-268 1
mu_G S-268 1
chi S-270 1
Gamma_min S-271 1
ell_min S-272 1
kappa_min S-273 1
Gamma S-088 1
Gamma_hat - 1
r_ret S-059 1
rho_hat S-247 1
rho_bar S-220 1
beta S-137 1
eps_ruin S-142 1
delta_conf S-228 1
PB S-139 1
PoR S-140 1
P_win S-216 1
b_K S-217 1
f_K S-218 1
n_pos S-219 1
psi - 1
varpi - 1
lambda_ES - 1
varrho - 1
M_obs S-223 1
D_dim S-224 1
alpha S-027 1
J_log - 1
q_star S-284 1
A_R S-283 1
A_l S-283 1
D_R S-283 1
D_l S-283 1
eps_rd S-285 1
eps_mach S-285 1
```

## 3. Equation dimension checks (manual cross-reference; the mechanical check is authoritative)

| Ref | Formula | Check |
|---|---|---|
| E-01 | F033 $E_t=C_t+\sum_iq_{i,t}m_{i,t}-Y_t$ | $[\mathrm{USD}]$; the sum over $i$ is valid only after conversion to $[\mathrm{USD}]$ ✓ |
| E-02 | F055 $G$ | every term $[\mathrm{USD}]$ ✓ |
| E-03 | F061 $L^{\mathrm{stop}}$ | $[\mathrm{sh}_i][\mathrm{USD}/\mathrm{sh}_i]+[\mathrm{USD}]$ ✓ |
| E-04 | F062 $L^{\mathrm{gap}}$ | $[1]\cdot[\mathrm{USD}/\mathrm{sh}_i]$ inside the min ✓ |
| E-05 | F095 $Q_k=\delta_q\lfloor b_k/(\delta_q\ell_k)\rfloor$ | floor acts on the dimensionless count $b_k/(\delta_q\ell_k)$ ✓ |
| E-06 | F074 $f^{\mathrm{trd}}B_t$, $\mu^{K}K_t$ | $[1][\mathrm{USD}]$ ✓ |
| E-07 | F083 (H8) | $[\mathrm{USD}]$ ✓ |
| E-08 | F087 (H12) $n\le\rho^{\mathrm{in}}w^{\mathrm{in}}\mathrm{ADV}_i$ | $[1][\mathrm{day}][\mathrm{sh}_i/\mathrm{day}]=[\mathrm{sh}_i]$ ✓ (fixed in baseline: the window-free form was ✗) |
| E-09 | F088 (H13) | ✓ |
| E-10 | F036, F038 | $[\mathrm{USD}/\mathrm{unit}]$; $[1]$ ✓ |
| E-11 | F040 | $[1][\mathrm{USD}/\mathrm{unit}][\mathrm{unit}]=[\mathrm{USD}]$ ✓ |
| E-12 | F098 $\vartheta_K$ | $[1]$ ✓ |
| E-13 | F019 $\log(W_{t+1}/W_t)$ | argument $[1]$ ✓; $\log W$ alone ✗ |
| E-14 | F112 $\iota\propto p\,\hat\sigma\sqrt{n/\mathrm{ADV}}$ | $[\mathrm{USD}/\mathrm{sh}_i]$ ✓ only if $\hat\sigma$ is per $\sqrt{\text{day}}$ and ADV per day |
| E-15 | F113 $\hat\sigma\sqrt h$ | $[1]$ ✓ dimensionally; validity needs A-STAT-03 |
| E-16 | F010 $\mathrm{ES}_\beta(\mathcal L)$ | $[\mathrm{USD}]$ ✓ (ES of a relative loss is $[1]$ — never mix) |
| E-17 | F118 | all in units of $J$ ✓ |
| E-18 | F110 naive $Q=\lfloor R/\ell^{\mathrm{stop}}\rfloor$ | ✗ floor of $[\mathrm{sh}_i]$ — valid only in the one-share special case $\delta_q=1\,\mathrm{sh}$; corrected form $\delta_q\lfloor R/(\delta_q\ell^{\mathrm{stop}})\rfloor$ (AUD-031) |
| E-19 | F133 volatility-targeted size | a form "fraction × $W/\hat\sigma$" is ✗ ($[\mathrm{USD}\cdot\mathrm{day}^{1/2}]$); corrected $W\sigma^{\mathrm{target}}/\hat\sigma$ ✓ (AUD-031) |

## 4. Dimension traps (each is a registered failure mode in 09)

| ID | Trap | Consequence |
|---|---|---|
| DT-1 | Summing share counts across instruments | meaningless "total shares"; exposure must be summed in $[\mathrm{USD}]$ |
| DT-2 | Annualised $\hat\sigma$ with daily ADV in an impact formula | impact off by a trading-days-per-year factor (that constant itself **UNDEFINED**) |
| DT-3 | Kelly fraction of **notional** vs fraction of **wealth at risk** (F114) | notional fraction = risk fraction × $p/\ell$; confusing them mis-sizes by $p/\ell$ (e.g. 50× for a 2% stop) |
| DT-4 | Relative vs absolute losses in ES/VaR | a budget in $[\mathrm{USD}]$ compared with a measure in $[1]$ |
| DT-5 | Participation cap without a time window (E-08) | cap silently depends on order-working duration |
| DT-6 | Calendar vs trading days in $h^{\mathrm{ex}}$, TTL, holding horizon | stale data admitted over weekends/holidays or over-restrictive TTLs |
| DT-7 | bps vs fraction (fee rates, spreads) | $10^4$ errors; every rate field MUST declare its unit in the schema |
| DT-8 | Price per share vs per lot / per contract | out of v0 scope; schema must carry a multiplier if ever admitted |
| DT-9 | Floor of a share-dimensioned quotient (E-18) | hidden by the one-share special case; wrong on any other lattice |
| DT-10 | Volatility in a denominator without a matching target volatility (E-19) | size has dimension $[\mathrm{USD}\cdot\mathrm{day}^{1/2}]$ |
