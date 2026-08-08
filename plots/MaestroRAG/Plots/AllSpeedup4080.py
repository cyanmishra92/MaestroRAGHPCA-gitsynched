#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless environments

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

###############################################################################
# 1) MaestroRAG (Latency for multiple DB sizes) on RTX 4080
###############################################################################
data_ours_4080 = [
    {"Batch Size": 2,  "DB Size": "1 mil", "Latency": 2.144},
    {"Batch Size": 2,  "DB Size": "2 mil", "Latency": 2.57},
    {"Batch Size": 2,  "DB Size": "4 mil", "Latency": 3.199},
    {"Batch Size": 2,  "DB Size": "8 mil", "Latency": 4.70},

    {"Batch Size": 4,  "DB Size": "1 mil", "Latency": 2.285},
    {"Batch Size": 4,  "DB Size": "2 mil", "Latency": 2.71},
    {"Batch Size": 4,  "DB Size": "4 mil", "Latency": 3.462},
    {"Batch Size": 4,  "DB Size": "8 mil", "Latency": 4.817},

    {"Batch Size": 8,  "DB Size": "1 mil", "Latency": 2.882},
    {"Batch Size": 8,  "DB Size": "2 mil", "Latency": 3.285},
    {"Batch Size": 8,  "DB Size": "4 mil", "Latency": 3.959},
    {"Batch Size": 8,  "DB Size": "8 mil", "Latency": 5.066},

    {"Batch Size": 16, "DB Size": "1 mil", "Latency": 4.138},
    {"Batch Size": 16, "DB Size": "2 mil", "Latency": 6.39},
    {"Batch Size": 16, "DB Size": "4 mil", "Latency": 7.36},
    {"Batch Size": 16, "DB Size": "8 mil", "Latency": 11.58},
]

df_ours_4080 = pd.DataFrame(data_ours_4080)

###############################################################################
# 2) Merged Speedup Data for EdgeRAG, FlashRAG, PipeRAG (DB Size = 4 mil/4M)
###############################################################################
data_speedup_merged = [
    # EdgeRAG:
    {"Implementation": "EdgeRAG",  "Batch Size": 2,  "Speedup": 4.723351047},
    {"Implementation": "EdgeRAG",  "Batch Size": 4,  "Speedup": 8.965915656},
    {"Implementation": "EdgeRAG",  "Batch Size": 8,  "Speedup": 8.848193988},
    # BS=16 => OOM (no numeric row)

    # FlashRAG:
    {"Implementation": "FlashRAG", "Batch Size": 2,  "Speedup": 3.085339168},
    {"Implementation": "FlashRAG", "Batch Size": 4,  "Speedup": 2.455228192},
    {"Implementation": "FlashRAG", "Batch Size": 8,  "Speedup": 1.960090932},
    # BS=16 => OOM

    # PipeRAG:
    {"Implementation": "PipeRAG",  "Batch Size": 2,  "Speedup": 4.438887152},
    {"Implementation": "PipeRAG",  "Batch Size": 4,  "Speedup": 5.805892548},
    {"Implementation": "PipeRAG",  "Batch Size": 8,  "Speedup": 5.354887598},
    # BS=16 => OOM
]

df_speedup_merged = pd.DataFrame(data_speedup_merged)

###############################################################################
# 3) Enforce categorical ordering
###############################################################################
batch_order = [2, 4, 8, 16]

df_ours_4080["Batch Size"] = pd.Categorical(df_ours_4080["Batch Size"], categories=batch_order, ordered=True)
df_ours_4080["DB Size"] = pd.Categorical(df_ours_4080["DB Size"], categories=["1 mil","2 mil","4 mil","8 mil"], ordered=True)

df_speedup_merged["Batch Size"] = pd.Categorical(df_speedup_merged["Batch Size"], categories=batch_order, ordered=True)
df_speedup_merged["Implementation"] = pd.Categorical(
    df_speedup_merged["Implementation"],
    categories=["EdgeRAG", "FlashRAG", "PipeRAG"],
    ordered=True
)

###############################################################################
# 4) Set up Seaborn style
###############################################################################
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

###############################################################################
# 5) Plot: MaestroRAG Latency (for 4080)
###############################################################################
def plot_ours_latency(df, output_filename):
    fig, ax = plt.subplots(figsize=(5, 3))

    sns.barplot(
        data=df,
        x="Batch Size",
        y="Latency",
        hue="DB Size",
        palette=palette,
        edgecolor="black",
        ax=ax
    )

    ax.set_xlabel("Batch Size", fontsize=10, labelpad=-10)
    ax.set_ylabel("Latency (s)", fontsize=10)
    ax.tick_params(axis='both', labelsize=10)

    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.tick_params(axis='y', which='minor', direction='in', length=2, color='black')

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

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.35)
    fig.savefig(output_filename, bbox_inches="tight")
    plt.close(fig)

###############################################################################
# 6) Plot: Merged Speedup (EdgeRAG, FlashRAG, PipeRAG) with one horizontal OOM label
###############################################################################
def plot_merged_speedup(df, output_filename):
    fig, ax = plt.subplots(figsize=(5, 3))

    sns.barplot(
        data=df,
        x="Batch Size",
        y="Speedup",
        hue="Implementation",
        palette=palette,
        edgecolor="black",
        ax=ax
    )

    ax.set_xlabel("Batch Size", fontsize=10, labelpad=-10)
    ax.set_ylabel("Speedup", fontsize=10)
    ax.tick_params(axis='both', labelsize=10)

    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax.tick_params(axis='y', which='minor', direction='in', length=2, color='black')

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

    # Since BS=16 rows are missing for all implementations (OOM), place a single horizontal "Out of Memory" label centered at x=3.
    x_center = 3  # group index for Batch Size = 16 (0-based indexing: 2->index0, 4->index1, 8->index2, 16->index3)
    y_pos = 0.05   # Adjust as needed for a good vertical position
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

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.35)
    fig.savefig(output_filename, bbox_inches="tight")
    plt.close(fig)

###############################################################################
# 7) Generate and Save Plots
###############################################################################
# 7.1) MaestroRAG Latency Plot for 4080
plot_ours_latency(df_ours_4080, "4080Latency_MaestroRAG.pdf")

# 7.2) Merged Speedup Plot (EdgeRAG, FlashRAG, PipeRAG)
plot_merged_speedup(df_speedup_merged, "4080Speedup_Merged.pdf")
