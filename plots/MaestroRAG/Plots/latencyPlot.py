#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for headless environments

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -------------------------- 1) Define the raw latency data --------------------------
data = [
    # Ours
    {"Implementation": "Ours", "Batch Size": 8,  "Database Size": "1 mil", "Latency": 4.29},
    {"Implementation": "Ours", "Batch Size": 8,  "Database Size": "2 mil", "Latency": 5.027},
    {"Implementation": "Ours", "Batch Size": 8,  "Database Size": "4 mil", "Latency": 6.497},
    {"Implementation": "Ours", "Batch Size": 8,  "Database Size": "8 mil", "Latency": 9.86},

    {"Implementation": "Ours", "Batch Size": 16, "Database Size": "1 mil", "Latency": 8.317},
    {"Implementation": "Ours", "Batch Size": 16, "Database Size": "2 mil", "Latency": 9.72},
    {"Implementation": "Ours", "Batch Size": 16, "Database Size": "4 mil", "Latency": 12.97},
    {"Implementation": "Ours", "Batch Size": 16, "Database Size": "8 mil", "Latency": 25.47},

    {"Implementation": "Ours", "Batch Size": 2,  "Database Size": "1 mil", "Latency": 3.47},
    {"Implementation": "Ours", "Batch Size": 2,  "Database Size": "2 mil", "Latency": 3.78},
    {"Implementation": "Ours", "Batch Size": 2,  "Database Size": "4 mil", "Latency": 4.468},
    {"Implementation": "Ours", "Batch Size": 2,  "Database Size": "8 mil", "Latency": 5.946},

    {"Implementation": "Ours", "Batch Size": 4,  "Database Size": "1 mil", "Latency": 3.747},
    {"Implementation": "Ours", "Batch Size": 4,  "Database Size": "2 mil", "Latency": 4.087},
    {"Implementation": "Ours", "Batch Size": 4,  "Database Size": "4 mil", "Latency": 4.879},
    {"Implementation": "Ours", "Batch Size": 4,  "Database Size": "8 mil", "Latency": 6.55},

    # EdgeRAG
    {"Implementation": "EdgeRAG", "Batch Size": 8,  "Database Size": "1 mil", "Latency": 14.58},
    {"Implementation": "EdgeRAG", "Batch Size": 8,  "Database Size": "2 mil", "Latency": 15.26},
    {"Implementation": "EdgeRAG", "Batch Size": 8,  "Database Size": "4 mil", "Latency": 28.4},
    {"Implementation": "EdgeRAG", "Batch Size": 8,  "Database Size": "8 mil", "Latency": 119.12},

    {"Implementation": "EdgeRAG", "Batch Size": 16, "Database Size": "1 mil", "Latency": 29.47},
    {"Implementation": "EdgeRAG", "Batch Size": 16, "Database Size": "2 mil", "Latency": 31.68},
    {"Implementation": "EdgeRAG", "Batch Size": 16, "Database Size": "4 mil", "Latency": 72.87},
    {"Implementation": "EdgeRAG", "Batch Size": 16, "Database Size": "8 mil", "Latency": 156.7},

    {"Implementation": "EdgeRAG", "Batch Size": 2,  "Database Size": "1 mil", "Latency": 4.54},
    {"Implementation": "EdgeRAG", "Batch Size": 2,  "Database Size": "2 mil", "Latency": 4.66},
    {"Implementation": "EdgeRAG", "Batch Size": 2,  "Database Size": "4 mil", "Latency": 16.18},
    {"Implementation": "EdgeRAG", "Batch Size": 2,  "Database Size": "8 mil", "Latency": 57.48},

    {"Implementation": "EdgeRAG", "Batch Size": 4,  "Database Size": "1 mil", "Latency": 9.03},
    {"Implementation": "EdgeRAG", "Batch Size": 4,  "Database Size": "2 mil", "Latency": 9.24},
    {"Implementation": "EdgeRAG", "Batch Size": 4,  "Database Size": "4 mil", "Latency": 20.48},
    {"Implementation": "EdgeRAG", "Batch Size": 4,  "Database Size": "8 mil", "Latency": 65.36},

    # FlashRAG
    {"Implementation": "FlashRAG", "Batch Size": 8,  "Database Size": "1 mil", "Latency": 13.914},
    {"Implementation": "FlashRAG", "Batch Size": 8,  "Database Size": "2 mil", "Latency": 12.96},
    {"Implementation": "FlashRAG", "Batch Size": 8,  "Database Size": "4 mil", "Latency": 16.39},
    {"Implementation": "FlashRAG", "Batch Size": 8,  "Database Size": "8 mil", "Latency": 18.89},

    {"Implementation": "FlashRAG", "Batch Size": 16, "Database Size": "1 mil", "Latency": 18.78},
    {"Implementation": "FlashRAG", "Batch Size": 16, "Database Size": "2 mil", "Latency": 19.21},
    {"Implementation": "FlashRAG", "Batch Size": 16, "Database Size": "4 mil", "Latency": 19.78},
    {"Implementation": "FlashRAG", "Batch Size": 16, "Database Size": "8 mil", "Latency": 25.14},

    {"Implementation": "FlashRAG", "Batch Size": 2,  "Database Size": "1 mil", "Latency": 6.85},
    {"Implementation": "FlashRAG", "Batch Size": 2,  "Database Size": "2 mil", "Latency": 9.08},
    {"Implementation": "FlashRAG", "Batch Size": 2,  "Database Size": "4 mil", "Latency": 11.77},
    {"Implementation": "FlashRAG", "Batch Size": 2,  "Database Size": "8 mil", "Latency": 18.776},

    {"Implementation": "FlashRAG", "Batch Size": 4,  "Database Size": "1 mil", "Latency": 8.91},
    {"Implementation": "FlashRAG", "Batch Size": 4,  "Database Size": "2 mil", "Latency": 10.68},
    {"Implementation": "FlashRAG", "Batch Size": 4,  "Database Size": "4 mil", "Latency": 12.23},
    {"Implementation": "FlashRAG", "Batch Size": 4,  "Database Size": "8 mil", "Latency": 19.06},
]

