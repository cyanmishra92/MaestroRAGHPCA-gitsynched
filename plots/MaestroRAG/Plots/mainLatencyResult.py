#!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Non-interactive (headless) backend

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

###############################################################################
# 1) Data: Main Latency Results
###############################################################################
# Devices: 4090, 4080, Jetson
# Implementations: Ours, Ours w/ Cache, EdgeRAG, FlashRAG, PipeRAG
# Some combos = N/A => we store as None.

data_main = [
    # Ours
    {"Device": "4090", "Implementation": "Ours",           "Latency": 6.497},
    {"Device": "4080", "Implementation": "Ours",           "Latency": 3.959},
    {"Device": "Jetson","Implementation": "Ours",          "Latency": 28.56},

    # Ours w/ Cache
    {"Device": "4090", "Implementation": "Ours w/ Cache",  "Latency": 0.92},
    {"Device": "4080", "Implementation": "Ours w/ Cache",  "Latency": None},  # N/A
    {"Device": "Jetson","Implementation": "Ours w/ Cache", "Latency": None},  # N/A

    # EdgeRAG
    {"Device": "4090", "Implementation": "EdgeRAG",        "Latency": 28.4},
    {"Device": "4080", "Implementation": "EdgeRAG",        "Latency": 35.03},
    {"Device": "Jetson","Implementation": "EdgeRAG",       "Latency": 38.62},

    # FlashRAG
    {"Device": "4090", "Implementation": "FlashRAG",       "Latency": 16.39},
    {"Device": "4080", "Implementation": "FlashRAG",       "Latency": 7.76},
    {"Device": "Jetson","Implementation": "FlashRAG",      "Latency": None},  # N/A

    # PipeRAG
    {"Device": "4090", "Implementation": "PipeRAG",        "Latency": 19.8},
    {"Device": "4080", "Implementation": "PipeRAG",        "Latency": 21.2},
    {"Device": "Jetson","Implementation": "PipeRAG",       "Latency": None},  # N/A
]

df = pd.DataFrame(data_main)

###############################################################################
# 2) Configuration: Order, color families, baseline for improvement factor
###############################################################################
device_order = ["4090", "4080", "Jetson"]
impl_order   = ["Ours", "Ours w/ Cache", "EdgeRAG", "FlashRAG", "PipeRAG"]

# Base colors (pastel) for each device
base_colors = {
    "4090":  "#377eb8",  # pastel-ish blue
    "4080":  "#e41a1c",  # pastel-ish red
    "Jetson":"#4daf4a",  # pastel-ish green
}

def generate_shades(base_hex, n=5):
    """Generate n shades from dark to light based on base_hex."""
    return sns.light_palette(base_hex, n_colors=n, reverse=True, input="hex")

# Build color families
device_shades = {}
for dev in device_order:
    device_shades[dev] = generate_shades(base_colors[dev], n=len(impl_order))

df["Device"] = pd.Categorical(df["Device"], categories=device_order, ordered=True)
df["Implementation"] = pd.Categorical(df["Implementation"], categories=impl_order, ordered=True)

# Compute a dictionary for "Ours" latency on each device => used as baseline
# If Ours is None, factor can't be computed.
ours_latency = {}
for dev in device_order:
    row_ours = df[(df["Device"] == dev) & (df["Implementation"] == "Ours")]
    if not row_ours.empty:
        val = row_ours.iloc[0]["Latency"]
        ours_latency[dev] = val if pd.notna(val) else None
    else:
        ours_latency[dev] = None

###############################################################################
# 3) Plot Setup
###############################################################################
fig, ax = plt.subplots(figsize=(5, 3))

group_width = 0.8
bar_width   = group_width / len(impl_order)
x_limit     = len(device_order) - 1  # last group index
y_limit     = 25.0                   # we clip at 30

# We'll place device groups at x=0,1,2,...
x_positions = np.arange(len(device_order))

