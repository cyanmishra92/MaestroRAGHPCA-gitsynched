#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Headless backend

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# -----------------------------------------------------------------------------
# 1) Data
# -----------------------------------------------------------------------------
# 4 Cores, Flat, 1 Million, Top_k=5, 15W
# Batch Size | EdgeRAG | MaestroRAG    | Speedup (EdgeRAG/MaestroRAG)
#      2     | 14.14   | 12.923  | 1.09417318
#      4     | 23.44   | 17.87   | 1.311695579
#      8     | 38.62   | 28.56   | 1.352240896
#     16     | 59      | 33.979  | 1.736366579

df = pd.DataFrame({
    "Batch Size": [2, 4, 8, 16],
    "EdgeRAG":    [14.14, 23.44, 38.62, 59],
    "MaestroRAG":       [12.923, 17.87, 28.56, 46.979],
    "Speedup":    [1.09417318, 1.311695579, 1.352240896, 1.255880287]
})

# -----------------------------------------------------------------------------
# 2) Prepare Data for Grouped Bars (Latency)
# -----------------------------------------------------------------------------
df_latency = df.melt(
    id_vars="Batch Size",
    value_vars=["EdgeRAG", "MaestroRAG"],
    var_name="Implementation",
    value_name="Latency"
)

# -----------------------------------------------------------------------------
# 3) Styling: Pastel colors, black outlines, etc.
# -----------------------------------------------------------------------------
sns.set_theme(
    style="whitegrid",
    rc={
        "axes.edgecolor": "black",
        "axes.linewidth": 1,
        "xtick.color": "black",
        "ytick.color": "black",
        "font.size": 11,
        "axes.labelsize": 11,
        "legend.fontsize": 10,
        "grid.color": "0.8"  # Primary grid color
    }
)
palette = sns.color_palette("pastel")

# -----------------------------------------------------------------------------
# 4) Plot: Combined Latency (bars) with Speedup (line) on secondary y-axis
# -----------------------------------------------------------------------------
fig, ax1 = plt.subplots(figsize=(5, 3))

# Primary Y-axis: Grouped Barplot for Latency
sns.barplot(
    data=df_latency,
    x="Batch Size",
    y="Latency",
    hue="Implementation",
    palette=palette,
    edgecolor="black",
    ax=ax1
)

ax1.set_xlabel("Batch Size", fontsize=10, labelpad=-10)
ax1.set_ylabel("Latency (s)", fontsize=10)
ax1.tick_params(axis='both', labelsize=10)

# Minor ticks on primary y-axis
ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax1.tick_params(axis='y', which='minor', direction='in', length=2, color='black')

# Legend for bar groups below x-axis
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(
    handles,
    labels,
    loc="lower center",
    bbox_to_anchor=(0.45, -0.3),
    ncol=len(labels),
    frameon=False,
    title=None
)

# Secondary Y-axis: Speedup as a free-flowing line
ax2 = ax1.twinx()
ax2.set_ylabel("Speedup", fontsize=10)
ax2.tick_params(axis='y', labelsize=10)

# Set minor ticks on secondary y-axis
ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator())
ax2.tick_params(axis='y', which='minor', direction='in', length=2, color='black')

# Set a different grid for the secondary y-axis (e.g., blue dashed lines)
ax2.yaxis.grid(True, which='major', linestyle='--', color='lightcoral', linewidth=0.5)
#ax2.yaxis.grid(True, which='minor', linestyle='--', color='lightblue', linewidth=0.4)

# Plot speedup as a line on ax2.
# Get x positions (Barplot treats Batch Size as categorical; positions: 0,1,2,3)
unique_sizes = sorted(df["Batch Size"].unique())  # [2, 4, 8, 16]
x_positions = np.arange(len(unique_sizes))          # [0, 1, 2, 3]

df_sorted = df.sort_values("Batch Size")
ax2.plot(
    x_positions,
    df_sorted["Speedup"],
    marker="o",
    color="red",
    linestyle="-",
    linewidth=2,
    label="Speedup"
)

# Adjust x-ticks to match categorical positions
ax1.set_xticks(x_positions)
ax1.set_xticklabels(unique_sizes, fontsize=10)

fig.tight_layout()
fig.subplots_adjust(bottom=0.3)
fig.savefig("JetsonThemVsUs.pdf", bbox_inches="tight")
plt.close(fig)
