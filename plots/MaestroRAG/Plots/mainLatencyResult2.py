#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')  # Headless backend

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

###############################################################################
# 1) Data Setup
###############################################################################
data_main = [
    # MaestroRAG
    {"Device": "4090", "Implementation": "MaestroRAG",           "Latency": 6.497},
    {"Device": "4080", "Implementation": "MaestroRAG",           "Latency": 3.959},
    {"Device": "Jetson", "Implementation": "MaestroRAG",         "Latency": 28.56},
    # MaestroRAG w/ Cache (only for 4090; ignored elsewhere)
    {"Device": "4090", "Implementation": "MaestroRAG w/ Cache",  "Latency": 0.92},
    {"Device": "4080", "Implementation": "MaestroRAG w/ Cache",  "Latency": None},
    {"Device": "Jetson","Implementation": "MaestroRAG w/ Cache", "Latency": None},
    # EdgeRAG
    {"Device": "4090", "Implementation": "EdgeRAG",        "Latency": 28.4},
    {"Device": "4080", "Implementation": "EdgeRAG",        "Latency": 35.03},
    {"Device": "Jetson","Implementation": "EdgeRAG",       "Latency": 38.62},
    # FlashRAG
    {"Device": "4090", "Implementation": "FlashRAG",       "Latency": 16.39},
    {"Device": "4080", "Implementation": "FlashRAG",       "Latency": 7.76},
    {"Device": "Jetson","Implementation": "FlashRAG",      "Latency": None},
    # PipeRAG
    {"Device": "4090", "Implementation": "PipeRAG",        "Latency": 19.8},
    {"Device": "4080", "Implementation": "PipeRAG",        "Latency": 21.2},
    {"Device": "Jetson","Implementation": "PipeRAG",       "Latency": None},
]
df = pd.DataFrame(data_main)

###############################################################################
# 2) Configuration
###############################################################################
device_order = ["4090", "4080", "Jetson"]
plot_order   = ["MaestroRAG", "EdgeRAG", "FlashRAG", "PipeRAG"]

df["Device"] = pd.Categorical(df["Device"], categories=device_order, ordered=True)

# Baseline latency from "MaestroRAG" for speedup factor
ours_latency = {}
for dev in device_order:
    row = df[(df["Device"] == dev) & (df["Implementation"] == "MaestroRAG")]
    if not row.empty and pd.notna(row.iloc[0]["Latency"]):
        ours_latency[dev] = row.iloc[0]["Latency"]
    else:
        ours_latency[dev] = None

# Single pastel-ish but vibrant colors
policy_colors = {
    "MaestroRAG":     "#69A1FF",  # pastel-ish blue
    "EdgeRAG":  "#8FD694",  # pastel-ish green
    "FlashRAG": "#FF9EE2",  # pastel-ish pink
    "PipeRAG":  "#FFB870",  # pastel-ish orange
}
cache_color = "#CBA7EA"  # pastel purple for the cache portion

###############################################################################
# 3) Plot Setup
###############################################################################
fig, ax = plt.subplots(figsize=(5, 3))
group_width = 0.8
n_bars = len(plot_order)
bar_width = group_width / n_bars
y_limit = 20.0
x_positions = np.arange(len(device_order))

