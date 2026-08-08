#!/usr/bin/env python3
"""
fig6_power_energy.py -- camera-ready rebuild of Figure 6 (shepherd item 3).

Replaces Figs/power_energy_comparison.pdf, which showed power and energy on a shared
dual axis with no stage-level decomposition. Output goes to Figs/cr/ so the original
figure and the scripts under plots/MaestroRAG/Plots/ stay untouched as the provenance
record of the submitted version.

WHAT CHANGED, AND WHY
  * A fourth panel decomposes CPU energy by pipeline stage. That is the shepherd's
    actual request.
  * A vertical rule separates the power section from the energy section, as suggested,
    and each section carries its own axis label with units.
  * Energy is reported PER QUERY, matching the 253.3 / 792.00 / 780.93 J the prose
    quotes, rather than per 12 s measurement window.
  * The canvas is drawn at the printed size (7.007 in = \\textwidth) so the LaTeX scale
    factor is 1.0 and an 8 pt label prints at 8 pt.
  * No white text on any fill: every annotation is near-black on a light fill.

THE DENOMINATOR PROBLEM, AND HOW IT IS HANDLED
  The stage shares come from the rebuttal and are shares of IDLE-SUBTRACTED CPU package
  energy, DRAM excluded. The PowerComp joules are IDLE-INCLUSIVE: 579.60 J / 48.30 W is
  exactly the 12 s window, so idle draw sits inside that number. The idle-subtracted
  totals are not recorded anywhere.

  Stacking the shares onto the absolute joule bars would therefore assert that they
  partition a quantity they do not partition, and the error would be exactly the idle
  fraction. Panel 4 is drawn NORMALIZED, on its own percent axis, and labeled as a share
  of attributed energy. Absolute joules stay in panel 3. The two are never mixed.

DATA PROVENANCE
  Panels 1-3: data/MaestroRAGResults.xlsx, PowerComp tab (authorised), rows 2-7.
              Per-query energy divides the tab's window totals by the batch size of 2,
              which is what Section 5.6 already reports.
  Panel 4:    the rebuttal's stage-attributed energy shares. No workbook tab holds them.
              Reproduced exactly as stated, including sums that round to 99.9-100.5.

Usage:  python3 plots/cr/fig6_power_energy.py
Requires matplotlib. Output is byte-deterministic (SOURCE_DATE_EPOCH is pinned below).
"""

import os

# Pin the PDF CreationDate so two runs produce byte-identical output.
os.environ.setdefault("SOURCE_DATE_EPOCH", "0")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTDIR = os.path.join(REPO, "Figs", "cr")
OUTFILE = os.path.join(OUTDIR, "fig6_power_energy_breakdown.pdf")

# ---------------------------------------------------------------- page geometry
# \textwidth of iiswc26.cls at 10pt letterpaper = 505.89 pt. Drawing at exactly this
# width and including at \linewidth inside a figure* gives a scale factor of 1.0.
TEXTWIDTH_IN = 505.89 / 72.27
FIG_W = TEXTWIDTH_IN
FIG_H = 2.62

# Every text element is >= 8 pt, and the canvas is 1:1, so these are page sizes.
BASE = 8.0
plt.rcParams.update({
    "font.size": BASE,
    "axes.labelsize": 8.5,
    "axes.titlesize": 8.5,
    "xtick.labelsize": BASE,
    "ytick.labelsize": BASE,
    "legend.fontsize": BASE,
    "font.family": "sans-serif",
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
    "xtick.major.size": 2.0,
    "ytick.major.size": 2.0,
    "pdf.fonttype": 42,
})

# ------------------------------------------------------------------------- data
SYSTEMS = ["FlashRAG", "PipeRAG", "MaestroRAG"]

# PowerComp tab, rows 2-7. Order: FlashRAG, PipeRAG, MaestroRAG.
AVG_CPU = [48.30, 62.72, 42.37]      # C2, D2, E2
AVG_GPU = [83.67, 58.48, 42.06]      # C3, D3, E3
PEAK_CPU = [184.20, 171.09, 158.30]  # C4, D4, E4
PEAK_GPU = [244.80, 252.43, 244.40]  # C5, D5, E5
ENERGY_CPU_WINDOW = [579.60, 815.24, 254.20]   # C6, D6, E6
ENERGY_GPU_WINDOW = [1004.40, 746.61, 252.36]  # C7, D7, E7

