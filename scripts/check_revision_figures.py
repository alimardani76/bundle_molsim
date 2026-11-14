"""Small, independent release check for revised numerical and plotting materials.

This intentionally does not verify historical manuscript/deck checksums. The revised
branch distributes numerical sources and figures, not an old LaTeX release.
"""
from pathlib import Path
import sys

import fitz
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/revision/corrected_wca_238.csv'
FIGS = [
    *sorted((ROOT / 'figures/main').glob('fig[1-6]_*.pdf')),
    *sorted((ROOT / 'figures/si').glob('figS[1-4]_*.pdf')),
    ROOT / 'figures/toc/TOC_interaction_stages.pdf',
]


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    d = pd.read_csv(DATA)
    check(len(d) == 238 and d.alias.is_unique and d.mof_id.is_unique, '238 distinct MOFs required')
    w = d.lnS_wca_corrected.to_numpy()
    a = d.delta_lnS_attr_corrected.to_numpy()
    e = d.delta_lnS_elec_unchanged.to_numpy()
    lj = d.lnS_LJ_unchanged.to_numpy()
    full = d.lnS_full_unchanged.to_numpy()
    check(np.isfinite(np.stack([w, a, e, lj, full])).all(), 'nonfinite selection data')
    check(np.allclose(w + a, lj, rtol=0, atol=1e-8), 'LJ-WCA decomposition')
    check(np.allclose(lj + e, full, rtol=0, atol=1e-8), 'LJ-full decomposition')
    check(np.all(w < 0) and np.all(lj > 0), 'WCA/LJ preference signs')
    check(d.precision_pass.astype(bool).all() and (d.CI95_upper < 0).all(), 'registered WCA precision')
    check(abs(np.median(w) + 0.207469591892595) < 1e-8, 'corrected WCA median')
    check(abs(np.median(a) - 2.5326873020516754) < 1e-8, 'corrected A median')
    check(abs(spearmanr(w, lj).statistic + 0.7965586319268984) < 1e-8, 'corrected WCA-LJ rho')

    top = lambda vals: set(d.iloc[np.argsort(-vals, kind='stable')[:24]].alias)
    check(len(top(w) & top(lj)) == 0, 'WCA/LJ top-24 overlap')
    check(len(top(lj) & top(full)) == 17, 'LJ/full top-24 overlap')
    metrics = pd.read_csv(ROOT / 'data/revision/geometry_cv_metrics_for_fig3.csv')
    check(metrics.target.tolist() == ['WCA', 'LJ-WCA', 'Charging', 'Full'], 'Fig3 metric target labels')
    check(np.allclose(metrics.R2_geometry_5fold_OOF, [.967506, .879658, .188040, .845241], atol=1e-6), 'Fig3 metrics')

    check(len(FIGS) == 11 and all(f.is_file() for f in FIGS), '11 publication figure PDFs')
    for pdf in FIGS:
        with fitz.open(pdf) as doc:
            check(len(doc) == 1, f'{pdf.name}: expected one page')
            p = doc[0]
            check(p.rect.width > 100 and p.rect.height > 100, f'{pdf.name}: invalid size')
            check(pdf.stat().st_size > 5000, f'{pdf.name}: unexpectedly small')
    print('PASS: 238-framework corrected results, ML figure metrics, 11 publication PDFs')


if __name__ == '__main__':
    try:
        main()
    except (AssertionError, ValueError, KeyError, FileNotFoundError) as exc:
        print('FAIL:', exc, file=sys.stderr)
        sys.exit(1)