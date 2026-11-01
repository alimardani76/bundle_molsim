# Scientific reconciliation of v9

The 238-MOF source CSV and all verified paper results are preserved. No simulation or model refit was performed. Original v9 and source archives remain unchanged. Detailed old/new text and evidence for **34 document/source-description corrections** are recorded in [DOCUMENT_CHANGES.json](quality_control/DOCUMENT_CHANGES.json); the [restored-source manifest](docs/RESTORED_SOURCE_MANIFEST.json) records each recovered original file and its digest. [FILE_CHANGES.csv](quality_control/FILE_CHANGES.csv) inventories added/changed selected release files and their original/final SHA-256 values.

| Previous statement or behavior | Reconciliation | Evidence and affected files |
|---|---|---|
| Examples described as all-pair closest-2% optima | Document actual 384→96 restricted candidate procedure; retain examples; separately report 564-candidate exhaustive optima | Archived case/candidate code; `data/final/pair_selection_reconciliation.csv`; main/SI pair methods and Figure 4 caption |
| Final metrics available only as transcription | Restore matching 14-feature OOF vectors/manifest/protocol; recompute exact metrics and bootstrap; do not substitute v2 or 25-feature predictions | Historical SHA matches; `data/provenance/descriptor_hierarchy_*`; `data/final/geometry_oof_predictions.csv`; Figure 3, main/SI model sections |
| Baseline could be read as fold-trained | Explicitly label full-cohort median reference | Archived fit source; model provenance, main/SI, Figure 3 labels |
| Matching discussion says 14 descriptors | Nine matching descriptors distinguished from 14 regression features | Archived matching code and manifests; main Methods/discussion |
| Preregistration timing asserted from archive | Retain reproducible selection operation without asserting an independently established freeze date | Historical selector and endpoint code; main/SI methods |
| IDs used to assert elemental composition/topology | Restrict to identifier metadata; no atomic or topology attribution inferred | Main matched-case discussion; released evidence scope |
| WCA 2,052 total versus retained seed strata | Explicit 2,052 = 2,034 retained + 18 excluded jobs | Three job tables and retained-ID filter; SI sampling |
| One residual bound reflects stored historical column | State portable 1e-12 tolerance and fresh approximately 8.9e-16 CSV residual | Main closure statement and independent audit |
| Bridge/shuffle/probe evidence absent in v9 ZIP | Restore compact final tables, verify saved evidence without new simulations or fits | `data/provenance`; final evidence audit; SI provenance |
| Figure 4 missing, later figures misnumbered | Include existing verified matched-pair figure; restore six-figure sequence | Main TeX/PDF |
| Figure 3 caption names two of four bars | Describe all four targets and restored saved-prediction basis | Main caption and final Figure 3 |
| Literal rho/citation keys; missing SI S prefixes | Repair TeX escapes and SI figure/table/equation numbering | Main/SI TeX/PDF |
| TOC WCA annotation overlaps sentence | Move explanatory sentence below the plot | Figure generator and regenerated TOC |
| Windows TIFF replacement fails | Explicitly close Pillow TIFF handle before replacement | Figure generator; direct and Windows batch builds |
| Plot summaries contain fixed counts and transcribed model inputs | Derive counts/overlaps from cohort and Figure 3 from saved-OOF metrics; export and read explicit inputs for all figures | Result/source exporters and figure generator |
| Incomplete/stale historical checksum evidence | Preserve history note; build new manifests for selected current deliverables | Historical checksum note and current manifests |
| Broad dependency ranges and limited verifier | Pin tested analytical environment; add independent arithmetic audit, figure/document checks, portable commands and CI self-test | requirements/environment/scripts/CI |

All figure PDFs/PNGs/TIFFs and both manuscript PDFs are regenerated from the corrected source. Numerical agreement and rendering/metadata identity are distinguished. Source and archived-code additions are evidence; no dormant fitting or simulation program is executed by release commands. The release supports analytical reproduction and saved-prediction auditing; it does not claim fresh molecular simulation or training replay.
