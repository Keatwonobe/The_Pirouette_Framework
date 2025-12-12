import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image
import io

# ----------------------------------------
# CONFIGURATION
# ----------------------------------------
RES = 120            # Resolution (Keep <150 for smooth 3D animation)
TWIST = 3.8
GAMMA = 0.5
DT = 0.02
STEPS = 120          # Total physics steps
FRAME_SKIP = 1     # Update plot every N steps
ZOOM = 12

# Viewport
M_MIN, M_MAX = -ZOOM, ZOOM
L_MIN, L_MAX = -ZOOM, ZOOM

def get_force_vectorized(m, lam):
    # The Unified Field (Teal/Red/Gold)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    scaling_factor = np.sqrt(np.sqrt(sum_m**2 + sum_lam**2))
    
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
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
    
    return Fm, Flam, nw_red

def run_growth_animation():
    print(f"[*] Initializing Topological Growth Simulation ({RES}x{RES})...")
    
    # Grid Setup
    m_range = np.linspace(M_MIN, M_MAX, RES)
    l_range = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_range, l_range)
    
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    prev_ang = np.arctan2(lam, m)
    total_ang = np.zeros_like(m)
    
    frames = []
    
    # Plot Setup
    fig = plt.figure(figsize=(15, 5), facecolor='black')
    
    # We use a 1x3 grid
    ax_top = fig.add_subplot(131, projection='3d')
    ax_angle = fig.add_subplot(132, projection='3d')
    ax_side = fig.add_subplot(133, projection='3d')
    
    axes = [ax_top, ax_angle, ax_side]
    
    print(f"[*] Simulating Growth ({STEPS} steps)...")
    
    for step in range(STEPS):
        # --- Physics Integration ---
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        # Winding Calc
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        delta = np.where(delta > np.pi, delta - 2*np.pi, delta)
        delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)
        total_ang += delta
        prev_ang = curr_ang
        
        # --- Rendering ---
        if step % FRAME_SKIP == 0:
            # Prepare Data
            winding = np.abs(total_ang) / (2*np.pi)
            Z = winding.reshape(RES, RES)
            
            # Clear Axes
            for ax in axes: ax.clear()
            
            # PLOT 1: Top View (The Map)
            ax_top.plot_surface(M, L, Z, cmap='nipy_spectral', rcount=RES, ccount=RES, shade=False)
            ax_top.view_init(elev=90, azim=-90) # Looking straight down
            ax_top.set_title("TOP VIEW (The Wound)", color='white')
            ax_top.axis('off')
            
            # PLOT 2: Angled View (The Structure)
            ax_angle.plot_surface(M, L, Z, cmap='nipy_spectral', rcount=RES, ccount=RES, shade=True)
            ax_angle.view_init(elev=45, azim=-45)
            ax_angle.set_title(f"GENESIS | Step {step}", color='white')
            ax_angle.axis('off')
            
            # PLOT 3: Side View (The Spike)
            ax_side.plot_surface(M, L, Z, cmap='nipy_spectral', rcount=RES, ccount=RES, shade=True)
            ax_side.view_init(elev=0, azim=-90) # Looking from the side
            ax_side.set_title("PROFILE (The Rise)", color='white')
            ax_side.axis('off')
            
            # Limit Z axis to keep scale consistent as it grows
            # Or let it grow naturally. Let's fix it slightly to prevent jumping.
            for ax in axes:
                ax.set_zlim(0, 4)
                ax.set_facecolor('black')
            
            plt.tight_layout()
            
            # Capture
            buf = io.BytesIO()
            plt.savefig(buf, format='png', facecolor='black')
            buf.seek(0)
            frames.append(Image.open(buf).copy())
            buf.close()

    print(f"[*] Compiling Multi-Angle GIF...")
    frames[0].save('vacuum_spike_multi_angle.gif', save_all=True, append_images=frames[1:], 
                   optimize=True, duration=60, loop=0)
    print("✅ Growth Animation Saved: vacuum_spike_multi_angle.gif")

if __name__ == "__main__":
    run_growth_animation()