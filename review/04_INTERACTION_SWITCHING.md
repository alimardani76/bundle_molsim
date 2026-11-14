# Phase 4 — attraction switching and the reverse interaction path

**Verdict: PARTIAL.** The saved production is complete: **192/192 gas-paired seed/condition records, zero failures**, represented by 24 common-configuration energy traces. All 56 interior-lambda and eight WCA+Coulomb framework-level estimates pass the registered precision checks. The neutral attraction-switching curves and reverse-path electrostatic contrasts support bounded conclusions for these eight frameworks. A complete four-corner convergence claim is unsupported: M084 full-mode CO2 fails the registered pooled insertion-weight ESS target, M085 full-mode CO2 retains rare-tail limitations, and several nonadditivity/crossing statements do not resolve under simultaneous intervals. No simulation was launched for this analysis.

The fixed panel is M002, M029, M043, M085, M089, M192, M084 and M171. These are selected examples, not a representative sample of the 238-framework population. Reviewer scope: Miguel **M10–M12, M59**, and Uzair **U18**. The source comments are in `evidence/provenance/forensic/REVIEW_COMMENT_REGISTER.csv`; this report does not modify their historical status fields.

**What was calculated.** Define `L=ln S(CO2/N2)`, with `00=WCA`, `10=full LJ, charges off`, `01=WCA+Coulomb`, and `11=full LJ+Coulomb`. The two orders give

```text
A0 = L10 − L00             E1 = L11 − L10
E0 = L01 − L00             A1 = L11 − L01
I  = E1 − E0 = A1 − A0 = L11 − L10 − L01 + L00
A0 + E1 = E0 + A1 = L11 − L00.
```

The final selectivity remains a state property. A nonzero I means that the **allocation into incremental contributions depends on switching order**, not that the total equilibrium selectivity depends on the route. Here “attraction increment” means the specified LJ–WCA complement on this force-field path; it does not mean all physically attractive interactions or an isolated, uniquely observable dispersion contribution. Coulomb interactions can also be attractive or repulsive.

The saved protocol uses the unchanged rigid structures, guest geometries, framework/guest force-field parameters, periodic cells, 298 K temperature and native full-mode Ewald treatment. Native RASPALIB 3.0.29 supplies separate LJ/Coulomb energies; the Phase 1B/1C validated kernel supplies WCA energies. The original finite LJ cutoff/shift convention is retained. Existing engine unit constants are retained, including the WCA/RASPA conversion difference; no interaction parameter was adjusted. The already completed M002 fixed-pose and stochastic endpoint gate is PASS (`work/phase4_interaction_switching_20261114/control/endpoint_gate.json`); it was not rerun here and does not establish convergence of other frameworks.

Three independent PCG64 replicate streams per framework use `SeedSequence([20261114, framework_number, seed_label])`, labels 58101–58103, and the preserved isotropic configurations. A numerical seed label does not identify the original RASPA random stream. Gas/state configurations are deliberately shared, so those results are correlated. Each new 01 condition uses 1,000,000 attempts/gas/seed; each interior lambda uses the first 200,000. These match the original nominal 50,000-/10,000-cycle insertion budgets; fixed equal gas counts differ from native stochastic component allocation. One native energy trace is cross-scored at the registered states; 192 records are not 192 independent streams. Original 10/11 endpoints are retained, and 00 reuses corrected WCA factors. Additional corner energies on these same poses are diagnostics, not extra simulations.

All reported L values use **mean seed log ratios**, matching original RASPA aggregation. Frozen Phase 1C instead uses the log ratio of pooled gas factors. The largest difference for these eight 00 endpoints is only 0.0000235918 (M171), but the estimators are explicitly distinguished in `04_INTERACTION_NONADDITIVITY.csv`. Neither frozen table is changed. New B values are dimensionless insertion-factor means, not absolute Henry coefficients. Original KH values have units mol kg^-1 Pa^-1. Only their within-framework CO2/N2 ratios are compared; the common Henry normalization cancellation was checked in the completed M002 gate. No cross-framework absolute-Henry normalization is invented.

**Nine-point neutral attraction-switching curves.** The implemented potential is `U(lambda)=(1−lambda)U_WCA+lambda U_LJ`, with charges off. Entries below are mean seed ln S. Full precision, gas-specific estimates, standard errors, pointwise/simultaneous intervals, ESS and source paths are in [04_ATTRACTION_SWITCHING.csv](04_ATTRACTION_SWITCHING.csv).

