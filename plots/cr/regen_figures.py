#!/usr/bin/env python3
"""
regen_figures.py -- Task 7 Part A: redraw Figures 2, 4, 5 and 7 at print scale.

The defect this fixes is uniform across the paper's script-generated figures: they are
drawn on a 5 in canvas and included at 2.1 to 2.2 in, so a 12 pt label lands on the page
at about 5 pt. Figure 2's smallest element measures 3.1 pt against 10 pt body text.

The recipe is the one Task 6 established for Figure 6: draw the canvas at exactly the
width the panel prints at, so the LaTeX placement scale is 1.0 and the point size set
here is the point size that lands. Nothing is enlarged after the fact, so line weights
stay proportionate too.

THIS IS A LEGIBILITY PASS, NOT A REDESIGN. Every panel plots exactly the values its
predecessor plotted. Nothing is transcribed: _origdata executes each original script
with its file writes stubbed and hands back its module globals, and the arrays below are
those objects. Colors, series order and chart types are carried over unchanged.

Outputs go to Figs/cr/. Nothing in Figs/ or plots/MaestroRAG/Plots/ is touched.
Output is byte-deterministic; SOURCE_DATE_EPOCH is pinned below.

Usage:  python3 plots/cr/regen_figures.py
"""

import json
import os
import sys

os.environ.setdefault("SOURCE_DATE_EPOCH", "0")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.patches import Patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _origdata as O  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "Figs", "cr")
MANIFEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plotted_values.json")

# ------------------------------------------------------------------ print geometry
# figure* spans \textwidth = 505.89 TeX pt = 504.000 PDF pt = 7.000 in.
# A single column is \columnwidth = 243.91125 TeX pt = 3.3750 in.
TEXTWIDTH_IN = 504.0 / 72.0
COLWIDTH_IN = 243.91125 / 72.27

W_FIG2 = 0.30 * TEXTWIDTH_IN   # 2.100 in
W_FIG4 = 0.32 * TEXTWIDTH_IN   # 2.240 in
W_FIG7 = 0.32 * TEXTWIDTH_IN   # 2.240 in
# Figure 5 sits inside a wrapfigure of 0.65\linewidth and is included at \linewidth
# within it, so it prints at 0.65 x columnwidth, not 0.9 x columnwidth.
W_FIG5 = 0.65 * COLWIDTH_IN    # 2.194 in

# Figure 2's panels were included with a height=1in override on top of a width, which
# scaled x and y differently and distorted the glyphs. The override is dropped in the
# .tex; these canvases set the aspect instead. See the report for the height cost.
H_FIG2, H_FIG4, H_FIG7, H_FIG5 = 1.46, 1.58, 1.92, 1.86

BASE = 8.0
INK = "#1a1a1a"
GRID = "#cccccc"

plt.rcParams.update({
    "font.size": BASE, "axes.labelsize": BASE, "axes.titlesize": BASE,
    "xtick.labelsize": BASE, "ytick.labelsize": BASE, "legend.fontsize": BASE,
    "font.family": "sans-serif", "axes.linewidth": 0.6,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.0, "ytick.major.size": 2.0,
    "pdf.fonttype": 42, "figure.dpi": 100,
})

PASTEL = sns.color_palette("pastel").as_hex()
BAR = dict(edgecolor="black", linewidth=0.5)
RECORD = {}


def frame(ax, xlabel=None, ylabel=None):
    ax.grid(axis="y", color=GRID, linewidth=0.4, linestyle="--", alpha=0.9)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("black")
    ax.tick_params(colors=INK, pad=1.5)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=BASE, color=INK, labelpad=1.5)
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=BASE, color=INK, labelpad=1.5)


def save(fig, name, values):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name + ".pdf")
    fig.savefig(path, format="pdf")
    plt.close(fig)
    RECORD[name] = values
    print(f"  {name:<38} {fig.get_size_inches()[0]:.3f} x {fig.get_size_inches()[1]:.3f} in")


