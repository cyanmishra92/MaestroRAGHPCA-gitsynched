import matplotlib
# Use the Agg backend for non-interactive (headless) environments
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

# Set default font size to 10
plt.rcParams.update({'font.size': 10})

# Data for only the four stages: Encode, Retrieve, Augment, Generate
stages = ["Encode", "Retrieve", "Augment", "Generate"]
startup =    [0.46,  3.73,  0.0,  0.0]
execution =  [0.258, 4.0079, 0.1,  3.41]
grand_total = 11.9659  # overall total time

# Define base pastel colors for each stage
base_colors = [
    "#80b1d3",  # light bluish
    "#b3de69",  # light green
    "#bebada",  # light purple
    "#fdb462",  # light orange
]

# Function to darken a hex color (used for the Execution portion)
def darken_color(hex_color, factor=1.3):
    import colorsys
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = max(0, min(1, l / factor))
    r_d, g_d, b_d = colorsys.hls_to_rgb(h, l, s)
    return "#{:02x}{:02x}{:02x}".format(int(r_d*255), int(g_d*255), int(b_d*255))

# Create figure (5 x 3 inches)
fig, ax = plt.subplots(figsize=(5, 3))
x = np.arange(len(stages))
width = 0.5

# For the legend, we create custom handles.
legend_handles = []

# Plot each stage's bars
for i, stage in enumerate(stages):
    color_start = base_colors[i]
    color_exec = darken_color(color_start, factor=1.3)
    
    # Plot startup bar (bottom part)
    ax.bar(x[i], startup[i], color=color_start, edgecolor=None, width=width)
    # Plot execution bar (stacked on top) with label for legend
    ax.bar(x[i], execution[i], bottom=startup[i], color=color_exec, edgecolor=None, width=width, label=stage)
    
    # Draw an outline around the entire bar
    total = startup[i] + execution[i]
    rect = plt.Rectangle((x[i]-width/2, 0), width, total,
                         fill=False, edgecolor="black", linewidth=1)
    ax.add_patch(rect)
    
    # Compute percentage of total time and add a scatter marker and percentage annotation
    percent = (total / grand_total) * 100
    marker_y = total + 0.05
    ax.scatter(x[i], marker_y, color="black", zorder=5)
    ax.text(x[i], marker_y + 0.02, f"{percent:.1f}%", ha="center", va="bottom")
    
    # Build a custom legend handle for this stage using the base (startup) color
    legend_handles.append(Patch(facecolor=color_start, edgecolor='black', label=stage))

# Place the legend inside the plot area, top right, with 2 columns
ax.legend(handles=legend_handles, loc="upper right", bbox_to_anchor=(0.98, 0.98), ncol=2)

# Set x-axis and y-axis labels and ticks
ax.set_xticks(x)
ax.set_xticklabels(stages)
ax.set_ylabel("Time (s)")
ax.set_xlabel("Stages")

# Option to reposition the x-axis label: change 'xlabel_y' to move the label vertically.
xlabel_y = 0.15  # Adjust this value as needed (axis coordinates: 0=bottom, 1=top)
ax.xaxis.set_label_coords(0.5, xlabel_y)

# Add grid lines on the y-axis
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig("stacked_graph.pdf", bbox_inches="tight")