| lambda | M002 | M029 | M043 | M085 | M089 | M192 | M084 | M171 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | -0.110601 | -0.233861 | -0.228057 | -0.239605 | -0.298779 | -0.270294 | -0.293158 | -0.670855 |
| 0.05 | -0.067003 | -0.140483 | -0.140583 | -0.163050 | -0.179743 | -0.141604 | -0.205357 | -0.479427 |
| 0.10 | -0.020856 | -0.043169 | -0.049112 | -0.086957 | -0.060703 | -0.009697 | -0.113806 | -0.278810 |
| 0.20 | 0.078421 | 0.164486 | 0.146461 | 0.072529 | 0.181005 | 0.263078 | 0.075517 | 0.127033 |
| 0.35 | 0.248052 | 0.514076 | 0.478429 | 0.333493 | 0.552988 | 0.697839 | 0.376338 | 0.747805 |
| 0.50 | 0.448509 | 0.916418 | 0.867184 | 0.628056 | 0.936772 | 1.168308 | 0.699550 | 1.383629 |
| 0.70 | 0.776558 | 1.539745 | 1.485763 | 1.094348 | 1.467603 | 1.858942 | 1.169917 | 2.255662 |
| 0.85 | 1.077328 | 2.067610 | 2.023022 | 1.520665 | 1.880441 | 2.427224 | 1.555906 | 2.928171 |
| 1 | 1.439556 | 2.638083 | 2.609497 | 2.012835 | 2.304527 | 3.035516 | 1.983195 | 3.610760 |

All eight curves have increasing point estimates on the tested grid. All eight remain N2-favored at lambda=0.05 even under the 72-point simultaneous intervals. All eight are negative at 0.10 and positive at 0.20 under pointwise 95% intervals. Thus the measured adjacent-node reversal bracket is **(0.10, 0.20)** in every example. This is direct intermediate-potential evidence, not interpolation from endpoints. It contradicts a claim that preference switches at any nonzero complement strength in these examples. It does not locate an exact, unique or minimum crossing: unmeasured behavior between nodes and nonmonotonic excursions are not excluded.

| Framework(s) | Pointwise adjacent-node bracket | Simultaneous adjacent-node bracket | Wider bounds between simultaneous resolved signs |
|---|---|---|---|
| M002, M029, M043, M089, M192 | (0.10, 0.20) | Unresolved | (0.05, 0.20) |
| M085 | (0.10, 0.20) | (0.10, 0.20) | (0.10, 0.20) |
| M084 | (0.10, 0.20) | (0.10, 0.20), marginal | (0.10, 0.20) |
| M171 | (0.10, 0.20) | Unresolved | (0.05, 0.35) |

The wider bounds include uncertain intervening grid nodes and are not reported as resolved adjacent-node crossings. M084's simultaneous lower bound at lambda=0.20 is only **+0.000130311**, so its narrow simultaneous bracket is particularly marginal. [04_CROSSINGS.csv](04_CROSSINGS.csv) preserves these distinctions. No interpolated crossing coordinate, threshold fit, new lambda or monotonicity assumption is used.

**Reverse-order electrostatics and nonadditivity.** E0 adds charges to WCA; E1 adds charges after LJ. The primary I uses unchanged original 10/11 endpoints. In the table, E0 parentheses contain its estimated SE; I brackets are pointwise 95% t-scaled intervals using the estimated unknown-cross-state-covariance SE bound. These intervals remain conditional on adequate sampling.

| MOF | E0 (SE) | E1 | Primary I [pointwise interval] | Common-pose I (SE), diagnostic |
|---|---:|---:|---:|---:|
| M002 | 0.108572 (0.000471) | 0.572640 | 0.464068 [0.372772, 0.555365] | 0.482736 (0.009990) |
| M029 | -0.033912 (0.001270) | 0.140695 | 0.174607 [0.134714, 0.214501] | 0.169475 (0.007838) |
| M043 | -0.014853 (0.000734) | 0.108650 | 0.123503 [0.057595, 0.189412] | 0.124662 (0.014925) |
| M085 | 0.458570 (0.007365) | 2.000689 | 1.542119 [1.188723, 1.895515] | 1.438817 (0.017366), tail-qualified |
| M089 | 0.334095 (0.002982) | 0.465717 | 0.131622 [0.050988, 0.212257] | 0.130885 (0.002240) |
| M192 | 0.047469 (0.001282) | 0.139862 | 0.092392 [0.053650, 0.131135] | 0.090421 (0.004886) |
| M084 | 0.534699 (0.007363) | 1.720186 | 1.185486 [0.987047, 1.383925] | 1.188994 (0.028983), **ESS fail** |
| M171 | -0.102490 (0.002981) | 0.054848 | 0.157338 [0.111092, 0.203583] | 0.153436 (0.003753) |

E0 is negative for **M029, M043 and M171**, and positive for the other five; all eight E0 signs resolve in the secondary eight-framework Bonferroni comparison. Thus charges do not universally favor CO2 relative to N2 on the WCA reference. E1 point estimates are positive in all eight. A positive charging increment also need not establish final CO2 preference: M002's L01 is -0.00202879, with pointwise interval [-0.00425688, +0.00019930], so its charged-WCA preference is unresolved.

