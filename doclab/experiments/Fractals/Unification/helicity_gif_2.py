import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from numba import njit
from PIL import Image
import os
import shutil
import time

# =========================================================
#  CONFIGURATION
# =========================================================
OUTPUT_DIR = "helicity_zoom_frames"
GIF_FILENAME = "animated_helicity_zoom.gif"

# Animation & Viewport Settings
FRAMES = 60          # Total frames for one loop
DURATION_MS = 50     # Speed (50ms per frame = 20 FPS)
RES_ANIM = 600       # Grid resolution (300x300 for speed)

# Zoomed Viewport (Matching proton_helicity_color_0.05.jpg)
M_MIN, M_MAX = -2, 2
L_MIN, L_MAX = -2, 2

# Animation of the chaotic parameter
TWIST_BASE = 3.8
TWIST_AMPLITUDE = 0.1 # Range will be 3.7 to 3.9

# Dynamics parameters (from pi_scanner_3.py)
GAMMA = 0.5
DT    = 0.015
MAX_STEPS = 200
EPSILON = 1e-5
R_ESCAPE = 50.0
HELICITY_STOP = np.pi * 0.95

# =========================================================
#  1. MODIFIED PHYSICS KERNEL (JIT compiled)
# =========================================================

@njit
def normalize_angle_diff(delta):
    return np.arctan2(np.sin(delta), np.cos(delta))

@njit
def get_force(m, lam, current_twist): # <-- MODIFIED TO ACCEPT TWIST
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    F_red_m   = -(m - 0.0)
    # USE ANIMATED TWIST PARAMETER
    p_violation = current_twist * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2)
    scale   = np.sqrt(mag)

    F_gold_m   = sum_m   * scale
    F_gold_lam = sum_lam * scale

    angle_deg = np.degrees(np.arctan2(lam, m)) % 360.0

    diff_g = min(abs(angle_deg - 30.0), 360.0 - abs(angle_deg - 30.0))
    w_gold = np.exp(-(diff_g / 80.0)**2)

    diff_t = min(abs(angle_deg - 150.0), 360.0 - abs(angle_deg - 150.0))
    w_teal = np.exp(-(diff_t / 80.0)**2)

    diff_r = min(abs(angle_deg - 270.0), 360.0 - abs(angle_deg - 270.0))
    w_red  = np.exp(-(diff_r / 80.0)**2)

    tot = w_gold + w_teal + w_red + 1e-6

    nw_red  = w_red  / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot

    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam, nw_red

@njit
def measure_helicity(m0, l0, current_twist): # <-- MODIFIED TO ACCEPT TWIST
    """
    Run a real + shadow trajectory from (m0, l0) and
    return log(max angular decorrelation).
    """
    m1, l1 = m0, l0
    pm1, pl1 = 0.0, 0.0

    m2, l2 = m0 + EPSILON, l0 + EPSILON
    pm2, pl2 = 0.0, 0.0

    max_diff_angle = 0.0

    for _ in range(MAX_STEPS):
        # Real
        Fm1, Flam1, w_red1 = get_force(m1, l1, current_twist) # <-- PASS TWIST
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Flam1) * drag1
        m1 += DT * pm1
        l1 += DT * pl1
        Fm1, Flam1, w_red1 = get_force(m1, l1, current_twist) # <-- PASS TWIST
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Flam1) * drag1

        # Shadow
        Fm2, Flam2, w_red2 = get_force(m2, l2, current_twist) # <-- PASS TWIST
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Flam2) * drag2
        m2 += DT * pm2
        l2 += DT * pl2
        Fm2, Flam2, w_red2 = get_force(m2, l2, current_twist) # <-- PASS TWIST
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Flam2) * drag2

        # Helicity
        ang1 = np.arctan2(l1, m1)
        ang2 = np.arctan2(l2, m2)
        diff = normalize_angle_diff(ang1 - ang2)
        adiff = np.abs(diff)
        if adiff > max_diff_angle:
            max_diff_angle = adiff

        # Stops
        if max_diff_angle > HELICITY_STOP:
            break
        if (m1**2 + l1**2) > R_ESCAPE:
            break

    return np.log(max_diff_angle + EPSILON)

