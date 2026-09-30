# Phase-0 Review — Bibliography and Novelty Audit

## 1. Mechanical counts (document 11 §1 at `8198877`)

| Metric | Value | Method |
|---|---|---|
| TOTAL REFERENCES | **115** | entries parsed from 11 §1 (split on " · " within topic paragraphs); checker `_BIBLIOGRAPHY_TOTAL` |
| DUPLICATES | **0** | case-insensitive title comparison; the only repeated author–year key (Bäuerle 2011) is two distinct works (Bäuerle & Rieder book; Bäuerle & Ott article) |
| UNVERIFIED REFERENCES (by this audit, independently) | **115** | independent re-verification was attempted and blocked: this session's egress policy denies doi.org, api.crossref.org, onlinelibrary.wiley.com, dblp.org, www.sciencedirect.com, econpapers.repec.org, joss.theoj.org and marco-campi.unibs.it (proxy 403 / EGRESS_BLOCKED). A deterministic sample (IDs 1, 21, 41, 61, 81, 101) could not be fetched. |
| VERIFIED BY SUBAGENT (same session, earlier, web search) | 111 as given + 4 corrected = **115** | subagent report; evidence URLs recorded in §3 below (they were not in the repository at `8198877`) |
| BROKEN IDENTIFIERS | **0 in the document; NOT MACHINE-CHECKABLE in this session** | 11 contains no DOIs or URLs (by design at baseline). The 115 evidence URLs in §3 could not be resolved from this session (egress policy). |
| CORRECTED REFERENCES | **4** | #9 Sun & Boyd (subtitle), #21 Shapiro–Dentcheva–Ruszczyński (edition years), #24 McNeil–Frey–Embrechts (edition years), #100 Cowlishaw (2009 version) |
| Citations in other documents not present in 11 | **0** | mechanical paragraph-aware surname–year match of every citation-like string in 01–13 against the 115 entries |

Evidence-quality note: most evidence URLs are publisher or DOI landing pages. Some are secondary: #25 (review in ASTIN Bulletin), #31 and #94
(Semantic Scholar), #34 (library catalogue), #58, #69, #97, #111 (Google Books), #29 (SSRN; *Risk* is a trade magazine).

## 2. Content claims

Four content claims were checked by the subagent from abstracts: Grossman & Zhou (1993), Busseti, Ryu & Boyd (2016), Mohajerin Esfahani &
Kuhn (2018), and Balder, Brandl & Mahayni (2009). None was re-verified by this audit (egress policy). Every other statement about what a
cited work shows is a reading task (11 §4), not a verified fact.

## 3. Evidence register (as reported by the subagent; not independently re-resolved)

