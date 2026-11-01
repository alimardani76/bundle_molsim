# Reconciled v9 numerical audit

The original 238-framework cohort is byte-identical to v9: SHA-256 `f317eef220e6f8757be6aa8d6e4ec29b9bf90e0eeaad8d86009a265b65b1b149`. No RASPA/LAMMPS calculation or model fitting was performed.

The current independent saved-evidence audit has **6,436 comparisons and 0 failures**. The machine-readable record is `NUMERICAL_RECONCILIATION.csv`; `final_evidence_audit.json` records the full bootstrap and replay scope. Final publication additionally requires the document, figure, checksum and clean-environment gates recorded in `release_check.json` and `VALIDATION_COMMANDS.json`.

| Evidence | Verified count/result |
|---|---:|
| Frameworks / gas–state aggregates | 238 / 1,428 |
| WCA archive-wide / retained / excluded gas-specific jobs | 2,052 / 2,034 / 18 |
| Full/LJ gas-specific result rows, all / retained | 2,960 / 2,920 |
| Restored final geometry OOF vectors | 952 rows = 238 × four targets |
| Regression / matching descriptor count | 14 / nine |
| All unique framework pairs / closest-2% candidates | 28,203 / 564 |
| Archived initial / lower-quartile pair candidates | 384 / 96 |
| Main / SI / TOC figures | six / four / one |

The initial audit's verified medians, signs, family counts, endpoint statistics, ranks and top-24 overlaps are preserved by keeping the exact original cohort. The restored final OOF predictions reproduce the original final metric transcription, including attraction R² 0.8744874648851713 and electrostatic R² 0.18803998403816946, within floating-point tolerance. Rounded article values are unchanged. A neighboring 25-feature model and the earlier v2 model are explicitly excluded as substitutes.

All three nested identities pass an absolute tolerance of **1e-12** log units; fresh CSV closure is at machine precision (maximum approximately 8.9e-16). Ordinary unrounded summaries use 1e-10 absolute tolerance; manuscript rounding uses half the displayed final unit. Full/LJ archived seed summaries are independently aggregated in log-Henry space, with Henry units mol kg^-1 Pa^-1, and WCA summaries are independently pooled in dimensionless Boltzmann-factor space. No primary simulation values were synthesized.

The previously unresolved 18 WCA jobs belong to the two excluded frameworks: `DB0-m15_o11_o139_f0_fsc` contributes six jobs and `DB0-m15_o14_o50_f0_fsc` contributes twelve. The SI distinguishes the archive total from retained jobs.

Both pair rules are reproducible and documented in `docs/PAIR_SELECTION.md`. The historical nearest-three/index-restricted/lower-quartile procedure reproduces the original examples. Exhaustive closest-2% optima are separately labelled M099/M136 (attraction) and M043/M085 (electrostatics). The examples M089/M192 and M029/M085 remain unchanged; their Figure 4 curve/contrast data are not replaced.

## Restored prediction and uncertainty evidence

The original prediction file, exact metric file and feature manifest match two historical copies and their recorded authoritative-file SHA-256 digests. The geometry subset is 952 of 1,904 saved rows. All observed vectors align with the unchanged cohort; normalized prediction exports retain the saved values. The full-cohort median-reference definition is made explicit.

The archived pipeline puts median imputation and standardization inside the training-fold pipeline. The final manifest contains only 14 pre-simulation geometry columns. This checks the source protocol and saved vectors; no estimator was refitted to test its execution. Fold IDs are reconstructed from the recorded KFold5 shuffle seed 20260918 and original row order, and are labelled as reconstructed metadata rather than an independently saved fold artifact.

The 5,000-resample bootstrap (seed 20260920) reproduces every archived 95% interval, including G = 0.6864474808470018 and G interval **[0.5597498842208415, 0.9053752180468466]**. Framework bootstrapping measures sensitivity to resampling the observed cohort; it does not establish seed-level significance or external transfer.

Saved-stratum replay independently reproduces 10,000 shuffles for each of two targets and each of 8/10/12 strata, without refitting prediction or PCA models. The PC variance percentage is checked using singular values of the fixed descriptor matrix. The secondary diagnostic does not establish electrostatic independence from geometry.

The 90 paired bridge seed rows reproduce the 30 framework/gas means and reported MAEs, maximum shifts and rank correlations. The 6,000/10,000-position saved pilot tables reproduce the twelve descriptor-convergence statistics and the two rank-order checks; only one feature converges at the archived threshold. The failed probe preflight remains a non-supporting historical diagnostic. No new energy evaluations or downstream probe model were run.

For seed-level uncertainty, Var(X−Y) = Var(X)+Var(Y)−2Cov(X,Y). Independent quadrature uses the zero-covariance assumption; matched-seed covariance requires aligned records and cannot be replaced by a framework bootstrap. The WCA diagnostic still has 19 upper approximate 95% bounds touching/exceeding zero, despite 238 negative point estimates. Seven shortlist entries are replaced at point estimates; no per-material significance or process-performance claim is added.

## Resolved release inconsistencies and limits

The false missing/source-availability conflict is resolved by actual restoration. The nine/14 mix-up, pair-rule claim, omitted main Figure 4, Figure 3 caption, literal TeX escapes, SI S numbering and TOC overlap are corrected. Unsupported composition/topology assertions from identifiers and unsupported temporal preregistration assertions are removed. Recorded molecular protocol/guest/force-field evidence is restored, without claiming a complete fresh simulation replay or exact structural-release snapshot.

Historical checksum inconsistencies are retained as a provenance note, not retroactively marked PASS. The reconciled checksum manifests are new records over existing selected files. Original v9 and archive inputs are preserved; historical bulk, private submission drafts, engine/vendor directories and caches are excluded from the public repository.