All primary I pointwise intervals exclude zero, conditional on the uncertainty assumptions. Under the eight-test family comparison using the unknown-covariance bound, I remains positive for **M002, M029, M085, M084 and M171**; **M043, M089 and M192 remain unresolved**, not demonstrated additive. Their family intervals are respectively [-0.069346, 0.316353], [-0.104318, 0.367562], and [-0.020969, 0.205754]. The M084 and M085 positive estimates retain the full-mode sampling qualifications below. The common-pose calculation, which measures covariance directly, resolves seven of eight family intervals (M043 remains unresolved), but its M084 ESS failure prevents a reliable convergence-certified I claim. It is a diagnostic estimator with different finite samples and does not replace the registered primary endpoints.

A0 ranges from **1.550157 (M002) to 4.281615 (M171)**; A1 ranges from **2.014226 to 4.438953** for those same endpoints. Their differences equal I. For M085, A0=2.252440 and A1=3.794559; E0=0.458570 versus E1=2.000689. Its reverse gas-specific changes are +0.488672 in mean ln B(CO2) and +0.030102 in mean ln B(N2). These quantify coupling in the specified model, not a unique binding mechanism or a physically separable percentage of selectivity. Exact M085/M084 effect rankings are not established. Complete four-state values, both A/E orders, estimated SEs and pointwise/family intervals are in [04_INTERACTION_NONADDITIVITY.csv](04_INTERACTION_NONADDITIVITY.csv).

**Uncertainty conventions and sampling limits.** Existing `analyze.py` routines provide seed log ratios, within-run raw and fixed 10,000-pose-block estimates, and first/second-half diagnostics. For a new mean, SE is the maximum of between-seed SE and the two propagated within-run estimates. Paired gas/state influence functions retain the actual common-configuration covariance for E0 and common-pose I. Three independent replicates give df=2 t intervals; curve simultaneous intervals use Bonferroni over 72 points, and I uses eight tests. The secondary E0 family also uses eight tests. These are approximate finite-sample Monte Carlo intervals, not rigorous bounds on unsampled tails.

For original endpoints, SE is the maximum of paired seed-log-ratio variation and propagated native block uncertainty. Native reported five-block halfwidths are converted using the existing 2.776 factor; they are not counted as independent runs. Unknown within-job gas covariance uses the sum-of-gas-SE bound. Unknown original cross-state covariance is not invented: the primary I CSV reports both an independence approximation and the conservative estimated bound `SE11+SE10+SE(E0)`. The table uses the latter with df=2. A t-scaled estimated-SE bound is not a distribution-free confidence guarantee. The 72-point curve CSV explicitly marks original LJ insertion-weight streams unavailable, rather than certifying historical ESS from later cross-scores.

The registered new-state targets are SE(L)<=0.10, pooled concentration ESS>=1000/gas and the 4.5-SE half-run guard. **All 64 new framework/state aggregates pass without relaxing any threshold**: maximum SE=0.01320575 (M171, lambda=0.85), minimum pooled ESS=5214.72 (its CO2 weights), maximum half-run z=1.71010. The smallest individual new-state seed ESS is 1691.40; the largest single-pose weight fraction is 0.00511938 (M085 CO2, lambda=0.85). These are useful finite-sample diagnostics, not a proof of no missed configurations.

On common uniform poses, adjacent-lambda Bhattacharyya coefficients are **0.974727–0.999911**; 00→01 coefficients are **0.798040–0.997395**; 10→11 coefficients are **0.580118–0.994764**. The lowest charge-switch overlap is M084 CO2. These describe normalized insertion-weight overlap in the sampled poses. They do not establish connectivity, transport accessibility, or reliable arbitrary importance reweighting. The calculation directly integrates each potential over uniform positions/isotropic orientations; it does not sample a loaded LJ Boltzmann trajectory and reweight it into WCA. High sampled overlap cannot reveal an unsampled rare tail. The 480 per-seed/gas overlap entries are in [04_WEIGHT_OVERLAP.csv](04_WEIGHT_OVERLAP.csv).

Two full-mode limitations matter despite zero execution failures:

