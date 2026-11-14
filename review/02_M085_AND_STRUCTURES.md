# Phase2 — M085 reliability, structures and pore accessibility

**Verdict: PARTIAL.** Six new independent M085 full-mode jobs completed successfully at the original 50,000-cycle settings. Numerical reliability under the assessed sampling gates: **PARTIAL**; fresh/combined primary gate disposition: **PASS**; native uncertainty warning: **True**. Connected, orientation-feasible pore accessibility remains **NOT_ESTABLISHED**. The defensible role is a qualified, model-specific numerical example; unconditional convergence, accessible-pore and atom-specific motif claims are not established. No calculation beyond the authorized six jobs is run or proposed as an automatic continuation.

The bounded independent evidence **supports a large, predominantly CO2-driven electrostatic response within the original unrestricted rigid-framework model**. The M085-minus-M029 E contrast is 1.793289090 from fresh6 (factor 6.009185) and 1.815523861 in the diagnostic nine-seed pool (factor 6.144294), versus the historical1.859993403/factor6.423694. The pooled contrast has propagated max(seed,block) SE 0.03696060 under component independence, or estimated unknown-covariance SE bound 0.06119322. This supports the qualitative model contrast, not unconditional rare-event closure, the exact historical factor, pore accessibility or an atomic mechanism.

## Independent convergence and rare events

RASPA3 3.0.29 executable SHA256 `37ab1e47c0fddaf70a28e5c27c838cc9e4bee3a9f12a87505793f5059e32df91`; original rigid charged CIF, force field, guests, Ewald,298K,3x2x4 replication,50,000 cycles,zero initialization and both original gas components were preserved. The only simulation-input change is RandomSeed2026111401–2026111406. Seeds are authenticated by the executed input and native output, with separate process initialization, rather than filenames. These reconstructed inputs are new executions, not preserved historical decks. All six were completed regardless of agreement; no same-seed replay or smoke output is counted as independent evidence. The original parser and tested runner functions were reused. No WCA, LJ-only, control-framework or other simulations were executed.

Henry units below are **mol kg^-1 Pa^-1**. Each original or new full-mode seed is an independent-run unit. Existing shorter CO2-only20,000-cycle runs are separate evidence and are not pooled with the matched50,000-cycle two-component jobs. `combined9_50k` means original3 plus new6, not nine additional runs.

| MOF | Cohort | Gas | n | Geometric KH | SE(mean lnKH) | CV(KH) | Median native +/- / KH | Pooled block log-SE approx |
|---|---|---|---|---|---|---|---|---|
| M002 | original50k | CO2 | 3 | 2.3314148e-05 | 0.0006086145 | 0.00105 | 3.697% | 0.00668291 |
| M002 | original50k | N2 | 3 | 3.11697658e-06 | 0.01495212 | 0.02594 | 4.412% | 0.0110303 |
| M029 | original50k | CO2 | 3 | 0.000100821002 | 0.001902359 | 0.00330 | 1.463% | 0.00314687 |
| M029 | original50k | N2 | 3 | 6.26243391e-06 | 0.0002591152 | 0.00045 | 0.977% | 0.00177011 |
| M085 | original50k | CO2 | 3 | 8.28392076e-05 | 0.0489555 | 0.08569 | 20.119% | 0.0619743 |
| M085 | original50k | N2 | 3 | 1.49687243e-06 | 0.006213355 | 0.01079 | 4.084% | 0.0100105 |
| M085 | later20k_single_CO2 | CO2 | 7 | 7.68363268e-05 | 0.04741823 | 0.13129 | 30.846% | 0.0504459 |
| M085 | new50k | CO2 | 6 | 8.08070894e-05 | 0.037072 | 0.09406 | 21.542% | 0.0387081 |
| M085 | new50k | N2 | 6 | 1.56087323e-06 | 0.01473337 | 0.03672 | 12.230% | 0.0228506 |
| M085 | combined9_50k | CO2 | 9 | 8.1478862e-05 | 0.02809794 | 0.08648 | 20.119% | 0.0330557 |
| M085 | combined9_50k | N2 | 9 | 1.53924122e-06 | 0.01193127 | 0.03656 | 6.394% | 0.0155949 |

