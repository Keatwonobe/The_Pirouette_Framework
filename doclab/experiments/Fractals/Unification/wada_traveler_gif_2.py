import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource

# =========================================================
#  CONFIGURATION: THE WADA NEEDLE (3D)
# =========================================================
RES = 300       # Resolution for 3D plot (keeping it lighter than 2D map)
ZOOM = 4.0      # Viewport width
STEPS = 400     # Increased depth to grow the "needle"
DT = 0.05
R_ESCAPE = 10.0

def get_acceleration(m, l):
    # Hénon-Heiles Gradient
    acc_m = -(m + 2 * m * l)
    acc_l = -(l + m**2 - l**2)
    return acc_m, acc_l

def run_history_scan_3d():
    print(f"[*] Scanning Manifold Topography ({RES}x{RES})...")
    
    # Grid
    x = np.linspace(-ZOOM/2, ZOOM/2, RES)
    y = np.linspace(-ZOOM/2, ZOOM/2, RES)
    M, L = np.meshgrid(x, y)
    
    VM = np.zeros_like(M)
    VL = np.zeros_like(L)
    
    total_phase = np.zeros_like(M, dtype=float)
    active = np.ones_like(M, dtype=bool)
    
    prev_angle = np.arctan2(L, M)
    
    for t in range(STEPS):
        am, al = get_acceleration(M, L)
        
        VM += am * DT
        VL += al * DT
        M += VM * DT
        L += VL * DT
        
        curr_angle = np.arctan2(L, M)
        delta = curr_angle - prev_angle
        delta = (delta + np.pi) % (2 * np.pi) - np.pi
        
        phase_increment = np.abs(delta)
        total_phase += phase_increment * active
        
        prev_angle = curr_angle
        
        r2 = M**2 + L**2
        escaped_now = (r2 > R_ESCAPE**2) & active
        active[escaped_now] = False
        
        if not np.any(active):
            break
            
    return total_phase

print("[*] Generating Data...")
history_data = run_history_scan_3d()

# Prepare for 3D Plotting
print("[*] Rendering 3D Surface...")
fig = plt.figure(figsize=(12, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d', facecolor='black')

x = np.linspace(-ZOOM/2, ZOOM/2, RES)
y = np.linspace(-ZOOM/2, ZOOM/2, RES)
X, Y = np.meshgrid(x, y)

# Z = Log Phase (Complexity Height)
# Add small epsilon to avoid log(0)
Z = np.log1p(history_data)

# Custom Colormap "Magma" (Black -> Red -> White)
# We plot surface with stride to keep it rendering fast but looking smooth
surf = ax.plot_surface(X, Y, Z, cmap='magma', 
                       rstride=2, cstride=2, 
                       linewidth=0, antialiased=False,
                       shade=True)

# Lighting for dramatic "Mountain" effect
ls = LightSource(azdeg=315, altdeg=45)
rgb = ls.shade(Z, cmap=plt.cm.magma, vert_exag=0.5, blend_mode='soft')

# Clean up axes for "Void" aesthetic
ax.set_axis_off()
# ax.grid(False) # Turn off grid
# ax.set_xticks([])
# ax.set_yticks([])
# ax.set_zticks([])

# Adjust View Angle to see the "Needle" structure
ax.view_init(elev=50, azim=45)

ax.set_title("THE WADA NEEDLE | 3D Complexity Manifold", color='white', fontsize=16)

plt.tight_layout()
plt.savefig("wada_needle_3d.png", dpi=150)
print("✅ 3D Visualization Saved: wada_needle_3d.png")