df = pd.DataFrame(data)

# -------------------------- 2) Enforce ordering & set style --------------------------
# Order batch sizes [2, 4, 8, 16]
df["Batch Size"] = pd.Categorical(df["Batch Size"], categories=[2, 4, 8, 16], ordered=True)
# Order DB sizes [1 mil, 2 mil, 4 mil, 8 mil]
db_order = ["1 mil", "2 mil", "4 mil", "8 mil"]
df["Database Size"] = pd.Categorical(df["Database Size"], categories=db_order, ordered=True)

# Seaborn style with black axes, black outlines
sns.set_theme(
    style="whitegrid",
    rc={
        "axes.edgecolor": "black",
        "axes.linewidth": 1,
        "xtick.color": "black",
        "ytick.color": "black",
        "font.size": 10,          # Base font size
        "axes.labelsize": 10,     # Axis label font size
        "legend.fontsize": 10,    # Legend font size
        "grid.color": "0.8"       # Light gray grid lines
    }
)

palette = sns.color_palette("pastel")

# -------------------------- 3) Latency Plot (3 subplots, single legend) --------------------------
implementations = ["Ours", "EdgeRAG", "FlashRAG"]
fig, axes = plt.subplots(1, 3, figsize=(9, 3), sharey=True)

for i, impl in enumerate(implementations):
    subset = df[df["Implementation"] == impl]
    # Pivot: rows=Batch Size, columns=DB Size, values=Latency
    pivoted = subset.pivot(index="Batch Size", columns="Database Size", values="Latency")

    # Plot bars with black edges, no subplot legend
    pivoted.plot(
        kind="bar",
        ax=axes[i],
        color=palette,
        width=0.7,
        legend=False,
        edgecolor="black"
    )
    # No subplot titles
    axes[i].set_title("")
    axes[i].tick_params(axis='both', labelsize=10)
    axes[i].set_xlabel("Batch Size", fontsize=10)
    if i == 0:
        axes[i].set_ylabel("Latency (s)", fontsize=10)
    else:
        axes[i].set_ylabel("")