###############################################################################
# 4) Build the bars
###############################################################################
for i, dev in enumerate(device_order):
    # Subset for this device
    subset = df[df["Device"] == dev].sort_values("Implementation")
    # For j in [0..4], each sub-bar
    for j, impl in enumerate(impl_order):
        row = subset[subset["Implementation"] == impl]
        if row.empty:
            continue  # No data for that combo
        lat_val = row.iloc[0]["Latency"]

        # X position for this sub-bar
        x_pos = i - group_width/2 + (j + 0.5)*bar_width
        color_shade = device_shades[dev][j]

        # Check for N/A
        if pd.isna(lat_val):
            # Draw zero-height bar with hatch and label "N/A"
            ax.bar(x_pos, 0, bar_width, color="white", edgecolor="black", hatch="///")
            ax.text(x_pos, 0.2, "N/A", ha="center", va="bottom", fontsize=9, color="red")
            continue

        # We have a numeric latency => possibly clipped
        clipped_height = min(lat_val, y_limit - 0.5)  # We leave 0.5 margin for arrow
        bar = ax.bar(
            x_pos,
            clipped_height,
            bar_width,
            color=color_shade,
            edgecolor="black"
        )

        # Compute improvement factor if Ours is known and not zero
        factor_str = ""
        if ours_latency[dev] is not None and ours_latency[dev] > 0:
            improvement = lat_val / ours_latency[dev]
            factor_str = f"(x{improvement:.2f})"

        if lat_val <= y_limit:
            # Entire bar fits
            label_text = f"{lat_val:.2f}"
            if factor_str and impl != "Ours":  # don't show factor for Ours itself
                label_text += f"\n{factor_str}"
            ax.text(x_pos, clipped_height + 0.05, label_text,
                    ha="center", va="bottom", fontsize=9)
        else:
            # Bar is clipped => draw arrow at top
            ax.text(x_pos, clipped_height/2, f"{lat_val:.2f}\n{factor_str}",
                    ha="center", va="center", fontsize=9, color="black")
            # Place arrow symbol at top ~ y_limit
            ax.text(x_pos, y_limit - 0.05, "▲", ha="center", va="top", fontsize=12, color="red")

###############################################################################
# 5) Axis, Ticks, Legend
###############################################################################
ax.set_xticks(x_positions)
ax.set_xticklabels(device_order, fontsize=10)
ax.set_ylabel("Latency (s)", fontsize=10)
ax.set_ylim([0, y_limit])  # clip at 30
ax.tick_params(axis='both', labelsize=10)

# Build a legend for the 5 implementations, using 4090's color family as sample
legend_patches = []
for j, impl in enumerate(impl_order):
    sample_color = device_shades["4090"][j]
    legend_patches.append(plt.Rectangle((0,0),1,1, facecolor=sample_color, edgecolor="black", label=impl))

ax.legend(
    handles=legend_patches,
    title="Implementation",
    loc="upper left",
    #bbox_to_anchor=(0.02, 0.98),
    bbox_to_anchor=(0.45, -0.35),
    frameon=False,
    fontsize=9
)

# Add note explaining color families, arrow, factor
# #!/usr/bin/env python3

import matplotlib
matplotlib.use('Agg')  # Headless backend for CLI environments

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

###############################################################################
# 1) Data Setup
###############################################################################
# We have three devices: [4090, 4080, Jetson].
# Four bars per device: [Ours, EdgeRAG, FlashRAG, PipeRAG].
# Ours on 4090 includes an embedded "cache" portion (0.92s).

data_main = [
    # Ours
    {"Device": "4090", "Implementation": "Ours", "Latency": 6.497},
    {"Device": "4080", "Implementation": "Ours", "Latency": 3.959},
    {"Device": "Jetson","Implementation": "Ours","Latency": 12.923},

    # EdgeRAG
    {"Device": "4090", "Implementation": "EdgeRAG", "Latency": 28.4},
    {"Device": "4080", "Implementation": "EdgeRAG", "Latency": 35.03},
    {"Device": "Jetson","Implementation": "EdgeRAG","Latency": 14.14},

    # FlashRAG
    {"Device": "4090", "Implementation": "FlashRAG", "Latency": 16.39},
    {"Device": "4080", "Implementation": "FlashRAG", "Latency": 7.76},
    {"Device": "Jetson","Implementation": "FlashRAG","Latency": None},  # N/A

    # PipeRAG
    {"Device": "4090", "Implementation": "PipeRAG", "Latency": 19.8},
    {"Device": "4080", "Implementation": "PipeRAG", "Latency": 21.2},
    {"Device": "Jetson","Implementation": "PipeRAG","Latency": None},  # N/A
]

