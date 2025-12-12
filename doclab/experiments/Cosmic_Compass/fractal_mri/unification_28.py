import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --------------------------------------------------
# PIROUETTE FRAMEWORK: THE 3D PARTICLE
# --------------------------------------------------
# We lift the 2D Limit Cycle into 3D Phase Space
# (Mass, Lambda, Momentum) to visualize the
# "Tube of Stability" (The Torus).
# --------------------------------------------------

TWIST = 3.8
GAMMA = 0.05
DT = 0.005
STEPS = 40000
STABILIZE = 10000

def get_force_vectorized(m, lam):
    # --- Standard Pirouette Physics ---
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude)
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
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

def run_3d_vis():
    print("Generating 3D Particle Structure...")
    
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
    
    for _ in range(STEPS):
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

    # ----------------------------------------
    # PLOTTING 3D
    # ----------------------------------------
    fig = plt.figure(figsize=(12, 10), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Remove pane background
    ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
    
    # Plot the "Tube"
    # We use segments to color by "time" or just uniform gold
    ax.plot(hist_m, hist_lam, hist_pm, color='gold', linewidth=0.8, alpha=0.6)
    
    # Axis labels
    ax.set_xlabel('Mass Field (m)', color='white')
    ax.set_ylabel('Coupling (lambda)', color='white')
    ax.set_zlabel('Momentum (pm)', color='white')
    
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')
    ax.grid(color='#333333', linestyle=':', linewidth=0.5)

    ax.set_title("The Soliton: A Stable Torus in Phase Space", color='white', fontsize=16)
    
    # View Angle
    ax.view_init(elev=30, azim=45)

    plt.tight_layout()
    plt.savefig('particle_3d_torus.png')
    plt.show()

if __name__ == "__main__":
    run_3d_vis()