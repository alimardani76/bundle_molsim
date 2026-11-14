# Phase1C corrected WCA protocol ? NOT EXECUTION-FROZEN; PREFLIGHT FAIL

No population computation was launched. The current task stops under the explicit instruction: Stop with FAIL if any preflight validation fails.

Failure: The preflight code attempted to resolve repo/data/authoritative/mechanism_238_authoritative.csv through SOURCE_PATH_MAP.csv. That recovered-evidence catalog has no entry for this Git-frozen repository file, causing KeyError before authoritative-file verification.

This is an implementation/provenance-routing error in the new preflight code. No data hash mismatch was detected; absence from that catalog is not evidence that the original data changed. The earlier scientific validation remains its existing scoped evidence.

Completed checks: the copied Phase1B kernel matches SHA2567f32df788cc05a02d1e4ae556f7c4634ba2f91eb91d37246673f191bc45854e0; all existing336 fixed-pose records and their source hash passed recheck without new energy calculations; the original238 identifiers were staged with M081/M189 excluded; CO2/N2 molecular-definition hashes passed. Seven completed checks passed before the lookup exception.

The intended design was1428 gas-specific jobs (238 frameworks,2 gases,3 seeds,1e6 attempts), four workers, one thread each, unchanged isotropic/cumulative Phase1B kernel and Hamiltonian. The staged RNG design uses PCG64 via SeedSequence([20261114,panel_index,seed_label]), sharing a stream across gas partners and separating framework/replicate streams. These planned jobs were NOT generated, fully verified, frozen or executed.

Staged rules are preserved in work/phase1c_corrected_wca_20261114/FROZEN_RULES.json: historical SE(lnS)<=0.10; conservative seed/within-run paired precision; concentration and stationarity guards; extensions at6/9/12 only after completion of the initial cohort. The execution freeze was never issued. No production or extension was authorized by this failed preflight.

Remaining preflight tests were not executed: complete1428 manifest; all238 framework CIF/model hashes; periodic-cell/pair checks; saved-pilot aggregation; checkpoint interruption/recovery; duplicate/overwrite prevention; final resource and execution freeze. The staged wrapper code is unverified and must not be used for production.

Failure records: work/phase1c_corrected_wca_20261114/preflight/PREFLIGHT.json, CHECKS.csv and FAILURE.txt. The failure trace and staged scripts are preserved unchanged. No repair, preflight retry, simulation, downstream statistics, ML fitting, manuscript/figure edit, GitHub write or Phase2 work was performed after the failed gate.
