import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.gridspec import GridSpec

# ======================
# CONFIGURATION
# ======================
RES = 500               # Resolution of the Wada background
FRAMES = 180            # Duration (9 seconds)
FPS = 20

print("=" * 60)
print("P I R O U E T T E   E N G I N E   -   T H E   I N E V I T A B L E   K N O T")
print("=" * 60)

# ======================
# 1. SUBSTRATE GENERATION (Wada Basins)
# ======================
def generate_wada_substrate(res):
    print(f"[*] Generating Wada Substrate ({res}x{res})...")
    m = np.linspace(-2.2, 2.2, res)
    l = np.linspace(-2.2, 2.2, res)
    M, L = np.meshgrid(m, l)
    
    # Hénon-Heiles Dynamics
    iterations = 18
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
            # Map basins
            b_ids[(angle > 0.5) & (angle < 2.5)] = 1       # Red (Top)
            b_ids[(angle > 2.5) | (angle < -2.5)] = 2      # Teal (Left)
            b_ids[(angle > -2.5) & (angle < 0.5)] = 3      # Gold (Right)
            basin[escaped] = b_ids
            active[escaped] = False
            
    # Colorize for the "Cosmic Void" look
    img = np.zeros((res, res, 4))
    
    # Void (The Stability Island) = Deep Black/Blue
    img[basin==0] = [0.02, 0.02, 0.05, 1.0] 
    
    # The Escape Basins (Muted colors to let travelers pop)
    img[basin==1] = [0.4, 0.1, 0.1, 1.0] # Red-ish
    img[basin==2] = [0.1, 0.4, 0.4, 1.0] # Teal-ish
    img[basin==3] = [0.4, 0.3, 0.0, 1.0] # Gold-ish
    
    # Add subtle noise (CMB Texture)
    noise = np.random.rand(res, res) * 0.05
    img[..., :3] += noise[..., np.newaxis]
    
    print("[✓] Substrate Generated.")
    return img

# ======================
# 2. TRAJECTORY ENGINE (The Choreography)
# ======================
def get_positions(progress):
    """
    Calculates positions for T1 and T2 based on the narrative curve.
    progress: 0.0 to 1.0
    """
    
    # PHASE 1: THE APPROACH (0.0 to 0.4)
    # They enter from bottom corners and race to the bottom center
    if progress < 0.4:
        t = progress / 0.4
        # Linear approach with slight ease-out
        p = t 
        
        # Start at corners, end at center-bottom crossing point
        # T1 (Left -> Right)
        x1 = -1.8 * (1-p) + (-0.2) * p
        y1 = -1.8 * (1-p) + (-0.8) * p
        
        # T2 (Right -> Left)
        x2 = 1.8 * (1-p) + (0.2) * p
        y2 = -1.8 * (1-p) + (-0.8) * p
        
        status = "APPROACHING"
        scale_label = "MACRO (1m)"

    # PHASE 2: THE TURN (0.4 to 0.6)
    # They pass, miss, and are whipped upwards
    elif progress < 0.6:
        t = (progress - 0.4) / 0.2
        
        # The Turn: A parabolic swing up the center
        # T1 swings from x=-0.2 to x=-0.1, y goes from -0.8 to 0.0
        x1 = -0.2 * (1-t) + (-0.4) * t  # Swing out slightly
        y1 = -0.8 * (1-t) + (0.2) * t   # Shoot up
        
        # T2 mirrors
        x2 = 0.2 * (1-t) + (0.4) * t
        y2 = -0.8 * (1-t) + (0.2) * t
        
        status = "GRAVITY TURN"
        scale_label = "MESO (1mm)"

    # PHASE 3: THE COLLAPSE (0.6 to 1.0)
    # The dive into the Trefoil Knot at the top vertex
    else:
        t = (progress - 0.6) / 0.4
        
        # Center of the knot is near the top vertex (0, 1.0)
        cy = 0.2 + 0.8 * t # Move center up
        
        # Radius shrinks
        r = 0.6 * (1.0 - t * 0.8) 
        
        # Frequency increases (The "Diving" action)
        freq = 2 * np.pi * (1 + t * 4) 
        
        # Trefoil-ish winding
        # x = r * (sin(f) + 2sin(2f))
        # y = r * (cos(f) - 2cos(2f))
        
        # T1
        x1 = r * np.sin(freq) 
        y1 = cy + r * np.cos(freq) * 0.5 # Flattened ellipse approach
        
        # T2 (Phase shifted)
        x2 = r * np.sin(freq + np.pi)
        y2 = cy + r * np.cos(freq + np.pi) * 0.5
        
        status = "KNOT FORMATION"
        scale_label = f"QUANTUM (1e-{int(t*15)}m)"

    return (x1, y1), (x2, y2), status, scale_label

