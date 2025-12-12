import numpy as np
import matplotlib.pyplot as plt

def get_force_tension_mode(m, lam):
    # --- The Physics of Necessity ---
    
    # 1. Teal (EM): Harmonic Attraction to (-0.866, 0.5)
    # The "Charge" anchor
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak): Parity Violated Attraction to (0, -1)
    # The "Chiral" anchor
    F_red_m = -(m - 0.0)
    p_violation = 1.2 * np.sin(m * 3) # Stronger twist to force the Spin-1/2 behavior
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong): The Emergent Tension
    # FIX: Removed the negative sign!
    # The force in the Gold sector is the vector sum of the other two 
    # pulling the particle back to the center.
    F_gold_m = (F_teal_m + F_red_m)
    F_gold_lam = (F_teal_lam + F_red_lam)
    
    # Basin Weighting (Where are we?)
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    def gaussian(x, mu, sig):
        diff = np.minimum(np.abs(x - mu), 360 - np.abs(x - mu))
        return np.exp(-(diff/sig)**2)

    # Wide basins for smooth "hand-off"
    w_gold = gaussian(angle, 30, 80)
    w_teal = gaussian(angle, 150, 80)
    w_red = gaussian(angle, 270, 80)
    
    tot = w_gold + w_teal + w_red + 1e-6
    
    # Total Force (Weighted Average)
    Fm = (w_teal * F_teal_m + w_red * F_red_m + w_gold * F_gold_m) / tot
    Flam = (w_teal * F_teal_lam + w_red * F_red_lam + w_gold * F_gold_lam) / tot
    
    return Fm, Flam

def leapfrog_tension(m, lam, pm, plam, dt):
    Fm, Flam = get_force_tension_mode(m, lam)
    
    pm_h = pm + 0.5 * dt * Fm
    plam_h = plam + 0.5 * dt * Flam
    
    m_n = m + dt * pm_h
    lam_n = lam + dt * plam_h
    
    Fm_n, Flam_n = get_force_tension_mode(m_n, lam_n)
    
    pm_n = pm_h + 0.5 * dt * Fm_n
    plam_n = plam_h + 0.5 * dt * Flam_n
    
    return m_n, lam_n, pm_n, plam_n

def run_spin_verification():
    dt = 0.015
    steps = 6000
    
    # Initial Condition: 
    # Start in the "Teal" zone, heading toward "Gold"
    m, lam = -0.5, 0.5
    pm, plam = 0.8, 0.4 # Good strong kick to ensure it orbits
    
    traj_m, traj_lam, traj_color = [], [], []
    
    # Spin Analysis Variables
    initial_state = np.array([m, lam, pm, plam])
    prev_angle = np.arctan2(lam, m)
    total_angle = 0.0
    lap_counter = 0
    
    print(f"{'Lap':<5} | {'Angle (deg)':<12} | {'State Mismatch':<15} | {'Interpretation'}")
    print("-" * 60)
    
    for i in range(steps):
        # Tracking
        traj_m.append(m)
        traj_lam.append(lam)
        
        # Color logic
        ang = np.degrees(np.arctan2(lam, m)) % 360
        if 210 < ang < 330: c = (1, 0.3, 0.3) # Red
        elif 330 < ang or ang < 90: c = (1, 0.8, 0) # Gold
        else: c = (0, 0.8, 0.8) # Teal
        traj_color.append(c)

        # Integrate
        m, lam, pm, plam = leapfrog_tension(m, lam, pm, plam, dt)
        
        # Winding Math
        curr_angle = np.arctan2(lam, m)
        delta = curr_angle - prev_angle
        # Unwrap
        if delta > np.pi: delta -= 2*np.pi
        if delta < -np.pi: delta += 2*np.pi
        
        total_angle += delta
        prev_angle = curr_angle
        
        # Check Lap Crossing
        current_laps = int(abs(total_angle) / (2*np.pi))
        if current_laps > lap_counter:
            lap_counter = current_laps
            
            # Check state match
            curr_state = np.array([m, lam, pm, plam])
            dist = np.linalg.norm(curr_state - initial_state)
            
            status = "Drifted"
            if dist < 1.5: status = "Close..."
            if dist < 0.5: status = "RESET!"
            
            print(f"{lap_counter:<5} | {np.degrees(total_angle):<12.1f} | {dist:<15.4f} | {status}")

    # Plot
    traj_m = np.array(traj_m)
    traj_lam = np.array(traj_lam)
    
    plt.figure(figsize=(9, 9), facecolor='black')
    
    # Plot segments
    points = np.array([traj_m, traj_lam]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    from matplotlib.collections import LineCollection
    lc = LineCollection(segments, colors=traj_color, linewidth=2, alpha=0.9)
    plt.gca().add_collection(lc)
    
    # Add Markers for the Anchor Points to visualize the "Tension"
    plt.scatter([-0.866], [0.5], color='cyan', marker='x', s=100, label='Teal Anchor')
    plt.scatter([0.0], [-1.0], color='red', marker='x', s=100, label='Red Anchor')
    # Note: No Gold Anchor plotted because it is EMERGENT!
    
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    plt.axis('off')
    plt.legend(loc='upper right', facecolor='black', labelcolor='white')
    plt.title(f"Corrected 'Tension Mode' Orbit\nTotal Winding: {abs(total_angle)/(2*np.pi):.2f}", color='white')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_spin_verification()