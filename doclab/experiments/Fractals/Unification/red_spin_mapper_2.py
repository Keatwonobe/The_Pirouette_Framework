import numpy as np
import matplotlib.pyplot as plt
from numba import njit
import time

# =========================================================
#  QUANTUM MICROSCOPE
#  Target: The Twist Singularity (Quark)
# =========================================================

# --- TARGET COORDINATES (Found by Quark Hunter) ---
QUARK_M = -0.18107166
QUARK_L =  0.75130406

# --- PHYSICS PARAMETERS ---
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015
MAX_STEPS = 1000   # High detail for deep zoom
R_ESCAPE = 1000.0

@njit
def get_force_weights(m, lam):
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2)
    scale   = np.sqrt(mag)
    F_gold_m   = sum_m * scale
    F_gold_lam = sum_lam * scale

    angle_deg = np.degrees(np.arctan2(lam, m)) % 360.0

    diff_g = min(abs(angle_deg - 30.0), 360.0 - abs(angle_deg - 30.0))
    w_gold = np.exp(-(diff_g / 80.0)**2)

    diff_t = min(abs(angle_deg - 150.0), 360.0 - abs(angle_deg - 150.0))
    w_teal = np.exp(-(diff_t / 80.0)**2)

    diff_r = min(abs(angle_deg - 270.0), 360.0 - abs(angle_deg - 270.0))
    w_red  = np.exp(-(diff_r / 80.0)**2)

    tot = w_gold + w_teal + w_red + 1e-6
    return w_red/tot, w_teal/tot, w_gold/tot, F_red_m, F_red_lam, F_teal_m, F_teal_lam, F_gold_m, F_gold_lam

@njit
def trace_pixel(m0, l0):
    m, l = m0, l0
    pm, pl = 0.0, 0.0
    
    total_red = 0.0
    total_teal = 0.0
    total_gold = 0.0
    
    steps_taken = 0
    escaped = False
    
    for i in range(MAX_STEPS):
        nw_red, nw_teal, nw_gold, Frm, Frl, Ftm, Ftl, Fgm, Fgl = get_force_weights(m, l)
        
        total_red += nw_red
        total_teal += nw_teal
        total_gold += nw_gold
        
        Fm = nw_teal * Ftm + nw_red * Frm + nw_gold * Fgm
        Flam = nw_teal * Ftl + nw_red * Frl + nw_gold * Fgl
        
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * nw_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        pl = (pl + 0.5 * DT * Flam) * drag
        m += DT * pm
        l += DT * pl
        
        steps_taken += 1
        
        # Check escape
        if (m*m + l*l) > R_ESCAPE**2:
            escaped = True
            break
            
    norm = total_red + total_teal + total_gold + 1e-9
    return steps_taken, escaped, total_red/norm, total_teal/norm, total_gold/norm

@njit
def render_chromatic_grid(m_min, m_max, l_min, l_max, res):
    img = np.zeros((res, res, 4))
    
    m_vals = np.linspace(m_min, m_max, res)
    l_vals = np.linspace(l_min, l_max, res)
    
    for i in range(res):
        for j in range(res):
            steps, escaped, r, g, b = trace_pixel(m_vals[j], l_vals[i])
            
            # Brightness Logic
            if not escaped:
                # Inside the Basin
                intensity = 1.0 
            else:
                # Outside (The Holographic Field)
                # Use log-smoothing for continuous bands
                # This reveals the "Wave" structure
                nu = np.log(np.log(m_vals[j]**2 + l_vals[i]**2)) / np.log(2)
                smooth = steps + 1 - nu
                intensity = 0.2 + 0.8 * (np.sin(smooth * 0.2) * 0.5 + 0.5) 

            img[i, j, 0] = r
            img[i, j, 1] = g
            img[i, j, 2] = b
            img[i, j, 3] = intensity
            
    return img

def run_microscope():
    RES = 1000 # High Resolution
    
    # --- SCAN 1: THE QUARK CORE (Deep Micro) ---
    print("--- 🔬 MICROSCOPE MODE: Analyzing Quark Core ---")
    radius = 12 # Zoom window size
    m_min, m_max = QUARK_M - radius, QUARK_M + radius
    l_min, l_max = QUARK_L - radius, QUARK_L + radius
    
    # Compile
    trace_pixel(0.1, 0.1)
    
    print(f"Scanning Quark at ({QUARK_M}, {QUARK_L})...")
    img_core = render_chromatic_grid(m_min, m_max, l_min, l_max, RES)
    
    # Process for display
    final_core = np.zeros((RES, RES, 3))
    bg = np.array([0.05, 0.0, 0.0]) # Dark Red background for core
    for c in range(3):
        final_core[:,:,c] = img_core[:,:,c] * img_core[:,:,3] + bg[c] * (1 - img_core[:,:,3])
        
    plt.figure(figsize=(10, 10))
    plt.imshow(final_core, origin='lower', extent=[m_min, m_max, l_min, l_max])
    plt.plot(QUARK_M, QUARK_L, 'w+', markersize=20, label="Singularity")
    plt.title(f"The Quark Event Horizon\n(m={QUARK_M:.4f}, l={QUARK_L:.4f})")
    plt.legend()
    plt.savefig("quark_singularity_core.png", dpi=300)
    print("Saved 'quark_singularity_core.png'")


    # --- SCAN 2: THE HOLOGRAPHIC TEST (Deep Macro) ---
    print("\n--- 🔭 TELESCOPE MODE: Testing Holographic Projection ---")
    # Trillions Scale
    SCALE = 12
    m_min, m_max = -SCALE, SCALE
    l_min, l_max = -SCALE, SCALE
    
    print(f"Scanning at scale {SCALE}...")
    img_holo = render_chromatic_grid(m_min, m_max, l_min, l_max, RES)
    
    # Process
    final_holo = np.zeros((RES, RES, 3))
    bg = np.array([0.0, 0.0, 0.05])
    for c in range(3):
        final_holo[:,:,c] = img_holo[:,:,c] * img_holo[:,:,3] + bg[c] * (1 - img_holo[:,:,3])

    # Overlay: Theoretical Interference Pattern from the Quark
    # If the fractal structure matches these rings, the Quark is the source.
    print("Overlaying theoretical wave pattern from Quark source...")
    y_grid, x_grid = np.ogrid[l_min:l_max:RES*1j, m_min:m_max:RES*1j]
    
    # Distance from QUARK (not origin!)
    dist_sq = (x_grid - QUARK_M)**2 + (y_grid - QUARK_L)**2
    # Use log distance because the fractal structure is usually log-periodic
    log_dist = np.log(dist_sq)
    
    # Create faint white rings
    rings = np.sin(log_dist * 2.0) # Adjust frequency if needed
    
    plt.figure(figsize=(10, 10))
    plt.imshow(final_holo, origin='lower', extent=[m_min, m_max, l_min, l_max])
    
    # Plot the Rings (Alpha blended)
    plt.contour(x_grid.flatten(), y_grid.flatten(), rings, levels=[0.95], colors='white', alpha=0.3, linewidths=0.5)
    
    plt.title(f"Holographic Field (1 Trillion Units)\nOverlay: Theoretical Waves from Quark Source")
    plt.savefig("proton_hologram_test.png", dpi=300)
    print("Saved 'proton_hologram_test.png'")
    plt.show()

if __name__ == "__main__":
    run_microscope()