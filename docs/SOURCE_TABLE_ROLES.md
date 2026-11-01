# Numerical source roles

| Location | Role |
|---|---|
| `data/authoritative/mechanism_238_authoritative.csv` | Unchanged final 238-framework cohort; preserved original SHA-256 |
| Other `data/authoritative` scalar/sensitivity/case tables | Original frozen supporting tables, checked against the cohort |
| `geometry_cv_FINAL_v5_transcribed.csv` | Original rounded metric transcription retained for comparison; not used as the final plotting authority |
| `geometry_holdout_metrics_v2.csv`, `data/source_v2/figure_3_source.csv` | Earlier model evidence; never substituted for the final 14-feature evaluation |
| `same_endpoint_pairs.csv` | Historical 50-row candidate table using a 0.10 endpoint threshold; not the final 1,411-pair membership list |
| `data/provenance/descriptor_hierarchy_*` | Restored original saved-prediction evidence and original exact summaries |
| `data/provenance/*jobs.csv`, `raspa_final_gas_rows.csv` | Archived gas-specific job/seed result summaries; not a new molecular simulation |
| `data/final` | Regenerated final metrics, ranks, endpoint membership, and explicit optimal-versus-illustrative pair results |
| `data/figure_sources` | Explicit current CSV inputs read by the plotting code for every final figure |
| `data/derived_v7` | Small original family/shortlist exports, retained and reproducible for continuity |

Folder names from v9 are preserved for traceability. A historical table in `authoritative` does not make a different model final, or turn a candidate table into final selection membership. Exact sources and transformations are documented in the traceability matrix and restored-source manifest.