def grid_series(recs, xkey, huekey, vkey):
    """list-of-dicts -> (x order, hue order, {hue: [values in x order]})."""
    xs, hues = [], []
    for r in recs:
        if r[xkey] not in xs:
            xs.append(r[xkey])
        if r[huekey] not in hues:
            hues.append(r[huekey])
    table = {h: [] for h in hues}
    for h in hues:
        for x in xs:
            m = [r[vkey] for r in recs if r[xkey] == x and r[huekey] == h]
            table[h].append(m[0] if m else None)
    return xs, hues, table


def grouped_bars(ax, xs, hues, table, colors):
    n = len(hues)
    w = 0.8 / n
    idx = np.arange(len(xs))
    for j, h in enumerate(hues):
        pos = idx - 0.4 + (j + 0.5) * w
        vals = [0 if v is None else v for v in table[h]]
        ax.bar(pos, vals, w, color=colors[j % len(colors)], label=str(h), **BAR)
    ax.set_xticks(idx)
    ax.set_xticklabels([str(x) for x in xs])


# =============================================================== FIGURE 2 (6 panels)
def fig2a():
    ns = O.load("pieChart.py")
    stages, startup, execution = ns["stages"], ns["startup"], ns["execution"]
    total = ns["grand_total"]
    base = ns["base_colors"]
    dark = ns["darken_color"]
    fig, ax = plt.subplots(figsize=(W_FIG2, H_FIG2))
    x = np.arange(len(stages))
    for i, st in enumerate(stages):
        ax.bar(x[i], startup[i], 0.55, color=base[i], **BAR)
        ax.bar(x[i], execution[i], 0.55, bottom=startup[i], color=dark(base[i], 1.3), **BAR)
        tot = startup[i] + execution[i]
        ax.text(x[i], tot + total * 0.015, f"{tot / total * 100:.1f}%",
                ha="center", va="bottom", fontsize=BASE, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(["E", "R", "A", "G"])
    ax.set_ylim(0, 9.9)
    frame(ax, "Stage", "Time (s)")
    fig.subplots_adjust(left=0.20, right=0.985, top=0.975, bottom=0.20)
    save(fig, "stacked_graph", {"stages": stages, "startup": list(startup),
                                "execution": list(execution), "grand_total": total})


def fig2b():
    df = O.load("FwdPassBS.py")["df_8cores"]
    xs = list(df["Batch Size"]); ys = list(df["Latency (s)"])
    fig, ax = plt.subplots(figsize=(W_FIG2, H_FIG2))
    ax.bar(np.arange(len(xs)), ys, 0.62, color=PASTEL[:len(xs)], **BAR)
    ax.set_xticks(np.arange(len(xs))); ax.set_xticklabels([str(v) for v in xs])
    frame(ax, "Batch Size", "Latency (s)")
    fig.subplots_adjust(left=0.235, right=0.985, top=0.975, bottom=0.20)
    save(fig, "forwardpass_8cores", {"x": xs, "y": ys})


def fig2c():
    df = O.load("FwdPass.py")["df_bs16"]
    xs = list(df["# Cores"]); mn = list(df["Min Latency (s)"]); mx = list(df["Max Latency (s)"])
    fig, ax = plt.subplots(figsize=(W_FIG2, H_FIG2))
    c = PASTEL[1]
    for i in range(len(xs)):
        ax.plot([i, i], [mn[i], mx[i]], color=c, linewidth=1.6, zorder=2)
        ax.scatter([i, i], [mn[i], mx[i]], color=c, edgecolor="black",
                   linewidth=0.5, s=22, zorder=3)
    ax.set_xticks(np.arange(len(xs))); ax.set_xticklabels([str(v) for v in xs])
    frame(ax, "# Cores", "Latency (s)")
    fig.subplots_adjust(left=0.235, right=0.985, top=0.975, bottom=0.20)
    save(fig, "forwardpass_bs16_range_discrete", {"x": xs, "min": mn, "max": mx})


def fig2d():
    df = O.load("stackedLatencyMotivation.py")["df_batch"]
    xs = list(df["Batch Size"]); f = list(df["Index Fetch (s)"]); s = list(df["Similarity Search (s)"])
    ylim = 15
    fig, ax = plt.subplots(figsize=(W_FIG2, H_FIG2))
    idx = np.arange(len(xs))
    ax.bar(idx, f, 0.62, color=PASTEL[0], label="Index Fetch", **BAR)
    ax.bar(idx, s, 0.62, bottom=f, color=PASTEL[1], label="Sim. Search", **BAR)
    ax.set_ylim(0, ylim)
    tot32 = f[-1] + s[-1]
    ax.text(idx[-1], (f[-1] + ylim) / 2, f"{tot32:.2f} s", ha="center", va="center",
            rotation=90, fontsize=BASE, color=INK)
    ax.set_xticks(idx); ax.set_xticklabels([str(v) for v in xs])
    frame(ax, "Batch Size", "Time (s)")
    ax.legend(loc="upper left", frameon=False, fontsize=BASE, handlelength=1.0,
              handletextpad=0.35, borderpad=0.1, labelspacing=0.2)
    fig.subplots_adjust(left=0.20, right=0.985, top=0.975, bottom=0.20)
    save(fig, "batchsize_stacked_linear_labeled",
         {"x": xs, "index_fetch": f, "similarity_search": s, "ylim": ylim})


def fig2e():
    df = O.load("CharacterizationPlot1.py")["df_cores"]
    xs = list(df["# Cores"]); ys = list(df["Latency(s)"])
    fig, ax = plt.subplots(figsize=(W_FIG2, H_FIG2))
    ax.bar(np.arange(len(xs)), ys, 0.62, color=PASTEL[:len(xs)], **BAR)
    ax.set_xticks(np.arange(len(xs))); ax.set_xticklabels([str(v) for v in xs])
    frame(ax, "# Cores", "Latency (s)")
    fig.subplots_adjust(left=0.20, right=0.985, top=0.975, bottom=0.20)
    save(fig, "latency_cores", {"x": xs, "y": ys})


def fig2f():
    df = O.load("CharacterizationPlot1.py")["df_dbsize"]
    xs = list(df["DB Size (M)"]); ys = list(df["Latency(s)"])
    fig, ax = plt.subplots(figsize=(W_FIG2, H_FIG2))
    ax.bar(np.arange(len(xs)), ys, 0.62, color=PASTEL[:len(xs)], **BAR)
    ax.set_xticks(np.arange(len(xs))); ax.set_xticklabels([str(v) for v in xs])
    frame(ax, "DB Size (M)", "Latency (s)")
    fig.subplots_adjust(left=0.20, right=0.985, top=0.975, bottom=0.20)
    save(fig, "latency_dbsize", {"x": xs, "y": ys})


# =============================================================== FIGURE 4 (6 panels)
def _bs_db_panel(recs, name, ylabel, dbfmt=True):
    xs, hues, table = grid_series(recs, "Batch Size", "DB Size", "Latency")
    fig, ax = plt.subplots(figsize=(W_FIG4, H_FIG4))
    grouped_bars(ax, xs, hues, table, PASTEL)
    frame(ax, "Batch Size", ylabel)
    short = [str(h).replace(" mil", "M") for h in hues]
    hs = [Patch(facecolor=PASTEL[i % len(PASTEL)], label=short[i], **BAR) for i in range(len(hues))]
    ax.legend(handles=hs, loc="upper left", ncol=2, frameon=False, fontsize=BASE,
              handlelength=1.0, handletextpad=0.35, columnspacing=0.7,
              borderpad=0.1, labelspacing=0.2)
    top = max(v for h in hues for v in table[h] if v is not None)
    ax.set_ylim(0, top * 1.42)
    fig.subplots_adjust(left=0.175, right=0.985, top=0.975, bottom=0.185)
    save(fig, name, {"batch_sizes": xs, "db_sizes": [str(h) for h in hues],
                     "values": {str(h): table[h] for h in hues}})


def fig4():
    ns = O.load("SpeedUpPlot4090.py")
    _bs_db_panel(ns["data_ours"], "4090LatencyOurs", "Latency (s)")
    _bs_db_panel(ns["data_edge"], "4090speedupEdgeRAG", "Speedup vs EdgeRAG")
    _bs_db_panel(ns["data_flash"], "4090speedupFlashRAG", "Speedup vs FlashRAG")
    _bs_db_panel(ns["data_pipe"], "4090speedupPipeRAG", "Speedup vs PipeRAG")
    ns8 = O.load("AllSpeedup4080.py")
    _bs_db_panel(ns8["data_ours_4080"], "4080Latency_MaestroRAG", "Latency (s)")
    # merged 4080 speedup: hue is the baseline, x is batch size
    recs = ns8["data_speedup_merged"]
    xs, hues, table = grid_series(recs, "Batch Size", "Implementation", "Speedup")
    fig, ax = plt.subplots(figsize=(W_FIG4, H_FIG4))
    grouped_bars(ax, xs, hues, table, PASTEL)
    frame(ax, "Batch Size", "Speedup")
    hs = [Patch(facecolor=PASTEL[i % len(PASTEL)], label=str(hues[i]), **BAR) for i in range(len(hues))]
    ax.legend(handles=hs, loc="upper left", ncol=1, frameon=False, fontsize=BASE,
              handlelength=1.0, handletextpad=0.35, borderpad=0.1, labelspacing=0.2)
    ax.set_ylim(0, max(v for h in hues for v in table[h] if v is not None) * 1.45)
    fig.subplots_adjust(left=0.155, right=0.985, top=0.975, bottom=0.185)
    save(fig, "4080Speedup_Merged", {"batch_sizes": xs, "baselines": [str(h) for h in hues],
                                     "values": {str(h): table[h] for h in hues}})


# ==================================================================== FIGURE 5
def fig5():
    df = O.load("JetsonThemVsUs.py")["df"]
    xs = list(df["Batch Size"]); edge = list(df["EdgeRAG"])
    ours = list(df["MaestroRAG"]); sp = list(df["Speedup"])
    fig, ax1 = plt.subplots(figsize=(W_FIG5, H_FIG5))
    idx = np.arange(len(xs)); w = 0.38
    ax1.bar(idx - w / 2, edge, w, color=PASTEL[0], label="EdgeRAG", **BAR)
    ax1.bar(idx + w / 2, ours, w, color=PASTEL[1], label="MaestroRAG", **BAR)
    ax1.set_xticks(idx); ax1.set_xticklabels([str(v) for v in xs])
    frame(ax1, "Batch Size", "Latency (s)")
    ax2 = ax1.twinx()
    ax2.plot(idx, sp, color="#c0392b", marker="o", markersize=3.2, linewidth=1.2,
             label="Speedup")
    ax2.set_ylabel("Speedup", fontsize=BASE, color=INK, labelpad=1.5)
    ax2.tick_params(colors=INK, pad=1.5)
    ax2.spines["top"].set_visible(False)
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="upper center", bbox_to_anchor=(0.5, -0.26),
               ncol=2, frameon=False, fontsize=BASE, handlelength=1.0,
               handletextpad=0.3, columnspacing=0.6, borderpad=0.1)
    ax1.set_ylim(0, max(edge) * 1.12)
    ax2.set_ylim(0, max(sp) * 1.18)
    fig.subplots_adjust(left=0.175, right=0.845, top=0.985, bottom=0.375)
    save(fig, "JetsonThemVsUs", {"batch_sizes": xs, "EdgeRAG": edge,
                                 "MaestroRAG": ours, "Speedup": sp})


