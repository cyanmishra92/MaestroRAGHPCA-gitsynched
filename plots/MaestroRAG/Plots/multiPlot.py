import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
import matplotlib.gridspec as gridspec
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd
from matplotlib.cm import get_cmap

# Set up the data
db_sizes = ["1 mil", "2 mil", "4 mil", "8 mil"]
batch_sizes = [2, 4, 8, 16]

# Reorganize data in the proper format
data = {
    'Ours': {
        2: [3.47, 3.78, 4.468, 5.946],
        4: [3.747, 4.087, 4.879, 6.55],
        8: [4.29, 5.027, 6.497, 9.86],
        16: [8.317, 9.72, 12.97, 25.47]
    },
    'EdgeRAG': {
        2: [4.54, 4.66, 16.18, 57.48],
        4: [9.03, 9.24, 20.48, 65.36],
        8: [14.58, 15.26, 28.4, 119.12],
        16: [29.47, 31.68, 72.87, 156.7]
    },
    'FlashRAG': {
        2: [6.85, 9.08, 11.77, 18.776],
        4: [8.91, 10.68, 12.23, 19.06],
        8: [13.914, 12.96, 16.39, 18.89],
        16: [18.78, 19.21, 19.78, 25.14]
    }
}

# Convert to pandas for easier manipulation
rows = []
for impl in data.keys():
    for bs in batch_sizes:
        for idx, dbs in enumerate(db_sizes):
            rows.append({
                'Implementation': impl,
                'Batch Size': bs,
                'Database Size': dbs,
                'Latency (s)': data[impl][bs][idx]
            })

df = pd.DataFrame(rows)

# Define pleasant color palettes for each implementation
colors = {
    'Ours': sns.color_palette("Blues", n_colors=6)[1:5],
    'EdgeRAG': sns.color_palette("Greens", n_colors=6)[1:5],
    'FlashRAG': sns.color_palette("Oranges", n_colors=6)[1:5]
}

# Create two types of visualizations
# 1. Bar plot comparing all implementations by batch size

# Use non-interactive backend to avoid displaying
import matplotlib
matplotlib.use('Agg')

plt.figure(figsize=(15, 10))
plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)

# Setup the plot
for i, impl in enumerate(['Ours', 'EdgeRAG', 'FlashRAG']):
    # Position the implementation groups
    x_positions = np.arange(len(db_sizes)) + (i - 1) * 0.8

    for j, bs in enumerate(batch_sizes):
        # Extract data for this implementation and batch size
        y_values = data[impl][bs]

        # Plot the bar with appropriate color and label
        plt.bar(
            x_positions + j * 0.2,
            y_values,
            width=0.2,
            color=colors[impl][j],
            label=f"{impl} - BS{bs}" if i == 0 else "_nolegend_"
        )

# Configure axes and labels
plt.xticks(np.arange(len(db_sizes)), db_sizes, fontsize=12)
plt.xlabel('Database Size', fontsize=14)
plt.ylabel('Latency (seconds)', fontsize=14)
plt.title('Latency Comparison by Implementation, Batch Size, and Database Size', fontsize=16)

# Add a legend with better organization
handles, labels = plt.gca().get_legend_handles_labels()
by_impl = []
for i in range(0, len(batch_sizes)):
    by_impl.append(handles[i])

leg1 = plt.legend(by_impl, [f"BS{bs}" for bs in batch_sizes],
                 loc='upper left', title='Batch Size', fontsize=12)
plt.gca().add_artist(leg1)

# Add a legend for implementations
impl_patches = [plt.Rectangle((0,0),1,1, color=colors[impl][0]) for impl in ['Ours', 'EdgeRAG', 'FlashRAG']]
plt.legend(impl_patches, ['Ours', 'EdgeRAG', 'FlashRAG'],
           loc='upper right', title='Implementation', fontsize=12)

plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('latency_comparison_bars.pdf', bbox_inches='tight')

# 2. Line plot showing trends across database sizes
plt.figure(figsize=(15, 10))
plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)

markers = ['o', 's', 'D', '^']
line_styles = ['-', '--', '-.']

