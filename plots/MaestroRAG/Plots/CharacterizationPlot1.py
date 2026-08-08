#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend for headless environments

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------
# Global style: pastel, black edges, ~10–12 pt fonts
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
        "legend.fontsize": 12,
        "grid.color": "0.8"
    }
)
palette = sns.color_palette("pastel")

# -----------------------------------------------------------------------------
# 1) 2 mil, Flat, BS=8, Top_k=5
#    # Cores vs. Latency (s)
# -----------------------------------------------------------------------------
df_cores = pd.DataFrame({
    "# Cores": [1, 2, 4, 8, 16],
    "Latency(s)": [8.77, 5.84, 4.935, 4.12, 3.72]
})

fig, ax = plt.subplots(figsize=(5, 3))
sns.barplot(
    data=df_cores,
    x="# Cores",
    y="Latency(s)",
    palette=palette,
    edgecolor="black"
)
ax.set_xlabel("# Cores", fontsize=14)
ax.set_ylabel("Latency (s)", fontsize=14)
ax.tick_params(axis='both', labelsize=14)

plt.tight_layout()
plt.savefig("latency_cores.pdf", bbox_inches="tight")
plt.close(fig)

# -----------------------------------------------------------------------------
# 2) 16 Cores, Flat, BS=8, Top_k=5
#    DB Size (M) vs. Latency (s)
# -----------------------------------------------------------------------------
df_dbsize = pd.DataFrame({
    "DB Size (M)": [1, 2, 4, 8],
    "Latency(s)": [2.11, 3.72, 7.449, 12.069]
})

fig, ax = plt.subplots(figsize=(5, 3))
sns.barplot(
    data=df_dbsize,
    x="DB Size (M)",
    y="Latency(s)",
    palette=palette,
    edgecolor="black"
)
ax.set_xlabel("DB Size (M)", fontsize=14)
ax.set_ylabel("Latency (s)", fontsize=14)
ax.tick_params(axis='both', labelsize=14)

plt.tight_layout()
plt.savefig("latency_dbsize.pdf", bbox_inches="tight")
plt.close(fig)

# -----------------------------------------------------------------------------
# 3) 4 Cores, Flat, 2 Million, Top_k=5
#    Batch Size vs. (Index Fetch + Similarity Search), stacked
# -----------------------------------------------------------------------------
df_batch = pd.DataFrame({
    "Batch Size": [2, 4, 8, 16, 32],
    "Index Fetch (s)": [3.36, 3.36, 3.36, 3.36, 3.36],
    "Similarity Search (s)": [4.408, 0.7539, 1.79, 3.81, 224.58]
})

fig, ax = plt.subplots(figsize=(5, 3))
stack_data = df_batch.set_index("Batch Size")[["Index Fetch (s)", "Similarity Search (s)"]]

stack_data.plot(
    kind="bar",
    stacked=True,
    ax=ax,
    edgecolor="black",
    color=palette
)
ax.set_xlabel("Batch Size", fontsize=14)
ax.set_ylabel("Time (s)", fontsize=14)
ax.tick_params(axis='both', labelsize=14)

# Place legend horizontally below x-axis, remove legend title
handles, labels = ax.get_legend_handles_labels()
ax.legend(
    handles,
    labels,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.4),
    ncol=len(labels),
    frameon=False,
    title=None
)

plt.tight_layout()
# Make room for the legend
fig.subplots_adjust(bottom=0.3)

plt.savefig("batchsize_stacked.pdf", bbox_inches="tight")
plt.close(fig)