# =============================================================== FIGURE 7 (3 panels)
def fig7a():
    recs = O.load("mapping.py")["data"]
    ours_colors = ["#a6cee3", "#1f78b4"]
    emp_colors = ["#ffb347", "#ff7f0e"]
    groups = ["1M", "2M", "4M", "8M"]
    fig, ax = plt.subplots(figsize=(W_FIG7, H_FIG7))
    x = np.arange(len(groups)); w = 0.36
    rec = {}
    for i, g in enumerate(groups):
        for meth, cols, dx in (("MaestroRAG", ours_colors, -w / 2),
                               ("Empirical", emp_colors, w / 2)):
            r = [d for d in recs if d["DB Size"] == g and d["Method"] == meth][0]
            tot = r["Encode"] + r["Retrieve"]
            ax.bar(x[i] + dx, r["Encode"], w, color=cols[0], **BAR)
            ax.bar(x[i] + dx, r["Retrieve"], w, bottom=r["Encode"], color=cols[1], **BAR)
            ax.text(x[i] + dx, r["Encode"] / 2, f"{r['Encode']}", ha="center",
                    va="center", fontsize=BASE, color=INK)
            ax.text(x[i] + dx, r["Encode"] + r["Retrieve"] / 2, f"{r['Retrieve']}",
                    ha="center", va="center", fontsize=BASE, color=INK)
            ax.text(x[i] + dx, tot + 0.3, f"BS:{r['Batch Size']}", ha="center",
                    va="bottom", rotation=90, fontsize=BASE, color=INK)
            rec[f"{g}/{meth}"] = {"Batch Size": r["Batch Size"], "Encode": r["Encode"],
                                  "Retrieve": r["Retrieve"], "Total": tot}
    ax.set_xticks(x); ax.set_xticklabels(groups)
    ax.set_ylim(0, 14.6)
    frame(ax, "DB Size", "# Cores")
    hs = [Patch(facecolor=ours_colors[0], label="MR-E", **BAR),
          Patch(facecolor=ours_colors[1], label="MR-R", **BAR),
          Patch(facecolor=emp_colors[0], label="Emp-E", **BAR),
          Patch(facecolor=emp_colors[1], label="Emp-R", **BAR)]
    ax.legend(handles=hs, loc="upper center", bbox_to_anchor=(0.5, -0.28), ncol=2,
              frameon=False, fontsize=BASE, handlelength=1.0, handletextpad=0.3,
              columnspacing=0.6, borderpad=0.1, labelspacing=0.25)
    fig.subplots_adjust(left=0.155, right=0.985, top=0.985, bottom=0.345)
    save(fig, "cores_allocation_stacked", rec)


