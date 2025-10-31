import numpy as np
import matplotlib.pyplot as plt
from numba import jit

# Upgraded JIT function to compute both interior and exterior detail
@jit(nopython=True)
def compute_attractor_lattice_detailed(gamma_vals, ta_vals, max_iters, escape_radius):
    """
    Computes a detailed fractal map, capturing both smoothed exterior
    and structured interior data.
    """
    height, width = len(ta_vals), len(gamma_vals)
    exterior = np.zeros((height, width))
    interior = np.zeros((height, width))
    alpha = 4 * np.pi / 3  # Ki(motion)

    for i in range(height):
        for j in range(width):
            c = gamma_vals[j] + 1j * ta_vals[i]
            z = 0 + 0j
            
            for n in range(max_iters):
                if np.abs(z) > escape_radius:
                    # Exterior smoothing formula
                    exterior[i, j] = n - np.log2(np.log2(np.abs(z))) + 4.0
                    break
                z = alpha * np.sin(z) + c
            else:
                # Point is in the set; store the final |z| for interior coloring
                exterior[i, j] = 0 # Mark as interior
                interior[i, j] = np.abs(z)
                
    return exterior, interior

# --- Parameters for the Visualization ---
resolution = 1200
gamma_range = (2.15, 2.175)
ta_range = (-0.025, 0.025)
max_iterations = 200
escape_val = 10.0

# --- Generate the Data ---
print("Generating the Detailed Prime Attractor Lattice...")
gamma_ax = np.linspace(gamma_range[0], gamma_range[1], resolution)
ta_ax = np.linspace(ta_range[0], ta_range[1], resolution)
exterior_data, interior_data = compute_attractor_lattice_detailed(
    gamma_ax, ta_ax, max_iterations, escape_val
)
print("Generation complete.")

# --- Combine Interior and Exterior for Plotting ---
# Create a mask for the interior points
interior_mask = (exterior_data == 0)

# Normalize the exterior and interior data separately to use the full colormap range
final_image = np.zeros_like(exterior_data)

# Apply exterior coloring (using a colormap like 'magma')
# Filter out zeros to avoid division issues if all points are stable
non_zero_exterior = exterior_data[~interior_mask]
if non_zero_exterior.size > 0:
    final_image[~interior_mask] = (non_zero_exterior - non_zero_exterior.min()) / (non_zero_exterior.max() - non_zero_exterior.min())

# Apply interior coloring (using a different colormap like 'twilight_shifted')
non_zero_interior = interior_data[interior_mask]
if non_zero_interior.size > 0:
    final_image[interior_mask] = (non_zero_interior - non_zero_interior.min()) / (non_zero_interior.max() - non_zero_interior.min())

# Choose colormaps
exterior_cmap = plt.cm.magma
interior_cmap = plt.cm.twilight_shifted

# Create the final colored image by applying the colormaps
# We map the normalized values to RGBA colors
colored_image = np.zeros((resolution, resolution, 4))
colored_image[~interior_mask] = exterior_cmap(final_image[~interior_mask])
colored_image[interior_mask] = interior_cmap(final_image[interior_mask])


# --- Plotting ---
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(colored_image, extent=[gamma_range[0], gamma_range[1], ta_range[0], ta_range[1]], origin='lower')

ax.set_title("Detailed Prime Attractor Lattice\n(Interior Structure and Smoothed Exterior)", fontsize=14)
ax.set_xlabel("Γ (Temporal Complexity)", fontsize=12)
ax.set_ylabel("$T_a$ (Temporal Coherence)", fontsize=12)
plt.savefig("prime_attractor_lattice_detailed.png", dpi=300, bbox_inches='tight')
plt.show()