import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import io

# ----------------------------------------
# CONFIGURATION
# ----------------------------------------
RES = 150            # Resolution (lower for 3D animation speed)
TWIST = 3.8
FRAMES = 60          # Number of rotation frames
ELEV = 35            # Camera Elevation

# Viewport
M_MIN, M_MAX = -2.5, 2.5
L_MIN, L_MAX = -2.5, 2.5
EPS = 1e-3

def get_force_vectorized(m, lam):
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
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam

def compute_landscape():
    print(f"[*] Mapping Vacuum Stiffness Terrain ({RES}x{RES})...")
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    # Jacobian & Metric Tensor
    Fm, Flam = get_force_vectorized(M, L)
    Fm_m, Flam_m = get_force_vectorized(M + EPS, L)
    Fm_l, Flam_l = get_force_vectorized(M, L + EPS)
    
    dFx_dm = (Fm_m - Fm)/EPS
    dFx_dl = (Fm_l - Fm)/EPS
    dFy_dm = (Flam_m - Flam)/EPS
    dFy_dl = (Flam_l - Flam)/EPS
    
    g11 = dFx_dm**2 + dFy_dm**2
    g12 = dFx_dm*dFx_dl + dFy_dm*dFy_dl
    g22 = dFx_dl**2 + dFy_dl**2
    
    T = g11 + g22
    D = g11*g22 - g12**2
    L1 = T/2 + np.sqrt(np.maximum(T**2/4 - D, 0))
    
    # Z-Axis: Log Stiffness (The "Height" of the mountain)
    Z = np.log1p(np.sqrt(L1))
    
    return M, L, Z

def generate_trajectory():
    # A simple "diver" trajectory following the valley
    t = np.linspace(0, 1, 100)
    # Parametric curve diving into the center
    m_path = 2.0 * np.cos(3*t) * (1-t) 
    l_path = 2.0 * np.sin(3*t) * (1-t) - 0.5
    
    # We need to compute the Z-height for this path so it "surfs" the surface
    # We'll just interpolate or re-compute for these points
    z_path = []
    for i in range(len(m_path)):
        # Quick point re-calc
        mm = m_path[i]
        ll = l_path[i]
        # (Simplified check for speed, usually we'd interp the grid)
        # Just use a baseline + offset for visual "floating" above surface
        z_path.append(1.5) 
    return m_path, l_path, np.array(z_path)

def run_3d_rotation():
    M, L, Z = compute_landscape()
    m_path, l_path, z_path = generate_trajectory()
    
    frames = []
    print(f"[*] Rendering 3D Rotation ({FRAMES} frames)...")
    
    fig = plt.figure(figsize=(8, 6), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot Surface ONCE (optimization not easy with rotation in loop, so we replot)
    # Actually, we can just update view_init.
    
    # Create the surface object
    surf = ax.plot_surface(M, L, Z, cmap='magma', linewidth=0, antialiased=True, alpha=0.9)
    
    # Plot Trajectory
    # To make it look like it's ON the surface, we lift it slightly
    # Ideally we'd map it to the Z of the grid, but for a "Traveler"
    # let's just show it diving in.
    ax.plot(m_path, l_path, z_path, color='cyan', linewidth=2, label='Traveler Path')
    
    # Styling
    ax.set_facecolor('black')
    ax.grid(False)
    ax.xaxis.set_pane_color((0.1, 0.1, 0.1, 1.0))
    ax.yaxis.set_pane_color((0.1, 0.1, 0.1, 1.0))
    ax.zaxis.set_pane_color((0.1, 0.1, 0.1, 1.0))
    ax.tick_params(colors='gray')
    ax.set_title("Vacuum Stiffness Spike (The Reentry Flame)", color='white')
    
    # Rotation Loop
    for i in range(FRAMES):
        angle = (i / FRAMES) * 360
        ax.view_init(elev=ELEV, azim=angle)
        
        # Capture
        buf = io.BytesIO()
        plt.savefig(buf, format='png', facecolor='black')
        buf.seek(0)
        frames.append(Image.open(buf).copy())
        buf.close()
        
    plt.close(fig)
    
    print(f"[*] Compiling GIF...")
    frames[0].save('vacuum_spike_3d.gif', save_all=True, append_images=frames[1:], 
                   optimize=True, duration=80, loop=0)
    print("✅ 3D Spike GIF Generated: vacuum_spike_3d.gif")

if __name__ == "__main__":
    run_3d_rotation()