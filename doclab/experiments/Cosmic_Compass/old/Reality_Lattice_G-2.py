import numpy as np
import matplotlib.pyplot as plt
from numba import jit

# Using our detailed lattice generator
@jit(nopython=True)
def compute_attractor_lattice_detailed(gamma_vals, ta_vals, max_iters, escape_radius):
    height, width = len(ta_vals), len(gamma_vals)
    potential_field = np.zeros((height, width))
    alpha = 4 * np.pi / 3

    for i in range(height):
        for j in range(width):
            c = gamma_vals[j] + 1j * ta_vals[i]
            z = 0 + 0j
            for n in range(max_iters):
                if np.abs(z) > escape_radius:
                    # Using a simple potential for this test: iteration count
                    potential_field[i, j] = n
                    break
                z = alpha * np.sin(z) + c
            else:
                potential_field[i, j] = max_iters
    return potential_field

# --- 1. Generate a High-Res Lattice Section ---
resolution = 800
# Zoom into the most complex "node" region from our previous explorations
gamma_range = (2, 3)
ta_range = (-0.5, 0.5)
max_iterations = 300

gamma_ax = np.linspace(gamma_range[0], gamma_range[1], resolution)
ta_ax = np.linspace(ta_range[0], ta_range[1], resolution)

print("Generating high-resolution lattice section for the probe...")
lattice_potential = compute_attractor_lattice_detailed(gamma_ax, ta_ax, max_iterations, 10.0)
# Normalize potential for consistent calculations
lattice_potential /= lattice_potential.max()
print("Lattice generation complete.")

# --- 2. The Triaxial Probe Simulation ---
@jit(nopython=True)
def run_triaxial_probe(potential_map, probe_size_pixels):
    """Moves the probe across the map to find the most resonant point."""
    height, width = potential_map.shape
    resonance_map = np.full((height, width), 1.0) # Initialize with max chaos (std dev = 1.0)
    
    # Define probe geometry (equilateral triangle)
    p_height = int(probe_size_pixels * np.sqrt(3)/2)
    
    # Iterate over every possible center point for the probe
    for i in range(p_height, height):
        for j in range(probe_size_pixels // 2, width - probe_size_pixels // 2):
            # Get the three vertices of the probe
            v1 = potential_map[i, j]
            v2 = potential_map[i - p_height, j - probe_size_pixels // 2]
            v3 = potential_map[i - p_height, j + probe_size_pixels // 2]
            
            # Calculate resonance metric (standard deviation)
            potentials = np.array([v1, v2, v3])
            resonance = np.std(potentials)
            resonance_map[i, j] = resonance
            
    return resonance_map

print("Running Triaxial Resonance Probe...")
# Probe size is about 1% of the image width
probe_size = resolution // 100
resonance_data = run_triaxial_probe(lattice_potential, probe_size)
print("Probe simulation complete.")

# --- 3. Find the Most Resonant Point ---
min_val = resonance_data.min()
# Find the index of the absolute minimum standard deviation
resonant_idx = np.unravel_index(np.argmin(resonance_data), resonance_data.shape)
resonant_gamma = gamma_ax[resonant_idx[1]]
resonant_ta = ta_ax[resonant_idx[0]]

# --- 4. Make the Physical Prediction ---
# From Pirouette theory, the electron's anomaly (a_e) can be related to its
# fundamental Gladiator Force (Γ) via the Ki(motion) constant.
# This is analogous to the Schwinger formula a_e = α / 2π
K_motion = 4 * np.pi / 3
predicted_g_minus_2_anomaly = resonant_gamma / (2 * np.pi * K_motion)

# Compare to the experimentally measured value (CODATA 2018)
experimental_anomaly = 0.00115965218076

# --- 5. Visualization ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
fig.suptitle("Predicting Electron g-2 with the Triaxial Resonance Probe", fontsize=18, weight='bold')

# Left plot: The Resonance Map
im = ax1.imshow(resonance_data, extent=[gamma_range[0], gamma_range[1], ta_range[0], ta_range[1]], 
                cmap='magma_r', origin='lower')
ax1.set_title("Resonance Map (Lower is More Stable)")
ax1.set_xlabel("Γ (Temporal Complexity)")
ax1.set_ylabel("$T_a$ (Temporal Coherence)")
fig.colorbar(im, ax=ax1, label="Potential Std. Dev. at Probe")

# Highlight the most resonant point
ax1.scatter(resonant_gamma, resonant_ta, s=200, facecolors='none', edgecolors='cyan', linewidth=2)
ax1.text(resonant_gamma, resonant_ta + 0.005, "Point of Maximum Resonance", 
         color='cyan', ha='center', fontsize=12)

# Right plot: The Prediction
ax2.bar(["Lattice Prediction", "Experiment"], 
        [predicted_g_minus_2_anomaly * 1e10, experimental_anomaly * 1e10],
        color=['#00A1E4', '#FF6B6B'])
ax2.set_title("Result: Predicted vs. Experimental Value")
ax2.set_ylabel("Anomaly value (a_e)  x 10^10")

# Display the numbers
pred_text = f"Γ_res = {resonant_gamma:.7f}\nPredicted a_e = {predicted_g_minus_2_anomaly:.12f}"
exp_text = f"Experimental a_e = {experimental_anomaly:.12f}"
ax2.text(0, predicted_g_minus_2_anomaly * 1e10, pred_text, ha='center', va='bottom', fontsize=11, color='white')
ax2.text(1, experimental_anomaly * 1e10, exp_text, ha='center', va='bottom', fontsize=11, color='white')

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("g-2_prediction_from_lattice.png", dpi=200)
plt.show()