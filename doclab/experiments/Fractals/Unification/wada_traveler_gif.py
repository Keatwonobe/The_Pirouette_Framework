import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from numba import njit, prange

# =========================================================
#  CONFIGURATION: THE WADA IMPACT
# =========================================================
RES = 800
ZOOM = 4.0   # Zoom out to see the 3 escape channels (The "Arch")
STEPS = 200
DT = 0.05

# Hénon-Heiles Constants
# Escape Radius (if r > this, it has left the center)
R_ESCAPE = 10.0 

@njit(fastmath=True)
def get_acceleration(m, l):
    # Hénon-Heiles Gradient (Force = -Grad V)
    # V = 0.5(m^2 + l^2) + m^2*l - 1/3*l^3
    
    # dV/dm = m + 2ml
    acc_m = -(m + 2 * m * l)
    
    # dV/dl = l + m^2 - l^2
    acc_l = -(l + m**2 - l**2)
    
    return acc_m, acc_l

@njit(parallel=True)
def compute_basins(res, zoom):
    """
    Determines the Fate of every pixel (The Wada Map).
    0 = Trapped (Black)
    1 = Exit A (Top Right)
    2 = Exit B (Top Left)
    3 = Exit C (Bottom)
    """
    wada_map = np.zeros((res, res), dtype=np.int32)
    
    x_range = np.linspace(-zoom/2, zoom/2, res)
    y_range = np.linspace(-zoom/2, zoom/2, res)
    
    for i in prange(res):
        l0 = y_range[i]
        for j in range(res):
            m0 = x_range[j]
            
            # Initial State (Released from rest)
            m, l = m0, l0
            vm, vl = 0.0, 0.0
            
            status = 0 # Default: Trapped
            
            for t in range(STEPS):
                # Symplectic Euler / Velocity Verlet-ish
                am, al = get_acceleration(m, l)
                vm += am * DT
                vl += al * DT
                m += vm * DT
                l += vl * DT
                
                # Check Escape
                r2 = m*m + l*l
                if r2 > R_ESCAPE**2:
                    # Determine Exit Channel based on Angle
                    angle = np.arctan2(l, m)
                    
                    # Angles for Hénon-Heiles Exits (approximate sectors)
                    # The triangle points up/down depending on sign convention.
                    # Based on your potential: V = ... - l^3/3. 
                    # This points the "cliff" towards +y or -y?
                    # Let's just classify by raw angle sectors.
                    
                    if angle < -2.6 or angle > 2.6:
                        status = 1 # Left-ish
                    elif angle > -0.5 and angle < 2.6: # Top/Right
                        status = 2 
                    else:
                        status = 3 # Bottom
                    
                    break
            
            wada_map[i, j] = status
            
    return wada_map

def compute_trajectory(m_start, l_start, dt, steps):
    """
    Traces a single particle path.
    """
    path_m = []
    path_l = []
    
    m, l = m_start, l_start
    vm, vl = 0.0, 0.0 # Standard traveler starts from rest? 
                      # OR does it have initial velocity?
                      # If it's the "Traveler" from the previous GIF, 
                      # it was a scattering event. Let's assume it carries momentum.
                      # To see the "Impact", let's shoot it AT the center.
    
    # Let's fire a particle FROM the Void (Bottom Left) TOWARDS the center
    # Initial setup for a "Collider" shot
    
    # Actually, to match the "Void Head" concept, let's just trace 
    # the evolution of a point *near* the instability (the saddle).
    
    m, l = m_start, l_start
    vm, vl = 0.0, 0.0 # Release from the "cliff edge"
    
    for _ in range(steps):
        path_m.append(m)
        path_l.append(l)
        
        am, al = get_acceleration(m, l)
        vm += am * dt
        vl += al * dt
        m += vm * dt
        l += vl * dt
        
        if m*m + l*l > R_ESCAPE**2:
            break
            
    return path_m, path_l

# =========================================================
#  EXECUTION
# =========================================================

print("[*] Mapping the Wada Basins (This defines the Void Head)...")
wada = compute_basins(RES, ZOOM)

print("[*] Tracing the Traveler Trajectory...")
# We pick a point on the "Blade" of the fractal (unstable ridge)
# A point slightly offset from center usually rides the ridge
traj_m, traj_l = compute_trajectory(0.01, -0.1, DT, 200)

# Visualization
fig, ax = plt.subplots(figsize=(10, 10), facecolor='black')

# Custom Wada Colormap
# 0=Black (Core), 1=Teal, 2=Gold, 3=Magenta (The 3 Fates)
colors = ['#000000', '#00cccc', '#ffaa00', '#cc00cc']
cmap = ListedColormap(colors)

# Plot Basin Background
extent = [-ZOOM/2, ZOOM/2, -ZOOM/2, ZOOM/2]
ax.imshow(wada, origin='lower', extent=extent, cmap=cmap, alpha=0.9)

# Plot Traveler Path (The "Pierce")
ax.plot(traj_m, traj_l, color='white', linewidth=2, alpha=0.8, label='Traveler Path')
ax.scatter([0], [0], color='red', marker='x', s=100, label='Impact Point')

ax.set_title("THE WADA IMPACT | Traveler vs Destiny", color='white', fontsize=14)
ax.legend(loc='upper right')
ax.axis('off')

plt.tight_layout()
plt.savefig("wada_impact_overlay.png", dpi=150)
print("✅ Visualization Saved: wada_impact_overlay.png")