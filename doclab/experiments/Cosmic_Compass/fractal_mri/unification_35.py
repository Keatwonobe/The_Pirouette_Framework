import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --------------------------------------------------
# PIROUETTE FRAMEWORK: PORTRAIT OF A FERMION
# --------------------------------------------------
# We input the Fundamental Constant we discovered
# (Twist = 2.83814) to visualize the "Perfect"
# Spin 1/2 Particle. We expect a double-loop
# or Mobius-like topology (720 deg symmetry).
# --------------------------------------------------

TWIST = 2.83814 # <--- THE MAGIC NUMBER
GAMMA = 0.05
DT = 0.005
STEPS = 50000
STABILIZE = 15000

def get_force_vectorized(m, lam):
    # --- Standard Pirouette Physics ---
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
    
    angle = np.degrees(np.arctan2(lam, m)) % 360
    # Weights
    diff_g = np.minimum(np.abs(angle - 30), 360-np.abs(angle - 30))
    w_gold = np.exp(-(diff_g/80)**2)
    diff_t = np.minimum(np.abs(angle - 150), 360-np.abs(angle - 150))
    w_teal = np.exp(-(diff_t/80)**2)
    diff_r = np.minimum(np.abs(angle - 270), 360-np.abs(angle - 270))
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red, nw_teal, nw_gold = w_red/tot, w_teal/tot, w_gold/tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_fermion_vis():
    print(f"Generating Portrait of Spin 1/2 Particle (Twist={TWIST})...")
    
    # Coordinate from Poincare map
    m, lam = -1.8, 0.0
    pm, plam = 0.0, 2.0 
    
    # Stabilization
    for _ in range(STABILIZE):
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

    # Recording
    hist_m = []
    hist_lam = []
    hist_pm = []
    
    # Color by time to see the "winding"
    colors = []
    
    for i in range(STEPS):
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
        
        hist_m.append(m)
        hist_lam.append(lam)
        hist_pm.append(pm)
        colors.append(i)

    # ----------------------------------------
    # PLOTTING 3D
    # ----------------------------------------
    fig = plt.figure(figsize=(12, 10), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Clean Axis
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    
    # Plot using a colormap that highlights the "Loop"
    # 'hsv' is good for cyclic things (hue wheel)
    ax.scatter(hist_m, hist_lam, hist_pm, c=colors, cmap='hsv', s=0.5, alpha=0.8)
    
    ax.set_xlabel('Mass Field (m)', color='white')
    ax.set_ylabel('Coupling (lambda)', color='white')
    ax.set_zlabel('Momentum (pm)', color='white')
    ax.tick_params(colors='white')
    
    # Title
    ax.set_title(f"The Fermion: Spin 1/2 Geometry\n(Twist = {TWIST})", color='white', fontsize=16)
    
    # Optimal View for the "Double Loop"
    ax.view_init(elev=20, azim=60)

    plt.tight_layout()
    plt.savefig('fermion_portrait.png')
    plt.show()

if __name__ == "__main__":
    run_fermion_vis()