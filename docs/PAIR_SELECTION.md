# Pair-selection reconciliation

The 238-framework cohort and retained case IDs are unchanged. Nine matching descriptors are standardized over that cohort using population standard deviations. These are distinct from the 14 geometry regression features.

The original candidate builder iterates over each row's three nearest neighbors, retaining a pair only for `i < j`, then drops duplicate pair IDs. This creates **384** candidates, not an exhaustive undirected nearest-neighbor graph: a reverse neighbor can be omitted by the index condition. The case selector keeps the lower distance quartile, **96 pairs**, using cutoff **0.25916457244131114**, then maximizes attraction or electrostatic contrast. This reproduces M089/M192 and M029/M085. The operation depends on original row order, which is preserved and checksum-protected.

The manuscript had instead described retaining the closest 2% of **all 28,203** unique pairs: floor(0.02 × 28,203) = **564** candidates. Independent enumeration yields:

| Rule and target | Pair | Geometry distance | Target contrast |
|---|---|---:|---:|
| Archived restricted set, attraction | M089/M192 | 0.1991704168396062 | 0.6576376621059161 |
| All-pair closest 2%, attraction | M099/M136 | 0.4629286213924029 | 1.366852966063336 |
| Archived restricted set, electrostatics | M029/M085 | 0.2575292552493385 | 1.859993402796716 |
| All-pair closest 2%, electrostatics | M043/M085 | 0.3953638804901030 | 1.892038546603417 |

The retained examples are optimal **within the archived restricted set** and illustrative relative to the exhaustive rule. Figure 4 continues to show M029/M085, preserving its 6.42-fold contrast and gas-resolved values. It does not claim the all-pair optimum.

[Exact reconciliation](../data/final/pair_selection_reconciliation.csv), [564-pair candidate set](../data/final/geometry_closest_2percent_candidates.csv), [96-pair set](../data/final/archived_geometry_candidate_set.csv), and [original alias mapping](../data/provenance/framework_aliases.csv) make both operations inspectable. `scripts/reconcile_results.py` regenerates them; the release verifier independently enumerates the exhaustive optima. The [archived code](archived_code/) is retained as evidence, not executed to fit models or run simulations.

The archived code establishes the operation implemented; its presence does not independently establish when selection was frozen. The revised text removes unsupported temporal preregistration assertions. No pair has been substituted into the original illustrative figure.
