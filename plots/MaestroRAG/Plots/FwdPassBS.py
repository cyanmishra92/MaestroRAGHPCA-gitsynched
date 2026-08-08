#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend (headless)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# 1) Global style: pastel colors, black axes/edges, ~10–12 pt fonts
# -----------------------------------------------------------------------------
sns.set_theme(
    style="whitegrid",
    rc={
        "axes.edgecolor": "black",
        "axes.linewidth": 1,
        "xtick.color": "black",
        "ytick.color": "black",
        "font.size": 10,
        "axes.labelsize": 10,
        "legend.fontsize": 10,
        "grid.color": "0.8"
    }
)
palette = sns.color_palette("pastel")

# -----------------------------------------------------------------------------
# 2) Data for 8 cores, varying batch size
# -----------------------------------------------------------------------------
df_8cores = pd.DataFrame({
    "Batch Size": [2, 4, 8, 16, 32],
    "Latency (s)": [0.0546, 0.0989, 0.256, 0.5515, 0.9836]
})

# Plot 1: bar chart
fig, ax = plt.subplots(figsize=(5, 3))
sns.barplot(
    data=df_8cores,
    x="Batch Size",
    y="Latency (s)",
    palette=palette,
    edgecolor="black"
)
ax.set_xlabel("Batch Size", fontsize=14)
ax.set_ylabel("Latency (s)", fontsize=14)
ax.tick_params(axis='both', labelsize=14)

plt.tight_layout()
plt.savefig("forwardpass_8cores.pdf", bbox_inches="tight")
plt.close(fig)

# -----------------------------------------------------------------------------
# 3) Data for Batch Size=16, varying # Cores (min & max latency)
# -----------------------------------------------------------------------------
df_bs16 = pd.DataFrame({
    "# Cores": [1, 2, 4, 8, 10],
    "Min Latency (s)": [0.3624, 0.309, 0.21, 0.11, 0.07],
    "Max Latency (s)": [0.5257, 0.57, 0.34, 0.23, 0.21]
})

# Plot 2: “range plot” (vertical lines from min to max, with markers)
fig, ax = plt.subplots(figsize=(5, 3))

# Choose a pastel color for the lines/markers
color = palette[1]

# Draw a line + markers for each row
for i, row in df_bs16.iterrows():
    x = row["# Cores"]
    mn = row["Min Latency (s)"]
    mx = row["Max Latency (s)"]

    # Vertical line from min to max
    ax.plot([x, x], [mn, mx], color=color, linewidth=2, zorder=2)

    # Markers at min and max
    ax.scatter(x, mn, color=color, edgecolor="black", s=50, zorder=3)
    ax.scatter(x, mx, color=color, edgecolor="black", s=50, zorder=3)

ax.set_xlabel("# Cores", fontsize=14)
ax.set_ylabel("Latency (s)", fontsize=14)
ax.tick_params(axis='both', labelsize=14)

plt.tight_layout()
plt.savefig("forwardpass_bs16_range.pdf", bbox_inches="tight")
plt.close(fig)

