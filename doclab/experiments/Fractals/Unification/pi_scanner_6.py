import numpy as np
import matplotlib.pyplot as plt
from numba import njit
import time

# =========================================================
#  CHROMATIC STRUCTURE SCANNER
#  Decodes the "Flavor" and "Depth" of the Proton Basin
# =========================================================

# --- CONFIGURATION (Adjust your Zoom Here) ---
# WIDE VIEW (Holographic Scale)
# M_MIN, M_MAX = -2.8e11, 2.8e11
# L_MIN, L_MAX = -2.8e11, 2.8e11

# CORE VIEW (The "Wacky Circle")
M_MIN, M_MAX = -1, 1
L_MIN, L_MAX = -1, 1

RES = 1000          # Resolution
MAX_STEPS = 500     # Higher steps = deeper fractal detail
R_ESCAPE = 1000.0   # Boundary for escape

# --- PHYSICS PARAMETERS ---
TWIST = 3.8
GAMMA = 0.5
DT    = 0.015

@njit
def get_force_weights(m, lam):
    """
    Returns the weights of the three forces at a given point.
    """
    # 1. Teal Force (Linear)
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    # 2. Red Force (Parity/Twist Violation)
    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold Force (Nonlinear Scaling)
    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2)
    scale   = np.sqrt(mag)
    F_gold_m   = sum_m * scale
    F_gold_lam = sum_lam * scale

    # Angular Weights
    angle_deg = np.degrees(np.arctan2(lam, m)) % 360.0

    # Gold (30 deg), Teal (150 deg), Red (270 deg)
    diff_g = min(abs(angle_deg - 30.0), 360.0 - abs(angle_deg - 30.0))
    w_gold = np.exp(-(diff_g / 80.0)**2)

    diff_t = min(abs(angle_deg - 150.0), 360.0 - abs(angle_deg - 150.0))
    w_teal = np.exp(-(diff_t / 80.0)**2)

    diff_r = min(abs(angle_deg - 270.0), 360.0 - abs(angle_deg - 270.0))
    w_red  = np.exp(-(diff_r / 80.0)**2)

    tot = w_gold + w_teal + w_red + 1e-6
    return w_red/tot, w_teal/tot, w_gold/tot, F_red_m, F_red_lam, F_teal_m, F_teal_lam, F_gold_m, F_gold_lam

@njit
def trace_chromatic_trajectory(m0, l0):
    """
    Traces a particle and records:
    1. Escape Time (Structure)
    2. Average Color Dominance (Identity)
    3. Winding Number (Vorticity)
    """
    m, l = m0, l0
    pm, pl = 0.0, 0.0
    
    # Accumulators for "Color Charge"
    total_red = 0.0
    total_teal = 0.0
    total_gold = 0.0
    
    # Winding tracking
    prev_angle = np.arctan2(l, m)
    total_winding = 0.0
    
    steps_taken = 0
    escaped = False
    
    for i in range(MAX_STEPS):
        nw_red, nw_teal, nw_gold, Frm, Frl, Ftm, Ftl, Fgm, Fgl = get_force_weights(m, l)
        # Accumulate dominant force "flavor"
        total_red += nw_red
        total_teal += nw_teal
        total_gold += nw_gold
        
        # Calculate Net Force
        Fm = nw_teal * Ftm + nw_red * Frm + nw_gold * Fgm
        Flam = nw_teal * Ftl + nw_red * Frl + nw_gold * Fgl
        
        # Dynamics Step (Verlet/Drag)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * nw_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        pl = (pl + 0.5 * DT * Flam) * drag
        m += DT * pm
        l += DT * pl
        
        # Winding check
        curr_angle = np.arctan2(l, m)
        d_angle = curr_angle - prev_angle
        # Fix wrap-around
        if d_angle > np.pi: d_angle -= 2*np.pi
        if d_angle < -np.pi: d_angle += 2*np.pi
        total_winding += d_angle
        prev_angle = curr_angle
        
        steps_taken += 1
        
        if (m**2 + l**2) > R_ESCAPE**2:
            escaped = True
            break
            
    # Normalize Color
    norm = total_red + total_teal + total_gold + 1e-9
    r_val = total_red / norm
    g_val = total_teal / norm # Map Teal to Green channel for RGB
    b_val = total_gold / norm # Map Gold to Blue channel for RGB
    
    return steps_taken, escaped, r_val, g_val, b_val, total_winding

@njit
def render_scan(m_vals, l_vals):
    h = len(l_vals)
    w = len(m_vals)
    
    # Output grid: R, G, B, Alpha (Structure)
    image = np.zeros((h, w, 4)) 
    
    for i in range(h):
        for j in range(w):
            steps, escaped, r, g, b, winding = trace_chromatic_trajectory(m_vals[j], l_vals[i])
            
            # --- VISUALIZATION LOGIC ---
            
            # 1. Structure (Brightness/Alpha)
            # If trapped (did not escape), it's the "Basin" (Solid)
            # If escaped, use log-smoothing for "Glow"
            if not escaped:
                intensity = 1.0
                # Darken high vorticity centers (The "Eye")
                if abs(winding) > 6*np.pi: 
                    intensity = 0.6 
            else:
                # Smooth escape banding
                nu = np.log(np.log(m_vals[j]**2 + l_vals[i]**2)) / np.log(2)
                smooth_steps = steps + 1 - nu
                intensity = 0.1 + 0.9 * (smooth_steps / MAX_STEPS)

            # 2. Color Mapping
            # Red Channel = Twist Force + High Vorticity Warning
            # Green Channel = Teal Force (Stability)
            # Blue Channel = Gold Force (Non-linearity)
            
            image[i, j, 0] = r 
            image[i, j, 1] = g
            image[i, j, 2] = b
            image[i, j, 3] = intensity 
            
    return image

def run_chromatic_scan():
    print(f"Scanning range: [{M_MIN}, {M_MAX}]...")
    start = time.time()
    
    m_vals = np.linspace(M_MIN, M_MAX, RES)
    l_vals = np.linspace(L_MIN, L_MAX, RES)
    
    # Run the Numba kernel
    # Compile first
    trace_chromatic_trajectory(0.1, 0.1) 
    
    raw_img = render_scan(m_vals, l_vals)
    
    print(f"Scan complete in {time.time() - start:.2f}s")
    
    # Post-process for display
    # We want a black background, so we blend the Alpha
    final_img = np.zeros((RES, RES, 3))
    
    alpha = raw_img[:, :, 3]
    rgb = raw_img[:, :, 0:3]
    
    # Background color (Deep Space Black)
    bg = np.array([0.0, 0.0, 0.05])
    
    for c in range(3):
        final_img[:, :, c] = rgb[:, :, c] * alpha + bg[c] * (1 - alpha)
        
    plt.figure(figsize=(10, 10))
    plt.imshow(final_img, origin='lower', extent=[M_MIN, M_MAX, L_MIN, L_MAX])
    plt.title(f"Chromatic Structure Scan\nRed=Twist, Green=Stable, Blue=NonLinear")
    plt.xlabel("Mass Field (m)")
    plt.ylabel("Coupling Field (lambda)")
    plt.tight_layout()
    plt.savefig("chromatic_fractal.png", dpi=300)
    print("Saved 'chromatic_fractal.png'")
    plt.show()

if __name__ == "__main__":
    run_chromatic_scan()