| # | Reference (short) | Subagent status | Evidence URL |
|---|---|---|---|
| 1 | Kelly 1956 | VERIFIED | https://onlinelibrary.wiley.com/doi/abs/10.1002/j.1538-7305.1956.tb03809.x |
| 2 | Breiman 1961 | VERIFIED | https://projecteuclid.org/proceedings/berkeley-symposium-on-mathematical-statistics-and-probability/Proceedings-of-the-Fourth-Berkeley-Symposium-on-Mathematical-Statistics-and/Chapter/Optimal-Gambling-Systems-for-Favorable-Games/bsmsp/1200512159 |
| 3 | Thorp 2006 | VERIFIED | https://www.sciencedirect.com/book/9780444532480/handbook-of-asset-and-liability-management |
| 4 | MacLean, Thorp & Ziemba 2011 | VERIFIED | https://www.worldscientific.com/worldscibooks/10.1142/7598 |
| 5 | MacLean, Ziemba & Blazenko 1992 | VERIFIED | https://econpapers.repec.org/article/inmormnsc/v_3a38_3ay_3a1992_3ai_3a11_3ap_3a1562-1585.htm |
| 6 | Samuelson 1979 | VERIFIED | https://ideas.repec.org/a/eee/jbfina/v3y1979i4p305-307.html |
| 7 | Algoet & Cover 1988 | VERIFIED | https://projecteuclid.org/journals/annals-of-probability/volume-16/issue-2/Asymptotic-Optimality-and-Asymptotic-Equipartition-Properties-of-Log-Optimum-Investment/10.1214/aop/1176991793.full |
| 8 | Busseti, Ryu & Boyd 2016 | VERIFIED | https://web.stanford.edu/~boyd/papers/kelly.html |
| 9 | Sun & Boyd 2018 | CORRECTED | https://arxiv.org/abs/1812.10371 |
| 10 | Rujeerapaiboon, Kuhn & Wiesemann 2016 | VERIFIED | https://www.jstor.org/stable/24740351 |
| 11 | Merton 1969 | VERIFIED | https://ideas.repec.org/a/tpr/restat/v51y1969i3p247-57.html |
| 12 | Artzner et al. 1999 | VERIFIED | https://onlinelibrary.wiley.com/doi/10.1111/1467-9965.00068 |
| 13 | Acerbi & Tasche 2002 | VERIFIED | https://www.sciencedirect.com/science/article/abs/pii/S0378426602002832 |
| 14 | Rockafellar & Uryasev 2000 | VERIFIED | https://sites.math.washington.edu/~rtr/papers/rtr179-CVaR1.pdf |
| 15 | Rockafellar & Uryasev 2002 | VERIFIED | https://www.sciencedirect.com/science/article/abs/pii/S0378426602002716 |
| 16 | Föllmer & Schied 2002 | VERIFIED | https://link.springer.com/article/10.1007/s007800200072 |
| 17 | Ruszczyński 2010 | VERIFIED | https://link.springer.com/article/10.1007/s10107-010-0393-3 |
| 18 | Riedel 2004 | VERIFIED | https://www.sciencedirect.com/science/article/pii/S0304414904000420 |
| 19 | Cheridito, Delbaen & Kupper 2006 | VERIFIED | https://projecteuclid.org/journals/electronic-journal-of-probability/volume-11/issue-none/Dynamic-Monetary-Risk-Measures-for-Bounded-Discrete-Time-Processes/10.1214/EJP.v11-302.full |
| 20 | Artzner et al. 2007 | VERIFIED | https://link.springer.com/article/10.1007/s10479-006-0132-6 |
| 21 | Shapiro, Dentcheva & Ruszczyński | CORRECTED | https://dblp.org/rec/books/siam/ShapiroDR09.html |
| 22 | Gneiting 2011 | VERIFIED | https://www.tandfonline.com/doi/abs/10.1198/jasa.2011.r10138 |
| 23 | Fissler & Ziegel 2016 | VERIFIED | https://projecteuclid.org/journals/annals-of-statistics/volume-44/issue-4/Higher-order-elicitability-and-Osbands-principle/10.1214/16-AOS1439.full |
| 24 | McNeil, Frey & Embrechts | CORRECTED | https://ideas.repec.org/b/pup/pbooks/10496.html |
| 25 | Embrechts, Klüppelberg & Mikosch 1997 | VERIFIED | https://ideas.repec.org/a/cup/astinb/v28y1998i02p285-286_01.html |
| 26 | Grossman & Zhou 1993 | VERIFIED | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-9965.1993.tb00044.x |
| 27 | Cvitanić & Karatzas 1995 | VERIFIED | https://conservancy.umn.edu/items/f9b11232-1479-4a33-9884-b9a38531a52d |
| 28 | Chekhlov, Uryasev & Zabarankin 2005 | VERIFIED | https://researchwith.stevens.edu/en/publications/drawdown-measure-in-portfolio-optimization/ |
| 29 | Magdon-Ismail & Atiya 2004 | VERIFIED | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=874069 |
| 30 | Goldberg & Mahmoud 2017 | VERIFIED | https://link.springer.com/article/10.1007/s11579-016-0181-9 |
| 31 | Black & Perold 1992 | VERIFIED | https://www.semanticscholar.org/paper/Theory-of-constant-proportion-portfolio-insurance-Black-Perold/4d479fab3aa8825817fef76b02bb9b3e6d1b5e35 |
| 32 | Balder, Brandl & Mahayni 2009 | VERIFIED | https://econpapers.repec.org/article/eeedyncon/v_3a33_3ay_3a2009_3ai_3a1_3ap_3a204-220.htm |
| 33 | Aubin 1991 | VERIFIED | https://dl.acm.org/doi/10.5555/120830 |
| 34 | Aubin, Bayen & Saint-Pierre 2011 | VERIFIED | https://catalog.princeton.edu/catalog/6787561 |
| 35 | Bertsekas 1972 | VERIFIED | https://www.mit.edu/~dimitrib/Infinite-TimeReachability.pdf |
| 36 | Blanchini 1999 | VERIFIED | https://www.sciencedirect.com/science/article/abs/pii/S0005109899001132 |
| 37 | Abate et al. 2008 | VERIFIED | https://www.sciencedirect.com/science/article/abs/pii/S0005109808002677 |
| 38 | Summers & Lygeros 2010 | VERIFIED | https://www.sciencedirect.com/science/article/abs/pii/S0005109810003547 |
| 39 | Mayne, Seron & Raković 2005 | VERIFIED | https://dl.acm.org/doi/10.1016/j.automatica.2004.08.019 |
| 40 | Ames et al. 2019 | VERIFIED | https://arxiv.org/abs/1903.11199 |
| 41 | Wabersich & Zeilinger 2021 | VERIFIED | https://www.sciencedirect.com/science/article/abs/pii/S0005109821001175 |
| 42 | Alshiekh et al. 2018 | VERIFIED | https://dl.acm.org/doi/10.5555/3504035.3504361 |
| 43 | Mohajerin Esfahani & Kuhn 2018 | VERIFIED | https://link.springer.com/article/10.1007/s10107-017-1172-1 |
| 44 | Fournier & Guillin 2015 | VERIFIED | https://link.springer.com/article/10.1007/s00440-014-0583-7 |
| 45 | Gao & Kleywegt 2023 | VERIFIED | https://dl.acm.org/doi/abs/10.1287/moor.2022.1275 |
| 46 | Blanchet & Murthy 2019 | VERIFIED | https://pubsonline.informs.org/doi/10.1287/moor.2018.0936 |
| 47 | Ben-Tal et al. 2013 | VERIFIED | https://research.tilburguniversity.edu/en/publications/robust-solutions-of-optimization-problems-affected-by-uncertain-p/ |
| 48 | Duchi, Glynn & Namkoong 2021 | VERIFIED | https://pubsonline.informs.org/doi/10.1287/moor.2020.1085 |
| 49 | Delage & Ye 2010 | VERIFIED | https://pubsonline.informs.org/doi/10.1287/opre.1090.0741 |
| 50 | Van Parys, Mohajerin Esfahani & Kuhn 2021 | VERIFIED | https://pubsonline.informs.org/doi/10.1287/mnsc.2020.3678 |
| 51 | Bertsimas, Gupta & Kallus 2018 | VERIFIED | https://dl.acm.org/doi/10.1007/s10107-017-1125-8 |
| 52 | Rahimian & Mehrotra 2022 | VERIFIED | https://www.numdam.org/articles/10.5802/ojmo.15/ |
| 53 | Nilim & El Ghaoui 2005 | VERIFIED | https://econpapers.repec.org/RePEc:inm:oropre:v:53:y:2005:i:5:p:780-798 |
| 54 | Iyengar 2005 | VERIFIED | https://pubsonline.informs.org/doi/10.1287/moor.1040.0129 |
| 55 | Shapiro 2016 | VERIFIED | https://www.jstor.org/stable/24740530 |
| 56 | Epstein & Schneider 2003 | VERIFIED | https://ideas.repec.org/a/eee/jetheo/v113y2003i1p1-31.html |
| 57 | Gilboa & Schmeidler 1989 | VERIFIED | https://ideas.repec.org/a/eee/mateco/v18y1989i2p141-153.html |
| 58 | Hansen & Sargent 2008 | VERIFIED | https://books.google.com/books/about/Robustness.html?id=7wwV27TvR8EC |
| 59 | Garlappi, Uppal & Wang 2007 | VERIFIED | https://ideas.repec.org/a/oup/rfinst/v20y2007i1p41-81.html |
| 60 | Nemirovski & Shapiro 2006 | VERIFIED | https://epubs.siam.org/doi/10.1137/050622328 |
| 61 | Calafiore & Campi 2006 | VERIFIED | https://marco-campi.unibs.it/pdf-pszip/IEEE-TAC-scenario.pdf |
| 62 | Howard & Matheson 1972 | VERIFIED | https://pubsonline.informs.org/doi/10.1287/mnsc.18.7.356 |
| 63 | Whittle 1981 | VERIFIED | https://www.cambridge.org/core/journals/advances-in-applied-probability/article/abs/risksensitive-linearquadraticgaussian-control/9D29B8E7D13589A3823E75525181117F |
| 64 | Bielecki & Pliska 1999 | VERIFIED | https://link.springer.com/article/10.1007/s002459900110 |
| 65 | Bäuerle & Rieder 2011 | VERIFIED | https://link.springer.com/chapter/10.1007/978-3-642-18324-9_4 |
| 66 | Bäuerle & Ott 2011 | VERIFIED | https://link.springer.com/article/10.1007/s00186-011-0367-0 |
| 67 | Chow et al. 2015 | VERIFIED | https://proceedings.neurips.cc/paper/2015/hash/64223ccf70bbb65a3a4aceac37e21016-Abstract.html |
| 68 | Browne 1995 | VERIFIED | https://pubsonline.informs.org/doi/abs/10.1287/moor.20.4.937 |
| 69 | Asmussen & Albrecher 2010 | VERIFIED | https://books.google.com/books/about/Ruin_Probabilities_2nd_Edition.html?id=ntDFCgAAQBAJ |
| 70 | Magill & Constantinides 1976 | VERIFIED | https://econpapers.repec.org/RePEc:eee:jetheo:v:13:y:1976:i:2:p:245-263 |
| 71 | Davis & Norman 1990 | VERIFIED | https://pubsonline.informs.org/doi/10.1287/moor.15.4.676 |
| 72 | Almgren & Chriss 2001 | VERIFIED | https://www.risk.net/journal-of-risk/volume-3-number-2-winter-2000 |
| 73 | Gârleanu & Pedersen 2013 | VERIFIED | https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12080 |
| 74 | Perold 1988 | VERIFIED | https://www.pm-research.com/content/iijpormgmt/14/3/4 |
| 75 | Bouchaud et al. 2018 | VERIFIED | https://www.cambridge.org/core/books/abs/trades-quotes-and-prices/limit-order-books/8557B9B63548E46D15F91DC185DF624F |
| 76 | Tóth et al. 2011 | VERIFIED | https://arxiv.org/abs/1105.1694 |
| 77 | Markowitz 1952 | VERIFIED | https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1952.tb01525.x |
| 78 | Michaud 1989 | VERIFIED | https://www.jstor.org/stable/4479185 |
| 79 | DeMiguel, Garlappi & Uppal 2009 | VERIFIED | https://lbsresearch.london.edu/id/eprint/407/ |
| 80 | Ledoit & Wolf 2004 | VERIFIED | https://econpapers.repec.org/RePEc:eee:jmvana:v:88:y:2004:i:2:p:365-411 |
| 81 | Longin & Solnik 2001 | VERIFIED | https://econpapers.repec.org/RePEc:bla:jfinan:v:56:y:2001:i:2:p:649-676 |
| 82 | Hamilton 1989 | VERIFIED | https://www.econometricsociety.org/publications/econometrica/1989/03/01/new-approach-economic-analysis-nonstationary-time-series-and |
| 83 | Ang & Timmermann 2012 | VERIFIED | https://www.annualreviews.org/doi/abs/10.1146/annurev-financial-110311-101808 |
| 84 | Künsch 1989 | VERIFIED | https://projecteuclid.org/journals/annals-of-statistics/volume-17/issue-3/The-Jackknife-and-the-Bootstrap-for-General-Stationary-Observations/10.1214/aos/1176347265.full |
| 85 | Politis & Romano 1994 | VERIFIED | https://www.tandfonline.com/doi/abs/10.1080/01621459.1994.10476870 |
| 86 | White 2000 | VERIFIED | https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0262.00152 |
| 87 | Hansen 2005 | VERIFIED | https://ideas.repec.org/a/bes/jnlbes/v23y2005p365-380.html |
| 88 | Romano & Wolf 2005 | VERIFIED | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-0262.2005.00615.x |
| 89 | Benjamini & Hochberg 1995 | VERIFIED | https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1995.tb02031.x |
| 90 | Harvey, Liu & Zhu 2016 | VERIFIED | https://academic.oup.com/rfs/article/29/1/5/1843824 |
| 91 | Bailey & López de Prado 2014 | VERIFIED | https://www.pm-research.com/content/iijpormgmt/40/5/94 |
| 92 | Bailey et al. 2017 | VERIFIED | https://scholarworks.wmich.edu/math_pubs/42/ |
| 93 | López de Prado 2018 | VERIFIED | https://www.wiley.com/en-us/Advances+in+Financial+Machine+Learning-p-9781119482086 |
| 94 | Lo 2002 | VERIFIED | https://www.semanticscholar.org/paper/The-Statistics-of-Sharpe-Ratios-Lo/05561b77acfdd034a585c32048819cc9ba6d1434 |
| 95 | Goldberg 1991 | VERIFIED | https://dl.acm.org/doi/10.1145/103162.103163 |
| 96 | Higham 2002 | VERIFIED | https://epubs.siam.org/doi/abs/10.1137/1.9780898718027 |
| 97 | Moore, Kearfott & Cloud 2009 | VERIFIED | https://books.google.com/books/about/Introduction_to_Interval_Analysis.html?id=tT7ykKbqfEwC |
| 98 | Neumaier & Shcherbina 2004 | VERIFIED | https://link.springer.com/article/10.1007/s10107-003-0433-3 |
| 99 | IEEE 754-2019 | VERIFIED | https://standards.ieee.org/standard/754-2019.html |
| 100 | Cowlishaw 2009 | CORRECTED | https://speleotrove.com/decimal/ |
| 101 | MacIver, Hatfield-Dodds et al. 2019 | VERIFIED | https://joss.theoj.org/papers/10.21105/joss.01891 |
| 102 | Claessen & Hughes 2000 | VERIFIED | https://dl.acm.org/doi/10.1145/351240.351266 |
| 103 | Segura et al. 2016 | VERIFIED | https://eprints.whiterose.ac.uk/110335/ |
| 104 | Kupiec 1995 | VERIFIED | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7065 |
| 105 | Christoffersen 1998 | VERIFIED | https://econpapers.repec.org/RePEc:ier:iecrev:v:39:y:1998:i:4:p:841-62 |
| 106 | Vince 1992 | VERIFIED | https://www.wiley.com/en-us/The+Mathematics+of+Money+Management:+Risk+Analysis+Techniques+for+Traders-p-9780471547389 |
| 107 | Hsieh, Barmish & Gubner 2016 | VERIFIED | https://dl.acm.org/doi/10.1109/CDC.2016.7798825 |
| 108 | Cover 1991 | VERIFIED | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-9965.1991.tb00002.x |
| 109 | Rotando & Thorp 1992 | VERIFIED | https://escholarship.org/content/qt2sf6m38g/qt2sf6m38g.pdf |
| 110 | Maccheroni, Marinacci & Rustichini 2006 | VERIFIED | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1468-0262.2006.00716.x |
| 111 | Pflug & Pichler 2014 | VERIFIED | https://books.google.com/books/about/Multistage_Stochastic_Optimization.html?id=q_VWBQAAQBAJ |
| 112 | Altman 1999 | VERIFIED | https://openlibrary.org/books/OL97592M/Constrained_Markov_decision_processes |
| 113 | García & Fernández 2015 | VERIFIED | https://dblp.org/rec/journals/jmlr/GarciaF15.html |
| 114 | Hewing et al. 2020 | VERIFIED | https://www.annualreviews.org/content/journals/10.1146/annurev-control-090419-075625 |
| 115 | Kolm, Tütüncü & Fabozzi 2014 | VERIFIED | https://www.sciencedirect.com/science/article/abs/pii/S0377221713008898 |

