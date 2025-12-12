import numpy as np
from scipy.ndimage import binary_erosion, zoom, label, center_of_mass, maximum_filter
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist

# --- 1. DATA LOADING/PLACEHOLDER (MUST BE REPLACED) ---
N_initial = 1024
y, x = np.ogrid[-N_initial//2:N_initial//2, -N_initial//2:N_initial//2]
r = N_initial * 0.4

# Placeholder for the simple core mask (Boolean: True=Stable Core)
core_mask_initial = (x*x + y*y < (r*0.9)**2).astype(bool) 
# Placeholder for the full basin mask (Boolean: True=Basin area)
basin_mask_initial = (x*x + y*y < r**2).astype(bool) 
# Placeholder for a Valued Basin Mask (for Method 1) - **REPLACE THIS**
# Simulating a valued field for testing the percentile threshold
valued_basin_mask = np.exp(-((x)**2 + (y)**2) / (2 * (N_initial*0.1)**2)) # Gaussian
# Use the boolean core mask for pi calculation, etc.
basin_mask = valued_basin_mask # Use the valued field for quark extraction
print(f"Initial mask shape: {basin_mask_initial.shape}")

# Placeholder for Helicity Field (for Method 2) - **REPLACE THIS**
# Simulating a field with 3 potential 'peaks' for the gradient test
theta = np.arctan2(y, x)
# Create a tri-lobed pattern
helicity_field_initial = (np.cos(3 * theta) * np.exp(-((x)**2 + (y)**2) / (2 * (N_initial*0.2)**2))) 
# Normalize to have non-trivial gradient
helicity_field_initial = (helicity_field_initial - helicity_field_initial.min()) / (helicity_field_initial.max() - helicity_field_initial.min())
# --------------------------------------------------------

# --- UTILITY FUNCTIONS (Unchanged from your file) ---

def extract_boundary(mask):
    """Get 1-pixel-wide boundary of stable region"""
    eroded = binary_erosion(mask)
    boundary = mask & ~eroded
    return boundary

def box_counting_dimension(boundary_mask, scales=None):
    # ... (function body omitted for brevity, it is working) ...
    if scales is None:
        scales = 2**np.arange(1, 8)
    
    counts = []
    for box_size in scales:
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
    
    log_r = np.log(scales)
    log_N = np.log(counts)
    
    coeffs = np.polyfit(log_r, log_N, 1)
    D_f = -coeffs[0]
    
    return D_f, scales, counts

def measure_effective_pi(core_mask, resolution):
    # ... (function body omitted for brevity, it is working) ...
    y_coords, x_coords = np.where(core_mask)
    if len(y_coords) == 0:
        return np.nan, 0, 0, 0
    x_c, y_c = x_coords.mean(), y_coords.mean()
    boundary_mask = extract_boundary(core_mask)
    by, bx = np.where(boundary_mask)
    if len(by) == 0:
        return np.nan, 0, 0, 0
    distances = np.sqrt((bx - x_c)**2 + (by - y_c)**2)
    r_mean = distances.mean()
    delta = 1.0
    C_eff = len(bx) * delta
    D_eff = 2 * r_mean * delta
    pi_eff = C_eff / D_eff
    return pi_eff, C_eff, D_eff, r_mean

# --- REFINED QUARK EXTRACTION (METHOD 1: Basin Center of Mass) ---

def extract_quark_positions_basin_CoM(valued_basin_mask):
    """
    Find the three 'lobes' corresponding to the deepest stability pockets (quarks)
    by thresholding a VALUED basin mask and finding the center of mass (CoM).
    
    Args:
        valued_basin_mask (np.ndarray): The 2D array of stability values.
    """
    
    # 1. Threshold for deep pockets. Assumes lower values = higher stability/deeper pocket.
    # Use a small percentile (e.g., 5th percentile) to isolate the core regions.
    threshold = np.percentile(valued_basin_mask, 5)
    deep_pockets_mask = valued_basin_mask < threshold 
    
    # 2. Label connected components
    labeled, n_components = label(deep_pockets_mask)
    
    if n_components < 3:
        print(f"Warning: Only {n_components} components found below the 5th percentile. Adjust threshold.")
        return np.array([])
        
    # 3. Get labels of the 3 largest components
    sizes = [(labeled == i).sum() for i in range(1, n_components+1)]
    largest_3_indices = np.argsort(sizes)[-3:]
    largest_3_labels = largest_3_indices + 1
    
    quark_positions = []
    for label_id in largest_3_labels:
        mask_i = (labeled == label_id)
        # Center of mass returns (y, x)
        y_c, x_c = center_of_mass(mask_i)
        quark_positions.append((x_c, y_c)) # Store as (x, y)
    
    return np.array(quark_positions), deep_pockets_mask

# --- NEW QUARK EXTRACTION (METHOD 2: Helicity Gradient Peaks) ---

def find_quark_peaks_in_helicity(helicity_field):
    """
    Quarks are defined as local maxima of the helicity gradient magnitude |∇H|.
    The boundary between stability and instability is sharpest where a quark sits.
    """
    # 1. Compute the gradient magnitude
    grad_y, grad_x = np.gradient(helicity_field)
    grad_mag = np.sqrt(grad_x**2 + grad_y**2)
    
    # 2. Find local maxima (using a filter for smoothness and robustness)
    # The size=20 filter ensures we only pick peaks that are locally dominant
    local_max_mask = (grad_mag == maximum_filter(grad_mag, size=20))
    
    # 3. Get coordinates and values of the peaks
    peaks_y, peaks_x = np.where(local_max_mask)
    peak_values = grad_mag[peaks_y, peaks_x]
    
    # 4. Select the top 3 highest-valued peaks
    if len(peak_values) < 3:
        print(f"Warning: Only {len(peak_values)} local maxima found in the gradient.")
        return np.array([]), grad_mag
        
    top_3_idx = np.argsort(peak_values)[-3:]
    # Quark positions are stored as (x, y)
    quark_positions = np.column_stack([peaks_x[top_3_idx], peaks_y[top_3_idx]])
    
    return quark_positions, grad_mag

# --- 2. EXECUTION BLOCKS ---

# 2.1. Box Counting Fractal Dimension (Running on the simple placeholder mask)
# ... (Box counting code block omitted for brevity) ...

# 2.2. Effective Pi Convergence (Running on the simple placeholder mask)
# ... (Pi convergence code block omitted for brevity) ...

## 2.3. Beefed-Up Quark Position Analysis ⚛️

print("\n--- Method 1: Basin Center of Mass Analysis ---")
quarks_CoM, deep_pockets = extract_quark_positions_basin_CoM(basin_mask)

if len(quarks_CoM) == 3:
    print(f"CoM Quark positions (x, y): \n{quarks_CoM}")

    # Compute triangle formed by "quarks"
    distances = pdist(quarks_CoM)
    print(f"CoM Quark separation distances: {distances}")
    ratio = distances.max() / distances.min()
    print(f"Distance ratio (should be ~1 for equilateral): **{ratio:.3f}**")
    
    # Visualization for Method 1
    plt.figure(figsize=(8, 8))
    plt.imshow(basin_mask, cmap='viridis', origin='lower') 
    plt.colorbar(label='Stability Value (Lower = Deeper Pocket)')
    
    # Plot the 5th percentile mask boundary
    plt.contour(deep_pockets, levels=[0.5], colors='w', linewidths=0.5, label='5th Percentile Contour')

    # Plot the extracted quark centers
    plt.plot(quarks_CoM[:, 0], quarks_CoM[:, 1], 'ro', markersize=10, 
             label='Quark Positions (CoM)') 
    points = np.vstack([quarks_CoM, quarks_CoM[0]]) 
    plt.plot(points[:, 0], points[:, 1], 'r--', linewidth=1, label='Quark Triangle')
    
    plt.title('Method 1: Quark Positions via Deep Basin CoM')
    plt.legend()
    plt.show()
    
else:
    print("Method 1: Could not find 3 distinct 'quark' components in the basin mask.")


print("\n--- Method 2: Helicity Gradient Peak Analysis ---")
quarks_grad, grad_mag = find_quark_peaks_in_helicity(helicity_field_initial)

if len(quarks_grad) == 3:
    print(f"Gradient Peak Quark positions (x, y): \n{quarks_grad}")

    # Compute triangle formed by "quarks"
    distances = pdist(quarks_grad)
    print(f"Gradient Peak separation distances: {distances}")
    ratio = distances.max() / distances.min()
    print(f"Distance ratio (should be ~1 for equilateral): **{ratio:.3f}**")
    
    # Visualization for Method 2
    plt.figure(figsize=(8, 8))
    plt.imshow(grad_mag, cmap='hot', origin='lower') 
    plt.colorbar(label='Helicity Gradient Magnitude $|\\nabla H|$')
    
    # Plot the extracted quark centers
    plt.plot(quarks_grad[:, 0], quarks_grad[:, 1], 'wo', markersize=10, 
             label='Quark Positions (Grad Peak)') 
    
    plt.title('Method 2: Quark Positions via $|\\nabla H|$ Peaks')
    plt.legend()
    plt.show()
    
else:
    print("Method 2: Could not find 3 distinct 'quark' components in the helicity gradient.")