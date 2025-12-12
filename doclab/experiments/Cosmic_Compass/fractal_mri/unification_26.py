import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE FRAMEWORK: POINCARE SECTION
# --------------------------------------------------
# Instead of drawing the chaotic "spaghetti," we slice
# through the phase space. We record a point only
# when the particle crosses the Lam=0 plane.
#
# Patterns we are looking for:
# - Scattered Dust = Chaos (Free Particle)
# - Closed Loops/Islands = Stable Matter (Resonance)
# --------------------------------------------------

TWIST = 3.8
# We use a slightly higher gamma to dampen the wildest chaos
# and reveal the "attractors" (stable states)
GAMMA = 0.05 
DT = 0.005
STEPS = 150000 

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

def run_poincare_map():
    print("Generating Poincare Section (Slicing the Chaos)...")
    
    # We will launch MULTIPLE particles with different energies
    # to map out the whole "skeleton" of the vacuum.
    start_energies = [0.1, 0.4, 0.7, 1.0, 1.3]
    colors = ['cyan', 'lime', 'yellow', 'orange', 'red']
    
    poincare_m = []
    poincare_pm = []
    poincare_c = []

    for i, start_vel in enumerate(start_energies):
        print(f"Scanning Energy Layer {i+1}/{len(start_energies)}...")
        
        # Start near the Teal basin
        m, lam = -0.8, 0.0 
        pm, plam = 0.0, start_vel 
        
        # History for crossing detection
        prev_lam = lam
        
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
            
            # --- POINCARE DETECTION ---
            # Did we cross the Lam=0 plane?
            # (Check if sign of lam changed)
            if (prev_lam < 0 and lam >= 0) or (prev_lam > 0 and lam <= 0):
                # Interpolate to find exact crossing point for precision
                # Linear interpolation: fraction f where crossing happened
                f = abs(prev_lam) / (abs(prev_lam) + abs(lam) + 1e-9)
                
                cross_m = m - (m - (m - DT*pm)) * (1-f) # Approx
                cross_pm = pm # Approx velocity at crossing
                
                poincare_m.append(cross_m)
                poincare_pm.append(cross_pm)
                poincare_c.append(colors[i])
            
            prev_lam = lam

    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(12, 8), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # Scatter plot of the crossings
    # X-axis = Position (m), Y-axis = Momentum (pm)
    ax.scatter(poincare_m, poincare_pm, c=poincare_c, s=1.5, alpha=0.6)
    
    ax.set_title("Poincaré Section: The Skeleton of Stability\n(Dots = Islands of Order, Void = Chaos)", 
                 color='white', fontsize=16)
    ax.set_xlabel("Position (Mass Field)", color='white')
    ax.set_ylabel("Momentum (Velocity)", color='white')
    
    ax.grid(color='#333333', alpha=0.4)
    ax.tick_params(colors='white')
    
    # Add annotation explaining the plot
    plt.figtext(0.5, 0.02, 
                "If you see RINGS or CLUSTERS, those are stable Particles.\nIf you see scattered dust, that is Chaos.", 
                ha="center", color="gray", fontsize=10)

    plt.tight_layout()
    plt.savefig('poincare_section.png')
    plt.show()

if __name__ == "__main__":
    run_poincare_map()