df = pd.DataFrame(data_main)

# We also define the "Ours w/ cache" portion for 4090 specifically:
ours_cache_4090 = 0.92  # bottom portion
# The remainder is 6.497 - 0.92 = 5.577 (top portion).

###############################################################################
# 2) Configuration
###############################################################################
device_order = ["4090", "4080", "Jetson"]
impl_order   = ["Ours", "EdgeRAG", "FlashRAG", "PipeRAG"]

df["Device"] = pd.Categorical(df["Device"], categories=device_order, ordered=True)
df["Implementation"] = pd.Categorical(df["Implementation"], categories=impl_order, ordered=True)

# We'll color by device, from darkest shade (Ours) to lightest shade (PipeRAG).
base_colors = {
    "4090":  "#377eb8",  # pastel-ish blue
    "4080":  "#e41a1c",  # pastel-ish red
    "Jetson":"#4daf4a",  # pastel-ish green
}

def generate_shades(base_hex, n=4):
    """Generate n shades from dark to light for the 4 bars (Ours->PipeRAG)."""
    return sns.light_palette(base_hex, n_colors=n, reverse=True, input="hex")

device_shades = {}
for dev in device_order:
    device_shades[dev] = generate_shades(base_colors[dev], n=len(impl_order))

# We'll also define a distinct color for the "cache portion" of Ours on 4090:
cache_color = "#bc80bd"  # pastel purple, for example

# For speedup, we need to know Ours' latency on each device:
ours_latency = {}
for dev in device_order:
    row = df[(df["Device"] == dev) & (df["Implementation"] == "Ours")]
    if row.empty or row.iloc[0]["Latency"] is None:
        ours_latency[dev] = None
    else:
        ours_latency[dev] = row.iloc[0]["Latency"]

###############################################################################
# 3) Plot Setup
###############################################################################
fig, ax = plt.subplots(figsize=(7, 4))

x_positions = np.arange(len(device_order))  # 0,1,2
group_width = 0.8
bar_width   = group_width / len(impl_order)  # 4 bars per group
y_limit     = 20  # Clip bars at 20

###############################################################################
# 4) Build Bars
###############################################################################
for i, dev in enumerate(device_order):
    subset = df[df["Device"] == dev].sort_values("Implementation")
    x_center = i  # the group is at x=i

    for j, impl in enumerate(impl_order):
        row = subset[subset["Implementation"] == impl]
        if row.empty:
            continue
        lat_val = row.iloc[0]["Latency"]
        x_pos = x_center - group_width/2 + (j + 0.5)*bar_width

        # Determine color
        color_shade = device_shades[dev][j]

        # If Implementation is "Ours" on 4090, do a partial stacked bar for cache portion
        if dev == "4090" and impl == "Ours":
            # total is 6.497
            # bottom portion = 0.92 (cache)
            # top portion    = 5.577
            # Check if the total bar is above y_limit
            total = 6.497
            top_val = total - ours_cache_4090  # 5.577
            # Clip if needed
            clipped_total = min(total, y_limit)
            # bottom portion
            clipped_cache = min(ours_cache_4090, clipped_total)
            bar_cache = ax.bar(
                x_pos, 
                clipped_cache, 
                bar_width,
                color=cache_color,
                edgecolor="black"
            )
            # top portion
            if clipped_total > ours_cache_4090:
                # We have some space for the top portion
                top_portion_height = clipped_total - ours_cache_4090
                ax.bar(
                    x_pos,
                    top_portion_height,
                    bar_width,
                    bottom=ours_cache_4090,
                    color=color_shade,
                    edgecolor="black"
                )
            # If total > y_limit => place arrow
            if total > y_limit:
                ax.text(x_pos, y_limit - 0.05, "▲", ha="center", va="top", fontsize=12, color="red", rotation=0)
                # label inside bar
                ax.text(x_pos, y_limit/2, f"{total:.2f}s", ha="center", va="center", rotation=90, fontsize=9)
            else:
                # entire bar fits
                # label not needed for Ours? If you do want it:
                ax.text(x_pos, total+0.1, f"{total:.2f}s", ha="center", va="bottom", fontsize=9)

            # Also label the cache portion?
            # e.g. inside bottom portion "0.92s"
            if ours_cache_4090 <= clipped_total:
                ax.text(x_pos, ours_cache_4090/2, f"{ours_cache_4090:.2f}", ha="center", va="center", rotation=90, fontsize=9, color="black")

            # top portion label
            if total <= y_limit:
                top_str = f"{top_val:.2f}"
                ax.text(x_pos, ours_cache_4090 + top_val/2, top_str, ha="center", va="center", rotation=90, fontsize=9, color="black")

            continue  # skip the usual single bar logic for Ours on 4090

        # For everything else:
        if pd.isna(lat_val):
            # N/A
            ax.bar(x_pos, 0, bar_width, color="white", edgecolor="black", hatch="///")
            ax.text(x_pos, 0.2, "N/A", ha="center", va="bottom", fontsize=10, color="red", rotation=0)
            continue

        # Possibly truncated bar
        clipped_val = min(lat_val, y_limit)
        ax.bar(x_pos, clipped_val, bar_width, color=color_shade, edgecolor="black")

        # Speedup factor if Ours is known and not zero, and not Ours bar
        factor_str = ""
        if impl != "Ours" and ours_latency[dev] and ours_latency[dev] > 0:
            factor = lat_val / ours_latency[dev]
            factor_str = f" (x{factor:.2f})"

        if lat_val > y_limit:
            # truncated
            # arrow at top
            ax.text(x_pos, y_limit - 0.01, "▲", ha="center", va="top", fontsize=12, color="red")
            # label inside bar
            label_str = f"{lat_val:.2f}s{factor_str}"
            ax.text(x_pos, y_limit/2, label_str, ha="center", va="center", rotation=90, fontsize=10)
        else:
            # entire bar fits
            label_str = f"{lat_val:.2f}s{factor_str}"
            # place label near middle or top? We'll do near middle with rotation=90
            ax.text(x_pos, clipped_val/2, label_str, ha="center", va="center", rotation=90, fontsize=10)