def fig7b():
    recs = O.load("mainLatencyResult2.py")["data_main"]
    colors = {"MaestroRAG": "#69A1FF", "EdgeRAG": "#8FD694",
              "FlashRAG": "#FF9EE2", "PipeRAG": "#FFB870"}
    cache_color = "#CBA7EA"
    devices = ["4090", "4080", "Jetson"]
    order = ["MaestroRAG", "EdgeRAG", "FlashRAG", "PipeRAG"]
    ylim = 20.0
    fig, ax = plt.subplots(figsize=(W_FIG7, H_FIG7))
    gw = 0.84; bw = gw / len(order)
    rec = {}
    for i, dev in enumerate(devices):
        for j, pol in enumerate(order):
            xp = i - gw / 2 + (j + 0.5) * bw
            v = [d["Latency"] for d in recs if d["Device"] == dev and d["Implementation"] == pol]
            v = v[0] if v else None
            rec[f"{dev}/{pol}"] = v
            if v is None:
                ax.bar(xp, 0, bw, color="white", edgecolor="black", linewidth=0.5, hatch="///")
                ax.text(xp, 0.6, "N/A", ha="center", va="bottom", rotation=90,
                        fontsize=BASE, color="#c0392b")
                continue
            if dev == "4090" and pol == "MaestroRAG":
                cache = [d["Latency"] for d in recs if d["Device"] == dev
                         and d["Implementation"] == "MaestroRAG w/ Cache"][0]
                rec[f"{dev}/MaestroRAG w/ Cache"] = cache
                drawn = min(v, ylim)
                ax.bar(xp, cache, bw, color=cache_color, **BAR)
                ax.bar(xp, drawn - cache, bw, bottom=cache, color=colors[pol], **BAR)
            else:
                ax.bar(xp, min(v, ylim), bw, color=colors[pol], **BAR)
            if v > ylim:
                ax.text(xp, ylim * 0.985, f"{v:g}", ha="center", va="top", rotation=90,
                        fontsize=BASE, color=INK)
    ax.set_xticks(np.arange(len(devices))); ax.set_xticklabels(devices)
    ax.set_ylim(0, ylim)
    frame(ax, "Device", "Latency (s)")
    hs = [Patch(facecolor=colors[p], label=p.replace("MaestroRAG", "MR")
                .replace("EdgeRAG", "ER").replace("FlashRAG", "FR")
                .replace("PipeRAG", "PR"), **BAR) for p in order]
    hs.append(Patch(facecolor=cache_color, label="MR cache", **BAR))
    ax.legend(handles=hs, loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=3,
              frameon=False, fontsize=BASE, handlelength=1.0, handletextpad=0.3,
              columnspacing=0.6, borderpad=0.1, labelspacing=0.25)
    fig.subplots_adjust(left=0.155, right=0.985, top=0.985, bottom=0.345)
    save(fig, "MainLatencyResults2", rec)