BATCH = 2  # Section 5.6 reports energy per query; the window holds BS=2 queries.
ENERGY_CPU = [v / BATCH for v in ENERGY_CPU_WINDOW]
ENERGY_GPU = [v / BATCH for v in ENERGY_GPU_WINDOW]

# Rebuttal stage shares of idle-subtracted CPU package energy, DRAM excluded.
# Reproduced verbatim. FlashRAG sums to 100.1, PipeRAG to 100.5, MaestroRAG to 99.9;
# these are the rebuttal's own rounding and are NOT renormalized here.
STAGES = ["Encode", "Retrieve (+Augment)", "Augment", "Generation-driving", "Other"]
SHARES = {
    "FlashRAG":   [0.0, 79.2, 0.0, 19.1, 1.8],
    "PipeRAG":    [20.4, 64.5, 0.0, 15.6, 0.0],
    "MaestroRAG": [5.5, 83.2, 0.0, 11.2, 0.0],
}

# ----------------------------------------------------------------------- colors
# All fills are light so that every annotation can be near-black. No white-on-light.
C_CPU = "#9ecae1"
C_GPU = "#fdbe85"
STAGE_COLORS = ["#a6cee3", "#b2df8a", "#fdbf6f", "#cab2d6", "#dddddd"]
INK = "#1a1a1a"
EDGE = "#404040"

BAR_KW = dict(edgecolor=EDGE, linewidth=0.5)


def grouped(ax, cpu, gpu, ylabel, ymax_pad=1.30):
    """Two bars per system, CPU and GPU side by side, values labeled above."""
    xs = range(len(SYSTEMS))
    w = 0.36
    ax.bar([x - w / 2 for x in xs], cpu, w, color=C_CPU, **BAR_KW)
    ax.bar([x + w / 2 for x in xs], gpu, w, color=C_GPU, **BAR_KW)
    top = max(max(cpu), max(gpu))
    for x, (a, b) in enumerate(zip(cpu, gpu)):
        for dx, v in ((-w / 2, a), (w / 2, b)):
            ax.text(x + dx, v + top * 0.02, f"{v:g}", ha="center", va="bottom",
                    rotation=90, fontsize=BASE, color=INK)
    ax.set_ylim(0, top * ymax_pad)
    ax.set_ylabel(ylabel, fontsize=8.5, color=INK)
    style_axis(ax)


