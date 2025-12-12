import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# ==========================================================
#  The Holographic Projector: Manifold Stress Field
# ==========================================================

# --- Configuration ---
LOBES = 3.0             # The particle type (Proton)
TEAR_INTENSITY = 1.5
ROTATION_SPEED = 2.0
DECAY = 1.0             # No decay for this short simulation
GRID_SIZE = 100         # Resolution of the field map
FIELD_RANGE = 5.0       # Radius of the visible field
PATH_STEPS = 200        # Steps to average the knot's stress over

# --- Physics Function to Get Stress ---
def get_orbit_data(lobes, angle_offset, steps):
    """Generates the position and velocity of the two travelers."""
    t = np.linspace(0, 2 * np.pi, steps) # One full period
    r_base = np.power(DECAY, np.arange(steps)) * 5.0 
    theta = ROTATION_SPEED * t
    
    # Position
    x1 = r_base * np.cos(theta)
    y1 = r_base * np.sin(theta)
    x2 = r_base * np.cos(theta + np.pi + angle_offset)
    y2 = r_base * np.sin(theta + np.pi + angle_offset)
    
    # Z-axis (Tear) - not strictly needed for 2D projection but included for completeness
    z_amp = r_base * TEAR_INTENSITY * 0.5
    z1 = z_amp * np.sin(lobes * theta)
    z2 = z_amp * np.sin(lobes * theta + np.pi + angle_offset)
    
    # Velocity (Approximation by difference, scaled by DT for magnitude)
    dt = t[1] - t[0]
    vx1 = np.gradient(x1, dt)
    vy1 = np.gradient(y1, dt)
    vx2 = np.gradient(x2, dt)
    vy2 = np.gradient(y2, dt)
    
    v_mag_sq_1 = vx1**2 + vy1**2
    v_mag_sq_2 = vx2**2 + vy2**2
    
    pos = np.array([[x1, y1, z1], [x2, y2, z2]])
    vel_sq = np.array([v_mag_sq_1, v_mag_sq_2])
    
    return pos, vel_sq

def calculate_stress_field(pos_data, vel_sq_data):
    """Calculates the average Manifold Stress on a 2D grid."""
    
    x_grid = np.linspace(-FIELD_RANGE, FIELD_RANGE, GRID_SIZE)
    y_grid = np.linspace(-FIELD_RANGE, FIELD_RANGE, GRID_SIZE)
    X, Y = np.meshgrid(x_grid, y_grid)
    
    total_stress = np.zeros_like(X)
    
    num_travelers = pos_data.shape[0]
    num_steps = pos_data.shape[2]
    
    for step in range(num_steps):
        instantaneous_stress = np.zeros_like(X)
        for i in range(num_travelers):
            # Traveler position at this step (x_t, y_t)
            xt, yt = pos_data[i, 0, step], pos_data[i, 1, step]
            
            # Squared distance from every grid point to the traveler
            r_sq = (X - xt)**2 + (Y - yt)**2
            r_sq_safe = np.maximum(r_sq, 0.1) # Softening length
            
            # Stress contribution: Stress ~ Energy / Distance^2
            # Energy is proxied by Velocity Magnitude Squared
            energy = vel_sq_data[i, step]
            instantaneous_stress += energy / r_sq_safe
            
        total_stress += instantaneous_stress
        
    # Return the average stress over the entire orbit
    return total_stress / num_steps

def plot_holograms(knot_stress, slip_stress):
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))
    
    vmax = max(knot_stress.max(), slip_stress.max())
    vmin = min(knot_stress.min(), slip_stress.min())
    
    # --- Plot 1: Knot Side (Matter) ---
    im1 = axes[0].pcolormesh(knot_stress, cmap='magma', 
                             norm=colors.LogNorm(vmin=1e-1, vmax=vmax)) # Log scale helps show far-field stress
    
    axes[0].set_title(f"Hologram: Knot Side (Matter)\nPhase Offset: 0.2", fontsize=14)
    axes[0].set_xticks([]); axes[0].set_yticks([])
    fig.colorbar(im1, ax=axes[0], label="Manifold Stress (Log Scale)")

    # --- Plot 2: Slip Side (Shadow) ---
    im2 = axes[1].pcolormesh(slip_stress, cmap='viridis', 
                             norm=colors.LogNorm(vmin=1e-1, vmax=vmax))
                             
    axes[1].set_title(f"Hologram: Slip Side (Shadow)\nPhase Offset: {np.pi:.2f}", fontsize=14)
    axes[1].set_xticks([]); axes[1].set_yticks([])
    fig.colorbar(im2, ax=axes[1], label="Manifold Stress (Log Scale)")
    
    plt.tight_layout()
    plt.savefig('holographic_stress_field.png', dpi=150)

if __name__ == "__main__":
    # 1. Generate Data for Knot Side (Matter)
    KNOT_PHASE = 0.2
    pos_knot, vel_sq_knot = get_orbit_data(LOBES, KNOT_PHASE, PATH_STEPS)
    
    # 2. Generate Data for Slip Side (Shadow)
    SLIP_PHASE = np.pi 
    pos_slip, vel_sq_slip = get_orbit_data(LOBES, SLIP_PHASE, PATH_STEPS)
    
    # 3. Calculate Stress Fields
    print("[*] Calculating Knot Side (Matter) Stress Field...")
    knot_stress_field = calculate_stress_field(pos_knot, vel_sq_knot)
    
    print("[*] Calculating Slip Side (Shadow) Stress Field...")
    slip_stress_field = calculate_stress_field(pos_slip, vel_sq_slip)

    # 4. Plot Results
    plot_holograms(knot_stress_field, slip_stress_field)