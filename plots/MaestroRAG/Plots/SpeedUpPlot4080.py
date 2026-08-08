#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for headless environments

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# -----------------------------------------------------------------------------
# 1) Define the data for RTX 4080 latencies
# -----------------------------------------------------------------------------
# Batch Size | 1 mil  | 2 mil  | 4 mil  | 8 mil
#       2    | 2.144 | 2.57   | 3.199  | 4.70
#       4    | 2.285 | 2.71   | 3.462  | 4.817
#       8    | 2.882 | 3.285  | 3.959  | 5.066
#      16    | 4.138 | 6.39   | 7.36   | 11.58

data_4080 = [
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

df_4080 = pd.DataFrame(data_4080)

# -----------------------------------------------------------------------------
# 2) Ensure categorical ordering for Batch Size & DB Size
# -----------------------------------------------------------------------------
batch_order = [2, 4, 8, 16]
db_order = ["1 mil", "2 mil", "4 mil", "8 mil"]

df_4080["Batch Size"] = pd.Categorical(df_4080["Batch Size"], categories=batch_order, ordered=True)
df_4080["DB Size"] = pd.Categorical(df_4080["DB Size"], categories=db_order, ordered=True)

# -----------------------------------------------------------------------------
# 3) Set up Seaborn style (pastel, black outlines, etc.)
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
# 4) Plot the grouped bar chart
# -----------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(5, 3))

sns.barplot(
    data=df_4080,
    x="Batch Size",
    y="Latency",
    hue="DB Size",
    palette=palette,
    edgecolor="black"
)

ax.set_xlabel("Batch Size", fontsize=10, labelpad=-10)
ax.set_ylabel("Latency (s)", fontsize=10)
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

fig.tight_layout()
fig.subplots_adjust(bottom=0.35)
fig.savefig("4080Latency.pdf", bbox_inches="tight")
plt.close(fig)
