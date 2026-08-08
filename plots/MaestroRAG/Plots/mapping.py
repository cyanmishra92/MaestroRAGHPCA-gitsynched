#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')  # Headless backend

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Patch
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------
# 1) Data preparation (updated for your new table)
# ---------------------------------------------------------------------
data = [
    # 1M
    {"DB Size": "1M", "Method": "MaestroRAG",      "Batch Size": 8, "Encode": 2, "Retrieve": 2},
    {"DB Size": "1M", "Method": "Empirical", "Batch Size": 8, "Encode": 4, "Retrieve": 4},
    # 2M
    {"DB Size": "2M", "Method": "MaestroRAG",      "Batch Size": 4, "Encode": 1, "Retrieve": 4},
    {"DB Size": "2M", "Method": "Empirical", "Batch Size": 4, "Encode": 1, "Retrieve": 4},
    # 4M
    {"DB Size": "4M", "Method": "MaestroRAG",      "Batch Size": 8, "Encode": 2, "Retrieve": 6},
    {"DB Size": "4M", "Method": "Empirical", "Batch Size": 2, "Encode": 2, "Retrieve": 8},
    # 8M
    {"DB Size": "8M", "Method": "MaestroRAG",      "Batch Size": 2, "Encode": 1, "Retrieve": 6},
    {"DB Size": "8M", "Method": "Empirical", "Batch Size": 2, "Encode": 1, "Retrieve": 8},
]
df = pd.DataFrame(data)
df["Total"] = df["Encode"] + df["Retrieve"]

# ---------------------------------------------------------------------
# 2) Parameters and color schemes
# ---------------------------------------------------------------------
# Use cooler pastel colors for "MaestroRAG" and hotter pastel colors for "Empirical".
ours_colors = ["#a6cee3", "#1f78b4"]  # (Encode, Retrieve)
emp_colors  = ["#ffb347", "#ff7f0e"] # (Encode, Retrieve)

db_order = ["1M", "2M", "4M", "8M"]
df["DB Size"] = pd.Categorical(df["DB Size"], categories=db_order, ordered=True)
groups = df["DB Size"].cat.categories.tolist()  # e.g., ["1M", "2M", "4M", "8M"]
x = np.arange(len(groups))  # [0,1,2,3]

width = 0.35

# ---------------------------------------------------------------------
# 3) Plotting
# ---------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5, 3))

for i, group in enumerate(groups):
    df_group = df[df["DB Size"] == group]

    row_ours = df_group[df_group["Method"] == "MaestroRAG"].iloc[0]
    row_emp  = df_group[df_group["Method"] == "Empirical"].iloc[0]

    pos_ours = x[i] - width/2
    pos_emp  = x[i] + width/2

    # --- MaestroRAG (stacked bar) ---
    ax.bar(pos_ours, row_ours["Encode"], width, color=ours_colors[0], edgecolor="black")
    ax.bar(pos_ours, row_ours["Retrieve"], width, bottom=row_ours["Encode"], color=ours_colors[1], edgecolor="black")

    # Inside labels for MaestroRAG
    ax.text(pos_ours, row_ours["Encode"] / 2,
            f"{row_ours['Encode']}", ha="center", va="center", fontsize=9)
    ax.text(pos_ours, row_ours["Encode"] + row_ours["Retrieve"] / 2,
            f"{row_ours['Retrieve']}", ha="center", va="center", fontsize=9)

    # Above bar label in 2 lines: "BS:x" and "TC:y"
    ax.text(
        pos_ours, row_ours["Total"] + 0.2,
        f"BS:{row_ours['Batch Size']}\nTC:{row_ours['Total']}",
        ha="center", va="bottom", fontsize=9
    )

    # --- Empirical (stacked bar) ---
    ax.bar(pos_emp, row_emp["Encode"], width, color=emp_colors[0], edgecolor="black")
    ax.bar(pos_emp, row_emp["Retrieve"], width, bottom=row_emp["Encode"], color=emp_colors[1], edgecolor="black")

    # Inside labels for Empirical
    ax.text(pos_emp, row_emp["Encode"] / 2,
            f"{row_emp['Encode']}", ha="center", va="center", fontsize=9)
    ax.text(pos_emp, row_emp["Encode"] + row_emp["Retrieve"] / 2,
            f"{row_emp['Retrieve']}", ha="center", va="center", fontsize=9)

    # Above bar label in 2 lines: "BS:x" and "TC:y"
    ax.text(
        pos_emp, row_emp["Total"] + 0.2,
        f"BS:{row_emp['Batch Size']}\nTC:{row_emp['Total']}",
        ha="center", va="bottom", fontsize=9
    )

# ---------------------------------------------------------------------
# 4) Final plot formatting
# ---------------------------------------------------------------------
ax.set_xlabel("DB Size", fontsize=10, labelpad=-10)
ax.set_xticks(x)
ax.set_xticklabels(groups, fontsize=10)
ax.set_ylabel("Total Cores Allocated", fontsize=10)

# No title

# We want a 2-row legend:
# Row 1: MaestroRAG:  [Encode patch], [Retrieve patch]
# Row 2: Empirical: [Encode patch], [Retrieve patch]
# We'll do it by carefully ordering the handles with ncol=2.

ours_header = Patch(facecolor='none', edgecolor='none', label="MaestroRAG:")
emp_header  = Patch(facecolor='none', edgecolor='none', label="Empirical:")

legend_elements = [
    ours_header,
    Patch(facecolor=ours_colors[0], edgecolor="black", label="Encode"),
    Patch(facecolor=ours_colors[1], edgecolor="black", label="Retrieve"),
    emp_header,
    Patch(facecolor=emp_colors[0], edgecolor="black", label="Encode"),
    Patch(facecolor=emp_colors[1], edgecolor="black", label="Retrieve"),
]

# We'll do ncol=2 so that:
#   Row1: [ours_header, Encode], [Retrieve, (maybe next?)]
#   Row2: [emp_header, Encode], [Retrieve, etc.]
# The arrangement depends on how Matplotlib lays out the handles, so we might need to tweak.

ax.legend(
    handles=legend_elements,
    loc="upper left",
    bbox_to_anchor=(-0.01, 1.25),
    ncol=2,
    frameon=False,
    fontsize=10
)

# Explanation note under the x-axis
# ax.text(
    # 0.5, -0.15,
    # "Inside each bar: allocated cores (Encode, Retrieve). Above each bar: two-line annotation with BS and TC.",
    # transform=ax.transAxes,
    # fontsize=9,
    # ha="center"
# )

plt.tight_layout()
plt.savefig("cores_allocation_stacked.pdf", bbox_inches="tight")
plt.close(fig)
