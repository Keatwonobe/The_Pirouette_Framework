import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
import io

# =========================================================
#  TIME FRACTAL: INTERFERENCE & ANIMATION ENGINE
# =========================================================

# Configuration
RES = 300
ZOOM_WIDTH = 12.0 # Slightly wider to catch the tips of the triangle
CENTER = 0.0
DT_MAG = 0.1
EPSILON = 1e-5

class PirouetteHamiltonian:
    def gradient(self, m, l):
        dV_dm = m + 2 * m * l
        dV_dl = l + (m**2 - l**2)
        return np.array([dV_dm, dV_dl])

class TensionScanner:
    def __init__(self):
        self.physics = PirouetteHamiltonian()
        
    def scan_frame(self, steps, dt_val):
        """
        Generates a tension map for a specific duration and direction.
        """
        # Grid Setup
        m_vals = np.linspace(CENTER - ZOOM_WIDTH/2, CENTER + ZOOM_WIDTH/2, RES)
        l_vals = np.linspace(CENTER - ZOOM_WIDTH/2, CENTER + ZOOM_WIDTH/2, RES)
        M, L = np.meshgrid(m_vals, l_vals)
        
        # Initialize Reality (1) and Shadow (2)
        m1, l1 = M.copy(), L.copy()
        pm1, pl1 = np.zeros_like(M), np.zeros_like(M)
        
        m2, l2 = M + EPSILON, L + EPSILON
        pm2, pl2 = np.zeros_like(M), np.zeros_like(M)
        
        # Max Divergence Tracker
        max_div = np.zeros_like(M)
        
        # Physics Loop
        # We manually unroll the loop slightly for speed or just keep it simple
        for _ in range(steps):
            # Update Reality
            grad1_m = m1 + 2 * m1 * l1
            grad1_l = l1 + (m1**2 - l1**2)
            
            pm1 -= 0.5 * dt_val * grad1_m
            pl1 -= 0.5 * dt_val * grad1_l
            
            m1 += dt_val * pm1
            l1 += dt_val * pl1
            
            grad1_m = m1 + 2 * m1 * l1
            grad1_l = l1 + (m1**2 - l1**2)
            
            pm1 -= 0.5 * dt_val * grad1_m
            pl1 -= 0.5 * dt_val * grad1_l
            
            # Update Shadow
            grad2_m = m2 + 2 * m2 * l2
            grad2_l = l2 + (m2**2 - l2**2)
            
            pm2 -= 0.5 * dt_val * grad2_m
            pl2 -= 0.5 * dt_val * grad2_l
            
            m2 += dt_val * pm2
            l2 += dt_val * pl2
            
            grad2_m = m2 + 2 * m2 * l2
            grad2_l = l2 + (m2**2 - l2**2)
            
            pm2 -= 0.5 * dt_val * grad2_m
            pl2 -= 0.5 * dt_val * grad2_l
            
            # Calc Divergence
            dist_sq = (m1 - m2)**2 + (l1 - l2)**2
            # Update max divergence (keep largest seen so far)
            max_div = np.maximum(max_div, dist_sq)
            
            # We don't break early here to keep the map uniform for the animation
            # (unless it explodes to infinity, but we want to see the explosion)

        return np.log(np.sqrt(max_div) + EPSILON)

def create_image_from_data(data, title):
    fig, ax = plt.subplots(figsize=(6, 6), facecolor='black')
    
    # Magma is good for energy/tension
    im = ax.imshow(data, origin='lower', cmap='magma', 
                   extent=[CENTER-ZOOM_WIDTH/2, CENTER+ZOOM_WIDTH/2, CENTER-ZOOM_WIDTH/2, CENTER+ZOOM_WIDTH/2])
    
    ax.set_title(title, color='white', fontsize=12)
    ax.axis('off')
    
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png', dpi=100)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)

# =========================================================
#  EXECUTION
# =========================================================
scanner = TensionScanner()
frames = []

# 1. Backward (Void) Sequence: Steps 30 -> 1
print("[*] Generating Void Approach (Negative Time)...")
final_reverse_data = None

for s in range(30, 0, -1):
    # Integrate backwards
    data = scanner.scan_frame(s, -DT_MAG)
    if s == 30: final_reverse_data = data
    
    img = create_image_from_data(data, f"VOID APPROACH | T = -{s}")
    frames.append(img)

# 2. Forward (Chaos) Sequence: Steps 1 -> 30
print("[*] Generating Chaos Eruption (Positive Time)...")
final_forward_data = None

for s in range(1, 31):
    # Integrate forwards
    data = scanner.scan_frame(s, DT_MAG)
    if s == 30: final_forward_data = data
    
    img = create_image_from_data(data, f"CHAOS ERUPTION | T = +{s}")
    frames.append(img)

# Save GIF
print("[*] Saving GIF...")
frames[0].save(
    "henon_heiles_impact.gif",
    save_all=True,
    append_images=frames[1:],
    optimize=False,
    duration=100, 
    loop=0
)
print("✅ GIF Saved: henon_heiles_impact.gif")

# 3. Interference Image
print("[*] Calculating Interference...")
# Product of the two 30-step maps
# Since data is Log, sum them? Or multiply?
# Visual product: data_fwd * data_rev
interference = final_forward_data * final_reverse_data

fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')
im = ax.imshow(interference, origin='lower', cmap='inferno', 
               extent=[CENTER-ZOOM_WIDTH/2, CENTER+ZOOM_WIDTH/2, CENTER-ZOOM_WIDTH/2, CENTER+ZOOM_WIDTH/2])
ax.set_title("INTERFERENCE: The Standing Wave", color='white', fontsize=15)
ax.axis('off')
plt.tight_layout()
plt.savefig("henon_interference.png", dpi=150)
print("✅ Interference Saved: henon_interference.png")