Native +/- is the reported five-block confidence halfwidth, not independent-seed SE. The block convention is inherited from the completed source audit; five blocks are never counted as five independent simulations. The table separately gives SD(lnKH)/sqrt(n), the KH CV, median native relative halfwidth, and delta-method propagation of within-run five-block SEs into the pooled log mean. Historical primary gates SE(lnKH)<=0.05 and CV<=0.10, plus the native10% warning, are unchanged. A primary pass with a native warning is not an unconditional rare-event convergence certificate. Per-condition t intervals are in NATIVE_SEED_SUMMARY.csv and rely on small-sample distribution assumptions.

| Fresh seed | CO2 KH | Native +/- | Relative +/- | Largest/smallest Henry block |
|---|---|---|---|---|
| 2026111401 | 7.298593e-05 | 1.127768e-05 | 15.452% | 1.38185 |
| 2026111402 | 7.980465e-05 | 2.147746e-05 | 26.913% | 1.88555 |
| 2026111403 | 7.793539e-05 | 8.201385e-06 | 10.523% | 1.26512 |
| 2026111404 | 9.480185e-05 | 4.390592e-05 | 46.313% | 2.11620 |
| 2026111405 | 8.404017e-05 | 1.996943e-05 | 23.762% | 1.55017 |
| 2026111406 | 7.698232e-05 | 1.487435e-05 | 19.322% | 1.45178 |

| Gas | New minus old mean lnKH | SE difference | Welch df | Descriptive p | 95% Welch interval |
|---|---|---|---|---|---|
| CO2 | -0.024836768 | 0.06140826 | 4.37586 | 0.704878 | [-0.1897103, 0.14003677] |
| N2 | 0.041867545 | 0.01598993 | 6.42831 | 0.0372342 | [0.0033649158, 0.080370174] |

Welch comparisons use fresh6 versus original3 independent mean-log results. Their p-values are descriptive, unadjusted and not equivalence tests; small samples with concentrated insertion weights limit calibration. Similarity or non-rejection does not bound unseen tails. The same-seed replay exactly repeated historical means/blocks but contributes zero new independent runs here. Ordinary M002 and matched M029 remain context from archived outputs only.

CO2 has no detected old/new mean-log shift at this resolution; that is not equivalence. N2 shifts upward by0.041867545 log units, with the displayed unadjusted seed-only Welch p=0.037234. It is not robust evidence of a new physical effect: there are two gas comparisons, only3 old runs, and block-derived old/new uncertainty is larger (approximate SE0.0249471 rather than seed-only0.0159899). Fresh N2 native halfwidths range5.50%–25.04%, with median12.23%. All six fresh CO2 seeds exceed the10% native warning; N2 seeds2026111403,2026111404 and2026111405 also exceed it. These are warnings, distinct from the passing primary SE/CV gates. Thus the historical N2 response contrast0.010545 is not independently reproduced to those digits: fresh and pooled contrasts are0.052413 and0.038457. CO2 still dominates, with corresponding contrasts1.845702 and1.853981. Do not label both gas coefficients independently confirmed merely because CO2 is compatible.

The later p19 QMC arrays contain eight scrambles of524,288 weights, with mean dimensionless weight 198.849044244, between-scramble SE 4.681277826 and reported relative95% halfwidth 5.5668%. Directly reading all eight arrays gives concentration ESS 309.128–373.389; the top0.1% carry 74.243%–78.091% of mass. These are concentration statistics, not IID QMC sample counts. p18/p19 are nested levels of the same scrambles, not16 independent replicates. The p19 relative95% halfwidth5.5668% remains above its original5% full-electrostatics closure target. Earlier full-mode spatial-method gates failed and remain negative evidence; the later coarse-map pass does not retroactively validate them. Original and fresh production per-insertion streams are not exported, so no production insertion ESS, maximum-weight share or rigorous tail-bias bound can be recovered from five block means. Zero-molecule energy arrays are not insertion-energy trajectories.

