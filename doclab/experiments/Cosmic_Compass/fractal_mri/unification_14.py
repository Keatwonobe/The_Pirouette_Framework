import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ----------------------------------------
# DOUBLE SLIT PARAMETERS
# ----------------------------------------
TWIST = 3.8
GAMMA = 0.5
DT = 0.015
STEPS = 4000

# Interaction Strength (Effective Gravity/EM)
G_EFF = 0.5 

def get_force_individual(m, lam):
    # Standard Model Soliton Physics (Tension Mode)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # Non-linear Confinement
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude) # F^1.5 scaling
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Basin Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Gaussian weights
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

def get_interaction_force(m1, l1, m2, l2):
    # Vector from 1 to 2
    dx = m2 - m1
    dy = l2 - l1
    dist_sq = dx**2 + dy**2 + 1e-6 # Softening
    dist = np.sqrt(dist_sq)
    
    # Phase Interaction (Constructive/Destructive)
    phi1 = np.arctan2(l1, m1)
    phi2 = np.arctan2(l2, m2)
    phase_factor = np.cos(phi1 - phi2)
    
    # Force Magnitude (Inverse Square + Phase Modulation)
    # If phase aligned (cos=1) -> Attraction
    # If anti-aligned (cos=-1) -> Repulsion
    f_mag = G_EFF * phase_factor / dist_sq
    
    fx = f_mag * (dx / dist)
    fy = f_mag * (dy / dist)
    
    return fx, fy

def run_double_slit():
    print("Initializing Double Slit Experiment...")
    
    # Initial Conditions (The Slits)
    # Start two particles slightly offset in the stable basin
    start_m, start_l = -0.5, 0.5
    offset = 0.2
    
    # Particle 1
    m1, l1 = start_m - offset, start_l
    pm1, pl1 = 0.9, 0.4
    
    # Particle 2
    m2, l2 = start_m + offset, start_l
    pm2, pl2 = 0.9, 0.4
    
    # History
    traj1_m, traj1_l = [], []
    traj2_m, traj2_l = [], []
    dist_hist = []
    phase_corr = []
    
    for _ in range(STEPS):
        # 1. Background Forces
        Fm1, Fl1, wr1 = get_force_individual(m1, l1)
        Fm2, Fl2, wr2 = get_force_individual(m2, l2)
        
        # 2. Interaction Forces
        # Force on 1 from 2
        Fint_x, Fint_y = get_interaction_force(m1, l1, m2, l2)
        
        # Total Forces
        # Particle 1 feels F1 + Interaction
        F_tot_m1 = Fm1 + Fint_x
        F_tot_l1 = Fl1 + Fint_y
        
        # Particle 2 feels F2 - Interaction (Newton's 3rd Law)
        F_tot_m2 = Fm2 - Fint_x
        F_tot_l2 = Fl2 - Fint_y
        
        # 3. Integration (Leapfrog with Drag)
        # Particle 1
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * wr1)
        pm1 = (pm1 + 0.5 * DT * F_tot_m1) * drag1
        pl1 = (pl1 + 0.5 * DT * F_tot_l1) * drag1
        m1 += DT * pm1
        l1 += DT * pl1
        
        # Particle 2
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * wr2)
        pm2 = (pm2 + 0.5 * DT * F_tot_m2) * drag2
        pl2 = (pl2 + 0.5 * DT * F_tot_l2) * drag2
        m2 += DT * pm2
        l2 += DT * pl2
        
        # Re-evaluate for second half-kick (Simplified: using old interaction for speed, or re-calc?)
        # Let's re-calc background, keep interaction const for half-step (approx)
        Fm1, Fl1, wr1 = get_force_individual(m1, l1)
        Fm2, Fl2, wr2 = get_force_individual(m2, l2)
        # Update interaction? Better precision if we do.
        Fint_x, Fint_y = get_interaction_force(m1, l1, m2, l2)
        
        F_tot_m1 = Fm1 + Fint_x
        F_tot_l1 = Fl1 + Fint_y
        F_tot_m2 = Fm2 - Fint_x
        F_tot_l2 = Fl2 - Fint_y
        
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * wr1)
        pm1 = (pm1 + 0.5 * DT * F_tot_m1) * drag1
        pl1 = (pl1 + 0.5 * DT * F_tot_l1) * drag1
        
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * wr2)
        pm2 = (pm2 + 0.5 * DT * F_tot_m2) * drag2
        pl2 = (pl2 + 0.5 * DT * F_tot_l2) * drag2
        
        # Record
        traj1_m.append(m1)
        traj1_l.append(l1)
        traj2_m.append(m2)
        traj2_l.append(l2)
        
        d = np.sqrt((m1-m2)**2 + (l1-l2)**2)
        dist_hist.append(d)
        
        # Phase correlation
        p1 = np.arctan2(l1, m1)
        p2 = np.arctan2(l2, m2)
        phase_corr.append(np.cos(p1-p2))

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), facecolor='black')
    
    # 1. Trajectories
    ax1.set_facecolor('black')
    # Plot P1
    ax1.plot(traj1_m, traj1_l, color='cyan', linewidth=1, alpha=0.8, label='Particle 1')
    # Plot P2
    ax1.plot(traj2_m, traj2_l, color='magenta', linewidth=1, alpha=0.8, label='Particle 2')
    
    # Plot "Interference" Connectors (draw lines between them occasionally)
    # visible 'web' of interaction
    skip = 50
    for i in range(0, len(traj1_m), skip):
        ax1.plot([traj1_m[i], traj2_m[i]], [traj1_l[i], traj2_l[i]], 
                 color='white', alpha=0.1, linewidth=0.5)
        
    ax1.set_title("Double Slit Trajectories (Phase Interaction)", color='white', fontsize=14)
    ax1.axis('equal')
    ax1.legend(facecolor='black', labelcolor='white')
    ax1.axis('off')
    
    # 2. Interaction Metrics
    ax2.set_facecolor('black')
    t = np.arange(STEPS) * DT
    
    # Separation Distance
    ax2.plot(t, dist_hist, color='lime', label='Separation Distance')
    
    # Phase Correlation (Scaled to fit)
    # +1 = In Phase (Attract), -1 = Out Phase (Repel)
    ax2.plot(t, np.array(phase_corr) + 2, color='yellow', alpha=0.5, label='Phase Correlation (+2 offset)')
    
    ax2.set_title("Interaction Dynamics", color='white', fontsize=14)
    ax2.set_xlabel("Time", color='white')
    ax2.legend(facecolor='black', labelcolor='white')
    ax2.grid(color='#333333', alpha=0.5)
    ax2.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('double_slit_interaction.png')
    plt.show()

if __name__ == "__main__":
    run_double_slit()