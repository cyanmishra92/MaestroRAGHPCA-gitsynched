#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')  # Headless backend (no GUI)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

###############################################################################
# 1) Data Setup
###############################################################################
data_main = [
    {"Device": "RTX 4090", "Implementation": "MaestroRAG",     "Throughput": 1.6},
    {"Device": "Jetson",   "Implementation": "MaestroRAG",     "Throughput": 0.432432432},

    {"Device": "RTX 4090", "Implementation": "EdgeRAG",  "Throughput": 0.287640449},
    {"Device": "Jetson",   "Implementation": "EdgeRAG",  "Throughput": 0.064516129},

    {"Device": "RTX 4090", "Implementation": "FlashRAG", "Throughput": 0.683103853},
    {"Device": "Jetson",   "Implementation": "FlashRAG", "Throughput": None},  # Not compatible

    {"Device": "RTX 4090", "Implementation": "PipeRAG",  "Throughput": 1.185185185},
    {"Device": "Jetson",   "Implementation": "PipeRAG",  "Throughput": 0.370091945},
]

df = pd.DataFrame(data_main)

###############################################################################
# 2) Configuration
###############################################################################
device_order = ["RTX 4090", "Jetson"]
impl_order   = ["MaestroRAG", "EdgeRAG", "FlashRAG", "PipeRAG"]

df["Device"] = pd.Categorical(df["Device"], categories=device_order, ordered=True)
df["Implementation"] = pd.Categorical(df["Implementation"], categories=impl_order, ordered=True)

# Define pastel-ish colors for each implementation
impl_colors = {
    "MaestroRAG":     "#69A1FF",  # pastel-ish blue
    "EdgeRAG":  "#8FD694",  # pastel-ish green
    "FlashRAG": "#FF9EE2",  # pastel-ish pink
    "PipeRAG":  "#FFB870",  # pastel-ish orange
}

###############################################################################
# 3) Plot Setup
###############################################################################
fig, ax = plt.subplots(figsize=(5, 3))

x_positions = np.arange(len(device_order))  # [0, 1] for the two devices
group_width = 0.8
n_impls = len(impl_order)
bar_width = group_width / n_impls
y_limit = 2.0  # Adjust as needed

###############################################################################
# 4) Build Grouped Bars (Group by Device)
###############################################################################
for i, dev in enumerate(device_order):
    # Subset for this device
    subset = df[df["Device"] == dev].sort_values("Implementation")

    # We place one group at x=i, with bars for each Implementation side by side
    for j, impl in enumerate(impl_order):
        row = subset[subset["Implementation"] == impl]
        if row.empty:
            # No data found (should not happen if the data is consistent)
            continue

        val = row.iloc[0]["Throughput"]
        # x position for this Implementation’s bar within the device group
        x_pos = i - group_width/2 + (j + 0.5)*bar_width

        # Check for None => "Not compatible"
        if pd.isna(val):
            # Draw a zero-height bar with hatch
            ax.bar(x_pos, 0, bar_width, color="white", edgecolor="black", hatch="///")
            ax.text(x_pos, 0.05, "Not compatible",
                    ha="center", va="bottom", rotation=90, color="red", fontsize=8)
        else:
            # Normal numeric throughput
            ax.bar(x_pos, val, bar_width, color=impl_colors[impl], edgecolor="black")
            # Label the bar
            ax.text(x_pos, val + 0.02, f"{val:.3f}",
                    ha="center", va="bottom", fontsize=9)

###############################################################################
# 5) Axis, Ticks, Legend
###############################################################################
ax.set_xticks(x_positions)
ax.set_xticklabels(device_order, fontsize=10)
ax.set_ylabel("Throughput (Queries/s)", fontsize=10)
ax.set_ylim([0, y_limit])  # Adjust if needed
ax.tick_params(axis='both', labelsize=10)

# Build legend for the 4 implementations
legend_patches = []
for impl in impl_order:
    legend_patches.append(plt.Rectangle((0, 0), 1, 1,
                                        facecolor=impl_colors[impl],
                                        edgecolor="black",
                                        label=impl))

# Place legend below the x-axis in one row
ax.legend(handles=legend_patches, loc="upper center",
          bbox_to_anchor=(0.5, -0.15), ncol=len(impl_order),
          frameon=False, fontsize=9)

plt.tight_layout()
plt.savefig("ThroughputResults.pdf", bbox_inches="tight")
plt.close(fig)

