import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from scipy.ndimage import maximum_filter

# ----------------------------------------
# PHYSICS CONFIGURATION
# ----------------------------------------
RES = 800
TWIST = 3.8
GAMMA = 0.5
DT = 0.015
STEPS = 1200

# Viewport
M_MIN, M_MAX = -3.0, 3.0
L_MIN, L_MAX = -3.0, 3.0

def get_force_vectorized(m, lam):
    # The Standard Model Soliton Physics
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude) # F^1.5 scaling
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    diff_g = np.abs(angle - 30); diff_g = np.minimum(diff_g, 360-diff_g)
    w_gold = np.exp(-(diff_g/80)**2)
    
    diff_t = np.abs(angle - 150); diff_t = np.minimum(diff_t, 360-diff_t)
    w_teal = np.exp(-(diff_t/80)**2)
    
    diff_r = np.abs(angle - 270); diff_r = np.minimum(diff_r, 360-diff_r)
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_unification_scan():
    print(f"Generating Grand Unification Map ({RES}x{RES})...")
    
    # 1. Grid
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # Metrics
    coherence = np.zeros_like(m)
    prev_pm = np.zeros_like(m)
    prev_plam = np.zeros_like(lam)
    
    # 2. Integration
    for step in range(STEPS):
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        # Coherence (Light) Calc
        v_mag = np.sqrt(pm**2 + plam**2) + 1e-9
        prev_mag = np.sqrt(prev_pm**2 + prev_plam**2) + 1e-9
        dot = (pm * prev_pm + plam * prev_plam) / (v_mag * prev_mag)
        coherence += np.maximum(0, dot)
        
        prev_pm = pm.copy()
        prev_plam = plam.copy()
        
        if step % 200 == 0: print(f"Step {step}/{STEPS}...")

    # 3. Post-Processing
    
    # A. Basin Map (Where did they end up?)
    final_angle = np.degrees(np.arctan2(lam, m)) % 360
    # Classify into 3 Basins (0=Teal, 1=Red, 2=Gold)
    # Teal ~ 150, Red ~ 270, Gold ~ 30
    basin_id = np.zeros_like(final_angle)
    # Simple angular sectors for coloring
    basin_id[np.where((final_angle >= 90) & (final_angle < 210))] = 0 # Teal Sector
    basin_id[np.where((final_angle >= 210) & (final_angle < 330))] = 1 # Red Sector
    basin_id[np.where((final_angle >= 330) | (final_angle < 90))] = 2 # Gold Sector
    
    Basin = basin_id.reshape(RES, RES)
    
    # B. Coherence Map (The Light)
    Light = coherence.reshape(RES, RES)
    Light = Light / np.max(Light) # Normalize 0-1
    
    # 4. PARTICLE FINDER (Local Maxima in Light)
    # We look for bright spots in the coherence map
    print("Locating Stable Particles...")
    neighborhood_size = 20
    local_max = maximum_filter(Light, size=neighborhood_size) == Light
    background_thresh = 0.6 # Only count bright spots
    particles = (Light > background_thresh) & local_max
    
    # Get coordinates of particles
    y_idx, x_idx = np.where(particles)
    
    # List identified particles
    particle_data = []
    print(f"{'ID':<5} | {'Basin':<10} | {'Mass (Radius)':<15} | {'Stability':<10}")
    print("-" * 50)
    
    for i in range(len(x_idx)):
        # Map pixel to physics coord
        px, py = x_idx[i], y_idx[i]
        phys_m = M_MIN + (px/RES)*(M_MAX-M_MIN)
        phys_l = L_MIN + (py/RES)*(L_MAX-L_MIN)
        
        radius = np.sqrt(phys_m**2 + phys_l**2)
        stability = Light[py, px]
        
        # Identify Basin
        b_val = Basin[py, px]
        b_name = "Teal (EM)" if b_val == 0 else "Red (Weak)" if b_val == 1 else "Gold (Strong)"
        
        particle_data.append((phys_m, phys_l, radius, b_name, stability))
        print(f"{i:<5} | {b_name:<10} | {radius:<15.4f} | {stability:.4f}")

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(16, 8), facecolor='black')
    
    # Plot 1: The Composite Overlay
    ax1 = fig.add_subplot(1, 2, 1)
    
    # Create RGB Basin Map
    # Teal=(0,1,1), Red=(1,0,0), Gold=(1,0.8,0)
    rgb = np.zeros((RES, RES, 3))
    
    # Vectorized color assignment
    mask_teal = (Basin == 0)
    mask_red  = (Basin == 1)
    mask_gold = (Basin == 2)
    
    # Base Colors (Dark versions)
    rgb[mask_teal] = [0.0, 0.2, 0.2]
    rgb[mask_red]  = [0.2, 0.0, 0.0]
    rgb[mask_gold] = [0.2, 0.16, 0.0]
    
    # Add Light (Coherence) as additive brightness
    # We boost the color channels by the Light intensity
    # This creates "Glowing" basins
    
    # Enhance contrast of light
    Light_Curve = np.power(Light, 2) 
    
    for c in range(3):
        # Add light to existing color
        rgb[:,:,c] += Light_Curve * 2.0 # Brightness boost
        # Add white-hot core
        rgb[:,:,c] += Light_Curve * 0.5 
    
    rgb = np.clip(rgb, 0, 1)
    
    ax1.imshow(rgb, extent=[M_MIN, M_MAX, L_MIN, L_MAX], origin='lower')
    
    # Mark the detected particles
    for p in particle_data:
        ax1.scatter(p[0], p[1], color='white', marker='+', s=50, linewidth=1)
        # ax1.text(p[0]+0.1, p[1], f"{p[2]:.2f}", color='white', fontsize=8)
    
    ax1.set_title("The Grand Unification: Space, Time, and Matter", color='white', fontsize=14)
    ax1.set_xlabel('Mass Field', color='white')
    ax1.set_ylabel('Coupling Field', color='white')
    ax1.tick_params(colors='white')
    
    # Plot 2: The Generational Slice (Radial Profile)
    ax2 = fig.add_subplot(1, 2, 2, facecolor='black')
    
    # Extract radial profile of Coherence
    # We convert cartesian grid to polar bins
    radii = np.sqrt(M**2 + L**2).flatten()
    lights = Light.flatten()
    
    # Histogram/Binning to get average brightness at radius R
    bins = 100
    r_bins = np.linspace(0, 3.0, bins)
    digitized = np.digitize(radii, r_bins)
    
    radial_profile = []
    for i in range(1, len(r_bins)):
        mask = (digitized == i)
        if np.any(mask):
            # We want the MAX stability at this radius (the peaks), not average
            radial_profile.append(np.max(lights[mask]))
        else:
            radial_profile.append(0)
            
    ax2.plot(r_bins[1:], radial_profile, color='cyan', linewidth=2)
    ax2.fill_between(r_bins[1:], radial_profile, color='cyan', alpha=0.2)
    
    ax2.set_title("Mass Spectrum: Generational Layers", color='white', fontsize=14)
    ax2.set_xlabel("Mass (Radius from Center)", color='white')
    ax2.set_ylabel("Stability (Coherence)", color='white')
    
    # Annotate Peaks (Generations)
    # Simple peak finding on the profile
    # ... (visual annotation)
    
    ax2.grid(color='#333333', alpha=0.5)
    ax2.tick_params(colors='white')

    plt.tight_layout()
    plt.savefig('grand_unification_map.png')
    plt.show()

if __name__ == "__main__":
    run_unification_scan()