# ======================
# 3. VISUALIZATION
# ======================
def create_animation():
    img = generate_wada_substrate(RES)
    
    fig = plt.figure(figsize=(10, 12), facecolor='#050505')
    gs = GridSpec(3, 2, height_ratios=[1, 3, 0.5])
    
    # Views
    ax_t1 = fig.add_subplot(gs[0, 0])   # T1 Cam
    ax_t2 = fig.add_subplot(gs[0, 1])   # T2 Cam
    ax_main = fig.add_subplot(gs[1, :]) # God View
    ax_hud = fig.add_subplot(gs[2, :])  # Metrics
    
    for ax in [ax_t1, ax_t2, ax_hud]:
        ax.axis('off'); ax.set_facecolor('black')
    ax_main.axis('off')

    # History
    hist_x1, hist_y1 = [], []
    hist_x2, hist_y2 = [], []

    def update(frame):
        prog = frame / FRAMES
        (x1, y1), (x2, y2), status, scale = get_positions(prog)
        
        # Update History
        hist_x1.append(x1); hist_y1.append(y1)
        hist_x2.append(x2); hist_y2.append(y2)
        if len(hist_x1) > 40: # Tail length
            hist_x1.pop(0); hist_y1.pop(0)
            hist_x2.pop(0); hist_y2.pop(0)

        # --- MAIN VIEW ---
        ax_main.clear(); ax_main.axis('off')
        # Background
        ax_main.imshow(img, extent=[-2.2, 2.2, -2.2, 2.2], origin='lower')
        
        # Tails
        ax_main.plot(hist_x1, hist_y1, color='cyan', lw=2, alpha=0.5)
        ax_main.plot(hist_x2, hist_y2, color='magenta', lw=2, alpha=0.5)
        
        # Heads
        ax_main.scatter([x1], [y1], color='cyan', s=120, edgecolors='white', zorder=10)
        ax_main.scatter([x2], [y2], color='magenta', s=120, edgecolors='white', zorder=10)
        
        # Connection (Wound Channel)
        ax_main.plot([x1, x2], [y1, y2], color='white', linestyle='--', lw=1, alpha=0.6)
        
        ax_main.set_xlim(-2.2, 2.2)
        ax_main.set_ylim(-2.2, 2.2)

        # --- TRAVELER CAMS ---
        # T1 View (Looking at T2)
        ax_t1.clear(); ax_t1.axis('off')
        ax_t1.set_xlim(-1, 1); ax_t1.set_ylim(-1, 1)
        rel_x, rel_y = x2-x1, y2-y1
        dist = np.sqrt(rel_x**2 + rel_y**2)
        
        ax_t1.scatter([0], [0], color='cyan', marker='+', s=50) # Self
        ax_t1.scatter([rel_x], [rel_y], color='magenta', s=50+50/dist) # Target
        ax_t1.text(0.05, 0.9, "TRAVELER 1 FEED", color='cyan', transform=ax_t1.transAxes, fontsize=8)
        
        # T2 View (Looking at T1)
        ax_t2.clear(); ax_t2.axis('off')
        ax_t2.set_xlim(-1, 1); ax_t2.set_ylim(-1, 1)
        ax_t2.scatter([0], [0], color='magenta', marker='+', s=50)
        ax_t2.scatter([-rel_x], [-rel_y], color='cyan', s=50+50/dist)
        ax_t2.text(0.05, 0.9, "TRAVELER 2 FEED", color='magenta', transform=ax_t2.transAxes, fontsize=8)

        # --- HUD ---
        ax_hud.clear(); ax_hud.axis('off')
        hud_text = f"""
        NARRATIVE PHASE: {status}
        SCALE:           {scale}
        SEPARATION:      {dist:.4f} units
        """
        ax_hud.text(0.5, 0.5, hud_text, color='lime', fontfamily='monospace', 
                   ha='center', va='center', fontsize=11)
        
    print(f"[*] Rendering {FRAMES} frames...")
    anim = FuncAnimation(fig, update, frames=FRAMES, interval=50)
    anim.save('inevitable_knot.gif', writer=PillowWriter(fps=FPS))
    print("[✓] Saved to 'inevitable_knot.gif'")

if __name__ == "__main__":
    create_animation()