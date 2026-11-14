# Phase1C acceptance: PASS

**Execution and provenance: PASS.** All1428 initial gas-specific jobs completed, with3 independently seeded streams per gas/framework and1,000,000 cumulative attempts per run. All238 original retained identifiers are present; M081/M189 remain historical exclusions. Existing output/configuration hash verification and all714 paired-gas stream checks completed. No rerun or extension was launched.

**Frozen precision/convergence:238/238 PASS;0 flagged.** The primary0.10 SE rule, conservative registered SE components, ESS>=1000/gas and4.5-SE disjoint-half guards are unchanged. Missing95%-resolved sign is reported separately and does not trigger extra sampling.

None. All238 frameworks meet every frozen initial-cohort precision/convergence criterion; no additional seeds are indicated by those rules.

## Numerical comparison

| Quantity | Historical | Corrected |
|---|---|---|
| Median lnS_WCA | -0.203749485237 | -0.207469591893 |
| exp(median lnS_WCA) | 0.81566668214 | 0.81263795218 |
| Median attractive increment A | 2.53737562365 | 2.53268730205 |
| exp(median A), manuscript convention | 12.6464383687 | 12.5872865682 |
| Spearman WCA vs LJ | -0.750859763428 | -0.796558631927 |
| Spearman A vs E | -0.0885675386621 | -0.0992305189646 |
| N2-favoring WCA point estimates | 238 | 238 |
| Positive attractive increments | 238 | 238 |
| WCA sign-unresolved intervals | 19 | 0 |

Historical sign-unresolved count uses the manuscript's1.96*SE normal approximation; corrected intervals use the frozen t(df2)*registered-SE rule and actual paired covariance. These are disclosed conventions, not an identical interval construction. Corrected interval counts:{'N2_FAVORED': 238}. Point preference changes:0. Maximum corrected registered SE:0.00395264291.

## Ranking consequences

| Comparison | Spearman | Median absolute rank change | Max promotion | Max demotion | Top24 overlap |
|---|---|---|---|---|---|
| original_WCA_to_LJ | -0.750859763 | 102.0 | 234.0 | 226.0 | 0 |
| corrected_WCA_to_LJ | -0.796558632 | 103.0 | 235.0 | 230.0 | 0 |
| original_to_corrected_WCA | 0.951115322 | 10.5 | 59.0 | 85.0 | 23 |
| original_to_corrected_attraction | 0.997375869 | 2.5 | 22.0 | 16.0 | 21 |
| unchanged_LJ_to_full | 0.905055057 | 9.0 | 175.0 | 55.0 | 17 |

Old versus corrected WCA top24 retains23/24; attraction top24 retains21/24. Rank1 means highest value; promotion means old rank minus corrected rank. Full/LJ ranks and their17/24 common shortlist remain unchanged. Numeric entries describe point rankings, not an uncertainty-certified ordering of near ties. Largest WCA value change: M211, -0.748585283669 -> -0.575742266105 (corrected minus historical +0.172843017564); its A changes by the opposite amount. Median absolute WCA change: 0.0182380440135. Largest WCA promotion: M083 (184 -> 125); largest demotion: M052 (104 -> 189).

## Scientific conclusions

| Scientific statement | Disposition after correction | Boundary |
|---|---|---|
| All repulsive-reference point estimates favor N2 | SURVIVES: 238/238; 0 point sign changes | Model-defined WCA reference, not measured accessibility. |
| Attraction reverses N2 preference | SURVIVES as point estimates: 238/238 A>0; all 238 unchanged LJ endpoints favor CO2 | Population precision flags must accompany any affected rows. |
| Median12.65-fold attractive enhancement | CHANGES numerically to 12.587287-fold (-0.4677%) | Uses exp(median A), not median(exp A). |
| Strong WCA-to-LJ rank reversal | SURVIVES; rho -0.750860 -> -0.796559 | Exact ranks, shifts and WCA shortlist membership require corrected tables. |
| Weak attraction/electrostatic point association | SURVIVES as a point description; rho -0.088568 -> -0.099231 | Original bootstrap CI belongs to old A; not regenerated here. |
| Individual WCA sign intervals at 95% | {'N2_FAVORED': 238} | Registered per-framework t intervals are not a simultaneous familywise guarantee. |
| Geometry predicts attraction/WCA better than E | NOT REVALIDATED for corrected targets | WCA/A OOF targets changed; no refit or scoring of stale predictions against new targets. |
| Historical15-MOF alternative-force-field robustness | NOT REVALIDATED | Its legacy endpoint/angular sampling does not validate corrected WCA; no alternative-force-field work performed. |
| LJ/full-only findings and electrostatic increments | UNCHANGED numerically | Their existing independent physical/model/convergence limitations remain. |

## Matched-case comparison

| Fixed original pair | Historical &#124;delta A&#124; | Corrected &#124;delta A&#124; | Unchanged &#124;delta E&#124; |
|---|---|---|---|
| M099/M136 | 1.366852966 | 1.35705121 | 0.5778429299 |
| M089/M192 | 0.6576376621 | 0.7025034011 | 0.325855276 |
| M043/M085 | 0.6378037318 | 0.5851143342 | 1.892038547 |
| M029/M085 | 0.6283855158 | 0.6195040679 | 1.859993403 |

The same 1411 stored full-endpoint-matched pairs were reevaluated; no framework/panel selection was performed. Median mechanism distance 0.188850888 -> 0.186241224;95th percentile 0.750057211 -> 0.730983101. The original highlighted pair M085/M223 now has distance 2.49349598 and corrected distance rank 2.0. Full endpoint differences and E contrasts remain unchanged. This is numerical mechanism-coordinate nonuniqueness, not an atomistic binding-site claim.

The corrected table preserves all238 rows even if precision flagged. No fit, bootstrap interval, alternative force field, new model, new MOF or accessibility investigation was added. Population medians and correlations are arithmetic descriptions of this fixed population; the old bootstrap intervals for changed quantities are not reused. Original numerical reproduction remains reproducibility of the historical table, while this version corrects its WCA measure/accumulation defects.

## Handoff

Seven requested files contain the actual protocol/manifest/data/comparison/dependencies/acceptance. The pre-execution manifest remains byte-identical; existing failure reports were archived before replacement. Supporting corrected rank, matched-pair, fixed-endpoint and source-trace tables are in work/phase1c_corrected_wca_20261114/aggregation. Per-job weights/checkpoints/commands remain under jobs; no immutable result was modified.

Scientific kernel SHA256:7f32df788cc05a02d1e4ae556f7c4634ba2f91eb91d37246673f191bc45854e0. Frozen precision rules SHA256:252d40b6453b360b30e0aa5a593310370687bac4335b806216b9ee39de8850a8. Original authoritative SHA256:f317eef220e6f8757be6aa8d6e4ec29b9bf90e0eeaad8d86009a265b65b1b149. Report/analysis artifact hashes are recorded in the dedicated work directory. Original simulations,scientific data,manuscript,figures and pinned Git commit remain unchanged. Stop at this Phase1C report; no Phase2 work occurred.