# Single legend below the subplots
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(
    handles, labels,
    title="",
    loc="lower center",
    bbox_to_anchor=(0.5, -0.25),  # Adjust as needed for spacing
    ncol=len(labels),
    frameon=False,
    title_fontsize=10
)
# Adjust bottom to make room for legend
fig.tight_layout()
fig.subplots_adjust(bottom=0.3)

fig.savefig("latency_results.pdf", bbox_inches="tight")
plt.close(fig)

# -------------------------- 4) Speedup vs FlashRAG --------------------------
# Speedup = FlashLatency / OursLatency
df_ours = df[df["Implementation"] == "Ours"].rename(columns={"Latency": "OursLatency"})
df_flash = df[df["Implementation"] == "FlashRAG"].rename(columns={"Latency": "FlashLatency"})
merged_flash = pd.merge(df_ours, df_flash, on=["Batch Size", "Database Size"], how="inner")
merged_flash["Speedup"] = merged_flash["FlashLatency"] / merged_flash["OursLatency"]

fig = plt.figure(figsize=(5, 3))
ax = fig.add_subplot(111)
sns.barplot(
    data=merged_flash,
    x="Batch Size",
    y="Speedup",
    hue="Database Size",
    palette=palette,
    edgecolor="black"
)
ax.set_xlabel("Batch Size", fontsize=10)
ax.set_ylabel("Speedup (FlashRAG vs Ours)", fontsize=10)
ax.tick_params(axis='both', labelsize=10)

# Single legend inside, horizontal, below x-axis
handles, labels = ax.get_legend_handles_labels()
legend = ax.legend(
    handles, labels,
    title="",
    loc="lower center",
    bbox_to_anchor=(0.5, -0.4),
    ncol=len(labels),
    frameon=False,
    title_fontsize=10
)

fig.tight_layout()
fig.subplots_adjust(bottom=0.35)
fig.savefig("speedup_vs_flashrag.pdf", bbox_inches="tight")
plt.close(fig)

# -------------------------- 5) Speedup vs EdgeRAG --------------------------
# Speedup = EdgeLatency / OursLatency
df_edge = df[df["Implementation"] == "EdgeRAG"].rename(columns={"Latency": "EdgeLatency"})
merged_edge = pd.merge(df_ours, df_edge, on=["Batch Size", "Database Size"], how="inner")
merged_edge["Speedup"] = merged_edge["EdgeLatency"] / merged_edge["OursLatency"]

fig = plt.figure(figsize=(5, 3))
ax = fig.add_subplot(111)
sns.barplot(
    data=merged_edge,
    x="Batch Size",
    y="Speedup",
    hue="Database Size",
    palette=palette,
    edgecolor="black"
)
ax.set_xlabel("Batch Size", fontsize=10)
ax.set_ylabel("Speedup (EdgeRAG vs Ours)", fontsize=10)
ax.tick_params(axis='both', labelsize=10)

# Single legend inside, horizontal, below x-axis
handles, labels = ax.get_legend_handles_labels()
legend = ax.legend(
    handles, labels,
    title="",
    loc="lower center",
    bbox_to_anchor=(0.5, -0.4),
    ncol=len(labels),
    frameon=False,
    title_fontsize=10
)

fig.tight_layout()
fig.subplots_adjust(bottom=0.35)
fig.savefig("speedup_vs_edgerag.pdf", bbox_inches="tight")
plt.close(fig)