def compute_helicity_grid(res, m_min, m_max, l_min, l_max, current_twist):
    m_vals = np.linspace(m_min, m_max, res)
    l_vals = np.linspace(l_min, l_max, res)
    H = np.zeros((res, res), dtype=float)

    # Use nested loops (Numba is inside measure_helicity)
    for i, lam in enumerate(l_vals):
        for j, m in enumerate(m_vals):
            # Pass the current twist value
            H[i, j] = measure_helicity(m, lam, current_twist)
    
    # We flip the grid (H) so that lower 'i' corresponds to lower 'y' on the plot
    return np.flipud(H)

# =========================================================
#  2. ANIMATION DRIVER
# =========================================================

def run_helicity_animator():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    print(f"--- 🌀 HELICITY ZOOM ANIMATOR ---")
    print(f"Rendering {FRAMES} frames at {RES_ANIM}x{RES_ANIM}...")
    
    # Pre-compile Numba functions by calling them once
    print("[SETUP] Running Numba compilation (first time is slower)...")
    get_force(1.0, 1.0, TWIST_BASE)
    measure_helicity(1.0, 1.0, TWIST_BASE)
    print("[SETUP] Numba compiled. Starting rendering.")

    frames_buffer = []
    start_time = time.time()
    
    for f in range(FRAMES):
        prog = f / FRAMES
        
        # 1. Animate the chaotic parameter
        current_twist = TWIST_BASE + TWIST_AMPLITUDE * np.sin(2 * np.pi * prog)
        
        # 2. Compute the Helicity Field
        H_grid = compute_helicity_grid(RES_ANIM, M_MIN, M_MAX, L_MIN, L_MAX, current_twist)
        
        # 3. Visualization
        plt.figure(figsize=(6, 6))
        
        # Clip values to maintain the high-contrast color scheme seen in the image.
        # Original color range is roughly -5 to -10.
        H_clipped = np.clip(H_grid, -10.0, -5.0) 
        
        plt.imshow(H_clipped, origin="lower",
                   extent=[M_MIN, M_MAX, L_MIN, L_MAX],
                   cmap="turbo", # 'turbo' closely matches the color progression
                   aspect='auto')
        
        # Title to show the current animated parameter value
        plt.title(f"Proton Basin: Helicity Field H (TWIST={current_twist:.3f})")
        plt.xlabel("Mass field m")
        plt.ylabel("Coupling field λ")
        
        # Add a placeholder colorbar (matplotlib will handle the colors)
        cbar = plt.colorbar(label=r"Angular Decorrelation (Helicity $H = \log(\Delta\theta_{\rm max})$)")

        # Save without border/axis for a clean animation frame
        plt.axis('off')
        plt.tight_layout(pad=0)
        
        fn = os.path.join(OUTPUT_DIR, f"frame_{f:03d}.png")
        plt.savefig(fn, dpi=100, bbox_inches='tight', pad_inches=0)
        plt.close()
        
        if f % 10 == 0:
            elapsed = time.time() - start_time
            print(f"  Frame {f}/{FRAMES} done. Time per frame: {elapsed/(f+1):.2f}s")

    # 4. Stitch GIF
    print("Stitching GIF...")
    # Load frames back from disk for PIL
    for f in range(FRAMES):
        frames_buffer.append(Image.open(os.path.join(OUTPUT_DIR, f"frame_{f:03d}.png")))
    
    frames_buffer[0].save(
        GIF_FILENAME,
        save_all=True,
        append_images=frames_buffer[1:],
        duration=DURATION_MS,
        loop=0
    )
    print(f"✅ Saved: {GIF_FILENAME}")
    shutil.rmtree(OUTPUT_DIR)

if __name__ == "__main__":
    run_helicity_animator()