def fig7c():
    recs = O.load("goodput.py")["data_main"]
    colors = {"MaestroRAG": "#69A1FF", "EdgeRAG": "#8FD694",
              "FlashRAG": "#FF9EE2", "PipeRAG": "#FFB870"}
    devices = ["RTX 4090", "Jetson"]
    order = ["MaestroRAG", "EdgeRAG", "FlashRAG", "PipeRAG"]
    fig, ax = plt.subplots(figsize=(W_FIG7, H_FIG7))
    gw = 0.8; bw = gw / len(order)
    rec = {}
    for i, dev in enumerate(devices):
        for j, impl in enumerate(order):
            xp = i - gw / 2 + (j + 0.5) * bw
            v = [d["Throughput"] for d in recs if d["Device"] == dev
                 and d["Implementation"] == impl]
            v = v[0] if v else None
            rec[f"{dev}/{impl}"] = v
            if v is None:
                ax.bar(xp, 0, bw, color="white", edgecolor="black", linewidth=0.5, hatch="///")
                ax.text(xp, 0.05, "N/C", ha="center", va="bottom", rotation=90,
                        fontsize=BASE, color="#c0392b")
            else:
                ax.bar(xp, v, bw, color=colors[impl], **BAR)
                ax.text(xp, v + 0.03, f"{v:.3g}", ha="center", va="bottom",
                        rotation=90, fontsize=BASE, color=INK)
    ax.set_xticks(np.arange(len(devices))); ax.set_xticklabels(devices)
    ax.set_ylim(0, 1.95)
    frame(ax, "Device", "Throughput (QPS)")
    hs = [Patch(facecolor=colors[p], label=p.replace("MaestroRAG", "MR")
                .replace("EdgeRAG", "ER").replace("FlashRAG", "FR")
                .replace("PipeRAG", "PR"), **BAR) for p in order]
    ax.legend(handles=hs, loc="upper center", bbox_to_anchor=(0.5, -0.30), ncol=4,
              frameon=False, fontsize=BASE, handlelength=1.0, handletextpad=0.3,
              columnspacing=0.6, borderpad=0.1)
    fig.subplots_adjust(left=0.175, right=0.985, top=0.985, bottom=0.315)
    save(fig, "ThroughputResults", rec)


def main():
    print("regenerating 16 panels at print scale:")
    for fn in (fig2a, fig2b, fig2c, fig2d, fig2e, fig2f, fig4, fig5, fig7a, fig7b, fig7c):
        fn()
    with open(MANIFEST, "w", encoding="utf-8") as fh:
        json.dump(RECORD, fh, indent=2, sort_keys=True, default=float)
    print(f"\nwrote {len(RECORD)} panels to {OUT}")
    print(f"wrote plotted-value manifest to {MANIFEST}")
    print(f"  Fig 2 canvas {W_FIG2:.3f} in (0.30 x textwidth); "
          f"Fig 4/7 {W_FIG4:.3f} in (0.32 x); Fig 5 {W_FIG5:.4f} in (0.90 x columnwidth)")
    print(f"  smallest type set anywhere: {BASE:g} pt, at placement scale 1.0")


if __name__ == "__main__":
    main()