## Exact structures and charges

| Alias / exact identity | P1 atom-site composition | Sites | Net charge / e | Site charge range / e |
|---|---|---|---|---|
| M002 / DB0-m12_o12_bcu | C40 H32 N16 Ni4 | 92 | -3e-06 | -0.279010 to 0.293550 |
| M029 / DB0-m15_o100_o150_f0_fsc | Co2 O8 C34 N2 H22 | 68 | 4e-06 | -0.654140 to 0.826220 |
| M043 / DB0-m15_o106_o150_f0_fsc | Co2 O8 C38 N2 H20 | 70 | -2e-06 | -0.665866 to 0.777930 |
| M085 / DB0-m15_o11_o30_jea | Co4 O16 C24 H10 | 54 | -2e-06 | -0.634494 to 1.082026 |
| M089 / DB0-m15_o11_o75_f0_fsc | Co2 O8 C16 N2 H6 | 34 | -1e-06 | -0.583026 to 0.934328 |
| M192 / DB0-m15_o14_o77_f0_fsc | Co2 O8 C30 H14 N2 | 56 | 1e-06 | -0.678534 to 0.903736 |

All inspected CIFs identify REPEAT_Assigner and P1. Site labels, elements and every partial charge match the actual full-mode force-field pseudoatoms; LJ-only framework and guest charges are zero. Net-charge residuals at10^-6e scale are reported, not silently neutralized. Every exact CIF SHA256 and model path is in STRUCTURE_FACTS.json. M085 is54 sites (4Co,16O,24C,10H), not an assignment inferred from its suffix. Its3x2x4 cell has1,296 sites. M029 has68 sites and2Co; matching geometry does not imply identical composition or local charge environments. A proposed explanation based solely on different metal elements is contradicted for this pair: both are Co-containing.

No inspected CIF contains a chemical-name or explicit bond loop, occupancy or disorder tags. Absence of those tags does not prove chemical completeness or absence of disorder. SBU/linker names, formal metal oxidation states, open-metal-site identity and topology remain NOT_ESTABLISHED. `jea`, `fsc`, `bcu`, `o11` and similar tokens are recorded identifier labels, not independently authenticated structural/chemical assignments. The full210/28 identifier groups are not reclassified from these six structures.

## Corrected M085–M029 contrasts and uncertainty

| Quantity | M029 | M085 | M085 minus M029 |
|---|---|---|---|
| Historical lnS_WCA | -0.2013218609595037 | -0.1981839297833456 | 0.0031379311761580986 |
| Corrected lnS_WCA | -0.2338605945939956 | -0.2396041112491526 | -0.005743516655156988 |
| Corrected attractive increment A | 2.8719431326695095 | 2.252439064724554 | -0.6195040679449555 |
| E from archived LJ/full endpoints | 0.1406952326393931 | 2.0006886354361075 | 1.8599934027967144 |

| M085 minus M029 | Independent-component seed SE | Covariance-agnostic seed SE bound | Max(seed,block) propagated SE | Max(seed,block) covariance bound |
|---|---|---|---|---|
| attraction | 0.00334149955 | 0.00751254314 | 0.0042604928 | 0.00902131969 |
| electrostatic | 0.0494885846 | 0.0634472567 | 0.0630177612 | 0.0845275404 |

