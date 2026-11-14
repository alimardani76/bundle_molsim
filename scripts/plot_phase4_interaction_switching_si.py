#!/usr/bin/env python3
"""Plot saved Phase 4 results only; no simulation, fitting or new intervals.

From the repository root:
  python scripts/plot_phase4_interaction_switching_si.py

Output: figures/si/figS5_interaction_switching.pdf
Requires the existing NumPy/Matplotlib environment. CSV identities are frozen
below. The established figure style is read as literals rather than importing
regenerate_figures.py, whose import would modify the existing figure-build log.
Every numerical line/marker/interval is checked against its source CSV before
export. Connecting segments are visual guides, never fitted curves or roots.
"""

from __future__ import annotations

import ast
import csv
import hashlib
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import MultipleLocator
import numpy as np


REPO = Path(__file__).resolve().parents[1]
SOURCE = REPO / "data" / "revision" / "phase4"
OUTPUT = REPO / "figures" / "si" / "figS5_interaction_switching.pdf"
PANEL = ("M002", "M029", "M043", "M085", "M089", "M192", "M084", "M171")
GRID = np.array([0, 0.05, 0.10, 0.20, 0.35, 0.50, 0.70, 0.85, 1.0])
EXPECTED = {
    "04_ATTRACTION_SWITCHING.csv":
        "cb89ae99530e30af83c68ab62d2b0618deb4cda23bf3a002444e98162e6daa73",
    "04_INTERACTION_NONADDITIVITY.csv":
        "c55a1e1d9e5897b6844577d8508920f3f2c06d3610b0072e3e7cd881368df9f5",
}


def established_style():
    """Reuse the current plotting infrastructure without its import side effects."""
    tree = ast.parse((REPO / "scripts" / "regenerate_figures.py").read_text(encoding="utf-8"))
    palette, rc = {}, None
    names = {"INK", "TEAL", "CORAL", "BLUE", "GOLD", "PURPLE", "GREY"}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in names:
                    palette[target.id] = ast.literal_eval(node.value)
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            call = node.value
            if ast.unparse(call.func) == "plt.rcParams.update":
                rc = ast.literal_eval(call.args[0])
    assert set(palette) == names and rc is not None, "Established style changed; inspect before plotting."
    # Same fonts, vector embedding and palette; sizes adapted to a 184-mm SI figure.
    rc.update({
        "font.size": 8, "axes.titlesize": 9, "axes.labelsize": 8,
        "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
        "legend.fontsize": 7.5, "axes.labelcolor": palette["INK"],
        "text.color": palette["INK"], "xtick.color": palette["INK"],
        "ytick.color": palette["INK"], "axes.edgecolor": palette["INK"],
        "axes.titleweight": "normal", "mathtext.fontset": "dejavusans",
        "pdf.compression": 9,
    })
    return palette, rc


def read_frozen(name):
    path = SOURCE / name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == EXPECTED[name], f"Source changed: {name}"
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def floats(rows, column):
    values = np.array([float(r[column]) for r in rows], dtype=float)
    assert np.isfinite(values).all(), column
    return values


def bounds_check(mean, low, high, family_low, family_high):
    assert np.all(low <= mean) and np.all(mean <= high)
    assert np.all(family_low <= low) and np.all(high <= family_high)


def checked_line(ax, x, y, **kwargs):
    line, = ax.plot(x, y, **kwargs)
    np.testing.assert_array_equal(line.get_xdata(), x)
    np.testing.assert_array_equal(line.get_ydata(), y)
    return line


def checked_intervals(ax, positions, low, high, *, horizontal=False, **kwargs):
    """Draw actual saved endpoints, without constructing or recalibrating CIs."""
    if horizontal:
        artist = ax.hlines(positions, low, high, **kwargs)
        expected = np.stack((np.column_stack((low, positions)),
                             np.column_stack((high, positions))), axis=1)
    else:
        artist = ax.vlines(positions, low, high, **kwargs)
        expected = np.stack((np.column_stack((positions, low)),
                             np.column_stack((positions, high))), axis=1)
    np.testing.assert_array_equal(np.asarray(artist.get_segments()), expected)
    return artist


