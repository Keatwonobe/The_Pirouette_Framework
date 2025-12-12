import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

# ----------------------------------------
# FRACTAL CONFIGURATION
# ----------------------------------------
RES = 400            # Resolution (400x400 for speed/GIF size)
TWIST = 3.8          # The Standard Model Twist
GAMMA = 0.5          # The Critical Higgs Viscosity
DT = 0.015
STEPS = 1000         # Duration of the "Tumble"
FRAME_SKIP = 20      # Capture a frame every N steps

# Viewport
M_MIN, M_MAX = -2.5, 2.5
L_MIN, L_MAX = -2.5, 2.5

def get_force_vectorized(m, lam):
    # 1. Teal (EM)
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    # 2. Red (Weak)
    F_red_m = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    # 3. Gold (Strong)
    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    magnitude = np.sqrt(sum_m**2 + sum_lam**2)
    scaling_factor = np.sqrt(magnitude)
    F_gold_m = sum_m * scaling_factor
    F_gold_lam = sum_lam * scaling_factor
    
    # Weights
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
    
    return Fm, Flam, nw_red

def run_fractal_gif():
    print(f"[*] Initializing High-Res Simulation ({RES}x{RES})...")
    
    # Initialize Grid
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
    
    print(f"[*] Rendering Animation ({STEPS} steps, capturing every {FRAME_SKIP})...")
    
    for step in range(STEPS):
        # Physics Update
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        # Second Half-Step (Leapfrog-ish)
        Fm, Flam, w_red = get_force_vectorized(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        
        # Winding Calculation
        curr_ang = np.arctan2(lam, m)
        delta = curr_ang - prev_ang
        delta = np.where(delta > np.pi, delta - 2*np.pi, delta)
        delta = np.where(delta < -np.pi, delta + 2*np.pi, delta)
        total_ang += delta
        prev_ang = curr_ang
        
        # Capture Frame
        if step % FRAME_SKIP == 0 or step == STEPS - 1:
            # sys.stdout.write(f"\r    Frame {(step//FRAME_SKIP)+1} / {STEPS//FRAME_SKIP}")
            # sys.stdout.flush()
            
            # Construct Image
            winding = np.abs(total_ang) / (2*np.pi)
            fractal_map = winding.reshape(RES, RES)
            
            fig = plt.figure(figsize=(6, 6), facecolor='black')
            ax = fig.add_subplot(111)
            
            # We fix the scale (vmax=4) so the colors "fill in" as spin increases
            im = ax.imshow(fractal_map, extent=[M_MIN, M_MAX, L_MIN, L_MAX], 
                           origin='lower', cmap='nipy_spectral', vmin=0, vmax=4)
            
            ax.set_title(f"Fractal Genesis | Step {step}", color='white')
            ax.axis('off')
            
            # Save to buffer
            buf = io.BytesIO()
            plt.savefig(buf, format='png', facecolor='black')
            buf.seek(0)
            frames.append(Image.open(buf).copy())
            plt.close(fig)
            buf.close()

    print(f"\n[*] Compiling GIF...")
    frames[0].save('fractal_genesis.gif', save_all=True, append_images=frames[1:], 
                   optimize=True, duration=50, loop=0)
    print("✅ GIF Generated: fractal_genesis.gif")

if __name__ == "__main__":
    run_fractal_gif()