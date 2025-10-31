import numpy as np
import matplotlib.pyplot as plt
from numba import jit

# Use Numba's Just-In-Time compiler for a massive performance boost
@jit(nopython=True)
def compute_attractor_lattice(gamma_vals, ta_vals, max_iters, escape_radius):
    """
    Computes the fractal stability for each point on the Gamma-Ta plane.
    
    Args:
        gamma_vals (np.array): Array of Gamma values (real part).
        ta_vals (np.array): Array of Ta values (imaginary part).
        max_iters (int): The maximum number of iterations before declaring a point stable.
        escape_radius (float): The radius at which a point is considered to have escaped.

    Returns:
        np.array: A 2D array of iteration counts for each point.
    """
    height, width = len(ta_vals), len(gamma_vals)
    lattice = np.zeros((height, width))
    alpha = 4 * np.pi / 3  # The fundamental Ki(motion) constant

    for i in range(height):
        for j in range(width):
            c = gamma_vals[j] + 1j * ta_vals[i]
            z = 0 + 0j
            
            for n in range(max_iters):
                if np.abs(z) > escape_radius:
                    lattice[i, j] = n
                    break
                z = alpha * np.sin(z) + c
            else:
                lattice[i, j] = max_iters
                
    return lattice

# --- Parameters for the Visualization ---
resolution = 1200
gamma_range = (2.0, 3.0)
ta_range = (-0.5, 0.5)
max_iterations = 150
escape_val = 10.0

# --- Generate the Data ---
print("Generating the Prime Attractor Lattice... (this may take a moment)")
gamma_ax = np.linspace(gamma_range[0], gamma_range[1], resolution)
ta_ax = np.linspace(ta_range[0], ta_range[1], resolution)
lattice_data = compute_attractor_lattice(gamma_ax, ta_ax, max_iterations, escape_val)
print("Generation complete.")

# --- Plotting ---
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(lattice_data, extent=[gamma_range[0], gamma_range[1], ta_range[0], ta_range[1]], 
          cmap='magma', origin='lower')

ax.set_title("Prime Attractor Lattice\n(Spacetime Stability Map derived from $z_{n+1} = K_{motion} \sin(z_n) + c$)", fontsize=14)
ax.set_xlabel("Γ (Temporal Complexity)", fontsize=12)
ax.set_ylabel("$T_a$ (Temporal Coherence)", fontsize=12)
plt.savefig("prime_attractor_lattice.png", dpi=300)
plt.show()