def main():
    curves = read_frozen("04_ATTRACTION_SWITCHING.csv")
    corners = read_frozen("04_INTERACTION_NONADDITIVITY.csv")
    assert len(curves) == 72 and len(corners) == 8
    assert {r["alias"] for r in curves} == set(PANEL)
    assert {r["alias"] for r in corners} == set(PANEL)
    assert len({(r["alias"], r["lambda_value"]) for r in curves}) == 72
    assert len({r["alias"] for r in corners}) == 8
    corner = {r["alias"]: r for r in corners}
    color, rc = established_style()
    # The first six colors are the established palette; the last two distinguish
    # the remaining fixed cases. No framework is selected or sorted by its result.
    colors = [color[k] for k in ("BLUE", "TEAL", "PURPLE", "CORAL", "GOLD", "GREY")]
    colors += ["#A23A6A", "#44542A"]
    markers = ["o", "s", "^", "D", "v", "P", "X", ">"]

    with plt.rc_context(rc):
        fig = plt.figure(figsize=(7.25, 4.75), facecolor="white")
        gs = fig.add_gridspec(1, 2, width_ratios=[1.44, 1],
                              left=0.09, right=0.985, bottom=0.30,
                              top=0.89, wspace=0.40)
        axa, axb = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])
        zoom = axa.inset_axes([0.095, 0.61, 0.50, 0.35])
        for ax in (axa, zoom):
            ax.axhline(0, color=color["INK"], linewidth=0.7, linestyle=(0, (3, 3)), zorder=0)
        zoom.axvspan(0.10, 0.20, color="#E8EEF1", zorder=-1)

        handles = []
        for i, alias in enumerate(PANEL):
            rows = sorted((r for r in curves if r["alias"] == alias),
                          key=lambda r: float(r["lambda_value"]))
            x, y = floats(rows, "lambda_value"), floats(rows, "L")
            np.testing.assert_array_equal(x, GRID)
            assert all(r["n_seeds"] == "3" for r in rows)
            assert all(r["precision_pass"] == "True" for r in rows[:-1])
            # The archived LJ endpoint has no retained insertion-weight stream.
            # Its intentionally blank precision flag is not converted to PASS.
            assert rows[-1]["origin"] == "REUSED_ORIGINAL_LJ_HENRY"
            assert rows[-1]["precision_pass"] == "" and rows[-1]["unresolved"]
            lo, hi = floats(rows, "CI95_lower"), floats(rows, "CI95_upper")
            flo, fhi = floats(rows, "family95_lower"), floats(rows, "family95_upper")
            bounds_check(y, lo, hi, flo, fhi)
            # The reused endpoints and four-corner table must describe the same L.
            np.testing.assert_allclose(y[[0, -1]],
                [float(corner[alias]["L00"]), float(corner[alias]["L10"])], rtol=0, atol=1e-12)
            c, marker = colors[i], markers[i]
            checked_intervals(axa, x, lo, hi, color=c, linewidth=0.9, alpha=0.85, zorder=2)
            line = checked_line(axa, x, y, color=c, marker=marker, markersize=3.1,
                                markeredgewidth=0.55, linewidth=1.05, zorder=3)
            handles.append(line)
            use = x <= 0.20
            checked_intervals(zoom, x[use], flo[use], fhi[use],
                              color=c, linewidth=0.65, alpha=0.5, zorder=2)
            checked_intervals(zoom, x[use], lo[use], hi[use],
                              color=c, linewidth=1.8, alpha=0.95, zorder=3)
            checked_line(zoom, x[use], y[use], color=c, marker=marker, markersize=2.0,
                         linewidth=0.65, markeredgewidth=0.4, zorder=4)

        axa.set(xlim=(-0.015, 1.015), ylim=(-0.83, 3.9),
                xlabel=r"Attraction coupling, $\lambda$",
                ylabel=r"Log selectivity, $L=\ln S_{\mathrm{CO_2/N_2}}$")
        axa.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        axa.yaxis.set_major_locator(MultipleLocator(1))
        axa.text(-0.16, 1.07, "A", transform=axa.transAxes,
                 fontsize=11, fontweight="bold", color=color["TEAL"])
        axa.set_title("Attraction switching (charges off)", loc="left", pad=15)
        zoom.set(xlim=(-0.012, 0.215), ylim=(-0.89, 0.52))
        zoom.set_xticks([0, .1, .2], ["0", "0.10", "0.20"])
        zoom.set_yticks([-.5, 0, .5], ["-0.5", "0", "0.5"])
        zoom.tick_params(labelsize=6.5, length=2, pad=1.5)
        zoom.set_facecolor("white")
        zoom.text(.03, 1.045, r"Low-$\lambda$ detail", transform=zoom.transAxes, fontsize=7)
        zoom.spines["top"].set_visible(True)
        zoom.spines["right"].set_visible(True)
        for spine in zoom.spines.values():
            spine.set_linewidth(0.5)

        yr = np.arange(len(PANEL), dtype=float)
        means = floats([corner[a] for a in PANEL], "I_reference")
        low = floats([corner[a] for a in PANEL], "I_cov_bound_CI95_lower")
        high = floats([corner[a] for a in PANEL], "I_cov_bound_CI95_upper")
        family_low = floats([corner[a] for a in PANEL], "I_cov_bound_family95_lower")
        family_high = floats([corner[a] for a in PANEL], "I_cov_bound_family95_upper")
        bounds_check(means, low, high, family_low, family_high)
        for i, alias in enumerate(PANEL):
            r = corner[alias]
            # Algebra checks existing values; no new statistical estimates.
            np.testing.assert_allclose(means[i], float(r["L11"]) - float(r["L10"])
                - float(r["L01"]) + float(r["L00"]), rtol=0, atol=1e-12)
            assert r["I_point95_sign"] == "POSITIVE"
            assert (r["I_family8_sign"] == "POSITIVE") == (family_low[i] > 0)
            checked_intervals(axb, yr[i:i+1], family_low[i:i+1], family_high[i:i+1],
                              horizontal=True, color=colors[i], linewidth=0.8, zorder=2)
            checked_intervals(axb, yr[i:i+1], low[i:i+1], high[i:i+1],
                              horizontal=True, color=colors[i], linewidth=3.2, zorder=3)
            qualified = alias in {"M085", "M084"}
            checked_line(axb, means[i:i+1], yr[i:i+1], linestyle="none", marker="o",
                         markersize=4.5, markeredgewidth=0.95, color=colors[i],
                         markerfacecolor="white" if qualified else colors[i], zorder=4)
        axb.axvline(0, color=color["INK"], linewidth=0.7, linestyle=(0, (3, 3)), zorder=0)
        axb.set_yticks(yr, [a + ({"M085": r"$\dagger$", "M084": r"$\ddagger$"}.get(a, "")) for a in PANEL])
        axb.set(xlim=(-0.18, 2.7), ylim=(7.55, -0.55),
                xlabel=r"$I=L_{11}-L_{10}-L_{01}+L_{00}$")
        axb.set_xticks([0, 1, 2])
        axb.tick_params(axis="y", length=0, pad=5)
        axb.text(-0.24, 1.07, "B", transform=axb.transAxes,
                 fontsize=11, fontweight="bold", color=color["TEAL"])
        axb.set_title("Interaction nonadditivity", loc="left", pad=15)

        # Legend, interval key and sampling cautions remain separate from the data.
        axa.legend(handles, PANEL, ncol=4, frameon=False, handlelength=1.35,
                    columnspacing=0.95, handletextpad=0.4,
                    loc="upper left", bbox_to_anchor=(-0.05, -0.15), borderaxespad=0)
        interval_handles = [
            Line2D([], [], color=color["INK"], lw=3.0, label="95% pointwise"),
            Line2D([], [], color=color["INK"], lw=0.8, label="95% simultaneous"),
        ]
        axb.legend(handles=interval_handles, frameon=False, loc="upper left",
                   bbox_to_anchor=(-0.08, -0.15), borderaxespad=0,
                   handlelength=1.8, labelspacing=0.5)
        fig.text(0.09, 0.105, "A: pointwise intervals; inset also shows simultaneous intervals (72 points).",
                 fontsize=7)
        fig.text(0.09, 0.066, "B: simultaneous family = 8 MOFs. Open markers: qualified full-state estimates.",
                 fontsize=7)
        fig.text(0.09, 0.027,
                 r"$\dagger$ M085: rare tails unresolved.  $\ddagger$ M084: full-CO$_2$ ESS < 1000.", fontsize=7)

        fig.canvas.draw()
        # All drawn uncertainty segments must fit; never clip a saved interval.
        for ax in (axa, zoom, axb):
            xmin, xmax = sorted(ax.get_xlim())
            ymin, ymax = sorted(ax.get_ylim())
            for collection in ax.collections:
                if not hasattr(collection, "get_segments"):
                    continue
                ends = np.asarray(collection.get_segments()).reshape(-1, 2)
                assert np.all((ends[:, 0] >= xmin) & (ends[:, 0] <= xmax))
                assert np.all((ends[:, 1] >= ymin) & (ends[:, 1] <= ymax))
        # No clipping of any text, including titles, inset labels and legends.
        renderer = fig.canvas.get_renderer()
        frame = fig.bbox
        for item in fig.findobj(matplotlib.text.Text):
            if not item.get_visible() or not item.get_text():
                continue
            box = item.get_window_extent(renderer)
            assert box.x0 >= frame.x0 - 1 and box.y0 >= frame.y0 - 1, item.get_text()
            assert box.x1 <= frame.x1 + 1 and box.y1 <= frame.y1 + 1, item.get_text()
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(OUTPUT, format="pdf", metadata={
            "Title": "Attraction switching and four-corner interaction nonadditivity",
            "Author": "P01 scientific workspace",
            "Subject": "Saved Phase 4 results; source CSV SHA-256: "
                       + "; ".join(f"{k}={v}" for k, v in EXPECTED.items()),
            "Creator": f"Matplotlib {matplotlib.__version__}; plot_phase4_interaction_switching_si.py",
            "CreationDate": None, "ModDate": None,
        })
        plt.close(fig)
    # Recheck that plotting did not change the scientific source bytes.
    for name in EXPECTED:
        read_frozen(name)
    print("PASS: 72 curve points, 8 primary I values, and all drawn CSV interval endpoints checked.")
    print("No fitted/interpolated crossings, recalculated intervals or diagnostic-endpoint substitutions.")
    print(f"Python plotting dependencies: NumPy {np.__version__}; Matplotlib {matplotlib.__version__}")
    print(OUTPUT)


if __name__ == "__main__":
    main()
