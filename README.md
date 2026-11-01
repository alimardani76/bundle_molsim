# CO2/N2 selectivity: interaction-stage evidence

Data and analytical reproduction for **When Does CO2/N2 Selectivity Emerge in Metal–Organic Frameworks?** This reconciled v9 release preserves the original **238-framework** table and the verified paper results. It restores the matching final **14-feature saved out-of-fold (OOF) predictions**, distinguishes illustrative matched pairs from exhaustive-search optima, and includes six main figures, four SI figures and a TOC graphic.

[1. Simulate](#1-simulate) · [2. Simulation outputs](#2-simulation-outputs) · [3. Article results](#3-article-results) · [4. Figures](#4-figures)

## 1. Simulate

This repository supports **analysis of archived outputs**, saved-prediction metric/uncertainty calculations and final figure reproduction. It does not supply a complete fresh simulation or model-training workflow.

The [recorded molecular protocol](docs/model_provenance/production_protocol.json) specifies RASPA3 3.0.29, rigid frameworks at 298 K, the UFF framework baseline and charged/full versus LJ-only modes. [Guest and force-field records](docs/model_provenance/) document the archived definitions. WCA results were generated with the archived repulsive-reference workflow.

Fresh simulation additionally needs the complete original framework CIFs, per-job inputs, job runner and executable environment. Those are not provided here as a complete runnable set, so no fresh simulation command is claimed. No RASPA/LAMMPS simulation or predictive model fitting was performed during this reconciliation.

## 2. Simulation outputs

- [Unchanged authoritative cohort](data/authoritative/mechanism_238_authoritative.csv): 238 unique frameworks; SHA-256 `f317eef220e6f8757be6aa8d6e4ec29b9bf90e0eeaad8d86009a265b65b1b149`.
- [Archived numerical provenance](data/provenance/): full/LJ gas-specific seed summaries, WCA base/extension/rescue rows, final OOF predictions, descriptor manifest and sensitivity evidence.
- WCA accounting is 2,052 archive-wide gas-specific jobs = **2,034 retained + 18 in two excluded frameworks**. These are jobs, not 2,052 frameworks.
- Full/LJ Henry coefficients are in mol kg^-1 Pa^-1; selectivity ratios and log increments are dimensionless. The archived convention averages log Henry coefficients across seeds; WCA pools Boltzmann factors before taking logs.

## 3. Article results

Use Python 3.13. The [tested environment](environment/software.json) and [pinned dependencies](requirements.txt) record the analytical build.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python scripts/make_results.py
python scripts/verify_package.py
```

On macOS/Linux, activate with `source .venv/bin/activate`. Each Python entrypoint also works with an explicit interpreter path.

[Final tables](data/final/) contain coordinate summaries, families, shortlist ranks, endpoint pairs, exact saved-OOF metrics, and the [pair-rule reconciliation](data/final/pair_selection_reconciliation.csv). The original M089/M192 and M029/M085 examples remain unchanged. They maximize their contrasts within the archived **96-pair restricted candidate set**, and are illustrative examples relative to the separate **564-pair exhaustive closest-2% search**. The latter has different optima, reported in the SI and reconciliation table.

The final geometry evidence is the 14-feature `geometry` subset of the restored prediction table, not the earlier v2 model or a neighboring 25-feature model. Fold assignments are **reconstructed metadata** from the archived KFold seed and preserved source row order. The comparator is a **full-cohort median reference**, not an OOF-trained baseline. [Model provenance](docs/model_provenance/geometry_cv_protocol.json) states the audit boundary. Metrics and the 5,000-resample bootstrap are recomputed from saved predictions; no model is refit.

The verifier independently checks the cohort, original seed aggregation, exact identities (absolute tolerance 1e-12 log units), published rounding, OOF alignment, bootstrap, saved-stratum shuffles, bridge/pilot evidence, figure inputs, manuscript figure references and digests. [Numerical audit](quality_control/NUMERICAL_AUDIT.md), [reconciliation CSV](quality_control/NUMERICAL_RECONCILIATION.csv), and [change log](CHANGELOG_SCIENTIFIC.md) give the evidence.

## 4. Figures

The [source map](data/figure_sources/SOURCE_MAP.json) identifies inputs for **all 11 figures**, including Figure 6, S1–S4 and the TOC. Figure 3 uses metrics recalculated from the restored final OOF vectors.

```powershell
python scripts/make_figures.py
python scripts/verify_package.py --prepare-checksums
python scripts/write_checksums.py
python scripts/verify_package.py
```

The equivalent Windows command is `cmd /c run_figures_windows.bat`. Outputs are in [figures/main](figures/main/), [figures/si](figures/si/) and [figures/toc](figures/toc/), in PDF, PNG and compressed 600-dpi TIFF. These are the final scientific panels and annotations; font rendering, PDF metadata and pixels can vary across environments, so byte/pixel identity is not claimed.

[Main manuscript](manuscript/main.pdf) and [SI](supporting_information/supporting_information.pdf) include all six and four figures respectively. To compile them with a LaTeX installation containing `achemso`, pdfLaTeX and BibTeX:

```powershell
python scripts/build_documents.py
python scripts/verify_package.py --prepare-checksums
python scripts/write_checksums.py
python scripts/verify_package.py
```

After intentional regeneration, refresh digests only after the numerical/document checks pass. The committed [checksum manifest](quality_control/SHA256SUMS.txt) covers the selected release files. CI checks the delivered digests before running the analytical self-test; it does not run simulations or train models.
