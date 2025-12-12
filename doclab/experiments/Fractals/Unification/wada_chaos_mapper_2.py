import numpy as np
from numba import njit, prange
import matplotlib.pyplot as plt

# --- Use the outputs from your existing script ---
# Assume 'basin' and 'stress' are the output arrays from render_manifold(RES, ZOOM)
# For demonstration, we'll load them as variables here:
# basin = ... (your basin_map)
# stress = ... (your stress_map)

# ==========================================
# 1. IDENTIFY THE BASIN BOUNDARY
# ==========================================

@njit(fastmath=True)
def get_basin_boundary_mask(basin_map):
    """
    Creates a binary mask where a pixel is 1 if it is a boundary pixel 
    (i.e., its value is different from at least one of its neighbors)
    and 0 otherwise.
    """
    H, W = basin_map.shape
    boundary_mask = np.zeros((H, W), dtype=np.int8)
    
    # Iterate over the interior pixels (avoiding boundary checks)
    for y in prange(1, H - 1):
        for x in range(1, W - 1):
            current_basin = basin_map[y, x]
            
            # Check 4 direct neighbors (can expand to 8 for higher accuracy)
            if (current_basin != basin_map[y+1, x] or
                current_basin != basin_map[y-1, x] or
                current_basin != basin_map[y, x+1] or
                current_basin != basin_map[y, x-1]):
                
                boundary_mask[y, x] = 1
                
    return boundary_mask

# ==========================================
# 2. BOX-COUNTING ALGORITHM
# ==========================================

@njit(fastmath=True)
def box_count_data(boundary_mask, max_box_size=1024):
    """
    Performs the box-counting analysis on the boundary mask.
    Returns lists of log(1/s) and log(N(s)).
    """
    H, W = boundary_mask.shape
    
    # Generate box sizes (powers of 2, up to half the image size)
    # Box size s will be a power of 2: 2, 4, 8, 16, ...
    box_sizes = [2**i for i in range(1, int(np.log2(min(H, W) / 2)))]
    
    log_one_over_s = []
    log_N_s = []

    for s in box_sizes:
        # Number of boxes N(s)
        N_s = 0
        
        # Iterate over the grid, stepping by box size 's'
        for y_start in prange(0, H, s):
            for x_start in range(0, W, s):
                
                # Check if this box contains any '1' (a boundary pixel)
                # We do this by checking the sub-array defined by the box
                box_contains_boundary = False
                
                # Iterate within the current box of size s x s
                for y in range(y_start, min(y_start + s, H)):
                    for x in range(x_start, min(x_start + s, W)):
                        if boundary_mask[y, x] == 1:
                            box_contains_boundary = True
                            break # Found a boundary pixel, move to next box
                    if box_contains_boundary:
                        break

                if box_contains_boundary:
                    N_s += 1
        
        # Store the log values for regression
        if N_s > 0:
            log_one_over_s.append(np.log(1.0 / s))
            log_N_s.append(np.log(N_s))
            
    return np.array(log_one_over_s), np.array(log_N_s)

# ==========================================
# 3. CORRELATION DATA PREP (FOR REGION-SPECIFIC ANALYSIS)
# ==========================================

def prepare_correlation_data(basin_map, stress_map):
    """
    Prepares a list of (stress, boundary_complexity) for correlation.
    
    For a simplified start, we'll only correlate the average stress 
    at the boundary points, but a local fractal dimension calculation
    would be more robust (and complex).
    """
    
    # 1. Get the Boundary Mask
    boundary_mask = get_basin_boundary_mask(basin_map)
    
    # 2. Filter Stress values to only include the boundary points
    boundary_stress_values = stress_map[boundary_mask == 1]
    
    # 3. Calculate Overall Fractal Dimension (D_B)
    log_inv_s, log_N_s = box_count_data(boundary_mask)
    
    # Perform a linear regression: log(N) = -D_B * log(s) + C
    # The slope is -D_B
    D_B, intercept = np.polyfit(log_inv_s, log_N_s, 1)

    print(f"[*] Estimated Box-Counting Dimension (D_B): {D_B:.4f}")
    
    return D_B, boundary_stress_values

# ==========================================
# 4. PLOTTING AND REGRESSION (MAIN EXECUTION)
# ==========================================

if __name__ == "__main__":
    # --- Simulate your data loading ---
    # Load your actual basin and stress maps here
    # Example:
    # basin = np.load('basin_map.npy')
    # stress = np.load('stress_map.npy')
    
    # NOTE: You MUST replace the lines below with your actual data
    # (e.g., re-running the render_manifold function from your original file)
    
    # For a placeholder, let's assume your original script ran and you have the data
    # In a real environment, you'd run:
    # from wada_chaos_mapper import render_manifold, RES, ZOOM
    # basin, stress, steps = render_manifold(RES, ZOOM)
    # Since I cannot run your file, I'll use placeholders for now:
    
    # --- Placeholder data creation (replace this) ---
    RES = 512
    ZOOM = 2.0
    basin = np.random.randint(0, 4, (RES, RES), dtype=np.int8) 
    # Create a boundary-like structure for the stress map
    stress = np.abs(np.fft.fftshift(np.fft.fft2(basin))) 
    stress = np.log1p(stress).astype(np.float32) 
    
    # 1. Get D_B and boundary stress values
    D_B, boundary_stress_values = prepare_correlation_data(basin, stress)
    
    # 2. Plot Box-Counting Regression (for D_B verification)
    log_inv_s, log_N_s = box_count_data(get_basin_boundary_mask(basin))
    
    plt.figure(figsize=(8, 6))
    plt.plot(log_inv_s, log_N_s, 'o', label='Box Count Data')
    # Plot the fit line
    plt.plot(log_inv_s, D_B * log_inv_s + (log_N_s[0] - D_B * log_inv_s[0]), 
             'r--', label=f'Fit Line (Slope $\\approx$ {D_B:.4f})')
    plt.xlabel('$\\log(1/s)$')
    plt.ylabel('$\\log(N(s))$')
    plt.title('Box-Counting Regression for Fractal Dimension')
    plt.legend()
    plt.grid(True)
    plt.show()

    # 3. Analyze and Plot the Stress Distribution at the Boundary
    plt.figure(figsize=(8, 6))
    plt.hist(boundary_stress_values, bins=50, density=True, color='purple', alpha=0.7)
    plt.title(f'Stress Distribution at the Basin Boundary (D_B $\\approx$ {D_B:.4f})')
    plt.xlabel('Frustration/Stress Magnitude')
    plt.ylabel('Density')
    plt.grid(axis='y', alpha=0.5)
    plt.show()

    # --- Next Step: Correlation Analysis ---
    print("\n--- Correlation Analysis ---")
    print(f"Overall D_B (Geometric Complexity): {D_B:.4f}")
    print(f"Mean Boundary Stress (Dynamic Complexity): {np.mean(boundary_stress_values):.4f}")
    print(f"Std Dev Boundary Stress: {np.std(boundary_stress_values):.4f}")
    
    # The true test: Is the stress EXPONENTIAL to the dimension?
    # This requires local D_B calculation, which is much harder.
    # For now, we correlate the mean boundary stress with the overall D_B.
    # Future work would be to define a local D_B in small patches and correlate it 
    # with the average stress in that patch.