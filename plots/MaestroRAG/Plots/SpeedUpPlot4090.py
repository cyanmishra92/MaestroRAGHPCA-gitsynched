#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless environments

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# -----------------------------------------------------------------------------
# 1) Data
# -----------------------------------------------------------------------------

# EdgeRAG (no OOM)
data_edge = [
    {"Batch Size": 2,  "DB Size": "1 mil", "Latency": 1.308357349},
    {"Batch Size": 2,  "DB Size": "2 mil", "Latency": 1.232804233},
    {"Batch Size": 2,  "DB Size": "4 mil", "Latency": 3.621307073},
    {"Batch Size": 2,  "DB Size": "8 mil", "Latency": 9.667003027},

    {"Batch Size": 4,  "DB Size": "1 mil", "Latency": 2.409927942},
    {"Batch Size": 4,  "DB Size": "2 mil", "Latency": 2.260827012},
    {"Batch Size": 4,  "DB Size": "4 mil", "Latency": 4.197581472},
    {"Batch Size": 4,  "DB Size": "8 mil", "Latency": 9.978625954},

    {"Batch Size": 8,  "DB Size": "1 mil", "Latency": 3.398601399},
    {"Batch Size": 8,  "DB Size": "2 mil", "Latency": 3.035607718},
    {"Batch Size": 8,  "DB Size": "4 mil", "Latency": 4.371248268},
    {"Batch Size": 8,  "DB Size": "8 mil", "Latency": 12.0811359},

    {"Batch Size": 16, "DB Size": "1 mil", "Latency": 3.543344956},
    {"Batch Size": 16, "DB Size": "2 mil", "Latency": 3.259259259},
    {"Batch Size": 16, "DB Size": "4 mil", "Latency": 5.618350039},
    {"Batch Size": 16, "DB Size": "8 mil", "Latency": 6.152336082},
]

# FlashRAG (OOM at BS=16)
data_flash = [
    {"Batch Size": 2,  "DB Size": "1 mil", "Latency": 1.974063401},
    {"Batch Size": 2,  "DB Size": "2 mil", "Latency": 2.402116402},
    {"Batch Size": 2,  "DB Size": "4 mil", "Latency": 2.634288272},
    {"Batch Size": 2,  "DB Size": "8 mil", "Latency": 3.157753111},

    {"Batch Size": 4,  "DB Size": "1 mil", "Latency": 2.377902322},
    {"Batch Size": 4,  "DB Size": "2 mil", "Latency": 2.61316369},
    {"Batch Size": 4,  "DB Size": "4 mil", "Latency": 2.506661201},
    {"Batch Size": 4,  "DB Size": "8 mil", "Latency": 2.909923664},

    {"Batch Size": 8,  "DB Size": "1 mil", "Latency": 3.243356643},
    {"Batch Size": 8,  "DB Size": "2 mil", "Latency": 2.578078377},
    {"Batch Size": 8,  "DB Size": "4 mil", "Latency": 2.522702786},
    {"Batch Size": 8,  "DB Size": "8 mil", "Latency": 1.915821501},

    # BS=16 => Out of Memory, so comment out any numeric row
    # {"Batch Size": 16, "DB Size": "1 mil", "Latency": ...},
    # etc.
]

# PipeRAG (OOM at BS=16)
data_pipe = [
    {"Batch Size": 2,  "DB Size": "1M", "Latency": 3.250720461},
    {"Batch Size": 2,  "DB Size": "2M", "Latency": 3.019312169},
    {"Batch Size": 2,  "DB Size": "4M", "Latency": 3.622873769},
    {"Batch Size": 2,  "DB Size": "8M", "Latency": 4.710729902},

    {"Batch Size": 4,  "DB Size": "1M", "Latency": 3.266613291},
    {"Batch Size": 4,  "DB Size": "2M", "Latency": 3.185466112},
    {"Batch Size": 4,  "DB Size": "4M", "Latency": 3.915966387},
    {"Batch Size": 4,  "DB Size": "8M", "Latency": 4.693129771},

    {"Batch Size": 8,  "DB Size": "1M", "Latency": 3.004662005},
    {"Batch Size": 8,  "DB Size": "2M", "Latency": 2.629799085},
    {"Batch Size": 8,  "DB Size": "4M", "Latency": 3.047560412},
    {"Batch Size": 8,  "DB Size": "8M", "Latency": 3.138235294},

    # BS=16 => Out of Memory
]

# Ours (no OOM)
data_ours = [
    {"Batch Size": 2,  "DB Size": "1 mil", "Latency": 3.47},
    {"Batch Size": 2,  "DB Size": "2 mil", "Latency": 3.78},
    {"Batch Size": 2,  "DB Size": "4 mil", "Latency": 4.468},
    {"Batch Size": 2,  "DB Size": "8 mil", "Latency": 5.946},

    {"Batch Size": 4,  "DB Size": "1 mil", "Latency": 3.747},
    {"Batch Size": 4,  "DB Size": "2 mil", "Latency": 4.087},
    {"Batch Size": 4,  "DB Size": "4 mil", "Latency": 4.879},
    {"Batch Size": 4,  "DB Size": "8 mil", "Latency": 6.55},

    {"Batch Size": 8,  "DB Size": "1 mil", "Latency": 4.29},
    {"Batch Size": 8,  "DB Size": "2 mil", "Latency": 5.027},
    {"Batch Size": 8,  "DB Size": "4 mil", "Latency": 6.497},
    {"Batch Size": 8,  "DB Size": "8 mil", "Latency": 9.86},

    {"Batch Size": 16, "DB Size": "1 mil", "Latency": 8.317},
    {"Batch Size": 16, "DB Size": "2 mil", "Latency": 9.72},
    {"Batch Size": 16, "DB Size": "4 mil", "Latency": 12.97},
    {"Batch Size": 16, "DB Size": "8 mil", "Latency": 25.47},
]

