import numpy as np
from scipy.ndimage import binary_erosion, zoom, label, center_of_mass
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist

# --- 1. DATA LOADING/PLACEHOLDER ---
# **YOU MUST REPLACE THIS WITH YOUR ACTUAL MASK LOADING CODE**
# e.g., basin_mask = np.load('your_basin_mask.npy')
# Create a dummy mask for demonstration (a simple circle)
N_initial = 1024
y, x = np.ogrid[-N_initial//2:N_initial//2, -N_initial//2:N_initial//2]
r = N_initial * 0.4
basin_mask = (x*x + y*y < r*r).astype(np.int32)
# Ensure it's a 2D array of integers/booleans
# (Assuming black=0/False stable core, white=1/True unstable region based on comments)
# Let's assume 1 = stable core for the rest of the logic
core_mask_initial = (x*x + y*y < (r*0.9)**2).astype(bool) 
basin_mask_initial = (x*x + y*y < r**2).astype(bool) # This is the full basin image
# For the rest of the script, we'll use a mask where True is the region of interest
# Let's use the core_mask_initial as the input for functions that expect the core.

print(f"Initial mask shape: {basin_mask_initial.shape}")
# ------------------------------------


# Load your basin mask (black = stable core)
# From your proton basin images
def extract_boundary(mask):
    """Get 1-pixel-wide boundary of stable region"""
    eroded = binary_erosion(mask)
    # The boundary is the set of points in the mask that are NOT in the eroded mask
    boundary = mask & ~eroded
    return boundary

def box_counting_dimension(boundary_mask, scales=None):
    """
    Compute fractal dimension via box-counting.
    
    For a true fractal: N(r) ∼ r^(-D_f)
    where N(r) = number of boxes of size r needed to cover the set
    """
    if scales is None:
        scales = 2**np.arange(1, 8)  # [2, 4, 8, 16, 32, 64, 128]
    
    counts = []
    for box_size in scales:
        # Partition into boxes
        ny, nx = boundary_mask.shape
        n_boxes_y = (ny + box_size - 1) // box_size
        n_boxes_x = (nx + box_size - 1) // box_size
        
        count = 0
        for i in range(n_boxes_y):
            for j in range(n_boxes_x):
                # Slice the box
                box = boundary_mask[
                    i*box_size : min((i+1)*box_size, ny),
                    j*box_size : min((j+1)*box_size, nx)
                ]
                # Check if the box is non-empty (contains part of the boundary)
                if np.any(box):
                    count += 1
        counts.append(count)
    
    # Fit log(N) vs log(1/r)
    log_r = np.log(scales)
    log_N = np.log(counts)
    
    # D_f = -slope
    # The fit is N(r) = C * r^(-D_f), so log(N) = log(C) - D_f * log(r)
    coeffs = np.polyfit(log_r, log_N, 1)
    D_f = -coeffs[0]
    
    return D_f, scales, counts

def measure_effective_pi(core_mask, resolution):
    """
    Measure π by computing Circumference/Diameter at given resolution.
    
    As resolution increases, C/D should approach π asymptotically.
    For a fractal boundary, it never converges—it oscillates around π
    with amplitude decreasing as log(resolution).
    """
    # Find centroid
    y_coords, x_coords = np.where(core_mask)
    if len(y_coords) == 0:
        print("Warning: Core mask is empty.")
        return np.nan, 0, 0, 0
        
    x_c = x_coords.mean()
    y_c = y_coords.mean()
    
    # Compute distances from centroid
    boundary_mask = extract_boundary(core_mask)
    by, bx = np.where(boundary_mask)
    
    if len(by) == 0:
        print("Warning: Boundary is empty.")
        return np.nan, 0, 0, 0
        
    distances = np.sqrt((bx - x_c)**2 + (by - y_c)**2)
    r_mean = distances.mean()
    
    # Perimeter = number of boundary pixels × pixel size
    delta = 1.0  # Pixel size in arbitrary units
    C_eff = len(bx) * delta
    
    # Diameter is approximately 2 * mean radius
    D_eff = 2 * r_mean * delta
    
    # Effective π
    pi_eff = C_eff / D_eff
    
    return pi_eff, C_eff, D_eff, r_mean

def extract_quark_positions(basin_mask):
    """
    Find the three 'lobes' in the triadic fractal structure.
    These should correspond to quark positions.
    """
    
    # Find the deepest stability pockets (e.g., the "holes" in a Wada structure)
    # Since we don't have stability values (only a boolean mask), 
    # we'll try to find the 3 largest "holes" if the input is the full basin, 
    # or the 3 largest components if the input is a complex core structure.
    
    # Placeholder: If your mask has actual 'depth' values, use:
    # threshold = np.percentile(basin_mask, 5)
    # deep_pockets = basin_mask < threshold 
    
    # Using the boolean mask, let's look for the 3 largest connected regions.
    labeled, n_components = label(basin_mask)
    
    if n_components < 3:
        print(f"Warning: Only {n_components} components found. Cannot extract 3 quark positions.")
        return np.array([])
        
    # Get component sizes
    sizes = [(labeled == i).sum() for i in range(1, n_components+1)]
    
    # Get labels of the 3 largest components (+1 because label IDs start at 1)
    largest_3_indices = np.argsort(sizes)[-3:]
    largest_3_labels = largest_3_indices + 1
    
    quark_positions = []
    for label_id in largest_3_labels:
        mask_i = (labeled == label_id)
        # Center of mass returns (y, x)
        y_c, x_c = center_of_mass(mask_i)
        quark_positions.append((x_c, y_c)) # Store as (x, y)
    
    return np.array(quark_positions)

# --- 2. EXECUTION BLOCKS ---

## 2.1. Box Counting Fractal Dimension

# Run on your highest-resolution basin mask
boundary_mask_initial = extract_boundary(basin_mask_initial)
D_f, scales, counts = box_counting_dimension(boundary_mask_initial)
print("\n--- Box Counting Dimension ---")
print(f"Calculated Fractal Dimension D_f ≈ **{D_f:.3f}**")
print(f"Scales (r): {scales}")
print(f"Counts (N(r)): {counts}")

# Plotting the Box Counting Fit
log_r = np.log(scales)
log_N = np.log(counts)
coeffs = np.polyfit(log_r, log_N, 1)
fit_line = coeffs[0] * log_r + coeffs[1]

plt.figure(figsize=(8, 6))
plt.plot(log_r, log_N, 'o', label='Measured $\log(N)$')
plt.plot(log_r, fit_line, '-', 
         label=f'Fit: $\log(N) = {-coeffs[0]:.3f}\log(r) + {coeffs[1]:.3f}$')
plt.xlabel('$\log(r)$ (Box Size)')
plt.ylabel('$\log(N(r))$ (Box Count)')
plt.title(f'Box Counting Fit: $D_f \\approx {-coeffs[0]:.3f}$')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

## 2.2. Effective Pi Convergence

resolutions = [100, 200, 400, 800, 1000] # Use a subset since N_initial is 1024
pi_values = []

print("\n--- Effective Pi Measurement ---")
for res in resolutions:
    # **REPLACED WITH RESAMPLING LOGIC**
    # Resample your basin mask to 'res x res'
    zoom_factor = res / basin_mask_initial.shape[0]
    # Use order 0 for nearest-neighbor (good for boolean masks)
    resampled_mask = zoom(basin_mask_initial, zoom_factor, order=0)
    
    # Ensure the mask is exactly the target size (can happen with truncation)
    if resampled_mask.shape[0] != res or resampled_mask.shape[1] != res:
        # Pad or truncate if zoom didn't hit the target exactly due to float precision
        resampled_mask = resampled_mask[:res, :res] 

    pi_eff, C, D, r = measure_effective_pi(resampled_mask, res)
    pi_values.append(pi_eff)
    print(f"Resolution {res}×{res}: π_eff = {pi_eff:.6f}, C={C:.2f}, D={D:.2f}")

# Plot π_eff vs resolution
plt.figure(figsize=(10, 6))
plt.semilogx(resolutions, pi_values, 'o-', label='Measured $\pi_{eff}$')
plt.axhline(np.pi, color='r', linestyle='--', label='True $\pi$')
plt.xlabel('Resolution (log scale)')
plt.ylabel('$\pi_{eff}$ ($C/D$)')
plt.title('Fractal Pi Convergence')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()


## 2.3. Quark Position Extraction

# Note: This part may fail or give nonsensical results with the simple circular mask.
# It is designed for the triadic fractal structure mentioned in your comments.
print("\n--- Quark Position Analysis ---")
quarks = extract_quark_positions(basin_mask_initial)

if len(quarks) == 3:
    print(f"Quark positions (x, y): \n{quarks}")

    # Compute triangle formed by "quarks"
    distances = pdist(quarks)
    print(f"Quark separation distances: {distances}")

    # Should form approximate equilateral triangle for SU(3) symmetry
    ratio = distances.max() / distances.min()
    print(f"Distance ratio (should be ~1 for equilateral): **{ratio:.3f}**")
else:
    print("Could not find 3 distinct 'quark' components. Check the mask structure.")
    # Re-run your helicity scan with finer zoom on the core
# Center on the black region, zoom factor ~10x

# Look for THREE peaks in |∇H| (helicity gradient magnitude)
# These are the quark positions

def find_quark_peaks_in_helicity(helicity_field):
    """
    Quarks = local maxima of helicity gradient magnitude.
    The boundary between stability and instability is sharpest
    where a quark sits.
    """
    grad_y, grad_x = np.gradient(helicity_field)
    grad_mag = np.sqrt(grad_x**2 + grad_y**2)
    
    # Find local maxima
    from scipy.ndimage import maximum_filter
    local_max = (grad_mag == maximum_filter(grad_mag, size=20))
    
    # Get coordinates of top 3 maxima
    peaks_y, peaks_x = np.where(local_max)
    peak_values = grad_mag[peaks_y, peaks_x]
    
    top_3_idx = np.argsort(peak_values)[-3:]
    quark_positions = np.column_stack([peaks_x[top_3_idx], peaks_y[top_3_idx]])
    
    return quark_positions

# Run this on your highest-resolution helicity data