# JCTC revision protocol — Miguel and Uzair (locked scope)

**Authority:** Miguel main-PDF annotations \`M01–M59\`, Miguel SI annotations \`S01–S07\`, Uzair email \`U01–U52\`. The three files in \`Miguel_Uzair_Comments (1).zip\` are reference registers, **not** new experimental evidence. Three annotation objects (\`M13\`, \`M40\`, \`M53\`) lack readable annotation text and must be inspected in page context. **118 tracked objects are not 118 independent scientific problems.**

**Revision starting point:** numerical/code repository \`alimardani76/bundle_molsim\` \`main\` at \`50da988a323d0265cb3c15b910f2fbe5dac4021a\`; latest supplied editorial manuscript \`P01_selectivity_origin_map(1).zip\` (V14). These are **not** perfectly text-identical; integrate V14 editorial changes after file-tree verification, not by indiscriminately overwriting either source.

**Working branch:** \`review-miguel-uzair\`. **No edits to scientific data/manuscript until Phase 0 passes.**

## Rules that cannot be relaxed

1. **Review-driven only.** Every computation, figure, paragraph and new file must cite at least one \`Mxx\`, \`Sxx\` or \`Uxx\` comment and resolve a stated concern. No unrelated feature engineering, new datasets, universal screening study or exploratory project.
2. **One phase at a time.** Do not start phase N+1 until phase N has a signed PASS or a documented BLOCKED/FAIL with a reviewer-facing consequence. Do not use later results retroactively to rewrite the registered protocol.
3. **Frozen numerical baseline.** The published 238-MOF results, source data and prior simulation figures are immutable evidence. Derive revisions in new directories with checksums and complete provenance. Correct a numerical value only when direct source-level evidence proves it wrong, and document every downstream figure/manuscript change.
4. **No invented reproduction.** Aggregated Henry data do not imply the original Widom simulations can be rerun. A shared seed ID does not prove paired covariance. A structure drawing does not prove an adsorption motif. A group-name suffix does not establish metal/SBU/topology.
5. **Fixed subset and computational ceiling.** No new simulations for all 238 MOFs. Freeze one core panel of **up to 20** framework IDs using explicit rules **before** simulations, anchored to the available 15-MOF force-field bridge and including M085, M029, M043, M089/M192, both database-identifier groups, typical and extreme responses and an independent endpoint match where feasible. Freeze a nested **up-to-eight-framework** sensitivity subset before changing charges/guest models. Do not add frameworks after seeing outcomes.
6. **Completion requires evidence.** Each review item ends in exactly one status: \`VERIFIED_EXISTING\`, \`CORRECTED\`, \`NEW_RESULT\`, \`LIMITATION_DISCLOSED\`, \`NOT_APPLICABLE_TO_CURRENT_VERSION\`, or \`BLOCKED\`. A limitation is not interchangeable with a requested result. Do not claim every substantive comment is scientifically resolved if a required test is blocked.
7. **Freeze before writing.** Manuscript and figures follow the finalized scientific tables, not the reverse. All new calculations get a source manifest, executable command, seeds, results CSV, validation and fixed interpretive boundaries.
8. **Miguel-first priority, complete Uzair coverage.** Simulation definitions and physical mechanisms are front-loaded; editorial and submission corrections still remain mandatory. The tutorial request \`U51\` is a separate educational request, **not a paper deliverable**.

## Phase 0 — Inventory, freeze and atomic review register

**Input:** user-supplied full working file tree; current GitHub checkout; V14 source; Miguel annotated main/SI PDFs; Uzair email; three indexed action documents.

**Actions**
- Identify actual CIFs, ARC-MOF source snapshot, WCA/LJ/full simulation inputs, raw gas-by-state seed output, original job registry, chemistry/charge definitions, model predictions/folds, source CSVs and figure sources. Compute hashes and record storage locations; mark missing precisely.
- Make a version table: V14 manuscript/SI and figures versus GitHub, including Shayan's approved Figure 1(d)/4(c) art; choose the precise editable TeX baseline without discarding either version's verified changes.
- Create \`review/COMMENT_MATRIX.csv\`: each \`M01–M59\`, \`S01–S07\`, \`U01–U52\`, page/section, exact criticism, stage, evidence file, owner, status and final response. Inspect blank annotation objects in page context. Cluster duplicate comments but preserve every original ID.
- Recheck original cohort/identity/rank checksum gates (238 records, 210/28 group sizes, three-state telescoping identity, WCA job ledger, major medians and 7/24 shortlist replacements). No simulation/model rerun.

**Deliverable:** \`review/00_INVENTORY_AND_BASELINE.md\`, \`review/COMMENT_MATRIX.csv\`, frozen input manifest, missing-input ledger.

**PASS gate:** Every existing file located or explicitly marked missing; exactly 118 comment objects registered; frozen manuscript/source commit and framework IDs recorded. **This is the only phase to start after receiving the file tree.**

## Phase 1 — Prove what was simulated (Miguel M17–M23, S01–S05; Uzair U08–U17, U45)

**Actions**
- Trace selection of 240 original structures to 238 retained; name input ARC-MOF release/snapshot and excluded records, no reconstructed history without evidence.
- Establish WCA executable and code version (not automatically RASPA or LAMMPS), WCA potential and all-charges-off status, full/LJ RASPA3 version and JSON, partial-charge source, guest models, UFF/mixing/cutoff/shift, simulation cells/supercells, Ewald tolerance and blocked-pocket policy.
- Reconcile **2,052 gas-specific WCA jobs = 2,034 retained + 18 excluded** against *actual job ledger*, and examine four high-SE WCA structures and the 3/6/9/12-seed extensions.
- Report absolute CO₂ and N₂ Henry coefficients for typical cases with correct units and converted reference convention, independently of any literature benchmark.

**Deliverable:** \`review/01_SIMULATION_PROTOCOL.md\`, versioned sample input templates or original inputs with immutable hashes, \`wca_job_ledger.csv\`, method-ready facts.

**PASS gate:** Every configuration claim traceable to actual scripts/logs. If original inputs absent, state specific blockage and **do not** invent or silently run a different Hamiltonian.

## Phase 2 — M085 validity and structure/accessibility evidence (Miguel M38/M49/M58, S01; Uzair U03–U07/U09/U12–U14)

**Actions**
- Decode and verify CIFs/atom types/partial charges for M085, M029, M043, M089, M192, a separate endpoint pair and balanced control structures. Characterize metal, SBU, linker, topology, pore dimensions and the 210/28 source groups. Distinguish structure identity from identifier guesses.
- Analyze M085 gas × state seed/block normalized insertion weights, convergence (especially **CO₂ full**), running means, independent-replicate uncertainty, weight concentration and rare-event diagnostics. Explain why M085 appears in three examples without calling them independent confirmations.
- Audit connected access regions, periodic pockets, CO₂/N₂ orientation feasibility, missing atoms/disorder and the original pocket treatment. Differentiate thermodynamic insertion access from kinetic accessibility. Perform **targeted M085/control reruns only if these checks require new evidence**, with a predeclared max of **12 independent seeds per condition**. Mark unresolved if this ceiling is insufficient.
- Compute per-gas \`SE[ln K_H]\`, uncertainty of A/E and M085−M029 contrasts using actual independent units and covariance when available. If access treatment changes results, correct all affected downstream claims instead of keeping the old number.

**Deliverable:** \`review/02_M085_AND_STRUCTURES.md\`, structural ID crosswalk, visualization sources, pocket test, convergence/SE tables.

**PASS gate:** M085's claimed role is numerically reliable under the stated model or its abstract/figure prominence is reduced; inaccessible-region claim is explicitly supported or disclosed as unverified. No atom-specific binding-site assertions from CIFs alone.

## Phase 3 — Explain observed physics and test ML robustness using existing data (Miguel M05/M28/M30/M34/M38/M45–M49/M58; Uzair U02/U07/U21–U26)

**Actions**
- Explain WCA↔LJ rank anticorrelation (\`ρ≈−0.751\`) with prespecified pore-size/shape/accessible-volume descriptors; show pooled and within-group associations, uncertainty and nonmonotonicity where present. No causal claim from correlation alone.
- Define the nine geometry-matching descriptors and the fourteen geometry-ML descriptors, with units/definitions. Verify near-equal endpoint selection (closest 5% of 28,203 pairs), 96 restricted vs 564 all-pair closest-2% geometry comparisons; preserve which pairs were **selected examples** versus global optima.
- Select one **second, non-M085 endpoint-matched** example using a fixed algorithm and percentile; present mechanism distance as distance in the selected A/E coordinates, not site chemistry.
- Reconstruct exact final ExtraTrees model and preprocessing. Rerun one controlled group/topology-aware test on validated structural groups; the two DB0 identifier groups alone cannot support five-fold GroupKFold. Include training-fold median baseline, R², MAE, bias and target-tail diagnostics. No tuning after grouped-test results.
- On **the same split and hyperparameters**, test a predeclared limited panel of simulation-independent charge/field descriptors: geometry-only, charge-only, combined. Audit leakage and report negative results honestly.
- Reconstruct state- and gas-specific uncertainty and uncertainty-conditioned top-24 membership **if original seed records support it**; distinguish original point-estimate 7-replacement statement from uncertainty-aware selection robustness.

**Deliverable:** \`review/03_EXISTING_DATA_PHYSICS.md\`, reproducible CSV/plots, \`review/03_ML_VALIDATION.md\`, frozen second-pair selection and shortlist uncertainty results.

**PASS gate:** All ML metrics originate from demonstrably identical targets/splits; no leakage; chemistry and pore interpretations bounded to verified structures; no posthoc selection of a convenient matched pair.

## Phase 4 — New path simulations: reverse order, staged attraction, energy cross-scoring (Miguel M10–M12/M59; Uzair U18)

**Fixed core panel:** up to 20 frozen cases from Phase 0/2, not the full 238.

**States:** \`00=WCA, charges off\`; \`10=full LJ, charges off\`; \`01=WCA + framework–guest Coulomb\` (new); \`11=full LJ + Coulomb\`. Match guest, framework, cell, accessibility mask, cutoffs, charging convention and temperature.

**Actions**
- First reproduce \`00/10/11\` endpoint values within registered numerical uncertainties; reject a run with a mismatched Hamiltonian before using it as an extension.
- Compute \`01\` and nonadditivity \`I=L11−L10−L01+L00\`, with seed/block uncertainty. State clearly that it measures **path dependence in this model**, not a unique physical decomposition.
- Calculate \`U(λ)=U_WCA+λ(U_LJ−U_WCA)\` at **nine predeclared λ values**: \`0, 0.05, 0.10, 0.20, 0.35, 0.50, 0.70, 0.85, 1\`; both gases. Allow **no more than two additional λ values per structure** where needed to bracket a crossing. No interpolating endpoints and calling the result a measured threshold. If no resolved crossing, report unresolved.
- Cross-evaluate multiple potentials on the **same insertion configurations** where possible. Use correct Boltzmann weights, logsumexp and effective sample size; do not naively average energies or apply reweighting with poor overlap. Independent insertion is the reference cross-check.
- Quantify \`ln S(λ)\`, \`λ*\` where statistically supported, and the effect of path order for the frozen panel. Do not generalize subset results to the full cohort without a selection/uncertainty qualification.

**Deliverable:** job manifest, per-seed \`ln K_H\` by gas/state/λ, uncertainty and weight-overlap diagnostics, frozen numerical result tables, at most one main and one SI path-dependence graphic.

**PASS gate:** Endpoints match the baseline under exactly defined settings; overlap and uncertainty criteria are met; any unresolved cases are marked and omitted from strong claims.

## Phase 5 — New model sensitivity and independent reference check (Uzair U16/U19/U20; Miguel M22/M57)

**Fixed sensitivity panel:** at most eight frameworks, selected *before results* from the core panel, including M085 and matched/typical controls.

**Actions**
- Compare **one** alternate framework charge scheme (choose DDEC6 or EQeq only if actually supportable) with baseline, consistently keeping structures/guest models/cell convention matched. Recompute charged states and appropriate controls; no silent changes to underlying LJ parameters.
- Compare **one** alternative internally coherent guest model for both CO₂ and N₂ (e.g. TraPPE only where adequately parameterized), recomputing all corresponding WCA/LJ/full states if the guest LJ parameters change. Evaluate preference signs, electrostatic tail, M085 contrast and shortlist implications *within the tested subset*.
- Benchmark 2–5 chemically and thermodynamically comparable literature/experimental Henry coefficients/heats where valid, with temperature, activation, units and model definitions. If no valid comparator exists, report only a plausibility check, not external validation.
- Document model dependence as a *result*, not a reason to keep expanding the study to more forcefields or many candidate structures.

**Deliverable:** exact alternate-model files and hashes, per-gas results, unit-normalized comparison table, one compact model-sensitivity SI table/figure.

**PASS gate:** One charge scheme, one guest model, and available benchmark evidence fully reported; no claims beyond the fixed panel.

## Phase 6 — Rewrite and figure correction, directly from validated evidence (all writing/figure comments)

**Actions**
- Lead Abstract/Introduction with (1) nonunique interaction fingerprints for similar endpoints, (2) geometry–electrostatics prediction gap under the tested CV regime, (3) seven of 24 shortlisted MOFs replaced upon restoring charges; treat universal WCA→LJ reversal as the model-specific baseline.
- Explain quadrupole/charge/dispersion physics without asserting unmeasured binding motifs. Compare honestly with charged/uncharged screening and free-energy/interaction-switch work; bound claims to rigid 298 K Henry selectivity and selected MOFs, not mixed-gas process performance.
- Remove version/history/audit jargon, repeated closure checks, redundant matched-pair paragraphs and scattered caveats. Keep one appropriate limitations section. Condense duplicative SI §§17–21 without removing reproducibility essentials.
- Figures: keep Shayan's verified 1(d)/4(c) redesign unless source-level criticism requires changes; repair 1b/d redundancy, Figure 2b misleading “electrostatic share”, Figure 3 target/baseline labels, Figure 4b bar-value labels and structural identities, Figure 5c undefined categories, Figure 6a structural meaning/6c explicit “0 retained/24 replaced” and “17 retained/7 replaced”, all SI cross-references and print-size fonts. Add only data-backed new panels from Phases 2–5; remove or merge one existing panel if the figure count should remain bounded.
- Correct symbolic notation (unused gas \`g\`), exact definitions and units, bibliography author lists and irrelevant chemisorption reference, titles/data-availability wording, SI housekeeping and build instructions. Verify Angelo and Uzair affiliations, contributions, acknowledgments, funding and COI **with the actual authors**; never invent statements.
- Keep the reviewer-facing comment matrix current; mark already-fixed issues against the compiled final version rather than editing them again.

**Deliverable:** complete source \`main.tex\`, \`supporting_information.tex\`, bib and required figure sources/graphics, compiled PDFs; section-by-section change report \`review/06_MANUSCRIPT_CHANGELOG.md\`.

**PASS gate:** Main/SI statements match final numerical tables; no unsupported chemistry, no version-specific research diary in prose; all figure values, manuscript references and journal layout pass.

## Phase 7 — Independent release audit and synchronized submission

**Actions**
- Run clean-checkout numerical-source checks, simulation-subset QA, per-gas/ML verification, figure regeneration, PDF compilation, reference integrity and checksum verification. Preserve original simulations in a protected archive. Recompute summaries; never rewrite data to match manuscript text.
- Resolve every \`Mxx\`, \`Sxx\`, \`Uxx\` status with evidence, manuscript location and one-paragraph response. Distinguish \`CORRECTED\` from \`LIMITATION_DISCLOSED\` and \`BLOCKED\`; do not fake full reviewer satisfaction.
- Commit onto \`review-miguel-uzair\` with individual stage reports; merge into \`main\` **only after complete scientific and document sign-off**. Export one Overleaf ZIP pinned to that merged commit, not to a mutable branch without a record. Verify the exported ZIP matches main/SI/bib/figures in Git apart from intentional LaTeX path adjustments.

**Deliverable:** \`review/FINAL_REVIEW_RESPONSE.md\`, final \`COMMENT_MATRIX.csv\`, release checksums, reproduction tiers, final compiled PDFs, synchronized Overleaf package and exact Git commit.

**PASS gate:** All scientific tests either passed or have reviewer-visible evidence-backed limitations; all manuscript/figure issues corrected; final Git/Overleaf content reconciled.

## Operational rule for the next turn

The user will supply a **file tree**. Execute **Phase 0 only**: produce a source-of-truth file inventory, find missing indispensable items, reconcile the V14 manuscript baseline against the current Git data, and create the complete atomic comment matrix. Do **not** begin Phase 1 structural analysis, model retraining, new simulations, figure redesign, or manuscript rewriting in that same turn. Proceed sequentially after explicit phase review.

## Scope exclusions

Not part of this revision: unrelated MOF discovery/screening projects; expanding the population beyond the selected 238; new GCMC adsorption isotherm studies; dynamic flexibility or mixed-gas breakthrough predictions; broad optimization sweeps; adding extra alternative forcefields/charge methods; many post-hoc matched pairs; exploratory ML feature fishing. Uzair's separate request for molecular-simulation tutorials is retained as correspondence but excluded from the manuscript workplan.
