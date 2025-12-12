import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
import io

# =========================================================
#  PROTON BRAID: COLLISION ANIMATION (-30 to 30)
# =========================================================

# Parameters
TWIST = 3.8
ZOOM = 0.2
M_MIN, M_MAX = -ZOOM, ZOOM
L_MIN, L_MAX = -ZOOM, ZOOM
RES = 400  # Reduced slightly for GIF generation speed (60 frames)
DT_MAG = 0.005

def get_force(m, lam):
    # Unified Field Laws (Same as before)
    F_teal_m   = -(m + 0.866)
    F_teal_lam = -(lam - 0.5)

    F_red_m   = -(m - 0.0)
    p_violation = TWIST * np.sin(m * 2.5)
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m   = F_teal_m   + F_red_m
    sum_lam = F_teal_lam + F_red_lam
    mag     = np.sqrt(sum_m**2 + sum_lam**2)
    scale   = np.sqrt(mag)

    F_gold_m   = sum_m   * scale
    F_gold_lam = sum_lam * scale

    angle_deg = np.degrees(np.arctan2(lam, m)) % 360.0

    # Mixing weights
    diff_g = np.minimum(np.abs(angle_deg - 30.0), 360.0 - np.abs(angle_deg - 30.0))
    w_gold = np.exp(-(diff_g / 40.0)**2)

    diff_t = np.minimum(np.abs(angle_deg - 150.0), 360.0 - np.abs(angle_deg - 150.0))
    w_teal = np.exp(-(diff_t / 40.0)**2)

    diff_r = np.minimum(np.abs(angle_deg - 270.0), 360.0 - np.abs(angle_deg - 270.0))
    w_red  = np.exp(-(diff_r / 40.0)**2)

    tot = w_gold + w_teal + w_red + 1e-6
    nw_red  = w_red  / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot

    Fm   = nw_teal * F_teal_m   + nw_red * F_red_m   + nw_gold * F_gold_m
    Flam = nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam

    return Fm, Flam

def run_simulation(dt, steps):
    # Setup Grid
    m_vals = np.linspace(M_MIN, M_MAX, RES)
    l_vals = np.linspace(L_MIN, L_MAX, RES)
    M, L = np.meshgrid(m_vals, l_vals)
    
    m = M.copy()
    l = L.copy()
    
    trajectory_length = np.zeros_like(M)
    active = np.ones_like(M, dtype=bool)
    
    # Integration
    for t in range(steps):
        Fm1, Flam1 = get_force(m[active], l[active])
        
        m_pred = m[active] + Fm1 * dt
        l_pred = l[active] + Flam1 * dt
        
        Fm2, Flam2 = get_force(m_pred, l_pred)
        
        dm = 0.5 * (Fm1 + Fm2) * dt
        dl = 0.5 * (Flam1 + Flam2) * dt
        
        m[active] += dm
        l[active] += dl
        
        step_dist = np.sqrt(dm**2 + dl**2)
        trajectory_length[active] += step_dist
        
        # We don't remove active particles to ensure consistent visualization
        # just like the original script logic
        
    return np.log1p(trajectory_length)

def create_frame(data, step_label, title_color='white'):
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')
    
    # Colormap
    colors = [(0, 0, 0), (0.1, 0.1, 0.4), (0, 0.8, 0.8), (1, 1, 1)]
    cmap = LinearSegmentedColormap.from_list("abyss", colors, N=256)
    
    # Plot
    # We fix vmax slightly to avoid extreme flickering, based on approx max values
    # Max steps 30 -> length ~ 0.15 -> log1p ~ 0.14
    # But some particles move fast. Let's stick to auto-scaling but with fixed vmin.
    im = ax.imshow(data, origin='lower', cmap=cmap, extent=[M_MIN, M_MAX, L_MIN, L_MAX], vmin=0)
    
    ax.set_title(f"IMPACT EVENT | T = {step_label}", color=title_color, fontsize=12)
    ax.axis('off')
    
    # Save to buffer
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# =========================================================
#  GENERATE GIF FRAMES
# =========================================================
frames = []

print("[*] Generating Approach (Void) Frames -30 to -1...")
# Loop 30 down to 1
for i in range(30, 0, -1):
    # Reverse Simulation (Negative DT)
    data = run_simulation(-DT_MAG, i)
    frame = create_frame(data, f"-{i} (Void Incoming)")
    frames.append(frame)

print("[*] Generating Departure (Chaos) Frames 1 to 30...")
# Loop 1 to 30
for i in range(1, 31):
    # Forward Simulation (Positive DT)
    data = run_simulation(DT_MAG, i)
    frame = create_frame(data, f"+{i} (Chaos Ejecting)")
    frames.append(frame)

# Save GIF
print("[*] Saving GIF...")
frames[0].save(
    "proton_collision_impact.gif",
    save_all=True,
    append_images=frames[1:],
    optimize=False,
    duration=100, # 100ms per frame = 10 fps
    loop=0
)
print("✅ GIF Generated: proton_collision_impact.gif")