# -----------------------------------------------------------------------------
# 2) Build DataFrames with ordered categories
# -----------------------------------------------------------------------------
df_edge  = pd.DataFrame(data_edge)
df_flash = pd.DataFrame(data_flash)
df_pipe  = pd.DataFrame(data_pipe)
df_ours  = pd.DataFrame(data_ours)

# Common batch size order
batch_order_edgeflashours = [2, 4, 8, 16]  # EdgeRAG, FlashRAG, Ours
batch_order_pipe = [2, 4, 8, 16]          # PipeRAG

df_edge["Batch Size"]  = pd.Categorical(df_edge["Batch Size"],  categories=batch_order_edgeflashours, ordered=True)
df_flash["Batch Size"] = pd.Categorical(df_flash["Batch Size"], categories=batch_order_edgeflashours, ordered=True)
df_ours["Batch Size"]  = pd.Categorical(df_ours["Batch Size"],  categories=batch_order_edgeflashours, ordered=True)
df_pipe["Batch Size"]  = pd.Categorical(df_pipe["Batch Size"],  categories=batch_order_pipe, ordered=True)

# Edge/Flash/Ours DB sizes: ["1 mil", "2 mil", "4 mil", "8 mil"]
db_order_edgeflashours = ["1 mil", "2 mil", "4 mil", "8 mil"]
df_edge["DB Size"]  = pd.Categorical(df_edge["DB Size"],  categories=db_order_edgeflashours, ordered=True)
df_flash["DB Size"] = pd.Categorical(df_flash["DB Size"], categories=db_order_edgeflashours, ordered=True)
df_ours["DB Size"]  = pd.Categorical(df_ours["DB Size"],  categories=db_order_edgeflashours, ordered=True)

# PipeRAG DB sizes: ["1M", "2M", "4M", "8M"]
db_order_pipe = ["1M", "2M", "4M", "8M"]
df_pipe["DB Size"] = pd.Categorical(df_pipe["DB Size"], categories=db_order_pipe, ordered=True)

# -----------------------------------------------------------------------------
# 3) Global Seaborn/Matplotlib styling
# -----------------------------------------------------------------------------
sns.set_theme(
    style="whitegrid",
    rc={
        "axes.edgecolor": "black",
        "axes.linewidth": 1,
        "xtick.color": "black",
        "ytick.color": "black",
        "font.size": 12,
        "axes.labelsize": 12,
        "legend.fontsize": 10,
        "grid.color": "0.8"
    }
)
palette = sns.color_palette("pastel")

# -----------------------------------------------------------------------------
# 4) Helper function to plot
# -----------------------------------------------------------------------------
def plot_latency(df, output_filename, YL):
    fig, ax = plt.subplots(figsize=(5, 3))

    sns.barplot(
        data=df,
        x="Batch Size",
        y="Latency",
        hue="DB Size",
        palette=palette,
        edgecolor="black"
    )

    ax.set_xlabel("Batch Size", fontsize=10, labelpad=-10)
    ax.set_ylabel(YL, fontsize=10)
    ax.tick_params(axis='both', labelsize=10)

    # Minor ticks on y-axis
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.tick_params(axis='y', which='minor', direction='in', length=2, color='black')

    # Legend below x-axis
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles,
        labels,
        loc="lower center",
        bbox_to_anchor=(0.45, -0.35),
        ncol=len(labels),
        frameon=False,
        title=None
    )

    # If BS=16 is OOM for this method, place one label at x=3
    if "FlashRAG" in output_filename or "PipeRAG" in output_filename:
        x_center = 3  # group index for BS=16
        y_pos = 0.05
        ax.text(
            x_center,
            y_pos,
            "Out of\nMemory",
            rotation=0,
            color="red",
            fontsize=10,
            ha="center",
            va="bottom"
        )

    # Optional: set a title or remove if not needed
    # ax.set_title(title, fontsize=11)

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.35)
    fig.savefig(output_filename, bbox_inches="tight")
    plt.close(fig)

# -----------------------------------------------------------------------------
# 5) Create & Save each figure
# -----------------------------------------------------------------------------
plot_latency(df_edge,  "4090speedupEdgeRAG.pdf",   "Speedup vs EdgeRAG")
plot_latency(df_flash, "4090speedupFlashRAG.pdf",  "Speedup vs FlashRAG")
plot_latency(df_pipe,  "4090speedupPipeRAG.pdf",   "Speedup vs PipeRAG")
plot_latency(df_ours,  "4090LatencyOurs.pdf",      "End to end Latency (s)")
