# Phase1B WCA implementation verdict: CORRECTION_REQUIRED

Authority: M21,S02,S04,U11,U14; cross-engine references M17-M18. Fixed pilot M002/M085/M211, both gases, three original base seed identifiers, two protocols. No Phase2 or population job was launched. Original238 table, manuscripts, figures, ML and prior reports are unchanged.

## Authenticated estimator

The versioned FixWidom::pre_exchange resets its factor at each invocation; attempt_molecule_insertion averages ninsertions=500, and compute_vector returns that batch's mu/factor/volume. Original decks use run2000 and print final f_W[1]. Thus nominal1,000,000 attempts yield an exported estimate from the last500; the earlier999,500 are not accumulated into it.

Because a version string alone does not authenticate compiled semantics, one minimal recovered-engine execution was used. Its first batch B=0.34013854450368508, second/exported B=0.32467854827012682, and two-batch mean=0.33240854638690598. This directly confirms final-batch behavior in the actual DLL. An independent Park-Miller RNG/source-draw-order/energy implementation reproduces both native batches with maximum discrepancy 2.78e-16. Native beta implies R=0.0019872067 kcal mol^-1 K^-1 at298K.

For uncertainty the historical unit is a saved500-attempt endpoint per separately declared seed, typically3/6/9/12 such endpoints per gas. Do not count1e6 retained observations or2000 independent simulation replicas. Importantly, the archived SE formula already uses variability among saved endpoints divided by sqrt(number of seeds); it does not divide their SD by sqrt(1e6). The defect does not justify multiplying every reported SE by sqrt(2000). Original precision is noisy and sampling-budget wording is wrong; recomputation can recover the work that was attempted but not averaged. Historical extension effective-seed authentication remains a separate limitation.

f_W[2] is dimensionless B, not mean energy despite legacy mean_dU_kcal_mol. The analysis uses R=0.00198720425864083 to invert saved mu. The pilot reports raw native B and separate original-analysis-convention factors. No constants or historical values are silently replaced; no absolute RASPA Henry normalization is invented.

## Orientation: mathematical and deterministic evidence