## 4. Novelty mapping (brief §11 categories; no novelty is claimed)

| Component | Closest prior literature (from 11 §1) | Category |
|---|---|---|
| Kelly / fractional Kelly sizing inside caps | Kelly 1956; Breiman 1961; MacLean, Ziemba & Blazenko 1992; Thorp 2006 | KNOWN |
| Risk-constrained / distributionally robust growth | Busseti, Ryu & Boyd 2016; Sun & Boyd 2018; Rujeerapaiboon, Kuhn & Wiesemann 2016 | KNOWN |
| Cushion-proportional risk budget (floor preservation) | Black & Perold 1992; Grossman & Zhou 1993; Cvitanić & Karatzas 1995 | KNOWN |
| Gap-risk cushion multiplier ≤ 1/Γ | Balder, Brandl & Mahayni 2009 (CPPI gap risk under discrete trading) | KNOWN |
| Tiered guarantees U/S/G/L as nested disturbance sets with one-step invariance (T-10, T-21) | viability theory (Aubin 1991; Aubin, Bayen & Saint-Pierre 2011); set invariance (Blanchini 1999; Bertsekas 1972); robust MPC (Mayne, Seron & Raković 2005); CPPI | KNOWN COMBINATION (elementary results; likely known in some form) |
| Deterministic safety filter with exact projection around an arbitrary proposer | Wabersich & Zeilinger 2021; Alshiekh et al. 2018; Ames et al. 2019 | KNOWN |
| Feasibility-defined model caps for monotonicity in the ambiguity set (T-09) | DRO literature (Mohajerin Esfahani & Kuhn 2018; Ben-Tal et al. 2013); comparative statics not surveyed | POSSIBLE MATHEMATICAL NOVELTY — REQUIRES FORMAL COMPARISON |
| Certified advantage against no-trade using the infimum of the difference (P-12a) | maxmin / multiple priors (Gilboa & Schmeidler 1989); robust optimisation | KNOWN (the inequality is elementary) |
| Binary64 floor-safety condition (T-22) | Higham 2002; Goldberg 1991; Neumaier & Shcherbina 2004 | KNOWN (standard error analysis applied to one operation) |
| Directed-rounding table + certified non-rational evaluation for a risk engine | interval arithmetic (Moore, Kearfott & Cloud 2009) | KNOWN COMBINATION |
| Composition: snapshot-bound pure exact engine + tiered envelope + feasibility-defined model caps + certified no-trade comparison + evidence hashing | industry practice largely unpublished; safety filters; robust control | POSSIBLE SYSTEMS NOVELTY (unverified; requires prior-art search L-6) |
| Any claim of "new risk formula" | — | UNSUPPORTED NOVELTY CLAIM (none is made) |
