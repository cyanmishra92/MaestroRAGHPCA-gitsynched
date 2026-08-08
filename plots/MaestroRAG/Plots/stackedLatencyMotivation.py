#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless environments

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
        "font.size": 10,
        "axes.labelsize": 10,
        "legend.fontsize": 10,
        "grid.color": "0.8"
    }
)
palette = sns.color_palette("pastel")

# -----------------------------------------------------------------------------
# Data: 4 Cores, Flat, 2 Million, Top_k=5
# -----------------------------------------------------------------------------
df_batch = pd.DataFrame({
    "Batch Size": [2, 4, 8, 16, 32],
    "Index Fetch (s)": [3.36, 3.36, 3.36, 3.36, 3.36],
    "Similarity Search (s)": [0.6, 0.7539, 1.79, 3.81, 224.58]
})
df_batch["Total Time (s)"] = df_batch["Index Fetch (s)"] + df_batch["Similarity Search (s)"]

# Convert to a format suitable for stacked bar plotting
stack_data = df_batch.set_index("Batch Size")[["Index Fetch (s)", "Similarity Search (s)"]]

# -----------------------------------------------------------------------------
# Plot: stacked columns, linear y-axis, truncated for the largest bar
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5, 3))

stack_data.plot(
    kind="bar",
    stacked=True,
    ax=ax,
    edgecolor="black",
    color=palette,
    width=0.7
)

# Truncate y-axis so the largest bar doesn't dominate
y_limit = 15
ax.set_ylim(0, y_limit)

ax.set_xlabel("Batch Size", fontsize=14)
ax.set_ylabel("Time (s)", fontsize=14)
ax.tick_params(axis='both', labelsize=14)

# Legend (horizontal, below the x-axis, no title)
handles, labels = ax.get_legend_handles_labels()
ax.legend(
    handles,
    labels,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.5),
    ncol=len(labels),
    frameon=False,
    title=None,
    fontsize=12
)

# -----------------------------------------------------------------------------
# Annotate the bar for Batch Size=32 INSIDE the orange region
# -----------------------------------------------------------------------------
row_32 = df_batch[df_batch["Batch Size"] == 32].iloc[0]
index_fetch = row_32["Index Fetch (s)"]              # 3.36
similarity_search = row_32["Similarity Search (s)"]  # 224.58
total_32 = row_32["Total Time (s)"]                  # ~227.94

# The orange (similarity) portion starts at y = index_fetch and extends to y = total_32
# but we are truncating at y_limit. We'll place the text near the middle of the visible portion.
bar_bottom = index_fetch
bar_top = min(total_32, y_limit)  # truncated top
y_pos = bar_bottom + (bar_top - bar_bottom) / 2  # halfway in the visible orange section

annotation_text = f"{total_32:.2f} s"

ax.text(
    4,  # x-position for the 5th bar (Batch Size=32 is at index 4 in 0-based)
    y_pos,
    annotation_text,
    ha="center",
    va="center",
    rotation=90,   # vertical text
    color="black",
    fontsize=12
)

fig.tight_layout()
fig.subplots_adjust(bottom=0.3)  # Make space for legend
plt.savefig("batchsize_stacked_linear_labeled.pdf", bbox_inches="tight")
plt.close(fig)

