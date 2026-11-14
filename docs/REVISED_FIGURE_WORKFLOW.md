# Coauthor guide: reproduce and edit the revised figures

This `revision` branch intentionally contains **numerical and plotting sources only**, not the manuscript/SI. Use the final Overleaf ZIP for article and SI text.

## One command

From the repository root (Python 3.10+):

```powershell
python -m pip install -r requirements_figures.txt
python scripts/plot_revision_all.py
```

This generates `figures/main/fig1...fig6*.pdf`, `figures/si/figS1...figS4*.pdf`, `figures/toc/TOC_interaction_stages.pdf`, plus PNG and TIFF renders and two standalone revised panels under `figures/panels/`. No molecular simulation or ML training occurs.

## Which files should I edit?

| Goal | Source |
|---|---|
| All corrected article panels and TOC | `scripts/plot_revision_main.py` |
| SI figures S1, S3, S4 | `scripts/plot_revision_si.py` |
| Figure 3 geometry model metrics | `data/revision/geometry_cv_metrics_for_fig3.csv` |
| Figure 4(b) original gas-response labels | `data/revision/matched_pair_gas_increments.csv` |
| 238-framework mechanisms/ranks | `data/revision/corrected_wca_238.csv` (frozen; do not edit manually) |
| Approved layouts and unchanged figure panels | `data/revision/figure_baselines.zip` (visual canvases, not current data) |

Approved Figure 1(d) and Figure 4(c) artwork is retained by the patched PDF workflow, including corrected WCA numerical labels. The old `scripts/redraw_final_panels.py` is **not** the revised publication entrypoint; its original numbers are outdated. Panel PNG/SVG crops are regenerated from final compound PDFs.

## Scientific invariants

- Cohort: 238 MOFs. Median corrected WCA log selectivity: −0.207469592; median LJ–WCA increment: 2.532687302; median multiplier: 12.59×.
- Corrected WCA–LJ Spearman rank correlation: −0.796559. WCA/LJ top-24 overlap: 0; LJ/full overlap: 17, as **point-estimate** memberships.
- WCA: all 238 N₂-favoring with registered individual precision; not a simultaneous coverage assertion.
- Original full and LJ electrostatic endpoints are unchanged by the WCA correction. Original M029/M085 response data and later M085 diagnostic cohorts must not be mixed.
- Geometry ML numbers are five-random-fold results, not transfer to unknown structures. Figure S2 remains unchanged because it plots the original full–LJ gas response.
- The additional model sensitivity is bounded to a six-MOF panel; its alternative framework-charge arm was blocked, not validated.

## Editing and regeneration

Modify only plot functions or their clearly identified inputs. Run the command; inspect the changed PDF at publication scale. Numeric assertions in plotting scripts reject a 238-row count mismatch, a nonzero WCA/LJ shortlist overlap, and algebraic inconsistency. The figure-output files are derived artifacts. Historical source files under `data/authoritative` and archived simulations are never overwritten.

**Note:** Much of the publication layout is rebuilt with vector overlays on approved historical canvases. It reproduces the final artwork, but not every retained panel is independently editable as a standalone Matplotlib artist. For a redesign of a retained panel, start from its older figure source and intentionally replace its historical data dependency with the corrected source.
