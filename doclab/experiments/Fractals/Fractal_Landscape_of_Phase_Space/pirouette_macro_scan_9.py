import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d import Axes3D

# --------------------------------------------------
# PIROUETTE SPEED MANIFOLD (ROBUST VERSION)
# --------------------------------------------------
# Fixed to handle the 60K "Resonance Zone" crash.
# --------------------------------------------------

# Configuration
RANGE = 6000000000000.0  # The crash zone
RES = 300
STEPS = 400 
DT = 0.05
GAMMA = 0.02
TWIST = 2.83814

def get_force_numpy(m, lam):
    # Vectorized Physics
    F_teal_m = -(m + 0.866) 
    F_teal_lam = -(lam - 0.5)

    F_red_m = -m
    p_violation = TWIST * np.sin(m * 2.5) 
    F_red_lam = -(lam + 1.0) + p_violation

    sum_m = (F_teal_m + F_red_m)
    sum_lam = (F_teal_lam + F_red_lam)
    mag = np.sqrt(sum_m**2 + sum_lam**2)
    # Avoid div by zero in scale if mag is 0
    scale = np.sqrt(mag)
    
    F_gold_m = sum_m * scale
    F_gold_lam = sum_lam * scale
    
    # Weights
    angle_deg = (np.degrees(np.arctan2(lam, m))) % 360.0
    
    def get_w(target):
        d = np.abs(angle_deg - target)
        d = np.minimum(d, 360.0 - d)
        return np.exp(-(d/80.0)**2)

    w_gold = get_w(30.0)
    w_teal = get_w(150.0)
    w_red = get_w(270.0)
    
    tot = w_gold + w_teal + w_red + 1e-6
    nw_red = w_red / tot
    nw_teal = w_teal / tot
    nw_gold = w_gold / tot
    
    Fm = (nw_teal * F_teal_m + nw_red * F_red_m + nw_gold * F_gold_m)
    Flam = (nw_teal * F_teal_lam + nw_red * F_red_lam + nw_gold * F_gold_lam)
    
    return Fm, Flam, w_red

def generate_speed_manifold(res, rng):
    x = np.linspace(-rng, rng, res)
    y = np.linspace(-rng, rng, res)
    M, L = np.meshgrid(x, y)
    
    m = M.flatten()
    lam = L.flatten()
    pm = np.zeros_like(m)
    plam = np.zeros_like(lam)
    
    print("Simulating Particle Acceleration...")
    for _ in range(STEPS):
        Fm, Flam, w_red = get_force_numpy(m, lam)
        drag = 1.0 / (1.0 + 0.5 * DT * GAMMA * w_red)
        pm = (pm + 0.5 * DT * Fm) * drag
        plam = (plam + 0.5 * DT * Flam) * drag
        m += DT * pm
        lam += DT * plam
        
        # SAFETY CHECK: If values explode, clamp them mid-sim
        # This prevents float overflow before it happens
        m = np.clip(m, -1e10, 1e10)
        lam = np.clip(lam, -1e10, 1e10)
        
    # Calculate Speed
    speed = np.sqrt(pm**2 + plam**2)
    
    # Final Safety Polish
    speed = np.nan_to_num(speed, nan=0.0, posinf=1e6, neginf=0.0)
    
    # Reshape
    Speed_Grid = speed.reshape(res, res)
    
    # Log Scale
    Log_Speed = np.log1p(Speed_Grid)
    
    return Log_Speed

print(f"Generating Speed Manifold (Range +/- {RANGE:,.0f})...")
Z = generate_speed_manifold(RES, RANGE)

print("Rendering 3D Surface...")
x = np.linspace(-RANGE, RANGE, RES)
y = np.linspace(-RANGE, RANGE, RES)
X, Y = np.meshgrid(x, y)

fig = plt.figure(figsize=(16, 12), facecolor='black')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('black')

ls = LightSource(azdeg=315, altdeg=45)
rgb = ls.shade(Z, cmap=cm.plasma, vert_exag=0.1, blend_mode='soft')

surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=rgb,
                       linewidth=0, antialiased=False, shade=False)

ax.xaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.yaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.zaxis.set_pane_color((0.0, 0.0, 0.0, 0.0))
ax.grid(False)
ax.axis('off')
ax.view_init(elev=55, azim=-45)

plt.tight_layout()
filename = f"pirouette_speed_manifold_{RANGE}.jpg"
plt.savefig(filename, dpi=100)
print(f"Saved to {filename}")
plt.show()