###############################################################################
# 5) Axis, Ticks, Legend
###############################################################################
ax.set_xticks(x_positions)
ax.set_xticklabels(device_order, fontsize=14)
ax.set_ylabel("Latency (s)", fontsize=14)
ax.set_ylim([0, y_limit])
ax.tick_params(axis='both', labelsize=14)

# Single row legend at the bottom
# We'll show 4 patches for the 4 bars: [Ours, EdgeRAG, FlashRAG, PipeRAG],
# plus 1 patch for "Cache portion" maybe, if you want it labeled.

# We'll sample the color family from e.g. 4090:
legend_patches = []
# Ours: partial bar is a combination of cache_color + device_shades["4090"][0],
# but we'll just pick device_shades["4090"][0] as representative
legend_patches.append(plt.Rectangle((0,0),1,1, facecolor=device_shades["4090"][0], edgecolor="black", label="Ours"))
legend_patches.append(plt.Rectangle((0,0),1,1, facecolor=device_shades["4090"][1], edgecolor="black", label="EdgeRAG"))
legend_patches.append(plt.Rectangle((0,0),1,1, facecolor=device_shades["4090"][2], edgecolor="black", label="FlashRAG"))
legend_patches.append(plt.Rectangle((0,0),1,1, facecolor=device_shades["4090"][3], edgecolor="black", label="PipeRAG"))

# If you want to show the cache portion in the legend:
legend_patches.append(plt.Rectangle((0,0),1,1, facecolor=cache_color, edgecolor="black", label="Ours w/ Cache"))

ax.legend(
    handles=legend_patches,
    loc="lower center",
    bbox_to_anchor=(0.5, -0.17),
    ncol=5,  # single row
    frameon=False,
    fontsize=10,
    title=None
)

# Add a text note below x-axis explaining some details
# ax.text(
    # 0.5, -0.38,
    # "Bars exceeding 20s are truncated with a red arrow.\n"
    # "Inside each bar: latency (and speedup vs. Ours if applicable).\n"
    # "Ours on 4090 shows a stacked portion for cache (0.92s) + remainder.",
    # transform=ax.transAxes,
    # ha="center", va="center", fontsize=9
# )

# plt.tight_layout()
# plt.savefig("MainLatencyResults_Custom.pdf", bbox_inches="tight")
# plt.close(fig)


plt.tight_layout()
plt.savefig("MainLatencyResults.pdf", bbox_inches="tight")
plt.close(fig)
