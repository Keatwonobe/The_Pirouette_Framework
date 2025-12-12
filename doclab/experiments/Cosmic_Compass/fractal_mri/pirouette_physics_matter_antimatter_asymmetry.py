import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE PRESSURE TEST 2: THE MIRROR TEST (ANTIMATTER)
# --------------------------------------------------
# We test for CP Violation (Matter/Antimatter Asymmetry).
#
# Method:
# 1. Spawn a stable Electron (Matter) at (-1.8, 0.0).
# 2. Spawn a "Mirror Electron" (Antimatter) at (1.8, 0.0).
#    (Spatial Reflection P).
# 3. If the Vacuum is symmetric, both should survive.
# 4. If the Vacuum is Chiral (Twisted), the Antimatter
#    should destabilize and die.
# --------------------------------------------------

TWIST = 2.83814 
GAMMA = 0.02
DT = 0.005
STEPS = 8000

def get_force_vectorized(m, lam):
    # --- The Unified Physics (Tuned) ---
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    mag = np.sqrt(sum_m**2 + sum_lam**2)
    scale = np.sqrt(mag)
    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale
    
    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    diff_g = np.minimum(np.abs(angle - 30), 360-np.abs(angle - 30))
    w_gold = np.exp(-(diff_g/80)**2)
    
    diff_t = np.minimum(np.abs(angle - 150), 360-np.abs(angle - 150))
    w_teal = np.exp(-(diff_t/80)**2)
    
    diff_r = np.minimum(np.abs(angle - 270), 360-np.abs(angle - 270))
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_mirror_test():
    print("Running The Mirror Test (Matter vs Antimatter)...")
    
    # --- PARTICLE 1: MATTER (The one we know works) ---
    m1, l1 = -1.8, 0.0
    pm1, pl1 = 0.0, 2.0 
    traj1_m, traj1_l = [], []
    
    # --- PARTICLE 2: ANTIMATTER (The Mirror Twin) ---
    # We reflect the coordinates (Parity Flip)
    m2, l2 = 1.8, 0.0   
    # We also flip momentum to respect P-symmetry
    pm2, pl2 = 0.0, 2.0 
    traj2_m, traj2_l = [], []
    
    print("Simulating parallel universes...")
    
    for i in range(STEPS):
        # Update Matter
        Fm1, Fl1, w1 = get_force_vectorized(m1, l1)
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w1)
        pm1 = (pm1 + 0.5 * DT * Fm1) * drag1
        pl1 = (pl1 + 0.5 * DT * Fl1) * drag1
        m1 += DT * pm1
        l1 += DT * pl1
        
        # Update Antimatter
        Fm2, Fl2, w2 = get_force_vectorized(m2, l2)
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w2)
        pm2 = (pm2 + 0.5 * DT * Fm2) * drag2
        pl2 = (pl2 + 0.5 * DT * Fl2) * drag2
        m2 += DT * pm2
        l2 += DT * pl2
        
        traj1_m.append(m1); traj1_l.append(l1)
        traj2_m.append(m2); traj2_l.append(l2)

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), facecolor='black')
    
    # Plot 1: Matter
    ax1.set_facecolor('black')
    ax1.plot(traj1_m, traj1_l, color='cyan', linewidth=1.0, alpha=0.8)
    ax1.set_title("Universe A: Matter (Stable)", color='white', fontsize=14)
    ax1.set_xlim(-4, 4); ax1.set_ylim(-4, 4)
    ax1.grid(color='#333333', alpha=0.5)
    
    # Plot 2: Antimatter
    ax2.set_facecolor('black')
    ax2.plot(traj2_m, traj2_l, color='magenta', linewidth=1.0, alpha=0.8)
    ax2.set_title("Universe B: Antimatter (Unstable?)", color='white', fontsize=14)
    ax2.set_xlim(-4, 4); ax2.set_ylim(-4, 4)
    ax2.grid(color='#333333', alpha=0.5)
    
    # Check if Antimatter survived (is it bounded?)
    final_r = np.sqrt(m2**2 + l2**2)
    status = "SURVIVED" if final_r < 4.0 else "ANNIHILATED"
    color = "lime" if status == "SURVIVED" else "red"
    
    plt.figtext(0.5, 0.05, f"ANTIMATTER STATUS: {status}", ha="center", color=color, fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('mirror_test.png')
    plt.show()

if __name__ == "__main__":
    run_mirror_test()