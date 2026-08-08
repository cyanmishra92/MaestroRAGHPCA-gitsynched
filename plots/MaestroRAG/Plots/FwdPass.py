#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless environments

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

sns.set_theme(
    style="whitegrid",
    rc={
        "axes.edgecolor": "black",
        "axes.linewidth": 1,
        "xtick.color": "black",
        "ytick.color": "black",
        "font.size": 12,
        "axes.labelsize": 12,
        "legend.fontsize": 12,
        "grid.color": "0.8"
    }
)
palette = sns.color_palette("pastel")

# -----------------------------------------------------------------------------
# Data for Batch Size=16, # Cores vs. Min/Max Latency
# -----------------------------------------------------------------------------
df_bs16 = pd.DataFrame({
    "# Cores": [1, 2, 4, 8, 16],
    "Min Latency (s)": [0.3624, 0.309, 0.21, 0.11, 0.07],
    "Max Latency (s)": [0.5257, 0.57, 0.34, 0.23, 0.21]
})

fig, ax = plt.subplots(figsize=(5, 3))

# We'll create discrete x positions [0, 1, 2, 3, 4] for each row
x_positions = np.arange(len(df_bs16))

color = palette[1]

# Draw a vertical line + markers for each row
for i, row in df_bs16.iterrows():
    mn = row["Min Latency (s)"]
    mx = row["Max Latency (s)"]
    x = x_positions[i]

    # Vertical line from min to max
    ax.plot([x, x], [mn, mx], color=color, linewidth=2, zorder=2)

    # Markers at min and max
    ax.scatter(x, mn, color=color, edgecolor="black", s=50, zorder=3)
    ax.scatter(x, mx, color=color, edgecolor="black", s=50, zorder=3)

# Set the x-axis ticks to be the discrete positions, labeled with # Cores
ax.set_xticks(x_positions)
ax.set_xticklabels(df_bs16["# Cores"], fontsize=14)

ax.set_xlabel("# Cores", fontsize=14)
ax.set_ylabel("Latency (s)", fontsize=14)
ax.tick_params(axis='y', labelsize=14)

plt.tight_layout()
plt.savefig("forwardpass_bs16_range_discrete.pdf", bbox_inches="tight")
plt.close(fig)

