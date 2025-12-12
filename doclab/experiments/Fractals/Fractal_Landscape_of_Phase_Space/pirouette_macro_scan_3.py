import numpy as np
import matplotlib.pyplot as plt
from time import time
from numba import jit, prange

# --------------------------------------------------
# PIROUETTE: HYPER-ACCELERATED DEEP FIELD SONAR
# --------------------------------------------------
# GOAL: Detect "thin" fractal structures in the 
# 6 Trillion unit void using stochastic sampling.
# --------------------------------------------------

# --- Configuration ---
RANGE = 60
RES = 1000                   # 1000x1000 Image (1 Million Pixels)
SAMPLES_PER_PIXEL = 4        # Higher = Better detection of thin lines, but slower.
STEPS = 2500                 # Integration depth
DT = 0.01
GAMMA = 0.02
TWIST = 2.83814

# --- JIT Compiled Physics Engine (The Fast Part) ---
@jit(nopython=True, fastmath=True)
def get_force_fast(m, lam):
    # The Unified Physics (Unrolled for Numba speed)
    
    # 1. Base Forces
    F_teal_m = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)
    
    F_red_m = -m
    # The Twist Violation
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation
    
    # 2. The Gold Force (Geometric Mean)
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    mag = np.sqrt(sum_m*sum_m + sum_lam*sum_lam)
    scale = np.sqrt(mag)
    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale
    
    # 3. Dynamic Weights based on Angle
    # arctan2 returns radians, convert to degrees
    angle_rad = np.arctan2(lam, m)
    angle_deg = (angle_rad * 180.0 / np.pi) % 360.0
    
    # Gold Weight (Target 30 deg)
    diff_g = np.abs(angle_deg - 30.0)
    if diff_g > 180.0: diff_g = 360.0 - diff_g
    w_gold = np.exp(-((diff_g/80.0)**2))
    
    # Teal Weight (Target 150 deg)
    diff_t = np.abs(angle_deg - 150.0)
    if diff_t > 180.0: diff_t = 360.0 - diff_t
    w_teal = np.exp(-((diff_t/80.0)**2))
    
    # Red Weight (Target 270 deg)
    diff_r = np.abs(angle_deg - 270.0)
    if diff_r > 180.0: diff_r = 360.0 - diff_r
    w_red = np.exp(-((diff_r/80.0)**2))
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    # 4. Final Force Composition
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

@jit(nopython=True, fastmath=True)
def sim_pixel_sonar(center_m, center_l, pixel_width):
    # "Sonar" detection: Check multiple random points in this pixel.
    # Return the MAXIMUM instability found.
    
    max_disp = 0.0
    
    for i in range(SAMPLES_PER_PIXEL):
        # Random offset within the pixel to catch thin lines
        # Only add noise if we are doing more than 1 sample
        if SAMPLES_PER_PIXEL > 1:
            off_m = (np.random.random() - 0.5) * pixel_width
            off_l = (np.random.random() - 0.5) * pixel_width
        else:
            off_m = 0.0
            off_l = 0.0
            
        m = center_m + off_m
        lam = center_l + off_l
        
        start_m = m
        start_l = lam
        
        pm = 0.0
        plam = 0.0
        
        # Integration Loop
        for step in range(STEPS):
            Fm, Flam, w_red = get_force_fast(m, lam)
            
            # Drag calculation
            drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
            
            pm = (pm + 0.5 * DT * Fm) * drag
            plam = (plam + 0.5 * DT * Flam) * drag
            m += DT * pm
            lam += DT * plam
            
            # Optimization: Early exit if it flies off to infinity?
            # Actually, let's keep it robust.
            
        # Calculate Displacement
        disp = np.sqrt((m - start_m)**2 + (lam - start_l)**2)
        if disp > max_disp:
            max_disp = disp
            
    return max_disp

@jit(nopython=True, parallel=True)
def run_scan_parallel(res, range_val):
    result_grid = np.zeros((res, res), dtype=np.float64)
    pixel_width = (range_val * 2.0) / res
    
    # Parallel loop over rows
    for y in prange(res):
        # Map y index to physical coordinate (Coupling Field)
        # origin='lower' logic
        l_coord = -range_val + (y * pixel_width)
        
        for x in range(res):
            m_coord = -range_val + (x * pixel_width)
            
            val = sim_pixel_sonar(m_coord, l_coord, pixel_width)
            result_grid[y, x] = val
            
    return result_grid

# --- Main Execution ---
if __name__ == "__main__":
    print(f"--- PIROUETTE SONAR SCAN ---")
    print(f"Target: +/- {RANGE:,.0f} Units")
    print(f"Resolution: {RES}x{RES}")
    print(f"Supersampling: {SAMPLES_PER_PIXEL}x (Total pings: {RES*RES*SAMPLES_PER_PIXEL:,})")
    print("Compiling Physics Engine (this takes a moment)...")
    
    t0 = time()
    
    # Run the big scan
    grid = run_scan_parallel(RES, RANGE)
    
    t1 = time()
    print(f"Scan Complete in {t1-t0:.2f} seconds.")
    
    # Plotting
    print("Rendering Image...")
    plt.figure(figsize=(12, 12), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Log scale is CRITICAL here to see faint structures against the void
    # inferno: Black=Low(Stable), Yellow=High(Chaos)
    plt.imshow(np.log1p(grid), extent=[-RANGE, RANGE, -RANGE, RANGE], 
               origin='lower', cmap='inferno')
    
    # Mark Home
    plt.scatter([0], [0], color='cyan', marker='+', s=100, label='Origin (Zone 1)', alpha=0.7)
    
    plt.title(f"Pirouette Framework: The {RANGE} Limit\n(Sonar Mode: {SAMPLES_PER_PIXEL}x Supersampling)", color='white')
    plt.xlabel("Mass Field Dimension", color='white')
    plt.ylabel("Coupling Field Dimension", color='white')
    plt.colorbar(fraction=0.046, pad=0.04).set_label("Log Displacement (Instability)", color='white')
    plt.legend(facecolor='black', labelcolor='white')
    
    filename = f"sonar_scan_{RANGE}.png"
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    print(f"Saved to {filename}")
    plt.show()