import mpmath as mp
import matplotlib.pyplot as plt
import numpy as np
from time import time

# --------------------------------------------------
# PIROUETTE: SUB-ATOMIC MICROSCOPE
# --------------------------------------------------
# GOAL: Pierce the "Machine Epsilon" barrier using
# arbitrary precision math to see the true center.
# --------------------------------------------------

# --- Configuration ---
# We are zooming into the sub-atomic scale of the framework
RANGE = '6.0e-20'  # 10^-20 scale. Standard float math fails here.
RES = 60           # Low resolution because mpmath is SLOW (it's pure software)
STEPS = 500
DT = 0.01
GAMMA = 0.02
TWIST = 2.83814

# Set Precision to 50 decimal digits (Standard is ~15)
mp.dps = 50

def get_force_mp(m, lam):
    # Mpmath versions of the physics
    # We must be careful to keep everything as mp.mpf types
    
    F_teal_m = -(m + mp.mpf('0.866')) 
    F_teal_lam = -(lam - mp.mpf('0.5'))

    F_red_m = -m
    # sin calculation is expensive in mpmath
    p_violation = mp.mpf(TWIST) * mp.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    
    # Magnitude
    mag = mp.sqrt(sum_m**2 + sum_lam**2)
    scale = mp.sqrt(mag)
    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale
    
    # Weights (This is the heavy part)
    # arctan2
    angle_rad = mp.atan2(lam, m)
    angle_deg = (angle_rad * 180.0 / mp.pi) % 360.0
    
    def get_weight(target_deg):
        diff = mp.fabs(angle_deg - target_deg)
        if diff > 180.0: diff = 360.0 - diff
        return mp.exp(-((diff/80.0)**2))

    w_gold = get_weight(30.0)
    w_teal = get_weight(150.0)
    w_red = get_weight(270.0)
    
    tot = w_gold + w_teal + w_red + mp.mpf('1e-50') # tiny epsilon
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_microscope():
    print(f"--- PIROUETTE SUB-ATOMIC MICROSCOPE ---")
    print(f"Precision: {mp.dps} decimal digits")
    print(f"Range: +/- {RANGE}")
    
    range_val = mp.mpf(RANGE)
    
    # We can't use numpy arrays for mpmath objects easily
    # We have to use Python lists and loops. It will be slow.
    
    grid = np.zeros((RES, RES))
    
    t0 = time()
    
    print("Scanning pixel by pixel (this may take a minute)...")
    
    pixel_width = (range_val * 2) / RES
    start_offset = -range_val
    
    for y in range(RES):
        # Progress bar
        if y % 10 == 0: print(f"Row {y}/{RES}...")
        
        l_coord = start_offset + (y * pixel_width)
        
        for x in range(RES):
            m_coord = start_offset + (x * pixel_width)
            
            # Simulation
            m = m_coord
            lam = l_coord
            pm = mp.mpf(0.0)
            plam = mp.mpf(0.0)
            
            orig_m = m
            orig_l = lam
            
            for step in range(STEPS):
                Fm, Flam, w_red = get_force_mp(m, lam)
                
                # Drag
                drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
                
                pm = (pm + 0.5 * DT * Fm) * drag
                plam = (plam + 0.5 * DT * Flam) * drag
                m += DT * pm
                lam += DT * plam
            
            # Calculate Displacement
            # Convert back to float for plotting
            disp = float(mp.sqrt((m - orig_m)**2 + (lam - orig_l)**2))
            grid[y, x] = disp
            
    t1 = time()
    print(f"Scan complete in {t1-t0:.2f}s")
    
    # Plotting
    plt.figure(figsize=(10, 10), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    plt.imshow(np.log1p(grid), origin='lower', cmap='inferno')
    
    plt.title(f"Sub-Atomic Limit ({RANGE} units)\nPrecision: {mp.dps} Digits", color='white')
    plt.colorbar(fraction=0.046, pad=0.04).set_label("Instability", color='white')
    
    plt.savefig("microscope_scan.png")
    plt.show()

if __name__ == "__main__":
    run_microscope()