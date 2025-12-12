import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------
# PIROUETTE FRAMEWORK: THE ELECTRON FIELD
# --------------------------------------------------
# We zoom in on the "Fermion" coordinates and map
# the surrounding vector field.
#
# If this is a charged particle, we should see
# a Dipole Pattern (Field lines looping out/in).
# --------------------------------------------------

# The Fundamental Constant we found
TWIST = 2.83814 

# Zoom Window (Centered on the Particle at m ~ -1.8)
M_MIN, M_MAX = -2.5, -1.1
L_MIN, L_MAX = -0.7, 0.7
RES = 400

def get_force_vectorized(m, lam):
    # --- Standard Pirouette Physics (Tuned) ---
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

def run_field_vis():
    print("Mapping the Electron's Electric/Magnetic Field...")
    
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    # Get the Flow Vectors (The Field)
    Fm, Flam, w_red = get_force_vectorized(M, L)
    
    # Calculate Field Magnitude (Potential)
    Mag = np.sqrt(Fm**2 + Flam**2)
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    fig = plt.figure(figsize=(12, 10), facecolor='black')
    ax = plt.gca()
    ax.set_facecolor('black')
    
    # 1. The Potential Gradient (Background)
    # Log scale to see the subtle field lines
    im = ax.imshow(np.log1p(Mag), extent=[M_MIN, M_MAX, L_MIN, L_MAX], 
                   origin='lower', cmap='inferno', alpha=0.8)
    
    # 2. The Field Lines (Streamplot)
    # Cyan lines = The flow of the vacuum around the charge
    strm = ax.streamplot(M, L, Fm, Flam, color='cyan', density=2.0, 
                         linewidth=0.8, arrowsize=1.0, arrowstyle='->')
    
    # 3. The Particle Core (Approximate location)
    # We draw the "Knot" size
    circle = plt.Circle((-1.8, 0.0), 0.2, color='white', fill=False, linewidth=2, linestyle='--')
    ax.add_patch(circle)
    ax.text(-1.8, 0.0, "e-", color='white', fontsize=20, ha='center', va='center', fontweight='bold')

    ax.set_title("The Aura of Matter: Local Field Geometry\n(Twist = 2.83814)", color='white', fontsize=16)
    ax.set_xlabel("Mass Field", color='white')
    ax.set_ylabel("Coupling Field", color='white')
    
    ax.tick_params(colors='white')
    ax.grid(False)
    
    plt.tight_layout()
    plt.savefig('electron_field_lines.png')
    plt.show()

if __name__ == "__main__":
    run_field_vis()