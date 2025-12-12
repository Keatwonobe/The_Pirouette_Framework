import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.gridspec import GridSpec
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap

# ======================
# CONFIGURATION
# ======================
RES = 600               # Resolution of the substrate
FRAMES = 160            # Duration (approx 8 seconds)
FPS = 20
CMB_ZOOM = 2.0          # Field of view

print("=" * 60)
print("P I R O U E T T E   E N G I N E   -   T R A V E L E R   K N O T")
print("=" * 60)

# ======================
# 1. SUBSTRATE GENERATION (Wada Basins)
# ======================
def generate_substrate(res):
    print(f"[*] Generating Cosmic Substrate ({res}x{res})...")
    m = np.linspace(-2.0, 2.0, res)
    l = np.linspace(-2.0, 2.0, res)
    M, L = np.meshgrid(m, l)
    
    # Fast Hénon-Heiles Basin Map
    iterations = 15
    dt = 0.1
    m_cur, l_cur = M.copy(), L.copy()
    pm, pl = np.zeros_like(M), np.zeros_like(L)
    active = np.ones_like(M, dtype=bool)
    basin = np.zeros_like(M, dtype=int)
    
    for _ in range(iterations):
        dm = m_cur + 2 * m_cur * l_cur
        dl = l_cur + (m_cur**2 - l_cur**2)
        pm -= dm * dt
        pl -= dl * dt
        m_cur += pm * dt
        l_cur += pl * dt
        r2 = m_cur**2 + l_cur**2
        escaped = (r2 > 10.0) & active
        if np.any(escaped):
            angle = np.arctan2(l_cur[escaped], m_cur[escaped])
            b_ids = np.zeros_like(angle, dtype=int)
            # Map escape angles to basins
            b_ids[(angle > 0.5) & (angle < 2.5)] = 1       # Red (Top)
            b_ids[(angle > 2.5) | (angle < -2.5)] = 2      # Teal (Left)
            b_ids[(angle > -2.5) & (angle < 0.5)] = 3      # Gold (Right)
            basin[escaped] = b_ids
            active[escaped] = False
            
    # Colorize
    img = np.zeros((res, res, 4))
    # Colors: Void (Black), Red, Teal, Gold
    img[basin==0] = [0, 0, 0, 1] 
    img[basin==1] = [0.8, 0.2, 0.2, 0.3] # Red (faint)
    img[basin==2] = [0.0, 0.8, 0.8, 0.3] # Teal (faint)
    img[basin==3] = [0.8, 0.6, 0.0, 0.3] # Gold (faint)
    
    # Add "Stars" (Random noise for CMB texture)
    noise = np.random.rand(res, res)
    img[..., 3] += noise * 0.1
    
    print("[✓] Substrate ready.")
    return img

# ======================
# 2. TRAJECTORY ENGINE
# ======================
def calculate_trajectories(t_prog):
    """
    Calculates the positions of Traveler 1 and 2 based on the narrative.
    t_prog: 0.0 to 1.0
    """
    # Phase 1: The Approach (0.0 - 0.3)
    # Bottom corners -> Center Bottom
    if t_prog < 0.3:
        p = t_prog / 0.3
        # Start at (-1.5, -1.5) and (1.5, -1.5)
        # Meet at (0, -0.5)
        x1 = -1.5 * (1-p) + (-0.2) * p
        y1 = -1.5 * (1-p) + (-0.5) * p
        
        x2 = 1.5 * (1-p) + (0.2) * p
        y2 = -1.5 * (1-p) + (-0.5) * p
        
        scale_text = "MACRO"
        scale_val = 1.0

    # Phase 2: The Ascent (0.3 - 0.6)
    # Center Bottom -> Top Vertex (The "Sharp Turn")
    elif t_prog < 0.6:
        p = (t_prog - 0.3) / 0.3
        # Swing out slightly then up
        angle1 = -np.pi/2 + p * (np.pi * 0.8) # Swing left-up
        angle2 = -np.pi/2 - p * (np.pi * 0.8) # Swing right-up
        
        r = 0.5 + 1.0 * p # Radius grows as they ascend to the top
        
        # Center of rotation shifts upwards
        cx, cy = 0.0, -0.5 + 1.5 * p
        
        x1 = cx + 0.3 * np.cos(angle1 * 3) # Wobbly ascent
        y1 = cy + 0.3 * np.sin(angle1 * 3)
        
        x2 = cx - 0.3 * np.cos(angle1 * 3)
        y2 = cy + 0.3 * np.sin(angle1 * 3)
        
        scale_text = "MESO"
        scale_val = 1e-5

    # Phase 3: The Collapse (0.6 - 1.0)
    # Top Vertex -> Center Void (The Trefoil Dive)
    else:
        p = (t_prog - 0.6) / 0.4
        
        # They are now "falling" into the singularity
        # We model a Trefoil Knot projection
        
        # Speed increases (Frequency rises)
        t_fast = p * 8 * np.pi 
        
        # Radius shrinks
        r_decay = 1.0 * (1 - p)
        
        # Trefoil Parametric (2D Projection)
        # x = r * (sin(t) + 2sin(2t))
        # y = r * (cos(t) - 2cos(2t))
        
        # Traveler 1
        x1 = r_decay * 0.3 * (np.sin(t_fast) + 2*np.sin(2*t_fast))
        y1 = r_decay * 0.3 * (np.cos(t_fast) - 2*np.cos(2*t_fast)) + 1.0 * (1-p) # Offset starts high, drops to 0
        
        # Traveler 2 (Phase shifted by PI)
        x2 = r_decay * 0.3 * (np.sin(t_fast + np.pi) + 2*np.sin(2*(t_fast + np.pi)))
        y2 = r_decay * 0.3 * (np.cos(t_fast + np.pi) - 2*np.cos(2*(t_fast + np.pi))) + 1.0 * (1-p)
        
        scale_text = "QUANTUM"
        scale_val = 1e-15 * (1/(1-p+0.01))

    return (x1, y1), (x2, y2), scale_text, scale_val