All differences use M085 minus M029. A=lnS_LJ-lnS_WCA; E=lnS_full-lnS_LJ. Corrected WCA SE includes its frozen paired-gas covariance; original gas/state log coefficients are averaged across the actual seed units. The first SE column assumes component independence. The sum-of-marginal-SE bound allows arbitrary unknown covariance, conditional on those estimated marginal SEs. The final columns conservatively use max(between-seed SE,pooled native-five-block delta SE) per RASPA component, without double counting the same variability. These propagated SEs and bounds are descriptive estimates, not universal95% coverage or a rare-tail-bias bound. Same seed labels across states/frameworks do not establish paired insertion configurations or cross-state covariance. FULL_GAS_JOB_COVARIANCE.csv separately records empirical two-gas covariance across the actual full-mode jobs, without assuming common gas poses.

Corrected WCA difference is -0.00574351665516, versus independent-framework-stream SE 0.00098940179; close point values are distinguishable at their current Monte Carlo precision. The corrected attraction contrast is -0.619504067945; the historical electrostatic contrast is 1.8599934028, or 6.42369439 in the ratio of electrostatic enhancement factors. Original A contrast was -0.628385516. The new full-mode runs affect E/full diagnostics, not A.

| M085 full cohort | E_M085 | E_M085 minus E_M029 | Enhancement-factor contrast | CO2 response contrast | N2 response contrast | SE contrast max(seed,block) | Unknown-covariance SE bound |
|---|---|---|---|---|---|---|---|
| original50k | 2.00068864 | 1.8599934 | 6.42369439 | 1.87053861 | 0.0105452091 | 0.063017761 | 0.08452754 |
| new50k | 1.93398432 | 1.79328909 | 6.00918475 | 1.84570184 | 0.0524127538 | 0.045284373 | 0.074101351 |
| combined9_50k | 1.95621909 | 1.81552386 | 6.14429409 | 1.85398077 | 0.0384569056 | 0.036960597 | 0.061193223 |

The fresh6 and combined9 columns are diagnostic recomputations using unchanged archived LJ and M029 values. They are not silently substituted into the frozen population table. The archived CO2 response contrast1.870538611928 correctly rounds1.871; the archived N2 response contrast is0.010545209132. The new-run columns quantify how this gas attribution and enhancement contrast move under independent full-mode sampling. The larger electrostatic response is relative to each framework's LJ reference: historical full-mode CO2 geometric KH is8.28392076e-5 for M085 versus1.00821002e-4 for M029, while LJ-only values are1.08557386e-5 and8.57707183e-5. Thus the electrostatic enhancement contrast is not a claim that M085 has the larger absolute CO2 Henry coefficient or better process performance.

For the already highlighted M085/M223 endpoint example only, unchanged M223 lnS_full=4.02950885317 (saved SE0.0032333745). Absolute endpoint differences are0.015985264 historically,0.082689577 with fresh6, and0.060454806 with the diagnostic nine-seed mean. Both updated point differences exceed the reported0.0538 historical endpoint-selection cutoff. This does not prove physical nonequivalence under the remaining uncertainties, but it removes support for retaining the original unqualified endpoint-matched/extremal headline. De-emphasize this example and retain only its historical-selection provenance; no replacement pair was selected. See M085_ENDPOINT_EXAMPLE_DIAGNOSTIC.json. M029/M085's distinct geometry-matched role and large CO2-driven response remain qualified model findings.

## Pore accessibility

**NOT_ESTABLISHED:** a periodic connected pore network with a continuous CO2/N2 orientation-feasible path, probe-specific blocking mask, or a definitive original blocked-pocket policy. Inspected templates specify no explicit mask and the successful runs use those original unmasked definitions. Missing keys do not independently authenticate historical defaults. Uniform insertion can sample disconnected thermodynamically favorable cavities; positive Henry/WCA factors, constructed-move fractions, nonzero ASA and pore-diameter descriptors do not demonstrate transport connectivity. The archived (Df,Di) pore scalars are (5.75643,7.28113)A for M029 and (6.17587,7.43577)A for M085. Even a spherical-probe/free-sphere path, if its computational provenance is accepted, would not by itself establish the continuous molecular orientation-feasible route required here.

