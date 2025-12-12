import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE FRAMEWORK: THE COLLIDER (FIXED)
# --------------------------------------------------
# FIXED: Added position integration for Particle 2.
# Now both electrons are free to move and scatter.
# --------------------------------------------------

TWIST = 2.83814 
GAMMA = 0.02
DT = 0.005
STEPS = 5000 # Increased steps to see the aftermath

# Interaction Strength
G_COUPLE = 0.8 

def get_force_individual(m, lam):
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

def get_interaction(m1, l1, m2, l2):
    dx = m2 - m1
    dy = l2 - l1
    dist_sq = dx**2 + dy**2 + 1e-6
    dist = np.sqrt(dist_sq)
    
    f_mag = G_COUPLE / dist_sq
    
    fx = f_mag * (dx / dist)
    fy = f_mag * (dy / dist)
    
    if dist < 0.2: # Soft Core
        fx *= 5.0
        fy *= 5.0
        
    return fx, fy

def run_collider_fixed():
    print("Re-Running Collision (Now with Physics!)...")
    
    # P1 (Left -> Right)
    m1, l1 = -3.5, 0.0
    pm1, pl1 = 1.0, 2.0 
    
    # P2 (Right -> Left)
    m2, l2 = 0.5, 0.0   
    pm2, pl2 = -1.0, 2.0 # Symmetric velocity
    
    traj1_m, traj1_l = [], []
    traj2_m, traj2_l = [], []
    dist_hist = []
    
    for _ in range(STEPS):
        Fm1, Fl1, w1 = get_force_individual(m1, l1)
        Fm2, Fl2, w2 = get_force_individual(m2, l2)
        
        Fx_int, Fy_int = get_interaction(m1, l1, m2, l2)
        
        F_tot_m1 = Fm1 - Fx_int
        F_tot_l1 = Fl1 - Fy_int
        
        F_tot_m2 = Fm2 + Fx_int
        F_tot_l2 = Fl2 + Fy_int
        
        # P1 Update
        drag1 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w1)
        pm1 = (pm1 + 0.5 * DT * F_tot_m1) * drag1
        pl1 = (pl1 + 0.5 * DT * F_tot_l1) * drag1
        m1 += DT * pm1
        l1 += DT * pl1
        
        # P2 Update (FIXED: Added Position Update)
        drag2 = 1.0 / (1.0 + 0.5 * DT * GAMMA * w2)
        pm2 = (pm2 + 0.5 * DT * F_tot_m2) * drag2
        pl2 = (pl2 + 0.5 * DT * F_tot_l2) * drag2
        m2 += DT * pm2
        l2 += DT * pl2
        
        traj1_m.append(m1); traj1_l.append(l1)
        traj2_m.append(m2); traj2_l.append(l2)
        
        d = np.sqrt((m1-m2)**2 + (l1-l2)**2)
        dist_hist.append(d)

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), facecolor='black')
    
    # 1. Trajectories
    ax1.set_facecolor('black')
    ax1.plot(traj1_m, traj1_l, color='cyan', linewidth=2, label='Electron A', alpha=0.9)
    ax1.plot(traj1_m[0], traj1_l[0], 'o', color='cyan')
    ax1.plot(traj1_m[-1], traj1_l[-1], '*', color='white', markersize=10)
    
    ax1.plot(traj2_m, traj2_l, color='magenta', linewidth=2, label='Electron B', alpha=0.9)
    ax1.plot(traj2_m[0], traj2_l[0], 'o', color='magenta')
    ax1.plot(traj2_m[-1], traj2_l[-1], '*', color='white', markersize=10)

    # Connect closest point
    min_dist_idx = np.argmin(dist_hist)
    ax1.plot([traj1_m[min_dist_idx], traj2_m[min_dist_idx]], 
             [traj1_l[min_dist_idx], traj2_l[min_dist_idx]], 
             color='yellow', linestyle='--', label='Closest Approach')

    ax1.set_title("Scattering Event: Two Free Particles", color='white', fontsize=14)
    ax1.legend(facecolor='black', labelcolor='white')
    ax1.grid(color='#333333', alpha=0.5)
    
    # 2. Distance Plot
    ax2.set_facecolor('black')
    ax2.plot(dist_hist, color='lime', linewidth=1.5)
    ax2.set_title(f"Interaction Distance (Min = {min(dist_hist):.3f})", color='white', fontsize=14)
    ax2.set_xlabel("Time Step", color='white')
    ax2.set_ylabel("Separation", color='white')
    ax2.grid(color='#333333', alpha=0.5)
    ax2.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('collider_fixed.png')
    plt.show()

if __name__ == "__main__":
    run_collider_fixed()