- **M084:** full-CO2 pooled cross-score ESS is **871.43**, below 1000; per-seed ESS is 204.91, 353.04 and 398.37. One pose contributes up to **3.604%** of a seed's total weight. The original full-CO2 native relative halfwidth reaches **18.05%**. Its common-pose I cannot support a precision-qualified four-corner conclusion; the primary I remains a conditional numerical estimate. Its neutral lambda curve and 01 results pass their own checks and are not invalidated by this separate full-mode failure.
- **M085:** full-CO2 pooled cross-score ESS is **1868.27**, while each seed has only **608.38–641.31** effective weight contributions; maximum single-pose fraction is **0.8181%**. The original full-CO2 relative native halfwidth reaches **44.00%**. The common-pose full L is 3.915063 versus historical 4.013524. Three similar estimates or a pooled-ESS pass do not close its rare-event uncertainty. The Phase 2 independent evidence and remaining limitations in `02_M085_AND_STRUCTURES.md` still apply; Phase 4 neither pools those six runs into the frozen endpoint nor treats repeated seed labels as independent confirmation. A qualified coupling example is supported; an exact historical mean, convergence certificate, effect ranking or accessible-pore claim is not.

No sampled-state agreement establishes connected, orientation-feasible pore accessibility. No accessibility analysis or atomic-site interpretation was performed. For M043/M089/M192, the unresolved primary family intervals prevent an all-eight, simultaneously resolved nonadditivity claim even though their pointwise estimates are positive. For six frameworks, the narrow adjacent-node crossing is not simultaneously resolved; wider sign bounds are reported instead. No additional sampling is implied or requested by this report.

**Reviewer-facing conclusions.**

| Comment | Finding and permissible conclusion |
|---|---|
| M10, M11 | Define “attraction increment” as the specified LJ attractive complement relative to WCA, with charges off. Electrostatic attraction is not included in that name. The quantitative decomposition must state its order; it is not a unique physical partition. |
| M12 | Common configurations have been scored under WCA, LJ, Coulomb and their registered combinations, with explicit covariance and overlap diagnostics. This supports an energy-switching comparison in the Widom insertion measure. It does not certify general LJ-ensemble↔WCA importance reweighting; original endpoint weight streams and tail guarantees remain unavailable. |
| M59 | Nine actual lambda values show N2 preference at 5% and 10%, followed by CO2 preference at 20% under pointwise intervals in all eight. Report measured grid brackets and the wider simultaneous bounds; do not claim an infinitesimal-attraction reversal, an exact threshold, uniqueness or population universality. |
| U18 | The measured reverse 01 state demonstrates reference-dependent charging increments, including three negative E0 effects. I quantifies nonadditivity of the increments while the total cycle closes algebraically. M084/M085 full-mode limits and unresolved family comparisons must accompany the claim. |

**Files and reproducibility.** The five essential CSVs linked above contain 72 curve points, eight crossing rows, eight cycle rows, 312 seed/source rows and 480 overlap rows. [04_SEED_RESULTS.csv](04_SEED_RESULTS.csv) distinguishes the 192 new authorized condition records, 72 reused-configuration diagnostic corner records and 48 original RASPA seed records. Its B and KH fields are explicitly separate. All paths are relative to `D:/P01`. Saved per-condition JSONs, diagnostics, poses, native reduced-energy arrays, checkpoints, source hashes and the frozen execution protocol remain under `work/phase4_interaction_switching_20261114`; no redundant scientific evidence copies are created.

The analysis-only command is:

```powershell
Set-Location D:\P01
.\.venv\Scripts\python.exe work\phase4_interaction_switching_20261114\summarize.py
```

It imports the existing `analyze.py` aggregation routines, reads saved records, writes the five CSVs and a scientific intermediate `analysis_summary.json`, and has no simulation entry point. Production, replay and endpoint-validation commands were not executed for this analysis. Original scientific data identities remain:

| Source | SHA-256 |
|---|---|
| `repo/data/authoritative/mechanism_238_authoritative.csv` | `f317eef220e6f8757be6aa8d6e4ec29b9bf90e0eeaad8d86009a265b65b1b149` |
| `repo/review/01C_CORRECTED_WCA_238.csv` | `728c320511be4e9873f07f4b4d222347e1d8ba8a5cb7130b5effdb6a240e62d7` |
| `repo/data/provenance/raspa_final_gas_rows.csv` | `f51d299450f0e9c6e348e3e4dd0a59966260d03a591fc1d0540e18575f8e825a` |
| Phase 1B/1C WCA kernel `work/phase1c_corrected_wca_20261114/scripts/wca_model.py` | `7f32df788cc05a02d1e4ae556f7c4634ba2f91eb91d37246673f191bc45854e0` |
| Frozen native backend `work/phase4_interaction_switching_20261114/fixed_position_energy_frozen.py` | `be398e4c9d8423250d427f4c56b59895552dfa4c2fd1df7daa8de66835b3aa59` |

The protocol and analysis-source hashes are recorded in the scientific intermediate. **Stop: PARTIAL**, with numerical switching/reverse-path evidence delivered and the precise remaining limits above. No new simulation, figure, manuscript change or next phase was initiated.