The retained M085 field is an orientation-integrated3696-voxel0.75A map with32,768 orientations/point. Its actual arrays store coordinates, weights, relative density and angular-SE summaries; they do not store an orientation-feasible path graph. Its mean weight194.575171946 and the1A-map mean185.677375998 differ4.7921%; the fine mean is2.1493% below the later QMC reference. The orientation sanity check concerns only three selected points. These bounded coarse-map checks support a thermodynamic field summary, not general pointwise convergence or molecular accessibility. The selected local M029 full-field folder contains only its input manifest; no unavailable M029 field array was assumed or reconstructed. The retained M085 N2/full array was also read: its3696 log weights imply mean weight3.96318030546, matching metadata, with16,384 orientations/point. It too is an integrated field, not an orientation-feasibility mask. The separate N2_LJ_GATE_FINAL.json passes its131,072/196,608-orientation plateau checks against262,144 orientations, explicitly only for the M085 N2/LJ angular-method gate; it validates neither full mode nor pore connectivity.

The existing support report defines the minimal voxel set carrying99.5% insertion mass, with pairwise support unions. M085 has871/3696 reported support voxels and M029622/3060; those counts describe probability support, not connected geometric void volume or a gas-probe feasible region. No connectivity, accessibility-mask, structural reconstruction or new spatial calculation was performed.

## Consequences for existing claims

| Existing statement / location | Scientific disposition |
|---|---|
| M029/M085 are mutual nearest neighbors in the specified nine-descriptor space (main:85,180,194) | SURVIVES as the archived selection fact (distance0.257529255249); it establishes neither identical pores nor chemical identity. The selected pair is not the all-pair optimum; M043 is a different verified structure. |
| Nearly identical WCA numbers -0.201/-0.198 (main:180) | NUMBERS CHANGE to -0.233860595/-0.239604111. They remain numerically close, but their difference is resolved relative to corrected WCA Monte Carlo SE; do not claim statistical equality. |
| E contrast1.860 / 6.42-fold (main:180; conclusion:237) | QUALITATIVE CONTRAST SURVIVES: fresh-six contrast1.793289 (factor6.009185), diagnostic nine-seed contrast1.815524 (factor6.144294). Exact1.860/6.42 needs qualification as historical, with sampling uncertainty. This ratio compares electrostatic enhancement factors, not final selectivities. |
| CO2 drives the electrostatic contrast (main:182,186) | CO2 DOMINANCE SURVIVES, with updated sampling estimates: fresh-six CO2 contrast1.845702 versus N2 0.052413; nine-seed1.853981 versus0.038457. Historical1.870538611928 rounds1.871. The exact tiny N2 contrast0.011 needs qualification; native warnings remain. |
| M085/M223 final endpoints differ by0.016 while increments compensate (main:155) | DE-EMPHASIZE this headline. Fresh-six/nine-seed endpoint differences from unchanged M223 are0.082690/0.060455, exceeding the reported0.0538 point cutoff. Historical matching remains a selection fact; current endpoint equivalence and extremal rank are not established. This is not proof of physical nonequivalence. No replacement pair was selected. |
| M085 highlighted in matched pair, endpoint example and rank mover (main:155,180; SI ranking) | QUALIFY as reuse of one material and its shared endpoint evidence, not three replications or independent confirmations. Exact rank/prominence is conditional on uncertainty; no new population ranking is asserted here. |
| Candidate motif explanations discussed but explicitly withheld (main:188; reviewerM38) | KEEP THE LIMITATION. Composition and charge-bearing model sites are verified; specific binding-site/SBU/linker/topological attribution is NOT_ESTABLISHED. Do not convert the discussed possibilities into demonstrated explanations. Global coefficients and coarse orientation-integrated maps are insufficient. |
| Spatial insertion probability establishes connected accessible pores or transport | MUST NOT BE CLAIMED. No verified periodic connectivity plus continuous orientation-feasible molecular path or definitive original pocket mask is available. Unmasked insertions can occupy disconnected cavities. |
| Original fields were absent (main:188) | Update the evidence limitation in a later authorized text revision: a scoped M085 field and later weight arrays are now locally recovered; the selected M029 full-field directory contains an input manifest only. This does not establish atom-specific motifs or accessibility. |

