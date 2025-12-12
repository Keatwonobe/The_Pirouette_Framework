import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------
# PARAMETERS
# ----------------------------------------
RES = 800
TWIST = 3.8
GAMMA = 0.11  # Standard Model Viscosity
# Viewport
M_MIN, M_MAX = -3.0, 3.0
L_MIN, L_MAX = -3.0, 3.0

def get_force_vectorized(m, lam):
    # Standard Physics
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # Gold = Squeezed Vector Sum
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude) # F^1.5
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Weights
    angle = np.degrees(np.arctan2(lam, m)) % 360
    
    # Fast Gaussian
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
    
    # Total Force
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam

def calculate_stiffness_map():
    print(f"Mapping Vacuum Stiffness (Mass Coupling)...")
    
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    # Numerical Derivative (Jacobian)
    EPS = 1e-4
    
    Fm, Flam = get_force_vectorized(M, L)
    
    Fm_dm, Flam_dm = get_force_vectorized(M + EPS, L)
    Fm_dl, Flam_dl = get_force_vectorized(M, L + EPS)
    
    # Derivatives
    dFm_dm = (Fm_dm - Fm) / EPS
    dFlam_dl = (Flam_dl - Flam) / EPS
    
    # Total Stiffness = Magnitude of the Divergence/Curl
    # Roughly: How much does the force change if I move slightly?
    # This is the "Grit" of the sandpaper.
    stiffness = np.sqrt(dFm_dm**2 + dFlam_dl**2)
    
    return M, L, stiffness

def run_coupling_map():
    M, L, stiffness = calculate_stiffness_map()
    
    # Particles identified in previous run (Approximate Coords)
    # Teal (Light): (-0.90, 0.81)
    # Red (Medium): (-0.21, -0.60)
    # Gold (Heavy): (2.46, 1.74)
    particles = [
        {'label': 'Teal (Light)', 'pos': (-0.90, 0.81), 'color': 'cyan'},
        {'label': 'Red (Med)',    'pos': (-0.21, -0.60), 'color': 'red'},
        {'label': 'Gold (Heavy)', 'pos': (2.46, 1.74),   'color': 'gold'},
    ]
    
    # ----------------------------------------
    # PLOTTING
    # ----------------------------------------
    plt.figure(figsize=(12, 10), facecolor='black')
    ax = plt.gca()
    
    # Log scale for dynamic range
    stiffness_log = np.log1p(stiffness)
    
    # Use 'copper' or 'gist_earth' to look like terrain/grit
    im = plt.imshow(stiffness_log, extent=[M_MIN, M_MAX, L_MIN, L_MAX], 
               origin='lower', cmap='gist_earth')
    
    # Overlay Particles
    for p in particles:
        mx, my = p['pos']
        plt.scatter(mx, my, color=p['color'], s=100, marker='o', edgecolors='white', linewidth=2)
        plt.text(mx+0.2, my, p['label'], color='white', fontsize=12, fontweight='bold')
        
    plt.title(f"The Texture of Mass: Vacuum Stiffness Map\n(Brighter = Rougher = Heavier)", 
              color='white', fontsize=16)
    plt.xlabel("Mass Field", color='white')
    plt.ylabel("Coupling Field", color='white')
    plt.tick_params(colors='white')
    
    cbar = plt.colorbar(im)
    cbar.set_label("Local Coupling Strength (Stiffness)", color='white')
    cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
    
    plt.tight_layout()
    plt.savefig('fractal_coupling_map.png')
    plt.show()

if __name__ == "__main__":
    run_coupling_map()