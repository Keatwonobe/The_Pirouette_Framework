import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

# Load the catalog
with open('basin_catalog.json', 'r') as f:
    catalog = json.load(f)

all_locks = catalog['locks']
params = catalog['survey_parameters']

print("=" * 70)
print("PROTON BASIN ANALYSIS")
print("=" * 70)
print(f"Total Locks: {params['total_locks']}")
print(f"Search Grid: {params['radial_samples']} radii × {params['angular_samples']} angles")
print(f"Fractal Depth: {params['max_fractal_depth']} layers")
print()

# --- ANALYSIS 1: Radial Distribution ---
print("📊 RADIAL DISTRIBUTION:")
radii = [lock['r'] for lock in all_locks]
r_bins = np.linspace(0, max(radii), 20)
hist, edges = np.histogram(radii, bins=r_bins)

for i in range(len(hist)):
    if hist[i] > 0:
        print(f"  R = {edges[i]:.2f} to {edges[i+1]:.2f}: {hist[i]} locks")

# --- ANALYSIS 2: Depth Distribution by Layer ---
print()
print("🔍 FRACTAL DEPTH ANALYSIS:")
layers = {}
for lock in all_locks:
    d = lock['depth']
    if d not in layers:
        layers[d] = []
    layers[d].append(lock)

for depth in sorted(layers.keys()):
    layer_locks = layers[depth]
    avg_r = np.mean([l['r'] for l in layer_locks])
    avg_intensity = np.mean([l['intensity'] for l in layer_locks])
    print(f"  Layer {depth}: {len(layer_locks)} locks, avg R={avg_r:.3f}, avg intensity={avg_intensity:.2e}")

# --- ANALYSIS 3: Quark Mixing Patterns ---
print()
print("⚛️  QUARK MIXING PATTERN DETECTION:")

# Group by search origin to find "mixing zones"
origin_groups = {}
for lock in all_locks:
    sid = lock['search_id']
    if sid not in origin_groups:
        origin_groups[sid] = []
    origin_groups[sid].append(lock)

# Count how many locks each origin produced
lock_counts = [len(locks) for locks in origin_groups.values()]
print(f"  Locks per search point: min={min(lock_counts)}, max={max(lock_counts)}, avg={np.mean(lock_counts):.1f}")

# Find "hot zones" with maximum mixing
hot_zones = sorted(origin_groups.items(), key=lambda x: len(x[1]), reverse=True)[:5]
print()
print("  Top 5 Mixing Zones:")
for idx, (search_id, locks) in enumerate(hot_zones):
    origin = catalog['search_grid'][search_id]
    print(f"    #{idx+1}: R={origin['r']:.2f}, θ={np.degrees(origin['theta']):.0f}° → {len(locks)} fractal layers")

# --- VISUALIZATION ---
fig, axes = plt.subplots(2, 2, figsize=(16, 14))
fig.suptitle('Proton Basin Complete Analysis', fontsize=18, fontweight='bold')

# Plot 1: All locks in M-L plane (colored by depth)
ax1 = axes[0, 0]
depths_array = np.array([lock['depth'] for lock in all_locks])
m_coords = np.array([lock['m'] for lock in all_locks])
l_coords = np.array([lock['l'] for lock in all_locks])

scatter1 = ax1.scatter(m_coords, l_coords, c=depths_array, cmap='plasma', 
                       s=10, alpha=0.6, edgecolors='none')
ax1.set_xlabel('M-axis', fontsize=12)
ax1.set_ylabel('L-axis', fontsize=12)
ax1.set_title(f'All {len(all_locks)} Fractal Locks (Colored by Depth)', fontsize=14)
ax1.grid(True, alpha=0.3)
ax1.set_aspect('equal')
plt.colorbar(scatter1, ax=ax1, label='Fractal Depth Layer')

# Plot 2: Radial density distribution
ax2 = axes[0, 1]
ax2.hist(radii, bins=30, color='cyan', edgecolor='black', alpha=0.7)
ax2.set_xlabel('Radius from Origin', fontsize=12)
ax2.set_ylabel('Number of Locks', fontsize=12)
ax2.set_title('Radial Distribution of Fractal Locks', fontsize=14)
ax2.grid(True, alpha=0.3)

# Plot 3: Intensity vs Radius (colored by depth)
ax3 = axes[1, 0]
intensities = np.array([lock['intensity'] for lock in all_locks])
scatter3 = ax3.scatter(radii, intensities, c=depths_array, cmap='plasma', 
                       s=15, alpha=0.5, edgecolors='none')
ax3.set_xlabel('Radius', fontsize=12)
ax3.set_ylabel('Intensity', fontsize=12)
ax3.set_title('Lock Intensity vs Radius (Colored by Depth)', fontsize=14)
ax3.set_yscale('log')
ax3.grid(True, alpha=0.3)
plt.colorbar(scatter3, ax=ax3, label='Fractal Depth Layer')

# Plot 4: Polar plot of layer 0 locks (surface level)
ax4 = axes[1, 1]
ax4.remove()
ax4 = fig.add_subplot(2, 2, 4, projection='polar')

layer0_locks = [lock for lock in all_locks if lock['depth'] == 0]
theta_l0 = [lock['theta'] for lock in layer0_locks]
r_l0 = [lock['r'] for lock in layer0_locks]
intensity_l0 = [lock['intensity'] for lock in layer0_locks]

scatter4 = ax4.scatter(theta_l0, r_l0, c=intensity_l0, cmap='hot', 
                       s=30, alpha=0.7, edgecolors='black', linewidth=0.5)
ax4.set_title('Layer 0 Locks (Surface) - Polar View', fontsize=14, pad=20)
plt.colorbar(scatter4, ax=ax4, label='Intensity', pad=0.1)

plt.tight_layout()
plt.savefig('basin_analysis.png', dpi=150, bbox_inches='tight')
print()
print("✅ Analysis visualization saved: basin_analysis.png")

# --- CREATE HEATMAP ---
fig2, ax = plt.subplots(figsize=(12, 10))

# Create 2D histogram
H, xedges, yedges = np.histogram2d(m_coords, l_coords, bins=50)
H = H.T  # Transpose for correct orientation

extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
im = ax.imshow(H, extent=extent, origin='lower', cmap='hot', aspect='auto', interpolation='gaussian')

ax.set_xlabel('M-axis', fontsize=12)
ax.set_ylabel('L-axis', fontsize=12)
ax.set_title('Proton Basin Density Heatmap (All Layers)', fontsize=16, fontweight='bold')
plt.colorbar(im, ax=ax, label='Lock Density')

# Add source positions
src_m = [-10.0, 10.0, 0.0]
src_l = [5.0, 5.0, -10.0]
ax.scatter(src_m, src_l, c='cyan', s=200, marker='*', edgecolors='white', 
           linewidth=2, label='Wave Sources', zorder=10)
ax.legend(fontsize=12)

plt.tight_layout()
plt.savefig('basin_heatmap.png', dpi=150, bbox_inches='tight')
print("✅ Heatmap saved: basin_heatmap.png")

print()
print("=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)