Reviewer traceability: U03 (shared M085 evidence),U04 (gas-specific convergence),U05/U12 (pockets/access),U06/M49 (verified identity/labels),U13 (A/E uncertainties) are addressed with the limitations above. U09/M58 remain partial for SBUs/topology and general identifier-group chemistry. M38/S01 are bounded by recovered evidence and the absence of atom-specific attribution. U14's historical WCA precision concern is referenced to the completed corrected-WCA238/238 gate, not resolved by these RASPA runs. U07's second non-M085 endpoint selection and M38's new chemistry correlations are outside this focused task and were not initiated.

## Evidence and stop

| Evidence | Exact local source |
|---|---|
| Structures and charge matching | evidence/structures/{mof_id}_repeat.cif; full/lj_only model paths and SHA256 in work/phase2_m085_20261114/STRUCTURE_FACTS.json |
| Original native production | evidence/raspa/base/work/{M002,M029,M085}__{full,lj_only}__s5810{1,2,3}/output/output_298_1e+05.s0.txt |
| Existing shorter independent runs | evidence/spatial/results/native/co2_m085_full_widom_20000_9840{1..7}/simulation.json and output/output_298_1e+05.s0.txt |
| Later QMC weights | evidence/spatial/results/full_electrostatics_validation_m085_co2_final/nested_qmc_p18_rep{0..7}.npz; nested_qmc_p19_rep{0..7}.npz; nested_qmc_convergence.json |
| Retained M085 maps | evidence/spatial/fields/M085_CO2_full_0.75A_32768orient/{field.npz,metadata.json}; M085_N2_full_0.75A_adaptive/{field.npz,metadata.json}; evidence/spatial/results/n2_lj_validation_m085/N2_LJ_GATE_FINAL.json; full_spatial_closure_m085_co2/{ORIENTATION_SANITY_REPORT.json,OVERNIGHT_CLOSURE_REPORT.json} |
| Failed full-spatial gates and support definition | evidence/spatial/results/full_electrostatics_validation_m085_co2/FULL_ELECTROSTATICS_GATE_REPORT.json; full_electrostatics_validation_m085_co2_qmc/FULL_ELECTROSTATICS_ROBUST_GATE_REPORT.json; final_spatial_figures_supported/{SUPPORTED_FIGURE_REPORT.json,support_statistics.csv} |
| Corrected WCA | repo/review/01C_CORRECTED_WCA_238.csv;01C_PRECISION_AND_CONVERGENCE.csv |
| New independent jobs | work/phase2_m085_20261114/production/M085__full__s202611140{1..6}/{simulation.json,execution.json,replay_result.json,output/output_298_1e+05.s0.txt} |
| Direct scientific results | work/phase2_m085_20261114/{CORRECTED_ORIGINAL_ENDPOINT_CONTRASTS.json,NATIVE_SEED_SUMMARY.csv,NEW_NATIVE_ROWS.json,ORIGINAL_VS_NEW_COEFFICIENTS.csv,M085_ELECTROSTATIC_UPDATE.csv,FULL_GAS_JOB_COVARIANCE.csv,PHASE2_NUMERICAL_RESULTS.json} |

Analysis scripts and intermediate numerical files remain under work/phase2_m085_20261114. No source dataset, original simulation input/output, model, figure, manuscript or GitHub state was changed. **Stop: PARTIAL**, with exact remaining scientific limitations: native rare-event/tail convergence bounds for full-CO2; connected orientation-feasible accessibility and pocket policy; and unverified SBU/linker/topology/atomic-motif assignments. The six-job budget is exhausted; no automatic calculation expansion occurs.