# ======================
# 3. VISUALIZATION
# ======================
def create_knot_animation():
    img_data = generate_substrate(RES)
    
    # Layout: 
    # Top Row: Traveler 1 View | Traveler 2 View
    # Bottom Row: Main CMB View
    fig = plt.figure(figsize=(10, 12), facecolor='#050505')
    gs = GridSpec(3, 2, height_ratios=[1, 3, 0.5]) # Top views, Main view, HUD space
    
    # -- VIEWS --
    ax_t1 = fig.add_subplot(gs[0, 0])
    ax_t2 = fig.add_subplot(gs[0, 1])
    ax_main = fig.add_subplot(gs[1, :])
    ax_hud = fig.add_subplot(gs[2, :])
    
    # Styling
    for ax in [ax_t1, ax_t2, ax_hud]:
        ax.set_facecolor('black')
        ax.axis('off')
    
    ax_main.axis('off')
    
    # History Trails
    trail1_x, trail1_y = [], []
    trail2_x, trail2_y = [], []
    
    def update(frame):
        t = frame / FRAMES
        (x1, y1), (x2, y2), s_txt, s_val = calculate_trajectories(t)
        
        # Update Trails
        trail1_x.append(x1); trail1_y.append(y1)
        trail2_x.append(x2); trail2_y.append(y2)
        # Keep trail length manageable
        if len(trail1_x) > 40: 
            trail1_x.pop(0); trail1_y.pop(0)
            trail2_x.pop(0); trail2_y.pop(0)
            
        # --- MAIN VIEW (CMB) ---
        ax_main.clear()
        ax_main.axis('off')
        
        # Background
        ax_main.imshow(img_data, extent=[-2, 2, -2, 2], origin='lower')
        
        # Plot Travelers
        # T1 = Cyan, T2 = Magenta
        ax_main.plot(trail1_x, trail1_y, color='cyan', linewidth=2, alpha=0.6)
        ax_main.plot(trail2_x, trail2_y, color='magenta', linewidth=2, alpha=0.6)
        
        # Heads (Glowing)
        ax_main.scatter([x1], [y1], color='cyan', s=100, edgecolors='white', zorder=10)
        ax_main.scatter([x2], [y2], color='magenta', s=100, edgecolors='white', zorder=10)
        
        # Connecting Line (The "Wound Channel" Tension)
        ax_main.plot([x1, x2], [y1, y2], color='white', linestyle='--', linewidth=1, alpha=0.5)
        
        ax_main.set_xlim(-2, 2)
        ax_main.set_ylim(-2, 2)
        ax_main.set_title("THE COSMIC MICROWAVE BACKGROUND", color='gray', fontsize=10, pad=10)

        # --- TRAVELER VIEWS (Relative "Targeting") ---
        # Perspective of T1 looking at T2
        ax_t1.clear(); ax_t1.axis('off'); ax_t1.set_facecolor('black')
        ax_t1.set_xlim(-1, 1); ax_t1.set_ylim(-1, 1)
        
        # Relative position
        rel_x = x2 - x1
        rel_y = y2 - y1
        dist = np.sqrt(rel_x**2 + rel_y**2)
        
        # Draw "Target"
        ax_t1.scatter([0], [0], color='cyan', s=20, marker='+') # Self crosshair
        ax_t1.scatter([rel_x], [rel_y], color='magenta', s=50 + 100/dist) # Target grows as it gets closer
        ax_t1.plot([0, rel_x], [0, rel_y], color='magenta', alpha=0.3)
        ax_t1.text(0.05, 0.9, "TRAVELER 1 FEED", color='cyan', transform=ax_t1.transAxes, fontsize=8)

        # Perspective of T2 looking at T1
        ax_t2.clear(); ax_t2.axis('off'); ax_t2.set_facecolor('black')
        ax_t2.set_xlim(-1, 1); ax_t2.set_ylim(-1, 1)
        ax_t2.scatter([0], [0], color='magenta', s=20, marker='+')
        ax_t2.scatter([-rel_x], [-rel_y], color='cyan', s=50 + 100/dist)
        ax_t2.plot([0, -rel_x], [0, -rel_y], color='cyan', alpha=0.3)
        ax_t2.text(0.05, 0.9, "TRAVELER 2 FEED", color='magenta', transform=ax_t2.transAxes, fontsize=8)

        # --- HUD METRICS ---
        ax_hud.clear(); ax_hud.axis('off')
        
        wound_thick = dist * 0.1
        freq = 3e8 / (dist + 1e-9)
        
        hud_text = f"""
        SCALE DOMAIN: {s_txt}
        SEPARATION:   {dist:.2e} m
        FREQUENCY:    {freq:.2e} Hz
        WOUND THICK:  {wound_thick:.2e} m
        STATUS:       {'COLLAPSING' if t > 0.6 else 'APPROACHING'}
        """
        ax_hud.text(0.5, 0.5, hud_text, color='lime', fontfamily='monospace', 
                   ha='center', va='center', fontsize=10)
        
        return ax_main, ax_t1, ax_t2, ax_hud

    print(f"[*] Rendering Animation ({FRAMES} frames)...")
    anim = FuncAnimation(fig, update, frames=FRAMES, interval=50)
    anim.save('traveler_knot_collapse.gif', writer=PillowWriter(fps=FPS))
    print("[✓] Saved to 'traveler_knot_collapse.gif'")

if __name__ == "__main__":
    create_knot_animation()