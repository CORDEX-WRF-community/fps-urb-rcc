import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import argparse
import pandas as pd
from collections import Counter
import requests

# LCZ categories
lcz_names = {
    51: "1", 52: "2", 53: "3", 54: "4",
    55: "5", 56: "6", 57: "7", 58: "8",
    59: "9", 60: "10", 61: "11"
}

# Set the height of the urban levels 
dz_u = 5

# Set the height of the urban levels 
nbui_max = 3

#--------------------------------------------------------------------------------------------
# Plot the distribution of building heights per LCZ based on 2D info in URBAPARAM variable 
# in a geo_em file
#--------------------------------------------------------------------------------------------

# Load the WRF input file
url = "http://www.meteo.unican.es/work/josipa/fps_urban_file_urb3/wrfinput_d02"
response = requests.get(url)
response.raise_for_status()

with open("wrfinput_d02", "wb") as f:
    f.write(response.content)
    
ds = xr.open_dataset("wrfinput_d02", engine='netcdf4')

# Extract LU_INDEX and BUILD_HEIGHT
lu_index = ds['LU_INDEX'].values
build_height = ds['BUILD_HEIGHT'].values

# Check shape compatibility
assert lu_index.shape == build_height.shape, "Shape mismatch!"

# Flatten arrays
lu_flat = lu_index.flatten()
bh_flat = build_height.flatten()

# Mask LCZs 51-61 in LU_INDEX values
mask = (lu_flat >= 51) & (lu_flat <= 61)
selected_lu = lu_flat[mask]
selected_bh = bh_flat[mask]

# Prepare figure
fig, axes = plt.subplots(3, 4, figsize=(16, 10), sharex=True, sharey=True)
axes = axes.flatten()

# Store heights by LU_INDEX
height_distributions = {}

# Histogram bins (optional: adjust based on your data)
#bins = np.linspace(0, np.nanmax(selected_bh), 20)
raw_max_height = np.nanmax(selected_bh)
max_height = np.ceil(raw_max_height / dz_u) * dz_u
bins = np.linspace(0, max_height, int(max_height/dz_u)+1)  # n bins = n+1 edges

# Plot distribution of the LCZs
for idx, lu_val in enumerate(range(51, 62)):
    lcz_name = lcz_names.get(lu_val, f"{lu_val}")
    bh_for_lu = selected_bh[selected_lu == lu_val]
    height_distributions[lu_val] = bh_for_lu
    total = len(bh_for_lu)
    total_percentage = round(100 * len(bh_for_lu) / len(lu_flat), 3)

    # Calculate histogram as percentage
    counts, bin_edges = np.histogram(bh_for_lu, bins=bins)
    if counts.sum() > 0:
        percentages = 100 * counts / counts.sum()
    else:
        percentages = np.zeros_like(counts)
        
    # Plot
    axes[idx].bar(bin_edges[:-1], percentages, width=np.diff(bin_edges), align='edge', alpha=0.7)
    axes[idx].set_title(f"LCZ={lcz_name}; N={total} grids ({total_percentage}%)")
    axes[idx].set_ylim(0, 100)

    if idx % 4 == 0:
        axes[idx].set_ylabel("Percent (%)")
    if idx >= 8:
        axes[idx].set_xlabel("Building Height (m)")

# Remove unused subplot if needed
if len(axes) > 11:
    for ax in axes[11:]:
        fig.delaxes(ax)

plt.suptitle("BUILD_HEIGHT distribution per LCZ category", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("build_height_distribution.png", dpi=100, bbox_inches="tight")
plt.show()

#--------------------------------------------------------------------------------------------
# Print out the info on the number of grids per LCZ within the domain
#--------------------------------------------------------------------------------------------

# Prepare table data
table_data = []
total_grids = len(lu_flat)

for lu_val in range(51, 62):
    lcz_name = lcz_names.get(lu_val, f"{lu_val}")
    count = np.sum(selected_lu == lu_val)
    percent = round(100 * count / total_grids, 3)
    table_data.append((lcz_name, count, percent))

# Create DataFrame
df = pd.DataFrame(table_data, columns=["LCZ Category", "Grid Count", "Percentage (%)"])

# Print the table
print(df.to_string(index=False))


#--------------------------------------------------------------------------------------------
# Get info on the building heights according to URBANPARAM variables, nbui_max, and dz_u 
# ready for URBAPARAM_LCZ.TBL
#--------------------------------------------------------------------------------------------

nbins = nbui_max
mask = (bh_flat >= 51) & (lu_flat <= 61)
valid_mask = (~np.isnan(bh_flat)) & (bh_flat != 0.0)
lu_flat = lu_flat[valid_mask]
bh_flat = bh_flat[valid_mask]
bh_rounded = np.round(bh_flat / 5) * 5  # round to nearest 5 meters

out_tbl = []
for code in range(51, 62):
    heights = bh_rounded[lu_flat == code]
    total = len(heights)
    if total == 0:
        continue

    count = Counter(heights)
    top3 = count.most_common(nbui_max)

    # Normalize and get exact percentages
    top3_sum = sum(c for _, c in top3)
    raw_percentages = [(h, c * 100 / top3_sum) for h, c in top3]

    # Round down and keep track of remainders
    rounded = [(h, int(p), p - int(p)) for h, p in raw_percentages]
    current_sum = sum(p for _, p, _ in rounded)

    # Adjust to make sure total = 100%: sort by largest remainder and increment until sum is 100
    remainder_sorted = sorted(rounded, key=lambda x: -x[2])
    i = 0
    while current_sum < 100:
        h, p, r = remainder_sorted[i]
        remainder_sorted[i] = (h, p + 1, r)
        current_sum += 1
        i += 1

    # Sort by height
    final = sorted([(h, p) for h, p, _ in remainder_sorted])

    out_tbl.append(f"BUILDING HEIGHTS: {code - 50}")
    out_tbl.append("#      (sf_urban_physics=2,3)\n")
    out_tbl.append("#     height   Percentage")
    out_tbl.append("#      [m]       [%]")

    for h, p in final:
        out_tbl.append(f"      {h:4.1f}      {p:.0f}.")

    out_tbl.append("END BUILDING HEIGHTS\n")
print("\n".join(out_tbl))

# Save to file
output_filename = "building_heights_table.txt"
with open(output_filename, "w") as f:
    f.write("\n".join(out_tbl))

print(f"Output table saved to {output_filename}")



