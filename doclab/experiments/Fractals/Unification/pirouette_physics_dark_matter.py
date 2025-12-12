# unification_37_dark_matter.py
import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE PRESSURE TEST 1: THE GHOST SECTOR
# --------------------------------------------------
# We scan the "Gold Basin" (Strong Force Sector)
# to see if stable particles exist that have ZERO
# interaction with the Teal Field (Electromagnetism).
#
# If they exist, they have Mass (Stiffness) but no
# Charge (Teal Coupling). They are Dark Matter.
# --------------------------------------------------

# The Fundamental Constants we derived
TWIST = 2.83814 
GAMMA = 0.02
DT = 0.005
STEPS = 6000

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
    
    return Fm, Flam, nw_teal, nw_gold

def run_dark_matter_scan():
    print("Scanning the Ghost Sector (Gold Basin) for Invisible Matter...")
    
    # We scan the phase space, but we focus on the "Gold" sector (Angle ~ 30 deg)
    # Start points in the Gold Basin
    
    # Generate a grid of start points
    # We focus on the Gold quadrant (positive m, positive lam mostly)
    m_starts = np.linspace(1.0, 4.0, 15)
    l_starts = np.linspace(0.0, 3.0, 15)
    
    stable_particles = [] # Stores (m, lam, teal_coupling_avg)
    
    for start_m in m_starts:
        for start_l in l_starts:
            m, lam = start_m, start_l
            pm, plam = 0.0, 1.0 # Give it a kick
            
            # Tracking
            teal_coupling_sum = 0.0
            is_stable = True
            
            # Run simulation
            for step in range(STEPS):
                Fm, Flam, w_teal, w_gold = get_force_vectorized(m, lam)
                
                # Check for stability (if it flies off to infinity)
                if abs(m) > 10 or abs(lam) > 10:
                    is_stable = False
                    break
                
                # Accumulate "Tealness" (Visibility to Light)
                teal_coupling_sum += w_teal
                
                # Integration
                drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_gold) # Gold particles feel Gold drag
                pm = (pm + 0.5 * DT * Fm) * drag
                plam = (plam + 0.5 * DT * Flam) * drag
                m += DT * pm
                lam += DT * plam
                
                # Half step
                Fm, Flam, w_teal, w_gold = get_force_vectorized(m, lam)
                drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_gold)
                pm = (pm + 0.5 * DT * Fm) * drag
                plam = (plam + 0.5 * DT * Flam) * drag
            
            if is_stable:
                avg_teal = teal_coupling_sum / STEPS
                stable_particles.append({'pos': (m, lam), 'teal': avg_teal})

    print(f"Scan Complete. Found {len(stable_particles)} stable candidates.")
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(10, 8), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Plot the background basins for context
    # (Simplified visualization)
    
    # Plot the Candidates
    # Color them by "Visibility" (Teal Coupling)
    # Bright Cyan = Visible Matter
    # Dark Grey/Red = Dark Matter
    
    x_vals = [p['pos'][0] for p in stable_particles]
    y_vals = [p['pos'][1] for p in stable_particles]
    c_vals = [p['teal'] for p in stable_particles]
    
    sc = ax.scatter(x_vals, y_vals, c=c_vals, cmap='gray', s=100, edgecolors='lime')
    
    # Reference: The Electron (Visible)
    ax.scatter([-1.8], [0.0], color='cyan', s=200, marker='*', label='Standard Electron (Visible)')
    ax.text(-1.8, -0.3, "Visible Sector", color='cyan', ha='center')

    ax.set_title("Pressure Test 1: Search for Dark Matter\n(Darker Dots = Less Interaction with Light)", color='white', fontsize=14)
    ax.set_xlabel("Mass Field", color='white')
    ax.set_ylabel("Coupling Field", color='white')
    
    cbar = plt.colorbar(sc)
    cbar.set_label("Teal Coupling (Visibility)", color='white')
    cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
    
    ax.legend(facecolor='black', labelcolor='white')
    ax.grid(color='#333333', alpha=0.5)
    ax.tick_params(colors='white')
    
    plt.tight_layout()
    plt.savefig('dark_matter_scan.png')
    plt.show()

if __name__ == "__main__":
    run_dark_matter_scan()