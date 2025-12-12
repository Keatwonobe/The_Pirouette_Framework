import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
TWIST_FACTOR = 3.0  # High Asymmetry (Breaking the Boson)
DT = 0.015
STEPS = 15000       # Increased steps to capture the larger orbit

def get_force_genesis(m, lam):
    # 1. Teal (EM)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak) - High Twist
    F_red_m = -(m - 0.0)
    p_violation = TWIST_FACTOR * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong) - Tension Mode (Free Rule)
    # F_gold = F_teal + F_red (Vector Sum/Tension)
    F_gold_m = (F_teal_m + F_red_m)
    F_gold_lam = (F_teal_lam + F_red_lam)
    
    # Basin Weighting
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360 - np.abs(x - mu))
        return np.exp(-(diff/sig)**2)

    w_gold = gaussian(angle, 30, 80)
    w_teal = gaussian(angle, 150, 80)
    w_red = gaussian(angle, 270, 80)
    
    tot = w_gold + w_teal + w_red + 1e-6
    
    # Total Force
    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    
    return Fm, Flam

def leapfrog_genesis(m, lam, pm, plam, dt):
    Fm, Flam = get_force_genesis(m, lam)
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    Fm_n, Flam_n = get_force_genesis(m_n, lam_n)
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    return m_n, lam_n, pm_n, plam_n

def run_genesis_zoom():
    m, lam = -0.5, 0.5
    pm, plam = 0.9, 0.4 
    
    initial_state = np.array([m, lam, pm, plam])
    
    traj_m, traj_lam, traj_color = [], [], []
    prev_angle = np.arctan2(lam, m)
    total_angle = 0.0
    
    print(f"SIMULATING GENESIS (Zoomed Out)")
    
    for i in range(STEPS):
        traj_m.append(m)
        traj_lam.append(lam)
        
        # Color logic
        ang = np.degrees(np.arctan2(lam, m)) % 360
        if 210 < ang < 330: c = (1, 0.3, 0.3)
        elif 330 < ang or ang < 90: c = (1, 0.8, 0)
        else: c = (0, 0.8, 0.8)
        traj_color.append(c)

        m, lam, pm, plam = leapfrog_genesis(m, lam, pm, plam, DT)
        
        # Angle Tracking
        curr_angle = np.arctan2(lam, m)
        delta = curr_angle - prev_angle
        if delta > np.pi: delta -= 2*np.pi
        if delta < -np.pi: delta += 2*np.pi
        total_angle += delta
        prev_angle = curr_angle

    # Plot
    traj_m = np.array(traj_m)
    traj_lam = np.array(traj_lam)
    
    plt.figure(figsize=(10, 10), facecolor='black')
    
    points = np.array([traj_m, traj_lam]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    from matplotlib.collections import LineCollection
    # Thinner line alpha to see overlaps
    lc = LineCollection(segments, colors=traj_color, linewidth=1.0, alpha=0.7)
    plt.gca().add_collection(lc)
    
    plt.scatter([-0.866], [0.5], color='cyan', marker='x', s=50, label='Teal Anchor')
    plt.scatter([0.0], [-1.0], color='red', marker='x', s=50, label='Red Anchor')
    
    # Auto-Scale logic with a bit of padding
    margin = 1.0
    plt.xlim(traj_m.min() - margin, traj_m.max() + margin)
    plt.ylim(traj_lam.min() - margin, traj_lam.max() + margin)
    
    plt.axis('equal') # Keep aspect ratio circular
    plt.axis('off')
    
    winding = abs(total_angle)/(2*np.pi)
    plt.title(f"Broken Boson Topology (Twist={TWIST_FACTOR})\nWinding: {winding:.2f}", color='white')
    plt.legend(facecolor='black', labelcolor='white')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_genesis_zoom()