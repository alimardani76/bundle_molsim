# Phase3 — fixed ML validation using existing structures and targets

**Scientific verdict: PARTIAL.** Completed corrected geometry OOF results were reused with **zero geometry refits**. A single predefined three-charge-feature comparison substantially improves E prediction in this panel: R2=0.188040 geometry,0.349725 charge-only,0.602657 combined. Geometry still predicts WCA/A much better than E, and combined A remains better predicted than combined E. This is a fixed random-fold, within-panel result; independently supported structural/topology groups are absent, so **no group-aware fit or extrapolation PASS is claimed**. Nothing was tuned after inspecting scores.

## Frozen inputs and evaluation

All 238 original retained frameworks are used; only WCA and A targets use01C_CORRECTED_WCA_238.csv. LJ/full/E remain unchanged; Phase2 M085 diagnostic estimates are not selectively mixed into targets. The exact 14 geometry columns are listed in 03_EXISTING_DATA_PHYSICS.md and 03_DESCRIPTOR_DEFINITIONS.csv.

The small feature set was fixed before fitting: **charge_min_e=min(q_i), charge_max_e=max(q_i), charge_rms_e=sqrt(mean(q_i²))**, over all original charged P1 framework sites. Each CIF charge/atom label/element matches the original full-mode pseudoatom model; all 238 sources and hashes are in 03_CHARGE_FEATURES.csv. Features use framework partial charges only, in e. They use no Henry coefficient, gas insertion, WCA/LJ/full energy, response, prediction, rank, framework ID, metal label or test-set target. They are simulation-independent with respect to adsorption sampling, not independent of the study's pre-existing electronic charge assignment. No field grid, orientation, new charge calculation, alternative descriptor panel or feature search was added.

Geometry-only 14 uses completed saved OOF predictions; charge-only 3 and combined 17 each reuse the original ExtraTrees algorithm and explicit hyperparameters: `n_estimators=500`, `min_samples_leaf=3`, `max_features=0.7`, `random_state=20260918`. Original ColumnTransformer numeric median imputation and StandardScaler are fitted only on training folds; empty categorical branches are retained. The original source AST constructs and calls the actual pipeline, not a substitute model. Original KFold5 shuffle seed 20260918 matches every saved fold membership and unchanged row order. max_features stays the same fraction; absolute candidate-feature counts naturally differ by panel size.

Exactly 8 target/panel CV predictions (40 fold-specific fits) were executed for charge/combined, with no geometry retraining, extra split, tuning, model selection or failed-score suppression. The initial integration NameError occurred before any estimator fit and was repaired by supplying the original outer-loop y; its trace is preserved in work. The same four targets and folds are used for all panels. Combined uses geometry 14 in original order, followed by the three fixed charge columns.

The reference is now the **training-fold target median**, predicted on that fold's held-out rows. It is not the old full-cohort-median descriptive reference. Both are distinguished in 03_ML_METRICS.csv. R2/MAE/bias are computed from concatenated OOF predictions across all 238, rather than averages of fold scores. Bias=mean(predicted−observed); target units are dimensionless natural logs. Feature calculation itself uses only the individual structure, requiring no cohort fit; preprocessing uses no held-out information.

## Numerical comparison

| Target | Fixed panel | OOF R2 | MAE | Bias (pred−obs) | MAE/training-median MAE |
|---|---|---|---|---|---|
| lnS_wca | geometry | 0.967505598 | 0.014228182 | -0.000495350 | 0.144275 |
| lnS_wca | charge | 0.288733694 | 0.081995283 | -0.000354206 | 0.831441 |
| lnS_wca | combined | 0.967716568 | 0.013932575 | -0.000303844 | 0.141278 |
| delta_lnS_attr | geometry | 0.879658475 | 0.176148834 | 0.004079012 | 0.316252 |
| delta_lnS_attr | charge | 0.456270034 | 0.431470894 | 0.002354185 | 0.774649 |
| delta_lnS_attr | combined | 0.911093371 | 0.151540394 | 0.004816265 | 0.272071 |
| delta_lnS_elec | geometry | 0.188039984 | 0.146023953 | -0.001567996 | 0.991659 |
| delta_lnS_elec | charge | 0.349725153 | 0.137485465 | 0.000113280 | 0.933674 |
| delta_lnS_elec | combined | 0.602657232 | 0.107977072 | -0.002680377 | 0.733280 |
| lnS_full | geometry | 0.845240527 | 0.188768270 | -0.001327254 | 0.376129 |
| lnS_full | charge | 0.338895253 | 0.409899668 | 0.002706274 | 0.816742 |
| lnS_full | combined | 0.859464217 | 0.180722442 | -0.003341679 | 0.360097 |

The completed geometry correction changed WCA R2 from 0.835027 to 0.967506 and A from 0.874487 to 0.879658; those fits were not repeated. Saved E/full geometry R2 remain 0.188040/0.845241. Geometry's A−E R2 gap is **0.691618491**; with the fixed combined feature panel it is **0.308436140**. The distinction narrows with charge information but does not disappear. Geometry-plus-charge E MAE0.107977 is about 26.7% below its training-fold-median baseline, whereas geometry-only E MAE0.146024 is only about 0.8% below it. Charge-only is better than geometry-only for E but worse for WCA, A and full endpoint. This is complementarity within a fixed protocol, not evidence that three charge moments are sufficient or causal.