def style_axis(ax):
    ax.set_xticks(range(len(SYSTEMS)))
    ax.set_xticklabels(SYSTEMS, rotation=20, ha="right", fontsize=BASE, color=INK)
    ax.tick_params(axis="both", colors=INK, pad=1.5)
    ax.grid(axis="y", color="#cccccc", linewidth=0.4, alpha=0.9)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(EDGE)


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    fig = plt.figure(figsize=(FIG_W, FIG_H))
    # Two header rows sit above the panels: legends on top, section headings below.
    # Column 2 is an empty gutter carrying the power/energy dividing rule; without it
    # the rule and panel 3's y-label collide with panel 3's leftmost tick label.
    gs = fig.add_gridspec(
        1, 5, left=0.075, right=0.995, top=0.735, bottom=0.255,
        wspace=0.82, width_ratios=[1.0, 1.0, 0.30, 1.0, 1.10],
    )
    ax1, ax2, ax3, ax4 = (fig.add_subplot(gs[0, i]) for i in (0, 1, 3, 4))

    # -- Panel 1: average power ------------------------------------------------
    grouped(ax1, AVG_CPU, AVG_GPU, "Average power (W)")

    # -- Panel 2: peak power ---------------------------------------------------
    grouped(ax2, PEAK_CPU, PEAK_GPU, "Peak power (W)")

    # -- Panel 3: energy per query, CPU + GPU stacked --------------------------
    xs = list(range(len(SYSTEMS)))
    w = 0.52
    ax3.bar(xs, ENERGY_CPU, w, color=C_CPU, **BAR_KW)
    ax3.bar(xs, ENERGY_GPU, w, bottom=ENERGY_CPU, color=C_GPU, **BAR_KW)
    totals = [c + g for c, g in zip(ENERGY_CPU, ENERGY_GPU)]
    for x, t in zip(xs, totals):
        ax3.text(x, t + max(totals) * 0.02, f"{t:.0f}", ha="center", va="bottom",
                 fontsize=BASE, color=INK)
    ax3.set_ylim(0, max(totals) * 1.22)
    ax3.set_ylabel("Energy per query (J)", fontsize=8.5, color=INK)
    style_axis(ax3)

    # -- Panel 4: normalized CPU energy composition ----------------------------
    bottoms = [0.0] * len(SYSTEMS)
    for si, stage in enumerate(STAGES):
        vals = [SHARES[s][si] for s in SYSTEMS]
        ax4.bar(xs, vals, 0.52, bottom=bottoms, color=STAGE_COLORS[si], **BAR_KW)
        for x, (v, b) in enumerate(zip(vals, bottoms)):
            if v >= 9.0:  # only label segments tall enough to hold 8 pt text
                ax4.text(x, b + v / 2, f"{v:.1f}", ha="center", va="center",
                         fontsize=BASE, color=INK)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    ax4.set_ylim(0, 108)
    ax4.set_yticks([0, 25, 50, 75, 100])
    ax4.set_ylabel("Share of attributed\nCPU energy (%)", fontsize=8.5, color=INK)
    style_axis(ax4)

    # -- section headings and the dividing rule --------------------------------
    p1, p2 = ax1.get_position(), ax2.get_position()
    p3, p4 = ax3.get_position(), ax4.get_position()
    xrule = (p2.x1 + p3.x0) / 2.0
    fig.lines.append(plt.Line2D([xrule, xrule], [0.055, 0.885], transform=fig.transFigure,
                                color=EDGE, linewidth=1.1))
    fig.text((p1.x0 + p2.x1) / 2, 0.800, "Power", ha="center", va="bottom",
             fontsize=9, fontweight="bold", color=INK)
    fig.text((p3.x0 + p4.x1) / 2, 0.800, "Energy", ha="center", va="bottom",
             fontsize=9, fontweight="bold", color=INK)

    # -- legends, on their own row above the section headings ------------------
    fig.legend(handles=[Patch(facecolor=C_CPU, edgecolor=EDGE, label="CPU"),
                        Patch(facecolor=C_GPU, edgecolor=EDGE, label="GPU")],
               loc="upper left", bbox_to_anchor=(0.075, 1.000), ncol=2,
               frameon=False, fontsize=BASE, handlelength=1.1, handleheight=0.9,
               columnspacing=0.9, handletextpad=0.4)
    used = [0, 1, 3, 4]  # Augment is 0% for every system; omit it from the legend
    fig.legend(handles=[Patch(facecolor=STAGE_COLORS[i], edgecolor=EDGE,
                              label=STAGES[i]) for i in used],
               loc="upper right", bbox_to_anchor=(0.995, 1.000), ncol=4,
               frameon=False, fontsize=BASE, handlelength=1.1, handleheight=0.9,
               columnspacing=0.9, handletextpad=0.4)

    # -- the exclusion, stated in the figure rather than only in the caption ----
    fig.text(0.075, 0.012,
             "EdgeRAG excluded: its on-demand embedding path performs additional, "
             "non-equivalent work.",
             ha="left", va="bottom", fontsize=BASE, color=INK)

    fig.savefig(OUTFILE, format="pdf")
    plt.close(fig)
    print(f"wrote {OUTFILE}")
    print(f"  canvas {FIG_W:.3f} x {FIG_H:.3f} in; \\textwidth = {TEXTWIDTH_IN:.3f} in")
    print(f"  scale factor at \\linewidth inside figure* = "
          f"{TEXTWIDTH_IN / FIG_W:.4f}; smallest type = {BASE:g} pt on the page")


if __name__ == "__main__":
    main()
