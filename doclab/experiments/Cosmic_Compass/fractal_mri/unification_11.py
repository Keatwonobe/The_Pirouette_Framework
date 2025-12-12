import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ----------------------------------------
# MESH CONFIGURATION
# ----------------------------------------
RES = 300            # Resolution for 3D mesh (300x300 is good for plotting)
TWIST = 3.8
GAMMA = 0.5
DT = 0.015
STEPS = 1200         # Duration

# Viewport
M_MIN, M_MAX = -2.5, 2.5
L_MIN, L_MAX = -2.5, 2.5

EPSILON = 1e-6 # For Lyapunov

def get_force_vectorized(m, lam):
    # Standard Model Soliton Physics
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # Non-linear Confinement
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    
    # Avoid div/0
    scaling_factor = np.sqrt(magnitude)
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Fast Gaussian
    diff_g = np.abs(np.degrees(np.arctan2(lam, m)) % 360 - 30)
    diff_g = np.minimum(diff_g, 360-diff_g)
    w_gold = np.exp(-(diff_g/80)**2)
    
    diff_t = np.abs(np.degrees(np.arctan2(lam, m)) % 360 - 150)
    diff_t = np.minimum(diff_t, 360-diff_t)
    w_teal = np.exp(-(diff_t/80)**2)
    
    diff_r = np.abs(np.degrees(np.arctan2(lam, m)) % 360 - 270)
    diff_r = np.minimum(diff_r, 360-diff_r)
    w_red = np.exp(-(diff_r/80)**2)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, nw_red

def run_topological_mesh():
    print(f"Building 3D Topology Mesh ({RES}x{RES})...")
    
    # 1. Initialize Grid
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    # Flatten
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    # Shadows for Lyapunov
    m_s = m + EPSILON
    lam_s = lam + EPSILON
    pm_s = np.zeros_like(m)
    plam_s = np.zeros_like(lam)
    
    # Metrics
    lyap_sum = np.zeros_like(m)
    total_ang = np.zeros_like(m)
    prev_ang = np.arctan2(lam, m)
    
    # 2. Integration
    for step in range(STEPS):
        # --- Main Trajectory ---
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
        
        # --- Shadow Trajectory ---
        Fm_s, Flam_s, w_red_s = get_force_vectorized(m_s, lam_s)
        drag_s = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red_s)
        
        pm_s = (pm_s + 0.5 * DT * Fm_s) * drag_s
        plam_s = (plam_s + 0.5 * DT * Flam_s) * drag_s
        m_s += DT * pm_s
        lam_s += DT * plam_s
        
        Fm_s, Flam_s, w_red_s = get_force_vectorized(m_s, lam_s)
        drag_s = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red_s)
        
        pm_s = (pm_s + 0.5 * DT * Fm_s) * drag_s
        plam_s = (plam_s + 0.5 * DT * Flam_s) * drag_s
        
        # --- Lyapunov Calculation ---
        dist = np.sqrt((m-m_s)**2 + (lam-lam_s)**2 + (pm-pm_s)**2 + (plam-plam_s)**2)
        dist = np.maximum(dist, 1e-15)
        rescale = EPSILON / dist
        lyap_sum += np.log(dist/EPSILON)
        
        # Pull shadow back
        m_s = m + (m_s - m) * rescale
        lam_s = lam + (lam_s - lam) * rescale
        pm_s = pm + (pm_s - pm) * rescale
        plam_s = plam + (plam_s - plam) * rescale
        
        # --- Spin Calculation ---
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        delta = np.where(delta > np.pi, delta - 2*np.pi, delta)
        delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)
        total_ang += delta
        prev_ang = curr_ang
        
        if step % 200 == 0: print(f"Step {step}/{STEPS}...")

    # 3. Data Formatting
    lyap_exp = lyap_sum / (STEPS * DT)
    spin = np.abs(total_ang) / (2*np.pi)
    
    # Reshape
    Z = lyap_exp.reshape(RES, RES)
    C = spin.reshape(RES, RES)
    
    # ----------------------------------------
    # 3D RENDER
    # ----------------------------------------
    fig = plt.figure(figsize=(14, 10), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    
    # Surface Plot
    # Z = Height (Chaos)
    # Facecolors = Spin
    
    # Normalize spin for colormap
    # We want to highlight integer steps. 
    # Use 'nipy_spectral' or 'hsv'
    norm = plt.Normalize(0, 4) 
    colors = plt.cm.nipy_spectral(norm(C))
    
    # Log scale Z for better visual peaks
    Z_log = np.log1p(Z)
    
    surf = ax.plot_surface(M, L, Z_log, facecolors=colors, 
                           rstride=2, cstride=2, # Downsample for rendering speed
                           linewidth=0, antialiased=False, shade=True)
    
    ax.set_title("The Topography of Existence\nHeight=Chaos, Color=Spin", color='white', fontsize=16)
    ax.set_xlabel('Mass Field', color='white')
    ax.set_ylabel('Coupling Field', color='white')
    ax.set_zlabel('Log Chaos (Lyapunov)', color='white')
    
    # Remove grid panes
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('#333333')
    ax.yaxis.pane.set_edgecolor('#333333')
    ax.zaxis.pane.set_edgecolor('#333333')
    ax.tick_params(colors='gray')
    
    # Standard Model View Angle
    ax.view_init(elev=45, azim=-45)
    
    plt.tight_layout()
    plt.savefig('fractal_topology_mesh.png')
    plt.show()

if __name__ == "__main__":
    run_topological_mesh()