###############################################################################
# 4) Build the Bars (Stacked for 4090 "MaestroRAG") & Labels
###############################################################################
for i, dev in enumerate(device_order):
    for j, policy in enumerate(plot_order):
        x_pos = i - group_width/2 + (j + 0.5)*bar_width

        # Stacked bar only for 4090 "MaestroRAG"
        if dev == "4090" and policy == "MaestroRAG":
            row_ours  = df[(df["Device"] == dev) & (df["Implementation"] == "MaestroRAG")]
            row_cache = df[(df["Device"] == dev) & (df["Implementation"] == "MaestroRAG w/ Cache")]
            if row_ours.empty or pd.isna(row_ours.iloc[0]["Latency"]):
                # N/A case
                ax.bar(x_pos, 0, bar_width, color="white", edgecolor="black", hatch="///")
                ax.text(x_pos, 1.0, "N/A", ha="center", va="center", fontsize=9,
                        rotation=90, color="red")
            else:
                total_latency = row_ours.iloc[0]["Latency"]
                cache_latency = 0.0
                if not row_cache.empty and pd.notna(row_cache.iloc[0]["Latency"]):
                    cache_latency = row_cache.iloc[0]["Latency"]

                remainder     = total_latency - cache_latency
                drawn_total   = min(total_latency, y_limit)
                bottom_height = min(cache_latency, drawn_total)
                top_height    = drawn_total - bottom_height

                # Bottom: cache portion
                ax.bar(x_pos, bottom_height, bar_width, color=cache_color, edgecolor="black")
                # Top: remainder
                if top_height > 0:
                    ax.bar(x_pos, top_height, bar_width, bottom=bottom_height,
                           color=policy_colors["MaestroRAG"], edgecolor="black")
                if total_latency > y_limit:
                    ax.text(x_pos, y_limit - 0.05, "▲", ha="center", va="top",
                            fontsize=12, color="red")
                # Cache portion label
                if bottom_height > 0:
                    ax.text(x_pos + 0.08, bottom_height/2, f"{cache_latency:.2f}s",
                            ha="right", va="center", rotation=0, fontsize=9, color="black")
                # Remainder label (90° rotation)
                if top_height > 0:
                    ax.text(x_pos, bottom_height + top_height/2, f"{remainder:.2f}s",
                            ha="center", va="center", rotation=90, fontsize=9, color="black")
                # Total label above
                ax.text(x_pos + 0.08, drawn_total + 0.1, f"{total_latency:.2f}s",
                        ha="right", va="bottom", rotation=0, fontsize=9, color="black")

        else:
            # Non-stacked bars (including "MaestroRAG" on 4080/Jetson)
            row = df[(df["Device"] == dev) & (df["Implementation"] == policy)]
            if row.empty or pd.isna(row.iloc[0]["Latency"]):
                # N/A case
                ax.bar(x_pos, 0, bar_width, color="white", edgecolor="black", hatch="///")
                ax.text(x_pos, 1.5, "N/A", ha="center", va="center", fontsize=9,
                        rotation=90, color="red")
            else:
                lat_val = row.iloc[0]["Latency"]
                drawn_height = min(lat_val, y_limit)
                ax.bar(x_pos, drawn_height, bar_width, color=policy_colors[policy],
                       edgecolor="black")

                # Show label for all bars
                if policy == "MaestroRAG":
                    # For MaestroRAG, just show the latency (no factor)
                    label = f"{lat_val:.2f}s"
                else:
                    # For non‑MaestroRAG, show latency + factor
                    base = ours_latency[dev] if (ours_latency[dev] and ours_latency[dev] > 0) else 1
                    factor = lat_val / base
                    label = f"{lat_val:.2f}s, x{factor:.2f}"

                # Place label near the middle of the bar, rotated 90°
                ax.text(x_pos, drawn_height/2, label,
                        ha="center", va="center", rotation=90, fontsize=9, color="black")

                # If the bar is truncated
                if lat_val > y_limit:
                    ax.text(x_pos, y_limit - 0.05, "▲", ha="center", va="top",
                            fontsize=12, color="red")

###############################################################################
# 5) Axis, Ticks, Legend
###############################################################################
ax.set_xticks(x_positions)
ax.set_xticklabels(device_order, fontsize=12)
ax.set_ylabel("Latency (s)", fontsize=12)
ax.set_ylim([0, y_limit])
ax.tick_params(axis='both', labelsize=12)

# Legend with one entry per policy
legend_patches = []
for policy in plot_order:
    legend_patches.append(plt.Rectangle((0, 0), 1, 1, facecolor=policy_colors[policy],
                                        edgecolor="black", label=policy))

# Place legend below x-axis in one row
ax.legend(handles=legend_patches, loc="upper center",
          bbox_to_anchor=(0.5, -0.06), ncol=len(legend_patches),
          frameon=False, fontsize=9)

plt.tight_layout()
plt.savefig("MainLatencyResults2.pdf", bbox_inches="tight")
plt.close(fig)
