# Restored final prediction evidence

The initial v9 ZIP supplied a transcription of final geometry metrics but only earlier-model prediction evidence. A fuller historical `mof_selectivity_mechanisms` project contains the matching `path_b_analysis/leakage_free_descriptors/` records and a publication copy under `mof_selectivity_publication/`.

The two copies of each restored descriptor table are byte-identical. Their SHA-256 digests also match the independently archived authoritative-file manifest:

- Prediction table: `45eab3592d4f9f650e4732a480c180050c4baeeadfad27fc63f61e7ab7912b90`.
- Metric table: `77a2e6c781031acb826fec992486e04e60cb25342be1e5e717d0ae7bb00304a8`.
- Feature manifest: `c52b9b15b312d73b94ea43e5923a747c2c222d66c9e539da8a3c69758a6f776c`.

The unmodified prediction file contains **1,904 rows**, representing two feature-set orderings (`geometry`, `combined`) for four targets over 238 frameworks. The published final analysis uses the **952 geometry rows**, with 14 descriptors. Predictions from the `combined` ordering are not substituted. The nearby `final_descriptor_hierarchy` analysis uses 25 geometry features and different scores; it is not the source of the final v5/v9 numbers. Earlier v2 random/group-holdout models also remain distinct.

`data/final/geometry_oof_predictions.csv` is a documented geometry-subset export. It preserves observed/predicted values and adds normalized target names, reconstructed fold IDs, and the comparator definition. The original saved vectors do not contain standalone fold membership. Fold metadata are reconstructed from the archived KFold(5, shuffle=True, random_state=20260918) protocol and unchanged source row order; they are not misrepresented as independently saved historical fold artifacts.

The inspected archived source puts median imputation and standardization inside the training-fold pipeline and uses 500 ExtraTrees, minimum leaf size 3 and max_features 0.7. Only the recorded pre-simulation geometry columns enter the final geometry model. Its comparison MAE is the **full-cohort median reference**, not a median predictor trained separately within each fold. The text and Figure 3 now state this distinction while preserving all published values.

Saved predictions reproduce exact R²/MAE values and the 5,000-resample bootstrap, including predictability-gap interval **[0.5597498842208415, 0.9053752180468466]**. This is an arithmetic audit and resampling of saved predictions, not a new fit or an independent training replay. Saved estimators were not needed or used.

The fuller archive also supplies matched force-field bridge rows, frozen geometry strata/shuffle results, finite probe-pilot descriptor tables, and recorded molecular protocol/parameter files. Their compact sources were restored and audited without recalculating molecular energies. [Source manifest](RESTORED_SOURCE_MANIFEST.json) records relative source paths, digests and historical manifest matches.