for i, impl in enumerate(['Ours', 'EdgeRAG', 'FlashRAG']):
    for j, bs in enumerate(batch_sizes):
        plt.plot(
            np.arange(len(db_sizes)),
            data[impl][bs],
            color=colors[impl][j],
            marker=markers[j],
            linestyle=line_styles[i],
            linewidth=2,
            markersize=8,
            label=f"{impl} - BS{bs}"
        )

plt.xticks(np.arange(len(db_sizes)), db_sizes, fontsize=12)
plt.xlabel('Database Size', fontsize=14)
plt.ylabel('Latency (seconds)', fontsize=14)
plt.title('Latency Trends by Implementation and Batch Size', fontsize=16)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=10, ncol=3, loc='upper left')

# Save this plot
plt.savefig('latency_comparison_lines.pdf', bbox_inches='tight')

# 3. Create a heatmap visualization
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
plt.subplots_adjust(wspace=0.05)

impls = ['Ours', 'EdgeRAG', 'FlashRAG']
colormaps = ["Blues", "Greens", "Oranges"]

for i, (impl, ax, cmap) in enumerate(zip(impls, axes, colormaps)):
    # Extract data as a 2D array for this implementation
    data_array = np.array([data[impl][bs] for bs in batch_sizes])

    # Create the heatmap
    im = ax.imshow(data_array, cmap=cmap, aspect='auto')

    # Configure axes
    ax.set_xticks(np.arange(len(db_sizes)))
    ax.set_xticklabels(db_sizes)

    if i == 0:
        ax.set_yticks(np.arange(len(batch_sizes)))
        ax.set_yticklabels([f"BS{bs}" for bs in batch_sizes])
    else:
        ax.set_yticks([])

    # Add title
    ax.set_title(impl, fontsize=14)

    # Add values to cells
    for j in range(len(batch_sizes)):
        for k in range(len(db_sizes)):
            text = ax.text(k, j, f"{data_array[j, k]:.2f}",
                           ha="center", va="center", color="black" if data_array[j, k] < 30 else "white",
                           fontsize=9)

    # Add colorbar
    if i == 2:
        cbar = plt.colorbar(im, ax=axes, orientation='vertical', pad=0.01)
        cbar.set_label('Latency (seconds)', fontsize=12)

# Add common labels
fig.text(0.5, 0.01, 'Database Size', ha='center', fontsize=14)
fig.text(0.08, 0.5, 'Batch Size', va='center', rotation='vertical', fontsize=14)
fig.suptitle('Latency Comparison Heatmap by Implementation', fontsize=16)

plt.savefig('latency_heatmap.pdf', bbox_inches='tight')

# 4. Faceted bar plot for clearer comparison
plt.figure(figsize=(18, 10))
gs = gridspec.GridSpec(2, 2, height_ratios=[1, 1])

# Map batch sizes to subplots
subplot_positions = {
    2: gs[0, 0],
    4: gs[0, 1],
    8: gs[1, 0],
    16: gs[1, 1]
}

for bs in batch_sizes:
    ax = plt.subplot(subplot_positions[bs])

    # Filter data for this batch size
    for i, impl in enumerate(['Ours', 'EdgeRAG', 'FlashRAG']):
        x_positions = np.arange(len(db_sizes)) + (i - 1) * 0.3

        # Plot the bar with appropriate color
        ax.bar(x_positions, data[impl][bs], width=0.3, color=colors[impl][0], label=impl if bs == 2 else "")

    # Configure axes and labels
    ax.set_xticks(np.arange(len(db_sizes)))
    ax.set_xticklabels(db_sizes)
    ax.set_title(f'Batch Size {bs}', fontsize=14)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Add y-label only for leftmost plots
    if bs in [2, 8]:
        ax.set_ylabel('Latency (seconds)', fontsize=12)

    # Add x-label only for bottom plots
    if bs in [8, 16]:
        ax.set_xlabel('Database Size', fontsize=12)

# Add a single legend for the entire figure
handles, labels = ax.get_legend_handles_labels()
plt.figlegend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 0.98), fontsize=12)

plt.suptitle('Latency Comparison by Batch Size', fontsize=16, y=0.99)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('latency_by_batchsize.pdf', bbox_inches='tight')

print("Visualizations saved as PDF files.")
