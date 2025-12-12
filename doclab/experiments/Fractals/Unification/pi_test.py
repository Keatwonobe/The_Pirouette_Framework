import numpy as np
from scipy.ndimage import binary_erosion
import matplotlib as plt

# Load your basin mask (black = stable core)
# From your proton basin images
def extract_boundary(mask):
    """Get 1-pixel-wide boundary of stable region"""
    eroded = binary_erosion(mask)
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
                box = boundary_mask[
                    i*box_size : min((i+1)*box_size, ny),
                    j*box_size : min((j+1)*box_size, nx)
                ]
                if np.any(box):
                    count += 1
        counts.append(count)
    
    # Fit log(N) vs log(1/r)
    log_r = np.log(scales)
    log_N = np.log(counts)
    
    # D_f = -slope
    coeffs = np.polyfit(log_r, log_N, 1)
    D_f = -coeffs[0]
    
    return D_f, scales, counts

# Run on your highest-resolution basin mask
# Expected: D_f ≈ 1.3 for Wada boundary
# If proton = fractal: D_f should match measured proton structure function scaling

def measure_effective_pi(core_mask, resolution):
    """
    Measure π by computing Circumference/Diameter at given resolution.
    
    As resolution increases, C/D should approach π asymptotically.
    For a fractal boundary, it never converges—it oscillates around π
    with amplitude decreasing as log(resolution).
    """
    # Find centroid
    y_coords, x_coords = np.where(core_mask)
    x_c = x_coords.mean()
    y_c = y_coords.mean()
    
    # Compute distances from centroid
    boundary_mask = extract_boundary(core_mask)
    by, bx = np.where(boundary_mask)
    
    distances = np.sqrt((bx - x_c)**2 + (by - y_c)**2)
    r_mean = distances.mean()
    
    # Perimeter = number of boundary pixels × pixel size
    delta = 1.0  # Pixel size in arbitrary units
    C_eff = len(bx) * delta
    
    # Diameter
    D_eff = 2 * r_mean * delta
    
    # Effective π
    pi_eff = C_eff / D_eff
    
    return pi_eff, C_eff, D_eff, r_mean

# Run at multiple resolutions by downsampling/upsampling your basin mask
resolutions = [200, 400, 800, 1600, 2000, 4000]
pi_values = []

for res in resolutions:
    # Resample your basin mask to 'res x res'
    # ... (interpolation code)
    pi_eff, C, D, r = measure_effective_pi(resampled_mask, res)
    pi_values.append(pi_eff)
    print(f"Resolution {res}×{res}: π_eff = {pi_eff:.6f}, C={C:.2f}, D={D:.2f}")

# Plot π_eff vs resolution
plt.figure(figsize=(10, 6))
plt.semilogx(resolutions, pi_values, 'o-', label='Measured π_eff')
plt.axhline(np.pi, color='r', linestyle='--', label='True π')
plt.xlabel('Resolution')
plt.ylabel('π_eff')
plt.title('Fractal Pi Convergence')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

def extract_quark_positions(basin_mask):
    """
    Find the three 'lobes' in the triadic fractal structure.
    These should correspond to quark positions.
    """
    from scipy.ndimage import label, center_of_mass
    
    # Threshold to get only the deepest stability pockets
    # (the "holes" in your punctured structure from Figure 4)
    threshold = np.percentile(basin_mask, 5)
    deep_pockets = basin_mask < threshold
    
    # Label connected components
    labeled, n_components = label(deep_pockets)
    
    # Get centers of the 3 largest components
    sizes = [(labeled == i).sum() for i in range(1, n_components+1)]
    largest_3 = np.argsort(sizes)[-3:] + 1
    
    quark_positions = []
    for label_id in largest_3:
        mask_i = (labeled == label_id)
        y_c, x_c = center_of_mass(mask_i)
        quark_positions.append((x_c, y_c))
    
    return np.array(quark_positions)

quarks = extract_quark_positions(basin_mask)

# Compute triangle formed by "quarks"
from scipy.spatial.distance import pdist

distances = pdist(quarks)
print(f"Quark separation distances: {distances}")

# Should form approximate equilateral triangle for SU(3) symmetry
ratio = distances.max() / distances.min()
print(f"Distance ratio (should be ~1 for equilateral): {ratio:.3f}")