For initial molecular axis e_z, the legacy rotation gives z'=cos(theta)+(1-cos(theta))*n_z^2, with uniform axis n and uniform angle theta. E[n_z^2]=1/3,E[n_z^4]=1/5,E[cos(theta)]=0,E[cos(theta)^2]=1/2, so E[z'^2]=1/2-1/3+3/10=7/15. The required isotropic value is1/3; E[P2(z')]=1/5 rather than0. Both gases are head-tail symmetric, but this is an even-moment defect and survives that symmetry. Uniform rotation angle is not Haar rotation sampling.

A deterministic orientation-only262144-draw diagnostic gives legacy mean z^2=0.465281843, versus uniform-quaternion 0.3339559. KS(|z|,Uniform[0,1]) yields legacy D=0.166912,p below floating-point reporting, and quaternion D=0.00132533,p=0.746023. The quaternion construction is the correctly normalized Shoemake map from three independent uniforms. Tests are independent of framework energies. Source/draw-order fingerprinting ties the inspected legacy transform to the recovered native sampler; all18 new legacy endpoints also reproduce original archived endpoints.

## Historical recovery

Only the2052 already indexed native screen files were inspected by exact path and checked against recorded hashes. Each retains20 positive-step batch factors at100-step intervals:10000 sampled attempts of the nominal1e6. Step0 is not a sampled batch. No complete2000-batch history exists, so exact full-run recovery is impossible from these logs. Neither unprinted batches nor per-insertion angles/weights can be inferred from sparse means. Their partial averages cannot repair orientation bias.

## Correction implementation validation and bounded execution

The correction pilot uses an independent NumPy/SciPy/Numba insertion integrator, not a patched or substituted LAMMPS force field. It reads the exact original generated atom data, guest-site coordinates, pair epsilon/sigma/cutoffs and computes the same shifted lj/cut pair energies. Twenty-seven explicit periodic images and an exact radius search accelerate the sum; no energy interpolation/grid or approximate cutoff is introduced. Fractional excursion bounds including guest extent and cutoff are below1 for all six models, proving image coverage for home-cell centers.

Before production,336 native LAMMPS framework/guest group-group fixed-pose energy comparisons across all six models, including whole-cell translations, passed the registered tolerances max(1e-9 kcal/mol,1e-11*abs(E)) and1e-10 in B; maximum B discrepancy 2.45e-13. Partial finite-weight poses were included for every model. The kernel file hash was frozen and checked by every correction job. These validations plus the native1000-draw fingerprint establish exact-model consistency within the stated precision.

One parser assertion initially counted the fix ave/time step0 record as sampled. The actual native validation execution succeeded. analyze_validation.py excluded that initial record and analyzed the same preserved outputs; no diagnostic execution or force-field tuning was repeated.

Exactly36 production jobs completed:18 native original-rotation jobs with every500-insertion batch retained, and18 isotropic-quaternion jobs. Each uses1e6 attempts, the same original structures/guest model/potential/cell/temperature, and original base seed labels58101-58103. Original native accumulation-only and endpoint values come from the identical executed stream. Isotropic runs use documented PCG64 seeds and uniform quaternions; same labels across protocols do not imply shared configurations. Across gases within one protocol the generating code does share positions/orientations, explicitly supporting paired gas diagnostics in this pilot.

Scripts, inputs, job specs, commands, native logs,2000-batch histories, corrected per-insertion weights and hashes are retained under work/phase1b_wca_integrity_20261114. Scientific code is cache=False. Tested analytical versions are recorded in every corrected result.json; no package was installed or global environment edited.

## Pilot numerical consequences

All B values below are dimensionless arithmetic averages over three base-seed estimates. Historical refers to the original last500 endpoints, verified by new native replay. Accumulation and orientation are separated explicitly.

| Framework | Gas | Historical last500 mean B | Legacy cumulative mean B | Isotropic cumulative mean B | Isotropic between-seed SE(B) | Orientation change |
|---|---|---|---|---|---|---|
| M002 | CO2 | 0.331020195 | 0.329969416 | 0.331337817 | 0.0002001 | +0.415% |
| M002 | N2 | 0.367969329 | 0.369911958 | 0.370019284 | 0.000214 | +0.029% |
| M085 | CO2 | 0.0937288905 | 0.0900250292 | 0.0901753813 | 5.686e-05 | +0.167% |
| M085 | N2 | 0.110453503 | 0.113973284 | 0.114765416 | 9.045e-05 | +0.695% |
| M211 | CO2 | 0.00913234687 | 0.00915791555 | 0.0117315839 | 5.69e-05 | +28.103% |
| M211 | N2 | 0.0172976039 | 0.0188144939 | 0.0207838818 | 5.07e-05 | +10.467% |

L=ln(mean B_CO2/mean B_N2); A=the unchanged frozen lnS_LJ minus L. The orientation delta compares the two cumulative1e6 protocols; historical-base comparison is separately available. M085's final frozen WCA used6 seeds andM211 used12, so a difference versus the frozen publication table is not solely a correction effect. The CSV includes those cohort distinctions and both native/legacy-analysis constants.

| Framework | Historical base3 lnS | Legacy cumulative lnS | Isotropic cumulative lnS | Orientation delta A | Holm p, lnS test |
|---|---|---|---|---|---|
| M002 | -0.10582020 | -0.11426506 | -0.11041667 | -0.00384838 | 0.074746 |
| M085 | -0.16418817 | -0.23587634 | -0.24113373 | +0.00525739 | 0.010749 |
| M211 | -0.63874528 | -0.72000893 | -0.57189309 | -0.14811584 | 8.5269e-05 |

The registered orientation tests compare mean seed-level log B or log gas ratio with independent Welch tests (3 runs per protocol), followed by Holm adjustment across six gas-factor and three selectivity tests. Ratios of pooled means and means of per-seed logs are labelled separately; their differences are retained at full precision. Familywise significant conditions: [('M085', 'CO2/N2'), ('M211', 'CO2'), ('M211', 'N2'), ('M211', 'CO2/N2')]. M211's orientation-only pooled lnS shift is +0.14811584 (about16% in S), with a corresponding -0.14811584 attractive-increment shift. M085's small ratio shift also survives the registered correction. M002 is not resolved at familywise0.05 in this pilot; that is not proof of equivalence or absence of bias.

Accumulation-only paired gas tests all have95% intervals including zero: historical endpoints versus full means are consistent with their large endpoint Monte Carlo noise here. This is a loss-of-precision/export-scope defect, not evidence that accumulating more draws itself changes the expectation. Orientation changes the sampling measure and produces systematic pilot shifts; uncertainty relabelling alone is insufficient.

All2000 batch means are retained per new job, with250k/500k/1m prefixes, halves/quarters,500-batch and fixed10k-block SEs. Corrected per-insertion weights give weight-concentration ESS ranging 18196.8 to 392333.6; these are concentration diagnostics, not independent simulation counts or proof of population convergence. Native within-batch squares are unavailable, so native raw-weight ESS is explicitly not reconstructed. Between-seed SE, within-run MC precision and the paired gas-covariance diagnostic are separate columns. Three seeds can give an accidentally small between-seed SE; the report retains the within-run diagnostics and does not promote that small estimate to a universal precision guarantee. Primary statistical decisions remain the frozen seed-level tests, not posthoc block tests.

## Minimum defensible scientific correction

This is CORRECTION_REQUIRED, not merely corrected uncertainty reporting. Original WCA values cannot be certified as the intended isotropic insertion integral. For a corrected238-framework release, recalculate WCA for every retained framework and both gases using the validated cumulative/isotropic method, with execution-bound hashes, separately seeded runs and a frozen precision/extension rule. A minimum initial base design would be238x2x3=1428 jobs, followed only by separately authorized, preregistered precision extensions; retaining the original seed-tier design would instead require2034 retained jobs. No such population work is authorized or launched here. There is no need to rerun existing LJ/full solely because WCA changed.

After population WCA completion, regenerate the dependent WCA/attractive columns, SEs, sign counts, medians, ranks, matched attraction contrasts, WCA-to-LJ correlations, WCA-dependent mechanism/shortlist/geometry-model claims and figure-source tables under a new version. Existing WCA-target/attractive-target ML claims need renewed analysis under separate authorization; no model is refitted now. Three pilot structures do not validate the238-framework sign pattern, median12.65-fold attractive enhancement or ranking conclusions.

Original RASPA absolute Henry results, LJ/full-only selectivities and electrostatic differences do not numerically change due to this WCA correction. The full-minus-LJ CO2 contrast/rounding and LJ/full top24 overlap remain their separate existing results. Their pre-existing scientific limitations are not resolved by this pilot. Frozen baselines remain immutable historical evidence, with completed numerical reproduction distinct from validity of the intended WCA measure.

## Source identities

| Primary source / frozen record | SHA256 |
|---|---|
| runtime\reference_source\fix_widom_stable_22Jul2025_update4.cpp | acb688b517cdbbc3edcfe68391602c491870916432a1573b7147cdb90342ac5e |
| runtime\lammps\bin\lmp.exe | dc80f4c73fdfa488cc72444448b4f777a6fe3dba1cafd0f8e265a4f077f786a3 |
| runtime\lammps\bin\liblammps.dll | 60bc6c51988d6c50d114e72cba208947d72cc5fd8cc6b732c8cb3885cf840349 |
| repo\review\01_WCA_JOB_LEDGER.csv | 7e98ddcb7eac7c3828bea33ccde3e2a33cba784ed00e7c12fa7c111184ecc12a |
| repo\data\authoritative\mechanism_238_authoritative.csv | f317eef220e6f8757be6aa8d6e4ec29b9bf90e0eeaad8d86009a265b65b1b149 |
| repo\data\provenance\wca_base_jobs.csv | f07f950d375aebf62d2c1ef5f155f4a01acb2525218a7d27ed47cd51141bb3cd |
| work\phase1b_wca_integrity_20261114\FROZEN_PLAN.json | 60d37faef906040ad409bca56b5fa01261717c18a07aaa68e5a04e0bfed8978e |
| work\phase1b_wca_integrity_20261114\PILOT_JOB_MANIFEST.json | c8b59875e41780c8f43e4cbcdd61dc0d9a3848191713e3ceeba0ef8720a084c8 |

The four requested review files and the dedicated artifact manifest give exact traceability. No Phase2, population run, manuscript/figure edit, GitHub write or ML refit occurred. Stop at the Phase1B gate.