For M28/M30: the models predict four nested **log-selectivity/increment targets**, not gas-specific Henry constants. A high endpoint score therefore does not demonstrate recovery of each physical coordinate. M05's external-generalization concern remains unresolved without valid held-out structural groups; random folds do not establish transfer to unseen chemistry.

## Target skew and tail diagnostics (U24)

E has mean 0.369016208, median 0.309492037,90th percentile 0.513642113,99th percentile 1.689961077,maximum 2.000688635. The fixed upper 24 account for **81.072%** of total squared deviations from the mean. Thus a small high-E tail strongly influences the R2 denominator, while MAE weights all residuals linearly. R2 and MAE answer different questions; neither alone establishes uniform predictability. Tail diagnostics use bottom/top 24 by observed target then ID, fixed before fitting; they do not define training or trigger tuning.

| E model | All 238 MAE | All 238 bias | Upper24 MAE | Upper24 bias | Upper24 median-baseline MAE |
|---|---|---|---|---|---|
| geometry | 0.146023953 | -0.001567996 | 0.540466727 | -0.540466727 | 0.707021760 |
| charge | 0.137485465 | 0.000113280 | 0.466054233 | -0.432532549 | 0.707021760 |
| combined | 0.107977072 | -0.002680377 | 0.380944623 | -0.320727666 | 0.707021760 |

All models underpredict the high-E tail. Combined features reduce that bias but the upper 24 mean bias remains -0.320728, despite nearly zero whole-cohort bias. A small aggregate bias is not calibrated recognition of high-E frameworks. All target/panel bottom 24 and top 24 MAE/bias values are retained, rather than only the favorable E result. Tail R2 is deliberately not reported for its restricted target range. No outlier was removed and no extra model was trained after inspecting tails. Native simulation label uncertainty (especially M085) and source-panel selection remain outside these predictive residuals.

## Group-aware validation gate (U23)

**NOT_ESTABLISHED; zero grouped fits.** The original source has group_column=null and the authoritative training table has no authenticated topology, topology_family, metal_cluster or geometry_cluster column. None of the 238 inspected CIFs contains an independently assigned topology/SBU group tag. Database suffixes (including fsc), the two DB prefixes, P1 crystallographic symmetry and PCA-derived strata do not authenticate framework-net groups. Parsing actual CIFs verifies210 Co-containing and 28 Ni-containing frameworks, exactly aligning with the two identifier subsets; these are elemental classes, not SBU/net groups or a validated multi-family topology partition. No invented five-fold GroupKFold or unrequested alternative metal-extrapolation experiment was run.

Consequently these results cannot establish topology/chemistry generalization, family-independent causal descriptor value or error-compensation robustness beyond the original panel. The exact missing input for that stronger claim is an independently supported structural grouping per framework with a defensible held-out-family design. The current task stops with that limitation; no new dataset or structural investigation is initiated.

## Runtime, scope and claim disposition

Current tested versions: scikit-learn 1.9.0,NumPy 1.26.4,pandas 2.3.2,SciPy 1.17.1. Completed WCA/A geometry OOF was produced in this same tested runtime. E/full geometry OOF is the preserved archive; its exact historical estimator environment was not locked. All explicit source settings and fold memberships match, but this is not an authenticated binary-environment comparison for those two archived controls. Small gains cannot be isolated from version effects, and score differences are descriptive rather than a formal causal feature test. The old bootstrap intervals are not transferred to corrected/new scores.

- **Survives:** geometry predicts corrected WCA/A substantially better than E within this panel (M28,M30,U21); the four-target decomposition exposes information hidden by a high endpoint score (M05,M45–M48).
- **New bounded support:** fixed charge-only and combined descriptors add E information without gas-output leakage (M38,U25). This positive result was obtained without tuning; it does not establish an atomic binding-site mechanism or a universal charge law.
- **Must be qualified:** any claim that E is intrinsically unpredictable from all simulation-independent descriptors, that near-zero whole-panel bias resolves the E tail, or that random-fold scores demonstrate new-family generalization. Skew/tail errors and missing structural holdouts remain explicit (U23,U24).
- **Unresolved identity labels:** actual metal composition is verified, but SBU/linker/topology assignments and broad database-family interpretation remain unsupported (M34,M49,M58). No topology label was guessed from an identifier.

Essential results:03_ML_METRICS.csv (all/tails),03_ML_OOF.csv (2856 predictions, including reused geometry),03_CHARGE_FEATURES.csv (238 original structures). Sources: original descriptor_fit_archived.py.txt,geometry_cv_protocol.json,descriptor_feature_manifest.csv,geometry_fold_membership.csv; completed01C geometry OOF and original E/full OOF. Fixed choices and minimal science scripts are underwork/phase3_existing_20261114. No simulations, new source datasets, alternate models, figures, manuscript edits or GitHub changes occurred. **Stop: Phase3 PARTIAL for structural generalization and uncertainty claims; numerical comparisons above are complete.**
