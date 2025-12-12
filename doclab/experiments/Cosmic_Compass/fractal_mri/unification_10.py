import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ----------------------------------------
# COMPOSITE SCAN CONFIGURATION
# ----------------------------------------
RES = 600            # Resolution (360k Universes) - Balanced for speed/detail
TWIST = 3.8          # The Standard Model Twist
GAMMA = 0.5          # The Critical Higgs Viscosity
DT = 0.015
STEPS = 1200         # Duration

# Viewport
M_MIN, M_MAX = -2.5, 2.5
L_MIN, L_MAX = -2.5, 2.5

# Perturbation for Chaos Check
EPSILON = 1e-6

def get_force_vectorized(m, lam):
    # The Pirouette Physics Engine
    
    # 1. Teal (EM)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak)
    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong)
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude)
    
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
    nw_red, nw_teal, nw_gold = w_red/tot, w_teal/tot, w_gold/tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_correlation_scan():
    print(f"Running Composite Scan (Spin + Chaos)...")
    
    # 1. Initialize Grid
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    # Main Particle
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # Shadow Particle (for Lyapunov)
    m_s = m + EPSILON
    lam_s = lam + EPSILON
    pm_s = np.zeros_like(m)
    plam_s = np.zeros_like(lam)
    
    # Metrics
    prev_ang = np.arctan2(lam, m)
    total_ang = np.zeros_like(m)
    lyap_sum = np.zeros_like(m)
    
    # 2. Integration Loop
    for step in range(STEPS):
        # --- Main Particle ---
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

        # --- Shadow Particle ---
        Fm_s, Flam_s, w_red_s = get_force_vectorized(m_s, lam_s)
        drag_s = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red_s)
        
        pm_s = (pm_s + 0.5 * DT * Fm_s) * drag_s
        plam_s = (plam_s + 0.5 * DT * Flam_s) * drag_s
        m_s += DT * pm_s
        lam_s += DT * plam_s
        
        Fm_s, Flam_s, w_red_s = get_force_vectorized(m_s, lam_s)
        drag_s = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red_s)
        pm_s = (pm_s + 0.5 * DT * Fm_s) * drag_s
        plam_s = (plam_s + 0.5 * DT * Flam_s) * drag_s
        
        # --- Measurements ---
        # 1. Spin (Winding)
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        delta = np.where(delta > np.pi, delta - 2*np.pi, delta)
        delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)
        total_ang += delta
        prev_ang = curr_ang
        
        # 2. Chaos (Lyapunov)
        dist_sq = (m - m_s)**2 + (lam - lam_s)**2 + (pm - pm_s)**2 + (plam - plam_s)**2
        dist = np.sqrt(dist_sq)
        dist = np.maximum(dist, 1e-15)
        
        # Log divergence
        lyap_sum += np.log(dist / EPSILON)
        
        # Rescale shadow to prevent overflow (Benettin renormalization)
        rescale = EPSILON / dist
        m_s = m + (m_s - m) * rescale
        lam_s = lam + (lam_s - lam) * rescale
        pm_s = pm + (pm_s - pm) * rescale
        plam_s = plam + (plam_s - plam) * rescale

        if step % 100 == 0:
            print(f"Correlating... {step}/{STEPS}")

    # 3. Process Data
    # Spin
    spin_raw = np.abs(total_ang) / (2*np.pi)
    spin_map = spin_raw.reshape(RES, RES)
    
    # Chaos
    lyap_exp = lyap_sum / (STEPS * DT)
    lyap_map = lyap_exp.reshape(RES, RES)
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(15, 10), facecolor='black')
    
    # Plot 1: The Raw Spin Topology
    ax1 = plt.subplot(1, 2, 1)
    ax1.set_title("1. Spin Topology (Winding Number)", color='white')
    im1 = ax1.imshow(spin_map, extent=[M_MIN, M_MAX, L_MIN, L_MAX], 
                     origin='lower', cmap='nipy_spectral')
    ax1.axis('off')
    
    # Plot 2: The "Reality Filter" (Spin masked by Stability)
    # We create a mask where High Chaos = Transparent/Black
    # Low Chaos = Visible
    
    ax2 = plt.subplot(1, 2, 2)
    ax2.set_title("2. Stable Matter Candidates (Spin x Stability)", color='white')
    
    # Normalize Lyapunov for alpha channel
    # Lower is better. 0 -> 1.0 opacity. Max -> 0.0 opacity.
    lyap_norm = (lyap_map - lyap_map.min()) / (lyap_map.max() - lyap_map.min())
    alpha_mask = 1.0 - lyap_norm 
    # Sharpen the mask (be strict about stability)
    alpha_mask = np.power(alpha_mask, 3) 
    
    # Create RGBA image using the Colormap of Spin
    # Get RGB from spin map
    cmap = plt.get_cmap('nipy_spectral')
    norm = mcolors.Normalize(vmin=spin_map.min(), vmax=spin_map.max())
    rgba_img = cmap(norm(spin_map))
    
    # Apply alpha from Lyapunov
    rgba_img[:, :, 3] = alpha_mask
    
    ax2.imshow(rgba_img, extent=[M_MIN, M_MAX, L_MIN, L_MAX], origin='lower')
    ax2.axis('off')
    
    # Highlight Integer Zones on the Stable Map
    # Contours where Spin is close to integer
    ax2.contour(spin_map, levels=np.arange(0, 10, 1), 
                colors='white', linewidths=0.5, alpha=0.3,
                extent=[M_MIN, M_MAX, L_MIN, L_MAX])

    plt.tight_layout()
    plt.savefig('correlation_matter_map.png')
    plt.show()

if __name__ == "__main__":
    run_correlation_scan()