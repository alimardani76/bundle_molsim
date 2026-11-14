**Attraction switching and interaction nonadditivity in eight fixed frameworks at 298 K.**
**(A)** CO2/N2 log selectivity, `L = ln S`, at the nine evaluated couplings
`lambda = 0, 0.05, 0.10, 0.20, 0.35, 0.50, 0.70, 0.85, 1`, for
`U(lambda) = U_WCA + lambda(U_LJ - U_WCA)` with charges off. Symbols are the
saved mean seed log ratios; connecting lines guide the eye and are not fitted
curves. Main-axis whiskers are pointwise 95% intervals. In the low-lambda inset,
thick whiskers are pointwise intervals and thin whiskers are the saved
Bonferroni simultaneous intervals over all 72 framework/coupling means. The
shaded strip marks the tested-node interval 0.10-0.20, not a fitted crossing.
All eight pointwise sign reversals are bracketed by these nodes; the same
adjacent-node bracket is resolved simultaneously only for M085 and, marginally,
M084 (lower bound at lambda=0.20: +0.000130311). Simultaneously resolved wider
sign bounds are 0.05-0.20 for M002/M029/M043/M089/M192 and 0.05-0.35 for M171.
All eight remain N2-favoring at lambda=0.05 under the simultaneous intervals.
No exact, unique or minimum crossing is inferred.

**(B)** Primary four-corner nonadditivity,
`I = L11 - L10 - L01 + L00 = E_after_LJ - E_before_LJ`, where
`00 = WCA`, `10 = LJ without charges`, `01 = WCA + Coulomb`, and
`11 = LJ + Coulomb`. Thick segments show saved pointwise 95% intervals and thin
segments the saved eight-framework Bonferroni simultaneous intervals. Both
use the estimated unknown-cross-state-covariance SE bound, not the smaller
independence approximation. Markers use the original archived LJ/full
endpoints and the Phase 4 00/01 estimates; the common-pose diagnostic I is not
substituted. All eight pointwise intervals exclude zero conditionally; the
simultaneous intervals include zero for M043, M089 and M192. A nonzero I means
that increments depend on switching order; the final equilibrium selectivity
remains a state property. These are path-defined responses, not unique
energetic fractions or evidence of specific adsorption sites.

Three independent replicate streams underlie each new condition. New-state
SEs are the maximum of between-seed and propagated raw/block estimates, with
measured paired gas/state covariance where available; original endpoint SEs
include between-seed and native block uncertainty. The original LJ endpoint
weight streams are unavailable: later common-pose diagnostics do not certify
historical endpoint ESS. The displayed intervals
are the existing t-scaled estimates (df=2); the SE bound is not a rigorous
confidence guarantee against unsampled tails. Panel A uses mean seed log
ratios, including its reused WCA endpoint, rather than the distinct Phase 1C
log ratio of pooled factors. Open markers qualify full-state results:
M085 (dagger) retains unresolved full-CO2 rare-event/tail uncertainty despite
pooled diagnostic ESS=1868.27; M084 (double dagger) has full-CO2 diagnostic
ESS=871.43, below the registered 1000 threshold. Their panel-B effect sizes
and apparent simultaneous resolution are conditional, not convergence
certificates. These full-state limitations do not invalidate their separately
passing neutral switching curves in panel A. No inference of connected pore
accessibility, population-wide universality or exact effect ranking is made.

Sources: [completed Phase 4 report](../review/04_INTERACTION_SWITCHING.md),
[attraction-switching results](../data/revision/phase4/04_ATTRACTION_SWITCHING.csv)
and [four-corner results](../data/revision/phase4/04_INTERACTION_NONADDITIVITY.csv).

Reproduce from the repository root using the existing figure environment:

```powershell
python scripts/plot_phase4_interaction_switching_si.py
```

The script checks the frozen CSV SHA-256 values and every plotted numerical
coordinate/interval endpoint. It reads the established Matplotlib style
without executing the legacy figure builder and writes only
`figures/si/figS5_interaction_switching.pdf`.
It performs no simulations, fits, interval recalibration or crossing estimation.
